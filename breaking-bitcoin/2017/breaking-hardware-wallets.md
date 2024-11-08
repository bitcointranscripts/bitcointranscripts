---
title: Breaking Hardware Wallets
transcript_by: Bryan Bishop
tags:
  - security-problems
  - hardware-wallet
speakers:
  - Nicolas Bacca
date: 2017-09-09
media: https://www.youtube.com/watch?v=eCE2OzKIab8&t=6h42m30s
---
Breaking hardware wallets: Tales from the trenches and glimpses into the future

<https://twitter.com/kanzure/status/1005627960160849920>

Hello. Nobody cares? Ah. So next up is Nicolas. And he will talk about hardware attacks. Thank you.

## Introduction

Hi everybody. Thanks for making a great conference so far. I am Nicolas from Ledger hardware wallet. Today I am going to be talking about breaking hardware wallets. I don't mean physically breaking them. If you expected to come steal a hardware wallet and be able to break it, then you will be disappointed. But if you want to learn some basics about hardware attacks, then you might learn something.

## Hardware wallet

First a small reminder: if you don't know what a hardware wallet is; it's necessary because we don't expect user PCs to be safe or secure. Here you have a representation of a user PC. It's not taken care of. It can be attacked by trolls who want to just destroy your data or make you lose bitcoin because they don't like bitcoin for whatever reason. Or by actual attackers who want to steal your bitcoin. Your hardware wallet should protect you from both.

The hardware wallet will use private keys, it should be able to show you something on a trusted screen, and it should help you make an educated decision, and not totally fail you when you want to send bitcoin to an address.

## Threats

We want to protect the user against malware. It's the biggest risk. We want to protect the private keys, the most critical asset. We want you to validate the operation being performed in a trusted environment. You want to validate the address and amount. Hardware wallet should protect you as much as possible against physical theft. The attacker shouldn't be able to walk away with your wallet and get some crypto. It should also protect you against bad cryptography. Good cryptography is difficult to write. In open-source software there's famous software that has had terrible cryptography. You should have the wallet run the RNG or PRNG and should have proper entropy. Also, there should be sidechannel resistance. By observing the behavior or the electrical behavior of the wallet, you should not be able to deduce information about the keys getting processed.

## Types of attacks

So how are you going to break hardware, supposing you want to break hardware? I found this in the ARM trustzone security guidelines for some terminology. There's hack atthack, shack attack, and lab attack. Hack attacks are where the wallet is attacked by software. Shack attack is where the hardware wallet is attacked by low-budget hardware attacker. This attack is called shack attack because the attacker is not meant to be extremely organized, and maybe he's buying hardware from Radio Shack which doesn't exist anymore-- so for French people, it would be Dondi, which doesn't exist anymore either. So you get the idea. A student, basically. And then there are lab attacks where the attacker can be a professional attacker breaking hardware as a business or maybe a government agency or someone with unlimited time or resources. This is close to impossible to protet against.

## Software attacks

Software attacks are not really specific when discussing hardware... they are exactly the same attacks as you would see in software, the difference is that they run inside the hardware. On the early version of the trezor firmware, which was fixed quickly and it had good response from the community... so, I think in one of those attacks you had a buffer overflow, and another one you had a timer problem. You have the repository if you want to check that one. I didn't describe it here because someone is going to have a talk about it. There was a similar attack in an earlier protocol. If you can change the curve paramater, then you can manipulate the computation into retrieving the key. Don't let people change your curve parameters.

## Shack attacks

In passive shack attacks, attackers are able to obtain information from something observed, like timing variation of the device. There are simple SPA and DPA. These are non-invasive non-detectable attacks. If you leak private information in a sidechannel then this could be recovered. In the end this is mostly a matter of software implementation. We would like to get code from Bitcoin Core and libsecp256k1 and constant-time AES implementations. These are very good references in the open-source community. If you are going to run these algorithms on a chip then you should make sure you are not leaking information that is specific to the chip itself.

## Fault injection

