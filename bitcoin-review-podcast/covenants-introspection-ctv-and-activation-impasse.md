---
title: "Covenants, Introspection, CTV and Activation Impasse"
transcript_by: jeffreyweier via review.btctranscripts.com
media: https://www.youtube.com/watch?v=o8tjsVdiPUI
tags: ["covenants","vaults","soft-fork-activation"]
speakers: ["James O'Beirne","Rijndael","NVK"]
categories: ["podcast"]
date: 2023-09-29
---
## Introduction

NVK: 00:01:10

As usual, nothing is happening in Bitcoin and we figured, what a great day to put people to sleep in a one to three hour podcast.
We don't know yet how it's going to be.
We actually don't know how this is going to play out at all.
I have here with me Mr. Rijndael.
Hello, sir.
Welcome back.

Rijndael: 00:01:30

Hello.
Good morning.

NVK: 00:01:32

Good morning.

James: 00:01:33

For his like 600th appearance on the show.

Rijndael: 00:01:37

I haven't been sleeping well enough.
So I came back to record this so I can sleep to it.

NVK: 00:01:43

James, we can't acknowledge it.
Otherwise, we have to add him to the splits.

James: 00:01:47

Oh, yeah, fair.
Okay.

NVK: 00:01:49

And it goes to OpenSats.
So priorities, but...

James: 00:01:53

Amen.
Yeah, it's good to be back.
Hi, everybody.

NVK: 00:01:58

As I was mentioning earlier, CTV has given place to other things in my mind as of late, been trying to ship products and stuff, the things that pay the bills.
But I think we've crossed a chasm on the conversation.
I think most of the FUD is going away, especially in recursive covenants, the scary stuff.
And Ethereum is dying.
And I think a lot of people, especially bigger piles, are realizing that we don't have acceptable custody solutions yet for serious amounts of money that don't depend on third parties, especially corporate.
And things are changing, evolving.
And I think the space, the industry is maturing a little bit.
And I think the covenants conversation is going to be the next big thing.
And I think it's really going on that way.
So with that small little premise, why don't we talk about what is covenants?
What is covenants in Bitcoin?
And then after that, maybe we start talking about what we can do today and what we can't do today.
So who wants to give us a little premise on covenants in general?

James: 00:03:29

Rijndael, you warm us up, man.

## Technical overview of covenants

Rijndael: 00:03:31

I'll take a swing at it.
I think it might be helpful just to understand what Bitcoin script is and how it works.
Anytime you send a Bitcoin transaction to an address, what you're really doing is you are locking those coins to some kind of script.
Bitcoin has this really basic scripting language, and when you spend those coins you provide some input that satisfies the locking script.
The really basic one is, if you're using a singlesig wallet and somebody sends you Bitcoin, you say, in order to spend this Bitcoin I have to produce a signature that corresponds to the public key that encumbers my Bitcoin, and then you can spend it.
There's other conditions that you can use to lock your Bitcoin.
You can use timelocks.
You can say, this can't be spent until after some block height or after some time.
You can use hashlocks where you say, in order to spend this Bitcoin, I have to provide the preimage to a hash that I commit to when I lock up my Bitcoin.
You can add multiple keys together to do multisig.
You can combine hashlocks, timelocks, and multisig to do Lightning.
You can compose these things together.
The thing that's important to understand is that all these conditions or locks or encumbrances, they govern the input side of the transaction.
I send coins to James and there's a set of conditions that James has to satisfy in order to spend those coins.
But once he satisfies them, there's no conditions on how he spends them or where he spends them.
This ends up being really important if we want to have multi-party ownership of coins and you want to let people unilaterally withdraw their coins.
Imagine if we had, the three of us, we have some shared UTXO and all three of us sign together in order to move the whole thing.
But say that NVK wants to unilaterally exit without James and I co-signing, it would be really useful for him to be able to sign a transaction that takes out his portion of the coins and nobody else's.
And in order to do that, you need to have a locking script that says, if NVK presents his signature, then he can take this many coins to a given address, but he can't take all of them.
And that's not a thing that you can currently express in Bitcoin script.
You have to solve that with other means.

NVK: 00:06:25

Essentially what we can do now is, we can sign in, but we can't sign out.
Essentially, right now, you can do a multisig.
Standard P2SH kind of multisig, and send to an address, to an UTXO.
But the UTXO has no control on the way out, except for the script that you had before.
So, wouldn't it be nice if the UTXO had two things?
One is a capacity to essentially have conditions on itself on how it goes to the next hop.
And the second thing is some introspection.
So maybe it knows how much it's size is.
Because right now a UTXO doesn't know if the UTXO is one Bitcoin, two Bitcoin, or a SAT.
So it would be nice if he knew at least its size or maybe its place in time.

Rijndael: 00:07:25

Right.
And the application for this that really made it real for me, that made me really interested in covenants and clicked is the idea of a vault.
The classic problem in Bitcoin is, what do I do with my seed phrase?
How do I secure my wallet?
Because if somebody gets your seed phrase or whatever key backup you have, then they can just spend all your money.
There's no way for you to say, my money can only be spent in a particular way.
What I think you'd actually like to do is say, I've got my vault, I've got my deep cold storage and it should only go from my cold storage to my hot wallet, or from my cold storage to my exchange account because I'm selling or something.
You want to be able to restrict how the funds come out of your cold storage so that if somebody compromises the metal seed phrase you have buried under the tree or something, then they can't just run away with your money.
There's not a way to do that in Bitcoin at the script level right now.
You have to do that with hacky pre-signed transactions that we can talk about.
If you think about this idea of exactly what NVK just said, where you can have a transaction introspect its contents and set rules on where it's sending coins, how many coins it's sending, the shape of the output of the transaction.
Then you can start building more interesting self-custody solutions.
And then we can turn that into other stuff too.

NVK: 00:09:06

Even if you go back in time, pre Bitcoin, even pre fiat.
There's essentially two main things that people try to do when they have an important asset, or an important item in volume inside something.
They wanna be able to do what's called velocity.
A velocity essentially dictates that you have a quantity per time that comes out.
For example, in a silo, when you have all your grain there, you choose your velocity by adjusting the size of the door.
Because you don't want all the grain to come out.
Before, for example, old banks would have a tiny little door.
So nobody can stick a gun in and shoot, but also there is a maximum amount of things that can come out from one side to the other.
And what I think the scripts really do is it resolves the HSMs that banks have been using for ages.
And everybody else in industry similar have to do this, which is, can I add some very world compatible policies to my spending.
Please don't let any more than one Bitcoin per hour leave this vault.
It really is not that complex when you actually come down to earth with very mundane kind of examples.
Because if somebody gets hold of those keys, you don't want them to drain the vault.
Maybe they just take a little bit out until you find out.
And you really mitigate risk in that sense.

Rijndael: 00:10:53

And if you combine that with one of the two main things that Taproot gave us, the ability to more easily compose multiple policies together.
You can imagine having a policy where you say, with this one key I have some velocity control.
I can only spend money to a particular address, or I can only spend it some unit per some number of blocks.
But then if I combine that with a second key, then I can override that velocity control.
And so you can say, if I turn all of my nuclear keys at the same time, then I can spend all of the money.
But otherwise I have this very constrained flow out of my vault.
And this is probably one of the more broadly used uses for Bitcoin is savings.
Store of value and custody is the killer feature for Bitcoin right now.
And the ability for people to more easily protect their Bitcoin, is a set of features that I think we should be pursuing and investigating.

James: 00:11:55

But to just underline the general point of what covenants are, I think that word introspection is probably a better description of what we mean when we say covenants.
There are a lot of Bitcoin developers behind the scenes who get mad at the branding of covenants because it has negative connotations.
But what you guys said is right, which is that covenants really just increase the scope of what we're able to look at from within the script interpreter when we're spending a coin.
And that winds up oftentimes being on the output side.
But in a sense, we already have a timelock which is almost like a covenant because that's not necessarily on the input side.
You're looking at the end lock time in the transaction.
So we're already looking at some things that are outside of the witness.
We just want to look at more things so that we can do these interesting and vital applications like vaults, like congestion control, which I think is going to be increasingly important when we start scaling to second layers and want to provide safe exit for everybody.
A lot of the scaling solutions that have been proposed in the last few months.
Pretty much every draft, for whether it's Ark or John Law's Timeout Trees, they all use this, these covenant primitives of being able to say, I want to be able to commit to spending to a certain set of outputs without needing a signature.

NVK: 00:13:38

Right now in Bitcoin we have this very raw way of handling transactions.
You essentially throw your gold into a bucket and you hope that it lands in the bucket and stays in the bucket.
And if you ever wanna take it out of the bucket, you just turn the bucket upside down and whatever is in that bucket comes out.

James: 00:14:01

It's all or nothing.

NVK: 00:14:02

That's it.
That's a very cool, amazing primitive, that we finally figured out how to do with computers.
But it really limits us in a way that is detrimental to the ultimate goal, which is replacing central banks.
We're not even getting into the shitcoining idea, velocity, payments, fuck payments for this conversation.
None of that.
We're talking about just pure, unadulterated, store of value here.
If you just think of that, what is the ultimate goal of a store of value?
It's store the value safely.
And make sure you don't lose the value by losing the money.

## Watchtowers

James: 00:14:41

If you want to be a global reserve asset, you have to have an absolutely bombproof pattern for custody.
A setup where if you follow the instructions the right way and they're not terribly complicated, that you know you're not going to lose your coins.
If you have your coins vaulted and you have a certain number of watchtowers, you just know that there's no way that those coins are going to get stolen.
I think we need that.

NVK: 00:15:05

You don't even need watchtowers.
You don't even need to get that complicated.
You can have a watch-only wallet.
That might tell you from the mempool that there is a transaction being tried.
I know that's what a watchtower does.

James: 00:15:22

Different kinds of watchtowers.

NVK: 00:15:24

But when we say these big words, we're now thinking, oh my God, watchtowers, it must be some other crazy, complicated galaxy brain thing.
It's not.
It's just a fucking wallet that watches for transaction.

Rijndael: 00:15:37

Somewhere there's a watch-only wallet.
And if it sees a transaction happen, it broadcasts this clawback transaction and that's it.

NVK: 00:15:45

We have a dog that barks.
If he sees the wolf, he barks.
There is nothing more to it.
It is not related to changing Bitcoin.
It's not like some of the lightning crazy shit.
No, no, no, no.
This is very, very simple.
You're just watching for transactions related to you on the mempool.
Nothing else.

James: 00:16:05

Right.
You got a 19 year old intern sitting there refreshing mempool.space and that's your watchtower.

NVK: 00:16:10

That's it.
Yes, they are the watchtower now.
Look at me.
I'm the watchtower now.

## Use cases for vaulting & scripts

Rijndael: 00:16:16

Pretty incredible.
Because without that kind of primitive, some kind of vaulting primitive, what we have right now is if you want to hold a lot of Bitcoin, you need to have the most paranoid lockdown security setup in the world to make sure that one bad event doesn't happen one time.
Because if it happens one time, you're done.

James: 00:16:38

And that's a centralizing force.
So every rich guy ever is going to say, oh, I got to take my coins to Coinbase.

Rijndael: 00:16:47

I gotta outsource this to the guy that has all the HSMs and has all the armed guards pointing guns at each other around the HSMs in order to protect this.
But if we had some vault setup, you could have a $3 wall art with a wifi chip and it plugged into your wall.
And if the bad thing happens, that thing broadcasts a single transaction and you get all your money back.

NVK: 00:17:11

There's two problems here that I think are important to separate.
One is you still need things that create very safe key material.
You still need to create keys that are very, very safe.
And we still have to go through crazy hoops to do those things safely.
You're throwing your dice on your Coldcard and you create your key material.
But we wanna make the other parts of it become less problematic because of the rest of the stack.
The business logic right now is completely merged with your main key.
Which is a huge fucking problem because remember, if you just assume that the stack with the deterministic build and shit on your hardware wallet, is all kosher.
You know your keys are good.
But right now the problem is every time you want to sign for like 1% of the stack that's being protected by that, you have to put the whole thing at risk.

