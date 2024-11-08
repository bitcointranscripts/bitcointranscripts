---
title: Bitcoin Data Structures
transcript_by: Bryan Bishop
speakers:
  - Jimmy Song
date: 2019-09-09
aliases:
  - /scalingbitcoin/tel-aviv-2019/edgedevplusplus/bitcoin-data-structures
---
<https://twitter.com/kanzure/status/1170974373089632257>

# Introduction

Alright guys. Come on in. There's plenty of seats, guys. If you're sitting out on the edge, be nice to the other folks and get in the middle. Sitting at the edge is kind of being a dick. You're not letting anyone through. Come on guys, you don't have USB-C yet? You all have powerbanks. Get with the times. Okay, we're getting started.

I have 90 minutes to teach you the rest of my book. I think I did 2 or 3 chapters so far. It's a 14 chapter book. That means we have another 10 chapters to cover in the next 90 minutes. I'm going to cover these topics. It's a lot. We're going to go through how addresses are created, transactions, we're going to go through Bitcoin script which is the smart contract language behind bitcoin. Then we'll go through pay-to-scripthash, pay-to-witness-public-key-hash, and other segwit transaction formats. I was told that I need to cover all of this in 90 minutes. This is going to be a larger firehose of information than the last session. I hope you guys can keep up. If not, remember that everything is in my book, and it's open source so you can go read it online.

# Bitcoin address

The SEC (standards for efficient cryptography) format and it's a way of encoding a public point. Remember sG=P and P is your public point and s is your secret. We need to encode that somehow like when we store it on disk or transmit it over the network. You need some way to serialize it. This is the way.

There are two formats, compressed and uncompressed. Uncompressed starts with 04 and it has a 32 byte x coordinate which is 256 bits, and then 32 bytes for the y coordinate which is 32 bytes. It's essentially 65 bytes because there's the 1 byte marker 0x04. This is what was used early on. All the early bitcoin blocks are all 65 byte uncompressed public keys.

That is, until Pieter Wuille found out about the compressed format in the openssl library. So you take the x coordinate and then you figure out what the y coordinate is. Remember the equation that you were given. y and negative y end up being y and p-y and p is a prime number. So y and p-y have to be different, one is odd one is even. Any prime number above 2 is an odd number. There's one byte for the parity, and then the 32 byte x coordinate. This is a compressed format. 02 if y is even, 03 if odd-- this is the marker.

Here's what that looks like. How do we get an address from this? Given the SEC format, it's either compressed or uncompressed. So we use sha256 to hash the result and then we use RIPEMD160 the result. This is known as hash160. We pre-pad with a network prefix (0x00 for mainnet, and 0x6f for testnet). This is so that you don't send real bitcoin to a testnet address, or a testnet coins to a real address. If you don't know what testnet is, it's sort of like a "fake" bitcoin network for developers and the coins on testnet aren't supposed to be worth anything although they are scarce because bitcoin is scarce.

Hash256 is two rounds of sha256. We add a 32-bit hash256 checksum at the end. We encode this whole thing in base58, which is every capital letter and every lowercase letter and every digit, this gives you 26 + 26 + 10 which is 62. Then we eliminate confusing letters: 0 and O look similar so we eliminate those. Lowercase l and capital I also look similar so we eliminate those. So we eliminate those from the 62, and we get 58 numbers. That's how we encode it.

So we take the SEC format, we hash160 it, we prepend it with the network magic byte 0x00, and then we take that and we hash256 that value and use the first four bytes as a checksum that we append to the 0x00 || h160 value. One of my problems with ethereum is that it doesn't have a checksum. If you make a mistake with the address, then you send it into the aether. See what I did there?

So you encode it using base58, and then you get an address. This example here is a pay-to-pubkeyhash (P2PKH) address. It starts with a 1. Notice that all the rules of base58 were followed. The last 4 bytes in there are the hash256 which wallet software is supposed to verify.

# Bitcoin transactions

