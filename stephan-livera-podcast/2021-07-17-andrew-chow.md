---
title: Output Script Descriptors for Bitcoin
transcript_by: Stephan Livera
speakers:
  - Andrew Chow
date: 2021-07-17
media: https://www.youtube.com/watch?v=kGM3DNtd_iw
---
podcast: https://stephanlivera.com/episode/292/

Stephan Livera:

Andrew welcome back to the show.

Andrew Chow:

Hey, thanks for having me.

Stephan Livera:

So, Andrew, you’ve been working on a bunch of things, one of which was the output descriptors idea. There’s been a little bit of progress on that. So maybe just tell us a little bit about what you’re working on lately.

Andrew Chow:

I’ve been working a lot on the Bitcoin core wallet, as usual. We’ve been preparing to support taproot with the next major release of the Bitcoin core software. So for the next release 22.0, we’re going to be having the ability to spend taproot outputs from the core wallet. And so this is in preparation for taproot activation in November. So I’ve been working on a bunch of stuff related to getting that, to work like output descriptors for taproot and PSBT fields for taproot.

Stephan Livera:

Awesome. And actually I think I saw on Twitter, there was some people commenting. I think it theinstagibbs Gregory Sanders and maybe one or two others who were saying, I think they had found out that there were actually some taproot outputs sitting there that someone could spend. I think someone had spent like a small amount just to play around with.

Andrew Chow:

Yeah. So I’m not sure I saw that, but I do know several months ago there was a test to see what wallets actually support sending to bech32 addresses for a SegWit V1 and above. So taproot uses SegWit version one, and it was at that time, we wanted to see if all these software were actually compliant with BIP 173, which says that if you get an address for a version number that you don’t know about, you should still make the output because as the sender, it’s not your place to worry about whether the receiver can spend it. So there was a bunch of tests done where someone made a bech32 address for SegWit V1 went to as many wallet software, custodial services, whatever, anyone who could send Bitcoin somewhere and see if they could make a SegWit V1 output, some of them did, correctly. And those are probably the outputs that we can see or today some of them did incorrectly. So there are a few burned coins and some of them just didn’t work at all.

Stephan Livera:

Well, pour one out for the sats we lost on the way hey. Let’s talk a little bit about, Bitcoin wallets and hopefully that this will be educational for listeners out there who are just thinking, oh, I just have a certain number of coins in my wallet or I’ve got — it just kind of manages it all in the background. Do you want to just outline a little bit, what’s actually going on there in the background and where is the output descriptors fitting into that?

Andrew Chow:

All right. So in a wallet that obviously you have keys, but Bitcoin doesn’t actually operate on keys themselves. We use this thing called Bitcoin script. And when you make a Bitcoin transaction, the outputs that you’re sending Bitcoin to, you put a script there. And the way to know what script to put is through an address and address is a human shorthand for saying, use this script in a transaction output. And so your wallet will generate keys from those keys, that generate scripts. And from those scripts, it makes addresses. And when you want an address, you click get an address. It gives you an address that it made from a script that was made from a key. This is usually how wallets work, where everything is based on that key. With descriptor wallets and output descriptors. We’re slightly changing that where we’re actually the base step is the script. And the script says I have these keys. So instead of going from key to script to address, we just go script to address. And then the script has some internal thing. Like we have a key.

Stephan Livera:

Gotcha. So, and there are different situations for listeners out there because, obviously not every listener is just using the Bitcoin core wallet. Probably a lot of users are using some form of hardware wallet. They might be using that with Specter or Sparrow or Electrum, and there’s maybe — I mean, it is like what you’re saying. It is still that, but it’s like a different way of kind of happening. Maybe it’d be good to just talk a little bit about the common standards, like for example, BIP39. Could you just outline a little bit about how those wallets are working from like, let’s say I’ve just created a wallet and I’ve got my 12 word seed or my 24 word seed BIP 39. How does that relate to what you were just saying?

Andrew Chow:

Yeah. So that’s all related to the keys part of the wallet. So BIP39 is a BIP that specifies how to encode a bunch of random bytes as, 12 words, 18 words, 24 words as those words that you memorize. And from those words we use another BIP, BIP32 to derive all the keys in your wallet. So you can have a single source of randomness and from there be able to derive all the keys that you’re going to use. And so if you just back up that single source of randomness as a mnemonic, then in the future, you will be able to restore your wallet by just using that single mnemonic phrase, because you can regenerate all the keys that you’ve previously used. So BIP32 is a method for doing that.

Andrew Chow:

BIP 32 has these things called derivation paths. So you can say derive the first key and then from the first key drive another key. And from that key drive another key. And that’s how you get like M 44 H zero H like those derivation paths that you might see. And then, the next level is we have BIPs like BIP 44 BIP 49, 84, and now 86, which describe those derivation paths for scripts that we want to use. So if your wallet is say, BIP 44 compliant, then if it supports BIP 39, 32 and 44, then you’ll have your 12 word mnemonic. From there we use BIP 32 to generate the keys. And we generate the key specifically that BIP44 says to generate. And then from there, those keys that we generate, we turn into a specific type of address, which is the pay to public key hash address. And those are the addresses that begin with a 1.

