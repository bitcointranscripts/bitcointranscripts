---
title: FediMint
transcript_by: Ringoz1 via review.btctranscripts.com
media: https://www.youtube.com/watch?v=lQ0dETyS28o
tags:
  - ecash
  - ux
speakers:
  - Stephen DeLorme
  - Justin Moon
  - Christoph Ono
date: 2022-07-29
aliases:
  - /bitcoin-design/learning-bitcoin-and-design/fedimint/
---
## Introduction

Stephen DeLorme: 00:00:04

All right.
Welcome, everybody.
This is the Learning Bitcoin and Design Call.
It's July 26, 2022.
And our topic this week is FediMint.
And we have Justin Moon here with us and several designers and product folks in the room here that are interested in learning about this.
So I've got a FigJam open here where we can toss images, ideas, text, links, whatever we want to consolidate during the call.
And anyone on the call right now can find that in the Jitsi chat if you want to jump in there with me.
But without further ado, I'll just turn it over to Justin and I'll let you kind of take this wherever you want to take it.
If you want to center this around specific questions, we can do that.
Or if you just want to take it away and give us an overview of FediMint, that's cool too.

## Justin introduces FediMint

Justin Moon: 00:01:00

Yeah.
So FediMint is kind of hard to explain.
It's a little bit like Bitcoin and there are sort of different facets to it.
So, let me think how to best explain it.
I'll start from just like the obvious thing.
So one thing that it's a layer two technology basically or you know whatever you layer two layer three whatever you want to call it.
And it it works really well with the layer two technologies like with Bitcoin and then with Lightning.
So that's kind of how to think of it.
It's a layer two technology.
And so what is it used for?
Like one thing that it's very good for is scalability.

## Scalability

Justin Moon: 00:01:50

Think of it like a side chain, like Liquid or something like that, that allows people to transact without having to go on Bitcoin.
For example, one FediMint Federation can run on a couple of Raspberry Pis and it can do about as many transactions as Bitcoin.
So if you can think of a world where like there's 10,000 of these out there, then you just increase the amount of transactions that Bitcoin can support by 10,000 times, something like that.
So that's one thing that it's a way of moving transactions off of Bitcoin.
So it helps Bitcoin scale.
It also helps Lightning scale.
One problem with Lightning is that it's kind of difficult to run a Lightning node just because it's not just a UX problem, there's UX problems, but it's just a complicated protocol and there's, you know, so you have to manage liquidity, you have to manage channels, you have to stay online all the time.
There's all kinds of difficulty in terms of being able to send a payment across a bunch of routes and have every single peer really online and everything.
It's difficult for a mobile phone to be able to do this, for example.
And also it's capital intensive.
You have to lock money into a channel, right?
And so, FediMint also helps scale Liquid because you could have a lot of users share one Lightning channel, for example.
And so, it allows for a little more specialization there too.
So for example, you can have one really expert Lightning node operator serve like, let's say, a thousand people in the FediMint, 10,000 people.
So it's a little more specialization there and that these Lightning node operators can compete based on how good they are at completing Lightning payments.
And so usually when you have these trade-offs for scalability, for outsourcing stuff like running a lightning node, usually the privacy is terrible.
Usually that's the trade-off.
It's more convenient, but the privacy is terrible.

## Privacy

Justin Moon: 00:03:51

And so one of the things that's very interesting about FediMint is that while it helps with the scalability, while it helps with a simpler user experience, the privacy is actually better than with Lightning or with Bitcoin.
You don't need to know too much about it, but I'll give just like a simple example.
So how FediMint works is users deposit money into it and can withdraw from it.
So it's custodial.
And when you deposit money into it, you get an IOU.
And the IOUs have an interesting property where any two IOUs, once they're issued, let's say I'm issued an IOU, I deposit and I get an IOU.
Stephen deposits and gets an IOU.
When Stephen goes to redeem that IOU, the mint can't tell if it was him or me.
So every one of these IOUs looks exactly the same.
And so that's where the privacy comes from, is that you get these little IOUs and everyone looks the same.
And this is why it has to be kind of a custodial system because it's IOU based.
And so yeah, you can think of it that way.
It's very good for custody or it's very good for scalability and it's also very good for privacy.

## Custody with a federated mint

Justin Moon: 00:05:09

