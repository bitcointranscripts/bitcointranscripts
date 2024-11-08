---
title: Burying Soft Forks
transcript_by: Ringoz1 via review.btctranscripts.com
media: https://www.youtube.com/watch?v=C7wG2ngayy8
date: '2022-02-25'
tags:
  - security
  - taproot
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
episode: 54
summary: |-
  In this episode of Bitcoin, Explained, hosts Aaron van Wirdum and Sjors Provoost revisit the Taproot activation saga, this time to discuss burying of soft forks.

  Taproot, the last soft fork to have been deployed on the Bitcoin network, activated in late 2021. Now, Bitcoin Core developers are considering to 'bury' the soft fork, which means that future Bitcoin Core releases will treat Taproot as if the rule change has been active since Bitcoin's very beginning. (With the exception of one block mined in 2021 that breached the Taproot rules which have since been added to the protocol.)

  In the episode, Sjors explains what the benefits are of burying a soft fork, in particular pointing out how it helps developers when they review the Bitcoin Core codebase or when they perform tests on it.

  After that, Aaron and Sjors outline a potential edge case scenario where burying soft forks could, in a worst-case scenario, split the Bitcoin blockchain between upgraded and non-upgraded nodes. Bitcoin Core developers generally don't consider this edge case - a very long block re-org - to be a realistic problem and/or believe that this would be such a big problem that a buried soft fork would be a minor concern comparatively. However, they explain, not everyone agrees with this assessment entirely.

  Finally, Aaron and Sjors touch on issues like whether soft fork activation logic should itself be considered a soft fork, and whether soft fork burying logic should be considered a consensus change and/or require a Bitcoin Improvement Proposal (BIP).
---
## Intro

Aaron van Wirdum: 00:00:20

Live from Utrecht, this is Bitcoin Explained.
I love it.
Sjors here we are again.
It feels very retro.
We just recorded three-quarters of an episode before you realized you weren't recording anything.

## No Counter

Sjors Provoost: 00:00:35

Yep, there's this little device and you have to put the SD card in it.
Otherwise you'll press the record button and you'll see all the volume and all that stuff.
It looks very good, but there is no counter.

Aaron van Wirdum: 00:00:46

Yeah, I think that used to happen almost every time in the first couple of months.

## Introduction

Sjors Provoost: 00:00:50

No, I think we've only done it once.
No, more than a few minutes.

Aaron van Wirdum: 00:00:55

What?
No, we did it all the time, Sjors.
Did you forget about that?

Sjors Provoost: 00:00:59

Maybe I suppressed the memory.

Aaron van Wirdum: 00:01:00

Anyways, so this time I hope you're recording and we're going for take two.

Sjors Provoost: 00:01:06

I see a clock ticking, so that's good.

Aaron van Wirdum: 00:01:08

Nice.
We're going to discuss burying soft forks.

Sjors Provoost: 00:01:13

All right.

Aaron van Wirdum: 00:01:14

Yeah, this is one of these topics that I sort of knew was a thing that was sometimes discussed by developers, but also based on the discussion that I was sort of eyeing on the Bitcoin development mailing list, I could tell that it was kind of a niche, not super important, kind of big deal sort of thing that only developers that are very far into the weeds kind of cared about.
So I never really paid attention to it.

Sjors Provoost: 00:01:40

But then we were desperate to find a new topic and I found it and you found it interesting.

Aaron van Wirdum: 00:01:45

Yeah, I thought it was actually kind of interesting.
It's one of these topics that, it might be niche, but it still has some sort of broader implications about, how do we think about Bitcoin.
In a way, I've always found protocol changes the most interesting part of Bitcoin because it kind of gives you a very existential idea of what Bitcoin actually is.
Like if it can change, then you can sort of think about what conditions can you change it then or what is Bitcoin then?
You can get very philosophical about it if you want to.
But I don't think we're really going to do that today, but we are going to discuss burying soft forks.
So yeah, we have discussed Taproot and Taproot Activation in multiple episodes so far.

Sjors Provoost: 00:02:29

Five episode epic story.

Aaron van Wirdum: 00:02:32

