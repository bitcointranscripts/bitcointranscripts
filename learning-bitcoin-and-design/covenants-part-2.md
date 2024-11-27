---
title: Covenants Part 2
transcript_by: varmur via review.btctranscripts.com
media: https://www.youtube.com/watch?v=zk_EEKeAFuY
tags:
  - covenants
  - ux
speakers:
  - Christoph Ono
  - Michael Haase
  - Mogashni
date: 2024-02-02
aliases:
  - /bitcoin-design/learning-bitcoin-and-design/covenants-part-2/
---
## Introduction

Christoph Ono: 00:00:01

All right, welcome to our second learning Bitcoin and Design call about covenants.
Today, the idea was to go deeper into covenants use cases, right?
Last time, the first call was more about just generally what it is and what it does.
Now we wanted to go deeper.
I think on the web, on the GitHub issue, there was one request about congestion control.
But the other big one was scaling, I think.
So how's everyone feeling about covenants today?
Maybe we should just pick up, I don't know, wherever our brains are.

Michael Hasse: 00:00:50

Well, I'm feeling bullish on covenants (laughter).
I think they open up fascinating capabilities that I would personally probably want, but in terms of the technical soundness or the security implications there's nothing I can contribute.
In general I'm kind of more interested in this kind of bolting or scripting stuff than scaling.
But that's just the nature of what I'm working on currently, so that's not at all some kind of judgment or so.
But it's just in terms of the scaling question I'm not sure how valid any of the things that I have to say or think is relevant.
But it's really interesting, and what stuck from the last call was I think Owen said, in terms of scaling, you can transfer ownership without on-chain transactions and have the same assurances.
So that's definitely something interesting.

## Covenants scaling example

Christoph Ono: 00:02:45

So Owen's threads here, he has three threads, they're really awesome.
I tried to sit down earlier and actually understand that specific part.
I tried to understand how does this enable any sort of scaling and how do you transfer ownership off chain?
There's this one thread here, on the one hand, it kind of makes sense, but there was something I was missing from it too... and let me try to explain.
There was one thread with an example that I thought was pretty good.
So here's what I came up with, which helps maybe with the scaling stuff.
I tried to create a very simple example of this.
There are three people, Alice, Robert, and Charles.
Robert owes Alice 0.1 Bitcoin, and Charles owes Robert 0.2 Bitcoin.
What they would do right now is, Robert sends Alice 0.1 Bitcoin and Charles sends Robert 0.2 Bitcoin.
Two transactions done.
Cool.
Now let's make this way more complicated.
So, Alice gives Robert the address, like Alice's address 1.
Cool.
Robert could technically now just send her 0.1 Bitcoin and be done, but he makes it more difficult.
So he creates his own address because he's expecting money from Charles.
Charles needs to send him money.
So Robert creates an address, Robert's address 1, and that one has rules baked into.
So any funds that go into this address, 0.1 of that has to go to Alice's address, right?
So when he receives whatever he receives, 0.1 is reserved for Alice and no one will ever be able to change that.
That's just how it is.
It cannot be used anywhere else.
Then rule number two is that another 0.1 should go towards a Lightning channel with Dan.
So those are rules baked into this address, right?
Then Robert gives this address to Charles, Charles puts the 0.2 Bitcoin in.
Now we have this Robert's address with 0.2 Bitcoin, and that address cannot be freely spent.
0.1 has to go to Alice and 0.1 has to go to this Lightning channel with Dan.
That's it.
Only Robert knows this because he baked this into the address.
No one else knows about this, right?
On the blockchain, it's like, "hey, there's an address with 0.2 Bitcoin."
Cool.
That's it.
But so Robert tells Alice, hey, look at this address.
There's a rule baked into this one.
So Alice looks at the address and she's like, "cool, that is true."
There's 0.1 Bitcoin in your address, but at some point, they can only be spent to me.
So, you, Robert still has them, but the only thing that can be done with them is to give them to me.
Is that as good as me having them?
You could say yes.
There's a promise in there that cannot be broken.
So Alice now says, cool, they're not technically in my address, but they have to go there.
So it's like they're mine, but they're not really.
They are and they aren't, Schrodinger's cat or whatever.
Then Robert shows Dan the address, and the rule number two, and then you can open up a Lightning channel with them, because there's this promise that cannot be changed.
So in a way there was one transaction that happened.
So Charles sends those 0.2 Bitcoin, but actually we accomplished three things at the same time.
So literally on the blockchain 0.2 were sent from Charles to Robert.
So that debt is kind of settled.
Then there are these baked in promises - that 0.1 will go to Alice - and another 0.1 will go to the Lightning channel with Robert and Dan.
So without covenants, it would be three different things, with covenants they're one.

