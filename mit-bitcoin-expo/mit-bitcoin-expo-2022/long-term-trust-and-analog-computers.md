---
title: Long-Term Trust and Analog Computers
transcript_by: kouloumos via review.btctranscripts.com
media: https://www.youtube.com/watch?v=kf48oPoiHX0
tags:
  - codex32
speakers:
  - Andrew Poelstra
date: 2022-05-07
---
What I am here to talk to you about are analog computers and long-term trust.
And what I mean by long-term trust is how can you have assurance that your Bitcoin secrets, your seed words or your seed phrase or whatever have you, how can you be assured that that is stored correctly, that the data has integrity and so on, and how can you be assured of that for a long time?
And so where trust comes into this is that traditionally, in the last 100 years, in order to verify the integrity of data, you have to put it into some sort of electronic computer.
And in doing so, you then have to trust that those computers are not doing horrible things, they're not leaking your data, they're not destroying it, they're not lying to you when they say that it's the right data, and so on and so forth.
And I propose that you can avoid these kind of trust issues, and they are ongoing trust issues, as I'll talk about, by simply using analog computers.
And analog computers are simple mechanical devices that I'll demo a little bit, that will do computations in a way where you know exactly what's happening.

## What makes a safe hardware wallet?

Before I jump into that, let me give sort of an overview of hardware wallets and the way that we normally think about hardware wallets.
A hardware wallet, of course, is like a dongle, it's like a ledger or a trezor or a coldcard or whatever that you buy.
And you store your bitcoins on it, and you connect it over USB, or maybe you ferry SD cards between your computer and the thing, and it does signatures on your behalf.
So you have this special-purpose piece of hardware that you can't load software onto, or at least not without being signed.
And so the idea is it shouldn't have malware, it should be designed to handle sensitive data and you have some control over what's going in and out of it.

So what makes a good hardware wallet?
Well if you go on like r/Bitcoin, you'll get advice like the following (slide#3).
And this is good advice, to be clear, but it's fairly basic.
They'll say get one of the popular hardware wallets that's manufactured by somebody who you trust.
When you receive it, make sure that it's sealed properly.
If it comes with a list of pre-filled seed words, then you have some sort of supply chain issue and you should throw it out, and you certainly should not use those seed words.
I'm laughing that, by the way, that is a real very common supply chain attack.
If you buy a hardware wallet from Amazon or whatever, the Amazon shipper will just stick a piece of paper in saying, please use these seed words.
It's very easy for them, but it gets people.
So don't do that.
So there's good advice for buying a hardware wallet.

But we're MIT students here, so we can maybe be a little bit more technical and look into how are these things assembled.
Some devices have secure elements, which are these sort of proprietary chips that are designed to be resilient against various means of breaking them open and extracting data and things like this versus an ordinary computer chip which is not designed to be adversarial against a physical attacker.
And then maybe you care about what kind of software is running on it.
You want it to work using PSBTs rather than some random ad hoc protocol.
Maybe you want all the latest goodies, you want it to support Taproot or multi-signatures or descriptors or whatever the latest hotness is and so on.
Maybe you want to download the source code, it should be open source.
I could go on for quite a while, but all these different things that you could think about.
And the unfortunate thing is that there's nothing on the market that checks all of the boxes that I'm describing, and so there's a good chance that if you're thinking at this level, you're not going to make a different decision than if you were just buying the most popular thing, but you will feel less secure about it.
And that's sort of a theme here, that the more you know, the less comfortable you're going to feel about how you're storing all your bitcoins.
So there's another layer down the rabbit hole we could go.
And if you hang out on the right IRC channels or spend time with a lot of Bitcoin OGs, you'll find advice like this, where, like famously, Greg Maxwell advocates using an old ThinkPad or an old laptop that you purchased before Bitcoin was a thing.
And it's not going to be backdoored in any way that would be Bitcoin-specific, because nobody knew that Bitcoin would be a thing back when it was manufactured.
There are also various people who file bugs on libsecp saying it doesn't work on 8-bit processors and so on, because they are trying to run Bitcoin software on their GameBoys or Nintendos or old calculators.
I think most people in this room probably use a TI-83.
So before the TI-83, there was a TI-85, which is an even more primitive TI graphing calculator that you used to have to use in school.
And you can run Bitcoin on this.
You can implement cryptography and TI basic and do that, and presumably your TI calculator is not backdoored in some way.
And it's also a good disguise.
If you're one of these people, you've probably got a house full of old, crappy electronics, half of which doesn't even turn on, and if something in the pile is secretly your Bitcoin wallet, well, nobody's going to target it.
So, that's something.
It's not bad advice.
If you have the means and the motivation, I certainly would advocate doing this.

