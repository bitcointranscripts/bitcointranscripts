---
title: "Hardware Wallet Integration in Bitcoin Core and HWI"
transcript_by: NeroCherubino via review.btctranscripts.com
media: https://www.youtube.com/watch?v=TXyi-G1Snx4
tags: ["bitcoin-core","hardware wallet","hwi"]
speakers: ["Sjors Provoost","Aaron van Wirdum"]
categories: ["podcast"]
date: 2021-03-05
---
Aaron van Wirdum: 00:01:46

Live from Utrecht this is The Van Wirdum Sjorsnado.
Hello!
Are you running the BIP8 True independent client yet?

Sjors Provoost: 00:01:56

Negative.
I did not even know there was one.

Aaron van Wirdum: 00:01:59

One has been launched, started.
I don't think it's actually a client yet, a project has started.

Sjors Provoost: 00:02:05

Okay, a project has started, it's not a binary or a code that you can compile.

Aaron van Wirdum: 00:02:09

But I did see you were reviewing the BIP 8 code a little bit.

Sjors Provoost: 00:02:16

Yes, I mean it's a pull request that has a bunch of changes in it.
A lot of them are totally not controversial.
So I'm just working on it from top to bottom.

Aaron van Wirdum: 00:02:26

Just code review?

Sjors Provoost: 00:02:28

Code review, and I've also started my own pull request where I've taken a couple of commits from that just to split it up.
Makes everybody's review life easier.
If everybody's talking about `LOT=True` or `LOT=False` on a pull request but there's a lot of nitty-gritty stuff that you really don't want to screw up just because you're talking about one little thing.

Aaron van Wirdum: 00:02:46

That's good.

Sjors Provoost: 00:02:48

So that's all good and we'll see where that ends.

Aaron van Wirdum: 00:02:50

And I think you were working on something else as well and that's actually what this episode is going to be about.

Sjors Provoost: 00:02:55

But by the way, if there are independent clients, just be sure to listen to our earlier episodes about open source and deterministic builds and all the things that can go wrong there and then do it right.

Aaron van Wirdum: 00:03:07

Other project, other thing, the other thing you're working on.

Sjors Provoost: 00:03:10

Hardware wallet stuff.

Aaron van Wirdum: 00:03:11

Yeah, you're working on, not just you, but I think you're one of the core devs working on hardware wallet integration for Bitcoin Core, is that correct?

Sjors Provoost: 00:03:21

Yes, right.
It's me, it's Andrew Chow, Instagibbs, as he likes to call himself on GitHub.

Aaron van Wirdum: 00:03:27

And you've made some good progress.
There was a new merge this week.
And we're basically going to discuss hardware integration in Bitcoin Core in a general sense in this episode, I think.
So basically your top specialty maybe.

Sjors Provoost: 00:03:42

Definitely one of my favorite topics.

Aaron van Wirdum: 00:03:45

You wanted to refer to some previous episodes where we discussed some of this stuff, I think?

Sjors Provoost: 00:03:49

We talked in the first episode about hardware wallets, sort of the security things you need to worry about when it comes to change and etc.
So that might be a nice refresher.
Apologies for the atrocious audio in the first episode there was a literal tornado.
I think in episode 7 we explained to Peter McCormack but also to other listeners what an XPUB is which is quite relevant when it comes to hardware wallets because an XPUB represents like a whole bunch of addresses.
And hardware wallets like to communicate that.
And then there was episode 21.

Aaron van Wirdum: 00:04:28

You put it in a show note, so it has some relevancy.

Sjors Provoost: 00:04:31

That's right.

Aaron van Wirdum: 00:04:32

Okay, where are we with hardware wallet integration for Bitcoin Core?
Let's just start from the top.

Sjors Provoost: 00:04:38

There was a lot of things that needed to happen and mainly that which has been done a while ago is to rewrite the entire wallet that Bitcoin Core comes with because it was atrocious.
And that's mostly been done by Andrew Chow.
I've done a lot of testing and reviewing for that.

Aaron van Wirdum: 00:04:56

