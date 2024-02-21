---
title: "Anchors & Shackles (Ark)"
transcript_by: Refisa via review.btctranscripts.com
media: https://www.youtube.com/watch?v=OBt1nS14Ac4
tags: ["ark"]
speakers: ["Burak Keceli"]
categories: ["conference"]
date: 2023-04-29
---

Hey, Guys. My name is Burak. Today I will be talking about something that I have been working on for the past six months. To give a bit of background, I started first in a big block sort of camp and then got introduced later to Liquid. I did some covenant R&D on Liquid for about two years, and now I have explored the Lightning space for about a year.
As someone who initially comes sort of from that sort of big block camp, I have always had objections towards the lightning, mainly around the UX, from backups to interactivity to liquidity problems.

I have severe objections. A few months ago, I tried to sort of work in a new light and more to address these problems. I have come to the realization that these objections—the objections that I had in the past—are all addressable in the long run. Page DLCs can be sold with the same receiving initiative and proof of payment, but there is still one big problem: inbound liquidity. To me, it's like a non-starter. If you're orange billing someone for the first time and you cannot receive, what happens is you get a swap, some ring swap in, and it doesn't scale. To me, if something works 90% of the time, it doesn't work 10%; to me, it doesn't matter. There has to be zero friction. So I sort of try to come up with solutions to address these problems. And then today I'll be presenting a new sort of alternative Layer 2 protocol. It all started as a small idea—a Lightning idea based on channel factories and all that. And it later evolved into layer two on its own.
 
At some point, I realized, okay, what I'm building is lightning, but it is like a new layer two in its core. At its core, it's like, internally, a new off-chain protocol. So the protocol is that it requires APO or CTV, a new covenant primitive, to work. That's not something we can do on Bitcoin today. We can do it in the Bitcoin Inquisition's signature, and I think that's how we are going to start. But to give a high-level overview, first of all, we haven't set a name yet for the protocol. So to give a high-level overview, the protocol has no liquidity constraints. It's a simple protocol. It mimics the on-chain UX. Just like you do with on-chain wallets, you have an address you can receive, send, and hold. You don't have any interactivity requirements. And you don't have to acquire inbound liquidity to onboard the system in the first place. You don't have to run a server; you can use your smartphone; and you don't have many interactivity requirements. And every payment takes place in a coin-join route, so you don't leave your identity, especially receivers; do not leave their identity.
In Lightning, if hubs call it or they comply with OFAC; two hubs can sort of extract the payment route. If I'm using IE and LSB XIZ and you're connected to ABC and they have direct channels for each other, so the receipt is 12A, then they can call you to extract the payment because it's linked through the same HDLC, the Bolt 11 hash identifier. So in this protocol, it's not a state channel design. It's not a roll-up design of any sort; it's its category. So, here is a comparison table, comparing this protocol with Lightning on-chain, also Ecache, obviously Ecache, Charm and Ecache, and FedEvent stuff, it's called Studio, so it's controversial what Layer 2 is and not.

To me, e-cash doesn't fall into the Layer 2 category, but it's good to compare. So, on-chain Bitcoin, to me, lightning is the only layer 1, as related to Bitcoin. To me, the layer 2 definitions are really like a sort of separate piece of software where you transact Bitcoin without polluting on-chain, yet you can revert your coins to one chain without asking for a corporation. So by that definition, the protocol falls into a layer two category. So it's self-constitutional. You can unilaterally revert your coins on the chain, but you transact off the chain. So interactivity, well, PHTLCs solve the receiving issue.
And you can generate print. And they don't have a generic pre-image ready offline, but you still have to sign or monitor the network for channel breaches if you're not trusting a watchtower. And just like on-chain, you don't have to be online like that. Scalability-wise, I think this is the number one and biggest property we have. Lightning—you cannot onboard the whole planet to lightning; it doesn't scale. Channel openings and some might swap ins, so out, they do not scale. It's not only the on-chain footprint, right?

The non-liquidity doesn't scale. I have this utopian idea of onboarding the whole planet to Bitcoin in a non-custodial way. I know in reality it's probably never going to happen, but I'm super obsessed with it. So I think my goal is to be able to at least give people an option for the whole planet to onboard Bitcoin and not custodial, so in theory, with this primitive, you can onboard the whole planet. In theory, on-chain footprint-wise, there are probably other challenges, but the point is, you don't consume any pretty much, you don't consume any pretty much footprint, on-chain footprint. Everything is off-chain, pretty much. Unlike in Lightning, you have to touch on-chain sometimes. Of course, on-chain is the worst. Nothing touches on-chain, doesn't scale, or touches anything. And privacy, again, guys, it's also controversial, right?
Lightning versus on-chain privacy. To me, lightning is worse than on-chain, but many people, argue that on-chain is worse than lightning. But with this primitive, whenever you make a payment, the payment takes place via a coin-join route, sort of like an off-chain coin-join protocol. So, coin-joins today are mostly used for data market use cases, maybe, but here, the anonymity set is everyone. Anyone involved in a payment, whether that payment is in a coin join or a blended mixing route, maybe that's pretty correct. So onboarding—again, you don't have any onboarding setup. You onboard someone, you want to tip someone, you just onboard Orangefield someone, and you can receive payment like on-chain, but it scales. So it's a simple protocol. I mean, it's not a state channel design.

