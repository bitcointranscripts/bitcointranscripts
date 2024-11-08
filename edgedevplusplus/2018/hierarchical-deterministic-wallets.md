---
title: Hierarchical Deterministic Wallets
transcript_by: Bryan Bishop
tags:
  - bip32
speakers:
  - James Chiang
media: https://www.youtube.com/watch?v=OVvue2dXkJo
date: 2018-10-04
aliases:
  - /scalingbitcoin/tokyo-2018/edgedevplusplus/hierarchical-deterministic-wallets
---
<https://twitter.com/kanzure/status/1047714436889235456>

<https://teachbitcoin.io/presentations/wallets.html>

## Introduction

My name is James Chiang. Quick introduction about myself. My contributions to bitcoin have been on the project libbitcoin where I do documentation. I've been working through the APIs and libraries. I think it's a great toolkit. Eric Voskuil is speaking later today and he also works on libbitcoin. I also volunteered to talk about hierarchical deterministic wallets.

When we talk about bitcoin wallets, you always have some kind of secret or entropy you want to keep safe. One way to handle it and store it more easily is to use word lists. Obviously, you want to derive new fresh keys whenever you transact, so that's child key derivation. Also, there's a tree structure for standard recovery of the keys.

## bip39: Mnemonic keywords

<https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki>

What we're doing here is we have some kind of entropy to encode words. So here we have 128 bits of entropy. But you can have any multiple of 32 bits all the way up to 256 bits. When we encode these words, we want to make sure we have this checksum part. There's a 4-bit checksum, first few bits of the entropy you begin with, the length of the checksum depends on your entropy length. When we concatenate the secret with the checksum, it has to be a multiple of 11 bits. They ultimately map to via dictionary to words. You can map your entropy to different language dictionaries or word lists.

So you've generated entropy, you concatenated a checksum, so that if you mix up the words then that can be catched, and the resulting word list essentially encodes the entropy.

## Mnemonics-to-seed (bip39)

Imagine backing up your hierarchical deterministic wallet to a wordlist. This is not just a reverse process from before. You're taking the mnemonic passphrase and you pass it through a password-based key derivation function, which is a mouthful. You have a key and a message, and we do this 2048 times, to kind of make the bruteforcing of that a little more expensive. We end up with a 512-bit seed. Just to make that clear, that 512-bit seed is not the secret entropy we began with, but it's derived from it.

You could create your own word sentence and as long as the checksum goes through, this derivation of that 512-bit value would be valid. Pretty straightforward, right?

I can actualy demonstrate that in an example here. What I'm showing here is that this is a libbitcoin explorer, it's a command line tool. I'll go over that tomorrow. I just want to emphasize the process-- we generate entropy, using "bx seed", and then "bx mnemonic", and then "bx mnemonic-to-seed", and also there's "bx hd-to-public". I'm creating a new mnemonic word list with those 256 bits after running "bx seed --bit\_length 256". If I change the length of my original entropy, the length of my word list becomes shorter because decoding the entropy wouldn't be 1-to-1.

That concludes the mnemonics part. Now we have this 512-bit seed that seeds the entire HD walle.t

## Hierarchical deterministic wallets (bip32)

<https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki>

bip32 is based on deriving child keys. We're trying to generate new keys that means new bitcoin addresses. Maybe you're receiving multiple payments and you want htese payments to go to different addresses. Unfortunately, using a single address is bad because there are chain analysis techniques to track those coins and infer that those are the same owner. But if you use different addresses, that breaks down completely. You can derive via an index and a child key path, you can derive child keys from a bip32 master key.


    ## derive the mnemonic phrase (bip39)
    bx seed --bit_length 128

    bx mnemonic-new --language ja `echo "blah" | sha256sum -`

    bx mnemonic-to-seed --langugae ja (output from last)

    ## derive the master HD keys (bip32)
    bx hd-new seed

That concludes the mnemonics part. There's now a 512 bit seed which seeds the entire HD wallet. The next part of HD wallets in bip32 is about deriving child keys.

## Child key derivation

What we're trying to do here is generate new keys that lead to new addresses. Maybe I'm receiving multiple payments and I want these payments to go to different addresses. If all the payments go to the same address, then that's pretty obvious that it's the same recipient and all these payments are going to the same person. If I can generate fresh keys, then chainalysis becomes a little harder. You have to infer wallet heuristics to group these addresses together.

