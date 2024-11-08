---
title: Schnorr and Taproot workshop
transcript_by: Bryan Bishop
tags:
  - taproot
  - schnorr-signatures
  - tapscript
  - musig
date: 2019-09-27
media: https://bitcoinops.org/en/schnorr-taproot-workshop/
---
Location: Chaincode Labs, NYC

<https://github.com/bitcoinops/taproot-workshop>

<https://bitcoinops.slack.com>

<https://twitter.com/kanzure/status/1177697093462482949>

Run: `jupyter notebook`

## See also

Schnorr signatures and taproot: <https://diyhpl.us/wiki/transcripts/sf-bitcoin-meetup/2018-07-09-taproot-schnorr-signatures-and-sighash-noinput-oh-my/>

<https://github.com/sipa/bips/blob/bip-schnorr/bip-schnorr.mediawiki>

<https://github.com/sipa/bips/blob/bip-schnorr/bip-taproot.mediawiki>

<https://github.com/sipa/bips/blob/bip-schnorr/bip-tapscript.mediawiki>

## Why Schnorr and why taproot?

Who here already feels comfortbale with Schnorr/Taproot? This is a proposed consensus change to bitcoin. When we talk about consensus changes, we often talk about tradeoffs and compromises. It would be irresponsible to say taproot has no downsides, but I think it's important to mention it's a clear win for bitcoin.

The first win is in scalability. Schnorr because of its linearity properties allows block batch validation improvements. This is 2.5x faster block validation. This linear property also allows multisignatures to be expressed as a single signature and single pubkey on chain, which is more efficient than our legacy multisig implementation.

It's also a win for fungibility and privacy. We can express a multisig setup as a single key and signature, so the spending policy aren't leaked on to the chain. That's great, nobody knows if you're doing 3-of-4 or 50-of-100 multisig or if it's a single signer. Today, though, that if you see a 2-of-3 multisig on-chain it's a good chance it's Bitgo. Schnorr hides all of this and removes it from the chain. That's great for privacy.

Another aspect of schnorr/taproot is that there are spending paths that are hidden unless they are actually executed. You can have rich contracts with complex spending policies, which never appear on the blockchain. This is again great for privacy.

Another reason is functionality, like having very large multisig like 1-of-2 or 4-of-7 or 50-of-100 and they all look the same on chain. You can have much larger scripts with different spending paths, so you can have complex spending conditions. You can have adaptor signatures, atomic swaps, blind signatures, discreet log contracts, we're just getting to explore the functionality available here.

## Schnorr signatures

I am going to talk briefly about Schnorr signatures. They are better than ECDSA. Becaus eof the encoding used in bip-schnorr, they are 11% smaller than existing signatures. They are compatible with existing private keys; you can just use Schnorr with your current private keys. They have the same security assumption, but with a formal proof which is not available for ECDSA. Also, the verification algorithm is linear and I'll show later why that is great and allows a lot of new functionality.

Schnorr uses the same elliptic curve, field and group, so your private keys can be used both with ECDSA and Schnorr without any change to the private key.

## Schnorr enables key and signature aggregation

In traditional bitcoin script, for multisig, you would place 3 public keys and 3 signatures on chain for a 3-of-3 multisig. But in Schnorr, you can use Musig to aggregate the keys and you get an aggregated key.

## Script trees

In taproot, we can have multiple spending conditions. We can have a primary spending script and an alternative spending script. We can place these scripts into a merkle tree. When we spend one of them, like if we're revealing a spending script, we can reveal only one branch of the merkle tree of scripts and we don't need to reveal anything about the alternative scripts.

## Tweaking the public key

We have a public key, and we tweak that with a commitment to the script. So this taproot output can either be spent with the original public key which could be a single key or an aggregated key, or it could be spent with either of these scripts in the merkle tree here.

As an example, imagine you have an exchange and you have a third-party that co-signs all your withdrawals. One way to do this would be to sign a 2-of-2 which would appear as a single signature with your third-party, and you put the other 2-of-3 into a tree. The majority of the time you spend with 2-of-2, and only if you need to use your cold storage do you use one of these other script paths. We'll go into this later as well.

## Why Bitcoin Optech?

Why are we doing this? Why is Bitcoin Optech involved? We started Optech 18 months ago because we wanted to help bitcoin companies adopt scaling technologies. At the time that was batching and fee estimation, but we're also looking at what's coming along like Schnorr, Taproot, eltoo maybe. We're also helping to get Schnorr and Taproot reviewed and later implemented by services. So we want to help drive adoption of scaling tech to bitcoin.

## Why this workshop?

Schnorr/taproot is still a few months or a year out. We still want to share the current thinking around Schnorr and taproot. Pieter and Andrew have been working very hard on this proposal. They want to share with people in the industry what the current thinking is, around taproot. We want to give you guys a chance to play with the technology, write code, and see what you can do with the technology. We also want you involved in the feedback process. Right now the proposal is going through community feedback right now, and we want you guys to be able to take part of that feedback process since you guys are the ones who will be implementing it out when this gets rolled out.

## A few warnings

Schonrr/taproot is a proposal. It will change. In fact, it has changed. In our notebooks, we were using 33 byte public keys. But in the proposal, they have now switched to 32 byte public keys.

There is no roadmap. Nobody is in charge of bitcoin and says when we can make a consensus change. This stuff could be rolled out and implemented, it could be in 6 months or many years, we don't know. It probably won't be 1 month.

Also, all of the code you see today is only for educational purposes, please don't spend real money with our libraries. They are not secure.

bitcoind v0.19 makes spend-to-taproot standard. So you can spend to these addresses. The wallet has always let you spend to v1, but they were not accepted to the mempool. So from v0.19 they will be accepted, and by default miners will include it, if it's accepted to the miner's mempool.

## Elliptic curve math

We'll go over this quickly to refresh everyone.

In elliptic curve math, we have scalars which are nmbres. All of the scalars are over modulo arithmetic. You do an operation between A and B and then you do modulo n. The modulo here will be of the group order called SECP256K1\_ORDER. Division done using modular inverse requires Fermat's little theorem. Numbers can go from 0 to (group order - 1) because it's modular arithmetic. So 15 + 9 mod 21 is 3. So 24 mod 21 is 3. If it's higher than the modulo, you need to subtract the order. If it's lower than 0, you need to add the order. So these are scalars.

Now we'll talk about points on an elliptic curve. There are x and y coordinates. There's something called the generator point which is a way to take scalars and project them into the curve. We'll see in a second how this works. The points in secp curves form an abelian group. What does this mean? It's about closure. If A is a point and B is a point then A + B is also a point. Let's look at integers. They are also an abelian group. 5, 7, and 12 are all integers. There's also associativity meaning (A + B) + C is the same as A + (B + C). Also, there's an identity element meaning, in integers if you do 5 + 0 you get 5. But in elliptic curves, you have an infinity point. A plus infinity is A if A is a point. There's also the inverse property of an abelian group: for any point A there exist some point B such that A + B = 0. So for every A point there's a minus A point. Another property is commutativity, such that A + B is the same as B + A. This should give you some intuitoin that the math over points is similar to math over the integers.

Scalar operations are a bit different, though. There are ways to do operations between points and scalars. So you can multiply a scalar by a point. So you can multiply the scalary by the generator point G. So we take a scalar s and multiply by the generator so it's sG = (G + G + G ....). By contrast, point by point division isn't feasible and it requires solving the discrete log problem.

Let's switch over to the notebook.

<https://github.com/bitcoinops/taproot-workshop/blob/master/0.2-Elliptic-Curve-Math.ipynb>

ECKey.generate will generate a valid scalar, so that you don't have to run randrange(1, SECP256K1\_ORDER). There is also a function generate\_key\_pair to help make your life easier.

To get the negation, take the order minus the scalar. But if it's part of a bigger operation, then the modulo operator will take care of that in python. In C or rust, modulo operator doesn't work as expected on negative numbers. In python, it works as expected. In C and other compiled languages, it doesn't work like that. The negate method negates it in place, that might be confusing.

## Schnorr signatures

Schnorr is where things get interesting.

So how does Schnorr work? To help everyone, I have put a glossary here at the top.

m is a message.

e is a hash of what we'll sign, it will be E = H(R || P || m).

G is the generator point.

d is our private key which is actually a scalar.

point is a scalar * G (which has an x and a y)

P is the public key (P = dG).

k is a random nonce

R is the nonce point (take the nonce and multiply it by the generator to get a point) (R = kG)

