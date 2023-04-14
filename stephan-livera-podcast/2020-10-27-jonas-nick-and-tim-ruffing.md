---
title: What’s MuSig2? What Does it Mean for Bitcoin Multisig?
transcript_by: Stephan Livera
categories: ['podcast']
speakers: ['Jonas Nick and Tim Ruffing']
tags: ['taproot']
date: 2020-10-27
media: https://stephanlivera.com/download-episode/2581/222.mp3
---
podcast: https://stephanlivera.com/episode/222/

Stephan Livera:

Jonas and Tim, welcome to the show.

Jonas Nick:

Hello.

Tim Ruffing:

Hey.

Stephan Livera:

So thanks guys for joining me today. I was very interested to chat a little bit about some of your recent work with MuSig2, but firstly, let’s hear a little bit about each of you. So Jonas, do you want to just start by telling us a little bit about yourself and how you got into doing cryptography?

Jonas Nick:

So I’m working at the research group at Blockstream. I work on libsecp the library of Bitcoin core, and I work on a few of these cryptography things, but mostly just because I want to implement them in the way that the misuse resistance, or developers can use it without the possibility of making huge mistakes. And yeah. What else do I do at Blockstream? I’ve been working on liquid a little bit and researching scriptless scripts and yeah, these are mostly my responsibilities.

Stephan Livera:

Great. And Tim, let’s hear a little bit from you.

Tim Ruffing:

My name is Tim Ruffing. I’m in Germany, like Jonas is I got into cryptography in the, I don’t know, let’s say the traditional academic way. So I did my PhD on cryptography in particular cryptography in Bitcoin and at Saarland University. The title of my dissertation really was cryptography for Bitcoin and friends. So this is really on the spot. So during that time I mostly worked on privacy in Bitcoin and now that I’m in the research team at Blockstream I work a lot on signatures in particular. Yeah. All the stuff you’re hopefully going to talk about today, like MuSig multisignature, threshold signatures, basically everything that’s related to Schnorr signatures.

Stephan Livera:

Fantastic. So the context for today, we’ve got this, this coming soft fork that everyone, basically everyone wants into Bitcoin, the Schnorr or colloquially, the Taproot soft fork. So perhaps you could set the context a little bit. What’s the relation between Schnorr, Taproot and then MuSig. And multisignature so perhaps Jonas, if you want to just set the context for us.

Jonas Nick:

Yeah. So taproot is basically this new witness program version that we will have hopefully after the activation. So instead of having like a segwit version zero output, you will have a SegWit version one output. And what this means is that now you have different ways of this coin, and one of these ways is to provide a Schnorr signature. So this is how it will BIP Schnorr relates to BIP taproot. And this is kind of an upgrade to how this works right now with ECDSA signatures, especially because Schnorr signatures are a little bit simpler and allow, m few more applications on top of that. And, MuSig is the idea of, making multi signatures, compact in Bitcoin. So right now in Bitcoin, you have this, check multisig opcode, but calling this a multisignature is perhaps a little bit of a stretch because it’s not really compact because what you’re doing with this, you just write down all the public keys and all the signatures, and then you verify them one by one. But what you really want is that, this is all efficient, which means that you have a single signature and a single public key, but your policy is still a multi signature. And this is kind of the idea behind MuSig for a Schnorr signatures.

Stephan Livera:

I see. So maybe just to spell that out for listeners who might not be as familiar. So current day multisignature relies on using, as you’re saying this Bitcoin scripting. And as part of that, let’s say we’re doing a two of three multisignature output. Then we have to actually show both what two signatures, and what we’re talking about here is in the taproot world, we’ll be moving to, and I presume you’re referring to there, like that’s like their taproot key path spend where we can construct a multisignature let’s say between the three of us and on the chain, it only looks, you can only see one signature, correct?

Jonas Nick:

Yes. Although I think it would make sense to already start here differentiating between multi signatures and threshold signatures. So with MuSig, you can do multi signatures, meaning M of M or N of N, you need as many signatures as you have public keys. So in this would be something that can be done with MuSig. And with taproot, you can still use the old way of doing threshold signatures, where you just write down in the chain, the signatures and the public keys.

Stephan Livera:

I see. Yeah. And so that’s the difference between let’s say doing in that example, doing two of three, versus having it such that you must do three of them?

Tim Ruffing:

Yeah. I think that’s kind of an important difference in the terminology. Because when you talk to a Bitcoiner and say multisig they usually think about this M of N can really be smaller than M as you mentioned, for example, two of three. And if you look at academic literature, what they call a multisignature is really restricted to this N of N case where you need the full number of signers. The other thing is called as Jonas mentioned, is called thresholds signatures. And we also working on this, but MuSig so far only supports this n of n case where the numbers are equal.

Stephan Livera:

Okay. And so that’s essentially the diverse, the difference there between threshold signatures and then multisignature when we’re talking in the academic context, right. So perhaps you could just outline a little bit around this journey because there are different forms of MuSig, right? So there’s MuSig1, MuSig-DN and MuSig2. So perhaps you could spell out for us, what are the differences there between those different types?

Jonas Nick:

Tim, you’re the expert on history of MuSig.

Tim Ruffing:

History of MuSig. Yeah. yeah, let’s actually go even a step back more and yeah. See what was there before MuSig, because there’s really an interesting story to tell there. Before we had MuSig, so one of the main reasons to get Schnorr signatures into Bitcoin is really that, you can build a lot of things easier, which no signatures than with ECDS, for example, multisignature threshold signatures, and other advanced types of signatures scriptless scripts, things like that. So all of these are somewhat nicer with original signatures because the math around Schnorr signatures is easier. And so some years ago, I can’t even tell when this was people, like Andrew Poelstra, Peter Wuille, Greg Maxwell thought about doing MultiSignatures, with Schnorr.

