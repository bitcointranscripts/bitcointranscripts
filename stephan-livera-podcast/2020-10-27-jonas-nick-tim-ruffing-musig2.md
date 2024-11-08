---
title: MuSig, MuSig-DN and MuSig2
transcript_by: Michael Folkson
speakers:
  - Jonas Nick
  - Tim Ruffing
tags:
  - musig
date: 2020-10-27
media: https://stephanlivera.com/episode/222/
---
Tim Ruffing on Schnorr multisig at London Bitcoin Devs: https://diyhpl.us/wiki/transcripts/london-bitcoin-devs/2020-06-17-tim-ruffing-schnorr-multisig/

MuSig paper: https://eprint.iacr.org/2018/068.pdf

MuSig blog post: https://blockstream.com/2019/02/18/en-musig-a-new-multisignature-standard/

Insecure shortcuts in MuSig: https://medium.com/blockstream/insecure-shortcuts-in-musig-2ad0d38a97da

MuSig-DN paper: https://eprint.iacr.org/2020/1057.pdf

MuSig-DN blog post: https://medium.com/blockstream/musig-dn-schnorr-multisignatures-with-verifiably-deterministic-nonces-27424b5df9d6

MuSig2 paper: https://eprint.iacr.org/2020/1261.pdf

MuSig2 blog post: https://medium.com/blockstream/musig2-simple-two-round-schnorr-multisignatures-bf9582e99295

Transcript completed by: Stephan Livera Edited by: Michael Folkson

## Intro

Stephan Livera (SL): Jonas and Tim, welcome to the show.

Jonas Nick (JN): Hello.

Tim Ruffing (TR): Hey.

SL: So thanks guys for joining me today. I was very interested to chat about some of your recent work with MuSig2. Firstly let’s hear a little bit about each of you. So Jonas, do you want to start by telling us about yourself and how you got into doing cryptography?