Stephan Livera:

So just for our listeners who might be struggling to follow along, think of it like this, your wallet’s managing all of this in the background, but we’re just trying to talk out the dynamic or talk out what’s going on there. So let’s say you spin up a wallet, you initialize a wallet that could be a hardware wallet, or it could be a phone wallet, something like a blue wallet or one of these other ones. It will give you that 12 or 24 words that words represent your secret. And then from that secret using these standards, we were just talking about, so that’s a BIP 32, BIP 39, that particular seed type, and then using these particular derivation paths. And these are specified in the other BIPs that you were mentioning. So 44, 49 and 84, and they will correspond to the different address types.

Stephan Livera:

So like the address types that start with a 1 addresses and start with a 3 and nowadays the default, which is bc1, which most wallets are using that. And so we can think of it like that initial seed that you’ve got. That’s really the really key thing you have to be careful of careful with, and then everything else will get generated out of that. But I think to the point of output descriptors and all this stuff is that we’re moving into a world where perhaps things are getting more complex than the simple setup that we had in the past. So could you outline a little bit around that complexity and why there’s a need now for this more generalized approach, as opposed to the very specific sort of BIP 44 49 and 84?

Andrew Chow:

Yeah. So as Bitcoin grows, we’re learning that there’s a lot of other useful things that you can do with it, especially with Bitcoin script. So if you want to do, cool things with scripts like contracts or even lightning or other things that aren’t just a key that signs, it’s hard to represent those in a wallet and output descriptors are kind of moving towards that, but descriptors also actually solve a different problem. So everyone who listened to my explanation, might’ve gotten confused by all the different BIP numbers. And if you wanted to take your wallet to somewhere else and make sure that you could still see all of your addresses, you would have to figure out, the software that you use originally, what BIPs does it support go to a different wallet and see, does it support the same BIPs and will it by default use those certain BIPs?

Andrew Chow:

So as an example I believe if you try to import something into Electrum, it will ask you, do you want SegWit, or do you want legacy? Like, so that’s P2WPKH or P2PKH. And if your previous wallet supported both, so you could have a wallet that had both non SegWit and SegWit addresses in Electrum, you only get to choose to use one of those kinds of addresses. And this gets really confusing to users. It can be frustrating when you’re restoring a backup, if just between software versions or if you want to try out a different software that has different features and descriptors actually solves this problem for us. It’ll still be multiple BIPs, but it won’t be like, three things chained together.

Andrew Chow:

It won’t be, you have BIP 39 and 32 and then 44 or whatever. It’ll be just like BIP, I don’t know what number Luke is going to give it, but some BIP number, maybe a different one saying like we support this kind of this specific function and descriptors the way that we’re able to compress all of these different things into one is that the descriptor contains the seed rather that you derive everything from, and then the derivation path explicitly. So instead of saying, I’m using BIP 39 with BIP 44 it’s just, here’s a key plus it’s derivation path. I don’t need to care about that the derivation path is BIP 44. It could be whatever I want. Any wallet that supports a descriptor, will know how to derive those keys because the derivation path is attached to your backup.

Andrew Chow:

And then the last part is the descriptor itself will say what kind of script to create. So it’ll say like make a P2PKH script or make a P2WPH script or whatever, instead of trying to infer that based on, we’re using BIP 44, or we’re using BIP 84, it just says it right there on the descriptor. So your single backup string contains everything that the new wallet needs to know to recreate your wallet. And that’s really what that’s like one of the major things that descriptors solves and was one of the original motivations for creating them.

Stephan Livera:

Gotcha. Yeah. So again, so just to paraphrase that it’s like saying it’s like giving your wallet, the map to know where to find all the coins, if you will and knowing what type of scripts to look at, whether that’s, as you’re saying, P2PKH, so pay to public key hash, or witness public key hash, or the script hash types, and the different ones. So basically it’s sort of pointing your wallet, where to look and on what pathways to go down, if you will, in terms of generating a new address, when you want to generate a new receive address and the keys associated for that. So it’s kind of all helping the wallets, manage those things together. I’m also curious, Andrew, if you could maybe give some context for us on the different seed types.

Stephan Livera:

So I know years ago BIP39, I think it was one of those ones where it’s like the, it seems to me like some of the core developers weren’t as hot on BIP 39. But it seems like that was the way the industry went because a lot of the hardware wallets use BIP39, a lot of the phone wallets use BIP39, although, obviously Bitcoin core does not use that at a protocol level. And at like the wallet in Bitcoin core, could you just outline some of the thoughts around that and some of the different seed and standards and things?

Andrew Chow:

Yeah. So really the only standard that we have as a BIP for seeds and mnemonics is BIP 39. So BIP, 39 is the de facto standard by it being the only one. Electrum has their own seed format which, so they moved, they also didn’t quite like BIP 39 and they decided to go do their own thing. So they have an incompatible seed format that is similar to BIP39. It’s still, I think it’s still 12 words, it’s words that you can memorize. But it’s really BIP39 and Electrum, and in both of these, the seed only really pertains to the keys. So BIP39 is only like from this seed, we can make keys and Electrum’s is pretty similar to that. It’s from the sea. We can make keys, although Electrum also says Electrum has a version number that is kind of a hint to the software, say use these keys to make, P2WPKH adresses or something like that. So these are the two main seed formats Bitcoin core has chosen to not implement either of them. This is partially due to some philosophical objections to BIP39 itself and partially due to the fact that it’s hard to do and no one feels like doing it.

