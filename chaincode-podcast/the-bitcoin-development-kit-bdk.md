---
title: The Bitcoin Development Kit (BDK)
transcript_by: nymius via review.btctranscripts.com
media: https://podcasters.spotify.com/pod/show/chaincode/episodes/Alekos-Filini--Daniela-Brozzoni-and-the-Bitcoin-Development-Kit-BDK---Episode-32-e24m4o1
tags:
  - descriptors
  - hwi
  - wallet
speakers:
  - Alekos Filini
  - Daniela Brozzoni
summary: The podcast covers the evolution of the Bitcoin Development Kit (BDK), originally known as the Magical Bitcoin Library, from its inception at Blockstream to its current status as a fully-fledged open-source project. Key topics include the renaming of BDK, its foundational use of Rust and descriptors for wallet architecture, and the broad applicability for both individual and enterprise users. Early adopters and contributors to BDK's development are highlighted, alongside discussions on the challenges and technical hurdles such as asynchronous operations and wallet management across multiple descriptors. The conversation also touches on the motivations behind developers preferring to build wallets from scratch and the potential advantages of adopting BDK for future-proofing wallet applications. Upcoming features in BDK 1.0 promise further enhancements, particularly in syncing mechanisms and transaction planning.
date: 2023-05-23
episode: 32
additional_resources:
  - title: Bitcoin Development Kit (BDK)
    url: https://bitcoindevkit.org/
  - title: BDK Discord
    url: https://discord.com/invite/dstn4dQ
  - title: Rust HWI
    url: https://github.com/bitcoindevkit/rust-hwi
  - title: Greenwallet
    url: https://blockstream.com/green/
aliases:
  - /chaincode-labs/chaincode-podcast/the-bitcoin-development-kit-bdk/
---
## Intro

Adam Jonas: 00:00:06

We are recording again.

Mark Erhardt: 00:00:08

We have as our guests today Alekos and Daniela from the BDK team.
Cool.

Adam Jonas: 00:00:13

We're going to get into it.
BDK, how it came to be, some features that are going to be released soon.
So hope you enjoy.
All right, Alekos, Daniela, welcome to the Chaincode podcast.
We're excited to have you here.

Daniela Brozzoni: 00:00:30

Hi, thank you for having us.

Alekos Filini: 00:00:32

Yeah, thank you for having us in this awesome office.
Super cool.

Adam Jonas: 00:00:35

It is a nice office, isn't it?

Mark Erhardt: 00:00:36

It is pretty nice.

Adam Jonas: 00:00:37

Sometimes we get a little too used to it.
We're super excited you're here.
And maybe we should start with BDK, since you both have strong ties to BDK, but tell us about how BDK came to be.

## How BDK started

Alekos Filini: 00:00:51

Yeah, so that's kind of a long story.
First of all, I'm the founder of BDK.
Although when I founded it, it wasn't called BDK.
It was called Magical Bitcoin library because it was like the library that supported the magical Bitcoin wallet, which was like the UI, which I don't think we've ever released.
It was terrible.
Like we kind of developed it and then throw it away.
But anyway, this Magical Bitcoin wallet started when I was at Blockstream.
So it was kind of a fun project that some of the Blockstream employees and I developed in our free time, essentially, just to kind of experiment and see.
Essentially the question was, we were all working on the Green team, so on the Green wallet, and the question was, what if we had to remake Green today?
What would we change?
And one of the pain points of Green was that it was, it supported only a few, or still it supports only a few types of scripts, which is like 2-of-2, 2-of-3, stuff like that.
And it's very hard to add new ones because everything is kind of hard-coded.
So the main focus was maybe we should try to make something that's very generic and if we were to use it for Green, it would allow us to quickly like iterate.
So that started as this kind of internal project and then over time I managed to find funding, initially part-time funding, then full-time funding to work on it as my full-time job, essentially.
And yeah, this is how it started.

## Why is it named BDK and not the Magical Bitcoin Library?

Alekos Filini: 00:02:09