It's like a mini-series within our podcast.
From start to finish, we sort of covered the whole Taproot activation saga.
And in a way, this is a new entry in that mini-series.
So I like it.

Sjors Provoost: 00:02:45

That's right.

Aaron van Wirdum: 00:02:45

Probably the last one.
Probably this will be the last entry because at this point, we're going to discuss, the soft fork happened, activation happened, it all went great.
And at this point, the question is sort of, how do we move forward from there?
How do we now retroactively kind of deal with the activation code and with taproot?
And that's what burying soft forks is about.

Sjors Provoost: 00:03:13

Yeah.
So one analogy that can be used, although we'll get to the philosophical discussion about that, is that activation code is a scaffold.
It's like when there's a soft fork, it's like building a new house.
And when you're building a house, there's a scaffold next to it.
And then the question is, what do you do with the scaffold when the house is done?
And that's kind of what we're going to talk about.
Can we just remove it somehow?

Aaron van Wirdum: 00:03:36

Yeah.
So this has happened before, but burying soft forks, it's not a completely new concept.
It is being discussed again, at least sort of on GitHub, not really on the Bitcoin dev list this time, I think, because I guess Bitcoin Core developers have already sort of agreed that this is kind of the way to go.

Sjors Provoost: 00:03:55

Well, it's still open, so.

Aaron van Wirdum: 00:03:57

All right.
So it is being discussed again, but it has happened before.
So I'll just let you explain, Sjors, what does it mean?
What is burying a soft fork?

## What is a soft fork

Sjors Provoost: 00:04:06

Well, I think you wanted to recap first what a soft fork is.

Aaron van Wirdum: 00:04:09

Yeah, sure.
Let's start with that.
You're right for those listeners that don't know that.

Sjors Provoost: 00:04:14

It's also relevant to explain how the burying works.
So a soft fork is a tightening of the rules.
And intuitively you might think, what?
How do you get new features when you have less rules?
Well, we've explained this in earlier episodes.
But basically, Bitcoin has a lot of ways to throw away money.
And so you can make all sorts of addresses, quote unquote, that you can send coins to.
And then anybody can take the money from those addresses.
And generally, you don't want to do that.

Aaron van Wirdum: 00:04:43

Yeah, you don't even need a signature.
There's just no requirements.
You can just take the money from these outputs or addresses, like you say.

Sjors Provoost: 00:04:50

So what a soft fork does, in practice, at least some soft forks do, is to say, well, there's now going to be slightly fewer ways to throw away your money.
So if you make this specific type of transaction, we're now going to call that taproot and you can only spend that with a valid Schnorr signature etc.
Etc.
Whereas before the soft fork you could just take those coins.
And this ties into the burying of the soft fork Because it turns out that if you look back at the history of the blockchain, and you see how many people have actually thrown away their money in the past, in a way that would now be called taproot, turns out that's only happened once.
So there's only one historical transaction that happened before Taproot activated, where somebody sent money to something that we now call a Taproot address.
And more importantly, somebody else took that money.
And that taking of the money would not be compliant with the modern Taproot rules.

Aaron van Wirdum: 00:05:46

Yes.
Well, actually, I'll have to correct you there a little bit.
So actually several people sent money to a Taproot address before Taproot was active.

Sjors Provoost: 00:05:56

But only one took it.

Aaron van Wirdum: 00:05:57

Yes.
It's only been taken one time.
Sending to such an address was always okay, of course, and is still okay, and that was never a problem.
It's a taken from that address that since Taproot is active, you cannot do that anymore.
But before Taproot was active, you could just take that money.

Sjors Provoost: 00:06:15

That's right.
And so this presents an opportunity to look at the Bitcoin Core source code, which currently just says, wait, when you see the blockchain for the first time, you think the whole thing, you look at the signaling, and then after a while, you've seen that the speedy trial activated, and now you're going to apply the new rules to the new blocks.
What you can do instead is say, don't worry about the signaling, just apply the taproot rules from the Genesis block onwards, pretend that taproot has always existed with one exception.
And that exception would be hard-coded in the source code, saying, well, Zaproot is always active except for this specific block.

Aaron van Wirdum: 00:06:53

Yes, and that block would be the block that includes the transaction that I just mentioned that took these coins.

