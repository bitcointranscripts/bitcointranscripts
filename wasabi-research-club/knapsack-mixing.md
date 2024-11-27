---
title: Knapsack Mixing
transcript_by: markon1-a via review.btctranscripts.com
media: https://www.youtube.com/watch?v=XDCQI7hrB58
tags:
  - research
  - coinjoin
speakers:
  - Aviv Milner
  - Felix Maurer
  - Lucas Ontivero
  - Adam Fiscor
date: 2020-01-06
summary: |-
  In this video, the participants of the Wasabi Research Club discuss the concept of knapsack mixing and its potential for privacy in Bitcoin transactions. They explain the process of merging inputs and outputs to create sub-transactions, and how different versions of the knapsack mixing algorithm have improved over time. However, they acknowledge that perfect anonymity is difficult to achieve and there are computational complexities involved. They also discuss the challenges of handling transaction fees and the difficulty of implementing efficient algorithms for finding all possible mappings and partitions. Overall, the speaker believes that knapsack mixing has the potential for anonymity but more research and testing is needed.
  Furthermore, they discuss various aspects of knapsack mixing, including the potential benefits and limitations. They explore the possibility of combining multiple inputs in a transaction and its impact on privacy. The necessity of calculating mappings in Wasabi is also debated, with the suggestion that it could help identify bottlenecks in blockchain analysis companies. The participants discuss the idea of setting a lower bound for the number of participants and outputs in a transaction to ensure computational privacy. Additionally, they consider the possibility of allowing non-mixing participants to participate in Wasabi transactions for stronger privacy. The conversation then shifts to the concept of users participating in knapsack-type coin joints for spending purposes only, which could be offered as a separate service in Wasabi. They also touch upon topics like blockchain with lists of inputs and outputs, determining conjoined transactions, RBF in transactions, and feedback for improving future episodes of the club. Overall, the participants engage in an informative discussion on knapsack mixing and its implications.
aliases:
  - /wasabi/research-club/knapsack-mixing/
---
Aviv Milner: 00:00:00

So we're talking about knapsack coinjoins today.
I'm just going to run through this slide and then hopefully Felix will jump in to clarify questions as they come or if I make a mistake.

## Anonymous Coin Join Transactions with Arbitrary Values (2017)

Aviv Milner: 00:00:15

So yeah, this is the paper, Anonymous Conjoin Transaction with Arbitrary Values.
We have one of the authors with us.
This PowerPoint will be made available if anyone wants it.
Very straightforward.

## The privacy problem with Bitcoin

Aviv Milner: 00:00:31

So what's the problem in Bitcoin?
Transactions are public.
Transactions point to previous transactions in a sort of directed acyclic graph and transactions can leak future spending.
That's the problem.
We're trying to obfuscate the transaction graph.

## Idea #1 - Joining Transactions

Aviv Milner: 00:00:48

So a simple idea from 2013 or even earlier is just joining transactions.
So suppose you have two transactions on the left here.
We have two transactions with two inputs and two outputs.
One output is likely sending money somewhere and another output is change.
What we could simply do is we could take transactions and we could just essentially collapse them together.
So there's nothing in Bitcoin that bars us from doing this currently at the moment.
So how does this look like?
On our left we have two unique transactions by two individuals and I've highlighted in red the output that likely represents sending funds to a third party or to someone else.
And on the right, what we do is we just take those inputs and outputs and we merge them into a single transaction.
Now when we look at this from the outside we have to ask ourselves is it possible to unravel the two sub transactions we merged together.
So we can start by taking an output like this one here, valued at 50, and we could try to find inputs that exactly match the value of the sum of the outputs.
So in this case, we try these two and it turns out there's no way we could come up with an output on the right that would match the two inputs on the left.
And we try again and we find that yes, actually we can break this transaction down into two pieces once again because we see that the bottom two inputs and the bottom two outputs equal exactly 64 and the top two inputs and two outputs exactly equal 33.
We're excluding transaction fees in this model for simplicity.
And so essentially what happens is we take this single transaction and we split it into two once again and we're left with the same privacy that we would have had before we did any of this joining.
So this isn't very good.
So most of the time we'll be able to unravel these transactions.

## Formal Definitions

Aviv Milner: 00:03:14

So If we look at the work done in this paper, what they've done is they've formalized some basic ideas.
So transactions have inputs, outputs, and values.
Inputs, we have the input set, the output set, and then we have coins, which belong either to the inputs or the outputs.
And then a very basic rule which is that the sum of the inputs must equal the sum of the outputs for any subset that we create.
So a coin-join transaction consists of sub-transactions, and there must be at least one way of partitioning all inputs and outputs so that each subset of inputs has exactly one corresponding subset of outputs with which it forms a sub-transaction.
And essentially what this means is that if we take a transaction, we must be able to cut it up in such a way, just like we did before, where a subset of the inputs matches some subset of the outputs in terms of value.
And we call this a mapping as it maps inputs to outputs.
So we have a set of all partitions denoted phi of a set, and then the set of all inputs, set of all outputs, and then set of all mappings is big M.
And essentially the set of all mappings below here is just the set of all, I think it's bijective mappings of inputs to outputs of the superset, such that the sum of the inputs equals the sum of the outputs.
So again, this is just saying that we can take a transaction and create a list of all possible ways we could cut it up, essentially figuring out different ways we could get sub-transactions, and the entire list of all ways we could cut it up is denoted in M.
I hope I haven't lost anyone so far, but good idea to maybe pause and ask, have I lost anyone so far?

Adam Fiscor: 00:05:12

No, I think it's a great introduction.
I just want to say for some administration that since Felix appeared in this conversation, welcome Felix, he is one of the authors of the paper and I think after your presentation we could move on to pick his brain and in order to not waste his time too much and then after that we can move on to other people's presentations and ideas and discussions about that.

Aviv Milner: 00:05:48

Yeah so this is pretty much almost over I think we're probably two thirds of the way through so we'll be able to ask Felix questions directly.

## In simpler terms

Aviv Milner: 00:06:00

So yeah now moving on to results so yeah in simpler terms we want to be able to break down transactions into sub-transactions, a combination of inputs and outputs.
In the paper, they clarify between derived and non-derived sub-transactions.
What that means is that a non-derived sub-transaction is a sub-transaction that isn't composed of smaller sub-transactions inside of it, and we're only concerned with non-derived sub-transactions for simplicity.