I think it's conceptually simple; it's simple to reason about. So there are two parties: users and operators. Operators are akin to service providers in Lightning, LSPs. Factory operators are also LSPs under this protocol. They can run Lightning Rogers, too.
You can pay with this protocol Lightning invoice, as it's interoperable with Lightning.
It's not a competitor by any means. It's much; it's a compliment, Lightning Bar. So users aren't interactive entities; they hold and receive coins just like they do on-chain, but they do it entirely off-chain. Factory operators, just like LSPs, provide liquidity to the protocol, but it's slightly different. Lightning uses liquidity more efficiently because channels are bidirectional. Here, it's more like a one-directional design.
The factory operator has to constantly provide liquidity for the protocol. So the protocol, again, and the idea require a common primitive. We need a common primitive to constrain the transaction outputs of a spending transaction. And you can use CTV for that, which is a bit controversial. And we can use an APO to emulate CTV. We can emulate it by hard-coding the signatures 65, 33, and an unknown pop-key type. And a script to emulate the CTV use case. There are other alternatives, TI-cache, and some other combinations in even syntheticity. However, it requires common and primitive constraint outputs in advance of creating a Bitcoin output. So it's just like a coin join.
You have a set of coins. Coins are Bitcoin transaction outputs, but they live off the chain.
They ideally never touch the chain, but you can, of course, literally revert, but the coins live off the chain. Think of it like a UTXO set that lives entirely off the chain.
So you have a set of coins in your wallet, software, from one to a million, forget about the dust limit, and keep things simple, from one to a million sets. So the design begins with a factory. So factory, it's like a channel factory; I name it factory; it could be something else, the naming, but because it's similar to channel factories, I name it factory.
The factories are a shared UTXO model. So factory is a Bitcoin transaction output.
It's a shared UTXO. And it has a bunch of nested coins in it. The coins I mentioned earlier live in this factory, under this factory. They nest in these factories. And the factory operator is the one who creates the factory, say, every five seconds, to put things simply.
 
But contrary to CoinJoin, CoinJoin can take from hours to days to complete a CoinJoin session. Consider this a CoinJoin round that occurs regularly, say every five seconds. So every single one of these factories is a coin joint. They're like blinded mixing rounds. It's operated by; the factory outputs are funded by the factory operator. And here is what a factory looks like: This is the factory where the factory operator sort of creates crops every five seconds. So you have one or more inputs to fund.
And the coin output, connector output, and a factory change. So the coin output has a bunch of coins. Coins that you have live in this output. And each coin is a 12-2, just like lightning. The initial idea was to have lightning channels instead of coins that nest in the coin's output. But things have evolved. So instead of having lightning channels in one UTXO, just like coin pools and factories, we have coins. And the coin is like a one-time-use-only channel. You spend it, and you create new coins, just like one chain. And the idea is that you have a bunch of coins that are coming to a single transaction called output12coins. You can unilaterally reveal the coin content and the factory content. Sort of the coins have like a script path forger, and anyone who knows the sort of template hash, the content of the coins, can reveal the content. And the connector output, the second output in a factory, has a bunch of connectors similarly. But this one is more like a withdrawal tree: update, top-leaf, and update, verify style, withdrawal tree.
The difference is that we have connectors. Connectors are also Bitcoin transaction outputs that connect to this output. They're commitments just like coins, but the difference is that you have to reveal them one by one. You have to reveal the connectors one by one. In coins, you have to reveal them all at once. So the primitive—I mean, the protocol is at its core—is realized at the time of contract; this is a new buzzword I made up. It's ATLC, so this is a comparison table. HDLCs are the absolute worst. As soon as you're receiving, you can't create a preimage when you're offline. HTLC solves that. Also, proof of payment is a bit of a gray area in HTLCs. But ATLCs check all the boxes; HTLCs do, but differently, ATLCs have no liquidity constraints.

So you don't know anything about the liquidity requirement you receive; it's like a magic button. You push a button, and you receive whatever you deserve, like on one chain. 
So to make things simpler, if we have a coin, we have a bunch of coins. Each one of these coins is 12-2. 12-2 between the coin owner and the factory operator just like lightning. Like 12-2 between me and my channel partner. Think of the channel partner as the factory operator, like a central hub. I have a 12-2, I'm a co-signer and a lot of coins. And I join if I want to spend these coins, right? Like my UTXOs, I want to spend them. And I join a factory session, just like joining a Coin Join session. And the factory operator is a blind coordinator. And I register my coins first, on the left. In a coin join, you register inputs and outputs in the same phase. You register the coins, and these coins are from the previous factories, right? You get paid from coins from someone else in the past, and you create them. You now register for new coins, payout coins, or plus change in the round. And, in this round, there are many participants, so you can have thousands of transactions and coins in a coin joint. Here, you still have the same limit, but with Tableau, if they verify, it can be millions. But the idea is to have; it's like a coin; join or retain UX; you have a coin on the left; you're spending; and you're creating new coins. You're destroying coins, and you're creating new coins. So on the right. So these coins are commitments. So the factory operator is here, right? We have a session, a factory session, And the factory operator is trying to create a new factory. The factory operator and his factory template—I mean, the factory he's crafting—are placing these coins—coins that we registered, among many other participants.
 
