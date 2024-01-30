---
title: "FROST Panel"
transcript_by: zachbitcoin via review.btctranscripts.com
media: https://www.youtube.com/watch?v=8nuFt-1SWRI
tags: ["frost","hardware-wallet","multisignature","lightning"]
speakers: ["Jesse Posner","Rijndael","Vivek","NVK"]
categories: ["Podcast"]
date: 2023-06-01
---

**## Intro Music to Podcast**

Everything else versus Bitcoin essentially gets spent and dies.

I want to be able to have reactive security and I think OpVault is today the most straightforward, easiest to use way to do that.
I will not be insulted by a clockmaker.

Overall these kind of ways to make the network easier to both build on and interact with, I think is a really big deal.

If Bitcoin existed when we started Twitter, We would not have to go down the ad model path.
I mean, as simple as that.
Integrating Lightning into a social network is the killer app.

**## End of Intro Music to Podcast**

**## Intro**

NVK: 

Hello and welcome to the Bitcoin.Review podcast, where we explore developments and projects with the people who actually make them happen.
The show is supported by Pod 2.0, SatStreaming and CoinKite.
If you're a new listener, I'm NVK.
I run CoinKite, where we've been helping people secure their Bitcoins for over a decade.
We make the cold card and fun products like the Block Clock.
You can find more information about it on CoinKite.com.
Today we're going to be talking about frost and maybe we get even into roast.
And that is not a dish.

**## Guest introductions**

So with that, why don't I welcome our guests, Mr. Jesse Posner.

Jesse Posner: 00:01:21

Hi everyone, I'm happy to be here.
I'm working on an open source Frost implementation.
So very excited to talk about Frost.

NVK: 00:01:31

Very cool.
Mr. Rindell.

Rijndael: 00:01:34

Hello.

NVK: 00:01:35

Welcome back.

Rijndael: 00:01:36

Thanks.
Great to be here.

NVK: 00:01:38

Seared Salmon.

Vivek: 00:01:40

Hello.
The angry translator is back.
I will hope to distill this wisdom that Jesse bestows upon us.

**## What is FROST?**

NVK: 00:01:50

All right, guys.
So why don't we sort of start from the very beginning here.
What is frost?
Is it frozen?

Jesse Posner: 00:02:04

It's, it's, well, it's cold.
But not necessarily frozen.
Yeah, so Frost, I think the best way to explain Frost is first to kind of take a step back and think about how we typically set up multi-sig in Bitcoin, which is that we use scripts.
So you can use a Bitcoin script to define a set of public keys and a threshold.
And then if you want to spend that Bitcoin, there needs to be a production of signatures that matches the threshold and the public keys that is specified in the script.
And so that's how we get these great multi-sig configurations for secure Bitcoin storage.
But there's a few disadvantages to doing it this more traditional way.
One is there's a privacy loss.
So when you go to spend the Bitcoin, you have to reveal the script and then that reveals the public keys that were involved in the threshold.
And if you're using a very idiosyncratic setup, that might actually identify who you are.
If you're one of the only people that does a 25 of 108 or something, maybe, you know, that, that creates a signature where people can identify what you're up to.
At the very least, it reveals information about your setup that you probably don't want the whole world to know about.
So there's this privacy leak.
And the other potential issue is we can have some really big scripts with multi-sig because we have to list all the public keys explicitly.
So Frost is a way of getting these same benefits of multi-sig, except when we look at the blockchain, we only see one public key and one signature.
And it just looks like a key spend path for a taproot spend.
And so you can't tell that there were multiple keys involved.
You don't know anything about the threshold and we get this nice constant space Scaling efficiency where no matter how complex the multi-sig setup is the amount of space That the redemption script takes on the chain is always the same.

NVK: 00:04:24

Would you say that Frost is essentially single sig right as far as Bitcoin cares, right?
It's Bitcoin single SIG.
And what are you doing there is some magical, fancy, Shamir secret sharing of that original single key, right?
In a way that nobody really has that single key.
And then you just magically get everybody to sign in whatever M of N, which is really threshold, but let's just keep it simple.
You find quorum, right, of those shards.
And then once you have quorum of that, then you compose a Bitcoin single signature with that key.
Right.
And now you have your Bitcoin.
Is that correct?

Jesse Posner: 00:05:12

Yeah.
Yeah.
So you could kind of think of it as single sig from an on-chain perspective.
But there's multiple signatures that are taking place off-chain that then are constructing the single signature that you see on-chain.
And Shamir's secret sharing is definitely a good point of reference here because not only is Frost an improvement over Multi-sig in terms of Bitcoin script, although there are some trade-offs.
It's not simply superior because with Frost There's an interactive setup process that you need to do to create the key, whereas with the script-based method you don't have that.
But going back to Shamir's secret sharing, it's a useful point of comparison.
So typically, the way Shamir works is you have a secret, a private key, you split it into pieces, and then when you want to sign, you've got to bring these pieces back together to reconstruct the key.
And the generation and the reconstruction are two vulnerable points in the process because that is where a single key is constructed all by itself.
So you need like a very secure trusted process to do that without leaking the secret.
With Frost, we can generate Shamir shares without ever having to have a single secret that is split.
So we have the shares, but we don't have the single secret, and then we can sign for this key without bringing the shares back together.

Vivek: 00:06:43

This is what's known as the polynomial interpolation, correct?

Jesse Posner: 00:06:48

Well, so for Shamir secret sharing, the reconstruction is polynomial interpolation.
So the idea behind Shamir is, if you have two points, those two points uniquely define one line.
And if you have three points, those three points uniquely define a parabola.
And in general, any n points uniquely defines an n minus one degree polynomial.
So if you want to create a Schmier secret sharing shares, you have your secret, which is a private key, and then you create a polynomial with a degree that's equal to the threshold that is required to reconstruct.
Then you set your secret as the coefficient of the first polynomial term, and then you create random coefficients for the other terms.
Then what you do is you derive points that fit the polynomial.
So you plug in x equals one, you get a y value.
You plug in x equals two, you get a y value.
And each one of these xy coordinate pairs is a Schemere share.
So when you distribute Schemere shares, they're xy coordinate pairs that were derived from some polynomial.
And then once you have, when you want to reconstruct, you get the necessary number of shares.
So let's say we're doing a 2 of 3, we need two points to define the line.
So once I know the two points, I can interpolate the line that crosses the two points, I can reconstruct the original polynomial and then I can derive the secret by taking that first coefficient.

Vivek: 00:08:29

That sounds like moon math as Lloyd Hensley said.

NVK: 00:08:34

Yeah I mean that is definitely getting a little bit too much into the weeds there.
But, you know, I guess the important part here is that the magic of Frost is because you're doing that, you can now just share a nonce, right?
So that you don't have to do all this computation interactively between all the parties.

Rijndael: 00:08:54

I think like in the past, if you wanted to have some kind of threshold scheme to protect your Bitcoin, you had kind of two choices.
You could either have single SIG and you would shimmy or split it, but then you still have to get all of the pieces back together on one device.
And in that one device, if there's malware on it, if somebody kicks in your door, like whatever, like you have a single device with one key on it that can spend all of your money.
Or you would go with script-based multi-sig, where you can go and do partial signatures at different places and then combine them together, but it's a lot bigger on chain, it's more expensive, it leaks some privacy information.
Frost is kind of the best of both worlds.
You can split up your key into multiple places and then go and do partial signatures with each of those individual shares and then combine them together.
And from Bitcoin's perspective, it's still a single signature, but you have like there's not one place where you have a key that gets reconstructed.

## FROST methods for key generation and secret sharing

Vivek: 00:09:54

Could we touch on, I guess, maybe the different methods or functions for this scheme versus, like, the traditional ECDSA where we generate, assign, and verify.
Like how does it get a bit more complex with the Shamir secrets and the non-commitments and things like that?

Jesse Posner: 00:10:15

Yeah.
So basically, when you have just like a standard, let's say, ECDSA or Schnorr signature, you generate a public-private key pair and then you've got a sign algorithm and a verification algorithm.
And it's pretty simple from an API perspective.
Once we move into Frostland, things get more complex.
So the first thing is we need to think about three distinct phases or processes.
One is the key generation process itself.
So if we're looking at standard signatures, you just take a private key, a scalar that's in the setP group, and you take the generator and you raise it to the power of that scaler, and that's your public key.
Now, with Frost, we have to do something called distributed key generation, because we want to build the key in a distributed way, where multiple entities are contributing to the entropy of the key without any one of those entities knowing what the actual key is.
So that's DKG and that's like a three-round protocol to do the DKG that's interactive.
And so what happens is each participant generates a Shamir polynomial and derives shares for each other participant.
And then each participant takes the shares they've received and aggregated them.
And what ends up happening is the aggregated shares are shares of the aggregated polynomials.
Nobody knows the aggregated polynomials.
Each participant only knows their own polynomial.
And there's also some additional processes called VSS, where this is a more secure way of doing Shamir secret sharing, verifiable secret sharing, where you also distribute a commitment to your polynomial.
So each participant can verify that the structure of the polynomial is what they expect.
And then you also have to provide a proof of knowledge for the first coefficient term to prevent a row key attack.
And you also need to provide a signature at the end, signing a hash of all the commitments to fulfill a broadcast channel requirement that each participant saw the same commitments as everybody else.
So that's the first part is the DKG.
And at the end of that, each participant has a Shamir share of a private key of which nobody knows the private key.
And everybody has been able to derive the public key.
So you have a public key and Shamir shares of a private key at the end of the DKG?