The way derivation works on a high-level is that you can derive on an index. I have a master key. My child keys are of subsequent generations which are derived by index. From those, we can derive grandchildren with their respective indices as well. We'll go into this a little deeper in terms of how this is derived. The point of having this ability is that, I can create different subtree and each subtree can represent an account or a purpose or even a cointype or network.

HD tree:

* Fresh addresses to improve privacy
* HD tree is derived from master key
* HD tree can be reconstructed from a master key (given the tree structure)

The master keys are derived from the HD root secret. The subtrees allow for separation of keys for accounts or usage. Also, you can selectively share keys based on which subtree you want to share.

Derivation of master keys from the 512 bits from the bip39 section; that seeds the HD wallet. How do we generate the master keys? Generating the master seed begins with an HD root seed. As you can see here, it's valid entropy lengths going from 128 to 512 bits. We generated 512 bits before. This means you don't have to seed it with a mnemonic derived root seed, you could use your own 128 bit entropy if you like. We pass that root seed into an HMAC-SHA512 function, with "Bitcoin Seed" as the key and the HD root seed as the message. Out comes 512 bits. We split these 512 bits into 256 bits on the left and the 256 bits on the right. The left ones represent the master private key, and the right one is the master chain code.

The master chain code is important because it gives you the privilege or information required to derive children later on. From the private key on the left side, we can generate the master public key by multiplying with the generator. Then we have a master public key. And then we have the chaincode, which we will use in a second.

## Child key pair derivation

Say you want to derive children from these master keys. This scheme applies to every generation of subsequent child key derivation. We start with the parent public key and the parent chain code, which is the rightmost 256 bits, and a child index. For every child, we use an index to specify that particular child.

Again, we pass that to an HMAC-SHA512 function. Here, the parent chaincode is the key, and for the message we concatenate the parent public key with the index (parent public key || index). This gives up 512 bits again. We split it up into 256 bits on the left and on the right, again.

Note that you can derive the child public key from the parent public key without having the parent private key. The child public key can be derived by multiplying the parent private key plus the leftmost 256 bits, and multiplying that all by the generator.

Something we can observe here is that here we have required that if we look at the keys we have used to derive the children, the parents keys in effect-- we need the parent private key. The parent public key on the top left can be derived publicly. Right now, I need the parent private keys to derive any children.

But note that I can write out (parent private key + L256bits) * G as (parent-private-key * G + L256bits * G) instead. What I have now is essentially the parent public key plus the point of the leftmost 256 bits. Right? What that equals is, that I can essentially skip the step where I take the parent-private-key and derive the child public key directly from the parent public key.

This is derivation with the parent private key and the parent public key. I can skip this step because I multiply out this expression and this translates to the parent public key plus the l256bits times the generator.

We can also derive public children from the parent public key. To make that a little more obvious, here is the derivation path. So we have the parent keys on the left. We have the private key. We have the chaincode. From the private key, I can obviously derive the public key. But in terms of the children, I can derive the private children and from the children private key I can then derive their public counterpart. What we saw before was that with some algebraic trickery, we can directly derive children public keys from the parent public keys.

This gives us a property where we can create two parallel derivation paths. I can either take the parent private key and derive child keys, or I can take the extended public key and start deriving public children from that value without actually revealing any private keys. If you had some frontend application where you wanted to regenerate new addresses, you could do that with an extended public key without exposing any private key information.

## Extended key format

There's an encoding format for extended keys both public and private.

There's one interesting thing about this where we have a "parent fingerprint". Whenever we look at one of these keys, they all include a parent fingerprint, a hash160 of the private key or the parent public key, and so that allows you to look at a child and ask does that child belong to that parent. This is sort of like a checksum-ish verification feature.

So we have the chaincode in there, the private or public key. If it's a private key, then it's 32 bytes. What we do is we pad it with a 0 byte. You have version, depending on whether it's mainnet or testnet network. Or whether we're talking about xpub or xpriv.

There's also a checksum. We end up with 82 bytes for the extended key. It includes all the information you need to derive the respective children.

## Example of deriving unhardened child HD keys

