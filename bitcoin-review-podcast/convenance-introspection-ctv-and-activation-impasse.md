---
title: "Convenance, Introspection, CTV and activation impasse"
transcript_by: kouloumos via review.btctranscripts.com
media: https://www.youtube.com/watch?v=o8tjsVdiPUI
tags: ["covenants"]
speakers: ["James O' Beirne","Rijndael"]
categories: ["podcast"]
date: 2023-09-30
---

Speaker 0: 00:00:02

Everything else versus Bitcoin essentially gets spent and dies.

Speaker 1: 00:00:05

I want to be able to have reactive security and I think OpVault is today the most straightforward, easiest to use way to do that.
I will not be insulted by a clockmaker.

Speaker 2: 00:00:21

Overall these kind of ways to make the network easier to both build on and interact with, I think is a really big deal.
If Bitcoin existed when we started Twitter, We would not have to go down the ad model path.
I mean, as simple as that.

Speaker 1: 00:00:33

Integrating Lightning into a social network is the killer app.

Speaker 0: 00:00:37

Hello and welcome to the Bitcoin.Review podcast, where we explore developments and projects with the people who actually make them happen.
The show is supported by Pod 2.0, SatStreaming and CoinKite.
If you're a new listener, I'm Nvk.
I run CoinKite, where we've been helping people secure their Bitcoins for over a decade.
We make the cold card and fun products like the Block Clock.
You can find more information about it on CoinKite.com.
Hello and welcome back to the Bitcoin.review.
As usual, nothing is happening in Bitcoin and we figured, hey, what a great day to put people to sleep in one to three hours podcast.
We don't know yet how it's going to be.
We actually don't know how this is going to play out

## Guest intros

at all.
So I have here with me Mr. Rindell.
Hello, sir.
Welcome back.

Speaker 2: 00:01:30

Hello.
Good morning.

Speaker 0: 00:01:32

Good morning.

Speaker 1: 00:01:33

For his like 600th appearance on the show.

Speaker 2: 00:01:37

Yeah, I've been sleeping.
I haven't been sleeping well enough.
So I came back to record this so I can sleep to it.

Speaker 0: 00:01:43

James, we can't acknowledge it.
Otherwise, we have to add him to the splits.

Speaker 1: 00:01:47

Oh, yeah, fair.
OK.

Speaker 0: 00:01:49

And he goes to open SATs. So, you know, priorities, but.

Speaker 1: 00:01:53

Amen.
Yeah, it's good to be back.
Hi, everybody.

## Recap

Speaker 0: 00:01:58

So, guys, As I was mentioning earlier, CTV has given place to other things in my mind as of late, been trying to ship products and stuff, you know, the things that pay the bills.
But I think we've crossed a chasm on the conversation.
I think the most of the FUD is sort of like going away, especially in recursive covenants and stuff like that, the scary stuff.
And the Ethereum is dying.
And I think a lot of people, especially bigger piles, are realizing that we don't have acceptable custody solutions yet for serious amounts of money that don't depend on third parties, especially corporate.
And, you know, it's just things are changing, evolving.
And I think sort of the space, the industry is maturing a little bit.
And I think the Covenant's conversation is sort of like it's going to be the next big thing.
And I think it's really sort of going on that way.
So with that small little premise,

## Technical overview of covenants

why don't we talk about what is Covenants?
What is Covenants in Bitcoin?
And then after that, maybe we start talking about what we can do today and what we can't do today.
So who wants to give us a little premise on Covenants in general?

Speaker 1: 00:03:29

Brian Dahl, you warm us up, man.

Speaker 2: 00:03:31

Yeah, I'll take a swing at it.
I think it might be helpful just to understand what Bitcoin's script is and how it works.
Anytime you send a Bitcoin transaction to an address, what you're really doing is you are locking those coins to some kind of script.
Bitcoin has this really basic scripting language, and when you spend those coins you provide some input that satisfies the locking script.
The really basic one is, if you're using a single SIG wallet and somebody sends you Bitcoin, you say, in order to spend this Bitcoin I have to produce a signature that corresponds to the public key that encumbers my Bitcoin, and then you can spend it.
There's other conditions that you can use to lock your Bitcoin.
You can use time locks.
You can say, this can't be spent until after some block height or after some time.
You can use hash locks where you say, in order to spend this Bitcoin, I have to provide the preimage to a hash that I commit to when I lock up my Bitcoin.
You can add multiple keys together to do multi-sig.
You can combine hash locks, time locks, and multisig to do lightning.
You can compose these things together.
The thing that's important to understand is that all these conditions or locks or encumbrances, they govern the input side of the transaction.
So I send coins to James and there's a set of conditions that James has to satisfy in order to spend those coins.
But once he satisfies them, there's no conditions on how he spends them or where he spends them.
So this ends up being really important if we want to do things like we want to have multi-party ownership of coins and you want to let people unilaterally withdraw their coins.
So imagine if we had, the three of us, we have some shared UTXO And all three of us sign together in order to move the whole thing.
But say that NVK wants to unilaterally exit without James and I co-signing, it would be really useful for him to be able to sign a transaction that takes out his portion of the coins and nobody else's.
And in order to do that, you need to have a locking script that says, if NVK presents his signature, then he can take this many coins to a given address, but he can't take all of them.
And that's not a thing that you can currently express in Bitcoin script.
You have to solve that with other means.

Speaker 0: 00:06:25

Just to make this a little bit more grug-brain-like, essentially what we can do now is we can sign in, but we can't sign out.
Yeah, yeah, exactly.
Essentially, right now, we can agree, like you can do a multi-sig, right?
Standard P2SH kind of multi-sig, and send to an address, to an UTXO.
But the UTXO has no control on the way out, except for the script that you had before, right?
So wouldn't it be nice if the UTXO had two things?
One is a capacity to essentially have conditions on itself on how it goes to the next hop.
And the second thing is some introspection.
So maybe it knows how much its size is, right?
Cause right now a UTXO doesn't know if the UTXO is like one Bitcoin, two Bitcoin or a SAT.
So it would be nice if he knew at least its size or maybe its place in time.

Speaker 2: 00:07:25

Yeah.
And like the application for this that really made it real for me, that made me really interested in covenants and clicked is the idea of a vault.
What you want to do is, the classic problem in Bitcoin is, what do I do with my seed phrase?
How do I secure my wallet?
Because if somebody gets your seed phrase or whatever key backup you have, then they can just spend all your money.
There's no way for you to say, my money can only be spent in a particular way.
What I think you'd actually like to do is say, all right, I've got my vault, I've got my deep cold storage and it should only go from my cold storage to my hot wallet or from my cold storage to my exchange account because I'm selling or something.
You want to be able to restrict how the funds come out of your cold storage so that if somebody compromises the metal seed phrase you have buried under the tree or something, then they can't just run away with your money.
There's not a way to do that in Bitcoin at the script level right now.
You have to do that with hacky pre-signed transactions that we can talk about.
If you think about this idea of exactly what MBK just said, where you can have a transaction introspect its contents and set rules on where it's sending coins, how many coins it's sending, the shape of the output of the transaction.
Then you can start building more interesting self-custody solutions.
And then we can turn that into other stuff too.

Speaker 0: 00:09:06

You know, even if you go back in time, pre Bitcoin, even pre fiat, right.
There's essentially like two main things that people try to do when they have an important, an important, let's call it an asset, or an important item in volume inside something.
So they wanna be able to do what's called velocity.
So a velocity essentially dictates that you have, you're gonna have like a quantity per time, right?
That comes out.
So for example, in a silo, when you have all your grain there, you choose your velocity by adjusting the size of the door, right?
Because you don't want all the grain to come out.
Before, you'd have like, for example, old banks would have like a tiny little door, right?
So of course, so nobody can stick a gun in and shoot, but also there is a maximum amount of things that can come out from one side to the other.
And what I think the scripts really do is it resolves like the HSMs that banks have been using for for, you know, ages.
And everybody else in industry similar have to do this, which is, you know, can I add some very world compatible policies to my spending, right?
Like, so please don't add any more than one Bitcoin per hour leave this vault, right?
It really is not that complex when you actually sort of come down to earth with like very mundane kind of examples.
Because if somebody gets hold of those keys, you don't want them to drain the vault.
Maybe they just take a little bit out until you find out.
And you really mitigate risk in that sense.

Speaker 2: 00:10:53

And then if you combine that with one of the two main things that Taproot gave us, is the ability to more easily compose multiple policies together.
So You can imagine having a policy where you say, with this one key I have some velocity control.
I can only spend money to a particular address, or I can only spend it some unit per some number of blocks.
But then if I combine that with a second key, then I can override that velocity control.
And so you can say, if I turn all of my nuclear keys at the same time, then I can spend all of the money.
But otherwise I have this very constrained flow out of my vault.
And this is something that probably one of the more broadly used uses for Bitcoin is savings.
Store value and custody is the killer feature for Bitcoin right now.
And so the ability for people to more easily protect their Bitcoin is, you know, a set of features that

Speaker 1: 00:11:55

I think we should be pursuing and investigating.
But to just underline the general point of what covenants are, I think that word introspection is probably a better description of what we mean when we say covenants.
There are a lot of Bitcoin developers behind the scenes who get mad at the branding of Covenants because it has negative connotations.
But what you guys said is right, which is that Covenants really just increase the scope of what we're able to look at from within the script interpreter when we're spending a coin.
And that winds up oftentimes being on the output side.
But you know, you can think of in a sense, we already have like a time lock is almost like a covenant because that's not necessarily on the input side.
That's, you know, you're looking at the end lock time in the transaction.
So we're already looking at some things that are, you know, outside of the witness.
We just want to look at more things so that we can, you know, do these interesting and vital applications like vaults, like, you know, congestion control, which I think is going to be increasingly important when we start scaling to second layers and want to provide safe exit for everybody.
A lot of the scaling solutions that have been proposed in the last few months.
Pretty much every draft for, you know, whether it's ARK or John Law's timeout trees, they all use this, these covenant primitives of being able to say, hey, I want to be able to commit to spending to a certain set of outputs without needing a signature.

Speaker 0: 00:13:38

Well, right now in Bitcoin, like the biggest issue is we have this very raw way of handling transactions.
It's like, you know, you essentially throw your gold into a bucket and you hope that lands in the bucket and stays in the bucket.
And if you ever wanna like take it out of the bucket, you just turn the bucket upside down and whatever is in that bucket comes out.

Speaker 1: 00:14:01

It's all or nothing.

Speaker 0: 00:14:02

That's it.
That's a very cool, sort of like amazing primitive, like that we finally figured out how to do with computers.
But it really limits us in a way that is detrimental to the ultimate goal, which is replacing central banks.
We're not even getting into the shitcoining idea, velocity, payments, fuck payments for this conversation.
None of that.
We're talking about just pure, unadulterated, store of value here.
If you just think of that, what is the ultimate goal of a store of value?
It's store the value safely, right?
Totally.
And like, make sure you don't lose the value by losing the

## Watchtowers

money.

Speaker 1: 00:14:41

If you want to be a global reserve asset, you have to have an absolutely bombproof pattern for custody.
Like a setup where if you follow the instructions the right way and they're not terribly complicated, that you know you're not going to lose your coins.
If you have your coins vaulted and you have a certain number of watchtowers, you just know that there's no way that those coins are going to get stolen.
And I think we need that.

Speaker 0: 00:15:05

I mean, you don't even need to watch towers.
Like you don't even need to get that complicated, right?
Like you can have a like a watch only wallet, right?
That might give you like, you know, like might tell you from the from like the mempool that there is a transaction being tried.
So I know that that's what a watchtower does.

Speaker 1: 00:15:22

Yeah.
Yeah.
No, I know.
Different kinds of watchtowers.

Speaker 0: 00:15:24

I know.
But like when we say these big words, right, like we're now thinking, oh, my God, watchtowers, it must be some other crazy, complicated, you know, galaxy brain thing.
It's not.
It's just a fucking wallet that watches for transaction.
That's it.
Like,

Speaker 2: 00:15:37

somewhere there's like a watch only wallet.
And if it sees a transaction happen, it broadcasts this clawback transaction and that's it.
Right.

Speaker 0: 00:15:45

Like we have a dog that barks.
Yeah.
If he sees the wolf, he barks.
There is nothing more to it.
Like it is not like related to changing Bitcoin.
It's not like, you know, some of the lightning crazy shit.
Like, no, no, no, no.
This is very, very simple.
You're just watching for transactions related to you on the mempool.
Nothing else.

Speaker 1: 00:16:05

Right.
You got a 19 year old intern sitting there refreshing mempool.space and that's your watch tower.

Speaker 0: 00:16:10

That's it.
Like, yes, they are the watchtower now.
Look at me.
I'm the watchtower now.

## Use cases for vaulting & scripts

Speaker 2: 00:16:16

Pretty incredible, right?
Because like without that kind of primitive, like some kind of vaulting primitive, what we have right now is if you want to hold a lot of Bitcoin, you need to have the most paranoid lockdown security setup in the world to make sure that one bad event doesn't happen one time.
Because if it happens one time, you're done.

Speaker 1: 00:16:38

And that's a centralizing force, right?
100%.

Speaker 2: 00:16:42

So every rich guy ever

Speaker 1: 00:16:44

is going to say, oh, I got to take my coins to

Speaker 0: 00:16:46

my point base.
I got to out order

Speaker 2: 00:16:47

The guy that has all the HSMs and has all the armed guards pointing guns at each other around the HSMs in order to protect this.

Speaker 0: 00:16:54

But if we had- This is why Deco exists.
Yeah, if we

Speaker 2: 00:16:56

had some vault set up, you could have a $3 wall wart with like a USB chip or a wifi chip and it plugged into your wall.
And if the bad thing happens, that thing broadcasts a single transaction and you get all your money back.

Speaker 0: 00:17:11

