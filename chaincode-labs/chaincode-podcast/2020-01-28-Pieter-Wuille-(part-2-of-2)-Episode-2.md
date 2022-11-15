---
title: Pieter Wuille (part 2 of 2) - Episode 2
transcript_by: Whisper AI & PyAnnote
categories: ['podcast']
tag: []
---

Chaincode Labs podcast: Pieter Wuille (part 2 of 2) - Episode 2

SPEAKER_00: I try to work on things that I'm excited about, but sometimes this also means following through on something after you've lost some of the excitement about it.

SPEAKER_01: So here's part two of our conversation with Peter Waller. If you haven't listened to part one yet, you should go back and download that. Listen first and then come back here.

SPEAKER_02: We're going to pick up where we left off in episode one with a discussion of lessons learned from the 0.8 consensus failure. We then go on to cover LipsetP and Peter's thoughts about Bitcoin in 2020. We hope you enjoy this as much as we did.

SPEAKER_01: Okay, so I have a bunch of questions. One is, what are the lessons from that?

SPEAKER_00: One of the things I think learned from that is that specifying what your consensus rules are is really hard. That doesn't mean you can't try, but who would have thought that a configuration setting in the database layer you're using actually leaked semantically into Bitcoin's implicitly defined consensus rules? You can attribute that to human failure, of course. We should have read the documentation and been aware of that. With testing, of course. I think probably things like modern fuzzing could have found this, but who knows, right? Because you're dealing with, say, there could be a bug in your C library. There can be a bug in your kernel. There can even be a bug in your CPU. In your hardware. Yeah, exactly. Anywhere. That we can talk about a boundary in trying to abstract out the part of the code base that intentionally contributes to consensus. But it's very hard to say clearly this code has no impact on consensus code because bugs can leak.

SPEAKER_01: Yeah, exactly. Anyway.

SPEAKER_00: things to learn there is you really want software that is intended for using a consensus system where not only you have the requirement that if everyone behaves correctly everybody accepts the right answer but also that everybody will disagree about what is an invalid piece of data in lockstep right and

SPEAKER_01: Thanks for watching! that condition is much harder.

SPEAKER_00: That's much harder and it it is not a usual thing you design things for I Think if you look at that say It's maybe a good thing to bring up the the VIP 66 Der signature Failure

SPEAKER_01: Mm.

SPEAKER_00: Because you also had getting rid of OpenSSL on the list of things to talk about. This is a... So Bitcoin signatures or validation of signatures in Bitcoin's reference code used to use OpenSSL for validation and signatures were encoded in whatever data OpenSSL expects. The...

SPEAKER_01: But let's take a step back and talk about Satoshi implementing Bitcoin Satoshi created or wrote a white paper and then produced a reference implementation of Bitcoin and In that reference implementation. There was a dependency on open SSL. Correct. That was used for many things correct

SPEAKER_00: It was even used for computing the difficulty adjustments, I think. It was used for signing. At some point it was used for mining.

SPEAKER_01: Okay. Okay. An open SSL is a very widely used open source library, it's been deployed in many applications for many, many years, so it wasn't a bad choice to use open SSL.

SPEAKER_00: I think it was an obvious choice from like a standard software engineering perspective. It was a very reasonable thing to do without the things we've since learned. What this meant was that even though ECDSA and the SECP256K1 curve have all nicely written up specifications, it wasn't actually these specifications that define Bitcoin signature validation rules. It was whatever the hell OpenSSL implemented. And it turns out what OpenSSL implemented isn't exactly what the specification says.

SPEAKER_01: and isn't exactly consistent across different platforms.

SPEAKER_00: Exactly. So what we learned is OpenSSL signature parser at the time, this has since been fixed, but at the time allowed certain violations of the DER encoding specification, which is a way of structured data in a parsable way that ECDSA specification refers to. OpenSSL used the, I think, now widely considered bad idea philosophy of being flexible in what you expect and being strict in your outputs exactly because of the inconsistencies it introduced. OpenSSL allowed signatures that violated the spec. And mind you, this didn't mean that this permitted forging a signature, right? Someone without a private key still could not construct anything that OpenSSL would accept. The problem was that someone with a private key might construct a signature that some versions would accept and others wouldn't. Because as you said, indeed in one of these permitted violations of DER, it had a bound on the size of a length field. And that bound was 32 bits for 32-bit platforms and 64 bits for 64 platforms. So you could construct a signature at the time that says the length of this integer is the next five bytes. And then those five bytes would just contain the number 32 or 33.

SPEAKER_01: So to get a bit more specific, when we create a signature in ECDSA, we have two values, an R value and an S value, and together, that forms the signature. And when we talk about encoding, we're talking about how we put those values into bits that we transmit across the network. Correct. And DER encoding has a bunch of fields, as well as ER and ES fields, which are saying, this is the length of the thing I'm about to do. It would. Right.

