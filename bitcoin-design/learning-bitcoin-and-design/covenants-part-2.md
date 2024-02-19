---
title: "Covenants Part 2"
transcript_by: varmur via review.btctranscripts.com
media: https://www.youtube.com/watch?v=zk_EEKeAFuY
tags: ["covenants","ux"]
speakers: ["Christoph Ono","Michael Haase","Mogashni"]
date: 2024-02-02
---
Speaker 0: 00:00:01

All right, welcome to our second learning Bitcoin and design call about covenants.
So today, I think the idea was to go deeper into covenants use cases, right?
Last time, the first call was more about just generally what it is and what it does.
And then now we wanted to go deeper.
And I think on the web, on the GitHub issue, there was one request about congestion control.
And then the, but the other big one was scaling I think so but how's everyone how are you feeling about covenants today maybe we should just pick up I don't know wherever our brains are well so I'm feeling bullish on covenants okay no but it's it's that I would personally probably want to have a look at.

Speaker 1: 00:01:04

I think it opens up a they open up a kind of fascinating capabilities that I would personally probably want but in terms of whether what the let's say the technical soundness or the security implications there's nothing I can contribute and but in general I'm kind of more probably interested in these kind of bolting or kind of scripting stuff than scaling.
But that's just the nature of what I'm working on currently.
So that's not at all some kind of judgment or so.
But it's just in terms of the scaling question I'm not sure how valid any of the things that I'm gonna say or I have to say or think is relevant But it's really interesting and what stuck from the last call was I think Owen said you can, in terms of scaling, You can transfer ownership without on-chain transactions and have the same assurances.
So that's definitely something interesting.

Speaker 0: 00:02:45

So, yeah.
So Owen's threads here, he has three threads.
They're really awesome.
I tried to earlier, I tried to sit down and actually understand that specific part.
I tried to understand how does this enable any sort of scaling and how do you transfer ownership off chain?
And there's this one thread here that talks about, I don't think it's this one actually, where it's something, on the one hand, it kind of makes sense, but I was missing, there was something I was missing from it too and let me maybe I'll maybe I'll try to explain and try to get there there was one thread with an example that I thought was pretty good.
So here's kind of what I came up with, which kind of helps maybe with the scaling stuff.
So, and I tried to create a very simple example of this.
So there are three people, Alice, Robert, and Charles, right?
Robert owes Alice 1.01 Bitcoin and Charles owes Robert 0.2 Bitcoin.
So what they would do right now is Robert sends Alice 1.01 Bitcoin and Charles sends Robert 0.2 Bitcoin.
Two transactions done.
Cool.
Now let's make this way more complicated.
So, but Alice gives Robert the address, like Alice's address one.
Cool.
So Robert could technically now just send her zero point Bitcoin and be done, But he makes it more difficult.
So he creates his own address because he's expecting money from Charles.
I think this needs to be Charles, right?
Charles needs to send him money.
So Robert creates an address, Robert's address one, and that one has rules baked into.
So any funds that go into this address, 0.1 of that has to go to Alice's address, right?
So when he receives zero, whatever he receives, 0.1 is reserved for Alice and no one will ever be able to change that.
That's just how it is.
It cannot be used anywhere else.
And then rule number two is that another 0.1 should go towards a lightning channel with Dan.
So those are rules baked into, right?
And then in this address, then Robert gives this address to Charles.
Charles puts the 0.2 Bitcoin in.
Now we have this Robert's address with 0.2 Bitcoin.
And those address cannot be freely spent right.
0.1 has to go to Alice and 0.1 has to go to this lightning journal with Dan.
That's it.
So but only Robert knows this because he baked this into the address.
No one else knows about this, right?
On the blockchain, it's like, hey, there's an address with 0.2 Bitcoin.
Cool.
That's it.
But so Roberts tells Alice, hey, look at this address.
There's a rule baked into into this one.
So Alice looks at the address and she's like, cool, that is true.
There's 0.1 Bitcoin in your address.
But at some point, they can only be spent to me.
So, right, you, Robert still has them.
But the only thing that can be done with them is to give them to me.
Is that as good as me having them?
You could say yes.
Like there's a promise in there that cannot be broken.
So Alice now says, cool, they're not technically in my address, but they kind of have to go there.
So it's like they're mine, but they're not really, you know, they are and they aren't, Schrodinger's cat or whatever.
And then Robert tells, shows Dan the address and the rule number two and then you can open up a lightning channel with them and because even right because there's this promise that cannot be changed so in a way we've like there's was one transaction that happened.
So Charles sends those 0.2 Bitcoin.
But actually we did three, we accomplished three things at the same time.
So literally on the blockchain 0.2 were sent from Charles to Robert.
So that debt is kind of settled.
And then there are these baked in promises that 0.1 will go to Alice and another 0.1 will go to the lightning channel with Robert and Deb.
So without covenants, it would be three different things with convenance they're one.