Sjors Provoost: 00:07:00

Yeah.

Aaron van Wirdum: 00:07:00

They were sent to Brink, actually.
There's a blog post that was, while we're discussing it, let me just mention that real quick.
So it was actually taken by, or at least the Bitcoin developer named 0xb10c.
He sort of initiated it and then it was included by F2Pool, and it was sent, so these coins that were sent to Brink at the time.

Sjors Provoost: 00:07:27

That's very nice.

Aaron van Wirdum: 00:07:27

Not very important in the context of the rest of this episode, but a little detail.

## Exception block

Sjors Provoost: 00:07:31

No, and it turns out something like this has happened in the past with BIP16, back in 2012, that introduced pay-to-script-hash.
There was also one exception block.
So there is precedent of having an exception block in the Bitcoin source code in this way.
So the taproot would just have another exception block.

Aaron van Wirdum: 00:07:51

So let me recap that real quick.

Sjors Provoost: 00:07:54

Okay, and with SegWit, I just add is there is no exception necessary.
So SegWit rules can be applied from the Genesis block perfectly.
There's no exception.

Aaron van Wirdum: 00:08:02

Right.
Yes.
Okay.
So if you currently run a Bitcoin core node, better yet, if you sync a Bitcoin core node,
so if you start from the Genesis block. You start from the very first block that was released by Satoshi, and then you go through the entire blockchain to verify every transaction, every block.
Then what your Bitcoin Core node is currently doing is at some point it will check if there is blockchain signaling going on, and then it sees that there is in fact blockchain signaling going on.
And then from a certain block, it will start to enforce the taproot rules.
That's how a Bitcoin Core node right now works when it comes to taproot.
And then this proposal, which has been done with other soft fork  before, is that it will actually start applying the taproot rules from the very beginning, with the exception for this one block that has an invalid spend in it under the taproot rules, and we'll just ignore that.
Right?
This is the recap.
This is how it would work.
So what are the benefits of implementing this in Bitcoin Core?
Why is it better to start from block zero?

## Benefits

Sjors Provoost: 00:09:12

Yeah.
So I think the first thing to say is that this is not a dramatic benefit that we're going to talk about.
It's somewhat marginal.
However, we're dealing with very critical code.
So the less headache basically for developers, the more likely they spend their time finding real bugs.
First of all, it makes the code a little bit simpler, but that's very marginal.
So instead of saying, after this block, do X, it says, do X all the time, except for this block.
And the other side is that it makes testing the code easier.
So Bitcoin Core itself has tests that are run in something called the RegTest framework from regression.
And these tests, what these tests do is they simulate a fresh blockchain, so with a fresh genesis block or maybe the real genesis block, and then they create very low difficulty blocks.
So they very quickly can build a blockchain with 100 blocks or 200 blocks on it.
And then they can, you know, check all the rules basically.
So there's a test that says, okay, make sure that before Taproot activates, these rules apply and these blocks are still valid.
And then after Taproot activates, you want to, the test might check that the Taproot rules are actually enforced.
And so if you just pretend that Taproot has always been there, 1984 style. Then basically the test can be simplified because you only need to test for the enforcement of Taproot rules.
You don't have to test anymore for pre-activation scenarios.
So that's basically a simplification there.

Aaron van Wirdum: 00:10:42

Right.
So you've now mentioned two benefits.
One of them, it cleans up the actual code of the Bitcoin Core codebase.
And the other way is it simplifies tests that you might run because now there's less scenarios.

Sjors Provoost: 00:10:56

Well, those tests are in the Bitcoin source code too.
So yeah, there's fewer permutations to test, right?
Especially if you add up multiple soft forks.
Like, okay, we have to test before segwit, and then after segwit, but before taproot, those kind of combinations.

Aaron van Wirdum: 00:11:11

Okay.
So I think we can actually summarize it as it just cleans up the code.
It's a code cleanup.

## Code Cleanup

And the idea is essentially that the soft fork activated so long ago that it doesn't really make a difference.
Am I saying it right?

Sjors Provoost: 00:11:28