SPEAKER_00: it would start with saying here is a concatenation of two things and it is this many bytes and then it would say the first element is an integer and it is this many bytes and then you would actually have the data the next thing is an integer it is this many bytes and here is the data and then bitcoin adds a signature hash flag at the time at the end but that's not part of the dr thing um and so this this encoding of the r and s values it could either say it is the next n bytes up to 126 or something but if it is more than that it it would actually include a marker that that says the length of the next field is given in the next n bytes and the maximum length of that indirect size field was platform dependent in open ssl

SPEAKER_01: Okay, and so, so what do you do about that?

SPEAKER_00: What do you do about that?

SPEAKER_01: You've discovered that Bitcoin is inconsistent with itself.

SPEAKER_00: Yeah, well, in a similar way that that 0.7 and everything before it were inconsistent with itself due to this PDB lock issue, this was a much more concrete thing like you know exactly like these platforms, like I can construct a signature that these platforms will accept and these won't. This wasn't non-deterministic. This was deterministic. It was just dependent on the platform. So the problem was fixing this wasn't just a database update. This was implicitly really part of our consensus rules. So what we needed to do was fix those consensus rules. And that is why what BIP-66 was designed to do. The full rationale for BIP-66 wasn't revealed until long after it was deployed because this was so trivial to exploit. We did keep that hidden for a long time. And BIP-66's stated goal, which was correct, was in part being able to move of OpenSSL. So it says, well, let's switch to a very well specified subset of signatures, which everybody already produces, like the the signing code that people were using was was sufficiently strict that apart from a few other implementations, this was generally not a problem. Yeah, there were concerns at the time about miners that didn't actually do full validation, which would have made it even easier to broadcast such a signature on the network and getting it included. Yeah, that was interesting. And it, again, taught us that even when you think you have a specification of what your consensus rules are, like everybody would have thought, well, there's this document that specifies ECDSA and SIGP256K1. That is our specification. It turns out it wasn't. Right. Yeah, that was interesting. And it, again, taught us that even when you think you have a specification of what your consensus rules are, like everybody would have thought, well, there's this document that specifies ECDSA and SIGP256K1. That is our specification. It turns out it wasn't.

SPEAKER_01: Consensus is kind of slippery. Yeah. Touches everything.

SPEAKER_00: Yeah.

SPEAKER_02: When you're sitting on an exploit like that, when you're aware that something is open for exploitation, how does that change the process? Or how do you sort of think about coming up with a solution? You don't sort of have the, maybe the, you have a time constraint, I guess.

SPEAKER_00: Given that it had been there for a long time Yeah, it it it changes and it becomes a very And there's trade-offs like like who do you tell? How fast do you move to fix this because Moving too fast might draw suspicion moving too slow might make it exploitable But really these things always need to be considered on a case-by-case basis

SPEAKER_01: Well, I think that brings us nicely to the third PR, or family of PRs that I had on my list or projects that you've contributed, which is LibSecP. So can you give us a bit of background on what the genesis of that project was, where it came from?

SPEAKER_00: Yeah, so it's not actually known, I think, why Satoshi picked the SECP256K1 curve, which was standardized, but a very uncommon choice even at the time. But there was, I don't dare to say when, maybe 2012, a post on Bitcoin Talk by Hal Finney about the special properties that this curve has and presumably why it was picked because it had this promise of accelerated implementation. And what this was was a particular technique that would allow faster implementation of elliptic curve multiplication using an efficiently computable endomorphism. I won't go into the details unless you want me to, but it's a technique that gives you a certain percentage speed up for multiplication. It also makes certain requirements on the curve that not everyone is as happy with. It also gives you a small speed up for attackers, but that's generally, you want an exponential gap between the time it takes for an attacker and an honest user anyway. So anyway, Helm made this post saying, I looked into actually how to implement this particular optimization for the curve. Here's a bit of the math. I think maybe he had some proof of concept code to show it, but I was curious to see well, how much speed up is this actually going to give? And I first tried to look at, can I integrate this in OpenSSL itself? Because OpenSSL didn't have any specialized implementation for this curve nor for this optimization technique in general. So I started doing that, but OpenSSL was an annoying code base to work with, to say it mildly. And so I thought, well, how about I just make my own from scratch implementation just to see what the effect is. And this started as a small hobby project thinking about, to be fair, it is a much easier problem if you're only trying to implement one algorithm for one curve compared to a general library that tries to do everything cryptography. But so I had the option of picking a specific field representation for how are you going to represent the X and Y coordinates. I learned some techniques from how other curves like at 255.19 were implemented to use some of those techniques. I started off by only implementing this optimized construction actually, and it turned out when I was done it was maybe a factor four faster than OpenSSL, which was a very unexpected result. I hadn't imagined that with fairly little work, it would immediately be that much better. But I guess it made sense just by being so specialized and being able to pick data structures that were specifically chosen for this curve rather than generic, you get actually a huge advantage.

