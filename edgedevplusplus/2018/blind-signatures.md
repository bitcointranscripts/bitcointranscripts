---
title: Blind Signatures
transcript_by: Bryan Bishop
speakers:
  - Ethan Heilman
tags:
  - cryptography
media: https://www.youtube.com/watch?v=3Y25x3yAfpA
date: 2018-10-04
aliases:
  - /scalingbitcoin/tokyo-2018/edgedevplusplus/blind-signatures
---
<https://twitter.com/kanzure/status/1047648050234060800>

See also <http://diyhpl.us/wiki/transcripts/building-on-bitcoin/2018/blind-signatures-and-scriptless-scripts/>

# Introduction

Hi everyone. I work at Commonwealth Crypto. Today I am going to be talking to you about blind signatures. I'd like to encourage people to ask questions. Please think of questions. I'll give time and pause for people to ask questions.

# What are blind signatures?

A very informal definition of blind signatures is that they are a signature scheme that allows one party to sign a message without learning the message they signed. If you think about this, this sounds strange. Often signatures are used to authenticate someone saying something. Like someone proving that Alice authenticated a message, but it's difficult to imagine Alice authenticating a message she doesn't know. It's not the opposite of what signatures are designed for, but it's odd. Alice has authenticated something, but she can't recognize later what it was other than the fact that she authenticated it. One metaphor for describing this is imagine you have-- how many people know about carbon copy paper? You have a piece of paper, and you write on top of it, and the signature goes into the paper below. Imagine creating a contract and then hiding what the actual contract says and have someone sign in carbon copy on top. They can just see that the paper underneath has a signature. So it's a strange thing.

# History of blind signatures

Blind signatures were invented by David Chaum in 1982 for a specific purpose, namely for an early centralized digital currency called "anonymous ecash". Anonymous ecash enabled a trusted party to issue and redeem coins without learning to whom these coins were spent. The bank could issue the coins and the bank couldn't tell how the coins were spent. The bank would know that they issued some coin to Alice, and the bank would not know that Alice paid Bob. They would not be able to link the two coins.

# Non-anonymous ecash

To explain blind signatures, I'm going to first explain anonymous ecash. But first I'll explain not-anonymous ecash. THe bank has a public key and a secret key (PK, SK). Bank debits Alice's account. Issues her a coin by signing SN. Alice wants a coin so she can pay Bob. Alice is going to ask the bank to debit her account a certain amount and issue her a coin. The way in which the bank issues a coin is that Alice chooses a random number which we call the serial number or SN. The bank signs the serial number, basically saying I've authorized one coin to Alice and I'm going to use the sigma symbol to represent a signature. So the signature is over SK and the serial number SN. So a coin is a serial number and sigma (the signature). Bob gets this but there's a problem- Bob doesn't know if Alice has sent this to someone else. So it requires Bob to ask the bank and to use the bank to detect and prevent double-spending. Bob sends the coin to the bank and the bank checks that the serial number has not been used before. If it has been used before then this would be considered a double spend. So the bank would check that the sigma value is a valid signature under the bank's secret key. If it is, then the bank takes the coin from Bob and credits Bob that coin in his bank account until Bob asks for some new coins to be issued and his account is debited.

The above scheme does not provide any privacy. The serial number that Alice gave to the bank to be issued the coin, can be linked to the serial number when Bob redeems the coin at the bank. Clearly the bank can tell and follow the link.

To solve this problem, blind signatures were invented. I am going to be talking about RSA blind signatures but there's many others out there.

# Blind signatures

Alice chooses a random serial number SN. Alice blinds the serial number with a random number r (the blinding factor). So there's a function to compute a blinded serial number (bSN) like Blind(r, SN). The signer signs bSN to generate a blinded signature (bsigma). The signer does not actually see what the serial number is. It only sees this blinded serial number. Alice unblinds the blind signature to a signature on the serial number. She has a function unblind and it takes Unblind(r, blinded sigma) and get the real signature back. Now Alice has a signature on the serial number but she has never revealed the serial number to the bank (the signer).

# Anonymous ecash

Let's use blind signatures to make the ecash scheme have some anonymity. Alice blinds her serial number using a random value r. The bank signs the blinded signature number. Alice unblinds the blinded signature and then she can pay Bob and Bob is able to redeem the serial number and signature at the bank. The bank can then make sure the serial number has not been spent before and that the signature is valid. This is the first time that the bank has seen the serial number.

Q: If Alice sends the coin to multiple people, then the first Bob that talks to the bank can get the money.

A: Correct. This is different from bitcoin. This is from 36 years ago. Bob might be running a merchant store on the internet. If he gets money from Alice then he has to go to the bank immediately and redeem the coin. Otherwise Alice might spend the same coin somewhere else.