Michael Hasse: 00:07:35

It depends on what kind of address Alice gave to Robert.
So if that's a normal kind of address, she can then spend this 0.1 Bitcoin freely as well.
So basically you can then chain transactions onto this.

Christoph Ono: 00:08:19

Yeah.
You're basically unwinding a bunch of stuff, then you're winding up things, or you bake in all these promises.
You can build promises and promises and promises and promises.
The question is then, and that's something Owen also wrote in his thread, can you do that forever or does at some point this whole thing just have to unwind?

Michael Hasse: 00:08:43

I think this is what he meant with the trees of trees of trees, with this kind of layers of trees.
It always depends what the next hop is going to do.

Christoph Ono: 00:08:56

Your point was Alice's address could also hold promises to other people.

Michael Hasse: 00:09:00

Exactly, and that's also something that nobody else knows.

Christoph Ono: 00:09:10

Yeah.
The thing is, if Robert forgets the rules, then no one can recover them.
No one will know them, because they're not saved anywhere on-chain.
They only exist because he baked them in, and if he forgets them and doesn't share, then they're gone.
That's where I have a whole bunch of questions.
Can all of this fall apart if someone forgets something?
And then all this stuff gets locked or is there always a way out to unwind it where anyone can just back out of this whole system, screw it, I don't like these shenanigans.
And if let's say you do that three times in a row, and I'm secretly paying Mo, and I'm like "yeah you know these Bitcoin they're actually yours", but really they're in Michael's address you have with this rule, but then they're in Lois's address in this rule, and he paid me before with that rule, and then they're actually Bitcoin that my mom sent four years ago with that other rule and then it came over there.
It's like do I need to do all that stuff, or do I not, or how do I prove them that, and will you accept it when you're like "this is way too complicated for me just give me my money."

Michael Hasse: 00:10:35

Well the way that I understood it is the all of these checks are automated in the background, right?
So the address that I give you is only spendable by my rules.
If you receive something into this address then I have the assurance that I can spend it the way I want to spend them.
That's all of this rule checking that you just described.
That's how I understood it works.

Mogashni: 00:11:15

Now, when we speak about use cases, and I'm just thinking about the scenario that Christoph presented.
I personally would never enter into such a scenario because there's just too much of "he said, she said, I promise, you promise, he promises, they promise."
If I would think of a very practical use case, I would just think of a family using it between three people, the husband, and then the wife, and then the kid.
The kid has their own Bitcoin savings for their university or whatever they want to study for, and the couple has an account and it's a joint Bitcoin account, and both of them earn in Bitcoin.
Every time money comes in they both agree that there's a rule that 5% of that goes to the kid's university fund.
It's a covenant between them.
Then it's safe, it's trusted, it's the husband and the wife.
There's not too many people making promises.

Then maybe between the husband and wife, they have their own covenant, which is like, OK, certain percentages, 10% goes for a holiday and then that is that own covenant.
I'm just trying to think of a very practical use case, in a situation which I think would practically work, but I think the more people you add on to this - "I promise, he promises, she promised" is a problem.

Christoph Ono: 00:12:37

The trick is you might not even know, because on chain these addresses look like regular addresses, there might be all kinds of stuff in but you just can't see it.

Michael Hasse: 00:12:47