You know, we have like, there's two problems here, right, that I think is important to separate.
One is you still need things that create very safe key material, right?
Like you still need to create keys that are very, very safe, right?
And we still like, you know, have to go through crazy hopes like to do those things safely, right?
Like, you know, you're throwing your dice on your cold card and like you create your key material, right?
But what we wanna do is we wanna make now the other parts of it become less problematic because the rest of the stack, right?
The business logic right now is completely merged with your main key.
100%.
Which is a huge fucking problem because remember, like, you know, if you take, if you take, just, if you just assume, right.
That the stack with the deterministic build and shit on your hard wall, it's all sort of like kosher, right?
Like, you know, your keys are good.
Right.
But right now the problem is every time you want to sign for like, you know, a 1% of the stack that's being protected by that, you have to put the whole thing at risk.

Speaker 2: 00:18:17

Yep.
You got to dump the whole bucket

Speaker 0: 00:18:18

out.
Everything.
Right.
Which is a huge fucking problem.
Right.
So if we can separate this business logic for lower amounts transactions right from your total bucket pile key material like we win huge.
Like it's a huge improvement.
And like Rindel was saying, and James were saying, like, you know, you have the centralizing force, BitGo exists because corporate, especially corporate, or extremely large holders, you know, when, when you are telling, you know, your people who like legally and logically sort of like maintain the policies on how you do stuff so you don't get robbed and you have insurance, right?
Because nobody with real amounts of things do things without insurance except us insane people in Bitcoin.
Yeah.
You know, like, you need to check some boxes, right?
Because, like, they know through actuaries, through time, through history, right?
They're like, if you don't do certain things in a certain way, we have extra counterparties, right?
Like, you will lose the money.
Like, this is like, you can't just have Michael Sealer have like, you know, like the coins in a single hard wallet because, you know, he runs the company and he's the executive of the company.
You can't do that, right?
There's other shareholders, right?
And the way you find accountability, right.
And you find audits on logs and all this stuff.
Anything that's happening is by having counterparties, having other parties that co-sign, right.
They will have different incentives, right.
Maybe they are co-signing solution like BigMoney.
And their incentive is make sure that everything is accounted for and doesn't get signed until you meet some threshold that you set with them to begin with.
We can do all this with scripts.

Speaker 1: 00:20:00

Right, right, right.
And that makes it into a low overhead process that many, many, many people can do instead of a few specialized companies that are able to hire tons of operations people to do this stuff.
But a necessary prerequisite to getting to that point is to enable some kind of a covenant in Bitcoin.

Speaker 2: 00:20:20

Well, and not only does it help make it more accessible, but I think it also helps with the censorship resistance and permissionless aspect.
If the only way you can safely hold a large amount of your value in Bitcoin is if you're in a position where you can have a contractual relationship with a very well-operated service provider.
Then over time, especially in certain regulatory regimes or in certain legal scenarios, that ends up shutting out a lot of people where they say either I have to hold this asset in an incredibly risky way or I have to not hold this asset.

Speaker 0: 00:20:57

Or KYC, right?
I mean, like, you know, Like most people in Bitcoin don't want a KYC because you know KYC is the crime.
So like you know if you and this is assets you own under jurisdiction that allow you to own them so you're not breaking any laws you're not doing anything wrong even though you know we can argue about that stuff.
But you know just just like following within the Fiat universe that we live in.
You know, you're in a position that you can do this stuff by yourself.
You don't have to report to anyone, right?
Like right now you can't use Bagel because they require KYC, right?
Most of the solutions do.
And then you have the privacy aspect too, right?
Because even if you find a non-KYC co-sign service out there, right?
Like they still have full visibility over your coins, right?
It's the prerequisite of how the scripts work right now.
So all this stuff is a huge problem.
And

## Use cases for vaulting & scripts

we can get into the current issue with lock time transactions, right?
Because like right now, if you want to do some stuff, you kind of can using a degrading multisig or something like that.
But every time you spend, you have to reshuffle all the coins again, which makes it unusable.

Speaker 2: 00:22:12

Let's unpack that a little bit because I think a lot of times when I've talked to people about, hey, we need some kind of covenant to do something like a vault.
What people will point to is, oh, well, you should do a decaying multisig.
The way that that works, if you're one of the three people who aren't asleep right now, and you haven't heard of this yet, is imagine you have a couple different spend paths in your tap tree and you say, okay, right now, my coins are in a three of three multi-sig, but after three months, I can use a different path where I can sign with two of those keys.
And then three months after that, I can sign with one of my keys.
So the idea is that normally it takes three keys to spend my coins, but if I lose one of them, I just have to wait.
And if I lose two of them, then I wait longer.
And folks want to do this for like inheritance or just for more flexible multi-sig or key recovery.
And the problem there is that that timer of having to wait starts as soon as the UTXO is created.
So if you're just like hodling coins in your wallet, then after three months your security degrades to a two of three and after three more months it degrades to a one of three.
And so if every month you're buying Bitcoin and throwing it into your wallet, then every time a UTXO gets to be two months and 28 days, you need to go and do an on-chain transaction to effectively reset the timer.
And when you start talking about large amounts of money or operational complexity, I think that starts to be a non-starter.
It's hopeless.

Speaker 0: 00:23:51

I fucking hate it.
Yeah, and

Speaker 2: 00:23:52

when fees go up and shit gets expensive, it's going to suck.

Speaker 0: 00:23:56

I love that people are trying, but it doesn't work.
There's a reason why nobody's using it.

Speaker 1: 00:24:00

Yeah, you've got to dig up all your keys on a periodic basis, you know, like activate your spending capacity on a periodic basis.
And that's always an opportunity for theft or security.

Speaker 0: 00:24:11

You know, if you're a crazy person like me, you know, if you want to spend anything, you need to like, it would take me like probably a couple months like I have to travel to different countries, wait for things, it's like crazy shit right?
And like wouldn't it be cool if you can represent your trust you know as a script and you know like you just sort of essentially wash your fucking hands when you die.
It's right.
Sorry.
Right.
This is how it works.
You know, it's a little crazy, but like totally within the helm of possibility.
If you have like some decent introspection on this.
Mm-hmm.

Speaker 1: 00:24:49

Well, and in some ways what, like for example, OpVault does, like one of the things that OpVault does is like Rheindel was saying, you know, when you spend the coins into that structure, you start the time lock.
All the covenant does in OpVault is basically say, we're gonna delay that until like one spend out further so that when you spend the coin from there, then the time lock starts, then that clawback period starts.
So you're just kind of like delaying that decay process.

Speaker 0: 00:25:20

I like to say that time locks should be reactionary.
They shouldn't be part of the initial transaction that you want to make.

Speaker 2: 00:25:27

What you really want to do is you want to start the timer when you initiate the spend, not start the timer when you receive the money.
And what we have right now is you start the timer when you receive the money, and what you could do with OpVault is say, I want to do a withdrawal.
There's two ways for me to do a withdrawal from my vault.
One of them is I take the transatlantic flight, I go and get all of my keys and I can spend my money immediately.
Or I have a single SIG key and if I spend that, that starts a three-week timer.
And during that three-week timer, I can push a button and cancel it and claw my money back.
Or if I don't, if I don't cancel it, then my money goes where it's supposed to

## Covenants as a solution to third party

go.

Speaker 0: 00:26:10

I mean, think about like how like stupid works right now, right?
Like, you know, when you have a safe, a deposit safe, right?
Normally when you put the money in the hole, it just drops inside.
But right now, and then when you want to open, normally you have a timer, right?
So you put in the pin and then you have to wait like three hours to open or something, right?
Right now is the opposite.
When you drop the money, the money takes like, you know, three hours to drop, but when you want to open it, it just opens.
Like, it's just like completely stupid.

Speaker 2: 00:26:44

Or just another example, right?
Like If you have a Coinbase account or a Gemini account, they both have this feature where you can say, I have a white list of addresses, and I can withdraw my coins only to those addresses.
And if I want to add a new address, then I have to do MFA and I have to wait a seven-day waiting period before that address is active and I can withdraw to it.
And so that way if somebody compromises my Coinbase account, they can't just steal all my money.
It's kind of crazy that if you want, that's a great feature.
If you want that feature, you have to go with a KYC custodial holder of your Bitcoin.
What I think we would all want is for any Bitcoin wallet that anybody goes and builds permissionlessly in the world to be able to have that functionality and have it be enforced by Bitcoin consensus instead of having to rely on business logic of a centralized custodial

## Covenants and censorship risks

server.

Speaker 1: 00:27:43

Totally.

Speaker 0: 00:27:46

I mean, it's an easy conversation here because the three of us agree, right?
What is the steel man argument against Covenants?
So far I heard, you know, like, oh, you could have issues where, I don't know, the government forces you to participate in some.
Well, they can do that with multi-sig now.

Speaker 1: 00:28:07

Right now.
Yeah.
Yeah.
And it's much more practical with multi-sig.

Speaker 0: 00:28:10

Way more because you want the opposite.
Yeah.
You want to participate when you sign and not after.

Speaker 2: 00:28:18

And maybe we can unpack why MultiSig is actually a great solution for the state wallet for FedCoin and why covenants would be bad for FedCoin.
So the risk here that people are worried about is they're worried that there's some regulatory crackdown and the government says You must receive your Bitcoin into a wallet that enforces this covenant and this covenant restricts who you can send coins to.
So if you eat too much meat, if you say wrong things on Twitter, whatever you do, then you're going to be on the blacklist and James won't be able to send me coins.
And if I have a good enough social credit score, then I'll be on the white list and James can send me coins." That's the threat that people are worried about and they're worried that introducing covenants will open this new vector for this kind of control on Bitcoin.
The thing is that with all the covenant proposals that are being seriously talked about like CTV, you have to exhaustively enumerate all of the different destinations and all the different kind of shapes of transactions that coins can take at the time that you receive those coins.
So one of the things that that means is, let's say that you're some government agency that's maintaining this whitelist based on, you know, social credit score or something.
Every time that whitelist changes, you would have to get everybody to re-spend their coins to a new version of the covenant that includes the new whitelist.

Speaker 0: 00:29:53

Oh, and they're going to fuck up.
And they're going to fuck up all the time.
Like 100%.
Absolutely.
This is within the stuff they fuck up.

Speaker 2: 00:30:00

100%.
Yeah, like Screwing up a list of things in a database is very on-brand for bureaucratic fuck-ups.
What you would much rather do, that's one problem, and then there's other problems.
Not only do you have to enumerate all the destinations, but you also have to enumerate all the change addresses.
Managing this whitelist through on-chain rollover of UTXOs is just like a non-starter.
It's expensive, it's slow, it'll never work.
If instead you did something where you said, for FedCoin, James, if you want to be compliant, you have to receive coins into a wallet that does a two of two multi-sig.
And you hold one key in your FedCoin wallet, and then me, the government, I hold a second key.
And then what I do is I just run a co-signing server.
And The whitelist is just a database.
It's just a plain old MySQL database.
Whenever Rodolfo gets kicked off of the list, he's no longer allowed to receive FedCoin, I remove him from the whitelist.
And then if James wants to send him Bitcoin, it sends a cosigning request to the server and the server says, nope, you're not on the whitelist.
He goes, send me coins and I'm a good citizen.
So it says, yep, he is on the whitelist and it just cosigns it.
You could update that whitelist hundreds of times a second.
It doesn't have increased on-chain footprint.
You don't have to roll these things over.
Blockstream actually already has a product like this.
It's called AMP and it's used for issuing regulated assets on Liquid.
So if you want to buy a stock on the Liquid network, they only want you to be trading stock with other people who are accredited investors or whatever.
So they have a co-signing server that restricts who the token can go to.
So we already have the technology to do Fedcoin today in a more efficient way and a more operationally sound way than using covenants.
So it doesn't matter.

Speaker 0: 00:31:52

I mean, personally, if I were to do Fedcoin, I would do it on Ethereum.

Speaker 2: 00:31:56

Yeah, for sure.
Because it's

Speaker 0: 00:31:57

actually quite perfect for it.
I mean, it uses accounts, it doesn't have UTXOs. So you can keep an account on the whole person's pile of an asset.
I mean, they have the whole shebang for it.
No wonder they're probably right now knocking on the door of regulations.
Can you please use our system for it?

Speaker 2: 00:32:13

There's already regulated stable coins on it.
The account thing is actually a big deal.
If you want to be able to look back and see transaction history, that's very hand-wavy in a UTXO system.
In an account-based system, you just look at the transaction history for an account and you say, yep, Here's the NFTs that you bought.
Those are hate speech.
So you're no longer allowed to receive your stipend.

Speaker 0: 00:32:37

That happened with Tornado Cash.
Because people sent and wanted Tornado Cash to people in their accounts.
So here's just so people to understand the difference.
So think of the UTXO system as essentially like we have 21 million coins, right, like literal physical coins, okay?
And we just send and receive these coins.
They are not mine, really.
They're just part of the network and I happen to own them right now.
But it's really akin to gold in that sense.
The account system, on the other hand, is essentially like how Fiat works.
It's a ledger-based system per owner.
So the owner has its own ledger.
So it's fucking terrible for privacy.
So anyway, so this is all interesting.
Is there any other steel men for...

Speaker 2: 00:33:23

I think

## Covenants and censorship risks

the best argument that I've heard against specific proposals like CTV, which is I think the one that probably, I'm going to go out on a limb and say CTV probably has the most consensus out of all the covenant proposals right now.

Speaker 0: 00:33:38

Let's just have opinions, it's okay.

Speaker 2: 00:33:40

Yeah, for sure.
And I think the strongest argument that I've heard is maybe it doesn't go far enough.
Like maybe we want a more general covenant.
Maybe it's too restrictive.
And if we're gonna go through the social activation energy of doing a soft fork, maybe we should like make a better covenant.

Speaker 0: 00:33:59

But- Yeah, but that would never happen because now it's too big and everybody's going to have more reasons to bike shed and hate on things.
It's hopeless.

## Risks of major Bitcoin changes

Speaker 1: 00:34:07