Rijndael: 00:13:04

Yeah.
I think a reasonable mental model for this is if you think of Shamir secret sharing as like you go and you generate a secret and this could be like a Bitcoin private key or it could be a Nostra key or something else.
And then you split it into pieces and you distribute those pieces and then you delete the original.
That's the way that you would like shard out your private key with like Shamir secret sharing.
The DKG that we do in frost is kind of that, but upside down.
So instead of starting with a shared key and then splitting it, you have your different participants and these could be different people, they could be different signing devices, they could be different machines, they could be whatever.
Your different participants each generate a share and then you have a way for them to combine the shares together to basically create a shared secret that nobody has at any point in time.
And then the last thing that Jesse was touching on is there's all kinds of attacks that you can do where if you can sort of reactively choose your shares based on what other people's shares are, then you might be able to cancel out certain terms or you might be able to cause like denial of service or cause like other problems later on when those keys get used.
So there's some additional like, we're going to say nonce commitment a lot during this episode.
But there's a bunch of points during key generation and during signatures where before you reveal a value, you send over a hash of it so that people can tell that you didn't change your mind later when you saw their values.
So there's a couple of moving parts there as well.

NVK: 00:14:39

So that's a nice sort of like a deeper dive into how it works.


**## FROST use cases**

I guess let's explore some use cases here because that might help people sort of start to understand, like, what is the value of all this?
Because, you know, why not multisig, right?
And I mean, multisig in practice is an absolute clusterfuck.
It's horrible.
It's like horrific, right?
It's so bad that most people still advise people to just go single sig with passphrase, right?
Because in multisig, you're essentially committing to the M of N right from the beginning, right?
And it's very strict, right?
Like in very plain terms.
I mean, you know, if you set something to be two of three, it is two of three forever, right?
And there is no half of something.
There's nothing.
It's just two of three.
It is on chain, right?
So that means that everybody can see, once you sign a single transaction, they can see it.
It's so bad that I can't remember which exchange was, but somebody did a timing attack or just timing analysis on, it might have been BitMEX or something like that, where they essentially figure out where each of the executives were, and which of them signed the big balance of some cold storage.
It might not have been BitMEX, so don't associate that name with it.
I can't really remember which one it was, but it was a big one.

Vivek: 00:16:10

They do have like a 3 in 6 threshold payout wallet or something, right?

NVK: 00:16:15

I can't remember.
Well, I

Rijndael: 00:16:17

mean, yeah, so it's like the first benefit that a lot of people see with things like Frost or Music, which is related, but Music is, you know, N of N and Frost is threshold.
So it's, you know, T of N.
The first benefit that a lot of people see is, again, on-chain, it just looks like a single SIG.
And so if we move into this world where people might have tap scripts that they don't reveal and they're able to make payments through the key path, and you can do that either as a single sig or as a threshold signature, then it really helps with privacy and fungibility because nobody can tell if that one key that you're using or 50 keys or 100 keys, it's all just a single signature.
That also makes things cheaper.
You're not paying for all of these other public keys on chain.
I think those are really cool benefits.
But for me, the crazy superpower that Frost has is, you know, earlier when Jesse was describing, say that you have a two of three, the mental model here is imagine the private key is like at the Y intercept of some graph, and then you draw a line through that, and you pick, you know, three points on that line, and any two of them can reconstruct the line and get you back to your private key.
What's cool is if you have two of those points, you can pick a third point.
So you can effectively generate new keys without actually or new key shares without actually changing the private key.
So imagine if you have a multi-sig, like you have a 2 of 3 or a 3 of 5 or a 11 of 15 or something And you lose one of your signers.
Right now, what you basically have to do is either just live with it or you have to do like a wallet sweep and move all of your funds to a new wallet with a new set of signers.

NVK: 00:18:13

What everybody does is move.
Yeah.
You know, And every time you

NVK: 00:18:19

have a new executive, you

NVK: 00:18:19

have to do that again.
And the issue with that is these are each actual Bitcoin keys.
So you have to go through the trouble of creating backups of each, burying them wherever you bury them, traveling around, it's an absolute cluster.
And there is no good secure way of creating a Bitcoin multi-sig quorum either.
So there is no trusted way for you to communicate with each other to create that script either, even with BSMS, BIP 329.
Is it 329?
I can't remember now.
But regardless, there is no good way of doing that.
And I think Frost really addresses most of all hanging fruit, low hanging fruit that does this and adds more.

Rijndael: 00:19:07

Yeah, like there's definitely more complexity, but being able to say, hey, I want to add new keys or remove old keys without actually needing an on-chain transaction, without perturbing all of your UTXOs is just a wild capability that I think we haven't really seen in Bitcoin.
And it opens a lot of doors for key management, especially if you have, if some of your signers are like really hard to get to, or if they're really locked down and you don't wanna go and touch them every time you have to add or remove a key, it's a pretty crazy superpower.

NVK: 00:19:43

Yeah, I think, I mean, I don't know, I was sort of like thinking about the complexities, like of just in practice of doing Frost and because you kind of solved most of the interactivity issues with pre-generated nonces, it is not hard to share with each other some nonsense and store them on harder wallets.
That should be fairly straightforward.
And especially I think if somebody's going through the trouble of creating a proper Frost wallet with important signers and real money, I mean, you can pre-generate, I don't know, like a thousand of them.
I don't know, maybe a thousand might be much, but you know, and you store them And now you're good to go.
What's too unclear to me, and we'll get to ROSE later, is like when you unroll, like when you take somebody out of the, you essentially like kill one of the shares, if the analysis are still valid or not, I haven't looked into that.
But regardless, I think that that's been greatly, because originally with MoSig, when I saw that I said like, okay, well, this is cute.
I see cryptographers are having a lot of fun with this, but there's absolutely no fucking way you can do this in the wild, because unless you're using HSM servers, it's kind of pointless because like, if you're gonna keep wallets hot in order to do all this back and forth and it compounds too, right?
So as you're doing all this essentially almost like multi-party computation here, You know, it's kind of loses the point.
And then again, like the frost came in.
I'm like, oh, fuck.
Yeah, this is usable.
So Jesse.

**## Nonces**

Jesse Posner: 00:21:22

Yeah.
So let's let's let's chat about nonce.
So the thing is, so what we do like ECDSA and Schnorr, we have the luxury of being able to use a deterministic nonce.
The main issue with nonces is if you reuse a nonce across two different signatures, the private key can be trivially computed.
So, you know, it's the worst case scenario, you do not want to reuse nonces under any circumstances.
So with a typical signing algorithm like ECBSA, we can just take the private key and the message and hash it and use that as the nonce.
And that way, if the message changes, the knots will change.
And you've got a pretty good guarantee you're never going to reuse the knots.
Once you get into Music and Frost, we can't do that anymore.

Vivek: 00:22:11

And

Jesse Posner: 00:22:11

in fact, it can be quite dangerous to generate your knots deterministically in these multi-party protocols, because if a malicious participant causes the generation to restart, all the participants are going to generate the same nonce, but the aggregate nonce will change.
And so you can actually induce nonce reuse because of deterministic nonces once you move into this multi-party setting.

NVK: 00:22:36

Well just before we move on, what's the issue, I don't think people know, but what's the issue of reusing a nonce?

Jesse Posner: 00:22:44

Yeah, so Let's say, I mean this is very algebraic, like the outcome is the private key is leaked.
Why?

NVK: 00:22:51

Exactly, money gone.

Rijndael: 00:22:53

How did Schnorr make it easier?

Vivek: 00:22:54

Yeah.

Jesse Posner: 00:22:56

I mean it's a problem for both ECSA and Schnorr, but it's easier to explain with Schnorr because the equation for Schnorr is so simple.
It's s equals r plus cx.
So if you have two signatures s1 and s2 with c1 and c2, so you've got s1 equals r plus c1x and you've got s2 equals R plus C2X.
When you minus S1 minus S2 and divide C1 minus C2, that equals X, your private key.
So anybody just looking at the blockchain or looking at the two signatures, Signatures are public data.
If you just take these two signatures, subtract them, subtract the challenge hashes, which are also public data, and you can get the private key.
And this has happened in the wild.
One of the most notable cases is the PlayStation 3 firmware.
They reuse the same nonce when they're updating their firmware, they leak their private key, and now you can jailbreak your PS3 and do whatever you want with it.