Then the factory operator places a set of additional outputs in the factory template called ATLC connectors. So ATLC connectors are added to the factory; the number of spending coin times is on the left. So we are spending N coins, and the factory operator adds N ATLC connectors. And we are creating M new coins. And what happens next? We did the input registration port and the audit registration port, and it's the signing phase. So, of course, connectors and coins are mixed; it's a mixing round. So when I register a coin on the left, the operator gives me a blinded credential so that I can register for the new coins. Then in the signing phase, I attach ATLC to my coin to sign, to lock my coins in for the factory. So, this is similar to lightning, right? You have to think of Coin as a tool to use the Lightning channel, and you attach an ATLC instead of an HDLC. And from there, you sign the ATLC with the 12.2 to connect to an ATLC connector. So with that ATLC, you're signing an off-chain transaction, like a state update, simply. One state update only.
You're signing an ATLC from the 12.2 ATLC to connect to an ATLC connector. And you do the same for all other coins. So you sign all participants in a round; they add ATLC to their coin and connect that ATLC to its connector. And if someone hesitates to add an ATLC, you get back, and the factotrupid bends you from the session. So this is what the on-chain transaction looks like. It's pretty simple. The ATLC is a two-to-two. I’m the call signer. I'm spending this coin, and I'm paying out to Bob, someone, under a new factory, and I'm signing this off-chain transaction to do so, to connect my ATLC to your connector.
I'm signing the ATLC, which is the first input itself. The first input to the ATLC I'm signing is a call signing from 12.2. Again, the other call signer is the factory operator. The second input I place is on the ATLC connector from the new factory. The ATLC in the first input I'm spending is from a previous factory. The connector, the ATLC connector, and the second input are from the new factory. And ATLC connectors, carry dust. And they are single-signature spendable by the factory operator. ATLC is a tool of two; connectors are single-signature factory operators. So in the outputs, we place one output for the factory operator to sleep, to claim his funds. So by doing that, as you remember, we have coins in a factory, and by doing that, we, the factory operator, created a set of new coins. It's an on-chain transaction. You provide liquidity for these coins. And the factory operator now has to claim my coin; I should be able to claim my coin and my previous coins, right? To do so, the factory has to exist.

The factory operator should not double-spend on this factory. If the factory operator double spends, the factory operator is not able to claim my ATLC, my first input, because I signed the off-chain transaction with SIGHASHALL and it commits to the second input, ARTPOINT, which is the transaction ID of the factory. So for an ATLC to be claimed by the factory operator, the factory operator should not double-spend the factory. If there is a double spend, it's not atomic; it's an atomic construction. My ATLC is no longer redeemable. I can do an illegitimate closure for my ATLC with the script path. So it provides an atomic layout for the construction of an aggregate transfer schedule here. So here's a bit of a logical overview. So, you remember, we have coins—commutative coins—that are put in a factory. And here's what it looks like, logic-wise. So we have operators, like the circle ones are the UTXOs and the rectangle ones are the transactions. So the operator funds a factory, in this case, the coin output. And it has two possible spans, two secret paths. The first secret path is that, after four weeks, the factory operator can claim solely this output. He funded that output in the first place.
After four weeks, he can claim it. The factory, so to speak, expires after four weeks, which means that coins can only be refactored, revealed, and claimed within that timeframe. You should spend your coins in that timeframe. If you have coins that are about to expire, you do a self-swap. You send your coins back to yourself to reset that timer. So there is a little interactivity requirement. You have to be online every two weeks to speak. It's not as harsh as lightning.
 
On the second script path, with no delay, anyone can reveal the factory content—the coins that nest in that factory. And if this happens in a non-collaborative case, i.e., the factory operator is not responding anymore for a long period or is not collaborating with me, I can do an analytical closure. I can reveal the coins in a given factory from the past, and I can claim my coins there.
But a coin has, again, a lifetime of four weeks, right? After four weeks, your coin is claimable by the operator who funded it in the first place. Within the first two weeks, the coin is claimable by the recipient, the owner of the coin. And just like HDLC timeouts, which are by default set to 24 hours, the CLTV delta, just think of it as two weeks in HDLC, in-flight HDLC with a two-week timeout, the sender can get a refund. After two weeks, the sender who sent the coin and funded the coin can get a refund in that time frame, just like claiming an in-flight HDLC in Lightning. And of course, after four weeks, it's claimable by the factory operator.
                         
The reason why we have this second sort of closure, sort of time window period, is because after four weeks, the factory operator can claim it, but the recipient cannot be online and may not be able to claim it. So it's going to go to the factory operator. So as a sender, I should be able to claim it if the recipient is not responding. And from the coin output, the coin itself, each coin has three closures, three script path closures. The first one is due in four weeks, at any time.
The recipient himself can claim the coin. The second closure is after two weeks. In the last two weeks, with a relative delay, the sender of the coin can get a refund, like an HDLC timeout. The control of the coin is now in the sender's hands. And of course, after four weeks, if this coin is revealed, the factory operator can sweep it.


The first two closures are the same, except the first one is claimable by the recipient; the second closure is redeemable by the sender. So from here, you can, so if your factory operator is non-collaborative, you reveal your coin in a factory, in a non-collaborative case, or non-responsive case, and then you do a SPATH from the first script path closure, from the first tap leaf, to create this transition. You create an ATLC, so you attach an ATLC to the first TELP leaf. And you can immediately do it within 4 weeks. This state transition is called a recipient claim. And this is very similar to L2. And after doing that, after a 24-hour delay, you can get a refund. But if you have attached an ATLC, like connected an ATLC to your connector before, and you're no longer the owner of this one, you already spent it. So if you try to double-spend an ATLC, the factory operator can claim it because you already attached an ATLC to an ATLC connector.
The factory operator can immediately sort of sleep points back to himself, or if you haven't spent it already and the operator is not responding or collaborating, you can do from C to A, and we'll wait for this delay period, and then read your coins. And in the second enclosure, it is the same, but for the sender. 