Speaker 1: 00:07:35

Plus Alice since Alice probably gave I mean it depends on what kind of address Alice gave to Robert.

Speaker 2: 00:07:56

So if that's a normal kind of address, she can then spend this point zero one, point one freely as well.

Speaker 1: 00:08:10

Right.
So yeah, basically, basically you can then you could basically change transactions on onto this.

Speaker 0: 00:08:19

Yeah.
You're basically unwinding a bunch of stuff then like you're winding up things right or you bake in all these promises.
But then, then you can build promises and promises and promises and promises.
But then the question is then and that's something Owen also wrote in his thread.
It's like can you do that forever or does at some point this whole thing just kind of have to you know unwind.

Speaker 1: 00:08:43

I think this is what he meant with the trees of trees of trees right with this kind of layers of trees.
It always depends what the next hop is going to do.

Speaker 0: 00:08:56

And your point was this Alice's address it could also hold promises to other people.
Exactly.
Maybe she wanted to...

Speaker 1: 00:09:05

Exactly.
And that's also something that nobody else knows.

Speaker 0: 00:09:10

Yeah.
So I think it's like if, but the thing is, if Robert forgets the rules, then no one can recover them.
No one will know them.
Right.
Because they're not saved anywhere on chain it's they only exist because he baked them in and if he forgets them then it doesn't share then they're gone.
So I guess that's where I have a whole bunch of questions about how can all of this fall apart if someone forgets something, right?
And then all this stuff gets locked or is there always a way out to unwind it where anyone can just back out of this whole system, screw it, I don't like these shenanigans.
And if let's say you do that three times in a row and I want to, I'm secretly paying Mo and I'm like yeah you know these Bitcoin they're actually yours but really they're in Michael's address and you have with this rule but then they're in Loic's address in this rule and he paid me before and with that rule and then they're actually Bitcoin that my mom sent four years ago with that other rule and then it came over there.
It's like do I need to do all that stuff or do I not or like how do I prove them that and will you accept it when you're like this is way too complicated for me just give me my money.

Speaker 1: 00:10:35

Well the way that I understood it is the I mean all of these checks are automated in the background right so the address that I give you is only spendable by my rules or if you receive something into this address then I have the assurance that I can spend it the way I want to spend them.
And that's all of these rule checking that you just described.
And that's how I understood it, that it works.

Speaker 3: 00:11:15

No, when we speak about use cases, and I'm just thinking about the scenario that Christophe presented.
I personally would never enter into such a scenario because there's just too much of he said, she said, I promise you promise he promises they promise.
If I would think of a very practical use case, I would just think of a family using it between three people, the husband and then the wife and then the kid.
The kid has their own Bitcoin savings for their university or whatever they want to study for and then the couple has an account and it's a joint Bitcoin account and both of them are in Bitcoin and every time money comes in they both agree that there's a rule that 5% of that goes to the kids university fund.
It's a covenant between them.
And then it's safe.
It's trusted.
It's the husband and the wife.
There's no more.
There's not too many people making promises.
And then maybe between the husband and wife, they have their own covenant, which is like, OK, certain percentages, 10% goes for a holiday and then that is that own covenant.
I mean, I'm just trying to think of a very practical use case in a situation which I think would practically work.
But I think the more people you add on to this I promise he promises she promised a problem.

Speaker 0: 00:12:37

But so the trick is you might not even know because on chain these addresses look like regular addresses there might be all kinds of stuff in but you just can't see it.

Speaker 1: 00:12:47

