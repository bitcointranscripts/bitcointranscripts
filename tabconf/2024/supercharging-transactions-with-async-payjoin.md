---
title: 'Supercharging Transactions with Async Payjoin'
speakers:
  - Brandon Lucas
tags:
  - payjoin
  - coinjoin
  - psbt
  - payment-batching
  - coin-selection
source_file: https://youtu.be/vPzvLxv0YfQ?si=yNhZFY9VTZkdBGuu
media: https://youtu.be/vPzvLxv0YfQ?si=yNhZFY9VTZkdBGuu
categories:
  - Privacy Enhancements
  - Fee Management
date: '2024-12-22'
transcript_by: 0tuedon via tstbtc v1.0.0 --needs-review
summary: >
  Brandon Lucas (frontend engineer at Voltage and open-source Payjoin
  contributor) delivers a beginner-friendly introduction to Payjoin and its v2
  async upgrade. The talk opens with a critique of the common-input-ownership
  heuristic (CIOH) first noted by Satoshi, which Greg Maxwell later showed to
  be a false assumption \u2014 multiple parties can co-author a single transaction,
  the insight that spawned CoinJoin. Lucas traces the lineage from CoinJoin
  through Payjoin (BIP-78), explaining why CoinJoin's equal-output fingerprint,
  coordinator fees, and need for repeat usage are practical drawbacks, while
  Payjoin addresses these by making collaborative transactions indistinguishable
  from ordinary ones. He reframes Payjoin not merely as a privacy tool but as a
  peer-to-peer batch transaction protocol: a sender and receiver co-authoring
  the most efficient transaction possible using PSBTs and BIP-21 payment URIs.
  The core limitation of BIP-78 \u2014 the receiver must run an always-online
  TLS/Tor server \u2014 is what Draft BIP-77 (Async Payjoin) solves by delegating
  coordination to an untrusted lightweight directory. End-to-end encryption via
  HPKE prevents the directory from reading PSBT payloads, and Oblivious HTTP
  hides sender and receiver IP addresses from the directory operator. The talk
  then highlights two under-appreciated capabilities: transaction cut-through
  (redirecting incoming outputs to satisfy a pending outgoing payment, saving
  an entire on-chain transaction) and receiver-side batching (exchanges
  incorporating depositor inputs into withdrawal transactions to reduce chain
  footprint). A live demo with payjoin-cli illustrates the full async flow.
  The Q&A covers directory operator incentives, the unnecessary-input heuristic
  and waxwing's analysis work, multi-party Payjoin as a future direction, and
  why Oblivious HTTP polling is preferred over WebSockets for metadata
  protection and BIP-78 backwards compatibility.
---

Speaker 0: 00:00:05

