---
title: "Nesting, ROAST, Half-Aggregation, Adaptor Signatures"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://podcasters.spotify.com/pod/show/chaincode/episodes/Pieter-Wuille-and-Tim-Ruffing---Nesting--ROAST--Half-Aggregation--Adaptor-Signatures-part-2-e1sdgjf
tags: ['adaptor-signatures']
speakers: ['Pieter Wuille', 'Tim Ruffing']
categories: ['podcast']
date: 2022-12-27
---
Speaker 0: 00:00:00

Just as

Speaker 1: 00:00:00

a warning, so don't do this at home.

Speaker 0: 00:00:01

Yes, of course.
Still have your friendly neighborhood cryptographer have a look at it.

Speaker 2: 00:00:16

This is the second half of the conversation with Tim and Peter.
If you have not listened to the first half, I'd suggest going back and listening to that episode.
We cover all sorts of fun things, including when to roll your own cryptography, why we prefer Schnorr signatures over ECDSA, Schnorr efficiency improvements, multi-sig, mu-sig, interactive versus non-interactive signing, Frost, and more.
So we're going to pick things back up, talking about nesting.
We'll cover roast, block-wide aggregation, adaptive signatures, atomic swaps.
This is a great conversation, and I hope you enjoyed as much as I enjoyed recording it.

## Nesting

Speaker 2: 00:00:50

So Frost sounds exciting, especially when used in combination with Music, there's this sort of idea for the future called nesting.
How could these ideas be combined?

Speaker 1: 00:01:11

Yeah, so again, like Music is an event setup and Frost is a T event setup, where you just require some subset, but now you can think of combining or nesting those in a three-style fashion.
For concreteness, again, maybe assume a Lightning Channel is my standard example.
Let's say I have a Lightning channel with Peter, I'm one participant, like Peter is on the other side.
And in this Lightning channel, we can have a two of two music.

Speaker 0: 00:01:41

You have a hardware wallet and whatever.

Speaker 1: 00:01:43

But on the top, it's a two of two music for the Lightning channel.
I mean, it's not supported by Lightning yet, but hopefully will be soon.
And then, but on my side, maybe for improved security, I could have a hardware wallet or three hardware wallets.
And then just on my side for this part of the music, for my key in the music, I want to have another threshold set up.
Like if two of my hardware wallets agree, then they can sign for just my part of the music.
So it's basically a two of two music at the top and on my side it's a two of three on that side of the tree.

Speaker 0: 00:02:20

Yeah, it's like a two of three and a single key.

Speaker 1: 00:02:25

Yeah, and you're on your side and now you can go a step further.
Like you shouldn't be even aware of the fact that I use a 2 of 3 under the hood.
First, because of privacy, maybe I just don't want to reveal it, but also just for simplicity, because the Lightning protocol spec shouldn't be concerned with what I do locally with my keys.
So I don't want to reveal that I use a two of three, not only for privacy reasons, but also to keep the specification simple because then whenever, like let's say in the future, I want to do something else with my keys for every new use case in a sense, or a key setup case, you would need to change the Lightning specification.
That's not what we want to do.
So this is the rough application idea of nesting.
In this example, it would be a frost inside the music, but you could also think of arbitrary combinations, like a music inside the music, music inside the frost, and arbitrary trees you

Speaker 0: 00:03:21

can build.
And in addition, we have other things too, like we have BIP32 derivation, like can you do a frost setup between participants and then get the next pub out that you can derive multiple keys from that all of them now may be signable.
We believe that's the case, but.
Yeah, and yeah.
Or do use that inside Taproot.
And this is kind of interesting because that's actually what we today expect people to do.
We don't actually have a security proof that a combination of those two is a secure thing.
We have a proof for Taproot signing, we have a proof for music signing.
We have very good reasons to assume that you can just combine the two, but.
Right, so this is like, there are

Speaker 1: 00:04:08

a few open research questions here.
So the first, like the thing you mentioned is just nesting that I talked about now.
So in fact, when we came up with music too, what we actually wanted to solve was this nesting thing, because we were thinking about nested music.
How can we have a music inside a music?
And it turned out the first round of the protocol was really annoying.
So I had this idea of, OK, how can we do nesting?
It involved getting rid of the first round of the protocol and this made it a two-round protocol.

Speaker 0: 00:04:40

It's kind of impressive that you kept thinking about it because you must have had the realization oh no, this first round is the problem and we know the proofs break without it.
Yeah,

Speaker 1: 00:04:53

I mean, I kept thinking about it for like every few months.
I spent a week on this and it was never successful until it was, so I was pretty happy about it.
But anyway, this is how this idea of having two rounds started.
And actually, like, Music 2 is designed with this use case in mind.
Just we didn't include it in the Music 2 paper because we first wanted to have the two-round scheme then, and nesting basically was out of scope of

Speaker 2: 00:05:20

the paper.

Speaker 1: 00:05:21

I just

Speaker 2: 00:05:21

want to double-click on that epiphany moment, because I've obviously never had one of those myself.
But as an engineer, sometimes you have the, I'm trying this thing, I'm trying this thing, I can't figure out an elegant way, and then it clicks.
Does it feel like that?
Or is it like, I'm throwing, like, sort of from a research perspective, like, I'm throwing a lot of different ideas at this thing, and trying to prove them out, and one of them clicks?

