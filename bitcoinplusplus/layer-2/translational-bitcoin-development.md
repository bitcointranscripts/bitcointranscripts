---
title: "Translational Bitcoin Development"
transcript_by: NeroCherubino via review.btctranscripts.com
media: https://www.youtube.com/watch?v=BsWR94cbZ3Y
tags: ["ux"]
speakers: ["Tadge Dryja"]
categories: ["video"]
date: 2023-04-29
---
## Introduction

This is called Translational Bitcoin Development or Why Johnny Can't Verify.
So quick intro, I'm Tadge Dryja.
Stuff I've worked on in Bitcoin over the last decade is the Bitcoin Lightning Network paper, the Discreet Log Contracts paper, Utreexo, and building out a lot of that software.
In terms of places I've worked, Lightning Labs, founded that, and then MIT DCI is where I used to work for a couple years and now I'm at a company called Lightspark.

## Goals

First I'm gonna talk about, do we even agree on the goals?
Probably not.
People have different ideas of what Bitcoin should be.
I think I made up the term, like Bitcoin is the currency of enemies.
Everyone's sort of got very different ideas and people fight about stuff.
But yeah, maybe people can agree with this.
I think, For me, I want lots of people to use Bitcoin and Lightning Network.
Fully verifying on hardware they control, their own hardware.
I think things like Lightning Network, Utreexo, all that kind of stuff helps.
But to me, part of the goal is, we should try to get it so people can run full nodes, so people can verify the whole thing, so everyone gets this trustless property.

## We Know Bitcoin

I don't want to speak for everyone here, obviously, totally different, but we know Bitcoin!
Maybe even if you're like, you can say I'm a noob, but you're at Bitcoin++, you're not a noob!
We run Bitcoin, we compile it from source, we GPG verify all the different maintainer signing keys, we've got reproducible builds with geeks, and it's like a custom one external that won't work with projectors, and you've got like a hand-soldered RISC-V board, and you know, Bitcoin works.
Like, we can get Bitcoin, you're like, oh, I wanna send a payment easily.
We sync up, we've got a node.
So that part works for us.

## Most people don't know Bitcoin

But most people don't know Bitcoin, right?
So I don't know to what extent, like once you've worked on Bitcoin for a while, like a lot of my friends work on Bitcoin and stuff like that, but I still have friends that are not Bitcoin people.
So hopefully you guys do too.
But like a lot of them are computer people because I've been working on computers for longer than I've been working, like I've been doing computer stuff my whole life.
So a lot of my friends are like, some of my friends are like video game developers.
I mean they think Bitcoin's cool or they say that to not have me bug them, but they work on like Unity and they develop games or something.
Or they know computers but they're not Bitcoin people.
And for a lot of people it's scary.
Bitcoin doesn't work like other stuff.
Terminology is tricky, just a monoid in the category of endofunctors.
It's, you know, oh this PBST and there's so many HTLCs, what are all these things?
I just want to send people money.
But I think a lot of people want the same thing we do.
A lot of people I've talked to get the idea and they're like, yeah, I want that.
I don't want to dedicate my life to Bitcoin.
I don't want to develop Bitcoin, I'm not gonna program it, but I want what that offers.

## Nov 2022 FTX incident

And so here's an example that I want to talk about.
It's not gonna be super technical.
It's gonna be hopefully more of a discussion.
I don't have any new amazing cryptographic cool thing.
It's sort of reflecting on like the last six months.
Especially this.
So, FTX went down in November, I think, and a lot of my friends messaged me.
And this is also, one, it's frustrating because it's like, wait, MtGox, That was like eight or nine years ago.
That was a really long time ago and the same thing's happening, right?
It's just the exact same thing.
And when Joseph and I were working on the Lightning Network paper, that was also a long time ago and that was, MtGox was very much in our minds.
So Lightning Network, I sort of thought the first uses would be exchanges, because people aren't going to trust exchanges anymore, so they're going to want channels with their exchange.
Never, maybe it's happening now, but yeah, it didn't quite go that way.
Anyway, so people messaged me back in November.
And they're like, hey, just saw about FTX.
I should get my coins off crack.
And I was like, yeah, you should.
And then people were like, hey, just saw this news.
Do you think Gemini's okay?
And I'm like, I mean, yeah, it's probably okay, Gemini seems like a well-run exchange.
I don't know, I haven't really talked to them, but yeah, you should move stuff to your own node, maybe you should just run Bitcoin.
Let me know if you need help.
And I did help people.
Okay, so here's what happened.
So I'm going to do this (download and install bitcoin) right now.
Let's see.

