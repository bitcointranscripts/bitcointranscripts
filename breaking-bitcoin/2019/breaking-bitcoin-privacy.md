---
title: Breaking Bitcoin Privacy
transcript_by: Bryan Bishop
tags:
  - privacy-problems
  - privacy-enhancements
  - output-linking
speakers:
  - Chris Belcher
media: https://www.youtube.com/watch?v=9mvm-tdxv7o
---
0A8B 038F 5E10 CC27 89BF CFFF EF73 4EA6 77F3 1129

<https://twitter.com/kanzure/status/1137304437024862208>

## Introduction

Hello everybody. I invented and created joinmarket, the first really popular coinjoin implementation. A couple months ago I wrote <a href="https://en.bitcoin.it/wiki/Privacy">a big literature review on privacy</a>. It has everything about anything in privacy in bitcoin, published on the bitcoin wiki. This talk is about privacy and what we can do to improve it.

## Why privacy?

Privacy is essential for fungibility, a necessary property of money where one unit is always equal to any other unit. When you receive a coin, you shouldn't need to do any additional checking about the coin other than validity. It would be a nightmare to have to check a centralized blacklist or some government-run blacklist or whatever. If that happened, that would destroy the decentralization of bitcoin because it would be centralized.

Another reason we're interested in privacy is censorship resistance. If your transactions are visible to the world, then you could be discriminated against. Similarly, if your landlord could see your coins then your landlord would be able to hit you up for more rent if he sees your increase in salary or income. If you run a business, then competitors might be able to undercut you or compete with you.

We live in a world now where advertisers and social media accesses your data and collects your information. It would be nice if we could avoid that.

When I talk about privacy, I want to say that privacy is something where you can voluntarily reveal information if you want to. If you're an exchange, you could do proof-of-reserves. You can still reveal things if you want to. Privacy is the act of choosing what you reveal to the world and to whom.

When we talk about privacy and security, we have to talk about threat models. The threat model is the bitcoin transaction surveillance companies like Chainalysis and Elliptic. These companies have a business model based on breaking the privacy of bitcoin, getting transaction data and tracking everything and selling the data to governments and businesses that want to do surveillance. If you run a business and you think your competitors don't have the skills to spy on you, but really they could just pay a company that offers the service.

## On-chain wallet clustering

A big way that privacy is broken on the blockchain is wallet clustering. You find bitcoin addresses, and then you find certain evidence that the addresses are owned by the same person. This is called wallet clustering. You use a bunch of heuristics and assumptions. You find clusters that you believe are owned by the same person; when the adversary sees transactions going between clusters they can get all kinds of privacy-relevant information like transaction time, amounts, where it's going, which cluster made the transaction, which cluster received it. The clustering is usually based on heuristics or assumptions based on what the adversary thinks is happening. That's how we can obtain more privacy.

When someone sees a bitcoin transaction on the blockchain, there's actually multiple interpretations. Someone might be paying themselves or paying a change address or paying someone else. If you want to gain privacy, you have to specifically do the thing that nobody expects you to do. I think that's how you find privacy. It's a constant arm race between people making these assumptions, people trying to track, and people interested in privacy trying to break those assumptions.

## Heuristic: Address reuse

This is a major privacy leak known since the whitepaper. Bitcoin is pseudoynmous, not anonymous. If you use the same address again and again, then your address is your identity. Suppose you're using an exchange and you want to sell some amount of bitcoin on an exchange and you send them to a deposit address that you have used many times before. Your unconfirmed transaction gets broadcasted to the network, and because you have used it before everyone in the world can see that you're depositing to an exchange. They will see that instantly as soon as you are broadcasting it. But the confirmations will take a while, and within that time of a few hours or whatever, the price will move against you. Other traders will see these transactoins and they will open shorts because they know your sell is about to come. So when you do sell, you sell at a less attractive price. So your privacy leak has cost you a real amount of money. All you need to do is use a new deposit address, and then the leak is completely avoided.

About 30-40% of all bitcoin transactions involve an address that has been used before. There's only one suggestion I've heard for fixing this: maybe the name "address" tells the wrong mental model to users. It's like using an email address or postal address that you use again and again. Bitcoin addresses aren't like that at all. So we should instead change it to "bitcoin invoice address" and then 15 years later change it to "bitcoin invoice". Then you would say, please send money to my bitcoin invoice. Maybe that would help the situation?

## Common-input-ownership heuristic