But let's go a little bit deeper down the rabbit hole here.
So what I'm going to advocate here is rather than dealing with this electronic hardware that perhaps is older than Bitcoin and unlikely to be backdoored.
It's still got chips, it's still got flash memory, chances are, and it might have some wear leveling logic or something like that.
You still can't really tell what it's doing and ensure yourself that it's not storing anything or doesn't have side channels or whatever.
But if we instead use paper and metal, and I mean large chunks of metal that you can see and manipulate with your hands, then you have a pretty good physical intuition about what your side channels might be.
You have some assurance that the laws of chemistry are not backdoored in a way that will undermine your bitcoins, and if they are, forget about it, there's no hope for you or anyone.
But it's not.
That's a good authority.
It's in the Bible.
So and then the other benefit of this is that if you're doing all these computations by hand, all your intermediate computations are going to be on worksheets.
They're going to be on paper that you write out.
So what you can do is you can take your final computations, you can store them in a crypto steel or something so it's physically encoded, and all your intermediate computations you just set fire to.
You've got a whole bunch of worksheets, You just burn them, they're gone, that's the end of that.
So, I'm gonna come back to this in the second half of my talk and show some pictures and spin some wheels up here and do some kind of stuff.
But let me do a bit of a digression to try to justify this mode of thinking and this trust model to people who are not innately metalheads or steampunks.

## How can you protect yourself? (Trust and the Future)

The first thing I want to emphasize is that this is an ongoing, like a continual thing.
If you're storing bitcoins for a long time, say like years or decades even, then there's kind of a continual trust requirement in how you manage your stored secrets.
So there's a question of, well, what kind of hardware should you be using if you're going to be using hardware wallets.
So maybe you have a hardware wallet that you like now, but maybe in five years it doesn't work anymore.
So should you just buy a new one every five or 10 years and keep trusting that every time you purchase a new hardware wallet there's not going to be any problems forever.
Should you buy a dozen right now, and then just kind of cycle through them and hope that there won't be new issues found in the old hardware that you're using?
Or maybe that'll become unpopular enough that nobody's going to bother targeting?
I mean, there are arguments for both sides.
And certainly it doesn't seem safe to be using stuff that you're never updating, because then you're not going to get security updates and stuff.
But on the flip side, if you are continually updating stuff, then you have kind of a new trust requirement and a new opportunity for bugs to slip in that might cause you problems.
So you have to think about this for the hardware you're buying, you think about this for the firmware update so you put on that hardware.
You think about it in general for like, what is your process for testing your backups, if you even have one.
Maybe you've got these crypto steals, and maybe you just trust that the tiles won't move if nobody opens it.
And, I mean, that certainly makes an amount of physical sense, but it's uncomfortable.
If you have all the stuff stored in a crypto steel and it's got a tamper-proof sticker on it and you just store it for 20 years, and the last time you looked at it was 20 years ago, I don't know.
How much faith do you have that really nothing has changed out from under you.
So these are scary questions, and they're not necessarily rational things to worry about, or there's certainly different degrees of plausibility and so on, but they are an ongoing source of discomfort, and an ongoing question that you have to answer for yourself.

## How can a hardware fail? (Trust and the Present)

So let me talk a bit more about what specific things you might see go wrong with hardware wallets and the different directions that you might need to worry in.
So kind of the classic direct thing, if your hardware wallet fails, there are a few ways that it can fail that are sort of obvious, and that they're direct ways.
So one thing is if you let the hardware wallet generate your key material, and most of them will, you just say, generate me a new seed, and it'll give you some seed words.
If those seed words are bad, if they're low entropy or they're copied or they're backdoored in any way, then it's just game over.
So that's unfortunate.
As I said, it's not, I haven't heard of this happening with Bitcoin wallets in a while, this happened with an Android wallet a very long time ago, it used a bad RNG.
But with harder wallets, as I said, the most common thing is somebody just literally prints a paper with a bad seed on it and advises you to use it, which is much easier to pull off.
Another thing is it could just sign transactions.
It's plugged into your computer, somebody figures out how to bypass the screen that shows you the address and destination and stuff, and then it signs off all your coins that you don't even know about.
And ultimately, it could just directly leak your key material.
Maybe there's some really serious bugs, some buffer overflow or whatever, and you have some malware on your computer, it breaks into the hardware wallet, it gets your key material out.
Game over.
But then there's more subtle things that you might not think about unless you work on hardware wallets or you do security modeling for a living.