And maybe I should talk about the story, about the name as well, because I mentioned this was called Magical Bitcoin library, Magical Bitcoin Wallet.
At some point Steve Myers, who independently started the BDK project with funding from Spiral, he approached me and said, you know, we're basically building the same thing, maybe we should join forces and do it together.
And so we looked at my code for Magical BDK Library and his code for BDK and realized that my code was a bit further ahead.
It was basically the same thing, but with a few more months of development into it.
And so we decided to keep, to basically keep my code, but I really like the BDK name, so we used his name.
When we merged the project, we didn't really merge the code.
It was just my code, but we took the name of BDK and the old legacy BDK just died.
I think it's still somewhere on Github, but nobody really uses it anymore.
So yeah, that's the story.

Adam Jonas: 00:03:06

And then as you continue to work on it, you said it started as part-time and it's full-time.
Like, tell me the progression of how the project evolved and maybe Daniela, you can fill us in on where it is today.

Alekos Filini: 00:03:19

Yeah, so I mean I think that the biggest part of the project was developed in the first few months and then it became more of a just fixing it up and improving it little by little.

## The first users of BDK

Alekos Filini: 00:03:30

A bunch of people slowly started to join.
So I think the first users were like Justin Moon, I think he was the first user who came and started contributing a little bit.
Then came Lloyd as well.
And he really did like a lot of contribution.
He was using it for, I don't remember his name, GAN, I think, something like that.
It was like a wallet.

Adam Jonas: 00:03:49

Go up a number.

Daniela Brozzoni: 00:03:50

Yep, exactly.

Alekos Filini: 00:03:51

Yeah, I think that's it.
And so with Lloyd and a few other people joining, it kind of started becoming more of a mature project in a way, but still kind of the core concepts and architecture, they were still the same.
And this is going to be an important talking point because I guess we're going to talk about BDK 1.0 later.
So this kind of explains why BDK 1.0 is going on now.
And yeah, Daniela joined.
She started contributing on and off, I think kind of early.
You did the coin selection.

## Rust HWI

Daniela Brozzoni: 00:04:18

Yeah, I think, I mean, I did the coin selection, which Murch reviewed and the code was horrible.
I'm so happy because we're going to throw it away and I'm so happy about that.
And I also implemented Rust HWI.
I mean, when BDK was still Magical Bitcoin Library.
Yeah, very early.
But then, because at the time I was unemployed, but then I found a job and it's difficult to have a full time job and also contribute to open source libraries, especially when you're a junior dev.
So I just stopped contributing to BDK until about a year ago, maybe a bit more, I think around February 2022.
Because, yeah, basically Alekos just told me, hey, we need more people contributing on the library.
And so I started contributing to BDK as a full-time developer.
And I got a grant for working on it in June.
So it's about to expire.
So yeah, that's pretty much about it.

Adam Jonas: 00:05:14

And where is the project today?
Like, it's come from this sort of side project and evolved over time.
So where is it today?

Daniela Brozzoni: 00:05:22

Well, first of all, today it works.
And I really want to say that because we're going to say like it does have some problems, but it works for most easy use cases.
It works.

Adam Jonas: 00:05:35

And it works for what?
Like who's using it?

Alekos Filini: 00:05:37

Not that many companies are using it, but I guess there's a lot of interest.
Like we, we get a lot of questions, a lot of new users joining.
We have a Discord server, So they join the server and they ask questions.
In practice, like in production, there are not that many.
I can think of Foundation devices.
They've built another wallet and the mobile app that kind of controls the other wallet and I think that's built with BDK.
I know there's Mutiny, but I don't know if it's in production.
I know they're using it.
There are a few more that I can think of right now.
But yeah, we were talking about it before.
So in terms of users, we don't have that many.
But I think given the amount of interest there is, I hope it's going to pick up soon.
Like the number of people are going to pick up soon because...

Daniela Brozzoni: 00:06:21

Yeah, also I suppose there are many projects which are just using it and not telling us.
Because I mean, if you think about it, when you, I don't know, create a new project and you include some libraries, you don't go on the Discord and tell the maintainers, hey, I'm using your library.
So I think there are many other projects using it.
Yeah, and also, as he was saying, we have a BDK Discord and we have a BDK users channel, and that's always full of people just posting questions and also helping each other which is pretty cool so as maintainers we don't have to all the time help people.
So yeah I think someone is using it, but I'm not sure.

Alekos Filini: 00:06:58

