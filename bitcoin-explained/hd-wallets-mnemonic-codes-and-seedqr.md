---
title: HD Wallets, Mnemonic codes and SeedQR
transcript_by: QureshiFaisal via review.btctranscripts.com
media: https://www.youtube.com/watch?v=s8dCyjpfS5E
tags:
  - hardware-wallet
  - bip32
speakers:
  - Sjors Provoost
  - Aaron van Wirdum
date: 2022-09-17
episode: 64
aliases:
  - /bitcoin-magazine/bitcoin-explained/hd-wallets-mnemonic-codes-and-seedqr
---
Aaron van Wirdum: 00:00:19

Live from Utrecht, this is Bitcoin...

Sjors Provoost: 00:00:21

Explained!

(Ad removed)

Aaron van Wirdum: 00:01:41

All right, let's move on. Sjors, today, you've got a new hobby.

Sjors Provoost: 00:01:46

I have a new hobby.

Aaron van Wirdum: 00:01:47

What am I looking at here?

Sjors Provoost: 00:01:48

You're looking at an anvil.

Aaron van Wirdum: 00:01:50

You've got an actual miniature anvil on your desk right here.

Sjors Provoost: 00:01:53

That's right.

Aaron van Wirdum: 00:01:54

And you're using that for what exactly?

Sjors Provoost: 00:01:58

Well right now I'm just using it as a nice decorative element but I want to hobby around a bit with these QR codes that you can basically put in steel plates.

Aaron van Wirdum: 00:02:07

Right, you're going to hammer your private keys into steel.

Sjors Provoost: 00:02:09

Well, or some test net private key probably, but we'll see.

Aaron van Wirdum: 00:02:12

Fair enough, yes. Well, so The specific thing we're going to discuss is SeedQR. This is something you proposed.

Sjors Provoost: 00:02:20

Yes.

Aaron van Wirdum: 00:02:22

I had never heard of it. I don't know where you found it. And I think you didn't remember where you found it either.


Sjors Provoost: 00:02:26

I remember.


Aaron van Wirdum: 00:02:28
Oh, where did you find it?

Sjors Provoost: 00:02:29

Yeah, I was on Twitter as..  I sometimes do.

Aaron van Wirdum: 00:02:30

As usual.

Sjors Provoost: 00:02:31

And I was doom scrolling and then I saw this really cool video of somebody writing down with pen and paper a QR code, just with regular pen and paper, and scanning it and it actually worked. So I was quite surprised to see that you can actually draw them by hand and quite sloppily even.

Aaron van Wirdum: 00:02:49

Why is that surprising? That doesn't surprise me at all.

Sjors Provoost: 00:02:52

I was expecting it to be very sensitive so like if you don't print it with a computer and the squares are not perfectly square then I thought it wouldn't work but it turns out no you can do pretty sloppy work and it still works.

Aaron van Wirdum: 00:03:04

Right. So basically you can draw out a grid and start coloring some of the blocks.

Sjors Provoost: 00:03:10

Yeah, but I think he didn't even draw out a grid here. So yeah, it was just roughly.

Aaron van Wirdum: 00:03:13

Oh, and it still works?

Sjors Provoost: 00:03:14

Yep.

Aaron van Wirdum: 00:03:15

That's actually pretty interesting then. So this was someone using SeedQR? Does this tie in?

Sjors Provoost: 00:03:23

Yeah, so I was wondering what's behind that? What's the standard or maybe a proposed standard? And yeah, so there's apparently something out there called SeedQR. And the context in which it's used is a device, I guess we'll get to that later, it's a device called the SeedSigner and that is not really a company, it's just an open standard for how you can make your own device. So you buy, I think it's a Raspberry Mini or Arduino, something like that. Very tiny computer, has a little camera on it and you install some software on it that's open source. And then you can use that to scan a QR code and this QR code will then convert into your 12 words or 24 words.

Aaron van Wirdum: 00:04:03

Okay.

Sjors Provoost: 00:04:04

And vice versa, you can use a keyboard or it's not really keyboard, just a couple of buttons to enter your 24 or 12 words. And it'll show you a QR code and you can then draw that QR code on a piece of paper. That's kind of what it does.

Aaron van Wirdum: 00:04:16

Right.