## Download and run bitcoin 23.0

It's download and install Bitcoin Core 23.0.
That was the one that was out November (2022).
And it's hard!
So if you go to bitcoin.org, it doesn't have it.
Bitcoin.org hasn't been updated for well over a year.
So you gotta go to Bitcoin Core.
And that is decentralization, right?
And so we're gonna get 23.

So you go here (bitcoincore.org) and then you download it.
And you're like, I want the Linux 64-bit one.
So you copy.
I'm not going to do it because actually this internet is kind of slow.
But I'm just going to do it on desktop.
Here's my desktop.
This worked great on one screen, I thought I'd be able to mirror it.
I'm gonna download Bitcoin.
Got Bitcoin here, and I've got this zip file, put it in here, and I extract it?
Okay, fine, open with Archive Manager, Here it is, Bitcoin 23.
So this is what I did with my friends.
Because they have Linux.
They can download the zip file, you know, tar.gz, and then, okay, here you go.
Okay, README.
Well, how do I run this?
Oh boy!
Well, let's open it in a normal editor.
Okay, so the README has no mention of how to use Bitcoin.
Zero!
That's okay, yeah I already know that.
License, development process, testing, automated testing, contributing, manual quality assurance, translation, nothing.
So that doesn't help.
bin? (referring to bin directory in the bitcoin core source code)
Well, I want a bitcoin-wallet.
Yeah, I don't know, should I run it?
It doesn't run, I don't know what it does!
Does anyone here know what that binary does?
No, really, I have no idea what it is.
No one knows what it does that I do.
I don't know what any of these binaries do.
They're there.
They're a decent size.
That's 36 megs or so.
Anyway, you got to click Bitcoin Qt, right?
None of these other ones will do anything.
This one does something (bitcoind).
That one does something, but that's in command line.
And so for a normal person who's like, I want to run Bitcoin, you've got to know that it's Qt. So one of my friends was like, how am I supposed to know that?
Posts on Twitter.
And some people said, well, you just need to know how to use computers.
And I'm like, yeah, so anyway.

(Running demo of bitcoin-qt)

And like, okay, default data, I don't know, yeah, go for it.
Okay, it's doing it.
I got it to work, right?
And this, my friend, they got this far, one year later.
No, and then they're like, okay, let's do this.
Create a new wallet?
I don't know what a descriptor wallet is.
Use descriptors for scriptPubKey management.
This is where one of my friends stopped at.
They said, I don't know.
"Use descriptors for scriptPubKey management".
It's checked.
If I uncheck this, do I lose all my money?
They said, okay, I tried, I have the eight binaries, I know, got it to work, you know, you're helping.
I'm out.
Here's what they said, I'm out.
Okay, and so they said, nope, not making a wallet.
I don't know what any of this, this sounds bad (referring to the "Disable Private Keys" option).
But it's checked, so I should leave it checked?
Okay, I'm leaving my money on Gemini.
And that's what it is right now.
That money is still on Gemini.
And I think it sucks!
It seems like a low-hanging fruit.
So that's the first example.

### bitcoind and lightning

And now let's say I've got bitcoind running.
Okay, great.
Now I get Lightning.
I downloaded it from GitHub.
I got the `lnd`.
This one we run in command line, but let's try it.
Okay, bitcoin is active.
It's like 20 steps to get it to work.
But yeah, and then it asks for `btcd`.
And you have to change, yeah, so it's like, hey, I'm connecting to `btcd`.
And I'm like, well, I don't want it.
So then you try to go into the `lnd` folder to change the config file, it's not there yet, because it hasn't generated that folder because you haven't successfully started to the point where it'll generate the config file to let you change the config to connect to the `bitcoind` that's already half synchronized.
It's frustrating because like I've worked with so many people and I've worked myself on all these cool technologies and all this cryptography, and then that's the funnel that stops people.

