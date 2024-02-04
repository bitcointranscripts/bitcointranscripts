---
title: "OP_VAULT Round 2 & OP_CTV"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://www.youtube.com/watch?v=h4ReIIapN8Y
tags: ['vaults', 'op-checktemplateverify', 'dlc', 'soft-fork-activation']
speakers: ["James O'Beirne", 'Greg Sanders', 'Rijndael', 'NVK', 'Ben Carman']
categories: ['podcast']
date: 2023-05-11
---
## Introductions

Speaker 0: 00:01:25

Today, we're going to get back to OBVault, just kidding, UpVault, this new awesome proposal on how we can make people's money safe in the future.
And in my opinion, one of very good ways of scaling Bitcoin self-custody in a sane way.
And with that, let me introduce today's guests, Mr. James.
And welcome back.

Speaker 1: 00:01:32

Hey, thanks.
It's always good to be here.
This is quickly becoming my favorite Bitcoin podcast.
It's not official yet, so don't, you know, go bandying that about, but we're on the road.

Speaker 0: 00:01:43

If I knew you only took to invite you a couple of times here.
I mean, I have done that earlier.
Mr. Rindell.

Speaker 3: 00:01:51

Hey, good to be back.

Speaker 0: 00:01:52

Welcome back.

Speaker 3: 00:01:53

Yeah, thanks.
Good to be here.
Greg.
Hi. Sometimes a listener, first time caller.

Speaker 0: 00:01:59

For the people that don't know you, you want to just give us the elevator pitch on why you're here?

Speaker 3: 00:02:04

Yeah, so I just I've been working with James a little bit on this OpVault proposal and that's why I'm here.

Speaker 0: 00:02:11

Glad to have you.
Ben DeCartman.

Speaker 4: 00:02:15

Sup guys, happy to be here again.
Big fan.

Speaker 0: 00:02:18

So guys, a lot has happened in OpVault since we had you here.
I think it was episode 23.
And at that time, you had not even made the BIP public yet.
So a lot changed.

## Primer on OP_VAULT

Speaker 0: 00:02:35

So, James, do you want to just sort of like first give the people who may not know what OpVault is, just give us like a quick primer on it and then we can get into a bit of, you know, what changed and everything else.

Speaker 1: 00:02:47

Yeah, for sure.
So it's no news to anybody that everybody using Bitcoin is to some degree concerned with custodying.
And custodying is notoriously hard because it basically amounts to keeping key material both accessible and out of the reach of people who want to steal your Bitcoins.
So that's that's really hard in the general sense.
But luckily, Bitcoin script gives us a lot of ways to potentially mitigate the difficulty of that.
And so for a long time, there's been this idea floating around of vaults.
I think the earliest mention I could find was 2013 in some Bitcoin talk forums.
And the basic idea with vaults is you can lock up your coins in such a way that they're still spendable by you, of course, but if you want to spend them somewhere, you basically say beforehand, okay, when I spend this coin, I'm going to wait some period, whether that's 10 blocks or two days, whatever it might be.
And you publicly declare the intent to spend that coin to some particular destination.
And during that period, you can come in and say, oh, wait a second, I don't recognize that spend, or I didn't mean to do that spend, or NVK backdoored my hardware wallet, and so now I want to recover those coins or claw them back or cancel that transaction.
And so that's the basic idea of vault.
It's a really, really powerful concept.
I think it's something that almost everybody would wanna do in some form if it were costless.
But the problem has been that it's not costless, especially kind of the way that Bitcoin is now.
You can kind of emulate this behavior, but it requires doing a bunch of operationally complicated things like generating these temporary keys that you use to pre-sign this whole graph of transactions that kind of fixes your coins into a known flow.
You have to worry about all kinds of things there, like deleting that temporary key that you used or else somebody can backdoor and disrupt your flow.
You have to worry about fee management.
You have to worry about fixing addresses that the coins ultimately flow into.
So if you're a really, really big company, maybe you can do this and maybe you can eke out some security benefits.
But if you're an individual or you know kind of a smaller operation it's really not as practical.
So I've been kind of involved in various custody efforts including my own for a while and I've been thinking about how to use vaults and I did like a very simple implementation using OPCHECK template verify And this makes vaults kind of more achievable, but there were still some downsides.
Basically, OPTCHECK template verify is just a way of saying, hey, we're gonna lock these coins up and they're spendable into this particular set of outputs with like no signature or anything else.
And it may be kind of counterintuitive, but you can use that to create these like pre-existing graphs of transactions that are allowable.
So you can use that to create the vault structure without having to do this, this temporary key thing.
So operationally it gets a bit simpler.

Speaker 0: 00:05:51

Can you, I guess, like, since we're crossing a little bit in CTV here, which is like a whole other can of worms.

Speaker 1: 00:05:57

Yeah, and we'll get into that.

Speaker 0: 00:06:00

Do you want to give us a sort of like, without CTV, like if a little bit of like technical explanation of like how the vault is created, right?
And then the trade-offs and then maybe like, okay, now if we use CTV, like how the vault is created and what other set of trade-offs are we getting?

Speaker 1: 00:06:17

Yeah, for sure.
So in Bitcoin today, if you want to create a vault, you have to decide the allowable flow of transactions.
So you might say, OK, we're going to pick this wallet that.
So we're going to pick a few things to start with.
We're going to pick our recovery path or like our super secret nuclear cold wallet that's kind of going to be used to interrupt any unexpected transaction.
We're going to pick our like warm wallet that's going to be used to actually initiate the withdrawal that can be then interrupted by the recovery wallet.
And with Bitcoin today, if you're going to do this, you have to pick your target ahead of time.
So like when we start the withdrawal process for this vault, which wallet are the funds actually gonna flow into on their way to the final destination where you actually kind of want to put the Bitcoin, you know, whether that's sending it to somebody or uploading to an exchange or whatever.
So you pick the various parameters that are involved.
And then what you have to do to actually get this behavior in Bitcoin today is you have to decide on what all the possible flows are of funds.
So that might be, OK, I want to create a path where I'm putting in 10 Bitcoin to my vault, I wish, right?
And then I'm going to allow, you know, a withdrawal of five Bitcoin at a time, or I'm going to allow a withdrawal of, you know, one Bitcoin at a time.
So you basically have to decide on like what the structure of this vault is going to be.
And then you have to generate this temporary key, this ephemeral key.
And what you do is you send your Bitcoin to this ephemeral key, you pre-sign this whole flow of transactions, kind of whatever you come up with, and then you delete that key and you make sure that nobody else can ever use that key to spend Bitcoin because if they did, they'd have a backdoor into your vault.

Speaker 0: 00:08:17

Yeah.
And then we have this question, right?
Like, how do you prove that you deleted a key, which is nearly impossible.

Speaker 1: 00:08:23

It's literally impossible, you know, to prove to yourself, to prove to auditors, whatever.
So like, you know, You can come up with schemes where you have a pretty good assurance that you deleted the key and you know, so maybe you're comfortable with that, maybe not.

## How is CHECKTEMPLATEVERIFY achieved?

Speaker 1: 00:08:37

The advantage of then using check template verify or something like it, you can use any prev out.
But basically what you need is a way of at the consensus layer on layer one, locking the coins to travel a certain path.
And that's all CheckTemplateVerify does.

Speaker 0: 00:08:55

How is that achieved?

Speaker 1: 00:08:57

So what you do is, what CheckTemplateVerify says is, it has one argument, which is the hash.
So you do like in your script, you know, where in your script you might say, hey, I require a signature from the private key that has this corresponding public key.
The way that CheckTemplateVerify works instead is like, hey, I require the outputs and some other information about the spending transaction to look this way, to hash to this value.
So it basically just uses one half of what's called the SIG hash right now.
It uses basically the output side of the SIG hash as well as some other stuff to just lock some coins into being spent into a particular set of outputs.
But then what you can do is, maybe the programmers out there will start to follow, You can recursively use check template verify to build out this like tree of transactions that you're pre committing to.
And it turns out you can use that technique then to build a vault that removes the need for this temporary key.
So you get rid of the key deletion problem if you actually use check template verify.
And you also get rid of the need to persist all the signature data for your pre-signed vaults.
Because if you're doing vaults right now in Bitcoin, and you're pre-signing this big graph of possible transactions that you can use to actually make the funds move, you have to save every single signature that you've created because it's essentially a bearer asset that's controlling the Bitcoin.
So if you lose those signatures, your Bitcoin is gone.
Whereas in CheckTemplateVerify, like the signature is just the content of the spending transaction.
So you don't actually need to save the signatures.
You just keep track of the parameters you used to generate this graph of transactions.
So CheckTemplateVerify actually does make the vaults on its own.
It makes vaults quite a bit simpler operationally.
But where it still falls down is in CheckTemplateVerify, it's very, very constrained because you have to spell out exactly what the nature is of all the outputs that you're going to be using.
And so you have to decide on which wallet you're actually unvaulting to.
You have to decide on what kind of fee rate you're paying or what your fee structure is.
Like maybe you have some, you know, child pays for parent outputs.
So you're still kind of locked into a very particular flow of funds, a very particular set of parameters.

Speaker 0: 00:11:25

Right.
So I mean, do we still need the nuclear key, something that we have a full backup from on CTV, I guess that's not possible, right?
You're now truly committed to that template and to what comes out of that, right?
You no longer have your nuclear option really.
Is that right?

Speaker 1: 00:11:46

So you still, with CTV, you still have your like recovery path.
And in fact, like in CTV, you could have a little escape hatch where you say, okay, at any time I spend the full balance of this vault to, you know, a certain, a certain key pair Like CTV lets you do that.
So CTV really lets you do anything.
All CTV makes you do is kind of pre-commit to how the coins can be spent.

Speaker 5: 00:12:11

Well, and because of Taproot, you could have a tap leaf that's like, you know, anything you want with a particular key or with, you know, some quorum of keys or something.
So you could say, I'm going to do a CTV spend path for like my normal spending paths, but then I have some other tap leaf that's, you know, unencumbered, except by like normal checks of operations.

Speaker 0: 00:12:33

But that's only if you're using Taproot.

Speaker 1: 00:12:36

No, no.
Well, even so Taproot makes it more efficient, but even before Taproot, you can still have conditional scripts.
Right.
And so with CTV, you can still kind of lock in those conditional scripts and say there could be any number of spend conditions.

Speaker 0: 00:12:51

Okay.
So what you're saying is now like your proposal is sort of like, it's kind of still the same, but you're added the fact that now if you have CTV on it, right?
I mean, you can make the vaults more usable and more realistic and sort of, you know, not make them so convoluted as they were before because of the ephemeral key issue.

