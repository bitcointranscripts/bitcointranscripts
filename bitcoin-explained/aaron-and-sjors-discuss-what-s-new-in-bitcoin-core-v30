---
title: Aaron and Sjors discuss what's new in Bitcoin Core v30
speakers: []
tags: []
source_file: https://bitcoinexplainedpodcast.com/audio/@nado/99.mp3
media: https://bitcoinexplainedpodcast.com/@nado/episodes/99
categories: []
date: '2025-11-06'
episode: 99
transcript_by: 0tuedon via tstbtc v1.0.0 --needs-review
---

Speaker 1: 00:00:00

Intro Music Hello, how are you?

Speaker 0: 00:00:23

It's been a while.

Speaker 1: 00:00:24

It's been a few days.

Speaker 0: 00:00:26

Yeah, we haven't made an episode because we always committed to only making episodes live in person.
There were some exceptions, but I think neither of us really liked that, so we kind of made it a rule.
But I haven't been in the Netherlands for a while now, never mind in Utrecht, so we couldn't do it.
We decided to pick up where we left anyways.

Speaker 1: 00:00:47

Yeah, especially because this is a topic that really nobody talks about, and I think we should.

Speaker 0: 00:00:53

Yeah, there's apparently a very obscure new software release called Bitcoin Core 30, and we thought maybe it's time that someone brings it under the attention of the people out there.
On that point, I do want to start with that a little bit because I think this has been the most...

Speaker 1: 00:01:12

Do we want to thank our sponsor?

Speaker 0: 00:01:15

Yes, thank you, CoinKite.
Thanks for being our sponsor.
Thanks for making the brilliant cold cart and all the other magical devices you put out there.
What's the, Serge help remind me, what's the little USB thing he called?

Speaker 1: 00:01:31

I think it was the coin, the cold power.
No! Oh you mean the open dime?

Speaker 0: 00:01:38

The open dime?

Speaker 1: 00:01:39

The legend.

Speaker 0: 00:01:40

Yes, legendary legendary coin kite.
Thanks for sponsoring us.
Oh my god.

Speaker 1: 00:01:47

I think the OpenDime still doesn't support Taproot.
Because I opened a pull request once to make it use Taproot and they closed it because it wasn't cockroach enough.
Anywho.

Speaker 0: 00:01:59

Anyways.

Speaker 1: 00:02:00

Let's talk about this obscure piece of software.

Speaker 0: 00:02:02

Oh yeah, so I wanted to ask you, we're mostly going to be making a drama-free episode here.
We're going to discuss what's actually new in Bitcoin Core 30.
Like I said, it does seem like this has been probably the most controversial Bitcoin Core release ever.
Like the social media community has been sort of ablaze over all of this.
I don't think I've seen it this bad since the Block Size Wars, and in some ways even worse than the Block Size Wars.
And I'm just sort of wondering, you as a Bitcoin Core developer, I know you're not on Twitter, you're not on X, like how much are you seeing of this or how much does it affect you and maybe others?
Do you have a, can you give some sort of estimation of that?

Speaker 1: 00:02:55

Yeah, I guess compared to the block size wars, because the community was smaller too, this is probably actually smaller in relative terms.
Right, but it's just more money to be made and more attention to be had on social media.
Probably, maybe social media is just worse than it was 10 years ago.
Yeah.
Yeah, like I said, I try to just ignore things as much as possible, other than like the actual facts.
Because just arguing with people on Twitter or even Nostra is just a huge energy drain.
We did record a whole episode on probably the most controversial part of it.
That's our previous episode, the return of the Aperture.
So people can listen to that.
And I don't think anything has changed, although...
I think we'll address a couple of very minor things here in the release notes.

Speaker 0: 00:03:46

Yeah, but that's a good non-spoiler warning, maybe.
We're not going to spend half an hour discussing this change because we made a whole episode about it.
Anyone who wants to know how Shor's thinks about that, or me, can go to the previous episodes.
Previous episodes, that's where we really discussed the up return limit change.

Speaker 1: 00:04:09

I would say if you look at, say, the GitHub repo, and 99% of the work of Bitcoin Core is completely unrelated to these controversial changes.
And that work just continues as before.
It's interesting how, you know, there's like 350 open pull requests on the GitHub repo, and they're almost all like silos.
So one pull request can be super crowded and noisy and the other one is completely deserted and nobody's even looking at it.
I think I've made the analogy before that the Bitcoin Core project sometimes feels like you have a very large Brutalist office building and everybody has a little cubicle.
And if you're in that cubicle, your pull request is like a cubicle.
You might be in multiple cubicles, I guess.
But if nobody comes by, then nobody can hear you.

Speaker 0: 00:04:58

Yeah.
Okay, well, regardless, let's actually kick off with that specific topic just to get it out of the way.
So the up-return policy limit has been lifted basically entirely, right?
Again, I think We've said enough about that.
Anyone who wants to know the details about that can go to the previous episode.
However, there is also another related change that's close to it, but that we did not discuss in the previous episode, which is, I think there's also a policy rule, is that it's now also possible, besides bigger upreturns, to include multiple upreturns in one transaction, right?
We did not cover that last time.

Speaker 1: 00:05:45

I'm not sure if we did, but we can just repeat it.
So you can either make one operator and that is the maximum size of a transaction or less, or you can make multiple ones, which can ultimately add up to the same size.

