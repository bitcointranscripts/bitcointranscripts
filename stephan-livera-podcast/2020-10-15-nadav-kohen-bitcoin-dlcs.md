---
title: What You Should Know About Bitcoin DLCs
transcript_by: Stephan Livera
speakers:
  - Nadav Kohen
date: 2020-10-15
media: https://stephanlivera.com/download-episode/2559/219.mp3
---
podcast: https://stephanlivera.com/episode/219/

Stephan Livera:

Nadav welcome to the show.

Nadav Kohen:

Thanks for having me.

Stephan Livera:

Nadav I’ve been following your work for a little while. Obviously I really I like reading your blog posts over at Suredbits, and I had the chance to meet you earlier this year in London. Can you tell us a little bit about yourself and what’s your role with Suredbits?

Nadav Kohen:

Yeah. so I am a software engineer at Suredbits. I’ve been working there since I graduated college a bit over two years ago. I’ve been primarily working on kind of the open source side of things with Bitcoin S, which is the Scala library for Bitcoin and primarily working a lot with Discreet Log Contracts in the last many months. And I also dabble a bit in various lightning related things as we do at Suredbits. And yeah, I read a lot of blog posts also, so that’s most of what I do.

Stephan Livera:

Awesome. So today we’re going to focus on DLC, and I think it’d be great to talk about what are the key things that people need to know about DLCs. Cause they might’ve heard about it a little bit here and there, but they don’t, they might not have really dived taken the time to dive into this. So do you want to start by telling us what is a DLC?

Nadav Kohen:

Yeah. So DLC stands for discreet log contract. The name itself is actually a pun Discreet is like misspelled to be like a hidden or not hidden. What’s a better word, like private, so to speak. So yeah, a discreet log contract is a blockchain contract it’s possible to do on Bitcoin, which is what we’re implementing it on which is enforced through a digital signature, specifically a Schnorr digital signature off chain that is provided by an Oracle. So essentially on kind of just the low level, like Bitcoin contracting side of things, the discreet log contract is just a contract, which is contingent on a discreet log, as you might imagine. Where the discreet log in this case is a signature. So we can get more into what all of that means and why it’s called that later.

Nadav Kohen:

But at a high level, a discreet log contract is simply a group of people coming together, make an agreement about you know, if the Oracle says that this real world event happened, then we are going to have these payouts and say like, you know, super simple example say like me and Stephan wanted to have a little contract to see whether or not Bitcoin was going to go like over a 100k by the end of the year or something like that. And you know, one of us could go over, one could go under and then we could put some Bitcoin into a shared output on the blockchain. And then based on what the price was, according to what an Oracle says it was, we would then distribute the funds accordingly in a kind of non-custodial derivative kind of fashion.

Stephan Livera:

Great, and so I guess to zero in on that question of why would I use a DLC then I guess it’s a different level of trust, is that why we would use a DLC as opposed to just say, I just go to a betting website and I just make a bet on that centralized, openly centralized website.

Nadav Kohen:

Totally. Yeah. Yeah. So the main feature, I would say that separates DLC from other ways of doing these kinds of contracts is custodianship. So you don’t have to trust kind of your matchmaking service to actually hold any of your Bitcoin or deal with any of that. One of the main nice things about DLCs is that at no point, are you relying on anyone else other than maybe the Oracle, which we can get into, to determine kind of what happens with these funds, like it’s you and another party directly putting these funds into this contract, that’s enforced on chain without any third parties needed. And it also has the added benefit of kind of along the same lines. They’re more private. So rather if you’re using like a centralized service, you know, the centralized service knows what everyone is doing at all times.

Nadav Kohen:

And with a discreet log contract the actual contract, the thing that ends up on chain is pretty vanilla. Like it doesn’t really reveal anything about what your contract actually is. Most of the magic happens off chain, similar to how if you see like two of two multisig on chain today, you know, you can’t know whether that’s lightning or whether that’s like, you know, two friends sharing some Bitcoin or one person with multiple keys or any of these kinds of things. I think that yeah, so, and it turns out DLCs today have the exact same on chain footprint as like a lightning channel. Well I should specify prior to actual execution, they look exactly the same as an open lightning channel. Afterwards things get a little bit more detailed and hairy, but yeah, essentially there’s almost no on chain footprint for DLC, especially at no point even in any scenario, do you actually have to reveal to the world what the entirety of your contract is? You just reveal like the actual payouts of what happened and yeah. So I guess the main two benefits of discreet log contracts over say, like, you know, using BitMex or something like this is you custody and privacy.

Stephan Livera:

Do we have sense of the size of the market for this? And I guess just naively, we might, we might be thinking, Oh, hang on. Is this thing just for degenerate gamblers or are actually real businessman who might use this kind of product?

Nadav Kohen:

Yeah, totally. Yeah, so, I mean, I guess I have a couple of different answers. One is that I mean, I think that when it comes to Bitcoin, like so far, one of the most successful, you know, killer apps that Bitcoin has to do with is trading. And so you know, I would say that if we achieve nothing else with discreet log contracts, at the very least, you know, we open the door for things like decentralized exchanges and these kinds of things to occur in kind of the best way they can, or at least I believe that DLCs are kind of the way of doing that. But then, you know, that aside, you also have all of the kind of, you know, normal things that you know, derivatives kind of give to businesses. So, you know, you can hedge against, you know, really any index you want. You can really take any position against any real world thing, you know, be that like the price of corn or the hash rate, or you know, whether or not the Patriots win the super bowl or, you know, whatever else it is you want to take a position on, you can kind of do that. And you can do that without kind of needing permission from anyone to do so.

Stephan Livera:

Great. And so maybe just to make that a little bit more real for listeners, what might it look like in the future? Would they have some kind of wallet that also has a DLC function and then they would select an Oracle and then have a counterparty, or what would it look like?

Nadav Kohen:

