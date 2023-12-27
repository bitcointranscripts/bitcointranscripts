---
title: "Explaining Bitcoin Addresses"
transcript_by: mubarak23 via review.btctranscripts.com
media: https://www.youtube.com/watch?v=R1kF1rnLvM8
tags: ["script", "bech32"]
speakers: ["Sjors Provoost","Aaron van Wirdum"]
categories: ["podcast"]
date: 2021-02-19
---
Aaron van Wirdum: 00:01:45

Live from Utrecht this is the Van Wirdum Sjorsnado.
So the other day I wanted to send Bitcoin to someone, but I didn't.

Sjors Provoost: 00:01:52

Why?
Shouldn't you hodl?

Aaron van Wirdum: 00:01:55

I hodl all I can, but sometimes I need to eat, or I need to pay my rent, or I need to buy a new plant for my living room.

Sjors Provoost: 00:02:05

Yeah, let's do.

Aaron van Wirdum: 00:02:06

So the problem was, the person I wanted to send Bitcoin to, I didn't have their IP address.

Sjors Provoost: 00:02:11

You did not have their IP address?

Aaron van Wirdum: 00:02:13

I did not have their IP address.
Luckily, it turns out there's this trick in Bitcoin called Bitcoin addresses.

Sjors Provoost: 00:02:21

That's right.

Aaron van Wirdum: 00:02:21

Have you heard of this?

Sjors Provoost: 00:02:23

Yes.

Aaron van Wirdum: 00:02:24

Maybe our listener hasn't yet, Sjors, so let's explain what Bitcoin addresses are.

Sjors Provoost: 00:02:30

Okay, what are Bitcoin addresses?

Aaron van Wirdum: 00:02:33

First of all, so I made a stupid joke about IP addresses, but this was actually an option, wasn't it?

Sjors Provoost: 00:02:38

In the initial version of Bitcoin, Satoshi announced it on the mailing list and said, well if you want to send somebody some coins, you just enter their IP address and then it'll exchange, I guess, an address to send it to.

Aaron van Wirdum: 00:02:51

So it was actually possible to send Bitcoins to people's IP addresses.
I don't think that's possible anymore.
That's not in any of the code.

Sjors Provoost: 00:02:58

I don't think so either.
I haven't seen it.
because the other way is that you just get an address to send to, and then it goes to the blockchain.
And because the other side is checking the blockchain also, it'll show up.

Aaron van Wirdum: 00:03:10

Well, that's actually not how it works at all.
But we're going to explain it now, I think.
Let's go.
Okay.
First of all, Sjors, when you send Bitcoin to someone, what do you actually do?
What happens?

Sjors Provoost: 00:03:22

Well, you're creating a transaction that has a bunch of inputs, and it has an output.
And that output describes who can spend it.
So you could say anybody can spend this.
That's not a good idea.
We talked about that in an earlier episode.
So what you do is you put a constraint on it.
And the very first version of that constraint was he or she who has this public key can spend the coins.
So that's called pay-to-public-key.

Aaron van Wirdum: 00:03:49

We just mentioned this IP example.
So what actually happened was you would connect to someone's IP.
I don't know the nitty-gritty details, but in general, you would connect to someone's IP and you'd ask for a public public key and that person would give you the public key and I think that's what you send the bitcoins to.

Sjors Provoost: 00:04:08

Yeah I believe so too but I haven't seen that code in action so we could be slightly wrong there somebody should dig it up, I'd love to see screenshots of like what that used to look like.

Aaron van Wirdum: 00:04:14

is there anyone who's ever used this way of paying someone pay to IP address?

Sjors Provoost: 00:04:23

Yeah we'd love to know.

Aaron van Wirdum: 00:04:24

It was technically possible.
If anyone listening has ever actually used this We'd be curious to hear that.

Sjors Provoost: 00:04:31

I mean, it makes sense to think that way in the first version of Bitcoin.
Because before that, you had all these peer-to-peer applications and they were generally very direct, so with Napster and all these things, or Kazaa, I don't know which one, you would connect to other people and you would download things from them.
And with Bitcoin, you connect to other peers, but nowadays you just connect to random peers.
But perhaps in the beginning, the idea might've been, okay, you connect to peers you know, and so then you might as well do transactions with them.
But right now you don't really do transactions with the peers you're directly connected to.
At least not in Bitcoin on-chain.