Vivek: 00:23:57

Run a full node.

NVK: 00:23:58

Yeah, exactly.

Jesse Posner: 00:24:02

So the nonces have to be dealt with very, very carefully.
And so when we use either Frost or Music, we have an option, which is we can pre-generate nonces in advance to bring the signing down to a single round.
Or we can do a nonce generation protocol for each signing round, which adds additional communication rounds.
And so, but there is a risk to pre generating the nonces because let's say you pre generate, you know, a thousand nonces.
You have to think about the attack vectors that could trick a device into...
Did

NVK: 00:24:42

we lose Jesse?
This was an important part guys.
This was a really important part.
Jesse, you might want to repeat this part it kind of matters

Rijndael: 00:24:54

jesse's like whatever you don't do don't do and then

NVK: 00:24:57

don't do it like it just freezes this is beautiful

Rijndael: 00:25:03

the nsa cut the wire it's amazing

NVK: 00:25:07

That's right.
This was the attack vector.
And now everything's fine.

Vivek: 00:25:12

We never received the nonce.

Rijndael: 00:25:14

Always players here.
Yeah.
Jesse, somebody is going to come back with a Jesse mascot and say, guys, just use deterministic nonsense when you're…

NVK: 00:25:21

That's right! I mean, do we trust that Jesse is Jesse when he comes back?

NVK: 00:25:29

Yeah.

NVK: 00:25:31

I mean, it's gonna be hard to follow up here, I mean, I'm not qualified to replace Jesse on the rest of this explanation.

**## FROST + Nostr**

Vivek: 00:25:39

Yeah, I mean, so the main thing is I wanted to continue down the line of the different functions now associated with Frost.
And also maybe if you guys could touch on the schemes, right?
There's an accountability scheme versus a privacy scheme, and that's protection from, I guess, the public versus the other signers, and then eventually what led to the TAP scheme.
I don't know how much Rendell is in the know with that stuff either.

Rijndael: 00:26:08

I don't know what the TAP scheme is, but I'm very familiar with the accountability issue because me and Nick Farrow were talking about the ship host now that I want to do on Noster.
Using Frost.

Vivek: 00:26:21

Yeah, we can take a quick usability tangent or a use case tangent.

Rijndael: 00:26:27

Yeah, I mean, so like one of the other things that's really cool about Frost is Noster uses Schnorr signatures, right?
So all of the cool things that we've been talking about being able to do with signature aggregation with Schnorr, you can actually use in Noster.
So Nick Farrow, who is UTXO club on Twitter.
I think I'm the North America branch of the Nick Farrow fan club.
He made a tool called Froster.
Is that what it's called?
Yeah, Froster.

NVK: 00:26:58

Oh, God.
That's a little too close to frother.

Rijndael: 00:27:01

Yeah, right.
And it's...

Vivek: 00:27:03

I don't know.
It lets you

Rijndael: 00:27:05

do Nostra posts with Frost keys.
So you can, you can actually do threshold signing for Noster.

**## Nonces (cont)**

I think Jesse's coming back.
Jesse?

NVK: 00:27:20

Well, we better see a new nonce use when he comes back.

Jesse Posner: 00:27:26

Hi.

NVK: 00:27:28

Okay, can we have proof that it's actually you and you're not going to give us a different answer now that you've been compromised by the NSA?

Jesse Posner: 00:27:37

We haven't done a key exchange protocol in advance, so I don't think there's any way for us to have cryptographic certainty.
But...

NVK: 00:27:48

Okay, we're going to have to just roll with it.

Rijndael: 00:27:52

All right, person who claims to be Jesse, you were in the middle of saying,

Vivek: 00:27:56

you know, we're not doing this.

NVK: 00:28:00

The line was, you have to think about the attack vectors that could.

Jesse Posner: 00:28:05

Right, so if you take away one thing from this whole conversation, blink.
Yeah, so what I was saying is that The devices could be tricked into reusing a nonce.
Let's say you load a thousand pre-generated nonces onto a hardware wallet.
How does the hardware wallet keep track of the nonces that it's already used?
It could try to delete nonces that's already used.
It could have a counter.
It's not impossible, but that is where the, that's where you have to put some attention into to making sure there's no way, like with a fault injection.

**## Implications for signing devices
**

NVK: 00:28:44

I have a couple ideas.

Jesse Posner: 00:28:45

Yeah, please.

NVK: 00:28:46

So we started doing this thing where every single export that Coldcard does has a detached signature.
So essentially you can actually verify that the owner of that private key essentially gave out this actual PSBT for you to sign, or cosign, or the address explorer.
So essentially, the addresses that it's providing are the actual addresses that were provided, so the computer didn't cheat it.
So you could use detached signatures in a way.
It's not foolproof, because, yeah, I mean, I guess it is.
Because the issue here is, if you have access to the private key, then you have access to the private key, so you don't really care.
So yeah, I mean, that could help.
Another thing that we could maybe do is we could have a whole DFE sort of, kind of like a handshake between all the wallets that are part of the quorum.
So that every time you send, this is part of actually, I'd love to add this to PSBT v2, which is maybe there is a signature to the actual PSBT.
And you can start building a little bit of more trusted comms, right, between the things.
So it's a lot harder for you to cheat with the messaging transit or this sort of partially signed or unsigned bits that you have to have in and out of the wallets, as long as it's not interactive again, because to me, the best, like the ultimate benefit you get in terms of like, free security is just not attaching things to anything.
Right, like It's amazing.
You could have an encrypted piece of data on your desk, right, if it's not connected to anything.
It's better than any kind of encryption that ever existed, right?
So if we start connecting wallets together, we kind of lose all the beautiful benefit of being air gap.
So I just keep on thinking like, how can we maybe find other ways of signing things?
And we've been sort of breaking our head.
And one is detached signatures.
The other thing is we can maybe start signing.
So detached signature plus another signature that's done with a secret that's part of the hardware, not part of the key that is holding.
And it wouldn't be a key that you can easily change or anything like that, right?
Like It's like a key that's part of the secure element or something like that.
So you'd have to break both in order to, for example, fake that nonce or tell it to use a...

Rijndael: 00:31:24

It's like some device key or something that comes from some PUF in the device.
And it's not actually your Bitcoin key.
It's like a device export like authenticity check or something.

NVK: 00:31:38

Yeah.
I mean, listen, I didn't want to take too much in a tangent of the hardware deep hole, but.

Jesse Posner: 00:31:43

Yeah.
Well, there's a couple of important nuances here.
So first of all, imagine if you have disjoint sets of signers.
Let's say you have three or six.
So you have three signers that may not know that this other set of three signers use the same knots.
It's actually not as much of an issue in frost compared to the older threshold schemes because in frost each set of each subset of signers has a completely different knots.
Whereas in some of the very similar protocols that were precursor to Frost, all the signers would actually get to the same, each subset of signer could create the same NOX.
So that's less of an issue, but it's something you have to think about is not all the signers are going to have the same view of what we place.

NVK: 00:32:35

But with Frost that wouldn't be an issue.

Jesse Posner: 00:32:37

Right, so with Frost that's actually not an issue.
The other thing though to consider is there is already some interactivity to get the signature from the device to the coordinator that's going to aggregate the signatures.

NVK: 00:32:54

Yeah but that could be done with SneakerNet right?
So you're not as concerned.

Jesse Posner: 00:32:59

But If you can do that through SneakerNet, you could also do an additional nonce round through SneakerNet.
So it's a trade-off of saying, okay, maybe we add an additional round.
We already have one round, maybe two rounds is fine.
Or we really think through securing the pre-generated nonces and then having a system to re-up the nonces when they run out.

NVK: 00:33:23

Yeah, so I'll just weigh in here a little bit because we've been thinking about this a little, like actual sort of like implementation.
And I think you kind of end up in the same place because if you're protecting the private key, and you lose that, you're kind of screwed anyways.
So if you can protect the private key, you can protect the nonsense, right?
Because it's going to be essentially benefiting from the same level of protection.
So that's one thing.
The other thing that I've learned through these years now is that most of the people who are air gapping their devices, wised it up.
And they don't have the device in the same place as the coordinator or in the same place of really anything.
So say, for example, a guy will have his hardware wallet sitting in some safe deposit box in Monaco or something, right?
So he'll fly from Miami to Monaco.
He'll go inside his safe deposit box without a computer, just a PSBT inside a micro SD card.
He goes inside there, there's no radios there or anything.
He signs his transaction, right?
And then he flies back to Miami with his signed transaction for the secondary signer to sign in some other location.
Right.
And it's kind of fascinating.
This does this capacity of doing like a single touch per device, fully air gap, fully remotely.
Like it creates this amazing security for for no cost except for time and space displacement.

Rijndael: 00:34:52