Sjors Provoost: 00:04:17

We're getting a little ahead of ourselves, but that's what I was looking at.

Aaron van Wirdum: 00:04:19

Yeah, let's just take this one step at a time, and then we'll get to whatever you're talking about in a minute. First of all, Sjors, how do people make sure they don't lose their Bitcoin?

Sjors Provoost: 00:04:35

They make backups.

Aaron van Wirdum: 00:04:36

Great!

Sjors Provoost: 00:04:37

Or they become a no-coiner.

Aaron van Wirdum: 00:04:38

Well, so people used to make backups. You know, back in the days, we all made backups, which basically meant you literally backed up every private key you had, right?

Sjors Provoost: 00:04:50

Yeah, so I'm using the word backup very broadly, but back in the day you actually had to make a backup in the more narrow sense that you click the button that says make backup and you store the backup somewhere else. So if you were using the old Bitcoin client before it was called Bitcoin Core, it came with a wallet and yes in order to not lose your coins you had to make a backup of the wallet but not just once. Initially every time you spent, Every time you made a new receive address, it would be a completely random receive address. So you'd have to make a backup every time you receive coins or at some point, I think it was improved, so it would make a hundred receive address in the background and you'd make a backup of those 100 addresses. If you forgot to do that, you would suddenly lose all your coins if you restored an old backup.

Aaron van Wirdum: 00:05:36

Right. Okay. So the problem with this, for one, is you need a lot of, well, maybe not a lot, but you need to backup a bunch of data. One for each transaction, one for each receiving transaction, because ideally, of course, you make a new address for each transaction, as we've explained like three episodes ago, I think.

Sjors Provoost: 00:05:54

We've mentioned it a couple of times.

Aaron van Wirdum: 00:05:56

It's also somewhat, everyone knows.

Sjors Provoost: 00:05:58

And so you didn't have to do it every transaction. I think you would have to do it every 100 transactions or something, and they would just make a hundred backups, something like that. But anyway, if you forgot to do that, your coins, you know, not only do you use new receive addresses, even if you use the same receive address every time when you're sending coins, you create a change address to your wallet, and your wallet will create new change addresses..

Aaron van Wirdum: 00:06:17

Right.

Sjors Provoost: 00:06:19

Because it's very disciplined. And so when you hit change address number 101 or whatever it was and you don't have a backup of number 101, now all your coins went to this new change address and they're all gone.

Aaron van Wirdum: 00:06:30

If your computer crashes or something. Yeah.

Sjors Provoost: 00:06:33

Yeah.

Aaron van Wirdum: 00:06:34

Okay. So this was improved. We're just going to have to kind of rush through this because we've discussed it before and I think we've even had entire episodes about some of this stuff. Like for example, the thing we're going to mention now are seeds. I think we've had a whole episode, it was like episode, was an early episode, what is an XPUB?

Sjors Provoost: 00:06:51

Yeah that's a famous episode.

Aaron van Wirdum: 00:06:53

Is it is it a famous episode?

Sjors Provoost: 00:06:55

No! I don't know

Aaron van Wirdum: 00:06:56

I think all of our more actually none of our episodes are famous I'd say.... BIP 32, that's seeds, so was a seed, Am i saying that right? No, no I'm saying it wrong.

Sjors Provoost: 00:07:06

Seed yes, but it's not a mnemonic. So basically a seed just means one key that creates all the other keys. So it's like a plant seed.

Aaron van Wirdum: 00:07:16

Right, yep.

Sjors Provoost: 00:07:17

And so what BIP32 did is you create this one master seed, master key, or whatever you want to call it. And that's the thing you back up, which is the first thing you do when you get the new wallet. You back up this master seed and you're good. Then what happens is you have a tree of derivations, basically, so that each address is unique, but it is all derivable from this one seed. So that's how you can restore it

Aaron van Wirdum: 00:07:41

Just to jog my own memory, really, I mean, if I don't remember, probably some of our listeners don't, Is it essentially just the case that you generate a first private key and then you hash the private key and the hash and the hash and the hash and that's just new private keys.

Sjors Provoost: 00:07:55

Pretty much.

Aaron van Wirdum: 00:07:56

Or is it a bit more complicated?

Sjors Provoost: 00:07:57

