---
title: Sydney Socratic Seminar - FROST
transcript_by: Michael Folkson
tags:
  - threshold-signature
speakers:
  - Jesse Posner
date: 2022-03-29
media: https://rumble.com/vz3i3u-frost-the-future-of-schnorr-multisignatures-on-bitcoin.html
---
FROST paper: <https://eprint.iacr.org/2020/852.pdf>

secp256k1-zkp PR: <https://github.com/ElementsProject/secp256k1-zkp/pull/138>

secp256kfun issue: <https://github.com/LLFourn/secp256kfun/issues/85>

Ceremonies for Applied Secret Sharing paper: <https://cypherpunks.ca/~iang/pubs/mindgap-popets20.pdf>

Coinbase blog post: <https://blog.coinbase.com/frost-flexible-round-optimized-schnorr-threshold-signatures-b2e950164ee1>

Andrew Poelstra presentation at SF Bitcoin Devs 2019: <https://btctranscripts.com/sf-bitcoin-meetup/2019-02-04-threshold-signatures-and-accountability/>

Tim Ruffing presentation at CES Summit 2019: <https://btctranscripts.com/cryptoeconomic-systems/2019/threshold-schnorr-signatures/>

## Introduction

Lloyd Fournier (LF): This is going to be a discussion meeting with our very special guest Jesse Posner is going to tell us about what he’s been up to, what he thinks about FROST and its applications to Bitcoin. We are going to also provide him input about where we think that should go. It is an open question about how users will interact with this thing, how it will evolve and be used by Bitcoiners. I have created a slideshow of notes that we’ll go through as a way of structuring the conversation and making sure we don’t forget anything. Let me get that up.

Does that start quite basic, what is FROST? Or are we going straight in?

LF: We are going to say quite briefly what that is, for the sake of the recording. It doesn’t really have any diagrams or anything. You probably have to go elsewhere for your basic knowledge on FROST. Unless you are happy with a very short summary.

## How multisig currently works

LF: We have this opcode called OP_CHECKMULTISIG which we put in to pay-to-script-hash (P2SH) outputs. Pay-to-witness-script-hash (P2WSH) or P2SH. If you want t of n signers, t is the threshold of signers and n is the total number of possible signers. Very common ones are 3-of-5, you need 3 signatures out of 5 possible keys. Or 2-of-3 is probably the most common one. In order to that you put your n public keys in a script and you provide t individual signatures in the witness to that transaction. That’s how it currently works.

## FROST

LF: With FROST we are moving to a model where we just have a single public key and a single signature for any number of thresholds you want.

## Advantages of FROST versus existing multisignatures

(With naive multisig to spend there is 96+ bytes per signer in the witness. It has bad privacy as a chain observer can learn how coins are being held onchain and can see when they leave the wallet using heuristics. With FROST regardless of the number of signers there is just 64 bytes in the witness. Spends reveal nothing.)

LF: The main advantages are two things. There is much less data. For the existing multisig there is more than 96 bytes per signer. The first signer who is going to authorize this transaction, more than 96 bytes for each one. If you have got 3-of-5 it is 3 times 96 and a little more. For FROST regardless of the threshold and the number of signers it is just 64 bytes every time. It is less for a 1-of-1, that’s how Schnorr is, as you increase the number of signers it doesn’t increase at all. It is the same as a single signature. That is fantastic for reducing the blockchain footprint of multisignatures, it is also really good for privacy. If you can see the blockchain and you see someone spend with a 3-of-5 or a 2-of-3 you know how those coins are being held. If it is a lot of coins you know potentially how difficult the attack would be on those coins. How many persons own them. You’ll also see where coins go. It is very easy to see when that 3-of-5 makes a donation to an address which one is the change address, which one is the main one because one will be going to a P2SH which eventually gets spent as well with a 3-of-5 again. You’ll be able to see “That 3-of-5 is moving their coins here. Those coins are going to someone else.” It is bad for privacy and it also means that these multisig spends, which will be a large proportion of Bitcoin spends, do not contribute to the anonymity set of other types of spends like Lightning channels and so on. When Lightning channels move to MuSig(2) they will also be a single signature from Schnorr. You’d like all these multisig spends to also be single signature spends so you cannot distinguish a Lightning channel opening or any kind of protocol from a multisig spend. That would be ideal. They are the main big wins from FROST. There are other wins and there are losses as well. We are going to get into the weeds about what those are and what pathway we can take to reduce the losses and make it flexible so you can choose your trade-offs in your context and how to accentuate the gains you get from moving to this new model.

## Distributed key generation

LF: The FROST protocol starts off with distributed key generation. Jesse, this is where I am going to ask you to come in and give us the high level view on how that works and what that means for someone who wants to use FROST.

Jesse Posner (JP): Let me just apologize in advance because it is 1am my time, I might be a little bit slower than usual. The idea with distributed key generation is we want to create a public, private keypair where none of the parties involved know the private key. But they all contribute data to create this private key, they send some data around. At the end of the process we have a public key and we have Shamir shares of a private key. The actual private key itself has never been constructed. This is in contrast to how we typically do things with Shamir’s Secret Sharing where we start out with the secret and then we split it into shares. At some later point we take the shares and we combine them back into the secret. Now what we are doing is we want to have the shares without starting with it constructed and we want to be able to sign with it without having to bring the shares back. Distributed key generation, there is no signing, it is just about building this public, private keypair. If you know a little about Shamir’s Secret Sharing works you generate a polynomial with random coefficients and you evaluate the polynomial at different indexes to get the shares. The idea with distributed key generation is if we have multiple participants each creating a polynomial, when they evaluate points with their polynomials the sum of the y coordinates is the evaluation of the point at the sum of their polynomials. It sounds really confusing when you describe it that way but if we had more time to whiteboard it it would be more clear.

LF: We can leave the moon math out. Polynomials are moon math to me. They key takeaway is that at the end of the thing you get a secret from the output of the protocol. You send some messages, you get some messages, your secret will be generated from the output of that protocol.

JP: What it will look like from an API level is each participant is going to call a function to generate shares. They are going to generate one share for each other participant. Let’s say there are 3 participants: Alice, Bob, Carol. Alice generates 3 shares, Bob generates 3 shares, Carol generates 3 shares. Each participant sends a share to each other participant and keeps a share for themselves. Alice keeps a share for herself, Alice sends a share to Bob, Alice sends a share to Carol. Bob keeps a share for himself, sends to Alice, sends to Carol, so on. Now what they do is each participant has 3 shares, one from each other participant that they’ve received, not the ones that they generated but the ones they received including the one they generated for themselves. They add those together. That aggregate share is a share of the secret that is the aggregate of the secret of the participants. Once they add the shares they’ve received together, that aggregate share, that’s their new secret. That’s their Shamir Share. The private key part of the process is now done. Each participant has a share of the private key. The public key, how you get that, when we created these shares we did it by creating a polynomial, a polynomial is defined by coefficients. These were random coefficients. Each participant, they are going to commit to each cooefficient. Essentially what they are doing is they are providing a commitment to the structure of the polynomial without revealing the actual terms of the polynomial. Once each participant has this structure of the polynomial they can verify their shares against it but they can also use that to compute the public key. The commitment to the first coefficient, when you sum those commitments together it will be the public key because the private key is the sum of the first coefficient of all the polynomials. To summarize, you generate shares, you generate commitments, you distribute shares, you distribute commitments, verify the shares, aggregate the shares. Then you derive the public key. The last step is there is a requirement when you send these coefficient commitments around that each participant needs to know that they received the same ones as everyone else. The way that is described in the paper is that it calls for a broadcast channel.

LF: I have a slide on this. We are going to leave the integrity of that process and how we ensure it later on.

Ruben Somsen (RS): Is it the case that with these polynomials you can just do linear math? Is it as simple as that? You are adding these polynomials together. Is it all just linear like Schnorr?

LF: It can all be done through group operation. The mathematics is not linear but the bit where you care about the polynomial is in the scalar field. The polynomial, the squaring and the cubing and stuff that happens is all done in the scalar field where you can do multiplication, where that works well.

RS: You are also adding the private key. A simple example would be I have a polynomial, you have a polynomial. We can add the results together for a 1-of-2, if we have two points on them. It is just addition basically, that’s the question.

JP: Yeah you are just adding polynomials together, adding y values that are evaluated against those polynomials together. Everything combines very nicely.

LF: What does a 1-of-2 look like? The most pathologically simple case, what does that look like?

JP: A 1-of-2 is going to be a zero degree polynomial. A 1-of-2 is just you know the secret right? You could take a private key and just copy it over and over again and give it out to people.

