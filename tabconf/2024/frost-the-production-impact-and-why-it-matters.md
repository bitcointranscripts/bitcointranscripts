---
title: " FROST, The Production Impact and Why It Matters"
speakers: null
source_file: https://www.youtube.com/watch?v=Z0F6AkGPby4
media: https://www.youtube.com/watch?v=Z0F6AkGPby4
date: "2024-11-26"
summary:
  "Requirements for Bitcoin key management are ever more demanding, and\
  \ many off-chain tools require user dependence on hot keys instead of (safer)\
  \ cold keys. Breakthroughs in cryptography like Flexible Round-Optimized Schnorr\
  \ Threshold Signatures (FROST) and the Taproot upgrade are helping developers\
  \ and users re-think their approaches to private key security. FROST is a protocol\
  \ that minimizes the number of rounds of communication between participants in\
  \ Schnorr signature schemes to reduce network bandwidth, time, and probability\
  \ of errors. Cryptographers, protocol developers, and other Bitcoin builders will\
  \ discuss the state of FROST, its use by Bitcoin companies, and its potential\
  \ for reshaping Bitcoin security.\n\n What would an attendee learn from this talk?\n\
  \nThe Basics: \u201CWhat is F.R.O.S.T.?\u201D\n\nComparing offchain and onchain\
  \ multisig tools\n\nComparing different multisig key aggregation schemes\n\nOverview\
  \ of FROST, Frostsnap, and other private collaborative custody tools\n\n Is there\
  \ anything folks should read up on before they attend this talk?\n\nhttps://en.bitcoin.it/wiki/BIP_0340\n\
  \nhttps://gist.github.com/nickfarrow/4be776782bce0c12cca523cbc203fb9d/?ref=tftc.io\n\
  \nhttps://frostsnap.com/introducing-frostsnap.html\n\nhttps://www.tftc.io/issue-1379-using-frost-to-increase-privacy-in-collaborative-bitcoin-custody-models/\n\
  \nhttps://brink.dev/blog/2021/04/15/frost/\n\n Relevant Links\n\n About the panelist\n\
  \n Social Links\n\nhttps://github.com/jonasnick\nhttps://github.com/jesseposner\n\
  https://github.com/satsie\nhttps://github.com/0xBEEFCAF3\nhttps://github.com/jurvis\n\
  \n\nTwitter: @Arminsdev\n\nWebsite:\_[www.botanixlabs.xyz](http://www.botanixlabs.xyz/)\n\
  \nTABCONF 6, GitHub link\nhttps://github.com/TABConf/6.tabconf.com/issues/50"
tags: []
categories:
  - Education
transcript_by: 0tuedon via tstbtc v1.0.0 --needs-review
---

## Introductions

Speaker 0: 00:00:05

All righty.
Hi, everyone.
Thank you all so much for coming today.
My name is Satsi.
These are my friends.
And today we are going to be talking about FROST.
I promise you it's going to be a cool panel because FROST stands for Flexible Round Optimized Schnorr Threshold Signatures.
But that's all I'm going to tell you about because our panelists are far more qualified to talk about it than I am.
So let's jump into introductions starting with you, Jervis.

Speaker 1: 00:00:35

Hi, my name's Jervis.
I work at Block on the BitKey wallet.
Yeah.

Speaker 2: 00:00:43

My name's Jesse.
I work with Jervis on BitKey.
And I'm also working on an open source Frost implementation in the secp-zkp repo.

Speaker 3: 00:00:57

I'm Jonas, I work in the Blockstream research group.
I've been working on a protocol related to Frost for a couple of years that is called Music.
I co-authored the paper as well as the implementation.

Speaker 4: 00:01:16

Hey I'm Armin.
I've been working on Bitcoin self-custody and privacy, actually with Jervis and Stacey for the past half decade.
And for the last year, I've been working on sidechains.
We've been using Frost.
Thanks.

## What is FROST

Speaker 0: 00:01:30

Great.
Awesome.
So, we got to start with what Frost is.
And when I first learned about it, there's a lot of cryptography involved, and the one person who was able to teach me about it was Jervis right here.
So can you do us a solid and share with the audience what Frost is and what some of the pros and cons are when you're comparing it to something like the script-based multi-sig that we all know, but not all of us love.

