---
title: Secure protocols on BIP taproot
transcript_by: Bryan Bishop
tags:
  - taproot
  - tapscript
  - musig
  - adaptor-signatures
speakers:
  - Jonas Nick
date: 2019-06-06
media: https://www.youtube.com/watch?v=JdvVKRTMwz8
---
36C7 1A37 C9D9 88BD E825 08D9 B1A7 0E4F 8DCD 0366

<https://twitter.com/kanzure/status/1137358557584793600>

<http://diyhpl.us/wiki/transcripts/bitcoin-core-dev-tech/2019-06-06-taproot/>

slides: <https://nickler.ninja/slides/2019-breaking.pdf>

## Introduction

I am going to tlak about something that is a collaboration of many people in the bitcoin community including my colleagues at Blockstream. The bip-taproot proposal was recently posted to the bitcoin-dev mailing list which proposes an improvement for bitcoin.

## Disclaimer

It's not at all certain that a bip-taproot soft-fork will activate in its current form or at all. This all depends on community consensus. So far things are looking good. At Blockstream we're interested in this because it makes many of the things we do cheaper and more fungible, including greenwallet, sidechains and our lightning implementation.

## Taproot

How does bip-taproot work? Assume we have some policy where a coin can be spent by an authorization from a single party with a single key. So the only thing you need to do in order to create a scriptpubkey is you push the number 1 on to the stack which now indicates that this is a witness script with version 1 as opposed to a v0 witness program which is already defined, then you push your public key on to the stack. Things get more interesting with bip-tapscript if you have more complex policies, such as a coin can be spent by an authorization from a key or from some collection of bitcoin scripts.

## Taproot address generation (witness version 1)

The pubkey is called the internal public key. You take your various scripts and build a merkle tree out of it by recursively hashing the leaves and the inner nodes until you arrive at some root. Then you use a construction called pay-to-contract to create the taproot output public key.

## bip-taproot spending

What happens if you want to spend such an output when you see it? There are essentially two ways to spend this. There's the key spend, where you provide a bip-schnorr signature for this public key in the output. Or you do a script spend, and you do that by first showing the script that you have committed to, you show a proof that this script connects to your merkle root, you show that the merkle root is in the output, or the output committed to in the output public key. Also, you provide the inputs to the script in order to satisfy.

The important part is that the only thing that is in the output is- and at which time, you need to decide which spending method you want to use.

## progress

We have been working on libsecp256k1 which was originally written by Pieter Wuille for Bitcoin Core. One of the main ideas behind the library is that it should be difficult to use incorrectly or insecurely. It's fast, mostly portable, and well reviewed because it has been in Bitcoin Core. It's also free of timing sidechannels. There are options for using various bindings to libsecp256k1. One of the interesting bindings is rust-secp256k1. The ingredients to support bip-taproot in your wallet are not merged in libsecp256k1 yet, they are only pull requests.

There's libsecp-zkp with a few advanced schemes like rangeproofs for confidential transactions, surjection proofs, Schnorr signatures, a MuSig scheme, and just this week we released rust bindings to libsepc256k1-zkp so you can use it in a type-safe way. This beta version only supports Schnorr signatures and nothing more but we will change this in the future.

The first thing you need to do is read the documentation in the directories for these C libraries. I am going to talk about some of the pitfalls of using these libraries in a moment.

## libsecp256k1 schnorrsig module

The minimal thing you need to support for bip-taproot is how to make Schnorr signatures. You always see either links to pull requests or modules so that later you can click on my slides and get to these things on the web. A schnorr signature is very similar to an ECDSA signature. A schnorr signature is 64 bytes consisting of two elements, an encoding of a point in 32 bytes, and the other one is just a number. The point is usually called R, and the other value is called s. A nonce is called a nonce because it's a number that is supposed to be used only once. This isn't the problem at all if you just use Schnorr signatures in the regular way where you create a signature. This is the same as ECDSA: your nonce is generated deterministically from the message such that you have a guarantee that if you use a different message then you will use a different nonce. You never have to use a particular nonce. In a discreet log contract or in single Schnorr signatures where you have to commit to a single nonce, you just sign twice becaus eyou will always be using the same nonce.

