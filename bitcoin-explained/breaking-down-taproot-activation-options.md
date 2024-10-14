---
title: Breaking Down Taproot Activation Options
transcript_by: Sjors, edilmedeiros
media: https://www.youtube.com/watch?v=mT0t8Jm0m5E
tags:
  - bitcoin-core
  - taproot
  - soft-fork-activation
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
date: 2020-07-25
episode: 3
summary: This podcast episode delves into the nuances of Bitcoin soft fork activation, with a particular focus on the upcoming Taproot activation. Hosts Aaron van Wirdum and Sjors Provoost discuss the history and mechanisms of soft fork activation, including the challenges faced during previous activations such as SegWit. They explore different proposals for activating Taproot, weighing the merits and drawbacks of methods like BIP 9, BIP 91, BIP 148 (UASF), and the newer BIP 8. The discussion highlights the importance of achieving consensus within the community and the complexities involved in coordinating upgrades across the decentralized Bitcoin network. The episode concludes with considerations for future soft fork activations, emphasizing patience, thorough review, and the potential for innovative solutions like "sporks" to address these challenges
---
Aaron van Wirdum:

We're going to discuss Taproot activation, or more generally soft fork activation.

Sjors Provoost:

Yeah.

Aaron van Wirdum:

This has become a topic again in the sort of Bitcoin debate community public discourse.
How do we activate soft forks?
Because Taproot is getting to the point where it sort of ready to be deployed almost I think, so now the next question is, "Okay, how are we actually going to activate this?" This has been an issue in the past with several soft forks.
And it came up in the mailing list, I think a couple of months ago.
And now it's sort of reemerged, there's now a IRC channel where it's being debated, there's a Telegram's channel.
I wrote an article on it.
It's back on the death list.

Sjors Provoost:

Yeah, I read the whole IRC channel.
No, actually I started reading the IRC channel.
I got stuck at the meta discussion about whether or not there should be a Telegram channel and whether or not you need to ask permission.
And whether or not asking permission was off topic in the IRC channel.
And after an hour I gave up, but you spent your entire Saturday I believe?

Aaron van Wirdum:

I spent most of my Saturday reading through all of the logs and sort of trying to summarize it into an article.
I didn't read past Saturday, so if there was any sort of big discussion or development since Saturday, I might be out of the loop a little bit, but that wasn't really my impression.
I think I covered most of it.
So I think we can cover most of it in the podcast as well.

## Soft forks explained

Sjors Provoost:

So maybe we should say what a soft fork is.

Aaron van Wirdum:

Let's start there.
What is a soft fork Sjors?

Sjors Provoost:

So it's basically a tightening of the rules.
An analogy I like to make is with kosher food.
I've made this analogy three times today.

Aaron van Wirdum:

Yes, this is the first time you're making an analogy because we're recording this start of the podcast for the third time which is a pain, but let's just go on.

Sjors Provoost:

But basically kosher food is a subset of regular food.
So there's a few things you don't eat.
So often you might not notice it.
There's a lot of soft drinks that are kosher and you wouldn't know the difference.
But sometimes you would know the difference and that could be a problem.
But with Bitcoin, there is no such problem.
Because the things that are no longer allowed after soft fork are very stupid things.

Aaron van Wirdum:

Yeah, so hang on.
The thing you're saying is that soft fork is backwards compatible in the context of Bitcoin.
And the reason for that is like let's say I go to a restaurant every day because I love the food there, and then one day they introduce kosher foods and the food is still great.
I can still go there, because I don't care if it's kosher or not.
Right?
So there're tiny rules.
I didn't care about whether or not it's kosher, so it's fine for me.

Sjors Provoost:

Yeah, but you would if your favorite recipe was now kicked out of the restaurant, but it turns out...

Aaron van Wirdum:

I would care if they get bacon out of the fridge.

Sjors Provoost:

Exactly.
But this is not the case in the way Bitcoin soft fork works.
So they wouldn't remove your bacon, basically.
They would remove your ability to stab yourself basically.
And so it's a nice and elegant way to make the rules more strict without suddenly freezing anybody's coins.
So normal people can keep using it.
They don't have to upgrade.
They can keep using the old rules if they want to.
An exchange can basically ignore SegWit for years and it's perfectly fine, as far as the blockchain is concerned.
I guess we can talk about some examples.
So Satoshi introduced soft fork in the very beginning, in a way that we wouldn't do anymore.
Basically, one of the things he did was introduce a one megabyte limit.
There was no limit, he realized that was bad or dangerous.
So he put in a limit and then later on when it was already active, he said, "Oh, by the way, there's a limit."

Aaron van Wirdum:

So that's an interesting example that I didn't mention in my article for Bitcoin magazine, which is...
I mean, we're going to discuss how to implement soft forks, how to upgrade the protocol.
And one of the examples that's Satoshi used was to basically just snuck it in there.
And only once people are running the code, they'll figure out that there's now one megabyte limit.

Sjors Provoost:

Right.

Aaron van Wirdum:

Which worked at a time, I guess.
And maybe it was even a good way to do it because in his mind he was probably fixing like an attack factor.

Sjors Provoost:

Yeah.

Aaron van Wirdum:

And in that case, it makes sense because you tell people about it and that increases the chance of the attack factor being exploited.

Sjors Provoost:

Right.
But it could also happen by accident.
You accidentally add a rule to the system that you didn't know was there.
So that sort of stuff could happen, but that's not what we're going to talk about.
We're going to talk about a deliberate change in the rules.
So the other way that was done when there was a new rule, was a flag day.
To say, "Basically from this day forward, this new rule shall apply." And you announced that plenty of time in advance, and then people upgrade and it's all good.

Aaron van Wirdum:

Yeah.
So you're going to say like, "One year from now," so that's like July 24th when this is being published I think.
"July 24th, 2021, that's when the new rules are enacted."

Sjors Provoost:

Right.

Aaron van Wirdum:

Or you say at block height annual.

Sjors Provoost:

Yeah, exactly.

Aaron van Wirdum:

Some block height in the future, at this point the new rule is enacted.

Sjors Provoost:

But there was still a problem there, which is that you want to make sure that everybody's actually running the new software.
And especially that miners are running the new software, because they kind of have to enforce those new rules.
I mean, it's really nice if they enforce the new rules.

Aaron van Wirdum:

Well, everyone's enforcing the new rules.
Or at least everyone who's upgraded is enforcing the new rules.
But if a majority of hash power does it, that means they always reclaim the launch chain even for the non-upgraded nodes, like they still consider that the [Fallout 00:05:49] chain.
So then everyone, old and new nodes will converge on this chain.
So that's why it's very nice if a majority hash power enforces the rules as well.

Sjors Provoost:

Exactly.
And for miners there's a risk.
If a majority of miners enforces the new rules, but a minority doesn't, they could accidentally mine the wrong block.

Aaron van Wirdum:

The minority could mine an invalid block and then have their block orphaned.

Sjors Provoost:

Exactly.

Aaron van Wirdum:

They might not even know why, if they're not upgraded.

Sjors Provoost:

Exactly.
So it's nice if miners signal that they're ready to do this upgrade, so that you can get an idea, "Okay, most miners are clearly ready, and the few miners that are not, well hopefully they'll be fine."

Aaron van Wirdum:

So that's sort of the other upgrade strategy, apart from just stuffing it in there without telling anyone.

Sjors Provoost:

Yeah.

## BIP 9, BIP 91 and BIP 143 soft fork activation mechanisms

Aaron van Wirdum:

You have flag days and you have miner activation.
So signaling.
So the signaling works as a coordination mechanism for the network to figure out, "Okay, enough miners have upgraded now." This signals to everyone the network is ready.
And through this signaling mechanism, a date or a time, or a block height is communicated essentially.
That's embedded in the code, that if enough signals are included in the blockchain, then we all know at block height X, the new rules will go into effect.

Sjors Provoost:

Exactly.
So usually it's every two weeks you count the number of blocks that have the signal.
And if it's above a certain threshold, for example, 95%, then you know that two weeks later the new rule is active.

Aaron van Wirdum:

That was BIP 9.
Is what you're explaining now.
The Bitcoin Improvements Proposal 9 uses this difficulty period, 95%.

Sjors Provoost:

So these are the three main mechanisms, right?
You can just randomly do this.
You can announce a date and you can have miner signal up to a certain threshold.
And now the question is, what are you going to do for Taproot?
And what have we done in the past?
And maybe you want to combine some of these methods.

Aaron van Wirdum:

So mention why BIP 9 is a problem?

Sjors Provoost:

So BIP 9 was used a couple of times to deploy some features, I believe.
But when it was time to deploy SegWit, it took a long time.
Like we don't know if it would've happened eventually, but I think for at least half a year or so that the code was ready, it just didn't activate.
Only a small percentage of miners were signaling for it, or at least not the 95%.

Aaron van Wirdum:

Yes.
But we have a pretty good idea why that was.
I mean, at least the miners that were blocking it were telling us why they were blocking it.

Sjors Provoost:

Yes, exactly.
I mean it's possible that some miners were just completely not interested.
But there was definitely miners that were actively not signaling in.

Aaron van Wirdum:

Yeah.
Miner apathy.
That was probably a factor for at least some miners.
Sure.

Sjors Provoost:

So what happened then, is a number of different things happened outside the blockchain.
There was basically a group of people that said, "Hey, you know what?
We're just going to, instead of the signaling, we're just going to go back to the old flag day approach." And that was called BIP 148.
So they picked April 1st, 2017 and basically said, "Well, our nodes are now going to enforce these rules."

Aaron van Wirdum:

But hang on.
So to explain this real quick, like the downside of BIP 9 was that miners were blocking the upgrade, because they wanted either political leverage, or they were secretly benefiting from something that the upgrade would've fixed without telling anyone that that was the case.

Sjors Provoost:

Yes.

Aaron van Wirdum:

Or both.
But there were bad reasons basically for the miners to block this upgrade and this made Bitcoin core developers and other Bitcoiners realize that, "Okay, that's actually kind of a downside to BIP 9."
Because it gives miners this leverage, which they shouldn't have at all.
Like they're treating it like a vote and they're sort of abusing their vote in ways that's bad.
Why it's not even meant to be a vote, it's just meant to be a coordination mechanism.

Sjors Provoost:

Exactly.
And also the reasons why you might want to oppose a proposal, generally should be technical in nature and not political.

Aaron van Wirdum:

Yes.

Sjors Provoost:

So I guess that.

