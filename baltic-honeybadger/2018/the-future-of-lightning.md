---
title: The Future Of Lightning
transcript_by: Bryan Bishop
tags:
  - lightning
speakers:
  - Elizabeth Stark
---
The future of lightning

The year of #craeful and the future of lightning

<https://twitter.com/kanzure/status/1043501348606693379>

It's great to be back here in Riga. Let's give a round of applause to the event organizers and everyone brought us back here. This is the warmest time I've ever been in Riga. It's been great. I want to come back in the summers.

# Introduction

I am here to talk about what has happened in the past year and the future of what we're going to see with lightning. One second while we get the clicker working. The tech never works at tech events. It's not the first time. Okay, awesome. Okay, it works sometimes.

One year ago, actually less, about 10 months ago, I was at Baltic Honeybadger. At the conclusion of my talk, I mentioned how excited I was for all the cool things coming in 2018. And now here we are. We need micropayments so I can use a micropayment to get my slides going here on lightning.

I think we're okay with the clicker now. Fingers crossed.

# History

For those who may not have been following the latest on lightning.... the year is 2008 and there's a pseudonymous person going by the name of Satoshi Nakamoto and he releases a whitepaper to the world to little or no fanfare and basically nobody cared. The 10th anniversary of this paper is October 31st of this year. We're super excited about this. Yeah. I think we're going to have some great halloween parties.

The first response a few days later, was basically "this system sounds great but I don't think it scales to the required size" so basically "cool story bro but does not scale". This was recognized very early on. When you have a global decentralized consensus system, there are scalability issues.

Fast forward to 2015 there's a paper that I helped edit... called the Lightning Network. It's a series of smart contracts operating on top of bitcoin, a layer 2 protocol using local consensus.

# Lightning network overview

Alice and Bob enter into a 2-of-2 multisig contract to get into lightning. They both put in some money and then they update the state between them. These are real bitcoin transactions. By the way, there's no lightning ICO. I know. It uses real bitcoin transactions. Alice and Bob update their state when they send money between each other. Every time they update the state, they sign off on a new state and revoke the previous state so that they can't steal from each other by going back on their word. Cooperative close can be done in 10 minutes.

# Payments as packets

Maybe Alice and Bob only see each other once in a blue moon. You can have a network and payments can be routed through other nodes. This can use multi-hop and hash timelock contracts (HTLCs). The way that the forward in lightning works is that intermediate nodes can receive funds only if it atomically goes to sender. In the vast majority of cases, it instantly transacts and goes to the end of the route. We also have onion routing which is where the intermediate nodes only know the before/after nodes but not the entire path.

We're eliminating counterparty risk. You don't have to trust Alice or Bob or anyone else in the system.

# If alice goes offline...

Maybe Alice is sick of bitcoin twitter and she's going to go to a desert island... what happens to Bob? Bob can broadcast a transaction to the chain and he waits a given amount of time and then he gets his money back. Alice gets her money back when she comes online again and everyone is made whole.

# If Bob tries to cheat...

You can't make up a state that doesn't exist, but you can broadcast a previous state. If Alice is offline, maybe a watchtower was monitoring and saw that Bob was trying to cheat. This can be enforced on the blockchain using pre-signed contracts. Bob shouldn't treat because if he tries, he's going to lose all of his money.

# Removing the trusted financial intermediary

You don't have to trust Alice or Bob. The blockchain functions as a judge or dispute resolution mechanism. You can think of blockchain contracts as contracts. Not all contracts go to court. The vast majority of lightning transactions won't go to the blockchain. It can't be bribed. These transactions are pre-signed and we know exactly what will happen and how it will be enforced. This is of course based on the security of the blockchain, and bitcoin is the most secure blockchain with the most hashrate backing it up.

# Lightning for many blockchains

Lightning also works on litecoin, which activated segwit. There's a concept of a lightning cross-chain atomic swap. Bob and Alice are on two different coins and they can be routed through an intermediary and to do an atomic swap between the two. November 2017 had the first lightning atomic cross-chain swap. This is exciting stuff in progress.

# Launching lightning

That's the recap for the people who may have been under a rock for the past year. As is the case in the bitcoin community, all of this technology is open-source. We implemented something called lnd, lightning network daemon. We have almost 3k github stars, so that's exciting. I highly recommend you check out the source code. This past year has been a wild ride. January 2017 we announced the alpha for lnd and we had an amazing community of people building and testing.