Speaker 1: 00:05:48

That's hard to say.
I think, like, usually, the way you get ideas is that you have problems in your mind and then you think about them and you think about them and you don't get a solution.
And then at some moment under the shower it suddenly makes click, right?
But it's really because you put the problems in your mind and you thought about them earlier.

Speaker 0: 00:06:09

It's interesting that here, like the goal was solving the nested music problem, maybe not even thinking about provable security, just wanting to make a scheme that could plausibly work with nesting.
And it turns out, oh, as a side effect, they came up with a two-round multi-signature scheme, which was novel, And it was like, whoa, wait, we should work on that first.
And I think that's interesting because you, as you say, like you're researching a problem, you have a particular problem in mind you're trying to solve, but maybe the solution is applicable to other things.

Speaker 1: 00:06:44

Yeah, and it's really, it says something about like how research should be done, right?
It's not like you have this one problem and now you lock yourself in a room for a month and then you come out and solve it.
No, it's like really you need to think about different problems, even if they're not exactly in your scope.
And then maybe at some point you realize, okay, now I knew that idea from that area.
I had a failed idea two weeks ago from that area.
Maybe now I can put them together and suddenly.

Speaker 2: 00:07:10

And so how do you sort of think about that applicability of those eureka moments to, for example, like to Frost.
So you sort of have something that's, you want to cut down on the interactivity of Frost.
You were sort of able to attack this kind of problem in music world.
Is it, is there a world where you can take those lessons and apply it to something that's totally novel?

Speaker 0: 00:07:34

I don't

Speaker 1: 00:07:34

know.
I think like research mostly is idea driven in one sense.
So you like you get some idea and then some neat trick maybe that you discover and then you try to find applications for that trick.
And then if you already know about problems in the space, it's more likely that you find an application where it's actually relevant.
That's basically how it works.

Speaker 0: 00:07:59

In a way, I think the same can be said about Music because its research was originally driven by this cross input signature aggregation thing but we sort of like wait no we have a really cool multi signature scheme and that's like well analyzed and much easier to think about and has like much more clear way to production than this other thing.
Let's focus on that

Speaker 1: 00:08:24

first.
Music too was built with this nesting idea in mind in the sense that, but we like we didn't include it in the paper, but we think we have a way to do it, but like, or we thought we have a way to do it now, like a month ago, we discovered it doesn't really work.
So it's still like an open research question.
It's not like, if you look at the scheme, you could think you could do it today, but please, please don't do it because it's still an open problem.
We have to think about it carefully, like maybe add some restrictions and then write a proper security proof for it.

Speaker 0: 00:08:55

When you say a way to do it that both encompasses like what the actual algorithm is but also how do we go about proving it?
Because today...
Security and functionality, yeah.
Right, because you like, Music 2 is specifically designed to support nesting, originally designed to support nesting.
So it, If you just look at the spec and do the naive thing, like it is a

Speaker 1: 00:09:20

natural thing you could do to make nesting work in a sense that like

Speaker 0: 00:09:26

you get valid signatures, right?

Speaker 1: 00:09:27

You can create a signature and the signature would verify but it doesn't mean that this specific way is secure and this is the problem we still need to solve.

Speaker 0: 00:09:35

While at the same time if you try to do the same thing with the three round music one either you'll conclude that you just can't make it work or you're gonna change the scheme in a way that will obviously and completely break it.
Yeah, yeah.

Speaker 1: 00:09:52

And this is what I was mentioning, this is really just only about the music inside music case, so not even talking about Frost inside music, which will probably...

Speaker 0: 00:10:01

Or with BEP32 on top or with Taproot on top or cross-input second iteration on top.

Speaker 1: 00:10:06

There's a lot of open problems here.
Also, with what you're mentioning now, basically, we have very well-defined security proofs for a lot of our schemes.
For example, for Music 2, in a specific setting, we know we're pretty confident that this is secure.
But now if we move to practice, we combine this with taproot tweaking.
Tweaking is really like offsetting the key a little bit.
And we use this, for example, in PIP 32, deterministic key derivation, we use it in taproot, we may use it in other schemes.
So it's really like, in practice, we put all those components together and there's really still a gap and there probably will always be a gap between what we have proven secure in theory and what we do in practice.
And I really hope we'll never get it wrong in practice, but I'm not entirely sure.
It can be really subtle.

Speaker 0: 00:10:58

It's interesting that I think if we would have come up with a new digital signature scheme, didn't write a paper about it, just like wrote a BIP up like BIP 340, I would have expected you know, whoa whoa whoa guys you are deploying a new signature scheme let's analyze this first.
Well at this somewhat higher level of combining things, it seems unnecessary to ask these questions.
And I think that that's a bit the same of like the lower level and the higher level there's more of an expectation to have an academically rigorous look at the lower cryptography part and less at like you know this security of composition.
I'm overgeneralizing obviously.

Speaker 1: 00:11:48

