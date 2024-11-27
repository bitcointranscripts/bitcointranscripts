---
title: "The Great Consensus Cleanup Revival (And an Update on the Tornado Cash and Samourai Wallet Arrests)"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://bitcoinexplainedpodcast.com/@nado/episodes/episode-93-the-great-consensus-cleanup-revival-and-an-update-on-the-tornado-cash-and-samourai-wallet-arrests-5bbxi
tags: ['wallet', 'consensus-cleanup']
speakers: ["Sjors Provoost", "Aaron van Wirdum"]
summary: "In this episode of Bitcoin, Explained, Aaron and Sjors discuss the Great Consensus Cleanup Revival soft fork(s). This proposal would fix some known bugs in the Bitcoin protocol, specifically the timewarp vulnerability, large block validation times, 64 byte transactions and BIP 30 verification."
episode: 93
date: 2024-05-29
additional_resources:
  - title: CoinKite
    url: https://store.coinkite.com/promo/BITCOINEXPLAINED
  - title: https://bitcoinexplainedpodcast.com/
    url: https://bitcoinexplainedpodcast.com/
---
Speaker 0: 00:00:19

Life from Utrecht, this is Bitcoin Explained.
Sjoerds, it's been a month.
That means you had a whole month to think about this pun that you told me you're going to tell our dear listeners for this episode.
Let's hear it.
Let's hear it.

Speaker 1: 00:00:35

That's right.
So it's cold outside.
The government is cold.

Speaker 0: 00:00:39

You know what else is cold?
Sure.
Our sponsor.
That's right.
The cold cart.
The cold cart.
If you have coins, you want to store them.
Cold car is the place for that It's the audio.
Okay, are we too loud?
It's too much echo too much echo Okay, cold card cold card cold card cold card cold card cold card.
I think that was like our 20 seconds that we're obligated to talk about the coldcard.
What do you think?

Speaker 1: 00:01:09

I think it's great, but it's a hardware wallet for people who don't know.

Speaker 0: 00:01:12

Yes, why did you say the government is cold?

Speaker 1: 00:01:15

Well, that's a segue to our next section.

Speaker 0: 00:01:19

So this episode we're going to talk about the Great Consensus Cleanup Revival, which is a proposed soft fork, which sort of includes several soft forks into one, you could kind of argue, right?
Basically, that's what it comes down to.
But before that, a lot has happened in the Bitcoin and Ethereum space in a way that's relevant to Bitcoin as well.
So you want to touch on that a little bit.
First, you've been following it pretty closely.
Let's start with...
Where do we start?

Speaker 1: 00:01:52

Let's start with what happened with tornado cash in the netherlands yeah in case anybody was living under a rock the tornado cash we talked about that in episode 69 but he got convicted.
So that's bad.

Speaker 0: 00:02:08

Yeah, Alexey Pertsev, one of the Tornado Cash developers got convicted for 64 months in prison.
Yep.
Which does seem to have a lot of relevance for Bitcoin because really he was just writing codes.
You know, he was writing privacy code, but he was never, maybe you should give the context.
Why do you think it's relevant for Bitcoin?

Speaker 1: 00:02:30

Well, the main point of relevance for us, I think, is the fact that he was building a non-custodial system.
So a system that does not hold the coins yourself.
I mean, there is a website and those kind of tools.
So That's a very dangerous precedent, I think, because it's not very clear where that line is.

Speaker 0: 00:02:49

Yeah, we already knew that running a custodial mixer, which a lot of other mixers were, where you just send coins to someone and that someone sends different coins back, that was always illegal.
And everyone knew that was illegal.
If you're doing that, that's basically money laundering and that is illegal.

Speaker 1: 00:03:05

Well I think you can narrow it down slightly it's not illegal to mix the coins but it is when you don't do KYC I guess that's maybe a different interpretation.
Right.
But for the you know if for all practical purposes you can't build a mixer with KYC in an ethical way anyway.
So effectively, mixes are illegal, but technically, I think the non-KYC part of the mixer is what makes it illegal.

Speaker 0: 00:03:30

Fair enough.
In either case, so far it was generally assumed that yeah, if you're taking coins and they're sending other coins, then you're at risk.
But if you're just developing software, which allows other people to send their coins to other people, then you're not the one money laundering.
However, the Dutch court just struck that down, and now it looks like, nope, just developing code can make you responsible for how other people use that code, right?

Speaker 1: 00:03:58

Well, probably, but We don't really know because this verdict was extremely unclear about that.
So we don't know if it's simply the act of writing code or it is the, you know, making that code available on your own website or, you know, making that code available on some automatic website-like system or whether it's about maintaining this code after you've written it once, or if it's about promoting the code or making money from the code, it's very unclear.
And in fact, the prosecutor seemed to emphasize making money from the code, but the judge much less so.

Speaker 0: 00:04:34

Yeah, the prosecutor really hones down on it essentially being a business.
And that's why you say the making money part was important, but the judge didn't even really seem to focus on that.
The judge just said, look, if you write this code, knowing that it can be used for this purpose and you don't do anything to stop that then you're responsible if it's really used for that purpose right yeah pretty much and what was the purpose especially of course being money laundering yeah what was especially interesting though not clear entirely how that's going to apply to Bitcoin, was the argument that he made the whole thing unstoppable.

Speaker 1: 00:05:10

So in Ethereum, part of the system at least is unstoppable.
It's a smart contract, unless you stop Ethereum itself, of course.
And the fact that he did that where the prosecutor just tried to argue well it's not all decentralized some of it is is fake decentralization others is real the judge completely ignored that and basically said well the fact that you even tried to make it decentralized that is actually making it worse so that that argument of course can apply extremely broadly because you could say well if you just publish source and you know that other people are using that source and you just keep updating that source code, well, that's also kind of unstoppable in a way.
So that might also be a problem.
And of course, we all know somebody, or we don't know them, somebody who created an unstoppable system a long time ago and kept working on it.

