---
title: Joinmarket
transcript_by: Bryan Bishop
tags:
  - coinjoin
speakers:
  - Adlai Chandrasekhar
date: 2016-10-08
media: https://www.youtube.com/watch?v=8BLWUUPfh2Q&t=2196s
---
<https://twitter.com/kanzure/status/784681036504522752>

slides: <https://scalingbitcoin.org/milan2016/presentations/D1%20-%202%20-%20Adlai%20Chandrasekhar.pdf>

Finding a risk-free rate for Bitcoin

Joinmarket, just to clear up a misconception... <a href="https://github.com/JoinMarket-Org/joinmarket">Joinmarket</a>, like bitcoin, it is a protocol. Not a company. The protocol is defined by an open-source reference implementation. There are other versions of the code out there. It's entirely, I guess you could say it's voluntary like bitcoin. Those of you who might have less of a finance background might not be familiar with the term risk-free rate. When you are investing fiat currency, you invest the government bonds, and it gives you a low return. It's not just fungibility, it's also an investment.

I am one of the joinmarket contributors. Some of the other joinmarket developers are here today. We actually haven't had a definition of fungibility yet. It's the property where equal amounts of some commodity or some monetary good or whatever are interchangeable. In the case of mushrooms, you don't want to interchange equal weights of different strains. But in the case of bitcoin, most software will treat equal quantities of bitcoin the same. It's people that go look at the history and violate the fungibility.

We're trying to make their job more difficult. Another interesting quote from cypherpunks more than 2 decades before joinmarket occurred, Eric Hughes foresaw this development. "It's a way to transfer a non-private good in a more private manner". So what is anonymity and privacy?

## What is privacy?

Anonymity is always within a set. An important concept is that of an <a href="https://en.wikipedia.org/wiki/Degree_of_anonymity">anonymity set</a>. You're one of a few billion people. You're one of a few million bitcoin users. You are one of a thousand joinmarket users. If you are at a protest wearing a certain mask, then you are one of those people. If you show up with the wrong mask, then suddenly your anonymity set is a lot smaller. So the purpose of fungibility is to increase your anonymity set.

There are two kinds of privacy protection: against "Kid sister"s, or against governments. The same is true for privacy as well. You can fool most of the people most of the way, but you can only be a saint for six confirmations before the devil knows you're dead. Governments and nosy spouses can figure out which coins are yours. We are more focused on giving people privacy that stands up to the privacy tracking startups, and to casual observation.

There's also the concept of hiding and the concept of deniability. Attacking startups that say this customer of yours is using a gambling site or whatever-- they can't actually do that. They are just saying we found a link. They give the estimate. But they can't prove that the link is you. So you have deniability even from regular bitcoin use. We try to give you better deniability but you have to go to great lengths to actually hide and have people not able to tell at all what your transaction graph is.

If you get enough deniability with enough different plausible explanations, then you are hiding behind a smokescreen of possible explanations.

Before Joinmarket, users would just use all sorts of arbitrary methods. They would buy an altcoin, send it to another exchange, sell it back, send through wallets, send through gambling sites, and arguably these methods-- they give you worse privacy. So there are sites dedicated to unlinking. They call themselves "tumblers" which is a reference to "coin tumbling" where you collect old coins and mix them with sand and water as polish. When you use a fungibility technology that everyone else is not using, then your coins become dirty. A tracking startup would notice you are trying to be private. So your personal transaction graph might be more difficult to track, but overall, your coins are as distinguishable as privatized(?) coins.

Greg Maxwell proposed <a href="https://bitcointalk.org/index.php?topic=279249.0">Coinjoin</a> and <a href="https://bitcointalk.org/index.php?topic=321228.0">Coinswap</a> in 2013 on bitcointalk. Coinjoin has gained traction, but Coinswap has not unfortunately. Darkwallet offered P2P Coinjoin, without a central server, but you had to wait a very long time-- hours or even days until enough people with enough bitcoin were online at the same time. And then you could make a Coinjoin using Darkwallet.

Just in case someone has not seen what a coinjoin looks like, <a href="https://i.imgur.com/mys3yC9.png">here is an example</a>.

## Coinjoin

This is arguably the simplest smart contract. We have two participants. One participant has this output here, the other one has two outputs, the first and the third one. They each get 0.8 BTC out. There's no way for you to look at this transaction and knows which output corresponds to the first input or the middle input.