## Fee issues on CTV

Speaker 0: 00:13:12

How are you resolving the fee issues on CTV?

Speaker 1: 00:13:17

Yeah, yeah.
And so to be clear, we're still talking about like history.
This isn't anything to do with the new vault proposal.
This is kind of like how we got to the new vault proposal.
But so yeah, you know, fee management's really an important thing to worry about when you're thinking about vaults, because you're locking coins up for potentially, you might leave these coins in this vault for years and years and years, you might withdraw it next week, but it also might stay there for a long time.

Speaker 0: 00:13:43

Other years.

Speaker 1: 00:13:44

Yeah, Yeah, exactly.
And so if in the meantime, the fee market's gone crazy, as maybe we all hope it will in some sense, and fees are much, much higher than when you initially created the vault, you can get into a lot of trouble if the fee rate that you actually put onto these pre-formulated transactions isn't high enough.
And so one technique that you can use is basically locking in some outputs that are just used for fee control.
Like you could have a sort of a dummy output that maybe anybody can spend or you know goes to a.

Speaker 5: 00:14:22

Would that be kind of like an anchor output or something?

Speaker 1: 00:14:25

Exactly.
Yeah.
Exactly.
Like an anchor output.
But the downside there is that right now with the relay policies in Bitcoin, if the transaction that you're trying to fee bump with an anchor output has too low of a fee rate, you can't even broadcast it in the first place.
So I don't want to get too deep into mempool stuff unless you want to get too deep into mempool stuff.

Speaker 0: 00:14:45

We can do that later on.

Speaker 1: 00:14:47

But the point is, fees are really hard.
And with our relay policies today, it's still almost a non-starter for CTV based vaults.

Speaker 3: 00:14:57

Yeah.
Can I pipe in just real quick?
So there's kind of two ways of bringing in fees real quick.
One is people call it bring your own fee where you add an input and a change output.
Right.
So you can add this dynamically.
And the other is child pays for parent where again, you have this anchor and you spend it.
So basically for James Obfolt idea, He had to kind of shoehorn one of those ideas in there.

## How has the proposal evolved?

Speaker 0: 00:15:20

Okay.
So do you want to tell us now, like how the proposal has sort of like evolved and like where we are at now and how's it looking?

Speaker 1: 00:15:30

Yeah.
Yeah.
So let me just like reframe a little bit and emphasize the conversation's gotten really complicated really fast.
And maybe a lot of people are wondering like, why the hell are we going to all this trouble?

Speaker 0: 00:15:40

That's okay.
They're smart enough if they're listening to this.

Speaker 1: 00:15:43

Yeah, yeah, yeah.
But there's some really cool, I mean, like if you think about having this divorce between recovery keys and like your warm key or everyday key or whatever, you can do some amazing things.
Like you can generate offline keys that are only on paper and only get exercise in the recovery path, in the unlikely recovery path versus your everyday stuff.
But anyway, so all that to say, I think it's really important use case.
So we came up with this proposal, OpVault, which takes CTV and builds on top of it.
Initially, I just came up with a completely separate thing that was the simplest thing that achieves vaults, but then I realized that that actually encompasses CTV as Ben pointed out on the mailing list pretty quickly after I put the proposal out there.
But so yeah, last time, since last time I came on here and was talking about Vaults, Greg and AJ have really made some substantial improvements to the proposal in the sense that when I designed it, It was kind of from a naive standpoint.
I haven't done like a tremendous amount of scripts, certainly not as much as Greg has.
And I kind of came at it really just like kind of designing for one particular use case for vaults, which I think is pretty general, but it doesn't compose well with like the rest of Bitcoin.
So it introduced a lot of like weird requirements for changes to the script interpreter that like aren't that like long in terms of lines of code, but conceptually, they're pretty big changes.
Like I had this thing where you commit to the recovery path that you're going to use by hashing a script pubkey and then later on presenting a script pubkey.

## Simplification of OP_VAULT proposal

Speaker 1: 00:17:26

So there's just like all this kind of Additional stuff that I had to introduce but Greg and AJ kind of found a simpler way That's more idiomatic to taproot that really I think simplifies and makes the proposal more and more composable Greg do you feel like you want to like talk a little bit about what your thought process was there?

Speaker 3: 00:17:48

Yeah.
So like you were mentioning, there's some stuff that wasn't what you call Bitcoin script idiomatic, right?
And so kind of, I looked at this first, I think the first thing I did was how to incorporate taproot to it.
Cause I think the original one didn't even really incorporate taproot.
So I did that first and then I still wasn't super happy with the abstraction.
And then I kind of sat there for a couple hours or something like that, just trying to make it more taproot idiomatic, actually.
And I came up with kind of the halfway step measure, which is saying, you know, let's use the tapstructure to kind of flex the conditional kind of script we actually want, this recovery versus unvaulting path functionality.
And that's where I came up with this forwarding idea, where you take such a script you want to forward this to as the staging area, and then leave everything else the same.
The recovery path just stays there, doesn't get changed.
But everything else gets the trigger path gets changed.
And then from there, once AJ read that, he went and went even further with kind of making the, this forwarding script more, compose even further composable resulting in kind of this, T love tap leaf update, verify like mechanism, which is pretty nice.
Yeah.
Too.
And then, we called it flu at the time forward leap update, but, then it became backer named to

Speaker 1: 00:19:17

COVID.

Speaker 3: 00:19:17

Yeah.
I've COVID up up five G to, that, That is now what we call up vault right so the vault part is the part It's kind of putting this value into the staging area with this forwarded script

Speaker 1: 00:19:32

Mm-hmm and so like Greg was saying the composability got a lot better and the way that that kind of manifests is when I presented the original proposal, Luke Jr. On the mailing list piped in and he was like, hey, you know, okay, this is all right.
But what if I want to say lock my coins up in a vault and then instead of, you know, triggering a withdrawal to certain outputs, what if I just want to delegate the coins to a new key?
And the new proposal actually like facilitates that use case because instead of necessarily like locking in use of say, CTV or any particular like triggering process, it actually allows the wallet designer to specify that triggering process as the script template that gets this update verify thing.

Speaker 3: 00:20:25

Yeah, so the trick here is it can forward to any single key.
So this covers any time you can aggregate a key.
So think music two or frost or something like that, or single, just a single normal key.
But this is where we're really hitting limits in the Bitcoin script kind of design is where it's very difficult to compose it further without kind of a radical upgrade to Bitcoin script.
So it's kind of like that's kind of like the limit we're hitting there.

Speaker 1: 00:20:51

But I think it's in a really good place in the sense that

Speaker 0: 00:20:54

it solves the problem.

Speaker 1: 00:20:55

It solves it.
It really it just obliterates the problem in a way that I think is going to be like very, very useful.
And it's like simple.
It's It winds up being simpler than the original proposal, which is great.

Speaker 5: 00:21:07

Well, and having it composable means that if you're trying to write some more complicated policy in something like Miniscript, being able to incorporate fault in there without having to like throw out all that tooling.
And, you know.

Speaker 3: 00:21:20

It also probably composes better with things like Miniscript because now it's, I need an authorization policy on this state transition.
Just add it, right?
There's no, I don't have to read the spec to know I can do that.

## Script libraries and CTV templates

Speaker 0: 00:21:34

Okay, so what's the expectation here?
Are we gonna have like, you know, like, I mean, cause Miniscript is already kind of like that.
Are we gonna have a miniscripttemplates.org where you go and you find like, you know, 10 different safe scripts, because people will fuck this up.
I mean, people can barely serialize and un-serialize stuff with JavaScript, right?
So is this like the future we see where like there is like essentially banks of scripts that people can use And then there's the ones that maybe like the wallets are going to have like two, three things that like, here, you can do this with your coins.
Is this sort of like the, because you can order corporate enterprise for a second, right.
That has, you know, budgets and people that can audit things and can come up with new ideas.
I'm talking about like 90% of the people who actually even have coins to do this.
Is this sort of like template libraries, how we see the future going?

Speaker 1: 00:22:28

I just think it's It boils down to wallet developers, right?
Like no user of Bitcoin out there is like, I'm not sitting here writing mini scripts to manage my coins and I'm a core dev.
Like it doesn't work that way.
You use some wallet software that you trust, hopefully that you've vetted somehow.
And so I think really when you're working on a proposal like this, you're thinking about how can I make it easy for wallet developers to actually adopt this stuff and implement it safely?
And yeah, and like the guys are saying, how can I mesh with the existing ecosystem things like mini script and output descriptors?

Speaker 0: 00:23:05

OK, so I mean, you know, output descriptors just seem to be like now the show.
And then we got into mini script was essentially like just a fancy way of doing output descriptors.

Speaker 3: 00:23:15

Yeah, it's a super set.
They fall under the same umbrella now, apparently.

Speaker 0: 00:23:20

Yeah, I mean, we're going to have now, what, like, CTV templates, right?

Speaker 5: 00:23:27

Yeah, well, it's like, you know, output descriptors are C, right?
So like script is assembly, output descriptors are C, we now have Python and so eventually we'll have JavaScript.

Speaker 3: 00:23:36

So also the good news is Jeremy Rubin already has a branch of Miniscript with CTV.
So he's already done that hard work

Speaker 1: 00:23:42

for us.
And the CTV stuff is dead simple in terms of coming up with the templates.
It's like a eight line Python script basically.

## OP_VAULT criticisms

Speaker 0: 00:23:52

So, you know, I can picture this future.
I can sort of like be pretty excited about it, but at the same time it's like, okay, holy shit, we're adding all this complication to Bitcoin now.
You know, and, and some of these concepts have been sort of like heavily debated and have a lot of contention.
So, so maybe like, let's start sort of addressing some things and sort of exploring this a little, because, you know, the original OpVault was like, Hey, look, I have this simple new primitive, right.
That like, you know, like, please let's activate this kind of thing.
Right.
And then now it has sort of like expanding, like all software studying and development happens.
It's always like that, right?
I mean, new people come in, some give good ideas, some give bad ideas and sort of like it mashes up and then you sort of like start evolving, evolving and evolving, especially in Bitcoin because that part of the development is fairly academic, right?
So, CTV was essentially dead.
And there's a lot of cool stuff in it.
There's a lot of scary stuff in it.
Nobody so far has been able to show me what's actually bad about it.
So, why don't we sort of like maybe still men some criticisms and then try to sort of break it down because you know I think that by opening CTV up like essentially opening up this proposal to to more grief even though it might be the right solution.

