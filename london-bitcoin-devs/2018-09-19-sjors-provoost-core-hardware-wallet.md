---
title: Using Bitcoin Core with hardware wallets
transcript_by: Michael Folkson
tags:
  - hardware-wallet
  - bitcoin-core
speakers:
  - Sjors Provoost
date: 2018-09-19
media: https://www.youtube.com/watch?v=SUDkYbkcTsQ
---
Slides: <https://github.com/Sjors/presentations/blob/master/2018-09-19%20London%20Bitcoin%20Devs/2018-09%20London%20Bitcoin%20Devs%200.5.pdf>

Core, HWI docs: <https://hwi.readthedocs.io/en/latest/examples/bitcoin-core-usage.html>

# Introduction

I am Sjors, I am going to show you how to use, you probably shouldn’t try this at home, the Bitcoin Core wallet directly with a hardware wallet. Most of that work is done by Andrew Chow. I’m just showing how it works. I will have some thoughts of my own on how that could be made more user friendly.

# Bitcoin Core wallet

The Bitcoin Core wallet, most people will probably recognize it either as a graphical user interface but a lot of people use the command line. This is what the GUI looks like, it is pretty bare bones but it works. It receives Bitcoin, it sends Bitcoin, it validates all the transactions. Then other people prefer it like this where you say “Give me a list of transactions”. I prefer GUIs actually. Why would you want to use the Core wallet? It validates all the blocks, checks all the rules, it is very well reviewed code mostly. But there is a downside, it sits on your computer. If you are like me, use all these developer tools and all these fun programs then maybe a virus sneaks in and takes your private keys. It could just look for `wallet.dat` file and take it. That is a pretty big downside.

# Hardware wallet

Hardware wallets on the other hand are not on your computer. Even if there are problems with the hardware at least it is not on your computer. But the downside is it reveals addresses to a third party. You have to use the Ledger, Trezor whatever backend service to see your balance. They shipped the device to your physical address. IP addresses are usually easy to correlate to physical addresses, it is not good. I am surprised that’s not used more but I guess there are easier ways to go after people. The other thing is it relies on external truth. We talked about BIP148, the opposite of that is SegWit2x where other companies said “Let’s change Bitcoin”. Those other companies can just tell you “This is your balance” and your transaction is perfectly valid on this other chain. We don’t want to rely on external truth. It involves quite a lot of code. Especially if they also ship a wallet that tends to be a tonne of Javascript and Python bindings, lots of stuff that probably doesn’t get as much review. I’m sure they do great work and they have auditors and all that stuff. It is all open source but still it is a lot of code.

# Combined

So let’s combine this. Keys are not on your computer, that’s good. You get much better privacy because all the checking of your balance is done on your computer. You download the whole blockchain so nobody knows what you are interested in. If you relay your transactions through Tor as was talked about earlier that could help. As well as the Dandelion idea coming up. There’s no external truth, that’s good. The amount of code that you still have to review would be much, much smaller. It might just be a driver for that specific wallet and the software that runs on the actual device. That’s a bright future.

# Problems

There are some problems. How do you encode transaction data? That’s been solved recently with something called Partially Signed Bitcoin Transactions (PSBTs). I’ll show that in a bit. That used to be a problem, how do you communicate a transaction? There’s no standard for it. There is now. The other is how do you actually communicate, what protocol do you use? Electrum Personal Server is one way to communicate between the device and the Core wallet. You can do lots of things semi manually which I’ll show you. I have some ideas on how to turn that into a better standard. Also how do you minimize the amount of stuff you need to install? When it comes to Bitcoin Core specifically making super radical changes like adding device specific support, USB drivers and the whole kitchen sink, I don’t think that will ever get merged. Whatever you do has to be extremely minimal. Maybe add one RPC call or one little thing.

# Anatomy of Bitcoin Core Wallet

So what does a Bitcoin Core wallet look like roughly? You have a master private key, your seed essentially which you should backup. Then this thing called the keypool which is a pool of keys. You take the master key and you derive all these keys from it. Then whenever you want to receive something it turns that key into an address and you send money to that address.

