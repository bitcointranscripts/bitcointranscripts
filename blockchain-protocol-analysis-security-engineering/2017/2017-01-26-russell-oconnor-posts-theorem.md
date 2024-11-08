---
title: 'Post’s Theorem and Blockchain Languages: A Short Course in the Theory of Computation'
transcript_by: Michael Folkson
speakers:
  - Russell O’Connor
tags:
  - cryptography
date: 2017-01-26
media: https://www.youtube.com/watch?v=TGE6jrVmt_I
---
## Intro

Hi. My name is Russell O’Connor. I am here to talk to you about Post’s theorem, the theory of computation and its applications to blockchain languages. There is a bit of a debate about whether Turing complete languages are appropriate or not for doing computations, whether the DAO fiasco is related to the Turing completeness problem or is it an unrelated issue? If we do go for non-Turing complete languages for our blockchains how much expressiveness are we losing? If we go back into the history of the theory of computation we can answer at least some of these questions. That theory was mostly worked out in the 1930s and 1940s. We have a lot of history that we know about. We can bring it to bear on the question. However I think the essence of the problem was best illustrated from a possibly forgotten scene from The Matrix movie that you might not quite remember.

Morpheus was talking with Neo and he asks “Neo what is the most expressive type of language possible for a blockchain?” To which Neo responded “Clearly Turing complete languages are the most expressive possible. Every computer scientist knows this.” He works as a SWE in that big grey building. He is not wrong when he says this. But then Morpheus asks “What if I told you that you could design a language that was just as expressive and guaranteed termination?” So Neo asks “What are you trying to tell me? That I can execute arbitrary computation?” And Morpheus replies “No Neo, I’m trying to tell you that when the time comes you won’t have to.” I think it is in the outtakes or something.

## Blockchain Programs

A very quick review of what is going on. I want to be very abstract here, I don’t want to talk about specific blockchains that necessarily exist, just the abstract idea that is compatible with most blockchains out there. What you have is some sort of global blockchain state. In Bitcoin it is the UTXO set. In another blockchain it could be more complicated. You have transactions that are coming in and they are producing updates to that global blockchain state. We have consensus rules that decide which transactions are valid in a particular blockchain state. Then we have miners that are competing to sequence these transactions. That is a very high level view of what is going on with most blockchains.

Blockchain programs let users build smart contracts by providing controls for them to decide programmatically which transactions are going to be valid.

Very abstractly what we are looking at is that a blockchain program defines a predicate and that predicate has to be satisfied for the entire transaction to be accepted. There might be other rules on top of that but this is the part that the users get to programmatically control. That predicate is some function of the state and the transaction that they are trying to apply to that state. The predicate returns TRUE or FALSE depending on whether that transaction is going to be allowed for the purposes of the program. A little aside over here, these predicates can be as expressive as functions. Another way you might want to think about things is that rather than having predicates you have a function that takes some input and the current state of the blockchain and produces the transaction. You might think this is an alternative model but we can incorporate this into the predicate model. As long as we combine the inputs with the transactions and put them together into one object then we can just have a predicate that takes our global state, extracts the input from the transaction, runs our function F on it which produces some transaction output. Then we compare that to the transaction that is being passed to the predicate. If they are equal then we have satisfied it. This predicate expresses exactly the same transaction the functional version is trying to do and we can even do vice versa. They are equally as expressive. I am going to be looking at the predicate perspective over here without loss of generality.

## Theory of Computation

To understand what is the class of predicates we can define programmatically what we do is we turn to the theory of computation.

We define computable functions as partial functions on the natural numbers that can be defined by a Turing machine or can be defined by a lambda calculus term or can be defined by general recursion. The big result of the theory of computation is that all these three models produce exactly the same answer for what the computable functions are. That is how we have come to accept this definition. Whilst the logicians and mathematicians use the natural numbers N for their predicates you guys should just think blob of data when you see the natural numbers. All data can be encoded as a natural number. The logicians and mathematicians don’t care about particulars of the data so they just work with the natural numbers. Any time you see this funny looking N just think blob of data. These functions are partial functions of course because our computations might not terminate. We might not produce an output from our Turing machine or lambda calculus term.

What we do is we define computably enumerable predicates as those predicates over the natural numbers or over blobs of data, that are the domain of some computable function. The inputs for which some computable function will halt.

These C.E. predicates, these computably enumerable predicates are the broadest class of predicates that we can define programmatically. This class of predicates was completely characterized by Post using logic and the Arithmetic Hierarchy. Just to show you how broad this class of C.E. predicates are, if you have a traditional characteristic function, some function that is returning TRUE or FALSE we can turn this into a C.E. predicate just by taking that function as a subroutine. Calling it, if it returns TRUE our machine halts, if it returns FALSE we just go into an infinite loop. Now we have made a function whose domain is equal to the characteristic function we passed in. The C.E. predicates are the broadest class of predicates that we can programmatically define.

