---
title: "#MPCbros vs #TeamScript Debate"
transcript_by: Bruno-Simoes via review.btctranscripts.com
media: https://www.youtube.com/watch?v=4oCwbRCuF7I
tags: ["musig","covenants","taproot","miniscript"]
speakers: ["Rijndael","NVK","Rob Hamilton"]
categories: ["podcast"]
date: 2023-07-31
---
# #MPCbros vs #TeamScript Debate

**NVK**: Hello and welcome back to the Bitcoin.review.
Today we have a very interesting show.
It's going to be a knife fight.
Two men go into a room with one knife.
One comes out.
On my left side, Rijndael for Team MPC, weighing 64 kilobytes.
On my right side, Rob for Team Script with variable sizing, so we don't know.
Is this already a loss?
We don't know, let's find out.
Hello, gentlemen, welcome to the show.

Rijndale (**R**): Hey, how's it going?

Rob Hamilton (**RH**): Thanks for having me.

**NVK**: Just so you guys know, there is a bit of a delay already, I can see.
So we're going to work with that.

## Team MPC Primer

**NVK**: So guys, well, let's start here with Rijndael.
Can you please give us a little bit of a primer on Team MPC?

Rijndale (**R**): Yeah.
So, you know, something that you've been able to do in really complicated and convoluted ways for years with ECDSA is you've been able to do what's called multi-party computation, where you have multiple actors or multiple devices work together in order to create a shared public-private key pair and then sign transactions.  
This is really useful if you want to have segregated signers or have other kind of multi-party protocols like Mercury Wallet uses state chains.  
But now that we have Schnorr signatures in Taproot, we have really easy and straightforward signature aggregation, which means that you can do things like have a multisig, a threshold signing scheme where you have T of N signers required to spend some Bitcoin, but it all squishes down to a single signature on-chain.  
And so it's more private, it's more space efficient, and we can support new protocols that would have been either too cumbersome or too expensive or too difficult to do with Bitcoin script.  
And so we all need to embrace signature aggregation and lean into multi-party computation protocols for all the cool stuff we're going to build on Bitcoin.

**NVK**: Hey, but is MPC even Bitcoin?

**R**: I mean, MPC is a general class of algorithms and protocols, multi-party computation.  
There's MPC outside of Bitcoin, but we can use MPC to do Bitcoin things.

**NVK**: Oh, so it's not Bitcoin?

**R**: It's still Bitcoin.

**NVK**: Oh, I see.  
Well, we're going to find out.

## Team Script Primer

**NVK**: Mr. Rob, do you want to give us a primer on TeamScript?

Rob Hamilton (**RH**): Yeah, TeamScript has a rich, deep history in Bitcoin starting in block 170 when Satoshi paid Hal Finney.
It's very the grub brain equivalent of just you have a key, you present a public key and then you present a signature for it.  
And it's so beautifully simple.  
That's TeamScript, baby.  
Just one key, one element on the stack, and it works.  
And it's been around since the start of Bitcoin.

## Simplicity

**R**: Hold on.  
No. So, hold on.  
No, that's not Team Script.  
You just made the case for Team MPC.  
If we wanted to do threshold signing in Bitcoin, right now you have two options.  
You can either do script based multi-sig with OP check multi-sig and we should explain what that means in a minute.
Or now that we have Schnorr signatures, you can do signature aggregation and in signature aggregation, you have one public key, one signature, and you check it, and that's it.  
It's like the purest expression of Bitcoin.  
Rob is trying to get everybody to put multiple pub keys on chain and multiple signatures on chain, and then use a for loop and counting to figure out whether or not your spend is allowed.  
It's insanity.

**RH**: This is just your typical MPC, MPC, you know, rhetoric.
It is absurd.  
Yeah, okay, you can do even more things.
And that's what makes Bitcoin programmable money, right?
You could put many things on the stack and you can do different things.  
And that's what's so beautiful about it.  
OPEC multisig just works.
And it's a beautiful thing because it's all sitting there on chain.

## Auditability

**RH**: Here's something that we really in Bitcoin, we really value the idea of auditability, right?  
With MPC, you have this weird concocted security scheme that exists off chain, and then you don't even know who actually signed at the end of the day.  
You have no verifiability, right?  
You want to actually have accountability of who actually signed that signature and you lose that all with MPC.

**R**: Yeah, but I mean on the other hand, you know, if you have auditable, recognizable setups on chain, then one of two things happens.  
Either you have to use one of the really common script setups, so you're either doing single-sig or maybe you're doing two of three or a small number of people do three or five, or you end up standing out like a sore thumb because if you build some really interesting time decaying multi-sig or if you end up building some really exotic 13 of 15 multi-sig because that's what makes sense for you as an individual or an organization, then that ends up being very identifiable on-chain because there's nobody doing it.  
So another thing that's nice about Bitcoin is that it's pseudonymous and ideally just spending your bitcoins doesn't immediately identify you on-chain.  
And if you have all of these really exotic key hierarchies in your redeem script, then you're just calling out to the world.
You know, here I am, I'm making this transaction right now.

**NVK**: Yeah, but see, you guys are just blabbing now.
You know, I want to I want to hear use cases here, real world use cases, none of this Miniscript Pi dream.

**RH**: What are you even talking about? Miniscript yet?  
Miniscript is it's all other things.  
So like I said, you know, you want to understand how Team Script works.  
It's live today.  
It's in Bitcoin Core, you know, Block 170, you know, Satoshi sent money to Hal and that's how bitcoins work for a very long time.  
This is a really great point too, **NVK**, talking about pipe dreams here.
Rijndael, what wallet it's out there right now, you mentioned Mercury wallet.
But like if I wanted to do on chain MPC, like what does that even look like right now?
It sounds like it's a whole pipe dream to me.

**R**: Well, I mean, you don't even know because, you know, you can't identify those spends on chain.  
So they could be happening right now and you would have no idea.

**RH**: Oh, cool.  
So like the, but what wallet can I use to actually do this?

**R**: You know, maybe we should like take a step back and explain.

**NVK**: That was a good punch.

**RH**: Yeah, talking about pipe dreams, man, like every single wallet I can, Sparrow uses scripts, you know, Spectre uses scripts, all of the hardware wallets uses script.  
Like it's all live.  
Bitcoin Core uses script.

## Interactivity and nonce management

**NVK**: Let's talk about interactivity.

**R**: Yeah, let's let's talk about interactivity.  
So, you know, the way that Bitcoin script works, if you have to go and set up a multi-sig, right?  
So you need to pass around a bunch of XPUBs and use that to have everybody come up with script pub keys that you're going to lock your funds to.  
And then when you go to spend those funds, then you hopefully are making a PSBT and you pass that around and everybody signs it.  
In a MPC world, it's a little bit more involved.  
In order to create the script pub key that you're going to lock your funds to, you have to generate a shared public key.
And this works a little bit differently in FROST versus MuSig, but In general, everybody generates kind of public key shares and passes, pass those around.  
You add them together.  
And then when you want to spend funds, you pass around non-commitments, you partially sign your transaction, and then you pass around those partial signatures and you add them up.

**NVK**: This sounds complicated.

**R**: Yeah, but you know, like we have software.
Software is really good at automating complicated things.
So this isn't something that a human would have to do.
This is something that your wallet would do.

**NVK**: Yeah, but how is bunker coin people in their bunkers in a cave gonna do this on the wall with chalk?

**R**: Well, they're not gonna be spending their Bitcoin, so it's fine.

**NVK**: That's then a good point.

**RH**: Yeah, and then, so I feel like we kind of skipped over a huge piece here, right?  
Because with the output, like first off, output descriptors streamline the script redemption path, right?  
It's very well understood now that if you have an output descriptor, you have the necessary information to recover your money.  
Whereas there's a word, like the key word in this whole MPC architecture is the nonce, right?  
You mismanage that nonce and you could have an attacker on the inside and money gone, right?  
Interactivity, like that's multiple rounds of signing and interacting with each other.  
And those are just, you know, I like to call it foot gun as a service.  
As it's just finding a bunch of different ways that you can just make money gone.  

**NVK**: You know, we can do this.  
You know, we had a whole episode on FROST where I think we can store nonce securely and not repeat them.  
I think it's possible.