Aaron van Wirdum: 00:05:05

So that's one way of paying someone to a public key, is you'd connect to their IP address and you'd get their public key.
The other way is if you mine Bitcoins.
So if you're a miner, then you're actually sending the block rewards to your public key.
Is that still the case?
It used to be the case in the beginning.

Sjors Provoost: 00:05:24

Well, in the beginning, Bitcoin had a piece of mining software built into the software, right?
So if you downloaded the Bitcoin software, it would just start mining.
And so it would use that mechanism.

Aaron van Wirdum: 00:05:35

Well, you just have to press a button.

Sjors Provoost: 00:05:37

And then later on, you had mining pools and it all became more professional.
So the way they would pay out might be very different.
Probably, you know, might go to a multi-sig address from which it's paid back to the individual pool participants, or it could be paid directly to the pool participants, although that's a bit inefficient because you need a long list of addresses in the Coinbase, but I've seen huge Coinbase transactions, so probably people were doing that.

Aaron van Wirdum: 00:06:06

Right.
Well, anyway, so the point I was making was this pay to public key way of paying someone.
I learned this while doing a little bit of research for the show.
That was only ever really used for pay to IP address and for the block reward.
It wasn't actually used for anything other than that.
What was used other than that was pay-to-public-key-hash. 
So you're not sending money to a public key, but you're sending money to the hash of that public key.
And this is where addresses come in.
Because this type of payment actually used addresses for the first time.
Not for the first time, this was always there.
Also something I learned while doing a little bit of research.
This was there since day one.
There were Bitcoin addresses since day one, but they were only there for pay-to-public-key-hash.

Sjors Provoost: 00:06:58

So the script on the Bitcoin blockchain would in that case say, okay, the person who can spend this must have the public key belonging to this hash.
So the nice thing about that is that you're not saying which public key you have, or at least at the time it was thought that maybe that was safer against quantum attacks.
But the other benefit is that it's a little bit shorter, so it saves a bit on block space, although, of course, that wasn't an issue back then.
So yeah, you pay to the public key hash.

Aaron van Wirdum: 00:07:27

I guess in a way, it's slightly more private as well, right?
Because you're only revealing your public key when you're paying?
No, that doesn't make sense.

Sjors Provoost: 00:07:35

Exactly, (it) doesn't matter.

Aaron van Wirdum: 00:07:37

Okay, so that's paying to public key hash.
And like you said, what you see on the blockchain itself, what's recorded on the blockchain is the actual hash of a public key.
However, when you're getting paid on a pay-to-pubkey-hash, what you're sharing with someone is not this hash, it's actually an address.

Sjors Provoost: 00:08:02

Yes, well you are sharing the hash, but you do that using an address.

Aaron van Wirdum: 00:08:07

Exactly, so what is an address?

Sjors Provoost: 00:08:09

So an address essentially is, at least this type of address, is the number one followed by the hash of the public key.
But it is encoded using something called base58.

Aaron van Wirdum: 00:08:20

What's base58?

Sjors Provoost: 00:08:22

Okay so let's go back to base64, I don't know if you've ever seen an email source code like an attachment all these weird characters in there that's base64.
base58 is based on that, but maybe to say what it is, it is all the lowercase letters, all the uppercase letters, and all the numbers, and without any of the signs, and with some ambiguous things removed.
So you do not have the small O, the big O, and the zero.

Aaron van Wirdum: 00:08:50

Should we start with base10?
I want people to understand what base means.

Sjors Provoost: 00:08:58

Yeah exactly.
So this is what's in base58, but then the question is what is base?
And so base10 is you have 10 fingers and so if you want to express say the number 115 you can make three gestures, right?
You show a one and a one and a five and that is base10 because you're using your 10 fingers three times and that's also how you write down numbers but there have been different bases.
I think the Babylonians were very much into base 360 that's why we have...

Aaron van Wirdum: 00:09:27

Hang on hang on because we're not actually using fingers most of the time so I want to make this clear that it just means there we have a decimal system so that means we have 10 different symbols that represent a number.

Sjors Provoost: 00:09:45