## Anonymity in this framework

Aviv Milner: 00:06:35

So the way that we look at anonymity or privacy in this model is we essentially take a transaction which has all these inputs and outputs.
And it has all these mappings, all the possible ways we could cut up the transaction.
And we essentially say that a specific coin on the left-hand side and any other coin on the right-hand side or on the left-hand side is linked to that coin in a probabilistic way depending on how many mappings, of the total mappings there are, how many of them include the two coins being in the same sub-transaction.
So I think there's probably an easier way to think about this.
Here it is formalized in the paper, but intuitively it makes a lot of sense.
And I think we'll see an example of it in just the next slide.
But that's the idea, it's a probabilistic framework.
So in this case here, if we go back and recreate what we did, and we split these up into two sub-transactions, we would say that, for example, output 3 is directly linked to input 3 with 100% probability, because there's only one way to partition this coinjoin.
And output 3 appears with input 3 100% of the time.
And we'll see later how that can be done differently.

## Evaluation of Joined Transactions

Aviv Milner: 00:08:06

So in the paper, they essentially create a bunch of random transactions and then essentially purposefully combine them together, and then observe the time it takes to recreate the sub-transactions from the coupled transactions.
So here we see that in the orange, if you have five sub-transactions with four inputs each, that takes about a second for a computer to be able to unravel that coinjoining to its relevant sub-transactions.
And then we notice here that the number of non-derived mappings isn't very high, even as there are as many as four or five sub-transactions because, like we did in the first example, we can typically unravel coinjoins and have very little overlap in terms of other ways we could map inputs and outputs.
So in here we see that only with 6 sub-transactions and 4 inputs per sub-transaction do we see more than just a few non-derived mappings.

## Idea #2 - Knapsack Mixing

Aviv Milner: 00:09:40

So there's a solution to this problem because right now what we see is that it doesn't take a lot of time to unpack these coinjoins and when you do there are very few non-derived mappings which means there's very little ambiguity in terms of what's linked.
So could we increase this?
Well, you know, here's knapsack mixing.
The idea is how to optimize filling a knapsack with various things of different weights.
In this case, we're trying to optimize the way to have outputs that they fill given inputs.
So the algorithm is pretty simple.
The idea is to compare the two output sets and to essentially try to break down one of the outputs so that one of the values of the output is the difference between the two sets.
So in this case, the number 31 is the difference between the green and the orange.
And so here we've done it with, you can see that we've split up the 50 into 31 and 19, and on the right we've recombined them to make a single coinjoint transaction and now when we try to figure out the sub-transactions we actually get two sub transactions.
We get this one here which connects the two on the left with the three on the right, but we also get this sub-transaction here.
And so the result is that if you asked, for example, is O1 linked with I3, the answer is that there's a 50-50 chance that O1 and I3 are linked because of the two sub-transactions that we have, in half of them O1 and I3 are not linked and the other half they are.
To have a probability of one to be matched with another input or another output?

Felix Maurer: 00:12:52

Yeah, right.
So the left graph shows the number of pairs of inputs and outputs that are linked with probability one.
And the right one shows the number of input-input pairs that are linked with a probability of one, always depending on which Knapsack mixing algorithm you've used.
So I think in the paper, I had two different versions of the Knapsack mixing algorithm, one which I called input mixing and one output mixing.
And I think I even hinted at a third one that I came up with later in the time when I was writing the paper.
So this one even improved over what you see in the graph so far.

Aviv Milner: 00:13:40

Okay, well very cool.
So I think the important thing to note here is that we still have a problem where some inputs are connected with other inputs and some inputs are connected with other outputs.
We have some coins that are achieving no additional anonymity except for the computational complexity that it takes to unravel the coinjoin.
So that's pretty much the end here.
There's some anonymity here in the computational complexity that's required to figure out how to break down these coinjoins, especially if we start talking about 10 participants, 30 participants, 50 participants.
There's still a link between inputs and outputs.
The entire sub-transaction partition must be known in order to apply the algorithm.
This is the most important trade-off I think, is that currently from what I've read it seems that this can't be done in a trustless way where someone isn't coordinating all the transactions.

Felix Maurer: 00:14:53

Yeah, and that's exactly the third algorithm I came up with.
I will have to read my own work again to understand what I did because it's two years now that I was working on it.
But I had a third version of the algorithm which was working without knowing all the outputs.
So everybody needs to know all the inputs, but each participant only needs to know his own outputs.

## Concluding Thoughts

Aviv Milner: 00:15:22

Okay, so everybody just needs to know all the inputs.
Okay, so interesting.
So upper bound anonymity, it's like, if we look at this way of looking at transaction anonymity and we apply it to ZeroLink, we see that ZeroLink is like a perfect knapsack coinjoin.
So that sort of provides us the upper bound anonymity, which is essentially the number of total participants that are doing this knapsack coinjoin.

Adam Fiscor: 00:16:01

I don't agree with a lot of things here, and I think this is your last slide.
So can we come back to it later and discuss everything, every concluding thoughts, one by one?

Aviv Milner: 00:16:16

Sure, sure.
So yeah, I'll leave it to Felix, because that's pretty much it for introducing the paper.

Adam Fiscor: 00:16:28

Yeah, so thank you, Aviv.
It's a nice introduction to get everyone catch up with the paper and we can go into the details here and there.
I was thinking that if Felix appears, then we would start with some questions to Felix and then if anyone has some small presentations then we would continue with those and then we would end up with discussions, questions, what did we not understood in the paper.
Although this could be bring here right now because Felix is still here.
So and we would finally discuss some things like if you have any ideas that came to your mind with this paper.
And then we would end with deciding on what should be the next paper on next week.
So, let's start with some more fun things.
Felix, I would like to know what was the story behind the Knapsack paper?
How did you come work on it?
And yeah, can you tell us about it?

Felix Maurer: 00:18:02