Speaker 0: 00:06:01

Yeah, that's important to note.

Speaker 1: 00:06:03

I would say that's mostly a simplification.

Speaker 0: 00:06:07

Well, it's important to note because in this entire shitstorm, it has been brought up as well as another supposedly bad thing that Bitcore developers have done.
But as you point out, even if there are multiple upreturns in a transaction, the total size of these upreturns are still bound to whatever the limit is.
And this limit, even in BAKERCORE, is still configurable, right?

Speaker 1: 00:06:38

Yeah, so we kind of went back and forth on that.
The initial idea was to completely drop it because it's essentially a placebo, but There was a lot of drama.
So eventually, I think now the default has been changed.
There's no limit.
But if you do set a limit, the only difference between now and before is that the limit applies to the total for a transaction.
So let's say you set the limit to 83 bytes.
That was, I think, the previous default.
Then somebody could make, I guess, 20 upper churns of 2 bytes each, if they somehow wanted to.
Now that'd be pretty expensive for them, because every output has an overhead.

Speaker 0: 00:07:15

Yeah, I'm pointing it out because there was a point of critique, as I mentioned, that okay, you can change the default setting now, you can change it back to where it was.
But the critique was, but now you can still include multiple operators in a transaction.
However, The point is that if you do change it back to, let's say, 83 bytes, then if you then put multiple upreturns in a transaction, then their combined size can still only be 83 bytes.
So, even if you do change the defaults, for whatever reason you may think you want to do that, then that is still the actual limit for upreturns.
You can split it up into two different upreturns, but it's still 83 bytes in that case, right?
Yeah, okay.
So then why you said the change was made, and I'm talking again specifically about the fact that you can include multiple opportunes, that was made as a simplification?

Speaker 1: 00:08:11

That's how you're— Yeah, I mean, it depends on how you look at it, I guess, but The idea was there can only be one, so that restriction is dropped.
Now it doesn't matter how many outputs are opportunes.
So the rules are simplified, whether that actually is simply in the code, that's debatable.
Now you have to check the total against multiple outputs.
As long as the option is there at all, there's some complexity.
As soon as you remove the option, it becomes simpler because you're just not counting it at all.
But now, it has to count.
Look at the first output, look at the second output, look at the third output, and then complain when something goes over it.

Speaker 0: 00:08:45

And because we're talking about a policy rule, just to repeat this point, it does not apply to the consensus rules.
If your node receives a block with a transaction in it that has bigger up-returns than whatever setting you're switching it to, then you'll still accept that.

Speaker 1: 00:09:05

Yeah, in fact, a block could contain a 4 megabyte operator in a single transaction, which would not be even possible with the new Bitcoin Core over the mempool.
Yeah.
So each transaction is limited to 100 kilobytes in general.

Speaker 0: 00:09:18

Yeah, so what is technically new in this specific instance is that there can now be multiple OP returns in a transaction on whatever size you want to put that setting.
And then if it's within that size, you will accept it in your mempool and relay it to other nodes, correct?

Speaker 1: 00:09:36

Yes.
And so just a little bit more background on why, you know, such a...
I mean, first of all, if the setting was entirely removed, which was the initial idea, it's actually a simplification.
But because the setting is still there, we still need to look at the total, so you could argue it's not really a simplification, but it is in the long run.
But another reason to do this is because if somebody has a need to have multiple upper turns, and I don't know if anybody does at the moment, but if they do, and we still have this limit of one opportune transaction per turn, one opportune output per transaction, then there is another incentive for people to go outside the mempool and use accelerators, which creates the centralization pressure that we tried to solve in the first place.

Speaker 0: 00:10:18

Yeah.
And on that point, what I also find interesting to sort of highlight here is that your reasoning, so you said, we don't know if there's a use case for it.
Maybe there is, maybe there isn't.
That in itself has drawn a lot of ire.
There seem to be a lot of people that feel that unless you can prove that there is a use case for it, you shouldn't make any changes.
While you, and I agree with you, see it more as, well, if there's no harm, if there's no harm, then what's the problem?
If there's no harm and you simplify the code, then that seems like an improvement.

Speaker 1: 00:10:58

Yeah, though I guess in this case, where the confusion comes from is, or potentially comes from, is that initially the idea was to drop the setting entirely.
And because we haven't dropped it entirely now, the simplicity argument isn't as strong.
But yeah, The problem with these alternative use cases is if you wait until they're actually fully deployed and they go around the mempool because they're already deployed, now you lift the limit and, well, they're already going around the mempool, so why would they change anything?
So you might be too late if you keep chasing these things and Bitcoin Core only releases once every six months.
And we'll have another topic on the list where something similar happens where it was a response to actual behavior.
So we were a little bit late this time, I guess.

Speaker 0: 00:11:45

Yeah, so if you're being reactive on these things, you're actually too late.
And if there's no harm in doing it, then it's better to just do it now in case someone might need it.

Speaker 1: 00:11:55

Especially because the total amount doesn't change, right?
Like you said, you can spread it over multiple outputs.

Speaker 0: 00:12:03

Yeah, okay.
Let's move on from that point.
Anyone who was listening specifically to hear more about the Operator in Drama can now switch off because we're going to talk about other interesting notable improvements in Bitcoin Core 30.
Right, Or was there anything else you wanted to say about this?

Speaker 1: 00:12:20

