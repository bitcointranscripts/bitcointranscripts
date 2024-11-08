---
title: Taproot on hardware wallets
transcript_by: Michael Folkson
tags:
  - taproot
  - hardware-wallet
speakers:
  - Stepan Snigirev
date: 2022-03-03
media: https://www.youtube.com/watch?v=8uM-v1pSFgs
---
## Intro (Jeff Gallas)

I’m very happy to announce our first speaker for today. It is Stepan Snigirev from Specter, he is the CTO of Specter Solutions and has been working on Bitcoin software and hardware wallets for 3 years now so welcome Stepan.

## Overview (Stepan Snigirev)

What I want to talk about is Taproot on hardware wallets. We recently got the Taproot upgrade, yay, this is awesome. It activated in November. Some of the software wallets started to integrate that and even some of the hardware wallets started integrating it. But they are using a really tiny fraction of the capabilities of Taproot. Right now what everyone is using is a boring single signature, single key approach. I want to talk a bit about what can be done with Taproot. I think everyone knows so I will be pretty fast here. Then I will discuss why it is extremely difficult to implement on the hardware wallet and what exactly is difficult on the hardware wallet. If we don’t get it on the hardware wallet where can we get it?

## Privacy by obscurity

Taproot is awesome. First it gives us privacy. When you see something on the blockchain that looks like a single signature and a single public key what can be inside is a key and a tree of scripts. The key itself can be a collection of keys and the script tree can be also a very deep and complex collection of scripts. Here you can have any kind of timelocks, backup keys that are normally not used and you use them only in case of emergency. This means that all complex policies will look the same on the blockchain and this is huge. Even each of these keys that are inside any of the structure can also be a collection of keys. It is like infinite power of the key aggregation. This is really cool.

## Miniscript (safer plaintext backup)

The first thing that I would personally use this for is better plaintext backups. Why does nobody use Miniscript right now or complex Bitcoin scripts? First because Bitcoin scripts were too complex to write before Miniscript was introduced and second because everyone is not using it. We have a chicken and egg problem where everyone is using either single sig (90 percent), multisig (10 percent) and only 0.3 percent is using anything custom. If you are using some custom scripts then you expose yourself in this 0.3 percent. All chain analysis companies know that if this script is used this is probably the same guy. This is really bad for privacy and this is one of the barriers.

Policy

`or(HW, and(backup, timelock))`

Descriptor

`tr(HW, {and_v(v:pk(backup), older(timelock))})`

Tapscript

`<backup> OP_CHECKSIGVERIFY <timelock> OP_CHECKSEQUENCEVERIFY`

