---
title: 'Lightning Dev Kit: Making Lightning More Accessible to Developers'
transcript_by: ttiiggss via review.btctranscripts.com
media: https://www.youtube.com/watch?v=W-ajI5YleIo
tags:
  - lightning
  - career
speakers:
  - Matt Corallo
date: 2021-11-05
---
## Introduction

So, I worked on Bitcoin Core for many many years, but I am not here to talk about that!  I now spend my time, full time at Square Crypto working on a project we call the Lightning  Dev Kit (LDK).  So, working to enable Lightning to be more accessible to developers and I'm here to talk about that and give the lay of the land for why it exists, what the state of the Lightning ecosystem is broadly, and why we think it's an important project and why Square is funding us, to work on it.

## Quick History

So in order to get into why Lightning Dev Kit and why better developer tooling around  Lightning in the specific model that we have is important, we first have to kind of cover  what exists in Lightning today.

* **What is the state of the Lightning ecosystem?**
* **What projects can you use to interact with the Lightning network?**

So everyone probably here knows [LND](https://github.com/lightningnetwork/lnd) and [C Lightning](https://corelightning.org/), the kind of two I would say by  far most popular, uh Lightning routing nodes. Certainly for large scale Lightning.  They're great.  They run on your Raspberry Pi or on a big server, if you have a lot of channels; you probably want to do that.  They have an RPC (Remote Procedure Call) interface.  They're like a fairly monolithic daemon. You know, they're like a program you run.

I think C Lightning is maybe a little less monolithic, but then of course relies a little more on standard operating system features, in Linux and other operating systems.  And so it was really designed to run on a server, on something that has to be online 24/7, because that's kind of a basic requirement for Lightning.

So that's kind of how they came at Lightning from day one, right? C Lightning and LND were around basically on day one when Lightning was being invented.  They came at it and said, well, we need this thing that's going to be online 24/7, so we're just going to build it and target servers, because like, mobile... is weird on Lightning and whatever and so they built this really great *thing* that you run; but it is... really just targeted at that specific runtime, right? So it has SQL (Structured Query Language), fairly monolithic.

## More recent Lightning implementations

More recently we have a few other Lightning implementations that have gotten a little more popular. Obviously [Electrum](https://electrum.org) now has a built-in Lightning implementation.  They spent many years writing from scratch a Lightning implementation to integrate with:

1) Existing on-chain logic
2) Existing thing that downloads the blockchain
3) Key generation

All that good stuff.  Of course, it's fairly tightly integrated with Electrum, the wallet, right?  It's written in Python, it's written to integrate with the existing system of the Electrum wallet.

There's also [Eclair](https://github.com/ACINQ/eclair) which is similar to C-Lightning in terms of it being targeted largely at server-side platforms, although they do have some, forks of it, which they now run as [Phoenix](https://phoenix.acinq.co/) on mobile clients. Again, it's still a fairly monolithic thing that is targeted at specifically, their deployment. And so the *theme* of all of this, these are kinda the ways you go interact with the Lightning network. The *theme* of all of this is, well, they're programs you run and you interact with them.

They're not things that you can use to integrate Lightning into your application.  Right, so if you want to actually build a new mobile wallet that supports Lightning, well, none of these are really going to do it for you...  you can build off of them, you could take LND and just let LND do **all** of the work, including sync the chain and have an on-chain wallet, all that good stuff, but it works the way it works and there's not a lot of flexibility there.

Or you could go the route that Electrum did and spend multiple engineers, multiple years to build a custom from-scratch Lightning implementation. But, we think neither of these are really good answers for someone who wants to build a Lightning, especially on mobile, application.  The future of getting good user experience (UX) in Lightning and I think across Bitcoin is enabling developers to build new and creative options for how you interact with these networks.  There's not a lot today, in terms of ability to do that, but as we add better tooling and make that an easier thing for developers to do, we can have a lot more experimentation and because Lightning is this fairly early system today, we need that experimentation to grow it and to enable really slick user experiences.

## Lightning Dev Kit

So we think that's kind of where LDK (Lightning Dev Kit) comes in.  We're not interested in competing with LND or C Lightning or Eclair or Electrum or whatever.  They're really good at what they do, but we think they only do very specific things.  So, we're targeting, especially like I was saying, existing mobile wallets or new mobile wallets, but especially existing ones.

Right, If you are someone like Blockstream Green Wallet or whatever, you are an existing mobile Bitcoin wallet, you have on-chain support, you've already written all of this logic to  sync the blockchain, to generate keys, to process transactions, and you've hooked that up to your UI (User Interface) and all this great stuff.  ***How*** do you add Lightning?  Well, if you use one of the existing solutions insofar as they even work on mobile, they are going to download the chain again. So you're going to download the chain twice and your phone's going to get really hot.  Or they're going to also have their own on-chain wallet, so maybe you're going to create an extra on-chain transaction to move from the old wallet to the Lightning part of the on-chain  wallet and then you're going to open a channel and that's a... mess.

