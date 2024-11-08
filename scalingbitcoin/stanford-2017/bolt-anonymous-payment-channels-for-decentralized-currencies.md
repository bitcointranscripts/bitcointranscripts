---
title: BOLT Anonymous Payment Channels for Decentralized Currencies
transcript_by: Bryan Bishop
tags:
  - research
  - privacy-enhancements
  - lightning
speakers:
  - Ian Miers
date: 2017-11-04
media: https://www.youtube.com/watch?v=BPNs9EVxWrA&t=3630s
---
paper: <https://eprint.iacr.org/2016/701.pdf>

To make questions easier, we are going to have a mic on the isle. Please line up so that we can have questions quickly. Okay, now we have Ian Miers.

My name is Ian Miers. Just got my PhD at Hpkins... authors of zcash, zerocash, ... My interest in bitcoin was, first getting involved, was dealing with the privacy aspect. There is also a scaling problem. I assume you are aware of that. The bottom line is... converting this to PDF doesn't work well, hm. The bottom line is that... blockchain-based payments have scaling issues. They are expensive in resources and money resource usage and just time, the time latency. This is a problem that is kind of annoying. It's next generation payments, but it's expensive? What?

This is something we're fmailiar with. Hve you tried to buy a drink at a bar? It has fees at the merfhant payment processor. It has a time involvement.

The solution to this is that you batch payments together. If you're at a bar, then you opne a bar tab. You give them your credit card. As you buy drinks, you build up this debt, and at the end of the night, you pay. The bar tender might not trust you. If they do trust you, then you put it on the tab and give them the card at the end of the night. You amortize the cost of an expensive payment system over multiple transactions. This is the basic idea behind a payment channel. The difference is that in a bar, there's a trust. What about in a trustless scenario?

The way to think about payment channels is that they are a protocol for IOUs. They are not debt based though. They have real money. If the two people don't trust each other, at the beginning of the night you give the bartender $100, and he gives you $95. So you have this channel established between the two. But this is only if there's not a multi-hop network. You exchange these for "IOUs" that can be repudiated on the blockchain. At the end of the night when you're done, you have to go cash out the IOU and this should work as a pamyent protocol. Who do you cash it out with? You cash out the IOU wit hthe bartender but then you have to trust them. This is where the analogy breaks down... but the answer is a blockchain. That's where you pay. You can do this with escrow, of course. You have a lbockchain. Cost some resources.. you make a bunch of payments, then later come back and close the channel. This is one way to think about another payment channel network- put some money in, do a bunch of transactions... This is nothing new. This is not my work here. This is the basics of this thing. The question that comes up, is ...

... it actually makes the situation worse because if ... you have ot identify your transactions. So you, end you identify your self. If you are trying to do this micropayments.. the bandwidth.. you identify yourself every time you do tihs, you build up this pattern. So there are privacy issues. You don't want to do that. You can't use it for some applications.

Worse, it doesn't solve the privacy problem- everything on the blockchain is public. You think that by removing the transactions that you gain something. True, but you have t oworry about the aggregate data too. It doesn't matter that you are paying a psychiatrist once a week- what matters is that you know that they are paying a psychiatrist at all, even with channel open channel close.

The situation gets better with payment channel networks with multi-hop. You can do onion routing. And then all that anyone sees is that you have a channel open with a particular entity. But there are still some problems. Hubs in the network learn what you're doing. This causes a bunch of issues. It's not really clear what these channel.... The hope is that you get a decentralized network. Even in this you have some problems, as mentioned in the last talk. You have a path through the network and if all the peers onhte path collude, then they can identify you, and it coul dhappen after the fact too. Even worse, you end up in this, where it might happen, where the network is centralied. You don't have to worry about collusion- the guy just knows anyway. And this has a bunch of problems. This starts to look exactly like what we have now for payment tech, it is unsatisfactory where you have a centralized payment provider. And they have start doing monetization stuff, selling your data, or whatever. It will happen there. For bitcoin, the situation gets worse, it's not going tobe like Visa which gets regulated-- they have rules about what you can do with personal data. BUt it will be, insert your sketchy exchange here... Might not be based in your friendly jurisdiction. So there are more privacy problems there.

And so, the legality of the matter... the ... might actually have worse privacy without NIZKs. You have multiple identities in bitcoin, they are free to create. In lightning, identities are costly, you have to use escrow and burn money to do this. The identities are long lived. The point is to amortize the cost of making payments over a number of transactions. You can open a channel and make a transaction and create the open, close, do the payment, but you don't gain anything. So you can't do that.

The hubs might need your real identity, depending on KYC laws or their jurisdiction. It's a long term .... It's quite easy to link these to your real world identities. You use the payment channel to pay Amazon well now they know the linkage and they can collude. Opening channels with anonymous funds.. like zcash, use coinjoin or some mixnet to get privacy in bitcoin, doesn't solve these issues, because you still have long-term pseudonyms. Bitcoin plus lightning is not particularly private. Zcash has privacy-- if you could combine that with lightning, you will lose privacy.

## Solutions

So then we get into my work. This is BOLT. It's a set of protocols for privacy preserving payment channels. There are three versions. There's a uni-directional channel that allows Alice to send fixed amounts of money to Bob, using zcash and some cool tricks and compact e-cash scheme (not zcash sorry). Then a bi-directional scheme allowing them to exchange arbitrary values between... it's blinding signatures, zero knowledge proofs, fair exhange, etc. And then third a multi-hop chained payment network, ... third party payments.