## Joinmarket goals

Joinmarket's goals emerged from that status quo, the prior part that I described. First of all, no counterparty risk. We don't want to be a centralized mixing service. We're not going for strong privacy. It's difficult. It uses complex mathematics, which most bitcoin users don't understand. Possibly even most people! It has to be a liquid tool. It must be highly available. You muts be able to show up with hundreds of coins and get some fungibility right away. You should be able to make coinjoins on-demand.

It has to be compatible with the existing "vanilla" bitcoin protocol. Some people might not like this attitude, but we don't want users to install any different software other than the client they have today. So if you use a 5-year old bitcoin client, which doesn't have an RPC command that we use, we consider that a bug. Please let us know.

It's probably pretty obvious, but we want a system that is usable. If it's not usable, then it's not useful. We're going for a working tool that people can use as soon as possible.

## Joinmarket participants and users

Joinmarket's fundamental innovation, which I think several people came up with independently, is ythat you compensate people for participating in the protocol. So you incentivize people to leave their clients running. Also this brings in more liquidity. People who don't care about fungibility do care about making money. So you increase the anonymity set as a user of running joinmarket. There are people investing dozens or 100s of coins. They would usually leave them in cold storage and forget about them for a year or more. Instead they are now running hot wallets and they are increasing other people's anonymity sets.

Joinmarket divides participants in two different roles. There are passive participants or "makers". And then there are iniators/takers. Initiators have sporadic participation. If you are a participant, then you sign transactions that look okay with you. If you are an initiator, then you coordinate and assemble transactions. Initiators pay fees, and participants earn them.

Because the initiators are coordinating transactions, they learn some information about the other participants. So the regular participants get less privacy than the initiators. If you want the best possible privacy, then you have to pay for it.

## Protocol

I'll run through the protocol quickly. If you want to get a precise idea, read the code.

Participants publicly advertise liquidity, and fee expectations. Initiators pick which counterparties they want. They contact them with an encryption key and the amount they want to transfer. In coinjoin, everyone has to use the same amount. The participant applies each one separately with the encryption key. From this point onwards, everything happends with end-to-end encryption in a hub-and-spoke model. Each participant has an end-to-end encrypted channel. Participants sign encryption keys with bitcoin keys. We sign the encryption key so that you know you're talking with someone who owns those bitcoin rather than someone who just wandered in.

The participants reply with the unspent outputs that they want to use as their inputs, and the addresses to which they want their new outputs pointing and finally, they sign with their bitcoin key. The initiator signs and then broadcasts. That's how we get coinjoin.

You may notice a problem. The initiator is the last one to sign. What if they don't sign? They have learned the mapping-- which inputs belong to which makers. They know additional unused addresses of those makers. So if they don't sign at the end, then they have learned this for free.

This attack was known for a while. We didn't want to withhold a project with some theoretical attack. Over the summer, we saw the successful transaction count increasing, but in parallel there very suddenly appeared about three to ten times as many failed transactions where someone would start the protocol, and break it off partway, after learning the mapping. We called this a <a href="https://github.com/JoinMarket-Org/joinmarket/issues/156">snoop attack</a>. This was not a <a href="https://en.wikipedia.org/wiki/Sybil_attack">sybil attack</a>, which was a common misconception.

The snoop attack is free. It doesn't cost the snooper anything. We can prevent this entirely. You can pay for the transaction and learn the mapping. So the second protocol has the same basic sequence. We add a signature on every message. The key thing here is that the takers don't just sign the encryption key with a bitcoin key. They commit with a unique commitment to some bitcoin some unspent bitcoin doesn't even have to be the same one. What does this mean that it's a unique commitment? Every bitcoin that exists currently generates one commitment. If you have seen a commitment, you can't figure out which bitcoin created it. If you see the same commitment again, you know it's the same. This lets the makers and the participants not talk to people who are initiating multiple transactions. Effectively, it puts a cost on snooping. You can still snoop, but you have to create new coins each time. We have not yet seen anyone conducting a snoop attack on this second protocol. So either this was a sufficient discouragement, or they are still writing code and collecting funds and perhaps the snoop attack will continue. Remains to be seen.

## Future directions

We have two wallet integrations that are written, but they need more review and testing. Electrum and Core.

