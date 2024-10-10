---
title: Challenges in implementing coinjoin in hardware wallets
transcript_by: delcin-raj via review.btctranscripts.com
media: https://www.youtube.com/watch?v=gqINXwsR33g
tags:
  - coinjoin
  - hardware-wallet
  - taproot
speakers:
  - Pavol Rusnak
date: 2023-03-02
---
## Introduction

Hi everyone. I'm Pavel Rusnak, known as Stik in the Bitcoin community. I'm the co-founder of Satoshi Labs, the company that brought Trezor.  Today I'm going to be talking about the challenges of implementing CoinJoin in hardware wallets.

### Why Privacy

 Let's summarize why privacy matters. Among all reasons I consider these reasons as most important.
* **Autonomy**:  Privacy allows individuals to have control over their personal information, enabling them to make independent choices and decisions.
* **Personal safety**: Privacy protects individuals from harm or danger, such as stalking, harassment, or identity theft.
*  **Freedom of expression**: Privacy encourages free expression and open communication.
* **Trust**: Privacy is essential for building trust between individuals and institutions.
* **Equality**: Privacy helps ensure that everybody is treated equally, regardless of race, gender, religion, and so on.
* **Democracy**: Privacy is critical to maintaining democracy by enabling citizens to communicate freely with one another and their representatives.
* **Innovation**. Privacy promotes innovation by providing a safe environment for individuals and companies to experiment and develop new ideas and technologies without fear of theft and abuse.
So, it can be summarized that privacy is a fundamental human right that protects individual autonomy, safety, and freedom, as well as promoting trust, equality, democracy, and innovation.

## Privacy in Bitcoin

### What is the state of Bitcoin privacy?

Transactions are recorded on a public blockchain and can be traced and analyzed by anyone, even retroactively.  The identity of transaction parties is not necessarily known, but these identities are very often linked through various means.  So, that means IP address tracking, and public information disclosure.  Examples of linking transactions to identities include publishing one's bitcoin address for donation in Twitter or Nostr profile, especially in combination with address reuse is a big issue. But not as big as exchange and other customers' practices.
### What are the privacy-enhancing technologies?

* There are confidential transactions, which is a method which obfuscates transacted amounts, but we need to verify that no Bitcoins were created or destroyed in the process.  These are usually deployed as sidechains. We don't have confidential transactions in the Bitcoin base layer.
* Then there is Lightning Network, which helps with privacy because blockchain now shows only channels open and closes, but it does not show individual transactions.
* There are services like Tor and VPNs where you can hide your user's IP address and thus location.  And it's harder to link transactions together. For example, in Tor, you can switch identities when performing different transactions and then you see them as a different person online.
* And, of course, there is CoinJoin.

## CoinJoin

So, what's CoinJoin?  It's a privacy-enhancing technique to increase the anonymity of Bitcoin transactions.  And it happens when multiple parties agree to merge their transactions, meaning inputs and outputs, into a single larger transaction.  And the resulting transaction makes it more challenging to link individual inputs and outputs to their respective owners.  CoinJoin can be much bigger than this, but this is just an example.
### Example

Consider three participants agree to join their transactions with 5 + 3 outputs (3 takes the change outputs into consideration). Consider three on the input side, you can probably guess that this change output belongs to that person and so on.  But you can't tell anything about other outputs.  You don't know whether this output belongs to that person or that person or that person.
So, the idea is let's create outputs of the same size.  And these clusters of same-sized outputs, gain something that we call k-anonymity.  So in this example, the group of outputs have k-anonymity where k is five because you can't guess which person this output belongs to.

### Phases of a CoinJoin

1. **Input registration** where each participant registers their input at a coordinator.  This happens usually via Tor, so a different Tor identity is used for each input.  For each successful input registration, a coordinator gives a participant something I will call a token, but it's not like a cryptocurrency token.  It can be, for example, a blind signature that's used in Wasabi 1, or a keyed verification anonymous credential which is used in Wasabi 2.  I don't get into the details of what this means, but the important thing is that you are given this token and you can use this token in the second phase, which is output registration.
2. **Output Registration** where each participant registers their outputs at the coordinator via a different Tor identity again.  What's important here is that these are different identities than those used in the input registration, so there is no link.  Each output registration presents a token, which is proof that you are allowed to register output of a certain size.  This token is burned, which means that the CoinJoin coordinator marks it as used.  Usually, this token is tied to a CoinJoin round, so it's not usable in another round.  And that's good because then this marked or used list can be discarded after the CoinJoin round.  They don't grow infinitely over time.  There are certain techniques where these tokens are not limited to a certain point of time, but then we are talking about various e-cash implementations such as Cashew or Fedimint.  Back to CoinJoin, these tokens are limited just for this particular round.
3. **Signing** After the inputs and outputs registration phase, we compose the transaction and send it to each participant to be signed.  We can use different identities, but it doesn't matter.  We can even use identities from step one.  Because if you were registering input in that phase, it's 100% sure that you will be signing the same input in that case.  All signatures are collected from participants.  When the final composite transaction is valid, then the CoinJoin round is successful and the transaction is broadcast to the network.

