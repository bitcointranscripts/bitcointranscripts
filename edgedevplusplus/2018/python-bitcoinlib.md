---
title: Interfacing with Python via python-bitcoinlib
transcript_by: Bryan Bishop
speakers:
  - Bryan Bishop
date: 2018-10-05
media: https://www.youtube.com/watch?v=JnBOO1zjm4I
aliases:
  - /scalingbitcoin/tokyo-2018/edgedevplusplus/python-bitcoinlib
---
python-bitcoinlib repo: https://github.com/petertodd/python-bitcoinlib

Bitcoin Edge schedule: https://keio-devplusplus-2018.bitcoinedge.org/#schedule

Twitter announcement: https://twitter.com/kanzure/status/1052927707888189442

Transcript completed by: Bryan Bishop Edited by: Michael Folkson

# Intro

I will be talking about python-bitcoinlib.

# whoami

First I am going to start with an introduction slide. This is because I keep forgetting who I am so I have to write it down in all of my presentations. (Joke)

Before I get started, there is a presentation right after mine that is about libbitcoin. That is a separate project. This is python-bitcoinlib. Sorry for the ambiguity but it is not my fault.

# What is python-bitcoinlib and where to find it

Retrieve from: https://github.com/petertodd/python-bitcoinlib

`pip3 install python-bitcoinlib`

python-bitcoinlib is a library of Python classes, functions and other little helper methods for representing, parsing and serializing Bitcoin data. Running Bitcoin scripts, evaluating Bitcoin scripts. It is a Python library. It is very useful for application development, for testing, things like that. Before I get too deep into this, I’m quite curious. Can I see a show of hands for who actually writes in Python in this audience? python-bitcoinlib is useful if you are doing rapid application prototyping or something. It is not a full node implementation. I suppose you could in theory make a full node implementation from it but there are a lot of pieces missing so it is not a full node.

# Library history

I believe originally this was started by Jeff Garzik as python-bitcoinrpc and then it evolved over the years passing from maintainer to maintainer or fork to fork. There are also a few other forks flying around, one called python-bitcoinrpc1 I believe made it into the Bitcoin Core repository for testing of Bitcoin Core. There are a lot of Python scripts there. Anyway that is a separate branch and separate evolution of the library. python-bitcoinlib itself is currently hosted under Peter Todd’s repository. He is ostensibly the maintainer although he warns that it will go unmaintained very soon or already has. That is something that people are going to have to deal with. Peter has been more interested in Rust lately which I will mention in a moment.

# Library structure

`bitcoin.core` - Basic core definitions, data structures and (context independent) validation

`bitcoin.core.key` - ECC pubkeys

`bitcoin.core.script` - Scripts and opcodes

`bitcoin.core.scripteval` - Script evaluation/verification

`bitcoin.core.serialize` - Serialization

`bitcoin` - Chain selection

`bitcoin.base58` -  Base58 encoding

`bitcoin.bloom` - Bloom filters (incomplete)

`bitcoin.net` - Network communication (in flux)

`bitcoin.messages` - Network messages (in flux)

`bitcoin.rpc` - Bitcoin Core RPC interface support

`bitcoin.wallet` - Wallet related code, currently Bitcoin address and private key support

So what does the library have? It has some of the basic data structures you’d expect such as representing transactions and blocks. It has a basic ability to represent keys and secret keys, things like that. Also opcodes and scripts, it can represent scripts and parse abstract syntax tree formats. It is not really a tree, it is a list of operations. It can evaluate scripts and verify them as well. Also it can serialize data, it can construct certain network messages, it has a basic ability to interface with RPC. It has a bunch of items and fun things you can do.

# Mutable vs immutable data structures

In python-bitcoinlib there is a distinction between mutable data structures and immutable data structures. This is a little odd because Python is generally considered to be not the right language to use if you want to preserve memory correctness which you generally want to do when you are dealing with Bitcoin. The theory behind this is if you are going to handle transaction data in Python or any other language, at least you want to try to mark which ones are final and aren’t going to be modified. In python-bitcoinlib that is `CMutableTransaction` and `CTransaction` is the immutable version. Whereas if you create a `CTransaction` and you initialize the data structure with a list of transaction inputs and a list of transaction outputs, the `CTransaction` type is not going to allow you to add extra inputs because theoretically you have already defined the transaction. The transaction should not be able to be updated after that point.

(From slide - Unlike the Bitcoin Core codebase this distinction also applies to `COutPoint`, `CTxIn`, `CTxOut` and `Cblock`. This is helpful for preventing mutation of transaction data in memory throughout a Python application but this is not Python’s superpower.)

# Endianness gotchas

Also Bitcoin Core shows transaction and block hashes as little endian hex and everything else is big endian hex. There are some conversion tools to be able to play around with data. This is very useful if you are ever on the command line just playing around with Bitcoin stuff.

