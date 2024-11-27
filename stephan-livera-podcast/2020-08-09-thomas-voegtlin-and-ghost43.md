---
title: Electrum Wallet
transcript_by: Stephan Livera
speakers:
  - Thomas Voegtlin
  - Ghost43
date: 2020-08-09
media: https://stephanlivera.com/download-episode/2385/199.mp3
---
podcast: https://stephanlivera.com/episode/199/

Stephan Livera:

Thomas and Ghost43. Welcome back to the show.

Thomas V:

Hi, thank you.

Ghost43:

Hey Stephan, Thanks for having me.

Stephan Livera:

So welcome to the show guys. Now, Thomas, I know my listeners have already heard you on the prior episode, but Ghost, did you want to tell us a little bit about yourself, how you got into Bitcoin and how you got into developing with Electrum Wallet?

Ghost43:

Yeah, sure. I mean, I got into Bitcoin a few years ago because I had some personal bad experiences with the traditional financial system, I guess you could say. And then, I mean, first I only started using Bitcoin for doing a couple of donations, but then I found that actually, when I set up for cold storage and I’m full on using Bitcoin since then I’ve started contributing to electrum, I guess, almost three years ago now. At that point I had been using Electrum for a year or so already, I think, but that summer near the end of the summer 2017, I had a lot of free time and I decided I would fix a few bugs that had been nagging me. I mean that I’ve experienced as a user and first I’ve only been fixing a few things in my free time, but then I spent more and more time on it. And then it became a full time job basically. I mean, quite literally Thomas offered me a job back then, so since then I’ve been working for Electrum Technologies and I get paid to work on stuff that I love and with you is anyway, so, yeah.

Stephan Livera:

That’s great. And so today we’re going to chat a little bit more in detail about Electrum wallet 4, which is the new release. So Thomas, did you want to just tell us a little bit, I mean, our last interview was I think, towards the end of last year. And so there was a bit of a gap between versions 3.38 and version 4. Can you tell us a little bit about that?

Thomas V:

Yes, sure. Just to bounce back on what Ghost said, if you, if you want to work for Electrum, if you want to have a job it’s a very good idea to start by submitting pull requests. And then from there on you might actually end up being a full time developer. Yeah, that’s my 2 cents. So why was there such a big gap? Yeah, last time we talked about it on your podcast. I mentioned that we just merged the lightning branch into master and at that point so it means that we had code that was already fairly stable and but merging it into

Thomas V:

Triggered a lot of code reorganization because there are things that you cannot do when you work on two branches and you can only start doing them once you have the thing on the same branch. So since it’s a big change we did a lot of things that are, have to do with the code architecture and how things interact that couldn’t be done before we were working on a separate branch. Another thing is of course, that we had to test a lot of edge cases as people know with lightning. The difficulty is not, the happy path the happy execution path of things it’s when things go wrong. So this this involves a lot of testing and along the way, we added even more features that we were not planning in the first place. So this is also one of the reasons why it took so much time.

Stephan Livera:

Let’s talk a little bit about some of the new features that came in. So obviously lightning is the main, it’s probably the big thing. So can you tell us a little bit about how that came into Electrum and what were your experiences there? What were some of the hurdles, or what were some of the things that were difficult with putting lightning into Electrum?

Thomas V:

Oh, yeah, sure. But when I say new features, I mean, along lightning we added things such as a Watchtower or submarine swaps that were not planned initially, but that are nice to have too.

Ghost43:

Lightning is a metal feature. It’s like, there’s a reason we’ve been working on it for like two years or something.

Thomas V:

Yeah. It’s been a very long thing, a long process.

Stephan Livera:

So let’s talk a little a bit about the process then of setting it up. So I had a play around with lightning on Electrum just, you know, just to test it out, obviously. So I spent spun up a test wallet, put some, a small amount of sats in there. And then I noticed you’ve got that additional it’s like that additional tab there with the channels. And so you go into, I think, wallets information, and then you enable lightning on that wallet and then you can start the lightning part of it. So I noticed you, when you go to open a channel, there’s also a little suggest box there where it suggests a node to open the channel with. So can you tell us a little bit about that feature and how that suggestion works?

Thomas V:

Or in terms of GUI, things are not really finished or set in stone. I think what you said about how, how lightning is enabled, for example the feedback we have received from users shows or suggests that it might be a bit confusing because users do not expect to have to visit that dialogue in order to enable lightning. So I’m thinking that we might actually move that button into the channels tab. So yeah, the user interface is really that’s our first iteration. So we are going to change a few things there.

Ghost43:

Yeah. I mean, specifically about the wallet information dialogue thing to enable lightning, we made the decision as a temporary thing, as far as I recall that. I mean, we wanted to make it a bit more hidden. We didn’t want too many users to enable lightning at the same time, as soon as we release and then have more bug reports than we can handle.

Thomas V:

Yeah. That’s another part of it. That’s also the reason why we have not yet enabled the notification that there is a new version available as I’m planning to do it in the coming days. But that’s because I was also away from from my computer. So at the moment we want to slow things down because we receive more, bug reports than we can handle.

Stephan Livera:

So what was some of the early feedback on the new version of Electrum?

Ghost43:

Some users were confused and are still confused about the, I’m not talking about lightning here. I’m talking about the way you can, you have to do now coin selection, but it has to do with lighting because we wanted coin selection to be more generic, to be a usable with not just on chain transactions, but also when you open a channel or when you do a submarine swaps you want to be able to to select the coins in any context. So Ghost had this idea that I find really nice too, to have this this coin selection visible from all the tabs. And so that means that you have to do it in two steps, but it’s much more powerful because so yeah, that’s one thing. Another thing is of course in the send and receive tabs now we handle both on chain and lighting transactions. That means that requests are abstracted away from from whether they are on chain or lightning. And the fee, the on chain fee is decided after so these are the new, the things have confused some users.

Stephan Livera:

Yeah, that makes a bit of sense. So essentially when we are kind of switching between doing a Bitcoin on chain transaction, when we’re thinking in terms of sats per byte, and then when switching context now to doing a lightning transaction, well, it’s different, a different way it operates there. And so I also noticed that, yeah, as you mentioned, that there’s a few different little dialogues and things, so you’ve got like watchtowers and swaps aspects perhaps let’s talk about the swaps component. So I had a look in the dialogue and it looks like that’s going through Boltz exchange. So can you tell us a little bit about how the submarine swaps feature works there?

Thomas V:

Yeah, sure. It is not going through Boltz exchange. It’s a node that we are operating using the Boltz software. So that’s not exactly the same. It’s also a new business model for us because we are collecting the fees there. So we hope that is going in the future to develop as a new source of income. But yeah, if you are familiar with the Boltz exchange, the UI is very close. What we have done is we give a bit more freedom to the user in terms of selecting the fee. What, I mean, you cannot do that on the website of Boltz. So it’s a double edged sword because we give more power to the user, but it also implies that they can actually shoot themselves in the foot. Maybe more easily but in the end its not so dangerous because I mean if the transaction never gets minds, then you can yeah, you can cancel the whole thing.

Stephan Livera:

So let’s just back up one step there. So in terms of the submarine swap, could you just tell us what direction and what context it would work in? So let’s say I’ve just funded my wallet, is the idea that I would I can create a channel and then I can push some of that balance out of the lightning channel, receive it back on chain. And then now I’ve got more incoming capacity. Is that the idea?

Ghost43:

Yeah. That is the main use case. We have this issue that if you’re a merchant and you want to receive lightning funds you do not necessarily have a channel with incoming capacity. And initially I think we thought about creating a server that allows a little bit like a Bitrefill, you know, that I mean, they opened the channel to you for you, and that’s a service they charge for. So we thought about that. And then I found about this Boltz exchange software that is nice and easy to use, and it allows us to do so much more things than, than just a service that opens the channel. That for the user, it’s actually better to have two swaps because so yeah. Okay. This Submarine swaps is also known as a loop in loop out. If you, if you use the terminology of lightning labs, they also have the same service with a different name. But we call them swaps I’m sorry, I’m getting lost. I forgot the beginning of your question.

Stephan Livera:

Oh, yes. I was just clarifying which direction it was in. So in this case, it’s kind of like you’re, you just set up your channel or you can go both ways.

Thomas V:

And go both ways. So if you open the swaps dialogue you can actually click on the lightning icon and it will swap the lightning and Bitcoin icons. So you can either send on chain or you can send lightning. Yeah. You can also switch in the same way on the Boltz website. Actually.

Stephan Livera:

A quick example might be, let’s say you are a merchant, you’re taking a lot of payments. And then over time, those channels, all the balance is now sitting on your local side and now you need to push it back out. And that’s where you might use that swap.

Thomas V:

Yeah exactly, that allows you to keep receiving on the same channel. And that’s very good because the customers that have found the path to you are likely to find the same path again in the future. So if that channel gets exhausted, you, you probably want to rebalance it.

Stephan Livera:

Yeah. and now in terms of opening channels, so let’s say I open up my Electrum. I fund it with some Bitcoin. I try to open a channel. I was having a little bit of issues trying to manually open the channels to some of my own Bitcoin nodes. I was able to do it through a suggested one. So is there any difference there in terms of using the URI to pick which node, or I think the box currently says, alias, can you outline a little bit around that?

Thomas V:

Which box is this, sorry?

Stephan Livera:

When you open a channel and then you have to paste in the, like the pub key of the other person who you want to open the channel with.

Thomas V:

Yeah. So you can paste a remote node ID and a connection string. It’s the node ID plus the IP address and the port. If the node is already in your database, then you don’t need the full connection string, but sometimes it’s not going to be the case. So that’s why there are connection strings. And the suggest button will give you a nod that you are already connected with. So we know that this node is online.

Ghost43:

Yeah. I mean, the decisions button is very naive at the moment we are going to change it probably in the future, but at the moment, it just gives you one of the nodes. You already have a transport connection established with.

Stephan Livera:

Let’s talk a little bit about the watchtowers. So I guess for people who might’ve used another lightning wallet or lightning daemon, let’s say that they’re used to that daemon monitoring the chain to check for, if somebody is trying to cheat you, et cetera. Can you outline a little bit about how the Electrum watchtowers work and I see you’ve got two different models there.

Thomas V:

Yeah. Okay. Let me first say, okay. We, we developed this because I was thinking about the Watchtower as a business model for us. And the idea was that we were going to have a Watchtower as a service for our users. But I backed up because the requirements in the current model are too large. So currently the Watchtower implementation that we have is I mean, it’s okay for your own personal use, but we did not implement a user authentication system that would allow you to have a Watchtower with many, many users. So regarding yeah, you are asking about the different models. And that’s precisely the question. So you have, there is this idea that you could incentivize the Watchtower by giving them a share of the justice transaction, and you would not need to pay them.

Thomas V:

Other than that was one of the early ideas around watchtowers. I don’t know if anyone has ever actually implemented that kind of Watchtower because obviously you have you don’t have a good guarantees if you use this type of Watchtower because the Watchtower, so you have, you have strong anonymity, the Watchtower doesn’t need to know anything about you. But you don’t have the guarantee that they will keep watching your channel forever or for the lifecycle of your channel. So my suggestion was to have a Watchtower that knows you about, a few more things about your identity, so that it can so it knows about your channels and so that you can at trash the data when the channel is closed. And then you can save some disk space.

Thomas V:

And so the idea was to have a Watchtower that would charge not, it would not charge you for the justice transaction, but it would charge you for the action of watching. So you would need to have a subscription for that kind of service. But like I said, we did not develop this fully into a commercial service. So the code is open source. Someone else can actually use it to do that if they want. But at the moment we decided that we are not going to offer this as a service. So the Watchtower code is a useful if you, run your own private Watchtower, and you can do this. For example, if you have a machine that is always online, but you don’t want to have private keys on that machine typically if you have your own private Electrum server, it makes sense to also have a Watchtower on that.

Ghost43:

Yeah. I mean, regarding the question of there being two different, watch tower models, I guess, in the, in the current codes what’s well okay, so there’s the local and the remote Watchtower options and the remote, watchtower is what I guess a power user, when thought about watchtowers without compensation would think about I mean, that’s the remote Watchtower. So if you have multiple computers, for example, I mean, let’s say you have a server or an always online machine back at home. Then you could use the remote tower such that you run Electrum with the Watchtower options configured always online or almost always online on that machine. And then your other client sets as a remote Watchtower to connect to your home machine. And the other option, the local watchtower is such that well, I guess it’s kind of specific to Electrum. In that Electrum, you can have multiple wallets and I’m not sure whether this is actually true about any of the other current lightning wallets.

Ghost43:

So, I mean, if you open, if you create multiple wallets in Electrum, you can even open them at the same time simultaneously. And the enabling or disabling lightning is independent among the wallets. So you can enable lightning for I don’t know, two of your out of five of your wallets or whatever, and you can even open them at the same time. And then they will spin up independent lightning nodes with separate IDs and their own channels. And so this introduces a complication, or I guess several, but from the point of view of the Watchtower without the Watchtower, if you could, if you have lightning enabled in one of your electrum wallets, but you don’t have that Electrum wallet that open because let’s say I don’t know, you’ve created another one for your work funds or whatever, and you only have that one open and you’re using that one to do a few transactions.

Ghost43:

Then in case you let’s say your counter party cheated and breached one of your channels for your other electrum wallets, then you wouldn’t notice because, I mean, that’s a completely independent wallet. It’s separate lightning node. And to check for that, I mean, naively, you might even think that you might want private keys, let’s say, but in any case you have to have some kind of information and you have to have this wallet decrypted. But anyway, so the point is that if you enable a local Watchtower with Electrum, then we will save some information that doesn’t include private keys on your local disc, such that if any, wallet file is open with Electrum. If Electrum itself is running independent of what you are doing, then it will watch all of your wallets at the same time.

Stephan Livera:

Gotcha. Yeah.And so let’s say the user, sorry, go on Thomas.

Thomas V:

I just wanted to make one thing clear. I mean, it might not be obvious, but if you run a watchtower, well, you don’t need to run a lightning node is simply a daemon that watches the blockchain. And if a UTXO is spent then it broadcasts a transaction, so when you run a watchtower, it’s completely independent from when you’re running a lightning node.

Stephan Livera:

And so in this example, let’s say the user is just running Electrum wallet on their laptop, PC, and, you know, they opened up some channels and then later, you know, they closed their laptop for the day. And I guess, as I understand you, then it means, you know, let’s say they’ve gone to sleep and they only open their laptop again when they wake up in the morning. And I guess at that point, then the Watchtower, the local Watchtower, in that example, on the laptop running on that Electrum wallet would then pick up, Oh, okay. There’s been a transaction on the chain. I need to broadcast the justice transaction. Is that, is that how it would work there? Or where am I getting it wrong there?

Ghost43:

Yeah. I mean, the point of running a local machine is that you don’t need to have the wallet file decrypted, I guess that’s the most simplistic use case. Because I mean, you might have everything decrypted, the whole file and you need to enter your password to open it. Right. And you might have multiple wallets and without some kind of architecture, such as this local Watchtower, you would need to decrypt all of your wallets and have all of those checked for breaches.

Ghost43:

But we developed the local watchower so it’s enough to just start the application and don’t care about that. You don’t need to open all of your wallets.

Stephan Livera:

Because otherwise, yeah, you might have to sit there doing the five different passwords to your five different wallets, and then it just becomes a bit of a, right.

Thomas V:

You can even have the application run in the background without any wallet open, if you, I mean, there is a GUI preference for that. So in that case, the Watchtower will be active.

Stephan Livera:

Yeah. And so I suppose for users who are running an always on node, it might make sense for, let’s say the package node in a box. So, you know, things like myNode and nodl, and so on, RaspiBlitz, if they package in an Electrum server, it might make sense for them to also package in the Watchtower, the external Watchtower. And then, so that way it just kind of, it’s always running there.

Thomas V:

Yeah, absolutely.

Stephan Livera:

Around lightning as well. So obviously with lightning, because the channels, yeah. Just the importance of doing backups. Can you talk, can you talk to us a little bit about the use of static channel backups for Electrum lightning?

Thomas V:

Okay. So the backups that we have do not allow you to restore the channel. That’s a, I think that’s also the same with LND and yeah. So the only thing you can do with that kind of backup is to have the channel closed. So it should not be confused. I mean, yeah, there should be a different word than backup, but I don’t have one. So yeah the main point here is that if you, if you have a lightning channel the funds in your lightning channel cannot be recovered from your seed words. So in case you lose your device, or you have an accident you probably want to have a backup of your channels. Now currently we use a static remote key, and the static remote key that we use is actually one of the public keys of your wallet.

Thomas V:

That’s a feature that might not stay in the future because it won’t be possible anymore soon because of some changes in the lighting protocol. But that means that currently you have this extra comfort that if the remote party force closes the channel, then your funds will land on your wallet whether you have made a backup or not. So you could argue that the backup currently is not very useful, but it will probably be more important in the future if this feature is removed.

Stephan Livera:

And just speaking about lightning implementations more generally as you know, Thomas, I know we spoke about this the first interview can you tell us a little bit around your efforts around doing your own lightning implementation? Has that been difficult for you? Can you tell us a little bit about that?

Thomas V:

Sure. Maybe Ghost you want to talk about that?

Ghost43:

Okay. so originally we didn’t actually want to do our own implementation. And we had another developer inaudible who experimented with another model. And we even researched. I mean, obviously we researched other existing implementations and took a looked whether we could somehow just package them up and then write some API to use those. But in the end, as amusing as it might sound, it turned out to be easier to write our own. Maybe it wouldn’t be the case today with rust lightning, which was written with basically this use case in mind of packaging it into an existing wallet, but back then rust lightning didn’t exist.

Ghost43:

So we decided to write our own implementation. And the main advantage for us is that because it is written in Python and because we are the ones maintaining it, although that obviously also entails burdens we can experiment freely with it and implement stuff that is not part of the protocol yet. Experimental features that well, I mean, it allows us more freedom. So for example, we could come up with features such as in what ACINQ is doing with Phoenix with the experimental TLV type length value extensions.

Thomas V:

and also the Trampoline routing.

Ghost43:

Yeah, that too,

Thomas V:

We have more freedom to experiment and to implement our own features. And also, I mean, it’s a lot more motivating than having to adapt to a moving target as in another implementation that changes its API every time.

Ghost43:

Yeah. But I mean, to be honest originally when we had started with this approach, which was, I think maybe in April, 2018 or something we didn’t think it would take this much time. I mean, originally we thought that we might have some prototype that works for the happy path in like two weeks, but that was overly optimistic. Yeah. Even for something that worked somewhat reliably for the happy path, it took like two or three months, I think. And then, I don’t know, after maybe a year we had something that worked okay, but it was almost trivial to trigger bugs that resulted in critical issues. So that’s why it took more than two years in the end. It’s a lot of work to implement lightning from scratch. It’s yeah. You don’t want to do it unless you really have the resources and you can commit to it.

Stephan Livera:

You’re touched on Rust lightning. And I presume you’re also referring there to LDK by the square crypto team as well. Right?

Ghost43:

Yeah. I guess is the new name for it, but even originally when Blue Matt had started rust lightning he said that well, okay. Maybe, maybe at the very beginning, he said that he wanted to just experiment with lightning. But after a few months he said that he wants to write something that can be integrated into existing wallets. And I mean, that’s been the narrative ever since, as far as I’m up to date with it. And I mean, that’s exactly the use case actually that we would have needed, except it didn’t exist at the time.

Stephan Livera:

Right. And it would just be too difficult now to change back. Right?

Ghost43:

Well, yeah, it would be a lot of work, I think. But to be honest, I mean, even still, we are more comfortable with python code and we can freely change anything and we are deeply intimate with how the code works. That we wrote now. So I guess at this point, it’s not worth even trying to change it.

Thomas V:

But I think lightning is so important that at some point someone would have started to write a python implementation of lightning if we didn’t. So because, because it’s also about the language. I mean, people are familiar with the programming language.

Stephan Livera:

I wanted to chat a little bit about the user experience. So when the user is starting up, Electrum for the first time, there’s been some discussion there about people who are more privacy conscious that they would want to maybe get prompted in terms of connecting, whether that’s to their own server or whether to a public server. Do you have any thoughts on that and whether anything could be done there around the user experience for the more privacy conscious?

Thomas V:

Yeah. There is a difference between the Android app and the desktop, the desktop app allows you to do what you just said. And we have had the same, the request to, to have the same option on the Kivy application which doesn’t have it at the moment.

Ghost43:

Yeah. So you can already do this on QT, on desktop, but not on Android yet.

Stephan Livera:

I see. So this is like you open it up and then in the bottom,right. You click the the connection, like the red, green, red light or green light. And then, so we’re referring here to the first time set up of Electrum wallet, or first time use?

Ghost43:

Yes it is a special case in what we called the install wizard. So, I mean, if you start Electrum and you don’t have a wallet, or even if you do have a wallet, but it’s encrypted and it tries to open that the wizard to be open to creating new words or entering your password for your existing encrypted wallet. And we have logic to detect that it is the first time you, you start the wizard. So I mean, that means it’s the first time you started the application itself. And if, so, there’s an extra dialogue at the beginning, which is basically the same as the network dialogue users might be familiar with as part of the main application, when you already have a wallet open and you can just configure to only connect to one server or connect to your own server or any combination of that.

Stephan Livera:

And also any thoughts around whether that could be made easier for some users who maybe they’re not as comfortable with command line or doing manual configuration. Is there anything there that you think you would, you might be able to add into the user interface there so that the GUI-only user can achieve a similar level of privacy there, like say oneserver option?

Ghost43:

Well, I mean, I think if you’re talking about the desktop application and again we have plans to make the Android application up to par, to implement the same with Android, but on desktop, I think actually even in the GUI, this is already possible. Although maybe I guess it’s not that well known, but I mean, there’s a prompt when you open the Electrum for the first time and you can set this up even one server mode Oh wait, okay. Maybe not one server modes, but so definitely connecting to your own server. Yes. Yeah,

Stephan Livera:

Yeah. So I think you can select your own server, but I think there’s that thing where it shows you like how many other nodes or how many other servers you could connect to. And I guess maybe if you’re more paranoid and you only want to connect to one, your own one or something like that.

Thomas V:

One, one thing I don’t want, I want to say is that I don’t want to promote too much to do the oneserver option because it’s actually a deep reduction of your security. If you don’t use it with your own node and you use it with an external server that is not yours, the oneserver option makes SPV ineffective.

Ghost43:

Well, I mean, I’m yeah. Well, okay. I mean, you’re talking about the scenario where that single server operator is also a miner, right?

Thomas V:

Yeah. Yeah. I mean, it kind of, for SPV to work, you need to connect to multiple nodes, not just a single one.

Ghost43:

Okay. I mean, I see what you’re saying, but maybe that’s not the best way of saying it. I’m not sure. I think SPV works even if you only connect a single node except you have to be more careful than which, I mean only a power user or would know to do such as you would have to actually check whether you have the expected number of blocks and stuff like that, because I mean, okay.

Ghost43:

So like one possible attack vector is that you connect to a single server with oneserver mode, which is not actually yours, which is, I mean, it’s easy. It would be easy to do if everything was exposed in the GUI. And then let’s say the operator of the server even is either a miner themselves or collaborates with the minor. And let’s say they have like 10% of the hash rate or something, and then they could trick you with transaction and have one or two confirmations. I mean, mine actual blocks for that transaction. And then all the SPV checks would pass. I mean, even full node checks might pass. Right. But the point is that this branch of the chain would be weaker, would be shorter than the main, the best chain. But you wouldn’t know about the best chain because you’re only connected to one node.

Stephan Livera:

I was thinking more just in the context of, let’s say the user already has their own Electrum server running and it’s in that, in that context, but certainly for the light wallet user the one who’s not using their own Electrum server, then that makes sense to me. Let’s chat a little bit about a hardware wallet support as well. So there was that recent thing about the Trezor the, I think they locked it down to certain derivation paths. Did that impact you guys?

Ghost43:

Derivation paths? Do you mean the, BIP143, the SegWit signing?

Stephan Livera:

Yes. That one that’s the one. Yep.

Ghost43:

Yeah. Okay. So yes, it impacted us in the sense that it was another factor actually to speed up doing a release doing I mean releasing 4.0 because they, to fix that vulnerability, they had to basically this allow, I mean, they had to do a breaking change in their internal protocol, such that the existing latest version of Electrum back then, for example, wouldn’t be able to sign transactions with the Trezor. So yes, impacted us in that sense. Yeah.

Stephan Livera:

And in terms of maintaining support with any of the other hardware wallets has any of that other that been a challenge for you or that has just been, not such a big deal?

Ghost43:

Yeah. I mean our current model for hardware support doesn’t really scale, I would have to say. Yeah, because I mean, in practice hardware wallet manufacturers send a pull request. They, they write the initial codes and we also asked to have actual devices sent to us so that we can test it. But then it’s only one of, it’s only some of the larger manufacturers who actually help us maintain that code at all. The smaller ones, basically after the initial pull request, don’t do anything. And so that means every time we change something in the codes, even the minor refactor, let’s say, then we have to obviously change that they are plugging as well, which is fine. But then to properly do that, we have to test with the actual device because it’s really, it would be extremely difficult to set up automated tests that that would catch everything.

Ghost43:

So we have to test with the actual device and then we have to test with like 10 devices at this point, I think so. Yeah. And we actually keep getting requests to have more and more hardware wallets. So yeah, we will have to figure something out, but I have to say that at least Trezor and digital BitBox02, or, I mean, BitBox02 they keep sending poor requests to, to significantly lesser the burden of maintenance for us so that they basically maintain their own plugins. So that’s very nice, but yeah, not everyone does it.

Stephan Livera:

Alright. So other hardware manufacturers pick up your game, Hey?

Thomas V:

I mean, I’m very much looking forward to a unified hardware wallet interface. I think that that will be a progress, but also it might not align with the interest of private companies because they want their product to have more features than the competition. So I don’t know if that will ever be a reality.

Ghost43:

Well, I mean, there’s the Bitcoin core project, the HWI at this point, which is kind of similar. So at this point, I don’t think any further unification would happen because that took away all the incentives. But so I mean, one question is whether maybe we could use HWI for Electrum.

Thomas V:

My, point is whether, whether hardware, wallet manufacturers are going to fully embrace this and comply with this.

Ghost43:

Well, I mean, I think the whole point of HWI is embracing the reality that that won’t happen. And the Andrew Chow that just decided to write an abstraction layer himself. So I think realistically, the question for us is whether we could use HWI, but yeah, I mean, last time I looked at it, I’m not so sure that it would be good for us mainly because, I mean, first and foremost, this is written with the CLI use case in mind.

Stephan Livera:

Then does that mean you might have to eventually start rationalizing the hardware to the supported hardware wallets down to just the big ones that you want to maintain support.

Ghost43:

Yeah. I mean, I don’t know about that.

Thomas V:

We might have to do that. It depends on the burden that we have maintaining the plugin.

Stephan Livera:

Also wanted to chat a little bit about multisignature. So Electrum is well known as one of the ways that if an individual wants to set up their own multisignature well this is one of the ways to do that. And it’s got the wizard there. So users can you know, pull together different hardware wallets and put them together. And I think even in this recent version, it’s now possible to do I think there was, I think that previously there was some difficulties doing like different hardware wallets together, but I think this new version actually does allow it I think with Coldcard. So like, for example, if you want to do like a Coldcard and a ledger and a Trezor in a two of three, something like that. I think this new version allows for that. Just also wanted to just discuss for users who are thinking about doing that, what are some of the things they need to think about in terms of backups? What should they be keeping if they want to do that kind of setup?

Ghost43:

Well, I mean, okay, so first I have to say that I mean, even before since like I’m not sure electrum 2.8 or something, I think that multisig with multiple hardware signers involved already,

Thomas V:

But not with Coldcard.

Ghost43:

the change in version. Yeah. The change in version four is that Coldcard because of using PSBT and the intricacies of PSBT itself it didn’t work well. I mean, there was a very involved workaround, but let’s just say that Coldcard didn’t work as part of a multisig before now it works, but actually even right now, it’s not really ideal. I’m not sure a complete newbie could set it up because well, okay. I mean, it works now kind of easily if you’re willing to connect the Coldcard via USB to the computer, but if you want to use it well cold, then it’s still a bit involved because the issue is that xPubs are no longer sufficient to set up a signer.

Ghost43:

Now you also need a derivation prefix. I mean the beginning part of the derivation path and also a root fingerprint. So I mean, the issue is that an xPub is no longer enough to describe a fully a co-signer as part of a multisig. And this used to be the case in the past. So they basically, we would need to come up with a new format, which could hopefully become standardized to contain this extra information in addition to the xPub. And then it would, once again, become easy to do all kinds of multisig and in the future maybe even more complex wallets.

Thomas V:

There is already also the issue of what we’re going to do in the future with script descriptors or mini script. So it overlaps with the question that Ghost just raised.

Stephan Livera:

Yeah, actually that’s what I was going to ask about it, whether you were interested to use that the script descriptors approach and whether that would save you time or whether it wouldn’t really save you much work there.

Ghost43:

Yeah. I mean, we are definitely interested in using output script descriptors. I mean, not just for this reason I’m not sure when we will have the time to get to that, but I mean, obviously if anyone is interested, in working on that, then contributions are welcome and we would help in any way we can. Otherwise it might need a year or whatever, but specifically for this issue, actually output script descriptors themselves would still not be enough because they are like just not high level enough in the sense that I mean the most simplistic example is that if you have a standard wallet then I mean, an HD Wallet then typically what you would have in almost all the wallets nowadays maybe apart from Bitcoin core is you would have a simple depth, two, three where like one branch is used for receiving addresses or external addresses.

Ghost43:

And another branch is used for change addresses or internal addresses. And this would not be hardened. It would be public derivation, almost all wallets do this. So like M/0/I is your receiving addresses and M/1/J is your, those are your change addresses. And to describe your receiving addresses, you would need one output script descriptor with a star at the end, and to describe your change addresses, you would need another. So the point is you would need two output script descriptors, not just one, and also actually you would need some kind of additional metadata to signal that you want to use one descriptor for your receiving addresses and the other one for your change addresses. So you would need to put all this information into a string or some kind of blob that ideally you can copy paste let’s say, instead of what we are currently doing with xPub.

Stephan Livera:

I see. Yeah. So there’s a bit more complexity there. And then maybe then we’re back to the user having, maybe they have to save some kind of JSON file with all that information in it and

Ghost43:

Yeah, exactly. But at that point that becomes really hard to back up. And I’m even not that comfortable to I guess, even copy paste. Yeah, I mean, in terms of backups I guess maybe you wanted to talk about this too, but so if you have a multisig wallet, what what you need to back up is well, okay, so ideally you would need multiple backup locations for your multiisig wallet, right? So I’m talking about the scenario where a single user to reduce risk and attack surface. They would, set up a multisig wallet, contrast that with multiple signers sharing a multisig wallet, right? So a single user could create multiple seeds, let’s say. And distribute the backup locations physically, or maybe store one seed online and another offline and another at a friend or whatever, and then require two out of those three, or I don’t know.

Ghost43:

I mean, there are endless possibilities almost, but the point is that they would need to store all the xPubs potentially at all the locations, or at least that’s the easiest way to do it because in the end, when you restore, if you have to use your backups you will need all your master public keys involved. And I mean the corresponding public keys can be derived from the seeds, but probably you will have only one or two seeds or whatever, and you will need the master public keys for the missing seeds as well. Right. So, yeah. So with this output script descriptor, or, well, even more complicated actually, as I said, multiple script descriptors actually tagged whether they are change or not, and stuff like that, you would need to store those, then instead of the xPubs, which becomes more and more difficult. So, I mean, that’s not something you can print onto paper because you cannot really expect users to be able to tie back some JSON string from paper.