Let's talk a little bit about the custody side.
So you have to deposit into a mint.
What is a mint?
So usually when you deposit into something it's like one entity, right?
There's one entity that runs it and if that entity decides to treat you poorly, you're just out of luck.
And so how FediMint works is it's something called a federation.
And a federation just means that instead of one entity running it, there's multiple entities.
And one example of this is Liquid.
Liquid is a federation, right?
So it's a second layer blockchain that has a bunch of features that don't exist on Bitcoin.
For example, confidential transactions.
These are transactions where the amount is hidden or confidential assets.
I think you can't even see what the asset is and you can't see the amount either.
And so, FediMint works similarly underneath and why is that useful?
Well, if you have a custodial thing that has great privacy features, maybe it's a target of tax, for example.
And so if you spread out who runs it it might be a little harder to shut down for example and so and I guess so one last interesting thing about this.
So, yeah, Federation is basically, it's like a multi-sig.
It's a multi-sig.
Each one of these servers, there's like, let's say me, Stephen, and Christoph are running FediMint, right?
We'll each have a server and the server just runs one program, relatively simple program.
And so underneath me, my server, Stephen's server, and Christoph's server all have one key and a two of three multi-sequence site.
And then the server itself has a bunch of logic for what to do with that custody of Bitcoin, right?
Like whether to accept the deposit, whether to issue a withdrawal, whether to issue these e-cash tokens, and lastly, whether to use these e-cash tokens to basically incentivize a Lightning node to do payments for them.
And so the federation is the multi-sig and then there's some logic inside that my server, Stephen's server, and Christoph's server need to agree on that allows basically smart contracting.
So it's kind of like underneath, it's kind of like a smart contract as well.
And the smart contracting so far is very blunt, but one of the, they can only do a couple of very specific things.
But I think one of the promises over time is that all the smart contracts and that exists on we'll call them altcoins could exist here in a federation.
And when you really think about it, most of these altcoins are basically federations, right?
They're not terribly decentralized.
There's a handful of entities that basically control what the rules are and they they pretend to be something very distributed and organic like Bitcoin but we know that all of them besides Bitcoin really aren't this way, especially, and some of them aren't even close.
And so, if you had like a let's say you had a federation with 100 servers, that's probably more distributed than Ethereum is.
You there's probably less centralized trust there.
And so if smart contracting is a good idea, like if there are a lot of use cases, potentially it could happen on a system like FediMint that's a federation and it would work just as well as on Ethereum and plus it's all trust-based.
So you have to trust who runs the servers.
That's an important thing.
To use it, you need to trust me and Christoph and Stephen, right?
And you basically trust that no two of us conspire to steal the money from everyone else.
Right.
So it's a trust based system.
So the security comes from trust and not from proof of work or proof of stake or any of these other consensus mechanisms.
And from my point of view, that would be completely inappropriate for like a global money like Bitcoin.
But like, one example we talk about the land registry, right.
A way to register land titles and like a local area not global just a local area this would probably a lot better than a proof of work mind blockchain or something it's just simpler and clearly trust based.
So these are kind of some of the different angles of FediMint and just to sort of summarize this like, what the hell is this used for?

## Community banking use case

Justing Moon: 00:09:23

We think it could be really interesting thing for like community banking kind of like Galoy has been used so far.
So, you know last week there was a company announced, Fedi.
We're not going to talk about that in the call but that's just an example of like the use case there will be community banking to try to actually deploy these in areas that are under, that really a lot of these places just don't really have much of a financial infrastructure like we have in the West.
I have in the West for example.
And yeah, they also have a lot stronger trust relationships in their local communities.
It's less institutionalized in the West for example, but on the other side, the trust relationships at a local level are much stronger in the US.
For example, a lot of people don't trust their neighbors at all, which is kind of sad.
So yeah, with that, I'll pause and kick it back to Stephen and Christoph.

Stephen DeLorme: 00:10:19

That's awesome and I'll go ahead and say if anybody has any questions feel free to you know chime in throughout this call.
These are usually pretty open.
I can think of one but maybe before I ask one does anybody else in the room have any questions like for Justin having having heard that overview of what FediMint does?
Cool, well I'll jump in with one.
Sorry go ahead Christoph.

## Where is the FediMint project right now?

Christoph Ono: 00:10:51

I was just gonna ask where is the project right now?
Is this a very new idea that's just kind of starting to take shape or how far is the development of their first alpha version.

Justin Moon: 00:11:05

Yeah great question.
It's been a research project for like kind of like a couple of years.
Eric Syrian the creator had this idea a few years ago and then there's a lot of cryptography and stuff that he needed to develop before it would actually be usable.
So he's working with Blockstream at the time so he got a lot of valuable basically mentorship from people like Tim Ruffing, let me know if this is too windy by the way, if it's making a bunch of noise.
So, that was kind of going on for like the last two years or so and so now it's at a point where it's starting to become usable like so you can you can run it on your computer and you can run like 2 Lightning nodes and you can do lightning payments with it running on one computer.
Over there I could bring it later on we have a stack of four Raspberry Pis that are our first like federation so we've deployed it on one it's still like testing but it like one actual thing where each one is running on a different server and that works and so we're currently basically trying to set up the first one that we have a prototype mobile app that can just send and receive Lightning.
And so we're currently in the process of trying to get our first deployment that can send and receive with fake Bitcoin, like RegTest or Signet, something like that, Bitcoin.
So it's getting to the point where it's usable, but definitely not on main net.
And so hopefully, we're hoping like maybe three months from now, four months from now, kind of like October timeframe, really, we could start having our first testing on main net of the federation.
So it's kind of like alpha, pre-alpha.
But the foundation is really strong.
That's a really great thing about this from the software point of view, is that the software is extraordinarily high quality from my point of view.
So while it's not quite ready, like the foundation is really strong.
So hopefully, the testing will be successful.
We won't have to go back to the drawing board very much.

## Self-custody vs Community-custody

Stephen DeLorme: 00:13:21

So it's curious to know, how do you think about the custodial nature of FediMit because I think you know for a lot of people in open source you know we think about self custodying the seed phrase or having you know a channel backup of your Lightning node or something like that and this this project is interesting because it's actually being like no we are custodial we're just custodial in a different way so you can tell us your thoughts a little bit about how you think about that.

Justin Moon: 00:13:47

Yeah.
So I mean I love self custody.
I have a very paranoid multi-sig personally.
So you know we're pro self custody.
And on the other hand almost everybody uses heavily centralized custodial services today.
And many of them indirectly steal from you by selling you fake Bitcoin as if it's the real thing.
And so I don't know.
When we see in the kind of the community discussions, like there's a lot of discussion about importance of self custody, but there's a little bit of a blindness to the fact that all the normal people use heavily centralized custodial third parties that are not your friend.
So a lot of the idea with FediMint is to try to find something between hardcore self-custody and not just hardcore but like self-custody and these super centralized third-party custodians.
So that's one aspect and there's another aspect of it too.
Like, I have self custody.
I've done it for a long time, a while, and I'm comfortable with it.
But I would still like to use this because I don't really care so much about self custody for my Lightning node for payments.
What I want for my Lightning node for Lightning is I want the payment to work every single time.
I want it to never fail.
I want it to work quickly.
I don't want to have to maintain anything.
I don't have to think.
And I would like it to be private.
So like I would personally love to use this for a spending wallet for Lightning in addition to multi-sig cold storage.
If you ever had like the taco truck at a Bitcoin conference and look at the wallets people are using, you'll notice that a lot of people's Lightning wallets who are hardcore, self custody maxis are using custodial lightning wallets.
So, I think those are two angles.