Well, we'll get to that, I think.
There's a second part to the cleanup that I want to emphasize, and then we can say that analogy.
The second thing is, now that we've said taproot has always existed, as in the 1984 example, we still have these signals that happened in blocks.
And, well, there's no point in looking at those signals anymore because we've already said segwit is always there or taproot is always there so why do we look at the signals.
So the second cleanup would be to simply not check those signals anymore so to remove the speedy trial essentially in this case and that has again somewhat of a benefit for developers. What it allows developers to do is say, hey, we want to change the activation mechanism itself.
Maybe we want to change the BIP9 system to something more like a BIP8 system.
And then we can just change the code, basically.
We don't have to copy the code and write a new piece of code.
We can change it entirely because the code is no longer used for anything.
So it's safer to just change it.
Again, that's marginal, but it's still nice.

Aaron van Wirdum: 00:12:35

Yeah, and it's also still code cleanup, right?
That's the benefit, essentially.

Sjors Provoost: 00:12:41

Yeah, so especially if you understand that BIP8, at least the simple version of BIP8 with `LOT=false` that we talked about, is essentially simpler than BIP9.
So yeah, you can actually maybe remove some code net, but I don't know

Aaron van Wirdum: 00:12:56

Well, that wasn't really the point I was getting at.
I was just, in general, not having to check for the activation signals for this specific software.

## Scaffold

Sjors Provoost: 00:13:05

Yeah, it saves, again, a little bit of code.

Aaron van Wirdum: 00:13:08

So that makes a lot of sense to me.
I can barely think of any downsides to that, and that is sort of what you were getting at earlier, where you mentioned scaffolds, right?
I think that was in this recording, not in the one we erased.

Sjors Provoost: 00:13:24

Yeah, we brought it up in this recording.

Aaron van Wirdum: 00:13:26

Or maybe in both.
Anyway, so for the second benefit, you're basically removing the scaffolds.
It activated, everyone agreed that it activated on this specific block.

Sjors Provoost: 00:13:36

Yeah, arguably both are scaffolds because the idea that you're going to start applying rules from a certain block is also a scaffold compared to just applying the rules all the time.

Aaron van Wirdum: 00:13:49

I think that's where the discussion comes in.
So I think we're ready to point out where some of the disagreement stems from, right?

Sjors Provoost: 00:13:58

We're ready.

Aaron van Wirdum: 00:13:59

Right.
So we've just mentioned that the main benefits are all kind of code cleanup related.
They benefit, you could argue they benefit developers, indirectly anything that benefits developers benefits users because developers work for users, but they are things that benefit developers and they shouldn't affect users.
And they arguably don't affect users.

## Softfork


But there are some edge cases where it could actually affect users.
So when we were discussing at the beginning of the episode, I think that was this one and not the one we erased.
I hope we mentioned anyways that a soft fork can in fact split the blockchain or even a hard fork.

Sjors Provoost: 00:14:49

No, I don't think we've said that in this recording yet.

Aaron van Wirdum: 00:14:51

So, yeah.
Maybe, do you want to point it out?
Well, I'll just point it out.
So basically, either a soft fork or a hard fork can split the blockchain between users that are using the old rules and users that are using new rules.
Now the great benefit of soft fork is that if a majority of hash power is enforcing the soft fork rules then the chain should not split and the upgrade should be backwards compatible as they call it.

Sjors Provoost: 00:15:20

Yeah.

Aaron van Wirdum: 00:15:22
Alright now...

Sjors Provoost: 00:15:23

Which means that people do not have to upgrade their nodes immediately when there's a soft fork, and that's kind of nice, because you don't want to force people to upgrade.

Aaron van Wirdum: 00:15:30

Yeah, they can upgrade a bit later if they want or potentially even never.

## Edge Case


Okay.
In this case, a new Bitcoin Core node would assume that the taproot rules have always applied.
Now, what this means is that, and this is the edge case, if there is a very big reorg, so someone starts mining on top of a block from a year ago or whatever it is, and that someone, aliens have come to earth, I think is the analogy.

Sjors Provoost: 00:16:07

Yeah, it's either the aliens or some secret government agency.

Aaron van Wirdum: 00:16:13

Yeah, someone has a lot of hash power for whatever reason.
They start mining on a block from a year ago, and they actually claim the longest chain.