**R**: Yeah, and the danger is something for protocol designers to figure out, right?  
Like we used to have nonce problems with just normal single-sig Bitcoin before, and then we standardized on using deterministic nonces.  
In multi-party signature aggregation protocols, you don't want to use deterministic nonces.  
Instead, you want to pre-commit to them ahead of time by sending around hashes of your nonces so that you can ensure that people haven't changed them after they've seen your nonce.
But this is a solvable problem.  
It's solved in the specs for both Music2 and for FROST.
And you just need to follow the spec when you implement it.
It's just like writing a Bitcoin wallet.  
If you implement ECDSA and you're just doing pay-to-witness pubkey hash and you decide to just use the same nonce over and over again, then money gone.  
Right?  
Like nonce mishandling.

**NVK**: Didn't blockchain.info had that problem?

**R**: Yeah, exactly.  
Like nonce mishandling is just a problem with digital signatures.  
So no matter what you're doing, you have to be careful with your nonces.

**NVK**: For people that don't know, it's a number once.

**R**: But I mean, getting back to something that Rob said, right?  
So I mean, if you're using a complex script to manage your funds, then you need to handle the availability and durability of your Redeem script.  
And output descriptors are a handy way to encode that.
But now you have this extra metadata that if you have your funds in a three or five multi-sig and you only have three of your keys, but you don't have that output descriptor, then money gone.  
So in either case, there's like some additional metadata that you have to keep track of or money gone.

**NVK**: One part that I don't like about the interactivity is that it has to happen.  
You have to share those nonces at some point.  
Normally, you'd say when you do the setup and you have to store them securely unless we have deterministic nonces.

**RH**: Well, you have to store them securely and then there's the metadata you then need to keep track of right as the nonce counter, right?  
So if you start a signing process and you decide to, you know, halfway through, like rotate out, like then you necessarily need to increment your nonce because, and the reason why specifically this is important is that if you have a malicious person in your MPC arrangement and nonces start getting reused, they can start unilaterally signing and taking over the money, removing the security because it's only one public key on chain.  
So because of that, if they get enough information leaked out from the other parties, they have enough information to construct a malicious transaction and broadcast it to the network.  

**NVK**: Have anybody been working on resolving the nonce issue, the unique nonce issue, like maybe deterministically like we do with standard script or something else?

**R**: So you don't want to do deterministic nonces, but people are playing with different mechanisms to not make it be its own round.  
So if you read the FROST paper, for example, the way that it's written is you do nonce commitment as a discrete step.
So if the three of us were doing a FROST key signing, we would trade nonces and then once that's done, then we'd move on to the actual signing step.  
There's ideas that folks are working on.  
Things like, when you do a signing, as part of that message, you also exchange the nonce commitments for the next signing.
So you always are ahead by one.

**NVK**: So you ratchet it.

**R**: There's also implementations where when you trade nonce commitments, you don't just trade one nonce commitment, you actually pass around a big bag of nonce commitments.  
You say, I have 100 nonces from Rob.  
And then when we do signing, we just indicate which index we're using.  
So there's engineering ways that we can reduce this so that it's not two steps every time you have to sign a transaction.

**NVK**: So what you're really saying is that this is really cool, We have some ideas, but we're not quite there yet.  
We're just waiting for some very smart Galaxy Brain to email the mailing list saying, ha ha, I figured it out.

**R**: I don't even think it's there.  
Like, I think I think people are implementing it, you know, right now.  
And it just takes some time to get built and get tested.

## MuSig

**NVK**: Okay.
Didn't BitGo add MuSig too?

**R**: They did.  
So BitGo is responsible for a large portion of value transacted on the Bitcoin network every day and their enterprise customers can start moving over to MuSig2, which is pretty cool.  
We should probably say that FROST and MuSig2 are different.  
Maybe, just to take a step back for people who aren't familiar with the terminology, FROST is a threshold signing scheme, so when when you think of Bitcoin multi sig traditionally, that's called a threshold scheme, where you say I have N total keys and I need to sign with some threshold, T of them. So I have three keys total, I need to sign with two of them. I have five keys total, I need three of them. I have 999 keys and I need to sign with 998, whatever that is.  
That's threshold signing.  
FROST is a scheme using Schnorr signatures where you can do threshold signing, but it all collapses down to a single public key and a single signature on chain.  
So even if you're doing a 998 out of 999 multi-sig, it's still just a 64-byte signature on-chain and a single public key.
So it looks identical to a normal single-sig Bitcoin transaction and it takes the same amount of space.  
MuSig on the other hand is confusingly what in normal cryptography is called a multi-signature, which means that it's n of n.  
So it's 2 of 2, 3 of 3, 5 of 5, 100 of 100.  
People probably have heard of MuSig before because I think it's what we're going to end up using for Lightning.  
So Lightning channel is normally a 2 of 2 multi-sig, but it'd be great if that channel open was actually indistinguishable from a normal single SIG Bitcoin transaction.  
So that's using MuSig.  
Another use case for MuSig is this BitGo thing.  
So BitGo, if you're like an enterprise customer of theirs, you can be in this two of two wallet where one key is cold and one key is hot.  
And it takes signatures from both of them in order to move the money.  
And normally with script-based multi-sig, you just see these two of two Bitcoin transactions on chain and using MuSig, it's indistinguishable from a normal single-sig transaction.  
So it just looks like a single key signed.

**NVK**: Do you think the biggest driver for them was the privacy or was on-chain fees?  
Because the fees were getting pretty high.  
And traditionally, like, you know, a lot of the Bitcoin brokerages and big enterprise, like they don't re-pass those fees to customers.  
So on, actually, no, on the BigGo case, it's coming from the customer's wallet, So they are paying the fee.  
So maybe they were complaining to BigGo that BigGo was overpaying fees and spending their money.  

**R**: Yeah.  
I mean, it could be, especially if you have a transaction with lots and lots of inputs.  

**NVK**: Miners.

**R**: Yeah, miners or exchanges where they've been taking lots of little deposits and then they need to do a consolidation.  
You have to provide a valid witness for every input in a transaction.  
So if you're doing a transaction that has 300 inputs and each one of them is a 2 of 3 multisig or a 2 of 2 multisig, then for 300 inputs, you're putting 600 signatures on chain and either 600 or 900 pub keys on chain.  
Versus if it's MuSig, Then if you have 300 inputs, you're putting 300 pub keys and 300 signatures.  
So it like literally cuts your cost in half.  
If you can do this key aggregation.

## Shitcoin use

**RH**: There's another context here, though, for the reason that like a BitGo and all these entities use MPC.  
There's a third option, Rodolfo.  
It's shitcoin tech debt is what it is, is all the other coins.  
They can have one solution that wraps up all of the different cryptocurrencies, whereas they can't use Bitcoin script because they're all unless they're a fork of Bitcoin, they don't use Bitcoin script.  
So they're actually incentivized to support all of this because it supports all the other coins.

**NVK**: Do you think that their MuSig implementation support shitcoins?  
I'm not sure, because we know Firebase, which is the other essentially half of the market for enterprise Bitcoin and Shitcoin solution for the exchanges.  
They use a type of MPC that has nothing to do with the coins.
It's just how they secure the keys, essentially.  
The BitGo, I didn't read the specifics,
I don't even know if they released the specifics,
I wonder if it's useful for the Shitcoins.  

**R**: Well, like if you do, so there have been some MPC EDSA wallets, like I think Coinbase has one in their custody offering.  
And those are actually useful for other coins that do ECDSA.  
So like, Ethereum, right?  
You could do it that way.  
Not a lot of other coins do Schnorr signatures.  
The Ethereum ecosystem is leaning really hard into BLS signatures because they're more useful for ZK snarks.  
So, MuSig doing Schnorr signatures is actually not quite as specific as Bitcoin script, but that is pretty peculiar to Bitcoin.  
That's not going to be portable to lots of other things.

**NVK**: That's what I thought.  
By the way, BLS signatures, aren't those new and shiny and shouldn't be used yet for something like that?

**R**: They rely on bilinear pairings, which is like much newer cryptography.  
I think one of the things that the Bitcoin ecosystem is very conservative about is relying on new cryptographic assumptions and pairings are a new cryptographic assumption.

## Signing schemes

**NVK**: Hey, we have Adam back chiming in here.  
He's like, I'm not sure I'd put MuSig FROST in the same category as MPC constructs, which in my opinion, complex for agile risk of crypto implementations mistake.  
The Demgard-Jurek-based ECDSA construct is a bit complex in itself, though, while not generic MPCs, so similar critique for that.