Yeah.
And so that that was actually the impetus for AppVault.
But maybe let's put a pin in that and go back to some of the like, like one concern that I can think of that's reasonable is anytime you're adding functionality to the Bitcoin script interpreter or changing it, you know, there's some level of risk there.
And I think in any case, you do have to be very diligent about looking at the proposed change to the script interpreter and saying, okay, well, you know, is this going to increase computational requirements for doing validation?
Is this is there some new avenue we've introduced for DOS?
You know, does this require more caching or whatever to make sure that the validation time doesn't actually blow up when you use this new feature.
And when Jeremy introduced CTV, I was like, OK, I'm going to go pore over this thing and see if I can actually break it or find some kind of critical issue.
And what's funny is that for all the reputation and ire that CTV has accumulated over the years, in its early days anyway, the change is really, really simple.
And yeah.
It's tiny.

Speaker 0: 00:35:20

You know, it's funny.
I started as a CTV liker and then I became a CTV hater because of because of how it started to get pushed and everything else.
And then and then I became a CTV lover again.
You know, like I went through the whole roller coaster of sentiments around it, because, you know, I think Sapio and And like what you can do with CTV once you go galaxy brain really sort of like confused me And you know, I don't have the bandwidth to go fucking review it, you know And and you know, I think he muddies the water I think if we had just kept it to like what it is and like here's where it goes as opposed to like look at all the insane shit you can do with it if you do it this certain way.
Yeah,

Speaker 1: 00:36:10

I think Jeremy got tired of talking about Rossi TV because again, it is so simple.
And he develops APO, which is like this, like very space-aged, you know, smart contracting platform that compiles down to Bitcoin script.
And he started showing that off and people looked at that.
And I mean, that's like a, that's a very complicated system.
And I think that scared, you know, that scared a lot of people because they weren't made aware of the distinction between the underlying script primitive, which is CTV and Sapio.

Speaker 0: 00:36:42

You know, I mean, I'm a little bit of like the, I transverse both the Luddite camp and the non-Luddite camp when it comes to Bitcoin changes, you know, the ossification versus non-ossification.
And what truly scares me with Bitcoin changes is we have a thing that works, okay?
Like, and it's kind of a fucking big deal.
It's the only thing we have.
And my bags depend on it.
Right.
So, I am really scared of unknowns, unknowns.
And it's very hard to know what happens.
Right.
I mean, like, you know, we saw the taproot thing.
I feel like a lot of people got taken for a ride on Taproot.
They couldn't understand it.
And they got to accept it because, you know, the devs say it's okay.
And then we had, you know, the dick butts show up on chain.
And people are like, look, you know, you can have unknowns, unknowns.
Right.
I mean, it made absolutely no difference.
Once people understood really like it's all dying down, it's all, you know, the economics kills these things.
But it could have been worse to be to be fair to people.
It could have been worse.
Right.

Speaker 1: 00:37:46

Oh, for sure.
And taproot was basically like lifting the engine out of Bitcoin, you know, and putting a new engine in and,

Speaker 0: 00:37:55

oh my God.
Yes.
Why are running?
Yeah.
Well, well, both of them were

Speaker 2: 00:38:02

So like SegWit and Taproot were both huge upgrades that kind of fundamentally change how Bitcoin works.
And CTV or APO aren't.

Speaker 0: 00:38:14

I mean, CTV is akin to like up.
Check lock

Speaker 1: 00:38:17

time verify or check sequence.

Speaker 0: 00:38:18

No, not even.
It's more like opcode.
Like you just have a little space there, you stick some stuff, it makes no fucking difference.

Speaker 2: 00:38:27

Yeah, and like what CTV does is it takes a whole bunch of fields in the transaction.
And we can rattle them off, but it takes a bunch of fields in the transaction and you hash them.
And then you say, check template verify, and you provide that hash.
And when you go to spend those coins, if those fields in the transaction hashed the same value as what you committed to, then the transaction is allowed.
And if they don't, the transaction is denied.

Speaker 0: 00:38:52

It's like there's a very simple mechanism.
Here's the worst case scenario for CTV, okay?
People YOLO their scripts and they can't move their coins anymore, which is going to happen.
But that's great.
For sure.
That just makes Bitcoin be more deflationary.
You know, seriously, like I already believe that 20, 30% of all Bitcoin cannot be moved, right?
Because people just don't know yet.
They cannot move their coins.
Right.
It's always the...

Speaker 2: 00:39:14

Yeah, for sure.

Speaker 0: 00:39:15

But with CTV, it's just more of the same.
You don't have to use it.
It's backward compatible.
It's all like, whatever.
And it doesn't change the incentives.
Sorry.
It doesn't change incentives when it comes to mining.
It doesn't change the incentives on any of this stuff.
We don't have economic incentive change that you wouldn't happen already if you didn't do, if you couldn't move your multi-sig because you forgot the script or whatever.

## Cryptographic improvements of CTV

Speaker 1: 00:39:39

Another interesting thing is that CTV is basically just a hash comparison.
And that's like upwards of 20 times faster than elliptic curve operations.
So the CTV opcode itself is like way faster than a Schnorr verification.

Speaker 0: 00:39:53

Do we need a new name for it?
Hash check.

Speaker 1: 00:39:56

I I don't want to.
I it's it's it's fine.
Like, you know, we've we've done so much deck chair rearrangement, I feel like with this stuff that people just need to grow up, put on their big boy pants and like come to grips with the existing, you know, branding and

Speaker 0: 00:40:12

take it

Speaker 1: 00:40:13

for what it is.

Speaker 0: 00:40:13

Do you

## Quantifying the scale of change in code

think would be more helpful if we can get the TX hash people, the APO people and like whatever fucking thing people wanting to like more on board of this and hey, you know, like all this stuff you guys are proposing is not going to fucking happen.
Like I am certain that TX hash is not going to happen.
For example, it's like two out there.
It's like it's too much code.
It's just like, you know, sure.
I mean, maybe maybe if we debate for another 10 years, it's not impossible.
Let's put it this way.
But like, realistically speaking, and imagine Bitcoin in 10 years, The amount of different people who own it and not willing to change it, right?

Speaker 1: 00:40:48

Yeah.
Well, bit of news.
I spent the last week putting together a branch on core that has CTV, APO, and OpVault.
And it's 6,000 lines.
That's not a big change.
That's not a lot of that's including like all the test code.
Yeah.
The test vectors and all that stuff.

Speaker 0: 00:41:09

If you compare that to outside of sorry, outside of tests.
How much are we talking about here?
Like a third?

Speaker 1: 00:41:15

Yeah.
Yeah.
I think probably two thousand lines.

Speaker 0: 00:41:19

And you didn't forget any comma, right?
And a lot

Speaker 2: 00:41:22

of that test code is like Python, which is more verbose because it's like wallet setup.

Speaker 0: 00:41:28

Yeah, a lot of

Speaker 1: 00:41:28

the CTV code is just like these raw transactions and big JSON files that Jeremy generated to make sure everything is cool.
A lot of the APO test codes, there's a fuzz test case in there.
So it's really padded out with a lot of test code.
So like these changes are small.

Speaker 0: 00:41:45

But here's the counter argument to that, right?
I mean, like, you know, changing the block size was, you know, a single number change there, you know, so it's like, it's, it's, you know, The size of the code, I mean, for people to understand is like the smaller literal character change in terms of code makes it a lot easier to review, right?
But it doesn't eliminate some other issues, right?
Because you could change a tiny little thing and cause massive fucking problems.
But like, that's what tests are for.

Speaker 1: 00:42:19

Totally.
Yeah.
And that's, I mean, yeah, the size of the code makes it more readily comprehensible, but I just brought that up to compare it to, and this is like the way opposite end of the spectrum, like to like simplicity, You know, the proposed change set into elements is like something on the order of 80,000 lines.
And I know that allegedly comes with a lot of test code and proof verification and all that stuff.
But, you know, that like scrutinizing something like that is like, you know, a much, much, much bigger proposition.

Speaker 0: 00:42:48

And it's also a single source.
It comes from a single company.
We like them, but it's much harder for you to review something in terms of face value when it comes from a single entity, right?
Like if you had like 10 entities that hate each other writing that code, it'd be much more believable, like much more trustworthy on face value.

Speaker 2: 00:43:08

Well, and like, I would argue that the actual amount of code that's gonna be needed to make that thing useful is probably gonna be another order of magnitude larger.
Cause the thing with simplicity is it's this very low-level scripting system built out of these algebraic combinators that you assemble together and then they create predicates for your scripts.
In order to actually make software out of that, we're going to need higher level languages and libraries to actually build tooling for it.
If we have, call it CTV and Vault, you can hack four lines into Peter Todd's Bitcoin Python library and start using it.
You can start building a wallet on top of that.
If you have APO, you can hack a new SIG hash flag into your favorite Bitcoin library and you can start doing APO things.
So it's 7,000 lines and that's enough for people to start using it.
I would say something like Simplicity, there's probably going to be other languages and libraries and tooling that we're going to need

Speaker 0: 00:44:15

on top of it.
We can also steal men from the other side and see how absurd it is.
Remember OpEvol?
It broke Bitcoin.
This is OpEvol's method.
It's like, that's the wrong way to go about it.

Speaker 2: 00:44:32

I did a read of Luke wrote ConsensusLogic for BIP300 for drive chains.
And that's not a ton of code, but that comes with a whole bunch of new minor incentives and a whole bunch of new economic incentives for Bitcoin to just behave differently.
And it introduces a brand new security model.
It's actually a pretty big change.
Something like CTV is, yeah, if you screw up you might not be able to spend your coins, but that's not going to affect my coins.
I think one of the big differences between something like Bitcoin and something like Ethereum is that Bitcoin transactions don't go and mutate a whole bunch of global state.
I can't write a locking script that messes with James's coins.
Right.
I think that's like a core invariant in Bitcoin.
And none of these proposals that we're talking about change that dynamic.
Like I might lock myself out, but I'm not going to lock James out.

Speaker 0: 00:45:29

That's right.
I mean, like there is no socialization of your transaction here.
Like there is no externality to them.
Like you're not making everybody do anything else.
Like, you know, it's more akin to like, you know, you just happen to use addresses that like you mind and they all have like, you know, five A's at the end.
Like it's irrelevant to the rest of the network.
The

Speaker 1: 00:45:53

only way that it would affect other people is again, if the validation complexity went up somehow and you could kind of abuse these new op codes, but

Speaker 2: 00:46:00

with CTV

Speaker 1: 00:46:02

that's been proven not to be the case.
With APO, I don't think that's the case.
So, we talk about TxHash, and for people who haven't heard of TxHash, all TxHash is, is a way of, Like so CTV takes certain parts of the transaction, rolls it into the hash, and then does the comparison with TxHash, you can kind of select different parts of the transaction to go into that hash.
So you have something that's in theory more flexible, But the problem is because you can do all these different hash combinations, then you have to start worrying about what's called quadratic hashing attacks, which is where you select a bunch of different incantations of that hash in the same transaction.
And then all of a sudden, the validation engine has to do a bunch of work to do some kind of a combinatorial selection of all the hashes that are possible

## TX hash

with the transaction.

Speaker 2: 00:46:53

So I thought with TxHash, and maybe I'm behind on this, the original TxHash proposal was you'd say opt TxHash and then you would pass a bit mask basically of which fields to select to go into the hash.
And the idea was that at a consensus level, only certain values of that bitmap would be allowed.
And so the idea is that on day one, when it got activated, the only permissible value is like the exact same set of fields as CTV.
So in my mind, it's kind of just like rebranding CTV, like CTV has too much baggage with a certain sect of people on Twitter.
So we're going to rename it and add a bitmask.
But the idea is that in the future we could soft fork new allowed values for that bitmask.
And so I assume that in order to get people to do that soft fork, you'd have to show them that this thing doesn't open you up to quadratic hashing.

Speaker 1: 00:47:49

So three points there.
Number one, the two main distinctions of TxHash from that CTV use case that you're talking about is, number one, you've got data loss because you've got to provide an extra parameter just to say, oh, do the CTV hash.
Number two, Tx hash would be a tap root only opcode.
So you have to use tap root.
And that means it's not a space efficient because it turns out that like literally the most efficient version of CTV is doing a bare CTV so that you just have the 32 byte hash, the two byte op code.
So you're 34 bytes, not even a paid a script chat, it's just a raw script.
So if you wanna do congestion control, that's like the most efficient incarnation of that.
But then the third point is that a lot of people don't realize that CTV actually was designed with upgradability in mind.
So what happens in the CTV rules is if the hash that you pass as the argument is 32 bytes, it does the default CTV hash.
But the way Jeremy designed it is, if that hash is more than 32 bytes, if there's like an extra flag on there, it's opt-true.
So if you wanna soft fork in more template hashes, you can if you want to.
So it's really, it's just, you know, it's all the same stuff except TX hash is less

## Simplicity of CTV

space efficient.

Speaker 0: 00:49:04

The way I like to think about this is more like, you know, CTV is essentially up return.
You know, you're just storing, you know, 32 bits there, 32 bytes.
And then when, well, all we're saying is that for a transaction that says it's a CDV, like check that that hash matches, that's it.
Like there really is nothing

Speaker 2: 00:49:26

else to it.

Speaker 0: 00:49:27

Yeah.
And you know, this is not to minimize like, you know, tertiary effects kind of thing, but, it does make it a lot easier on the cold side to review and, and sort of like, you know, make sure that we're not sort of causing like technical bugs, right?
Like, you know, economically speaking, you know, maybe there's more conversations to be had.
I'm satisfied.
But, you know, maybe maybe people can still argue more about the soft stuff.
But on the hard stuff, like it's it's it's pretty like simple.

Speaker 1: 00:49:58

Yeah.
Yeah.
And it's been picked over by everybody.
I mean, everybody wanted to find a problem with CTV and the code's been out there unchanged for so long.

Speaker 0: 00:50:06

Well, and if I remember

Speaker 2: 00:50:07

right, there's like a five Bitcoin bounty out there for if you find a bug in it.
To this day.

Speaker 1: 00:50:12

To this day, yeah.
If you find a sizable bug with CTV, You get something like five Bitcoin from the Lincoln Labs people.

## The consensus deadlock