Speaker 5: 00:25:19

So I feel like we have to start with the classic covenant FUD, right?
Which is like, okay, so and maybe for folks who haven't listened to all the other prior episodes, whenever we're talking about covenants, you know, the way that Bitcoin works is when you have a transaction you're spending inputs and you are unlocking those outputs and then you lock them to a new set of outputs and All of the restrictions that we can put on Bitcoin are restrictions on how those coins are unlocked, like on the input side.
And so covenants let you put restrictions on the output side.
So it's not just how they can be unlocked, but it's like where they can be spent.
And so CTV is a really, really simple covenant scheme.
There's more complicated covenant schemes.
OpVault is a covenant scheme, right?
You're saying when these coins are spent, they can only be spent into this holding zone and then after six months, eight blocks, whatever you specify, then they can be sent somewhere else.
So the classic concern that people have is, okay, if there's a way of saying these coins can only be sent to certain destinations, then what if I go and withdraw from an exchange and the exchange sends me these tainted coins that can only be sent to like white listed addresses and this is how the state is going to lean on regulated exchanges and make it so that I end up with like Chinese social credit score Bitcoin that I can only send my Bitcoin to People on the approved list and if I you know eat too much beef or something then then I can't spend my Bitcoin This is like the classic as soon as you say Vault CTV like I asked on Nostr before this episode like what what questions should I ask James about op fault?
And I got two answers and one of them was about this

Speaker 0: 00:27:13

All right.

Speaker 5: 00:27:13

So like this is this is where everybody goes

Speaker 0: 00:27:15

so specifically about beef

Speaker 5: 00:27:17

Specifically beef.
It's all beef and Bitcoin.
So the concern is, you know, I'm going to hit withdraw and the coins that I get are going to have these restrictions on them that I did not opt into.
That's going to control how I can spend my Bitcoin.
And it's no longer my Bitcoin.
It's my Bitcoin at the pleasure of the exchange or the state or whatever.

Speaker 1: 00:27:37

Right.
So and the obvious counter to that is that like covenants are a really bad way to do that.
And in fact, today you can do that with multisig.

Speaker 5: 00:27:44

Terrible way.
Yeah, I

Speaker 0: 00:27:45

mean, multisig would be a lot better.
It would be a lot better.

Speaker 1: 00:27:48

That's right.

Speaker 5: 00:27:48

For a lot of reasons, right?
So one of the problems with covenants is you have to go and figure out all of these conditions in the future when things get changed.
So if you have your allow list or your white list of where these coins are allowed to go.
Every time you update that list, you have to go and like recompute the covenants and you have to get everybody to like reroll their coins.
It's a lot simpler if you just say, hey, your coins are now in a two of two multi-sig and I have a co-signing Oracle and my co-signing server will refuse to sign a transaction with you unless they're going to an approved destination like that's that's how you would actually build Fedcoin.

Speaker 0: 00:28:27

Also like how is the exchange going to make this happen?

Speaker 3: 00:28:32

They can't, so that's the point.
You hand the exchange an address, This address commits to all the spending conditions.
So don't include those spending conditions.
And you're okay.
Right?
And if they don't send it there, then they didn't pay you.
That's the end.

Speaker 0: 00:28:46

Yeah.
I mean, you're still like, you know, holding the bag next.
I mean, it's still yours and Bitcoin is very good that way.
So you're already pre defended against, against deeds.
Let's put it this way.
Unwanted new deeds on your coin.
Ben, I think you want to add something?

Speaker 4: 00:29:03

Yeah, I think the only way they could actually build that is by building their own wallet.
But at that point, just make it all custodial and you get the same benefit.
And it's cheaper.
So there's really no reason to ever do that.

Speaker 5: 00:29:17

The thing that Greg just said I think is really important, and it's a fundamental misunderstanding that I think a lot of people have about how Bitcoin works that leads this concern.
Which is the address that you generate commits to the spending conditions for when those coins can be spent.
So if you generate a normal single SIG address, what you're generating is an address that's an encoding of the hash of the public key that you're going to use to unlock those coins.
And so anytime that you want to have your coins encumbered by some script, you have to commit to that script when you generate the receive address.
So nobody can like push coins to you that commit to some script that you don't know about.
Your wallet has to generate those conditions in order to generate a receive address that commits to them.
So just don't do that.

Speaker 0: 00:30:07

I guess like the next one sounds kind of, you know, kind of silly, but, Oh my God, recursive stuff, right?
Like are we at OPIVO again?

Speaker 1: 00:30:18

Right.
Right.

Speaker 0: 00:30:19

You know, What are the issues that we could have here?
Or at least what are the, there really is no issues, but like what are the perceived issues that we could have here if we have like recursive things happening in the base layer?

Speaker 1: 00:30:34

Yeah, so I think there are two kinds of concerns with that.
The first concern is, oh no, what if I get coins caught in some infinite loop and they can never escape from this this dumb covenant that I wrote?
And my answer to that is kind of like, well, you can burn coins in a number of ways today.
So like, feel free to burn your coin.
But the second more nuanced and definitely the thing that I worried about with covenants when I first encountered them was what kind of like on-chain contagion could you see?
Like, are you going to like, We don't want to go anywhere near having Ethereum-like execution characteristics on-chain in Bitcoin.
That's obviously nobody in the right mind wants to do that.
And so if you talk about, you know, the thing that scared me when I first started hearing about covenants was this unbounded opcat execution, where you can just have the script interpreter go crazy because it's trying to do this really complicated thing and maybe blowing up in space or time or whatever.
And I think that's a completely legitimate concern and something to look at.
The irony, I think, specifically with CTV is it's what's called a limited or non-recursive covenant.
And so like with CTV, you can't have an unending tree of transactions that the covenant locks the coins up in.
With OpVault, OpVault is actually a fully recursive covenant.
And that's kind of part of the value is you don't want to be bounded in the number of times you can withdraw from your vault.
If you want to maintain that vault for your whole life, you should be able to do that.
But the important thing to address is that there's no on-chain pollution in terms of resource use.
And, you know, in the case of OpCTV, it's literally just doing a hash.
It's like It's less expensive than elliptic curve operations.
Basically the whole Internet's been trying to break CTV to, you know, like, hassle Jeremy since it came out and nobody's been able to.
I mean, I tried.
There's been multiple Bitcoin bounty.
So CTV is like the Galaxy Brain criticism of CTV when it was on the table was, it doesn't go far enough.
Like we can't have these unending covenants.
So we should wait for a system that actually has unending covenants or can support that functionality.

Speaker 0: 00:32:47

Well, we don't have even a proposal for that.

Speaker 1: 00:32:50

Yeah, I mean, there's kind of...
There's ideas.
Yeah, there are ideas for using CAT and CheXIG from Stack to do these very messy script, giant programs that people put on chain.
I'm very skeptical of all that.
And frankly, like, if you think about what are the things that you actually want to use Covenants for, I have two things I'm excited about.
Number one is vaults, which like literally everybody using Bitcoin should care about because it's about safer custody.
And number two is something like coin pools, where you could actually scale Bitcoin by sharing UTXO ownership in a trustless way.
Coin pools is still a science experiment.
And I hope to God it happens because we need it.
But it's very much a science experiment.
Nobody really understands it.
Vaults are extremely well understood.
And so I don't really care about general covenant mechanisms because I like the two things that I'm excited about are kind of like squared away in my mind.
And, you know, OpVault hits the first use case really well.

Speaker 0: 00:33:49

Okay so what are there, I mean we can get more into the CTV stuff but is there like other sort of criticisms?
I'm trying to essentially like what I want to know is like what do we expect once we start putting this out there as like, Hey, I think it's done.
Let's let's activate.
Right.
I mean, it's still going to take a while, but like, it's going to happen.
Right.
And, and I want to just preemptively understand like, you know, what's coming here and how do we address it?
Because, you know, this is Bitcoin.

## Do we need OP_VAULT? Why change Bitcoin?

Speaker 5: 00:34:21

I think like another question that I've seen around is, you know, hey, we have mini script is like getting better.
People are building better tooling for doing Bitcoin script, do we need this?
What does this give us that we can't already do?
And I think that that's probably not a question coming from a place of trying to tear apart UpVault.
It's more a general question of anytime we add anything, we should say, like, do we really need this?
It's fair.

Speaker 0: 00:34:53

It's a fair question.
It's like Bitcoin works with like, original pre-BIP32, like, you know, pay-to-key.
So like, I mean, why do we need more stuff?
Right.
I mean, like it works.
Why are we risking our golden goose?

Speaker 1: 00:35:11

And NVK, it's a great question.
And it kind of gets to what you were mentioning in the episode with Paulstra and Waxwang, which is like, well, we already have Taproot and you can do these complicated spending conditions with Taproot.
Why isn't that sufficient for the Vault's use case?
The answer is pretty simple.
We may have to chew on it a little bit to kind of fully articulate it well.
But the idea is that right now, like without OpVault, there is no way of starting a relative time lock, like at any point you choose.
So right now you can lock up some coins and you can say, okay, I have this crazy taproot tree that has all these different spending conditions.
One of them is that in a year, the coins are going to go to my recovery key or are spendable by my recovery key.
You're like, oh yeah, I've got vaults.
But you actually don't because when you actually create that UTXO, the clock has started on that year long kind of march towards the recovery.
And so what you wind up having to do is like, say, rotate your coins every so often.
And there's a trade off then between how often you have to rotate your coins and when they become accessible by the recovery path.

Speaker 0: 00:36:23

There's a few problems there too right I mean you lose your privacy once those coins move right or depending on how it's set up but it's like high risk of privacy loss, high risk of, you know, your target recovery path having issues too.
Like it's just one more thing you're getting forced to use, even though you weren't going to use.

## OP_VAULT Opsec

Speaker 0: 00:36:44

You know, One funny thing I think it's gonna happen with the best version of OpVault that comes out is that some dude is gonna point his, say whatever, like a million SATs to a phone wallet when he was building the script.
50 years pass and nobody touches that.
And that vault sort of goes to that phone as recovery.
And all of a sudden the guy has $10 million on his phone and hopefully he has a backup.
That's where the people fuck up, Right?
Like it's like, it's in this sort of like, it's very hard to think in the future.
So having things that the clock starts are kind of a problem too, because that execution will happen if you don't do anything, right?
It's like starting a fuse.

Speaker 5: 00:37:32

