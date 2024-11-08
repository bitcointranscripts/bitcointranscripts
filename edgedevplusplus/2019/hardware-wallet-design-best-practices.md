---
title: Hardware Wallet Design Best Practices
transcript_by: Bryan Bishop
tags:
  - hardware-wallet
  - security-problems
speakers:
  - Stepan Snigirev
date: 2019-09-10
aliases:
  - /scalingbitcoin/tel-aviv-2019/edgedevplusplus/hardware-wallet-design-best-practices
---
<https://twitter.com/kanzure/status/1171322716303036417>

## Introduction

We have 30 minutes. This was a talk by me and Jimmy but Jimmy talked for like 5 hours yesterday so I'll be talking today.

Imagine you want to start working in bitcoin development. There's a chance you will end up using a hardware wallet. In principle, it's not any different from other software development. There's still programming involved, like for firmware. Wallets have certain features and nuances compared to software wallets. Why are hardware wallets different from normal wallets? What do we need to keep in mind to develop a decent hardware wallet?

## Why do we need hardware wallets?

Back in the day, we were storing keys on our computers and it was bad. We had lots of other crap running there like userspace and malware. We wanted to move the signing keys away from the computer to a separate device. The idea is that the physical isolation is the best form of isolation. We need to reduce the attack space as much as possible. It should be as "dumb" as possible. All of these constraints make this different from a normal software wallet.

## What do we need in a hardware wallet?

In particular, hardware wallets tend to not know what's going on on the blockchain. The hardware wallet should be able to sign transactions and show the user what exactly is being signed or about to be signed. All the information can come from a watchonly Bitcoin Core node on an internet-connected device.

We need some kind of communication channel between our host and our hardware wallet. It can be either something like USB or sdcards that Coldcard is using, or even QR codes that you can scan with cameras and screens and get the transaction details from the computer. Then we need something pretty simple but still capable of signing with elliptic curves, so probably a microcontroller. Also, to keep it simple, we probably have memory and program size constraints.

Finally, we need to have some trusted peripherals for interacting with the user like a display and buttons.

We'll talk about protocol design, secure key storage and generation, firmware security, and other various hints.

## Protocol design

What about the communication protocol. What the hardware wallet should know is the root key. Bryan yesterday covered bip32 and hierarchical deterministic keys. I suppose you know about this now. We have a root key and we can derive any number of addresses from this key. The hardware wallet only knows the root master secret.

We need to show the user what the transaction details are, such as mining fees and where the money is coming from or where it is going. If we have several outputs, then probably one of them is sending money back to the user. We need to determine this and mark it as a change address.

In order to sign, we need to know the derivation path from the master secret. These HD keys tree is really enormous. We don't want to bruteforce through all possible keys. We need the actual bip32 derivation path. We also need some information from previous transactions like scriptpubkey, maybe the amount, and maybe your witness scripts. Also, for the change address, we'll talk a bit about this later.

## Partially signed bitcoin transactions (bip174)

Right now the best way to communicate with hardware wallets is partially-signed bitcoin transactions (bip174). This is a good standard. The idea there is that together with the raw transactions that you're sending to the hardware wallet, we also send some metadata. In particular, we add cosigner xpubs for multisig setups. This is not useful for normal keys but for multisig keys it is very beneficial. For each input, we provide the bip32 derivation paths, the scripts, and also previous output information.  There's a difference there for segwit vs legacy. For outputs, if we're talking about a destination address, we don't know anything about that we just send to it. But if there's a change output, then we let the hardware wallet verify that the change output is related to the user's wallet. We need to sign the input with a particular key, so the derivation path here means how to derive this particular private key that will generate a valid key for this particular input that can sign for this input.

Q: What about the derivation path for the output script?

A: We have one root key, and we derive multiple keys from that one root key. We don't like to reuse addresses. Every time you receive bitcoin, we generate a new address corresponding to a new key. So to get a new address, we just bump a number in the bip32 path.

## Change detection

Change outputs are a little bit tricky. What can be considered a change output? If you have an input, and the key was derived there like this like a P2SH-WPKH bip32 key or something. Then it sends to another P2SH-WPKH script. If it's the same address or script, then it's probably change. But what if instead of using nested segwit, we use native segwit? Well, depending on the software wallet used on the host, either you will be able to detect this money or not. Bitcoin Core is watching for all types of scripts, as an example. If you have this address, then it will look for nested segwit, native segwit and legacy transactions. However, other wallets will stick to the same script. So, the point is that change output detection is difficult.

Most watchonly wallets monitor for a certain range of addresses. Electrum has a gap limit of like 20 addresses. Bitcoin Core also has a limited keypool normally it's like 1000 keys or so. If we sign the transaction and detect this as a change address, then mark it as change. The user might not be able to find the money. It makes sense to warn the user that the derivation path looks suspicious or something.

