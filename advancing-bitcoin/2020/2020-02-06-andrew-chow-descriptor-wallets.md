---
title: 'Rethinking Wallet Architecture: Native Descriptor Wallets'
speakers:
  - Andrew Chow
date: 2020-02-06
transcript_by: Michael Folkson
tags:
  - wallet
media: https://www.youtube.com/watch?v=xC25NzIjzog
---
Slides: https://www.dropbox.com/s/142b4o4lrbkvqnh/Rethinking%20Wallet%20Architecture_%20Native%20Descriptor%20Wallets.pptx

Support for Output Descriptors in Bitcoin Core: https://github.com/bitcoin/bitcoin/blob/master/doc/descriptors.md

Bitcoin Optech on Output script descriptors: https://bitcoinops.org/en/topics/output-script-descriptors/

Bitcoin Core dev wiki on Wallet Class Structure Changes: https://github.com/bitcoin-core/bitcoin-devwiki/wiki/Wallet-Class-Structure-Changes

# Intro

Hi everyone. I am Andrew Chow, I am an engineer at Blockstream and also a Bitcoin Core contributor working mostly on the Bitcoin Core wallet. Today I am going to be talking about rethinking the wallet architecture with native descriptor wallets. But first in order to understand why we need to rethink the wallet architecture we have got to understand what the current wallet does or what it did before I guess.

# Old Wallet Architecture

What is the old wallet architecture, at least in Bitcoin Core? We have a thing what I call the “bag of keys” model. The wallet just has a bunch of keys and it does a bunch of things with those keys. Everything is centered around those keys and a lot of wallets follow the same thing just with a little bit of variation of what they produce with those keys. What we do with those keys is we take a key and we convert them into addresses and scriptPubKeys. You take a key and wrap some script around it to make a P2PKH scriptPubKey, make that address and hand it to the user. That is what we do right now. But the problem with this besides one key having multiple addresses, is that it is not very expansive. We can’t use a single key to make multisigs. We can’t give out multisig addresses. And we can’t give out addresses that correspond to arbitrary scripts that do that weird contract thing that you really want to do. So the way that we are going to solve this is by using the descriptor wallets. To do that we need to redesign the wallet architecture.

# Native Descriptor Wallets

First what are native descriptor wallets? As the name suggests they store descriptors. What are descriptors? I will get to that in a minute or two. The thing with native descriptor wallets is they can store any kind of descriptor including multisig descriptors or in the future Miniscript. With native descriptor wallets we can have a wallet that hands out addresses for multisigs, for arbitrary scripts, basically whatever you want without the wallet software having to hardcode in what to do with keys or what kind of scripts to produce. We also use a specific type of descriptor called a range descriptor that lets us generate multiple things from a single descriptor.

# Output Script Descriptors