So which part of this construct is conscious and which not, right?
Because I just want to send you money, and the only thing that I have to know and you have to know is that I can spend that money and it goes to you, and then you can spend it freely afterwards.
So that means consciously we don't even need to know it.
It doesn't concern us, this huge construct doesn't concern us.
The only thing that we need to know is that we can spend that money.
So this is not an attempt to set up this big construct, because nobody has a use case like that.
It's just that we need to have the assurances that whatever we want to do with the money can be done.
For each person in that line of succession, the only thing they need to know is they can spend the way they want to spend.

Christoph Ono: 00:14:10

Yeah, that's true.

Michael Hasse: 00:14:11

Automate it basically.
If I'm in the middle of this whole sequence, I don't need to know what's before it, and I also don't need to know what's after it.
I just need to know that whatever comes into this address can be spent the way I want.
That's it.

Christoph Ono: 00:14:39

Yeah, and it's true, Mo, you define your own rules because it's your address.
So no one can force rules on you.

Michael Hasse: 00:14:49

So you're not part of some kind of bigger scheme, but you're just receiving and sending.
Everything that we talked about is basically happening in the background and it shouldn't even really...

Mogashni: 00:15:06

Right, the protocol is making sure that all of those conditions are met.

Michael Hasse: 00:15:10

Exactly, but you should be able to say okay now I received this 0.1 Bitcoin and then I want, because these are mine and I want to spend them, I want to automatically put 10% of that into my savings wallet, and the rest I just send to people.
So these are then your rules, right?
It's basically one up after that.
The question that Christoph raises, does it break at some point?
Or can you do this forever?

Mogashni: 00:15:55

Good question.

Christoph Ono: 00:15:58

To continue on that thought, I'm not sure what I said was actually right, that no one can force things on you.
So here, Robert tells Alice, hey, look at this address.
There are funds in there for you.
Can she already send them to someone else?

Michael Hasse: 00:16:25

No, the point is the funds have to be sent to the address that Alice gave him.
So then Alice has enough assurances because she constructed the address, and the address contains the spending conditions, or the policy.
So that means once the funds hit her address, she knows that she can spend them.

Christoph Ono: 00:16:59

The way that Owen put it was there's like a PSBT in there.
So, Robert really doesn't have to pay any fees there, but eventually Alice will have to.
So, let's say fees are 200 bucks, right?
And I'm like, "Check Alice, the 100 bucks I'm supposed to send you, they're right there, you can grab them."
But then she has to pay the fees instead of he being the sender who puts it in her address for paying the fees.
He kind of gets around the fees and kind of puts that on her in a way, right, because it's almost like she has to withdraw them.
Or is it if it's a PSBT?
I don't know if it's a fully signed transaction baked in, then I guess it's still on him.
Or is it on... I guess who pays the fees then in that regard?
How does that trickle back?

Mogashni: 00:18:04

I'm trying to see what Bitcoin technical search is going to provide.
I actually said, "how do fees with covenants work?"
I'm just reading through whatever's coming up here.

Christoph Ono: 00:18:13

Maybe no one even knows.

Mogashni: 00:18:15

Yeah, exactly.
There is no direct article about it.

Christoph Ono: 00:18:20