What was the problem?
What was so bad about it?

Sjors Provoost: 00:04:58

It was started by Satoshi and it just had pay to public key addresses in it and then pay to public key hash I guess was added and then there was other things added and then segwit was added and it just became an unmaintainable mess.
So all that unmaintainable mess has been put in a box and that box has been abstracted in a way that you can create another box that has the same functionality but the implementation can be rewritten from scratch and so that's kind of what we did.
We put the existing stuff in a box because we don't want to understand it anymore.
And we created a new box to replace it with the same form.
And that uses descriptors.
And I guess we'll dedicate some other episode in explaining what output descriptors are.
But they're kind of a nice, elegant way to describe how to derive your addresses, for example, from the seed.
So it would say okay take the seed and then take the first account and then here's an XPUB and then you know take these address derivations and then I want you to make it a native SegWit address.
You can express that in one string and that gets just to the hardware wallet part is because a hardware wallet can then spit out that information so the hardware wallet can tell you okay these are the addresses I have and then you just import it and when your hardware wallet is disconnected you can you know exactly which addresses the hardware wallet has and you only need to connect when you want to sign something.

Aaron van Wirdum: 00:06:24

Would the hardware wallet in that case spit out the XPUB?
Is that why you mentioned XPUB just now?

Sjors Provoost: 00:06:30

Actually currently indeed it spits out XPUBs.
Ideally it would spit out these descriptors, because a hardware wallet might not understand what taproot is, or it might not understand even what segwit is.
And if it just gives you an XPUB, well, that XPUB doesn't really tell you anything.
It's just a way to derive addresses, but it doesn't tell you what kind of things it can do.
So you really want some way for a hardware wallet to tell it what it's capable of.
But for now, we've avoided having to think about that using a project called HWI.

Aaron van Wirdum: 00:07:05

I've seen it a lot, HWI what does it stand for?

Sjors Provoost: 00:07:08

Hardware Wallet Integration.
Or interface I guess.

Aaron van Wirdum: 00:07:12

Which one is it Sjors?

Sjors Provoost: 00:07:13

I don't care I think it's interface.

Aaron van Wirdum: 00:07:16

Okay.

Sjors Provoost: 00:07:17

So that is a Python library.
And again, mostly by Andrew Chow.
What he did is, because all these hardware wallets, like the Trezor and the Ledger and the KeepKey and the Coldcard, et cetera, they all have their own little Python libraries that you can find on GitHub because it's all open source.
But they're all different.
They all have different ways to display an address.
They have different ways to get an XPUB.
They have different ways to sign a transaction.
What he did is he combined all these drivers, stripped all the shit coins out of them, because some of them would do Ethereum things and we don't want Ethereum code.
And then basically put that all together in one little library and made it consistent.
As far as the user is concerned, you tell HWI, enumerate, and it will give you the list of all the connected hardware wallets using all these different drivers to find them.
And if you say, get descriptors, then it will give you a list of descriptors that describe exactly what keys, what addresses the hardware wallet has, and it does all the magic of fetching XPUBs using whatever method is necessary.

Aaron van Wirdum: 00:08:22

So could I describe HWI as sort of like a meta protocol that communicates with all of the different hardware wallet protocols, I'd say?

Sjors Provoost: 00:08:34

Yeah, I guess.
Another way to say it is that HWI is a tool, but it has a way of communicating, you have a way of giving it commands, and that is a protocol, essentially.
So somebody else could make a tool that is behaves the same as HWI but is you know just for their own hardware wallet so hardware wallet manufacturer you know doesn't have to let people use HWI they could make their own driver that just behaves the same way as HWI and then Bitcoin Core as we'll discuss next we'll know how to talk to it.

Aaron van Wirdum: 00:09:06

If someone brings a new hardware wallet to the market which does its own thing again then HWI will be updated potentially to be able to communicate with that as well?

Sjors Provoost: 00:09:18