Yes, but I was just changing the sequence of items on our to-do list.
All right, let's talk about the minimum relay fee then.
Because that's sort of in the same area of changes, and then we'll move on to completely different changes.

Speaker 0: 00:12:44

Okay, It was very important to adjust that in the Google Doc that no one else will see besides you and me.
Good thing that you did that.

Speaker 1: 00:12:52

Exactly.

Speaker 0: 00:12:54

Okay.
So yeah, so this is another policy change, which, okay, so that's the minimum fee that is included in a transaction, can now be lower before Bitcoin Core nodes will accept it in the mempool and relay it to other nodes, right?

Speaker 1: 00:13:13

Yeah, so it used to be 1 Satoshi per Vbyte, now it's 0.1 Satoshi per Vbyte.
And this is a case of people start doing things and Bitcoin Core has to follow, otherwise everybody will go around the mempool.
So what started happening is because the fee market is such an amazing success.
Yeah, people wanted to pay less fees.
And well, like I said, I'm not on social media myself at the moment.
But my understanding is that there was sort of a Twitter movement for people to individually configure their relay fee to go lower by a factor of 10.

Speaker 0: 00:13:51

Yeah, and that was...

Speaker 1: 00:13:52

Some of us followed that example.

Speaker 0: 00:13:54

And so that was...
Sure, that was always possible with Bitcoin Core.
Any individual user could already lower the main relay fee?

Speaker 1: 00:14:06

Yes, it's a matter of changing a setting.
Now, keep in mind, everything is possible with Bacon Core if you recompile it yourself, but in this case, it's just a matter of changing a setting.
So you can already lower it to 1, 000th of a Satoshi per feedbyte.
Not lower because the amounts internally are processed at that resolution.
So you'd have to do some more changes if you want to go even lower than that.
But I guess, Yeah, people settled on about 10x lower.
And some miners followed, and that means these things get mined.
But that means if you don't change your default setting, now you're kind of surprised about what gets into blocks.
And that surprise hurts compact block relay, among other things.
So we talked about compact block relay in our previous episode, but generally the idea is that if you're sending a block to the next person down the line, to one of your peers, if you know what's in their mempool, you really only need to send the header of the block and a summary of the transactions, like a list of the transaction IDs, rather than the full block with all its contents.
But if you don't know what's in somebody else's mempool because they changed some setting, now you have to send the whole block over.
And so this delays propagation network wide.

Speaker 0: 00:15:18

Yeah, it's better for the health of the network if blocks find their way across the entire network as fast as possible.
And that requires that mempools closely reflect the actual blocks that are being mined.
So if for whatever reason the blocks start to look different, in this case because very low fee transactions start to make their way to miners, then it's actually better for the health of the network that everyone adapts the same behavior.
So in this case, and also very relevant to the upper turn issue, but in this case as well, Bitcoin Core has decided to allow lower fee transactions in the mempool and relate it to other nodes in order to better reflect the mempool with blocks that are being found.
Good summary?

Speaker 1: 00:16:13

Yes, and so this has been a general theme now over a few different topics.
We've seen with RBF, full RBF, the changes.
We've seen it with Operaturn.
Now we're seeing it with the fee rate.
And the response has been slightly different in different cases.
So in the case of full RBF, you had somebody basically promoting that concept, releasing an alternative client, and then BitConcord did not follow until at some point, you know, all the miners, or at least a large chunk of the miners were doing this and compact block relay was broken.
And so then Bitcoin Core said, okay, let's turn RBF on.
So arguably that was too late.
Because we already had broken compact block relay and the longer you let that sort of centralization risk exist, maybe at some point the damage is irreversible.
Probably not in this case.
Okay, so then we had the OpryChurn stuff where Bitcoin Core developers saw that a use case was imminent and tried to preempt it.
That caused an enormous amount of drama.
And now it's kind of in between, like this spontaneous change in policy by users and beacon core follows it just a month or two later.

Speaker 0: 00:17:30

Yeah, I do think it's...

Speaker 1: 00:17:32

I don't think there's really consensus on how to best deal with this.
Like these three options, you can either be too early or too late or right on time.
And at some point there might be a deviation from in policy that is simply not acceptable, as in it would just be unsafe, cause a DOS problem.
And at that point, there's nothing BitConcord can do other than propose a consensus change or just accept that nodes are slow or vulnerable or something bad like that.
So it's not a healthy development, I think, but people do what they do, right?
It's an open source, open system.

Speaker 0: 00:18:08

Yeah, and I think that's an important point to emphasize here because this says a lot about how the Bitcoin Core project sort of operates.
It's that you guys, you are one of the Bitcoin Core developers, you don't see yourselves as authorities that decide how other people can or even should use the network.
It's not in your control how people, what kind of transactions people send or what kind of transactions miners mine.
Bitcoin Core can only, you know, adjust to that.
So And then, like you said, there are a couple of ways to do that, which is either sort of, you know, do it in advance when you see it coming, or only do it when it's kind of too late.
And that's sort of the difficult aspects here to balance.

Speaker 1: 00:18:57

Or worse, like you can't do it at all, because there might be some trade-off that's really unacceptable.

Speaker 0: 00:19:03

Yeah.
So this is a good example of that as well.
Users were already starting to relay very low fee transactions.
Miners were already starting to mine that.
So then BitHook Core in this release said, okay, we're going to lower the fee minimum in order to better...

Speaker 1: 00:19:21