Schnorr has signing and verification. To verify, you do sG = kG + edG.  For signing, s = k + ed   (Sig(s, R)). e = H(R || P || m). So Sig(s, kG). If the verification equation holds, then the signature is correct.

e is H(R||P||m) where R is the public nonce, P is the public key that you want to verify with, and m is the message you're signing. s is a scalar, so 32 bytes. The point has an x and y, which are each 32 bytes. But we don't want to increase signature size compared to bitcoin today. So what can we do about this?

We can remove the y value and we can still tell what the point is. If we look at the equation for secp, we need to do a square root to solve for y. Secp256k1 is y^2 = x^3 + 7.  So you need to solve for y, meaning +- square root of (x^3 + 7). We can say, even or odd, which will provide some information. If you take an odd number and you subtract an even number from it, so if y is an even number then you get an odd number, meaning that if the +y is even, then to get the -y then we're doing order minus the number. This will give us an odd number then. If the +y is odd, then we're doing the order which is odd minus y, which gets an even number. So if we can restrict and say for instance we're only accepting odd y values, then that's all you need to know. So you give someone an x value, and they solve it and get a y value.

Another way is to do lower/higher half. You can say, I'm only using y values wihch are higher than half the order. The third option is quadratic residue which is more complex, but basically it means that there's some square root. The y value has a valid square root. In integers, 49 has a square root, but 7 doesn't. So quadratic residue means that it has a square root.

In practice, all of these are valid ways to do it. These are three separate ways to do it.

Q: Why do you know one of them will be a quadratic residue?

A: I hoped nobody would ask this. Minus 1 is a quadratic residue. Minus 1 is the group order minus 1, and it has no square root. Euler criterions say... a rule of thumb is that a quadratic residue times a quadratic residue is a quadratic residue. So quadratic resude times non-rquadratic residue is quadratic non-residue and quadratic non-residue times quadratic non-residue is a quadratic residue. If you want, after this I could prove this to you with Euler's criteria.

In practice, we actually use quadratic residue. I assure you, it's all number theory and proven. There's nothing funky here, it's a very known thing. It's a bit complex. But in practice, it gives us high performance in verification. Because we're using this part and not the other two, we can verify faster, and it gives us the same exact assurances of the other two ways.

With this, it means we're only sending x. This means the signature is going to be 64 bytes which is less than the current ECDSA signature size which is up to 72 bytes. So we have made Schnorr better in signature size than ECDSA.

Now let's go through the notebooks: <https://github.com/bitcoinops/taproot-workshop/blob/master/1.1-Introduction-to-Schnorr.ipynb>

The signature s is k + H(x(R) | P | m)d where k is the nonce, x(R) is the x-coordinate of R (the nonce point), d is the private key.

To check if it's a quadratic residue, we use the Jacobi symbol. It's a nice tool that tells you if something is a quadratic residue. So you give it a number, and the group order (the field size), the modulo you're working on, and it returns 1 if it's a quadratic residue, and -1 if it's a quadratic non-residue, and 0 if it's 0. We'll need to give it the y value because we're limiting y to be the quadratic residue. So then we give the field size. This is the only place today where we'll use the field size instead of the group order. The coordinates x and y are modulo the field size, but everything else like the points and scalars are modulo the group order. The only place you need for computing the field size is for the Jacobi symbol. The field size doesn't relate to the group order. The field size is what it's chosen for the coordinates. In elliptic curves, we take some field, and the group order is the result of that, then we check how many points are possible and that's the group order. We only care about the group order, usually. Only because we're playing with the y value, we care about the field size.

Q: Is that how far it goes up in the cartesian plane, and what the cutoff is in the graph?

A: Yes. Pub keys are modulo.

So you choose a nonce k, you take the point of that nonce, and then you take y from that nonce, and you check if it's a quadratic residue using the Jacobi symbol. If it's a quadratic residue, then great. If it's not a quadratic residue, then you need to negate it either by negating the y value or the k.

In the Schnorr workbook, see example 1.1.1 to see how to calculate a valid nonce.

There's an exercise 1.1.2 to choose a nonce, check if it's a quadratic residue, and if it's not, you need to negate the nonce. If anyone is stuck for some reason, there's solutions in the text file that you can use to cheat. This exercise is for "vierfying that the inverse nonce values k and -k generate inverse points R and -R".

Q: Why is the quadratic residue approach faster for verification?

A: Because in most computation, you have Jacobi coordinates and... you have three coordinates rather than 2, you convert from one to the other. You converting from Jacobi to Alpine is very expensive. To use quadratic residue, you don't need to do the conversion. So you look at the final y coordinates and test if it's odd or even; but it's true that your quadratic residue will always be the same in alpine and jacobian coordinates. You avoid the conversion.

Q: What are three jacobian coordinates?

A: It's a projection in 3-space. It's x, y and z. It's a different coordinate system. Your y is divided by z^3, and your x is something else. It's an optimization thing. It doesn't really matter to the math.

Are you familiar with projective coordinates? It's a re-parameterization of projective space, using a square scaling factor for x, and your scaling factor for y is a cube.

Let's go over the answers: <https://github.com/bitcoinops/taproot-workshop/blob/master/solutions/1.1-schnorr-signatures-solutions.ipynb>

In 1.1.2, we wanted to check the inverse and check that ... so we're generating k and R, we're taking the x of R and the y of R. We're negating k by doing order minus k.secret, and then we're creating minus R from that minus K value. This will also return us an EC Key for that scalar. So we can easily do operations without thinking about the modulo. So then we take the minus R x value and the minus R y value. So we assert the R x value is the same as minus R x value. So then we assert SECP256K1\_FIELD\_SIZE minus R's y coordinate is the same as minus R's y coordinate.

In 1.1.3, the next operation is to sign, to create a Schnorr signature. Here, you create a private key and a public key. Here you create a nonce and a public nonce. You need to implement here the jacobi symbol to check if it's a quadratic residue or a quadratic non-residue, and if it's a quadratic non-residue then you negate it. Then we take the X coordinate of the R value, .... you need to hash them together to get the e value, and then you need to use the signature equation, and then the asserts should verify where you run the Schnorr verification equation.

Q: Inverse points mean that the x is the same, but the y are inverses?

A: Yes.

You need to negate k to sign, but if you're verifying you can just negate..... Correct.

Q: The generate key pair is not in the bitcoin test framework?

A: No. You'll see in the next chapter, there's a bunch of new functions.

Let's go over the solution for section 1.1.3. Again, we generate a private key, public key, nonce, public nonce.  We take the X coordinate of R, we take the bytes of the public key, we hash them together to get e. Then we do the Schnorr equation to do k + h * d where h is actually like e but it's a hash result. THen we take the signature, which is the X of R as bytes in big endian order, plus s.secret.to\_bytes(32, big endian).

Section 1.1.4, this is something interesting and important. Until now, we created random nonces. In python, it's fun to use random.randrange but in practice random is complicated and it's not such an easy thing. We don't want to rely on every signature to need a random number, because if the random number is bad then someone can crack our private key. So we want a deterministic nonce. It's a way where we can get a nonce without having to generate random stuff every time. So what we will do is we will hash our private key and the message together to get a nonce. So if we sign the same message twice, we get the same nonce. Since nobody else knows our private key, nobody can know what's in that nonce. So in 1.1.4, we'll do the same thing again, but this time we'll use a deterministic nonce. The verification will pass if it's a random nonce, or even if it's a deterministic nonce. Signature verification will pass in both cases.

There's a typo in 1.1.4 where it says pubkey in the comment, this should be the private key. If you do use the public key, then the assertion won't pass. See <https://github.com/bitcoinops/taproot-workshop/pull/104>

## Musig

Now we'll switch to talking about Musig.

paper: <https://eprint.iacr.org/2018/068>

<https://github.com/bitcoinops/taproot-workshop/blob/master/1.2-Introduction-to-Musig.ipynb>

Something nice about Schnorr which is not available in ECDSA is that because the function is linear, we can do multisignatures. We'll start by going over the naieve multisignature and how it looks like and how Schnorr makes it easy. Then we'll show some problems with it, and how to solve those problems.

The naieve version of key aggregation is s1 = k1 + ed1, and s2 = k2 + ed2 and then we add s1 + s2 to get (k1 + k2) + e(d1 + d2).  So say we simplify this and call it s prime = k prime + ed prime. So as you can see, this is the Schnorr signature which is valid for d prime. D prime is (d1 + d2). So we get a signature which is valid for the public key which is the addition of their public keys. This is pretty awesome, it's very simple. The problem is that there's ways to attack this.