Here I am showing an example of deriving HD keys.

    bx hd-new (128 bit seed)
    bx hd-to-public (xpub)

The testnet serialization starts with tprv. This indicates it's a testnet private key in the bip32 extended serialization format. From that tprv, I can derive the tpub public key.

## Upstream private key exposure

So that's all fine and good. What can happen, however, is that if the parent extended pubkey and the private child is exposed, then there is the possibility of deriving the parent private key even if that's not what you intended. In a sense, this is an upstream key exposure.

You might have a frontend that just works with the extended public key but for some reason a child downstream private key has been exposed. This is what can happen. So we can compute the leftmost 256 bits because we had the public parent key, the child index, and parent chain code. We can derive the leftmost 256 bits and the child chain code. If you have a look at the child private key right now, what's happening there is that because the child private key was the scalar addition of the parent private key and the leftmost 256 bits, we can now reverse that operation and derive the parent private key by subtracting the leftmost 256 bits from the child private key. So now the parent private key has been exposed.

## Upstream private key exposure 2

Let's look at how this effects our HD tree. We have the extended public keys, and they get exposed. There's a child private key that gets exposed. The chaincodes of both private and public key are the same, and of the same index, and the same for the children. Then we can derive the parent public keys. The parent private key has been derived now, and subsequently all the children downstream can be derived from that.

So imagine the top-left were the master keys. If the master keys are exposed in that way, then obviously my entire wallet has been exposed, and that's bad.

## Hardened HD children

We mitigate that by using hardened HD children.

Here's the same derivation scheme as before. This is how you would derive a non-hardened child. We have parent public key, parent chain code, and child index. Say I change that public key to a parent private key. What's fed into the HMAC-SHA256 is different. We concatenate the message with an additional zero byte.

Child private key hardening: the parent public key replaces the private key. The HMACS512 takes in the parent chaincode as the key, and the message is 0x00 || private key || index. Hardened public keys can't derive any children, and they are derived only from hardened parent child keys.

The rightmost 256 bits are altered. These are now hardened child keys. It is no longer possible to derive a child public key directly from the parent public key. That is no longer possible.

This breaks the derivation path.

## Hardened HD key path

So we can have a look at the effect on the derivation tree. Hardened child keys break xpub derivation paths. Note that hardened keys are denoted with prime' in the bip32 child key derivation path information. Although the parent keys are hardened, note that children keys mustn't necessarily be hardened, as shown here in a diagram. This means that the child xpub keys in this example can derive grandchildren xpub keys.

Note: in the case of key exposure in any of the subsequent child generations, the upstream key exposure cannot propagate up to the hardened parent key.

    bx hd-private --hard --index 44 tpriv.....

    bx hd-public --hard --index 44 tprv....

You can only derive a child of a hardened key by having the private key for the parent and then deriving the child. This child itself doesn't need to be hardened, though.

## bip44 and bip43: HD wallet tree structure

There's a standardization in terms of the bip32 derivation hierarchy captured in bip44. What this basically says that when you derive your keys for use in an HD wallet, there's a certain scheme that you should adhere to. Starting with m/44' just refers to bip44. The second one refers to the network like mainnet or testnet. The third one is account number, like individual wallet accounts. The 4th level refers to whether it's a change address or a receiving address. Receiving address is 0 (unhardened) and the change address is 1 (unhardened). Finally, there's an address index in the last level.

## HD wallet restoration

This really helps with HD wallet restoration. Say we have a mnemonic word list, and we derive our bip32 master keys. Let's assume you've lost your hardware wallet and you only have that mnemonic word list and the optional passphrase that you have backed up. Every wallet obviously has a unique usage pattern. The tree derived in your wallet will look differently depending on how you use it. For every transaction, I decide to generate a new receive address, and for every send, I make sure to generate a new change address.

How do I know which key to derive up to? You check whether an address has been used on the blockchain. If they are unused, you iterate through the indices and you tolerate a gap up to (by default) 20 unused addresses, although a user can configure this of course. This means that the user is likely to not have generated more than those addresses.

    bx fetch-history (payment address)

## Conclusion

So that's it. It's mnemonic word list, child key derivation, and standardization of the bip32 derivation hierarchy. Do you guys have any questions? I'd be happy to try and answer.