And like, I think that operational complexity gets worse when you think about the ways that people actually spend and use Bitcoin.
So if you're doing some weekly or monthly DCA and every single one of those UTXOs has its own timer that starts the minute it hits your wallet, you now have a ton of operational complexity to deal with like, oh great, every month I have this laddering, rolling, expiring time lock that I have to flip.
Instead of just saying all of these go to a common vault construction, and then when I want to be able to spend for my savings, I start the clock.
When I hit spend, it takes three months or whatever, And then I have a recovery path or I have my normal spending path.

Speaker 1: 00:38:19

Right.
And it's worth pointing out that we're only even talking about the op vault use where like op vault protects you if you lose your key.
We're not talking about intervening in a key theft or preventing the theft of your bitcoins.
There's just like simply no way of doing that today, especially when you start talking about all the cool kind of recovery methods that you could use, you know, whether whether it is like some kind of crazy offline, you know, cypher wheel key that you generate, or whether it's a three of five social recovery that you distribute to your family, or whether it's some kind of like long time lock thing, or whether it's like all these conditions under a single taproot tree, like you can really, really get an incredible degree of security that you hopefully never have to use.
And then in the meantime, you can feel very confident about using, say, just a single cold card or even a software wallet, honestly, if you have the right kind of watchtowers in place for really convenient transactions.
But you still sleep at night because you know, okay, I have, you know, let's say a two day time lock.
Someone, you know, like there's no way someone's going to walk away with my coins and I'm not going to intervene kind of in a period like that.

Speaker 0: 00:39:30

One thing I'd love to do is, I kind of wanted to do this with CodeCard before, which is you integrate the hardware device into your home alarm system.
And this is totally doable.
It's just kind of cost and not yet interested in the complexity.
But, and this could be wireless too, which poses other trade-offs, but let's say it's wired.
So there's no sort of like a tinfoil hat people's concern for this argument.
So it's wired, right?
Your house alarm goes off.
Somebody opens the door of the house at night, a timer starts on the device.
And if you don't stop the device timer, the coins go away or the device bricks itself.
Right, like super, super easy to do.
Like you can ship it tomorrow kind of thing.
But the problem is I don't feel safe doing this unless I have other recovery methods that are involved on this, right?
Because again, 10 years pass that you had that set up on because the device is good, the setup is good, And ideally you don't touch your shit once it's working.
Right.
So 10 years past, I can't remember anymore.
Is that key, the recovery key really backed up?
Where is it?
That kind of stuff.
I can't remember.
Maybe I hit the head in the something and I just forget.
The people forget.
And if I have like a proper like recovery, like part of the recovery path, not part of your script path, like, but there is for that key where the money goes.
Whereas a pre signed thing, you feel a lot more secure without having to remember all this stuff.
That could live in a vault somewhere of your will and you're probably still alive hopefully and you go, you check it.
Oh yeah, of course, it goes here.
So you didn't get robbed and the money is not gone.
Right.
That's huge.
This is the kind of stuff that I think we're going to like start getting into as the years and attack like the physical attacks will start to increase, especially as you will see a billion dollar Bitcoin for the year.
So

Speaker 5: 00:41:33

I think that's a great example, right?
Because like you could that set up that you described, you could go and build today.
Right.
So there's like Home Assistant, which is like open source home automation that you can run on Raspberry Pi.

Speaker 0: 00:41:44

Fuck Raspberry Pis.

Speaker 5: 00:41:45

Sure.
But you could like run that on a low power, you know, Unix machine of your choice, you know, hook it up to your alarm system, get a signal over MQTT or something, and then have a cold card plugged in in CK bunker mode and have it just automatically send your coins if somebody opens the door between 2 a.m. And 6 a.m. Or something.

Speaker 0: 00:42:08

That's how banks work.

Speaker 5: 00:42:09

Yeah, for sure.
And so, but anybody who does that is gonna have this moment of like, oh shit, I've got this unlocked live device that can now send all my money anywhere.

Speaker 0: 00:42:19

It could still be locked, but yeah.

Speaker 5: 00:42:21

Right.
But it's still this risk of like, how much do I really trust this thing?

Speaker 0: 00:42:24

Oh, of course.

Speaker 5: 00:42:24

So by having having a vault construction, you could say like, oh, no, if somebody goes and like hacks this device, then I still have a cancellation path.
Like I still have some way of clawing my money back so that it's, you know, it doesn't completely compromise everything.

Speaker 0: 00:42:41

Yeah, it's, I guess like the goal, at least in my mind to the bias to the things I do, the idea is like, how do you sleep at night?
And the problem is once you have too many nights, well slept, you forget.
You forget what he did.
You forget what stuff is.
You forget who has what.
And I like this idea that it's not a person.
It's the chain, right?
I mean, in one way or another, it's like my stuff lives on chain.
So that like, okay, like at least, you know, like it's not all lost, right?
And then you start sort of like digging through the notes and figuring out what's gonna happen next.
And you also have time, right?
Like you have like a decent amount of time that who knows, maybe even rewind it.
It goes back to the original wallet, right?
Or maybe there is a way to cancel it.

## Cancel paths

Speaker 0: 00:43:29

I don't know, Like, does the current proposal have a means for you to cancel something once it's in the time period that it's going to say, something is going to happen in, say, 10 blocks, right?
Is there a way for me to say, hey, no, stop that?

Speaker 1: 00:43:45

Yeah, actually.
So one of the benefits of the new formulation of the proposal is originally that wouldn't have been possible.
But what you could do now is you can include a tap leaf that is like all these coins are immediately spendable back to the original vault.
And that gets preserved in the tap tree as the triggering process happens.

Speaker 5: 00:44:07

Is that the T-love change to it?
Is like, as long as this tap leaf is in the output, then you're good?
Is that where that came from?

Speaker 1: 00:44:17

So I think if

Speaker 3: 00:44:18

I remember right when we talked about this, it was using the op-vault-recover path.
So you basically have additional recover paths that point to like a new...

Speaker 5: 00:44:29

It's the same

Speaker 3: 00:44:30

vault, so to speak, but it has to be slightly different because you can't commit to itself.
But you basically have a cancel path.

Speaker 1: 00:44:37

Greg, I'm even thinking you could, if you just had a leaf in the tap tree that was the same exact vault parameters as like what you had originally started, that's like an always cancel or always go back to vault initiation.

Speaker 5: 00:44:52

It always resets back to the initial state.
Right.

Speaker 1: 00:44:54

Yeah.

Speaker 0: 00:44:55

So here's a cool thing, right?
Say, you know, that home issue happened, right?
The guy hopefully didn't kill me.
He saw that, you know, like really there's nothing I can do.
And, but I still feel like the, the S the system is, is like reasonable and say, for example, I have a two week waitout period, right.
That I can still cancel, but to cancel that I have to travel to like a very distant land where I have a specific key that triggers the cancellation.
The whole beauty of this is that nothing moved.
Right?
Like coins not moving is a feature, not a bug.
Right.
So like my, that's where like my head is at with a lot of this stuff.
It's like, how can I build this, the scenarios and, and like, I don't know, like, I hope that at some point soon we start having like some interesting user stories, right?
Like of like things that you can do and how you actually achieve them, you know, and how do you construct them and like both script wise, but also like how do you deploy them, right?
Okay.
So is there other aspects of this that should be part of this, of this specific moment of the conversation?

Speaker 1: 00:46:03

Yeah, I think so.
Like there's another thing people have worried about in the past, which was a surprising one to me, but in hindsight it's understandable.
I think a few people on Twitter have asked like, okay, well if you've got this ObVault thing and I go and, you know, send some coins to a merchant when I'm buying something.
But I have this ability to cancel and claw back.
Can't you scam the merchant by trying to pay, by unvaulting and then reclaiming your coins?
And yeah, the answer is, of course, like the merchant's wallet expects the coins to be sent to a specific address and you can't actually get to that specific address until you're out of the withdrawal period or the trigger period.

Speaker 0: 00:46:43

So one good way I think to sort of exemplify this a little bit simpler is the receiver controls the deed forward.
So it's the receiver of the coins that sets the rules on how those coins get spent.
So if you're a merchant once the coins hit you they are yours for you to decide if that receiving address of the coins is a standard one or is one that has deeds or covenants going forward.
And I guess I'm kind of oversimplifying, but I think that this is the part that people don't seem to get.
Is that the sender doesn't really have control over the coins that you received.
It's only you, the receiver, that can control that forward.

## Why do OP_VAULT along with CTV?

Speaker 0: 00:47:30

What other issues do we foresee people having here?

Speaker 1: 00:47:35

So let's just like just so we make sure we address this one.
I want to say kind of, okay, well, now OpVault's all modular and composable, and it doesn't have a strict reliance on CTV.
Like, why am I recommending we do this along with CTV?
Like, why can't we wait for something else?
And the answer there is, so number one, like to do vaults, you need some way of saying, okay, I'm publicly committing to these coins going to a fixed set of outputs.
So you just kind of need that behavior.
Number two, CTV winds up being the safest way to do that and the simplest way to do that.
Like, when I started this proposal, I wanted to, I mean, I love Jeremy, I love his work, we're friends.
I think the world of CTV, but I didn't want to go out and just do CTV because I knew there was going to be a bunch of drama and controversy, yada, yada, yada.
But this convergent evolution thing happened where the solution that we came to, it just wound up encompassing CTV.
Jeremy's already written a bunch of tests, like the change set is really very small to do the whole CTV thing.
So I figured I'll just reuse that.
He's already got a bit like pull that in.
The union of the CTV changes and the OpVault changes wind up being about 5,000 lines, which is, I'd have to check the numbers, but I'm gonna say it's like an order of magnitude less change than like Taproot or SegWit.
So you're looking at a potential.
Or elements.
Or, oh yeah, I mean like, you know.

Speaker 0: 00:49:09

Is it 80,000?

Speaker 1: 00:49:10

The simplicity, yeah, the simplicity branch on elements.
And I don't wanna trash like that.

Speaker 0: 00:49:14

No, no, no, I'm not saying, it's not trashy, just sort of like just by the number.
So people understand the scale of things.
Right.

Speaker 1: 00:49:21

Yeah.
Yeah, exactly.
Exactly.
And so that's I guess my point is like I want to return to an era where like we can look at small soft forks Because Segwit and Taproot were complete reimaginings almost of like various aspects of Bitcoin.
And there were massive, massive like engine overhauls.
And this is a change that's a lot like check sequence verify or check time lock verify or check lock time verify, like really well contained, pretty modest, simple changes.
And so both CTV and OpVault are a very manageable, kind of small set.