So that's the part which part of this construct is conscious and which not, right?
Because I just want to send you money and the only thing that I have to know and you have to know is that I can spend that money and it goes to you and then you can spend it freely afterwards.
So that means consciously we don't even need to know it.
It doesn't concern us.
This huge construct doesn't concern us.
The only thing that we need to know is that we can spend that money.
And So this is not a kind of an attempt to set up this big construct because nobody has a use case like that.
It's just that we need to have the assurances that whatever we want to do with the money can be done.
So I think we have to separate the part that is kind of for each person in that line of succession.
The only thing they need to know is they can spend the way they want to spend.
Yeah, it's true.
Automated basically, nobody at the beginning, if I'm in the middle of this of this whole sequence I don't need to know what's before it and I also don't need to know what's after it right so I just need to know that that whatever comes into this address can be spent the way I want.
That's it.

Speaker 0: 00:14:39

Yeah.
And it's true, Mo, you define your own rules because it's your address.
So no one can force rules on you really.

Speaker 1: 00:14:49

So you're not part of some kind of bigger scheme, but you're just receiving and sending.
Everything that we talked about is basically happening in the background and it shouldn't even really...

Speaker 3: 00:15:06

Right, the protocol is making sure that all of those conditions are met.

Speaker 1: 00:15:10

Exactly, but you should be able to say okay now I received like this 0.1 Bitcoin and then I want, because these are mine and I want to spend them I want to automatically put I don't know I want to put 10% of that into my savings wallet yeah And the rest I just send to people.
So these are then your rules, right?
So that and everything, it's basically one up after that.
And the question that Christoph raises, does it break at some point?
Right?
Or is it the can you do this forever?

Speaker 3: 00:15:55

Good question.

Speaker 0: 00:15:58

I guess you know I'm not to continue on that thought I'm not sure what I said was actually right that no one can force things on you.
So here, you know, Robert shares tells Alice, hey, look at this address.
There are funds in there for you.
But they're not detect that.
How can she already sent them to someone else?

Speaker 1: 00:16:25

No, I mean that the point is it has to be funds have to be sent to the address that Alice gave him.
So, and then Alice has enough assurances because she constructed the address and the address contains the spending conditions or the policy.
So that means once the funds hit her address, she knows that she can spend them.

Speaker 0: 00:16:59

So I think that the way that Owen put it was there's like a PSPT in there.
So, Robert really doesn't have to pay any fees there, but eventually Alice will have to.
So, let's say fees are 200 bucks, right?
And I'm like, check Alice, you're at the 100 bucks I'm supposed to send you.
They're right there.
You can grab them.
But, you know, then she has to pay the fees instead of he being the sender who puts it in her address for paying the fees.
He kind of gets around the fees and kind of puts that on her in a way right because it's almost like she has to withdraw them Or is it if it's a PSPT?
I don't know if it's a fully signed transaction baked in, then I guess it's still on him.
Or is it on?
I guess who pays the fees then in that regard?
How does that trickle back?

Speaker 3: 00:18:04

I'm trying to see what Bitcoin technical search is going to provide.
I actually said, how do fees with covenants work?
I'm just reading through whatever's coming up here.

Speaker 0: 00:18:13

Maybe no one even knows.

Speaker 3: 00:18:15

There is no direct article about it.

Speaker 0: 00:18:20

So here's another one if you're cool with looking at something else.
I was trying to figure out how payment pools work, which are also supposed to be this technique.
So basically, Robert, Alice and Charles, we want to create a payment pool.
So we we collaboratively create an address that has some rules that we put stuff in.
So on chain, there's an address with funds in it.
That's all people see.
But baked into this, there are a few rules.
So Robert puts 0.1 Bitcoin in Alice 0.2 and Charles 0.3. And then the rules that say this is how much everyone else.
So each of those, there are rules that each of them can exit this arrangement and they just get the 0.1 back.
Then there's another rule that if all of them agree the funds can be split up differently.
So Robert can get it all and Alice nothing or Alice can get 0.4 and the others 0.1 whatever it is like they can they can exit with a different arrangement.
So that basically means between the three of them there's now these funds.
It's a little bit like lightning, lightning, right?
You have these funds locked up between the three of them and then it's just like split wise one day one person pays for lunch they're like okay cool I'm keeping track that you know I owe you this much and then they do something else and then at some point they can just settle the whole thing and collapse it into one on chain transaction.
It's a bit like split wise and all that.
So yeah they pay Jill a bunch of times one year later Alex says screw you guys I'm done with this let's settle.
So cool so that's It seems like an overly complicated way of doing things for three friends that can just talk to each other and actually use splitwise.
Right.
Why go through all these shenanigans.
So that's why I put this thing here.
Well, where is this useful?
Is it useful in, let's say there are three companies or banks across countries that need to settle between them regularly or where there's not such a trusted scenario.
Then the other thing in the examples was that, well, someone can exit from a pool and the others can continue in the same pool or they can spend and split up and go into another pool.
And then it's like, awesome, cool.
But what do you, like, that was one of the things that I read it's like you can have pools and pools and pools and they're all linked and I thought I don't get it what's the like what are you actually achieving here that doesn't seem and then who tracks all of this stuff right so I don't know that was my it was so hard my insight into payment pools and I don't I feel like I'm missing something still, but I also didn't spend a ton of time on it.
So I don't know.