Aaron van Wirdum:

So ultimately this is what you were getting at.
This was resolved in some way or another, and there's still debate to this day how it was resolved exactly.

Sjors Provoost:

Right.
Because two things happened at the same time, right?
You had the BIP 148 (UASF) rules, the guys with the guns and the nodes.
And-

Aaron van Wirdum:

With the hats.
I don't think they had guns, but they had hats.

Sjors Provoost:

Some of them had guns.

Aaron van Wirdum:

[crosstalk 00:10:29].
That's true.
I think they were like...

Sjors Provoost:

In the forest, defending the Bitcoin.

Aaron van Wirdum:

Yes.
That's true.
And I think [inaudible 00:10:35] had like a knife.
Whatever.

Sjors Provoost:

And so...
Then the question is, you can tell if you read all the social media and the mailing lists, that obviously played a role.
But if you just look at the blockchain, you can't really tell.
Because what you see in the blockchain is, all of a sudden 95% started signaling and the thing activated.

Aaron van Wirdum:

Sure.

Sjors Provoost:

Now it's of course very remarkable that this activated exactly before August 1st and not some random other date that it could have happened.
But there were no blocks rejected that we could still point at saying, "Hey look, there was actually a fight between miners and et cetera." At the same time, there was an initiative from the New York Agreement Group.
And they had a whole bunch of things that they were planning to do.
But one thing they were doing is called BIP 91 and they were basically, "Lower the threshold." So they said, "Instead of having 95%, we're just going to accept 75%."

Aaron van Wirdum:

Well, to be a little bit more precise, what they did in the end was use 75% forced signaling.
So it was like BIP 148, but it was like a soft fork to activate a soft fork.

Sjors Provoost:

So basically you had to signal that you were going to activate the soft fork.

Aaron van Wirdum:

Yes.

Sjors Provoost:

And then because there was more signaling, it would activate.
But then again, you cannot tell from the chain, because immediately people started signaling at 95%.
And so that's the nice thing about these kind of situations.
You can't really tell what happened.
It didn't go wrong.
Like nobody called each other's bluff.

Aaron van Wirdum:

Yes.
And I think everyone agrees that it was at least sort of a tense period and it showed everyone that maybe we've got to rethink how we're actually going to do soft fork's, because this was very close to becoming a huge mess.

Sjors Provoost:

If you think through the worst case scenarios, so I guess we'll just avoid now because it'll get too confusing.

Aaron van Wirdum:

Yes.

Sjors Provoost:

But if you have chain splits and especially if you have multiple chain splits with people having different opinions about what the blockchain should be, that kind of defeats the purpose of a well-functioning blockchain.
So it's something you want to avoid.

Aaron van Wirdum:

Yes.
And let's skip the details.
But there was a risk of it becoming a pretty big mess.
I think that we both agree on that.

Sjors Provoost:

I was worried for quite a while it would be an absolute clusterfuck.

## BIP 8 for soft fork activation

Aaron van Wirdum:

So, new ideas.
How are we going to think about soft forks and soft fork activating from now on?

Sjors Provoost:

Well, one thing that was done is a revamped proposal called BIP 8.
And yes, that's a lower number because the proposal was older.
But now it's actually newer, so that is confusing.
But generally there were just a couple of improvements to the original mechanism.
Maybe not super interesting, for example, using blocks instead of dates.

Aaron van Wirdum:

Well, explain what BIP 8 is in the first place.

Sjors Provoost:

Well, BIP 8 was I think just a flag date proposal.

Aaron van Wirdum:

Was it originally just a flag date?

Sjors Provoost:

Yeah, I think so.

Aaron van Wirdum:

Okay.
But later it was definitely...
Like the idea was that it was a combination of BIP 9 and a flag date basically.

Sjors Provoost:

Right.
So what it is now at least, that's probably the most useful thing to describe.
Is the signaling is still there with some tweaks, but there is also a built in option to have a flag date.
And now BIP is just a sort of a proposal of how you could do things.
And so you could use a flag date or you could not use the flag date.
But the proposal now explains, okay, if you have a flag date, this is how you do it.
And it's a one way mechanism.
So you could propose a new soft fork and not set a flag date, and then later on set a flag date.
But you cannot propose a flag date and then unset it, basically.
So if you decide on a flag date, you better go through with it.
So it kind of [crosstalk 00:14:30].

Aaron van Wirdum:

Well, you can release a new client that doesn't have the flag date of course.

Sjors Provoost:

But now you have a mess, because you have...

Aaron van Wirdum:

Well, one of the nice things about BIP 8 is actually that it doesn't have a flag date purely.
It has a forced signaling deadline.
So it's kind of like BIP 148 before, where if you have the flag date on, so let's just call it the flag date for now.
Then it doesn't mean that it activates the soft fork itself.
It means that if near the end any block that's not mining activation, not mining support for the soft fork, that block will be orphaned.

Sjors Provoost:

Yeah.

Aaron van Wirdum:

Right.
So it forces signaling towards the end.

Sjors Provoost:

Yeah.

Aaron van Wirdum:

So this means that if you have two groups of BIP 8 nodes, one of them has the forced signaling on and one of them has the forced signaling off.
But miners go along with the forced signaling on, then the nodes that have forced signaling off, will still accept the soft fork because they're still seeing all-

