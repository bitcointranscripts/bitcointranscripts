---
title: Scalable Smart Contracts Via Proofs And Single Use Seals
transcript_by: Bryan Bishop
tags:
  - research
  - contract-protocols
speakers:
  - Peter Todd
date: 2017-02-03
media: https://youtu.be/7BA7f5vk3jQ
---
<https://twitter.com/kanzure/status/957660108137418752>

slides: <https://cyber.stanford.edu/sites/default/files/petertodd.pdf>

<https://petertodd.org/2016/commitments-and-single-use-seals>

<https://petertodd.org/2016/closed-seal-sets-and-truth-lists-for-privacy>

## Introduction

I am petertodd and I am here to break your blockchain. It's kind of interesting following a talk like that, in some ways I'm going in a more extreme direcion for consensus. Do we actually need consensus at all? Can we make a more robust system by eliminating it to the maximum extent possible? I think for some use case at least I have some techniques that will let you go do this.

## Disclaimer

I want to first give a disclaimer. Chances are that nothing in this talk is original, but rather merely forgotten in the blockchain mania. In the sense that a lot of these techniques have been around for quite a while. Funny story with this is that this approach to smart contracts is actually something I worked at at R3 and at one point I was one of their architects for their Corda system. We sat down in London and said what are we going to do for smart contracts? All three of us basically had the same idea, with some distinction. Anyway, I just want to be clear that I don't want to take too much credit for this.

## Bitcoin non-scalability

And where this all kinds of comes from is that I've been interested in the scalability of bitcoin for a long time. Your fundamental problem here is that depending on how you design the system with nodes, keys, transactions you have order n squared total work. For bitcoin that's a particularly serious problem and has caused no end of political problems and we honestly don't have a good way of scaling it up. When I was at R3 and clients before that, we were very concerned about that. We could throw servers at problems, we wanted to come up with something better.

## A simple transaction

I think it would be good to start with a simple use case, which is that let's do a simple type of transaction with low requirements which is can we represent the buying of a house. What's good about this is that it's a single transaction that doesn't necessarily need to be fast, but it does need to be secure. When we say secure, what are we trying to achieve here? If Alice is buying that house, when she finally gets off facebook and looks at her brokerage she wants to be in a position where what's displayed on her computer and UI represents something accurate: the house sale has gone through and it needs to be accurate. She doesn't care if some database somewhere has the correct or incorrect status. All she cares is that her own device shows the correct status. She wants proof of what state the sale is in.

## Digital signature chains

For old cypherpunks, easy enough to imagine a system, plenty of prior art all the way back to the 1980s when digital signatures were invented. And just like standard land title systems, you could imagine signing a message saying alright I had a house and I'm going to sell it to Alice now and we're going to sign it. And we can go make a chain of these and we can validate the chain. At some point it gets back to the beginning of the chain- your genesis title. This is a diagram of the doomsday book in the UK, the comprehensive record of their ownership in the land. Alice and others can agree on this genesis record between that and digital signatures we can certainly go and show yes it's very likely that her house sale actually could have gone through and when it pops up on her screen that says yes you bought the house then she has reasonable confidence in that.

## Simple formal title transfer scheme

We can even think about this in terms of maybe somewhat more formal title transfer protocol where we have various titles, and you have your genesis title, and various states that form a linked list, and then a "title verify" function, we check our signature and verify recursively and once we hit the genesis title then we're good to go. Very simple. Could be programmed in a few lines of code. You might add more, like merging property lots or something in a real world application, but I think it's safe to say that this represents the core of the problem.

## Double spending

Obviously we have a problem. We're not a bunch of communists: Alice will be very unhappy when she finds out that she has to share her house with Adam. Fundamental digital problem. Our question is now, what is the absolute bare minimum that we need to prevent this problem? Some people might say blockchain. But I think we could actually do something much more targeted. It's the idea of a single-use seal.

## Single-use seals

You see these in the physical world where if you have ever seen a shipping container get packaged up, these are physical seals uniquely numbered. I can tell the guys at the other end of the planet that hey when you receive this shipping container you should see a seal that is closed and it has this number on it and as long as the manufacturer is honest and never makes another seal with the same number then you can have pretty reasonable confidence that when you open up the shipping container nothing is inside the container. We can do a digital equivalent of this.

## Formalizing a digital single-use seal

<https://www.youtube.com/watch?v=7BA7f5vk3jQ&t=6m16s>

Here's our formal definition. We initialize the seal. We get some number s from the initializer. We can go close the seal over some message and get a witness w. We can verify using a seal, a witness and a message, and that returns a boolean true or false. The system is secure if it's infeasible to go find two witnesses such that two different messages return true on a SealVerify operation.

When you think back to the idea of what a digital signature is, we can take this primitive and drop it right into anything that checks a digital signature. We have the exact same properties, but you can't sign twice.