Yeah I mean if you say it's it seems unnecessary it sounds like the famous last words of the applied copter it works until it doesn't work but yeah

Speaker 0: 00:11:58

I mean I agree with you I don't mean to say we shouldn't ask this, I'm saying it seems that people are okay with the question not being asked.
Yes.

## ROAST

Speaker 2: 00:12:09

So, go back to Frost and your shower thoughts about making Frost more robust.
Like how did you approach that and what was the outcome?

Speaker 1: 00:12:20

Yeah, so you're obviously referring to ROSE, which is one of my recent academic works together with a lot of other people from, with Elliot who also works at Blockstream and with a few co-authors in Germany that I still know from university.
So the problem in Frost is, so first of all, it's nice because it has this two rounds property but one of the problems really is that it's not what we call robust.
And robustness is a very specific thing.
And it means that, let's say we have a two of three setup and we start a protocol with like all three people, but only two of them are actually willing to sign, which is okay, right?
Because we only need two to produce a signature.
But maybe that other guy, the third guy, is actively trying to disrupt the protocol, maybe because it could be malicious, it could be just offline, just not actively, of course, but of course covered by also active.
So if you can prevent against active attacks, you can also prevent it against just being offline.
So we start the protocol with maybe three people and at some point we need to commit to a specific subset.
We need to say after the first round, OK, now let's finish the protocol with exactly those two signers.
And now either we pick the right signers, and they are online, and they're actually willing to sign the message, then everything is right.
But if you pick the wrong two signers, then basically the protocol gets stuck and there's nothing we can do except restarting and picking another group of signers.
And this is a fundamental trade-off that Frost made in a sense, because if you look at cryptographic literature, the academic literature, there have been papers like pretty like decades old that essentially solved this problem of robustness but like they're the signature schemes or the signing schemes are pretty complicated.
So as I said, Frost has two rounds, and this makes it very, very nice.
And I think the best known scheme in the literature that we have known so far requires seven rounds, even in the best case.
So even if there's no attack at all, you would require seven rounds of communication.
And now, okay, this is, like, if you look at the paper, like with my academic head on, that's, Yeah, you could do it.
Like if you ask Peter as an engineer, it's like, I know you.
What, seven rounds?
Seven rounds, it's crazy, right?
They wouldn't do this.
Yeah.
ROSE kind of is, so yeah, what the first people did is like they realized that the reason why those old protocols, they're so complicated is that they have robustness built in.
So basically the main idea of, I shouldn't say this because like I also had this nice idea of having a two-round scheme, but one of the main design decisions in Frost was basically, okay, just get rid of this robustness property, and then suddenly everything becomes much simpler.
And Roast is now an idea to add robustness again to Frost, but in a really different manner.
The idea of Roast is really like it starts FROST sessions in a clever way.
So I mentioned that when you run a FROST session, it might happen that you pick the wrong subset of signers and then the protocol will get stuck.
And ROST doesn't actually fix this directly, but Roast now is a clever way of starting a new session of the protocol, such that in the end, you know that you only start at most like a linear number of sessions.
I think you need, like if n and t are the parameters, you need like N minus T plus one sessions at most.
And this is a way where you can, in some sense, get the best of both worlds in the sense that if everyone is online and willing to sign, then like your first first session that you would start would complete and you get this nice two round property.
But if you are under attack or maybe some of the signers is offline or some of the signers are offline, then you spend a few more rounds, but you can still run the, like get the signature within a reasonable amount of time.
This is the main idea of Roast, or the main thing it achieves.

Speaker 2: 00:16:38

And so, in terms of applicability of both Frost and Roast, where are these things being deployed?
Where are they being used?
What are the applications you imagine?

Speaker 1: 00:16:48

Peter has already mentioned that Frost already is maybe more like a niche thing than music because it's really only helpful when you really specifically need the threshold property.
And then if you add ROST on top of it, I think like ROST is really helpful in settings where you not only need specifically the threshold property, but where you also need a large threshold setup.
Like At Blockstream, we have this liquid sidechain, which is run by a federation and currently has an 11 out of 15 setup.
This is already a little bit larger than what you probably do at home, I guess.
And ROST really makes sense, and also frost really makes sense if you scale up to larger parameters.
If you have large N and large T and 11 or 15 is maybe, yeah, it's larger than 2 or 3, but it could be maybe like 50 of 100 or 60 of 100.
And this is doable with frost and roast with this specific combination.
So, and I think this is where it's going to be used.
It's probably roast is nothing that you would use in your two or three at home, or even like

Speaker 0: 00:17:54

a three or five at home or something like that.
But maybe because for your two of three, you really just don't want to use a threshold signature scheme in the first place.
That's why

Speaker 1: 00:18:02

I mentioned also 305.
Like even let's say you have a 305 at home, I guess you wouldn't need Roast because it's like, okay, like I picked those three hardware wallets to make a signature or some of it failed, what like, yeah, replace the one that failed with another one and try again.
You could do this restarting of Frost sessions basically manually.
So Roast really I think is helpful when you have some federation of nodes around the world that are running automatically.
They're supposed to produce a signature every one minute or every 10 minutes, and then you need the automatic way of making sure that they really can produce a signature.
I think this is where ROS is strong.
But it's good for these federation use cases, but I think this is really like a niche case in a sense.

