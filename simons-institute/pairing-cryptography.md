---
title: Pairings in Cryptography
transcript_by: Bryan Bishop
tags:
  - cryptography
speakers:
  - Dan Boneh
date: 2015-07-14
media: https://www.youtube.com/watch?v=8WDOpzxpnTE&list=PLgO7JBj821uGZTXEXBLckChu70kl7Celh&index=21
---
[Dan Boneh](http://crypto.stanford.edu/~dabo/) (see also [1](https://en.wikipedia.org/wiki/Dan_Boneh))

slides: <http://crypto.biu.ac.il/sites/default/files/3rd_BIU_Winter_School/Boneh-basics-of-pairings.pdf>

<https://twitter.com/kanzure/status/772287326999293952>

original video: <https://video.simons.berkeley.edu/2015/other-events/historical-papers/05-Dan-Boneh.mp4>

original video sha256 hash: 1351217725741cd3161de95905da7477b9966e55a6c61686f7c88ba5a1ca0414

Okay, so um I'm very happy to introduce another speaker in this historical papers series seminar seminar series which is organized by Daniel Wigs and Vanakutanata. Daniel is here but where's..? Okay. All of these talks are being recorded, you can watch some online if you have missed some. It's a pleasure to introduce Dan Boneh, a professor at Stanford. Dan is a unique person in our community. There are a few maybe a handful of people like Dan who are able to combine an excellent level of theoretical computer science and research and practice and implementation of things and so on. Our field is in great debt to Dan Boneh for introducing [Weil pairings](https://crypto.stanford.edu/pbc/notes/elliptic/weil.html) into cryptography and implementing it with the notion of identity-based encryption. The introduction of [bilinear maps](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.111.7700&rep=rep1&type=pdf) really created a revolution in our field. The number of citations of this paper and those with this technique is simply tremendous. He is also responsible for the microwave attacks, which is a paper he did while he was at Princeton, which really set off a field of tampering in order to extract cryptographic materials, which is another area that has flourished over the years. And also he had the scheme with Go and Nissem with having the first crypto system where you could do as many additions as you wanted with single multiplication, and this result kept the hope going that we would find a fully homomorphic encryption scheme and I think Dan nurtured this idea throughout. On the practical side, he has ingenious ideas and beautiful ideas, so he has this password scheme where the idea is that you despite knowing the password and being able to get into the system, you would not be able to transfer this information to another person, which seems paradoxical but his results seem to transfer along these lines. Many of his ideas are like this where you say "hm, wonderful". He has contributed, raised a generation of students. I think at any given time he has about 50 students. Well that might be a little bit of an exaggeration. Also he teaches courses on [cryptography on Coursera](https://www.youtube.com/playlist?list=PL9oqNDMzcMClAPkwrn5dm7IndYjjWiSYJ), which is an online education platform. They are amazing classes. His work has been noticed not just by us, but the community as well, such as the Packard prize and ... and this is just to name a few. To finish with a little story which is not research and sort, it was clear that Dan would be a cryptographer because he intended the first Crypto in Santa Barbara. It's a true stroy. He was a child living in Santa Barbara at the time. His father was at a university, but he was there, and from there present and he started a great career. So please welcome him.

I'm really blushing. Thank you. I don't think I have ever heard an introduction like that. In fact, I should just end the talk right here and declare victory. So thanks for the introduction, and thanks for gviving me a historical relic talk. I don't think of myself as a historical relic, but so be it. I would have enjoyed to talk about more recent work we are doing, but I'll guess I'll do that some othe rtime. For now, I guess I will talk about the history of pairings, whre they come from, and where they have been used. Before I get started, I wanted to thank everyone for finishing their TCC submissions on time. I think the submissions server just closed. Everyone is probably tired and thinking about subscripts you got wrong or something. In this hour, I wanted to focus on stories and not torture you with lots of proofs. Hopefully this will be a light talk, we'll see how it goes.

With that, let's get started. I am going to talk about how [pairings](https://en.wikipedia.org/wiki/Pairing-based_cryptography) are used in crypto. Where do pairings come from? And the impact that they have had. I am going to try to outline a bunch of open problems. I hope I can inspire you to work on these open problems. I think there's a lot of progress to be made. Some of these are open problems on pairings, some are that we want to do it with [LWE](https://en.wikipedia.org/wiki/Learning_with_errors#Public-key_cryptosystem) (see also [homomorphic encryption](https://en.wikipedia.org/wiki/Homomorphic_encryption)) but we know how to do it only with pairings. Hopefully this can inspire you to come up with LWE-based constructions.

# Standard computational complexity assumptions

Let's start at the beginning. In the beginning, there was the [diffie-hellman protocol](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_problem), which works in a group of prime order. It's a famous protocol, you know, sending g^A and g^B and getting the secret key, the shared key is g^(AB). Security of the diffie-hellman protocol of course follows from the decision diffie-hellman (DDH) assumption, so it should be the case that this g^ab is indistinguishable from a random element from the group. So we all know and love the DDH assumption. There are a lot of consequences and applications to the DDH assumption. More generally, we state these complexity assumptions in the group G, these are kind of just the standard complexity assumptions that we know and love. We would like the discrete-log problem to be difficult, so I give g, g^x, and it should be hard to get x. We would like the computational diffie-hellman (CDH) problem to be difficult ([CDH assumption](https://en.wikipedia.org/wiki/Computational_Diffie%E2%80%93Hellman_assumption)), given g, g^x, g^y, it should be difficult to get g^(xy). And as we said, we like the [decision diffie-hellman (DDH) problem](https://en.wikipedia.org/wiki/Decisional_Diffie%E2%80%93Hellman_assumption) to also be hard, where you have g, g^x, g^y, g^z and you get 0 if z=xy and you get 1 otherwise. So again these are the standard complexity assumptions that you all live with every day, and we make lots of uses for them.

# Which group G should be used? FpStar?

The first question is that, in the diffie-hellman protocol, or at least in the abstract diffie-hellman protocol, the first question that comes up is, which group g should you actually use? What is the group that we instantiate with? Of course, Diffie and Hellman, when they originally wrote their paper, they instantiated their protocol using a group defined over a finite field. So they used a group FpStar ((7min 44sec)). So this is all nice and fine, and this works well in practice. The only problem with this is that the [discrete log problem](https://en.wikipedia.org/wiki/Discrete_logarithm) in FpStar is not as hard as you would like. As you know, there are sub-exponential algorithms that actually break discrete log in FpStar. Because of these sub-exponential algorithms, we have to use a relatively large prime to get security to be wher it's supposed to be. Today people use primes that are on the order of 2000-bits. The recommendations are to use primes as much on the order of 3000 bits. So these are relatively large primes which cause the protocol to be slow. So I'm sure you're all aware of this.

The search for other groups has kind of been going on for quite a while. There are other groups that have a hard discrete log problem in which you can try to run the diffie-hellman protocol. Right? So you can use extension fields, matrix groups, class groups, all of these have bee explored for running the diffie-hellman protocol. Unfortunately all of these either have an easy discrete log or a sub-exponential discrete log problem, which would result in large parameters and be somewhat inefficient, or they have a slow group operation which would again result in a slow protocol.

# Class groups

Before we go on any further, I wanted to mention this one fact about class groups which used to be ignored. Maybe this will be useful to you in the future. Class groups are things that kind of have been proposed in what I want to say was the 80s or so, and somewhat died. They're not really used in crypto these days. There's one property of class groups that is useful for people to remember. So, if you need a group where the group size is unknown, so you want a group of unknown order, the standard way to generate that is that you just generate an RSA modulus, and we know that a multiplicative group modulo an RSA modulus has an unknown order. Its order is 5n and 5n is hard to compute assuming factoring is hard. Well, suppose you wanted to build a group of unknown order, without a trusted entity. Someone with RSA, someone has to multiply the two primes together and publish this modulus n. So, if you wanted to generate a group of unknown order, without a trusted entity, it turns out that class groups are a really good way to do that. These are groups. They are easy to define. Computing their order takes exponential time. Groups of unknown order, without a trusted entity. So this is good to keep in mind. Yeah, question?

Q: ...

A: So the best algorithm takes sub-exponential time. There's no known better algorithm, exactly.

By the way, an alternative, just to drive the point home, if you need a group of unknown order, an alternative way to do it without a trusted entity, is to just generate a large enough random number and hope that it has two large prime factors. Turns out you have to generate a relatively big number for that to happen, and class groups are actually a more efficient way to do that. So just keep this in mind when it comes up in applications like accumulators where you need groups of unknown order and you can generate them here without a trusted entity. If this ever comes up, then keep in mind that this can be something put to use.

# Group of points of elliptic curves

Okay, so those are kind of groups that have been considered over the ages. All of them are not better than FpStar. And the first group that has turned out to be better than FpStar of course has been the group of points of elliptic curve, proposed by [Miller 1985](https://www.researchgate.net/profile/Victor_Miller/publication/2812617_Elliptic_Curves_and_their_use_in_Cryptography/links/0c96052e065c9e4f39000000.pdf) and [Koblitz 1985](http://www.ams.org/journals/mcom/1987-48-177/S0025-5718-1987-0866109-5/S0025-5718-1987-0866109-5.pdf) where first of all, the best known algorithm for discrete log takes exponential time, it's square root of the size of the relative prime. So this means again we can use much much smaller primes and achieve the same complexity as working in FpStar, at least as far as we know, maybe there's a breakthrough to be made that we don't know about. Today, as far as we know, we can use much much smaller primes because the discrete log problem is much harder in this group, and we have efficient group operations. There's a famous table (for size of primes) that came out of NIST that says, if you want comparable security to a 128-bit symmetric key, if you're using FpStar, you're supposed to use a 3092-bit modulus, and if you're using an elliptic curve, you can use just a 256-bit modulus. So as a result, operations here tend to be faster than operations here. And this has gotten quite a bit of deployment.

The interesting thing is that for many years, people have only looked at elliptic curves just for their efficiency improvements. You can use smaller primes. So things run faster. And that's the only interest in elliptic curves, just efficiency improvements. It turns out, actually, and that's kind of what spurred this topic, it turns out that elliptic curves actually have an additional structure called a pairing and that gave birth to this whole new tool which I am going to talk about. Yeah, question?

Q: ... exponential algorithms for discrete log?

A: Yeah, they're basically reducible to kind of finite fields. You have to restrict yourself to abelian subgroups of matrix groups, and then they are reducible to finite fields. Yeah, so, good question.

Okay so before, this is the reason; so for many years this structure was ignored, in fact was viewed as a problem and the point is that this structure is actually quite useful.

<https://www.youtube.com/watch?v=8WDOpzxpnTE&t=13m2s>

# Quick review of elliptic curves

Before I talk about pairings, I want to go back to this group of points of an elliptic curve, and just make a few comments about this. I'm not sure you're aware of everything happening today, so I just want to quickly point out a couple of issues with it.

First of all, the group of points of an elliptic curve, just as a quick review, what we do is we fix these parameters a and b, these a and b define this equation, this curve, y^2 = x^3 + ax + b, and the group of points is basically the set of solutions to this equation. And of course, this is not just a set of points, there's a group operation defined on them, meaning given two points you can add them up and get a third point, and that is a group operation. So this again, I'm sure, this is just a quick review.

I'll just use E(Fp) to denote this group. Okay, so, in practice, what do people do? First they use a 256-bit prime, that's the only thing primarily used in practice. The measurements basically show that this is 10x faster than using a comparable FpStar, and as a result of this 10x speedup, the world is slowly transitioning to these elliptic curves. It's actually quite remarkable to see this transition. For example, if you look at Google, every time you connect to Google these days, you're actually doing a key exchange using elliptic curve diffie-hellman. All key exchange with Google essentially use elliptic curve. We actually did a study last year, of the top 100,000 websites, if you look at the Alexa top 100k, we connected to each one of those, we asked what kind of key exchange do you support, and about three quarters of them supported elliptic curve diffie-hellman, which means that three quarters of the top 100k websites will by default use elliptic curves over prime fields. So that's quite interesting.

The other interesting thing is that in fact of these 100k websites. Sorry, of the three quarters of the 100k websites that support elliptic curve (ECDHE), almost all of them, 96.1% of them use a particular curve called p256, it has a name. So you wonder, what is this curve p256? Where does it come from? Let me just quickly show you where it comes from. I hope not everybody has seen this.

NIST standard ([FIPS 186-3](http://csrc.nist.gov/publications/fips/fips186-3/fips_186-3.pdf) appendix A): y^2 = x^3 - 3x + b (mod p)

So this curve comes from a NIST standard, it comes in an appendix to the NIST standard. The curve looks like this. This is the structure of this curve. In the standard, literally, the standard says here is the prime you are supposed to use. You'll notice that this is a prime of low weight, so the arithmetic is simple on it.

p = 2^256 - 2^224 + 2^292 + 2^96 - 1

And this is the number of points on the curve, points mod p, it's roughly 2^256. So 256-bits. This is the number of points. And this next one is the coefficient b on the curve (5ac635d8 aa3a937 b3ebbd55 769886bc 651d06b0 cc53b0f6 3bce3c3e 27d2604b). And this is one curve that you can use as a generator, they give you Px (starting with 6b17d1f2 ....) and Py (starting with 4fe3422 ....) which is a point P=(Px, Py).

So as I said, almost all websites use this one particular curve (p256). That's a lot of eggs in this one basket. The next question you should ask is, where did this curve come from? Where did P256 come from? Here the story is more disturbing. In the standard in the appendix FIPS 186-3 appendix D.1.2.3, there's one magical seed ( c49d3608 86e70493 6a6678e1 139d26b7 819f7e90 ) and that seed is hashed using SHA-1 and that SHA-1 hash gives you the parameters for this curve.

So the next question is, where does the seed come from? And we have no idea. Literally. We have no idea. The seed is written like it's stamped in the standard, and we have no clue where it comes from. A couple of people have come forward and said they generated the seed, but we know nothing about how it was generated. In fact, if I told you who these people were, you would be a little worried. (laughter)

Q: ... doesn't this give us some assurance?

A: So here's the problem. So, first of all, the SHA-1 is supposed to destroy any structure in the seed. The thing we are worried about is, imagine there was a faster discrete log algorithm for one out of a million curves. If all curves are dead, then fine, there's no security at all. If all curves are secure, then this is fine. The problem is what happens if only one out of like a million curves are insecure? And in that case, you can pretty much see what the attack is. You loop a million times until you find the seed that you can break, and then that's the thing you put in the standard. That's the concern.

So, yes, this is kind of the state of the world today. There's a big transition to elliptic curves, but this is the curve we all use. And the question is, how hard is CDH on this curve? And we have no idea. So in fact, yeah.

Q: ... from what you said ... 75% of traffic ...

A: Yes. P256.

Q: .. that's not what happens .. these websites support CDH, but most of the connections are not CDH.

A: Most modern browsers support ECDH. And in fact they use it by default. There's a preference for forward-secrecy. And if the browser supports ECDH, the server will choose it.

Q: What percentage of connections are...?

A: Those are difficult numbers to get. But we know that essentially Internet Explorer, Chrome, Safari, all the popular browsers all support elliptic curve diffie-hellman, and if it's presented as an option to the server, then the server will choose it. So that suggests that the majority of connections to those servers are in fact doing key exchange with ECDH. So very very very common. But this one curve is being used everywhere. If you're interested in the paper, we actually list 96% using this, so you should ask, what do the other 4% do? So they do all sorts of crazy things. And in the paper we kind of list what they do. Yeah.

Q: ..

A: No. The client says I support ECDH. And then the server says I am going to choose this cipher spec, and here's the curve you're going to use. And P256 is one of the named curves, and that's how it's specified. So, good.

I wanted you to be aware that this is happening. In fact, there is an active effort at NIST now to try and move to new types of elliptic curves (NIST Workshop on Elliptic Curve Cryptography Standards). The focus seems to be mostly on performance. It's not so clear how you choose. There's really very little theory to tell you how to choose a curve that would actually give uh that would kind of have some assurance that it's secure. There's no family of hardest possible curves in terms of random set reductions. So it's kind of, it's not really, .... [there is theory that is needed to help us in choosing these curves](https://safecurves.cr.yp.to/), right now that really doesn't exist.

Okay, this was a quick-- yeah?

<https://www.youtube.com/watch?v=8WDOpzxpnTE&t=19m47s>

Q: ...

A: Why not choose a random curve? Oh you mean every server would choose its own curve? It would just flip bits and choose its own curve? It turns out that is not a good idea, and the reason is that there are a lot of tests, that, we do know about many classes of weak curves. If you choose a random curve, there is a risk that you'll fall into one of those weak classes. So what NIST does is they hash, then they check whether it's one of the weak curves, and if it is then they add one to the seed and then they hash again and check again. So basically, p256 is the first curve which is known to not ... which is not subject to the known attacks that follow from this seed. So generating a curve by itself is actually quite a bit of work, doing it correctly is difficult, so it's better that everybody uses a standard curve. Yeah, that's the reason.

Q: So do we know actually that you have for every large enough n that more than many curves with the property you're doing? So you know, the number of cardinal.. do we know that?

A: Ah, yeah. So you're asking, ... it's actually, most curves are fine. Most curves in fact have a hard discrete... as far as we know.

Q: In order to have pairing...

A: No, pairing is a different story. So far these curves don't have pairings yet. We'll get to pairings. This is a really good point actually. Pairing curves are actually very special, so in fact, these curves themselves don't have pairings, we're going to talk about pairing-friendly curves in just a second.

Q: ...

A: What?

Q: ...

A: Depends on what you want to do. If you need pairings, use a curve that is pairing-friendly. If not, you don't have to.

Q: .. use this for diffie-hellman key exchange, right?

<https://www.youtube.com/watch?v=8WDOpzxpnTE&t=21m30s>

A: Well, no. Hold on. Hold that thought. It turns out actually that it's not a problem. Pairings, if you know what you're doing, pairings are not necessarily the problem. In fact, the point of pairing based crypto is that they are not a problem, they are actually a blessing.

Q: ... if in the future we have pre... attacks...

A: Yeah that's an excellent question. The question is that if we have pre-computation attacks, is it a problem that we use the same curve? P256 is big enough that doing pre-computation is actually too difficult, well as far as we know at least; so the current methodology... I'm describing the state of the world. That's the recommendation and that's what websites do. And the question is, which curves should we use? So there's a need for more theory to help choose curves.

# Pairing cryptography

Okay, so, let's go back to pairings. So that's our topic. So as we said, some curves have an additional structure called a pairing. Let's define that. I imagine that some of you have seen this already. Well, let's just walk through this anyway.

What is a pairing? A pairing abstractly is something that operates on two groups. There is a source group, which we call G, and there's a target group called GT. Now, normally the source group will be the points of an elliptic curve. And the target group (GT) would be just a finite field, just element in a finite field. And what a pairing does is it takes two points in the source group and maps them to the target group in such a way that the exponents multiply. The pairing is bilinear, and bilinear here means multiplication of exponents.

Formally, what a pairing is is a map, which has this bilinearity property because it allows us to multiply exponents in the exponent, but it moves us to a different group, so we can only do the pairing once and never again. And the requirement is that ((23min 25sec)) it is polynomial-time (poly-time) computable and it better not be degenerate. And it's not degenerate, in the sense that it maps generators to generators (g generates G => e(g,g) generates GT).

Okay, and as I said, the best examples that we have so far is where the group G is a group of points of an elliptic curve (G from E(Fp)) and the target group (GT) is from some, basically a finite field, a finite field extension.

Why are pairings so useful in crypto? Really there's two tricks that keep coming up again and again and again. When you look at pairings, one trick that we use all the time is that if you look at the pairing of g^x and h^y, that is, if you are looking at e(g^x, h^y), you notice that the x y come out of the parentheses and then they can go back into the parentheses in the reverse order. So e(g^x, h^y) is the same as e(g^y, h^x). So this we use all the time. During encryption you use e(g^x, h^y) and during decryption you use e(g^y, h^x). So that's one reason why pairings are so useful in crypto.

The other reason why they are so useful in crypto is because basically they allow us to compute inner-product on encrypted values. So if you have a vector of exponents, a vector given to you in the exponent on the one hand, and another vector given to you in the exponent on the other hand, you can compute the inner product of these vectors just by computing the vector of the corresponding pairings. These two tricks come up again and again and again in pairing-based crypto. And that's basically why we get the functionality we get.

More generally, you can imagine I might have a matrix here. So g^x1 in this example would instead be g to the power of some matrix. And instead of h^y1 it would be h to the power of some matrix. What the pairing allows us to do is compute the product of these matrices in the exponent. It's e(g, h)^(x dot y). And we can only do two matrices and no more. And that's, in some sense, the limitation of pairings. We can multiply two matrices, and that's all we can do.

# Consequences of pairing

Let's talk about some consequences of pairing. Basically, if we have a pairing then the decision diffie-hellman (DDH) problem that we know and love in traditional group, actually turns out to be easy [J'00, JN'01]. And here's how we do it. If I give you g, g^x, g^y, g^z, and you want to test whether z=xy (z equal to x times y) then all we do is just compute these two pairings and by the property of the pairing the x and the y come out of the parentheses and you get a equality only if z is equal to x times y. To test if z=xy you do: e(g, g^z) =? e(g^x, g^y).

So DDH becomes an easy problem. So we can't do the standard diffie-hellman protocol in pairing groups. And the other property is that we get this reduction from discrete log in G, to discrete log in the target group. So it better be the case that discrete log in the target group is hard, otherwise this discrete log in the source group will not be hard. DLog reduction from G to GT is described in [MOV'93]. DLog in G you have g, g^a from G, this becomes DLog in GT with e(g,g), e(g,g^a) from GT.

So those are the two immediate properties that we get out of pairing. Now we can ask about the complexity assumptions that come up in the world of pairing. Basically we get the standard complexity assumptions that we know and love. So the discrete log is a perfectly kind of a requirement for pairing-based groups, we need the discrete-log problem to be hard. We need the computational diffie-hellman (CDH) problem to- we would like it to be hard.

When it comes to CDH, I already told you that CDH is not hard, it's an easy problem. But we can fix that, basically if we just add one more element. By the magic of powerpoint, you can see that here ((26min 38sec)). This is the [bilinear decision diffie-hellman (BDDH) problem](https://cseweb.ucsd.edu/~hovav/dist/kbdh.pdf). And this becomes the new replacement for CDH. And a lot of encryption schemes actually use this as a randomizer for the encryption, and that's what we use for encryption and decryption. These are just translations of the standard assumptions. So far so good? Any questions? So far we're just doing basic stuff. We'll get to more sophisticated things in a minute.

# Decision linear assumption (DLIN) and k-DLIN

Okay. There's one assumption that turned out to be quite useful in the world of pairings. In fact, it's almost like an assumption that allows us to build many different assumptions. This assumption is called the [decision linear assumption (DLIN)](https://en.wikipedia.org/wiki/Decision_Linear_assumption), described in [BBS 2004](https://crypto.stanford.edu/~xb/crypto04a/groupsigs.pdf) and others. It's a little bit of a wacky assumption to describe. I tried to capture the cleanest form here. But again, this turns out to be, the DLIN assumption is almost the most important complexity assumption that is used in pairings. Many constructions that we would like to have, can be built out of this decision linear assumption. Let me try to explain it to you, and then we'll state a more, a cleaner version of the assumption. ((27min 44sec))

In the decision linear assumption (DLIN), I'm giving you a bunch of generators. k+1 many generators. Now what I do is I give you random exponents of these generators. And I either give you the sum of these exponents, so a linear combination of these generators, that's where the name comes from. So either I give you a linear combination of these generators, or I give you some other random exponent. The question is whether you can distinguish these two things. And if you can't distinguish them, then we say that the decision linear assumption (DLIN) holds. And again as I said, this is a very important assumption in the world of pairings. Turns out there are many ways to argue that this assumption holds. You can give generic arguments, proofs to say that this holds, and as I said, many constructions reduce to this particular assumption. If you would like, this is like the LWE of pairings in some abstract sense.

Hierarchy: DDH == 1-DLIN >= 2-DLIN >= ... >= k-DLIN, where DDH === 1-DLIN is easier to brak ad k-DLIN is considered "harder" to break.

In fact, the larger, let me give you a little bit of intuition about the assumption in that there's this parameter k, it's called k-decision linear, it turns out that the larger k is, the harder the problem becomes. The harder the problem, the weaker the assumption. So like, 1-DLIN is just DDH, which you can break using a pairing. 2-DLIN you can't break even if you had a pairing, but you can break it if you have a 3-linear map. So we get this hierarchy of assumptions. And this 2-DLIN assumption is very useful in the world of pairings. And as I said, if you have a (k+1)-linear map in G, you can break that k-DLIN and it's false. But if you only have a bilinear map, a pairing, then all 2-DLIN and 3-DLIN and 4-DLIN seem to be fine assumptions to use.

Assumption: k-DLIN holds even if k'-linear map in G for k'<=k.

Q: ...

A: What?

Q: ... so in the left exhibition, the term is sum of th..

A: Sum of the exponents, yeah.

Q: It is sum?

A: Sum, not product. It's called linear assumption because it's a linear combination of the exponents.

Q: .. g^x, g^y...

A: If you plug in k=1, you get g1^x1 is g1^ .... oh yes yes yes, ignore this. .... that's the DDH assumption. The multiplication is happening implicitly. There's a multiplication going on in there. It is DDH. That's a good question.

So let me just tell you a quick variation of DLIN. There's a cleaner way of thinking about this assumption which I think is kind of elegant and very clean.

Many bilinear constructions can be based on 2-DLIN. A useful implication is that g is from G order q.

Which is to say, what the DLIN assumption says is that if I give you a random matrix, under this assumption decision linear, if I give you a random matrix in the exponent, so g to the first element, g to the second element, g to the third element, basically the entire matrix is given to you in the exponent, that's indistinguishable from g to the power of some other matrix, where the matrix is bounded by rank k. When we use it, we use it in this form. So the reason why decision linear assumption (DLIN) is useful is that it says that you can't distinguish random matrices in the exponent from low-rank matrices in the exponent. That's a cleaner way of stating the assumption.

What I wanted to do next... oh I have to speed up a little bit? How much time do I have?

<https://www.youtube.com/watch?v=8WDOpzxpnTE&t=31m30s>

Well that's what I wanted to tell you; it said an hour, but actually it's an hour and a half. Oh, really? Cool. Okay. So I can torture you... well, I'll try not to go over too much, or maybe I'll leave time for questions and discussions. Alright. There are things I want to get to.

# Where pairings come from

The next thing I want to do is tell you about where pairings come from, and then we can talk about applications.

Where did pairings come from? We have our basic elliptic curve group, E(Fp) = G. We have a group of points over a finite field, E(Fp), and we're going to call this group G. So here I'm giving you pairings under the hood how they actually work. There are q points in this group, q is the size of the group, it's defined over a field of size p. And we know that q is about the size of p. So far so good.

If we look at the number of points over an extension, so all of the sudden we look at the points on the curve not only over Fp but Fp^alpha, an extension to Fp, what the image that pops up is that all of the sudden there's another set of q points so that the total... so that the group of order q, the group of points of order q, is in fact a 2-dimensional object. Elliptic curves you can naturally think of them as 2-dimensional objects, and again basically you have a q by q, or zq by zq, as groups of .. as the points of order q. Now, you can take arbitrary two points in this two dimensional structure. And it turns out that on these 2-dimensional structures, there was a natural pairing which was defined by Adrian Vaille ... when he did his very very famous work on curves, one of the things that he did is that he defined this pairing. I love this story by the way. This was work that he published in 1949.

Maybe some of you have heard me say this before, but Andre Ve actually defines the pairing while he was sitting in jail during World War 2. So he wrote his autobiography which actually was really fun to read, his autobiography was about his life during WW2 and the utter chaos that Europe went through during WW2, and it's from the perspective of what is it like to be a mathematician in a time of war. And he actually refused to serve in the French army, so the French promptly stuck him in jail. Apparently he was in jail for like 2 years or so. And he says this was apparently by law they were required to give him a pencil and paper and apparently this was the most productive time of his life (laughter). Yes, so this is to the point actualy, he says this in his book, he says in his autobiography that he was considering sending mail to the head of the French mathematics academy recommending that every mathematician spend at least two years in jail because it would be so productive. This is literally in his book.

So in this work, defining this pairing which he did while he was sitting in jail, the odd thing to me is that he did extra work to check that his definition was computable. In fact, when you look at modern accounts of [algebraic geometry](https://en.wikipedia.org/wiki/Algebraic_geometry), they give a very different definition of pairing, one for which it's easier to prove its properties, but it's completely useless from a computer science point of view. It's really odd that he did extra work just to get a definition that is computabe. So anyhow, he gave a definition of a pairing, take this pair p and q, and the definition basically, I just wrote it up very abstractly, what it does basically is that there's a function F sub P, it's just a polynomial, a polynomial in the coordinate, it's defined by the point p. There's a certain polynomial defined by the point p. It's a bivariate polynomial with input that are the two coordinates of the point q. You treat it as x, y and then you evaluate this polynomial and you evaluate it and you get this pairing. The problem with this polynomial is that it has exponential degree. And in fact someone wrote a paper saying the pairing is non-computable because this polynomial has this exponential degree. And Victor Miller did (1984), in a seminal work in 1984, is that he said yes this polynomial, this is a bivariate polynomial with exponential degree, but in fact it has a short line program that allows us to evaluate it very quickly. Miller sent it to STOCK and it was rejected because "it had no applications". Then he burried it for ages. I like this example-- if any of you have sent papers to TCC and you get back comments that the paper has no application, like maybe what happened recently, then you can always confer with Miller and make fun of the committee for many years after the fact. (laughter)

<https://www.youtube.com/watch?v=8WDOpzxpnTE&t=36m35s>

So anyhow, this was finally published in 2004, it was kind of too embarrassing that such an important paper would remain unpublished, so finally this was published in a 2004 special issue of the Journal of Crypto. So he showed in fact that pairing is computable, and it has all the bilinearity properties that we would want. There's only one problem, which is that what we would like to have-- in crypto, we don't like these two-dimensional structures, we like to think in cyclic groups. We'd like to basically have our pairing just defined on this ground field, this ground group. The problem is that if you take two points in the ground group, if p and q live over here, then the pairing would always be 1. It's degenerate on this ground field. So that's kind of unfortunate.

There are many ways to fix it. One way to fix it is that you could use particular sets of curve on which there is an automorphism map that basically allows you to move the points, so when you want to compute the pairing with p and q, you first move the point, you move it to somewhere outside of the ground field, and then you're guaranteed that it's not degenerate, and then you actually define the pairing is P plus this automorphism of Q, and that gives you a symmetric pairing, so both groups are the same, mapping you to the target group. So that's one type of pairing.

The other type of pairing is what we call asymmetric pairing, where you actually have two groups. You have a group G1, and then you have a group G2 defined over this extension field, and this group has to be chosen somewhat carefully, and again you would get a non-degenerate pairing on these two groups. The interesting thing is that in this setting, if you just look at the group G1, there is no pairing on it, because the pairing is degenerate. If you just look at the group G2, there is no pairing on it, because the pairing is degenerate. It's a funny situation, where you have a pairing defined on G1 cross G2, but since you have no pairing on G1 and G2, DDH actually appears to be hard both on G1 and G2. So this is sometimes called a [symmetric XDH assumption (SXDH assumption)](https://en.wikipedia.org/wiki/XDH_assumption) that we have a pairing but even though we have a pairing, and normally pairings break DDH, but in this setting the pairings not only not break DDH, we have two groups where DDH is believed to be hard. And this has a whole bunch of applications just on its own.

<https://www.youtube.com/watch?v=8WDOpzxpnTE&t=39m03s>

So that's asymmetric pairings, and it turns out that this is the way to implement pairings in practice. You always implement them using these kinds of groups.

Q: Two questions for the previous slide.

A: Yes.

Q: The one before that.

A: Oh the one before that. This one.

Q: Why is it that you have.. pairing.. when you said it's due to ..

A: Excellent question. Yes.

Q: My second question is, if Miller's paper wasn't published until 2004, the how did it get dessiminated?

A: Yes, yes. This is the beauty of the internet. He wrote his paper in 84.

Q: But it was pre-internet.

A: The internet was around in 1984. I was barely born then, but it was around.

Q: And you had already attended Crypto?

A: 84? Ah. That's, there you go, yes. I think I was in sixth grade back then, or fifth grade, I don't remember.

Anyhow, so the first question is why is it called a Tate pairing? Well, okay so, the Vae pairing is defined slightly differently, it's actually defined as a ratio between two functions. It turns out that the denominator, basically slows you down by a factor of 2, and what was observed was that in fact even if you get rid of the denominator, and you do this extra clean-up step, then you can get rid of the denominator, and everything works twice as fast, so you might as well just use this. The reason why it's called Tate pairing is because Tate pairing is basically half of the weil pairing.

How did Victor's paper get dessiminated? That's a good question. Oh, I know how it happened. So what happened was that Victor wrote his paper, and unfortunately it was rejected. But then he circulated it among friends and, Minez, Comodo, and Vansays, learned about the pairing and the fact that it is computable, and they came up with a reduction from a discrete log on elliptic curve to discrete log on the finite field, using the pairing. And that's where the attribute of course to Victor Miller, and that's where the, that's how it became well known. So if you have a result that is not published, get someone else to write a strong paper that uses it.

Q: .. worked for ideal research ...

A: Yeah, it was dessiminated inside of IBM, that's true. Very very true. But also there was the internet.

Q: .. application for breaking DDH on certain classes of elliptic curve groups.

A: Yeah this was pre-DDH, in fact the first paper I know that uses DDH is from 1991.

Q: But there's a diffie-hellman key exchange protocol, right? That's, and if you use elliptic curves, then it makes it, it allows you to ... which is not exactly.

A: That was noticed much, much later. That was noticed in like 2001. But yeah, you're saying it actually allows you to somewhat weaken discrete log. That was what they were excited about. The DDH aspect was noticed much later.

Q: .. would it be good... high number of points on it, right?

A: Yeah.

Q: So... how..

A: Oh boy. That's an excellent question. Yeah, so, that's an excellent question, there's a whole field, in fact a whole conference, devoted to the question of how do you pick pairing-friendly curves where the number of points is prime. This is not a question I want to answer here. I will say, though, that in this first case ..

Q: My question is can we do it for every ...

A: Yeah.

Q: How many are there?

A: You can do it, under appropriate assumptions about densities of primes, you can do it for every n.

Q: ...

A: You have to assume primes of special form. If I give you a polynomial, then the density of primes along that polynomial are dense enough, it's true, but proving these things is always kind of tricky. Under appropriate assumptions of densities of primes, this will exist for every n. Yeah. I guess that's what you were asking?

Q: And also then, when you map into the second, the target group, you need the same number of elements?

A: Yes, that's right. You basically have, when you construct pairing-friendly curves, you have two parameters that you want prime. You want the size of the source group to be prime. And then you want the size of the target group to be divisible, or the finite field needs to be the finite field minus 1 needs to be divisible by the size of the source group.

Q: My question is .. so your curve has to have that property?

A: Yes.

Q: How many are there?

A: It looks like, using this method, this curve this particular curve, like y^2 = x^3 + x and p=3(mod 4), any time p is 3 mod 4, you will have a pairing group of size p + 1. ((symmetric pairings slide))

Q: So it's not a general curve, it's that curve.

A: It's that curve. This is one method. The second method, the asymmetric pairing method, this will actually let you build curves of arbitrary size, but here this is harder. This actually takes more work. But once you find the curve, everyone can use it, much like we did with P256. Does that answer the question? Cool.

Q: How much do you think of alpha anchor?

A: The alphas are very small. You don't want it to be too large, because the larger the alpha, the slower the operation. Typically you think of alpha as 6, 8 or 10 or 12, so this E(Fp) the p would be like 256 bits, and you would want the alpha to be like 10, so that the discrete log on the finite field is hard.

Q: Do we know that for a discrete value of alpha there exists an infinite family?

A: No, no. The constructions are for specific alpha. And in fact, you don't want alpha to get too large.

Q: For a fixed alpha, like alpha equals 8, ...

A: Well, if you say alpha equals 10, then yes, there's a family, the family will give us as many curves as we want, for varying sizes.

Q: For alpha=10.

A: For alpha=10, alpha=12, various alphas.

Q: For infinite sequences of alphas?

A: There's a taxonomy paper that goes and analyzes many many different alphas, like up to alpha 100 or so, and they say for each one, here's the best family to use.

Q: Infinite sequences of alphas?

A: You don't want alpha to get too large.

Q: As p grows, there's some relationshpi, isn't that true?

A: This goes beyond... alpha of 100 goes beyond what people are interested in. I'm sure it's doable, but nobody bothered.

Q: But theoretically, you move p to infinity, and then you want alpha to grow as well.

A: Yes, that's right.

Q: But that's not understood.

A: Ah, it's just because nobody wrote it down. But it's not that difficult to actually do. Yeah, good question. Any other questions? Okay. So far so good.

Let's move on to more interesting things. And the previous discussion was about where pairings come from.

# Multilinear maps

So the first interesting question you want to ask is, well can we generalize this? As you know, pairings are only the beginning. The real magic comes from [multilinear maps](https://crypto.stanford.edu/~dabo/papers/mlinear.pdf) (also [1](https://en.wikipedia.org/wiki/Multilinear_map)). (BS'03), ([GGH'13](https://pdfs.semanticscholar.org/c909/57a517608a2d2d7e83fedbd64022e8876884.pdf)) and others. Not just 2-way multilinear, but multi-linear. Can we generalize these constructions to build multilinear maps? And the first goal, the easy goal, would be, could we have a 3-way multilinear map, where we have 3 copies of G, and map to GT, such that we have a 3-way multilinearity property.

<https://www.youtube.com/watch?v=8WDOpzxpnTE&t=47m>

I didn't want to write this down on a slide, but I'll mention it. The two, the standard weil pairing, you can think of it as a 2-by-2 determinant, if you visualize things properly, literally what it's computing for you is a 2-by-2 determinant, and that's why it's bilinear, 2-by-2 determinant. You can generalize that and ask, well, what if we just define a 3-by-3 determinant in the exactly same way. You can write down a very precise definition of a 3-multilinear map, and it's in fact, it would be multilinear, and it's a dream come true. Unfortunately, we showed, this was in work with Alice Silverberg, that in fact all these generalizations of pairings from algebraic geometry, that is to say generally abelian varieties, none of them, even though they are all multilinear, and they have all the properties like hard discrete log and multilinear and everything we want, unfortunately none of them are computed by polynomials in the way that the Vale pairing is computed by polynomials. And it's a particular way to show that it's not computable by polynomials, basically you show one gal one go is not invariant under, so there's something magic about the number 2 that makes the pairing computable, and the minute you go beyond 2, it's no longer computable. So if we want multilinear maps, which we definitely want multilinear maps, if we're going to build them from algebraic geometry, we're going to have to build them from a completely different way of doing it.

So of course, my favorite result of the last decade, huge huge result, is a multilinear map, I'm sure you guys have heard about this to infinity by now, of course, GGH'13, came up with this beautiful result, but it doesn't quite solve the original problem in the sense that the multilinear map that operates on noisy representation of group elements and not actually kind of these clean algebraic representation of group elements. So a major open problem, this is actually one of the open questions where I'm spending a lot of my time these days, is looking at pairings that come more from traditional algebraic geometry and see if there's a way to generalize them to get a 3-linear map. I'm absolutely convinced that these exist. If I went to sleep now and woke up in 100 years, I'm certain that we will have a clean 3-way multilinear map without noise. I'm absolutely convinced that this exists. So far everything I have tried doesn't work, so please please think about this too.

Q: agraded algebra?

A: Everything we look at, is actually agraded algebra as well, it's not just pairing. The problem is always one of two things. Either we get a wonderful multilinear map that is not computable, or we get a wonderful multilinear map that is computable but the discrete log is easy. Somehow we always get stuck with one of these two things. But I'm convinced that this exists. So we'll see.

Q: How many jail years do you think?

(laughter)

A: I think this is a good measure of hardness. How many jail years, yeah.

Q: .. offering money to solve problems? So how much are you putting on it?

A: What's the highest prize right now?

Q: 3 dollars.

A: 3 dollars?

Q: There could be a $200. There's a $300. Small hundreds.

Q: And five months in prison.

Q: So how much are you putting up? How much?

A: I'll wager. I'll definitely be your friend forever, and also, I'll definitely do $100. Even $1000, you know what. I will do it. Okay. You caught me in a generous mood. Please work on this.

Q: .. computable bipolynomials... why do we..

A: There's... it's impossible to prove that things are not computable. So instead we would try to generalize the algorithm that Miller gave. The algorithm that Miller gave basically defines a polynomial, the polynomial based on the point p finds a polynomial , and the polynomial evaluates at the point q to give the result of the pairing. So think of a polynomial that would take the coodinates of these 3 inputs, so it takes 6 inputs, and produce the pairing as a polynomial because that's how Miller's algorithm works. Even though it's exponential degree, it's still a polynomial. So what you could show is that's not possible. It's not going to be a polynomial, and you can use that by using GaGoa maps ((51min 30sec)). It doesn't mean, there might be other ways to compute it, but that would require a completely new idea, and we're not there yet.

Q: .. you also convinced there's something hard about it?

A: Yeah, when I say that it exists, I mean it's computable, and it has a hard discrete log problem.

Q: So you can only, at the end, something confuses me.

A: Ah. Well here the challenge problem is just this. I want a 3-way map where discrete log in GT is hard. So G should be computable, and GT should have a hard discrete log.

Q: And we don't need a zero test because there's no noise?

A: Yeah, you don't need a zero test because there's no noise. The way, so, the zero test was needed because you can't compare things because of the noise. If you don't have any noise, then the way you compare things is as bit strings. You don't need a zero test at all, in fact you could do a comparison at any level, not just at the top level.

Q: Unique representations?

A: Unique representations, exactly. Unique representation of group elements. Every group element has exactly one canonical representation.

Q: ... you can't compute it...

A: You can compute it.

Q: ... not grav....

A: This was a simple multilinear map, but you can talk about the graded version of this, where you go from G x G to G x G1 to GT... all the constructions we look at have this grading property. Every group element should have a unique representation. This would allow us to get rid of noise. So when we do obfuscation and have really high degree of multilinearity, the noise wouldn't blow up, because there's no noise. So there's hope that this would give a much more efficient way to obfuscate. That's the hope. Whether it's true or not, some of us have to go to jail for that. (laughter)

Q: .. large .. map.. for large n.. right?

A: Yes.

Q: it's necessarily...

A: It depends on the degree. It depends on how multilinear. If you get up to exponential multilinearity, you have problems. That's true.

Q: Why is there like..

A: Yes, that's why I'm only asking for a 3-way multilinear map. 3, not 4. I am very modest. So the feeling is that the way the constructions would always work is that you would specify k, then we would come up with the algebraic structure that supports k, but not k + 1. Now, remember, k is also going to derive the prime. So if k is too big, then the prime is going to be even bigger. So you will never reach the black box results. That's how this will play out. That's a really good question.

Q: So you're also asking, a computable map for a reverse string?

A: Oh my god, yeah. Yes. Exactly right. If we had a bilinear map, that went from G cross G to G, yes, that would be remarkable, where discrete log is hard. There would immediately be a sub-exponential attack on discrete log, but it wouldn't be broken. That is possible. G cross G to G, and that would essentially give us, what was the $3 million dollar prize, that would give us homomorphic encryption, that's really cheap. Because you can just keep computing on the same group and never change group and you could keep computing for as long as you want. So that would be remarkable, but, even in 100 years, I'm not sure. That, I'm not sure that exists. That's probably too hard.

<https://www.youtube.com/watch?v=8WDOpzxpnTE&t=55m18s>

Was that clear? If you...

Q: .. becomes an algebra?

A: It becomes an algebra, that's exactly right. Yeah, with a hard discrete log. We're nowhere near anything like that.

Q: .. security..

A: You would have to randomize. You would do [El Gamal](https://en.wikipedia.org/wiki/ElGamal_signature_scheme) on top of that. We already know how to do that. Semantic security is the easy part.

Okay, cool. This is a really good discussion. So please work on this problem. I think it's really interesting and it would have a lot of consequences. Before we move on to consequeces, I want to acknowledge early work on pairings in crypto.

* [Miller 1986, weil pairing](https://crypto.stanford.edu/miller/)

* Menezes-Okamoto-Vanstone attack (IEEE '93) ("[Reducing elliptic curve logarithms to logarithms in a finite field](http://www.dima.unige.it/~morafe/MaterialeCTC/p80-menezes.pdf)")

* Joux (ANTS '00)

* Sakai-Ohgishi-Kasahara (SCIS '00)

* B-Franklin (Crypto '01)

... and many others since then.

I already told you about Miller's seminal work. Menezes-Okamoto-Vanstone was sort of the first application in terms of attacks. Joux came up with the first positive applications of pairing. There's an interesting story here that Antoinne tells me that, what he did is he basically came up with an implementation of the pairing, for the purpose of implementing this attack. The problem is, so, the best implementation up until that point took a couple of minutes to run. Joux came up with an implementation that runs blindingly fast. People said, well it's an attack, why do we care if it runs in minutes or seconds? It doesn't matter, it's an attack, and attacking something in minutes is just as good as in seconds. And he said fine, so here's a positive application, just so that he could get his paper published. So sometimes the fact that committees reject your paper, is actually inspiring new research. And then a team in Japan, Sakai-Ohgishi-Kasahara, who also did really nice early work on pairings, and then of course the work with Matt and so on. And of course many others since then.

# Applications

Now I want to switch gears. I don't have a lot of time. You have about half an hour. Oh, half an hour. Alright, I see. Well. I guess I'll stop when we all get tired. Or hopefully before.

Let's talk about some applications. Pairing is basically well as you know, thanks to all of and many of you, pairings are kind of everywhere. I started writing out all sorts of citations to lots of papers, and there's just no way to fit it all on a slide. When I say many contributors, that's many in this room and others. And pairings give us new forms of encryption.

Pairings everywhere:

* Encryption: [identity-based encryption](https://en.wikipedia.org/wiki/Identity-based_encryption) (IBE), (formula) [attribute-based encryption](https://en.wikipedia.org/wiki/Attribute-based_encryption) (ABE), (inner-product) predicate encryption, 1-somewhat homomorphic encryption (1-SWHE), short broadcast encryption, searchable encryption.

* New signatures: group signatures, ring signatures

* new NIZKs ([non-interactive zero-knowledge](https://en.wikipedia.org/wiki/Non-interactive_zero-knowledge_proof)), SNARGs (succint non-interactive arguments of knowledge), accumulators, see [1](https://diyhpl.us/wiki/transcripts/simons-institute/snarks-and-their-practical-applications/), [2](https://diyhpl.us/wiki/transcripts/simons-institute/a-wishlist-for-verifiable-computation/), [3](https://diyhpl.us/wiki/transcripts/simons-institute/zero-knowledge-probabilistic-proof-systems/), [4](http://diyhpl.us/~bryan/papers2/bitcoin/snarks/).

* adaptive [oblivious transfer](https://en.wikipedia.org/wiki/Oblivious_transfer)

* PRFs, VRFs, anonymous credential systems, [anonymous cash](https://github.com/scipr-lab/libsnark)

* and many more.

1-SWHE is encryption that allows us to do 1 multiplication and no more. It allows us to do broadcast encryption where the broadcast ciphertext is constant size, independent of the size of the set you're broadcasting to. We get new signature schemes, new SNARGs, new NIZKs, we get adaptive oblivious transfer which is a beautiful result due to Susan, we get PRFs, VRFs, etc... and many others. So basically, pairings have been, as you know, have been extremely productive in crypto.

This is what we could do with a 2-way multilinear map. A 3-way multilinear map doesn't seem to help us that much. Oddly, even though we don't know how to construct 3-way multilinear maps and it would be a good goal, a 3-way multilinear map by itself doesn't seem that useful. It goes... no-way linear map gives us diffie-hellman, 2-way multilinear map gives us IDE and all this other stuff, 3-way multilinear maps ... doesn't give us much, but many-way multilinear maps would give us the magic of obfuscation. So when you go to a many-way linear map, al of these things better, so attribute-based encryption would work for circuits not just for formulas, and predicate encryption becomes way stronger because you could get functional encryption. Of course, we get k-way homomorphic encryption, and we get even better broadcast encryption.

I just want to say in words what happens when you apply this to, what happens to this box here when you use LWE. It's a fantastic assumption, it's extremely productive as well. I love lattices. Wonderful results there. And so, in the world of LWE, again, attribute-based encryption becomes applicable to circuits. And even in stronger ways than we could do with multilinear maps. And predicate encryption I guess there's progress, but we're not quite there yet. And of course the killer app for LWE is fully homomorphic encryption (FHE), this is way better with LWE than with pairing. The one interesting thing is broadcast encryption; I would encourage forks to work on this. With pairings, we can get broadcast encryption where the size of the broadcast ciphertext is always constant size. You can broadcast to a large set of people, it doesn't matter how many people, the broadcast is always constant size. With LWE, we don't know how to do it, we have good candidates but we can't prove it's secure for LWE. If anyone is interested in thinking about broadcast encryption, I would be thrilled to send you our proposed construction.

Q: Maybe we should make it more variants...

A: The funny thing is that with a variant of LWE, we do actually know how to prove security, but that's not the LWE game. In the world of lattices, you're supposed to prove things from LWE. (laughter) I don't know, it's a rule I would like to follow. It would be nice to have just one assumption from which everything follows. This is also why I mentioned the decision linear assumption, because it's just one assumption from which everything else follows. If we start adding different assumptions to LWE, if we start making changes to LWE, it's a little disconcerting because many, because if you start making changes, then the assumptions break.

So anyway, if anyone is interested in broadcast encryption from LWE, I would love to send you some proposed candidates, maybe you could break them or prove security. But it is a bit of a gap. We can do this with pairings, but not with LWE, it's probably because well I don't know, nobody has it figured out yet, but it's probably doable.

Now that we have this list, I could obviously, I can't talk about all these applications. I figured I would talk about just one application that I like.

# Application of pairing to signatures

<https://www.youtube.com/watch?v=8WDOpzxpnTE&t=1h2m11s>

I'll talk about the application of pairing to signatures, and then we'll stop.

Q: You mentioned obfuscation as an application of multilinear maps.

A: Yes.

Q: What assumption do you need?

A: Oh. Really? Horrible assumption.. it has a name.. it's a... well, you know... what can I say. It's a complex assumption on multilinear maps that's needed for obfuscation. Hopefully this will get better over time. There's constant improvement in these constructions.

Q: ...

A: Well, it's an assumption, we can write it down, so it's already better than what we had initially, thanks to again, thanks to the obfuscation team. So that's where we are. Yes, exactly.

I just want to walk through one particular signature scheme and talk a little bit about its properties, and then we'll conclude. This is the simplest simplest application of pairings. If you hadn't seen pairings before, this is the easiest way to explain why pairings would be useful, so I hope this will be interesting to those of you who have not seen pairings before.

# BLS signatures and short signatures

see also <http://diyhpl.us/wiki/transcripts/2016-july-bitcoin-developers-miners-meeting/dan-boneh/> and <https://bitcoincore.org/logs/2016-05-zurich-meeting-notes.html>

These are called [BLS signatures](https://en.wikipedia.org/wiki/Boneh%E2%80%93Lynn%E2%80%93Shacham) (see also the [BLS paper](https://www.iacr.org/archive/asiacrypt2001/22480516.pdf)). This is a signature scheme that works as follows. We have our two groups, G1 and G2, I am using the asymmetric setting here. The public key and the secret key are simple. The secret key is some number alpha in the range 0 to q minus 1. So the public key is just g^alpha.  The exponent is the secret key. The way we sign, it's simple, we take our message, we hash it to a point in our base group here, and we raise the result to the alpha. Hash, and raise to the alpha, and that's our signature.

How do you verify a signature? The way you verify a signature is very simple. It basically requires two pairing operations. You pair the signature with one generator, and you pair the hash of the message using the public key, and you verify the two are equal. A bit of thought will show you that if the signature is valid, the signature is H(m)^alpha, and the public key is g^alpha, the alpha comes out of both sides, and you get something equal there. If the signature is invalid you will get an inequality. That's it, that's the whole signature scheme.

Key generation: output [g1, g2, pk=(g2)^alpha], sk <--- alpha

Sign(sk, m):  output  sigma <--- H(m)^alpha

Verify(pk, m, sigma):  accept iff e(H(m), pk) =? e(sigma, g2). And that's e(H(m), g2)^alpha.

Q: What... do you need ... G1 for?

A: This is the asymmetric version of BLS signatures. So G1 is the group of points over the base field. And G2 is the group of points over the extension field.

Q: ... target of the hash function... maps to G1..

A: I see what you're saying. Fine. Actually, it's used in the hash function, but implicitly. We'll leave it in there for completeness.

You can prove a theorem that says that under the [asymmetric computational diffie-hellman assumption (aCDH assumption)](https://en.wikipedia.org/wiki/XDH_assumption) in the [random oracle model (RO)](https://en.wikipedia.org/wiki/Random_oracle), this just comes up because of, we're using asymmetric pairings, then in fact the signature is existentially unforgeable in the random oracle model. So you need the hash function to be a random oracle, and you can argue that this is secure under aCDH. So it's really simple. It's the easiest way I know to explain the benefits of pairings. And, the only thing of course is that this is a signature scheme that can only be analyzed in the random oracle model.

What I would like to do is talk about very quickly three properties of this signature scheme. I think it's three properties that have not been utilized practically as much as they should, so I would like to point them out.

The first property is that the signature is really short. There's a beautiful open problem here that I want to mention. A signature is really just one group element in the group G1. A group element in principle can be quite short. Here I wrote down the signature sizes. Let me back up one sec. What we would like to have is have short signatures, which come up in a variety of contexts. At some point, I got an email from the South African DMV, where they were worried about car thefts, so they decided to print signatures on all of their license plates. And they tried various signatures, and there was literally no space on the license plates for a bar code for long signatures. So they googled "short signatures" and landed on my page, and then asked if they could use my signature scheme. So I said great, it's not patented; and there's a funny story there, and yes it's not patented, it's open for anyone to use. And so, that's one case, where you have no space, so you want a short signature. Another case where you want short signatures is where you have a human who has to type in a signature. This is often the case in digital rights management, like the secret code you type into something to activate software, it's critical there that the signature is as short as possible so that a human can actually type it.

How do we build short signatures? The particular problem is that you want a signature where the best known attack runs in time 2^lambda. What's the shortest possible signature we could have? So you want best attack to run in time 2^128. What's the shortest signature? Here I wrote down the signature size for various schemes.

<table>
<tr><td>algorithm</td><td>signature size</td><td>lambda=128</td></tr>
<tr><td>RSA</td><td>O(lambda^3)</td><td>2048 bits</td></tr>
<tr><td>ECDSA</td><td>4 lambda</td><td>512 bits</td></tr>
<tr><td>Schnorr</td><td>3 lambda</td><td>384 bits</td></tr>
<tr><td>BLS</td><td>2 lambda</td><td>256 bits</td></tr>
</table>

BLS, with one group element, the signature size is only 2 lambda, so 256 bits. Why is it 2 lambda? Why is not lambda? Square root attack on discrete log. So you want CDH in the group G to be hard. So there's always a square root attack on discrete group, so we have to double the size of the group to get the best attack to run in time 2 lambda, and that forces us to use 256 bits.

One property is that it's short. There's a beautiful open problem here, why are we stuck at 2 lambda? This has been driving me nuts for a long time. Why can't we get this 2 lambda to come down? Why not a lambda bit signature where the best attack runs in time 2^lambda? And again, there's beautiful work by Waters that shows that by using obfuscation, you can get a lambda-bit signature. It's simple, it's a puncturable MAC. But basically the way you sign is you compute a [MAC](https://en.wikipedia.org/wiki/Message_authentication_code) of the message, and the way you verify is you publish a public key, which is an obfuscation of the MAC verification algorithm. So the signature is always lambda bits, and it has security 2^lambda. Of course, with the current state of obfuscation, the South African government would have a little bit of trouble implementing this. It would take a while; car thiefs would get away with a car before they would be able to verify the signatures. And the car would be obsolete by the time verify the signatures. So again, it's an open problem, and I would encourage, I really like, I really hope someone could solve the problem. Could we have an implementable method? Could we, for example, could we have a lambda-way multilinear map? So a 128-way multilinear map, to get a lambda bit signature?

Q: If you just do, [birthday attack](https://en.wikipedia.org/wiki/Birthday_attack) on the hash function.

A: I didn't say it has to be hash signed.

Q: ...

A: We have a existence proof.

Q: If you want to sign arbitrary messages, you will need to hash.

A: The output of the hash doesn't need to be the size of the signature. You could hash, and the signature can be even shorter than the hash.

Q: .. using a signature.. you could give it a... and show how to get hash out of signature..

Q: No, but that's interesting.

A: Well, those are not short. In principle you don't need hashing for signatures. The fact that a hash has to be size 2 lambda is not necessarily an impediment.

So we know this is possible, we would like to be able to do this in a better way. It would be interesting if LWE could do something like this, although LWE signatures don't seem to be in this table anywhere, but again maybe over time, this is a wonderful question, could we build short signatures using LWE? That would be really nice.

Q: ... possible with lambda bits... so if you assume some completely insane assumptions...

A: All you need is iO.

Q: ... best attack 2 to the lambda..

A: Appropriate assumption on the iO scheme. Oh, I see what you mean. So remember, the signature scheme is basically a PRF of the message. As long as your PRF has security 2^lambda, which is fine, then your message will have security 2^lambda. The public key is an obfuscation of a PRF. So that security is kind of independent of the security of the signature scheme.

By the way, I'm surprised that nobody complained, the proof here is only selective security, but we don't care about that, because you can do complexity leveraging that only impacts the size of the public key, not the size of the signature. So in fact, you can, you might as well assume this is a fully secure scheme.

Q: Could you .. lambdas as well..

A: What lambdas? Oh, below lambda bits? No.

Q: ... lambda for... so.. for everything.. break down... smaller?

A: Anything below 2 lambda, I'll take even 1.999 lambda, 1.5 lambda, that would be pretty cool.

Q: .. you may not want 128-bit security.

A: Oh I see what you're saying. If you want lambda to equal 64, then this would be 128 bits for BLS. Well, you have an attack that runs on time 2^64, and at some point the scheme stops being secure at some point if you scale it down too far. No money here, but maybe you can get money from the South African government. This is a beautiful problem to solve, though.

# Signature aggregation

<https://www.youtube.com/watch?v=8WDOpzxpnTE&t=1h13m45s>

The second property is <a href="https://crypto.stanford.edu/~dabo/pubs/papers/aggreg.pdf">signature aggregation</a>. Anyone can compress n signatures into a single signature. It has, not only are BLS signatures, short signatures, but you can take many signatures and compress them into a single signature. This was a paper with Craig Gentry and Lynn and Shacham. You can take a whole bunch of signatures, produced by many different people, and compress them all into a single signature and this one signature in fact convinces the verifier that in fact for all i, user i signed message m sub i.

If you think of certificate chains, where the signatures in the chain are all these BLS signatures... today, these signatures, you have to list all the signatures in the chain. But using aggregation, you could compress them into a single signature and this would actually reduce traffic in [SSL](https://en.wikipedia.org/wiki/Transport_Layer_Security) but unfortunately this is not used today.

Q: Why?

A: I don't know.

Q: ...

A: Verifying them takes just a few milliseconds. So that's fine. And verification is done on the client. A few ms on the client is fine.

So why they're not used, I don't know, it's a real shame. The world would be a better place if they were in use. And similarly, by the way, in bitcoin. The way bitcoin works is that they generate a bunch of transactions, then those transactions become a block, then they generate another another block. Today, all of the signatures in those transactions have to be recorded because that's how bitcoin is transferred. You can reduce the size of the blockchain, at least the transactions on the blockchain, by aggregating all the signatures in a block into a single signature. As to why this is not used today, I think it's because people are not aware that this property exists.

Q: Can you take hashing... elliptic curve..

A: Yes, but that's quite easy. That's not a problem.

I'll just say quickly, how do you aggregate? You take all the signatures and multiply them together. If you do the math, you can verify the aggregate and everything just works.

user 1: pk1 = g^alpha\_1, m\_1 --> sigma\_1 = H(m\_1)^alpha\_n
user n: pkn = g^alpha\_n, m\_n --> sigma\_n = H(m\_n)^alpha\_n

sigma <--- sigma\_1 * sigma\_2 * ... * sigma\_n

<https://www.youtube.com/watch?v=8WDOpzxpnTE&t=1h16m>

And the last property I'll mention is that, in fact, it's really easy to thresholdize these signatures. If you think about how these signatures work, it's raising something to the power of alpha. Making it into a threshold signature is trivial, and similarly distributed key generation is trivial, there's really nothing to do. So it's like, both signature generation and key generation are very easy to distribute. It's easy to threshold RSA, but it's difficult to do distributed key generation. Schnorr and DSA has simple key generation, but complicated threshold signatures.

Another open question that I really like is regarding a simple LWE-based threshold signature [BKP'13]. For some reason, I don't know why, from LWE it's still really hard to do threshold signatures. For folks working in LWE, it would be really nice, it's kind of missing from LWE. We would like to get threshold signatures for large numbers of participants. When we do threshold signatures, we multiply partial signatures by binomial coefficients to do the interpolation, and this multiplication by binomial coefficients actually blows up the noise and it ruins what could be done by LWE. Chris has a paper he is working on this. It's no where near as simple as RSA or BLS. It's a problem driving me nuts. It would be really nice if we had a LWE-scheme where we had a threshold property as simple as RSA or BLS. Today, we don't know how to do it. LWE is a wonderful assumption and a beautiful thing to work with, but there's still basic things that we want to have, that we can't build from it. Simple as in precise. What I mean by simple, it just means that, the signer sends a message to a bunch of servers, each server can compute a signature on its own without interactivity to other servers, if enough servers respond, you combine them to get the signature. We don't know how to do that with LWE today. I think that's a gap in our LWE understanding, and I think it needs to be resolved. We need a new LWE-based signature, because the existing LWE signatures don't have that proprety. So we would need to invent a new one that has the threshold signature property.

Q: So non-threshold LWE signatures are possible?

A: Yes. Well, they are long, but they are very practical, yeah of course, absolutely. But when it comes to threshold... and by the way, the world needs threshold signatures. When you look at certificate authorities, they always store their keys in threshold manners, so we can't use LWE without threshold signatures in certificate authorities, it's kind of important.

Q: ...

A: No, even with random oracles we don't know how to do it. The only assumption that seems to help is iO. When we try to construct it, it looks like to actually consider the construction, we almost need obfuscation to make it work. So maybe there's some impossibility result there?

Q: Quantum signatures?

A: I don't know. It's an excellent question.

Q: Short one-time signatures?

A: You have to give a full... oh I see, for single-bit, it's easy. But for may bits. I don't know.

Q: How long is your message?

A: It's basically 2 lambda bits, say, the output of a hash function. That's it. It would be really nice.

Actually I think there might be some lower bounds on the length of quantum signatures. It's in the number of oracle queries, but it would be nice to extend that to length as well. I think there's a lot of work to do on short signatures.

Q: Oracle queries?

A: Oracle queries, if you're trying to prove it relative to an ideal function, the number of oracle queries you need for the ideal function. This is Luca's work. It bounds the time, not the size of the signature.

Q: ...

A: Oh, possam homond.. oh that's right, sorry.

Okay, I'm going to stop now. There are also ways to build signature schemes without random oracles. I am going to skip that, because I'm running out of time. And so, let me conclude just by, I really liked Amitz's last slide from his talk. I am going to steal his last slide, except I couldn't find the same graphics. So I had to use abstract graphics, which captures my inability to do art. So the summary of all this is that I think this is a really exciting time in crypto. I have been doing crypto now for a long time. I love this field, I love this community, the problems are fun to think about, the world cares about what we're doing, so I can't imagine having any other field to work in. It's a beautiful, wonderful area to be in. Over time, essentially our power has kind of grown. We started with one-way functions where we could do encryption signatures (OWF), then came [trap-door functions (TDF)](https://en.wikipedia.org/wiki/Trapdoor_function), [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)), discrete log, hard Dlog, and now we can use that for key exchange and public key encryption. Then came pairings, which allowed us to do new forms of encryption which we couldn't do before. With LWE, the killer app is [fully-homomorphic encryption](https://en.wikipedia.org/wiki/Homomorphic_encryption#Fully_homomorphic_encryption). So our power has been growing over time. The revolution we're seeing right now is multilinear maps, and of course the killer app is [indistinguishable obfuscation]( (iO), but there's a ton of things we're going to be able to do with multilinear maps. There's a lot to get out of those multilinear maps. The question I kind of have for you is, what's next? What other things do we have, that we want to build that we can't build today, and what are the tools that we will come up with? But with indistinguishable obfuscation, almost every problem I can think of is solvable with iO. So what's next? What is our legacy, what do we leave to our children? What are they going to be working on? So again I would challenge the community to help our children make sure we leave the same world that we live in for our children so that there's a hard challenge that we don't know how to solve so that they will invent the tools to solve that problem. And on that note, I will stop. Thank you very much.

<https://www.youtube.com/watch?v=8WDOpzxpnTE&t=1h23m26s>

We have time for a few more questions.

Q: Just a comment and a question. In the pairing world, computations are moving forward. You either have an exponent and you raise to an exponent, or you have two values... but in lattice crypto you move forward and sometimes backwards... do you think this accounts for things we can do versus things we can't do?

A: Oh, that's a philosophical question. Well, I think the way, the power from LWE comes from the fact that it sort of emulates a multilinear map. It's not exactly a multilinear map. You get somewhat like that behavior, and you see that in the ABE constructions from lattices, and you sort of, in ABE constructions, you can move from gate to gate, but you always stay in the same structure. So that's why you can keep applying with that, I mean the noise blows up, but ...

Q: But to generate keys,

A: But to generate keys, you have to go back. Right. So, it's kind of the best of both worlds, you get a pairing and a trap door. So maybe that's where the power of LWE comes from. Yeah, I don't know, every construction has its own beauty.

Q: ... stuck in the past still. These .. linear maps.. are much better. But I still worry, there's only one curve that everyone is using. For example, you can say the same, one prime for which we're doing discrete log, but there I would say use a bunch of primes, forget the efficiency, choose a large number of primes, small fraction will be hard, do a lot of them, do XOR, and just say..  but I would like to do something similar here... if you have a curve, is it distributed As and Bs, then there's a distribution of the orders... under the conjecture.... but here's there's only one curve?

A: Well there's another parameter here; you are free to choose other primes of course.

Q: Yes but once you choose a prime it's a problem, because the other group, the target group, ...

A: That also depends on the prime too.

Q: The same prime.

A: No, you choose a prime, you get a prime and a target group. You get a different curve.

Q: To fix the problem, you choose a prime at random, now oyu have a curve. So you want to see...

A: I understand the question. So first of all, in practice, you would not choose the y^2 - x^2 - x curve; you would use the asymmetric pairings, and with these asymmetric pairings there's a wide variety of curves you could use. It's not just curve. There's more variations in the family. The way to generate these curves is generate the curve and the prime at the same time. You can generate many curves and primes, and each time you get a different curve and a different prime. Now all these curves, all these pairs, you know, they give you different bilinear groups. So if you assume there's computational independence, you can amplify.

Q: ... gives me a non-negligble fraction of... and for which the diffie-h problem is hard.

A: So the assumption, which we know as far as we know is true, if you choose one pair of prime curve, and another one, there's no reduction between those two. It's possible one is easy and one is hard.

Q: ...

A: If there was a reduction, you could point to a hardest possible curve, that's true. But right now, it's exactly like RSA, you generate one RSA modulus, you generate another RSA modulus and there's no relationship between the problems on those modulus.

Q: ...

A: I'm saying the same thing. These are MNT curves. For every n. These are MNT curves, it's a family of curves, you can [generate MNT curves](https://eprint.iacr.org/2004/058.pdf), you press a button and it spits a pair, press the button again and it spits out another curve.

Q: There's an issue with the alphas... as you go to larger and larger primes...

A: The taxonoomy specifies it up to some sort of large alpha, and in our lifetime those are all the alphas that we would need, unless some kind of disaster happens. The generation problem is considered solved.

Q: ...

A: As alpha goes to infinity? It's not written anywhere, there's no reason why the taxonomy couldn't be extended to larger alpha, it's just not interesting.

Q: ...

A: Once you fix alpha, you can generate lots of bilinear curves. There's quite a bit of diversity. The family is called MNT curves.

Great, thanks a lot.

[Aggregate and verifiably encrypted signatures from bilinear maps](http://crypto.stanford.edu/~dabo/papers/aggreg.pdf)