People kept asking when mainnet when mainnet. In March 2017, we announced the first beta for the lightning network. This was a huge deal. We didn't sleep for a week on our team. We put this out to the world which was super exciting. This was a huge milestone in the past year. The amount of progress we've seen since then has been mindblowing.

Last week, we announced lnd 0.5 beta. This includes neutrino lite client improvements, better phone support, better privacy support, more tor support, reliability improvements, better pathfinding. For those of you running lnd, please upgrade if you haven't yet.

# Interoperability

There's Blockstream c-lightning and ACINQ eclair client, and rust-lightning by BlueMatt, and a few implementations from someone in Japan. We've all been working from a common specification. There is only one lightning network, like the internet. We want everything to be interoperable. Here's the BOLTs specification repository. In December 2017, we announced interop tests between the 3 major implementations were complete. So we created an interoperable lightning network. I know many folks are excited about that.

# Developers, developers, developers, developers

It's important to get developers and to build usable application. Last week at Lightning Labs, we released a new version of our lightning desktop app. We have this beautiful design with cool colors. Our goal was to make it simple for people to use and interact with lightning. It's in testing mode. Right now it's a testnet version. The mainnet version is dependent on neutrino.

In this video, our lead app developer is... please work. Do I have to press something? No? Alright. Tankred is from Germany and he's our lead app developer. The german equivalent of coffee is... he used our desktop app to buy a beer. He thought the coffee thing was fun but a beer would be better. It's Oktoberfest in Germany right now.

# lnd 0.5

Neutrino had achieved a big milestone. Neutrino is a lite client implementation that we use at Lightning Labs together with Jim Posen from Coinbase have designed that. BlueMatt had been involved in that. Includes bip157 and bip158. It's substantially more private and does not leak various user data and transaction information. This is a very big deal.

# watchtowers

People have been asking about the desktop app-- when mobile? One of the important aspects of mobile phone support isn't just neutrino because you don't want to run a full node on your phone, but that we have watchtowers which are important. You might be traveling for a week and we want to make sure there are watchtowers monitoring for cheating on the network.

# A platform for merchants

For whatever reason, people like talking about buying coffee with bitcoin. We have a high-performance merchant platform where you can buy... is bitrefill here? They had mainnet support up when we released lnd beta. People were buying real things with real bitcoin using lightning. In fact, the next day, we at Lightning Labs gave a talk at airbnb, again I had no idea it would be the day after beta and laolu demoed this with me and we bought cell phone minutes with bitcoin. We had been working on this for so long, and holy shit it actually worked. So that was amazing to see.

We also had btcpay for those who don't know this is an open-source version of merchant payment processing software. NicolasDorier and some other developers had been working on this for a while and they were frustrated with other technologies in this space so they created their own. They have support for lightning in there. If you want to run merchant processing, check out btcpay.

GloBee has enabled lightning payment processing.

I believe we have Coingate here at the conference. We couldn't believe this, it's 4000 merchants that are now accepting lightning. It's been incredible to see this evolve over the past year.

# An application layer for bitcoin

Is not only lightning a tech for high volume transactions on bitcoin, it's also an app development platform for bitcoin. We have yalls.org, my cofoundered laolu named this. A similar site with a similar name was not using lightning. So yalls is an article micropayment site where you can use lightning to pay for articles, or you can buy beers or a beer emoji.

We have zap which is an application and UI for bitcoin and litecoin. I am sure we have some folks in the room have used that. How many people in here have sent a lightning transaction in this room? Okay, great. How many plan to do a lightning transaction in the next year?

# Satoshi's Place

In June 2018 there was a website that came online... I took a screenshot, I was thinking I need to show a screenshot of this for Baltic Honeybadger. There used to be million dollar homepage and you paid per pixel. In some versions, yo ucouldn't overwrite the pixels. This is mostly a safe-for-work version... I have some devil ears on, but it's not so bad. I'm thankful for my friends and team for restoring my image on this, thank you. This was on the frontpage of reddit and it went viral. This was an application where you could send 1 satoshi per pixel. This was a major moment for lightning that even though this might be a silly website where we're keeping bitcoin weird... warning, if you go there now, it might not be safe for work.

There were pixel wars.. I had to go to the scrollback on youtube. I was on satoshi's place and trying to figure out what went on, but someone put the FBI hidden site seized. The creator of this site makes $60-70 each time they do this. Luckily the community had saved the prior states and it got reverted. There are these pixel wars going on here. So why not make some pixel futures and have a marketplace for that?