In practice, we might want to make it a little more practical and say well when we initialize, let's set some conditions, and when we close it, we'll show that we were authorized to go close it.

## Pubkey authorization is simple

So there's your useful definition- what are the conditions, I mean I think this conference we've had people talking about great formal languages and so on. So there's a lot of options but the very simplest is just pubkey and the authorization is just a signature and you pubkey authorize it.

## Commitments

We also have to think about the question of how are we going to implement this thing. And what I find interesting is that the idea of a single-use seal is very close to that of a commitment, which is where you take a message, you hash it, and we can verify that the commitment protocol was followed when we take the message again and hash it and it matches. This maps to a seal. The seal initialization takes a message, and SealVerify takes a message again and the witness isn't actually needed. But this isn't terribly useful because you can't make the seal in advance. I can't go use this to seal a house.

## Random oracle implementation

So here's your academic implementation, let's call it the random oracle implementation. The verifier takes a witness and a message and then hashes it. Of course, you might ask: how on earth would you ever get that feature? Well, we could just invent a magical genie that brute-forces hash collisions for us. This might not be the most practical implementation, but we could do this with trust pretty easily.

## Trusted oracle implementation

Say we had a trusted oracle that could guarantee that the seal is closed only once. Assuming that the oracle is honest, we're done. And I think in the context of a lot of fintech we might be able to be finished here and actually implement a system that is reasonably useful and meets the requirements. The simplest implementation would probably have auditing and you might even throw it off into a blockchain. But our bare minimum, that's it. Last I checked, R3's corda project, that's actually pretty close to what they do. There's a bit more complexity on top of it, but it's roughly the primitive you have.

## Bitcoin implementation

Similarly, unsurprisingly, we could do this with bitcoin in that in bitcoin transaction ids are unique. There was an interesting bug about that a few years, I guess. We can close a seal by spending a txout and committing a message, or a hash of the message, and then you can verify it by checking your commit transaction in the blockchain which is your witness showing that it was closed. Simple enough. There's a lot of interesting stuff you could do to amortize this and so on.

## Trusted hardware implementation

Another kind of interesting implementation of digital single-use seals is trusted hardware. Teechan, if you've read about it, it's really simple idea: have some trusted hardware, it follows some particular rules baked into it, and ultimately like the trusted one it will produce a signature plus one more signature that is traceable back to the manufacturer say Intel. This is an Intel skylake processor in the photo which has SGX. If this all works and is secure, we'd have yet another good implementation of digital single-use seals.

We do have some issues though, which is among other things, that not necessarily it's easiest to actually get access to. There's still issues with production licensing. SGX itself currently you can't actually extract an exportable signature from in an easy way. You can't get a signed message from Intel you can get directly. I was excited to hear that Ledger Inc yesterday talking about their progress on this.

## Trusted hardware limitations

But we still have fundamental issues with scalability. We saw that in teechan where while they have done good work at getting fast systems that can do, apparently the number is 10x this on screen, the fundamental problem is that the thing that prevents the double spend is implemented in EEPROM deep inside the chip and while the rest of the system can do 1k transactions/sec, the EEPROM can't. You could write it 100-500 times a second, and even writing at 1 time per second, many implementations you'll burn out the chip in a few days. So that's a big challenge for us using that kind of system.

## Parallelization

But this is where this approach gets exciting in that, even though we're on such limiting hardware and it's so slow, well, we could just use 100 of them in parallel. Let's go back again to what our problem was. We have houses. We're buying and selling houses. When you buy and sell a house does it matter what other houses are doing? There's no need to have consensus over the state of those transactions. It's irrelevant to Alice whether Bob is selling some other home too. There's no interaction between those two financial transactions. This is not true of all financial transactions, but there's a big class of financial transactions where this is true, and I think we should take advantage of this by designing systems where we can modularize the consensus.

This kind of thing is very robust where if you implemented such a system on a group of however many 100 intel SGX processors or whatever... what happens if half of them go down? That only means that the half of the people might have to wait for their transactions. The other half is just fine. You can still go build on those chains of proofs, even though the rest of the system is-- well, say, consensus isn't quite correct. Simply shutdown is, simmilarly, if you draw a line in the middle and say half is one side of the planet and half the other and cut the fiber optics lines down the middle then the system still works even though I can't go sell a house to a guy in Asia... but I can still go sell a house in my own geographical area. This is a robust system, even though it didn't have any consensus. It was also built on simple primitives.

## Consensus domains

<https://www.youtube.com/watch?v=7BA7f5vk3jQ&t=14m30s>

