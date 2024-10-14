---
title: Pieter Wuille (part 2 of 2)
transcript_by: Michael Folkson
tags:
  - bitcoin-core
speakers:
  - Pieter Wuille
date: 2020-01-28
media: https://www.youtube.com/watch?v=Q2lXSRcacAo
episode: 2
aliases:
  - /chaincode-labs/chaincode-podcast/2020-01-28-pieter-wuille-part2/
---
Jonas: We are gonna pick up where we left off in episode 1 with a discussion of lessons learned from the 0.8 consensus failure. We then go on to cover `libsecp` and Pieter's thoughts about Bitcoin in 2020. We hope you enjoy this as much as we did.

John: Ok I have a bunch of questions from that. One is what are the lessons from that?

Pieter: One of the things I think learned from that is specifying what your consensus rules is really hard. That doesn’t mean you can’t try but who would’ve thought that a configuration setting in the database layer you are using actually leaked semantically into Bitcoin’s implicitly defined consensus rules. You can attribute that to human failure of course. We should’ve read the documentation and been aware of that.

John: Would testing have caught this?

Pieter: Probably things like modern fuzzing could’ve found this. Who knows right? There could be a bug in your C library. There can be a bug in your kernel. There can even be a bug in your CPU.

John: In your hardware, anywhere.

Pieter: Exactly. We can talk about the boundary in trying to abstract the part of the codebase that intentionally contributes to consensus but it is very hard to say clearly this code has no impact on consensus code because bugs can leak. I think one of the things to learn there is you really want software that is intended for use in a consensus system where not only you have the requirement that if everyone behaves correctly everybody accepts the right answer but also that everybody will disagree about what is an invalid piece of data in lockstep.

John: That condition is much harder.

Pieter: That’s much harder. It is not a usual thing you design things for. Maybe a good thing to bring up is [BIP66](https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2015-July/009697.html) DER signature failure. You also had getting rid of OpenSSL on the list of things to talk about. Validation of signatures in Bitcoin’s reference code used to use OpenSSL for validation. Signatures were encoded in whatever data OpenSSL expects.

John: Let’s take a step back and talk about Satoshi implementing Bitcoin. Satoshi wrote a white paper and then produced a reference implementation of Bitcoin. In that reference implementation there was a dependency on OpenSSL that was used for many things.

Pieter: Correct. It was even used for computing the difficulty adjustment I think. It was used for signing. At some point it was used for mining.

John: OpenSSL is a very widely used open source library. It has been deployed in many applications for many years. It wasn’t a bad choice to use OpenSSL.

Pieter: I think it was an obvious choice from a standard software engineering perspective. It was a very reasonable thing to do without things we’ve since learned. What this meant that was even though ECDSA and secp256k1 curve have nicely written up specifications it wasn’t actually these specifications that defined Bitcoin signature validation rules. It was whatever the hell OpenSSL implemented. It turns out what OpenSSL implemented isn’t exactly what the specification says.

John: And isn’t exactly consistent across different platforms.

Pieter: Exactly. What we learned is that the OpenSSL signature parser, at the time, this has since been fixed, at the time allowed certain violations of the DER encoding specification which is a way of structured data in a parsable way that ECDSA specification refers to. OpenSSL used the I think now widely considered bad idea philosophy of being flexible in what you expect and being strict in your output exactly because of the inconsistencies it introduced. OpenSSL allowed signatures that violated the spec. This didn’t mean that this permitted forging a signature. Someone without a private key still could not construct anything that OpenSSL would accept. The problem was that someone with a private key might construct a signature that some versions would accept and others wouldn’t. Indeed in one of these permitted violations of DER it had a bound on the size of a length field and that bound was 32 bits for 32 bit platforms and 64 bits for 64 bit platforms. You could construct a signature at the time that says “The length of this integer is the next 5 bytes.” Those 5 bytes would just contain the number 32 or 33.

