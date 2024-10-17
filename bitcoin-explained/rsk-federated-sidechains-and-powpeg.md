---
title: RSK, Federated Sidechains And Powpeg
transcript_by: jinformatique via review.btctranscripts.com
media: https://www.youtube.com/watch?v=dricwvjkhV0
date: '2020-12-11'
tags:
  - sidechains
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
episode: 20
summary: In this episode of The Van Wirdum Sjorsnado, hosts Aaron van Wirdum and Sjors Provoost discuss RSK’s shift from a federated sidechain model to the project’s new Powpeg solution. They explain how this works exactly, and discuss some of Powpeg’s security tradeoffs.
aliases:
  - /bitcoin-magazine/bitcoin-explained/rsk-federated-sidechains-and-powpeg
---
Aaron van Wirdum: 00:00:07

Live from Utrecht, this is the Van Wirdum Sjorsnado.
Hello! Sjors, I have another announcement to make.

Sjors Provoost : 00:00:13

Exciting, tell me.

Aaron van Wirdum: 00:00:14

Did you know you can find the Van Wirdum Sjorsnado on its own RSS feed?

Sjors Provoost : 00:00:19

I did, yes.
And this is actually a new recording of that announcement this is not spliced in by the editor.

Aaron van Wirdum: 00:00:25

The thing is the existing Bitcoin magazine RSS feed also has the Van Wirdum Sjorsnado on it but that feed is going to be broken up and all podcasts are going to have their own feed and then there's going to be an other aggregated feed.
But the point is our listeners that are listening to the Bitcoin Magazine main feed and they want to keep listening to us, now they really need to switch to the Van Wirdum Sjorsnado RSS feed or the Van Wirdum Sjorsnado podcast thingy in their app.
Or maybe they can switch to the new aggregated feed when it's there, but it's going to take a month.

Sjors Provoost : 00:01:03

No, you should switch immediately.

Aaron van Wirdum: 00:01:04

Yeah, switch now.
Switch now.

Sjors Provoost : 00:01:06

Cool.
I always listen to dedicated podcast feeds but it's just my own listening habit.

Aaron van Wirdum: 00:01:11

Especially the Van Wirdum Sjorsnado.

Sjors Provoost : 00:01:13

Yes.

Aaron van Wirdum: 00:01:14

Schurz What do you think of Ethereum?

Sjors Provoost : 00:01:16

It exists.

Aaron van Wirdum: 00:01:17

Yes.
What do you think of DeFi?

Sjors Provoost : 00:01:19

I've heard of it.

Aaron van Wirdum: 00:01:20

Wouldn't you love it if you could use DeFi on Bitcoin?
No. No. Good.
That's a great start of this podcast because we're going to explain how to do that.

Sjors Provoost : 00:01:30

Exactly.

Aaron van Wirdum: 00:01:31

Here's the thing, oh wait, have you ever been to the...

Sjors Provoost : 00:01:34

I'm always in favor of explaining how one might do something even if it's not something I want to do.
For example, I can, we can explain how to burn coins, you know, on Bitcoin Chain.
We've done that with Rubin too.
You don't have to do that.

Aaron van Wirdum: 00:01:46

You don't have to actually burn coins.
Well, the other thing I want to ask, have you ever been to the Lab Bitconf?
I think that's what it's called.
The Latin American one?

Sjors Provoost : 00:01:56

No, I heard it's great fun, but unfortunately not.
Yeah,

Aaron van Wirdum: 00:01:59

so this year...

Sjors Provoost : 00:02:00

I've never been in Latin America, period.

Aaron van Wirdum: 00:02:03

I've been in Suriname for a while.

Sjors Provoost : 00:02:05

Unless you count Mexico.

Aaron van Wirdum: 00:02:07

I've been there as well.
Anyway, this is getting off the rails.
Okay, so here's the point.
I'll get to the point, dear listeners.
I'm going to get to the point right now.

Sjors Provoost : 00:02:14

This is actually take four.

Aaron van Wirdum: 00:02:16

RSK, you know about RSK?
Yeah.
Okay so RSK is a Ethereum-like sidechain for Bitcoin and on LaBitConf they announced a new pegging system.
Do you know what pegging means?

Sjors Provoost : 00:02:31

Well, yeah, it means trying to keep the exchange rate the same, right?
Central banks are very good at that.