We would prefer that more people are using it but you know I think it's growing it's kind of slowly but it's growing.

Mark Erhardt: 00:07:04

So let's maybe take a step back.

## Built around descriptors

Mark Erhardt: 00:07:07

BDK is written in Rust, of course, and I think one of the central points is that it is from the base app built around descriptors as an idea, but where at the time when BDK started, hardly anyone was using descriptors, but I think BDK might have been one of the first wallets that actually rolled that out.

## The ideal use case of BDK

Mark Erhardt: 00:07:27

So what would you describe as the ideal user or the expected user for BDK.
You say it's a single wallet, it's hard to use many descriptors, so it's maybe not an enterprise library, but.

Alekos Filini: 00:07:41

I think, yeah, so the way it's built right now, I mean, you can do anything, so you can use it, obviously, as an enterprise.
I mean, if you are an enterprise managing multiple wallets for multiple users, maybe it actually fits very well into that because it makes sense to have separate wallets for separate users.
Where it kind of doesn't work right now, or maybe let's first talk about what are the users we had in mind when we were developing it.
Essentially we wanted to make something super generic so we focused both on in terms of features like we want to provide an API that can be, I don't know if you want to build a single-sig wallet you can use it easily, But if you want to build a multi-sig wallet, you can do the same, as easy as building a single-sig wallet.
Or even if you want to start doing more advanced stuff, you want to have time locks in your scripts.
The idea we wanted to build was something that can kind of generalize.
And then you just use one API, and everything works fine.
And this is in terms of features and in terms of like platforms, the library works well on desktop, works on mobile.
Now with the refactoring of BDK 1.0 it's going to work on embedded hardware as well.
So it's going to be no `std` in technical terms.
So, yeah, the idea is basically to build something that works anywhere and can kind of do everything.
And yeah, in terms of the limitation that there are today, I think where it kind of starts breaking down is when you want to monitor multiple descriptors and you want to spend from all of them at the same time.

## Pain points

Alekos Filini: 00:09:11

So if you are an enterprise and you're managing multiple different clients wallets, it's fine because normally you don't want to spend funds of like different users together unless you want to do batching or you can still do it there's an option to from the perspective of a wallet you can say add this UTXO which doesn't belong to this wallet but you can add it as an input and spend it as well.
So you can do it but it's a bit more involved I guess.
And yeah, any other thing where it breaks down is if you use async Rust basically because the wallet structure is not thread safe so when you use async normally you want something that can be moved around threads because you don't know which thread is going to run a specific task.
And the BDK wallet is not thread safe, so you have to work around it and use mutex and stuff.
So those are the two biggest pain points that BDK 1.0 is trying to fix.

## Why do devs keep building wallets from scratch?

Adam Jonas: 00:10:06

Even higher level than that, the vision was, given the inspiration for starting it, you wanted to create the kernel of a wallet that people could just build their own custom cases on top of.
And so, given that these wallets continue to spin up, why do you think people are continuing to start things from scratch as opposed to using what's out there and Rust is sexy and so you'd imagine that that would attract, like, some devs in its own right.

Alekos Filini: 00:10:37

My guess is one of the reasons is the language, because Rust is sexy, but if you're building, especially mobile app, and most of the wallets today are mobile apps, it's not that sexy anymore because you have to wrap it and find a way to call it from like Swift or Java, Kotlin, whatever.
So with BDK we do provide bindings, but they're not as good as the Rust library.
So if you use the Rust Library directly, you have access to all the features.
And if you use the bindings, you have access to like 80%.
It's still very good.
You can still do a lot of things, but you don't have access to the internals pretty much.
Maybe one reason is that.
The other reason is we probably don't have the right bindings because right now we have Swift and Kotlin, these are the two main ones, because we wanted to target mobile users.
But we don't have, or at least, there's somebody working on them, but they're not fully ready.
We don't have React Native, so I'm thinking most of the wallets nowadays, or a few of the big wallets are written in React Native, so we don't have that covered.
Maybe it's also scary for people, because there are libraries that are kind of focused on, I don't know, building a single-sig wallet, and you just take them and use them.
BDK, it's maybe slightly more complicated, because it's generic, but still, if you want to build a single-sig wallet it's super easy, but maybe that slight little extra complexity that kind of scares users away.
Although I would argue that it's a good investment to spend time and learn BDK because even if you're building a single-sig wallet, maybe tomorrow you want to introduce something more.
You want to introduce remote signers with 2FA or stuff like that and with BDK it's super easy to do.
So I don't know, if I were developing something I would do that extra step, maybe some other developers are not.