**R**: Yeah, I mean, like MPC is like a really general term.
And I think Adam's right, which is that MuSig and FROST are much more, I'd say, constrained and much more tightly defined than a general MPC signing scheme.  
In a really strict sense, they are a multi-party computation, but they are very strict and tightly defined.  
One of the things that was interesting about FROST is FROST actually came with a security proof, right?  
So like we have a proof that FROST kind of reduces down to the same cryptographic hardness assumptions that we normally rely on for Schnorr signatures.

**RH**: Yeah, I mean, there's an interesting point here too, just to briefly talk about Schnorr signatures, is that they were originally around and available during the Bitcoin white paper, but it had a patent on it.  
So when the patent expired, they were able to do the part of that upgrade.  
So it was already tech that was ready to go and people wanted, because it has these better aggregation properties.  
But talking about the general, like you're right in that specifically MuSig and FROST don't really benefit other coins, but MPC as a concept in the industry has been put forward, TSS, Threshold signature scheme as a way to like have one security stack which secures everything, which on August 10th at the Black Hat USA conference is gonna be a whole breakdown of how the open source rust in GO language implementations of TSS are actually broken.  
And with one to two rounds of signing ceremonies, a malicious actor can break the threshold signing.  
And this is what I'm getting at, is that it's not secure.
Just be a grug brain, put the pub key on chain, and it's gonna be okay.

**NVK**: So guys, I mean, like, you know, it's kind of interesting that like we have like a wrench thrown in here, which is Taproot and the capacity of having all this in the same vehicle.  
So maybe there is a path in which we can address both?

**R**: Yeah, I mean, so the thing that's really cool about Bitcoin script, right, is there's a bunch of operations that we can do in Bitcoin.  
So we can check signatures.  
That's like the foundational one.  
That's the bottom of everything, right?  
We can also compare values.  
And like one of the value comparisons that's really useful is you put a hash into your script, and then you provide in the script witness a value, and you say, does this value I provided hash to the same thing that I committed to in my script?  
And that's called a hash lock.  
We can also do time locks where we say, is the current block later than the current block height or has so many blocks passed by?  
And those are time locks.  
And we can combine these things together and compose them together.  
And one of the things that's cool is that Bitcoin script, especially in a post-Taproot world, if you compose a script and you say, I want these coins to be spendable.  
If this signature is valid and it's been 15 blocks and you provide the pre-image to a hash, it doesn't really care if that signature is generated from a single key or from a bunch of key shares that then have been added together.  
And in fact, you can't you can't tell.  
So you can actually use a FROST or a MuSig key as part of a larger script.  
So that's really helpful.  
Like, you know, NVK, you asked for use cases a few minutes ago, if you wanted to do a time decaying scheme where you say, pubkey A is good now, but pubkey B is going to be good in three months.  
And maybe that B pubkey is like a different person, or maybe if you're using FROST, pubkey B is a FROST key with a smaller threshold.  
And so now you can do sort of a time decaying multisig where you say, I've got a three of three, but it, you know, decays to a two of three, and then it decays to a one of three.
And you can express that progression of time through different script paths.  
And then either, and then your choice is, do I just want to put all the pub keys on chain and pay for the bytes and pay for the privacy?  
Or do I want to go through a little bit of complexity when I do signing and have it all be a single key?

## Switching sides

**NVK**: So since, you know, everything can be done together now with Taproot, why don't we switch sides here and make each other's points?  
Rob, how do you save MPC from losing this battle?

**RH**: Oh, MPC.  
This is a really incredible point here, is that every single time you want to rotate out these signers, it's an on-chain transaction, right?  
But with MPC, you can actually use FROST and you can rotate out who is your two of three without having to do an on-chain transaction.  
And this is how we get to scale Bitcoin, right?
We get to scale Bitcoin because we get to compress data on chain.  
So we are not taking up as much block space so we can make room for the entire planet to get on boarded.
And further, Let's say the two of us are in a two of three multi-sig and then NVK, you go off into the Canadian woods and you have a boating accident, we can rotate and kill your share of a key and recompute the polynomial such that we can have this without having to move funds on chain, it could be myself, it could be Rijndael and a third party, right?  
We'll have Johnny come in and be the signer.  
And that scales because it doesn't require an on-chain transaction, but we provably can kind of outright do this rotation and change who's holding the key material without ever having to interact with the chain.

**NVK**: Well, this is through
Roast, right?

**R**: Roast like makes FROST more asynchronous and more robust because like one of the things that Rob you know, left out when he was painting this rosy picture of a post FROST
future for us.  
It's so easy to leave out the details, but you know what, Rob?
Details matter.  
You know, something that Rob left out is that in this key signing ceremony that he's constructed with FROST, If you have a malicious signer who just decides like, you know what, I'm just going to hang up partway through the signing process, then you force everybody to have to just like start over again.
And if you're doing two of three, that's not a big deal, but if you're doing a really high cardinality threshold, then it can actually be really disruptive because you have these interactivity requirements.  
And maybe if one of the signers is running bad software, you can actually force them to reuse a nonce because they think that they're still part of an old signing session.  
So what Roast does is Roast makes FROST robust against, you know, signers going away or refusing to cooperate by basically running a whole bunch of signing sessions in parallel.

**NVK**: Is somebody mowing their grass?

**R**: Yeah, that's me, sorry.

**NVK**: Nice.

## Multisig vs single sig

**NVK**: OK, guys, so I think we we get to a point here where I still defend the fact that I don't think, you know, FROST is ready, but I don't think anybody does.  
We did a whole FROST episode, which people should really listen to.

**R**: I mean, one of the things that's just great about Script, is you can do multi-sig constructions in Script today.
They work.  
The auditability point is a good point.  
Like something with FROST is if you wanted to do, let's say it was like a three of five, and all of a sudden the money moves, you can't actually look on chain and see who signed for it.
Whereas with like a script based multi-sig or having a script path, you could.  
So, you know, in that in that scenario that Rob just painted for you, like he and Johnny might might go and steal all the money and, you know, you won't actually be able to prove that they're the ones who signed for it.

**NVK**: You know, thinking just sort of like pragmatically here in terms of enterprise, it does look like having multi-sig with some of those keys being FROST is more interesting because now you can have sort of like groups, right?  
And the groups are provable in chain.  
So at least you have some auditability on the signing that happened.

**RH**: You know, technology moves over time and progresses and there's evolutions, right?  
Just because today we don't have these things doesn't mean down the road we're not going to be able to do this.  
And I want to build for a bright orange future where everything is a single-sig on chain.  
Don't have to worry about it, right?  
Like it's just, like there's no need to do all the complication stuff.  
Like it's just adding extra pieces on chain.  
And if the chain doesn't lie, you have much more flexibility to kind of orchestrate all of your security procedures off chain because that's not dealing with the consensus mechanisms.  
And it's much easier to get to a scalable final answer if it's all just being done off chain and you put as minimal information as possible on chain to actually execute your transaction.

## Covenants and transaction introspection opcodes

**NVK**: Question for you guys.  
Do you guys know what the new wallet from Block uses on their, cause they have some kind of like threshold signing in terms of like spending capacity.  
So that means to me that they must have something or is that just like business logic?

**RH**: To my understanding, it's a two of three, right?
You have a key on the phone, you have a key on the hardware wallet and you have a key in the server. And to my understanding, it's a two of three logic.  
And then the server is able to implement, you know, kind of business logic, right?  
And this is like a whole point about being able to govern some rules off-chain is you can have certain spending limits, right?  
You could have frequency of spending and amounts of spending and the server is able to enforce that to help protect users.

**NVK**: Okay, so it's just a standard multi-sig.

**R**: Yeah, we don't, There's been a bunch of conversations about covenants all over the place, including on this show.
And something that would actually be really great is if we had some transaction introspection opcodes.  
Because like one of the things that you cannot do today in Bitcoin is you cannot say, I have a one Bitcoin UTXO, half of it needs to go left and half of it needs to go right.  
If we had enough of a covenant to be able to do output introspection, to be able to look at the amount and the script pub key of the outputs of a transaction, then you actually could send to a pay to script hash type output that said, only this amount or only up to this amount can go to these addresses or can go anywhere if I sign with particular keys.

**NVK**: You know, it gets even more interesting, right?  
You know, if we had a way for transactions to know the amounts, you could have a time locks on thresholds, which really, really makes stuff interesting, right?  
Because now you can have spending velocity, which is like one of the most useful things that HSMs offer.