## Taproot Rules


Now in that chain, they make a transaction.
And they do this before the original taproot activation block.
They make a transaction that breaks the taproot rules.

Sjors Provoost: 00:16:37

That's right.

Aaron van Wirdum: 00:16:37

All Bitcoin Core nodes, for example, will accept this chain because it's the longest valid chain.
While new Bitcoin Core nodes who are enforcing all their taproot rules, no sorry, who are enforcing taproot rules from the beginning, they will reject this chain because it's an invalid chain.

Sjors Provoost: 00:16:58

Yeah, so basically when a new chain appears, what the node will do is it will just roll back its blockchain.
It will just like basically do everything in reverse and when all the coins that are spent are recreated until it gets to the forking point and then follows the longest chain all the way up checking the rules for that new longest chain.
And so if it goes indeed, if it goes before taproot activation, then yeah, taproot rules didn't apply.
If you're an old node, you would say, okay, taproot is no longer active because you've gone back in time.
And those blocks can just do whatever they want.
But if you're a new node under this this little cleanup you're going to say no no taproot rules are always active so if if anything violates taproot rules I'm going to complain.
So that means if if the new blocks are written at the low enough, then yeah, it's going to be a problem.
And it could even be worse.
Like Taproot could never activate at all, according to the old nodes.
Because if you go back before the speedy trial, if the aliens basically re-org back to 2020 and then replay again, they might just decide to not signal for taproot and say taproot never happened.
Now the reason we don't care about that this much is that this scenario is really, really, really bad.
So the analogy might be to say, well, if all of the Netherlands is flooded, are we really going to argue about this street name in Rotterdam that we have issues about?

Aaron van Wirdum: 00:18:25

You explained it clearly, I think, but still to reiterate, the argument is that if a reorg happens that is this bad, then Bitcoin is screwed either way and it's not worth considering even essentially, right?

Sjors Provoost: 00:18:45

Or maybe at least you probably have to do some human intervention to decide what on earth you're going to do about this situation because it means that probably lots of people's coins won't exist anymore.
All the transactions may or may not be replayed again.
So unless you bought Bitcoin in 2011 and you just huddled and never moved them, you're gonna be impacted by this event.
And the whole point of a money system, kind of goes away if that much changes.
It's Very similar to a fiat system, if suddenly your bank account is zero or a million, depending on some random historical glitch, are you really going to just keep on going with the bank balance or are you going to do something else?
It's a big disaster if this happens.

Aaron van Wirdum: 00:19:28

Yeah.
Well, so on the other side of the debate is, for example, Eric Voskuil, who's the lead developer of Libitcoin.

## Eric Voskuil

And he argues, or at least one of his arguments is that this threshold that you just...
Like at what point is this the case?
At what point doesn't it matter anymore that there's a big reorg?
Is it after a day?
Is it after two days?
Is it after a week, two weeks?
Where is this threshold?
And I guess he values consistency a lot when it comes to these kinds of things.
And his argument would be, or is, I think, well, I need to be careful to represent his arguments because he might disagree with my explanation of it.

Sjors Provoost: 00:20:16

We could say a hypothetical argument could be whether or not somebody makes the argument.

Aaron van Wirdum: 00:20:19

Maybe that's better.
Yeah.
The only consistent arguments there is that there is no threshold.
It's just for each block, you need to assign a probability that it's going to make reorgs harder.
So the more confirmations you have, it will just make a reorg harder and harder and harder.
And it's kind of how we apply it already.
Like, one confirmation is not as secure as two confirmation is not as secure as three.
And this change would imply that there's some hard cutoff to that logic, rather than it's just always going to be incrementally safer to wait longer.

Sjors Provoost: 00:21:01

Now there is actually a real cutoff because very old versions of Bitcoin Core use checkpoints, but that hasn't been done for many, many years.
But a checkpoint basically meant that that specific block had to exist.
So there are a couple of blocks in the source code that say this block must exist, otherwise the chain is not valid.

Aaron van Wirdum: 00:21:18

Yes, but that's not, you know, that is itself also controversial.

Sjors Provoost: 00:21:22