In the few times that you want to cross consensus domains, there's plenty of options. I think this is a great example: we have a house, and we want to sell it for money. Bob isn't going to just give Alice a house. Instead it's a situation where Alice pays Bob and that payment needs to trigger the seal to close. What's acually happening here is that-- Bob has a house, Alice is the bitcoin, Alice goes and creates a dummy transaction and moves it off into a consensus domain maybe a physical SGX chip and Bob does the same thing and they are both in the same consensus domain and they could do a transaction where the actual authorization says this transaction isn't valid unless this seal closes at the same time and vice-versa. And then they can go back their own way and send it to wherever they need to in terms of consensus when they're done and want to get off the SGX system.

There's a couple more options here like lightning-style time delays and hashlocks. But I think the point of this is that we can solve this and it's really not that hard. And between those 3 consensus domains, did they care that halfway around the world the internet was down? No, of course not. All they care about is the single-use seal and does it work. You can make this happen.

## Validity oracles

The fact that we're talking about bitcoin gets us to our next open issue with this, which is that, well maybe house isn't going to change hands that often. If we're talking about money, then that's probably not the case. In the UTXO model, you have coins that are bought and sold and this creates a pretty big graph in a reasonable economy. And interestingly, I know R3 corda did actually go with the UTXO model. At some point, Alice may not want to download 20 gigabytes of transaction history. She might be willing to- just like with single-use seals themselves- use a little bit of trust and make things more efficient. This is not that hard to do. Even without moon-math, we're already trusting people to hold the money and make it worth anything. Have them sign an attestation periodically saying "this part of the transaction graph is valid". You don't have to actually go check it. Equally we had some exciting news about SNARKs and STARKs... this part of the problem might get replaced by math and it might be possible to create a mathematical proof that transaction history was valid up to a certain point, but I don't have to rely on that because I can just throw a bit more trust at the problem and the system will still work.

This kind of validity oracle just like the single-use seal... there's no strong need for consensus here. All you're doing at worst is telling the oracle here's a bunch of transaction data could you please validate it and give me back a signature and say you checked it? Maybe you do it recursively and give the validity oracle a signature from a previous run. This is a simple trust model and we can easily come up with business solutions to go do this in a trust environment. I would call this a solved problem.

## Do proofs and single-use seals scale?

With all that in mind, our real question now is whether this model like this did we make it this scale? And first and foremost I'll say that at worst we have done no worse than bitcoin or order n squared, for the simple reason that if you're a bitcoin user or similar system and you run a node, then the situation you're in is equivalent to getting all the possible transactions, validating it all, and doing validations and checking things and spitting out a proof on the screen as to whether the transaction went through. So your absolute worst case is no worse than the status quo.

Depending on your trust model, we can do better than the status quo. This question gets down to what are we trying to prevent? What is the trust model? What kind of guarantees do we want? Probably we can get down to order n for the simple fact that in a fintech environment we have legal systems that say yes not every single user checked every transaction but we have good assurance that of the single-use seals and validity oracles that collectively this was audited just like a traditional banking system. In that kind of environment, yes we do have a system that has roughly order n scalability. And from the point of view of Alice in that transaction maybe it's even faster in some cases. Because we have a flexible system here, we can decide what makes sense and what doesn't. Does data have to be received from other people or something? We get a lot of flexibility. At R3, we ended up in a model like this where we looked at it from the point of view of what needed to be proved, what needed to be prevented, etc.

As simple as this is, I think it's worth looking back sometime and saying do we need the complexity of modern protocols. And if you have a question, please ask.

## Q&A

<https://www.youtube.com/watch?v=7BA7f5vk3jQ&t=21m>

Q: ...

A: I think that's absolutely true. Something that comes to top of my mind is that, anything where you see high-speed trading right now. The whole purpose of orderbooks is to have fast and comprehensive visibility into the economy at large. I don't want to claim that single-use seals are for everything. But on the other hand, you could probably do hybrids where high-speed trading facilities might do net settlements with other systems through something like this. But sometimes systems don't need high-throughput. Like if you have money movements and you have to report to someone... that doesn't necessarily mean that the regulator involved in reporting needs to have consensus directly. It may be sufficient to publish that information provably and make it part of the rules. You must prove that you notified the appropriate people as part of your transaction proof. But it doesn't mean that the reception and notification needs consensus. There's lots of options there.

Q: There are signature schemes where if you sign more than one thing then you give away your private key.

A: I think they could be used here. But it would worry me that you really, the assumption that the revealing matters depends on the architecture of the system. You have these nonces in monero that gets revealed as part of the spend and it should not be possible to reveal the same nonce twice. But in monero to maintain consensus there's a list of nonces revealed with full consensus. But unfortunately this doesn't give you good partition tolerance or scalability. But say in monero it was best-effort it would then be possible to arrange scenarios where you can get away without fraud. It's one of the design or business decisions- maybe you're in a situation where occassional fraud gets through, maybe you're not. I think they are interesting systems but they should be carefully analyzed for what could go wrong.

Thank you.