This probably not a coincidence that that happens to match.

Aaron van Wirdum: 00:09:48

I totally agree, I just want to make it clear that we're not actually using fingers most of the time.

Aaron van Wirdum: 00:09:54

Okay, so we have 10 symbols, so that means that once you get by the 11th number, at that point you're going to have to reuse symbols you've already used, so you're now going to use combinations.
So in our case, that would be, well it's going to get confusing because the first number is a zero, so then the 11th number is the one and the zero.

Sjors Provoost: 00:10:13

Exactly, and there have been different bases in use, right?
So base360 I believe was used by Babylonians, or maybe base60.
And then for computers we tend to use base2 internally, because chips are either on or off, so it's 0 or 1, so a long series of 0s and 1s.
And you can express any number of that now in order to read machine code typically you would use hexadecimal which is base16 so that is 0 to 9 and then a to F.
So base58 is basically this 58 possible characters to express something with.

Aaron van Wirdum: 00:10:51

Yeah, it's all numbers and there's different ways of expressing a number based on your base.
That determines how many symbols you're using.

Sjors Provoost: 00:11:02

Right, the trade-off here is readability really, because you could represent machine code as normal characters, so the ASCII alphabet, or the ASCII character set is 256 different characters, so that's base256.
But if you've ever done something like print and then the name of a file, your computer will show complete gibberish on the screen and it will start beeping.
And the reason it starts beeping is because one of these codes, somewhere in the base256 is a beep, which actually makes your terminal beep.
So it is completely impractical to view a file using base256, even though there is a character for every of the 256 things there.
So that's why you tend to do that in base16.
Hexadecimal is relatively easy to read, but then it's quite long.
If you take a public key and you write it as hexadecimal it's a rather long thing to write down but and base58 is a little bit shorter so maybe you know it's easier to copy paste perhaps.
It's not even easy to read on the phone, base58 is pretty terrible because it's uppercase, lowercase, uppercase, lowercase.

Aaron van Wirdum: 00:12:05

Just to restate that briefly.
So base2 is just you're just using two symbols, which is 1 and 0.
And base10 is what we use most of the time.
It's 0, 1, 2, 3, 4, up until 9.
Then you have hexadecimal, which uses 0 through 9, plus A, B, C, D, E, F.
And then what we're talking about here is base58, which uses 58 different symbols, which are 0 through 9, and then most of the alphabet in both capital letters and undercase, right?

Sjors Provoost: 00:12:40

Yeah, I think it's lowercase and uppercase, and then most of the numbers, but there are some letters and numbers that are skipped that are ambiguous.
So the number 0, the letter O, both lowercase and uppercase, or at least uppercase is not in there.

Aaron van Wirdum: 00:12:53

I think for example the capital "I" and the lowercase "l" are both not in there because they look too similar.

Sjors Provoost: 00:13:01

Right, and that's why you get a little bit less than, you know, if you just add 26 letters plus 26 uppercase plus 10 numbers, right?

Aaron van Wirdum: 00:13:09

So I think we finally explained what base58 means.

Sjors Provoost: 00:13:11

And just as a side step, I talked about email earlier, that's base64.
That is the same, but it also has some characters like underscore and plus and equals and that was mostly used for email attachments and I guess they didn't want to use all 256 characters either because they didn't want the email to start beeping but they did want to squeeze a lot of information into the attachment.

Aaron van Wirdum: 00:13:32

Okay, that's base58.
Now, why are we talking about this?
What is an address?

Sjors Provoost: 00:13:37

So the address is the value 0, I believe, but that's expressed as a 1 because that's the first digit in this character set (base58).
So it starts with a 1 and then it's followed by the public key hash, which is just expressed in base58.

Aaron van Wirdum: 00:13:54

Right, is that all it is?

Sjors Provoost: 00:13:56

Yes, and keep in mind, so that is the information you send to somebody else when you want them to send you Bitcoin.
You could also just send them 00 and then the public key and maybe they would be able to interpret that.
Probably not.
You could send them the actual script that's used on the blockchain because on the blockchain there is no like base58 or base64 or anything like that.
The blockchain is just, binary information.
So the blockchain has this script that says, if the person has the right public key hash, has the public key belonging to this public key hash, then you can spend it.
And we talked about in an earlier episode how Bitcoin scripts work.
So you could send somebody the Bitcoin script in hexadecimal, anything you want.
But the convention is you use this address format.
And that's why all traditional Bitcoin addresses start with a one.
And they're all the same, roughly the same length.