Speaker 0: 00:05:59

You're referring to Satoshi Nakamoto.

Speaker 1: 00:06:01

Exactly.
So we're waiting for his arrest warrant, I guess.

Speaker 0: 00:06:04

Yeah, well, the short way of looking at it, I would say is we all thought so far that there was a fairly clear line of what would make you responsible, which is custody in a way.
And now it's kind of a all bets are off type of situation.

Speaker 1: 00:06:24

Yeah, and this creates a bit of a problem because we assumed that this line existed, we did not do much to defend people who built custodial mixtures.
And in retrospect, that was probably a mistake, because as soon as you lose that line of defense, now, you know, I guess the only way to win now is to go all the way back and say, no, all mixtures should be legal, including custodial ones.
But now you have all this precedent that wasn't stopped.
So that's a problem.

Speaker 0: 00:06:51

Right.
OK, let's move on to the actual Bitcoin case, which is the Samurai devs.

Speaker 1: 00:07:00

Just to add one little detail, as far as I know he is going to Appeal, so we'll see what happens.
And Appeals can quite dramatically change things.

Speaker 0: 00:07:09

Yeah, is there any timeline for that?
I don't know.
No. Okay, so let's move to the more Bitcoin relevant case or I mean...
The more direct Bitcoin case.
Yeah, exactly.
So the Samurai wallet developers Keone Rodriguez and Bill Hill William Hill both of them you know right yep yeah I used to work with them when I was at blockchain.com, so back in time, blockchain.info.
Right, so they were arrested as well, one of them in Portugal, one of them in the United States, but both on behalf of the Department of Justice, DOJ.
So what do you want to say about that, if anything?

Speaker 1: 00:07:53

Well, I'm not surprised that this happened, because the fact that they were going after Tornado Cash made it clear that they would go after non-custodial systems, after non-custodial mixes.
So it seemed like a matter of time before they would go after it and then obviously they always go after the biggest or at least a big one.
So the only question was, were they going to go after Wasabi or were they going to go after Samurai?
Samurai has some interesting marketing that maybe made them more interesting to prosecute, but I don't know if the difference, you know, and of course we know that Wasabi was doing some proactive compliance-ish things, But I don't know why they picked one and the other.
Ultimately, we'll find out.
What else was I going to say about it?

Speaker 0: 00:08:40

Well, it was my suggestion to just sort of explain how the Samurai Mixing actually works.
But at this point, should we just move on to the main topic of the episode?

Speaker 1: 00:08:52

No, I think it may make sense to briefly explain a little bit.
So there's three aspects to Samurai Wallet, I think, that are relevant.
One is It's not just a mixer, definitely not.
It's a wallet, right?
It's a non-custodial wallet.
And so far it seems that that wallet was taken down mostly as a side effect of taking the mixer down, not as a direct target.
But it is down.
But fortunately it was a non-custodial wallet and people wrote down their 12 words, hopefully.
And so they should be fine because they can just import it into another wallet.
But there was also a mixer component.
And I think the two most important parts of that are something called the Whirlpool, which is a 5 input, 5 output mixer that you can use multiple times.

Speaker 0: 00:09:37

Yeah it's just a coin join which uses equal amounts.

Speaker 1: 00:09:41

Yeah and then there is something called Ricochet which basically just as far as I understand it just forwards your coins a couple of times.
So you're making a couple of unnecessary transactions and then you send the email that you want to send and that might help when you're dealing with an exchange that only looks at say five hops ago or two hops ago and then maybe you can get around that.
I don't know how effective any of these things are.

Speaker 0: 00:10:06

Yeah, you're basically making transactions to yourself a couple times.

Speaker 1: 00:10:09

Yeah, now it should be noted that from my reading of the indictment, they don't even talk about whether or not these tools, these mixing tools were effective or not.
The fact that it's doing any mixing, that is the problem.
So that's something to keep in mind.

Speaker 0: 00:10:27

Yeah, I would say the Ricochet one, The fact that that one is even mentioned is blatantly absurd.
Like every wallet, with every wallet you can send coins to yourself.
There's just a button that just sort of automates that you do that a couple of times.

Speaker 1: 00:10:42

Exactly.

Speaker 0: 00:10:43

That this is even, Like the other, the Whirlpool, I can sort of at least understand why it's seen as some, I mean, I don't agree with the rest of the course.

Speaker 1: 00:10:52

Well, the Whirlpool requires coordinating with other users, right?
Whereas the Ricochet thing does not.
It's just your wallet sending a transaction to itself, essentially five times in a row.

Speaker 0: 00:11:01

Yeah, which again literally every wallet can do.

Speaker 1: 00:11:05

But I would be very surprised if in the court case they're going to debate the specific details of what is and what is not mixing.
My guess is they just go with the marketing.
They say, well, you guys called it a mixer and that's all we care about.

Speaker 0: 00:11:23

Right.
Anyways, yeah, seems like a new era in Bitcoin and Bitcoin development to me.

Speaker 1: 00:11:32

Yeah, and I think we could briefly do a recap of the differences, how these cases relate to each other.
So we brought up most of the things.
So the interesting thing about Samurai is that it's only happening in the US, whereas The Tornado Cash trial is happening in the US and the Netherlands in parallel, which is interesting.

Speaker 0: 00:11:50

Yeah, you didn't mention that yet, but yeah, one of the other Tornado Cash co-founders was arrested in the US and will be on trial there.

Speaker 1: 00:11:59

Yeah, and this is interesting because the Dutch court system is not very transparent.
You can go to the court hearings but you don't get to see any of the dossier.
Whereas in the US it's much more transparent so we'll probably learn much more about the Dutch case through the US case.
Both of them are non-custodial.
Both of them use a, well no, so the samurai uses a central coordinator, so that might be a service, whereas in Tornado Cash it's a smart contract, so that's not really a service, although the prosecutor argued that it's a service anyway.

Speaker 0: 00:12:36