It is a bit more complicated but it really boils down to that. You hash it and maybe you add the number one and there's some nuance there, but yeah.

Aaron van Wirdum: 00:08:01

That's essentially the gist of it, all right.

Sjors Provoost: 00:08:06

It's deterministic, so your wallet will know what to do..

Aaron van Wirdum: 00:08:09

Right.

Sjors Provoost: 00:08:10

Once it gets the seed. It will know how to find the addresses that you've used before.

Aaron van Wirdum: 00:08:13

Sure, okay, Now then I guess the problem here, again we're rushing through it a bit, through this part. The problem here is that remembering even the seed, even the first private key is a little bit hard, not for you of course. But for regular people like me and most of our listeners we don't actually remember that kind of stuff. So we need something that's a bit easier.

Sjors Provoost: 00:08:33

Well, so the thing is, initially with the Bitcoin client, you would just back up on a USB stick or something like that, right? It'd still be a digital backup. And so some people would prefer to have a backup that's physical, that's probably written on a piece of paper. And that means, yeah, then it gets really cumbersome to start writing these hexadecimal things down, if you can even find them.

Aaron van Wirdum: 00:08:54

Right, it's not even about memory. You shouldn't even use your memory. You should write it down either way, but we need an easier way to write it down.

Sjors Provoost: 00:09:01

Yeah, so if you want to, yeah, and I guess that's another thing. So then there was this idea called BIP39, which is a mnemonic, and the idea is really you just take the letters or the hexadecimal numbers and you just map them onto words. So there's 4,000 words and each...

Aaron van Wirdum: 00:09:19

No, there's 2,048 words I think.

Sjors Provoost: 00:09:21

Okay, some number. Those just map onto the numbers.

Aaron van Wirdum: 00:09:24
It's 2 to the 12th. 2 to the power of 12. That's 2,048.

Sjors Provoost: 00:09:29
That sounds like 4,000. Because 2 to the power 10 is 1,000.

Aaron van Wirdum: 00:09:34

No, I'm pretty sure. I looked it up this afternoon. I think it's 2,048 words. But there may be several standards, right? Aren't there several?


Sjors Provoost: 00:09:43

Well, I'm talking about BIP 39.

Aaron van Wirdum: 00:09:44

Me too.

Sjors Provoost: 00:09:46

So there's a number of words, which we'll have to look up. And they really, those words just represent numbers, essentially. So that's that simple. And then...

Aaron van Wirdum: 00:09:54

Basically, it's just the first word is Number 0000 there. They all are four numbers, right? And then the second word is 0001, and that all the way through to 2048.

Sjors Provoost: 00:10:05

Exactly! Now there is a little caveat there. It works one way, as in you start with the numbers. So the numbers are the seed you generated essentially, your computer generated, and then they are converted to words. But when you use it, it's actually not going back to the numbers. So when you enter the words, the next step in order to create this hierarchical wallet is to just process the words as they are written and hash that. It's a little implementation detail that you generally don't have to worry about unless you want to do translations. So basically the first address of your wallet is derived, so you start with this random numbers, those are turned into words, and those words pasted behind each other and maybe with a little password behind it, those are hashed, and that's where the first key come from. But that means that if you have say a German alternative for this BIP39 that if you have the same you start with the same numbers but now you're starting to write German words and knowing you hash the German words you're gonna get a different key than when you hash English words. So you cannot translate one seed into another. That makes no sense.

Aaron van Wirdum: 00:11:25

Right, okay.

Sjors Provoost: 00:11:27

And this is relevant because That's one reason why I don't think it's a good idea for people to use BIP39 in other languages. Because in that case, you know, you may have one piece of software that will understand what to do with the German words, but your other piece of software that you may want to use later, your other wallet, will not understand it. So because as much the.. most of the support is for the English words.

Aaron van Wirdum: 00:11:51

Right okay well anyway I didn't know that I also don't is it important for the rest of the episode or it's just not important for the rest?

Sjors Provoost: 00:11:56

It is one of those things that if we ever had to redo these standards, that we should do better.

Aaron van Wirdum: 00:12:04

Right. I do have another question. So some seeds have 12 words and some have 24.

Sjors Provoost: 00:12:13

Yep.

Aaron van Wirdum:00:12:14