Depending on the enthusiasm of the maintainers of HWI, they might go out and find that driver and include it.
If the enthusiasm is slightly less, then the manufacturer or a fan, a user, can go to HWI, make a pull request, and say, "Hey, here's the support for this new hardware wallet".
And then recently there were some guidelines merged for that.
So the hardware wallet has to be open source.
At least the firmware that runs on it has to be open source, with the only exception being if there's a secure element in it that's under NDA, that's okay.
And it has to be sort of what, maintainable, the software.
But then, yeah, anybody can just make support, add support for any other hardware wallet to HWI.
But again, it's not necessary.
The hardware manufacturer could also make their own software that just speaks the same language as HWI.

Aaron van Wirdum: 00:10:14

And HWI was already merged into Bitcoin Core?

Sjors Provoost: 00:10:18

HWI is a separate program that's in the Bitcoin, not in the Bitcoin Core repository, but there is a GitHub organization called Bitcoin Core, which has a bunch of repositories, and that includes HWI.
So it's separate from Bitcoin Core because it's all this Python stuff and USB drivers.
So I guess we don't want to put that in the Bitcoin source code because that's too scary with all the dependencies.
But it is maintained by Bitcoin Core people.
So it's a trust slightly less or I don't know how to put it.

Aaron van Wirdum: 00:10:49

HWI is a separate program essentially and it needs to be installed separately if you want to use it.

Sjors Provoost: 00:11:00

Exactly, you can download it separately, install it separately, or just put it somewhere.

Aaron van Wirdum: 00:11:04

It's not in the Bitcoin Core client that I'm running at home?

Sjors Provoost: 00:11:09

No, because in order for that to happen, first of all, it would probably have to be written in C++ or in Rust or something like that.
And all the USB drivers would have to be inspected with a tooth comb, and that'll take forever.
It's something you install separately, and there is some risk, obviously, with just running that software.

Aaron van Wirdum: 00:11:28

This is not new, is it?

Sjors Provoost: 00:11:31

That's right.
HWI has been around for at least a year.

Aaron van Wirdum: 00:11:40

What was merged last week?

Sjors Provoost: 00:11:42

Before last week, if you wanted to use HWI with Bitcoin Core you can do that but you have to execute a bunch of commands manually so for example if you wanted to sign a transaction you would tell Bitcoin Core okay I'd like to create a PSBT so we explained PSBT in an earlier episode.

Aaron van Wirdum: 00:11:59

Yeah partially signed Bitcoin transactions.

Sjors Provoost: 00:12:01

Exactly, you tell Bitcoin Core okay give me a PSBT, a partially signed transaction, in this case actually an unsigned transaction probably and to the destination and then you would copy paste the result and you'd say, okay, HWI, please sign this thing.
And then HWI would do its thing.
And then you get a result and you copy paste that back into Bitcoin Core and say, "Bitcoin Core, please process this thing and send this thing".

Aaron van Wirdum: 00:12:24

You're running both programs, the Bitcoin Core program and the HWI program, and then you're manually copy pasting data from one to the other.
Using your hardware wallet on HWI, getting some signature and then copy pasting it to Bitcoin Core, and that's how it would work.

Sjors Provoost: 00:12:42

Exactly.

Aaron van Wirdum: 00:12:43

And you're doing this all in the command line, I assume?

Sjors Provoost: 00:12:46

Yes, That's right.
There was already some help with that because HWI also comes with a little graphical program where you can actually click buttons to make it do these things, but you'd still be copy pasting back and forth with Bitcoin Core.

Aaron van Wirdum: 00:12:58

I love buttons.

Sjors Provoost: 00:13:00

What is new now is that Bitcoin Core now knows how to communicate with HWI.
Still from the command line, but it still gets easier.
Because now when you want to send coins, you just tell Bitcoin Core, send, and then the destination and the amount.
And it will know that it needs the hardware wallet.
So it will say, "Hello, HWI, please do these things".
And it will wait for the results.
And it will process the results.
And it will send the transaction.
So you go from four back and forths with copy-pasting to just send.
And it works.

Aaron van Wirdum: 00:13:34

No more copy-pasting.

Sjors Provoost: 00:13:35