**R**: Absolutely.  
And you could use this all over the place where you say, hey I've got my mobile wallet, and this is exactly a spending velocity use case, But just to say it for the people who are still awake, you know, hey, I've got my mobile wallet and I can spend up to, you know, $100.  
But then I need to co-sign with my hardware wallet if I'm spending above that.  
You'd be able to do that and have it actually be enforced at the consensus layer of Bitcoin if we have covenants.  
So like that, that's the kind of thing that we could do if we had something like CTV.

**NVK**: But you know that The current Covenant proposal, UpVault, does not...  
Well, I mean, they did expand UpVault to have CTV as part of the package, didn't they?  
And CTV does provide the capacity of this introspection.

**R**: I think you might be able to do something similar with APO.  
There's a trick to be able to get the transaction hash on chain.  
And then I think if you have Opcat, you could construct the transaction in your script and then do a comparison.  
But it's a lot more moving parts.

**RH**: Doesn't Opcat bring recursion back?

**R**: I don't know.  
And frankly, I don't think that that's actually a bad thing.  
People get freaked out about recursive covenants and they say, Oh my God, this is going to turn into Ethereum.  
I think the original sin of Ethereum is actually global state and reentry.  
It's not recursion.  
Because we can have boundary recursion.  
We have script op limits.  
So we could do a similar thing.  
I don't know.

**NVK**: Well, they don't have UTXO, so they can't really go to any grid in there.  
They have to check the whole script to know what the account balance is.  
Just the amount of computation you need for that.
I feel so bad for the exchanges that support Ethereum and all its contracts.  
I don't think people appreciate how insane it is to keep balance.

**R**: Yeah, I mean it's pretty nuts because the way that all these token contracts work.  
So like if you have either an NFT or like a fungible token in Ethereum, the way that it works is like your account doesn't have a balance of that token.  
What happens is that tokens contract has a little hash table that lists account IDs and then the token balance.  
So if Rob wants to know his account balance, what he has to do is he has to look at every token on chain and then see what his balance is with that token and then add it up.
So it's this big scatter gather.  
So what ends up happening is a small number of entities run giant indexes that just invert that index.  
And instead of saying, what's your token balance per contract, they say, what's the token balance per account.  
And like, that's why, you know, all these Ethereum wallets hit like the same API endpoint because they have to build this giant index and track the whole thing.  
It's absolutely insane.  

**RH**: I was looking at Bitcoin Optech, as I often do to go deep in the weeds on stuff.  
And this is where another option of TLOV, right, becomes an option, Tap Leaf Update Verify, where you actually can have amount introspection become part of the logic of the tap leaves for like, how you're spending things and looking here, it says it would require an additional op code.  
But then you would be able to do this too, which is basically a different approach of trying to have this covenant like feature.  

## Taproot

**R**: And I mean, like just kind of pulling it a little bit back more towards what we were talking about earlier, right?
Like the thing that's so cool about Tapproot and Hopefully if people are still awake, they understand this about Taproot.
The thing that's magical about Taproot is Schnorr signatures and then mast.  
If you have a really big, complex Bitcoin script, usually the way that most contracts or most protocols work is it's like, okay, if everybody agrees that this is what we should do with the money, then we should just do that.  
If not everybody agrees, then there's a bunch of conditions and there's a set of 'ors' between them.  
If we don't all agree, then Rob gets the money if he can provide the pre-image dish hash.  
Or Rijndael gets the money if he can sign with a particular key.  
Or NVK gets the money if it's been six months and nothing else has happened.  
That's a common way to construct complex financial transactions.  
And so what you can do with Taproot is you can say, all right, we're going to take all of those script paths.  
So like Rob does the pre-image, Rjindael does a signing, or NVK just waits until a timeout happens.  
You take those three scripts and you put them into a Merkle tree and then you take the root of that Merkle tree and you add it to a pub key, that would be like if the three of us took all of our pub keys and added them together and got a single pub key out of it.  
So if we aggregated our keys together, then that's the we all agree case.  
So if all of us agree and we just sign, then that's a key path.
If we don't sign, then we descend into this Merkle tree.
And so you can have the happy path of it's just a normal check sig as the key path, And then if you need to descend down into the tree, then you only reveal the script component that you're actually using.  
You only pay for that in terms of block space, and you only reveal that in terms of privacy.  
And that's Taproot, right?  
And it's a way that you can do all of these things.

**RH**: It's the best of both worlds.  
And additionally, something that's may not fully understood with Taproot, they actually got rid of `OP_CHECKMULTISIG`.  
Because `OP_CHECKMULTISIG` is a for loop and it's very computationally inefficient.  
Whereas in Taproot to do a multisig, you do `OP_CHECKSIGADD`.  
And then you just add up the signatures and either it's a zero or a one.  
Is it a valid signature or not?  
And then you get to the end and you compare it to what your threshold is.  
So it's computationally more efficient as well.  
And additionally, with the Schnorr signatures, you can, as we mentioned earlier, since you're using Schnorr signatures in Taproot, you can have a single public key on chain and it's actually its own aggregated `T` of `N` behind the scenes using FROST or an `N` of `N` using MuSig too.

**R**: It sounds like the real like best case scenario is that we actually build a tree of script leaves for the different spending conditions that we want and then within those script trees, those individual leafs, we use aggregated signatures to save space and to make it more efficient to check.

**RH**: That sounds like a reasonable compromise.

**R**: Yeah, so why don't we do that?

**NVK**: I don't want to hear compromises.
Just kidding.  
For the folks listening, I'm having a terrible fucking connection here.  
It's hard to keep track.  
So anyways, guys, it's fascinating that we went like everywhere and also like managed to cover a lot in only 45 minutes.  
Where do we go from here?

**R**: What's cool is that with Taproot, we can construct addresses and construct wallets where in kind of the happy path, when you're just spending your money, it just looks like a single SIG on chain.  
And whether that's actually a single key behind it, or if it's like a FROST or a MuSig aggregation, nobody really knows or cares, except for you, it's just your business.  
But then if you want to do something really complex, like you want to have a time decaying multi-sig or in a post-covenant world, if you want to have amount-based spend conditions, or want to have key hierarchies that have hash locks or timelocks attached, then you get a script and you only reveal that script when you actually spend it.  
I think one of the problems, in addition to just this stuff is complicated to build, is that there's a handful of exchanges and wallets and Bitcoin ATMs that don't support pay-to-Taproot yet.  
So If Rob goes off and builds a really kick-ass Taproot wallet that has all these really advanced features in them, but people can't get their coins into it, out of Coinbase, then a whole bunch of people aren't going to use that wallet.  
It's going to be a big question about whether or not Rob wants to lean on those features in the first place.  
I think something that we need to do is we need to get exchanges and other service providers to support pay-to-Taproot like today.  
Taproot came out more than a year ago and it's a few line changes for most people to be able to support pay-to-Taproot.  
They have to be able to correctly parse bech32m addresses.
There's a website called [whentaproot.org](https://whentaproot.org/) and it lists which exchanges support Taproot and which ones don't.  
That doesn't even mean receiving Taproot, just pay-to-Taproot.
It's literally a two or four line change.  
So I would encourage everybody to like go on that website, find your exchange, and if they don't support pay-to-Taproot, you should open support tickets or blow them up on Twitter and say, when can I withdraw my Taproot wallet?  

**RH**: Yeah, just to name and shame, the remaining ones are Binance, Binance US, Bitfinex, Coinbase, Crypto.com, Fireblocks, Gemini are really like the big ones left.
Venmo and PayPal too.  
But to your exact point, there's a very different architecture requirement to like receive Taproot because you need to have all that code.  
But just to send to a Taproot adjust, it's just checking a checksum.  
It's not involved code and it doesn't incur tech debt or complications to being able to custody and manage funds.

**NVK**: I mean, but like, guys, we don't like, I mean, that's that's important to have.  
But like, you know, this is not like, you know, the thing holding us back because, you know, most people who are playing with these features and, you know, companies were playing these features, You know, these users will probably have a hop in between the exchange.  
They're not going to send from their exchanges to whatever they're going to do directly.  
By the way, we see sometimes people paying from an exchange to an invoice and can take a day or two for the exchange to process the payment out.  

**R**: Yeah, it's nuts.

**NVK**: Yeah, So like, I don't think that that's the bottleneck.  
I think the bottleneck is just that like this shit is complicated.  
And I don't think people are seeing the like 10x, 100x sort of like immediate magical upgrade in UX or in price or in anything really.  
And that's sort of like what's really holding people back.