Yeah, I think it's good that those don't exist anymore.

Aaron van Wirdum: 00:21:25

Right, exactly.

Sjors Provoost: 00:21:25

But this is not as strong as a checkpoint.
The only thing you could argue, and I think maybe that's what Voskuil was arguing, is that the fact that you're now retroactively, in a certain sense, activating taproot is in a way a hard fork.

Aaron van Wirdum: 00:21:41

No it is in a way a checkpoint.

Sjors Provoost: 00:21:45

A checkpoint says this specific block has to exist.

Aaron van Wirdum: 00:21:48

Yes.

Sjors Provoost: 00:21:49 

This just says these rules have to apply, regardless of what the blocks are.

Aaron van Wirdum: 00:21:53

No, sure.
But it does have sort of the similar implications for it, because you're assuming that before that block, no split could have possibly happened.
Otherwise, you would have to check, right?
Am I saying that right?
I think so.

Sjors Provoost: 00:22:06

Well, I mean, the problem with checkpoints is you could have almost completely arbitrary rules, right?
It gives too much power to the people who decide what is a checkpoint.
But I think in the case of Taproot, you don't have that discussion because it's not that by having this rule or by not having this rule, that Taproot is always active.
It doesn't really matter that much.
It's like there's not a specific person who stands to benefit from whether or not that rule happens.
We can't predict what the disaster is going to look like.
So that's why I think it's not as bad as a checkpoint.

Aaron van Wirdum: 00:22:37

So yeah, whether or not it's a checkpoint or some kind of checkpoint or some kind of subcategory of a checkpoint is maybe not the important part.
The important part here is that one group of developers, I guess mostly in Bitcoin Core, figure that if there's a reorg this big, then Bitcoin is screwed anyways.
While someone like Voskuil will argue, you know, there's no single point where you can make that argument.
There's no point where Bitcoin will be that if the reorg is that bad.
It just, gets incrementally worse for, every extra block that's being reorg.
But there's no objective point you can point to and therefore the only sort of logic that you can apply is simply longest [inaudible] chain, that's what will you accept to be Bitcoin.

## What is signaling

Sjors Provoost: 00:23:27

So this reminded me of the other argument that you can have here, which is, do we look at only the blockchain?
Like should nodes only look at the blockchain or should nodes keep into account sort of the social consensus?
And that gets back to what signaling means.
Is signaling something that must occur on the blockchain and then a soft fork is active?
Or is it a way to coordinate the activation of a new set of rules in a point in?
And so in essence, does a soft fork activate on a chain or does it activate in a chronological point in the space-time continuum?
So can we say as of November 21 or whatever date it was, 2021, Taproot is active.
If you produce blocks in the future, even no matter what the height of those new blocks is, it's still after November 21, 2022, and therefore you should know that Taproot is active and you should just enforce it.
That is, of course, also a philosophical question you can have.
And If you agree with the latter, if you say Taproot should be considered active after a chronological point in time, well then this deep reorg is not a problem because you'll enforce Taproot.

## Two visions

Aaron van Wirdum: 00:26:28

Well, I think there's two issues here.
Or at least there's one thing to point out, and I think that's what you're getting at.
So there are sort of two visions on what the activation logic is in the first place.
So everyone agrees basically what a soft fork is, and that's, you've explained it a couple minutes ago, and I think everyone will agree on that.
But then there's the activation of the soft fork, sort of the activation logic, like you must signal or the signaling logic itself, which is something some developers will itself consider a soft fork, while other developers will argue that's the word you used before, that's scaffolding. That shouldn't be considered a consensus change.
So I think that the arguments, at least if you hold the second opinion, of removing the signaling logic from the code, that's a much easier argument to make, which I also mentioned before, I think.

Sjors Provoost: 00:27:30

Yeah, I mean, we presented these two parts of the burying, right?
So the first part is we're going to apply the rules from Genesis, and the second part is we don't check the rules.
And in that order, that's one way to look at it in that order, but you can look at it in the other order.
I guess that's what you're saying now, if you just drop the signaling requirement.

Aaron van Wirdum: 00:27:48

