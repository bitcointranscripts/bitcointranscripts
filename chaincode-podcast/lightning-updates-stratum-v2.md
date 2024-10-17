---
title: Lightning updates / Stratum V2
transcript_by: stackeduary via review.btctranscripts.com
media: https://podcasters.spotify.com/pod/show/chaincode/episodes/Steve-Lee-and-Lightning-updates--Stratum-V2---Episode-23-e1ofl4j
date: '2022-09-28'
tags:
  - lightning
  - zero-conf-channels
  - stratum-v2
speakers:
  - Steve Lee
episode: 23
aliases:
  - /chaincode-labs/chaincode-podcast/lightning-updates-stratum-v2/
---
Murch: 00:00:00

Hey Jonas.

Jonas: 00:00:00

Hey Murch.

Murch: 00:00:02

What are we up to?

Jonas: 00:00:03

We are back.

Murch: 00:00:04

Who are we recording today?

Jonas: 00:00:05

We have Steve Lee in the office this week.

Murch: 00:00:04

He is the head at Spiral.
He's done a lot of open source development.
He talks to a bunch of people.
He's also the PM for the LDK team.
So we're going to talk Lightning, the challenges that are open with Lightning, and maybe a little bit about other projects in the space.
And I want to touch a little on Taproot.

Jonas: 00:00:28

Yeah, totally.
We talked, again, not just about Lightning, but sort of waded into Stratum V2 and that new spec that's coming out and the project around there.
So, great way to get back into the swing of things.
We've been taking a little bit of a break here.

Jonas: 00:00:48

Welcome Steve.
Let's just sort of dive right into it.
So maybe we can start a little bit with where is LDK these days and what you're thinking about and then we can maybe move into more specific topics from there.

Steve: 00:01:01

Thanks for having me on.

Jonas: 00:01:02

Yeah.

Steve: 00:01:03

Great to see you guys this week.

## Lightning Dev Kit

Steve: 00:01:03

Let's start with LDK.
So the Spiral team and other contributors have been working on it now for about two and a half years.
Last year, in the spring of 2021, we got our first real adopter of it.
The LDK had matured enough to get ready for someone to adopt and BlueWallet to date had been non-custodial for on-chain but custodial for Lightning, and they wanted to move to non-custodial for Lightning.
They successfully integrated it on their iPhone app and their Android app by August of last year.
And it's actually in the App Store, but it's still not the default experience.
So I thought I'd share some lessons learned, like why isn't it the default experience yet.
The good news is, LDK worked exactly as the LDK contributors had planned, and it was great to have a first adopter be able to get it working.
But the biggest problem for BlueWallet is that the channel management is still manual.
Like an end user has to set up their channels, manage the liquidity, etc.
Wallets like Breeze and Moon and Phoenix have demonstrated that if you do that automatically, it's a much better user experience.
So I think one lesson learned for everyone in the Lightning space is that we need more LSPs, we need LSPs that are available for any wallet to integrate with, and we need an LSP spec.
And so, the good news there is that there are a lot of people working towards that, both the spec and commercial LSP services.

## Zero-conf Channels

Steve: 00:02:21

So that's one lesson.
There's a few other features that BlueWallet was hoping for out of LDK and we've delivered with them.
One is zero confirmation for Lightning channels and not only did LDK implement that, but it's actually part of the Lightning spec now and LND and CLN support that as well.
So that's an improvement in the past year.

Jonas: 00:02:39

That's really just on first use?

Steve: 00:02:41

Yeah, I mean, how it impacts the user experience is that if you're like onboarding a brand new user, you install the wallet, you can't receive money right away.
So to get, you need to inbound liquidity and a channel opened to you.
If you have to wait for six confirmations, wait an hour or so, not a great first time experience with an app or a product.
So zero-conf makes it instant.
And the trust model there is such that it's reasonable to take the risks of, I mean, zero-conf in general has security risks on Lightning and specifically with the relationship between a wallet and an LSP.
I think most people consider that a reasonable risk to take for the UX benefit.

Murch: 00:03:18

So the idea is that usually users first want to receive, not send?
And by having the Toribird[inaudible] channel, the LSP basically just trusts them for whatever amount they're going to receive.
But since the channel isn't confirmed yet, it's not really lost.
And if so, it's just pushed to the other side at the point when it gets confirmed.

Steve: 00:03:38

That's right.
And so that was one change they wanted to see that's been made.
So I think, you know, all wallets are gonna be able to take advantage of that moving forward.

## Rapid Gossip Sync

Steve: 00:03:46

Another was that the way that they initially implemented or integrated LDK into their wallet, they did the pathfinding, like finding a route to do a payment on the server still.
They weren't doing it on the phone.
They did it that way because of performance reasons, because one of the most resource-heavy activities in Lightning, in Lightning Protocol, is doing pathfinding.
You have to download the entire Lightning graph onto the phone.
And so a feature that the LDK project worked on in the past year was just announced within the past week or so called rapid gossip sync and let me actually first start by saying what's the problem with doing it on a server?
The problem with doing it on a server is whoever controls that server has all the payment data.
So you know a company that has thousands or millions of users, they have millions of users' entire payment history and which has obvious privacy implications.