Yeah. So, I mean, I think there’ll be kind of a mix of things out there that are all kind of underlying, you know, under the hood, they’re all using the same protocol underneath. So certainly I think that there will be wallets that kind of let you do DLCs in various ways. You know, we’re working on integrating DLCs into the Bitcoin S wallet. I know that Nicolas Dorier is working on integrating DLC into BTC pay server. So they’ll, they’ll pop, you know, they’ll pop up in a bunch of wallets. I think certainly I think also that there will be kind of platforms that are interested in facilitating matchmaking for various kinds of you know, contracts or instruments, financial instruments. So for example, you know, I could imagine that like you could connect to Bitfinex with like some desktop app and Bitfinex would then facilitate like matchmaking for people, but then, you know, once a match is made you don’t actually go through Bitfinex to enter into this position.

Nadav Kohen:

You just go straight peer to peer and enter into this position. And I also think that there’s a possibility that in the future you’ll have something that looks a bit more like lightning, where like there’s like a P2P DLC network or something a bit more decentralized where you know, Oracle signatures are being gossiped around. And I don’t know, maybe you have some way of doing matchmaking one way or another, or maybe you’re just connected to a bunch of market makers or however it might be where you can just in an entirely peer to peer manner kind of find DLCs if there’s a position you want to enter in. Yeah, but I guess a lot of it also just depends on like what you want to use DLCs for. Yeah. Cause I mean, for trading, I think it makes a lot of sense for things like exchanges or things like decentralized exchanges to kind of facilitate, you know people finding each other.

Nadav Kohen:

But, you know, you can also kind of do the you know, the IRC or Twitter DMs kind of matchmaking, or, you know, just tweet out like, you know, this is how it’s work. This is how it works today. So to speak, like you know, Nicholas Dorier tweets out, like, I want to bet on the US election and then, you know, Chris Stewart at Suredbits you know, as like, you know, we’ll take you on let’s enter into a DLC and then, you know, you just go do that peer to peer. So yeah, I think, I think there are a lot of different ways that it could end up happening. It’s kind of too soon to know how widespread or unique or niche, I guess it will be. But right now you know, if you want to enter into a DLC today, which is possible it takes a little bit more work than it will in the future. But if you want to enter into a DLC today, then I think it’s mainly integrated into wallets and DLC specific libraries, but yeah, I mean, we’re working on a specification so that you can just kind of support DLCs wherever you want, where you know, you have keys and Bitcoin lying around, you can safely enter into DLCs with, you know, anyone else using any other client.

Stephan Livera:

Great and so I’m hearing there that some of that is just going to be people making bets against each other and some of that will be trading. And some of that will just be actually, there will be business cases in the sense of business people or traders who want to do things like maybe you’re a miner and you want to express a certain view about the hash rate or energy pricing. And that is where maybe there’s a link back to underlying Bitcoin businesses. Correct?

Nadav Kohen:

Totally. Yeah. So, yeah, I mean, you know, and anything that an Oracle can put a number to and just broadcast out you know, you can make a contract that is contingent on that and also contingent maybe on other things, you know, you can make kind of these composite positions or yeah, I mean, yeah. So I think I agree with what you said it’s mostly kind of trading and all of the things that you get out of trading instruments, existing, which, you know, hedging is usually the thing to think about.

Stephan Livera:

And maybe it would be useful to just think from a comparative perspective there. So let’s say you know, Nicolas Dorier and Chris Stewart, they’re doing this bet now they could theoretically have just gone for, okay, let’s just do multisignature, we’ll find a trusted person in the community and they will be the, you know, the third key in a two of three set up and blah, blah, blah. Could you just outline for us a little bit, how to think about the difference there of doing it as a DLC versus doing, just with on chain multisig today.

Nadav Kohen:

Totally. Yeah. So if you were going to do a two of three kind of what I would call it, like an escrow position where you find some escrow to kinda decide where the funds go in case of disagreement. I think that this has some interesting use cases, but DLCs are clearly going to end up being superior. And here’s why, so essentially the key difference between a discreet log contract Oracle and kind of a traditional, like, you know, third party escrow kind of like you just described in this scenario where we kind of just get a, you know, third party person who we both trust to, you know, decide where the funds go and in what quantities. So yeah, the biggest difference is that discreet log contract Oracles are at least in some sense oblivious. So they don’t know about their users.

Nadav Kohen:

They don’t know what contracts exist. They don’t know how they’re being used even. So if you’re signing, say a price anyone can construct any contracts they want, you know, they can go long, they can go short, they can do a strangle or a wedge, or, you know, do whatever fun, funky payout curve, me and Ben at Sured bits, we were chatting the other day of like how maybe for privacy reasons, someone might want to do like a sine curve looking like, you know, oscillating payout function. That doesn’t really mean anything. But yeah, anyway, so point is that a discreet log contract Oracles don’t know who their users are. They kind of are these entities that just broadcast signatures of things they see publicly. And that’s kind of all they do. They don’t know about their users, whereas in the escrow case bribery becomes more of a concern because, you know, say like I see that I’m going to lose, well, I’d be willing to give up like almost all of those funds since I’m going to get zero, say I would be willing to give up like all of it, a couple thousand stats for you to sign the other way.

Nadav Kohen:

Cause then I at least make something instead of nothing. So yeah, I guess, I mean, if you truly trust the person and they’re trustworthy, then I think, you know, sure. I mean, when you have trust, you don’t need heavy machinery, but kind of, as far as the spectrum of trust goes, I would say that kind of escrows require the most trust. And they you know, are maybe the simplest way to go. DLCs require very little trust, at least comparatively. And, you know, we can get ways of mitigating trust by, you know, using more than one Oracle and, you know, having fraud proofs for Oracles. So, you know, this oblivious entity whose only job is to sign what happens in the world. Do you know, it’s very making sure that any time that they cheat or they signed something that they shouldn’t have, or they sign multiple things, or, you know, do kind of any Oracle it’s fully traceable and fully provable kind of to the rest of the world that, you know, this Oracle shouldn’t be trusted.

Nadav Kohen:

Yeah. And I think that also kind of the ecosystem that I expect to eventually sprout out around Oracles is going to be based in kind of you want your Oracles to be trustworthy. So I guess this might be getting into kind of a different comparison. So if you compare discreet log contract Oracles to say some of these very, very good, complicated, decentralized Oracle schemes that you see on platforms like Ethereum, I personally don’t find decentralized Oracles to be too appealing because it kind of seems like you’re, you know, you’re, I have this problem, which is that trust is required in order to do anything that requires information from them outside of just like transaction data. So, you know, say I want like the Bitcoin price or you know, okay. And any other thing that happened in the real world who won the election, for example, you need to trust something to give you like a digital signature of what actually happened in the real world.

Nadav Kohen:

And if the thing that you’re, you know, one solution is don’t trust one thing, trust like many, many, many, small things are anonymous entities that you don’t know, and aren’t necessarily very trustworthy, but you know, so long as like maybe some weird game theory happens and you’re shelling points or some other argument for like why this process should result in truth is kind of my framing of how I think about decentralized Oracles. Whereas with discreet log contract Oracles, I think of it as more the solution is, yes, you should trust multiple or you should spread your trust, but not too thinly should spread your trust between trustworthy like sources, right? So like people are willing to trust a Bitfinex, I think, much more than they’re willing to trust like random scheme of pseudonymous people who may all be actually just one person gaming everyone else, or like something like this.

Nadav Kohen:

Yeah. So I think with decentralized Oracles, you have a lot more to worry about when it comes to like gaming the system where, you know, it’s kind of a similar, maybe just this is a bad analogy, but it’s somewhat similar to like, you know, the concerns between, or comparing proof of stake to proof of work where like, you might worry that in a staking system, or like in this decentralized Oracle, you know, one person with the most wealth or most resources might be able to just dictate the truth is kind of how it plays out. Whereas in this proof of work system, it’s based on like something in the real world that you need to like exhaust in the case of proof of work or in the case of discreet log contract Oracles in this analogy in the real world, you need to like have a reputation and have like, you know, a public image that people trust and maintain that by, you know, being a good Oracle and all of these kinds of things.

Nadav Kohen:

So I think yeah, I guess that’s, that’s a loose analogy, but I think that at its core discreet log contracts are more part of what discreet log contracts are, is kind of a proposal for not necessarily a solution to the Oracle problem, but you know the Oracle problem isn’t solvable so much as I think a better framing is. So for those who don’t know that the Oracle problem is just kind of the problem I described of you want to do something in the digital world. But you have no way of verifying that. Like, the thing happens that you, that happened in the real world other than trusting some Oracle or, you know, Oracle meaning like a black box thing that could be a set of entities or one or two or something like this. So I think that these are all kind of different answers to like how to solve the Oracle problem.

Nadav Kohen:

Right? One is like pick someone you trust and put them in a two or three multisig. One of them is like do some weird game theory, things that seem to, you know, occasionally, you know, people find ways to game them and all sorts of other problems and complexity. And then for discreet log contract, kind of the answer for what we should do about Oracles is that you should make Oracles oblivious to their users and that you should use more than one. So, you know, these Oracles kind of their signatures should be composable. And then beyond that, you should just be able to enter into kind of a two of two multisig where the technology that discreet log contract use today is called adapter signatures. So we use adapter signatures to kind of make kind of these, I guess we can go into the actual scheme if you want to.

Stephan Livera:

While we’re on this whole Oracle thing, I guess one analogy or one example would be something like, let’s say, people want to make bets on the sport on sports outcomes. And then theoretically, maybe someday the NFL or the NBA would run an Oracle. And they would using that Oracle announce the results kind of the truth of the results of who beat who, and then you, and I might make a bet and our DLC would depend on, let’s say the NFL or the NBA to correctly state who won. Right. But without knowing that you and I made that bet. Right?

Nadav Kohen:

Yeah. And they wouldn’t know that we were making a bet using them versus, you know, using someone else they might, you know in a taproot future, they won’t even know that like a DLC happened. And even in the case that you like make some kind of guess based on chain analysis today that a DLC happened, do you have no clue what it was about? Like Oracles can’t see themselves in contracts. Other people can’t see Oracles in contracts, they’re kind of hidden in the signatures in various ways. Some kind of you know, yeah it’s pretty much untraceable to the Oracles. And I will note though, so I think it totally makes sense for like, you know, NBA, NFL, they could publish signature is not just about like who won, but also like all the stats, right.

Nadav Kohen:

They essentially, you know, there are these entities that are just amassing a ton of data and, you know, to some extent making it very public so that it can be used in things like fantasy sports and stuff like that. But you know, just the extra step of just sign that data is I think not too high an overhead, especially for something like a, cryptocurrency exchange today, you know, a lot of them are already, you know, signing things for like various, you know, chain-link or Ethereum based Oracles. And I think that it makes a lot of sense for them to kind of just sign their data streams as they go out.

Stephan Livera:

Okay. So look, let’s talk a little bit through the execution of this. Maybe talk through just an example, like what is the funding transaction? What’s the suspending transaction.

Nadav Kohen:

Yeah. Say that you and me want to enter into a discreet log contract. I’m assuming you want to take the position that Bitcoin is going to be over a hundred K by end of year. And, you know, I have a ton of Bitcoin hidden away, so I’m going to, you know, hedge in this case against that. So and say that, you know to make the numbers easy, say we’re each going to put in one Bitcoin and then winner takes all. So, you know, if it’s over a 100 K, you’re going to get all of it. If it’s under, I get the two Bitcoins. So how this works is first, you know, we do kind of what I just described, which is like, you know, find a counter party, find someone who wants to kind of take the opposite position from you.

Nadav Kohen:

And then what the two of us do is we kind of give each other enough information to build all of the transactions that we’re going to need. So that means like, you know, I’m like, here are my UTXOs that I’m going to use you know, this one has a Bitcoin in it. That’s what I’m going to use. You tell me about yours. And then we also kind of agree on an Oracle who has committed to this event over under a 100 K at the end of the year. So we have some Oracle that’s going to attest to this event. We agree on that Oracle say maybe multiple, but let’s keep it simple, just one Oracle. And then we agreed on the contract terms already. So now what we do is we build a funding transaction, which simply takes our inputs, the inputs that we’re using, that each say have a Bitcoin in them.