LF:  Exactly, a 1-of-2, if you were to follow the protocol exactly you would both generate secret keys, then you would give the other guy your secret key. You would have the joint key be the sum of your two keys. This is totally superfluous, you could just generate a key and send it to the other guy I guess.

JP: You wouldn’t need to sum them in that case. In fact I think they may just define the protocol that t is greater than 1. I’m not sure.

## The signing keys are not derivable

(How can users recover funds in case they have seed words but lost FROST keys?)

LF: The signing keys are not derivable, you cannot derive these signing keys from seed words. How can users recover funds in case they have seed words but have lost their FROST keys from the key generation? Do you have thoughts?

JP: The share generation API takes a public, private keypair as an input. The private key becomes the first coefficient. That is up to the user to generate using their own entropy some keypair. If you provide that API the same keypair with the same parameters, it is deterministic, you will get the same cooefficients. That’s one potential way to recover the polynomial. You backup this keypair and the parameters, then you can reconstruct the polynomial.

LF: You can reconstruct your own polynomial? The entire beginning of the protocol is you provide an input, a single Bitcoin keypair. The other portion of secret data which is the rest of the coefficients in the polynomial will be deterministically derived from that?

JP: That’s one potential path. I might add to the API some auxiliary randomness. If you want it not to be deterministic you can throw in some extra random data.

LF: We cannot recover funds just because we have our polynomial?

JP: Once the participant has their polynomial they could re-derive the shares that they have created. Then they would need other participants to derive their shares. This is not as good a way for backup potentially as the other idea which is to take your aggregated secret share and split that into shares, distribute those shares to the other participants. Let’s say I lose my share. I can ask a threshold of participants for their disaster recovery shares that I’ve given them. They give them back to me. Now I can reconstruct my aggregate share. That is one potential method for recovery.

LF: You can do that without bringing every device online? You can do a recovery by only bringing a threshold of devices online.

JP: Yes and it could be asynchronous.

RS: The scenario here is you have your seed phrase but you don’t have anything else. You still need to know who the threshold is, who you were communicating with. You need more information than just your seed. I guess it is difficult because you make the seed phrase first. It makes sense to me that you make the seed phrase, you make it for the purpose of the multisig, you do the whole generation thing and you just back that all up as the seed phrase. It seems like that is necessary anyway because you need to remember who the participants are.

JP: A compact way of serializing the necessary parameters is probably a useful API. Whatever is necessary for backup reconstruction, there should be some standard way to save that somewhere.

LF: We don’t have a specification for creating seed words from existing data. I don’t know if I have seen that in Bitcoin. If that exists then please let me know. I think right now you have to create the seed words first, that gives you the data. You cannot go from data to seed words.

Nick Farrow (NF): I guess you could go from 1s and 0s, convert it into numbers like they do with the dice rolls. You could get a seed that way.

LF: I think it is possible theoretically.

NF: There is no standard for it or anything.

LF: Maybe that is something we have to do as part of this work. There are a number of ways you could recover. You don’t know what your other signing devices are. In the setting of an individual user with multiple hardware wallets stashed away in different places, this is not a concern because that person will know the physical identity and can bring a threshold of them online to recover the other devices’ data.

NF: If a threshold of other people can come online and recover the secret shares that you stored with them earlier, that doesn’t let them sign for you because you still need your first coefficient from your polynomial which is derived from your seed?

LF: They can sign because they are threshold. They could come together and create everyone else’s shares but they could already sign straight away.

NF: So it doesn’t really matter.

LF: You assume that a threshold is always honest. Otherwise it is screwed. There is no plausible security model outside of that. The other idea is that you have this static key that goes into the initialization of the protocol, you could just hide a Tapscript which has that threshold using those static keys in it. If something bad happens you could always recover from seed words, you just have to reveal a Tapscript which could be deterministically generated. The problem would be is that you would still need to know what the public key is. If you have a threshold of the seed words you will not necessarily know what the public key is. If you only had 3 out of the 5 seed words you would still need to know which public keys were yours. You’d also have to have stored the public keys somehow or to recall the outputs, the UTXOs, somehow to be able to spend with that threshold.

JP: Yeah. I haven’t thought about it that deeply but that seems right. It seems like it is a problem space worth exploring more. I suspect there are some optimizations or some ways of making this work better. Another interesting idea is related to the method that you can use to refresh the shares or add participants or remove participants. This is another way to potentially do a recovery. Let’s say Alice forgets her share, she can generate coefficients with a zero term for the constant in the polynomial. The other coefficients are random. Then she evaluates shares from her polynomial and distributes those shares. The other participants can refresh their shares by generating new coefficients for the other terms or they can just evaluate the same shares, give her the shares that they did before. Now you’ve changed the shares, the secret is the same.

LF: The joint public key is the same, the funds don’t need to move. You do have to bring online every device in this case?

JP: Right.

## How many rounds of communication is the protocol?

(What will the workflow be for hardware wallet setup? How will this work in a hot wallet setup?)

LF: Let’s say you are an exchange who is setting up a 3-of-6 to hold custodial funds, what will the workflow be like for them to setup and do this key generation?

JP: One additional issue is that I don’t believe there is a hardware wallet that will do this kind of signing out of the box. It is not trivial to try to write custom Yubikey, HSM stuff. We need a hardware wallet that can do FROST. Hopefully we are going to get one in the not too distant future or multiple. One method that people do to still leverage a hardware wallet or more specifically a HSM not for signing but for decrypting things. Let’s say I have a share, maybe that share is stored in the cloud somewhere, but when I go to decrypt it I use my HSM to decrypt it. Now I have to be very careful about the device I’m using to decrypt the share. It will be in memory on that device. Then you have maybe an air gapped device that you can decrypt the share with, perform the signing. Now you have to export the signature from the air gapped device. It would be much nicer to just have some secure piece of hardware that can perform the signing without having to do this decryption, that actually has the share stored on the hardware. But for now we have to do these workarounds. Or you just rely on the distributed security. Rather than being super paranoid about one participant’s share and an air gap and all of this stuff, you accept that an individual share is vulnerable but an attack against a threshold of shares is not feasible. Then you might be able to just sign using a standard computer that isn’t air gapped. Another thing is you can have not just a set of human participants but you can have a set of server participants. Maybe you could even spread these servers across different clouds. You could have some in the Microsoft cloud, the Google cloud etc. The main thing is figuring out how to somehow split the access structure between these different server or cloud environments. One area for future exploration is how to have nested FROST setups or nested MuSig and FROST setups. What you want at a top level is for a threshold of servers and a threshold of humans to both sign. But both constituencies are required. You have a 2-of-2 top level MuSig key and then each of those components is a t-of-n threshold, one of servers and one of humans. You can start thinking about different ways of composing these different hierarchies and maybe mapping them onto organisational structures. You have a lot of flexibility on how you might set something like that up.

LF: A lot of flexibility to be extracted. One idea you just had, a good solution to the previous slide, we could encrypt the shares. What you could do instead of having to bring a threshold of devices online to recover your shares you could just encrypt your shares to every other guy when you’re giving him his shares. Maybe afterwards because you have to get your entire shares back. You could encrypt them and give them to everyone else. Then you just have to tell one coordinating signing device “Here’s my encrypted share” and you could get it back later on, decrypt it with your seed words based key. That makes sense?

JP: That’s right, yeah.

LF: Let’s say I’ve got these hardware wallets, they are FROST enabled hardware wallets and they are built specifically to do FROST. In the ideal world what does this look like? Let’s say each hardware wallet is air gapped or perhaps it can be plugged into the computer one by one. What does the workflow look like for me? How long is this going to take? Do I need all the hardware wallet devices in one room or can I do the first bit of the setup at my house with one hardware device, go over to my storage locker and do the next bit of the setup. I’ve got a hardware wallet over there. Can that be done or are there complications?

JP: It depends on if you want everything to be air gapped or if they can be networked devices. I imagine at some future state we can use a secure enclave on our phones or we have a hardware wallet device that plugs into our phones. Let’s say we need to generate keypairs rather than needing some crazy Faraday cage and all this crypto ops stuff. If we have networked devices spread out that can participate and send this data around then that would be ideal. If they are not going to be networked or some percentage of them aren’t networked then it depends on how you are securing your air gaps and who is running the air gaps, the operational flow around the air gaps will dictate the process.