Rijndael: 00:18:17

Yep.
You gotta dump the whole bucket out.

NVK: 00:18:18

Everything.
Which is a huge fucking problem.
If we can separate this business logic for lower amount transactions from your total bucket pile key material we win huge.
It's a huge improvement.
And like Rijndael was saying, and James you were saying, you have the centralizing force, BitGo exists because corporate, or extremely large holders, when you are telling your people who legally and logically maintain the policies on how you do stuff so you don't get robbed and you have insurance.
Nobody with real amounts of things do things without insurance except us insane people in Bitcoin.
You need to check some boxes.
They know through actuaries, through time, through history.
If you don't do certain things in a certain way, we have extra counterparties.
You will lose the money.
You can't have Michael Saylor have the coins in a single hardware wallet because he runs the company and he's the executive of the company.
You can't do that.
There's other shareholders.
And the way you find accountability, and you find audits on logs and all this stuff.
Anything that's happening is by having counterparties, having other parties that co-sign.
They will have different incentives.
Maybe they are co-signing solution like BitGo. And their incentive is make sure that everything is accounted for and doesn't get signed until you meet some threshold that you set with them to begin with.
We can do all this with scripts.

James: 00:20:00

Right.
And that makes it into a low overhead process that many, many, many people can do instead of a few specialized companies that are able to hire tons of operations people to do this stuff.
But a necessary prerequisite to getting to that point is to enable some kind of a covenant in Bitcoin.

Rijndael: 00:20:20

Not only does it help make it more accessible, but I think it also helps with the censorship resistance and permissionless aspect.
If the only way you can safely hold a large amount of your value in Bitcoin is if you're in a position where you can have a contractual relationship with a very well-operated service provider.
Then over time, especially in certain regulatory regimes or in certain legal scenarios, that ends up shutting out a lot of people where they say either I have to hold this asset in an incredibly risky way or I have to not hold this asset.

NVK: 00:20:57

Or KYC.
Most people in Bitcoin don't want to KYC because you know KYC is the crime.
If this is assets you own under jurisdiction that allow you to own them so you're not breaking any laws you're not doing anything wrong even though we can argue about that stuff.
But just following within the fiat universe that we live in.
You're in a position that you can do this stuff by yourself.
You don't have to report to anyone.
Right now you can't use BitGo because they require KYC.
Most of the solutions do.
And then you have the privacy aspect too.
Because even if you find a non-KYC co-signing service out there, they still have full visibility over your coins.
It's the prerequisite of how the scripts work right now.
All this stuff is a huge problem.
And we can get into the current issue with lock time transactions.
Because right now, if you want to do some stuff, you kind of can using a degrading multisig or something like that.
But every time you spend, you have to reshuffle all the coins again, which makes it unusable.

Rijndael: 00:22:12

Let's unpack that a little bit because a lot of times when I've talked to people about, hey, we need some kind of covenant to do something like a vault.
What people will point to is, you should do a decaying multisig.
The way that that works, if you're one of the three people who aren't asleep right now, and you haven't heard of this yet, is imagine you have a couple different spend paths in your tap tree and you say, right now, my coins are in a three of three multisig, but after three months, I can use a different path where I can sign with two of those keys.
And then three months after that, I can sign with one of my keys.
So the idea is that normally it takes three keys to spend my coins, but if I lose one of them, I just have to wait.
And if I lose two of them, then I wait longer.
And folks want to do this for inheritance or just for more flexible multisig or key recovery.
And the problem there is that that timer of having to wait starts as soon as the UTXO is created.
So if you're just hodling coins in your wallet, then after three months your security degrades to a two of three and after three more months it degrades to a one of three.
And so if every month you're buying Bitcoin and throwing it into your wallet, then every time a UTXO gets to be two months and 28 days, you need to go and do an on-chain transaction to effectively reset the timer.
And when you start talking about large amounts of money or operational complexity, I think that starts to be a non-starter.

NVK: 00:23:51

It's hopeless.
I fucking hate it.

Rijndael: 00:23:52

Yeah, and when fees go up and shit gets expensive, it's going to suck.

NVK: 00:23:56

I love that people are trying, but it doesn't work.
There's a reason why nobody's using it.

James: 00:24:00

Yeah, you've got to dig up all your keys on a periodic basis and activate your spending capacity on a periodic basis.
And that's always an opportunity for theft or a security leak.

NVK: 00:24:11

If you're a crazy person like me if you want to spend anything, it would take me probably a couple months, I have to travel to different countries, wait for things, it's crazy shit.
Wouldn't it be cool if you can represent your trust as a script and you just essentially wash your fucking hands when you die.
This is how it works.
It's a little crazy, but totally within the realm of possibility.
If you have some decent introspection on this.

James: 00:24:49

And in some ways, one of the things that OP_VAULT does is like Rijndael was saying when you spend the coins into that structure, you start the time lock.
All the covenant does in OP_VAULT is basically say, we're gonna delay that until one spend out further so that when you spend the coin from there, then the time lock starts, then that clawback period starts.
So you're just kind of delaying that decay process.

NVK: 00:25:20

I like to say that timelocks should be reactionary.
They shouldn't be part of the initial transaction that you want to make.

Rijndael: 00:25:27

What you really want to do is you want to start the timer when you initiate the spend, not start the timer when you receive the money.
And what we have right now is you start the timer when you receive the money, and what you could do with OP_VAULT is say, I want to do a withdrawal.
There's two ways for me to do a withdrawal from my vault.
One of them is I take the transatlantic flight, I go and get all of my keys and I can spend my money immediately.
Or, I have a singlesig key and if I spend that, that starts a three week timer.
And during that three week timer, I can push a button and cancel it and claw my money back.
Or, if I don't cancel it, then my money goes where it's supposed to go.

## Covenants as a solution to third party custody

NVK: 00:26:10

Think about how stupid it works right now.
When you have a safe, a deposit safe.
Normally when you put the money in the hole, it just drops inside.
And then when you want to open, normally you have a timer.
So you put in the pin and then you have to wait like three hours to open or something.
Right now it's the opposite.
When you drop the money, the money takes like three hours to drop, but when you want to open it, it just opens.
It's just completely stupid.

Rijndael: 00:26:44

Or, another example.
If you have a Coinbase account or a Gemini account, they both have this feature where you can say, I have a whitelist of addresses, and I can withdraw my coins only to those addresses.
And if I want to add a new address, then I have to do MFA and I have to wait a seven day waiting period before that address is active and I can withdraw to it.
And so that way if somebody compromises my Coinbase account, they can't just steal all my money.
That's a great feature.
If you want that feature, you have to go with a KYC custodial holder of your Bitcoin.
What I think we would all want is for any Bitcoin wallet that anybody goes and builds permissionlessly in the world to be able to have that functionality and have it be enforced by Bitcoin consensus instead of having to rely on business logic of a centralized custodial server.

James: 00:27:43

Totally.

## Covenants and censorship risks

NVK: 00:27:46

It's an easy conversation here because the three of us agree.
What is the steel man argument against covenants?
So far I heard, you could have issues where, the government forces you to participate in some ...
well, they can do that with multisig now.

James: 00:28:01

And it's much more practical with multisig.

NVK: 00:28:10

Way more because you want the opposite.
You want to participate when you sign and not after.

Rijndael: 00:28:18

Maybe we can unpack why multisig is actually a great solution for the state wallet for Fedcoin and why covenants would be bad for Fedcoin.
The risk here that people are worried about is that there's some regulatory crackdown and the government says you must receive your Bitcoin into a wallet that enforces this covenant and this covenant restricts who you can send coins to.
So if you eat too much meat, if you say wrongthink on Twitter, then you're going to be on the blacklist and James won't be able to send me coins.
And if I have a good enough social credit score, then I'll be on the whitelist and James can send me coins.
That's the threat that people are worried about and they're worried that introducing covenants will open this new vector for this kind of control on Bitcoin.
The thing is that with all the covenant proposals that are being seriously talked about like CTV, you have to exhaustively enumerate all of the different destinations and all the different kind of shapes of transactions that coins can take at the time that you receive those coins.
So one of the things that that means is, let's say that you're some government agency that's maintaining this whitelist based on social credit score or something.
Every time that whitelist changes, you would have to get everybody to respend their coins to a new version of the covenant that includes the new whitelist.

NVK: 00:29:53

And they're going to fuck up.
This is the stuff they fuck up.

Rijndael: 00:30:00

100%.
Screwing up a list of things in a database is very on-brand for bureaucratic fuck-ups.
What you would much rather do, that's one problem, and then there's other problems.
Not only do you have to enumerate all the destinations, but you also have to enumerate all the change addresses.
Managing this whitelist through on-chain rollover of UTXOs is just a non-starter.
It's expensive, it's slow, it'll never work.
If instead you did something where you said, for Fedcoin, James, if you want to be compliant, you have to receive coins into a wallet that does a two of two multisig.
And you hold one key in your Fedcoin wallet, and then me, the government, I hold a second key.
And then what I do is I just run a co-signing server.
And the whitelist is just a database.
It's just a plain old MySQL database.
Whenever Rodolfo gets kicked off of the list, he's no longer allowed to receive Fedcoin, I remove him from the whitelist.
And then if James wants to send him Bitcoin, it sends a cosigning request to the server and the server says, nope, you're not on the whitelist.
He goes, send me coins and I'm a good citizen.
So it says, yep, he is on the whitelist and it just cosigns it.
You could update that whitelist hundreds of times a second.
It doesn't have an increased on-chain footprint.
You don't have to roll these things over.
Blockstream actually already has a product like this.
It's called AMP and it's used for issuing regulated assets on Liquid.
So if you want to buy a stock on the Liquid network, they only want you to be trading stock with other people who are accredited investors or whatever.
So they have a co-signing server that restricts who the token can go to.
So we already have the technology to do Fedcoin today in a more efficient way and a more operationally sound way than using covenants.
So it doesn't matter.

NVK: 00:31:52

Personally, if I were to do Fedcoin, I would do it on Ethereum.
Because it's actually quite perfect for it.
It uses accounts, it doesn't have UTXOs. So you can keep an account on the whole person's pile of an asset.
They have the whole shebang for it.
No wonder they're probably right now knocking on the door of regulations.
Can you please use our system for it?

Rijndael: 00:32:13

There's already regulated stable coins on it.
The account thing is actually a big deal.
If you want to be able to look back and see transaction history, that's very hand-wavy in a UTXO system.
In an account-based system, you just look at the transaction history for an account and you say, yep, here's the NFTs that you bought.
Those are hate speech.
So you're no longer allowed to receive your stipend.

NVK: 00:32:37

That happened with Tornado Cash.
Because people sent unwanted Tornado Cash to people in their accounts.
Just so people understand the difference.
Think of the UTXO system as essentially we have 21 million coins, literal physical coins.
And we just send and receive these coins.
They are not mine, really.
They're just part of the network and I happen to own them right now.
But it's really akin to gold in that sense.
The account system, on the other hand, is essentially how fiat works.
It's a ledger based system per owner.
The owner has its own ledger.
It's fucking terrible for privacy.
This is all interesting.
Is there any other steel man for...

Rijndael: 00:33:23

I think the best argument that I've heard against specific proposals like CTV, which is I think the one that probably, I'm going to go out on a limb and say CTV probably has the most consensus out of all the covenant proposals right now.

NVK: 00:33:38

Let's just have opinions, it's okay.

Rijndael: 00:33:40

Yeah, for sure.
And I think the strongest argument that I've heard is maybe it doesn't go far enough.
Maybe we want a more general covenant.
Maybe it's too restrictive.
And if we're gonna go through the social activation energy of doing a soft fork, maybe we should make a better covenant.