And this change, I don't think this change is particularly bad because, you know, the last time this limit was lowered, I think it was 10 sets per fee byte in the past, or maybe five, and the price has gone up 10, 000x.
So if you look at this, you're gonna have to look at it as a DOS, like a denial of service protection.
If the minimum fee relay is too low, then somebody can just cheaply cause you to use a lot of bandwidth, everyone to use a lot of bandwidth.
Right, and so I think the initial calculation years ago was done on like, okay, if somebody spins up a bunch of Amazon nodes and just starts flooding us with random data, you know, How much does it cost them versus how much does it cost the ecosystem?
How much cost does the attacker have and how much resources of the community are they wasting if you add up everybody's node costs?
And so I think we're still quite on the safe side of that equation.
It's really expensive for the attacker.
They need to spend quite a lot of SATs to cause people to use bandwidth.

Speaker 0: 00:20:25

Yeah, okay.
One last note on this point, because I noticed that in the GUI, that change...
Yeah, so in the user interface, that change does not apply.
Like the minimum fee if you want to send a transaction is still the same as it ever was, right?

Speaker 1: 00:20:45

Technically, it's the wallet that's unaffected.
So the wallet can be used from the command line.
You'd be surprised some people use it from the command line and they like it.
But yeah, as far as I know, the wallet still has one set per view byte as a minimum.
I think you can manually set it lower but my guess is the wallet will follow in the next in a later release.
You kind of want to make sure that the network actually relays your transaction because let's say we change the wallet now to use this 0.1 set per view byte and you start your GUI and you have maybe five peers and none of them you know have this custom setting because you know a lot of people do but not everybody does so you might not be connected to anyone he does.
So you sent your 0.1 sats per fee by transaction and it just gets rejected by your peers.
And they don't tell you it's rejected.
So you just, you send it, you close your wallet, you go to sleep and the next morning you're like, why isn't this confirmed yet?
It's because it never went anywhere because you only had your note open for five minutes and none of your peers accepted your transaction.
So you kind of want to be a bit conservative when it comes to the wallet.
But I think you can just do it manually if you want to.

Speaker 0: 00:21:58

Right.
So in that sense, BitHooker actually also adjusts to the situation on the network.
It will only be implemented in the wallet once there's a good enough likelihood that it will actually make its way through the network.

Speaker 1: 00:22:12

Yeah, and of course there's also a bottleneck of just that very small number of people that work on the wallet in general in Bitcoin Core.
I don't think we've adjusted the new RBF, I don't think we've adjusted to the new RBF reality yet, for example.
And there's some...

Speaker 0: 00:22:28

How so?
You can use RBF for Bitcoin Core, right?

Speaker 1: 00:22:33

Yeah, well, Bitcoin Core wallet has been setting the RBF flag for wallet transactions for many years.
We don't have to anymore because it's gone.

Speaker 0: 00:22:43

But there's also no harm in doing it, I guess.

Speaker 1: 00:22:46

No, and well, there's actually harm in turning it off.

Speaker 0: 00:22:49

Maybe privacy.

Speaker 1: 00:22:51

Yeah, you can see who upgraded if we change this.
And maybe something similar applies to fee rates.
If we suddenly drop it, then you can see who's upgraded.
So I'm not sure what the right path is there.

Speaker 0: 00:23:01

Right.
Okay, let's move on to the next point.
Cool.
Actually, I think this is also, there's another policy issue.
There's a new policy rule, just correct me if I'm saying anything wrong, but there's a new policy rule that restricts the number of signature operations, SIGOPs, per transaction or no, per output, right?

Speaker 1: 00:23:24

Yeah, so we did a whole episode, 93, about the great consensus cleanup restoration software proposal, which deals with time warp attacks, and one of the attacks that soft fork proposed soft fork is trying to deal with is Preventing somebody from making a transaction that takes like an hour and a half on a Raspberry Pi to Sorry to create a block that takes an hour and a half on a Raspberry Pi to validate.
And maybe several minutes on a modern computer.
Because if a malicious miner produces such a block, they can stall their competition and maybe get a headstart out of that.
But in the way that was fixed involves that particular rule.
So this is 2, 500 CCOPS limit per, I think it's per transaction.

Speaker 0: 00:24:18

Okay, but just explain what it is.
It means basically, if I understand correctly, you can make a transaction or an output with what...
So you're not sure which of the two it is?
It's either a transaction or an output?

Speaker 1: 00:24:31

I think it's per transaction, but what you're counting is you're counting SIG ups in the inputs and in the outputs.

Speaker 0: 00:24:40

Okay, so that can be a maximum of 2, 500 signatures basically in a transaction then, right?
That's what it means.

Speaker 1: 00:24:48

Yeah, signature operations is slightly different.
So for example, a legacy multisig, or bare multisig as we called it,
I think it counts as 20 or something like that.
I'm a little fuzzy on the details here, but basically it's a limit in the number of signature operations.
No sane transaction would actually go over those limits.

Speaker 0: 00:25:13

Because it's thousands.
Yeah, exactly.

Speaker 1: 00:25:16

You'd need a very insane kind of multi-sig.
So the only people who would be making such a transaction are people trying to DOS a network or people doing experiments.
I think there were some historical examples of these actually violating them.

Speaker 0: 00:25:32

Okay, so right now if you make a transaction with 3000 SIGOPs, well, it can still be mined in a block.
It is still consensus valid, correct?