I think these are the two most common amounts of words. Why is there a difference? Is one just more secure? Or..

Sjors Provoost: 00:12:18

Yeah, it's more bits. So 12 words means 128 bits of random data. So basically throwing coins. Yeah, you're basically throwing 128 coins.

Aaron van Wirdum: 00:12:29

For heads or tails. Yeah.

Sjors Provoost: 00:12:32

Yes. Or if you have 24 words, you're effectively throwing 256 coins, heads or tails.
And that is not twice as secure. That is like..

Aaron van Wirdum: 00:12:40

A lot more secure.

Sjors Provoost: 00:12:41

Yeah.

Aaron van Wirdum: 00:12:42

What's the number Sjors? From the top of your head.

Sjors Provoost: 00:12:43

Well, I don't know.

Aaron van Wirdum: 00:12:44

Come on.

Sjors Provoost: 00:12:45

Basically, twice as many bits of security. But that, you know, it takes a lot more time to brute force it, right? Because every bit you add means it takes twice as long to brute force it. If you want to guess what somebody's mnemonic is, you try one combination of words, you try another, you try another, you try another. And if it's a two-bit system, if it's a two-bit seed, well then you just have to try four times. But if it is a four-bit seed, You don't have to try eight times. You have to try 16 times.

Aaron van Wirdum: 00:13:17

So is 12 enough then? Why don't all wallets just use... If some wallets use 24, why don't they all use 24?

Sjors Provoost: 00:13:24

I mean, ultimately, it's better to have more bits of security. If there's no trade-off, why not? Right? And ultimately in the long run, you know, the worry is that as computers get faster or as problems are found, you need more bits to be really secure. And maybe one day we'll reach the point where 128 bit is not secure anymore, but then 256 will last us a bit longer. So it's that kind of long-term thinking.

Aaron van Wirdum: 00:13:51

Is it maybe also partly a human problem? Like some people will cut their seed in half, thinking if they hide them in different places then they're goods, but then if people don't, if someone finds half of 12 seeds.

Sjors Provoost: 00:13:59

Yeah, so then you're getting really in trouble. Because if you have a 12 word seed and you cut it in two, that's six words each. And that is only 64 bits of entropy.That's still a lot, but it might be within the realm of something you can crack. Because again, twice as long does not mean that it takes twice as long to crack it. It means it takes exponentially longer to crack it. So that's indeed one of the risks, but I don't think that's the reason. So basically you could say that the limit of Bitcoin, the way it's architected, is 256 bits. And that is because the hashes of a block, as well as the elliptic curve, all use 64 bits, 256 bits. Right, so if you have a way to crack a 256-bit number, like find the private key, et cetera. That's basically the security level anyway. So you might as well use that.

Aaron van Wirdum:00:14:51

You've broken Bitcoin itself, yeah.

Sjors Provoost: 00:14:52

Yeah, so that's why I guess that's one argument to say, well then, why don't you use seeds that are at that limit? It makes no sense to go beyond it, but it also makes no sense to stay below it. All things equal, because you do have to write these things down or do something else with it. And if that's too much work, then people won't do it. And then you just lose your coins. So The benefit of 12 words is that people are more likely to write them down.

Aaron van Wirdum: 00:15:19

Okay. Now let's get to the meat of this episode. I think that was a long recap of stuff that people already knew, or at least most people already knew most of that. So now we're getting to SeedQR and this is your hobby project. So I guess you just explain what it is.

Sjors Provoost: 00:15:35

Yeah, so as far as I know, it's a proposed standard and there are some tools that are using it. And the idea is that you take these 12 to 24 words and rather than writing them down as words, you convert them into a QR code. Because remember, these things represent numbers. So you just take the word, find the corresponding number, and now you have a bunch of numbers. And if you have a bunch of numbers, essentially, if you have 128 bits of data or 256 bits of data, you can squeeze that into a very small QR code.

Aaron van Wirdum: 00:16:06

Right. And so right now a lot of people are storing their Bitcoin essentially their private keys as a list of, or at least their backup as a list of words. And according to... with this standard, they could back up their keys as a QR code which they hide somewhere.

Sjors Provoost: 00:16:24

Yeah, and so one benefit of that could be...