Aaron van Wirdum: 00:02:37

Apparently it's slang for fornicating, but that's not what we're talking about.
We're talking about a different kind of pegging where you, like Sjors said, you peg coins to other coins.
Okay, so RSK does this.
We're gonna explain how the new pegging, peg in and peg out mechanism works.
Okay, first of all, let's start at the start.
Sjors, RSK is a sidechain.

Sjors Provoost : 00:03:00

What are sidechains?

Aaron van Wirdum: 00:03:02

Great question.
So a sidechain is a blockchain.
It's a separate blockchain from the Bitcoin blockchain but in some way or another you can essentially move bitcoins to the sidechain and then move them back to Bitcoin. Slightly more technical there are different tokens on the sidechain so there is a different blockchain with different tokens but somehow you can always exchange one of the tokens on the other blockchain for a Bitcoin therefore they should be worth the same.
Because if you get one of these other tokens, you can always just get a Bitcoin.
So, you know, they should be valued the same.
And as long as you have a system where you can do that both ways, so you have a Bitcoin and you can exchange it for a token, or you have a token you can exchange for a Bitcoin then that's what we would call a sidechain I think.
There's some discussion about the definition that's my definition of a sidechain I call that a sidechain if it does that.

Sjors Provoost : 00:03:56

I think that's fine I mean others might have you know all sorts of arguments why maybe the thing on the side is not a chain, or maybe the thing on this, or maybe, you know, it because it involves more trust on the other side, it shouldn't really, it's not like the original Satoshi's vision of a sidechain, even though I don't think Satoshi was the one envisioning the sidechain.

Aaron van Wirdum: 00:04:18

No, that was like the original Blockstream vision, I guess.

Sjors Provoost : 00:04:21

Right, I mean, there was an original vision where the sidechain would almost be an equal partner.
And, you know, there are variations on it where the sidechain is less and less that.
I mean, PayPal could be a sidechain too, if they wanted to, right?

Aaron van Wirdum: 00:04:35

Yeah, well, according to my definition, they would definitely need some sort of token that's packed to Bitcoin in one way or another and I think there needs to be something there needs to be a blockchain as well.

Sjors Provoost : 00:04:44

So what I would imagine is PayPal could say well you send us some Bitcoin to this address and now it's on the PayPal sidechain and you can send it between PayPal users and then if you want to redeem it we'll send it back to you and we'll do that according to our database.

Aaron van Wirdum: 00:05:00

Yeah I still think there needs to be something of a blockchain, and then I guess we get into the definition of a blockchain.

Sjors Provoost : 00:05:05

I agree.
I tend to agree, because otherwise, why not just call it the custodial wallet?
Yeah.
So then, are you building...
I think some of the solutions to this problem are...
What's it called?
It's called a Rube Goldberg machine.

Aaron van Wirdum: 00:05:19

Right.

Sjors Provoost : 00:05:20

So it's one of those super complicated machine where you can move all sorts of objects around and they fall and then something rolls and a rabbit comes out of the hole and then all of a sudden, look, it's a sidechain.
So, you know, I'm not saying that RSK is that, but I'm saying that's why you can have very long discussions about whether something is a true sidechain or not.

Aaron van Wirdum: 00:05:39

Yeah, I think it was Jorge Stolfi or however I announce that, who argued that his couch was a sidechain.

Sjors Provoost : 00:05:46

Like I said, you can probably argue anything is anything.

Aaron van Wirdum: 00:05:49

Okay, let's get to RSK.

Sjors Provoost : 00:05:52

The principle here is you put something into RSK, you park some Bitcoin, you're going to explain it.

Aaron van Wirdum: 00:05:57

I'm going to try to explain how RSK works, roughly.
First of all, RSK is a merged mine, merged mine sidechain.
So in RSK's case, that means that, well, I guess, well, there are different ways of doing merge mining, but in RSK's case, I didn't know this, I thought it was kind of interesting.
It's that it works sort of similar as mining, or I should say pools mining, where all miners in the pool, they are sort of trying to find the next block.
And now every block they try is going to be a valid block, but there's sort of a subset of blocks that are kind of almost valid, and then they're still sort of valid within the pool to determine who gets the rewards.
And RSK has sort of a similar thing where not all blocks that are valid for Bitcoin are valid for RSK, but there are like a bunch of sort of blocks that are almost valid for Bitcoin that are still valid for RK.
So it's more…