Stephan Livera:

Yeah. And I think it’s one of those things where things don’t necessarily all have to be done at a protocol level. I think it’s fair to say that if people want things and they can potentially be done at the application level and that’s, I guess that’s all part of the market and the choices made by the individuals and the businesses out there who are building in the Bitcoin space. So, yeah. So I guess that’s a crucial difference for listeners to understand, like, if you are just using the Bitcoin core wallet, it’s not going to give you 12 or 24 words, it’s a different type of backup. You’re going to have the wallet.dat file. Whereas if you’re using the typical hardware wallets and all that, you’re going to generally have the 12 to 24 words as your backup.

Andrew Chow:

Yeah. and the a lot of this, I would say actually does come down to the fact that the way that Bitcoin core was the, at least the wallet was organized from the very beginning was not very conducive to having a seed. I mean, it was difficult just getting BIP32 into core itself. So getting more complicated things like BIP39 was a lot harder to do. and a lot of work has been put into a new architecture for using output script descriptors as the way that the wallet works. So we have descriptor wallets, which basically cut out all of the old stuff and just added a complete new implementation that uses descriptors.

Stephan Livera:

Yep. And, I’ll note as well. There is an interesting example with Muun wallet. I’m not sure how familiar you are with them, Andrew, but Muun wallet — their backup is actually using more of an output script descriptor approach. As I recall from my episode with Dario, from the team at Muun where their backup is not like the typical 12 or 24 words, it actually is like the whole descriptor style of backup where you’re writing these things down. And it combines with the different pieces to create that script descriptor approach. Whereas most other wallets are just doing the typical BIP 39 or Electrum seed, or actually, I think there’s also the aezeed, which is like the lightning labs LND style one as well.

Andrew Chow:

I forgot LND had also made their own seed format.

Stephan Livera:

Yeah. And I think the typical reason is that they wanted, I think it was a version control and also a birthday thing to say this seed was created on this date. So therefore, when the wallet is going back to rescan the chain to sort of figure out how much money you have or what transactions you’ve done, it knows at what point to start the search, as opposed to searching all the way back to January 2009 when Bitcoin’s blockchain started.

Andrew Chow:

Yeah. That’s actually one of the complaints with BIP39 and we see that there’s an Electrum seed, there’s aezeed, it’s like BIP39 is literally just randomness with a checksum. It doesn’t have a version number. It doesn’t have a birthday. It doesn’t have any other like security on it. It’s just, here is randomness. And we stick a check sum on it, just in case you type something wrong. So I believe Electrum added version number, and I think they might’ve also had a birth date and I guess aezeed has version number, birthday. And I, I seem to remember, they also have a way to encrypt the seed as well. So it’s not just, the randomness we use in your wallet, but the randomness encrypted. So if someone takes it, they don’t necessarily take your whole wallet.

Stephan Livera:

Interesting stuff. So I guess at the end of the day, it’s going to change the way people do backups longer term. But potentially for now in a typical multisignature context, you might have say three hardware wallets, or five hardware wallets, or however many you’re doing. And for each of those, that user might have a 12 word or a 24 word seed. And for each of those, they might want to do a metal backup seed product, right. To have like everything backed up in metal. But I guess that also does introduce another complexity now for the output script descriptor context, because how do you, like, do you think people would be writing that out into metal? Or do you have any thoughts around that? Or you kind of, you don’t really have a position on that?

Andrew Chow:

Well descriptors was specifically designed so that it is human readable, so it’s not binary and these characters, they exist on a keyboard, so I’m sure you could get metal stamps or whatever to stamp it into metal, if you want it to descriptors can be quite lengthy and verbose. So it might not be something you want to put into metal but if you did, it definitely contains all of the information that you need to restore the wallet completely. So you have all your derivation paths and, you know what kind of addresses to make and descriptors also have a error correcting checksum. So like bech32 if you have a typo somewhere, it will be able to find it. It’ll be able to tell you where it is. And in many cases, it’ll be able to tell you what it should be. So even if you mistype it you’re not completely out of luck. The checksum should be able to tell you where you’ve made your mistake and even tell you how to fix it. But other than that, like descriptors as a backup, isn’t quite as neat as memorizing 24 words or 12 words. and it definitely takes up more space because it’s going to be more characters than a mnemonic.

Stephan Livera:

Gotcha. Yeah. And so I guess from what I have seen so far in the space, for example, Specter desktop is another popular wallet and that wallet does have a backup file that you can do. And it’s also got a QR code. So that QR code represents the output script descriptors of that multisignature wallet or single signature, if that’s what you’re using. And so that’s one potential way things go is that maybe these would be stored on say a USB key. And that USB key would maybe be left with the metal seed backup as like a way for people to recover. Obviously there is a privacy concern with that, but it’s, again, that trade-off of how much redundancy do you want, the ability to always recover it versus the privacy. If someone stumbles across this backup and is able to then say, “ah, I see how many coins Stephan or Andrew has”. And I know, where they are and that kind of thing.