The sender can spend his coins in that two-week time frame in the last two weeks. So the protocol, as it looks, doesn't look like Lightning; it's like a new unique protocol primitive, but it's interoperable with Lightning. It has Lightning interoperability at its core. Just like adding coins and connectors to a factory, the factory operator can add HDLCs and PHDLCs to a factory template. So a user, in this case, Alias, won a PayBub 21 set with Lightning, right? Alias is this protocol user, and Abub is a Lightning user. Alias can buy PayBub, and Alias has a bunch of, like, six coins in here, and in the protocol, you can have multiple factories and factory operators, and you can have your UTXO. Your coins can be distributed among other operators. So you have 2 of 2 between Alice and X here, and in the other factory, your two other coins are 2 of 2 between U and Yai, and the other two coins are between U and Z. And you can sort of do an MPP-style payout. You join three factory sessions, and you have six coins. You register for T coins in each factory session.
And the factory operators add HDLCs to their factories, and then they forward HDLCs to Bob from there. So you can do MPP; you can pay the Lightning invoice by destroying your coins, just like you create new coins.

Similarly, you can also get paid from mining with HDLC nested ATLCs or page DLC nested ATLCs. So the protocol is as in receiving by design; I mean, it's similar to silent payments. So, if out is the factory out point, the funding input, it's a unique ID, and we can come. Whenever you want to make a payment, the idea is to tweak the recipients. The recipient has a dedicated, well-known public key like an Nthop, and you tweak that public key with a unique commitment, just like what you do in silent payments. You first create a shared secret between the sender and the recipient. And you calculate a payment commitment. You put FL in this unique random data plus the shared secret plus the senders and the recipient's public key. This also provides proof of payment when the recipient claims this payment as ATLC. And you tweet at the recipient's public key; we are on a public key with the payment commitment time generator. And you send this commitment out of band, i.e., we are in Australia, to the recipient. So the recipient can look up the factory, that particular factory, and you can, okay, I see, okay. I have payout coins in this factory, I and the recipient can claim them from there. So it prevents address reuse. Each coin has a unique sort of script pub key, different sorts of public keys, and co-signer keys, it solves the async receiving issue.
The protocol can also have a penalty design similar to Lightning. So you might wonder, okay, everything is launching commitments, So if I'm receiving a coin, I need to wait for a confirmation for a settlement. We can have a penalty design, but it's like lightning so that we can have instant settlement assurance here also. So, in a factory, the first input, right, the funding input, records a new software goal, so XOR or OPCAT, we can constrain the signature first, half, and nonce to a particular field in the script so that if the factory operator double-spans the factory, as a user, I can forge the operator's private key and so that I can, as a user, redeem my previously spent coins. It provides an invalidity instant settlement trade-off here without compromising on a protocol design. There is another thing. We thought we had this sort of penalty design. When you have unconfirmed zero-conf coins, you can, of course, spend them to pay someone or create new coins for them. I mean, you can hand over zero-conf coins because a coin is a two-of-two, and the new coin is also a two-of-two, and the operator is a cosigner of both coins. But you can also pay a lightning invoice with a coin if it's zero cough. Even if it's zero cough, you can spend a coin to pay a lightning invoice because it's a two-for-two. You're spending on a two-of-two coin where the factory operator is a cosigner. And the factory operator is also a Lightning router. The same guy is also a router and can forward HTLCs to any recipient. So you can have an unconfirmed coin and the protocol, yet be able to pay a lightning invoice instantly. So it pretty much sums it up. Thank you, guys, for listening. I'm pretty sure you guys have a bunch of questions. I'm happy to have you shoot it over.
Thank you. I'm going to start the question. Sure. And I'm going to break the ice because I'm going to ask a question that might not make sense to make everyone else feel comfortable, so I'm doing this for you all. But one thing that, some of this was a little bit over my head, but one thing I'm curious about is, is the nature of the privacy necessary for this to work, or is that something that is an added feature? That wasn't clear to me. It's like, I mean, the protocol can perfectly work without a coin joining. I thought it was a bit, in fact, and this idea has evolved. The initial design was a lightning sort of channel factory design, and this evolved into a coin join design. This protocol is doable; the idea without the coin joins components, but I thought it'd be a nice addition to have.
I think I missed an important step because it seemed like all the owner had to do was wait four weeks, and then they could just take everyone's money.
And it was starting to make more sense at the end where that was intended as the penalty, but I must have missed why would they not just set up shop, take the Didn't you say that the person just waits four weeks, and then they become spendable by the owner? The factory? Yes. So, you guys think, how does the penalty mechanism work for like a sender or a sender? Yeah, the penalty mechanism is, for instance, settlement assurances, right? If you want, if you're a vendor, i.e., if you demand instance settlement, I mean, you better use Lightning. Lightning is great for that use case. But I mean, if you demand instance settlement for some reason, that's why the penalty mechanism is a nice addition here. But the protocol works perfectly without it.