Stephan Livera:

Yeah. Right, right. So I guess just walking through that example, you’re saying, okay, let’s just make a quick example to make it clear. So you might be doing a two of three multisignature. You might want to keep them in three different locations and you might think, okay, so two or three, and if you lost one of the keys and the wallet file, now you will no longer be able to spend, unless you also kept the backup of the xPubs for all three, correct?

Ghost43:

Yes. And that’s how it always works. That’s how it must work because to be able to reconstruct the on chain Bitcoin script, you need all the public keys involved and the different public keys are derived from different master public keys.

Stephan Livera:

I guess if I’m understanding you correctly, there, it could be done then with two separate output descriptors, one for the main, I guess, your main receiving addresses and another for all your change addresses. So would that mean then you’re keeping two script descriptors in that idea?

Ghost43:

Yeah. That’s one possible thing we could do. Yes.

Stephan Livera:

Obviously this is that’s. I mean, I’m just discussing theoretical there, but in terms of today, what you do today is basically you have to keep the xPub for each key. And I guess it also helps if you keep the derivation path for each one. Right.

Ghost43:

Well, I mean, it depends on what kind of key stores, what kind of individual signers the multisig is comprised of, because if you’re just using Electrum seeds, the kind of seeds that electrum the application would generate and give you then all the derivation path and script type logic is abstracted away from the user it’s encoded basically into the seed itself. So the user doesn’t have to know about it.

Stephan Livera:

I see. I got you. So it’s more if they’re using the traditional BIP39 or some hardware wallet then they need to just be mindful of that. And again, it gets too technical for the average user. So?

Thomas V:

Well maybe we come up with a very simple mapping between mini script or script descriptors and integers. If we can do that, then we could actually have a type that includes the script descriptor in the seed.

Stephan Livera:

And so I guess on this whole question of multisignature and standards, are there any other things that could be done to make kind of multisignature standard standardized across different, you know hardware wallets, or different wallets? Is there anything there?

Ghost43:

I guess what we’ve just been talking about would be the main thing, because I think there are two large points here. One is that how you would back up and correspondingly of course, restore from the backup and the other is for your wallet and the other is how you would sign transactions and transfer unsigned and partial transactions between your different locations. And I think the second point has been by now almost completely solved by the PSBT approach BIP174.

Stephan Livera:

The PSBT approach seems to be being adopted or at least supported by many different wallet softwares and hardwares around the space. So that’s, I guess, yeah, that’s the spending part. So I guess it’s just the backups and the backups part that needs to, there needs to be some sort of standard that people kind of form up on. Also you mentioned earlier around the seeds part, so Thomas, I know we spoke about this on the earlier episode, we were talking a little bit about so, currently many hardware wallets are well are using BIP39 style mnemonic BIP39 seeds and Electrum has its own seed style. And I suppose just for some users, that could be a little bit confusing because when they’re recovering, they are often taught, okay, you only need the first four letters of each word to be able to you know, recover that wallet. But it can be a little confusing if there’s like multiple word sets. So I’m wondering whether your thoughts have changed on that Thomas or Ghost, if you wanted to touch on that as well, the comparison of the different seed types and whether you would go to a BIP39 style seed.

Thomas V:

We would need to get rid of our old word list to do the initial word list of Electrum if, if we wanted to have this four letters disambiguation. And I don’t know if we can do that yet. I mean, maybe we could disable it by default but for sure some users would be confused or maybe we can have something a bit smarter that I mean, the big, the big problem we have is that when BIP39 was published, it’s a, standard that had that did collide with the existing Electrum seeds. So, because both use English words, so they have words in common. And so the Electrum seeds could be in some cases, valid BIP39 seeds. Well, yeah, I mean, so you’re just talking about the word lists, but the word list is just one small part of a seeds definition. I mean, a scheme. Yeah, so, so regarding the word list there are currently two English Electrum word lists. The one we had used at the very beginning which is used by so-called old type seeds for Electrum.

Thomas V:

And since version two when the current new seed scheme was introduced for Electrum these modern actual seeds have been using actually the same word list as the BIP39 English word list. And, the current scheme is independent completely of the word list. So but yes, so technically to decode a seed you don’t even need the word list. The word list is simply used to generate seeds that contain English words, but the current Electrum scheme for the seeds is completely independent of any language or words, or it just uses Unicode characters.

Stephan Livera:

I see. Yeah, yeah. Understood. The word list is distinct from the, actual way by which you turn

Thomas V:

Yeah. Did was to not include the word list in the standard and to be able to change it freely later or to localize. So that was my initial ambition. And the big problem we have now is that on Android and also on the desktop users, want to have completion. I mean they it’s much easier if the word list is fixed, because you can have a smart keyboard that detects the beginning of the word.

Ghost43:

Yeah. But just to make it absolutely clear. So, I mean, this is in contrast to what BIP39 has with the, I mean, actually several languages, but if you only consider the English, but at least it’s part of the BIP39 standard. You couldn’t just change the word list because then specifically the check sums would not work out. So, I mean the word list for BIP39 is basically set in stone. You cannot change it, but in the case of actual, if we wanted to, we could change it at any moment, basically.

Stephan Livera:

Yeah. I guess it just kind of comes to that point of with enough new people coming in, and if they’ve already got a BIP39 seed, and then they’re getting confused about trying to recover that into Electrum for example.

Ghost43:

Yeah. Yeah. But I think that’s a separate question, but we can talk about that too. I mean, I guess, well, I don’t know, you decide Stephan whether Thomas should talk about why we are not using BIP39,

Stephan Livera:

Right? Yeah. I think we did speak about this in the earlier episode, Thomas.

Thomas V:

No. Okay. Maybe to make it clear I think BIP39 is dangerous because nontechnical users will only write down their seed words and nothing else, or they might even

Thomas V:

Give this information to someone else who does not know about which client they were using. The problem is that since there is no version number in BIP39 and the software is supposed to be smart and to know about the derivation for your private keys. And of course it cannot work that way because new derivations are added over the years all the time. And you cannot expect software to work like that unless you are willing to accept, to lose Bitcoins how to say, I mean, users, okay. The whole point of this English word presentation is to make it simple for users who do not want a technical description. If users are willing to have a technical description, then why would you use this seed words, I mean, you could just write a string or hexadecimal, and that would be, that would work just as well. The whole point of those words is to have something simple, something you can write down without a computer, just with a pen and paper, and you can restore later. And so the restoration process should be unambiguous. It should not require more technical information such as the deviation path or the type of software that you were using. And how many derivation chains you are using in your wallet? It’s ridiculous to expect users to know that.