You mean the main smart contract?

Speaker 1: 00:12:39

Yeah, the main smart contract and everything around it.
You could argue like it's an autonomous system, so it's not really a service, but that's what they're arguing, I think, in both the Netherlands and the US, against or for, depending on which side you're at.
I'd say Samurai used fees, fairly pretty direct fee system, whereas The Tornado Cash system did not charge fees directly, at least the fees don't go directly to the developers or operators.
They have a more convoluted tokenomics system where at least the prosecutor argued that these tokenomics are, you know, how it is, how the business works.

Speaker 0: 00:13:21

I think the short summary I would give is if the Tornado Cash developer is guilty in the Netherlands, which he is, then the Samurai developers have to be as well.
So it's sort of even more straightforward.

Speaker 1: 00:13:34

Exactly.
It's a simpler case.

Speaker 0: 00:13:37

Right.
So, yeah, bad news.
Let's move on to our actual topic for the podcast.
What do you think?

Speaker 1: 00:13:45

Yeah, also some bad news in a way.

Speaker 0: 00:13:48

Yeah, but bad news that we're going to fix, right Sjoerd?

Speaker 1: 00:13:50

Yeah, exactly.
That we hopefully fix in time.

Speaker 0: 00:13:54

So we're going to talk main topic of the podcast.
Finally, we're here.
We're here, ladies and gentlemen.
We're going to talk about the Great Consensus Cleanup, or maybe more specifically the Great Consensus Cleanup Revival.
That's right.
Because the Great Consensus Cleanup was proposed by Matt Corello a couple of years ago, and it was recently revived by Antoine Ponssois.
Am I saying that right?
Probably.
It was him, right?
I got the person right at least.
Whether I got the name pronunciation right or not sure about that one.
And The Great Consensus Cleanup revival, maybe what's the difference between the original and the revival?
Is there a difference?

Speaker 1: 00:14:39

Yeah, there is.
So the revival adds something and I guess I'll let you know when we get to that due bit.

Speaker 0: 00:14:46

Okay, And as far as I understand, the great consensus cleanup would be, well, it would basically be one soft fork that bundles several soft forks and these soft forks sort of fix existing bugs in the protocol.

Speaker 1: 00:15:01

Yeah, that could be individual softworks and you know in the worst case maybe out of the four components people really like three of them and are kind of arguing about the fourth one then you can simply do three and not do the other one.

Speaker 0: 00:15:14

Okay and if I understand correctly basically everyone and when I say everyone I mean everyone that's you know has enough expertise to have an opinion in the first place, agrees that at least the bugs are problems.
There's maybe at most like some conversation about the best way to solve these problems, whether these are the best ways.
But the problems are real.
There's no one that says, no, these are actually futures, right?
These are just real problems, bugs that exist in the Bitcoin protocol.

Speaker 1: 00:15:45

I think when it comes to the Time Warp attack, there might have been someone who could think of some interesting schemes that you can do using a Time Warp attack.

Speaker 0: 00:15:53

That's right.
You're thinking of Mark Friedenbach, who had some sort of proposal years ago to sort of increase the block size.
Yes.
Yeah, You're right.
But let's...

Speaker 1: 00:16:03

Every bug is a feature.

Speaker 0: 00:16:04

Yeah, let's table that for a second.
Although, I mean, it is interesting that you bring that up.
But...

Speaker 1: 00:16:09

Well, I mean, that won't work if somebody exploits the time warp maliciously before the legitimate use case happens, I think.

Speaker 0: 00:16:20

Well, is the legitimate use case still possible after this bug would be fixed?

Speaker 1: 00:16:25

Actually, I'm not sure.

Speaker 0: 00:16:27

Probably not, right?

Speaker 1: 00:16:27

We'll shelve that.
So there may be a, you know, As always, there may be some ways that you could use this to your advantage.
I think it's better to fix them.

Speaker 0: 00:16:35

Yeah, okay.
There are basically four bugs, right?
There are four bugs, there are four things that this would solve.

Speaker 1: 00:16:43

That's right, plus an open invitation to anyone who knows another bug.

Speaker 0: 00:16:48

Okay, so four.
Let's start with the first one.
So the first one, you already mentioned it, the time warp attack, the time warp problem, what do we call this?

Speaker 1: 00:16:58

Yeah, the time warp attack.

Speaker 0: 00:17:00

Yeah, and so it's about the time warp attack is possible now, and we're talking about fixing that, that it's possible.
Like that shouldn't be possible, essentially, right?

Speaker 1: 00:17:10

That's right.
And we did an earlier episode about the time warp attack.
It's episode number five.
So scroll all the way back.

Speaker 0: 00:17:17

That's a long time back.

Speaker 1: 00:17:18

Where we explain how it works, I think.
I didn't listen back to it.
But basically, I mean, the deal there is that you can mess with the timestamps in every block so miners can, you know, Bitcoin is not a clock, contrary to popular belief, but blocks do have a timestamp in it.
And this timestamp cannot...
I mean, the miner can pick this timestamp however they want, but there are a few restrictions on it based on earlier possible attacks.
One of the restrictions is that it cannot be more than two hours in the future, as determined when you receive the block.
The other rule is that every, I think it's a rolling average or the median, I should say, of the last 11 blocks has to go up by one second every block.
And so basically, you know, the block time has to go up a little bit and it can't be too far in the future.
Those are the only two restrictions, but it turns out you can still mess with the system with those two rules.

Speaker 0: 00:18:17

How so?

Speaker 1: 00:18:19

Well, you can basically fool the system...
I think we need to explain another related bug here first, which is that the difficulty adjustment, how the difficulty adjustment works.
So the goal of the system is to keep one block every 10 minutes and this is achieved by looking at the last block of the difficulty adjustment period and comparing it to the first block in that period and then dividing it by 2016.
And there are multiple problems with that, but the biggest one is that you are not comparing the first block of each period to the first block of each last period.
You're comparing the first block of a period to the last block of a period.
And that allows you to kind of mess around the edges.