Speaker 1: 00:25:45

Yeah, and that doesn't change, right?
This is a policy change.
So the only thing that changes is you can't relay it anymore.

Speaker 0: 00:25:50

Right.
So if someone sends a transaction like that to you and you're running Bitcoin Core 30, then you're going to not include that in your mempool and not relay it to other nodes.
But if it's in a block, again, then that's still fine.

Speaker 1: 00:26:03

Yeah, and this change is there to protect future miners.
It's not really there to protect the network because I don't think they're that terrible.
But a future miner, when and if, or if and when this becomes a soft fork, then it is consensus.
And we don't want a miner to accidentally mine this thing.
And so that's one of the reasons, that's one of the goals of policy rules is to prevent accidentally mining something.
Because the miner does it as a standard transaction, they'll never see it, they'll never mine it.

Speaker 0: 00:26:35

Right, so it's kind of in anticipation of hopefully, potentially a future soft fork to already sort of, you know, push network behavior kind of in that direction so that when the soft fork happens, then it's a relatively small change that can't really cause too much problems, essentially, right?

Speaker 1: 00:26:54

Yeah, exactly.
You want soft forks to be as safe as possible for users, but also for miners.

Speaker 0: 00:26:59

Yeah, And I think also, so that ties in with, I guess, another point.
We do apparently keep getting back a little bit to the Operatron issue.
As a general sort of direction, I think the goal of the Bitcoin Core project is to essentially, you know, as much as possible, just get rid of policy rules and make what nodes accept and relay as close as possible to the actual consensus rules.

Speaker 1: 00:27:27

Is that correct?
There is a philosophy that says that policy and consensus should converge.

Speaker 0: 00:27:33

Yeah, exactly.

Speaker 1: 00:27:35

I don't know if that's realistic, but one of the reasons is that one of the goals of, one of the use cases for policy is upgrades, upgrade hooks.
Upgrade hooks means that, say, SegWit version 2, or 3, or 4, currently is not standard, so it will not be relayed, but it is consensus valid.
It's just that if you mine it, it has no meaning.
So that's a case where we don't want them to be the same because you would simply never be able to upgrade.

Speaker 0: 00:28:08

Sure, yeah.

Speaker 1: 00:28:09

So I get the philosophy of like you don't want to have these pedantic limits as some people would call them, like the opportune size or RBF things.
But it's not, I don't think it's true that consensus and policy cannot be identical because you would never be able to upgrade Bitcoin anymore.

Speaker 0: 00:28:25

Yeah, you still gotta leave the room for upgrade.

Speaker 1: 00:28:28

Or you'd make it, depending on how, you could also say well you'd make it completely unsafe.
So you could also say well let's just allow SegWit version 3 relay and not worry about it.
But then people can shoot themselves in the foot and give away their money.
Because you would get a BC1F address which might be some future SegWit version, I don't know what the letter F maps to,
and you would just send to it and that money would just disappear and it wouldn't even go to anyone.

Speaker 0: 00:28:57

Okay, what's, just to give our listeners a sort of rough idea because so now the limit is 2500.
Like you mentioned, that is probably far beyond anything that anyone would ever use for any real reason, essentially.
What kind of impact does this actually have on a note?
Let's say this limit is touched.
There is a transaction that actually has 2500 SIGOPs. Are we talking about a transaction that's going to stall your note with like a second or not even that?
Or what sort of ballpark do you think about?

Speaker 1: 00:29:36

I haven't looked at the exact numbers, but my guess is it's negligible.
Like this is very safe for individual transactions.
And one of the reasons is that the policy...
There's another policy limit which limits transactions to 100, 000 kilobytes.
So my guess would be that the combination of these high numbers of seagulls and a very large transaction are what really is more dangerous.
You got to keep in mind that we have this quadratic phenomena in Bitcoin, so quadratic hashing that's what solves the segwit, but legacy transactions still...
If you simplify it, If two transactions of one kilobyte have like one bad each, right, it adds up to two bad.
But if you make it a two kilobyte transaction, it might be four bad.

Speaker 0: 00:30:31

It's bad times bad.

Speaker 1: 00:30:33

Yes, So if it's one big transaction, it's much worse than several small transactions, quadratically.
And so, that's probably why an individual transaction violating this policy limit is not going to be a problem, but a minor could include a bigger one.

Speaker 0: 00:30:49

Right.
But in any case, to summarize this, a transaction that has 2, 500 sig ops is both very implausible to be used for any real reason, while at the same time also still well within safety limits.
So that's why, at least as a ballpark, that number was picked.

Speaker 1: 00:31:08

Well, yeah, and in general, the idea of this consensus cleanup thing is to mitigate the worst-case scenario without confiscating any legitimate use case or getting anywhere near legitimate use cases.
Yeah.
So there is a trade-off.
You might not be able to solve like...
There might still be blocks that are slow to validate but not as slow.
You can't have a perfect solution, because then you're going to start risking that you confiscate somebody's very obscure, but still potentially real setup.

Speaker 0: 00:31:42

Yeah.
Okay, Let's move to the next point.
An other improvement is one parent, one child orphanage, or there's something improved in that sense.
Can you remind me what it is?

Speaker 1: 00:31:56