Nadav Kohen:

And so this transaction takes those as inputs output. It has a single output that we care about called the funding output. And that is just to have two multisig between the two of us. So while we were talking earlier before building we each gave each other a public key, and then we use those to public use these funding, public keys to create a 2 of 2 output. And this is going to be our funding transaction. So this is the thing that’s going to actually be on chain. And then we’re going to have a bunch of stuff spending it. That’s going to be off chain. So before we sign the funding transaction, we have to build all of the transactions spending it. So we call these contract execution transactions or CETs, and CETs are like as simple a transaction.

Nadav Kohen:

Well, almost as simple a transaction as you can get, they have one input, which is going to be the funding output. And they have one or two outputs in this case. So in this case, both of them are just going to have one output cause it’s winner takes all, but you could imagine we, you know, do something a bit more nuanced where we’re like, you know, we want to take like some curve and as the price goes up, one of us gets more and one of us gets less and vice versa going the other direction. So, you know, that would end up with like a bunch of intermediate states that each have different output values. And we would both get something depending on what the price was, unless, you know, you reach some maximum point on either the left or the right, but in this case, super simple binary outcome, just two CETs that we’re going to need.

Nadav Kohen:

In this case, since it’s winner takes all, one of the CETs just spends the funding out to my address and the other one spends the funding output to your address for two Bitcoin. And then so, so now it comes the part where we actually, so far, you know, we’ve just kind of built out all of these transactions that you know, we have a funding transaction, which spends our inputs and we have the CTS, which spend the funding transaction. And here’s the part where we actually introduce kind of the Oracle or how we use the Oracle. So the Oracle committed to signing this event. Yeah. And they do this with a public announcement. We call it an Oracle announcement. And in this announcement they include kind of the cryptographic data that you need to I think would calls, it anticipate their signature.

Nadav Kohen:

So we can’t compute their signature because they haven’t signed it. And we don’t know their private keys, but if we know their public keys and this extra public commitment which is the commitment to the nonce that they’re going to use to generate this digital signature. So they give you like the public key to this private key that they’re going to use. So with just these public keys, you can compute an anticipation of the signature, which this is going to get just a little bit weird, but stay with me the signature, which is just a number it’s a short signature, it’s just, you know, some numbers same as a private key. And so in this case, we kind of abuse the fact that it’s just a number and we treat it like a private key. And so it has some public key.

Nadav Kohen:

So you can compute the signatures public key as if the signature was a private key from just public information. And then we use that public key to essentially tweak our signatures. So when we’re, when I’m giving you, so right there, these two CTS lying around, you need signatures of them from me. So that we know that, you know, you don’t need me in order to execute the contract. You don’t need cooperation later. So I give you a signature of both of the contracts, execution transactions, but it’s not a valid signature, it’s a tweaked signature, or what’s called an adaptor signature. So essentially with just this public point, kind of the anticipated signature, I can tweak my contract execution, transaction signature, which I’m giving to you a lot of signatures here. And the only way you can and tweak it is with the Oracle signature that corresponds to that.

Nadav Kohen:

So to kind of stay that without saying the word signature as any times. You know, I can’t do it using the word signature a couple of times. I need to provide you with some invalid digital signatures, which can only be made valid by you if you know, a specific Oracle signature. So for example they’re going to say, sign the message over or under then for the message over, I generate an invalid signature of that CET, which spends all of the money to you and for the message under, I anticipate a different signature. And I use that to tweak and give you an invalid signature of the CET that sends all the money to me, and you do the same to me. So we kind of have these invalid signatures from each other, and then, you know, come years end, the Oracle is going to broadcast just one signature, say over, and in that case, you will then be able to kind of un-tweak the thing I gave you, the signature I gave you. And now exactly one of our contract execution transactions has become valid. And then you spend that and you get all the money. So that’s in gory detail what happens.

Stephan Livera:

Yeah, that’s cool. So, I mean, first off it sounds, it, it feels very similar to lightning in some ways, right? Like, let’s say I’m opening a lightning channel with you. Well, it’s a similar kind of flow in some, in some aspects, right? So it’s like, we are creating this shared output. There’s two of two and we are passing back and forward a pre-signed commitment transaction to close the channel. Right. But in this case, that’s like a CET, a contract execution transaction, but the difference here is in lightning world. The pre-sign commitment transaction is a valid transaction if broadcast to the blockchain, but in DLC world, it’s not, we’re waiting and we need that Oracle signature to make either your side valid or my side valid, and then we can broadcast it to the blockchain and claim the funds, et cetera. Right.

Nadav Kohen:

Yep. Exactly. And yeah, so, I mean, especially at the very beginning, like just kind of the idea of having a funding output on chain and then kind of a bunch of stuff off chain that doesn’t ever end up unchain is very similar to lightning. You know, we use the exact same funding, transaction structure pretty much almost. And we actually were reusing or mimicking at least a lot of what’s in the dual funding channel proposal for lightning, for negotiating DLCs. We reuse almost all of it as it stands today. So yeah the transactions are pretty much almost, I mean, there are a couple of fingerprints right now in today’s implementations, but especially in the future, I mean, these things are going to look very similar to a lightning channel. And then another similarity that these have to lightning is in lightning, your payments are kind of enforced using these HTLCs. So you have like some hash, and in order to claim these funds, you have to reveal a pre image. So the mechanism for actual enforcement is also quite similar with you know, DLCs where you can think of it, conceptually as we have these potential signatures, these anticipated signatures, and you can only claim the fund with this transaction, if you reveal the pre-image to that anticipation, which is the actual signature.

Stephan Livera:

Okay. So we’ve spoken through what we might call the happy path, right? Let’s talk a little bit about the unhappy or the failure pathways. So maybe an example might be, what if our counter party goes offline or they try to cheat you can they? Or basically they can’t cheat you?

Nadav Kohen:

Yeah, so they cannot in the current scheme. So I apologize in advance to anyone or not an advance, I guess, but I apologize to anyone who is waiting on me to update the blog posts that I’ve written kind of a while ago about DLCs but some stuff has changed. We no longer use any kind of penalty scheme now that we’ve moved to adapter signatures. And so what’s really cool right now about DLCs is that there is no difference between the kind of happy path and sad path closing in either case does not require cooperation. And you can’t, I guess there’s not really any reason to use cooperation since you have all of the signatures you need. Once the Oracle has broadcast their signature, you have, you know, everything you need to just broadcast your contract execution, transaction, no need to contact your counterparty.

Nadav Kohen:

They can be offline. They can be in a plane, they could be dead, or, you know, whatever the funds it’s kind of fully trustless. You have everything you need to execute on your own. And there’s not really any reason to do it any other way. That is until we get to taproot. When, you know, essentially it’ll be nice because you won’t have to reveal like your tree and stuff like that. But so we’ll, re-introduce cooperation there, but in the case where the other party isn’t online, there’s no weird time locks. You have to wait on, there’s no infrastructure you have to deal with at all. It’s literally just, you know, broadcast your signatures or your broadcast fully signed transaction. You’re done.

Stephan Livera:

Yep. And so that’s the counterparty. Now, what about if things happened with the Oracle? So maybe some different scenarios here. One might be, the Oracle goes offline, or maybe for example, you and I make this bet and we say, okay, Bitfinex is going to be our Oracle. And let’s say, I mean, you know, forbid this happened, but let’s say Bitfinex went out of business, they went bankrupt or, you know, or the other one might be if the Oracle lies what do we, how do we deal with these kinds of situations?

Nadav Kohen:

Yeah. So in the case where just to keep it simple, you’re using one Oracle and it doesn’t release a signature, or releases a signature of some weird thing that, you know they weren’t supposed to which you can prove that they weren’t supposed to based on their announcement. So it’s not like some sneaky trick to like, not sign anything. Like if you don’t sign anything, you didn’t sign anything. And if you signed something you weren’t supposed to, people can prove you weren’t supposed to prove it because in the Oracle announcement, they tell you everything you need in order to anticipate all of the possible signatures. So if you couldn’t anticipate that signature, you can use their announcement against them. But anyway so yeah, say that an Oracle goes offline. That’s the kind of easiest scenario that you can imagine, or, you know, something else goes wrong and they just don’t broadcast a signature.

Nadav Kohen:

So our mitigation against this right now kind of in the scenario where you’re just using one Oracle, is that you and your counterparty, when you were constructing all of those CETs kind of the things spending the funding transaction, you construct an extra one, which is time locked sometime way in the future called the refund transaction, which just sends us back our funds. So I guess I should mention, this is a two of two multisig kind of unchain is what’s actually kind of what holds the Bitcoin. So if you want, you can always like break your contract so long as both parties agree. You can do anything you want. The DLC is just kind of a way of like agreeing now, and then not having to agree later on how the funds should be spent based on what Oracle does.

Nadav Kohen:

So I guess, yeah, the simplest answer is we have a refund transaction with the time lock on it, but there’s a bit more to the story which also ties into like, what if they say something they aren’t supposed to or by re-chaining a line and say the price is something that it isn’t, or say someone one who didn’t, or, you know, whatever it might be. So the first wall of defense is you should use more than one Sig or use more than one Oracle, you should be using multiple Oracles. So that means for example, in the future, I think people will do something like they do. You know, when you care about key management with multisig today, you use like two of three Oracles or three of five Oracles and agreement or something like this.

Nadav Kohen:

So if one Oracle lies the first thing you can do is easily generate a fraud proof and show everyone like, Hey, this Oracle light or something went wrong. They’re not trustworthy beware. And, you know, make that public in a way that everyone can see that they light. Because the thing that the Oracle presents is a digital signature and only they could have generated that unless they’ve leaked their private keys, in which case also not trustworthy. So yeah, these we kind of have this property that any time an Oracle does something that you don’t think that they should have, you can generate a proof that anyone else can verify that that happened. So that’s one benefit. And then this kind of gets a much better when you are using say three or five Oracles, because now not only is the cost of bribery, like if I want it to go to these Oracles that everyone is using super high, because I need to bribe like three different Oracles or something like this.

Nadav Kohen:

But also, you know, if I successfully bribe two and fail to bribe the third one who I thought I had in the bag, then these other two Oracles suddenly have to like go out of business. Cause everyone can see that they lied and, you know, you didn’t even make any money out of it. So I think there certainly are concerns and I think people should be concerned and think about kind of what to do when an Oracle lies and making sure that you are validating that you actually trust the Oracles that you’re using and using more than one Oracle. But I guess, yeah, kind of the conclusion at the end of the day is if you like, you know, say three of the Oracles all lie in the same way together. Like you lose that money, but to be clear, this is still much better than like something that would happen on an exchange where they literally are holding onto your keys. So if they’re not trustworthy, like you know, single points of failure.

Stephan Livera:

Yeah, yeah, yeah.

Nadav Kohen:

And then, you know, there’s other things other ways in which DLC are better as well, but yes it is fair to point out if, you know, your entire kind of Oracle setup becomes compromised, then you’re going to lose funds. So long as you know, you can’t reach out to your counterparty and come to an agreement about how the funds should be spent. I will say there’s one last protection that’s kind of built into DLCs that’s quite interesting, which is Oracle’s cannot say two different things happen, or they can’t say multiple different things happened to different people. So if an Oracle broadcasts two different signatures for the same event, then they leak their private keys. So I mentioned earlier that how you commit to an event is you commit to the nonce you’re going to use. And so if you sign two different messages, you just did nonce reuse. And if you reuse, nonces when you’re signing, you leak all your private keys to anyone who sees those two signatures. And you know, if you’re an Oracle and your private keys, aren’t private, you’re not really a trustworthy Oracle anymore. Anyone can see that, you know, they shouldn’t be usingn you.

Stephan Livera:

Yeah. So that’s a big penalty for them for doing that. And let’s say, I’m the NBA, or I’m the NFL. Well, then there’s more incentive for me to get it right when I’m announcing the results of the statistics of my games. Because as you mentioned there’s a big risk there around nonce late well private key leakage, totally. In your blog post, you mentioned equivocation what’s that?

