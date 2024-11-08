---
title: Coldcard Mk3 - Security in Depth
transcript_by: Michael Folkson
tags:
  - security
  - hardware-wallet
date: 2019-09-14
speakers:
  - Rodolfo Novak
media: https://youtu.be/2IpZWSWUIVE?t=23739
---
## Intro

My name is Rodolfo, I have been around Bitcoin for a little while. We make hardware. Today I wanted to get a little bit into how do you make a hardware wallet secure in a little bit more layman’s terms. Go through the process of getting that done.

## What were the options

When I closed my last company and decided to find a place to store my coins I couldn’t really find a wallet that satisfied two things that I needed. Which was physical security and open source. There are two wallets on the market. One is physical secure but it is closed source. The other one is not physically secure but it is open source. I just couldn’t take that so I created a new one. Coldcard Mk3 achieves that.

## MCU + SE

One thing that is interesting is there is rhetoric about how you can’t really do open source hardware wallets with a secure element. That’s not true. You can create open source firmwares using secure elements. Secure elements are a very specialized chip that makes things secure. We did that. There is also by the way no such thing as a open source secure element or open source chip in general. There are some hobby projects but all hardware is essentially closed source. Just the software you run on it is open source. As long as you don’t use the cryptography that is maybe closed source in the chip you are ok. You use your own, that’s open source and people can verify it.

## Security in Depth

We play with this theme that security in depth is essentially how do you increase the cost of an attack to be completely asymmetrical to the attacker. You want it to be very expensive and take a lot of money so that your attacker feels that way.

## Peeling the layers

What we do is create a lot of layers. Each layer makes it cost more. The first layer for us is a wallet is fully airgapped if you want it to be. With Coldcard you don’t actually have to ever connect to a computer if you don’t want it to be connected to a computer. That decreases your attack vector significantly because most attacks require you to somehow interact with the device to try to get the stuff out of the device. We have ways of going around that.

## Starting from the basics: Local supply chain

The first thing you do is you control your supply chain. We make our devices in Canada. The factory is about 30 minutes from my house. The micros are made in Singapore, from a major supplier of microchips that do it for all the cars you drive, it would be the same chips. But we test them in our own facility.

## Packing Simplicity: No USB Cable! Tamper Evident Bag + Serial Number on SE

Then we go to the next stage. How can I ship from my factory to you and prevent some tampering in the middle? We’ve sourced out a company that makes bags for banks to deposit money inside. They will show if it is voided if you try to open it and tamper with it in customs or something. Then what we do is we get the serial number from the bag to prevent the factory from messing with you. We program that inside the secure element of the wallet. Even if you did manage to make the bags exactly the same you still need to know the serial number of the bag and you can’t tamper with that inside the secure element.

## Clear case: Device Inspection

The next stage is “Ok great I’ve got my wallet. I check the bag, I check the serial number of the bag.” We provide high resolution pictures of the device on our website and the case is clear so you can actually look inside and see that there is no funny stuff in there. A lot of attacks would require them to modify the hardware to try to take your coins from you. Let’s say everything looks exactly as it is supposed to, great.

How do we secure the chips? The secure element is right here. It is this little guy. It is connected directly to the LEDs for a reason I will explain later. We put epoxy on top of that. Even if you want to try to break apart the wallet, take the secure element out, try to read it somehow, you are probably going to break it trying to get it out of there. You’ve already had to break the case for that. We also put a little bit of epoxy on the contacts the matter from the other microchip that it talks to.

## Peeling the layers

Then we have this system where we want to be able to attest the hardware without ever having to talk to the actual software. Our secure element is connected directly to the red LED and there is epoxy over that connection. It is not impossible that somebody gets there but that’s just one more feature that you have to get through. It starts costing a lot of money for you to get over everything. But if your device is genuine, there you go, you get a green light after you log in and you are good to go.

## Split PIN with anti phishing 2 words ie Evil Maid: Device Swap/Parts Swap