Here's the raw hex dump of a bitcoin transaction. I've color coded it for you. This, again, is in the book. The very first bytes... each pair is a byte, this is hexadecimal. The first four bytes are a version. This is in little endian. Little endian starts first, for little. There is transaction version 1, and then there's transaction version 2 and that's only if you're using OP\_CHECKSEQUENCEVERIFY which I think was introduced as part of bip68.

Bitcoin runs on a UTXO system. That means unspent transaction outputs. What you have to do for each input is have a reference to the previous output that you are spending. That's what we're going to do here. There's a previous transaction hash. It's hash256 (or two rounds of sha256) of the previous transaction, and this gives you a 32 byte reference to a previous transaction. Note that it's not the current transaction, it's some transaction that existed before. You also need to specify which output of that previous transaction you're spending in this input. You have to reference the index of the output in the list of outputs of that previous transaction.

scriptSig is a variable length value. There's a buried signature in here in this example. Then there's the nSequence value. This was originally conceived to do something called payment channels that Satoshi thought would be useful except it was completely broken and miners could attack it.

Every transaction can have one or more inputs, and one or more outputs. It can be any number, actually, as long as you don't violate other rules. It's one input and two outputs in this example. Each output has an amount, which is the number of satoshis that are being assigned to this particular output. Then the scriptpubkey. This is the address that you saw before-- it's essentially here. This is the spending conditions for this new output.

Finally, there's an nLocktime value that again Satoshi thought would be useful but you say-- it's only valid after some particular time or block. That's essentially what it's saying.

So this is what a transaction looks like.

Yes, you need a signature for each input. Coins can either be spent or unspent. Ethereum is different, they have accounts instead of coins and no UTXOs.

# Script

<https://diyhpl.us/wiki/transcripts/scalingbitcoin/tokyo-2018/edgedevplusplus/p2pkh-p2wpkh-p2h-p2wsh/>

<https://diyhpl.us/wiki/transcripts/scalingbitcoin/tokyo-2018/edgedevplusplus/scripts-general-and-simple/>

Both the input scriptSig and the output scriptpubkey use the bitcoin smart contract language called script. It's purposefully not Turing complete. Unlike ethereum, it's not turing complete, so it can't run infinitely. This is why ethereum needs this complicated thing called gas because otherwise you can ddos every node by running an infinite loop in a contract which would be bad because the whole network would stop working. By not being turing complete, bitcoin script is more limited and doesn't allow for infinite loops. It's sort of like the Forth programming language. It's a programmable way of assigning coins and spending predicates. Every bitcoin address does this.

There are elements and operations. Elements are data, like signatures or public keys. Operations do something, like OP\_CHECKSIG and OP\_HASH160 and OP\_DUP. You have to process all of the commands. If at the end you have the--- if the top element left on the stack is non-zero then it's considered a successful execution. If the top element is 0 or if there's no elements or if it terminated early then it's a failed execution. Every input has to end up with a successful execution for a transaction to be valid.

<https://en.bitcoin.it/wiki/Script>

Some opcodes of particular interest:

* OP\_DUP

* OP\_CHECKSIG

* OP\_HASH160

# Parsing script

Each byte is interpreted as an integer. If the byte is between 1 and 75 inclusive, the next n bytes are an element. Else, byte is an operation based on a lookup table which is defined as part of the language. OP\_0 puts a zero at the top of the stack. 0x93 is OP\_ADD, add the top two elements.

# Processing scripts

So you take the scriptpubkey from the previous transaction and then you take the scriptsig from the current transaction. You combine them and process them one at a time. The current transaction has a previous transaction output. It points to that. It points to a particular transaction via the previous transaction hash that points to this particular transaction. Within that transaction, you are told which output index to look at. That particular output has a scriptpubkey. This current input on the new transaction has a scriptsig. So you take the scriptsig and scriptpubkey elements and combine it into a particular script.

# Popular bitcoin scripts

* p2pk - pay-to-pubkey
* p2pkh - pay-to-pubkeyhash
* p2sh - pay-to-scripthash
* p2wpkh - pay-to-witness-pubkeyhash
* p2wsh - pay-to-witness-scripthash

