---
title: 'Secure Signatures: Harder Than You Think'
transcript_by: Bryan Bishop, Michael Folkson
tags:
  - schnorr-signatures
speakers:
  - Andrew Poelstra
date: 2019-03-09
media: https://www.youtube.com/watch?v=0gc1DSk8wlw
---
Twitter announcement: <https://twitter.com/kanzure/status/1104399812147916800>
## Introduction

Hi everyone. Can you hear me alright? Is my mic? Okay, cool. I was scheduled to talk about the history of Schnorr signatures in Bitcoin. I wanted to do that but then I realized I’ve only got 20-30 minutes to talk here. Instead I am going to focus on one particular piece of that history, which is the security model surrounding not just Schnorr signatures but extensions to Schnorr signatures we really care about. I'm just going to focus on the security model evolved as we started doing this.

## Secure signatures

Let me start by describing what a Schnorr signature is. There are two purposes depending on what part of the audience you’re in to this slide. One is to intimidate you with algebra but the other is to show that what a Schnorr signature is is just really this one simple equation.

`P = xG`

`R = kG`

`e = H(P, R, m)`

`s = k + ex`

`(s, R)` is the signature

For a bit of context this Schnorr signature is a digital signature algorithm that has been proposed for inclusion in Bitcoin to replace the existing ECDSA algorithm. For a number of reasons, one of which being algebraic simplicity. You can see this signature consists of these two objects, I am not going to say what they are because I don’t want to do a math lecture here, I promise there won’t be too many more equations. There are these two objects, they are computed by these two simple equations. The only operations here, there is a `H` there, that’s a hash function, there’s a plus sign and I guess there’s multiplication, the two things beside each other are multiplication. There is no division, there is no modular inversion, there’s nothing exotic. There is no computing an elliptic point and taking its x coordinate or anything else. It is really straightforward Grade 9 algebra kind of stuff that gives us a Schnorr signature.

You would think, seeing an equation like this and having gotten through Grade 9, that maybe you could turn this into a proposal for Bitcoin and that would be very straightforward. You could do it and then a month later you would have a BIP or something and we can all fight about deployment strategies and miner collusion and all of that good stuff. But in fact it turns out there is a lot more to Schnorr signatures than just this simple equation. What this equation gives you is that the signature is correct. That somebody who knows the secret key `x` is able to produce a signature. But there’s an inverse property that cryptographic objects need to have, signatures need to have, which is security. It is not just important that a signer be able to produce a signature, it is important that nobody else can produce a signature who doesn’t have a secret key.

Let me try to formalize this intuition and we will get into why this might be difficult. By the way this is the signing and verification equation. The difference is just this and that, it goes into some algebraic simplicity arguments that I want to talk about but I don’t have time.

## Secure Signatures (cont.)

What makes a signature secure?

* If nobody (i.e. no probabilistic poly time algorithm) can extract the secret key from signatures?
* If nobody can sign a given message without the secret key?
* If nobody can sign any message?
* What if they’re allowed to request signatures on other messages?
* The same message?
* What if they change the key? Choose it freely?

What does it mean for a signature to be secure? First off you need to define your attacker somehow if you want to formalize this. The way that we do this is we say an attacker is any probabilistic polynomial time algorithm. Meaning basically any computer program, anybody who has a realistic amount of hardware including a quantum computer for example. Although as we’ll see later it turns out our signatures are not secure against quantum computers. We define an attacker as anything that is operating within the physical universe, the polynomial amount of time and space to work with. For our purposes means practical, there are fun philosophical reasons why those are interchangeable. The intuition we have for signatures is that nobody can sign a message without knowing a secret key. If you are trying to formalize that you might say “Suppose I had a polynomial time algorithm that could produce a signature”. Then maybe I could somehow use that algorithm to extract a secret key from it. If any such algorithm would be amenable to this kind of modification then it must be that somehow morally the algorithm knew the secret key in the first place and we’re good? Well no. That’s a good way to think about but that’s not sufficient because in fact it is possible to create fake signatures without knowing a secret key if you have a sufficiently broken signature algorithm. For example you can imagine a signature algorithm where the verification process was you look at it and if it has got enough bytes it is a signature. This is something that is trivially forgeable in the sense that any pile of bytes is going to be a forgery according to our definition and it is not going to be secure. Anybody can produce a sufficient pile of bytes.

