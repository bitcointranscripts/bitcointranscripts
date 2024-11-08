---
title: Recovering Payment Channel Midstates Using only The User's Seed
transcript_by: Bryan Bishop
tags:
  - lightning
  - watchtowers
speakers:
  - David Vorick
date: 2019-09-12
media: https://www.youtube.com/watch?v=Uh6Ywxrobzw&t=7850s
---
<https://twitter.com/kanzure/status/1172129077765050368>

## Introduction

Cool. This addresses the lightning network which is a scaling technique for the bitcoin network. A big challenge with the lightning network is that you have these midstates that you need to keep. If you lose them, you're out of luck with your counterparty. We had a lot of talks this morning about how to recover midstates but a lot of them used watchtowers. However, this proposal does not require a watchtower and you can restore midstates knowing nothing but your wallet seed.

## Watchtower complications

What's wrong with watchtowers?

The way that watchtowers are currently used, there's a big storage challenge. Every time you do a state channel update, the watchtower has something new to watch for. This can be prohibitive.

To be effective, watchtowers need to have high uptime and reliabiliy.

In general, it's yet another piece of infrastructure for the lightning network to depend on. It's not some gross intractable piece of infrastructure, it's something practical that can be built, but it would be better if we didn't need watchtowers at all.

This talk is just one angle that we can use to drop the watchtower requirement for most users.

## Goal

The goal is to stay safe against an untrusted counterparty even if we end up losing our channel midstates or our data.

## Major assumption

The major assumption that I'm making here within the bounds of this talk is that the user has some interaction with a payment hub where I'm going to define a payment hub as a high-reliability counterparty. We can expect that this hub will not be losing data or going offline. This might be Coinbase or this might be some community hub or it might be a university. We're going to depend on hubs, instead of watchtowers. If you still want watchtowers, there's no reason you couldn't have a watchtower do all of these things, but we're trying to get away from watchtowers. I do believe there's avenues where we can drop the hub requirement and make this purely p2p. As of today, I don't have a direct way to do that.

## Strategy

Our hub counterparties are going to be leveraged as data storage devices. We're going to store this data on the hubs. We don't want to tip our hand to the hubs when we've lost our payment channel information, because they are a counterparty in the channel and they can take advantage of us if they realize we're vulnerable. We want to construct every transaction with the hub in a way where it seems like we've lost our data; in the majority of cases, we can catch them cheating. The one time we really need it, if they cheat we won't catch them, hopefully they will have no clues that we are in fact in a vulnerable state.

## Information storage

We're going to take an encrypted blob, constant sized, and store it on the hub. I suggest 40 kilobytes, which allows you store a fair number of payment channel midstates and lets you throw in encryption passwords. If you're using utreexo, then you can store a signed utreexo hash and skip blockchain validation upon recovery. Anyway, we're assuming about 40 kilobytes. A hub can support hundreds of thousands of users with a few gigabytes on disk or just in RAM. If the hubs are collecting fees, then I really don't think this is an unreasonable burden to place this on the hub.

Our encrypted blobs will be encrypted derived from our wallet seed. Each time we update it, we increment the counter. We can compare versions of encrypted blobs and make sure they are all up to date. Because the blob is fixed size, we can put anything we want in the padding if there's some external use we have for that, it becomes available to us.

## User requirement

The user will also be storing this blob and information in a decrypted way. When we ask the hub for the encrypted blob, we can verify that the hub is being honest.

## Pamyent protocol

We're going to tweak the lightning protocol. The very first thing we ask is the hub for this encrypted blob. This gives us plausible denialability at the cost of this extra 40 kb before the user makes any transactions. If the blob matches, the user will prepare the desired transaction and give each honest hub a new blob to store which contains the updated midstates.

If the hubs are communicating with each other, and in one case they see the hub is contacting one hub or in another case contacting multiple hubs, then for perfect security every time we do a transaction we need to contact all the hubs. Each time we're transacting, we're doing 40 KB roundtrip to each payment hub that we're using.

If all the blobs match, we continue forward and we just make a normal transaction. But before we finalize the transaction, we update all the blobs with the new midstate, and we pass this over to the hubs, and then we broadcast the transaction.

## Dishonest hub

What do we do if the hub is dishonest? The hub might provide us with an outdated state. If it's a hub we're not transacting with, we just mark them as bad. If the hub we're directly contacting provides us with an outdated state, it's actually safe to play naieve and so you can move forward-- the hub presents you an outdated state, you can move forward and complete the transaction. You haven't given the hub any hint that something is wrong; later, you stop interacting with them. Later, when they broadcast or close out the channel, you should be able to deliver a penalty transaction.

## Protocol extension: fraud proofs

One more thing that we can do with this protocol is we can extend it so that at each stage of interaction, whatever the hub is telling us, they can sign it and provide that signature with a timestamp. This provides cryptographic proof later that we can say hey this hub was trying to cheat me. This is a fraud proof we can hand out. It raises the stake on the hub. You're not just risking one customer or counterparty, you're potentially risking a wider set of users.

## User recovery

