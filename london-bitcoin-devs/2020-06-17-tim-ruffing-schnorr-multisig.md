---
title: Taproot and Schnorr Multisignatures
transcript_by: Michael Folkson
tags:
  - schnorr-signatures
  - musig
date: 2020-06-17
speakers:
  - Tim Ruffing
media: https://www.youtube.com/watch?v=8Op0Glp9Eoo
---
Slides: https://slides.com/real-or-random/taproot-and-schnorr-multisig

Transcript of the previous day’s Socratic Seminar on BIP-Schnorr: https://diyhpl.us/wiki/transcripts/london-bitcoin-devs/2020-06-16-socratic-seminar-bip-schnorr/

## Intro (Michael Folkson)

We are now live. This is London Bitcoin Devs with Tim Ruffing. We had the [Socratic Seminar](https://diyhpl.us/wiki/transcripts/london-bitcoin-devs/2020-06-16-socratic-seminar-bip-schnorr/) yesterday, I think we have some people on the call that were at the Socratic Seminar. That was brilliant. Thanks to Tim, Pieter, Greg, waxwing and everyone for showing up and taking 2 and a half hours out of their day. That was great, we’ll get a transcript for that up. The video is up on [YouTube](https://www.youtube.com/watch?v=uE3lLsf38O4). Today Tim is going to present on Schnorr multisig and threshold schemes and then we will do a Q&A afterwards on that topic and also his thesis. For those who don’t know Tim, Tim Ruffing is a Cryptographic Engineer at Blockstream, contributor to libsecp256k1, BIP Schnorr, Bitcoin Core and author for the thesis “Cryptography for Bitcoin and Friends.” I’ll pass over to Tim, thanks for being here Tim.

## Intro (Tim Ruffing)

Thanks for having me. I enjoyed the seminar yesterday. Yesterday the things we didn’t really cover were mostly multisignatures. I will give a quick overview of Taproot from my point of view as a cryptography person. Then I will talk about different issues in constructing multisignature schemes. Feel free to interrupt me if you have a question.

## UTXOs in Bitcoin

From a very simple point of view what are UTXOs in Bitcoin? A UTXO is a spending condition that says “If you fulfill this condition then you are allowed to spend the funds.” Those are encoded in a small program called a script. In almost all cases, the boring case, you need to provide a signature for the transaction you want to make. You need to provide a signature under a given public key that is hardcoded in that script. The scripts look like this:

`OP_DUP OP_HASH160 <Public KeyHash> OP_EQUAL OP_CHECKSIG`

This might be an old version, just to give you an idea. You don’t need to understand what this does. The public key is inside this hash. The script says “Give me a signature under this public key” and then you are allowed to spend the funds. That is how we can define ownership of coins in Bitcoin. If I send it to your public key then these are your coins because you can spend them with your secret key. Currently we have a public key inside the script. In Taproot, if you want to describe Taproot in one sentence it is a script inside a public key. It is the other way round. How can we do this?

## Elliptic Curve Public Keys can serve as Commitments

The idea here is that elliptic curve public keys can serve as cryptographic commitments .They can commit to messages. If you look at how a public key looks, a public key is something like:

`pk = g^(x + H(g^x, data)`

where g is the generator of the secp curve in our case. Sorry for using multiplicative notation if you are not familiar with that. I had to decide on one and I prefer that one. What we can do with this g^x, we can add this tweak here. We can tweak x with plus H(g^x, data). To an outside observer this still looks like an ordinary public key because it doesn’t see that structure here. Correspondingly we can tweak the secret key which is just the exponent here in the same manner.

`sk = x + H(g^x, data)`

The secret key is tweaked with this hash function. Now we have a public key with a tweak and the secret key with the same tweak. Data can be anything we want to commit to.

## Taproot

`pk = g^(x+H(g^x, script))`

In Taproot the data we commit too is essentially the script. If we have such a public key in a UTXO on the chain what we can do is spend it in two ways. The first one is key-path spending. This is an ordinary thing. You can produce a Schnorr signature which is valid under that public key pk. I will talk about Schnorr signatures later. What I have said so far is not specific to Schnorr signatures. The keys in ECDSA would look the same. We could do the same trick with ECDSA but it is not that cool for applications. I will get onto that later. Just accept for now we will do this with Schnorr signatures. Key-path spending is one way. We can produce a Schnorr signature that is valid under this public key. The cool thing about this is if we do this left part we never reveal that script. Nobody will ever notice that there is a script inside at all. With script-path spending we reveal the script and we reveal `g^x` and we fulfill the original script. The script, like in Bitcoin today, can be arbitrary spending conditions encoded in a program. In Taproot it is not only single script, it is a Merkle tree of scripts, but for what I am discussing it doesn’t really matter much. Usually key-path spending is what we would do traditionally if a single party is involved. Even if there is no script at all, this is just an ordinary UTXO, you don’t need the script here and ownership is defined by knowledge of x. Script-path spending becomes interesting if we have what people call a smart contract which I define as some UTXO where multiple people are involved in the ownership. For example a 2-of-2 multisig in Lightning where you need several parties to agree on an outcome.

## Smart Contracts

Let’s talk more about this. Let’s say we have two parties and they both have a secret key. The first party has a secret key x_1 and the second party has a secret key x_2. This means they have a combined secret key of x_1 + x_2. This is not perfectly correct but I will explain that part later. For now accept that we just take a sum here. The secret key will be the sum of x_1 and x_2. Now we tweak it again with this script.

`sk = x_1 + x_2 + H(g^(x_1 + x_2), script)`

Now we have two cases. If those two parties are cooperative and agree what they want to do with this UTXO then they can produce a single Schnorr signature that is valid under this combined key. This will be a multisignature. This is the simple case. In this case they will not reveal what the script here is. To an outsider it won’t even be clear this is a multisig. This looks like an ordinary spend. The only case where the script is relevant is if the people don’t agree or don’t cooperate. Let’s take the Lightning example. Usually you assume that the other party is online and cooperative. But if it is not then there is the timeout and after this timeout you are able to spend the funds on your own without the cooperation of the other party. This would be a condition that is encoded in this script here. As long as the parties in this smart contract, it can be more than two, as long as they all agree we won’t need to reveal the script which is great for privacy. People won’t even notice that there is a multisig or smart contract going on.

## Taproot is Cool

Let me summarize those advantages. This means that all Taproot UTXOs will look the same. There is a single public key in a sense plus an amount of course but the amount is not relevant in our discussion here. The UTXO itself is not a script anymore. It is just a single public key. This is great because public keys are short, they are just 32 bytes. Also as I said before most spends look the same. Usually if you take the key-path spend then the spend of a UTXO is just a single signature. This is also nice because Schnorr signatures are short, they are 64 bytes. The only exception is if we have parties in the smart contract that don’t agree. This is the only case where we need the script-path spend and need to put more data on the chain plus need to reveal what is actually going on.

## Applications

This is great for applications because our idea here is that at the consensus layer we can just put simple Schnorr signature verification. The consensus layer doesn’t care about advanced Schnorr signature protocols. But we can build those on top without changing the consensus code. We can build multisignatures on top, we hopefully can build threshold signatures on top, we can build Blind Schnorr signatures on top as long as the output of all those things looks like an ordinary Schnorr signature. It is understandable by the consensus rules and the consensus rules just do simple Schnorr signature verification. This is great because the contracts are hidden from verifiers. It is a single public key and a single signature and you don’t see what contract is going on. Additionally the consensus layer is kept simple. It is just Schnorr signature verification and the consensus layer doesn’t need to care about multisignatures, threshold signatures. It doesn’t even know what a threshold signature is. It just understands Schnorr signature verification.

Q - That bottom layer currently supports all of the above options in terms of multisignatures, threshold signatures, blind signatures. There is no scheme out there that would need changes to that Schnorr signature verification that you are aware of? They can all work with Schnorr as it is currently implemented?

A - I will come back to that part later. Multisignatures I think are basically solved. We need more work for threshold signatures and we need more work for blind signatures. I believe all of this can be done but we are not quite there yet. I will talk about multisignatures and threshold signatures in the rest of the talk. I won’t cover blind signatures but for blind signatures the situation is that more work needs to be done but we are confident that we can develop schemes that have blind signatures that look like Schnorr signatures.

## Taproot BIPs

As a summary there are currently three Bitcoin Improvement Proposals that cover Schnorr signatures and Taproot. The numbers are here ([BIP 340](https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki), [BIP 341](https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki), [BIP 342](https://github.com/bitcoin/bips/blob/master/bip-0342.mediawiki)). Taproot was so large that we split it into two. There is a lot of stuff going on.

## Research Agenda

Inspired by this idea or vision here when people ask me what I am doing at Blockstream or what my research agenda is I work on everything as long as it looks like a Schnorr signature. Then it is compatible with Taproot. I am really interested in multisignatures, threshold signatures, blind signatures or even things that aren’t signatures. As long as in the end they output something like a Schnorr signature we can put it on the blockchain and play with it. The rest of the talk, I will be mostly talk about multisignatures and a little bit about threshold signatures.

## Schnorr Signatures

Let’s look at Schnorr signatures first. Secret keys are integers, scalars and exponents.

`sk = x`

`pk = g^x`

So far this is just like ECDSA. We don’t change anything about keys except for encoding. The underlying math is the same when you look at the keys. The signing algorithm takes the secret key, the public key and a message.

`Sign(sk = x, pk = g^x, m)`

It draws a random value r called the nonce. I will discuss later how we should implement this in practice. It computes a public part of the nonce which is R.

`R = g^r`

It computes what we call a signature hash, challenge hash c which is the hash of the public key, R and m.

`c = H(pk, R, m)`

For people familiar with the details of the cryptography this is Fiat-Shamir style. Then it computes a value s which is what we call a partial signature.

`s = xc + r`

Intuitively you see what the point of this r value is because we later output R and s. Everybody can compute c. If we didn’t have this r value then people would know s and they would know c. They could immediately compute x. This gives a hint why this r value is so crucial in signatures.

The verification algorithm takes a public key X which is g^x but the Verifier doesn’t know x. It takes a signature which is (R,s) and it takes m.

`Verify( pk = X, (R,s), m)`

It can compute the same hash here because it has pk, R and m.

`c = H(pk, R, m)`

Then it can check this equation on the left hand side (s = xc + r). But because it doesn’t have x, it needs to check it in the exponent. This look like this now.

`g^s == X^c R`

X^c is the same as g^(xc). Multiplied by R which is g^r. This is the public version of the equation. This is why verification can be done publicly. This is what we want from a signature scheme. You check if this equation holds and if it does the signature is valid. I won’t explain why this is secure. The idea of this slide is to give you reminder of what Schnorr signatures look like and we can work from here towards our multisignature scheme.

## Deterministic Randomness

First let me talk about this random here. We covered this yesterday a little bit in the Socratic Seminar. How should we compute this random value? On the previous slide I used the dollar sign \$ the symbol people use for random. Maybe we should replace it with the Bitcoin sign and not use the dollar sign. What we do in practice is we derive this randomness deterministically which first sounds like a paradox. Is it randomness if it is deterministic? It is not really randomness if it is deterministic but it is still unpredictable to adversaries and this is what matters. How we derive this value is we take another hash function H_non, non for nonce. H are all variants of SHA256. When I wrote these slides I am looking at it from a theoretical point of view and any good hash function will do. I just write H it is simpler. We have H_non here. We have some public inputs, the public key, the message but we also have the secret key as an input. This is why it is unpredictable to attackers. The attacker doesn’t know the secret key x and so can’t compute this value here.

`r = H_non(x, pk, m, rand)`

`R = g^r`

We also mentioned this yesterday. If you just put x, pk and m here then it would be really deterministic. But because we are super careful we also add some additional real randomness in this hash function. If this rand argument here is not really random then we still have the deterministic thing and the attacker can’t predict it. If this is real randomness it is additionally randomized so it is even better to protect against side channel attacks. If you are interested in side channel protection read the BIP. This is the only thing I changed in the algorithm here. Why is this important? The problem is that if you don’t use this trick of deriving randomness deterministically what can happen in practice, and this has happened too often now, is if you use a random number generator maybe from your operating system those tend to fail in weird ways. The code path that should handle the failures is often not well tested. It doesn’t give you an error message, it just gives you zeros back, it gives you repeatable values back, the entropy is not enough. There are so many things that can go wrong here. To give you one example the worst case that can happen is that you use the same randomness twice. You use the same r twice. Now if you have different messages and sign different messages with the same r value then the c value will change because you put a different message in the hash function.

`c = H(pk, R, m)`

In one case we have s = cx + r and s’ = c’x + r. Now you reveal those two values to the world. What happens is you can subtract these two equations and you get this here.

`s - s’ = x(c - c’)`

`x = (s - s’)/(c - c’)`

This lets everybody compute your secret key because they know s, this is what you revealed as part of the signature and they know c because they compute it from public values. This is the worst case that can happen. If you reuse the same randomness for different messages everybody can compute your public key. To give you an idea why this hash function helps if you use the hash function to derive the randomness. The reason is that if you use different messages here, the m is an input to the hash function H_non, those will result in different r values. Assuming we have different m we will have different r and the revealing of x above can never happen. This is how you should implement Schnorr signatures in general. The same holds for ECDSA and similar signatures. If you look at the BIP we do it in exactly this way.

## Naive Multisignatures (Insecure!)

This is what Schnorr signatures look like. Let’s see how we can expand the idea to multisignatures. This is the naive way and it is insecure. It should be obvious from the slide.

`x = x_1 + x_2 + … + x_n`

`r = r_1 + r_2 + … + r_n`

It goes in the right direction, it gives you the right idea and we start from here. The idea is that the secret key x is now split among multiple parties. They all have a share of it. The first party has x_1, the second party has x_2 and so on up to x_n. If we add them together we get x. This is how we set up the secret keys. For the secret nonces we do the same. If you look at the corresponding public values you can say that the public key of the first party is X_1 which is g^x_1. The public nonce of the first guy is R_1 which is g^r_1 and so on. I don’t have it on the slides here but this gives us a way to compute an aggregated public key. Multiplying all those public keys into a single public key X.

What would a signing algorithm look like? On the left hand side this is the ordinary Schnorr signing algorithm. I put it here as a reference. On the right hand side I give you the naive multisignature algorithm that is broken. Let me stress again it is broken. The idea is that everybody now computes this nonce r_i if you are participant i.

`R_i = g^(r_i)`

Now all the parties broadcast their values R_i. As soon as everybody as received all the Rs we can combine them into a single R.

`R = R_1 x R_2 x R_3…..`

If we have this final R we can compute c as before.

`c = H(pk, R, m)`

Then everybody can compute his partial signature which is s_i.

`s_i = (x_i)c + r_i`

We can sum up all the s_i and give the signature back (R,s). Because everything is nice and linear it will work out. This will give a valid signature in the end. If you look at:

`s = xc + r`

It is the sum of all r_i which gives r and the sum of all x_i which gives x. We implement this by summing all the s_i to get s. Everything is nicely linear so we can just add up everything and get the final signature. This works. The problem is not that it doesn’t work, the problem is that it is not secure. Why is this not secure? There are two issues.

## Issue 1: Rogue Key Attack

The first issue is, we mentioned this yesterday, the rogue key attack. Let’s say we have three parties. The first two are honest. They compute their public keys pk_1 = g^(x_1) and pk_2 = g^(x_2) and then there is a third malicious party. The malicious party, the attacker, selects the public key pk_3 dependent on the other public keys.

`pk_3 = g^(x_3)/(pk_1 x pk_2)`

x_3 is known by the attacker. Yesterday you called this the key subtraction attack. I switched to multiplicative notation so it is key division attack now. It is exactly the same thing. Now if you combine this into a combined public key, we take the product of this and we see that x_1 cancels out, x_2 cancels out and what we get in the end is g^(x_3).

`pk = pk_1 x pk_2 x pk_3…. = g^(x_1 + x_2 + (x_3 - x_1 - x_2)) = g^(x_3)`

This is very bad because this is the final public key. x_3 is known to the attacker so the attacker can now sign alone without Party 1 and Party 2. This is exactly not what we want in a multisignature scheme. The entire goal is that they all should agree on the message and no single party can sign for everybody.

Q - The key subtraction attack is the same as the key cancellation attack which is the same as the rogue key attack? There are three names for exactly the same thing, the same kind of notion.

A - If you are strict about terms here, what we looked at here specifically is a key cancellation attack and depending on how you write it it is key subtraction or division. In the end what matters is that the key cancels out. The term “rogue key attack” if you look into the academic literature the term “rogue key attack” applies to every attack where you choose your key in a malicious way. The honest way would be to do as the first parties do. Take a fresh x exponent and compute g^x. This is obviously not what the third party here does.

Pieter Wuille: I think the term “key cancellation” is one that we came up with when we discovered a problem with naive multisignatures before we knew of the academic term “rogue key attack” which is the more generic term for problems with untrusted keys.

That is a good point. It is sometimes a little bit confusing. In particular in cryptocurrencies where there is so much work from academia plus practitioners. They both invent their own language sometimes and then they have problems talking to each other when they are talking about the same thing. This is just about terms, it is a detail here.

Q - There are two separate concerns here. There is one where you are trying to convince all the participants in the scheme that it is a multisig but actually you are just using one key. Then there is also one where you can ensure one of the parties doesn’t get to participate in that multisig? Or are they exactly equivalent? Pushing one party out versus pushing everybody out apart from yourself?

A - I think you can implement this attack in every way. You can push out an arbitrary set of signers. Of course if you are the attacker you go for the best thing which is push out everybody else. But you could also do it in a manner where you just push out a single party.

Q - If you are able to push out one party does it then iterate so that you can effectively push out everybody if you can push out one? Or are there certain scenarios where you can only push out one party?

A - You can arbitrarily choose as the attacker.

Q - How many parties you push out?

A - Right. If you are malicious there is no point in pushing out only one. Maybe if you are two malicious guys and you have a deal.

Q - Unless there is accountability but I think you will go onto accountability later. That brings another dimension in.

## Avoiding Rogue-Key Attacks

That is the attack. How do we get around this? Avoiding rogue key attacks. There are two approaches to avoid those attacks. One is called [proofs of possession](https://eprint.iacr.org/2018/483.pdf) (“pop”). This is what people have done very early when they discovered these attacks in the 1980s or 1990s. At least two decades old. The generic way to prevent this is to add proofs of possession to your public keys. What does this mean? You could also say a proof of knowledge. It is proof of knowledge of your secret key. You have your public key and what you add to it is a zero knowledge proof that you know the corresponding secret key. Because Schnorr signatures are zero knowledge proofs of knowledge you can sign your public key with your secret key. That sounds weird but it does the job. Why does it work? Let’s go back. In this example:

`pk_3 = g^(x_3)/(pk_1 x pk_2)`

The attacker wouldn’t succeed if he needs to provide a proof of possession because for his public key pk_3 he doesn’t know the secret key. He only knows the x_3 part.

`pk = pk_1 x pk_2 x pk_3…. = g^(x_1 + x_2 + (x_3 - x_1 - x_2)) = g^(x_3)`

It is actually `x_3 - x_1 - x_2` and he doesn’t know x_1 and x_2. He wouldn’t be able to produce a zero knowledge proof that he knows this sum in the brackets here. You can prove that this prevents the attacks. It is not the nicest or the most practical way.

The better way, or what we believe is the better way is what [MuSig](https://eprint.iacr.org/2018/068.pdf) does. What we do there is we use a public key aggregation function with tweaks. How does this work?

## MuSig Key Aggregation

The slide is wrong here. Forget about this middle part here. Instead of multiplying the public keys we additionally add a coefficient here for every party. Coefficients a_1, a_2 and a_3.

`pk = g^((a_1)(x_1) + (a_2)(x_2) + (a_3)(x_3))`

The product of pk_i raised to a_i. What are those coefficients? They are computed via a hash function. You can call them tweaks, that is why I said it is tweaked key aggregation.

`a_i = H_agg(i, pk_1, pk_2, pk_3)`

There is another hash function. What do we put inside the hash function? All the public keys and the index of the signer. The index will make sure that this is a different value for all the signer. All the public keys makes sure it depends on all the public keys. We have these additional coefficients here. This is what avoids the rogue key attack. It does it in a nicer way. We don’t need those proofs of possession. You can just work with simple public keys. You don’t need to additionally send proofs of possession around. It is not necessary. It just works out. This is essentially a public function. You have public keys here, they are public and you can compute the a_i, they depend on public values. Everybody can compute the aggregated key given all the public keys. This is how MuSig avoids rogue key attacks. I won’t prove why this works but it is in the paper.

## Issue 2: Parallel Security

The second issue we have to deal with is parallel security. What I mean by that is running multiple signing sessions in parallel. Can we do this? It turns out if you look at a naive scheme again we can’t. Why is that the case? I will show you an attack.

## Wagner’s Algorithm

First I need to talk about Wagner’s algorithm. What is Wagner’s algorithm? I won’t explain how it works but I can explain what it does. Let’s look at this problem here.

`Find m_0, m_1 such that H(m_0) = H(m_1).`

This looks like a hash function collision. You have to find two messages such that the hash function H gives the same value for both messages. For a good hash function this is a hard problem. I think we can all agree on this. Interestingly and this is very unintuitive, if you do this for more than two messages, let’s say 100 messages this is a similar equation.

`Find m_0, m_1,…., m_100 such that H(m_0) = H(m_1) + …. + H(m_100)`

If you look at the above equation you could also write H(m_1) - H(m_0) = 0. You could do the same here. Finding some messages where the hashes sum up to zero. This is written again in another way. Surprisingly this problem is easy. It is easy because Wagner’s algorithm exists. This example with 100 here I think this is 2^40 operations. The larger you make the number of messages here the easier this problem gets. How can we turn this into an attack? I said I want an attack if we run multiple sessions in parallel. If there is a single signer that uses the same secret key for multiple sessions in parallel.

## Attack Using Wagner’s Algorithm

The attack works as follows. We have a public key. This is the combined public key. Again I am looking at the naive thing, the key aggregation is the simple one here. It doesn’t matter for this attack just because it is simpler. Let’s say x is the value that belongs to the victim, the honest party and x’ is the value of the attacker.

`pk = g^(x + x’)`

What the attacker does is open 100 sessions with the victim. 100 signing sessions with those messages m_1,….., m_100. We assume that the victim wants to sign these messages. What the victim will send the nonce, 100 nonces, 1 nonce for each session. Note the indices now denote the sessions not the different parties as before. What the attacker is multiply all those Rs to get this final R.

`R = R_1 x R_2 x …. x R_100`

This is a little bit similar to Wagner’s algorithm. It multiplies R from several sessions and the attacker uses Wagner’s algorithm to find nonces R’_1 to R’_100 to send back to the victim such that the following equation holds.

`H(pk, R, m) = H(pk, R_1 x R’_1, m_1) + …. + H(pk, R_100 x R’_100, m_100)`


This is the same pattern I showed on the previous slide where you have one hash on the left hand side and you have the sum of a lot of hashes on the right hand side. Look at the hashes on the right hand side. They will be the signature hashes in the individual sessions. The first one is the signature hash for the first signing session. Why? Because it is the message of the first session and the combined nonce of the first session. (In the original slides there was a typo but the above equation is correct.) In the first session we multiply the nonce of the honest signer with the nonce of the attacker and this would be the result. We do this for every session. These hashes on the right hand side here are the hashes of the individual sessions. What the attacker can do is influence these hashes because he controls his part of the nonce, these R’. He can play around with these R’ values and using Wagner’s algorithm he can find R’ values for the right hand side such that they match a single target value. This target value R on the left hand side. Why is this useful? Now the attacker sends those nonces that he found and the attacker will obtain partial signatures from the signer because the honest signer completes all the sessions sending partial signatures s_1 to s_100. Interesting if we add up all those s_i here (s = s_1 + … + s_100) then this is a partial signature on this m with nonce R. This works because everything is nicely linear. What the attacker did here is multiply all the nonces which corresponds to summing up all the partial signatures here. With Wagner’s algorithm the target R is exactly that R in that hash. I haven’t written this up but if you do the math you can check that this is a valid partial signature on message m because the hash here matches. Then the only thing the attacker needs to do is complete it with his own partial signature.

`(R, s + x’H(pk, R, m))` is a forgery on m.

s plus the partial signature of the attacker and now he has a final valid signature on m.

Q - A parallel session is when you have a server set up to do the signing. If it is coming to a human and the human sees all these signature requests the human is going to notice something is weird is going on. It is taking advantage of there being an automated server to sign and people not noticing that it is providing lots and lots of signatures.

A - It is not necessarily not noticing. The scenario you are describing is exactly the right one. It may be a service that serves multiple clients, that is one example. There are other examples, let’s say you have the same key on several devices. Here you should think about key management. They can’t talk to each other so they can’t even notice that there are parallel things going on. They all use the same signing key. This is another scenario. It is not necessarily about noticing. Of course you could say “We don’t care about this parallel security and we just set up our service in a way that it only handles one client at a time.” You could do this. It is just not what I would call robust. It can go wrong in multiple ways. Maybe the code doesn’t check if there are multiple things going on. Maybe you are running in a VM and somebody runs multiple copies of you. Or maybe there is a key on a different device. Or you are just not careful enough and you don’t know this attack exists. There are so many things that can go wrong. That is why we want to have a scheme that is robust against this in the first place and eliminates the issue from the beginning.

Q - Which is definitely the right approach to take as a protocol engineer designing it. Perhaps a corporate situation, they could just limit how many signatures are provided or if there is any strange activity flag it.

A - Yes. It is not like this is broken. If you don’t run this in parallel this attack doesn’t apply. It is just hard to ensure in practice that you are doing the right thing. Exactly as you said from the point of view of a protocol designer we want to build a protocol that doesn’t have this issue so people can’t use it in the wrong way. Another problem, if you limit your service to a single signature, maybe you can run into DoS issues because you can only do one signing session at a time. There is a single client and you can’t provide a service to other clients. Depending on the setting you are an easy target for DoS attacks.

Q - Andrew Poelstra said in a SF Bitcoin Devs [presentation](https://diyhpl.us/wiki/transcripts/sf-bitcoin-meetup/2019-02-04-threshold-signatures-and-accountability/)  “There is always a simple fix.” But some of those fixes have downsides. Some of them introduce complexities that perhaps a corporate wouldn’t want. There are going to be trade-offs when there are fixes pushed to address some of these attacks.

A - In general you are right. If you look at the previous issue with the rogue key attack I think the fix is simple enough. It adds a little bit of engineering overhead but it shouldn’t matter to you if you use a nice library that has already implemented it. You only have to do it once and take it off the shelf. It adds a little bit to the runtime but it is acceptable for the increased security. Of course everybody is free to make their choices. I think your comment would apply more to the fix that I am showing now. This is really something that people don’t like in practice. There is a real trade-off.

## Parallel Security

So how do we fix this attack? How do we get parallel security? The problem if you look back at the previous slide is the attacker can influence what is going into the hash function here. He influences the right side of the products (R_1 x R’_1, R_2 x R’_2 etc) here. This is the gist of the problem. If the attacker can’t influence what is going on, he can’t play around with these values then he can’t apply Wagner’s algorithm and make the sum on the right hand side match the left hand side. The problem is the attacker controls the hash value because he controls part of the nonce. For anybody with a little bit of background in provable security what does this mean for the security proof? In the proof this would mean the reduction must know this final R in every session before the attacker knows. This is required for programming the random oracle on H(pk, R, m). This is how you simulate signatures. If the attacker can predict this R value because he controls it then the attacker can make this query before we can program the random oracle. How do we fix this issue now? The fix is that we let every signer send a commitment to this R value upfront. Why does this help? If you look at the attack the victim sends nonces and then the attacker knows those nonces already and can play around with them. In particular he already knows the final target value R here which is the product of all those nonces R_1, R_2,… before he needs to reply with his own nonces R’_1, R’_2,… here. By introducing a commitment we will avoid exactly this.

## MuSig

If you look at the final MuSig algorithm. On the left hand side this is a normal Schnorr signature. On the right hand side, I am lying a little bit here. This is not MuSig. Please don’t implement this. Please don’t implement crypto if you don’t know what you are doing. What I left out for simplicity is the protection against rogue key attacks. It wasn’t important here but I wanted to put a note on this slide and I forgot to. It doesn’t have the a_i coefficients but it protects against the attack we have just seen. Why? In this line we are introducing what I said.

`broadcast h_i = H(R_i)`

`broadcast R_i, R = R_1 x R_2 x ….`

Everybody commits to his nonce upfront. Now the attacker also has to commit to his R_1 value. Only if we receive the commitment from the attacker we will broadcast our own value. This means the attacker can’t choose his R values depending on our R values. At the moment he needs to commit to his R values he doesn’t know our R values. Later we need to check if the commitment of the attacker was correct. If not we abort.

`fail if H(R_i) does not equal h_i for some i`

`c = H(pk, R, m)`

`broadcast s_i = (x_i)c + r_i`

`s = s_1 + s_2 + ….`

`return (R,s)`

This is a very simple fix and fixes the problem entirely. The weird problem with this fix is that it introduces a third round. If you don’t do this round here the MuSig signing protocol is just two rounds. If you introduce this round it is three rounds. This can be annoying in practice. This is a nice example for the trade-offs you mentioned. If you are willing to give up that additional safety you can skip that broadcast round and make sure you never run parallel sessions but I wouldn’t recommend it. It is fragile.

Q - If you already have two rounds that additional third round isn’t a big deal. It would be a much bigger deal if we were going from non-interactivity to interactivity. But once you have got interactivity another round isn’t a big deal?

A - Right. Also what you can’t do in MuSig, for the same reason, Jonas Nick has a nice [blog post](https://medium.com/blockstream/insecure-shortcuts-in-musig-2ad0d38a97da) on insecure shortcuts in MuSig. You should read it, it is cool. It mentions one issue where even if you have this additional round, you are maybe annoyed you have three rounds, can we optimize this? You might have the idea to do this round `broadcast h_i = H(R_i)` upfront before knowing the message. Let’s say in the future you will have a signing session with some parties so you can already prepare now and take a R_i value here, compute H(R_i) and share now. You can do this. Then you save this round or precompute it in a sense. When you know you have the message and you want to sign the transaction at the end you just need to run the additional two rounds. You can do this. The problem is if you do this you might also have the same idea for the second round here. `broadcast R_i, R = R_1 x R_2 x ….` You might also broadcast this already before the message is known. This is a perfectly fine idea because m is only used here. It seems like you can run the protocol up to that point without knowing m. The problem here is that thing is horrible. The problem is exactly the same as before. The attacker can influence the final hash value. If you go back to the attack using Wagner’s algorithm the R values are fixed. The attacker can’t influence this. But now if the message is not fixed yet when you do this step the attacker can influence the message. He controls all the hash values on the right hand side and can do the exact same attack. I can only recommend this Jonas Nick blog post, it is really useful.

## Extensions to MuSig

The last part shows some extensions to MuSig. I won’t go into detail, just one slide per extension. One thing that is basically done and accepted at a conference.

## MuSig-DN

Let me repeat that Schnorr signatures, they need randomness, I have talked about this a lot. I also explained that true randomness can be broken and this leads to bad failures. Use a pseudorandom generator, I called this deterministic randomness. Sorry the wording is not perfect from my previous slides. This is exactly what I showed you with the H_non function where we derived the randomness deterministically from the secret key and the message. We hammered this into the heads of people that they should really do this. This is the right way to do it. The problem is and we also talked this yesterday, if you apply to this to multisignatures it fails catastrophically. It is exactly the other way round. If you do it deterministically it fails. Why is that the case? I can give you an intuition at least by going back to the Deterministic Randomness slide. I explained this attack on the right hand side. If you use the same r, the nonce, for two different messages or two different c then everybody can compute your secret key. Now if we look at the simplified MuSig where the key coefficients are not there, the same attack would apply if you give a partial signature with the same r_i and different c. How can c be different? Let’s say we are two parties, you are the attacker and I am the honest user. I derive my nonce deterministically. We have a session for a message m and I derive my nonce from the secret key and m. I arrive at a r_1 value and I give you this partial signature s_1. You get this and now you start the second round for the same message. Maybe because you claimed the first one failed and you never received the value or whatever. What you do in the second session you send a different partial nonce for you. You send a different R_2. This will result in a different c but because I derive my own nonce deterministically I will use my same nonce, the r value, but now the c is different. Because you didn’t choose your nonce deterministically. This is how we fix this problem. We introduce zero knowledge proofs that prove that everybody chooses the nonce deterministically. Then it is working again. This is exactly what avoids the attack that I just mentioned. You can only use deterministic nonces if you know everybody is using deterministic nonces. The only way to be aware of this is to add zero knowledge proofs to the protocol. When I say they are somewhat expensive, they explain maybe one second to the protocol depending on your hardware and the number of signers. About one second. On the way we get rid of the three rounds. We have two rounds now. But again if you use those zero knowledge proofs it is a real trade-off here. If you care about efficiency it is not clear what is better here. Maybe it is better to run a third round depending on your setting and scenario. The main point of this paper is not to go to two rounds but to avoid the requirement for true randomness. This can fail in practice.

Q - If we compare the randomness requirements, let’s say you and me are both generating independent private keys to hold our funds. We would want as good a source of randomness as we can possibly get and we don’t want any relationship between my private key and your private key. When we are generating nonces are you saying there should be a relationship between those nonces, the definition of deterministic. You don’t want complete randomness, you want a relationship between those nonces as long as you are not reusing them. Is that right?

A - I am not sure if it is a relationship. What all of this wants to avoid is that the attacker chooses his nonce depending on your nonce. This is what you want to avoid. This is maybe a nice intuition why this gets down to two rounds. We needed the third round, this hash commitment, to prevent the attacker from choosing his nonce depending on the honest nonce. With this hash the attacker doesn’t have a choice anymore. At the point when he needs to decommit to the nonce there is only one choice left for the attacker. Now if we have zero knowledge proofs the attacker needs to prove that the nonce was chosen deterministically. Again there is only one choice which is the output of the deterministic function. Again the attacker can’t play around with his nonce and choose it depending on our nonce.

Q - It is more than just nonce reuse. It is an attacker choosing a different nonce based on your nonce. But there is a relationship between those two nonces.

A - One use on your side. You would reuse your own nonce.

Pieter Wuille: The problem is when an attacker can predict what nonce you are going to use while they change their own. You want the property that if any participant changes their nonce everyone’s nonce has to change. The two ways of accomplishing that is everyone picks a random one every time or everyone picks a deterministic one and proves to each other that they picked the only one possible. The first one corresponds to every time all of them are going to change. The second one corresponds to nobody can ever change. These are the two solutions to this problem.

Q - But in a normal signature scheme you don’t want to be reusing nonces. You are not reusing nonces in this MuSig scheme either?

Pieter Wuille: If you are naively using deterministic nonces just like you do with normal Schnorr, you hash the private key and the message. If halfway the protocol the other party goes offline and they restart the protocol they already know what nonce you are going to use. It is deterministic, you will pick the same one but they can change theirs. That is the attack.

I think the issue here is that it is not about reusing nonces, it is about reusing nonces with different messages or different signature hashes in the end. If you think of normal ordinary Schnorr signatures in the single signer case and you sign the same message twice and you derive your randomness deterministically then you also reuse your nonce. It is not a problem because the c value, the signature hash will also be exactly the same. The problem is not reusing itself, it is reusing with a different signature hash value. Now if you have this interactive scheme the attacker can influence the signature hash value by choosing his own nonce. In the single signer case one signer chooses everything, there is nothing where the attacker can influence the signer during the signing process. But in multisignatures you can. You can use this power to change the c value and then force you to reuse your nonce on different c values. This is what creates the problem in the end.

This is one project. It is accepted at the CCS conference this year. It is not public yet, we don’t have a pre-print available but hopefully soon. Hopefully not only the paper but also a blog post that explains it for a different audience. This is joint work with Jonas Nick, Yannick Seurin and Pieter Wuille. Pieter has a nice intuition for the paper and why he is involved.

## Disclaimer

I have two slides left. They are both projects that are work in progress. We are not sure yet if what we are doing is the right thing and if it makes sense. If it doesn’t work out don’t come back to me in a year and complain that it didn’t.

## (Simple) 2-round MuSig

The first thing and I think I have never talked about this in public is that we are working on a simple 2 round MuSig scheme. On the MuSig slide I said we can go back to two rounds but it needs zero knowledge proofs. If your goal is to have a two round scheme I think we have a better idea. The story of MuSig is that the first revision of the paper, this contained a two round scheme with a security proof under an assumption that is not exactly discrete logarithm (DL) but a little stronger. It is called one more discrete logarithm (OMDL). It is related to discrete logarithm. It is still a reasonable assumption one can make. The original two round MuSig scheme was proven secure under this assumption, or we believed it was proven secure until Drijvers, Edalatnejad, Ford, Kiltz, Loss, Neven, Stepanovs found a [bug](https://eprint.iacr.org/2018/417.pdf) in the proof and an attack on the scheme. The attack is interesting because it is an attack based on Wagner’s attack. If you do MuSig naively in two rounds it won’t work. The reason is the attack that is written up in detail in this paper. Then people who wrote the MuSig [paper](https://eprint.iacr.org/2018/068.pdf), Maxwell, Poelstra, Seurin, Wuille had to revert to a three round variant and give another security proof for the three round variant. We are pretty confident it is true. Now this is work in progress but we have a very simple idea that brings us back to two rounds. We are currently writing this up and our plan is to first share with fellow researchers before we release anything stupid to the public. But we are getting more and more confident that this is working. This would be very nice for this area. Hopefully what this will also enable is what I could call nested MuSig where you have multiple nested MuSig sessions. What do I mean by this? I think the canonical example is let’s say we have MuSig in a session for something like a Lightning channel where we need a 2-of-2. I am one of the participants in the Lightning channel and I want to have an additional MuSig with my part of the key where I share my part of the key again between my desktop machine and my hardware wallet maybe. It is basically MuSig inside of MuSig. I have part of the key and this part of the key is split into my desktop machine and the hardware wallet. This should work in a way that is still secure and also in a way that the other party in the Lightning channel doesn’t need to be aware of what I’m doing with my own keys. The other party in the Lightning channel shouldn’t even know that I’m internally running another MuSig session. This is the goal of this nested MuSig. I think this would be helpful in practice in exactly those scenarios and I am sure there are other scenarios. This is joint work with Jonas Nick, Yannick Seurin, Duc Le at the moment. This might change if more people join. We are working on it, we think it works but we are not confident enough to share with the world at the moment. Please be patient.

Q - This is the use case where you are opening a channel with a counterparty and you don’t want that counterparty to know the people who are signing to open the channel on your behalf. MuSig will only have one signature onchain so you are not telling the world that it is a Lightning channel. You are just worried about the privacy with your channel partner.

A - As long as we cooperate with the counterparty an observer that just simply observes the blockchain won’t notice that this was a Lightning channel because of Taproot. What I worry about is the privacy against the counterparty. I don’t want to tell my counterparty how I’m doing key management with my hardware wallet for example. It is a little bit like in Taproot, it is not only for privacy it is also for simplicity. In a technical Lightning specification we probably only want to support 2-of-2 MuSig just for simplicity. You don’t want to explicitly care about the case where one of the parties is a multisig between more keys. You can keep the specification simple and the code of the counterparty doesn’t need to care about what you are doing because it doesn’t know in the first place. It is good for simplicity and it is good for privacy.

## Threshold MuSig

(Tim Ruffing [presented](https://diyhpl.us/wiki/transcripts/cryptoeconomic-systems/2019/threshold-schnorr-signatures/) on “The Quest for Practical Threshold Schnorr Signatures” at CES Summit 2019)

This is my last slide, threshold MuSig. To remind you what that is, multisignatures of n-of-n and threshold signatures are a generalization to t-of-n. A typical case is a payment with an escrow where you have a 2-of-3. Or you share your key among multiple hardware wallets and store them at different locations. If one of them gets stolen or destroyed you still want to be able to spend using your keys. You can lose a few of those hardware wallets. There are a lot of different applications. At Blockstream we are particularly interested in this because Liquid uses a federation that holds Bitcoin. Currently we have a 11-of-15 federation. To make that efficient it would be cool to have a threshold multisignature scheme such that those 15 people can handle the coins more efficiently. The numbers should increase, we won’t be sticking to 15. It should be much larger. When we started to write the Schnorr signature [BIP](https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki), when I say we I don’t mean Blockstream I mean the people on the Schnorr signature BIP of course, we believed that threshold Schnorr signatures were a solved problem. Why? Because there are many papers in the literature that use Shamir’s Secret Sharing and these are all papers that are decades old. They looked pretty solid. Last year we took a closer look at this and discovered a few problems with this. For example the schemes in the literature, they mostly assume that there is an honest majority. If you translate this to real numbers this would basically mean you can’t do 7-of-10 or something like this. You could do something like 3-of-10 but I think there are not a lot of people in the world who are interested in a 3-of-10 signature scheme. Maybe there are. I think cases where t is roughly two thirds of n are usually the interesting cases. Another problem is they assume a broadcast channel. This is a thing that you see often in theoretical papers. They say “We have some channel where everybody can send broadcasts. This is reliable and we don’t care about it.” In a threshold signature scheme it is not even a weird assumption. It depends on the use case you make this assumption for. Let’s say you have this 7-of-10 scheme, let’s assume you can do this. The first problem is we need a broadcast channel. What you want to guarantee is if there are 7 honest people there they can produce a signature. If you want to guarantee this in theory then we need to assume they can talk to each other. If the network is broken they can never get the signature. That is a perfectly fine assumption. Of course if the network is broken we can’t do protocols. This is ok. The problem with these papers is they assume the broadcast channel not only being able to produce a signature but also for unforgeability. If the network is broken the attacker can read your key. This shouldn’t happen. This was very surprising when we saw this. These papers were lying there for decades and nobody really bothered to look at the practical aspects of them because nobody bothered to implement them. Now when we look at them because we have real use cases suddenly those problems become real. Another problem, I mentioned this for MuSig, it is the same problem for threshold signature schemes, parallel security. All these papers don’t care about parallel security. Maybe it works, maybe not but no one has looked into it. This is future work. Threshold MuSig becomes easier with the two round MuSig so this is even more speculative. If you can do the thing on the previous slide then we hope that this becomes easier. This is a lot of speculation now. If you are really interested in threshold sigs watch my talk at CES Summit 2019. There is a [link](https://diyhpl.us/wiki/transcripts/cryptoeconomic-systems/2019/threshold-schnorr-signatures/) here. It talks about the problem of building threshold signature schemes.

Q - By broadcast channel you mean a secure communications channel?

A - I don’t mean secure. It depends on how you define secure. What is assumed in these papers is that it is reliable. What they mean by reliable is what you could describe when you say secure. It is not controlled by an attacker and it works. For example, it needs to have the property that when I broadcast a message to all of my co-signers they not only all receive a value, they all receive the same value. Assume we do the broadcast via a server in the middle and the server is malicious. Then I can send my message to the server and the server can send different messages to all the other people. “Tim sent this value x to the first signer and sent value y to the second signer.”

Pieter Wuille: I am not an expert here. But isn’t it true what is called a broadcast channel is what we call a consensus system? You know everyone receives every message? It is probably slightly weaker.

A - It is certainly very related but I think in a slightly different context. What these papers do is say “We have a broadcast channel” and they don’t talk about relation to consensus or Byzantine agreement, I think this is what you have in mind here. It is true what you say that notions like consensus or Byzantine agreement are very related to what is called terminating reliable broadcast. This is what I describe now. Essentially equivalence. Given a protocol that solves consensus you can solve terminating reliable broadcast. There are two problems with that. First of all there is a huge overhead. In the worst case, if there are malicious people that want to prevent you from finishing the protocol you add a lot of messages. For every broadcast message you want to send you need a lot of rounds to make that one broadcast happen. If you put this terminating reliable broadcast protocol below your threshold signature protocol then the resulting thing is not very efficient. The second problem is because this is related to Byzantine consensus, it only works with a two thirds majority. This is again what we want to avoid with this honest majority assumption. We don’t want to assume that two thirds are online. What we want in the end is a threshold protocol that works without this broadcast channel. It is secure even if you don’t have a broadcast channel.

Q - In a consensus system you will get the message or the transaction whatever assuming there is no eclipse attack or network partition. This wouldn’t be a consensus system because there needs to be a message sent from Party A to Party B. Rather than propagating via other parties to get to Party B?

A - I think this is again a little bit confusing with the terminology. When Pieter said consensus what I hope he meant because it fits my explanation is something like Byzantine agreement. This is a notion from the distributed systems literature. Usually when people talk about this they mean something like a well defined number of parties like a federation, or maybe a permissioned blockchain, with clear membership and not an open system like Bitcoin. When we say consensus we typically use this term for systems like Bitcoin where everybody can join and there is no defined membership. If you look at the distributed systems literature it would say there are 20 servers and they want to agree on a value. This is called Byzantine agreement.

Pieter Wuille: I should’ve used that term, that is what I meant.

Q - Are there any attacks for a man in the middle on that broadcast channel? Can he malleate signatures or something?

Pieter Wuille: The assumption that you have a broadcast channel implies there is no man in the middle.

Q - So it is a secure channel. I suppose it is terminology again, when you use which words.

A - Usually when people say secure channel they think of two endpoints. They say there is no man in the middle and this is what we call a secure channel. Here we are talking about a broadcast channel. It is really subtle.

Pieter Wuille: Something where you have the property that anyone can send out a message, everyone will receive it and everyone will also know that everybody has received that message. That is far stronger than a secure, encrypted, authenticated channel between any two parties which is why we don’t want to have that assumption.

When talking about this assumption in threshold signatures, the gist is you want two properties. You want unforgeability where you say if the attacker controls less than t signers then he isn’t able to produce a signature. If he controls t-1 signers he can’t produce a signature. Then there is another property which you could call robustness which says that if you have t honest signers then you should be able to produce a signature. It is perfectly to assume something like a broadcast channel if you are talking about reliability or robustness as I called it now. If those t signers, they are all honest, they still need a way to talk to each other. If they don’t have a reliable network where they can talk to each other then it is clear that they can’t produce a signature. If the attacker blocks all messages for example they can’t make progress. That is not a surprise. We think in layers and if your only interest is to build a secure threshold signature scheme then you can certainly make that assumption that you have a broadcast channel available to produce signatures. That is a problem we handle at a different layer. What shouldn’t happen is we make this broadcast channel assumption for unforgeability. This is exactly what those protocols do. If you watch my talk I explain that attack. Think of a man in the middle that implements the broadcast, it is a server that connects all the people and does the broadcast for you but the server is malicious. Not even changing messages, just by omitting messages this server can learn the secret key of all the parties. This is really not what you want to have in practice. It was so surprising for us. If you look at the paper it makes this broadcast channel assumption. When I read this my feeling was they need this for reliability, for robustness. If you look at the details, this is very subtle, it turns out they also need it for unforgeability but they are never explicit about this. This sounds like a complaint, it is not, if you use a certain model you can make that assumption. I am just saying this is not enough yet. We need more work to make threshold signatures work.

## Q&A

Q - We tried to set the setting yesterday of what a signature scheme requires. We then talked about what a signature scheme in a system like Bitcoin needs to have. It is like piling on requirements all the time. With a multisig scheme you are piling even more requirements on top of what you need in Bitcoin. There is such a long list of requirements. You didn’t talk about accountability at all. On the schemes that you talked about today or some of the competing multisig schemes there are various levels of accountability. Perhaps you could explain what accountability is and which ones are good for accountability?

A - First we need to clarify what this actually is. I’m not sure if you are referring to what I have in mind. When I hear accountability in terms of multisignatures it only applies to threshold signatures. A simple example, we have a 2-of-3 threshold signature and we know the 3 parties involved. We can’t pinpoint who the two guys were who actually participated in signing this message. I think this is what you mean by accountability. In an accountable scheme we can tell that those were the parties that signed the message. Can we do this? I didn’t talk about this at all. This seems very hard with a scheme that is compatible with Schnorr signatures. At the moment I can’t say much more than this. I don’t think we believe it is impossible. I thought about this what it was a while ago.

Pieter Wuille: Have you ever heard of a scheme called Polysig? It is a Schnorr multisignature scheme where the signature size grows with the number of missing participants and it is accountable. If everyone is present it is just a single signature. For every missing party you reveal some public key of a polynomial evaluation that lets you cancel out some subset.

That sounds reasonable. I think this is a nice example for one point I wanted to make. It is a Schnorr based scheme where the signature size grows with the number of missing parties?

Pieter Wuille: It needs onchain support. It is not a single Schnorr signature.

The final signature is not a single Schnorr signature. There are multiple ways to construct schemes where we change the signature slightly and we get accountability. The problem with all those approaches is if you use them in a Bitcoin context they are usually useless because you need that side information. You can’t force people to give it. In the context of Bitcoin when you talk about signatures, they are signatures on transactions. The use case is then someone stole my coins and I want to figure out who it was. The problem is the only thing you have onchain is the transaction and signature on the transaction. The blockchain validation doesn’t force you to put auxiliary information that would help me figure out who actually signed the transaction.

Pieter Wuille: There is an inherent conflict. You want to design protocols that leak as little information as possible onchain. Then there is this accountability information that inherently adds more which is really only useful for the participants. If you actually want this, a Merkle tree where every leaf is a subset of signers is an obviously actually accountable and relatively efficient scheme. It is not O(1) but it is O(log n) in the number of combinations. The number of combinations is actually exponential.

There are better tricks one can play. It looks like this needs chain support. Now that I think about it I said before we don’t know if it is impossible. If I recall now without chain support, assuming we have Schnorr signatures without additional modifications it seems pretty impossible. Somebody should look into that and try to prove that it is impossible to give motivation to work on other things. Or maybe try to prove it is impossible and not succeed, even better. It looks like you need some auxiliary information in addition to the ordinary Schnorr signature. That is why it seems incompatible with pure Schnorr signatures because as long as you have nothing but Schnorr signatures you can’t force people to give you that auxiliary information.

Q - There is also a deniability property with some of these schemes, I’m not sure which. In which case you can prove that you weren’t the one who was malicious. If you have that and everyone can prove that they are not malicious you can surely narrow it down to who was the malicious party?

A - That is a very good comment, I had forgotten about this. I am not aware of those schemes but it is a very interesting notion. In particular because I just mentioned that the other thing seems very hard to do. If something seems very hard to do it is a good approach to look for something which is not exactly the same but very similar. What you mention is indeed this. It is a little bit weaker because given the signature I can’t tell who were the bad guys that stole my money but I can at least call the good guys and they can prove to me that they weren’t the bad guys. If I reach enough good guys then it is clear the remaining ones are the bad guys. Maybe that is impossible. That sounds much more plausible.

Q - Pieter mentioned Polysignatures. I tried to look them up and I found a transcript but I didn’t find a paper. Could you give a reference? I thought it was very interesting for accountability.

Pieter Wuille: I am afraid there is no reference. It is something some people have talked about. I don’t think there has ever been a good write up. Given that it requires onchain support it is not likely to go very far.

Q - Signature aggregation across soft forks, this would be future soft forks and you wouldn’t be able to aggregate SegWit version outputs across soft forks? What was the problem?

Pieter Wuille: In a scheme where you do cross input aggregation or in general any scheme where you aggregate signatures across multiple CHECKSIG operators or whatever equivalent exists you cannot have soft forks that disagree on what a CHECKSIG operator is. That even means if you introduce an opcode that just returns TRUE that is something that Tapscript ([BIP 342](https://github.com/bitcoin/bips/blob/master/bip-0342.mediawiki)) introduces, there are a bunch of opcodes that are reassigned to define “if you ever encounter this opcode the script is unconditionally valid” which is an amazing extensibility tool because you can give it any semantics later on. This interacts in a really annoying way with cross input aggregation. Once such an opcode is given a meaning and then after that a CHECKSIG operator follows, all nodes will not execute that CHECKSIG but new nodes will. The aggregated signature can only be valid for one of those. This is not a fundamental problem, it is an engineering issue. You must make sure that whenever a soft fork changes what the set of public keys that are supposed to sign is, those need to be aggregated separately. Does this make sense?

Q - I didn’t realize it was a cross input aggregation problem.

Pieter Wuille: It is not necessarily a cross input aggregation issue. Any kind of onchain aggregation where you have multiple public keys onchain but then a single signature for it. The aggregation we are talking about in the context of MuSig is offchain. You compute the aggregated key offchain and on the on the chain you only see the aggregated key and the aggregated signature. Nobody knows anything, that is fine. It would be very useful to have a way of having non-aggregated keys onchain and expect an aggregated signature with them. This is a requirement for cross-input obviously because you can’t pre-aggregate across inputs because they come from separate outputs and the outputs are created separately. This is a model where you have multiple public keys onchain, within one input or across inputs, and only expect a single signature for all of them. The difficulty this introduces is that you must make sure soft forks agree on what the set of those public keys is. Because the aggregated signature will only be valid for one of the two. This is part of the reason why we didn’t push for cross input aggregation together with the Taproot proposal. It is logistically hard to solve this problem. Not theoretically, have a separate aggregate signature for every possible… There are solutions to this but it complicates things.

Q - This is where I am unsure on the difference between key aggregation and signature aggregation.

Pieter Wuille: All of this is key aggregation. The question is whether the aggregated key goes onchain or the non-aggregated keys go onchain. In MuSig you put the aggregated key onchain and then a signature with the aggregated key. In what I am talking about here you would have pre-aggregated keys onchain but then a signature with their aggregate. The consensus rules would do the key aggregation.

Q - The keys are going onchain but only one signature is. In the key aggregation only one key and one signature is.

Pieter Wuille: Both of them are key aggregation. It is just whether the aggregated key goes onchain or the pre-aggregated keys.

Tim Ruffing: Are there scenarios other than cross input aggregation where this would be useful? To aggregate keys onchain?

Pieter Wuille: Any scenario where you would have multiple public keys in a single script. The theory is that in most tractable cases you would turn all those combinations out into a Merkle tree and then have one leaf for every combination and every leaf only has one key. Then that problem doesn’t occur. I am sure there are useful perhaps rare non tractable scenarios where combinations cannot be easily expressed as a Merkle tree. It may be worth it to have multiple keys in one script. Anytime you have multiple keys in one script that are online simultaneously. Obviously you still only have a single signature so you have an interactive protocol to sign. If you want real independence between all the keys then this doesn’t apply.

Tim Ruffing: This is an optimization to the spending then, into the script itself.

Pieter Wuille: If you had a way where if you can’t pre-aggregate keys then put all the keys on the script but you don’t require a separate signature for each. You can still aggregate the signatures together.

Tim Ruffing: Or you could have accountable MuSig onchain with all the public keys onchain. Assuming we have something like threshold MuSig the script simply says “Pick any 7 of those 10 keys but then give me only a single aggregated signature for it.”

Pieter Wuille: Probably with larger numbers because 7 out of 10, you can just turn into a Merkle tree. With the risk of confusing Michael further you don’t actually need a key aggregation scheme for this. You could just use a signature aggregation scheme like Bellare-Neven.

Q - You talked about some multisig and threshold schemes today. There were additional ones we briefly touched upon yesterday. And then there is the possibility of having one particular multisig scheme nested within a different multisig scheme. It is getting very complicated now. Do you see the way this is used and deployed in the real world, that there will be one or two schemes that everybody uses or do you see the trade-offs being so large between the different schemes that people decide to use whatever flavor that works for their use case?

Tim Ruffing: One answer is to this is I could have added an additional slide that says “This is super future, future work. The one scheme fits all approach. A way you have everything combined like threshold, nested.” Think of nested thresholds. So far I have talked about nested multisig but not nested threshold. You can think of nested threshold. If it is within Taproot, this would be one goal of this research, not build different schemes but we want to unify them into a single one. First of all, because it is easier specification wise. You only have one specification and you don’t put the burden of choosing the scheme to the implementer. Also you need only one implementation and only one security proof. But of course it is harder. My gist here is that if this two simple round scheme works out we have this hope that it makes threshold easier. I can imagine that there is something like threshold nested but that is far away. There is a lot of work to do to get all this right especially if you care about proving the security of these things. Functionality wise because of linearity it is generally easy to compose things on the functional side but it is pretty hard to compose things on the security proof side. We end up getting a huge thing that no one can review anymore. I think the only thing where I don’t see some way at the moment to unify this is this CN scheme. This really requires those expensive zero knowledge proofs. If this two round idea works out then I can see a hope for a scheme that does two round, threshold and nesting and a combination of all these. Even if that is far in the future. What I can’t see right now is how to put this deterministic nonce thing together with this.

Pieter Wuille: I think if the two round thing works out, I believe it also avoids the insecure shortcuts problem with precomputed nonces. That is a pretty nice advantage of the two round scheme too. You could precompute your nonces and still be secure. I think there is a big difference in acceptable use cases between things that require interactive setup and non-interactive setup. Anything with thresholds inherently needs an interactive setup unless you mean Merkle tree based thresholds. Ignoring those all efficient threshold schemes require an interactive setup. Perhaps it is worth having a unified scheme of all non-interactive things. It plays well with descriptors and deterministically derived keys and not needing backups. All these things. If the two round thing plus nesting works that is pretty close already I think.

Tim Ruffing: These are two very good points that should be stressed. Let me repeat this. First what I didn’t mention about this two round idea is that if this works out it gives us another optimization. It is not only two round but you can perform the first round, sharing nonces basically, without knowing the message. If you remember I showed this attack where this is not possible. You can do the hash upfront but you can’t do the second round, the nonce round, upfront because this would become insecure if you don’t know the message yet. If this two round idea works out we remove the first round and the round that is now the first round, we could pre-do this. In the end this means that we can share nonces at any point in time. As soon as you have a message to sign it is just one additional round. One round is what people call “non-interactive” in a sense.

Pieter Wuille: It is as non-interactive as CHECKMULTISIG is now. Everybody produces their signature and you put them together.

Tim Ruffing: There is a single leader and everybody computes partial signatures and sends them to this single leader. This single leader combines it and sends it to the blockchain. This is another nice advantage. It is weird I forgot to put it on the slides. Michael pointed out when I said this third round is annoying that it is not that bad. We have two rounds anyway, it is not that bad to add a third one. With this two round idea we could actually go to one round with precomputation. This is a pretty nice thing if it works out. The second point that Pieter made, I didn’t really mention this because I didn’t go deep into threshold signatures. As Pieter said reasonable or efficient threshold schemes require a special key setup based on Shamir’s Secret Sharing. In the multisignature case we can take any existing public keys and aggregate them together and have a multisignature session without any special setup. But we can’t do this in threshold signatures.

Q - Since we talked about key aggregation I want to ask this question. In Lightning Network we have this problem that HTLCs use up a lot of space. The question is if we have PTLCs, whether it might be possible to combine several PTLC outputs to one large output. Of course the timelocks are an issue here. Let’s assume we have the same length timelocks for all of those to simply this. We still have the problem that if we hit the chain we might have the secrets for some of them but we don’t have them for others. Do you see any way other than Merkle trees to resolve this?

Tim Ruffing: I am not sure what you mean by combine them onchain?

Q - Aggregating them to one output.

Tim Ruffing: You mean different channels from entirely different parties?

Q - We have the channel and on regular operation it could happen that I currently have 50 HTLCs with you in flight that come from different routing requests. Assume they are all PTLCs. It would still be 50 outputs. If the commitment transactions hit the chain it uses a lot of space. The question is whether there is a chance we can combine these HTLCs in our channel to a smaller script. I understand the timelock is one issue here but let’s assume there is a safety window for timelocks so in 100 blocks time we can combine all of them.

Tim Ruffing: Even if we want to write down the timelocks explicitly maybe it can still save space. I have no idea. It is an interesting problem but I would have to look at it to have an answer.

Pieter Wuille: What is a PTLC?

Q - A point timelocked contract using adaptor signatures.

Tim Ruffing: I think HTLCs should’ve been called… because they are based on one way functions. If you replace the hash function with discrete log you get a PTLC. This would be an interesting question for Jonas (Nick) because he is into Lightning and also multisigs. He knows a lot of pitfalls.

Q - These multisig and threshold schemes, can they be battle tested on Liquid? How are they going to be battle tested before people are confident enough to use them? There is just the proof and the theoretical phase, there is also getting the code out and getting it into the wild. What are the steps to get it into the wild and have people rely on it?

Tim Ruffing: What you mentioned is one possible way. Battle testing on Liquid. Our hope at Blockstream is that people put real coins on Liquid so maybe you don’t want to battle test with those either. We have testnets, we can write different implementations. It is a large problem but it is a standard problem. For every new technology we need to battle test somewhere. I think I said this yesterday, we are very excited about this stuff because it makes things so much clearer and more efficient and more natural onchain. From what we have seen with SegWit adoption is not immediate and super fast. Even if we have a soft fork today it is not like tomorrow everybody will use multisigs. In particular because they are not so widespread as of today. At the moment you can create multisig and threshold signatures using script. They are transparent in a sense, they are not privacy preserving. People can see you are doing multisigs and threshold sigs but this is still a niche use case. Of course my hope and I guess Pieter agrees with this, is that if we have better schemes that do multisig, they are more efficient and more private, the same is true for threshold sigs, then they will hopefully become more prevalent. For example threshold signatures are the right approach to store your coins safely if you want to store them in multiple locations. You have maybe two hardware wallets and your desktop machine and you do 2-of-3. You can also do this now but it is more expensive, it is obvious to the world. What people also propose, it is not the final answer, you could secret share your key in a 2-of-3 manner using normal Shamir’s Secret Sharing or other methods without using a proper threshold scheme. What this means is still you need 2 of those 3 devices to produce a signature. But it is much more fragile because it means you need to get 2 devices in the same place and they have to precompute the full signing key. If there is something compromised, one of those devices is compromised, where you get the full key in that moment then somebody can steal the full key. This undermines the entire idea of splitting the key onto several devices. Threshold signatures is one of the answers here. If you have better schemes or any scheme there will be more interest in those schemes.

Pieter Wuille: A lot of the work we have been doing is because multisignature, threshold signature schemes, these have been known for decades and academically often treated as a solved problem. A lot of our work is in how we make these things practical. All the issues you might run into with turning it into an actual protocol and the shortcuts people may take. I think it would be an amazing goal to make these things more useful.

Q - Perhaps smaller amounts rather than experimenting with Liquid’s 11-of-15 in an experimental threshold scheme.

Tim Ruffing: There was not so much research on this I think because there were no practical use cases. Now we have them and from a theory point of view those were not interesting to researchers. Most of the cryptography that is around, if it is based on discrete logarithm there is probably always some way to turn it into a threshold scheme. You can have threshold signatures, threshold encryption, I guess there are some other primitives you can build threshold schemes for. Usually if you ask theory researchers, those are not the interesting problems. It is a small additive contribution than to take an existing thing and make a threshold version out of it. It is not creating a new thing it is just adding a small amount of top of it. This is another reason why academia hasn’t really looked into those things.

