---
title: Signet Workshop
speakers:
  - Kalle Alm
date: 2020-02-07
transcript_by: Michael Folkson
tags:
  - taproot
  - signet
---
## Let’s prepare

```
mkdir workspace
cd workspace
git clone https://github.com/bitcoin/bitcoin.git
cd bitcoin
git remote add kallewoof https://github.com/kallewoof/bitcoin.git
git fetch kallewoof
git checkout signet
./autogen.sh
./configure -C --disable-bench --disable-test --without-gui
make -j5
```

When you try to run the configure part you are going to have some problems if you don’t have the dependencies. If you don’t have the dependencies Google your OS and “Bitcoin build”. If you have Windows you’re out of luck.

```
cd ..
git clone https://github.com/kallewoof/btcdeb.git
cd btcdeb
git checkout taproot
./autogen.sh
./configure -C --enable-dangerous
make -j5
```
In your src folder you should have bitcoind, bitcoin-cli and a couple of the binaries. If you are all done with this part you can go into your src folder and type `./bitcoind -signet` and hit enter.

If you have managed to sync up Signet do:

`./bitcoin-cli -signet getnewaddress`

You should get a `sb1…` address. Post this address in the Telegram group.

Q - Do you have to be fully synced to get a new address?

A - No you don’t.

`./bitcoin-cli -signet getbalance`

`ssh gcog`

`cd workspace/signet/src`

`./bitcoin-cli -datadir=$HOME/signet-sgniii getrawtransaction 4b9911….88c7 1`

`bitcoin-cli -datadir=$HOME/signet-sgniii sendtoaddress sb1…5spr 100`

`cd contrib/signet`

`./mkblock.sh ../../src/bitcoin-cli -datadir=$HOME/signet-taproot`

`./bitcoin-cli -signet getbalance`

`./bitcoin-cli -signet getunconfirmedbalance`

Some person out there set up their own Signet so we are getting blocks for it.

`./bitcoin-cli -signet getconnectioncount`

`./bitcoin-cli-signet getblockcount`

`./bitcoin-cli-signet getpeerinfo`

I have a network running with Signet Taproot right now. We will eventually switch to that one. If you are going to Stepan Snigirev’s hardware workshop this afternoon which I recommend you should do then you will be able to continue using the Signet Taproot setup that you have with coins and everything in his workshop with a hardware wallet.

`./bitcoin-cli -signet settxfee 0.00001`

`./bitcoin-cli -signet sendtoaddress sb1….8mg 1`

