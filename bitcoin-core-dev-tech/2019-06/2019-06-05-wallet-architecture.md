---
title: Wallet Architecture and Descriptors
transcript_by: Bryan Bishop
tags:
  - wallet
  - bitcoin-core
  - descriptors
speakers:
  - Andrew Chow
date: 2019-06-05
aliases:
  - /bitcoin-core-dev-tech/2019-06-05-wallet-architecture/
---
Bitcoin Core wallet architecture + descriptors

<https://twitter.com/kanzure/status/1136282460675878915>

writeup: <https://github.com/bitcoin/bitcoin/issues/16165>

## Wallet architecture discussion

There are three main areas here. One is IsMine: how do I determine a particular output is affecting my wallet? What about asking for a new address, where is it coming from? That's not just get new address, it's get raw change address, it's also change being created in fundrawtransaction. The third issue is wallet signing. Storage is not an entrypoint, it's just a way of implementing these things.

Right now IsMine is independent of the wallet, for some reason. It's not part of CWallet. It's fine to abstract it out. IsMine is relevant when a new transaction comes in and we want to see our balance. It's used for getcredit/getdebit functions from wallet outputs, it's used in a lot of places. When a transaction comes in, the wallet gets notified.

![wallet architecture](/bitcoin-core-dev-tech/2019-06/2019-06-05-wallet-architecture.jpg)

## Legacy wallet architecture today

The wallet key store contains the private keys, scripts, watched things. IsMine gets queries, and then it itself queries the key store. That's how things work now. Then there's the keypool which has the HD key information, and really this is something that gets queried from time to time, asked to refill the key pool, and the key pool puts things into that blob of data. IsMine's only input is scriptpubkey. Then there's various overloads, one where you can give it a txout, so it looks up the txout and then passes the script into IsMine checks. The signing code actually also calls the wallet's keystore. The signing code uses a signing provider, but the signing provider is implemented by the key store. It's this thing where everything gets dumped in and queried from. But it's way too low level. It doesn't understand what is going on. You import a script, you import some keys, and it happens to know it can sign for it, so we are going to call it IsMine. It has no idea what things arei ntended to be... also, the keypool has keys but it doesn't have addresses, so it can't reason about what kind of address you'd like to have.

One use case we talked about earlier today is you want to get a segwit address, and we have no way of importing bech32 address without also importing the corresponding p2sh wrapped version of it, and also the legacy p2pkh, and p2pk which doesn't even have an address. So enter descriptors.

## Descriptor records and scriptpubkey managers

Native descriptor wallets <https://github.com/bitcoin/bitcoin/pull/15764>

You have a transaction that has a script. It's an IsMine on the descriptor. No, you don't need that. Each descriptor has its own key, kind of. The central kind of thing is something like this, I would call them "records". These records contain a descriptor, but they also contain every record has its own- not a key pool but an expansion cache. It has things like lookahead, gap limits information, up to how far it has been explored which is implicit due to the cache maybe not. You have multiple records. Some of these records you mark as "this is the one you get bech32 addresses from". The keypool is now gone, essentially, it's just part of the record thing. The record is identified by a hash of the descriptor. You configure the "default bech32 source" is "this" record or another. With these records, you can populate a set of scriptpubkeys to look for. We just query them. The function is "expand" I think. You throw away the metadata like the scripts and keys come out of it, and then you remember the scriptpubkeys and remember them in a set. Now "IsMine" is "does it exist in this set". That's the only thing you need to do. This is consistent with the pull requests so far. This is consistent with the descriptor wallet PR.

How does that PR deal with key pool? We don't have a concept of a key pool anymore, really. There is something in the record that is start and stop index. If you say you want a bech32, it goes to the current start and fetches it and then sends it back. But it doesn't use get key or whatever. I replaced that for descriptor wallets to be "get address from the".. and it gives you the address, not the key. Ideally, we would convert the old thing to deal with this gap address.

I think we want an abstraction around keypool, key store, and IsMine. Here is an address I have seen, is the script mine? We should have one implementation for that which uses keystore and all the existing logic. Then we can create a new one which is the records system, and it would have the exact same entrypoint. You ask the descriptors, is this mine? All it does is test is it in a set. But if you ask the other one, it goes through the old logic. For records, there is an entrypoint like "I have seen this script in the network or in the wallet to advance the ..." but the old system advances the keypool, but the records one increases the lookahead points.

Signing involves expanding the private key. The problem with expanding private keys is, how do you know that this scriptpubkey belongs to this descriptor? I have to expand to some index too. So what I had done to, part of shoving it into the existing stuff, when you do "top up keypool", it expands all of the private keys and write them down as normal keys. Can we not do that? The other way to do that was really dumb. I had to have a map of all the scriptpubkeys and they are mapping to..... yeah. You need a map from scriptpubkeys or even hashes of scriptpubkeys to which descriptor and which position in it. That's useful anyway, because if I'm doing getaddressinfo, we should report that information in getaddressinfo. I would really like us to not write every key we use, to the wallet file anymore. That's exactly what shouldn't be needed anymore.