Okay, thank you everybody.
So my name is Brandon Lucas.
I'm here to talk about how you can supercharge transactions with asynchronous pay join.
So just a little bit about me.
I am a front-end developer at Voltage.
I spend my days centering divs and coloring buttons at Voltage, And when I'm not doing that for my full-time job, I spend my days centering divs and coloring buttons for FOSS projects, mainly PageJoin.
So I worked on the pagejoin.org website.
And yeah, that's me.
So just to give a little bit of an outline about what we're going to go over, I want to start by talking about some false assumptions made about the way transactions in Bitcoin work very early on in Bitcoin that kind of set the course for the way wallet software worked.
Then we're going to talk a bit about the history that led to the creation of PageJoin, some recent improvements that the PageJoin team has been working on, and finally the fun stuff, use cases and some novel use cases that PageJoin implements that may be new to a lot of you.
And finally, the call to action, the call of duty.
We need help, and so we'll talk about some ways that if you're excited about pay join, which you should be, you can help the project.
Right in the white paper itself, in the privacy section, Satoshi says the following, as an additional firewall, a new key pair should be used for each transaction to keep them from being linked to a common owner.
So that first sentence, that's common, that's most wallet software does that today.
He goes on to say, some linking, and he's talking about pub keys with identities, is still unavoidable with multi-input transactions which necessarily reveal that their inputs were owned by the same owner.
The risk is that if the owner of a key is revealed, linking could reveal other transactions that belonged to the same owner.
So, Greg Maxwell, a couple years later, made a post to Bitcoin Talk where he actually makes a different claim.
So he says here, a lot of People mistakenly assume that when a transaction spends from multiple addresses, all those addresses are owned by the same party.
This is commonly the case, but it doesn't have to be so.
People can cooperate to author a transaction in a secure and trustless manner.
We can make it a lot easier for people making this mistake, this assumption, to discover their folly by making there be a single address that seems linked to everything.
And so he doesn't say it outright in this post, but he basically discovered coin join.
Later, he goes on to formalize this in another post and actually creates and coins it, CoinJoin, right?
But essentially, what the idea is, is that you do not have to have all of the inputs in a transaction from the same person, right?
You can actually have multiple parties create a transaction together.
And so the original purpose of this was for privacy, right?
So what does this mean?
This means that the white paper has a mistake, right?
That clause which necessarily revealed that their inputs were owned by the same owner, that's not true.
That is an assumption and despite the fact that that's the way most wallets work today, that is just not true.
So just to recap real quick, Satoshi assumed all transactions must belong to the same owner.
This isn't true, and that discovery led to the creation of CoinJoin.
So before we can go further and dive into how CoinJoin works and how PageJoin works, we have to understand how at a high level transactions work, right?
So very simply there are inputs and outputs to every transaction.
Coins that are consumed in a transaction are referred to as inputs, coins that are spent from a transaction are referred to as outputs, okay?
So that's like the very basic way to think about it.
So you can see here, let's say Alice has a set of UTXOs, maybe people paid to her in the past.
And so these are unspent transaction outputs that she has not used as inputs to any other transaction.
And they're associated, as you can see here, with what we're used to seeing in Bitcoin is the addresses, right?
Each output is associated with an address.
So Alice might need to pay one Bitcoin to Bob using three of these UTXOs, let's say.
So her wallet software will select some of the UTXOs that she has that add up to what she needs to be able to pay Bob, right?
In this case one Bitcoin, So it'll take the 0.3, the 0.5, and the 0.2, since she didn't have any single inputs that were greater than or equal to 1 Bitcoin.
So it selects multiple inputs and sends those to Bob.
This is the typical transaction, right?
This is the structure of a typical transaction.
They all generally take the form of having all the inputs come from a common owner, from the sender, right?
This has led to a heuristic that blockchain analysis companies can use to pretty trivially track users.
So despite the fact that we don't use best practices in wallets now or don't reuse addresses, we all know that, that's pretty common information.
This common input ownership problem though is still very much alive.
Greg Maxwell in his discovery of coin join, let's say, realized this.
So what this implicates is that people who are trying to spy on you now have a very easy way to do so, right?
A very trivial way to do so.
So again, CoinJoin is a transaction in which multiple parties, let's say in this case Alice, Bob, and Carol, are collaborating or cooperating to contribute their inputs to a transaction such that the link of their UTXOs, their identities, become obfuscated.
So As you can see here, one thing to note is the evenly split outputs, so they're all 0.1s, they all come out to be the same value.
The reason that happens is because if you had, it would make sense if Bob had 0.3 and then sent himself back 0.3 out the other side, that would be trivial identifiable, so you need to create these equal-sized UTXOs for each person to maintain their privacy.
So there's, this is great, This was a great discovery for Bitcoin.
This means that no changes are required to Bitcoin, right?
So this kind of skirts the debate.
This is something people can do right now.
This is something people could have done from the very first version of Bitcoin.
Coordinators came along after a while to ease the use of finding a market, essentially, of people that want to CoinJoin.
Finding those people can be difficult on your own, so coordinators sort of provide a service that does that for you, and they take a little fee to do that.
And as a result, CoinJoin kind of becomes the de facto recommendation for people to achieve privacy on Bitcoin.
But it's not all great, right?
There's some bad things about CoinJoin.
One of the problems is that you have high on-chain fees.
That's because these are very large transactions, right?
So a lot of people are contributing inputs, a lot of people, a lot of outputs are created, and they have to be created in this kind of special way where they're all evenly split.
So maybe you're creating more outputs than you really need so that you preserve privacy.
Coordinators take a cut for providing the service and most people who do coin joins use the services.
And finally, they must be performed regularly.
Right?
So if you just do one CoinJoin, okay great, you kind of broke the chain tracking you, but you're kind of just resetting the time, right?
You're kind of just resetting things.
So like In the future, people can still associate your transactions unless you keep kind of doing this process.
So yeah, coin joins need to be performed regularly.
And then the ugly, right?
We have, this is a highly interactive process, which offends my front end sensibilities, but this means that people essentially have to go out of their way to do a coin join, right?
And if we really want people to have privacy on Bitcoin.
We really need to make it something that people can do by default.
Not to mention that they're spending extra time, extra money, just to do these transactions for the single purpose of preserving privacy.
So there's all these extra steps people have to take, and the reality of it is that most people don't take those steps, right?
So coin joins also leave a fingerprint.
Because this is an overt method of trying to preserve your privacy, it has a very identifiable, distinguishable pattern on the blockchain.
So the multiple outputs of equal size, that's pretty identifiable as a coin join.
And in fact, if you go to mempool.space, there's actually a little tool, the mempool goggles, where you can see transactions that follow that type of pattern.
And you can see here in this picture that those are highlighted.
If you were to dig into those, you'd see those equal size outputs in the transaction.
And then just a note on the fact that trusted third parties are commonly used to do this.
And a lot of them have disappeared from the US recently.
So as I'm sure many of you know, the Samurai developers who were a popular coordinator that provided this CoinJoin service, the Samurai developers were arrested a few months ago.
As a result of the regulatory uncertainty, Wasabi, another popular CoinJoin coordinator, fled the US.
And then JoinMarket, which is not a company.
It's a software that sort of tries to help create that market.
It's like a decentralized way to create that CoinJoin market.
That's kind of the last remaining option people have, and I believe it was like the least popular because it was more involved.
So trusted third parties are a problem here.
So recap, common input ownership heuristic is used to track people.
Coinjoin enables multiple parties to construct transactions which contribute all their inputs by which they gain privacy.
And KoiJoin has financial and user interface barriers which lead to low usage.
So enter PageJoin, right?
So PageJoin was created in this environment of trying to figure out how to solve this problem or how to at least provide an alternative solution with a different set of trade-offs.
So, what I will call the legacy definition here of payjoin is, and this is directly in BIP78, which is version one of payjoin.
This document proposes a protocol for two parties to negotiate a CoinJoin transaction during a payment between them.
So essentially, it's still being thought of as in terms of coin join, right, in terms of the privacy narrative.
But as you'll see there's a lot more ways that you can think about pay join.
And so I'm kind of poking fun at this idea that PageJoin is merely a privacy protocol, right?
And you can see that this is pretty well ensconced in how we think about PageJoin as a community.
We think about it as kind of an alternative to CoinJoin or something with a different set of trade-offs, when really I want to propose to everyone that that is really narrowing the scope of what PageJoin is and can be.
So like imagine if I said about the Lightning Network that you asked me to define Lightning Network and I say, oh well Lightning is a scalability improvement for Bitcoin.
Okay, yeah that's part of it.
Is that all it is?
No. It's a way to do micro payments, right, because we took transactions off chain.
It's a way to make transactions near instantaneous, right.
There's a lot of benefits to using lightning that go beyond the scope of scalability.
So saying that doesn't really do it justice.
In the same way, I want us to put pay join in that light.
So how about this?
How about we say pay join is a protocol for coordinating peer-to-peer batch transactions?
Because that's really what it is.
It's a sender and a receiver cooperating to form the ideal transaction, right?
A transaction that would best work for whatever situation they're in.
So how does BIF-78 work?
Well, at a high level, a receiver adds their UTXOs to the sender's transaction.
So this is the two-party coin join part, right?
Because there's just two people, that's how to break the common input ownership heuristic.
You just have a receiver add one of their inputs or multiple of their inputs into the transaction.
One of the problems with BIP78 is that a receiver had to run an always online secured server because they didn't know when a sender would try to make a payment to them.
You can't anticipate that ahead of time.
Let's say if you're a business running BTC Pay Server or something like that, you want to be able to accept payments at any time.
So version one of PayJoin was synchronous.
BIP78 used a few primitives, or a few BIPs, already present in Bitcoin.
One is BIP21, the Bitcoin URI.
So you can see right here in the PJ equals there, we have the Bitcoin URI, which has the address, and then we have PJ equals, which specifies the payjoin endpoint, the receiver's payjoin endpoint, that the sender, well basically it communicates to the sender where they should send the transactions to, right?
And it also makes use of partially signed Bitcoin transactions or PSBTs to allow the receiver to modify the transaction that the sender proposes to them.
So to go over the sequence diagram of how it works, the receiver starts by sending out of band this BIP21 string with the address and the pay join endpoint to pay to.
The sender takes that, constructs what's called the original PSBT, which is just a normal transaction.
It's just a transaction with all of the sender's inputs as essentially, yeah, all of the sender's inputs into the transaction.
So it's just a normal transaction, nothing special about that.
The sender sends that over, the receiver takes that, adds their inputs, sends that back to the sender.
This is the pay join proposal.
And the sender checks to make sure that everything is okay with the transaction, that the receiver isn't trying to do any funny business by increasing the amount that the sender pays to them or something.
If everything is okay, then the sender will finalize that PSPT and broadcast it to the network.
So there are some drawbacks to this.
The receiver is required to run a server, as we mentioned earlier.
That led to a lot of wallets not wanting to implement pay join.
That's just a technical difficulty, right?
It also led to transactions being synchronous, right?
So that's why the receiver needs to run the server, is because both parties need to be online at the same time.
So as a result, PageOin hasn't seen very much adoption so far.
And there's actually a really good message sent to the Bitcoin developer mailing list by Craig Raw, who is the lead developer behind Sparrow Wallet, which is a great wallet.
It uses a lot of best practices, I would say, for creating Bitcoin transactions.
And so he puts it perfectly.
He says, I think one of the barriers to greater payjoin adoption is the need for a server endpoint on the receiver side.
Ideally, all wallets should be able to conduct payjoin transactions with each other.
This would require a different mechanism to exchange the PSBTs, but otherwise, the specification should need no amendment.
So what if that was the truth?
What if we did that?
What if we could be unburdened by what has been?
So Dan Gould, a developer who is working on PageJoin, proposed a draft BIP called PageJoin version two, asynchronous PageJoin, this is draft BIP 77, it's still under review, and it aims to solve this problem.
So what is async-pay-join?
Basically, at the highest level, it outsources that pain point for the receiver to be required to have a server.
It outsources that to an untrusted pay join directory server, okay?
And the reason that pay join directory can be untrusted is that hybrid, something called hybrid public key encryption provides end-to-end encryption for the PSBTs. So the page-join directory can't actually see the payload, the PSBT payloads that are being sent across to the page join directory.
And it also uses oblivious HTTP, which is, you can think of sort of as Tor Lite, to hide the IP address of the sender and the receiver from the page join directory.
So just to kind of show you how, like what what does this directory look like?
It's stupid simple, very dumb, very, you know, there's not much to it.
All it is is a list of subdirectories.
The subdirectories are public keys that have been base64 encoded.
These are not public keys that have anything to do with Bitcoin, right?
We don't want anything that is going to lead back to anything related to a wallet.
So these are just plain old public keys, and these public keys are used as identifiers for the sender to know where the receiver wants them to do the pay join.
And you can see inside of one of these subdirectories, all it is is like a buffer, like a placeholder to hold the encrypted PSBT blob while the pay join communication protocol is happening.
And so to look at how the sequence diagram changes for this, It doesn't change as much as it looks like here, right?
We have all the familiar old things from BIP-78, where the receiver starts by sending out of band their BIP-21 to the sender.
But there's a key change in this first step, where you see, instead of sending their address and that the pay join server endpoint, that the sender needs to basically know which server the receiver is running, now they send the sub directory.
Right, So now they say which sub directory on the pay join directory is shared, or is going to be used for this pay join transaction.
So they send that to the sender.
In the meantime, the receiver starts polling.
So the receiver does long polling get requests waiting for the original PSBT to be put in the mailbox, so to speak.
The sender, The sender, once it gets the BIP21, constructs the original PSBT, same as before, but instead of sending it to a receiver server, sends it to the page join directory.
When the receiver detects, via polling, that the PSBT is in the mailbox, it grabs it out, modifies it to include his own inputs, encrypts it, posts it back to the directory.
The sender, in the meantime, has also been polling, right?
Waiting for this to happen.
And once the PSBT makes it to, makes it to the directory, and the sender polling detects that it's present.
The sender grabs it, decrypts it, checks that everything's okay just like before, and then broadcasts the payjoin transaction.
So really the only thing that's added here is the payjoin directory, the untrusted third party, and these polling get requests for each side.
So now they can go offline in between steps And when they come back online, they can check if the PSBT, or the next PSBT in the step, has been created and communicated.
So, Immediately, PayJoin has some improvements over CoinJoin.
There's no extra transaction required, right?
So you don't need, basically with CoinJoin, you basically have to go out of your way to construct a transaction just to receive privacy.
There's no coordinator or extra fees.
This is completely peer-to-peer between sender and receiver.
And there is no or little interaction required.
So what we're aiming for, especially from a UX perspective, would be privacy by default, right, because that's the only way we're gonna get people to achieve it.
But there is more than just these improvements over CoinJoin.
There's actually new things that we can do with Payjoins, right.
So one that I want to talk to you about is transaction cut through.
And this was actually the idea that got me into pay join.
And then batching.
So what is transaction cut through?
This is actually another idea by Greg Maxwell.
So I kind of want to just like troll the early Bitcoin talk sometimes to see like what are ideas people have that no one's using, right?
But transaction cutthrough is basically, imagine you have a transaction where Alice pays Bob, Bob knows he needs to pay Carol.
So normally what happens is Alice will pay Bob, Bob will say, OK, I received the payment, now I can pay Carol later, whatever.
But if he knows in advance that he needs to pay Carol, And by the way, I couldn't think of any famous carols that are like relevant to my generation, so sorry if there is one and I just missed it.
That's why carol is just a circle.
But if he knows he needs to do this in advance, and the UTXO that Alice is sending him is enough to cover the transaction he needs to send later, why wouldn't he just send it now?
Why wouldn't he just say to Alice, hey, can we modify this transaction a little bit and redirect this output to another purpose.
Alice doesn't care.
Maybe for the privilege of doing that, Bob can offer to pay a little bit of the fee, whatever.
But now, Bob has just turned two transactions into one, And one for which he probably doesn't have to pay the fee.
So this is the transaction cut through idea.
It's the idea that if you have multiple transaction intents, if you have multiple transactions you know you need to make, it's possible to redirect the outputs of incoming transactions to serve those purposes instead of creating whole new transactions.
So what's one use case of this?
Well, lightning.
Faster, cheaper lightning channels.
So the typical way lightning nodes are created and funded is, let's say Alice has a stash and she wants to create a lightning node, it's a brand new node.
So First she'll go into Thunder Hub or whatever and send a funding transaction to the wallet, the Lightning Nodes wallet, and then using that she can create a channel with Bob, or a channel with whoever, however many channels she wants, right?
But with this transaction cut-through idea, why can't she just do this?
Why can't, she knows in advance where the outputs are gonna go, why can't she just send them there directly, right?
So if the Lightning server is page one enabled and her wallet is page one enabled, this is a possibility.
It actually gets better than this because you can combine it with batching.
That's actually been done as a proof of concept via the no looking project.
So this is the result of a hackathon project a couple years ago.
It's a proof of concept so please do not use this in production, but basically what it proved is that you could fund and open multiple lightning channels in one payment.
And the UI for this was really cool.
Like you could just, if you knew the public keys of the nodes that you wanted to pay to in advance, you could just queue them up, generate a QR code, scan it, and then it would fund and open all of those at once.
So very cool.
So this is basically combining the ideas of batching, cut through, and the ability to break the common input ownership heuristic to achieve privacy.
What else can we do?
What about exchanges?
How might this impact exchanges?
So let's say we're a very stupid exchange, and people are constantly withdrawing transactions from us, or sorry, requesting withdrawals from us, well, we might naively just send them their money right away, right, and we might just create a transaction for every request.
That's obviously very wasteful, so one way to improve over that is to do batching.
So in this case, let's say the exchange has, you know, a four Bitcoin UTXO and Alice, Bob, and Carol want to withdraw from the exchange, well, the exchange is probably going to say, OK, sorry, you have to wait for an hour or so because we're gonna create a queue of other people who want to do a transaction so that we don't waste a bunch of money on fees, right?
And then they'll send one transaction with all of those UTXOs on the hour or something like that.
So that's definitely a lot smarter.
That saves a lot of money.
So that would be sender side batching.
With PageOin we could do even better.
We could do receiver side batching.
So this opens up a whole new avenue for batching.
So let's say in this example Alice, Bob, and Carol are still there, they still want to withdraw.
But let's say Aaron wants to withdraw two Bitcoin, right?
Well they just have that four Bitcoin UTXO, maybe they'd have to include another one of their UTXOs or maybe they'd include another transaction later.
Well any exchange isn't just having people withdraw from it, it also has people depositing to it at any given time.
Why not make use of those to fund the withdrawal outputs?
So here you have, let's say Dave, inputting or depositing three Bitcoin.
The exchange can just say to Dave, like, hey, why don't you just use this as an input to this withdrawal transaction, right?
That way, that's one less transaction on the receiving side, on the depositor side, and maybe the exchange can do something fun like let Dave, you know, I don't know, pay a part of his fee or something if it's sufficiently helpful to the exchange.
So yeah, the idea here is that pay join opens up one side of the equation that was previously closed, just because now the sender and receiver can negotiate what to do in this transaction.
And then I just want to point out that there's a lot more use cases here.
These are just two that we thought of.
But really, at a high level, a protocol that utilizes transactions more effectively makes anything downstream of that better, right?
Lightning, eCash, whatever.
And, pay join helps people even if you aren't pay joining.
This is one key way that it's distinct from coin join.
In a coin join, it's identifiable as a coin join, so you can kind of just take that and say, okay, you know, these guys are doing their own thing, and maybe we can try to track the people that are doing coin joins.
You kind of out yourself as a coin joiner, as a person who wants to protect your privacy, ooh, you know.
But when you pay join, it's not obvious who is actually doing the pay joins, right?
Which transactions are pay joins?
Because they look like normal transactions.
Which means that if you're an analysis company, you begin to not be able to trust the validity of your analysis.
Because let's say we can say that, okay, 5% of transactions on the network are probably pay join.
Which five?
How do you track people if you don't know which ones are the ones that you're trying to track properly, right?
So that's one way.
And then another way is just the effective use of cut-through and batching.
We can have more throughput on the chain and lower fees.
So where are we going?
One way that the payjoin protocol could potentially be improved is by having multi-party pay joins.
So right now, you don't gain too much privacy from a single interaction if you just have a sender and receiver.
If you do that over time, that really adds up.
But you also have, if I'm doing a pay join with a receiver, that receiver knows which of the outputs are mine because they're just simply not his.
So with multi-party pay joins, we can solve this problem and have a lot of the benefits of both coin joins and pay joins, right?
And try to remove the negatives of either.
So just to wrap up, put it in a nutshell, PageJoin is a peer-to-peer batching protocol.
There's no changes to Bitcoin required.
Version 1, PageJoin required a receiver to run a server, which limited the potential for adoption.
Version 2 is asynchronous and outsources the server requirement to an untrusted third party, which opens up a lot that wallet developers can, that opens up a lot of use cases for wallet developers and improves the UX and lowers the interactivity of the protocol.
And also, PageOin supercharges transactions via concepts like batching, cut through, and preserve privacy.
We're trying to make transactions more efficient and increase privacy via this peer-to-peer batching protocol.
So if you want to find out more about PageJoin, go to pageoindevkit.org or pageoin.org.
PageOin DevKit is a library written in Rust to facilitate wallet developers integrating PageOin.
And we are trying to create bindings to other languages for this.
So be on the lookout for those.
And then if you want to get like a higher level idea of PageOin, a lot of the stuff that we talked about in this presentation, but in more detail, go to pageoin.org.
And if you are a developer, please contribute.
Please, we need your help.
Bitcoin wants you to help us work on this protocol.
There's a lot of work to be done, so you can read bit 77, give feedback on that, write tutorials, spread the word on Noster or Twitter or whatever, And yeah, that's pretty much all I had.
So we mostly talk on Discord, so feel free to scan the QR code and join the conversation.
We'd love to have you.
And that's it.
Thank you for listening.
So I'll take any questions.