Speaker 0: 00:19:09

Oh yeah, okay.
So how do you mess around the edges?

Speaker 1: 00:19:12

Well, one thing you can do here is you can increase the timestamp of...
Basically, you increase the timestamp of every block as little as possible.
So the entire two-week period will look like it's only a few minutes basically.

Speaker 0: 00:19:28

Yeah and well to be clear this would require a majority of miners to collaborate.

Speaker 1: 00:19:34

Yeah, the time warp attack is a 51% attack, basically, or requires a 51% attack.

Speaker 0: 00:19:39

So miners, a majority of miners is faking the timestamps, and all nodes on the network will accept this, because it's not breaking the rules.
The nodes are just looking is this block mined in the future and is it mined at least one second previously later than like the 11 blocks before it's offline.
Exactly.

Speaker 1: 00:19:59

So then you can mine, you can fake the timestamps to make every blocks look like it was all mined within the same minute basically yeah and then you might think it's mined within the same minute why would you want to do that well there's another part of this attack which is where you take the last block of the difficulty adjustment period and there you don't lie You just put it two hours in the future or right now, it doesn't really matter.
If you do that in just one difficulty adjustment period, it really has almost no effect, right?
Because the first block in that period had a real time because you weren't lying.
The last block in the period has a real time because you weren't lying.
You were only lying for the other blocks.
So the difficulty will just stay the same because it took you two weeks to make these blocks.
But the attack has already begun even though it doesn't have any visible effect yet.
For the next two weeks, you do the same thing.
So the first block, you set a fake time as low as possible.
So much older than the last block of the previous period.
You just keep that original clock going.

Speaker 0: 00:20:59

Right.
So now you're back in the original minute, so to say.

Speaker 1: 00:21:04

Yes, and now the last block, you're speaking the truth again, the last block of the period.
And now if the blockchain is looking at what to do with the difficulty, it's seeing the last block of the period, which is real, and it's seeing the first block of that new period, which is now four weeks ago.

Speaker 0: 00:21:23

Right.

Speaker 1: 00:21:23

Because we've only increased that timer very slowly.
Yeah.
And so that means the difficulty can be cut in half now.
Yeah.
And then you repeat this little trick.

Speaker 0: 00:21:32

Yeah, the rest of the network, all nodes are looking at these two blocks and they're thinking, wow, it took a whole month to mine 2016 blocks.
It's way too long.
We got to decrease the difficulty by half.
Exactly.
So now the difficulty is divided by half.
Even though that was not really necessary, it's just the timestamps were all being faked.

Speaker 1: 00:21:50

Exactly.
So now you can make two weeks worth of blocks in just one week.

Speaker 0: 00:21:57

Assuming that all the hash power is still the same, now you can mine two weeks of blocks in one week yep yeah and because again and then at the end of that one week you're still faking the timestamps so we're still sort of back mining in the first minute or you know yeah so at the end of that of that week which you know for the blockchain is two weeks you're like okay this was five weeks This took five weeks to produce this block, so I'm gonna decrease the difficulty even more.

Speaker 1: 00:22:23

And then, so it gets cut in half again, so now you can mine in about two and a half days, the equivalent of two weeks, and the blockchain is like, whoa, that took five weeks and two days.
I got to reduce the difficulty again.
And so the difficulty goes to one very, very quickly in a matter of about 40 days according to Antoine's calculation.

Speaker 0: 00:22:44

Right.
So yeah, miners, like you said, it's basically 51% stack where miners can drive the difficulty down to one.
And then they can mine all remaining coins that are still to be mined over the next century.

Speaker 1: 00:22:59

They mine the equivalent of until the year 2106.
We've got every last set.
We've got millions of blocks in a very short period of time.
And then they probably stop the attack, because there's no need to do it anymore.

Speaker 0: 00:23:13

Yeah.
And then on top of that, that would mess up probably a bunch of like smart contract things, time lock types of things.

Speaker 1: 00:23:23

No, well, time locks are, well, they might be affected, but because time is moving more slowly, your time locks would indeed not expire, but that's probably not a big deal.
Like during this attack, because the attack takes five weeks plus a little bit to suck all the coins out.

Speaker 0: 00:23:39

Well, it could definitely, the time locks that are locked on a certain block in the future.

Speaker 1: 00:23:43

Yeah, so if you're looking at hide locks, I guess you'd call them, hide locks are definitely affected because if you have a contract that expires in block one million, well, guess what?
That happens immediately.
But a time lock would be, kind of during the attack, it would be affected because your time lock is never happening because they keep the time behind.
But once they stop the attack, it'll be fine.
So you might be unlucky if your lightning thing is in the wrong place yeah it could be bad but the the worst aspect of this attack other than the five-week disruption is simply that they have now exhausted the full subsidy.
And so we were hoping to not have to deal with a no subsidy world only 20, 30 years from now, but we have to deal with it in, well, 40 days, worst case, if this happens.

Speaker 0: 00:24:31

If this attack is exploited, yeah.

Speaker 1: 00:24:32

And it could happen at any moment.

Speaker 0: 00:24:34

Okay, so...

Speaker 1: 00:24:35

And a majority of miners, you know, might think, well, you know, why not?
We're the majority of miners.

Speaker 0: 00:24:41

Well, I mean, one reason why not is that it would probably undermine trust in the protocol.
But let's ignore that.
Let's see if we can fix the protocol instead of relying on that kind of stress.
So what's the fix here?

Speaker 1: 00:24:52

The fix is actually fairly simple.
The ideal fix would be that we just compare every block to the same block in the last period,
but that's a hard fork.

Speaker 0: 00:25:04

Okay.

Speaker 1: 00:25:04

So instead, at least I think it's a hard fork.
So instead...

Speaker 0: 00:25:07