Yeah, of course.
Actually, it started as my master thesis.
So more or less, when the most of the content of the paper is also my master thesis, I omitted more of the related work, which was also a big part of my thesis.
And some of the results have not been part of my thesis, but more or less the idea and the general, most of the work is basically my master thesis.
So after I finished the thesis, I wrote a paper based on it.
And I think the one interesting thing is also that the term Knapsack for this mixing is not my idea.
I picked up the idea from two papers, which basically in one or two sentences describe that something like this could be done but did not really go into it.
So yeah, this is how I came up with this idea or why I started working on this idea.

Adam Fiscor: 00:19:18

Nice, and did you follow up on things, writing the paper or what did you move on to?

Felix Maurer: 00:19:27

No, actually, after my thesis I started doing a PhD at the RWTH in Aachen but after after one year I realized that it's not the right environment for me so I moved on and I'm now working at Fraunhofer Institute, which is not at all related to what I've done before.
So unfortunately, since two years, I am not working on the topic at all anymore.

Adam Fiscor: 00:19:59

I see anyone has any general questions?
I have more more in topic questions now.

Lucas Ontivero: 00:20:10

Hi, well I would like to know about the test, the validation of this hypothesis, if you have published the source code for this paper?

Adam Fiscor: 00:20:28

That would be my question too.

Felix Maurer: 00:20:31

Yes, actually I have.
I have published the code that I was used to produce the results of the paper.
I'm not sure if it's linked anywhere, but it's a public repository on GitLab.
Let me paste the link for you.

Adam Fiscor: 00:20:54

Thank you.
It's great, thank you.
Most of the difficulties I encountered is the deciphering the pseudocode.

Felix Maurer: 00:21:08

Yeah, no, I was just looking into the code, everything's there.
It's written in Rust, I don't know if you have experience with Rust, but it should be readable for anybody who is used to imperative languages.
I think the interesting part is in the main source folder, the `distribution.rs` file.
In there are the different mixing algorithms that I used.

Adam Fiscor: 00:21:46

Yeah, thank you.
Lucas here wrote code for it too, and actually I wrote code for it too.

Felix Maurer: 00:21:54

Yeah, perfect.

Adam Fiscor: 00:21:57

So we can validate.
I have one last question that only you can answer is that on the paper at the end you wrote that however currently our output splitting algorithm requires knowledge of all sub-transactions.
Using it in a peer-to-peer network would likely leak information to all participants.
We are already researching a new output splitting algorithm that mitigates this problem.

Felix Maurer: 00:22:31

Yes, this is exactly the third mixing algorithm that I developed at the end of writing the paper.
So it is not part of the paper anymore.
Unfortunately, it was finished shortly after the paper.
Let me see.
It's in the code.
It's this line.
Basically, the idea is that you broadcast to all participants all the inputs, but you can also do that in a fashion that you don't know which input belongs to which participant.
And then you can split your own outputs based on the all the inputs that you've seen without telling anybody all the outputs.

Lucas Ontivero: 00:23:32

Yeah sorry, where are you sharing the links?

Felix Maurer: 00:23:36

In the Hangouts chat.

Adam Fiscor: 00:23:40

I saved them.

Lucas Ontivero: 00:23:43

Okay, thank you.

Adam Fiscor: 00:23:47

So that was all my questions that only Felix could answer.
Anyone has any questions to Felix?

Lucas Ontivero: 00:24:01

Yeah, well.
Okay, I go again.
About the two things.
First, I was playing with this concept for a while and what I do is I sort the outputs descending by amount.
It's just a special case, right?
And I used two outputs, one is the payment, another is the change.
I realized that in this scheme, with this modification, well I don't know if it is with this modification only, but it creates for example 1.5 outputs for each original output.
For example, if I have a two participant coinjoin with four outputs, it creates six outputs.
If I have three participants with 2 outputs, I mean 6 outputs in total, it creates 9 outputs.
I don't know if you have some comments about this, but I want to know how many participants are in that conjoin.
Is it that I'm doing something wrong or it's just because I'm sorting the outputs?
Or, well, I can answer my question just by coding a bit more, but I don't know if it's something that you can share with us about that.

Felix Maurer: 00:25:57

No, that's actually an aspect that I didn't look into.
One other aspect that I did not look into is answering the question whether looking at multiple Knapsack mixed coin transactions would allow you to then again establish stronger links between inputs and outputs.
So this is something I would look into.

Lucas Ontivero: 00:26:31

Okay, and my second question is about the fee, because in the paper you don't analyze the fee, you say basically that the fee adds some kind of noise, right?
So you cannot match the partitions by equality because the sum of the inputs and the sum of the outputs are not equal, so it will be a bit harder to find the sub-transactions.
But I was playing with this concept and I don't know if you have some idea about what's the best way to handle the fee because if the participants use the same fee rate that is for example pretty common in Wasabi, right?

Felix Maurer: 00:27:32

No.

Lucas Ontivero: 00:27:33

No?

Felix Maurer: 00:27:37

I was actually trying to create transactions, this analysis on Wasabi transactions, and it's really bad because we can go up to 1% plus mining fees and this unreliability makes it really interesting.

Lucas Ontivero: 00:28:04

Well, yes, what I mean is that if the coordinator, one coordinator that is coordinating this knapsack transaction, right?
If everybody uses the same fee rate, even the inputs are bigger than the outputs, so they pay more fee.
If they pay proportional to their transactions, I can find the the sub-transactions, the partitions and check if the fee paid matches the sum transaction or not.
So it is a strong clue for the chain analyzer.
So do you have, Felix, any idea how to handle this?
What can we do?
Any idea?

Felix Maurer: 00:29:23

Actually, no.
To analyze it, I implemented an algorithm which enumerates all the possible subsets of the inputs and outputs and tries to match them.
So yeah, I think, I don't remember how I did it, but I sped it up with a Bloom filter.
And I realized that implementing a fast algorithm should probably intuitively be more difficult if the sums did not match.
So my thinking was that maybe it does not make the mathematical problem harder, but it makes it much harder to implement an efficient algorithm to actually find all the possible mappings or the possible partitions.

Lucas Ontivero: 00:30:20

Yes, that's clear, because I'm suffering with that problem.
It is hard to match in a range, right?
If it is more or less this value, so yes, it's a pain in the ass, but...
You cannot use a Bloom filter, of course, so you have to keep it in memory, which is even worse.
But the question was about how can we make the participants pay a fee in such a way that it doesn't provide additional information to the chain analyzers?

Felix Maurer: 00:31:20