Now let’s say you have a problem where you left the device unattended in your house or in a hotel. You could have an evil maid and the evil maid could try to swap your device. This is actually an attack that does happen, not so much for hardware wallets yet, not at least known, but it is a common one. Essentially an attacker would replace your device with a dummy device because you are not going to inspect everything again. He’ll be in the other room for example with your actual device. But his is actually transmitting you typing the PIN to him. So he can go in and take the money out. What we do is we split the PIN into two. There are essentially two PINs, The first PIN, it is going to unlock these two words. These two words are unique to you and the device. Then once you look at the device after putting your first part of the PIN you see these two words. If the two words are wrong that means that device is not your device. They can’t really change that inside the secure element. It is about 4 million combinations. If the words are ok then you type the second part of the PIN. Even if they got the first part of the PIN because it did transmit to the other room, now you have the second part of the PIN protecting your wealth there.

## Air-gap seed generation + dice rolling option

A huge problem with hardware wallets or any sort of cryptography in general, you need to have a sound seed or private key. To generate that, wallets would use the random number generator inside their secure element. If they are good they will have true RNGs. The issue is that you are still trusting the silicon on the chips. You can’t trust that because if somebody has a backdoor on the chip you get screwed out of your coins again. What we do is we use dice. You can throw dice and it can provably tell you that you are inputting your own entropy. We walk you through on the device screen. You just throw a few dice and you are going to get a sound private key, it is pretty mathematically provable. You do that completely airgapped. Coldcard can work with just a battery. You can plug it into your computer and have a very nice traditional way of using a hardware wallet, say for your warm funds. But for your deep stuff, your deep cold storage, this device so far has not touched a computer. You can go inside your Faraday cage, you can have Michael Flaxman standing guard outside of it, you can wear your tinfoil hat. You can do this whole process knowing that nobody is intercepting anything.

## Multi-Sig Setup also Air-Gap

Then you can go the next level. You can do multisig. What we do is you can actually create the multisig quorum, the M-of-N of your multisig wallet without ever touching a computer again. You go to your first one and you say “I want to create a multisig”. It is going to ask you how many of how many. Then you put on the second one, the third one, the microSD card going through and then it goes back to the first one, you are all set. You just load that file into say Electrum and you have a multisig setup without ever touching a computer. It is very important.

## Your seed is encrypted in secure element with one-time pad

Let’s say the device was intercepted by some agency with a lot of resources and they decided they want your coins. They will definitely get physical access to it. Physical security is very important so what do we do? We actually encrypt your private key inside of the secure element with one-time pad. One-time pad is essentially the only provable, unbreakable cryptography that you can do to make that secret. Even if somebody sends your device to some facility, they can peel the chip that is servicing the secure element. Now we are already costing hundreds of thousands of dollars to make this attack happen. They manage to peel the chip, they use your electro microscope to look at the gates inside of your chip and do somehow manage to get out the data. They can’t break it, it would be really hard.

## SE enforces max 13 PIN attempts, user defined “Brick Me” PIN

So you left your device in your house and it is not that agency that wants your coins, it is your bad employee or something. They will try to outsource some of that, they will try to break in the PIN or something like that without going through the whole effort of peeling it. On this new version we use monotonic counters. These are one way counters inside the chip that cannot be reversed. This is a secure element that is designed to that. If you type the PIN wrong 13 times it is poof. The thing becomes a brick. It is as good as garbage. Hopefully you had a backup of your seed and you can make your new device somewhere else. We don’t believe in factory resets. A factory reset could be used as a backdoor. We don’t want to open ourselves to anything, we’d rather just trash a 100 dollar device. There is no point in trying to salvage that.

Then backup, backup is super important. You are going to have your seed in one of these metal devices or paper. But a very important thing to do is to have a few backups that are actually easier and safer to restore. We do that with the micro SD cards, industrial grade SD cards, SLC cards. We essentially encrypt the backup and some extra information for you of the wallet, inside of the device you already trust with your private key which is your hardware wallet. We give you 12 words that secures that. You can really keep this whole thing without ever touching a computer. That’s the way we do this.

## Signing transactions (PSBT)