Q: Shouldn't you choose the change address bip32 derivation path?

A: Well, we don't trust the host computer. Say I change the data that is going to the hardware wallet, using malware. Then I can ransom the user and say, if you want the bip32 path, then pay the attacker to get the bip32 path. This assumes the hardware wallet didn't record the bip32 derivation path for the change address. It can't just say, yes the change address is derived from the root key.

Current hardware wallets will detect weird looking bip32 derivation paths for change. Ledger and Trezor hardware wallets currently do this. But if it looks normal, they ignore it and not show it to the user, even though I think it's better to always show it to the user anyway.

With a single key, everything is pretty clear. Multisig is a little more freaky for change detection. We have not only our own key, but we have cosigners. However, we still need to be able to detect the validity of change outputs. We can use a field in PSBT bip174 that provides the master xpubs of the cosigners in the multisig policy. If you have the master xpubs of the cosigners, then you can verify that the change output script is really derived from the master xpubs of the multisig policy. You can verify that the number of signatures in this multisig address is the correct number of keys and so on.

If we're talking about more complex scripts, at the moment no hardware wallets support timelock contracts or HTLCs or anything else. But in principle, what Bitcoin Core and Blockstream also are working on, are a script descriptor language for wallets. This is a way to describe what is the script type and how exactly to derive addresses, for more complex scripts than just a single key or multisig. Separately, there's also miniscript which can help you to define a more complex policy for key derivation. In this case, you will also be able to detect the change, you will just have to check that the policy is the same and the derivations are correct.

## Secure key storage and generation

How we normally backup and generate keys. To get the root secret, normally all the software and hardware wallets, but Bitcoin Core, are using bip39. This is the mnemonic phrase technique.  These are human readable representations of a random number. To generate a key, you start with a good random number. Getting a true random number is pretty challenging. Most of the modern trips have true random number generators builtin, but they are closed-source and yet "certified" so they are probably generating good random numbers but we can't really verify it. We can only trust that they will not degrade over time and that they will not fail. There is the nice feature of random numbers which is that, if you add a random number to anything, it becomes random. You can mix in multiple sources of entropy. You can use multiple heterogenous random number generators or input noise or whatever else. You can also use user input. At the moment, I think both Trezor and Coldcard are using user input, or at least you have an option to do it. Trezor is doing it under the hood. Every time you touch the button or the screen or communicate with the hardware wallet, the Trezor firmware is capturing these timestamps and mixing them into the entropy. Coldcard gives you an option to roll dices and enter the entropy from the dices. Once you mix the entropy togethre, and you use sha256 or some other cryptographic hashing function, then at the end you get better entropy.

From there, you can derive the recovery phrase that is this random number split into pieces of varying bits and then convert it into mnemonic words. The words are selected from the dictionary. There's a standard dictionary of 2048 words described in bip39. It's just a list of words. You look up each word in the dictionary and then you put the information together and there's a result, and also a checksum. There's a few problems with this recovery phrase. I don't particularly like bip39 recovery words, but everyone is using them.

For hardware wallets, we're protecting not just against remote attacks, but also physical local attacks. Attackers can extract secrets from physical hardware if they are using particular techniques.

Another interesting feature in the bip39 standard is the password. It's a user-defined word and every password is kind of correct. You never store the password itself on the device.

## Types of hardware attacks

There are ways to observe information from the wallet by interacting with the hardware device in non-usual ways. Sidechannel attacks are quite interesting. There's ways of monitoring power utilization, or you can monitor the chip with a microscope. You can also freeze the chip in liquid nitrogen, then flash new firmware, and read out the RAM memory. All these things are used to hack hardware wallets. These are real attacks.

There's interaction attacks where you interact with the wallet in non-usual ways. You can shoot a laser into the memory and erase bits that are stored there, like the pin counter. You just shoot a laser, and wipe the bits for the counter, and then you have unlimited tries.

Another good approach is that when you're storing the secret, it should be stored in an encrypted format. If you can observe the memory, then you can't really get the decryption key anyway because it's not stored on the device. The user provides it through a keyboard or something.

Another interesting one is speculative execution.

Fault injections are another powerful thing. When you take the voltage of the chip and you drop it a little bit down, at certain points in time, in a very precise manner, then you can cause a microcontroller to skip an instruction or calculate an instruction in a wrong way. All of this stuff is pretty scary.

To get around these issues, people use secure elements or trusted execution environments. Unfortunately these are not generally available to the public, and you have to sign non-disclosure agreements to get access to program any of these chips. But it's a more secure chip that can protect against some of these attacks.

## PIN code problems

What can go wrong with the PIN code? If you store the correct PIN code inside the device, that's really bad because the software always reads the PIN from memory. There are real attacks that can do this. LedgerHQ was able to use a sidechannel to extract a PIN from a Trezor.