Murch: 00:04:38

And not only that, they also control the routes, so they could, for example, take a route that earns more fees and things like that?

Steve: 00:04:44

Yeah, that's a good point.
You're trusting for that as well.
So now let me describe rapid gossip sync, which also actually has that drawback too, what Murch just mentioned.
With rapid gossip sync, it's intended to enable client-side, like in a phone, pathfinding in a performant way.
Right now the entire Lightning network graph is on the order of 60 megabytes.
So the problem with mobile development is you can't guarantee that your app can run in the background.
So ideally you could just download this data over time continuously in the background, but that's not possible.
So if a user hasn't opened your app for days or weeks or even months when they go to open it, it might take dozens of seconds or even, I've used some wallets that take minutes to sync before you can use it.
I'd call that a showstopper user experience for mainstream adoption.
With rapid gossip sync, what we've done is filter out a lot of the gossip protocol information that's not necessary for pathfinding and also compress it.
And we've been able to squeeze that 60 megabytes down to like two megabytes and measured it at like 0.4 seconds to download and process on the client to be able to do routing.
So we believe it will be performant enough that even if it's been like a month since you've opened the app, the user won't even notice that's happening and by the time they wanna send a payment, it just worked.
The one caveat is what Mark mentioned earlier, trusting the server to not withhold graph data.
So a trade-off here is that whatever server's serving up the rapid gossip sync, if it wanted to, like let's say it were being run by the LSP, it could selectively choose certain data withhold to optimize the routes going through nodes that it controls to maximize its fee revenue.
So that's a trade-off with it that exists as well even if you're doing in the cloud.
So I think what's important for Bitcoin and the deployment of this is have good reasons to trust the server that you're downloading it from and ideally it's independent from any money-making, Lightning infrastructure provider.

Murch: 00:06:34

When you do rapid gossip sync and you push basically a skeleton of the graph to the mobile phone, is there a way to backfill, pad the route between a receiver and the mobile phone that I just learned more about neighbors of my route or something like that?
There was a very early blog post by Rusty years ago where he talked about beacons for when the Lightning network gets immensely large.
Does something like that happen, or is that basically in there already because the skeleton prunes for the most important channels and routes and nodes?

Steve: 00:07:12

Well, just to be clear, so what rapid gossip sync does today, it is the entire network graph.
It just eliminates a bunch of data from the gossip protocol that's not necessary for that.
So it's not a subset of the graph.
Again, there could be a malicious server that prunes things out, but the way the code's written and the way it's intended to be run, it's the full graph, but it does remove like signatures and a bunch of unnecessary information so that the client can't prove to itself that it's the complete graph.
So that's the trust.

Murch: 00:07:42

Uh huh, I see, okay.

Steve: 00:07:44

Now in the future, so I mean, an open question is...if, yeah, the Lightning network grows a thousand fold over the day, is it still gonna be practical to download to the phone?
There's reasons to believe yes, but I mean, still to be determined.
But a lot of the information that's been eliminated to make it faster is literally redundant information.

Murch: 00:08:04

I see, I see.
Yeah, I miss it.

Steve: 00:08:05

And then another part about that too is it would be possible to use rapid gossip sync but also download all the gossip data, do both so that you can sort of check on the server that's serving that up to sort of police it.
That's gonna be a question of, or so to do a payment, you're not dependent on that, but to sort of double check its work, you could do that.
That's just a question of like, is it worth the bandwidth and what's that cost gonna be to the end user?

Murch: 00:08:29

Yeah, especially on a mobile.

Steve: 00:08:31

We'll have to see how that plays out.
I think it's really good to have this infrastructure in place, though, to be used.
But that was another request by BlueWallet, and I believe they're experimenting with it right now.
I know some other wallet developers, too, that are experimenting with it.
So I look forward to seeing actual performance data and actually trying out prototypes and real wallets using this to just confirm that it really is performant.
I think it will be based on our data so far, but it'll be nice to see the end user experience.

## How does LDK pick priorities?

Jonas: 00:08:55

So just as you think about your roadmap, a lot of this feature set is influenced by people who aren't able to use it in the way that you hoped they would use it?
Is that sort of the idea?
And how's it being informed on BlueWallet and whatever else?

Steve: 00:09:10

Yeah.
I'd say more generally, how does the LDK project pick its priorities, what it works on?
Two huge inputs.
One, you already mentioned, users.
And the users of LDK are other developers building apps and wallets.
So we certainly listen to all of our existing users.
We're also listening though to prospective users that have maybe looked at LDK and given feedback as to why they're not proceeding with it or what they want to see before they do.
I'll speak to that in more detail in a second.
We also, of course, it's compatible with the Lightning specification and protocol specification.
So, LDK contributors work with LND and CLN and Eclair and other Lightning protocol developers on both making sure that we're standard but also working on protocol improvements.
Like Lightning has a long ways to go to improve security and privacy and scaling in UX.
So we're working with other implementations as well.
That's the two big areas that influence what we work on.
Let me go a little deeper on what we've been hearing from mobile wallets that wanna use LDK.
BlueWallet, they did a great job of taking the LDK API, integrating it, so have other wallets as well.
But there's another category.