Let's talk about pay-to-pubkeyhash. The scriptpubkey determines what the scriptsig is going to need to be, in order to unlock the funds. Think about the scriptpubkey as the "lock box" that the bitcoin is "in". You define a lockbox in a particular way.

Note that only the pubkeyhash bytes really change when using p2pkh.

Pay-to-scripthash is different from pay-to-pubkeyhash. To use p2sh, you need to use a redeemScript that can serve as the preimage to the hash (required in the scriptsig) placed in the original scriptpubkey.

<https://diyhpl.us/wiki/transcripts/scalingbitcoin/tokyo-2018/edgedevplusplus/p2pkh-p2wpkh-p2h-p2wsh/>

OP\_CHECKMULTISIG checks if m of the signatures are valid of the n public keys for the current transaction. Puts 1 back on the stack if valid, and 0 otherwise. You can do 2-of-3, 4-of-5, all sorts of things. Turns out, OP\_CHECKMULTISIG has an off-by-one error. It consumes one more stack element than it is supposed to. This is a bug that Satoshi originally introduced. To make it backwards compatible ,it's always using this initial 0 value that you have to place there.

You can use OP\_CHECKMULTISIG in conjunction with OP\_OR or other schemes. So you can have things like, after this amount of time, these other keys are acceptable or something.

# Block parsing

Let's talk about blocks. Here's the block data structure. This is just a raw hex dump of a block. It has a block header, then the number of transactions, and then every transactions in the block in order. The nice thing about a blockheader is that it's only ever 80 bytes. Right now we're a little under 600,000 blocks in the blockchain. So 600,000 times 80 bytes is like 40 megabytes. In fact, this could fit on your phone. A lot of lite wallets essentially only download the block headers.

The blockheader has the version number, which is similar to the one used for a transaction. The version encodes a bunch of stuff, actually. Every block has a-- if you has256 the block, two rounds of sha256, you get the block ID. That block ID is chained-- this is why it's called a blockchain-- every block points to a previous block. So it includes a value that is hte hash of the previous block. It goes all the way back to the very first one, which is called the genesis block.

Then you have the merkle root. I don't know if I'm going to cover it. Then there's a 4 byte timestamp, which is a unix timestamp. Then there's nBits and nonce which we will get to.

The block version is stored as a little endian value, so 0200020 is stored as 0x20000002. bip9 versionbits readiness is signaled with the top 3 bits. The reason for switching to bip9 for activation is that, if you just have version rolling and increasing by one, then you can only implement and deploy one soft-fork at a time.

The timestamp is calculated by median time past. The timestamp is stored in little-endian unix time. The nBits are the bits determining target and difficulty. The nonce is space to tweak the block header to get proof-of-work. The nonce space is 32 bits, which is not nearly enough to compute proof-of-work. 32 bits is about ~4 GHash and an Antminer S9 does 9 TH/second. It will roll through the nonce space in a microsecond. That's just one machine, and we have many of those out there.

# Proof-of-work

What is proof-of-work? It's a way to give someone the right to publish a block. The nice thing about a proof-of-work system is that you don't need anyone's permissions. It's a way to distribute the control of the blockchain and to secure it. To roll back a block requires just as much energy as creating a block. To rollback 2 blocks, it requires as much energy to generate those two blocks, and so on.

Essentially what PoW is is that it's creating a hash below a target number. You take a hash and interpret the 256 bit value as a number. That number has to, essentially, be very low, below the target value. The probability of finding a winning value can be adjusted based on the target.

The difficulty gets adjusted every 2016 blocks. Because blocks come on average once every 10 minutes, and 2016 blocks is about 2 weeks. The difficulty adjustment algorithm looks at the performance over the last 2 weeks; if the previous 2016 blocks took less than 2 weeks, then the difficulty gets harder. If it took longer than 2 weeks, then the difficulty gets easier.

# Calculating target from nBits

The exponent is the last byte. The coefficient is the first 3 bytes in little endian. You plug this into a particular formula where you do coefficient * 256^(exponent - 3). When you do a hash, you end up with a random number. You are trying to grind and find a value that makes this hash hit the requirement where it has a certain number of leading zeroes, and the value has to be below the target value. It's extremely improbable that it has this many leading zeroes. You have to calculate a lot of different hashes to get below this number.

