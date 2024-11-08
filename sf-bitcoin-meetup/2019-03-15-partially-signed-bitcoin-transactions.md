---
title: Partially Signed Bitcoin Transactions
transcript_by: Caralie Chrisco
tags:
  - PSBT
date: 2019-03-15
speakers:
  - Andrew Chow
media: https://www.youtube.com/watch?v=H6xZSRDXUiU&feature=youtu.be
---
## Introduction

Andrew: So as Mark said I'm Andrew Chow and today I'm going to be talking about BIP 174, partially signed Bitcoin transactions, also known as PSBT. Today I'm going to be talking a bit about why we need PSBTs, or Partially Signed Bitcoin Transactions, what they are, and the actual format of the transaction itself and how to use a PSBT and the workflows around that.

A quick story, around this time last year there was a fork of Bitcoin and I had some fork coins on a Trezor and I wanted to get these fork coins off my Trezure so I could sell them obviously. I wanted to do this locally and securely so I was going to use Bitcoin Core and Electrum. I figured this would be easy. It would be a pretty standard process that you do for signing offline transactions with Bitcoin Core. You just create a raw transaction, I bring it to Electrum, sign it using the Electrum Trezor plug-in, bring it back to Core and broadcast it to the network. So I went to do this and I created a raw transaction and brought it to an Electrum and I saw this problem. It says that the transaction doesn't belong to my Electrum wallet.

Back to this story, Electrum says this transaction was not related to my wallet. It definitely was. I assure you this transaction was related to my wallet. It also says the transaction is signed but according to Core that's definitely not signed. The scriptSig is completely empty. I spent a long time trying to figure this out, many hours reading through some documentation that wasn't very clear and reverse-engineering Electrum's transaction format. I finally figured out what the problem was.

### The Problem

Bitcoin Core will create a transaction that does not have anything in the input scripts but Electrum expects to see things in these input scripts. It actually expects to see public keys. That's how it identifies whether a transaction is in that wallet so that I can sign. Obviously the transaction I gave it from Core did not have this information and the result was that electrum and Bitcoin Core were completely incompatible with each other if you try to do raw transactions and that is really the only way you can even try to interact these two together. There was this problem and there were some other problems with doing raw transactions.

For those of you who don't know, raw transactions actually require more data than just the transaction and the private key itself in order to sign that transaction. We need some extra data like the previous transaction or the output script of the outputs that are being spent.  We need redeem scripts and we need to know what keys are being used to sign this transaction. And to do this in Bitcoin Core you have to provide this out-of-band in the command and you get a command that looks like this. It's a lot longer when you have many inputs and it's hard to get right and it's hard for relatively new users to even know how to do this and get it correct.

So in this example you’ll see -

Audience Member: Users too.

Audience Member: People who wrote the software, too.

Andrew: I make a lot of JSON errors.

You can see highlighted, that's the extra data that we have to provide: it's the previous transaction the scriptPub key which is the output script in the amount and if this was P2SH we'd also have to provide the redeem script. I found this to be a problem. It’s annoying to take things across wallets and we obviously need more data than just these raw transactions. So I decided I was going to create yet another standard.

### Another Standard

Now this is not quite just another standard. It's actually I would say the first standard for having a transaction format that contains everything that's needed for signing. This is actually well specified unlike the current formats that are used and it solves a problem of the incompatibility because it's a standard, obviously. It's also actually being used by some other software already. Of course this standard is Partially Signed Bitcoin Transactions.

Some information about the format itself. The transaction is what we call “partially signed” which may be a misnomer if we include Schnorr signatures in this, but let's ignore that for now. What I mean by partially signed is that the transaction, what we call fully signed, is something that if you broadcast it to the Bitcoin network it would be immediately accepted by the network ignoring lock time. This means that the transaction is fully signed because it has a full set of signatures and all of its inputs. So partially signed is everything up until that fully signed state. Not all the inputs have all their signatures. They may even have no signatures at all and if none of them have their signatures, that’s unsigned, which I consider still to be part of this partially signed state.

The partially signed Bitcoin transactions are for the state where the transactions are not fully signed yet and so these transactions consist of the raw unsigned transaction itself followed by metadata for each input and output. This data is everything that is needed to sign. It's everything needed to know what you are signing is actually what you intend to sign. It is everything that you need to know in order to sign the transaction. It's also everything that you need to know in order to construct the final transaction at the end when you have all of these signatures. Of course this doesn't include the private keys because that would be kind of pointless.

The format also holds all these signatures as is indicated by this partially signed name and I've also designed it to be easily extensible so that we can extend it in the future in order to support new things such as Schnorr signatures.