I am sending everyone 1 Signet Bitcoin. If you go to the [Signet block explorer](https://explorer.bc-2.jp/) copy the `AddToWallet` text string and put it into the block explorer. You should see it is unconfirmed, the fees etc.

## btcdeb

I am going to move onto the btcdeb part. This is the Bitcoin debugger that I maintain. It has experimental support for Taproot so I figured out we could use that.

```
cd ..
git clone https://github.com/kallewoof/btcdeb.git
cd btcdeb
git checkout taproot
./autogen.sh
./configure -C --enable-dangerous
make -j5
```

Q - I do have an issue with a config file.

A - You may have to remove the -C flag.

Q - What does the -C flag do?

A - It speeds up configure when you run it multiple times because it will cache all of the outputs. But I think there is an issue with libsecp that causes this to a problem the first time. You can do without -C.

## Remotes

Your fork of Bitcoin Core git@github.com:user/bitcoin.git

Upstream https://github.com/bitcoin/bitcoin.git

Feature remote https://github.com/owner/bitcoin.git

```
origin git@github.com:kallewoof/bitcoin.git (fetch)
origin git@github.com:kallewoof/bitcoin.git (push)
sipa https://github.com/sipa/bitcoin.git (fetch)
sipa https://github.com/sipa/bitcoin.git (push)
upstream https://github.com/bitcoin/bitcoin.git (fetch)
upstream https://github.com/bitcoin/bitcoin.git (push)
```

Right now Signet is not in Bitcoin Core which causes complications. The [Signet PR](https://github.com/bitcoin/bitcoin/pull/18267) is in the [high priority blockers](https://github.com/bitcoin/bitcoin/projects/8) category so hopefully it will be in 0.20 which is supposed be released in May. Until then we have to juggle GitHub repositories. Eventually you will be able to use the default Signet with any supported custom upcoming features. With Taproot or OP_CHECKTEMPLATEVERIFY or any potential soft forks, in the future if there are any soft forks, as soon as they are added to the Signet miner which is just one machine, anyone can turn these on and off however they want. If you want to mine Taproot you can grab the Taproot branch. You can send Taproot transactions and you can receive them. Right now it is a little manual. We will try to set up a custom Signet for the people here. We will pick one person who is the miner or a couple of people. We could do one of everyone in here if we wanted to. I would say just pick one miner. I don’t know if you are familiar with using GitHub but there is something called a remote. By default there is only one remote, it is called origin. It is whatever you type in after git clone. But you can add remotes. You can do `git remote add name URL` and then you have another remote.  You can do `git fetch remote-name` and it will fetch that. In this case I am creating a Taproot Signet network. I have my origin which is my Bitcoin repository. Because I am using `git@github` here I am able to use RSA keys instead of having to enter a password all the time. I am adding this sipa remote because sipa is the person who is doing the work in progress Taproot [pull request](https://github.com/bitcoin/bitcoin/pull/17977). You don’t have to add this, you could pull directly the pull request but this is in some ways easier. You can pull directly. Upstream is Bitcoin, you don’t really need upstream in this case. In your case you would replace origin kallewoof with your name.

## Branches

Because Signet is not merged yet there is a `signet` branch. As soon as it is merged into Bitcoin Core we don’t have that anymore. In our GitHub we create a signet branch and then we create a `signet-vanilla-taproot` (signet and network params). We have a `taproot` upstream feature branch which is sipa’s. Then we create a `signet-taproot` branch. That is feature (`taproot`) merged on top of `signet-vanilla-taproot`.

## Branches (post signet merge)

One it gets merged we won’t have a `signet` branch.

## Branches (future)

In the future we will only have a feature (`taproot`) branch (upstream feature with signet params). It is going to be a little finicky today but we’ll see how far we get.

## The signet branch

We have already done this part and you should have built this branch already.

(You can add https://github.com/kallewoof/bitcoin.git as a remote and then fetch it and simply checkout the signet branch)

```
git remote add kallewoof https://github.com/kallewoof/bitcoin.git
git fetch kallewoof
git checkout signet
```

(Alternatively you can fetch the pull request directly from the bitcoin remote)

```
git fetch upstream pull/16411/head:signet
git checkout signet
```

## The signet-vanilla-feature branch

(We create this once and then base our signet-feature branch off of it. If we end up wanting to reset signet-feature we do so by recreating it based on this branch.)

From the signet branch do

`git checkout -b signet-vanilla-taproot`

(And then tweak the chainparams.cpp file (we do that later)

Right now we are on the signet branch. What we want to do is change the chain parameters a little bit. If we use signet right after this it is going to use the whole signet which does not have Taproot support. If we are going to create a custom Signet for own feature, or sipa’s feature, we need to first tweak some chain parameters. We create this branch here `signet-vanilla-taproot`.

Q - This is in the Bitcoin repo?

A - Yes. btcdeb is already set up to work with this.

If you have done that you should now have a branch called `signet-vanilla-taproot`. We’re not going to do anything with that now but we are going to change the chain parameters later.

## The feature branch

(We keep this identical to owner (here “sipa”) and never diverge:

```
git remote add sipa https://github.com/sipa/bitcoin.git
git fetch sipa
git checkout taproot
git pull
git reset --hard sipa/taproot
```

sipa is Pieter Wuille by the way.

Q - …

A - Some other Signet was technically connected to us. You can exit if you want to or you can keep it running for now.

`git checkout signet-vanilla-taproot`

We have already created this `signet-vanilla-taproot` branch, check it out. I don’t think we are going to have time to do our own network so let’s use one that I have already made. In the Telegram I posted this code snippet from chainparams.cpp. In whatever editor you want if you open this file (chainparams.cpp) and then you go down to find the class called `SigNetParams`. There is this if case here and inside here is the default Signet parameters. You want to delete all that and then put this instead. I have posted that in the Telegram so you don’t have to type it manually.

```
LogPrintf("Using default taproot signet network\n");
bin = ParseHex("512103ad5e0edad18cb1f0fc0d28a3d4f1f3e445640337489abb10404f2d1e086be430210359ef5021964fe22d6f8e05b2463c9540ce96883fe3b278760f048f5189f2e6c452ae");
genesis_nonce = 280965
vSeeds.push_back("178.128.221.177");
```

Q - On which branch is this?

A - signet-vanilla.

I will quickly go through what this is. The `bin` part is the challenge. You probably recognize it. It looks like a normal Bitcoin script. What it does it says a 1 and a 33 byte push and a pubkey and a 1 and a CHECKMULTISIG. It is a 1-of-1 MULTISIG. The second part is a genesis nonce, I will talk about that. The third party is a seed, the computer that is running this version of Signet.

`git commit -am “new signet parameters”`

You should commit to your signet-vanilla-taproot repository with your new parameters. Once you have that you can merge this with taproot. When we run it we should be able to use Taproot.

Q - …

A - You don’t need to compile right now. If you want to compile that is probably a good idea to make sure you don’t have any errors.

We check out signet-taproot.

`git checkout -b signet-taproot`

And then we do the `git merge taproot`. If you have done `git checkout -b signet-taproot` already you may want to do `git merge signet-vanilla-taproot` first. When you’ve done that you do `git merge taproot`.

(We merge taproot on top of signet-taproot)

When you do the `git merge taproot` you are going to have conflicts. You need both parts but remove the verify witness program in the first part.

The reason why I am having you painstakingly go through this is because this is exactly what you are going to have to do if you ever have a feature yourself that you want to merge. You are going to have these merge conflicts that show up. We are now at the part where our Signet is working. If you manage to compile this and run it it will crash. The reason why it crashes is because you have an old Signet running. You want to delete the Signet folder in your Data. Let’s do that. Stop your running bitcoind.

`rm -rf ~/.bitcoin/signet`

For Macs:

`rm -rf ~/Library/Application\ Support/bitcoin/signet`

Remove that folder. You should be on the `signet-taproot` branch.

`make`

Once you have finished make:

`./bitcoind -signet`

If you remembered to delete the signet folder in your data it should now connect to a different Signet which has Taproot. This one started in January 2020. If you were back in 2019 you are using the previous Signet.

`./autogen.sh`

`./configure -C --disable-test --disable-bench --without-gui`

If you are running into compiler errors you may have to `./autogen.sh` and `./configure` again and then `make clean`.

## btcdeb

While we are waiting for some compiler stuff let’s take the last few minutes to see if we can do something with this. We have the btcdeb folder.

`cd btcdeb`

There is a `tap` man here that has a bunch of features.

`./tap`

The homework is to use this man to create a Taproot address and send that to me. If you send that to me I will send you some coins. This is all experimental and new. If you do this and run into problems, have bugs whatever, that is invaluable for the Bitcoin community. I really encourage you to do this. You may even be able to make a contribution to the current [pull request](https://github.com/bitcoin/bitcoin/pull/17977), the work in progress Taproot pull request on the Bitcoin Core repository. If people play around with this stuff and break it then we can improve that pull request. But it is all very new and experimental. I can show you an example. I don’t know if you have ever used btcdeb before. This version of btcdeb can handle BIP-Taproot spends.

`./btcdeb --txin=$txin --tx=020000…`

What I am doing is saying “This is the input transaction here and then this is the transaction and tell me what happens.” It says this is a SegWit transaction and gives the transaction data. Then here we come to the `Taproot commitment`. This has the `control` object. Have you heard about MAST? This is MAST implemented in Taproot. What Taproot does is uses MAST to prove that a particular script, this `script`, was actually added into the address at creation time. When you create the address you can insert any amounts of scripts you want but no one is going to see the scripts unless you use them to spend. In this case I am using this one to spend the transaction. The `control` object is saying that you use this data to derive the root of the Merkle tree. If you have a root of the Merkle tree and it matches then that script was committed. The ‘control’ object has a version byte and then it is followed by a pubkey. Pubkeys in Taproot are 32 bytes. If you are used to pubkeys in Bitcoin in general they are 33 bytes. They have 02 or 03 followed by a hex value. We remove the 02 or 03 and it is assuming they are a particular type. Then there is a `program`. There is `p` and `q`. `p` is the internal pubkey used to create this Taproot spend. Then there is some Merkle root stuff that goes on. What btcdeb does here is it steps through this commitment phase. There is this `final k` here and then there is a `TapTweak`. There is a `CheckPayToContract` here. This script only has one input so it doesn’t have a Merkle tree at all. Once this finishes with the Taproot commitment check we see the script being run. It is OP_SHA256, OP_EQUALVERIFY and then there is a pubkey and a OP_CHECKSIG. This is just like normal.

`btcdeb> step`

This is the result of the OP_CHECKSIG. You can see a few things here. It is a 32 byte pubkey so it is a `schnorr sig check`. This pubkey is different from the internal pubkey that we gave. This is part of the script, this is Alice’s pubkey. The internal pubkey is everyone’s pubkey that they share. We do the `VerifySchnorrSignature` and that works. There is a [document](https://github.com/bitcoin-core/btcdeb/blob/taproot/doc/tapscript-example-with-tap.md) where I go through an example which has two different scripts. [This](https://github.com/bitcoin-core/btcdeb/blob/taproot/doc/tapscript-example-with-tap.md) is the normal Bitcoin script. Instead of doing this OP_IF OP_ELSE OP_ENDIF thing we take this and the CHECKSIG as one script and we take this and the CHECKSIG as the other script. Whenever we spend it we don’t have to show the world all this stuff. We just prove that this was a possibility and we satisfy it.

Q - This is the Merkle tree part? You don’t provide the whole script, you only provide the path that you are executing.

A - Yes. This works exactly like the Merkle root inside transactions except there are some tweaks with version bytes and stuff.

If you look at it like this you are not saving a lot of space but you have to remember that these things are all big blobs, 32 byte values. If you look here you see this thing is kind of big. If you don’t have to show one of these you are saving space and saving fees. It is a huge improvement. If everyone agrees you can spend it as if it was a regular pubkey. That is a huge saving privacy wise and fee wise. Nobody is going to be able to separate your custom stuff with a normal pubkey if everyone is in agreement. Think about a payment channel in Lightning, how often do you have the other person not agreeing to close a channel? Usually they are like “Ok”. Normally you would just use the pubkey and be done with it. In this example I actually have the private key, normally you don’t. The way you do this is you use MuSig or something to create the internal private key. That way nobody actually knows the private key but you can still spend it. I didn’t get as far as I hoped but hopefully you got a start at least.