A really useful heuristic for the bad guys is the common input ownership heuristic. You look at three inputs and they pay to two outputs. The heuristic is that all three are owned by the same person. So if you imagine the adversary sees this transaction on the blockchain, they can from that deduce a likelihood that the other inputs belong to the same person. In practice, this heuristic is very powerful and you can link many addresses together on the blockchain. The reason it's so powerful is that in any kind of money it has to be divisible. Most people transact in amounts that aren't matching the amounts they had received, so they have to join coins together to create the output amount they want.

This common input ownership heuristic was mentioned in the whitepaper. It was one of the few things wrong in the whitepaper. He said that the common input ownership heuristic gives evidence that the inputs are owned by the same person. But you can make a transaction where people come together and contribute inputs to one transaction and it's called coinjoin. It's a powerful technique we can use to improve our privacy.

## Coinjoin

There are two kinds of coinjoin we have today. There's equal-output coinjoins. Another is payjoins where the peers pay each other. In equal-output coinjoin, it would be like an input of 5 BTC and an input of 3 BTC, with outputs 1 BTC, 1 BTC, 4 BTC and 2 BTC. We trick anyone using the common-ownership heuristic. In payjoins, this is where you have a coinjoin where users in the coinjoin are paying each other. Say you have 2 BC and 5 BTC, and they pay 3 BTC and 4 BTC. What's happening there is that someone is receiving money and someone is spending money. The inputs are owned by different people, but the money has changed hands. There's a few toy implementations of payjoin. This could be used today to create coinjoins for customer-merchant relationships. When you pay a merchant, you could do a coinjoin at the same time.

It's important to emphasize that coinjoins are deniable. I've made these example transactions, but someone can make fake ones where all the inputs and outputs are owned by the same person, and you can't really tell just by looking at them on the blockchain.

## Change address detection

So we have address reuse and common-input-ownership heuristic is about looking backwards. But change addresses are about going forwards. If you know someone's inputs, then maybe you can tell which of the outputs is the change and which is the payment. There's a few ways to do this. Normally the payment amount is reused, and the change address is generated newly. If you see a transaction on the blockchain where one output is a reused address then that's certainly the payment address, and the other one not used before is probably the change address.

Another leak is a mismatch between address formats. If all the inputs are P2SH and one output is P2SH and one is P2PKH then it's almost certain that the address type that matches is the change address because wallets generally use the same address type. But there is one or two wallets that use different key types for change addresses to break this. Script types the same thing; say if you have two inputs that are multisig and one output is multisig and the other one isn't, then you can tell the one isn't is probably a payment.

Consolidation and batching is about how users create transactions. Inherent to how an economy works, merchants have lots of incoming payments and they merge together the coins when fees are cheap on Sunday night and then they do payouts by batching. You can detect change addresses in this way. If you see something you think is a payment, and later the outputs go into a big consolidation and later the other output went to a later payment, then you could say that the business was the likely party that did the consolidation.

Replace-by-fee is another easy leak. It replaces a transaction with one that pays a higher fee, but it reduces the change output amount to pay a higher fee. So that leaks information.

Unnecessary inputs can suggest change outputs. Also, round numbers can indicate change outputs. If one of the outputs is a round number, then that's probably a payment, and the other one is probably the change output if it is not a whole round number. Also, you can convert the BTC amount to another currency based on the market price and you can tell which amount is probably the change address because the payment is probably a round number in some currency if not BTC.

A paper came out where someone was able to analyze the blockchain and analyze what fiat currencies people are probably doing. It's linked on my privacy wiki page. It's really interesting.

## Most common

The most common are common-input-ownership heuristic and address reuse. The paper "unreasonable effectiveness of address clustering" finds the three reasons for why clustering is so effective. If you have these two, address reuse and the common-input-ownership heuristic, you can be very effective. It finds that about 0.2% of non-coinjoin clusters contain 22% of all addresses and 23% of all transaction outputs. When you correlate the big transactions, they correspond to big businesses, mining pools and markets and so on. These super-clusters correspond to major exchanges, casinos, mining pools, marketplaces, etc. If you make a bitcoin payment to some business, then anyone who does this simple analysis can generally figure out that you transacted to this business or whatever it might be.

I think the best solution here is payjoin. What would happen with payjoin-- remember, it is a coinjoin where in a merchant-customer relationship you merge the two clusters into one cluster. The two wallet clusters get merged together. Even if you just have 5% of all transactions being payjoin, but they were spread around roughly equally in the bitcoin economy, then you could get to a situation where all the wallet clusters are just merging into one giant wallet cluster and this would break the common-input-ownership heuristic.