This transaction form, we can visualize it in a bit of a diagram like this. We have some header bytes that are just magic bytes. We have this unsigned transaction which is actually part of a set of global data and if we look into this unsigned transaction a bit we also notice that the unsigned transaction has a header, a list of inputs, and a list of outputs and the inputs in this unsigned transaction map directly to inputs in our PSBT. You see we have our input in the unsigned transaction maps to an input in our PSBT that just comes after our global data. We do this for every input and every output. We end up with global data which has our unsigned transaction followed by a list of inputs and all the metadata associated with those inputs and then a list of outputs and all the metadata associated with those outputs.

If we dive a bit deeper we have the actual format on the very low level is a set of typed key value pairs. We have the map, we have the set of Global's which we can really call a map is just key value pairs, or it's a map or a dictionary. We have the map for the globals, a list of maps for the inputs and a list of maps for the outputs. Writing this as a struct we get a transaction, list of inputs, list of outputs and we also have some unknown things that I'll get to later.

For our inputs, the data we include in the input is a UTXO of the the output that we're spending, the sighash type that we want to sign with, redeem scripts, signatures themselves, public keys and their BIP 32 derivation paths for this input, the final scriptSig and also a few unknowns. They're actually SegWit variants for the UTXO, the final scriptSig, and the redeem script because SegWit has some slightly different semantics.

For outputs we have redeem script necessary to spend the output and public keys necessary to spend the output. The reason we actually have the outputs is so that we can verify that where we are sending the coins is what we actually intend to send the coins to. So we can check if we're sending to a multi-sig that we're actually sending to a multi-city with the people we thought the multi-sig is part of. It's also useful for identifying our own change.

So for these unknown things, those unknown things are so that we can easily extend PSBT in the future. Because the PSBT is a set of typed key value pairs we can add new types for new key value pairs and the unknowns that we have is because we can view a set of key value pairs as a map, we just have a map of keys to values of things that when we do serialize we don't know what their type is. Not everything needs to understand all the types that are available. You can ignore some of them and still understand and even some roles that we'll get to later don't have to understand types at all. So a signer also doesn't need to understand some types because they can still produce a valid signature using the information that they know and at worst a signature will just be invalid and you can't use it. Those are the unknowns highlighted for each of the different scopes.

## Roles

Here's an example using a 3-3 multi-sig. For those of you who don't know what a 3-3 is, you have three people and all three of them must sign the transaction in order for it to be valid. So let's say in our 3-3 we've got Alice, Bob, and Carol, which in my slides they will be color-coded. Alice is red, Bob is grey, and Carol is green. Let's say Alice wants to make a transaction, so she'll talk to Bob and Carol and figure out what inputs to spend and what outputs they want to create and she will create a PSBT. This will be completely blank. It just has the raw unsigned transaction and empty maps for the inputs and the outputs.

Then Alice says if she has a node but her wallet doesn't know all the Redeem squares are public keys for the inputs but she has a node so she will add the UTXO information to this PSBT. Then because she can't do anything else with this, she's going to give it to Bob. Bob has the scripts and key information. Bob was going to add these scripts and keys to the PSBT. Now all the inputs have all the information needed to sign. It has the UTXOs, it has the keys, the public keys and it has the scripts. So Bob sends this PSBT to Alice and Carol and Alice and Carol are going to sign this transaction using the information provided. And if say Carol has an offline signer she can take the PSBT as it is, straight off her online computer to the offline signer and sign it there without having to add any extra information. She can bring it back and the PSBT she brings back will have her signature inside of it.

Once Alice, Bob, and Carol have signed the PSBT, say Carol is going to be the one that broadcasts. They all send their PSBTs to Carol. Carol is going to combine the PSBTs together into one new one that has all of the signatures that Alice and Bob and Carol created. This combined PSBT then will be used to construct those final scriptSigs. Using the signatures and the keys provided, Carol can produce the final scriptSigs that will go into the network transaction. Lastly Carol is going to use those final scriptSigs and make that final transaction and then broadcast it to the network. So all of this is done with PSBT and various software.

Alice, Bob, and Carol didn't really have to input anything extra except their private keys and usually the wallet software handles your private keys for you anyways. This can be broken down into different roles and these are defined in BIP 174. As a side note, these multiple roles don't have to act independent of each other. Multiple roles can be implemented in one entity in the software.

