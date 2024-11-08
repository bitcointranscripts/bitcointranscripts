---
title: Privacy Concepts for Bitcoin application developers
transcript_by: Bryan Bishop
tags:
  - privacy-enhancements
  - privacy-problems
speakers:
  - Udi Wertheimer
date: 2019-09-09
aliases:
  - /scalingbitcoin/tel-aviv-2019/edgedevplusplus/privacy-concepts
---
<https://twitter.com/kanzure/status/1171036497044267008>

## Introduction

You're not going to walk out of here as a privacy protocol developer. I am going to mention and talk about some ideas in some protocols that exist. What I find myself is that of really smart people working on a lot of pretty cool stuff that can make privacy easier and better to use. A lot of times, application developers or exchanges aren't even aware of those things and as a result the end result is that people just sometimes use bitcoin in very non-private ways because they're not aware of how to do privacy.

## Privacy

Which of you have read the bitcoin whitepaper? That surprises me, not everyone's hand went up. You can read it, it's like 9 pages. It's not a lot. Of those 9 pages, about half a page talks about privacy. I think it's kind of an oversight. Satoshi talks about some problems with privacy when all data is public but there's this one quote which says "well, privacy can still be maintained by rbeaking the flow of information in another place: by keeping public keys anonymous" which is kind of true but keeping public keys truly anonymous is really, really hard.

## Let's talk about privacy

We'll talk about why you should care about privacy for bitcoin, and how bitcoin data leaks, and what we can do to protect user data.

## Why should we care about privacy?

There are many reasons to care about privacy. Bitcoin privacy is unintuitive. It's not like traditional services where we at least kind of understand it. If we share stuff on Facebook, then we know Facebook has the data and could always sell the data. That's easy to reason about. With bitcoin, since everything is kind of public, we might not be aware that we're sharing data that anyone around us can find out about us. It's not just the companies that Facebook sells the data to. A lot of people who have access to bitcoin services because they bought some bitcoin, they might not be aware of any of this. They might have heard from the news media that bitcoin is anonymous.

Even users that do understand that there's some tricks here, they sometimes have unrealistic expectations. They might think, OK I'll just use tor and everything will be hidden and we'll be safe. That's not really true. They might think, all of my problems are going to be solved if I use a privacy coin. Whatever you choose to use, you should be aware of how it works and what it gives you and how you can work around the problems.

All that said, it's probably possible to use bitcoin in a private way.

Another reason to protect privacy is because leaking user data can hurt your application or your business. Users might be using other companies that are surveilling the blockchain and might cancel the user's account for doing business with you. Accidentally exposing data on employees is also bad. You might reveal confidential business data, like transaction flows or number of customers.

## How does bitcoin data leak?

Let's talk about some imaginary scenarios but I hope I can share my imagination with you and see what I'm talking about.

Let's say you're an employee at some company and your employer pays you in bitcoin. Once a month, you get a 0.5 BTC payment from your employer. A few days later, you move 0.1 BTC to your landlord for your rent. This is a transaction that everyone can see, including your employer and your landlord. The landlord can use heuristics to infer that you still have 0.4 BTC left each month. The landlord can then raise rents because he knows that you're able to pay. Not to mention, what happens if the landlord is friends with your co-workers? In this scenario, the amount and timing data is leaked.

Some people might not like paying for VPNs. Bob pays for a VPN and he uses a custodial wallet to do this. And the custodial wallet is based in the country that Bob lives. That's not the smartest thing to do, but Bob just isn't aware of that. The VPN uses a new address each time they send an invoice to Bob. But when the service pays their hosting provider, someone who just gives them the infrastructure that they use, they make them --- they combine, they make a transaction that combines Bob's payment with some payment from a spy from this country and then send this to the host that they use. Now the spy knows that Bob paid the VPN service. If both coins end up in the same transaction, then you can infer they are being spent by the same entity when the VPN service provider mixes their coins. Bob might then get suspended because his country doesn't like that he was using a VPN.

One heuristic is that if there's two inputs in a transaction and one output, then you can generally infer that both inputs belong to the same entity.