Stephen DeLorme: 00:15:52

Yeah, that makes sense.
And, another another kind of thing I've been you know I'm not sure if anybody else on the call has been like kind of following up with like all the FediMint podcasts and stuff but one other angle I thought was interesting is just the idea that like if you're going to have a custodian it might as well be like someone you trust in your community.

Justin Moon: 00:16:18

That's a great point.
Yeah.
There's an Uncle Jim aspect of it too, right?
Like we've talked about this Uncle Jim idea of having, there's a big question, how are normal people going to access Bitcoin?
Right?
And currently, the answer is Binance, right?
If we're being honest, that's the answer currently is like, is Binance, Coinbase, FTX.
That's what people are using.
And so it'd be nice if we could have something where it's like you know Stephen's neighbor accesses it through Stephen because Stephen's an expert right.
Christoph's landlord access it to Christoph and you know people in their community who are like the experts that would be an improvement, right?
And we have to be realistic about you know how you know whether how much effort people need to be spending on their Bitcoin stuff, right?
Like ideally, we shouldn't all be spending a part-time job just to use Bitcoin properly, right?
Like that's a lot of it is like, can we create like good default privacy, right?
Like, cause you can get really good privacy today, but it takes a lot of effort.
And it would be nice if we had a little bit more like default privacy that doesn't require any effort.

## Are mints interoperable? How Chaumian mints work

Christoph Ono: 00:17:30

I have a question.

Justin Moon: 00:17:32

Go for it.

Christoph Ono: 00:17:33

So two questions, actually.
One is, are mints interchangeable?
Can I take an IOU from Stephen's mint and redeem it at your mint?
Or is it bound to a specific mint and is it possible to find out like here's an IOU it belongs to Stephen or someone else?

Justin Moon: 00:17:54

Yeah that's a great question.
So "Fedi" - "Mint", right?
It's concatenated two words, Fedi for Federation and mint for Chaumian mint.
I described Federation I haven't described Chaumian mint yet.
So it's a very interesting idea from the 1980s from 1982 I think was when the original is a paper and this is the idea of this remember when I was saying like me and Stephen would have an IOU and the mint could not tell from whom the IOU like when we go to redeem it they can't tell whether it's mine or Stephen's right that was this guy David Chaum invented this idea.
What the IOU actually is just like a little piece of data you know it's a couple hundred characters long and so let's say I am a Chaumian mint and Stephen is a Chaumian mint and we don't know each other, if a user presents a token from my Chaumian mint to Stephen, he would just be like, well, I don't, it's even if it's the same format, the token is exactly the same format.
He would look at it and be like, well, I don't know of this token.
I have never issued this myself.
I know that I did not issue it's actually the token with the signature, right?
So the signature would be wrong.
And so the answer to the question is are our mints wouldn't be able to interoperate at all.
And this is a big problem with this idea historically is that it would struggle to plug you into like the broader commercial world.
And so that's where lightning comes in.
You can think of these mints as like kind of little enclaves.
Right.
But they're connected by like a road that is Lightning.
Right.
So lightning is like the instant settlement layer between these mints.
So if I'm in like, let's say if I'm in mint A and Stephen is in mint B, then I can generate an invoice that when paid, I will receive tokens in my mint and he can pay that invoice using tokens from his mint and, between the mints, it's just a normal Lightning payment.
So in a sense, you can think of it as kind of like an extension to lightning where like the first or last hops on a route don't actually happen in Lightning at all.
They actually happen between a mint and a lightning node operator.
This is really cool because it's not trying to compete with Lightning or anything it's trying to add something you know it's kind of like tarot for example right like tarot is and to introduce this idea of like assets and stable coins into Bitcoin and so a good thing about it is building on top of lightning.
So if it works it'll make lightning bigger and more liquid.
I think the same thing is true of FediMints as well.
Like if it works it'll just make will make Lightning better.

Stephen DeLorme: 00:21:01

Someone's dropping in.
Go ahead.

Jimmy: 00:21:05

I was just saying in a way it's settling like strike advertisers.
Well, for Bitcoin, basically, and then like settle back into another token.

Justin Moon: 00:21:16

Yeah, basically.
Yeah, exactly.

## Connecting mints over lightning

Stephen DeLorme: 00:21:22

So I'm curious to dig into this graphic that somebody dropped in here.
User one requests Lightning invoice A from LSP3 in mint 2.
So this is what user 1 meant to...
That's the LSP right there.

Justin Moon: 00:21:36

It's a very detailed.
It's a great.

PW: 00:21:42

That might be a bit complex to walkthrough.

Justin Moon: 00:21:43

Yeah.
It's kind of like how it works.
It illustrates how like, see the three, like this mint A and mint B, those are Federation mints.
LN merchant, it doesn't know anything about Federation, doesn't even know they exist.
The cool thing is, Mint 1 and Mint 2 can interoperate.
And Mint 1 and LN Merchant can also interoperate, because like, Lightning is the lingua franca.

Stephen DeLorme: 00:22:13

We've got this LSP over here, and let's say like someone in that one decides that they want to pay somebody over here in Mint 2.
Well, you would end up with is this Lightning transaction between these two LSPs here.
And so this Mint would lose some of its Bitcoin.
This Mint would gain some Bitcoin and then in response to gaining that Bitcoin they then have to Mint eCash tokens to represent those.

Justin Moon: 00:22:43