Speaker 3: 00:21:30

So is there, there's, this is a protocol layer thing that makes it that make sure that these agreements are met and then it makes sure that everything goes on agreement underneath the hood.
So it isn't, it is a protocol layer that will continuously be worked on so that the rules are constantly updated according to the needs of the network.
I mean, this is just the thing that I'm trying to understand as well.
Like, is there one dedicated developer now working on Covenants or how is it like?

Speaker 0: 00:22:04

I gotcha.
So, you know, what all of this stuff, both examples here, they're based on the same thing, that you can bake rules into addresses that no one can change.
And then everyone has to follow that it's it's actually a somewhat simple idea right just how those what can be done with the Bitcoin in in the in that are deposit put in this address and this as far as I know this idea has been around for a very long time.
And there are, if you go to what's the covenants info, let me switch over real quick.

Speaker 3: 00:22:44

Yeah, 2016.
I see one of the first talks given about it.

Speaker 0: 00:22:49

Yeah, coming inside info.
So there are 123456789 different.
Hey, working there nine different proposals around there.
And from the Stefan Levere podcast, they had their their have various different technical complexities.
So generally people want the simplest version because there's the lowest risk that anything can break.
It's easiest to reason about.
And each technique solution has kind of, it allows you to do things slightly differently, right?
And it's important to think through how these differences could play out over time and what they could lead to.
So yeah, that's why nothing's been...
And then there are these different use cases and stuff.
And some is more, you know, not spectacular.
What is it called?
Speculative than others.
So yeah, no one's decided on anything.
It does feel like a whole bunch of people really want this to happen and others say well there's no real urgent need we have other problems and other things to figure out so yeah and there's also seems to be some confusion right now about how you actually make change to Bitcoin.

Speaker 2: 00:24:14

Yeah so from And I think that's also why Owen focused on CTV, which is one version of implementation, version of what Christoph just mentioned, Because that seems to be the most widely kind of accepted one and best studied.

Speaker 1: 00:24:40

But yeah, I mean, every, any kind of assessment of viability is far beyond my.

Speaker 0: 00:24:52

And so the, Are you there, Michael?

Speaker 1: 00:24:56

I'm here.
Okay.

Speaker 0: 00:24:58

Yeah.
Sorry, it just froze for me for a little bit.
One extra thing was that, you know, it's not like these things are just get discussed and then someone decides and then they get implemented.
Some of these things have been implemented on test net or rec test or maybe even on other chains.
So you can kind of see in practice how they pan out.
I feel like liquid even had something like that for some.
So there are these practical explorations that take you to a certain point.
But the other bar is just really, really high for any of this.

Speaker 1: 00:25:34

Yeah.
And you, and then you have the concern or people, I mean, if you, let's say, if we say, if we take this scaling example, what kind of impact does this have on miners who actually secure the network?
It could collapse their income basically.
What's the kind of the impacts of that?
I don't know because if you can collapse 10 transactions into one, then obviously there is an economic impact.
So that's why it's also maybe taking apart from the security concerns that's another thing to consider.

Speaker 0: 00:26:17

You know, maybe the Bitcoin network in the future, all of the actual transactions will just be really cheap.
And we just live off of the money from art collectors and all the JPEGs. It's just art funding.
Yeah.

Speaker 3: 00:26:35

So apparently there's also some people also write white papers, well not white papers, but they write there's something called vaults and covenants as well.
And in this paper we examine how they might be implemented.
Okay, that new approach is presented, which avoids pitfalls of general covenant proposals.
So as Christoph said, there's many different covenant proposals.
And then each proposal has its own pitfalls.