Aaron van Wirdum: 00:14:45

Okay, so a Bitcoin address is basically just a base58 representation of a version number plus a public key hash.
Sjors, is base58 used for anything else in Bitcoin?

Sjors Provoost: 00:15:01

You can also use it to communicate a private key and then that case your version number is - well it's written as 5 - but it actually represents I think 128 and then followed by the private key.

Aaron van Wirdum: 00:15:13

So that's why all private keys start with a 5 or at least used to start with a five?

Sjors Provoost: 00:15:19

In the old days you had paper wallets that you could print and if you generate them actually securely without a backdoor then on one side of the piece of paper you would have something starting with a five and on the other other side of the paper you would have something started with a one and then it would say like show this to other people and don't show this to other people.

Aaron van Wirdum: 00:15:36

Right now I happen to know Sjors that there are also addresses that start with a three.
What's up with that?

Sjors Provoost: 00:15:44


Well usually those are multi-signature addresses but they don't have to be.They could be single signature addresses.
What they are are...

Aaron van Wirdum: 00:15:51

They could also be types of segwit addresses.
There could be many things, right?
They could also be single sig, But you already mentioned that.
So let's go on.
Okay, three.
It starts with a three, what does it mean?

Sjors Provoost: 00:16:04

So it basically says pay-to-public-key-hash.
So it is that number.

Aaron van Wirdum: 00:16:08

Pay to public script hash.

Sjors Provoost: 00:16:10

Sorry, public script hash.
Well, not even public, just pay-to-script-hash.

Aaron van Wirdum: 00:16:14

We're getting there.

Sjors Provoost: 00:16:15

We're getting there.

Aaron van Wirdum: 00:16:16

Eventually, pay-to-script-hash.

Sjors Provoost: 00:16:17

Yes, and it says basically anybody who has the script belonging to this hash and who can satisfy the script.
So just knowing the script is not enough, you actually have to do whatever the script says you should do.

Aaron van Wirdum: 00:16:30

Yeah, so the first version we just described was pay-to-public-key-hash, which required people to offer a valid signature corresponding to the public key.
And now we're talking about pay-to-script-hash, which means someone needs to present the script and be able to solve the script.
So why do these start with a three?

Sjors Provoost: 00:16:51

There's just a convention.
So as we said, everything that you communicate through base58 starts with a version number.
And if it starts with a 1 then you know it's pay-to-public-key-hash if it starts with a 3 you know it's pay-to-script-hash if it starts with a 5 you know it's a private key.
So it's just a convention and has no meaning on the blockchain itself.

Aaron van Wirdum: 00:17:13

Once again all this is is a version number plus this hash represented in base58.
Is that all it is?
This is all so much simpler than I once thought, Sjors.

Sjors Provoost: 00:17:26

No, it's really simple.
And the only mystery that has been solved today, I guess, is, well, what if you only use the public key but that wasn't done using this system so there is no initial letter that would represent trying to do that.

Aaron van Wirdum: 00:17:40

Yeah that was never represented in base58

Sjors Provoost: 00:17:42

Otherwise probably that would have been version 0 and then all normal addresses might have started with the two, who knows.

Aaron van Wirdum: 00:17:48

I think for anyone who already knew this which is probably a good chunk of people this is a very boring episode so far but I think it's gonna get better because Sjors we now have a new type of address since a year or two, which starts with BC1.

Sjors Provoost: 00:18:09

BC1Q even, usually.

Aaron van Wirdum: 00:18:11

Yeah, usually, but not always.
And we're getting into that, I think.
So what is this all about?

Sjors Provoost: 00:18:16

Well, that is BECH32 or however you want to pronounce it.
And it's been used since SegWit, basically.
And again, it is something that doesn't exist on the blockchain, so it's just a convention that wallets can use.
This is a, as the name suggests, a base32 system.
Which means you have almost all the letters, and almost all the numbers, minus some ambiguous characters that you don't want to have, because they look too much like numbers or letters.