Daniela Brozzoni: 00:12:17

Yeah, I think we have some work to do on the documentation side of things, because I realized recently just looking at the questions that people had, that our documentation assumed that people would have a good knowledge of how Bitcoin works.
And if you're building a wallet, I mean, you should know something about Bitcoin, of course, but you don't have to know exactly what's a `ccache` and what's a lock time, etc.
Those are basic concepts, but if you really just want, okay, I'll create a single seed wallet, whatever, you don't want to have a documentation that just assumes that you know everything.
So we do have some work to do on that side.

Alekos Filini: 00:12:55

Yeah, documentation examples as well, because most people just copy paste examples.
That's like the reality.
So maybe more examples would help.

## Greenwallet

Mark Erhardt: 00:13:03

You said earlier that you originally were motivated by working on Green Wallet and wanting to sort of build a new wallet from scratch with what you had learned from working on Green.
So are they looking at BDK now as an inspiration or potential switchover?
I know that they, for example, are trying to use more complex scripts.
There was the 1-of-2 or 2-of-2 multi-sig with a decay and I think there was also a 2-of-3 wallet at some point maybe?

Alekos Filini: 00:13:36

Yeah so Green is interesting because it's a very old product, old in terms of Bitcoin years, Bitcoin age and so it kind of started in a way and then kind of evolved with Bitcoin where `OP_CSV` at some point became available so they started using it.
So internally Green supports the old 2-of-2 it's like it's a normal 2-of-2 but they email you a pre-signed transaction with a future lock time.
So the service disappears you have this email with a pre-signed transaction, you can just apply your signature and recover the funds.
Then they introduce the 2-of-2 with CSV.
So that's done inside the script, it's the user always need to sign, and then it's either the server or you wait some time.
And then I think they introduced a slightly tweaked version of this concept, which is still a 2-of-2 with CSV, but it's descriptor compatible, essentially.
So it's basically written, the descriptor is a form that can be parsed into a descriptor or vice versa.
You can from a descriptor get the script and then they also have 2-of-3, which doesn't have any time lost or anything.
It's just one key that the server has one key and the user has the other two.
And so you can always recover your funds if...

Daniela Brozzoni: 00:14:50

Sorry, stating the obvious, they also have a single-sig wallet.

Alekos Filini: 00:14:53

Ah, single-sig, yeah, single-sig came pretty recently.

Daniela Brozzoni: 00:14:55

Yes.

Alekos Filini: 00:14:56

So in the Green app, you can also select a single-sig wallet, but that's implemented separately.
It's like a Rust library, while everything else it's in C++, so it's kind of complicated.

Mark Erhardt: 00:15:07

So for the Rust library, do they use BDK?

Alekos Filini: 00:15:09

No, actually.
But yeah, going back to the BDK question, I don't know from the high ups if they agree with that.
I know the actual devs, our ex-colleagues working on the wallet, I know they would like to use BDK.
The problem is their library, which is called GDK, which is Green Development Kit, does Bitcoin and Liquid together.
And BDK is Bitcoin only.
So I think that's the main roadblock there.
So we kind of explored the ideas for...
So at one point I wanted to make BDK generic over the amount type.
So the idea was to use Rust generic so that you can have...
You can use any type for your amount as long as you can basically sum two amounts so you can compare them so I can say this is greater than that.
So the idea was if I, for Bitcoin you would use an unsigned 64 bit integer but for Liquid you would use their, whatever, Pedersen commitment type, because you can sum them together, but you can't really compare them, so you can't say is this greater than this one because it's binary, so I tried to implement that and it was a mess, so I stopped.
So yeah, I think that that's one of the roadblocks, otherwise they would probably be happy to use it, I think.

Adam Jonas: 00:16:21

Interesting.

## If you have a working wallet, should you switch to BDK?

Daniela Brozzoni: 00:16:23