Speaker 0: 00:27:03

And vaults, I don't know, I feel like vaults are more of an implementation or a use case for covenants.

Speaker 1: 00:27:10

Exactly.
A use case for covenants.
Yeah.
Like scaling is a use case.
And that's why, or one of the one of the things that kind of because covenants take so long.
That's why in recent in the last maybe 12 months, the interest in Miniscript picked up, or 18 months, picked up significantly because you can actually program similar or not quite as sophisticated stuff like with governance but you can achieve some kind of programmability with miniscript already, right, with what we have now.
And so that's kind of the dynamic.
Basically, Covenants would take that programmability to the next level, definitely.

Speaker 3: 00:28:17

So chat PDF to the rescue.
I downloaded that white paper.
It's called Vaults and Covenants.
It's 13 pages, published 9 January 2023.
And I uploaded the chat PDF and I asked how how vaults are related to covenants and basically it's a storage mechanism so it's something yeah it's more for more security but yeah there's a 13 page article on vaults and covenants if you'd like to read it.
Vaults are a technique for substantially reducing the risk of Bitcoin theft.
They are a form of covenant that give Bitcoin users operational simplicity but heightened security.

Speaker 1: 00:29:03

I mean this definition of a vault, I mean it really depends on what you, this is a technical description of the implementation of vaults but you can also understand a vault just as an applicant you can You can create a vault from a different type of covenant proposal, right?
So it's, I have a hard time to actually, I see a vault as an object and not as an implementation.
A feature.
A feature, exactly.
A feature or a use case.
Yeah.
Vault is a use case, but for me, and I'm a technical layman, but I have the feeling it's more helpful to think of Vaults as the feature or the thing that you want to achieve rather than the way of achieving it.

Speaker 0: 00:30:17

By the way, did you see Owen's Figma prototype?
No. Do you want to look at that one or do you want to continue with the vault?

Speaker 3: 00:30:27

No, let's see the prototype.
I mean, I'm keen on seeing it.
If anyone else is open to as well.

Speaker 0: 00:30:35

I'll share that link.
I think my link here.
So he he he mocked up the idea of cold channels.
So that's what what earlier in the example I think what is it Alice, Robert, whoever said well part of this deposit is dedicated to a lightning channel, right?
So that lightning channel is not technically active.
There are no nodes talking to each other and stuff but the funds are dedicated to it right it's just kind of like secretly committed to this lightning channel and so typically you do need to create a new on-chain transaction to get funds into that state but here you kind of have that automatically.
So it saves you a transaction and you kind of have this secret what he calls cold channels or in this case reserves.
So let's say you're in Phoenix here and someone sent you 0.1 Bitcoin or whatever and you've created an on-chain address with this cold channel option.
So then that would go into what he calls reserves.
So here you would in this example the balance is 433,000 sets plus 1.3 million in reserves.
So that means if he ever runs low on liquidity, he could activate his reserves, activate these cold channels for free, I think.
So what can I click here?
So I can receive.
Now here, let me get my head out of the way.
So here you can see that I can choose between regular addresses or what he calls simple address and cold channel addresses.
So it looks pretty much like a regular address, but anything received to that has the cold channel option.
And then I want more liquidity and then I can see, you know, here are all these different deposits that I can activate.
And then I activate one, I confirm it, cool, sweet.
I have now 300,000 more sets that I can spend on lightning basically for free and right an instant I think I think the there just needs to be this connection needs to be established with the other node.
But because on-chain transactions taken care of already, you save those 10 minutes or that block confirmation.
Yeah.
How does that sound?

Speaker 2: 00:33:49

It's saving just a transaction fee in the future.

Speaker 0: 00:33:58

Sorry, what was the first thing that you read?
I didn't quite catch where that came from.

Speaker 2: 00:34:02

Oh, it's it was the final page in this little prototype.

Speaker 0: 00:34:06

Oh, OK.
Let me let me take a look at that one.
Where is it?
Under receive or how do I get there?

Speaker 2: 00:34:15

Oh, just keep clicking.
Oh, it's.
After it says activate this reserve, activate now one page back after that.
Oh,

Speaker 0: 00:34:30

okay.
Here at the bottom.

Speaker 2: 00:34:31