I mean, because you can pay line invoices with zero call points. You have like this four-week timeout because in channel factory design in IE, yeah, you can open a bunch of channels and bundle them together in one, but you at some point have to reveal them, and it pollutes on-chain. By having a one-directional design, the liquidity of the coins excels at some point, right?
It's like a one-directional channel. So that when all coins in a factory are spent, sort of liquidity is on the factory operator's side, right? In a four-week time frame, assuming all coins are spent in a four-week time frame so that the factory operator can sleep his coin, I mean the factory. When you say spent, do you mean within the factory? Sleeping is on-chain; sleeping involves an on-chain mechanism. What do you mean to spend? Just normal spending? Like spending in the protocol, they are on-chain. Are they off-chain coins? They are, too. It's off-chain. When you spend coins, they're entirely off-chain. The only on-chain footprint is the factory. You have this factory if you have one or more inputs and four or three outputs every five seconds, and when you spend a coin and you create new coins, you spend coins from the previous factory, and that spending is off-chain. It doesn't have: Why is that big off-chain coin joining? I guess I don't. Yeah, it's an off-chain coin join. If I may, I think what you're asking is: How do you prevent your coins from getting swept in the factory? I believe the answer is that you have to keep moving. You've got to keep jumping from one factory to the next. If your coins are about to expire, you send them back to your cell phone. Yeah, but what if someone just says they didn't get my message or whatever?

## Burak:
 Oh yeah, it's atomic.
So I'm DMing you a message, right?
I sent you a coin. If you don't get the message, After two weeks, I get a timeout refund. I mean, then I'm able to, as a sender, redeem the coins I've sent. You put The whole thing you pull on to layer one? The whole thing is off-chain. The closures are on the chain. I mean, the closures—you have the ability. In the first two weeks, the recipient can only add an ATLC. In the last two weeks, the center has

## First participant:
 I've been saying this all. I've been saying this for 15 days, and nothing's happening. I just want to get my money back out of this factory. I want to go to a different factory.

## Burak: 
No, no, no—the same factory. Because the TILF has remained unchanged. You're still on the same client.

## First participant:
 How many people do you think would be in each factory?

## Burak: 
A thousand. I mean, if it's an update, template, update, or verify design, it's millions.

## First participant: 
Yeah, but don't you think, like, I thought the factory design was flawed in that if any single person in the factory stops responding, the whole thing has to be drawn?

## Burak: 
Yeah, exactly the disaster scenario.

## First participant:
 Yeah, I mean, it's crazy that more than like 20 right, that would be like already pushing.

## Burak:
 Yeah, I mean, the disaster scenario also goes for lightning. If someone broadcasts all states, I mean, it's a disastrous scenario.

## First participant:
 I get it, but you easily join the factory with zero coins or like five dollars, and then what would it take to bring the factory on a chain? So a factory transaction is like 20, or 40 times the size of a normal transaction.

## Burak:
 Yeah. So ideally, in the end, we should have a top-level update verifier designed for the coins so that you're only redeeming the coins you're interested in. But yeah, I mean the coin is below dust, like one satin, worthless coin. In theory, you can claim it, but economically, it doesn't make sense. But what the protocol does is set the incentives right so that the factory operator doesn't cheat. I think that also goes for lightning. But you have the ability to claim that one Satoshi, although it's not economically...

## First participant:
 But I was just trying to make sure that I understood, because I think I don't understand it, right? So it's like a bunch of off-chain coin joins, and then on layer one you spend in, you join the factory.

## Burak: 
So you have coins, right?
I mean, you're assuming you have coins, but I mean, in the first place...
I said that I had Bitcoin on layer one. Okay, so the first step is: how do you onboard to the protocol, right? You have one machine, you take it on the Bitcoin chain, and you want to onboard. You were using—it could be—you can withdraw from Bitfinex or something—an exchange that supports the protocol, right? So that the exchange has points already in the protocol. You can get paid for it, but if you have Bitcoin,.

## First participant:
 Because someone has already been onboarded to Layer 2.

## Burak:
 Yeah, you were onboarded to Layer 2. You have Bitcoin on your chain.

## First participant:
 But the first person opens the channel.

## Burak:
 There are no channels here. Maybe the factory is there.

## Second participant:
 No, like they have a wallet. I tell you, hey, do you know what Bitcoin is? You say no. Okay, you go to the wallet; I go to the wallet, and I send you some stocks. That means I have to marry Satoshi. That's the first step. You could try to peel the oranges, but I believe that is extremely difficult. I think this is what he's saying: there are no nodes, no channels; it's just wallets.

## Burak:
 Right, okay. I'll count on that as what you're saying.

## First and third participants: 
Yeah, so if anyone has one, that's the question. The first is if Biffin X is already onboarded into the factory like they already have the coins. Yeah, we have to call them some days. We call them a Barack coin. They're the next to have these two coins. I can get them, and I can send my public keys. Yeah, and then I have a wall that supports this. When they refresh it every five seconds, they refresh it into something where it swaps out the, there's a new Merkle root or whatever that has, instead of something that never contained my key, it's now something that contains my key. So now I'm on board with this scheme.

## Burak: 
So the flow is like you have Bitfinex, and Bitfinex assumes it has already collected a protocol, and you want to withdraw from Bitfinex to your business protocol wallet. You have, like, a dedicated public key. You paste the public key into the Bitfinex interface, and they make you a payout. And Bitfinex offers coins. Two of the coins are exchanged between the factory operator, and Bitfinex joins the factory operator in the next session and creates new coins. He spends his coins and creates new coins for you, the payout coins for you. And you're a cosigner on this; you're a cosigner of your coins, but you can do a refund. It has a script for refund closure. If you get a coin, yes, under a new factory, Bitfinex can prove it. It's a launch commitment. I can prove it to you. Okay, I paid you. You have a new coin, you have a bunch of coins under a new factory, or Bitfinex can also DM you, okay?
 

## First participant:
 Bitfinex also, every block rolling over, like an output or something?
It must be because my public key is making it into something.