## Identifying clusters

There's a few ways to put identities to the clusters. There's mystery shopping payments. If you have a shop, sometimes you have mystery shoppers that come around and see how the shop is doing. You go to the casino, you deposit some money, and then you wait and see in your analysis where those coins end up and in which cluster it is. Then you can identify that cluster as this casino or that exchange. There's also AML/KYC-- if you open an account on an exchange, they ask your name and other private information. When you upload those, they end up in a database like those transaction surveillance company's databases. They will link your name to those clusters and identify who is making those. If they ever get hacked, then that data will end up in the hands of hackers who will do something with the information.

Forced address reuse, or dust attack. It's when an adversary sees some addresses on the blockchain and send an amount of money, and they hope the wallet will automatically spend that coin and merge it into other transactions. This will leak some information and identify the cluster.

Then you have timing analysis... there's a few papers where people have analyzed certain kinds of clusters and you can match it with timezones and google trends and get some evidence of what country a transaction is. Another one is eavesdropping and wire tapping. If you're sending a transaction or an address to someone in cleartext, then anyone on the wiretap can link that to you on the cluster that they find in the blockchain. It doesn't have to be wiretapping, it could also be if you're communicating publicly on a forum. You can avoid this by using encryption to encrypt any of your addresses.

Sometimes you can just ask users to give up their information. They are very happy to do that sometimes.

## Example: QuadrigaCX exchange

Earlier this year Quadriga went down and lost a lot of customer's money. Some users on the internet asked, is there a way to get this information? So they asked users, could you tell us the addresses and let us know? The customers were happy to do this because their money was missing and they want to recover it. So they posted the addresses on a forum. There's a site called walletexplorer.com that does some basic wallet clustering. They found what was almost certainly the hot wallet of Quadriga. What made this work was that people kept depositing to the same deposit addresses. The hot wallet also did a lot of merging together of inputs. It was fairly easy to find.

The analyst also tried to find the Quadriga cold wallet. They said they didn't have a cold wallet. The cold wallets can be harder to find because cold wallets almost never do address reuse and they actually make very few transactions. They generally depending on the person who owns them, they often merge all their inputs at once without a change address, and that could do a lot to help privacy.

## Example: Bustabit casino

This is another example from about a year and a half ago. They were a bitcoin casino. Online gambling is not allowed in the US. Any customers of Coinbase that deposited straight to Bustabit would have their accounts shutdown because Coinbase was monitoring for this. Bustabit did a few things. They did something called change avoidance where you go through-- and you see if you can construct a transaction that has no change output. This saves miner fees and also hinders analysis. Also, they imported their heavily-used reused deposit addresses into joinmarket. At this point, coinbase.com customers never got banned. It seems Coinbase's surveillance service was unable to do the analysis after this, so it is possible to break these algorithms.

## Security/privacy tradeoff trap

We've been talking about using coinjoins to improve privacy. The most decentralized and most secure systems are things like basic bitcoin transactions, where you make a payment with an output and a change output and sometimes you merge together inputs. The next level down is joinmarket or Wasabi wallet. They break the common-ownership heuristic and they break the graph. But they have higher miner fees because the transactions are so large, and the system can't support as many of those transactions.  But they are more private, as you saw in the last example. Monero is more private than joinmarket and wasabi but full nodes aren't prunable... so Monero's system doesn't know when a coin has been spent, so they can't delete coins that are spent. They have a perpetually growing data structure. The transaction output set can't ever be deleted and every full node has to carry it forever. The system is private, but much less scalable, and therefore less decentralized and less secure. Then there's zcash which uses zero-knowledge proofs and doesn't have a transaction graph. The amounts aren't visible, so it's more private than monero. But zcash has a trusted setup which has certain cryptographic information that if ever revealed would destroy their system and let users be spied on or cause inflation. It's even more private, but even less secure or decentralized. There was also Digicash in the 1990s and it used blind signatures. It had information-theoretic privacy, which meant that even if you had an infinitely powerful computer you couldn't break the privacy. It's the most private system you could imagine. But unfortunately, it was the most centralized, it had a central server and it could be turned off and in fact it was.

If we're not careful, you can design a system that trades off security for privacy. We want a system that is both secure and private. There's no point in having security when you can just turn it off. So what's the solution?

## Off-chain transactions