Yeah.
Yeah.
Oh no, not that page.
One, try going one more.

Speaker 0: 00:34:40

Oops.
Maybe back.
Back.
There's no back here anymore.

Speaker 2: 00:34:50

OK, well, sorry, let me see maybe under receive.
It was activate reserves.
It was starting out 1234.
It was the fourth screen.
Oh, I was just clicking on clicking along the bottom navigator.
I wasn't using the prototyping.

Speaker 0: 00:35:15

Oh, okay.

Speaker 2: 00:35:16

Yeah, sorry.

Speaker 0: 00:35:18

Oh, this one the receive with the payment tree leaf.
Yeah, that's a that's a whole different thing.
That's not the cold.

Speaker 2: 00:35:27

No, no, it wasn't.
That's fine.
I'm, it was just a general definition of what was going on and I was just trying to get my head around the what exactly was going on.

Speaker 0: 00:35:39

Yeah I mean so the way it typically works is that you receive funds in your address and then when you want to open a lightning channel that is another transaction.

Speaker 2: 00:35:48

Right.

Speaker 0: 00:35:48

That takes 10 minutes to confirm.
And yeah, that's basically you have to pay another fee takes 10 minutes.
But with with you can kind of collapse this into one using covenants.
So you have you get these funds and it's like they're they're just primed for a lightning channel.
They're not the light channel is not active, but it's all ready for it.
It's all set up.
So you don't need to wait another 10 minutes you don't need to pay the extra fee so you just need to say let's go and the channels right there but you don't know you don't have to write it's like an option a free option to have a lightning channel right and that's through governance yeah so it's kind of cool you could also just You could just also send it as a normal on-chain transaction.
You can either use it as a regular on-chain transaction or as a Lightning channel.
It's up to you.
There may or may not be a delay in there.
That's something that I wasn't quite clear on.
Because if let's say I promise that I think channel on the one hand, and then I have the option to spend it in another way.
You know, how, how is that?
How do I prevent, you know, some scamming there, if there's not a time lock or some other mechanism that people can hold me accountable for it.
That's one thing I wasn't quite sure on.
But then this is the basic idea.
And I really liked how Owen mocked this up.
It's very, very in your face.
It explains a lot.
I don't know if we need all that in the future.
But I think that's a really good way to start this.
To put it in a UI.
Okay, well, what are your questions?

Speaker 3: 00:37:38

Now I was clicking around on the prototype and just trying to actually understand.
So we discussed a bit of how it works, like what a covenant is.
So I'm trying to click through the UI and try to get this theory that I have in my brain and see how that's making sense on the actual design.
So these sort of, if I'm understanding correctly, the reserves are actually the agreements or rather the covenants that I have with other people is that correct?
Or?
Yeah.

Speaker 0: 00:38:15

So you are?

Speaker 3: 00:38:17

That's how I'm understanding it.

Speaker 0: 00:38:23

So you're Robert here.
You created an address.
And there was a rule baked in there that some of this can go to a lightning channel with a specific person.
But you made this commitment.
So that's baked into the address.
And that's why other people can trust, right?
You're good for this.
You've committed your funds.

Speaker 3: 00:38:49

Yeah.
And that's the fund that's called the reserve in this UI, in this design that we, like this one here, this is that reserve bit, is this bit here, that's this, like I have an agreement between me and John that he gives me 1% and you can count on this 1% it's here and then I have another agreement with Mary and this is the agreement I have with her.
So if I want to, I can use this because it is my stats.
I just activate it and then I can use it in my transactions.

Speaker 0: 00:39:30

Yeah, you just activated a channel, a channel that was very well prepared, but was not quite active.
And,
you know, you, the terminology, of course, is something that that may or may not change.
He uses the term cold channels in here, and reserves.
And, you know, but then the it's obviously a new term.
So no one knows really what it means unless you actually worked on it.
So that all of this stuff is usual, you know, communication stuff.

Speaker 1: 00:40:01

Yes.
So in this case, all of these code channels together are the reserves, right?
Yeah.
And the covenant is just basically a rule or a smart contract or kind of it's a I mean even even a normal single SIG or a multi-SIG address are a covenant or a type of covenant because they define how funds can be spent from that address.
So it's a bit kind of confusing discussion because it's just it's kind of the concept of covenants it's just about enhancing the programmability of the existing system right And you can do that in a bunch of different ways.
And all these covenant proposals are each a different way of enhancing or implementing this.
But a covenant is just a bunch of rules.