Tim Ruffing:

And they came up with the scheme and at their main challenge was to avoid some some attack that’s called rogue key attack or others call it key cancellation attack where let’s say we are, like we do a three of three among us here. And I published my public key and Stephan maybe publishes his key. And then Jonas is the attacker and looks at our keys and chooses his key depending on our keys and by doing so, what he can achieve is that if like, if we would do this in a naive way, then the resulting key the MultiSignature key that would, that should represent all of us would actually only represent him. So Jonas could sign alone with this key, which is totally not the goal of MultiSignatures of course, because we all should be able to –

Stephan Livera:

Ha, scary.

Tim Ruffing:

Yeah. And this is basically really just cancellation. You can think of just adding up, like if we add up the keys and Jonas’s chose the key in a, in a pretty way, then our keys just substrate out again, they’re gone. Right. So he could sign alone. Yeah. And of course it’s not what we want. So those people thought they have a solution to to this problem and which actually fights this problem. And then the sense, yes. What they came up with was really a solution for that problem, but it had other, it had another issue too. And this issue is a Wagner’s attack. Maybe we will come to that later. I don’t want to go into the details of this now, because I guess then the story will be even longer. But yeah, so they try to publish, try to write this up at the paper and publish it. And then people pointed them to existing work in the literature that basically didn’t solve this problem, but solve the other problem about Wagner’s attack.

Tim Ruffing:

And so the story there kind of continued and then they got together with the coauthor of also for us, like Yannick Seurin from France is a brilliant cryptographer I’d say. And he was happy to have them write up a proof or scheme. That’s basically the combination of the two worlds that solve both problems. And this was, let’s say the old version of MuSig1. And when I say old version, I mean like an insecure version, because even they screwed it up again, in this other work, they were appointed to, this was a paper by Bellare and Neven from 2006 and it’s so for MultiSignature, so you need an interactive, signing procedures, all the signers need to talk to each other, they each other way to signature and the process, and this paper had three rounds. So they needed to send three messages to each other and Yannick had the idea for improving that two rounds. Unfortunately this idea was flawed. So we had to revert back to three rounds, and this is basically then MuSig one, which is three rounds multisignature and avoid the cancellation attack.

Stephan Livera:

So can we just unpack the idea of interactivity? So as I understand MultiSignature. Today, at least in Bitcoin or threshold signatures, I guess if we want to be more technically precise, it is non-interactive right. Like the three of us can just put in an xPub each and create this MultiSignature and off you go, but what’s the interactivity part mean in the MuSig context?

Jonas Nick:

Yeah. So I think there’s still a little bit of interactivity because your signing device needs to get the message, the transaction to sign, and then it replies with a signature. So you could say that’s kind of like a one round signature scheme. And with this MuSig secure version of MuSig1 we have three communication rounds, and this has two problems. One, it’s just the communication rounds. They, they just add up you have a protocol that uses this, for example, in lightning, we figured out that if you would use MuSig instead of regular signatures, then you would have to add half of a round trip, that would be a problem because this half round trip adds up on every hop. And we know that lightning are connected for a Tor sometimes. So this could really add some, some latency. And another problem would be if you have a setup with multiple signing devices, and one of them you have in a safety deposit box, and either you basically take all your devices, bring them to the same location and do this whole signing ritual, or we have to go two times to your safety deposit box. And this would also be a problem, I suppose. So this is really the problem with interactivity.

Stephan Livera:

Putting that into the example, as you were saying, you might have, let’s say a three different hardware wallet, devices, and one coordinating laptop or machine with like a Bitcoin Core or a Specter or something. And in that example, you would have to then go to each hardware wallet, location, get the signature, come back, go to the hardware wallet two, come back and like do a few rounds of that. And that obviously is not very practical. Could you also just outline for us the difference in terms of usetup of the, you know, creating that multisignature quorum, versus signing a transaction for that quorum? Is there a difference there, or does it still kind of three rounds, whatever you’re doing?

Tim Ruffing:

I think if you talk about set up like for really, for MuSig again, restricted to the case, that’s N of N multi signatures. One big advantage of MuSig in general is that the setup itself is, is still not non-interactive in the sense that you can take any public keys and combine them into an aggregate public key, and everybody can do this. So you can just like if I know the Pub keys of you two guys, I could now immediately send 2 of 2 of you without even talking to you again.

Stephan Livera:

I see, gotcha.

Tim Ruffing:

There is a difference when we move to threshold signatures, if we in the future want to accept MuSig to support, M of M, threshold signature say, then this would be an inherently different.

Tim Ruffing:

I think there we really need an interactive setup because when it comes to threshold signatures, the tricks that usually play to make that work is that you create a secret key. Everybody creates a secret key and then shares parts of that secret key with the other people. And this sharing process needs to happen before we can use the signature scheme. So this is kind of inherently interactive and in a funny sense, I’d say what we call naive thing that works on Bitcoin today with scripts still better in that respect, but because it’s always non-interactive.

Stephan Livera:

Right. From a practicality perspective. So in terms of that process, you mentioned if we were to try that, is that the nonce commitment part? Maybe you want to explain what that part is for us.

Jonas Nick:

Yeah. So perhaps just to elaborate on another problem with MuSig1, which is that you need to keep state securely, and this is kind of an abstract problem. If you’re not an engineer, but many people would be perhaps familiar, but it’s not really possible to back up lightning channels. And this is a similar problem. If you start a signing session, you back up the state, because you write it on a disc and then you back it up to your NAS or whatever you finish the signing session, then you restore the backup and then you sign again with the same session. Then you have re-used your nonce, and you’re not supposed to reuse your nonce with a different signature and someone can easily compute your, your secret key. This is the other problem with MuSig1 So, that makes it difficult also too. One of our goals is to write libraries, right, and implementations. And our implementation of MuSig1, we have this huge documentation. So not supposed to copy this state or write it somewhere. Keep it on memory and you have to pay attention to this and that’s norm for these things. And this makes it really dangerous.