So in this example our first role is the creator. In this case the creator was Alice because she created the transaction obviously. The next role is the updater and in this case this was both Alice and Bob because they updated the transaction with new information. They updated it with the metadata needed to sign. The updater, it could be split like this, you can have multiple, or it can be just one person that happens to know everything. Then we have signers who sign the transaction and this was Alice, Bob, and Carol. They all performed signing. Then we have the combiner which was Carol. The combiner is very simple actually as I mentioned earlier. The combiner doesn't need to understand all the types, it just needs to merge all the maps together and make sure there aren't there aren't any duplicates. You can just shove everything back together. Then we have the finalizar which produces the final scriptSigs that will eventually go into the final transaction and we have the extractor who takes those final scriptSigs and produces the final transaction and kind of looks like it's extracting the transaction out of the PSBT. The extractor is also the one who likely broadcasts the transaction to the network.

## Other Use Cases

So there are other use cases besides multistage. We can use this for CoinJoin, we can use it for hardware wallets and we can use it for offline wallets as I mentioned earlier.

So actually go through an example using CoinJoin because this shows how you can use this without everyone having to update their inputs for everyone else. For those of you who don't know, a CoinJoin is where multiple people participate in the same transaction. The inputs of the transaction come from multiple different people.

In the first step of the CoinJoin you're going to do some CoinJoin protocol. This could be like Join Market, Coin Shuffle, or Zerolink. But somehow some protocol happens where everyone figures out what inputs and what outputs they're going to use in their transaction. Then whoever is coordinating that CoinJoin let's say in this case it's Alice again. She's going to use the information from the CoinJoin protocol to create a PSBT. Once she creates it, she's going to send this PSBT to Bob and Carol. It's going to actually be blank and have no information on it. Alice, Bob, and Carol are actually all going to update their PSBT separately with their own UTXO information and their own key and script information and then they're also going to sign it themselves.

In this example Alice, Bob, and Carol don't actually see the input information from the other participants in this CoinJoin. But using PSBT if one of them has a hardware wallet or an offline signer after they update the PSBT they can take it to their offline signer, sign it there and bring it back without having to enter any additional information. Once this is signed, then they'll send it all to Alice again and Alice is going to combine everything. Once Alice combines the PSBT she will also finalize it and then extract it using the same process that I described earlier and eventually the transaction is broadcast by Alice to the Bitcoin network.

## Where Can I Use PSBT?

Lastly - where can we use PSBT? Well right now PSBT isn't really in production but it has been merged into Bitcoin Core 0.17 which is going to be released hopefully in September. There you'll be able to use PSBT with a variety of RPC commands that have been implemented into it. PSBT has also been implemented into the ColdCard hardware wallet created by CoinKite and they use PSBT natively where its whole communication thing is based around passing back and forth PSBTs from your computer to their hardware wallet. They currently have a simulator I think they're shipping soon. Of course there are libraries and other wallets that are implementing PSBT. There are a few libraries and wallets that are in the process or are very close to finishing their implementations of PSBT.

That's it. Any questions?

[Applause]

## Q&A

Audience Member: Since Electrum implements their own little thing using Bitcoin transactions like you mentioned before, have you heard any feedback from them if they're planning on supporting this yet?

Andrew: No but I know people that are going to implement it into Electrum.

Audience Member: Okay.

Audience Member: So for transmitting the PSBT's between people, you're basically like supposing that we use email or some other like third party communication system?

Andrew: Right, the BIP doesn't specify how you're going to get PSBT's to people. It’s just describing the format of the transaction used. So you could use email, maybe it'll be supported in the payment protocol or something. I don't know.

Audience Member: It seems to go be really cool to have some sort of like solution for people to communicate as well.

Andrew: It would.

Audience Member: Because you're opening up the signing process from internal to you know between different entities and that there seems like there could be some security implications. Have you thought about those?

Andrew: I have thought about that and what I eventually figured out was that at worst you'll make an invalid signature. The signature can't be used for this transaction and it couldn't be used for any other transaction either. This kind of assumes that the signer is doing some sort of sanity checking and that they are making sure that the input they're signing is what they expect it to be and that the outputs are what they expect it to be.

Audience Member: You mentioned that hardware wallets, it's important to have a little footprint of the data that is flowing through the memory. How much bigger is the footprint of this protocol if compared to the traditional unsigned transaction?

Andrew: So the PSBT contains within it the unsigned transaction so it's going to be larger. One part I didn't mention because it’s kind of in the weeds but for non SegWit outputs, the UTXO that you provide is actually the entirety of the previous transaction and so this can end up to be very large. Which I guess isn't super useful for hardware wallets however if you are using SegWit only, we don't provide the full transaction we only provide the output. This means that if your transaction is entirely SegWit outputs it can be pretty compact.