All you need to do is tell Bitcoin Core where HWI lives, so where on your computer you installed it, and then it will just call it for you.

Aaron van Wirdum: 00:13:43

If you know how to work the command line this is pretty big improvement I guess.

Sjors Provoost: 00:13:49

This is significantly less tedious.
The approaches like with the manual back and forth and with this it's much easier.

Aaron van Wirdum: 00:13:56

But you do still need to use the command line.

Sjors Provoost: 00:13:59

In Bitcoin Core you have this window, the debug console, which is essentially a little command line.
But you cannot do it in the user interface, but you can actually open this window console and then you can just type send, and it'll work.

Aaron van Wirdum: 00:14:15

This was merged into Bitcoin Core, which will be released in, I guess, it will probably be Bitcoin Core 22?

Sjors Provoost: 00:14:23

Yeah, Bitcoin Core 22 should be out in fall.

Aaron van Wirdum: 00:14:27

Might it also come into a minor release?
I guess that might depend on taproot activation stuff.

Sjors Provoost: 00:14:32

This is not the kind of stuff that would be backported.

Aaron van Wirdum: 00:14:35

So it's definitely gonna be a major release is that what you're saying?

Sjors Provoost: 00:14:38

Because in order for things to backport has to be simple enough or like a really critical bug fix but usually the only things that are backported are bug fixes and soft forks but not entire new features.

Aaron van Wirdum: 00:14:51

This will be in the upcoming Bitcoin Core 22 release.

Sjors Provoost: 00:14:55

Or if you compile the master branch yourself.

Aaron van Wirdum: 00:14:59

The step after that I would assume would be GUI support.

Sjors Provoost: 00:15:04

GUI support that's right, because having to type commands is kind of annoying.
So I have a pull request open that builds on top of this, and it adds a couple of things.
It adds something to the settings screen.
So there is a settings screen in Bitcoin Core.
And there you tell it where HWI lives.
You don't have to give that to the command line.
You just copy paste that file directory.
And then when you go to the menu to create a wallet, if you have this HWI path correctly, and you have a hardware wallet inside your computer and it's like unlocked if you create a new wallet it'll detect it so it'll say "Oh would you like to use this ledger X or whatever"
and then you click next and it will automatically pull the keys from the device and your wallet will just look like any other wallet.
You can click on receive address, you'll see an address.
And then the other feature is that if you click on a receive address, so in Bitcoin Core, you click on, get me a new address, then it kind of makes a little mini address book and you can right click on that, I believe, and then click on verify.
That's a new button.
And the verify button, again, if the device is plugged in, will automatically show the address on the hardware wallet.
You can check that it's real.
And then the third thing that's added is you can now just send Bitcoin as you would in Bitcoin Core.
Just click on send and type the destination, set the fee area.
And when you hit send, if the device is plugged in, it'll show up on the device and you click on approve and it just sends it.
Now the downside is that if anything does not go exactly right as I just described it, it will probably crash.
So it's still a work in progress.

Aaron van Wirdum: 00:16:54

Would it work with all of Bitcoin Core's current futures?
That would be for example be RBF I guess and sent to many or whatever it's called, batching, these kinds of things.

Sjors Provoost: 00:17:05

If in the graphical interface you can send a transaction, you can send it to like 10 different recipients if you want to, that'll work.
I believe RBF I have not implemented because internally that does a few other things.
You can try.
But it would be trivial to add that as a follow-up.
But I try to keep these pull requests as minimum as possible.
These are like three features that I think are really at least good enough.

Aaron van Wirdum: 00:17:30

Are these things possible now?
Are we just talking about the UI?

Sjors Provoost: 00:17:35

This is the GUI pull request.
Right now you can do all these things with the command line, but they'll work in the GUI, which is very nice, especially coin selection.
So in the command line, typing send an address and an amount that's not too bad.

Aaron van Wirdum: 00:17:50

Other good example, coin selection.

Sjors Provoost: 00:17:52