So one that worries me personally is this first one, which is that you have storage anywhere that key material is stored, even temporarily.
Potentially it won't be erased.
If you have a SSD in your computer, the SSD itself has wear leveling logic where after a certain cell has been ridden to or read from a certain number of times, the drive itself will say, well that cell's gone bad, so we're not going to use it anymore.
And the drive actually comes with more capacity than it advertises, so it has room to kind of expire various cells, and it'll last for quite a while, because there's a stochastic process in which of these fail.
So if you have your key material stored somewhere, and then you go to delete it by overwriting it with zeros or random data or whatever have you.
But between you storing the key material and you overwriting it with zeros, the drive decides that it's not going to use that cell anymore, then you're not going to overwrite it.
You'll overwrite some other random part of the drive.
And then much later, you throw it in the trash and somebody with an electron microscope gets a hold of it somehow, which can happen if you're a visible Bitcoin developer.
People will try stuff like this.
And now they've got your key material, and now they can steal your coins.
And there's no way that you can tell unless you get an electron microscope yourself and then load your key material into your electron microscope software, which I can assure you is not written by cryptographers, and then detect whether or not you can find it anywhere on your drive, and then I guess point the electron microscope at its own storage and try to do some sort of Douglas Hofstadter thing there.
It's expensive, it's complicated, and I'm pretty sure none of us have ever done this.
Another more subtle thing, you might sign things that shouldn't.
If you can trick the hardware wallet, you can find a bug where it will show something on the screen, but actually what it's signing is something different from that.
Then you lose coins, you don't want those kind of bugs.

And then the final thing here is a side channel issue.
And this is something where if you have an air-gapped hardware wallet, you don't have to worry about this, but if it's plugged into your computer over a USB, and you have malware on your computer, it can do stuff like request a signature, and then listen to figure out how long it takes to sign.
And it may turn out that the hardware wallet will take a different amount of time to sign a transaction depending on the pattern of zeros and ones in your secret key.
And you can detect those timing differences, and then you can infer information about the secret key that way and kind of extract stuff.
So timing is a classic side channel, so is power draw.

If you've got malware that has direct access to your USB bus and can measure this.
Or if you have an attacker who's just physically stolen your device and has connected it to an oscilloscope.
You can measure all sorts of things.
You can measure the electromagnetic waves that are emanating from the wallet as it's doing computations.
All manner of things.
The nature of doing these high frequency electronic things is that you're going to leak what you're doing, no matter how much you try to harden the hardware.

And this is one, like a sort of a general reason to distrust electronics.
It moves very quickly, it's working with secret data, it's designed to be low power and fast, and there's often a trade-off between being constant time and side-channel resilient, and fast and low power.

## Volvelles (Trust the Past)

So, let's get into the meat of this talk.
And actually, most of my slides from here on out are going to be pictures.
So I'm going to try to make this not super technical.
There's no way in 20 minutes I can show how to actually use this scheme.
So I'm just going to try to justify it, and then show some pictures, and then give you guys some links where you can go find some more.
Here is the most technical slide that I've got, where we are going to define the word Volvelle.