Speaker 1: 00:36:25

So while the directory seems very lightweight in terms of service, What's the motivation for participants to provide that service consistently?

Speaker 0: 00:36:41

Yeah, that's a good question.

Speaker 1: 00:36:43

Part one of the question, so go ahead.

Speaker 0: 00:36:45

Okay.
Yeah, I mean, not much at the moment as far as I understand it, and someone feel free to correct me if I'm wrong, but not much.
The idea is that it's a very, very very, very light weight, Very, very dumb, so not expensive to run.
So the idea is that kind of like a Nostra relay, I guess you could say, there would be a lot of people running these very, very lightweight things and it would be trivial to switch from one to another, right?
And the worst it can really do is kind of deny your payment by going down or something.
But it's not going to, there's no way for it to steal funds or anything like that.
So yeah, so no, At the moment, I don't believe there are any financial incentives or anything like that for people to run it, but I don't see why that couldn't be integrated or iterated on in the future.
Maybe there could be some financial incentive added to that.
So, yeah.

Speaker 1: 00:37:49

I guess as a follow-up to that, it seems to me that just like running your own node gives you a certain amount of privacy, right, in what you're doing, If you're doing that, then you could probably do this as well, not only for yourself, but as a service to the broader community.
If it was, say, plug here, start 9 service that one click and it's running and you can expose it to the Internet such that other people could leverage it, then I guess your own alternative or altruistic motive benefits the community.
So that's pretty then pretty good deal then for you.

