---
title: 'Miniscript'
transcript_by: 'hkmiadli via review.btctranscripts.com'
media: 'https://podcasters.spotify.com/pod/show/chaincode/episodes/Sanket-Kanjalkar-and-Miniscript---Episode-17-e1a4pmc'
date: '2021-11-11'
tags:
  - 'descriptors'
  - 'htlc'
  - 'miniscript'
  - 'psbt'
  - 'taproot'
speakers:
  - 'Sanket Kanjalkar'
categories:
  - 'podcast'
summary: 'Sanket describes to Murch his work on Miniscript. We explore uses for Miniscript, learn about intersections with PSBTs, Output Descriptors, and Taproot, and suss out the difference between Miniscript and Miniscript Policy.'
episode: 17
additional_resources:
  - title: 'Partially Signed Bitcoin Transactions (PSBTs)'
    url: 'https://bitcoinops.org/en/topics/psbt/'
  - title: 'Miniscript website'
    url: 'http://bitcoin.sipa.be/miniscript/'
  - title: 'Rust Miniscript'
    url: 'https://github.com/rust-bitcoin/rust-miniscript'
  - title: 'Miniscript C++ implementation'
    url: 'https://github.com/sipa/miniscript'
  - title: 'Gramtropy'
    url: 'https://github.com/sipa/gramtropy'
---
Jonas: 00:00:15

Welcome back to the Chaincode Podcast.

Murch: 00:00:17

Hey, this is Murch.

Jonas: 00:00:18

And Jonas.
Murch, this episode sounds a little bit different when we actually get into the meat of things.
So why is it different?

Murch: 00:00:26

I did a little bit of field reporting.
So I recorded an episode myself for the first time.
We were using different equipment, different environment.
I think the sound could have gone a little better, but I recorded a great episode with Sanket.

Jonas: 00:00:42

Cool.
Yeah, it's really great to have Sanket on. And you really get into the weeds in this miniscript stuff, huh?

Murch: 00:00:48

Yeah, we explore a little bit the intersection of miniscript with other developments recently.
So PSPTs, output descriptors, miniscript policy versus miniscript.
I think especially if you're into wallet development or addresses and that sort of stuff, this one will be fun.

Jonas: 00:01:07

One of your many nicknames is the wallet whisperer.
So I think it'll really be showing your colors here.

Murch: 00:01:14

Hahaha, I guess.

Jonas: 00:01:15

All right, hope you enjoy the episode.

Murch: 00:01:24

Hi I'm sitting here with Sanket Kansalkar and I'm gonna talk to him about miniscript and miniscript policy and his work that he's doing on making it easier for us to implement more complex contracts on Bitcoin.

Sanket: 00:01:49

Hi, I'm Sanket.
Nice to be here in New York and excited to discuss more about miniscript.

## What's Miniscript?

Murch: 00:01:57

Miniscript, what is that even actually?

Sanket: 00:02:00

Miniscript is Bitcoin script, a subset of Bitcoin script.
So to understand what miniscript is, I'll just go briefly into the problems with current Bitcoin script.
As the listeners of this podcast are aware, we have Bitcoin script, which is a stack-based language, which operates on certain opcodes, which manipulate the stack in certain ways to hopefully finally give you a success result.
And even though it seems simple at first glance, like you have the stack and you have these opcodes which do some deterministic things on stack.
It should be easy to analyze these things, but you could do lots of complex things with Bitcoin, with the current Bitcoin script, which aren't easily analyzable.
Like look at the first element, look at its size and based on that, do something else.
And what we, our goal with miniscript was to have something which is more structured.
It should enable composition and analysis of script.
We also get some other cool features which we will get into but first we get this semantic analysis of script.
I give you some script and you want to figure out what it does.
It's a mini script you will you can easily figure out what it is doing and right now if you look stare at bunch of like Bitcoin script with this opcodes and weird hexes looking at you, you really have no idea and you hope that it does what it does correctly.
 
Murch: 00:03:25

Okay, let me try to extract all the things you said here.
Miniscript is a subset of the whole Bitcoin script language and you're only using opcodes to understand what they're doing on a...

Sanket: 00:03:38

It's best if we not think in terms of opcodes, but we think in terms of fragments of the operations which we are interested in.
So, miniscript has three fundamental operation Bitcoin fragments that we are interested in, like signature checking, hash locks, and time locks.
And we have different types of hash locks and time locks, but at a higher level, we have these three constraints, which we would want to use Bitcoin script for and any combination of those you could have ands of time logs or like this time and this key or these three keys spent together so any combination 'ands' or 'or' thresholds of these is a mini script.
So we don't have to think in terms of opcodes or what is like check sequence verify or like doing hash or checking the pre-image is equal or not.
For thinking about mini scripts it's best if you think about these three basic constraints and combinations of these constraints.