Speaker 1: 00:01:58

All right, I guess when I first introduced you to it was a couple of years ago.
So I'm going to try again.
Might have gotten worse over time.
So Frost is basically a paper written by Chelsea Kamlo.
And it is basically a way of constructing Schnorr signatures distributively and also being able to get a bunch of participants to come together to construct a bunch of key shares without ever having construct a key in the first place.
And a combination of that allows you to enroll like a bunch of signers that would be able to come together to create a Schnorr signature to spend Bitcoin transactions that appear just like any taproot transaction on-chain.
And so as a consequence of that, what that means is contrary to pre-existing models of multi-sig, meaning the ones that use object multi-sig.
That means that when you spend Family Wallet as, I don't know, a two or three, a three or five or whatever, everything shows up on-chain just as a regular taproot transaction.
So there are a bunch of benefits and it's not just about privacy on-chain and not revealing all the public keys on-chain or key arrangement on-chain, but also as it turns out a lot of practical benefits.
For example, say you are a collaborative custodial customer, and you have a two or three, and that's the app, the server, and a hardware wallet.
Say today with a pre-existing model, if you lose a hardware wallet, effectively, you would have to go purchase a new hardware wallet and then sweep everything and to reestablish the 203 quorum.
And that specific user event, if you will, incurs not just a monetary cost that comes with needing to pay fees to sweep your entire wall, and depending on the amount of outputs you have, it could cost quite a lot.
And on top of that, there's also a bit of a privacy loss, right, because you kind of make yourself susceptible to sort of transaction linking because you're really just gathering all your outputs and be like, hey look this is me.
And so Frost kind of lends itself well to leveraging extension protocols like proactive secret sharing, where it kind of takes care of that in a sense where you move a lot of these rotations and repairs off-chain.
So none of that will require going on-chain and as a result like no fees, et cetera, et cetera.
So, was that helpful?

## Distributed Key Generation

Speaker 0: 00:05:10

Thank you for that.
So, Frost can be divided into two parts with the first being something called distributed key generation or you'll see it a lot as DKG, which we're going to talk about more.
Armin, can you tell us a little bit about DKG?
And you're using Frost right now, so can you tell us what it's been like to implement that?

Speaker 4: 00:05:30

Yeah.
Jervis kind of covered DKG a little bit.
So this is distributed key generation.
And the goal of DKG is to generate secret shares and an aggregate public key for our threshold multi-sig in a verifiable, and it's in the name, distributed way.
And I think the best way to explain DKG is to understand the alternative, which is a trusted dealer setup.
So this is where a single authority will generate the secret shares for each peer and distribute them in a secure and authenticated way.
But the clear drawback with this is that the key has to be constructed in memory at one place.
So if you have an application that has high security requirements, this might not be a very attractive property of your protocol.
But if you don't, it's actually quite nice, because then you don't have to play an interactive protocol.
So that's the break me out to DKG, which has a really neat property where each peer can generate their own secret share and the aggregate public key without the key ever being present in memory fully.
But it also has some drawbacks.
So I mentioned this interactive protocol.
So DKG is a two-round asynchronous protocol, and it has drawbacks.
You have to deal with the edge cases.
What if a peer disappears halfway through maybe round two, how do you restart this thing?
Maybe you need to discard shares of a previous session in some verifiable way.
It also has kind of a gnarly and novel property for most applications called agreement.
So this is where peers need to...
So Alice and Bob will have to agree that they receive the same protocol messages from Carol.
And if they don't, they can end up with different aggregate public keys, and money can be gone.
So that's a little bit about DKG.
And maybe I'll stop right there and ask if the other panelists want to add anything.

Speaker 3: 00:07:28