Sjors Provoost : 00:06:51

based on proof of work, right?

Aaron van Wirdum: 00:06:52

It's based on, it's just Bitcoin miners who are mining this.

Sjors Provoost : 00:06:55

Yeah, because with Bitcoin, indeed, if you're a pool, you produce a proof of work, and in order to get accepted by Bitcoin nodes, the proof of work has to be, for example, 100.
But miners can say, well, as long as you produce 10, then we know that you're actually mining and not cheating.
And so we're going to allocate you 10% of whatever the next block is.

Aaron van Wirdum: 00:07:14

Yeah.
So RSK has sort of a similar thing where they have more blocks than Bitcoin and they sort of use the same trick.

Sjors Provoost : 00:07:22

But they're actually mining blocks in between then as well.
Okay, so that's different.
Yeah, there are some proposals for Bitcoin too to do that where you would have intermediate blocks.

Aaron van Wirdum: 00:07:32

Yeah, so RSK has that.
So they have a block like Ethereum every 15 seconds or something like that and this is how they do it.
So these miners are just Bitcoin miners and they are producing valid RRSK blocks and these include transactions and they're doing whatever miners are doing and they're doing whatever miners are doing, and they're doing whatever miners are doing on Ethereum, apparently.
But they're producing blocks anyways.

Sjors Provoost : 00:07:53

And they're referencing these blocks in the Bitcoin blockchain, right?

Aaron van Wirdum: 00:07:58

Yes, every time a Bitcoin block is mined, it also has, it's also an RSK block, so yes.

Sjors Provoost : 00:08:03

But not every Bitcoin block.

Aaron van Wirdum: 00:08:06

No, every Bitcoin block.

Sjors Provoost : 00:08:07

I mean, not every RSK block is referenced in a Bitcoin block.

Aaron van Wirdum: 00:08:11

Correct.

Sjors Provoost : 00:08:11

Because there would be gaps.

Aaron van Wirdum: 00:08:12

Yes.

Sjors Provoost : 00:08:13

But that's fine.

Aaron van Wirdum: 00:08:14

Yeah.
Okay, is that part sort of clear?

Sjors Provoost : 00:08:17

Yeah, it is.
And if people want to learn more about merge mining in general, I think they should also listen to our episode with Ruben, where we kind of talk about another way to do this merge mining that does not need the help of Bitcoin miners.

Aaron van Wirdum: 00:08:28

Exactly.
Okay.
So this is part one.
Okay, then we get to how do you actually get Bitcoin onto RSK?
And after that, how do you get RSK coin back to Bitcoin?
By the way, RSK coin is called Bitcoin on RSK or RBTC.
RBTC is not a subreddit

Sjors Provoost : 00:08:50

it’s so much censorship.

Aaron van Wirdum: 00:08:51

Yes, they picked the same name for their coin, RBTC.
But in this context of today's podcast, that means this token.
Okay, now we want to send Bitcoin to RSK.
So okay, so this is what we're doing right now.
And then we'll get to the new change.
Right now you send a Bitcoin to a multi-sig address.
And this multi-sig is controlled by a group of Bitcoin companies or cryptocurrency companies.
Once the coins are sent to the multisig, these companies control it by majority.
They control the coins.
There's a smart contract on the RSK chain that keeps an eye on this multisig.
And once coins are sent to the multisig, the smart contract on the RSK chain knows, okay, time to issue that amount of new coins.
And they are issued to the person that sent the money, the Bitcoin to the multisig.
And then they have RSK coins from that point on.
Yeah.
That part is pretty clear, right?

Sjors Provoost : 00:09:51

Yeah, and I think we also talked about that with Ruben, right?
You can do that and on the Bitcoin side it just looks like money going into a multisig and nobody cares.
That's fine.
Yeah.
The question is how to get it out.

Aaron van Wirdum: 00:10:02

Yeah.
Okay.
So how to get it out.
Right now, the way to get it out is you send, while these coins, while the RBTC are on RSK, the coins in the multisig cannot move or shouldn't move.
You know, the companies that are controlling this multisig should not move the coins until the RBTC are sent back to the smart contracts.
And at this point, these companies know, okay. Now these coins are locked in the smart contracts.
Now we're going to release them from the multisig.
So then they're sent back to whoever wants the coins on Bitcoin's main chain.