## OP_VAULT + ANYPREVOUT

Speaker 0: 00:49:57

How does this relate to, say, like just in comparison to say any prev out?

Speaker 1: 00:50:01

Yeah, so you can actually use any prev out to do the same thing.
Like if we wanted to do op vault and APO, I am pretty sure that would work as well as op vault and CTV.
It's just that to do the CTV thing with any prev out, it actually winds up being more space consumption, because you have to actually include like a dummy signature in there.
So you're using, I think it's something on the order of like 32 more bytes to do the same thing.

## Blockspace concerns

Speaker 0: 00:50:28

Okay, so another question that everybody has, Can I vault my dick butts?

Speaker 1: 00:50:37

You sure can.

Speaker 0: 00:50:39

There you go.

Speaker 1: 00:50:40

Rheindahl, you want to talk about that?

Speaker 5: 00:50:41

Well, I mean, yeah, the Ordinal stuff, Like it's all just Bitcoin and UTXOs and like this works with Bitcoin.
So it works.
I mean, I think there's kind of something in there that you hit on that I think is important.
There's a lot of, you know, well, why don't we do this software instead of that one and we can emulate everything else?
And I think, you know, something that's important to remember is that block space is the constrained resource.
And so if there's going to be common cases that lots and lots of users of Bitcoin are going to be doing then it makes sense to have kind of optimal implementations for those use cases to be more space efficient.

Speaker 0: 00:51:18

I mean, but dude, like, I mean, seriously, like this stuff is like minuscule compared to like half of the, the multi-sig, the complex multi-sig, like not complex, but just multi-sig with like enough inputs and outputs, like this stuff is still minuscule, right?
Like I mean, like, or compared to JPEG.
This is ridiculously small when it actually comes down to actual transactions.

Speaker 5: 00:51:42

Well, but you know, like store value is the dominant use case for Bitcoin right now, I would argue, outside of just like pure spot speculation.
And so if we think in a couple of years, if this got activated in a couple of years, I'd bet that most wallets would have some kind of vaulting functionality.
And so it makes sense to kind of have like the most compact vault implementation that we can rather than emulate it in some other covenant scheme and waste some bytes.

Speaker 1: 00:52:09

Totally.
Yeah, Rheindel is right.
I mean, you have to multiply all this stuff by a billion users, potentially.
I mean, like, I don't know what the right scaling number is, but I think a

Speaker 0: 00:52:18

billion users can use Bitcoin based layer.

Speaker 1: 00:52:21

Yeah, right.

Speaker 0: 00:52:22

Certainly not even close.
Yeah, certainly not in its

Speaker 1: 00:52:24

current form.

Speaker 0: 00:52:25

They're going to be using Cashew.

Speaker 1: 00:52:27

But like the most scarce resource here is Chainspace.
And, you know, as a runner up, it's time to verify, time to download the entire blockchain or, you know, some kind of equally secure form of it.
So Randall's point's really good, I think.

## Use in chaumian mints/ecash

Speaker 5: 00:52:42

So NVK, you just mentioned Cashew, you know, We just talked about Chami and Mints not that long ago.
This would actually also be great to add to Chami and Mints, right?
So if you have either a Feti Mint or a Cashew Mint and you want to say, all right, we're going to have our Mint's treasury in a vault that has like a, you know, this time locked predestined withdrawal path so that if either one of the functionaries of the mint or if somebody pwns the software and tries to like run away with the money, then we can claw it back.
This fits in really, really well with the idea that maybe we'll have some collaborative custodyments for a lot of users.

## Managing security between L1 & L2

Speaker 0: 00:53:25

So what I'm seeing now, just conceptually, there is a trend, right?
We now understand Bitcoin doesn't scale, right?
I mean, we knew that from like, you know, 14 years ago.
But like everybody else is sort of starting to catch up with the fact that Bitcoin, even if you make the block size 10 times bigger, right.
Like it doesn't scale right to 8 billion by the time that we are done with this is going to be 10 billion people in the world, right?
So we have to find solutions to keep the extreme high value transactions safe, right?
The extreme high value like vaults, that being up vault or just vaults safe.
These are not going to be people's phone wallets on base layer.
And we have to manage to keep all the L2 stuff safe.
So you have the vaults that feed liquidity into lightning pools, right?
That sort of fund all the LSPs and all that stuff.
So you need to keep the coins that feed those safe in enterprise environments or in sort of like, you know, small business sort of solutions, right?
And we have to do this trans nationally, which makes things extremely complicated from a regulatory point of view and an actual operations.
Right.
So like you have, say block has a head office in Canada, head office in the U S, a head office in Germany.
They all have three different sets of laws.
They all want to put everybody in jail.
So like, you know, how do you resolve these problems with like the whole compliance shit and not get robbed, right?
So the trend is like, how do we resolve all these ill to custody of a lot of monies?
And then you have the clearing of essentially Bitcoin is wires, right?
Eventually, you're going to have people just clearing between each other, like large amounts of of economical value in a smaller possible transaction, because the blocks will be full.
And then you have this L3 solutions, right, where they don't necessarily clear to Bitcoin, but they're leveraging Bitcoin either to Lightning or directly to create even further atomization of those economic movements, right?
So because Lightning also does not scale to 8 billion people.
So you're gonna keep on creating this atomization on top of atomization, right?
But at the end of the day, you still have a problem.
Where's the Bitcoin private key?

Speaker 4: 00:55:45

That's

Speaker 0: 00:55:45

right.
Right?
And it's a lot of money on those as we keep on moving into this like higher levels of trade offs.
And I keep on going back to the op vault.
That's what my interest is in.
It's like, how do you do this stuff?
And like, you can't do it with just ECC calculators.
Right.
We need to do this with programmatic money.
So that's like my little short rant, optimistic rant there.

Speaker 1: 00:56:15

I think you're 100% right.
If you imagine there's a likely world where Bitcoin success is kind of like you have a constellation of 10,000 Feddy-like systems that are all interconnected, maybe with something that looks like lightning.
You need a bomb proof way for each of those little subsystems to secure their big pool of capital.
Like this just unquestionably secure.
Like so we need to develop patterns where if you're running a FEDI installation, you just know you're not going to get hacked.
You know you're not going to lose your coins if you're following a certain procedure.
And I think vaults are a big part of that.

## Vaults & DLCs

Speaker 0: 00:56:56

Ben, any interesting sort of like side tangents here between vaults and DLCs?
I've heard that you like DLCs.

Speaker 4: 00:57:04

I'm a fan.
Yeah, we talked about it a bunch on the previous episode, but I think it was Lloyd Fournier released a post on the mailing list a few years ago saying, oh look, if we had CTVs, or basically kind of any Covenant, I think Jonas Nick showed you could do with any privout, and I showed you could do with old op vault.
And now that new op vault has a CTV again, you could do it the same way.
But basically, like, 10x the usability of DLCs, because say, right, like, if I want to do a DLC like on the Bitcoin price with you, Rodolfo, like it's going to be, you know, like probably like 80,000 signatures and that, you know, doing that on the phone is like, you know, a ton of like processing time and data we need to send.
So it's not really usable for the layman, at least as much as we'd like it to be.
But with CTV, or any company, you just distill that into, we both need to generate the same address, and if we do, then we have the same DLC contracts.
That explodes the usability, I think, and as well as the composability because now you could, with CTV, you could have DLCs that are paid out to, not just my address, we could have it paid out to another DLC or another, some thing where it's like, this goes into an address that then splits it among five people safely instead of having to trust a multi-state configuration or something like that.
So it makes the like you can kind of get into like the world of like we're now again some really fancy kind of contracts are like almost competing with like eth, degen stuff but like in an actual safe way that's not just like, you know, retarded like JavaScript on the blockchain kind of stuff.

Speaker 1: 00:58:52

It's like mostly off chain, right?

Speaker 4: 00:58:54

Yeah, it's all off chain.
We're just like, you know, doing hashes and signatures.
But you're able to like do the really complex stuff that's just like a chain of transactions.

Speaker 0: 00:59:04

No, no, their blockchain is on Amazon.
There's two archival nodes.
That's not a joke.

## How do we activate OP_VAULT?

Speaker 0: 00:59:10

So, okay, great.
We love this.
This is very cool.
How do we activate this?
Especially now that CTV sort of been added to the hat?
This is going to be, I mean, Bitcoin activation should be excruciatingly painful.
I know engineers don't like to hear that, but it kind of should.
That's a defense mechanism.
But how do we get there?

Speaker 1: 00:59:31

From here, it goes to AJ Towns Inquisition.
And what's nice about that is that it's going to allow me and anybody who thinks this is worthwhile to create some example wallet software to play with it, to make sure it's the right thing, you know, to vet it against, like, other outstanding proposals.
Like what's cool about Inquisition is you've got active right now on Inquisition, you've got APO, CTV, some of Greg's mempool stuff.
So we'll get to see how it plays with some of the other proposals out there.
But, I mean, so I'm obviously biased.
I've been working on it a lot.
I'm going to continue to work on it, obviously, and do whatever I can technically.
But probably there need to be other people who advocate this.
You know, if other people find this important, they're going to need to speak up and, you know, kind of signal that they actually want it because I'm not in the business of selling, you know, consensus changes.

Speaker 0: 01:00:22

Oh, but you are, you have to, that's how it works.

Speaker 5: 01:00:26

That's what this is now.
But, like the,

Speaker 0: 01:00:28

this is literally what this is.
Yeah.
Yeah.

Speaker 5: 01:00:32

Welcome to the sales job, James.

Speaker 4: 01:00:35

Welcome to hell.

Speaker 5: 01:00:36

So the Inquisition thing, I think it's super important, right?
Because like, I think one of the problems that CTV ran into, for example, is, and like, I don't want to beat up on CTV.
I think it's just a good illustration.

Speaker 0: 01:00:48

No, please beat it up.
It's going to be all brought up again.

Speaker 5: 01:00:53

CTV could do a lot of things.
I think a lot of people had trouble connecting the dots between, okay, I have Bitcoin, it works for me now.
Any change to Bitcoin is a change to Bitcoin.
What am I going to get out of this?
Why does this make Bitcoin better for me?
And I think it was hard for a lot of people to connect the dots of what they were going to get out of CTV.
And what's cool about OpVault being active on something like Inquisition is we can go and build wallet software to say, hey, look, here's a single SIG wallet that is as easy to use as a normal phone wallet.
Maybe it's a command line app,

Speaker 0: 01:01:31

Maybe it's a phone wallet, maybe it's a