Yeah, I would like to add something.
So we've been working on a BIP draft for a distributed key generation protocol.
The problem that it solves is that you can implement it without knowing much about cryptography or having to read the paper.
If you want to implement Frost right now, you can look up on the internet.
There is a Frost RFC standardized by the IETF.
And in the abstract, they make it clear that they don't specify a distributed key generation protocol.
They only specify the trusted dealer mode.
Okay?
If you don't want to have the trusted dealer mode, There are good reasons for not to have this trusted dealer because the dealer might be compromised and not able to delete secret shares.
You want to implement a distributed key generation algorithm, which means that you need to read the frost paper and understand what they are saying there, how to build this protocol.
And the way they describe it in the paper is that they make some assumptions about the reader, namely that the reader has some background in cryptography.
So they say the secret shares must be sent over a secure channel to the other participants.
I guess most people in the room will understand what that means.
Secure channel means this is a channel that allows you to send encrypted messages and it's authenticated.
The other primitive they need to use or they need to use in order to build a DKG in the Frost paper is a broadcast channel.
And a broadcast channel is often misunderstood what it is, at least if you give it to an engineer a An engineer will think that a broadcast channel just means that you send messages to everyone but That's not what a cryptographic broadcast channel is.
And so when reading the first paper and wanting to implement that, you need to understand that.
And the advantage of ChildikG is that, essentially, it does all that thinking for you.
We call it, it's a standalone implementation, so it doesn't refer to these external primitives like secure channels or the broadcast channel.
It deals with the edge cases that you mentioned, And it has a couple of additional features that are useful for a DKG.
For example, it has some relatively novel approach to to backups it works with an untrusted coordinator and Yeah, things like that Nice thank you for that.

## Signing

Speaker 0: 00:10:19

Yeah, check out chill DKG when you have a moment Okay, so we're gonna talk about the second part of frost which is the signing So I have an easy question for you Jesse and a hard one The first one is just please describe how the signing process works and then the follow-up to that is that given that Frost typically will have multiple participants, is there anything interesting that we can do with privacy?
Like, do all signers need to see everything that is being signed?

Speaker 2: 00:10:46

Yeah, so the way signing works is it's built on a Schnorr signature, and a Schnorr signature is kind of a remarkably beautiful and simple signature construction.
So It is a linear equation.
The primary part is you can describe it as R plus CX.
And so R is a random nonce.
X is the private key.
And C is this thing called the challenge hash.
And the challenge hash takes the public key, the message, and a commitment to the nonce.
And so it's just these three components, R and CX.
And what's cool about this is, let's say you had a participant generate a Schnorr signature with their nonce and their private key, but they use the same challenge hash as another participant.
And participant B does the same thing.
When you add these two equations together, the r's will sum together, so you get r1 plus r2, and the CX1 plus CX2, you factor out the C, and so you get this sum of the nonces plus the challenge hash times the sum of the private keys.
So they aggregate really nicely.
And this is very similar to what we see in Music, how we sign in Frost uses very similar properties where we're going to add these signatures together, the nonces are going to combine, the private key shares are going to combine, and it's just going to form into a standard Schnorr signature.
To do that, the participants have to exchange these nonce commitments in advance because they have to sum their nonce commitments as an input into the challenge hash.
So they exchange these nots commitments, and they do their signatures with their private key shares.
And then they add the partial signatures together, or some aggregator does.
And boom, you have a valid Schnorr signature.
One thing we do differently in Frost than MuSig is because these are Shamir shares, we need to add a Lagrange coefficient because we're doing Lagrangian interpolation.
A simple way of thinking about this is, like, if you have a line, there's, if you have two points, there's only one line that goes through those two points,
And if you are given the two points, you can use Lagrange interpolation to get back to the line.
And so without going into too much detail, we have to do this interpolation.
And by just simply multiplying the private keys by a Lagrange coefficient.
You add everything together, you get a valid Schnorr signature.
Now, on the privacy question, there's some interesting properties of Frost that lend themselves to having some privacy where some signers may not know the transaction details.
So imagine a collaborative custodian setup where you have a client and you have a server and they each have a Frost key share, but the client doesn't want the server to know their entire financial life, how much Bitcoin they have, the transactions they're sending, what, you know, Bitcoin they're receiving, they want to blind the collaborative custodian from knowing those details.
One interesting thing is when we use BIP32 tweaking with Frost, the tweak can be added by the aggregator.
So the server needs to have the tweaked key in their challenge hash, but they don't actually have to add the tweak to their private key, they can just perform their partial signature without the tweak, and then they can send it to the aggregator, and the aggregator adds the tweak at the end.
So that gives us one building block where we can have the wallet owner is solely responsible for the chain code and never tells the server what the chain code is, never tells the server what their key tweaks are.
And so yeah, the server knows the root frost public key, but they can't find any of the child keys without the chain code or any tweaks to derive child keys, which means they can't derive any addresses, which means they can't find any transactions on the blockchain with respect to the chain code.
Now, you still have this problem that the server could recognize its own signature on the blockchain.
And also, it has to figure out how to compute the challenge hash and the nonce hash.
There's a paper that was published earlier this year called concurrently secure blind signatures.
And there's this primitive called a Schnorr blind signature, where basically a signer can get a blinded message and return a blinded signature, and then the requester can unblind it, and the signer can't recognize their own signature, and it doesn't really know what they signed.
This paper adds a cool idea, which is a predicate blind signer, which is if the signer, you can also attach a zero knowledge proof to the blinded signature such that the signer can verify any arbitrary predicates.
So the signer might need to enforce certain signer policies, maybe for compliance or maybe for security.
Maybe they're going to enforce time delays, or whatever it is that, whatever signing policies they need to enforce, they can do so by virtue of this zero-knowledge proof.
So basically, The signer knows the signing policy is passed.
They don't learn anything else about the transaction.
Now, this requires additional work, because the paper that we have is not built for Frost or any kind of multi-party construction.
But my team is actively working on adapting that protocol to work with Frost so we can have this really nice collaborative custodial privacy.