But the coin selection is only practical in the GUI so you can actually like decide which coins to spend and having coin selection with hardware wallets is very nice.
It does work but it only works if it doesn't crash.
That just needs more review and requires me to fix things and maybe make it asynchronous so the screen doesn't block while the hardware wallet is doing something.

Aaron van Wirdum: 00:18:16

This will probably not be ready before Bitcoin Core 22.

Sjors Provoost: 00:18:20

I'm bullish.
I think it might be possible.
It depends on the review because I have a couple things that I want to improve about it but I tend to get more motivated when people start screaming at me in the reviews.

Aaron van Wirdum: 00:18:31

I can scream at you in the reviews.
I won't say anything useful, but I can scream at you.

Sjors Provoost: 00:18:36

You do have to actually test it.
Don't just come in from Twitter and comment on it.
But if you actually run the code and something goes wrong, then I'll try to help or fix the bug.

Aaron van Wirdum: 00:18:45

What about multi-sig?

Sjors Provoost: 00:18:53

Everything I've described is for a single-sig.

Aaron van Wirdum: 00:18:57

If you'd want to use three hardware wallets, and then two out of three, stuff like that.

Sjors Provoost: 00:19:04

Eventually I'd like to see something similar to how Electrum, just let you make a pie chart.
None of that is there yet, not even in the command line.
It is possible, I think I once made an experimental pull request that did do multi-sig at least from the command line.
But there's a lot of moving parts.
I'd like to get all the single-sig stuff merged.
Then we'll move on to multi-sig.
Bitcoin Core multi-sig with hardware wallets will be a while.
There's another project, is called Specter.
Specter is also a hardware wallet but in this case what we're talking about is the Specter desktop software, another Python project.

Aaron van Wirdum: 00:19:49

There's a device, a Specter device?

Sjors Provoost: 00:19:51

Yes.
It's very cool I should have brought it with me, but it's a do-it-yourself hardware wallet.
You can actually order the components from any manufacturer that sort of makes these Arduino-like or smartphone-like things.
And you take a QR scanner and you solder it on it.
This is by Stepan Snigirev.
He's been working on that.
He's also been working, I believe, on support for actual secure elements, so that you can buy your own secure element from like a manufacturer that makes a lot of these general-purpose secure elements so they might not even know that you're using it for Bitcoin purposes which is very nice supply chain wise and you don't have to trust them.

Aaron van Wirdum: 00:20:33

That's the device.
We were actually going to talk about the wallet, I guess, the software.

Sjors Provoost: 00:20:37

Because I guess in order for them to develop that device, they wanted to use that inside a multi-sig setup.
And so they spent a lot of time building a multi-sig system.
And that is called the Specter Desktop.
What it does is, again, it's a program you download and it opens on your computer.
And then it says, "hey, where's Bitcoin Core?"
Or hopefully it finds it.
And then if it finds Bitcoin Core, it says, "Bitcoin Core is synced, tt's got all the blocks".
Do you have any devices you'd like to configure?
And then you say, OK, yeah, I have a Ledger wallet, and I have a Trezor wallet, and whatever.
You add those devices one by one by just plugging it in.
And under the hood, that uses HWI.

Aaron van Wirdum: 00:21:18

Specter uses HWI as well.

Sjors Provoost: 00:21:21

It just comes bundled with it.
So it knows how to detect them it knows how to add them.

Aaron van Wirdum: 00:21:25

So you need to install HWI as well?

Sjors Provoost: 00:21:27

No I think Specter just has.

Aaron van Wirdum: 00:21:29

It includes it.

Sjors Provoost: 00:21:31

That's the trade-off right so in Bitcoin Core we don't just want to add HWI, but in Specter, they do.
And then basically you add devices and then you say I'd like to configure a wallet.
And the terminology is a bit confusing.
That's why I used the word device, or the device because the device is also a wallet.
We create a wallet and you say I want to combine the Trezor and the Ledger and I want a two of two.
Or one of two.
And then it says I'm going to create a wallet now.
And it creates that wallet in Bitcoin core so that means that Specter does not have to maintain like all the code necessary to create a whole wallet from scratch because that's a lot of work it lets Bitcoin core do that it also means it can let Bitcoin Core do all the coin selection magic.