John: To get a bit more specific. When we create a signature in ECDSA we have two values, a r value and a s value. Together that forms a signature. When we talk about encoding we’re talking about how we put those values into bits that we transmit across the network. DER encoding has a bunch of fields as well as the r and the s fields which are saying this is the length of the thing…

Pieter: It would start by saying “Here is a concatenation of two things and it is this many bytes.” Then it would say “The first element is an integer and it is this many bytes.” Then you would actually have the data. “The next thing is an integer. It is this many bytes and here is the data.” Then Bitcoin adds a signature hash flag at the end but that is not part of the DER thing. This encoding of the r and s values could either say “It is the next n bytes up to 126” or something but if it is more than that it would include a marker that says “The length of the next field is given in the next n bytes.” The maximum length of that indirect size field was platform dependent in OpenSSL.

John: So what do you do about that? You’ve discovered that Bitcoin is inconsistent with itself.

Pieter: In a similar way that 0.7 and everything before it were inconsistent with itself due to this BDB lock issue. This was a much more concrete thing. You’d know exactly that I can construct a signature that these platforms will accept and these won’t. This wasn’t non-deterministic, this was deterministic. It was just dependent on the platform. The problem was fixing this wasn’t just a database update, this was implicitly part of our consensus rules. So what we needed to do was fix those consensus rules. That is what BIP66 was designed to do. The full rationale for BIP66 wasn’t revealed until long after it was deployed because this was so trivial to exploit. We did keep that hidden for a long time. BIP66’s stated goal which was correct in part was being able to move off OpenSSL. Let’s switch to a very well specified subset of signatures which everybody already produces. The signing code that people were using was sufficiently strict apart from a few other implementations this was generally not a problem. There were concerns at the time about miners that didn’t actually do full validation which would have made it even easier to broadcast such a signature on the network and get it included. That was interesting. Again taught us that even when you think you have a specification of what your consensus rules are everybody would’ve thought there’s this document that specifies ECDSA and secp256k1, that is our specification. It turns out it wasn’t.

John: Consensus is slippery and touches everything.

Jonas: When you’re sitting on an exploit like that, when you’re aware that something is open for exploitation how does that change the process and how do you think about coming up with a solution? You have a time constraint I guess.

Pieter: Given it had been there for a long time there are trade-offs like who do you tell? How fast do you move to fix this because moving too fast might draw suspicion, moving too slow might get exploitable. Really these things always need to be considered on a case by case basis.

John: I think that brings us nicely to the third PR or family of PRs that I have on my list or projects that you’ve contributed to which is libsecp. Can you give us a bit of background on what the genesis of that project was and where it came from?

Pieter: It is not actually known I think why Satoshi picked the secp256k1 curve which was standardized but a very uncommon choice even at the time. I don’t dare to say when, maybe 2012, a post on Bitcointalk by Hal Finney about the special properties that this curve has and presumably why it was picked because it had this promise of accelerated implementation. What this was a particular technique that would allow faster implementation of elliptic curve implementation using an efficiently computable endomorphism. I won’t go into the details unless you want me to but it is a technique that gives you a percentage speedup for multiplication. It also makes certain requirements on the curve that not everyone is as happy with. It also gives you a small speedup for attackers but generally you want an exponential gap between the time it takes for an attacker and honest user anyway. Hal made this post saying “I looked into actually how to implement this particular optimization for the curve. Here is a bit of the math.” I think maybe he had some proof of concept code to show it but I was curious to see how much speed up is this actually going to give. I first tried to look at can I integrate this in OpenSSL itself? Because OpenSSL didn’t have any specialized implementation for this curve nor for this optimization technique in general. I started doing that but OpenSSL was an annoying codebase to work with to say it mildly. I thought how about I just make my own implementation from scratch just to see what the effect is. This started as a small hobby project thinking about… To be fair it is a much easier problem if you are only trying to implement one algorithm for one curve compared to a general library that tries to do everything in cryptography. I had the option of picking specific field representation for how are you going to represent the x and y coordinate. I learned some techniques from how other curves like ed25519 were implemented. I used some of those techniques. I started off by only implementing this optimized construction actually. It turned out when I was done it was maybe a factor of 4 faster than OpenSSL which was a very unexpected result. I hadn’t imagined that with fairly little work it would immediately be that much better. I guess it made sense just by being so specialized and being able to pick data structures that were specifically chosen for this curve rather than generic. You get actually a huge advantage.