Specifically, there's something called key cancelation or rogue key attack. The way it works is that say we want to do a multisig and I'm the second party. Say the other party sends me a public key, but instead I subtract his public key and I tell him my public key which is constructed in a certain way. He accepts it, and he adds his public key with my public key, to create a multisig key. So I told him a public key, but it is actually P2 minus P1. So we have P1 and minus P1 and they cancel each other out, and he actually gets my public key. As a consequence, I can sign for everything, which is obviously a problem.

Musig is a great paper by Andrew Poelstra and Pieter Wuille and others. It solves this problem by adding musig coefficients. The idea is that we need to create some random number based on everyone's public keys, such that you can't predict what that number can be without giving your public key. That number is going to change the public keys so that if you try to do the rogue key attack you have a problem; you need the coefficient to do the key cancelation attack. So the way it works, again, is that we have two parties here. We're creating a hash with the list of the parties. The hash will contain both of the public keys, and the public key of the person with.... The point is, the hash function is based on everyone's public keys, and it's unique per participant. So now they get this ci value which is the result of this hash. Each of them can modify their private keys by that coefficient, and the public keys. Because this coefficient is based only on public keys, then as long as everyone knows everyone's public keys, you can calculate the coefficients for everyone, and calculate the corresponding public keys. By multipliny c1 by P1, you can get a public key that you can sign for by  multiplying d1 by c1. You need the public key to get the coefficient, and you need the coefficient to know what to subtract from your public key. This protects us against a key cancelation attack, and it's non-interactive because you only need the other people's public keys. There's no required signatures or whatever. If you do a commit-reveal scheme with a hash function, that would be interactive. This is for key generation, which is non-interactive.

For signing, there's another problem. In signing, the security proofs of musig requires you to create the nonce individually. Pieter actually told me 2 days ago that there's an attack here; it's not just that the security proof is invalid, it's that there's an attack if one of the party knows one of the nonces when he makes his own nonce. So now we need to do nonce commitments. So when we do the actual signing, this is about creating the public key or address. But now we go to signing.

When we go to signing, everyone needs their own nonce. Before they exchange nonces, they need to commit to them. See that e has the combined nonce R prime and the combined public key P prime and the message. So to create a signature, we need to know what key we're signing for, and what the public nonce is.

So we first exchange commitments. Each party generates their nonces, and each party will have their own public nonces. The naieve way is to share their public nonces, everyone adds them up and then they sign. But the seecurity proof shows that we first need to commit. So everyone sends a hash of their public nonce, and once everyone has everyone's commitments, then they verify the nonces are valid for the commitment. Everyone locally hashes the public nonce, and makes sure it's the same that they were committed to. Such that, we know tha teveryone created the nonces without knowing what anyone else's nonces are. This commitment is interactive, and signing is going to require 3 rounds of communication. You'll actually do it now in the notebook.

Q: In two slides ago, did the participants still have to exchange public keys, or do they multiply...

A: They first exchange, because to know the c value you need to know the public keys. For key generation, everyone has to exchange public keys. It could be interactive, but if there's an HD seed then you know everyone's public keys. After you know the public keys, you multiply each public key by the corresponding coefficient, you add it up, and there you go. To sign it, you need to modify your own private key.

Q: So those c coefficients, are deterministic too once you know all the parties ---

A: Yes, they are deterministic. I don't know if that's the right word, because you're not supposed to reuse public keys. Everything in ci needs to be public information, but the idea is that it contains everyone's keys and something unique about each participant.

Q: Does ci need to be modulo the..

A: Actually, the group order. But the group order is close enough to... so the chances of this being over the group order are fairly small. So you can either do modulo or hash. Usually modulo over random numbers isn't a great thing, but since the chances are so low, it's probably fine.

AP: In libsecp256k1, we don't check that. It's never going to happen in the lifetime of the universe. I promise.

The coefficient could be 0 and then you get into problems, but it won't be 0.

In Musig, you shouldn't use deterministic nonces. If you use deterministic nonces, then someone can basically break your private key out. It's easy to show it. Say there's two parties. We start the signing protocol. Party one sends s1 which is k1, his deterministic nonce. So there's multiple rounds and you can.... exactly. As the second party, maybe I drop connections on purpose or it's an accident. The communication is done. Now we're retrying, to do the same thing. Before we got here, we first exchanged nonces. We did the nonce commitment and then the exchange. So we had k1, he had k2, we exchanged these values, etc. Now I drop the connection, and we redo everything. This time, he's going to send k1 because he's using a deterministic nonce and we're signing on the same thing. But I'm going to send him k3, and I'm not going to use deterministic nonces. So now he is going to create a signature s1 prime which is going to have his nonce k1 but now with the hash of R double prime, because the combined nonce is now different, with P prime and the message and then the hash gets multiplied by d. With these two signatures, we can--- someone can solve for the private key. If you can prove that everyone is using deterministic nonces, then that's okay-- but the problem is, how do you know everyone is using deterministic nonces? But then we can do a zero-knowledge proof. So we're assuming the counterparty isn't recording the deterministic or non-determnistic nonces in a database, which is an unreasonable requirement because there will be a lot of storage requirements and the wallet will require a database of all the past signatures. So you couldn't restore from seed on a hardware wallet, so it assumes the counterparty is stateful. Anyway, using determnistic nonces is dangerous, that's the conclusion.

The coefficients are sometimes called challenge factors.

The musig paper proposes uses lexical sorting for constructing ci the coefficients. We want to standardize this across the industry. There should be lexical ordering of the keys, or maybe we could argue for something different that might be more efficient like start with the key you're hashing for and do lexical ordering for the rest. There's different ways to do it, but we need a BIP if we want it to be a standard across the industry.

In the next section, we'll move from key generation to signing for musig. For signing, we need everyone to generate a nonce, commit to the public nonce, then exchange the public nonces, and then they can do the 3-round signing protocol. So here what we're going to do is exactly that; we'll generate three nonces. Here we're not using random ones, we're using a hard-coded one so that the asserts are easier to check. We could have done a verify signature assert, but we also want to check some other stuff.

You can use the function aggregate\_schnorr\_nonces which will add them up and return a boolean, if you need to negate them. We still need to check if the resulting R point is a quadratic residue or quadratic non-residue. If it's not a quadratic residue, then all the nonces, all three, need to be negated. After this, we get to signing. This is about the commitments and aggregating the nonces. If you add them up and it's not a quadratic residue, then you can negate all of them and add them up, and that will by definition be a quadratic residue.

Q: Is the Schnorr signature generation and verification already in mainstream libsecp256k1?

A: It's not in mainstream, but there's a pull request by Jonas Nick. It will only get merged once the community has consensus about adding taproot and Schnorr. It will probably occur around the time that these proposals get merged into Bitcoin Core.

Round 1, they generate nonce point commimtents and exchange them. Round 2, they exchange the nonce points, and each participant verifies that the nonce point commitment matches the nonce. Then the nonces get aggregated together. If the aggregated nonce is not a quadratic residue, then negate the aggregate nonce and individual nonce scalars and nonce points.

You shouldn't negate the nonce points in the ... aggregate. So the boolean will always be false. You don't want to do it twice. When you aggregate the nonces, you shouldn't negate the nonce points. In reality, you don't need to negate the aggregate point, because we're only using the x value for it, and the x value stays the same anyway. The interesting thing to negate are only the k scalars.

<https://github.com/bitcoinops/taproot-workshop/pull/106>

Now that we have exchanged nonce commitments, we created an aggregate nonce, we negated the scalar nonces if needed. The last part to do is to create the signatures, add them up, and prove that with musig we can verify the signature just as if it is a regular signature. Then you pass it to the regular verify schnorr function, it's not a musig specific verification function. So we need to create partial signatures, add them up, and verify that they are correct for the combined key.

There's a function called aggregate\_musig\_signature which accepts a list of partial signatures and it will add them up for you, and will return a valid signature.

If you use bip32 with your nonces, yeah don't do that. If you really really want, you could do a random seed and feed it into Chacha20 and then create nonces. But this doesn't solve most of the problems. Even if you were to specify that everyone must use deterministic nonces, someone could still just not, unless there was a way to prove it was a deterministic nonce. Is it insecure if you know the other guys nonces ahead of time? Yes. In parallel, you could initiate a bunch of signatures, so everyone commits to a hundred nonces, they commit to a hundred nonces, and then they reveal a hundred public nonces, and then they have a stack for the next year to keep signing with musig.