### Coinjoin on a Hardware Wallet
#### Current State

So what about the hardware wallet?  Usually, if you have a regular transaction on CoinJoin, a hardware wallet signs transactions with user interaction.  What does it mean?  It means that the user confirms output addresses, which are output scripts.  Then the user confirms output amounts and mining fee, which is usually the sum of outputs minus the sum of inputs. And there is an asterisk there because usually hardware wallets if they don't detect extremely high fees, they don't ask about this. I will talk about it later.
#### Challenge

For CoinJoin, we need transaction signing with no user interaction. Why?  Because we don't know when the other parties are ready for signing and when we reach the signing phase.  Usually, we need more CoinJoin rounds than one.  And we don't want to force users to sit in front of their computers for two days or something like that.  And in that case, a hardware wallet needs to do several things. It has to check if the sum of my inputs equals the sum of my outputs plus a small epsilon, which is the mining fee, coordinator fee, and so on. The trick here is how to correctly identify which inputs are mine, and which outputs are mine, and their amounts.

### Pre-SegWit Fee Attack (spoof input amount)

The idea is that the sum of inputs minus the sum of outputs is the mining fee.  But transaction inputs do not contain any amounts.  They contain just the transaction hash and transaction index.  So what if an attacker lies about the amount of input?  For example, you can spend 10 BTC input but lie that it's only 1 BTC.  Remember that on the hardware wallet, you just confirm the outputs, not the inputs.  Then the user will spend 9 Bitcoins on transaction fees.
#### How Trezor mitigates this attack

So on Trezor we always require full previous transactions.  So the hardware wallet can compute the real input which is being spent.  And this can be a little problematic when the transactions you are spending are pretty big.  And as I said, when the fee is high, we show a warning.  When the fee is very high, we throw an error.  If the fee is below this threshold, then we just let it pass.

### SegWit v0 fixes this?

* BIP-143 signatures commit also to the amount of spent input, which is good.
* And if the attacker lies about the UTXO amount, then the signature is simply not valid in the Bitcoin network.

#### Problem with the above fix

Are we done?  Well, no.  Because segwit version 0 does not fix this entirely.  Why?  Imagine the victim has two BIP-143 UTXOs of 15 and 20 BTC.  The malware asks the user to confirm the transaction, which takes input 1 as 15 BTC input and input 2, and it presents it as it has only 5 BTC plus 1 satoshi.  Then the user chooses the outputs and the value exchange output if necessary.  The user confirms the transaction.  They only confirm the outputs.  And they think they are spending 20 BTC plus 1 satoshi fee.  Then the malware throws an error and tells the user to confirm the transaction again.  But this time the malware uses input 1 but tells the hardware wallet, hey, this is just 1 satoshi and input 2 has 20 BTC.  So from the user's perspective, they don't see the inputs, they just see the output side of things.  So it's the same transaction as they were signing earlier.  The user sees an identical transaction and again confirms spending 20 BTC plus 1 satoshi.  But actually, they spend 15 plus 20 BTC when the malware combines these two signatures and creates a transaction that spends both of these.  This means that again 15 BTC are spent as a transaction fee.

### SegWit v1 fixes this?

Now BIP341 signatures commit to all input amounts.  That's great.  So all signatures in the transaction commit to all input amounts.  They also commit to the input script, which is great.  And the attacker cannot modify the input script.  But are we done?
#### Problem

What do you think?  No.  Not yet.  The attacker can also lie about the input script, that it doesn't belong to the wallet.  And fool the hardware wallet into not taking this input into account.  And you can again perform the same two pass signing, extract and collect two signatures, combine them and do essentially the same attack.
#### Solution

This issue was encountered by my colleague Andrew Kozlik in 2020 while working on Coinjoin.  He immediately proposed that BIP341 signatures should commit to all input scripts, not just the one input script that is being signed.  And luckily there wasn't a very long discussion and all parties agreed that it should be done this way.  There is no reason not to do it.  So SegWit version 1 does fix this issue.  SegWit version 1 input signatures commit to the previous transaction hash, pref index, the amount being signed, all amounts in the transaction, input script being signed, and all input scripts.  Essentially this is why Coinjoin loves Taproot.

### Taproot in CoinJoin

Having signatures that commit to everything is great for automated transactions containing external inputs.  For example, in Coinjoins, an attacker cannot change the input amount or input script because if they do then the whole transaction is ruined because of the wrong signature.
#### Ownership Proofs