But yeah, I mean, I think the protection that Jesse is hitting on is I think a lot of people think of having a single touch signer as being able to be like a stateless device where like it boots up, it has a key on it, you use it, sign a PSPT, and then you shut it off.
And like, nothing has changed other than the power state.
And if you are, doing a bunch of pre-committed nonces in a batch, then there's some additional state that you have to keep track of, where you either need to make sure that you securely delete the nonce that was just used, or you have to keep an index for how far into your list of pre-computed nonces you're using, and you cannot mess that up.
If you mess that up, you will lose your key.
And so I think that for some designs for signers, that might be a new amount of state that they need to either mutate or deal with like popping off the front of a stack or something.
And like you really have to not mess that up or you leak your private key.

NVK: 00:35:54

Yeah, I mean, you know, right now we kind of already have a little...
So for example, in our case, on the cold card case, we actually have state for multisig because of grifting attacks.
So technically you could, If you don't know what the change output is, or you can have grifting attacks there where they send it to a non-derivation, all kinds of shit.
So we find that multisig without state is pretty unsafe.
So that's one thing, right?
Now I wonder, I'm sure people come up with it, people smart as Jesse is, will come up with some little scheme on how, maybe you need to prove that you know what is the next nonce before you sign it, for example.
Like, I don't know, maybe there is like a little protocol that is also part of that single interaction.
So you know, everybody knows essentially not to use the previous nonce, right?
Maybe there's a hash of the previous nonce that's included in that PSPT.
So, you know, you have a hash list, so you're not using the bare nonces and you know that like, okay, don't use this one because this one is the previous or something clever than that.
I'm sure

Jesse Posner: 00:37:21

you can also have the problem of potentially leaking a private key just for a single signer.
So let's say you had a hardware device that didn't put in a secure way of preventing itself from reusing a nonce and somehow, like let's say through a fault injection attack, where right when it's going to sign and increment its counter and delete the nonce, you force the device to crash but it still exports the signature.
So then when it reboots, it doesn't realize it already did that NOX, and then you ask for a new signature of a new message.
Now, just from that one device, you've been able to extract the private key, even if you haven't been able to track the aggregate private key, you've been able to extract the component private key for that one device.
So it's not that it's impossible to secure, it's just something that people need to pay extra attention to.
And if you put the time and the effort, like there are secure ways to do it.
But if you do it naively, then you can get into trouble.

NVK: 00:38:21

It's a good year, Mark.

Jesse Posner: 00:38:28

But yeah, I think the rotating stuff is actually really useful, to be able to rotate the shares without changing the underlying secret.
Because, especially in a high fee environment, having to do sweeps a lot could get expensive.

**## Implications for lightning**

And where it can get really interesting is actually in a lightning context and I think in terms of use cases I think in in lightning I think that may be eventually where we see Frost get its biggest benefits because with Lightning, we don't really have a native way to do multi-sig.
And that's why we kind of treat our Lightning wallets like a hot wallet, not like a cold wallet, not for long-term savings, for short-term everyday spending because you've got one key that signs the state updates, you don't have your fancy multi-sig cold storage and so on.
But with Frost and really only, well either with frost or with ECDSA MPC, we have a way of potentially getting multi-sig like security with our lightning keys.
Because we can take these single keys and we can split them up.
And from the Lightning protocol layer, it still just looks like a single key, a single signature, but actually is requiring multiple entities to sign.
Now, when we think about doing this with the taproot channel, what we'd actually be doing is embedding a frost key inside of a music key.
When we'd set up a taproot channel, we have a two of two music between the channel counterparties.
Now, One or both of these public keys that creates the music key could in fact have been generated with Frost.
So now we have a Frost key embedded in a music key.
We know we can do this algebraically.
We know we can produce valid signatures.
What we don't yet have is a security proof.
So I would caution anybody from just implementing this and signing.
Hopefully, we'll get that security proof in the not-too-distant future.
There's a lot of reasons to think that it is secure, but we just want to make sure that that is the case.
And then there's another complexity with this, which is all the signers ideally would have a BFT consensus about the state of the channel because otherwise one of the offline signers could get tricked into signing a revoked state or an old channel state because they don't know about the state updates that the other signers are doing.
So the offline signer needs to be able to come to consensus about what the latest state is.
But once we have security proof and if you can have BFT consensus among the signers, then we can get these highly secure lightning wallets that we can have more funds in the wallet securely.
And when a secret is lost and we need to rotate shares, we don't actually have to close and reopen the channel because the underlying secret didn't change so we can keep the same channel open even when we're recovering and have lost devices and things like that.

**## Derisking potential of FROST**

NVK: 00:41:56

You know, one thing that sort of came to mind the first time I bumped into the frost paper was the fact that we can really, really de-risk risky devices.
So for example, you can now have a phone, where phones are kind of, all the hardware for phones are already owned.
So your wonderful cypherpunk Android is fully remote accessible by the carrier.
Same is for your iPhone and all this stuff.
So I'm thinking, hey, with this, I mean, you could have two, three phones each with a highly de-risked key, so a low threshold key.
And then you can have your CK bunker running your higher threshold key with some policy.
And then you can start having these little protocols where a device talks to the other device that talks to the other device and money moves or money doesn't move.
And if you lose your key, you don't really care.
So if you don't lose your phone or your phone gets owned or whatever, it's not really a big deal.
Maybe we arrive at a place where hardware wallets are not even required anymore, like in the distant future here, Or at least not for mid-sized funds or operational funds, right?
I mean, you know, the phones are still fucked with the AI, but, you know, your AirGap devices can resolve a lot of the AI attack issues.
But anyways, I think we're still sort of like thinking in terms of like, you know, trying to fix old problems instead of just sort of like really looking much more forward into like, what can we actually create that was not possible, right?
I don't know, I feel like we're still stuck in that.

Rijndael: 00:43:51

Yeah.
And like there's a project called VLS.
It's validating Lightning Signer.
And the idea is to take like the Lightning state machine and separate it out from all of the RPC bits and just have that available as a signer.
And so you can run that in a really constrained environment and have it do policy-based signing of Lightning channel updates.
And I think if you combine it with kind of this idea, you can imagine that you have this multi-sig Lightning wallet and you have less trusted keys on your phones, you have a more trusted key in your CK bunker or some other more locked down computing environment running VLS, and that thing can do policy-based signing and you can start having, you know, different risk levels for your different signers and have them like more or less accessible.

Jesse Posner: 00:44:45

Yeah, I think that's a really interesting model for future key management.
And I think Frost really helps in terms of having this flexibility and being able to add and remove signers without changing the underlying secret.
So Let's say you have a bunch of different signers amongst the devices people already have, you know, their watch, their phone, their computer, their tablet, like people already have many different devices and they could all be participating in a Frost Quorum where you could add and remove these devices, you can rotate the shares across those devices and create this really flexible key management setup across many different signers without having to kind of have it be so locked into a fixed configuration right from the outset.

Vivek: 00:45:38

Back to the low-hanging fruit of Lightning and its interactivity, currently there's six secrets that need to be generated and of which I believe I think it's three or four need to be online at all times is that right?

Jesse Posner: 00:45:57

I don't know the exact number but roughly yeah I mean you've got the you've got the funding key you've got the the revocation secret, those all have to be online.
You've got the payment hash preimage has to be online.
But then the keys that get paid out from the outputs don't have to be online.

Rijndael: 00:46:19

Yep.

Vivek: 00:46:21

Gotcha.
So then Frost would easily replace the ones that are online, assuming we get the security proof and all the moon math checks out, but that's the goal.

Jesse Posner: 00:46:33

Yeah, so you've got the funding key can be done with frost the output keys can be done with frost.
The thing that is the trickiest is actually the The revocation secret.
So the way we currently do the revocation secret is we use what is referred to as Rusty's trick.
Where there's this hash scheme to derive a secret and to store a secret that is super space efficient.
So I think it's even like constant space scaling.
And the thing is that does not work with FROST because FROST you can't sign over a like once it goes through the hash, FROST can no longer operate on the secret.
So this very specific scheme that is used would not be available.
So what we'd have to do is you'd basically get an unbounded growing list of secrets that have to be archived.
When you get the revocation secret from the counterparty, like There's not an efficient way to store that until we maybe come up with something else.
But for now, that would be the tradeoff is you just have this growing archive of secrets.

Vivek: 00:47:56

Well, what I'm hearing is you're an LN Symmetry and L2 supporter.
So I guess the representation and punishment mechanisms being updated would further simplify this.

Jesse Posner: 00:48:11

Yeah, I think L2 is going to work much more nicely with Frost because of that change to how the replication works.

**## State of implementations**

NVK: 00:48:20

Very cool.
So what's the state of implementations now?
I mean like you know when can we start sort of seeing some people playing with this in the actual wild?

Jesse Posner: 00:48:33

