---
title: Comments and Observations about Timelocks and VDFs
transcript_by: Bryan Bishop
tags:
  - timelocks
speakers:
  - Ron Rivest
media: https://www.youtube.com/watch?v=NadhhH_eQBQ
---
## Introduction

Welcome everybody. It's not only about solving the puzzles, but the immense interest in verifiable delay functions. When setting up this conference, I hadn't expected that. It's hard to predict where technology will go or what things will be popular decades later when you work on something.

I am just going to review some of the basic stuff we did way back when, setting up a puzzle which was just recently solved by Simon and Bernard where's Bernard. Bernard first and then Simon and team second. And Juan is about ready to solve it too. I don't know who else is here solving it simultaneously but let's give them applause. Congratulations everybody.

## LCS35 timelock crypto puzzle

This started for us back in the 1990s. I'll talk about what we did and the puzzle we setup. We setup a timelock puzzle idea back in 1996 as Rivest-Shamir-Wagner puzzle design. In 1999, we had a party for the LCS 35th celebration. As part of that, we setup a timelock puzzle where the solution would be the key for opening the time capsule. We did that on Wednesday and opened the time capsule.

## Sequential computation

The question was about sequential computation. Can two women have a baby in 4.5 months? That joke didn't go over well on Wednesday. Can parallelism speed up the computation?

You need intrinisically sequential computations. This was the goal back in 1996. It was to design a computation that can't be sped up using vast parallelism. It's important that it can be created to require a certian chosen number of operations to solve (in series). You start at some point, you follow each nodes and get to the finish line. That was our goal.

## Timelock puzzle design

There are a number of ways to do this, like iterating a hash function, but if you use some algebra you get some other useful properties.

Unsurprisingly, we based it on the product of two primes p and q multiplied together defining the n value. The chosen t value is the number of operations required. You publish (n, t) as a puzzle description, and the puzzle is to compute 2^(2^(t)) (mod n). So you can do this by repeated squarings starting with 2 (mod n) and then the next a value is a^2 sub (i-1) times (mod n) for i equals 1 through t. The solution to the puzzle is a sub t. I don't see any way to short circuit that other than repeated squarings, or knowing the factorization.

## Embedding a message M

The puzzle reator knows prime factors (p, q). The puzzle creator can compute a sub t quickly. You publish C = M xor a sub t. The puzzle solver can compute a sub t (with t squarings) and then compute M = C xor a sub t. You can use this as a pseudo one-time pad.

## Birthday bash

So we had that party at LCS in April 12-13 1999. The Laboratory for Computer Science was created in 1963 as "Project MAC". The director was Mike Dertouzos (1974-2001).

One of the things that happened was that we had a time capsule we wanted to memorialize for the lab. The celebration featured a Gehry-designed "time capsule" with significant artifacts from LCS history, to be opened in "35 years". The capsule was to be opened when "time capsule crypto-puzzle" I supplied was solved. So I needed to create a "35-year puzzle"... So we tried, and we were within a factor of two.

## Creating a 35-year puzzle

How did we create the 35-year puzzle?

We measured how long squarings took. This was an iterated squaring problem. We measured, or estimated rather, 3000 squarings/second in 1999 using Java. We estimated Moore's law was 22%/year faster until 2012 (13x total), then 7.5%/year faster thereafter, providing 5x total speedup. Back in the 90s, Moore's law was still in full swing. That was our model of Moore's law, based on the semiconductor industry roadmaps. The total number of squarings would be 94.6 billion in the first year. And the total squarings required was about 80 trillion.

## Unlocking the timelock

We had the time capsule sealed by Bill Gates. We sealed up the capsule and then started the puzzle. Then, amazingly, last month or so, a solution was announced. It was surprising to me. I had no idea someone was working on this problem. Bernard did it first, and Simon was next.

Bernard Fabrot will talk about this on Wednesday. He took 3 years + 3 months of computation, using a software-based approach. He solved it on April 15, 2019 (exactly 20 years from LCS35th) and his email was sent on April 16, 2019.

The second solution was provided by an international group including Simon Peffers, Erdinc Ozturk, Justin Drake, Jeromy Johnson, and they put together a FPGA design which solved it on... they wrote the email on April 17th, which was one day after we received the email from Bernard. They solved it on May 10th, 2019. This took them 2 months of computation.

We have made a new puzzle this week, which has 2^56 squarings, and a 372-bit number. It was targeted for 50 years.