# Core + HWW Setup

When you want to combine this, the workflow you’d want that has been built now, you start with an empty wallet that does not allow any private keys in it. That is a new flag (`watch-only`). A watch only wallet. There is nothing in the keypool, there’s no addresses. What you are going to do is feed it with addresses from the hardware wallet.

# Core + HWW Usage

Once you’ve fed it now the wallet contains a bunch of public keys from the hardware wallet and you can generate receive addresses as before. The nice thing about this is you can receive money and create new addresses without having the hardware device plugged in. It just has a bunch of addresses. When you want to spend something now you’ll need to connect it and you somehow need to sign the transaction with the hardware device. That is the thing I will show.

# HWI

<https://github.com/bitcoin-core/HWI>

Docs: <https://hwi.readthedocs.io/en/latest/>

HWI, hardware wallet interactions, a repository by Andrew Chow who has been working on this for a while. Finally getting some attention. What he’s done is he has taken all these device drivers from Ledger and Trezor and a bunch of others that are all in Python and built a generic wrapper around it so they all take the same commands. You can tell it “Give me an address” or “Give me an xpub” or “Sign this thing” without having to think too much about the specific device. There’s a nice manual here.

# List devices

One of the commands you can do is:

`./hwi.py enumerate | jq`

It will say “I found a Ledger and the fingerprint which is the BIP32 root key is that”. If you know the fingerprint then you can talk to the device. We create a watch only wallet with the top command:

`bitcoin-cli createwallet “ledger” true`

`bitcoin-cli -rpcwallet=ledger getwalletinfo`

New in Bitcoin Core 0.17 is that you can create new wallets on the fly. That’s quite nice. You can load and unload them. What does that wallet look like? You give it a name and the most important thing is that that keypool is empty. There’s no keys in it. We haven’t done anything with it yet.

# Get keys from device: receive

Now we are going to get some keys from the device. We identify it with the fingerprint, one way to reach it.

`./hwi.py --testnet --fingerprint d9d676d4 getkeypool “m/84’/1’/0’/0” 0 0 --keypool | jq`

We give it a BIP84, is everyone familiar with BIP44 address generation? You start with a master key and then you derive a bunch of subkeys from it down a hierarchy. That is why it is called a hierarchical deterministic wallet. The first derivation is called the purpose. In this case I’m using `84` which is the new bech32 SegWit format. `1` is the coin type, `0` would be Bitcoin, `1` would be Bitcoin testnet. Ethereum is g\*d knows what number. The next number is the account and the last is whether it is a receive or a change address. This is a receive address instead of a change address. Then you give it a range, you say “Give me the change addresses from number 0 to say 100”. You only want to do this whole setup process so I would take 1000 keys or whatever it can handle. This spits out the public keys in a format that Bitcoin Core understands. You don’t actually have to be able to read this, just know that Bitcoin Core understands it. You can ignore the address field, that is not actually used.

# Get keys from device: change

The same with change addresses. There is a `1` here instead of a `0`.

# Import keys into wallet

Then you import it using the call `importmulti`. You copy, paste the output from the previous command, it says `“success”: true`. That’s good. If it throws an error message you did something wrong. Done that wrong a few times. There is one little extra thing here that I should clarify.

`”m/84h/1h/0h/1/0”`

Here it explains that this public key that you are about to import belongs to a device or a tree with this fingerprint at this location. The reason you need that is if your hardware wallet wants to sign something, if you just tell the hardware wallet “Here’s a transaction, go sign it” the hardware wallet will say “What the hell are you talking about? I have a million private keys, do you want me to check all of them?” No, you have to tell it what specific private key to use. This is how you communicate which specific private key to use. The problem is Bitcoin Core currently doesn’t actually import that type of information. One of the changes Andrew Chow made which is probably mergeable does store that. That’s the little tweak you could potentially get into Bitcoin Core, nothing too radical, just a little extra field. You import that, it is happy.