## LDK Lite

Steve: 00:10:10

What I've observed, developers who have experience with Lightning tend to understand the LDK API and use it, and they understand why they want to use it, and they make good use of it.
I think other developers who might have Bitcoin experience but haven't done Lightning yet might find LDK API to be a bit intimidating.
Either perception or reality or a mix of both, but I think the perception's definitely there, and it is a powerful API, and arguably a bit overwhelming if you're just learning Lightning.
So a sub-project within LDK that was undertaken a few months ago, tentatively named LDK Lite, although we're still trying to figure out how to refer to it, is really just intended to create a much simpler API for mobile wallet developers to get started.
But one that could be used in production and one that we think, you know, for those that aren't super familiar with LDK, it is not one instance of a Lightning node implementation.
It's a toolkit to allow you to build a Lightning Node.
And so it allows you to pick any recipe you want, which is super powerful.
But there happens to be one recipe for mobile that I think will satisfy many mobile wallets.
So we're going ahead and building that recipe to simplify the API down to pretty much like send and receive.
It's a little bit more complicated than send and receive, but sort of our aspiration is to make it as simple as send and receive.
And so that's being worked on right now and hopefully will be available within even weeks for early testing.
And I think that is going to be really well received by a lot of mobile wallet developers that I've spoken with to get them going much faster.
Then for some of them, they'll be able to launch a product with it.
Great.
Others will find that it just doesn't give them enough flexibility that they want and then they can use the more powerful LDK API.

Murch: 00:11:48

But it's a good stepping stone to get there and to familiarize yourself with the problems.
What's the interface?
Is it like broken down to the level of create invoice, receive payment, pay invoice and create invoice?
Or is it...?

Steve: 00:12:01

It's pretty much that simple.
I mean, it also includes like creation of channels, but the hope is to utilize LSP spec that's being built out so that even if a wallet developer wouldn't even have to like manually create their own channels, they could just use the LSP spec.
So even the wallet developer in that case wouldn't be doing all of the channel management work.
Also probably like you know a transaction history or payment history API call to get that data.

## Will LSPs be needed forever?

Murch: 00:12:25

Right.
You've been mentioning LSP's Lightning Service Providers a lot.
Would you say it's accurate that as a mobile wallet, you basically are always contingent on a service provider because most nodes will not want to have a channel with you?
As a mobile client, you're offline most of the time.
Is that still the case or is there something in the future that will change that?

Steve: 00:12:47

No, I think that's the case, you know, for both the offline concern that you mentioned and also just, you know, mainstream users I don't think are gonna wanna manage their own channels.
That feels much more like a hobbyist or someone running a small Lightning routing business kind of interface.

Jonas: 00:13:03

But that couldn't be simplified as in there's, you know, there's, there's optimization around the edges for something like that, as in your home node could be providing those services for you.
And then you're using, I mean, the ride, the Lightning, Zeus sort of family of remote control kind of way.

Steve: 00:13:18

Yeah, so that's all true.
So I don't think there's not one solution that any of us could say that's going to be for everyone.
I'm bullish on the Umbrels and MyNodes and running a small server at home.
I'm actually bullish on that.
But today it's very much a hobbyist environment.
But I think that can become mainstream.
But let's define mainstream.
Like think like a home run success over the next five to eight years would be 100 million people in the world having something like that.
Like basically, you know, a Bitcoin bank in their home.
I think the bill of materials for that gets down to like five or ten dollars, super cheap, and it gets integrated into other home device products that people buy.
So it's just a very simple experience.
But a home run success there is like 100 million people having that, which would be amazing.
That's not billions, that's not the world.
There'd be many people probably in emerging markets and stuff that aren't gonna have that at home.
So we also need to think about running a note on your phone as well.
And basically giving mobile phone users the most trust-minimized solution as we can.
I'd say that's the goal of Spiral and I think that the K Project.
So today it's true, there's several servers or services on servers that are needed to build out a wallet and a Lightning wallet, maybe like five or six different types of services that are needed on servers.
There's a roadmap and a path to keep eliminating those or reducing those and shifting the intelligence to the phone.
We just talked about one, rapid gossip sync is a way to shift not everything to the phone, but it does reduce trust because it's a privacy win.
LSPs and providing liquidity, I think it's going to be hard, except for the home node case to do.
So what's important is having a spec, having lots of alternatives.
And ultimately, I imagine a wallet developer will connect to multiple LSPs so that the wallet doesn't become dependent on one LSP.
And some wallets might have an interface that even exposes that to the end user so the end user can choose their LSPs as well.
So reducing switching costs and making that very frictionless, I think it's important for Bitcoin.
Because we don't want to end up in a state when one company is the LSP.

## Validated Lightning Signer

Jonas: 00:15:19

