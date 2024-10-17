---
title: Privacy and robustness in Lightning
transcript_by: markon1-a via review.btctranscripts.com
media: https://podcasters.spotify.com/pod/show/chaincode/episodes/Rusty-Russell-and-privacy-and-robustness-in-Lightning---episode-34-e27t6go
date: '2023-08-09'
tags:
  - lightning
  - eltoo
  - privacy-enhancements
speakers:
  - Rusty Russell
episode: 34
summary: In this technical discussion, Rusty Russell, Mark Erhardt, and Adam Jonas delve into the intricacies of the Lightning Network (LN) after eight years of development. They emphasize the importance of simplicity and robustness in the protocol, noting how attempts to increase fairness often complicate the system. Russell highlights the ongoing need for improvements in privacy and robustness, pointing out that while these areas aren't usually urgent, they are crucial for long-term stability. They discuss the LN symmetry (formerly Eltoo) proposal, which aims to simplify the protocol by eliminating penalties for unintentional errors, thus making the network easier to maintain. The conversation also touches on the challenges posed by recent fee spikes and the need for better fee management and protocol upgrades. They conclude by acknowledging the significant progress made and the continuous efforts required to keep improving the network
aliases:
  - /chaincode-labs/chaincode-podcast/privacy-and-robustness-in-lightning/
---
## Introduction

Rusty Russell: 00:00:00

Simplicity is a virtue in itself, right?
So you can try to increase fairness.
If you reduce simplicity, you end up actually often stepping backwards.
The thing that really appeals about LN symmetry is it's simple.
And every scheme to fix things by introducing more fairness and try to reintroduce penalties and everything else ends up destroying the simplicity.

Mark Erhardt: 00:00:27

So soon again.

Adam Jonas: 00:00:28

Yes.
For those of you that aren't tracking us in real time, we are getting a bunch recorded today.
So had Rusty Russell in the office.

Mark Erhardt: 00:00:39

Yeah.
So this is one of my favorite podcast guests to listen to, and I'm very happy that-

Adam Jonas:

Why?

Mark Erhardt:

Because he has the capacity to cut through a lot of the noise and get to the crux of things, say them as they are.
Ugly truth, sort of.
Very nice for engineers to actually talk about the elephants in the room.
So I'm expecting that we'll hear a little bit about what's still broken and Lightning where the ship is sailing.

Adam Jonas:

Okay, here come the elephants.
Welcome, Rusty.
It's great to have you here.

Rusty Russell: 00:01:22

Thank you.
I am fresh off the boat.
I literally arrived less than 24 hours before from the other side of the world.
So I hope this will be coherent.

Adam Jonas: 00:01:30

Our budget is for this podcast is incredible.
We fly people from all over the world to this office.

Rusty Russell: 00:01:36

I must say that private jet was lovely.
Thank you for that.

Adam Jonas: 00:01:39

It was delightful.
You are here for the Lightning summit.
Let's talk about Lighting.
Just sort of just get into it.

Rusty Russell: 00:01:46

Let's do that.
Yeah.
Okay.

Adam Jonas: 00:01:47

Tell us what you think this group should be thinking about as you're as you're gathering together.
There's going to be specific conversations that happen about specific proposals.
But I guess more generally, as lightning has grown up. What are the kinds of things that you're thinking about and concerned about?

Rusty Russell: 00:02:04

Yeah, okay.
That's a fair question.
There are obviously specific things that we're going to talk about at the summit.
Definite concrete proposals and that's all great.
This is always a fantastic time for everyone to come together.
I think if we step back a bit. This is like eight years now for the Lightning Network.
So we've been doing this for a while.
And there are a couple of things that I think we really need to make sure we keep focusing on because it's easy to get in the weeds of specific things and I would love to go into those and we can totally go there.
But I think robustness and privacy are the two things that are rarely actually on fire, but are always important.
And they're both areas where we can definitely make incremental improvements, and I think we should.
Privacy in particular is something that everyone cares about until you need to put the engineering effort in and there's other stuff.
There's bugs, there's issues, there's, there are always other things that are more urgent, even if they're not more important.
And so I definitely try to keep the perspective of going, if not now, when?
And I think, privacy is something that we definitely need to put more effort in.

Adam Jonas: 00:03:07

Yeah, I imagine that privacy goes to the end of the line pretty much every time.
But can we talk about robustness for a moment?
Because robustness is definitely something that you think about in Bitcoin quite a bit.
It's different though, in terms of layer one versus layer two, because layer two sort of promises to be this move fast and break things approach, because it needs to move fast and it needs to grow and it needs to catch up.
Now things have broken, but I guess not to the same extent that I think people are trusting it.
I mean, there's serious money on the line.

Rusty Russell: 00:03:42

Yeah.

Adam Jonas: 00:03:43

And I guess the question is, do you have to react to the amount of money that's in the system?
Or is it still, well, we're still figuring this thing out.
And that's up to you if you want to put that much money in there.
But we still need to experiment.
And again, it is a robustness speed trade off in terms of what you can do.

Rusty Russell: 00:04:07

So, robustness on some extent is always something we need to think about.
But also, I think like the recent fee spike showed us that there are definitely places we can improve.
Robustness from the protocol level means we want stuff where we become more immune to fee issues.
I think that's something definitely, we need longer term.
The assumption is fees are going to go up, they're going to get more volatile, we're going to have these spikes, we need to handle that really well.
And I certainly hope that we, we have a number of tricks we can do.
Some of which is like, well, we want some soft forks, right?

## LN symmetry

Rusty Russell: 00:04:39

If we can get LN symmetry, which used to be called  Eltoo, but LN symmetry is a much better name.
Sorry to question who named  Eltoo.
He blames me.
I blame him.
For example, sidesteps a whole heap of, it reduces robustness by introducing simplicity.
It does make it a lot simpler to maintain your Lightning channel.
There's no longer toxic waste that you have to worry about, old states and stuff like that.
Watchtower has become now almost trivial.
So that adds some simplicity.

Rusty Russell: 00:05:04

Can we take a quick side route on that?

Mark Erhardt: 00:05:07