And then for injection, which looks a little bit like black magic... so the main idea behind fault injection is that by performing variation of something on the chip like the clock or the power provided to the chip or an electromagnetic variation or something or pointing a laser at the chip then you are going to change the way that the chip will behave. This doesn't mean that you are going to make the chip run something by flashing it with a laser. It's a very complex and statistical pattern where you mutate something in the data or the instruction set. This type of attack takes a lot of time. You can use this to bypass some critical paths or checks of the security of an implementation.

## Lab attacks

Finally, in lab attacks... when we are dealing with such attackers, we can suppose they will be able to break apart the chip, use electron microscopes or other hardware to break open the chip and get anything. If you have someone extremely motivated and wants to extract something from a chip, then you are screwed. So how do we avoid those situations? It's better to avoid that situation rather than resist that type of attacker.

## hardware wallet expectations

What do we expect from a hardware wallet? We don't want it to leak secrets. We must resist simple attacks. They must resist various passive attacks. If someone finds a hardware wallet on the table, then it shouldn't leak secrets. The idea is that we have to define what "very little time" means but let's say that after one day you have enough time to migrate your keys to some other hardware or some other software. If people can break your hardware wallet within 30 seconds while it's on your table, then that's not good and it should be fixed.

## Hardware wallet architecture

If we look at the hardware wallet chain of trust, you have a bootloader, you have firmware, which gets verified and it reflashes the firmware, and it does the same thing for applications if the hardware wallet supports multiple applications. This chain of trust is critical to the hardware wallet. Otherwise you could run untrusted code and change hte behavior of the hardware wallet itself. As an example, as always, a deal between security and convenience. If you want to put information about the user into the wallet, then you are making a decision between convenience and security. The wallet runs a vulnerable scenario where rogue firmware could dump vulnerable user information. If you dump the data before reflashing then you don't have to fear that, but it's inconvenient. In the end, user convenience wins. You have to think about the possible risk when you work on the product.

## Patchability

When you look at threat levels prepared to patchability. At the bottom, there's software attacks, which you can usually patch against with new software or firmware. With a shack attack, it's patchable in some cases, you can issue new firmware that fixes that isutation. Finally, we're probably looking at the attacks today-- we're not protecting against sophisticated shack attacks exploiting the chip itself. There's a core security mechanism of the chip which could be visible by an attacker.. if you end up in this situation then you have something non-patchable which you can't patch a chip. So you either deal with it or change the chip.

## Trezor

If we want to compare the architecture of different products... bitlox, keepkey, trezor. The easiest one, the most common way is to have a simple chip that executes the logic and connects the chip to the different inputs and outputs of the hardware wallet. It's an architecture used by bitlox, keepkey and trezor. It's fully auditability up to the chip proprietary security mechanisms because no chip is open-source today. One thing about this architecture is that you can't see who issued the chip, because they are all common generic components, and anyone can flash whatever into the chip, and verifying the chain of trust is very difficult.

## Opendime

You can have an architecture with a generic MCU and a chip dedicated to cryptographic functions. This architecture is not common today, it's used by digital bitbox and opendime. That chip holding the secret value will offer better value than a single chip. There's still no proof of origin and there's more exotic architecture. We lack data about how exploitable this can be.

## Ledger hardware wallet

You can use a secure element, like CoolWallet, Ledger hardware wallets, Feitian... Feitian is a Chinese secure lemons company entering the hardware wallet. There's a genreic MCU that acts as a proxy, then a secure element that processes business logic, and the MCU communicates with the screen. The cons are that there's limited auditability. The upside is that there's proof of origin.

## Other architecture

You can use secure MCUs which are quite new. I haven't seen an architecture using that in the field so far. I have seen one proposed called Second Lot... running on the NXP connectux platform I think. It offers auditability. Cons, no proof of origin. It's not developed so far. It's something promising.

So that's about hardware. Are there easier ways to break hardware wallets? Attacking hardware is interesting but hard.

## Hardware impersonation