## Cross-input Signature Aggregation

Speaker 2: 00:18:49

So Peter, you have mentioned cross-input aggregation as the inspiration for a lot of the work that actually has been done to date.
Let's talk about signature aggregation, maybe start with interactive floor aggregation and sort of the cross-input aggregation history, and then we'll

Speaker 0: 00:19:10

explore some other ways.
Let's first say what signature aggregation is.
It's very closely related to a multi-signature.
But the difference is really, think of a multi-signature with multiple participants each signing, but they can all be signing a different message rather than signing all different, allow all messages to be different rather than the same.
Now signature aggregation can be done interactively or non-interactively, which refers to the rounds of interaction at signing time.
Is it possible for them to just create their partial signature now once, their individual one, and can a third party aggregate them, or do they really need to collaborate in order to produce that signature?
Now if we're restricting ourselves to interactive ones, which is certainly the easier thing to build, there is a trivial way of turning any multi-signature scheme into an aggregated signature scheme, namely, everyone just signs everybody's message.
Because it's interactive, they're talking anyway, like effectively the message could be like, here are all the messages and all the signers.
Yeah, you just take

Speaker 1: 00:20:27

all the individual messages, concatenate them, this forms the message you put into the multi-signature scheme.

Speaker 0: 00:20:32

Or you say the message is key one signs message this, key two signs message that, key three signs message that, and everybody signs that.
That makes an interactive aggregate signature scheme, like just take a multi-signature scheme and turn into that and you're there.

Speaker 1: 00:20:49

That is...
Modulo some subtle details.
Yeah, let's not go into that.
But just as a warning, so don't do this at home.

Speaker 0: 00:20:56

Yes, of course.
Don't

Speaker 1: 00:20:57

phone your crypt, I'm so sorry.

Speaker 0: 00:20:59

Still have your friendly neighborhood cryptographer have a look at it.

Speaker 2: 00:21:04

Before you move on, that's just because of being able to actually tease out like private keys based on reused nonces or like what's the, what is the actual issue that you'd be most concerned.
If I did that, what would be the first mistake I would make?

Speaker 0: 00:21:21

In the music paper, I remember Russell O'Connor came up with this fairly far-fetched attack of, if you just do that, what I just said, and try to use that specifically in the context of Bitcoin transactions with one signature there was a problem but I don't remember there could be a problem if you're a single party and you have like you have multiple messages that you want to sign.
You can be tricked into, and you participate multiple times, you can be tricked into signing the same one instead of different ones.

Speaker 1: 00:21:58

It's like you could be tricked into, I think, signing your message twice instead of only once.
And it's not even clear if that is a problem, but I really may not remember the details.
And if you're interested, look at the Music One paper, there's an appendix that exactly specifies the attack and the problems.

Speaker 0: 00:22:15

But yeah, it's...
Because this was sort of folklore knowledge of like, you can build an IAS out of a multi-signature scheme.
Here's a way of doing that.
And that paper was like, maybe don't do just that, because...

Speaker 1: 00:22:30

Apparently, like if you have a simple idea and it looks obviously correct and you try to secure and you try to really prove it secure, it can turn out that there are actually some subtle problems with it.

Speaker 0: 00:22:43

Interactive aggregate signature scheme, we now know how to do that.
So we can take music one, music two, those can be turned into an aggregate signature scheme if needed.
And so that is something that could be used for say cross-input aggregation, but only under the condition that all the input signers are collaborating.
And usually that is the case, usually there's just one party involved, but say in a coin join transaction there are multiple participants, so if such a scheme were to be deployed and you have a CoinJoin then of course CoinJoins are at the same time the strongest motivation for wanting something like cross-input signature aggregation, I think.
Because think about it this way, every input in a Bitcoin transaction today has one signature.
In sort of a music, taproot world, they will in fact all have exactly one signature.
That signature takes up some block space.
But if we were to be using a cross-input signature aggregation scheme, there would just be one signature for the whole transaction.
So that's a cost savings.
And it is a cost savings that, I shouldn't call it a coin join, but like a pay join, where like, A wants to pay B and C wants to pay D, they can join these two transactions into A and B, sorry, A and C, pay B and D.
And interestingly, in a cross-input signature aggregation world, this aggregate transaction would be smaller than the sum of the individual ones because there's only one signature rather than two.

Speaker 2: 00:24:31

So there's this economic motivation in.

Speaker 0: 00:24:33

No, that economic motivation is small.
It's partially due to the fact that SegWit introduced a discount for witnesses, so those signature are already relatively inexpensive.
They also have a relatively low cost on the ecosystem, but this makes the, you know, differential between the two fairly small.
So it isn't a like, wow, this is going to incentivize everyone to start merging their transactions.
But it is a nice thing in the sense of like it gives a potential justification, like, hi, I regulator, why are you merging your transactions?
Being able to say, well, it's cheaper is a much better justification than like, whoo.

Speaker 2: 00:25:23

Makes sense.

Speaker 0: 00:25:23