Sure.

Rusty Russell: 00:05:09

Because we've talked about LN symmetry specifically with Instagibbs.

## Do we want LN Symmetry to be symmetrical?

Adam Jonas: 00:05:12

But I'd be interested in getting your take on, given that asymmetry seems to be healthy for the network, do you want it to be exactly symmetrical?

Rusty Russell: 00:05:21

Okay, so this is a good question.
So at the moment, let's step back.
LN penalty, as it's retronamed into, is the current scheme where basically if you screw up, I take your money.

Adam Jonas: 00:05:31

Yeah,

Adam Jonas: 00:05:31

Tadge is over there, too.
We can pull him in.

Rusty Russell: 00:05:33

Yeah, okay.
We can do that.
Right now, so what we found in practice is that usually what happens is you screw up, I take your money, and I feel really sorry about it, and I try to give it back to you.
Right?
So, the current scheme is actually a little bit too harsh for the world that we actually live in, because we rarely see people actually trying to cheat, and we often see them do it accidentally because they're a store from backups and, that was bad, right?
With the LN symmetry approach, simply if you screw up, I just fix up, right?
There's no massive penalty for you doing so.
The danger is then, have I created an incentive problem where you might try to cheat because it doesn't cost you anything?
Now, this is interesting in a couple of ways.
One is, is that actually always more expensive for you to close unilaterally, even under LN symmetry, than it is to do a mutual close.
But you talk to me and we go forward and we produce a mutual close transaction that's got a tailored fee rate and everything else and it's smaller.
So if you can talk to me, you're going to want to do that.
But if I was unreachable, well, I might as well try to spend in an older state.
So the cost of an attack has dropped significantly because that risk issue.
Well, you're paying some fees for it, sure, but you're not risking that if you screw up, you're going to lose all your funds.
But on the other side of the coin, my implementation is much simpler and watchtowers are now trivial.
It's so much so that we can have many watchtowers looking out for these kind of things.
They only have to remember one transaction, which is the last one.
They see it, they drop it to chain, we're done.
So the fact that watchtowers are much more scalable means that while your risk is reduced as an attacker, your probability of success is reduced even more.
So there is less of an incentive problem than you might have originally thought with going for LN symmetry.

Mark Erhardt: 00:07:09

But it still costs you the same to broadcast in the old state or the newest state, so you don't lose anything, right?

Rusty Russell: 00:07:16

Yes.
But on the simple protocol level, you go, well, you didn't lose anything.
But on a higher level, I'm not going to trust you again because you're obviously doing weird because they restored from backup.
But you know, if you start doing this a lot, people are gonna be like, no, no, I don't trust them anymore.
So, so if the potential benefit for you is so small, that that social convention that, if I want to become a big node, I'm not going to get there because I people have noticed that I keep double spending because it's really clear on chain.

Adam Jonas: 00:07:47

Yeah, but that also changes with high fee environments, right?
I mean, you start making it more difficult for people.

Rusty Russell: 00:07:55

But now, remember, in a high fee environment, the cost for you to do a unilateral close is much higher.

Mark Erhardt:

I see.

Rusty Russell:

You want to do a mutual close.
So the only case where it really comes out is when I'm unavailable you can't do mutual close.
You're going to use the unilateral close anyway and now you're like well I might as well try to cheat.
So you're already kind of in a corner case because that's already sending more money than if you just spoke to me and closed your channel.

Mark Erhardt: 00:08:16

So we've talked quite a bit about LN symmetry and how we want to retain the symmetric aspect of it.
There was also a proposal where you would have some sort of penalty for the initiator of the closing transaction by having a larger output on the commitment transaction than input.
So you would have to add a second input to provide additional funds.
Could we talk about that proposal?

Rusty Russell: 00:08:42

Simplicity is a virtue in itself, right?
So you can try to increase fairness.
If you reduce simplicity, you end up actually often stepping backwards.
So the thing that really appeals about LN symmetry is it's simple.
And every scheme to fix things by introducing more fairness and try to reintroduce penalties and everything else ends up destroying the simplicity that, for me, is like, well, it depends on the ratio of attacks, right?
At some point, how much engineering, how much effort is going in to save a few cents statistically on your attack probability.
And so I've come around to the idea that making watchtowers ubiquitous is enough by itself to then go for a very simple and dumb protocol that at the end of the day will be far simpler to implement and have fewer corner cases and those things than trying to get fancy and bring back everything.
Because then we end up back at basically somewhere like LN Penalty and I'm like, well no, we didn't like that.
You know, there's definitely like, I'm not completely ruling out the design space, but I do like the simplicity of going, well, you've got one transaction, you spend it, you're done.
It's nice.
You know, and whoever spends it ends up having to fund the close.
That's pretty nice too.
The other argument for breaking symmetry is you can then tell who screwed up.
If everything's symmetrical, I can make it look like you screwed up by just spending the n minus one transaction the nth transaction and then go, you spent that one and actually it was me.
There's some cost to doing that, I'm going to have to pay fees on both of them.
But no one can canonically assign blame for that kind of screw up.
So you start to go, well, maybe we do make them asymmetric but then you're like yeah you're reintroducing complexity and the real appeal is simplicity and simplicity is often underrated as far as going you know there's enough moving parts in Lightning as we've discovered without making the base protocol.
So I find the simplicity more compelling I think now than I did when the first idea was introduced.
So I've definitely come along.
The good news is that we need a soft fork, we need to roll this thing out, it's not going to happen overnight, we're going to have both side by side, and we will find the engineering tradeoffs, to be honest.
If I'm wrong and we end up going, no, actually, we want some hybrid scheme, or we prefer LN penalty or everything else, but we'll get there as well.
There's no huge hurry in this process.

Mark Erhardt: 00:11:02

Of course, people that still want a penalty can just continue to use LN penalty.

Rusty Russell: 00:11:07