The first thing is that I'm not going to talk long about, we could have a full conference about it-- if you want to impersonate the hardware, it's quite easy. If you're out at a conference and someone gives you some hardware in a swag bag, you don't really konw what this hardware is doing. You could have something sitting between the real thing and the screen and buttons and basically taking inputs just referring to different functionality. If you want to protect against this, just reflashing everything is not enough. You need to be able to have validation of the hardware. So maybe you just need to look at it yourself. That's good, but not really practical if you want worldwide adoption of hardware wallets. So we have to make some balance here between security, convenience, usability. This could be a great topic for the panel, but I don't have a perfect solution for that.

## Attacking the user experience

You can also attack the hardware wallet from the user experience angle, which is really easy. Starting with something really simple, just attacking the payment address is trivial because bip70 payment protocol is not extremely popular in bitcoin. If you are using your hardware wallet, reading an address from a webpage.. you have no proof that the address was generated by the webpage that you just browsed. There's no real solution against this other than asking users to validate addresses on a second channel. This is a great topic for usability vs security.

## Address and payment attacks

And then confusing forks... we had an example with bcash. If you heard about it, it's a fork of bitcoin which rotates the logo by 15 degrees I think. One problem is that it uses the same address format. So it's extremely confusing. It has a different signature algorithm for transactions. Let's say some service interacts with the hardware wallet and tricks you into interacting with the other chain then this service could obtain information about the other chain which is bad for privacy or make you sign on the other chain which is bad because you can lose money. This is a bad issue if you want to support forks with the hardware wallet because it makes the UX extremely confusing. And it goes against the main principle of hardware wallets, which is supposed to make things easier for users. Forks really complicate things with hardware wallets.

## Change UTXOs

If we want to be even more creative, and again that's a UI problem... today people don't really understand anything about change in bitcoin. I don't mean people in this room. I mean change addresses. Users want to see something on the screen saying okay I am sending money to that address, I don't care if half of my money is coming back to an address that comes back to me. But the products are hiding this information from users. But how could they verify that the change is actually going back to their address under bip32 or something? To recover it, you would have to explore your bip32 tree of addresses, which is quite complex. So we could think about some very imaginative ways of where people send change to a random path and then charge you to recover your money, because you don't know the bip32 child derivation path. There's a lot easier ways to steal money from people, of course. But it would be another way to do a ransom attack (bip32 ransom attack).

## Bundling with other hardware

One of the problems of hardware wallets today is that you have to buy hardware wallets. You could offer hardware wallets on existing hardware. On modern CPUs, you don't have isolation. You have the same issues and it's not a silver bullet. Your algorithms can be ameniable to the same attacks. You have to make sure you don't leak information, which I think is the topic of another talk. And also, you don't have a lot of resistance against physical attacks, such as people having physical access to your PC. It's not a great solution, but it's convenient.

## Attestation

Other things to look at, for where we want to go with this technology-- we need a trusted display and user input/output. This is often seen as an optional feature so it's not always available for users. You can protect your key, but you don't know what you're interacting with. The most critical issue is the different trust model. You could use attestation features inside of your protocol itself to "enhance" the security of the blockchain with trusted features (POET, Coco, ...) like proof of elapsed time and Coco from Microsoft. Unfortunately this relies completely on the security of the hardware. Another option is to use attestation features to use them only once. You could let the user verifies that the platform is genuine and then you are back to the original step where you can run things on this code and enjoy the security features brought by the hardware you verified- you verify the code is running, and then that' sit. I'm trying to push people towards those solutions.

## Moxie + SGX

I want to introduce, and of course the name of the confernece is breaking bitcoin, and something broke on my end. We'll see what you can do with this... it's a project running on SGX.

<https://github.com/LedgerHQ/bolos-enclave-catchme>

It's a simple library using libsecp256k1 for ECC cryptography.. and moxie virtual CPUs, well integrated with the GNU toolchain. This repository is delayed because of CVE-2017-5691. Everything can be validated and recompiled by the user. I wanted to start a bounty on this, and then I noticed CVE-2017-5691, which was rated critical and saying people can extract information from SGX. Otherwise, I thought it was an interesting idea. Follow this thing and see what happens over the next few months.

## Conclusion

To finish, I would say, you might have noticed that you have some hardware in your swag bag. You can try to break it, try to play with it. Tell me what you think about it. Now it's time for questions.