Murch: 00:04:38

So, miniscript is an abstraction layer over Bitcoin script.
It takes the concepts out of Bitcoin script and expresses them as a logic composition basically.

Sanket: 00:04:49

Yes, It's abstraction, but it's one-to-one mapping.
Like, you can go from Bitcoin script to miniscript and miniscript to Bitcoin script, like vice versa.
Cool.
So abstraction, people usually think of it like you lose some information or you gain away but it helps you look at the same subset of Bitcoin script in a more structured way so there is a one-to-one mapping between.

Murch: 00:05:11

Okay that's important yes.

## Partially Signed Bitcoin Transactions (PSBTs)

Murch: 00:05:13

How did you come up with needing miniscript?
Why did do we need it and who is it for?

Sanket: 00:05:20

Okay, so this is before my involvement in miniscript.
How did people come up with miniscript?
It started with PSBTs. So with PSBTs you have, in the PSBT workflow, we have these different roles where- 

Murch: 00:05:36

PSBT of course stands for Partially Signed Bitcoin Transactions and describes a protocol for creating multi-user transactions.

Sanket: 00:05:46
Yeah, so with this PSBTs, we have like this partially signed Bitcoin transactions.
We have all these different roles.
We have a, in a PSBT workflow, we have say a creator role which creates a basic transaction skeleton and we, I'm ignoring the PSPT v2 parts for now, but let's just stick with the original PSPT.
The rules are pretty much the same.
We have a transaction creator.
We have some transaction updater role, which would update the transaction with some necessary signing information.
We have the signers, which could be your hardware wallets, which would sign that transaction.
And we have this role finally called finalizer, which is different from signer.
And the job of finalizer, so the job of signer is to get, like take this PSBT, this bunch of key value pairs and for a particular input, put its signature in some certain, in a key value pair onto this PSBT data structure.
And you would pass on this PSBT to different hardware wallets, software wallets, and we even have extended PSBT spec with hash, like hash free images.
And people would feed in all this information into your PSBT key value store.
And you still somehow have to create this script SIG or witness.
And the job of this finalizer is to create this, like look at all this information, which has already used, like has all the signatures and everything and finally create this final witness or final script SIG fields Which those are called in PSV.

## Analyzing PSBTs with Miniscript

Murch: 00:07:23

Right.
So how does mini script?

Sanket: 00:07:25

Yeah, this is where mini script comes into play. So let's say you have a complex like some script now you have some complex script like a three or five and one of them in like you're trying to spend a three or five output and one of the three or five is say another some complex policy which has you implement a time lock and maybe it has it can also be spent by some like lightning HDLCs. So when your hardware wallet just gives you a signature for the corresponding like corresponding input and the signature message and now you have to still satisfy this given all these signatures you still have to create a final witness now this is where many script comes in it looks at all these possible like so it looks at the script which you are spending the witness script or the redeem script, and figures out what, like based on this public key, this satisfaction, I have satisfaction for these keys, I know the pre-images for these time locks, and it is currently it is this sequence number for this transaction and it is this time log so can I use this path?
It will figure out all it will take all this information and create this final like this final witness or final script so it's kind of like a smart finalizer you could have any miniscript and you just your wallets just given their signatures and like hash images and the miniscript finalizer would just automatically fill in the witness for you.

Murch: 00:08:55

So the miniscript in PSPT is basically used as a recipe on how to reconstruct all the ingredients, all the signatures that people have provided, given the public key information and so forth, into the actual Bitcoin transaction that then can be sent to the network.

Sanket: 00:09:14

Yes, exactly.
And that's how it was motivated.
Now you have all these signatures.
Now, how do you actually create this?

Murch: 00:09:20

Right,ok

Sanket: 00:09:21

and that is what led to like then we should have so you cannot obviously do this for all Scripts like you could have complex scripts where it cannot even if you have signatures or something, you just can't reason about these scripts, how to satisfy those.
But then I think Peter and you were primary Andrew Postron and Peter, whatever they were involved before I started working on this project.
And they decided, okay, if we look at a subset of this, which is analyzable, we can satisfy those scripts generically.
And that is where miniscript was like, that's how miniscript was started.

Murch: 00:09:56

Okay, so basically, it was that just describes how we got a subset of script in the first place.
We only took the ones that we could analyze and could generically express.
And the motivation was to be able to craft these recipes for PSPT.

## How do Output Descriptors relate to Miniscript

Murch: 00:10:15

I think that's also related to output descriptors, right?

Sanket: 00:10:19

Yes, so yeah, that is also related to output descriptors.
So, output descriptors essentially are like encodings of your witness script or script pub key, or sorry, reading script.
So when I say, I just try to distinguish those witness script is like segwit thing and reading script is like the P2SH version of.