Eventually you have to spend Bitcoins and you are not touching a computer in this perfect scenario. So what you do is you can choose the USB. We have some protections for that, the protocol is encrypted, but that is not the best way of doing it. The best way of doing it is you have your Electrum or your HWI in Core or eventually your Casa node and you create your transaction there. You save that to a micro SD card. That micro SD card, you can take it to your bank safe deposit box where you keep that Coldcard. You go there, you plug in just a battery, you sign it, you save to this micro SD card. You can just go and broadcast the transaction somewhere else. Or you just plug it in, sign it and send it. But being able to do SneakerNet and never touching a computer is a big deal. That’s how most of the attacks will be attempted. Another thing we do a lot is we do very careful analysis on change outputs. A lot of attacks on any Bitcoin thing, they are going to try to get the money that you’re returning. In Bitcoin when you send a coin out there is no way of breaking that down. Essentially you give the system the address that you want to receive the change of that transaction. The other 10 out of the 100 dollars you sent because you wanted to pay 80. We noticed that a lot of wallets don’t check change outputs, they don’t make sure that that output is part of your private key. You could lose funds that way and they just YOLO.

This is a massive summary, I just wanted to add it in there. We plan on adding Shamir’s Secret and doing a bunch of other things. I figured I’d just do a Q&A and answer some questions about hardware wallets and security if anybody is interested.

## Q&A

Q - …..

A - It is going to depend. That library, it is very memory intensive. I’m not sure there is enough room in the memory of the previous versions. With this new version we added more memory, more security so we can do more things. That is why it is a little bit more expensive too.

Q - You talked about a monotonic counter to enforce 13 tries for the PIN. Do they reset when you get it right?

A - It is not like a dying device so every time you get it wrong. We actually chose 13 on purpose because in a lot of countries it is a bad number. Every time you get your PIN right it resets the counter.

Q - Since we can use it for long term cold storage what is your strategy for firmware upgrades in the long term? Not only for Mk3 but also for previous devices that someone may have.

A - We try to support backwards as much as we can. Some features just can’t because they need the new hardware. What I would suggest is simple. If it is not a security upgrade from us and you don’t need the feature don’t upgrade. Don’t go into your secure area to upgrade your device if you don’t need to do. It is why my iPhone has a lot of apps that have never been upgraded. If I don’t need it and it is still working I’m not upgrading. But if it is a security upgrade and it makes sense for you to do it we document fairly well our upgrades.

Q - Have you signed a ND to get the secure element?

A - Yes we did sign a NDA for the 508a. Then the manufacturer opened the specs for everybody which is great. We are working now with the 608 which we are working on them getting it open. But it doesn’t really matter because one, the specs are leaked everywhere anyways. Two, the firmware is fully open so you can actually buy all the parts we use, you can build your own device and load our firmware. You can prove to yourself that the device is safe. We don’t use any of the closed source features of the chip, none of the crypto accelerators for anything related to Bitcoin.

Q - You said that the seed is encrypted and stored on the secure element and encrypted with the one-time pad. Where do you store the one-time pad? It is MCU?

A - It is a mix of the PIN in the secure element and the MCU.

Q - Will your implementation of Shamir’s Secret be compatible with Trezor?

A - I don’t know, I’m hopeful. We haven’t reviewed it so I can’t promise that we are going to use that. Everybody has their opinions. You always need just one more standard to be the standard for all the standards. We are going to try to because we want to be compatible with everything.

Q - Can you elaborate a bit more, you mentioned if you enter your PIN a few times wrong and then you enter it correctly it resets. But earlier you said it cannot reset? Can that reset be simulated in some way to infinitely try a lot of PINs?

A - That is what a secure element provides you. If a wallet doesn’t have a secure element it can’t do this, it is hopeless. That is why we created this. You need a monotonic counter. It is sort of like a counter function that it can reverse. But then you could have something pretend to be that. The secure element provides you with the type of memory you need that can’t be changed, period. It just can’t. We can prevent that from being an attempt. Then once it does reset it resets the monotonic counter.