## Burak: 
When Bitfinex joins, I mean, if they're paying constant payouts into Bitfinex, Bitfinex joins the factory session every five seconds, yes.

## First participant:
 Yeah, but isn't there something that's at least 32 bytes long on layer one that has to change when I onboard, right?

## Burak:
 So, are you asking about the first onboarding step?

## First participant:
 Yeah, I have on-chain layer one Bitcoin now joined.

## Burak:
 How do you join? How do you have a coin? Okay, so the first initial onboarding protocol step. So you have a layer one UTXO, and you have a hardware bullet, and you want to convert that Bitcoin into the protocol coins. So you deposit your single set, you have created a type of coin, and you deposit it into a two-of-two chain. On a chain of Bitcoin, you take two of two, just like coins, but coins are... It's like a channel, but a one-time-use-only channel.
Two of two, and from there, you can even pay away any money.
So if it's a real channel, or you can, because you can get paid from an HDLC Nested coin in the protocol, or you can, coins are off-chain, but you created an on-chain coin, right, two of two, and you can join a coin with that on-chain coin. You can register that coin, the on-chain coin, for the next coin join session, the fact-check session.

## First participant: 
I just wanted to quickly recap it in my mind to make sure I understood it, and then ask my question. So the factory is putting money into this transaction to create coins. And then, if I have money, I want to buy into this contract, and we're going to have some secret that we share out of band where I can control where you spend those coins.
So you're using the connectors to do it in an atomic way?

## Burak:
 Yeah, you use connectors in an atomic way; someone pays you, and in the factory, you're not aware of it. I mean the factory is there, whether it's confirmed or not, the factory is there, you're in the way, but you realize, okay, I have a DM, okay, someone says, okay, I paid you, in this factory, go check it out, and you go check it out, okay, real, I know the factory content because he sent me, the center sent me the factory content and the factory ID, the transaction ID, and go check it out, okay, there is a factory, there are coins, you'll verify the content and all that, and okay, I see there are a bunch of coins, and then with each coin, I mean, the sender can tell you the index in what index your coins are in the factory, and then you check it out, okay, calculate the script tab key, okay, and my cosigner key is this, with this tweak at, and the cosigner key is null, publicly null, the LSB, I mean the factor of it is publicly null, you calculate the tapping script, and okay, this is a coin, this is the script pubkey, this coin is mine.

## First participant:
 Okay, so are the connectors also their outputs?

## Burak:
 Connectors are also transaction outputs. Yes, just like coins.
 
They're commitments. Yes, just like coins. The difference is that connectors are not told to do anything, and they carry dust value.

## First participant: 
Okay, I sort of understood that. One thing that you brought up that I didn't understand is the XOR operation as a penalty.
Yeah. Can you explain that a little bit? That's the right way.

## Burak:
 Sure. So you're receiving a coin. You have this coin, i.e., coin number one. Let's say it carries 1,000 sets. You have this coin. The factory is not confirmed. It's in my memory. But you demand your settlement. What happens is the factory; you can accept it as Zeroconf as it is. You can say, Okay, I consider this payment, payout, instant, settled.
 Although it's not confirmed because the factory operator is to double spend on this factory transaction, you forge the factory operator's private key. And if you have previously spent coins in the protocol, you have coins in the past; you spent them already, but because you can forge the factory operators with 202, the private key, you can forge with 202, and you can claim your previously spent points.

## First participant:
 Okay, so because you've already done business, are you using data from an existing transaction and this new transaction to try and forge the factory operators?

## Burak: 
If you're already on board, assuming you already have, just like Lightning, when you're on board, but if you have previous points and have already spent them, then you can penalize your partner from there. But it also sets the incentives right. But other than that, you can pay the Lightning invoice. If you just got on board, you cannot have instant settlement, yes, because you don't have any previously spent points. What you can do is still consider it an instance because, I don't know, you can pay a Lightning invoice for it. The Lightning invoice involves an instance settlement by nature.

## First participant:
 Do you run into issues with fees for the transaction clearing?

## Burak:
 So this is a liquidity network, just like Lightning. So they're launching fees, but it's a factory commitment. So, this is like 250 bytes, like one transaction, right? It's a launching transaction, and they'll have, say, 1,000 participants and the fees are divided by that number of participants; that's like 25,000 subs, divided by that number of participants, plus liquidity fees. It's lightning, and there's all liquidity networks. This liquidity is used less efficiently here.

## First participant:
 Thank you. Sure. All right, cool. Can I ask one question? So, in this diagram, the stuff on the left is confirmed. So you can see three outputs, and then that coin's output is sort of an Opsy TV kind of thing that you can expand out to 100. So, when everyone uses this, they can see that my share is coming from that. Okay, so then there's this four-week delay. Let's say there's a scenario where everyone's aware, like, okay, this operator, this factory guy, he's offline, he's dead. So, we know, why wait four weeks? We need to close. What is the process that any, let's say, large and there is a hundred? Is it the case that any of the? 100 can then close at the current state, or do you need it? Like, what is the process?

## Burak: 
Oh, yeah, sure, so you're doing coins, but that's not enough to claim. So from each real coin, you also have to make a claim, a sort of closure, from each coin, and then you wait for 24 hours to finally settle, just like an auto.

## First participant:
 Okay, and so that, is that multi-stage fan art, or is that like, okay, you spend coins, you get like 100 different outputs, and then each one of those, people have to sweep on their own, or?

