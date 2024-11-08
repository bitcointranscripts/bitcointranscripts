---
title: Fungibility Overview
transcript_by: Bryan Bishop
tags:
  - privacy-problems
  - privacy-enhancements
speakers:
  - Matt Corallo
  - Adam Back
date: 2016-10-08
media: https://www.youtube.com/watch?v=8BLWUUPfh2Q&t=500s
---
<https://twitter.com/kanzure/status/784676022318952448>

## Introduction

Alright. So let's get started. Okay. Why fungibility? Let's start. What does fungibility mean? Bitcoin is like cash. The hope is that it's for immediate and final payments. To add some nuiance there, you might have to wait for some confirmations. Once you receive a bitcoin, you have a bitcoin and that's final. So even with banks and PayPal, who sometimes shutdown accounts for trivial reasons or sometimes no reason at all, it's typically not the case that it's someone who sent you money... if you were selling something on ebay, and someone bought an item from you, and that person had an account shutdown, the money you received will not be removed from your account. This effects-- the multiple hops of people sending you bitcoin, if they are associated with som trade on Silk Road or something like that, it turns out that some exchanges and wallets are using taint-tracing services and up to 4 hops away from you, if something is associated with Silk Road, they will ask you to freeze your funds and take your funds elsewhere. The reality is that for people using bitcoin on those services, the fungibility in bitcoin is actually worse than Paypal, because other people's actions unrelated to you-- and 4 hops away is a very long way away-- and potentially anyone who has done any trades with bitcoin is 4 hops away; it's a very interconnected system. There's a social networking theory that everyone is within 13 hops globally of everyone else. Paypal doesn't freeze your funds if your customer's customer's do something bad; and in bitcoin this is happening because of companies...

Your lack of fungibility impacts everyone else. So fungibility costs are externalized. Everyone needs fungibility, or nobody has it. "Nothing hide nothing to fear" doesn't work because while you might have nothing to hide, you don't necessarily know how the data is going to be interpreted in the future. This impacts the value of the coin because it becomes worse money.

Fungibility can impact permissionlessness. It's a critical feature of bitcoin that we have this permissionless. You need fungibility for bitcoin to function. If you receive coins and can't spend them, then you start to doubt whether you can spend them. If there are doubts about coins you receive, then people are going to go to taint services and check whether "are these coins blessed" and then people are going to refuse to trade. What this does is it transitions bitcoin from a decentralized permissionless system into a centralized permissioned system where you have an "IOU" from the blacklist providers. Obviously, we don't want this to happen. If you don't have permission to transaction, then you wouldn't have bitcoin. If someone had to go to a central service to check if their coins are invalid, then this could eventually lead to collapse and lapse of confidence. There is precidence in physical money that there are court cases in the distant pass where there were concepts about for money to be functional, it has to be fungible. So there are rules against... if you unknowingly received lost property, and it turns out it's stolen, then you lose and have to give it back. But with cash and paper money, that's not the case,by law in most countries in the world. That's because of this issue where if you can't have confidence about receiving money, then it makes the currency non-functional and it impacts the economy.

<http://diyhpl.us/wiki/transcripts/bitcoin-adam3us-fungibility-privacy/>

## Taint tracing

Taint tracing is backwards looking. It's not so much "who is receiving the money" but rathr backwards up to 4-hops. Who was involved in the money? It's primarily focused on grouping transactions from individual groups of senders, or the UTXOs and who owns those. This is in part.... there are a series of academic papers that look at network analysis, and there are factors about the way bitcoin is used that makes taint analysis easier. Most inputs tend to come from a single donor, so that correlates UTXOs to the belonigng to the same person.

Address reuse is bad.

Another type of attack is network address taint tracing. When someone broadcasts a transaction, then people connect to nodes on the network and try to identify the IP address of the sender by looking at trickle on the network.

Different wallets send slightly different network transactions too, because of differences in parameters. This reduces the anonymity set, where the anonymity set is the set potential of senders.

Transaction censorship is another attack.

## Scalability

Fungibility can be a tradeoff with scalability. In some cases, fungibility can hurt scalability. Sometimes fungibility can bring a large scalability improvement. The reason why fungibility impacts scalability s because fungibility aims to reduce information leakage-- so this means that sometimes less information goes into the blockchain. And conversely, if we have extremely high scalability, like transaction throughput and bandwidth, this can also in the other direction help fungibility because we can use some types of fungibility that use more data like <a href="http://diyhpl.us/~bryan/papers2/bitcoin/Borromean%20ring%20signatures.pdf">ring signatures</a> and <a href="https://people.xiph.org/~greg/confidential_values.txt">confidential transactions</a> (see also <a href="http://diyhpl.us/wiki/transcripts/gmaxwell-confidential-transactions/">this talk</a>).