And there is one more thing we have to figure out and that's attacker can still withhold some kind of information.  For example, whether the input belongs to the hardware wallet.  Maybe the attacker doesn't want to tell the hardware wallet which BIP32 path is being used and the hardware wallet can't figure it out on their own.  And the input would not be taken into evaluation.
So we need to somehow ascertain ownership of all inputs.  So how do we do that?  Yeah, and this is important for all transactions with external inputs.  Not only for Coinjoin but also dual-funded Lightning channels, etc.  And we need a mechanism to reliably determine for which input whether it belongs to the wallet or not.  So how do we do that?

### SLIP 19 Proof of Ownership

This is described in SLIP 19.  SLIP is satoshilab's equivalent of BIP.  And the SLIP 19 is named proof of ownership and it works that way.
We have essentially three pieces of information which are signed.
1. The first is the ownership identifier which allows us to efficiently determine whether the wallet can spend and who takes so having a given script pubkey or not.  It's a very simple construction where basically you take a symmetric key derived from the master seed and then use HMAC to process this key and script pubkey as its message.
2. The other piece of information is the script pubkey itself.
3. And then also we have arbitrary additional commitment data.  You don't even have to use that if you don't want to.  But basically, it's a random 256-bit value which in the case of Coinjoin we use a 192-bit Coinjoin coordinator ID and 64-bit Coinjoin round ID.  But it can be any value depending on what kind of application I'm building.
4. Everything is signed via a method described in the March 2020 edition of BIP-322 generic signed message format.

### So why people do not use Coinjoin much.

1. So first of all I guess the real issue here is lack of awareness which hopefully I'm kind of fixing now.
    * People don't know that Coinjoin exists.
    * People don't know they need privacy at all.
    * People don't care about privacy at all.
I think we live in a bubble and there are like 99% of people out there that don't really care about it.
2. Complexity.  I mean I said like probably several thousand pieces of new information in a couple of minutes and I didn't scratch even the top of it.
3. Then lack of integration with hardware wallets because Coinjoin wallets have usually been hot wallets and you don't want to put all of your stash in the hot wallet.
4. And last but not least there is a scare of legal implications.

## Conclusion

So I'm hoping that we are going to be addressing all four of these points by introducing the Trezor and Wasabi collaboration which will be launched later this month.  And I think that's all from my side.  And if there are any questions I still think we have like five minutes so I'm here to answer them.

## Questions

Audience: I know that last year Adam Gibson did a workshop on Coinjoins and it seemed like one of the other issues that he talked about was that we don't know who the other participants are.  And it seems like another fear is that maybe all the other participants are a single entity that is targeting you.  What are your thoughts on that?

Pavol Rusnak: Yeah,  I think Max could probably give a more elaborate answer.  But my take is we should strive to make Coinjoins as big as possible. And I don't know what's the current limit in Wasabi Coordinator but I think it's 150 inputs at least.  Something around that.  And it's very hard to pull a sybil attack if there are like 150 participants.  If there are just five participants it's much, much easier.  And if there will be... I mean I'm hoping that this integration will attract even more people to Coinjoin and I think we can start to raise this bar and limit up. That's my answer there.

Audience: (Inaudible) For example, if I want to go to an exchange and whether the exchange can refuse coinjoin?

Pavol Rusnak: So the question is what's the relationship or how do exchanges look at Coinjoin transactions?  And I guess that's a question for them not for me.  But I mean not all exchanges have the same patterns of behavior.  And some of them are marking all Coinjoins as something legal. They don't want to accept coins from Coinjoins.  I know there are even some more crazier exchanges that are looking at transactions after you withdraw coins from exchanges.  And they say hey you withdraw your coins from an exchange and you do it like a Coinjoin several days after.  We don't like this.  And I think that's draconian.  But what I also believe we are doing here we are attracting a huge user base to Coinjoin.  So I hope that earlier it was very easy for exchanges to dismiss Coinjoins as something illegal.  But if there will be like I don't know several hundred thousand legitimate users doing that hopefully they will change this behavior.  And if they won't then I guess they have a problem.  So it's like a game theory slash four-dimensional chess we are playing here.

Audience: Hi, my name is Robert. I run a Start9 node.  What's the biggest justification in terms of legal to use Coinjoin?  I mean they are coming after developers, right? How do you justify it?

Pavol Rusnak: How do I justify it? For example there is a pretty big chain in the Czech Republic who is selling electronics. I like buying electronics from that store by using bitcoins.  But I don't really want to be revealing all my stash to them.  And it's very easy if I don't use Coinjoin because you can just look at the transactions on the blockchain and right away see hey so this is a person that buys electronics.  I'm kind of KYC'd to this electronics vendor because I just ship these electronics to my place.  And I mean they are probably not doing that but they could if they want.  So if I use Coinjoin then I'm basically putting a wall between the coins I'm spending at the store and between the coins I have in my wallet.