Speaker 3: 00:41:27

If I understand this correctly, then I actually entered into, would you say, so then I entered into a covenant with this person over here on the 12th of July and now I'm trying to activate this covenant but this person set a rule, well this is not a rule, this is that because the channel partners are responsive but this could be like a notification that would pop up to say that this this person who you entered into a covenant with yeah this these this is only available in four weeks or something like this.
Does that make sense what I just said?

Speaker 0: 00:42:04

Yeah.
So the way it works here is that this other person doesn't even know that you want to have this channel with them.
You haven't revealed that yet.
So you banked into your address.
You said, I want to have the option for these funds to have a lightning channel with Michael but I'm not gonna tell him right I'm just gonna bake that in and then at some point when you say well I want to I want to get that finally it's time I want this lightning channel with Michael.
But maybe Michael's notice just not online right now.
Then you just can't make that connection.
But he's just not his phone, his computer, his notes down, whatever.
Maybe he got a new wallet or changed his notes or whatever it is.
If you wait it like six months, then maybe it's just not that connection cannot be made anymore.
So and that's why that's why this might might fail.
But you always have the option to just okay, cool, leave the funds there or just put it onto another address and you know, that just that's just not going to happen that lightning channel.

Speaker 3: 00:43:09

Interesting.
I'm just from the from the UI here as well.
It's like, I don't know what I clicked on enter on enter an on chain address receive the withdrawn funds.
So now it's working that the technical problem doesn't exist now.

Speaker 0: 00:43:23

No, no, no, it is exist.
You're just taking the other route.
You're kind of giving up on this channel with Michael and you're just putting the funds somewhere else because you just don't want that.
That reserve is useless to you.
Michael's just, it's not going to work out.
You give up.
So you're just like, okay, I'm going to put the funds in my cold wallet or I'm going to pay rent or something.
Just going to do something else with it.

Speaker 3: 00:43:45

Okay.
Okay.
All right.
Wow.

Speaker 1: 00:43:49

You know, if you think that lightning channels, this is like, whoa, whoa, whoa, you know, goodness, from a from a from a UX perspective is actually I don't do much different than I do today.
All these kind of discussions are about the logic that happens in the background.
So once you give me an address and I send funds to that address, whether it be an on-chain transaction or kind of like a covenant enabled promise, then you know you can spend and you can do whatever you want.
You don't even know about all of these things.
So, yeah, you might just pay or not pay a transaction fee.
And that was one of the questions.
But what idea or in general, you don't even actually touch these concepts as a user.

Speaker 0: 00:45:03

Ideally.
And that's why we need wallets to be really smart for people.
So wallets can just notify people and says, hey, there are some old reserves that are we just can't make a connection anymore or a liquidity is low.
I prepared something for you.
If you want to, you can just enable that real quick and you're good to go.
You know, all of this stuff is ideally automated and intelligent.
And we are here to design this and implement it and make it happen, work with the developers and all that.

Speaker 1: 00:45:35

Yeah.
One of these use cases that I thought about that we didn't discuss yet is, or something like it is kind of an escrow address or an escrow wallet where all the parties have to preemptively inspect the address whether it actually matches what they agreed on.
I mean so far we talk whether I can spend something or not but this would be something where I would have to know beforehand if funds are deposited into that address if that still works as intended per our agreement.
And that's probably for another call since we have like five minutes left.

Speaker 0: 00:46:30

Yeah, I think it would be cool to as a follow ups to these understand calls, just to a bunch of jam sessions and just design these UIs. And just just feel out what this could would actually be like and what we need.
When I generate an address, do I need this whole rule builder thing now?
When I paste in an address, do I need to have an option?
It's like someone gave me a rule for this address.
Can you just verify?
And then what does that look like?
And if I have my transaction list and it's like, I don't know, it feels like that's why I think would be really interesting to figure out how you would actually interact with this stuff.

Speaker 1: 00:47:19

Some kind of visualizer.
I was thinking about this with manuscript descriptors, wallet descriptors, because they are like this long, right?
If you have like, you have a two or three, after six months, it's a one or three, after another six months, a fourth key gets activated and you need some actually somebody would need to visually see not just the string of like 9,000 characters to, but they would need to kind of visualize that in to actually reason about it.