I think that's a nice question, because if you already have a wallet that's working, should you switch to BDK?
It's not like, yes, you should.
It does take time to just port your code from whatever you're using to BDK, because that's just refactoring, right?
I'm not sure they should.

Alekos Filini: 00:16:45

I'd say it's an investment.

Daniela Brozzoni: 00:16:46

Yeah, it's an investment.

Alekos Filini: 00:16:47

If you want to add more advanced features in the future.
So if you have a wallet and you say this is going to be this forever, no Taproot, no next Taproot in five years when it comes, then okay, stay with your code.
If you plan to upgrade over time, it's a good investment of time to switch to BDK because then you get Taproot for free, all the new stuff because we implement them in the library.

Mark Erhardt: 00:17:10

Or if you want to do a multi-sig wallet with descriptors or any more complex descriptor wallet, I think that most libraries, I don't know many libraries that actually support descriptors at all yet.

Alekos Filini: 00:17:22

Yeah, no, there are not that many.
I mean now it's kind of starting to grow a little bit, like the descriptor ecosystem, there are hardware devices supporting them.
I think there's a Python implementation now.
There's a JavaScript implementation or something.
It's kind of starting to grow a little bit, but yeah, it's very early still.

## HWI complaints (see Python)

Mark Erhardt: 00:17:41

You said that you had some bones to pick as well with trying to work into other projects?
Should we get into them?

Alekos Filini: 00:17:50

Yeah.
I mean, so when we were talking earlier about the topics for the podcast, I said, you know, we can always complain about other projects, hoping the developers of these other projects listen to the podcast and come and help.

Adam Jonas: 00:18:07

Not likely with this podcast.

Alekos Filini: 00:18:08

Not likely.
I don't know, yeah, but one thing we can complain about is HWI, because in the Bitcoin Dev Kit organization we have this project called Rust HWI, which is kind of a wrapper written in Rust over HWI.
The problem obviously is HWI is written in Python.
So this Rust is kind of a complicated thing that loads a Python interpreter and tries to run HWI code.
So yeah, my complaint is HWI is written in Python and it's desktop only, which is something that I think most of our users are targeting mobile platforms, so they would like to use other devices on mobile.

Mark Erhardt: 00:18:49

I think I heard something about someone starting a Rust implementation.
Was that Antoine?

Alekos Filini: 00:18:54

Yeah, Antoine.
In your project or?

Daniela Brozzoni: 00:18:56

Right, yeah.

Alekos Filini: 00:18:57

Antoine from Revault.

Daniela Brozzoni: 00:18:59

Wizardsardine.

Alekos Filini: 00:18:59

Wizardsardine, yeah.
Which is the company behind Revault.
Is starting a Rust implementation, So that's good.
But I think it's still desktop only, right?

Daniela Brozzoni: 00:19:08

Yeah, I think so as well.
But yeah, they're working on that.
I think that it's important to have some kind of library to access hardware wallets on mobile, because I mean I really do use my computer a lot and while I can think of, okay, I'll just leave my phone at home and go on holiday for two weeks or something, I could never do that with my computer, but I suppose it's like the opposite for most of people.
So most of people just want to have something on mobile and then they want to connect whatever their other wallet or maybe it does have Bluetooth and just use that.
So I think it's pretty important.

Alekos Filini: 00:19:46

My holy grail, which I'm just mentioning it hoping that somebody will come and implement it because I don't have time to do it myself.
My holy grail for this library would be something that kind of separates the logic of a specific device with the communication layer, essentially.
Because the problem is if you implement a Python or Rust library for desktop, you use a libusb or whatever proprietary windows or macOS or whatever bindings you have, but then you cannot port it to Android, for example.
So what I have in mind, I'm dreaming of this library where you have one part that manages the logic, so it's like I get this message from the other wallet and this is the reply I need to send.
And then you can plug in different transport protocols or whatever.
So on Android you can implement it using Android's USB stack and then you can implement it differently on Linux and on Windows and you can also transfer the data over Bluetooth if you want.
So this is kind of what I have in mind.
At some point I thought about starting it myself and then I realized I'm doing too many stuff at the same time so I don't have time.
So I hope.

Daniela Brozzoni: 00:20:52