Speaker 0: 00:50:19

You know, now, like, you know, as we all know in Bitcoin, you know, for as much as we like to say Bitcoin is decentralized, it kind of isn't when it comes to like Bitcoin updates and things, you know, like you kind of have to get the, the approval of the, of like the, the main original gray beards, you know, like, and, and like, how's the state of, of the, of like, you know, Gmax retired, essentially.
I'm sure he will have an opinion on Reddit, but like, you know, and, you know, and then, I mean, you know, you have Willy, you know, Pulse for maybe a little bit less, you know, but like, what's the state of consensus from the wizards?

Speaker 1: 00:51:10

I call this the consensus deadlock because we're in a situation right now where the people who have led the last few consensus changes to Bitcoin really don't want to weigh in because they have felt like they're encouraging this muscle memory in the community that they're essentially the implicit benevolent dictators and that they have to bless every new change.
And that's obviously antithetical to what Bitcoin is supposed to be.
So that's their choice.
I mean, I still wish that some of the people would involve themselves to an extent, but they don't have a willingness to.
So we're in a position now where there's kind of a credibility vacuum.

Speaker 0: 00:51:46

Yeah, I think the other issue, too, is aside, I mean, from people being burnt out, which, by the way, I believe people should be burnt out.
I believe we should be excruciating.
So horrible.
Maybe you might disagree with me, James, but like I want people to like literally hate working on core Bitcoin.
Like because it's done.
Yeah, exactly.
Right.
Like it needs to be so awful that like, you know, you're either, you know, like a spook or you're masochist or both, you know, who want to be there.
And it's so intense.
And it needs to be that way, right?
Because then you have less social attacks on it.

Speaker 2: 00:52:23

Well, I mean, maybe another way of saying it, right, is the only time that you go and start changing things on Bitcoin is when you have no other option.

Speaker 0: 00:52:32

That's right.

Speaker 2: 00:52:32

You're like there's no more pleasant way for me to do this.
So I'm going to have to go and change Bitcoin.

Speaker 0: 00:52:38

That's right.
You're in a spaceship, right?
You really don't want to do a spacewalk, you know, because that's how everybody always dies, right?
Like they have to go outside to fix something in their Epstein engine or something, right?
And then they die.
They fall into the vacuum of space.
So and I kind of feel like every time, you know, Bitcoin has changed, the people who went to walk outside, you know, they fix the thing and then they sort of got swallowed by the vacuum of space and then they never come back.
It's OK.
It's OK if people were, you know, they burned themselves out doing that one thing, and it's for the common good.
So like, OK, so we don't have those guys.
And in all honesty, like I have a feeling that like, if we, if we have those guys, then, then the bike shedding was also start and, you know, unlikely to get anywhere.

Speaker 1: 00:53:29

What I'll say is two things.
Number one is that I think vaults is something that's widely recognized as being really, really desirable.
Pretty much, you know, the vaults have been talked about since 2013.
And I think every major contributor to Bitcoin at some point is, yeah, this is probably functionality that we need.
Otherwise, custodying coins is just too much of a crapshoot in the long run.
And number two, as people keep coming up with these proposals to do things like scale the Lightning Network, scale UTXO ownership, do vaults, people keep reinventing the need for CTV.
And I think it's just become obvious to a lot of the technical community, whether they're coming out and saying it explicitly or not, that we just need this primitive.
So I actually, I mean, the reason I started preparing this soft fork branch is because I think if something like that were proposed, there would be a lot of, there would be pretty good broad consensus that, okay, maybe it's time to look at activating CGB and APO.

Speaker 0: 00:54:35

Did you buy your helmet to walk in space yet?
This is gonna be your retirement project.

Speaker 1: 00:54:40

Yeah, honestly, the social stuff doesn't really bother me that much.
Maybe because I think I make fairly limited claims and I'm not that pushy, but yeah, I'm ready to take the spacewalk, I guess.
Mostly because I'm hoping it'll be a pretty boring spacewalk and I won't be offended if I get totally rejected.
And because I like I just I've spent enough time prototyping this stuff and working with it to say that like, yeah, it'll probably happen eventually.
And if it doesn't, that's fine.
I mean, I think it'll be to Bitcoin's detriment.
And at that point, I'll probably go and work on something else entirely.
But that's OK.
Like, so, yeah, I don't know.
I'm I guess a little, you know, zen about it.

## Social coordination and activation

Speaker 0: 00:55:34

So like, I think like, you know, honestly the main problem is gonna be activation and how to do it.
Like I mentioned many times and I think most devs still cannot internalize it.
They're like, you know, speedy trial is it's not something that passes the mustard in terms of like how users and the economic nodes feel.

Speaker 1: 00:55:52

It's hard- So tell me what speedy trial is.
Let's make sure we agree on definitions here.

Speaker 0: 00:55:58

So, you know, I think the problem really is you can't have something that does not have Flag Day.
People want the Game of Chicken.
You're trying to remove the Game of Chicken.
What happens with that is you show your hand.
See, all the devs wanna do is remove the game of chicken.
That's what Speedy Trial does.

Speaker 1: 00:56:28

Well, I mean, so with Softworks in general, like when you provide a way to coordinate miners doing the upgrade, you're not like, I think it's a big misconception that that process is somehow designed to solicit the feedback of the miners or to ask for permission from the miners.
It's really not.
It's it's literally to coordinate the upgrade that we're going to do one way or another to make sure there's no chain split.

Speaker 0: 00:56:57

Oh, no, no.
I understand.
That's that's what technically.
Yeah.
So technically, that's that's what the code does.
The problem is once you get miners to coordinate before economic nodes, what it really signaling is that the miners are choosing if they wanna do something or not without knowing how the economic nodes are going to go.

Speaker 1: 00:57:21

But how do the economic nodes broadcast their willingness for a fork?

Speaker 0: 00:57:26

Well, UASF, the way it should be.

Speaker 1: 00:57:29

OK, so what, we're all going to go out and advertise via user agent that we want a certain fork.
Well, that's Sybil.
That's a Sybil attack.
Like there's just no good way of economic nodes saying, yeah, we all want this thing, you know.

Speaker 0: 00:57:44

And they shouldn't be.
See, like, I believe that part of the reason why Bitcoin was never successfully attacked is because there is not a clear game to activate anything for somebody to game.
This messy chaos that is UASF, even though it feels dangerous, it feels like it could be cybert or whatever, it forces true economic actors to coordinate out of channel.
Because trust me, everybody is calling each other meeting and trying to understand outside of Twitter and outside of the network, right?
Like, what are you supporting?
Where are you going?
So it is literally forcing people to do that coordination out of channel.
And then you're not showing your hand to bad guys trying to push in a different direction.
They simply don't know the state of things.
So they risk their coins.
It's actually quite beautiful.
It is true chaos.
And like state actors cannot game something that's chaotic.

Speaker 1: 00:58:55

Yeah.
I mean, I think if there's broad agreement that we should do something with consensus, like There's no reason to induce that chaos, risk chain splits and coin loss, and Bitcoin looking like an absolute shit show.
That doesn't make any sense to me.
UASF is always in the back pocket.
If miners drag their feed or if people want, you know, like you can always UASF and the opposite is always true.
Let's say the miners get together and they decide to activate some fork that, you know, doubles the supply.
Well, guess what?
Like the economic nodes can run a trivial Python script that examines each block.
And if it violates their rule set, it runs invalidate block.
Like the activation method is literally window dressing to make sure that there isn't a big chain split.
It's nothing more.
Because there's always the avenue to reject a bad consensus change if people want to.

Speaker 2: 00:59:57

It's been a while since I've read BIP-8, But my understanding was the way that PIP8 activations want to work.
I don't think we've actually done this yet.
But the idea is that you would run a lot equals true client.
So there's a drop dead date.
At this date, nodes will start enforcing.
And if the economic majority of the nodes are running that code, then this is now the will of the economic majority.
But you still have a minor signaling period to do early activation.
And that's not minor selecting.
That's minor signaling, I'm ready to not mine invalid blocks.
So that if you say the lot equals true date is two years out to give everybody plenty of time to upgrade.

Speaker 0: 01:00:51

Miners are last.
They don't even know where their mines are.

Speaker 2: 01:00:55

Right.
But the idea is that if we think that there's broad consensus before then, and if the miners are ready to upgrade all their software, then we don't need to wait the whole two years, but there's a drop dead date in two years.
That's my understanding of that mechanism.
Something that I've always thought would be interesting is, And I don't know, it's just an idea.
Let's talk about it.
If we think that a particular soft fork has broad consensus and we think that lots of people want to do it, we could go and solicit some donations from the community to put a wallet together to go and pay a miner to mine an invalid block once we think it's active.
Because there's no way for user agent signaling.
If you say, we're going to stick iLikeCTV into your user agent, It's trivial for somebody to go and spin up a million nodes on AWS and like have this sock puppet consensus.
But if a miner mined a block that includes a transaction that violates CTV and that block gets forked off of the network, then we know that CTV is active.

Speaker 0: 01:02:04

See, this is the problem, right?
We cannot use, until fiat is 99% of 9999999% of the total world economic value, right?
And Bitcoin is just a SPAC.
We cannot use any system that allows for economically stronger actor that has infinite money to fuck with it.
This is the problem, right?
They can do anything except make miners come out of the ground.
Right.
Because that's a that's a physical thing that you have to manufacture and deploy.
And they, you know, as we know, governments are not great at that.
It'll take them a little while.
And we cannot make anything that they could pay to go better in their...
So for example, with Segwit, we had the futures for the two tokens, which was Bitcoin and Bitcoin Cash on BitMax at that time.
That was very useful because state actors didn't have any time to game that out.
Right.
Because it was a one-time thing.
It popped up out of nowhere, total chaos, like spontaneous order thing.
Right.
If we make that part of the system now, we're essentially tipping the guys to prepare for that.
They'll get the funds ready and they'll sort that out.
And then like, can you imagine they could, they could totally skill that, right?
They can short the fuck out of one and long the fuck out of the other, right?
Because they have infinite money.
And now that, that futures market is completely gamed, right?
Because remember, again, these guys have disposable, burnable cash.
It's not like us.
They have real money, right?
Like you can't play that game.
This is one of the issues that I have.

Speaker 2: 01:03:43

Well, it's actually even worse than that because The way that budgeting works in large organizations is if you want the same budget next year, you can't spend less money

Speaker 0: 01:03:50

this year.
That's right.

Speaker 2: 01:03:51

So you are incentivized to spend all of your budget.

Speaker 1: 01:03:53

But hang on now.
I don't understand this, because how do you coordinate socially, which is a prerequisite to doing a fork, without publicizing your intent to do the fork.

Speaker 0: 01:04:05

No, you publicize your intent.
But remember, there is a very, very large amount of economic actors that are fully quiet on any sort of form of social media or whatever.

Speaker 2: 01:04:16

Well, I think the thing that MBK is saying is that you can't measure willingness or support through something that is gameable by an adversary with a lot of money.
So The example that I said of user agent signaling.
If I'm somebody and I want to tip the balance, I just go and spin up a giant fleet on AWS.

Speaker 0: 01:04:39

Amazon, credit card, problem resolved.

Speaker 1: 01:04:41

Have a huge AWS bill.

Speaker 2: 01:04:44

And it's easy.
The thing that I like about, let's pay a miner to go and mine an invalid block, is that that's something where you're measuring support by looking at what happens on the network, which is ultimately the thing that matters.

Speaker 0: 01:04:59

What if we had non-fidelity bonds?
That kind of really shows how much of the pile you have and how much you're willing to go.
You know, because then you can just show like, look, you know, like 10 million Bitcoin is willing to go this way.
Five million Bitcoin did not vote.

Speaker 2: 01:05:16

And so you're saying like you lock up some Bitcoin in like a time locked CTV thing.
And if CTV doesn't activate like that, Bitcoin's up for grabs?

Speaker 0: 01:05:24

Maybe.
Yeah.
I don't know.

Speaker 1: 01:05:26

Somebody tried this back in the SegWit days.
They came up with this scheme where you could sign a message of support using keys that correspond to some out points.
And I think, but...

Speaker 0: 01:05:39

But it's still fully gameable too, right?
Because you can't measure majority unless you truly have more than X million amount of Bitcoin in a meaningful way, but it has to be like ultra super majority.

Speaker 1: 01:05:51

Proof of stake.
I mean,

Speaker 0: 01:05:53

it's,

Speaker 1: 01:05:54

you know, like,

## Speedy trial - good or bad for Bitcoin?
so it's, yeah.
So I just want to be really, really clear for the audience and say that I think Speedy Trial again, has been victim to its branding.
And all it is, is basically a way of saying, hey, if the miners and the users like all agree that we want this consensus change to happen, let's just do an abbreviated period where if somehow within a few months, all the miners say, yeah, I'm ready to do this upgrade.
Like we can lock it in and wait even a longer period than BIP-9 had us waiting.

Speaker 0: 01:06:24

Well, but what if we tack on pre-SPD trial, there is a USF period in which like everybody runs the client, right?
And maybe there is like, you know, you make a transaction or something that like, if the miners do go through a speedy trial, then those transactions are valid.
Therefore, you know, everybody agrees now that this thing got activated.

Speaker 1: 01:06:48

No, but see, you guys are proposing hard forks.

Speaker 0: 01:06:51

Yes, absolutely.

Speaker 1: 01:06:55

Making a transaction that was previously invalid valid is a hard fork.
So, like, we can't, you know...

Speaker 0: 01:07:03

You got to put some skin in the game.

Speaker 2: 01:07:05

Wait, what, what, sorry, what, where was the proposal to make a previously invalid transaction valid?

Speaker 1: 01:07:12

I think NVK was just saying you should lock coins up in a way that, you know, like you have to activate CTV for the spend to become valid.
Yeah.
Yeah.

Speaker 0: 01:07:25

