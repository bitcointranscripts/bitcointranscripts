---
title: Blind Signatures in Scriptless Scripts
transcript_by: Bryan Bishop
tags:
  - adaptor-signatures
speakers:
  - Jonas Nick
date: 2018-07-03
media: https://www.youtube.com/watch?v=_1dcU70zhqs
---
<https://twitter.com/kanzure/status/1014197255593603072>

My name is Jonas. I work at Blockstream as an engineer. I am going to talk about some primitives about blind signatures, scriptless scripts, and blind coin swap, and I will explain how to trustlessly exchange ecash tokens using bitcoin.

I want to introduce the blind Schnorr signature in a few moments.

## Schnorr signature

My assumption is not that you will completely understand <a href="http://diyhpl.us/wiki/transcripts/blockchain-protocol-analysis-security-engineering/2018/schnorr-signatures-for-bitcoin-challenges-opportunities/">Schnorr signatures</a>, but maybe you will at least agree that if you can understand Schnorr signatures then the step to blind Schnorr signatures is not a big step.

So we have some group with G is generator of a discrete log hard group. In bitcoin, we use points on the curve secp256k1.

A signature scheme has three algorithms- the key generation algorithm which creates a new private key at random and computes a public key by multiplying the private key times the generator of the group (G) and then it returns this keypair consisting of the private key and the public key.

Then there's a signing algorithm which generates a new private nonce at random (k), a public nonce (R) which is just k*G, and then it computes s, which is k+ hash(R,P,m)*X where the challenge is the hash of the public nonce, the public key, and the message. The signature is the public nonce R, and s.

Verification algorithm is simple- you just check if S*G is equal to R + hash(R, P, m)*P.

If you don't know the discrete logarithm of the public key, in this case x, then you are not able to create a signature such that this verification algorithm would return true.

## Blind signatures

The blind signer does not know the message being signed. The message is blinded. After signing the message and producing a blind signature, this blind signature is unblinded such that it is unlinkable from the actual signature. Both blind signature and signature are unrelated.

This system is usually explained as a two-party protocol between a client and a server where the client knows a message and the server does not, client creates blind challenge, server signs blind challenge and gives to client, then the client unblinds the signature.

## Blind Schnorr signatures

The creation of the nonce and the signing are two different algorithms here

This requires server\_nonce change, and gives this nonce to the client, and the client creates a challenge from that. It creates the challenge by getting two random values, alpha and beta. Then it computes a new nonce from the old one, called R'. Then it creates the challenge which is just the hash of the new nonce, public key, and the message. It then blinds the challenge by adding some random numbers added to this challenge to blind it, basically.

Signing, from the point of view of the signer, is almost identical to before except now the server doesn't have control over what it was signing. Previously the message would be hashed, but now it just has this challenge c value and it computes s and returns the value. The client unblinds this s value by adding alpha, and verification is the same as before. This is very important-- in every system where you have Schnorr verification, you can always use some sort of blind Schnorr signatures.

## Ecash

Something often built with blind signatures is e-cash, which usually has a trusted server with a database to prevent double spending. The server database consists of serial numbers that have already been spent. The token is a tuple of serial number and server signature of the serial number.

There needs to be a reissuance protocol or refresh protocol where someone who has a token can exchange it at a server for a fresh unlinkable token. The client chooses a new random serial number, creates a blind chalenge for that, and client shows token and blind challenge to the server, the server checks the signature, and the server also checks whether the token serial number is in the database, and the server inserts the serial number in the database to validate that it's spent. The client unblinds the signature to get fresh token.

This unlinkable property holds. The server at this point has only seen the old token and it has signed some new token, but since it's a blind signature, it doesn't actually know what the client now has.

This reissuance protocol is also used for payments. Alice gives Bob a full token as a payment, and Bob tries to do a reissuance protocol with the server and then Bob is able to know whether the token is valid.

## Exchange discrete log for bitcoin

We would like to get to a protocol where you can buy a blind signature using bitcoin without having to trust anyone. The buyer will definitely get the blind signature, and the sellers will definitely get the bitcoin. There's no way to cheat.

We need to define a protocol for how to exchange a discrete log for bitcoin. Let's say the buyer wants to buy the discrete log of some point, like T = t*G. This is the basic scriptless script technique.

The buyer first creates a multisig output with a seller. It would be a 2-of-2 multisig. The seller sends a transaction that sends the coins from the multisig output to the buyer. And an adaptor signature- I don't want to go into this right now, but you can look that up later. Next, the buyer gives seller her signature over the transaction. The seller can now spend the output using the transaction already signed by the buyer. The buyer then learns the signature from the seller's tx signature and adaptor signature and can therefore learn the discrete logarithm.

On the blockchain, this looks like a single boring transaction and can't see any of this stuff happening off-chain.

## Buying discrete logs on bitcoin with lightning network payments

Doing this on chain is nice, but what if you could buy discrete logs with lightning network payments instead? This is currently not supported in the lightning spec. But maybe with multi-hop locks in place of HTLCs, it might become possible to buy discrete logs in the lightning network. This was discussed on lightning network mailing list under the name "scriptless scripts with lightning". A research group proved this construction is secure, they used the name multi-hop locks.

In HTLCs, each hash is some hash of a preimage, each hop has that hash of a preimage, and the seller claims with preimage p. And that's how payment works in HTLC chains.

Multi-hop locks use curve points instead of hashes. The buyer sets up a route, and the locks aren't HTLCs they are points. So say the buyer wants to buy a discrete log of some point T = t * G. The buyer can control how these points look like. So you can add randomly generated numbers by the buyer...  ...  ((other stuff)) And that's basically it.

## Exchange blind signatures for bitcoin