## Bitcoin user experience

So, it was easier when I started using Bitcoin.
I think it was around this version (0.3.21).
It was before BlueMatt put encryption for `wallet.dat` in, because I know it never asked for a password to encrypt the wallet.
So this was a while ago.
It was easier.
You download it, it just runs.
There was no Bitcoin.
There was only that one binary.
It was like, oh, it kind of works.
It was all integrated.
It's kind of nice.
So I want to point out to people, like, so a lot of people here are going to be working on Bitcoin.
And obviously, I like working on the cool cryptographic stuff and all these protocols, but I do want to think about that and I always want to test things with my dad.
Because my dad's running a full node and he's running Bitcoin Core.
I think it's a bit of older version.
It's not updating, but whatever.
And he syncs it up every weekend, plugs it in.
And my dad running Bitcoin Core resulted in, I think, two changes to Bitcoin Core.
Because he would tell me stuff, he's real smart.
He never got into Bitcoin because he was working, and then he retired, and then I go to Thanksgiving, and he'd be like, so the generator of the curve, who determines the point G?
And I'm like, whoa, okay, he's learning about Bitcoin.
And then a couple months later, he's like, okay, I'm going to buy Bitcoin.
I understand it now.
And I'm like, okay, like, you could have bought it when I told you in 2013.
But he wanted to, learn it.
So he's running it, he backed up `wallet.dat` onto a USB stick, uninstalled Bitcoin, reinstalls, tried to restore, it couldn't restore.
Because at the time it would only load wallet.dat from the .bitcoin folder.
So you had to manually put the file back in.
And I told him that, and he's like, it's not there.
I'm like, yeah, it's a hidden folder.
He's like, what?
So that's fixed.

But it also feels like that's not how this should work where I'm helping my dad run Bitcoin Core and I know all the people who work on Bitcoin Core and then I bug them.
He's like, hey, my dad's trying this.
So there's papers and a good analogy.
And this is what I worry about.
This is like more than scalability and all these things.

## Great reference: Why Johnny Can't Encrypt

### PGP never really made it

I worry that Bitcoin's going to become like PGP or GPG, because it feels like it's going that way.
So there's a paper called Why Johnny Can't Encrypt.
It's from 1999, and they have a bunch of college students, and they're saying, hey, Encrypt a message to someone else.
You got 20 CS undergrads, who has this software to exchange pubkeys, encrypt a message, send it to your friend.
And I think a couple people did it, but most people did not.
And I know This is also the case because I worked at MIT for like five years.
Ron Rivest, who's a professor there, who is the "R" in RSA, which is widely used, he would do this kind of stuff in class.
He would say, okay, everyone use GPG and send me an encrypted email.
If you look on PGP key servers, there are hundreds of Ron Rivest's, because so many students registered their own key as Ron Rivest.
And so there's just tons of old Ron Rivest keys, and you're like, well, are all these your keys?
It's like, no, these are students who were trying to send me a message and they registered their key as mine.
There's also why Johnny still can't encrypt, why Johnny still still can't encrypt.
This hasn't changed.
This was a couple days ago.
I was like, well how do I use GPG, but like you type GPG, it's like, type your message, and then you press control+D, I don't even know what that's supposed to do.
I have done key signing parties with lots of other Bitcoin developers, I have never successfully gotten GPG to tell me like yes, this is fanquake's signature.
It always says it's untrusted.
It always gives some weird error that it's not trusted.
And then I have to set like trust and it's like do you trust fanquake unconditionally?
I'm like I don't know.
I'm friends with him but do I trust him with my life?
He seems like a nice guy.
So I set unconditionally to all the keys, and it still gives me this, this key is unknown or something.
So I'm pretty sure I'm doing it right, but it doesn't say I am.
So this is still the case.

## People will jump through hoops