Stephan Livera:

What was the approach going forward from that was, it seemed like, Oh, well, we’re just going to have to mitigate this and have all the application developers just be really mindful of it before they use MuSig1. Or was it more like, okay, now we need to find other approaches?

Jonas Nick:

Basically yes, because there was also this paper called on the security of two round multi signatures, and they showed that you cannot prove two round MuSig1 secure. There’s no way to do it in any model that we care care about. So we kind of didn’t try then, but then,

Tim Ruffing:

Right. I mean, it’s broken it’s of course they also showed that you can’t prove it’s secure, but it’s also because it’s just insecure. So again, we are talking about the old version of MuSig 1 though. That’s what is referring to with two round MuSig1.

Jonas Nick:

But they didn’t prove that you cannot prove another scheme is secure. And so, yeah. Then we basically started also looking into these other schemes, like MuSig-DN and MuSig2.

Tim Ruffing:

Right. I think this is where it really started with MuSig-DN then.

Stephan Livera:

Yeah. So let’s get into MuSig-DN. What is that?

Tim Ruffing:

MuSig-DN the DN spells out Deterministic Nonce, which is a very technical term, I think. But it really relates to what was Jonas saying with about you can’t reuse states, so you have to use store your or the state between the rounds of your signing procedure in a, in a secure way, in particular like you can’t you make sure you have to make sure that it can’t be rolled back. For example, if you run your wallet in a virtual machine, for whatever reason, then you can reset the machine would be, so it’d be really bad. And very related problem to this is that of choosing nonces in a secure manner. And what’s a nonce, a nonce is a number used once. And these nonces are required when you create signatures.

Tim Ruffing:

Like we know them, not only Schnorr signatures also ECDS a signatures, and they have very specific requirements about being random. So they need to be, yeah, it sounds weird, but like, like very random, you can’t have a small bias in this nonce. So the worst thing that can happen is like, what you just mentioned is if you reuse your nonce, like say you have a random number generator that’s supposed to generate these random nonces. And for some reason it would output the same nonce twice, which is astronomically unlikely. But if it’s broken, maybe it’s a test this flow that it would output the same number twice. And then if you use the same nonce to sign different messages, then people can just look at the resulting two signatures and compute your secret key. So it’s catastrophic, it’s totally game over. But as I said, it’s even, like this is just the worst case that can happen.

Tim Ruffing:

So even if there’s a slight bias and choosing that nonce there are ways to extract the secret keys from your signatures. So that’s why in, in normal single party signatures, if ECDSA or Schnorr signatures or ed25519 all the elliptic curve, signature schemes, we know if there’s really common engineering practice to generate Nonces deterministically. And this is maybe sounds weird, right? Because this deterministic, is kind of the opposite to random so how can this work? While it can work, if you in deriving those nonces deterministically, you kind of use your secret key as a secret ingredient, and then still no one can predict what the outcome is. So you can generate these nonces in a secure manner, without relying on an external source of randomness that could fail, and still generate your, signature securely.

Stephan Livera:

So when we’re saying deterministic here, it’s kind of like it’s like that concept of when you hash the same, like word, it’ll always hash out to the same, like so long as you do it through the same algorithm, it’ll still hash out to the same outcome. Right?

Tim Ruffing:

Right, right. And it’s, it’s basically almost what we do or it’s actually what you do. So you would take your secret key. Would take the message that you want to sign. You put those into a secure hash function. And what you get out is the result of the hash function is something that only you can know, because only, you know, the secret key and you set as your nonce. This is a simple procedure. And the problem with it. So as I said, like, everybody’s doing this in signatures because it’s the right way. The problem is now, if you move to multisignature world where you have this interactive signing a process, suddenly it’s the other way around now, suddenly if you use deterministic nonces your security breaks down immediately. This is a very weird thing. And yeah, so we now even, like, if you look at BIP 340 which specifies, Schnorr signature, we actually put a warning in there to make that explicit after people got it wrong and took our MuSig scheme and implemented it in a deterministic way, because they thought, okay, look like this is the. We have always been told to the use deterministic nonces. So of course we kind of do this year and I can’t blame them for this because it’s all natural.

Stephan Livera:

So then how did MuSig-DN come up and like what kind of context makes sense to use MuSig-DN?

Jonas Nick:

The interesting thing, there is if only one signer derives their nonce deterministically, then that’s insecure, but if everyone would derive their nonce deterministically, then it would be secure. And it turns out that you can build a zero knowledge proof showing to the other signers that you yourself have deterministically derived your nonce. So what you are doing compared to the normal MuSig scheme is just, you will see nonces and proofs, and you verify them and you generate your own loans deterministically, and then there’s a secure the big question there is how to, or the big part of the paper is one. It was this still insecure signature scheme, and two, how can we really make this efficient?

Stephan Livera:

And that was this Adam Back’s idea?

Jonas Nick:

I don’t know, actually, I would say it’s probably folklore that came up in an IRC or something.

Tim Ruffing:

I heard it’s your idea, but I can’t, I don’t know, but maybe it’s folkfore, yeah.

Jonas Nick:

I’m just, yeah, I think it wasn’t really all that great. It’s difficult to make it efficient.

Stephan Livera:

So tell us a little bit about that process. So zero knowledge proofs as I understand they are, they tend to be computationally efficient or the size of the transactions and things like that are bigger. So tell us a little bit about that in terms of MuSig-DN.

Jonas Nick:

So perhaps if we start with the end result that you can see that it’s not too limiting, so on a desktop machine, it takes about one second to create a proof for a single signature and a few milliseconds, I think on the order of 50 to verify such a proof. So that’s not really a limitation. And the size of a proof is about a thousand bytes. If I remember correctly.

Stephan Livera:

So not an issue for a desktop computer, but perhaps an issue if we were to talk about, would it be an issue if we were to talk about hardware wallet, devices, like Trezor and Coldcard and things like that?

Jonas Nick:

Having things hardware wallet devices, they have very different specs, right? And they’re do different things on different processors. So it’s not really easy to serve that would really workable. And in a Bitcoin transaction, you can have multiple signatures, not only one. But I think what this shows is that the limitation really isn’t the computational complexity but rather the code complexity that this zero knowledge proof entails. So if someone were to use that in practice, we have proof of concept code, but you really need to audit the code very, very closely. And see if there are any flaws.

Stephan Livera:

I see.

Tim Ruffing:

Yeah. So let me just stress that because people tend to forget about this of course, MuSig-DN removes one possibility to shoot yourself in the foot, which is like, it removes this random, this reliance on the random number generator on the other hand. It’s much more complex than what we did in MuSig1. For example, in terms of engineering, complexity. So building the secure zero knowledge proof, and implementing it correctly is pretty complicated. Of course you can get it right. But yeah, it’s yeah. Software has bugs, right? So I don’t have a measure on the lines of codes of the zero-knowledge proof as compared to the rest of the signing. But I think the difference is large. Maybe I don’t know, 10x this is just a guess, but of course, like if you have 10x lines of code, it’s much easier to make a mistake there. So I think we really need to work on the careful implementation of MuSig-DN before it’s really ready to be used in practice. And we can trust it.

Stephan Livera:

Out of curiosity. What kind of business, or what kind of use case would that make sense for? Like, are we talking like maybe a Bitcoin exchange wants to have like warm wallet and they would use MuSig-DN to distribute that? Or like, what kind of example uses would you see for MuSig-DN?

Jonas Nick:

So I think, again, that’s really hard to say because we need to se how, if it’s really a problem to self or to maintain state or not. So we at Blockstream we’re not currently focusing on developing these techniques and showing that our MuSig-DN implementation is actually without any bugs. So we are more focusing on MuSig2. Right now,

Tim Ruffing:

Maybe one thing we could add here, maybe we, you can see this as a intermediate step, because there’s now you mentioned, I think, cold storage for exchange for example, is in a sense, a good one because they really need the highest level of security I’d say, and you’re maybe willing to accept, hven you run this additionally on a, on a hardware wallet. I mean, maybe this then takes 10 seconds. Maybe it takes a minute. I dunno, it depends on the, on the hardware wallet, them, I’m just making up these, these numbers. But even if it takes a minute, of course, like this is usually not something that you expect from cryptography on your, on your desktop machine. But moving from cold storage to warm storage, if this takes a minute, think you don’t really care.

Tim Ruffing:

This is all acceptable. I think that the big limitation here is that again, this is only for N of N and I don’t think that if you are a huge exchange, you want to keep your cold storage in M of N because if you lose one of those devices or whatever it is, your keys will be gone, right? So you probably want M of N where maybe this is, I don’t know, two or three or seven of 10 or something like this. And think until we build a version of music, the end that works with special signatures, they’re not currently working on this. Maybe we can see this as an, more like an intermediate step. At least if you think about those scenarios that you mentioned, where we really need the highest level of security,

Jonas Nick:

just to give an example for lightning, it’s not a problem to keep state because it can keep the state in memory. And if your program aborts or crashes, then you just do a completely new signing session and the same holds for federated sidechains and also Blockstream green.

Stephan Livera:

So shall we chat about MuSig2 then? So what was the impetus behind this?

Jonas Nick:

So the impetus, I think was just realizing that there is some kind of trick where you could actually do two round MuSig, and it’s a very simple trick, unlike MuSig- DN there’s no heavy machinery, the complexity is very similar to, MuSig and,then we just started trying to prove this secure, because we didn’t want to make any claims again, that would have found some two round scheme that was secure.

Tim Ruffing:

By the way, maybe you should mention that MuSig-DN also has only two rounds, but it’s rather like a neat side effect of it, right? Because you need this expensive zero knowledge proof. It doesn’t matter. Like if you have one run more or less. Yeah. But, okay. This was only one additional about MuSig-DN.

Jonas Nick:

Yeah. And then we’re teamed up again with Yannick Seurin and wrote two different proofs and two different models to show that this can actually be used and it’s even simpler in code complexity than MuSig1. And you could even say it’s noninteractive because it’s very first round. You can view it as some kind of a pre-processing step, which can happen before the message is known. So you can imagine that if you have, want to set up your quorum, you have some pairing step where you already exchange first round you store it, the state. Okay. But then later when you have a transaction to sign, it’s the same as right now, no additional rounds or rubbing back and forth to your safety deposit box.

Stephan Livera:

In the paper here, you talk about MuSig2 being secure under concurrent signing as opposed to previously requiring sequential signing. So what’s the difference there?

Tim Ruffing:

I think there, this really relates to for the hinted at earlier with Wagner’s attack. So the reason, or the reason why MuSig1 has three rounds and two rounds, the insecure two round version of it was insecure is really only a concurrent sessions, which means that you have a device which has a secret key, and which is involved in multiple signing sessions at the same time. Which can of course happen if this is your desktop machine and you’re creating transactions with multiple people at the same time. Then only in this case this two round version becomes, insecure and attacks like Wagner’s attack apply by basically the attack roughly works by creating a lot of signing sessions with you. Let’s say, like, I don’t know, 50 signing sessions and then driving a lot of hash nonces, but we’re just then possible.