In musig, you don't really use non-deterministic nonces. If you do all the signing communication online public, then yes... But if you're doing it in private, then you have the same security problem with random Schnorr where with the aggregated signature you have entropy from all the participants. So it's highly unlikely to see your reused R value on-chain. But still, between them, we don't want to rely on anyone being trusted. So between the participants, it's still the same security model of using random nonces in Schnorr, but outside of that I would argue it's a bit better.

Okay, should we go over the answer for this? So we're hashing a message, then we're creating three partial signatures using the function sign\_musig which gets the tweaked private key, the nonce, the aggregated public nonce, the public key, and the message. This is just a helper function that hashes the-- it creates e, which is the hash of the X coordinate of R, the public key and the message, and then it does the modulo the order in case it's bigger, and then it's basically the schnorr equation. So it's a helper function to help do that. Now that we have the partial signatures from all the participants, we just use aggregate\_musig\_signature which just sums them up and modulo the order. Then it does a conversion to make it a valid signature by converting it to bytes and then adds R to it. Then we pass it to verify\_schnorr and it passes. Yahoo. This is the full musig scheme, and it works. Now that you have an aggregated signature and aggregated public key, there's no way to know that it's a musig. It looks just like any other Schnorr signature out there. And that's it for musig.

Any questions about Schnorr or Musig before we break for lunch? We're a little bit ahead of schedule.

Q: Could you prove that this was a musig, if you wanted to, by revealing the partial signatures? Is there deniability?

A: Revealing partial signatures doesn't help, because you can fake partial signatures. But what you could do is prove that the public key is an aggregate of multiple public keys. You can take the partial signatures, take a random scalar, and subtract, and say here's two values that come together to be the aggregated s. But with the public keys, because the coefficients contained the original public key, I think it creates a commitment. Right Andrew? Sorry. Theoretically, could you prove a musig aggregated public key is a musig key by revealing the coefficients and they then act as a commitment. In the signature, I don't think you can prove it, but on the public keys you can do it, if you have the original public keys and the coefficients. I think the coefficients act like a taproot commitment of some sort since they contain the original public keys. If I just give you the commitments, then you can't tell that I didn't make them up. You need the full list of the original public keys to prove that the aggregated resultant key is in fact a musig key.

## Taproot

You can add additional script encumberences to a taproot output. We have a few chapters about taproot, and then a case study, and then a write-up. It's a great idea outside, so I recommend using the deck during those five minute breaks between the sections.

So first a few main takeaways for the motivation behind taproot and what we're trying to do here. A taproot output allows us to have a default spending path. The default spending path is simply spending a public key. With Schnorr signatures, you can have a single key and a single signature, or you can have multisig and it's indistinguishable on-chain. Also there's the ability to spend the same output through alternative spending paths, and these alternative spending paths are encumbered with bitcoin script called tapscript. So these are the two ways you can spend a taproot output. This becomes more intuitive when you look at an output that has a multi-party contract. In a multi-party contract, the default spending path is an aggregated pubkey/signature, and the alternative spending path is the different scripts that we commit into the output. This gives us multiple ways to spend it. If the parties agree that the contract can be spent, then they might as well just use the default spending path and this reveals none of the other alternative routes by doing that.

So the default spending path is just the taproot public key. We'll look at how that is encoded in a segwit output. If you want to commit alternative spending outputs into that taproot public key, then we use a tweaked internal key which commits the different tapscripts we want to put into it. There's a tapscript commitment tree that lets us commit multiple tapscripts, and we have some design freedoms around how to structure that taptree.

Q: A tweaked internal key is a tweak of the..

A: The taproot public key is a tweak of an internal key, and the internal key is only revealed if you want to use one of the alternative spending paths. Otherwise the internal key doesn't need to be revealed.

### Segwit v1

Segwit v1 is about this high-level taproot public key. It's about how we encode it in an output. So the segwit v0 format is a version byte plus a witness program which can be 20 or 32 bytes, if it's a P2WSH. In segwit v1, we have a version 1 as the version byte, and then we have a 32 byte public key as the witness program. We have 33 byte public keys in the jupyter notebook because a previous version of the proposal used 33 byte public keys, but the latest proposal uses 32 byte public keys.

So there's two spending possibilities: there's the key path, where you can provide a 64 byte bip-schnorr signature. The alternative paths are represented in the script path. So there's a key path and a script path. Here, in this chapter, we're just looking at the key path because we're just looking at the public key.

Is there anything controversial about that public key? Well, quantum resistance. Pieter Wuille's view is that there's already 5 million BTC in revealed public key outputs. So the whole economy will collapse anyway.

### P2PK vs P2PKH

V1 script is version 1 and a 32 byte public key. The v1 witness is a 64 or 65 byte signature.  In v0 script, it's 00 and a 20 byte pubkeyhash. The public key is going to be revealed anyway, so there's no disadvantage really. Another thing is that when people talk about quantum security from pubkey hashes, the idea is that maybe one day we would hard-fork in a zero-knowledge proof to let you spend those old coins to prove something. But say thta we had software that could spend all the quantum-compromised coins, and we say, if you provide a proof of your taproot derivation or something, and you do that in a quantum-resistant way, then maybe you could spend with a zero-knowledge proof. So with a zero knowledge proof, I could spend the p2pkh output without revealing the public key. Also, in a post-quantum world, if your xpub is exposed, then they know all your public keys.

### Taproot sighash flags

In general, taproot retains all the legacy sighash flag semantics. We have ALL, NONE, SINGLE, and ANY. There's also a new one implied all, which works as follows. Say I have my Schnorr signature with 32 bytes for the x-coord of the R point, and an s value which is also 32 bytes. If I don't use a sighashflag byte, then SIGHASH\_ALL is implied. You could use the byte, but that increases the size by a single byte.

SIGHASH\_ALL is the most used and by far the most common. So you get to save a single byte. In taproot, you could add the byte for SIGHASH\_ALL if you want, but it's not required.

### Taptweak

Let's look at the notebooks.

<https://github.com/bitcoinops/taproot-workshop/blob/master/2.1-Segwit-Version-1.ipynb>

In this notebook, we're going to use a segwit v1 example that we send coins to from the coinbase outputs. Then we construct a CTransaction that spends this taproot output back to the wallet address. So we'll take a segwit v1 output, we'll spend it on the public key path, and in the future we'll do a spend using one of the script paths, but the pattern remains the same and we're going to do this over and over again.

We take the segwit v1 output, and we're encoding it as one version byte plus the 32 byte public key. So let's do the example of constructing a segwit v1 output. We generate public and private keys. Then we create our witness program as follows. It's version 1, and then the public key in bytes. We're creating the address to which we want to spend. The output is going to be the version byte plus the witness program, and the witness program is the public key but the first byte of that public key is either a 0 or 1 which indicates the evenness or oddness of the point. So we're slicing out the first byte here, which is from the compressed pubkey. In the compressed pubkey, we have a 2 or 3, and we want a 0 or 1. We determine the oddness by bitwise AND with '1' with the first byte of the pubkey. So the address is created with program\_to\_witness(version, program).

We're using Pieter Wuille's taproot branch, which uses 33 bytes for public keys instead of 32 bytes, even if bip-tapscript says use 32 bytes. Once there's a branch with 32 bytes, then we'll use that.

So bitcoind v0.19 makes it standard to send to segwit v1... so what's standard now? So, segwit defines witness program is between 2 and 40 bytes, for all segwit---... any unknown version, are 2 and 40. I thought the idea was that once you figure out what the length will be, you soft-fork that in? But this is just a standardness change, not a consensus change. The standardness change is that, any segwit address, for any version-- 0 is different, but for any future segwit version, sending to any length witness program is now considered IsStandard. There will be another standardness change to add any restriction in the future.

Moving on, we've created our standard segwit v1 output. Now we want to send funds to it from the Bitcoin Core wallet. So we do that by setting up a util\.TestWrapper which is exported from Bitcoin Core. This is just a bitcoind test. You can call setup on it, and it will spin up a node and logging and in our case a single bitcoind instance. We can access the RPC interface direclty through the test.nodes list. So we set it up, and we can generate funds for the wallet directly by calling test.nodes[0].generate(101) so that the first block is spendable after 100 blocks of maturation. Then we make a transaction by calling sendtoaddress(address, amount\_btc). In the second step, we decode the transaction using getrawtransaction(txid) which returns the transaction hex string. Then we call decoderawtransaction(txhex) and we want this because in order to spend the transaction output we need to know the txid and the position of that output. Because the Core wallet randomizes the change output, we search for which one is change.