So that's interactive aggregation.
It has complications.
All aggregate signature schemes that we want to do across more than individual inputs, like need consensus rules to work with them.
In the same sense that like, you know, as explained, like in a way there's a relation with batch validation, where in batch validation we're thinking of, well, you first run all the scripts, pretend all the signatures succeed, but keep a list of all signature checks that have to be done, and now we do all those signature checks at the end.
In a cross-input signature aggregation world, it would be exactly the same, except there is now just a single signature provided rather than multiple signatures.
And even technically, these schemes are very similar, so that the math that's used for both is comparable except of course in one case you have multiple signatures that need to be merged together versus just one.

Speaker 1: 00:26:29

So Another reason to see why this requires a consensus change is really like what consensus supports now is strong signature verification.
This is really like an algorithm that takes a single public key, a single message transaction and a single signature.
And really like The primitive we are talking about here, the verification side of it would take multiple public keys, multiple messages, where they all could be the same transaction but like a little bit different, okay?
But only one signature.
So really this is a different interface already.
Like you couldn't just do this with the current Schnorr verification algorithm that we have in consensus code right now.

Speaker 0: 00:27:07

And I think a more fundamental reason, like today you cannot spend any input without a signature, assume it has a public key.
Like that would be a problem if you could spend an input without a signature.
Yet, if we go to a cross input signature aggregation world, a transaction with two inputs, well, there's only going to be one signature.
That means there's at least one input without a signature.
Of course, the idea is that signature will cover all of them simultaneously, but the rules cannot think about that.
Any kind of cross-input aggregation scheme is going to require an additional consensus soft fork rule.

Speaker 2: 00:27:49

The community didn't feel like it was worth waiting to more fully bake cross input?

Speaker 0: 00:27:54

Yeah, I think, so when the discussions around tap roots, which North Signature started, there were a whole lot of ideas and many of them were actively being discussed because there were like improvements to taproot, there was graftroot, there was groot, and so forth.
And how those would interact with signature aggregation is kind of unclear because there is a complication here is soft fork compatibility.
So we want the property obviously that a change that introduces cross input aggregation is a soft fork And also that things that could be built on top, extensions to the script language later, are a soft fork with respect to signature aggregation already existing.
And so this isn't a fundamental problem, but it's kind of annoying.
Say, imagine there's an opcode change that introduces something like an opif, just something that changes the execution path through a single script.
You need to make sure that old nodes and new nodes agree on what signatures are being aggregated, even though some of them may execute the checksig that's being skipped and others that don't.
So if you think about it, it's non-trivial.
Like one possibility is doing like, well, whenever a soft fork is introduced that changes which codes are executed, you create a new separate batch for aggregated signatures like you just do the aggregated signatures that are according to the pre-soft fork nodes and then everything that's added or changed with respect to that, they go into a new bucket and you end up with two signatures, one for all the signatures, or one aggregated signatures for all the things visible to old nodes and then another one for the additional ones that are visible to new nodes.
That's one idea.
Another one, one that I'm I think more in favor of, is so Taproot has this internal key, which is like the special elevated key which we believe to be the everyone agrees situation.

Speaker 2: 00:30:18

Right, the common path.

Speaker 0: 00:30:20

Common path.
And that one involves no scripts at all.
Like the taproot consensus rules say you can spend a taproot output by just giving a signature on the, not the internal key, but on the tweaked key, and there are no scripts involved.
So all the complexities about compatibility in script just don't exist.
We could work on a system with cross-input aggregation that just does aggregation of signatures on the key path spans.
And this disappears, it means it isn't as efficient as it could be because you don't get the aggregation for signatures occurring in scripts.
But we do believe that that's actually the exceptional case, not the most common one.
So that gives most of the benefits with small amounts of work.
And why we didn't include this is just there were too many ideas at a time.
Those have mostly died out, I think.

Speaker 1: 00:31:17

But also on the cryptography side still.
So you said like you gave this trivial way or a naive way of creating a signature aggregation scheme from a multi-signature scheme.
And now we have multi-signature schemes and you said like the math will be pretty similar but it's actually, if you look at the specifics of this, you probably wouldn't want to use something based on, let's say, music, or music two, or music one,

Speaker 0: 00:31:45

and any of these.
Because they're kind of overkill for...

Speaker 1: 00:31:49

Kind of overkill, yeah.
What you actually need is a little bit weaker.
And also there are other issues when it comes to compatibility with batch verification or with batch validation.
One way to think about this is really like in a signature aggregation scheme, it's a little bit like a multi-signature scheme, but as you said, like the verifier will do the key aggregation because the verifier gets all the individual public keys and somehow would need to aggregate those keys.
And if we do this in a music style, this key aggregation, then this key aggregation again is an elliptic curve computation, but we couldn't add this to the batch for doing batch validation.
So we couldn't batch it together with a signature validation or with a taproot commitment openings.
So probably there are other signature aggregation schemes that more different from music that would actually allow for fetch validation.
So yeah, really, it's like, as you say, like you could construct it basically from music, but music is overkill.
And that's the reason not to

Speaker 0: 00:33:00

do that.
The Belaraneva scheme is simpler and would work.

Speaker 1: 00:33:05