If the user has lost data, from the hub's side it looks the same. The user asks the hub that they want to transact with for the most recent state information. Then they also ask the other hubs that they have channels with for the most recent recovery information. Then they will compare the blobs that they get with each other. The user decrypts it, they compare the information and they cross-reference it. They make sure all the hubs gave the same information. All you need is for one of the many hubs to give you honest information, and you can catch all the malicious hubs.

Externally, the hubs have no idea that you have lost information. You come online, you download everything, you check it all. If it all checks out, you move forward like normal. If a couple of hubs lie to you, you do the same broadcast thing, and you may or may not be able to construct a fraud proof and then you blacklist and close out and move on from the hubs that have tried to cheat you.

## p2p channels

As long as the user has a channel with at least one hub, you can follow this protocol and lump in p2p channels with it. To move to payment channel recovery style, you don't need all your payment channels to be on a hub. Just enough of them.

If you have no other way to get your channels back, this is just one more option you have given yourself. Maybe it will work, maybe it won't. If you're using watchtowers, maybe that's sufficient. This is just another option you've given yourself to recover your payment channels.

## Tradeoffs

The biggest tradeoff is that every time you make a payment channel update you have to contact your hubs and do a 40 kb roundtrip with each hub. I don't think this is a big deal. I think doing a megabyte of bandwidth for a financial transaction is really not that bad. But if you want extremely fast lightning payments, then 1 MB might be prohibitive and you might have to look at alternatives.

A smaller tradeoff is that the hub now has to store 40 KB per user. This should be trivially, especially if users are paying the hubs with transaction fees.

## Incentives

This creates an interesting, mild incentive in practice. If you think about lightning network where hubs are collecting fees, every hub represents competition to other hubs. If you see a hub and you see a user who is potentially vulnerable, and you suspect the other hubs are trying to cheat them, you can give the user the opportunity to penalize the other hubs. So hubs have a mild reason to help users prove fraud of the other hubs. That's pretty interesting.

## Failure modes

If every hub is collaborating or trying to take advantage of the user, or every hub knows that the user is vulnerable, then all the hubs could work together to give the users an outdated midstate.

## Missing pieces

I think the hard part is just the protocol about getting the midstate from a hub. If the true goal is to recover all your payment channel information from nothing but your seed, well we have already assumed we know the counterparties or hubs. We still have to-- to get true seed-based recovery, we need a way to figure out someone who to ask for the midstate recovery information in the first place.

## Payment channel coloring

You can scan through the blockchain and identify which payment channels are yours. We can do this with coloring. You put an encrypted message in each payment channel or transaction you make, that uniquely identifies only to you that this payment channel belongs to you. If you include information such as one of the output IDs of the transaction in the encryption key, then you can take your wallet seed and deterministically derive something that will let you check every payment channel in the blockchain and identify whether it's yours. People will see that the channels are colored, but no external party can link your channel to you unless you leak your wallet seed. An external party can't look at the blockchain and link multiple channels together. You can color it in a way where it is obvious that the transaction has been colored, but you don't stand out from other people who are using the same coloring technique, but you can identify exactly your payment channels. Also see stealth addresses.

## Counterparty discovery

Once you figure out your channels, you need to figure out your counterparties. Myabe take one of the public keys from the transaction, and put another set of encrypted data into the transaction to identify the counterparty. From there, we would use the public key to lookup the counterparty in some public-key infrastructure whether we're using the MIT hosted PGP stuff, or we could put the public key infrastructure on-chain, or some hub could announce this is my public key and this is my IP address for how you can communicate with me. I think there's a lot of ways to approach this problem and didn't want to get into this.

## Tradeoffs again

The biggest tradeoffs for these two techniques are the extra on-chain data. You have to include the coloring data and also the encrypted public keys. I tihnk there's a way to minimize the impact. But maybe you can minimize the data, like sneaking data in through pay-to-contract into your signatures. I don't have an explicit technique to do this.

## Watchtowers comparison

So this requires payment hubs, which is a downside over watchtowers. It requires slightly increased on-chain data, which is definitely a disadvantage. And also, you require more interaction. It would be my suggestion or my understanding is that this is probably simpler than implementing watchtowers in practice. It's also a protocol modification, which is never simple. It's clearly not a strict upgrade or strict replacement for watchtowers. But I think it's an interesting alternative, and it would be interesting to be able to operate as a user in this scheme.

## Future research

I think the biggest item is increased on-chain transaction sizes could be reduced. If you get creative about how you setup your payment channel recovery strategy, maybe you can contact only some subset of hubs and there might be some deterministic random selection of which hubs you contact and which ones you cross-reference. It's not clear to me that it's a requirement to contact all the hubs every single time.

I didn't even talk about fee mechanisms or how hubs are getting rewarded for the work they are providing. We should look into that.

What would be really great is if we can do this at the p2p level. Joseph Poon was suggesting there's some negotiation protocol you could do between peers, like a bidding game. It sounds promising. With further research, we might be able to drop the hub specific requirement and just run this at a pure p2p level. I don't have that fleshed out at this point. I don't know what the conclusion of that would be.

Q: Couldn't the colluding hubs defect from the collusion by giving a more recent midstate?



