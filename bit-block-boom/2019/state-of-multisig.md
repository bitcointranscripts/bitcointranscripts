---
title: State Of Multisig
transcript_by: Bryan Bishop
tags:
  - psbt
speakers:
  - Justin Moon
media: https://www.youtube.com/watch?v=xrReq7V7oJU
---
State of multisig for bitcoin hodlers: Better wallets with PSBT

<https://twitter.com/kanzure/status/1162769521993834496>

## Introduction

I am going to be talking about the state of multisig. It's a way of creating a transaction output that requires multiple keys to sign. This is a focus for people holding bitcoin. I'll talk about some of the benefits and some of the issues. I am not a security expert, though.

## Perspective

Multisig is an emphasis on saving and not spending a lot. This is about individuals, not institutions. Multisig has benefits for institutions, but that's not on topic. Also, "not your keys, not your bitcoin"--- it doesn't count if someone is doing multisig for you. Also, "don't trust, verify". We want to try to pinpoint all the places where we're trusting a third party. Some of this might be kind of paranoid, but it's a good exercise to figure out all the things we're trusting and failing to verify ourselves. Finally, whose consensus rules are you using? It needs to be difficult to change the rules.

## Value proposition for multisig

The main value proposition is no single point of failure. Losing one key is kind of a catastrophic event that one won't happen often, but when it does, multisig lets you recover from that. If you can survive a single key loss, I think you can sleep a lot better at night, as long as you can manage the increase in complexity that comes along with it.

## How multisig

You can create a spending policy that allows key loss without fund loss. You generate, store and access different keys differently. The idea is that if something goes wrong with one of the keys, that same problem won't occur to the others, because each one was generated and stored and accessed somewhat differently. Maybe the entropy you used to generate the key becomes predictable, so that breaks the key as well. Any attack can only get you once, so you need multiple low probability catastrophic events to lose your bitcoin, which is very appealing.

6-of-11 multisig stored unencrypted on paper in your desk is really just a complex single key setup. I am not saying "just do multisig", there are costs as well.

## Disadvantages of multisig

Complexity is the enemy of security. You must keep track of redeemScripts and other information. For pay-to-scripthash, you have redeem scripts. It's a piece of information besides your key that if lost you will lose your funds. There's also issues around inheritance and estate planning. Having more dials to tweak, can make inheritance a little bit easier.

There's also on-chain fees. Multisig has bigger scripts, more signatures, and therefore the transaction is bigger and the fees go up. It's not a huge cost at this point. But also, there's off-chain fees like travel, repetition, having to sign multiple times, you want to have your keys in different locations so you have to travel, and backups. These costs, though, are direct security benefits.

## 2-of-3 multisig example

Here is a very brilliant ASCII diagram:

    < ------- time -------- >
    key 1: <safe>   <safe>
    key 2: <safe>   <lost>
    key 3: <safe>   <safe>

           (now)   (1 month)

Losing a single key is not catastrophic. So we can now recover with keys 1 and 2. That's what we can do at this point, because we can weather the storm. Once you lose one of your keys, you need to transfer to a new multisig wallet with a replaced key for the key that you lost.

## Diverse key strategies

If it's on paper in your desk, then it is a complete waste of time to use multisig. But if you can have some geographic areas, like in different towns or states or you can really get crazy but probably not too crazy. Also, different jurisdictions can be helpful. Hardware, with heterogeneous hardware architectures from different vendors. Each vendor has different supply chain vulnerabilities. And software, like firmware and operating system is the base software on the hardware wallet, and then the programming language and different languages can have different bugs at different times. These are all rare things; I'm not trying to scare you. And entropy, where you got the private key or secret from.

## We do 3 things with private keys

We generate private keys. We store them. We interact with them. Pretty simple.

Key generation: there's a couple of ways to get a private key. It's just a really huge number. You want a really random number. It must be hard to guess. Randomness is important if you want something that is hard to guess. There's a few ways to do it, like hardware true random number generators like your hardware wallet uses which uses physical and environmental noise like from wifi signals. Dice rolls is a great one, unless you're using casino dice. You can roll a dice 62 times to get a private key. You can also smash the keyboard for a while and eventually you'll be able to convert that into a random number. You can in theory combine randomness, like if you take a random number and add 100, two things added together will be the same randomness as the most random one. Combining values is possible, but it's tricky.

Key storage: the question is, what to store? We have to think about these, because we want to have a couple keys and do each one differently. You could use paper, metal (steel or titanium), electronic storage like hardware wallets, encrypted files on USB drives, faraday cages or EMP bags. You can also store mnemonics and the 25th word password separately. CryptoSteel is cool because even if your building catches on fire, you still have your key. If the 25th word password is stored together with the mnemonic, there's no benefit really.