Yeah, good question.
So I have a PR in the secp-ckp repo that has a full Frost implementation that's currently in review.
I just proposed a refactor based upon some of the review comments and I'm about halfway through implementing the refactor and hopefully that's pretty much like very close to where we need to be and we can get it merged in within the next few months.
I also have a Python implementation that I need to update.
It does a Schnorr signature but not BIP 340 compatible that I'm going to be updating within the next few weeks that people can use to generate valid signatures and kind of for prototypes and experimentations and to understand how the protocol works better.
And the last thing is there's a brand new implementation that is that Tim Ruffing just pointed to in my Frost PR that is another LibSecP based Frost implementation that just came out recently and it looks quite quite nice.
I'm going to take a look at it and see.
If if there's some good ideas that maybe I'll migrate to my own implementation, so we've got basically those three.
Oh, in the sec P fun.

Rijndael: 00:50:03

Yeah, yeah, there's the sec P Fun one that Nick Farrow did.
I don't know if you've looked at that one.
I think it produces BIP340 compliant signatures.

Jesse Posner: 00:50:12

It does, yeah.

Vivek: 00:50:15

I was talking to Nifty about that, I think in Miami, and she mentioned your Python implementation.
I guess BIP340 compliance in this context is something about supporting X only or something like that, right?

Jesse Posner: 00:50:31

Basically, yeah.
I mean, it's funny because there's no Schnorr.
There's not actually like a standard Schnorr specification.
Unlike ECDSA that has, you know, is well specified.
There's all these Schnorr flavors and there's little variations of how you can have things.
So BIP340 is a specific implementation of Schnorr and its most notable kind of distinct quality is that it uses X only public keys.

NVK: 00:50:57

That's what I think we're using for the last for the edge release of CodeCurt, it was the X only.

Rijndael: 00:51:06

Yeah, it's what you need.

Jesse Posner: 00:51:09

Yeah, all of Taproot is X only public keys, much to the chagrin of many cryptography implementers who like the level of code complexity that is required to account for X only public keys is pretty substantial so it there's a lot of work to save that one bite

Rijndael: 00:51:28

yeah I've screwed up that parody bit when I've done key tweaking before.
It's subtle.

**## Nostr signing**

But yeah, the one that's in SecP256KFund, that one's in Rust.
And I think Froster ends up using that.
So if you want to do threshold signing for Noster because you want to keep the intern from posting on your Nostr account or because you want to have multi-sig for Nostr or because you want to make a shitpost out, there's a rust implementation of frost that you can use.

Jesse Posner: 00:52:03

Yeah I mean I think Nostr is a really interesting use case because we don't have any other way of doing multi-sig on Nostr literally.
Like frost is all you've got because there's no ECDSA so there's no ECDSA MPC There's no Bitcoin script and it uses BIP 340 signatures.
So, and we need secure Nostra key management.
It's your whole online identity.
It's really important to secure those keys.
And right now they're just like floating around in password managers or on people's phones or emails and stuff.
And what we really want is like a multi-sig hardware wallet enforced Nostr signing setup.
That's at least what I want.
And I think Frost is going to be how we get that.

NVK: 00:52:51

I mean, it's going to be really hard to use Nostr hardware wallets because like every single like It's signed.

Jesse Posner: 00:53:01

That's true.

NVK: 00:53:03

No, I mean, you know, like and I've been talking to the guys a lot about this.
It's like, OK, it's great.
Yeah, we can we can sign some of these keys now, But we can't really practically use it.
So Pablo just released today NSEC Bunker.

Rijndael: 00:53:24

NSEC Bunker, really?

NVK: 00:53:25

NSEC Bunker, I know.
We feel flattered, Pablo.
He borrowed CK bunker.
So essentially, it's kind of like a HSM as a service for your insect keys on Nostr, because companies can't share their keys with their employees because there's just a key.
So I'm very much looking forward to Frost for Nostr because you can now share keys with employees, but they don't have full threshold and you get to approve things and they can't run away with your company keys.

Rijndael: 00:54:01

Well, it would be cool to have some policy evaluation in there because like you could imagine you could have a policy enforcing signer for Nostra messages that are like, if you're going to like or repost an event, then that just gets approved.
But if you're going to zap something, then you have a budget.
And if you're going to post a note, then that has to be approved.

NVK: 00:54:25

No, it's more fun to do full censorship on the employees.
So if they want to, for example, say, I like big blocks, it doesn't sign.

Rijndael: 00:54:34

That's right.

NVK: 00:54:36

You know, like, you can really get in there.
Yeah, I know, but the main issue with Nostr is that, like, unlike, so Bitcoin can just move the funds to a new key, right?
With Noster, I mean, your identity is that key.
So until we have some galaxy brain, figure out some key delegation on a Noster-like network, which is too hard to have state.
Nobody knows how to do it.
Yeah, I mean, it's going to get weird and interesting.
Maybe we're just going to have a society acceptance that you burn keys.

Vivek: 00:55:16

I was going to just say, luckily these keys are not used for money.

Rijndael: 00:55:21

So in some places they are.

Vivek: 00:55:23

Yeah.
Yeah.
Yeah.
Yeah.

NVK: 00:55:26

That's fair.
The YOLO is only going to get stronger.

Rijndael: 00:55:29

Yeah.
Yeah.
There's been.
So the two things that I've seen, you know, ARK has been in the news lately.
And I think right now the current plan for ARK is that it's going to use a Nostra key as kind of like a silent payment type, type key.
And then the other one is there's a Lightning wallet that they wanted to add Ordinal support.
And so they're using your nPub as a public key and using it for Bitcoin also.
So people are starting to use Nostra keys for Bitcoin, which is terrifying.

Vivek: 00:56:06

Wait, they're using a Nostra key that was a Lightning Node pub key to receive portals?

Rijndael: 00:56:15

It's for on-chain, right?
So they're taking like your Nostra and pub and using it for on-chain Bitcoin.

Vivek: 00:56:22

Gotcha.
Gotcha.

NVK: 00:56:23

Oof.

Rijndael: 00:56:25

Why?

NVK: 00:56:28

One does not ask why.

Vivek: 00:56:30

No, no, no.

NVK: 00:56:31

I can tell you the

Vivek: 00:56:32

real reason.
Real reason is it's a bear market.
People might be trying to raise money or show growth.
For the users, this is like the adoption or that bootstrapping of that user base.
Because people are using Nostr, so you're like, hey, if I add this quick feature, then we'll suddenly get this user.
And then we'll suddenly have 5K or 10K users.
But I think it's short-sighted, probably for the same reasons you guys are saying.
Because once someone actually does lose that money, then whatever goodwill and usability you've brought up is...

Rijndael: 00:57:07

Yeah, I think it was actually more opportunistic than that.
It's like there's a browser extension that's an in-browser Lightning wallet that's actually pretty good for an in-browser Lightning wallet that also has Nostra support.
And so there's a Nostra key in there and somebody wanted to build a market where you could pay Lightning and then receive an ordinal.
And they were like, where are you going to get a, you know, on-chain compatible public key from?
We'll use your Nostra key.
And like, that's, so here we are.
So it's going to happen.
So Frost for Nostra keys is probably going to be the thing that gets more serious when people realize that they have bags attached to their Nostra identity.

NVK: 00:57:50

Yeah, I mean, you know, you could also lose all your Cashew as well.

Rijndael: 00:57:54

You know, Cashew

NVK: 00:57:55

is going to be worth a lot of money.
Jesse, are you familiar with the Cashew project?

Jesse Posner: 00:58:00

No, I'm not.

Vivek: 00:58:02

It's Chamin Mint, single SIG.

NVK: 00:58:05

This is very, very cool.
I mean, Kali, who wrote that.
Yeah, I mean, it's just Chamin Mint and you can trade these tokens using Noster.
I don't know if it's fully integrated with Noster or not.

Rijndael: 00:58:20

Yeah, the command line version is.
So like, if you use the command line client, like, like, Jesse, if I have your npub, I can say send 500 sats to this npub.
And it sends like a like a Noster DM to you with a bunch of Cashew eCash.
And then you run the Cashew command line client and it grabs your DMs and looks for Cashew tokens in them and then automatically redeems them.

Jesse Posner: 00:58:49

Oh, that's cool.

NVK: 00:58:50

Yeah, it's essentially the hackers version of FedeMint without being federated.
They were first to market.
Anyways, it's and I think the Fede guys are also going to do a lot of stuff related to Nostr as well.
Well, actually Mutiny as well.
So I don't know if you're familiar with Mutiny.
You are.
So they are also using Nostr IDs as a way to have a contact to send Bitcoin to.
I don't know to the extent of the integration because I didn't read it.
But I think people are starting to use that because it is a signed ID, right?
And it's self-signed too, which is really cool.
So you have a permanent person, a permanent ID somewhere.
It's going to get weird.
It's going to be weird and cool, but it's going to get weird.

## FROST tradeoffs

OK, guys.
I mean, do you guys want to start touching a little bit on roast?
I think maybe a good point, unless there is something else that we missed there on the first part.

Rijndael: 00:59:51