Murch: 00:10:41

Right,

Sanket: 00:10:42

yes.
Ideally, we would want to extend these output descriptors with mini script descriptors.
So you would have, right now our descriptors are like fairly limited.
You have like multi and multi is I think probably the most complex one which you have.
So...

Murch: 00:11:01

You mean upcheck multi-sig?

Sanket: 00:11:03

Yeah, no, multi-descriptor.
Like, you know, multi-descriptor.

Murch 00:11:05

Oh, multi-descriptor. Ok

Sanket 00:11

So with miniscript, we would have a miniscript descriptor, which would be something like a WSH of, inside of that you would actually write your mini script descriptor.
And since there is a one-to-one, so this is how it like fits in with PSBTs, where you have this redeem script or witness script, And from this, I mentioned previously that we have this one-to-one mapping between all of these mini scripts and the scripts.
So you look at all these witness scripts, you create a mini script from it.
So one-to-one mapping, we can do that.
And by looking at that, and like the structured mini script and the witnesses, you can create this.

Murch: 00:11:52

On the one hand, miniscript can be used by somebody that looks at Bitcoin script to convert it to something more generic and the miniscript representation, and then to forward it to the others?
So I think you lost me a little bit, sorry.

Sanket: 00:12:11

So I think the question was like output descriptors and how does miniscript fit into, like I'm interpreting the question as how does miniscript relate to output descriptors and where does miniscript fit in this descriptor world?
So this would be a, miniscript descriptors would be like an extension to the current descriptors where right now we have like say WSH of multi is a descriptor.
Inside of that, you would have WSH and a miniscript string representation, which would describe a miniscript output.

Murch: 00:12:43
Right.
Okay.

Sanket: 00:12:44

And that is how, like, you, and then you get all the cool properties of like descriptors.
You can figure out the script of keys and with miniscript you get like figure out.

Murch: 00:12:55

So, so currently output descriptors do not use miniscript yet, but it would be cool to do so.

Sanket: 00:13:02

Yes.

Murch: 00:13:02

Okay.

Sanket: 00:13:03

Yeah, it would be like as an output descriptors, we use those as in like in Rust miniscript and like there is a full like miniscript is fully specified and we have a good idea and we know that we are going to use how we are going to use output descriptors, but they are not specified in Bitcoin core output descriptors.md

Murch: 00:13:23

Right, right, okay.

Sanket: 00:13:25

So we have a very good idea and probably a final idea of how miniscript descriptors are going to look like.

Murch: 00:13:30

Cool.
You mentioned that there is a difference of course between or that there is more than one implementation of miniscript.

## Implementations of Miniscript

Murch: 00:13:39

There's Rust miniscript.
I think you've been working a lot on that.
And there's another miniscript implementation.
Is that in Bitcoin Core?

Sanket: 00:13:49

I mean that's a C++ implementation which is designed to be implemented, like easy to be merged to it with Bitcoin Core.
So it's not in Bitcoin Core, it's a separate repository.
You can go to like sipa/miniscript. That's a C++ implementation of miniscript.

Murch: 00:14:06

I see.
So miniscript is not in Bitcoin Core at all yet?

Sanket: 00:14:09

No, it is not in Bitcoin Core at all yet.

Murch: 00:14:13

Aha! So how's that going to happen?

Sanket: 00:14:15

Hopefully through some part through me and Yeah community review.
So it is one of the things which I have taken up on myself and like Hopefully plan to do in the near future is to take Peters were like Peters currently implemented version of many script and make a PR to Core to have miniscript descriptors and output wallet support for miniscript.

Murch: 00:14:42

Okay, cool.

Sanket: 00:14:43

Yeah, and that will bring a bunch of cool things.

Murch: 00:14:46

My understanding is that you and Repulstra, SIPA of course, have been looking at miniscript for a while.

## Semantic analysis of Scripts

Murch: 00:14:56

You mentioned that you use it as a tool for analysis of what script does.
Can you tell us a little bit about cool improvements that you found or astonishing discoveries you made while doing that?

Sanket: 00:15:09

Yeah.
I'll split this answer into two parts.
So first is the analysis part, which is, given a miniscript, you can look at the miniscript, like you can just, it's a tree structure.
You can look at the miniscript and you can understand what it does, which is something you cannot do with script.
You can see it's an add.

Murch: 00:15:29

Yes, I can attest to that. Hahaha

Sanket: 00:15:33

Yes. But not only that, it is a, since we have this structured format, you can answer questions like can this miniscript ever be spent?
If I don't have access to my cold wallet, can anyone ever spend the script?
And you can answer these type of questions which you might want for your security audits.