Another use case is business income sold on an exchange. Claire's business receives a payment from a client. The exchange always shows the same deposit address for all the deposit for the same user. This is surprising, many exchanges do this. It's really bad. So suddenly Claire's client can see all the payments made to Claire because they can look at that one deposit address and see all the people making payments into that address. So now you can see all of Claire's clients and see how often they pay, how much they pay, and their other transactions. So that's not great.

Another potential leak is in lite clients. Let's say Meg uses a light client, like mobile wallets, or electrum (with default settings at least), or software bundled with hardware wallets like Tredger or Lezor. The way these light clients work is that instead of downloading the entire chain, they query some server that is remotely operated. And that server might be some random node operated by some operator, and the server operator can be recording all of the requests that the wallet makes to this server. This can deanonymize your entire wallet. This remote node not only knows all of your addresses that you sent it, but also knows your IP address and then can connect it to you. So that's not great. The wallet operator ends up with this weird database of balances of pretty much all of their users. If you think of someone using a hardware wallet wihch they consider safe and they use them for long-term savings, then suddenly this company has a database that they probably don't want.

There's a similar leak when you use block explorers online. If you give them your address, then they will note that you're interested in those addresses. Generally, don't type in your address into search engines either. It's the same problem because it indicates interest.

Some people might say use Tor and hide from traffic analysis. You hide some of it, like your IP address, but the remote server or remote node will still know the list of addresses you're interested in, or the fact that a Tor user is interested in that address, which leaks some additional information itself.

## Preventing leaks

For your company or service, I recommend using your own Bitcoin Core full node. Definitely use your own full node. It shouldn't be too difficult for a business to do this. The reason why full nodes are great for privacy is because they download all the data and all the blocks. People connected to you can't tell what you're interested in, except to the extent that they can detect what transactions you're broadcasting and initiating.

The next step that might be relevant to some applications, like for wallets, if you're releasing an app that the user is supposed to download, then maybe give them the option of adding a full node that will start up and sync in a friendly way. It can be a remote full node that is a backend for the wallet. There's some desktop lightning wallets that have started to do this, which is an interesting experiment. But it has drawbacks; it means that the user would have to first sync the node. But you can use pruning to save disk space. Some people might not be aware of the possibility of pruning, which means you can run a full node with only 5 GB of space including UTXOs which isn't too much.

Giving the users the ability to connect to their own remote full node, such as their full node at home, then maybe the mobile wallet should let users connect remotely. Yes, this is about incoming transactions right now, but I'll get to sending in a moment.