Yeah, we have covered this in previous episodes, But a quick recap is that one parent, one child transactions packages are useful for especially tools like Lightning.
So in the Lightning network, when two people have a channel, they need to agree on a force close transaction or a penalty transaction.
Basically the transaction that you can unilaterally close the channel with so if you and I have a channel and one of us is offline we both have a transaction to close the transaction without talking to the other side But we have to decide how much fees go into that transaction.
And we don't know how much fees the future is going to hold.
So that's always been a bit of a complexity in Lightning.
And the general solution to that is anchors, where you allow yourself to add a transaction later, a child transaction later.
And there are different mechanisms to do that.
And a lot of them separate from pinning attacks, where you would add a transaction, but somebody else would add another one and you wouldn't be able to bump it and it would never get confirmed and you'd be too late and people cry.
People came up with the concept of ephemeral dust, which is not the Finnish metal band, which basically lets you make a transaction with a zero fee, zero amount output.
And then the child spends that zero fee, zero transaction output and pays whatever fee is necessary and can decide that at the last moment.

Speaker 0: 00:33:25

Yeah, and to do that, you of course have to add some of your own coins then.
And basically what you're doing is you spend that zero amount output to yourself in combination with some real money bitcoin sats that you're sending to yourself and you include a fee in that new transaction and if that you know now because this is a new transaction you basically know exactly how much fees you're supposed to include for it to confirm within a reasonable time.

Speaker 1: 00:33:53

Yes, and you can replace it if fees go up immediately.
So, that's a nice solution.
Normally, you're not allowed to relay a transaction that has a zero fees, zero that has no fees in general, of course, that's not going to relay.
Having an output with a zero amount is also not going to relay because we have a dust limit there.
The idea is that you can relate them as a package, a one-child, one-parent transaction.
So it's ephemeral dust because the dust exists, but it's immediately spent, and it always goes as a pair in the same block.
So the block never creates any dust, only the transaction does.

Speaker 0: 00:34:30

Yeah, the zero set transaction is immediately, or output is immediately spent in the same block.
It's just, it's immediately gone, right?
That's the point.
Yeah.
So what's the improvement in Bitcoin Core 30?

Speaker 1: 00:34:44

The improvement is that this mechanism under the hood relied on something called the orphanage.
And the orphanage is a way for Bitcoin Core to see, hey, I just got a new transaction, but I don't know what the parent is, so I'm just going to keep it for a little bit and then ask the peer for the parent.

Speaker 0: 00:35:00

And so the orphanage is specifically for transactions that do make it to you over the peer-to-peer network, but you don't see basically where it's coming from on the blockchain.

Speaker 1: 00:35:11

Yeah, it's not spending anything you know.
So you're like, tell me what the parent is and the peer sends it to you.
Right.
That mechanism has been around now for I think since version 29.
The problem with that mechanism is that it's very easy to attack.
So you can flood the orphanage basically with infinite child transactions.
That can just be complete garbage transactions because the node has no way to know that a child is a real transaction.
So it's essentially free to, if you know what peer you want to influence, you just flood them with orphans basically.
And it's a first in first out system, so once 100 orphans are there, you just replace all 100 of them, and there's no orphans anymore.
And so this relay mechanism doesn't work.
So I guess in the lightning scenario, if you are trying to attack your counterparty and you roughly know what peers they're connected to,
maybe you can blast their orphanages out and then your peer will not be able to get their penalty transaction out.
Something like that, that would be the risk.

Speaker 0: 00:36:19

Yes, I would feel.

Speaker 1: 00:36:20

So version 30 makes the orphanage a lot stronger.
It basically, well, I don't understand the full mechanism, but it boils down to, If one of your, let's say you have 10 peers, and one of your peers starts misbehaving by sending you tons and tons of orphans, you're not just going to flush them all.
You're only, if another peer also sent you that orphan, you're gonna hold onto it.
So there's just a better accounting system that makes it more difficult to attack the orphanage.

Speaker 0: 00:36:52

Bitcoin Core is protecting the kids.

Speaker 1: 00:36:54

Exactly, yeah, yeah.
Protect the children.

Speaker 0: 00:36:58

Okay, so the orphanage is more robust now.
Next point.

Speaker 1: 00:37:04

Yes, there's a Bitcoin command, but I think that was a bit too nerdy.
I don't know if you cared about it.

Speaker 0: 00:37:09

Oh yeah no no go for it though yeah.

Speaker 1: 00:37:11

There's one command to rule them all so there used to be Bitcoin D, Bitcoin QT, Bitcoin well Bitcoin D and Bitcoin QT basically and then there's some other changes coming up that would add Bitcoin Node and Bitcoin GUI and you know other developers like okay this is becoming a confused mess somebody downloads Bitcoin and they see like 15 commands that start with Bitcoin.
What to do now?
And so the solution is to add another command which is just called Bitcoin And you call that command and you tell it what else to call.
So it has a documentation, you call Bitcoin space node, it starts BitcoinD.

Speaker 0: 00:37:59

There are 15 standards.
That's too many standards.
We need a standard to rule them all.
Now there are 16 standards.

Speaker 1: 00:38:07

Yeah, exactly.

Speaker 0: 00:38:09

So this is for nerds that use the command line, which as you said, command line doesn't exist for me.
If it's not in the GUI, sure, so I'm not aware of its existence.
I don't care about it, but this is for those people like yourself that for some reason prefer to use that, right?

Speaker 1: 00:38:30

Yes.