So by that you mean instead of comparing the first to the last block within the same period, you know, and checking if that's two weeks, you should really just check the first block to the next first block.
Yeah.
But that's not possible, right?

Speaker 1: 00:25:22

As far as I know that's a hard fork, so can't do it.

Speaker 0: 00:25:25

But also how is that even possible?
Because by then the difficulty should have already adjusted, right?
By the time the first block of the next period is marked.

Speaker 1: 00:25:34

Well obviously you'd have to change exactly how the difficulty adjustments happen but you should just do the difficulty adjustments correctly.
But the simplest solution here is that every first block, or block 0 of every period, needs to be in the present, or two hours ago, but no more than that.

Speaker 0: 00:25:52

Every what?

Speaker 1: 00:25:53

Every first block of every period, so block 0, block 216, etc., has to be in the present, the timestamp.
And it can be two hours ago for weird mining-related reasons, and it can, of course, not be more than two hours in the future.
But basically, it has to be in a four-hour window between two hours ago and two hours in the future.

Speaker 0: 00:26:14

Every first block has to be?

Speaker 1: 00:26:16

Yes.
Right.

Speaker 0: 00:26:18

Okay, yeah, that sounds like a pretty simple fix.

Speaker 1: 00:26:20

Yeah, because remember the attack involved comparing the last block to the first block, and really messing with the first block.
That's the part of the messing that you weren't messing with the last block already, But you were messing with the first block and this fix basically makes that impossible and therefore the difficulty adjustment will be correct and solved.

Speaker 0: 00:26:39

Okay, makes sense.

Speaker 1: 00:26:40

Yeah and as far as I know that's still the going, the proposed fix that hasn't changed.

Speaker 0: 00:26:47

Okay, that was a time warp attack fix, what's the next one?

Speaker 1: 00:26:52

Slow scripts.
So as you know it takes a while to validate the whole blockchain and Some blocks take a bit longer than others.
That can be because there's tons of tons of transactions in them, but there's certain, you know, at least we have a limit on the block size.
A block can be more than four megabyte.
So there's some limit to how much you can do in a block, but it turns out you can make some special transactions that are really quite slow to verify.
And that's usually a combination of lots of signature checks, because signature checks take a while, you have to do the ECDSA thing, and hashing.
So we talked about this signature checking speed problem back in episode...
Let me see...
I think episode 32 and episode 76.

Speaker 0: 00:27:44

Yeah.
Yeah, so from what I understand, the problem here essentially is like every transaction includes scripts and for many transactions that's just a straightforward, you know, check that the signature is valid type of thing.
But you can make more complex transactions that include, like you say, hashing or more signature validation.
Yeah.

Speaker 1: 00:28:08

So Stoichi, for example.

Speaker 0: 00:28:09

And if you would intentionally want to design a transaction or maybe even a block full of transactions with complicated stuff, then that could in the worst case lead to blocks that take minutes to actually validate.

Speaker 1: 00:28:25

Yeah, and so, you know, people have been, Antoine, I believe, has been doing some math on seeing what is the absolute worst you can do?
And he came up with something that took more than one hour to validate on a Raspberry Pi 4.

Speaker 0: 00:28:37

Right.

Speaker 1: 00:28:38

And that's not good.
Now you could say, well, it sucks to have a Raspberry, but it'd be nice if it didn't.

Speaker 0: 00:28:45

And even on a fast laptop, it took several minutes.

Speaker 1: 00:28:49

Yeah, and several minutes would be bad, right?
So if you are a miner and you receive that block that takes you several minutes to validate, well, now your competitor can do all sorts of shenanigans because you're kind of stuck validating.

Speaker 0: 00:29:02

Yeah, or not shenanigans, just get a head start on finding a nice block, for example.

Speaker 1: 00:29:08

Right, that's one shenanigan, but I think there might be other things you can do.

Speaker 0: 00:29:12

Yeah, it would be a disruptive thing for the network if blocks take minutes or even longer than that to validate.
Yeah,

Speaker 1: 00:29:17

And so the question is, how do we prevent those blocks from being created?
Now, for now,

Speaker 0: 00:29:24

Just to give a comparison, how long does it take to validate average block right now?

Speaker 1: 00:29:31

I think on a good laptop a fraction of a second.

Speaker 0: 00:29:33

Yeah and on like a Raspberry Pi?
Probably one second.
Yeah okay just to sort of paint the context there.
Okay so the solution?

Speaker 1: 00:29:45

Well the solution is in the original proposal by Bluemat, there was a solution which was just changing a few rules.
I think now there's discussion about a slightly different solution.
So that's actually still ongoing research, what is the actual best solution.
But the gist of it is that there are certain extra rules in SegWit and in Taproot that make the script safer.
This was why the block size could be increased with SegWit because any of these extra SegWit transactions would not be as expensive and as slow.
These worst case couldn't happen.
But it looks like some of these rules should also be applied to legacy scripts, to legacy transactions.
And then the problem is you can't just apply all of SegWit's rules to legacy transactions, so you have to be very careful which ones you'd want to apply.
Main problem there is, you know, somebody might have a transaction that they put in a cold wallet and or like offline wallet, right?
So we don't see it on the blockchain and now they want to broadcast it, but we changed the rules and now they can't spend it anymore.
Now the changes that people have in mind would only impact the most bizarre, unrealistic transactions that you can possibly imagine, but still that could still be controversial.
So the key is to find the absolute minimum extra rules that you need in order to fix the problem and no more.
Because the simplest solution would just be to say, hey, you know what, you can only make TAPO transactions.
That would fix the problem, but it would make a lot of people very angry.

Speaker 0: 00:31:20

Yeah, I thought the idea was also to only apply these new rules from a certain block height.
So if you already had your coins in some...

Speaker 1: 00:31:32