Schnorr signatures also allow you to do batch verification which means you verify a batch of signatures at once, which is faster than individually verifying them one by one. Using batch verification, if it fails you don't have any information about which one failed. Batch verification may not reduce your worst-case cost because you need to figure out who was dishonest in this protocol. Or maybe the attacker would send a signature such that it wouldn't be in your batch or something like that.

## Covert nonce channel

This is something else we're implementing in libsecp256k1. This is a problem in Schnorr signatures and ECDSA. This is based on an idea from gmaxwell. A problem with hardware wallets right now is that it's possible to exfiltrate a private key through a nonce. Say you have done a bad hardware wallet firmware update, your hardware wallet is now compromised. Generally the only thing that the hardware wallet has to communicate with the rest of the world is a signature. There's a way to put the private key into the signature using the nonce. The general idea of this is that both the hardware wallet and the attacker generate the nonce in a very specific way, except for a few bits that need to be grinded by the attacker. If there's a match between the nonce in the blockchain and the attacker's computation, then the attacker knows a few bits of a nonce. This is an encrypted channel, so nobody else can see it.

The idea in libsecp that we're implementing is that you use a construction called sign-to-contract where you enforce there is some randomness in the nonce. The host computer enforces this. The way this works is that the host draws some randomness, sends a commitment of the randomness to the hardware wallet. The hardware wallet derives their nonce with this randomness, a key, and the message. The hardware wallet uses sign-to-contract to create a special nonce that uses this special randomness. When the host receives a signature, they just need to make sure was my randomness actually included. If not, don't send the signature out to the blockchain and raise an alert.

The alternative is to create a MuSig key aggregation between the hardware wallet and the host but unfortunately this is pretty difficult for hardware wallets to do at the moment.

## Tweak add

If you want to do more interesting things with bip-taproot, you also have to support this other pay-to-contract construction or "tweak add". This takes your internal public key and a merkle root and it computes this taproot output key. So mathematically what this is that if your internal public key is P, it's fairly straightforward, you just add the hash of (prefix, P, root) multiplied by G the generator. You then receive your new taproot output point, Q. In libsecp, this is just a function called \_ec\_pubkey\_tweak\_add. The tweak is the hash. But there's some problems with fungibility...

## Tweak add fungibility

Try avoiding using the script path at all. If you have a multiparty contract, then you should generally try to get all parties to agree on the endstate of the contract and then let everyone sign using key aggregation instead of falling back on this script path. Also, don't reuse keys. Internal keys and leaf keys too. Using the script path basically leaks the wallet, like information about what wallet you use... it reveals at least the minimum depth of the tree, and a script which can have a lot of identifying information in it. Also, you have to make sure you have sufficient leaf entropy so that you always have a different public key in a leaf, otherwise an attacker can bruteforce search your leaf script because there's no randomness otherwise applied to individual leafs.

## Multisignature options with bip-taproot

If you want to use multisig with bip-taproot you have a few options. You could use CHECKDLSADD which is batch verifiable, and CHECKMULTISIG is not. It's a replacement to CHECKMULTISIG. Another thing you can do is key aggregation. This allow syou to encode an n-of-n signing policy in a single public key and a single BIP-schnorr signature. This is more fungible because you never see a script path and it's definitely cheaper because you only have a single public key and a single signature, but the problem is that this is an interactive protocol with multiple parties sending messages in multiple rounds and they need to keep state.

## Key aggregation options

With bip-taproot, there are some papers thta explain how to do some of the key aggregation stuff with ECDSA so you could use p2wpkh for maximum fungibility. But this uses new assumptions and it's hard to implement and hard to avoid timing sidechannel attacks. Also it only has 80 bits of security which might be okay for some use cases, but it's not the 128 bit security we usually want.

You could do MuSig key aggregation, where you aggregate the public keys, and the MuSig coefficient is multiplied in and the index.

Another option is non-musig key aggregation where you add up your individual public keys, then provide a proof-of-knowledge that you know the secret key to this public key in order to avoid key cancelation. But now a single party can add a taproot tweak without it being noticeable and it oculd have a script such that one malicious party on its own could just spend the coin. bip-taproot right now recommends that you could always have a script path, but this script path would be unspendable as a solution.