Murch: 00:15:52

That sounds really important in the context of PSPT and some of the vulnerabilities we found with hardware wallets in the last year or so where hardware wallets could be tricked into participating in transactions where the outputs were actually not spendable by them and things like that.

Sanket: 00:16:07

So this allows you, this is more for your software wallet analysis type of things, but hardware wallet, like it does not help you.
Hardware wallet probably do not even need to understand miniscript which is slightly digressing but I think I should highlight this point.
So miniscript like hardware wallet should just understand that given this is your key and this is the PSPT.
Just create a signature for it.
And in the PSPT workflow, they don't need to understand anything.
They just need to know, I know this private key and I'm asked to give the signature.
I'll give the signature.
Now, miniscript does not deal with like vulnerabilities of those sort, but your software wallet on the other hand can make these claims that if I trust this hardware wallet or if I trust this key and as long as that is not hacked, I have all these different components of my script or spending different spending paths.
As long as those are compromised or whatever happened with them, I can be sure that I have this thing with me and without that you cannot steal it.

Murch: 00:17:09

So being able to more clearly analyze how the script works allows us to test our security assumptions more easily.

Sanket: 00:17:16

Yes.
So, I'll correct myself slightly, I mentioned software wallet.
I should just mention software.
Like, it does not have to be wallet.
Like, you could have a mini script analyzer, which will analyze your script and tell you statically, this cannot be spent before this time and this cannot be and you do this generically.

Murch: 00:17:36

Yeah We've had lately a bit of a push by some people to distinguish wallets from signers Like actually a hardware wallet might be better called just a hardware signing tool or module.
Because a lot of what we think of as the wallet is really the software that keeps track of your funds and provides UX to the user.
So maybe that's a little related here, the hardware signer and the software wallet.

Sanket: 00:18:07

The software analyzer.
It does not even have to keep track of your funds or anything.
It's just for analyzing your script.
And so that is the analysis.
That's how miniscript relates to semantic analysis.
And you can, we are open for more PRs or anything if you find more cool things to analyze with this.
And for example, I just have access to these mini keys, how does my script look like?
I never want to use my cold wallet.
What do my spend conditions look like?
I want to spend it two years from future.
You can answer these type of questions.
So going to the other part, which is like While analyzing these things and while working on many scripts, we discovered a bunch of interesting things, limitations of scripts.
As long as you, whenever you try to do something slightly complicated, you run into the script resource limits, which are the 201 opcode limit, some standardness and policy, such standardness and consensus rules about the script, like about the script size, rules about how many witness elements you can have initially in your stack as a standardness rule.
Yeah, I think those are like, those are the important ones.
So if you try to write complex if you just run into a case where you are certainly like exceeding 201 opcodes and... 

Murch: 00:19:31

That's per transaction or per input?

Sanker: 00:19:33

That is per script, per output. Sorry, per input to any which you are executing the previous output.
But if I give you, let's say you are trying to... so miniscript has to deal with all of these things because if I am spending, if I give you a like a miniscript and you look at it. You look at the tree and you say "oh, it looks great!" like I can spend it with this key and you analyze your own policy maybe for your company you implement some complex policy And let's say there's one path which requires more than 201 opcodes to spend it.
So the miniscript has to detect all of these things and one, or just not have those as valid miniscripts where you say that user, maybe if you try to spend these funds, the network won't accept it.

Murch: 00:20:17

Right.
So you could have a very complex script where parts of it are actually unspendable due to the complexity that it takes to create the input script for them.

Sanket: 00:20:27

Yeah

Murch: 00:20:28

That would be a pretty rude thing to do to a transaction partner.

Sanket: 00:20:34

Yeah, and if you're in a multi-party setting, maybe you just trick them.
You're saying, oh, this part looks good?
Yeah, why don't you accept it?
And then they try to spend it, and boom, you cannot spend it.

Murch: 00:20:43

Oh, do you want to give me 50% of your money in order to spend your money.
Yeah, I see where that might be going.

Sanket: 00:20:50

Yeah, so that is one.
So you could also, for example, have like your script size, like maybe some of your satisfactions require more than 100 elements, then certainly it becomes non-standard.
So miniscript, when we tried to look at, when we looked at these things, we thought, okay, this is a problem, because when you're dealing with small scripts, everything is good.
But when you are like certainly touching these resource limitations, you exceed one of these paths.
And then some miniscript detects all of those things.
And like in SegWit context, you have these different rules.
So miniscript would tell you, it would warn you that this script has spent paths which would possibly, which cannot be spent.
One of the examples is like Russell O'Connor recently discovered that, it was known to people, but recently highlighted that you cannot spend a time lock and height lock in the same thing because your 'n', your number for 'n lock time' in a transaction it is either greater than 5 million in which case it is interpreted as a timestamp or it is less than million where it is interpreted as a block height and say you were given this thing where your satisfaction suddenly requires you to have a time block and a height lock and you just cannot do both of them together.