Yeah, I don't want to promise anything but I think that eventually the BDK team might work on that just because in BDK we do support hardware wallets using Rust HWI as Alekos was saying, but every time we have some kind of problem and it's Python related, we just look at the code and we're like, come on, let's just start it again from scratch, right?
So it might happen eventually.

Alekos Filini: 00:21:14

But if somebody wants to give us to it, please do.

Mark Erhardt: 00:21:18

I think that we had Andy on a while back and he was like, I started HWI in Python because most of the hardware designers already had Python libraries.
So that was easy to plug in.
But if anybody implements it in another language, they're happy to have it.
It's a year and echo here.

Alekos Filini: 00:21:38

Yeah, that's kind of the problem.
You need to have hardware manufacturers on board because you cannot realistically implement.
Nowadays there are five or six different devices you cannot really implement all of them reverse engineer them or anything you need the cool thing with Python is ledger releases their own library Trezor does and everybody does with Rust it's a bit harder but the reason why I'm mentioning it here is that if the Bitcoin Core organization, which I know many Bitcoin Core developers listen to this podcast, if they bootstrapped this effort, maybe the hardware manufacturer would follow them.

Mark Erhardt: 00:22:14

I think some inroads has been made with descriptors and PSBT, especially as a transfer format.
And I think that some, at least that has been adopted by hardware signing devices.
Can't make any more promises beyond that.

## BDK 1.0 release features

Daniela Brozzoni: 00:22:33

Can talk more about what's new with BDK 1.0, if you want that?

Adam Jonas: 00:22:36

Yeah, tell us about it.

Daniela Brozzoni: 00:22:37

Okay, so another big thing that's coming, it's a new syncing mechanism, let's say.
So right now in BDK, we do have one Rust trait, which defines how you sync the wallet and just for context we have this structure called `Wallet` and what it has inside it's the transactions of the user and the UTXOs so that you can just build new transactions, right?
So, sync basically means either you go to a service like Esplora, Electrum, or Bitcoin Core RPC, or maybe you use compact block filters, and somehow you update your internal state.
And so, you basically just update the list of transactions you made, adding new transactions if they happen, removing transactions if some reorg happened or if they were invalidated or something, and you update the list of UTXOs. So right now we have this method for doing the sync and it's really monolithic.
So you call sync and you have to sync everything at once.
And also that's a bit problematic because while you're syncing all the wallet structure, you can't use it.
It's basically locked.
And if you think about syncing, you can think about it as in three different steps.
The first one is some network call, let's say, where you just go to Esplora, go to Electrum, go to Bitcoin Core RPC, and just say, hey, what do you have for me?
The second step is some kind of processing.
You get this answer and you just process it and you just try to understand what's happening.
And the third step is saving what you just found out.
So you do need locking, you do need to lock the wallet for the second and the third step because you don't want someone to modify the wallet while you are processing data or while you are saving it, but you don't want to lock the wallet while you're just doing network calls and network calls usually take more time.
So we are updating the API so that, first of all, you don't have to sync all at once.
And while you're syncing and doing the actual network calls, you don't have to lock the wallet.
And you can still use it to get the balance and to create new transactions.
So, that's pretty cool.
I'm really excited about that because there are some pretty cool use cases that you could implement on top of the new BDK 1.0. For example, I was reading of this user who wanted to sync the wallet slowly, opening many Tor connections, and for each Tor connection it would just ask about one script pub key.
So that's like a very exotic way of syncing a wallet.

Adam Jonas: 00:25:19

What's the advantage of doing that?

Daniela Brozzoni: 00:25:20

I don't know.
It was just, oh hey, we could do that.
Yeah, privacy.

Alekos Filini: 00:25:24

I mean, the Electrum server receives from the same connection five requests, can assume that those five scripts are from the same user.
So you can kind of correlate scripts.
And I guess they wanted to build separate total circuits so to the Electrum server it looks like five different users asking for one script each.
I mean you can do timing analysis, right?
If it's like a sequence, it's not perfect.
But you can see improvement.

Daniela Brozzoni: 00:25:52

Exactly, you can have some weird heuristic on how to open the connections, etcetera.
So that can be done with BDK today.
With the new API, which gives us access to some lower level structures for syncing, you can do that.
And that's pretty cool.
I'm excited about that.