Speaker 5: 01:01:31

command line app, maybe it's a phone wallet, maybe it's a web page, whatever.
But hey, look, if somebody steals your money, here's how you would intervene and recover it.
Or, hey, here's a wallet that has a built-in inheritance flow.
Or, hey, here's a wallet that has complex spending conditions for this other use case.
And people can actually try it out and start building some intuition for how they would actually use these things in their life.
And I think the way, if we want to do, I'll call it a community-driven or a user-driven activation of a fork, I think people have to really understand, like if I'm gonna go and run this other software on my node and opt into this new set of rules, like what's the economic benefit for me?
And so giving people tangible ways of feeling that I think is really important.

Speaker 0: 01:02:19

I mean, all people really need to do is try to change to a new phone.
And they're going to realize how many of their wallets are lost, how many have a super ultra complex, completely stupid retarded way of like recovering in case you do lose the key because they don't have a seed.
It is surprisingly like surprising how much these things touch you as soon as you try to do any changes to your setup.

## Is there enough interest to do the work?

Speaker 0: 01:02:43

So, okay, so there was like, for example, say Liana, right, Where they're trying to do some of this sort of fake covenants by just doing a bunch of pre-signed scripts.
You know, zero interest from people really.
I mean, realistically speaking, nobody cares, nobody's interested.
So How do we get some of this apathy combated?
Because nobody's going to do SIGNET.
Nobody's going to try with fake coins.
Is this like a whole other, let's make little videos, let's do this, let's do that.
Is there enough appetite, enough budget really, from people that care enough about this to do a lot of this work?

Speaker 1: 01:03:19

It's a really good question.
And I think there, I mean, from my perspective, there isn't a big solution for it.
I think my approach has been to come up with this solution and put it out there.
And hopefully, maybe it'll take time for people to actually say, hey, no, we really want this.
I mean, I think luckily there's a lot of interest, like certainly from large custodians.
You know, Alex Leishman of River.com has been like really, he went on like a tear when he read the paper.
And he said like this is like an order of magnitude improvement in my custodial operations.
This will make me like actually sleep at night.
So I think like there is definitely industrial interest.
And obviously that's going to like maybe trigger people a little bit.
But it's it's really coming from the best.

Speaker 0: 01:04:02

But it's a small scale, guys.

Speaker 1: 01:04:04

Yeah.

## Investment insurance concerns

Speaker 0: 01:04:05

You know, the big guys are still going to go to fire blocks, right?
Like Coinbase and all this stuff.
And they're still going to do all that crap today because that's people don't understand, like the majority of Bitcoin that is not in HODLers hands is in fireblocks.
And these fuckers just keep on transferring to each other without transferring to each other.
So they're all printing Bitcoin essentially right now at this moment.
I'm sure it's just a latency issue on the clearing, right?
Just enough to add a little margin to that position.
So like, what I like is that because say for example, River, right?
So Alex Lishman, you know, even though he's going to write it in Elixir, which is going to be a problem.
So let's say, Is he

Speaker 3: 01:04:45

really?
Yeah.

Speaker 0: 01:04:47

Yeah.
Yeah.
So, so let's say like, you know, he has this company that is sort of like a mid to small size, you know, Bitcoin brokerage.
Right.
The problem is like it's going to be very hard for him to find more capital to increase his liquidity.
Right.
To be bigger because he's not going to find insurance.
He's not going to be able to, to do the kind of the diligence you're going to need to do.
Like all this stuff around the DD, right?
That he's going to have to do in order to grow to the next stage of his company, he's gonna have to go to Fireblocks because they hit the check boxes.
Right.
That's the check box people.
So what do you do if you don't wanna go to the check box people?
We had that problem as a company way back in the day.
Like, it's like, fuck the check box people.
We're just simply not gonna do it.

Speaker 5: 01:05:33

Or just more generally, like if you have unlimited budget, like you could build a really kick-ass vaulting system.

Speaker 0: 01:05:40

Like it's not gonna be certified.

Speaker 5: 01:05:41

Well, right.
Well, and it's not gonna be cheap, right?
Like If you have a lot of money, a lot of people, and a lot of hardware in geographically distributed locations, you can build a kick-ass vaulting system.
I think one of the things that's cool about OpVault is it lets anybody build a kick-ass vaulting system just out of Bitcoin script.
If you're an individual hodler who wants to be able to move money from their phone, but then if they get robbed, then they drive to the bunker, dig the thing out from underneath their well, then you get kind of the same grade of security as somebody who has a shitload of HSMs on three continents.

Speaker 0: 01:06:17

Well, actually better because, you know, the HSMs could be hacked, the vault can't.
So, no, but it gets weird, right?
Because see, the Fireblocks have all the FIPS certifications, right?
So if you wanna get those at that level, you're going to be spending millions of dollars on just the certification.
Right.
And it doesn't mean it's secure.
It means it just has the correct back doors for FIPS.
So, so like, you know, what's really cool about this is that you're enabling like all this mid-sized businesses to have like the checkboxes needed for them to be big businesses, for insurance purposes, for all the investor due diligence stuff, without having to go and deal with Fireblocks, for example.
Well, it's

Speaker 1: 01:07:00

funny you mentioned the insurance stuff because I think, I don't want to put words in his mouth, but I think I recall Rob from Anchor Watch really expressing a lot of support for a proposal like this, this proposal particularly.
And for anybody who isn't familiar, Anchor Watch proposes to be in the business of insuring theft.
So if you set up a wallet, you know, per some specification that they would give you, they'll say, OK, this is like a good enough setup that we're going to actually insure this against law.
So if those coins somehow get stolen, you know, we pay you out.
I don't know too much about their company, but I know, you know, something like this makes, de-risks them quite a bit because if there's like super high security, then, you know, they're gonna have fewer payout events.

Speaker 0: 01:07:46

Disclosure, I'm an investor.
Do

Speaker 3: 01:07:48

they actually watch the anchors and like sweep them or something?
Because as an insurance company- I don't know how it actually-

Speaker 0: 01:07:53

No, it has nothing to do with actual anchor watch, like actual watch towers or anything like that.

Speaker 3: 01:07:58

Okay, because an insurance company should be incentivized to do things like that.
Right.
To not pay out.
That's an interesting idea.

Speaker 0: 01:08:05

That's just the name of the company because it's like a thing that used to happen in the Navy.

Speaker 5: 01:08:09

Yeah.
It's a nautical term.

Speaker 0: 01:08:11

Yeah.
So essentially like what they're trying to do is create some standards.
Right.
That are insurable.
So they're going back to, to reinsurers and, you know, all the underwriters and everybody sort of say, Hey, you know, this is how we think we could do it so that the coins are actually safe, can insure this, right?
So they're trying to find the packages that meet the technology that can be done.
And they're sort of like a mini script sort of makes their life easier to, yeah, no, nothing to do with ephemeral and CoreWatch.
So they're trying to just create policies based on setups.
And if you want to get your ear talked off, just go to ask Rob about Miniscript.

## Now really, how do we activate OP_VAULT??

Speaker 0: 01:08:56

So yeah, guys, what else here?
Okay, so let's go back to the painful topic, which is like, how do we activate this?

Speaker 1: 01:09:02

Reyndall's shaking his head.

Speaker 3: 01:09:04

Yes.
So I'll pipe in a little bit.
I think we still need review cycles.
So people read the bit and the documentation about like use cases are all fired up, but not many people are fired up about reading specs and trying to see what makes sense.
So I've been spending some more time on that too, back and forth with James and others, and I think that's got to continue for a little longer while we figure out the SIGNET stuff.
So that's my, my intention at least.

Speaker 0: 01:09:33

Yeah.
So like I'm not suggesting we're like imminent to activate this.
I know there's still like, you know, months, if not, like maybe a year or two on how like we're sort of like, OK, this is it.
Right.
Like everything is great.
Everybody agrees it's great.
And then we can start the argument about how to reactivate something.
It's just I have a feeling that this one might be the one that reopens the activation.
That and 324 as well.
It might be all in an ominous bill kind of deal.

Speaker 1: 01:10:03

Wait, 324 is peer to peer encryption.

Speaker 5: 01:10:05

Does 324 actually need a soft fork?
Because 324 is just P2P.

Speaker 1: 01:10:08

I think it's just implementation.

Speaker 0: 01:10:10

No, doesn't it?
I could swear it needed a soft fork for something on it, But maybe I'm wrong.

Speaker 1: 01:10:16

I sure hope it

Speaker 4: 01:10:16

does.
It's just P2P, so it should be fine.

Speaker 0: 01:10:19

OK, it's just a P2P part?

Speaker 1: 01:10:20

Yeah.

Speaker 0: 01:10:21

OK, wonderful.
So we're going to just argue about clients and connections.
Great.

Speaker 1: 01:10:26

Easy stuff.

Speaker 0: 01:10:27

So anyway, so it does look like it's going to be just this.
I don't have another bone to throw because I was going to put the 324 in there.
Hey, look, there is something else that comes with this.

Speaker 5: 01:10:38

324 is going to be awesome.
And maybe the timing works out like at the same time.
And so it might be it might be the case that what ends up happening is there's a lot of hullabaloo because there's a perception that it's this big change to add covenants and make Bitcoin encrypted or something because 324 adds opportunistic encryption to the P2P networking and it's not actually a consensus change, it's just transport.
But the timing might work out that way.

Speaker 1: 01:11:08

One thing I've been thinking about, and maybe Greg can chime in on this, is like what if we did, What if we eventually proposed a fork that was up all CTV and APO?
Because I know you know a lot of people have wanted a peel for a while Obviously, I can't judge the use in l2, but the size of that fork is

Speaker 5: 01:11:30

James Ellen symmetry.

Speaker 1: 01:11:31

Oh, yeah, you know you're up.
Thank you.
Thank you.
Yeah, I want to I want

Speaker 3: 01:11:35

to Oh, thanks James for bringing this up.
Just today I got an LN Symmetry channel close onto Cygnet by the way.
So, you know, show that later.
But yeah, I mean, so these soft forks are all aimed at very specific use cases, improving things we have today, right?
We have channels today, like lightning channels, we can make them better with IPO.
We have vaults today, but we can make them better without vault.
We have DLCs, you can make them better with CTV.
That's sort of the notion.
So I'm definitely on that wavelength of sticking kind of close while there's like more fundamental research happening for longer term.
I'm not sure what that means.
When it comes to deployment, I think that's going to be tough.
I don't think we're there yet, but we have communities that are motivated for their specific pieces, and I think that's really important.