Sjors Provoost:

They're still seeing the signaling.

Aaron van Wirdum:

Exactly, so that's a slight change from previous BIP 8.

Sjors Provoost:

Yeah.
And I forgot whether...
I think if you have a flag date in mind, you may still need to put it in there because you don't want different people to have different flag dates.
So I guess it doesn't matter if you force signaling, but it just becomes a mess.
Because if you force people to signal and then they don't signal, and you just decide to not accept all their blocks.
If only a small number of people do that, then you still get a mess.
So I don't think it's completely thought out, but you probably still want to have some consensus.
If you decide on the flag date, you want to have a very large consensus on what that flag date is and that really everybody goes along with it.

Aaron van Wirdum:

Maybe.
I mean, it depends, right?
Like even if you don't have consensus, but at least miners don't want to see splits.
Or they could play it safe.
That's sort of how BIP 148 happens.
Right?

Sjors Provoost:

Yeah.
But now imagine if you had two different, like you had the August 1 group and you had the August 15 group.
And maybe it didn't activate at August 1, but some like major exchanges decided to join the August 1 group and some other major exchanges decided to join the August 15 group.
And so it would still be a mess.

Aaron van Wirdum:

Yes.
The assumption is that in that case, or the hope is that in that case, miners just go for the August 1 one.
So they don't split the network.

Sjors Provoost:

That's one option.
But I think at least an improvement here is that let's say you just have miner apathy.
You thought you can get 95% signaling, but there's apathy.
You can have another discussion on mailing lists and everybody says, "Yeah, yeah.
We're fine with this upgrade." And no miner is objecting to it, they just not bothering to upgrade their software to signal.
Then you can calmly agree on a date, as a flag gate, and just calmly add it and there's not going to be too much chaos.
But you still have the problem of the miners not enforcing the rules.

Aaron van Wirdum:

Okay.
So I think these are sort of the basics of BIP 8.
And the next thing is that you can sort of play around with the parameters in all sorts of way.
So we've already mentioned with or without flag day.
And the flag day in turn can be an actual flag day or forced signaling.
Then you can play around with like a parameter of how long, how far into the future should this flag day be.

Sjors Provoost:

Yep.

Aaron van Wirdum:

You can play with a parameter of how much hash power it is.
So far we've mentioned 95%, but you could lower this.
You could say 75% is enough.
50% is enough.
Even 1% is enough.
You could potentially do that.
Right?

Sjors Provoost:

Yeah.
That's pretty useless, but you could.

Aaron van Wirdum:

I agree.
But like the point is you can play around with these permutations in all sorts of ways.
So now you sort of have pieces of the puzzle and then you can think of ways to put these pieces together, to come up with like a concrete activation strategy that we're going to use for Taproot.

Sjors Provoost:

But you can also imagine that there's going to be a lot of permutations.
And so this could be a byte shedding nightmare.

## Different proposals for taproot activation

Aaron van Wirdum:

Yes it could.
But should we cover some of the sort of general ideas that are floating around?

Sjors Provoost:

Yeah, sure.

Aaron van Wirdum:

Okay.
So one idea that has been proposed by Matt Corallo, a well known core contributor, is he calls it modern soft fork activation.
So what he proposes is, let's use BIP 8 without forced signaling on the end, or without forced activation on the end for a year.
So that's more like BIP 9, that's what we used to do.
See if miners activate it, just requiring a 95% hash power support threshold, let's see if they do it or not.
If they do it, great.
Soft fork has been activated.
If they don't, then phase two of this proposal comes into play which is six months of developer reconsideration.

Aaron van Wirdum:

So developers see if there was a good reason for miners to block it.
Maybe there was a problem with the proposal, in this case Taproot, that they hadn't considered before.
So developers are just going to sort of reconsider.
If after six months they haven't found anything wrong with the proposal and they conclude that, okay, it's actually just miner apathy or miners trying something or whatever, like no good reason, then we're going to deploy it again.
This time BIP 8 with either forced signaling or...

Sjors Provoost:

With a flag day.

Aaron van Wirdum:

Flag day on the end.

Sjors Provoost:

Yeah.

Aaron van Wirdum:

I think Matt's original idea was flag day on the end, but he's probably open to forced signaling I would imagine.

Sjors Provoost:

I mean, the question is if you have a flag day, what do you do on the flag day?
And one thing you can do with the flag day is enforce the soft fork and the other is you can force the signaling, which then triggers the soft fork.

Aaron van Wirdum:

Well, exactly.

Sjors Provoost:

So I don't think that's...
That's more of a detail and it's probably not controversial to force the signaling instead of forcing the soft fork.

Aaron van Wirdum:

I think that wouldn't be very controversial.

Sjors Provoost:

Just makes it more compatible with what other people are doing.

Aaron van Wirdum:

Yes, exactly.
So that would probably be, yeah.
Okay.
So that's one idea, it has the benefits of sort of taking it easy and reconsidering if there's maybe something wrong with the proposal.
And if there is something wrong with the proposal that people don't have to actually need to upgrade their soft fork, they can just keep running whatever they were running.
Because there was a time out anyway in the soft fork, it just didn't happen.
And it's sort of fine, there's no sort of emergency upgrades needed at all or anything like that.
The downside is that if miners don't cooperate, it's going to take a long time before the soft fork actually is live on the network, like three and a half years.
So that means App developers have to wait three and a half years.
Everyone's just sort of stuck waiting for three and a half years for basically no good reason.
So that's why some people really don't like this proposal.
What do you think?