What I would use personally, I am extremely scared of plaintext recovery phrases that are lying somewhere in my house. If someone breaks into that I will lose all my funds. What I would personally use is a hardware wallet that I don’t backup and I have the backup script where I use a timelock plus the recovery phrase. Then if I screw up and my hardware wallet is broken I need to wait for maybe half a year but then I get my funds back. But if my recovery phrase is compromised then they will not be able to steal my funds while I have the hardware wallet. I have enough time to migrate to a new setup. If you are thinking about the hardware wallet and the Miniscript implementation none of them are really supporting it yet. Too bad. But it is not actually very difficult. When I was integrating Miniscript in our hardware wallet it basically took me one week. I sat and wrote the thing because it is extremely well documented. There are two components. One of them you can just ignore. One of them is when you have a policy that is human readable that you convert to the descriptor. It is kind of complex but you don’t need to do it on the hardware wallet. The second part is when you compile the descriptor to actual Bitcoin Script. This is pretty much just a replacement of these operators to the OP operators in Bitcoin Script and placing the derived keys in the right spot. It is pretty easy. Then the hardware wallet will be able to determine which output is the change so it can verify that the change output is derived from the same descriptor and then you are good. I want to mention that Ledger recently did a lot of [work](https://blog.ledger.com/miniscript-is-coming/) in upgrading their Bitcoin application. They took this Miniscript approach while designing it. Even though right now it only supports multisig it is pretty easy to upgrade it to support custom Miniscripts so I’m looking forward to that. Regarding hardware wallets I don’t know about their plans. But at least there will be two hardware wallets that support that.

## xpub for interactive multisig

`xpub = {c, P}`

`{c, P} = {h1(c, P, i) , P + h2(c, P, i)}`

Another use case is let’s say you are running a collaborative custody company. You want to give the users the ability to use your key in their multisig setup. For example they have a 2-of-3 multisig where 2 keys are controlled by them and 1 key controlled by the company. You don’t want to rely on a single point of failure for your keys, you want to give the user one key but you don’t want to have actually one key. What you can do is have an interactive multisig. Here you need to combine them in such a way that you can give the user a single xpub. It is actually possible of how BIP32 and xpub derivation works. It just tweaks your public key with a certain hash based scalar. It is doable if you combine the keys in advance. When you are constructing this xpub you take the chaincode, you XOR them, you combine the public keys with a normal MuSig or whatever you use and then when you need to derive a new child key you just use this aggregated chaincode and public key to derive the next keys. You will be able to sign it interactively between your devices. These are awesome applications.

## Taproot is hard - interactive multisig zoo

But they are relying on this interactive multisig that I said a few times. If you look at the papers, how many approaches there are to build interactive multisig, there are at least 5 (MuSig, MuSig2, FROST, MuSig-DN, GKMN21), these are the 5 that I know of. This means that each of them introduces a certain trade-off. There are security problems in each of them. I want to talk a bit about all of them and why they are hard. I should remind you of the Schnorr signature.

Schnorr signature

Pick a nonce `r`, `R = rG`

```
sig = {R, d.hash(P, R, m) +r}
                    xG
           P. hash(P, R, m) + R
```

Aggregated signature
```
P = sum of a_k P_k
R = sum of R_k = sum of r_k. G
sig_k = {R, a_k.d_k . hash(P, R, m) + r_k}
sig = {R, d.hash(P, R, m) + r}
                xG
           P.hash(P, R, m) + R
```

If you want to sign you pick a random nonce, you hash the public point of the nonce together with the public key and the message, and then multiply it by your private key and add this random nonce that hides your private key in the signature such that no one can calculate your private key. Then the verifier can just take a signature, multiply it by the generator point and verify that the equation still holds. If you are trying to do it in the multisignature setting you have the same but with a few problems. First here we have the nonce in the hash and each of the co-signers need to generate their own nonces. The first requirement is that they all should communicate to each other and say what nonce they are using. Only after that when you have aggregated the nonce they can generate their shares of the signature. Then the software wallet for example can just add them together and you get the final signature. The scheme is also not super complicated. You just need to have an additional round where you coordinate the nonce.

Why are there so many papers? The first one is MuSig, probably the first one that was introduced. It relies on the key aggregation in the n-of-n setting. You have either 2-of-2, 3-of-3, 5-of-5, you cannot do 2-of-3 or 3-of-5. It will require 3 rounds. The first round is when you pick the nonce (`R_i = r_i.G`), you hash it (`hash(R_i)`) and send to everyone else. This is basically a commitment to the nonce. You say “This is the hash of the nonce, I commit to it, I will use this exact nonce, I cannot change the nonce anymore”. Then you send the nonce (`R_i`) itself and you get all the nonces from other co-signers (`R = sum of R_i`). You verify that they used what they committed to. And only after that you generate your own signature (`sig_i`) and aggregate. Three rounds is terrible. Let’s say you have multiple hardware wallets distributed across different geographical locations. Then you need to run around 3 times across all of them. While doing that they also need to maintain the state here. They still need to remember about all the commitments and stuff like that. This is not how current hardware wallets work. They try to be stateless, they try to not be interactive.

```
R’_i = r’_i x G, R’’_i = r’’_i x G
R’_i, R’’_i
R = sum of (R’_i + b_i.R’’_i)
sig_i
```

Then there was MuSig2, this is an upgrade of MuSig, where you remove this first round of commitments but instead of that you generate not a single nonce but you generate two nonces. Then you share this nonce with everyone else, you combine it with some hash based coefficient, I don’t want to go into details but this way it is secure under certain assumptions. If you want to make it even more secure you generate 4 nonces. This relates to some funky cryptographic things like the Forking Lemma and time machines and whatnot. I recommend you read the paper if you want to get into the details. Basically generating one extra nonce makes everything secure and then you have two rounds. Two rounds is already much better. What you can do is generate the nonces in advance. You can gather 100 nonces from each of the hardware wallets and then you just use them when you need to sign. Then you need to run through all your hardware wallets only once. This again requires the state. The hardware wallet needs to know about the nonces that it generated and it needs to verify that it didn’t reuse the same nonce twice. If you reuse the same nonce then you are screwed. You basically lose your private key.

Then finally FROST. FROST is interesting because it is not focusing on this nonce negotiation. It is focusing more on the key aggregation. It allows you to do 2-of-3, 3-of-5, something like that. The idea there is you use Shamir’s Verifiable Secret Sharing Scheme. If you want to do 2-of-3, if you have 3 private keys that are on the same line then you can derive this combined private key or public key or signature only having 2 of them. Any 2 points of these 3 can help you to reconstruct the final signature. This means that the only problem is how to make sure that the private keys that we generated at random will end up on this line. The main idea of this FROST paper is how to communicate between different signers in such a way that they end up on the same line. It is an interactive scheme but it is very nice because after the first interactive setup you can move them around and you still have 2 rounds. But again all these 3 schemes are relying on the fact that your nonce is never reused. This means that in order to generate fresh nonces you need either a counter or a random number generator. These are two problems especially on the hardware wallet because I can hack the counter, I can hack the random number generator. Let me show how you do this.

Pros - fairly simple to implement, almost non-interactive with 2 rounds

Cons - heavily relies on RNG or counter, requires keeping state

## Taproot is hard - nonce derivation for multisig

The first idea is just use the counter. You have a number that you always increase and never reset, never reuse the same value and you hash it together with your private key to get this nonce.

counter++

`r = hash(d, counter)`

When you use something you increase the counter again. It works perfectly in theory. In theory there are plenty of attacks, for example what the Fraunhofer Institute [did](https://www.aisec.fraunhofer.de/en/FirmwareProtection.html) with unlocking a microcontroller. They just shot a laser into it. If you shoot the laser into the right spot of the flash memory of the microcontroller it will reset. Either it will go to zero or you will flip the bit and it can go down in the counter, it can be reusing the same counter again. Here the problem is as this is the nonce in the signature this means that it will be on the blockchain or it is known by your co-signers and your software wallet. This means that if there is not enough entropy or it is reused then they can recalculate your private key from the signature. With a random number generator there was a very nice [talk](https://www.youtube.com/watch?v=Zuqw0-jZh9Y) at Defcon where they talk about problems of random number generators for 45 minutes. This means that even if you are using a certified (closed source) random number generator it is normally not enough. Most of the talk is about how you can screw up the random number generator yourself as the developer. It doesn’t even touch the problem of hacking the random number generator.

## Taproot is hard - Breaking RNG (Wait for bad RNG output)

So how can you screw up with the random number generator? First it happened in the wild. The Sony Playstation 2 was hacked this way because they reused the same nonce and leaked the private keys so you could homebrew your Playstation 2 with these leaked Sony private keys. Yubikey, when they went through the certification process they got certified but they screwed up with the initialization of the random number generator. You only had to have 3 signatures to reconstruct the private key so there was a huge problem there. Then as I mentioned in this [talk](https://www.youtube.com/watch?v=Zuqw0-jZh9Y) they analyzed the output of two random number generators from different microcontrollers. What they saw, sometimes you accidentally get a bunch of zeros, your nonce is zero, that is bad. Then sometimes it repeats the same value multiple times because you are asking for random numbers too often. It just wasn’t able to generate a new random number. And also sometimes the RNG fails because there is a voltage glitch or for some mysterious reason the sun heats the microcontroller and something happens. By the way this can also happen with the counter. You will be very, very unfortunate if this happens with your hardware wallet that uses the counter. This is how you can shoot yourself in the foot.

## Taproot is hard - Breaking RNG (Influence RNG operation)

Now let’s say someone else wants to shoot you in the foot. How can you do this? This is the most common random number generator architecture, a ring oscillator. Basically because it is using standard NOT gates that can be easily done in the semiconductor. You have a NOT gate that converts `0` to `1` and `1` to `0`. Then you chain 3 of them one after another such that you get some time delay. Then you feed the output of the third one to the input of the first one. This becomes this ridiculous logic circuit that is constantly switching between `0` and `1` and the timing between the switching is very dependent on the environment, on the manufacturing imperfections, on the impurities of the semiconductor, on all this stuff. This basically gives you a very unpredictable output. To get even more random numbers you take a bunch of these oscillators and XOR them together. Now I am asking you to remember your physics class, high school or elementary school. What happens if you have multiple pendulums on a rod? On the rod everything is fine, they are oscillating with their own frequencies, but what if you put it on a rope that can transfer energy from one pendulum to another one? Then after some time it will synchronize. Google it on YouTube and see how it works in action. The problem is if you have a bunch of oscillators that are coupled together they will eventually synchronize and then your random output will be not random anymore. In the certified, good, well designed random number generator there are some countermeasures and they check the output is fine. What happens if you just put your microcontroller on the PCB board that is poorly designed that has a trace going through all of them? It can introduce this coupling. If there is an attack, like an evil maid attack, that takes your device, disassembles it, puts some wire there, it also can introduce the coupling and then you are screwed. Other types of random number generators are also not perfect. If you are using something that is dependent on the temperature you can freeze them. Also you can lower the supply voltage of the random number generator and it will output `0`s more often than `1`s or do some weird stuff. Weird stuff is where low entropy is. You don’t have enough entropy, your nonce is brute forceable and then you are done. Also all kinds of fault injections where I can just take an electromagnetic meter and force all these oscillators or the random number generator to malfunction. So a random number generator is bad or at least not perfect.

## Taproot is hard (interactive multisig zoo) cont.

Is there a solution? You saw that there are 5 papers. In the second column there are 2 papers that don’t require a random number generator. They use deterministic nonces and not just deterministic nonces, they use verifiable deterministic nonces. This means that your hardware wallet or your signer can generate the nonce and prove to everyone else that it was generated deterministically using a particular algorithm. [MuSig-DN](https://eprint.iacr.org/2020/1057.pdf) is MuSig deterministic nonces. [GKMN21](https://eprint.iacr.org/2021/1055.pdf) (Garillot, Kondi, Mohassel, Nikolaenko) is something from Facebook. They actually published this paper but it is a very nice one. It looks like a very good solution. The only problem is that generating these proofs, that you generated the nonce deterministically, is pretty complex. For example in MuSig-DN the benchmark says that if you are running it on a Intercore I7 3GHz, like a normal computer, it will generate 1 second to generate the proof. If we think about hardware wallets that are 100MHz, they are also 32 bit not 64 bit, you can easily get a factor of 100.

## Interactive multisig comparison

Here is the comparison. The first 3 guys (MuSig, MuSig2, FROST) are relying on RNG so we don’t care about the benchmarks, it is fast. But the last two guys (MuSig-DN, GKMN21), MuSig-DN on the microcontroller it will probably take 100 seconds. If you have a 5 input transaction you will need to wait for 10 minutes, not great. Also the memory requirements are pretty high. I think it can be optimized but still 10MB is not what you have on the microcontroller. There you normally have 100KB, something around this. Maybe megabytes you can get on the high end ones. Keystone for example that is Android based can have plenty of memory but they are running the secure code on the secure element that is also not very performant. And the proof size is ok, 1KB. I am a QR code guy so I don’t like transferring 1KB over QR codes, that will be complicated but ok fine. Then finally the second paper (GKMN21). It uses a different zero knowledge proof so it is much faster and on the microcontroller it can actually run. On the memory I am not sure but I think it is also using a few megabytes. The proof size is 1MB. So it is like a whole block of the Bitcoin blockchain is just a proof that you generated the nonce properly. But you don’t need to broadcast it so just internally transferred from one signer to another. This is the summary of all multisignature schemes. All of them have certain trade-offs. I would say if you are using multiple hardware wallets that you don’t want to connect at the same time to the same computer, you for example have them distributed, then don’t use interactive multisig. Use just normal multisig until we get some reasonable MuSig implementation. But there are plenty of use cases where it is extremely useful.

## Taproot - Where can we use it now?

For example Lightning, completely different security model, your keys are always online anyway. You need to keep the state anyway. It doesn’t increase your attack surface if you start using MuSig. Lightning, good. Then atomic swaps, here also you probably have it on the hot wallet so very similar situation. So also fine. Then for services where you have a server that is one of the signers. For example Blockstream Green uses 2-of-2 or 1-of-2 plus timelock. This can be really optimized for Taproot. Muun wallet is using 2-of-2, the guys at Square are doing something funny with a server, mobile wallet and secure key storage. These are very good use cases. And finally my favorite, my dream, my passion, my precious, I am dreaming about this for 3 years but never had time to implement. A paranoid HSM where you combine multiple chips in the same device. You take RISC-V PGA board that is fully open source, you take a secure element under NDA from Infineon for example and you take some other RAM based microcontroller for example. Each of them has a key and each of them needs to sign in order to generate the full signature. Then if the attacker wants to hack this thing he needs to hack 3 different microcontrollers. This is really, really great, especially for HSM enterprise use cases. In the HSM, enterprise you can also cover it in the Faraday cage and have a conductive mesh that detects all the tamper attempts and so on. This is really cool. I think Taproot is awesome. Let’s see how it evolves, it is really nice.

## Q&A

Q - What Lightning wallets can use Taproot multisignature today?

A - I think right now it is not even specified in the specs so I don’t think it is implemented in software yet. I think c-lightning is working in that direction but maybe better to ask Christian Decker who is here. I think it is still in the write a specification step. But in general this would mean all your channel opening and mutual channel close transactions appear on the blockchain as a single signature and single key. Only if you need to do a unilateral close, then you expose the fact that there is a timelock in the Taptree.

Q - Which one of the collaborative multisig schemes do you think is on the path to mainstream adoption? We are in a weird situation when you have 14 standards, we need to create one standard to rule them all and then we have 15 standards.

A - I don’t know which one will be the one that is used by everyone. I personally like MuSig probably and some kind of combination with FROST because it gives you threshold signatures, 2-of-3, something like that. From my understanding FROST will have problems with cross input integration, Sanket mentioned that. I don’t know frankly speaking. I think it makes sense to start looking at MuSig first because this will probably be the first adopted. It might be better to ask someone who is writing libsecp256k1. I don’t have a definite answer.

Q - Are there any hardware wallets that allow you to provide your own entropy for the nonce? If not is there a good reason why not?

A - Before all the Taproot stuff what was discussed in the hardware wallet, Bitcoin community was the verification and mitigations of the chosen nonce attacks, anti side channel thing where the hardware wallet when it is hacked can leak your private key. I know two hardware wallets implemented mixing of additional entropy into their signatures, this is [Jade](https://medium.com/blockstream/anti-exfil-stopping-key-exfiltration-589f02facc2e) and Bitbox. As far as I know no one else implemented that. But this is pretty much for the first step for MuSig. I think we can reuse the same specs and protocol for MuSig coordination as well. I think as soon as other hardware wallets start, if they start implementing MuSig, they will need to have this API for mixing additional entropy.

Q - You mentioned RISC-V. Do you think there is any scope there for custom instructions to try to make this really quick? Basically you have to emulate everything in software implementations.

A - With RISC-V on FPGA? I would recommend to look at [Precursor](https://www.bunniestudios.com/blog/?p=5921) the project from Bunnie, the secure communication device for journalists and stuff that was on crowdfunding. Now they are manufacturing it. The guys are really into hardware, they use FPGA and a RISC-V core on the FPGA so it makes sense to look into that. They also have a OS and stuff and some secure measures. In principle they are also fully open source. What we can do, we can take everything that they did and use for our benefit. I think open source RISC-V cores are evolving fairly quickly and getting more production ready. In this setup for example you don’t need to hit the really production ready state because you also have security by other chips. I think there are also some FPGAs manufactured in China, I don’t know how much you trust China. They are extremely cheap and can run RISC-V in the minimum implementation. Generally with FPGAs if you want RISC-V and reasonable speed you need to pay a premium because FPGAs are more expensive, maybe a few hundred dollars.