So actually it's a good try but that's not exactly how it works.
One interesting thing about FediMint is that in order to do anything useful the mint has to custody Bitcoin.
So it all starts with a deposit.
Someone deposits some Bitcoin in and then tokens are issued.
And one of the important things is the amount of all issued tokens and the amount custody should always match each other.
And this is actually one of the limitations of FediMint is that since it's so private, it's kind of the same problem that like Monero has, for example.
And this is probably one of the reasons why Bitcoin will never have really strong on-chain privacy, is that if you add a ton of privacy and you make it's not everything public, then it becomes difficult.
FediMint can do a proof of reserves.
It can prove the reserves they have, but it can't prove the liabilities because they would have to basically de-anonymize all their users, right?
They would have to like, there's just not really a good way, like it can't prove its liabilities, but internally in the system, like if the system is running as expected right if no one is tinkering with it and trying to make it work incorrectly the assets and the liabilities would be equal at all times.
And that's like we do a lot of work to ensure that.
And so to the question of how does a payment between Mint 1 and Mint 2 work.
So Stephen was saying like oh well one of the mints loses Bitcoin and one of them gains Bitcoin.
And that could work if the mint itself actually ran a Lightning node.
But actually, the Mint itself does not run a Lightning node.
The mint custodies Bitcoin and it has like a little smart contract system.
And a Lightning node operator, LSP1 or LSP2, they basically like serve at the...
We envision like a free competition for these LSPs to be able to go and serve federations.
And so what does that mean?
So the LSP has to trust the federation because they'll have to hold a balance of these IOU tokens, right?
And so if the Federation is a bunch of liars and they issue fraudulent tokens that they don't redeem later, then the Lightning Gateway would lose money, right?
So the Lightning Gateway has to trust the Federation, but the federation does not have to trust the lightning gateway which is which is very nice because it kind of hopefully it will allow like a healthy competitive environment where the LSP's compete to serve federations in terms of how good they are at competing Lightning payments.
And this is how you might get like very, very reliable quick transactions.
And so, the LSPs have to hold a balance of tokens.
And so the way the transactions actually work is like, let's say there's a user in Mint 1 and he's trying to pay a user in Mint 2.
What will happen is his tokens in Mint 1, the user in Mint 1's tokens will be sent to the LSP attached to Mint 1.
Does that make sense?
So LSP 1 will get a little bit of tokens.
Like, okay, just because this is a little complicated, but it's worth seeing.
There's a user in Mint 1.
He wants to pay a user in Mint 2, right?
So some of the user in Mint 1's tokens will go to LSP 1.
LSP 1 now owns a little more tokens.
Now LSP 1 will send some Lightning to LSP 3.
So now he's gained, or she's gained in e-Cash tokens and lost Lightning.
And probably there's a, they probably gained a little total to represent a small fee right and so now LSP3 has a little bit more Lightning balance and so what they'll do now is they'll give a little bit of their e-Cash an equal amount of their e-Cash balance to the user inside Mint2 right so that's the way it works like The LSPs are kind of like a money changer between the token, the IOU token, and Lightning Network itself.
And so the way it works is it's basically an escrow underneath.
And the agent, it's an escrow between the user and the gateway, the LSP and the user, and the federation basically judges whether the transaction worked by basically checking whether pre-images are correct.
So it's very simple.
It's an escrow and the gateway is the judge or the sorry the federation is the judge.
It's not important to understand like that aspect of it but just like the you know the flow of funds is kind of interesting.

Stephen DeLorme: 00:27:15

Got it that makes sense that when you said that the LSP needs to trust the Federation but the Federation doesn't necessarily need to trust the LSP because the Federation is going to be the judge of like whether the users receive the money or not.

Justin Moon: 00:27:34

Yeah.
So one thing that also one thing in addition to the the you know the idea of like a competition between lightning nodes that do it for like a profit incentive.
You know the alternative is also like somebody in the mint just wants their friends and family to have like a nice lighting node and so they'll run and they won't charge any fees maybe you know they want they could be running it without a profit motive which is also kind of cool.

Stephen DeLorme: 00:28:00

So it's almost like the node operator, there has to be like some kind of software plugin or something that they can hook up to their Lightning node that basically allows them to hold this token balance in addition to sending out the ordinary lightning transactions and Lighting messages that they usually do.

Justin Moon: 00:28:18

Yeah, so the way this works is we only support Core Lightning so far, formerly known as C-lightning.
And so basically there's just one file.
So Core Lightning has this thing called plugins.
If you want to add extra functionality Core Lightning, you run a plugin.
What is a plugin?
It's just one little file, a little computer program.
And you stick in a folder that you tell Core Lightning here this is the folder with all my plugins right and some plugins are for rebalancing channels other plugins are for you know doing stuff like that and so we just have a little plugin that teaches the gateway how to hold an e-cash balance and and you know a couple other details with you know when a when a payment comes in that might be a FediMint payment like what to do with that and how a user can tell the gateway like here I'd like to do an outgoing payment, right?
But it's basically just you copy one file into a folder and rerun C-lightning which is so it's really really simple and LND will work roughly the same way they have this thing called an HTLC interceptor.
It's just like one little file you got to run.
And so hopefully this could be something very simple if you're doing on the command line as command line go command line can get very complicated.
Just run one little file and and hopefully eventually there will be integrations and stuff like Voltage, some of these node offerings, maybe BTCpay, some of these things that have like, or maybe Umbrel, some of these things that build UIs for your Lightning node.
They could just have a couple buttons like, hey, would you like to become a gateway okay what what is the config file for the federation you want to serve right and that just has the addresses like the you know the URLs for the federation servers, right?
And so you just like paste that in or scan a QR code and now you're a gateway and you just have to decide how much e-cash tokens you want to hold and someday there will probably be options for, like automatic rebalancing between the two, but that's just a dream at this point.