Murch: 00:22:09

Right, obviously.

Sanket: 00:22:10

So we run into these issues and the job for miniscript is to do this once and for all like check and the library would warn the users that okay you are participating in a transaction where like you should not be participating in this transaction with a in this contract with someone else because it has unspendable paths.

Murch: 00:22:29

That sounds really hard to to delimit like this small section of possible scripts that are actually spendable, well-formed, don't exceed any limits, are standard, and not malleable.
So that's what you guys did, right?

Sanket: 00:22:44

And not malleable.

## Non-malleability of miniscript

Sanket: 00:22:47

That was an important part, which I should have mentioned at the start.
Yeah, miniscripts are designed to be non-malleable.
Like with segregated witness, or segwit, we destroy one form of malleability. But we also have other forms of malleability.
We have as in like your poorly constructed contracts could have, could be malleable in other ways.
And with design, if manuscript policy, like library says that this is safe, you know that if you're satisfied using that, it would be safe, non-malleable.
So where this comes into play is you could, for example, have a weird contract and change your witness so that it is still satisfied.
The funds are still sent, but you increase the size of transaction and that sort of vectors would like decrease that's an attack vector because it decreases the fee per byte of the transaction and suddenly it's not confirmed and then you have this...

Murch: 00:23:46 

Right, you could maybe make a pinning transaction pinning attack that way or just delay the confirmation of your transaction.

Sanket 00:23:54

Yeah, and that affects security of off-chain protocols because that's certainly security assumption for them.
It is important to have these things and that you know that these things are non-malleable and having...

Murch: 00:24:10

So we covered a little ground here.
We found that miniscript is always not malleable, that it is a smaller subset of all of scripts expressiveness, which in some allows you to make more final analysis of whether you can actually spend what you're participating in and things like that.
But my understanding is that you have a converter that takes a script and produces a miniscript and then vice versa you can map it back.
When you fed in some of the scripts that are currently used on the network, say in Lightning.
What did you find out about them?

Sanket: 00:24:53

Yeah, so a miniscript, as we said, is a subset of scripts.
So current Lightning script, first of all, is not a miniscript, unfortunately, because it does weird things where it looks at the first element, sees its size and determines whether that's a public key or a pre-image.
And that is something which is not friendly to the miniscript, like the type system.

## Miniscript Policy

Sanket: 00:25:15

So with miniscript, we have this additional tool, which we call the policy, miniscript policy, that is designed as a way for developers to approach miniscript, because if we look at miniscript, It has ANDs and ORs of like these things, but we also have this wrappers around those things, which are, which manipulate each fragment.
Wrapping means, wrappers mean when you transform many script from one type to some other type, or you change some of the type properties.
Each fragment is either like does something, it either puts something on top of stack or puts nothing on top of stack or evaluates the second expression.
So, miniscript has these two, broadly speaking, two type, two attributes.
Like one of them are correctness attributes and one of them are non-malleability attributes. These correctness attributes like show how we want to combine or compose this miniscript. So miniscript is like also did not highlight this it's also composable which is like you have a miniscript with which outputs which is for certain set and we have another miniscript and you can compose using this it and and ours and so on so but you cannot like just naively compose them there are we have different ways of like composing things and just directly composing them does not work at the miniscript level.
So when we modify each fragment, we change the type of each fragment, we call those as wrappers.
Wrappers are transformation from one type to other type.
So we go from, as a simplest example, if we have something which pushes a non-zero element onto the stack, which is we call 'type B' on miniscript, and we add a verify wrapper.
So if we just put up verify after it, then we'll just put nothing on stack.
So it's a transformation from miniscript 'type B', which puts something on stack, to a verify wrapper, which just checks, like it just, if there is in, it aborts if the top is not zero and it will not push anything on stack.
So we have all these different miniscript types which hold these different invariants across.
So this is bit into a technical design, but these are like the miniscript wrappers.
So why I was getting into those is these wrappers are required to make the miniscript composition work.
Like you cannot just write 'and PK' 'and PKB'.
You would have to write something like 'and PK 'and W' of some, it's like a, you would, if you read the manuscript documentation, you would understand like what all these wrappers do, but it essentially help in composing these manuscript fragments.

Murch: 00:27:58

So basically you're saying that there is not just an 'AND' operator, but there's different operators depending on which types you want to combine.

Sanket: 00:28:08