So we think that's a really important avenue that needs to be solved by the Lightning community is that there's not a good answer for these people. Of course, also, more interesting mobile experiences going forward is also something that isn't, doesn't have a great answer. So if you take LND or C Lightning or something like that, I'm going to keep picking on them, maybe they have, I know C Lightning does, I think LND might soon have a generic SQL backing.  So you can use any generic SQL database for your storage, SQLite or something if you want  to do it locally.

But let's say, and we've chatted with a few mobile wallets who want to do live synchronization  of the Lightning state onto a server, encrypted obviously, so that you can just close your Lightning wallet and open it on a new device and you can pick up where you left off and you don't have to worry about it being out of sync or something. Or let's say you want to have live backup so that you always have the latest state on  a server in the cloud somewhere, again, encrypted, of course, but so that you don't have to worry about losing your phone and, oh, well, you can only get the you know; non-HTLC (Hashed Timelock Contracts) encumbered parts of your balances and some parts of your balances might be lost because you don't have the latest state and you need **that** to recover.

These are things that you need a very flexible API in order to support. Finally, one of our last kind of target markets, which may be a little less interesting to this audience, although I don't know exactly; is kind of more custom enterprise back ends. So if you're a cryptocurrency company, you're probably already kind of built around this concept of taking a node, running it in Docker or some VM (Virtual Machine) service and then interacting it  with RPC because that's how basically everything in cryptocurrency works, and especially if  you're one of these various cryptocurrency exchanges that offers the shitcoin casino for everyone. You're certainly built around scaling up the number of random garbage coins you support, and then you're going to be built around this kind of architecture.

And so LND and C Lightning fit super, super well into this architecture and you should  totally use those if this is the architecture you're set up around. *But* if you are a corporate who has more infrastructure on the back-end, you know, if you're someone like Google, you are not set up around that. You have all kinds of custom stacks for basically everything you can name that's running on the server is completely custom and you want to actually integrate with this existing infrastructure that you have in a much tighter way. So again, this is something where if you just take an existing Lightning product off the shelf and you know, maybe you use a plugin to switch the SQL back-end for it, that's still not going to get you where you want to be.

It's usable, it might work well, but it's not quite the kind of tight integration you might want.

So this might give you a rough idea of what LDK is. So LDK

* Is a generic library that does all of the hard work for you in terms of implementing Lightning
* All of the protocol state machine
* All of the on-chain enforcement so it knows how to create transactions
* If your counter-party misbehaves, it can punish them and do all of the on-chain enforcement required for that.

But what it doesn't do is *it* doesn't have an RPC interface.  It's not designed to run as a daemon.  It doesn't spawn its own threads.  It just does what you tell it to do.  It's just a shared library, callable in C, but we have interfaces in Java and Swift and it's actually written in Rust. So it is callable for many of these languages, but it's just a library that you would interact with like any other library in your native language. And yeah, so as I mentioned, it's written in Rust. It's basically derived from the Rust Lightning project.  It has all these language bindings, but we had to write from scratch our own language bindings generation logic. Turns out basically every language binding generation logic out there is not designed around a kinda fully featured object-oriented interface. So we actually had to write our own and spent probably a full year doing that.

But so now we have language bindings in various languages.  We have, we can add more languages as users want. So if we have people who want to use certain languages, we can add those languages. We kind of have C and C++ support, so if people want that, we can fix that up as well.

So because it is a very lightweight library, so it's designed to scale kind of as you want right? So it works really great on mobile if you want to run a single thread and run everything  in that thread, it does fine with that.  Or if you want to run it on a 20-core machine and spawn 20 threads, it's also designed to parallelize basically as much as you want it to. So it's really kind of scalable across that entire range. Just depends on exactly how you want to integrate it, you're going to get very different scalability properties there.

## Application Programming Interface Usage

But everything is an API (Application Programming Interface), right?  So it doesn't do its own interaction with the OS (Operating System), so disk access, so storing all of that great lightning state is just an API. It doesn't actually call to the disk itself. It can, there's some options that you can kind of take off the shelf and run with that.  But if you want to instead call to the network instead of ever writing to the local disk, you can totally do that and we support that.

Network access is just an API.  So if you are an enterprise and you want to run the full lightning state machine on a device that doesn't have an IP stack and just connects to the outside world and shuffles lightning messages over, let's say, a RS232 modem, you can totally do that. And that might protect you from some types of attacks if you're really worried about these kind of online keys and you want to not have a full TCP (Transmission Control Protocol) stack on the device with all these keys with money in it. Seems like a reasonable thing to do.  And so we just have a generic plug-able interface for send bytes to the peer.  And same for messages as well.