Speaker 0: 00:38:31

Okay.

Speaker 1: 00:38:32

Well, one such user might be a miner.

Speaker 0: 00:38:36

Sure, I mean, I'm sure there's a lot of people that use it.

Speaker 1: 00:38:41

That was a bridge to the next topic.

Speaker 0: 00:38:44

Oh, so you're Clever.
IPC mining interface.
Yeah, I don't remember what this was.

Speaker 1: 00:38:54

Tell me.
Tell me more.
We talked about Stratum V2 a couple of episodes ago.
We had, Yeah, well, we did, I think in multiple episodes.
There has been the idea of decentralizing mining, Stratum V2 is one way to do that.
It adds encryption for one thing, and it also adds the ability for individual miners to create their own block templates.
To kind of separate, you know.
And that is mostly...

Speaker 0: 00:39:21

I mean, it's basically a way to decentralize mining pools, right?
Miners on a pool can for themselves decide what they put in blocks.

Speaker 1: 00:39:29

Yeah, And this mostly exists outside of Bitcoin Core.
There's a project called the Stratum Reference Implementation, SRI.
They make all sorts of software tools, like to run your own pool, to convert between Stratum V1 and Stratum V2, to make your own block templates, etc.
But they do need Bitcoin Core for one thing, which is to make the block templates.
And also to send the solution if you find a block.
And this part is called the template provider.
And so the original idea was for, when the spec was written, was for Bitcoin Core to be the template provider.

Speaker 0: 00:40:04

Just to be very clear about this, templates basically just means everything that goes into a block.

Speaker 1: 00:40:10

Except the solution for it.
Yeah, except the nods.

Speaker 0: 00:40:13

Except the hash, yeah, sure.

Speaker 1: 00:40:15

And the payout stuff.
Yeah, so Bitcoin Core is good at making templates, but the problem was that in order for Bitcoin Core to do this, it would have to speak the StatMp2 protocol.
So it would have to support the same encryption standards and new messages.
And so this was implemented by me and a few others, and there was some resistance to adding, basically to adding all this extra complexity, adding these extra cryptographic methods and listening to ports and processing messages, etc.
So then a compromise was reached, which is that we'll have Bitcoin Core listen on a protocol we call IPC, Inter-Process Communication, and it's not directly supporting Stratum V2, but it does support the messages that Stratum V2 needs, or it can give the information Stratum V2 needs.
So it can give a block template, it can push a block template, etc.
And So that's what's in version 30 of Bitcoin Core.
And then you can use a separate application to connect to Bitcoin Core and actually, basically translate this to the actual Stratum V2 language.

Speaker 0: 00:41:30

Right, so let me repeat this back to you and see if I get it.
So Stratum V2 is basically a different project.
It's a mining specific project.
It's like I said, a way for mining pools to decentralize part of their operations.
Namely, individual hashers, you know, users of the pool, miners, they can decide what goes into a block, which transactions go into a block.
But for that, they would actually use Bitcoin Core to hear what transactions are on the network, etc.
And use this to construct essentially the block.
And then now there's kind of a bridge, a way to connect with the Stratum V2 protocol in order to make it all work.
Is that a good enough summary?

Speaker 1: 00:42:19

Yeah, exactly.
So there's a bridge between Bitcoin Core and the rest of the Stratum V2 ecosystem, and it uses this new IPC system.
Right.
Which initially was intended for something completely different, namely the separation of processes.
So it was designed to split the node from the wallet and from the GUI so that if one of them crashes, the other doesn't crash.
And we might still do that, but for now we basically repurposed this tool.
Right.

Speaker 0: 00:42:47

So right now, the only mining pool that I'm aware of that uses Stratum V2 is Demand Pool, but they're kind of still in startup phase, I think.

Speaker 1: 00:42:57

And Brains as well.

Speaker 0: 00:42:59

Do they use it?

Speaker 1: 00:43:00

Yes, but I don't think they do their own, I don't think they offer custom templates.
They just support the new technology.
But that's already an improvement because if you run your ASIC farm and you connect to any Stratum V1 pool now, your router or your internet provider or anyone can just steal your hash rate.
Yeah, yeah, yeah.

Speaker 0: 00:43:22

That's no good, Sjoerd.
But, yeah, okay.
But Brains does not, or at least not yet, allow individual miners to construct their blocks.

Speaker 1: 00:43:32

I don't believe so.
And Demandpool does plan to do that, but I don't think they've actually launched this yet.
So there was a bit of a chicken egg.

Speaker 0: 00:43:40

I happen to know that they're getting close to sort of launching for real, basically.

Speaker 1: 00:43:46

Oh, that's good news.
It has been a bit of a chicken egg problem on the Bitcoin Core side because shipping this new, even this new IPC interface was also controversial partially because nobody was using it yet and so there's some people that say well we should first thoroughly test it with the pools and etc.
To make sure it's right and then ship it.
Whereas the counter argument to that is, well, the pools are not going to test it if it's not already shipped in Bitcoin Core, because it's too much of a pain for them to compile some custom experimental version, and especially if they're not sure that it's actually going to be deployed, right?
They need to have at least some confidence.
Yeah.
There was that chicken egg, but now it's in the release.
But it's not completely final yet, so it might still make a few breaking changes in the next release.

Speaker 0: 00:44:31

Okay, I was just gonna, so I was gonna ask, oh, is this completely good to go now, or is there still work to be done on the Bitcoin Core side?