## Transaction graph privacy: Address reuse

Address reuse, most wallets are using hierarchical deterministic wallets, which has advantages for backup scenarios. Another type of address privacy is the "stealth address" which hasn't been so much used because it's difficult to find payments. So you have to be a full node or you have to rely on a third party service to scan the network for you.

## Transaction graph privacy: inputs and outputs

I think this transaction graph privacy refers to the concept of peope being able to scan th eblockchain and being able to analyze the flow of transactions, that's probably what people think of the most for fungibility. So the most obvious thing to solve fungibility is <a href="https://bitcointalk.org/index.php?topic=279249.0">coinjoin</a>. It's great. Depending on how coinjoin is done, it can be a slight improvement in scalability. It can reduce the size of transactions, some. It primarily focuses on increasing your anonymity set, making it more private as to which inputs correlate to which outputs, which makes transaction graph analysis a bit harder. It's not a massive win, but we will talk about that in a second.

Tumblebit authors are going to present soon (<a href="http://diyhpl.us/wiki/transcripts/scalingbitcoin/milan/tumblebit/">tumblebit presentation</a>). I'm going to leave this out. It's a big scalability win.

Lightning is obviously a massive scalability improvement. It came out of being a scalability solution; it was not designed to be for fungibility. However, it has onion routing for pamyents, so if your goal is to increase privacy about where coins are going and where they came from, then onion routing is one of the big things that everyone hopes for.

Another thing that people think about is <a href="http://diyhpl.us/~bryan/papers2/bitcoin/Ring%20CT%20for%20Monero.pdf">ring signatures</a>, which was pioneered by Monero. People like to talk about Monero as a more private bitcoin. Monero, the way it accomplishes better privacy is to for each input spending a given output, you spend an output but you don't identify which one, but you can validate that the transaction is valid, fi you try to double spend the network can detect it. You can increase your anonymity set here. You can't say "this output was directly related to this input" you can't do that.

The next solution that we have kinda for input-output privacy is <a href="http://diyhpl.us/~bryan/papers2/bitcoin/Increasing%20anonymity%20in%20bitcoin%20using%20one-way%20aggregatable%20signatures.pdf">one-way aggregate signatures</a>. I don't think an altcoin has implemented this yet. It's a good idea. The effect on fungibility is that it's coinjoin for every block. A block becomes a single large transaction. You can't correlate inputs and outputs other than they appeared in the same block. There's still some analysis you can do on the p2p network layer, but it's great for fungibility in consensus history. It has some additional cryptographic assumptions, though. The way that people have proposed doing OWAS is perhaps a little weaker in crypto assumption terms; it has been less studied than the other forms of cryptography. So it is hard to bet a lot of money in it immediately.

Zcash is a bigger step towards fungibility-- it hides essentially everything about a transaction, you can only see that a transaction happened at all. It has much different cryptographic assumptions. zkSNARKs are very new and have been studied much less. It's awesome technology, however it's highly... it's laughably large blocks, it's unscalable. Large transactions. Takes a long time to validate transactions.

<a href="http://diyhpl.us/wiki/transcripts/scalingbitcoin/milan/mimblewimble/">Andrew Poelstra will be talking about mimblewimble later</a>. It has OWAS-like protection, ring signature-like protection, and has awesome scaling as well.

So let's move on.

## Balance privacy

A big way which people identify transactions as from the same sender is able to group and split transactions according to different groups of senders. This is balance privacy. The biggest example is that in a given transaction you can see the inputs and outputs and it's often easy to correlate which output is the change, just based on the output value. A way that people fix this in coinjoin is balance discretization, so that every output is 0.1 BTC or 1 BTC. This is obviously expensive in terms of scalability. You need more transaction outputs to represent the same value.

This is where confidential transactions (CT) comes in. It's much more expensive cryptographically-- more operations, longer to validate, bigger signatures on the inputs, but it's essentially giving you the same zcash-style privacy of balances where you can see nothing about the balance other than it was a valid spend of the previous output without needing to do any discretization where you have a number of outputs per value.

Mimblewimble of course again, it's kind of an extended version of confidential transactions. I'll let Andrew Poelstra get to that.

Zcash also again, it has the same properties where you can't see anything about the transaction going in or out, but again terrible scaling.

## Network attacks

Let's talk about network attacks. They are kind of the biggest way that we see fungibility loss today. Across the netwrk, if you have a node online for a short period of time, there's some Chainanalysis firm that makes 50 connections to your nodes instantly. They claim to be Android wallet but they don't even have the same behavior. So they connect to everyone and do this heavily to correlate transactions and where they came from, which happens to be a good indicator of who sent the transaction.