A volvelle is a physical computer that is formed by two pieces of paper that rotate relative to each other.
I'll show some more pictures closer up.
This is just connected by a brad.
I printed this off on my home printer.
I used an X-Acto knife to cut out a bunch of little windows, and you can see that as it turns, different values are appearing through the windows there.
This kind of computer, I think, basically dates back for as long as we have any historical artifacts.
But Wikipedia claims that these volvelles in particular came from a particular scholar who developed a whole bunch of new volvelle tech around 1000 AD.
They have actually a history of being used for cryptography.
There's a 1980 article by David Kahn, who wrote The Code Breakers, which is the classic history of crypto book, where he talks about how throughout the Middle Ages, there was a lot of usage of volvelle for crypto, for substitution ciphers, or cryptograms is what we're familiar with.
So you could take something like this disc here, where you can see I've got an inner wheel and then all the symbols there point to symbols on the outer wheel.
And I can literally just translate character by character and do kind of like a primitive version of encryption, doing stuff like that.
In fact, there was some cryptographer called Alberti sometime in the 1400s who was actually doing this, and this is one of the really historical examples of substitution ciphers being used.
But then we can do all sorts of new stuff.
I'm just going to run through all these things.
You can do error correction codes, you can do polynomial interpretation, blah blah blah, you can do a whole bunch of mathematics just using these wheels.

Here's a close-up picture (slide#14) of an old version of the volvelle that I just showed you here.
You have a pointer up at the top, you point it to some particular number, and what this is doing is an operation we call addition, although it's not quite like the addition you're familiar with.
You just combine two values by turning the pointer to one of them, looking up the other one on the front of the wheel and then seeing what the result is.
Pretty straightforward.
Here's a wooden volvelle that my fiance made me for Christmas.
So you can see this is fun for the whole family.
The wooden one, unfortunately, is actually pretty slow to use, so I use the paper ones.

