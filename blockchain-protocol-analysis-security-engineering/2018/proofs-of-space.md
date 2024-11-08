---
title: Beyond Hellman’s Time-Memory Trade-Offs with Applications to Proofs of Space
transcript_by: Bryan Bishop
tags:
  - research
speakers:
  - Bram Cohen
date: 2018-01-31
media: https://www.youtube.com/watch?v=iqxkO7C-cyk
---
Beyond Hellman's time-memory trade-offs with applications to proofs of space

<https://twitter.com/kanzure/status/962378701278208000>

# Introductions

Hi everyone. This presentation is based off of a paper called "<a href="https://eprint.iacr.org/2017/893.pdf">Beyond Hellman's time-memory trade-offs</a>". I'll get to why it's called that. These slides and the proofs are by Hamza Abusalah.

# Outline

I am going to describe what proofs of space are. I'll give some previous constructions and information about them. I'll give a simple new construction which has lots of advantages to it.

# Proofs of space

The concepts of proofs of space comes from 2015 (<a href="https://eprint.iacr.org/2013/796.pdf">Dziembowski-Faust-Kolmogorov-Pietrzak 2015</a>). The idea is that there's some parameter N which is your amount of space. You have a verifier and a prover. The prover has some amount of storage capacity and some amount of CPU. The verifier wishes to be assured by the prover that they are in fact using a certain amount of space. Ideally, what you want is for the verifier to have I am just going to say "order" of these things listed-- which is ignoring, polylog factors.. Which is to, have about order 1 communications to the prover in a challenge. The prover then uses N space and O(1) computation. The verifier uses O(1) computation to verify the response that the prover gave.

Now, you can have an attacker (the purple bird on the slide) who is misbehaving. They have the potential to instead of using S space to use T time of the same amount as S. An important point here is that the bad prover might actually use S space but do so very transiently so the amortized amount of space they are using is nothing. The important point is that the prover has these two choices. They can either use S space or they can use T time. T is going to be basically the same as S.

# Known proofs of space

* Dziembowski-Faust-Kolmogorov-Pietrzak 2015
* <a href="https://eprint.iacr.org/2016/333.pdf">Ren-Devadas 2016</a>

There's a good one from 2015 based on graph pebbling. That one is asymptotically optimal using either N space or space-time during the execution. It is unfortunately a complex construction that cannot be made fully non-interactive when used in blockchains, which proves to be a really serious problem because in blockchains you want people to be able to join without any preparation. The proof relies on some idealized assumptions.

# This work

This work is going to be introducing a new proof-of-space based on inverting random functions. It's much simpler and easier to explain than the older ones. The proof holds unconditionally in the random oracle model. It's some nice solid proofs here.

The disadvantage is that it's asymptotically less optimal. It still has some potential tradeoffs, but we think they are good enough that in practice that everyone just honestly uses the amount of space they are supposed to.

# Towards a simple construction

If we're going to go over simple ways of doing proofs of space, the very simplest one is where the verifier makes a random table and communicates the entire random table to the prover and then after that setup is done the verifier then sends an index into the table to the prover and the prover responds with that entry into the table. This clearly works.

The problems are that it has ridiculous amounts of communication complexity, and it's very space-inefficient on the verifier side.

So a simpler construction is that the verifier picks a random function pi which you can use a secure hash function in practice, and sends that to the prover, the prover generates the table, the verifier then picks an index again, and the prover sends the inverse. This sounds very intuitively compelling, unfortunately it's busted because <a href="http://www-ee.stanford.edu/~hellman/publications/36.pdf">Hellman 1980</a> found an attack where the prover can use square root of N space and square root of N time which is entirely practical for them to pull off. The approach to doing this is that you repeatedly find the function on N. if it's a permutation, then when you repeatedly find the function, on average half of the things will be in one single giant gigantic cycle. There are little tricks to avoid the problems that not everything is in the giant loop, I'll gloss over that for now, I'll pretend like if you find pi of N that it forms a single loop of everything; the prover actually runs this through this entire thing and they store a square root of N of these and they remember what order they are in as they go around. The prover remembers some of these, and remembers that the next one to come up after... but they don't remember the steps in the middle because that's the square root of N factor they are saving on their space.

Say the verifier challenges the prover to invert x3 in this example. The prover then repeatedly hashes x3, and they come across x4 in this example that happens immediately, then they go okay I need to step back to x1, then they walk forward from x1 until they hit x3 again, and now they go oh well I've now inverted x3. And so this only took them square root of N space and time. It turns out that you have a pretty nice sliding scale of these kinds of attacks you can do, and the invariant is the space times the time is limited by N the amount of space you're supposed to be doing honestly. At an extrema, T is 1, and S is the actual amount of space you should be doing, but you have these tradeoffs you can make.

It's been proven that there aren't  better tradeoffs than that that an attacker can do.

# Inverting functions

* <a href="https://dl.acm.org/citation.cfm?id=100226">Yao 1990</a>
* <a href="https://eprint.iacr.org/2000/017.pdf">Gennaro Trevisan 2000</a>
* <a href="https://eprint.iacr.org/2005/001.pdf">Wee 2005</a>
* <a href="http://ttic.uchicago.edu/~madhurt/Papers/dtt-new.pdf">De Trevisan Tulsiani 2010</a> (<a href="http://ttic.uchicago.edu/~madhurt/Talks/owf-talk.pdf">slides</a>)