## Backups for FediMint users

Stephen DeLorme: 00:30:20

So I thought it was interesting you said about your you mentioned with the Core Lightning thing the balance of e-cash tokens.
And so it gets me thinking that the data structure of this is much different than what a lot of us are traditionally used to.
We're used to thinking of a Bitcoin wallet as being a seed phrase.
And as long as I have the seed phrase and two or three other pieces of information, I can regenerate the whole wallet.
If I have lightning wallet I need that plus some kind of channel backup and I can regenerate the whole node or sweep those force close, sweep the funds on chain.
But the whole backup recovery process uses much different data in the federated model.

Justin Moon: 00:31:07

Totally.
So the way these eCash tokens, these tokens work, these IOUs, eCash tokens means these like anonymous, like private IOUs, they're indistinguishable IOUs. Like this is kind of an implementation detail.
Most users in the future I don't think will necessarily even know this is happening.
Kind of like a channel.
Like someday I don't think most users will even know what the channel is potentially or like a UTXO you know you might be a Bitcoin user you might have a Bitcoin you know wallet but you might not actually know what a UTXO is that terminology isn't hopefully we could get to a future where you don't need to know all this terminology.
Okay so yeah the token a little piece of data and you'll actually have a lot of tokens.
So basically the tokens have to have a fixed amount.
This is kind of a little in the weeds, but it's interesting to think about.
They have to have a fixed amount because your anonymity set comes from all the people that have the token of the same denomination.
So if you encoded an amount in there, your anonymity set would probably just be you unless you were using a very standard amount.
And so you end up with tiers, right?
Like there's a one sat token, a 10 sat token, a hundred sat.
And these are combined to make payments, to express an arbitrary amount.
Someday I think we'll be able to use fancy cryptography to encode the amount like in a zero knowledge proof but that doesn't exist yet.
So we don't we wouldn't need these denominations.
So inside the wallet you have a bunch of these little tokens kind of like dollar like like quarters and dimes and nickels in the US you know.
And so and importantly these are you know these are bearer instruments IOUs. And so if you lose them, you can't prove that you actually own them, right?
And that's where the privacy comes from.
And so if you lose them currently as it exists now your money's gone big big UX hurdle right and so one one thing that we will eventually do is implement recovery schemes and.
So how that would work is that some of the data inside the token could be represented with like a seed, right?
And so it's a little weird to think about this because like the whole idea was, it's a custodial system, but now we have a seed again what's going on here right I think there's some really interesting things we can do because we have this federation of trusted servers right so like one one one option is you could seed and you just store it like you and any other wallet but it's a little weird because you lose some self-sovereignty in terms of self custody but you gain a lot of privacy.
So personally, as someone who knows how to deal with seed, I might like that.
I might use that.
But most users we envision using that, this is not a great option for them.
So one thing you could do is you could shard the seed into pieces and send one to each server and have them store it for you, right?
And then so you would need some way to go to this federation each of these servers later.
Hopefully in this scenario run by people who would know you in some manner.
So if you lost your phone, lost all your tokens, you could go to these things and say like, hey, I'd like to recover.
Maybe you could message them, something like that.
This is kind of like, there's all kinds of scenarios we could think of how this might work in concretely.
But basically you convince them, hey, I'm me and you have my shard of my seed and I'd like it back.
And so if they say yes to that, then they can send it back to your wallet and you can reconstitute the seed and go discover all your tokens again.
So potentially we can leverage this like local trust architecture eventually and to make like nice recovery schemes.
But this is kind of still like a research topic.
I think there's a lot of really interesting options, but it's like a fundamental trade-off that you get where like, if you end up with a seed, it is a little weird, but I think there's a lot of interesting backup potentials due to these trusted servers.
Because again, the whole point revolves around the fact that you trust the people running the servers.
That's the whole foundation here.
But that this would be like, in terms of like, where designers could contribute.
I think this would be a really fascinating thing to just think of all the different ways that this, these, these recovery schemes might work.
There was an interesting proposal in our Discord today, chat.fedimint.org if you want to go to where the developers are.
I try to come pop by the design Slack every once in a while, but I'm just on the Discord a lot more.
There was an interesting discussion have some biometric information, encrypt it and store it with the federations.
That's kind of an interesting idea.
There's downsides to that.
There's kind of a lot of interesting things and you know you could combine two of them or something.
I was just talking with Tankred today about Photon maybe using something like Photon to store the secret in the cloud.
There's a bunch of options for that.
But I think the leveraging the trust in the servers is probably the novel one, right?
Like it's different from normal key management.

Stephen DeLorme: 00:36:40

Sorry, go ahead.

Triston: 00:36:43

No, you go ahead first.

Stephen DeLorme: 00:36:45

I was just making a comment that I think that this is a powerful idea that you know I think that that'll be very appealing idea to a lot of people just the one of the most common things I'm talking to people about Bitcoin is when they learn about a recovery phrase or whatever they're like the first thing they say is there should be a forgot password request.

Justin Moon: 00:37:09

Yeah.
So that's that's kind of like ideally over the long term we could have a forgot password a flow like a forgot password.
Like, you know, there's a thousand details there.
Maybe we'll never achieve it.
But I think on paper we could get not only to something like that, but hopefully many different options.
And that's, that's interesting about FediMint is that it's technically, it's very module based.
And so this is a difference between FediMint and Liquid, right?
Liquid is like a one federation deployment.
That's very, it's exactly what they want and you can't tweak anything.
There's one federation and it works like Blockstream says it works, right?
Which is great because you know, they're, they do a good job.
But if two different groups of people would like different features, they just have to hope that the features they want get in.
And if they're conflicting, they might not.
So, FediMints is very modular.
So some deployments might use, you know, recovery method A, some other deployments might use recovery method B.
And then from an ecosystem point of view, I think it would be very interesting to see a diversity of deployments and then in the wild, discover what are the best ways of using it,, through testing, with small amounts of money and in different places, like, you can actually figure out through testing what people like rather than, having to just guess and build your one system and hope it's right.

