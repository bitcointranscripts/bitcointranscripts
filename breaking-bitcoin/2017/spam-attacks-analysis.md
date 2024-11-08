---
title: Hunting Moby Dick, an Analysis of 2015-2016 Spam Attacks
transcript_by: Bryan Bishop
tags:
  - research
  - security-problems
speakers:
  - Antoine Le Calvez
date: 2017-09-09
media: https://www.youtube.com/watch?v=eCE2OzKIab8&t=1h12m10s
---
<https://twitter.com/kanzure/status/1005525351517360129>

## Introduction

Hi. Thanks for Breaking Bitcoin to invite me to speak and to present this research on Moby Dick.

Moby Dick and spam attacks-- let me explain, Moby Dick is an entity that spammed or sent a lot of transactions in bitcoin in 2015. We did some analysis on who this person is or what they were doing. This is bitcoin archaeology, where we analyze past activities and try to analyze what happened and get insight into what could happen.

Who am I? I am Antoine Le Calvez. I created p2sh.info in 2014 which is a website that releases statistics on bitcoin that I find interesting. I like to dig into stuff like spam attacks. I have been doing this work with LaurentMT.

There's been some research about what these in particular on spam attacks.. there was a published paper, but we tried to dig deeper and present insights.

## A note about spam

Spam is a word that is thrown around a lot, especially since the bitcoin debates got heated.

On a blockchain, it's a bit hard to know what is spam. Labeling something as spam could be contentious from time to time. We also have the example of services being inefficient about not batching transactions or just doing silly things. It's hard for someone to come in and say this is spam or not spam. And one of the goals of bitcoin is to not centrally censor transactions.

General rules about spam-- it's unsolicited, it's high volume. Thankfully for the attacks that we saw, or the transactions we studied, we knew they were stress tests or spam attacks. That made it easier for us to be comfortable saying this is spam or not, even though people could argue.

A lot of people saw the chart of number of UTXOs which grew steadily through 2014-2015 and one day just grew up and continued growth. The spam attacks we studied created many UTXOs. They were very visible at the time where people saw full blocks.

If we look at the small UTXOs between 1k and 10k sat BTC, we see that they had these low values and match the definition of spam.

## Semi-manual analysis

To dive deeper into this, we used something called semi-manual analysis. It's not automated.

We look at transactions, patterns in fees, input numbers, output numbers, in value. We found some distinct waves of spam that each happened.

Wave 1: between 2015-06-16 and 2015-07-01 Claimed by coinwallet.eu. 10k sat UTXOs.

Wave 2: between 2015-07-06 and 2015-07-17. Made miners produce 1 megabyte blocks, including a monster 1 MB block with 2 transactions. 1k sat UTXOs.

Wave 3: between 2015-07-25 and 2015-08-09. This is the most mysterious one, with 1k sat outputs.

Wave 4: between 2015-09-01 and 2015-09-07. This was claimed by coinwallet.eu, and had 1k sat UTXOs.

These were "stress tests" claimed by coinwallet.eu. The second wave happened a bit later and they reduced the size of the outputs and it was less money to spend. It was the first time that a one megabyte block that was mined, and it had a single transaction that took a while to process.

The biggest one we have less information about who did it and why. And the last wave, wave 4, happened a bit later.

That's how it looks on the network. The second wave was the most interesting as it used many different patterns of creating UTXOs. It was sending money to private keys, to services, etc. Money was sent to wikileaks and many different parties -it was a bit of a party on the network.

There were millions of UTXOs created in a matter of days or weeks. We wanted to dig deeper into this one because it had more meat. There was one where people were creating UTXOs and just claiming them later- less interesting.

## Overall statistics

* 2.78 GB of block space (2.2% of current blockchain)
* 268 BTC in fees (9.6 sat/byte average)
* 1.34 million transactions (0.05% of total)
* 2 million UTXOs still unspent (3.7% of current UTXO set)

In 2015, 268 BTC was somewhat expensive. They had to create the UTXOs and the spending of the outputs. It's not the same person that bears the cost of not cleaning up or spending the money. It was 1.3 million transactions, which now is a few days but back then it was a lot of transactions.

There's still 2 million UTXOs that every node has to store in memory. It looks like it's not going to go down, unless someone spends or gives away the private keys, and with the rising fees it's less economically viable for these coins to get spent. It's a burden on all the nodes.

## A two step dance

The main attack had a two step dance aspect where someone created outputs in days, one party. It took many months for people to spend them- the services, the attackers, it's not clear who was on the receiving side of it. It was effected by network conditions and backlogs. The effect has now dissipated after other waves of activity which are still in the UTXO set. But for this one, we-- here we start-- pure facts, we start speculating.

## A strange timing

There was a comment: "Don't pay attention to those spam broadcasts, as all miners have been ignoring them since October by using the minrelaytxfee command line/bitcoin.conf option" -- jtoomim, May 2016

You can see at the red line, it looked like these transactions would be stopped processing, but it started again. To relay a transaction, it has to pay at least 1 sat/byte. These were not. They were under the min relay fee. There was a 2 week backlog around July 26 before the transactions... the blocks were sort of empty, not empty though. By some miners, not all of them, these were getting mined. There's more to talk about this that LaurentMT talked about in some medium articles.

This may have been produced for political reasons to fill blocks when there was not a big demand for it.

## What can we do?

We cannot people from spending their money. That's the whole point of bitcoin. But we can try to prevent inefficient use of bitcoin. I would like everyone to be able to spend their coins but to do it in a least impactful way, in a highly efficient way.

High volume activity is still doable but fees can mitigate this. The fee market can compete against attacks.

The targets could use segwit- cheaper claiming of outputs. It used to be cheaper to create outputs than to spend them. If you don't spend them then you don't have the burden of spending them later. Segwit reduces this asymmetry. But it's still present- it still costs more to spend an output than to create it.

Raising the dust limit could work. It's the minimum for a transaction to be relayed. Raising depends on the fee. It's defined as the amount that is economically spendable.

Better monitoring would be useful. People see the mempool clog up and assume there's spam. There needs to be more tools to be transparent about what's going on. The network is not necessarily under attack. We need some way to make it clear what is high volume activity, which is supposedly legitimate, and high-volume activity that seems to be spam.

Coin selection algorithms could be spam-resistant if it is optimized to deal with low value outputs and to ignore those. There's incentive for some people to send low value outputs so that coin selection algorithms pick them up and spend them. People might try to do this to leak outputs together, which is bad for privacy.

## Conclusion

If you have any questions or ideas-- we tried our best to figure this out, but we would like to learn more in tandem with the community. The more information, the more enlightened we are. Thank you.