Speaker 2: 00:47:55

So it's something I'm a little late to the party.
I'm sorry.
But as that's what happens as time increases more can you get added to it?

Speaker 1: 00:48:07

No that's just that's a it's a different discussion from from from covenants but in order to be you can do this with manuscript wallets already, but you can say, so I say I have a two or three multi-sig, but after six months, I want to have this to be the threshold to be lowered to one of three.

Speaker 2: 00:48:32

You set that up in advance?

Speaker 1: 00:48:34

You set that up in advance and you set up while you set up the wallet.
But then when you import it somewhere else, you want to you want to verify that it actually does what I think it does.
And currently the only way to do that is you have a string of text.
There's no way for normal people to actually know what it does.
And kind of a visualizer or visualization pattern templates tool for these kinds of things.
It's probably might be even more needed for something like escrow addresses and escrow wallets because you want to inspect the contract before you enter into it or deposit money into it.

Speaker 0: 00:49:22

Design huddle of Covenants.
My brain is getting pretty fried here.

Speaker 1: 00:49:31

I think it's a good time to call it a covenant day and continue next week or a week after that.
I mean,

Speaker 0: 00:49:45

do you feel like we need another learning session on this one or do you feel like we've kind of tapped out a good amount of the use cases and ideas?

Speaker 1: 00:49:56

We could maybe do an iteration with Owen based on this call where we basically were guessing on our own and maybe take this one of these use cases and go through just with one thing.

Speaker 0: 00:50:16

Do you know that saying that the best way to get something validated is or the best way to find out how to do something is to do it wrong and show it to people.
There's something like that.
Just curious if you should just design a bunch of stuff where we're like, it's probably something like that.
And then you know, that will trigger some responses quickly.

Speaker 1: 00:50:44

Yeah, that was that was basically that's describing my entire high school and academic career.
Yeah, let's do it.

Speaker 2: 00:50:57

Real quick, I know everybody's brain fried, but is the oracles, is there any oracles on Bitcoin?
And the oracles, do they dovetail with covenants at all?

Speaker 0: 00:51:10

How much do you know about oracles?

Speaker 2: 00:51:12

I mean just they're kind of, you know, receive data from the real world and then link to the blockchain somehow.

Speaker 0: 00:51:21

Yeah.
So my understanding is just exactly that.
It's like a connection between the real world and the blockchain.
If something gets evaluated, how do you get the current price of a euro how do you get the temperature how do you get you know like if there's a betting thing how do you get the end result of some soccer game or something how do you get that in there So I feel like it's just basically just a fancy word for an API call.
Right.
So I guess a price API and you just at some point you're like, okay, API, what's the what's the price or value?
Yeah, right.
Thanks for joining.

Speaker 2: 00:52:01

The trusted nature of it, I guess, becomes like a sticking point, I guess.

Speaker 0: 00:52:05

Yeah.
Yeah.
So I don't know I feel like there's there's no such thing as an on chain Oracle and all of this stuff and I feel like some of it is just kind of a big hype and whatnot.
So I don't know.
That's that's my understanding.
So it's a source of data.
You have to trust it and make sure you can rely on it.

Speaker 2: 00:52:30

Right.
Now, the only reason I brought it up was there's this thing called a Tongue Teen I think where people join a group and then whoever's the last person that died gets the money.
So that's always what came to mind when I was thinking about Oracle.
So I think it's from an old Simpsons episode.

Speaker 0: 00:52:55

Yeah.
Yeah.
Especially with betting and some of this stuff.
People seem to love betting markets.
It seems to be just kind of thing a lot of people like that's where that always comes in.
Or also these price feeds for like, let's say, actually for stabilizing Bitcoin value that page if you want to have some synthetic dollar or euro or so you at some point you kind of need to know what that value is.
That's where you need an oracle.
But it's I mean, it sounds like magical and stuff, but it's just like a data feed.

Speaker 2: 00:53:31

Right?
Right.

Speaker 0: 00:53:37

Cool.
My brain's fine.

Speaker 3: 00:53:41

I was out for a bit I was continuing with my design design because I'm just done.

Speaker 0: 00:53:47

Cool let's stop the recording then if anyone watching thanks for tuning in.

Speaker 3: 00:53:51

Thank you.