## Cool Features

Speaker 0: 00:17:29

Wow, That's really cool.
So predicate blind signing for anyone that wants to look into it more, which is super new.
Okay, so I've got a bunch of questions for everyone now, so feel free to jump in.
The first one is I want to start talking about some of these bells and whistles that we get with Frost.
Are there any that you all think are particularly interesting, ones that can maybe change the overall user experience, not just for multisig in the context of self-custody, but for applications outside of that use case?

Speaker 2: 00:18:06

I can take this one.
So Jervis alluded to this earlier.
So one cool thing about Frost shares is they're Shamir shares.
And there's a whole line of academic research that deals with cool things we can do with Shamir shares under these domains of proactive secret sharing and dynamic secret sharing.
So one of the things that you can do with Frost is you can refresh, you can rotate your key shares without changing the secret.
So like Jervis was saying, we don't need to move funds on chain, incur fees or link UTXOs together in a single transaction.
And there are protocols for adding and removing participants also without having to move funds, and even moving the threshold around, increasing and decreasing the threshold without having to move funds.
So now, imagine a setup where you have a two of two frost wallet between a phone and a server, and then later you decide you want to add a hardware wallet.
Or maybe you want to add a tablet,
Or maybe you want to add a tablet or maybe you want to add a laptop and you have this really flexible setup that you can change around but you're not having to incur transaction fees to make these configuration changes.
So that can be really useful.
And this is kind of, you know, this stuff, we don't have all the formalization and security proofs that we'd like.
So I'm kind of getting into some more theoretical areas that still require more work to get done, but as long as we're kind of wildly speculating another interesting cool thing you can do with frost is nesting frost in musig.
So this can be interesting in the lightning context, where you have a lightning channel that consists of a 2 of 2 mu sig between the channel counterparties.
But what if somebody wants to have distributed security for their key that they use to sign channel updates.
Rather than just treating Lightning as this kind of hot wallet that you only wanna put some spending cash in, but nothing beyond that.
We could kind of ramp up the security, potentially, by having one of those two or either of those two music public keys that is used to instantiate the channel could be a frost public key, an output from a frost DKG, meaning that either of those lightning counterparties could have a 2 of 3 under the hood or any arbitrary T of N split for their side under the hood because we're nesting a frost key or two frost keys inside the music setup.
And there's a bunch of issues with getting consensus around the channel update and dealing with the revocation key and is the nesting even secure at all, and so on and so forth.
But there is this theoretical possibility that I think is pretty exciting.

Speaker 4: 00:21:30