So those are other things you could do to restrict the possible damage that a rule could do.
But the trade-off there is complexity.
So a rule that says only do this after this block, or only when the coins you're spending is from this block.
That's extra complexity that you'd prefer not to have.
Plus, you know, if the attack, this is one of the problems, once you publish the exact fix somebody might come up with what it is fixing and then do the attack before the soft fork is activated.
That's probably inevitable anyway, just like the time warp attack, everybody knows what to do there.
Yeah.
So there's that.

Speaker 0: 00:32:13

Yeah.
Well, you really want to avoid that people lose their coins, right?
That's kind of a non-negotiable, I would say.

Speaker 1: 00:32:17

Yeah, so realistically, even the original proposal by Bluemet, I think it was changed a bit by him because there were several things that he wanted to change for this problem.
And I think they ended up dropping one of these things.
So hopefully there's a way to make sure that you can like there's nothing gets unspendable.
It might just take more fees for example.

Speaker 0: 00:32:42

Right.
Okay So that was slow scripts.
Are we done with slow scripts?

Speaker 1: 00:32:49

Yep, we are.

Speaker 0: 00:32:50

All right, and the next point is about banning 64 byte transactions.
Is that right?

Speaker 1: 00:32:55

Yes, 64 bytes, bad.
Why?
Well, We mentioned this a few times in other episodes, I don't think we've done an actual episode about it, but in our episode 81 we talked about a change to Bitcoin Core 25 that makes transactions that are 65 bytes or greater, I think they make them illegal again or something weird about that.
I forgot what exactly we discussed.
The point is 64 byte transactions are bad and the reason they're bad is because they look the same as 232 byte transactions next to each other in the block.
Because of the way the Merkle trees are made.

Speaker 0: 00:33:36

Sorry, we have to take a step back here, Sjoerd.
What does it mean?
Why is there such a thing as a 64 byte transaction and also such a thing as a 32 byte transaction?
Why aren't all transactions the same number of bytes?

Speaker 1: 00:33:49

Because the size of a transaction depends on the number of inputs, the number of outputs, what kind of script you have in those inputs and outputs and whether it has a witness or not.

Speaker 0: 00:33:57

Okay and then 64 but a 32 transaction would also look like two 16 byte transactions, right?

Speaker 1: 00:34:09

Yeah, but I don't think you can make a 16 byte transaction because simply it wouldn't fit.

Speaker 0: 00:34:15

Okay, and a 128 byte transaction would look like 4, 32 bytes.
Why is 64 singled out is my question.

Speaker 1: 00:34:23

Okay, so the Merkle tree that the Bitcoin transactions are stored in takes the SHA256 hash of every transaction and then puts that next to the shot to 56 hash of the next transaction.
So you take all the transactions and you take their shot to 56 hashes and then in pairs you put those hashes next to each other.
And the size of a hash is 32 bytes.

Speaker 0: 00:34:49

Right, that's always 32 bytes.
Yes.
Yeah.
So two hashes next to each other.
I vaguely remember this problem.
We discussed it.

Speaker 1: 00:34:58

So two hashes next to each other is 64 bytes.
And so then the question is, when you are, so I guess it's not two 32 byte transactions because you can't have 32 byte transactions, too small.
Because the minimum size of a transaction, keep in mind that a transaction has an input, at least, and the input is already 32 bytes plus a little bit more because the input of a transaction refers to the hash of a previous transaction.
We just set the hash to 32 bytes.
So then it has to have a number and a few other things.
So yeah, a transaction cannot be 32 bytes, But it can be 64 bytes.
It would be a pretty nonsensical transaction, but it can be 32 bytes.
And so...

Speaker 0: 00:35:36

64.
64, yeah.
But that would look like two hashes that are both 32 bytes.
And why is that a problem?
Because...
Where are these hashes in the blockchain?
It's caused multiple problems in the past.

Speaker 1: 00:35:48

Exactly.
So there is a in each block is a Merkle tree of all the transactions in that block.
And all the leaves of the tree are 32 bytes, these transactions.
And then you go one level up and it's 32 bytes again, it's 32 bytes again.
And now what you can do is you can give somebody a block and say, here's a block and here's all the transactions in this block.
And then you verify it and you see these 32 transactions.
Sorry, you see these two times 32s and you combine them and it looks all good, but somebody could leave out the actual transactions and just pretend that it's only a 64 byte transaction instead of two separate ones.
But then you validate the 64 byte transaction and you say hey this is an invalid transaction so the whole block is invalid and now you think this block is invalid and the next time you see this block because somebody gives you the same block hash you're like I don't you know I'm not gonna check this block it's invalid but actually it's not invalid because somebody sent you because now you got the real one where you actually have the two separate transactions in it.

Speaker 0: 00:36:55

I'm lost.
Who's the target here?
What's the problem and who are we targeting?

Speaker 1: 00:37:02

Well, there are different targets.
So this example, I think, could be used to make a network split where you would make a real block with two 32-byte transactions in it, but that when you combine those two 32-byte transactions, it would also make a real 64-byte transaction.
So the hash of those two transactions, not 32-byte transactions, but the hashes of those two transactions, if you add them together, look like a real transaction, but it's an invalid transaction.
So now you are, or the other way around, the 64 byte thing is valid, but the two individual transactions are invalid.
So if you give somebody a block, it will have the same hash at the top because the Merkle tree is the same at the top and that's the only thing you're communicating when you're communicating a block hash.
So I'm giving you a block hash and I'm giving somebody else the same block hash but I'm going to give you the two transactions And I'm going to give this other person the one 64 byte transaction.
And now one of you is going to say this block is invalid, and the other is going to say this block is valid.
Now you have a network split.

Speaker 0: 00:38:13

Yeah, okay.
I kind of get that now.
Except, what do you mean?
Why would they check for different things?

Speaker 1: 00:38:20

Because I've given you the the block hash the root of the Merkle tree I've also given you all the transactions individually okay so you're actually putting those back in a tree But I'm giving you a different set of transactions than I'm giving the other person.
They get the same root of the tree, but one of them will say, hey, this transaction is invalid, because I don't know, it's spending more money than it's earning some other rule that's violated.