Nadav Kohen:

So that’s the fancy word for saying two different things happened or saying multiple things happened, equivocation or equivocating on something is flip-flopping so to speak. Yeah. So that’s what, when people in DLC land like to use the fancy word, like equivocation isn’t allowed because it leaks your private keys, this is what we’re talking about.

Stephan Livera:

Gotcha. And now this is another thing that I know the lightning protocol developers deal with, which is the fee market or what we might call the block space market. Right. And so as they open the lightning channels to each other, they might need to periodically renegotiate the fees. So a quick example would be, let’s say we open the channel or we start the DLC when the fees are low, but then later when you’re going to close it out, the fees are higher. How do we deal with this?

Nadav Kohen:

Yeah. So there, there are a couple of different scenarios and each of them has a couple different kind of ways of dealing with this. We’re super lucky to have Antoine Riard working on DLC and in lightning on this problem. So we’re using kind of a lot of the same solutions and, you know, we run into a lot of the same problems as lightning does on this issue. So one solution for the, or I guess this is kind of a fee problem that you didn’t even mention cause it’s not as much of a problem I guess, but you know, theoretically, you know, we’re spending some time signing transactions for each other and by the time everything is signed, like the fee has moved and all of a sudden, not even our funding and transaction, like has a high enough fee or something like this.

Nadav Kohen:

Well for that we can use I think it’s BIP 125 replaced by fee which allows us to kind of replace our funding transaction with a higher fee funding transaction. This is not currently implemented in the specs or any DLC things, but it’s part of the dual funded lightning channel proposal. And we plan on implementing it eventually just early days. So we haven’t gotten around to that. Kind of the bigger mitigation that we have is using a procedure called child pays for parent which relies on package relay, which we will be getting in Bitcoin hopefully soon. But this is kind of just a low level issue where we essentially need to transport multiple things at the same time over the net, like in the relay part of the network of just the Bitcoin peer to peer network.

Nadav Kohen:

That is so we need to tell you about like multiple transactions. Cause like, say my first transaction say like it’s a CET or something that we signed a long time ago, the fee is like not large enough and the fees gone up since then we need to pay more fees. So what I can do is I can spend my CET with just another normal transaction, paying myself from myself to myself. And this transaction, you can have a super high fee. So that combined, if you look at just like the virtual or the Satoshi per virtual byte or something like that then you know, now it’s an acceptable fee. If you look at both of the fees kind of averaged way diddly together. So what we do then in this case is we ensure that any party who might be worried about this transaction getting on chain.

Nadav Kohen:

So for example, if you’re getting money on a CT, well, then you’re guaranteed to have an output on there. And so you can spend that output with a really high fee transaction to yourself and then broadcast both of those things at the same time in order to kind of bump your fee rate higher. So that’s kind of the main thing we’re trying to make sure that we can get to work. We call these kind of outputs, anchor outputs. So you have these outputs that make sure that you can essentially dynamically choose what your fee rate is later by just introducing another transaction with a higher fee rate. And the same thing goes for the funding transaction, where so long as you have a change output on there you can also spend the change output on the funding transaction with a high fee transaction. And as I mentioned, this is called child pays for parent. So if you picture like the transaction that doesn’t have a high enough fee, we call that the parent and the one that’s spending it. So it’s the child on the transaction graph pays for the parent’s fee is essentially what happens.

Stephan Livera:

Gotcha. So essentially we’re using RBF and CPFP to help deal with the fee problem, as well as the anchor output concept, which is also in lightning as well.

Nadav Kohen:

Yeah. And we have a bunch of, you know, similar concerns about, you know, mempool pinning and all sorts of other really complicated things that Antwan knows more about than I do. So I might not be able to answer.

Stephan Livera:

Speaking of, I mean, we’ve, so we’ve mostly spoken through unchain DLC. Let’s talk a little bit about what DLC look like when they’re done using lightning.

Nadav Kohen:

Yeah. So the kind of cool thing about lightning channels is that they let you put kinda any output you could put unchain. You could theoretically put on a lightning channel. So, you know, we have our normal ones, like two local and two remote, or just these kind of plain, or sorry to remote is just this plane kind of this key gets these funds and to local uses like a lock time on it with like, you know, the revocation spending path and we use Bitcoin script and then, you know, you can put DLC on lightning channels and like that’s all in today’s lightning. Those are the three things you can put on a lightning channel. But there are a lot of different independent, well, maybe not all independent, I’m sure they’re working together to some extent, but there are many efforts to kind of allow lightning implementations to be more general so that you can cause in theory, there’s nothing stopping us from implementing a lightning node and a lightning channel in which you can, you know, negotiate arbitrary outputs to put on your channel.

Nadav Kohen:

And so since that’s the case, you can put a discreet log contract, like our funding output. You can put a funding output on your channel. So, you know, you have like your normal channel with say, each of us have, you know, two Bitcoin on each side of the channel. And then we like, instead of moving some amount of funds into an HTLC, we can both move some funds into a DLC that just lives on our channel, much like an HTLC lives on a channel. And then you know, when the DLC is done and the Oracle is broadcast at signature we can use that much. Like you would use a hash pre-image on lightning to kind of just say, we should update, get rid of this DLC, send funds the way that they’re supposed to go and then do that all without anything ever hitting the blockchain.

Nadav Kohen:

And then because we’re using outputs that are compatible to go on chain if ever there’s a disagreement and stuff does end up on chain, then you can always execute it, you know, the same as you would an on chain DLC. So essentially, you know, if you think of, you know, lightning HTLC as a slightly modified version of just like this weird on chain contract you could do on Bitcoin, which says, like reveal this pre image to claim these funds. Otherwise I get it back after this timeout, we can take our DLC output as we were thinking about it on chain, and just throw that on a commitment transaction.

Stephan Livera:

I say, so we could, I guess, modify that example we did before, and let’s say, I have a channel open with you, and then we can then set up a lightning DLC. Now, would I have to, let’s say, I didn’t have enough money in that channel open with you that I wanted, but I wanted to bet more than that. Would I have to like splice or what would that sort of thing look like there?