## Burak:
 Yeah, so I mean, this is a bit of a less efficient design because if you want to claim just one coin, you have to reveal all coins. That's what tablet update verification solves, or CTV. You can emulate it with CTV, but ideally, with TX hash, we can emulate it perfectly. But in the current design, you have to reveal all the coins to spend, to redeem your own, and from there, you do another spend from the coin and wait, and then you redeem it. You just feed your funds.

## First Participant: 
Yeah, so the trade-off is sort of if you think it's unlikely, well, yeah. And yeah, so there's trade-offs like, okay, if you make it a tree, then the worst case is worse, but if it's all at once, then you have this sort of frivolous problem where there are too many people, one person posts it, and then it sort of ruins it for everyone.

## Burak: 
Yeah.

## First Participant:
 Yeah, so it was. Okay,  got it. Cool.

## Second participant: 
I have a question about what you said before: I need to connect as a receiver, right? I need to connect to a factory, right?

## Burak:
 You don't have to connect. You don't know who the factory is. You just got an orange pill, and you don't know who. You just downloaded a wallet. I mean, you know what a factory is, because it's like a factory wallet—a wallet operated by a factory. And I sent you a coin. I could send you a coin from a different factory, too. Like, it can be two different wallets. I use factory ABC and factory XIZ, but it's an interoperable design, right? I can send you coins, but the coins I'm sending you are 12–2 between them; say I'm using factory XIZ. You have to make some coins with ABC. I'm sending you coins, and the coins are between you and XSS, my factory. Your vault is compatible with other factories too, so you can recognize your coins at other factories.

## Second participant:
 So actually, my question was like, okay, basically, when you DM me, hey, go look it up, you have a payment coming to you, I will recognize the pubkey, the well-known pubkey, or factory that way, so I know where to look it up.

## Burak: 
Yeah, exactly. In the DM, I also tell you who the factory is and how it works.

## Second participant:
 So this factory transaction, is it sitting on the chain or in the mempool?
Burak: Is it confirmed? Some of them are confirmed; the new ones are in the mempool. 

## Second participant: 
Okay, so if they're sitting in the mempool, you can push things out of the mempool. If the mempool overflows and things like that.

## Burak: 
Yeah, fee bumping doesn't work here because if you add or increase a fee, the transaction ID changes, which violates the autonomy of the name. So ideally, you should do CPIP-style bumping. So we should either have another output, which is spendable by the fact, or we have a change, yeah. So you can do CPF-style bumping that way without affecting the TXID. 
## Second participant:
 So theoretically, I could use this factory transaction: it's sitting in the mempool, I use it to pay somebody, I get the goods, and then I do some shenanigans in the mempool, it gets thrown out of various mempool, and the payment never happens.

## Burak: 
Yeah, that's the thing, right? The factory operator should make sure that, yeah, this is going to be confirmed. You should have a factory operator because otherwise, the factory operator is not able to claim the coins that he sent.

## Second participant:
 Yeah, but then the incentive of the factory operator, making sure it's confirmed, is quite an expensive process, especially if people are trying to fix it right now, but under the current rules and the mapping rule, you can get evicted with people doing weird things. 

## Burak:
 Sure. So there have to be a lot of workarounds for that, yeah? Yeah, and making sure that's discussed.

## Second participant:
 So the factory, if I want to use it for payments, I can start using it; I don't know, will not use the six-block rules, but something like that. So this is, in many ways, slow.

## Burak: 
Yeah, if you have previously spent coins, it can penalize the factory operator that way, or you can. I mean, I think that Lightning is better suited for vendors who demand instant settlements. I think I have this analogy. Lightning is UTP; this is CTP, WCP. His protocol is more like a user protocol, but Lightning is more like a vendor protocol. If you're a vendor, you know your cash inflows are predictable, you can acquire some liquidity from someone, and you demand instant settlement. And this is more like you have a user, your cash inflows, it's not predictable, and you can use the protocol to straight on board and send and receive coins without liquidity constraints and pay by the invoice.

## Second participant:
 Okay, so you're making a choice between doing things immediately versus, like, liquidity use or something like that, if I understand correctly?

## Burak:
 That's right.
Second participant: So, there is, like in Lightning, the instantaneous part. And here you're choosing not to have the instantaneous part, but to make it cheaper or... What's the trade-off? It's all about the liquidity problem. Okay, yes. So it's like the... Okay. Cool. Yes, I mean, they're all because of the networks, yeah. Okay. And if I have another sec., I have another question. So, you said that if I have one of the coins and then I try to double spend or something like that, the factory operator gets the money.
Burak: Because I said so too, you cannot double-spend.
Second participant: No, so did I hear. I thought that you mentioned...
Burak: Double-spending the factory; the factory operator if double-spending the factory.
Second participant: Oh, if the factory operator tries to double spend... the factory that he created. Okay, yeah. So if I'm trying to move... Can you give a quick explanation? I have coins in the factory, and now I want to give these coins to somebody. What happens if it's inside the factory? What happens if it's outside the factory?

## Burak:
 So in an on-chain payout, if you're paying someone in an on-chain transaction, you can double spend it. And then, if I deliver you good products or services, yeah, I can get it right.
Here, if I, as a vendor, have this penalty assurance, I previously spent coins. I can't do my next-term settlement here if the factory operator double-spends it. Of course, as a vendor, I ensure that the factory pays adequate fees for the coins I receive. I see the message. Okay, this is going to be confirmed. I'm sure it's going to be confirmed, and at some point it will be confirmed, right? If there is a double spend in the mempool, well, then I'm penalized as a vendor, the factory operator, so I'll claim my previously spent coins anyway.