Speaker 0: 00:38:33

Right, right, yeah, so and maybe that's just part of the motive, right, is well I just want to run one for myself.

Speaker 2: 00:38:42

Thanks so much for everything.
You gave a great example in the coin join case of the amounts being relevant in and out, specifically the outputs being equal, and I'm curious, I might have missed it but I don't think you provided one for the pay join example, and is that because it doesn't matter?
For example, if Alice is sending Bob one Bitcoin and Bob wants to pay join in one of Bob's UTXOs, does it matter whether it's equal to or less than or greater than that one Bitcoin?

Speaker 0: 00:39:15

Yeah.
So it doesn't matter in the same way that it matters for CoinJoin.
Payjoins are kind of designed to not be easily identifiable.
And this is probably just a mistake on my part that I didn't include that.
But there are examples online, specifically if you look up Waxwing, I believe he's done a lot of work on this.
Waxwang, Waxwing, I guess Waxwing Pageoin, That's important.
Come up to me after and I can try to find where he does this, because this is on Mastodon I think.
He actually plays a game with people where he says, who can figure it out?
He does a page join and he asks people, where are the outputs going?
So he's done a lot of work kind of trying to figure out where the edges of this are.
That is a really good question though because There are heuristics that can identify pay join as a pay join, and they're called the unnecessary input heuristic.
And again, this is waxwing, where, and unfortunately I can't remember them off the top of my head, but there have been papers written about this.
Let's see.
If a transaction is formed in a way such that it contains seemingly unnecessary inputs.
Yeah, that's it.
So if a receiver adds an input to the transaction, well, that probably didn't need to be there, right?
And so if it didn't need to be there and we can identify that, that's a problem.
There's ways around that.
And people have done work to say, okay, like we can make it look like all the transactions, all the inputs are actually needed, or at the very least, confuse chain analysis.
All of that being said, it is way less relevant than for CoinJoin, because CoinJoin is so distinct.
It's always that 0.1, 0.1, 0.1, or whatever that number is.
It's always that, so it's trivially identifiable.
If we do this, we'll save ourselves a lot of time in the future as is.
We'll buy ourselves a lot of time essentially, while we work on eliminating the unnecessary input heuristics, so I think there's two of them that have been identified.
So you can look up, I think his website's Rayify.
Rayify, yeah, so he has a great blog post about, oh no, what, not anymore?
That's weird.
Okay, well he had a great blog post about PageOne where he talks about this, so I'll see if I can find if that's still around, but anyway.
Yeah.