Stephan Livera:

Yeah. Yeah. I see. There’s definitely some valid concerns there on both sides. And also on the question of re-scanning I saw an interesting I think Luke Childs who made a contribution around rescanning on all the common or well known derivation paths. Could you tell us a little bit about that?

Thomas V:

Oh yeah this is something we are going to merge? We didn’t have time yet because we’ve been really focused on the release. So the idea is to Okay. I didn’t want to touch BIP39 myself because I think it’s a never ending thing for the very reason that BIP39 works with BIP43 and BIP43 is really the issue. It says that the number of potential derivations is unbounded. It can go indefinitely in the future. So you need to perpetually maintain code that will explore the different derivations that have been used by different software wallets or hardware wallets. So these pull requests is the goal to precisely do that.

Thomas V:

To have a sort of a comprehensive exploration of the deliberation path. And yeah, I don’t know how it’s going to be maintained in the future, but I’m open of course, to merge it because at least it will make life easier for some users.

Ghost43:

That’s exactly the whole point that this is only needed because of how BIP39 is constructed because the user might not have their derivation paths written down. And actually it’s not even the derivation paths anymore. It’s also the script type. And even in the future, it might be other things such as like I said, I don’t know, half an hour earlier that nowadays most wallets use this very simple depth two structure of one branch, one HD branch for receiving addresses and another for change. This is also implicit. So BIP39, like everything is implicit and the user would actually write all this down as part of their backup. So in the future, you could conceive that not only do you need to grow it force, the derivation path and script types, also different basically branches of wallets. I mean.

Thomas V:

Gap limit.

Ghost43:

Yeah Gap limit too.

Stephan Livera:

Yeah. These are all very good points, I think. So I guess just to summarize, so it’s kind of like, you might have, basically a user might be in a situation where they’ve got their 12 words or 24 words, but they still don’t know exactly how to access that coins. Cause it’s kind of like searching for a needle in a haystack basically because there’s kind of all these different possible combinations of what that wallet might’ve been set up to use. And that makes it very difficult then to deal with, from a wallet standpoint, if they’re trying to recover into Electrum wallet, for example,

Ghost43:

right, yeah.

Stephan Livera:

You know, Oh, also we should chat a little bit about the Electrum servers. So as I understand the recent, the ElectrumX apparently that guy went all BSV. And so now the Electrum team is maintaining ElectrumX?

Thomas V:

Yeah well it was very nice, as long as it’s lasted because this developer Kyuupichan was maintaining ElectrumX for a bunch of different coins actually. But he’s a Bitcoin Cash and then Bitcoin SV guy. And now for some reason he has decided to drop support for anything else, but Bitcoin SV, which he calls the real bitcoin. So we had to take over and of course we are familiar with the code because we’ve been also co-developing this, every time we had to do a change in the protocol we had to add it to Electrum. So it’s not a problem for us to maintain this code, but it was convenient actually to have him maintain it because he’s the author of that code. I am not the author of ElectrumX. I designed the initial Electrum server, which is a different codebase and which was slower.

Thomas V:

So now we are going to maintain the server code for that reason. But that’s also I mean, in the future, we might also add new things to the protocol. So I mean, I’m very excited about utreexo I don’t know if you have heard about that. So this is something I have a branch on that report that that is a preliminary implementation of utreexo. So if we want to do these kind of things, of course, we need to change the protocol all the time.

Ghost43:

Yeah. I mean, I really have to say that it was great to have Kyuupichan maintain and even write ElectrumX in the first place, because having it hats off to him, he did write really good codes and it’s, it’s really maintainable. I mean, of course there are small bugs here or there, but that’s true for any code base nothing can last forever. Now Kyuupichan decided that he wants to support Satoshi’s vision or whatever. So now we will have to maintain our own fork.

Stephan Livera:

Gotcha. Yeah. And as I understand so typically a lot of users, well, in terms of like the packaged nodes, they typically run with Electrum Rust server. Whereas I think the people who want to have, who want to be more efficient across lots of wallets, they tend to use ElectrumX. And I think there was a recent post by Jameson and the Casa team talking about benchmarking and the different Electrum servers. And I think for them, they found ElectrumX worked best for them.

Ghost43:

Yeah. I saw that blog post too. It was nice. Yeah. I mean, if you want to run a public facing Electrum server serving the public, serving many wallets, then I still recommend you should run ElectrumX I think well, you should probably run our own fork now, but yeah. But if you just want to set up an Electrum server for your own, and you don’t want to expose it publicly, then you have a whole bunch of options. I mean, you can see that actually works for that too, but you can also run the Electrum Rust implementation or Electrum personal server by Chris Belcher, or there’s another implementation now I think that’s very lightweight to similar to EPS by Nadav Ivgi (Shesek).

Stephan Livera:

BWT.

Thomas V:

But one thing about Electrum personal server is, I mean, last time I checked, at least you use it with lightning because lightning requires your, Electrum Server to be able to watch arbitrary addresses.

Ghost43:

yeah. So there’s that for the complication. Yeah. But okay. I mean, if you run Electrum Rust server or ElectrumX, then you should be perfectly fine.

Stephan Livera:

And also, yeah, it’s interesting as well, just touching on earlier, you mentioned Thomas utreexo by Tadge Dryja. So that might be an interesting idea for people to be able to more easily run something in between. I mean I probably won’t be able to explain it very well, but basically I, as I understand the idea is that you could have this I forgot the, I can’t remember the exact term, but basically people could be running like a full node on a mobile phone sort of thing, because it would compress it.

Ghost43:

Yeah. I think maybe he called it a compact node.

Thomas V:

Yeah, you can, you can I mean, it has what is called a compact node. So I would not call it a full node, but yeah, there are different reasons why I’ve been looking at utreexo. So it’s not clear yet. I mean, we are experimenting, so it’s not clear yet whether we will make it part of the Electrum protocol or not. That’s, really an experiment and ongoing experiment.

Stephan Livera:

So is there anything else that you guys wanted to touch on in terms of things you’ve got coming up with Electrum what should users be looking out for?

Ghost43:

Well, I think at the moment we are very focused on bug fixes, bug fixes.

Thomas V:

I think we we’ve been adding a lot of new features and now is the time for fixing bugs and consolidating code and also improving the GUI because the user experience, we get feedback on the user experience. I mean, when you add a new feature, do the first iteration the GUI that you make for that feature is obviously not the best. So you, you learn also from the user feedback.