Lightning network and coinswap are possible solutions. Instead of adding decoy data, they remove transactions from the blockchain. They are more private because less data is being transmitted. It's similar to change avoidance too. The next generation of privacy improvements would be something that also improves the scalability of the system. It should work by removing data, not by adding decoys.

## Lightning network

I think lightning network is very promising for privacy. All the blockchain-based privacy leaks simply don't work for lightning. There's no common-input-ownership heuristic because there are no inputs. There's no address reuse, because it doesn't have them. There's no change addresses, none of that. But there are other leaks. For example, on the bottom is a diagram of roughly how lightning works where payments get routed through multiple hops on the network. You can imagine a transaction surveillance company that sets up lots of lightning nodes and channels and then sees the payments. One thing they can see is that the amount is leaked. That can be fixed if we had atomic multi-path payments, which is a lightning payment that is split up and goes over many routes and finally ends at the place it is paying. Then the amount wouldn't be leaked, you only leak the lower bound. That would be really great.

Another leak in lightning is that today lightning payments work by having a common HTLC value, the R value. If a payment route involves two or three sybil nodes then they could tell the same payment was routed through them. This could be fixed with scriptless scripts to replace the hashlock technique but with cryptographic magic- this is the wrong talk to go over it; if you search for it, you will find it. The way it works is that the Schnorr public keys have a different tweak, a value added to them at each hop, and different nodes can't tell they are part of the same scriptless script scheme.

Lightning channels still rely on channel UTXOs and they are often revealed. Private channels can help fix this. If you use private channels, you have to reveal your UTXO when you're receiving a payment. If the adversary sees a UTXO then they can use blockchain-analysis methods to maybe get some information about you.

## LN probe payments attacks

There was a paper a few months ago about "On the difficulty of hiding the balance of lightning network channels". The balance is only known to the participants because an adversary can track a payment going through and seeing the amounts changing at each point.... Adversary opens 624 channels at a total cost of $47 USD (current as of January 2019) and can see all channel states. It's an attack for discovering channel states around the network. If the channels don't have enough capacity, they send back a different error message that says "insufficient funds". Using this, the adversary can send payments through a slowly increasing payment amount until they get back an error message about insufficient funds. By doing that, they can recover information about channel state. They are using a fake payment hash, so their payments never succeed, and they don't lose money. The only cost is opening up the initial channels. You don't need to open a channel with every node, just every other node because most nodes are well connected and you only need one side of a channel. Using this technique, you can watch payments go through channels and that would be a privacy leak.

## Conclusions

ON-chain privacy is really not great right now, and it can be broken fairly easily by anyone on their laptop if they are a fairly good programmer. There's a privacy/security tradeoff. We need to target both privacy and security. Payjoin is probably the best thing to work on to merge all the wallet clusters. The lightning network greatly improves privacy, although there are still some problems that can be improved. If you want more information about this, review my privacy wiki page that I worked on and give that a read if you're interested in this stuff. Thank you.

## Q&A

Q: In World War 2, the Germans didn't know that enigma was broken. They were so sure that it wasn't broken, and this was a cause of their defeat. How do you contemplate that we don't know, like what Chainalysis or Elliptic do know? They might not disclose certain research. How do we understand what the adversary is doing?

A: For these transaction surveillance companies, they can have customers who are anyone. So you can leak information from the company and see what information they share with their customers. It can also be observed by the behavior of exchanges and which transactions they ban you for. These surveillance companies publish papers. You can read their papers on Google Scholar. They tell you how it works. This is where I got most of this information from. A lot of these heuristics weren't invented by them themselves. The common-ownership heuristic is actually in the bitcoin whitepaper and they were mentioned back in 2010 and 2011 on the bitcointalk forums. I think the leaks that exist today are scary enough and we should do something about them. That's my view.

Wallet fingerprinting is a technique where wallets usually have differences in how they construct transactions, like a different nsequence value or different locktimes or they might choose their inputs differently or how they compose the transaction. You can tell which wallet made a transaction.

Q: What about confidential transactions on Liquid?

A: Confidential transactions are a technology where the amounts are hidden. Any kind of analysis about round numbers or unnecessary input heuristic, those things can't work. The downside is that far fewer people use Liquid. It's the same with Monero and zcash- because fewer people use it, you might have a lower anonymity set. I could see some people doing some transactions in Liquid, doing confidential transactions, and then withdrawing over a few transactions and that might be enough to break the link between their addresses. That could work.