## Musig protocol

Musig's functions here on this slide are similar to the ones in the implementation. It's three rounds. You initialize your session, and you need a new session ID that you have never used before. You make a nonce commitment and exchange nonce commitments. Once you have all nonce commitments, you get your public nonce. Then all parties exchange those nonces. Once they receive a nonce, they set it and makes sure it matches the commitment and if not then the protocol needs to be avoided. They combine the nonce, then they exchange partial signatures, then they combine partial signatures and now we have a bip-schnorr signature.

Our implementation using libsecp-zkp is safe if you do two things: never reuse a session id (use uniform randomness or an atomic counter that can never be reused), and you must never copy the state otherwise you would have problems with nonce reuse which would leak your private key or you are vulnerable to active attacks.

## MuSig: Reducing communication

Probably your protocol already has existing messages and maybe you can attach your musig protocol messages to that already. You could also run multiple musig sessions in parallel, where oyu have an initialization share where you pre-share nonce commitments and only when there's a message that you want to sign then you exchange partial signatures at that point. You could also have a fixed number of parallel sessions where you get one signature per round, such that a single message roundtrip would also result in a partial signature.

## Using musig with offline or hardware wallets is difficult

When you use a hardware wallet and there's multiple rounds ,your hardware wallet will lose power. So then you need to move the state to some persistent medium. This is a copy operation, and very dangerous because you need to ensure there is only one instance of your state there, ever. Therefore, in our implementation right now we don't really support serializing the state. But remember this is only for signing. For online devices like in lightning, this would be very quick. If you would suddenly shutdown during signing, then you would just start again. You could have a single session and then move it to persistent storage, and ensure there's only a single state, then load it.. but then you would need to travel to your hardware wallet for every single signature and your transaction might require many signatures so it's not really workable in practice.

There's some research into deterministic nonce generation for musig. Here, every party would just generate the nonce similar to how it works in the single-party case by deriving it from public keys and the message. The catch here is that you need to prove that you have done this correctly and you need to verify that everyone else has done this correctly. This would reduce it to two rounds of communication, but you would still want the zero-knowledge proof of nonce derivation to be done efficiently like for a low-power device. This adds code complexity and potentially there's a lot of places for bugs or vulnerabilities here.

## Musig adaptor signatures

Our implementation also supports adaptor signatures. You can do scriptless scripts atomic swaps or scriptless scripts lightning. The gotcha is that you always need to verify partial signatures, which you don't have to do in general.

## Blind schnorr signatures

Blind Schnorr signatures are also enabled by bip-taproot. Blind signatures are an interactive protocol between client and signing server. The signing server doesn't know hte message being signed, but the result is a bip-schnorr signature. The signer returns a blind signature, Alice can unblind the signature, and now she has a signature on the transaction. Unfortunately blind signatures are broken; you can forge this due to Wagner's attack, with only 2^32 work which is very low, and they can't be proven secure in the random oracle model. If you just need blind signatures, like for an ecash scheme, then don't use blind schnorr signatures. There are way better schemes out there that have provable security and many more features. But if you need blind signatures for bitcoin signatures then you're stuck with blind schnorr signatures. There's some ideas for preventing Wagner's attack; one has a 128 communication blow-up, where you use 128 different blinding factors, send all of them to the server, and the server randomly picks one and returns it back to the client.

## Conclusion

bip-taproot is a substantial efficiency and fungibility improvement. Allows a lot of interesting protocols on top of it. There's still simple sending. Mainly you need to somehow create Schnorr signatures, other than that it's very simple. You can use libsecp256k1-zkp for the cryptographi primitives. bip-taproot doesn't change anything in the cryptographic assumptions. There's still the discrete logarithm assumption in place; verification is fast and it's well-studied. The problem though is that this often requires as we have seen, it requires interactive protocols which have challenges of their own, which are at least off-chain challenges but it's still a problem.

We haven't talked about k-of-n threshold signatures.. there's a pull request to libsecp256k1-zkp for this, but we're working out subtle issues with denial of service attacks. Please try to break any of these, and write toy implementations and try to compare them. There's a lot of work to be done in this whole field. Thank you.
