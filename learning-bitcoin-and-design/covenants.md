---
title: Covenants
transcript_by: varmur via review.btctranscripts.com
media: https://www.youtube.com/watch?v=rCQKqe2XCqI
tags:
  - covenants
  - ux
  - op-checktemplateverify
speakers:
  - Christoph Ono
  - Michael Haase
  - Owen Kemeys
  - Yashraj
  - Mogashni
date: 2024-01-19
aliases:
  - /bitcoin-design/learning-bitcoin-and-design/covenants/
---
## Introductions

Christoph Ono: 00:00:01

Welcome to our first Learning Bitcoin and Design call of 2024.
We haven't had one of these in a while, but we're picking them back up again.
The first topic is a really tough one, I think at least, it's covenants.
The reason, one of the reasons why this came up is because on Bitcoin Design, we have this new design challenge.
We have a page with design challenges that are meant to be kind of take home challenges.
If you want to challenge yourself to assign something, there's something you can do, and Dan added covenants, for scale, because someone tweeted about it - someone called Leishman, who is CEO of some Bitcoin company that I just forgot.

Yashraj: 00:01:00

River, I think River.

Christoph Ono: 00:01:01

River?
Okay, cool.
And that post said, hey, we really need people to dig into this covenant stuff from a design perspective.
So that kind of kicked that off a little bit, and then we decided to create this learning call.

I don't know how about how everyone else is on this topic.
Until a month ago or so, I basically heard about that it exists, and that there were a bunch of technical proposals called CTV, that basically make no sense if you hear them and you're not familiar with anything.
The term "covenant" didn't really tell us anything.
I put Alien Covenant in the background because literally that's the only time in my life that I've ever heard the term covenant.
Couldn't even figure out what that's supposed to do.
I did listen to some podcasts recently, by Stephan Livera, that were extremely helpful and have this great overview, and I don't think it's actually that difficult after listening to those podcasts.
We're here on this call now that we can kind of shed some light on this stuff, and then hopefully we can work towards some of these design explorations and figure out how this technical mumbo jumbo can actually make Bitcoin more useful, for more people.
And maybe address scaling.
I don't know, what is everyone else bringing into this conversation here?

Michael Hasse: 00:02:30

I came across covenants relatively early, during or after my grant started.
It can help to improve the programmability of Bitcoin, of wallets, of transactions.
In terms of, let's say, automated inheritance or vaulting features that might be helpful.
I focus more on Miniscript, which is something that exists today and can do something limited, something similar.
Covenants are like that on steroids, so you can do much more advanced stuff with it.
But I didn't know about the scaling Enigma thing at the time.
Just read that this week.

Yashraj: 00:03:42

Yeah.
Hey everyone.
Nice to see you guys.
My journey on this one has been pretty similar to Christoph's. There are so many abbreviations, so much arcane stuff, it seems so difficult to understand, APO, CTV, CSFS.
The abbreviations go longer and longer - "What's happening?"
I think it's all very technical, it looks there is a class of people, mostly devs, who are interested in the digital money programmability side of Bitcoin.
They want to make it more technically useful, and you should be able to do different things, and all of that.
As Michael was saying about it, spending it in different ways and things like that.
A lot of the motivation of covenants, so I think the original use case was vaults so being able to specify different types of conditions that UTXOs can be spent, and all of that stuff.
This thing was pretty old.
This is from three, four years back, but in the last few months, it has picked up steam again with so many devs coming in.
My perspective on this is this is too technical and I love understanding all this stuff, but as a designer, I'm trying to think what are the use cases, what are the features that will help people.
Not thinking from the programmability point of view, but scaling and privacy and those things, I think that is something that we require nowadays, in 2023, 2024, and I'm excited to see how it can help.

Christoph Ono: 00:06:04

I think it would be helpful if we take a step all the way back, because like you said, there's this programmability stuff and the dev conversations.
These all seem to be pretty much already sold in, they're not even talking about what this thing is for, they're just talking about how it can work.
I'm really glad Owen is here and also raising his hand, because I think just earlier I came across his two threads here, which I think you posted on GitHub or somewhere.
Those are really good explanations of what this stuff actually does.
So you just raised your hand, Owen, go ahead.

## Covenants overview

Owen Kemeys: 00:06:43