So the... prove enloyments... are if, if you have a permutation you're using for this, you have this pretty tight S times T is bounded by N and the optimal values for the attackers here are setting S and T to be the same and that ends up being the square root of N. For random functions, the best known upper and lower bounds aren't as tight, but there's an N^(2/3) limit that is known and actual one is probably a bit higher. The general functions around here are weird, if things have too many collisions in too weird of a way, then these repeated hashing things don't work, but we have no idea how to generate something that behaves in those obnoxious ways or what it might look like, so it's somewhat academic, but the limits on that are better.

We actually have an improvement on this. Our functions are-- you pick a k, and that winds up being limited by N^(k/(k+1)) so it can get arbitrarily close to N and approaching it very rapidly in practice because you get pretty big constant factors here and the kth root of N gets pretty small pretty fast.

How is this possible? I just said it's been proven that you can't do better on some of these things, right? Well, we're using a loophole.

# Two observations

The loophole is that for Hellman's attack to work, the function needs to be easy to evaluate in the forward direction. Most of the obvious approaches do in fact make the function easy to evaluate in the forward direction. To be useful for proofs-of-space, you don't actually need that. All that you need for proofs-of-space is that it is sufficient for the function table as a whole is computable in linear time. You can have some kind of construction where you compute the function table in one fell swoop but you can't piecemeal compute each individual thing inside of it. This is a subtle and important observation that we can exploit.

# Our function

Let's say that we have a permutation F and a function G which takes two things in N and outputs one thing in N. It's just hashing them together, say. And then we have a function gamma which is an involution without fixed points, so we're flipping all bits for example or flipping the last bit it doesn't really matter which one it is.

We're going to define a function gf of x, which is g of x and x prime such that gamma(f(x)) is equal to f(x prime). Or we could say, gf(x) is this other way of expressing the same thing.

We can prove that if an attacker has S bits of advice and makes up to T queries to f and g and succeeds in inverting gf with some probability, then we have this limit on how good the attacker can be. There's a caveat: this only holds for T up to N^(2/3). There's going to be weird discontuinities shown in graphs later which raises interesting questions about what the real curve is like.

# Function inversion for proof-of-space

This is what on a log scale what ST = N looks like. The black curve is the idealized perfect solution. This is what it looks like for k = 2.  This is for three, which doesn't matter, it's another thing.

# Proof methodology: A compression argument

Our proofs here are going to be first we're going to prove the ST = N for the simple approach that is somewhat busted but we can still say something about it. That's the old proof. Then we're going to be a bit more clever to prove the gf(x) results.

This is based on a compression argument. The idea is that our function table is incompressible. So we're going to prove that if you start with your entire function table and then we have some, if we have an attacker that can perform something then they can compress it, compress our function table down to some smaller size, and then be able to re-expand it to the full compression table, which implies that the attacker must have the appropriate--- if this is the case, if P is delta less than the size of f, and f is incompressible, then it means that the amount of advice bits that the attacker has must be at least delta.

# Lower bounds for random permutations

In order to do this, we're going to say that we're going to use the attacker as an oracle. We're going to start with 1, then do f(1) and f(f(1)) oh sorry we're going to say that we want to invert 1, and this is going to take up to T queries, so we assume the attacker does a whole bunch of queries, we're going to write down all the queries that the attacker did, and at some point they are actually going to ask for the thing that is the thing that one inverts, and now we're going to compress this and say that this thing is 1. We don't have to express that full thing. Now we're going to move on to the next thing, we skip over the queries that the attacker already made, we start with 4 here, and so on, and this is going to be at least N/T invocations because you're not making more than T queries each time. We as part of our encoding we have to copy all of our answers to these things verbaitm, we can compress down these ones, and because we pulled out N/T bits this means S * T has to be greater than or equal to N and we have proven the limit that we wanted in the first place.

# Compressing gf

If we're doing it for gf(x) then we do a slightly more complicated thing that is really in two places. Either, the attacker makes less than square root of T queries, or greater than square root of T queries. In practice, the attacker might mix and match it, and not do the same thing every single time. The full proof is more complicated.

If they make less than square root of T queries, we can make the same argument that we made before, just on compressing g using ST >= N. And if they make greater than the square root of T queries then because-- every time they do an x and x prime, we can compress the x prime by saying that's the same as the x that we said before but flipped and this ends up hitting the same limit.

# Proof-of-space based on gf

In practice, the way that you actually implement this is that the verifier and the prover-- the verifier communicates gf and gamma to the prover. The prover then makes their function table so first they do a pass of finding all of their f values and then they pair up the things that are in pairs of gamma from each other and then they take the g of those two things and then they sort by that so that was a linear time log n in order for them to do because it was just sorting... and then the verifier sends an index to the prover that they want, and the prover responds with the appropriate x and x prime such that g(x, x prime) is y. And there's a specific construction for that.

This new construction is much more practical and simple than the older ones and it has nice things on it. The k can be increased by doing this iterative labor, g on top of g on top of g.

That's it.

# Q&A

Q: f is random permutation. what is g?

A: g is a random function on two values in the domain. You just hash them together basically.