Now let’s talk about output descriptors themselves. Output script descriptors are named as they suggest, they describe output scripts. But they also describe output scripts along with everything you need in order to solve them. Solving is a thing that is kind of specific to Core, a term that we define in Core. It means that if we have valid signatures or we have the private keys related to a script we can produce a valid input scriptSig. This means that we have all the redeem scripts and all the witness scripts we need in order to produce that scriptSig. The output script descriptor will tell us all of this information, not just what that output script is. Output script descriptors are also engineer readable. Slightly less readable than human readable because your average user probably won’t be able to read them. But if you understand Bitcoin terminology the descriptor will tell you everything you need to know. If you really want to dive deep into the specific details about descriptors there is a [document](https://github.com/bitcoin/bitcoin/blob/master/doc/descriptors.md) in the Bitcoin Core repo that you can go look at. That explains everything in far more detail.

# Descriptor Examples

These are some descriptors. They may look very confusing and it may be a little hard to see. If you look closely at the beginning of each one we have got things here that are human readable like `pk` or `pkh` and `wpkh`. For those of you that know Bitcoin terminology you might notice that those stand for public key or public key hash and witness public key hash. Similar to P2PK and P2PKH. We just drop the P2 part because that is extra noise. Really a descriptor is a function. We have a function name and the descriptor function returns a script and it takes some arguments like you would in any programming language like C or Python. The arguments can vary. Some of them take public keys, some take scripts, some take multiple public keys, whatever. Let’s go into a bit of detail on one of these descriptors.

`￼pkh(02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7aba
c09b95c709ee5)#8fhd9pwu`

This is a very simple descriptor. At the beginning you see it says `pkh`. This stands for pubkey hash, it is just the function name it returns. This tells you it returns a pubkey hash script. The argument to this is a public key, just a public key, nothing special about it. At the end we have a checksum. This checksum at the end is based on bech32. That means that there is some error detection and error correction in case for some reason you are typing these in by hand. Although I am not sure why you would want to do that. From this descriptor we now know the scriptPubKey. It is that thing.

`76a91406afd46bcdfd22ef94ac122aa11f241244a37ecc88ac`

And we know the address which is up there as well.

`1cMh228HTCiwS8ZsaakH8A8wze1JR5ZsP`

These are correct, I did compute them. But besides just knowing this output script we also know what we need in order to produce that valid signature. We need to have that pubkey and we need to have the private key for that pubkey. Because we know that we have that pubkey it is solvable. Here is a slightly more complicated example.

`pkh([d34db33f/44'/0'/0']xpub6ERApfZwUNrhLCkDtcHTcxd75RbzS
1ed54G1LkBUHQVHQKqhMkhgbmJbZRkrgZw4koxb5JaHWkY4ALHY2grBGR
jaDMzQLcgJvLJuZZvRcEL/1/*)#ml40v0wf`

This kind of descriptor is actually what we will be including in our wallet. This, like the previous example is `pkh`. But you will notice that the public key argument is far longer and far more complicated. First we have got this square bracket thing. This is for key origin information. I’ll get into that a little bit later. Then we’ve got a xpub which I am sure many of you are familiar with. Then we have a thing at the end that is actually some derivation information. And of course the checksum. What is this key origin information in our square brackets? It is based on derivation paths. It looks very similar to one. Instead of the m at the beginning like you would see in a derivation path we have this thing called the fingerprint. The fingerprint is just the first four bytes of the hash160 of the master public key. In this example it is `d34db33f`. That is just an identifier of the master public key. After that is the rest of the derivation path `44’/0’/0’`. What this tells us is that this xpub is derived from a master public key with the fingerprint `d34db33f` at the derivation path `m/44’/0’/0’`. After our xpub is more derivation information. `/1/*` is telling us where to derive more keys at. What this descriptor is telling us is that even though we have given it a single key we can actually produce a tonne more keys from it and therefore many, many scriptPubKeys from it. The resulting scripts that we get will have public keys derived from d34db33f at m/44’/0’/0’/1/i which if you are familiar with BIP 44 is a standard BIP 44 derivation path. We call these range descriptors. The astute among you may have noticed that this only produced one kind of scriptPubKey. It only produces `pkh`. It also only produces keys at a specific derivation chain. This does not cover your change addresses and if you wanted to use SegWit you can’t do it with this particular descriptor. In our descriptor wallets we did the lazy approach and we just have six of them.

# Stored Descriptors

There is one for each address type. There is one `pkh`, one `sh(wpkh)` and one `wpkh`. And one of each of those three for change and receiving addresses. But the cool thing here is that we are not limited to just these three kinds of descriptors. You can replace say the `wpkh` one with `wsh(multi)` if you wanted to have bech32 multisig addresses.

# Benefits of Descriptor Wallets

That is one of the cool things about descriptor wallets. They are expandable, we can just swap out one of the descriptors with a different one and we can still get addresses for that. The wallet itself doesn’t really need to know how to sign for that multisig that you put in there because the descriptor tells you how to sign for it. Another thing about descriptor wallets is that those descriptors are completely unambiguous as to the derivation paths you are using and what kind of address you are producing. This means that if you wanted to import a descriptor to another wallet you don’t have to guess what derivation path it is going to use and you don’t have to guess what kind of address it is going to use. The descriptor tells you right there exactly what it is going to produce. That means we can get rid of [walletsrecovery.org](https://walletsrecovery.org/). That makes backups easier. We have everything we need in one single string or I guess a couple of strings you can slap together. That checksum also makes them portable in case you decided to type them in by hand for some reason.

# Implementing Descriptor wallets

How do we get descriptor wallets in Bitcoin Core? In Bitcoin Core we still have this bag of keys model and the way it is implemented is very tied in with the wallet. It is hard to separate it out. For the past several months I have been working on a project within Core to first abstract some parts of the wallet. Specifically we have been abstracting out this key and scriptPubKey management into a very obviously named [ScriptPubKeyMan](https://github.com/bitcoin/bitcoin/pull/17261). This abstraction just means that we take all the keys and the way that the scriptPubKeys are produced and we shove it into its own box where it can do its own thing and where we can actually change how the scriptPubKeys are being produced. Really what the wallet cares about are the scriptPubKeys not the keys themselves. The keys are just extra data that are related to the scriptPubKeys. So what this model means is that we are moving away from the “Take a key and make a script out of it”. We are changing to “Here is a script. What do we need in order to sign for it?” With this refactor our main wallet class `CWallet` will just contain scriptPubKey managers and it will ask scriptPubKey managers for new scriptPubKeys. When it needs to sign a transaction it just hands it off to the scriptPubKey manager and that figures out what needs to be done in order to sign for the scriptPubKeys. This means of course we can change out what is inside. Obviously we have got the old thing that we do, shoved into its own thing that we call `LegacyScriptPubKeyMan` because it is legacy code. And we’ve got a new thing for output script descriptors. We will have an output script `DescriptorScriptPubKeyMan`. This descriptor scriptPubKey manager will use our descriptors to produce scriptPubKeys. Our descriptors tell us how to sign, that is how the scriptPubKey manager knows how to sign for everything. If you are interested in more nitty gritty details there is a [document](https://github.com/bitcoin-core/bitcoin-devwiki/wiki/Wallet-Class-Structure-Changes) on the Bitcoin Core developer [wiki](https://github.com/bitcoin-core/bitcoin-devwiki/wiki) that no one realizes exists.

# Current State of Descriptor Wallets

So where are we at now with getting all of this into Core? As far as I know no wallet actually uses descriptors yet which is a shame. Core is getting there slowly but it takes a lot of work. I think a few other wallets also have it in their roadmap but so far no one uses descriptors yet. But in Core we have done this refactor so we are getting pretty close. The refactor into `CWallet` and `LegacyScriptPubKeyMan` was [merged](https://github.com/bitcoin/bitcoin/pull/17261) last week after I had written these slides. But hey it got merged. There is an open [PR](https://github.com/bitcoin/bitcoin/pull/16528) that introduces our `DescriptorScriptPubKeyMan`. That will be merged hopefully in a few months. Maybe by the end of this year we will have descriptor wallets. Even though this seems like this is the closest to descriptor wallets in the Bitcoin space I am hoping that someone else will catch up and get to this before we do in Core. But at the very least descriptor wallets and our whole refactor will make Core into a more modern wallet and catch up to where every other wallet is at now. It will also allow us to move forward faster in the future.

# Q&A

Q - I do appreciate that it is engineer readable but I was wondering if you thought about providing also the bech32 encoding or the encoding for moving from wallet to the other. It could be easier to encode into a QR code or to move around. Would it make sense to encode the whole descriptor as bech32 address?

A - There has been some discussion about encoding it in some way. Specifically bech32, I don’t think it would make sense there because bech32 is not optimized for this kind of string. That is why we do have a checksum at the end of it. That is based on bech32 and that checksum is optimized for descriptors themselves. There was a suggestion to base64 encode the entire descriptor and call it some magic string and hand it off to users if they wanted to import them.

Q - Within HD wallets in the relevant BIPs there is a description of a lookahead of 20 keys. When a wallet is trying to rebuild the structure after it has found that many keys without any cash in them it will give up. Is there something more intelligent that descriptors can add to that?

A - No.

Q - In BTCPay when I started it the concept of output descriptors did not exist so I wrote my own that I called DerivationScheme. I am considering trying to move away from this and more into this output descriptor language. But the main issue I have with it is that because it is not merged and lots of people don’t rely on it, it means that if I do it now there is lots of chance that the language evolves. If it evolves it might break my stuff pretty badly. That is the reason why I am not going into this yet. Do you think right now it is stable enough and you are pretty sure that it won’t move and break soon?

A - Everything that is currently implemented is extremely unlikely to change even though there is no BIP for it or anything. Whatever exists now, the examples I showed, they are probably not going to change at all. But descriptors will be improved. There will be things added to it like Miniscript. There will be more functions added but the things as they are now are not going to change.

Q - Why is there no hash of the chaincode in the xpub?

A - The xpub includes a chaincode.

Q - The hash of the pubkey, that is just for verifying or double checking?

A - The fingerprint thing, I was talking about the hash of the pubkey. That is just there for an identifier. That is particularly useful in PSBTs because a PSBT has to contain the fingerprint of the master public key to identify the signer. We just tacked that onto descriptors because it is useful.