LF: You have multiple rounds of this thing. So we cannot just do it in one round. We can’t just tap our NFC FROST thing once onto each phone. We have a phone that is our signing device, we have some NFC tapping FROST signer off there, the phone coordinates the signing,  we choose our transaction, we choose what we are going to do on the phone. But when we go to the phone app and we create this new FROST wallet, do that setup with our signing devices what I think we’ll have to do is tap at least twice. You’ll have to tap each device once and then tap each device again. Three times if you want to distribute the backups that we just talked about. Maybe the phone could keep the backups but you would still have to tap another time in that case. There are two rounds of interaction at the beginning, you have to tap at least twice every device. You probably want to start off with the devices in the same room before you move them around to another place if they are offline devices. If you could somehow plug the device into your laptop, you have one guy in Australia, one guy in Singapore, one guy in the US, if you want to do a 2-of-3 you plug your things into your laptop and at that point your app talks to each other and sets it all up. But if they cannot be plugged in you are going to have to at least tap these things at the same time. You can of course use the internet to bridge that.

JP: Absolutely. I misunderstood the question. For DKG, creating the private, public keypair, you have the two rounds. The first round is to distribute the commitments, the coefficients and the shares. Those are distributed. Then the second round is to distribute the signatures of the commitments. That’s one thing we touched upon briefly. The broadcast channel thing, you have to sign the commitments, distribute that. Then you are done. You have these two broadcast rounds for DKG, to set it up. Now you have a public, private keypair. The next thing to think about is how does signing work?

LF: We’ve got to the point where we understand how we get the key and how that process might feel as a user.

Michael Folkson (MF): An alternative setup would be you have a centralized coordinator, finalizer type party. That would reduce the complexity, With FROST everyone has to receive the shares of everybody else. That requires a lot of communication, perhaps you are sending your share to every single other party involved in the threshold. The comparison would be you just send your share to the coordinator, finalizer guy. Obviously that comes with downsides. Does a scheme like this work with a centralized coordinator, finalizer?

## How do you verify that the DKG worked?

(How do I know that the public key we get at the end really had contributions from each of my devices? In the corporate/organisation scenario how do we verify that each branch got a correct share before we put coins into it?)

LF: Let’s say you had this coordinator. How do you verify that this coordinator didn’t do anything wrong while you are doing this key generation? If you are sending messages all to each other how do you verify that one guy sent the same messages to the other guy that are all consistent? Are there concerns here?

JP: Yeah absolutely. With the coordinator when you are using the coordinator to send shares those shares are going to be encrypted to each participant. The coordinator is just collecting data that other participants  can query their shares from. Of course if you allow a trusted setup and you trust a coordinator to split the shares that simplifies setup quite a bit. If you don’t have a trusted setup then all the coordinator can do is collect things for the other participants to poll their shares down from.

LF: You are assuming that participants have a public key already for all the other devices. I want to infer at this point that you have to by some other channel verify. Call up Bob in Singapore and say “Hey Bob is this fingerprint the same as your fingerprint on your side?” Even if you are using a coordinator. There has to be some other way of verifying, at least in the first stage when no one has exchanged any messages.

JP: Yeah you are going to want to have some secure communication channel from each participant to each participant. The easiest way is for each participant to know an authentication key for each other participant, some public key. Each participant has to send secret data to each other participant, that data has to be encrypted. It has to be only seen by the participant it is being sent to. Everything already assumes you have secure communication channels set up.

MF: And if you have to set that up then there’s no upside to the centralized coordinator right? If you have that cost of setting up those private, secure communication channels between every single other party there is no real benefit to having a centralized coordinator. You might as well just keep it distributed.

JP: Instead of having peer-to-peer messaging let’s say you just have some central server that everybody is posting data to and polling data from. That may be convenient, they are just sending ciphertext back and forth through some central server. That would be the coordinator but it doesn’t really change that much. They could just send the data peer-to-peer instead.

MF: I think the point that I was alluding to and I think Lloyd was too is if you have that centralized coordinator in this alternative scheme everyone just sends the share to the centralized coordinator and you don’t need to set up all these communication channels between every single other party. Perhaps there is a public key that you can verify from the centralized coordinator that proves that it is actually been constructed using your share.

JP: When Alice sends some shares to the centralized coordinator, she sends a share for Bob and a share for Carol. She has to encrypt those shares. We don’t want the central coordinator to be able to see Bob’s shares or Carol’s shares. She needs to have some public key for Bob and some public key for Carol that she can encrypt the shares with before sending it to the coordinator. That public key is really the building block to the secure communication channel. Whether that channel is happening through a server that is an intermediary or through a direct connection, it is a secure channel because it is an encrypted communication that is made possible because they know each other’s public keys which has to happen by reference to some key registry or in person, they exchange public keys. Once these public keys are in place you can do it either way very easily. Through the coordinator or directly.

LF: On the theoretical side you need this existing public key and a secure channel. But if we are clever about it we can make it so that secure channel is as simple as a Signal message or a WhatsApp message. If you just happen to already have a Signal setup with that person you can perhaps get a visual thing there that we all match the same thing. A bit like when you log into a SSH server for the first time you get a visual fingerprint that shows you “This is the fingerprint of the server’s key”. You may remember it from what you’ve seen before, that’s the hope. If you are logging in from a device that doesn’t have that key you may remember the fingerprint that it gives you and say “Yes that is what I was expecting from that server”. What we can do at the end of the distributed key generation is take some subset of the data or all the data and hash it into a digest. As long as you can verify by pulling them up or by looking at the Signal message, “Yes we all have the same bytes, the same bech32 string or whatever, we all saw the same thing”. Even though we didn’t have public keys setup beforehand formally in the protocol we had some basic secure channel with each other through some messaging protocol, through the phone lines or whatever. I know your voice as long as it can’t be deepfaked. You have some trusted way of communicating, it can even be audio. Or just a text message. That is sufficient to set this up. You don’t need pre-existing shared public keys necessarily.

JP: This is a related problem to simply let’s say somebody gives me a Bitcoin address? How do I know that the person giving me that address is the person that I think they are. It is the same basic problem. That person could be man in the middled unless I have a secure communication channel with them through which I transmitted the address. Same thing with MuSig. If I am getting public keys from people to create this aggregate key how do I know where these public keys came from? How do I know it is Carol’s key and not Bob’s key? In a way all of Bitcoin presupposes that we have a secure way to give each other data about public keys, about addresses.

LF: That’s an excellent way of putting it. It is not a new problem we are solving here. It exists in existing multisig. You are giving me keys for a multisig, I need to know that the keys actually came from you to put into the multisig. These shares and all this stuff sounds complicated but it is actually the same problem and it is solved in the same way.

NF: Did you mention a trusted registry could be a possible solution? Something like PGP? That maybe wouldn’t leak any privacy because these public keys aren’t actually used for anything other than the encryption of the shares. It is not like you derive addresses or anything from them.

JP: Now we are just into the problem space of PKI and the whole universe of different solutions and systems that I don’t even know that much about. I know there is a lot there, people have thought about that for a long time, the best way to do that. Of course we have infrastructure built in to TLS and the web certificates. We probably want it decentralized. I am sure there are a million people who have claimed to solve this with the blockchain. Whether anyone actually has or not is of course another story.

LF: It is a general problem for all cryptography and especially relevant to Bitcoin but we have the same solution that already existed. You can also use registries and a bunch of other things. It depends on your setting, that is the main thing. The application developer, the person who is developing the interface, has to decide how you are going to verify these keys, these shares and the data that goes in the DKG. How are you going to verify that? It depends on the application I guess.

MF: And without the centralized coordinator, the centralized coordinator could go offline, die, get blown up and the scheme still continues to work. That is the obvious upside by everyone being able to construct the public key of everyone’s shares even if one party goes offline forever.

LF: You could set up a 2-of-3 or 3-of-5 via Signal without any coordinator. “Here’s my key, put it into the 3-of-5 that jointly owns these funds.” With this it is going to be a bit more complicated than that. We are not going to be able to send each other Signal messages. I’ve put crazy stuff in messages but we’re not going to specify that. That is a slight downside. You cannot just set it up so casually. You do need software that creates messages and talks to other people. If you are an individual it is much less of a problem. You are just doing a threshold with yourself. Or perhaps with a service like Casa or whatever. That is simple. You just have to put your hardware wallets in one after the other, go in a round robin fashion.

## Proofs of possession in the protocol

(There are “proofs of possession” in the protocol i.e. signatures that are there just to prove you know the private key. What should they sign? Do we even need them? Can’t we use MuSig’s trick instead? Wouldn’t it be useful to have the joint key a MuSig key anyway?)