**RH**: Well, I think it goes to just starting to build out these features, right?  
In that, I mean, I directly like was starting to mess around with a mini tap script.  
The reality though is to Rijndael's point, like to build a wallet that can't receive funds from Coinbase makes it like a hard wallet to interface with.
It's not everything.  
And I think part of the path forward is leading by example and having these features available and being able to show a better way of doing things and then kind of setting a standard to have people want to try and catch up to try and improve user experience.  
And that's the thing is that end users, like just someone who's just holding their Bitcoin, they bought some Bitcoin.
They don't care about all the fancy expressiveness, but it's our duty as people that are building in the space to try and show that they don't even realize like the possible upsides and being able to support these features and just being able to make it be the first mover, get it out there, get people playing with it.  
And then over time, kind of like shifting the mindset of what's possible in Bitcoin and leading by that feature set.

## Adoption of new features

**NVK**: I mean, to me, what really is going to drive this home is, you know, somebody out there makes a very cool app, phone wallet that does something that is interesting and new and sort of like super efficient somehow or does something that was not possible before.  
And everybody wants that feature for whatever reason.
And that's how you get it.  
Like that's how adoption gets it.  
It's like something goes in the market that's just like remarkably better than everything else.  
And then everybody starts switching to it and starts like, I wanna put my stuff in it, right?  
That's how you get the demand to happen.

**RH**: Very fair.  
Yeah, that's hopefully some of the stuff I'm working on right now kind of starts doing that, having Bitcoin have more flexibility in doing different things.  
You're not going to see these upsides if everyone's just doing NMM multisig, Because NMM multisig is good enough with pay to witness script hash, right?  
So you need to start kind of expanding the design space without doing a soft fork, right?  
Like there's 117 opcodes that are active right now in Bitcoin out of the original 256.  
Like the mini script stuff I'm doing, like uses like 20 of those op codes to try and do some really interesting things.  
But I've started rotating out of being a mini script influencer into now being a paid to Taproot, back 32M influencer, just to get, I went back and forth with Coinbase.  
I had to go through four levels of support just to have their specialist support team tell me that Taproot was enabled in November of 2021 and they still don't support it.  
So just getting like gently nudging them on that side while also putting out good products that make people want to use these advanced features.

**NVK**: So like on the custody side that like, you know, it's like sort of a companies.  
Why is it that Nunchuk, Casa and Unchain don't have it?  
Because they would be to me the first, sort of like non, they assisted more company-like kind of entities that would be the first people to have more interesting Taproot solutions.

**RH**: So for Casa specifically, Nick Newman was on the Galaxy Brains podcast And he said specifically the mini script stuff is really interesting as an added feature set.  
So I think they're starting, they've already like, I don't know if they're actually at the second building on it, but it's definitely caught their attention.
And I think people are now just starting to realize this opportunity.  
So it's gonna, there's gonna be a little bit of a lag because companies have roadmaps and obligations and deadlines of existing things.  
So you have to go into some sort of like quarterly sync up of like, what's the next set of features you add for the next quarter, right? So there's gonna be a little bit of a lag because companies have roadmaps and obligations and deadlines of existing things.  
So you have to go into some sort of like quarterly sync up of like, what's the next set of features you add for the next quarter, right?  
So there's gonna be a little bit of a lag, but I see, you know, a year from now, there's gonna be multiple companies that are gonna be implementing this for more advanced custody use cases that better empower users to manage their money on their own terms.  

**R**: Well, and like, you know, we have Liana Wallet, which is doing a bunch of stuff with Miniscript, mostly for either an inheritance use case or like a backup key use case, right?
So after some time lock expires, you get to use a different key.  
And I'm pretty sure right now that's all just like normal, you know, pay to Segwit, pay to like Witness Script Hash.  
I wouldn't be surprised if in the not too distant future, they end up like moving to Taproot, because I don't think, you know, those users are gonna want to reveal their whole spend policy every time they do just a normal happy path spend.  
I think we're going to see a lot of stuff like that, where people start with Segwit, ScriptHash encumbrances using Miniscript or using something else.  
And then they end up moving to Taproot because it gives them more compact and more private spends.  
And then as MuSig gets more widely available And as FROST gets finalized, I think we're going to see people start incorporating those also.  
Like Nick Farrow has a project to actually do like a FROST hardware wallet on like commodity hardware.
It's like super early.  
You know, we'll see how that goes.  
We talked about, you know, some MuSig deployments that are like already seeing production right now.  
I think it's just very early for a lot of this stuff, but I'm cautiously optimistic that it's going to start rolling out.

**NVK**: The challenge that I see with something like Liana is that essentially UTXO rotation is a no-go.  
So it's like dead on water.  
So until we can overcome those issues, it feels like just sort of like jerking off.

**R**: The thing that would be useful, because in order to solve that problem, you have to do one of two things.  
You either need to have a server that does key deletion and you do a vault setup with pre-signed transactions, or we need covenants that support vaults.  
Whether that's OpVault or something else, if we had an actual covenant opcode then you don't need to do UTXO refreshing every six months or something.

**NVK**: Hang on a second, you can't do server key deletion, right?  
That's pointless because it's not provable and it doesn't end well.  
I mean, realistically speaking, at least in my view, we can't move on from this impasse until we have covenants.
On-chain.

**R**: I think that's right, but maybe this is just helping prove out demand.

**NVK**: Nobody's going to use it if they have to rotate their UTXOs.

**R**: Yeah, that's probably true.

**RH**: So this is an interesting third way, just as opposed to key deletion or waiting for the protocols to get updated.  
I've been debating usability of this, where you can use nLockTime to basically pocket a pre-signed transaction, and then you can auto broadcast like the refresh later.  
So you just said as a quick, just quickly explain.  
So just to quickly explain the difference though, is that like at a script level, like you, you encumber the, like, like using op check sequence, verifier up, check, lock time, verify.
Those are at the script level tied to the UTXO, whereas an nLockTime time lock is locked to the transaction level.  
So just for the people at home, for the one or two people still awake, is that with an nLockTime, it's almost using NLockTime for a time lock.  
It's almost like having a check and post-dating it.  
So if I wanted to like send Ryan a check, I can say like, oh, this is only available in December 31st of 2023.  
So it's sitting there, it's ready to go, but then it can't be broadcasted earlier.  
And then you sequence that so that it's before the time lock threshold expires.  
And then you can just auto broadcast the transaction hex then.
And the network won't look at it until it's ready to actually be broadcasted.

**R**: You're delegating the interactivity requirements to somebody else, right?  
So instead of you having to come online and rotate all your UTXOs every six months, you say, like, all right, I'm gonna have the server rotate all my UTXOs every six months.

**RH**: Yeah.  
No, you do have an interactivity because you have to actually hit it to the network when it's ready to go.  
You can also have paid services though, that like provably, like when they broadcast it, you know, you could find some sort of ways of monetizing where I think Pablo built something like this where he would hold your UT your transaction hex for you and then it would broadcast at the set time and he'd get paid over lightning or something to be able to like manage that service and Then you can give it to multiple services because you only need one person to actually successfully broadcast the transaction for it to work.

**R**: Sure.  
I mean, like the real answer is covenants, right? 
But I think we, I don't know, I hope we don't end up in a chicken egg scenario where people who are pro premature ossification say, oh, we don't need this because look, nobody's using wallets that would depend on these features.  
But then nobody wants to use those wallets because we don't have covenants.  
That's the and egg scenario that we're probably going to end up with.

**NVK**: Yes and no.
Because you're going to get a false negative, because nobody's going to use this wallets that required UTXO rotation.  
So I rather not have the false positive than to simply say, you know what?  
Like we believe there is demand and you know, we're gonna build it and we're gonna UASF it.  
Wait, did I just say we're gonna UASF?

**RH**: You did.

**NVK**: Confidence?

**RH**: You did.

**NVK**: Oh boy, did I just start something?

**RH**: Yeah, that's gonna wake everyone up if they were asleep.

**NVK**: Yeah, no, I really think that it's ought to be done at some point.  
I just, I think we need to see something that essentially everyone feels overconfident about in terms of a proposal.  
And then I think the gears are going to start to move.

## Covenants

**R**: I mean, it's kind of funny that it's like an accident of history that we don't have covenants.  
Like, you know, We turned off a couple of opcodes, otherwise we would probably have the kind of functionality that we want.  
Or the one that I think is always funny is we have, for folks who are APO fans, like we have Sighash_none, but we don't have Sighash, you know, any prep out.  
And so it's very like asymmetric.  
And I think if you were designing all the Sighash flags from a blank sheet, you would either have both of them or none of them.  
Like it's weird that you can commit to an input and not an output, but there's no way of committing to an output and not an input.  
Like it's very asymmetric.  
And so I think It's strange that we don't have covenant mechanisms in Bitcoin.