No, we'll rip the damn thing out as soon as we can.
I mean, the simplicity argument only applies if you don't have to support both.
Now, to be fair, you can migrate from LN penalty to LN symmetry, but you will have to handle a case where the other person goes back and spends one of those ones that needs a penalty, because you can't symmetry that afterwards.
I can't come up with any scheme where you can just retro in and attach on.
It's theoretically possible, but it's not actually possible as far as I can tell.
So you will need to still be able to have your penalty code, even if you no longer open new ones.
If you've got existing channels that have not been spliced or otherwise had some kind of on-chain commitment, you will still need to have the code that handles, crap, they spent the old one, I now have to do a penalty thing or whatever else.
It's not a huge amount of code, it's not as complicated as some of the other parts, but it will still be there until the point where you go, no.
Everyone has all those channels are dead.
We've got all new channels.
At that point, you would be able to get rid of the whole concept entirely.
But this is the benefit of having different implementations and a simple protocol where a new implementation come along and go, I want to write it in whatever the language flavor of the week is, there's always somebody who's prepared to rewrite it.
So by having a simple protocol, they may go, actually, I'm not going to implement all that crap.
We're only going to implement the new one.
And that may well be what carries us forward.
I don't know.

Mark Erhardt: 00:12:29

It makes it way easier to have more than two parties, right?
So it might be the roads to channel factories or you can still share your schemes.

Rusty Russell: 00:12:40

So yeah, your point about opening the door to channel factories and multi-party channels and all that is definitely a huge impetus to do LN Symmetry because we can go multiparty, we can do all these wild and wonderful things on top.
So I'm like, we simplify it and then we add all new complexity by building another layer on top.
But, that's all good because I'm hoping that that won't be my problem and somebody else can do the implementation on top.

Adam Jonas: 00:13:04

So we've covered robustness.
Are there other things?
Yeah, I mean, what else do you have in mind when you're talking about that principle?

Rusty Russell: 00:13:12

So at the moment, we have a fairly complicated state machine with just the way that we deal with updates.
And when Greg implemented  Eltoo, he did roll in the simplified update proposal that I made a couple years ago now, where basically instead of both of us proposing changes at the same time. So the basic way our peer-to-peer protocol works is that I go, okay, add this, add this, add this, resolve this, resolve this.

## Peer to peer protocol

Rusty Russell: 00:13:37

At the same time, you can be proposing changes and we commit to each other and we kind of roll this thing in and eventually it's okay.
That protocol was something that is optimal, but also introduces a significant amount of complexity.
And it turns out that if you just take turns in adding updates, then it's a lot easier to understand the protocol.
It is theoretically slightly higher latency in the case where we both want to make changes because you end up having to wait for me and then it's your turn.
But in practice, while that adds some latency in that corner case, it also gives you more opportunities for batching.
So if you're really being hammered in both ways, you don't lose.
Right?
The latency of individual payments may go up, but the latency of the whole system is better because we end up just you end up doing five commitments at once because you've been waiting.
So with that in mind, I think simplifying the pure level protocol can help us somewhat.
And in fact, that simplification is a subset of the current state machine, in fact, so it turns out to be pretty nice.
And once we've got that, we have then the ability to knack changes.
So at the moment, I expressed to your node, there are certain things I will not allow.
Here's your maximum of HTLCs, here's your maximum HTLC size, all these restrictions because there's no way in the protocol for you to send an update and me go, no, no, no, I don't like that one.
We have to go through a whole round and then I have to close it out.
At some point, I'm left holding the commitment transaction with that thing that you put in.
I have to tell you what you can't do.
If we have a Knack protocol where you're going to know I'm going to reject that and force you to go around again, then that means that I no longer have to tell you what my restrictions are.
You can try everything and I just go no that doesn't work and close it out.

It's a fairly simple protocol change. But if we tried to do it in the existing protocol where we can have change from both sides in flight, it's a bit of a nightmare.
Whereas when we've got this turn taking protocol, it's much, much easier.
The other thing that happens with the turn taking protocol is if we want to do some kind of upgrade to the channel, we want to splice or we want to upgrade to a new kind of channel.
It turns out with the current protocol, we have to have a whole quiescence protocol to go, hold on, I want you to stop sending updates.
You go, cool, I'm ready to stop sending updates.
We clear all the updates and then we're ready to go.
With turn taking, it happens automatically.
When it's my turn, by definition, you haven't got anything in flight.
So I can say, hey, it's time to upgrade.
And it's much simpler in that way too.
So this is something that we just learned through experience that we over-designed the original protocol.
And now whether this becomes a separate change or goes in with an  Eltoo change or not, this is something we're going to discuss at the summit.
But from my point of view, we end up with a more robust and simple protocol at the end of this.
And it turns out that supporting both is actually pretty easy.

Adam Jonas: 00:16:10

When we were talking about  Eltoo, you're talking about changes and you're sort of casually mentioning the soft fork piece of it.
I mean, there's not going well, there's Greg Sanders will be there and he's obviously thinking about this, but you don't really have the people at the table that are actually doing like would be pulling the soft fork together that really understand the lightning case, I guess.
Maybe AJ, maybe Instagibbs.
The list gets very short after that.
So, like, how are you able to communicate those needs down to the lower layer?

Rusty Russell: 00:16:47

Well, I think the `ANYPREVOUT` cases have been pretty strong for a long time.
The question's always been, do we want other soft fork as well?

## CTV

Rusty Russell: 00:16:54

And people are like, oh, if we had `OP_CTV` and `OP_CHECKSIGFROMSTACK`, we can also do it.
Sure.
I can probably build a car out of matchsticks and snot, but I don't want to.
And don't make me do it.

Adam Jonas: 00:17:09

Could you do that?

Rusty Russell: 00:17:12

A theoretical engineer probably could do that.
I could not do that.
I'm not crafty at all.
But, okay.
That is probably an aside.
We don't need to go down.
But `OP_CHECKSIGFROMSTACK` is like, it's cool that you can even make that work.
But it is a terrible basis for just about anything.
And it's more like a game we could play as far as what's the most obscure way we could do some kind of introspection.
And the answer would be, `OP_CHECKSIGFROMSTACK`.
And the proposals that are in that cluster, and there are a few, are pretty clean, pretty well understood.
AJ would definitely be the person unfortunately he's not here in New York he's kind of done a fair bit of travel recently he was like "no I'm not going".
So I'm hoping that while we're in New York he is in his mountain lair somewhere coming up with a scheme to activate `ANYPREVOUT`.
That's if you're listening, AJ, I hope you're going to make that prophecy come true.
I think, we understand that we want this and we've wanted it for a fair period of time and nothing else has come up that's gone, oh no, we want this instead.
`ANYPREVOUT` by itself is a fairly simple piece.