NVK: 00:33:59

But that would never happen because now it's too big and everybody's going to have more reasons to bike shed and hate on things.
It's hopeless.

## Risks of major Bitcoin changes

James: 00:34:07

That was actually the impetus for OP_VAULT.
But let's put a pin in that and go back, one concern that I can think of that's reasonable is anytime you're adding functionality to the Bitcoin script interpreter or changing it there's some level of risk there.
And I think in any case, you do have to be very diligent about looking at the proposed change to the script interpreter and saying, well is this going to increase computational requirements for doing validation?
Is there some new avenue we've introduced for DOS?
Does this require more caching or whatever to make sure that the validation time doesn't actually blow up when you use this new feature.
And when Jeremy introduced CTV, I was like, I'm going to go pore over this thing and see if I can actually break it or find some kind of critical issue.
And what's funny is that for all the reputation and ire that CTV has accumulated over the years, in its early days anyway, the change is really, really simple.

NVK: 00:35:20

It's funny.
I started as a CTV liker and then I became a CTV hater because of how it started to get pushed and everything else.
And then I became a CTV lover again.
I went through the whole roller coaster of sentiments around it, because I think Sapio and what you can do with CTV once you go galaxy brain really confused me.
And I don't have the bandwidth to go fucking review it, and I think he muddies the water I think if we had just kept it to what it is and here's where it goes as opposed to look at all the insane shit you can do with it if you do it this certain way.

James: 00:36:10

I think Jeremy got tired of talking about raw CTV because again, it is so simple.
And he develops Sapio, which is this very space age smart contracting platform that compiles down to Bitcoin script.
And he started showing that off and people looked at that.
And that's a very complicated system.
And I think that scared a lot of people because they weren't made aware of the distinction between the underlying script primitive, which is CTV and Sapio.

NVK: 00:36:42

I transverse both the Luddite camp and the non-Luddite camp when it comes to Bitcoin changes, the ossification versus non-ossification.
And what truly scares me with Bitcoin changes is we have a thing that works.
And it's kind of a fucking big deal.
It's the only thing we have.
And my bags depend on it.
I am really scared of unknown, unknowns.
And it's very hard to know what happens.
We saw the Taproot thing.
I feel like a lot of people got taken for a ride on Taproot.
They couldn't understand it.
And they gotta accept it because the devs say it's okay.
And then we had the dick butts show up onchain.
And people are like, look you can have unknown, unknowns.
It made absolutely no difference.
Once people understood it's all dying down, the economics kills these things.
But it could have been worse to be fair to people.
It could have been worse.

James: 00:37:46

Oh, for sure.
And Taproot was basically like lifting the engine out of Bitcoin and putting a new engine in.

Rijndael: 00:38:02

SegWit and Taproot were both huge upgrades that kind of fundamentally change how Bitcoin works.
And CTV or APO aren't.

NVK: 00:38:14

CTV is akin to ...

James: 00:38:17

Check-locktime verify or CheckSequenceVerify.

NVK: 00:38:18

No, not even.
It's more like an opcode.
You just have a little space there, it makes no fucking difference.

Rijndael: 00:38:27

And what CTV does is it takes a whole bunch of fields in the transaction.
And we can rattle them off, but it takes a bunch of fields in the transaction and you hash them.
And then you say, check template verify, and you provide that hash.
And when you go to spend those coins, if those fields in the transaction hashed the same value as what you committed to, then the transaction is allowed.
And if they don't, the transaction is denied.
It's a very simple mechanism.

NVK: 00:38:52

Here's the worst case scenario for CTV.
People YOLO their scripts and they can't move their coins anymore, which is going to happen.
But that's great.
That just makes Bitcoin be more deflationary.
Seriously, I already believe that 20, 30% of all Bitcoin cannot be moved.
Because people just don't know yet.
They cannot move their coins.

Rijndael: 00:39:14

Yeah, for sure.

NVK: 00:39:15

But with CTV, it's just more of the same.
You don't have to use it.
It's backward compatible.
And it doesn't change the incentives.
It doesn't change incentives when it comes to mining.
It doesn't change the incentives on any of this stuff.
We don't have economic incentive change that you wouldn't happen already if you couldn't move your multisig because you forgot the script or whatever.

James: 00:39:39

Another interesting thing is that CTV is basically just a hash comparison.
And that's like upwards of 20 times faster than elliptic curve operations.
So the CTV opcode itself is way faster than a Schnorr verification.

NVK: 00:39:53

Do we need a new name for it?
Hash check.

James: 00:39:56

I don't want to.
It's fine.
We've done so much deck chair rearrangement, I feel like with this stuff that people just need to grow up, put on their big boy pants and come to grips with the existing branding and take it for what it is.

## Quantifying the scale of change in code

NVK: 00:40:13

Do you think it would be more helpful if we can get the TXHASH people, the APO people and whatever fucking thing people wanting to be more on board with this and all this stuff you guys are proposing, is not going to fucking happen.
I am certain that TXHASH is not going to happen.
It's too out there.
It's too much code.
Maybe if we debate for another 10 years, it's not impossible.
Let's put it this way.
But realistically speaking, and imagine Bitcoin in 10 years, the amount of different people who own it and are not willing to change it.

James: 00:40:48

Yeah.
Well, bit of news.
I spent the last week putting together a branch on Core that has CTV, APO, and OP_VAULT.
And it's 6,000 lines.
That's not a big change.
That's including all the test code.
The test vectors and all that stuff.

NVK: 00:41:09

Outside of tests, how much are we talking about here?
Like a third?

James: 00:41:15

I think probably two thousand lines.

Rijndael: 00:41:22

And a lot of that test code is like Python, which is more verbose because it's wallet setup.

James: 00:41:28

A lot of the CTV code is just these raw transactions and big JSON files that Jeremy generated to make sure everything is cool.
A lot of the APO test codes, there's a fuzz test case in there.
So it's really padded out with a lot of test code.
So these changes are small.

NVK: 00:41:45

But here's the counter argument to that.
Changing the block size was a single number change there.
For people to understand is the smaller literal character change in terms of code makes it a lot easier to review.
But it doesn't eliminate some other issues.
Because you could change a tiny little thing and cause massive fucking problems.
But that's what tests are for.

James: 00:42:19

Totally.
And the size of the code makes it more readily comprehensible, but I just brought that up to compare it to, and this is the way opposite end of the spectrum, for Simplicity the proposed change set into elements is something on the order of 80,000 lines.
And I know that allegedly comes with a lot of test code and proof verification and all that stuff.
But scrutinizing something like that is a much, much, much bigger proposition.

NVK: 00:42:48

And it's also a single source.
It comes from a single company.
We like them, but it's much harder for you to review something in terms of face value when it comes from a single entity.
If you had like 10 entities that hate each other writing that code, it'd be much more believable, much more trustworthy on face value.

Rijndael: 00:43:08

I would argue that the actual amount of code that's gonna be needed to make that thing useful is probably gonna be another order of magnitude larger.
Cause the thing with Simplicity is it's this very low-level scripting system built out of these algebraic combinators that you assemble together and then they create predicates for your scripts.
In order to actually make software out of that, we're going to need higher level languages and libraries to actually build tooling for it.
If we have, call it CTV and VAULT, you can hack four lines into Peter Todd's Bitcoin Python library and start using it.
You can start building a wallet on top of that.
If you have APO, you can hack a new SIGHASH flag into your favorite Bitcoin library and you can start doing APO things.
So it's 7,000 lines and that's enough for people to start using it.
I would say something like Simplicity, there's probably going to be other languages and libraries and tooling that we're going to need on top of it.

Rijndael: 00:44:32

I did read Luke wrote consensus logic for BIP300 for drivechains.
And that's not a ton of code, but that comes with a whole bunch of new miner incentives and a whole bunch of new economic incentives for Bitcoin to behave differently.
And it introduces a brand new security model.
It's actually a pretty big change.
Something like CTV, if you screw up you might not be able to spend your coins, but that's not going to affect my coins.
I think one of the big differences between something like Bitcoin and something like Ethereum is that Bitcoin transactions don't go and mutate a whole bunch of global state.
I can't write a locking script that messes with James' coins.
I think that's a core invariant in Bitcoin.
And none of these proposals that we're talking about change that dynamic.
I might lock myself out, but I'm not going to lock James out.

NVK: 00:45:29

That's right.
There is no socialization of your transaction here.
There is no externality to them.
You're not making everybody do anything else.
It's more akin to you just happen to use addresses that you mined and they all have like five A's at the end.
It's irrelevant to the rest of the network.

James: 00:45:53

The only way that it would affect other people is if the validation complexity went up somehow and you could kind of abuse these new op codes, but that's been proven not to be the case.
With APO, I don't think that's the case.
So, we talk about TXHASH, and for people who haven't heard of TXHASH, all TXHASH is, is a way of ...
So, CTV takes certain parts of the transaction, rolls it into the hash, and then does the comparison.
With TXHASH you can kind of select different parts of the transaction to go into that hash.
So you have something that's in theory more flexible, but the problem is because you can do all these different hash combinations, then you have to start worrying about what's called quadratic hashing attacks, which is where you select a bunch of different incantations of that hash in the same transaction.
And then all of a sudden, the validation engine has to do a bunch of work to do some kind of a combinatorial selection of all the hashes that are possible with the transaction.

## TXHASH

Rijndael: 00:46:53

So I thought with TXHASH, and maybe I'm behind on this, the original TXHASH proposal was you'd say OP_TXHASH and then you would pass a bitmask basically of which fields to select to go into the hash.
And the idea was that at a consensus level, only certain values of that bitmap would be allowed.
And so the idea is that on day one, when it got activated, the only permissible value is the exact same set of fields as CTV.
So in my mind, it's kind of just rebranding CTV.
CTV has too much baggage with a certain sect of people on Twitter.
So we're going to rename it and add a bitmask.
But the idea is that in the future we could soft fork new allowed values for that bitmask.
And so I assume that in order to get people to do that soft fork, you'd have to show them that this thing doesn't open you up to quadratic hashing.

James: 00:47:49

Three points there.
Number one, the two main distinctions of TXHASH from that CTV use case that you're talking about is, number one, you've got data loss because you've got to provide an extra parameter just to do the CTV hash.
Number two, TXHASH would be a Taproot only opcode.
You have to use Taproot.
And that means it's not as space efficient because it turns out that the most efficient version of CTV is doing a bare CTV so that you just have the 32 byte hash, the two byte opcode.
So you're 34 bytes, not even a Pay-to-Script-Hash, it's just a raw script.
So if you wanna do congestion control, that's the most efficient incarnation of that.
But then the third point is that a lot of people don't realize that CTV actually was designed with upgradability in mind.
So what happens in the CTV rules is if the hash that you pass as the argument is 32 bytes, it does the default CTV hash.
But the way Jeremy designed it is, if that hash is more than 32 bytes, if there's an extra flag on there, it's OP_TRUE.
So if you wanna soft fork in more template hashes, you can if you want to.
So it's all the same stuff except TXHASH is less space efficient.

## Simplicity of CTV

NVK: 00:49:04

The way I like to think about this is more like CTV is essentially OP_RETURN.
You're just storing 32 bytes there.
And all we're saying is that for a transaction that says it's a CTV, check that that hash matches, that's it.
There really is nothing else to it.
And this is not to minimize tertiary effects kind of thing, but, it does make it a lot easier on the code side to review and make sure that we're not causing technical bugs.
Economically speaking maybe there's more conversations to be had.
I'm satisfied.
But maybe maybe people can still argue more about the soft stuff.
But on the hard stuff, it's pretty simple.

James: 00:49:58

Yeah.
And it's been picked over by everybody.
Everybody wanted to find a problem with CTV and the code's been out there unchanged for so long.

Rijndael: 00:50:06