Aaron van Wirdum: 00:16:27

Is that new? I mean I've never heard of it but it sounds like a fairly obvious thing to do but it's new.

Sjors Provoost: 00:16:34

Yeah I mean it depends really depends on your use case right so if you're if you have your keys in some very far away cold storage place in the middle of the Antarctica well it you know it may be useful for you if you need those words anyway you can either type them or you can scan them. Those are the two ways you can enter them back into a machine. And since most hardware wallets are pain in the ass to type on, maybe using a camera might be easier, but I think only the Jade hardware wallet and the Spectre DIY wallet have cameras, so there's only limited use for QR codes.

Aaron van Wirdum: 00:17:12

Okay, so the general idea is we're using a QR code as a backup? What are the challenges here?

Sjors Provoost: 00:17:19

Yeah, and not just as a backup, it could even be, let's say you have a phone wallet, right? And when you're walking around with your phone, maybe it's a phone wallet that you don't use for shopping, but you do use it for your everyday stuff. It's not like cold storage, it's not a huge amount of money. But when somebody robs you in the street, you don't want to be able to give them Bitcoin, so you don't want to have the private keys on the phone itself. You want to have them somewhere safe at home. And so then a QR code could be useful because when you do want to use it, you just scan the QR code and now boom you can spend your Bitcoin. But when you're on the street nobody can rob you. If they go to your home they can, that's that's a trade-off.

Aaron van Wirdum: 00:17:56

Right, so the idea there would be that your phone doesn't actually store any of the keys, It just scans them for one time use.

Sjors Provoost: 00:18:03

Exactly!

Aaron van Wirdum: 00:18:04

It scans the QR code for one time use and then forgets it. And it can be a phone, it can also be another device. Of course, it could be a hardware wallet that operates like this. So then the keys aren't even on the device.

Sjors Provoost: 00:18:12

Yeah, well, they are when you're using it, but after that they're not, well, unless it was compromised.

Aaron van Wirdum: 00:18:17

Right, so rather than thinking of it as a backup, in that case, it is essentially your actual cold store wallet.

Sjors Provoost: 00:18:26

Yeah, or at least your actual offline, semi-offline wallet or something like that.

Aaron van Wirdum: 00:18:30

Right, right, right. Okay, so are there any, what are the challenges to accomplishing this? If there are any.

Sjors Provoost: 00:18:38

Well, for one thing is, again, it depends on the use case. For the easy use case where you are printing a QR code with a physical printer, then I guess it doesn't matter, right? You can make a very big QR code or a small one doesn't matter but when you as we described in the beginning you want to write down your QR code on a piece of paper which you can draw it's nice if the QR code is not too many little points because it's very tedious to do it. And if you want to put them on metal, then you really don't want to have 5,000 little points that you need to put on the QR code.

Aaron van Wirdum: 00:19:10

Right. And I guess the reason this matters is that you ideally don't want to have your private keys touch a computer at all, possibly, or a printer at all. These things can be hacked, and I think some printers even have memory of stuff they printed. Ideally it just flash on your hardware wallet or something, and then you write it down with a pen and paper.

Sjors Provoost: 00:19:35

Exactly, and that's what the Seed Signer does. So the Seed Signer, this sort of open source device, you can buy off the shelf components and make it yourself. What this device does is you enter your words and it shows you the QR code, or you scan the QR code and it shows you the words. And then I think that device can also sign things but maybe you don't want to use that part maybe you want to use your regular hardware wallet for the signing so you then take your mnemonic and put it in your regular hardware wallet something like that that could be the operation flow And that means you're not using your main computer, which will probably have millions of viruses on it. You're not using your printer, which will probably have millions of viruses on it. And then it's really important because you're doing this step by hand, you're drawing a QR code, the drawing part should be as little work as possible.

Aaron van Wirdum: 00:20:16

Right.

Sjors Provoost: 00:20:17

So then they've done some research about how small these QR codes can get.

Aaron van Wirdum: 00:20:22

And how small can these QR codes get?

Sjors Provoost: 00:20:23

For 12 words, you can use 21 by 21 points. And a large part of that, if you look at a QR code, there's these giant rectangles, right? So it's 21 by 21, including those giant rectangles.

(Ad removed)

Aaron van Wirdum: 00:21:34

