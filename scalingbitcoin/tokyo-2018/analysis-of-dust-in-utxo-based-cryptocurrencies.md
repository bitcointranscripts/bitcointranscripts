---
title: An analysis of dust in UTXO-based cryptocurrencies
transcript_by: Bryan Bishop
speakers:
  - Sergi Delgado Segura
date: 2018-10-06
media: https://www.youtube.com/watch?v=YgtF7psIKWg&t=2256
---
Cristina Pérez-Solà, Sergi Delgado Segura, Guillermo Navarro-Arribas and Jordi Herrera (Universitat Autònoma de Barcelona)

Sergi Delgado Segura

<https://eprint.iacr.org/2018/513.pdf>

<https://twitter.com/kanzure/status/1048380094446632961>

## Introduction

Thank you everyone. I am glad to be here today to tell you about our analysis of the UTXO set in different cryptocurrencies. This is shared work with the other coauthors listed. The outline is that I'll talk about the UTXO set, then I'll talk about definitions, our results, and our conclusions. I am going to define some of the things we've been dealing with and how we've been calculating things for our analysis.

## UTXOs

To start, unspent transcation outputs (UTXOs) is a transaction output that has not yet been spent. It's from a previous transaction. When we talk about bitcoins, we are talking about values stored by UTXOs. All those UTXOs are stored in the UTXO set, which is part of every single bitcoin full node. We have one entry in the UTXO set for each output. It doesn't matter the owner or the conditions of the UTXO for spending it, and it doesn't matter the value. We always have only one single entry for each coin.

## Properties of the UTXO set

The UTXO set is part of every full node. The bitcoin value of a UTXO does not affect its size. Bigger value does not mean a bigger amount of data stored in the UTXO set. In general, the larger the output script of a UTXO, the more space stored in the UTXO set.

## Analysis goals

We wanted to see how many unspent outputs were actually worth spending. How much space is being devoted to storing worthless dust UTXOs that are unspendably small?

## Outputs worth spending

What do we mean when we talk about unspendably small outputs? How much data does such an output contribute to a new transaction that would be spending that new transaction? What is the fee rate we would need or want to pay for spending that UTXO? This depends on the transaction fee weather.

## Bitcoin Core dust definition

Dust: Bitcoin Core defines **dust** as an output that costs more in fees to spend than the value of the output. To compute the cost of spending an output, both its size and the size of the input are considered. It used to be that when were checking dust, we used to mean an output that would have to pay more than 1/3rd of its value in fees. But recently, the definition has changed. They are basically counting an output as-- it has to spend more in fees than the face value of the bitcoin. There is a new is\_dust function. There are different constants used here for segwit and non-segwit outputs.

## Our definitoin: unprofitable outputs

Unprofitable: We define an **unprofitable** output as the output of a transaction that holds less value than the fee necessary to be spent, taking into account **only the size of the input** that will be needed to spend it. Our goal was to try to predict which inputs we were going to bring and which size we would need. The predicted size of the input that will spend an output. There's also the segwit reduction to consider here as well.

But how do we know the size of an input before we see it? Here's the basic structure of a transaction. There's a version, a few bytes for the number of inputs, and then each input. We compute the minimum size by setting the fixed size, and then a variable size. The fixed size is the output + nSequence whic his going to be 40 bytes. So the variable size is the script length and another factor.

We have two different metrics for unprofitability: a lower bound on unprofitablility that will take into account the minimum size of the input. Then there's an estimation of unprofitability that tries to estimate the real unprofitable rates taking into account data available in the blockchain. We analyze the blockchain data to help with this aspect.

## Variable size: non-segwit outputs

For pay-to-pubkey (p2pk) outputs, there's a PUSH sig and a signature, the lower bound is like 72 bytes. We also analyzed pay-to-multisig (p2ms). We also consider compressed and uncompressed keys.

## Variable size: segwit outputs

We look at public key sizes in the bitcoin blockchain. We get every single public key ever used in every single transaction in the blockchain and then compute the average pubkey size depending on the block. When we were checking certain UTXOs in the set and we wanted to know what was exactly the most probable size of this public key... we took the average of.. and then put it into the ...

## P2SH redeem scripts in the bitcoin blockchain

We looked at several redeem scripts such as multisig, p2wpkh, p2wsh, non-standard, p2pk, p2pkh, and p2sh (hash puzzle). We can count the number of inputs and hte average input size, which is 210 bytes. This also depends on the block size.

## Results

Here is a graph of percentage of UTXOs and the fee rate (sat/byte). Which fraction of the UTXO set can be counted as dust or non-profitable? Depending on the fee rate, we were using a quite wide fee rate. If the fee rate is 0, then there's no unspendably small UTXOs basically. But at 350 sat/byte fee rate, the percentage of unspendable UTXOs is closer to 60%. If we look at the total bitcoin supply and the amount of BTC in circulation, the total amount of dust is like less than 0.000025... so we are wasting half of the size of the utxo set to store an astonishingly small amount of BTC.

## Unprofitability evolution of bitcoin

This is nothing new. This has been going on for years. We're reaching a certain point at which this will become a real problem. You may think this is not so bad... you might ask, is this a problem? We performed this analysis for bitcoin and also other projects. I'm not trying to blame litecoin, I'm just showing data. Almost 80% of all the UTXOs in litecoin are actually dust or almost nothing. This has been going on since the beginning. The main reason for this is that around 67% of the UTXOs in a UTXO set in litecoin are worth exactly 1 satoshi LTC. This happened at the beginning of the coin when it was easy to perform these attacks; but this can happen today in bitcoin, it might be more expensive so you might need an attacker with a lot of money and incentives to do it, but it could happen.

## Conclusions

There is a fairly big percentage of dust in the UTXO set. The current implementation of the UTXO set can grow unboundedly. The bigger the set gets, the less suitable it is to run a full node in low resource devices. Dust attacks can be performed to make the set grow. Nowadays the UTXO set is around 4.5 gigabytes. If you try to get that into RAM on low-RAM devices, you're going to get a problem. And it is going to keep growing, and anyone can cause UTXO set growth size.

There has been some proposals to mitigate this such as TXO commitments from petertodd. That's the only one I'm aware of. I think Bram Cohen has talked about this. Folks should do output consolidation when fees are low. A good coin selection algorithm is important, especially for bitcoin exchanges.

I think nobody expected fees becoming so high a year ago. So we should try to avoid this before it gets to be a problem again. Whether we like it or not, a huge amount of transactions on the network are from exchanges.