Sjors Provoost:

Well, you're going to think in the long run, right?
So it's nice if you can have these improvements ship very quickly.
But if there is a tradition that developers decide on a soft fork and it gets activated quickly, well then maybe a government starts calling developers and saying, "Hey, we have this KYC soft fork.
And since nobody really pays attention and miners are run anything you want, why don't you just make that soft fork and don't worry about the review process?" So you don't want to put too much power in the hands of the developers.
They don't want that kind of power because it means they're going to get very unpleasant phone calls at some point.
So.
It's a difficult trade off, because on the time scale of 200 years, it really doesn't matter if the soft fork takes three years longer.
But we have no idea what the right time is, maybe it makes no difference for this political problem.

Aaron van Wirdum:

Yeah.

Sjors Provoost:

It might really just be wasting three years or it's really important to make sure there's no problem.
[crosstalk 00:23:00].
I'd like to see it deployed soon and hopefully miners are excited.
But it's going to get more and more difficult to deploy these things in general because if you get, and we want that, lots and lots of very small individual mining pools while trying to get 95%, even just to communicate to them is going to be harder.
And that's a good thing, but it could slow things down.
Very...

Aaron van Wirdum:

Sure.
So another idea is BIP 8, let's say with like a year deadline at which time forced signaling happens.
Almost kind of like a basic proposal.
Would this be...
So to first ask you about that, do you think that's too fast?
One year, forced signaling?

Sjors Provoost:

So my problem with the forced signal is, if you ship this thing and you say, "Okay, miners can signal for it.
But if they don't, it's going to activate." You kind of lock yourself into that outcome.
There's no real way to object anymore.
Because even if miners come up and say, "Hey, wait a minute, there is a problem." Then you can't cancel it anymore, because people are this new soft fork and they have the forced signaling in.
So lots of people would see their nodes just stop.
And so you're essentially having a hard fork if you decide to not do it.
So what I think you should do at minimum is say, "We ship this version without the hard coded date in it, but we're probably going to enforce that hard coded date in a new upgrade." But I think that should be [crosstalk 00:24:27].

Aaron van Wirdum:

Yeah well, that's another proposal I want to get there next.

Sjors Provoost:

Okay.

Aaron van Wirdum:

But I want to...

Sjors Provoost:

So this one I don't like, because if you remove any ability to object, then why even bother with the miner signaling.
Because once you put a flag date in the code and you ship that code, that's it.
It's just going to activate.

Aaron van Wirdum:

Well the idea behind any soft fork-

Sjors Provoost:

Unless you force people to upgrade and that's a hard fork.

Aaron van Wirdum:

Yeah.
Although the idea behind any soft fork including Taproot presumably, is that there shouldn't be a problem with it if it's going to be shipped at all.
Like at the point of it being shipped, there shouldn't be any problems with it.
And after that, it's just a matter of coordinating the upgrade.

Sjors Provoost:

But the question is when are people going to bother to review it?
And I could imagine that if I'm a miner and like, "Oh, I have to run this new version, let's see what it's doing."

Aaron van Wirdum:

Right.

Sjors Provoost:

"Holy shit.
I don't like these new rules.
Why are they reducing the block reward?"

Aaron van Wirdum:

Right.
That's one of Matt's arguments as well.
That people and miners will only really consider it when the code is out there and the software is out there.

Sjors Provoost:

And it's an expensive signal too, right?
As a developer, you're really shipping this software.
That's a bigger commitment than saying, "Okay, looks good and get up."
So I think that is a critical moment and you can't expect review to happen after that.
Or review to happen after that.
So that's why I don't think you should put the date in stone, at least not the first try.
Maybe a half a year later.
Maybe you don't have to wait for the whole year.

Aaron van Wirdum:

So a related idea and it's almost kind of the same idea I guess, but it's Luke-Jr.

Sjors Provoost:

Luke Dashjr.

Aaron van Wirdum:

Yeah.
Luke Dashjr, Luke-Jr.

Sjors Provoost:

People call him Luke-Jr.
But he once said in a podcast, "It's Luke Dashjr." So.

Aaron van Wirdum:

Oh, he did?

Sjors Provoost:

Yeah.
The Peter McCormack show.
That's the first time I learned.

Aaron van Wirdum:

All right.

Sjors Provoost:

Maybe he's lying.

Aaron van Wirdum:

Oh no.
He's not allowed to lie according to his religion.

Sjors Provoost:

Okay.

Aaron van Wirdum:

He likes BIP 8 with forced signaling towards the end, but he prefers it to be deployed in forks for clients.
So not in Bitcoin core.
So kind of like BIP 148.
Like he thinks soft fork activation should happen through different clients.
That sort of takes away this pressure on Bitcoin core developers.
Like potential government forced soft forks, that sort of stuff.
So only do it through forks of Bitcoin core, or forks clients.
What do you think of that idea?

Sjors Provoost:

Well, how do you coordinate the date?
Is that-

Aaron van Wirdum:

Someone just picks one or it's sort of coordinated in some slack channel, like what happened with BIP 148, or...

Sjors Provoost:

The problem is, like we discussed before.
If you have multiple dates, you're going to get the cowboy bias.
Because whoever picks the most aggressive date, that's the party you kind of have to listen to.
But that might be a recklessly early date, because some people might be [crosstalk 00:27:18].

Aaron van Wirdum:

I think if...
So, like we mentioned before with the kosher food, a soft forks shouldn't have any downsides really, or at least that's when it's becoming-

Sjors Provoost:

But a fast activation could still cause problems.

Aaron van Wirdum:

Yes.
But then that's the downside in itself.
So if people in general think, "Okay, this is too aggressive.
Like this isn't good for Bitcoin to do this aggressively." Then that's the reason itself, I think, it might fail.
So there's-

Sjors Provoost:

But the problem with this is the minority rule.
The intransigent minority rule that Taleb likes to talk about.
The most fanatic group.
So probably the most fanatic group is going to say the earliest date, and the rest will have to just go along with that earliest date.

Aaron van Wirdum:

No they don't.
Not if the rest really dislikes the solution.
The only reason it works with sodas is because most people don't care either way.

Sjors Provoost:

Right.

Aaron van Wirdum:

But if most people really cared about what was in their soda, then the minority wouldn't get their way necessary.

Sjors Provoost:

I would prefer if you went this route and there's some merit to it.
I would still like at least the development community, like people on the mailing list to agree on a date.
And then once that date is agreed on, we say, "Okay, we're not going to endorse this thing, but if you do this thing, here's the download and we all have the same date in mind.
So there's no chaos around the date."

Aaron van Wirdum:

Yes.

Sjors Provoost:

And then...
Yeah, there is something to be said for like not having-

Aaron van Wirdum:

But they don't seem to agree, so that's going to be tricky as well.
Right?

Sjors Provoost:

Who doesn't agree?

Aaron van Wirdum:

Well, I think for example, Luke.
I think also Jeremy Rubin to name a few names.
They'd like a much faster activation date than for example Matt Corallo, or I think AJ Towns is also someone who prefers a slower activation date.
So there's dispute in there it seems.
So that makes it kind of tricky, right?

Sjors Provoost:

Yeah.
It may be that that ends up in something that will forever be known as the Bike Shed Wars.

Aaron van Wirdum:

Well, but then, the cowboy might actually come around and...

Sjors Provoost:

Yeah.
And activate-

Aaron van Wirdum:

And almost sort of save the day.
I'm not necessarily endorsing that, but-

Sjors Provoost:

But let me give you a bad scenario-

Aaron van Wirdum:

Let me put it this way Sjors.

Sjors Provoost:

Okay.

Aaron van Wirdum:

I find it almost inevitable, like someone out there is going to Leroy Jenkins.
Like it's got to happen.
I don't know if it's going to succeed, but it's almost inevitable.

Sjors Provoost:

So here's a bad scenario.
Let's say we ship the completely ready Taproot code ready for main net in two months.

Aaron van Wirdum:

Yes.

Sjors Provoost:

Not going to happen, but let's say we do that.
And the code has this one year miner signaling thing and then it expires.
And now the most aggressive group comes out and says, "No, no, no, we're going to activate this like one month later." That's going to be the consensus of the loudest people.

Aaron van Wirdum:

Yes.
That's going to be the Leroy Jenkins.

Sjors Provoost:

So two weeks into that scheme, the miners actually start reviewing.
Because like we just talked about, people might only review code when it's ready.
Now they find a critical bug.
And most of the core developers would agree, "Okay, this is actually a bug.
We should abort.
Soft fork miners, please don't signal for it."
But at the same time you have this super loud group, who's already canceled everybody who doesn't agree with them to activate this thing.
So that's why I like the idea of having at least some decent amount of time and some community agreement on, "When are we going to flag date this thing?" And it shouldn't be within a few months.
You should give people a decent amount of time.
But you know, I can't decide what people are going to do.

Aaron van Wirdum:

Well, I said, that's kind of my point.

Sjors Provoost:

But you might get a...
Either that might be successful and it just deploys early and we get lucky.

Sjors Provoost:

Maybe it's a botched UASF sort of situation where they try.
They make a really loud noise.
But the main players in the industry, because of this bug for example, say, "No, no, no.
We're not doing this."

Aaron van Wirdum:

Yes.

Sjors Provoost:

And they just collide head on and nothing happens, where you get a bunch of orphan blocks.
It's hard to predict.
But that could be a mess and that could be on CNN.
And then there's like, "Oh, Bitcoin is broken," on CNN.
And Bitcoin was already broken two podcasts ago.
Remember?
I don't know what the topic was.
I think at was about [crosstalk 00:31:20].

Aaron van Wirdum:

No, that was a security something....

Sjors Provoost:

Oh, it was unconfirmed transactions.

Aaron van Wirdum:

Oh yeah.
That was the thing.

Sjors Provoost:

But now imagine all these very mediagenic people with their machine guns in the forest advocating a soft fork that all of the core developers are saying, "Let's not activate this, because there's like a really, really bad bug in it."

Aaron van Wirdum:

Yes.
But I do think the dynamics then would be very different.
Like if there's an actual bug in the actual soft fork itself, compared to an actual...
Or just an objection to that situation itself.

Sjors Provoost:

Right.

Aaron van Wirdum:

Like these are two different-

Sjors Provoost:

This was a very extreme example.
But less extreme would be, I think miners should have some time to review this code after it's shipped.
And some people might say, "No, they should have reviewed it earlier, because like we don't want to set the incentive."
I think it could be messy.
So that's why waiting longer, I think is just better.

Aaron van Wirdum:

So here's another right idea.
Another idea is BIP 8 plus BIP 91.

Sjors Provoost:

Okay.

Aaron van Wirdum:

So this basically means you're going to deploy BIP 8, I think with a long signaling period.
Like could even be three years or whatever, like something that's similar to Matt's proposal.
After these three years, three and a half, whatever it is, the activation is triggered.
So there's a long lead up.
In the meantime though, you're going to see what happens.
So for example, if after a year it's still not activated, then developers can sort of try to find out why it hasn't activated again, sort of similar to Matt's idea.
Developers take their time.
They figure out, "Okay, there's actually no good reason that it's not being X failed." At that point, they can deploy a new client that has sort of BIP 91 in it, which forces miners to signal support for it before the three and a half year are over.

Sjors Provoost:

You mean a lower threshold?

Aaron van Wirdum:

Yes.
A lower threshold.

Sjors Provoost:

Okay.
So you basically ship an update, which has a lower threshold in it.

Aaron van Wirdum:

Yes, which in turn triggers the higher threshold.

Sjors Provoost:

So I like the idea of lowering the threshold over time.
What I am worried about, and maybe that was discussed, is what if there's a bug?
Because if this thing has a three year window, that means there is three years in which this thing could activate, even though everybody agrees, it shouldn't activate.

Aaron van Wirdum:

Right.
Well then, so that's-

Sjors Provoost:

That's kind of scary.

Aaron van Wirdum:

Right.
So then the answer is deploy a new client that includes a soft fork that undoes the Taproot soft fork in that case.

Sjors Provoost:

Well, if you undo a soft fork, it's a hard fork.

Aaron van Wirdum:

Not if it's not activated yet.

Sjors Provoost:

But you don't know that.

Aaron van Wirdum:

What do you mean?

Sjors Provoost:

The problem is people who are running the first version, they're just waiting for that 95%.
They're waiting for three years until this thing activates.
But then if there's a bug fix, then you need to have a new signal flag to indicate the new version of Taproot that you're going to activate.
And you have to make sure the old version never activates, because [crosstalk 00:34:27].

Aaron van Wirdum:

Soft fork is a tightening of the rules.
So now you say any soft fork, any Taproot, anything is just not allowed.
You're not going to include it in blocks.

Sjors Provoost:

Yeah.
You could completely ban version one basically.
Right.

Aaron van Wirdum:

That would be soft fork.

Sjors Provoost:

But that's pretty horrific.
It would be nice if you didn't have to do that.

Aaron van Wirdum:

It would be kind of ugly.
Yes.
Plus it would be important that people upgrade.
[crosstalk 00:34:50].

Sjors Provoost:

So a one year signaling thing is nice, because that means that you can say, "Okay, if this thing doesn't activate in a year because there's a bug.
We wait a year and we try again and then we know for sure we're not going to accidentally activate the old version after that year."

Aaron van Wirdum:

Yes.

Sjors Provoost:

And yeah, it's kind of annoying to have to wait for a year.
But then if there really is a bug in a thing that was ready to be deployed, that really warrants a year of thinking really, really well about how the hell that could happen.

Aaron van Wirdum:

Okay.
So then there was another idea.
I added this, as an-

Sjors Provoost:

But the idea of saying that signaling thresholds could go down, that makes sense to me.
So you could say, "Well, when the year starts, it's 95%.
But you know, after six months it should just be 80%.
And after 11 months it should be a little bit less.
And then if it still doesn't happen, we give up and we decide again for next year, what we're going to do."

Aaron van Wirdum:

Yes.
All right.
So then there was another idea which is, I guess, is it the opposite as a previous one?
Maybe not.
You take BIP 8 with a long period, but without forced signaling at the end.
Then you still keep an eye on what's happening.
If after a while you find that there is no problem with it, but miners aren't signaling for it because they're just apathetic or they have another bad reason.
Then you can deploy another client with BIP 8, this time with forced signaling that starts forced signaling before the end of the current signaling period.

Sjors Provoost:

Okay.

Aaron van Wirdum:

Or at least not later than that.
Like if it starts before that, then you have two groups of nodes online on the network, the BIP 8 nodes you deployed first that don't have forced signaling on the end.
And now the new group of BIP 8 nodes that do have forced signaling.
So if they do so the forced signaling stuff, then the older BIP 8 nodes will also accept that as an upgrade.

Sjors Provoost:

Oh, well that sounds like a regular idea of BIP 8.
Right.
So BIP 8 has the option to allow soft fork signaling.
So initially you do not ship that option, and then later on you do ship the option.
And yeah, the old nodes won't be confused, because they see the signaling.

Aaron van Wirdum:

Yep.
Pretty much.
So what's your preference here?
It sounds like you're kind of conservative.

Sjors Provoost:

Well, like I said, I don't like the idea of hard coding a flag date initially.
So I can see the benefit of, you ship something, you wait.
Say it has a year of a window.
You wait for six months and then you still don't see any signaling, but you also don't see the miners that reviewed your code and found problems.
Then maybe you say, "Okay, let's do a flag date." So it's like, "That's not super patient." And then you ship, you have that flag date within six months.