Yeah, the scheme we have in mind is really closer to Bellara Neve.

Speaker 0: 00:33:08

And I think that's an interesting discussion about trade-offs because clearly when we're talking about taking some cryptographic scheme and building it into Bitcoin's consensus rules, that is I think a higher bar to meet than we're going to introduce Schnorr verification in the consensus rule, knowing that there are lots of things that could be built on top, but they don't actually become part of the consensus rule.
Like music you can use today, consensus rules know nothing about it.
That is not true for the signature aggregation.
The consensus needs to know about it.
So I think there's a higher bar in like, well, even if we have agreement on how and whether to do it, what scheme specifically do we pick?

Speaker 1: 00:33:59

Also when it comes to cryptographic assumptions, right?
Like all provable security and cryptography is always relative to some hard problem.
I mean I mentioned like we can prove Schnorr signature secure if you assume that discrete logarithm problem is hard and some other side-side conditions.
And also like for example I mentioned, Bilal Ranevinsky differs from music in terms of what do we actually need to assume as a hard problem.
And this is another question that becomes much more relevant now that you try to bake this into Bitcoin consensus.

## Half-aggregation

Speaker 2: 00:34:32

And then there's half aggregation, which is different.
How so?

Speaker 1: 00:34:37

Like what we talked about so far is what we also call full aggregation.
And it's, we call it full aggregation because if you have ends, in a sense, like you have N parties, they all have their public keys, they all have their messages or their transactions, and the resulting signature you aggregate is really just, it looks like one, or it has the size of one signature.
So it's really like you compress it to, like you have n parties involved, n

Speaker 0: 00:35:04

messages involved.
Let's give numbers, like a Schnorr signature today, 64 bytes.
Without aggregation, if you have n signatures, it's 64 times n bytes.
With full aggregation, it's 64 bytes, regardless of how many signatures you have.
With half aggregation, it becomes 32 plus 32 times N.
So literally half of the signature becomes independent of N and half of it remains.

Speaker 1: 00:35:30

Or in other words, like if N grows, like the savings will tend to a half of the size.

Speaker 0: 00:35:38

Yeah, asymptotically, full aggregation is constant, no aggregation is 64 times n, half aggregation is 32 times n.

Speaker 1: 00:35:48

And so you get less savings, but the advantage really now is that half aggregation is non-interactive.
And it's actually a public operation.
It really means like I have two Schnorr signatures or ten or whatever, I know nothing about the secret keys of those Schnorr signatures.
So these are not signatures that I have generated.

Speaker 0: 00:36:10

You're not a participant.

Speaker 1: 00:36:12

I'm not a participant, I just received some signatures.
And now I can do this aggregation or compression operation.
I can compress them into a half-aggregated signature that is now smaller than the size of the sum of the individual signatures, but still is verifiable against all the messages and public keys.

Speaker 0: 00:36:33

So you need to know all the public keys, all the messages and all the signatures?

Speaker 1: 00:36:37

That's the same as in full aggregation.
So both of these are really compression mechanisms in a sense.
And with half aggregation we get less savings in the space and compression, but really the advantage is that now this is a non-interactive public process.
You just get some signatures and everybody can compress them.

Speaker 0: 00:36:54

And so this means that at a transaction level, this is easier to do because the participants don't need to interact with each other.
It would still require a consensus change, to be clear.
This doesn't affect any of that.
It requires a soft fork to add cross-input half-aggregation as well.
But at the signing side, it is simpler because say for a coin join, the individual signers now don't need to interact with each other.
They can just produce their individual signatures and whoever is coordinating the creation of the coin join or really any participant at all can just take all the signatures, put them together, and have a signature that can go on chain.
But that's not everything.
In fact, because it is non-interactive, there's no reason to stop at the transaction level.
And this can be done at the block level too.
It would be the miner in that case, or whoever is assembling the block that would take all the signatures in the individual transactions but combine them into a single block wide signature for everything.
So that is a 32 bytes per signature over the whole block that disappears.

Speaker 1: 00:38:08

It is of course would be yeah the savings would be huge and that's why it is a very interesting idea but like because it's really like not it's crossing transaction borders like

Speaker 0: 00:38:20

the issues it could create potentially are...
So for example, what this would mean like pre-SegWit, this would have been a huge problem because it would mean the miner is changing the transaction IDs. That's thankfully no longer the case with SegWit, but it's still the case, like we have this WTX ID, which is the witness transaction ID, which is a hash of all the data in the transaction together with it witnesses, the version that ends up in a block would have a different WTXID than the version that's relayed on the network.
So these aren't fundamental problems, but there are some engineering challenges for like caching and nodes will validate signatures as they come in individual transactions and cache the results.
Now they see a different version of that transaction in the block because that half thing is stripped out.
Is there a way to leverage the cash they have or do they need to recompute from scratch?

Speaker 1: 00:39:21

One maybe more fundamental problem which is still open or we should really look

Speaker 0: 00:39:28

at it is how this interacts with adapter signatures.

## Adaptor signatures and atomic swaps

Speaker 0: 00:39:32