Exactly what Spirit Try is trying not to do.
See, I think this is the problem.
Like, You know, it's one of those things that, you know, cold wise, it's not too hard, right?
Like, I mean, it's not hard for us to program something that does this change very safely, right?
Like we know that.
The issue is, it's like, how do we satisfy the completely irrational chaotic part of what makes Bitcoin good?
Right.
Which is like the, essentially like the, the, the social, the, the social sentiment towards where things are going and, and, and sort of like having this chaos being the, the firewall against the opposite of it, which is state actors, right?
Like state doctors, again, cannot deal with chaos, right?
Like it's, it's, it's like, it's poison to them.
That's how the terrorists work.
That's like, you know, they just cannot handle shit that's disorganized.
So being disorganized is good.

Speaker 1: 01:08:28

I'm a crazy anti-government person.
I'm all for hardliners.
I'm all for securing Bitcoin against the state.
That's like pretty much what I've devoted my career to at this point.
And I'm just for doing it in a way that's actually effective, which is like, OK, tomorrow the state gets control of all miners and Coinbase and whoever else.
And they and they push out a client that doubles the supply.
What's our actual deterrence?
And that's literally the part of the economy that wants real Bitcoin runs a program that invalidates blocks that are not valid.
That's the deterrence.
Like anything short of that is sort of meaningless.

Speaker 0: 01:09:05

I don't know.
Like, I think it's one of those things where like, I agree with you intellectually.
Right.
But I still like there is sort of like this intuitive part that's not being satisfied.
And I think that like, you know, as most like early Bitcoiners would sort of probably agree is that like, there's a lot on this that we don't still fully understand, especially on the economic side of Bitcoin.
And it's very hard to satisfy that with like, oh, here's a simple solution in code that will do the trick.
And I don't know, maybe it's just, we just haven't explored, you know, this enough in terms of like trying to find a more sane path for activation that sort of satisfy both camps.
Again, Speedy trial feels more like, you know, it's making the devs feel more safe and cozy, but I don't think they have fully satisfied the economic nodes.
And I think it shows.
I mean, like you go ask around, like People don't like it.

Speaker 1: 01:10:18

People don't know what it is.
I mean, people, if you ask your average person on Twitter what speedy trial is like, they won't be able to tell you.
They'll say like, oh, it's a way of quickly activating a soft fork, which is like a very incomplete view of what it actually is.
So I just think like, look, all of Bitcoin's development process is threading this needle where at one end of the spectrum, it's like making changes too easy and, you know, enabling some usurper to come in and screw up Bitcoin.
But the other end of the spectrum, which like we're at a real risk of traveling, is like burning all of your human resources out and making like non-contentious things impossible so that Bitcoin can't actually improve.
And we gotta be diligent of that.

Speaker 0: 01:11:04

I think there's a little bit of nihilism there too, with like the core sort of maintainers.
Like there's a lot of people out there that, you know, are perfectly fine with the state of the software.
And, you know, we could find people that just update the clients for a new Windows version.
You know, like, and I'm just saying like, I, I feel like, you know, as each year, sort of like the balance of that sort of tips to a different side a little bit.
I think like a lot of more sensitive people came on board too.
Like, you know, a lot of the drug dealers went.
And you know, like the true sort of like hardcore people trying to hide from Jio, sort of like, no longer as like out loud, you know, or they started IPOs now.
But the thing is like, I feel like there's more sensitive people who are now part of development.
You know, brilliant minds, great.
Love to have you.
But I think when the rubber meets the road, Bitcoin, a lot of this sort of like, fuck your sentiments stuff comes back.
It's just we're in a little kumbaya time now.
You know, I think if you actually start talking about forks and things like, you know, the conversation sort of reverts to the me.
Go ahead, Brindel.

Speaker 2: 01:12:12

Yeah.
I mean, I kind of think that the, the difference between the activation method that James is, I don't want to say advocating, I don't want to put words in your mouth, but trying to explain, and maybe the sentiment that MVK is explaining is just like lot equals true.
I think that's literally it.
I think The people that I heard, and I don't talk to everybody, but the people that I talked to who were the most annoyed by Speedy Trial, I think the thing that they were annoyed by was that there was this idea that if Speedy Trial failed, then we would go back to the drawing board.
And they thought that that meant that miners were needing to tap in.

Speaker 0: 01:12:57

That's right.
And it does give that impression to the network and to the business people who don't understand the code.

Speaker 2: 01:13:02

Right.
And whether that's true or not, that's the message.
And what lot equals true says is there's a flag day.
And if you're not on board by the flag day, you're going to get forked off the network if we're the economic majority.
And so, like, I wonder if maybe the the the thing here that kind of everybody once is like speedy trial with lot equals

Speaker 0: 01:13:25

true.
That's it.
But that was the ask that everybody who wanted to compromise said I had a lot through my Twitter handle.
So it must count.

Speaker 1: 01:13:33

So I think every there is not a person who is advocating speedy trial, who contradicted the idea that if the speedy trial fails, that we won't come back with the user activated software.
I think everybody who's serious knows that's in our back pocket.
But it's a little bit like speak softly and carry a big stick.
And equally, even if you're running lot equals true before that timeout, you can change your software.
So it's like kind of bullshit.
You know, like lot equals true is like kind of just a it could be a

Speaker 0: 01:14:08

bluff.
But you know, bluffs go a long fucking way, man, between humans.
It is fascinating.
I mean, everything, every aspect of your life is carried on by bluff.
When you cross the street outside of a red light, you're essentially bluffing with your life that the car is gonna probably stop for you.
Like, you know, like it is fascinating how it sets the tone in every human interaction.

Speaker 1: 01:14:35

But Rodolfo, what I'm saying is that threat is always there.
The threat of a UASF is always there.
That's always an option to us.
Nobody is saying that we wouldn't do that.
It's just like-

Speaker 0: 01:14:45

I'm gonna drive James crazy.

Speaker 1: 01:14:47

You're gonna drive me nuts.
Yeah, because like this whole thing is like, so to be clear,

Speaker 0: 01:14:52

like, I have, I don't know.

Speaker 1: 01:14:54

I like, I don't care how activation happens.
It really doesn't matter.
It's solely just like a way of like kind of easing the deployment by not having chain splits.
It can happen any number

Speaker 0: 01:15:07

of ways.
Then why don't we do lot true?

Speaker 2: 01:15:11

I'm going to float a thing.
I think that there might just be a subtle psychological difference between saying, we could always go and implement lot equals true, and actually implementing it and letting users turn it on.
It's this thing where If you're a non-technical, or I don't want to say non-technical, if you're somebody who's not going to go and hack on Bitcoin Core, and you're just an economic actor, you care about Bitcoin, you care about this change.
If you hear, hey, we can always go and implement lot equals true.
There's kind of an implicit like if we decide to do it.
And that's different from you have the code.
Hopefully we won't need to use it.
But like here it

Speaker 0: 01:15:58

is.
Remember,

## Problems with Bitcoin core defaults

Bitcoin core defaults, even if they're soft defaults like that, okay, they rule things for the lazy which is 80% probably of the network.
Right, so if you put law through as default on core, It's very likely that 80% of the people won't change that.
It's the same conversation that we had about RBF.
Okay, these things really matter.
They set the tone.
Most people will follow what comes out default from core.
And if you're serious about that change, making it lot true, it probably puts that weight in.
It means that the majority of the people who work on that code believe that this fork, this update is likely to be the winner of that.

Speaker 2: 01:16:49

But then by that argument, wouldn't you want to actually have lot equals true to be or lot equals false to be the default?
And like what you'd actually want is to say, if the economic majority of the network actually cares about this change, then they need to go into their Bitcoin.com and flip the switch.

Speaker 0: 01:17:04

But this is exactly one of the reasons why I don't like speedy trial.
It's because you get into this game of it depends on which side you like more.
You can make the argument both ways and now you're introducing order, which is gameable, versus the chaos.
Well, the thing

Speaker 2: 01:17:21

that I think that you would want is you'd want the configuration option to be there, but it would be default off.
Like the default is what we have today, but the switch is there.
And if enough people care to flip the switch, then they go flip the switch.
Yeah.

Speaker 1: 01:17:35

Yeah, so here's the problem with lot true by default.
If you ship a binary that has lot true by default and people start to run that, and let's say during the trial, you know, the signaling period, we discover that there's some problem, some bug, right?
All of a sudden now, like the software that isn't supposed to require upgrades, Bitcoin, That's the whole reason we do soft forks is not to force upgrades.
Now, of course, upgrade.
Now you have a forced upgrade where it's like, oh, you got to swap out the binary to make sure that your node doesn't fork itself off the network at this at this drop dead date.
So it's I don't know, man.

Speaker 0: 01:18:16

This is the issue.
Again, it's like,

## The politics of changing Bitcoin

this is the problem.
It's like, I understand and respect the effort that went into developing Speedy Trial.
I really do.
Like, I mean, it's an impossible position to be in, to be a core dev when there is a fork coming, right?
Like, it really is like awful.
And trying to come up with stuff like this is exactly what you should be trying to do.
However, it's just, it just didn't suffice as a solution.
Like it does.
See, if you want to measure if something works or doesn't, you can measure by like, you know, how much you hate you get hate from it when you put it out there.
Right.
I mean, like, speedy trial was like a disaster.
Let's call it in public relations.
You know, people really hated it.
I don't know if it

Speaker 1: 01:19:03

was a disaster.
I like I'm all for arguing.
I love arguing about Bitcoin.
I think people should be engaged with the technical community.
It's like, let's argue about meaningful things like this is not a meaningful thing.
You know,

Speaker 0: 01:19:13

I think it is the most meaningful thing, like like updating Bitcoin and how you update Bitcoin is...
Because remember, right, a lot of bad actors want to change Bitcoin to have, say, 22 million or to have tail emissions or whatever, right?
So like...

Speaker 1: 01:19:28

No, but those are...
Yeah, those are risks.
But like the mitigation to those risks is is responding proactively with like invalidate block scripts.
It's not, you know, we're just not running some shitty software that someone puts out.

Speaker 0: 01:19:40

It's because it's still a game of convincing enough people.
Like, this is the thing that like most Bitcoiners don't want to accept is that Bitcoin is fully political, 100% political.
Everything is politics.
How many people can you convince to go your way?

Speaker 1: 01:19:52

Right.
And that's still in the mix.
It's just the question is whether or not you upgrade your version of Bitcoin Core.
So let's say if the maintainers merge some controversial software tomorrow, the really interesting process is whether or not people upgrade Bitcoin Core.
That's the vote.

Speaker 2: 01:20:12

If the Bitcoin Core maintainers go evil and double the supply or implement tail emissions or whatever, what you would hope would happen is somebody would fork the repo and then go and tell everybody, don't run Bitcoin slash Bitcoin, run Rindol slash Bitcoin instead.
Because It doesn't have the evil patch in it.
And like, you've got to convince enough people that it's in their best interest to like change their back.

Speaker 0: 01:20:38

I mean, the challenge, the challenge is that Bitcoin is fully centralized, right?
Like you have one client.
Right.
Essentially, you have one URL where the client is deployed.

Speaker 2: 01:20:47

It's nuts.

Speaker 0: 01:20:48

It's fully central.

Speaker 1: 01:20:48

And that's a real problem.
It's a real

Speaker 0: 01:20:50

problem.
Super.
Essentially, everybody expects it.
They go to bitcoin.org, they press download, that's what they should be running, and they're saving the world.

Speaker 2: 01:20:57

Right?
Right.

Speaker 0: 01:20:59

And this is why I always go back to Bitcoin defaults are very complicated, right?
Because essentially the people who deploy Bitcoin kind of like run it, you know, they kind of own it in a way.

Speaker 1: 01:21:10

I agree.
I agree.
It's really bad that Bitcoin as an ecosystem implicitly looks to the maintainer merge button as the source of truth about like what to do.
Because I think

Speaker 2: 01:21:23

like the fact is the code, there is no spec.
Like the implementation of Bitcoin Core is the spec.

Speaker 0: 01:21:28

I mean, it's Netscape, guys.
Like it's a hundred percent

Speaker 1: 01:21:32

of the

Speaker 0: 01:21:32

network runs the client, right, runs that specific call.
And this is why, you know, again, when you make things like speedy trial, whatever, you're implicitly sending people in a certain direction.
You really are.
Right.
Like, and it may not be, you, you don't feel that way because you understand that the call doesn't do what I'm saying.
Right.
But like, but that's not what you're endorsing something, you're pushing something.
Right.
So like, this is kind of cool because at the same time, there is no solution possibly.
Like there really is no good solution.
And it's just one of those things that not having a good solution is the firewall.
You know, again, state actors cannot handle that, right?

Speaker 1: 01:22:15

Like- Yeah, so maybe your argument is like, there's not a well-defined process.
And so that makes the whole thing resilient because you can't follow a reliable method to achieve change, which, yeah, there's definitely a point there.

Speaker 0: 01:22:30

You know, democracy was something kind of very useful and very good on the very beginning, right?
I mean, like for you to vote in Greece, you had to own land.

Speaker 1: 01:22:38

Yeah, I wish we would go back to that in America.

Speaker 0: 01:22:40

Because the vote was linked to skin in the game.
If you ruined your shit, you lose your money because land is not portable.

Speaker 1: 01:22:49

Totally.

Speaker 0: 01:22:49

Right.
So like you worked.
And then what happened is through thousands of years, we gamed it.
Right.
And then and then, you know, we gamed gold.
We gamed...
Humans, all they want to do all day is game shit.

Speaker 1: 01:23:03

Right.

Speaker 0: 01:23:03

Right?
Like, it is literally why we're better than other animals, is that we figure out a way of gaming shit, right?
So the more chaos you introduce in that, the less likely you are to be gamed.

Speaker 1: 01:23:15

So yeah, so again, it all goes back to threading that needle between making the process resilient to being gamed, but also like not doing these own goals where like we all agree that we need something and it doesn't happen because the process literally, mechanically can't happen.
So I don't think any of us are saying

## Testing for consensus

it can't happen.

Speaker 2: 01:23:37