So chain sync is also actually multiple different APIs you can use for providing chain data.  So we support providing full blocks or only headers.  We also support individual transaction connection that maps very well to the Electrum APIs. And so depending on what kind of API you either want to use or maybe already use for your blockchain sync, we already have an API that maps fairly well against anything you do for your blockchain sync and you can feed that blockchain data into LDK and then it will kind of do as required to keep the lightning state machine updated from that block data, you know, punish counter-parties, make sure the right state is on chain, all that kind of stuff.

So then the actual live state machine, which is fairly small, it's just the current state of all your channels, that is a separate module from historical enforcement.  Right, so if you're familiar with the watchtower model, there's several different watchtower models.  But that's easy to implement because they're just different objects and you can serialize them and move them around to different servers and do kind of whatever you want. You have the live state machine, which is small enough, it's not quite going to *fit* in a hardware wallet, but it's trivially small enough to fit on even a super ancient Android phone or something. You can keep that runtime super tiny and then actually do the on chain enforcement somewhere  else, depending on how you set up the key storage, you can do that on the device or elsewhere; and then we support remote signing through the lightning signer project, which is one of the teams we've given a grant to, that's also going to form the back end for C Lightning's new HSMD (HSM Daemon), so you can use the same code to sign for C-Lightning channels as for LDK channels and do offline actual lightning state machine enforcement and potentially even run that in a hardware wallet.

## The state of LDK

So hopefully there's at least one or two people who think maybe you want to build an app using this. So where are **we**?  We have a number of mainnet nodes, so we're very happy with how it works today and its stability and its performance. We think it's fairly feature complete in terms of everything you might need to run a lightning  node in a number of different configurations. And the first two kind of downstream users or really downstream applications that are being built around LDK, we're hoping to get them in production by the end of the year, but we'll see whether they both make it that quickly or whether they get delayed on other kind of decisions around how they want to integrate, how they want to build a user experience around lightning because, now they don't have to kind of worry about all of the details of the lightning state machine that LDK has kind of solved for them.

We have, so we're currently funded through Square, we have four full-time engineers working on LDK and we have several outside contributors, both, who are building apps based on LDK for new lightning nodes & also there's another company who's working on building an LDK based wallet who's contributed several engineers to work on LDK as well.  So external contributors are increasing and we'd *love* more external contributors if you  want to learn Rust or you want to learn Lightning or you want to learn both at the same time. We're very friendly to new people who don't know Rust.  All of us learned Rust on LDK so we would love more contributors. It's fairly, by code volume, it is significantly smaller than all of the other lightning implementations. Not necessarily by feature volume but once you cut out all that stuff like RPC interface, generic SQL back-end and all of these things and you just replace it with a generic API, suddenly you have a lot less code by total code volume and so it's a lot easier to kind of get into and start using and it also makes it a little more maintainable in our view.

We're also, you know, we would love more people to develop using it.  We're planning on as much as we have time being very high touch for anyone who wants to build an app around LDK. So far we've been, you know, we've had a lot of interest and a lot of people penciling it in for, you know, two or three quarters from now.  And so we've been working with, working fairly closely with some of our initial customers  in terms of helping them understand exactly how everything fits together and helping them build a good user experience around LDK.

## Call to arms

And so, you know, if you want to build an app using LDK, you want to build a really slick Lightning user experience or something a little more unique than exists today or you have some clever idea of how Lightning user experience should work, we'd love to work with you.  We'd love to be really, you know, hands on and help you out in any way we can. So get in touch!

And so, yeah.  So where are we going from here?  So we're, we kind of just got to the point that we're happy feature completeness wise.  And so this is of course resulted in us getting a little behind on some of the new lightning spec stuff. So things like BOLT 12 and offers and onion messages and all kinds of new channel types that are coming down the pipeline. So that's something that we're going to spend a bunch of time implementing, and also if anyone externally wants to really learn the guts of lightning protocol state machine, again, we'd love more external contributors.  There's a lot of opportunity right now to really kind of dig into real guts of lightning  and implement low level kind of next generation features.

## Conclusion

And also we're hiring.  So Square crypto itself has some headcount to we're not sure whether it's going to be 100% of new headcount on LDK or maybe some other projects.  But we are actually hiring for full time roles in addition to of course we have a very large grant program and love to fund whether it's any other Bitcoin project or also Bitcoin projects using LDK or BDK (Bitcoin Development Kit).  We love to fund that too.

So get in touch with us, if you want a grant.  Grants at [squarecrypto.org](https://squarecrypto.org) is always the right contact.  And then you can probably email there too if you want a job.  But I don't know if the right person will see it. I don't know.

But that's all I got.  So thank you!  And yeah, Thank you.