For some people, full nodes might not be a realistic option. At least a lot of the times, a good fallback might be client-side filtering like [Neutrino](https://diyhpl.us/wiki/transcripts/breaking-bitcoin/2019/neutrino/). Basically client side filtering means that-- each block has a deterministic filter, and your client checks the filter in the blockheader, and if it's interesting then it will download the full block and process it locally. Not a lot of data leaks there becvause there's a lot of transactions in each block and it's hard to tell which one you're interested in. There's some false positives, though. Which is probably good-- it tells you yes you should download a block but then you find nothing that is interesting to you, but that's probably good because it strengthens the privacy.

If you're going to do that, you should fetch blocks from different peers. Maybe use tor and switch tor circuits between fetching of each block this way you don't look like the same person doing it.

You might be interested in looking at bip17 and bip158. I think this is implemented in btcd already. There's at least a pull request in Bitcoin Core. I am not sure if it's merged yet. It's probably coming.

## Broadcasting transactions

So far we've talked about incoming transactions and verification of transactions sent to you. But what about transactions that you spend and send? In the default case, you have a number of peers and you broadcast your transaction to all of your peers. If the peers aren't actively trying to track you, then it's fine but what happens if all the nodes that you are connected to happen to be spies or a surveillance company? There are companies that run nodes like this, to analyze where transactions originate. If they are all of the connected nodes you're connected to, and they learn about the transaction from you, then you're probably the one making that.

One way to get around this is Dandelion bip156. It's not merged yet, it's a proposal. There's a stem phase where when you create the transaction you first send the transaction to one node. That one node is going to flip a coin and decide if they're going to only send it to another one node, or if they are going to flip to the fluff phase where they send it to everyone. If you're anyone in the stem phase, you can't be sure if the person who sent it to you is the first one or not. If you're in the fluff phase, you don't know if the person who sent it to you was the last member of the stem phase.

In the future, you can use dandelion and tor at the same time, for broadcasting.

Q: If all the peers I'm connected to are surveillance company nodes, and I post a dandelion transaction, then I'm screwed because they know that I'm the originator of the transaction.

A: If all of them, then you're probably screwed. But what about a mix of surveillance nodes instead of all of them being sybils? The idea is that the transaction could come from any of the honest nodes.

Q: What about censorship?

A: ....

Q: How is dandelion better than just broadcasting the transaction?

A: You can use statistics in the default case to more easily figure out who originated the transaction.

You can use tor to mask the IP address of where you send the transaction from. But you should know that whoever you're sending to might still try to link the transactions from the same session. So you might want to switch tor circuits between broadcasts. One thing that you might choose to do is, in your application, choose some public API for broadcasting. Some block explorers have an endpoint for broadcasting transactions. Maybe if you use that, then all of your users use the same thing, and then the anonymity set grows, but it has costs in censorship resistance because if this endpoint stops working then you can't use it. So that's a tradeoff.

## Don't reuse addresses

If I didn't have a microphone in my hand, I would be clapping now. Don't. Reuse. Addresses. It should be obvious and simple. Don't. Reuse. Addresses. Please don't do it. If you're a bitcoin exchange or work for one, please, allow people to get new deposit addresses every time they make a deposit. This should be the default. I guess the reason why exchanges don't do this is because of customer support requests and people that get confused? But you should help them understand, because this really hurts their privacy and probably in some way hurts your business because it opens the doors for frontrunning and a lot of other problems. If you detect address reuse, then you should probably say something about it to the user. Tell the user so that they can stop doing it. That would be very useful. Things would be so much better if there was no address reuse. That's really an easy one.

## Coin selection

Another thing is UTXO selection. When you build a wallet, please let users select their own UTXOs when they build transactions. A lot of pro users do this anyway. I think it's not that difficult to understand this concept. This is an option if people consider it. Allow people to label transactions. When you get a transaction from say Kraken, you should be able to say that this transaction comes from Kraken not just for your own record but in the future when you spend this transaction it might be useful to you to know where it came from so that you know what kind of information you're revealing to the recipient that you're paying. You should select what you're okay with them knowing or not okay with telling them.

## Coinjoin

<https://diyhpl.us/wiki/transcripts/breaking-bitcoin/2019/breaking-bitcoin-privacy/>

<https://diyhpl.us/wiki/transcripts/building-on-bitcoin/2018/coinjoinxt/>

<https://diyhpl.us/wiki/transcripts/scalingbitcoin/milan/joinmarket/>

<https://diyhpl.us/wiki/transcripts/bitcoin-adam3us-fungibility-privacy/>

## Confidential transactions

<http://diyhpl.us/wiki/transcripts/gmaxwell-confidential-transactions/>

<https://diyhpl.us/wiki/transcripts/realworldcrypto/2018/mimblewimble-and-scriptless-scripts/>

## Schnorr and taproot

<http://diyhpl.us/wiki/transcripts/sf-bitcoin-meetup/2018-07-09-taproot-schnorr-signatures-and-sighash-noinput-oh-my/>

Generally, Schnorr signatures and the Taproot proposal could allow for different transactions that do different things but they will look the same. It's useful. If you can think of, I don't know, maybe you use a very weird transaction type. It's usually easy to deanonymize you based on that, but using Schnorr and Taproot can enable those weird transactions to look like normal transactions. Another option is to make regular scripts use other realistic-looking branches that are impossible to reach, to increase the anonymity of what the real script is that you're using.

## More resources

<https://en.bitcoin.it/wiki/Privacy>

dandelion <https://github.com/bitcoin/bips/blob/master/bip-0156.mediawiki>

client side filtering: bip157, bip158 <http://diyhpl.us/wiki/transcripts/breaking-bitcoin/2019/neutrino/>

Taproot <https://github.com/sipa/bips/blob/bip-schnorr/bip-taproot.mediawiki>