So adapter signature is another advanced signature technology which for example allows you to do atomic swaps on the chain that just look like two normal transactions.
So if you look at the blockchain again you see only two schno signatures and it looks like just two more normal transactions.
What actually happened is an atomic swap and basically the way how they work is that we set up our keys in a special way and then I send you a coin and because I have to sign this transaction I have to publish my signature on the blockchain.
You look at the signature and take information out of it and this now allows you to...
Yeah, so the idea is both parties lock up their coins in a two-of-two music or any kind of aggregates.
So both with a taproot path that like after some time they can take their coins back because you don't wanna log them forever if one of them steps away.
And now one of them gives a signature to spend one of those to the other, but sort of in a damaged way.
You don't give the real signature yet, you give a signature and you sort of add an error term to it, and you do that for both.
So you say I produce two, the two transactions, one that takes my money and gives it to you, the other that takes your money and gives it to me.
I sign them both, or my side of it, but in a damaged way.
And now when I publish the real signature, you can look at the difference between, you can learn the error term by looking at the real signature and the other one I've given you, apply the error term to the other thing and take your coin.

Speaker 2: 00:41:12

But this could be done on ECDSA as well.

Speaker 0: 00:41:14

Yeah, yeah.
It can be, yes.
It can

Speaker 1: 00:41:16

be, yeah.

Speaker 2: 00:41:17

So, I know Alex Bosworth has been talking about this, I don't know, for four or five years, but what is the interaction between half aggregation and removing that property from Schnorr?

Speaker 1: 00:41:27

The way it, the idea of this atomic swap protocol is really that like we have two transactions and we want to make them atomic.
Either both of them happen or none of them happens.
The idea is really that we create our keys in such a way that if one of the transactions happens, then you're forced to publish the signature of this transaction on the blockchain and then this enables the other party to look at the signature, extract information from it and make the other transaction happen.
And half aggregation, like If now this signature that's published on the blockchain would be half aggregated, then it's not the full signature that would be published there.
We would exactly remove that part that you need to look at to make the second transaction happen.
So this is how this would interfere.
And now, as you say, it could actually be done with ECSA.
So one very simple, of course not very satisfactory solution would be, okay, like, if you want to run an adapter signature protocol, then resort to ESA signatures.
So one, maybe a little bit more clever approach would be, okay, like you, you could do it with Schnorr signatures but maybe have a marker in your transaction that says okay like this could be aggregated or this could not be aggregated.
Of course this...

Speaker 0: 00:42:39

That's unfortunate because now you're revealing to the chain that like this is really a data carrying signature and...

Speaker 1: 00:42:47

This is not good for privacy obviously.

Speaker 0: 00:42:49

And of course adapter signatures are an alternative to say, HTLCs, which are used for exactly the same purpose today, except they reveal hash per image, rather than using the signature itself as the data channel.
So if we're going to, you know, oh, adapter signatures, yay, they're all indistinguishable now.
And now with half aggregation, Oh, wait, we need to add a marker to it to say it can be aggregated.
We're again saying there's a data carrying here.
Like how much is that better than just using the HTLCs?

Speaker 1: 00:43:25

For example, one idea in that direction is basically very similar to what you said for full aggregation.
So maybe try to restrict this to taproot key spends, in a sense, that only signatures for those can be half aggregated.
And maybe this is enough to make sure that you can still run your...

Speaker 0: 00:43:47

Unfortunately, it isn't, because the whole point of an adapter signature is that you would use it for the internal for the keypath spend.

Speaker 1: 00:43:55

Yes but I mean you could say like okay aggregate only the other ones and then I think...
Only aggregate the script ones?
No no only aggregate the keypath ones And I looked at this with Jonas and I think we, like we could normal just the atomic swap protocol, we could make it work with that restriction.
And it's kind of an open question at the moment, like if this would cover all applications of adapter signatures, because like if this restriction is enough to not interfere with adapter signatures, then this would be one way to maybe to move forward in the future but it's kind of an open problem.

Speaker 2: 00:44:33

Would this be considered a block size increase in the same way that SegWit was considered a block size increase?

Speaker 0: 00:44:39

I don't think so because it is, unless you think of Taproot, does a block size increase too?
I mean it's more efficient use of the existing space and thereby it's a capacity increase.
But I think SegWit is pretty different because it's actually adding more bandwidth.

Speaker 1: 00:45:00

I agree with that view, but there's one point you can make about verification time.
So the time you need to validate a half-aggregated signature, which basically is, let's say, the combination of 100 signatures, the space it needs is smaller, but the time you need to validate it is still almost the same as for 100 individual signatures.
So in that sense, now if you use block space more efficiently, you can squeeze more signatures in the block, And this then requires in the worst case more, or you could say in the best case, rather than the most complex case, you could have more signatures in there and then this would require more verification time.
So in that sense, it's not a block size increase, but it's a block verification time increase.

Speaker 0: 00:45:48

Yeah, it's just like today there will be at least 64 bytes for every signature check being done.
And with half aggregation, maybe that's the same cost can be per 32 bytes.
The way that taproot rules already work, they actually require 50 bytes of witness data for every signature check being done.
So if that rule is maintained, but maybe that rule shouldn't, that rule doesn't really make much sense.
And yeah, I mean,