We need to change this from just extracting secret keys to maybe forgeries. Now we say “Can an attacker be created that will sign some message that I choose? If nobody can sign this message that I choose then maybe that is sufficient for security?” That is not really strong enough. Let’s say the attacker is allowed to choose the message. Our security definition is going to be no probabilistic polynomial time algorithm is able to choose a message and forge a signature. That sounds pretty good. That sounds pretty general, we are letting any algorithm run, we are letting it choose a message, we are letting it produce a forgery, what more could we need? In fact there are insecure signatures that are secure under this definition. One example is say [Winternitz signatures](https://eprint.iacr.org/2011/191.pdf) that are used by some altcoins out there. The way these signatures work is that they are so called one-time signatures. If somebody produces enough signatures then anybody who sees those signatures is able to extract parts of the secret key and create a forgery. The security definition where we said nobody can create a forgery somehow failed to capture this property that this algorithm needs to be able to get signatures. Or rather if the algorithm can see signatures maybe that will help it. We’ll strengthen this definition. We’ll define an attacker as a probabilistic polytime algorithm, it is able to request signatures on whatever series of messages it wants and we have to give it to the algorithm, they have to be valid signatures. Given that, the attacker is allowed to choose another message and produce a forgery on that and then ask for more signatures say if it wants. Once it is forged that won’t help it but in a lot of protocols we let it do queries between everything that it does just to make sure that it has as much power as it possible can. What we’re doing here is we are trying to define an attacker to be as powerful as is reasonably possible, where reasonably means can we still prove security against such attackers? We want to keep on giving the attacker more and more power and hopefully we will get to a point where in principle it seems there is no more powerful adversary that makes sense to be called an adversary. We started out by saying an attacker is somebody who can extract secret keys, that is very specific. What we really care about is forging signatures. Then we say “If we want the attacker to have as much information as it might possibly need for this we’ll let it ask for a whole bunch of other signatures”.

In fact even this isn’t really enough. Our attacker here, suppose we want to prove that Schnorr signatures are secure, maybe you can define an attacker that is allowed to request ECDSA signatures with the same key or zero knowledge proofs with the same key, weird different functionality. If you want to do that you get into a security model called universal composability which I definitely don’t have time to go into. But it is much stronger than I want to consider here. There are still a few intuitive ways you can strengthen this. You can say “Maybe the attacker is allowed to request a signature on the message it is going to forge on”. You don’t want to let it just give you back the signature that you gave it, that doesn’t count as a forgery. We say that they have to give you a different signature. And then something relevant to Bitcoin, this last point, what if you let the attacker choose the signing key? Of course if your attacker chooses the signing key then of course they can produce signatures. You can’t let the attacker choose the key. But suppose we give it a public key and we say the attacker is allowed to derive BIP32 child keys from this. Can it produce forgeries then? It turns out the answer would be yes for a more naive form of Schnorr signatures where this `e` is this hash of public key `P`, this `R` object and the message `m`, if we didn’t have the public key in there the resulting signature scheme would be insecure against that more general model.

These definitions that I’ve described, these are standard definitions in the literature. The one where the attacker can request a bunch of messages is what it means to be a “secure signature”. A signature that is secure against existential forgeries under a chosen message attack, existential meaning it can choose a message, chosen message meaning it can request signatures. If we allow it to request signatures on the message it is going to forge it is called a “strong signature” which is slightly stronger. And if we let it choose a key, as far as I know there isn’t a name for this definition in the literature because of the most academic signature literature does not consider this as part of the security model. It assumes that a public key is somehow associated to some person, some identity, your key fob  when you try to get into the building and that that’s not going to change. You take the public key that’s fixed, you define your signature security assuming a fixed key and move on with your life. We already see a hint that maybe things are not so simple in Bitcoin by the fact that this is insufficient to protect forgeries using BIP32 child keys from signatures on a parent key.

## Uniformly random distributions in signature schemes

In fact there’s even more than just the security definition that I want to talk about here that gives some difficulties when trying to deploy this stuff in practice. One is that in my first slide when I had those equations to make it look less scary I didn’t mention that some of the values that you need need to be uniformly random. Uniformly random means essentially any probabilistic polytime algorithm is unable to distinguish the values generated by whatever you’re claiming to be uniformly random from an actually uniformly random thing. That’s not a circular definition but I’m not going to go into why. In real life uniform randomness is hard to come by, especially if you’re signing with a key fob or a hardware wallet or something with constrained ability to gather randomness from the environment, something that needs to run on low power. One thing you might ask is what happens if you screw up the randomness? Suppose you are supposed to generate a 256 bit random number but actually your 7th bit is usually 1, more often than half. What is the danger in that? It turns out the danger in that is that if you produce enough signatures you will leak your secret key. There is no room for biased randomness at all. Which is frustrating because when you read a paper describing a signature scheme there’s this symbol, an arrow with a dollar sign above it, which means uniformly random, drawn from a uniformly random distribution. That little symbol is not something that anybody thinks about. But in real life you have to think about it, it is very frustrating. You think “Suppose I don’t have a hardware random number generator, suppose I’m worried that it is biased. What am I going to do?” Even if I think that I can produce uniformly random values how can I convince anybody that they are uniform? How can I convince anyone that I didn’t somehow backdoor this randomness so it is biased in some way? I could even bias it in very difficult to detect ways. This is something that we worry about.

There’s a standard solution to this. You take this value `k`, part of your signature which needs to be uniformly random, and you hash your secret key and the message. We assume that our hash function is uniformly random in some nebulous sense called the random oracle heuristic. It turns out that this assumption, if your hash function is something like SHA256, has held up very well in practice. It is not really random. In particular if you give the same input to the function over and over you will keep getting the same output. You’d think that a random output would change. And it is also not really random in that if I give you a SHA2 evaluator you can plug stuff into it and you’ll be able to predict what the output will be. But because I’m going to put my secret key in here and I am going to assume that my secret key is unguessable, if I take a hash function seeded with the secret key we can treat that as uniformly random for our purposes. This is great, it works, people do this, it works very well. The result of hashing the secret key and the message is that if anybody ever changes the message they will get a different uniformly random nonce, `k` value. And if they don’t change the message they will produce exactly the same signature. Even though you are repeating your randomness the upshot of that is that you are repeating your signature, anyone can copy and paste a signature. A question you might ask is what about your secret key itself? Does that have to be uniformly random? As near as I can tell the answer is no. Don’t do that because I said that but seriously it seems like the answer is no. It needs to have sufficient entropy so that nobody can guess it. In practice it seems like this is actually secure. That is kind of surprising, you read a paper, you’ve got that arrow dollar sign symbol saying “Draw your secret key uniformly randomly and draw your nonce uniformly randomly”. The first one is advice, the second one, if you violate it even by less than 1 bit out of 256 you will lose all your keys. That is the kind of thing that really surprises you in real life. It doesn’t surprise when you read it, it surprises when you try to implement it. When you are trying to write code and people keep breaking your stuff in ways that the paper didn’t say they could.

## Sign-to-contract

`P=xG`

`R_0 = kG`

`R = R_0 + H(R_0|c).G`

`e = H(P, R, m)`

`s = (k + H(R_0|c)) + e.x`

Moving on, let me talk about one extension. I have two extensions to Schnorr that I want to talk about. One is this thing called sign-to-contract which I’ll rush through and the other is multisignatures which I’m going to rush through even more. All I want to do is highlight the security properties of this. There is this construction called sign-to-contract where you take a signature, you have this value `R` called a public nonce, it is just `kG` where G is the elliptic curve generator. You can turn `R` into a commitment. You can hide data in the blockchain using this, you can timestamp data in a blockchain. What you do is you take your nonce, you do your normal signature scheme and compute this nonce `R`, you hash the nonce along with some other secret message you want to covertly sign and then you add that to the original `R` and then you use this new object, the original is `R_0`. You use this as the nonce in your signature. This works, it's easy, it is algebraically trivial and it seems very powerful. What this lets you do is take a signature on a transaction or something and it secretly becomes a signature on some other auxiliary data. Now you can sign this transaction represents whatever metadata you want. You can sign the current state of your wallet, a timestamping mechanism. You can take arbitrary data from people and basically anchor it into the blockchain this way. You get a timestamp for zero space which is great. It seems really straightforward, you can see that the only way I’ve changed the signature scheme is I am modifying this object `R` which is public data so surely you should be able to tweak it and not have anything bad be happening. I’m not messing with any secret keys, there’s nothing secret in what I’ve changed. The final signature, I’ve just added this hash there but whatever.


## Sign-to-contract replay attack

<https://btctranscripts.com/sf-bitcoin-meetup/2019-02-04-threshold-signatures-and-accountability/>

`k = H(x|m)`

```
s = (k + H(R_0|c)) + ex
s = (k + H(R_0|c’)) + e’x
```

`0 = H(R_0|c) - H(R_0|c’) + (e-e’)x`

So we’d better have `k = H(x|m|c)`

How could this go wrong for me? We don’t even need a security model. All we are doing is tweaking public data. Well here’s the thing. In the last slide I said “Uniform randomness is hard. Why don’t we generate our nonce by hashing a secret key and a message?” If you have a hardware wallet or something that is doing that and then you ask it to do this sign-to-contract construction, you say “The next signature you make I want you to not only sign this message, I want you to also commit to this other object”. If the wallet is generating a secret nonce by hashing the real message and its secret key then if you ask it for multiple signatures on the same message but different commitments you can solve the resulting signatures and extract the secret key. The reason is in these equations which I’m not going to go into. Already we have to think a bit harder about this. The awful thing is that this is not even something that might be caught by a security model in a published paper. The reason being that the vulnerability comes from our replacing our uniformly random nonces with some sort of hash function in a way that we argued was correct for single signatures and intuitive, well reviewed and audited, in a way that is actually correct for single signatures. This seems kind of trivial, you take a random function, you replace it with a hash, what could be simpler than that? Here we are, we try to add something unrelated, we are just tweaking public data, what could go wrong? Somehow these two things interact and now you’ve leaked your secret key again.

## Sign-to-contract as an anti-nonce-sidechannel measure

* If the hardware device knows `c` before producing `R_0` it can grind `k` so that `(k+H(R_0|c))` has detectable bias
* If it doesn’t know `c` how can it prevent replay attacks?
* Send hardware device `H(c)` and receive `R_0` before giving it `c`
* Then `k = H(x|m|H(c))`

There's a solution. This is what the solution looks like. There are four things, the first three cause you to lose your keys, the fourth one I think saves you. It took many iterations, every time we would try something to prevent this something would go wrong. I would like to say more about this but I want to move on as well.

## Multisignatures

`P_i = x_i.G`

`P` = sum of `P_i`

`R_i = k_i.G`

(exchange `R_i`s)

`R` = sum of `R_i`

`e = H(P,R,m)`

`s_i = k_i + e.x_i`

(exchange `s_i`s)

`s` = sum of `k_i` + sum of `e.x_i`

Let's talk about multisignatures real quickly. Multisignature are cool, this is the big reason that we want Schnorr in Bitcoin versus the existing ECDSA. The nice simple equation I showed you on the first slide has some nice algebraic properties. If you have a whole bunch of people producing signatures you can just add them together and the result will be something that you can verify was a sum of signatures.

If you tweak this add a bunch of signatures thing slightly and you say “What if everybody uses the same `e`?” In the middle of this slide I have this `e` equals a hash of public key, nonce, message. If everyone uses the same challenge to create a signature and you add those together you will get a single signature on a single message with a single public key, where that public key is jointly controlled by all the different participants. This is really straightforward. You can see I took my first slide, I said now everyone is going to do this independently. Then at each step they tell each other what they did, everyone adds up what everyone gave them. You do that twice and then you get a signature. Multisignature, super straightforward, super fast, algebraically simple, clearly correct. Is it secure? Sure it is secure. You can see the signature is the same as the original Schnorr signature so what could go wrong?

The real cool thing about Schnorr is that the difference between signing and verification is literally just these `G`s here. I apologize for not giving any introduction to elliptic curve cryptography before saying that and smiling. If you are familiar you will appreciate this.

## Secure multisignatures

Musig paper: <https://eprint.iacr.org/2018/068>
Blog post: <https://blockstream.com/2018/01/23/musig-key-aggregation-schnorr-signatures.html>

What does it mean for a multisignature to be secure?
* Now the attacker can be a signer? Freely choose the key?
* How about all the signers? All but one?
* Start multiple signing sessions in parallel?

The thing about a multisignature being secure is not just that nobody can forge. Now you have to think about all these different signers. You have a whole collection of signers. None of them individually control the entire signing key. So now you want to think what if one of them is bad? What if all of them are bad? If all of them are bad you are back to your attacker chooses the key, that is kind of boring. But if all but one is bad that is something interesting. Suppose you have one honest signer in the middle of a multisignature, what can happen to them? Also suppose you have one honest signer and he is being asked to use the same key, or even related key, in multiple multisignatures going on at the same time. One thing that differed between this and the first slide are that there are multiple rounds here. You can think about doing stuff in parallel, you can think about being adaptive and saying “Based on what the honest guy did in the first round of all of these, now I am going to do something bad. I am going to somehow manipulate his responses or something like that”. It really makes the security model more complicated.

When I start layering on all these different things that an attacker can do in a multisignature setting we are moving away from the intuition from the first couple of the slides that we somehow defined the most powerful attacker that we can. It should be making you uncomfortable. It is starting to feel like I’m listing a bunch of attacks and saying “We are going to define our attacker to be able to do these specific attacks that I can think of and not any of the ones that I can’t think of”. We are no longer doing every attacker can request whatever they want and do whatever they want. That should make you a bit uncomfortable. But I’m not going to go into that. That’s life. You wind up with your security models for multiparty protocols that are really long and you have to review the security model really carefully even in the pure academic setting.

* In fact the just described scheme is insecure in multiple ways.
* Rogue key attacks: if `P` = sum of `P_i` then a bad signer can choose the whole key
* So set `P` = sum of `mu_i.P_i` where `mu_i` is “random”. Hash `P_i` or all the `P_i`s?
* Parallel attack: grind `R_i`s until you get a lot of `e`s that sum to each other
* So add an extra round where everyone precommits to `R_i` preventing any individual from grinding `R`.

In fact the scheme that I described, everybody added everything, is insecure. It is insecure in multiple ways. The one I’m going to talk about is simply that your attacker can choose their key adaptively. Suppose you have one attacker, you’ve got a whole bunch of honest people. Your attacker and your honest people all want to produce a signature together. Then the attacker can wait for everyone else to provide their public keys and then it will just make a public key on its own. It will subtract everyone else’s and say “My public key is this difference here”. Then when you add these altogether, the sum of public keys, the result is just the attacker’s key by itself for something that everybody in the signing protocol thinks is a multisignature key. It is actually a single signer key controlled by the attacker. There are a few iterations of ways to prevent this that we went through. In the end what we did in a signature scheme called MuSig, a multisignature scheme that works that produces Schnorr signatures, you hash everyone’s public keys together. Then every individual signer when they contribute their public key they are required to hash their index in the signing session with that hash of everyone’s keys. It turns out that prevents these kinds of attacks. But there’s another attack which I dreamed I would have enough time to go into and I really don’t. There’s a parallel attack, your attacker waits for everybody to choose their `R`s, they open a thousand signing sessions in parallel, they wait for all the honest people to choose their `R` values, their nonces, and somehow they are able to grind their choice of nonces in a way they can make a whole bunch of `e`s from 999 of these sessions to add up to an `e` from the 1000th session. Basically they get a free signature out of it. They are able to produce a forgery by doing enough parallel signing sessions, they are able to get one more parallel signing session. That was something that we didn’t see. We managed to publish a paper, we got it almost all the way through the peer review process before somebody else published a paper responding to our pre-print, they didn’t say it was insecure, they said that the proof technique we had used in our paper provably could not be used to prove that our signature scheme was secure under the assumptions they were using. This meta reduction that proved our paper had to be wrong. This is really kind of a punch. It is one thing if your thing is wrong but for somebody to publish a proof that you can’t possibly be right. It is really unfair. That’s what they did. Six months later they found an actual attack, it was insecure. We were able to fix it. The fix is fairly straightforward. The issue is that the attacker chooses their nonce after everybody else chooses their nonce. You add a pre-commit phase to your signature protocol. Now everybody exchanges a hash of their nonce, then everybody exchanges their nonces, adds them up. Then everybody exchanges their signatures, adds them up. And you’re good. That’s all that I have. Thank you all for listening.

## Q&A

Q - There’s another fun thing you can do with signatures and that is you can generate the signature using a random number generator and then compute the public key. This is used in Ethereum. The way they check an address in Ethereum, you use the `ECRecover` function, you calculate the public key, you hash it and find the address. The second thing you can do with it is you can actually create a transaction, pre-sign it by doing this, essentially it is one of the mechanisms to implement covenants without having any onchain logic. The choices you guys have had to make here in terms of keeping the thing secure have made that impossible. Is that a final statement? This is always going to be insecure, to compute a public key from a signature? Or is there any vulnerability in Ethereum because it uses this pretty fundamentally?

A - Great questions. The question is about this thing called pubkey recovery where you produce a signature, anyone given a signature can figure out what pubkey was used to produce that signature assuming that the signature does not hash the public key in the way that I described. The thing with Schnorr signatures is that the algebra required for pubkey recovery and the algebra required to do the attack I hinted at with BIP32 children are actually one and the same. If Ethereum were to use Schnorr signatures and try to do this pubkey recovery mechanism like this it would be insecure to use BIP32 as described with Ethereum. But Ethereum today is using ECDSA which is algebraically quite different from Schnorr and it appears to be different enough from Schnorr in this respect that actually there is no vulnerability caused by pubkey recovery. But my argument for that is not that there has been a paper published that demonstrates some resilience against the attack, the argument like with everything with ECDSA is that a lot of us spent a long time banging our heads against the algebra and got frustrated and gave up. To answer your meta question on whether this is a hard stance I’m taking against pubkey recovery or accidentally against pubkey recovery because I want to be hashing these public keys, the answer is yes. It is very scary especially with Schnorr where you have these linear equations that grant the ability to make your signatures much more flexible. It seems like if we don’t commit to the public key we get blindsided even more by weird attacks that you don’t think are part of your security model until you’re in Bitcoin where keys are being generated in weird ways and related in weird ways and you’ve got limited hardware. I’m pretty hard line about that.

Q - Can you talk about how threshold ECDSA have been proposed by the Princeton team compared to Schnorr as well as BLS?

A - You can produce threshold Schnorr signatures. I believe the threshold signatures proposed by Princeton, fast threshold ECDSA… You can do threshold signatures that output Schnorr signatures. You can do threshold signatures that output ECDSA signatures. On a very high level these are essentially the same. On the level of details ECDSA ones are extremely complicated. They take thousands of times as long to compute, they require some non-trivial, non EC cryptography to be doing. The implementation complexity is much higher, there are a lot more risks related to that. With Schnorr it is much more straightforward. I have another [talk](https://btctranscripts.com/sf-bitcoin-meetup/2019-02-04-threshold-signatures-and-accountability/) that I did recently at the SF Bitcoin Devs meetup that describes how to do it in slides like these. I was able to fit all the algebra onto one slide. BLS is conceptually much simpler but it is slower to verify. That is all I have to time to say. I could give a whole talk comparing these different things but it is slower to verify and requires some new crypto assumptions.