Adam Jonas: 00:18:21

Not a precluding piece to other things that we can do in the future.

Rusty Russell: 00:18:24

Absolutely.

Adam Jonas: 00:18:25

This is the two-way door, one-way door kind of thing.

Rusty Russell: 00:18:28

In this case, we will want `ANYPREVOUT` even when we have full covenants and everything else.
So I'm pretty confident to say this is something that we should enable.
Right?
Now that said the detail the fine details you know hand wave hand wave I know try not to spend too much time coming over details but I'm pretty happy that somebody will come up with a proposal.
We will vet it and make sure that it works.
And away we go.
Greg Sanders, of course, will be the person to talk to.
He's been doing both sides.
I know he and AJ are all over this.
I trust them to weed through all the different possibilities, come out with a proposal, and then we'll tear it apart and then go again and do it properly.

Mark Erhardt: 00:19:07

Yeah, I believe it's live in inquisition already.

Rusty Russell: 00:19:11

Yeah, exactly.
So, you know, I think we're well on the way to getting that.
Now, just to set expectations correctly, even if we saw for tomorrow and it activated the week after, there's a little latency involved here, right?
We still need to then go through and implement it, roll it out, it gets spec'd out, it gets packed together, then we ratify it.
We get two different independent implementations both to implement it and interoperate and make sure that works.
Then it's spec final.
Then everyone else can go ahead and implement it.
Then it can roll out on the network.
Then everyone can upgrade.
Then once both your peers are upgraded, then now you can open a new channel.
A new channel will be one of these cool, Eltoo channels and everything else.
So, this is a long road, right?

Mark Erhardt: 00:19:57

Yeah, we were just talking with El and Oli, how one and a half years after Taproot's been active, simple Taproot channels are close to being spec out.

Rusty Russell: 00:20:07

Yes, exactly.

Mark Erhardt: 00:20:08

We know what you mean.

Rusty Russell: 00:20:10

And the other thing is that, look, it enables simplicity, it makes things a lot nicer for us, and it makes it cleaner, but not immediately.
At the moment, it's just work.
Because we don't get to drop anything that we're currently doing.
Now, eventually, sure, we do.
At the end of the road, there's this beautiful rainbow and there's unicorns dancing and everything else.
But we have to trade through a lot of unicorn crap.

## Pushing privacy and robustness to the front of the line

Adam Jonas: 00:20:35

This goes back to the open, which is privacy and robustness.
They always go to the end of the line.
So if you're never prioritizing them,
you're never prioritizing those things which never get attention.
It's sort of the equivalent of like, it's not tech debt, it's like philosophical debt.
And so, yeah, how do you push those to the front of the line and put them front and center?
Is it because they can come in the form of new features that it's time for?
Like, yeah, how do you push those forward?

Rusty Russell: 00:21:07

How do you push those forward?
You have that internal compass of, you need to spend a certain amount of your time on stuff that's literally broken on fire and everything else.
You need to spend a certain amount of time on other things.
As an engineer, this is the eternal battle between...
Just look at me personally, right?
I lead the core lightning team.
There's a certain amount of just dealing with time sheets and just doing random managerial overhead that I have to do.
There's a certain amount of like peering on random podcasts to talk about stuff.
There's a certain amount of actual coding that I have to do on core lightning features that people want because, scalability, whatever thing it is, right?
Oh, well, this is a cool new feature.
We should do that.
And then there's the protocol work as well right so there's always more things to do well in any fun job like working on this there's always more things to do than you necessarily have time for you have to prioritize so to answer your question how do you do that And the answer is that you have to reserve a certain amount of time for long-term work.
You just have to.
And you have to be aware through experience that if you do not explicitly reinvent some of your time, it'll never be a good time.

## The dynamics of developing a spec with commercially associated implementations

Adam Jonas: 00:22:18

I have two things to push back on.
One is LDK is a little bit of a maybe a question mark for me, but the others are three commercially driven implementations.

Rusty Russell: 00:22:30

I didn't realize we were commercially driven.
Okay, good.
I like that.

Adam Jonas: 00:22:35

And so, well, they have to be, I mean, they're companies, if the companies don't exist, do these implementations exist, I guess?

Rusty Russell: 00:22:45

So that is a very good philosophical question.
And hey, I work for a startup, right?
And you should always be thinking what happens if my startup collapses because almost by definition right that's the endgame for most startups is like they fail right and so when you have an open source project and you're like well I'm running this what happens after this to some extent the answer is, I'm gonna keep working on this whatever happens unfortunately my wife has given explicit approval for me to take some time off and work.
Should all of us fail?
We've had this discussion, right?
She's been like, cool, that's okay.
You can go do that.
At least for a while before you have to get a real job again.
So I feel fairly confident to go, we're going to move forward.
And maybe not as fast as we are at the moment.
But, there's some future there.

Adam Jonas: 00:23:24

I guess my other bit of that was because they're commercially associated, maybe not driven, commercially associated.
That means that features get pushed to the front of the line.
Because I've worked for companies, I know how it works.
So when you're talking about, ring fencing things and making sure that we're thinking long term.
These are different than just like building a product that's in JavaScript and can wow an investor.
There is a philosophical side to what's happening here.
And there is a collaboration side of no implementation can do it by themselves.

Rusty Russell: 00:24:07

Yes.

Adam Jonas: 00:24:07

And so those dynamics just don't seem to add up to a long term thinking and long term moving the ball forward in these kinds of dimensions.

Rusty Russell: 00:24:21