And if I remember right, there's like a five Bitcoin bounty out there if you find a bug in it.
To this day.

James: 00:50:12

To this day, yeah.
If you find a sizable bug with CTV, you get something like five Bitcoin from the Lincoln Labs people.

## The consensus deadlock

NVK: 00:50:19

As we all know, for as much as we like to say Bitcoin is decentralized, it kind of isn't when it comes to Bitcoin updates and things you have to get the approval of the main original gray beards.
G.
Max retired, essentially.
I'm sure he will have an opinion on Reddit.
You have Wuille, Poelstra maybe a little bit less but, what's the state of consensus from the wizards?

James: 00:51:10

I call this the consensus deadlock because we're in a situation right now where the people who have led the last few consensus changes to Bitcoin really don't want to weigh in because they have felt like they're encouraging this muscle memory in the community that they're essentially the implicit benevolent dictators and that they have to bless every new change.
And that's obviously antithetical to what Bitcoin is supposed to be.
So that's their choice.
I still wish that some of the people would involve themselves to an extent, but they don't have a willingness to.
So we're in a position now where there's kind of a credibility vacuum.

NVK: 00:51:46

I think the other issue, too, is aside from people being burnt out, which, by the way, I believe people should be burnt out.
I believe we should be excruciating.
So horrible.
Maybe you might disagree with me, James, but I want people to literally hate working on Core Bitcoin.
It needs to be so awful that you're either a spook or you're masochist or both to want to be there.
And it's so intense.
And it needs to be that way.
Because then you have less social attacks on it.

Rijndael: 00:52:23

Well, maybe another way of saying it, is the only time that you go and start changing things on Bitcoin is when you have no other option.
You're like, there's no more pleasant way for me to do this.
So I'm going to have to go and change Bitcoin.

NVK: 00:52:38

That's right.
You're in a spaceship.
You really don't want to do a spacewalk because that's how everybody always dies.
They have to go outside to fix something in their engine or something.
And then they die.
They fall into the vacuum of space.
And I feel like every time Bitcoin has changed, the people who went to walk outside, they fix the thing and then they got swallowed by the vacuum of space and then they never come back.
It's okay if people burned themselves out doing that one thing, and it's for the common good.
So we don't have those guys.
And in all honesty, I have a feeling that if we have those guys then the bike shedding would also start and unlikely to get anywhere.

James: 00:53:29

What I'll say is two things.
Number one is that I think vaults is something that's widely recognized as being really, really desirable.
The vaults have been talked about since 2013.
And I think every major contributor to Bitcoin at some point is, this is probably functionality that we need.
Otherwise, custodying coins is just too much of a crapshoot in the long run.
And number two, as people keep coming up with these proposals to do things like scale the Lightning Network, scale UTXO ownership, do vaults, people keep reinventing the need for CTV.
And I think it's just become obvious to a lot of the technical community, whether they're coming out and saying it explicitly or not, that we just need this primitive.
So the reason I started preparing this soft fork branch is because I think if something like that were proposed, there would be pretty good broad consensus that, maybe it's time to look at activating CTV and APO.

NVK: 00:54:35

Did you buy your helmet to walk in space yet?
This is gonna be your retirement project.

James: 00:54:40

Honestly, the social stuff doesn't really bother me that much.
Maybe because I think I make fairly limited claims and I'm not that pushy, I'm ready to take the spacewalk, I guess.
Mostly because I'm hoping it'll be a pretty boring spacewalk and I won't be offended if I get totally rejected.
And because I've spent enough time prototyping this stuff and working with it to say that it'll probably happen eventually.
And if it doesn't, that's fine.
I think it'll be to Bitcoin's detriment.
And at that point, I'll probably go and work on something else entirely.
But that's OK.
I'm I guess a little Zen about it.

## Social coordination and activation

NVK: 00:55:34

I think honestly the main problem is gonna be activation and how to do it.
Like I mentioned many times and I think most devs still cannot internalize it.
Speedy Trial is not something that passes the mustard in terms of how users and the economic nodes feel.

James: 00:55:52

So, tell me what Speedy Trial is.
Let's make sure we agree on definitions here.

NVK: 00:55:58

I think the problem really is you can't have something that does not have flag day.
People want the game of chicken.
You're trying to remove the game of chicken.
What happens with that is you show your hand.
All the devs wanna do is remove the game of chicken.
That's what Speedy Trial does.

James: 00:56:28

With soft forks in general, when you provide a way to coordinate miners doing the upgrade, I think it's a big misconception that the process is somehow designed to solicit the feedback of the miners or to ask for permission from the miners.
It's really not.
It's literally to coordinate the upgrade that we're going to do one way or another to make sure there's no chain split.

NVK: 00:56:57

Oh, no, no.
I understand.
That's what technically the code does.
The problem is once you get miners to coordinate before economic nodes, what it's really signaling is that the miners are choosing if they wanna do something or not without knowing how the economic nodes are going to go.

James: 00:57:21

But how do the economic nodes broadcast their willingness for a fork?

NVK: 00:57:26

Well, UASF, the way it should be.

James: 00:57:29

OK, so what, we're all going to go out and advertise via user agent that we want a certain fork.
Well, that's Sybil.
That's a Sybil attack.
There's just no good way of economic nodes saying, yeah, we all want this thing.

NVK: 00:57:44

And they shouldn't be.
I believe that part of the reason why Bitcoin was never successfully attacked is because there is not a clear game to activate anything, for somebody to game.
This messy chaos that is UASF, even though it feels dangerous, it feels like it could be sybiled or whatever, it forces true economic actors to coordinate out of channel.
Because trust me, everybody is calling each other meeting and trying to understand outside of Twitter and outside of the network.
What are you supporting?
Where are you going?
So it is literally forcing people to do that coordination out of channel.
And then you're not showing your hand to bad guys trying to push in a different direction.
They simply don't know the state of things.
So they risk their coins.
It's actually quite beautiful.
It is true chaos.
And state actors cannot game something that's chaotic.

James: 00:58:55

I think if there's broad agreement that we should do something with consensus, there's no reason to induce that chaos, risk chain splits and coin loss, and Bitcoin looking like an absolute shit show.
That doesn't make any sense to me.
UASF is always in the back pocket.
If miners drag their feet, like you can always UASF and the opposite is always true.
Let's say the miners get together and they decide to activate some fork that doubles the supply.
Well, guess what?
The economic nodes can run a trivial Python script that examines each block.
And if it violates their rule set, it runs invalidateblock.
The activation method is literally window dressing to make sure that there isn't a big chain split.
It's nothing more.
Because there's always the avenue to reject a bad consensus change if people want to.

Rijndael: 00:59:57

It's been a while since I've read BIP-8, but my understanding was the way that BIP-8 activations want to work.
I don't think we've actually done this yet.
But the idea is that you would run a LOT=true client.
So there's a drop dead date.
At this date, nodes will start enforcing.
And if the economic majority of the nodes are running that code, then this is now the will of the economic majority.
But you still have a miner signaling period to do early activation.
And that's not miner selecting.
That's miner signaling, I'm ready to not mine invalid blocks.
So that if you say the LOT=true date is two years out to give everybody plenty of time to upgrade.

NVK: 01:00:51

Miners are last.
They don't even know where their mines are.

Rijndael: 01:00:55

Right.
But the idea is that if we think that there's broad consensus before then, and if the miners are ready to upgrade all their software, then we don't need to wait the whole two years, but there's a drop dead date in two years.
That's my understanding of that mechanism.
Something that I've always thought would be interesting ...
if we think that a particular soft fork has broad consensus and we think that lots of people want to do it, we could go and solicit some donations from the community to put a wallet together to go and pay a miner to mine an invalid block once we think it's active.
Because there's no way for user agent signaling.
If you say, we're going to stick iLikeCTV into your user agent, it's trivial for somebody to go and spin up a million nodes on AWS and have this sock puppet consensus.
But if a miner mined a block that includes a transaction that violates CTV and that block gets forked off of the network, then we know that CTV is active.

NVK: 01:02:04

This is the problem.
We cannot use, until fiat is 99% of 99.99999% of the total world economic value.
And Bitcoin is just a spec.
We cannot use any system that allows for an economically stronger actor that has infinite money to fuck with it.
This is the problem.
They can do anything except make miners come out of the ground.
Because that's a physical thing that you have to manufacture and deploy.
And as we know, governments are not great at that.
It'll take them a little while.
And we cannot make anything that they could pay to go better ...
for example, with SegWit, we had the futures for the two tokens, which was Bitcoin and Bitcoin Cash on BitMEX at that time.
That was very useful because state actors didn't have any time to game that out.
Because it was a one-time thing.
It popped up out of nowhere, total chaos, spontaneous order thing.
If we make that part of the system now, we're essentially tipping the guys to prepare for that.
They'll get the funds ready and they'll sort that out.
And then you imagine they could totally kill that.
They can short the fuck out of one and long the fuck out of the other.
Because they have infinite money.
And now that futures market is completely gamed.
Because remember, these guys have disposable, burnable cash.
It's not like us.
They have real money.
You can't play that game.
This is one of the issues that I have.

Rijndael: 01:03:43

Well, it's actually even worse than that because the way that budgeting works in large organizations is if you want the same budget next year, you can't spend less money this year.
So you are incentivized to spend all of your budget.

James: 01:03:53

But hang on now.
I don't understand this, because how do you coordinate socially, which is a prerequisite to doing a fork, without publicizing your intent to do the fork.

NVK: 01:04:05

No, you publicize your intent.
But remember, there is a very, very large amount of economic actors that are fully quiet on any form of social media or whatever.

Rijndael: 01:04:16

I think the thing that NVK is saying is that you can't measure willingness or support through something that is gameable by an adversary with a lot of money.
So the example that I said of user agent signaling.
If I'm somebody and I want to tip the balance, I just go and spin up a giant fleet on AWS.

NVK: 01:04:39

Amazon.
Credit card.
Problem resolved.

James: 01:04:41

Have a huge AWS bill.

Rijndael: 01:04:44

And it's easy.
The thing that I like about, let's pay a miner to go and mine an invalid block, is that that's something where you're measuring support by looking at what happens on the network, which is ultimately the thing that matters.

NVK: 01:04:59

What if we had non-fidelity bonds?
That kind of really shows how much of the pile you have and how much you're willing to go.
Because then you can just show, look like 10 million Bitcoin is willing to go this way.
Five million Bitcoin did not vote.

Rijndael: 01:05:16

And so you're saying you lock up some Bitcoin in a timelocked CTV thing.
And if CTV doesn't activate like that, Bitcoin's up for grabs?

NVK: 01:05:24

Maybe.
Yeah.
I don't know.

James: 01:05:26

Somebody tried this back in the SegWit days.
They came up with this scheme where you could sign a message of support using keys that correspond to some out points.

NVK: 01:05:39

But it's still fully gameable too.
Because you can't measure majority unless you truly have more than X million amount of Bitcoin in a meaningful way, but it has to be ultra super majority.

James: 01:05:51

Proof of stake?

## Speedy Trial - good or bad for Bitcoin?

James: 01:05:59

I just want to be really, really clear for the audience and say that I think Speedy Trial again, has been victim to its branding.
And all it is, is basically a way of saying, if the miners and the users all agree that we want this consensus change to happen, let's just do an abbreviated period where if somehow within a few months, all the miners say, yeah, I'm ready to do this upgrade.
We can lock it in and wait even a longer period than BIP-9 had us waiting.

NVK: 01:06:24

Well, but what if we tack on pre Speedy Trial, there is a USF period in which everybody runs the client.
And maybe you make a transaction or something that, if the miners do go through a Speedy Trial, then those transactions are valid.
Therefore everybody agrees now that this thing got activated.

James: 01:06:48

No, but see, you guys are proposing hard forks.

NVK: 01:06:51

Yes, absolutely.

James: 01:06:55

Making a transaction that was previously invalid valid is a hard fork.