Aaron van Wirdum: 00:18:46

I think one of the big differences compared to base58 is that this time there are no longer uppercase and lowercase letters.
Every letter is only in there once.

Sjors Provoost: 00:18:58

Exactly.

Aaron van Wirdum: 00:18:59

I'll mention one benefit of that, which is that if you want to read an address out loud it's going to be a little bit easier now that there's no difference between uppercase and lowercase.

Sjors Provoost: 00:19:11

The other difference is, I didn't check with base58, but basically it doesn't start with zero or anything like that.
It looks pretty arbitrary.
So the value zero is written as a Q, the value one is written as a P, the value two is written as a Z, etc.

Aaron van Wirdum: 00:19:27

Why is the value one just written as a one?

Sjors Provoost: 00:19:30

Well it's completely arbitrary first of all, right?
You can pick any, you can connect any value to any symbol you want.
I f there is a human interpretation that depends on it, then you don't want to do anything confusing.
But if your only goal is to make it easy to copy paste things and if your other goal is for every address to start with BC1Q because you know BC1 sounds cool then maybe there's a reason why you want to do them out of order I haven't read what the rationale is in the order.

Aaron van Wirdum: 00:20:02

Okay, now BECH32.

Sjors Provoost: 00:20:05

Yeah, so there's a set of 32 characters, but it's doing the same thing, right?
It's again saying, okay, here's a pay-to-public-key address.
In this case, a pay-to-witness-public-key-hash because it's using segwit but it's the same idea.
So it says hello, and then followed by the hash of the public key

Aaron van Wirdum: 00:20:30

So BECH32 addresses what are we looking at exactly.
Because what we're seeing for each address, it starts with BC1 and then usually a Q and then a whole bunch of other symbols.
So what does this all mean?

Sjors Provoost: 00:20:43

That's right, so there is something called the human readable part.
And that doesn't really have any meaning other than that humans can recognize, okay, if the address starts with BC, then it refers to Bitcoin.
And the software of course can see this too, but both humans and software can understand this.

Aaron van Wirdum: 00:20:58

So if Litecoin would want to use these kinds of addresses.
Maybe they do actually, I don't know.

Sjors Provoost: 00:21:04

Probably, then they might start with LT.

Aaron van Wirdum: 00:21:06

Exactly.
So these first two letters just refer to which currency is this about.
What blockchain is this for.

Sjors Provoost: 00:21:12

And it can be, I think, a fairly arbitrary number of letters.
The idea is that it's separated by a one.

Aaron van Wirdum: 00:21:17

Oh, it could be more than two letters as well?

Sjors Provoost: 00:21:19

I think initially Bitcoin Cash was using a much longer introduction.

Sjors Provoost: 00:21:24

So that's pretty arbitrary.
Obviously, you want to conserve space, so BC is nice and short and a one, that's a separator, has no value.
So if you look at the, what do all the 32 numbers mean, then 1 is not in it.

Aaron van Wirdum: 00:21:36

One just means, The human readable part is over, now the fun stuff starts.

Sjors Provoost: 00:21:43

And the fun stuff, it's a little bit easier actually than with base58, because there's a convention.
The convention is it starts with the SegWit version, so the first version of SegWit is 0, which in BECH32 is written as Q.
And then it's either followed by 20 bytes or 32 bytes.
And that is, then it means either it's the public key hash, or it is the script hash.
And they're different lengths now because SegWit uses the SHA-256 hash of the script, rather than the RIPEMD-160 hash of the script.
So in base58 the script hash is the same length as the public key hash but in segwit they're not the same length.
So simply by looking at how long the address is, you know whether you're paying to a script or you're paying to a public key.
So we don't have to say it.

Aaron van Wirdum: 00:22:36

So to reiterate the first two letters, B C, that just means this is about Bitcoin.
Then the 1 says, okay, that was the part telling you which currency this is.
Now pay attention where you're actually going to pay money to.
Then the Q means which version is going to follow, which version of segwit.
And then what comes after it is actually the BECH32 representation of this hash, which is either pay-to-public-key-hash or pay-to-script-hash.

Sjors Provoost: 00:23:08

Yeah exactly or pay-to-witness-public-key-hash or pay-to-witness-script-hash.