LF: This is about proofs of possession. Unlike the MuSig protocol the way to protect against malicious key attacks or [rogue key attacks](https://btctranscripts.com/london-bitcoin-devs/2020-06-17-tim-ruffing-schnorr-multisig/#issue-1-rogue-key-attack) or key cancellation attacks as they are sometimes called, we provide in this protocol that we know the private key. We didn’t choose a public key maliciously. We know the private key, it is a valid private, public key from that perspective. You can choose your public key so that you don’t even know what the secret key is. It turns out that messes up badly with many protocols, multisignatures especially. That’s why MuSig was invented, to circumvent this problem. In FROST we are not using the same mechanisms as MuSig. Why would we not do that? Is there a good reason for that? What should the signature sign?

JP: For one the security proof for FROST is based on a proof of possession type of proof. That’s the weasel answer. We don’t use the MuSig style aggregation in FROST because of the security proof. The implementation I have in my PR right now is based on using the MuSig style key aggregation. Let’s say you already had a MuSig setup, a n-of-n MuSig setup. You can convert that into a FROST setup without changing the aggregate key by using the MuSig method of key aggregation instead of the proof of possession. That is what I have for my current implementation. I discussed this with Tim Ruffing and Jonas Nick, there is some [discussion](https://github.com/ElementsProject/secp256k1-zkp/pull/138#issuecomment-1007655837) on the PR, we decided for the first version of the implementation we would stick closer to the security proof and the protocol because the benefit of having this convertibility between MuSig and FROST, we are not quite clear what the use case is for that. There are some disadvantages, it is nice to have clear domain separation and clear separation between types of keys. It protects users from making mistakes where they could confuse their setups and stuff like that. I am right now working on a change to the implementation to use the proof of possessions and not the MuSig key aggregation coefficient. But I am totally open to anybody’s ideas or thoughts on which one is better or worse. I think it is an interesting choice. Two different ways to solve the same problem, protecting against the rogue key attack.

LF: We just lack a proof that it works in the context of FROST. To be fair it is quite a different context to the original. Even though on the surface it looks to be the same attack there are quite some differences there. One interesting problem with proofs of possession is that there may be cases where you already know that that person has the key. You’ve done the proof of possession implicitly outside the structure of your protocol somehow. That key is an input to the protocol anyway. We provide it ourselves in the API. Perhaps we’ve already signed with that key already and then this thing would be superfluous. Is there a possibility of letting the application decide or does putting a strong warning saying “You must make sure that this person owns this key otherwise you are screwed”. Or is that a terrible idea?

JP: This is where we get into the broadcast channel trick. We are repurposing the proof of possession to get this broadcast channel thing. Each participant sends these commitments to their coefficients to each other participant, that’s what we talked about before. They are revealing the structure of their polynomial without revealing the secrets for verification purposes. The verifications don’t provide the guarantees that you want unless you know that the commitments you received by the participant are the same commitments that everyone else received. Let’s say Alice sends out commitments to her polynomial and she sends different commitments to Bob and different commitments to Carol. She can trick Bob into having his shares verify and Carol into having her shares verify, even though they are not part of the same polynomial. So Bob and Carol need to know that they got the same commitments from Alice. In the FROST paper and in most threshold scheme papers they simply specify that the participants have access to a broadcast channel. What they mean by broadcast channel is there’s this guarantee that whatever is sent in the broadcast channel every participant knows that every other participant saw the same thing. Because we don’t really have a broadcast channel…

LF: You may or may not depending on your setting.

JP: We don’t really know what we should use for the broadcast channel depending on the setting. There is not some obvious straightforward way to do it. One way of getting the same guarantee, if I want every participant to know that they saw the same thing, each participant signs the commitments that they received and distributes that signature to every other participant. Now if all the participants have a valid signature where they’ve signed the same collection of commitments then they know that they all have received the same commitments. We already need to distribute signatures anyway because of this proof of possession step that we are using to defend against the rogue key attack, we are already distributing a proof of possession. In the FROST paper the proof of possession, they sign some arbitrary message. It is just a proof of possession, it is not endorsing anything in particular. It is just proving possession of the private key. They could sign anything, they just decide to sign the public key. The tweak I am going to make in my implementation, instead of producing this proof of possession in the first broadcast round where you sign the public key as specified in the paper, we wait to distribute the proof of possession until the second broadcast round. We sign all the commitments instead of just this public key and we get the broadcast channel for free. We already had to distribute the signature anyway.

LF: I like that idea. I was thinking of doing something similar. Specifically what you do is you hash all the commitments together and create a 32 byte digest. I think this digest also serves that purpose, it is the thing you can send in your Signal message to the other participants, “This is what I got at the end of the DKG. You guys get the same thing?” They can say “Yes”. That thing is also the thing you sign for the proof of possession. I guess that is another way of verifying. If you get those proofs of possession at least everyone got what they thought they got. Assuming that they were all actually part of the thing in the first round. Everyone who was in the first round got the correct thing in the second round.

JP: Each participant, all they need to do is check that the hash that I signed when I produced my signature, all the signatures I receive need to verify against that hash. As long as that is true we don’t even need the Signal communication.

LF: You need it because you don’t know in the first round that it is the right people. You might be connecting to the coordinator and the coordinator is providing all the shares in the first round and produces proofs of possession for them, he owns them. He sends you everything correctly but you don’t know that the people you are communicating with in the first round are actually the right people. That still needs to be done out of band. The digest is a convenient thing to do both. The thing you can sign, it is also the thing you communicate out of band to verify the first round. Once you’ve verified the first round the second round is automatically authenticated then. I guess it is already authenticated by that check.

## Once we’ve done the DKG can we use that as an XPUB to derive further addresses using BIP32?

(What would go in the second 32 bytes of the XPUB?)

LF: We’ve got this public key. We want to derive addresses from it. How do we go about doing that? We’ve got this fixed public key, you can’t change it. How do we go and practically use it in a Bitcoin wallet? We do BIP32 derivation from it, I guess that’s fine. Is there any problem with doing BIP32 derivation? What would you suggest should be the chaincode of that?

JP: I haven’t really thought about this that much but it is a great question. Anything that is derivable from the public key will work because you can produce a signature from the public key. Beyond that I haven’t really thought that much about it.

LF: We could do BIP32 derivation, it would fit into existing wallet infrastructure. There is nothing to stop it.

NF: You take your joint public key as the extended public key for your wallet that you derive addresses from with BIP 32?

LF: It is not extended yet. You need 32 bytes of something else which could be this session digest or some random 32 bytes that everyone knows. You can make an XPUB potentially. I saw a [paper](https://eprint.iacr.org/2021/1287.pdf) on the security of BIP32, it was less than expected. You cannot prove security. Combining BIP32 with FROST somehow lowers the security? It seems to lower the security theoretically of a single key. I didn’t read the paper yet. I think it is fine.

## What kind of signing structures can we make?

(Can we make a hierarchy?)

LF: What kind of signing structures can we make? Can we make a hierarchy? This is a 2 out of these 3 things but one of the things itself is also A or 2 out of B, C and D. I need a 2 out of 3, it can E and D by themselves or it can be E and A or D and A. Or if A is not available for some reason A can be emulated by 2 out of B, C and D. We can set this kind of thing up with FROST?

JP: This is something I am very excited to explore more. I white boarded it and played around with some proofs of concepts. As far as I can tell these hierarchies work, both with nested FROST structures, you have a FROST key, and each component itself could be split with FROST. Let’s say you have a 3-of-5 and each of those 5 could be a 2-of-4. They could keep splitting forever. The operational complexity of building this signature might get really annoying really fast. But as a theoretical thing I believe it works. The other thing is layering in MuSig. You could build a n-of-n with FROST. One nice thing about using MuSig is you guarantee that it will always be n-of-n. If you build a n-of-n with FROST the threshold can change, participants can change. But a MuSig construction can’t ever change. It has a locked configuration. If you want to lock in these n-of-n’s that are very stable and have these FROST thresholds that are inside the hierarchy as well. The one I was describing before, the 2-of-2 of servers and humans, that’s the MuSig configuration that you always want to be n-of-n, never change, 2-of-2 no matter what. You also get the benefit in MuSig that you have non-interactive key aggregation. If that happens to be useful you get that benefit for your n-of-n instead of using FROST where the setup is way more complicated.

LF: If I have a human 2-of-3 and a robot 2-of-3 I can take the public keys that are generated from these distributed key generations, do MuSig on it and there is an algorithm to sign with the 2 of those 2 things. As long we know about it and we have nonces and so on. Leaving that aside, mathematically that is possible.

JP: Absolutely. For the top level MuSig key that’s made up of 2 public keys. First you build the FROST keys and then you take their public keys and you add them together, that’s your MuSig key. Since the KeyAgg coefficient is a constant each participant can add this extra coefficient in when they sign. It should factor out and everything should aggregate correctly. It is surprisingly seamless how these schemes combine. In all these different ways they seem to be able to transform from one into the other very easily.

LF: Let’s say I have a MuSig 2-of-2 on a Lightning channel, is it possible to do the signing and not be aware that the other party in the 2-of-2 is actually a 2-of-3 FROST?

JP: Yeah.

LF: How does the MuSig2 signing work? You have two levels of nonce delinearization. There is this nonce delinearization that goes in both protocols. By hashing everyone’s nonces and delinearizing the two nonces based on the output of the hash, there is now two levels of this. That all can work together? Can it work together in the same number of rounds? Or you have to figure out what your nonce is going to be in the FROST side and then you have to pass that nonce out to the MuSig side. I guess that’s how it would be. You have to start at the bottom of the tree, figure out the nonces and pass those up as the nonces in the next level of the tree. All the people on the lower level of the tree have to know all the tree above them so they can do the delinearization at multiple levels. They cannot just do it on their own level. They have to first do the FROST delinearization, then know what the other parties’ nonces are in the MuSig one and do more delinearization. I think.

JP: I think so too. There is no paper on this. This is something that I think needs to be formally described. Those details are something that I hope to be able to investigate. Maybe that is something we can work on together at some point.

MF: The key point here is that they are totally independent protocols. Maybe you can have some corner cutting exercises to reduce the number of setup rounds if you try to do some merging of a MuSig and a FROST protocol. Maybe you get some savings by doing something like that but then you also lose the benefit of them being totally separate concerns that can be analyzed separately. You have certain guarantees on both without doing some weird merging of the two.

LF: I think that’s the perfect description of the situation.

## Can we change the signers/devices after the DKG is done?

(Could you take a proactive secret sharing approach?)

LF: Next, a malleability question. You can have these complicated trees of rules. Can we change what the trees are afterwards? Can we do a proactive secret sharing approach?

JP: Absolutely. Proactive secret sharing is a term in Shamir’s Secret Sharing where you want the participants to refresh their shares or change their shares, rotate their shares, without the secret itself changing. There are a couple of ways this is useful. Let’s say there are shares on a set of servers and they are rotating the shares every 5 seconds or every few minutes. Now an attacker has to be within a threshold of these servers within the time duration. They can’t compromise one and then get the next one a few days later. You have raised the cost of attack.

LF: If it has got a threshold of shares it is still going to be able to own the whole thing forever in the future?

JP: Once you get the threshold it is game over.

LF: What you couldn’t do is get one and then on the next weekend hack the next one. The one you had before is now trash because they have updated their secret shares without changing the key.

JP: Exactly.

LF: Everyone has to delete their old keys. The old shares get memory holed and you generate new ones.

JP: You delete the old ones or you overwrite the old ones. You are actually doing a summation. You could overwrite what you already have. Each participant, they create new coefficients except for the constant term. They create new coefficients that they then add to the coefficients they already have in their polynomial. This is another reason why it will be useful to reconstruct the polynomial if you need to potentially from just some keypair at the beginning. Now you can refresh the shares because you create these new coefficients. You add them to the coefficients that you already have. You create new coefficients with zero for the constant term and you evaluate shares with that polynomial. Each participant adds those shares to the shares they already have. Then you’ve added the polynomials together. Now the shares have changed. You can use the same technique to change the threshold because you can add additional higher degree polynomial terms. You can reduce the threshold using a similar technique. You can remove a participant because if a threshold of participants create new shares and they don’t distribute to other participants they could kick out a participant. You can also add a new participant in. There’s a lot of flexibility here.

LF: You can even delete people from your ownership. That’s amazing. You can have a 2-of-3 and if 2 of you don’t like the other guy delete him. You can change it to a 2-of-2 later on. That’s very fun.

JP: Or replace him with someone else.

LF: Without moving the coins, the address is the same. That’s quite remarkable. You can do that with just a threshold of participants? Not all the participants?

JP: Yes.

MF: I am going to have to read the paper, how the pubkey doesn’t change when you are totally revamping all the participants and all their shares…

LF: Listen to what he said. These shares, these coefficients and all this stuff, each person has several coefficients of a polynomial which is just several secrets. There’s one secret that is more important than the other one. That’s the one that determines the key. That one is only one of those secrets. Each party has one of those secrets that determines the joint key. When we are talking about redoing the shares and changing the coefficients we are not changing that one. We set that one to zero so when we add them together it is a non-factor.

NF: The first coefficient, you don’t change that. You are only adding to the later coefficients. Because that first coefficient is where you get your public key and the joint public key as well? From the sum of those?

JP: When the new participants are coming in they are not adding anything to the secret anymore. The random data that made the secret, that was seeded by the original participants. The new participants, they are not modifying that anymore. That is set. As long as you have a threshold of shares that will combine to the original secret then you can keep creating more shares and creating higher degree polynomials or lower degree polynomials. They should reconstruct to the first…

MF: You don’t have to set a limit? One way would be there is never going to be more than 10 participants, we are going to split it into 10 shares. We’ll start off with the 3-of-5 but because it is only a 3-of-5 I’ve got 5 ways of changing it in the future. I initially set up 10 shares. It is even better than that. You’ve got 3-of-5 and you can literally do as many changes as you want as long as you get the agreement of 3 of those 5 parties. You could do thousands of changes in the future.

LF: Add people in, take people out, change whatever you want.

JP: I’m pretty sure that works. This is something I just started thinking about recently and looking at the paper recently, I might be getting it wrong. This is something that is on my to do list to work on once I get this [PR](https://github.com/ElementsProject/secp256k1-zkp/pull/138) merged. To start looking at these modification algorithms, changing the setup, stuff like that. I’m pretty sure that is how it works. Chelsea (Komlo), the co-author of the FROST paper, she has some [tweets](https://twitter.com/chelseakomlo/status/1504114844819079170?s=20&t=a463gxkQjMm4DY-TKnH-6w) about these modification schemes. She linked to a couple of papers about it.

## Signing phase

(One round of nonce sharing, one round of signing. The first round can be precomputed so we can faithfully reproduce the signing experience with existing multisig wallets, we hope!

In order for one round signing to work we have to have nonces from all the signers already. How do we ensure this in a cold storage setting and in a hot corporate/org setting?)

LF: So the signing phase. There is one round of nonce sharing and there is one round of signing, by producing the actual signatures. The nonce sharing stuff is all public data, people sending public stuff to each other, no secret stuff and nothing relevant to the signature at that point or the message. This can be precomputed. Hopefully the fact that we can precompute the first one means that we can have a single round signing just like it exists in current multisig. If we are using a Coldcard we take the SD card with a PSBT and we put it into each device that is signing once. Then put it into the connected device. That same workflow can exist with FROST. But it is trickier to achieve.

LF: We have to have nonces from all the parties before the signing round starts. It is hard to put this correctly. The thing that must happen is that every signer has nonces from every other signer already before they sign. It doesn’t necessarily mean the computer you are initiating the signing on, your phone or whatever, has to everyone’s nonces. It could be that for example the computer writes out to the SD card in the case of Coldcards, a signing session, signing this transaction, this message, whatever. It goes to the first Coldcard and the first Coldcard you put it in decides the nonces for everyone else. That could be a way that it works. But the rule is that every signer needs to have nonces from every other signer before they start signing. How do we ensure this? In a cold storage setting how do we do this? In a hot wallet setting, when the exchange is signing withdrawals, how do we make sure that nonces are everywhere. In the hot wallet case you can do the nonce sharing online but in the cold storage case where humans are going to these devices it is a little bit more tricky. What are the ideas we have around this?

JP: This is a critical component. From a security perspective this is the trickiest part of the system. It is very similar with MuSig where we have to be very careful with handling nonces. A trick that we normally have, the deterministic nonce, is not as useful to us in a multiparty setting. This is equally an issue in MuSig. Blockstream has a great post about this. The problem with the deterministic nonce in a multiparty setting, if Alice generates the same nonce, Bob generates the same nonce and Carol distributes an invalid nonce then you rerun the protocol. Carol is like “Here’s my new nonce commitment”, Alice generates the same nonce, Bob generates the same nonce but now they’ve signed something different. You’ve induced nonce reuse through the determinism of the nonce. Now under multiparty settings determinism, what used to be your friend, now becomes your enemy. You have to be very careful about not reusing nonces. When you pre-generate nonces the biggest problem is can you by mistake or get tricked into reusing one of the pre-generated nonces? How do you know the nonce hasn’t already been used? One thing is when the nonce is used the participant should delete it. It is very important that it is deleted even if the signing round fails or doesn’t succeed. As soon as the API is called the nonce should never be used again.

JP: Another thing that comes up a lot is using a counter. If you have some pre-generated nonces you have some monotonically increasing index. We use number 1, number 2, number 3. A big downside of that is that it is stateful. You have to keep track of the state, what happens if the state is lost? Then you have synchronization issues. This is something Lloyd has some cool ideas about how to address. If some subset of participants have participated in a signing round the remaining participants are not necessarily aware that that subset used some nonces. If they have their own index of nonces that have been used they have to find out when the other group uses theirs. Lloyd had the idea that each combination of participants should have their own separate list.

LF: That is what I’m going with. Every person who could initiate signing has to have a totally independent set of nonces they use for each other participant. There is a bit of keeping track of which ones I’ve used for other people, which ones I’ve used for myself, which ones other people have used for me. If I’m asked to sign with a nonce that I’ve pre-generated I have to remember that I’ve already signed with that nonce. There is nothing to do in that case, you just have to remember. This is not an impossible engineering task for a wallet or for any setting, to remember a bit of data. If you forget it we are not talking about losing funds here. We can forget this nonce stuff and we can go back to some fallback mechanism. This could be that we do a single signing with the keys in the Tapscript. If we needed to guarantee single round we could also in parallel do my FROST signature and my signature in the Tapscript. If all goes to hell you’ve done your signing on your Coldcard at home, you’ve taken a flight to another city where you have a Coldcard in a storage locker, in Zurich or whatever. You’ve got your signature half done and your nonce has already been used, somehow this happens, you can always revert back to that Tapscript threshold. Of course this means we cannot do the changing of all the thresholds, all the fun stuff we talked about. Perhaps that is not appropriate for most multisigs. I think the answer here is you just have to have lists and lists of nonces for every single participant. I think what this boils down to is you take every signing device and each signing device has the nonces for every other signing device in the threshold. I was thinking of playing with the idea of having the designation of an initiating device, the one you will typically initiate the signing from. This is the case in all settings really, you have a particular laptop that you initiate signing from. If you are not using that laptop you fallback to the 2 round protocol or the Tapscript protocol. It would be good if you could just initiate from anywhere. The thing that is common to every signing session, it will have at least one but usually more of these signing devices in them. The signing devices carry round nonces for every other signing device. Then you are always going to have nonces and with a single round protocol, pure FROST, almost all the time. It shouldn’t be too difficult to hide this fact from the user, I hope. Any other ideas?

MF: Why do you care the reason a certain nonce was used in the future? Every party has to have independent sets of nonces. But even within an individual party if they want nonces for different uses, those lists should also be independent. Surely no one should care why a nonce was used or for what purpose a nonce was used previously. All they care about is that it was used previously and they should not use that nonce again.

LF: That’s correct. There’s no purpose attached to the nonce. I was thinking that there could be a difference between signing devices and signing initiating devices. The signing devices could have less data having to be stored on them. You could have this designation, “This device can only sign. It cannot start the protocol.” But I think it makes more sense, at least for the beginning to say that every signing device is a device that you can start the protocol from. That is where I’m headed with it.

MF: I think you want independent lists of nonces everywhere. Whether that is split between users or split between use cases of that user.

LF: My device has a list of nonces for every other device that isn’t part of the possible signing set. Every device has that. Let’s say I plug it into my laptop, my laptop says “We are going to sign this message”. That device I’ve plugged in or put the SD card in from can say “Here are the nonces for each of those parties that are about to sign with.” There is no way that those nonces could be on someone’s list or be already used because I’m keeping track of when I’ve used those nonces. As soon as I give them out, let’s say the laptop starts the signing, I delete them or I increase a counter, “I’m never going to use them again no matter what”. When that bit of information that defines the signing sessions gets to the other devices it says “This is the guy who initiated the signing session and this is the index it chose for you to use a nonce at”. You re-derive that nonce, you check it matches the one you were told to use, you say “Yes ok. I am going to sign”. There should be no conflicts here. The only thing that can happen is you can run out of nonces. Each signing device may run out of nonces for any other particular signing device. It may run out of nonces for one faster than the other, this could naturally happen if there is a more common subset that sign. This is the main thing that I want to tackle now. How do we replenish these nonces? How do we replenish the nonce supply of a particular device?

## How do we replenish the nonce supply?

LF: It seems like you could naturally update the nonces by having each party who consumes a nonce from the initiator’s nonce list provide a new one at that point. “I am signing, I am extinguishing this nonce and I have got a new one that you can add to your list.” If it is a SD card in the case of a Coldcard kind of device, when this SD card comes back there is a directory that has already been populated with new nonces. At some point in the future that initiating device can read from that and insert it into its own nonce list. These new nonces can also be signed by the key that defines that device so you know it came from them.

JP: The participants who were not in the signing round, they have to at some point get the new nonce commitments that were generated.

LF: No they do not. They each have their own. It is only the initiator.

JP: None of theirs were depleted. Ok, yeah. This is another area where MuSig interoperability rears its head. MuSig and FROST nonces are almost exactly the same in their structure. They are actually fully interchangeable from an algebraic perspective. In my implementation I am sticking with the paper for now. What is on GitHub right now uses MuSig nonces because it simplified my code. But it is something to be aware of. If somebody comes up with a clever solution for MuSig nonces in hardware or in software and we want to leverage that in FROST it is very easy to do that. Also if somebody has some big pool of nonces that they want to use for both systems and be able to draw upon the same pool of nonces, that is totally possible.

LF: In our first hacked together thing Nick and I did, we did the same thing as you. We used the MuSig2 nonces. I believe that if you look at their paper that proved FROST the same proof applies to MuSig2. It may be worth getting in touch with the authors about that. I know that they have a IRTF draft specification for FROST that I will post on the last slide. They are doing work on the specification for FROST on other curves. We can potentially insert this into that conversation. We should see if we can extract as much value from that specification effort for this one.

MF: Why does there have to be any coordination on nonces? Why can’t every device have an independent nonce generator on that device? Why does a coordinator need to know what nonce one of the devices that it is coordinating is going to use?

LF: There is no need for a coordinator at all.

MF: There could be independent nonce generation on every device?

LF: Yes there would be.

MF:  And hence there would be no monitoring of which nonces are being used because everyone is independently generating their own list of nonces.

LF: You can generate your own ones but you need a list from someone else. You cannot ask someone to sign with a nonce you’ve generated. When the SD card arrives at your Coldcard it needs to be able to generate the nonce you’ve told it to sign with. That Coldcard needs to have communicated a list of nonces to whoever is initiating the signing, this could be another Coldcard, a laptop whatever. That person who is initiating the signing “This is the message we are going to sign. Here’s the parameters for the signing.” That gets written onto the SD card. When that SD cards arrives the Coldcard needs to say “Yes ok I’m using that nonce for this signing session. That’s fine. I know how to derive that one.” You generate them independently but you need those independently generated lists to be shared with everybody else. They each need to be independent for everyone else. You generate independent lists for each other signer. That’s the way I imagine we would solve this. It seems to work. It is definitely guaranteed secure from the protocol proofs. There is nothing wrong with it. And it also has this natural replenishment mechanism. As soon as I extinguish a nonce I can add a new one and hopefully that gets communicated, depending on how the application organizes that, eventually back to all the initiating devices. All the initiating devices that I extinguished a nonce from.

MF: A Coldcard can’t generate nonces.

LF: Right now it generates nonces for signing ECDSA signatures. For every signature it makes there is a nonce in there. These don’t need to be shared. These are generated at the signing time inside the Coldcard using deterministic nonce generation from the message, the secret key and the public key I guess. It just needs to do that same algorithm or a similar algorithm and share them with everyone ahead of time so we can generate the signature together. That’s the problem we are solving.

JP: The Coldcard can just run SHA256 for ECDSA to get a deterministic nonce. But for FROST it needs good entropy. It can’t just use SHA256 and rely on the entropy that was already created in the private key. It needs fresh entropy every time it generates a new nonce.

LF: You don’t need fresh entropy? You can use deterministically from your secret key. Just have a counter or whatever.

MF: It creates tracking problems. Upsides and downsides.

LF: If you are going to get single round signing you have to accept the tracking problems.

JP: What do you do if the counter resets or you lose the saved counter.

LF: You can’t.

JP: You’re screwed.

LF: If something happens to it it deletes the Coldcard. It has to be so secure. Hardware has this requirement. You have to store the PIN in such a way that the PIN is there but if anything changes to it it cannot work anymore. I think this is not an extra requirement that hardware cannot accomplish although I don’t build hardware and don’t design hardware.

JP: I’m not sure how good the Coldcard’s tamper resistant mechanisms are. I know on some of the more higher grade Yubico HSMs, they have tamper resistant functions. This is a whole rabbit hole of can you even make an unhackable HSM because they all seem to get broken one way or another. That’s a whole separate topic. If these are not air gapped and they can do network calls and you don’t want to get into the problem space of pre-generated nonces you can just generate them fresh on demand when you need a signature. That’s a perfectly acceptable way of doing it if you don’t need the pre-generation.

## Accountability - can we tell who spent the coins?

LF: Can we get accountability in this scheme? Let’s say I’m a participant in a 3-of-5, I’m in the Sydney office, some guy is in the Singapore office and there is a guy in the New York office. I can get accountability on who spent the coins from the address that we jointly own. I didn’t authorize that transaction. Obviously in that case it should be the other two. Let’s make it more interesting, a 3-of-6. Can you get accountability in this protocol?

JP: I don’t think we can get it at the cryptographic protocol level. Obviously there are other ways people leave traces and there are other forms of forensics that can be used. If this is a cryptocurrency exchange for example it would be very difficult to conduct an operation without it moving through networks and logs and stuff. But at the protocol level I don’t know of a way to get accountability. Of course the flip side of that is this is what makes it so private. You can’t tell who participated. There are definitely contexts in which accountability is useful. I have heard that some of the reasons people don’t use a threshold signing system like FROST is if they really need strong accountability. This is not a good use case for that.

NF: I was speaking to someone about FROST at the weekend. They were wondering about FROST being used in a company board of directors situation. This is a dealbreaker for him almost. People could collude within the signers and sign something. You wouldn’t be able to go and check who were the corrupt ones, who signed this message. You couldn’t blame people in the group. I think Lloyd had some ideas for some way you could fingerprint signatures but it would be opt-in.

LF: There is a way of fingerprinting signatures in a clunky but will work way. We do some kind of rejection sampling on our nonce values. Once we’ve figured out all the nonces… Let’s say we have a setting where we have honest hardware devices but dishonest people. Some guys are stealing money from the company but they have to use their hardware devices to steal it. Each hardware device has a single share of the total key. They need a 3-of-5 to spend the coins. These hardware devices are working and they are not hacked. Those humans who have control of these hardware devices are using them maliciously to spend the coins somewhere else. These hardware devices could enforce in their nonce that it leave a fingerprint, a certain pattern. When you hash the aggregate nonce together the last bits indicate which of the signers were in the thing. These honest devices when they get told what they are signing, they will know who are the other signers. We can enforce that. The other signers we know from the nonces that were used. Or we can have a signature saying “Yes I want to contribute to this signature here”. As long as there is one honest device amongst them, that honest device can say “These are the people signing”. That means when I generate the aggregate nonce, it is not exactly going to be the aggregate nonce I would generate. I do generate that one but I keep adding a single thing to the nonce with a known discrete logarithm until the hash of it with some particular hash has a bit pattern that matches the signer’s. It has 1s in the bits that correspond to the signers who are demanding that this signature be made. The dishonest persons who own these devices could not stop the hardware device checking for this. It is hardcoded into the hardware device that they check this thing. Each of those devices is going to take the aggregate nonce, can rejection sample until it finds a joint nonce that matches that pattern. When the signature is broadcast the aggregate nonce will when hashed have that bit pattern in it. What this allows you to do in this case, the honest participants who have their funds maliciously spent will be able to say “It was these guys”. Assuming the hardware cannot be tampered with they can prove cryptographically under that assumption it was those guys who did it. Also this doesn’t reveal any information to anyone else. If you hash it so that some secret information is only known to the parties. Perhaps it is this session ID we talked about, this digest we talked about before. Something that defines all the signers, the hash of all the signing keys whatever, goes in there. To everyone else it looks like a normal nonce but to the devices that have a part of the signing set it will be able to deterministically tell that this was from these parties. What do you think?

MF: It sounds like you are relying on malicious parties following an out of band process. Perhaps they will follow this honest process every time until they do the malicious activity in which case they won’t bother to follow this out of band process.

LF: It relies on honest hardware.

NF: There could be a fork of whatever protocol that doesn’t enforce this. Your FROST repo that adds a fingerprint, someone could fork it and use this repo to steal funds.

LF: But the hardware device has it on the firmware.

NF: It would be the same for the hardware. Someone could buy hardware.

LF: We are assuming honest hardware here. Malicious parties but if the hardware does this protocol they will leave the fingerprint whenever it generates a signature.

NF: It would stop unsophisticated attackers but the sophisticated who understand what to do, they would probably be able to steal it.

LF: If they can break the hardware.

NF: When you say hardware, couldn’t they just do their signing on different hardware? I don’t understand what you mean by honest hardware.

RS: It is a trusted device. It is like a HSM.

JP: You can’t extract the secret from the device.

RS: Does this assume that the HSM is a part of the threshold that always has to sign? Or is it still a 7-of-10 where 1 of the 7 is the HSM? Because then you increase the threshold by 1. You just need more malicious parties to avoid the HSM. That would be one way around it I guess.

LF: In the example I gave this is a corporate example and every guy who can sign has this hardware device. We are assuming those are honest. Your point is correct, it needs at least 1 honest hardware device as part of the malicious signers’ set in order for that thing to work. If some of them are hardware and some of them are owned on devices that could be corrupted let’s say, if that’s the case then yeah this doesn’t work at all. The downside is that you could put a fingerprint that is invalid. You could leave the fingerprint that implicates somebody else.

JP: Right.

RS: Another thing in general about HSM use is not everybody is comfortable using it. If everybody uses the same HSM and they all fail for the same reason no matter what your threshold is the HSM is the weak spot. That would be one thing to think of. That was the model you had in mind. I thought maybe have one HSM that is always required. You have a threshold but one person always has to sign. Then the HSM also becomes the weakness. I do think it is interesting in principle that it is possible.

JP: You can do a similar model with the humans and the servers, the 2-of-2. If you have a set of servers that you trust to enforce some set of heuristics or some set of validations where they just refuse to sign unless they got attestations from everyone who was signing on the other side. Assuming you can trust a threshold of these servers to enforce those things, that’s the cloud equivalent of having these HSM enforcements.

MF: You only need the accountability feature though when there is a sufficient number of malicious parties. The whole point of accountability is funds are sent, you don’t know who made up the threshold to send those funds somewhere else. But you only care who did it because something malicious has gone on. In which case you want to identify who the malicious parties are. If you have a sufficient threshold of malicious parties they are going to try to avoid any notarization or any following of out of band processes, protocols.

JP: If they are part of a 2-of-2, if there is a threshold that is one of two keys. Even if there is a threshold of malicious parties on one side they still need the other side to sign to get the full signature. That’s where if you have some servers or some other thing that can enforce some rules on this side of the key. You are kind of pushing the security model in a way. If you have pretty good network infrastructure and a good security story around your servers, how they are deployed, how they can be accessed, you have cloud HSMs. That may be able to give you enough assurance that you’d get good enough accountability. Or the key just won’t be able to sign. It would just refuse to sign. But it is very context specific.

LF: I think it is an attractive idea for many settings but not for others. Let’s say we have this honest hardware, a payment shouldn’t have been made but did you follow all the steps you were meant to do before you made that payment inside a business environment? Or let’s say I break the rules a bit and I make this payment early to this counterparty for some reason. We want to get the money in there early. No one will be able to tell who it really was. They will just point figures at us later on even though it wasn’t malicious. We were not following the protocol properly. It is nice that that fingerprint is always there for those unsophisticated users who are given this power to spend funds that can’t attack HSMs. They know that they will always leave a trace about what they did on the blockchain. The organization itself will be able to audit who did what at a later date in case those transactions are not identified as malicious or semi malicious in a grey area. There are a lot of grey areas that occur in crypto organizations. Maybe that can be audited later on. When something like Mt Gox happens in a different way, when the auditors and liquidators come in they are not told different stories by different people. That accountability is there, we can tell on every transaction which devices were part of that thing. You can never hope to weasel your way out of accountability or responsibility for transactions within such an organization. I think that’s where it makes sense.

RS: That does assume that you don’t need a HSM because everybody is acting non-maliciously. You don’t even need the HSM in that case.

LF: You do because otherwise how do you keep a track of who spent the funds?

RS: You follow the model that you said you should follow. Because everybody is acting non-maliciously everybody does the whole nonce thing that you described.

LF: Yeah you need to be following the protocol somehow. Even an unsophisticated person can install a different signing thing on their laptop, a fork of whatever.

RS: But then they are malicious. Or dumb I guess. That’s also possible. In the sense that they are trying to avoid the fingerprinting which is mandated by your company.

LF: I guess that is a good thing to have enforced without having to rely on the honesty of the individual party.

RS: I don’t disagree. But your example, imagine people are not being malicious but accountability is still nice. That was your example. I am just saying in that example the HSM is not necessary. I agree that you might as well have a HSM.

LF: Yes. Not strictly necessary from a security model point of view. But from a practical point of view it is nice to have that guarantee. As you said having HSMs in an organization, the same type of one that does the same thing is a risk in itself that has to be considered very seriously when you are starting this setup.

NF: The more I think about it I actually quite like Jesse’s solution. What if every participant was in a 2-of-2 with the other person being a trusted company server. Every time you go to sign you have to let the company server know that “I’m signing”. That will leave a record.

MF: When I see accountability in this multisignature setting I see it as “When you see a signature onchain can you determine how that signature was constructed?” The answer is no. You are going to want secure company processes, you are going to want audits, you are going to try to encourage everyone to follow correct procedures etc. That is a way of out of band trying to work out who did what.

LF: You can look at the blockchain and figure out which set of participants signed it assuming secure hardware, with a security assumption.

MF: But you are not getting that from what is onchain. Isn’t the signature identical even if different participants have signed?

LF: There is a bit of randomness in the signature, the nonce and it is different for every message. It is not deterministic, it is random. And it can be used to leave a trace in the signature itself.

MF: I see that as an external process rather than an observing the blockchain process. Because in theory someone could just not use that hardware, create their own hardware, use whatever nonce they are supposed to use or a different nonce.

LF: In theory yes but in practice it could be a useful tool.

JP: It is definitely an interesting idea. All of these ideas are ways of getting something less than a pure protocol level solution but depending on your model or your use case might be sufficient.

LF: Yes.

## Q&A

LF: There is a [draft](https://github.com/cfrg/draft-irtf-cfrg-frost/blob/master/draft-irtf-cfrg-frost.md) IRTF, internet research task force, for secp256k1. It is going to have to be modified quite a bit by us to apply secp256k1. I did see before this they want to include secp256k1 in the specification. That is a GitHub [issue](https://github.com/cfrg/draft-irtf-cfrg-frost/issues/69). We might leave a message about that. It would be great if they could incorporate the x only keys to make it relevant to Bitcoin. Otherwise we’ll have to make a BIP or something to do it. That’s the state of art in FROST everyone.

RS: Could you go over how signing would work with polynomials? Let’s say in a 2-of-3. Describe the steps for me similar to what you did at the beginning talking about polynomials. I’m interested because I’ve been trying to hack together my own implementation of polynomials. I am interested in how that works.

JP: The nonces are just additive nonces, they are not polynomials. The nonces are the same as MuSig nonces. A simplified version, each participant generates a nonce, each participant generates a commitment to their nonce, they distribute those commitments and your nonce round is done at that point. Keep in mind this is really only among the participants that are signing which is a subset typically of all the total participants. In key gen all the participants were participating. Now in the signing round only the subset who are signing, they send these nonce commitments or they have them pre-generated where they just send some index around saying “I’m using nonce index 1, 3” or whatever it happens to be. Then you have a Schnorr signature where the challenge hash has the message, it has the aggregate public key and it has the aggregate nonce public key where you’ve added all the nonce commitments together to get the aggregate nonce. Same thing as MuSig so far. Then each participant generates a Schnorr signature where they sign with their Shamir share, polynomial share. If the Schnorr signature is `s = r + cx`, x is the private key, they replace the private key with their Shamir share.

RS: The Shamir share is a polynomial in itself no?

JP: It is a y coordinate. When they evaluate these polynomials each participant has an index, Alice is 1, Bob is 2, Carol is 3. The polynomials are evaluated at that index, they get the y coordinate and then they aggregate them. They get this aggregate y coordinate.

RS: Does everybody have their own degree? How are people divided in the polynomial?

JP: The degree is equal to the threshold minus 1. If your threshold is 2, let’s say you have a 2-of-3 set up then you need a 1 degree polynomial. We know this intuitively because we know that for any n points there is a n-1 degree polynomial that is uniquely defined by those n points. For example if you have 2 points there is a single line. 2 points, 1 degree polynomial. 3 points, 2 degree parabola. Each participant created a polynomial. They evaluated shares for each other participant. They aggregated them and so they each have a y coordinate that is a share of a polynomial that is the sum of each participant’s polynomials.

RS: You add all those y coordinates together that you get from everybody right?

JP: Yes. And when you go to sign each participant signs with that aggregate y coordinate, their respective aggregate y coordinate. They sign with that instead of the private key. Here’s the extra trick. They also multiply it by the Lagrange coefficient. From Shamir’s Secret Sharing when you have the Lagrange coefficient multiplied by the share, for a threshold of participants when you sum up the product of those quantities, `lambda_i` times `x_i`, the sum of that `i` to `t` all interpolates to the secret. What happens when the partial signatures are added together you have these Shamir quantities multiplied by the respective Lagrange coefficients. Those sum together and cleanly interpolate into the private key. You have `s  = r + cx`. The `c` value is constant. It stays the same. Then the `r`’s are additive, they are not polynomial, they are additive nonces where the nonces add together. Alice’s nonce plus Bob’s nonce plus Carol’s nonce. Simple addition. That’s how the signature equation comes together.

RS: Basically you take your y coordinate which is the addition of all the shares that you receive from all the participants, you use that in the Schnorr signing scheme and then you multiply the result `s` by your respective Lagrange coefficients. You add all those together and you get the final signature.

JP: A slight modification, when you perform the partial signature the participant will multiply their aggregate y coordinate by the Lagrange coefficient. Rather than multiplying the partial signature by the Lagrange coefficient. If you multiply the partial signature by the Lagrange coefficient the Lagrange coefficient would distribute through the signature so you’d have a coefficient multiplied by the nonce and multiplied by the private key. You just do it inside. For whatever reason if you wanted to create nonce polynomial shares instead of additive shares then you could do it the other way. You’d want it to distribute through. That’s how the pre FROST schemes actually did it. If you look at the older papers they did that way.

RS: Thanks that was very helpful.

MF: There’s this [blog post](https://blog.coinbase.com/frost-flexible-round-optimized-schnorr-threshold-signatures-b2e950164ee1) from Coinbase that said they are using FROST. I am assuming they haven’t open sourced anything? Is it following a similar approach to what you are doing with your PR? Do you know anything about that?

JP: Before I was working on FROST I was at Coinbase building their threshold system. We were building that before FROST was published. We were doing the precursor to FROST. I was on the team that built that at Coinbase. Then I left at Coinbase and now I am doing open source stuff. Then they updated their system, they already had something very similar, but they updated it with the new tweaks that FROST adds. They have open sourced some of their stuff. They also built a threshold ECDSA system which is much more difficult to build and has a lot more rounds. They might have open sourced some of their FROST stuff, I’m not sure.

LF: FROST on BItcoin?

JP: They might be. The whole strategy was about making it so that instead of having these different signing systems for each currency, from a scalability perspective it is not as good as having a signing system for each signature type and curve type. If you have a threshold system that supports all secp Schnorr across any currency that supports secp and Schnorr then you’ve covered that. It is about scaling their systems. That is one of many considerations that goes into these types of things.

LF: That would imply Coinbase are using SegWit v1 addresses. Can you even deposit to a SegWit v1 address?

JP: It would have to be Taproot addresses. It has to be Schnorr. They are probably not using Bitcoin.

LF: If we were working on a precursor of FROST at Coinbase it wasn’t used on Bitcoin unless you were using ECDSA?

JP: No it wasn’t at the time. I was just speculating on what it might be doing today.

NF: I doubt it would be doing hot wallet withdrawals with it purely based on what Lloyd said. There are not many Taproot addresses being used. They could do something like cold wallet to hot wallet withdrawals with something like FROST, that could be possible.

MF: At least on the date of the blog post which is October 2021 it sounds like it is just a proof of concept. They are not actually using it in production. It says “We look forward to adding it to our suite of threshold signing services”.