NVK: 01:07:03

You got to put some skin in the game.

Rijndael: 01:07:05

Wait, sorry, what, where was the proposal to make a previously invalid transaction valid?

James: 01:07:12

I think NVK was just saying you should lock coins up in a way that you have to activate CTV for the spend to become valid.

NVK: 01:07:25

Exactly what Speedy Trial is trying not to do.
I think this is the problem.
It's one of those things that code wise, it's not too hard.
It's not hard for us to program something that does this change very safely.
We know that.
The issue is, how do we satisfy the completely irrational chaotic part of what makes Bitcoin good?
Which is essentially the social sentiment towards where things are going and having this chaos being the firewall against the opposite of it, which is state actors.
State actors, again, cannot deal with chaos.
It's poison to them.
That's how the terrorists work.
They just cannot handle shit that's disorganized.
So being disorganized is good.

James: 01:08:28

I'm a crazy anti-government person.
I'm all for hardliners.
I'm all for securing Bitcoin against the state.
That's pretty much what I've devoted my career to at this point.
And I'm just for doing it in a way that's actually effective, which is, okay, tomorrow the state gets control of all miners and Coinbase and whoever else.
And they push out a client that doubles the supply.
What's our actual deterrence?
And that's literally the part of the economy that wants real Bitcoin runs a program that invalidates blocks that are not valid.
That's the deterrence.
Anything short of that is sort of meaningless.

NVK: 01:09:05

I think it's one of those things where, I agree with you intellectually.
But there is this intuitive part that's not being satisfied.
And I think that as most early Bitcoiners would probably agree is that there's a lot on this that we don't still fully understand, especially on the economic side of Bitcoin.
And it's very hard to satisfy that with, oh, here's a simple solution in code that will do the trick.
And maybe we just haven't explored this enough in terms of trying to find a more sane path for activation that satisfies both camps.
Again, Speedy Trial feels more like it's making the devs feel more safe and cozy, but I don't think they have fully satisfied the economic nodes.
And I think it shows.
You go ask around, people don't like it.

James: 01:10:18

People don't know what it is.
If you ask your average person on Twitter what Speedy Trial is they won't be able to tell you.
They'll say, oh, it's a way of quickly activating a soft fork, which is a very incomplete view of what it actually is.
I just think all of Bitcoin's development process is threading this needle where at one end of the spectrum, it's making changes too easy and enabling some usurper to come in and screw up Bitcoin.
But the other end of the spectrum, which we're at a real risk of traveling, is burning all of your human resources out and making non-contentious things impossible so that Bitcoin can't actually improve.
And we gotta be diligent of that.

NVK: 01:11:04

I think there's a little bit of nihilism there too, with the Core maintainers.
There's a lot of people out there that are perfectly fine with the state of the software.
And we could find people that just update the clients for a new Windows version.
I'm just saying I feel like as each year the balance of that tips to a different side a little bit.
I think a lot of more sensitive people came on board too.
A lot of the drug dealers went.
And the true hardcore people trying to hide from jail, no longer is like out loud or they started IPOs now.
But the thing is, I feel like there's more sensitive people who are now part of development.
Brilliant minds, great.
Love to have you.
But I think when the rubber meets the road, a lot of this, fuck your sentiments stuff comes back.
We're in a little kumbaya time now.
I think if you actually start talking about forks and things the conversation reverts to the mean.
Go ahead, Rijndael.

Rijndael: 01:12:12

I kind of think that the difference between the activation method that James is, I don't want to say advocating, I don't want to put words in your mouth, but trying to explain, and maybe the sentiment that NVK is explaining is just like LOT=true.
I think that's literally it.
I think the people that I heard, and I don't talk to everybody, but the people that I talked to who were the most annoyed by Speedy Trial, I think the thing that they were annoyed by was that there was this idea that if Speedy Trial failed, then we would go back to the drawing board.
And they thought that meant that miners were needing to tap in.

NVK: 01:12:57

That's right.
And it does give that impression to the network and to the business people who don't understand the code.

Rijndael: 01:13:02

Right.
And whether that's true or not, that's the message.
And what LOT=true says is there's a flag day.
And if you're not on board by the flag day, you're going to get forked off the network if we're the economic majority.
I wonder if maybe the thing here that kind of everybody once is like Speedy Trial with LOT=true.

NVK: 01:13:25

That's it.
But that was the ask that everybody who wanted to compromise said I had a LOT=true my Twitter handle.
So it must count.

James: 01:13:33

So I think there is not a person who is advocating Speedy Trial, who contradicted the idea that if the Speedy Trial fails, that we won't come back with the user activated soft fork.
I think everybody who's serious knows that's in our back pocket.
But it's a little bit like speak softly and carry a big stick.
And equally, even if you're running LOT=true before that timeout, you can change your software.
So it's kind of bullshit.
LOT=true is kind of just a ...
it could be a bluff.

NVK: 01:14:08

But you know, bluffs go a long fucking way, man, between humans.
It is fascinating.
Everything, every aspect of your life is carried on by bluff.
When you cross the street outside of a red light, you're essentially bluffing with your life that the car is gonna probably stop for you.
It is fascinating how it sets the tone in every human interaction.

James: 01:14:35

But Rodolfo, what I'm saying is that threat is always there.
The threat of a UASF is always there.
That's always an option to us.
Nobody is saying that we wouldn't do that.
It's just like-

NVK: 01:14:45

I'm gonna drive James crazy.

James: 01:14:47

You're gonna drive me nuts.
Yeah, because this whole thing is like ...
I don't care how activation happens.
It really doesn't matter.
It's solely just a way of kind of easing the deployment by not having chain splits.
It can happen any number of ways.

NVK: 01:15:07

Then why don't we do LOT=true?

Rijndael: 01:15:11

I'm going to float a thing.
I think that there might be a subtle psychological difference between saying, we could always go and implement LOT=true, and actually implementing it and letting users turn it on.
It's this thing where if you're a non-technical, or I don't want to say non-technical, if you're somebody who's not going to go and hack on Bitcoin Core, and you're just an economic actor, you care about Bitcoin, you care about this change.
If you hear, we can always go and implement LOT=true.
There's kind of an implicit, if we decide to do it.
And that's different from you have the code.
Hopefully we won't need to use it.
But here it is.

## Problems with Bitcoin Core defaults

NVK: 01:15:58

Remember, Bitcoin Core defaults, even if they're soft defaults like that, they rule things for the lazy which is 80% probably of the network.
So if you put LOT=true as default on Core, it's very likely that 80% of the people won't change that.
It's the same conversation that we had about RBF.
These things really matter.
They set the tone.
Most people will follow what comes out default from Core.
And if you're serious about that change, making it LOT=true, it probably puts that weight in.
It means that the majority of the people who work on that code believe that this fork, this update is likely to be the winner of that.

Rijndael: 01:16:49

But then by that argument, wouldn't you want to actually have LOT=false to be the default?
And what you'd actually want is to say, if the economic majority of the network actually cares about this change, then they need to go into their Bitcoin.com and flip the switch.

NVK: 01:17:04

But this is exactly one of the reasons why I don't like Speedy Trial.
It's because you get into this game of it depends on which side you like more.
You can make the argument both ways and now you're introducing order, which is gameable, versus the chaos.

Rijndael: 01:17:21

The thing that I think that you would want is you'd want the configuration option to be there, but it would be default off.
The default is what we have today, but the switch is there.
And if enough people care to flip the switch, then they go flip the switch.

James: 01:17:35

So here's the problem with LOT=true by default.
If you ship a binary that has LOT=true by default and people start to run that, and let's say during the signaling period, we discover that there's some problem, some bug.
All of a sudden now, the software that isn't supposed to require upgrades, Bitcoin, that's the whole reason we do soft forks is not to force upgrades.
Now you have a forced upgrade where it's like, you got to swap out the binary to make sure that your node doesn't fork itself off the network at this at this drop dead date.

## The politics of changing Bitcoin

NVK: 01:18:16

This is the issue.
Again, this is the problem.
I understand and respect the effort that went into developing Speedy Trial.
I really do.
It's an impossible position to be in, to be a Core dev when there is a fork coming.
It really is awful.
And trying to come up with stuff like this is exactly what you should be trying to do.
However, it just didn't suffice as a solution.
Like it doesn't.
If you want to measure if something works or doesn't, you can measure by how much hate you get when you put it out there.
Speedy Trial was a disaster.
Let's call it in public relations.
People really hated it.

James: 01:19:03

I don't know if it was a disaster.
I'm all for arguing.
I love arguing about Bitcoin.
I think people should be engaged with the technical community.
Let's argue about meaningful things, this is not a meaningful thing.

NVK: 01:19:13

I think it is the most meaningful thing, updating Bitcoin and how you update Bitcoin is...
Because remember, a lot of bad actors want to change Bitcoin to have, say, 22 million or to have tail emissions or whatever.

James: 01:19:28

Yeah, those are risks.
But the mitigation to those risks is is responding proactively with invalidateblock scripts.
Or, just not running some shitty software that someone puts out.

NVK: 01:19:40

It's because it's still a game of convincing enough people.
This is the thing that most Bitcoiners don't want to accept is that Bitcoin is fully political, 100% political.
Everything is politics.
How many people can you convince to go your way?

James: 01:19:52

Right.
And that's still in the mix.
It's just the question is whether or not you upgrade your version of Bitcoin Core.
So let's say if the maintainers merge some controversial software tomorrow, the really interesting process is whether or not people upgrade Bitcoin Core.
That's the vote.

Rijndael: 01:20:12

If the Bitcoin Core maintainers go evil and double the supply or implement tail emissions or whatever, what you would hope would happen is somebody would fork the repo and then go and tell everybody, don't run Bitcoin/Bitcoin, run Rijndael/Bitcoin instead.
Because it doesn't have the evil patch in it.
And you've got to convince enough people that it's in their best interest to change back.

NVK: 01:20:38

The challenge is, Bitcoin is fully centralized.
You have one client.
Essentially, you have one URL where the client is deployed.
It's fully centralized.

James: 01:20:48

And that's a real problem.
It's a real problem.

NVK: 01:20:50

Super.
Essentially, everybody expects it.
They go to bitcoin.org, they press download, that's what they should be running, and they're saving the world.
And this is why I always go back to, Bitcoin defaults are very complicated.
Because essentially the people who deploy Bitcoin kind of run it, they kind of own it in a way.

James: 01:21:10

I agree.
It's really bad that Bitcoin as an ecosystem implicitly looks to the maintainer merge button as the source of truth about what to do.

Rijndael: 01:21:23

Because I think the fact is the code, there is no spec.
The implementation of Bitcoin Core is the spec.

NVK: 01:21:28

I mean, it's Netscape, guys.
It's a hundred percent of the network runs the client, runs that specific call.
And this is why again, when you make things like Speedy Trial, you're implicitly sending people in a certain direction.
You really are.
And you don't feel that way because you understand that the call doesn't do what I'm saying.
But you're endorsing something, you're pushing something.
So this is kind of cool because at the same time, there is no solution possibly.
There really is no good solution.
And it's just one of those things that not having a good solution is the firewall.
Again, state actors cannot handle that.

James: 01:22:15

Yeah, so maybe your argument is, there's not a well-defined process.
So that makes the whole thing resilient because you can't follow a reliable method to achieve change, which, there's definitely a point there.

NVK: 01:22:30

Democracy was something kind of very useful and very good in the very beginning.
For you to vote in Greece, you had to own land.

James: 01:22:38

Yeah, I wish we would go back to that in America.

NVK: 01:22:40

Because the vote was linked to skin in the game.
If you ruined your shit, you lose your money because land is not portable.

James: 01:22:49

Totally.

NVK: 01:22:49

So you worked.
And then what happened is through thousands of years, we gamed it.
And then we gamed gold.
Humans, all they want to do all day is game shit.

James: 01:23:03

Right.

