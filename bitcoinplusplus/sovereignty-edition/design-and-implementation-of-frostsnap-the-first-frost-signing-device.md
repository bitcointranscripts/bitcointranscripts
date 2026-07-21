---
title: 'Design and Implementation of FrostSnap, the First FROST Signing Device'
speakers:
  - Lloyd Fournier
date: '2026-01-13'
tags:
  - threshold-signature
  - multisignature
  - schnorr-signatures
  - taproot
  - hardware-wallet
  - cryptography
  - security
  - btcplusplus
categories:
  - conference
source_file: https://www.youtube.com/watch?v=WBF-N35Y9Do
media: https://www.youtube.com/watch?v=WBF-N35Y9Do
summary: Lloyd Fournier presents FrostSnap, the first FROST hardware signing device, at bitcoin++ Sovereignty Edition in Taipei, covering the FROST threshold signature scheme's core advantages over legacy multisig — single on-chain key and signature for privacy, no descriptor backups needed, and polynomial-based Shamir secret sharing — alongside the specific UX and cryptographic tricks the FrostSnap team used to manage the protocol's complexity including daisy-chained device key generation, a VRF-derived four-byte security check replacing full hash comparison, coordinator-contributed randomness for both key generation and signing nonces to defeat malicious-device attacks (including the Dark Skippy exfiltration attack), NorFlash-based deterministic nonce state management to prevent reuse even across power loss, and a backup system using BIP39 words with an embedded share index and polynomial fingerprint so any threshold of devices or paper backups can be automatically grouped and recovered without manual descriptor verification.
transcript_by: 0tuedon via tstbtc v1.0.0 --needs-review
---

Speaker 0: 00:00:00

I think digital signatures are really cool.
It couldn't get colder than frost, though.
So very excited to have one of the cryptographers who was early to understanding frost, I think, do one of the first implementations in Rust, perhaps.
He's been working on how to bring this very cool digital signature technology to consumers at Frostnap, and so very excited to have him here today talking about some of the challenges of translating cryptography into the user space.
So Give it up to Lloyd Fournier.
Thank you.

Speaker 1: 00:00:42