Speaker 1: 00:44:39

No, there's still, I mean, it should, it's usable, but I think it can be improved.

Speaker 0: 00:44:44

Right, sure.
Okay, any last thoughts on this topic before we move to the last one on our list?

Speaker 1: 00:44:54

No, let's move.

Speaker 0: 00:44:55

Okay, last one on our list is...
You explain this to me.

Speaker 1: 00:45:02

NATs BMP Import Control Protocol, PCP.
We have covered this in earlier episodes.
It's a lonely world out there, especially if you run your node from a residential place.
Typically, your router will block any connections to you.
So your node can reach the outside world, but the outside world cannot reach you.
And there's various methods that's often used.

Speaker 0: 00:45:27

Don't call us, we'll call you kind of a...

Speaker 1: 00:45:31

Yes, and now in the world of gaming and torrents, etc.
There have already been methods developed to change that, so that you can actually listen to people connecting to you.
Because there's some performance reasons that you want to do that.
And other reasons why you want to do that.
And Bitcoin Core was using that from very early on, like 2012 or even earlier.
But the method it was using back then was unsafe, it was called UPnP, and so it was kind of turned off by default.
It's there, it's always been there, but it was off because there were too many vulnerabilities in the software.
And as of recently, we have a brand new method.
By brand new, I mean it's a 10-year-old standard probably, called PCP, Port Control Protocol.
It's been implemented from scratch in Bitcoin Core itself.
And as of version 30, it's on by default.
So that means if you install your node freshly, and if your router supports this protocol, which it may or may not, I think a lot of modern routers will support it, Your node is listening, which means you can have a bit more connections and the network is going to be more robust.

Speaker 0: 00:46:37

Yeah, so basically, normally if you start up a node, then you can connect to other nodes, but other nodes cannot connect to you.
Which means there is essentially a subsection or a sub-community, whatever you want to call it, of Bitcoin Core nodes that are providing more services or more connection to the rest of the network than others.

Speaker 1: 00:47:01

Yeah, they're going to be better connected and also there's a demand on those nodes because there's only a limited number of them and everybody wants to connect to them.

Speaker 0: 00:47:10

Yeah, so it's a slightly centralizing factor actually that everyone sort of initially...

Speaker 1: 00:47:15

I wouldn't say centralizing because there's plenty of them, but they could get overloaded.
If the ratio becomes too asymmetrical, then the few notes that are listening will get completely overwhelmed.

Speaker 0: 00:47:29

I didn't say centralized, but I would say that is a sort of centralizing aspect, right?
It's better if all nodes are sort of equal in that sense and everyone helps each other rather than everyone relying on some subset.

Speaker 1: 00:47:42

It's better, but I don't think there was a risk of centralization here.
But I do think there's just a risk of overloading these resources.
And part of the problem is because we want to move away from...
So, Bitcoin nodes want to connect to a diverse set of peers.
And not in the woke sense of the word, but in the as many places in the world like different countries, different networks, so that it's harder to trick you for one network operator to trick you.
There's a new project we talked about years ago in a podcast called ASMAP, where we try to map the internet and then try to connect it really to different countries etc.
And one of the side effects of that project is that we might start connecting to very obscure places and a lot of nodes would start connecting to those very obscure places because they're trying to diversify a bit too much.
And then those, like you run in some random place in South America, you have an internet provider that with just one Bitcoin node in it, and then like thousands of nodes try to connect to you because you are very unique and special.
And so if more nodes are listening, then hopefully on that obscure internet provider, there's also going to be more nodes listening.
So not all the traffic just goes to that one listening node.

Speaker 0: 00:49:00

Yeah, okay.
So, and this is...
Sorry, what exactly is new in BitMarkore?
Like, this is now just a thing, or?

Speaker 1: 00:49:08

So this feature has been in there since the last version, but it's now on by default.
So if you upgrade and you didn't manually turn it on or manually turn it off, it will be on.

Speaker 0: 00:49:18

If you turn it off, it's not going to be turned on.
Then it can be called by the outside world.

Speaker 1: 00:49:23

If your router supports it, yes.

Speaker 0: 00:49:27

Okay.
Do routers generally support this, or what's the if there?

Speaker 1: 00:49:32

I'm not sure.
Like, we'll find out.
Like, it should be pretty clear in the stats that the number of listening notes would go up dramatically.
Because at the moment, most of the listening notes are on tour, because the way people set up their tour notes usually is such that they're also listening.
So that's why some people are saying, oh, the majority of Bitcoin notes is on tour.
Well, that's not true.
The majority of listening Bitcoin notes is on tour.
But that might no longer be true eventually.
Right, right.

Speaker 0: 00:50:01

PCP is also a type of drugs.

Speaker 1: 00:50:05

That's not my expertise, but you tell me.

Speaker 0: 00:50:08

Coincidence?

Speaker 1: 00:50:09

I think every three letter acronym probably is.

Speaker 0: 00:50:14

Okay, I think we made it through the list, Shorts.

Speaker 1: 00:50:17

We did.
Well, in that case, unless you have anything to add?

Speaker 0: 00:50:22

No. Where can people find this?
Where can people find BitcoinCore30?
BitcoinCore.org.
Okay.
Thanks, Shorts.

Speaker 1: 00:50:30

Thank Thanks for listening to Bitcoin Explained.