So the piece that you're missing here is the pie is still growing, right?
And so there is more emphasis on growing that pie and doing those bold new things because the world is still in front of us right light network as it is in 10 years time is much bigger than light network today with that assumption how do you lead how do you become the one everyone wants to be and the answer is you do the cool new things.
And that's not so much features.
It is that focus on the next, basically the lightning 2.0. What are the cool new things coming down the pipe?
Is it  Eltoo?
Is it LN symmetry?
Have you already got those, right?
Is it Taproot channels?
Like look at LNDs, huge amount of resources they're putting in to doing that.
Now, a lot of that is commercially driven.
Why?
Because it gives them cool points and it makes the rest of us sweat.
And we have to then catch up, right?
This is always the way.
One of the implementations does something really cool.
And I'm going, on the one hand, I'm going, wow, that's amazing.
On the hand, I'm going, shit.
Now we have to do that.
Right?
There is definitely a commercial reason to do these things.
Now, is it theoretically possible that you could avoid doing any real work and just concentrate on, adding features to your own implementation.
I think it's too early.
At the moment, you can't do that because no one else is doing that and you will get left behind.
There are four implementations out there and there is choice in what you can run.
So everyone is sweating at the moment a little bit.
There's something of a treadmill effect.

Adam Jonas: 00:25:51

My other side of that.

Mark Erhardt: 00:25:54

Isn't it five, meanwhile, with Electrum also in the mix now?

Rusty Russell: 00:25:58

Electrum has been in the mix for a while, but we haven't really seen them pushing the boundaries of the spec process.
They're quite happy to kind of follow along and meet the requirements.

Mark Erhardt: 00:26:08

Okay, so you're talking about four that are participating in the spec.

Rusty Russell: 00:26:12

There are three other teams I can hit up when I want someone else to interoperate with on some new feature who are really going to drive it forward.
And those are really reliable.

## Expecting new implementations

Rusty Russell: 00:26:21

So there's certainly other implementations to come up.
And I actually expect to some extent that LN symmetry may open some new opportunities because people go, actually, I can implement that now.
That is a serious subset.
If I just implement that, maybe I've got an advantage over the others who have legacy they've got to still handle whereas I can just have a clean implementation that just does this new thing so we're gonna see these, these new kids coming up with their, I don't know Kotlin implementation I've heard of those I know some some some some of them one of those languages, you're like you implemented in what I've heard of that kind of thing.
That may be the next thing.
And that's exciting for me.
I think, that brings, new blood, just a new design space, a new point of view to the implementations, and that's always great.

## Privacy revisited

Adam Jonas: 00:27:02

Privacy.
Privacy, yes.
So we were talking about sort of the robustness dimension and that sort of that principle.
What's on your mind about privacy?

Rusty Russell: 00:27:11

Well, privacy, I think, privacy is a bottomless well, right?
You can keep going on privacy for just about forever.
There are some fairly obvious things you can know on privacy.
I think some of them are just like a quality of implementation.
So the Oakland Protocol, which was discussed at the last summit, which is this idea that you can shield exposure to where HTLCs have gone through because you can make it a lot harder for people to probe.
Hold on, you used to have this much in channel, now you've got this much.
I can tell therefore that that payment that went through me went out this channel for you.
So we can actually shield a lot of that using the Oakland protocol.
So that requires widespread implementation.

Mark Erhardt: 00:27:48

As a reminder, that was basically just under-reporting your channel capacity.

Rusty Russell: 00:27:53

That's right.
Yeah.
You act as if the payment may have gone out multiple channels.
You artificially restrict their capacity by some amount, in the case where your maximum HTLC size has hit the bounds of the capacity.
So it doesn't actually make a difference in a lot of cases, because for most implementations, you set the maximum HTLC size that they can go through to, say, 10% of your channel capacity anyway.
So as long as you've got more than 10%, they can't tell.
They literally cannot tell.
When you're under 10, the question is like when you're on the boundary you can you can start probing and so at that point you start the Oakland protocol and well, we're going to actually let you use slightly less capacity than we actually have because we don't want to leak that we didn't send the HTLC out through there.

Mark Erhardt: 00:28:34

Couldn't prober still send multiple payments, lock up more funds and then probe like the 40 to 50% by having four other 10%?

Rusty Russell: 00:28:45

Exactly.
So you can do it with multiple probes, but the Oakland protocol basically restricts it because it gives you a fixed point where you go.
And some implementations actually restrict the total HTLC in flight.
So you have another thing that they can't basically exhaust the whole channel.
So there's that, there's low-hanging fruit like that.
There's splicing, which just messes up your graph a little bit, so it makes it harder to...
Dual funding particularly allows you to combine multiple things into one transaction, just the common ownership heuristics starts to break down.
This is useful.
There's a whole pile of different fun things you can do once you've got splicing and you can splice in and out and everything else and just mess people up, which is kind of nice.
Particularly if we start to see things like Payjoin of things coming out of splices and really really kind of a lot more.
So once your Lightning channel is also used for onchain things through splicing, I think it becomes a lot more complicated to see exactly what's going on, which is just a nice low-hanging fruit that we're going to get.

Mark Erhardt: 00:29:40

Especially if we no longer announce which UTXO a channel is from.

Rusty Russell: 00:29:46

The gossip question, right?
Do we break the linkage between for anti-spam reasons?
We say, hey, improve.
I have this UTXO and this is the basis of our channel.
We're going to have to weaken that slightly anyway, because chatbot channels are going to have a different form.
So we need a new gossip thing anyway.
At that point, we're going to have this debate this week as to whether we go all the way and say, hey, we don't have to prove the funds for this particular channel.
One proposal is that you prove that you have some funds and that allows you to announce a certain number of channels or a certain capacity of channels, but they don't have to be related.
Cool.
Just prove that you have some funds.
So you can't claim, hey, I've got all these giant channels without some anti-spam requirement.
But we could loosen it out and say, cool, you proved you got a million sats.
You can advertise eight million sats worth of channels.
Right.
To hand wave, there have to be some other restrictions in there.
But that would potentially allow us to break this heuristic where you're basically announcing your channels.
Now, the gossip announcement, that's my fault actually, because I put that in the protocol.
And I was thinking, well, you're public anyway, it's fine.
But it turns out, of course, that leaking that one piece of information then often leads to a lot of other information that you did not intend to be leaked, particularly about unannounced channels, which we've recently had improvements on, right, with with SCID aliases, we're no longer leaking those, but indirectly you can now start to tell what's happening with private channels, which was, or unannounced channels, which was never the intention.