Thank you, Lisa.
I'm really excited to talk about Frostnap, the design implementation of Frostnap, give a technical talk.
I think this is the first technical talk I have given on Frostnap, and I'm really excited to do it.
I asked myself what do you guys want to know about, actually?
What does the audience want to see?
They probably don't want to hear stories, they might, some people might, but I think it would be better if I gave you an autistic stream of consciousness of technical details.
That's what I came up with.
It's a very technical talk I've got here today.
I'm glad you guys didn't have breakfast because I don't think some of you would be able to handle it too well.
I think it's fine to call myself a cryptographer as long as it's only semi-serious.
Most of the time I actually spend resizing buttons and stuff nowadays, and making things build on Mac.
That's probably where I spend most of my time, but I do know I'm a little bit dangerous with cryptography, and that's really what the talk will be about.
It's like the tricks we used, we added over the existing cryptography to make it a good UX, basically.
UX hacks down to the mathematical level.
I'm going to quickly tell you what FROST is if you don't already know.
So it's some kind of acronym there.
It's a T of N threshold signature scheme.
It's a mathematical replacement for multi-sig.
I guess you guys are aware You can condition the spending of Bitcoin on signatures under multiple public keys rather than a single public key, so multiple people need to sign, or multiple devices need to sign.
Frost is an optimised version of Bitcoin multi-sig.
You have, Instead of having multiple keys on chain, you have a single key on chain, but each device or each party holds a different secret share of that key, and any T of the parties, so two, two out of three set up would be able to produce a signature, and that signature is actually indistinguishable from a normal single-sig signature, so it's just a normal signature that goes on chain and a single key, so no-one can even tell that you're using multi-sig.
We create BIP 340 signatures, that's taproot signatures, on chain.
That looks like it's a normal signature but it's actually a multi-sig.
This is how it's evolved, sort of from the research part of it.
There was Frost by Kolmo and Goldberg, and there was also Moosig 2 at around the same time.
They both came up with the same kind of trick.
This was for N of N schemes, and this was for T of N.
Moosig 2 was a useful contribution because it had a better security proof, but the frost the Coborn-Globerg also came up with a fixed their original security proof, I would say, in this paper, proving Schnorr assuming Schnorr, and then eventually Chui et al, which also includes some of the Blockstream research people, produced this practical Schnorr threshold signatures paper which is what really our implementation is sort of based on, or at least there is then a specification called the chill DKG specification made by Blockstream Research based on that paper with a few extra tricks added, and then finally we have Frostnap which is based on that and is adding our own tricks.
So I've got to briefly, here's where the math starts, we're going to briefly explain Shemitah secret sharing because not everyone is going to be familiar with it but it's really cool.
Instead of having multiple public keys on chain, you would instead take a single secret key and you split it up mathematically, so you split it up in a mathematical space.
For example, this would be a three out of five, you need three signatures from five keys, you would take this A0 which is your secret key and you would split it up across this parabola here, and every point on the parabola, you can think of it as a secret share.
What you do is you take your polynomial, or your parabola, and you evaluate it at different points, and each point you evaluate it is a different secret share, and any three of the points on the parabola lets you redraw the parabola and figure out what A0 is, which is your secret.
A0 is the thing with all your bitcoins on it, right?
So What are the benefits of splitting up the key in this way?
So we have, first of all, and probably the most consequential thing for you as an end user in a personal Bitcoin security situation is you don't have to have this descriptor back up.
One very dangerous thing about traditional multi-sig, or legacy multi-sig, as we like to call it, is that you have, if you have a multi-sig, let's say it's a three out of five, you have five public keys on chain, and You have five devices, and each one probably has a seed word back-up, right?
You would think that with three of those seed word back-ups, you would be able to get the funds, but actually you can't.
If you only have three of the seed word back-ups, you will lose all your money.
That's very unfortunate.
The problem is you need to know what the other two public keys are to be able to find the funds on chain to be able to spend from it, because the public keys are not in the output, they're not in the address.
You need to know how to reveal what is inside that address, and you need everyone else's public keys to do that.
So getting three of the backups is not enough, and so we don't have that problem.
If you have FrostSnap, if you have three of the backups, and a three out of five, you have all the money.
That's all you need.
You don't need to know about anything else.
That's because you're mathematically splitting up the secret, and so that parabola, you can still produce it and still get the main secret.
On-chain efficiency, of course, we've got a single signature, single public key, same cost as a single SIG transaction, so less fees, and the privacy is better because you're not revealing what multi-SIG you're doing.
You can also do more funky things we haven't implemented.
You can have multiple access structures, two out of three, and a three out of five accessing the same funds.
You can even add, for example, you can have a two out of three to start off with, and even add a three out of five later on with different devices without moving the funds on chain.
You can also enrol a new device, you've got a two out of three, you could add a fourth one in there, add part of the same access structure.
No need to move the funds on chain, no-one can tell you've done it, it's a pure offline operation.
This is quite important for businesses if they put out an invoice with an address, like give this much money to this address, and then, while that invoice is out there, they need to make a personnel change, they need to get rid of Steve from the company, now you've got to change the invoice.
You've got to call them up, sorry, Steve's left the company now, we're going to change the address for that invoice.
With Frost, you can remove Steve without having to change it.
So here is key, This is when we go through key generation and show what we did to make things a bit better.
Key generation in Frost is everyone is doing a local Shemir secret sharing, so they're all running that parabola sort of thing locally and splitting up a secret to everyone else.
Then we sort of just adding them together.
This coordinator guy in the middle, he's taking everyone's polynomials, or their coefficients of the polynomial, and the encrypted secret shares that are destined for each of the devices, adding them all together, and then finally giving them to the end devices.
There's also this little proof, you need this proof to make sure that device one knows that their contribution was made, was included in the final result, and so then, After adding everything together, you get the aggregated polynomial, and every device is able to decrypt their secret share and check that they've got the right one.
This is how it works in Chill DKG.
You can imagine how do you do that protocol with wallets?
There was these guys called Stacks Wallet who very bravely managed to get an HRF bounty on making a mobile Frost wallet, and they did this all with QR codes, so they did the whole protocol all with QR codes, and it is a very time-consuming task to do every single round of the protocol with QR codes, so registering devices, every device registering their public key, every device message that every device wants to send, have a QR code for that, and then everyone getting the final result have another QR code round for that.
It was a very difficult thing to do, so we didn't want to do this in FrostNAP.
So what we wanted to actually do was, well, just for a moment, just think about normal multi-sig, you've got to register all your devices and their public keys, into the main wallet, and then you've got to generate the wallet and then export the descriptors, right, back to the devices so they can check the addresses.
That's basically, it's still a little bit of work, and with Frost, it would be impossible, or, I mean, very difficult to do this, because of how much time it would take, because there are extra rounds.
We really can't do what you do in legacy multisig, so we wanted to come up with a solution, so we came up with the daisy-chaining solution.
You take the FrostSnap devices and you plug them into each other, and they all run it live.
So they all run several rounds of the protocol all together, and there is no unplugging things out and back in.
And so That's our first UX hack to try and get this thing good.
Now I'm going to go through a few more that are more cryptographic, more in-depth.
One of the really tricky things is this, what you would do in legacy multisig is you would have to check on every single device that they have all the same descriptor, right?
So they all get the same addresses, and they're all convinced they're part of the same wallet.
Same thing you could say you would have to do it with Frost, but what we wanted to do was come up with a compact way of checking that, not scrolling through very scary things, and not having to check big chunks of data, and checking every little hex byte is the same as the other byte, so we came up with a way of producing randomness during the key generation that allows us to reduce the security check down to only four bytes.
So you can just see, you look at the device, you check that is the same.
That actually allows you to guarantee that every device was part of the key generation, had its input included, and no-one is trying to hijack it.
If it wasn't for this VRF check, this verifiable random function that we used during the certification round of the protocol, you would have a big 32-byte hash that you have to check.
So that's how much we care about you.
That's how much we care about your eyes.
We put in a lot of cryptography just to make that very small check.
The other thing we did is generation.
So We are the first hardware wallet to do this.
All other hardware wallets, I think, you get a USB stick in the mail or something, and you say, generate me the thing that is going to hold my life savings on it, right?
It's an interesting behaviour, but it works because we have very good hardware wallet companies in the Bitcoin space, but we don't do that with Frostnap, actually.
We don't just let them generate keys.
So even if we ship you three malicious hardware wallets, the software on the coordinator, and of course it's all open source, it's going to add its own polynomial to the thing, right?
So these guys are all generating polynomials, splitting up shares and sharing them, but the coordinator is going to add his own one also, and that's going to be included and that means that's going to be included in the main public key, this randomness, so these devices are not going to be able to generate a key that is owned by an attacker, whereas otherwise you would easily be able to do that.
Now I will go into signing, so key generation, We nailed that, we made a really good signing.
Basically our main task is just to make it as good.
We just wanted to be the same as legacy multi-sig, you go to different devices, and you sign without having to worry about any of the technical details, right?
So the difficult thing is this nonce problem.
In Frost, you have to share these things called nonces up front into the which go into each signature.
When you're doing single-sig or legacy multi-sig, each device is doing that, but they're handling it behind the scenes, you don't have to worry about it whatsoever.
They generate the nonces at the time of signing, but because all these devices are sharing a single signature on chain, you actually have to generate these nonces together, and this is one of the most difficult things to design around.
The coordinator is aggregating them, and there's the real challenge, the security challenge is that the devices must never reuse the nonces.
When I talk to people about Frost, they're often like, no, man, you can't do that, the nonce management thing is too difficult a problem to make this thing secure.
If my thing accidentally, or if an attacker is able to get me to reuse the nonce, then all my money is gone.
At that point, it's a big risk.
And indeed, It is a little bit of a risk, but we can address it.
So just imagine this scenario.
So device is signed, it's used a nonce, it's never allowed to use that nonce again.
It's signed a thing, it sends the signature, but then it loses power.
The device doesn't know if the coordinator received the signature.
Maybe it lost power while it was transmitting the signature.
The coordinator, even if it did receive it, could lie that it has not received it.
So what we really want is that if the coordinator asks for the signature again, if it's the same message, and it's the same nonsense, just return the signature that has already been produced, so save it.
But if it's a different message and the same nonsense, reject it, and guarantee you can never use any nonces you've already used.
In the end, this is not like a deep cryptography trick, it's just shown it's not so hard to do this.
You can forget about data with the right hardware.
This is all you have to do, is you take the state at the beginning as you're at nonce N, you get asked a sign, you take these two slots of flash memory, and you write the next N plus one into the one slot and write the signature.
Now you've got the signature.
If you've lost power in this state, you return the signature, right, because you've got your state n plus 1, you return what is slot B, but first you write it to A, and now A and B have been fully moved forward to the next state and then you return the signature.
So really it's not so complicated to overcome this problem.
Once you've gone to N plus one, and both things are N plus one, N is deleted from the universe, so you can never produce that old nonce ever again.
You only ever return the signature once you get to that state.
So with NorFlash, which is what you have on embedded devices usually, erasing is a real erase.
It's definitely gone after that, there's no coming back.
So We can actually guarantee what we need to guarantee here, and you don't have to worry about nonces.
The next thing we've done is something that other hardware wallets have done, which is to do anti-XFIL, which is the signing equivalent of what we did in keygen.
We get the coordinator to get its nonces from the devices, the nonces they're going to use, but then it adds its own random nonce to it.
Then when it goes out to sign, it's got this RC from the coordinator in there, and so the devices, no matter what they try and do, they cannot contrive the nonce.
Contriving the nonce means having R1 and R3 be very special, that those two devices are working together to leak their secrets and leak the money on chain which is a very dangerous thing, a very dangerous attack, and there is this attack called darkskippy.com that shows how a device can, in pretty much a single transaction, leak a full 12-word seed phrase just by messing around with those nonces, right?
So we don't trust the devices to sign, other hardware worlds do, they're just like let's let this device produce the nonce and put the signature on chain.
We do not let them do that, and we don't let them generate keys by themselves easier, so we don't actually let the device do any trusted operation, anything that they're doing that involves randomness, where they're meant to generate randomness properly, we do not let them generate it by itself.
We provably add in our own randomness, and so we have this where the first hardware war, there's not a trusted third party slogan.
Terms and conditions apply to that, but it's roughly true, and I think it is an important fact that we don't allow devices to generate randomness by themselves, there's no reason to do it.
There are some engineering reasons.
I wonder if anyone knows, but the main reason why it would be hard for single SIG things to do this or other hardware to do this that are not frost-based, is that you can do it, and the nonce stuff is done by some other hardware wallets, but the key generation one is very tricky if you want to use BIP39 seed phrases.
BIP39 seed phrases gets in the way of it because it's a system where an individual device has to do that hashing of the entropy, and, since that hashing is not a homomorphic function, it's very difficult to let other people disrupt what that device wants to do.
It has to be trusted to do it by itself.
Since we're in Frost and we're all doing key generation and all these things are being shared already, it becomes very easy for us to take this coordinator and disrupt any attacks, because the coordinator is already having this stuff pass through it anyway.
So back-up and recovery.
So when we started this project, I didn't think all that much about this.
It turns out that making a hardware wallet and a Bitcoin security sovereignty system is like 80 per cent at least backups and recovery, and that's where I spent most of my time working on backups and recovery, and not cryptography.
So We've done a good job.
At the beginning, I thought we could get away with not having backups in recovery because you've got multiple devices, two out of three, or two out of four, and you've got redundant devices, so if one breaks, you've got extra devices, but then I realised that no-one would buy that at all because you could have four devices fail, I know people who have had a whole batch of devices fail, and so you do actually need backups, unfortunately, and so we did generate and craft a backup system That we're quite happy with in the end.
So in the end it actually just is some words.
They're BIP39 words with a number on the front.
That number is the share index, like where it was evaluated on the polynomial, right?
So it could be 1, 2, 3, whatever, and then you've got 24 words which has the secret share, so that's the evaluation of the polynomial, plus the polynomial checksum, I will explain what that is soon, and then this 25th word which is just the checksum over all the 24 words.
So this polynomial checksum is a weird one, it's not really straightforward about what that is, but do you know when you recover even legacy multi-sig, there is this check that I've already mentioned, you have to kind of check that after you've loaded all the seed words into each device that you've got the right descriptor on each device, right?
They all have agreement, because if you try to check addresses, you need to make sure that that device really is in the right multi-sig with all those other devices.
If not, it could be in a multi-sig, but it could be in a multi-sig majority controlled by an attacker.
You don't know what that laptop you're plugging into is doing, or what it's exporting to those devices unless you check it against the other devices.
We figured that this is actually a really difficult thing to explain to users, and to get them to do it, and so we actually, and in Frost Snap, it's even more difficult to see that that's what you need to do.
You need to somehow check an address on every device to make sure that the next thing you do is generate a receive address after recovering that it is actually part of the wallet, and not just something that the coordinator, your phone or your laptop, is lying to the device about.
So we put this little 8-bit checksum in here just to sort of say, just because we really didn't know how much we care about this kind of thing.
We don't want you to go around and having to do all these manual check steps.
It's a very weak attack.
This is how it works.
You restore everything from backup.
The malicious coordinator provides the wrong public key, but it says you're a secret share as part of this public key.
The device displays the attacker-controlled addresses because that's the next thing you do is try to receive funds, and then those funds are actually controlled by an attacker.
So what we do is We put this 8-bit checksum inside the seed words which says, listen, you've got a 0.5 per cent chance of pulling this kind of attack off which probably means it's non-economical.
Just a little thing we threw in there.
And so with backups, the reason we chose this approach, what our approach is, is that you're just backing up the secret chairs, is because out of all of them, it seems like the best one.
There are other things you can do.
You can have a cloud backup thing which stores the whole key generation, and that's actually what the chill DKG spec gives you as a backup system.
This is pretty much bringing back the descriptor back-ups which we didn't want to do, we didn't want to have to have some digital back-up, we just wanted the seed words to be the thing.
We could have added separate seed word access structures, so In other words, you have your main funds on your devices, and then you have different pieces of paper for backups.
They're not backups of the devices, they're different backup access structures.
I have a two out of three for my devices, but I have a three out of five for my paper backups and I give them out to different people.
We thought this might be very confusing for users, though.
There's lots of difficult questions about how you display those paper backups.
If you're inheriting money, or you're trying to recover money, and You don't have devices to put the backups on, it's just like pieces of paper.
You're left in a tricky situation.
In the end, each device has a backup of the secret that's on it.
It's as simple as that.
We used BIP39 words because people can't record BEC32 correctly.
That's the encoding of addresses, and I thought at the beginning that BEC32 would be the cool modern way to do this, but in the end, many people write fives like Ss, and it's totally indistinguishable from each other, and many other letters.
Some people write numbers that look like there's other numbers, you know?
Some people write letters that look like other letters.
It's not really possible, the words is really a good mental checksum.
And Our main goal with this thing is to be able to easily reproduce the code, so Frost has all this stuff, magic stuff going into it, but the backup and recovery system is actually relatively simple.
We are doing the Shamir secret sharing, but you can get a Shamir code in Python very easily, so you can describe to an LLM a couple of sentences and it will reproduce the code needed to take the backups and get the money off them.
So this is I think my final trick for today.
It was quite a nice trick that I came up with, and this is the problem of not knowing whether backups are related to each other.
You've got all these different backups, and you don't know if they fit together, right?
This could have been some backup you made for a different key, and now you've got it, and how do you know it's related to this key?
You could put some extra check sum stuff, some labels on the words, or in the words, or something to make sure this is what they're related, but that would mean extra words, and we don't want people to have to say, we don't say people like write down 30 words, right?
25 we can get away with maybe, but 30 is going to be pushing it.
We use the mathematical structure of the Shemir secret sharing, the polynomial that shares it, we actually embed and grind a fingerprint into the polynomial.
That means that there's a very small subset of polynomials when you take the secret shares and you interpolate them into the polynomial, there's a small subset of polynomials that actually are valid frost snap polynomials, so you will know when you get the shares together whether they were actually together.
So we are actually part of the same case.
This is what it looks like in the UX.
You get these three, you load in these three back-ups, and the system detects actually the one and three are part of the same wallet, but this one, four, with Greg's one, was not part of the same wallet.
We can automatically remove that for you, so your task when you're recovering the funds is just to get the seed word backups and load them in, or devices, and just load them in as many as you have, as many as you want, and it will automatically mathematically figure out which ones were part of the same wallet and which ones were not part of the same wallet.
In the end, with all these tricks, what do we have?
We've got a sovereign multi-sig wallet that recovers from a threshold of devices and or paper backups.
It can be restored by non-technical family members, single on-chain signature and privacy same as single SIG.
Most of the effort goes into hiding the complexity so we can at least match the UX of traditional multi-SIG, but on top of that, we get some big wins, so no descriptor back-ups, a four-byte security check, and not a trusted third party.
So we're pretty happy with that for our first product, And we've got more things coming on the way, but that is it.
And if there is time, I'll take questions, but otherwise I can get out of here.