So I want to touch on the first thing you said.
These first set of bells and whistles, creating a dynamic multi-sig, it's really useful in self-custody, but it's even more useful in off-chain protocols, particularly side chains.
So in side chains, we have this one problem of we want to make the federation dynamic.
So for those who don't know how sidechains work, there's usually a multi-sig.
You deposit your Bitcoin onto this multi-sig and get minted some sidechain equivalent of Bitcoin to some address.
And what we like to do is to expand this federation and to also reduce it.
If someone lost their key in the federation, we like to replace that person.
So traditionally how sidechains do this is either two ways.
One way is really bad, which is to maintain different wallets with different signatories.
This starts to get really complicated because there's no bound to the number of wallets here.
What if you need to spend a bunch of UTXOs across all these wallets?
Now you need to track these signatories, and it can get really messy.
The other way is to slowly sweep the UTXOs onto the newer wallet that has the updated multi-sig, which just costs a lot.
Frost is really nice here, because now we get to dynamically change the federation and we don't need to do any on-chain activity.

## Frost vs Bells whistles

Speaker 3: 00:22:53

I have maybe a bit more conservative view on this because I would make, at least today, state of today, a rather big distinction between FROST and the bells and whistles, because for FROST we have multiple papers that prove its security in different ways.
We have a relatively easy security model which defines what exactly we want to achieve.
We want to achieve a threshold signature scheme.
Whereas the bells and whistles, I agree the applications are really cool, but we don't really have a good security proofs or even definitions what these bells and whistles actually are, what we want to achieve and what we can achieve.
As far as I know, correct me if I'm wrong, there exist papers in the literature that solve parts of this grand unified bells and whistles theory of frost.
They only solve a part of it and only in relatively restricted models.
So for example, they assume that the adversary is semi-honest, whatever that means.
Or they say that your threshold in this T of N setting must be Below a certain number which is a big restriction on how people usually think about Frost because they assume that there is some honest majority in your in your group of Frost signer and this is why I think at least right now there is this distinction but that doesn't mean that maybe tomorrow or maybe it already happened yesterday or the day before someone came out with a complete specification of what we want to have, including all the security proofs, et cetera, that you just need to implement, and then everything is fine.

Speaker 2: 00:24:58

Yeah, and one thing is that there are separate protocols for all these different things.
There's a refresh protocol, which is completely different than the enrollment protocol, which is completely different than threshold increase, threshold decrease, and they all have different schemes and different levels of proofs and modeling and assumptions.
And then we have these other schemes that try to combine them all into one kind of grand, secret resharing thing, where you just have a single protocol that can do all the stuff.
And that has other assumptions and limitations, and some of them work with bivariate polynomials and not univariate polynomials.
So we have to think about, can we adapt them and sum them?
So I think some of these are on a little bit more solid ground than the others.
And also, some of them we have good proofs with the passive adversary model, but not the active adversary model.
But we think there's some pretty straightforward ways to at least work with the refresh protocol and the repair protocol.
And so that is our current focus, but we're working towards kind of getting all the bells and whistles that we would like.
And we do think that there's a path towards that, and we just need to continue doing the work to figure that out.

## How to use Frost

Speaker 0: 00:26:38

Thanks for bringing that up, Jonas.
I think it's important.
It's easy to get excited about it, and I'm very optimistic, But we do have to keep ourselves in check a little bit.
Next question is, so you guys have convinced me that Frost is cool.
I want to shift it now to how can we get Frost into the hands of users?
What are some things that developers need to be aware about when they're trying to bring Frost into their projects.

Speaker 4: 00:27:10

So how can you use Frost today?
There's a number of different libraries.
Jesse has his own library.
I'll let you pitch that.
I've been using and testing and supporting the Zcash Foundation's Frost library, which is also written by the Frost authors.
At Botanics Lab, when we were looking at implementing Frost, we were looking at really a unified interface for both DKG and Signing.
We didn't wanna do these in two separate libraries.
We didn't wanna duct tape a solution together.
And Zcash is really, sorry, the Zcash Frost library is a really good solution to that.
The only problem was it didn't support taproot signatures.
So over the last couple months, we've been working with the community to add taproot support.
If you don't know, I'm sure most of you are familiar with taproot.
The signature scheme is slightly different.
Uses x-only public keys.
And tweaking is a little bit complicated.
Jesse mentioned the bib32 tweaking.
We also needed support for additional tweaking.
So this is, you kind of think of this as like a nested operation of tweaking.
And at the end is your taproot tweak.
So all that stuff we've been working with the maintainers of this library to add that in and we're almost there.
It's gonna be included in the next release so check that out.