I think like the downside for Frost, so like we've been talking about lots of good things for Frost.
So like smaller on-chain footprint.
If there's second layer protocols that assume that you have single SIG, then like you can just kind of drop frost in there.
That's like really nice.
Being able to add or remove keys is really nice.
Being able to change the configuration of your multi-sig is really nice.
Some of the downsides just to like round it out are, there's more complexity and it's more stateful around like the non-sequitur that we talked about.
But another one that we haven't really mentioned is if you're using multi-sig in like a multi-user setup.
So you have a bunch of people at your company and everybody holds a key, if you're doing script-based multi-sig, you can tell on-chain who signed, which adds some really nice transparent accountability.
And with Frost, all of those signatures get aggregated down into a single signature.
And so if you had a three of five and all of the money moves on chain, you can't really look on chain and see which three people moved it.
So if accountability is a feature that you're looking for, then there's some other things that you can do.
There's a number of schemes out there, but in general, where Frost starts having some trade-offs is if you wanted to use it for something like the Fediment on-chain wallet, you might want to really make sure that you know which of the Fediment Federation guardians signed for the money if all of the money leaves.
And so if you're going to adopt something like Frost, then you need to add some additional mitigations to make sure that you have accountability.
Yeah.

NVK: 01:01:39

I mean, nothing is without trade-offs, but.

Rijndael: 01:01:41

Oh, for sure.

NVK: 01:01:42

Yeah, I mean, I just, I don't know, like every single time, you start sort of examining the practicality of standard multisig P2SH, right?
You really sort of like, it's just like a pit of sorrow, You know, it's just horrible.
I mean, because see, you know, we talk about like, you know, yes, technically now you need some statefulness, right?
But

Rijndael: 01:02:10

I'll take it.
Sounds great.

NVK: 01:02:12

In practice, you need statefulness in multi-sig too, because, you know, you have three metal plates now that need to be buried somewhere or need to be re-shamiered somewhere else, right?
Or the security risk of rolling all the funds into a new wallet and the privacy loss because you're not going to do some crazy coin join to move all your business money from one wallet that might be compromised to another.
Right.
Like things break down so fast when you get into the actual practicality of it that when you compare the actual practical concerns of Frost versus P2SH, right?
Like those trade-offs are not as bad.
I mean, they really aren't.
And at the end of the day, I mean, like, I feel like right now it's been very sort of, you know, the hardware signing sort of industry has been sort of like a little bit too kiddy, like script kiddy, like with some things where, you know, we gotta grow up and learn how to do statefulness on things properly and, you know, have better protocols on how to exchange the information.
And you know, it's just, you know, there is a lot of money to be stolen and we see, you know, bad implementations out there who they do get own.
But like, I feel like as this industry sort of scales, like really into more people, more targets, like we're really going to have to grow up and do things in more complex ways that do sort of, you know, address a lot of this with other sets of trust things that are not just a Bitcoin signature itself, right?
So it's the devices, it's some protocol between the devices, it's, You know, the devices have second signatures or like how it decrypts the secret inside, whatever.
You know, it's all part of growing up as an industry.

Jesse Posner: 01:04:13

Absolutely.

Rijndael: 01:04:14

Yeah, totally agree.

Jesse Posner: 01:04:15

I mean, they say like in cryptography or in Bitcoin, you know, you replace all problems with key management problems.
You know, we don't have to worry about like, we don't have to worry about the Fed or, you know, all this other crap.
But the one thing we do have to worry about is key management.
And increasingly, as more and more of the world is built on top of this basis, these keys are literally going to secure our entire civilization and we're going to need to keep upping the game for how we manage them.

NVK: 01:04:46

Yeah, I mean, whatever you do, just keep them offline.
I just I can't emphasize this enough to people.
Every conversation should end with you never plug them in.

Jesse Posner: 01:04:59

Air gapping is strong.

**## ROAST**

Vivek: 01:05:02

Right?
I'll queue them up for the roast stuff.
So, so far to summarize Frost, we have, you know, it's unforgeable under concurrent signing sessions.
It's semi-interactive signing with respect to a pre-signature round that you can still exchange a committed nonce without a message or like the subset and then the signature round.
So Frost doesn't solve the robustness.
What is robustness, Jesse?
What is an identifiable board?
And why should we even care about having multiple concurrent sessions?

Jesse Posner: 01:05:40

Okay, great question.
So robustness is a guarantee within a signing round that as long as you have a threshold of honest participants that you can get to a signature without a malicious participant disrupting the round.
So in FROST, in advance we have to pick, okay, who's going to be signing?
Let's say we have a 33 out of 100 setup, and let's say we want to create a signature, like let's say to a FedEmint or something like that.
There needs to be a selection of who is going to sign.
And then the coordinator will pick out the signers.
Then the signers will proceed to produce signatures.
But if the signatures are invalid, then you have to figure out who submitted an invalid signature, then restart the process, kick the malicious participant out, or maybe they're just unavailable or they're not malicious, there's a bug in their code, but to kick out the defective participant, and then proceed again.
And when you have a very large set of signers, you could have a denial of service vector where participants could keep disrupting the signing process.
So What ROSE does is it creates a guarantee that you're going to get to a signature as long as you have a sufficient number of honest participants.
The way it does that is it actually instantiates multiple Frost sessions in parallel.
So Roast is just a wrapper around Frost.
You take the Frost APIs and you just structure them in a new way and you run them in parallel, and that's how you get Roast.
Since you have these parallel sessions, if some of the sessions don't complete, you have other sessions that will complete and you're guaranteed to get to this outcome.
And it's Really something when you get to large sets of participants where that becomes important.
Obviously in something like a two of three it doesn't matter if one of the participants doesn't complete you just switch to the other and you're done.
But as you get more and more participants, Roast is a really nice way to guarantee you're going to get this signature.

NVK: 01:08:05

You know, Jesse, I was I was having a drink with Justin and I mentioned to him that the ideal federation, every single participant in the federation, sorry, in that mint would have a key.
And then you're back into democracy where the majority can print the money.

Vivek: 01:08:28

Right, Yeah.

NVK: 01:08:30

So

**## How does coordination work?
**
here's the interesting thing.
Like, so maybe I have missed this from before.
So can any party coordinate or do you need a specific secret or, you know, how does it work for you to coordinate that maybe is different than P2SH?

Rijndael: 01:08:48

So in Frost, a coordinator isn't actually required.
It's an optimization.
So if you don't have a coordinator, then you need like a broadcast mechanism because you're going to be doing, you're trading around nonce commitments and then you're trading around partial signatures.
So having a coordinator is just like an optimization where everybody sends their pieces to the coordinator and the coordinator sends pieces to other participants instead of everybody having to send everything to everybody else.
The coordinator can be any of the participants and they don't have any like special secret key or something.
So you could, if this is like you're running Sparrow on your laptop and it has Frost support and you have a bunch of like signers, then you could use Sparrow as the signature aggregator.
Like that's the coordinator.
If this is like a multi-party protocol, then it could be like any person.
Maybe you have some like verifiable random shuffle or you take the last block hash and you do a mod the number of people and you say, okay, Jim, you're the coordinator now.
It can be like any other participants.

Vivek: 01:09:57

So to summarize and using Chelsea Kumlow's language, the combiner is what we're referring to as a coordinator here.
And then a signer can also be a combiner or a combiner can just be some other entity in general that gets all the shares.

Jesse Posner: 01:10:14

Yeah, that gets the signatures.

Vivek: 01:10:17

No signatures.

Rijndael: 01:10:18

Yeah, it doesn't get shares.

Jesse Posner: 01:10:22

Yes.
Yeah.
So, and typically, you know, only what, like, let's say you're signing a Bitcoin transaction, somebody is going to take the Bitcoin transaction and publish it to the network.
Not every participant is going to each publish it.
So usually you have somebody, some entity or system or service that's actually going to aggregate the signatures, publish the transaction, but it's not, they have no secret data.
They can't steal funds.
They can't forge a signature.
They don't have to be trusted.
Like the main thing they can do is just thwart the signing, you know, denial of service.
But they can't, they can't steal.
They don't have anything secret and anybody can serve that function and play that role.

NVK: 01:11:07

Very cool.
So are you concerned about having different sets of signers not coordinating correctly and maybe signing funds out without say, for example, you know, a group of six.
So say you have a six out of a hundred, right?
Something silly and you only need 10, right?
So 10 of them sign, right?
But then what if another 10 are doing the same thing and another 10 are doing the same thing?
I guess you're just gonna bump into issues where you're gonna have spent outputs, right?

Rijndael: 01:11:43

Yeah, I think it would be the same as if you had a, I'm gonna make this up, if you had like a one of 15, like P2SH multi-sig, and you had different people all trying to spend the money at the same time, then you're going to run into problems with like double spending the same outputs or other things like that.

Vivek: 01:12:02

Luckily with this, you can identify who is trying to do the spending, right?
Of the subsets.

Jesse Posner: 01:12:12

You wouldn't be able to tell from the on-chain transaction.
You wouldn't know who's signed.

Vivek: 01:12:17