## C.E. Predicates and the Arithmetic Hierarchy

Let’s talk about the arithmetic hierarchy.

## First Order Logic

Now we have to take off our computer scientist hat and put on our logician hat, do a quick review of formal logic, first order logic. It will be very fast. Thinking way back to maybe your undergrad days what is first order logic? We have these atomic formulas, they are made of variables and constants like zero and one. We have plus and times for arithmetic. We have an equality predicate relation and an inequality relation and those form our atomic formulas.

Building on top of these atomic formulas that are doing arithmetic operations we have connectives like AND for conjunction or OR for disjunction, implication and negation. We have those logical propositional connectives to form more complicated propositions. Then we have quantifiers which give us predicates. I am going to take an unusual step of separating between bound and unbound quantifiers. We define bound quantifiers as our existential, there exists some x less than some term t such that p holds. Or for all x which is less than some term t, p holds. Those are bound. Then we have also the unbound quantifiers which range over all the natural numbers, all data. There exists some natural number x such that p holds. Or for all x p holds. Those are how we define formulas in first order logic. If you do formal reasoning you will get very familiar with this sort of stuff.

## Arithmetic Hierarchy

The arithmetic hierarchy is defined as ways of classifying these different types of formulas. A delta_0 formula which is right at the bottom at the arithmetic hierarchy. Those are these arithmetic formulas that have no unbound quantifier. Every quantifier you see is bound. For all x less than something there exists y less than something for example. This is an example of a delta_0 formula.

A sigma_1 formula, those are the form where you have an existential unbound quantifier. There exists some x over the natural numbers such that p holds where p is a delta_0 formula. I give an example below. A pi_1 formula is of the form for all n over the natural numbers one unbound universal quantifier p holds where p is a delta_0 formula. It has no further unbound quantifiers. I give an example there. The hierarchy continues above there where we start alternating our universal existential quantifiers. We don’t need for the purposes of this talk to go any higher than this level in the arithmetic hierarchy.

We say a predicate is sigma_1 if it is definable by some sigma_1 formula. That sigma_1 formula will have one free variable which corresponds to the variable that the predicate is being performed over. Similarly we define a pi_1 predicate to be those that are definable by some sort of pi_1 formula.

This is Post’s theorem. It says that P is a computably enumerable predicate if and only if P is a sigma_1 predicate. These computably enumerable predicates are exactly the class of predicates that we can define programmatically and we can completely characterize them in terms of this arithmetic hierarchy as a logical proposition. Every one is of the form of a sigma_1 predicate and every sigma_1 predicate is computably enumerable.

## Post’s Theorem

So what does Post’s Theorem for our blockchain languages over here? Because our blockchain language only implements computably enumerable predicates we now know that every blockchain program is equivalent to some sigma_1 predicate. Whatever program you write it is of the form “There exists x of type natural number such that Q(x,s,t), state s, transaction t, holds where Q is a delta_zero predicate.” All P can do is search for some data x which we call a witness that satisfies our delta_zero predicate Q. No matter how fancy your little Javascript program is from the logician’s point of view all you are doing is a search for some piece of data x, the witness that satisfies some delta_0 predicate Q.

## The Key Idea

This is the key idea of the talk. This is exactly where the important thing happens. Rather than having everyone on your network do the search for that witness all you have to do is provide that witness as part of the transaction, provide it as part of the input. We make a new predicate P_0 which takes the witness x as its input and it passes it directly to Q. The point now is that P_0 is a delta_0 predicate and evaluation of delta_0 predicates always terminate because all the quantifiers are bounded. And we have lost no expressivity here. P_0 and our original predicate P are basically operationally equivalent in what they are expressing. The only difference is that rather than having everyone do the search for the witness we provide the witness upfront. We are able to use a language which always terminates, it must not be Turing complete, but we haven’t lost any expressivity in what we are able to encode with it.

## Recap

Here is the recap. Turing complete languages can only define computably enumerable predicates. Post’s Theorem tells us that computably enumerable predicates are identical to the sigma_1 predicates in the arithmetic hierarchy. Validating a sigma_1 predicate can be reduced to validating a delta_0 predicate as long as you provide a witness. Evaluating a delta_0 predicate always terminates.

## What is the witness?

What exactly is this witness blob of data that Post’s Theorem is saying we are going to be quantifying over? What is it that we are searching for?

Post’s Theorem directly doesn’t tell us exactly what is the meaning of this witness. There are a number of choices that we have of interpreting what that witness is. Here are two extreme examples of what that choice could be.

## Gas-based witness

We can have a gas based witness. This witness is a natural number which is the number of steps that the Turing machine takes to run. Our program Q is basically the same as program P except it always halts after x number of steps.