Alekos Filini: 00:26:12

Yeah.
So just kind of to expand on that, basically BDK now is like, you can implement custom blockchains, we call them, so you can implement your own.
You could try to implement this yourself, even if the BDK project itself doesn't provide this functionality, you can try to implement it yourself.
The problem is that BDK will call your function essentially, and it will assume that when your function returns, you've checked all of the scripts of the wallet.
And maybe you don't want to do that.
So this is what Daniela was mentioning when she said syncing all at once.
One thing you could do with BDK Core or BDK 1.0 is maybe you can just monitor the last, I don't know, 100 scripts, and then once per day you monitor all of these scripts just to make sure you're not missing out on anything.
But like in the tight loop that runs multiple times, I don't know, per minute, you can just monitor the most recent ones because those are the most likely to receive transactions.
That's one example of.
Do you want to talk about the planning or should I talk about the planning?

Daniela Brozzoni: 00:27:18

Yeah, I think you should.
Yeah, because you implemented it.

Alekos Filini: 00:27:20

So yeah, that's another cool thing.
Basically, BDK is super generic, so you can have time locks and complex conditions in your script.
And the problem is when you go and try to create a transaction, you need to know how you're going to spend later.
So essentially you need to know which path, if you think about all of the possible conditions in your script, it's kind of a tree, and you can think about the path in this tree that is the one you want to use.
And if in this path there are time locks, for example, you need to know that beforehand because you need to create a transaction in a specific way.
So for example, you need to set the unlock time to the right value, or if it's a CSV, you need to set the end sequence to the right value.
And so what we do today is BDK shows you the tree of, like an abstract tree of the policy of the wallet.
So it's going to be like a, you have a node which is an OR and then you have two child nodes which is like this key or this other key and stuff like that.
And you need to traverse this tree yourself.
And then you need to tell me which nodes of the tree you're going to use.
And this is easy on our end as developers of the library.
That is not so easy for the user because maybe they have in, like conceptually, they know they want to spend using this key and the time lock and they need to find where this key is in the tree, where the time lock is, and need to set everything up correctly.
So one thing that's going to come with the new BDK is this thing which we call the planning module, which is basically a bunch of code that you can use to plan how you're going to spend ahead of time.
So you're going to provide to the planning module what we call assets.
You can say I have this assets available, which means I have this key available so I can produce signatures with this key and another asset is I'm willing to wait so you can use time locks as well.
And then the planning module will figure out the optimal cheapest way to spend given the assets available if there is any.
And so with this planning module it's going to be much easier for the user to say, oh, I have this key available.
And I could show you on your mobile device a view where you say, this other wallet is available, this one, kind of, but I prefer not to use it.
And so the planning module can figure out and say, oh, yeah, you can spend just using this key if you wait a little bit and you can kind of interactively construct a plan to spend and then you can construct a transaction using the plan so it will set the write and sequence and lock time and everything.
So yeah, that's another thing that's coming.

Daniela Brozzoni: 00:29:45

Yeah, I'm pretty hyped about that as well.
So basically for using that, we have to basically rewrite the transaction builder API, because instead of building a transaction just saying, I want to use this policy, you have to provide assets, etcetera.
So that's what I'm working on right now.

Adam Jonas: 00:30:05

Thanks for coming.

Daniela Brozzoni: 00:30:06

Thank you for having us.

Alekos Filini: 00:30:08

Thanks.

Mark Erhardt: 00:30:19

So, I think I have a much better understanding on what I would use BDK for.
I think especially it's interesting to build a library around the use of descriptors with a mini script and especially also multi-sig really being very palpable now.
The musig too, BIP has been merged now.
We are hearing that there will be a multi-sig hardware wallet coming out eventually.
So everything will happen eventually.

Adam Jonas: 00:30:48

Really? It would happen eventually?

Mark Erhardt: 00:30:50

Well, it's starting to look more ready than it used to.
So I think there's quite the charm of having this generic descriptor-based approach.
I think more people should look at BDK.

Adam Jonas: 00:31:04

All right, you heard it here first.
Check out BDK, but in the meantime, thanks for listening.

Mark Erhardt: 00:31:09

Bye.