Speaker 1: 01:12:23

I just, from my standpoint, it feels to me like CTV and APO are very, very baked, and they're very, very small changes.
So I could almost, I think from a deployment complexity standpoint, it makes sense to me that if OpVault in the next few months here or whatever gets really well vetted and people feel very comfortable with it, it's not a lot of code.
And so the three of them together, I could see maybe atomically activating just because that way, you know, you can test the shit out of something like that.
And

Speaker 0: 01:12:55

it's going to be very interesting if there is a softbark for this much stuff together.

## Taproot & Segwit complexity VS OP_VAULT

Speaker 3: 01:13:02

Still smaller than Segwit.

Speaker 1: 01:13:03

Well, if you think about it, like Tapper contained way more.
Segwit contained

Speaker 0: 01:13:07

way more.
Oh yeah, I know.
But it has one name.

Speaker 3: 01:13:09

And Segwit was even scarier.
I was there.
It was terrifying.
It's a lot of code.

Speaker 0: 01:13:13

Yes.
But there is one, just one name of the thing, right?
Like people are counting the things.

Speaker 1: 01:13:19

But that's the irony of all this.
That's that's like the Bitcoin community really needs to take a long, hard look at itself and realize that like people got played.
People like people are constantly the victim for as much as there's like the whole like verify don't trust thing in the Bitcoin community.
Like people say taproot like they know what it means.
I didn't know what taproot meant fully when it deployed.
Like how familiar are you with the specifics of the annex and the way that that works.
Do you even know that there's

Speaker 0: 01:13:47

an annex?
I still don't put money in Taproot.

Speaker 3: 01:13:49

I do, James.
James, I used it today.
I know what it is.

Speaker 0: 01:13:53

And I'm not talking to any of

Speaker 1: 01:13:54

you guys, but I'm talking, dear listener, like, were you lobbying for Taproot and did you really understand what was in it?

Speaker 5: 01:14:00

Well, I mean, like a lot of people are shocked that Taproot is actually three BIPs, right?
Like Taproot isn't one thing.

Speaker 0: 01:14:07

Yeah.
I mean, people still don't understand that we added another cryptographic primitive to Bitcoin.

Speaker 1: 01:14:13

Yeah.
So like,

Speaker 0: 01:14:15

It's kind of a big deal.

Speaker 1: 01:14:17

It's just funny to me that these software we're talking about here are extremely narrow, extremely well-scoped, extremely well-understood.
And yet, because of the marketing machinations, like, you know, we got, I mean, and don't get me wrong.
I love Taproot.
I'm happy we got Taproot.
I love, you know, all the stuff that it enables, but like there, there was not the like broad consensus that people think that they had because they were very comfortable, like delegating their, their technical opinions to other people.

Speaker 0: 01:14:51

I mean, to be fair, I mean, like there is very few people who can really, really, really understand that code.

Speaker 1: 01:14:57

Yeah.

Speaker 0: 01:14:57

Like very deeply, like period.
That's true for a lot of Bitcoin stuff.
Like, I mean, people do trust some people to give them some, like, that's where they infer from, right?
I think that's part of the reason why there is this backlash.
I want to call it almost like ludistic on new features and things.
It's because, you know, Bitcoin is a really complex to begin with.
Right.
And it's progressively becoming ultra complex.
And, you know, people just they won't understand.
Like, I mean, it's just it's just not possible.
The same way, You know, I don't understand how the brain really works.
Right, like you can tell me as a scientist who studies brains, right?
Like, I mean, you know, like there is a limit.
So I have to trust that you're poking in the right place with your knife, right, kind of thing.

Speaker 1: 01:15:45

And I'm not trying to criticize at all Segwit and Taproot the way they were handled by the people who helped activate them.
I mean, again, great changes.
They were communicated kind of as clearly as you possibly could, I think.
But I'm just, you know, it's a frustrating state of affairs when something like CTV and Jeremy to his credit pointed out a lot of stuff with Paproot He pointed out a lot of the issues with the annex and nobody listened cuz crazy Jeremy

Speaker 0: 01:16:11

I think like his delivery was was not a

Speaker 3: 01:16:15

I don't agree.
This is issue, but we could debate about that later.

Speaker 4: 01:16:19

He did find that with OPTCHECKSIGAD, like a timing or not timing attack, but he could take like 60 minutes or 60 seconds to verify a block or something.
So he did find some vulnerabilities.

## OP_VAULT product market fit

Speaker 0: 01:16:32

No, I know.
But like guys, like ultimately, right?
Like you guys are all smart and smart specifically in this field.
Right.
You have to understand that there is like all these other people that just won't be able to like understand it, period.
So now it becomes a point of like, it is also your job as the people who came up with the idea to sell it.
Right.
I mean, the top root people did a fantastic job selling it.
Right.
Like so much so that there was zero contention, except me saying I'm not putting my money on this shit forever until like I became comfortable with it.
Right.
And the contention became just on the activation mechanism.
Right.
So the whole fight around that stuff was around around speedy trial, which I still don't like.
But like, you know, like it's very possible that if the sales job is done right, then I mean this is like not insidious sales, just like an honest sort of attempt at like really getting people to understand this stuff at a level that they can understand.
And hopefully it's just going to be a fight over how we activate it, not over what's in the package.

Speaker 5: 01:17:35

Well, that's where I was trying to go talking about things like Inquisition or other places to have people actually understand what this change is for.
If everybody can wrap their head around the behavior of this change, what it can do, what it can't do.
OpVault does not turn Bitcoin into the surveillance permission coin.
It does not enable all these crazy, horrible 1984 use cases, what it does do is it lets you better secure and better custody your Bitcoin.
And having people really understand that and understand the ends of it, I think is going to be a lot of the work and it's going to be, yeah, I mean some amount of, and I don't mean this in a scummy way, but like marketing, frankly, right.
And like helping people like understand it and understand like what it does and doesn't do.
And then from there, yeah, it's a question of like, are we doing, you know, BIP-8?
Are we doing something like, you know, what do we do to actually turn this on?

Speaker 0: 01:18:35

I mean, there is a reason why the Bible exists in many languages.
You know what I mean?
It's like you want more people to be part of your thing, right?
Like, so like you got to meet them where they are at.
Right.

## Recursiveness of OP_VAULT

Speaker 3: 01:18:47

So I have one, one quick technical point.
So also a vault is only very slightly recursive.
It's only recursive in the sense of that you're allowed to revolt your change.
Everything else is actually not recursive.
So it's recursive in the most limited sense, I would call it.

Speaker 0: 01:19:03

That's a very

Speaker 3: 01:19:04

good point to bring up.

Speaker 1: 01:19:05

A good point.

Speaker 3: 01:19:06

Because you have to pre-commit up front to all the other paths, essentially, or at least the form of the path.
And so the only recursive part is it allows you to go back to the same coin, same address.

Speaker 0: 01:19:16

Well, I mean, that's what separates Bitcoin from Ethereum, right?
We literally don't have a way for you to create a full recursiveness there without having those things pre-committed.

Speaker 3: 01:19:26

So if we had like elements, tap script, all those crazy introspection, you could, but I'm just saying op bolt is actually like not that recursive.
It's not recursive in the way people are talking about usually.

Speaker 5: 01:19:37

I mean, the other thing that's important, right.
Is other networks like a theory, have like global state and in Bitcoin, your transaction is still scoped just to the inputs and outputs of your transaction.
So even, you know, like it's just a completely different animal.

## OP_VAULT main selling points

Speaker 0: 01:19:53

Yeah.
Okay, guys.
Listen, I think we covered a lot of ground and I can feel the resistance over talking about activation.
I think we should still explore, maybe not on this episode, but I think we should still explore a little bit of the, how do we bring people over to this?
Because it's going to be hard.
And I think if we leave people behind on this one, it's going to become even more complicated.
You know, you look at, I think just like by pointing to people that you're not going to get a new form of dick butts on chain because of this change is already like, I mean, huge, like, listen guys, like, look, it makes the dick butts even be like worst or something.
You know what I mean?
Like it's just pointing out like the fears that most people have, even if they're unfounded, I think it's a huge part of this.

Speaker 5: 01:20:52

That specifically is a thing that I've heard a lot around this, is we thought Taproot was going to give us better smart contracts and instead it gave us inscriptions.
So what is OpVault going to do?
Like, what horrible degeneracy is OpVault going to unleash on the world is something that I've heard a couple times.
I have my own answer for that.
James, I'm curious what your answer is.

Speaker 1: 01:21:15

Yeah, I think it's really tough to be in a position where you don't have the technical chops to go in and make your own judgment about things.
But what I'll say is that I think most developers for OpVault, for CTV, and for APO can go in and read the code and go, all right, this is pretty clearly bounded.
The number of things that can go wrong with this is pretty limited.
Whereas with SegWit or Taproot, that's a much more difficult exercise.
And even people who are familiar with the code, you know, have a much harder time kind of bounding the, you know, the implications.
But what's your answer, Rheindahl?

Speaker 5: 01:22:00

Well, I mean, so my answer is like two of the fundamental, like one of the fundamental things that Segwit did, arguably the fundamental thing is it changed like the structure of transactions and like how we store and how we like relay transactions around.
We like relay transactions around.

Speaker 0: 01:22:18

And

Speaker 5: 01:22:18

that made it cheaper to store arbitrary data on the blockchain.
And then Taproot explicitly was trying to make it easier to do larger, more complicated scripts, which made it easier to store larger dickbutts in single inputs.
OpVault is really aimed at letting you put restrictions on the output side of a transaction to let you specify that when these coins are spent, if you break into my house and steal my key or if you steal my phone and steal my key, you can't spend those coins anywhere.
You can only spend them on this predetermined path that has an escape hatch and that has a time lock so that I can be sure that my coins are going where they're supposed to be going.
And so constraining the rules on the output side is like a much slimmer design space for unintended consequences.
Like I hope that people come up with interesting, new, innovative use cases for taking vaults and using them to like solve more money problems, but it's way less of a blank check or a blank canvas from like a design perspective than, hey, here's a whole bunch of extra script space that you can put scripts in.

Speaker 4: 01:23:36

Can we market OpVault as you're guaranteeing your coins will never go into an inscription because you're locking them up forever and then they'll, you know, make sure I won't put it into some stupid dick but

Speaker 0: 01:23:48

there you go.

Speaker 5: 01:23:49

It's now more expensive for dick butts because there's gonna be less coins on the market.

Speaker 0: 01:23:52