Yeah, Not to the public, but as a signer.

Jesse Posner: 01:12:20

If you have good, you know, you would need like logging and forensics and stuff to figure it out.

Vivek: 01:12:25

Nice.
Okay.

Rijndael: 01:12:26

Yeah.
Another like really interesting scheme that I heard, I forgot who told me this, An idea that I heard was, you know, since we have taproot, like one way that you could do frost is you have a tap leaf for, so say that you had like a three of five, just to keep the numbers small.
So imagine if what you did was you had five tap leafs where each one had a single SIG with one participant and then a two of four frost for the other ones.
So you're still using Frost to aggregate most of your quorum down to a single signature, but then one of the signatures is identifiable.
And whoever is being the coordinator, you have them have an exposed single signature in that tap leaf, and then you have everybody else aggregate down to a single key, and that way on-chain, you can identify who the coordinator was, and then you go to them and say, who else signed?
So I think that there's like some tricks like that that we could use to add some on-chain accountability while still keeping some of the benefits for like really large quorum sizes, you're still doing a script path spend so you don't get all of the benefits of Frost, but it's a way that if you were running like a federated system, you could still have a lot of on-chain space savings but still some accountability.

NVK: 01:13:48

Very interesting.
But it's

Jesse Posner: 01:13:49

a great point that it does not solve the issue of the signers needing to know what they should actually sign.
So you know, and this is typically I think the weakest point in a lot of these systems is if you can corrupt, like let's say you have this giant system of servers and humans and all these different people signing, but you corrupt the actual address you're spending to And whatever services, the person inputs the address, this is where I want to spend.
And then that's swapped out.
And that system sends to all the signers, hey, sign this transaction.
Like there needs to be a way of authenticating, like is this what I should actually sign?
Is this correct or not?
And that is oftentimes the easiest way to subvert these types of systems is just corrupt the process by which the signers believe that they're signing the correct thing.

NVK: 01:14:46

Right.
And is there a solution for that?

Speaker 1: 01:14:51

Is

NVK: 01:14:51

there sort of like a parallel sort of protocol or something where you were exchanging?
You know, It's like you go back to the BSMS thing, the Bitcoin secure multisig thing, which is not like great either.
I still think that we still haven't found, or at least like I don't know of, a good solution around transporting this stuff securely, right?
Is this something that's being worked on?
Because multisig is max 12 signers, realistically speaking, with Frost it's going to be 100, 1000, we don't know.
So now having a proper protocol to do this is going to be really important.

Vivek: 01:15:39

The most adjacent and probably advanced is probably the VLS team, correct?
I think because of essentially the trade-offs though with blind signing versus VLS, it varies greatly per use case, whether Once you're adding the velocity checks and the policy and the white listing and blacklisting and then thresholds and other things, at what point do you realize you're just recreating like a full node in another smaller hardware device and if there's a better way of doing it?

Rijndael: 01:16:15

Yeah, I mean, there's a mix of, you know, you want to do validation of whatever you're signing like close to the signing.
So this is the classic, like, actually check that this is your change address, like make sure that, you know, you're not spending to some derivation path that like you can't spend from in the future.
There's that, but then there's also you want to make sure that the destination has some amount of authenticity and integrity protection, and hasn't been tampered with in flight.
And that opens up a lot of questions about like, okay, do I have some, you know, trust on first use key that came from the coordinator and they're going to use that to like sign PSBTs that they send at me or like, you know, it's really complicated and there's not like a standardized protocol for it yet.
I think that that's something that would be cool to see in some common like multi-sig coordinators and get that standardized where you could have interoperability between signers to have kind of like authenticated signing sessions would be a nice improvement for Frost, but also just for like P2SH style multisig as well.

Jesse Posner: 01:17:31

Yeah.
I also think the, what is it, the like the stealth addresses or the new protocol.

Rijndael: 01:17:40

Silent payments.

Jesse Posner: 01:17:41

Yeah, could really help if we can have more static identifiers for payees and that they could be you know on people's NOSTR or otherwise where you'd have some out of bed way of checking like I'm a signer I got a request to sign should I approve it or not well it's being sent to Alice and this is you know, this is drivable from Alice's silent payment address and I can check that she has that listed on her Nostr and on you know, maybe a couple other places.
These ways of verifying that who you're sending it to, the address matches the intended recipient, and that there's multiple ways of checking that, and that we even maybe build out like secure address books or contact lists that allow this to be done in a secure way, I think is going to be part of the solution for this type of problem.

Rijndael: 01:18:38

Yeah, it's really funny.
We were talking about people sending money to Nostra end pubs earlier.
I just realized I'm pretty sure that you could use an end pub as a silent payment, like reusable identifier.
So you actually could send to somebody's end pub, but not have it be identifiable on chain that you're sending somebody's end pub, which would be pretty dope.

NVK: 01:18:55

Things are going to get so weird.

Vivek: 01:18:57

Yeah, things are going

Rijndael: 01:18:58

to get really freaky.

NVK: 01:18:59

Things are going to get really, really weird.

**## Libraries and repositories: where should FROST live?**

OK, so on that vein, Jesse, have we missed anything in terms of reviewing Frost and Roast to people, on your perspective?

Jesse Posner: 01:19:20

I think we've covered all the main points, all the important stuff.

NVK: 01:19:25

Okay.
And I guess, yeah, I mean, I guess we can't really get into the weeds of implementations because we're still waiting for an implementation to sort of really be released.
And once that's released, we're going to start finding all the problems.

Jesse Posner: 01:19:42

Well, hopefully that will be surfaced in review.

NVK: 01:19:46

But yeah, that might happen.
No, no, I mean, not the problems with the implementation, but the practicality and sort of like how to actually use this in wallets and users.
Yeah.
Integrated and

Jesse Posner: 01:20:00

applying.
Yeah.

Vivek: 01:20:03

So the order of operations is, you know, you're on the SECP, ZKP library, rebasing your PR.
Then once you rebase it, I guess you'll ask for review, probably do the rounds like Bitcoin Core PR Review Club, whatever other, you know, Bitcoin Optech sessions, whatnot.
And then after much more further scrutiny, we can expect to see it in official like SecP256k1 library, correct?

Jesse Posner: 01:20:34

Yeah, that may be a while.
I mean, there's some discussion over what is this proper scope for these two different repos.
So we've got the SecP256k1, Then we've got SECP256K1-ZKP.
And right now, mainly all the direct dependencies of Bitcoin Core are in SECP proper.
And then things that aren't a direct dependency like Music, Frost are in Dash DKP.
But there's been some discussion by the maintainers to potentially expand the scope of SecP proper to include cryptographic protocols that are relevant to Bitcoin but may not be a direct dependency, but only when we have a very high confidence in them.
So eventually we'll hopefully see Frost and Music and these systems make their way over to the main repo, but for now that stuff is kind of living in ZKP and ZKP is like a nice staging ground for some of the more experimental or new cryptographic protocols.

Rijndael: 01:21:45

But like, what's nice is it doesn't like, we're not going to be dependent on, you know, a soft fork or any kind of consensus change for this.
Like, I think, you know, a lot of folks are going to look at the ZKP implementation as like a reference implementation, you know, maybe it's really easy to integrate into other wallets.
Maybe people use the SecP256K Fun one for like Rust applications.
But once there's sort of some standards, that there's community consensus around, people can start building on top of this stuff.
And it doesn't necessarily have to end up in Bitcoin Core.
Like you don't have to be blocked on it getting into Core.

NVK: 01:22:23

Yeah.
I mean, Core doesn't have a lot of things still that are like that are in the double digit BIPs. So it's normal, right?
I mean, like, I personally think that the core wallet is going to slowly start to be so behind that, like, even the people who are very adamant about using it may not be using it anymore.
And, you know, we're going to just accidentally become Bitcoin Core as Core versus Bitcoin Core the wallet Which was the intended separation that one day is gonna happen It's just too much right for for that implementation to have on it.
I mean, it's just It's silly, especially because it's not consensus code.

Vivek: 01:23:04

So we're all Libbitch Colonel shills now.
I was selfishly asking about the order of operations because you know in the cold card we use the SecP library So I'm doing some mental math in my head and figuring out when I get to say when frost 10vk You know in a year or so like just thinking about it from that angle

NVK: 01:23:29

You know, I like I like taking Peter's approach is that never.
The question goes away and then a month later, boom, here.

Jesse Posner: 01:23:39

Right.
Yeah.
I mean, once it's in ZKP, I think that's a good time to start using it.
You know, It could be years before it makes its way into SecP proper, not for a security reason or anything else, just because there's a lot of process questions of where code should live and stuff like that.
Live and stuff like that.
One thing is also I'm working on a Frost BIP.
So that will provide a standard way for anyone to implement it in the way that's compatible with Bitcoin.
So we'll have that as well.
And also I plan on implementing Rust findings.
I'm still kind of waiting to see how the Rust findings work for Music.
Are we going to have a Rust ZKP or a Rust Bitcoin ZKP?
That is where this kind of like repo stuff starts to get complicated is like how the Rust dependencies build on top of it.