## Backing up other user wallet metadata

Stephen DeLorme: 00:38:44

Triston, you had a comment.

Triston: 00:38:47

I just didn't have a comment.
Yes, so I was wondering if with this architecture there would be any kind of like data store.
And I guess like as I say that I realized that there might be some privacy drawbacks of doing so and the reason that I'm asking about data storage because there's some additional kind of information that a wallet may need to store, for example, labels and contact data and whatever within the mint.
And that could even be stored on, as you mentioned, something like Google Cloud or iCloud if it's using something like Photon, but yeah, there's just like a mass amount of like arbitrary data that someone's wallet within the mint might want to store.
Settings, for example, different configurations.
Is something like that being considered or is it just going to be like left for like a plugin based system?

Justin Moon: 00:40:01

Yeah so I mean on the server side like each server has a database.
And that's what basically the federation member, the servers send messages back and forth is basically to just ensure they have exactly synchronized database.
And so with the, these recovery ideas, like sending a shard of your seed to one of these servers, it would just go on their database.
And so that's kind of the interesting thing is like it already has a database.
And so for certain things like this, backing up of pieces of a seed, right?
Like you have this new design constraint, like, oh, we could stick it in that database that we've been carefully curating, right?
And so there's that.
But on the client side, on the actual, like the end user app, for example, there's not as much, like, there's not that much data required, like you have to store these tokens, but every token is like, a couple hundred bytes, like 100 bytes or something.
And so there's, and you might have like a couple hundred, you might have a hundred tokens at any given time just to be able to represent different amounts.
It's the data storage on the actual phone is very, very minimal, which is a nice.
Go ahead.

Jimmy: 00:41:15

Yeah.
Like the question isn't so much like like the capacity needed to storage capacity needed on the device but more like you know if I'm migrating to a different device I want to have like some metadata about my transactions you know and that's something that Bitcoin applications like really feel on or I want at least for my configurations to be the same and then we could extend that even further with some kind of like messaging system.
As you said, there's already some mechanism in there for that where I want to be able to through a contact be able to request a payment to someone else who I could identify within the mint.

Justin Moon: 00:41:59

Yeah, these are all great ideas.
I mean, these are totally unexplored at this point, but in order to get this in the wild, we'll need solutions for these things.
So yeah, these are things that we'll have, apps being built on FediMint we'll have to solve kind of similar to any other system.
I mean, there could be interesting ways to have the Federation servers be able to relay messages, being able to store metadata.
It's an interesting option.
It's like you can kind of think of the servers as like your own private cloud in a sense as long as you can you know there might be some system in order to like request that you can do that but it's it's the federations are like a private cloud you just can't store too much in there, right?
Because you have to have redundant copies and it's a bit of a tragedy of the commons, right?
You don't want to be uploading videos, but that is a new constraint that you could design stuff around.
But yeah, no plans for that so far.

Triston: 00:42:58

All right.
Thank you.

Justin Moon: 00:43:00

It is a great observation though.
Bitcoin wallets do really suck it.

## Checking the status of the mint or proof-of-funds

You set a new one up it's like there's nothing in here you know.

Christoph Ono: 00:43:09

I have a question it seems like a lot of user interactions between the users and the mint managers to figure out.
I would assume users also want to know, like, is this mint still running?
Are they doing a good job?
Do they have all the funds?
Is there a way to, I don't know, to provide some insight into what's going on.
I don't know exactly what to say there, but it's kind of like a proof of funds or I don't know.

Justin Moon: 00:43:39

Yeah.
So you'll be able to see if it's running very easily.
Like it'll just check whether, the phone will just send a message and it can see whether servers are offline.
In terms of whether it's doing a good job, I guess you could see whether a critical number of servers are offline or something like that.
Although I don't know how much of that information like the user would actually want to know maybe some kind of health indicator or something.
And the tricky thing is in terms of like you can't ever really know whether a mint is properly collateralized or not, right?
Like the software, if running correctly should never allow, like basically if it discovers that anything was created or destroyed, like if stuff doesn't add up to zero in any given epoch like a block, it will just stop.
Right.
So but you could have something that looks like federation servers, but some malicious person modified the code to print tokens out of thin air, for example.
And so, yeah, that's like a fundamental problem that there's no way to prove that the mint is properly collateralized just because like, you can't see the liabilities because that's where the privacy comes from.
One solution here is something like automated bank runs.
Just like every once in a while I'll see like, hey, let's just everyone try to exit and re-enter the mint, for example.
Something like that would be kind of interesting.
You know like that Lightning gate with the LSP for example could you know could attempt that just like can I get my money in and out and publish for proof that they did?
I don't know.
There's probably other options here, but yeah, that's like one of the drawbacks here is you can't really, you basically trust that the Federation is not screwing you over.
It's a trust system that they're not not under collateralized.

Stephen DeLorme: 00:45:45

That just the idea of the automated bank run is really wild that just the idea of like having this like what if you have some kind of like third-party lightning node that's like trying to hold the mint accountable for the community It's like constantly like they have enough, Bitcoin in the lightning nodes so that they can constantly like at random times try to like make obscenely large redemptions just to kind of keep them honest.

Justin Moon: 00:46:15

Yeah.
Yeah, there's a lot of thinking there, but it's kind of one of these ideas where everyone's like, oh, inflation is bad, right?
They all think inflation is bad.
They get into Bitcoin.
It's like, wait, maybe inflation isn't bad.
It's kind of one of those ideas.
Well, maybe a bank run is actually a good thing, right?
Like frequent bank runs are good.
It just proves that it proves solvency, right?
Like that's the real way you can prove solvency.
Everyone can get out and get back in.
Right.
Maybe it's maybe this is not a priori bad thing.