Yes, there's different operators.
And you can also change what types you want to combine using these different things.
So that is somewhat tricky to understand at first.
So we have this thing called manuscript policy. Which is another abstraction layer out of manuscript where you remove all these wrappers, where you remove all the different types of 'ANDs' and 'ORs', and you just have simple, like the one which you want to look at end of this, this, this, and all of this, which is what you would conceptually visualize your manuscript as.

Murch: 00:28:37

So that's basically a human readable, writable thing that then later gets transformed into a miniscript.

Sanket: 00:28:46

Yeah.

Murch: 00:28:46

And from the miniscript is, of course, exchangeable to bitcoin script.

Sanket: 00:28:51

Yes.
So I would like to highlight that this is one, like this policy, yeah this representation is what we call the policy and we have a one way for going from miniscript policy which we call 'compiling'.
So it's not a one-to-one mapping anymore because you're losing information when you try to lift up.
So this invariant is, it's not necessary that it will hold.
You can go to policy to use miniscript and miniscript to policy, it might not.
The compiler might do different things and it might change things.
But policy is like the most natural way for any developer person who is interacting with script to write something.
You think about things that are like 'and' of this, 'or' of this.
You don't necessarily think about, you never think about many script fragments.
Those are like our constructions.

Murch: 00:29:39
Right.

## Rediscovering HTLCs

Sanket: 00:29:40

So we have, so for lightning policies. We looked at like, we made a compiler, which just looks at all the different possibilities and proof forces things and we found something which was better in average satisfaction cost than what the lightning developers had initially constructed and not only that we get something which has less satisfaction rates for HTLCs. Now, this is technically, I like to highlight this, these are never meant to be broadcasted on-chain, like HTLCs should never be, but still they can be in case a spear goes offline.

Murch: 00:30:14

You want to avoid it, but they're totally meant to be broadcast.

Jonas: 00:30:17

Yeah, they're totally meant to be broadcast.
Yeah, that's a good point.

Murch: 00:30:20

They're basically cached on the second layer and only when necessary are executed on-chain to decide a conflict.

Sanket: 00:30:31

Yes, so we found something which is cheaper to that.
But not only that, that is miniscript.
So with that, you get all these bunch of cool things which we discovered.
Like you could have REST miniscript, like any wallet which can satisfy it.
You could do analysis on it.
You could do smart fee estimation on it 

Murch: 00:30:49

You could basically have a lightning signer use any existing hardware signer as a lightning signer done, right?

Sanket: 00:30:57

You could you could use any signer you would just need a miniscript finalizer to finalize all these things. So, yeah. You could use any hardware signer or any signer which you want.

Sanket: 00:31:06

And you don't need to have all these like hard coded logic for, I have not looked at Lightning Core, but I would assume that they have this logic which would be like hard coded for this particular Lightning script we need to feed in.
Like the first element should be this, the second element should be this, and third.
And if you looked at any all the smart contracts which people have deployed, they have this hard-coded things.
And this really screws up inter-operation between wallets, which is a very slick, a good point where if you have miniscript compatible wallets, you have green two of three and something like you cannot just go to some other wallet, right?

Murch: 00:31:40

So basically that brings us back to the question, who is miniscript for?
And it is, It could be used by wallet developers to ensure interoperability with hardware wallets or second layer protocols.

Sanket: 00:31:54

Yeah, second any wallets basically. Like if you're supporting miniscript scripts and other wallets support miniscript scripts then they can satisfy your thing, you can satisfy their thing.
It is just the finalizer which I would like to highlight.
Your signer does not need to do anything.
Like it's just only the final, the part, the one which puts in the witnesses into place. That one needs to understand miniscript.
So it can just be a software thing.

Murch: 00:32:17

Nice.

Sanket: 00:32:18

So you don't have to go through all the hardware wallets to see a ad miniscript.

Murch: 00:32:24

You found a way to better express the currently prevalent Lightning transaction types.
And how did that go?
Did everybody adopt that already?

Sanket: 00:32:36

No, no.
I mean, my understanding is that in Lightning implementations you already have that deployed everywhere and to change the way in which you negotiate HTLCs and is not only like just a script problem but a network layer problem probably requires much more of an engineering effort to get it through and I think they're like with the new implementations they were discussing it on the mailing list thread about whether they can adopt miniscript, like miniscript supported, or many script descriptors, or miniscript scripts, and that would be really great if they adopted.

## Miniscript uses

Sanket: 00:33:11

And so it's who should use miniscript.
If you are a wallet, like if you're a wallet, you should make sure that you're not doing...
Most of the things can be done by miniscript.
It's like hash locks, time locks, and signatures, and that is most what you use Bitcoin for.
So you should have miniscript.
And for users, if you're doing any complex multi-party contract, You can just analyze your thing that you're participating is correct.

Murch: 00:33:34

And so would it be fair to say that miniscript makes the job of a wallet developer easier?

