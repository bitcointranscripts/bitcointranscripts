---
title: Hardware Wallets (History of Attacks)
transcript_by: Michael Folkson
tags:
  - hardware-wallet
  - security-problems
speakers:
  - Stepan Snigirev
date: 2019-05-01
media: https://www.youtube.com/watch?v=P5PI5MZ_2yo
---
Slides: <https://www.dropbox.com/s/64s3mtmt3efijxo/Stepan%20Snigirev%20on%20hardware%20wallet%20attacks.pdf>

Pieter Wuille on anti covert channel signing techniques: <https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2020-March/017667.html>

## Introduction

This talk is the second in the series after my previous [talk](https://vimeo.com/showcase/8372504/video/412057285) in London a few months ago at the Advancing Bitcoin conference. There I was talking mostly about general attacks on hardware, more from the theoretical perspective. I didn’t say anything bad hardware wallets that exist and I didn’t specify anything on the bad side. Here I feel a bit more free as it is a meetup not a conference so I can say bad things about everyone.

## Our project

The reason is that we are building a Bitcoin hardware platform and we are trying to make another hardware wallet plus a developer board and a toolbox for developers so they can do whatever hardware devices or Bitcoin powered devices. When you start doing something like that you obviously want to learn from others what mistakes they did. During this research I found a lot of interesting attacks and I found many interesting things, what hardware wallets do or do not do. That is what I want to share with you today.

## Why hardware wallets?

This I will skip because we have already discussed it.

## Cast

These are the wallets I will be talking about: Trezor, Ledger are pretty well known, Coldcard is a nice hardware wallet made in the US and allows you to use a complete air gap so you don’t need to connect it to the computer and you use a SD card to transfer transactions back and forth, and Digital Bitbox is a product of a company from Switzerland, Shift Crypto.

## Table of contents

I split all the attacks into four categories. The first one is f\*\*\* ups. There are not many in this section. These are very serious vulnerabilities and if you have them then your product failed to deliver what it promised. The first reason for hardware wallets to exist to protect against remote attacks. If your computer is compromised your keys should be safe. F\*\*\* ups cover these kinds of attacks where it doesn’t work. Then there are attacks on the software side. When you write something in software that is vulnerable then you have an attack and you can fix it with software. Hardware attacks due to certain features of hardware, some of them can be fixed by software and some not. And finally the architecture things. You have certain limitations when you choose how your hardware wallet works and what protocol you use, what data you use to verify stuff and also what microcontrollers you use.

## Change address verification

<https://sergeylappo.github.io/ledger-hack/>

First the f\*\*\* ups. The first one is the pretty recent one. It was described in December 2018, a few months ago and it was on Ledger. What happens if you are trying to sign a transaction with Ledger? You connect Ledger to your computer and your computer prepares a transaction and says to the wallet “Here are the inputs. It has 1 Bitcoin and this is the derivation path you need to use to derive the private key to sign it. And these are the outputs. The first output is what we are actually sending and the second output is our change.” You don’t need to show the change on the wallet itself. You can provide the information for the hardware wallet to verify that this amount will actually end up in the address that the wallet controls. You use the derivation path to get the private key and to figure out that you actually control this address. Then on the hardware wallet side it displays to the user that you are sending 0.1 Bitcoin to this address and 0.01 Bitcoin for a fee. You don’t need to show the change address because you can verify that it will go back to you. The problem with Ledger was they trusted the computer when the computer was saying “This is the change address”. They didn’t verify it will be controlled by the private key from the wallet. You could replace this address by any other address, just send some derivation path, the Ledger didn’t check it and just remove this output from being displayed to the user. You will send 0.1 Bitcoin to the address you wanted and you will lose all your funds. This attack was fixed. I don’t know the reason why they didn’t check that but now they do check it. I would say it is a pretty critical vulnerability.

## Hidden wallet feature

<https://saleemrashid.com/2018/11/26/breaking-into-bitbox/>

The second one is a very nice hidden wallet feature of the Digital Bitbox. We don’t like to reuse addresses. To derive new addresses and private keys we use BIP32 and master private and public keys (xprv and xpub). The master private key is a pair of 32 byte numbers, one is the chaincode, the other is the private key. Then the corresponding master public key will be the same chaincode and the public key corresponding to this private key. If our computer knows the master public key it can derive all the addresses and all the public keys underneath that. If you know the master private key you can derive corresponding private keys. Here is the flaw of this hidden wallet feature. Why do you need a hidden wallet? Imagine you were trapped and the robbers hit you with a wrench until you sent them all your Bitcoin. You tell them the password and send the Bitcoin. If you have a hidden wallet that they don’t know about then you can easily send the funds and you still have most of your funds securely stored on the hidden wallet. How did these guys implement hidden wallets? They used the same values as in the master private key but they flipped them. In the hidden wallet they used the private key of the normal wallet as a chaincode and the chaincode as a private key. What this means is if your computer knows the master public key of the normal wallet and the hidden wallet, for example you want to check your balances, then you get the chaincode from here (xpub) and the private key from here (xpub’). The whole private key for all your funds are transferred to your computer. This is kind of sad. When you try to protect yourself and use a nice feature and then it screws you up. Now they have fixed it, it was in November (2018). They fixed it by normal use of the passphrase. To derive the hidden wallet master private key you use the same mnemonic with another password. Similar to what Trezor does. Right now it is not an issue anymore but it was pretty sad to see. It was discovered by Saleem Rashid together with a few other vulnerabilities that are not that interesting.

## Software

So we had two major f\*\*\* ups. Two is already enough. Now let’s move to the software side.

Q - What went wrong there? They didn’t do the right checks? How does that happen?

A - If you don’t know how exactly master private keys work then you can make this kind of mistake. It is not about the validation. The private key should always stay private, it shouldn’t go anywhere else. What they did, they screwed up the standard implementation.

Sjors Provoost: They made two mistakes. One they ignored the standard, there was a standard for hidden wallets. And two they rolled their own crypto. “We’ll just swap these two things around”.

Normally if you try to do something you need to look at the standard that already exists. There are smart people developing cryptographic standards and they are thinking about all kinds of things that you would never think of. If you don’t have any kind of standard then you need to think more than twice, many times, before you release something like that. I think this can be solved by security audits at least.

Q - This will be an issue only if you are signing with a hidden wallet?

A - Not even signing. Normally master public keys are used not to sign but just to monitor the blockchain. If you never give your computer the master public key then it will know your private key for this wallet. It would be probably ok-ish to use one computer to monitor this master public key (xpub) and to use another one to monitor this (xpub’). But then the usability of your hardware wallet isn’t great. You have two different wallets on your phone.

Q - The hidden wallet is just one button click away. The guy with the wrench would just say “Can you also click the button for the hidden wallet?”

A - I don’t know how exactly it was implemented but probably yeah. The password scheme works much better because you have an infinite amount of hidden wallets. If you want to go really crazy. Another problem is the attacker will hit you with a wrench until you give out all of them.

Sjors Provoost: If they know which addresses you control they can keep using the wrench.

A - This is the privacy issue that you should solve with coinjoins and stuff.

Q - Just give you enough plausible deniability in case that happens.

A - In general disclosing information about your funds is pretty bad.

So the software part.

## USB descriptor

<https://blog.trezor.io/details-of-security-updates-for-trezor-one-firmware-1-8-0-and-trezor-model-t-firmware-2-1-0-408e59dc012>

I talk a lot about Trezor in the other parts not because they are bad but because they are the oldest wallet and also they are the most collaborative I would say. I learned a lot by reading their security updates and their blog and talking to them directly. More eyes are monitoring the code of Trezor so more attacks are discovered, they fix it almost instantly. In that sense I think it is a great product and I would recommend Trezor. There are some attacks that we can learn from. One that was fixed in March 2019, a few months ago, it is pretty relevant to the talk I gave a month earlier. It is a glitch during the USB communication. When you have your hardware wallet and you plug it into your computer over USB what happens under the hood? The computer asks the hardware wallet “Who are you? What is your vendor ID? What is your description?” The wallet should send back something like “I am Trezor Model T. This is my vendor ID, blah blah blah”. It was happening before you unlocked the wallet with a PIN. Normally it is fine. Even if the computer asks for more bytes than you can deliver there was a check “If the computer is asking for more than 14 bytes then give back only 14”. This is Trezor Model T. But the problem is if you are using an application microcontroller that doesn’t have any protection against glitches. If you send this request and if you time everything correctly such that when this comparison of 500 to 14 happens you either skip this interaction or make it evaluate to a wrong value then the wallet will just send you 500 bytes. It happened that after the descriptor there was a mnemonic. Asking for 500 bytes would give you “Trezor model T” and here is my mnemonic. It was fixed very quickly and easily. First for Trezor Model 1 I think they added read protected bytes. When the microcontroller is trying to read this byte it will go into fault. It will never go after that. This is the first protection for Model 1 and for Model T they made it even easier. They didn’t respond to any request until you enter the PIN. If you know the PIN then you control the wallet so it is fine. They have these `read_protected_bytes` just in case but a pretty elegant solution I would say.

## PIN side channel

<https://blog.trezor.io/details-of-security-updates-for-trezor-one-firmware-1-8-0-and-trezor-model-t-firmware-2-1-0-408e59dc012>

Another one is on the PIN side channel. I don’t know if you were at Advancing Bitcoin or not but basically there is such a thing as a side channel attack. This is a slide from the presentation. If you are trying to verify the PIN, this is the PIN we entered and this is the correct PIN. If you do it not smart enough then with the `strncmp` function the microcontroller first checks the first digits. If they are different then it returns `false`. If they are the same it keeps going. What you can do is try the first digit and measure the time between the start of the PIN verification and the failure. If the first digit is correct then the time that the microcontroller will take is a little bit longer. You know that you guessed the first number. Then you continue the same with the second, the third, the fourth. This was not an issue in Trezor, they had a slightly different issue. They were comparing the PIN digit by digit and were keeping it until the end. If you entered the wrong PIN and the right one is `1234` then it compared all 4 digits and at the end returned `false`. The timing attack was not an issue. The issue was the power consumption and electromagnetic radiation. When you are comparing `5` to `1` the pattern of the radiation and the power consumption is slightly different compared to other comparisons like `6` to `2` and so on. What Ledger did, it was disclosed by Ledger, they trained a neural network, artificial intelligence, to distinguish between different comparisons and with a random hardware wallet they were able to guess the right PIN after I think 5 tries or so. You still have a pretty small delay on this range. If you try 5 times it will be maybe a day but still doable. It was also fixed. And it was fixed in a very smart way. Trezor even released an open source library for encrypted storage. Basically your mnemonic and your private keys and all the secret information was stored encrypted and this encryption key is derived by the PIN and other entropy from different sources. For example the unique ID serial number of the device. Now they are also working on having some key from the SD card. Given all these keys you can decrypt the mnemonic but otherwise you can’t. It is very resistant against all kinds of side channel attacks because what you always do is take this PIN, you don’t know the correct one, you use that together with a fancy algorithm to derive the decryption key, then you try to decrypt your secret information and if you decrypt it correctly you will see it looks like a mnemonic so it is the correct PIN.

Q - I’m assuming the PINs on all the hardware devices are implemented the same? You can only have 3 tries…

A - In Trezor you can have as many tries as you want if you are willing to wait long enough. They use an incremental timer. Between the first try and the second try it is 1 second, after that that you have to wait for 15 seconds, then for 1 minute, for 5 minutes. After 10 tries you will need to wait for a few days and if you fail once again it will already be weeks.

Q - How does it track time?

A - They start the timer at boot. They increase the counter then even if you unplug the device and plug it back you just need to wait for this time.

Q - This is the Trezor Model T, it is also on the Trezor Model One?

A - Yes they have very similar firmware?

Q - And Ledger…

A - Ledger has a limited number of tries, they refine the PIN on the secure element. The secure element was designed to do everything correctly because it is used in banking applications and so on. For them it is not an issue. You normally don’t have such side channel attacks. On the Coldcard they use secure key storage. There is another attack on Coldcard I will talk about later but in principle it is also not vulnerable against side channels. I don’t know how the Digital Bitbox because they have pretty bad overall security.

Q - They are still a very new company in comparison.

A - Yes they are working on a new product where they will fix some of these things, hopefully. What else do we have?  All the Trezor clones are probably very vulnerable to these kinds of attacks. In principle if the hardware wallet uses some kind of secure element then probably you are fine with side channels. If it is just an application microcontroller then there is a pretty big attack surface for side channels and deleting and fault injections.

Q - One feature that I’d love to see in hardware wallets is it always give you a delay. If I enter my PIN code or even before I can enter my PIN code, just wait 24 hours. If somebody wants to rob you physically they have to wait 24 hours.

Q - That also means you can’t spend your money for 24 hours.

Q - Maybe it is like different PIN codes for different periods on how long you have to wait.

A - There is another option. You can have a PIN code, like in banking applications, that erases, wipes the device. Instead of `1234` you enter `4321` and then everything is erased. I don’t know what will happen to you afterwards. To restore you probably have the seed or maybe Shamir’s Secret Sharing.

Q - The timeout gives you plausibly deniability.

## Frozen memory attack

<https://medium.com/@Zero404Cool/frozen-trezor-data-remanence-attacks-de4d70c9ee8c>

This attack is pretty old actually. It is August 2017, it was fixed a long time ago. The problem was when you load something into the memory it stays there for a while. When you unplug the device from the power it starts to decay. At room temperature it happens pretty quickly. This is a chart of how fast it happens for different devices. At room temperature it is a few hundred milliseconds. But if you take the device, you freeze it, then it can last for 10 seconds for example. What you could do, you plug in your Trezor, it loads into the memory your PIN code and you mnemonic phrase. Then you can trigger a firmware upgrade. You unplug the device, plug it back and then start update process, you get your new firmware and then you can read out the contents of the memory. The whole procedure doesn’t require a PIN. Maybe you forgot your PIN and you just want to wipe your device or something. The solution for this was pretty easy. You just don’t load the mnemonic until the PIN is entered. With this encrypted storage it became even nicer. You don’t even know the PIN. But still it is an attack surface. You need to be careful on what you store in the memory.

## Point multiplication: lookup tables

<https://blog.trezor.io/details-of-security-updates-for-trezor-one-firmware-1-8-0-and-trezor-model-t-firmware-2-1-0-408e59dc012>

Recent attacks, they are not directly fixed because you need to know the PIN and then you control everything. Guys are working on that in Trezor. Again, side channel, when you are computing your public key you take your private key and multiply it by the generator point of the curve. To make it efficient you normally use lookup tables. It is a huge table where you have G, 2G, 3G, 4G and many other Gs. G multiplied by many different numbers. Then when you have a private key, we show it in binary, “Here I have one, I need to add G. Here I have another one I need to add 2G. Here I have zero so I don’t need to add 6G, I go further and I add 8G here”. All these values, you don’t compute by yourself, you take them from the lookup table. It improves the performance of the signing and public key derivation by roughly a factor of 3. But the problem is when you are accessing different regions of the memory of this lookup table you provide some information to the outside. I think again it was the electromagnetic radiation. Maybe power consumption. Here the easy fix would be to not use lookup tables and multiply the numbers. But it is not really an issue, I don’t know if they will downgrade the performance or not. To ask for the public key you need to know the PIN. I see some problems with that in future. When for example you have a hardware wallet that supports Lightning Network and you want to keep it locked at home. It routes the payments for you, it does all the automatic stuff and verifies that you are only earning money. Here you can have an attack surface for these kinds of side channels. But right now it is not an issue because no one supports Lightning Network yet, even coinjoin.

## Hardware

We are done with the software attacks, now to the hardware side.

## Scalar multiplication: imul instruction

<https://blog.trezor.io/details-of-security-updates-for-trezor-one-firmware-1-8-0-and-trezor-model-t-firmware-2-1-0-408e59dc012>

Trezor again. A major player in the talk. Scalar multiplication, basically the same stuff. Even if you don’t use the lookup tables and you try to compute the public key. What you normally do during this computation, you take huge numbers, 256 bit numbers, and you need to multiply them. The microcontroller cannot multiply such huge numbers. We have 32 bit, 64 bit. So you need to split it into smaller pieces. In the current implementation they use 30 bit numbers, the leftover is 16 bits, and then you multiply them. The problem with the multiplication instruction on the hardware level, on the semiconductor level, they use slightly different implementations depending on the value of the number. When you are using 30 by 30 bit number multiplication it will be one instruction, 30 by 16 will be different, with two small numbers even more different. Another thing where performance gave you an attack surface on the side channel. Here there is a way to slightly change the implementation of the elliptic curve calculation and use roughly the same length of these words for multiplication and not one of them is much shorter than the other. Then you should be safe. It is a hardware problem that needs to be fixed by changing the software implementation.

## SRAM dump

<https://blog.trezor.io/details-of-security-updates-for-trezor-one-firmware-1-8-0-and-trezor-model-t-firmware-2-1-0-408e59dc012>

Another hack that was [demonstrated](https://www.youtube.com/watch?v=Y1OBIGslgGM) at the Hacker Congress in Leipzig in December by the wallet.fail guys. This was a great talk. What they showed is how you can extract the firmware including the PIN code and the mnemonic phrase from Trezor using a pretty nice tool. It looked like this. You have the thing, you put your Trezor microcontroller and you get everything. The problem there was they were able to glitch the chip in such a way that the protection level of the chip implemented by the manufacturer of the chip can be downgraded. The chip normally has three different RDP levels of access to the memory. Level 0 is full access. When you connect your debug interface you can read and write anything, both from the memory and from the Flash. Then there is Level 1 that is used by most consumer electronics. When you connect the debugger you can read only the memory but you cannot read what is in the Flash. And then finally Level 2 that doesn’t give you any access to any information. Trezor normally uses RDP Level 2 so you should be safe. This is implemented in software actually. Your microcontroller boots in Level 0, then it quickly changes it to Level 1, Level 2 and then you are fine. If you glitch at the right moment then you can downgrade from Level 2 to Level 1. What glitching does, it allows you to skip certain instructions or make them complete in a wrong way. The problem is still that the mnemonic phrase is in the Flash. Here on Level 1 you don’t have access to the Flash. What you need to do, you need to first somehow move your mnemonic to the memory and then use this glitch. What they did, they started an update process. What happens during the update process? Normally you don’t want the user to reenter your mnemonic. You just copy all the secret information into the memory and start writing into the Flash new firmware. At this moment you glitch and downgrade the protection level to Level 1, cool you have access to the memory and you have the mnemonic in your memory. You have everything.

## Cortex M3 bug

<https://blog.trezor.io/trezor-one-firmware-update-1-6-1-eecd0534ab95>

Another problem that was fixed already by the semi-conductor manufacturers, SD Microelectronics. It was discovered on Trezor. The problem is on Cortex M3, the one that was used in the Trezor Model One, there was an annoying bug. You can set this protection level by putting a certain value into the register and committing this value to writing it on the chip. Then you should be safe. The problem was what you could do, you could write to the chip the Level 2 and then you write to the register a different value, for instance AA. The microcontroller for some reason was taking not the value that is stored in the microcontroller itself but the value in this register. You can put any value without committing it and you completely remove the read protection this way. It is also pretty annoying but it was fixed by implementing the software workaround. It is a little complicated.

## F00DBABE

Another nice one is from Ledger, also from the CCC conference. The Ledger architecture, you have a secure element, then you have the microcontroller that controls your display and the buttons, then you have the USB for communication. What happens when you update the firmware on Ledger? When you start updating there is a register in part of the memory where the Ledger stores a certain magic value. When the update process starts, before the verification, the microcontroller sets this value to all zeros and after writing the full firmware it verifies that the signatures are ok, that the firmware comes from Ledger and if it is true then it puts back the F00DBABE to this register. You don’t have access to this register during the firmware update. If you don’t have a signature you still have zeros so the hardware wallet will not start at all. You need to put back the original firmware. The problem was that if you carefully read the manual for the microcontroller you will see that the same parts of the Flash can be accessed with this memory mapping, with different addresses. This meant that if you try to put something into `000_3000` it would effectively write this value to this magic memory region `800_3000`. Using the simple bug that was caused by not carefully reading the documentation of the microcontroller. It is easy to skip this thing because it is 150 pages long, the documentation for the microcontroller. It is painful to read it but if you are developing a security device you should probably read it. You can write whatever you want to whatever value you want and then it looks like valid firmware. This is the video that they demonstrated. Your device is genuine but you can play Snake on it. You still don’t have access to the secure element, to your private keys, but you do control the display and the buttons. This means that in principle by slightly changing the firmware you can encode something “Please always consider the second output as the change address and never show it to the user”. Together with a compromised computer you can steal all their funds, I still think it is an issue. It was fixed by the way.

## Architecture

Then the architecture.

## Man In The Middle

<https://saleemrashid.com/2018/03/20/breaking-ledger-security-model/>

Still about Ledger. The recent Ledger Model X, even though they advertise it as Bluetooth the real nice thing about it is they improved the architecture. Before on Ledger Nano S they had this microcontroller that is like a Man In The Middle. It controls all the important parts like the screen and the buttons. Whatever you see you see it not from the secure element but from this microcontroller. If this guy (the MCU) gets hacked then you are probably screwed because you don’t need to have access to the mnemonic itself, you just need to fool the user to get you the signature. Displaying something weird is enough. Together with a previous attack what you can have, during the supply chain attack when you slightly change the firmware here you can set entropy to zero or a defined value that is known by the attacker. Then all the users will always derive the mnemonic that you know. This is another video from Saleem Rashid where he is setting the entropy to zero. He is initializing the new device and the mnemonic looks like “abandon abandon abandon abandon…”. The last one is different. It is when everything is zero but obviously you can set it to arbitrary known by the attacker values.

## Bruteforce attack

<https://twitter.com/FreedomIsntSafe/status/1089976828184342528>

Now about the Coldcard. It is a pretty new wallet and I would say it is pretty safe mostly because you can use it in a completely air gapped mode. You don’t have a bidirectional dataflow and you pass everything with a SD card. But still there is a question about the architecture. What they use, they use a secure key storage chip that can store your keys securely. But it cannot do any PIN verification or elliptic curve calculations. This means that every time when you sign the transaction or whatever you grab your private key from the key storage, put it into the microcontroller, do all the calculations and when you are done you put it back. The same happens with the PIN. With the PIN they use a certain counter inside here. Whenever you enter the wrong PIN the microcontroller increases this counter and asks the key storage for this counter on the next run and waits for a corresponding amount of time. What happens if you put a chip on this bus? This chip is basically blocking the message that is increasing the PIN counter. Then the PIN counter will never be increased, what you can do, this is the demo, you can try as many PINs as you want one by one without any delays. Initially it uses the wait similar to Trezor, first you wait 15 seconds then more and more. Here you just need to enter them one by one. Still you need to wait for half a second before every try, it is hardcoded in the microcontroller. This way you can hack all the PINs that are smaller than 6 digits. Coldcard recommends you to use 8 or 10 digit PINs. This is exactly the reason.

Q - The reason is specifically for this attack?

A - Yes this brute force attack. To communicate to this key storage you need to keep a pairing secret. As soon as you get this pairing secret, using any kind of attack that was demonstrated on Trezor for example, you can just drop all this stuff, directly connect your own fast microcontroller to this key storage and without any delays brute force all the PINs. There will be a limitation due to the communication speed, I think even 8 PIN numbers are breakable if you know the pairing secret. With this MITM in the bus you can easily try 4 or 6 digits in a couple of days.

There is a solution that they decided not to take. There is another counter in this key storage that cannot be reset at all. You can design the protocol in such a way that your mnemonic is stored encrypted and is recoverable only until this counter reaches a certain value, let’s say 10. But this would mean that in total you have only 10 tries to enter the wrong PIN. After 10 tries you need to throw away your device and get a new one. But on the other hand you don’t have a brute force problem. There is a trade-off. I think they decided to go more user friendly than towards security.

## Multisignature flaws

I wanted also to talk a bit about multisignature in general. This is an issue on most of the hardware wallets. Coldcard doesn’t support it currently, they are working on it but it is not released yet. I will tell you why afterwards. Trezor supports multisignature very nicely. They verify everything, they show you the fee, they hide the change addresses from you, they can verify that they are indeed the change addresses and so on. I saw on the Ledger website “Buy our bundle”. I used this bluetooth thing for my everyday expenses where I store a small amount and then I use 2-of-2 multisignature between these two devices to keep my life savings safe. This guy is stored somewhere in my safe at home. Even if some guys get that device, still I am safe because I’m using 2-of-2 multisignature. The problem is that when you try to display the address on the screen of the device, when you are using Ledger and multisignature, you can’t really do it. But it is important. Imagine I want to be sure that I am sending my Bitcoin to my multisignature address. How would I do it if I can’t verify it on the screen of the device? What should I rely on? This is the first problem. The second problem, I feel bad I bought this device. This is the Ledger Model Blue. It never gets the firmware updates, they dropped support for it and they don’t want to develop it anymore. I feel like I spent 300 euros for a brick. This is what the multisignature transaction looks like when you try to do it on Ledger Blue. Still even on the Ledger Nano S it will display the fee but it will not display that one of the addresses is the change address. I cannot verify that the change money is going back to my address. We really need to work more on the multisignature side of hardware wallets. Right now if you are trying to use multisignature you decrease your security and that is weird.

<https://github.com/stepansnigirev/random_notes/blob/master/psbt_multisig.md>

Another problem on the protocol, this is probably the reason why Coldcard still don’t have the multisignature support. I sent an email to the mailing list. This is the missing piece in the partially signed Bitcoin transaction (PSBT) format. Imagine that we have a 2-of-4 multisignature scheme. We use 2 hardware wallets, one air gapped computer and one paper backup. And we have 4 keys, we have our addresses that use these 4 keys. If there are 2 signatures then we are fine. When we are preparing the transaction what do we want? We have the input, we have the keys there, we need to know the derivation path for these keys and then for our change address our software wallet, watch only wallet should be able to tell us that these are the keys derived from the same master keys as the inputs. Then we can consider that this thing is the change output and we are good. The problem right now is that in the PSBT you don’t have the master public key field. You only have the derivation path where you have a fingerprint and derivation indexes. This means that if I am sending this information to one of these two guys they will be able to verify that their keys are here but they have no idea about the other two. They will just have to trust that they are not replaced by something else. What the attacker can do is replace two other keys with his key and then using a pure PSBT that Coldcard is trying to do you can lose all the money because the attacker also controls this output. Hopefully we will add xpub fields to PSBT and then you are fine.

## Should we trust chip manufacturers?

<https://www.aisec.fraunhofer.de/content/dam/aisec/ResearchExcellence/woot17-paper-obermaier.pdf>

Another thing that I want to say about architecture and hardware in general. The problem is we don’t really know what is happening inside the chips, what capabilities they have. Maybe they have backdoors. It was shown actually. These are three research papers, Skorobogatov from Cambridge, which demonstrate there is a backdoor or some hidden functionality in the debug interface of the security focused… And other things like how to make the microcontrollers work less securely than they should. I would say that what I would like to see in hardware wallets is chips from different vendors, ideally open source cores. Right now the only option for that is RISC-V architecture that has an open source core. Unfortunately there are no security focused devices based on that. Plus all the vendors take this open source core and put proprietary stuff around it. Pretty sad. But at least we have a core. Ideally we should be able to take this open source core, put some open source anti-tamper and security features around it and have a completely open source chip. That would be perfect. But for now what can we do?

## Wishlist

We can at least stop relying on a single manufacturer and single chip. When we have Schnorr multisignature, then we can store the keys on different parts of our device, one on the secure element, one on a microcontroller, another on another microcontroller. Maybe the third one on the computer. Then we merge them together in such a way that the full key is never assembled in a single part of the chip. Or at least to make the hardware untrusted. For that I have one proposal that I wrote sometime ago.

## Bonus: if hardware wallet is hacked

Imagine if you have a hardware wallet and this hardware wallet is hacked. Let’s say you are super paranoid and you are using it in a completely air gapped way. You can go to a remote part, inside a Faraday cage and you do everything in a super paranoid way. How can the attacker, this malicious hardware wallet, disclose your private key? There is a way. In every signature that you are generating you have a wonderful thing called a random nonce, the blinding factor. For every signature you need to generate a random number or a pseudorandom number according to certain standards, and then use it to generate the signature itself. If the hardware wallet is compromised he can pick whatever random number he wants including not a random number. Including the number that is known to the attacker. With this signature you can leak some information about your private keys. The attacker doesn’t need to compromise your computer, it just needs to scan the blockchain for certain patterns, for certain keys or transactions with certain flags. I had a proof of concept demo where I was able to extract the master private key in roughly 24 transactions. What you could do instead, you don’t let the hardware wallet choose this random nonce. You have a software wallet that is not compromised and a hardware wallet that is compromised. It is the other way around compared to normal assumptions. Then on the software wallet you generate a random number and send the hash of this random number to the hardware wallet. The hardware wallet then needs to commit to this certain nonce that it will use. Basically after this commitment it cannot change it because otherwise you will reject the transaction. Then you tell him the random number and verify that for the signature he was using this number (k) plus this number (n). Then if one of these parts is honest then you are safe. In principle even if this (k) is not a random number, by adding a random number to it you randomize everything. Something like this is already implemented in the Schnorr MuSig protocol. We can extend it also to ECDSA.

## Q&A

Q - …

A - There are different types of supply chain attacks. First is when you swap the device for another one. Here ideally every device should come with a unique key that can be verified by you that this key belongs to the vendor. What you can do is ask the device to sign a random message, get the signature and then verify that the signature corresponds to the public key that you are expecting. For example we are sending you a hardware wallet via post and we are also sending you an email with a public key of the device that is coming to you. Then the only way to forge the device is to extract this key somehow. If it is not possible then you can authenticate that this is the device that was sent to you. This is the first option. The second supply chain attack is when the chip is still there but there are additional components or hardware implants. How do you solve that? Coldcard is doing pretty well by using a transparent casing. I would say that all countermeasures of Trezor and Ledger, Ledger don’t have any, Trezor has this whole graphic thing that is not really secure. For us we are actually planning to do transparent casing as well but there are ways, if you are thinking about really large amounts, to make sure that the whole device is genuine. I can tell you how. There is such a thing as physically unclonable function. Let’s say you have the casing itself and it obviously has a bunch of perfections. You can use these perfections that appeared due to manufacturing processes as a unique fingerprint of the fingerprint. This fingerprint you can use to derive some kind of secret key. Physically unclonable means it is extremely hard to manufacture something even close to that. Also what you can do, there are a few groups working in this direction, even if you drill a tiny hole then you screw up this key. There are a few ways. One approach is where you cover the whole device with a conductive mesh and on the boot of the device you are measuring the frequency response of this mesh. From these measurements you derive the key. The second one, there was a talk at CCC, you can emit the electromagnetic radiation from the inside of the chip. It will be reflected by the boundaries of the casing and they will obviously interfere. Then you measure this interference pattern and from this pattern you derive the key. There is a third one that is hard to implement but might be possible. When you use a speckled pattern on the optical propagation of the laser light. The casing is made of glass, you put some laser light in there, it bounces back and forth, reflects and interferes with imperfections of the material. This is the ultimate level. The problem with these things is it is still in development and it is also raising the price of the device quite a bit. If you drop it it may break. Also in some of these solutions if you increase the temperature there will be a different key. To turn on your device you may need to go to the room where you have exactly 22 degrees.

Q - The electromagnetic field changes?

A - It is not very sensitive to magnetic fields. This electromagnetic reflection and interference is sensitive to temperature because the air pressure and the density and the index of reflection changes so the optical path is changing. With a mesh it is easier but the problem is that in our case we need to put a display in there somehow. That is the problem. Right now what we decided to do, we have transparent casing and we only have the wires that are coming from the chip to the display. Every time when you turn it on you verify that it looks good.

Q - It would be cool to have a compass, you have to hold it in a certain direction.

A - In principle there are plenty of ways how you can move away from just a simple PIN to something crazier. For example you have the compass and the orientation or some movements. You make your magic dance and then it unlocks. Also what we discussed in London, this challenge and response. You don’t enter the same PIN all the time. Before you enter the digits your hardware wallet vibrates a few times and then you add the number of vibrations to your digit. Every time your PIN will be different. Different crazy things. Hopefully with the developer board you could do something like that. But for the consumer device you don’t want to go that crazy.

Q - My first question is about hardware but in mobile phones, coming out with secure storage for private keys for example. Samsung is coming out with a device similar to that. In the future perhaps we could see mobile phones with integrated hardware wallets. Based on what we know of these devices right now have you explored any attack vectors to find out if they are secure or not. My second question, right now we have a lot of apps that are mobile wallets. They use secure storage for various data, the private keys are stored securely on the mobile phone, Abra and Bluewallet for example. What are the attack vectors for such apps? Have there been any known breaches?

A - I didn’t look closely into that. I’ve heard a few talks about that. You split your phone into two parts, your process into two parts: insecure world and secure world. If these apps that are running on the secure side are implemented correctly then you are pretty much safe. There are still issues with the shared memory and some side channels. By design the secure storage is not resistant to side channel attacks. By side channel attacks I mean not even the physical side channels like power consumption and stuff. You can check how much memory and how much processing time this process is using. It is not a completely physically isolated storage. It is running on the same microcontroller so you still have some issues. Also if the application that is running on the secure side is screwed then you are probably screwed. If that part has a vulnerability you can explore that and you can get into the secure side of the process. I would say that it is much better than just using an app, better to use secure storage than not to use it, but it is not an ultimate solution. I would still say that for everyday expenses you can use your phone but for larger you need a dedicated device, ideally cold storage.

Q - With mobile phones using secure storage for critical data like private keys and mnemonics, have there been any dedicated attempts to deconstruct the app and figure out what the logic is. Maybe not in iOS but in Android devices, have there been any known issues like that?

A - You mean for Bitcoin applications? Regarding that I don’t know. It is still a pretty new field for attackers and for the security investigators. There are no nicely developed toolboxes to do all these kinds of things. I think we will see some attacks in this direction later on as the Bitcoin ecosystem evolves but right now I don’t know about any of them. We just got some interest from the researchers into the hardware wallets and then we had a very productive winter. Maybe the next frontier will be apps.

Q - Can you have an attacker at the assembly level when they assemble the component?

A - Yes. For example, when the microcontroller is talking to the display and the buttons, this is the most obvious one. If you are using Trezor T they have a touchscreen. If you are using Ledger X there is a display controller that is controlling the device. These are separate chips, not the microcontroller itself. They obviously have firmware. With the standard components you cannot verify that they are genuine or not. You talk to it and hope it is ok. On the assembler level I would say that you can flip the display driver to another one that analyzes what is sent to it and then changes it. This is an issue. On the touchscreen controller the same. You can add some functionality to the firmware there, to touch the thing whenever some trigger happens. It is a pretty sophisticated attack I would say. I doubt that we will see it in the wild, at least now. But in principle they are possible. On the other hand vendors can ask the manufacturers of the touch screen drivers or display drivers to use custom firmware that also has a unique private, public keypair. Then you can authenticate the device. The problem is it becomes more expensive and you need to order on large scales to get them interested.

Q - Someone on Twitter said that the next attack on hardware wallets is going to be an insider job from the manufacturer of the hardware wallet. How do you protect that? If you are a manufacturer and one of your staff is an insider doing an inside job how are you going to protect against that?

A - What I said on the previous slide, this is what I was trying to solve. I don’t want to trust the manufacturer at all. I want to be able to use the hardware wallet even if I consider it can be hacked. Some kind of untrusted setup would help.

Q - For the entropy?

A - Entropy provided by the user. If you don’t trust the hardware random generator you can also ask the user “Please keep pressing these buttons. I will tell you what they are and then you can actually verify.” This is the number that I generated by the hardware random generator, you have a 32 byte number let’s say. Then you start hitting the buttons and you have a string that you hash together with this random number and you get the entropy that is produced by both the hardware and by you. You can verify it, you can XOR in your head right?!

Q - No. I could have the computer do a similar game as that right?

A - Yeah. Here we ended up with a random number that is not known by the computer and it is forced by the computer to be random. You can use the same scheme for the key derivation. I just don’t like plugging anything into the computer, that is why I thought about the mind method. On the other hand the communication doesn’t have to be over USB. You can use QR codes or whatever, audio channel, QR is probably better because it is more space constrained. That is the perfect world where you don’t need to rely on the manufacturers or on the insiders and still operate securely.

Q - You can take quite a few countermeausures. I think Ledger for example, when they release a firmware binary, a bunch of people have to sign off on it and that gets deterministically built as well. It is not like someone can sneak a binary into a specific user’s device.

A - Another thing, you ship everything blank. The only thing that is on the microcontroller is the key from the factory that is verifying the bootloader is fine. Then you can still mess up the bootloader probably or you can make a setup procedure that uploads the firmware and also updates the bootloader. Then if you build deterministically you don’t need to trust anyone. You just build, you compare this against firmware from the vendor, you still need to use firmware from the vendor because it has signatures.

Q - The other thing that scares me is some sort of government order to ship a firmware update to a specific customer plus a gag order. They can’t tell anybody else that they are doing it. They could steal money from one specific user. I think one solution to that could be all firmware updates have to be committed to the blockchain, a hash, in a particular way. Then at least your own computer can see that there is a firmware update and that everybody in the world is seeing that firmware update. You are not getting a special firmware update. That would be done on your computer so it doesn’t work if your computer is also compromised. It will at least prevent someone specifically messing with your hardware wallet.

A - I just don’t like putting data on the blockchain.

Q - You could put it on a website but that website can look different from wherever your IP address is.j

Q - If you use pay-to-contract then it doesn’t cost any block space.

Q - This is one UTXO per quarter so you can do it efficiently.

A - Probably the optimal way would be to run a sidechain for that.

Q - I guess the government would work around this by putting a camera in your home and waiting for you to enter your PIN code.

A - Or just taking you to their facilities and asking you to do whatever they want. Different levels of paranoia.

Q - I would want there to be a ban on your neighbors having an Alexa because if they put it next to the walls. Those things are scary but then so is your phone. Anything with a camera can also be used as a microphone indirectly, you can film a Coca Cola bottle through the window and get the audio.

A - There are other interesting side channel attacks on these kinds of general things. You can use the fan on your computer to send the data by speeding it up and slowing it down. It is a pretty slow thing but still your fan can be a communication channel. Then if you are using a standard computer that is plugged to your power plug and you are using an old keyboard then by listening to the signal on this power line in the same building, maybe a few floors away, you can guess what keys were pressed, you have a key logger in your power plug. Crazy stuff. I would definitely recommend watching some Defcon, CCC and Black Hat talks, it is amazing what you can hack and how.

Q - Regarding multisig you said ideally multi device setup would be best. Trezor is working quite well but what if you use Ledger, Trezor and Coldcard for example?

A - Coldcard will hopefully get it soon. Ledger are not fixing this issue so I would not recommend using Ledger in the multisignature setup. The workaround I found to do this is if I write a software wallet that asks Ledger to display at least his public key, his address corresponding to this change or receiving address and then having my own do-it-yourself device that can show me all the public keys and addresses of all the three. It is ok but it is an ugly workaround I would say. Bitcoin App is actually open source so if someone would spend a few weeks ago and putting in proper support for mulitisignature in their app then it would be great. But right now as soon as Coldcard implements multisig I would probably use Trezor and Coldcard. When we release I think we will use ours together with Trezor and Coldcard. I don’t know any other nice hardware wallets unfortunately.

Q - The PSBT format, it is a BIP, they can implement the xpub field?

A - Hopefully as soon as we have more hardware wallets that support PSBT natively and if we continue working on PSBT then we will have many interesting applications. For example another one that we are working on right now with Trezor is how to implement coinjoins securely on the hardware wallet. It is pretty challenging. Here you have a bunch of inputs from random people and you can fool the hardware wallet by saying “This input is yours and this one is not yours”. Even though both of them are yours. Then you flip it. There are ways with a recent PSBT implementation to steal the money using coinjoin. But hopefully also we will develop a scheme that makes it secure and then ideally all the hardware wallets that support PSBT will be nice enough to work with multisignature and coinjoin and other stuff.

Q - So without PSBT how are these wallets transferring the partially signed transaction?

A - Every vendor has their own format. Ledger are using APDU commands that are normally used in communication with smartcards. They have a very specific format in principle. Trezor is using Google’s protobuf as a communication protocol. They implement something very similar to PSBT, by changing a few bytes you will get PSBT, it is easy to transfer them back and forth. Coldcard is using PSBT. Others I don’t know. Before PSBT we had a bunch of different formats, now we have plus one different format but hopefully this one will become standard. The nice thing is that we have a tool, [HWI](https://github.com/bitcoin-core/HWI), that is in the Bitcoin Core repository, a Python tool that converts from PSBT to any of those devices. Using that you can forget about all other standards, you only use PSBT. Then you will be able to communicate through this universal translator to all of the hardware wallets.

Q - What’s that tool?

A - It is called HWI, hardware wallet interface. It is in the same organization as Bitcoin Core. The nice thing is that it is pretty easy to implement. If you decide to do your own hardware wallet for instance you take this tool, you make a few Python files, you write in Python, everything is nice and convenient and then you have your own wallet integration into this format. No matter what type of communication you use. Pretty nice project I would say.

Q - You went through some of the hardware issues, most of them if not all were solved by firmware updates. What would have to happen for them not to be able to be resolved by firmware updates?

A - With the Cortex M3 bug it was a problem by the manufacturer. Basically they fixed it for a particular use case. It is still an issue. Maybe it was fixed by the manufacturer afterwards but you can’t update hardware itself. It was fixed in such a way that at least you can’t extract secrets from the Trezor. They had to place the secret in a certain place such that when you log the device the bootloader overrides this part during the firmware updates and things like that. It was really a workaround. As far as I know there is an attack that Ledger discovered on all Cortex M cores that are not really fixable. I think the Trezor guys will still fix it somehow in the software but unfortunately Ledger did not disclose exactly the details of the attack. So no one really knows what it is about. It is hard to fix something that people don’t give you the information for. In principle I would say most of Trezor’s problems are coming from the fact that they are using an application microcontroller. These are not designed to protect against all kinds of hardware attacks. They try really hard and really well to protect against all of them but I feel like there will be more and more in the upcoming years just because of the architecture limitations. This is why I said my dream is to make a secure thing that has internal power reference, anti tamper mechanisms and is still open source and used by all kinds of hardware wallets. You can verify that by putting it into the X-ray machine and checking the semiconductors that are there but it is not going to happen in the next couple of years. It is more like a goal for a decade. But Bitcoin is changing the world so we can also change the semiconductor industry.

## Hardware wallets and Lightning

Q - You did a presentation on the role of hardware wallets in Lightning. I’m trying to understand how hardware wallets will be used with regards to end users and also routing nodes. I’m struggling to understand how routing nodes are going to use hardware wallets.

A - The problem is if you are a routing node you have open channels and you are routing the transaction. This means that someone offered you a HTLC that gives you some money if you give back the hash. Then you offer a slightly smaller amount of money to another node if he gives you the hash. If he gives you the hash you can pass this hash forward and then you earn some fees. For the hardware wallet it is important that you get all these pairs together such that you can verify on the hardware itself, you don’t want to click the button all the time “Ok yes I want to earn 1 satoshi”, “Yes I want to earn another satoshi”. Instead it should happen automatically as soon as you have two transactions that in total increase the amount of funds of the user. In principle it doesn’t look complicated, it becomes harder if you think about what can happen to this channel. We have me as a hardware wallet and as a node, we have two guys, I have to open channels with them. If my node is compromised, this is the goal of the hardware wallet, if the computer is compromised you still have the funds secure. This node closes the channel unilaterally. Then we wait for one day, we don’t tell this to the hardware wallet. The hardware wallet still thinks there is a channel open and you can get channel updates. You update the channel increasing the funds of the user on this non-existing channel and then you steal the money from the other channel. The hardware wallet will sign. The problem here is that hardware wallets for Lightning need to monitor the blockchain. They need to get every 10 minutes or whatever new blocks, they need to check the block, parse the block and see that there are no channel closing transactions for the channel that they have. They need to store the database, either on the node encrypted and authenticated, or on the SD card. Plus you need a real time clock because how do you know that the timelock didn’t pass? You tell the hardware wallet “No the 1 day didn’t pass yet”. You need a realtime clock. You need a lot of other stuff to make it happen.

Q - The block header would be enough right?

A - Imagine you start delaying the blocks. Instead of sending them every 10 minutes you send them every 20 minutes. Delay the blocks. The hardware wallet needs to know the time, it needs a real time clock because in the block you have the timestamp. If you don’t have a real time clock you can’t verify that the block is coming to you is the current block and isn’t from 1 day ago. Then another problem, what happens if you have the HTLC update and when you are trying to push another one you get disconnected, then this channel is closed and you can steal one routing payment. The node is still hacked. There are plenty of problems in here. It looks like in general that the hardware wallets that we currently have, they will still work and make your private keys for Lightning much more secure than when you store them in the node, but it is not perfect security. To have perfect security of your keys, assuming the hardware wallet is not hacked, you will also need to have some kind of backup channel or watchtowers and other stuff. The problem with Lightning is it is very interactive and has time constraints. But in principle having the secret keys on the hardware wallet and verifying this transaction, it is already much better.

Q - It seems to me to have Lightning on a hardware wallet, the hardware wallet needs to be a full node. It has to monitor all these blocks and check that they are valid.

Q - It has to be one with full access to the internet because otherwise you are just performing an eclipse attack. You can do all sorts of things with eclipse attacks including making it look like the Bitcoin difficulty is going down. You have to trust the computer you are connected to. Let’s say you have a little node at home connected to a hardware wallet, you go on vacation and somebody breaks into your house, it would be nice if there’s no way for them to take your money without unplugging it and turning it off. Just that I think would be nice.

A - It would also be nice to have your Lightning node in the cloud without any secrets. You have public IP, you can do it however you want and then you have your hardware wallet at home that is connected to this node in the cloud. You don’t put your private keys into the cloud of Digital Ocean or Amazon or Google.

Q - You are still trusting them a little bit.

A - In Lightning you can’t completely remove the trust in your computer but you can try to diversify the risks a bit.

Q - Is it fast enough?

A - Depending on how many transactions you are routing. If you are trying to route 1000 transactions per second, that probably never happens in Lightning through one node, then you might have problems. But in principle I think it is 30 milliseconds per signature so 100 easily.

Q - Just plug in multiple hardware wallets.

A - Alternatively you can have HSMs, this rack of hardware wallets that are processing that. You can also have a load balancer, they all need to agree on the state of the channels. Or you can run multiple nodes, this is also ok. I don’t know how many transactions you are routing per second? 70,000 in 3 months? So easily doable with a hardware wallet if they don’t come in within 1 second.

Q - How durable are hardware wallets? With a normal hardware wallet you might sign a couple of transactions. But now you are talking about signing a lot of transactions. Is it going to burn out?

A - I don’t think so. I didn’t test them intensively, I’d run our chip through a bunch of transactions. As long as we are not doing heavy multiparty computation it is ok. One signature per second is safe. The hottest part in the hardware wallet right now is the display actually. Signing is not a big deal there.

Q - It is a great problem to have. The chip gets so hot that you are routing so many Lightning payments.

A - If you earn 1 satoshi per payment then it is a pretty effective miner I would say.

Q - That would mean the Lightning wallet in Trezor would be a custodial node?

A - Not necessarily. You can still run your own node and Trezor plugs into your computer. Why do you need to go custodial? It has to be hot, permanently connected to the computer. The problem there is if you leave your hardware wallet unintended in the current setup you keep it unlocked because you entered the PIN so people can steal your funds. For that kind of thing you need to think about outer locking and keeping the transactions going.

Q - It is like the coinjoin right? With the coinjoin you could leave it on at home but it will only sign transactions that make it richer, otherwise it will turn itself off.

A - Yeah. Then we don’t need to rely on the centralized service and pay the fees, we can actually earn something. Alternatively a coinjoin transaction doesn’t happen instantly. Right now if you try to do it with a hardware wallet you will probably need to confirm a few times. First you need to commit, second you need to sign, then if the transaction fails you need to sign again a slightly different transaction. Another approach, you commit once to a type of transaction, not a transaction itself but a transaction that has to have these inputs and these outputs. I don’t care about the other stuff. You confirm once, the rest happens automatically. I would say coinjoin support will happen pretty soon in Trezor and Wasabi, Wasabi is already integrating hardware wallets but you can’t use it with coinjoins. The next step would be to make it happen. Not in two weeks but maybe in a few months.

Q - LND uses macaroons. Do you know much about macaroons?

A - Not really, I normally work with c-lightning.

Q - Would you set LND up such that if you are signing transactions you’d require a hardware wallet but if you are doing read only functions you wouldn’t.

A - What kind of read only functions? In Lightning there are three types of private keys. The first one that is controlling onchain transactions, another one that is controlling channel updates and a third one that is controlling your node ID. I would say keeping the node ID on the Lightning node is fine. Then you can broadcast your channels or connect to other nodes but you cannot open channels, you cannot route payments, you can’t do anything valuable. You can only watch the network and observe what is happening there.

Q - It is still useful for things like watchtowers though. You don’t necessarily have to have the ability to sign transactions.

A - For a watchtower do you even need to be a Lightning node? You can just sit and watch the blockchain. A service built on top of bitcoind or something.

Q - I can’t remember which presentation but you said C has a bunch of built in functions, many of them are not secure. Using C, isn’t that just a challenge of training developers to only use the secure functions and not using the insecure ones or is there a problem with using C generally and people should use other languages such as Rust?

A - C has a bunch of functions that are not secure but you can use secure versions of them. If you know what you are doing you are perfectly fine working in C. You can easily mistakes there. You can use some tools like static code analyzers or cover everything with tests, also hire smart developers that are careful enough and have experience in security. It is doable. Still most of the embedded devices are written in C. Even the Java virtual machine that is inside the smart card was written in C. You can make secure firmware in C. It is just much easier if you use a memory safe language. You decrease the number of potential bugs, you make the overall flow easier, you spend less time on that. In that sense Trezor decided to go with MicroPython. It is a pretty good choice. I still think that it is not very well developed so you may have some issues. Probably better than C. Coldcard is doing the same, I think that they even use Trezor’s MicroPython bindings to Trezor’s crypto libraries. By the way be careful with that. This means that security updates on the Trezor crypto libraries will appear on the Coldcard a little bit later, they are a fork. Then what is interesting right now, embedded trust is super interesting. Folks were tired of the memory consumptions and leaks in Firefox so they invented a new language. But they also designed it like a system programming language for security critical applications. Now it is going to embedded development so you can start playing on a few boards that they support. Around 10 but you can port to any board. You can have both C parts of the code that you normally get from the manufacturer of the libraries and API. And you can write Rust parts, they all work together. There is even an OS that allows you to write everything in C but you can’t be sure that each process is separated from each other. Even if you have bugs in the SD card driver or system driver you don’t expose any secrets because you have a supervisor of the whole flow.

Q - McAfee’s super device, is it secure? McAfee said it is unhackable.

A - I didn’t look at it. It was hacked the next day or so.

Q - You can run Doom on it but is it really hacked? Can you extract private keys out of it?

A - I don’t know. We have a bunch of new game consoles. McAfee’s Doom, Ledger’s Snake. You can also upload custom firmware on Trezor and play whatever game you want there.

Q - Wasn’t the McAfee problem also that it was just a phone number password. You could brute force and start taking money from random people.

A - Fortunately I didn’t look into this product and I feel I don’t need to spend time on that.

Q - Security consultants usually don’t consider this a major player in the market of hardware wallets?

A - There are also other hardware wallets that are either based on Android phones or something like Raspberry Pi and I don’t think they are really secure. The only way for instance to make a reasonable hardware wallet on Raspberry Pi is if you get rid of the whole operating system and program on the bare metal, the powerful microcontroller that it has. Then you have a pretty nice thing that is super fast, it is hard to glitch with precise timing because it is fast and has multithreading. Still a reasonable choice but don’t run a full OS on there, it is too much.

Q - There is Ledger and there is Trezor and there is other stuff. The other stuff, there isn’t really anything coming up, Coldcard is coming up. KeepKey is nowhere in terms of traffic and sales.

A - Who has hardware wallets that are not Trezor or Ledger? Coldcard? The market is mostly covered by Trezors and Ledgers. I personally have two Ledgers and two Trezors and I have Digital Bitbox but I don’t use any of them for Bitcoin storage. I just play with them and like to see how they look inside.

Q - Would you like to discuss CryptoAdvance?

A - Quickly to say, we are doing not just a hardware wallet but hopefully a whole platform. One quote I really liked from one of the talks is “Your security model is not my security model” but yours is probably fine. If we can make a tool that is flexible enough to cover all craziness of Bitcoin hodlers so they can make something custom for them then it would be great. That is what we are focusing on as well as a normal hardware wallet because normal people also need to store Bitcoin somewhere. And we are currently in the fundraising phase, we are here today and tomorrow. If you are interested in developing something on top of our platform or any other, talking about hardware security or about our project talk to us. I didn’t to say that everyone is bad and we are good because we will also fail at some points and have certain attacks. I hope in two years I will come here again and give a 2 hour presentation about our hacks and how we fix them.