`x` is the function for big endian hex to bytes. Since it is used so often it had a one letter name. This is really terrible if you are in the habit of using one letter abbreviations for names for your variables when you are doing rapid prototyping or testing. Just be aware that `x` is actually a function.

Similarly there is a function which is `lx` little endian hex to bytes. Or `b2lx` which is bytes to little endian hex and `b2x` which is bytes to big endian hex.

# Other stuff in python-bitcoinlib

The library helps you use both testnet and mainnet. The way it does that is switching through a function called `SelectParams`. `SignatureHash` is for transaction signing and hashing the transaction in the correct format so you can sign it. I believe it does have transaction signing capability using OpenSSL although you should probably not intend to use it for that purpose. Perhaps for testing it is fine. `VerifyScript` seems to be consensus correct. You can run a script through it and check whether or not it ends up returning TRUE or FALSE. There are a bunch of unit tests and you can do pay-to-script-hash for multisig although it doesn’t implement BIP 32. For that I use pycoin’s `BIP32Node` class when I need to use BIP 32.

# RPC

There is a RPC library for communicating with Bitcoin nodes, in particular Bitcoin Core. I have often found that I’ve needed to write a wrapper around the RPC connection function especially if you ever use this in a high volume environment where you are rapidly in succession querying the Bitcoin Core RPC. There is a RPC thread limit and sometimes you need to refresh the connections. Often I write a decorator around this RPC make-connection or any other RPC call to refresh the connection in the event that an error like that occurs. One interesting thing to note here is that when you are developing an application that uses Bitcoin Core you should be careful not to treat Bitcoin Core as a database because it is really not a database. Even though some of the RPC interfaces used to pretend it was, especially around accounts. Accounts were a good example because if you issue a RPC command to change an accounts, I guess a benign one would be to change an account’s name or something, it is not really a transactional interface like you would with a Postgres database. In the event that other things in your software stack have failed you would have to manually go back and fix all the things that you’ve told Bitcoin Core to do. There is no transactional atomicity guarantees.