NVK: 01:23:03

It is literally why we're better than other animals, is that we figure out a way of gaming shit.
So the more chaos you introduce in that, the less likely you are to be gamed.

James: 01:23:15

So again, it all goes back to threading that needle between making the process resilient to being gamed, but also not doing these own goals where we all agree that we need something and it doesn't happen because the process literally, mechanically can't happen.
So I don't think any of us are saying it can't happen.

## Testing for consensus

Rijndael: 01:23:37

You made a point earlier that I really agree with, which is if somebody ever forces through some bad change, maybe it's miners collude and turn on drivechains or whatever.
I kind of hope so, because I want to test out this next part, which is you can write 30 lines of Python to inspect blocks and invalidate them.
And Jeremy actually wrote a script to invalidate CTV blocks.
He's like, if you hate CTV, here's your user-resisted soft fork code.
It runs as a sidecar next to Bitcoin.

NVK: 01:24:17

You've got to love Jeremy, man.

James: 01:24:17

He's one of the most honest, hardworking guys in Bitcoin.

Rijndael: 01:24:23

He's like, here's a for loop that kicked you off of the CTV chain if you don't like it.
Maybe if there is no process, the way that you test if there's consensus is you activate a thing and you see if the majority of the network kicks you off.

NVK: 01:24:40

But is Core going to deploy that?

James: 01:24:43

Probably not, because Core is ultra-conservative.

NVK: 01:24:45

No, but see, this is the challenge too.
We always go back to this thing that maybe is unsolvable.

Rijndael: 01:24:52

Well, but the thing that Core could do is Core could bundle an option or a tool with bitcoind to let you reject blocks.

NVK: 01:25:00

It should be, you can't run Core.

Rijndael: 01:25:04

It comes with a popup, when you open the software.
And then you pick the button.
And if you pick the 'No' button, then it invalidates blocks.
If you pick the 'Yes' button, then it accepts blocks.

NVK: 01:25:15

That's right, but you can't have a go back.
It really is like you have to run the previous version of core.

Rijndael: 01:25:21

You've got to IBD again.
You've got to move away your directory and sync it again or something.

NVK: 01:25:27

That's right.
I like that.
Maybe that's the way it creates the, but see that creates the game of chicken.
On UI.
How many people check the thing.
They'll just press Yes.

James: 01:25:42

Right, right.

NVK: 01:25:43

So now the discussion is gonna be, which one is the No, which one is the Yes?
Which one is on the left?
Which one is on the right?

Rijndael: 01:25:51

It's kind of funny because we kind of are, that's true.
People are going to be advocating for the right hand button is the one that I want.

NVK: 01:25:57

That's right.
Right hand is forward, is the future.

Rijndael: 01:25:59

That's right.
Oh my God.
Well, and then in the right to left languages, we'll have to flip the buttons.

James: 01:26:07

Is this like Tinder consensus where you're swiping right on CTV?

Rijndael: 01:26:10

Oh my God.
Yeah, that's right.
If you and G.
Max both swipe right.

NVK: 01:26:16

And then all the woke people are going to want to make users go through a little questionnaire that matches their values of which fork they want to like.

James: 01:26:27

Do a personality quiz.

NVK: 01:26:28

That's right.
They're going to do a gender assessment on the fork.
It's kind of funny.
It's a little reductionist.
But every single time I have this conversation, we always end up with the same fucking problem, which is nowhere.

Rijndael: 01:26:48

In my opinion, I don't think anybody in Core wants to be setting policy.
I don't think they want to be that guy.
I think what we should be doing is it should be very, very easy.
At the level of you launch Bitcoin-Qt and it gives you two buttons and the user gets to pick.
Because I think a lot of Core developers feel this real pressure of, people want new features, they want new things, but they don't want to be the person who decides.
And maybe the way to relieve that pressure is to just make the levers really, really easy and put them in front of users and then let people figure out their own politics and figure out how to convince users to click the right button.

NVK: 01:27:34

I don't know.

Rijndael: 01:27:36

Or we go back to flag days, I'm a big flag day maximalist.

NVK: 01:27:40

Yeah, flag days are great.
Just have a fucking flag day.
It's the closest thing that we have.

James: 01:27:46

Yeah, flag day wouldn't be bad, I guess.

Rijndael: 01:27:48

Yeah, if we just say this is the date and CTV is turning on.

James: 01:27:51

Right.

NVK: 01:27:52

If you care enough, show up.

Rijndael: 01:27:54

Yeah.
If you don't, here's 30 lines of Python.

NVK: 01:27:58

Yeah.
It's very sybil-able too.
That's the problem.
As more state actors come into play and it's tricky.
But I feel like we also exaggerate this concern at this specific moment in time in Bitcoin.
I'm pretty sure that in this specific time, we can find consensus like everybody within three calls of distance to them.
If I call three people right now, and I know they called another three people, I can have very solid confidence, I have no issues or coins at risk.
And again, the skin is in the game.

## State sabotage

James: 01:28:37

I think that's such a good point.
And that's what we really should be aware of is that state sabotage is more likely to come in the form of gumming up the works, or overt state sabotage is gonna come later.
But look at the CIA manual for subverting an organization.

Rijndael: 01:28:54

Bike shedding is thing number one.
You want to break up bureaucracy, just go on bike shed.

NVK: 01:29:00

Yeah, you want to know who those spooks are?
Go in the consortium policy or SPAC.
The W3C.
Look for the SPAC people, okay?
And then go look at how many of them used to work in aviation.

James: 01:29:17

Yeah, totally.

NVK: 01:29:18

Sorry, aviation people.

James: 01:29:20

So that's why I get a little prickly when talking about some of the activation stuff.
Because to me, it feels like I understand that the process of deployment, it's really, really important.
The process of coming to consensus is super vital.
And that is very important.
But the literal code that does the activation to me is kind of, column A, column B.

Rijndael: 01:29:38

Yeah, the amount of bike shedding that's happened on activation is indistinguishable from a state funded attack on Bitcoin consensus.

NVK: 01:29:46

Yes, absolutely.

Rijndael: 01:29:47

They would look the exact same.

NVK: 01:29:48

Look at what they did to PGP for fuck's sake.
PGP didn't happen because of that.
They made sure that the clients didn't have UI.
There is a great, great talk in 2014 or so about Operation Orchestra.
That's what they call it because they're they're playing you like a fucking fiddle.

Rijndael: 01:30:13

James, have you seen this talk?

James: 01:30:15

Yeah.
I think maybe on your recommendation, I gave it a watch and it's it's really good.
We should post it to Twitter when we get done with this call.

NVK: 01:30:22

Every Bitcoiner should watch that presentation, and understand where that blacklist comment that destroys the whole conversation comes from, or GitHub changing.
This is why the woke people so scary.
Because they are essentially, this is a Marxist playbook.
It's how you break things is by destroying language and destroying how things are run by rational, reasonable people.

James: 01:30:49

So internal suspicion among the community, make people fight within the community, make doing technical work really, really difficult and slow going.

NVK: 01:30:58

Secure elements are evil.
So let's not have them.
It's the most absurd shit I've ever heard in my life.

Rijndael: 01:31:06

My favorite comment from that thing was he was like every website should have by default a self-signed certificate.
But when you go, there's a scary browser warning that's like, careful, you might be talking to the NSA.

NVK: 01:31:19

That's right.
It's genius.
But we arrived at that point.
Google changed Chrome.
You can no longer have self-signed certificates.
And somehow, Cloudflare is free.
Just somehow.
They're like, oh, everybody should encrypt except your encryption keys for your sessions are in the NSA servers now.
So they just make it easier for everybody.

James: 01:31:45

It's a big black pill if you start to really think about this stuff.

NVK: 01:31:49

It's the incentives.
You can make it as nefarious or you can make it incentive based.
It doesn't matter.
We arrive at the same place.

## Moving forward with activation

I feel like if we want this, we're going to have to just lift our hands and start pushing in terms of I'm going to be running this I'm going to be running the CTV USF client.
Because that's the lingo that people understand as well.
I'm going to start running and that's it.
Because until people are now willing to put their reputations on the line, nobody believes this has any chance that that's how it works really.
It's just masturbation.

Rijndael: 01:32:31

There's still a lot of people who still don't understand what Taproot is.
Taproot was a very heady, abstract change.
It's going to let us do all these things in the future that are very sophisticated and advanced.
SegWit was also, a lot of people didn't quite understand SegWit and probably still don't.
What I'm hoping is the three changes that James said, CTV, APO, and VAULT, I think those are things that more people can wrap their heads around.
And I think that those are things that have more direct applicability to the things that people want to be doing with their Bitcoin today.
CTV and VAULT helps you make your coins safer today.
If all that you want to do is use Bitcoin as a store of value.
Bitcoin is a better store of value if you can keep it safer.
And then APO helps with Lightning, which we're going to need if you eventually ever want to spend your coins.
So it's much more concrete about why people would want these things and maybe it'll be less contentious.

NVK: 01:33:34

I think the issue here is it feels like an omnibus bill kind of thing.

Rijndael: 01:33:40

Stick the pork in?

NVK: 01:33:42

Now we have three things we're trying to push and people cannot comprehend already each of them.
And now you have to comprehend how they interact with each other and Bitcoin and stuff.
I don't know.
I feel like we got to just pick essentially probably CTV, which is the most comprehensive here.
That does the most.
And just fucking go with that.
Maybe you attach a few things to the CTV change, but the point is, I want the three personally, but I think it's gonna be very hard to get that through.
So I think if we just pick one thing and go with that and just deal with it.

James: 01:34:18

That's originally the route that I wanted to go.
And I started to actually prototype what vault wallet code looks like with just CTV.
And I came to the conclusion that if you're a big company, having CTV would operationally make vaults easier to do, but they were still impractical for your everyday user.
And that was really the outgrowth of OP_VAULT.

NVK: 01:34:46

Let business solve the easiness of it.
If the choices don't have anything.

James: 01:34:52

There's part of me that says yeah, sure.
Let's just do a CTV fork and exercise the software process.
But, the more that I talk to people, the more they're like, no, we should really just do it with VAULT.
And I kind of feel similarly.
And then APO has just been on the docket for so long.
It's such a simple change.

NVK: 01:35:14

What if we do this differently?
What if we game the chaos in the chaotic way?
Maybe this is the way to deal with this.
What if we essentially have enough people going, fuck it, we're gonna have a UASF flag day thing, okay?
And in the midst of all that and the fight, somebody goes, you know what, fuck it, I'm going to do Speedy Trial.
And essentially you arrive at what happened last time.
Because you can't prevent anybody from doing anything.
That's the beautiful thing of Bitcoin too.
If the miners want to do Speedy Trial, they can do Speedy Trial.
As long as their dates line up with our UASF date.
Let each balkanized camp go the way that they want to go.
As long as everybody's timeframes all work out, it's fine.
You arrive at the same place, but through chaos.

James: 01:36:10

The tricky part there is that then you have to write a bunch of different client code and, get the specifics right on the activation stuff.
You don't remember when Garzik came up with his own Bitcoin Core fork and there was an off by one and it would have been catastrophic if they had deployed.

NVK: 01:36:26

Yeah, but Garzik caused a lot of catastrophic problems.
We have better people.

James: 01:36:31

Yeah, yeah.
Maybe not the sharpest knife in the drawer, but that's not to say that it's easy by any means.

## State of Bitcoin development

NVK: 01:36:40

It's not going to be easy.
I think the way you have to think about this is like battle.
Like actual war.
There is no saints in war.
There is no people that go unscathed.
Everybody gets fucked a little bit.
There will be casualties, there will be collateral damage.
But at the end of the day, you got to move forward into your campaign.
You just got to accept that you can't please everybody.
You're going to step on toes.
People are going to get hurt.
People are going to quit.
If you can't handle the heat, get out of the kitchen.

James: 01:37:27