SPEAKER_01: advantage and at this point use this was still just a

SPEAKER_00: Oh yeah, this was 2013, probably.

SPEAKER_01: Just a personal project, you weren't thinking about it being part of Bitcoin Core.

SPEAKER_00: Then, yeah, I open-sourced this. It attracted some contributions from Greg Maxwell, Peter Dettman, who is a major contributor to the bouncy castle cryptographic library, who by now probably came up with half of the algorithms in libsecp, like sometimes incremental improvements, sometimes original research and algebraic techniques to optimize things here and there. That has pushed the performance like every time a couple percent here and there and it adds up. It was assembly implementations for some routines added by people that added things. After a while, including lots and lots of testing that was added, I think, in 0.10, the signing code was switched in Bitcoin Core to it and then 0.12, the validation code was switched to it. That was after BIP66 had activated and we knew the rules on the network are exactly this DER encoding and nothing else. Interestingly, by that time, this efficient endomorphism GLV optimization was made optional and off by default in libsecp because of potential concern around patterns around it. It's kind of ironic that this project started as an attempt to see what actually the benefit was of this optimization and then in the end, choosing not to use it. But despite that, it was still a very significant performance improvement over OpenSSL.

SPEAKER_01: So did you feel some urgency after BIP66 to move across to sec P?

SPEAKER_00: lip-seq-v which not not really it there there's of course this vague there was until very recently this vague concern well openSSL is a huge library with a huge attack surface it was not designed with these consensus like applications in mind but at least as far as the signature validation and parsing went I think at the time we felt well now we understand the scope of what openSSL does here and we had restricted it sufficiently that that I think we were fairly confident that that wasn't that exactly wasn't going to be a problem anymore it was more the unknown unknowns for for all the other things right so yeah I don't know how fast I think I don't remember

SPEAKER_01: And to enumerate some of the benefits of switching to Libsac-P, it is extremely well tested. It has almost 100% co-coverage, I believe.

SPEAKER_00: Yeah, I think so

SPEAKER_01: it's much faster than OpenSSL.

SPEAKER_00: Yeah, I think open as all has caught up a bit since but

SPEAKER_01: And there are many things about Libs.xp that make the API safe for users, I think.

SPEAKER_00: Yeah, it's very much designed to be a hard to misuse library, so it doesn't really expose many low-level operations that you might want from a generic cryptographic toolkit. It's designed with fairly high-level APIs in mind like validate the signature, parse the signature, create a signature, derive a key, and so forth.

SPEAKER_01: And lots of thoughts about constant time and avoiding time.

SPEAKER_00: Yeah, it was also from the start designed to be side channel resistant, or at least the typical side channels you can protect against in software, namely not having code paths that depend on secret data and not having memory accesses that depend on secret data. And despite doing that actually from the start, it didn't actually do that in the first, there was some timing leak in very early code that was probably very hard to exploit, but what we did was there was some table with pre-computed values and you'd need to pick one of them based on secret data, which is a problem, and I think what we did was spread out the data so that there's one byte of every table entry, like say there's 16 table entries, the first 16 bytes contain the first byte of every entry, and then the next 16 byte contains the second byte of every entry, and so on. And you would think, well, now it needs to access all groups of 16 bytes, and given reasonable assumptions about, you know, cache architectures that generally have cache lines of 64 bytes, you would think it's going to access every cache line so there shouldn't be any leak anymore. Turns out there's a paper that actually shows even in this case you leak information because the first byte and the second byte of things in a cache line, there's a very small difference in timing when they are available that can be observed. So the fixes actually access every user conditional move construction where you actually read through every byte always.

SPEAKER_02: I mean, as you sort of talk about the history, and certainly you've forgotten more about Bitcoin than most of us will ever learn, but are there, as you go back and sort of think about Satoshi's reference implementation, what are things that you would imagine you would want to do over from the beginning, things that are sort of baked into the software that are difficult to shake, even to now, that as you've made contributions over the years that you would want to have done differently from the beginning?

SPEAKER_00: You mean like in code design or like actually how Bitcoin works?

SPEAKER_02: I think either. I think in terms of code design, putting most of the code in one file probably wasn't particularly helpful from the beginning. But in terms of design choices, yeah.