(From slide - I have often found myself using the `_call` helper. I have often needed to write a wrapper around the make-new-RPC-connection function so that when RPC commands are called, a new RPC connection is established regardless of whether the connection is stale. Bitcoin Core RPC isn’t what you think it is (this is not database software with transactional capability or integrity guarantees) FakeBitcoinProxy class (available in a pull request) helps make unit tests without running bitcoind (mocks of bitcoin RPC)

# signmessage / verifymessage

https://github.com/petertodd/python-bitcoinlib/blob/master/examples/sign-message.py

Another useful thing in here is `signmessage` and `verifymessage`. This is very useful for audits or proving that you have control over a certain key. It is not just signing a message or a hash of a message directly. Rather there is a weird prefix. This isn’t the fault of python-bitcoinlib, this is a Bitcoin Core thing if you want to comply with this `signmessage` `verifymessage` standard. In fact there is a new standard being proposed for pay-to-witness-pubkey-hash. In certain situations you need to be able to prove that you have control of a certain output or whatever. `signmessage` doesn’t support all of those scenarios. Your wallet software needs to know how to produce those signatures and verify those signatures. One of the reasons why there is a prefix is so that you can’t do attacks. If you just ask an arbitrary user to sign this message to prove you have control and oops it is actually a transaction that you sign that spends all your coins to me, that would be a pretty bad vulnerability. Having a prefix makes sense. Also it uses something called ECDSA pubkey recovery. This is an interesting thing. I know it is completely off topic but in Ethereum, if you have ever looked at the Ethereum transaction data structure, unlike Bitcoin it doesn’t use UTXOs, it uses credits and debits. There is actually no “from address”. The address from which an account is debited in Ethereum is derived using ECDSA pubkey recovery. Similar to `signmessage` in Bitcoin, to derive the “from account” from the signature on the Ethereum transaction. I regret knowing this. I don’t want to know this but anyway. The URL at the bottom of the screen is an example of using `signmessage` and `verifymessage`.

# Example: Spend p2pkh UTXO (1/5)

https://github.com/petertodd/python-bitcoinlib/blob/master/examples/spend-p2pkh-txout.py

I am going to walk through an example of spending a P2PKH output. This scenario is that if you are paid and then you want to spend the money that you’re paid, this is an example of how to go about doing that using python-bitcoinlib. This page of code is setting it up and importing all the required functions, libraries and tools. Line 25 on the screen if you can see it, it is the longest line on the page, it is importing some of the script opcodes. `OP_HASH160`, this is P2PKH so there is a hash in there. There is a CHECKSIG because you want to check the signature, whether it matches. You need to do a `SignatureHash` because you want to sign the input. The next line, you have a `VerifyScript` because you want to check it is actually working. Also `SelectParams` is mainnet because you want to use mainnet not testnet. That’s where you are paid.

# Example: Spend p2pkh UTXO (2/5)

Before we begin, transactions have inputs and outputs. If you are spending this input, you were paid some Bitcoin and now you want to spend it, the transaction that you are creating to spend your money that you’ve earned is going to have to have an input. For the sake of example we can just arbitrarily say we were paid with this transaction hash ID. The next one (`vout`) is the index in that transaction of course. At the very bottom we are creating a transaction input based off of that transaction ID and the index.

`txin = CMutableTxIn(COutPoint(txid, vout))`

# Example: Spend p2pkh UTXO (3/5)

Then we also have to make the scriptPubKey. Also we are going to make a transaction output because we are spending it. This address is provided by whoever we are spending the money to so that is not our data.

`txin_scriptPubKey = CScript([OP_DUP, OP_HASH160, Hash160(seckey.pub), OP_EQUALVERIFY, OP_CHECKSIG])`

`txout = CMutableTxOut(0.001*COIN, CBitcoinAddress('1C7zdTfnkzmr13HfA2vNm5SJYRK6nEKyq8').to_scriptPubKey())`

# Example: Spend p2pkh UTXO (4/5)

`tx = CMutableTransaction([txin], [txout])`

Finally we are making a mutable transaction. That is because we are not done creating the transaction, we can have these inputs and outputs. If you notice the input hasn’t been signed yet. Then you have to figure out what are you signing. That is what the signature hash is for.

`sighash = SignatureHash(txin_scriptPubKey, tx, 0, SIGHASH_ALL)`

You sign the scriptPubKey from the transaction and we want SIGHASH_ALL because we want to ensure the transaction doesn’t change.

`sig = seckey.sign(sighash) + bytes([SIGHASH_ALL])`

This is pretty insecure. Don’t do this in production code. This is using OpenSSL under the hood. For the sake of testing, examples and demos it is about as good as you are going to get. It is just a function, sign this please. It produces a cryptographic signature and then you can add the signature to the actual scriptSig on the input.

`txin.scriptSig = CScript([sig, seckey.pub])`

Line 70, you have already created the transaction earlier at the top line of this slide. Now we are modifying it by adding a scriptSig. That’s why it needs to be mutable.

# Example: Spend p2pkh UTXO (5/5)

Then we can verify that the scriptSig works based off of the scriptPubKey for that input.

`VerifyScript(txin.scriptSig, txin_scriptPubKey, tx, 0, (SCRIPT_VERIFY_P2SH,))`

In python-bitcoinlib it will just fail with a raise an exception. I’m not going to catch the exception here. Finally there is a serialize method at the very end. You want to convert that to hex because serialization always produces bytes and you want some pretty printed hex so that you can copy and paste that into `sendrawtransaction` in the Bitcoin Core RPC interface.

`print(b2x(tx.serialize()))`

# Future improvements (wish list)

Some things notably absent from python-bitcoinlib. If you are going to implement something related to SegWit, don’t, because there is nothing implemented in there to handle SegWit. It is something important to note. It doesn’t have bech32 from BIP 173. It doesn’t have BIP 32 support. It doesn’t support BIP 174 (PSBTs). It doesn’t support output descriptors which I recognize that we haven’t talked about this past two days. There is no generally accepted proposal yet for script v2. Interestingly enough this will probably be called script v1 which is very confusing. That is because Bitcoin script is currently version zero. These guys are laughing over here but it is actually a huge problem. It is very ambiguous. Why is it still using OpenSSL? Who knows? In general for signing the signature is still going to be correct no matter which of the two libraries you are using. Perhaps an ability to switch out between the two, that would be an interesting project to implement. A simple weekend thing or something.

# That’s all, folks

That’s python-bitcoinlib. Just to be clear that’s not libbitcoin. Thanks

# Q&A

Q - This is completely different from bitcoind?

A - This is not related to bitcoind although the RPC interface, if you want to communicate to a Bitcoin node on the other end it would be bitcoind.

Q - When I look at this it seems like a great learning tool but who else uses it? What are the use cases?

A - I have used this in many projects for application development for everything from making exchanges for handling deposits and withdrawals. Anytime I have handled Bitcoin transactions. My two main options have been either write something in bash with the bitcoin-cli, `createrawtransaction` interface or you can use some other language other than bash. Why would anyone want to write in bash?

Q - I am one of the people working on bitcoinjs-lib and SegWit support is really hard.

A - That’s not my job.

Q - It sounds like people are using this for production code.

A - Yes

Q - It is scary that you mentioned that it is probably already unmaintained and it doesn’t support of all of these things.

A - Yes

Q - What is the history of maintainership?

A - Poor

Q - I think there’s an opportunity if you are into Python, this is a way to get involved in Bitcoin development.

A - Absolutely. In general it is considered a bad idea to use unmaintained code. At the same time there is a collection of work that has been performed here that could be useful. Some of the data structures are quite basic and they are not going to be deprecated. There are bits and pieces that you could probably safely use. Other parts that you should probably stay away from. Unfortunately this requires expertise to tell the difference.

Q - If someone is good at Python who could they talk to about reviving this as a maintained project?

A - Feel free to talk to me or Peter Todd. He makes himself available. Those are the two starting places I would recommend.