Stephen DeLorme: 00:46:43

Reminds me of the first chapter of Cryptonomicon, the book takes place in some small town in China.
And it's like as the book is opening up, it's like Friday afternoon.
And every Friday in this town, all the banks perform a bank run.
And they send people all around town carrying boxes of cash just to see if they can get their gold out and all the banks do it to each other.

Justin Moon: 00:47:04

It's a sign of an advanced civilization.
You can get your gold out.

## Hypothetical: remove some privacy features and add more proof-of-liabilities

Justin Moon: 00:47:08

But I mean, as I should mention also that like FediMint is interesting.
Like if you didn't have the private, like if you removed some of the privacy features, you could do much more.
You could make a better attempt at proving liabilities as well.
And so like, that's something that will be fun to experiment right like could you do just a purely kind of custody optimized thing like optimized for holding as opposed to spending right and so like you could kind of have a savings you could have a fed amount with a savings account and checking account, right?
The checking account has blinded IOUs where they're indistinguishable.
Maybe the checking account or the savings account does not have blinded IOUs. It's just plain text IOUs. And so these could be published at any time.
You could check whether the mint is publishing.
Every wallet could check whether the mint is publishing their IOUs. So like all the clients would keep that mint honest.
Like they tried to publish a proof of liabilities and that user's liability wasn't in there.
They could, send a message around to all the other users being like, hey, we're being cheated, something like that.
Then, this is like a theoretical feature, but like, that would be doable.

Stephen DeLorme: 00:48:46

Yes we're getting pretty close to the hour here.
This has been a fascinating conversation.
I want to just kind of open it up to the room again and just kind of see, I mean, I could probably talk about this all day, but I just want to see if there's any kind of like, designer level questions about what kinds of work needs to be done on FediMint or how certain things might work.
Any other questions from the room here?

## What should the initial setup of a FediMint server look like?

Justin Moon: 00:49:17

Well, I will mention one other thing just based on my experience where like, I was saying, this would be a good problem for designer is like, what should the initial setup be when you run the server?
Right?
Like, just to get because I wanted to if you think of be put be negative here it's like how would this fail well one reason this would fail is because it's an awful lot of running the servers right which people aren't good at right like people aren't good at passwords people aren't good at servers and so making the server setup here is like there's a technical component we're trying to solve.
We're trying to make the software like really easy to run, but there's a design problem too because you know you need to run the software and a little web page will show up and it'd be like, okay, who else?
Where you know what are the addresses in the public keys of the other servers, right?
Like there's a big life customer lifecycle there and then okay, once the server is up and running, what's the first step?
Like what's the first like win you get, you want your user to have like a win, right?
So like how do you get to the point where they can send their first Lightning payment, right?
Or receive their first, something like that, deposit the first, like that sort of life, customer life, lifecycle, whatever you call it, is like some design thinking would go a long ways there, because it's currently just developers thinking about it, mostly.

Triston: 00:50:32

Is it going to just rely on AWS at that point?
I mean, I don't know if you remember this old tools like fantastical and cPanel where you would like one click install WordPress or some...

Justin Moon: 00:50:35

Yeah I think it'll be diversity right like I think there will be really easy setup hopefully we can get to it like having really easy setups in stuff like Umbrel, RaspiBlitz, some of these things where people are already running.
It's helpful for people who are already running one but it's also like if you want to have like your own self-hosted server it's probably like your own hardware it's probably easier to set that up from scratch and try to attempt it yourself so that's one option another option is like I think it's been very a BC space had a lot of success with like Luna node, right?
So they built a little series of configuration forms.
You'd set up a VPN or VPC and then it would fire up a little configure or no, there was like a couple of forms you'd fill out and that would actually fire up the VPC, like the cloud server for you.
And then, like 10 minutes later, you'd see a little web form at that URL that would be like, okay, initial block download is happening.
I think something like that would be very successful.
And it's also nice.
It's not like there are benefits to not being on AWS for this because you know like a lot of these like Luna node you can just pay with Bitcoin right like you don't have to go through a whole you know maybe it's harder to be censored on something like that some of these niche ones and you know something like AWS and some of these are good too, because it's, people are really familiar with it.
So I think some federations could have a mix, right?
Hopefully, someday it can be like people's own hardware, but that's just we don't live in that world quite yet.
But I think, some of these Bitcoin companies like Start9, Umbrel, they're helping us get to that future.

## There can be many FediMints and each can try different design patterns

PW: 00:52:22

I think on that point I'll just add something from sitting in the telegram group and trying to ask, like answer a lot of questions on this.
Like one of the common misconceptions people have when they come into this is that it's called FediMint so there is a FediMint when the actual fact is there's probably going to be thousands to hundreds of thousands of these things and they're all going to vary depending on the particular group that you've set it up for.
So there's quite a large design space for looking at all of these different problems and how you might actually go through them.
So there's those questions earlier about a guy who's setting up masts in villages in Tanzania to blanket the local area with network connectivity, how would that work and what are the different failure modes that come to that.
It's pretty interesting from a design point of view to look at the many variations of, like backups for instance.
There's not necessarily going to be one answer to that there could be the backup for your mum versus the backup for your friends versus the backup for your local community might just be quite different so there could be like a good recipe list of stuff that can be developed.

Justin Moon: 00:53:34