Speaker 0: 00:30:00

Awesome.

Speaker 1: 00:30:08

Why can't we do 12 words instead of 24 words?
Yeah, it's something I've really tried to mathematically produce 12 words in between button resizings and stuff.
It can't be done.
Unfortunately, it simply cannot be done.
It encodes a secret key, right?
These scalers, these shares, Shamir's shares are 32 bytes, and that is basically what you get with 24 words, is the ability to encode 32 bytes.
I've tried to reduce it down, I've tried to come up with tricks, the tricks don't work.
Nothing I can squeeze.
There's nothing I can squeeze.
I will be very impassed if anyone can, you know, squeeze it out so you have a three out of five, and instead of having 24 words, you have 24 divided by three words, so you have totally, when you get them together, it's just 24 words in total.
That would be so amazing.
The backup and recovery stuff is something I poured over a lot of time and effort in and was not able to get that advantage.

Speaker 2: 00:31:17

So you said something about not liking descriptor backups, but what if I wanted to use Frost in a descriptor?

Speaker 1: 00:31:28

I think you can back up descriptor.
Thing is, what you want to be able to do is reproduce the whole descriptor just from the seed words, right?
So, if I can reproduce the...

Speaker 2: 00:31:44

If I wanted to do some funny mini script thing where I have multiple different Frost keys inside a mini script, because why not?