So here's another one, if you're cool with looking at something else.
I was trying to figure out how payment pools work, which are also supposed to be this technique.
So Robert, Alice and Charles, we want to create a payment pool.
We collaboratively create an address that has some rules that we put stuff in.
So on chain, there's an address with funds in it, that's all people see.
But baked into this, there are a few rules.
Robert puts 0.1 Bitcoin in, Alice 0.2, and Charles 0.3.
Then the rules that say this is how much everyone else.
There are rules that each of them can exit this arrangement and they just get the 0.1 back.
Then there's another rule that if all of them agree the funds can be split up differently.
So Robert can get it all and Alice nothing, or Alice can get 0.4 and the others 0.1, whatever.
They can exit with a different arrangement.
So that basically means between the three of them there's now these funds, it's a little bit like Lightning, right?
You have these funds locked up between the three of them and then it's just like Splitwise.
One day one person pays for lunch, they're like okay cool I'm keeping track that you know I owe you this much, and then they do something else, and then at some point they can just settle the whole thing and collapse it into one on chain transaction.
It's a bit like Splitwise.
So they paid you a bunch of times, one year later Alice says screw you guys I'm done with this, let's settle.
It seems like an overly complicated way of doing things for three friends that can just talk to each other, and actually use Splitwise, right?
Why go through all these shenanigans?
Well, where is this useful?
Is it useful in, let's say there are three companies or banks across countries that need to settle between them regularly, or where there's not such a trusted scenario.
The other thing in the examples was that, well, someone can exit from a pool, and the others can continue in the same pool, or they can spend and split up and go into another pool, then it's like, awesome, cool.
That was one of the things that I read - it's like you can have pools and pools and pools and they're all linked and I thought I don't get it.
What are you actually achieving here?
Who tracks all of this stuff, right?
I don't know, that was my insight into payment pools, and I feel like I'm missing something still, but I also didn't spend a ton of time on it.
So I don't know.

Mogashni: 00:21:30

So is this is a protocol layer thing that makes sure that these agreements are met, and then it makes sure that everything goes on agreement underneath the hood.
So it is a protocol layer that will continuously be worked on, so that the rules are constantly updated according to the needs of the network?
This is just the thing that I'm trying to understand as well, is there one dedicated developer now working on covenants or how is it like?

Christoph Ono: 00:22:04