I'm not sure whether it actually provides additional information.
I would have to think about it because it would only provide more information if it would help you distinguish between subsets that are more likely the real or mappings that are more likely the real mappings than others, right?

Adam Fiscor: 00:31:45

Yeah, I agree with that.
It doesn't provide additional information.
It makes it even harder to do the analysis.
And I did the analysis with the precision and the only real difficulty with the tunnel is this is how do you set the precision and what I realized for normal coinjoins you can set the precision as the mining fee because the mining fees the maximum amount one participant can pay.
With JoinMarket transactions, it's mining fee plus a random, I don't know what it should be, random whatever the JoinMarket transaction agreement was on the fees that the taker pays for the makers.
On Wasabi it's a mining fee plus 1% and that produces a bunch of unreliability, of course.
So, yeah, I don't see how it would provide more information.

Lucas Ontivero: 00:33:03

No, it does, it provides more information.
In fact, I mean, if you for example, you know that the feed rate is, I don't know, 1, yes?
And you have all the set partition.

Adam Fiscor: 00:33:17

Oh no, explain it.
What does it mean one?

Lucas Ontivero: 00:33:21

Okay, one satoshi per byte.
If the fee rate is one satoshi per byte, for example, and you see that you can take all the partitions, right?
And say, okay, the sum of these inputs, minus the sum of these outputs gives you the fee, right?
So, that fee, given the size of the transaction, you know how much it paid.
What is the fee rate?

Adam Fiscor: 00:34:05

You don't know who paid the fee.
There are many participants.
It could be that only one participant paid the fee.
It could be that all of them paid together.

Lucas Ontivero: 00:34:18

Yes, well, in that case, if only one pay the fee, yes, it makes sense, but in that case also is a problem because you can say, if it match exactly, then this is one of those that didn't pay any fee.

Adam Fiscor: 00:34:38

You may say exactly but I don't understand.

Lucas Ontivero: 00:34:42

If the sum of the input and the sum of the outputs is exact.

Adam Fiscor: 00:34:46

Then you can say that this participant did not pay anything.
Why would you say that?
There are many other sub-mappings that could be possible, even if you found one that all the duff like that, if you find other mappings that those are just as likely as that your first impression.

Felix Maurer: 00:35:15

I think I understand what you mean, Lucas.
So if all the participants pay exactly the same fee, and we have one mapping where all the input and the difference between the inputs and the outputs exactly matches this fee.
Then we would assume that this must be the true mapping.
But I'm not sure whether there would only be one such mapping.

Lucas Ontivero: 00:35:46

Well, yes, but in the in the runs that I made I found a lot of mappings, but some mappings have only two inputs, right?
And other mappings have six inputs, yes?
But if I know that they pay 1 satoshi per byte and the fee paid was x, I don't know, so I can know which of those mappings is the real one because one will be paying exactly one satoshi per byte and the other one will be paying a lot less because they have a lot more inputs.
So, it is a bigger sub-transaction.
So, I know that sub-transaction cannot be the real one because it's paying less than the expected fee.

Felix Maurer: 00:36:49

So you mean when you have multiple mappings and then the difference between the inputs and outputs of sub transactions should be proportional to the number of inputs and outputs and then you would know that is likely the mapping

Lucas Ontivero: 00:37:09

Yes, exactly

Felix Maurer: 00:37:16

Yeah, obviously I have to add this is more or less an empirical analysis.
It's not really a mathematical proof of this concept.
So I think the idea is really good and I think it would work combined because of the reason that it's likely infeasible to find out which mapping is correct.
And also difficult to actually find the mappings once the transactions get big enough, but it's not provably correct or provably anonymous in a more strict sense, I guess.

Lucas Ontivero: 00:38:13

One more question, I'm curious.
Your analysis, how many sub-transactions, inputs, outputs did you use?
I mean, did you try with a bigger number of participants, with more inputs and more outputs than those in the paper?

Felix Maurer: 00:38:40

Actually, no.
And the reason was that the time it took to find the mappings would just grow too much.
And it didn't run on my workstation.
I had a bit bigger server with lots of RAM and multiple cores, I think 64 cores.
Now, obviously, you could have a really much bigger computer or server or server farm.
But yeah, for us, it was really the case that it became just too difficult to find all the, or not difficult, but it took too much time to find all the mappings.

Lucas Ontivero: 00:39:29

Yes, I know, I tried with eight sub-transactions and it was running all the day and didn't finish.
So I canceled the process.
Yeah, okay. Thank you.

Felix Maurer: 00:39:50

And if my analysis of the theoretical complexity is not completely wrong, then I think the computing time it takes, depending on the inputs and output really increases by a lot when you increase the inputs and outputs.
I have it here, but it's not written down in an easy way.
I think two to the power of n times m which n is that assess n.

Adam Fiscor: 00:40:32

Are you talking about the van number or your lower bound estimation?

Felix Maurer: 00:40:40

My lower bound estimation.

Adam Fiscor: 00:40:47

I think it makes sense what I've read on the internet, on Wikipedia, that the best algorithms known for solving subset sum is still exponential.

Felix Maurer: 00:41:07

Yeah, so I think, the sizes of this mixed transactions in the paper I think should be only in an academical setting.
If you can automate it, and the idea was, you can join an arbitrary transactions because the sum or the value of the inputs doesn't matter.
It doesn't need to be a fixed amount for each input.
Then you can create for each transaction that you do, you can create with other peers for each transaction such a coin transaction of a huge size if enough people use the same wallet at the same time.

Adam Fiscor: 00:42:01

Since we are going into it, I'd like to say an idea of mine that one of the most frequent question in Wasabi was that why do we have the 100 anonymity set and like that.
But and the reason is because I sent out emails and that seemed like the consensus that okay that should be fine, 100 participants, but your lower bound estimation could actually give us a mathematic formula to set a minimum participants, right, for any coinjoins.
Okay, you kind of need at least this many participants in order to reach this computational hardness in deciphering the coinjoins.
Does that make sense guys?

Felix Maurer: 00:43:07

I think the theoretical bound is difficult to translate in and concrete amount of time it needs to find the partitioning.
But it's only really good for explaining how fast it gets more complex or how fast the time increases that you need to find a partition depending on the number of people who participate?