In part 3, we create a CTransaction object and we populate the members of the object. We have nVersion, nLocktime, the list of inputs, the list of outputs, and we have the witness (vtxinwit). The outpoint is the one that we found before, it's at a randomized index that we searched for. We can set the input to be that COutPoint. So now we have a transaction template. Now we have to populate outputs. This is what happens in section 2.1.6. Here, we spend our custom v1 output and spend it back to the Bitcoin Core wallet. So to do that, we need a new address from the wallet, and we obtain that by calling getnewaddress. We generate a new address, and then we can get the actual output script with the getaddressinfo call. We generate an address, we decode the address, then we get the scriptpubkey implied by the address. Then there's a min\_fee calculation here by calling getmempoolinfo to get the mempoolminfee value. Then we construct a CTxOut object for making the output, and we have the amount minus the fee, and we pass the scriptpubkey into that output object. Then we populate the output list with that object. Then we should be ready to sign. Here the witness is still empty because we haven't signed yet. The scriptsig is empty because it's a native segwit spend.

In section 2.1.7, we can now sign. Here's an overview of some of the sighash flags, including a new one which is an implied SIGHASH\_ALL which in most of these exercises we use. In order to generate the taproot scripthash, you call TaprootSignatureHash and you pass in some of the values. Then we sign using Schnorr, and we get a signature. Now all we have to do is we append that signature to the CScriptWitness witness object. So we do witness = CScriptWitness() and then witness.stack.append(signature).

To spend it, you serialize the transaction, and then you do testmempoolaccept to test whether it would be accepted by the mempool. Now we have the full transaction, and the witness is populated with CTxWitness(CScriptWitness(...)).

Now we're going to do the same thing, but with a musig public key. You can use a single sig, multisig key, or a musig aggregated key. So we're going to do the same thing as above, but we're going to use a different key. We're going to generate a segwit v1 address for a 2-of-2 musig aggregated public key. This is section 2.1.9. There's no real gotchas there. You can use generate\_musig\_key(ECpubkeylist). You'll have to generate the witness program, and from that you're going to be able to generate the address.

<https://github.com/bitcoinops/taproot-workshop/blob/master/solutions/2.1-Segwit-Version-1-Solutions.txt>

In section 2.1.11, you're just printing out a transaction template for spending a musig aggregated key address. Just constructing a transaction which spends the musig segwit v1 output. So, initiate a CTransaction object and populate the version, locktime and inputs. We set the input as a COutPoint of the musig transaction output with the right index. In this example, we send the funds back to the wallet address, which we don't need to do but it makes the example a little easier to understand.

In section 2.1.12, the goal is to create a valid bip-schnorr signature for the musig aggregate pubkey. Then add it to the witness, and construct the witness so that the transaction can be spent. To create the sighash, you'll have to call TaprootSignatureHash and then sign that by running through the musig signing protocol.

The only tricky part is the TaprootSignatureHash which gives us the transaction digest we want to sign. We pass in the CTransaction object we're populating (the spending transaction); we pass in the output which is the output we're spending, and then we have some toher parameters. scriptpath is a parameter that says am I spending along a scriptpath or a keypath. Since we're spending along the keypath, this is set to false. Then we aggregate our nonces; we negate if we need to, and then we sign, and then we aggregate the musig partial signatures.

The nice thing about spending along the keypath is that the witnesses look the same regardless of how we generate the public key. Nobody can tell if it's a single party or multiparty key.

## Taptweak

<https://github.com/bitcoinops/taproot-workshop/blob/master/solutions/2.2-TapTweak-Solutions.txt>

Any data can be committed to a public key tweak. There's some nice properties of this that we will use for taproot. Generally speaking, the owner of the public key, the one that can spend it, can do so as long as they have knowledge of the tweak. Doing the key path spend doesn't reveal the tweak or the committed scripts inside of that taproot output. The owner of the private key can later reveal the commitment without revealing the private key.

If we look at how this applies to taproot, we have a taproot public key. The first chapter that we just went through where we spent a segwit v1 output, that public key is the taproot public key. But we can take a public key and tweak it to arrive at this taproot output. We're going to have an internal key, we are going to tweak the public key, we're going to commit data to the tweak, and to an observer on-chain the resulting public key looks like any other public key. So the privacy is nice. We're going to start with a data commitment to demonstrate a point, but you can also do a script.

So the v1 witness program is a 32 byte pubkey Q. Q is a tweaked internal key. Q = P + H(P|c)G where P is the internal key and c is the commitment.  We can spend with the private key of Q without ever revealing the commitment. We simply tweak the private key with the same hash digest, the hash of the digest and the commitment. The spending witness is a 64 byte signature.

We need to hash a  pubkey point together with a commitment. Say we take the commitment and we tweak our internal key directly with that scalar. The problem is that for a given taproot output point Q, I could modify my commitment and I can solve for an alternative private key. So the pubkey point is the same, but I change my commitment and I can solve for another private key, and this linear relationship holds. If, however, we place the commitment inside the hash, this breaks the linear relationship and I can no longer solve for an alternative private key. So the commitment data is inside the hash together with the pubkey.

Taptweak is chapter 2.2 in the notebook. We're going to commit data to a pubkey point, and then spending that pubkey point without revealing the taproot.  So here's a recap of how to tweak a point. The taproot output point is simply the internal key P tweaked with the tweak point. To spend along the keypath, we tweak the private key in the same way.

In 2.2.1, we're demonstrating that we can sign a with a tweaked keypair. So we generate a private key, a public key, and then we have a random tweak that we're generating in this example. We establish the tweak as a private key, and then we lift it up to a point tweak\_point. So we have a tweak scalar and a tweak point. So this allows us to tweak the private key by adding in the tweak private key, and it allows us to tweak the public key by adding the tweak point to the public key. In the next example, we will solve for an alternative private key, because in 2.2.1 the hash is actually missing which makes it insecure. We're going to quickly go to example 2.2.3 because that's where we solve for an alternative private key.

We want to compute an alternative private key that together with a new tweak, can sign for the same taproot output point Q. So it's a linear equation, and we can solve for the new private key. This is an "attack", because nobody would use this as a commitment scheme. This shows that the linear relationship holds, and it doesn't work as a commitment scheme. Here, the tweaked pubkey for my  first private key is this, and my tweaked pubkey for my alternative private key, with my alternative tweak, is the same pubkey point. So that Q is the same for both equations. So we have two tweak and private key pairs. So this obviously doesn't work. So we need the hash expression.

I am going to jump to 2.2.2, where we're signing with a tweaked 2-of-2 musig keypair. I'd like you to try that. The trick here is to figure out when and where to tweak the keys. We have multiple partial signatures and multiple signers, so the question is who tweaks what during signing to produce a valid aggregated signature. So who needs to tweak the key? Do all the participants need to tweak the key?

The aggregate public key point is obviously the sum of all the individual public keys multiplied by the challenge factor. If we tweak the aggregate public key, what happens is that it's still the sum of all tweaked public keys plus the tweak point T. For private keys, the private keys are tweaked by the challenge factors and we simply add the scalar of the tweak. So only one of these participants needs to tweak their key. If everyone tweaked the key, we would have n-many t values. Instead of tweaking a single key pair, we could also tweak the signatures. In our example, we are going to do it with keypairs because it's a little easier. Sometimes it makes more sense to tweak the signature.

In our example, we tweak the aggregated public key. You could also derive a tweak point and add it to the aggregated pubkey, it would be the same. In this example, I chose private key 0 to be tweaked. You can see for yourself, that you can tweak any private key out of the 2 created, and it would create a valid signature for the tweaked musig aggregated key. If you want to, this is bonus, you can also try not tweaking the private key and instead tweaking the partial signature instead and that should result in a valid signature for the tweaked aggregated key. So they are equivalent.

Next we're going to look at the commitment scheme we use in taproot. We're going to motivate it, at least. We're going to tweak our public point with information committed to it. In section 2.2.3, we illustrate why we can't commit data by simplying tweaking the public key point with your commitment. It doesn't work. I won't go over that again. In section 2.2.4, we tweak with the hash of the internal key and the message. This is how you should commit data to a tweaked public key. In this example, we're actually hashing the pubkey first. We're also hashing the commitment, which is fine. So we take the pubkey, we hash it once, then we conccatenate the hash digest of the commitment and then we hash both again to obtain the tweak. We set the tweak as an EC private key, we derive the tweak point, and then we can directly tweak the private key and public key since they are also EC key classes, by adding them together. Then we can sign, with this keypair, and it will obviously be a valid signature. The only thing here that is different from what we did before is that we are committing data in a different way to the tweak.