Sjors Provoost : 00:10:41

Right.
So it's kind of similar to like they would get burned and created out of thin air.
Just a slightly different.

Aaron van Wirdum: 00:10:46

Yeah.
It's a slightly different way of doing it, slightly different terms, but it's sort of the same.

Sjors Provoost : 00:10:51

And so the key is that it has to stay in balance, because you do not want a situation where, you know, less RSK, where there is more RSK than the amount of Bitcoin in a multi-sig contract, because then you get a game of musical chairs.
So how do we prevent, or how do they prevent the game of musical chairs?
Because the Bitcoin side doesn't care, right?
When the multi-sig address is empty, Bitcoin just keeps going.
But some people may be very upset.

Aaron van Wirdum: 00:11:14

So right now there's no real way of preventing that.
It's trusting that these companies aren't going to cheat on the RSK users.
That's how it currently works.
You just got to trust that they're not going to collude against you, essentially.

Sjors Provoost : 00:11:28

And I think it's also that there has to be a threshold, right?
Because it's a multi-sig that has a certain threshold.

Aaron van Wirdum: 00:11:33

Yeah, it's a majority.

Sjors Provoost : 00:11:34

Right, so you want to make sure that the majority doesn't collude against you.

Aaron van Wirdum: 00:11:38

Yes, exactly, right.

Sjors Provoost : 00:11:40

Or is forced to, or is hacked.

Aaron van Wirdum: 00:11:42

Yeah, also possible.
But you know, and the theory is, like these are sort of well-known companies so you can probably trust that they're not all going to collude against you hopefully.

Sjors Provoost : 00:11:54

Yes, but you understand why I might make an analogy with a custodial wallet?

Aaron van Wirdum: 00:11:59

For sure yes I get why it's not ideal.

Sjors Provoost : 00:12:02

Not a legal analogy, but a physical analogy.

Aaron van Wirdum: 00:12:05

Yeah, okay, but RSK is upgrading.
So now they're going for a new solution.
The new solution is this.
The pegging in part is still the same.
You still send coins to a multi-sig address and the smart contract issued. Now you're sending back coins to the smart contract, well the pegging in part is not exactly the same either but here's the here's the change. All of these companies that are controlling the multisig, from now on they are using special hardware modules that have private keys embedded in them.
And these companies shouldn't even themselves be able to extract these private keys.
Okay, these modules, they are programmed in a certain way.
Namely they are programmed to only ever release coins from the Multisig, still by majority, but only do it if the coins are sent to that smart contract.
That's the only way they could possibly send the coins from the multi-key, if they are in fact sent to the smart contract.
And they have 4000 RSK block confirmations, which is equivalent to I think 200 Bitcoin blocks.

Sjors Provoost : 00:13:20

Okay.

Aaron van Wirdum: 00:13:21

So, now you're not just trusting these companies not to collude against you.
You are trusting the hardware modules, I would argue.
And then also these miners, if you are trusting the modules, then there are actually blocks being mined that are actually confirming that the coins have been locked back into into the smart contract which requires energy and you know hash power so it's not something they can do for free.
There needs to be actual energy expenses.
Plus, if someone would try to cheat on you somehow, it would be obvious because everyone can see what's happening on the blockchain.
Does that make sense?

Sjors Provoost : 00:14:05

Yes, I mean, you know, hardware modules are pretty cool, but they are not infallible.
So I very briefly read on their own blog post, they were talking about the problems with the Intel SGX system, which was a sort of a secure hardware module inside the Intel chips.
And there have been lots of scandals.
But in 2015, Intel was saying, oh my God, we have this amazing secure enclave thing where, you know, you can put trusted code and the whole world can trust it and there were proposals to put Bitcoin private keys inside of those hardware modules and basically you wouldn't need Lightning anymore and it was just going to be amazing.

Aaron van Wirdum: 00:14:45

That's T-Chain, you're referencing T-Chain.

Sjors Provoost : 00:14:47