Yeah, something that you said earlier that was really interesting, like you made a point earlier that I really agree with, which is if somebody ever like forces through some bad change, Maybe it's like miners collude and turn on drive chains or whatever.
It's going to happen.
I kind of hope so, because I want to test out this next part, which is you can write 30 lines of Python to inspect blocks and invalidate them.
And Jeremy actually wrote a script to invalidate CTV blocks.
He's like, if you hate CTV, here's your user-resisted software code.
It runs as a sidecar

Speaker 0: 01:24:17

next to Bitcoin.
You've got to

Speaker 1: 01:24:17

love Jeremy, man.
He's one of the most honest, hardworking guys in Bitcoin.

Speaker 2: 01:24:23

Yeah, he's like, here's a for loop that kicked you off of the CTV chain if you don't like it.
Maybe if there is no process, the way that you test if there's consensus is you activate a thing and you see if the majority of the network kicks you off.
Right?

Speaker 0: 01:24:40

But is Core going to deploy that?

Speaker 1: 01:24:43

Probably not, because Core is ultra-conservative.

Speaker 0: 01:24:45

No, but see, this is the challenge too.
We always go back to this thing that maybe is unsolvable.

Speaker 2: 01:24:52

Well, but the thing that Core could do is Core could bundle an option or a tool with BitcoinD to let you

Speaker 0: 01:25:00

reject blocks.
It should be like, you can't run core, right?

Speaker 2: 01:25:04

Like it comes with a popup,

Speaker 0: 01:25:07

when you open the software.
And then you

Speaker 2: 01:25:08

pick the button.
And like, if you pick the no button, that it invalidates blocks.
If you pick the yes button, then it accepts blocks.

Speaker 0: 01:25:15

That's right, but you can't have a go back.
Like it's like, you know, it really is like you have to run

Speaker 2: 01:25:21

the previous version of core.
You've got to like IBD again, right?
You've got to like move away your directory and like sync it again or something.

Speaker 0: 01:25:27

That's right.
No, I like that.
I mean, like maybe that's the way it creates the, but see that creates the game of chicken, right?
Like on UI.
Yeah.
How many people check the thing, right?
They'll just press yes.

Speaker 1: 01:25:42

Right, right.

Speaker 0: 01:25:43

So now the discussion is gonna be like, which one is the no, which one is the yes?
Which one is on the left?
Which one is on the right?
I mean,

Speaker 2: 01:25:51

it's kind of funny because we kind of are, yeah, that's true.
People are going to be advocating for the right hand button is the one that I want.

Speaker 0: 01:25:57

That's right.
Right hand is forward, is the future.

Speaker 2: 01:25:59

That's right.
Yeah.
Oh my God.
Well, and then in like the right to left languages, we'll have to flip the buttons.

Speaker 1: 01:26:07

Is this like Tinder consensus where you're swiping right on CTV?

Speaker 0: 01:26:10

Oh

Speaker 2: 01:26:10

my God.
Yeah, that's right.
If you and Gmax both swipe right.

Speaker 0: 01:26:16

And then all the woke people are going to want to make users go through a little questionnaire that like it matches their values, you know, of like which fork they want, you know, like.

Speaker 1: 01:26:27

Do a personality quiz.

Speaker 0: 01:26:28

That's right.
They're going to do a Gender assessment on the fork.
You know what I mean?
It's kind of funny.
It's a little reductionist.
But every single time I have this conversation, we always end up with the same fucking problem, which is nowhere.

Speaker 2: 01:26:48

Well, I think the move is that, in my opinion, I don't think anybody in core wants to be setting policy.
I don't think they want to be that guy.
I think what we should be doing is it should be very, very easy.
At the level of you launch Bitcoin QT and it gives you two buttons and the user gets to pick.
Because I think a lot of core developers feel this real pressure of, people want new features, they want new things, but they don't want to be the person who decides.
And maybe the way to relieve that pressure is to just like make the levers really, really easy and put them in front of users and then let people figure out their own politics and figure out how to convince users to click the right button.

Speaker 0: 01:27:34

I don't know.

Speaker 2: 01:27:36

Or we go back to flag days, like I'm a big flag day maximalist.

Speaker 0: 01:27:40

Yeah, flag days are great.
Yeah.
Just just have a fucking flag day.
It's the closest thing that we have.

Speaker 1: 01:27:46

Yeah, Flag Day wouldn't be bad, I guess.

Speaker 2: 01:27:48

Yeah, if we just say like, this is the date and CTV is turning on.

Speaker 1: 01:27:51

Right.

Speaker 0: 01:27:52

If you care enough, show up.

Speaker 2: 01:27:54

Yeah.
Maybe Flag Day.
Here's Bernie lines of Python.

Speaker 0: 01:27:58

Yeah.
It's very cyber-able too.
That's the problem, right?
Like as more state actors come into play and it's tricky.
But, you know, I feel like we also exaggerate this concern at this specific moment in time in Bitcoin.
Like I'm pretty sure that like in this specific time, we can find consensus like everybody within three calls of distance to them.
Like if I call three people right now, and I know they called another three people, I can have very solid confidence, I have no issues or coins at risk.
And again, the skin is in the game.
So like...

## State sabotage

Speaker 1: 01:28:37

Yeah.
Yeah, I think that's such a good point.
And that's what we really should be aware of is that state sabotage is more likely to come in the form of like gumming up the works or like overt state sabotage is gonna come later.
But like, look at the CIA manual for subverting an organization.

Speaker 2: 01:28:54

Bike shedding is thing number one.
Exactly.
You want to break up bureaucracy, just go on bikes, bike shed.

Speaker 0: 01:29:00

Yeah, you want to know who those books are?
Go in the consortium policy or like spec.
The W3C.
Look for the spec people, OK?
And then go look at how many of them used to work in aviation.
The aviation people always.

Speaker 1: 01:29:17

Yeah, totally.

Speaker 0: 01:29:18

Totally.
Sorry, aviation people.

Speaker 1: 01:29:20

So That's why I get a little prickly when talking about some of the activation stuff.
Because to me, it feels like I understand that the process of deployment, it's really, really important.
The process of coming to consensus is super vital.
And that is very important.
But the literal code that does the activation to me is like kind of like, OK, you know, column A, column B.

Speaker 2: 01:29:38

Yeah, I mean, like the amount of bike shedding that's happened on activation is indistinguishable from a state funded attack on Bitcoin consensus.

Speaker 0: 01:29:46

Yes, absolutely.

Speaker 2: 01:29:47

Like they would look the exact same.

Speaker 0: 01:29:48

I mean, look at what they did to PGP for fuck's sake.
I mean, PGP didn't happen because of that.
Right?
Like, I mean, they made sure that the clients didn't have UI.
Like there is a great, great talk by, Yes, BKH on in 2014 or so about Operation Orchestra.
That's what they call it because they're they're playing you like a fucking feudal.
And like, dude, like.

Speaker 2: 01:30:13

Yeah, James, have you seen this talk?

Speaker 1: 01:30:15

Yeah, yeah.
I think maybe on your recommendation, I gave it a watch and it's it's really good.
We should post it to Twitter when we get done with this call.

Speaker 0: 01:30:22

Every Bitcoiner should watch that presentation.
It's like and understand where that blacklist comment, you know, that destroys the whole conversation comes from, you know, or GitHub changing.
Like this is why they woke people so scary, right?
Because, you know, they are essentially, this is a Marxist playbook.
You know, it's how you break things is by destroying language and destroying how things are run by rational, reasonable people.
Totally.
Yeah.
Anyways.

Speaker 1: 01:30:49

So internal suspicion among the community, like may people fight within the community, make doing technical work really, really difficult and slow going.
Like it's just.

Speaker 0: 01:30:58

Secure elements are evil.
So let's not have them.
It's the most absurd shit I've ever heard in my life.

Speaker 2: 01:31:06

My favorite comment from that thing was he was like, you know, every website should have by default a self-signed certificate.
But when you go, there's a scary browser warning that's like, careful, you might be talking to the NSA.

Speaker 1: 01:31:18

That's right.

Speaker 0: 01:31:19

Right?
Yes.
It's genius.
No, but we arrived at that point, right?
Google changed Chrome.
You can no longer have self-signed certificates.
Yeah.
And somehow, Cloudflare is free.
Yeah.
Right?
Just somehow.
They're like, oh, everybody should encrypt except your encryption keys for your sessions are in the NSA servers now.
So like they just make it easier for everybody.

Speaker 1: 01:31:45

It's It's a big black pill if you start to really think about this stuff.

Speaker 0: 01:31:49

But you know, like we it's the incentives.
I mean, you can make it as nefarious or you can make it incentive based.
It doesn't matter.
Right.
We arrive at the same place.

## Moving forward with activation

So, guys, like I don't know, like I feel like If we want this, we're going to have to just lift our hands and start pushing in terms of like, you know, I'm going to be running this, you know, I'm going to be running the CTV USF client.
And because that's the lingo that people understand as well.
Right.
So I'm going to start running and that's it.
Like, you know, and because see, until people are now willing to put their reputations in line, nobody believes this has any chance that that's how it works really.
Right.
I mean, It's just masturbation.

Speaker 2: 01:32:31

I'm also hoping, Taproot, there's still a lot of people who still don't understand what Taproot is.
But Taproot was a very heady, abstract change.
It's going to let us do all these things in the future that are very sophisticated and advanced.
Segwit was also, a lot of people didn't quite understand Segwit and probably still don't.
What I'm hoping is the three changes that James said, CTV, APO, and Vault, I think those are things that more people can wrap their heads around.
And I think that those are things that have more direct applicability to the things that people want to be doing with their Bitcoin today.
Right?
Like CTV and Vault helps you make your coins safer today.
Like if All that you want to do is use Bitcoin as a store of value.
Bitcoin is a better store of value if you can keep it safer.
And then APO helps with lightning, which we're going to need if you eventually ever want to spend your coins.
And so it's much more concrete about why people would want these things and maybe it'll be less contentious.

Speaker 0: 01:33:34

I think the issue here is it feels like an ominous bill kind of thing, right?
Like where you omnibus bill.

Speaker 2: 01:33:40

Stick the pork in.
Yeah.

Speaker 0: 01:33:42

Yeah.
Like now we have three things we're trying to push and people cannot comprehend already each of them.
And now you have to comprehend how they interact with each other and Bitcoin and stuff.
I don't know.
Like, man, I feel like we we got to just just pick essentially like probably CTV, which is the most comprehensive here.
The most that does the most.
And just fucking go with that.
Maybe you attach a few things to the CTV change, but the point is, I want the three personally, but I think it's gonna be very hard to get that through.
So I think if we just pick one thing and go with that and just deal with it.

Speaker 1: 01:34:18

Yeah, the problem is, I mean, that's originally the route that I wanted to go.
And I started to actually prototype what vault wallet code looks like with just CTV.
And I came to the conclusion that, you know, if you're a big company, having CTV would operationally make vaults easier to do, but they were still impractical for like your everyday user.
And that was really the outgrowth of OpVault.
So I mean, there's part of me that...

Speaker 0: 01:34:46

Let business solve the easiness of it.
You know what I mean?
If the choices don't have anything.

Speaker 1: 01:34:52

Yeah.
There's part of me that says like, yeah, sure.
Let's just do a CTV fork and do it and, you know, exercise the software process.
But I don't know, the more that I talk to people, the more they're like, no, we should really just do it with Vault.
And I kind of feel similarly.
And then APO has just been on the docket for so long.
It's such a simple change.
Yeah.

Speaker 0: 01:35:14

What if What if we do this differently?
What if we game the chaos in the chaotic way?
Okay, maybe this is the way to deal with this.
What if we essentially like have enough people going, you know what, fuck it, we're gonna have, you know, a UASF flag day thing, okay?
And in the midst of all that and the fight, somebody goes, you know what, fuck it, I'm going to do speedy trial.
You know what I mean?
And essentially you arrive at what happened last time, right?
Like you, because you can't prevent anybody from doing anything.
That's the beautiful thing of Bitcoin too, right?
Like if the miners want to do speedy trials, they can do speedy trial, right?
Like as long as their dates work with the line up with our UASF date, right?
Like let each sort of balkanized camp go the way that they want to go.
As long as like, you know, everybody's sort of like, as long as their timeframes all sort of like work out, it's fine.
You arrive at the same place, but through chaos.

Speaker 1: 01:36:10

The tricky part there is that then you have to write a bunch of different client code and You know, getting the specifics right on the activation stuff.
You don't remember when Garzik came up with his own Bitcoin Core fork and there was like an off by one and it would have been catastrophic if they had deployed.

Speaker 0: 01:36:26

Yeah, but Garzik caused a lot of catastrophic problems.
We have better people.

Speaker 1: 01:36:31

Yeah, yeah.
Yeah, yeah.
Maybe not the sharpest knife in the drawer, but like, you know, that's not to say that it's that it's it's easy by any means.

Speaker 0: 01:36:40

So it's not going to be easy, right?
Like, but like, I think the way you have to think about this is like battle, right?
Like actual war, right?

## State of development and economic

There is, there is no saints in war.
There is, there is no, there is no people that go, that gets unscathed.
You know, there is no like everybody gets fucked a little bit.
You know, there will be casualties, there will be collateral damage.
But at the end of the day, you know what I mean?
Like you got to move forward into your campaign.
Right.
So. Yeah, I just got to accept, man, that there is Like, you know, you can't please everybody.
You can't you can't like you're going to step on toes.
People are going to get hurt.
People are going to quit.
And that's you know, if you can't get if you can't handle the heat, get off the kitchen.

Speaker 1: 01:37:27

Yeah.
At some point, you're going to have an empty kitchen and nobody's going to want to actually build this thing and secure it from state actors.

Speaker 0: 01:37:34

And- Nah, you can always hire a new line cooks.

Speaker 1: 01:37:37

I say good luck, like good luck, have fun because that's just not how software works.
I'm sorry.

Speaker 0: 01:37:46

No, it's fair.

Speaker 1: 01:37:46

I get your point.
I'm approaching the point where it's like, yeah, I'll work on this stuff, you know, under these conditions for maybe another few years and then I'm done.
And like, you know, look at the people we've lost so far and look at how well we're backfilling the intellectual capital.
It's not going great, guys.