NVK: 01:24:37

Can you even say the word Bitcoin and Rust together?
I think it's still under litigation.
So I'm calling it crust Until they resolve their legal issues.

Jesse Posner: 01:24:50

Yeah, I better be careful.
I don't want Craig Wright coming after me.

Rijndael: 01:24:55

Well, there's a community fork of that language.
I think it's called Crab.
So maybe we'll have a Crab...

Vivek: 01:25:03

Crab sec P.

NVK: 01:25:04

Why didn't they call it crust?
It was so good.

Rijndael: 01:25:07

Naming is hard.
Yes.

NVK: 01:25:10

Anyways, OK.
OK, so yeah, I mean, it's the natural path for any sort of new primitive, right?
I mean, I think the BIP is going to help clarify a lot.
The fact that there is no consensus changes or needs is a huge deal.
It means you don't need permission.
You can start frosting all your things.

Vivek: 01:25:32

You have a BIP number, by the way, Jesse?

Jesse Posner: 01:25:35

No BIP number yet, but I have a draft BIP that I have linked to in my PR.

NVK: 01:25:40

Is that going to include Roast, the same BIP?

Jesse Posner: 01:25:44

Initially it will not include roast.
Once we get frost settled then we can move on to to roast even I don't even know if there's like a roast implementation out there currently.

Rijndael: 01:25:58

I remember at one point the your Frost implementation was using part of Music, I think for the key generation, is that still the case?
Or did that get punted?

Jesse Posner: 01:26:11

I changed it.
Yeah, initially I realized I could actually use like most of the music APIs for frost.
If I change the frost protocol a little bit where you actually create both a music and a frost key.
And I was just kind of seeing like how, like there's a lot of overlap between like the signing protocol and the knots protocol between frost and music are basically exactly the same except for frost you're signing with the Shamir secret and with music you're not so there's a lot of overlap but in review and after talking to Jonas and Tim and Seth, we kind of decided it was better to like not try to merge these things.
And we couldn't really come up with like a use case, why it would be useful to have like a key that is both music and frost.
So, So now the current implementation has its own APIs. Some of them are modeled off of the music APIs, but it's not using any of the music APIs. My refactor is bringing the implementation even closer to how things are specified in the paper.
So a lot of this kind of early like weird stuff I was doing is kind of like made its way out of the implementation.

Rijndael: 01:27:27

Okay, cool.
I mean, that's nice because it means if somebody goes to the paper, we'll follow the implementation.

**## Broadcast channels and authentication**

Jesse Posner: 01:27:34

Yeah.
There's one, there's one thing that we have kept that I think is kind of cool, which is the paper doesn't tell you how to implement the broadcast channel.
It just says you need a broadcast channel.
And so what we're doing is we're creating this this hash of all the VSS commitments and signing that.
And that is fulfilling this requirement for the broadcast channel.
And another feature that I'm planning on adding is part of the protocol, you already need an authentication key for each participant.
And so what I'm considering doing is using that authentication key to export, and this is actually Elify's idea when he was reviewing the PR to export the shares.
What's that?

Vivek: 01:28:26

Whose idea?

Jesse Posner: 01:28:28

Elify.

Vivek: 01:28:30

True.
Yeah.

Jesse Posner: 01:28:31

Yeah.
Cryptographer.
I forget his last name, but he, yeah, it starts with a T.
He suggested that the API export encrypted shares from the key generation protocol, because that's left right now up to the user of the API that you generate shares and you have to send them to other participants, but that needs to be done over a secure channel.
But since we already have authentication keys baked into the protocol, what we can do is the API can use ChaCha20 poly1305 to take the authentication key of the recipient, encrypt the share with that authentication key using Diffie-Hellman, and then that way, built into the implementation, you already get the secure channels between all the participants.
And oh another thing is my implementation works with BIP32 key derivation so you can have a frost key and then you can derive keys from it and all the participants can sign the derived keys.
It works with taproot key tweaking as well.
So all of that stuff is working with frost.

Vivek: 01:29:45

Is there any particular reason you also chose like the same algos that Lightning has?
Like the ChaCha and the Poly?

Jesse Posner: 01:29:55

Mainly because, well, ChaCha20, Poly1305 is like one of the best authenticated encryption ciphers And we already have a ChaCha, not ChaCha20, but we have a ChaCha API in SecP that's used for, I forget what it's used for, It was some kind of optimization for like hashing the block or something like that.
But we have ChaCha in SecP and Poly13.05 doesn't take much to implement.
So I figured I just throw that in and then we'll have ChaCha20 Poly13.05 in SecP, which will be nice because it's built on all the highly secure SecP low-level primitives and APIs and will have tests for constant time and all that stuff.
So that might be useful in general for people who want to use an authenticated encryption cipher.

Rijndael: 01:30:48

Cool, and also BIP-324, which is the new encrypted P2P transport, that also uses Cha-Cha-20 Poly-1305.
So Yeah, I think they're using a different implementation, but it'd be really cool if they could just get that from LibSecP.

Vivek: 01:31:04

That would.
That's the peer-to-peer encryption VIP.

Rijndael: 01:31:10

Yeah, it's like opportunistic encryption for all the peer-to-peer traffic.
Very nice.

Jesse Posner: 01:31:15

Yeah, Peter worked on it as well.
Yeah, Peter Vola.

Speaker 1: 01:31:19

Yeah,

Rijndael: 01:31:19

it's super

**## Final thoughts**

cool.

NVK: 01:31:21

Very cool guys.
All right.
I mean, I think we've covered a lot of ground.

Rijndael: 01:31:26

Yeah, another boring episode where there's nothing happening in Bitcoin.

NVK: 01:31:30

That's right.
There's nothing happening in Bitcoin.
We've managed to bore you to death.
We've got some algebra lessons today and very basic stuff.
And if you didn't understand everything here, you clearly don't have what it takes to be a clown wizard at a Bitcoin conference.
And yeah, I mean, you know, like, what can I say?
Bitcoin is dead.
Listen, guys, this was awesome.
I'm really, really looking forward to seeing this dismerged because, you know, it's hard for people to start implementing client things until it's at least on ZKP, right?
Because, you know, until it's there, kind of people go like it's never going to happen on Bitcoin, right?
It's kind of a nice thing in a way.
So I mean, I'd love to have you again here, Jesse, when we have this hopefully on Coldcard and some other implementations around.
And Rindell, when you have some of your very cool, interesting projects you're involved in, maybe start leveraging some of this stuff.
So yeah, guys, thank you.
Thank you so much for doing this.
So let's just do a little round of any final thoughts.
Mr. Vivek.

Vivek: 01:32:45

My brain is completely fried.
Even preparing for this and watching.

NVK: 01:32:48

It's roasted you mean?

Vivek: 01:32:50

Yes, it's roasted.
I can't even use my arms anymore.
But after you watch like Chelsea Kumlo and like Tim Ruffing long enough and get to parse Jesse about implementations, your brain's just tapped out.
I'm a glazed donut up here right now.
So I want to thank you guys again.

NVK: 01:33:13

Jesse, any final thoughts?

Jesse Posner: 01:33:15

Yeah, just kind of jumped the gun there.
Thanks for having me on.
This has been great.
And I'm always happy to chat about Frost.
Please reach out to me if anybody's interested in learning more about it or reviewing it or implementing and working on it.
And more than happy to come back on the show anytime.
And I'm just really excited for the future of key management.
I think we're just barely even scratching the surface of what's possible.
And I think it's going to be really important that these systems continually involve and improve as they secure more and more data for more and more people.

NVK: 01:33:56

So what do you really have to say is that not your threshold of shards, not your Bitcoin?

Jesse Posner: 01:34:04

Exactly.
Well said.

NVK: 01:34:07

And Rindell, any final thoughts?

Rijndael: 01:34:11

Yeah.
So we talked about Frost a bunch.
The original paper is called Frost Flexible Round Optimized Schnorr Threshold Signatures.
So it should probably be Frosts, but whatever.
It was written by Kumlo and Goldberg.
I actually really recommend if you're interested in this stuff, go find the paper and read it.
As far as cryptographic protocol papers, it's actually one of the more readable ones out there.
And it does a good job of kind of walking you through all of the pieces underneath Frost and then how they come together and why they come together the way that they do to make Frost.
So if you're interested in this, definitely go and read the original paper and then pepper Jesse with lots of questions and he'll help you.

NVK: 01:34:54

That's right.
Let's give Jesse's phone number so people can just text him about their implementation questions and everything else.
Just kidding.
Well, guys, thank you so much.
This was awesome.
And with that, we're closing it up.
Thanks for listening.
For more resources, check the show notes.
We put a lot of effort into them.
And remember, we don't have a crystal ball, so let us know about your project.
Visit bitcoin.review to find out how to get in touch.
You

## End of podcast
