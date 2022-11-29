---
title: MuSig2
transcript_by: Michael Folkson
categories: ['meetup']
tags: ['schnorr', 'multisig']
speakers: ['Tim Ruffing']
date: 2022-08-11
media: https://www.youtube.com/watch?v=TpyK_ayKlj0
---

Topic: MuSig2

Location: London Bitcoin Devs

Date: August 11th 2022

Reading list: <https://gist.github.com/michaelfolkson/5bfffa71a93426b57d518b09ebd0998c>

# Introduction

Michael Folkson (MF): This is a Socratic Seminar, we are going to be discussing MuSig2 and we’ll move onto adjacent topics such as FROST and libsecp256k1 later. We have a few people on the call including Tim (Ruffing). If you want to do short intros, you don’t have to, for the people on the call. 

Tim Ruffing (TR): Hi. Thanks for having me. I am Tim Ruffing, my work is at Blockstream. I am an author of the MuSig2 paper, I guess that’s why I’m here. In general I work on cryptography for Bitcoin and cryptocurrencies and in a more broad sense applied crypto. I am also a maintainer of the libsecp256k1 library which is a Bitcoin Core cryptographic library for elliptic curve operations.

Elizabeth Crites (EC): My name is Elizabeth Crites, I am a postdoc at the University of Edinburgh. I work on very similar research to Tim. I also work on the FROST threshold signature scheme which I’m sure we’ll talk about at some point during this. 

Nigel Sharp (NS): I’m Nigel Sharp, bit of a newbie software engineer, Bitcoiner, just listening in on the call in case I have any questions.

Grant (G): Hi, I’m Grant. Excited about MuSig. I may have a couple of questions later on but I think I’ll mostly just observe for the moment.

# A retrospective look at BIP340