JN: So I’m working at the research group at Blockstream. I work on [libsecp](https://github.com/bitcoin-core/secp256k1) the library of Bitcoin Core. I work on a few of these cryptography things, but mostly just because I want to implement them in a way that minimizes resistance so developers can use it without the possibility of making huge mistakes. What else do I do at Blockstream? I’ve been working on Liquid and researching scriptless scripts. These are mostly my responsibilities.

SL: And Tim let’s hear a little bit from you.

TR: My name is Tim Ruffing. I’m in Germany like Jonas is. I got into cryptography in the traditional academic way. I did my PhD in the particular cryptography in Bitcoin at Saarland University. The title of my [dissertation](https://publikationen.sulb.uni-saarland.de/bitstream/20.500.11880/29102/1/ruffing2019.pdf) was “Cryptography For Bitcoin and Friends”. During that time I mostly worked on privacy in Bitcoin and now that I’m in the research team at Blockstream I work a lot on signatures in particular, all the stuff you’re hopefully going to talk about today like MuSig, multisignature, threshold signatures, basically everything that’s related to Schnorr signatures.

## The Taproot soft fork

SL: So the context for today. We’ve got this coming soft fork that basically everyone wants in Bitcoin, the Schnorr or colloquially the Taproot soft fork. What’s the relation between Schnorr, Taproot and then MuSig and multisignature. Perhaps Jonas, if you want to just set the context for us.

JN: So Taproot is this new witness program version that we will have hopefully after the activation. So instead of having a SegWit v0 output you will have a SegWit v1 output. What this means is that now you have different ways of spending this coin and one of these ways is to provide a Schnorr signature. This is how BIP-Schnorr (BIP 340) relates to BIP-Taproot (BIP 341). This is an upgrade to how this works right now with ECDSA signatures because Schnorr signatures are a little bit simpler and allow a few more applications on top of that. MuSig is the idea of making multisignatures compact in Bitcoin. Right now in Bitcoin you have this CHECKMULTISIG opcode but calling this a multisignature is perhaps a little bit of a stretch because it’s not really compact. You just write down all the public keys and all the signatures and then you verify them one by one. What you really want is that this is all efficient, you have a single signature and a single public key but your policy is still a multisignature. This is the idea behind MuSig for Schnorr signatures.

## Multisignature and threshold signatures

SL: To spell that out for listeners who might not be familiar. Current day multisignature relies on using Bitcoin scripting. Let’s say we’re doing a 2-of-3 multisignature output. Then we have to actually show two signatures. In the Taproot world we’ll be moving to a Taproot key path spend where we can construct a multisignature, let’s say between the three of us, and onchain you can only see one signature.

JN: Yes. Although I think it would make sense to already start differentiating between multisignatures and threshold signatures. With MuSig you can do multisignatures, meaning m-of-m or n-of-n. You need as many signatures as you have public keys. This would be something that can be done with MuSig. With Taproot, you can still use the old way of doing threshold signatures where you just write down in the chain the signatures and the public keys.

SL: That’s the difference between doing 2-of-3 versus having it such that you must do 3-of-3?

TR: Yeah. I think that is an important difference in the terminology. When you talk to a Bitcoiner and say multisig they usually think about this m-of-n where m can be smaller than n, for example 2-of-3. If you look at academic literature what they call a multisignature is restricted to this n-of-n case where you need the full number of signers. The other thing as Jonas mentioned is called threshold signatures. We are also working on this but MuSig so far only supports this n-of-n case where the numbers are equal.

SL: That’s the difference between threshold signatures and multisignature when we’re talking in the academic context. Perhaps you could outline this journey, there are different forms of MuSig. There’s MuSig1, MuSig-DN and MuSig2. Could you spell out for us what are the differences between those different types?

## History of MuSig

JN: Tim, you’re the expert on the history of MuSig.

TR: Let’s go a step back and see what was there before MuSig because there’s an interesting story to tell there. One of the main reasons to get Schnorr signatures into Bitcoin is you can build a lot of things easier with Schnorr signatures than with ECDSA. For example, multisignature and threshold signatures and other advanced types of signatures, scriptless scripts, things like that. So all of these are somewhat nicer with Schnorr signatures because the math around Schnorr signatures is easier. Some years ago people like Andrew Poelstra, Pieter Wuille, Greg Maxwell thought about doing multisignatures with Schnorr. They came up with a scheme and their main challenge was to avoid an attack called rogue key attack, others call it key cancellation attack. Let’s say we do a 3-of-3 among us here. I publish my public key and Stephan publishes his key. Jonas is the attacker, he looks at our keys and chooses his key depending on our keys. If we do this in a naive way then the resulting key, the multisignature key that should represent all of us would actually only represent him. So Jonas could sign alone with this key which is totally not the goal of multisignatures of course. This is really just cancellation. If we add up the keys and Jonas chose the key in a pretty way then our keys just subtract out again, they’re gone. He could sign alone. Of course it’s not what we want. So those people thought they had a solution to to this problem. What they came up with was really a solution for that problem but it had another issue too. This issue is Wagner’s attack. Maybe we will come to that later. I don’t want to go into the details of this now because then the story will be even longer. They tried to publish, tried to write this up in a paper and publish it. Then people pointed them to existing work in the literature that didn’t solve this problem but solved the other problem, Wagner’s attack. The story continued. They got together with the co-author, Yannick Seurin from France who is a brilliant cryptographer I’d say. He was happy to have them write up  a scheme that is basically the combination of the two worlds that solve both problems. This was the old version of MuSig1. When I say old version, I mean like an insecure version, because even they screwed up again. In this other work they pointed to, this paper by Bellare and Neven (2006). For multisignatures you need an interactive signing procedure. All the signers need to talk to each other when they generate the signature. The process in this paper had three rounds. They needed to send three messages to each other. Yannick (Seurin) had the idea of improving that to two rounds. Unfortunately this idea was flawed. So we had to revert back to three rounds and this is MuSig1 which avoids the key cancellation attack.

## MuSig interactivity

SL: Can we unpack the idea of interactivity? So as I understand multisignatures or threshold signatures today is non-interactive. The three of us can put in a xpub each and create this multisignature. What is the interactivity part in the MuSig context?

JN: There is still a little bit of interactivity because your signing device needs to get the message, the transaction to sign, and then it replies with a signature. You could say that’s a one round signature scheme. With this secure version of MuSig, MuSig1, we have three communication rounds and this has two problems. One, the communication rounds add up. If you have a protocol that uses this, for example Lightning, we figured out that if you use MuSig instead of regular signatures then you would have to add half of a round trip without eltoo. This would be a problem because this half round trip adds up on every hop. We know that Lightning nodes are connected through Tor sometimes. This could really add some latency. Another problem would be if you have a setup with multiple signing devices and one of them you have in a safety deposit box. Either you take all your devices, bring them to the same location and do this whole signing ritual or you have to go two times to your safety deposit box. This would also be a problem I suppose. This is really the problem with interactivity.

SL: Putting that into an example. Let’s say you have three different hardware wallet devices and one coordinating laptop or machine with Bitcoin Core or Specter or something. In that example you would have to go to each hardware wallet location, get the signature, come back, go to hardware wallet two, come back and do a few rounds of that. That obviously is not very practical. Could you outline the difference in terms of setup of creating that multisignature quorum versus signing a transaction for that quorum? Is there a difference there or is it still three rounds?

TR: If you talk about setup for MuSig restricted to the case of n-of-n multisignatures. One big advantage of MuSig in general is that the setup itself is still non-interactive in the sense that you can take any public keys and combine them into an aggregate public key. Everybody can do this. If I know the pubkeys of you two guys, I could now immediately send to a 2-of-2 of you without even talking to you again. There is a difference when we move to threshold signatures. If we in the future want extend MuSig to support m-of-n threshold signatures then this would be inherently different. There we really need an interactive setup. When it comes to threshold signatures the tricks we usually play to make that work is everybody creates a secret key and then shares part of that secret key with the other people. This sharing process needs to happen before we can use the signature scheme. This is inherently interactive. In a funny sense the naive thing that works on Bitcoin today with scripts is still better in that respect because it’s always non-interactive.

SL: In terms of that process you mentioned, is that the nonce commitment part? Maybe you want to explain what that part is for us.

JN: Just to elaborate on another problem with MuSig1, you need to keep state securely. This is kind of an abstract problem if you are not an engineer. Many people would perhaps be familiar that it’s not really possible to backup Lightning channels. This is a similar problem. If you start a signing session, you backup the state because you write it on disk and then you back it up. You finish the signing session, you restore the backup and you sign again with the same session. Then you have reused your nonce and you’re not supposed to reuse your nonce with a different signature. Someone can easily compute your secret key. This is the other problem with MuSig1. That makes it difficult. One of our goals is to write libraries and implementations. Our implementation of MuSig1, we have this huge documentation. You are not supposed to copy this state or write it somewhere. Keep it on memory and you have to pay attention to this and that. No one reads these things. That makes it really dangerous.

SL: What was the approach going forward from that? Was it we’re just going to have to mitigate this and have all the application developers be really mindful of it before they use MuSig1? Or was it more now we need to find other approaches?

JN: Basically yes because there was also this [paper](https://eprint.iacr.org/2018/417.pdf) called “On the security of two round multisignatures.” They showed that you cannot prove two round MuSig1 is secure. There is no way to do it in any model that we care about. So we didn’t try then.

TR: It’s broken. They showed that you can’t prove it’s secure but it’s also because it’s just insecure. We are talking about the old version of MuSig1 though. That’s what Jonas is referring to with two round MuSig1.

JN: But they didn’t prove that you cannot prove another scheme is secure. Then we started looking into these other schemes like MuSig-DN and MuSig2.

TR: I think this is where it really started with MuSig-DN then.

## MuSig-DN

MuSig-DN paper: https://eprint.iacr.org/2020/1057.pdf

Bitcoin StackExchange comparing MuSig-DN to MuSig1: https://bitcoin.stackexchange.com/questions/98845/which-musig-scheme-is-optimal-classic-musig-or-this-new-musig-dn-scheme

SL: So let’s get into MuSig-DN. What is that?

TR: MuSig-DN, the DN spells out Deterministic Nonces which is a very technical term. It really relates to what Jonas was saying, you can’t reuse states. You have to use store the state between the rounds of your signing procedure in a secure way. In particular you have to make sure it can’t be rolled back. For example, if you run your wallet in a virtual machine, for whatever reason, then you can reset this virtual machine, this would be really bad. A very related problem to this is that of choosing nonces in a secure manner. What’s a nonce? A nonce is a number used once. These nonces are required when you create signatures. Not only Schnorr signatures also ECDSA signatures. They have very specific requirements about being random. They need to be, it sounds weird, very random. You can’t have a small bias in this nonce. The worst thing that can happen is if you reuse your nonce. Say you have a random number generator that is supposed to generate these random nonces. For some reason it outputs the same nonce twice which is astronomically unlikely. If it’s broken, maybe a test of this flow, it would output the same number twice. If you use the same nonce to sign different messages then people can just look at the resulting two signatures and compute your secret key. It’s catastrophic, it’s totally game over. This is the worst case that can happen. Even if there’s a slight bias in choosing that nonce there are maybe ways to extract the secret keys from your signatures. That’s why in normal single party signatures, ECDSA or Schnorr signatures or ed25519, all the elliptic curve signature schemes we know of, there’s common engineering practice to generate nonces deterministically. This maybe sounds weird. Deterministic is kind of the opposite to random so how can this work? If when deriving those nonces deterministically you use your secret key as a secret ingredient. Then still no one can predict what the outcome is. You can generate these nonces in a secure manner without relying on an external source of randomness that could fail, and still generate your signature securely.

SL: So when we’re saying deterministic it’s like that concept of when you hash the same word, so long as you do it through the same algorithm it will always hash out to the same outcome.

TR: It is actually what we do. You take your secret key, you take the message that you want to sign. You put those into a secure hash function. What you get out is the result of the hash function. Something that only you can know because only you know the secret key. You use that as your nonce. It is a simple procedure. Everybody is doing this in signatures because it is the right way. The problem is now if you move to the multisignature world where you have this interactive signing process suddenly it’s the other way around. If you use deterministic nonces your security breaks down immediately. This is a very weird thing. If you look at BIP 340 which specifies Schnorr signatures, we put a warning in there to make that explicit after people got it wrong. They took our MuSig scheme and implemented it in a deterministic way. They thought “We have always been told to use deterministic nonces so of course we are going to do this here.” I can’t blame them for this because it’s natural.

SL: So how did MuSig-DN come up and in what kind of context does it make sense to use MuSig-DN?

JN: The interesting thing there is if only one signer derives their nonce deterministically that’s insecure. But if everyone derives their nonce deterministically then it would be secure. It turns out that you can build a zero knowledge proof showing to the other signers that you yourself have deterministically derived your nonce. So what you are doing compared to the normal MuSig scheme is you receive all these nonces and proofs. You verify them and you generate your own nonce deterministically. Then this is secure. The big question there is or the big part of the paper is one, is this still a secure signature scheme and two, how can we really make this efficient?

SL: Was this Adam Back’s idea?

JN: I don’t know, actually. I would say it’s probably folklore that came up in IRC or something.

TR: I heard it’s your idea. I don’t know. Maybe it’s folkfore.

JN: The idea isn’t really all that great. It’s difficult to make it efficient.

SL: So tell us a little bit about that process. Zero knowledge proofs, as I understand, they tend to be computationally efficient or the size of the transactions are bigger. Tell us about that in terms of MuSig-DN.

JN: If we start with the end result you can see that it’s not too limiting. On a desktop machine it takes about one second to create a proof for a single signature and a few milliseconds, I think, on the order of 50 to verify such a proof. So that’s not really a limitation. The size of a proof is about a thousand bytes if I remember correctly.

SL: So not an issue for a desktop computer but perhaps an issue if we were to talk about hardware wallet devices, like Trezor and Coldcard and things like that?

JN: These hardware wallet devices, they have very different specs. They do different things on different processors. It is not easy to say if that would really be workable. In a Bitcoin transaction you can have multiple signatures, not only one. I think what this shows is that the limitation isn’t the computational complexity but rather the code complexity that this zero knowledge proof entails. If someone were to use it in practice, we have proof of concept code, you would really need to audit the code very, very closely and see if there are any flaws.

TR: Let me stress that because people tend to forget about this. MuSig-DN removes one possibility to shoot yourself in the foot. It removes this reliance on the random number generator. On the other hand it is much more complex than what we did in MuSig1 for example in terms of engineering complexity. Building the secure zero knowledge proof and implementing it correctly is pretty complicated. Of course you can get it right. Software has bugs. I don’t have a measure on the lines of code of the zero knowledge proof as compared to the rest of the signing. I think the difference is large. Maybe 10x this is just a guess. If you have 10x lines of code it is much easier to make a mistake. We really need to work on the careful implementation of MuSig-DN before it’s really ready to be used in practice and we can trust it.

## MuSig-DN use cases

SL: What kind of business or what kind of use case would that make sense for? A Bitcoin exchange wants to have a warm wallet and they would use MuSig-DN to distribute that? What kind of example uses would you see for MuSig-DN?

JN: That’s really hard to say because we need to see if it’s really a problem to maintain state or not. So we at Blockstream, we’re not currently focusing on developing these techniques and showing that our MuSig-DN implementation is without any bugs. We are more focusing on MuSig2 right now.

TR: One thing we could add here, maybe you can see this as a intermediate step. I think cold storage for an exchange is in a sense a good one because they need the highest level of security. Even if you run this additionally on a hardware wallet, maybe it takes 10 seconds, maybe it takes a minute. It depends on the hardware wallet, I’m just making up these numbers. Even if it takes a minute, this is usually not something that you expect from cryptography on your desktop machine. But moving from cold storage to warm storage, if this takes a minute, I think you don’t really care. This is still acceptable. I think that the big limitation here is that this is only for n-of-n. If you are a huge exchange, you want to keep your cold storage in m-of-n because if you lose one of those devices or whatever it is your funds will be gone. You probably want m-of-n where maybe this is 2-of-3 or 7-of-10 or something like this. Until we build a version of MuSig-DN that works with threshold signatures, we’re not currently working on this. Maybe we can see this as more of an intermediate step if you think about those scenarios that you mentioned where we really need the highest level of security.

JN: To give an example, for Lightning it’s not a problem to keep state because it can keep the state in memory. If your program aborts or crashes then just do a completely new signing session. The same holds for federated sidechains and also Blockstream Green.

## MuSig2

MuSig2 paper: https://eprint.iacr.org/2020/1261.pdf

SL: Shall we chat about MuSig2? What was the impetus behind this?

JN: The impetus was just realizing that there is some kind of trick where you could actually do two round MuSig. It is a very simple trick. Unlike MuSig- DN there’s no heavy zero knowledge machinery. The complexity is very similar to MuSig. We just started trying to prove this secure because we didn’t want to make any claims again that we have found some two round scheme that was secure.

TR: Maybe you should mention that MuSig-DN also has only two rounds. It is rather a neat side effect of it. You need this expensive zero knowledge proof so it doesn’t matter if you have one round more or less. This was one addition about MuSig-DN.

JN: We teamed up again with Yannick Seurin and wrote two different proofs and two different models to show that this can actually be used. It is even simpler in code complexity than MuSig1. You could even say it’s non-interactive because the first round you can view as some kind of a pre-processing step. It can happen before the message is known. If you want to set up your quorum, you have some pairing step where you already exchange the first round, you store the state. Later when you have a transaction to sign, it’s the same as right now, no additional rounds or running back and forth to your safety deposit box.

SL: In the paper you talk about MuSig2 being secure under concurrent signing as opposed to previously requiring sequential signing. What’s the difference there?

TR: This relates to what I hinted at earlier with Wagner’s attack. The reason why MuSig1 has three rounds and the insecure two round version of it was insecure is really only concurrent sessions. This means that you have a device which has a secret key and is involved in multiple signing sessions at the same time. This can of course happen if this is your desktop machine and you’re creating transactions with multiple people at the same time. Only in this case this two round version becomes insecure and attacks like Wagner’s attack apply. The attack works by creating a lot of signing sessions with you. Let’s say 50 signing sessions and then grinding a lot of hash nonces. Then they can extract 51 signatures from you but they should only be able to extract 50. You are running 50 signing sessions. Maybe this is not so relevant in practice but we want schemes that robust to misuse. If we as a protocol designer can build signature schemes that don’t have this flaw then nobody can get it wrong in practice. Having multiple sessions is something that could easily happen. Say you copy your key to a second device. This is something you shouldn’t do but some people will do. Then those two devices could have concurrent sessions and they don’t even know each other. It is very hard to to make sure that you only run one session at a time and this may be a problem. If you go to scenarios like Lightning where you have a Lightning node and you want to use MuSig with a counterparty. Maybe there are two things going on at the same time. You would be blocked and others could run denial of service attacks on you. Starting a signing session and never finishing it. You would have to wait for it to be finished because otherwise you can’t move on to the second session. We really want a scheme that is usable with as many concurrent sessions as you wish. This is where MuSig2 comes in.

SL: Can you tell us more about MuSig2 and how it would look and what’s involved with it?

TR: If you look at applications where we really envision this to be used is protocols like Lightning. Currently you are in a Lightning channel between two parties, they run a multisignature, they do this using the naive thing with Bitcoin script. This is a scenario where we want MuSig to be used because it’s now efficient. You don’t need this additional round trip because it’s only two rounds. You can pre-process the first round. When you set up the channel you can already do the pre-processing. If you want to send some money over the channel only then you get the message you want to sign. Then it’s basically one additional message on the network to create the signature. If you want to differentiate this with MuSig-DN, it’s really simple and lightweight. This is something you can write into a specification for Lightning for example. In theory you could use something like MuSig-DN in Lightning but you probably wouldn’t want to have this in the spec because MuSig-DN only works if everybody is using this deterministic nonce that we explained earlier. You would put the burden of running the expensive zero knowledge proofs on everybody. It is probably not something you can agree on. But MuSig2 is simple enough that I hope that people can agree on using this in Lightning and other higher level protocols, discreet log contracts and other things you can build with Schnorr signatures.

## One-more discrete logarithm assumption

Paper on the one-more discrete logarithm assumption: https://eprint.iacr.org/2007/442.pdf

SL: What is the one-more discrete logarithm assumption and what’s the implication of that for the security of MuSig2?

TR: All of our modern public key crypto, when you talk about signatures it is a public key primitive in cryptography because it has public keys. It is built on cryptographic hardness assumptions. These are problems that we hope are hard to do on the computer. That’s where they get their security from. It is kind of weird when I say hope, it’s really just a hope. Our confidence in these assumptions is usually really, really good because people spend like 30 years trying to break them and trying to come up with efficient algorithms and failed to do so. This is how we obtain our security for Schnorr signatures, by assuming the hardness of a specific computational problem. This is the discrete logarithm problem. It is a problem related to elliptic curves where you get a group element and you have to compute the discrete logarithm of it. People tried this for many years and failed to come up with efficient algorithms for that so we believe this is hard. One advantage of Schnorr signatures over ECDSA, with Schnorr signatures we can prove them secure if the discrete logarithm is hard. For ECDSA that’s a hard story. You also hope that ECDSA is hard to break but we don’t have nice mathematical proofs for this. This is one theoretical advantage of Schnorr signatures. With MuSig2 we need to make a stronger assumption. For MuSig1 we were able to prove this secure if the discrete logarithm assumption holds. This is nice because as compared to Schnorr signatures, we need these to be secure because otherwise MuSig can’t be secure because it uses Schnorr signatures, we don’t need to introduce additional assumptions. For MuSig2 to get this more efficient we need to have an additional assumption that’s called [one-more discrete logarithm assumption](https://eprint.iacr.org/2007/442.pdf). The normal discrete logarithm assumption is I give you one elliptic curve point and you need to compute the discrete logarithm. We hope this is hard.

JN: Just to give an example your group element would be your public key. The secret key is the discrete logarithm.

TR: That’s a very nice example I should have brought up. It should of course be hard to compute secret keys from public keys. Otherwise all the security is gone. This is an example for discrete logarithm. In normal discrete logarithm, I give you one public key and you have to come up with the secret key. Hopefully this is hard. In one-more discrete logarithm this is a little bit generalized. The game is different. The game is I give you let’s say 10 public keys. Now you can ask me for nine secret keys and still you shouldn’t be able to figure out the 10th secret key. The interesting thing about this is that you can’t ask for exact secret keys of things that I gave you public keys for but you can combine them, you can add them up. For example I can send you 10 public keys, public key 1 to public key 10. Then you could ask me for the secret key of public key 1 plus public key 2. You can play tricks like this but you can only ask 9 questions. In the end after you ask 9 questions if you can compute the secret keys of all of these 10 things I’ve sent to you then you solve the problem. We still believe this is hard because people have used this in the past but it is not exactly equivalent to the normal discrete logarithm assumptions. We have to make a stronger assumption but as I say this assumption has been used in the past so we are pretty confident that it holds. It is not an issue in practice.

## MuSig2 use cases

SL: You mentioned earlier that your aim is that this would be used inside of Lightning as an example. Would it also make sense to have this as part of general hardware wallets and multisignature security? To use MuSig2 as part of that or in your view is it not really well designed for that purpose?

JN: I think this is really up to the designers of hardware wallets. If people figure out how to do this they really have a competitive advantage because using MuSig versus this naive technique of using Bitcoin script is more efficient. It saves fees and it’s more private. I think there’s an incentive to get this working. As I understand quite a few of the hardware wallets already are stateful and depend on state to be secure. It wouldn’t be such an additional burden to also use MuSig2.

SL: I know some of the hardware wallet manufacturers are looking at these things like registering the other participants inside your quorum for a security reason. Maybe that is similar to the point you were saying about having to maintain additional state. Would they would need additional specs in terms of the current day hardware wallets, would they need additional specs in terms of processing power or memory?

JN: No because these multisignatures are very similar to normal Schnorr signatures. If you can do a normal Schnorr signature in a reasonable amount of time you will probably also be able to do… It is a little bit more complicated but that shouldn’t matter much.

TR: It’s really similar. I think that’s really the selling point of MuSig2. It is almost as simple as a normal signature in terms of computing power and memory and all the resources you need.

JN: This is why we’re calling it MuSig2 because it really supersedes MuSig1. There’s no reason to use MuSig1.

## Using MuSig2 for threshold signature schemes

Murch on Taproot 2-of-3: https://medium.com/@murchandamus/2-of-3-multisig-inputs-using-pay-to-taproot-d5faf2312ba3

SL: To clarify with MuSig2, is this a threshold signature scheme or does it have to be m-of-m, 3-of-3 for example?

JN: It is a m-of-m scheme so you can only use it for having the same amount of signers as public keys. But as people might know in Taproot for example you have this key spend condition, which means that in a Taproot output there is this public key and you can spend directly from it or you could reveal some parts of a Merkle tree. If you want to instantiate a 2-of-3 policy with MuSig what you can do is you can create three 2-of-2 MuSig public keys and put them into leaves of this tree. This is cheaper than using 2-of-3 with Bitcoin script but it also doesn’t reveal that this is a 2-of-2 policy because it looks like a public key hidden in this tree.

SL: This is the difference between a key path spend and a script path spend in the Taproot world?

JN: If you have a 2-of-3 quorum there’s perhaps two signers which are more likely to produce signatures and you would aggregate their public key, put it into the Taproot key because that’s the most likely spend. The other 2-of-2 you will put into this tree. If you spend with these two then you would have to reveal that they are in this tree but you wouldn’t reveal that this is a 2-of-2. You would only show there’s a public key and you’re going to spend it.

SL: Let me put that into a practical example then. Let’s say listeners want to do Michael Flaxman’s guide to 2-of-3. Have one Coldcard, one Cobo and one seed picker which is a paper or metal seed, the 24 words. If they know that most of the time they’re going to be signing with the Coldcard and the Cobo vault then they would put that into the key path spend. The other spending pathways would be captured inside the script or tree aspect of it. That’s how they could still use MuSig2 if hypothetically Coldcard and Cobo supported it. That is an example of what’s possible?

JN: Yeah, exactly. This is a simple way to create threshold policies with MuSig2 in a Taproot world. Of course this doesn’t scale very well. If you try to have a 60-of-100 for example then your tree will get very, very big.

TR: I guess we really need to work on a threshold version. We are aware that this is what a lot of people will need but things take time. There are a lot of things going on, other research groups for example. There’s a paper called [FROST](https://eprint.iacr.org/2020/852.pdf) or scheme called FROST by Chelsea Komlo and Ian Goldberg. They came up with a very similar idea like we did for MuSig2. Their scheme works in a real threshold setting. We have some criticisms about their security proof because we believe ours is more precise. But I really think they are going in the right direction. It doesn’t have all the features that we want for MuSig, this kind of key aggregation step where you take some public keys and combine them into an aggregate key. They don’t have this in the same way as MuSig does. But I hope that in the future we can combine all these approaches and can come up with a MuSig2 threshold scheme. I’m talking about future stuff that of course can take time.

SL: The important part is that it’s possible right?

TR: We believe it’s possible. If you ask me now I could write up the procedure for doing it. It is just that we need to be very careful and do our work to try to prove this secure to be really confident about it.

SL: Are there any other key changes in terms of what it would look for setting up the quorum, the initializing of that multisignature setup or any other changes in terms of signing a transaction? Or do you think all said and done, it’s going to look very similar to current day multisignature once the spec is made, once the hardware wallets are made, once the software is updated for it?

JN: I would say so but I don’t say it with confidence because we’ve learned in the past one, two years that there are really subtle attacks on these hardware wallets. It’s really difficult to rule out at this point that there will be some additional measures that hardware wallets would need to take to use MuSig2.

SL: In terms of the Bitcoin wallet software required to do Taproot multisig or Taproot MuSig2. Are there any key changes that you can think of there that are required versus the typical ECDSA multisig available today?

JN: I don’t think so. It’s relatively straightforward to integrate this as long as you’re able to store this session state, or even better don’t store it, just keep it in memory and renegotiate or repair as soon as you start up again.

SL: In terms of required changes to Bitcoin script, would there be any key changes there or would it be that aspect we were talking about before with the key path and the script path spend versus the current day ECDSA just showing exactly the spending condition in the script?

TR: I think this is one of the nice features of this interactive way of doing multisignatures or threshold signatures is that what comes out of the signing process is a normal signature. What comes out of the key aggregation process is a normal Schnorr public key. This just looks like a normal signature onchain. As soon as you have support for Schnorr signatures onchain, you wouldn’t even need strictly speaking Taproot to do this. You just need the ability to verify Schnorr signatures on the chain. You can use all those interactive schemes like MuSig, MuSig2 and MuSig-DN to create your signatures. That’s pretty cool because what ends up onchain is just the public key and a signature. This is not only nice for efficiency because those are very small but also for privacy because in most cases people observing the chain can’t even tell that you used sophisticated multisignatures in the background. It just looks like a normal spend.

SL: In practice people could be doing MuSig2 for multisignature or a kind of threshold scheme to HODL their coins with more security or they could be opening Lightning channels to each other. In terms of onchain analytics or surveillance they would look similar?

JN: Or they could do a normal payment which looks exactly the same as well. In the Taproot world your spend is either just a signature so there is no opcode because you provide a signature for the public key and the Taproot output, or it’s just a CHECKSIG opcode. The same as a normal payment.

## Scriptless scripts and PTLCs

Nadav Kohen on PTLCs at The Lightning Conference: https://diyhpl.us/wiki/transcripts/lightning-conference/2019/2019-10-20-nadav-kohen-payment-points/

SL: Some very cool implications there in terms of giving everyone a little bit more privacy. Also Jonas, I know you were talking about scriptless scripts, point time-locking and the Lightning implications of this work. Could you outline a bit of that for us as well?

JN: We touched a little bit on that. There is the idea with Schnorr signatures, you can also do it with ECDSA but it’s more complicated, you could do Lightning payments with scriptless scripts. Perhaps people are familiar, right now in order to make a Lightning payment you have these hash timelocked contracts (HTLCs) so you need to provide a hash preimage to claim the payment. One of the problems is that this hash preimage has to be the same on every hop of the payment route. This allows nodes on this route to correlate the payment and see where the payment is coming from and where it’s going. One of the advantages with scriptless script Lightning is that you wouldn’t have hash preimages anymore. You would use public keys and secret keys. You would be able to randomize this payment preimage, it isn’t a hash preimage any more but a secret key now. You would be able to randomize it on every hop. Even if two nodes on the route collude and talk about which payments are are coming through they wouldn’t be able to correlate it aside from timing maybe because now this payment preimage is randomized on every hop. This is one of the advantages of scriptless script Lightning. One of the other ones is that you get a proper proof of payment. Right now if you pay someone you get a payment preimage but every hop on the route gets this preimage so this doesn’t really work as a proof of payment. Scriptless script Lightning solves that. In order to use scriptless script Lightning with Schnorr you need some kind of MuSig, preferably MuSig2.

SL: Listeners who are interested, you can check out my earlier episode with Rusty Russell, we spoke about MPP and he was talking about the proof of payment in that episode. If you’re interested in the Lightning spec discussion also check out Episode 200 with Christian Decker where we go into some of that also. So Jonas and Tim are there any other pieces of feedback that you’ve received from other cryptographers or other people in security on your work with MuSig2 and MuSig-DN?

TR: One interesting thing about MuSig2 is that as I already mentioned at least one other team came up with the same core idea to make this secure with two rounds under concurrent sessions. There was even a third team with Jeffrey Burgess that came up with the same idea independently. This is neat because this gives us some additional confidence if research teams have the same idea. It’s a fun coincidence that they have it at the same time but I think this is because there’s a lot of interest in building multisignature schemes right now. If three research teams or six people come up with the same idea this gives us some more confidence that it’s actually the right thing that we’re doing here and it’s really secure. This is one part, Jonas can you say something about MuSig-DN?

JN: Just to add to MuSig2, it’s really cool to see that other people are working on these problems as well because in the past it was hard to motivate these problems. Often cryptographers think these are boring problems that have already been solved. Why don’t you use more complicated cryptographic assumptions and so on. They don’t really understand this very specific setting of Bitcoin where we want to rely on only the discrete logarithm assumption and we cannot easily make consensus changes etc. It is cool to see with MuSig2 that other people are interested as well. This was also a bit of problem for MuSig-DN to motivate because everyone’s response was “It doesn’t seem to be very interesting. It just seems to be more theoretical.” Whereas we think this (MuSig2) is very practical because you don’t have the disadvantage of the zero knowledge proof. We did this because we need it in a practical setting and MuSig-DN makes some applications more practical.

SL: I guess maybe a skin in the game question. A few years down the line would you guys be comfortable keeping your own Bitcoin stash in a MuSig2 scheme?

JN: Yes.

TR: Certainly.

SL: Great to hear that there’s some confidence there.

TR: I’d prefer maybe a threshold setup but I’m very confident in MuSig2. Now I have some incentive to work on a threshold extension to keep my own coins very secure.

SL: Until a threshold scheme is done I guess people would have to be more careful about keeping the backup 24 word seed for example. Maybe they would have 3-of-5 and make sure that they’ve got all the 24 word backup on a steel thing so they can recover that hardware wallet key and still sign even in a 3-of-3 or 5-of-5 scenario?

JN: This works but of course this has the disadvantage as far as I know that you need to put all your backups into one location again to restore. I think it would be better to create threshold policies using the Taproot tree.

TR: It depends on the scenario. If you store your Bitcoin… that’s maybe where if you do it in a Taproot tree or using other methods will be better for now. In some scenarios you really need this n-of-n and our prime example again is Lightning. This is where we see MuSig2 where they have 2-of-2 channels and this is exactly what you need.

## Future Work

SL: Where do we go from here with MuSig2? What kind of development or contributions would you like to see? Or what do you see that’s necessary before we get further adoption of MuSig2?

JN: One thing that I really want to do is to update our implementation from MuSig1 to MuSig2. I hope that we’ll be mostly deleting code because you just delete now unnecessary states. I’m looking forward to actually do that.

TR: In terms of implementation we have this repository [secp256k1-zkp](https://github.com/ElementsProject/secp256k1-zkp) which Jonas was referring to where we currently have an implementation of MuSig1. We will of course update this to MuSig2. I hope that others will implement our scheme or use our library because it’s really simple in the sense that it’s not hard to implement. Crypto is always hard to implement but if you’re already implementing Schnorr signatures then it’s not much to be added on top of it. This is a difference to MuSig-DN where you have this hugely complicated zero knowledge proof which even scares me a little bit from an implementation point of view. MuSig2, because it’s so simple will see more implementations than our own library. I hope that people can play around with it and see if it fits their higher level protocols, like Lightning, DLCs, scriptless scripts and all the magic stuff you can build on multisignatures.

JN: I suppose previously the interest wasn’t really high because no one knew whether Taproot would be a thing in the future. Now it seems like this becomes a reality at some point. On the theoretical side I think one interesting thing that we want to do with MuSig2 is realizing a concept that we call nesting. This means that you can have a tree of MuSig keys. Let’s say you have Alice and Bob and they can aggregate their key. Their aggregated key can be used again with another participant called Charlie. They can aggregate this key together to have a 3-of-3 but Charlie doesn’t know there is an Alice and Bob. He just sees their aggregated key, a single key. This has some applications to channel factories. It makes some multisig setups more private because now we have signers that don’t need to know about all of the other signers. They only need to know about one aggregated key. You don’t know whether this is an aggregated key or this is a single signer.

SL: Interesting. So that could make sense in some kind of inheritance scenarios where a lawyer has a key or things like that.

TR: One simple example. I’m not sure if it’s a good example in practice. Think again of a Lightning channel 2-of-2, you have a Lightning channel with some other peer on the Lightning Network. Internally you want to use multisignatures for enhanced security. Your part of the Lightning channel is a MuSig between your desktop machine and your hardware wallet. The other party in Lightning channel wouldn’t know or wouldn’t even need to care that you internally run a MuSig. This is maybe an example to illustrate what’s going on here.

SL: I think those are the key points. Was there anything else that I missed or anything else you wanted to discuss related to MuSig2?

JN: If people want to help us implement this Tim already mentioned [secp256k1-zkp](https://github.com/ElementsProject/secp256k1-zkp) this is where we’re working or [secp256k1](https://github.com/bitcoin-core/secp256k1). See you there.

TR: Feel free to reach out to us and bother us with questions or ideas or anything.

SL: Great. So where can people find you online?

Jonas Nick: /@n1ckler on [Twitter](https://twitter.com/n1ckler).

TR: Twitter is nice or GitHub.

SL: Excellent. Thanks very much guys for joining me.