# Generate receive address

Then you can use it to receive as you would otherwise. You’d say “Give me a receive address” and it creates a nice address. You send some money to it.

# Wait for confirmation

You wait for it to arrive. Notice that now this on the watch only side. There is a [pull request](https://github.com/bitcoin/bitcoin/pull/13966) currently out there, if the wallet is only a watch only wallet then it is kind of nonsense to make this distinction. It is all watch only. That pull request will remove this and just have one number, much cleaner. This little icon will be moved over there. It is clear that this whole wallet is watch only. It is a very small tweak that you can do to make it better.

# Prepare transaction

We want to spend some of this money. We are going to create this PSBT thing, partially signed Bitcoin transaction. I will show what it looks like in a bit. It is like creating a transaction, you tell it where to send it to, the address, you tell it how much to send (0.1 test Bitcoin) and then importantly you say `includeWatching: true`. That’s a new thing. You tell it “Yes you can spend from your watch only addresses”. Bitcoin Core doesn’t normally let you do that. I say “Yes don’t worry about it”.  Then you add this `true` boolean which says “Give it the BIP32 derivation path”. If you forget that you will get very confused. It spits out this thing. We are going to look at what that thing is.

You can decode it, the same string, it splits it out. This is a whole long list. It contains the transaction hash as it would be before you sign it. It shows the inputs, it shows the outputs. The address is where you are sending it to. And this is the change address. Not that interesting. Then on the inputs what is important is you are telling the device what pubkey you are spending from but you also have this BIP32 derivation. It says this pubkey belongs to this path. That’s all part of that partially signed Bitcoin transaction format standard, that type of information. On the outputs again, this is a change address, `1` means change address. That means the Ledger or Trezor or whatever you are using knows that part of the money is going to the outside world, it will prompt you “Do you want to send money to this address?” and part of the money is going back to itself. It knows that it doesn’t need to show this because it has the private key for this, it doesn’t need to worry about this 100 Bitcoin that’s moving around. It just goes to myself. That is quite useful for a good user experience.

# Sign transaction

So you sign it with this command:

`./hwi.py --testnet --fingerprint d9d676d4 signtx insert_long_thing`

If you click the button on ok it spits out a slightly longer version of that same thing.

Q - Can I just ask why you’re not using process PSBT? Process PSBT takes what you had before, the output of create funded…

A - It can’t sign it. But if you had a multisig situation you would do that. I’ve tried that at home, don’t try that home, a multisig between a Bitcoin Core wallet and a hardware wallet. You tell the Bitcoin Core wallet “Process this thing”, it signs its side, you tell the hardware wallet “Process this thing”. You can even do that in parallel. There’s a command [combinepsbt](https://github.com/bitcoin/bitcoin/blob/master/doc/psbt.md#rpcs) which will take one thing signed by one device and one thing signed by another device and tries to combine it. If it has enough signatures it says “Done” and then you can broadcast it. It is very, very cool. Very scary to do it manually though. With all of this I’ve tried it with real money.

Q - With multisig it did work?

A - It did work. I’ve done it with multisig, not lost it yet. I’ve done it with just basically the hardware wallet as the only thing with keys and not lost anything yet.

Q - Why is it scary?

A - It is extremely scary. These are super manual commands with public keys, am I actually able to sign this money? You tell somebody “Go send money to this bech32 address”. They send you money and you’re like “Let’s see if I can still spend that”. I find that scary.

Q - You’ve got all these long JSON strings…

A - While making this presentation I screwed up like 3 times.

Q - The hardware wallet is supposed to internally prevent that.

A - You are generating keys so if you are generating addresses the wrong way. You want to make sure the destination is a public key controlled by the hardware. You want to make sure the derivation path is not some random string that you can not reproduce. It is probably easier to screw up on testnet. Even then I screwed up but I didn’t lose any testnet coins. I sent money to the same wallet instead of an external wallet, it was not too bad.

# Before

Before and after, what we see here is the input side of the transaction that they needed to sign, the address that it is coming from and the public key. It has this derivation for the public key (`”m/84’/1’/0’/0/0”`).

# After

Boom, partial signatures. It says “Now I have a signature for this thing”. That was added by the hardware device. That’s why that long string looks slightly different.

# Finalize and broadcast

We have this command called `finalizepsbt`.

`bitcoin-cli -rpcwallet=ledger finalizepsbt insert_long_thing`

You copy, paste the long thing in there. It produces a transaction in hex format that you can use. And it says `”complete”: true`. Complete means this thing has all the signatures and is otherwise valid. If it is incomplete then maybe you need to send it to someone else to add another signature or you did something wrong. Then you say `sendrawtransaction` or you copy, paste it in some other place.

`bitcoin-cli sendrawtransaction insert_transaction_hex`

It gives you the transaction hash and then it is on its way. It is very cool I think. It is a bit manual but I think it could be made quite elegant.

# Signer RPC

What I’ve been trying the last couple of days, I didn’t finish it, is to figure out how do you communicate that you want something signed. That could be a hardware wallet, “Go sign my transaction” but it could be a BitGo or some other service that does multisig where you say “Here’s my partial transaction. Go sign whatever you can sign and then give it back to me.” Have that completely automated. You are in a Bitcoin Core wallet with some other wallet and you are entering your destination, it figures out “I have these keys I need to sign. I know what the master public key is and I have some mapping of this master public key belongs to this service and that master public key belongs to that service”. That is why I’m thinking about a JSON-RPC because then you would have something like localhost, port 1000 and that represents a hardware wallet. Then the hardware wallet driver would just run a little server on your own computer that you talk to locally. They already do because a lot of times there is Electron Javascript simulated, it is like a little Chrome browser in a box. Often that actually is a client, server mechanism anyway, it is not even that bizarre to do it that way.

# Hardware wallet side

What could that look like? Something like this. The hardware wallet or the multisig service out there accepts a bunch of commands. It has a command `enumerate` that gives a list of devices. It has a command `getxpub` which you pass a device identifier `device_id` and the path `bip32_path`. “Give me the xpub of the receive chain” or “Give me the xpub of the change chain”. Then maybe something like `displayaddress` to show this particular address on the device so the user can check that it is the same to what they are seeing on their computer. And one that says `signtx` which takes one of these partially signed Bitcoin transactions.

```
enumerate
getxpub “device_id” “bip32_path”
displayaddress “device_id” “bip32_path” (“address_type”)
signtx “psbt”
```

# Bitcoin Core side

Then on the Bitcoin Core side you would add a number of fairly simple methods I think. One is when you launch it you give it a RPC URL.

`bitcoind -signerrpc=localhost: 1000`

```
listsigners
displayaddress “device_id” “bip32_path” (“address_type”)
importsignerkeypool “device_id” “bip32_path” start end
sendto “address” {signer: “device_id”}
```

There is one signer located at this address. It already knows how to do calls to other JSON-RPCs. That’s no dependency. Then you’d have a couple of extra commands. One is `listsigners`. This looks at all these things and asks it what devices do you have or what multisigs do you have. Also `displayaddress` which just relays the same command. Then the `importsignerkeypool`, that’s the whole flow I showed where you generate all these keys and import them. That would be one command. “Go fetch 1000 keys from this device”, it is a one-off thing. Then the last one would be `sendto`. You give it an address and an amount and tell it a hint which device to use as a signer. I would like it to just work but I don’t think that’s going to happen. I would like it to just go through the transaction and figure out “I need this signer and I’ll go call that service”. I don’t think it will be that automated. You can make a nice GUI around this. I would imagine you install your driver from the hardware manufacturer and then you go into Bitcoin Core and you say “Do you want hardware support?” It has a default place to look for but you can give it a manual address if it is somewhere else. Then it says “Ok. Please connect the device”. Behind the scenes it calls this `importsignerkeypool`, sucks in all the addresses and then whenever you want to send something it says “Plug it in and we’ll wait for it to sign it”. That is how simple it could get. From the Bitcoin Core side you have very few changes to merge, just a few new calls. You leave it to the hardware manufacturers to implement this particular standard. This wouldn’t be Bitcoin Core specific either because any wallet could call a RPC like that. That’s my thought, maybe someone has already done it, I haven’t Googled enough.

# Thanks

I’ll put the slides [here](https://www.slideshare.net/provoost) I have a [blog](https://medium.com/provoost-on-crypto), I have a PGP key. I didn’t check if somebody edited this thing.

# Q&A

Q - What about authentication?

A - If it is on the local device I don’t think you need authentication. If you are plugging in something your own computer then you trust it. It will call localhost unauthenticated. I was thinking about if you have an external signing service, one idea I had is JSON-RPCs can do logins and passwords and all that nonsense but it sounds complicated. Something that could be simpler is you call this service and you give it the unsigned transaction but you also give it a public key. Then the service basically gives you back a UUID, a completely random number plus a date, “Come back at this time”. Then you call that UUID which nobody can guess because it is random and it gives you back an encrypted payload using that public key you just gave them. Even if somebody could guess it they couldn’t decrypt the signed transaction. Then you get your signed transaction. That would be nice because the way this works so far is we are just blocking RPC calls. You say “Sign this thing” and then it blocks until you press the button. That’s fine if you are signing locally but if you have some service that says “Thank you. We are going to send you an email and a text message and we’ll give you a 2 day cool day period” and all that stuff you don’t want a blocking call waiting for that. Just come back later. The nice thing about this PSBT thing is it is in parallel. You could just have it call the hardware wallet and have it call some other service. They don’t need to come back at the same time. That would require more changes on the wallet side. Now you need to track what am I waiting for? You’d need to have a list somewhere of pending transactions and where you are expecting a result. That’s not that big either. This transaction, plus a URL plus a UUID and a date and you wipe it if it takes too long.

Q - If one key is Bitcoin Core and one key is Ledger and I don’t know which key is on the underlying multisig, I could ask Bitcoin Core to sign it and it would end up going to you and not me?

A - That’s where the authentication comes in. They receive a transaction from some random source. They recognize your public keys because there is enough information in there so they can map that back to you. Then they send you the email saying “Somebody is trying to spend your money. Is that you?” Maybe you want to add some extra hurdles there so you can’t just spam them and randomly try to intercept somebody’s email or some trick like that. I haven’t thought this through in that much detail. I’d just like this to work without any login concept but I’m not married to that.

Q - What are your thoughts on the security of hardware wallets? Do you feel it is the right model for long term cold storage?

A - I don’t know, I certainly know my laptop is not the right model for long term cold storage. My last laptop disappeared in Barcelona. I think this is unsolved. Even the hardware wallets tell you “Write down your paper key” so now you have this paper key lying around in your sock drawer. Is that good? I don’t know. For the time being unless you are extremely rich you are more likely to lose your Bitcoin because of your own stupidity than to get robbed by someone. My guess is in theory you should be able to get insurance against that type of physical theft, it is a very known threat model. You should just be able to say “If somebody robs me and I give some sort of proof of reserve to the insurance…”

Q - I dox myself and how many Bitcoin I have?

A - Your insurance company will know. That’s the trade-off. If you don’t want to trust the insurance company then don’t get insurance. If you do want insurance then the only trade-off is the insurance company will know how much you have, the tax authorities will know how much you have but they won’t know what you have. It may very well be worth it if you are rich enough. If you are rich enough people will know it anyway. That’s the thing with people who think they can avoid the tax authorities. If your behavior is like the behavior of a person who has a lot of money your neighbors are going to be jealous. “I think he has more money than he says he does. He is driving this lambo.” They will follow you and look at everything you are doing. They’ll dedicate 10 people for a month to dig into everything they find. They’ll blackmail your children. Taxing rich people is an older profession than prostitution, it is competing. Tax enforcement and prostitution are probably about as old. Everybody thinks Bitcoin changes everything, I doubt it. I really doubt it. But I’m a bit of a cynic.

Q - The keypool had to be empty so it has to be a fresh wallet when you set it up?

 A- You don’t have to. If you are comfortable getting extremely confused you can do this in an existing wallet. One of the setups that I tried was multisig where you would have a regular wallet that has its own keys and you combine it with a hardware wallet. You pull in the keys just for the purpose of multisig. Multisig however is extremely confusing in Bitcoin Core.

Q - How does it work? BIP32 has the gap so if I derive one key…

A - Bitcoin Core doesn’t do gap limit. What it does is derive a bunch of addresses, throws them in a keypool which it can draw from.

Q - If I use my Ledger with Bitcoin Core?

A - The compatibility problem? The way I did the demo here, I tried to stay compatible by using the standardized derivation paths. But then it is up to you to honor the gap limit.

Q - Are the keys in the keypool in order?

A - It picks them in order. You will probably honor the gap limit. If you wanted to patch Bitcoin Core and say “Honor the gap limit as an optional flag” that sounds like the kind of change that is small enough so that it could get in. The gap limit is especially a problem for merchants. What merchants do is they have a customer and they have a shopping cart, they generate an address specifically for that customer. They should not reuse that for another customer. They shouldn’t even reuse it at all. If I wanted to spy on a merchant I would just create all these fake orders and collect all their addresses and then monitor the entire revenue going into that shop. The problem with generating a new address is you hit the gap limit which is why merchants should use Lightning, Lightning doesn’t have that problem. It solves the gap limit problem quite elegantly. For normal users I think it is less likely because the way you break the gap limit is by generating 20 addresses in a row and having a very pedantic implementation from the other wallet. Wallets should be very conservative in not exceeding the gap limit. I worked for a wallet in the past and I spent quite a lot of time making sure it honored the gap limit very pedantically. But it should import quite royally. It should be accepting 100 or more if it can.

Q - How could multisig be improved using Bitcoin Core?

A - PSBTs is a huge improvement. That’s step 1. That makes it less confusing than it was. Me having done it 20 times also makes it less confusing. I know sipa is working on cleaning up the wallet in general using these output descriptors for example. The wallet was based on the very old model, you just have keys and those keys you have the private keys for. All the wallet cares about is do I have this private key or do I not have this private key? SegWit got added and now one private key could map to different spending scripts. That was kind of hacked into the wallet. If that gets cleaned up then I think we can have a way to describe “I know of these keys and I know I have one key of this multisig”. Right now it is quite a few commands to do multisig. You have to say “Give me an address” but then you also have to explicitly import that address.

Q - Multisig is quite easy to use on Electrum.

A - Your solution is easier for now. But you need to install more things. You need to add all of Electrum.

Q - Electrum used its own format for this kind of problem.

A - That was another problem I ran into it. It uses xpubs, ypubs and zpubs and they are not really standardized. You need to go through the right steps to not dox yourself when you install it. You need to make sure the first time you run Electrum it doesn’t connect to any of the external servers. You can do that if you do it carefully. Then you can get the xpub out of your Trezor or Ledger without it ever hitting the Trezor or Ledger servers but that is also not that easy. When you get a new Ledger it says “Go to this website. Install this program.” This program says “Welcome. Write down your seed and here is your balance” and now they know your keys. That’s why I use BIP32 addresses because the Ledger wallet doesn’t support those. Ledger doesn’t actually know those keys yet.

Q - You seem skeptical about this project but it is only because it is early?

A - I think it is not ready to use yet. But I am actually really optimistic. I can see how you could do this. It is not going to happen overnight but I can see where it goes. Multisig is more complicated and I like this idea of having this JSON-RPC standard that could work for different wallets and different signing services. I could see how people would find that useful. They would probably all have their own wish lists. Pretty optimistic.