We have a hybrid mode that doesn't quite work yet, where if you don't have to make a transaction immediately, you can participate in other transactions and earn perhaps more fee than for your own transaction.

We want to expose an API so that existing services, or exchanges, can use a hot wallet and also joinmarket at the same time. An exchange could offer their customers to earn money with coinjoin. I think a testnet faucet does this today, although not in a programmatic manner.

Joinmarket is the first market of its kind. A lot of coin flowing through it, and there was an estimate of about $1 million/month. I didn't calculate it, so I'm just <a href="https://www.bitcrime.de/presse-publikationen/pdf/BoehmeMoeser_Anonymity_WEIS2016.pdf">quoting it</a>. People are earning money here. Some participants are earning more than others. We want to look at how much people are earning, what are the optimal fee strategies, how can you maximize your earnings? There's a lot of unmined data here, it's sitting in the blockchain all public.

We want a tool where we can measure what privacy someone could have and could get after using Joinmarket. Right now it's pretty obvious that using a single Coinjoin is almost useless. Doing 100 Coinjoins is confusing to your attacker-- but where do you draw the line? These Coinjoins cost coin. People pay per join.

Also, we want to implement coinswap because the cool thing about coinswap is that whereas in coinjoin the anonymity set is the participants in that specific coinjoin, but in coinswap the anonymity set is everyone who was doing a coinswap at the same time, even if they were not coordinating with each other. Achieving that level of anonymity set increase using chained coinjoins is a lot more expensive, and I doubt that's the right strategy; the right strategy is to offer the additional protocol.

## Q&A

Q: How does this compare to <a href="https://bitcointalk.org/index.php?topic=567625.0">coinshuffle</a>?

A: Coinshuffle, for those who aren't familiar with it, is a protocol for creating a coinjoin transaction in a manner that requires less mutual information sharing amongst the participants. It's similar to <a href="http://ddg.gg/?q=multiparty+computation">MPC</a> protocols, and eventually results in a coinjoin which should be indistinguishable from one created using other protocols. It solves the most naive version of the snooping attack. The problem is combining the snooping attack and sybil attack. Someone could run multiple joinmarket clients. If you're initiating multiple transactions, you can eliminate the coins that you know belong to you. You can see which coins belong to the other users. If you can isolate a single participant, such as if you run 3 participants, and you initiate, and you contact 1 additional participant. It'll cost you capital expense, you have to tie up the bitcoin to run the participants, and you have to pay fees, but you can still learn information. It's not a perfect fix.

Q: What percentage of joinmarket users are using onion routers?

A: Tor? I would be surprised if anyone is using i2p. I'm not sure if you can connect to joinmarket servers for i2p. We use servers for communication channels. They don't have access to the end-to-end encrypted data. They do see some activity, I suppose. So what percentage is using onion routing? It's supported by the code. You change false to true, you get onion routing as long as you have tor running on the same computer. We have not collected that information because we are not spying on our users.

Q: You mentioned coinswap versus coinjoin. Can you elaborate on whether you see doing future work towards coinswap?

A: So personally I am one of those who independently thought abou the incentivization idea, and I imagined it with coinswap. I think building coinswap from the start is a much more scalable solution. You get a large anonymity set from the beginning. You need discretized amounts; if you have one coinswap with size of 1 coin, parallel to one with 2 coins, it's obvious that it's not the same people. But if everyone is amking coinswwaps with size 1, 10, 100, etc., then you have these tiered anonymity set. I think it's much better. To achieve the same size of anonymity set using parallel coinswaps or chained coinjoins, you would end up putting a lot more data in the chain. At the moment, joinmarket is loading the chain. Each initiator is creating some constant factor size transaction larger than regular transactions. Whereas a coinswap transaction is 4 transactions, happening in parallel with other set of coinswap transactions ycould give you roughly the same anonymity set as going one coinjoin of six participants... or many coinjoins, an entire switching network of coinjoin with fewer participants. 50 people doing coinswap in parallel, you would need a tremendous network of coinjoins to even come close to that. Coinswap is a much more stateful protocol. You don't just exchange information, sign and broadcast. You fund multisig addresses, then you exchange information, then you either take out your new coins, or you wait for a locktim to expire if a counterparty vanishes--- so coinswap is more complex of a protocol to implement. "Usable is useful" dictates that coinjoin be done first.

<https://github.com/JoinMarket-Org/joinmarket>