Maybe moving on, the next topic would be, and I'll reference Paul Erdős' Three Hats Problem blog post, which he talks about the sysadmin just having too many responsibilities and too much power.
And so he does point to the validated Lightning signer as a possible solution there.
And that's something you've been pretty involved with.
So can you tell us more about, yeah, what's going on there?

Steve: 00:15:41

Yeah, I'll talk about the project and just some of the, I just keep learning more and more about this project, its potential applicability, so I'm happy to share what I've been learning.
There's a project called Validating Lightning Signer, VLS.
Spiral has been funding it.
We're on year three now, so a little over two years we've been funding this project.
Two developers, Ken Sedgwick and Devrandom, who have both been in the Bitcoin space for a long time, they applied for a grant a little over two years ago, and the premise of their project made a lot of sense to me.
And the premise of VLS is that we want to improve security, and because Lightning introduces more security threats than on-chain Bitcoin because you need to have your keys connected on a computer that's connected to the internet, how can we mitigate those risks?
And certainly one way is to separate the keys and signing from the rest of the Lightning node and everything else you might be running on that server to produce the attack surface.
So I think some folks have maybe thought that it's as simple as just putting the keys on a separate computer and signing, but that would be blind signing, which I believe is a showstopper.
It's just simply not there.

Murch: 00:16:49

There's no benefit there.
If it blindly signs everything, then it might as well be part of the signing software.

Steve: 00:16:55

Yeah, because the node that's sending the transactions for it to sign can just send old states and the unintended recipient, et cetera.
So there needs to be a smart signer, and part of that intelligence is that it needs to run a mini Lightning state machine, and it needs to understand the Lightning protocol, and that's what VLS is.
So it is another implementation of Lightning, but it doesn't implement the peer-to-peer aspects or pathfinding routing.
Most of the components of Lightning, it does not implement.
What it does implement is signing transactions and keeping track of the state of all the channels.

Murch: 00:17:32

Basically, it solves a standard problem that we have in wallet service businesses, where you want to disintermediate the signing power from other processes in the business.
And you would especially like to lock up the keys in something where they can't be extracted, but you need a way to lock down a very small, minimal interface so that it actually only signs the things that it's supposed to.
So you need something that is able to check the policies or some sort of core set of rules that determines whether or not it should sign.

Steve: 00:18:03

That's exactly right.
That project is implemented on the order of a couple dozen policies.
So like you just said, so there's the notion of setting policies, policy enforcement, and whoever deploys the VLS project can configure that.
You also alluded to putting on a machine where it's difficult to extract the keys, so it's intended to run on HSMs as well.
Like, it can run on regular computers.
VLS is quite very compact.
It's written in Rust, and it has a very small footprint.
So it's intended to run in all kinds of environments, anywhere from like enterprise server equipment, enterprise HSMs,
but it can also run on mobile phones, and it can also run on hardware wallets and embedded systems, where the requirements are around like 500k of base.

Murch: 00:18:48

So just to repeat and rephrase, HSMs are hardware security modules, which are hardware devices that have this very minimal interface, where you, for example, just can ask, sign this, but you can't ask, give me the key.
And the key lives inside of the hardware security module and nobody has access, not even the sysadmin.
And then basically VLS is an operating system to run an HSM.

Steve: 00:19:12

Yep.
So let's talk about a few applications.
So the one we've been speaking about is like enterprise.
And so what this can enable is you can have an access control that's different for your primary infrastructure and then a different set for these keys.
And so your IT admin is gonna have access to most of the system, but they don't need to have access to the HSM running VLS and the keys.
That could be the CEO or CFO or some designated group that's different.
That's clearly one application.
Another is Blockstream has a product called Greenlight, and one configuration with Greenlight is to enable mobile wallets and for non-custodial mobile wallets.
To be non-custodial, the key has to be on the phone.
And like we just talked about, there needs to be secure signing, not blind signing for it to be actually secure and actually non-custodial.
So Blockstream is using VLS as part of their Greenlight solution, and I'm super happy that they're super supportive of the project as well.
Any project that Spiral funds, we obviously think it's a good idea for the space, but we also love to see others funding it as well, so that there's a good diversity of funding.
I think in the case of, you mentioned Paul and his company wrote a blog post recently about VLS.
I think they're interested in a couple of different use cases.
One is in the enterprise separating the keys like we talked about, but they'd also are envisioning a world in which their end users have a very small, cheap hardware device, which they're building, which can run VLS on it, so that their end users, like the stack work users, are able to have a non-custodial wallet.

Murch: 00:20:44

Essentially what this does is, so for on-chain transactions we have hardware signers or hardware wallets.
What VLS allows you to do is to essentially have a hardware signer for Lightning, which was notoriously difficult before because Lightning has so much more state and different things it needs to do.
It's not just a small transaction that you sign.

Steve: 00:21:05

Yep.
That's right.

Murch: 00:21:06

And Paul had a prototype in this blog post.
Have you heard more about that since it's been a few weeks, months?

Steve: 00:21:12