Sjors Provoost:

But I'm not sure.
In the short run it's nice to have all this stuff fast.
In the long run it's kind of scary if something can happen fast.
Because it gives you less time to stop it if it's bad.
But again, just being slow for the sake of being slow, doesn't make any sense either.
So I can see why these IRC threads are going to be really long.
But what I'm hoping will happen is, we just do BIP 8 without a flag date with a year of a window, and we get lucky and miners just activate the thing within a month.
And it's done.

Aaron van Wirdum:

That would be nice, right.
If miners just cooperate and maybe we're all making too big of a problem out of this.
Well, that's one of the...
Just for example like Greg-

Sjors Provoost:

Well, I don't want to say it would be nice if miners just cooperated, because Ethereum has that too and miners are very cooperative.
I would, [crosstalk 00:38:26], if miners were very excited about this proposal for good reasons and did so quickly.
But I'm not saying that it's not technically not cooperation, it's just agreeing, right.
Not obeying.
I guess it is cooperating, but I mean it in an agreement sense, not in an obeying sense.

Aaron van Wirdum:

Sure.
Well I think Greg Maxwell's position, for example, there are few like him.
Is I don't think he really cares strongly, like he feels like whatever is likely to work.
Like just go for it.
Don't overthink this, because-

Sjors Provoost:

It's probably a good...
Yeah.

Aaron van Wirdum:

"If it doesn't work out, we'll deal with it then." I think that's sort of his position, for example.
And like all of the options I've named so far, I think he's sort of okay with.
As long as, like something needs to be picked.
Because the longer it's going to take, the harder it's going to get probably, and the more controversial the whole topic might become.
And like just try something.

Sjors Provoost:

Yeah, it's quite possible.
You get a whole holy war over the exact details of how you activate a soft fork and that might be bad.

Aaron van Wirdum:

Do you think it's...
I mean, that's one of the reasons it could be like a holy war, is some people think that it's a very important precedent to like the way you're enforcing a soft fork.
The way you're activating a soft fork that really matters going forward for the next soft fork.
And it really sort of defines Bitcoin almost in a way.

Sjors Provoost:

Well, I don't know about the latter because things change.
So even if we do things in an amazing way, five years from now, there might be a whole new generation of people that just do not care about the ways of five years ago.
All these old people.
So.

Aaron van Wirdum:

Especially in Bitcoin, five years is an eternity.

Sjors Provoost:

I mean, I think that I mentioned today my main concerns, don't set something in stone that you have a serious chance of regretting.
So keep in mind that people don't review code before it's actually shipped.
And so that's why I kind of like the idea of having say a one year activation window.
Maybe with a minimum of three months, there was another proposal for that.
And then give miners and others some time to actually review this thing, because haven't done it.
And then if they find a problem, you could still abort.
And then if you don't see this objection, then you can choose to put in a flag day and then you can debate whether you want the flag day to be very quickly at the end of the year.
Or whether you say let's give it another year.
That just depends.
But I don't have a strong opinion there.
But I'm not the most patient person, so you should ask a more patient person.

Aaron van Wirdum:

Well, you sound pretty patient to me.
I think I'm pretty patient.

Sjors Provoost:

Not by like Greg Maxwell standards, I think.

Aaron van Wirdum:

Right.
I guess I'm pretty patient when it comes to soft forks and I'm not really in a rush.
Like Bitcoin works for me the way it's working.

Sjors Provoost:

A downside of having-

Aaron van Wirdum:

At the same time, it's like users are, "It's not up to me." Like people are going to get impatient and I think that's going to be an interesting dynamic to see play out.
Like too conservative is a risk in itself.

Sjors Provoost:

Yes.
Because if this soft fork is hanging in the air for years, it will get political.

Aaron van Wirdum:

Yes.

Sjors Provoost:

And then it might not go through because of politics.
That would not have happened if it went through a bit quicker.

Aaron van Wirdum:

Yes.
Or it just increases the chance that someone's going to Leroy Jenkins in a bad way.
If developers want to be too conservative, then you're going to see that kind of movement.
And that might not always be the best way to do it either.
I think this is a fascinating topic and I'm going to...

Sjors Provoost:

Should we end on the cliffhanger?

Aaron van Wirdum:

Do you have a cliff hanger?

Sjors Provoost:

What are sporks?

Aaron van Wirdum:

What's that?

Sjors Provoost:

What a sporks?

Aaron van Wirdum:

Oh, sporks.
You want to get into that one as well?

Sjors Provoost:

No, no.
I want to leave it as a cliff hanger.

Aaron van Wirdum:

Oh yeah.
That's even better.
So we discussed it in another episode?

Sjors Provoost:

In another episode or maybe never.

Aaron van Wirdum:

I like that.
Yeah.
Maybe never.
Maybe we're doing a lost cliffhanger.
You'll just never get the answer.

Sjors Provoost:

So.

Aaron van Wirdum:

But there is another idea for soft fork, which is called sporks.

Sjors Provoost:

Sporks.

Aaron van Wirdum:

Right Sjors.
That was it for this episode I think.

Sjors Provoost:

Thank you For listening to the Van Wirdum Sjorsnado.

Aaron van Wirdum:

There we go.