**NVK**: I don't remember, my memories already failing on this, but I don't remember any opcode that was deactivated that could have done something like that.  
But this is way, way back or any sort of like work on anything like it in the Satoshi days.  
There was OpEvol, but there was a disaster and there was Gavin.

**R**: So there's a trick to get the signature of the current or the hash of the current transaction onto the stack.  
And then if you have OpCat, you can construct, like, here's what all the outputs should be, here's what all the inputs should be, and then you hash it and you should get the SIGHASH.  
Right, so like you can use that to do like a really basic covenant.

**RH**: Yeah, and for all of these different opcodes, I usually look to like, and we talked about this on the Bitcoin script project, like episode that we did with Alex, like there's almost like a, like a two dimensional, like the kind of the feature richness of a given opcode and also like how production ready it is.  
Like, is something like a white paper or is it actually like implemented code, right?  
So CTV, like Jeremy has all that code sitting there, right?
Another one that's related to all this is like ChexSig from stack is already in the elements.  
It's like the block stream chain, right?  
So like it already has working reference code that could be audited, right?  
And then you go out further on the end, like simplicity where things just get so many diffs and so complicated, right?
It's a much wider swathing thing.  
And I think the idea I think should be, it's incumbent on people that are looking to try and like push the edge here to champion their solution and put it forward.  
And I think like what James is doing, like with OpVault, it's a great concise way of like a very straightforward functionality that I think no one would disagree that they wouldn't want to ideally have some sort of warm staging area before your funds just go out wildly, into the ether to someone else, right?  
Like there's a lot of opportunity.

**NVK**: I think stuff like elements kind of does a disservice, right?  
Because it's amazing stuff, amazing tech, no doubt.  
But the problem is it's like, almost 100,000 diff, right?
Like it's not gonna get merged period ever.

**RH**: No, no, you would never have to merge everything.  
Like there's a difference between like simplicity and everything versus like just OpCheck sig from stack.  
Right, Like you can take a small chunk of that whole thing.

**NVK**: I don't think you can.

**RH**: Okay.

**NVK**: Like if I remember right, like with Elements, I think was what we're an offhand kind of thing.  
And if they wanted to split a little part off, it would be like a whole other sort of like project to try to get that in.  
It's not, if I remember, it was not that simple, but it's been a while since I looked.  
But anyways, like my point is like, you know, I think, I mean, it's very hard to get everybody behind a single standard, right?  
I mean, XKCD has the best cartoon on them.  
So I don't know, but I have a feeling that the trend is changing and even folks who are pro-ossification like me are sort of like, you know, we need something.  
Yeah, I'm hopeful.  
Guys, is there anything else that we sort of like forgot to explore in the knife fight between MPC and TeamScript?

## Roundup

**RH**: I think we hit everything.  
I'm not sure if there's anything that you had, Rijndael, on your side.  
This has been a very fun shit post war to have something fun to actually talk about in the bear market as opposed to price models.  
I'll say that it's been, it's been a real, it's been a pleasure being in the knife fight with you.

**R**: Yeah, thanks.
You too.  
Yeah, I mean like maybe, maybe just the thing to hit is that, you know, if you can actually have both, right.  
So if the thing that you're trying to do with your script is express optionality or time or possession of some other secret value, Then you're going to use a script construction for that.  
And then for the actual threshold or multiple key part of it, today, Bitcoin script is kind of what we have.  
It's what's widely deployed.  
It's what we have code for.  
It works.  
But there's constructions for doing key aggregation that work.  
We have software for it, they just haven't found their way into many wallets yet.  
And so as that happens, we'll be able to get cheaper, more private transactions that we can also build new, better protocols on top of.  
So being able to compose things together because they think it's just a single signature.  
So it's probably not actually an or.  
The future is probably Bitcoin script and key aggregation, not Bitcoin script or key aggregation.  
But yeah, Rob and I were just really tired of the Bitcoin Twitter drama.  
And So we wanted to start a new drama.

**NVK**: Yeah, I mean, I really that was that was very refreshing.  
Very high signal posts with proper memes, too.
It was it was very expertly executed and I hope it continues.

**RH**: It will continue.
This isn't over.

**NVK**: Please don't stop.
We need competitive green checkbox tables, comparison tables.
Those are always winners.

**NVK**: Yeah, like, I think necessity is going to drive covenants and the stuff home.
Because when we get to the next ultra high fee environment, I don't think it drops to the levels that are in now.  
I think it's going to be something that's going to be a wake up call to people.  
Especially if we have like a third world country, high populated people sort of starting to actually adopt Bitcoin either via Lightning or on chain.  
I think shit's going to get weird.
And the Lightning companies, they need to close those channels, right?  
So they are going to be pushing a lot of the stack too, because it's in their interest to make the block size, the block space be used more efficiently, even by the people not doing Lightning, or they're out of business.

**RH**: Absolutely, yeah.  
And then the covenants to unlock things like coin pools and sharing UTXOs, it just makes it more feasible because like the scaling conversation is, you know, you have a set throughput that we made in the block size war of how many transactions can be in a block.  
We weren't going to increase the block side and ruin the decentralization of the network.  
And so because of that, now you need to find other creative ways to allow people to have a way to claim on-chain ownership of funds.  
And your options are, have it all sit in custodians, or do we build better cryptographic primitives that give some level of security assurances on chain?  
And it gets really interesting.
And just before I forget, just like a huge shout out.  
We mentioned the FROST episodes every time.
So huge shout out to Jesse Posner and all the work he's doing with FROST.
Specifically, fingers crossed that getting merged into the SEC 256k, like ZKP library later this year is like one of those bedrock things that allow the application layer devs like myself to actually be able to start going in and playing with these primitives and starting to push through these user experiences and wallet experiences that can push forward better ways of using Bitcoin.

**NVK**: Well, I mean, if it's not on LibSec, it's not going to get used.  
Like that's to me the threshold these days on how I look at some of this stuff.  
And not even the ZKP, right?  
We're talking about like actual mother LibSec.
Mother LibSec is essentially, I think, the best sort of heuristic of like, should be used, should not be used.  
And it's like sort of like nice to have things like that because it prevents people from losing money.

**RH**: And everyone uses that same library.

**NVK**: Yeah.
That's right.

## Trident

**NVK**: Yeah, it's very cool.  
Rob, do you wanna like tell us a little bit about Trident and what you're working on?

**RH**: Yeah.  
So Trident is the name of the wallet I'm building at AnchorWatch.  
Trident, a great name by my co-founder, Becca, was like the idea of multi-pronged security, right?  
And we're leveraging MiniScripts specifically.
Right now we're using pay to witness script hash to be able to embed more interesting custody array dimensions on chain.  
And the whole crux and first of all, we're trying to build is actually having a product that we can actually underwrite risk for to provide insurance.  
Because today in the custodial landscape, you have custodians that charge management fees and maybe they have one insurance policy that's covering all of the customers.  
But if there's a catastrophic loss, you're not really on the hook for anything, right?  
So if you're gonna have to give up your key somewhere, like having better like legal financial protections to actually identify you in the case of a loss, which has its own kind of backend complexities, but The tech part that's really interesting is using these more advanced scripting arrangements with TimeLocks, right?  
And we can use, for the length of your insurance contract, let's say, we at AnchorWatch are a required signer.  
And then when the insurance contract expires, you can just go and take your money.  
So you don't have to worry about calling a custodian and saying like, hey, can I get my money back?  
And then, you know, the other person on the other side of the phone is like a Prime Trust or an FTX or a Celsius.  
Right, you don't have to like, this is a way of like, giving the on-chain auditability to show for a fact that your funds aren't being moved around maliciously and that you're ultimately able to get access to it.  
So like it's a different way of kind of expanding the design space of how Bitcoin gets used today as programmable money to ultimately better serve customers.  
Our primary focus are gonna be commercial entities at first, but you have the Wizardsardine guys, which are using Liana wallet, which is kind of similar idea for more robust backup situations.  
And the ideal state is moving this also all over to Taproot.  
Our whole tech stack is built on Bitcoin Dev Kit, which is really a superpower in so far as having a really strong set of primitives built on, I'll use the right term, Crust Bitcoin and crust Miniscript.  
And having these like baseline level tools which are really robust, And when it becomes a conversation around like, hey, we wanna add coin controller.  
Hey, we wanna add, you know, Tapscripts.
Like we're not re-architecting the entire tech stack from the beginning.  
And most of it is very modular.  
It's a very powerful programming primitive.
So just another huge shout out to just the Bitcoin Dev Kit Team, all of the maintainers, Steve Myers, you know, Alicos, Daniel, like Thunderbiscuit, like there's a whole crew over there that are just grinding along and it gets really exciting too.  
And also just like shout out, like another example of like just the power of BDK very quickly is just like the Mutiny wallet guys are, you know, working on BDK and they were able to take their progressive web app and just push it into an Android app because the BDK library has bindings for all of the apps.  
Like, so You can build something in Rust and then you can push it over to Swift for iOS or Kotlin for like Android.  
And you don't have to re-architect an entire different code base.  
So it's an incredibly powerful, robust programming tool.  
And I see a future where like everyone uses the 256 library, like everyone's just going to start using BDK as like a default Swiss Army knife.
So you're not building a wallet in step one, doing elliptic curve cartography and finite field theory.  
You just have everything just works.