Key storage: the question is, where to store it? You can bury it in the ground, you could bolt it down in a fireproof safe, or you could store it in your human brain memory.

Key interactions: this is the big one. There's signing transactions, displaying addresses or public keys, and communicate with a hot machine connected to the internet. This process-- there are attacks where you can leak a private key in the communication process. Some considerations, when you're talking with a desktop, you want one communication channel. You don't want someone looking over your shoulder. USB is hard to control. There's stuxnet virus that Michael Flaxman likes to talk about which was delivered to Iranian nuclear reactors spread all over the world. There's also the Rubber Ducky one, that sends arbitrary keystrokes to your computer and can install anything. You can put this exploit on a thing that looks like a trezor, and sell it, and cause chaos. QR codes are easier to verify using an intermediate device to check the QR code contents.

Key manipulation devices: you have airgapped laptops and another one is a hardware wallet. The reason why you want it airgapped is-- airgap means it's not touching the internet. The internet is like a leaky valve, it's just going to-- information is just going to spill out, and that's not what you want for your private keys. You want to make it air tight and not connected to the internet. You buy a $200 laptop dedicated to this purpose, and nothing else. You remove all the networking chips....

## Glacier protocol: Airgapped laptops

One thing is Glacier protocol, which is a little outdated but proven, for setting up multisig with Bitcoin Core command line tools. It's probably quite secure, but it's very involved. It's a good read, you should read it, it will take like 20 minutes and you will see a lot of interesting techniques. It's very instructive to read and learn about. It has been reviewed by experts for like 5 years.

## Bitcoin hardware wallets

A hardware wallet is a tiny computer that only does a limited number of bitcoin-related operations. It's tiny, simple, and cheap. It's a tiny computer that handles bitcoin private keys. Some also attempt to guard against physical attacks from people who get the device, and others don't. The great thing is that these are cheap, off-the-shelf, diverse manufacturers, and there might sound like horrible exploits in the wild but few of them happen. Some of the problems, though, is that they are honey pots. Imagine how much money you can make if you're able to extract keys from all xyz hardware wallets. Right now there's better scams like shitcoins, so those people probably don't attempt this yet, but as those scams go away, this is going to be a really good scam and there's going to be a lot of people trying to do this scam. Address verification can be difficult for multisig, and there's limited desktop UIs like Electrum--- bitstein is writing one, I am writing one, I think in 6 months you're going to have a lot of nice multisig UIs that work directly with Bitcoin Core and stuff like that.

## Hardware wallet multisig with electrum

Electrum is currently the best UI to do multisig. It leaks your privacy, unless you run your own electrum server node as well. The default in electrum is to tell all of your information straight to Chainalysis. I'll just run through a few screens to give you an idea of how you can setup multisig. You create a wallet and name your wallet, and pick some options like multisig and other options. Then there's a nice slider for the threshold requirement, and they make a nice little pie chart.

Coldcard forces you to register the other keys involved in the multisig wallet. ((The other way to do this would be to encrypt the device's private key by the two public keys of the rest of the setup, forcing that key to only be unlocked by knowledge of the correct other two public keys-- or ask for a signmessage from the other hardware devices to verify that the key is actually usable.))

Different wallets have different levels of support for multisig. The Ledger device telling you "FEE: UNKNOWN" is really ridiculous. You need to see your change address, your receiving address, fees, your public keys, and so on.

## Custodial multisig

There's Coinbase, Xapo and Gemini. But these are non-starters for hodlers because not your keys, not your coins. But there's some collaborative custody things like Casa, GreenAddress, there are different levels of this sort of help with setting up with a multisig. They all have slick UIs unlike open-source tools such as Electrum. They have the key management expertise to protect some keys, and it also helps heirs figuring out how to get your coins after you die. Analysis paralysis is kind of avoided, because you just do whatever the third party says instead.

The business model can be subscriptions or small percentage for signing with the backup key, or add on services like hardware devices or loans. I am not sure what Blockstream Green's business model is. The costs are privacy loss (using current techniques), no control over consensus rules, and they generally only support Trezor and Ledger right now but hopefully that changes as we get more good hardware wallets supported.

## Commercial multisig products

Unchained Capital vaults: I am just going to run through kind of how this works. They have a 2-of-3 multisig vault product where they manage at least one of the keys. Their whole thing is protecting keys, that's supposed to be their core competency.

Casa Keymaster: it provides a slick mobile app to facilitate basic key setup and usage. It's 2-of-3 or you can pick 3-of-5. It's also seedless. They want to hold your hand, not your keys. It's a cool way of looking at it. By seedless, I mean the mnemonic gets thrown away. This was not originally how hardware wallets were intended to be used, but it's significantly simpler and they have some security experts on their team so I think they have thought it through.