Speaker 3: 00:28:31

I want to mention we started this discussion by splitting Frost into these two parts, key generation and signing, and there exist two BIPs, draft BIPs right now in the Bitcoin space.
One for key generation, that's the chill DKG BIP that I mentioned, and then one for signing, which is written by Sif2R.
A shout out to him, he cannot be here today due to visa issues, he should be here instead of me.
And So these are draft BIPs right now.
So what would help would be if people would look at these BIPs, see if they understand them, and try to implement them.
Both of these BIPs have reference implementations written in Python.
Both of the BIPs should be almost complete.
The Childik GBIP is missing one feature that we're currently working on, and it's missing test vectors.
I believe the signing BIP has test vectors.
So one next step to move this forward is to work on these BIPs. Then there are also implementations, like you mentioned, the Zcash implementation, Jessie has implementation for the trusted dealer mode mainly.
That needs more review.
It's written in C.
So I think if people want to review that, then help would be appreciated as well.
What I would also like to mention is that frost signing except for the Lagrange coefficient that Jesse mentioned is very similar to music signing And music does not have a key generation phase, really.
Or at least it's much, much simpler than the Frost one.
So one natural step, if you think, OK, maybe I should use Frost in my product one day, is to take this intermediate step and use music today, because for that we have, I believe, much better implementations, much more mature and also mature BIPs. And you can also do threshold signing with music by using the taproot tree.
So you can do a T of N also with music using music and the taproot tree.
So this would be one way to move towards this ideal future where multi-sig wallets are actually indistinguishable from normal payments.

Speaker 1: 00:31:14

Yeah, I think I wanted to sort of like highlight sort of the significance of Childe KG as a BIP because as Jonas mentioned, if you read the base protocol paper, it kind of, It does not prescribe a lot of things, things like secure and authenticated channel.
And so developers are just kind of like left to go figure out what that means.
Zcash has a great piece of documentation on how they're doing it.
But even that has a bunch of nuances to it over the adversary model.
That Jonas also did a bunch of work with, I think people have Tim Ruffing, and sort of like teasing out a little bit more.
And what they put together, Jilt-TKG is really this complete thing that has all of what you need prescribed and kind of takes care of a lot of kind of very hairy potential vulnerabilities, if you will, in a DKG implementation.
In fact, when we looked at DKG, that's pretty much what we rooted a lot of our initial explorations around, just kind of like taking a look at ChildiKG.
It also kind of, I believe the OLAF paper, which was sort of like, came before ChildiKG, kind of simplified some of the communication rounds required.
It took it down from sort of like two down to one.
And so yeah, I think the chilled EKG dip is gonna be pretty significant for moving Frost forward for the community.
So definitely go look at that.

Speaker 2: 00:33:05

And by the way, if anybody is interested in seeing what this might actually look like in a self-custody wallet, The BitKey team just posted a blog post in a white paper.
You can check it out at bitkey.build.
And we have a design for a 2 of 2 wallet with this upgrade path to the 2 of 3, with some of the privacy stuff we've talked about, some detail about how we implemented secure channels.
So that should kind of help give a better understanding of what this is actually going to look like in a fully embodied form, and the features and the kind of benefits that we're going to be able to deliver with the technology.

Speaker 0: 00:33:56

All righty.
So we've got one more question and then we actually might have time for questions if anyone in the audience has any.
So before we close it out, what are some cool projects that are currently using Frost or working on getting it into production?
I think we know the answer to that.
But also, anything that hasn't been mentioned that we Frost-ophiles should be watching?
Or did we just talk about all of that?
Well, you can plug Botanics.

Speaker 4: 00:34:27

Yeah, check out Botanics.
We use Frost and we're really cool.
We'll save you fees and we'll protect the privacy of the Federation.
And also check out BitKey.
These guys are awesome.

Speaker 1: 00:34:42

Sorry.
So Jesse mentioned we published something, and obviously this is us kind of like putting our best foot forward with reviewing pre-existing literature to try to apply, try to get to a user experience we want to deliver to our customers.
And we're also seeking feedback, so this is completely wrong, and if Jonas is going to open a paper and complete Dash All Dreams, it's perfectly okay.
Like that's part of the exercise.
So yeah, That's what we're kind of asking the community as well.