Now we're going to spend a taproot output and spend along the keypath. So we are going to demonstrate that the default spending path of taproot still works, even with committed data. In exercise 2.2.5, I'd like you to generate a taproot public key that is tweaked by the following taptweak factor. In the second step, we're going to spend that. In these examples, we don't reveal the tweak. We just commit it and spend the output as if nothing happened, for the sake of demonstration.

It would be dangerous to tweak your internal key with a tweak you obtained from someone else which you didn't derive yourself. I can spend his tweaked public key, and I'm not going to reveal my private key. So the tweak can be a script including a private key from the attacker or whatever. This tweak could have script commitments inside which could be spendable by an attacker. Great point, yeah we should note that in the comments here. This is dangerous.

Once we have the address, we can send funds to the tweaked key. We're going to spend it along the keypath. So this has been done for you in the exercise. We generate a transaction template, in 2.2.5, and then in 2.2.6, we're going to spend the taproot output with a keypath. So again, this is very similar to the previous exercise in section 2.1, but with tweaked keypairs.

There's a bug, not sure if this is a version problem. Make sure that in the previous section... we're going to reuse taproot\_pubkey\_v1 which is the witness program, and this is used again in section 2.2.5, in the sighash digest.  Okay, in section 2.2.5, we use taproot\_pubkey\_v1. We match the script with our witness program. Make sure this is named the same as what we set earlier on; if you don't get an error you're probably fine, but if you do, that's probably why.

tx.sha256 is the txid. It's poorly named. This was added back before segwit when it was just sha256. It's just the txid in bytes. If you want to add text, then you can use hash. But it's sha256. So it's txid with no witness and no witness marker. How do I get the wtxid? You don't. Or you can't. Not in the test framework, at least.

If you get testmempoolaccept errors, you can try printing it out and sometimes it tells you a reasonable error message. It's all been straightforward so far, right? Any questions? It's 3pm, so let's start again in 15 minutes.

## Tapscript

Chapter 2.3 is about tapscript. So far we have looked at spending by using the keypath, but we haven't looked at committing a proper script to a segwit v1 output. Committing to a script allows us to run a script, and this in turn allows us to encode a wider range of different conditions to an output.

In general, tapscript is upgraded bitcoin script. It's bitcoin script, but optimized for Schnorr. It allows for verifying schnorr signatures, and it allows for future tapscript versions. Different tapscripts are committed in taptweaks, which is how we commit different spending paths. So we have talked about taproot pubkeys, tweaked internal keys so that we can tweak in arbitrary data without revealing the keys, and then we can also commit a tapscript and reveal it and spend along its path during spend time.

In terms of taproot vs legacy bitcoin script, the signature opcodes are performing verification of bip-schnorr signatures. For signature opcodes, we now verify against schnorr signatures. Multisig opcodes have been removed, and replaced by CHECKSIGADD opcodes. This enables batch verification. In order to perform batch verification, we need to have an argument for every pubkey in the output script. In threshold multisig, that was not the case.

Every tapleaf can have its own tapleaf version. Then there's upgradeable opcodes, reserved for future functionality.

I want to spend a couple minutes talking about CHECKSIGADD to make it more clear. On this slide, here is an output script which can only be spent if someone provides valid signatures for pubkeys 0, 1 and 2. Notice that we have a mixture of checksig opcodes and checksigadd opcodes. We also have a 3 encoded in the output script which is the number of valid signatures required. We start our initial stack with three signatures, then run through this script and see what happens. Notice that the signatures are in the reverse order of the order we have in the output script.

output script: pk0 checksig pk1 checksigadd pk2 checksigadd 3 equal

initial stack: sig0 sig1 sig2

CHECKSIGADD is a little confusing, because add means addition. But that's not what that means there.

So we push pk0 to the stack, then we run checksig. Assume sig0 is valid, so it pushes a 1 to the stack. This 1 is going to serve as a counter. So checksigadd will then push pk1 on to the stack, and then it will result in the counter being incremented by 1 if it's a valid signature. This continues until we reach the very end; if you have 3 valid signatures, the counter is incremented to 3, and that equals the threshold indicated by the output script, and therefore it verifies.

CHECKSIGADD is a combination of rotate, swap and CHECKSIG.

Q: Reading the BIP, rotate rotates 3 items on the stack, whereas roll does the whole stack.

A: Yeah, it does 3 because-- we have the counter, the pubkey and then the signature. Once I push the pubkey on top, we push the pubkey on the top of the stack, we care about the pubkey, the counter, and the signature.

Q: I just found it interesting that OP\_ROTATE rotates the top three items. Is it just an amazing coincidence that it works well here?

A: There is a paper that is really hard to google, which I have been told exists, but I haven't been able to find it, which describes a thing called Secure Forth which bitcoin script is extremely similar to, almost identical.

### Tapscript descriptors

Today we have descriptors in wallets today, which are a high-level language to describe an output. So here's some examples of pay-to-pubkey descriptors:

* ts(pk(key))
* ts(pkhash(key, digest))
* ts(pkolder(key, delay))
* ts(pkhasholder(key, digest, delay))

There's also equivalents for checksigadd scripts:

* ts(csa(k, keys...))
* ts(csahash(k, keys, digest))
* ts(csaolder(k, keys, delay))
* ts(csahasholder(k, keys, digest, delay, ...))

### Committing a single tapscript to a taptweak

We're going to have a taptweak t. So Q = P + tG. t is now a TaggedHash("TapTweak", P, tapleaf). TaggedHash is defined as H(H("tag") + H("tag") + data). The tapleaf itself is a Taggedhash("TapLeaf", ver, size, script).

This TaggedHash makes it domain specific, and it helps with collision resistance. You have 64 bytes of reusable midstate, which is helpful for implementation as well.

There's no merkle root here because this is a special case of a single script. We directly commit the tapleaf to the tweak. So if we had multiple scripts, this would be an internal node so to speak, the root. That's in the next chapter.

There's an internal version. We can keep the same output version, but internally increment versions. It would require a soft-fork. I believe the other ones are unencumbered. You can have different versions in each leaf. I think there's five different ways here, like OP\_SUCCESS. The proposal has 5-10 different ways to put soft-forks in. There's a lot of flexibility in there.

Q: Why is the current version c0?

A: It's to avoid ambiguity with opcodes. "Choosing a value with the top two bits set, and tapscript spends are identifiable even without access to the UTXO". What does that mean? I don't know. It's in the tapscript BIP as rationale 1. Just ask on #bitcoin-wizards. It might be a magic number that sipa made up. If you're a hardware wallet, you have to sign a particular script code. It's so that you don't have to look up the output script, basically. You don't know if it's p2sh or segwit output or something.

The script code under the signature hash... if you're a hardware wallet and it has been requested if you sign some transaction with a script code, you don't know if the script code corresponds to a witness script or a redeemScript in p2sh, or a scriptsig, and they all have consequences for the weight of the transaction you're signing, and therefore the fee rate. So I think this is about that. If you see a script code that starts with c0, then you know that this could only be tapscript, and you don't need to know the UTXO being spent or to see the transaction being spent or anything like that to verify that. I believe this is the first byte of the tapleaf. It simplifies analysis, and they can't occur in the first item of the final stack element in either p2sh or p2wsh. Basically, the idea is that, these are impossible to occur in current segwit, it would just be invalid. For p2wpkh, that would not be a valid pubkey. For p2wsh, that would not be a valid script length. By having that set, it's also easy to identify what kind of script you're dealing with, without needing to see the scriptpubkey. But this means that if you want to do an upgrade here, you have to think about this all over again. It may not be the case that 0xc1 is just as nice. This is like version 0 of tapscript, and the version number is always ANDed with the top two bits. So the top two bits are always set. It's tapscript, version 0. You can say it like that.

To spend along the single tapscript, we basically just need more witness elements. Before, we just had a single signature. In this case, we need to supply the witness elements that fulfill the locking conditions of the tapscript which can be any tapscript you're committing. Then we have to provide the tapscript itself, and finally the internal key which is a part of the witness element called the control block. The control block could also include other things like inclusion proofs, but in this case, we only have one tapscript and that's all we need to show.

<https://github.com/bitcoinops/taproot-workshop/blob/master/2.3-Tapscript.ipynb>