Yes, I'm referencing T-Chain.
And it was already at that point clear, there were books written about that Intel module.
People spent, I don't know, some PhDs spent lots of time reverse engineering how the Intel stuff works in the inside, because it wasn't very well documented.
And basically the introduction said something along the lines of like no self-respecting, security conscious engineer should ever use this.
And then a couple of years later, there are all sorts of massive vulnerabilities with it.
The risk with these systems in general, I think, is that they can have serious bugs in them or backdoors.
Now, in this case, the RSK team, we're not using that particular system.
I don't know what they are using.
I mean, there are devices out there, right, like hardware wallets, the Ledger wallet that has one of those modules in it, the cold card too.
It's a very cool concept.
In principle, the chips are designed in a way that you need very sophisticated equipment to get into them.
And as long as you really can't get into them, they can hold on to a secret for you.
That's why they're great for hardware wallets because they can hold on to a secret but they can do more.
They can be given instructions, you can give them a piece of code and saying the only way you're gonna sign this thing is if these conditions are met and then you can never change the conditions again in theory unless you have, well here's where all the gachas come in, right?
Unless you have an upgrade mechanism where some arbitrary person can sign a software upgrade.
Oh, but the firmware upgrade, okay, who can sign the firmware upgrade?
Okay, now that's the guy the government goes after.
So there is the Gadget Gacha.
There could be a backdoor in it.
There was the, I think, the Crypto company in Switzerland that was backdoored by the NSA and they were happily eavesdropping on their own allies.
Right.
For a very, very long time because there were just a couple of engineers that they were corrupt enough or patriotic enough, I don't know, depends on your perspective, to cooperate with that.
So there's that risk.

Aaron van Wirdum: 00:16:43

So you're making it sound like a bad idea.
Is that your intention or how do you...

Sjors Provoost : 00:16:48

No, no, I mean you could argue that it's a strict improvement over just trusting the companies.
You could say, well, you're already trusting the companies, now at least the companies have to put in significantly more effort to run off with the coins.
So I'd say that's good as long as you're honest about how you present it.
The other problem would be a denial of service.
Okay, so if I am a government and I don't like this project, I walk into these companies, I tell them to turn off the machines or I shoot the machines physically.
Now the private keys are physically gone.
Does that mean the coins are really gone?
Or is there some backup system that now becomes alive?
I think there was something like that with Liquid.

Aaron van Wirdum: 00:17:26

Yeah, Liquid has some sort of backup.
Yeah.
And I didn't read that for RSK.

Sjors Provoost : 00:17:31

Yeah, but then you can choose to make that backup happen and then go after the backup.
And of course, RSK itself, as far as I know, I could be wrong here, relies on node software that honors certain private keys and certain behavior.
So you could issue a hard fork, but then of course it depends on how many people run their own node and whether they'd go along with that.
Yeah.
Similar discussion is with Bitcoin.
I don't know how the incentives are in that system, so I don't want to comment on that.
So there are all sorts of risks, but I think it's reasonable to argue that it's better to have the modules than not to have them.
Maybe.
Maybe not, because that backdoor could actually be worse than not having the modules.
And just using the old laptop, as someone likes to say.

Aaron van Wirdum: 00:18:20

In either case, I mean, RSK is a work in progress.
They would still like it to become a drivechain.

Sjors Provoost : 00:18:27

Yeah, so that's an interesting topic that we should dedicate a podcast to.

Aaron van Wirdum: 00:18:31

Yeah, we'll discuss drivechain in an episode one time but the essence in one sentence is that in that case it would, well can I summarize it in one sentence, it would just be hash power that controls the pegs, pegging in and pegging out?

Sjors Provoost : 00:18:46

Drivechain is not the end-all be-all either.
There are still sort of caveats.
I think we should discuss that in another podcast.

Aaron van Wirdum: 00:18:53

That's for another episode, yes.

Sjors Provoost : 00:18:54

But it is, it could be arguably maybe a nicer solution than hardware modules, because you're really moving away from these companies completely.
You're saying we're going to just integrate this with the Bitcoin protocol in general.
Now we have all these Bitcoin miners that you don't have to trust.
That's the idea, but that might not be possible either, but we'll find out.

Aaron van Wirdum: 00:19:12

Yeah.
Then again, I mean, at this point, you kind of...
Well, is that right?

Aaron van Wirdum: 00:19:18

There's sort of different levels of trust, like you're sort of trusting the hardware, but then, like the miners can't cheat on their own and the hardware, well, the hardware can cheat on its own, I guess.

Sjors Provoost : 00:19:30

Well, I guess if they want to move to drivechains they'd move away from the hardware.

Aaron van Wirdum: 00:19:33

Sure.
Sure.
I know I'm saying right now