Adam Fiscor: 00:43:42

Yes, it's not a perfect fit but the main problem is that there must be a number chosen of what's the minimum number of participants that we want to do and that's why I thought this formula, your lower bound estimation would be actually somewhat useful in deciding on that number that we kind of choose, let's say arbitrarily or with educated guesses, I don't know.

Felix Maurer: 00:44:19

Yes, I guess you could, based on the time it takes for some simple examples, you could extrapolate using that function for more complex cases where more participants with more inputs to take part.

Adam Fiscor: 00:44:36

All right.

Lucas Ontivero: 00:44:39

One more thing.
I remember in the paper you said that if you spend one of those outputs in another knapsack transactio, the problem of finding all the mappings across a chain of knapsack transactions, the difficulty also increases similar to the process of mining a chain of blocks, right?
Do you have any additional numbers about that?
Because I agree intuitively that that is true.
But do you have any numbers about that?
Have you tried that?

Felix Maurer: 00:45:44

No, sorry, that's something I didn't try.
And I'd like to add that intuitively, I think that the difficulty or the problem would be that if enough people would use this kind of transactions, and you would have a continuous flow of these transactions, which could create kind of a backlog of coinjoin transactions that you need to find the mappings for, which is what I mean in the complexity increases when you use it continuously.
On the other hand, linking, for example, two outputs together could actually be more easy if they both appear again as inputs in the next coinjoin transactions.
That is one of the open questions, one of the open problems.

Lucas Ontivero: 00:46:45

Okay, thank you.

Adam Fiscor: 00:46:51

Anyone would like to chime in who did not talk yet?

Rafael: 00:47:02

I only have a couple of basic, maybe a little bit stupid questions, but are you guys intending this knapsack coinjoin as a method of like payment for like straight up to for the, for example on some service or it is like basic coinjoin like it's the output will come to me the both outputs.

Aviv Milner: 00:47:43

[inaudbile] coinjoin for payments, whereas ZeroLink currently does coinjoins as mixing transactions.
This is actually the question I wanted to ask Felix was, if he knows anything about how Wasabi currently works and, the distinction between a coinjoin for mixing and a coinjoin for sending.
And I feel like having read this paper, I feel like Wasabi being able to send in a coinjoin might open doors for more privacy.

Felix Maurer: 00:48:19

Yeah, to be honest, I didn't know about Wasabi until now because I really I'm not keeping up with the current developments on Bitcoin anymore or other cryptocurrencies.
But yeah, my idea was that actually, that's the point of the Knapsack mixing, that you can use coinjoin transactions for actually performing the transactions that you want to do, and not only for anonymizing coins.
So you can in the same step, send coins to a third party and do the mixing.

Rafael: 00:49:01

Okay, thanks.

Lucas Ontivero: 00:49:08

One comment.
It is easy for us if we one day decide to implement something like this.
It is easy because if you mix to yourself, you can generate all the addresses that you need because you know your keys, right?
And you can generate your own keys, as many as you want.
But for payments, you need to be able to generate addresses for someone else.
Many addresses, probably by sure more than the payment and the change.
You need to be able to generate more addresses.
So, it is not hard to do, I think, but it is something that is not so easy with the existing culture, let's say.
Because if I want to pay you, Aviv, I ask you for one address.
Imagine I say, okay, Aviv, I want to pay you.
Send me 10 of your addresses.
It is unusual, right?
So we need something different.

Adam Fiscor: 00:50:20

Yes, I agree.
There are solutions for that, like stat addresses or give me your Onion address, and we could maybe work it out, but it's a lot of work.
Yes.
However, maybe it's possible to do a variation of knapsack where you kind of keep the payment as it is, but you are only mixing on the changes.
It should be an easier thing.

Felix Maurer: 00:51:05

Actually, I'm quite sure I've read about special kinds of Bitcoin addresses where you can for the receiver of the transaction generate as many addresses as you want, I don't remember how it was.
It was kind of like a public private key scheme where you can generate new addresses and only the receiver is able to use these addresses.
I guess the only remaining problem would be for the receiver to notice transactions which contain addresses that belong to him.
But I will try to find out what they were called.

Adam Fiscor: 00:51:47

I know too, both of them have some very serious trade-offs.
Say if it's one of them.
If it's not, then I would like to investigate.
One is stealth addresses, you were actually mentioning that in the paper, and the other one is payment codes.
Is it one of it?

Felix Maurer: 00:52:12

I'm not sure.
I thought it was something with blind signatures.

Adam Fiscor: 00:52:17

That would be actually awesome.

Felix Maurer: 00:52:22

Maybe I'm remembering something wrong, but I can try to look it up and try to find what I was reading.
But I thought that that might not be a problem.

Adam Fiscor: 00:52:41

Yes, it's a problem.
And anyway, I just like to say that I would really like to make these as a learning conversations and not necessarily how to integrate it or implement it into Wasabi or how to do anything with Wasabi.
Because there are like 600 more papers that I want to review and maybe at the end when we learn about everything, then we can come up with something, then we can use different techniques from different papers.
What my thinking is right now, is that it's just a vague idea, but if we could give a number to, hey, we mix this way and this mix is this efficient.
If we could scale the efficiency of the mix, if we could tell how efficient one mix is, then we could come up with a bunch of mixing solutions and we would know that, hey, this mixing solution gives the best blockchain space per anonymity gained number, right?
And what would be the anonymity gained?
What is this Knapsack paper is doing pretty well that it is...
I was always thinking about just breaking the link with how much anonymity set, but this Knapsack paper pointed me that, hey, you actually can break the link between the inputs, you can break the link between the outputs, and of course you can break the link between inputs and outputs.
So that makes the anonymity gained metric much better.
So that's great.
All right, do you guys have any presentations?
Who has presentations here?

Felix Maurer: 00:55:24

So, I guess at that point I'm going to leave because it's already quite late here.
The address in the paper is not a valid email address anymore.
I don't receive emails on that address anymore.
But if you have any questions, you can contact me at any time.
I send you my new email address in the chat.
So feel free to ask me if you have any more questions.

Adam Fiscor: 00:55:50

Yeah, thanks a lot for coming.
It was a pleasure to...

Felix Maurer: 00:55:55

Yeah, thanks for having me.
It's always nice to see that you've done something interesting.