Yeah.
At some point, you're going to have an empty kitchen and nobody's going to want to actually build this thing and secure it from state actors.

NVK: 01:37:34

Nah, you can always hire a new line cooks.

James: 01:37:37

I say good luck, good luck, have fun because that's just not how software works.
I'm sorry.

NVK: 01:37:46

No, it's fair.

James: 01:37:46

I get your point.
I'm approaching the point where it's like, yeah, I'll work on this stuff under these conditions for maybe another few years and then I'm done.
Look at the people we've lost so far and look at how well we're backfilling the intellectual capital.
It's not going great, guys.

NVK: 01:38:06

I don't know, James.
I'm a lot more optimist on that.
I really am.
I'm a big believer in the economic incentive.
For each type of very specialized activity, there's always gonna be only a handful of people.
That is true for anything ever in humanity.
There's only so many genius people at every single topic.
And we often create a lot of exceptions and we make it cozy for the people who can do a thing that nobody else can.
But, there's a lot of fucking great people out there.
There is a lot of great people out there that will find income.
I mean look what happened.
There was no money for developing Bitcoin full-time.
There's a lot of people also who are rich as fuck that claim to be poor so they don't get killed in Bitcoin.
There is a lot of noise in how you get your heuristics of the state of Core too.
But people are complaining that there is no money, but all of a sudden now there's three organizations that have enough money to support enough devs to work on Bitcoin.

James: 01:39:20

Totally, totally.
And there's good money and I can tell you if there wasn't good money in Bitcoin, I probably would not be working on Bitcoin right now.
I'd probably be working on nuclear or ...

Rijndael: 01:39:33

Bitcoin can't rely on altruism.
Bitcoin is PVP.
The only way that Bitcoin works is if it aligns incentives correctly.
And if it doesn't, then Bitcoin deserves to die.

NVK: 01:39:49

But it does.
For example look at some of the clients, look at Electrum.
It goes way back in time.
Somehow a 'not for profit' project keeps on being maintained.
Why?
Because there is enough OG's still using that piece of software and it's in their interest to pay people to keep on maintaining it.
The people who get paid to to keep on maintaining it don't talk about how much they make, if they work for free or not.
But there is enough incentive to maintain everything going.
You can say for example, a place like a Chaincode Labs.
It's a little bit cozier, it's a little bit more left-leaning kind of organization.
There is some people who have a lot of Bitcoin who maintain that place.
And then the incentive is for you to maintain your bags safe.
That means having devs working for it.

James: 01:40:42

I think that's the issue though, is that the people who were involved back in 2012, 2013, that era, you can accumulate a much bigger stack based upon the supply characteristics, the supply curve of Bitcoin.
And sorry, that's just not the case now.
I know a lot of people who are...

NVK: 01:41:02

Oh, you still can.
It's just early.
So early.
People said that...

James: 01:41:08

Maybe, maybe not.

NVK: 01:41:09

In 2013, seriously, in 2013, 2014, everybody was saying, if you got in Bitcoin in 2010, in 2011 you could have been made a fortune.
Look at me now, I can only have so many hundred coins.
I could have thousands.
That's going to be true on every single stage of the Bitcoin versus dollar price cycle.
That's just the nature of it.
Remember, there's only 22 million, 21 million units.

Rijndael: 01:41:38

That was a Freudian slip.

NVK: 01:41:41

I've been joking with Pablo on Nostr and I've been tipping him 22 million every single time, joking that like he got oversupply.
But anyways, my point is Bitcoin really is binary.
It either goes to zero or it goes to the moon.
I mean, people if they don't want to believe that they're probably in the wrong project.

James: 01:42:02

I agree with you.
And I don't think that the to the moon case is guaranteed by any means.

NVK: 01:42:08

And now we have full-time money.
People used to have to sell drugs to be on Bitcoin.
Now you actually can get a salary.
That's a huge improvement.
I'm just saying, I feel like we can't fall into this nihilistic, oh it's too hard to work on Bitcoin.
It sucks and stuff.

James: 01:42:29

And that's not what I'm saying.
And I know I bitch a lot.
And I'm in the midst of one of my bitch sessions here.

Rijndael: 01:42:36

Nobody's listening.
There's only three of us here.

NVK: 01:42:39

This is the thing, James.
This is the cool thing about this pod.
We can be extra, unless they're trying to get us, none of us are going to run for office.
So we don't have to be worried about people clipping the show.
I'm unelectable.

Rijndael: 01:42:51

And once you get past the 20-minute mark, everybody's tuned out anyway.
So this is just therapy now.

NVK: 01:42:56

That's right.
There's two dudes that keep on going.

James: 01:43:02

No, no, no, no.
So I fully realize I get emotional about this stuff.
I'm not actually maybe as emotional as I sound, but what I'm trying to do is raise the alarm that we don't want to burn our human capital, because I do really care about Bitcoin.
I want Bitcoin to succeed.
I want it to continue to improve.
I don't want it to be compromised by the state.
I also want it to be able to scale to its potential.
And what I'm seeing with my boots on the ground is this slightly worrying situation where the big parts of Bitcoin are not really progressing.
And the people who are full time working on Core are in this narrower, more technocratic, oh, does the mempool work the right way?
That's important.
But maybe we also need to think about how to actually scale Bitcoin, how to secure coins.

NVK: 01:43:51

I think it's a little self-selecting too.
The drug dealers no longer work on Bitcoin as far as I know.
So it's like the crowd who run servers and things, they want to look at graphs and see how much better it is.
Once you tweak something, they're not interested as much in can I cross a border, am I going to go to jail, kind of problems.

James: 01:44:18

Exactly.

NVK: 01:44:19

But then we can also change nothing.

James: 01:44:21

That's the problem, is the Core project right now has a very European bureaucratic approach, let's just not fuck up.
That's the highest priority.
Let's just absolutely not fuck up, which in a certain way, it should be the attitude, but it's also stifling over time, over a long enough time period if you're not innovating, and Bitcoin still requires innovation in my opinion, then you're going to kill the thing in the cradle.

Rijndael: 01:44:50

I would say that another thing that's underneath a lot of this is part of the core value proposition for Bitcoin is that it's money that works no matter what.
If the government is against you, your money still works.
If large companies are against you, it still works.
You just need to get a transaction included and for most of the miners to not try to reorg your block and your money works.
And I think that if you're doing a risk assessment or a threat analysis of Bitcoin and you're thinking of, what are my dependencies in order to have my money work?
There is kind of this implicit thing of I'm still depending on a relatively small group of developers for my money to work.
And I think maybe part of the difficulty around activation is that with the activation methods that we've had so far, there's still this implicit, I need to get a small group of devs to do the right thing.
I need to get miners to do the right thing.
That's an external dependency on my money working.
Maybe the thing that people are trying to articulate is there's some aspirational mode of activation where there is no single party that I can point to and say, this group has to cooperate.
It's more of this amorphous thing of, if the economics work out, then the soft fork activates.
And I don't think anybody exactly knows what that is, but I think that's the thing that people are reaching for when they say that they're not happy with what we've done so far.

NVK: 01:46:31

There is something that I think is an issue, too, is that there is a lot of fucking bitching.
People are not going to like me saying this.
And I get a lot of trouble for this, NVK is so insensitive and you know, this and that.
And it's not compatible with a lot of the kids and stuff.
But stop fucking bitching, Jesus fucking Christ.
There is money for people that really want it.
Even before these three organizations, they just got to make compromising work for somebody they maybe don't like.
Rijndael you're an example.
You have a source of income.
James, you have a source of income.
And I have a source of income.
We all have our own biases, our own incentive set.
And that's what Bitcoin is supposed to be.
I kind of fall a little bit sometimes into, what I like to call them my favorite Bitcoin Luddites camp, which is nobody has a God-given right to have a fucking a donation salary to fucking work full time on Bitcoin Core.
Bitcoin should just work in industry.
It was designed that way for industry.
The people who have most of the economic incentives to do things, to pay somebody to fucking do the things that they want, go pay for a feature.
Remember when Pierre made the website?
And you could pay for somebody to do a pull request or pay for somebody to review something.
That's the way it should work.

James: 01:48:03

Sadly, that never actually worked because I had a bounty that I wanted to collect on, but it turned out that I guess it was just people kind of pledging that they might pay you.

Rijndael: 01:48:14

And going back to the whole you can run 40 lines of Python to invalidate blocks.
Something that I think people forget is you can run whatever software you want.
If you want to run Bitcoin Core, do it.
If you don't like Bitcoin Core, you can either go to the library and borrow a C++ book and learn how to hack on Bitcoin Core, or you can pay somebody to go do it for you and then you can run that software.
Or you can run different software altogether if you don't like Bitcoin.
But you have agency to run whatever software on your computer you want.

NVK: 01:48:42

Yes.
I think it's too easy to snap into this God-given, and I feel this from a lot of devs in this space.
There is this sort of, oh my God, I'm so smart.
And oh my God, I have this God-given right to get paid full time to do this because nobody else is going to do it.
Trust me, if there is enough fear of something, there is enough money in Bitcoin that that will find its way.
Sometimes it needs to be pointed out to somebody that does have the resources to help with something, there's nothing wrong with that.
We're super lucky that it really comes down to mostly Jack right now.
Three or four organizations have their largest base from them.
And he literally makes it so that he has zero strings attached to the to the financial incentives.
And he does have this thing where he's actually funding the competing entities.
And ideally these competing entities should actually fucking disagree.
So OpenSats should fund shit that maybe Spiral doesn't want.
Spiral is actually part of Block.
And they don't fund shit that has licenses that don't match things that Block can use.
And Jack is very aware of that.
So I think that the beautiful thing of Bitcoin is that it really has spontaneous order vibes to it.
It does tend to go on that trend and somehow things find their way.
We have somehow survived with this thing for fucking 12, 13, 14 years.
I kind of lost count.
And it just fucking works.
So people need to embrace the chaos a little bit more stop being fucking pussies.

James: 01:50:26

Yeah.
But on the other hand, if you're coming at that from the non-technical outsider perspective of a user of Bitcoin, you can't just say, oh yeah, the magic pixie dust will make technical things happen and it'll all be fine.

NVK: 01:50:40

No, no, it's money.
It's literal money.
I'm advocating for literal money and people hiring a dev to go fucking make them a feature or go reveal something they have a concern with.
And listen, big industry does.
There is enough entities out there with enough capital, with enough Bitcoin that they have paid people to go review or request to go review Bitcoin, to go do diligence things.

Rijndael: 01:51:06

Well, but also if you're an individual user and you don't have the time or the inclination or skills or desire to go work on that, you can also donate and pay developers.
I have zero interest in going and working on Bitcoin Core.
It's just not a thing I want to do.
For all of the reasons.
But it's important to me that smart people whose judgment I trust do go and do it.
And so when those people say, hey, I'm raising money to support my work on this.
I go give them money because it's an important thing for me.

NVK: 01:51:42

People don't need a pat on the back.
They need ...

Rijndael: 01:51:45

I also give people pats on the back.

NVK: 01:51:48

You can give them money and then give them a hug.
I'm a hugger.
I'm a big hugger.

Rijndael: 01:51:53

Hey, we're two hours into talking about covenants.

James: 01:51:58

Yeah, this wound up being a little bit more meandering than I thought, but it's a great discussion because I think this stuff is worth talking about.
Selfishly for me, I'm cooped up in my house all day.
So it is nice to vent about this a little bit.

NVK: 01:52:11

That's the conversation.
We're having the conversation that three reasonable people talking about the next thing that's going to happen in Bitcoin.
They're going to discuss the thing.
Why the thing?
How does the thing work?
How do we activate it?
And then they end up in all this discussion.
There is no way to avoid this.

Rijndael: 01:52:30

