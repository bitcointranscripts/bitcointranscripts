---
title: Hardware Wallets in Bitcoin Core
transcript_by: Michael Folkson
tags:
  - hardware-wallet
  - PSBT
  - wallet
  - bip32
  - hwi
speakers:
  - Andrew Chow
date: 2020-02-05
media: https://www.youtube.com/watch?v=8mdfygEzQjE
---
Slides: https://www.dropbox.com/s/k02o32d0pagac4r/Andrew%20Chow%20slides.pdf

BIP174 (PSBT): https://github.com/bitcoin/bips/blob/master/bip-0174.mediawiki

PSBT Howto for Bitcoin Core: https://github.com/bitcoin/bitcoin/blob/master/doc/psbt.md

## Introduction

Hey everyone. As you may have guessed I’m Andrew Chow. I’m Engineer at Blockstream and I also work on Bitcoin Core a lot, mostly in the wallet. I am going to be talking about hardware wallets and a bit history with them in Core and also how to integrate them in Core and how we are integrating them into Core.

## What is needed for hardware wallets

So the first thing is what do we need in order to support hardware wallets in really any software? There’s the hardware wallet side, you need to be able to communicate with it, you have to have the USB stuff and then on top of the USB you have to have other application level messages. You have the USB layer, that’s the transport and then on top everyone has their own special stuff for sending data to the device. That’s just the hardware side, there’s also the software side. The wallet needs to be able to support a few things like BIP32 public derivation. The way the hardware wallets work now is you get an xpub from the device and then the software wallet will watch that xpub and get all the transactions and stuff. It also needs to know that there is a hardware wallet and it should talk to the hardware wallet. Everyone seems to forget that is a thing you have to do.

## Wire Protocols

Let’s start with the device side of things with wire protocols. As I mentioned everyone has the USB communication layer and the application layer on top of it. Everyone at some point used this thing called HID which is Human Interface Device except Trezor and Keepkey now use a thing called WebUSB. So some of their firmware uses HID but some use WebUSB. They are two completely different things. You have to remember to support both of them if you want to support new Trezors. The other thing is the application level, this is the messages we’re sending to the device. Trezor, Keepkey and all their clones use some protobuf thing that Trezor defined ages ago. Basically you take all the messages you want, you pack them into a specific protobuf format that they define and you send over to the device. If you wanted to support the Ledger, the Ledger does something completely different. They use something called Application Protocol Data Unit which is not very specific and is completely unhelpful to know that name. These APDUs are actually from Java smartcards if anyone is familiar with that. These are completely different from protobuf, they have their own special magic numbers, their own special magic serialization.

Q - Protobufs, do you mean Google protobufs?

A - Yes. Protobuf is Google’s protocol buffers, you can go look that up.

Ledger does something different. Then BitBox, they do something different. They actually just send JSON strings. You use ASCII to make a JSON string and you send it to the device. Except that is just the BitBox01. BitBox02, I don’t have the specification here and I’m not terribly familiar with it. The last time I looked they also use protobuf but it is a different protobuf from Trezor so you can’t even share code there. All you can share is that protobuf library. The last one I’m familiar with is the Coldcard. Coldcard has defined their own binary protocol that uses some mix of ASCII and sending binary data. They also use PSBT which is ok, that is great. But everything else is some weird self defined thing. At the end of the day this all means that when you are implementing hardware wallets with Core if you want to support every different wallet you have to have special code for every single wallet. Each wallet does the same thing but in a slightly different way and they are all incompatible with each other except Trezor ones.

## Do we want vendor specific stuff in Bitcoin Core itself?