To give you an idea, to find the hash that's below this target, you have to calculate on average 3.8 * 10^21 or 3.8 sextillion hashes. At this difficulty it would take the fastest GPU on the market (which does 2.5 GH/sec) about 50,000 years to find a hash that satisfies that Proof-of-Work difficulty level.

# Calculating difficulty from target

If you look at the blockheader, notice that the previous blockhash ends in a lot of zeroes. And it's for that reason-- it had to meet a particular PoW target. The bits tell you right away what the proof-of-work would have to be. I'm told that for gold mining, you need to go through 42 tons of dirt and rock before you can find 1 oz of gold. This is why we call it bitcoin mining. You have to go through the equivalent of numerical dirt and rock before you find the right value. Once you find it, just like gold, it's easy to verify. But in proof-of-work it's even easier, you just sha256 this thing twice and then check the number of leading zeroes which is extremely improbable meaning someone or the entire network expended a lot of energy trying to find this.

Target is easy for a computer to figure out, to compare two numbers. But for a human, it's not intuitive. To give us a more intuitive way for humans to understand it, we came up with a concept of "difficulty" which is essentially the reciripocal of the.... So you take the lowest target and divide by target. Right now it is 888 billion times more difficult to find a proof-of-work than it was back when bitcoin started. Of course, the difficulty is higher now.

# Segwit

What is segregated witness (segwit)? Well, it was first proposed as a fix for transaction malleability which is useful for the lightning network where you want to pre-sign some transactions before funding other earlier transactions. Segwit is also helpful for reducing network transmission. As a result, it's a way to increase transaction throughput. It's a block size increase, which many segwit opponents refused to acknowledge. It's also a way to allow for smooth future upgrades. We're right now in segwit v0 and part of the taproot proposal is what's going to probably going to be segwit v1. The one after that will be segwit v2, and son.

Here's the transaction that I showed you earlier, for pay-to-pubkeyhash. And here's pay-to-witness-pubkeyhash. It's significantly smaller. The chunk that is missing is the part that houses the DER signature. For multisig, this would be even bigger, there would be giant yellow sections in this diagram. This is known as the multisig penalty of course.

# Pay-to-witness-pubkeyhash ("native segwit")

You can identify P2WPKH because it starts off as bc1, and it's the shorter version, as opposed to pay-to-witness-scripthash (P2WSH) which is another one. So, P2WPKH acts like P2PKH but segregates the scriptSig data and puts it somewhere else. It's a new type of script, so it has a new address prefix, starting with bc1. The key to making it backwards compatible is that different data is sent to non-upgraded nodes vs upgraded nodes.

The non-upgraded nodes are given an empty scriptSig. This works because of a trick in the scriptpubkey. For upgraded nodes, the nodes know where to go find the witness commitments. The witness field has a DER signature and also has a SEC pubkey in there. Those two things used to be in the scriptSig field. The nice thing is that the txid is based on the non-upgraded transaction, this serialization.

# P2SH-P2WPKH

What about P2SH-P2WPKH? They came up with this for backwards compatible. It's a way to make segwit backwards compatible. All wallets, even if they don't know about segwit, can spend to a segwit wallet. It wraps the entire segwit thing around p2sh. It looks exactly like a p2sh address. These are addresses that start with a 3. You might have seen some of these and suspected they were segwit addresses; you don't know, it could just as easily be a p2sh multisig or something.

The segwit nodes will interpret this special rule: OP\_0 followed by 20 byte element is evaluated to mean that this is now evaluated as script elements. But this is still backwards compatible with pre-segwit nodes because OP\_0 would be put on top of the stack. There's two special rules used here, to make it all backwards compatible. Soft-forks means it's always backwards compatible, all the way back to before P2SH was originally implemented years ago. Even if you're a very old node, it would still work. You validate as much as you can, which won't be as much, but you will still see things as valid.

# Other

<https://github.com/jimmysong/programmingbitcoin>