Speaker 3: 00:42:03

Hi, I'm curious on the asynchronous aspect.
You know, if Alice wants to pay Bob and then Bob decides he wants to change the transaction in some way, you know, especially as you involve multi-parties, it sounds like there could be a lot of rounds of communication there.
So how do you avoid the same pitfalls of coin join of needing that central coordinator?

Speaker 0: 00:42:25

Yeah, so I don't know, is the short answer for the multi-party.
Just because that hasn't really been done yet.
This is just kind of like in the iterative idea phase.
As far as the current rounds, they're the current pay join V2.
Where is that diagram?
As far as this is concerned, this is still, this is sort of outsourcing.
So CoinJoin basically tries to create, tries to find a market, right, because of this multi-party thing.
I don't know how that's going to be solved for actual multi-party pay join, but for now, all you're having to do is just two people coordinating over a pay join directory that is trivial to switch between, and trivial to spin up, honestly.
This is so lightweight that you could run this on, you know, just a basic VPS.
So, I don't know if that answers your question super well, but it is, the async aspect of it is already, I would say, a huge interactivity over, improvement over PageWide, because this is something that could be integrated in wallets like right now without the user even really having to know, unless maybe something goes wrong.
Like, for example, if one of the parties is malicious and tries to, let's say the receiver tries to modify the output paying to himself to pay too much to himself, right?
But the idea is that this would all be put into the software, right?
This is all part of the pay join protocol.
These are all checks that would be happening.
They're specified in BIP 78 and BIP 77.
So really the big problem with coin join that you just can't get around, no matter how good your software is, is this market of people problem.
Which sender and receiver pay join at least does not suffer from.