Lucas Ontivero: 00:56:07

Yes, I'm a big fan of your work.

Felix Maurer: 00:56:10

Thanks.
So thanks and goodbye, maybe until some time later.

Adam Fiscor: 00:56:19

All right, bye bye.

Lucas Ontivero: 00:56:22

Yeah, I was thinking about, could you, Aviv, show your presentation again?

Aviv Milner: 00:56:28

Yeah, just give me one quick sec here.

Speaker 4: 00:56:30

Yeah.

Aviv Milner: 00:56:41

Did you have a slide in mind?

Lucas Ontivero: 00:56:43

Yeah.
Could you go on the one where is the inputs and outputs?
Like, yeah, for example, this case, what determines the actual numbers of the outputs?
Let's say that if this wasn't for payments where there is an exact number or some required, what determines these outputs or the value of them?

Aviv Milner: 00:57:08

Yeah, so the idea is you would get a more efficient knapsack mix if you just allowed for infinite outputs, because they would get very small and then it would take more time to compute, but there's the trade-off that you don't want to have lots of outputs so the simple knapsack idea here was just take regular transactions that have no special features and for every two transactions take the larger one, the one with the larger output and break down a large output into two parts where in this case the number 31 is the difference between the green and the orange brown values.
So in this knapsack method, you only add one output for every two transactions that combine.

Lucas Ontivero: 00:58:08

Yeah, okay.

Lucas Ontivero: 00:58:11

I'm back.

Adam Fiscor: 00:58:15

Yeah, you can go ahead with us.

Lucas Ontivero: 00:58:20

Yeah, yes.
Sorry, I lost connection.
Okay, what I want to show you is the difficulty with the free [inaudbile].

Adam Fiscor: 00:59:02