There you go.
It's kind of fascinating.
What I like about the op vaults sort of it looks like something that would align with the huddlers.
Right.
Like or like or the most sort of like a traditional sort of the people who want Bitcoin to change the least, move the coins the least, right?
And sort of like huddle forever, like upvotes is for you, Right?
Like you can find a way to create a script and only your 10th generation ahead will get it.
Right?
Like if you really want to go Valhalla style.

Speaker 5: 01:24:29

Yeah.
A lot of people are, when folks were talking about interesting new covenants or anytime somebody brings up simplicity or something else, there's this pushback of, oh, well, you don't need super programmable money.
It just needs to be money.
It doesn't need to do all these interesting things.
And OpVault just makes it easier for you to securely hold your money.
Like that's what it does.
It makes it harder for your money to run away from you.

Speaker 0: 01:24:52

You know, I was in Nashville last week and they had the design week there.
So a lot of people who were designers interested in working on open source, which is like kind of like good luck, right?
It's very hard for PMs and designers to participate in anarchic FOSS sort of projects at all.
Like maybe them creating like wonderful graphical explanations and sort of like, you know, helping people chew on this or even trying to explain to them what this does.
My radio sort of clarified to you, James and whoever else is championing this, like how to best sort of inform people about it, how to create the correct narrative for this.
Because so far, I think we're doing a disservice, right?
Like we've sort of, oh, it's CTV, oh, it does this, oh, it does that.
Like people don't get it.
It just sounds like we're gonna have some insane thing on Bitcoin.
I mean, I was scared of CTV when it came out.
So I don't know.
I feel like like the education part is going to be like 90% of the problem.
You know, like the actual code is the smallest part on something like this.

Speaker 1: 01:26:03

That's right.

## Multisig, OP_VAULT and improving HODL features

Speaker 1: 01:26:04

As an aside on CTV, I think maybe people understandably got confused between CTV and Sapio.
And Sapio was like a really big, wide-reaching, futuristic system that Jeremy wrote that, frankly, was very complicated.
And that's often kind of what he would demo when he would go out and talk about CTV sometimes.
And I mean, I get why he did it because he had a bunch of use cases that were kind of cool and, you know, like interesting, But that was a big complicated system And so I think people maybe kind of got lost in the fact that CTV isn't safe.
You know, CTV is just this really simple primitive

Speaker 5: 01:26:39

Yeah, I think something that has me cautiously optimistic about Op-Vault finding kind of product market fit or at least having a better PR campaign with with everybody is you know now a couple years later multi-sig has gotten a lot more accessible and I think people are thinking a little bit more deeply about the custody of their coins.
I mean, you know, if you look at for example, what like Nunchuck is doing for example with like you can do a multi-sig that's a key on your phone, a key on a tap signer, and a key on like a hardware wallet like a cold card or something.
That's starting to become accessible in your pocket, multi-sig.
And I think once you play with multi-sig long enough, you start asking a couple questions.
Ask anybody who's doing a lot of multi-sig.
And two of the questions that they're trying to figure out are, how do I balance accessibility and recoverability?
And oh my God, I now have this treasure hunt that you have to do for all of my keys.
What happens when I hit by a bus?
And I think as multi-sig tooling and as better wallet software, whether it's Liana or other things that start incorporating vault-like features, starts working its way more into the ecosystem, people are going to look at things and say, man, this is great, but it kind of sucks that I have to either trust this company to run all these watchtowers for me, or I've got this like weird ephemeral key thing that I'm trusting, or I've got this like co-signing server somewhere, or like whatever the thing is.
And so I just wonder if maybe in, you know, call it late 23 or mid 24, when there's been more design and more code review of this and people are starting to like really talk about it, if more people in the community are going to be more receptive to the, you know, maybe the answer isn't just throw more keys at it.

Speaker 0: 01:28:36

Well, I mean, when you look at this, it's like, you know, it's a distribution thing.
On the first few years of Bitcoin, very few people had a lot of coin, right?
So there were very few people who actually had to care about serious amounts of money being held in an individual level.
Right.
And then like, sort of like you had this distribution, sort of like a distribution cycle, right?
Now there's a lot of people with a little bit of coin.
Then the price goes up.
Right now you have like a bigger cohort of people with coin.
Then now they have to care about security.
Right.
And Bitcoin keeps on going in the cycles where it's redistribution.
Right.
And then price goes up and then now people have to give a shit again.
So the issue is like, as soon as like the majority of people start to realize how fragile their setups are, right.
Like versus how much money it actually is worth is normally when the questions start to come.
You know, I always joke that like Ledger is a funnel sales for us, right?
Because they go, they buy a Ledger, they put the stuff with their shit coins on it and they don't think about it.
But then they go, Oh shit, I have this wallet, it's mixing my shit coins.
I don't have a passphrase on it.
I don't understand.
And then they start reading.
And then they start understanding and like, oh, okay.
Maybe I should put a passphrase on my coins.
Well, if I'm going to do that, how am I going to do that?
Right?
Like where does the metal go?
You know, Like now I have two pieces of metal.
Oh, I actually have to have a second piece of metal for the best phrase.
And that's not even to start touching to the multisig.
I absolutely hate multisig.
I use it, but I hate it because It is inherently flawed.
It's a terrible, terrible system.
You just essentially create multiple points of failure that have to be mitigated with some complex sort of alternative solution.
And as a majority of the people who are not necessarily super technical, but now understand a little bit more and have to give a shit because they have more money, start to sort of really get into this.
I really think OpVault's going to sell itself.
It's going to be like, oh, great.
I don't have to have 50 pieces of metal around the world.
You know, like I don't have to trust all the hardware wallets.
I don't have to do this.
I don't have to do that.
Like that to me is what helps it sell itself.

Speaker 1: 01:30:55

Couldn't say it better myself.

Speaker 5: 01:30:56

What I'm hearing is the real answer is we need to be telling people to set up really high cardinality multi-sigs.
And then once they do it and they say, wow, that sucks.
What do I do?
We say, well, we need to activate OpVault and you can throw all these keys out.

Speaker 0: 01:31:10

Yeah.
I mean, isn't that what the Wookiee wanted?
Everybody to use 12 DVDs with burning laptops from Walmart.
That definitely going to keep your coin safe.
All right, guys.
Like, is there anything else that you think should be part of this in case somebody is listening to this as the only thing they heard about UpVault?

Speaker 1: 01:31:27

I think all I'll say is I welcome a better proposal.
I think none of us are married to this thing.
Now that, you know, Greg and AJ have a big part of them is now in this proposal, which makes me feel good because, you know, obviously a little bit of self-consciousness about like designing this thing in isolation.
But if there's a better proposal, I welcome it.
I really just want vaults in Bitcoin.
I really just want better custody for every individual, every, you know, industrial operation that's doing interesting, good things with Bitcoin.
It's something we all care about and we need to make it bomb proof.
So really, however we get vaults, so far, this is the simplest thing that I've seen.
But however we get vaults, as long as we get them sometime in the next few years, I'll be happy.

## Final thoughts

Speaker 0: 01:32:14

Very cool.
All right, guys.
So how about a round of last final thoughts here?
Rindell?

Speaker 5: 01:32:23

Yeah, the thing that made Vault concrete for me was a couple of years ago, I read the docs for ReVault, which is like the company behind Liana and also an open source project for doing vaults at an institutional level.
They have a really nice architectural description of their system and it uses a bunch of co-signing servers and oracles and stuff.
But if you read that description and what it accomplishes, and then you imagine, what if we're able to kind of like get rid of all of the servers and all of the watchtowers?
I think that that's maybe if you've listened to this whole episode and you're like, I still don't really get like what vaults are or why I would care, I would encourage you to go and check that out.
That was the thing that helped me kind of get there.
But yeah, otherwise like read the awesome paper that James put together, read the BIP and pepper him with all of your feedback.

Speaker 0: 01:33:16

Greg.

Speaker 3: 01:33:18

Last thoughts.
I guess I would echo James' last thought, which was basically we're not married to this, but it's the best we've got.
And I'd love to see people's feedback, like directed feedback at the proposal as it is now.
There are some things I wish the proposal could do, but I just think Bitcoin's script is a little too limited to do it.
But maybe I've overlooked something.
And so looking at if we can make something better, I'd be all ears to

Speaker 0: 01:33:44

it.
Ben, the car man.

Speaker 4: 01:33:47

Yeah, I think a lot of the conversation around Vault or Covenants for the last few years has been like, you know, these are all cool proposals, but we're waiting for like the good one, the right one.
And this kind of feels like, you know, OpVault was like a really cool implementation in the first version, and now the second version is the culmination of all the proposals we've had over the years into one beautiful thing.
Similarly to with Taproot where we had these ideas of Schnorr and Mast and we figured out a way to make it beautifully work together and evolve this 2.0 version because it's kind of done that I think.
So that makes me really happy to see, okay, this is the official, well thought out version of Covenants that our great core devs have figured out.
Maybe someone will figure out something better, but to me it's looking great right now.
This is kind of our best approach that we've had so far, by far.

Speaker 0: 01:34:38

And James, any last things?

Speaker 1: 01:34:41

I can't improve upon what Ben just said.

Speaker 0: 01:34:44

So Where can people find information about it, where they should be reading and how they can find you?

Speaker 1: 01:34:50

Yeah.
So the BIP number now is 345.
So hopefully if you Google BIP 345, it should take you to everything you need to see.
In case it doesn't, you can go to my paper at jameso.be.vaults.pdf.
And that's a paper I wrote before the proposal was really fleshed out in any meaningful way.
So it's kind of just about the background, but it does link to the BIP and I think the Bitcoin Inquisition pull request.
And so, yeah, if you want to actually scrutinize the code yourself and get in there and get your hands dirty, there is a pull request up on AJ Towns' Bitcoin Inquisition project.
I can't remember the number for that, but it's up there with all the pertinent details and test cases.
I mean, if you want to see how vaults are actually implemented using it, the functional tests in there are pretty comprehensive and they show you how to set everything up.
It's maybe not the most legible because it's obviously meant for testing, but it's kind of feature complete as being an example.
So yeah, I mean, thanks again for having us and putting together a great panel and giving the proposal some airtime.

Speaker 0: 01:36:02

Fantastic.
Okay, guys.
As usual, another, I hope that we bored everybody to death and I think we've accomplished.
Thanks for coming.
This was fun.
Thanks for listening.
For more resources, check the show notes.
We put a lot of effort into them.
And remember, we don't have a crystal ball, so let us know about your project.
Visit bitcoin.review to find out how to get in touch.
You
