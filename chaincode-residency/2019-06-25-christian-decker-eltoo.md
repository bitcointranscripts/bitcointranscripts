---
title: Eltoo
transcript_by: Michael Folkson
tags:
  - eltoo
  - lightning
speakers:
  - Christian Decker
date: 2019-06-25
media: https://www.youtube.com/watch?v=3ZjymCOmn_A
aliases:
  - /chaincode-labs/chaincode-residency/2019-06-25-christian-decker-eltoo/
---
Eltoo: The (Far) Future of Lightning

Location: Chaincode Labs

Slides: https://residency.chaincode.com/presentations/lightning/Eltoo.pdf

Eltoo white paper: https://blockstream.com/eltoo.pdf

Bitcoin Magazine article: https://bitcoinmagazine.com/articles/noinput-class-bitcoin-soft-fork-simplify-lightning

# Intro

Who has never heard about eltoo? It is my pet project and I am pretty proud of it. I will try to keep this short. I was told that you all have seen my presentation about the [evolution of update protocols](https://www.youtube.com/watch?v=HauP9F16mUM). I will probably go pretty quickly. I still want to give everybody the opportunity to ask questions if they have any.

# Off-Chain Protocols

We saw this yesterday already. Update mechanisms basically are some people meet, they lock in their onchain state and they go off and negotiate offchain on what to do with this state. They can renegotiate over and over again. The update protocol makes sure that all of the invalidated states are not applicable anymore. The Lightning penalty mechanism does this by penalizing who is misbehaving. Duplex micropayment channels and eltoo do that by overriding the effects that you were trying to get to by misbehaving.

# eltoo Update Mechanism

eltoo, just some quick notation. I represent outputs as circles and transactions as squares. This is called a funding transaction. It basically takes funds from the green user, let’s call her Alice, and creates a multisig output that is controlled by both Alice and Bob, Bob being the blue guy. From there on all the changes to the state of this output need to be negotiated between the two. What we do in eltoo is basically we attach to this output a settlement transaction called `Settle 0` that reflects the initial state. We could actually drop this one and it goes Alice creates a channel and we settle the channel and Alice gets her 5 Bitcoin back. This timelock which is represented by this clock here ensures that during this timeout we can actually go in and create an update. If we do that we create this update that ratchets this output forward and creates a new place to attach a new settlement that reflects the new state. In this case we have transferred 1 Bitcoin from Alice to Bob. This guy (`Settle 0`) becomes double spent and we can forget about this. We are currently replaying this onchain but we can lift this offchain quite easily later on. We can repeat this over and over again and this is basically already the entire mechanism. When we want to create a new update we double spend this output, this becomes invalid, it will never be able to reach the blockchain anymore. `Update 2` ratchets this forward and opens up a point where we can attach `Settle 2`.

Q - For your updates, when you say you ratchet forward what is that transaction, `Update 1`? Is that spending to a new 2-of-2 multisig?

A - Exactly. This is the multisig that is shared by Alice and Bob containing those 5 Bitcoin. Now we take this update transaction, we spend this output and create a new output that again contains 5 Bitcoin owned by Alice by Bob. The only difference being what we can attach to it. To this we can attach `Settle 1` but not `Settle 0`. The other thing that is particular from this one we can attach `Update 2` not `Update 1`.

We’ve just played this game on the blockchain. We’ve done this on the blockchain and it is really bad. Every time we do an update we create an onchain transaction which is probably not what we wanted because we pay fees every time. We wait for confirmations every single time. We wouldn’t have to wait for confirmations because these timeouts are chosen in such a way that these always gets precedence over this. We can be sure that if both of these are out there `Settle 0` will not confirm because `Update 1` has priority.

Q - If that timeout expires and you haven’t broadcast `Update 1` then you can just broadcast `Settle 0`. So what if you have a channel that doesn’t have a lot of action on it?

A - In the onchain case where we start this timeout right away with the creation of the funding output, in that case yes this has a limited lifetime of anything you feel comfortable with waiting for this timeout to approach. If this is one week probably after six days you should broadcast this. With the actual construction of eltoo we can introduce a trigger transaction in between here that is an update with no settlement. In this case this will stay there and only when we broadcast a trigger transaction will the timeout start ticking. That is how we can make a limited lifetime into an indefinite lifetime.

Q - You’d give an `Update 1` transaction after broadcasting the funding output onchain?

A - The trigger transaction is actually identical to `Update 1`, we don’t have a `Settle 0`. That’s exactly the idea yes.

Now we have this really huge onchain footprint which is kind of really bad. We lift off this protocol and keep all these transactions that don’t have a lock on it and keep them in memory. What we do is basically is we want to have `Update 3` be able to attach to a Settle but we can’t really do that because `Update 1` might be out there and we have no way of attaching `Update 3` to `Update 1` and the funding output. What we proposed and the jury is still out whether people actually want this in Bitcoin, is to have a new SIGHASH flag. SIGHASH flags you probably learnt about last week? Who doesn’t know what SIGHASH flags do? Excellent. SIGHASH_NOINPUT would take a transaction and blank out the reference to what output you are spending. What this does is remove the direct commitment to what funds we are spending and we make it rewritable. I can take `Update 3` and rewrite it to point to the funding output for example. We skip `Update 1` and `Update 2` and go directly to `Update 3` by having this pointer redirected here. The signature is still valid because we blanked before we signed and we blanked before verifying the signature. We no longer commit to the input that we are spending. We have this situation where we have `Update 3` can be attached to the funding transaction, it can be attached to the output of `Update 1` and it can also be attached to `Update 2`. We are in this case here (`Settle 2`) where Bob has 3 Bitcoin and Alice has 2 Bitcoin. I’m Alice, I would like to settle this one (`Settle 1`) or even better this one (`Settle 0`). I will send `Update 1` because that initiates the close with the desired effect that I want. Bob comes in and sees Alice is cheating here, she is trying to get here (`Settle 1`). Bob takes `Update 3` and rewrites it internally to point to `Update 1`. `Update 1` is getting confirmed because Alice was hoping to get this (`Settle 1`) outcome. But Bob has ratcheted this thing forward and double spent (`Settle 1`). By having this forward motion towards the later state that we agreed upon we can ensure that any old effect can be overwritten by a later state. What that means for us is that a honest player should always be able to react to anything that happens whether it is just the funding output or somebody published `Update 0` or whatever. By holding onto the last Update and the last Settle I can always react to whatever happens on the chain.

Q - In the worst case where you may have multiple updates broadcast onchain it is worse than the current way with revocation?

A - Absolutely. With Lightning the unilateral close of a channel is always a two step process. We publish the commitment and we sweep the funds. It ends there. With eltoo it may happen that we replay `Update 1`, `Update 2`, `Update 3` and then go on and on because it is always the other guy whose situation was better. A really neat trick that Rusty found out is that these are single input and single output transactions. So we can sign them using SIGHASH_SINGLE which means that after the fact we can attach a new input and a new output. That way we pay fees. You always have to pay the fees. If all of this were free we could replay all the states. But it is likely that we’ve done ten steps and I’m getting bored because I’m paying fees and I’m not getting the effect I want. I just jump to the last state and I’m done. I want this settled, I’m not going to pay more fees. That is how we penalize misbehavior in the network but it is not penalizing in a way that is as deadly as in Lightning Penalty where all of your funds are lost. I often compare it to a death by a thousand cuts compared to a death by decapitation. Trust me I want a thousand cuts.

Q - ….

A - That is something that took us a while to figure out. We can have a way that `Update 2` is only attachable to anything that has a lower state number. The way we do it is that each of these have a CLTV operation as their first thing in them. This guy (`Update 1`) gets a locktime that is somewhere in the past so we don’t actually have a locktime but we can still compare it with the current state number. What this guy (`Update 2`) does when executing the Script is pull my own locktime and compares it to the state number that is already on the stack from the previous one. Only if that locktime is larger than the state number that was pushed on the stack by the previous one will that be valid. The reason we use locktimes in the past is because we don’t actually want a locktime, we just want to have this comparison between two numbers. Locktimes in the past are immediately valid.

Q - …

A - And timestamps. We have a range. The semantics of the locktime switch over from being block heights to timestamps at a block height of 5 million. We have a range between 5 million and the current UNIX timestamp which is about a billion. We have about one billion updates we can perform with this mechanism with all locktimes being in the past. And our range grows with time so that’s good. One billion is more than any channel has ever done.

Q - …

A - This is a relative timelock such that only when this output is being created then this timeout starts to tick. We have absolute timelocks to ensure we don’t attach `Update 1` to `Update 3`.

Q - …

A - The issue with having the state number in the input script is that the input script is not committed to in the signature. I could go ahead and create an input script with any state number that is going to be higher than the one I’m trying to replace. The locktime is committed to in a signature. That was quite a headache. I’m not sure Russell O’Connor would call it covenants. You usually laughs at my attempts to create covenants. The whole SIGHASH_NOINPUT discussion has started and is a never ending bikeshed. I am trying to stay out of it as much as possible. I just want my fun tools and I don’t care about the actual implementation. People like to theorize about how to make it safer.

Q - …

A - As soon as we touch the blockchain we can reset the whole state. There is no need for us to carry over state from one instance of this protocol to the next one. If I eventually go and use `Settle 1` then I can reuse this output again to create a new instance of this. But since anything that is built on top of this here can never be attached to anything here because that is already settled I don’t have to care about that anymore. In the new instance here we would be using new keys. One of the downsides of SIGHASH_NOINPUT is that it actually makes replay possible. I can take any transaction that has an input that fits some output there on the blockchain, I can attach to that. I call this binding through script compatibility instead of binding through explicit commitment to an output you are spending. It gets us a lot of flexibility, it actually enables all of this. But it comes at the cost that it might be dangerous to use. Some of the proposals on the mailing list are going towards calling it SIGHASH_NOINPUT_DANGEROUS which I find funny but I’m totally fine with.

Q - …

A - Let’s say your wallet creates all signatures with SIGHASH_NOINPUT. You have two outputs that are 5 Bitcoin each on the same address. You want to send me 5 Bitcoin. You create a transaction doing that. I get my 5 Bitcoin using your one output but I can take this transaction, rewrite it and attach it to the other output as well. All of a sudden I’ve got 10 Bitcoin whereas you only wanted to send me 5. That’s how we replay in this case. There are a couple of safeguards that we try to use here. If you switch public keys or addresses that you use then this binding through script compatibility is broken. So I cannot take any of the other funds that do not have the same address or Script. The other safeguard is that we commit to the value. All of these are always 5 Bitcoin and we still commit to the output value that you are trying to spend. If you have a 10 and a 5 output and you send 5 to me I cannot rebind it to the 10. That’s simply because I could not come up with a good reason for making a rebinding that doesn’t change the transaction and all of a sudden the fee changes. The outputs still have 5 Bitcoin but you are now spending 10 so does 5 become fee? That’s kind of weird.

Q - …

A - They should not use SIGHASH_NOINPUT. It is a very dangerous tool but it is a very targeted tool that you should not use if you don’t need. All of these discussions revolve around that.

# To eltoo or not to eltoo

It is kind of simple compared to the sort of “I have this information, you have this information” and we can never share that information. It is completely symmetric. Everybody has the same information. There is no toxic information that might lead to you losing funds. We have no penalty as such. We only have a slight cost if you ever publish an old version which enables backouts.

Q - …

A - The downside of introducing penalties at a higher level. Trust me I tried because penalty comes up often. People like to penalize people by the way. If you ever want to penalize somebody for misbehaving you have to reintroduce this symmetry in state. There must be something by which I can identify that you were the one that misbehaved. This is mixed into this Lightning penalty mechanism where we have different information. The power of eltoo comes from all of this state being completely symmetric and there is no privileged information that I should know and you shouldn’t. I tried reintroducing penalties at a higher level. I have not found a nice way to do so so I usually go with the excuse that fees are punishment enough.

Q - …

A - We can reintroduce symmetries at the settlement step, that’s true. We have two settlement transactions, one for you and one for me. We do have a construction. With a SHAchain we can have revocation secrets that we can generate at will basically. It also has a cleaner separation of layers. What I am excited about is besides being able to put that back into Lightning we can actually create multiparty channels where we as a whole room for example manage a set of funds and we can move them freely between any of us without having to open channels or have multihops between us. It is just a pool of funds that we can rearrange however we want. Then we go into channel factories and all of that stuff but I will talk more on that on Thursday.

The disadvantages are no penalty and we need a change in the Bitcoin protocol which has proven to be a bit more difficult than I anticipated. That is always the case. I spent my whole PhD proposing stuff and no one ever using it. We talked about the proposals at Core Dev. There are two or three variants of it.

# When moon?

At [Core Dev](https://diyhpl.us/wiki/transcripts/bitcoin-core-dev-tech/2019-06-06-noinput-etc/) we discussed the different variants that we could have. One variant is that we add an additional signature to a Script using SIGHASH_NOINPUT called a chaperone signature. The idea is that your transaction is only valid if that transaction also has a non SIGHASH_NOINPUT signature. That way if we are participants in an offchain we would generate a private key and share it among ourselves. We can sign off on rebound versions but nobody else can. That’s a guard against third party malleability. The argument for it is that third party malleability is not desired. It might be weird if somebody is able to rewrite transactions that you weren’t aware was possible. The argument against it is that it is bigger, it is more costly. We need to add an additional pubkey, we need to add an additional CHECKSIG operation and we need to add an additional signature. But also we don’t want to encourage people to use SIGHASH_NOINPUT unless they need this flexibility. There is a difference between handholding all the way or giving fair warning and letting people touch the hot plate and learn on their own. I’m more in the second camp. The other variant is that we should use a different SegWit script version for it, one that isn’t serializable in bech32. So that even if you wanted to only ever use SIGHASH_NOINPUT you couldn’t create an address which to send. In all of these constructions we are always working directly with scripts and we are not using addresses in any of this. By making a SIGHASH_NOINPUT destination unaddressable we make it so that people couldn’t accidentally send money there. That’s the second thing. The third variant is changing the name to _DANGEROUS which I like a lot. We should do that.

Q - …

A - There is an argument for fungibility that has to be made. It is trading off what you care most about. Is it about people using wallets that are badly written or is it about you not being able to differentiate outputs from one another? In a unilateral close you would be able to tell that there was a unilateral close. In a non unilateral close you would. The bad case can be detectable, there is little we can do about that.

Q - …

A - The feeling that I got was that most people want this functionality because people are really excited about building stuff on top. Russell O’Connor is coming up with new interesting covenants that we could do and everybody is telling him not to. The flexibility we gain, from what I feel, is being seen as a net positive. At least the people that were present and discussing there, nobody had strong feelings for any of the encumbered versions. So we might eventually get it, maybe.

Q - ….

A - That’s true. There is an alternative proposal that takes this and mixes up the different variants. This does not commit to the previous Script because the Script actually changes over time. We have this state number that we compare with the locktime so we can’t commit to the Script. There is the other variant, this is being called SIGHASH_ANYPREVOUTANYSCRIPT. The other variant is just SIGHASH_ANYPREVOUT. That still commits to the Script. Those are two variants that are being proposed by AJ Towns. That is a competing proposal but it gets me my functionality so I am happy. ANYPREVOUT is a better name for this so we should probably use that.

Q - …

A - Both propose a bump of the SegWit Script version because we are redefining a new sighash and unknown sighases are an immediate failure if you don’t understand them.

Q - …

A - The point of this stacking multicolored cake I showed at the beginning is to show these are distinct layers that we can replace individually. We don’t have to break compatibility with the rest of the network. This is just our update mechanism. If the two of us agree to use eltoo instead of the Lightning penalty mechanism we can just start using it. Anything that is multihop that goes beyond our own scope, the scope of our channel, namely HTLCs and the onion, those remain identical. The update mechanism is really just a way for us to negotiate adding and removing outputs to the settlement transaction. What those outputs then are, whether they are HTLCs or additional channels maybe, that is all for upper layers. This clean separation of layers enables us to swap out individual parts. We would indeed signal our availability of eltoo in feature bits both in the init and potentially in the node announcement such that if I only implement eltoo I could selectively connect to peers that support eltoo as well.

Q - …

A - Absolutely, yes. By implementing eltoo and using it just between the two of us. Upgrade is a bad word in Bitcoin by the way. By deciding to use eltoo on individual hops we still maintain the ability to have multihop payments stay identical and we don’t break compatibility on those layers at all.

Q - …

A - They are being discussed. I didn’t add them to the BIP itself because BIPs are sort of static and I didn’t want to trace all the different proposals because there have been quite a few by now. I might write an update or add a discussion page where I summarize the pros and cons of individual proposals. I should also mention that we had a meeting in November in Adelaide with quite a few of us here. We laid out the roadmap for the version 1.1 spec and eltoo was purposefully not added to that roadmap. We don’t have a good estimate of if this is going to happen and when. We didn’t want to hold up version 1.1 of the specification for something that might take a few months. This is really the far future of Lightning and I am under no illusion that this is going to happen this year or anytime soon. But it would be cool. That’s me. If you have any questions about eltoo I will be around. I will point out any point where eltoo is more flexible and more usable until somebody tells me to shut up. Thank you.