Oh, no update in the past few weeks, but yeah, I'm excited.
I really liked their company and he has tons of great ideas, so I hope they're successful.
I guess maybe the last thing I'd say about the VLS project and I continue to learn more and more about its applicability and here's an example.
So to date, Lightning has always only supported single signature wallets, meaning like if Mark and I have a channel together, we can only use a single signature wallet for each end of our channel.
But there's work being done right now to make it so that multisig can be enabled.
First step of course is getting Taproot implemented and activated in the network.
That was done late last year.
And now the Lightning implementations are starting to integrate.
There's a number of different ways to improve Lightning because of Taproot and LND and CLN and LDK and Eclair are all making changes now to support Taproot, including MuSig2, which will enable N-of-N wallets.
And then there's a protocol called FROST, which will enable threshold signatures on Taproot and, in this case, on Lightning.
So for example, you could have a 2-of-3 wallet that's not only your 2-of-3 wallet for on-chain funds, but also Lightning channels.
So that's super exciting.
We can go deeper on that too.
I think it's really exciting but let me just link it back to VLS.
If you fast forward to this future where you have a 2-of-3 wallet on Lightning, there's three keys, three separate computers of those keys, and if you want to receive or send money, you need to have two signers.
Only one of those can be your full Lightning node.
So how does the other signer securely sign without trusting the other key?
Well, it needs to be running VLS, or it needs to be running something like VLS, but there's really no other project that does that today.
So another really cool application, and frankly, just necessary application of VLS, is any kind of multisig Lightning channel.

## FROST and ROAST

Jonas: 00:23:01

I was just quickly looking up ROAST versus FROST.

Steve: 00:23:04

They're very similar.
ROAST is necessary if you want a lot of keys and signers.
So there's some applications where perhaps like Fedimint where you might want a hundred keys or a hundred signers like a hundred out of a hundred and fifty or something and FROST would have performance, not really performance, I mean, it's kind of performance issues, but denial of service attacks would be problematic because with FROST, if just one of the signers goes offline, you have to start over.
It's an interactive signing process.
With ROAST, it addresses that.

Jonas: 00:23:35

It's async.

Steve: 00:23:35

So for like a two or three wallet, FROST should be perfectly suitable.

Jonas: 00:23:40

And there's other applications for FROST as well.

Steve: 00:23:43

Yeah, I'm really excited about FROST.
So I mean, not only does it give you, you know, beautiful multisig, threshold multisig, and on your on-chain footprint is only one key and one signature, it also allows much better recovery options for a wallet.

## Recovering a FROST wallet

Steve: 00:24:00

So let's imagine you have a 2-of-3 wallet and Block is building out a non-custodial wallet and their product conception they're gonna have a key on a server a key on a hardware device and control the customer and a key on the customer's phone. Something that most everyone does is lose your phone.
So if you have a two, three wallet, you lose your phone and one of the keys is on the phone.
What do you do?
How do you recover?
The traditional way is you rotate your keys and you basically create a new wallet.
You sweep all the funds into the new wallet, you know, but that's a bit of a hassle.
It takes time and it costs money too.

Murch: 00:24:32

It also reduces your privacy.
It's horrible.
You combine all your funds.

Steve: 00:24:36

And then you add in Lightning.
So if you have a wallet that's both on-chain and Lightning, you're having to close all your channels, re-opening them.
And today that might cost a few dollars, but in the future that could cost dozens of dollars or more.
So I mean you might spend $50 on your hardware wallet and then like you lose your phone and you're spending another $70 just to rotate the keys.
Getting back to FROST, a really beautiful thing about FROST is that you can rotate the keys with no on-chain footprint, no on-chain transaction.

Murch: 00:25:04

You can reconstitute the threshold quorum.

Steve: 00:25:06

Right.
Using two of three as an example and losing your phone, you can take the other two keys, the secret shares and FROST, and produce a new set of three.
Now the security consideration is you have to securely delete the two original keys.

Jonas: 00:25:22

Toxic waste.

Steve: 00:25:24

Toxic waste.
If you don't, then you know the attacker or and if you lose your phone I mean you might have lost your phone or it might have been stolen right but if someone were able to get that key and if one of the other two original keys are obtained, you'd be in trouble.
So you need to be confident that the original two keys are deleted.
So I think there's gonna be certain products where that's a reasonable assumption and other situations where it's not.
If you've got three individuals involved where each have a key and there's not a lot of trust between them or just minimal trust then that's probably not a good idea to trust that the other two co-signers deleted their old shares.
But if you have a product in which the software is written by one wallet author and you're the only individual, that seems like a reasonable trade-off to me.
And it gives you the benefit of much faster, simpler, cheaper replacement keys.

## Taproot adoption

Murch: 00:26:18

Now it sounds like that would be a really nice wallet, but it would only make sense if it only launched with Taproot outputs.
You wouldn't want to go back to older output, less capable output types.
Is there a holdup with that?

Steve: 00:26:32