Sanket: 00:33:40

Yeah, it allows you more functionality, which you could just be a simple thing like I only support free to book key and just have this one thing but if you want to step anywhere more than that you yeah this would make your life much easier like you don't have to deal with fee estimate as in like you don't currently yeah you cannot estimate your with if you have any complex contract it is hard for you to know what is the maximum possible satisfaction witness size which you can have maybe you look at this and it's a complex contract.
You don't know how much fees it would take. You cannot guess its fees. So you still have to have the fee output.

Murch: 00:34:18

So when you build a transaction and it is a complex contract that has multiple ways of being executed. Miniscript allows you to directly calculate how big the transaction might end up being on the chain, which you need to know in order to estimate the fees in advance.

Sanket: 00:34:34

Yes, exactly.

Murch: 00:34:35

And you need to pick the fees while building the transaction before signing.

Sanket: 00:34:38

Yes.
Right.

## Removing script limitations with Taproot

Sanket: 00:34:39

Yeah, that's one of the, one small thing which we did not highlight is all these script limitations which we discussed, they made their way into TAPscript.
So although we did a bunch of work for many scripts trying to deal with all these resource things, but in BIP 342, we realized that it's like not a, these things are Satoshi-age things, which we, like many other things, don't know.
The reason why, as in, they were there for denial of service reasons but now we better understand Bitcoin so you have removed those limits and those are only like block level limits now also the complex check multi-sig of code which did like weird counting for 201 opcodes that has also been replaced by a much more thing, which actually CHECKGISADD friends, which would more represent the cost that actually the CPU incurs when trying to validate the transaction.

Murch: 00:35:32

So Taproot removes UpCheck, MultiSig, CHECKSIGADD instead and a few other of the script limitations have been thrown out in order to make scripts easier to analyze and all of that came out of your, you and your colleagues' miniscript research.

Sanket: 00:35:51

Yeah.

Murch: 00:35:52

Cool.

## Generic signing

Murch: 00:35:53

What's the coolest thing in miniscript altogether, would you say?

Sanket: 00:35:58

So I would say like the coolest thing is like this generic signing or generic finalizing where you have your wallet, everyone has their own wallet in a fancy future, we have these different policies that everyone has.
You have your own policy, you are engaging in a multi-party contract with me, I have my own policy, you have your hardware wallet somewhere else, I have my signer somewhere else and in a PSBT workflow we would just transfer this PSBT around. All the wallets would just put in their signatures at their respective places And we have this complex contract, the wallets don't even need to know what the contract is, like where is the 3 of 5 or something. We just need to know I give you this public key, this is the message you need to sign for, they would put the signature there, and you just have one final miniscript software which would create this thing.
And this is really cool because previously you have all this, like, there's no interoperation between wallets.
Now you have different wallets, which do not even need to understand miniscript and this like just a final piece together, you can.

Murch: 00:37:03

So this will make it a lot easier for various different wallet software to interact and basically establish a industry standard on how to think about scripts.

Sanket: 00:37:17

Yeah, miniscript is a standard, like you would, it is Bitcoin script, but it is one of the, so it's not necessary that you have to, you don't need any soft fork or any like any consensus implementation.
You just have miniscript and you just need one final software and that's cool.

## Future work

Murch: 00:37:34

What's the general status of miniscript?
We talked a little bit earlier about how you're still working on getting it implemented in Bitcoin Core, how there's prototypes for it, but where are we at with miniscript right now?

Sanket: 00:37:48

We have, my primary role has been on the Rust implementation, like the Rust miniscript side of things.
And one of my projects there is to extend miniscript to TapScript, like Taproot miniscript.
Now that we don't have all these complex these weird constraints some things become easy but now we have this new upcodes so we need new terminals for expressing the checksigadd friends multi and we also have a different this is still an R&D so one side is R&D for tap script where we show different tap leaf versions and Merkle we are not sure that we're still thinking about how to extend that to taproot. Which will make things easy. And on the other side where we have seg-wit and support for that. So Rust miniscript version is like almost finalized. You'll see we are going to add new features, which would be more like how do you analyze things?
But the base level miniscript design and specification is fixed like there's nothing to be changed over there and you might add more smarter compilations. But for the C++ side of things I will be working, as you say. I am working so it's more correct as like I am working for the past few days. I will be working towards getting Peter's his repository miniscript updated with Rust manuscript and getting some reviewer there and then transferring and that would be like a multi-step thing because we'll discuss more with the community how that goes because it has a bunch of features, as we discussed.
One of them is just like script to miniscript.
Then we will have like, I don't know if analyzing capabilities belong in Bitcoin Core or you want different software for it.
We definitely want support for generic finalizing, that would be another task and all the tests and test framework and all those things.
So that's...