Aaron van Wirdum: 00:23:12

Sjors is there anything else cool about BECH32?

Sjors Provoost: 00:23:16

Yeah there is and it's about error correction.
So in base58 there is a checksum.
So a checksum basically means you add something to the address at the end and that way if you make a typo then that checksum at the end of the address is not gonna work.

Aaron van Wirdum: 00:23:34

They're gonna compute with the rest of the address.

Sjors Provoost: 00:23:36

So it'll tell you, okay, this address is wrong.
Now there is a certain chance...

Aaron van Wirdum: 00:23:40

It doesn't tell you what the correct version would be, it just tells you this is wrong.

Sjors Provoost: 00:23:44

Exactly.
Now there is a chance that you make a typo that happens to have a correct checksum.
I don't know what the odds are with base58, they're pretty low.

Aaron van Wirdum: 00:23:53

You'd probably have to make several typos.

Sjors Provoost: 00:23:55

Well, yeah, you'd have to have the unlucky typo.
I don't know if the odds are 1 in 10,000 or 100,000 or something.
But there's a lot of Bitcoin users.
But in BECH32 it's actually better because it will not just tell you that there's a typo, it'll tell you where the typo is.
And that's done differently.
So where we talked about in the base58 system, there is a checksum which basically takes all the bytes from the address and then hashes it.
Here there is very sophisticated mathematical magic.
I don't think it's super sophisticated, but I can't explain what the actual magic is.
But the magic makes it so that you can actually make a typo and it'll actually tell you where the typo is.
And you can make about four typos and it'll still know where the typo is and what the real value is.
If you do more than that, it won't.
And the analogy I like to make with that, as someone once told me, is it's like if you have a wall and you draw a bunch of circles on it, and each circle represents a correct value, and you're throwing a dart at it, and you might hit the bullseye, then you have the right value, or you might just slightly miss the bullseye, but you're still within that big circle, then you know exactly where it should have been.

Aaron van Wirdum: 00:25:11

Are you talking about interlocking circles?

Sjors Provoost: 00:25:13

No, they're not overlapping.

Sjors Provoost: 00:25:16

So the idea there is you want the circles to be as big as possible, obviously, but you don't want to waste any space.
So that's an optimization problem in general.
And of course, in the example of a two-dimensional wall with two-dimensional circles, it's pretty simple to visualize, right?
You throw the dart and you see okay it's still within the big circle so it should belong to this dot so that is like saying okay here's your typo and this is how you fix it.
But and in the case of BECH32 the way I think you should imagine it is that instead of a two-dimensional wall you have a 32 dimensional wall and the circles are also probably 32 dimensional hyperspheres.

Aaron van Wirdum: 00:25:53

I find that a little bit hard to imagine Sjors but I'm not a wizard like you.

Sjors Provoost: 00:25:58

Well, if you've studied something like physics or math, you know that anything you can do in two dimensions you know you can see it in three dimensions and you can do it in n dimensions you can abstract all these things out to to as many dimensions as you need but the general intuition is the same so now you're hitting your keyboard and somewhere in that 32 dimensional space you're slightly off, but you're still inside this sphere whatever that might look like and so it knows where that mistake is.
But there's a problem, all this amazing wizardry missed something.

Aaron van Wirdum: 00:26:32
It lost me a long time ago but go on.

Sjors Provoost: 00:26:35

Well basically it turns out that if your BECH32 address ends with a P, then you can add an arbitrary number of Qs to it and it still will match the checksum.

Aaron van Wirdum: 00:26:47

That was a bug in BECH32.

Sjors Provoost: 00:26:51

So I guess the analogy would be that the circles are not entirely separate in some weird way.
And that's not good.
But that's actually not a problem originally.

Aaron van Wirdum: 00:27:01

So any address that ended with a P could have any arbitrary numbers of Q following it.
And then you wouldn't be told that there's a typo.
Your software would think it's right and then you're sending money to the wrong address.

Sjors Provoost: 00:27:16

Yeah, which means it's unspendable.

Sjors Provoost: 00:27:18

But the good news is that there's another constraint for the original version of segwit, segwit version 0, which is that an address is either well 20 bytes or 32 bytes.
And that means that it's constrained because if you add another Q to it then it's too long so you still know it's wrong.