Yeah, that's a great question.
And for people familiar with when SegWit was activated, it took years for SegWit adoption to occur.
People actually receiving with the SegWit, and then specifically native SegWit receiving deposits and spending.
We're seeing a similar dynamic with Taproot.
Taproot was activated last fall.
If you look on chain, it's very little usage.
Some pundits on Twitter are mocking it, making fun of it.
I remain quite bullish.
I think there's very clear user wins in the future, but it takes a long time.
And what actually one sort of chicken-and-egg problem right now is if you have a wallet that wants to take advantage of the features we just mentioned, it needs all of the money received to be Taproot enabled.
So when you're depositing funds into this wallet, you can't use a legacy address.
If you do, you can't use FROST and you can't use these features.
If a wallet were to launch today and only receive Taproot, the big problem is that there's many exchanges that don't yet support sending to a Taproot address.
The address format is called Bech32m.
And with like,

Jonas: 00:27:39

I think that's probably contested at this point, but it's certainly possible that it's pronounced that way.

Steve: 00:27:45

Some people possibly on this podcast say Besh32m.

Murch: 00:27:49

You know, Peter has an IPA description of how it's pronounced.

Steve: 00:27:53

But however it is pronounced...I mean, it's...those familiar with SegWit and Bech32, original intention of Bech32 was that it would be forward compatible with Taproot or any other future SegWit version.
Unfortunately, a very remote isolated bug was found.
It was important to fix though, and that was fixed.
And that's what Bech32m is.
Now, what that means for wallets and exchanges is a very simple change.
It's a few lines of code for them to be able to recognize a Bech32m address and send to it.
I think the most important message here for wallets and services in the space, if you hear clamoring for supporting Taproot, step one is very simple.
It's just a few lines of code change and you only need to support sending to Bech32m to really unlock the rest of the ecosystem to do innovation.
Later, you can support receiving this and adding Taproot and FROST features, you know, but that's the prerogative of each service.

Murch: 00:28:50

Yeah, I mean, when you adapt receiving to pay-to-Taproot outputs yourselves, it's totally up to you, but if you support sending to Bech32m addresses, it would just help everybody else to be able to move forward and have these cool things.
And we know already that almost all Lightning projects are working on getting paid to Taproot channels.
If you want to fund Lightning channels, you'll have to be able to send to pay to Taproot.
If you want to send to users of these new wallets, if you want to enable your people to withdraw, you'll have to be able to send to Taproot.
And even the critics agree that Taproot will be useful down the road.
But it's like this two line code change.
So if you did now or do it then when you actually are forced to.

Jonas: 00:29:33

So someone willing to take the hidden fees and just create a service that just takes all the addresses and turn it into a commit?

Steve: 00:29:40

I know of folks that have been exploring that and there's a couple ways to, a forwarding service almost, and there's a couple of approaches.
One would be this sort of like semi-custodial or temporarily custodial service, which I think is what you were just describing.
There's a variation of it that's purely non-custodial as well, puts a little bit more onus on the end user and their wallet.
It's almost your wallet would receive the legacy, or you know, funds at the legacy address.
Those funds would be like in a holding pattern, and then the end user would have to like, hit a button to approve to sweep them into Taproot addresses, or maybe it happens automatically for them, but then they'd become sort of used, all of the wallet's features would become usable once the funds are in that.

Murch: 00:30:21

I think another signal that people that are interested in moving Taproot forward can provide is if you just move more of your funds into Taproot addresses already, you're sending a signal that it has been used and that people should get ready to be able to send it.

Steve: 00:30:36

Also a rumor has it people are working on a website which will have all the information needed to upgrade sending to Bech32m.

Jonas: 00:30:43

That's what this podcast is all about, spreading rumors.

Murch: 00:30:46

Yeah, you must be well connected to hear such rumors already.

## Future of the Lightning Network

Jonas: 00:30:49

You've been working on Lightning now for 2+ years and I think the big criticism of Lightning is there are certainly lots of things to polish up, but there are also some problems that we just don't really have any ideas of how to solve.
And so now that you've been steeped in this world for the last couple of years, how do you feel about the way things are progressing?
What's actually needed?
What kinds of expertise and skills that we need to add to the ecosystem, etc.?

Steve: 00:31:13

I remain very bullish and optimistic about Lightning.
Those that might be concerned, you just need to have patience.
There's a lot of known problems.
Like if you look at the user experience, you create a list of all the known problems.
But what heartens me is that for nearly all of those problems, there's a credible known solution and many of them are actively being worked on.
The reason it takes so long though, is that first you have to change the Lightning specification and you have to define that, so that takes a period of time.
Then you need to update the Lightning implementations, that takes a period of time.
Then you need to update all the wallets that use those Lightning implementations.
So most important changes are a multi-year effort, not too dissimilar from on-chain Bitcoin, maybe a little bit faster, but it is a multi-year effort.
So I'm very bullish.
If you look at all the problems around user experience, security, and privacy, I think there's pretty credible solutions that are going to happen for all of that.
Scaling is the one that in my mind remains unsolved.
And when I say scaling, I think Lightning is going to deliver two to three orders of magnitude more scaling over on-chain Bitcoin.
Like we'll achieve that.
But to extend that to billions of people around the world and maybe like machine to machine interactions and a million payments per second type of scale.
I don't see the technology roadmap to achieve that today.
That doesn't mean it can't occur, but I still remain optimistic even with that being a problem because number one, there could be technological breakthroughs that allow the sharing of UTXOs with really good properties.
Or maybe we entertain the block size debate again in the future.
Or even if neither of those pan out, there are many complementary Layer 2 technologies such as Fediment and even just full-blown custodial payment systems that can all complement each other.

