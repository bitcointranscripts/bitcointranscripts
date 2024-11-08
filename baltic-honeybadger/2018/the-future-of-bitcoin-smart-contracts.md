---
title: The Future Of Bitcoin Smart Contracts
transcript_by: Bryan Bishop
tags:
  - contract-protocols
speakers:
  - Max Keidun
---
<https://twitter.com/kanzure/status/1043419056492228608>

Hey guys, next talk in 5 minutes. In five minutes.

## Introduction

Hello everyone. If you're walking, please do it in silence. I am a bit nervous. I was too busy organizing this conference and didn't get time for this talk. If you had high expectatoins for this presentation, then please lower them for the next 20 minutes. I was going to talk about the traditional VC models and why it doesn't work in the bitcoin industry. They don't work, and nothing has changed in the past 3 months, so why waste our time on VCs? They don't understand shit about crypto.

My topic today and I will sit, is the future of bitcoin smart contracts. Smart contracts are one of the hype terms or buzzwords that everyone throws around but not everyone understands. I'm sure you here, the audience is more sohpisticated on bitcoin than the general public. But it's still a problem. For many people, it's still a question. How do bitcoin smart contracts work? How can they be used in the real life? How can they be used in real economy?

## Multisig

Multisig- which we will be talking about today- is a type of smart contract. It's nothing new. I want to talk exactly about multisig. The purpose of the talk is to give out ideas to people who are wondering what to build on top of bitcoin.

Obviously, Hodl Hodl is using smart contracts. This talk is not about our company. We can't work on too many smart contracts, actually. As a business, we try to inspire or we're happy as much as other people, to build something new and build smart contract solutions on top of bitcoin because we don't have enough time to do it ourselves. I wanted to share some ideas. If you have any questions later, feel free to approach myself or Roman Snitko.

## Smart contracts

What are smart contracts? Instead of a definition, let's use an example we use at our exchange. I will also discuss use cases. The classic example is Alice and Bob. As you can see on the slide, there's Alice and Bob, two separate parties. They both have keys to release funds from a special p2sh address. The smart contract says it requires both Alice and Bob's keys to release funds from that escrow. This is what is known as multisig. It requires several keys to sign the release transaction. This address becomes a multisig escrow account or wallet. It doesn't matter who sends the fund to this escrow address; the only thing that matters is whether both parties releases them or who owns the keys.

On our exchange, we use escrow to allow users to exchange fiat currency and bitcoin and back. They avoid holding bitcoin in Hodl Hodl wallets. As an exchange, we hold one key, and the seller holds another. It doesn't take a lot of imagination to see how this 2-of-2 multisig approach can be used in other businesses cases outside of crypto.

Suppose you want to rent an apartment; usually your landlord would ask you for a deposit. Normally this deposit is held directly by the landlord. It would be fair if it was in a multisig escrow and could later be returned when both parties agree on resolution. The same escrow mechanism can be applied to freelancers of all kinds; suppose you want to hire a developer from another country to work on your software. So you can lock up some money in escrow, for example.

Another interesting example is creating a bitcoin equivalent for a future contract, and settlement is done in bitcoin. This would allow for a sort of p2p futures where two parties bet on an outcome. Funds bet on this contract are stored at a multisig address and not at a third-party. A month ago, Bitmex had a problem where the shorts were closing massively and people were disappointed. This scheme solves that, because nobody can effect your futures and agreements.

I could continue on and on, but this 2-of-2 multisig approach can be used in many places outside of crypto.

## Dispute situation

Many people, when they hear how 2-of-2 escrow works, they ask- what if one party decides not to release funds from this escrow account? Does the money remain locked forever? And if so, what happens? Who controls the locktime transaction destination address? What's the default case where both parties disagree? You should always use locktime.

No party has incentive to keep funds locked forever. Different factors influence the decision to unlock the funds. Locked forever may be a more beneficial outcome. 2-of-2 is an escrow model that can be applied to some, but not all cases. You need to consider market influences and all the other stuff in your business.

## n-of-m multisig

2-of-2 is a special case of n-of-m multisig. You could have a variable number of keys required to release the funds. Consider 2-of-3 multisig, for freelancer payments. Suppose he completed the job, but the employer doesn't want to release the funds. There could be a mediator on the escrow account as well. We implemented 2-of-3 multisig on Hodl Hodl for the exchange, mainly for large OTC trades but also retail investors and retail traders can use that as well.

There's a more complex use case where you require more signatures with different layers of complexity. You can have something like 5-of-12 multisig which could make more sense.

## Multisig implementation

As I mentioned, the problem right now is that multisig is not consumer friendly. They are mostly used by exchanges to store user funds. Average users are going to become frustrated figuring out how to use multisig. It has to make your brains not explode.

One way to go about this is to implement everything in a browser, which is what Hodl Hodl did. The frontend can create keys and store them without sending them to the backend. This is prone to certain security issues and kinds of attacks. It would be more secure to generate a second key on a smartphone app or a specialized device like a Trezor or some hardware wallet.

We will operate a marketplace with the simplified solution with frontend key generation, but also more sophistication with standalone devices as another option.

I want to specifically point out that multisig isn't something exceptional or novel. Hodl Hodl isn't anything new under the sun. We don't innovate really. When I approach him with new ideas, he usually looks at me like this. Multisig has been around long enough. But it's not user friendly. Say you want a new multisig contract; do any of you know how to set that up and do that?

## How to bring multisig to consumers?

There's no out-of-the-box solution for multisig. There needs to be an online marketplace for multisig party participants. There needs to be a focus on service marketplaces rather than product placements.

Openbazaar uses this for products; but we don't have a marketplace for multisig services. There's no innovation in multisig here. Nobody has bothered to bring it together in a way that people can use it. Not for fun or just to point out that bitcoin could do it, but because it's useful.

## Announcements

We're introducing an OTC trading desk at Hodl Hodl for large trades using 2-of-3 multisig. We have a non-custodial approach we have been developing from the beginning for our exchange. The second announcement is the idea that we will be launching bitcoin futures. We're currently working on this, and it will be released soon. It will allow people to bet bitcoin on the outcome of other things, and in other words it's a prediction market. The future contract will be denominated in bitcoin, and it's peer-to-peer. Keep an eye on our twitter.