Sjors Provoost : 00:19:35

there are all sorts of different security trade-offs that you can make. I think the most important thing is to be honest about them. But what I was asking is how are they going to make money because it sounds like if you peg a currency, you can't pump it.
So is there a premined or are they like honest people?

Aaron van Wirdum: 00:19:49

The company?
Yeah.
IOV labs?
I don't know.

Sjors Provoost : 00:19:53

Okay, because one of the things of course that is nice about currencies that are pegged to Bitcoin is you can say well there's no speculative value in the exchange rate so you can focus a little bit more on the merits of the project itself.
That was one of the ideals behind a sidechain.
And the other might be to sort of try and piggyback on the proof of work security of Bitcoin somehow.
Well, that turns out to be complicated.

Aaron van Wirdum: 00:20:15

Yeah.
Well, one of the nice things about a sidechain like this, arguably, is that it allows Bitcoin miners to earn more fees, which improves Bitcoin security, even for those of us that aren't using the sidechain.
I guess the counter argument would be that running a mining pool or being a miner profitably would come with a little bit more overheads because you could be outcompeted.

Sjors Provoost : 00:20:40

Yeah so there could be a centralization problem there if the miners have to run all these sidechains in order to still have a good margin.
Now one of the sidechains turns out to be Ethereum 2.0 and like you have to process terabytes of data and you have to do it in a big data center.
You can't do it hidden away behind a Tor connection.
That could actually be bad, right?
Another problem, I forgot what the other problem is.

Aaron van Wirdum: 00:21:03

In general.

Sjors Provoost : 00:21:04

Yeah, yeah.
Another problem is if there is more value in one of these sidechains or smart contacts or whatever it is, if say the entire, let's say the gold bugs say, hey, you know what, we kind of like this blockchain technology.
We're going to put the entire ownership record of gold on the planet on the blockchain and protect it with Bitcoin's proof of work.
Well now you have a tiny thing, Bitcoin, protecting a very large thing.
Because probably most of the, I don't know, but my guess is there's more custodial gold out there than Bitcoin.

Aaron van Wirdum: 00:21:36

Is that bad?

Sjors Provoost : 00:21:37

If all the custodial gold in the world is backed by a sidechain on Bitcoin, then creating a re-org on the physical gold chain could be worth a very, very expensive 51% attack on the Bitcoin chain.
You don't care about the Bitcoin chain, you care about the gold sidechain.
So yeah, that would be very bad.
That would be like being the minority hash power.
Maybe not that bad because I'm guessing if you do this custodial gold sidechain, there's going to be some boss, because you're still protecting a physical asset so you could just ignore shenanigans on the chain and that might not be worth it because of something I would like to call proof of prison but

Aaron van Wirdum: 00:22:16

Do you think something like our sk could obliterate Ethereum. That wasn't the word I was looking for.
Replace Ethereum?

Sjors Provoost : 00:22:23

Does it pump?

Aaron van Wirdum: 00:22:25

It doesn't pump.

Sjors Provoost : 00:22:26

And how is it going to replace Ethereum?

Aaron van Wirdum: 00:22:27

I agree.
That's probably the main use case for Ethereum and it doesn't have that.

Sjors Provoost : 00:22:32

I don't want to say that.

Aaron van Wirdum: 00:22:34

But there are.

Sjors Provoost : 00:22:34

If it doesn't pump it's not going to replace a thing that at least has pumping as a feature.
Yeah.
Ethereum may have other features and maybe it can compete on that one.

Aaron van Wirdum: 00:22:42

Yes.

Sjors Provoost : 00:22:42

But so do spreadsheets.

Aaron van Wirdum: 00:22:44

Yes.

Sjors Provoost : 00:22:44

I don't know.

Aaron van Wirdum: 00:22:46

I don't know either.
I don't know.
I think if something like Ethereum needs to exist I prefer to see it as a Bitcoin sidechain.

Sjors Provoost : 00:22:53

That's not how the world works.
The world doesn't say something needs to exist and therefore we get to decide what it is.

Aaron van Wirdum: 00:22:59

The world doesn't form around me?
No. Well damn.

Sjors Provoost : 00:23:03

All right anything else?

Aaron van Wirdum: 00:23:05

No I think that was the podcast.

Sjors Provoost : 00:23:06

Okay thank you for listening to the Van Wirdam Sjorsnado.
There you go.