With the expansion cache, it's fast. You generate them on the fly, you update on the fly, you increase it, they get pushed into the map. Private keys are almost completely independent.  I think private keys for the records, are not even part of the records, just "here are the private keys I have access to" in the sense that you see it as a software-signing device. When you try to sign, you use that set of private keys to help with the derivation. I think we should not see private keys as like part of the wallet, they are more-- there's a software signing device you have built into your wallet, but you potentially have hardware wallets that have other private keys. It shouldn't really matter where the private key lives, until you have to sign. If you have hardened derivation then you need access to the private key at the derivation time too. But even that shouldn't depend on whether you happen to have your private keys locally or not. It should work uniformly whether it's somewhere else.

The old signing needed the key store because the signing provider didn't provide certain things. It was infuriating.

The wallet has a bunch of scriptpubkey management objects. It has these interfaces of ISMine, sign, and here's something I saw and give me a new address. Things that are current wallet things get moved into these scriptpubkey management objects. Right now there is no hybrid form between old IsMine and this new stuff. This shouldn't even be wallet.cpp. You don't want to duplicate a whole wallet just because scriptpubkey management changes. You want to abstract out scriptpubkey management. Is that a pre-requisite? So you want to turn this into a new box, and write other boxes that have the same interface and same shape. You can have a scriptpubkey management virtual class, and a legacy scriptpubkey management implementation, and a descriptor scriptpubkey management implementation and you hold either one of these in the wallet. So this old legacy code would be moved into a new scriptpubkey management object. CWallet should just remain as it is; it's a higher-level thing, because it also manages accounts, labels, UTXO set management. Nothing about what we have talked about touches UTXO management or all the various ways of computing a balance, or all the things with coin selectoin which is already a separate file thankfully. All of those things should just remain. Just these entrypoints that we need to standardize. Getnewaddress goes through a keypool and IsMine goes through something else. It's annoying. These things shouldn't go to different things, they are provided by one thing.

Our legacy method has a getnewaddress method, an ismine method that delegates to ismine.cpp initially for now, it also has "I saw a scriptpubkey". RPC calls like getnewaddress needs a new argument like which bag of keys you want to talk to? No, that's just multiwallet. CWallet shouldn't have more than one scriptpubkey management object. Multiple descriptors should be part of one scriptpubkey management object. No, every record should be one scriptpubkey management object. Uh, implementation choice. In the future, you probably want to point to a particular descriptor when calling getnewaddress. Not sure about that. Which scriptpubkey management object do you get that type of address from? It might be a legacy one or another one. I am fine with saying you can't mix legacy with non-legacy. But apart from testing complexity and user complexity... tests should largely not change.

So we have a bag of records, that's the unit we're talking about. That bag has a method getnewaddress, and it's up to the record that it can do that? That would just be CWallet. It would know which scriptpubkey management object to ask for which type of address. If you ask the wallet for a bech32 address, the wallet would forward it to the right scriptpubkey manager. It's more like a scriptpubkey manager really, not a key management object so let's stop calling it that. That's actually the whole point. It's "wallet internal thingy". No, it's not just a wallet.

When you say "key manager", I think about private keys. Okay, let's call it SPK manager or scriptpubkey manager. The wallet contains multiple scriptpubkey manager objects.

The reason that the CKeyStore object was created a long time ago was because of a circular dependency between the script signing logic which was in script.cpp and the wallet in wallet.cpp. The script code needed access to the private keys needed by the wallet, but clearly the wallet needed to be able to call into the script stuff. So an interface called CKeyStore was abstracted out for accessing the private key. The wallet had an implementation of this key store, but unfortunately that implementation ended up in keystore.cpp instead of wallet.cpp. It should always have been, you have an external file with the interface, and then the wallet has an implementation for it. Over time, any time people wanted to add things to what the wallet was storing, it was added to keystore.cpp and all of those things should have stayed in the wallet all the time. To fix that, we created the signing provider, which is really the interface that keystore was designed to solve, and now keystore implements a signing provider, and I think we should just get rid of keystore. There's still this bag of objects, right, but that's a wallet-specific thing.

CWallet is its own class that doesn't inherit anything. We could have a method like "sign this transaction", instead of exposing... I don't know what is easier to do that. Figuring out what the, boundaries of what this box should exactly entail. There's a lot of logic for various kinds of edgecases like when you derive a new public key that we know the private key for then we add the p2sh that we know the p2wpkh for it, and that should also be in the walle tbox so that we don't need it in this other box anymore.

## Serialization

With regards to serialization... it's tightly coupled to CWallet and the database. When you load a wallet, it starts instantiating objects immediately. Serialization can just be done by the CWallet parts. You would pass down the database object. There are a bunch of new serialized objects that need t ogo into these, but not all of these. You're reading object by object in the database, and you're instnatiating new objects and they need to go into this collect. Most of these things will belong to one box, so you would say, the flag says this is a legacy wallet, as you deserialize, you see a seed key, you pass it into the box. So as you deserialize, you create the box and you just start throwing things into it, and if you see a descriptor wallet then you start throwing things into that box. The descriptor box is- are- they have to be a new record.

## Back to other wallet stuff..

There's quite a few tests that rely on dumb "IsMine" behavior. The functional tests. The entirety of the wallet, basically. There's a lot of things shared between these.

Labels and addressbook, how does that interface now? We have a record that takes the address as a label. It's separate from adding script or whatever to the key store. Yeah, they're different. IsMine in the new one, has no such thing as "InMine solvable". It's either spendable, or watchonly. If you have a hardware wallet, we want to call it "spendable". For watchonly, maybe use multiwallet.