Mark Erhardt: 00:31:04

Just through taint on-chain transactions and pedigree?

Rusty Russell: 00:31:08

Yeah, well, just the fact that now you can see, okay, I know this channel came from you, and therefore I can see this other UTXO went to a Lightning channel, I'm pretty much sure that that is yours as well.
And you know, you can start to join things together just doing things like that.

## What broke when fee rate spiked?

Mark Erhardt: 00:31:22

So I would like to call back to you said a bunch of things broke when the fee rates spiked.

Rusty Russell: 00:31:27

Yeah.

Mark Erhardt: 00:31:28

And I was curious what what broke for various lightning implementations.
Can we get a little bit into that?

Rusty Russell: 00:31:33

Yeah, absolutely.

Mark Erhardt:

Robustness for fees folks.

Rusty Russell: 00:31:36

So yeah, so part of the problem at the moment is that you basically have to agree on what fee you're going to pay.
Now there's only one side pays fees.
It's the person who originally proposed it.
And they're the only one who can propose fee changes.
But fees are also charged on second stage HTLC transactions.
And that comes out of the HTLC.
So it may not be paid by the person.
So as a result of this flow through, you actually care what the person normally paying the fees sets it to.
So you have to have some agreement.
We tend to be pretty broad.
Now it turns out if you restart BitcoinD it seems that it often just drops a bundle of shit and starts to think that the floor for fees has dropped back down.
So people will restart the BitcoinD, it would go, no, no, min relay fees, all good.
We're, you know, we're back on like, one set or whatever.
And you would propose that to your peer who has not restarted and you fucking want no, and you could get forced closures that way.

Mark Erhardt: 00:32:29

Sure.
Yeah, this is meant to run consistently, and we don't get good fee estimates until a couple blocks have been found.

Rusty Russell: 00:32:36

That's right.
So some of that is just a learning experience, right?
The answer is that basically you shouldn't let the min fee drop over some period of time.
You just go, we're going to ratchet it up to a certain amount.
And then if it's been there for an hour and we're still getting, okay, then we start to let it down.
This is a workaround for that.
There's another issue that the Eclair people spotted that I think actually Bastien spotted, which is where you go on chain, you go to redeem an HTLC, you go, it's actually not worth me paying the fee that would be involved to redeem this because fees are high, whatever else, so I'm not going to, you still have to close it upstream at that point.
Normally you'd wait till it spans and then you go, whatever, but if you're not going to spend or you're not going to push paying a fee to force it through, you now need to make the call to fail it upstream.
You're at risk at that point because you could lose the HTLC, but you've already decided to write that money off because it's not worth.
But if you don't close it upstream, upstream then closes on you because you've left this HTLC and clock's ticking.
Upstream goes, right, I'm going to close the HTLC.
So you can end up with channel failure because of this issue.

Mark Erhardt: 00:33:37

Right, so you have an HTLC that's so small that at a high fee, it's not worth claiming.
You write it off, but you have to.

Rusty Russell: 00:33:44

But you don't actually close it out to the peer.
So that's a quality of implementation issue and you end up closing another channel, not just the first one, right?
So you end up this cascade effect.
So we had a little bit of that.

Mark Erhardt: 00:33:56

Could you clarify?
So the fee in a commitment transaction is paid by the channel proposer?
Like the person that started the channel.
So it's always the one that started the channel that has to cough up the fees.

Rusty Russell: 00:34:09

Yes.
But remember with modern anchor channels, your fee is actually pretty low ball.
It's just going to be enough to get you into the mempool, and you're going to use child pays for parent on one of the anchor outputs to actually bump the fee where it is.
So it reduces the problem that we have.
Just like I have to guess what the fee rate is going to be in future whenever I want to spend this to, I have to guess what the min fee is going to be in future. So I can spend this.

Mark Erhardt: 00:34:30

The dynamic mempool minimum fee.

Rusty Russell: 00:34:32

Yeah, that's right.

Mark Erhardt: 00:34:34

Which can be higher in the last few months.

Rusty Russell: 00:34:36

It's not actually that much of an easier problem, but at least the number is probably less.
So, you can lowball fees to some extent, whereas before we had to bump fees up quite a lot.
We used a magnifying factor to go, well, I could go as high as this.
The ultimate answer to this is to package relay, version 3, all those things.
So we can actually have no fees here and have all the fees in the child.
Well, the ultimate answer for this is Eltoo and everything else.
But meanwhile, package relay lets us not have-

Adam Jonas: 00:35:03

But even with Eltoo, you still need to have a mechanism to be able to broadcast on-chain.

Rusty Russell: 00:35:07

But in that case, we use a `SIGHASH_ANYONECANPAY` signal.
You have to bring your own fees.
And you bring your own fees through, right?

Mark Erhardt: 00:35:13

Yeah, sure.

Rusty Russell: 00:35:14

And in a more efficient way than child pays for parent, you actually bring your own fees on the board, which is really cool.
Anyway, so this means that then the person closing actually is the one who bumps it and then pays fees above some de minimis level at the moment.
So that actually works a little bit better and is a bit more incentive compatible.
So you want to close the channel, you're paying the fees.
Whereas the moment like, sometimes you want to close the channel, it's just like, I'm paying the fees.
That's not right.
Right.
So, so it does help to some extent to solve that.
So yeah.

Mark Erhardt: 00:35:42

So, so basically the commitment transaction must at least with anchor output still meet the dynamic minimum of the mempool.
We've seen that spike to above 10, I think 15 maybe in the last few months.

Rusty Russell: 00:35:57