Before I go on, I want to share this quote (slide#16).

> And in those days there appeared in Alexandria a female
> philosopher, a pagan named Hypatia, and she was devoted
> at all thimes to magic, atrolabes and instruments of music,
> and she beguiled many people through (her) Satanic wiles.
>
> ~ John, Bishop of Nikiu, from his Chronicles 84.87-103, writing some 300 years later

Because I think there's an interesting historical lesson here, which is not the intended one.
So this is a Coptic bishop from somewhere in Egypt in like 700 AD, that had these words to say about Hypatia, who was a scholar in Alexandria some 300 years before.
She was a pagan.
She was a neoplatonist.
There's some merit to these accusations of Platonism, but certainly she was not a witch, who was using astrolabes and musical instruments, I guess, to turn all the children evil.
But the cool thing here is that this bishop, John, all he can do is centuries later make impotent accusations of witchcraft when he has no ability to take any of her bitcoins.
Because all her use of these astrolabes has effectively secured them, even against 300 years of future technological development.
So this is what we should all aspire to.
Like somebody in this room in 300 years, I would like to be accused of a witch without losing their coins.

### The scheme (codex32)

Here's the scheme, here's a quick overview of everything that we can do with this scheme.
Again, I'm not going to say exactly how to use this, but I'll have a link at the end that you can follow.
Using these volvelle as well as some worksheets and an instruction booklet that we've written up, you're able to, first of all, generate coins, or generate random data just by rolling dice, and even if your dice are biased.
For example, a lot of cheap dice, especially ones you buy online, in manufacturing they have these pockets of air in the middle, just because they're kind of like drop-forged or however they do it.
You wind up with these air pockets that are not symmetrical, and so the dice will not show all six values with equal probability.
We have a worksheet that will let you eliminate that source of bias.
You can also compute and verify checksums, which give you assurance that your data has not changed.
We have what's called the distance nine checksum, which means that once you add these extra 13 characters of redundant data, which constitute the checksum, if there are up to eight errors anywhere in the rest of the string, you will be able to detect that that's the case, and even if there's more with overwhelming probability.
Even cooler, if there are up to four errors, it's actually even possible to correct them, to determine mathematically what those errors were and what the correct value is, no matter where they appear in the string.
So this gives you resilience against, like, if you're loading stuff onto a crypto steel and you use the wrong tile, say, or if it's subjected to heat and maybe one of them is not so easy to read, or if you're using paper and something gets wet or smudged or whatever might happen, this error correcting code will make sure that you're able to recover from that.
And then the other big benefit is that using the error correcting code and using these volvelles, every year or however often you want to check that your data is intact, you can run the checksum verification algorithm by hand, again, burning the intermediate things.
And you will know that your data is still intact and it has not changed, nothing's been swapped, and nothing's failed or become erased, or you just imagine that you originally loaded it to begin with.
So you can have an ongoing assurance that your data have integrity without involving any new trust requirements on electronic computers.
And then we have Shamir's Secret Sharing.
So you can split your secret up.
You choose a threshold value, let's say three.
You can split your secret into 10 pieces, hand them out, bury them in all 10 corners of the world, and any three of them are sufficient to reconstruct your secret.
But if you have only two of them, they have no information about the secret.
It's kind of a cool threshold that happens there.
So you can split your secrets up using this scheme, you can bring them back together using this scheme.
Again, no electronic computers here.
Then also, if you split your thing up into two pieces and you set your threshold to two, you can actually do encryption that way.
You can say, one of the shares is the encrypted data, the other share is the key.
And this is particularly useful if you're trying to move physical key data around the world.
You do this two of two splitting, you take one of the pieces on the plane with you to your next destination.
If you're searched by TSA or whatever, you just throw it out and restart.
It's no harm done.
If not, just take two trips.
You can move your data securely, and now you don't need to worry about customs or TSA or train thieves or whatever you might worry about.
Or mail inspectors, I don't know.

### Dice Generation Worksheet

I'm just gonna run through a couple of pictures here.
This is the dice generation worksheet.
You can sort of see how this works.
What we do is you basically roll a bunch of dice twice and you extract one bit.
So if the second value is greater than the first value, that's a one, if it's less than, that's a zero.
So you roll the dice once, you set some markers where the dice value are, you roll them again, you set the dice where they are, and then you follow that kind of tree on the left and you're able to generate a bunch of 5-bit values that way.

### Process Explanation

Here's a picture of the volvelles (slide#19), the three of them that you use for all the various computations.
Essentially what it is, you use the one on the right to look up what are called recovery symbols.
You use the two-sided one on the left, which is a potion (potion is the image on the volvelle).
You spin that to your recovery symbol, you flip it over, and then it will translate your shares.
And then the middle one you use to add all the shares together.
And that's how you do secret splitting.
That's how you do recovery.
It's always this translate-and-add kind of process.
Ιt's actually very mechanical.
You don't need to know any of the underlying math to follow these instructions.
It's actually kind of cathartic and kind of fun to do.
It takes a while, probably like 30 to 60 minutes to do a key recovery, but that's really not bad at all.
Ιt's not like you're spending a day doing a whole bunch of computations where a single mistake will mess you up.
You just do it, you can use the checksum, we'll protect you from mistakes and just move forward.

Here's the other side of the two-sided one there (slide#20), and here's a close-up so you can see how these work.
You can see I just took an X-Acto knife, sliced out some windows, and threw these together.

## Benefits of Paper

I am pretty much out of time, but in 20 seconds I'll just summarize exactly what I've been saying here.
The benefits of using paper here (slide#22).
You have no side channels, you have no EMF, you have none of this kind of stuff.
You can understand and verify how this stuff works, and I think there's a huge psychological benefit to that.
That you know what's happening to your secret key material as it's going through the checksumming and splitting and recovery processes like that.
You can feel it, it's very tangible.
If you want it to go away, you make it go away.
Rather than requesting some disk controller, please overwrite it for you, you just throw it into a campfire and God will take care of it.
And then the other thing is this stuff will continue to work.
It's not going to become obsolete, it's all very straightforward mathematics, believe it or not.
It's all just like polynomial interpolation.
It was developed, 200 years ago, most of it.
And it will just continue to work.
And you can even reconstruct the scheme, really.
If you knew a bit of the math, you could infer how the volvelles are constructed and just do it.
You don't even need the volvelles, you can do it with lookup tables, you can do it by hand.

The name that I'm using on this project is Pearlwort Snead, which is an anagram of Andrew Poelstra.
My co-author, Leon Olsson Curr, which is also an anagram, I encourage you to try to undo it and find out who he is.
The two of us have [this repo on GitHub](https://github.com/BlockstreamResearch/codex32), which has the Postscript file that will generate all of this stuff for you, or that is all of this stuff for you.
We're always happy to see issues and discussions and whatever feedback you might have.
At some point this year, we will do some professionally bound versions of this.
We still have some more iteration on the artwork and the instructions and stuff, but we're going to have some bound versions that you can buy online if you want.
Just one last tiny thing is to show you what these look like before they're printed out.
We just have this nice glossy paper.
They look very pretty.
You cut these out, you fold them together.
You need a brass fastener, but other than that, there's no glue or anything like that.
Nothing complicated.
Just ordinary art supplies.
So, thank you all for listening.