Speaker 1: 00:31:54

Yeah, I think it's fine.
You can do that.
But think about how do you reproduce each element of that descriptor, right?
The key thing we are solving is that you have a three out of five, right?
In that traditional descriptor, you would be like, I'm going to reproduce all five of those keys.
For Frost, you only reproduce three of them, any three of them.
You're shrinking what you need to reproduce, like, hopefully, like, the user's key is like some kind of multi-sig or something, and they just need to reproduce the threshold number, then all the other keys, like the static service provider key or whatever, can all be just reproduced by the software, and So they really don't need to actually have a descriptor backup.

Speaker 3: 00:32:43

On the same topic, basically what you're doing is an equivalent of like Which one is it like?
BIP42 that's like, you know kind of brute-forcing with just the Which is the the backups always just a mnemonic you can brute-force basically what the wallet will look like.
But this is actually the problem for wallets like us using descriptors, because users have been told basically they just need to keep their mnemonic, and then somehow their wallet will figure out where the coins are.
And then they don't back up descriptors.
So if someone wanted to use again a Frost let's say in early or whatever advanced wallet and they're like oh yeah but I read on the Frost website that I don't need a backup of my descriptor they will lose funds.

Speaker 1: 00:33:30

So Why would they lose funds?

Speaker 3: 00:33:33