Speaker 3: 00:35:22

Yeah, we've talked about a lot of exciting things already, like the blind cosigner, multi-sig lightning where you can split up your key into a frost.
I think that's that's all super cool multi-sig wallets like core for example is or Bitcoin core There's a PR to Bitcoin core for for music so it's not completely out of the question to assume that one day there will also be a pull request for Frost.
At Blockstream, part of the motivation for this research is for federated sidechains or like these large multisigs because in Liquid in particular, the spending policy is an 11 of 15 and we have a lot of UTXOs and It's actually quite expensive to spend these UTXOs. So it would be much cheaper if it was just a single public key and just a single Schnorr signature.

Speaker 2: 00:36:31

Also, you can do silent payments with Frost.
If you look at the silent payments BIP, there's like a little footnote about that.
So that's another cool application.

## Wrap Up

Speaker 0: 00:36:44

And Froster, Right?
Frost on Nostra, Nick Farrow's project?

Speaker 5: 00:36:47

Yeah, the Harvard site.

Speaker 0: 00:36:48

Yeah, yeah.
So you can do it there too.
Alrighty, I think that's it.
So we've heard it over and over again, but you have three pieces of homework now.
Thanks for coming.
Number one, check out the chill DKG BIP.
Number two, check out the Frost Signing BIP.
And then number three, check out Bikki's new paper.
Do we have any questions?

Speaker 1: 00:37:13

Questions from the audience.

Speaker 6: 00:37:19

Do you envision any way that Frost could be used as like a coin join alternative to get privacy again with transactions?

Speaker 4: 00:37:35

I think those are pretty discrepant ideas.
Like usually when you do your coin join, you don't want to give up access to your coins.
You will register your inputs and your desired outputs in this privacy preserving way, but you don't give up access to your coins.
That would be a really bad property of the coin-join protocol.
So yeah, I really see those as two completely separate ideas.
Yeah.
Gotcha.

Speaker 5: 00:38:02

Yeah, Thank you.

Speaker 7: 00:38:07

Let's have a question, just one more project that anybody interested might be, want to go check out.
So Mr. Cool Guy of the Fetiment project did a frost and then a roast signing module implemented for the Fetty Mint system that does Nostra notes.
I think it was inspired by the froster that Nick Farrow did.
So if you're interested in one, seeing how a Fetty Mint model is structured, but then also how Frost and Roaster was implemented in that.
That was another project to go check out.
Thank you.

Speaker 5: 00:38:56

Oh yeah, I don't know if you could talk at all about some of the issues in the original Frost paper.
Some of the issues in the original Frost paper.

Speaker 3: 00:39:10

Just to clarify, why?

Speaker 5: 00:39:15

Because I know that there was changes to Music and related and actually I can ask later if it's...

Speaker 3: 00:39:23

I mean it's a good question.
The original, it's true, the original Frost paper had two issues.
First of all, there was no proof of knowledge of the public keys Which resulted in a key what we in the Bitcoin space typically call a key cancellation attack Where you choose your public key to be the negative of someone else's public key.
And when you sum them up, then that some other person isn't there anymore because the sum is zero.
So you can cancel someone else out.
The other problem was that the original Frost, they proposed a two-round scheme, but they did not do the nonce delinearization technique using nonce coefficients and nonce hashes that we use today for frost and today for for music so it didn't work in the concurrent model and that was not in the concurrent setting and that was not pointed out in the original Frost paper, so you could say that was vulnerable, but it was fixed, I think, like six months later.
People pointed it out relatively quickly.
The version that was published in a, or in a conference journal, that one didn't have security issues as far as I know.
But it shows that proposing these cryptographic protocols and even having a security proof for it.
The original version of Frost also had a security proof.
It does not imply necessarily that it's actually secure.
So their proof actually Has this what they call heuristic step?
So there's actually a missing step in the proof and that still exists today and therefore there exists the follow-up papers, for example, the Olaf paper that Jervis mentioned that that also provides a proof and then shows maybe more convincingly that the frost is secure.

Speaker 1: 00:41:47

In that case, let's give a big round of applause for this fantastic panel.

Speaker 5: 00:42:00

You