SPEAKER_00: It's of course slow to change things, but I think over time, given enough time, if you're just talking about code design questions, if we have an agreement like this, we need to move to this other design, we can do it, whatever it is. You mention, of course, everything in one file, like in the 2010 code base, the wallets and consensus validation were all in one file, including direct calls to the UI. That was really hard to reason about. The wallet tracking, which outputs had been spent, was actually done through a callback from the script verifier that would tell the wallet, hey, I've seen a validation with this input, and this was really hard to reason about. Of course, these days there's a lot more complexity, so I don't want to claim that it's today actually easier to reason about things, but relative to its complexity and how much it was actually doing, it was fairly hairy back then.

SPEAKER_01: Yeah, I think we've made enormous strides. There's a well-defined interface between the wallet and the node, so we can be very confident that the box is not invoking consensus. Exactly.

SPEAKER_00: There's still a lot of work to do there too, but I think we're getting there You're talking about Like how could Bitcoin have been designed differently that that's a very hard question because you inevitably run into Philosophical questions like well if it were to have been designed differently would it have taken off? especially if you go into questions like you know economic policy and So that that's really hard to guess I think there are lots of things we have learned that like Say just the concept of P2SH What was clearly not present in the original design It could have been done in a much simpler way if it would have been something like P2SH from the beginning and and yet it seems so obvious that this is preferable because Before P2SH so every Like if if you personally have say some multisig policy Nobody was using multisig at the time, but I guess that was part of the reason but if you would have wanted to Use a multisig policy to protect your coin say with a device called storage key and an online key You would have somehow have needed to convey to anyone who wanted to pay you to construct the scripts that includes your policy and That that is annoying for multiple reasons like a that's none of their business Why do I need to tell you hey look I'm using a multisig policy It's just for my own protection Secondly you would be paying the fees for paying to my complex scripts And should not be a concern of mine either. So it shouldn't have been a concern of yours either and Lastly say Everything you put in an output leaks into the UTXO set and as we now know the size of the UTXO set is a critical scaling parameter of the system, so You

SPEAKER_01: And I'll add fourthly, you would have really long addresses, which would be kind of annoying.

SPEAKER_00: Exactly, you would need a standard for conveying that information which would be variable length inevitably if you go for big scripts. So I think P2SH was... I don't even think that all of these advantages were talked about at a time when P2SH was created. I think it was just the last one, like we have no address for this, it's really hard to create one. We can make it simpler by hashing the script first and I think the other advantages were things that were only realized later how much of a better design this is. So I think of course we've since iterated on that segwit. I think it's clearly something that should have been done from the beginning. The fact that signatures leak into the TXID made it really hard for all kinds of more complex constructions. But at the same time Bitcoin was the first thing in its class and it's hard to it's unrealistic to expect it gets everything right from the beginning and thankfully I think we've learned very well how to do safe upgrades to some of this.

SPEAKER_01: Yeah, I agree entirely that, like, this isn't really an exercise in, in faulting Satoshi for the mistakes. But I, if I could wave a magic wand, I think Segwit from, from the Genesis block would be, would be great, because then the block, the block could commit to the signatures, the WTX ID. Whereas now it doesn't.

SPEAKER_00: So in Segwit it does, so in Segwit there's a Coinbase output that contains a hash with the root of a Merkle tree that commits to all WTX IDs.

SPEAKER_01: Yes. But you don't know that until you deserialize the transactions from the block. Right. Which is a little bit annoying.

SPEAKER_02: How do you sort of think about how to spend your time on Bitcoin and there's so many ways to get nerd sniped and so many directions you could contribute to. So what are you excited about and then how do you sort of feel like the pull of your personal excitement versus the pull of what's necessary for someone like you to contribute to?

SPEAKER_00: That is a good question. I don't have a good answer. I try to work on things that I am excited about. But sometimes this also means following through on something after you've lost some of the excitement about it, because people now expect, you know, you've worked on this, that you continue. But it's a hard question. Like, I expect this in general in open source to be a problem where there is no set direction and ultimately people choose how to spend their own time themselves. What am I excited about? Well, I'm happy with the progress we've made with the Taproot review and how that is going. I'm excited to see that progress further. There's some interesting changes people are working on related to peer-to-peer protocol, things like Erlay, that I contributed to. There's too many things to mention. I think.

SPEAKER_01: temperature plus early is a good start of things to get excited about all right shall we shall we wrap up there sure thank you for your take

SPEAKER_00: Thank you. That was fun. You're welcome.

SPEAKER_02: So that was our first episode, John, what do you think?

SPEAKER_01: That's great. I mean, it's always a pleasure talking to Peter. He's been around for nine years. He's seen a lot. Eleven years, according to you. Well, off by one or two. And he's always got lots of great insights into Bitcoin. So it's great talking to you.

SPEAKER_02: Yeah, I think when we were talking about starting this podcast, this was our number one guest that we wanted. And so I think we can wrap it up.

SPEAKER_01: Great. All right. Let's talk to some more people.

SPEAKER_02: Okay, we can do that too.