Nadav Kohen:

Yeah. So I haven’t thought about this before, but I’m pretty sure you could MPP or amp maybe not MPP, you might have to AMP, but yeah. In the future lightning network where we have where we have PTLC instead of HTLC and some other stuff, I believe you should be able to use funds from other channels, if you’re clever or yeah, I guess there is this kind of fundamental issue of for things for DLC to work in a lightning channel, you do need kind of the available liquidity to go into that DLC. So yeah there are a couple of different ways you could try and like add to this by using routed DLCs, which require PTL CS and some other fancy stuff barrier escrows in particular to be implemented on lightning which we’ll get someday in the future hopefully in the near future, depending on how Tapper goes.

Nadav Kohen:

But yeah, so I guess short answer is you can’t really do it if you don’t have the liquidity in the channel without adding say liquidity to the channel which is something we’ll be able to do someday. But the longer answer is in the future, there will be ways of doing like almost amp or multipath DLCs or DLC, like things using multiple paths, just going to be weird. But I will note that one of the cooler use cases on lightning, in my opinion actually doesn’t require very much liquidity. So the idea is to kind of create synthetic synthetic assets on lightning using DLCs. So I think a year or two ago, it might’ve been two years now. There’s this paper called the network or a white paper about something called the rainbow network where you could essentially have lightning like channels that act as kind of synthetic assets.

Nadav Kohen:

So say that you know, I’m a business who wants to use the lightning network, but I don’t want to be exposed to BTC volatility. And I do all of my bookkeeping and say USD. So I want with a lightning channel, but I want to have like USD, like fixed USD value in, on my side of the channel and say, you want to go long on BTC USD, the trading pair. Then what we can do is we can open up a channel and like every 10 seconds based on some price feed, we move funds back and forth, depending on how the price moved. So that I have a fixed USD amount. So say I have like a hundred dollars worth in there, but keep in mind in reality, you know, I have Bitcoin in there, but say 10 seconds later, the price went up and I now have like $102.

Nadav Kohen:

Well then I have to send you $2 worth of Bitcoin over the channel to your side so that I have a fixed USD amount. And likewise, if the price goes down, you send money over to my side. So you can picture like an advocate or something. And you know, the beads are moving back and forth in this channel to make sure that one side has a fixed USD amount. The issue with this is that it’s kind of fully trusting, right? Like if there’s a big price jump against you, you could just like stop sending money over, like just don’t send that last payment it’s too big or something like that. So that’s the issue that DLC solve in this situation. So what you can do is rather than just having funds be sent back and forth directly in a fully trusted manner, you can put a relatively small DLC output on your channel to kind of trust this the, hold some collateral.

Nadav Kohen:

And so the reason that it’s trustless is because if the other party stops responding you can just close out that channel and execute that DLC and get the funds that are in there. So essentially what we do and we update the channel now is rather than moving the funds directly back and forth between us on the channel, you can think of there being kind of like this pot in the middle of our channel. And one person gets to take money out of the pot and the other party gets to put money into the pot. So there’s kind of this intermediate output that is, or this intermediate step that functions kind of the same way, right? At the end of the day, one of us is getting some money. One of us is losing some money or the other way but because the pot of money or the pot in the middle is a DLC output if one party stops cooperating, then those funds get distributed based off of how they should have if they were cooperating.

Nadav Kohen:

So you can get these kind of fully trustless synthetic asset channels on the lightning network. And then what that lets you do is say, you know, I want to have a fixed USD amount and I can have like a wallet that, you know, kind of denominates things in terms of USD. And I can still use the lightning network and pay people for accepting Bitcoin over the lightning network and receive money. And it’ll look to me like I’m receiving USD over the lightning network when in reality, people were paying me in lightning Sats. And all kinds of things like that.

Stephan Livera:

Very cool. I could see maybe someone could build a wallet service out of that and, you know, kind of market that to the developing world and have it sort of show fiat money on the front end for the user who doesn’t need to know all the technical stuff, but in the background, there’s actually just Bitcoin moving through the channels and stuff right?

Nadav Kohen:

Yeah, totally. Yeah. And honestly you can, you know, anything you can build the DLC on, you can create that thing as a synthetic asset on lightning. So I always like to joke, like you could take like I don’t know can Newton’s stats and, have Patriot points, like how well are the Patriots doing today? And, you know, the better they’re doing the more I have, or the more I have in my channel and the worst they’re doing the less I have in my channel.

Stephan Livera:

Right.If you’ve got a bet on at that time or something. Yeah.

Nadav Kohen:

Yeah. But yeah, I think the more realistic use cases people will use synthetic assets to kind of either not have exposure to Bitcoin or to have exposure to something else while keeping most of their funds fully liquid and just, you know, being part of the lightning network.

Stephan Livera:

Yeah. Very cool. One other area around private key management. Now I know Chris has done a talk and I think a presentation about stuff like in terms of lightning, which keys are required to be hot. What’s the equivalent of that in DLC, which case need to be hot and which ones can be kept cold.

Nadav Kohen:

Yeah. So one of the kind of cool things about DLCs once. So I guess there’s talking about like the actual setup, and then there’s talking about like, you know, the many years as you wait for the event to happen and say, or, you know, it could just be a couple seconds, but regardless in that latter portion, the cool thing is that you need no hotkeys whatsoever. Like you do not need to be signing anything, even when the event happens. So long as you just have these adapters signatures lying around you can just use your and your counterparties, adapters signatures, and tweak them and get valid signatures without ever touching your private keeps. So in theory, you don’t need your private keys at all once everything has been set up and signed for. So the only time you ever need to touch your keys when doing a DLC is at the very beginning, when you are signing all of the contract execution transactions and signing the funding transaction.

Nadav Kohen:

But after that for the users, all of your keys can be cold, which is super cool. Yeah. And then I guess for Oracle’s, you know, there are other key considerations, but that can, you know, get into some crazy stuff like threshold signing and stuff like that. But yeah Oracles obviously also care a lot about how they manage the keys and how hot or cold they should be and things like this. Yeah. So we’re, I guess this is kind of a, we’re beginning to figure out what best practices are for Oracles and clients and stuff around key management, but it is pretty early. And even, you know, the idea of you know, you don’t need any hotkeys. Well, right now, like all of the implementations are for wallets, like Bitcoin S or whatever else, and not yet coldcard compliant or whatever else. So it is quite early, but on paper you don’t, you don’t need any of your private keys, which is good.