## What is the privacy for channels?

Unlike in bitcoin or zcash, a payment if you make it, ... in channel enetworks, you have to have an open channel. If I am a bartender and someone wants to pay me on a tab, they have to already have a tab. That limits the anonymity set. It's not a random person, it's someone I have already interacted with. So that's a problem. In this setting, you only have point-to-point channels. One end has t obe a known pseudonym. If someone used a ranodm identifier, you wouldn't have any guarantees of any channels. So you have channels open... but it might just be you, so every time you use it, people will know it's you.

In a payment channel network, this gets better.

## Atomic swaps and zero-knowledge proofs

The problem... ... but you don't actually know; you just know it differed by 5 bucks. The funny thing is that this sounds hard. But it's not cryptographically hard. If you know some cryptography, this is simple: use commitments and zero-knowledge proofs. It works out well. With those, you can transform a setting where you have an IOU for $100, the merchant is owed, the customer is owed $100 and the merchant $0, and you... where the merchant is owed $5 and the customer $95. You do this trade, you want to do it without revealing anything. It's simple. All you have to do is, use a zero-knowlede proof. This thing exists. This is the magic of zero-knowledge proofs.

However, I said that's not even hard. If I have an IOU for $100 and $95, and I can go cash-out the $100 one, and I have a free beer... right? So, you need to somehow swap these two out. But if you invalidate the first IOU, the $100 one, then you have no guarantee that you can go and get your money back. She has no valid IOU anymore. On the other hand, if you do invalidation, you give the IOU for $95 first, then before the $100 one, then you can cheat the person. So this is concerning. Really you want to do an **atomic swap**. That's hard to do in cryptography.

The first function of an IOU is that it allows you to cash out your money in the blockchain. You also want to be able to buy another IOU. It's inconvenient, but you can only get your money back. You can go restart the process if you want. It's not a big problem. It means that Alice can safely give up her ability to buy another beer without losing money. The bartender can safely sign a new IOU for $95 if Alice goes and closes the other one. You can't give her the ability to go purchase more beers.

If you have your two IOUs ((are we doing e-cash here?))... you want the bartender to sign the new one. You prove that this one has been made correctly. Then you reveal the identifier to prevent you from playing this card. And then you actually get the bartender to sign the new one as valid before closing the channel. No payments have gone through, you have given him $5. Once you have a safe new one, you can destroy the old one. You can use this identifier and say it's no longer valid. If you try to close with that one, the bartender can say hey this one was stale I cna prove this. Once this is done, he can give you a new IOU, and this gives you complete privacy.

This is not a theoretical thing. We have implemented this. The details of the crypto primtives are not interesting. It takes less than 100 ms per hop to make a payment. This doesn't use zk-SNARKs (which is not synonymous with zero-knowledge proofs). There is no trusted setup here. You can do this with well-established cryptography. This is nice, it's scaleable. The numbers are in the paper.

You can do more than just send payments, having a bartender and a beer.... You can do multi-hop payment networks, where the participants and intermedaries are hidden. This sidesteps the issues with lightning network and collusion problems and so on. It doesn't have htis problem. We can hide payment value, participants, everything. The only thing is like maybe a sidechannel which is hard to get around. You can also do a more sophisticated stuff like more than just monetary balances... you can have an IOU for A, we are going to prove that the two IOUs differ by 5 dollars. Arbitrary state transitions, you could do something like plasma. Also you are moving out the cryptographic from the blockchain-- you are validating an ECDSA signature.

## Deployment

One thing I would like to do is compare this to tumblebit, lightning, everything else. The difference is that tumblebit and lightning payments work in bitcoin as-is. They don't offer privacy from collusion in others in the network. In lightning, if everyone in your channel or network colludes, you can be identified. In tumblebit, if the hub... they can identify the sender. In BOLT, you can get full privacy, but at the cost of...

So how do you deploy this? It ends up being the case that this can be deployed in zcash or bitcoin by adding a new opcode. I am not sure if this is a soft-fork or a hard-fork. Interesting discussion. You can deploy by adding an opcode. In bitcoin, one caveat. You need to be able to anonymize the funding of a channel. One cheat that makes this efficient is that it's a two-party protocol and you're doing exchanges back and forth. You can end up aborting.. the protocol goes dead or maybe it's malicious and you end up in an invalid state and you have to close the channel. This links a close to an abort. You want to make sure that if they link to the open channel opening, then they can't identify you.

## Q&A

Q: Can you talk a little bit about the requirements to... revocation keys... and what a large merchant such as large online retailer might need to build in infrastructure to deal with this?

A: It will be something like 32 bytes per... channel. So you have to store some data. And you have to monitor the network and make sure they are not closing the channels. Your infrastructure will store small data per client. You have to be online to monitor to watch for channel closure events.

Q: Any kind of expiration of IOUs is just internal to the merchants with a customer?

A: Yes there's a timeout. In lightning too, you have to pick a timeout parameter for how long until you post a closure. You have to wait for the other person to dispute it, too. You have to figure out the amount of money involved... infrastructure.. how much... that's a tunable parameter that can be set by the merchant and participants.

Q: Can you talk about the opcode that is needed and what it does?

A: It's an opcode that looks at the output of a transaction and you have to get a commitment the IOU it opens, and check that the balance and funds coming in are split according to the value of the commitment, like the amount going to the customer and the merchant and so on, and signed with the right private key.

Q: Alright, thank you.