Q - What’s the secret of your awesomeness? Specifically Twitter awesomeness, if you can elaborate on that.

A - Toxicity.

Q - In a couple of slides you have some features to make it easier to use this as a warmer solution. How much pressure are you getting from the market, from the leaders of your company who are trying to tell you what to build to make these things a little more accessible or easier to use?

A - We don’t really care. We built this for me. Everybody has a different journey in Bitcoin but everybody gets there eventually. There is only so much abstraction you can do without trusting somebody else. Every layer of abstraction you are trusting something else. It is very important for people to get there. We try to make it easy and we can probably make it easier as well. That is why we also support USBs so you can be warm with a more traditional way of using it. But there are things we will never do. We will never have a web wallet for this to be connected to via USB because that is insanity. We will never make you verify your device with our servers so you can use that device because you are essentially doxing yourself. Even if we are nice we don’t know who is listening. Essentially the philosophy of this device is that nobody knows you have it, it doesn’t touch anything and we don’t know you have it. It really goes down the privacy way of handling things. For that you get for free the airgap way of doing things. Just think about Stuxnet. The effort that those guys went through to get the malware inside the facility. It is all about creating that and standing by that. If you want a much easier wallet to use that provides you with some of the features that we would not do I’ll send you to my competitors’ website and you can buy from them.

Q - Can we enumerate once again all the things that are done on the secure element? It is storage of the mnemonic seed, it is managing the monotonic counter and the private key for attestation is there. Is there anything more that the secure element is doing?

A - We use a TRNG for some of the communication between the MCU and the secure element. You need that randomness, that is reasonable for the two to talk together because there is a one time token on the MCU. We use the randomness, we use its features to do the communication safely between the two, we don’t use any closed source crypto accelerators to do any Bitcoin thing. All Bitcoin operations are done with an open source crypto library that we share with other hardware wallets. There are a lot of eyes on that. I don’t know if that is the source of that question. No obscure crypto being used. Vendor libraries for embedded is really a cluster of crap. You don’t use it. You have your own things and then for all the cryptography that is related to Bitcoin you have libraries that are open and maintained by more than one person so there is a lot of eyes there.

Q - Is it possible to get the master public key?

A - Yes, it is HD. You can just export the xpub, zpub, support a bunch of different derivation paths, it is all your choice.

Q - If I generate my own randomness can I talk about how I input it and what it outputs?

A - It is quite fun. Matt Odell is here somewhere, he made a nice [video](https://www.youtube.com/watch?v=sM2uhyROpAQ) about this. Essentially on the key generation menu it is going to ask you if you want to do dice. You go to Amazon and you buy your casino dice. Then you choose what kind of level of paranoia you want to go. You can add a little bit, you can do halfway or you can go all the 99 that you need. Then you just throw the dice and you press which result you got. Throw the dice, press which result you got. Until you have filled up the entropy you need. That’s all provable, there is [documentation](https://coldcardwallet.com/docs/verifying-dice-roll-math) on that.

Q - I love the product, Mk3, I already ordered one. What do you feel about Mk4 maybe having a QR code reader?

A - QR codes are complicated for a couple of reasons. One is that you can’t just have a standard QR module reader. That is too expensive for me to make a hardware wallet I can sell to you. It is going to get too expensive. Two, there is added complexity to the wallet that I don’t want to include because there is more bugs on that stuff. Three, the screens are too small so you can’t really do transactions over QR codes. It is going to take hundreds of QR codes for you to get all the data out. In my personal opinion I don’t think there is added security there over the micro SD card. It is very unlikely. I like it for payments. If I am making a wallet that I am aiming towards payments then yes it is fantastic to get an address in. But for transactions I don’t think there is a massive gain there.

Q - My main problem with the card is the import tax from Canada.

A - We enable people to resell our stuff but we are never going to vouch for a reseller because that is a major security risk. In all honesty for the few bucks you are going to pay in taxes at least you know you are getting it directly from us. I think saving a few bucks for stuff that is going to store your wealth, it is not the correct time preference.

Q - Have you brought any?

A - No. Mk3 starts shipping late October, early November.