That's right.
Now you've got some time, you have a longer delay on your channel, you've got some time to get it in.
So a transient spike doesn't hurt you so much, but you do have to get in.
And this is one of the reasons that we talk about, Bitcoin Core traditionally has divided rules into like the hard rules of what can go in a block and then the software rules about what can propagate.
It's like when you're using it at a layer two, you don't care.
Like if you don't care why your transaction doesn't go in, whether it's because it's illegal or whether it's because it's considered immoral by the network, right?
Just these soft rules don't actually make a difference to you.
They're both really good, really important rules.
And so there's been more focus than there perhaps has been in the past, where these soft rules about what's allowed to propagate through the network have been seen as less important.
Yes, to some extent they are because they're changeable, but in a sense of you're operating, building on top of it, they're both really good.
So there's been a proposal to have a workaround where we actually start spraying things through the Lightning network so that people will jam them into their local nodes.
It may still happen at some point if we really need to.
As long as we can get them to miners.

Mark Erhardt: 00:36:57

Is that the third approach next to Nostr. 

Rusty Russell: 00:37:00

Yeah, that's right.
Exactly.
You know, we just all you separate them over all the networks as long as there's a minor missing, you might pick them up.
I know there was there was a proposal to have some kind of local package relay where you could kind of inject a package locally.
And then we could just paper over the rest if we needed to.
Obviously, we'd like to just go all the way to the, hey, do the whole peer-to-peer protocol for an upgrade, we're all good.
But you know, that's something that we could potentially do if we had to.
But, in the meantime, it's interesting to see the phenomenon.
This stuff happened because fees were so low for so long that it got pushed to the back of the line, right?
Even we were one of the first people to implement the old anchor system, which had fees built in.
And then when people implemented it, they went, actually, we want zero fee anchors.
And so that became whatever else implemented, we lacked.
Core Lightning did not implement that because it meant basically you always had to bring your own fees and you had to have a reserve for that and you had to basically be able to do a lot more dynamic fee stuff.
And it just wasn't on fire until it was.
And that PR is sitting there.
It's going to get merged.
And it is going to get merged because I'm release captain and it's damn well going to get merged before the release.
So we're finally fixing that.
The one good thing about volatility like this is it does shake your priorities up a bit and reminds you that you've got to address these things.

Mark Erhardt: 00:38:11

Pushes adoption of best practices, better fee estimation, better output type usage, your excel management, all the things.

Rusty Russell: 00:38:20

All these things that are not important until they suddenly are and you put the engineering work in.
Look, life's all about trade-offs and I actually can't, you can't be too harsh on people for going well, you know, I decided to defer that.
Like people give crap to Moon Wallet for example for using on-chain transactions.
I'm like look it's an engineering trade-off that's fine you know as long as you go in with your eyes open.
Now sure your timing isn't going to be perfect but hell if you'd asked me two years ago I would have said no no this stuff is critical you know fees are going up you've got to do it.
I mean really?
You actually had two years to get away with it.
And you could kind of bumble your way through the recent fees spike and go, okay, for all I know, we'll have another two years of low fees.
And you go, okay, maybe you panicked a bit too hard.
Just for the record, I do not think that's true.
And you should totally get your shit together now.
But I can't blame anyone else who made the same kind of decision and went, well, actually, if you're not on fire right now.
But yeah, it is part of a robustness approach means addressing these things.
I think we are slowly moving our way through the list, but there will always be things that you wish you had done earlier, but that's engineering.
You can't do all the things.

Mark Erhardt: 00:39:19

Right.
So the rainbows and unicorns in this case look like v3 transactions with ephemeral anchors, zero fee commitment transactions, package relay.

Rusty Russell: 00:39:33

Package relay.
And Eltoo also solves some of these problems.
But we have similar incentive problems, and you need to have the package relay as well, and v3, I think, for it to get  Eltoo to be secure as well.
We currently have two anchor outputs, and that makes your transactions bigger.
So in a low fee environment, you could argue that you shouldn't implement anchors because you're just making a bigger transaction for unilateral closes.
And you're spending, basically, your transaction is almost twice as big because it's got these two extra outputs.
With package relay and v3, I think we only need one anchor that we can share.
We're still in anchors.
You know, you're still a little bit bigger.

Mark Erhardt: 00:40:06

And the ephemeral anchor is smaller because it's just an uptrue.

Rusty Russell: 00:40:10

Yeah, that point, the ephemeral anchor, it shrinks right down.
So it's pretty good.
And at that point, you start to go, yeah, it's a bit of a wash.
And output's still not free, but, it's cheap.

Mark Erhardt: 00:40:19

Nine bytes.

Rusty Russell: 00:40:20

Nine bytes, Someone's on the math.
Cool.
So yeah, yeah that look that that's definitely the where we want to get to and again, it's an Maybe no one will notice if it takes a while to get there, but definitely it's one of those, the engineers look at these things and see problems.
And this is one of the problems we see and we crossed off the list and then we'll work on the next one.

Mark Erhardt: 00:40:38

Yeah, Gloria and I have been writing, "Waiting for Confirmation" series on the Optech newsletter.
Next week we're going to talk about mempool policy as an interface for layer 2 protocols.
So, not preparing for that yet, but I'm thinking already.

Rusty Russell: 00:40:56

Yeah, I look forward to reading it.
It's going to be interesting.

Adam Jonas: 00:40:58

What else is on your mind, Rusty?
Anything else to mention?

Rusty Russell: 00:41:02