How small can QR codes get in general? Is there..

Sjors Provoost: 00:21:36

21 by 21. At least..

Aaron van Wirdum: 00:21:39

Is that the smallest type of QR code?

Sjors Provoost: 00:21:40

I believe that is the smallest type of a regular QR code. There is also a micro QR like standard that is even smaller, but that is useless for this purpose. So if you look at my book, maybe I'll just shamelessly shill that I have a book.

Aaron van Wirdum: 00:21:53

We're shilling all the way.

Sjors Provoost: 00:21:54

'Bitcoin: A work in progress' or just Google 'Bitcoin Sjors'. You'll need to know how to spell that anyway.

Aaron van Wirdum: 00:22:01

No one knows Sjors.

Sjors Provoost: 00:22:04

That's all right. What was I saying? Yeah, so the book actually contains QR codes that will take you to various resources, right? So you don't have to type the whole URL, you scan the QR code, it takes you to a short URL. Those short URLs fit exactly into the smallest possible QR thing of the 21 by 21. That's "http://..."

Aaron van Wirdum: 00:22:26

Okay

Sjors Provoost: 00:22:27

But you can also put a seed in it.

Aaron van Wirdum: 00:22:29

So the smallest, at least the smallest sort of regular QR code is 21. Do you know what QR stands for, Sjors?

Sjors Provoost: 00:22:36

Quick response.

Aaron van Wirdum: 00:22:37

Very well, very good. So the smallest QR code is 21 by 21. And then there are bigger ones.

Sjors Provoost: 00:22:46

Yeah, and so the reason you want to use bigger ones is, for example, because you have more words that you want to put into it.

Aaron van Wirdum: 00:22:52

Right.

Sjors Provoost: 00:22:53

So I think you need a 25 by 25 to have 24 words. And the other thing you can do is increase the error correction. And so what a QR code does is it shows you, the QR code starts with the actual thing that it's describing, so say a URL or piece of text, and then it has a bunch of extra bits and a bunch of extra pixels and their purpose is to basically help the device that's scanning it to correct for errors because the camera might not be accurate.

Aaron van Wirdum: 00:23:19

Yeah or you know your ink may be blurry.

Sjors Provoost: 00:23:25

Yeah so basically you know some people abuse this feature. They'll put the company logo in the middle of a QR code and what that does is basically it obscures part of the QR code but because it has so much error correction you can actually obscure 5 or 10% of the QR code and still read it. That's the idea. We talked about error correction in an earlier episode I believe about this mempool sync project.

Aaron van Wirdum: 00:23:48

Okay.

Sjors Provoost: 00:23:49

Mini sketch.

Aaron van Wirdum: 00:23:50

I don't remember, well, I kind of remember vaguely, but let's get back to the point. So we're using 21 by 21 QR codes. Or bigger?

Sjors Provoost: 00:23:59

Yeah.The Seed QR standard uses several different sizes of QR codes.

Aaron van Wirdum: 00:24:04

Right. And is there any sort of... I recall they're doing some tricks to actually make it fit. Is that not the case?

Sjors Provoost: 00:24:14

Yes..So, yeah, exactly. There are two ways to put the data into the QR code. One is a way that is as compact as possible. That's where you get the 21 by 21. And the other is a way that other apps can actually read it. So the problem is when you use the most compact way to store it, there are not a lot of off-the-shelf applications that can actually read this QR code. So if you point your phone at it, if you use this very compact form, your phone will be confused. It won't understand what to do with the QR code.

Aaron van Wirdum: 00:24:44

Right.

Sjors Provoost: 00:24:45

That's kind of a feature, actually, because you don't want it to. But...

Aaron van Wirdum: 00:24:48

They've used optimisations that other apps don't understand. Is that the right way to put it?

Sjors Provoost: 00:24:53

Basically, when you scan a QR code, your phone is generally expecting a URL or at least regular text. But these things will use full, basically 256-bit ASCII. So if you ever go... I don't know if you've ever seen some binary file and you open it up and it has all these symbols and your computer starts beeping at you.

Aaron van Wirdum: 00:25:14

Yeah.

Sjors Provoost: 00:25:15

So that's basically what's in the QR code too. It's using all the bits it can and so your phone thinking it's text will render complete gibberish. In fact, it will just not work.