Tim Ruffing:

And then they can extract 51 signatures from you, but they should only be able to extract 50, right. Because you run 50 signing sessions. Now this is, again, something that maybe it’s not, you could even say, maybe that’s not so relevant in practice, but we want schemes that are as Jonas as mentioned in the very beginning. How did you say robust to misuse? Right. So if we, as a protocol designer can build signature schemes that just don’t have this flaw then nobody can get it wrong in practice. And this is again, like having multiple sessions as again, something that could easily happen, say, you copy your key to a second device. Maybe this is something you shouldn’t do, but some people will do. And then those two devices could have concurrent sessions, right.

Tim Ruffing:

And they can’t, they don’t even know each other. So this is very hard to to make sure that you really run only one session at a time and this may be a problem. If you, if you go to scenarios where let’s say, let’s say lightning, where you have a lightning nodes and you want to use MuSig with a counterparty, and maybe there are like two things are going on at the, at the same time. And then you would be plopped and others could run maybe like denial of service attacks on you, but just starting a signing session and never, never finished it. And then you would wait for it to be finished because otherwise you can’t move on to the second session and so on. So we really want the scheme that’s usable with as many concurrent sessions as you, as you wish. And this is where MuSig2 comes in.

Stephan Livera:

Can you tell us a little bit more about music too, and how it would look like, and what’s involved with it?

Tim Ruffing:

I think if you, if you look at if you look at applications where we want this, where we really envision this to be used is protocols like like lightning, where currently you in the lightning channel between two parties, they run a multisignature currently, they use they do this using the naive thing with a Bitcoin script. And this is really a scenario where we want music to be used because it’s now kind of efficient because you don’t need this additional round trips because it’s only two rounds. And you can, pre-process the first round in the sense that you, when you set up the channel, you can also already do the pre-processing and then if you want to send some money over the channel only then you get like the message you want to sign. And then it’s just basically one additional message on network to create the signature.

Tim Ruffing:

And yeah, I think if you want to differentiate this to to MuSig-DN, then it’s really simple and lightweight. So this is something you can write into a specification for lightning, for example. Whereas probably, I mean, in theory, you could use something like MuSig-DN in lightning, but you probably wouldn’t want to have this in the spec because MuSig-DN only works. If everybody is using this deterministic nonce as we explained earlier, so you would enforce, or you would put the burden of having the expensive zero knowledge proofs on everybody. And it’s probably not something you can agree on. But MuSig2 is simple enough that you can, or I hope that people can agree on using this or very end of this in lightning and then other higher level protocols maybe just discreet log contracts or other things you can build with Schnorr signatures.

Stephan Livera:

Okay, cool. One other thing that stuck out to me, I was curious to get your thoughts and perhaps you could help explain this for us. What is the one more discrete logarithm assumption? And what’s the implication of that for the security of MuSig2?

Jonas Nick:

Tim that’s a question for you.

Tim Ruffing:

Sure. You can answer that one as well. Yeah, no, I can explain it, of course. Uso all of our modern,uat least the public key crypto. For example, when you talk about signatures, as a public key primitive in cryptography because it has public keys. It’s built on assumptions on cryptographic hardness assumptions. So these are problems, that we hope that are hard to hard to how to do on the computer. And that’s why they, that’s how they get their security from. And yeah, it’s kind of weird when I say hope, right? Because we it’s really just a hope, but our confidence, these assumptions is usually really, really good because people spend like 30 years trying to break them and trying to come up with efficient algorithms and failed to do so.

Tim Ruffing:

And this is how we obtain our signature sorry, our security, for example for Schnorr signatures, by assuming of the hardness of a specific computational problem. And this is for Schnorr signatures, this is the discrete logarithm problem. So it’s a problem related to elliptic curves, where you get a group element and you have to compute the discrete logarithm of it. And people tried this for many years and failed to come up with efficient algorithms for that. So we believe this is hard. That’s, by the way, one advantage of Schnorr signatures over ECDSA because at least for Schnorr signatures, we know,uor we can prove them secure. If the discrete logarithm problem is hard for ECDSA that’s really a hard story. I mean, you also hope that ECDSA is hard to break, but we don’t have nice mathematical proofs for this.

Tim Ruffing:

This is one like a theoretical advantage of Schnorr signatures here and now with MuSig2. We need to make a stronger assumption for MuSig1, we were able to prove to secure if this discrete logarithm assumption holds. So, which basically means it’s nice because as compared to Schnorr signatures, which anyway, we need to be secure because otherwise MuSig is secure because it uses Schnorr signatures. We don’t need additional, you don’t need to introduce additional assumptions for MuSig2 to get this, more efficient. We need to have an additional assumption that’s called one more discrete logarithm assumption. And if you think about it, the normal discrete logarithm assumption is I give you a one elliptic curve point and you need to compute the discrete logarithm. And we hope this is hard.

Jonas Nick:

Just to give an example, your group element would be your public key, for example. And the secret key is the discrete logarithm.

Tim Ruffing:

That’s a very, very nice example I should have brought up. Yeah. So it should, of course, be hard to compute secret keys from public keys, right? Because otherwise all the security is gone, of course. And this is exactly an example for discrete logarithm, and so in normal discrete logarithm, basically, this means I give you one public key and you have to come up with the secret key. Hopefully this is hard and one more discrete logarithm, and this is a little bit generalized. The game is different. The game is give you, let’s say, 10 public keys. And now you can ask me for nine secret keys in the sense, and still you shouldn’t be able to figure out the 10th secret key. The interesting thing about this that you can’t only ask for exact secret keys are things that I gave you public keys for, but you can also combine them.

Tim Ruffing:

You can add them up. For example, I can send you yeah. 10 public keys, let’s say public key one to public key 10. And then you could ask me for secret key one. You could ask me for the secret key of public key 1 plus public key 2. And then you can play tricks like this, but you can only ask nine questions, but in the end, after you, ask nine questions, you can compute,the secret keys of all of these 10 things I’ve sent to you, and then you solve the problem. And, we still believe this is hard because people have used this in the, in the past, but it’s not exactly equivalent to the normal Discrete Logarithm assumptions. So we have to make a stronger assumption there in the sense, but as I say, this assumption has been used in the past. So we are pretty confident that it holds, it’s not an issue in practice.

Stephan Livera:

Just to walk through an example there. Well, actually one other point I wanted to ask. So you mentioned earlier that your aim is that this would be used inside of lightning as an example. Would it also make sense to have this as part of, you know, just general hardware, wallets and multisignature security to use MuSig2 as part of that, or in your view, is it not really well designed for that purpose?

Jonas Nick:

I think this is really up to the designers of hardware wallets. And if people figure out how to do this they really have a competitive advantage because using MuSig versus this naive technique of using Bitcoin script is more efficient. It saves fees and it’s more private. So I think there’s an incentive to get this working. And as I understand, quite a few of the hardware wallets already are stateful and depend on state to be secure. So it wouldn’t be such an additional burden to also use MuSig2,

Stephan Livera:

Yeah. So I guess just as a quick example, I know some of the hardware wallet manufacturers are looking at these things like registering the other participants inside your quorum, right? So that’s like for a security reason. So maybe that is kind of a similar, like, to that point you were saying about having to maintain additional state. So I’m curious then if you know, whether they would need additional specs in terms of the current day hardware wallets, would they need additional specs in terms of processing power or memory or things like that?

Jonas Nick:

No, because these signatures that are very similar to just normal Schnorr signatures. So if you can do a normal signature in a reasonable amount of time, you will probably also be able to do it’s a little bit more complicated, but that shouldn’t matter much.

Tim Ruffing:

It’s really similar. I think that’s really the selling point of MuSig2. That ‘s as simple as almost as simple as a normal signature also in terms of computing power and memory and all the resources you need.

Jonas Nick:

Yeah. And this is also why we’re calling it MuSig2, because it really supersedes MuSig1. There’s no reason to use MuSig1.

Stephan Livera:

Also, just to clarify with MuSig2, is this a threshold signature scheme, or is this a, you know, like it has to be M a what’s an M of M like three of three, for example?

Jonas Nick:

It is an M of M scheme. So you can only use it for having the same amount of signers as public keys. But as people might know in taproot, for example, you have the keyspend condition, which means that in a taproot output, there is this public key, and you can spend directly from it, or you could reveal some parts of a Merkle tree. And let’s say, if you want to instantiate a two of three policy, what music, what you can do is you can just create three 2 of 2 MuSig public keys, and put them into limbs of this tree and that where’s cheaper than using two of three with Bitcoin script. But it also doesn’t reveal that this is 2 of 2 policy because there’s a, it looks like a public key hidden in this tree.

Stephan Livera:

So if I understood you correctly, this is that difference between say a keypath spend and then a script path spend in the taproot world, right?

Jonas Nick:

Yeah, so you could, if you have two or three quorum, there’s perhaps, one or two signers, which are more likely to produce signatures and you would aggregate their public key, put it into the taproot key because that’s the most likely spending. And then the other two of twos you will put into this a tree. So if you would spend where these two, then you would have to reveal that there is this tree that you wouldn’t reveal that this is a two of two, you would only show, okay, there’s a public key and you’re going to spend it.

Stephan Livera:

I see. Yeah. So maybe let me just put that into a practical example then. So let’s say listeners want to do, let’s say Michael Flaxman’s guide two of three, right. Have one Coldcard, one Cobo and one seed picker, which is like a paper know or metal seed, you know, the 24 words. And if they know that they’re know, that most of the time we’re going to be signing with the ColdCard and the vault, then they would put that into the key path spend. And the other kind of spending pathways would just be captured inside the script or the tree aspects of it. So that’s how they could still do use MuSig2 in this like hypothetical, like if Coldcard and Cobo supported the whole, you know, et cetera. But I’m just, I guess that’s an example of what’s possible, right?

Jonas Nick:

Yeah, exactly, exactly. This is a simple way to create a threshold policies with MuSig2, in a taproot world. But of course this doesn’t scale very well. If you try to have a 60 or 100, for example, then your tree will get very, very big.

Stephan Livera:

Yep, yep.

Tim Ruffing:

Yeah. I guess we really need to work on a special version of this and we are actually aware that this is what a lot of people will need, just that things that time. But I guess there’s a, like there are a lot of things going on. Other also another research groups for example, there’s a paper called FROST or scheme called FROST by Chelsea Komlo and Ian Goldberg and they they come up, came up with a very similar idea. Like we did were for, for music too, but their scheme works in a threshold in the real threshold setting. We have some criticisms about their security proof because I think the, we believe ours is more precise. But really think they are going to in, into the, into the right direction. It doesn’t also, doesn’t have all the features that we want for MuSig, this kind of key aggregation step, where you take some public keys and combine them into an aggregate key. They don’t have this in the same way as, MuSig does. But I hope that in the future we can combine all these approaches and can, can come up with the MuSig2 threshold scheme. But for now that’s, yeah, I’m talking about future stuff that of course can take time to –

Stephan Livera:

The important part is that it’s possible, right?

Tim Ruffing:

Right. So we believe it’s possible. Also if you ask me now I could also write up the procedure for doing it. It’s just that we need to be very careful and to our work and try to prove this secure, to be really confident about it.

Stephan Livera:

I see. Yeah. And so are there any other key changes in terms of what it would look like in terms of setting up the quorum, the initializing of that multisignature setup, or maybe any other changes in terms of signing a transaction? Or do you think it’s kind of, all said and done, it’s going to look very similar to current day. Multisignature wants the hardware wallets. Like once the spec is made, once the hardware wallets are made, once the software is updated for it?

Jonas Nick:

I would say so, but I don’t say it with confidence because really, or we’ve learned in the past one, two years that they are really subtle a text on these hardware wallets. It’s really difficult to rule out at this point that there will be some additional measures that hardware wallets would need to take to use MuSig2.

Stephan Livera:

I see. And in terms of Bitcoin wallet software required to do taproot multisig or taproot MuSig2. Are there any key changes that you can think of there that are required versus say the typical ECDSA multisig available today?

Jonas Nick:

I don’t think so. I mean, it’s relatively straightforward. I think to integrate this as long as you’re able to store this session state, or even better don’t store it, just keep it in memory and renegotiate or repair, as soon as you start up again,

Stephan Livera:

In terms of changes to Bitcoin script required would there be any key changes there or would it be kind of that aspect we were talking about before with the key path and the script path spend aspects of it versus the current day, ECDSA just showing exactly the spending condition in the script.

Tim Ruffing:

I think this is kind of one of the nice features of this interactive way of doing a multisignature sort of threshold signatures. Is that really what, what comes out of the signing process is a normal signature. And what comes out of the key aggregation process is a normal Schnorr public key. So this just looks like a normal signature on chain. You can’t even. So as soon as they have support for Schnorr signatures on the chain, you wouldn’t even need a strictly speaking. You wouldn’t even need taproot to do this. You just need the ability to verify Schnorr signatures on the chain. You can use all those interactive schemes, like MuSig, MuSig2 and MuSig-DN to create your signatures. And then that’s pretty cool because yeah, what ends up on chain is just the public key and a signature. And this is not only nice for efficiency because those are very small, but also for privacy, because in most cases, people observing the chain can’t even tell that you use sophisticated multi signatures in the background. That just looks like a normal spend.

Stephan Livera:

Right so that means in practice, people could be doing music too, for multisignature or threshold doing a kind of threshold multisignature scheme to, you know, to HODL their coins, right, with more security or they could be opening lightning channels to each other. And in terms of on chain analytics or surveillance, they would look similar, correct.

Jonas Nick:

Or they could do a normal payment, which looks exactly the same as well, because like, just to answer the question in the taproot world your spend is either just a signature. So there is no op code because you provide a signature for the public key and the taproot output, or it’s just a check, stick op code. So the same as a normal payment.

Stephan Livera:

Yeah. That’d be some very cool implications there in terms of perhaps giving everyone a little bit more privacy. Also Jonas, I know you were working on some of the stuff around, or you were talking about some of this stuff scriptless scripts and point time-locking and lightning implications of this work. So could you outline a bit of that for us as well?

Jonas Nick:

Yes. I think we touched a little bit onto that as well. So that’s the idea that with with Schnorr signatures, you can also do it with ECDSA, but it’s more complicated, but with Schnorr signatures, you could do lightning payments were scriptless scripts. Perhaps people are familiar with that. Right now, in order to make a lightning payment you have these hash timelock contracts, so you need to provide a hash pre-image. And one of the problems to claim the payment and one of the problems is that this hash pre-image has to be the same on every hop of the route of the payments route. And this allows nodes on this route to correlate the payment and see where the payment is coming from and where it’s going. And one of the advantages with scriptless scripts lightning is that you wouldn’t have hash pre images anymore.

Jonas Nick:

You will use those typically public keys and secret keys, and you will be able to randomize this payment pre-image which isn’t a hash pre image any more, but it’s a secret key now, and you would be able to randomize it on every meaning that even two nodes on the route collude and see or talk about which payments are are coming through. They wouldn’t be able to correlate it aside from timing maybe because now this payment pre-image is randomized on every hop. This is one of the advantages of scriptless script lightning. And the other one is, or one of the other ones is that you get a proper proof of payment right now, if you pay someone, you get a payment pre-image, but every hop on the route gets this pre-image. So this doesn’t really work, as a proof of payment and scriptless scripts lightning solves that. But in order to use scriptless scripts lightning with Schnorr, you need some kind of MuSig, preferably MuSig2.

Stephan Livera:

Excellent and listeners who are interested, you can check out my earlier episode with Rusty Russell, we spoke about MPP and he was talking about the proof of payment and that episode. And also if you’re interested in, some other, the lightning spec discussion, also check out episode 200 with Christian Decker, where we go into some of that also. So Jonas and Tim, are there any other pieces of feedback that you’ve received from other cryptographers or other people in security on your work with MuSig2, and MuSig-DN?

Tim Ruffing:

One interesting thing about MuSig2, is that, m already mentioned that, at least one other team came up with least a very, let’s say the same core idea to make this two rounds, make it secure with two rounds under concurrent sessions. And there was even a third team on inaudible upper and Jeffrey Burgess that came up with the same, idea the independently. And this is kind of neat because, um, gives us some additional confidence, right? If like three research teams have the same idea, but it’s a fun coincidence that they have it at the same time. But I think this is because there’s a lot of interests in building this multisignature schemes right now. If three research teams or six people come up with the same idea this gives us some more confidence that it’s actually the right thing that we’re doing here, and it’s really secure. This is one part, Jonas can you something about MuSig-DN?

Jonas Nick:

Sorry, just to add to MuSig2. It’s really cool to see that other people are working on these problems as well, because in the past we also had problems just to motivate these problems because often cryptographers think that these are boring problems that have already been solved. And why don’t you use more complicated cryptographic assumptions and so on, because they don’t really understand this very specific setting of Bitcoin where we want to rely on only the discrete logarithm assumption and we cannot easily make consensus changes, et cetera. And this is cool to see with MuSig2, that other people are interested as well. And this was also a little bit of problem for MuSig-DN to motivate this because everyone’s exactly the response we got was yeah, it’s, doesn’t seem to be very interesting. It just seems to be more theoretical, whereas we think is a very practical, not very practical because you have all the disadvantages of the zero knowledge proof, but let’s because we need this, we need it in a practical setting and MuSig-DN makes some applications more practical.

Stephan Livera:

I guess maybe a skin in the game question. So imagine, you know, a few years down the line, would you guys be comfortable, you know, keeping your own Bitcoin stash on a MuSig2 scheme?

Jonas Nick:

Yes.

Tim Ruffing:

Certainly.

Stephan Livera:

Well, that’s great. Great to hear that there’s some confidence there

Tim Ruffing:

I’d prefer maybe a threshold set up, but as far as like, I’m very confident in MuSig2. Yeah, of course. Now I have some incentive to work on a threshold extension where to keep my own coins.

Stephan Livera:

Right. And I guess until a threshold scheme is done, then I guess people would just have to be really more careful about keeping the backup 24 word seed, for example. So maybe they would have like three of five and make sure that they’ve got all the 24 word backup you know, on this thing so they can create it so they can recover that key, that hardware wallet key, and still sign in, even in a five of five or a three of three scenario. Right?

Jonas Nick:

Yeah this works. But of course this has disadvantage, as far as I know that you need to put all your your backups into one location again, to restore. Right. So I think it would be better to create a threshold policies using the taproot.

Stephan Livera:

I see. Yeah. Yeah. That makes a lot of sense.

Tim Ruffing:

Depends on the scenario, right? Like if you store your Bitcoins yeah. That’s maybe where like threshold things, like maybe if you do it in a taproot three or using other methods will be better for now in some scenarios, you really need this n of n, and our prime example again, here is lightning. And then inaudible this is where we very see MuSig2 at the moment where they have just 2 of 2 channels, and this is what you need. This is exactly what you need.

Stephan Livera:

Yeah. Right. I guess, where do we go from here with MuSig2 what kinds of development would you like to see or contributions would you like to see? Or what do you see that’s necessary before we get further adoption of MuSig2?

Jonas Nick:

Yeah. So one thing that I really want to do is just to update our implementation from MuSig1 to MuSig2. And I hope that we’ll be mostly deleting code because you just delete now unnecessary states or this, I’m looking forward to actually do that.

Stephan Livera:

And Tim anything from your side?

Tim Ruffing:

Yeah. I think in terms of implementation we have this you have this repository libsecp or secp256, inaudible which Jonas was referring to where we have currently an implementation of MuSig1. And, me will of course update this to, MuSig2 And I hope that others will implement our scheme as well, or, or use our use our library because it’s really simple in the sense that it’s not hard to implement. Of course, like maybe I shouldn’t say this right. Crypto is always hard to implement, but if you’re already implement Schnorr signatures, then it’s not much to be added on, on top of it. And this is really a difference to MuSig-DN which is hugely complicated, zero knowledge proof, which, have scares me a little bit off from an implementation point of view. I think that MuSig2, because it’s so simple. We’ll see, more implementations than our own library. And hope that people can, now that it’s out, heah, play it, play around with it and see if it fits their higher level protocols, like lightning, DLCs, Scriptless scripts and all the magic stuff you can build on multisignatures.

Jonas Nick:

Yeah. And I suppose previously the interest wasn’t really high because no one knew whether a taproot would be a thing in the future. And now that’s, it seems like this becomes a reality at some point. And on the theoretical side, I think one interesting feeling that we want to do with MuSig2, is a realizing a concept that we call nesting, which means that you can have a tree of MuSig keys. So let’s say you have Alison Bob and Alice and Bob can aggregate their key and their aggregated key can be used again, with another participants called Charlie. And then they can aggregate this aggregate tree together to have basically a fruit of three, but child doesn’t learn that there’s an Alison Bob. He just sees their aggregated key, a single key and a, this has some applications to channel factories and perhaps makes some multi-sig setups, more private because now we have signers that don’t need to know about all of the other signers. They only need to know about one aggregated key. And you don’t know whether this is an aggregated key or this is a single signer.

Stephan Livera:

Interesting. So that could make use, make sense in a some kind of inheritance scenarios where maybe like a lawyer has a key or things like that. Right?

Tim Ruffing:

Maybe. Yeah. So one simple example. I’m not sure if it’s a good example you want in practice, but just to explain what’s going on there, think of again of a lightning channel two on two, sorry two of two. So you have a lightning channel with some other peer on the lightning network, but you internally want to use a multisignatures for enhance security. So your part of the lightning channel is, again, the MuSig maybe between your desktop machine and your hardware wallet, and like the other party and the lightning channel wouldn’t even know, or wouldn’t even need to care that you internally run the MuSig. This is maybe an example to illustrate what’s going on here.

Stephan Livera:

Yeah. Interesting one. Okay. So I think those are the key points. Was there anything else that I missed or anything else you thought you wanted to just discuss related to MuSig2 guys?

Jonas Nick:

Yeah. If people went to help us implement this Tim already mentioned libsecp is where we’re working on or libsecp. So see you there.

Tim Ruffing:

Right. And feel free to reach out to us and bother us with questions or ideas or anything.

Stephan Livera:

Great. So where can people find you online

Jonas Nick:

@n1ckler on Twitter.

Tim Ruffing:

Right. It’s through there is nice there will pick up.

Stephan Livera:

Excellent. Well, thanks very much guys for joining me. Thank you. Thanks.