Q: How does the verifier know based on this witness, whether it's a key path spend or spend path. How does the verifier know given this as a witness, that this is not a keypath spend but a script path spend.

A: The key path spend has one element on the witness stack. The key path has only the signature, and this one would have multiple elements. If the size of the stack is more than one element, then it's not a key path.

The control block will include the internal key plus the inclusion proof. The entire merkle proof is just one stack item.

OP\_CHECKSIG and OP\_CHECKSIGVERIFY now verify Schnorr signatures. In 2.3.1, we're doing an example for pay-to-pubkey tapscript.  You can construct a pay-to-pubkey tapscript using TapLeaf.construct\_pk(ECPubKey). The sat method gives you the witness elements required to satisfy the tapscript. This is a helpful thing to have. So it's not "satoshis". No, no.

So we construct a TapLeaf() object. If you run the sat function, it will say the type is signature and then give you the signature to satisfy the tapscript.

Here's an overview of OP\_CHECKSIGADD. It's rotatte, swap, checksig and then add which increments the counter by one if the signature check passed. For batch verification, it's for a lot of stuff. It's for verifying all signatures in a transaction but also across multiple transactions, although I think the implementation right now only does a single transaction. You can also batch the tapscript commitment checks. We have a rule somewhere, I think it's consensus now, if that you have a CHECKSIG that fails, the signature must be an empty string. So if you give an invalid signature to a checksig, that aborts the script and the whole transaction is invalid. If it's not reached, that's found, then it just doesn't contribute to the batch validation. So the idea is that when you're validating a transaction, every time you hit a CHECKSIG, you take the signature in there, the signature verification equation that you would do, and you add that to a queue or some set of equations to check. In the meanwhile, you keep on moving and you assume it's valid at first. Then later, after you validate the whole transaction, assuming everything is valid, then you verify all the signatures at once. So in theory you could do this for the whole block, or you could batch verify across many blocks at the same time. If you do more than 100 signatures, then you start to get deminishing returns and it takes more memory. You can also batch verify the tapscript checks. Whenever you expose a tapscript root, there's an EC equation that the verifier has to check, and you can throw that into the batch as well, it's very similar to the signature verification operation. Specifically, the internal key tweak can also be applied into the verification. Anything that you multiply by the generator, you can put into the batch verification. Yes, I think you're right. So the tweak times the generator, that becomes pretty much free.

Q: If you have a signature verification which is ... you're supposed to include an empty string as the signature, and this is the only consensus rule change that is requested? Batch verification is not part of consensus.

A: Correct. That rule is already a standardness rule right now.

It's a malleability risk if you have an invalid signature and someone else can just malleate it and throw random bytes in there. It also forces you to do a signature check that is going to fail.

Back to CHECKSIGADD... we're going to create a 2-of-3 checksigadd output for tapscript. We generate three key pairs, we construct a TapLeaf() object, we construct a CHECKSIGADD tapscript using construct\_csa(2, [pubkey0, pubkey1, pubkey3]). So we get a tapscript with those pubkeys. They are in reverse order because they were pushed on to the stack.

There's also a convenience function TapScript.generate\_threshold\_csa. The thing about doing k-of-n CHECKSIGADD is that, you will always have unused pubkeys. If I do a 2-of-3, I provide an empty vector for the pubkey I don't provide a signature for, but I end up revealing the public key when I spend. Plus also we pay for that 0 byte. Instead, we can convert a k-of-n locking condition into a set of n-of-n CHECKSIGADD tapscripts. The advantage of this is that, we have multiple tapscripts, but in the spending of each of these, no unused pubkeys are revealed. From a privacy view, that's nice.

In example 2.2.3, we're going to try this. We're going to use generate\_threshold\_csa. This is going to generate a set of tapscripts that express a 2-of-3 multisig, but expressed as individual 2-of-2 checksigadd tapscripts. You can print out the tapscript descriptor with the ts.desc property.

Tapscript allows for future upgrades of individual tapscripts and specific opcodes. There's a leaf version, committed to a taptree leaf node, and the nthere's also success opcodes which allow for future functionality any of which end script evaluation successfully.

Some more tapscript descriptor examples: these are the descriptors for the different tapscripts, and then we have the witness elements you would need to spend them. These are for public key tapscripts. Here are the constructor methods.

Instead of pkhash, call it pk delay. Using pkolder in tapscript, we use OP\_CHECKSEQUENCEVERIFY and we can encode a delay in there as well. In our examples, we are using relative locktimes.

We have similar helper functions for CHECKSIGADD like TapLeaf.construct\_csa, TapLeaf.construct\_csahash, construct\_csaolder, construct\_csahasholder, etc. In section 2.3.5, we're going to generate a 2-of-2 csahasholder tapscript, and then we're going to spend it along the script path.

So we're using construct\_csahasholder helper, and we use a relative timelock delay. This is a tapscript descriptor, but what's more interesting is the... It has a hash preimage, and it pushes hte size of this preimage on the stack, it has to be 32 bytes, the reason why we constrained that is because say you have a hashlock and an atomic swap and one is on bitcoin and the other one is on another chain and the preimage is so large that-- why.. pushdata limit is 520 bytes. If the other chain has more than 520 bytes there, then I can't spend it on my chain. There may be other reasons we check for size. So in any case, we check for size.

In the next section, we're going to commit this tapscript into a taproot output. We're going to use tagged hashes computed into the tweak. The commitment hash in this case is defined as .. so this is the taptweak, it's a tagged hash with the tag TapTweak, and the internal data is the internal\_pubkey + the tapleaf. And the tapleaf is defined here, it's a tagged hash. Double hashing "TapLeaf" was introduced in bip-tapscript. So it's the tag digest twice, but it's to avoid the -- block inclusion proof thing. There's the merkle-damgard construction issue. It's not related to merkle-damgard. The double hashing is... the block size is 64 bytes, but the target itself isn't. It's to prevent ambiguity on different things we're signing on. Why do it twice-- it's for the 64 byte digest. Sorry, my mistake.

We're going to compute a taptweak from a tapscript. So here you are going to create a tapleaf and then a taptweak. So you compute a tapleaf, and then you commit that tapleaf to the taptweak. This is pretty straightforward. We generate our internal public key and our internal private key, this is the keypair we want to tweak later to obtain the taproot output. We're tweaking it with the taptweak, which is computed from the tapleaf. So to compute the tapleaf, we use a tagged hash defined in a certain way. The tapleaf has the tapscript, and the taptweak we compute with a tagged hash again, and the internal data is the internal pubkey plus the tapleaf. Once we have a taptweak, we can tweak our internal public key, and then we have a... encoded in the segwit v1 format.

If you run example 2.3.7, you can check whether your derivation was correct. In 2.3.7, we use the TapTree class which will construct it for you automatically. We will use TapTree automatically. Just as a test, you can verify that you did it correctly. So there's a key and a root applied there.

Next, we're going to spend this taproto output. To do this, you need the stack element(s) to satisfy the tapscript. For csahasholder, it requires preimages, hash, a delay. Then there's the tapscript, and the control block c. The controlblock c is a single stack element consisting of the tapscript version and the internal public key.

So in example 2.3.8, we're going to generate a segwit v1 output for spending along the single script path. We will reuse the previously generated segwit v1 witness program which has the csahasholder tapscrpit committed to it, and encode it into a bech32 address. We are going to encode it as a segwit address so that we can send funds to it with a Bitcoin Core wallet.

In example 2.3.9, I setup my test wrapper. In 2.3.10, I generate the balance for my wallet. In 2.3.11, we are going to spend funds to the segwit v1 address. In 2.3.13, I'd like you to construct a transaction which spends this output along the script path. Once you're done with 2.3.12, feel free to do 2.3.14 and then we'll talk about it together. When you're done, feel free to finish all the way up to section 2.3.15 and finish the transaction.

For 2.3.12, let me point out a few hints that might be helpful. Since we have a tapscript with a delay, make sure you set the transaction version to 2. When you construct your txin outpoint, make sure you set the nSequence value here. I'll let you figure out what the value is going to be; you need to encode a certain value in nSequence and it will not be the default nSequence value.


For 2.3.12, it's pretty straightforward. The nversion is set to 2 because we want to use the nSequence field as a delay encoding, so we can no longer use version 1. We set the CTxIn, make sure the nSequence is set to the delay. That's the field that is checked when the output script is run. Then you have a spending transaction that could be signed.