I don't know if it's going to work (referring to other speaker's connection issues).

Rafael: 00:59:24

Okay, well, just going back to the Aviv's presentation thing.
I was just thinking about, if it wasn't for payments, and there would be like any kind of set amount that you would have to reach on as output.
I understand that we wouldn't like to use too many or break it down into too many UTXOs.
But in some sense, I think it could kind of work.
I'm not sure if it's just too expensive or something for after why it's like combining all these UTXOs or something like that, but, like breaking it down onto the smallest possible input that there is.
And, not maybe like, like the smallest one, but, just breaking it down into a smaller and exact the same outputs, like you could combine many inputs and the fee would go like a static, depending on how many inputs you're putting.
And then it would just, give you either like, for example, a bigger sum or a smaller sum.
They could be like different kind of knapsacks, coinjoins.
I'm not sure if I'm explaining this correctly.
Did you guys get any of that?

Aviv Milner: 01:00:55

I think I understand what you're saying.
There's some problems with that idea as well.
I mean, inefficiency is one of them.
But another issue that I see with these knapsack examples is we don't think about how transactions look like over a longer period of time.
So for example, let's say you have many, many, many change outputs.
If you decide to then spend many of these change outputs together in a transaction down the road, it undoes all of the privacy gains from the knapsack for the most part.
So I think those are one concern.
Is there something else you wanted to say?

Rafael: 01:01:44

Yeah, I'm not sure.
I mean I just thought about this thing right now.
So maybe I have to just sit down and think about a little bit more before I try to verbalize it.
But well, another thing was that about the mappings and the computation of that, I mean, is that actually necessary for Wasabi to do?
Or is it like, just beneficial thing if it would take too much time for actually go down on all these mappings?
I mean, let's say that there would be like, let's say, five participants, which all are putting like three different inputs.
And yeah, for example, getting that well, X amount of outputs.
I'm not sure if it's only a good thing if the mapping is hard to calculate.

Adam Fiscor: 01:02:47

Mapping is not necessary to do in order to build a system.
What's interesting about calculating these mappings is that we can actually see that where are the bottlenecks of blockchain analysis companies so that's that's why I am interested in calculating the mappings.

Rafael: 01:03:15

Yeah that's what I was thinking also I mean if we could just use it as a benefit.

Lucas Ontivero: 01:03:23

Yeah, for example, the idea that I said before that Felix actually estimated the lower bound for the subset sum analysis here.
And we could say that, hey, okay, we need at least this many inputs and outputs.
And if 10, I think 10 is pretty, let's say if 10 inputs and outputs are present, then that already provides computational privacy.
So we could set a lower bound for, okay, yeah, we want to target 10 as the minimum number of participants or something like that.
So, that's an interesting idea, yes.

Aviv Milner: 01:04:21

Adam, can I add something before I have to run here?
Right now we've split the mixing and the sending as two separate features, but it seems like privacy would be much stronger if people that weren't doing mixing could still participate in a Wasabi transaction.
It's just something that I thought about.

Adam Fiscor: 01:05:06

I'm not sure I understand.
Sorry.

Aviv Milner: 01:05:09

Yeah.
I mean, so, why...

Rafael: 01:05:18

That there will be like more people linked to the coinjoins, even if they don't actually use Wasabi.

Aviv Milner: 01:05:31

Yeah, what I mean to say is that what if a user just wanted to send someone money and essentially wanted to participate in these knapsack type coinjoins for spending?
Then that could be a separate service that could be added to Wasabi.
Like, imagine if the entire blockchain didn't have transactions, but just had lists of inputs and outputs.
I think we can agree that it would be computationally very hard for people to successfully unravel the entire block of inputs and outputs.
So I think that's sort of what I was thinking about.

Adam Fiscor: 01:06:23

Yeah, yes, of course.
Even if you don't do any mixing, right?
More problems there are with, let's say, how do you get all the participants of a block agree on the fee?
It raises more questions than it answers, I think.

Lucas Ontivero: 01:07:00

One more thing, the knapsack transactions...

## Deciding Next Meeting's topic

Adam Fiscor: 01:07:06

Lucas, because Aviv is leaving, before Aviv leaves, can we decide on what should be our next...
What should be next Monday.
What should we look into?
You guys have ideas?

Lucas Ontivero: 01:07:25

No. Coinshuffle?

Adam Fiscor: 01:07:33

All right, coinshuffle, one idea.

Aviv Milner: 01:07:41

There are some papers that were cited by Felix's paper that I thought were interesting but I think coinshuffle was one of them.

Adam Fiscor: 01:07:59

There is also [coinjoin Sudoku](https://github.com/kristovatlas/coinjoin-sudoku) from kristovatlas, de-anonymizing all the blockchain.info SharedCoincoinjoins that I had in mind.
Also, secure multiparty computation, which came up in the paper, but I've seen that came up so many times in so many papers in the coinshuffle paper too by the way that I'm just as interested what the heck that would be.
So anyway any more ideas or decide on these three now?
Or vote, let's vote for these three.
Or something else in the mix, do you want to add?

Lucas Ontivero: 01:09:04

I prefer Coinshuffle and there is another variant, I don't remember this, it is Coinshuffle++ or something like that.

Adam Fiscor: 01:09:15

There is coinshuffle, there is coinshuffle++ and there is valueshuffle, which is Coinshuffle++ with confidential transactions.
So anyway, let's go from left to right.
Aviv, coinshuffle, coinjoinsudoku, secure multi-party computation?

Aviv Milner: 01:09:39

I guess I'll vote for coinShuffle.

Adam Fiscor: 01:09:43

Okay, Lucas, CoinShuffle.
Igor?

Lucas Ontivero: 01:09:48

Probably yes.
Also coinjoinsudoku, but I think it's pretty much the same that we have discussed today, finding the partitions.
So I don't know if it brings something new to us.

Adam Fiscor: 01:10:06

Yeah, that was kind of my idea there, that we could look at someone else's work on the same topic that's actually a part of the knapsack paper and we could compare that.
There is also Snicker.

Lucas Ontivero: 01:10:32

Snicker too, yeah Snicker can be too.
Probably Snicker is better than coinshuffle because coinshuffle has some communication schemes that is pretty hard.
I don't know if it can be implemented really.

Adam Fiscor: 01:10:52

Okay, let's start it again then and I will note how much are the votes and let's get over with.
So, Coinshuffle is from Tim Ruffing and it's about mixing transactions.
It's similar to ZeroLink in that sense.
CoinJoin Sudoku is from Kristov Atlas and it is how do you de-anonymize coinjoins.
I think it's solving the subset sum problem somehow.
This is a smaller thing.
Secure multiparty computation.
I have no idea what is this but I think it's something that will come back because it came back many times.
Snicker is from Adam Gibson and this is some interesting idea to do coinjoins.
Okay, Aviv, coinshuffle, coinjoinssudoku, secure multiparty computation, Snicker, you can vote for multiple things.

Aviv Milner: 01:12:02

I think the coinshuffle or the Snicker would be interesting.

Adam Fiscor: 01:12:06

Okay, coinshuffle one vote, Snicker one vote.
Lucas?

Lucas Ontivero: 01:12:12

The Snicker.

Adam Fiscor: 01:12:14

Only Snicker?

Lucas Ontivero: 01:12:42
Yes.

Adam Fiscor: 01:12:45

Igor?
(Igor doesn't respond)
I cannot hear you.
Couldn't hear anything.

Aviv Milner: 01:13:03

I'm going to head out.
I trust your judgment to vote and I'll read whatever is submitted for next week.

Lucas Ontivero: 01:13:15

Perfect. See you Aviv, thank you.

Unknown Speaker 1: 01:13:19

Cheers, thanks.

Rafael: 01:13:20

Thanks, and awesome presentation.

Aviv Milner: 01:13:24

Thanks guys.

Lucas Ontivero: 01:13:26

Thank you.
All right, who would you like to keep your [inaudible]?

Unknown Speaker 1: 01:13:38

I would dive more deeper into what Adam Gibson does on this topic, because I know the man and yeah, I'm really curious what he's doing especially with regards to what you guys are researching.

Lucas Ontivero: 01:13:53

All right.
Rafael?

Rafael: 01:14:01

Yeah, I like the idea of shuffle and Snickers.

Unknown Speaker 1: 01:14:06

Everyone is hungry probably.

Adam Fiscor: 01:14:12

Yahya?
Yahya, are you with us?
Okay, I see what you wrote.
You're not familiar with any of it.
All right.
Well, it doesn't really matter what I wrote.
It's going to be Snicker.
Because that has four votes.
Okay, so it's going to be Snicker, the next next meeting, and Lucas you were saying something that I disrupted you so go ahead.

Lucas Ontivero: 01:14:50

Yes, just a comment that those knapsack transactions for an observer, an external observer, It is not easy to realize it is a conjoined, because I mean it can be a batch transaction, a pay-to-many transaction.
I mean in the blockchain there are lots and lots and lots of transactions with more than, I don't know, 5 inputs and 10 outputs that are not conjoined, right?
So, It is not easy to know that that's a conjoint transaction.
So there is not a clear fingerprint.
So you have to analyze the transaction and then you say, hey, this transaction has a lot of ambiguity, so it has to be a conjoined transaction.
But otherwise, it's not easy.
And, okay, this is a conjoined transaction, a knapsack transaction, but who has created that transaction or how many participants it has.
So, it's not so easy.
For example, in Wasabi we...

Adam Fiscor: 01:16:19

I disagree completely because there are just so many fingerprints in the blockchain that you can't tell exactly which wallet created that transaction by just looking at the `nLocktime`.

Lucas Ontivero: 01:16:35

Yes yes yes sure it is possible but anyway if you, for example, cannot know so easily how many participants are.
In Wasabi it is easy because you count how many equal outputs are.
If there are 66 equal outputs then there are 66 participants.
In this case it's a bit harder.
So it's something to have in mind.

Rafael: 01:17:15

By the way, if I can ask a weird question, then what did it mean, Nopara, about being able to know which wallet created the transaction by the `nLocktime`?

Adam Fiscor: 01:17:29

That different wallets are using different fees, different `nLocktime`s.
They either use it or not, or they either use a specific number.
They might bump the transaction able to do RBF.
You see there is a set of features.
Those features sometimes run on a...
Let's say the fee, you have to decide what fee you will do in the transaction and if that exact fee that transaction is being made with can only be produced with Electrum.
Electrum is a bad example because Electrum, Bitcoin Core and Wasabi kind of can produce each other's fees.
But if that can only be produced with Electrum, then it's going to be a transaction with Electrum.
Okay, so now we figured out that this is a transaction with Electrum.
Now we have to just apply our heuristic that what is the likelihood that this Electrum is going to create a pay-to-endpoint transaction.
So that's what I'm saying, that there are so many metadata in the transactions that you can probably tell what wallet created it.

Rafael: 01:19:03

Thanks for clarifying that.

Adam Fiscor: 01:19:09

I was fighting a lot against it previously, but I just realized it's not possible to hide anything because there is always something.

Rafael: 01:19:29

And If I may ask another stupid question is what exactly is analog time?
And I mean, I think I've heard about it, but I just don't remember anything.
Or what does it like conclude?

Adam Fiscor: 01:19:45

Lucas.

Lucas Ontivero: 01:19:49

It's when that transaction can be mined, basically.
You say, okay, this transaction can be mined right now, can be mined after this block height.
So basically that's all.
It's a field in the transaction where you specify when that transaction can be mined.

Rafael: 01:20:14

All right, thanks.

Adam Fiscor: 01:20:17

For example, Bitcoin Core and Electrum are using an `nLocktime` that is in order to discourage fee sniping, which whatever it is, it's not on top of my mind.
But, you know, things like this.
Or the RBF, that's like if you send a transaction and you have RBF enabled, then only that information that this transaction can do RBF.
Just, okay, now look at which wallets can do RBF and it must be, it's probably from those wallets.
Now if you do an RBF transaction, if you bump the fee then oh that's a lot more information to expose because you can only bump the fee from removing the change, then you just exposed where you are sending the money, which would be exposed by the transaction chain anyway later on.
But you just exposed at that point where you are sending the money and if the fee bump has such a specific number that, okay, let's say Bitcoin Core always bumps the fee with this number or with this fee rate, then you can further narrow the range of possible wallets that can do that.
So it gets really, really bad.

Rafael : 01:22:01

Okay, Yeah, I think I get it.
And with RBF, you like expose which one of the addresses or outputs are like the actual change.

Lucas Ontivero: 01:22:10

Yes.
That might be the most obvious one.
I didn't even do this for a very long time.
Then things just start to click, you know.

Rafael : 01:22:25

Good to know.

Adam Fiscor: 01:22:31

All right, what else do we have?

Unknown Speaker 1: 01:22:34

Nopara, I have a question.
You said about the paper that had information about confidential assets and mixing or something like that?
You mentioned it like 5 minutes ago or something.

Adam Fiscor: 01:22:51

Yes, I was explaining the history of CoinShuffle.
It started with CoinShuffle, then they came up with a new protocol that doesn't require TOR, that's called DiceMix, and they incorporated it into CoinShuffle, and they called it CoinShuffle++, and then they figured out how to do CoinShuffle with confidential transactions and that is called ValueShuffle.

Unknown Speaker 1: 01:23:30

Can you send me a reference link or something on that?
I'm already done the go in it, but it could be a bit faster and more helpful.
CoinShuffle++?

Adam Fiscor: 01:23:43

Just google ValueShuffle.

Unknown Speaker 1: 01:23:46

Okay.

Adam Fiscor: 01:23:52

Are you interested in CoinShuffle++?

Unknown Speaker 1: 01:23:56

Well, I'm interested in mixing and confidential assets involvement in that.
Because it is, well, I want to know if there is something that I can bring for RGB.

Adam Fiscor: 01:24:12

Yeah, that's something that we could contribute later on.

Unknown Speaker 1: 01:24:20

Okay, well, that could be the topic that I might be prepared for.
So yeah, thanks for explaining that again.

Adam Fiscor: 01:24:32

Yeah, bring it to next episode and we will see.
I think there is some interesting things to learn from me too.
I would give you a vote for that.

Unknown Speaker 1: 01:24:49

Thank you.
Good.
Thanks.

Adam Fiscor: 01:24:53

All right.
Do you guys have anything else?

Lucas Ontivero: 01:25:03

No.

Unknown Speaker 1: 01:25:05

Nothing, I have my homework.

Rafael : 01:25:09

Yeah, me too.

Adam Fiscor: 01:25:12

All right.
The next episode is going to be Snicker.
And yeah, thanks for coming and I will publish it to, I don't know where, if the recording is good I will publish it to probably the Wasabi channel.
And we'll see.
What are your thoughts about how was this so far?
Did you enjoy it?
Do you have any recommendations how to improve these conversations?

Rafael : 01:25:52

At least Aviv's presentation was pretty damn good in my opinion.
I mean like a short recap of what was what and what's the point of Knapsack.
So it makes a pretty good, like, yeah, just a video in itself.
But of course, also these talks too.

Adam Fiscor: 01:26:15

Yeah, I was kind of afraid that Felix is going to leave.
We have to grab Felix at the beginning because he's going to leave.

Rafael : 01:26:27

Yeah, definitely.

Lucas Ontivero: 01:26:29

Yes, from my point of view, the participation of Felix was great.
So, for Snickers, if we can have Adam here, it could be great too.

Adam Fiscor: 01:26:50

I will ask him, I can't promise.
Felix didn't promise it to either, he said he will try.
So that's why I didn't even send out a tweet or anything, "Hey, Felix is going to be here" because if he's not...
Anyway, I will tell Adam to come.
Yeah, definitely.
I hope he can.

Unknown Speaker 1: 01:27:21

Yeah, I think this format was very good.
On one hand, you had a person within the team who introduced the brief recap of the article, and then on the other hand, you had the actual author of the article that could contribute online and fix mistakes, misunderstandings and everything.
And also knowing that he's not working anymore, like Felix is not working anymore, for example, on this topic is also valuable because you kind of understand where it goes and what questions he can cover and which questions probably should be covered by someone else.
So yeah, having an author of paper is very good here.
And of course the discussion afterwards, as always, just marvelous.

Adam Fiscor: 01:28:14

All right guys, so if no one has anything, then thank you all for coming and if this is published and you are listening it on YouTube or something, then definitely everything that we talked about, the paper, Felix's code, our code, everything is going to be in the description.
So you can follow up and maybe change the word by getting some ideas.
All right, thank you guys.
Thank you.
All right.

Lucas Ontivero: 01:28:48

Thank you guys.

Unknown Speaker 1: 01:28:49

Bye-bye.
Thank you.

Rafael: 01:28:50

Bye.