**NVK**: Oh, I mean, like, you know, like Bitcoin is becoming complex enough now that like back in the day, I'd say it was already a bad idea for most people to write a wallet.  
Nowadays, it's definitely a bad idea for people to write a wallet from scratch.  
Unless they have some serious, serious people in the dev team that are very specialized on this, which is very few people.  
So leveraging something like this is very similar to leveraging something like LibSec.  
It gives you the correct primitives, the correct way of building the scripts so that people don't lose money because Bitcoin kills you on the edge cases.

**R**: Yeah.  
And the thing that we want to cut out here is undifferentiated heavy lifting.  
So like in Rob's application, the thing that's special and unique about Trident Wallet is the spending policy.  
Like He's not trying to innovate or push the envelope on coin selection.  
So being able to just say, all right, I'm just going to use the coin selection algorithms that come with BDK, he doesn't need to go and become an expert in branch and bound or whatever the new thing is.  
They just use what's in BDK.  
So Rob, in your system, the thing that you were describing of you guys are a co-signer, but then after a time lock it decays, I imagine that you could also do, kind of like a key hierarchy, right?  
Where maybe it's like, Oh yeah, like the, like maybe you guys are always a required signer, but then for one of the other, you know, signatories, like there's some optionality of it's like, it's always you guys, and then it's either like party A or party B, and then it's always two of parties C, D, and E, something like that.

**RH**: Yeah, and this is where it gets really interesting is like in a traditional, just like an event, like multi-sig world, one key represents one vote.  
Whereas with Miniscript, you can break it out and have multiple, let's say two of threes, right?  
So me at AnchorWatch can have a two of three, the customer can have a two or three, you can have third party two of threes.  
And this then means, and that's not a six of nine to be clear, you get to have not only across multiple institutions distributing risk, but individuals within a company or organization, like, you know, in theory, like you could have a Coinkite quorum where like Rodolfo's key must sign.  
And then it's like, if you if you feel spicy enough, you want to let Vic hold a key, Vic can hold a key, but he can't rug you, right?  
Like, that gets like a much more interesting arrangement where you can encode these governance processes of a key hierarchy where in a company setting, you don't want all of the keys to be equal.  
That's insane to have all the keys be equal, but at the same time, you don't want the CEO to be a Single-Sig.  
So you can distribute your risk out this way and it gets really interesting in redesigning and rethinking how does security work in Bitcoin and with organizations, we can have more interesting ways of encoding this.

## Scripts & HSMs

**NVK**: Well, I mean, ideally your script mimics your organization's business logic, right?

**RH**: Exactly.
The process.

**NVK**: The process, right?
Ideally, that's what you have, right?

**RH**: Yep.

**NVK**: But Bitcoin, you know, is Bitcoin.
And, you know, it can't do that yet or it can't do that specifically like that ever, but we can definitely get closer to that.
Maybe, especially with CTV.

**RH**: Yeah, no, definitely with CTV, you can encode all of those spending policies and limits, but it gets it closer rather than having it.  
And I got this like mental model actually talking with Will Cole, like application versus protocol level security.  
Like you could do this on an application layer but then like you can still end run it at the protocol level of Keysleak.  
But if you're able to mirror it.

**NVK**: Yeah.
You can't, right?
Servers get hacked.

**RH**: Exactly.

**NVK**: Like the way, a lot of times, the way these things get done is by breaking the HSMs that have the spending policies, right?
Like that's how you get hacked a lot of times, right?  
Dev keys get leaked and then they go and they change the policies because if somebody can change the policy on the HSM, it means that the bad guys will find a way to do the same, right?
But you can't change a script.  
That's the beauty of using a script as the HSM.

**RH**: Exactly.  
No, that's exactly it, right?  
So when you encode it on chain, you don't have to worry about a server doing the logic at the application layer.  
It's on the blockchain.  
So there is no end running around like, you know, these different processes.  
So you can actually insert the human element, go slow to go fast, so to speak.
You want to be very deliberate.  
And you can put human governance in between these signing processes so you're not just indiscriminately using the HSM with a policy blind signing things as it comes in, and if it gets compromised, you lose your application security.

**NVK**: Let's make every problem be a key security problem, not a computer security problem.

**RH**: Exactly.

**R**: The stuff that we can enforce in script is limited by what we can express in script, which is why we need more complex opcodes.  
But I mean, Rob, that example was probably a really good one because what you guys are saying is, all right, if you have multiple organizations that all have shared custody of some basket of funds, then for your signing, you're gonna rely on whatever internal controls you have.  
Whether those are technical controls, policy controls, a combination of the two of them.
But then you still have some consensus level enforcement of, two out of these three organizations have to sign.  
It might be that within one organization, somebody's able to get escalated privileges and sign a thing that they aren't supposed to, but that doesn't necessarily mean money gone because you still have to have somebody else in another organization sign for it.  
And so you're kind of using multi-sig to control the spend across organizational boundaries, but then you're relying on whatever internal controls people have within XBoundary.

**RH**: That's exactly right.  
And what's really interesting, I mean, at the moment, since we're not using MPC for anything, we can specifically, someone can hand us a transaction, and we're like, hey, your VP of sales signed this transaction, was this supposed to happen?  
And you then know for a fact which key got compromised, which helps just like with audits and governance checks, right, and like having multiple bands of communication to kind of verify these things in a way where you're not ultimately, you know, like this human element is so critical for making sure that you're doing things the right way and you have this audit log, which is the PSBT of what signatures are currently present.

**R**: In a post-FROST world, if you guys did this naively and you just said, we're going to do everything with the key path on Taproot and it just always looks like single sig on chain, then you'd lose that auditability.  
And so if you wanted to keep that auditability, you'd have to do something like have a tap script for each combination of signers, and you'd get kind of the auditability by looking at the control block and like which tap leaf got revealed.  
Or there's a Greg Maxwell idea floating around out there that like You do a bunch of tap leafs and then on each one, you have one of the signers just have their own signature and they act as a coordinator and then you have everybody else aggregate their signatures together.  
So each tap leaf ends up looking like two of two using ChexSigAd, like you were talking about earlier.  
And one of the signatures is an identifiable party.  
And then the other signature is a MuSig or a FROST.  
And so you're literally doing script-based multi-sig, but one of the signatures is actually an aggregated signature.  
And so you kind of get the best of both worlds where it's like two of two on chain, but that second key might be, you know, 15 of 20 or something.

**RH**: Yeah, it gets really interesting too.
So just as a quick note, when you're doing pay to witness script hash, you're committing to the entire script path, right?  
But with the TapLeaf, you're just committing to that TapLeaf.  
So you could have, you know, a hundred, a thousand TapLeaves each with the right common metrics of each different party in theory.
And then you have this auditability to your exact point.  
And then you don't have to worry about someone taking the signature and repurposing it later for something else like you would with pay to witness script hash.  
Cause you're only committing to that specific TapLeaf.  

**NVK**: Would it be a challenge to pre-compute this?

**RH**: That, yeah, that definitely would get more challenging.  
But I'm talking in a future state where the tooling has already kind of been largely figured out.

**R**: Yeah, because like you do you do commit to all of it.  
You have to precompute all of them and then you use the root of the Merkle tree to tweak your internal public key.

## Miniscript

**NVK**: Is there anybody working on some more advanced stuff like this already?  
Like that's like out there as like, you know, prototypes, scripts.