It's funny.
I feel like this pod has kind of turned into a microcosm of the whole discussion.
Because I think what happened with CTV is most people who looked at CTV technically said, this is really simple, this seems really reasonable.
And then where most of the controversy was, was activation.
I think CTV itself is actually not that controversial of a change.
I think it's all about how do we turn it on?

NVK: 01:52:54

Yeah, it's always going to be the conversation in Bitcoin.

Rijndael: 01:52:57

Yeah, never ask a man his salary, a woman her weight, or a Bitcoiner how to activate a soft fork.

NVK: 01:53:06

I guess since we're approaching two hours here, is there anything else we missed that we should address or do we kill at the usual?
You want to kill a Bitcoin discussion, talk about activation or funding Core devs.

James: 01:53:21

I wish we could do that 90s late night talk show thing where we have people call in and field questions.
But I guess that's what Twitter spaces is.

NVK: 01:53:30

We should do it.
I always wanted to have a call in live show, ala Frazier.

James: 01:53:35

How cool would that be?

## Next steps

NVK: 01:54:04

I feel like maybe we've murdered the conversation, which is great.
We all like to talk to each other.
We're eager to just keep on talking.
But I think the topic itself, it's funny, because the arc of this topic is always the same and it ends the same way.
So I guess in the spirit of being productive.
What's next?
What do we do next?
Do I just go run James' CTV client now?

James: 01:54:41

No, no, no, I wouldn't tell anybody to run the code that I've come up with.
I think I'm gonna post it.
Right now I'm debating whether to preface it with some kind of a mailing list post explaining my rationale.
Or just put up the code and say, this is one possible avenue that we could go.
And I encourage everybody to look at the code and try and find problems or propose a different approach.
But I do think it's important to start presenting tangible options for people and say, this is one way we could go.
So let's start thinking about the particular direction, because we shouldn't just spin our wheels for another four years.

Rijndael: 01:55:17

So CTV and APO are both active on the Inquisition signet today.
What's in your branch that's different from what's in Inquisition?
Is it basically Inquisition but for mainnet, or is there more?

James: 01:55:37

It's Inquisition, but the problem with Inquisition is that AJ, and I understand why he did this, but when he forked Inquisition, he added a bunch of utilities for adding deployments.
And that creates this really frustrating situation where you basically have to have separate patches for Inquisition versus just regular Core.
They're not compatible really.
They have to be rebased separately and all this stuff.

Rijndael: 01:56:03

Okay, so this is like porting all of those things into Core and doing all the rebases and all that.

James: 01:56:08

Yeah, exactly.
The deployment method is a little bit different in Inquisition, so really this is just me re-bundling everything to have a Core compatible deployment.

NVK: 01:56:16

So then what's next?
Do we need a volunteer to go and rebase for Inquisition?

James: 01:56:30

I don't know.
I think the jury's out for me on the usefulness of signet versus just like regtest.
I know that when I'm trying stuff out, it came up in the last week with an OP_VAULT demo, I encourage people to check out as well because that's a really fully fleshed out usage of what a wallet would look like using OP_VAULT, what the workflow looks like, how to compose all the scripts what the different pieces of data are.
And for something like that, the code that I wrote is signet compatible, but for my own sake, just testing, I find regtest a lot easier.
I can control when the blocks are mined and all that.

NVK: 01:57:10

James, thinking like a politician for a second.
What would be the next thing that will cause the next shit disturbance?
So that is useful.
Not, not bad thing.
Destructive shit, disturbance, they'll get the next wave of opinions and participation and engagement.

James: 01:57:28

I guess if I throw up a PR on the Core repo because all this stuff has been on Inquisition for a while and it hasn't really spurred anything.

NVK: 01:57:36

For the people that can't see, Rijndael's eyes just went fucking full laser.
He blinded us.
That was your unconscious mind really gave your position away on that one.
It was just absolutely on.
You got a terrible poker face.
Having a little bit of skin in the game, a PR or something, really unnerves a lot of people who just think this is just theoretical, because I think right now everybody is on this on this mental mold, I'm just going to ignore it.

Rijndael: 01:58:10

It's not real yet.

NVK: 01:58:11

And people are not going to put their weight or their thinking or their opinion on something that is positive and negative.
A lot of people are just going to stay out of it until maybe it's a PR.

James: 01:58:23

Yeah, yeah.
So I'll put the PR up and then I actually should coincide pretty well with our baby coming because I can drop the PR.
Basically walk out.

NVK: 01:58:33

Yeah, totally.

James: 01:58:34

And not sleep for a month while I'm taking care of him.

NVK: 01:58:36

You're screaming fire in a movie theater.
That's what PR on Core is.

Rijndael: 01:58:40

And then when you come back, you'll be sleep deprived.
You'll have a complete shift in your...

NVK: 01:58:47

Zero patience with bullshits.
Babies, dude newborns, all this polite veneer of James here is gonna just fucking go.
Newborns, they really focus you.

James: 01:59:01

Well, little there was to begin with.

Rijndael: 01:59:02

A hundred percent.
Somebody's going to go on that PR and say, won't this allow government whitelisting?
And you'll just delete that shit and be like, I don't have time for you.
My baby's screaming at me.

NVK: 01:59:12

That's right.

Rijndael: 01:59:12

Come back when you know how to.

NVK: 01:59:13

Post pictures of the baby's poo on the PR.

James: 01:59:16

Oh, yeah.
If you thought my mood was good now, just wait for another two months.

Rijndael: 01:59:22

It's going to be great.

NVK: 01:59:23

That's going to be very useful because I think that the conversation will shift into, this is the thing that we want to actually activate.

James: 01:59:32

And if there are people out there who want just CTV, I think that'll bring them out of the woodwork and say, no, we should just do a soft fork with CTV, or there's a group of people I've been talking to who just want VAULT, because you can do that.
It won't be as good as with CTV, but you could just do that.

NVK: 01:59:48

But it creates alliances.

James: 01:59:50

Yeah.

NVK: 01:59:50

That's the other good thing, too.
It's like, there's something for me.
There is something for you.
It's fucking politics, man.

James: 01:59:55

Right.

NVK: 01:59:56

You can't get humans out of it.

## Bitcoin politics closing summary

James: 01:59:57

It is.
That's what's really ironic to me is Bitcoin is the most deeply political system that I've ever worked on, compared to all the private companies.
Now it's a much bigger system, but it's surprisingly political.

NVK: 02:00:11

But before politicians became parasites in this fully-gamed systems, politics is nothing more than trying to sell the thing that you want that may affect other people.

James: 02:00:21

You're right.

NVK: 02:00:22

But there's nothing wrong with it.
It's just, you sell where you want to have dinner with your wife.
You have the political discussion about it.

Rijndael: 02:00:31

Ultimately, Bitcoin is a completely voluntary tool for economic coordination.
If you don't want to play the rules, there's 5,000 other clones that have slightly different rules that you can choose.
And so it's going to be political because money is inherently a social network.
It becomes more valuable the more people accept it and will pay you with it.
And so you want more people to play by your rules and you want them to be the rules that you want and not the rules that you don't want.

NVK: 02:01:05

I love that, the people try to say Bitcoin is a political whatever, but Bitcoin is essentially enforced libertarianism and people can't accept that is hilarious.
But in the absence of the central planning and central controlling, is political.
You can't save the children with Bitcoin because nobody's going to print your money.
You're going to have to use yours.
It's literally enforcing a certain political view.

James: 02:01:35

Yeah, that men shouldn't have control over the supply of money.

## Closing thoughts

NVK: 02:01:38

I think this was a fantastic discussion.
I really did.
We explored this like people who participate in the network would.
I really think that people are going to get something out of this.
I think it will help people go through the train of thought, agree/disagree with the stuff that we have to say.
I feel like it was a good arc.
We really covered all the things that need to be covered.
And hopefully people come out with an opinion that's a little bit more informed.
At the end of this, as opposed to just wishy-washy, which is, where the discussion about covenants was.
Maybe we get some good feedback telling us hey, can you go on this, discuss that or something that we missed or whatever.
But maybe we do a refresher on this discussion after the PR.
Because the PR is going to be very interesting in the PR comments.
And so with that, any final thoughts?
Rijndael?

Rijndael: 02:02:50

I don't think so.
I hope that whether people like these proposals or don't, that there's higher quality dissent and discussion coming out of it.
I think that what James is going to go do will hopefully be a forcing function for people to get a lot more concrete in their either alternatives or arguments or whatever.
A lot of this shit's been way too hand-wavy for way too long.
And so hopefully we got some real discussion.
I'm stoked, can't fucking wait.

NVK: 02:03:29

Yeah, yeah.
I think anybody who works on the ground and doesn't have the freedom to go fully galaxy brain on this either, feel the same way.
I work with self custody.
I understand the shit.
I understand I need this shit.
It's a very different vibe than even Taproot.
And let's not even get into Schnorr, just no longer Bitcoin.
It's a whole other conversation.
James, any final thoughts?

James: 02:04:01

Rijndael nailed it.
I just wanna say, I understand why we're here and not some place further down the path.
Because this has been my full time job for the past four years.
And even just staying on top of the conversation is a ton of time, requires a ton of technical context.
So I get why we are where we are, but I do think that it's time to start talking more in terms of concretes.
What are we planning on doing?
Evaluating specific sets of codes.
I'm definitely looking forward to how this conversation progresses.
And I have opinions, but I don't have a dog in the fight really.
I just wanna see things move forward in a concrete way because ultimately, I want to see Bitcoin realize its potential.
I think now more than ever, having a viable non-state money is absolutely critical.
And we have to make sure that this thing works.
I always love talking to you two guys and NVK, I love this venue for talking about stuff because we can shout at each other.
It's always a great conversation, but we always know that the other guys have the best intent.

NVK: 02:05:24

This is a safe space for people that don't like safe spaces.
I feel like there's just too much noise.
People whose intent is to disagree as opposed to just have three dudes having a beer kind of conversation and sorting shit out.
We don't actually have to agree.
People seem to be missing the point.
The idea is, where do we find a little bit of compromise to keep on moving.
And I'm extremely grateful that people like you guys come.
And you guys are people who build incredible things and do incredible work and are wasting two hours of your time just talking to me and maybe two people left listening this long.
But hopefully somebody gets some value out of this.
And then when somebody actually bitches on Twitter about something and say you put a link, go listen to us talking about it in depth it's very helpful.
It's the shut up link.
I am reaching my point, I think probably because of Nostr, because Nostr is new, so the bitching is young.

Rijndael: 02:06:38

It's fresh bitching.

NVK: 02:06:39

And I'm no longer young.
So my patience with bitching and people who have opinions and don't build anything is starting to diminish exponentially.
So I need a place, a safe place.

Rijndael: 02:06:57

One of the things that's a little bit contradictory about a lot of social media Bitcoin discussion is I think that this is a community that values sovereignty and self-determination more than most other communities.
But then simultaneously, a lot of people in this community forget that they have agency.
If you don't like the way that things are going, pick up a text editor and a C++ textbook and be the change.
Or pay somebody else to be the change.

NVK: 02:07:29

Learn to code.

Rijndael: 02:07:32

100%.
And there's nothing wrong with that.
I work on a whole bunch of stuff right now that I thought was missing in the world, so I'm going to go build it.
And Bitcoin's open source, open participation, permissionless system.
You choose your level of involvement.

NVK: 02:07:50

There is this trend I noticed a while back.
I'd say like three years ago or so.
It's what I call Bitcoin Marxism.
It's like there is a lot of people who don't understand what the fuck is going on.
They have no reasonable skin in the game.
They're not building anything.
It's just literal fucking noise.
And that's not useful.
It's not useful of their time.
It's not useful for us.
You sound like a credit card on Amazon.
You're just causing more noise.
You're just stifling the conversation.
But we're people we don't talk out loud, but we know everybody who builds stuff and talks, it's very obvious to everybody else that you are just noise.
So don't be the noise.
Anyways, with that, I think this one is cooked.
It's done.
This was awesome.