Aaron van Wirdum: 00:25:26

Right, okay.

Sjors Provoost: 00:25:32

But I think that's all solvable.

Aaron van Wirdum: 00:25:33

And what you were saying is that in a way, it's kind of nice that it does that because if some random person finds this QR code that has all your money on it, then it's kind of nice if they don't understand what it is.

Sjors Provoost: 00:25:43

That's one nice thing about QR codes. So now, you can start thinking about where could these fit into your security model. Well, if you're traveling with 12 words written on a piece of paper, if the customs search your bag, they'll see the 12 words, they know what to do with it. Maybe if you have say a vaccination password that has a bunch of QR codes on it anyway, you kind of shove in your little Bitcoin backup in that password and maybe they won't see it. But that's, you know, that's always a little scary.

Aaron van Wirdum: 00:26:13

Okay, so far this all sounds great. Also kind of straightforward. Is this just a straightforward episode or is there some magic still waiting in the corner? Where are we taking this?

Sjors Provoost: 00:26:23

My magical suggestion would be that yeah, this is pretty straightforward, but I would say that the downside of QR is that it is designed for computers. So it's very easy for computers and cameras to scan it. You can read it by hand as in there's a couple of YouTube videos and documents that you can read that will explain to you if you see QR code how to read it. It's very difficult. So what I would like to see is another standard, a new standard that kind of looks like a QR, but that is much easier for a human to read. So that means you wouldn't even need the Seed Signer device. You would just be able to take a pen and paper and just look at where the squares are and do some math and then you would actually know what the seed is.

Aaron van Wirdum: 00:27:13

I'm just thinking of the...

Sjors Provoost: 00:27:15

Yeah I know which XKCD you're thinking about.

Aaron van Wirdum: 00:27:18

Which one is it?

Sjors Provoost: 00:27:19

But this standard might actually already exist

Aaron van Wirdum: 00:27:21

There are 14 competing standards. 14 ridiculous... anyways. I think everyone knows it I'm not gonna finish the joke

Sjors Provoost: 00:27:29

Yeah so I don't necessarily think there has to be a new standard. It may be that there's already our standards out there that are designed for humans to parse rather than for cameras to parse. Yeah.

Aaron van Wirdum: 00:27:39

Okay well let's see if someone develops that then Sjors. Why don't you? Why don't you develop a new standard? We need the 15th standard.

Sjors Provoost: 00:27:45

Because I'm not an encoding master.

Aaron van Wirdum: 00:27:47

Okay, well, I'm not gonna do it either. So hopefully one of our listeners will feel inspired by your encouragement.

Sjors Provoost: 00:27:54

I hope SIPA picks it up because it'd be nice to have some error correction. Let's say you have a QR code, right? And QR code is every, if you read it from left to right, basically it's either black or it's white. So it's like a bit. So you could imagine having a device where you're clicking a button, either the left button or the right button. If you see a white pixel, you click the left button. If you see a black pixel, you click the right button. And then based on that click, click, click, click, click, click pattern, it reconstructs your seed. And it's nice if there's error correction while you're doing that. So rather than typing all the 24 words as you would now, and then it says, nope, sorry, it's wrong. Every six or seven characters, it would tell you, no, no, no, you did something wrong. And then you know that you have to go back and check the last seven characters because you know it's it's not easy to manually type something like a QR code without making mistakes so I think there's this promise there.

Aaron van Wirdum: 00:28:46

Okay.

Sjors Provoost: 00:28:47

But, that's all I got.

Aaron van Wirdum: 00:28:49

Okay, so when are you gonna make yours?

Sjors Provoost: 00:27:51

Oh, I don't know, whenever.

Aaron van Wirdum: 00:28:52

Your steel plate?

Sjors Provoost: 00:28:53

Whenever it arrives. I'll go play with it.

Aaron van Wirdum: 00:28:55

You're waiting for the actual plates to arrive? that's what you're waiting for?

Sjors Provoost: 00:28:58

Exactly.

Aaron van Wirdum: 00:28:59

All right. Well, you got that you got the rest of the tools ready. Sjors, I think that's it then. I think that's our episode. Sounds good. Thank you for listening to Bitcoin Explained.