Aaron van Wirdum: 00:27:35

Yeah if you have a 20 byte address and you add one Q then it's 21 which is still invalid so you'd have to accidentally add 12 Qs. That's pretty unlikely to happen

Sjors Provoost: 00:27:49

I might be confusing bytes and characters, but exactly.
That's very unlikely to happen for SegWit version 0.
But now we would say, okay, we're going to have future versions of SegWit, such as Taproot.
Which would be BC1P, because P is version 1.
And I believe for Taproot, there's also a constraint in how long these addresses are supposed to be.
So it's still not an acute problem but in the future maybe we want to have addresses that are somewhat more arbitrary in length because maybe you want to add some weird conditions to it or you want to communicate other information not just the address maybe you want to put the amount inside the address.

So this is why there's a new standard proposed BIP350 which is called BECH32m and it's actually a very simple change.
I think it adds to the all the math it adds one extra number to that math.
And then it fixes that particular bug.
And everybody's happy.

Aaron van Wirdum: 00:28:51

So it fixes the bug that the Qs don't matter anymore.

Sjors Provoost: 00:28:56

Yeah, you can't just add stuff to it without running into problems.

Aaron van Wirdum: 00:29:00

But I guess this does mean that wallets that have by now upgraded to support these special SegWit addresses, BECH32 addresses, they now have to upgrade again.

Sjors Provoost: 00:29:11

That's right.
So that's annoying, because it does mean that if your wallet wants to support sending to a taproot address, then it has to make a small change to the BECH32 implementation.
And there's some example code on the BIP.
It's not a big change because it just adds one number and if you look at the Bitcoin Core implementation it's a fairly simple change that does it.
But it does mean that moving forward when you see a BECH32 address you have to parse it, then see if it's the version 0 or the version 1 and then do things slightly differently but even that is just a very small change.
But it is annoying, it does mean that especially hardware wallets, you know, with firmware updates could take a while.

Aaron van Wirdum: 00:29:51

Right, so we started out with base58 addresses, now we're all starting to use BECH32 addresses.
Is this final?
Are we going to keep using BECH32 or are you anticipating some other address format somewhere in the future?

Sjors Provoost: 00:30:07

No, I think this will do for a long time.
BECH32 is a way to write addresses.
Now, what is actually inside an address, there could be more information in it, right?
And the most interesting example of that is Lightning Invoices.
Lightning Invoices uses BECH32, but they're much longer because they contain a lot more information.
They contain the public key, they contain the amount, they contain the deadline, they contain a bunch of secrets, they contain all sorts of stuff, all sorts of routing hints even.
It's like a whole book you're sending over.
So BECH32 is just an alphabet essentially.
You can make it as long as you want with this little caveat in mind that we talked about, but you're probably not going to type, manually type Lightning invoices anyway, because they're too long.
So you tend to copy paste them.

Aaron van Wirdum: 00:30:52

Yeah.
And generally you copy paste any address.
I don't retype addresses.
Do you, Sjors?

Sjors Provoost: 00:30:58

Well, you might have some like nuclear cold storage and the addresses for that nuclear cold storage might be written down on a piece of paper because you don't want them ever to touch anything that's on the internet.
But generally people copy paste.
But there was some discussion early on with BECH32, I think, that was explicitly talking about can this be communicated over the phone.
Even in your nuclear bunker situation, maybe you need to communicate something to somebody else in another nuclear bunker through smoke signals.
And then, you know, you could use BECH32 for smoke signals although maybe a base2 system is easier.
I don't know I've never done smoke signaling

Aaron van Wirdum: 00:31:37

No, I usually copy paste.

Sjors Provoost: 00:31:39

Okay that's cool it's also like a smoke signal just a bit more complicated. All right.

Aaron van Wirdum: 00:31:43

Was that everything there is to know about addresses Sjors?

Sjors Provoost: 00:31:47

Well I'm sure there's more but I think this is a nice primer.

Aaron van Wirdum: 00:31:50

You're going to call it a day?

Sjors Provoost: 00:31:52

We are.
So thank you for listening to the Van Wirdum Sjorsnado.

Aaron van Wirdum: 00:31:55

There you go.