But what I want to say is people will jump through hoops.
People still run Bitcoin Core.
This is (referring to slides) DC++, Direct Connect++, which was like early 2000s file sharing kind of thing.
Still popular in Russia, I guess.
You can download stuff.
It's not good UI.
I don't know if people have used uTorrent or some of these, Napster was okay UI, but people will jump through hoops to get what they want.
And so people will run Bitcoin or even despite all this, but you're competing with Coinbase, right?
Or exchanges or really easy software.
And there's some wallets that, as far as I can tell, or closed source, and to me closed source is basically custodial.
Like, is the key on here?
Yeah, maybe, but who knows.

## Discussion points

We've got, 10, 15 minutes, discussion points.
So I've talked to people about this in the last couple weeks, months and some people are like, just run Umbrel, or Raspblitz, or Casa or there's all these companies, they're like, look, here's a node in a box.
I don't wanna trash those companies, like that's a cool thing to build, people want that.
But also, why Raspberry Pi?
Raspberry Pi's are hundreds of dollars now, and they're not a good deal.
And you can just use an old computer with Linux or Windows on it.
Windows, for example, most people who have computers run Windows.
I know maybe not in this room, but in the world.
And at MIT, yeah, it's this kind of fun process where you'd see kids sort of hazing other kids, and they're like, bro, Windows, bro.
And then by the time they're seniors, they're all running Linux.
But the class I taught, a lot of people were running Bitcoin in Windows, and that was part of the homework, was like, okay, install Bitcoin, run testnet.
And some people couldn't get testnet to work because in Windows, you make `bitcoin.conf` and say `testnet=1`.
Windows `notepad.exe` renames it, it's `bitcoin.conf.txt`, and Bitcoin won't recognize that, and it doesn't show that in the UI.
Yeah, so it's hard.
Raspberry Pi is a nice standard, but it's not, it does seem like another layer of trust.
It's the sort of, okay, we've added this other standard, feels kind of like Docker or something.
I do think it'd be great if people could run stuff without buying any new hardware, without buying anything.
And then some people said, look, you can't have something that's easy for normal users and is sort of enterprisy, right?
Bitcoin Core has moved more towards expert users and it's really dropped off for normal home users and that's sort of a conscious choice.
Last year, one of the Core Dev meetups, we were like, let's just get rid of the UI.
No one wants to maintain it.
Let's get rid of `bitcoin-qt`.
It's just `bitcoind`.
And they're like, no one uses the UI.
I'm like, guys, everyone I know who I tell to run Bitcoin Core and fully validate, they all use the UI.
And there's this sort of disconnect between developers who are using it.

[External voice]: "Developers are not the users."

I like making software that I want to run, but I also have to know that I'm not most of the users.
So, and that might be a point, like yeah, maybe we need multiple packages.
There's Bitcoin Core, but there's also these other versions, but none of them are easy here.
If you run `btcd`, it's not like it's better, or some of the new ones may go Rust Bitcoin.
It's cool that there's different ones.
And then Electrum, which is easier to use, still not perfect, but it's not a full node.
There is no sort of Bitcoin core version that looks or acts like Electrum.
So that'd be something kind of cool.
This is not just Bitcoin.
It does seem that open source projects have a hard time with UI.
It seems that there are UI developers who want to work on open source, but it does seem that that's one of the real weak points, where Linux kernel, top tier, there's nothing better in the world, and it's all open source and everyone works on it.
But whatever, XFCE or X Windows or Wayland, it's not as good.
Why is this, how do we get more people working on that?
I don't know, like, is it a prestige thing, where like, oh, I'm working on these cool cryptographic algorithms, and that's like prestigious, but I feel like Apple is the most valuable company in the history of the civilization and it's because they have good UI.
Now they have the best chips and hardware and stuff, but 10, 20 years ago, they had kinda crummy stuff.
It was like PowerPC, then they run on Intel, it wasn't any faster, it wasn't better, it's just better UI, and that's why they got a lot of people using it, got a lot of money.

## What do y'all think?

What do you guys think?
Some people are like, maybe it's okay if Bitcoin is like GPG and as long as it stays true.
And other people are like, we don't wanna dilute it if we make it too easy.
Then I bet there's people in here who have the same problem, right?
I know lots of people who even use Bitcoin.
They're like, I don't want to manage my own node.
It's too hard.

[recording is missing the discussion part]
