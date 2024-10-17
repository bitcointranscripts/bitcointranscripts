---
title: Schnorr, MuSig, FROST and more
transcript_by: sagungargs15 via review.btctranscripts.com
media: https://podcasters.spotify.com/pod/show/chaincode/episodes/Pieter-Wuille-and-Tim-Ruffing--Schnorr--MuSig--FROST-and-more---Episode-26-e1sav0l
date: '2022-12-16'
tags:
  - cryptography
  - musig
  - schnorr-signatures
  - cisa
  - threshold-signature
  - libsecp256k1
  - taproot
speakers:
  - Pieter Wuille
  - Tim Ruffing
summary: Pieter Wuille and Tim Ruffing treat us to a conversation about Schnorr, multisignatures, MuSig, and more. We covered a lot so this is part one of a two part conversation.
episode: 26
additional_resources:
  - title: MuSig
    url: https://bitcoinops.org/en/topics/musig/
  - title: Yannick Seurin
    url: http://yannickseurin.free.fr/
  - title: Bellare-Neven
    url: https://btctranscripts.com/bitcoin-core-dev-tech/2018-03-05-bellare-neven/
  - title: FROST
    url: https://eprint.iacr.org/2020/852.pdf
aliases:
  - /chaincode-labs/chaincode-podcast/schnorr-musig-frost-and-more/
---
## Introduction

Mark Erhart: 00:00:00

This goes to like this idea of like really only using the blockchain to settle disagreements.
Like as long as everyone agrees with all we have to say to the blockchain, it's like, yeah, you don't really need to know what the rules were.
Hey Jonas, good to be back.

Adam Jonas: 00:00:19

So while you were out being the Bitcoin ambassador that we depended on you to be, I was here stuck in the cold talking to Tim and Pieter and I thought it was a good conversation.
Yeah.
I don't think I let you down too much.

Mark Erhart: 00:00:32

I'm looking forward to hearing it.
I hear that you went over a lot of stuff.

Adam Jonas: 00:00:37