Audience Member: Something to add to that is we don't really expect to have hardware wallets implement PSBT natively. There probably will be some like the CoinKite wallet does. But hardware wallets already support signing transactions and they already need all that information. They already have protocols to to do all these things. It's more expected that PSBT will be the communication between higher-level wallet software and a driver and the driver just speaks the native protocol with the hardware wallet. As Andy pointed out this is sometimes a problem, but it is already a problem. It's just encapsulating the communication in a different way.

Audience Member: This might sort of show my ignorance in asking this question, but is the is the entire transaction all or nothing? Like when Alice recomposes all the signatures is it going to include Alice, Bob's, and Carol's transactions and not just Alice and Bob's for example?

Andrew: The combiner is very dumb and it will just combine. If you give it Alice Bob and Carols transactions the end result is going to be all of those stuck together with duplicate things removed.

Audience Member: Is Alice signing all three or is Alice only signing...

Andrew: Alice only signs her own but because it is the same transaction like the same network transaction for all three at the end her signature is valid because it's really just the same thing but spread to three different places I guess.

Audience Member: I think the confusion here is Alice does commit to the complete transaction but she only signs her input. So if the transaction has three inputs, each of the signers commits to the whole transaction but signs only one of the three inputs. Does that make more sense?

Audience Member speaks

Audience Member: No it cannot. Someone proposes a transaction that spends three inputs. That is a transaction that everybody is going to sign and until everybody signs off on that entire transaction, and it is spending three different keys so all these keys need to sign off on the entire transaction, and until all of them do the transaction is not valid. So the transaction is an atomic

Audience Member: I think Pieter was trying to explain, the purpose of a CoinJoin is such that everybody commits the same transaction. Now if you wanted three separate transactions you can always have that and that that's been there since day one.

Audience Member: I think this is really cool by the way and I have a question regarding like, is it possible to do like more complex script types? Maybe ones that are non-standard? It is? Okay it looks like it may be using the unknown fields or something? It'll be cool if you don't need the signatures in like regular places where you can so you can inject them or something.

Andrew: So actually that is up to the finalizer. The finalizer needs to figure out how to construct the final scriptSig. We actually figured out you can implement a really dumb signer. When you sign, the signer only either needs the scriptpubkey or the redeem script it doesn't even need to know what their contents are or how to parse their contents. They just need to know whether it should sign this input and if it should what is the scriptpubkey and what does the redeem script and it can produce a valid signature from there. If you have a really complex redeem script with like whatever lock times or hash locks, whatever, only the finalizer needs to understand what those are, the signers don't.

Audience Member: Are there any more questions right now? Oh super!

Audience Member: You said one of the parties, I think it either Alice or Bob who are running a node. Is running a full node a requirement for any of the participants or can they be SPV?

Andrew: They can be SPV they just need to know what the UTXO's are and this is general for all transactions. You need to know the UTXO's that you are spending otherwise you can't produce a signature.

Audience Member: And the finalizar, say the three party example, can they be a totally different entity that is monitor the network for these kinds of...

Andrew: This the final I know doesn't even need to connect to the network it just needs to be able to parse scripts.

Audience Member: So these partially signed Bitcoin transactions aren't shared on the public Bitcoin network. They're shared between users that are engaging in some protocol multi-sig, CoinJoin, whatever and then after they go through the finalizer then they can be extracted and broadcast on the network. So you could make your own protocol that exchanges around partially signed transactions using this format is what it's communicating, but that's not something that the Bitcoin protocol does.

Audience Member: Also generally, the phases it goes through, as Andy has explained there is a creator, the updater, the signer, combiner, finalizer and extractor. Only the updater needs to know about a network. The updater for the proposed transactions or the creator creates a proposed transaction the updater which is generally the wallets that are involved and know about or the ones that treat those coins being spent as theirs, because they already know how that they are theirs so that they can just add that information to to the PSBT and once that is done nobody needs to communicate with the network at all anymore. It's just operating on the data within the PSBT file and then at the end broadcasts it.

Audience Member: So how does this differ than how CoinJoins are currently performed and how does it improve upon that?

Andrew: So CoinJoins right now, well they don’t work. I guess they don't work super well with hardware and offline wallets and this kind of helps with that as it generally helps with hardware and offline wallets. Alright, Greg has something to say about this.

Greg: So CoinJoins, multi-sig, hardware wallets, all these are all things that exist today. People use them, but they all have their own custom communication mechanisms that and so you often can't combine like a multi-sig of two different hardware wallets. Good luck with that right? CoinJoins with the hardware wallet. Because they all implement something like this partially signed Bitcoin transaction specific to their application and it's not interoperable. So what this does is provides a common communication layer where all these sorts of applications can hopefully speak largely the same language. As a result we should get some better tools coming out of it at the end.

Moderator: Any more questions? Well then thank you again Andrew for your talk.