## Second participant:
 I'm asking; I own coin zero. Now I want to give you three Satoshis, which are five Satoshis. What exactly is coin zero? How do we do that?

## Burak: 
You have Coin Zero in this factory, right? This is like a confirmed factory deep in the blockchain. You want to spend a zero coin and say it holds 100 sets. And then, with that coin, you join a new factory, and you register for that coin. And because it's a tool too, the factory operator knows that the factory operator funded this coin in the first place one time ago and can authorize this coin whether it's banned, expired, OFAC, or whatever. And you can join a new factory session and register for this coin.

## Second participant: 
With the same operator?

## Burak:
 Huh?

## Second participant: 
With the same operator?

## Burak:
 With the same operator, yeah.

## Second participant:
 Okay, I cannot do this with a different operator.

## Burak:
 Oh, yeah, exactly. You have to use the same operator, the 12-2 between you and the coin, as the factory operator, and you join the same factory operator. You ask to join his new session, like three minutes ahead, and you join it. You register it in the registration phase, you register for coin zero, and then you register for the payouts, plus change coins. Destroy coin zero and create new coins. I mean, you register for the payout coins based on the blanket credentials you received from the coin registration part. From this coin, it's a TOV2. From this coin, it's not a TOV2. The coin is not a TOV2. The coin is, this is the scheme, from a coin you have, from the first closure A, A to C, So this is a pre-computed sort of closure. From C to A, we can use CTV to constrain A to be the transaction output. And from here, ATLC is a 2 out of 2. And from A, you are a cosigner of A. The other cosigner of A is the operator. And you sign a transaction, an off-chain transaction, this transaction, ATLC Connect, by adding this connector, ATLC Connect, UTXO, to the second input. And this UTXO lives in the NIF factory; he commits to the NIF factory. Because you're signing with Ccash, this transaction ID is the factory's transaction ID, which commits to the factory and sort of forms a TX lock. A hash lock can look like a code TX lock.
So that you sign it so that you exchange signatures with the operator and get a signature. I'm good to go. I will release this factory. If you don't sign, you get banned from that session.

## Second participant: 
Well, where in all of this are you getting the coin? I'm trying to send it to you.

## Burak: 
Oh, you're sending me? Yeah, so you added in the Bitcoin registration phase, you added my coin, you did a tweet, you know my public key, Nostra public key, you tweet at the tweet, you send me a DM, then you added that coin, you registered that coin in the session, and then it's now committed to the transaction ID of the factory template. Then it forms a TX block for the template, and then the factory operator broadcasts it to mempool. So I see, okay, I see an unconfirmed incoming factory, and I have some coins under that factory. I see the payment; I see the factory pays enough fees. I can spend a coin; you hand it to me over a Zeroconf coin, right, and I can spend a coin on someone else or pay a lightning invoice with it instantly, or I can even just hold it.

## Second participant: 
Okay, so it's up to the factory operator to see that I'm not doing it twice.
I'm not paying you, for example.

## Burak:
 If you try to do it twice, I mean the factory operator won't let you in because the coin of the  80s is a 12 to do a second spent.

## Second participant:
 But what if I'm the factory operator? Like, what's in it for me to lose by allowing this?

## Burak:
 For the factory operator?

## Second participant: 
Yeah.

## Burak:
 If you do try to do it, you double-spend. If you try to double-spend, you get a penalty.

## Second participant:
 From whom?

## Burak:
 From anyone. It's going to be made public to the whole network. Anyone can forge my private key; in that case, any participants, pre-private participants. And if not, you can just not demand it as a settlement. You may not be interested in demanding it as a settlement; you can just receive coins and wait for them to be converted. If you don't want to make it, consider it settled. If not, with XOR or CAT, you can do it in the penalty mechanism.

## Second Participant:
 Let's take it offline because I think we're killing everyone.

## Burak:
 Sure.

## First participant:
 So my understanding is that in each factory, the confirmed factory has coin connectors and the factory output factory chain.

## Burak:
 yes.

## First participant: 
So is the connector is that a part of the pinning mechanism that I'm able as a person who has a coin, like so I submit an on-chain UTXO to a vector operator, I receive a coin, is the connector part of the mechanism, the pinning mechanism, like because basically in the connector, if we have the data, I would need to be able to, like if you try to double spin a vector operator, I can take the data from the previous connector and now get the funds back to myself? Is that what the purpose of the connector is?

## Buarak:
 Your question is if you're sending an on-chain UTXO, right? To pay someone?

## First participant:
 So I'm already in a confirmed factory. I'm in a confirmed factory.

## Burak: 
In a confirmed, okay, you're coins in a confirmed factory.

## First participant:
 I have coins in a confirmed factory. Is the connector part of the pivot mechanism if the factory operator tries to double spin?
Is that the purpose of the connector?

## Burak
: The connector is to commit to the transaction ID, so that if there is a double spin, it breaks your coin. The operator can no longer redeem your coin. Because the connector is part of the factory, it commits to the transaction ID of the factory, so if the factory already double spends...

## First participant:
 So the connector is the operative part of the bidding mechanism. Without the connector, as somebody who has a coin in the factory, I would be able to spend it to spin, but I wouldn't be able to penalize the operator.

## Burak:
 Not penalize. What penalizing is is a different sort of mechanism you won't be able to factory. It's for the factory operator to have assurance because the factory operator pays someone with his liquidity and should be able to claim your coins. For a factory operator to claim your coins, the factory operator needs that assurance that connects to the connector.
Second participant: Shall we continue with the rest? Give it a round of applause.