Speaker 4: 00:44:23

Speaking of distribution of page join, have you considered pitching or creating modules for like BTC pay server so that if a business is basically saying, hey, I'm already doing these transactions, let me just turn this on, then every single instance of BTC Pay Server might be able to interact with this and have maximally efficient transactions.
Any thoughts about this?

Speaker 0: 00:44:52

Yeah, that would be awesome.

Speaker 4: 00:44:53

All right, let's do it.

Speaker 0: 00:44:54

Yeah, that's the goal.
But we need help.
We need more developers, basically, helping and working on this.
So yeah, if you're interested, man, please.
Like, that is the bottleneck really, is wallet developers integrating this, right?
By the way, BTC Pay Server already does this.
They're, like, Nicolas Dorier is the guy who wrote BIP78, so I believe they might have been the first to integrate PageOin.
I might be wrong about that, but PageOin version one is actually enabled in BTC pay server, both sending and receiving.
So hopefully they would be open to it.
But yeah, and that is also kind of why we're doing these, we're focusing on these bindings to other languages, because right now, it's written in Rust, which is great, but to expand the number of wallets that can actually integrate this, we need to create these bindings.
And so that's one way that, if you're a developer, you can really support the project, is by helping us work on these bindings.
But really, honestly, just spreading the word and everything too, telling people about this would be really helpful.
So yeah, we definitely want to do that.

Speaker 1: 00:46:13

Just briefly, in the spirit of busy polling bad, what about a WebSocket instead of the busy polling?
It might even speed it up slightly.

Speaker 0: 00:46:25

So WebSockets, as I understand it, that's a good question, I don't really know.
HTTP polling I believe is much more lightweight.
I might be wrong about that, but I don't know, maybe someone else can speak to this.
This is a bit outside of my domain.
Okay.
Okay.

Speaker 5: 00:46:56

Is because WebSockets is a raw TCP connection after it gets bootstrapped over HTTP.
So it's very difficult to hide the IP metadata.
And what's not shown in this diagram is a separate oblivious HTTP relay that acts as a proxy for every message.
So that's reason one.
And reason two is for backwards compatibility.
BIP-78 already used HTTP.
So by continuing to use HTTP, the V1 senders can send to v2 receivers and vice versa.
Yeah, in the future that might change.
We can use web transport, which is like the second version of WebSockets, to tunnel this with the proxy, but that's for the future, that's to be excited about.

Speaker 0: 00:47:46

Great question.
I think we're good.
Thank you, Brandon.
All right, thank you
