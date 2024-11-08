---
title: Stroem - A Protocol for Microtransactions
transcript_by: Bryan Bishop
speakers:
  - Jarl Fransson
---
7 transactions per second, or is it 3? That's about what we can do with bitcoin. What if you need 100,000 transactions per second? I come from Strawpay, we've been looking into bitcoin for a long time. When we learned about scripting and the power of contracts, like payment channels, we thought maybe it's time to do micropayments and microtransactions. To give you some perspective on scale, let's say that 1 billion people make 25 transactions per day. That's maybe 1/5th of your average page views that people did today on the internet. So a user would only spend maybe $1-3 USD/day. On average this is about 300,000 transactions/second.

We had three design requirements when we started on this. The first one was to focus on the user. Maybe the bitcoin community hasn't always done this. Users need a really simple way to buy, and they don't want to wait, they don't want to login, they don't want to register, and it must work on mobile devices. The second requirement was efficiency. The scale of the system needs a high-level of efficiency. You need a really low transaction cost. The third requirement is that it has to work in a larger economy. Inside of a community we maybe forget this sometime. Merchants want to get paid in local currencies. Consumers are fine with using bitcoin, but they don't want to hold BTC. So they need a way to trade in and out of bitcoin, and maybe they don't even have to know they are using bitcoin.

It seems that plain bitcoin wont work here. What about using payment channels to connect consumers to special payment providers (PSPs)? Instead of a PSP for micropayment channels, you can have "issuers" that issue over an open protocol to create a liquid market for payments. We have a different approach to this than just connecting payment channels together. We call our protocol stroem.

I'd like to do a walkthrough of a Stroem transaction. Lisa wants to buy an article from a Swedish news site. She clicks on the article. The wallet presents her an offer. When she accepts, her wallet connects to her selected issuer using a payment channel, and buys a digital promisory note. So this is a time-limited promise by the issuer to pay the amount of the purchase to the owner of the note. Next, the wallet adds some information about the purchaser, transfers it to the merchant, merchant validates the payment and delivers the article. This whole process takes less than a second.

It's interesting to note that in this time, the consumer is out of the transaction. The consumer has no liability to anyone. We focus on the consumer experience. Later, maybe after the end of the day, all the payments, the aggregated promisory notes are redeemed at the issuer, and the issuer pays the merchant the total sum minus some fee. The point here was to make this an open protocol so that anyone could participate.

As another example, someone like Wells Fargo could issue notes denominated in BTC to facilitate microtransactions for their customers. Now merchants have to accept and redeem these notes from different issuers. So a redeemer role has to buy all the notes and redeem with the different issures. We envision a network where a lot of actors compete in an open market.

Stroem is middleware for microtransactions. The interaction between consumers and merchants. It has offers, orders, payments and receipts. There is flexible settlement for how the payment is actually completed. Today we pay merchants with standard bitcoin transactions, but we could do payment channels. In the future we could use the lightning network or something similar when it gets operational, but a lot of merchants will probably want to get paid in fiat currency. That's what we think, but we don't know.

How would we construct a digital promissory note? It would contain the amount, the issuer, the validity time. The issuer signs the note to the first owner, which is a consumer using a digital signature. The consumer makes a payment by transferring it to the merchant. That's done by a second signature. To transfer these notes, you need to create a digital signature, so you need to control the private key of the owner. These notes should not be easy to steal, it's like bitcoin where you have to keep track of your private keys.

The merchant redeems the note, which is a third signature, and at each transfer it's possible to add and authorize some information about the transfer. We use this to create an atomic transaction of the payment plus the order. This is an authorized order because it's signed. Because it's a single signature for the payment and the order, the payer cannot dispute the order (non-repudiation). We don't know who the payer is, but we know that whoever paid cannot dispute the order.

We support aggregation by having a special block transfer mechanism, where you can take a large set of payments and transfer them with a single signature, these blocks can be split and transferred to different issures if necessary.

For double spend verification, when an issuer redeems a note, the histories must match the list of verifies that is decided at the time of issue. This gives the protocol some nice offline properties. The issuers must always be online. The consumers only have to be online when they make payments, which is good because it works for mobile devices. But merchants can be offline and still receive payments and do validation. That's important for transaction aggregation that we want to happen at the merchant and redeemer levels. It also lets us support point-of-sale applications or vending machines that don't have to be online, as long as they are online every 10 minutes or every hour or something like that.

These notes are time-limited, to limit the double-spend verification resources needed, similar to electronic cash. These notes do not work as money, because they timeout and become worthless.

Payments are sold when they are routed in Stroem. Some important properties of the system are not decided by us, but rather by the market. The fee, validity time, aggregation vs immediate redemption, issuers to use, are all decided by markets.

To put it all together, does this scale? I will skip the details of this table of the signature operations for the system. We can see that the issuer spends 3 signature operations per transaction, and a lot of these are in batches. So we have to think that this system can actually scale with the current hardware to very high levels if this is needed.

This was a quick overview, if you want to find out more, read <http://stroem.io/> and our paper there.