Yeah, but you were making a point about social consensus applying to time.
But you can still apply social consensus to the blockchain itself.
So you can still argue that there's no reason for the signaling other than informing people that a soft fork is happening while still applying it to the actual blockchain and therefore accepting that a soft fork didn't happen if there's a big reorg even though we're past a certain date.

## Signaling history

Sjors Provoost: 00:28:15

You could, but if you go back to the history of soft forks, you know, we did that in another episode, but basically the reason miners started signaling, that wasn't the case.
The earlier soft forks and Satoshi's code were just activating at a certain height.
That was a problem.
So the idea was to have miners signal for it and there were various ways to do that signaling and eventually we ended up with BIP 9.
But the reason for the signaling is to make sure that miners actually upgrade and are actually ready.
And there's no reason to assume that with a big reorg they're suddenly unready.
They would have to downgrade their software, basically.

Aaron van Wirdum: 00:28:50

That's not something everyone agrees on, Sjors.

Sjors Provoost: 00:28:53

That's fine.
That's sort of the point I'm trying to make.
If that is your interpretation, if the interpretation is we use the signaling in the actual history of Earth, just to say, okay, now all the miners are ready, they have the latest software, they can enforce Taproot, then there's no reason to assume that when there's a deep reorg, they're certainly unready.
But you can also have the blockchain-centric perspective where you say, no, there is no reality outside the blockchain and outside this code.
In that case, you might say, no, if time is undone, it's like real time travel.
We've really changed history and taproot never happened or did or some other time.
That's a potential discussion you can have.

Aaron van Wirdum: 00:29:36

Yeah, well that's interesting you bring that up.
I think that's right.
So these are sort of two ways of looking at signaling, whether it's informing miners or whether it really means readiness signaling, which is definitely a term that has been used, but recently during the Taproot debates, there was also sort of this idea that signaling is really for users.

## Weeds

So users know that a certain change will activate, which also allows them to fork off if they disagree with the change, for example.
And that's really the reason for signaling.
So, I think we're getting really into the weeds at this point.
I think it's interesting, but We might be losing some listeners by now.

Sjors Provoost: 00:30:17

That's fine.
We've shown the listeners where the weed is.

Aaron van Wirdum: 00:30:27

Right.
Where the weed is?

Sjors Provoost: 00:30:28

Yeah, maybe not the best analogy.
We've shown them very deep into the rabbit hole.
They can explore more for themselves by just reading these mailing list threads.
We'll probably put them in the show notes.

Aaron van Wirdum: 00:30:38

Yeah, no, there's one other thing we do need to bring up.
Okay, we're jumping around now, so the episode's getting confusing.
Sorry, people.
But there is this other...
Sort of what it ultimately comes down to this discussion, I think, is whether burying a soft fork, as we've explained throughout this episode, whether that should be considered a consensus change or not, and by extension, whether it should be a BIP - Bitcoin Improvement Proposal.

## BIPS

Sjors Provoost: 00:31:16

A consensus BIP, because you can have an informational BIP that's not a consensus BIP.

Aaron van Wirdum: 00:31:20

Yeah, can you though?

Sjors Provoost: 00:31:21

You can basically write a BIP that says, hey, if you're running a full node, you could consider burying the soft fork because it will make your life easier.
But keep in mind that if this time travel thing happens, you have a problem.

Aaron van Wirdum: 00:31:36

It's not really the point of BIPs though, Sjors, is it?

Sjors Provoost: 00:31:39

Well, we've done an episode about BIPs. There are informational BIPs and there are consensus BIPs.

Aaron van Wirdum: 00:31:43

Well, yeah, but they need to be relevant for other nodes.

Sjors Provoost: 00:31:48

Well, they are.
It's good to explain to other nodes what you've done in your implementation that, under extreme circumstances can make a difference.

Aaron van Wirdum: 00:31:55

Well, you can make a very general informational BIP of this is a thing you can do, but then that BIP doesn't need to include a specific block height, right?
Well, that's the debate then.
Is this a consensus change?
In other words, if there would be this big of a reorg, should we expect all nodes to accept this reorg or reject it?
Like should they do the same thing?

Sjors Provoost: 00:32:23

Yeah, so this comes down to the little street in Rotterdam situation that I was talking about.