Andrew Chow:

Even with descriptors as a backup, there have been some ideas around encoding descriptors in a different way. So there’s definitely a possibility for yet another mnemonic method, but one that’s generic and can just encode any chunk of data. So there’s been some thoughts around, maybe we could have some, a bit more opaque, so you can’t just look at it and see what it is, but you could have like a mnemonic that encodes the descriptor. It’ll probably be a lot more than 24 words. But maybe something that you could memorize still and, or maybe some other kind of binary format that is easy to copy around. So there was an idea that was just kind of kicked around on the mailing list where instead of giving a person a descriptor and say back up this string, that to them would actually probably look like software code but to encode it in something like base64 and say, here’s your magic string to keep safe. And underneath it’s really just a descriptor.

Stephan Livera:

Right. Yeah. I like that idea. And I think even just the idea of if it could be reflected into a new mnemonic. So even if it was a 30 word mnemonic and people just put that on and like we have new metal seed backups that like, whatever, this new BIP39, whatever the new one is going to be, that actually has, the seed and the output descriptor, all encoded inside of it. Maybe that’s another approach that would be feasible because that’s the other thing, like when you’re thinking about when you are recovering some of these things, it might be the hardware might’ve failed or even the whole aspect. It might be years down the line. And maybe the support for USB is not as strong and it’s all USB-C or whatever is coming after that. And it’s 10 years down the line and maybe those things are always difficult. And that’s why, I guess, for some people, they feel comfortable with the typical BIP 39, 12 or 24 words. Cause it’s just English words in a metal thing. And that metal thing is not going to go up in a fire or whatever.

Andrew Chow:

Yeah. And really this is not to say that the BIP39 method is necessarily bad. I mean, it’s obviously worked for the past. I dunno like nine years, 10 years. But it doesn’t really, it doesn’t lend itself to future extensions. It doesn’t work well when we want to add new things and still have something that indicates like this is supposed to be the old method. And the reason that we have descriptors now is really that we noticed this problem with supporting both non SegWit and SegWit addresses. So this only really became a problem when we got SegWit and realize, oh, we have a key, but this key can actually be three different addresses. How do we represent this? How do we store it? How do we have users back it up? And how do we make sure that if they restore their backup, that they are getting the right one of those three possible addresses for each key.

Stephan Livera:

Right. And so someone could come back and say, oh, but why don’t you just check all three of them, but then that might not be a very scalable or sustainable approach. If let’s say that user has thousands of addresses. And now you’ve got to go and check all of these different things, or you have to check all the past addresses for this person because, they might have money that they don’t know about.

Andrew Chow:

Yeah. And that’s what core did. It would — you give it a key and it converts, it actually converted it into four different scripts. So you have your three, we have our pay to pub key hash address, pay to witness key hash address. pay to witness key hash wrapped inside of P2SH and then we have pay to pub key. There’s no address for pay to pub key, but core supports receiving on pay to pub key scripts. Yeah. Even if you can’t get addresses for it. And if you import a key into a Bitcoin core wallet a non-descriptor wallet, so we call these legacy wallets, then core will internally in memory, generate these four different scripts and scan the blockchain for all four of them. It eventually, when you have very large wallets, it starts to have a toll on memory usage and potentially even on dis space.

Stephan Livera:

Gotcha. And also, actually, this is probably another question people are thinking, is there a relation between the famed xPubs and output descriptors? Is there a relation to them is one contained inside the other, can you help disentangle that for us?

Andrew Chow:

Yeah. So descriptors have a way to represent keys and really what we’re doing right now is we’re not actually putting the seed inside of the descriptor. We’re putting an xPub or an xPriv. So from your BIP 39 seed you can generate an extended private key. And from there you can make extended public keys as xPub extended, private key is xPriv, and we take those xPubs and, or xPriv at the very root that comes out of the seed. And that’s what we put inside the descriptor. So in descriptors you’ll frequently see like you’ll frequently see the xPub, and then it’ll also be followed by a derivation path and that derivation path is how we get the rest of the keys. So that’s the relationship.

Stephan Livera:

Great. And so just to refresh for listeners, so it’s like you generate your seed and that 12 or 24 words represents that seed from that seed, you get the xPriv, as you said, the master private key. And then from that you create the xPub, the master public key, and then that xPub is then combined inside the output descriptor, which shows you how to find all the coins that you have. And that’s like a master public, or it’s kind of like a public key that allows you to see all of your coins. And then you need the private keys to spend that obviously. Is that correct?

Andrew Chow:

Yep. So in core, when we generate descriptors, we do generate a seed, it’s not a BIP 39 seed, those are different, there’s too many things that we call seeds. We generate a thing we call a seed and from there, we turn it into master private key that we put inside that descriptor so that we can then use that descriptor with private keys and be able to sign transactions. But yeah, most many descriptors that you will see coming from a wallet will contain it an xPub and that’s perfectly normal and that’s fine. Now, if you see a containing a yPub or a zPub that’s not normal and that’s a bug the software.