Technically Q is a decidable predicate because it always terminates after x steps but we haven’t really gained much by doing this. For instance the best bounds we can have on memory use is x times the maximum allocation of memory per step if you give this some sort of maximum memory that you can allocate in each step of your execution. Or you can copy unbounded amounts of data in each step of your Turing machine, then exponential is the best bounds that you can get by analyzing your program. Technically we can do some analysis. Technically we have avoided the undecidability consequences of Rice’s Theorem which tells us that we can’t decide almost any problem about Turing complete languages. But we haven’t done it any practical way because we still have this exponential search space over here.

## Trace-based witness

The alternative, the other side of the extreme spectrum here of what the witness is, is we could have a trace based witness. Here the witness, the natural number which if you remember is a blob of data, this data encodes a sequence of all the intermediate states that your original program P executed. Then your program Q is a program that just checks each intermediate state follows from the previous one according to the program.

In this case evaluation of Q is usually linear in the size of the witness. It typically runs in constant space, it depends on the exact details. Interestingly it can be run in parallel. For all these intermediate states because we have listed everything, we can consume that entire witness in parallel, checking even intermediately whether some little state S_1 goes to little state S_2. These can all be checked independently of each other that lets you massively parallelize the problem. However, of course the witness is going to be very large and it is going to have a bunch of redundant data in it. So it might not  really be that practical.

## Blockchain Language Design

So probably the best solutions lies somewhere between these two extremes. I like to point out that your favorite Turing complete language doesn’t look like our sigma_1 formulas. So when we write our blockchain language to express delta_0 formulas its syntax is also not going to look like this arithmetic formulation. It is just going to be something that is equivalent to it. I don’t know really how best to design a language for delta_0 programming languages. But I think we should be looking in that location when we are building our languages for blockchains.

One possible design is something where we have a simple bounded language and this lets users decide how to mix performing computations with validating trace data. If we aim for this design for blockchain languages we can have a simpler language for blockchain programming that only has bounded loops which simplifies the consensus critical portion of the blockchain. When you have trace based computation validation you can prune off untaken branches. Because they are not executed they don’t appear in the trace and you don’t even have to reveal those branches that you don’t take during execution. This helps for privacy. And you don’t need to do searches, for loops that search for some value. You can simply provide the answer to the search for every existential that you encounter during validation and put it in the witness. We get low computational complexity of evaluation. This allows us to bound the amount of computational resources we need just by analyzing the size of the witness. This helps mitigate some risk of denial of service attacks.

## Hashtag Post’s Theorem

So this is the conclusion slide here. You can tweet this to all your followers. That everyone has been talking about sigma_1 when they should be talking about delta_0. \#PostsTheorem \#ArithmeticHierarchy. Thank you.

## Q&A

Q - You mentioned trade-offs but we already have a perfect solution with recursive SNARKs. You get constant time, constant space and on top of that you have privacy.

A - Yes. SNARKs is the perfect solution (joke).

Q - I am reminded of Necula and Lee’s proof-carrying code where they essentially provide both a program and a proof that certain properties hold over that program. Checking the two in conjunction is a trivial operation. They typically do things like for example for looping programs you provide the fixed point. You avoid the need to analyze the program. It seems like what you have described here is analogous and/or isomorphic?

A - I think it is still quite different. The attitude here I want to convey is that the big difference between the sigma_1 perspective and the delta_0 perspective is that with the sigma_1 perspective what you think of is that I am going to write a program and everyone on the blockchain is going to execute this program. Everyone will do the same thing because they are running it in the same environment. This would apply to the proof-carrying code idea as well. With delta_0 thinking what you think is I am going to run the program myself on my computer and I am going to generate some witness data. I am going to have everyone only validate that witness data instead of running the entire program. That is a change of attitude and I think it will influence how you will design your blockchain languages when you think of your problem this way. Rather than distributing the computing and having everyone run your program, have you the person making the transaction run the program and produce the witness. Then you need to automatically be able to both generate the program that generates the witness and the program that validates the witness from the same source code. Then you distribute that validating program to your blockchain and have everyone validate the witness over there. That can potentially be a lot more efficient, a lot more private, save a lot of time. You could argue that SNARKs are an implementation of this taken to the extreme.

Q - Is the evaluation program an example of delta_0? Is it turtles all the way down basically? Is there a limit to the evaluation program and how much computation it can do?

A - For the witness validation program, this delta_0 thing, it is limited. The witness has to be long enough in a certain sense to allow it to churn through the computation. The longer your computation is the larger your witness becomes. You get to keep your low complexity validation delta_0 program because it consumes this witness data in order to do the validation. The amount of its runtime is going to be bounded maybe linearly or at least as a function of the size of that witness data. You know that witness is going to terminate because you have a finite amount of witness data. If you had an infinite amount of witness data it would run forever but no one is going to accept that on your blockchain.