Murch: 00:32:53

I think originally this problem was stated as Lightning scales payments but does not scale users because users still need channels.
And I think we can restate it a little bit in Lightning does not scale channels and channels if we can make them be usable by many different users we can still scale users even though each channel needs a UTXO.

Steve: 00:33:13

Yeah I agree with that and so the scaling thing I think that's a luxury problem that we hope to have in five years in the sense that let's fix all the other known things.
And then if the only problem we're left with at that point is scaling, then I think other options will develop.

Murch: 00:33:28

It also feels like a classical problem like the internet.
Back then we had dial-up and today we're like, oh my internet's a little slow today but I'm downloading a 4k movie and upstreaming data through a server and stuff like that.
It's just something that we can continue to fail at fully solving for a long time and fail at it better and better.

Steve: 00:33:49

I think Jonas also asked about how can people get involved or where help is needed.
Like Spiral itself grew from four full-time engineers to seven that are working on LDK.
I know Blockstream has been hiring a lot of developers on CLN.
So seeing an increase in a ramp up of protocol developers and implementations, super important.
There's also many dozens of wallets that are in development that are Lightning-enabled Bitcoin wallets.
So because they're in development, it's probably not broadly known that a lot of these are happening.
But, you know, I think over the next few years, we're going to see more and more of those launch.
And it'll be exciting to see many different recipes out there to see what's usable, what's not, what gets traction, what doesn't.

## Stratum V2

Steve: 00:34:25

Maybe we could give a few minutes to Stratum V2.
For folks that are not familiar with what Stratum is, this is, we're switching a new topic on Bitcoin, mining.
So in the mining space there's a protocol between mining pools and miners that's called Stratum.
It's been around for about a decade, you know, it's a protocol predominantly used in the space.
It certainly has gotten the job done.
There's been a lot of mining and billions of dollars earned the past 10 years, but as you can guess with something that was sort of hacked together 10 years ago, people have observed ways to improve it.
So for those following along maybe like four years ago or so, you might have heard Matt Corallo defining something called BetterHash and Jan and Pavel from Braiins working on Stratum V2.
The three of them got together about three years ago to merge their ideas into one proposed protocol, and that's what's referred to as Stratum V2.
About a couple years ago, Spiral funded a developer, Fi3, to start implementing this.
Because what's existed the past few years is that Braiins, as a company, they support Stratum V2 in their pool, in Slush Pool, and they have Stratum V2 firmware that can run on Bitmain miners.
So that's existed and there's some mining done today with that configuration, but there's not been an independent implementation or like a reference implementation of Stratum V2 for the space.
That's what Spiral started funding a couple of years ago.
So I'll give a quick update on where that specific project's at.
One, there's several funders of the project now.
In addition to Spiral, Galaxy is funding a developer for the project, and Foundry is also funding a developer for the project.
So it's great to have significant mining companies that are seeing the merits of Stratum V2 and funding it.
The project itself is healthy, has several developers, lots of good momentum.
And in fact, this fall, potentially within even weeks, there'll be several different pilot projects that will be done by some of the companies that I just mentioned and testing out some of the configurations because there's actually several different configurations for Stratum V2 because Stratum V2 can support existing equipment that's running Stratum V1 firmware.
You don't have to upgrade the firmware, but to do that, you need to run a Stratum V2 proxy that you, meaning the miner, would run that Stratum V2 proxy, which just simply translates the messages between that firmware and the pools.

Jonas: 00:36:46

And a lot of miners are already running proxies so it's not that crazy yet.

Steve: 00:36:50

It will be, it'll be an additional step, you know, step for miners.
So there's a couple reasons they would want to run this.
One is if they have Stratum V1 firmware equipment and they either can't or don't want to upgrade to Stratum V2 firmware, that's a reason they need to run the proxy.
Another reason to run a proxy or really just a server at their farm is if they want to do their own transaction selection.
And so That's, I mean, I didn't really speak to the benefits of Stratum V2, but I think the most impactful one and what Bitcoiners at large will really care about is that up until now, only the pools can do transaction selection.
And so Stratum V2 enables miners to do transaction selection or even another third party, which is something I just recently learned.
So another third party could run a future version of Bitcoind and then the pool nor the miner would actually be doing the transaction selection.
It would be up to that third party.

## OFAC and mining

Steve: 00:37:45

So it just provides a lot more configuration options and flexibility, which I think is important, not only for the sort of maybe obvious reasons for decentralization, there's orders of magnitude more miners than there are pools, but with some of the recently highlighted and emphasized censorship concerns, One reason I'm realizing that pools might want to adopt Stratum V2 is that perhaps they don't want to be selecting transactions.
It would actually reduce the pressure they face from regulatory bodies.
So that might lead to more rapid adoption of Stratum V2 by pools than I had anticipated.