Hi, I was asked to join this call.
I haven't joined a Bitcoin design call before, but it's good to get involved.
As you can see with those threads ([1](https://x.com/OwenKemeys/status/1741575353716326835), [2](https://x.com/OwenKemeys/status/1744181234417140076)), I put a lot of thought recently into trying to visualize how this stuff works, because it's very difficult for people to wrap their heads around how these functions work and what you can go on to do with them.
It's not actually that alien or strange, it's just different to how we do things today.
I started off with CTV because it's the most simple and sort of easy to rationalize about how it works and what you can do with it.
Other forms of covenant are more flexible versions of that, that I think might be wise to put to one side for the purposes of designing stuff, for now.

The way you can think of CTV is it's quite similar to PSBT, to having a pre-signed transaction where I could technically pay you by signing a transaction to spend my coins to your address and then just giving it to you, rather than broadcasting it to the blockchain.
However, you still have to trust that I'm not going to spend those coins differently first before you get it, so you can't consider that PSBT a payment, right?
Because I could spend them any other way before you broadcast it and they're not your coins anymore.
So today we're using only the chain itself to log ownership changes, and what covenants allow us to do are ownership changes off-chain, as long as you can plan them in advance.
There's a couple of use cases in those threads I gave, if you haven't read them already, I highly recommend starting there.

In the second thread, I got onto the actual use cases, and the more I've looked at this stuff, the more I've realized there's kind of two basic principles that covenants are useful for here, you end up with these kind of meta primitives.
Technically speaking, it's what I said a minute ago about having a pre-signed transaction that I can't spend differently, so you can consider yourself paid as soon as you have it.
The use cases tend to be vault type structures, which are kind of using the chain to trigger a time lock, because in Bitcoin's technical design at the moment, we don't have ways where a key expires in a multi-sig or something.
You can only make it more easy to spend, you can't make it less easy to spend.
So vault type structures allow you to trigger the start of the time lock, which is very useful.
Then the other one, which is where everyone's brain starts to melt, are tree type structures, which you could think of as aggregating lots of transactions together, or like a zip file of lots of transactions that only represent on-chain as one.
It is difficult to think about this stuff, but these are the areas, particularly the tree stuff - that's where we can start doing scaling.
That's what I think Alex was asking people to start thinking about the UX for, because it's just very different to how we do Bitcoin today.
But I don't think it's impossible.
I started to think about this stuff before I even got invited to this meeting, and I have some ideas already, but I haven't had a chance to start working on them yet.
Maybe I'll stop talking for a minute and let someone else speak.

Christoph Ono: 00:09:54

Awesome, thanks.

Yashraj: 00:09:57

Sorry Christoph, I just wanted to say thanks to Owen for joining in.
Those two Twitter threads are super duper useful.
I am happy that I've gone through at least the first one a couple of times and I'm still not completely there.
I think I have to read it again and try to do more research, but it was super, super, duper useful, man.
Thanks for joining.
I mean, I love that.
Thanks.

Owen Kemeys: 00:10:25

Yeah, no problem, and it felt like an area I could add some value to the conversation, because I recognized there was a lot of technical people that got how it worked, and a lot of normal people like us who just can't understand how this stuff is useful at all yet.
I spent the last six months or so, just gradually learning and learning about use cases and things, so I could start visualizing how you can actually use this and explain it to people or we're never going to get anywhere with it.

Christoph Ono: 00:10:50

In the Bitcoin Design guide, we have a whole section called "how it works", and it's very similar to what you put together there.
It's private key management, like here's a whole thing about how multi-key systems work.
Some of them have illustrations similar to yours, others don't.
Here's one about custom spending conditions with recovery paths, but it's the same idea what you did, just take these kind of complex things and translate them in our case for designers within the idea that they can take that and build products on top of them.
So maybe we could turn this into a "how it works" page too.
Twitter threads kind of get forgotten at some point, if you'd be open to that.

Owen Kemeys: 00:11:40

Yeah, sure.
Take whatever you think is useful from it.
I'm happy to comment if you want as well.

Christoph Ono: 00:11:47

Awesome.
I wanted to take one step further back.
As I said earlier, I didn't figure out what the word covenant means, but it's basically a promise to engage in some type of activity.
I found that helpful in the Stephan Livera podcast, with Brandon Black I think, where they said in Bitcoin every coin has a restriction on how it can be spent.
But right now, it's basically you need to have the private key, right?
There's one rule how you can spend it.
It's the private key.
If you have that, you can spend it, right?
That's the default that everyone knows.
The second one that Michael has been looking into a lot is the time locks.
You can spend it after a certain amount of time if you have a key.
In covenants, the idea there is to just really open that door much, much further, that you can have all kinds of complex predefined rules about how this can be spent by multiple people with different scenarios.
I found that a pretty good starting point.
Then the other thing I learned that was interesting is that CTV and all of these abbreviations and all this stuff, they're all trying to do the same thing technically.
They take different approaches that end up with some that are a little bit more complex, some a little bit easier, some of them have a little bit more flexibility, others are a little bit more rigid, but they're all kind of trying to do the same thing.
Then as you dig through those, you probably end up with different use cases.
One thing I found interesting, too, because the more complex proposals, they enable more, but they are more risky in terms of things that can go wrong, unforeseen circumstances and all of that.
So there seems to be more a tendency to get the simpler ones enabled.
So there were some takeaways that I found interesting that I wanted to add as well.

Owen Kemeys: 00:13:53

Yeah, I think that's a fair characterization and the simplicity - this is why I started with CTV because it's the easiest to think about, and it's the most tightly constrained, but it still unlocks a huge possibility space of interesting things we can do.
I use the word constructs because just a CTV by itself isn't that interesting, but the stuff it allows you to do is more.
Then a lot of the developers I speak to are thinking, okay, we'll start with this, we can build a ton of useful stuff already, and then as we learn more familiarity with how to use these covenant type structures and so on, we can start to realize where we need a little bit more power and a little bit more flexibility and maybe add those in later on with another fork down the road.
But lots of people are very wary about opening Pandora's box and doing something really complicated on day one.
I mean, none of this stuff is going to break Bitcoin, but some of the stuff is just too complex to rationalize about what its limitations are, whereas CTV is quite tightly scoped and also very well studied.
It's been around many years now at this point.

Christoph Ono: 00:14:56

So a question there around the two use cases that you found.
So the multi-sig vault, I find that pretty easy and that seems like it's a user-facing thing.
You can just say, these coins here, they can be spent, but there is a delay, before they can be spent.
So if someone else tries to spend them, then they either can't do it or they have to wait, so I'm going to notice it.
I'm going to get them into safety because everyone else has to wait.
That's kind of user facing use case that is easy to understand.
Then the scaling thing, that almost seems like it's something that users might never even see that could potentially be happening behind the scenes, right?

Owen Kemeys: 00:15:42

Yeah, so this is where it starts to get complicated.
And I think it might be useful to think of it from the two different directions.
On the one hand, users might build these trees themselves.
That's if you've got a number of payments you want to make to several different people for different reasons, but maybe not all of them right now, but you know I'm gonna pay rent next month and the month after and the month after.
So maybe next time I get my salary arrive, I could construct a tree myself, and that turns into just a regular receive address that I could give to the payroll company.
They pay to that address, and I know I've got my rent payments for the next six months kind of locked into the chain ready to go.
I don't need to make another on-chain transaction just by giving them that one address.
So that's an example of a user wanting to construct a tree, and I can kind of picture in my head what a UX for that might roughly look like.
I don't think it's that difficult, that's somewhat interesting.
But the interesting ones are where the tree structure is built by someone else, and it allows you to be paid inside that tree.
That's the really tricky one and that's where work needs to be applied.

Christoph Ono: 00:16:50

Gotcha.
Right now, if I want to do six months of rent payments, I can make six different transactions and batch them.
With this CTV, then I could basically bundle them all, compress them into like a single address or so, and then they would automatically be executed as time goes by.

Owen Kemeys: 00:17:13

That's one way of doing it.
It's more... you see this stuff is difficult to explain, even having written the thread about it.
Yeah, you can think of it as a compression thing.
That address will contain, if you've built it this way, will contain rules like - I can only spend this many coins once per month - or something like that.
So I can make my rent payments by giving the pre-signed transaction to my landlord, rather than having to actually send on-chain, I can just give him this transaction and that is enough information for me to look at my address I created and see that he now has all the information necessary to spend that one month's rent worth of coins from it, and I can't spend them anywhere else.
So what I'm doing is I'm just revealing some information to him and then he's able to claim them whenever he wants, and he knows that I can't spend them any other way either.
That's how it's useful for scaling because you're moving the ownership changes off-chain, you're changing it from needing to stamp a transaction onto the blockchain to needing to just reveal some information to the counterparty that they didn't know before.
Once they receive that information, they know that they have all the information necessary to claim it and that I can't spend them in a different way.

Mogashni: 00:18:32

I have a question.
So, sorry, my name is Mo from the Bitcoin design community.
I'm the UX researcher here, very random jumping into the question.
I was just thinking for a very long time trying to piece everything together.
You said, so this code that they share allows the transaction to happen completely off-chain.
So let's say I'm the owner of the code, and then I hand that code over to you, and then we enter into an agreement for X amount of Bitcoin.
What is preventing you from actually spending, you gave that to me, but how do I know that that amount of Bitcoin actually exists and that you don't just go spend it?

## Cold Channels

Owen Kemeys: 00:19:18

The addresses encode the spending conditions for coins that end up there.
So at the moment, all the addresses you generate with your regular today's wallet will say, you're not allowed to spend these coins unless you present a signature from this private key, right?
That's what we're all used to.
In a world where we're using CTV, the address that you generate will say - you're not allowed to spend these coins unless the spending transaction looks exactly like this, that I've predefined.
So to the rest of the world, on-chain it just looks like some coins going to some address, but as soon as I show someone the spending transaction, which would be sending coins to the landlord or whatever, then he is able to verify that that transaction, that spending transaction, is the only spending condition for that address.
So if he's not able to verify that, because maybe you've got some secondary spending condition where Mikey can still spend it after two weeks or something, where you can try and rug pull, if he's not satisfied that that spending transaction is the only way to spend those coins, which he can calculate for himself as soon as he had said information, then he should not consider himself paid.

Maybe it might be easier to have a look at another example, which is the cold channel example, because that's a much more immediately visualizable, useful thing.
I mean, we can't read it in the background, Christoph, but maybe you can scroll up a little bit, because that's easy to understand.
The cold channel construct is something useful for Lightning.
So at the moment, when you want to open a Lightning channel, you need to deposit coins into the multisig address with the channel partner, and there's normally several stages of on-chain hops before then, because you know you're getting paid your salary or something, you're not going to have that sent straight to the Lightning address because you and the channel partner need to negotiate in advance what the balance is going to be, and get everyone to pre-sign all the revocation transactions, all that stuff, so you don't tend to deposit straight into the Lightning channel address today.
Maybe it goes to your cold storage first and then later on you decide you want to have some more liquidity on Lightning, so you send it - and then all the node packages tend to want you to send it into the node's single custody first, so it can then do the negotiating stuff with the channel partner.
Then only once the negotiation stuff is agreed, do you then deposit coins into the channel address, and then you can start using it.
But that's using several on-chain transactions just to get this off-chain transacting started.

With CTV, we can do this thing called a cold channel, where using a couple of different spending routes, which are in one of the other slides, you can create an address that is a Lightning channel already, but the counterparty doesn't know about it yet.
To everyone else in the world, it just looks like a regular deposit address.
Then you can leave it there for months, years.
No one else knows there's any (other) way to spend it, it just looks like a regular signature address.
But when you decide you want to start spending those, you can reach out to that counterparty and say, hey, by the way, this address here, this was actually a Lightning channel between us the whole time.
If they're responsive, then you can start using it like a regular channel without any more on-chain transactions happening at all.
So you don't need to move funds from that address into a channel address or anything.
It's already a channel address and all that needs to happen is you give a little piece of extra information to the channel partner, and now he has everything necessary to start operating it as a regular channel with you.
So why that is interesting is not only does it cut out several on-chain transactions, but it also means that you can treat this as cold storage basically.
So you might as well receive all of your salary payments into these cold channels, because you get a free option to start using it as Lightning immediately at any time that you so wish without a security trade-off.
Whereas today, your channel partner knows all the channels that you have together, and that means that they have the opportunity to try and steal from you, because Lightning is this sort of like cooperative, but also adversarial protocol.
So you remove the adversarial element until you reveal the information to them.
That works because when you give the counterparty the information about all the CTV structure, he can see that the only ways to spend this coin are either through Lightning, which is just 2 of 2 multi-sig, or through the secondary path you can take is the justice transaction route.
He now knows that when you go that route, he will see a transaction on-chain that starts a time lock where he can spend it immediately, but you can't.
All the parties can have enough information to just start treating that existing address as a channel, without doing anything more on-chain.
So you save a couple of transactions, but you also flip the incentives around.
And that's why it's really interesting.
Maybe there's questions?

Yashraj: 00:24:27

Yeah.
Owen, so I think what you said, it made a lot of sense, it saves cost, and there is safety, and all of that stuff.
How do you think existing user flows will change if we deployed cold channels?
That's the first question.
The second is, are there any new user flows that are enabled by this?
Of course the first question was how does it change the existing user flows, for example in Phoenix we have deposited on-chain, so there is that kind of a user flow where you have to deposit funds first.
But then the way that Muun Wallet does it - is that it does these submarine swaps and kind of avoids it all together.
So it seems like around the channel stuff, there are a bunch of user flows, how would you say CTV impacts those, or improves those?

Owen Kemeys: 00:25:32

So how I think it would look is, first of all you construct this cold channel by yourself without needing anyone else's cooperation.
You just need the channel partners, public key or something like that, something that they publish that isn't risky to them.
So this would probably be like an LSP and they would probably publicize that they do this because it gets them more liquidity.

So what I imagine the UX sort of flow would look like is - you need to construct this address first of all, because you're going to give it to your payroll process, or your exchange, or whoever to do the withdrawal to, so you would need to pick who the channel partner is going to be, which LSP, which probably seems like a dropdown or something like Async or Zeus or whoever.
And then it seems like the wallet in the background would do all of the CTV construction stuff, because the user doesn't even need to see or care about any of that.
It's like a standard template that you would just deploy.
Then the outcome of that would just be an address that you just give to payroll or whoever, and it gets paid to.
I think you would need to, in the sort of the wallet balance area of the app, I think you would need to keep these in a segregated spot because they need to be almost like unsealed or something to start using them on Lightning.
So you wouldn't want to just dump it into the regular Lightning balance, because you can't start spending them right now.
A step needs to happen between the receiving and the spending.
It's just that that step does not require an on-chain transaction, just requires communications with the LSP.
So it seems to me you naturally end up with like a cash account or something, which is your actual Lightning available sats right now.
Then maybe like checking account or something, which is like sats that are available on Lightning, but you need to unseal them first, or we need to come up with a term that makes sense to people, but they're ready to go, you need to complete the communications loop first.
So they're sort of like reserves or something like that.
The unsealing seems like it could just be a regular button or something that starts a communications loop with the LSP, and you ping them and say "hello are you awake", and they go "yeah we're still here, everything's fine", and then you go "Bang here you go, this was actually a cold channel with you the whole time".
You're happy to start spending it and they go "yeah sure, whatever", and then you can move it into the available funds.

Yashraj: 00:28:01

So would it mean that wallets and even users might not have to think about an on-chain balance and a Lightning balance as two separate things, and they can just like start thinking about them as one and the same thing?

Owen Kemeys: 00:28:24

I'm trying not to put my personal...

Michael Hasse: 00:28:27

I think you would still have to top up this kind of, let's say, Lightning balance.
It wouldn't just be immediate.
You wouldn't need to deposit, but you would still have probably two different, let's say, buckets or balances.

Owen Kemeys: 00:28:47

Yeah, I wonder whether these might actually replace the whole on-chain balance thing, because that's not awfully useful in Lightning at the moment, right, because you need to go and make another $5 transaction to start actually using it.
Maybe these would just supersede the on-chain balance stuff.

Yashraj: 00:29:02

Right, because right now in Phoenix wallet, you try to make some transactions - from the user perspective, it seems at some random time, the wallet will tell you that no, now you need to pay $5 or something, and we don't know what's happening in the background - is the channel being made larger and all of these things.

What it seems like you might be saying is that the users will never have to think about that again.
It will simplify all of those those mechanics.

Owen Kemeys: 00:29:42

Yeah, in an ideal world I think so.
I mean there is still a trade-off to make.

What we didn't talk about already is in the case where you've got one of these cold channels, you deposit some funds there, and then you call the LSP that it's a channel with and say - "I'd like to start using it please", and they don't respond for whatever reason, then you need to move from that address to another one, because as part of the assurances that you need to provide to the LSP that you're not going to rug them, that means that the only routes to spending the cold channel are the cooperative case, which is the multi-sig like now, or the "something's gone wrong and I need to move on" case, which adds a time lock, which is how he's got an assurance that you can't rug pull him.

So if he doesn't respond, you do need to make an on-chain transaction and move to another address.
So we will still have to factor that in, but hopefully with a professional LSP, this is a very rare occurrence, like in the Phoenix situation.
Phoenix is so tightly integrated with ACINQ, they're not ever going to be offline, it shouldn't really ever be an issue.
But you do need to have that in the back pocket somewhere like how you would resolve that.
But it should be quite rare and it's kind of no worse than today where you have an on-chain balance that you still can't use without spending some money on another transaction anyway.

Yashraj: 00:30:59

So I would still be able to spend these funds for some other purpose, but I would have to do something else.

Owen Kemeys: 00:31:09

Yes, you need to make an on-chain transaction to move out of the cold channel construct and into another address, which could be a different cold channel with a different LSP, like in one swoop.
It doesn't have to be moved out to a regular private key address and then moved on again.
You can chain these things together because they're all just addresses on-chain that don't need negotiation first.

Christoph Ono: 00:31:38

Sounds like we have two potential user flows we could mock up here.
One, the vault, and then the cold channel one.
That would be really interesting to see some UI explorations on those, on exactly what we just talked about.

## Payment Trees

Owen Kemeys: 00:31:51

I think that's a good starting point as well.
The really important work to do later is the tree stuff.
It makes sense to start small.
A cold channel is basically a vault structure on top of with a multi-sig as well, you've just reshuffled who the parties are, but everything is basically either starting time locks or using keys to spend a different way.
It might make sense to come back to the tree stuff later on because it's just a bigger version of all the stuff that we're covering already.

Christoph Ono: 00:32:31

Yeah, I tried to understand the tree stuff.
There's a point where I just didn't get through it.
Especially once everyone's in their trees, how you have any assurances of anything in there.
But I don't know, how's everyone else doing with the tree stuff?

Mogashni: 00:32:53

Yeah, I'm going to sit in the tree right now and enjoy the view.
That's where I'm feeling the trees right now.

Christoph Ono: 00:33:00

But what questions do you have?
What can we clarify, or what would you like to?

Mogashni: 00:33:06

I think if it's explained in an example, if someone gets paid, I would be more able to understand it if it's an actual mock-up in a user flow, it would make a bit more sense to me.
I'm not, it's just not quite there.

Christoph Ono: 00:33:28

Which part?

Andrew Lawton: 00:33:31

I'm sorry, I'm gonna agree with what you just said, Mogashini, and ask if someone could just step through a narrative.
Just tell the story of how this thing works with the rent.
Like the example, if I think, okay, I want to post-date a bunch of rent.
Is that a good place to start?
I've talked with my landlord, and I'm going to stay in this apartment for a year, but then all of a sudden the water heater goes, and I have to move.
How would I run that scenario at month six, even though I gave him a bunch of post-dated checks, how do I stop from month six to month twelve, and move and not pay him until he fixes the water heater?

Owen Kemeys: 00:34:30

I think the rent example was not a good place to start.
I wanted to move to the cold channels, because I think once you understand that a cold channel is just an address, the same as any other address, but it has Lightning like optional functionality, then you can start to see how that is a very useful thing for everyone to have for every payment they receive from anything, because Lightning payments are just better if you can make it work.
The main hurdle is that you need to get the sats into Lightning in the first place, and we're kind of removing that concern.
So rather than the landlord rent example, if you think of it as next time I make a withdrawal from an exchange, I can only give them one address.
Let's say they're a dumb exchange that doesn't do Lightning or anything yet, they just do boring old on-chain transactions to one address, and they're going to charge me 50 bucks to withdraw or something.
What I could do is withdraw to an address that is actually a tree of my own of which one branch is a big cold channel right now.
Another one is like my backup cold channel that I might start using in a couple of months or something, just reserves.
And then another one is to my vault and that's 50% of the withdrawal or something.
You can do all those three things in one go with one address that the exchange doesn't need to cooperate with at all or know anything about.
They don't care.
They just send sats to an address and you're done.
It's the lack of needing cooperation, I think, is what's very useful about these.
That you don't need them to know or understand what you're doing at all.
All the clever stuff is happening on Bitcoin itself, and the person spending to you, the payer, just sees an address as complicated as you want.

Andrew Lawton: 00:36:18

This would be more like, okay, I got paid and I have a checking account and three savings accounts.

Owen Kemeys: 00:36:24

Yeah, you could easily structure it that way.

Michael Hasse: 00:36:30

You could probably even say that when the payment comes in, it goes into the checking account.
From there, at the end of the month, whatever is left, or a certain amount goes into a vault.
Two payments go to your children for their, I don't know, chocolate and stuff like that.

Andrew Lawton: 00:37:00

But if my child has been bad and they don't deserve the chocolate, can I reverse?
Can I switch it off?
We're getting at the essence of the covenant, the promise, and the promise being broken.

Owen Kemeys: 00:37:15

Yeah, so one way you can think about that is you can have multiple different spend paths, which is true today.
Think of a multi-sig, you could have a multi-sig that requires two of three to sign today and anytime, or one key, but I have to wait six months before I can spend it that way.
That's an example everyone's fairly familiar with.
You can do the same thing and have a CTV spend, which is you must use the exact template transaction, which is some goes to the kids, some goes to the landlord or whatever.
Or the alternative is maybe a multi-sig where the landlord and the kids and me...
That's maybe isn't a great example.
The point is you can fuse these two things, you can have a templated path or you can have a multi-sig path, and that multi-sig, you can think of that as everyone having a veto vote.
You know, we all have to agree, if we all agree, then we can spend this pot of sats, however the hell we want.
Or if we don't agree, then we can all trust the template path because that's locked in and committed already.

Andrew Lawton: 00:38:20

I see.
Yeah, yeah.
So, again, I'm staying with the narrative here.
So, my child did not do their homework, so they don't get the chocolate.
My wife and I are on the multi-sig and we both agree, okay, no, he can't get the chocolate.

Owen Kemeys: 00:38:41

Yes, it would work like that, but I don't think it's a great example and that's maybe more confusing.

Yashraj: 00:38:47

So, Owen, I feel with these covenants it means to make a promise and all of that stuff, sometimes you might want to break, you want to be careful before you make a promise and so if you do a transaction structure and then you don't want to do that, is it possible in scenarios to commit to something that I will do this, but then have the option to say no I don't want to do it.

Owen Kemeys: 00:39:31

Only if you've built it that way.
So remember, the address encodes the spending conditions, so you've decided what conditions should apply for you to be able to move those coins.
The covenant is almost more useful as a way to prove to someone else that I can't spend it any other way.
So maybe another example, and this is still a little bit abstract, it's not that useful by itself, but we can use it for payments between three people.
We've already covered the compression thing, we can give this one address to the exchange and it has many different things inside it.

Imagine that there are three branches and they are each branch is owned by one particular person.
Alice, Bob, Charlie.
Let's say we set it up so that the template route is - exactly one third goes to each member.
But there's also a multi-sig route that must be three of three.
And that multi-sig route, you can spend to anywhere that you want.
So we can all fall back on "the everyone gets exactly one third equally", because we know that that can't be removed unless we all agree.
But if we do agree, we can spend it any way we want.
So if Alice needs to pay Bob for something, and Bob needs to pay Charlie for something, and Charlie does something else for Alice, whatever, we can change the amounts.
It doesn't have to be one third to everyone, it could be 90% to Alice and 10% to Bob and nothing to Charlie, as long as we all agree on that.
And if we all agree, we can sign a transaction to spend from that initial address we gave, then it moves on to spend to wherever we want, because we all agreed.
So, you know, that's not really that useful in the real world, but as a principle, maybe that explains better, how this stuff can work.

Yashraj: 00:41:15

Yeah, yeah.
I just heard your example in detail, I think you're absolutely right.
That's not exactly giving the picture of what CTV can do, it seems in this case it would be CTV plus some of the other taproot things and combine them to get this use case.
This flexibility, I think that's the point here.
Yeah?

Owen Kemeys: 00:41:41

Yeah, it's not that useful by itself, but it's very powerful primitive when we combine it with other things that we have.

## Possible Use Cases

Yashraj: 00:41:50

Right, so I was trying to think about it in the lens of something that you mentioned earlier.
What are the new new use cases it enables?
How does it improve some of the existing use cases?
And what else?
Maybe it can do the exact same use case, but with improved privacy, or lower costs, or things like that.
So can we try to think about the use cases and CTV in these three categories, just to be able to understand it and the applications in a more concrete way.

Owen Kemeys: 00:42:40

Okay, so that example I just gave with the three people, that's a very small example of what's called a payment pool, or I kind of use the word tree sometimes, because that's more how it's actually structured.
But these can be scaled up to whatever size, the limit is how large do you think you can reliably collaborate between people.
Three sounds probably pretty easy, especially if you've got no time constraints.
Ten, probably fine.
Theoretically, hundreds, I guess, if you're like not in a rush, maybe.
Also remember that those inside the tree structures, inside the CTV, they're just payments to addresses, and addresses can also be CTVs. So each branch can be another tree in itself that you don't even need to know about or care about.
Like that payment to Alice might actually have had 500 branches coming off of it, some of them were vaults, and some were cold channels, and some were all sorts of other stuff.
Why this is powerful is because this allows us to scale Bitcoin significantly by pushing all this transacting off-chain but with on-chain level of assurances still.
There have been some papers even demonstrating that, things get a little bit unwieldy for sure, but in theory you can do global scale with this stuff if you can have a tree with a million people in, which is done by using some timeouts and things to force roll over at particular time so that everyone can rely on stuff without having to get those million people to actually collaborate on everything.
So this is the scope of what we're talking about here.
But we need to start small with things we can design right now for sure.

Yashraj: 00:44:17

Yeah, yeah.
I hear what you just said, so this is scalability and improves privacy.
Like these use cases could be, so if it's just one UTXO shared by a dozen people, and then there is a spend from that, you don't know who was the owner of the previous one and who's the owner of a new one and things like that.

Owen Kemeys: 00:44:47

So with what you can surveil on-chain, you're just seeing one UTXO, and we're all kind of familiar with it with Lightning already where it's one UTXO on-chain but it's owned by two people, but the sats in it - when we broadcast the closed channel state - and I have 5,000 fewer sats you know that I've paid them to the channel partner, but you don't know where he sent them onto because I've routed it through the whole Lightning network, so the privacy improves significantly.
A simple way to think about it is that you have that effect but with more than two people inside that UTXO, and you actually don't even know how many people are inside that UTXO.
It could be two, or it could be a million, there's no real way to know.
You get a lot of privacy for free.
Not perfect, sure, but better.
You get the payments kind of flexibility stuff in the same way as we do with Lightning.
But I think that the most compelling case for CTV was the scaling stuff, which is what a lot of people didn't really understand until about six to twelve months ago, just because it's very abstract and hard to think about.

Michael Hasse: 00:45:52

Like the movie Inception, you can have a dream in a dream in a dream, right?
That's the forest for the trees.
I found it a pretty good visual in the tweet thread.
Yeah, I'm going to definitely next week work on the vault thing because it's basically what I, in the hackathon, like a year and a half ago, worked on for the inheritance topics where you have a dead man's switch that keeps transactions from happening.
But you have to have previously on-chain transactions for everything, and you couldn't have something like these time locks where you have, let's say two weeks or a month before to reclaim the funds to an emergency address.
So that's definitely something that I'm gonna work on.
But I had a question - if I have, let's say, one Bitcoin and if I create a transaction, or have a kind of a setup where if I spend less than 0.1 Bitcoin, then I need only one signature?
If I want to spend more, I need two or three.
Is this something that would be also a use case for these kinds of things, no?

Owen Kemeys: 00:47:37

Yes, so you can't do that today, but you could do that in a covenants world.
That would look like having several different possible spend paths, one of which was a template - the spend must be 0.1 BTC to address A, with key A - and path 2 might be you need keys A and B and it goes to address C for 0.2 BTC or whatever.
You get the gist.

Michael Hasse: 00:48:01

Exactly.
So we have a reference design Christoph, for exactly this use case.
So somewhere we have exactly that, where you have a condition that if it's less than something, only one signature is enough.
But these are, I mean, these are the practical use cases, I'd say.

Christoph Ono: 00:48:28

No, that's a different, that's the assisted custody one, where you have an auto signer that signs transactions below a certain amount to facilitate low amount payments.
Then for larger amounts that you're not comfortable with being automatically approved, that's where you need to get your extra keys out, but it's the same key configuration there's just the software kind of enforces them.

Owen Kemeys: 00:48:54

So in that example you're trusting the signer software or the custody partner or whatever to not sign if they don't meet your terms.
This is what CTV kind of does is it allows us to take things that were previously trusted and make the chain be the only trusted thing instead, which is obviously an improvement for many things.

Christoph Ono: 00:49:15

Yeah, so I feel like I get some of this stuff.
So I was just trying to diagram a few things here, I made lots of other diagrams here earlier today for explaining fiat over Lightning with synthetic fiat and all of this stuff.
So I'm just reusing those.
So, here's my understanding.

So Alice comes up with a bunch of rules.
Like, I can spend these 2 Bitcoin after one year, but Charles, he can spend 1 of those Bitcoin after one month, and he can spend another 1 Bitcoin after two months, whatever the rules may be.
Then I kind of compress them and turn them into this address.

Then I tell Bob, Robert, who is my employer, so I give him this address, it looks like general address, and they're like, "Okay, here's your salary."
That means these Bitcoin here will be locked to the conditions saved in this address.
So now we have rules and we have bitcoins tied to them, and from then on, all interactions with these Bitcoin are governed by these rules.
No one knows about those rules, only Alice does.

So my landlord, which is this guy here, Charles, I have to tell him about those rules.
So I have to give him an address.
And it's like, here's my address, there are two Bitcoin in there, and here's a rule that I baked into this address, and Charles can verify from the address like that, that's actually accurate, and there are no other rules, where Alice can secretly take things away.
And he's like, okay, cool, I can spend one of those Bitcoin next month and then another one in two months, right?
But that's it.
Like no one can change these rules anymore.
And we're all kind of tied to them.
And that's kind of it.
So that's my understanding.

How do we get here from trees and trees and billions of scale?
Maybe it needs another 400 diagrams.

Mogashni: 00:51:16

This makes sense.
This makes a lot of sense.
I needed those visuals.

Michael Hasse: 00:51:19

And another call probably.

Yashraj: 00:51:22

But does this one require CTV, Owen?

Owen Kemeys: 00:51:27

Yes, because CTV is what's being used to say - you can only spend one Bitcoin.
Today, you can do time locks, sure, but you can't constrain how much, all you can do is completely unlock the address or not have it be spendable.
Whereas with CTV, you can say how it can be spent, in CTV is a specific type of covenant that is all the terms of the spending transaction are built in already.
So it's _how much_ and _where to_.
With some of the more flexible covenant ones, you can pick and choose which bits of the transaction you want to constrain.
It's easier to think about if you're using CTV as a starting point, where it's just - this is exactly how it must be spent and nothing else.

Christoph Ono: 00:52:09

I had one question on here, and that wasn't clear to me.
Alice can say, here are the rules, but what is the unique thing that only allows Charles to spend them?
Why cannot Alice not spend through those rules?
There has to be some secret that only Charles has where Alice can't give everyone else.

Owen Kemeys: 00:52:30

It's not that Charles can spend it, it's that one Bitcoin can go to Charles's address after one month.
So anyone who has this information can just broadcast it straight away.
Think of it like a PSBT that can't be spent differently.
The rule is the Bitcoin has to go to Charles's address.

Christoph Ono: 00:52:47

So Alice has to know Charles's address in advance when she comes up with those rules?

Owen Kemeys: 00:52:52

Yes.
That's one of the useful limiting factors of CTV because you can only bake as much in as you can coordinate in advance.
That's what stops things from going completely off the rails.

Christoph Ono: 00:53:03

Okay, so we need a thing here - where Alice talks to Charles and says "Give me some addresses."
Then she can bake those in the...

Owen Kemeys: 00:53:25

Yes.
And who knows what the addresses of Charles's are, they might be just vault addresses, or they might be regular keys, or they might be trees, or they might be vaults, or they might be cold channels, or God only knows what he's doing with them.
As far as you're concerned, it's just an address.

Michael Hasse: 00:53:39

Okay.

## Other covenant proposals

Yashraj: 00:53:42

Owen, I think we spent the whole hour talking only about CTV, and there are like a dozen more proposals and stuff.
What's the...

Owen Kemeys: 00:54:03

I lost the tail end of that question.

Yashraj: 00:54:05

Oh, sorry.
I was asking what about some of the other proposals?
This is just all about CTV.
What about but what about LNHANCE and `OP_VAULT` and CSFS (`OP_CHECKSIGFROMSTACK`)?
There are so many of these, I don't even know what those are.

Michael Hasse: 00:54:28

You have to wait for the next tweet thread.

Owen Kemeys: 00:54:32

LNHANCE packages CTV plus CSFS and something else (`OP_INTERNALKEY`) to make a suite of soft forks bundled into one that are particularly very useful for Lightning.
CSFS, just a way to think of it holistically is that CTV is the most constrained version because you specify everything, every element of the spending transaction in advance.
CSFS and other proposals allow you to say, maybe I constrain the amount, but not the destination, or vice versa, but you're generally making it more flexible.
There's other technical differences, like exactly how they go about that inside the code, and which bit gets hashed when, and which bytes are used for that, whatever, and so on, which is way beyond me.
From an object level, as far as we in the UX world are concerned, CTV is like everything must be defined in advance about how this gets spent, and other covenant proposals are where you can choose which elements you want to constrain and how.
That makes a design space even larger.
I haven't even started thinking about those yet.

Michael Hasse: 00:55:42

One of these things I seem to remember, and I hope I remember it correctly, is that you could leave out which UTXOs should be spent, because you don't know in advance.

Owen Kemeys: 00:55:56

And that's any AnyPrevOut, APO (`SIGHASH_ANYPREVOUT`).

Michael Hasse: 00:55:58

Yeah, probably.
It's a big design space.

Owen Kemeys: 00:56:07

Yeah.
I can't advise awfully much on anything else besides CTV at the moment, because it's even larger to think about.
I know any AnyPrevOut is particularly useful for Lightning because it allows you to not need to keep holding on to all these old channel states just in case someone broadcasts a really, really old one.
You can just keep hold of the latest one in the case that the channel goes wrong and you have to force close it suddenly somehow, the latest one is enough.
You can forget about everything else.
But I don't know how that is used in other more interesting covenant constructs yet.

Michael Hasse: 00:56:41

Right.
Yeah, we would probably need to know what we want to do before, and then only then can we say, okay, is CTV enough or do we need something else?
So probably reverse the reasoning there a bit.

Owen Kemeys: 00:57:04

That's one of the arguments that gets made and why there's a lot of discourse about this stuff, because some people want the really expressive forms, some people want the really limited forms of covenants, and I'm in the camp of the really limited form because there's already a lot of very interesting stuff we can build with it.
We also know it's about as safe as you can get in terms of soft fork upgrades, because it's so limited in scope and well studied.
Then as we build more things with it, we can start to see where it doesn't quite do enough, and then we have more confidence about what extra things we need to add without breaking stuff.

Michael Hasse: 00:57:41

Yeah, this was super helpful.
I really learned a ton today and from the threads.
It was really, really helpful.

Christoph Ono: 00:57:51

Yeah, for sure.
We could do a design huddle where we collaboratively try to design some flows for it.
I'm thinking about basic stuff where you look at your coins in there.
You're going to have to look at your balance or your transactions, and there has to be a little thing that says this one has extra rules attached, and then you'd have to somehow see those extra rules.
Then you would have to think of the whole backup flow, because this is off-chain data so that it doesn't get lost.

Michael Hasse: 00:58:27

We could also in a design huddle have these real world use cases, like the one with the rent, and the one with something else, and then we give that to Owen.
He then makes the table with all the different covenant proposals and he said "okay you can do that with CTV, with AnyPrevOut" or with all these different things, so we can compare them.

Christoph Ono: 00:58:58

Okay, and here in my background, to wrap things up are some AI generated trees made of Bitcoin addresses.
At least that's what Midjourney thinks it looks like.
Looks more like broccoli, but that can be our next topic.

Owen Kemeys: 00:59:14

Hey, That's cool.

## Questions

V: 00:59:21

Yeah, I had a question.
I got to know the idea of it, but I have a small question.
I know that all of this is off-chain, and how will he spend it?
When the owner or whoever gets the amount, he can spend it like that, or he needs to go and convert it into on-chain, and then he can spend it?

Owen Kemeys: 00:59:50

Yeah, that's the million dollar question.
This is where a lot of people get stuck, including really smart developers because it's hard to visualize.
Think of all the stuff you do with the covenants, the CTVs or whatever, as how far you can organize things in advance by collaborating and working together.
So, you know... no, I won't give an example, that's more confusing.
There's only so far ahead that we can plan and collaborate and things can actually work.
Once you reach the end of that and you need to change the structure altogether, you will need to go on-chain, but it doesn't have to be that every single member of the shared UTXO have to all exit out of the chain and then all start again.

You can work together and say, if you're doing a payment pool structure, and Bob wants to leave or something, Bob needs to do something he can't possibly do inside this structure anymore.
The rest of us can be like well I'm fine still staying in here, I don't need to get my own UTXO on-chain and then organize pooling together again in another one.
Why don't the five of the rest of us, we'll all just hop across at the same time that Bob exits, and start another pool or join an existing pool somewhere else.
The way we use Bitcoin today is kind of quite crude and simplistic, and we need to start realizing that the chain is for _logging commitments_ that you can't go back from, basically, rather than _ownership transfers_, because we can now achieve ownership transfers off-chain, but there just comes a point where we will need to do something that we can't do off-chain and we can capture that change in an on-chain transaction, but it doesn't have to be splintering it into a million pieces and starting from scratch.
We can still collaborate to move from one tree to another, but this is the stuff that's super hard to visualize, so I may not have explained anything at all.

V: 01:01:50

Yeah.
Okay.
And one more question.
In the start, you said that it's necessary that they respond back.
What was that about?

Owen Kemeys: 01:02:03

It's necessary that there's what, sorry?

V: 01:02:07

Alice has the rules, set up the rules, and there's a landlord.
So when it goes to him, he'll have to respond back, something like that.
I didn't get that idea.

Owen Kemeys: 01:02:31

I wish I'd never said this landlord example because I think it's more confusing than helpful.
Christoph is showing some stuff on the screen.
Was it about that?
What's on the screen right now?

Christoph Ono: 01:02:43

I think the question is like, what does Alice actually give him?
The understanding is she gives him a ready to broadcast transaction almost.
It's like, hey, here's information that you can broadcast, but you don't have to do it now, and it's not valid right now, but in a month, you can do so.
Then the landlord, Charles here, he just has to keep that transaction or that piece of information and then months later just plug it into his Bitcoin wallet and say "here, broadcast that, I want this to be executed," and then the Bitcoin will be transferred.

V: 01:03:24

Okay so he has to reply back to Alice that I want to use it?

Owen Kemeys: 01:03:29

No, she she will give him this little chunk of information.
So think of it as if we were doing it with PSBT, with signed transactions.
If we weren't using covenants, she could give him a pre-signed transaction and say, look, here's everything you need to withdraw some coins from my address and send them to yourself, signed by me.
But he can't trust that, because she could spend the coin differently before he broadcasts it, so he has to broadcast it now and get it mined, to be sure that it's his.
But in a world of covenants, she can say, here is that same PSBT, but you can also see that the address they're in, I can't spend them any different way than by broadcasting this transaction that sends them to you.
So you're using the transaction as the key that opens the lock now, rather than just a regular key.
By doing that, he may not even need to bother broadcasting them at all until he needs to go and buy a car next year or something, because he knows they can't go anywhere.
They're effectively, they are his.
They're not able to be moved by anyone apart from him.
So although they're not in his address yet, he can consider them his because there's nowhere else they can go.

Christoph Ono: 01:04:36

Yeah, I guess the one addition is that it's tied to that piece of information.
It's not an address generated by his wallet.
So he would have to make sure to keep that piece of extra information, because if he loses it, then he cannot get it back.

Owen Kemeys: 01:04:53

But I don't think that's a huge deal, because you already need to preserve a blob of information, the user doesn't even see the key anymore.
The wallet software is holding on to that key for dear life because if it loses it, it can't sign anything anymore.
This is just in an abstract sense, I think it's just a different blob of information the wallet needs to hold on to and make sure it backs up to the cloud or whatever.
It doesn't even matter if you keep it in iCloud or anything because it's not sensitive, it can't be abused by anyone, it can only send the funds to you.

Michael Hasse: 01:05:26

One design challenge that I think will be for the recipient, they have to be able to inspect this address, right?
Or what it does somehow.

Owen Kemeys: 01:05:42

Yes.

Michael Hasse: 01:05:43

So wallet software would need to surface this information in some kind of usable way.

Owen Kemeys: 01:05:59

Yeah.

Yashraj: 01:06:00

I think about it a bit like  PayJoin, just like one set, because that also involves the PSBTs and all that stuff.
So basically Charles could construct the transaction or like construct something, send it to Alice and then she does her stuff, adds her keys or signatures or whatever, and then she sends it back, and that's like the transaction that's like ready to broadcast.
Is that the right way to think about it at all?

Owen Kemeys: 01:06:35

I'm not 100% sure.
What we can say is that when Bob receives the spending transaction that we haven't broadcast yet, he could even himself go and reconstruct the address.