**RH**: So you mentioned earlier, right?  
Nick Farah was working on this new FROST like wallet right now, like starting to get this tooling out there

**R**: Yeah, or you know if people want to see really weird Taproot script construction Programmatically believe it or not the ordinals project or'd like that wallet has like a very unusual tap script embedded in it.  
So if you just want to understand like, what does it look like programmatically to build up a tree of tap scripts and then use that to generate an address.  
That's actually a really good source to go and check out.

**RH**: Yeah, it's a wide open space of opportunity.  
And one last thing that also gets really nice with Tap scripts versus Pay-to-Witness script hash, specifically with MiniScript, you can't have a duplicate public key in the stack.
That means you have to generate many child derivations.  
If you're using a signer, let's say it's a two of three and then it becomes a one of three.
If you have different branches, you can't use identical public keys.  
So the way this works right now is that you can generate a different account for each one.
But if it's all on Taproot, you don't have to worry about a duplicate public key ever happening and you're able to just have it in the TapLeaf.  
So you only have one account that you need to manage ever for a given signing device, which is definitely a better UX perspective and it makes it much more straightforward.  
It's all, yeah.

**R**: I got bit by that.  
Why can't you have duplicate pub keys in Miniscript?

**RH**: Oh yeah, so you can't have duplicate pub keys because within the same script stack, because when you sign it, you can't prove that someone isn't gonna like malleate the transaction and have that signature for that pub key appear in a different branch.
And it also breaks the composability.  
It breaks the, it's a common sub-expression, sub-expression issue.  
That's me just repeating a word that Andrew Pulsar said without me fully understanding the technical ramifications of it.  
Like, that's a good Oracle to use.

**R**: It's usually a good strategy.
Yeah, for sure.

**RH**: But many script policies are also composable, right?  
So that's the idea too.  
I think it breaks down the composability.  
If you have, if I'm say using this pub key in a different branch, like then you start having collisions, especially if it's pay to witness script hash, then like if you're signing, like if the key appears multiple times, that signature is valid for the whole stack.  
So it violates the malleability aspect of things.

**R**: That makes sense.  
Yeah, cause like With Taproot, that wouldn't be an issue because you only reveal just the leaf that you're actually using and then the control block.  
So For the one person who's still listening at this point, the way that you spend a Taproot script is, we mentioned earlier that you take all the scripts that you want to put into your taptree and you make a Merkle tree out of them.
So when you go to spend it, you provide a little data structure called a control block that includes a Merkle proof.  
It provides the sibling hashes all the way up the tree, back up to the root, to prove that the script that you're spending was actually included in that address.  
Because you have this Merkle inclusion proof that commits to a specific location in the tree, somebody couldn't take that signature and like play it in a different branch of the script because you haven't revealed the script.

**RH**: Exactly.

**R**: Yeah, it makes a lot of sense.

**NVK**: Yeah, guys, I kind of got dropped, but I think I'm back now.

**RH**: Everyone's falling asleep, including Rodolfo, who fell asleep.  
Now he's back.

**NVK**: Man, it's hard to do a podcast as a host with bad internet.  
So, okay guys, I guess the last thing here is, Rijndael, what are you working on that you can talk about?

## Team script custody tooling (Rijndael Project)

**R**: I'm working on using interesting Bitcoin script constructions to help people with more interesting custody setups.  
So I'm pivoting hard into TeamScript and working on custody tooling.

**NVK**: Okay, no specifics we can hear about the tooling?

**R**: Not today.

**NVK**: Okay, fair enough.  
Rijndael is a mysterious man.

**R**: That's right.

**NVK**: So, so guys, I mean, listen, thank you so much.  
I mean, we have almost two hours.  
You know, we went from like, you know, having the topic almost finished in 30 minutes, but then, but then not, but then yes, but then not.
I think it was fantastic.  
I think that if people are not sleep to the end, They're going to get a lot of signal here.  
I think you guys did a fantastic job.  
I need to declare a winner.  
And the winner is Elon Musk for rugging my connection again.

**RH**: Yeah, this is a Congrats, Elon.  
You deserve it.  
This was kind of like the emergent shit posting, just like Twitter banter was, you know, dammit, we're going to make everyone learn about Bitcoin.
And that's what was great.  
We started seeing meta memes of people watching the debate and seeing that there's a lot about Bitcoin people don't know about.  
And that's what we wanted to have fun and a nice little drama wrapper, have people start learning more about, you know, how Bitcoin actually works under the hood and getting people to think about like the opportunities of solutions and products that can be built on top of more advanced scripting and MPCs.

**R**: Yeah, you know, I'd love to see more fake drama around really obscure Bitcoin topics.
Like maybe the next wave is maybe we can get some like package relay like meme warfare started.  
That'd be pretty cool.

**RH**: I love it.  
We didn't even talk about the Taproot Annex.  
Like, you know, that's just like.

**NVK**: Or we should dig the version, the original client.  
Satoshi original, original client and start showing all the poker code blocks.

**R**: That would be awesome.

**NVK**: And say that Bitcoin was designed to be poker or something, start some like weird conspiracies too.  
That always helps.  
Listen, guys, thank you so much.  
Any final thoughts, Rijndael?

**R**: No, just, you know, be the memes that you want to see in the world.  
There's lots to do in Bitcoin. So go play with new stuff.

**NVK**: Rob.

**RH**: Yeah, it's a bear market.  
You should be building and learning about Bitcoin.  
You should post about price in the upswings and in the downswings.  
You should post about the tech and then you're always going to be happy in your lane, moisturized, happy, content.  
That's what you want to
be.

**NVK**: Flourishing.  
Yeah, I know my favorite meme of your fight was the one where It's like the frog sort of extended a hand to the guy on the floor.  
And like one guy is like super sad.  
The other guy is like winning.
I can't remember.
It was it was...

**R**: It was like the guy that was sad, it was like drive chain arguments, price things, SEC, all these things.  
And then the guy that was happy was like MuSig, FROST, Miniscript, Taproot.

**RH**: That's right.  
Why in 2023 Are we talking about stock to flow and price model guys?  
Like, let's just move on.

**NVK**: No, I mean, the best part is that everybody is an expert on clawbacks, right?

**R**: That's right.

**NVK**: And now everybody is an expert on superconductors.

**RH**: That's right.

**NVK**: By the way, I am starting a pod, the 
Superconductors.review,
I have the domain and I'm going to have some Bitcoin experts weigh in on the superconductors because Bitcoiners know everything and Bitcoiners are always right about everything.
So...

**R**: And **NVK**, so here's the format for the podcast.  
Every week you come on, you do your intro and then you say, has anybody reproduced the paper?  
No.  
And then you turn off the podcast.

**NVK**: That's that will be very successful.  
I mean, I should add some ads on the beginning.

**NVK**: By the way, that material, the LK99 medium stuff, it's very easy to make.  
You just need a small kiln that sells on Alibaba.  
And I'm certain that people are gonna do it.

**RH**: Yeah, there was like this random guy that had like a like an anime avatar in Russia, and he was like doing side by side separate productions and like it's accessible enough.  
People are just going to start running off and trying to do it.

**NVK**: I support home labs.

**RH**: Absolutely.
The favorite detail, though, I thought you would have picked up on that meme with comparing the two, I posted in the chat here is the Barbenheimer meme.  
You know, you have the pink cold card and you have the black cold card and you have to choose a side, which one are you?

**NVK**: I saw that.
I actually did see that.
That was that was something.

**RH**: That was American Hodl's idea.  
American Hodl said you need to do the Barbenheimer meme with the black and pink gold card.

**NVK**: Where does the glow fit in?

**RH**: We'll have to figure that out.  
Glow in the dark.  
I have to get a glow in the dark one before I can properly assess the vibe it has.

**NVK**: Listen guys, we're going to do this again, either with the next drama or with the expansion of this drama, Because I don't think the Bitcoin script versus MPC drama is ever going to go away.

**RH**: It's never going to go away.

**NVK**: Oh, I just can't wait for the CTV.  
We need some CTV drama.  
Oh, yeah.  
That'll be fun.  
I miss the CTV drama.  
OK, guys, Thank you so much.  
Thanks for putting up with this atrocious connection and my incapacity of participating too much.  
Maybe that's why I made it better.  
So you guys have a wonderful day.

## Outro
**NVK**: Thank you for listening.  
For more resources, check the show notes.  
We put a lot of effort into them.  
And remember, we don't have a crystal ball, so let us know about your project.
Visit bitcoin.review to find out how to get in touch.