Murch: 00:39:34

And then of course it has to map one-to-one to each other and be exactly, behave exactly the same way between the different implementations.
So probably it has a very strong testing core set, huge amount of test cases.

Sanket: 00:39:46

Yes, we have tested like, I don't know million, but we have tested a lot, like all the different possible combinations of miniscripts. Peter has one more cool tool called gram trophy if it's not one of his popularly known projects. When if you give it some grammar rules, it would generate different possible combinations for those.
And we have tested that extensively with miniscript.

Murch: 00:40:12

Is that how you found the Better Lightning constructions?

Sanket: 00:40:15

So the Better Lightning construction is a compiler part.
So that is when you go from a policy which you expect to do the mini script.

## The role of policy

Sanket: 00:40:23

And this is where people get confused and I would like to highlight is one of the most common confusions in miniscript across developers is policy to miniscript is not stable.
It is something which is just designed for you to approach miniscript.
You should just use policy once. Get your miniscript and use that miniscript.
So the C++ version would give possibly different outputs.
The rest of the script would give possibly different outputs.
In future, you might have new ways to compile things to a miniscript.
You might rearrange things.
So, policy is just one way to approach a miniscript.
You should not treat policy as your miniscript.
Those are different things.

Murch: 00:41:04

So, the actual interchangeable part is the miniscript policy is the human writable part that once gets compiled to miniscript and then you should stay there.

Sanket: 00:41:17

Yeah 

Murch: 00:41:18

Cool!
So the next step is to make Bitcoin Core or the Bitcoin Core compatible implementation plain as with Rust miniscript and then hopefully to roll it out.
And my understanding is that the tap script functionality is in rest miniscript already.

Sanket: 00:41:36

No, it is.
So Tapscript functionality is in, like, it's in works, like we're still in R&D, like there's no code yet.
We are discussing, because there are a bunch of things which we can do now with taproot.
Like you could have a private test.
Let's say you have to... one of the benefits of taproot is you only show what you're executing.
If you have an OR of two things, you don't show what your second OR is.
And so then we can have this as a different hidden node and just show the script to share execution which is not true for segwit. So there is still some like design things to be done over there. We still have a good idea of how we want to do it. There's one way where you go like completely private where let's say you have your leaves all of the leaves just represent ORs of different things and you only show one of them and there's a trade-off like maybe that blows up too high let's say you're doing 11 or 15 multi-sig or something then you clearly cannot have all the different ORs in the leave.
That would be too much.
So, there is still some trade-offs and design to be figured out there, but it's...

Murch: 00:42:40

So you would want to, for example, make your miniscript compiler take into account how many leaves that would require to express a construction like that?

Sanket: 00:42:51

So yeah, tapscript compiler is still in work but the tapscript to miniscript that thing should still just that is almost done.
You just have new fragments for checks multi-sig and we remove the resource limit checks and so on.
So that is, that is RUST miniscript.
That's not, as far as I understand, like Bitcoin Core wallet support for Taproot is still like right now under review.
So I think we'll just go slowly over there with SegWit and test framework and just make developers familiar in general with miniscript, make them comfortable so we have more informed review and go forward with that.
Right.

Murch: 00:43:25

That sounds all really cool.
Are we still missing something?
Did I forget to ask you something?

Sanket: 00:43:31

I think that miniscript covers pretty much it.
Miniscript is just part of descriptors like at a high level to summarize everything.
Miniscript is part of descriptors which fit into all of this PSPT workflow and miniscript would help you compose scripts, analyze them, find smart fees, generically sign for them.

Murch: 00:43:49

Right.
How do we keep abreast of the updates regarding miniscript?

Sanket: 00:43:55

There is a pound pound miniscript, IRC channel, which is fairly active.
So we discussed a lot of things over there and Rust miniscript and C++ miniscript are the two repositories.
And if you want to play around with miniscript, Peter has this great website which is like a go-to resource for miniscript which is 'bitcoin.cpa.be/miniscript'.
So, that is the place where you can start.
And if you have any questions, approach at pound pound miniscript.

Murch: 00:44:25

Those will, of course, be in the show notes then.

Murch: 00:44:32

I hope you liked that.
We're going to probably record a few more episodes soon because more people are going to be in the office again, and we might be going to more conferences as well.

Jonas: 00:44:44

The Chaincode Podcast is back!

Murch: 00:44:46

Again.

Jonas: 00:44:47

Full force.
[Hahaha]
We've said this before, but this time is different.

Murch: 00:44:51
We mean it.

Jonas: 00:44:53

All right.
Thanks, Murch.
Thanks for putting that together.
There'll be show notes and we'll see you next time.

Murch: 00:44:58

Yeah.
See ya.