Signing the transaction requires TaprootSignatureHash again, no surprises here. This is a checksigadd output and not a musig public key output we're spending, so no key aggregation. We jus thave two signatures here, explicitly given. Next, we need to populate the witness stack. Previously we were just appending the signature. But now we need some more: we need the signature1, signature0, the tapscript, then the internal key together with the leaf version which is the control map object here. To satisfy this, we need two signatures and a preimage, but we need a little more because the preimage and the two signatures are only the stack elements satisfying the tapscript. In addition, we need to provide the tapscript itself, and the control block. In our case, the control block is just the tapscript version and a public key. Then the witness stack has the preimage, signatures, the tapscript, and the control map for the tapscript. This is now a valid witness that spends along the single script path that we have for this exmaple.

We want to test that this timelock works. If we broadcast the transaction without any delay, without mining any blocks, then it will fail. So we call generate(delay) to generate enough blocks, the exact number of blocks, that we have chosen for the delay value. Once that has been done, we can use testmempoolaccept and this time it should pass in contrast to the output of testmempoolaccept before the delay expired.

## Taptree

You might want to use multiple tapscripts, and we do that with a binary tree structure called taptree. We use a binary merkle tree construction, but this tree doesn't have to be balanced. This allows for certain cost optimizations. If your tapleaf is closer to the root, then your inclusion proof will be cheaper on-chain. Now we're going to be committing a taptree into that tweak.

There is no ambiguity as to whether a node is a leaf or an internal node. There is also no ambiguity about the order of the children when computing the parent. So the siblings are ordered lexigoraphically. The internal nodes are tagged "TapBranch". The leaf nodes are tagged "TapLeaf". Tapscripts are committed to leaf nodes.

Finally, we can talk about taproot descriptors. We talked about tapscript descriptors, but how do I describe an entire output? We propose a tp tag, like tp(internal key P, and the taptree descriptor). The taptree descriptor captures the different tapscripts they are committing as well as their structure in the binary tree. The tapscript descriptor is simply nested tapscript descriptors. Every node is described by its children, so we have these touples. A tapbranch will have a left child and a right child. We can also nest the tapbranch-- so it can be [tapscript0, [tapscript1, tapscript2]].  So tapbranches are composable.

Finally, we come to the point where we want to spend a specific tapscript. In this case, we have the following taproot output, we have four scripts committed to a single output, and we want to spend script A. So the first elements are... the elements that satisfy script A, and then we have the script A itself, and then the control block. Previously we just had the internal key in the control block. It's still here, but in addition to that, there's an inclusion proof to prove that it is included in the taptree construction, which is always a 32 byte multiple.

Can you have specify a hash for an internal node such that it is also tweaked? It might be useful, that some wallet inputs an output script descriptor where some of the conditions aren't known to the wallet. Good point, you could I think. So let's say I have a single tapscript committed, at depth 2, and I provide the first digest here, and the second digest there. So these aren't a tapleaf, they are just hashes. In the descriptor, it's a tapscript. It could be a hash, sure.

In section 2.4.1, we're going to construct a taptree, and then in part 2 we're going to spend it. In section 2.4.1, the idea is to compute a taptweak from a series of tapscripts. We have three pubkey tapscripts, and please construct the taptree according to this graphic. So we make some taggedhash leafs, and then we have the first internal node which is internal\_nodeAB which is a tapbranch(taggedhash\_leafA, taggedhash\_leafB).  Then the next branch is tapbranch(internal\_nodeAB, taggedhash\_leafC). Then we compute a taggedhash with "TapTweak" as the tag, and then we use the internal pubkey and we append the root of our tree. That's our taptweak. Then we derive our segwit address. So then we compute the witness program, which starts with a 0 or 1. The segwit address is constructed by calling program\_to\_witness.

In 2.4.2, we have a few convenience methods on the TapTree class object which you need to populate with some values. We have the taptree root, we have nodes which are internal nodes, and we have constructor models for these. When you call Taptree.construct, it will return the segwit v1 script, the tweak (taking the internal key and tweaking it with the tweak), and then the control map which is the control block pairs for spending along the script path.

We talked about taproot descriptors. Now we're going to see how we can construct a taptree from a descriptor. A descriptor encodes all of the information required to reconstruct the taproot output.  There's a function from\_desc which parses a descriptor and creates a TapTree. The nesting of the tapscripts implies the structure.

One side note here is that, instead of manually constructing the tree along its structure, we can do the following instead. In example 2.4.4, we're going to build a TapTree with a huffman constructor which uses a greedy algorithm. The way it works is as follows. This is a method you can call on the taptree class. Once you set the internal key, you can call the huffman constructor which takes a list of tuples as arguments. The tuples are always a weight and a tapscript. The weight indicates a higher probability of this tapleaf being executed. So the algorithm takes the leafs, and as it hashes its way up, it will always try to include the lower probability of execution first, meaning it will be at lower levels in the tree. Lexographical ordering does apply. So it's only lexographical within a branch. It's a tie breaker. You compute a branch from its children. Once we do that, we can call the construct method and we get the tweak, and the version 1 script that we can send funds to.

The control block now includes not just the internal key but also the inclusion proof. You can get the control block map by calling TapTree.construct() and get it from there.

In section 2.4.5, we're going to construct a taproot output from a taptree. We're using four pubkeys. You can weight them however you like, and once you finish the exercise, I'd like you to change the weights and observe how-- when you change that, the weight of the tree changes. For now, though, just construct the taproot output. Use the huffman constructor to construct the taptree. Don't forget to set the public key in your taptree object. There's a taptree.key value, which needs to be set to the internal pubkey. Otherwise it's not going to get constructed properly.

In section 2.4.7, I'd like you to sign for tapscript A. So the scriptpath needs to be indicated at True, and in tapscript you need to provide the actual tapscript value so tapscriptA.script needs to be provided. Once you create the signature, feel free to construct the witness and test for mempool acceptance. The witness stack will be the individual elements that fulfill the tapscript, then the tapscript, and then the control block which is one stack element but it consists of the tapleaf version, internal key and the inclusion proof.

Q: The transaction digest doesn't include the inclusion proof, right? So any valid inclusion proof is fine, and it doesn't matter which one happens to get used if there's multiple possible inclusion proofs.

A: The digest knows the spend type, but it doesn't know about the inclusion proof specifically. That's right.

If you have two identical tapleafs, can you malleate it by changing the path-- because the signature is still valid. This is malleability. Imagine a different tapleaf, with a different script. It's a different node in the tree. You can malleate, but you need to be able to reconstruct the tapleafs from the bottom. So say I have two identical tapleafs, and he creates a spending transaction with an inclusion proof for the firs tonce. He malleates it, and the inclusion proof is now the one for the second one. Yes, but only you the sender can change it, so that's the same as malleating your signature today, so we don't care. The sender can always malleate. So this is based on only the sender knowing the full tree. This might not hold for-- it's not published in the transaction. If it's a multi-party contract, then it could be malleated. But that's only if you're dumb enough to include the same tapleaf twice. You generally wouldn't include the same tapleaf twice. But this could be related to the hidden spending paths not known to one party; there might be an identical leaf under the the other leaf. So you shouldn't sign for any taproot output where you don't know all the tapleafs. That's bad. It's interesting, that's not obvious at all-- well, you don't know if someone can just spend on their own, so you always always need to know all the tapleafs and it should be obvious.

Q: In the witness, how does the control block get consumed?

## Degrading multisig output

We're running out of time, so let's just look at this and discuss it. This is a hypothetical scenario we're describing.  Consider we have two types of keys here, we have 3 main wallet keys, and then we have 3-of-3 multisig, and then we have two backup keys. The main wallet keys can sign interactively. The backup keys cannot sign interactively. So we want to construct a degrading multisig. As you see here, there are two delays. The first delay is 3 days, and then the next spending path becomes available after 10 days. As we go down, more backup keys are required.  We can describe this as a set of tapscripts. Given the tapscript descriptors that we have talked about today, which ones capture these locking conditions and in what order of probability would you weight those? This exercise is about when to use musig keys, and when to have individual keys that can spend with CHECKSIGADD opcodes. When I need to sign with wallet keys, I can use the musig pubkey. So 3-of-3 multisig could be an internal key tapscript. The one backup key after 3 days- would this be a single leaf? Also, we odn't want to reveal any unused public keys. So instead of a single leaf, you use multiple leaves. I think it's 5 choose 3. We need 1 backup key, and the 1 backup key has 3 conditions, because there's 3 possibly missing people. For the second degradation after 10 days, we now require both backup keys. So there are 3 permutations here, right.