<http://diyhpl.us/wiki/transcripts/breaking-bitcoin/2019/extracting-seeds-from-hardware-wallets/>

Instead, use the PIN code to decrypt the mnemonic or something. Or generate a bunch of random data, hash it together with your PIN code, and then you get another piece of data. When the user tries to login, you take the PIN that he enters, again you do the hashing with the first piece of random data, and then you can get the second one. If it's correct, then great, you go through. After successful login, you re-generate this random stuff so that on the next round there will be another power consumption trace for checking the PIN code.

After that hack, Trezor developed a nice storage library called Trezor Storage that uses this exact mechanism where they put together all this different PIN code and other secrets available on the device to encrypt your mnemonic phrase.

When you check a PIN code, always increase the PIN counter before you check. The problem is that the device can be reset and the attacker tries again. Always increase the PIN counter before. Also, there's a way to erase certain regions of memory if you shoot it with a laser.  Use a checksum for the PIN counter, like use 01 for 0 and 10 for 1. Even if the memory is erased, you won't see 01 or 10, you will see 00 or 11. So you will see that something is definitely wrong and then you just wipe the device because obviously it's being tampered with.

Do not load private keys to memory until PIN check is passed. Don't load secrets into memory before checking the PIN. You can just use liquid nitrogen to freeze the device, flash new firmware, and then you can read this out.

When you enter the PIN into the device, how can you be sure tihs was your device and it wans't replaced? You need a hardware wallet that tells you its fingerprint and it needs to authenticate aginst you using some protocol. Coldcard after entering a few numbers of the PIN code, you press a button, and Coldcard shows you some words derived from some secret and this PIN code, and if you recognize the words then it's definitely still your device and then you can continue to enter the PIN code. If it doesn't say the right words, then it might be stealing your PIN code and sending it over wifi to an attacker. Think about evil maid attacks. Also, you should look at response time. You should do everything in a Faraday cage vault, which will eliminate some of those communication problems.

It's pretty hard to implement in reality, but in principle you can do challenge-response and measure the response and figure out how far is the real hardware wallet from your host for example. But in practice, it's difficult to do that sort of timing correctly. Maybe we can get to this level in 5 years or so.

## Key storage

I am running out of time. I want to talk about one important thing. When you're storing secrets, you need to be sure that even if your firmware is buggy, then nobody should be able to read it out. If someone glitches your firmware at a certain point, it shouldn't be able to get to the memory region of your private key. This means that you need to first use some kind of memory protection or memory management engine that allows you to make sure that only certain parts of your firmware have access to the secrets. For example, my communication stack might be vulnerable, because I don't know USB is pretty complex, shouldn't be able to get access to secrets. The best way is to actually have a physical separation again. For example, you can have one microcontroller storing the secrets like a secure element, and then another one that is managing trusted peripherals like display and buttons. It can also do image recognition for QR codes and so on. In principle, you can merge them all together into a single microcontroller, but then the problem is setting different permissions for regions of memory and what peripherals they can talk with.

## Conclusion

If you want to play around with hardware wallets, I have a few toys with me and you can talk with me today or tomorrow to check them out.

## See also

<https://diyhpl.us/wiki/transcripts/austin-bitcoin-developers/2019-06-29-hardware-wallets/>

## Q&A

Q: Do you think we'll see an open-source secure element?

A: I don't think we'll see a real open-source secure element. The whole security industry is really caring about certification levels. They give you 3 points if you're closed source. There's an incentive to keep it closed source, just to get some free points. There might be some way to get something open-source and secure with like the RISC-V and open hardware initiative. As a community, we might be able to get this done. It would be nice to see a secure element that even if it is closed source, at least has the functionality for the bitcoin curve and HD key derivation etc. We're working on something like that with Java Card, and we're also talking with Ledger and Trezor and they are thinking in that direction. Another option is what Coldcard is doing, which is using a secure key storage element. It can't do cryptography, but at least it can store the secret there. You might be able to convince the manufactuer to open source the firmware of the key storage, and even if you can't verify it's running there, at least it could be open-sourced.

Q: It's going to be an arms race of hardware security.

A: Well, one option is to have disposable burner wallets that you throw away. Another option is to use heterogenous wallets, like have a hardware wallet with 3 chips from 3 different nations like China, Russia and United States. Or with Schnorr signatures, you can combine these keys together and what's the chances that all three governments will collaborate? They are already collaborating, don't worry.

Q: ...

A: The problem is that secure elements are pretty weak and they can't drive a display or other peripherals. Ideally you want a secure element that stores the secrets and also drives the trusted peripherals so that we can see what the secure element intended us to see. But at the moment it's not really possible. Ledger Nano X is using a secure element driving the trusted display, but there's still a man-in-the-middle in the screen driver.

Sorry, can't take any more questions, so talk to me during the breaks.