This brings up a question that we got in Bitcoin Core which was do we want to have this vendor specific stuff in Core? Do we want to have device specific in Core? The answer to that is no. We definitely do not. First of all who is going to maintain it, who is going to write it and who is going to review it? If I implemented it that would be me but what if I stopped contributing to Core? Who is going to maintain it then? Also who is going to review it? If I wrote the code I at least have to have maybe two or three other people to review it so they also need to understand everything which is unlikely to happen. Then for changes they also need to review it and it just a huge pain in the ass. It adds a lot of complexity. An obvious answer would be to use vendor provided libraries but there aren’t any in C++ so I guess that is out of the question now. At least in Core because Core is C++. There is lots of complexity with every individual device and also each one introduces more dependencies. Just having HID and WebUSB would mean having to have [libusb](https://github.com/libusb/libusb) which does the USB driver stuff that at least someone else did the low level thing. But libusb is itself fairly large and because this would be part of the default Core installation you would run into an issue where if libusb has a vulnerability that is exploitable then anyone who is using Core can be exploited even if they are not using a hardware wallet. The hardware wallet users is still not that large. It would be a lot of users that would be affected even if they were just running Core and using the Core wallet.

## Solution

So what is our solution to this? The solution is that first of all we need to define some way to send data to the device. Mostly transaction data because the transactions were the most annoying part, everyone had done something different for every transaction. We need some common transaction format that we can send each device. Then we need to have something external to Core that Core can talk to in order to send data to the device. This external thing would contain the libusb and all the device specific drivers and whatever. At least it can be a different language. We could use a language that vendors have provided their libraries for and also it would just be active only when Core needs to use a hardware wallet. It is not always running. The last thing is we need to make some common API so that Core can just do one thing and only know that one thing and not have to figure out everything for every device. Figuring out everything for every device can be a separate driver. If you are familiar with my work you probably see where this is going. The common transaction format is PSBT. PSBT was designed with hardware wallets in mind even though they don’t fit on hardware wallets in memory. That was not a design consideration. Everything that PSBT does was created with hardware wallets in mind. That separate driver is HWI, the hardware wallet interface. That does all the device specific things and does converting from the common API that it defines into the device specific drivers. If you are going to ask me who is going to maintain the device specific drivers and the HWI the answer is not me it is actually the vendors because I am using their libraries. HWI is written in Python and every vendor has provided a Python library. I would not have done that if I had to write it all myself.

Q - After the fact you realized that PSBTs don’t fit in hardware device’s memory? Are there any thoughts that are rumbling around in the background to make them smaller?

A - At this point, no. I think most of the benefit from making them smaller would be to just tell everyone to stop using legacy transactions.

Q - Non-SegWit is the problem?

A - Yes non-SegWit inputs can be very large. If everyone used SegWit that is almost not a problem anymore.

Q - So is the expectation that future hardware wallets will just have more memory?

A - Yes. Future hardware wallets hopefully, not that PSBT is public and people know about it, people will consider that and include more memory. The Coldcard takes PSBTs directly. I guess part of their design process was that they knew about PSBT and figured out how much memory they would need in order to store a PSBT.

## Bitcoin Core Wallet

Let’s talk about the software in the Bitcoin Core wallet itself. It is actually not well suited to hardware wallets. First let’s talk about how the wallet itself is structured. A wallet has a few major components. We have key management and Bitcoin Core does this as a bag of keys. It just has a bunch of keys and everything is based on those keys. We take a key, turn it into an address, turn it into a scriptPubKey, sign things with it. Everything is based on keys. The Bitcoin Core wallet also has signing. It is actually related to key management and maybe should have been one bullet point. The wallet also does transaction tracking. It looks for the scriptPubKeys from the keys that it has and tries to see if any transactions are related to those scriptPubKeys. It also has a bunch of metadata like address labels. The part we are concerned about is key management and signing.

## Timeline for BIP 32 in Core

For a bit of history, we needed to get BIP 32 into Core before we could start doing hardware wallets. Do you know how long it took BIP 32 to get into Core? Forever. BIP 32 was published in 2012. The reference implementation which was just key derivation was actually merged into Bitcoin Core but it wasn’t used anywhere, not in the wallet not in the node. It was literally just part of the test binary and a reference for people to look at. In 2015 which is three years after BIP 32 and a tonne of wallets had already done BIP 32 by this point, we got our first attempt for BIP 32 into Core. This first attempt was actually pretty big. It did things like user defined derivation paths. You could rotate out the HD seed so you could do key rotation. It also did key derivation on the fly so it wasn’t storing any private keys, it would derive them as needed. It would just store public keys. But also it only did private key derivation. This still wouldn’t have been enough for hardware wallets. Unfortunately reviewers didn’t like it and six months later we got the second attempt. This dropped a few things from the first one. It didn’t do on the fly derivation, it was still using the key pool, derive a key and drop it in the key pool. I don’t think that one did user defined derivation paths either. It wouldn’t derive on the fly and you could not change the derivation path. It still did the key rotation stuff but this one also didn’t make it. The third attempt was in May 2016, six months later. This was the absolute bare minimum for BIP 32 which means it is also enormously unuseful for hardware wallets and enormously unuseful for literally anything else but getting a backup. All it did was replace the GenerateNewKey function from generating a key randomly to derive it from this HD seed. That’s all I did, absolute minimum, nothing else was changed in the wallet. That was finally got merged and that is what we still use today. There have been a few changes since then. We can now do key rotation. That was merged I think a year ago or something. You can change the HD seed. You still can’t change the keypaths and you can’t do public derivation. There was an attempt to get that public derivation which was in 2017 and actually based on this public derivation PR someone did a full Trezor implementation and someone else did a full Ledger implementation using the whole drop vendor specific code into Core. Those were never PR’ed because I think they knew it would get nowhere. They existed and people did use them or at least the author did. That watching external xpubs thing got killed after a year unfortunately. So what we are left with is a Core wallet that still has that bare minimum BIP 32 derivation, still can’t do a public derivation and still can’t let you use your own derivation paths which kind of sucks if you want to do hardware wallets. We need those features in order to have hardware wallets. Also the hardware wallet project kind of started in 2018, at least that is when everyone else jumped onboard. I have been working on this since 2017 but that was mostly just PSBT. In order to make hardware wallets work we have finally decided that instead of jamming it into the Core wallet and trying to hack things together we are just going to fix the wallet and make it possible for us to do new things in the future. This is huge refactor of the wallet basically and it has taken the better part of a year to finally get merged. It is at least a step closer to hardware wallets.

## CWallet <-> ScriptPubKeyManager

So the particular thing that we did was make this thing part of ScriptPubKeyManager. Basically what we did was take all the key management stuff, like the bag of keys thing, and really the key to ScriptPubKey part and shove it in its own box so it can be in a separate place from the wallet. It is just a layer of encapsulation and abstraction. Basically the wallet will ask the ScriptPubKeyManager for scriptPubKeys which means addresses in this case and use those scriptPubKeys to give to the user or watch for transactions. But how those scriptPubKeys came to be, how they were generated, that is all abstracted away into the ScriptPubKeyManager. The wallet doesn’t care about it. When the wallet needs to sign something, sign a transaction, it passes the transaction to the ScriptPubKeyManager and it does whatever special magic it needs to sign it. Or at least it should but I didn’t implement that way. I will probably fix that. I realized a couple of days ago that I had not done that so I need to fix it. The thing about this model is that we can make different ScriptPubKeyManagers that do different things internally. Obviously we have the thing that we do now, the bag of keys, which we throw into a thing that we call the Legacy ScriptPubKeyManager because it is legacy code and it is a legacy that we don’t want to have anymore.

Q - So it is still a bag of keys model even though you’ve switched to BIP 32 for deriving addresses as of May 2016?

A - It was 0.13.

Q - So from 0.13 it was already generating keys BIP 32?

A - Yes. It was still a bag of keys model. All it did was instead of calling the random number generator it called derive a key from a seed. Everything else about how keys were managed was exactly the same.

Q - What about restoring from seed?

A - You can’t.

Q - So what’s the point?

A - Exactly. The point was that if you backed up your wallet like that you didn’t have to do it every 100 keys. So you could back it up once…

Q - I had forgotten how terrible that used to be.

A - You could back it up once and then not have to make periodic backups and you would still have all your keys and not lose everything. Greg Maxwell still says you should backup periodically so you get all your transaction metadata because that is still fairly important especially if you want to preserve privacy.

Q - Why couple the scriptPubKey management and private key management?

A - Because the private keys and the scriptPubKeys are inherently related.

Q - The private key material is much more sensitive than the scriptPubKey.

A - This also lets us do different ways to produce scriptPubKeys. The way that it currently works or it worked two weeks ago was that we take a key and we turn it into something. The idea we are trying to move towards is “Here is a Script. What do we need to sign for it?” instead of “What can that sign for?” We are reversing that idea, that is why we have scriptPubKey management with the private keys. What this means is that we can hide away where the private keys are. One other thing that we are working towards with the ScriptPubKeyManager is to use descriptors. We are making a descriptor wallet and the way that we are doing that is we have this descriptor ScriptPubKeyManager. This model lets us have descriptors be the thing that produces our scriptPubKeys but nothing else needs to know that. Nothing else cares that that’s how it works, it just needs to work. In that model the private keys are less important. You need them for signing but that can just be the signing part of things but not the scriptPubKey management thing.

Q - Is a descriptor like a function from pubkeys to a scriptPubKey or something like that?

A - Are you going to Advancing Bitcoin tomorrow? I’ll be talking about it then. I have a whole talk on descriptor wallets tomorrow at Advancing. The descriptor is a function that takes arguments and spits out a Script, not necessarily public keys.

The last thing is that if you want to read about this we have a document on the [Bitcoin Core developer wiki](https://github.com/bitcoin-core/bitcoin-devwiki/wiki/Wallet-Class-Structure-Changes) that not many people know exist. You can go look at that. It is really in the weeds. There will be a lot of things that don’t make sense, probably.

Q - I didn’t even know the dev wiki existed.

A - No one checks it and I checked it a few months ago and someone had vandalized it.

Q - Is that like bitcoin.org?

A - This is basically where we stage release notes. When we are doing a release we have release notes in the master repo but when we start a release process we put them on the developer wiki so developers can go edit them and add things that need to be added.

Q - How did someone vandalize it?

A - Because this document was there that was an actual document. I don’t know why. I just reverted it.

Q - Someone needs merge rights to do that?

A - Not on wikis. At least not the way that GitHub has done this wiki for some reason. It would be nice if they limited it to just organization members.

## HardwareScriptPubKeyManager

This ScriptPubKeyManager thing is how we are doing hardware wallets because we are just going to make a HardwareScriptPubKeyManager. We’ve taken all the key management stuff like signing and abstracted it away so the HardwareScriptPubKeyManager can ask via HWI a hardware wallet for pubkeys, or in this case it will actually be descriptors. HWI will take the pubkeys and produce the descriptor for Core. The descriptor is what we are using to generate our scriptPubKeys. Then when we sign, the transaction goes to the HardwareScriptPubKeyManager which hands it off to HWI for signing. This is actually how we are going to do hardware wallets in Core. It is so much easier than hacking it into whatever exists right now.

## Current Status

For the current status of all this stuff we’ve got an [issue \#14145](https://github.com/bitcoin/bitcoin/issues/14145) that tracks everything or should track everything. I don’t know if it has been updated recently. It has a bit of the motivation and some other relevant details that people might care about for hardware wallet support. This refactor ([PR \#17261](https://github.com/bitcoin/bitcoin/pull/17261)) was merged finally last week after I had written the slides. We actually do now have this ScriptPubKeyManager model and so we are finally moving forward with descriptor wallets. Our descriptor wallet is in the works. There is a [PR \#16528](https://github.com/bitcoin/bitcoin/pull/16528) for it. It is experimental, you can try it out. You might lose your money, not my fault. But descriptor wallets is a step towards our hardware wallet stuff because we use the descriptors for scriptPubKey production. We are just going to subclass the descriptor ScriptPubKeyManager and then replace the signing part with HWI basically. There is actually a [PR \#16546](https://github.com/bitcoin/bitcoin/pull/16546) that lets you use hardware wallets in Core. Sjors (Provoost) has written one. I actually don’t know how he’s implemented it but I think the design will probably change just because his thing was screwing around mostly. That implements everything if you want to try it. As for HWI itself, HWI is feature complete and completely usable. It can talk to the five devices I mentioned, Trezor, Keepkey, Ledger Nano S and X, Coldcard and BitBox 01. You can use HWI as a standalone thing and actually Wasabi and BTCPay Server are both using HWI which is kind of crazy but they found many bugs which is also kind of crazy. Thanks to them for testing my software. Hardware wallets, you can use them with HWI and Core manually. There is a command line thing. If you are not scared of the Terminal you can do it but it is also very scary for everyone else. This is what I’m going to be demoing, there have been a lot of changes to Core and to HWI recently for upcoming changes to HWI that will let you do everything from the GUI. For all the new users and the more advanced users who don’t like the Terminal there will be a GUI that you can use for everything.

Q - How does it work the integration between HWI and Wasabi?

A - They told me that they are using it.

Q - It is based on NBitcoin, the C\## library?

A - I think so.

Q - C\## talks to the Python stuff?

A - HWI is Python but is a command line tool. In every programming language I know you can execute an external program and get its stdout results and same thing over stdin. The way that HWI is used in those software and will be used in Core is that we execute it as an external command, pass in whatever arguments and when it completes its thing it returns a result in JSON. That is how we get our stuff. That’s how they integrate it just using whatever C\## things that they need to do.

Q - Do they use console out?

A - I’m not sure. If you are Linux only you could use fork and exec if you really wanted to. But in Core I think we’re going to use Boost.Process probably.

Q - Why did you choose Python?

A - It is very simple. Everyone has provided a Python library. That means less work for me.

Q - It is not really practical?

A - It is not practical but everyone has a Python library which means that I don’t have to implement all the low level stuff. The vendors have done it and also they are presumably experts in their own device which means that they are unlikely to make a huge mistake like I would.

Q - Less likely

A - Less likely, they definitely have but it is not my fault.

Q - Python doesn’t seem the safest language to implement this kind of stuff.

A - There is nothing private that is being shared.

Q - Not for that but there is no compilation…

A - The Python doesn’t handle anything that needs to be kept confidential or secure.

Q - Could people not mutate descriptors so your wallet ends up sending money to someone else?

A - You can but also you should be verifying addresses on the device. It is kind of a user problem. You get an address from Core but there is a command in HWI that is displayaddress and if your device has a screen it will show the address. You should double check, you should do that with hardware wallets anyway.

Q - The BitBox01 doesn’t have a screen.

A - Yeah BitBox01 doesn’t have a screen and we haven’t figured out… Someone mentioned something about a mobile app that they could do something but we have not done anything with this. Also BitBox01 is officially not supported by Shift Crypto anymore which means that at some point it will officially be not supported by HWI once I decide to get rid of it like with Trezor One.

## Demo

Let me start testnet first.

Q - Is Trezor T supported?

A - Trezor T is supported. Trezor made a great decision with Trezor T and that is they used the same protocol for Trezor One and Trezor T which means that supporting Trezor T was only a matter of making sure everything still worked. And everything did still work. The Trezor T has this weird bug, at least last time I tried, where it can’t sign mixed SegWit and non-SegWit transactions.

Q - What do you mean by mixed?

A - A input of legacy and an input of SegWit. There was an issue and I think there is still an issue where it can’t do that. But the Trezor One can which is odd.

Q - What happens in that case?

A - It throws some bizarre error that makes no sense.

Q - Would you be able to make a new transaction and choose the inputs or keep selecting the same inputs again and again?

A - The Core selection is actually semi-deterministic so it would probably would try selecting the same inputs. If you are using purely the GUI you cannot create a legacy address in Core. It is literally impossible because that has been disabled in the GUI. If you are using the command line you can create a legacy address and it would only be a problem then.

Q - Or if you had old addresses from before?

A - You could use an older one. Initializing an already used device with Core is a bit weird. We have a rescan bug that has been near impossible to nail down. You might not be able to find your coins if you import an old device at least for now.

Q - Rescan bug? What is this?

Q - It is for HWI is it?

A - No in Core. Randomly I will import something into Core and I want to rescan from beginning and it cannot find the transactions.

Q - When did this happen?

A - 0.16 maybe at least when I first tried it. Actually I think it was 0.18.

Q - It must be rare then?

A - No it is not that rare. It might be some of the changes we made to importmulti specifically. I don’t think I replicated this on the other import commands.

Q - This is not related to that database lock slowing it down, with importmulti?

A - I don’t think so. There was just some weird thing about that. It will not work but then when I toss it into gdb to debug the thing it starts working.

Here is my testnet wallet, I am not going to sync because I’m on data and that is going to be expensive. For this one I am going to be using a Coldcard because that is the easiest thing to do. You can use any device. Core is running off my descriptor wallet branch which if you look in my repo it is named [wallet-of-the-glorious-future](https://github.com/achow101/bitcoin/tree/wallet-of-the-glorious-future). There have been some GUI changes to Core recently that when you have a watch only wallet it will produce a PSBT. You can send and when you click send it actually says “create unsigned” and it will make a PSBT. To actually do something with the PSBT you have to still go through the RPC console. [Glen (Willen)](https://github.com/gwillen) is working on a GUI for PSBT workflow. Then HWI, this is the experimental HWI GUI. I am not a GUI designer and I don’t work on Qt that much so it is not great but it works. This one is the Qt branch but there is also a bug fix in here from one of the other branches that has not been merged yet because I haven’t had the time to do it. Let me enter my pin of 12345. I have a tonne of hardware wallets and they are all test devices including this one. If anyone wants the private keys to this, I can’t tell you the seed because I don’t know it anymore. In HWI, in this GUI it picks up the Coldcard and I can select it and wait a few minutes while it tries to figure out everything. While that is going let’s make a new watch only wallet in Core. There is a nice GUI for this. Because it is watch only we will need to select the disable private keys option. This is how Core knows a wallet is watch only, by the fact that it has no private keys. Don’t confuse this for the fact that you can import an address as watch only into a normal wallet. I consider this to be bad design. We are deprecating it but you can still do it but please don’t. It will be unsupported very soon. Make a blank wallet, that doesn’t actually matter because disable private keys implies blank. Then I added a new checkbox in this PR so that you can make a descriptor wallet. Now HWI Qt, there are two commands to get descriptor stuff from HWI and that is `getkeypool` and `getdescriptors`. In the GUI what I’ve done is automatically do it in the main screen so you have the info right there. `getdescriptors` is just useful if you want to look at some descriptors but `getkeypool` is formatted specifically to work with `importmulti` and the `importdescriptors` command that we are introducing so all you have to do is copy and paste the thing if you are working on the command line. You don’t have to fiddle around with JSON. I can just copy this and then open up the debug console. We don’t have a GUI for importing either but I will probably add that soon. The command for this is `importdescriptors`, paste the thing copied from HWI and now I can fetch a bunch of addresses from Core. I get a new receiving address. What did I do wrong? This is a P2SH. When I set this up I used bech32 and not nested but the default is always nested. I can make new addresses. That’s a bug, the fact that shows nothing. That will be fixed eventually. If you choose to do P2SH addresses like I just did now you can see here is the address, you can get a bunch of them. If you look at the keypool size it stays 1000 even though I get a bunch of addresses. At least it should, there’s an off by one, it stays consistent. If you did this with `importmulti` only imports things into the keypool once. If you don’t import enough keys or you use all your keys you have to go back to your hardware wallet and fetch more. With descriptors, it is generally from the descriptors as it goes. The other cool thing with descriptors… the one I just imported was SH - WPKH. If I really wanted to I could make that a multisig and get multisig addresses. So this is bech32 now. Let me import descriptors. Now I can get a bech32 address. So I sent a transaction to this from that thing there. So hopefully it rescans. I screwed up somewhere.

`src/qt/bitcoin-qt -testnet -nowallet -noconnect`

Testnet is going to take a while. The main thing with this is that you can almost do it all from the GUI and hopefully in 0.20 you will be able to. There is an open PR for the PSBT side of things, in particular that is the `finalizepsbt` command and then `sendrawtransaction`.

Q - Is there a fire hazard over there?

A - It does that every time I start Core for some reason.

The other thing we haven’t done is the imported stuff, that will need its own GUI. I’ll make a wallet again. At least the import is fast. `importmulti` used to take 30 or so seconds. With even larger wallets `importmulti` used to timeout, the RPC. The RPC will wait 60 seconds and then timeout. `importmulti` used to do that. Descriptors is very quick.

Q - Scammers have been active.

A - That warning is because there was a time on Bitcointalk where people would tell people to `dumpprivkey` and they would post their privkey.

The block height I was using was that one. `rescanblockchain` and there’s a transaction I made last week. This thing, I can sign the transaction now. From the normal send dialog, it says `Create Unsigned` because this is a watch only wallet. I can send my Bitcoin back to where it came from. Amount, 10. If you notice there is a bug down here, it says zero down here it should say 10. So normally this has `Send` but now it says `Copy PSBT to clipboard`. It copies it and now I can go to HWI, click the `Sign PSBT` button, drop in the dialog, click Sign, wait a few minutes for it to do it. Validation, ok to send. Why not? It is just testnet coins. It signs it and spits out a PSBT. Then the last thing is to finalize the PSBT. I get this nice hex thing and I can do send. And it sends and it works. It is almost entirely in the GUI.

Q - It is in the GUI.

A - The only three commands that I needed to do are going to get their own actual GUIs soon.

Q - What is that step going to look like when you do it properly? You create the raw PSBT so you display to the user something like a visualization of a transaction that they’ve created. In Electrum they’ve got it quite nicely, they highlight….

A - I’m not sure what it is going to be. Glen has done it but I have not reviewed and I may not get round to it. I think that will have the finalize thing and the sending part too so it will actually be entirely in the GUI. For the importing stuff, there is a plan to do it in both HWI and in Core. Greg Sanders wants the HWI GUI to call the Core RPCs and do the create wallet and do the import for you which may be useful, maybe not. I don’t know. I am also planning on adding the import dialog to Core itself. So then it will actually all be in the GUI. That’s it. Any questions?

## Q&A

Q - The import address is actually quite practical. You said you would deprecate importing read only addresses. I find it practical.

A - Are you importing it into a wallet that already has private keys? You find that practical? The thing is we want to get rid of the mixed, you have private keys but you also have a bunch of things you’re watching, a bunch of watch only things. That causes a huge problem in Core. We are trying to get rid of that. You can still import stuff but you have to make a specific watch only wallet for your imports.

Q - I am wondering if PSBT could also be used to do things like coinjoin on the fly when you are paying a merchant and that merchant creates a transaction with one of his own inputs and gives it to you and you add your inputs to it.

A - Ask Waxwing. He partially came up with that idea.

Q - Payjoin is the common name for it.

A - PSBT can be used for that. You have your SNICKER thing right?

Q - We have payjoin in Joinmarket but it is just a completely Joinmarket to Joinmarket wallet thing and it is on the command line as well, it is not even in the GUI. It is very basic. I think you’re right I think that would be a natural application.

Q - I think that is like the future of privacy.

A - You could if you wanted to.

Q - PRs welcome is what you are saying?

A - Yes. PRs are welcome. So payjoin itself is on my list of things to do but it is also after descriptor wallets which is probably going to take another year. Not just descriptor wallets, hardware wallets in general will take a year or so.

Q - I’m curious about the process you went through for the BIP itself. You said you got feedback from the hardware wallet providers after the fact. Why weren’t they involved from the beginning since it was targeting them?

A - With PSBT I think I mailed the bitcoin-dev mailing list in the fall of 2017 and no one responded to it. I think I got literally zero responses. Maybe one from Pieter who had helped me write the thing. Not the greatest response.

Q - Sometimes you need to go to people directly. With the Taproot stuff there has been a lot of stuff going on trying to get this working group together. I know PSBT is not as big but still.

A - I probably could have contacted all the hardware wallet developers but at the time I was very new to hardware wallets. I got the feedback from Jonas Schnelli a few months afterwards. It was like a random comment on IRC that PSBT doesn’t fit on memory. Oops

Q - It feels like a shame. I like PSBT but I feel it is a shame that it doesn’t really solve the problem that people are still going to keep doing new stuff because there is no standard.

A - I think it can fit in most devices. I’ve been told that the vendors have been investigating PSBT in their stuff. Trezor has been doing some work on that. There is also a problem where they didn’t want to do it. I don’t know, some weird stuff like that. Then Coldcard came along and actually used PSBT in their device. For now we need to have this translation between PSBT and all the vendor provided things. Even if they did take PSBT they’d probably still all use their own application level type of message. There’s translation there anyway.

Q - There is varying motivation for whether they support multisig right? Ledger isn’t particularly interested in supporting multisig and Trezor maybe are.

A - It depends on how you define support actually. With Ledger you can do a multisig with HWI. There’s a question of some security things like is the change address correct? There is also is this multisig the multisig you are expecting to use. There’s questions like that. So technically Ledger does support it but maybe not in the way that you would want to define support. So this is also possibly a bad idea in HWI. We technically also support multisig in Trezor, at least Trezor One and sometimes Trezor T. Also we technically support coinjoin even though they don’t support coinjoin or multisig in this manner. The way that we do it is really dumb. We tell the device that it is signing for something, it is creating a signature for an input that it thinks is its and we just discard it if it is not actually theirs. So we tell the Trezor that this input that does not belong to the device, we tell it that it does belong to it even though it doesn’t actually and then we throw away the signature at the end. This is how we sign for coinjoins and stuff, probably not the safest thing to do. It is also how we sign for multisig because Trezor has some requirements on multisigs. For the keys that aren’t the Trezor’s we tell it it is the Trezor’s and then we throw away the signature. We can do this because of SegWit.

Q - It gives you a bogus signature?

A - It makes a signature, it gives you a signature. It will not give me any signatures if it doesn’t know certain parameters and we don’t always know those parameters. Usually we don’t. I just need it to give me a signature for the thing that I don’t care about and then it will give me a signature for the thing I do care about and I can throw away everything else. That’s how we do multisig with Trezor.

Q - I thought it would just moan and go “I don’t own that.”

A - It can’t check. It is too dumb to check.

Q - This doesn’t sound dangerous at all. I doubt there are any security issues (sarcasm)

A - I had implemented that and I was like “Wait we should probably fix it and not do that”. But then Greg Sanders was like “I think it is fine”. I was like “I guess I’ll hide it behind some expert mode switch” which I then didn’t introduce for a few months. The problem with multisig and Trezor T is that because we use SegWit to create the bogus signature if the entire transaction is not SegWit it runs into that mixed SegWit and non-SegWit error which is one of the most infuriating things I’ve run into.

Q - Functionality or security wise is there a clear statement of what your… can do or cannot do? Is there an explicit statement about any guarantee or conditional guarantee. Your interface would depend on some other things and also for the Python interface, Python itself is a huge liability including packages and modules. As long as it complies with a reduced set of language features then your interface can function?

A - I don’t have anything that documents that right now. I spent quite a bit of time going through all the dependencies that we rely on. One of the things that was an issue was that the Trezor lib by itself imports a whole bunch of other stuff for \*\*\*\*coins.

Q - How many dependencies?

A - Trezor lib had like 10 dependencies by itself or something. I think almost all of them I removed. Trezor supports a lot of \*\*\*\*coins. Originally we had depended on the Trezor library directly, it was an explicit dependency. Then what I did was I went to their source code, copied everything, copied it to HWI and then deleted everything we didn’t need. That was all the \*\*\*\*coins, all the dependencies that we don’t care about like requests, for those who don’t know is an HTTP library. Deleted a bunch of dependencies, deleted a bunch of code, deleted a bunch of things that were not necessary for HWI to function. I did this for every device. HWI only has explicit dependencies on maybe like 6 libraries and that includes the dependencies of the dependency. Trezor depends on a library called mnemonic. mnemonic is one of our six dependencies. It doesn’t actually rely on that many things. The other thing that we do for HWI is I use a tool called PyInstaller to produce a completely standalone binary for HWI that contains Python itself and any dependencies that are required so it is self contained. As for weird device things like that Trezor bug, every device has a document that says what it supports and all the weird caveats about using it.

Q - To link to Chris’ presentation then have you thought at all hardware wallets in Lightning?

A - Absolutely not.

Q - And then with Schnorr how much work is it going to be?

A - PSBT is going to get a bunch of new fields for Schnorr. We are not reusing the signature field for Schnorr. I think we’ll still reuse the BIP 32 pubkeys thing because that’s universal.

Q - Does this mean that PSBTs will get bigger?

A - Probably not. It depends on if you had like a Tapscript…. It probably won’t get that much bigger.

Q - Do you need to put the Merkle proof on the…?

A - That is still under discussion on whether that is going to be needed.