John: At this point this was still just a …

Pieter: Yes. This was 2013 probably.

John: Just a personal project. You weren’t thinking about it being part of Bitcoin Core.

Pieter: I open sourced this. It attracted some contributions from Greg Maxwell, not Hal Finney, Peter Dettman who is a major contributor to the Bouncy Castle cryptographic library who by now probably came up with half of the algorithms in libsecp. Sometimes incremental improvements, sometimes original research and algebraic techniques to optimize things here and there. That has pushed the performance every time a couple of percent here and there, it adds up. It was assembly implementations for some routines added by people. After a while including lots and lots of testing that was added I think in 0.10. The signing code was switched in Bitcoin Core to it and then 0.12 the validation code was switched to it. This was after BIP66 had activated and we knew the rules on the network are exactly this DER encoding and nothing else. Interestingly by that time this efficient endomorphism GLV optimization was made optional and off by default in libsecp because of potential concern about patents around it. It is kind of ironic that this project started as an attempt to see the benefit was of this optimization and in the end choosing not to use it. But despite that it was still a very significant performance improvement over OpenSSL.

John: Did you feel some urgency after BIP66 to move across to libsecp?

Pieter: Not really. There was until very recently this vague concern that OpenSSL is a huge library with a huge attack surface. It was not designed with these consensus like applications in mind. At least as far as the signature validation parsing went I think at the time we felt that now we understand the scope of what OpenSSL does here and we had restricted sufficiently. We were fairly confident that that exactly wasn’t going to be a problem anymore. It was more the unknown unknowns for all the other things. I don’t know how fast, I don’t remember.

John: To enumerate some of the benefits of switching to libsecp. It is extremely well tested. It has almost 100% code coverage I believe?

Pieter: I think so.

John: It is much faster than OpenSSL.

Pieter: I think OpenSSL has caught up a bit since.

John: There are many things about libsecp that make the API safe for users I think.

Pieter: It is very much designed to be a hard to misuse library so it doesn’t really expose many low level operations that you might want from a generic cryptographic toolkit. It is designed with fairly high level APIs in mind like validate a signature, parse a signature, create a signature, derive a key and so forth.

John: And lots of thought about constant time and avoiding…

Pieter: Yes it was also from the start designed to be side channel resistant or at least the typical side channels you can protect against in software namely not having code paths that depend on secret data, not having memory accesses that depend on secret data. Despite that actually from the start it didn’t actually do that. There was some timing leak in very early code that was probably very hard to exploit. There was some table with precomputed values and you need to pick one of them based on secret data which is a problem. I think what we did was spread out the data so that there’s one byte of every table entry, say there’s 16 table entries, the first 16 bytes contain the first byte of every entry. Then the next 16 bytes contain the second byte of every entry and so on. You would think now it needs to access all groups of 16 bytes and given reasonable assumptions about architectures that generally have cache lines of 64 bytes you would think it is going to access every cache line so there shouldn’t be any leak anymore. It turns out there is a paper that actually shows even in this case you leak information because the first byte and the second byte… things in a cache line there is a very small difference in timing when they are available they can be observed. The fix is actually access every user conditional move construction where you actually read through every byte always.

Jonas: As you talk about the history and certainly you’ve forgotten more about Bitcoin than most of us will ever learn, as you go back and you think about Satoshi’s reference implementation what are things that you would imagine you would want to do from the beginning? Things that are baked into the software that are difficult to shake even now as you’ve made contributions over the years that you would want to have done differently from the beginning?

Pieter: You mean in code design or actually how Bitcoin works?

Jonas: I think either. I think in terms of code design putting most of the code in one file wasn’t particularly helpful from the beginning. In terms of design choices.