Big issue in the network stoday and privacy of the users is <a href="https://github.com/bitcoin/bips/blob/master/bip-0037.mediawiki">bip37 bloom filters</a>. I'm sorry. I wrote that. It's terribly not private. There have been a bunch of posts, one in 2015 and a few before that, essentially the way that the "SPV" wallets do blockchain sync today is they send your addresses to all the peers, and if you're a Chainanalysis service, then this is massively detrimental because you're telling them the exact set of addresses, so they can connect which address and which IP addresses are connected to you in the future and they can watch as you move across the network. There's a few solutions we have for that, like committed bloom filters are maybe a solution. There has been some work in the mailing list regarding flipping away that people do scanning of the chain for addresses in a private way.

Connect-to-everyone attacks. They make 50 connections to everyone. This is terrible. Luckily this is one fo the few slides where I can say there's not just lots of ways we can fix fungibility but Bitcoin Core has been putting work into how it relays transaction, so that it doesn't say when you receive a transaction. This will improve the trickle analysis defense. Someone coming from a Chainalysis service opened a pull request against Bitcoin Classic asking this change to be reverted so they could do "better more compliant tracking" and this was obviously rejected from Bitcoin Classic as well.

There has been a lot of effor t randomizing the order in which transactions are sent to your peers. Randomness is not sufficient. Some various anonymity software like tor and such fought hard to learn that randomness is not sufficient protection for anonymity. If you have enough points, you can plot them and then see whether they match the random curve and then group transactions based on that. So it's not great.

In Bitcoin Core 0.14 and later, there's some work going in. But randomness has got a lot of work.

Improving transaction relay across the network is a good start. It's still the case though that man-in-the-middle attacks, like a global passive adversary, can identify where transactoins come from. The bip151 talk tomorrow will be interesting on this front. In Bitcoin Core, there has been some research about how to do really private relay, like if you're willing to wait for transaction relay using mixnets, where you can run an external daemon and you can handle some transactions to the daemon and then it does some crazy mixnet.... it would be deeply appreciated if someone would go finish that work.

## Transaction features identifications

A lot of chain analysis anti-fungibility services have become good at identifying which transactions come from which wallets. Coin selection is one way to determine who you are. A lot of coin selection algorithms give away which output is your chain output, and which wallet you were using based on the change output amount. Many of the coin selection methods are deterministic, so if someone wants to guess, then they can confirm whether they were right based on watching your transactions.

Finally, fee selection-- which fee are you using? This could give away whih wallet you're using.

Another issue is which scripts are used. These scripts are identifiabe. <a href="http://diyhpl.us/wiki/transcripts/scalingbitcoin/milan/schnorr-signatures/">Pieter will talk about Schnorr signatures</a>. People have also thought about using ...   <a href="https://github.com/bitcoin/bips/blob/master/bip-0114.mediawiki">MAST</a>.. using a <a href="https://en.wikipedia.org/wiki/Merkle_tree">merkle tree</a> over the script to reveal only part of the script. This is wonderful because you can say either a multisig of all the participants, or we run whatever contract we were attempting to do, so every transaction looks like a multisig in the default case.

Finally, <a href="https://github.com/scipr-lab/libsnark">zkSNARK-based systems</a>... this would be kind of gold standard in that all scripts would look the same.

So finally there's some non-script transaction features, like in Bitcoin Core, there is incentive compatibility where it sends all transactions with a locktime of the current blockheight so that it can only confirm at the next blockheight. This unfortunately gives away the fact that you are using Bitcoin Core.

## Transaction censorship

If someone can successfully censor your coins or any transaction that spends your coins, then your coins are less valuable. If they take 1 day to confirm or 6 hours to confirm, or they can't confirm, then that's really nasty because your coins are now worth much less than other coins. Right now there's no evidence that miners are doing anything gnarly here. However, it would be better if we could always make sure of this. In the near term, if miners continue to be honest, we would like software to notify people that miners have gone bad if they are coerced (perhaps by the US government) or something...

The final one is encrypted transactions. There has been a lot of work thinking about this. You commit to a transaction, the chain knows nothing about the transaction or which coins were moving. This is great for preventing transaction censorship. If the miners don't know what they were mining, then they can't censor you.

## Conclusions

If you were paying close attention, you might have noticed that a lot of layer 2 solutions like <a href="http://lightning.network/">Lightning</a>, a lot of fungibility solutions involve moving transfers off-chain. As Adam mentioned, this is incredibly powerful because there's less knowledge of all the data moving around. So it's much harder to attack fungibility. Sometimes having more transactions improves your anonymity set size.

Most of these things have not been implemented or don't have heavy use-- but we do know how to fix bitcoin and make it act like what we want it to be, rather than the traceable asset it acts like today.