Ghost43:

For example, I’ve seen on the sub-reddit actually for Electrum that it’s been a recurring question since version4 that I mean, the receive tab app changed and then users can’t find their receiving address because previously when you receive that you were given a Bitcoin address, I mean, right away, it was shown by default and now you actually have to press a button to generate a new one which was I mean, it was an attempt to unify the on chain and the lightning experience, but also also to reduce address, reuse such that you would actually have to manually create a new address.

Ghost43:

And I mean, an invoice and be given an address to use for a new payment. But so I mean, these kinds of things will have to be made easier to use, but yeah, I mean, there’s, there’s a lot of things to be done. For example I think we would need more tests. I mean like unit tests and functional tests for the lightning parts. Mostly, I mean, we already have quite a few, but to be honest, I mean, we would still need more to have better sleep at night. And yeah. There are new features to implement in the medium term too for example, I would like to look into PayJoin, let’s say, but I’m not sure when I will get to that.

Thomas V:

Yeah. There will also be a changes to the lightning protocol itself.

Ghost43:

Oh yeah, of course. I mean, we have to keep up with them.

Thomas V:

Maybe at some point we will also want to have Taproot.

Stephan Livera:

If any listener is interested to contribute, where would contribute be much needed?

Ghost43:

Well, I mean first of all, if you want to contribute, you should come to the IRC channel on Freenode it’s #Electrum. And also, I mean, obviously find the repository on GitHub and then, well, I mean, a good place to start, I think is just to look at some open issues and also pull requests and I guess maybe also to look at recent commits to see what we are working on, but yeah, I mean, first of all, I think you, you should ask on IRC, you should, you should say if you have some time and what you might be interested to work on, and we might be able to, we would probably be able to help you or might be able to give you ideas. But regarding ideas now.

Thomas V:

I’m very happy with the approach where people proposal a pull request for an issue that has been annoying them, because that’s actually the best let’s say capital allocation in terms of programming time people usually they start contributing because they see an issue that we do not see, and that’s very important. I think that’s also how you started to work on electrum. I mean, you were, Ghost, you were that’s where most of the time, the case when we received a full request, this is something that is not so important for us, but it’s important for someone. So they propose to fix it. And that’s very good because it increases the number of viewpoints on the software.

Ghost43:

But even if someone wanted to implement a completely new feature, I mean, they can go for it. I mean, I just mentioned PayJoin, for example, if someone said that they would be interested in implementing PayJoin for electrum then great. We would give all the help and then could talk about discuss the possible approaches and then what modifications would be needed for the code. And then they could go on and maybe not even do the whole thing, but just some prototype that sort of works. And then because PayJoin earlier.

Thomas V:

Because it seems like kind of easy to do now.

Stephan Livera:

Thinking about Bitcoin more broadly, you know, do you guys have any thoughts on what’s going to happen over the next year or two? Are there any things that you’re really interested to see in terms of Bitcoin, the protocol and any other developments in and around Bitcoin and lightning?

Ghost43:

Well, I hope the Taproot soft fork happens. I don’t know, realistically like a year or two. And then I hope that the lightning network with the bolts can start using Schnorr signatures and also tapscripts for some of the on chain scripts. Like I mean, which no signatures replacing the hash pre images with point multiplication and stuff like that. I mean that’s very exciting and I think it could realistically happen, but I mean the prerequisite is having Taproot.

Thomas V:

I would really like to have is a much better way to find a path in the lightning network. Currently we need to have the whole database locally. So there is this Trampoline proposal. I don’t know if someone will come up with an even better solution for the moment. It seems to be the best solution that has been proposed. So I hope that something will emerge or at least that the Trampoline solution will be adopted because it makes a, I mean, if you don’t have to run the lightning database locally and the gossiping, it makes your client much lighter.

Ghost43:

Yes. I think in terms of user experience after we fix some, some GUI issues when you use Electrum with Lightning, I think the main issue at the moment would be all this path finding and gossip stuff, because I mean if you use Electrum, as it’s intended to be used as a light client, that you just fire it up when you need it for a few minutes or whatever, then it’s really problematic to sync up all the lightning gossip. And without that, path finding doesn’t really work that well, and you will have a lot of failed payment attempts. And then the whole thing cascades, because I mean, this is like one of the main reasons watchtowers, for example, it doesn’t really scale at the moment that I mean, you have to make like 20 payment attempts to have a somewhat larger payment succeed or maybe even more. And then that needs 20 times the storage let’s say, so yeah, everything is related, I guess.

Stephan Livera:

Yeah. Some great reflections there. And I know some of the discussion there was quite heated amongst some of the lightning developers. I think the concern for some of them was that it would be a privacy concern because not enough people would run the trampoline node and then there would be too few people yeah, basically too few people running the node and too many people trying to be using the trampoline routing and so on. But I think that’s a bit more of a technical debate that we don’t need to wade into. And I certainly, I don’t have a position on that. I’m not that into the detail on it.

Ghost43:

Yeah. Right.I mean, I guess the main point is not that we want to use trampoline. It’s just, that’s the most mature solution, I guess, which doesn’t completely give up your privacy in terms of better path finding and routing. I mean, we would be content with any other competing solution if there was one.

Thomas V:

Maybe there will be one we don’t know yet. I mean, I would say that at the moment that Trampoline is the most reasonable solution in town, but yeah. Maybe someone will find something even better.

Stephan Livera:

Excellent. Well yeah, if you guys had any closing thoughts for the listeners.

Thomas V:

Well I don’t know. Thank you for having, for giving us this opportunity to talk about Electrum. I think we really want to make Bitcoin easy. That’s always has been the motivation behind Electrum to increase both security, privacy and ease of use. So use Electrum and do share feedback with us. That’s the best thing you can do to help. And then of course, if you’re a programmer, please do do help us fix bugs, propose pull requests. That’s the thing.

Ghost43:

Yeah, that last part is also what I wanted to say that, I mean, if you’re already a user of Electrum or become to be later or whatever then, and also if you are a programmer, then please, well, first of all, report bugs and have a look at existing bugs and maybe look at the code. And if you have a bit of free time, maybe submit a pull requests, I mean, that’s how open source works. That would be nice.

Stephan Livera:

Fantastic. So listeners go and find the guys find Electrum.org. Follow them @Electrum wallet on Twitter. And obviously it’s a #Electrum on Freenode. Thank you guys for joining me on the show today.

Thomas V:

Thank you.

Ghost43:

Yeah. Thanks for having us Stephan.