Note that fees are the inputs minus the output amounts. Each input has some number of satoshis from the previous transaction output. You add those up. Then you add up all the outputs. You need to be zero or positive, otherwise you're creating new coins which makes it invalid. If it's positive, then that positive amount is paid to the miners as a subsidy fee. That's how you incentivize miners to include your transaction.

# Q&A

Q: So we moved the signature from the scriptSig to the witness. How does this reduce the size of the transaction?

A: Well first, it's optional to transmit this data to the other node. It's only if they want the data. Also, if you're an older node, you don't store any of the script witness data because you don't even know about it. In that way, it's less resource intensive. Newer nodes, though, can do validation. It's essentially the same transaction size. I think it's slightly bigger because of the witness marker and-- there's a couple of things there. With segwit v1, I think you get stuff like Schnorr which lets you aggregate signatures like for multisig. I think we're getting rid of DER signatures too.

Q: I didn't quite understand the nBits field in the blockheader. Also, how do you calculate difficulty adjustment?

A: The nBits field encodes a very large number into four bytes. If you encode the entire number, it would be 32 bytes. But compressing it to 4 bytes is very nice. You don't get quite the resolution you would get with 256 bits or whatever, but that's the idea. The formula that I showed you is a common way to encode a number that big. As far as the difficulty adjustment, the formula is in the book. You can essentially encode the number fairly--- I don't think I have it in the book's code. Or maybe I do. Okay, `calculate_new_bits`. The time differential value is how long it took over the last two weeks * 4. If it's greater than 8 weeks, set it to 8 weeks. The maximum it can increase is by 4. The minimum it can decrease by is 1/4th. The new target is, according to this formula, you take the previous bits times the time differential divided by 2 weeks and then the new target is going to-- if it's bigger than the max target, then it's set to the max target, and then you convert back to bits. All of this is in the book and you can read about how exactly that works. It doesn't have to be a multiple of 2 or anything, it's finely grained.

Q: You skipped over the merkle root part of the blockheader.

A: I hesitate to talk too much about it. For SPV, I think that's going to be dead soon. You can encode all of the transactions into a merkle tree and into a 32 byte value known as the merkle root of that merkle tree. There's a concept of a merkle parent, which is you take two hashes, you concatenate them, and in our case we use a double sha256 hash function on that value. If you have a whole list of them, you can take a merkle parent of every pair, and the merkle root is you keep doing that until you end up with a single merkle parent and that's your merkle root. You can validate that a particular hash is a member of the merkle tree by revealing the pairwise complement all the way up the tree and prove that a particular transaction was included in a merkle root. That has its own vulnerabilities of course; I think there was a CVE issued for that. This is why I think [neutrino](http://diyhpl.us/wiki/transcripts/breaking-bitcoin/2019/neutrino/) is really the future.

Neutrino gives you a fingerprint on all the transactions in a particular block. If any of your addresses match that filter, then you just request the entire block and look for your transactions instead of the server proving that a particular transaction is a member of a block. There's privacy improvements by using neutrino. The server could otherwise cheat by telling you it's in there when it's not otherwise in there. A coinbase commitment might be required to commit to a particular filter, for Neutrino to work. So this would require a soft-fork.

Q: How does the witness root thing work in the coinbase transaction?

A: Coinbase transactions are different. They are the only transaction allowed to create new bitcoin. It has no inputs. It's supposed to have only one input and people can put anything they want into the scriptSig of that one input. If you look at the coinbase transaction for the genesis block, that's where Satoshi put his "Chancellor on the brink of second bailout for banks" message. The outputs, though, you can have as many of those as you want. You can put something into the coinbase scriptSig arbitrarily, like bip34. You can put a commitment to a filter in there. I think the current way is a witness commitment into --- is it the OP\_RETURN of the first output of the coinbase transaction? There's a commitment to the witness merkle root. Basically, you hack stuff into the coinbase whenever you want to add that. Again, this is something that everyone has to validate. It's a whole network cost when you put in a coinbase commitment. Greg Maxwell has pointed out that when you soft-fork something in and it ends up being a dud then it takes a hard-fork to remove it.