Speaker 0: 01:38:06

I don't know, James.
I'm a lot more optimist on that.
Like, I really am.
Like, I'm a big, big believer in the economic incentive, right?
Like, you know.
For for each type of like very specialized activity, there's always gonna be only a handful of people.
You know, that is true for anything ever in humanity, right?
Like there's only so many genius people at every single topic, right?
And We often create a lot of exceptions and we make it cozy for the people who can do a thing that nobody else can.
But there's a lot of fucking great people out there.
There is a lot of great people out there that will find income.
I mean, like, look what happened, right?
Like there was no money for, for developing, right?
Bitcoin full-time.
There's a lot of people also who are rich as fuck claim to be poor so they don't get killed too in Bitcoin, right?
Like, there is a lot of like noise in that sort of, in how you get your heuristics of the state of core two.
So, but, you know, people are complaining that there is no money, but like all of a sudden now there's three organizations that have enough money to support enough devs to work on Bitcoin.

Speaker 1: 01:39:20

Totally, totally.
And like, you know, there's good money and I can tell you if there wasn't good money in Bitcoin, I probably would not be working on Bitcoin right now.
I'd probably be working on nuclear or uses.

Speaker 2: 01:39:33

Well, I mean, like Bitcoin can't rely on altruism, right?
Like Bitcoin is PVP.
And the only way that Bitcoin works is if it aligns incentives correctly.
And if it doesn't, then Bitcoin deserves to die.
Right.

Speaker 0: 01:39:49

But it does.
Right.
I mean, like, for example, you know, look at some of the clients, like look at Electrum, right?
You know, it goes way back in time.
Somehow a non for profit between quotes project keeps on being maintained.
Why?
Because there is enough OGEs still using that piece of software and is in their interest to, you know, pay people to keep on maintaining it.
The people who get paid to to keep on maintaining it don't talk about how much they make it, if they work for free or not, right.
But like there is enough incentive to maintain everything going, right.
Like you can say like, for example, a place like a Chaincode Labs, right.
Like it's a little bit cozier, it's a little bit more left-leaning kind of organization.
You know, there is some people who have a lot of Bitcoin who maintain that place.
Right.
And then like there is the incentive is, is gonna, is it is for you to maintain your bag safe.
Right.
That means having that was working for it.

Speaker 1: 01:40:42

I think that's the issue though, is that like back, you know, the people who were involved back in 2012, 2013, that era, you can accumulate a much bigger stack based upon the supply characteristics, like the supply curve of Bitcoin.
And like, sorry, that's just not the case now.
Like I know a lot of people

Speaker 0: 01:41:02

who are...
Oh, you still can.
It's just early.
So early.
People said that...

Speaker 1: 01:41:08

Maybe, maybe not.

Speaker 0: 01:41:09

In 2013, no, seriously, in 2013, 2014, everybody was sort of saying, fuck, if you got in Bitcoin, you know, in 2010, in 2011, you know, you could have been made a fortune.
Right?
Like, look at me now.
I can only have so many hundred coins.
I could have thousands.
That's going to be true on every single stage of the Bitcoin versus dollar price cycle.
Right.
That's just the nature of it.
Remember, there's only 22 million, 21 million units, right?

Speaker 2: 01:41:38

That was a Freudian slip.
We know.

Speaker 0: 01:41:41

I've been I've been joking with Pablo and Nostra and I've been tipping him 22 million every single time, like joking that like he got oversupply.
But anyways, so my point is like Bitcoin really is binary.
Like it either goes to zero or it goes to the moon.
I mean, people, they want to don't want to believe that they're probably in the wrong project.

Speaker 1: 01:42:02

I agree with you.
I agree with you.
And I don't think that to the moon case is guaranteed by any means.

Speaker 0: 01:42:08

And now we have full-time money.
Like people used to have to sell drugs to be on Bitcoin.
Now you actually can get a salary.
That's a huge improvement.
That's right.
You know, I'm just saying, like, I feel like we can't fall in this nihilistic sort of like, oh, you know, it's too hard to work on Bitcoin.
It sucks and stuff.

Speaker 1: 01:42:29

And that's not what I'm saying.
And I know I bitch a lot.
And I'm in the midst of one of my bitch sessions here.
Yeah.
No, no, no.
I'm.

Speaker 2: 01:42:36

Nobody's listening.
There's only three of us here.

Speaker 0: 01:42:39

This is the thing, James.
Like, this is the cool thing about this pod.
Like, we can be like extra sort of like, unless they're trying to get us, None of us are going to run for office.
So we don't have to be worried about people clipping the show.
I'm an electable.
And once

Speaker 2: 01:42:51

you get past the 20-minute mark, everybody's tuned out anyway.
So this is just therapy now.

Speaker 0: 01:42:56

That's right.
There's two dudes that keep on going.
I think it's Amith Radheer and some other guy that keep on going all the way to the end.

Speaker 1: 01:43:02

No, no, no, no.
So I look, I fully realized I get emotional about this stuff.
I'm not actually maybe as emotional as I sound, but what I'm trying to do is like raise the alarm that like we don't want to burn our human capital Because I do really care about Bitcoin.
I want Bitcoin to succeed.
Like I want it to continue to improve.
I don't want it to be compromised by the state.
I also want it to be able to scale to the to its potential.
And like just kind of what I'm seeing with my boots on the ground is like this slightly worrying situation where the big parts of Bitcoin are not really progressing.
And the people who are full time working on like Encore are in this sort of like narrower, more technocratic, like, oh, does the mempool work the right way?
It's like, that's important.
But it's maybe, you know, like maybe we also need to think about like how to actually scale Bitcoin, how

Speaker 0: 01:43:51

to secure coins.
I think it's like a little self-selecting too, right?
I mean, like, you know, like again, the drug dealers no longer work on Bitcoin as far as I know.
Right.
So like, it's like, it's like, it's like, you know, it's like, it's like the crowd who run servers and things, you know, like they, they want to look at like graphs and see how much better it is.
You know, once you tweak something, they're not interested as much as in like, you know, like, you know, can I cross a border?
Am I going to go to jail?
Kind of problems, right?

Speaker 1: 01:44:18

Exactly.
Exactly.

Speaker 0: 01:44:19

But then we can also change nothing.

Speaker 1: 01:44:21

That's the problem, is like the core project right now has a very European bureaucratic approach, where it's like, oh, let's just not fuck up.
Like, that's the highest priority.
Let's just absolutely not fuck up, which in a certain way, it should be the attitude, but it's also stifling over time, over a long enough time period if you're not innovating, and Bitcoin still requires innovation in my opinion, then you're going to kill the thing in the cradle.

Speaker 2: 01:44:50

So I would say that maybe another thing that's underneath a lot of this is part of the core value proposition for Bitcoin is that it's money that works no matter what.
If the government is against you, your money still works.
If large companies are against you, it still works.
You just need to get a transaction included and for most of the miners to not try to reorg your block and your money works.
And I think that if you're doing kind of like a risk assessment or like a threat analysis of Bitcoin and you're thinking of like, what are my dependencies in order to have my money work?
There is kind of this implicit thing of like, you know, I'm still depending on a relatively small group of developers for my money to work.
And I think maybe part of the difficulty around activation is that with the activation methods that we've had so far, there's still this sort of implicit, I need to get a small group of devs to do the right thing.
I need to get miners to do the right thing.
That's like an external dependency on my money working.
Maybe the thing that people are trying to articulate is there's some aspirational mode of activation where like there is no single party that I can point to and say, this group has to cooperate.
It's more this like amorphous thing of like, if the economics work out, then the soft fork activates.
And I don't think anybody exactly knows what that is, but I think that's the thing that people are reaching for when they say that they're not happy with what we've done so far.

Speaker 0: 01:46:31

There is something that I think it's an issue, too, is that there is a lot of fucking bitching.
People are not going to like me saying this.
And like, you know, I get a lot of trouble for this, you know, and VK is so insensitive and you know, like this and that.
And, you know, it's not compatible with like a lot of the kids and stuff.
Like, but like, you know, stop fucking bitching, Jesus fucking Christ.
You know, there is money for people that really want it.
Even before these three organizations, They just got to make compromising work for somebody they maybe don't like.
You know, like, and like, I mean, Rindell, you know, like you're an example, right?
Like you have a source of income and, you know, James, you have a source of income, right?
And I have a source of income.
You know, like we all have our own biases, our own incentive set.
And that's what Bitcoin is supposed to be.
Like, you know, I kind of fall a little bit sometimes into like how, like some of the, what I like to call them my favorite Bitcoin Luddites camp, which is like, you know, nobody has a God-given right to have a fucking like, you know, like a donation salary to fucking work full time on Bitcoin Core.
Yeah.
Bitcoin should just work in industry.
It was designed that way for like industry, right?
The people who have most of the economic incentives to do things, to pay somebody to fucking do the things that they want, go pay for a feature.
Remember when Pierre made the website that he can go and yeah.
And you could pay for somebody to do a pull request or pay for somebody to review something.
That's the way it should work.

Speaker 1: 01:48:03

Sadly, that never actually worked because I had a bounty that I wanted to collect on, but it turned out that I guess it was just like people kind of pledging that they might pay you.

Speaker 2: 01:48:14

And like going back to the whole, you know, you can run 40 lines of Python to invalidate blocks.
Like something that I think people forget is you can run whatever software you want.
If you want to run Bitcoin core, do it.
If you don't like Bitcoin core, you can either go to the library and borrow a C++ book and learn how to hack on Bitcoin Core, or you can pay somebody to go do it for you and then you can run that software.
Or you can run different software altogether if you don't like Bitcoin.
But you have agency to run whatever software on your computer you want.

Speaker 0: 01:48:42

Yes.
I think It's too easy to snap into this God-given, and I feel this from a lot of devs in this space.
There is this sort of like, oh my God, I'm so smart.
And oh my God, I have this God-given right to get paid full time to do this because nobody else is going to do it.
Trust me, if there is enough fear of something, there is enough money in Bitcoin that that will find its way.
Sometimes it will be pointed out to somebody that does have the resources to help with something, which is there's nothing wrong with that.
I mean, we're super lucky that it really comes down to mostly Jack right now.
Like three or four organizations have like their largest base from them.
And like he literally makes it so that he has zero strings attached to the to the financial incentives.
And, you know, like he does have this thing where it's like, he's actually funding the competing entities.
And ideally these competing entities should actually fucking disagree.
So like OpenSAT should fund shit that like maybe Spiral doesn't want.
You know, Spiral has like, Spiral is actually part of Block, right?
And they don't fund shit that has licenses that don't match things that Block can use.
Right.
And Jack is very aware of that.
Right.
Like, so I think that like, the beautiful thing of Bitcoin is that it really has spontaneous order vibes to it.
It does tend to sort of go on that trend and somehow things find their way.
Right.
Like we have somehow survived with this thing for fucking 12, 13, 14 years.
I kind of lost count.
And it just fucking works.
So like, you know, people need to embrace the chaos a little bit more, you know, stop being fucking pussies.

Speaker 1: 01:50:26

Yeah.
But on the other hand, from like being from the, if you're, if you're coming at that from like the sort of non-technical outsider perspective of a user of Bitcoin, you can't just say, oh yeah, the magic pixie dust will make technical things happen and it'll all be fine.

Speaker 0: 01:50:40

No, no, it's money.
It's like literal money, right?
I'm advocating for like, it's like literal money and people hiring a dev to go fucking make them a feature or go reveal something they have a concern with.
And listen, big industry does.
There is enough entities out there with enough capital, with enough Bitcoin that they have paid people to go review or request to go review Bitcoin, to go do diligence things.

Speaker 2: 01:51:06

Well, but also if you're an individual user and you don't have the time or the inclination or skills or desire to go work on that, you can also donate and pay developers.
I have zero interest in going and working on Bitcoin Core.
It's just not a thing I want to do.
Gee, I wonder why.
For all of the reasons.
But it's important to me that smart people whose judgment I trust do go and do it.
And so when those people say, Hey, I'm, I'm raising money to support my work on this.
Like I go give them money because like it's an important

Speaker 0: 01:51:42

thing for me.
People don't need a pat on the back.
They need, I

Speaker 2: 01:51:45

also give people pats on the back.
Ginger does it right.

Speaker 0: 01:51:48

Yeah, sure.
And you can give them money and then give them a hug.
I'm a hugger.
I'm a big hugger.

Speaker 2: 01:51:53

Hey, we're two hours into talking about covenants.

Speaker 1: 01:51:58

Yeah, this wound up being a little bit more meandering than I thought, but it's a great discussion because I think this stuff is worth talking about.
I mean, selfishly for me, I'm like cooped up in my house all day.
So it is nice to vent about this a little bit.
And I

Speaker 0: 01:52:11

mean, but that's the conversation.
We're having the conversation that three reasonable people like talking about like the next thing that's going to happen in Bitcoin.
They're going to discuss the thing.
Why the thing?
How does the thing work?
And really, how do we activate it?
And then they end up in all this discussion.
There is no way to avoid this.

Speaker 2: 01:52:30

It's funny.
I feel like this pod has kind of turned into a microcosm of the whole discussion.
Because I think what happened with CTV is most people who looked at CTV technically said, okay, this is really simple, this seems really reasonable.
And then where most of the controversy was, was activation.
I think CTV itself is actually not that controversial of a change.
I think it's all about how do we turn it on.

Speaker 0: 01:52:54

Yeah, I mean, it's always going to be the conversation in Bitcoin.

Speaker 2: 01:52:57

Yeah, never ask a man his salary, a woman her weight, or a Bitcoiner how to activate a soft fork.

## Bitcoin.Review going late night call

Speaker 0: 01:53:06

So, so like, I guess, I guess since we're approaching two hours here, is there anything else like we missed that we should address or do we do we kill at the usual?
Like, I mean, you want to kill a Bitcoin discussion, talk about activation or funding Cordell, right?

Speaker 1: 01:53:21