# Blind signatures are unlinkable

Any blinded signature can be unblinded to any other serial number. A blinded serial number can't be linked to any serial number. If you want to say whether these two are related, a blinded serial number and then the serial numbers that were... I could always invent an r value that would relate them in that way. Since I can always invent an r value, then there's no way that a certain blinded serial number unblinds to a certain serial number. It's similar to one time pads. You can always invent a key that will relate a ciphertext and a plaintext; so you don't learn anything or any connection between the two of them.

Timing attacks are fairly powerful especially when there's a limited number of users, or where users behave in certain ways. Imagine every user in the system gets a coin and then immediately spends it. Timing attacks can reveal then which users are spending those coins. The bank doesn't really know for sure, but the anonymity set is not great in that scenario. These timing channels are very important to think about when using a system like this. You could have a system that has total unlinkability but it has only one user and then you always know what that user is doing. You need a crowd to hide in. The user behavior has to be such that it also provides a crowd, they shouldn't just instantly spend.

# RSA blind signatures

I am only going to be talking about RSA blind signature schemes. There's a large number of alternatives. There's BLS signatures have blind signatures components, there's many out there. BLS signatures are like 32 bytes. There are blind signatures out there. I'm talking about just RSA blind signatures because that's the first one that was invented. RSA is the original blind signature scheme and the easiest one to understand and the one that most people are using right now.

# RSA signatures

PK = (e, n) and SK = (d, N)

RSA(PK, x) = x^e(mod N)

You have a public key which is a value (e, n). And you have a secret key which is a value (d, N). All the operations are going to be done in mod N where N is the product of two primes. The important thing to take away is that you have two operations you can do here for RSA-1. You have the first one which raises some value x to the value e mod N and you have the second one which is RSA inverse which raises some value y to this value d which you see associated with the secret key mod N. If you choose some x and apply this RSA operation to it and then apply the inverse, what will end up happening is that you get x mod N back out because the e and the d will essentially cancel because they are inverses of each other and you will just get x.

A really simple version of an RSA signature scheme is you take a message, you hash it, and then you compute the inverse RSA on this. You have to be very careful about the hash function used. There's a lot of important details. Nobody should go write code based on this slide. At a high level, you hash a message, you compute the inverse RSA operation and this gets you a signature. When you want to verify, you take the signature, and you do the regular RSA operation. Because they are inverses, you will end up with an output that is the hash of the message mod d and since you have that you can compare them.

# RSA blind signatures

For blind signatures, it's similar but with one extra step. You take the hash of the message and remember that blinding factor r? You're going to take r and raise it to e (essentially raising it to the public key) and you're going to multiply that against Hash(message). This is the blinded message or blinded serial number when we're talking about anonymous ecash.

When you go to send this to be signed, the signature is this inverse RSA operation where you raise the blinded message to d (mod N) and when you work out the math it's (Hash(m)\*(r^e))^d mod N.... So it's Hash(m)^d * r (mod N). TO unblind it's another equation here. There's also a way to do verification.

You're going to divide the r out. You're adding random noise and then subtracting or dividng random noise out... you just have to be careful about this because of the exponentiation to the d value. e is used because it stands for encryption and decryption because they are inverses of each other. If you were using RSA to do encryption, then the e would be the value you raised to to encrypt, and d would be the value you raised to for decryption.

Does anyone have any questions on all that? I'm going to move on to another scheme which uses blind RSA.

# Blind decryption

Say that Bob has a public key and secret key pair (PK, SK). Bob is going to encrypt two files using k1, k2 using AES encryption. The encryption of these files will be ciphertext 1 (ct1) and ciphertext 2 (ct2). Bob then uses his public key to encrypt the keys. z1 = RSA(PK, k1) and z2 = RSA(PK, k2) and publishes z1, z2, ct1, ct2. Alice sees these values. Alice then wants to get z2, she wants to get Bob to decrypt z2 without Bob knowing.... Alice blinds z2 and bz2 and sends it to Bob. Bob uses SK to blindly decrypt bz2... Alice unblinds bk2 and uses it to decryupt the file f2 using the unblinding function and the decryption function. Bob doesn't learn which of the files that Alice actually got the decryption on.

This example is only for 2 files, but you could have many files. You could have a third-party where Bob encrypts files under a third-party's public key, and then Alice requests decryptions. This is a fairly valuable thing to do, like in the tumblebit protocol where a party can get decryptions on things without revealing what it is actually getting decryption on.

# Conclusion

We talked about anonymous ecash, blind signatures, building blind signatures using RSA, and blind decryption. ZeroLink uses blind signatures for coinjoin.

https://github.com/nopara73/ZeroLink