Jonas: 00:38:19

Yeah, let's just sort of spell that out because I think that's a really important point and should be emphasized.
So, if there is a transaction that's on OFAC or an address that's on an OFAC list and that is sent through a US pool that starts to get very dicey for the pool.
And so we, you know, we...

Murch: 00:38:37

well, people are still debating the exact legal implications and all that.

Jonas: 00:38:42

Maybe, but if the pool is not in charge of those, that transaction selection, it makes it very clear.

Murch: 00:38:46

It makes it easier, but there is still..so pools generally are created to revenue sharing, and they're still paying people for mining a block that includes it, so there is several different facets and shades to this.
Definitely it'll get easier to explain if transaction selection happens at a different layer than the pool?

Steve: 00:39:05

Yeah, all evidence I've seen is that OFAC transactions have not been censored by pools or miners.

Jonas: 00:39:12

There was talk that Marathon was very explicit that they were going to do that.

Steve: 00:39:18

And they reversed that.

Jonas: 00:39:19

And now this is reversed.

Steve: 00:39:20

There's also open source tools that have been developed that have been monitoring this for at least a year and a half.
And based on that tool and that data set, there's been no censorship of OFAC transactions.
So I think that's good news.
And I'm not aware of the OFAC organization requesting that or asking that.
But nevertheless, for the future health of Bitcoin at that layer, it's best to have more options and more configurations.
And Stratum V2 definitely delivers that.
I guess to me what's exciting is three years ago I struggled to see exactly what the adoption path would be because I thought pools might resist.
Now I think that pools might welcome this.

## Other benefits over Stratum

Jonas: 00:39:59

I would say the other benefit we haven't mentioned is the encryption piece, which maybe you want to go into because that's...

Steve: 00:40:05

So Stratum V2 enables this transaction selection and being moved around, but it can still be done by the pools.
Orthogonal to that, other benefits are just simply one is just way better security.
Something that has been demonstrated by Matt Corallo is that you can relatively easily hijack hash rate.

Murch: 00:40:21

Yeah, BTP attacks.

Steve: 00:40:23

Yeah, because the Stratum protocol is used today, there's no authentication, no encryption.
So Stratum V2 just adds basic encryption and authentication.
So that's another benefit.
And again, miners can get that whether they're using Stratum V1 firmware or Stratum V2 firmware, it's very flexible and configurable in different ways.
Another change to Stratum V2 is it's just a more efficient protocol.
Stratum V1 uses JSON, it's super verbose.
Stratum V2 is binary, so it's much more compact.
Also with, I mentioned that the SV2 proxy that is software a miner can run, that proxy connects to each ASIC machine in the farm using what's called a standard channel and then use the group channel to speak to the pool.
So it's able to condense all of the channels that are basically all the traffic from all the machines that are farm into one channel that's much more efficient.
I'd like to see more benchmarking data, but my hope is that there's much more efficiency gains.
What it can enable in the future is mining operations that are in more remote regions that have worse internet connections that today would take a material hit to profitability and revenue because of latency concerns.
And if we can, you know, so if it is, I don't know what the numbers are, but let's say it's 10 times more efficient, all of a sudden, what might have been a material hit to the profits of a mining operation become negligible, and we'll see more decentralization through that mechanism as well.

Murch: 00:41:48

That sounds great.
Super.
Thank you for coming in.

Steve: 00:41:51

Thank you so much.

Jonas: 00:41:59

What did you think?

Murch: 00:42:01

Well, we entirely prepared too much.
He brought all the topics already in his mind.

Jonas: 00:42:04

I know.
That's all right.
He is thinking about Lightning very deeply, and I like the idea of a technical PM thinking about the user experience more in Lightning.

Murch: 00:42:13

I think it's also nice to get someone that has an overview because they talk to so many people.
And that way sort of compounds many different questions and challenges that different teams are working on.
And just him saying that all of these problems already have people working on them sounds really fun.

Jonas: 00:42:30

I think the optimism bled through, especially at the end there, which is heartening because a lot of times this is sort of a doomsday podcast, especially when it comes to Lightning, all the things that are broken.

Murch: 00:42:39

Sure.
And also with the current discourse on the interwebs, I think it's nice to have a long term perspective on things.

Jonas: 00:42:46

Sure. What's the current discourse on the interwebs?
I try to stay off as much as possible.
Lightning is broke.

Murch: 00:42:50

It's a failure.
It's around for seven years and not every human on earth uses it yet.

Jonas: 00:42:56

Yeah, you gotta stay off the Bcash forums, I guess.
We hope to do some more recordings soon.
Hopefully not every few months, but hopefully we'll get something out.

Murch: 00:43:04

Yeah, we'll have a few more people coming from New York soon, so let's record them.

Jonas: 00:43:08

All right. Hope you enjoyed it and we'll see you soon.

Murch: 00:43:10

Bye.