Aaron van Wirdum: 00:22:17

And this uses the GUI of Bitcoin Core?

Sjors Provoost: 00:22:20

No, it's its own GUI, which is basically just a little web server on your own computer, kind of like how a modem looks if you log in to the admin panel.

Aaron van Wirdum: 00:22:29

It uses Bitcoin Core as a back end, but you're actually looking at Specter, which also includes HWI.

Sjors Provoost: 00:22:39

And I guess one scenario where this might be nice is if you run Bitcoin Core, not on your computer, but on a Raspberry Pi somewhere, which might not have a screen, or at least you don't want to use the screen and you could imagine remote connecting to your Raspberry Pi with Bitcoin Core running on it and you're not worried because your keys are not on Bitcoin Core it's just the read-only stuff is on Bitcoin Core.
So your Raspberry Pi in your living room with no security is not really a threat but it is a full node and you can use it that way.

Aaron van Wirdum: 00:23:11

That's one way.

Sjors Provoost: 00:23:12

It looks pretty slick it's very easy to use in my experience once you get it running.

Aaron van Wirdum: 00:23:15

That's one way to use a hardware wallet in combination with Bitcoin Core already, including multi-sig solutions.

Sjors Provoost: 00:23:25

Especially the latter.
I guess soon, TM, you'll be able to use Bitcoin Core with single-sig.
And then I would say the fewer moving parts you have, the better.
Nothing against Specter, but if you don't need it, then don't run additional code.
But for multi-SIG, it's great.
And to get that kind of UI, especially in Bitcoin Core, that's going to take a while.

Aaron van Wirdum: 00:23:45

There are a couple of other solutions like this.
You already mentioned Electrum, which you could of course also run in combination with your personal Electrum server, in which case you're also using full node security.

Sjors Provoost: 00:23:57

Although I'd have to see, I don't know if Electrum Personal Server also has support for multi-sig, but in theory that could be added.

Aaron van Wirdum: 00:24:07

There's something called a Lily Wallet.
I don't know if that uses full node security, I've never used it.
It looks very slick, I've seen that.
But that also allows for hardware wallets multi-setup stuff I think but I could be wrong I think that's spv light client type of wallet though.

Sjors Provoost: 00:24:25

I don't know.

Aaron van Wirdum: 00:24:26

I think there's also one called caravan.

Sjors Provoost: 00:24:29

Caravan I've heard of that.

Aaron van Wirdum: 00:24:30

I don't know much about caravan, I know it does something similar.

Sjors Provoost: 00:24:35

That's what I heard too and then there is Casa, I don't know how they do it, there's all sorts of ways.
I imagine in the future this is gonna get better and better.
We talked about very simple multi-sig setups, but imagine a scenario where we have not just taproot.
We have taproot.
And then we have Miniscript, which we talked about in an earlier episode, which allows you to make far more complicated setups.
Now you can imagine instead of a two or three setting where you have two hardware wallets, one you keep in a vault somewhere, one you keep wherever you are, and then the third key quote unquote is not actually a single key, it's not a single device.
It is some sort of bank, some sort of bank that helps you.
And they internally use some extremely complicated setup, which you don't have to understand.
From your point of view, it just looks like one signature.
In reality, it's very complicated.
And it can all be communicated through Miniscript and then you do something like Specter so you and your site can make sure everything works and only when you need the bank then you need to ask them for a signature but other than that all just works from your end.
Even though they have some super complicated rules set, for you it's just a third party and you don't care.
So I'm very bullish on the future but this is gonna take a while.

Aaron van Wirdum: 00:25:56

Well Sjors, thanks for the update.
This is where we are with hardware wallet integration in Bitcoin Core now and soon TM.

Sjors Provoost: 00:26:04

That's right, anything else?

Aaron van Wirdum: 00:26:06

I think that's it for me.

Sjors Provoost: 00:26:07

Alright.
Thank you for listening The Van Wirdum Sjorsnado.

Aaron van Wirdum: 00:26:10

There you go.