Speaker 0: 00:38:43

Right.
And that's Because it's not really a transaction, it's really two 32-byte hashes.
Yeah.
Am I saying that right?

Speaker 1: 00:38:51

Of real transactions.

Speaker 0: 00:38:52

Of actual transactions.
Yeah.
So for one person...

Speaker 1: 00:38:55

One person sees a 64-byte transaction.

Speaker 0: 00:38:57

One person sees one invalid 64-byte transaction.

Speaker 1: 00:39:00

Or valid.
One person sees one 64-byte transaction.
The other person sees two other transactions doesn't matter what size they are yeah and right if these two transactions are invalid but the 64-byte one is valid yeah then you come to a different conclusion at the block.

Speaker 0: 00:39:19

And this depends on which transactions you saw earlier, essentially, kind of.

Speaker 1: 00:39:25

Well the rest of the block is the same, right?
So It's just that one of these transactions is actually invalid.
So the 64 byte transaction might be invalid or it might be valid.

Speaker 0: 00:39:37

Yeah, I think...

Speaker 1: 00:39:37

That has nothing to do with what you've seen before.
You're basically just giving two versions of the same block that you know think is the same block because it only remembers the hash and it's not.
So that bug has been fixed by simply not storing the block if it's invalid.

Speaker 0: 00:39:53

So-
No, hang on.
Okay.
I have a question.
I still have one question.
All right.
You and I are both running a node, okay?
Yeah.
Now some Joker sends us a transaction, sends us a block that has this 164 byte transaction in it.
Why would my nodes look at this like 232 byte transactions while your node is looking at it like a 164 byte transaction.

Speaker 1: 00:40:21

Because as the joker is sending you the hash of the block and it's sending you all the individual transactions.
So he's sending you two individual transactions at the end of this block and it's sending me one individual transaction of 64 bytes.
So they're sending us two different things.

Speaker 0: 00:40:40

Isn't that just in the block?
Isn't that just the block that he's sending?
That's the block, right?
The In the block is the transaction.

Speaker 1: 00:40:48

When you receive a block, what it really is, is a message.
And the message starts with the header, and it's followed by the list of every single transaction.
And so that list of transactions, it's different.
So if you printed it out on a piece of paper, you would see that at the end of the piece of paper, it's different.
You and I got a different block.

Speaker 0: 00:41:07

We got a different block.
It just has the same hash.
Yes.
It hashes to the same hash.

Speaker 1: 00:41:12

And because you say it's invalid.

Speaker 0: 00:41:14

Yeah, because it is invalid.
The one you sent me is invalid, of course.

Speaker 1: 00:41:17

Exactly, but now if somebody else sends you the correct one.

Speaker 0: 00:41:20

Yeah, then I'll be like, no, I already saw this and it was invalid.

Speaker 1: 00:41:23

Yeah, and so that problem, you know, keep in mind that this problem was discovered in 2012 or something, so back then that attack was cheap.

Speaker 0: 00:41:30

Right.

Speaker 1: 00:41:30

Right now this attack would be expensive but the attack was fixed because basically when this happens to you, you say hey this block is invalid, you just forget it.
And so the next time somebody sends you the correct one, you're fine.
So that attack is fixed.
But then there was other ways that you can fool light clients like SPV wallets using the same trick because they are asking just for an SPV proof.
So they just want proof that a transaction was included and you could now give them a transaction that they think is included because you gave the SPV proof, but it wasn't included because the real block had two separate transactions that happened to combine to this one fake transaction.
And this could be used to steal Lite wallets, but possibly also to rob sidechains if those sidechains only use SPV proofs for peg ins and peg outs.
And that problem, I think was solved by telling Lite clients to be careful.
I don't think it was actually solved.

Speaker 0: 00:42:19

Okay, back to the great consensus cleanup revival.
What's the solution here?

Speaker 1: 00:42:24

Don't allow 64-byte transactions.

Speaker 0: 00:42:25

Well, what if my transaction is 64 bytes though?

Speaker 1: 00:42:28

Then you are out of luck.
So if you still have one of those in the safe, you better spend it.

Speaker 0: 00:42:34

So, if I create a transaction that consists of 64 bytes, because I want to pay exactly this many people, this many coins with these many UTXOs, then the Bitcoin network says no, your money is not valid here.

Speaker 1: 00:42:49

Yeah, I think the actual examples would be burning coins.
So you can make an OPRETURN transaction that burns your coins, doesn't send it anywhere.
And that can be shorter than 64 bytes, but it could also be 64 bytes.
So if you want to burn your money using a operator that is exactly 64 bytes in total, then yeah, you can do that.

Speaker 0: 00:43:10

Are there no normal transactions that are exactly 64 bytes?

Speaker 1: 00:43:13

I believe not.
So You can already not send those in the mempool today.
It won't be relayed.

Speaker 0: 00:43:20

Okay.

Speaker 1: 00:43:21

I think that was the change in version 25.
I think there was a rule that says nothing under 64 bytes, or sorry, nothing under 65 bytes.
That was the mempool rule.
And then people were like, well, but it could be useful to have a 63 byte or 62 byte transaction to burn your coins.
And so I think the rule was changed to no 64 bytes.
So the difference is make this consensus rather than policy.

Speaker 0: 00:43:46

Okay.
So most transactions are well over 64 bytes or at least more than 64 bytes.
That's normal for a transaction to be more than 64 bytes.
If you see a 64 byte transaction, it's kind of something special.

Speaker 1: 00:43:59

Yeah, then it's probably an attack.

Speaker 0: 00:44:00

Okay, right.
And now the great consensus cleanup says let's just get rid of that altogether.
However, 63 or 62 that's still okay.
If you really do like if you're not attacking but you're burning coins that that should work.
But yeah, so basically if people make 64-byte transactions in the future and the soft work happens, then their transaction wouldn't be confirmed.
Then they have to make a new transaction that's either 63 or 65 or something else.
As long as it's not 64.