Okay.
I think my mind is still somewhere over the Pacific Ocean right now.
So I'm not sure that it's all present.
Look, as I said, we've been going eight years on this and it's been a fantastic journey just to go through with this incredibly bright set of inspired engineers.
I'm not a morning person, but I still get up for 5.30 a.m. calls every two weeks on Tuesday, my time, Monday, everyone else's time, to hang out and like, and collaborate on the spec and do everything else.
It was really interesting to go through those days when there was excitement about lightning in the early days, and then everyone was pretty much pivoted to, no, Bitcoin's a store of value, payments aren't important.
And we're like, but we're working on payments.
Like, we're working really hard, you know.
And, to see it kind of come back around, now people are like, wow, this is actually usable.
Like, it's really cool.
I think it's a little bit of, it's a little bit gratifying to kind of, everyone to kind of come back to oh yeah this is this is actually pretty nice thank you that's good but you know we still have so much more to do and I think everyone's pretty aware of that to some extent you know this is a job that will never be finished, but it's going to get harder and harder as the network grows to change things.
And so there's a lot of effort on trying to make sure that we've got things correct now, we've laid the foundation correctly.
So that, you know, while, unlike Bitcoin, which is completely, ground into stone.
We do have some ability to move on the protocol, but over time it will become less and less just because of the weight and the inertia of things.
I look at the IPv4 to v6 transition, right?
It's going great.
Any day now, right?
Two weeks, TM.
You know, so, and there were things that we put in the protocol that were way overkill.
The onion stuff, like the onion routing, but just with everyone was very clear that while nobody's screaming for this today, it is a critical component that needs to be in the version zero.
It needs to be in there before anything else.
So I think we're in, all up.
You step back and you were in reasonably good shape.
And yeah, as I said, engineers tend to focus on the problem.
We tend to focus on this needs fixing and this needs fixing.
We need to do this and this.
We don't often look back and go look at, all the things that we've achieved over this time.
And so for me, this week is a little bit of both.
A little bit of kind of going, yeah, look at all the stuff that we've done.
Look at the excitement that has moved up.
The people building things on top of what we're doing.
That's really exciting.
And that's where more people will come into there and they're going to come into the low level and go, what I want to do?
I want to implement Lightning protocols from scratch.
You know, I welcome the crazies.
If you're listening to this and going, that's what I want to do, I want to implement that.
You're my people.
I love that.
But I just accept that most people will be building on layers above us.
And that's where the excitement will move up to.
But still, our job is going to be to just continue that incremental engineering and just making it better, little by little, and those wins will accumulate.

Mark Erhardt: 00:43:36

What are the things that you're excited to see being built on top of Lightning?
Well, I'll let you answer first, but I might have follow up.

Rusty Russell: 00:43:43

What is exciting?
I always said that there will be some killer application of Lightning that I will think is stupid because I'm old.

Mark Erhardt: 00:43:52

And you know how I feel about inscriptions.

Rusty Russell: 00:43:55

Yeah, yeah, exactly.
I don't even know what it will be.
And part of that is just the problem is that when you don't have a technology, when you don't have a way of making micro payments, what we would call real micro payments, not like making tiny payments, by definition, any business model or things or infrastructure that would require that do not exist because they can't.
And so there's an inertia behind that, right?
You create a technology, but then there's no immediate use for it.
There are a few fringe uses and people who can use it and, they can kind of like enhance things they're already doing.
But the whole Greenfields thing of things that didn't exist or didn't make sense before that suddenly makes sense.
And you know, I think at this point, Nostr tipping is probably something where people think, it didn't make sense before.
You couldn't really do that with credit cards.

Mark Erhardt: 00:44:43

It didn't.
I must admit, like on Stacker News, when I want to tip a post, and the little lightning zooms across the screen when I tip.
It's just like I started Lightning wallet, but I put in a few thousand sats and I got some tips back, bigger account number now.
It's neat.
If I ever want to get those sats back, I can just pull them back to my Lightning wallet.
It's pretty neat.

Rusty Russell: 00:45:08

And look at Cashu and some of the other things, the Fedimint and stuff using Lightning as a glue, right?

Mark Erhardt: 00:45:12

Yeah.
And just international payments.
So simple.
I traveled to Central America a while back and being able to just go and pay with my money there, everywhere, that made it very real, much more real than all this theoretical pondering on what the world will look like.

Rusty Russell: 00:45:35

Yeah, absolutely.
And which of these will be the, is it like slow accretion of all these things?
I don't know.
I'm not smart enough to tell what's happening, but it is exciting.
It is fantastic to see people actually use this and explore things.
And these people will build things that I could not even conceive of.
I certainly couldn't have built myself.

Mark Erhardt: 00:45:54

It's hard to see the potential of the black box thing when you're in the nitty gritty building the black box.

Rusty Russell: 00:45:59

That's right.
Yeah, and I'm sure any guesses that I would make about what it would do will become horribly dated and will be wrong.
Because you're a product of the pre-existing conditions, right?
It will take someone for whom someone Lightning native will come along and do something that yeah, probably the shaggiest, dumbest thing I've ever heard of.
It'll turn out to be a huge success and it shows that I knew.
That's why I'm not a business guy.
I'm just an engineer.

Adam Jonas: 00:46:25

Unreal.
Thank you.
Thank you for doing this.
Thank you.

Rusty Russell: 00:46:30

Thanks for having me.

Mark Erhardt: 00:46:31

Yeah, thanks.

Adam Jonas: 00:46:39

So did that live up to your expectations?

Mark Erhardt: 00:46:42

Yeah, I think so.
Looking back eight years in with people that got in really early that had a 20-year vision for it from the get-go.
It's refreshing.
I think it's really nice thinking back, writing so much, reading so much about it when Lightning just came out.
Yes, there's been a lot done.
It's getting used by people.
It's very cool.

Adam Jonas: 00:47:05

So 8 out of 20 means we're 40% in.
Are we 40% there?

Mark Erhardt: 00:47:09

I don't know.
Maybe it'll be a little faster.
It's already usable.
We're seeing some projects being built on Lightning.
I mean, last year I could buy pupusas in a place with stomped earth ground but lightning network payments and I don't know that was my plan so it's it's it feels like we're definitely some part there where you can use it, but some of the features that I've been hearing about for years still need to happen.
So yeah, maybe 40% is a good value.
I don't know if 20 years is the right amount, but taking that sort of approach and having that in mind makes it easier to.

Adam Jonas: 00:47:49

Is it always just 20 years out?
Do you take this?

Mark Erhardt: 00:47:54

I don't think it's like block times.
It's more like building a new protocol and also getting that person that will be a Lightning network that builds the killer use case just takes a generation maybe.
Anything really big that changes stuff progresses in 10 year steps.
So two steps.
Yeah, I think so.

Adam Jonas: 00:48:15

Cool.
Well, hope you enjoyed listening to it and we'll see you next time.