Stephan Livera:

Yeah. Actually, while we’re there? Do you want to just explain, what’s an xPub versus a yPub and a zPub?

Andrew Chow:

Yeah. So BIP 32 defined a way to serialize these extended keys to be used for key derivation. And the result is what we see as xPub, xPriv. When we got SegWit wallet software, other wallets, software vendors needed a way to — because previously there was allow you to export an xPub. So you could import it into some other wallet. But with SegWit, they needed some way to say here’s an xPub, but only use it to generate SegWit addresses. And so they came up with why don’t we export an xPub but instead of prefixing it with xPub, we prefix it with yPub and Z pub. And these are two, say keys, you generate with this public key are for P2WPKH wrapped inside of a P2SH. So that’s what yPub and zPub are. They’re kind of the trick of changing the version number to represent something new, but this is also not sustainable, you know, Z is, the end of the alphabet, do we go to aPub next for taproot?

Stephan Livera:

Yeah.

Andrew Chow:

So with descriptors, we can kind of sidestep this problem, avoid this problem, and just say, we will still use the xPub because BIP 32 to define xPub without giving any meaning to what script to create. And then we can just tack on in front of it, the scripts that we want to have.

Stephan Livera:

Got it. So just summarizing then again, so historically it was just xPub and that didn’t necessarily have a specific meaning, but now, or what happened then is xPub became also the way of representing a specific that the 1 addresses, right. And then what happened is a lot of the wallets made this yPub and zPub nomenclature to specify, oh, these are your three addresses. And then for the zPub that was for your bc1 address is like, that was what was done. And then as you’re pointing out, that’s not very, long-term sustainable and scalable because we’re going to run out of types. And it’s just not going to fit with the new context. Right?

Andrew Chow:

It’s also not easy, not as easy to understand, like I look at yPub and I’m like shoot. Y, which one is it? I know it’s one of the SegWit ones, but I don’t remember, is it P2SH-WPKH or just P2WPKH same with zPub, I never remember which one is which.

Stephan Livera:

Right. Yeah. Whereas it’s a generalized approach, right?

Andrew Chow:

Descriptor is generalized, and it’s pretty obvious because we reuse common terminology. So with a descriptor, if you see that it begins with WPKH that should, prompt you to remember, this is going to make a P2WPKH address, we’re you reusing the same terms and acronyms that we’ve used previously.

Stephan Livera:

Yeah. And this was historically, could have been an issue for people where let’s say an exchange didn’t support sending to bech32 addresses. They, that they only would send to a three address. And then if you’re a user and you’re sitting there with your wallet that only gives you bc1 addressesyou’re in trouble now. So then it became a bit of a game of, Bitcoin people trying to shout at exchanges to say, Hey, give us, we want bech32 to address withdrawal. We want native SegWit. It give us this SegWit withdrawal, and the exchanges might be dragging their feet on that because they would rather support some altcoin as supposed to supporting the best practice Bitcoin Stuff. Right.

Andrew Chow:

Yeah, so with adding new things to the wallet depending on how the wallet software is organized, it might be rather difficult to support new features. I think famously Bitcoin core didn’t support SegWit addresses in the wallet until 0.16 or something like that, which is about a year and a half after SegWit itself, the consensus rules was implemented into core.

Stephan Livera:

Ironic, eh?

Andrew Chow:

Yeah. So this time, with descriptor wallets, it was much easier because now we can just say we’ve defined a new descriptor and here’s the implementation for it. And we just drop it right in this spot that we reserve for adding new things to descriptors. So it was really easy to add taproot wallet support to Bitcoin core for the 22.0 release.

Stephan Livera:

Yeah. Gotcha. And so, as you were saying, it’s bringing it back to that idea that it’s going to be more future proofing because now when new features are coming out and new things are rolling out, it’s going to be all contained in this more generalized form. And that will apply even in the backups and in all of these other aspects, when you need to recover something, let’s say your wallet gets destroyed. If it’s a phone or a hardware wallet goes up in a fire, or that kind of all these kinds of things that you can recover that now a bit more easily. So yeah, let’s talk a little bit about some of those things that it might help enable. Like, I mean, an example might be lightning wallets. So as, as we mentioned earlier, that example with Muun wallet maybe multisig is going to be a bit more on a kind of certain standards.

Andrew Chow:

So descriptors right now we have descriptors for all of the major single key addresses. So there’s P2PKH, P2WPKH, SH, WPKH all of those. And then we have another descriptor, multi for multisigs. So it’s easy to represent a multisig inside of a descriptor. And so you can make multisig wallets. There’s still some questions about how to coordinate making a multisig wallet, but once you have it, you can represent it as a descriptor and everyone can take that descriptor and use it before for more complex things. We actually have an extension of descriptors that’s called mini script. So mini script is a generalized way to write complicated Bitcoin scripts. This hasn’t been implemented into core yet.

Andrew Chow:

There’s an open PR, but, and there’s ongoing work on minscript elsewhere. But miniscript will allow you to make, contracts that say, like only allow this key after this block height or time, or, start as a two or three multisig. And then after six months, turn it into a one of two multisig or whatever, whatever crazy thing that you want. Miniscript allows you to make these complicated contracts. And so one of the tests that was done with miniscript was to see if miniscript could recreate the lightning HTLC script and it can and I think it doesn’t make exactly the same script. But it’s semantically the same. It has exactly the same meaning.

Andrew Chow:

And I don’t remember if it was more efficient but it was definitely pretty close to what the lightning developers came up by hand. And one of the nice things about miniscript is if you want to make a script, you don’t have to understand script and analyze it for months and months to make sure that there’s no possible way to screw it up mini script. And the mini script developers have already worked out most of those gotchas and so you can use miniscript to make a complicated script without having to think too hard about possible corner cases.

Stephan Livera:

Yep. So mini script as a project, and I think it was, it was mostly Andrew Poelstra. And I think Sanket I think also put in some work onto it and a few people.

Andrew Chow:

Yeah. So it’s mostly being done by Andrew Poelstra, Sanket, and then Pieter Wuille. So those are the three main people who work on mini script.

Stephan Livera:

Yeah. And so in the future, when we get this, this might help people, let’s say they’ve got a big multisig and they’ve got their family life savings on it, or something like that. And they might have some more complicated, big setup of five keys or 10 keys out there. And then what you could do is sort of allow in this idea, as you were saying, that it might back off or back down. So it might start as whatever, seven of 10, but then over time, after a few years, it might back down into like five of 10 required to spend or something like that to kind of create more complicated scenarios. And obviously it will take time for the entrepreneurs and for Bitcoiners out there to figure out what are the best use cases for this and how it might be best used, and commercialized importantly. But those are some of the ideas, right? Of how it might be actually used in practice.

Andrew Chow:

One of the really cool things about miniscript is that it does its own optimization for size. So I’m fairly certain. One of the other tests that was done with miniscript was to see if it could recreate, recreate a bunch of other complicated scripts. And one of the ones that they did was Blockstreams liquid network. It has a complicated script for the Federation I believe. And what happened was when they use mini script to recreate that script, it actually came out with something that was more efficient than what the liquid developers could come up with by hand. So miniscript actually did a better job than the humans thinking on it for several months.

Stephan Livera:

Well, that’s an interesting result hey. And I wonder if it would then have any other applications, like if people were to use it in some kind of wallet that also combines with say lightning and things.

Andrew Chow:

I think, well, since lightning has fixed scripts it’s not quite as useful there. So lightning uses like fixed script templates, but if lightning needs to introduce new kinds of scripts, then it would definitely be useful. Mini script also helps with having multiple different signers involved without all of them knowing exactly what the script is. So one of the neat things about miniscript is that it can be analyzed so that and like analyze automatically. So if you have, say a hardware wallet that is signing for some arbitrary script, that is generated by miniscript then, then the hardware wallet doesn’t need to have known what that script was before. It doesn’t need to have known what that script does. It can take the script as it comes in hopefully from a PSBT and just analyze it on the spot, understand exactly what it does and then understand exactly what it needs to do in order to sign for that transaction.

Stephan Livera:

Yeah. So maybe that could also be handy in other contexts where maybe you have an always on signing box and these are distributed around and that’s like one of the keys in a multisig setup or something like that. Kind of like a CK bunker Coldcard bunker kind of idea, but implemented in a mini script compatible way. And maybe that’s another way it could be done as like a security thing to add another layer of protection in some way.

Andrew Chow:

Yeah. And with like the whole fallback thing, fall back after some number of months that signer could know that it’s going to take the fallback case because like the signer could without having seen the script beforehand, analyze a script, understand what the conditions are and then realize the fallback case is going to be taken because the lock time in the transaction is some specific lock time. and understand that and know that, okay, sign the fallback part, or like sign for the fallback part of the script rather than, the some other condition.

Stephan Livera:

Right. Yeah. And I guess this is all super early, so we’re just going to have to see what the entrepreneurs and the Bitcoiners out there come up with. Also, let’s talk a little bit about taproot. So you mentioned earlier that there is going to be an output descriptor type for taproot is there anything listeners should be thinking about from a taproot perspective with output descriptors and also, is it going to be a new address type?

Andrew Chow:

Yeah. So taproot is a new address type it uses bech32 M which is a modification of Bech32 to fix a…

Stephan Livera:

The PQ thing. Right?

Andrew Chow:

Yeah. It’s called a length extension attack. It’ss kind of a problem, I guess, enough. So that Bech32m was made. So Bech32m, is incompatible with Bech32, but it will look basically identical. The only way you can tell is if you’re really good at analyzing numbers. You have to do the math to tell the difference, basically. But with the taproot output, it’s going to have just the public key in the output. So a SegWit with P2WPKH and with non-SegWit P2PKH what we had was the hash of the public key that you wanted to use in the output. With taproot it’s still not just the public key itself.

Andrew Chow:

And this is important when you’re analyzing taproot descriptors. It’s not the public key itself, but it will still be a public key in the output. There’s some crazy math involved and we take the actual public key that we see in the descriptor and we hash it and combine it with some other stuff in order to get the public key that goes in the taproot output. So if you do see a taproot descriptor, I think the most common one you’ll see will just be TR and then an xPub. the keys derived from that xPub are not the ones that end up in the actual taproot output that you would see in the transaction. This is something that wallet software writers need to keep in mind because if you think that public key is what ends up in the taproot output, there will be compatibility issues. And we don’t like that.

Stephan Livera:

You might lose coins?

Andrew Chow:

Well, you won’t lose coins, but if you try to restore to a different wallet, you might not get the same addresses.

Stephan Livera:

Okay. And so then it’ll look to the user like, oh no, I’ve lost my coins. And then there’ll be a nightmare again.

Andrew Chow:

Then It looks scary. Like you lost your coins. And the thing that happens is it’s such a little, it’s really subtle because it’s like one line in BIP 341 that you should do this thing to generate the output key. And if you don’t read it too closely, you will miss it. So when I was writing the specification for taproot descriptors, like I put there, this must be, hashed in this way as specified as BIP 341. Just put that again, just to reinforce that it’s not just the pub key in the output.

Stephan Livera:

And MuSig2? Any thoughts there any impacts there, in terms of how let’s say people start using MuSig2, in the future for doing multisig, or potentially, maybe it’s even in a lightning context of use of MuSig2, would there be any changes or things to think about there from an output descriptor point of view or not really?

Andrew Chow:

Yeah. So there will be,uprobably descriptors or maybe something in miniscript, that allows for MuSig2. Right now we have decided that the current multi descriptor will, not be like overloaded. So we won’t have multi mean different things in different contexts. There will probably be like a MuSig descriptor that contains the keys that you, that you want to have. But MuSig2 specifically is a bit more complicated than just representing inside a descriptor, because setting up MuSig2 is interactive and kind of involved.

Stephan Livera:

Yeah. So I guess that will be a bit of a hurdle to overcome in terms of when people want to do their hardware, wallets, multisig setups, but maybe in a lightning context, it’s not as bad because you can deal with the interactivity better. Cause obviously you’re connected anyway.

Andrew Chow:

So lightning, I think it’ll be a lot easier for lightning to implement MuSig2, because they can talk to each other over the lightning protocol, but for a generic, like multisig setup thing. I mean, I don’t think we’re even there yet with normal multisig, let alone being able to do MuSig2.

Stephan Livera:

Any thoughts on multisig standards? Do you see anything that you think the ecosystem should be doing to move towards that kind of standard or you think we’ve kind of already taken the easy opportunities that are out there?

Andrew Chow:

It’s a hard problem. There has been a lot of things that have been proposed and for each one I can always think of something wrong. But at the same time, I also have a hard time with coming up with something myself that solves all those problems. It’s not something I’ve been looking into too much lately because there are many other things I’m working on. So I don’t have a lot of — hard to budget my time. Yeah, sure. One thing that I would like is for someone to write BIP 48 and at least — so this is a problem I’ve complained about multiple times on Twitter, where a lot of software will reference something called BIP48 for multisig. And yet BIP 48 itself does not exist, which is bizarre and really annoying. So I would like for someone to write down BIP48, that at least mentions all the things that everyone does that claims to be BIP48. So at least there’s one place to look at it.

Stephan Livera:

The mystery BIP. Okay. So anything to update us on PSBT wise. So partially signed Bitcoin transactions as the creator of PSBT. Do you have anything you wanted to update us on there?

Andrew Chow:

Yeah. There’s I proposed several new fields for supporting taproot. So PSBT currently has fields for BIP 32 derivation paths and signatures and scripts, but none of these really work with taproot, especially because taproot uses a different format for public keys, a taproot use a complete different signature algorithm. We decided that instead of reusing the same fields that we would instead just put new fields in for taproot specifically. So there’s a PR open to the BIPs repo and I sent out a mailing list post several weeks ago that defines these new fields, that will, that we can use for taproot. And these new fields will, they’ll also work with the two different versions of PSBT that we have. There’s no limitation on which version that they work with.

Stephan Livera:

Yeah. So just for listeners who aren’t familiar with, PSBT, it’s like a way of having multi stages in your Bitcoin transaction. And so you might’ve used it in a context where let’s say you’re using a coldcard and you’re doing a micro SD card transaction back and forth to the computer. Or it might’ve been used in other contexts, or it’s like actually being used in the background without us knowing, right. The wallet is just doing PSBT and it also might have context or applications in things like say lightning. People are talking about this idea of having a channel open from a hardware wallet, and then the channel close going back to the hardware wallet. And so the PSBT might be another way that or it is a way that is being used to coordinate some aspects of that transaction.

Andrew Chow:

Yeah. The new PSBT fields. I’m starting to implement them into core now, although they probably, they definitely won’t make it for 22.0. Hopefully after these fields are accepted into the BIPs repo, and people start implementing them, you’ll be able to, hardware wallets, hopefully we’ll be able to support taproot. And then you can use PSBT with a hardware wallet to get your taproot spends that way, too.

Stephan Livera:

Gotcha. Yeah. And so, as people have been talking about how taproot might have some slight benefits in privacy we don’t want to oversell that aspect. There is some small benefits there. And one of those is that in the taproot world, if we had lots of people using taproot, single signature spends and there was also taproot lightning happening then in the case of the collaborative channel open and collaborative channel close of a lightning transaction, that would look indistinguishable from the taproot single signature, say hardware wallet, or even phone wallet or desktop wallet spends. Right?

Andrew Chow:

Yeah. So one of the key innovations with taproot is the idea that everything can end up looking like a public key. So if you have a case where you have a complex script, but at the very top it’s everyone involved agrees, then, then that whole script is collapsed into just a single public key. And it looks indistinguishable from any single key signature for a taproot output on the Bitcoin network. So it does give you a privacy benefit there if you’re doing scripts or multisig or anything involving more than one key in the transaction.

Stephan Livera:

Yeah. But I guess let’s also be fair that it’ll take time for these benefits to come through. And so the things that you and others are working on are at a deep technical level at the protocol level. And then it takes time for that to actually show up in the applications that we use and in the hardware wallets that we use. But eventually we might reach that point. And I mean, just like when SegWit came out in 2017, it took some time for the wallets and some of the exchanges and businesses in the space to actually support it. And so in the early days, it was obviously a very low percentage of SegWit usage on the network. So potentially at the start by using taproot, you are sticking out like a sore thumb, right. But over time as more and more people use taproot then, and that’s maybe more of a medium and longer term thing where if everyone wants everyone’s in the taproot world, whether you’re a single sig, lightning or DLCs and some other fancy crazy things and multisig stuff, then you all start to look the same.

Andrew Chow:

Yeah. The other thing is that using these complex scripts is it’s not something that we even see on the network today. I mean, multisig too. we rarely see you don’t see that many multisigs around. We mostly see single key things. So for this privacy benefit to even have an effect, you need to be doing things other than single key things. And until people start doing that, there isn’t that huge of a privacy benefit.

Stephan Livera:

Yeah. Yeah. Right. And that’s only from a script or output type perspective as well. Of course there’s still chain analysis and there’s still the common input ownership heuristic, and all of those aspects that you still have to watch out for as well. But this is just one element on which people can differentiate or distinguish between different output types. And then use that to try to cleverly fingerprint you or figure out what’s going on on chain. And that’s where, the chain surveillance companies of the world might try to take away your privacy and it’s that constant back and forth. But nevertheless, it is an upgrade and it’s an improvement. And so hopefully over time it gets updated and happens. I think actually I recall seeing even Nicolas Dorier, the creator of BTCPay server was talking about this idea of, oh, should we have single single signature taproot outputs? And I think Pieter responded to him saying, yeah, why wouldn’t you do it?

Andrew Chow:

Yeah, I am of the same opinion. Why, why not have single key taproot outputs? There’s also the fact that more single key taproot outputs also increases the anonymity set for people who do use complex scripts and multisig with taproot. So taproot does have some fee benefits for at least the spenders, people spending taproot outputs. There’s also a fee reason for you to want to use taproot.

Stephan Livera:

Yeah. Well, And that’s good. I mean, arguably then everyone has an incentive because like, if you are a user of Bitcoin and you’re, cause even if you are HODLing, eventually you might be spending or if you pass it on to your children, then they’re going to be spending at some point. So there’s an incentive there. You could argue that everyone has an incentive to go to taproot, once everyone’s comfortable with it. And once the software and the hardware is all compatible with it and able to use it, all of those things. So anything else you wanted to mention around, Bitcoin development? Anything we haven’t touched on?

Andrew Chow:

No, I think that’s it.

Stephan Livera:

Cool. Okay. Well, I guess any, any tips for listeners out there, or maybe any calls for help you, do you want review, help or something out there?

Andrew Chow:

Yeah. So if you are interested in reading about like reading the specifying documents, the BIPs repo is where all of these, where all of these things have been, are being specified. So, I’ve got, I’ve got a PR open for these taproot fields for PSBT and I’m working on writing BIPs for the descriptors. It’s a bit strange that we’ve had descriptors in core for like three years now, but there’s no BIP. The specification is just a document that sits in the core repo. So I decided to finally finally write, write up several B, describing all of the descriptors. If you are technically inclined or even just want to read about how these work,uyou can go check out the BIPs rebuilt for those. If something’s not clear about how they work, please do leave a comment because we want these specs to be clear and easy to implement. Excellent. Maybe not easy to implement, but easy to understand so that they can be implemented correctly.

Stephan Livera:

Great. I’ll leave that in the show notes. So listeners go to stephanlivera.com/292. And you’ll find all the links for Andrew’s BIPs, as well as his mailing list posted there in relation to output descriptors Andrew, anywhere you would like people to find you online?

Andrew Chow:

Um, You can find me on most social media platforms with the name @achow101 that includes Twitter and GitHub, Twitch. I also do a stream every Monday where I work on Bitcoin core. And recently I have started work on my stream doing these taproom fields in PSBT. So if you want to watch, watch it happen, you can come drop on my stream, I guess. And yeah, you find me @achow101 online is probably me.

Stephan Livera:

Excellent. All right. Well, Andrew, thanks very much for coming on and helping explain these very complicated topics for us.

Andrew Chow:

Yeah, no problem.