MF: This is a BitDevs, there are a lot of BitDevs all over the world in various cities. There is a list [here](https://bitdevs.org/cities). This is going to be a bit different in that we’re going to focus on one particular topic and libsecp256k1. Also we are going to assume a base level of knowledge from a [Socratic](https://btctranscripts.com/london-bitcoin-devs/2020-06-16-socratic-seminar-bip-schnorr/) and [presentation](https://btctranscripts.com/london-bitcoin-devs/2020-06-17-tim-ruffing-schnorr-multisig/) Tim did a couple of years ago. This isn’t going to be an intro. If you are looking for an intro this won’t be for you. But anyone is free to listen in and participate and ask questions. The Socratic we did with Tim, this is before [BIP340](https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki) was finalized, this was before Taproot was activated, this was before Schnorr signatures were online and active on the Bitcoin blockchain. First question, BIP340 related, has anything in BIP340 been a disappointment or problematic or caused any challenges with any future work? It is always very difficult to finalize and put something in stone, put it in the consensus rules forever especially when you don’t know what is coming down the pipeline in terms of other projects and other protocols, other designs. The only thing I’ve seen, you can tell me if there is anything else, is the x-only pubkeys for the TLUV opcode. The choice of x-only pubkeys in BIP340, that has had a complication for a covenant opcode in its current design. That’s the only thing I’ve heard from BIP340 that has posed any kind of disappointment.

TR: I think that is the main point here. BIP340 is the Schnorr signature BIP for Bitcoin. One special thing about the way we use Schnorr signatures in Bitcoin is that we have x-only public keys. What this means, if you look at an elliptic curve point, there is a x and a y coordinate, there are two coordinates. If you have a x coordinate you can almost compute the y coordinate up to the sign basically. For each valid x coordinate there are two valid y coordinates. That means if you want to represent that point or store it or make a public key out of it you need the x coordinate and you need 1 bit of the y coordinate. What we actually did in the BIP here, in our design, we dropped that additional bit. The reason is that it is often encoded in a full byte and maybe you can’t even get around this. This saves 1 byte in the end, brings down our public keys from 33 bytes to 32 bytes. This sounds good, it is just 1 byte or 1 bit but I think it is a good idea to squeeze out every saving we can because space is very sparse. This was the idea. There’s a nice [blog post](https://medium.com/blockstream/reducing-bitcoin-transaction-sizes-with-x-only-pubkeys-f86476af05d7) by Jonas (Nick). This blog post explains that this is actually not a loss of security. Even though we drop a bit in the public key it doesn’t mean that the scheme becomes a bit less secure, it is actually the same security. That is explained in this blog post. Though it turns out that if you just want to do Schnorr signatures on Bitcoin with normal transactions then it is pretty cool, it saves space. If you want to do more complex things, for example MuSig or more complex crypto then this bit is always a little pain in the ass. We can always get around this but whenever we do advanced stuff like tweaking keys, a lot of schemes involve tweaking keys, even Taproot itself involves tweaking, MuSig2 has key aggregation and so on. You always have to implicitly remember that bit because it is not explicitly there. You have to implicitly remember it sometimes. This makes specifications annoying. I don’t think it is a problem for security but for engineering it is certainly annoying. In hindsight it is not clear if we would make that decision again. I still think it is good because we save a byte but you can also say the increased engineering complexity is not worth it. At this point I can understand both points of view. You mentioned one [thing](https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-July/020663.html) on the bitcoin-dev mailing list. There was a [suggestion](https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-September/019419.html) by AJ (Towns) for a new Bitcoin opcode that would allow a lot of advanced constructions, for example coinpools. You have a shared UTXO between a lot of people, the fact that we don’t have the sign of the elliptic curve point of the public key would have created a problem there. You need the sign when you want to do arithmetic. If you want to add a point to another point, `A+B`, then if `B` is actually `-B` then it doesn’t work out. You are not adding, you are subtracting, this is the basic problem there. There were some ugly workarounds proposed. I recently came up with a [better workaround](https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-July/020663.html). It is still ugly but not as ugly as the other ones. It is just an annoying thing. If we could always deal with this x only key and still save space but sometimes they are annoying. The only hope is that we can hide all the annoying things in BIPs and specifications and libraries so that actual protocol developers don’t need to care too much about this.

MF: I think coinpool was using this particular covenant opcode but it is a complication for the covenant opcode TAPLEAF_UPDATE_VERIFY. Then various things might use it if that was ever activated on the Bitcoin blockchain. That’s the only thing that has come to light regarding BIP340.

TR: Mostly. The other thing, it is not really a pain but we are working on a tiny change. At the moment the message size is restricted to 32 bytes so you can sign only messages that are exactly 32 bytes. This isn’t a problem in Bitcoin because we pre-hash messages and then they are 32 bytes. But it turned out that some people would like to see this restriction lifted. We are working on a small update that allows you to sign messages of arbitrary size. This is really just a tiny detail. The algorithm works but we specified it to accept only 32 bytes. We need to drop this check and then everything is fine basically.

MF: That’s BIP340. I thought we’d cover that because before it wasn’t active onchain and now it is. Hopefully that will be the only thing that comes to light regarding BIP340 frustrations.

# MuSig2 history

MF: Let’s go onto MuSig2. I have a bunch of links, a couple of talks from [Tim Ruffing](https://btctranscripts.com/realworldcrypto/2021/2021-01-12-tim-ruffing-musig2/) and [Jonas Nick](https://btctranscripts.com/iacr/2021-08-16-jonas-nick-musig2/). I thought I’d start with a basic history. The first paper I found was [this](https://cseweb.ucsd.edu/~mihir/papers/multisignatures.pdf) from Bellare, Neven (2006). They tried to do multisig, I guess key aggregation multisig. I don’t know what the motivation is for this. Before Bitcoin and before blockchains what were people using multisig for? What use cases were there where there were so many signatures flying around? Not only that but also wanting to have multiple people signing? And then on top of that wanting to aggregate it to get the privacy or space benefit? Is it just a case of academics pursuing their interests and not really worrying about the use case? Or is there a use case out there where people wanted this?

TR: You could have a look at the paper, if they have a use case.

MF: I don’t think there is much about use cases.

TR: No. I think blockchain and cryptocurrencies and Bitcoin changed cryptography a lot. A lot of things were brought from theory to practice. Cryptographers who were always busy with ideas and schemes but no one really deployed the advanced stuff. Of course you always had encryption, you had TLS, SSL, we had signatures and certificates also used in SSL, TLS. We had the basic stuff, encryption, secure channels, signatures. But almost everything beyond this simple stuff wasn’t really used anywhere in practice. It was proposed in papers and there were great ideas but cryptocurrencies have changed the entire field. Back then you wrote a paper and you hoped that maybe someone would use it in 10 years. Nowadays sometimes you write a paper, you upload it on ePrint, it is not even peer reviewed and people will implement it two days later. It is a bit of extreme. I’m not sure what Elizabeth thinks. That is my impression.

EC: Given that this paper was 2006, this is my perspective because I work on anonymous credentials, I think that was popular in 2001 to 2006, pre-Bitcoin era. I imagine that some of the motivation would have been distributing trust for certificate authorities. But I don’t know. I think they do say that in this particular paper as a motivation. As far as I know no one actually implemented this.

TR: Back then from a practitioner’s point of view, even if the goal is to distribute trust you could have a simpler construction of multisignatures with multiple public keys and multiple signatures. For CAs maybe that is good enough. This really becomes interesting when you have things like key aggregation and combined signatures that are as large as normal signatures. Space on the blockchain is so expensive, I think this is what makes it interesting to implement something like this. In the end all these modern multisignature schemes are interactive. Interaction is annoying, you have to send messages around and so on. I think if you don’t need to care about every byte on the blockchain maybe it is just not worth it.

MF: I suppose the challenge would be would they need privacy in that multisig setting or would they be motivated by the space savings. Why can’t it just be 5 signatures?

TR: This paper doesn’t have key aggregation?

EC: I think it does. I think this was the first paper that had key aggregation.

TR: I should know, let’s check.

MF: It has a section on rogue key attacks.

EC: They had the first idea to avoid the rogue key attacks.

TR: You can still have rogue key attacks even if you don’t have key aggregation.

EC: I think that was the thing, how to aggregate keys without rogue key attacks. 

TR: Let’s have a look at the syntax.

MF: If it is talking about rogue key attacks that is surely key aggregation, no?

EC: It doesn’t have to be.

TR: You could do it internally.

EC: You could just prove possession of your secret key and then multiply the keys together. But I think the interesting thing was that they were trying to not do that and have a key aggregation mechanism that still holds without being susceptible to that.

TR: Maybe go to Section 5.

EC: Also I think this was one of the first papers that abstracted the Forking Lemma from being a scheme specific type thing to a general…

TR: You see they just have a key generation algorithm, they don’t have a key aggregation algorithm. Of course during signing they kind of aggregate keys but you couldn’t use this for example for something like Taproot because from the API it doesn’t give you a way to get the combined key. They still can have rogue key attacks because in signing you still add up keys. You need to be careful to avoid this.

EC: How do they aggregate keys? I’m curious.

TR: They don’t because verification takes all the public keys as input.

EC: I thought that was one of the main motivations of this.

TR: MuSig1 was the first to solve that problem. It was there for BLS I guess already.

EC: I think this paper is a good reference for the transition for the Forking Lemma. There was a different Forking Lemma for every scheme you wanted to prove. I think this one abstracted away from something being specific for a signature scheme. Maybe I’m getting the papers confused. This is the one that referenced the change in the Forking Lemma.

TR: They say it is a general Forking Lemma but it is my impression that it is still not general. Almost every paper needs a new one.

EC: That’s true. It made it an abstract… lemma versus being for a signature scheme. You’re right, you end up needing a new one for every paper anyway. That’s the main contribution I see from this if I’m remembering this paper correctly.

MF: So we’ll move onto MuSig1. MuSig1 addressed the rogue key attack because that was well known. But MuSig1 had this problem where you had parallel signing sessions and you could get a forgery if you had a sufficient number of parallel signing sessions right?

TR: Yes and no. If you are going from Bellare Neven to..?

MF: Let’s go Bellare Neven, then insecure MuSig1 then secure MuSig1.

TR: The innovation then of MuSig1 compared to Bellare Neven was you had key aggregation. You have a public key algorithm where you can get all the keys and aggregate them. This didn’t exist in Bellare Neven. But yeah the first version of MuSig1, the first upload of ePrint [here](https://eprint.iacr.org/2018/068.pdf) had a flaw in the proof. This turned out to be [exploitable](https://medium.com/blockstream/insecure-shortcuts-in-musig-2ad0d38a97da). The scheme was insecure in the first version.

MF: This is committing to nonces to fix broken MuSig1 to get to secure MuSig1.

TR: They started with a 2 round scheme, this 2 round scheme wasn’t secure. The problem is that if you are the victim and you start many parallel sessions with a lot of signers, 300 sessions in parallel, then the other guy should get only 300 signatures but it turns out they can get 301 signatures. The last one on a message totally chosen by the attacker. This was the attack.

MF: Was there a particular number of signing sessions that you need to be able to have to get that forgery? Or was that a number plucked out of anywhere?

TR: You need a handful but the security goes down pretty quickly. There are two answers. With the first attack this covered, with Wagner’s algorithm, there it goes down pretty quickly. I never implemented it but around 100 I think it is doable in practice. If you have a powerful machine with a lot of computation power maybe much lower, I don’t know. Recently there was a new paper that improves this attack to super low computation. There you specifically need 256. If you have 256 sessions, or maybe 257 or something like this, then the attack is suddenly super simple. You could probably do it on your pocket calculator if you spend half a hour. 

# Different security models for security proofs

Jonas Nick on OMDL: <https://btctranscripts.com/iacr/2021-08-16-jonas-nick-musig2/#one-more-dl-omdl>

MF: One thing neither you nor Jonas in the presentations you’ve done so far, for good reason probably, you haven’t really discussed in depth the different security proofs. My understanding is there are four different security models for security proofs. There’s Random Oracle Model (ROM), Algebraic Group Model (AGM), One More Discrete Logarithm (OMDL) and then Algebraic One More Discrete Logarithm (AOMDL) that is weaker than the One More Discrete Logarithm (OMDL). Can you dig a little bit deeper into that? I was getting confused.

TR: I can try and Elizabeth can chime in if I am talking nonsense which I hope I don’t. Let me think about how to explain it best. First of all we need to differentiate between models and assumptions. They have some things in common but they are different beasts. In cryptography we usually need some problem where we assume that it is hard to solve, the most fundamental problem that we use here is the discrete logarithm. If the public key is `g^x` and you see the public key it is hard to compute `x` just from `g^x` but the other way round is easy. Other assumptions that we typically know, factoring, it is easy to multiply large numbers but it is hard to factor them. For MuSig we need a special form of this discrete logarithm. The discrete logarithm assumption is just what I said, it is an assumption that says it is hard given `g^x` to compute `x`. The reason why I call this an assumption is that it is really just an assumption. We don’t know, we can’t prove this, this is not covered by the proof. People have tried for decades to do this and they’ve failed so we believe it holds. This sounds a little bit worrisome but in practice it is not that much worrisome. All crypto is built on this and usually the assumptions don’t fail. Maybe there is a quantum computer soon that will compute discrete logarithms but let’s not talk about this now, that’s another story. For MuSig we need some special form of this discrete logarithm problem which is called One More Discrete Logarithm problem. It is a generalisation. The normal problem is given `g^x` compute `x`. Here it is “I give you something like 10 `g^x` with different `x`’s and I give you oracles, a magic way to compute 9 of these discrete logarithms but you have to solve all 10.” You always need to solve one more than I give you a magic way to solve it. This is One More Discrete Logarithm.

MF: There was an incorrect security proof for the broken MuSig1 that was based on One More Discrete Logarithm. That’s a normal model for a security proof. It is just that there was a problem with the scheme?

TR: Yeah. The security theorem would look like “If this OMDL problem is really hard to compute, I need to say if because we don’t know, it is just an assumption, then the scheme is secure.” The implication was wrong but not the OMDL problem. This is still fine. It is an assumption, we don’t know if it is hard, but this was not a problem. The algebraic OMDL, this is a tiny variant but it is not really worth talking about. Maybe when we come to the models. We need this OMDL assumption for MuSig2 also. And we also need the random oracle model, the random oracle model is basically a cheat. Cryptographers are only really bad at proving that particular things are hard, for example OMDL, we need to assume them. We are also pretty bad at arguing about hash functions. Modeling hash functions without special tricks is possible but it is very, very restricted and we can’t really prove a lot. That is why at some point people had the idea to cheat a little bit and assume that the hash function behaves like a random oracle. What is a random oracle? An oracle is basically a theoretical word for an API, a magic API. You can ask it something, you send it a query and you get a response back. When we say we model a hash function as a random oracle, that means when doing a security proof we assume that the hash function behaves like such an oracle where the reply is totally random. You send it some bit string `x` as input and you get a totally random response. Of course it is a function, if you send the same bit string `x` twice you get the same response back. But otherwise if you send a different one you get a totally new random response. If you think about practical hash functions, SHA256, there is kind of some truth in it. You put some string in there and you get the random looking response. But modeling this as an oracle is really an entirely different beast in a sense. It basically says an attacker can’t run this on their own. A normal hash function in the real world, they are algorithms, they have code, you can run them, you can inspect the code, you can inspect the computation while it is running, middle states and all that stuff. Whereas an oracle is some magic thing you send a message to and you get a magic reply back. You can’t really see what is going on in the middle for example. This is something where we restrict the attacker, where we force the attacker to call this oracle and this makes life in the proofs much easier. Now you can say “This is cheating” and in some sense it is but it has turned out in practice that it works pretty well. We haven’t seen a real world example where this causes trouble. That is why this methodology is accepted, at least for applied cryptography I would say.

G: I have a question about that. I noticed that in BIP340 and also in MuSig there has been talk about using variable length for the message as a parameter. Does that variable length play into this random oracle model assumption or is that completely separate?

TR: I think it is separate. If you have longer messages, you need to hash the messages at some point, they will go as an input to the hash function. Depending on how you model that hash function, that will be an algorithm or a magic random oracle. But I think the question of how long the message is is kind of orthogonal to how you model the hash function. To give you an idea how this helps in the proofs, it helps at several points. One easy example is that we can force the attacker to show us inputs. When we do a security proof what does it look like? The theorem is something like “If OMDL is difficult to compute and we model the hash function as a random oracle then MuSig2 is secure”. Roughly like this. How do we do this? We prove by contradiction. We assume there is a way to attack MuSig2, a concrete attacker algorithm that breaks MuSig2, and then we try to use that algorithm to break OMDL. If we assume OMDL is not breakable then this is a contradiction, the attack against MuSig2 in the first place can’t exist. This is proof by contradiction methodology that we call reductions. The random oracle model for example helps us to see how the attacker algorithm that we are given in this proof by contradiction uses the hash function. If we were just using SHA256 as an algorithm then this attacker algorithm can use this SHA256 internally and we can’t really see what is going on. If we don’t give it the SHA256 algorithm but we force the attacker to call this random oracle, to call this magic thing, then we see the calls. We see all the inputs that the attacker algorithm gives to the hash function. Then we can play around with them because we see them. We can make use of that knowledge that we get. But if you think about it model isn’t the right word, if there is some attacker somewhere in the world trying to attack MuSig2 it is not as friendly and doesn’t send us over all its inputs to the hash function. It just doesn’t happen. That is why this model is kind of cheating. As I said it turned out to be pretty successful. Elizabeth, maybe you want to add something? Whenever I try to explain these things I gloss over so many details.

EC: We use this notion of this idealized something, right. In the case of random oracle model we are saying a hash function should output something random. So we are going to pretend that it is a truly random function. What that means is that when we idealize a hash function in that way it says “If you are going to break MuSig you have to do something really clever with the explicit hash function that is instantiated”. Your proof of security says “The only way you are going to break this scheme is if you do something clever with the hash”. It kind of eliminates all other attack vectors and just creates that one. So far nobody has been able to do anything with the hash. It just eliminates every other weakness except for that which is the explicit instantiation that is used. That’s my two cents.

TR: That’s a good way to say it. When you think about a theorem, if OMDL holds this is one thing and if you model the hash function as a random oracle then the scheme is secure. This gives you a recipe to break MuSig2 in a sense. Either you try to break OMDL or you try to break the hash function. As long as those things hold up you can be sure that MuSig2 is secure. You also asked about AGM, the Algebraic Group Model. This is another idealized model. Here we are not talking about the hash function, we are talking about the group arithmetic. All this discrete logarithm stuff takes place in an algebraic group. This is now very confusing when I use this terminology. When I say “algebraic group” I just mean group in algebra terminology, a mathematical object. But when cryptographers say “algebraic” they mean something different. Here we restrict the attacker in some other way. We kind of say “The only way to compute in this group is to add elements”. If you have a public key `A` and a public key `B` the only thing you can do with this is compute `A+B` or maybe `A-B` or `A+2B` or something like this. You can’t come up with your own public key except drawing a new `x` and computing `g^x`. You can do this point addition, you can add public keys, and you can generate new public keys by drawing the exponent and raising `g` the generator to the exponent. But we assume that this is the only way you can come up with group elements. This is again very helpful in the proof. When I talked about the random oracle I said the attacker needs to show his inputs to the hash function. Here in the Algebraic Group Model the attacker needs to show us how it came up with group elements. For example what could happen is that we send the attacker the public key `g^x` and ask it to produce a signature on this public key that we haven’t created before. That would be a break of MuSig2. Now the attacker could say “Here is a signature” and the signature will contain a group element and then the attacker needs to tell us how it computed this element. This is an implication from what I said earlier. If you assume the only thing the attacker can do is add those things up then this is basically equivalent to forcing the attacker to tell us how it came up with these elements, give us the numbers basically. This again helps in the security proof. It mostly has theory implications only I would say as long as this model really holds up. It was a special thing with MuSig2 that we had two variants: the variant with the Algebraic Group Model where we need this stronger assumption is a little bit more efficient. 

MF: There isn’t neat strictly increasing levels of security right? It is just different paradigms? Because the Algebraic One More Discrete Logarithm (AOMDL) is weaker security than One More Discrete Logarithm. But how does One More Discrete Logarithm compare to AGM and ROM?

TR: Let me try to explain it the other way round. So far we have talked about assumptions and models. They are a little bit similar. The random oracle model (ROM) is in some sense an assumption. Whenever we add an assumption our proofs get weaker because we need to assume more. For the basic version of MuSig2, for the security, we need to assume that OMDL is hard and we need to assume the random oracle model (ROM). If we on top assume the Algebraic Group Model (AGM) then our security proof gets weaker. That means there is an additional thing that can break down. This Algebraic Group Model thing which is another cheating thing, if this doesn’t hold up in practice then the scheme might be insecure. On the other hand what we get out of the security proof is we now can have a more efficient way to do MuSig2. The Algebraic One More Discrete Logarithm (AOMDL) thing is really a slight variation of OMDL. This is very confusing even in the paper. Maybe this was your impression, if we add this algebraic assumption then this becomes weaker. We have a stronger assumption so our results become weaker. For the assumption it is kind of the other way round. I could explain it but I’m not sure if anyone will understand it if I try to explain it now.

MF: Ok, we’ll move on. We are not going to do a whole session on security proofs.

TR: If you are really interested, in the paper we explain it. But of course it is written with a specific audience in mind.

MF: I’ve just heard “This is weaker”, “This is stronger”, “We’ve got a stronger proof”, “We’ve got a weaker proof”. I was struggling to understand which one you are going from to another.

TR: It is hard because you say “weaker proof” and “stronger assumption” and even we get confused.

EC: The term “weaker” and “stronger” means different things in different contexts. A weaker assumption means better. A stronger assumption is worse. But then you have “stronger security”, it is a point of confusion in the terminology that we’re using.

TR: And it even confuses cryptographers. When you look at algebraic OMDL it is a weaker assumption than OMDL, slightly weaker which is slightly better. We have to assume less which gives us a stronger result. Even cryptographers are trained to believe whenever the hear the word “algebraic” it is something bad because now we have to make all these assumptions. In this specific case we are actually making a weaker assumption, that is why we stressed it so much in the paper. Whenever we say algebraic OMDL we have a relative clause that says it is actually weaker than OMDL to remind the reader that what we’re doing is actually a good thing and not a bad thing.

# MuSig-DN

Paper: <https://eprint.iacr.org/2020/1057.pdf>

Blog post: <https://medium.com/blockstream/musig-dn-schnorr-multisignatures-with-verifiably-deterministic-nonces-27424b5df9d6>

Comparing MuSig-DN with MuSig1 and MuSig2: <https://bitcoin.stackexchange.com/questions/98845/which-musig-scheme-is-optimal-classic-musig-or-this-new-musig-dn-scheme/>

MF: Ok let’s move on but thank you for those explanations. I’ll look at the papers again and hopefully I’ll understand it a bit better. So we were doing history. Let’s get back to the history. We went through broken MuSig1, we went through corrected non-broken MuSig1. Then there was MuSig-DN.

TR: DN was before MuSig2.

MF: Right, we haven’t got onto MuSig2 yet. MuSig-DN, it hasn’t been implemented, there is no one working on that. It was an advancement in terms of academic research but there’s no use case that you’ve seen so far why people would use MuSig-DN?

TR: Maybe there are some use cases but it is much more difficult. From the practical point of view what does it do? Multisignatures have some specific risks when using them in practice, at least all these schemes we’re talking about here. For example you need secure random numbers while signing. If you have broken random number generators, this has happened in the past, not in the context of multisignatures but in other contexts, then you might lose security entirely. You try to sign a message and the others can extract your entire secret key which is a catastrophic failure. MuSig-DN is an attempt to get rid of this requirement to have real randomness. This sounds good in practice because it removes one way things can go wrong but on the other hand the way we are doing this is we add a huge zero knowledge proof to the protocol. First of all we lose a lot of efficiency but even if you ignore this this comes with a lot of engineering complexity. All this engineering complexity could mean something is wrong there. In a sense we are removing one footgun and maybe adding another one. Adding that other one is a lot of work to implement. I think that is why it hasn’t really been used in practice so far. I still believe that there are niche use cases where it is useful. There has been at least one other paper that does a very similar thing to what MuSig-DN does but in a more efficient way. Their method is more efficient than ours but it is still very complex. It doesn’t use zero knowledge proofs, it is complex in a totally different way. But again a lot of engineering complexity. It seems there is no simple solution to get rid of this randomness requirement.

MF: So MuSig-DN is better for the randomness requirement and stateless signing. It is just that those benefits aren’t obvious in terms of why someone would really want those benefits for a particular use case.

TR: The randomness and the statelessness, they are very related if you look at the details. MuSig-DN has two rounds. When I say it is stateless it basically means that in one round I send a message, I receive a message from the others and then I send another message. That is why it is two rounds. When I say it has state the signer needs to remember secret state from the first round to the second round. This can be problematic because weird things could happen while you remember state. For example you could run in a VM, you do the second round and then someone resets the VM to the point where you did the first round but not the second round and you still have the state. You do another second round and you lost again. The basic idea is if we remove the requirement to have randomness then everything will be deterministic. That is why we don’t have to remember state. When we come to the second round we could just recompute the first round again as it is deterministic. We can redo the first round again so we don’t need to remember it because there is no randomness involved. That is why having no state and requiring no randomness are pretty related in the end. I think the motivation is we have seen random number generators fail in practice. Even in Bitcoin, people lost their coins due to this. It is a real problem but for multisignatures we currently don’t have a good way to avoid the randomness requirement. From an engineering point of view it could make more sense to focus on really getting the randomness right instead of trying to work around it. 

MF: Anything to add on MuSig-DN Elizabeth?

EC: No, I’d just say that I think there are some niche use cases for having a deterministic nonce, if it gets used in combination with something else. I personally have thought about a few things that might use it. I think it is actually a really nice result even with the expensive zero knowledge proofs. Maybe there is something that could be done there, I don’t know. I think it is not just pushing the problem to somewhere else, it is a different construction and I do think that determinism is useful when plugged into other schemes. I still think it is something worth pursuing and I like this result.

TR: We thought about using the core of it in other protocols and problems but we haven’t really found anything.

# MuSig2

MuSig2 paper: <https://eprint.iacr.org/2020/1261.pdf>

Blog post: <https://medium.com/blockstream/musig2-simple-two-round-schnorr-multisignatures-bf9582e99295>

MF: Ok so then MuSig2. This is getting back to 2 rounds. This is exchanging nonce commitments in advance to remove the third round of communication.

TR: Right, the fixed version of MuSig1 had 3 rounds. They needed to introduce this precommitment round before the other 2 rounds to fix the problem in the security proof, make the attack go away. It wasn’t just a problem with the proof, the scheme was insecure. Then MuSig2 found the right trick to remove that first round again. Whenever I say this I should mention that Chelsea Komlo and Ian Goldberg found the same trick for FROST. It is really the same idea just in a different setting. Even Alper and Burdges, they found the same trick in parallel. It was really interesting to see three teams independently work on the same problem.

MF: And this is strictly better than fixed MuSig1? MuSig-DN did still have some advantages. It is just that for most use cases we expect MuSig2 to be the best MuSig.

TR: Yeah. In this [blog post](https://medium.com/blockstream/musig2-simple-two-round-schnorr-multisignatures-bf9582e99295) we argue that MuSig2 is strictly better than MuSig1. It has the same safety requirements, it just gets rid of one round. You can precompute the first round without having a message which is another big advantage. A 2-of-2 Lightning channel may in the future use MuSig2, what you can do is do the first round already before you know what to sign. Then when a message arrives that you want to sign, a payment in Lightning that you want to forward or want to make, only then can you do the second round. Because you already did the first round the second round is just one more message. It is particularly useful for these 2-of-2 things. Then the transaction arrives at one endpoint of the Lightning channel, this endpoint can complete the second round of MuSig2 for that particular transaction, compute something locally, and then just send it over to the other endpoint. The other endpoint will do its part of the second round and at this point it already has the full signature. It is really just one message that goes over the network. That’s why you could call this semi-interactive or half-interactive. It is still interactive because you have two rounds but you can alway precompute this first round. Whenever you really want to sign a message then it is just one more message over the network. That’s why we believe MuSig2 is strictly better than MuSig1 in practice. But compared to MuSig-DN it is really hard to compare. MuSig-DN has this additional feature, it doesn’t need randomness. If you do the zero knowledge proof correctly and implement all of this correctly you definitely remove that footgun of needing randomness. This is a safety advantage in a sense. But on the other hand it is slower, it has more implementation complexity and you can’t do this precomputation trick so it is always two rounds. You can’t precompute the first round. These would be drawbacks. But as I said it has these safety improvements, you can’t say that one is strictly better than the other. But in practice what people want is MuSig2 because it is simpler and we like simple protocols. Not only because they are easier to implement but they are also easier to implement correctly. Crypto is hard to implement so whenever we have a simple protocol we have much less potential to screw it up.

MF: And on the security proofs you’ve proved the security of MuSig2 in the random oracle model. “We prove the security of MuSig2 in the random oracle model, and the security of a more efficient variant in the combination of the random oracle and the algebraic group model. Both our proofs rely on a weaker variant of the OMDL assumption”. Maybe I’ll never understand that. MuSig2, any other comments on MuSig2? 

# SpeedyMuSig and proofs of possession

Paper that references SpeedyMuSig: <https://eprint.iacr.org/2021/1375.pdf>

Comparing SpeedyMuSig with MuSig2: <https://bitcoin.stackexchange.com/questions/114244/how-does-speedymusig-compare-to-musig2>

MF: Let’s move onto SpeedyMuSig, that’s an additional MuSig protocol. This is your [paper](https://eprint.iacr.org/2021/1375.pdf) with Chelsea Komlo and Mary Maller. This has SpeedyMuSig in it and it is using proofs of possession which MuSig1, MuSig-DN or MuSig2 all don’t use. You argue in the paper that this potentially could be better in certain examples of use cases.

EC: Yeah, MuSig2 has this really nice key aggregation technique. What we do instead is we include proofs of possession of your keys. We talked a little bit before about how you want to avoid these rogue key attacks. One way is if you prove knowledge of your secret key then you can’t do that kind of attack. If you do that then the aggregate key for all the parties signing is just the multiplication of their individual keys. That makes for a more efficient scheme. I would say a use case where this might work really well is if you are reusing a key. It is a little bit more expensive to produce your key in the first place because you are computing this proof of possession. But if you are reusing keys a lot to sign then it is an alternative.

MF: Is this where Bitcoin has very specific requirements which make MuSig2 better than using proofs of possession, a SpeedyMuSig like scheme. In the MuSig2 [paper](https://eprint.iacr.org/2020/1261.pdf) it says proofs of possession “makes key management cumbersome, complicates implementations and is not compatible with existing and widely used key serialization formats”. This is Bitcoin specific stuff right? BIP32 keys and things like this? What is it that makes MuSig2 better than SpeedyMuSig in a Bitcoin context?

TR: I’m not sure it is really “better” and whether that is the right word. It is another trade-off. The proofs of possession are pieces of data that you need to add to the public keys. This means that when you want to aggregate a few public keys you need this additional piece of data. That’s data that we didn’t have so far in the public key and we wouldn’t have it on blockchains. For example if you do some crazy protocol where you take some random public keys or specific public keys from the chain without any additional context and you aggregate them then certainly MuSig2 is better because you wouldn’t have access to the proofs of possession. You would need to ask the other signers to send the proofs of possession before you can aggregate the key. On the other hand you can say “In practice we usually talk anyway to the people that we want to have multisigs with so they could send us their proofs of possession when we ask them. Both are true in a sense.

EC: I guess the idea is that the key is a little bit larger. If you are reusing the key constantly to produce these signatures then you only have to do it once and you can reuse it. It depends on the use case mostly.

TR: Yeah. SpeedyMuSig, the name already says it. It is a little bit more speedy, it is faster and MuSig2 is maybe a little bit more convenient depending on your use case. This is the trade-off. In the end I think it is not a big deal, you could use either for most applications.

MF: Maybe this is completely off-topic but I thought Bitcoin using BIP32 keys and having specific requirements, it would want to use MuSig2 over SpeedyMuSig. But that’s veering off course. BIP32 is a separate issue?

TR: Yes and no. BIP32, it maybe depends on which particular way of derivation you use here. For the others BIP32 is a way to derive multiple public keys, a lot of public keys, from single key material, a single secret key in a sense. There are two ways of using BIP32. There is public derivation and hardened derivation I think. In the hardened derivation, this is what people mostly do, there is just a signer with a secret key and this guy creates all the public keys and sends them to other people. In that model it doesn’t really make a lot of difference because the signer anyway has to generate a public key and send it to someone else. It could attach this piece of data, the proof of possession. If you do public derivation which is a little more advanced where you as a signer give a master public key to other people and they can derive more public keys that belong to you, that would be harder because they can’t derive the proofs of possession. Maybe they wouldn’t even need to, I never thought about this, maybe this would work. I should think about this.

EC: I think we should chat more about this.

TR: I think it would work.

EC: I should say that proof of possession in our case, it adds a couple of elements. It is a Schnorr signature.

TR: It is really just a Schnorr signature. It is confusing because we say “proof of possession” but it is again another Schnorr signature.

EC: It is another Schnorr signature because we love them so much. We are just adding one group element and one field element, a Schnorr signature to your public key.

MF: The Bitcoin specific things, you were describing the hierarchical deterministic key generation, a tree of keys that we have in Bitcoin, I don’t know if they use it on other blockchains, other cryptocurrencies. As you said this is generating lots of keys from a root key. We have a thing in Bitcoin where it is we don’t want to reuse public keys and addresses. We want to keep rotating them. So perhaps that Bitcoin requirement or expectation that you only use your public key once for a single transaction and then rotate to a new key generated from that tree impacts whether you’d want to use MuSig2 or SpeedyMuSig.

TR: It is hard to say. I think there is nothing specific about the way you use keys in Bitcoin that would mean you can only MuSig2 and not SpeedyMuSig, that you can’t use proofs of possession. It makes key management a little easier and also more backwards compatible for what we already have in our implementations. But it is not a fundamental thing, I think almost everything you could do with MuSig2 you could also do with SpeedyMuSig. Maybe you should ask Pieter about this because he has stronger opinions. I always argue proofs of possession are not that bad and Pieter says “Let’s avoid them”. It is not really a fundamental difference.

MF: I saw a [presentation](https://btctranscripts.com/mit-bitcoin-expo/mit-bitcoin-expo-2019/signature-scheme-security-properties/#qa) from Andrew Poelstra, apparently Ethereum has public key recovery from the signature. Someone (Bob McElrath) [asked](https://twitter.com/michaelfolkson/status/1558796319447285760?s=20&t=lcSoLWRVCWcn3ONFSBn2Eg) about this and Andrew said that’s not a good idea because of BIP32 keys in Bitcoin and that you need to commit to a public key. He was quite strong on not wanting to enable that. Apparently there is a covenant proposal that comes out of that if you can do public key recovery from the signature. Andrew was strong on saying that we shouldn’t enable that because of BIP32 keys which is kind of assuming BIP32 keys are fundamental to how we use Bitcoin in real life.

TR: I don’t know what he had in mind there. I don’t know this proposal but at the moment I can’t think of how BIP32 would interact with recovery.

MF: A question for Andrew then. Comments on YouTube, we’ve got one saying “Bellare Neven needed all keys for verifying”, maybe. 

TR: Right, we covered that.

Adam Gibson (AG): We have pubkey recovery in pre-Taproot already because we have it in ECDSA.

TR: We can’t do it in Schnorr, at least not with BIP340.

# MuSig2 draft BIP

MuSig2 draft BIP: <https://github.com/jonasnick/bips/blob/musig2/bip-musig2.mediawiki>

MF: MuSig2 now has a draft BIP. 

TR: I just updated it yesterday. Still a work in progress.

MF: Can you talk a bit about what work still needs to be done? Why is it still a work in progress? If it was changed to be SpeedyMuSig that would be a significant change. 

TR: That would be a significant change.

MF: What other things could potentially change in this BIP?

TR: Maybe go to the [issue list](https://github.com/jonasnick/bips/issues). If I look at this list we merged a few PRs yesterday. Most of the things in the actual algorithms are pretty stable. Almost all of what I see here is either already worked on or is improving the writing, the presentation but not the actual algorithms. One very interesting point here maybe is [Issue 32](https://github.com/jonasnick/bips/issues/32), the principle of just-in-time x-only. This is maybe something I forgot to mention when I talked about x-only keys. Here Lloyd (Fournier) argues that we should use x-only keys in a different way that reduces some of the pain that I mentioned earlier. I said x-only keys save 1 byte on the blockchain, in the public key, but they introduce a lot of pain in the algorithms. Lloyd here has a proposal, a different way to think about it, which reduces some pain. It is a really long discussion. At least we agreed on making certain specific changes to the BIP. We haven’t reached a conclusion on our fundamental philosophical views on how x-only keys should be thought about but at least we made progress. I promised to write a document (TODO) that explains how protocol designers and implementers should think about x-only keys. When they should use x-only keys and when they should use the keys that we used earlier.

MF: So the x-only thing is subtly complicating MuSig2 as well, I didn’t appreciate that. I thought it was just the TLUV proposal.

TR: It is what I mentioned earlier, it makes MuSig2 for example more complicated. On one side you can say it is not that bad because we can handle this complexity in the BIP and then we have a library where it is implemented, this handles all the complexity but still it is complexity. This discussion more turned into a discussion on how people should think about x-only keys. When we released BIP340 and now it is active with Taproot, some people got the impression that this is the new shiny key format that everybody should use. This is maybe the wrong way to think about it. It saves a byte but it saves this byte by losing a bit of information. It is a little less powerful. Maybe a better way to think about it, if you know that with a specific public key you really only want to do signatures, then it is ok to have it x-only. But if you may want to do other stuff with the public key, maybe add it to other keys, do MuSig2 key aggregation, do some other more advanced crypto, then it might be better to stick to the old format. “Old” is even the wrong word. We propose the word “plain” now. When I say “old” it comes with this flavor of old and legacy. It is actually not the case, it is just a different format. It really makes sense on the blockchain because there we save space. But for example if you send public keys over the network without needing to store them on the blockchain it might be better to use the plain format which is 33 bytes, 1 byte more. You can do more with these keys, they have 1 bit more information. They are more powerful in a sense. I can totally understand, if you read BIP340 you can understand that this is the new thing that everyone should migrate to. In particular also because 32 is just a number that implementers for some reason like more than 33. It is a power of 2, it doesn’t make a lot of difference but it looks nicer. Maybe that is the wrong way to think about it and that is why we had this issue and I volunteered to write a document, maybe a blog post, or maybe an informational BIP even, that explains how people should think about these keys and how they should be used in practice, at least according to my opinion. That’s another place where x-only keys made the world a little bit more complex. Now they exist there are two formats and people have to choose.

MF: So it is quite serious then. We’ll probably be cursing that x-only choice. As I was saying earlier it is just impossible to predict how the future goes. You have to converge on a proposal at some point, you can’t keep putting it off. Then no one will work on anything because they just think it will never get onchain.

TR: We had a lot of eyes on it. Of course in hindsight you could say if we had written the MuSig2 BIP and the code back then we would have maybe noticed that this introduces a lot of complexity. It is hard to say. At some point you need to decide and say “We are confident enough. A lot of clever people have looked at this and they agree that it is a good thing.” And it still may even be a good thing. It is not really clear. It saves space, maybe if people use it in the right way it will be good in the end.

MF: That’s the keys we are using, keygen. Are the other parts of the MuSig2 protocol kind of set in stone. Key aggregation, tweak, nonce generation. This is going to be solidified right?

TR: It is pretty much set in stone by now. If anybody here is really working on an implementation, when I say set in stone don’t count on it. It is still experimental and we could change things. This may lead to weird consequences if you use it now in production and then switch to a new version and so on. But if you ask me, yeah I think the algorithms are pretty much set in stone. Unless someone else finds a problem. One thing that is not set in stone when it comes to the real algorithms is one thing that was discussed in this x-only issue, where we want to change the key aggregation slightly. We should really hurry up now, it is there for a while now and we should try to get it finished.

MF: The BIP? Hurry up and finalize the BIP?

TR: Yeah because people really want to use it. In particular the Lightning people.

MF: In terms of the things that can go wrong in a MuSig protocol, you do need signatures from all parties so if one party is not responsive then you can’t produce a signature. You’d need a backout, an alternative script path.

TR: This is true in every multisig thing. If the other person doesn’t want to or is offline there is no chance.

MF: Either unresponsive or providing an invalid signature and it just can’t complete. In terms of sorting pubkeys, signatures, does that present a complication? If people are receiving pubkeys and signatures in different orders do you need a finalizer or combiner? Do you need to fallback onto that? Do you need to allocate a finalizer or combiner at the start?

TR: For key aggregation the way the BIP is written you can do both. The key aggregation algorithm in the BIP gets an ordered list as a data structure. You can parse an arbitrary list, which means you can sort the list of public keys before you parse it or you can choose to not sort it. We took this approach because it is the most flexible and different callers may have different requirements. For example if you use multisignatures with your hardware wallets at home you probably don’t want to have the complexity and just sort the keys. But maybe some applications already have a canonical order of keys, for example in Lightning. I’m not sure how they do it, I’m making this up, maybe there you have one party that initiates the channel and the other party which is the responder in the channel. Then you could say “Let’s put the initiator always at position 1 and the responder always at position 2”. I think we described this in the BIP in the text somewhere. If you don’t want to care about the order you are free to sort the public keys before you pass them to key generation. If you care about the order you can pass in whatever you want. If you pass two lists or two different versions of a list in a different ordering then the resulting key will be different because we don’t sort internally. For signatures it doesn’t matter in which order you get them. This is really handled in the protocol, that doesn’t matter. But if you are asking for things that can go wrong, I think the main thing that can go wrong is what we already talked about, the requirement to have good randomness. This is really the one thing where you need to be careful as an implementer. Of course you always need to be careful. You need some good source of randomness which is typically the random number generator in your operating system.

MF: And this is a new requirement because before with single signatures you are using the hash of various inputs to get the randomness. Now you do actually need an independent source of randomness.

TR: Yeah, right. That’s exactly the thing that MuSig-DN solves in a sense but by adding a lot of complexity. This is also a very, very important thing to know. People have tried to use this trick with the hash generating the nonce by hashing the secret key and the message for multisignatures. Don’t do this. If this was possible we would have added it to the BIP. But it is totally insecure. For years we told people when they implement signatures they should generate the nonce deterministically because this is way safer. This is true for ordinary single singer signatures. But funnily it is the exact opposite for multisignatures. This is really dangerous because we’ve seen people do this. We told them for years derive nonces deterministically and then they saw the multisignature proposal and said “Ok it is safer to derive nonces deterministically”. Now it is the other way round. It is strange but that is how it is. When you look at nonce generation here it has this note. “NonceGen must have access to a high quality random generator to draw an unbiased, uniformly random value rand”. We say it explicitly, you must not derive deterministically.

# MuSig2 support in Lightning and hardware signers

MF: Is this going to be the biggest challenge? Everything seems to take years these days but assuming we get hardware signer support for MuSig2, the hardware signer would need to provide this randomness that it currently wouldn’t.

TR: It is hard to say. You need randomness for doing crypto at all. You need randomness to generate your seed. In the hardware wallet case you could say “Let’s draw some physical dice”. For normal computers I think you assume you have some way to generate real randomness. We have cases where this broke down and we’ve seen cases in practice where this broke down and people lost their coins. This is one risk. Another risk is that you have this statefulness. If you do this… you precompute the first round in particular, which is what they want to do in a Lightning channel. Then you also have to make sure that you can’t really reuse that state twice. Whenever you have state you have some risk in practice that the state of your machine gets reset. For example if you run in a VM or you try to backup. Let’s say you do the first round of MuSig1, you have to keep the secret state in order to perform the second round, once you have a message. Now it would be a very bad idea to write that state to disk or even write it to a backup. What could happen is you complete the second round by sending out signatures and then at some point the user will restore the backup, you have the risk that you perform the second round again now with different inputs. This is exactly what we want to avoid, then you expose your secret key. That’s why we say in the BIP that you shouldn’t serialize the state. Even in our implementation we don’t give the user a way to serialize the state because this could mean some user will write it to some backup or store it somewhere else or whatever. If you really crash after the first round no big deal, just do the first round again. That’s totally fine. This is probably what Lightning will do. If a node crashes then they have to reestablish a connection to the other Lightning node and then they can run the first round of MuSig again.

MF: You can tell me to mind my own business but have you had any discussions with hardware wallet devs? You’ve got a hardware wallet at Blockstream. Any discussions with those guys? How long would it take? The BIP has to be finalized, you probably want a lot of experimentation before you make that investment.

TR: It is a good question. We should talk to hardware wallet people more. So far we mostly are in touch with Lightning people. I have the impression they really want to use it so they talk about it very often. I don’t know why because I don’t know the details of the Lightning protocol, I think in Lightning they said the statefulness is ok because if you lose state and you crash you need to trust the other side that they won’t steal your entire channel. They already have this assumption in their threat model so the additional state introduced by MuSig2 doesn’t change that really.

MF: I have a few links. I think it is specifically the Lightning Labs, LND devs, Laolu etc. I don’t know if they are already using it. [Loop](https://github.com/lightninglabs/loop/pull/497) is one of their products, maybe MuSig2 is already being used.

TR: Of course I hope my stuff is used in production but they need to be careful if we update the BIP and do some small changes. They have to be careful that it doesn’t break. At the moment we don’t care too much about backwards compatibility. It is not 0.1, it is not even a BIP, it is a BIP draft.

MF: It is merged but perhaps it is just an option, they aren’t actually using it in production.

AG: I know Laolu wrote an implementation of MuSig2 in the btcsuite golang backend but for sure it isn’t exactly final.

# FROST

FROST paper: <https://eprint.iacr.org/2020/852.pdf>

FROST PR in libsecp256k1-zkp: <https://github.com/ElementsProject/secp256k1-zkp/pull/138>

MF: So FROST. I have a quote from you Tim, a couple of years ago. I don’t know if you still have this view. “It should be possible to marry MuSig2 and FROST papers together and get a t-of-n with our provable guarantees and our key aggregation method”. Do you still share that view now? My understand of FROST is there’s a lot more complexity, there are a lot more design choices.

TR: I believe that is still true. Only a belief, I’m not sure what Elizabeth thinks. I think it is possible to create a scheme where you have a tree of key aggregations where some of those would be MuSig2, some of those would be FROST. Some of those would be multisig, some of those would be threshold aggregations. It is very hard to formalize and prove secure because then you get all the complexity from all the different schemes.

EC: I think it is worth pointing out that because FROST is a threshold signature scheme there’s a lot of added complexity with the key generation. When you have a multisig you have a nice, compact representation of the key representing the group. But as soon as you move to the threshold setting now you need some kind of distributed key generation which often has multiple rounds. There’s a trade-off there in terms of flexibility or having a nice key generation algorithm. These are different aspects.

TR: Maybe it is not related to that point of the discussion, I’m sure there is this [RFC proposal](https://datatracker.ietf.org/doc/html/draft-irtf-cfrg-frost-05) for FROST. I think this wasn’t included in the reading list.

MF: Sorry, what specifically?

TR: There is a draft RFC for FROST.

EC: FROST is being standardized through NIST. There’s a CFRG draft which has gone through several iterations.

TR: IRTF?

EC: Yeah. It would be helpful to pop those links into the list also.

MF: Ok I’ll definitely do that. So it is a threshold scheme but obviously with the k-of-n, the `k` can equal `n`. You can still do multisig with FROST. It is just a question of whether you would do that.

TR: I think you wouldn’t. If `k` equals `n` then you only get the disadvantages of FROST and not the advantages.

EC: Exactly.

MF: A couple of things I wanted to confirm with you guys. Jesse Posner who is writing the FROST implementation in [libsecp256k1-zkp](https://github.com/ElementsProject/secp256k1-zkp/pull/138), he said a couple of things, I wanted to confirm that this is true. I think he was a bit unsure when he said them. For FROST you can swap out public keys for other public keys without having an onchain transaction and you can also change from say a 2-of-3 to a 3-of-5 again without an onchain transaction? There is a lot of flexibility in terms of what you can do for moving the off-chain protocol around and making changes to it without needing an onchain transaction? This seems very flexible, certainly when you compare it to MuSig2. The only way you can change the multisig arrangement for MuSig2 would be to have an onchain transaction.

EC: I’m not sure if I understand that statement. If you are changing keys around at all then you need to rerun the distributed key generation protocol.

TR: I’m also not sure what Jesse is talking about here. I think in the pull request there were some discussions. What you certainly can do, you can downgrade n-of-n to k-of-n. This has been discussed. For example swapping out a key to a new key, maybe Elizabeth knows more, there are some key resharing schemes, I’m not really aware of those.

EC: Yeah. That’s what I was saying about doing the distributed key generation again. Say you run distributed key generation once and everybody has their secret shares of the overall group key. At least the DKG that is used in conjunction in FROST, the original one which is what we prove in our paper, it is based on Shamir’s Secret Sharing. There are some pretty standard ways to reshare using Shamir. That is possible. It is still non-trivial.

TR: You can do resharing but it is more like a forward security thing. You can’t reshare to an entirely new group of signers. You would still trust the old group of signers.

EC: You can transition from some group of signers to a new group of signers also. There are ways to reshare the keys. Or you can keep the same group and reshare a sharing of zero so your shares essentially stay the same, same group, or you can switch the group of signers. But it does involve performing the resharing. There’s a little bit that has to be done there.

MF: You would need to redo the protocol which surely means you’d need an onchain transaction in Bitcoin or blockchain lingo? It is not the case that you can have some funds stuck behind an address, a public key, and keep that public key associated with funds but rejig the protocol behind that public key.

EC: When you reshare you do have to send some values to the other parties so that everybody has their new shares.

TR: The old group will still have the signing keys. When you have a normal coin with a normal UTXO and single signer, of course what you can do is take your secret key and send it to another person, handover the keys. But this is not really secure because the other person needs to trust you, you still have the key. This would be the same in this FROST resharing. We can do the same transition from one group where you have a 2-of-3 sharing to totally different parties that again would have a 2-of-3. But they still would need to trust the old group not to spend the coins. In that sense it doesn’t give you a magic way to overcome this problem. Whenever you want to handover coins to a new person in a secure way you need to do a transaction.

EC: I think it is worth pointing out too that distributed key generation is dealt with as an entire field by itself, how to reshare things. When we say “FROST” it consists of these two components. There is the distributed key generation protocol and then the signing. What we tend to focus on is the signing because you could incorporate any number of distributed key generation protocols with the FROST signing mechanism. In terms of properties you want out of key resharing this is within the realm of distributed key generation research. Not really FROST research.

MF: And FROST also uses proof of possession, PedPop.

EC: Yeah. The original FROST paper proposed a distributed key generation mechanism which is basically the Pedersen DKG, this is a pretty standard DKG in the literature. With the addition of proofs of possession. That was why we proved our version of FROST together with the key generation protocol that they proposed. But it is basically just Pedersen plus proofs of possession.

TR: Maybe one thing to mention here, a step back and to reiterate, threshold schemes are in general more complex than multisignature schemes because not only the signing part is interactive but also the key generation part is interactive. In the MuSig paradigm you can just take some public keys and aggregate them. In threshold schemes, at least in those that work in the group we have in Bitcoin, the crypto in Bitcoin, even the key setup process is now interactive. This is of course again another layer of complexity. One interesting side effect here is that if we always during key generation need to talk to everybody, then we can certainly also send around proofs of possession. There is a requirement that we need to talk to everybody else during key generation. Then sending proofs of possession around is the natural thing to do. There is no drawback. We have the drawback already in a sense. That is why all these proposals use proof of possession and not MuSig key aggregation. This would probably be possible but you lose some efficiency.

MF: The Bitcoin implementation of FROST uses MuSig key aggregation.

TR: I think it does. Jesse said it is easier because then it is the same method, we could reuse some code. And it would be possible to do what he described there. Maybe you could start with a 3-of-3 setup and then downgrade it to a 2-of-3, something like this. Then it would make sense to start with the MuSig setup. When you start with the n-of-n thing you probably want to have the MuSig method. This was still an open point in this PR. He came up with this use case, I wasn’t really convinced that people want to do this in practice. Others maybe weren’t convinced either. I think we haven’t decided yet. At least in the Bitcoin world when you talk about this PR, it is much more work in progress than MuSig2. With MuSig2 we already have the BIP draft and it is almost finalized. Here we don’t even have a specification, we just have this draft PR which tries to implement it but without an explicit specification. It is worth mentioning that outside Bitcoin it is maybe the other way round. There is this IRTF proposal for FROST and there is nothing for multisignature. 

MF: So why is that? Given that MuSig is simpler. It is just that Elizabeth has done better speaking to the IRTF than the Bitcoin guys.

TR: I think there are a few things to say. First of all yes MuSig is simpler than FROST. Multisignature is simpler than threshold signature. Mostly because of the thing we just mentioned, key generation is non-interactive in multisignatures and interactive in threshold signatures. The second thing is use cases. In cryptocurrencies multisignatures have some use cases because in cryptocurrencies you always have an escape hatch when the other parties go offline. For example in a 2-of-2 Lightning channel you always need to have some timelock that says “If the other party disappears I can get the money back after some time”. If the other party disappears we can’t just create a new key because there’s money stored on that key and the money would be gone. In other applications, and the IRTF is probably not interested in cryptocurrencies, threshold signatures make a lot of sense. They also make sense in a lot of blockchain applications, as I said with blockchains we have these special cases where multisignatures make sense. But in general if you ignore cryptocurrencies for a moment then threshold makes more sense. You can scale it better. It is pretty useless to have a 10-of-10. What is the goal of all these schemes? To distribute trust. But with multisignatures you increase security but you decrease safety. Two things can happen, either some people get malicious or steal your keys, that is great with 10-of-10, 9 people can get compromised, their keys stolen, and the scheme is still secure. But on the other hand you always increase the probability that you lose the key material. If you have a 10-of-10 and you lose one of the 10 pieces the key is gone. You increase security against attacks but you decrease security against losing your keys. The only way out of this dilemma is threshold signatures where you don’t need to do 10-of-10 but you could do 7-of-10 or something like this. Then you can trade off this security against attackers versus security against losing stuff. This is something you can really only do with threshold keys. This is why in general people are more interested in threshold things. On top of this in Bitcoin I mentioned contracts, for example Lightning or other complicated things, we always have an escape hatch in these contracts. Even in other setups, for example at home when you store some larger amount of coins, maybe you want to have a 2-of-3 between 3 hardware wallets or 2 hardware wallets and your machine. This is a setup that I think a lot of people use. Even there you want threshold because if you lose one hardware wallet you don’t want to lose all your coins. But using Taproot there are some ways you could do this even with multisignatures. For example say you have 3 signers, 2 hardware wallets and a backup wallet somewhere else. You could have a Taproot output that is just a 2-of-2 of the two main signing wallets and you have some script paths that cover the other possibilities. You have two primary devices and as long as you have access to those you use this normal key spend. Whenever you need to resort to the backup device, then you need to open the Taproot commitment and show the script path, use the other MuSig combinations. You could implement this 2-of-3 [via 3 combinations of 2-of-2s](https://murchandamus.medium.com/2-of-3-multisig-inputs-using-pay-to-taproot-d5faf2312ba3). In the end this may be more convenient in practice than going through the hassle of running this interactive distributed key generation that you would need for FROST. I think this is another reason why multisignatures are interesting in Bitcoin. But of course this doesn’t scale. If you want to do 20-of-60 or 20-of-40, you probably don’t want to do this at home, you can’t enumerate all the possibilities here. It would be very inefficient.

MF: I guess finalizing the BIP, it is a bit closer to the use case than a IRTF standard. IRTF would be a “We have this paper. Academics are happy with the proof.” But it is not spec’ing it for a particular real world use case. Would that be correct to say?

TR: I think it is spec’ing it. It is a specification. Maybe Elizabeth knows more about the use cases that they have in mind.

MF: Are there particular use cases that this IRTF standard is being geared towards? With Bitcoin we have a couple of Bitcoin specific requirements that might not apply to other blockchains or other use cases. How close to a use case is this IRTF standard for FROST? I think Elizabeth has dropped off the call. And of course you can do nested MuSig within FROST and nested FROST within MuSig. But from a Bitcoin specific it makes sense to finalize MuSig first and then work out how one might nest into the other or vice versa.

TR: I really need to stress that we believe we can do this but we really don’t know. I could write down a scheme but I don’t know if it is secure. We’d need to prove it was secure and nobody has done that so far. I wouldn’t recommend using nested MuSig at the moment.

# libsecp256k1 scope

MF: Let’s finish off with libsecp256k1. I don’t know which is priority. Finalizing the MuSig2 BIP or getting a API release out for libsecp256k1. What’s your current thinking, obviously there are other contributors, other reviewers, other maintainers, on how close we are to having a libsecp256k1 release and formal API?

TR: You mean MuSig2 in libsecp256k1?

MF: I’m assuming MuSig2 won’t be in that first release.

TR: No, I really hope we have it in that first release.

MF: This x-only pubkey issue needs to resolved before there would be a libsecp256k1 release. And any other things that need to be finalized in terms of that MuSig2 BIP.

TR: I think the roadmap for MuSig2, at the moment we’re making changes to the BIP, it is mostly there. There are some final issues, mostly related to the x-only things where we need to do some changes, we also need some writing changes. They can always be done later. Once we are really confident about the algorithms that we have we can update the implementation in libsecp256k1-zkp or do it on the fly even. I need to say here that the current implementation based on an earlier version of the BIP draft is not in libsecp256k1 but in libsecp256k1-zkp which is a fork of this library maintained by Blockstream where we add a few pieces of functionality mostly relevant to our Liquid sidechain. But we also use it as a testbed in a sense for new development. That is why we added MuSig2 first there. Once we have the BIP finalized we will first the libsecp256k1-zkp implementation to match the finalized BIP. When I say “finalized BIP” at the moment it is a draft, it is not even proposed. We need to get it a BIP number, put it out for review. Maybe there are more comments and we need to update things. The plan is then to update the implementation in [libsecp256k1-zkp](https://github.com/ElementsProject/secp256k1-zkp/blob/master/include/secp256k1_musig.h) and once that is stable I really want to see this in libsecp256k1. Recently there has been discussion about the [scope](https://github.com/bitcoin-core/secp256k1/issues/997) of the fork and the library and so on. I tend to believe that things that are useful to the wider Bitcoin ecosystem should be in libsecp256k1. I believe MuSig2 is useful to the wider ecosystem so we should add it there. At the moment it is maybe nice in libsecp256k1-zkp because it is easier for us to get things merged and easier to play around with it in an experimental state. But once that code is stable we should add it to libsecp256k1.

MF: The libsecp256k1-zkp repo, other people are using it. Is it designed to be a repo that other people use. I suppose if you’ve got experimental on the things that you think are experimental it is kind of user beware type thing. Would there be a release for libsecp256k1-zkp as well? That’s predominantly for Elements, Liquid but if you use it it is kind of user, developer beware type thing.

TR: That’s a good question. I think at the moment it is a little bit of both and that is why I started this issue and this discussion. The discussion was there before in more informal channels. If you ask me personally what I’d like to see is in libsecp256k1 we have the things for the Bitcoin ecosystem and in libsecp256k1-zkp we have things for the Elements ecosystem and the Liquid ecosystem. If we have that kind of separation then the separation would be clearer. On a possible release of libsecp256k1-zkp, so far we haven’t talked about this at all. Maybe we wouldn’t need a release because it is used mostly by the Elements and the Liquid ecosystem that we (Blockstream) mostly control. Now that I think about it it is not even true. There are hardware wallets that support Liquid, they use libsecp256k1-zkp. I guess whenever you have a library, releases make a lot of sense. The truth is so far we were too lazy to put out a release for libsecp256k1, we should do this now. Maybe that is a good starting point to think about a possible release for the libsecp256k1-zkp library too. Independently of whether we move MuSig2 to this other library or not.

MF: It is hard, there are a lot of grey areas here. You don’t know where to draw the line. Which features should be in each library if any. Whether a feature should be in libsecp256k1 or libsecp256k1-zkp or neither. And also how much time the maintainers including yourself can dedicate to reviewing it.

TR: Upstream, the discussion in libsecp256k1 is much more interesting in that respect. There we really have a community project. We want to have the things there that are relevant for Bitcoin I think. But of course our time is limited. In the libsecp256k1-zkp fork, it is a repo controlled by Blockstream, we could do whatever we want with this repo. That’s why we don’t care that much what we put in there but maybe we should care a little bit more and have a discussion on the upstream repo. Then it would be more meaningful for everybody.

# Reusing code for future proposals (e.g. CISA)

MF: There was some [discussion](https://github.com/ElementsProject/secp256k1-zkp/pull/120#issuecomment-759674484) here. You’ve discussed some cross input signature aggregation type proposals, you were on a [podcast](https://stephanlivera.com/episode/400/) recently talking about half signature aggregation. There are some things that can be reused. You are having to think “Not only is this code potentially being used in the use case that we’re coding it up for but it might be used in future”. It is not consensus so it is not cemented on the blockchain but I suppose you are trying to think ahead in making sure it is modular and a potential module could do the same function for both use cases, even long term things.

TR: It is always hard to predict the future when you are writing code. Maybe not yet at an implementation level but at least at the level of writing papers we are thinking about this. You mentioned cross input signature aggregation, it is a different beast, it is not multisignatures, from a theory point of view it is a different thing. It turns out you could use something very similar to MuSig2, probably, we need to write a paper about it and prove it secure before we can be sure, to do cross input signature aggregation. But we are not sure on whether this is the best approach even. If I remember correctly our most recent thinking about cross input signature aggregation is if we want to propose something like this then the resulting crypto scheme would look more like the original Bellare Neven than MuSig. This is a little bit easier to prove secure probably and it is more efficient. In that setting Bellare Neven would be better or a variant maybe of Bellare Neven. If you think about cross input signature aggregation, you have multiple UTXOs, you are spending them altogether or you have different parties controlling them even, they run an interactive protocol and want to spend them altogether in a single transaction with a single signature. If you think about it now you have all the public keys on the chain. Whereas in MuSig you don’t have this. In MuSig you have a Taproot output which is an aggregate key, aggregated from multiple keys, but you don’t see the individual keys on the blockchain. But here you see them on the blockchain. This is exactly what makes Bellare Neven work in this setting. As we discussed earlier, with Bellare Neven all the individual keys go into the verification algorithm so you need them. But for cross input signature aggregation you have them so you could use Bellare Neven. You probably wouldn’t use it exactly, do some minor tweaks to it but at least it is a candidate there. On this issue, I didn’t really read this post, I think here Russell (O’Connor) is assuming that we would use something like MuSig2 for cross input signature aggregation. But this is over a year ago. As I said our current thinking is that we would rather use something like Bellare Neven. Jonas mentioned it here, somewhere in this discussion.

MF: It is not critically important. It is just a nice to have type thing. This long term forward thinking, what can be reused for what. I suppose if you are doing a BIP then you don’t exactly want to go through the hassle of changing the BIP.

TR: When you are writing code you can think about future applications. It is probably good to think about but it might turn out in a month you want to do it differently. That’s how it works.

# ROAST

ROAST paper: <https://eprint.iacr.org/2022/550.pdf>

ROAST blog post: <https://medium.com/blockstream/roast-robust-asynchronous-schnorr-threshold-signatures-ddda55a07d1b>

Tim Ruffing presentation on ROAST: <https://btctranscripts.com/misc/2022-07-14-tim-ruffing-roast/>

MF: I think we’re close to wrapping up then. Perhaps you can explain ROAST. I think Elizabeth briefly discussed it in her [presentation](https://btctranscripts.com/misc/2022-08-07-komlo-crites-frost/#roast) too recently at Zcon. So ROAST is a protocol, a wrapper on top of FROST. What specifically are you concerned with re FROST to want something on top of it to not be susceptible to certain things?

TR: Let’s say you have some threshold setup, I think the example I use mostly here is 11-of-15. You have a 11-of-15 setup and you want to create a signature so you need 11 people. The problem with FROST is you need exactly 11 people. You really need to commit on the exact subset of 11 people that you want to use. If it turns out that one of these signers in this set is offline or doesn’t want to sign then you need to reset the protocol from scratch. You need to pick another subset of 11 signers, kicking out maybe that one signer who was offline and replacing it with another one. But then it could fail again and fail again and so on.

MF: You have to decide upfront when you start the FROST protocol which 11 signers are going to be signing. If one doesn’t sign then you fail and you have to start again.

TR: Right. ROAST gives you a clever way to restart in a sense so you don’t need too many sessions in the end. Maybe I have to start a few protocol runs of FROST but I do it in a clever way so I don’t have to start too many of them. Another nice feature is that the resulting thing, what ROAST gives you is an asynchronous protocol in a sense. You can always make progress, you never need to have timeouts. For example in the simple approach that I just described here, you start with 11, maybe 10 of them reply and you have some 11th signer that never replies. It is not clear, maybe the network is super slow and at some point it will reply or it might never reply. If you do this naively at some point you would need a raise a timeout. Then maybe you’re wrong because you raise a timeout and a second later the message arrives. You would have aborted but actually the guy was there. ROAST avoids this because it never aborts sessions, it just starts new ones. It never needs to abort existing sessions. It works by starting one session and at some point after a few people reply you already start a second session. Either the first session can complete or the second session. If a few people respond in the second session you may even start a third session and so on. You leave them all open so you never miss a message. You never kick out somebody because he seems to be offline. You never need some kind of timeout. This is useful in real networks because timeouts are difficult. You never know what the right value for a timeout is.

MF: The parties of the 11-of-15 on Liquid are expected to be online all the time? I suppose it is just a hard decision, if you’ve got 15 parties why choose a specific 11 of them? Why would you ditch 4 of them? There’s no reason to if they are all equal parties.

TR: All ROAST does is start FROST sessions. It needs to start a first session for example and for this first session you need to make some choice. You need to pick some 11 to which you do the first attempt. But yeah you could just randomize it. Take a new random selection every time for example or always take the ones that responded quickly in the past. That is another meaningful strategy. I’d guess you would want to have some randomness involved. If you always pick the same 11 and they always work you would never notice if someone failed. Maybe one of those 4 that you don’t pick goes offline and you wouldn’t even notice. I guess you would notice because the TCP connection drops or something like this. But you want to have some randomization to make sure that everyone is picked from time to time to see if things are working. This is mostly just an implementation detail I think. If people are interested in ROAST specifically I gave a [talk](https://btctranscripts.com/misc/2022-07-14-tim-ruffing-roast/) about it which is also on YouTube. Maybe you can add it to the reading list.

MF: We were discussing before about changing it from a 11-of-15 to a 11-of-16 or whatever. If that is going to change regularly or semi regularly I suppose ideally if you could avoid that onchain transaction you would but it sounds like you can’t do that. You would need an onchain transaction every time you changed the setup for Liquid.

TR: But I don’t think that is a big deal.

MF: It hasn’t changed for years? Is it still the same 15 that it has always been? Or have they been swapped in and out?

TR: I don’t think they have been swapped in and out. But it is not a big problem to make onchain transactions because they do onchain transactions all the time, they do pay outs and peg outs from the Liquid network. Doing an onchain transaction isn’t a big deal. Even if you wouldn’t do it constantly how often do you add a member to this 15? Maybe once a month or so.

MF: I don’t know, I have no idea how it works. I know it is a 11-of-15 but I have no idea whether parties have been swapped in or out, it doesn’t seem to have changed from the original 11-of-15.

TR: We are adding more members to the federation but at the moment we are not adding more members to this set of signers because we have committed on this 11-of-15 thing because of some specific reason, how multisigs currently work in Bitcoin. If you go beyond 15 it will be more inefficient. ROAST in the long term would maybe give us a way to scale that number without losing efficiency onchain. Even in that setting if it was easy to add people we wouldn’t add a new member every day. Even if you do it every day one transaction per day, that’s not that expensive.

MF: Not currently. We don’t know what the fees will be like in future. Back to 2017 fee levels.

TR: At least at the moment it is ok.

MF: We don’t care at the moment. Is it currently randomized in terms of choosing the 11-of-15 in the CHECKMULTISIG. How do the 11 decide on who is going to sign?

TR: That’s a good question. I’m not sure. I think at the moment we have a rotating leader and the leader will ask everybody else to send a signature. We just take the first 11 signatures that we get and put them on the transaction. It uses this naive Bitcoin threshold sig, this is exactly where it is better than FROST in a sense. With this approach you don’t need to precommit on which 11 you want to use. You can just ask everybody for their partial signature and you wait until you have 11. But you can ask every one of the 15 members and take the first 11. Maybe we wait for a second longer and then randomize it, I don’t know. I bet we take the first 11 but I would need to read the code or ask people who know more about Liquid.

MF: I’m assuming it still uses CHECKMULTISIG rather than CHECKSIGADD. The benefit of using CHECKSIGADD is probably not worth the hassle of changing it.

TR: I’d need to ask the Liquid engineers.

# Q&A

Q - Back in MuSig land, in the [BIP](https://github.com/jonasnick/bips/blob/musig2/bip-musig2.mediawiki) there is a section called verify failed test cases and it provides some signatures. One of them exceeds the group size and it fails. One of them is the wrong signer and so it fails. And one of them is the wrong signature… why is that an important test to make?

A - In the test vector file, just yesterday we [converted](https://github.com/jonasnick/bips/pull/33) that to a JSON file. The reason is we really want to have a specific property in signatures. There are different security notions of signatures in theory. What we usually expect from a signature scheme, even without multisigs, just from a single signer, normal signature scheme, is some unforgeability notion. This means you can only sign messages if you have the secret key. There are various forms of unforgeability and what I just described is weak unforgeability. There’s also strong unforgeability, a little stronger as the name says. Let’s say I give you a signature on a specific message. You can’t even come up with a second signature, a different signature, on this specific message. This is strong unforgeability. If you didn’t check for the negation then you could easily do this. I send you a signature, you negate it and you have a different signature. It is just negated but it is different. The reason why we want to have this strong unforgeability is mostly just because we can have it. It is there. Have you ever heard of malleability issues in Bitcoin? This is specifically also related to this because this is one source of malleability. In SegWit signature data became witness data and from SegWit on it doesn’t influence the transaction IDs anymore. But before SegWit and with ECDSA this was one source of malleability. With ECDSA you could do exactly this. An ECDSA signature is like a Schnorr signature, it is two components. You could just negate one of them.

Q - For the negation is that multiplying the whole point by negative one (-1) for example or is that mirroring it on the other side of an axis. What does negation actually look like when it is performed?

A - I’m not sure what exactly is negated in this test case but if you look at the Schnorr signature it has two components. It is a group element, a point on the curve, and it is a scalar. The scalar is in a sense an exponent, something like a secret key. You could negate either. BIP340 makes sure that no matter what you negate it will always be an invalid signature. But in general it is possible to negate the point or it is possible to negate the scalar. Look into the old ECDSA specification because this had this problem and you can see how the negation was ignored there. When you have a negation, you have a signature, you negate one of the components and you get another valid signature. 

MF: I went through the Schnorr test vectors a while back and Pieter [said](https://bitcoin.stackexchange.com/questions/99418/how-do-i-tweak-the-bip340-test-vectors-to-check-that-signature-verification-fail/) negating means taking the complement with the group order n. “The signature won’t be valid if you verify it using the negated message rather than the actual message used in the signature.” 

TR: This is negating the scalar, what Pieter is talking about.

MF: It is the same thing that is being asked about?

TR: It is the same thing. There are two things you could potentially negate. A Schnorr signature has two components `R` and `s` and you could negate `R` and you could negate `s`. I guess `s` has been negated but the comment doesn’t say.

MF: Ok thank you very much Tim, thank you Elizabeth for joining and thank you everyone else for joining.

TR: Thanks for inviting me.

