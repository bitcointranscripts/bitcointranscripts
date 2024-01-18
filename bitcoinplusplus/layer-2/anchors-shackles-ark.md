---
title: "Anchors & Shackles (Ark)"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://www.youtube.com/watch?v=OBt1nS14Ac4
tags: []
speakers: []
categories: ['conference']
date: 2023-06-24
---
So hey guys, my name is Borat.
Today I'll be talking about something that I've been working on for the past, let's say, six months or so.
To give a bit of a background, I started first in a big block sort of camp and then got introduced later to Liquid.
And I did some covenant R&D on Liquid for about two years, and now I'm recently exploring the Lightning space for about a year.
And as someone who initially comes sort of from that sort of big block camp, I've always had objections towards lightning, mainly around the UX, from backups to interactivity to liquidity problems.
I've had severe objections.
A few months ago, I tried to sort of working on a new light and more to address these problems.
And I've come to realization that these objections, the objections that I had in the past, they're all addressable in the long run.
I, you know, page DLCs can sold in, same receiving initiative plus proof of payment, but there is still one big problem, the inbound liquidity.
To me, it's like a non-starter.
If you're orange billing someone for the first time and you cannot receive, what happens is you get a swap, some ring swap in, and it doesn't scale.
And to me, if something works 90% of the time, it doesn't work 10%, to me it doesn't work.
It has to be zero friction.
So I sort of try to come up with solutions to address these problems.
And then today I'll be presenting a new sort of alternative Layer 2 protocol.
It all started as a wallet idea, a Lightning idea based on channel factories and all that.
And it later evolved into a layer two on its own.
At some point I realized, okay, what I'm building is lightning, but it really is like a new layer two in its core.
At its core, it's like internally, it's like a new off-chain protocol.
So the protocol is, it requires APO or CTV, a new covenant primitive to work.
That's not something we can do on Bitcoin today.
We can do it in Bitcoin Inquisition's Signet, and I think that's how we're gonna start.
But to give a high-level overview, first of all, we haven't set a name yet for the protocol.
So to give a high-level overview, the protocol has no liquidity constraints.
It's a simple protocol.
It mimics the on-chain UX.
Just like you do on-chain wallets, you have an address you can receive, send, hold, simple.
You don't have any interactivity requirements.
And you don't have to acquire inbound liquidity to onboard to the system in the first place.
You don't have to run a server, you can use your smartphone, don't have much interactivity requirements.
And every payment takes place in a coin join route, so you don't leave your, especially receivers, they do not leave their identity.
You know, in Lightning, if hubs call it or they comply with OFAC, you know, two hubs can sort of extract the payment route.
If I'm using IE and LSB XIZ and you're connected to ABC and they have direct channel each other so the receipt is 12A, then they can call you to extract the payment because it's linked through the same HDLC, the Bolt 11 hash identifier.
So in this protocol, it's not a state channel design.
It's not a roll-up design of any sort, it's really its own category.
So, here is a comparison table, comparing this protocol with Lightning on-chain, also Ecache, obviously Ecache, Charm and Ecache, FedEvent stuff, it's called Studio, so, you know, it's controversial what, you know, what Layer 2 is and not.
To me, E-cash doesn't fall into Layer 2 category, but it's good to compare.
So, you know, on-chain Bitcoin, you know, to me Lightning is the only layer 1, as related to Bitcoin.
To me, the layer 2 definition is really like a sort of separate piece of software where you transact Bitcoin without polluting on-chain, But yet you can revert your coins back to one chain without asking for a corporation.
So by that definition, the protocol falls into a layer two category.
So it's self-constitutional.
You can unilaterally revert your coins back on chain, but you transact off the chain.
So interactivity, well, PHTLCs solve the receiving issue.
And you can generate print.
And they don't have a generic pre-image ready offline but you still have to sign or monitor the network for channel breaches if you're not trusting a watchtower.
And just like on-chain, you don't have to be online like that.
Scalability-wise, I think this is the number one, the biggest property we have.
Lightning, you cannot onboard the whole planet to lightning, it doesn't scale.
Channel openings and some might swap ins, so out, they do not scale.
It's not only the on-chain footprint, right?
The non-liquidity doesn't scale.
I have this utopic idea to onboard the whole planet to Bitcoin in a non-custodial way.
I know in reality it's probably never going to happen, but I'm super obsessed with it.
So I think my goal is to be able to at least give people an option the whole planet to onboard Bitcoin and not custodially so in theory with this primitive you can onboard the whole planet in theory on chain footprint wise there are probably other challenges but the point is you don't consume any pretty much, you don't consume any pretty much footprint, On-chain footprint.
Everything is off-chain, pretty much.
Unlike in Lightning, you have to touch on-chain sometimes.
Of course, on-chain is the worst.
Nothing touches on-chain, doesn't scale, anything that touches.
And Privacy, again, guys, it's also controversial, right?
Lightning versus on-chain privacy.
To me, lightning is worse than on-chain, but to many people, they argue on-chain is worse than lightning.
But with this primitive, whenever you make a payment, the payment takes place in a coin-join route, sort of like an off-chain coin-join protocol.
So, and you know, coin-joins today, they're mostly used for, you know, data market use cases maybe, but here, anonymity set is everyone.
Anyone who involves in a payment, that payment is in a coin join, in a blended mixing route maybe, that's pretty correct.
So onboarding, again, you don't have any onboarding setup.
You onboard someone, you want to tip someone, you just onboard Orangefield someone, and you can receive payment like on-chain, but it scales.
So it's a simple protocol.
I mean, it's not a state channel design.
I think it's conceptually simple, it's simple to reason about.
So there are two parties, users and the operators.
And operators are akin to service providers in Lightning, LSPs. And in fact, factory operators are also LSPs in this protocol.
They can run Lightning Rogers, too.
You can pay with this protocol Lightning invoice as it's interoperable with Lightning.
It's not a competitor by any means.
It's in fact much, you know, it's a compliment Lightning bar.
So users, they're not interactive entities, they hold and receive coins just like they do on chain, but they do it entirely off chain.
And factory operators, just like LSPs, they provide liquidity to the protocol, But it's slightly different.
In fact, Lightning uses liquidity more efficiently because channels are bidirectional.
Here, it's more like a one-directional design.
The factory operator has to constantly provide liquidity to the protocol.
So the protocol, again, the idea requires a common primitive.
We need a common primitive to constrain transaction outputs of a spending transaction.
And you can use CTV for that, which is a bit controversial.
And We can use an APO to emulate CTV.
We can emulate it by hard coding of the signature 65, signature and 33, but unknown pop key type.
And script to emulate the CTV use case.
There are other alternatives, TI-cache and some other combinations in even syntheticity.
But it requires a common and primitive constraint outputs in advance of creating a Bitcoin output.
So it's just like a coin join.
You have a set of coins.
Coins are Bitcoin transaction outputs, but they live off the chain.
They ideally never touch on chain, but you can of course, you know, literally revert, but the coins live off the chain.
Think of like a UTXO set that lives entirely off the chain.
So you have a set of coins in your wallet, software, from one set to a million, just forget about the dust limit, just keep things simple, from one to a million sets.
So the design is, the design starts with a factory.
So factory, it's like a channel factory, I name it factory, could be something else, the naming, but because it's similar to channel factories, I name it factory.
The factories are, is a shared UTXO model.
So factory is a Bitcoin transaction output.
It's a shared UTXO.
And it has a bunch of nested coins in it.
The coins I mentioned earlier, they live in this factory, under this factory.
They nest in these factories.
And the factory operator is the one who creates factory, say, in every five seconds to put things simple.
But contrary to CoinJoin, CoinJoin can take from hours to days, a CoinJoin session.
This one, think of a CoinJoin round that takes place in a regular basis in every say five seconds.
So every single one of these factories are a coin join.
They're like a blinded mixing round.
And it's operated by, the factory outputs are funded by the factory operator.
And here is what a factory looks like.
This is the factory that the factory operator sort of creates, crops in every five seconds.
So you have one or more inputs to fund.
And the coins output and connectors output and a factory change.
So coins output has a bunch of coins.
Coins that you have, coins live in this output.
And each coin is a 12-2, just like lightning.
Like the initial idea was to have lightning channels instead of coins that nest in the coins output.
But the things have evolved over time.
So instead of having lightning channels in one UTXO, just like coin pools, factories, we have coins.
And coin is like a one-time use only channel.
You spend it and you create new coins, just like one chain.
And the idea is that you have a bunch of coins that are coming to a single transaction called output12coins.
You can unilaterally reveal the coins content, the factory content.
Sort of the coins have like a script path forger, and anyone who knows the sort of the template hash, the coins content, can reveal the content.
And the connectors output, the second output in a factory, has a bunch of connectors similarly.
But this one is more like a withdrawal tree, update, top-leaf, update, verify style, withdrawal tree.
The difference is you, you know, we have connectors.
Connectors are also Bitcoin transaction outputs that connects to this output, connectors output.
They're commitments just like coins, but the difference is that you have to reveal one by one.
You have to reveal connectors one by one.
In coins, you have to reveal them all at once.
So the primitive, I mean the protocol is at its core, realized at the time of contract, this is a new buzzword I made up.
It's ATLC, so this is a comparison table.
You know, HDLCs are the absolute worst.
You know, as soon as you're receiving, you can't create a preimage when you're offline.
HTLC solves that.
Also, you know, proof of payment is a bit of a gray area in HTLCs. But ATLCs check all the boxes, HTLCs do, but differently we have, you know, ATLCs has no liquidity constraints.
So you don't have anything about liquidity requirement you receive it's like a magic button you push a button and you receive whatever you deserve like on like on one chain.
So to illustrate things simpler, so we have a coin, we have a bunch of coins.
Each one of these coins are 12-2.
12-2 between the coin owner and the factory operator, just like lightning.
Like 12-2 between me and my channel partner.
Think of channel partner as the factory operator, like a central hub.
I have a 12-2, I'm a co-signer, a bunch of coins.
And I join, if I want to spend these coins, right?
Like my UTXOs, I want to spend them.
And I join a factory session, just like joining a CoinJoin session.
And the factory operator is a blinded coordinator.
And I register my coins first on the left.
In a CoinJoin, you register inputs and outputs in the same phase.
You register the coins, and these coins are from the previous factories, right?
You get paid from coins from someone else in the past, and you create, you now register for new coins, payout coins or plus change in the round.
And you know, in this round, there are many participants, like you can have like thousands of transactions, you know, coins in a coin joint.
Here, you know, you still have the same limit, but with Tableau, if they verify, it can be millions.
But the idea is to have, it's like a coin, join or retain UX, you have coin on the left, you're spending, and you're creating new coins.
You're destroying coins, and you're creating new coins.
So on the right.
So these coins are, you know, again, these coins are commitments.
So the factory operator here, right?
We have a session, a factory session, And the factory operator is trying to create a new factory.
The factory operator and his factory template, I mean the factory he's crafting, is placing these coins, coins that we registered, among many other participants.
And then the factory operator places a set of additional outputs in the factory template called ATLC connectors.
So ATLC connectors are added to factory, the number of spending coin times on the left.
So we are spending N coins, and the factory operator adds N ATLC connectors.
And we are creating M new coins.
And what happens next?
You know, we did the input registration port, the audit registration port, and it's the signing phase.
So, of course, connectors and coins are mixed, it's a mixing round.
So when I register a coin on the left, operator gives me a blinded credential so that I can register for the new coins.
And then in the signing phase, I attach ATLC and ATLC to my coin in order to sign, to really lock my coins in for the factory.
So, this is similar to Lightning, right?
You have, think of Coin as a tool to one time use channel, Lightning channel, and you attach an ATLC instead of HDLC.
And from there, you sign the ATLC with the 12.2 to connect to an ATLC connector.
So with that ATLC, you're signing an off-chain transaction, like one state update, simple.
One state update only.
You're signing an ATLC from the 12.2 from the ATLC to connect to an ATLC connector.
And you do the same for all other coins.
So you sign, you know, all participants in a round, they add ATLC to their coin and connect that ATLC to its connector.
And if someone hesitates to, you know, add an ATLC, you know, you get back, you know, the factotrupid bends, you know, bends you from the session.
So this is what the on-chain transaction looks like.
It's pretty simple.
The ATLC is a two of two.
I'm the call signer.
I'm spending this coin, and I'm paying out to Bob, someone, under a new factory, and I'm signing this off-chain transaction to do so, to connect my ATLC to your connector.
I'm signing the ATLC, the first input itself.
The first input of the ATLC I'm signing, a call signing from the 12.2. Again, the other call signer is the factory operator.
And the second input I place, on the ATLC connector from the new factory.
The ATLC in the first input I'm spending is from a previous factory.
The connector, ATLC connector, the second input is from the new factory.
And ATLC connectors, they carry dust.
And they are single-sig spendable by the factory operator.
ATLC is a tool of two, connectors are single-sig factory operators.
So in the outputs, we place one output for the factory operator to sleep, to claim his funds, to claim these funds.
So by doing that, as you remember, we have coins in a factory, and by doing that, we, you know, the factory operator created a set of new coins.
It's an on-chain transaction.
You provide liquidity for these coins.
And the factory operator now has to claim my coin, should be able to claim my coin, my previous coins in here, right?
And in order to do so, the factory has to exist.
The factory operator should not double spend this factory.
If the factory operator double spends, the Factory operator is not able to claim my ATLC, my first input, because I signed the off-chain transaction with SIGHASHALL and it commits to the second input, ARTPOINT, and it is the transaction ID of the factory.
So in order for an ATLC to be claimed by the factory operator, the factory operator should not double spend the factory.
If there is a double spend, it's not atomic, it's an atomic construction.
My ATLC is no longer redeemable.
I can do an unlegitimate closure for my ATLC with the script path.
So it provides an atomic layout construction of an aggregate transfer schedule here.
So here's a bit of a logical overview.
So, you know, you remember we have coins, commutative coins that are put in a factory.
And here's what it looks like logic-wise.
So we have, you know, operator, like the circle ones are the UTXOs and the rectangle ones are the transactions.
So the operator funds a factory, in this case the coins output.
And It has two possible spans, two secret paths.
The first secret path, after four weeks, the factory operator can claim, solely can claim this output.
He funded that output in the first place.
After four weeks, he can claim it.
The factory, so to speak, expires after four weeks, which means that coins can only be refactored, can only be revealed and claimed within that timeframe, for a big timeframe.
You should spend your coins in that timeframe.
If you have coins that are about to expire, you do a self swap.
You send your coins back to yourself to reset that timer.
So there is a little interactivity requirement.
You have to be online every two weeks to speak.
It's not as harsh as lightning.
The second script path, with no delay, anyone can reveal the factory content, the coins that nest in that factory.
And this happens in a non-collaborative case, i.e. The factory operator is not responding anymore for a long period or not collaborating with me, I can do an analytical closure.
I can reveal the coins in a given factory in the past and I can from there, from there, from the coin here, I can claim my coins.
But a coin has, again, a lifetime of four weeks, right?
After four weeks, your coin is claimable by the operator who funded the coin in the first place.
Within the first two weeks, the coin is claimable by the recipient, the owner of the coin.
And just like HDLC timeouts, which is by default set to 24 hours, the CLTV delta, just think of it as two weeks in HDLC, in-flight HDLC with a two-week timeout, the sender can get a refund.
After two weeks, the sender who sent the coin, funded the coin, can get a refund in that time frame, just like claiming an in-flight HDLC in Lightning.
And of course, after four weeks, it's claimable by the factory operator.
The reason why we have this second sort of closure, sort of time window period, because after four weeks, factory operator can claim it, but the recipient cannot be online, may not be able to claim it So it's going to go to factory operator.
So as a sender, I should be able to claim it if recipient is not responding.
And from the coin output, the coin itself, each coin has three closures, three script path closures.
The first one is within four weeks, any time.
The recipient himself can claim the coin.
And the second closure is after two weeks, in the last two weeks, With a relative delay, the sender of the coin can get a refund, like an HDLC timeout.
The control of the coin is now in the sender's hand.
And of course, after four weeks, if this coin is revealed, right, the factory operator can sweep it.
The first two closures are literally the same, except the first one is claimable by the recipient, the second closure is redeemable by the sender.
So from here, you know, you can, so if your factory operator is non-collaborative, you reveal your coin in a factory, in a non-collaborative case, or non-responsive case, and then you do a SPATH from the first script path closure, from the first tap leaf, to create this transition.
A, you create an ATLC, so you attach an ATLC from the first TELP leaf.
And you can immediately do it within 4 weeks.
And this state transition is called recipient claim.
And this is very similar to L2.
And after doing that, after 24 hours delay, you can get a refund.
But if you have attached an ATLC, like connected an ATLC to your connector before, and you're no longer owner of this one, you already spent it.
So if you try to double spend an ATLC, the factory operator can claim it because you already attached an ATLC to an ATLC connector.
The factory operator can immediately sort of sleep points back to himself, O.
Or if you haven't spent it already and the operator is not responding, not collaborating, you can do from C to A and we'll wait for this delay period, and then reading your coins.
And in the second enclosure, it is the same, but for the sender.
The sender can spend his coins in that two-week time frame in the last two weeks.
So the protocol, it looks like, doesn't look like Lightning, it's like a new unique protocol primitive, but it's interoperable with Lightning.
It has Lightning interoperability at its core.
Just like adding coins and connectors to a factory, the factory operator can add HDLCs and PHDLCs to a factory template.
So a user, in this case, Alias won a PayBub 21 sets with Lightning, right?
Alias is this protocol user and Abub is a Lightning user.
Alias can buy PayBub and Alias have a bunch of like six coins in here and you know in the protocol you can have multiple factories you know factory operators and you can have your UTXO, you know, your coins can be distributed among other operators.
So you have 2 of 2 between Alice and X here and in the other factory, your two other coins are 2 of 2 between U and Yai and the other two coins are between U and Z.
And you can sort of do an MPP-style payout.
You join three factory sessions, you have six coins.
You register for T coins each in each factory session.
And the factory operators add HDLCs to their factories and then they forward HDLCs to Bob from there.
So you can do MPP, you can pay Lightning invoice by destroying your coins just like how you create new coins.
And similarly, you can also get paid from mining with HDLC nested ATLCs or page DLC nested ATLCs. So the protocol is as in receiving by design, I mean, it's similar to silent payments.
So if you know, if-out is the factory out point, the funding input, it's a unique ID, and we can come, you know, whenever you want to make a payment the idea is to tweak the recipients you know recipient has a dedicated well-known public key like an Nthop and you tweak that public key with a unique commitment just like what you do in silent payments.
And you first create a shared secret between the sender and the recipient.
And you calculate a payment commitment.
You put FL in this unique random data plus the shared secret plus the senders and the recipient public key.
This also provides proof of payment when the recipient claims this payment as ATLC, you know, this coin.
And you tweet at the recipient public key, we are on a public key with the payment commitment times generator.
And you send this commitment out of band, i.e. We are in Australian, to the recipient.
So the recipient can look up the factory, that particular factory, and you can, okay, I see, okay.
I have coins, payout coins in this factory, and I can, and recipient can claim it, claim these coins from there.
So it prevents address reuse.
Each coin has a unique sort of script pub key, different sort of public keys, co-signer keys, plus it solves the async receiving issue.
So the protocol can have also a penalty design similar to Lightning.
So you might wonder, okay, everything is launching commitments, So if I'm receiving a coin, I need to wait for a confirmation for a settlement.
But we can have a penalty design, but it's like lightning so that we can have an instant settlement assurances in here also.
So, you know, in a factory, the first input, right, the funding input, I mean, it records a new software goal, so XOR or OPCAT, we can constrain the signature first, half, and nonce to a particular field in the script so that if the factory operator double spans the factory, as a user, I can forge the operator's private key and so that I can, as a user, redeem my previously spent coins.
It provides invalidity instant settlement trade-off also here without compromising on a protocol design.
There is another thing.
You know, we thought we thought this sort of penalty design.
When you have a coin, unconfirmed zero-conf coins, You can of course spend them to pay someone, to create new coins for someone.
I mean, you can hand over zero-conf coins because coin is a two of two, and the new coin is also a two of two, and the operator is a cosigner of both coins.
But you can also pay a lightning invoice with a coin if it's zero cough.
Even if it's zero cough, you can spend a coin to pay a lightning invoice because it's a two of two.
You're spending from a two of two coin where the factory operator is a cosigner.
And the factory operator is also a Lightning router.
The same guy is also a router and can forward HTLCs to any recipient.
So you can have an unconfirmed coin and the protocol yet be able to pay a lightning invoice instantly.
So it pretty much sums it up.
Thank you guys for listening.
I'm pretty much sure you guys have a bunch of questions.
Happy to have you shoot it over.
Thank you.
Thank you.
Thank you.
Thank you.
Thank you.
Thank you.
Thank you.
Thank you.
Thank you.
I'm gonna start the question.
Sure.
And I'm gonna break the ice because I'm gonna ask a question that might not make sense to make everyone else feel comfortable, so I'm doing this for you all.
But one thing that, some of this was a little bit over my head, but one thing I'm curious about is, is the nature of the privacy necessary for this to work, or is that something that is an added feature?
That wasn't clear to me.
It's like, I mean, The protocol can perfectly work without coin join.
I thought it's a bit, in fact, and this idea has evolved over time.
The initial design was a lightning sort of channel factory design, and this evolved into a coin join design.
This protocol is totally doable, the idea without the coin join components, but I thought it's a nice addition to have.
I think I missed an important step because it seemed like all the owner has to do, the factory person just has to wait four weeks and then they can just take everyone's money.
And it was starting to make more sense at the end where that was like intended as the penalty, but I must have missed why would they not just set up shop, take the, Didn't you say that the person just waits four weeks and then they become spendable by the owner?
The factory?
Yes.
So, you guys think, how does the penalty mechanism work for like a sender or a sender?
Yeah, the penalty mechanism is for instance settlement assurances, right?
If you want, if you're a vendor, i.e., if you demand instance settlement, I mean, you better use Lightning.
Lightning is great for that use case.
But I mean, if you demand instance settlement for some reason, that's what the penalty mechanism is a nice addition here.
But the protocol works perfectly without it.
I mean, because you can pay line invoices with zero call points.
You have like this four week timeout because in channel factory design IE, yeah, you can open a bunch of channels, bundle together in one, but you at some point have to reveal them, and it pollutes on-chain.
By having a one-directional design, the liquidity of the coins excels at some point, right?
It's like a one directional channel.
So that when all coins in a factory are spent, sort of liquidity is on the factory operator's side, right?
In a four week time frame, assuming all coins are spent in a four week time frame, so that factory operator can sleep his coin, I mean the factory.
When you say spent, you mean within the factory?
Sleeping is on-chain, sleeping involves an on-chain mechanism.
What do you mean spend?
Just normal spend?
Like spending in the protocol, they are on-chain.
Are they off-chain coins?
They are too.
It's off-chain.
Spending coins, they're entirely off-chain.
The only on-chain footprint is the factory.
You have this factory, if you have one or more inputs, and like four or three outputs in every five seconds, and when you spend a coin, and you create new coins, so you spend coins from the previous factory, and that spending is off-chain.
It doesn't have- Why is that big off-chain coin join?
I guess I don't- Yeah, it's an off-chain coin join.
If I may, I think what you're asking is how do you prevent your coins from getting sweeped in the factory?
I believe the answer is you have to keep moving.
You've got to keep jumping from one factory to the next.
If your coins are about to expire, right, you send coins back to your cell phone.
Yeah, but what if someone just says they didn't get my message or whatever?
Oh yeah, it's atomic.
So I'm DMing you a message, right?
I send you a coin if you don't get the message after two weeks I get a timeout refund I mean then I'm able to as a sender I can redeem the coins I've sent You put The whole thing you pull on to layer one?
The whole thing is on off-chain.
The closures are on the chain.
I mean, the closures, you have the ability.
You know, here, the first two weeks, the recipient can only add an ATLC.
In the last two weeks, the center gets its, you know, I've been saying this all, I've been saying this for 15 days and nothing's happening.
I just want to get my money back out of this factory.
I want to go to a different factory.
No, no, no, the same factory.
Because the TILF, you know, has unchanged.
You're still on the same client.
How many people do you think would be in each factory?
A thousand.
I mean, if it's an update, template, update, verify design, it's millions.
Yeah, but don't you think, like, I thought the factory design was really flawed in that if any single person in the factory stops responding, the whole thing has to be drawn.
Yeah, exactly Disaster scenario.
Yeah, I mean, it's crazy that more than like 20 right that would be like already pushing yeah yeah I mean the disaster scenario also goes for a lightning if someone you know miners broadcast all states I mean it's a disastrous scenario I get it but you easily join the factory with like zero coins or like five dollars and then what it would take to bring the factory on chain.
So a factory transaction is like 20, 40 times the size of a normal transaction.
Yeah.
So ideally, in the end, we should have a top-level update verifier designed for the coins, so that you're only redeeming the coins you're interested in.
But yeah, I mean the coin is below dust, like one satin, worthless coin.
In theory you can claim it, but economically it doesn't make sense.
But what the protocol does is it sets the incentives right so that the factory operator doesn't cheat.
I think that also goes for Lightning.
But you have the ability to claim that one Satoshi, although it's not economically...
But I was just trying to make sure that I understand, because I think I don't understand it, right?
So it's like a bunch of off-chain coin joins, and then on layer one you spend in, you join the factory.
So you have coins, right?
I mean, you're assuming you have coins, but I mean the first place...
I said that I have Bitcoin on layer one.
Okay, so the first step, how do you onboard to the protocol, right?
You have one machine, you take so on Bitcoin chain and you want to onboard.
You were using, it could be, you know, you can withdraw from Bitfinex or something, an exchange that supports the protocol, right?
So that the exchange has points already in the protocol.
You can get paid from it, but if you have Bitcoin.
Because someone already onboarded to Layer 2.
Yeah, you onboarded to Layer 2.
You have a Bitcoin on chain.
But the first person opens the channel.
There are no channels here.
Maybe the factory is there.
No, like They have a wallet.
I tell you, hey, do you know what is Bitcoin?
You say no.
Okay, you go to the wallet, I go to the wallet and I send you some stocks.
That means I have to marry Satoshi.
That's the first step.
Like, you could fool and try to orange peel kids, but I think doing that is really hard.
Like, I think this is what he's saying, is no nodes, no channels, it's just wallets.
Right, okay.
I'll count on that as what you're saying.
You said?
All right.
Yeah, so if anyone has one, that's the question.
The first, if Biffin X is already onboarded into the factory, like they already have the coins.
Yeah, we have to call them some days.
We call them a Barack coin They're the next has these layer two coins I can get them I can get them and I send my public keys Yeah and then I have a wall that supports this.
When they refresh it every five seconds, they refresh it into something where it swaps out the, there's a new Merkle root or whatever that has, instead of something that never contained my key, it's now something that contains my key.
So now I'm on-boarded into this scheme.
So the flow is like you have Bitfinex, and Bitfinex assuming has already collected a protocol, and you want to withdraw from Bitfinex to your business protocol wallet.
You have like a dedicated public key.
You paste the public key to Bitfinex interface and they make you a payout.
And Bitfinex offers coins, two of the coins between the factory operator and Bitfinex joins the factory operator next session and creates new coins, spends his coins and creates new coins for you, the payout coins for you.
And you're a cosigner on this, you know, you're a cosigner of your coins, but you can do a refund.
It has a script that refund closure.
If you get a coin, yes, under a new factory, Bitfinex can prove it.
It's a launching commitment.
Can prove it to you.
Okay, I paid you.
You have a new coin, you have a bunch of coins under a new factory, or Bitfinex can also DM you, okay?
And- Bitfinex also, every block rolling over, like an output or something?
It must be because my public key is making it into something.
So when Bitfinex joins, I mean, if they're payout, constant payouts into Bitfinex, Bitfinex joins the factory session in every five seconds, yes.
Yeah, but isn't there something that's at least 32 bytes long on layer one, has to change when I onboard, right?
So, are you asking about the first onboarding step?
Like...
Yeah, I have on-chain layer one Bitcoin now joined.
And how do you join, how do you have a coin?
Okay, so the first initial onboarding protocol step.
So you have a layer one UTXO, and you have hardware bullet, and you want to convert that Bitcoin into the protocol coins.
So you deposit your single set, you have created a type of coins and you deposit into a two of two, on a chain of Bitcoin you take so, two of two, just like coins, but coins are...
Yeah, a channel.
It doesn't have to be, it could just be...
It's like a channel, yeah, like a channel, but one time use only channel.
Two of two, and from there, you can even pay away any money.
So if it's a real channel, or you can, because you can get paid from a HDLC Nested coin in the protocol, or you can, you know, coins are off-chain but you created an on-chain coin, right, 12 tokens, and you can join a coin join with that on-chain coin.
You can register that coin, on-chain coin, for the next coin join session, the fact check session.
Did you want to answer?
Go for it.
Yeah.
So I just wanted to like really quickly recap it in my mind to make sure I understand it and then ask my question.
So the factory is putting money into this transaction to create coins.
And then if I have money, I want to buy into this contract and we're going to have some secret that we share out of band where I can control where you spend those coins.
So you're using the connectors to do it in an atomic way?
Yeah, you use connectors in an atomic way, someone pays you and in factory you're not aware of it.
I mean the factory is there, whether it's confirmed or not, factory is there, you're in the way, but you realize, okay, I have a DM, okay, someone says, okay, I paid you, in this factory, go check it out, and you go check it out, okay, real, I know the factory content, because he sent me, the center sent me the factory content and the factory ID, the transaction ID, and go check it out, okay, there is a factory, there are coins, you know, you'll do the, you know, you verify the content and all that, and okay, I see there are a bunch of coins, and then with each coin, I mean, the sender can tell you the index, you know, in what index your coins are in the factory, and then you check it out, okay, calculate the script tab key, okay, and my cosigner key is this, with this tweak at, and the cosigner key is null, publicly null, the LSB, I mean the factor of it is publicly null, you calculate the tap script, and okay, this is coin, this is the script pubkey, this coin is mine.
Okay, so are the connectors also their own outputs as well?
Connectors are also transaction outputs.
Yes, just like coins.
They're commitments.
Yes, just like coins The difference is connectors are not told to their single thing and they carry dust value Okay, I sort of understood that.
One thing that you brought up that I didn't understand is the XOR operation, as a penalty.
Yeah.
Can you explain that a little bit?
That's the right of way.
Sure.
So you're receiving a coin.
You have this coin, i.e. Coin number one.
Let's say it carries 1,000 sets.
You have this coin.
The factory is not confirmed.
It's in the memory.
But you demand its own settlement.
What happens is the factory, you can accept it as Zeroconf as it is.
You can say, okay, I consider this payment, payout, instant, settled.
Although it's not confirmed because the factory operator is to double spend this, you know, this factory transaction, you forge the factory operators private key.
And if you have, you know, previously spent coins in the protocol, you know, you have coins in the past, you spent them already, but because you can forge the factory operators with 202, the private key, you can forge with 202, and you can claim your previously spent points.
Okay, so because you've already done business, and so, Are you using data from an existing transaction and this new transaction to try and forge the factory operators?
If you've already on board, assuming you already have, just like Lightning, when you're on board, but if you have previous points and you already spent, then you can penalize your partner from there.
But it also sets the incentives right.
But other than that, you can pay Lightning invoice.
If you just got on board, you cannot have instant settlement, yes, because you don't have any previously spent point.
What you can do is you can still consider it an instance because, I don't know, you can pay a Lightning invoice for it.
And Lightning invoice involves an instance settlement by nature.
Do you run into issues with fees for the transaction clearing?
So this is a liquidity network just like Lightning.
So they're launching fees, but I mean, it's a factory commitment.
So, you know, this is like 250 bytes, like one transaction, right?
It's a launching transaction and they'll like say, 1,000 participants and the fees are divided by that number of participants, that's like 25,000 subs, divided by that number of participants, there was plus liquidity fees.
It's lightning and there's all liquidity networks.
In fact, this liquidity is used less efficiently here.
Thank you.
Sure.
All right, Cool.
Can I ask one question?
So, in this diagram, like, the stuff on the left is confirmed.
So you can see three outputs, and then that coin's output is sort of an Opsy TV kind of thing that you can expand out to 100.
And so when everyone's using this, they see, okay, my share is coming out of that.
Okay, so then there's this four week delay.
Let's say there's a scenario where everyone's aware, like okay, this operator, this factory guy, he's offline, he's dead.
So we know, why wait four weeks?
We need to close.
What is the process that any let's say that large and there is a hundred is it the case that any of the?
100 can then close at the current state or do you need?
Like what is the process?
Oh, yeah sure so So you're doing coins, but that's not enough to claim.
So from each real coin, you also have to do a claim, a sort of closure, from each coin, and then you wait for 24 hours to then finally settle, just like an auto.
Okay, and so that, is that a multi-stage fan art, or is that like, okay, you spend coins, you get like 100 different outputs, and then each one of those, people have to sweep on their own or?
Yeah So I mean this is a bit of a less slightly less efficient design because if you want to claim just one one coin You have to reveal all coins That's what update you know tablet update verify solves or CTV.
You can you can you can emulate it with CTV, but Ideally with TX hash we can emulate it perfectly But in the current design you have to reveal all the coins to spend, to redeem your own or your owns, and from there you do another spend from the coin and wait and then you redeem it.
You just feed your funds.
Yeah, so the trade-off is sort of, if you think it's unlikely, well, yeah.
And yeah, so there's trade-offs of like, okay, if you make it a tree, then worst case is worse, but if it's all at once, then you have this sort of frivolous problem where there's too many people, one person posts it and then it sort of ruins it for everyone.
Yeah.
Yeah so it was, okay got it.
Cool.
Sure.
Sure.
I have a question about you know, you said before that I need to connect as a receiver, right?
I need to connect to a factory, right?
You don't have to connect.
You don't know who the factory is.
You just got an orange pill and you don't know who, you just download a wallet.
I mean, you know what a factory is, because it's like a factory wallet, a wallet operated by a factory.
And I send you a coin.
I could send you a coin from a different factory, too.
Like, it can be two different wallets.
I use factory ABC, use factory XIZ, but it's an interoperable design, right?
I can send you coins, but the coins I'm sending you is 12-2 between, you know, say I'm using factory XIZ.
You have to make some coins with ABC.
I'm sending you coins and the coins are between you and XSS, my factory.
Your vault is compatible with other factories too, so you can recognize your coins with other factories.
So actually my question was like okay, basically when you DM me, hey, go look it up, you have a payment coming to you, I will recognize the pubkey the well-known pubkey or factory that way so I know where to look it up.
Yeah exactly In the DM I also tell you who the factory is, how it is.
So this factory transaction, is it sitting on chain or in the mempool?
Is it confirmed?
Some of them are confirmed, the new ones are in the mempool.
Okay, so if they're sitting in the mempool, you can push things out of the mempool.
If the mempool overflows and things like that.
Yeah, fee bumping doesn't work here because if you add a fee, increase the fee, the transaction ID changes, so it breaks the autonomy of the name.
So ideally you should do a CPIP style bumping.
So we should either have another output, spendable by the fact, and we have a change, yeah.
So you can do CPF style bumping that way, without affecting the TXID.
So theoretically I could use this factory transaction, it's sitting in the mempool, I use it to pay somebody, I get the goods, and then I do some shenanigans in the mempool, it gets thrown out of a various mempool and the payment never happens.
Yeah, that's the thing, right?
Factory operator should make sure that, yeah, this is going to be confirmed.
You should have a factory operator because otherwise factory operator is not able to claim coins that he sent.
Yeah, but then the incentive of factory operator, making sure it's confirmed is quite expensive process, especially if people are trying to fix it right now, but under the current rules and the map rule, you can get evicted with people doing weird things.
Sure.
So there has to be a lot of workarounds on that, yeah?
Yeah, yeah.
And making sure that that's discussed.
So the factory, like if I want to use it for payments, I can start using it, I don't know, will not use the six block rules, but something like that.
So this is in many ways like slow.
Yeah, I mean, if you have previously spent coins, it can penalize factory operator that way or you can, I mean I think that Lightning is better suited for vendors who demand instant settlements?
I think like I have this analogy Lightning is UTP, this is CTP, WCP like you you know this protocol is more like users really, user protocol, but Lightning is more like a vendor protocol.
If you're a vendor you know your cash inflows are predictable, You can go acquire some liquidity from someone and you demand instant settlement.
And this is more like you have a user, your cash inflows, you know, it's not predictable and you can use the protocol to straight on board and send and receive coins without liquidity constraints and pay by the invoice.
Okay, so you're making a choice between doing things immediately versus like liquidity use or something like that, if I understand correctly?
That's right.
So, so there are like in Lightning, there is the instantaneous part And here you're choosing not to have the instantaneous part, but to make it cheaper or...
What's the trade-off?
It's all about the liquidity problem.
Okay, yes.
So it's like the...
Okay.
Cool.
Yes, I mean, they're all because of the networks, yeah.
Okay.
And if I have another sec, I have another question.
So, you said that if I have one of the coins and then I try to double spend or something like that, the factory operator gets the money.
Because I said so too, you cannot double spend.
No, so did I hear, I thought that you mentioned… Double spending the factory, the factory operator if double spends the factory.
Oh, If the factory operator tries to double spend...
The factory that he created.
Okay, yeah.
So if I'm trying to move...
Can you give a quick explanation?
I have coins in the factory and now I want to give these coins to somebody.
What happens if it's inside the factory, what happens if it's outside the factory?
So in an on-chain payout, if you're paying someone on chain transaction, you can double spend it.
And then if I deliver you good products or services, yeah, I can get it right.
Here, if I as a vendor, if I have this penalty assurance, I previously spent coins, I can't do my next-term settlement here, if factory operator double spends it.
And of course, as a vendor, I make sure the factory, the coins I'm getting, the factory pays enough fees.
I see the mempool, okay, this is going to be confirmed, I'm sure it's going to be confirmed, and if, you know, at some point it will be confirmed, right?
If there is a double spend in the mempool, well, then I'm penalized as a vendor, the factory operator, so I'll claim my previously spent coins anyway.
So I'm asking, I own coin zero.
Now I want to give you some three Satoshis, which are five Satoshis, what's exactly in coin zero?
How do we do that?
So you have CoinZero in this factory, right?
This is like a confirmed factory, deep in the blockchain.
You want to spend a zero coin and say it holds 100 sets.
And then with that coin, you join a new factory, and you register for that coin.
And because it's a tool too, the factory operator knows, factory operator funded this coin in the first place one time ago and can, you know, authorize this coin whether it's banned, expired, OFAC, whatever.
And you can join a new factory session and register for this coin.
With the same operator?
Huh?
With the same operator?
With the same operator, yeah.
Okay, I cannot do this with a different operator.
Oh, yeah, exactly.
You have to use the same operator, the 12-2 between you and the coin, the factory operator, and you join the same factory operator.
You ask to join his new session, like three minutes ahead, and you join it.
You register it in the registration phase, you register for coin zero, and then you register for the payouts, plus change coins.
Destroy coin zero and create new coins.
I mean, you register for the payout coins, you know, based on the blanket credentials you received from the coin registration part.
And then you, from this coin, it's a TOV2.
From this coin, actually it's not a TOV2, the coin is not a TOV2.
The coin is, this is the scheme, from a coin you have, from the first closure A, A to C, So this is a pre-computed sort of closure.
From C to A, we can use CTV to constrain A to be the transaction output.
And from here, ATLC is a 2 of 2.
And from A, you are a cosigner of A.
The other cosigner of A, this A is the operator.
And you sign a transaction, off-chain transaction, this transaction, ATLC connect, by adding this connector, ATLC connector, UTXO to the second input.
And this UTXO lives in the NIF factory, commits to the NIF factory.
Because you're signing with Ccash all, this transaction ID is the factory's transaction ID, commits to the factory, sort of forms a TX lock.
Hash lock can look like a code TX lock.
So that you sign it, so that you exchange signatures with the operator and okay operator, you know, you know, says okay, I've got a signature.
I'm good to go.
I will release this factory.
If you don't sign, you get banned from that session.
Well, where in all of this are you getting the coin?
I'm trying to, I'm trying to send to you.
Oh, you're sending me?
Yeah, so you added in the Bitcoin registration phase, you added my coin, you did a tweet, you know my public key, Nostra public key, you tweet at the tweet, you send me a DM, then you added that coin, you registered that coin in the session, and then it's now, it commits to the transaction ID of the factory template.
And then it forms a TX block for the template and then the factory operator broadcasts it to mempool.
So I see, okay, I see an unconfirmed incoming factory and I have some coins under that factory.
I see the payment, I see the factory pays enough fees.
I can spend a coin, you hand to me over a Zeroconf coin, right, and I can spend a coin to someone else or pay a lightning invoice with it instantly, and, or I can even, you know, just hold it.
Okay, so it's up to the factory operator to see that I'm not doing it twice.
I'm not paying you and for example If you try to do it twice I mean factory operator won't let you in because the two of two the coin of 80s is a 12 to Oh, yeah, I do a second spent But what if I'm the factory operator?
Like, what's in it for me to lose by allowing this?
For the factory operator?
Yeah.
Because if you do try to do it, you double spend.
If you try to double spend, you get a penalty from anyone.
It's going to be made public to the whole network.
Anyone can forge my private key, in that case, any participants, pre-private participants.
And if not, you can just not demand it as a settlement.
Like you may not be interested in demanding it as a settlement, you can just receive coins and wait for it to convert.
If you don't want to make it, to consider it as settled.
If not, with XOR or CAT, you can do it in penalty mechanism.
Let's take it offline, because I think we're killing everyone.
But yeah.
Sure.
So my understanding is that in each factory, the confirmed factory has coins connectors and the factory output factory chain, yes, so My is the connector basically is that a part of the pinning mechanism that I'm able as a person who has a coin, like so I submit an on-chain UTXO to a vector operator, I receive a coin, is the connector part of the mechanism, the pinning mechanism, like because basically in the connector, if we have the data, I would need to be able to, like if you try to double spin a vector operator, I can take the data from the previous connector and now get the funds back to myself?
Is that like what the purpose of the connector is?
Your question is if you're sending an on-chain UTXO, right?
To pay someone?
So I'm already in a confirmed factory, I'm in a confirmed factory.
In a confirmed, okay, you're coins in a confirmed factory.
I have coins in a confirmed factory.
Is the connector a part of the pivot mechanism if the factory operator tries to double spin?
Is that the purpose of the connector?
The connector is to commit to the transaction ID, so that if there is a double spin, it breaks your coin.
The operator can no longer redeem your coin, Because the connector is part of the factory, it commits to the transaction ID of the factory, so that if the factory already double spends...
So the connector is the operative part of the bidding mechanism.
Without the connector, as somebody that has a coin in the factory I would be able to spend to spin I wouldn't be able to penalize the operator not penalize you know what penalizing is a different sort of mechanism you won't be able to factory It's for factory operator to have an assurance, because factory operator pays someone with his liquidity and should be able to claim your coins.
And in order for a factory operator to claim your coins, factory operator needs that assurance that connects to the connector.
Shall we continue with the rest?
Give it a round of applause.