Because if they don't have the descriptor of a wallet using Frost but not just Frost or not assuming the equivalent of a single SIG being brute-forced by having the right derivation path.
If they don't back up the specificities of their wallet, they will never find the funds again.

Speaker 1: 00:33:54

That's true, but I would try and design it so the specificities can somehow be reproduced or be grinded in.
So if it's a service provider's key, then you can figure out which service provider it is.
If it's like, what kind of keys would you use in a Liana system that you couldn't reproduce?

Speaker 3: 00:34:11

Right.
So let's say I have a business.
So between the team that is going to co-sign as would be a multi-sig today, I use a frost setup.
Then after an inactivity of three months, we have the board of directors keys in a frost setup.
Then after one year, we have a two of three frost setup of three different service provider that can be there as a disaster recovery.
Do you want to brute force every single kind of setup like this?
Should it be enforced in a template?
Because we don't want that.
We want to leave the user define exactly what they want for their needs and not have any basic templates, like two of three or three of five.

Speaker 1: 00:34:57

Yeah, I mean, I would still hope that in such board of directors situation, like the board of direct, like somehow one is going to have that backup somehow natively.
Because the board of directors have the key already.
They can already just spend it.
And so you could just, if worse comes to worse, you don't need that.
So I would still try and avoid, for individual users, try and avoid cloud backup kind of things, if you can.
If it's not in your setting, it may not be appropriate.
But I think we're talking about mostly personal Bitcoin security here.
This is like people, someone's passed away, they've been incapacitated, and now what steps do I have to do to reproduce the thing?
And now that situation is where you really want to optimize for that.
I think there are a lot of other situations where you don't need to optimize for that thing.
So yeah, I think that's...
I think personal Bitcoin security, you should be able to grind it out.
That's what I hope.
Yeah.