We did.
We covered updates about [FROST](https://eprint.iacr.org/2020/852.pdf) and [Roast](https://eprint.iacr.org/2022/550.pdf), [MuSig2](https://eprint.iacr.org/2020/1261).

We talked about ideas that are a little further out in terms of batch verification, signature aggregation, interactive full aggregation, [cross-input signature aggregation](https://btctranscripts.com/tags/cisa/).

Mark Erhart: 00:00:54

So everything, like everything that pertains to Taproot and since then?

Adam Jonas: 00:00:58

Yeah, but It only took two hours.

Mark Erhart: 00:01:01

That sounds like a hefty episode.

Adam Jonas: 0: 00:01:02

That's all it takes.

Adam Jonas : 00:01:05

Yeah, no, I really enjoyed the conversation and was even able to follow it.
Anyway, hope you enjoyed listening.
♪♪ Welcome, [Tim](https://x.com/real_or_random) and [Pieter](https://x.com/pwuille).
Very excited to have you.
Unfortunately, [Murch](https://x.com/murchandamus) is not here to help me.
I could really use this help today, but this is what we've got.
So we're going to dive right in.
And the first question is for both([Pieter Wuille](https://x.com/pwuille), [Tim Ruffing](https://x.com/real_or_random)) of you, When do you need to roll your own crypto?

## When to roll your own cryptography

Adam Jonas: 00:01:33

This is something that we're not supposed to be doing, but you two have a long history of doing it, so why, when?

Pieter Wuille: 00:01:41

This is good advice, but it's a guideline, not a rule.
Very clearly, there are some people in the world who need to be rolling their own cryptography or we wouldn't have any.
I think it's more an understanding that like you need to be aware of your own limitations and you know there's a saying of like everybody smart enough to come up with a scheme, they can't break themselves.
But that doesn't mean nobody else can.
So I think it's more advice about you should be aware of what level you're targeting.
Are you experimenting?
Are you learning?
Are you talking about actually deploying something in production at what scale, at what level?
And there are different, you know, look at feedback, know who to ask, know that there are lots of smart people out there.

Tim Ruffing: 00:02:34

That's a pretty good answer actually.
The exact same saying came to my mind when you asked the question.
But yeah, it's like, of course, I mean, I also heard this rule, for example, when I took a cryptography course at university and they told us, okay, this is how the stuff works, but don't do it.
And it's like very unsatisfactory, right?
Because it feels like, okay, but where else should I learn this?
I mean, if I learned this at university...

Pieter Wuille: 00:03:03

You're supposed to be the expert.

Tim Ruffing: 00:03:05

I mean, yeah, but I mean, this was just some undergrad course, right?
Of course, it's different after you completed the PhD, maybe, but at some point, I guess you get the feeling of when you are at the point when you can do it.
And of course, yeah, get feedback, talk to other people and talk to.

Pieter Wuille: 00:03:20

And it's more a learning what level of assurance you need to get from others and not just a, okay, now I am confident enough to judge my own constructions.

Adam Jonas: 00:03:34

There just seems to be a different skill set though, in terms of understanding and or being able to break schemes and having the creativity or sort of the foresight to put schemes together.

## Different levels of cryptography 

Tim Ruffing: 00:03:45

It's very related, but yeah, it's a kind of different skill set.
I mean, it depends.
When I think about a new idea for cryptography scheme, it's like, of course, I try to break it, like think like an attacker, but I'm also, because I'm a cryptographer, I also try to think about how would I prove it's secure already.
So it's approaching it from both sides in a sense.
But I think there's another aspect to that discussion.
I think there's also different levels of cryptography in the sense of closer to implementation or closer to research.
And even on this level, you could say, I mean, I know people who I would totally trust to do a security proof, but I wouldn't trust them to write code.
And I guess the opposite is also true.

## Security Engineering vs Cryptography

Pieter Wuille: 00:04:32

Yeah, and I think even expectations around this differ, because if you go up this ladder from very theoretical, low-level ideas to closer to real worlds, There is some threshold where people stop calling it cryptography, where it becomes security engineering or something like that.
And that boundary is essentially arbitrary.
Because things may go wrong just as well at the higher levels as in the lower levels and in fact in practice they more often break at higher levels.
Maybe precisely because there is less of an academic expectation to like it is much more It feels much more acceptable for people to like, okay, I'm gonna build some software that uses some encryption and hashes and off-the-shelf building blocks together and think these building blocks are secure because they come from good cryptography.
I can arbitrarily put them together and build a system.
And these things sometimes break because the manner in which you compose them matters.

Tim Ruffing: 00:05:44

Yeah, and also it's really what you said.
I mean, security is hard because you have to get it right on every level.
And it really doesn't matter on which level you screw up.
In the end, you get an attack.

##  Quality of Feedback and Review from Peers in Cryptography

Adam Jonas: 00:05:55

So you said early that paying attention to feedback from others is really important.
And so What is the interaction between the work that you do on Bitcoin and the wider applied cryptography community?

Tim Ruffing: 00:06:08

It kind of depends again on what the concrete thing is.
But I guess a lot of work that I recently did was, I mean, I come basically from an academic background, right?
I have a PhD in computer science with a focus on cryptography.
So it's pretty standard and it should be the case like if that if you come up with a new cryptographic construction, you write it up in a proper paper, you try to get it published, which means you collect feedback from other researchers.
They hopefully look at it, they hopefully look at your arguments, at your security proofs.

Pieter Wuille: 00:06:41

They may point you at related work you were completely unaware of.

Tim Ruffing: 00:06:45

Totally, yeah.
This kind of feedback is very helpful.
But then again, if it comes to specific details of implementations, then this may stuff you couldn't send to other cryptographers.
I mean, of course you could send it, but there's nothing you would write up in a paper or get feedback from the academic community.
So this is more like a different set of people, I'd say, that you now would ask and get feedback on.

Adam Jonas: 00:07:12

Yeah, I guess not being in the academic community and not being an implementer of cryptography myself, it just sort of seems like cryptography is one of those areas where academia and implementation is actually closer together than other areas of Bitcoin.
There seems to be this sort of like at least arm lengths relationship in other parts, and possibly even bordering on disdain for like outsiders not properly understanding the system and like not like understanding the real research problems and the applicability.
But cryptography is one of those sweet spots where One, you get people that are actually academically trained in the field contributing, but also an appreciation from the, and it may be just the personalities, it may be the, you know, the Pieters and the G-Maxes and the, you know, the Jonas Nicks of the world who just appreciate that there's another side and getting that kind of review is of value.

## Full Stack Cryptographer

Tim Ruffing: 00:08:03

Yeah.
As I said, I think also earlier, there are different levels of, or different skill sets on different levels, like really from theory to practice.
If you ask me, then I usually tell people I try to be a full stack cryptographer, which means I want to be able to design schemes, prove them secure really in theory, but then also write specifications for them, write code for them, and not really like test them.
And not really like academic code.
I mean, if you hear about academic implementations, it may sound like a good thing, right, because it's from academics, but usually it just means low quality, it's a prototype thing.
So I really want to cover the entire range.
I mean, I leave it up to others to judge if I'm doing well at this, but as I understand my role is trying to get a little bit in all of these worlds to have the big picture in a sense.

Adam Jonas: 00:08:54

Cool, I don't want to belabor this too long because we got some lower-level stuff to talk about, but maybe let's start with Schnorr signatures.

## Schnorr Signatures

Adam Jonas: 00:09:01

So we have come up on just about a year, almost to the day, of Schnorr and Taproot being soft forked into Bitcoin.
Where are we at?
Are we happy with what's happened in the last year?
How do we feel about it?

Pieter Wuille: 00:09:17

Well, in...

Tim Ruffing: 00:09:20

Are you happy in terms of adoption?
Maybe that's an interesting question.

Pieter Wuille: 00:09:25

I don't care.
I was looking for words to say that, but really I don't care.
I feel like as far as taproot, the consensus rules and the specification and the bip and the work and the address format and all those things, my job ended two years ago.
That doesn't mean there's nothing left.
Whether or not this gets adopted and at what level, that's, I think, very long term.
These things weren't designed to, you know, I wasn't expecting everyone to immediately start using this.
It will start here and there in niche use cases that really use it.
And I certainly expect that over the course of a couple of years, it will essentially become a default, but no rush.

Tim Ruffing: 00:10:19

Right.
Also, I mean, I think what we can say after one year is that it's running, it always worked, right, it didn't create any...
No issues.
I mean there are some minor things that we might have done differently in hindsight, but I guess it's kind of unavoidable because you can never predict the future.
But all together, it works.
There were no issues discovered.
And this is, I think, good to know.

Adam Jonas: 00:10:44

And so maybe, just sort of recap, Introducing Schnorr has been something that's been talked about for a very long time.
2014?
2014, yeah.

## Why is Schnorr preferable to ECDSA?

Adam Jonas: 00:10:54

And so why do we want this over ECDSA?

Pieter Wuille: 00:10:58

Maybe it's good to go over the history here because I think our reasons for wanting it, at least me personally, have changed.
The very first, this observation years ago, 2014 was like, wow, Schnorr has this linearity property which means we can like aggregate signatures together in a transaction, what's currently being referred to as cross-input signature aggregation.
And that goal drove a lot of interest in the scheme, because if you're talking about individual Schnorr signatures on chain or individual ECDSA signatures, maybe a bit faster here or there, they have a better provable security scheme.
But on the other hand, like ECDSA is already used, like people, whatever its security assumptions and requirements for proofs are, people have, perhaps unwillingly, already accepted them.
And so the change, unless you expect to completely migrate, but who knows when that happens, There isn't really all that much benefit of like an individual signature whether it's one scheme or another.
All the advantages in practice come from either simplicity of schemes that can be built on top of it, extensions that can be made like crossing input aggregation and batch validation.

Tim Ruffing: 00:12:29

Maybe to add some of the history, more on the history of the signature schemes themselves.
Schnorr came up with this really nice signature scheme.
It has nice algebraic properties, like it looks elegant from a mathematical point of view in a sense, and this also makes it easier to prove it's secure, to give a formal proof of security, which means like if an attacker could forge signature under this scheme, then the attacker could also prove, sorry, could also solve the discrete logarithm problem with some side constraints and so on.
I can't go into technical details, but this is basically roughly what the proof would show.
Because people have studied this discrete logarithm problem on elliptic curves for a very long time, We are pretty confident that it's secure or that it's hard to solve.
So we are pretty confident that Schnorr signatures are hard to forge and they are actually secure.
And for ECDSA, the story is very different.
There are some ways to establish proofs for the security of ECDSA, but they're really like strange models, you need a lot of machinery and a lot of strange site conditions to be able to prove something.
So the confidence we really have in ECDSA signatures is really because they have been out there and nobody has really broken them so far.
But that's totally fine, I totally agree with Pieter.
This is not a main motivation to change this thing.

Pieter Wuille: 00:13:56

Maybe to give a bit of historical background here, because We're mixing the Schnorr versus DSA question with integer multiplication group versus elliptic curve question because when we're talking about Schnorr or ECDSA in the context of Bitcoin, there are always schemes built on top of elliptic curves.
But historically, the Schnorr signature scheme, the first one, was originally defined just over big integer numbers.
So that scheme has much bigger public keys, much bigger signatures, and so forth.
And then the DSA scheme was really a variant of Schnorr that was created probably with the explicit intent of avoiding his patents on this scheme.
And DSA, as far as I understand, was used in practice long before there was any security proof on them.
There are some now, but as Tim says, they're much more awkward and weird.
But DSA, just people started using it as far as I know, because it's similar enough.

Tim Ruffing: 00:15:07

Yeah, but if you look at it from a mathematical point of view, it's really like they started with Schnorr signatures, but because they were patented, they had to make a few very strange tweaks to it and what comes out of it it's a really really inelegant thing and this ended up being DSA and now if you okay if you port it to elliptic curves then you get ECDSA, Elliptic Curve DSA.

Pieter Wuille: 00:15:28

We talk about Schnorr signatures but we really should distinguish like Schnorr signatures versus elliptic curve Schnorr signatures.
And the latter do exist, like for example, ED25519 is a very well-known digital signature scheme that's, yeah, EDDSA, they call it EDDSA, but it's really Schnorr.

Adam Jonas: 00:15:50

Got it, but maybe that's not the main motivation.

## Schnorr efficiency improvements

Adam Jonas: 00:15:52

There's also some efficiency improvements.
Is that get us closer to reasons to move over?

Pieter Wuille: 00:16:00

I think it is, but they're only tangible in the batching situation.
To give some context, batch validation is you have multiple messages, multiple keys, every message has a key and a corresponding signature.
So you have triplets of message public key signature and you want to verify all of them at once, and you only care whether all of them are valid or whether at least one is invalid, and if it is, you don't care which one.
And this is a property that digital signature schemes have been studied before.
And it is such an amazingly good match for block validation in Bitcoin because we really have this hundreds or thousands of signatures that we really only care whether they're all valid or not.
And so there is a decent performance improvement, like a factor of two, three, that order of magnitude that you can get from, as you do more and more at once, you get.

Adam Jonas: 00:17:02

And so how would that work in practice?
So you have, let's imagine we have a, we already have mixed blocks, as in we have some blocks with DSA and some blocks with aided taproot outputs.
So you're really just sort of like combining the taproot outputs and then validating them, and then you do everything else as before.

Pieter Wuille: 00:17:22

Exactly.
There have been ideas in the past for batching ECDSA that it's possible with additional witness data, but that's really an ugly layer violating thing you need so I don't think anyone's practically thinking about adding batch validation for ECDSA.
It's also annoying so the Bitcoin script rules permit signature validations to fail like you could write a script today that's like take us input a signature and verify that it is not a good signature for this public key.
Like, succeed unless it is a good signature.
You could write that today, it's dumb, but you, because someone would just not satisfy it by giving an invalid one, but you could.

Adam Jonas: 00:18:17

Why was that left open?
Why not include that in the soft fork, for example?

Pieter Wuille: 00:18:23

So you can't do this anymore in Tapscript, specifically because in order to make batch validation possible, the software needs to know ahead of time which signatures are expected to be valid or not.
So the change that is made is you can still have invalid signatures, but they have to be basically the empty signature.
If you just give an empty signature, it's like that's obviously gonna be invalid.
I'm not even gonna bother trying and I'm gonna treat that as an invalid one.
But everything else, and this is how we envision batch validation to work once it gets implemented at that level because we need support for it like in `libsecp256k1` cryptographic library and then in validation logic.
But how that would work is basically you work in two passes.
In the first pass, you just run the scripts and every signature that's not an empty signature, you pretend will be valid.
You just continue as if it is valid.
But you remember the combination of the public key, the message and the signature that you saw and you put them all on a list.
And after you've done verifying the whole transaction or the whole block even, you have now this huge list of all signatures to validate and then you hand off to the batch validator and check are they all valid or not.

Tim Ruffing: 00:19:49

I mean, you mentioned that this is currently not implemented, but one very nice feature about batch validation is it's really just an optimization on the verifier side.
It doesn't require any soft fork or protocol change.
It's really just like a verifier.
So it could actually be that somebody's running it today.

Pieter Wuille: 00:20:05

Right, right.
And this is by design, right?
Like BIP-340, the Schnorr signature specification for Bitcoin and BIP-341, BIP-342, Taproot and Tapscript are all explicitly designed with the goal of being batch validatable.

Tim Ruffing: 00:20:23

Yeah, the BIP340, the Schnorr signature BIP already basically contains a specification for batch verification, batch validation.
Yeah, as you say, it's just not implemented yet.

Adam Jonas: 00:20:35

It's not just implemented because just adoption doesn't make it worth the work at the moment?

Pieter Wuille: 00:20:39

So there actually is a PR open against `libsecp256k1` that implements the batch validation at the low level.
But yes, the reason why it hasn't been a priority to work on is simply it doesn't make sense until there is significant adoption.
Because as you say, the batching would only apply to the taproot signatures.

Tim Ruffing: 00:21:02

The interesting part is that you have this batch validation not only of Schnorr signatures but also of taproot openings.

Pieter Wuille: 00:21:13

Right.

Tim Ruffing: 00:21:13

So If you have a taproot key spend, it's just a Schnorr signature, but if it's a script spend, you would open this taproot commitment to this taproot auto public key.
And checking this opening of the commitment is also an elliptic curve operation, in a sense, and we could also add it to this batching.
So you have a batch of signatures in your block, in a sense, and you have a batch of taproot openings in your, or script spends in your block, and you could also like, batch the, batch both of the operations together in one single bit.

Pieter Wuille: 00:21:47

So for context, how a taproot script spend works is, you know, every taproot output is essentially an encoding of you can spend with some public key or by satisfying one of possibly multiple scripts.
And that set of scripts can be empty, that public key can be a dummy key, but both sort of always exist.
And what you do is you compute the hash of all the scripts and you use that to tweak your public key in a way.
And when spending, either you give a signature with that tweaked key directly, and all you see is a signature, or you reveal on-chain, wait, actually, let me prove to you that this public key you saw before is actually derived from this other public key with this script as a tweak.
And taproot rules in that case allow you to spend as well.
But that involves a check.
Of course, the verifier has to check that if you claim, well, this public key was actually derived from this other public key in a script, that has to be checked.
And so that's the opening of the commitment.
And that check can be batched together with Schnorr signature validations.
They each count as half a signature.

Adam Jonas: 00:23:00

So another reason to adopt Schnorr is it just makes building advanced signing protocols easier?

Pieter Wuille: 00:23:10

I think that that is really the number one reason why we want this.

## Multisigs

Adam Jonas: 00:23:15

So what's the status of those protocols now and what could we imagine to happen in the future?

Tim Ruffing: 00:23:21

So first of all, we need to look at the different types of protocols, what you call advanced signing protocols.
I think like the most popular, in a sense, type of construction so far is multisignatures which are probably also known as N-of-N signatures.
So I mean there's some kind of, we need to talk about the terminology here, because when people in the Bitcoin space say multisig, they typically don't make a distinction between N-of-N multisig where you have like n users, they all have public keys, but you require all of them to agree to give a signature, so it's really like N-of-N versus this, what I call T-of-N multisig, where T is some other arbitrary number that can be smaller than N.
So like say we have a, we could have a 2-of-3 at this table here where we like have a set, We have a key that represents the three of us, but you would only need the agreement of two of us to actually sign it.

Pieter Wuille: 00:24:26

In the cryptography world, those are known as threshold signatures, while multisignatures are the N-of-N case.

Tim Ruffing: 00:24:32

So there's this difference in terminology between like, if you look at an academic paper when it says multisignature, it always only means this N-of-N case.
And when it says threshold signature, it means T-of-N for some arbitrarily.
Whereas in Bitcoin, when you say multisig, you usually mean any of these.

Adam Jonas: 00:24:50

Okay, so multisigs, let's say, are N-of-N, we'll use the proper terminology, and there's T-of-N threshold signatures, and MuSig is supporting N-of-N.

Tim Ruffing: 00:25:05

Right.

## MuSig

Tim Ruffing: 00:25:07

Okay.
Yeah, so there's this MuSig family of signing protocols for multisig, that's why it's called MuSig.
Don't know who came up with it.

Pieter Wuille: 00:25:16

[Yannick Seurin](https://yannickseurin.github.io/) came up with the name.

Tim Ruffing: 00:25:17

Yannick Seurin, okay, yeah.

Pieter Wuille: 00:25:18

Yeah, and I think the "mu" is also because it's a letter, Greek letter that's used for "micro", so they're small.

Tim Ruffing: 00:25:25

Oh, I didn't, I wasn't even aware of that, yeah.

Pieter Wuille: 00:25:28

Oh, and multiplicative, because there's a multiplicative tweaking in there.
I think that was also part of the motivation.

Tim Ruffing: 00:25:33

It's very deep, I see.

Pieter Wuille: 00:25:34

Yeah.

Tim Ruffing: 00:25:36

Yannick, by the way, is Yannick Seurin.

Pieter Wuille: 00:25:39

The co-author on, I think, all the MuSig papers so far.

Tim Ruffing: 00:25:43

Yes.
So it is, I think, started with what we now call MuSig1.

Pieter Wuille: 00:25:51

Or Broken MuSig1.

Tim Ruffing: 00:25:53

Broken MuSig1, and I wasn't really involved in that paper, so maybe Pieter can...

Pieter Wuille: 00:25:57

Yeah, I mean, and even that had an old history that came before it because right now we're talking about multisignatures and so that is talking about the use case where there is someone on-chain who wants a policy of multiple public keys Yes, we should actually first talk about what this is going to do, right?

Tim Ruffing: 00:26:20

What's going to achieve?

Pieter Wuille: 00:26:21

Yeah, and so the goal is there, we have a number of public keys, a number of parties in the real world that jointly want to control an output and they can spend with a single signature on chain and a single public key on chain and that public key really represents the combination of the consent of all the parties.
But interestingly, the blockchain does not know or care that there are actually multiple parties involved because all that happens on chain is a single public key and a single signature the public key was created by multiple parties in collaboration the signature was created by multiple parties in collaboration but the rest of the world really just sees...

Tim Ruffing: 00:27:03

Whoever was allowed to spend these coins, and in this case it could be a group, but just by looking at this public key you don't know, is allowed to...
Yeah.
Like, is authorizing this transaction.

Pieter Wuille: 00:27:15

Whoever was required to authorize this transaction has authorized it.
Go.

Adam Jonas: 00:27:20

Computation versus verification.

Pieter Wuille: 00:27:22

Yeah, but as I said earlier, that wasn't really the original motivation to talk about the efficient or native multisignature construction.
Namely, the original motivation was actually going further and have cross-input signature aggregation.
And that is the idea of really all inputs in a transaction, even if there are multiple parties, even if the transaction is like spending coins from multiple separate coins together, we want a single signature for all of them.
And this is possible if all those people cooperate, which is often the case in terms of like even today, like if you have a wallet and you have multiple coins in it and you're spending them simultaneously, you're just one party even though you have multiple public keys.
Why wouldn't you be able to spend that with a single signature?
And I think today we think of these things as very different concepts, but originally they weren't.
And the reason is of course, well, in both cases, we want one signature that's really multiple parties collaborating and have a single key that...
But there is actually a big difference in that in the cross-input aggregation case, there are still multiple keys on chain.
There is one for every output at least because the output has to say who is authorized to spend it and it would be the verifier that aggregates them together and then verifies it against a single signature that is provided.
The difference is the aggregation of the keys done off-chain or on-chain And in the case of cross-input aggregation, you can't do it off-chain because you don't know ahead of time which outputs are going to be spent together.

Tim Ruffing: 00:29:08

In the case of multisignatures, it's really like the verification is the normal Schnorr signature verification.
So really as a verifier, you don't know, you see just one single Schnorr-Public key, but you don't know if this is just an ordinary single sign-on key or if this really represents a group because they were combining this key in the background and then using like a multi signature protocol to create a signature.

Pieter Wuille: 00:29:33

That's really the difference.

Tim Ruffing: 00:29:34

This is the thing we're talking about at the moment, right?

Pieter Wuille: 00:29:38

Because in the case of cross-input signature aggregation, the verifier actually has to implement a multi signature scheme.
You cannot have consensus rules that aren't aware of multisignatures.
Like BIP342 today and its signatures could have been written and designed without even knowing of the concept of multisignatures and it would have been useful and people would have been able to come up afterwards with like, hey, we can actually use this to do multi signatures.
The same is not true for cross-input aggregation.
And so the history of MuSig actually starts with the idea of cross-input signature aggregation.
Because cross-input signature aggregation has this very important property that if you're going to aggregate all these keys together, The problem is that the keys those parties correspond to in the real world may not trust each other.
I mean, you have an output you created, you have an output I created.
I can try creating a transaction that spends both at the same time, maybe together with one of mine.
And so it is very important that there is no way for me to come up with a fake key that somehow, when combined with your keys, result in something that I could sign for.

## Rogue key attack or key cancellation attack

Adam Jonas: 00:31:01

This is called the rogue key attack?
Exactly.
Or the key cancellation attack.

Pieter Wuille: 00:31:04

Exactly, exactly.
So the obstacle in making cross-input signature aggregation happen was, whoa, we have this problem of cancellation of keys, and we need a solution for that.
And years ago I came up with what I thought was a solution for it, which is this delinearization trick of multiplying each key with a randomizer to stop that from happening.
And so we wrote that up and submitted it to places and like this is insecure or I think we noticed ourselves I think we found an attack ourselves before we tried to publish it like that this was insecure and we tried to fix it.
That fix was what is now called the MuSig scheme, with three rounds.

Adam Jonas: 00:31:54

So it was originally two rounds and then you added a third round?

Pieter Wuille: 00:31:58

It was originally three rounds.
And that's where we tried to get published, but really none of us had experience with proving a digital signature scheme or what security properties were required.

## Bellare-Neven

Pieter Wuille: 00:32:11

And governance were like, well, there exists a scheme for this already.
It's the [Bellare-Neven](https://btctranscripts.com/bitcoin-core-dev-tech/2018-03/2018-03-05-bellare-neven/) scheme from 2006, which had a proof, which had three rounds, and I think not too long after that, so we tried to, you know, maybe write it up better and take their feedback into account, because a crucial difference between our scheme and the Bellare-Neven scheme was that scheme could be used for cross-input aggregation but it didn't result in signatures that looked like normal Schnorr signatures.
So it wouldn't be usable for what we now call multisig.
I think then we got contacted by Yannick Seurin who was a French provable security cryptographer researcher and he was like, hey, I heard you're looking into Schnorr signatures, I have a background in provable security, I'm interested.
And so it just gave him a brain dump of like, this is a scheme worth thinking of, what we're trying to prove, these are the reasons why it's different.
And a couple of weeks later, he came back like, yep, I have a proof.

Adam Jonas: 00:33:20

How fortuitous.

Pieter Wuille: 00:33:22

Amazing.
And he also said, oh, I think we can do it with two rounds instead of three, which turned out to be a mistake.

Tim Ruffing: 00:33:32

Right, this is what we now call in some papers insecure MuSig.
I think the first paper you uploaded together with Yannick Seurin had this two round version, which was insecure.
Yeah, I just found an attack on this very end of MuSig and also...

Pieter Wuille: 00:33:52

It started with this meta-proof that showed that it would be impossible to prove such a scheme secure.
And we initially thought, okay, this is like a limitation of proof techniques, like there's clearly no way of attacking this, no, those same people like a couple months later came up with an actual practical attack.

Adam Jonas: 00:34:14

When Yannick Seurin came with a proof, He came up with a proof for the three rounds.

Pieter Wuille: 00:34:19

And two rounds.

Tim Ruffing: 00:34:19

No, for the two rounds, but the proof was wrong.
I mean, this is the detail.
Oh, okay.
Got it.
Yeah.
Left out now.
Yeah, so, yeah, I mean, there was a purported proof, and it turned out to be wrong, not only because people have shown that you can't prove the scheme secure, but also because, as you say, they came up with a concrete attack.
So you had to revert to the three-round version, and this is really what we finally know.

Pieter Wuille: 00:34:42

What we now call MuSig is the three-round scheme that...

Adam Jonas: 00:34:47

And are there applications for MuSig1?

Pieter Wuille: 00:34:49

Well, every multisignature...
In a sense, yes.

Tim Ruffing: 00:34:52

I mean, it's a totally fine scheme.
It's just three rounds.
And like, nowadays we believe like MuSig2 is basically in practice better in every aspect.
So there's not really reason to use MuSig1 in practice, but it's totally fine.
It's just a little bit annoying because it has this really three-round property.
And when I say three rounds, it's really like communication rounds, right?
So the end signers come together and they have to send three messages each in parallel.
So there's one round where everybody talks, then there's a second round where everybody talks, and then only after the third round, we can come up with this, like We have the final signature that we now created together.

## Interactive versus non-interactive protocols

Pieter Wuille: 00:35:33

Maybe this is a good time to go into interactive and non-interactive.
Because in the lifetime of a signature, there are sort of two big phases.
One is the setup, where the participants maybe exchange public keys.
In Bitcoin world, this corresponds to the computation of the address, like determine what is the address for us together.

Tim Ruffing: 00:35:55

When you say setup, you mean like really key setup, right?
It's not like signature setup, it's a key setup.

Pieter Wuille: 00:36:01

Yeah.
And then the second phase is when a signature is intended to be made and there are a number of parties who agree on signing a particular message, what steps do they have to take?
And so the naive Bitcoin multisig threshold, multisignature scheme has one round for both.
Why is that?
So the key setup is everybody reveals their public key and any party, not even a participant, can just take all those keys, put them together in a script, turn it into an address, and it's done.
It doesn't need to go back to the participants.
They're just involved ones.
And then at signing time, basically the same thing happens.
They all give a signature and anyone, not even a participant, can put those signatures together in a script or a witness.

Tim Ruffing: 00:36:59

And put together really just means concatenate, right?
Like not really combined in a clever way and compress it.
It's really just,

Pieter Wuille: 00:37:06

yeah.
Put them together, concatenate, put them in a transaction, and the transaction is valid.
When we're talking about MuSig1, the three round scheme, the setup, key setup is still a single round.

Tim Ruffing: 00:37:21

Yes, it's still like everyone kind of creates their own public key and just publishes to the other participant or even to some outside party.
And you can still take all of these individual public keys and there is a public algorithm that even an outside party can run and combine the individual public keys to an aggregate public key that then represents the entire group.
This is still true for all of the MuSig variants, which is a pretty useful property.

Pieter Wuille: 00:37:50

And so at signing time, however, MuSig1 has three rounds, which means it's sort of everyone comes up with a nonce, needs to reveal the hash of the nonce.
After everyone has revealed the hashes of their nonce, then everybody reveals their nonce.
But they can only do so after everybody has revealed the hashes of their nonces.
And then after everyone has revealed all their nonces, everyone comes up with a partial signature.
And then any party, not even a participant, can take the partial signatures and turn them into...

Tim Ruffing: 00:38:22

Combine them, compress them into a single file signature.

Pieter Wuille: 00:38:25

But there are two points where basically everyone has to wait for everyone to do something And so that's why we say it has three rounds.
And whenever it has more than one round, we say it's an interactive scheme.
Because it isn't just a, you know, fire and forget.
They have to do something and then wait for the others to do something else.
Now, MuSig2, because we're already starting of it, is sort of a strict improvement over MuSig1.
The primary thing it does is, well, it actually has two rounds with a proof that appears unbroken so far.
And with good reasons, like the argument that was found, like why the MuSig1 proof couldn't be secured, that argument does not apply to the MuSig2 proof so there are very good reasons to believe that that is actually correct.

Tim Ruffing: 00:39:17

It's not only two rounds in a sense it's even better than this because what you also can do is you can pre-process the first round which basically means you can run the first round without knowing the message or in our case usually the transaction you want to sign.
So that means like we can run this first round and like okay then we need to keep state so we exchange messages for the first round and then only later if we now know okay this is a transaction we want to sign, this is a spend we want to make.
Now we, at that point, we only need to do one more round.
So it's basically, you could call it half-interactive or something like that.

Pieter Wuille: 00:39:57

I think the best way of looking at this, Like you can think of this pre-processing round, the first round of the two signing steps, you can do that at key setup time.
But you could also do it later, but like you can see this as an extension of the setup because-

Tim Ruffing: 00:40:15

But you need to do it once for every signature, right?
Yeah.
So we could do it at key setup, but then you...

Pieter Wuille: 00:40:20

Yeah, okay, you need to do...

Tim Ruffing: 00:40:21

Okay, like I will do at most like 500 signatures, for example.

Pieter Wuille: 00:40:24

So you do it 500 times.

Tim Ruffing: 00:40:26

And of course, if I ran out of these pre-processing things,

Pieter Wuille: 00:40:29

I can still do more.
Not exactly the same, but what this does is it turns something before the signing step into something interactive.
But now the signing itself can happen non-interactively.
And this is a trade-off that in some settings is very useful.
If you want low latency signing, I believe like Lightning, for example, is particularly interested in that.

Tim Ruffing: 00:40:52

Lightning is very interested in that because you if you open a connection to someone on the lightning peer-to-peer network in a sense, when you open a channel you at that point you can already run the first round.
So you exchange nonces.
And then if there is an incoming payment, at that point, you know, okay, now I want to forward this payment and now I want to create a signature.
So then it's really just because it's two parties, then it's really just one more message.
Because we have run the first round, and then let's say I'm the one in the Lightning channel, then I can create my partial signature locally, and I just send it to the other participant, and then the other participant can create their partial signature, and then they already have the final signature.
I mean, I don't have it at that point, but it's maybe enough that one of the participants has it.
So it's really just like one message then when the transaction arrives that we want to sign.

Pieter Wuille: 00:41:43

So we call this interactive or non-interactive because the difference between one round or more than one round is huge, way bigger than two or three rounds, there's always interactivity.
I think a good way of seeing that is like, today we think of addresses as being generated using XPubs and you can write a descriptor where you put these things in.
That is all only possible because the key setup is non-interactive.
Today, all I need to do is get some public keys, or XPubs from some parties, and put them together, and I can compute addresses for all of them without them even being aware that I am generating addresses for them.
Of course, I'll need to talk to them before they can spend it, but it's possible for someone to construct an address involving some parties just by getting some information from them once.
And importantly, unidirectional.
There needs to be no communication from me to them.

## FROST

Pieter Wuille: 00:42:40

As soon as we go towards threshold signatures, you know, the T-of-N where there's only a subset and FROST in particular, which is...

Tim Ruffing: 00:42:50

You could say FROST is the threshold signature equivalent to MuSig, really.
It's like a threshold signature of MuSig.
And in the signing part, it's very, very similar.
Actually, it's fun that they came up with the same idea to basically build a two round signing thing.
At the same time, we came up with the idea, so there were really two.
There was even one other research team that had the same idea in parallels, which also is good to know because this again like confirms the idea that what we're doing here is correct.

Pieter Wuille: 00:43:20

Yeah, so this idea, the one trick that the MuSig2 ...

Tim Ruffing: 00:43:24

Right, that made it like possible to go from three rounds to two rounds.
This one trick really has been discovered independently by three different research groups.

Pieter Wuille: 00:43:33

But the big downside for it seems to be like every efficient threshold scheme within this class of algorithms we're looking at requires an interactive key setup and that is a huge impediment for just practicality.
Like you can't compute an address without, you know, interacting with your co-signers.
And sure there are ways where you might be able to do that once and then still derive multiple addresses from that, without proof.
But this I think makes that sort of schemes much more niche in that it is something to deploy within like well-defined protocols that have a real need for the advantages that has over the alternatives and it can be.

### MuSig vs FROST

Tim Ruffing: 00:44:22

Yeah, I think this is really an interesting distinction that we should emphasize because like coming from this traditional Bitcoin multisig view, it's really not a difference if you have an N-of-N setup or a T-of-N setup.
It's just some parameter that you literally, like you specify the T in the script, right?
And it could just say it's N.
And this is really no, like the scheme, it's really just the same thing for T-of-N or N-of-N.
But in like those Schnorr advanced multisignature or threshold signature things, there's really a big difference in terms of practicality when it comes to T-setup.
Like MuSig, the N-of-N case is still pretty simple, whereas in threshold signatures you can do it, but it's a little bit less practical.
So as you say, it probably makes only sense for use cases that really need it.
And if I say it really needed, there's a lot of things you can do with multi signatures already.
Like even for cases where you think you may want a threshold signature.
For example, in combination with Taproot, a typical threshold signature case, I think that most people are aware of is a standard maybe two or three that you might have at home, where you have three hardware wallets or two hardware wallets and a software wallet maybe.

Pieter Wuille: 00:45:37

Or you have some service that is co-signing and you have a key in a vault and a key on your hardware wallet or something.

Tim Ruffing: 00:45:45

Two of three is a pretty common combination.
And for example, what you could do now is if you can say, okay, like you have two main signing devices and a backup signing device in the sense that you, as long as the two main devices are working, not stole, not lost, whatever, those two devices, what you can now do is you can create a 2-of-2 MuSig setup or MuSig2 setup with those two devices and put this at the root of a Taproot.
So like computer combined 2-of-2 key and use this as the key in your tab root.
And as long as those two devices are there, you can use them.
And only if you have to resort to the backup device, you would have in your Taproot, have some script inside there.
So like what you described earlier, you would pull out the script, would prove, okay, actually this key is not only a two of two, or it's not only a normal Schnorr public key, it also has some scripts, and here's one of the scripts, and now I use this backup path in a sense.
And of course, in that case, you would reveal to the public, okay, you were actually doing a 2-of-3, so you lose a tiny bit of privacy.
Maybe you lose a tiny...

Adam Jonas: 00:46:54

Would you have other tap scripts that would be 2-of-2?
You just have...

Pieter Wuille: 00:46:58

So there are two variants here.
Either you have, you know, the 2-of-2 of, let's say A and B are the main keys and C is the backup key.
So you put a MuSig of A and B as the internal Taproot key, and then you either have a single script, which is C and A or B, but alternatively, because Taproot has the script tree notion, you can have two scripts in there, both of which are in fact each a 2-of-2 MuSig, one of A and C and one of B and C and this is actually more private and a bit cheaper too.

Tim Ruffing: 00:47:38

So there's different straight-ups you can make.
I mean I think my main point was that okay you lose a little bit of privacy because you show that something was going on under the hood but it's really just a tiny bit.
I think it's only in the case where you need to resort to your backup device or signer, and it's maybe a tiny bit less efficient, but in that case, you probably don't care.

Pieter Wuille: 00:47:56

But this whole thing, like the MuSigs, the scripts, the tree, all of that still has a non-interactive key setup.
The reason why you would want to do this over something FROST-like is sort of the traditional way of thinking of I can just generate addresses if I have the keys still works with this.

Adam Jonas: 00:48:18

So you've mentioned FROST a couple of times now.
What is FROST?

Tim Ruffing: 00:48:22

FROST is really like the...

Pieter Wuille: 00:48:25

Flexible, round, optimized, Schnorr threshold signatures.
Oh, FROSTs.

Tim Ruffing: 00:48:32

Yeah, the last S probably wasn't in the abbreviation.
Think of it like the MuSig2  equivalent, but in the threshold world.
And as I said, like the signing part of it, it's pretty similar.
It's a two round signature scheme, like a two round interactive protocol.
If you look at the signing protocols of MuSig2 and FROST, you really like, you could almost, really almost the same.
The difference is really like in, as Pieter said, in the, in the key setup.
Now where you like for, for the threshold thing, you would need to run this interactive setup.

Adam Jonas: 00:49:03

I see.
So there's no pre-processing that you can do there?

Tim Ruffing: 00:49:07

There's still pre-processing in the sense that, I mean, you have to run this interactive setup, but there's now again, like it has two rounds, but you could pre-process the first round of those.
This is still possible in FROST.
So you can still have this property where you, in a sense, you send your first round messages, your announcers already up front, and then only when a message or a transaction to sign arrives, then you give the actual partial signatures, and then it's just one round left.
That's really because the signing protocols are very similar.
It's just really the key setup what makes a difference here.

Adam Jonas: 00:49:41

I see.
So T-of-N, really, it could be N-of-N in terms of like...

Pieter Wuille: 00:49:48

Yeah, it would be overkill to use FROST for N-of-N, but I guess it would work.

Tim Ruffing: 00:49:52

In theory, yeah.

Adam Jonas: 00:49:53

But there is a little more, there is more flexibility by definition.
Yeah.

## Spending Policies with MuSig

Tim Ruffing: 00:49:57

But maybe one thing that I, maybe we should talk about is again like Taproot and MuSig, why this combination is so powerful and in the sense, because I think one thing idea, like the design idea of Taproot is really like, okay, there is this key and imagine any complex thing going on in the background, maybe like you could call it smart contract or spending policy or whatever.
For concreteness, maybe think of a lightning channel where we have one party and another party and they put their coins together in an output that they can only spend together.
Unless maybe one party disappears, there's some time out and so on.
And the basic idea here is really that as long as the involved parties in this contract or maybe in this Lightning Channel for concreteness, as long as they all agree and they're present and online and are willing to move the protocol forward, they can always just give a corporate random MuSig and give a multisignature.
As long as they do this on chain it really is like just a public key, just a signature.

Pieter Wuille: 00:51:10

Yeah and this is really the philosophy behind Taproot like why do we even bother like elevating one individual public key to be blessed, to be like, you can be spent super efficiently.
It is because of this understanding that almost all involved spending policies can, without loss of security, be turned into a, okay, that involved spending policy or everybody agrees like if everybody agrees and this goes to like this idea of like we're really only using the blockchain to settle disagreements like as long as everyone agrees with all we have to say to the blockchain is like yeah you don't really need to know what the rules were everybody who and then everybody who could have been involved in this thing agrees that this is the spend we want to do.

Adam Jonas: 00:52:04

Sure, the robo judge.
Yeah, exactly.

Pieter Wuille: 00:52:07

It's like, hello judge, we settled out of court.
Okay, stamp.

## Conclusion

Adam Jonas: 00:52:12

That concludes the first half of this conversation.

The second half we are going to talk about nesting, roast, block-wide aggregation, adaptive signatures, atomic swaps, and much, much more.
Hope you're enjoying the conversation and we'll see you