# Lightning tasks

lnd.work is a mechanical turk site for lightning. You can pay small micropayments to do small amounts of work. Check it out, post some tasks as well.

# First

We had a lot of firsts in the past year. For example, here was the first book purchased with lightning, the bitcoin standard. I know we're hearing about that here today. We can't keep up with everything going on, it's amazing and incredible. People can buy things with lightning here. Great work for those who put it up there. Someone purchased the first sandwich on lightning. There aren't many more firsts left, like the first champaign or the first shoe then you better do so soon because the firsts are running out.

# Building the network

When I was here in last November, we were on testnet but there was nothing on mainnet. But back in February 2018 this is what people were doing on testnet- there was so much engagement. We saw the network map developed and people spinning up nodes and running them. Here's the state of testnet back then. On January of 2018 there were only 46 lightning network channels. In September 2018, there are over 12,000 channels. It's incredible to see this growth. Explorers are not canonical and they might have outdated views of the network, and some of the channels may no longer be active. In terms of order of magnitude, we have definitely seen incredible growth. We warned everyone when we released the beta, "be craeful".  We have a BTC limit and so on. Don't put your life savings on lightning.

Here's romport's map of the lightning network. I think there's about 107 BTC on the network. This is a lot. Don't put a lot of money into lightning. We'll see why in a second. It's been wild to see this evolve.

# Craeful

John Olivier did this amazing segment back in March where they told people instead of being in hodlgang, you should be craeful. Don't put more money into lightning network than you're willing to lose. I told people to put in $20 or something not huge.

# shitcoin.com can't buy lightning nodes

He put out an article that he is going to buy all the nodes. But you can't even buy nodes. That's not how it works. He put 40 BTC on the network. There were node limits and transaction limits. He opened a bunch of channels. Alex Bosworth, a recent hire at Lightning Labs, runs yalls.org and a variety of other stuff... Alex had about 1 BTC and Andreas had 44 BTC but it turns out that Alex made more money on his 1 BTC than Andreas did on his 44 BTC. He made 40x more of these fees.

Nick Bhatia has been doing great blogging about the time value of bitcoin. Alex's annualized return on his BTC was 80x higher than Andreas's. Alex was manually opening channels to specific nodes that Alex liked. Andreas got all of his funds back in the event, hopefully he won't do that until LN gets farther along. It's about optimizing about where you connect in the network.

# Casa

There's a Casa lightning node.

# Community

We've been doing lightning hackdays in Berlin. Someone setup a lightning candy machine there too. Someone decided to take a photo of me while I was talking and then put it on twitter and satoshi's place while I was talking while I was at the Berlin lightning hackday. Amir Taaki tweeted about how engaged the community was. We had 150 people from all over Europe to come out and participate. We were blown away by the questions and how advanced everyone was and to see the community engagement. We're seeing these popping up elsewhere and that's incredible, one in NY and one in Madrid.

# The year ahead

We're working on watchtowers. Neutrino will get more updates. lnd 0.5 had neutrino for testnet only. We want secure software. We believe we should have secure financial software. Neutrino mainnet will be coming soon, which will enable lnd mobile apps. And desktop apps won't have to sync the entire blockchain. Also we're interested in atomic multipath payments where you chop up your $10 payments into 5 $2 payments. They would go atomically on the network and arrive to the destination either fully complete or go back to the sender. This is important for liquidity and flowing through. Splicing is where you can add funds into a channel. You can also send a transaction out from a channel, called splice out.  Alex Bosworth was manually enabling channels. When we have things going, we want to route and find paths manually that Alex was doing manually.

Jameson reminded us and I want to relay this- we want this technology to be private, and there will be private channels. These channel explorer websites will start to become inaccurate because it wont be able to see most of the channels. Don't just look at the node count. The node counts will be growing but it will not be trackable.

# Community

A certain community online who will remain nameless and it has three letters... decided that I was the CEO of the lightning network. But no there are other implementations and we're an open-source community. We are all CEO of the lightning network, except for Craig Wright. Please check out CryptoGraffiti. He makes great swag.

# Conclusion

It's really been an incredible year so far. Someone tweeted this in January--- in December 1969, there were only a few nodes for the internet. Since then, so much has changed in the world. I think we're the same for bitcoin and lightning. This is the beginning and I can't wait to see what happens next. Thank you so much.