Stephan Livera:

Okay. So let’s talk about from a spec perspective and the different clients and so on. Can you give us another view there, what’s the model you’re following and give us a bit of a lay of the land for someone who’s not familiar, who are the main players in the DLC world, and who’s contributing to the spec and who’s got a client and so on.

Nadav Kohen:

Yeah. So the github repo is github.com/discreetlogcontracts/DLCspecs. If you just Google part of that, I’m sure you’ll find it. And on here we are building together kind of a bunch of documents specifying exactly. You know, how to build your transactions, how to compute your fees, how to communicate over the wire to set up the DLC, how Oracle’s should be signing things, all of these different things. Currently there are four work in progress implementations. When I say work in progress many of them are already, or at least two of them I know are spec compliant and compatible with each other, which is super exciting, Bitcoin S and CFD DLC which Bitcoin S is an implementation me and Ben Carman of Suredbits have been working on, and they’re still working on adding new features and such and CFD, DLC is being worked on and maintained by Tebeau of crypto garage over in Japan.

Nadav Kohen:

And that is a, so ours Bitcoin S is a Scala implementation. CFD, DLC is a C++ implementation, but it has a JavaScript wrapper. So if you’re either in C++ land or JavaScript plan, a CFD DLC is there for you if you are in JVM plan. So Java, Scala, Kotlin, Bitcoin S is there for you there is an implementation called rust DLC, which Tebeau is also working on, I think maybe with a little bit of help from Antoine Riard. And there’s N DLC, which is a C sharp implementation meant to be used with BTC pay server, which Nicolas Dorier is working on. So those are the four implementations. And I mentioned a lot of the people who are working on the specs and on implementing DLCs, a person who I haven’t mentioned, who is also very active Lloyd Fournier is a square crypto grant recipient, who has been working a lot on kind of the Oracle side of things.

Nadav Kohen:

And he also is the one who figured out how to do adapter signatures in ECDSA, so that we can do DLCs today instead of using complicated scripts like we were earlier or waiting until taproot. So we use Lloyd Fournier’s cool ECD based adapter, signature scheme. And he is working on a spec for that. It’s not up yet or out yet, but as far as the specs that are already out we have a couple things that are kind of more high level. Like there’s a resources doc, there is a read me, there is an introduction. So lots of links out to cool things in blog posts and stuff from there. If you’re just curious and want to take a look, and then there are a bunch of more substantive docs about transactions and protocols and messaging and some more in the works and PR’s. Yeah, Yeah. And things are quite active yeah.

Nadav Kohen:

On here. I mean, sometimes it’s a bit wavy cause we’re working on writing some big doc can everyone’s debating and then some big stuff gets merged in. But yeah, I would say there’s a lot of progress happening and we’re getting close to some cool things being able to be done right now. You can already on, I think all of the implementations do simple things, like say bet on a sport sporting event, you know, kind of small number of outcomes, kind of things. I’m currently on Bitcoin S as you know, this week and next I am working on kind of more generalized, interesting derivative contracts based on various things and writing spec for that. But yeah, if you’re interested in contributing totally, you know, reach out we kind of all live on the, there are a couple of different places you can come to the Suredbits Slack, you can come to the lightning dev kit Slack, which is where we normally speak for historical reasons. Cause we were originally interested in like doing things with trust lightning and stuff like that. And also we have a telegram chat. That’s less technical. It’s not so much where we communicate for development and more so like, you know, people interested, DLCs looking for resources and stuff like that. Yeah. I forget what the link is to that, but yeah.

Stephan Livera:

Okay, great. And I guess maybe just a final question what are some of the next key pieces that need to slot into place for DLC?

Nadav Kohen:

Yeah, so a lot of it is just kind of figuring out the low level details of like, you know, which Sig hash algorithms we want to use on which inputs and, you know, stuff like that, but that stuff is nearly finalized. I would say we’re getting pretty close on that front. So we’re nearing kind of a nice stable version zero the kind of main, and next steps is building out a kind of Oracle’s. So Ben is working a lot on Bitcoin S side of things building out an Oracle. And I know that Lloyd is also working on his Oracle and I think Tebeau might also be working on an Oracle. So we’re all kind of working on Oracle, seeing what works and what doesn’t and working to put together kind of a standard for how Oracles should communicate their announcements and commitments and all of these kinds of things.

Nadav Kohen:

And then I would say that yeah, aside from kind of standardizing Oracles and making it easy and, you know, open source and all of these kinds of things to run an Oracle or, you know, experiment with Oracles as well as DLCs. I would say the next big step that a lot of progress is being made on is kind of making cool contracts. So I’m working right now on like a spec that will let you like, you know, take any payout curve you want and just like interpolate it with a couple of points to succinctly communicate, you know, kind of like a general function for like, you know, do you want like a straight line kind of like a colored future? Or do you want like some curvy thing to mimic, like some, one of BitMEX’s derivatives or, you know any kind of contracts you want to do on that front? Yeah. And yeah, there are like so many things, but I would say that that’s the main two places that I think are people are making a ton of progress on right now.

Stephan Livera:

Excellent. Well, Nadav, thanks very much for joining me today. So before we let you go, where can listeners follow you online?

Nadav Kohen:

Yeah. I’m at, Oh boy, am I going to get this right? I always mess up. I’m @nadav_kohen with a K on Twitter. I don’t tweet too much, but my DMS are open I suppose. And if you want to like, come bombard me with questions, feel free to do so. Come join the Suredbits Slack or otherwise the telegram for DLCs. And also, I guess you can email me at nadav@suredbits.com. I guess my online presence is lacking, but if you have questions do feel free to reach out.

Stephan Livera:

Fantastic. Thanks for joining me.

Nadav Kohen:

Thanks for having me.