I gotcha.
All of this stuff, both examples here, they're based on the same thing, that you can bake rules into addresses that no one can change, and then everyone has to follow that.
It's actually a somewhat simple idea, right, just what can be done with the Bitcoin that are put in these addresses, and as far as I know, this idea has been around for a very long time.
If you go to [covenants.info](https://covenants.info), let me switch over real quick...

Mogashni: 00:22:44

Yeah, 2016, I see one of the first talks given about it.

Christoph Ono: 00:22:49

Yeah, covenants.info - there are nine different proposals around there.
And from the Stephan Livera podcast, they have various different technical complexities.
Generally people want the simplest version because there's the lowest risk that anything can break, and it's the easiest to reason about.
Each technique, solution, allows you to do things slightly differently, right?
It's important to think through how these differences could play out over time, and what they could lead to.
Then there are these different use cases and stuff.
Some are more, you know, not spectacular, what is it called... speculative than others.
So no one's decided on anything, it does feel like a whole bunch of people really want this to happen, and others say well there's no real urgent need, we have other problems and other things to figure out.
There's also seems to be some confusion right now about how you actually make a change to Bitcoin.

Michael Hasse: 00:24:14

I think that's also why Owen focused on CTV, which is one version or implementation, version of what Christoph just mentioned, because that seems to be the most widely accepted one and best studied.
But any kind of assessment of viability is far beyond my...

Christoph Ono: 00:24:58

One extra thing was, it's not like these things just get discussed, and then someone decides, and then they get implemented.
Some of these things have been implemented on TestNet or RegTest or maybe even on other chains, so you can see in practice how they pan out.
I feel like Liquid even had something like that for some.
So there are these practical explorations that take you to a certain point.
But yeah, the bar is just really, really high for any of this.

Michael Hasse: 00:25:34

Yeah.
Then you have the concern or people.
If we take this scaling example, what kind of impact does this have on miners who actually secure the network?
It could collapse their income basically.
What's the kind of the impacts of that?
I don't know because if you can collapse 10 transactions into one, then obviously there is an economic impact.
Apart from the security concerns that's another thing to consider.

Christoph Ono: 00:26:17

You know, maybe the Bitcoin network in the future, all of the actual transactions will just be really cheap, and we just live off of the money from art collectors and all the JPEGs.
(Laughter) It's just art funding.

Mogashni: 00:26:35

So apparently there's also some people also write white papers, well not white papers, but they write - there's something called "Vaults and Covenants" as well.
In this paper we examine how they might be implemented.
That new approach is presented, which avoids pitfalls of general covenant proposals.
So as Christoph said, there's many different covenant proposals, each proposal has its own pitfalls.

Christoph Ono: 00:27:03

Vaults, I don't know, I feel like vaults are more of an implementation or a use case for covenants.

Michael Hasse: 00:27:10

Exactly, a use case for covenants.
Like scaling is a use case.
That's why, because covenants take so long, in the last maybe 12 or 18 months, the interest in Miniscript picked up significantly, because you can program similar or not quite as sophisticated stuff like with covenants, but you can achieve some kind of programmability with Miniscript already, with what we have now.
That's kind of the dynamic, covenants would take that programmability to the next level, definitely.

Mogashni: 00:28:17

So ChatPDF to the rescue.
I downloaded that white paper.
It's called [Vaults and Covenants](https://jameso.be/vaults.pdf).
It's 13 pages, published 9 January 2023.
I uploaded that to ChatPDF and I asked how vaults are related to covenants, and basically it's a storage mechanism.
It's more for more security but there's a 13 page article on vaults and covenants if you'd like to read it.
"Vaults are a technique for substantially reducing the risk of Bitcoin theft, they are a form of covenant that give Bitcoin users operational simplicity but heightened security."

Michael Hasse: 00:29:03

This is a technical description of the implementation of vaults, but you can also create a vault from a different type of covenant proposal, right?
I see a vault as an object and not as an implementation.

Christoph Ono: 00:29:53

A feature.

Michael Hasse: 00:29:54

A feature, exactly, a feature or a use case.
Vault is a use case, but for me, and I'm a technical layman, but I have the feeling it's more helpful to think of vaults as the feature, or the thing that you want to achieve, rather than the way of achieving it.

## UI - Owen's Figma Prototype

Christoph Ono: 00:30:17

By the way, did you see Owen's Figma prototype?
Do you want to look at that one or do you want to continue with the vault?

Mogashni: 00:30:27

No, let's see the prototype.
I'm keen on seeing it, if anyone else is open to as well.

Christoph Ono: 00:30:35

I'll share that link [here](https://figma.com/proto/o4sxu0rEIR1zmletrxtXRn/Phoenix-CTV).
So he mocked up the idea of cold channels.
So earlier in the example, I think Alice, Robert, whoever said part of this deposit is dedicated to a Lightning channel, right?
So that Lightning channel is not technically active, there are no nodes talking to each other and stuff, but the funds are dedicated to it, right?
It's kind of secretly committed to this Lightning channel, and so typically you do need to create a new on-chain transaction to get funds into that state, but here you have that automatically.
So it saves you a transaction and you have this secret - what he calls cold channels, or in this case reserves.
So let's say you're in Phoenix here, and someone sent you 0.1 Bitcoin or whatever, and you've created an on-chain address with this cold channel option.
So then that would go into what he calls reserves.
Here you would in this example the balance is 433,000 sats plus 1.3 million in reserves.
That means if he ever runs low on liquidity, he could activate his reserves, activate these cold channels for free, I think?
So what can I click here?
So I can receive.
So here you can see that I can choose between regular addresses or what he calls simple address, and cold channel addresses.
It looks pretty much like a regular address, but anything received to that has the cold channel option.
Then I want more liquidity and then I can see here are all these different deposits that I can activate.
And then I activate one, I confirm it, cool, sweet.
I have now 300,000 more sats that I can spend on Lightning, basically for free, and instant, I think there just needs to be this connection established with the other node.
But because on-chain transactions are taken care of already, you save those 10 minutes, or that block confirmation.
How does that sound?

Mogashni: 00:33:31

That was a lot to take in.

Joaquin: 00:33:32

"Each reserve is a dormant Lightning channel ready to activate and use countless individual smaller payments over a longer period of time.
Any channel finally depleted must be closed..."
So what is it saving?
It's saving just a transaction fee in the future?

Christoph Ono: 00:33:58

Sorry, what was the first thing that you read?
I didn't quite catch where that came from.

Joaquin: 00:34:02

Oh, it was the final page in this little prototype.

Christoph Ono: 00:34:06

Oh, OK.
Let me let me take a look at that one.
Where is it?
Under receive or how do I get there?

Joaquin: 00:34:15

After it says activate this reserve, activate now one page back after that.

Christoph Ono: 00:34:30

Oh, okay, here at the bottom?

Joaquin: 00:34:31

Oh no, not that page.
One, try going one more.
It was activate reserves.
It was the fourth screen.
I was just clicking on clicking along the bottom navigator.
I wasn't using the prototyping.

Christoph Ono: 00:35:15

Oh, okay.

Joaquin: 00:35:16

Yeah, sorry.

Christoph Ono: 00:35:18

Oh, this one the receive with the payment tree leaf, that's a whole different thing.
That's not the cold channel.

Joaquin: 00:35:27

No, no, it wasn't.
That's fine.
It was just a general definition of what was going on and I was just trying to get my head around what exactly was going on.

Christoph Ono: 00:35:39

The way it typically works is that you receive funds in your address, and then when you want to open a Lightning channel that is another transaction.

Joaquin: 00:35:48

Right.

Christoph Ono: 00:35:48

That takes 10 minutes to confirm.
You have to pay another fee, takes 10 minutes.
You can kind of collapse this into one using covenants.
So you get these funds and it's like they're just primed for a Lightning channel.
The channel is not active, but it's all ready for it, it's all set up.
So you don't need to wait another 10 minutes, you don't need to pay the extra fee, you just need to say "let's go" and the channel is right there.
You don't have to, it's a free option to have a Lightning channel.

Joaquin: 00:36:29

That's through covenants?

Michael Hasse: 00:36:35

You could also send it as a normal on-chain transaction.

Christoph Ono: 00:36:43

You can either use it as a regular on-chain transaction or as a Lightning channel, it's up to you.
There may or may not be a delay in there.
That's something that I wasn't quite clear on, because if let's say, I promise that Lightning channel on the one hand, and then I have the option to spend it in another way.
How do I prevent some scamming there, if there's not a time lock or some other mechanism that people can hold me accountable for.
That's one thing I wasn't quite sure on.
But then this is the basic idea, and I really liked how Owen mocked this up.
It's very, very in your face.
It explains a lot.
I don't know if we need all that in the future, but I think that's a really good way to start this, to put it in a UI.
Okay, Mo, what are your questions?

Mogashni: 00:37:38

I was clicking around on the prototype and just trying to actually understand.
So we discussed a bit of how it works, like what a covenant is.
I'm trying to click through the UI and try to get this theory that I have in my brain and see how that's making sense on the actual design.
If I'm understanding correctly, the reserves are actually the agreements, or rather the covenants that I have with other people is that correct?
Or?

Christoph Ono: 00:38:23

So you're Robert here.
You created an address, and there was a rule baked in there that some of this can go to a Lightning channel with a specific person.
But you made this commitment, so that's baked into the address.
That's why other people can trust, right?
You're good for this, you've committed your funds.

Mogashni: 00:38:49

That's the fund that's called the reserve in this UI, in this design, this is that reserve bit, is this bit here.
I have an agreement between me and John that he gives me 1%, and you can count on this 1% it's here.
I have another agreement with Mary and this is the agreement I have with her.
So if I want to, I can use this because it is my sats, I just activate it and then I can use it in my transactions.

Christoph Ono: 00:39:30

Yeah, you just activated a channel, a channel that was very well prepared, but was not quite active.
The terminology, of course, is something that that may or may not change.
He uses the term cold channels in here, and reserves.
It's obviously a new term.
So no one knows really what it means unless you actually worked on it.
So that all of this stuff is usual communication stuff.

Michael Hasse: 00:40:01

So in this case, all of these cold channels together are the reserves, right?

Christoph Ono: 00:40:08

Yeah.

Michael Hasse: 00:40:14

The covenant is just basically a rule or a smart contract.
Even a normal single-sig or a multi-sig address are a covenant or a type of covenant because they define how funds can be spent from that address.
So it's a bit of a confusing discussion because the concept of covenants, it's just about enhancing the programmability of the existing system, right?
You can do that in a bunch of different ways, and all these covenant proposals are each a different way of enhancing or implementing this.
But a covenant is just a bunch of rules.

Mogashni: 00:41:27

If I understand this correctly, then I actually entered into covenant with this person over here on the 12th of July, and now I'm trying to activate this covenant, but this person set a rule, well this is not a rule, this is that because the channel partners are responsive but this could be a notification that would pop up to say that this person who you entered into a covenant with, this is only available in four weeks or something like this.
Does that make sense what I just said?

Christoph Ono: 00:42:04

Yeah.
So the way it works here is that this other person doesn't even know that you want to have this channel with them.
You haven't revealed that yet.
So you baked into your address, you said "I want to have the option for these funds to have a Lightning channel with Michael", but I'm not gonna tell him, I'm just gonna bake that in.
Then at some point when you say well "Finally it's time I want this Lightning channel with Michael".
But maybe Michael's node is just not online right now, then you just can't make that connection.
Maybe he got a new wallet or changed his node, or whatever it is.
If you waited six months, then maybe that connection cannot be made anymore.
That's why this might fail.
But you always have the option to just leave the funds there, or just put it onto another address.
That's just not going to happen - that Lightning channel.

Mogashni: 00:43:09

Interesting.
From the UI here as well, I don't know what I clicked on - enter an on chain address receive the withdrawn funds.
So now it's working, that the technical problem doesn't exist now.

Christoph Ono: 00:43:23

No, no, no, it still exists.
You're just taking the other route, you're giving up on this channel with Michael, and you're just putting the funds somewhere else because you just don't want that.
That reserve is useless to you, it's not going to work out, you give up.
So you're just like, okay, I'm going to put the funds in my cold wallet or I'm going to pay rent or something, just going to do something else with it.

Mogashni: 00:43:45

Okay.
All right.
Wow.
If you think that Lightning channels are hard to get around people, this is like, whoa, whoa, whoa, you know, goodness.

## UX issues

Michael Hasse: 00:43:54

From a UX perspective, I don't do much different than I do today.
All these kind of discussions are about the logic that happens in the background.
So once you give me an address, and I send funds to that address, whether it be an on-chain transaction or a covenant enabled promise, then you know you can spend and you can do whatever you want.
You don't even know about all of these things.
So you might just pay or not pay a transaction fee.
And that was one of the questions, but in general, you don't even actually touch these concepts as a user.

Christoph Ono: 00:45:03

Ideally.
That's why we need wallets to be really smart for people.
So wallets can just notify people and says, "Hey, there are some old reserves that we just can't make a connection anymore, or liquidity is low, I prepared something for you."
If you want to, you can just enable that real quick and you're good to go.
All of this stuff is ideally automated and intelligent.
We are here to design this, and implement it, and make it happen, work with the developers and all that.

Michael Hasse: 00:45:35

Yeah.
One of these use cases that I thought about that we didn't discuss yet is, is an escrow address or an escrow wallet where all the parties have to preemptively inspect the address whether it actually matches what they agreed on.
So far we talked whether I can spend something or not, but this would be something where I would have to know beforehand, if funds are deposited into that address if that still works as intended per our agreement.
That's probably for another call since we have like five minutes left.

Christoph Ono: 00:46:30

Yeah, I think it would be cool, as a follow ups to these understand calls, just do a bunch of jam sessions and just design these UIs.
Just feel out what these could actually be like and what we need.
When I generate an address, do I need this whole rule builder thing now?
When I paste in an address, do I need to have an option?
If someone gave me a rule for this address, can you just verify that?
And then what does that look like?
That's why I think would be really interesting to figure out how you would actually interact with this stuff.

Michael Hasse: 00:47:19

Some kind of visualizer.
I was thinking about this with Miniscript descriptors, wallet descriptors, because they are very long, right?
You have a 2 of 3, after six months, it's a 1 of 3, after another six months, a fourth key gets activated, and you need to visually see this, not just the string of 9,000 characters, but they would need to visualize that to actually reason about it.

Joaquin: 00:47:55

I'm a little late to the party.
I'm sorry.
But is that's what happens?
As time increases more can get added to it?

Michael Hasse: 00:48:07

No it's a different discussion from covenants.
You can do this with Miniscript wallets already, but you can say, I have a 2 of 3 multi-sig, but after six months, I want this threshold to be lowered to 1 of 3.

Joaquin: 00:48:32

You set that up in advance?

Michael Hasse: 00:48:34

You set that up in advance while you set up the wallet.
But then when you import it somewhere else, you want to verify that it actually does what I think it does.
Currently the only way to do that is you have a string of text.
There's no way for normal people to actually know what it does.
A visualizer or visualization pattern templates tool for these kinds of things, it's probably might be even more needed for something like escrow addresses and escrow wallets because you want to inspect the contract before you enter into it or deposit money into it.

Christoph Ono: 00:49:22

Design huddle of covenants!
My brain is getting pretty fried here.

## Wrap Up

Michael Hasse: 00:49:31

I think it's a good time to call it a covenant day and continue next week or a week after that.

Christoph Ono: 00:49:45

Do you feel like we need another learning session on this one, or do you feel like we've tapped out a good amount of the use cases and ideas?

Michael Hasse: 00:49:56

We could maybe do an iteration with Owen based on this call where we basically were guessing on our own, and maybe take this one of these use cases and go through just with one thing.

Christoph Ono: 00:50:16

Do you know that saying - the best way to find out how to do something is to do it wrong and show it to people.
There's something like that.
Just curious if you should just design a bunch of stuff where we're like, it's probably something like that.
And then you know, that will trigger some responses quickly.

Michael Hasse: 00:50:44

Yeah, basically that's describing my entire high school and academic career (laughter).
Yeah, let's do it.

## Oracles

Joaquin: 00:50:57

Real quick, I know everybody's brain is fried, but is there any oracles on Bitcoin?
And the oracles, do they dovetail with covenants at all?

Christoph Ono: 00:51:10

How much do you know about oracles?

Joaquin: 00:51:12

I mean just that they receive data from the real world and then link to the blockchain somehow.

Christoph Ono: 00:51:21

Yeah.
So my understanding is just exactly that.
It's like a connection between the real world and the blockchain.
If something gets evaluated, how do you get the current price of a euro, how do you get the temperature, if there's a betting thing how do you get the end result of some soccer game, how do you get that in there?
So I feel like it's just basically just a fancy word for an API call.
So I guess a price API and you just at some point you're like, "okay, API, what's the what's the price or value?".
Yeah, right.
Thanks for joining.

Joaquin: 00:52:01

The trusted nature of it, I guess, becomes like a sticking point, I guess.

Christoph Ono: 00:52:05

Yeah.
So I don't know, I feel like there's no such thing as an on-chain Oracle.
I feel like some of it is just kind of a big hype and whatnot.
So I don't know.
That's that's my understanding.
So it's a source of data.
You have to trust it and make sure you can rely on it.

Joaquin: 00:52:30

Right.
Now, the only reason I brought it up was there's this thing called a Tongue Teen I think, where people join a group and then whoever's the last person that died gets the money.
So that's always what came to mind when I was thinking about Oracle, I think it's from an old Simpsons episode.

Christoph Ono: 00:52:55

Yeah.
Especially with betting and some of this stuff.
People seem to love betting markets, it seems to be just kind of thing a lot of people like that's where that always comes in.
Or also these price feeds for stabilizing Bitcoin value, if you want to have some synthetic dollar or euro you at some point need to know what that value is.
That's where you need an oracle.
It sounds magical and stuff, but it's just a data feed.

Joaquin: 00:53:31

Right, right.

Christoph Ono: 00:53:37

Cool.
My brain's fine.

Mogashni: 00:53:41

I zoned out for a bit, I was continuing with my design because I'm just done.

Christoph Ono: 00:53:47

Cool let's stop the recording then, if anyone watching thanks for tuning in.

Mogashni: 00:53:51

Thank you.