Aaron van Wirdum: 00:32:27

Hang on, let me finish this sentence.
Or is this just a thing that developers can do as a shortcut in their own code.
And then, essentially, if it does go wrong, that's the wrong problem.
That's a problem of that specific implementation.
That would essentially mean that that specific implementation has forked itself of the network.
I think if you really go into this debate, that's sort of ultimately what it's about.
And that's why I mentioned at the beginning of this episode that consensus changes are kind of interesting because it sort of says something about how do you define Bitcoin, what is Bitcoin.
And this is an example where that actually applies.

## What is Bitcoin


Like if in this unlikely scenario would happen, then would the buried version be the real Bitcoin?
That the nodes that have the buried soft fork, would that be the real Bitcoin?
Or would they fork themselves off of the real Bitcoin network?

Sjors Provoost: 00:33:18

Yeah, so we're talking about a specific deep re-org that actually violates the taproot rule, right?
Because there is a good chance that they don't violate taproot in the deep re-org.
So, I think in general, it's a good idea to think about an extreme scenario like this.
But I think if you do that, you'll end up seeing this is a really big problem.
There's all sorts of things we need to solve in such an event.
And this little thing about buried consensus rules is somewhere on the to-do list of that giant project of okay what are we going to do?
Like is there some threshold that we say if this alien shows up?
I guess in general we need a scenario what to do with the aliens.
The aliens might have extreme hash power. They might be able to just completely double spend everyone on the planet because they have some alien ASIC that can double spend any block at any depth and they can create re-orgs out of spite.
Or the secret government agency basically.
It might be useful to have a plan for that.
I just think that this won't be the most interesting part of the plan because it's a really bad situation.
And it probably means Bitcoin would be completely broken in that case.
But maybe not.
Maybe there is a rational way to deal with it.

Aaron van Wirdum: 00:34:30

That's the difference of opinion, right?
Some people like Eric Voskuil will say Bitcoin isn't broken, Bitcoin is working as intended, long as valid chain still applies.
There was a long re-org that's part of the Bitcoin consensus system.

## Conclusion

Sjors Provoost: 00:34:46

Yeah, but the question is, can you use it for practical transactions if that can happen again and again and again and again?
I would probably say no.
It's just the same reason with lots of altcoins that try to use SHA-256 and technically they're still valid chains.
It's just that nobody uses them anymore.
So I think it's good to have some sort of thought about what to do with the alien invasion.

Aaron van Wirdum: 00:35:13

So I want to close off this episode, but I want to ask you then, personally, should this be considered a consensus change?

Sjors Provoost: 00:35:23

No, I think this is sort of...

Aaron van Wirdum: 00:35:24

Or is this a developer shortcut at their own risk?

Sjors Provoost: 00:35:29

Yeah, I think it's a developer shortcut, but the idea of a one-year re-org is undefined behavior, I think.
So I think there is no consensus rule for a one-year re-org.
That's my opinion.
It's a disaster that's not been worked out.
There's just no contingency plan.
It's like saying what do we do if the 55 nukes go off over Amsterdam?
You know, what's the can you still go into a hospital without a mask?
I don't know.
It's undefined. But maybe it should be defined.

Aaron van Wirdum: 00:35:59
I guess I disagree with you.
I think it's defined as long as it's a valid chain.
That's it.

Sjors Provoost: 00:36:09

That's fine.

Aaron van Wirdum: 00:36:09

Well, then I guess that's the episode, Sjors.
We've reached the point, we've kept pulling the threads to the point where sort of the disagreement emerges, I think, of the broader discussion.
I hope our listeners could follow.
I think it was maybe a bit messy because it's a complicated topic, but I thought it was kind of interesting.

Sjors Provoost: 00:36:29

Yeah, I think so too.
Yeah, especially the fact that we're talking about hypothetical time machines in a situation where we lost one recording.
In other words, we also have this hypothetical time machine.
Did we say this before?
Was it really set?
Because we said it without recording it.

Aaron van Wirdum: 00:36:43

I'm sure that didn't help.
Yeah.

Sjors Provoost: 00:36:45

So anyway, thank all for listening to the Bitcoin Explained.