Speaker 1: 00:46:18

No, but I tend to agree.
Like Usually bandwidth constraints are much more important than verification time constraints.
Spending a little bit more verification time, I'm guessing you're right, but I guess it's more acceptable than maybe increasing the actual block size, the actual data that you need to send around.

Speaker 2: 00:46:35

We've been talking a while about a lot of different things.
Where do you see this all headed?
How do you see these things starting to gel and combine together?

Speaker 0: 00:46:43

We've been talking a lot about the provable security of these schemes.
And that is obviously one impediment for some combinations we have more confidence about than others.
I'd say like the nesting question is much harder than some other questions and so forth.
But there is another question too, and that is standardizing all these things and integration in parts of the ecosystem because just having the consensus rules that are compatible with it and a spec or a scheme or a paper that says you can do half aggregated adapter signatures, blah, blah, blah, isn't enough.
There's a need for how do we make things use them and interact with using them.
And so, music 2 for that now, which is making great progress, that's not the end of the story, right?
We will need probably how to integrate it in descriptors, how to integrate it in PSBT.
That will raise questions of how does it combine with BIP32 derivation because everyone derives their keys that way and there are obvious and less obvious ways that they can interact, we'll probably want to specify that.
And I think for music, too, that is fairly close.
For frost, that is further away.
Nesting is even further away.

Speaker 1: 00:48:15

So is aggregation.

Speaker 0: 00:48:16

So is aggregation.
So it's not just a pipeline because it's multidimensional and it doesn't move forward at the same speed and on every aspect.
But the whole provable security aspect is just one part and we shouldn't forget about the rest because multisig in Bitcoin, the threshold multisig naive thing, P2SH in 2012 was introduced for specifically that purpose because there was no address scheme to do multisig at the time.
It took years before anyone used it because we really had no good way of making multi-sig convenient.
And by convenient, I don't even mean user convenient, but like developer convenient.
How do you develop an application that uses this and wants to interact with others.
And these are all very hard questions of a very different nature that also matter.

Speaker 1: 00:49:07

I agree, yeah, and we haven't really touched upon the status of the specifications.
I think like the music 2 pip, as you're saying, It's in a good shape, I think.
But of course, like we need implementations there.
Like for Frost, it's a little bit further away.
And yeah, I agree.
Basically, just basically I'm summarizing, right?
So the rest is really further down the road.
And maybe like you're talking about this now, maybe in two years we realize, okay, like there's a much better way to introduce aggregation to the ecosystem or it's a stupid idea or I don't know.

Speaker 0: 00:49:38

You're like, adapter signatures are everywhere today and I'd love that.

Speaker 2: 00:49:46

So that's a world we all want to be living in.
Anything else on your mind?
So we've had a somewhat scoped discussion about, I wouldn't say it's particularly well scoped, but it's been scoped somewhat, talking about Schnorr, and then Muldy signatures, and threshold signatures, and Frost.
But like, let's imagine we had another two hours to sit down.
What would be other things that are on your mind that you're thinking about, that you're excited about?

Speaker 1: 00:50:12

I mean, in terms of, I'm not really thinking about it, but like, one thing that always comes up, and I really would need another two hours, and I have to be careful not to go deep here, but it's really the question, okay, can we do anything at all about post-quantum security, like if there's a quantum attacker maybe.
To be honest, I don't even think there's a lot we can do, but we should at least...
Today.
Today, but we should at least keep thinking about this.
This is a question that I often get.

Speaker 0: 00:50:45

It's a good one.

Speaker 2: 00:50:47

Well, thank you both for giving us almost two hours and I will say it's been a pleasure to watch you both escape to different rooms and draw indecipherable things on whiteboards.
So thanks for coming in Tim, spending the week with us.

Speaker 0: 00:51:05

All right, what did you think about that conversation?

Speaker 2: 00:51:08

I thought it was great.
Not to toot my own horn, but I thought it was a great chance to pull a lot of info out of those two.
And I think the conversation about diving into the advanced signing protocols and multi-sigs versus threshold signatures and state of frost and roast and mu-sig2, I thought that was all really fun.
But thinking about taking advantage of batch verification and signature aggregation and its future, I thought was really quite great.
We talked about signature aggregation and the interest in that with Josie a couple episodes ago, but it gave me a chance to actually better understand it.

Speaker 0: 00:51:43

Right.
What you mentioned now was that you also thought it was interesting to see how the sausages made it a little more.
Yeah.
About when to roll crypto.

Speaker 2: 00:51:53

Well, I just like the conversation about them referring to Music One as broken and just like being very upfront and public about the fact that it's broken and the upgrades that they made and sort of like the shower thoughts that Tim had to make Music 2 work and all those things.
It's, I think it's, it's fun.
So yeah, I hope you enjoyed listening to the episode as much as I enjoyed it.

Speaker 0: 00:52:15

Yeah, well, we hope to have one soon for you again.

Speaker 2: 00:52:18

I don't know, I don't know if we're gonna make it before our New Year's, but if not, hope you enjoy the holidays and Happy New Year's, and if so, we'll talk to you before then.

Speaker 0: 00:52:27

Bye.
Bye.