I wish we could do that 90s late night talk show thing where we have people call in and field questions.
But I guess that's what Twitter spaces is.

Speaker 0: 01:53:30

We should do it.
I always wanted to have a call in live show a lot Frazier.

Speaker 1: 01:53:35

How cool would that be?
Right.

Speaker 0: 01:53:37

You know, let maybe we can pull some people in and all like.
Maybe a little too late.
Johnny's going to kill me if we try to do that now.

Speaker 1: 01:53:46

Oh, yeah.
No, you probably need

Speaker 2: 01:53:47

to like coordinate it at a time so people are ready.

Speaker 0: 01:53:50

Yeah, people are going

Speaker 1: 01:53:51

to have to be a live thing.
Yes.

Speaker 0: 01:53:54

No, it doesn't have to be live live.
We can still edit stuff out, especially if we get some some people who don't necessarily

Speaker 2: 01:53:59

and I said, Please, no.

## Next steps

Speaker 0: 01:54:04

So anyways, guys, I feel like maybe we've murdered the conversation, which is great.
I mean, we all like to talk to each other.
We're eager to just keep on talking.
But I think the topic itself, it's funny, right, Because the arc of this topic is always the same and it ends the same way, right?
So I guess like in the spirit of being productive, right?
Like what's next?
What do we do next?
Like, would we, do I just like go run James CTV client now?
Like what's- No,

Speaker 1: 01:54:41

no, no, I wouldn't tell anybody to run the code that I've come up with.
I think I'm gonna post it.
Right now I'm debating whether to preface it with some kind of a mailing list post explaining my rationale.
Or just put up the code and say, hey, this is one possible avenue that we could go.
And I encourage everybody to look at the code and try and find problems or propose a different approach.
But I do think it's important to start presenting tangible options for people and say, hey, this is one way we could go.
So let's start thinking about the particular direction, because We shouldn't just spin our wheels for another four years.

Speaker 2: 01:55:17

So, you know, CTV and APO are both active on the Inquisition Signet today.
What's in your branch that's different from what's in Inquisition?
Is it basically Inquisition but for mainnet, or is there more?

Speaker 1: 01:55:37

It's Inquisition, but the problem with Inquisition is that AJ, and I understand why he did this, but when he forked Inquisition, he added a bunch of utilities for adding deployments.
And that creates this really frustrating situation where you basically have to have separate patches for Inquisition versus just regular core.
Like they're not compatible really.
They have to be rebased separately and all this stuff.

Speaker 2: 01:56:03

Okay, so this is like porting all of those things into core and doing all the rebases and all that.

Speaker 1: 01:56:08

Yeah, exactly.
So the deployment method is a little bit different in Inquisition, so really this is just me re-bundling everything to have a core compatible

Speaker 0: 01:56:16

deployment.
Very cool.
Okay.
So, okay.
So, so then, so then what's next?
Do we, do we, do we need a volunteer to go and rebase for Inquisition?

Speaker 1: 01:56:30

I don't know.
I'm, I'm still, I think the jury's out for me on like the usefulness of Signet versus just like RegTest.
I know that when I'm trying stuff out, I mean, I came up in the last week with an OpVault demo, which is like, I encourage people to check out as well because that's a really fully fleshed out usage of like kind of what a wallet would look like using OpVault, what the workflow looks like, how to compose all the scripts, you know, what the different pieces of data are.
And for something like that, like the code that I wrote is Cigna compatible, but from, for my own sake, just testing, like I find reg test a lot easier.
I can control when the blocks are lined and all that.

Speaker 0: 01:57:10

Thinking like a politician for a second.
Okay.
What would be the next thing that will cause the next shit disturbance?
So that is useful.
Like not, not bad thing.
I mean like, yeah, destructive shit, disturbance, like they'll get the next wave of opinions and participation and engagement.

Speaker 1: 01:57:28

I guess if I throw up a PR on the core repo because all this stuff has been on Inquisition for a while and it hasn't really spurred

Speaker 0: 01:57:36

anything.
For the people that can't see, Reyndell's eyes just like went fucking full laser.
He blinded us.
That was like your unconscious mind really gave your position away on that one.
It

Speaker 2: 01:57:50

was just absolutely on.

Speaker 0: 01:57:51

You got a terrible poker face.
It was just like, yeah.
You know, like having a little bit of skin in the game, like a PR or something, really sort of a nerf A lot of people who just think this is just theoretical, because I think right now everybody is sort of on this on this mold, mental mold, or it's like, I'm just going to ignore it.
It's just it's

Speaker 2: 01:58:10

not really.

Speaker 1: 01:58:10

Yeah.
Yeah.
Right.

Speaker 0: 01:58:11

And people are not going to put their weight or their thinking or their opinion on something that is positive and negative.
A lot of people are just going to stay out of it until like, you know, maybe it's a PR.

Speaker 1: 01:58:23

Yeah, yeah.
So I'll put the PR up and then I actually should coincide pretty well with our baby coming because I can drop the PR.
Yeah, just fuck it.
Basically walk out.

Speaker 0: 01:58:33

Yeah, totally.

Speaker 1: 01:58:34

And not sleep for a month while I'm

Speaker 0: 01:58:36

taking care of him.
You're screaming a fire in a movie theater, right?
That's what PR on Quora is.

Speaker 2: 01:58:40

And then when you come back, you'll be sleep deprived.
You'll have a complete shift in your-

Speaker 0: 01:58:47

Zero patience with bullshits.
Exactly.
Like, you just won't have fucking time for it.
Like, babies, do newborns, like, dude, like all this polite veneer of James here is gonna just fucking go.
Like, you know, newborns, like, they really focus you.

Speaker 1: 01:59:01

Well, little there was to begin with.

Speaker 2: 01:59:02

A hundred percent.
Like somebody's going to go on that PR and say, won't this allow government whitelisting?
And you'll just like delete that shit and be like, I don't have time for you.
My baby's screaming at me.

Speaker 0: 01:59:12

That's right.

Speaker 2: 01:59:12

Come back when you know

Speaker 0: 01:59:13

how to.
Post pictures of the baby's poo on the PR.

Speaker 1: 01:59:16

Oh, yeah.
Yeah.
If you thought my mood was good now, just wait for another two months.

Speaker 2: 01:59:22

It's going to be great.

Speaker 0: 01:59:23

All right.
So, okay.
So that's going to be very useful because I think that the conversation will shift into, okay, this is the thing that we want to actually activate.

Speaker 1: 01:59:32

And if there are people out there who want just CTV, I think that'll bring them out of the woodwork and say, no, we should just do a software with CTV, or there's a group of people I've been talking to who just want Vault, because you can do that.
It won't be as good as with CTV, but you could just do that.
So.

Speaker 0: 01:59:48

But it creates alliances, right?

Speaker 1: 01:59:50

Yeah.
That's

Speaker 0: 01:59:50

the other good thing, too.
It's like, oh, there's something for me.
There is something for you.
And it's fucking politics, man.

Speaker 1: 01:59:55

Right.

Speaker 0: 01:59:56

You can't get humans out of it.

Speaker 1: 01:59:57

It is.

## Bitcoin politics closing summary

That's what's really ironic to me is like Bitcoin is the most deeply political system that I've ever worked on, compared to all the private companies.
Now it's a much bigger system, but it's surprisingly political.

Speaker 0: 02:00:11

But before politicians became parasites in this fully-gamed systems, I mean, dude, politics is nothing more than trying to sell the thing that you want that may affect other people.
You're right.

Speaker 1: 02:00:21

You're right.

Speaker 0: 02:00:22

But there's nothing wrong with it.
Yeah.
It's just the main, you sell where you want to have for dinner with your wife.
Right?
I mean, you have the political discussion about it.

Speaker 2: 02:00:31

Ultimately, Bitcoin is a tool for, it's a completely voluntary tool for economic coordination.
If you don't want to play the rules, there's 5,000 other clones that have slightly different rules that you can choose.
And so it's going to be political because money is inherently a social network.
It becomes more valuable the more people accept it and will pay you with it.
And so you want more people to play by your rules and you want them to be the rules that you want and not the rules that you don't want.

Speaker 0: 02:01:05

You know, I love that, like, you know, the people try to say, you know, Bitcoin is a political whatever, but like Bitcoin is essentially enforced libertarianism and like people like can't accept that is hilarious.
But like, you know, the absence of the central planning and central controlling is what we are at is political, right?
Like you can't save the children with Bitcoin because nobody's going to print your money.
You're going to have to use yours.
Right.
So like It's literally enforcing a certain political view.

Speaker 1: 02:01:35

Yeah, that men shouldn't have control over the supply of money.

## Closing thoughts

Speaker 0: 02:01:38

Right?
I mean, it's...
Anyways, guys, I think this was a fantastic discussion.
I really did.
We explored this like people who participate in the network would.
I really think that people are going to get something out of this.
I think it will help people sort of like go through the train of thought, agree, disagree with, you know, the stuff that we have to say.
But I don't know, I feel like it was a good arc.
We really sort of covered all the things that need to be covered.
And hopefully people come out with an opinion that's a little bit more informed.
At the end of this, it's supposed to just wishy-washy, which is, I think, where the discussion about Covenants was.
Maybe we get like some good feedback telling us like, hey, you know, like, can you sort of go on this, discuss that or something that we missed or whatever.
But maybe we do a refresher on this discussion like after the PR.
Because the PR is going to be very interesting in the PR comments.
Yeah.
And yeah, so With that, guys, any final thoughts?
Rindell?

Speaker 2: 02:02:50

I don't think so.
I mean, I think, you know, I hope that, you know, whether people like these proposals or don't, I hope that there's higher quality dissent and discussion coming out of it.
I think that what James is going to go do will hopefully be a forcing function for people to get a lot more concrete in their either alternatives or arguments or whatever.
A lot of this shit's been way too hand-wavy for way long.
And so hopefully we got some like real discussion.
I'm stoked, can't fucking wait.

Speaker 0: 02:03:29

Yeah, yeah.
No, it's, I think anybody who works on the ground and is not sort of like, it doesn't have the freedom to go fully galaxy blame on this either, sort of feel the same way.
It's like, okay, I work with self custody.
I understand the shit.
Like I understand I need this shit.
Like it's a very different vibe than even Taproot.
And let's not even get into Schnorr, just no longer Bitcoin, right?
Like it's a whole other conversation.
But like, James, any final thoughts?

Speaker 1: 02:04:01

Yeah, you know, Ryan all nailed it.
But I just wanna say, I understand why we're here and not some place further down the path.
Because, you know, this has been my full time job for the past four years.
And and it's it's even just staying on top of the conversation is a ton of time, requires a ton of technical context.
So I get why we are where we are, but I do think that it's time to start talking more in terms of concretes.
What are we planning on doing?
Evaluating specific sets of codes.
So yeah, I'm definitely looking forward to how this conversation progresses.
And I still, I have opinions, but I don't have a dog in the fight really.
I just wanna see things kind of move forward in a concrete way because ultimately, I want to see Bitcoin realize its potential.
I think now more than ever, having a viable non-state money is absolutely critical.
And we have to make sure that this thing works.
So I always love talking to you two guys and NVK, I love this venue for talking about stuff because we can like shout at each other.
It's always a great conversation and you know, but we always know that that the other guys are, you know, have the best intent.

Speaker 0: 02:05:24

Yeah.
You know, this is this is a safe space for people that don't like safe spaces, you know, like I feel like there's just too much noise.
There's just too much.
People whose intent is to disagree as opposed to just have three dudes having a beer kind of conversation and sort of sorting shit out, right?
Like we don't actually have to agree.
That's what people sort of seem to be missing the point.
It's like, the idea is where do we find a little bit of compromise to keep on moving, right?
And I'm extremely grateful that people like you guys come.
And you guys are people who build incredible things and do incredible work and are wasting two hours of your time just talking to me and maybe two people left listening this long.
But hopefully, hopefully somebody gets some value out of this.
And then when somebody actually like bitches on Twitter about something and say you put a link, go listen to us talking about it in depth, you know, it's very helpful.
It's the shut up link.
I am reaching my point, I think probably because of Nostra, because Nostra is new, so the bitching is young.

Speaker 2: 02:06:38

It's fresh bitching.

Speaker 0: 02:06:39

And I'm no longer young.
So my patience with bitching and people who have opinions and don't build anything is starting to diminish exponentially.
So I need a place, a safe place.

Speaker 2: 02:06:57

Yeah, I mean, it's something where like one of the things that's a little bit contradictory about a lot of social media Bitcoin discussion is I think that this is a community that values sovereignty and self-determination more than most other communities.
But then simultaneously, a lot of people in this community forget that they have agency.
If you don't like the way that things are going, pick up a text editor and a C++ textbook and be the change.
Or pay somebody else to be the change.

Speaker 0: 02:07:29

Learn to code or learn to code.
100%.
And

Speaker 2: 02:07:32

there's nothing wrong with that.
I work on a whole bunch of stuff right now that I thought was missing in the world, so I'm going to go build it.
And Bitcoin's open source, open participation, permissionless system.
You choose your level of involvement.

Speaker 0: 02:07:50

You know, there is this trend I noticed like a while back.
And like I'd say like three years ago or so.
It's like what I call Bitcoin Marxism.
It's like there is a lot of people who don't understand what the fuck is going on.
They have no reasonable skin in the game.
They're not building anything.
It's just literal fucking noise, right?
Like, and that's not useful.
Like it's not useful at their time.
It's not useful for us.
You sound like a credit card on Amazon.
You're just causing more noise.
You're just sibling the conversation.
But we're people don't talk out loud, but we know everybody who builds stuff and talks like it's very obvious to everybody else that you are just noise.
So don't be the noise.
Anyways, with that.
I think this one is Cooked.
It's done.
This was awesome.

Speaker 1: 02:09:02

Ding.

Speaker 0: 02:09:03

Thank you.
Thanks for listening.
For more resources, check the show notes.
We put a lot of effort into them.
And remember, we don't have a crystal ball.
So let us know about your project.
Visit bitcoin.review to find out how to get in touch.