Yeah.
From like a high level, you can think that like Bitcoin and Lightning are kind of haunted by this problem where like everyone has to agree on a change, right?
Like more or less, right?
Everyone has to agree on a Bitcoin software.
Basically everyone has to agree on like a big Lightning protocol thing like bolt 12 or something right because everything has to be interoperable.
FediMints don't have to be interoperable on their own.
They can use lightning to interoperate right so like the different FediMints can be very very diverse as long as they can speak lightning for whatever things are expressible in terms of send and receive or maybe other lightning features eventually.
Those things can be interoperable between mints, but like you can have a lot of diversity between them, which is really exciting from a design point of view.
Also from a developer point of view, right?
Like Bitcoin, Core Lightning developers sometimes aren't the happiest folks because you know, it's so slow to get your stuff accepted.

Stephen DeLorme: 00:54:27

It's almost like the farther away you get from the main protocol, the more wild and experimental you can get.
Bitcoin development has to be very, very conservative and it has to be very slow because you're talking about the world's money supply.
And then when you move a layer up on Lightning, you can be a little bit more reckless there because you don't have to worry about if you try some experimental new technique for a channel and mess something up, it only hurts you and your channel partner, doesn't hurt the rest of the network.
And then you could take that even, I know you also consider a fedimental layer too.
In my mind, I keep thinking of it as kind of a third layer, just because I think of the FediMint is using lightning, that may not be technically accurate.
But if you think about moving layer above that with FediMint each federation could just completely do its own thing.
And then they can be interoperable because of Lightning.

Justin Moon: 00:55:18

Yeah, I guess I mean the terminology never really goes anywhere, there's an endless bike shed, but I think it's kind of a peer to Lightning, right?
Like they can talk to each other, but they also both access Bitcoin directly.
And yeah, I think it's just a compliment to Lightning, right?
The things that, yeah, it's very complimentary, which is exciting.

Christoph Ono: 00:55:45

It seems like from a design, from a UX perspective, it might make sense to just focus on one good the most what what likely is the most common use case and just try to think through that so I think otherwise it gets a bit bit hard to come up with a specific experience.

Justin Moon: 00:56:04

Totally.
I think I mean one thing that every single federation will need is they'll need the ability to set up servers.
And so that's like even before like that from a design perspective that would be that flow of how to get the server up and running and how to get it so they're talking to each other.
And then also how to do the first deposit because in almost every one of these systems, you're going to need to get some Bitcoin in and there's some steps there.
That would be a really interesting thing to get some design feedback on, because it would be shared by every single thing.
And I also believe just one simple use case is also desirable.

## Different types of users for FediMints

Stephen DeLorme: 00:56:43

So it's almost like you're kind of considering two different types of users here.
So one is the actual federation operators and trying to make their life a little bit easier, trying to help them actually get the federation set up so they can get up and running with it.
And then you've got this other class of user which is the actual federation like the I guess what we normally think of as being the end user the person who has the wallet app on their phone who's actually trading e-cash with their neighbors for goods and services.

Justin Moon: 00:57:15

Yep.
So from that point of view you know it's like Lightning, you need the actual node running first.
And then, the people, you know, it's complicated.
It's a potential failure.
If it's hard to set up servers, then no one ever gets to the privacy benefits, right?
Not enough people.

Stephen DeLorme: 00:57:32

And it seems like there's almost a couple of different ways that this user could get get their first Fedi wallet.
Like, you know, it could be someone who already holds Bitcoin.
They're like, I want to deposit some of this with the mint and get this kind of privacy shield, get my e-Cash tokens, where somebody else could be starting from absolute zero.
Someone could say, hey, I want to pay you.
I want to pay you in e-Cash.
Is that cool?
Download this wallet.
And they're starting from completely zero.
Maybe they've never even touched Bitcoin or Lightning before in their entire life.
Maybe they've used, Venmo or something like that.
Or maybe this is their first experience with any kind of digital interaction around money to begin with.

Justin Moon: 00:58:16

Yeah, I know there's an interesting point of view, like, we think where does a circular economy come from?
Well, it's probably not going to be people buying the money.
They're probably going to get their hands on the money in a different way.
They're probably going to earn it.
Maybe it's remittances.
Maybe it's something else.
But it's probably not going to be buying it.
I think the circular economies will emerge through actual usage probably.
And so that's like an interesting thing about this too, is like, if you can get, since it's kind of like naturally like a community local thing like it might you know if you can get the buy-in to actually run one of these keep it up and you know have the interaction between all these people maybe that actually helps form a circular economy as well you know.
No one's really succeeded there yet so it'll be interesting to see.

## Closing

Stephen DeLorme: 00:59:13

Well this has been so awesome.
Thank you so much Justin.
I think we're a little past the hour here.
So I want to be respectful of Justin's time and kind of formally end this, just that he feels free to go.
But if people want to hang out and keep chatting in the channel, please feel free to do so.
But we'll go ahead and consider this the formal end here.
And thank you so much, Justin, for taking time to share all this with us.

Justin Moon: 00:59:36

Yeah thanks it's fun to talk to you guys you know it's fun to have the designer point of view and everything.
I get code brain right now so I just think of everything in terms of how it works and then you know It's really nice to see the diversity of opinion.

Stephen DeLorme: 00:59:51

And so if anybody's interested in FediMint, just go join the FediMint discord.
I think this is the fediment.org website.
I'm assuming there's a discord link on there somewhere.

Justin Moon: 01:00:02

Yeah, chat.fedimint.org.
We should probably feature it a little more.

Stephen DeLorme: 01:00:08

So that's where you'll go if you want to.

Justin Moon: 01:00:10

Yeah.
I'll also try to get a couple more people from over there to hang out in the design discord too because you know it's a lot or the design slack because there's I see a lot of interest here so we'll try it out be a little more responsive.
I show up there like once a week so I'll try to show up a little more frequently.

Stephen DeLorme: 01:00:27

Awesome.
Well, thanks Justin and yeah, Christoph, could you go ahead and cut it off here.