You need comimtted R-point signatures. This has been used in discreet log contracts. The seller creates a public nonce R, and then the buyer can compute the seller's signature s*G. The buyer cannot compute the seller's signature because otherwise the signature scheme would be broken, but you can compute s*G which is R + the hash challenge and so on.

Committed R-point signatures work for blind signatures too. The client can compute the server's blind signature s * G. And then they buy the discrete log of s*G with bitcoin using on-chain or off-chain techniques.

## Blind coinswaps

Now that we are able to buy blind signatures for bitcoin, we can look into blind coinswap.

Coinswap is an old privacy technique where Alice and Bob can atomically and trustlessly exchange coins in order to break the history of those coins and make blockchain analysis harder.

There's some kind of server that does coinswaps all the time and this server cannot link with whom these coins were swapped. It's very similar to tumblebit in that sense, but it's only based on scriptless scripts. The blockchain footprint is quite minimal, you only see a payment, if you use on-chain transactions to buy the discrete log. It's only based on discrete logs, it does not use RSA.

The client buys a blind signature from the server and the message is only a transaction that gives server coins to the client. How does this work?

Assume the server has a bunch of coins, here represented by this box with a server label. The client creates an unsigned transaction spending these coins from the server. It needs the signature from the server to spend this, of course. It creates a blind challenge from this unsigned transaction, and a blind signature using these committed R points... and then it pays for its discrete log (the actual blind signature), and then it unblinds and broadcasts the transaction. So the point here is that the payment of the client to the server, and this transaction that sends coins to the client, is completely unlinkable because it was only ever seen by the server- blinded as part of this blind signature.

## Exchanging ecash tokens for bitcoin

So far we have only bought blind signatures from a server. What you actually want is clients that have some kind of ecash token and can exchange that without having to trust each other.

The central issue here is that the server somehow needs to make sure that the buyer gets the token and the seller only gets the bitcoin once, can't sell it twice or something like that. The easiest way to do this is to make the payment be a 2-of-3 multisig or something like that, where the buyer, seller and the server... but the obvious problem is that the server would be able to see who was actually involved in this payment and would also be able to link a payment to a token. So we don't want that.

Another idea would be to have the server part of a lightning payment route, and the server would be the lost hop, and it would atomically decide whether the payment goes through or not. But I have another proposal.

You can have some kind of token with a locktime and you can only spend it after the locktime expires. So let's introduce ecash with more encoded attributes. Essentially they are Pedersen multicommitments of the attributes. So now you have multiple generators not just G, you have multiple Gs, and you have some attributes, and you have some blinding... Because of this simple structure, it's also possible to prove attributes of tokens in zero knowledge, such as algebraic equations as to which attributes are related to each other or whatever.

## Brands credentials

<http://www.credentica.com/overview.pdf>

Just like before, there's a serial number and a server signature, but also there's an amount and a type which is new. The reissuance protocol is similar- the first two steps are the same, where the client chooses a new random serial number and blind challenge, and the client then shows token and blind challenge ot the server. But now the client needs to prove that the tyype and amount in the token and in the challenge is the same. Otherwise the client could create a token with different amounts or attributes. The server needs to make sure.

How can we have a buyer and a seller trustlessly doing this fair exchange of bitcoin and ecash tokens? There's now two versions of the reissuance protocol- one is where you just get a fresh token, but the other one is where someone receives two tokens with the same serial number. One of them is the buyer token similar to before but it also encodes a buyer secret only known to the buyer, and a seller secret at the beginning only known to the seller, and it's only reissued by the server when you prove knowledge of the buyer secret and seller token. And there's also a seller token, which is reissued only when the locktime is over.

The seller gives buyer token to the buyer but without a seller secret because the buyer is going to buy the seller secret. He proves the locktime of seller token is sufficiently far in the future such taht the buyer has time to buy this token. The buyer buys SELLERSECRETS, which are just discrete logarithms of some points, it's possible to use some on-chain or off-chain payments to buy this discrete logarithm.. the seller secret.. now either the buyer can run the reissuance protocol with the server because it already knows the buyer secret, or the buyer becomes unresponsive and the seller runs the reissuance protocol with the server after some locktime.

## Conclusions

Blind signatures are useful in bitcoin protocol designs, including blind coinswap.

There are ways to build trustless off-chain or on-chain ecash token exchange protocols using scriptless scripts. There is no blockchain footprint at all. That's CryptoKitties.

The next steps are that we want a Schnorr soft-fork. I think the committed R stuff is possible with ECDSA but it would be better to get Schnorr which has some other nice properties we would like to have.

There will probably be a Schnorr signature in the next few months. Implement it, advocate for it, review it, etc.

We see that Lightning is great but we also want scriptless scripts in lightning so that we can buy discrete logs and also blind signatures and so on.

<https://nickler.ninja/slides/2018-bob.pdf>

<https://github.com/jonasnick/scriptless-scripts/blob/46eb506dbfa51295853bc285ce667eeb47fe35b9/md/partially-blind-swap.md>

## Q&A

Q: Why do you use blinded Schnorr signatures compared to the traditional way of blinding?

A: A blind Schnorr signature and a regular Schnorr signature is going to look the same. If you unblind the signature, it becomes a valid bitcoin transaction- you can't do that with RSA because there's no RSA signature scheme in bitcoin.

Q: Implementation satus?

A: We need a good Schnorr signature proposal. Then we need to implement brands credentials in libsecp256k1.

Q: What about BLS signatures?

A: You can aggregate transactions non-interactively. With BLS signatures, you could do non-interactive coinjoin. Unfortunately it requires new cryptographic assumptions, and also they are quite a bit slower actually.

Q: Does the discrete log solution get revealed on the blockchain?

A: The signature on the blockchain is enough for the buyer to compute the discrete log. And this signature is indistungishable from any other signature. Only the buyer learns the answer from the seller.