Speaker 3: 00:35:55

Can I ask another question?

Speaker 0: 00:36:05

Sounds like we have our first descriptor debate lined up for you later tonight.
OK.
I don't know.

Speaker 1: 00:36:12

Stage freeze stuff.

Speaker 0: 00:36:14

OK.
Hi Lloyd.

Speaker 4: 00:36:19

What are the downsides of Frostnap in your opinion compared to a traditional 2 of 3 multi-sig or 3 of 5 or something else?

Speaker 1: 00:36:26

Yes, good question.
I did have slides on this and I was like, ah, delete it.
Downside's not fun.
But glad you asked the question.
So they usually happen in the signing part.
So the signing bit is you, one thing is I didn't mention but I should, is you have to choose which signers you're going to use before, when you start signing.
So it's like, I'm going to sign with Alice and Bob, or Alice and Carol, or Bob and Carol.
So when you start creating the signature, you have to choose which ones it's going to be.
You can't be like, oh, I go to Alice's house, and I was going to sign with Bob, but now I want to change my mind, I want to do Carol, you have to start again.
That's one.
Then the other one is actually this nonces stuff, we do have a limit on the number of inputs you can sign at once, so I think right now we have about 30, because I do 30 inputs at once, but there is some limit, right?
The coordinator only has some amount of nonces.
We could bump the number up to 50, it just makes things a bit slower, 100, whatever, just makes things a bit slower, but there is some limit on it, yes.
Also you don't know who signed, that's maybe another one, you can't figure out who it was that actually made the transaction.
So if you're in an organisation, maybe the three out of five on-chain, you can see all the public keys, you can see which public key is signed, and therefore which people made this decision, whereas Frost, you cannot, it's a single public key, single signature, you can't detect who it was in the organisation that authorised that transaction, just from the on-chain data.

Speaker 5: 00:38:11

Is it possible to sign a hardware sign remotely?
Or do the signers need to be physically in the same location?

Speaker 1: 00:38:19

No, they don't need to be physically in the same location, you can definitely leave the FrostNaps in different locations and sign them one by one, leaving each one, but then can you do it on the internet basically, right?
Yeah, yes you can.
We've done proof of concepts.
I don't know, it might be something to do in the Hackathon, Nick, we don't know.

Speaker 0: 00:38:40

There's a workshop this afternoon, we'll be doing it, and that will be in the talk slash workshop stage of the building.
That starts at 1 o'clock, I think.
After lunch.

Speaker 1: 00:38:51

All right.
Cool.

Speaker 0: 00:38:52

Thank you, Lloyd.
Give a big round of applause for Lloyd and Frostad.

Speaker 1: 00:39:00

Alex.
Cool.
Thank you.
Thank you.
Thank you.
Thank you.
You you you