Speaker 1: 00:44:31

And you can probably malleate it.
So I think we talked about transaction malleation, where you can like mess with another transaction.
So you might, even if you lost the original coin that you used to make this thing, I think you might be able to just make it one byte longer, but I'm not entirely sure about that.

Speaker 0: 00:44:48

Right okay got it sounds like.

Speaker 1: 00:44:52

But this is another case of like yes it would be you know you could just ban everything anything under 64 but or anything under 65 but you want to make the minimum change possible to reduce controversy that's not too complicated.

Speaker 0: 00:45:04

Okay last one BIP 3034.

Speaker 1: 00:45:08

Yeah we did a whole episode about this called episode 87.
It was called the block 1, 983, 702 problem.
Right.

Speaker 0: 00:45:18

What was that problem again?
It was about two transactions that look similar, right?

Speaker 1: 00:45:23

Yeah, so the TLDR of this one is that there was a BIP30 that prevents duplicate transactions.
Because having duplicate transactions, transactions with the same hash, it causes problems.
You can override coinbases, do all sorts of weird things.
It happened a few times in the beginning of Bitcoin.
It was fixed.
The problem of this fix is that it was a slow fix.
So every time there's a new block coming in, you have to check every transaction to make sure that it doesn't already exist and this check is expensive, requires a lot of disk reading.
Unfortunately and so there was a way to speed it up, the way to speed it up was to make, to force the Coinbase transaction to have the block height in it.
So that makes every Coinbase transaction unique, and since every transaction eventually descends from a Coinbase transaction, every descendant is unique.

Speaker 0: 00:46:12

Yeah, that way you can't have duplicate transactions anymore.

Speaker 1: 00:46:15

Yeah, and so then people thought, okay, so we can turn off this expensive check.
But it turns out you can't, because there are some very old transactions before this BIP34 rule was introduced, that if you read them, you could interpret the first bytes of those transactions as a version, sorry, as a block height.

Speaker 0: 00:46:36

Yeah.
And-
So there's something in these old transactions, in these old UTXOs, I guess we should say.

Speaker 1: 00:46:41

Yeah, that is effectively the same as putting a block height in there, but the wrong one.

Speaker 0: 00:46:45

Yeah, yeah, Yeah.

Speaker 1: 00:46:47

And so these ones are gonna start, we're gonna start encountering these and we've already encountered a few, but they didn't cause problems.
So we got lucky.
And so as of the first one we're going to encounter again is block 1, 983, 702.
So there is an old transaction out there that looks like it's at that height.
So in theory somebody could then make a could make a coinbase transaction that's a duplicate of that old one and we don't want that so the pip 30 check the slow check is re-enabled from that hide on.
That's annoying because that check as we said is slow, so the proposal here is to do something else that makes sure that this duplication cannot happen.
So not just putting the height in the Coinbase but also putting something else in it.
What that something else is we don't know.
My favorite is to make SegWit mandatory as in the SegWit commitment because every SegWit block has an OP return and followed by the hash of the witness data.
And right now, if there is no transactions in a block, including if there's no segwit transactions, even in the Coinbase, well then there's no witness commitment.
And so that opportunity is not present, but you could make it mandatory from off.
Basically you could make it mandatory starting at block 1, 983, 000.
And so people will have 20 years to upgrade.
Yeah.
But if they don't, they could accidentally mine an invalid block at that height.
Right.
There's different ways to do it.

Speaker 0: 00:48:16

We discussed this at length in the other episode, of course, which was 87, for anyone who wants to know more about this problem.

Speaker 1: 00:48:24

So that's roughly the...

Speaker 0: 00:48:24

And then also the potential fix, 87.

Speaker 1: 00:48:27

So that's the whole great consensus cleanup.
And so as you can hear, some changes are very straightforward, there's not really any discussion.
Some, there is discussion.
And so we'll have to figure that out.
And then at some point, somebody will have to take the initiative to actually propose this as a soft fork, do activation parameters, hope there's no drama.

Speaker 0: 00:48:49

Well, that is kind of one of the side goals of this proposal, I would say, is figuring out how we actually do soft forks and how we actually do Bitcoin upgrades.

Speaker 1: 00:49:02

Exactly.
This was proposed long before Taproot as a way to sort of get over the SegWit trauma.

Speaker 0: 00:49:07

Yeah.
Like we're still, it's still not clear how we're supposed to do these kinds of things.
So then the idea was let's do something that's very uncontroversial, that everyone should or does or will agree on.
There's nothing, like it's just very obvious bugs that we're going to fix.
And then we can figure out how we're actually supposed to do these soft forks.
And then, you know, it's sort of a good trial run for, you know, future software, I guess.

Speaker 1: 00:49:37

Yeah, now we've already done Taproot, but of course there was still discussion about how that software was activated.
So I don't know if we really now have a, you know, have broad consensus on how to do this.

Speaker 0: 00:49:46

Oh, we definitely don't, sure.

Speaker 1: 00:49:47

But this may be another case of like, nobody cares what the activation mechanism is, just activate it.
The main thing is, of course, this takes away the options of miners to do a time warp attack.
So if they actually like to keep that option, they might veto it, and then you get into more difficult territory.

Speaker 0: 00:50:07

Well, I don't know if we want to get into the whole activation discussion in this podcast episode.

Speaker 1: 00:50:14

We do not.
I'm just saying like it might be straightforward, it might not be and we'll have to we may have to I'm telling you it will not be okay I'm more bullish and of course we keep in mind that you can deploy multiple soft forks in parallel so This doesn't have to be before or after your favorite feature X.
You can activate 10 soft forks at the same time.

Speaker 0: 00:50:38

Yeah, remember when people thought that would actually happen?
Good times.
Good times,

Speaker 1: 00:50:44

indeed.
I'm just saying, don't worry about that aspect.
Okay, I think that's all we've got.
Thank you