Pieter: It is of course slow to change things but I think given enough time if you are just talking about code design questions, if we have agreement we need to move to this other design we can do it whatever it is. You mention of course everything in one file in the 2010 codebase, the wallet and the consensus validation were all in one file including direct calls to the UI. That was really hard to reason about. The wallet tracking which outputs had been spent was actually done through a callback from the script verifier that would tell the wallet “Hey I’ve seen a validation with this input.” This was really hard to reason about. Of course these days there is a lot more complexity so I don’t want to claim that it is today easier to reason about things. Relative to its complexity and how much it was actually doing it was fairly hairy back then.

John: Yeah I think we’ve made enormous strides. There’s a well defined interface between the wallet and the node so we can be confident that it is not involved in consensus.

Pieter: Yes exactly. There is still a lot of work to do there too but I think we are getting there. Your talk about how Bitcoin could have been designed differently, that is a very hard question because you inevitably run into philosophical questions like if it were to have been designed differently would it have taken off? Especially if you go into questions like economic policy. That’s really hard to guess. I think there are lots of things we have learned. The concept of P2SH, what was clearly not present in the original design, it could have been done in a much simpler way if there would’ve been something like P2SH from the beginning. Yet it seems so obvious that this is preferable because before P2SH if you personally have some multisig policy, nobody was using multisig at the time, I guess that was part of the reason. But if you would’ve wanted to use a multisig policy to protect your coins with a device or cold storage key and an online key you would’ve somehow needed to convey to anyone who wanted to pay you to construct this script that includes your policy. That is annoying for multiple reasons like a) that is none of their business, why do I need to tell you “Hey look I’m using a multisig policy, it just for my own protection.” Secondly you would be paying the fees for paying to my complex script. That should not have been a concern of yours either. Lastly everything you put in an output leaks into the utxo set and as we now know the size of the utxo set is a critical scaling parameter of the system.

John: I’ll add fourthly you would have really long addresses which would be kind of annoying.

Pieter: Exactly you would need a standard for conveying that information that would be variable length inevitably if you go for big scripts. I don’t even think that all of these advantages were talked about the time when P2SH was created. I think it was just the last one. We have no address for this, it is really hard to create one. We can make it simpler by hashing the script first. I think the other advantages were things that we’re only realized later, how much of a better design this is. Of course we have since iterated on that, SegWit I think is clearly something that should have been done from the beginning. The fact signatures leak into the txid made it really hard for all kinds of more complex constructions. At the same time Bitcoin was the first thing in its class and it is unrealistic to expect it to get everything right from the beginning. Thankfully I think we’ve learned very well how to do safe upgrades to some of this.

John: I agree entirely that this isn’t really an exercise for faulting Satoshi for the mistakes. But if I could wave a magic wand SegWit from the genesis block would be great because then the block could commit to the signatures, the wtxid whereas now it doesn’t.

Pieter: In SegWit it does. In SegWit there is a coinbase output that contains a hash with the root of a Merkle tree that commits to all wtxids.

John: Right, yes. But you don’t know that until you deserialize the transactions from the block which is a little bit annoying.

Jonas: How do you think about how to spend your time on Bitcoin? There are so many ways to get nerd sniped and so many directions you could contribute to. What are you excited about and then how do you feel the pull of your personal excitement versus the pull of what’s necessary for someone like you to contribute to Bitcoin?

Pieter: That is a good question, I don’t have a good answer. I try to work on things I’m excited about but sometimes this also means following through on something after you’ve lost some of the excitement about it because you have worked on this and people expect you to continue. It is a hard question. I expect this in general in open source to be a problem. There is no set direction and ultimately people choose how to spend their own time themselves. What am I excited about? I’m happy with the progress we’ve made with Taproot review and how that is going. I’m excited to see that progress further. There are some interesting changes people are working on related to the peer-to-peer protocol, things like Erlay that I contributed to. There are too many things to mention.

John: I think Taproot, Schnorr plus Erlay is a good start for things to get excited about. Shall we wrap up there? Thank you Pieter.

