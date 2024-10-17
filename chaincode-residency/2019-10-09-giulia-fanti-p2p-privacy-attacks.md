---
title: P2P Privacy Attacks
transcript_by: Caralie Chrisco
tags:
  - privacy-problems
  - p2p
  - dandelion
speakers:
  - Giulia Fanti
date: 2019-10-09
media: https://youtu.be/qKNEUfnYue0
aliases:
  - /chaincode-labs/chaincode-residency/2019-10-09-giulia-fanti-p2p-privacy-attacks/
---
Location: Chaincode Labs 2019 Residency

Slides: <https://residency.chaincode.com/presentations/bitcoin/giulia_fanti_bitcoin_p2p.pdf>

Giulia: So today I'm going to talk to you about some work that my collaborators and I've been working on for the last three years now. So this was joint work with a bunch of people who are now spread across a few different universities but it started at the University of Illinois: Shaileshh Bojja Venkatakrishnan, Surya Bakshi, Brad Denby, Shruti Bhargava, Andrew Miller, Pramod Viswanath.

A lot of you have probably heard in the news stories about Bitcoin being portrayed as this untraceable currency. Of course as you all know, I’m preaching to the choir here, but bitcoin is not totally untraceable. There’s a lot of different ways that bitcoin users and transactions can be deanonymized.

In this talk I'm going to focus on one particular avenue for deanonymizing Bitcoin transactions which is the peer-to-peer network. You got a great primer this morning from Suhas on how the Bitcoin peer-to-peer network works. For the purposes of this work I am going to use a very simplistic representation of how the network works.

In particular the problem here is that users in the Bitcoin peer-to-peer network have two identities. The first one is their public key that they're using to sign transactions. The second one is their IP address and to a large extent anonymity depends on not being able to link your public key to your IP address.

So whenever Alice wants to send money to Bob the first thing she does of course is to create a transaction message which is going to get broadcast over this network until all the other nodes hear about it and can start mining to add it to the blockchain.

## How users can be deanonymized

What about this allows users to be deanonymized? Typically when we talk about anonymity problems in the Bitcoin blockchain, people are talking about chain level attacks. Basically because the Bitcoin is just a ledger of every transaction that's ever happened, you can often link together different transactions coming from the same user. You can start making these kinds of graphs that connect together the same user doing multiple transactions with different parties. If you know who certain parties are, if you know that this group of big purple dot is Mt. Gox, you might be able to narrow down the set of users who are interacting with Mt. Gox.

This is typically what people mean when they talk about the privacy vulnerabilities in Bitcoin. Because a lot of people are reusing public keys, in some cases this means that entire transaction histories can be revealed. This was kind of the state of the art in privacy research or privacy understanding in Bitcoin for a while. But more recently people have started looking at the peer-to-peer network and how do the relaying protocols in peer-to-peer networks affect your privacy guarantees.

The goal in our work was to try to understand how easy or difficult it is to link a public key to an IP address. So those two identities that we talked about earlier.

In our work we basically had two main components. The first one was analysis. We try to understand how existing broadcasting mechanisms allow an adversary to prefer the source of a transaction based on just observing the spreading patterns in a network. The result of this was basically that it's pretty bad. In many cases an adversary can identify who is the source of a particular transaction.

The second part of the talk is going to be on trying to come up with a better design for how to broadcast transactions to try to mitigate this privacy vulnerability. That's a project called Dandelion that I will talk more about later.

In this talk I'm going to do something a little different from what I usually do which is to focus a little bit more on the actual process of doing this research and on some of the decisions that we made from a researcher standpoint. Usually when you hear a talk, you hear people say, “Okay, this is the problem we set out to solve. We sat in a room, thought really hard, and bam it's done, solved!” Of course that's not really how research goes. Often it's very roundabout. You don't know ahead of time what you're going to be able to do and what you're not going to be able to do. You have to make a lot of decisions and compromises. I'm going to talk a little bit about some of those decisions and compromises that we made and how they affected the final end result.

A big part of those decisions is in coming up with the model that you use to analyze your problem. Anytime you want to do theoretical analysis you always have to come up with a model for the system that you're trying to analyze. One of the big challenges that often arises is that if you want to be able to say anything conclusive theoretically, your model has to be simple enough to be analytically tractable. But if it's too simple then it no longer represents this system you're trying to model. So there's always this tension between trying to make a model that is not necessarily perfect, but representative enough of what you're trying to get a hold of.

Privacy and security are two areas where theoretical analysis is particularly important because for topics like efficiency, for example. It doesn't necessarily matter if you have a theoretical proof that it's efficient. If you know that it works in practice, if it's efficient in practice, it's efficient. But with things like privacy and security you might not know that it's broken until something really bad happens right? So that's the reason that it's particularly useful for privacy and security problems to have some kind of theoretical proof, so that you know the worst possible adversary can’t do more than this. Of course the flip side of that, is that your guarantees are only as good as your models. If you're able to prove some great results and you've got a model that's really restrictive, it's not that useful.

## Attacks on the network layer

We started this project after reading some papers from the security literature and these papers basically had the following structure. They're saying, let's suppose that we have our peer-to-peer network and we have an eavesdropper, a super node that sets up connections to everybody. The purpose of this eavesdropper is to try to figure out which node originated a particular transaction. So now when Alice starts broadcasting her transaction, she sends it to all of her regular peers but from her perspective this eavesdropper looks the same as anyone else. She'll also relay it to the eavesdropper and her peers also relay to the eavesdropper and so forth. So everyone is treating this eavesdropper just like any other node. Now if I'm the eavesdropper and I want to try to figure out who is the source node, a really natural thing for me to do is to wait for the first node that relays a transaction to me say, “okay I think you're the source.” Now this doesn't always work. Can anyone think of why this might not work all the time?

Audience Member: Network partitions?

Guilia: What do you mean?

Audience Member: A packlet might get dropped by a route in the middle so the timing is not as quick as expected.

Guilia: The key essence of what you said is that the timings are not always deterministic. So in particular in this diffusion spreading mechanism that Suhas talked about earlier, remember that you're relaying messages to your peers with some random delay. What could happen is Alice could send her transaction to Bob and Bob could forward it to the eavesdropper before Alice herself does. So in that case, if I'm the eavesdropper and I'm just pointing at the first node that relays it to me that's not always going to be 100 percent correct.

What can the eavesdropper do about this? Well in these security papers that we were reading, the approach that they took was to set up a bunch of mini eavesdroppers. Let's say we have like one eavesdropper on each port of the adversaries running. Each of these mini eavesdroppers makes a connection to each of the nodes in the network. Now what do we have? It’s spaghetti. But the point is that if Alice starts broadcasting her transaction now, three out of five of her connections are to the adversary. So with probability ⅗ the first message that she sends is going to end up with the adversary. So the adversary can get more and more accurate by making more and more of these connections.

Audience Member: There can still be a possibility that there is a different node that has better connection and going through him might physically be faster than going directly to the adversary?

Giulia: That is true. Here we're kind of imagining that all of these links are created equal or the same speed which might not be true in practice.

Audience Member: But isn’t the actual Poisson delay is significantly higher than what you might imagine network latency to be?

Giulia: That is also true. The Poisson delay is on the order of seconds. It's going to be a lot slower than changes in network. If you have two exponential delays that are roughly the same then network latency might play an effect but I think that's going to be probably a second…

So to try to capture this we made an adversarial model that is summarized by two parameters. The first one is theta ( 𝜃 ), which is going to be the number of connections that the eavesdropper makes to each of the compromised nodes. So here theta ( 𝜃 ) is equal to two. The second parameter is going to be “p” which is the fraction of nodes that are being eavesdropped on. In the previous examples that I showed you “p” was equal to one. The eavesdropper had connected to everyone but in principle you could imagine an eavesdropper who's only connecting to some fraction of nodes in the network.

Our adversarial model has these two parameters: “p” and theta ( 𝜃 ) and in our work we focused on two main operating regimes in this adversarial model.

The first one is where “p” is equal to 1 so the eavesdropper is connecting to everyone and theta ( 𝜃 ) can be arbitrary, anywhere from one to infinity. This is capturing basically this eavesdropper model that you've read about in security papers. The second adversarial model that we considered is where “p” is less than 1. But let's say that the eavesdropper has infinitely made connections with each node. It’s as if the nodes themselves are corrupt. We call this the botnet adversary and this way of framing it as an eavesdropper is really just a mathematical abstraction. Really we're thinking of these nodes as just being themselves corrupt. They're part of some colluding botnet that 's trying to deanonymize people. In this work, we started our analysis of the anonymization on the eavesdropper adversary and then ended up actually designing Dandelion to be robust against the botnet adversary.

Here I’m going to deviate from how I usually give this talk and explain a little bit more. This is a little funky right? We're analyzing the problem under one adversarial model and trying to fix it in another. So what happened here was that once we figured out there was a problem with the eavesdropper model it turned out to be actually pretty easy to fix that problem under the eavesdropper model. So here's a kind of a distinction that arises in academic research that might not happen if you're in industry and trying to research some of these issues.

So in academia we care about solving impactful problems but we also care about publishing papers. If your problem is too easy it's not going to be publishable. That was part of the motivation for going to this botnet adversary because we felt that this was still like an important problem but it was a little bit more challenging and required a little bit more mathematical machinery so we thought it would be a better fit for academia. In your case you probably won't have run into these kinds of considerations but it's just something to be aware of if you are working with academics in this space.

Let's start out with Part One: Analysis. Are there any questions so far on the model?

## Analysis

So analysis. How bad is this problem?

Here I should give a little bit more background and Suhas touched on this earlier. Now up until about 2015 the peer-to-peer network was using a broadcasting mechanism called trickle.

Here I made a very stupid mistake that I hope to convey to all of you so that you don't make it as well. I read about trickle in one of these security papers and the lesson here is that you should never try to understand a protocol just from somebody else's description of it. You should read the code. I misunderstood how trickle was working from the description of this paper and thought it was the following model. I thought that you arrange your neighbors in some random order, let's say 1, 2, 3, 4 and then let’s say every one second you send your message to those neighbors in that order. So it turns out this is a little bit off and we actually got an email after putting this paper on archive from Greg Maxwell being like, “Hi. I don't think you completely understood this correctly.”

My understanding and I guess there's people in this room who know this much better than I do, but my understanding is that what was actually happening is at each time slot, so like if we're waiting one second between each communication, at each time slot you pick one of your neighbors uniformly at random and then send the message over that edge. Is that correct?

It's similar to what is happening here but it's not exactly the same. Take these results with a grain of salt. This was done until about 2015 and then because of the privacy issues that Suhas mentioned they switched to diffusion. Under diffusion on each of your edges you take an independent exponential delay, and once that timer ticks you send your message along that edge. We were looking at the github logs and it said that they were doing this for privacy reasons but we didn't understand exactly what those trade-offs were.

So the question that we tried to answer was: does diffusion actually provide stronger anonymity than trickle spreading? So notice here that even though the model of trickle is like it's a little bit off it's close enough that I think it's probably a pretty reasonable representation, so I don’t think this is completely off...

To answer this we wanted to model the problem in some way that's analytically tractable. Now one of the big challenges in analyzing random processes on graphs is that graphs are a pain to analyze. If any of you have tried to do any analysis on graphs, getting results for general graphs is a big deal. It doesn't happen very often. So typically what people will do when they're analyzing these kinds of processes is to start with a simpler topology that's easier to analyze.

So for example we started with d-regular trees. So d-regular trees are trees where each node has exactly “d”neighbors and so we assume that like the honest connections are structured in a d-regular tree. Then we have our eavesdropper that's making theta ( 𝜃 )...

So this is our graph topology and here trees are actually a somewhat reasonable model for the Bitcoin peer-to-peer network because in random graphs that are sparse, so like in Bitcoin you can think of the graph as being constructed by choosing like let's say eight outbound connections. You have a bunch of nodes, you have like thousands of nodes in the network, you have tens of thousands if you include all types of clients.

In these kinds of graphs that are constructed by choosing random edges in a sparse way, it's been found in a lot of different cases that these graphs tend to be locally tree-like. What does that mean? That means if you look at one particular node and you look in a local neighborhood of it, it looks roughly like a tree. Trees end up being a pretty reasonable model for a lot of these types of analysis and we found in our simulation that our predictions on trees were pretty close to what actually happened in simulations on the real Bitcoin topology. That's one simplification that you could make if you were trying to do analysis on these kinds of problems.

Audience Member: Is there some kind of intuition of why - a node goes online and the slots get taken and so on and so forth?

Guilia: Good question. The reason, if you think about it intuitively, let's say that every one of us is picking two neighbors. Okay, say I pick you two. I’m selecting you uniformly at random from the pool of everyone in this room. Now, if we look at the probability of either of you two picking me again it's quite small. The dominant event here is going to be that you two pick somebody else and that continues for a few hops. So basically if you have enough nodes and everyone is picking only a few connections, you can show with high probability that locally you're going to get a tree looking structure. That make sense?

Audience Member: Yeah you can have outbound connections for the same incoming connection- it’s usually just one way.

Audience Member: She’s saying even your child won’t have your parent as a connection, probably.

Guilia: Exactly. This is our graph topology. The next thing that we need to specify when we're analyzing privacy is: what metric do we want to analyze? People have a lot of different metrics for privacy. For anonymity we chose to analyze the probability of guessing the true source conditioned on two pieces of information. The first piece of information that we condition on is how, which is going to be the timestamps that the adversary observes. So our eavesdropper from each of its connections, it's going to get some high stamps as to when the message gets relayed. We're assuming that the adversary sees all of that.

The other thing that we're conditioning on is the topology of the graph, the structure of the graph. Remember Suhas mentioned that it's actually, right now there's an ongoing effort to try to hide the structure of the graph and that's supposed to be difficult. There has been some work, Andrew Miller has some work on trying to recover the graphs topology even if it's supposed to be hidden by basically placing conflicting transactions at different locations in the network and seeing where they spread to. You do that a bunch of times you can kind of recover the topology. There have been some attacks on trying to recover the topology anyway. Assuming that the adversary knows the graph is basically worse case assumption. That gives the adversary the most power possible.

That's the metric that we're analyzing and finally we want to understand: what estimators should we analyze? What is the adversary actually doing to try to deanonymize users?

For this work we analyzed two different types of estimators. The first one we call the first-spy. This estimator basically just looks at all of the timestamps reported by each of the nodes and it picks the smallest one. This is basically saying the first person who relays to me, I'm going to say that they're the source. On this picture I think node four has the smallest timestamp. It's going to be the estimator for the first-spy adversary. The reason this is a useful estimator is because this is what's used in those security papers that I talked about earlier; it's a very natural easy estimator to run. It doesn't actually require any knowledge of the graph. Notice you can do this even if you don't know the underlying graph topology.

## Maximum likelihood

The other estimator that we look at has a lot more power, the maximum likelihood estimator. Out of curiosity how many of you take in a class on like estimation and detection? How many of you know and a maximum likelihood estimator is? Okay alright good. Let's talk about maximum likelihood.

Let's suppose that we're living in a world where there are two options. Let’s suppose that we know that the transaction came from either Alice or Bob. Let me write a little bigger so the people in the back can see. So we have two nodes, Alice and we have Bob and these guys are connected on the network in some way. Our adversary, remember, is observing timestamps from everyone. So our adversary has this vector tau (𝝉) of timestamps at which the adversary received the message from each one of the nodes in this network. Here we have a bunch of nodes that are not Alice and Bob.

When we talk about the likelihood of an event we mean the probability of seeing the observations that we saw, seeing let's say tau (𝝉), conditioned on each of the options that we're looking at. The probability of observing tau (𝝉) conditioned on Alice being the source versus the probability of tau (𝝉) conditioned on Bob being the source. We can compute these probabilities exactly because we know the graph and we know the random mechanisms that's being used to spread the transaction. These are called the likelihoods for Alice and Bob and the maximum likelihood estimator is going to pick whichever one of these probabilities is higher. Maximum likelihood estimators are a good choice when we don't know prior the probability of Alice being the source versus Bob ahead of time.  So if we think that everyone is more or less equally likely to be the source maximum likelihood estimation is a good way to go. Notice that maximum likelihood estimation doesn't say anything about the complexity. Here we're giving the adversary arbitrary computational complexity. They can take as long as they want to compute this. This is the best estimate that they can make.That's what I mean by this maximum-likelihood estimator. This is going to be more accurate. This is always going to be more accurate than the first-spy estimator. It’s using more information.

These are the two that we considered and now finally I've set up the type of graph that we analyzed, set up the metrics that we looked at, and the types of estimators that we analyzed. Now let's look at some results.

This table is showing you the probability of detection for both trickle and diffusion under the first-timestamp and the maximum-likelihood estimators. Now there's two things that I want to highlight here. The first one is that as- sorry here the asymptotics are in the degree of our graph “d” the degree of our tree -as the degree of our graph is growing, this is showing how the probability of detection scales. The first thing to notice is that for the first-timestamp estimator as our degree grows our probability of detection is tending to zero. Can anyone think why that might be?

Audience Member: Because you might pick one of the other ones first.

Giulia: Exactly. Let's say I have like a bazillion friends and the probability that I send to one of them very quickly and then they relay to the adversary very quickly before I send to the adversary gets higher and higher the more friends I have. Because you basically have a bunch of independent events. Intuitively this makes sense. However if we use the maximum-likelihood estimator, this isn't true. Our probability of detection remains bounded away from zero even as “d” grows to infinity. This is really showing you the power of knowing the graph. If you know the graph you can account for these events. The other thing to notice which is of course what we actually set out to answer in this work, is that at least asymptotically these columns look the same. Of course you should always be suspicious when you see asymptotic results because you don't know what the constants are. But it turns out that in this case the constants actually look pretty similar as well.

The intuition here is that the symmetry of these two schemes is outweighing local differences and randomness. What I mean by that, is even though trickle is sending, you know in this random order over its neighboring edges, on average its sending in all directions at the same rate and that's what diffusion is doing as well. When you send transactions at the same rate in every direction, your transaction is spreading kind of like a ripple on a pond. All the adversary needs to do is to find the center of that ripple to identify the source of your transaction. That’s the intuition behind all of these attacks.

I'm not going to go into detail on this proof sketch. I don’t want to bore you guys to death, but I will give you just a very quick intuition. Let's suppose that these yellow nodes are the nodes that have the source at the time of the attack and these blue guys are the ones that have the message and also reported it to the adversary. Basically if you look at the neighboring sub trees of the true source, the key point is that each of these neighboring sub trees is going to have approximately the same number of blue nodes. And that's not true for any of the other nodes in the graph. So like this blue node has 1, 0, 3 whereas this one had 1, 1, and 2 which are approximately the same. You can show that more formally using a technique called Generalized Polya Urns which I will not go into.

These results that I told you, they're kind of weird in the sense that they were asymptotic in “d” the degree of our graph. Why is this a weird result? Why should you be suspicious of that result? Is your graph changing its degree over time?

Audience Member: It shouldn’t.

Giulia: Yeah maybe a little but not large-scale. Typically what we're worried about is, you're given a graph, you have whatever topology you have and you want to understand: what's the adversary's probability of deanonymizing a node at any point in time? Does it make sense why that’s kind of a disconnect?

The results that I gave earlier, they’re asymptotic in a property of the graph. That means as the degree of our regular tree grows and grows, we see how the probability of detection decays. But that's kind of a weird result because in practice your graph topology is not actually changing. It is what it is. It might be changing a little bit, like you might have a few nodes that are changing their peers over time, but in aggregate it's changing at a pretty slow rate compared to the rate at which transactions are propagating. So far so good?

It's kind of weird to give a result that's asymptotic and a property of the graph when the graph isn't really changing over time. You’re not expecting the degree to grow to infinity as time goes to infinity. Does that make sense?

## Simulations

To try to understand what actually happens in practice we turn to simulations. We started by first simulating our results on trees, on regular trees again. Here we're comparing trickle and diffusion and the blue line is the theoretical prediction for diffusion and we see that they're basically identical. At least on a tree you don't expect, really any difference at all. But again this is not super representative because as we said earlier the Bitcoin graph is not a tree and here what I'm varying is the number of eavesdropper connections per node. So as the eavesdropper makes more and more connections to each node, their probability of detection is tending closer and closer to one, which is consistent with our intuition. But again this is kind of weird because we're looking at results on trees whereas the network is not really a tree.

What we tried next was to look at some results on the Bitcoin peer-to-peer graph. This was a snapshot of the graph taken in 2015, so it’s a bit outdated. Basically we simulated trickle and diffusion and we applied our predictions for a tree that has the same average degree as the graph snapshot that we used. To my infinite surprise it actually was a pretty good predictor of the simulated deanonymization accuracy on the real Bitcoin graph as well. That is presumably because of the fact that you have this locally tree-like property on the Bitcoin peer-to-peer network.

So here again what we're varying on the x axis is the number of eavesdropper connections. The more eavesdropper connections you get the higher your probability of detection gets. Now on the Bitcoin peer-to-peer graph we actually do see a little bit of a difference between trickle and diffusion. Remember lower is better here. We don't want, like for privacy we want the probability of detection to be low. It does look like there was some small gain by moving to diffusion but the problem is as this as this number of connections grows the difference gets smaller and smaller. The other problem is that even for just a few connections you can get probabilities of detection over ½ which is a little alarming.

That kind of wraps up the conclusions from the first part of our research which suggested to us that diffusion doesn't seem to have significantly better anonymity properties than trickle. Now the caveat here is that in moving to diffusion they also patched this other thing that Suhas mentioned where you could basically just force a node to tell you anytime they had a new transaction. So in practice it did have a good privacy implication but the properties that we were looking at were more theoretical looking at these two protocols to try to compare.

We’ve been going for about 45 minutes. I wonder, would it be a good time to take a five-minute break and then we can talk about the second part on redesigning the peer-to-peer network? Before we break are there any questions on the first part of this talk?

Audience Member: I'm curious if you tried with more than 20 connections? I assume that people like Chainalysis a thousand connections or even more...

Giulia: I'm sure they do. We were limited..

Audience Member speaks

Audience Member: It was 20 connections to each node?

Giulia: Twenty to each node.

Audience Member: Okay. That makes more sense.

Giulia: Yeah, I didn’t try more than 20.

Audience Member: Twenty is enough.

Audience Member: Before we also discussed churn and how that would influence how that graph connects to each other so that would be a significant improvement also?

Giulia: Yeah, that's a great point. So if you have a lot of peer churn in your network it becomes a lot harder to do some of these more sophisticated attacks. The first-spy adversary still works basically perfectly. That doesn't suffer at all for peer turn. Adding peer turn for privacy is something that we will try to exploit in the next part of the talk and I think that does help from a privacy standpoint but for some of these very basic estimators it doesn't really make much of a difference.

Audience Member asks a question

Giulia: Peer turn is just when the peers in your peer-to-peer network are coming and going or like changing connections, these types of things.

Audience Member asks a question

Giulia: I believe you have a per peer timer. Let's say if I have a connection with you, when your timer hits, I believe you send it in for all the transactions that are queued up for you.

Audience Member: I think we understand, so there's simulation versus the actual topology but I didn’t understand what actual topology did you take when comparing the two?

Giulia: For the simulation for the dotted lines, I used a snapshot of the Bitcoin peer-to-peer network measured in 2015 before they made it hard to understand what the graph topology looks like. This was collected by my colleague Andrew Miller who had a project that is basically an eavesdropper node. For the analytical prediction I took the theoretical results for a d-regular tree where “d” is equal to the average degree of the Bitcoin snapshot graph.

Audience Member: I'm sorry. Could you please recap the difference between trickle and diffusion?

Giulia: Sure. Trickle was the pre-2015 approach that was being used to relay transactions. This was the one that I kind of goofed up on the modeling aspect. The way I was modeling it was that you ordered your peers in some random order and then on every like “k” seconds you'll send the message to the next peer in that ordering. You can think of it almost as like a discrete-time relaying process.

Audience Member: That was close enough, so you stayed with that?

Guilia: I mean we found out about it after we posted the paper, so our hands were a little bit tied at that point. I do believe actually that if you were to change it to what was actually happening in trickle you would get similar results. Every “k” seconds you change which peer you're communicating with.

Audience Member asks a question

Giulia: That’s a really great question. The question was: is there any reason to think that between 2015 and today this predictive model might no longer hold? The answer is yeah, some things have happened I think in recent years that might make this a less good predictor. One of these is that we're starting to see more super nodes. We're starting to see nodes that are disobeying protocol and making like a bunch of connections. I believe that's happening to an increasing degree but maybe some of you guys who work on this more regularly can correct me if I'm wrong.

Basically the point is if you have a lot of nodes that are disobeying protocol and are not just making eight outbound connections, then it's going to look less tree-like basically. This is one of the things that Andrew Miller found with his eavesdropper node that he was using to try to measure the graph topologies that you have some nodes that are making way more connections than they're supposed to.

Audience Member: I'm curious how did you do the graph snapshot? It doesn't sound like even knowing the exact right graph right now is that easy.

Giulia: I think that's true. Back when Andrew collected this, I think there was some trick, where you could figure out if you are connected to a peer you could figure out who they were connected to. I think that's been kind of clamped down on by now.

Audience Member: It’s still very easy to figure out.

## Part two

At the end of the last session we concluded that diffusion doesn't seem to have significantly better anonymity properties than trickle. So some of the key things that I want you guys to take away from that portion of the talk was really how to think about modeling some of these problems if you want to do any kind of theoretical analysis.

Often if you're trying to do something fully general it can be tempting to make your models really complex and have all the bells and whistles that are actually represented in the real codebase. Often these are the kinds of things that are going to make the problem intractable; it probably won't be able to do anything. In our work we had to do a lot of simplifications down to a model that was pretty simple but ended up being reasonably representative of the final system. After concluding that trickle and diffusion have more or less the same performance, that really motivated our decision to try to come up with a better design that doesn't have this weakness.

Just as a reminder in this part of the talk we're going to have a slightly different adversarial model where we're going to assume that some fraction “p” of spies are participating in the network. We call this a botnet adversary and their identities are unknown. They get to observe whatever metadata comes to them. They're just regular nodes so they can see what time they get a transaction from you. They know who they got it from. These spies are all colluding and are trying to infer the source. In the beginning we assume that these spies are honest but curious. This means they are following protocol and they're using whatever information is available to them from the protocol to try to deanonymize users.

Matt was saying during lunch that there's some evidence of basically like botnets controlling something like 10% of the peer-to-peer network which was kind of surprising to me. It seems like this adversarial model may actually have some grounding in reality. We also assume for our analysis that these adversarial nodes are uniformly placed in the network. We're assuming that they're not targeting one particular node, they're kind of uniformly spread out.

If these nodes were targeting one particular node what should they do? Surround it. Yeah. I guess you learned about eclipsing attacks, was that yesterday? If they were interested in this guy they should try to basically surround it completely so whatever it sends they'll know who it was. But in this case we're interested in a more broad scale adversary that's trying to deanonymize as many people as possible. This would be the goal of… for example.

## Metrics for anonymity

Our metric for anonymity is actually also going to get a little bit more complicated in this portion of the talk. Remember in the previous portion of the talk we were analyzing the probability of detecting the source. In this portion of the talk we're going to assume that you have lots of transactions and lots of users and the adversaries goal is to try to map transactions to users.

The key difference here is that in the previous portion of the talk we were thinking about one transaction that's spreading. The adversary observes how that transaction spreads and tries to guess the source. In this case it's observing a bunch of different spreads and it can use those different spreads to try to improve its guess. Basically if we know that each user has one transaction, and so there are “n” transactions and “n” users I know that two transactions are not going to come from the same guy. I can use somebody else's transaction to actually improve my guess on your transaction which is kind of disturbing but it's possible in practice.

What we're going to do here, the adversary is going to design some mapping “M” that maps each transaction to one user. We're going to define first a metric called recall which basically just counts how many of these arrows are correct. In this case the top arrow is the only one that's correct so we have a recall of ⅓. I want to point out here that recall is basically the same thing as probability of detection so this is exactly the same metric we were analyzing earlier. I've given it a different name here because precision and recall are concepts from the machine learning literature as well as used in a lot of different domains that typically go together. So that's why I've changed the wording.

The second metric is precision. Precision is defined as follows: for every correct arrow, I'm going to count the number of total transactions that got mapped to that same guy and assign it a value of 1 over the total number of transactions mapped. For this red guy we have a correct arrow but three total transactions mapped to him. So this guy gets a value of ⅓ and these two get a value of zero. We take the average over all three so we get 1/9.

Intuitively precision is trying to ensure that the adversary doesn't put all of its guesses on the same user. It's trying to capture plausible deniability in some sense. Because if the adversary tries to put all of its guesses to the same user, the user can say for any one transaction, “well I couldn't have generated that one because you also said I generated this other one.” You should think of precision as like a plausible deniability type of metric. Whereas recall is just the raw probability type of metric. Recall is more commonly analyzed in the literature so this is a little bit new I would say. One key insight is that in practice, adversaries can and will use knowledge about other people's transactions to improve their knowledge of your transactions or try to deanonymize you better. Precision is trying to capture that.

These are our two metrics and we want both of them to be as low as possible. Remember we said probability of detection should be low. We also want precision to be low to have good anonymity. Our goal is to design a distributed flooding protocol that minimizes the maximum precision and recall achievable by a computationally-unbounded adversary. It’s a bit of a mouthful. I like to share this for a second.

I’m trying to minimize the maximum precision.  I'm going to try to interpret this goal in a picture for you. Remember we're looking at two metrics. One is recall, one is precision. Adversary wants to be up here and we want to be down here for perfect privacy. Here “p” is the fraction of spies in our network. We started by showing that because of the way we've defined precision recall, any scheme that you design is going to fall somewhere in this like almond shaped thing. That's basically because of the definition of precision recall.  Your recall is really high, by definition your precision will also be pretty high. So that's why you can't achieve any point in this. It's always going to be somewhere in this middle region.

Let's suppose we choose a spreading protocol. Let's say we're thinking about diffusion. Remember diffusion was the protocol that we talked about in the last half which is what's used today where you broadcast transactions to each of your peers with independent exponentially...(inaudible)

Now let's suppose that we consider every possible estimator the adversary can think of. Remember an estimator is just taking a mapping from transactions to users. Each of those estimators is going to be some point in this almond and if you cycle over every possible estimator you'll basically trace out a region. So this region should be filled in. You trace out a region in this space. The size of that region is basically telling you how good is your spreading mechanism, how private is your spreading mechanism. So the worst possible spreading mechanism we could think of would take up this whole region. The best possible would be just like a point down here. That make sense?

When we started this work, one thing that people like to do in theory circles, is to try to prove converse bounds or like lower bounds on whatever property you're trying to reason about. In this case we want to know what is the minimum possible precision and recall that we can hope for over any spreading mechanism. We started by showing that no matter what spreading protocol you use they are always going to have a maximum recall that is greater than or equal to “p” where “p” is our fraction of spies. This means no matter what spreading protocol we use this region has to extend to at least to this vertical dotted line, andbe to the right of it.

The second result is that no matter what protocol you choose your maximum precision is always going to be at least “p²”. So the top part of this region is always going to be above the horizontal side. The recall result is a lot easier to reason about but intuitively this is happening because if I send my message to some random person, with probability “p” they're going to be a spy. So if they just use the first-spy estimator you're going to be right at least “p”  fraction of the time. That's telling us why this maximum recall estimator....(inaudible). Kind of a similar intuition.

Make this a visual, every spreading algorithm that we look at is going to have at least one point in this gray area. In other words the best possible region we can hope for is this green triangle, this little nubbin. That's our goal. The goal is to find a spreading protocol whose region looks like the green triangle. If that's all you take away from this slide, green triangle. All of this is really just interpreting our metric and trying to understand what is the problem. Now how do we hope to achieve this? Well there's two intuitively there's two properties that we really want. The first one is asymmetry. If you guys remember from the previous half of this talk when we said that trickle and diffusion seemed to both be bad and the reason for that is that they're sending messages in every direction at roughly the same rate and by every direction I mean every direction on the graph.

Intuitively the way to improve your privacy is to break that symmetry. If you send it faster in one direction than the other it becomes harder for the adversary to figure out where it originated. We're looking for asymmetry. Another thing we're looking for is mixing and here I don't mean mixing in the sense of like a mixed network. I mean it in the following sense. Let's suppose we have four honest nodes in a row; they're all sending their messages to the right. We have the spy node at the end collecting them. The spy node is going to get four transactions one from one one from two three four and so on. From the adversaries standpoint, from the spies standpoint, all four of these messages basically look the same because it doesn't know when any of them originated. The metadata that this spy gets is just the time when the message was delivered to him and from who, but it's only getting delivered through this last edge so that doesn’t really differentiate anything. When I say mixing I mean whatever the spy sees it should have a hard time telling if it actually came from node four or if it came from node one or who it came from. Intuitively this is these are the two properties that we’re looking for.

We have a few knobs that we can control to try to make that happen. The first knob is the spreading protocol. We've given a graph on how we spread content. As we've talked about a few times today currently that's done via diffusion. The second knob that we have is the graph topology. Right now we have this construction where each node is picking up to eight outbound peers but in principle maybe you could change the peer-to-peer topology to make it more privacy-preserving, potentially.

Today we'll use this approximately regular. The third property is dynamicity. How often does the graph change? As we mentioned earlier this is changing on a fairly slow timescale. Most transactions take seconds to propagate, like tens of seconds whereas the graph is changing on a slower time scale. One option would be to have the graph change at a faster rate and make it harder for the adversary to learn the graph which in turn gives you better privacy. That's something that we've also touched on already today.

In Dandelion we're going to touch on all three of these properties. Let me start with the spreading protocol. The Dandelion spreading protocol is very simple. The idea is that if you start with let's say this node is the source. So the source instead of spreading the message to all of its neighbors it's going to choose just one. It sends its message to one neighbor and that one neighbor is gonna pick one of its neighbors to forward this message and this happens for a random number of hops. This is called the stem phase. After that random number of hops all of a sudden we switch into the fluff phase and here we start doing diffusion again. This guy spreads it to all of its neighbors and they spread it theirs and so on. We call this Dandelion because the spreading pattern looks like a Dandelion plant.

Why is Dandelion spreading a good thing to do?

It turns out that it has an optimally low maximum recall of “p” plus some terms that are put with 1 over “n”  and “n” here is the number of nodes in the network. As your network grows you get closer and closer to that lower bound precision like we talked about. Remember our lower bound is equal to “p”. This is good because it means like earlier we were reasoning about these regions we had two metrics that we were trying to optimize. Optimizing two metrics is a pain. We want to optimize one metric. This tells us that if we constrain ourselves to Dandelion spreading we can basically only worry about precision. No matter what graph topology we apply this to we're going to get recall “p” assuming the graph is good. That nails down the spreading mechanism.

The two other knobs we had were graph topology and dynamicity. For graph topology we think about having basically to to like overlay graphs. The blue lines here are going to represent the regular p2p Network whatever currently exists. In addition to that we have these black lines which represent the anonymity graph and this is what the stem is going to propagate over.

Just to show you how that works, if a transaction comes in at one of the nodes it propagates clockwise over this line anonymity graph or some random number of hops and then once the stem phase is over it gets diffused over the rest of the graph. This diffusion is ensuring that the transaction spreads quickly enough. If a second transaction comes in it's going to propagate clockwise over the same anonymity graph. This is actually important. They should be propagating over the same line until the fluff phase starts. This is the topology that we have in mind. I'll talk later a little bit about how to construct this topology.

Finally the third property that we talked about it's dynamicity. We want to change this anonymity graph pretty frequently and the reason for that is so that the adversary doesn't really know the graph really well. The adversary is always going to know its neighboring nodes. That's impossible to fix, you can't get around that. But what we don't want the adversary to know is what's in the areas that are uncharted. What's in the areas that it's not connected to? For that we're going to change this line graph periodically.

So the Dandelion network policy exists of Dandelion spreading line graph topology and fairly high dynamicity. In our analysis we assumed away some of the properties of this high dynamicity and just assumed that the adversary doesn't know the structure of the line graph in our initial analysis; later we extended this to when the adversary does know the topology. But in our first paper on the topic we just assumed that the adversary does not. In that case it did show that Dandelion has a near optimal maximum precision that looks like “p²” times log “p”. Remember our lower bound on precision was “p²”. Your “p” is less than 1 so “p²” is smaller than “p”. Here in our precision we have this p² term times a logarithmic term or a log factor away from optimal.

If we interpret this in terms of the picture that I showed you here, this little blue region shows you the anonymity region for Dandelion. The red one shows you a lower bound on the region for detergent. It could actually be larger, this was obtained through simulation. The yellow one is what would happen if you just flooded to all of your nodes with no delay. That’s here. This is showing us that basically we're pretty close to the green triangle, remember our green triangle.

## Why is Dandelion good?

Dandelion seems to have some good theoretical properties but why is it good? We give you a little bit more intuition as to why this should be the right thing to use. To try to give you some of this intuition I'm going to talk about some ideas that don't work.

The first thing we tried was a tree. There's a bunch of reasons why you don't want to structure your p2p Network like a tree potentially but we thought maybe for privacy this would be a good idea. Let's suppose you structure your network as a tree and every node is passing their transactions up the tree towards the root. This turns out to have a precision that looks like your “0(p)”. Remember “p” is larger than “p²”. We want p². We're getting “p”.

The reason this is happening is because trees have too many leaves. Basically what happens is for every red node in the second-to-last layer that red node is able to perfectly deanonymize two leaves or however many leaves there are. Because you have a constant fraction of red nodes in your second-to-last layer, basically these red nodes are doing a ton of damage. This gives us the intuition that we want a graph topology that doesn't have too many leaves in it.

The other type of topology that we actually thought would be really good is a complete graph. Here everyone is connected to everyone. Again there are reasons why you would not want your p2p network to be a complete graph, but it's for the sake of analysis. Let's entertain this idea. This turns out to also have suboptimal precision. The intuition here is a little bit subtle. Remember we talked about wanting to have mixing. We want different transactions to take the same path in the network so that they look similar to a spy. What happens in a complete graph is that there are so many paths the probability of two transactions taking the same path is actually very low. This red node, if it's observing transactions from different nodes in the network, the probability of those transactions coming in on the exact same edge is actually pretty small. This gives us an intuition as to what's wrong with complete graphs. They have too many paths internally, too many edges. What we want is a topology that has few leaves and not too many paths.

A line graph kind of ticks both of those boxes. Actually what I showed you was a cycle graph so it has no leaves and it has only one path internally. That's intuitively why Dandelion is getting good anonymity properties. Basically what we were thinking is that every node would choose one of their outbound connections to be their Dandelion edge like two or whatever- so I've only talked about line graphs. Choose one of your outbound connections as your Dandelion edge and anytime you either receive a message that's in stem phase or anytime you generate a transaction you send it over that Dandelion edge. Along with that message each node in the stem is flipping a weighted coin. Like with probability at a .1 they start the fluff phase with probability 0.9 they relay it to their Dandelion outbound edge.

The number one most common FAQ is why don't you just connect through Tor? The idea here would be that if Alice is broadcasting her transaction, she connects through Tor to some other random node and the other random node broadcasts her transaction. This is a reasonable thing to do and as Suhas mentioned, if you're worried about targeted attacks this is probably what you should be doing. One downside is that when you're relying on these kinds of third-party services basically it's only the people who are already really worried about privacy that will be using the solution. Ideally if you're trying to build a system that is protecting everybody's privacy there should be something built into the system that is protecting that. So that's kind of the spirit of Dandelion, this system is internal.

The other thing that people ask is I2P integration. For those of you haven’t heard of I2P, it's conceptually kind of similar to Tor. You're basically building a cryptographic tunnel to another node. The end result is that this other node gets it, the tunneling is done within the peer-to-peer network that you're looking at but these guys are not actually routing the transaction. I'm oversimplifying things a little bit here. But the point is this is not relying on an external service. For example Monero is doing this integration right now. This also addresses the same problem that we're trying to protect here. This would be another way of doing it. The only potential downside that I can see with this kind of approach is that it may take a little bit longer to implement just because implementing cryptography correctly is pretty hard. It can take a while to do it right and to build up the necessary expertise. A lot of projects that we've talked to maybe didn't feel comfortable or felt like integrating I2P would be too big of a change to their codebase and so they didn't want to do that. They felt the Dandelion was like a simple enough protocol that they were maybe a trade-off in terms of just easy (inaudible).

## Practical Considerations

So now let's talk about some of these practical considerations that you all have been asking very good questions. What do you think would be one of the trade-offs that you want to make when you're thinking about whether to deploy Dandelion or not? What's one of the downsides that you can potentially see?

Latency.

When you have this initial stem phase it takes longer for the transaction to reach all of the other nodes. This could be a problem if you want your transaction to get added as quickly as possible to the ledger. This is kind of an old plot, this is from 2013 but it's showing a PDF of the time to first transaction sighting. Here on the x-axis we have the number of seconds until each node first saw a given transaction and this is the density of that. What we see is that on average nodes, they're taking 10 and 20 seconds for you to see a transaction for the first time. This is actually kind of slow. I guess this measurement was taken when trickle was still used.

Even now if you think about diffusion, if each transaction, if each edge has a delay of about 2.5 seconds these numbers don't seem to be that far off and I'm sure there are more recent numbers that we’ll hear about later. But the point is this is taking on the order of 10 to 20 seconds so the amount of added latency that we can tolerate is maybe on the order of like a couple of seconds, probably the most you would want to add.

To try to understand what is the overhead of adding Dandelion another thing to point out here is that if you are running Dandelion, you don't have to use that two and a half second delay as you're relaying it. You can use that to lengthen your stem without adding too much latency overhead.

We implemented this and tried running some Dandelion nodes in the Bitcoin network and tried to measure as a function of our path length, of our stem length, how much time it took to reach 10% of nodes in the network. We took this measurement again using Andrew Miller's coin scope device. We waited to see we're connected to some 10% of nodes or we're connected to a bunch of nodes while we waited until 10% of them had relayed the transaction to the eavesdropper. What we see here, so when path length is 0 that's basically just regular diffusion. As you scale from zero hops to about 10 hops you're adding a couple of seconds on average to the latency required to reach the first 10% of nodes, which suggests that you can probably tolerate about 10 hops without adding too much latency. Again this is not an exact science, we’re really like ballparking numbers here.

How does the path length affect your privacy here? In the analysis that we did we assumed infinite path length but a key point here is that as soon as you reach a spy node everything that happens afterwards is not going to help your privacy. If you have like 10% spies in your network and in expectation it'll take you ten hops to reach one of those spies and then after that you're not getting any more privacy. So even though our analysis assumed infinite path length in practice the amount of path length that is actually contributing to your privacy is much shorter.

So based on these measurements as kind of a ballpark figure we chose 0.1 as our probability so that on average you'll have a path length of about 10.

Another question you asked is you don't actually know in this protocol if your message will get diffused. Let's suppose this was our stem but this guy is evil. He's going to drop our message, he’s not going to forward it. In the protocol that I've described to you so far there's basically nothing protecting you. Your transaction is never going to reach the rest of the network.

What we did in our reference implementation was to implement random timers on each of the nodes in this stem and once one of these timers goes off these are also exponentially distributed timers, once one of them goes off it starts diffusing the message. And similarly once this guy’s timer goes off he'll start diffusing the message and so forth. This is true for all of the nodes of the stem crop. Obviously this is going to have some impact on your privacy and we have a little bit of analysis on this in our paper Dandelion++ but this is really a trade off because you can't sacrifice robustness. Robustness always matters more than privacy in these kinds of systems. You have to have some kind of backup plan.

If you see that the fluff phase has started and you receive a message in fluff phase then you cancel your

I titled this slide incorrectly so apologies for that.

Remember we talked about changing your routes so periodically are going to change your Dandelion outbound edge.

One key question that I believe came up when the Bitcoin core team started thinking about what it would take to actually deploy this is, what happens if you change your route but you already sent some transactions on the first path and then you have some dependent transactions that you're sending on the second path of a new path. What do you do then? You’ve created a big mess.

The solution that we were thinking about was to retransmit the older earlier transactions on the new path as well which seems to solve the problem. But then there's this nasty little problem of RBF, reduced by fee. Even if you send the updated fee down the new path there are some nodes on the old path that still have the old fee. My understanding is that this is one of the big roadblocks at the moment and I would love to talk about this with yall more later. In practice even though the protocol seems really simple it turned out to be more complex than we expected when we first were designing this.

A final practical challenge that we looked at in our Dandelion++ paper is that in practice you're not going to be able to get everyone to deploy on day one. Practically you're going to have some subset of nodes that are maybe early adopters and then gradually more people will adapt going on. So it's really important when you're designing these kinds of protocols to make sure that everything is backwards compatible and that if you deploy something it's not going to break privacy for the other people or break robustness for the other people. That's partially why we implemented in our reference implementation the flag in the way we did so that it won't break nodes that are not running Dandelion. They'll just view it as another transaction that they should test.

We also did some analysis on the privacy guarantees and showed that as the fraction of honest nodes adopting Dandelion rose from zero to one, an upper bound on your expected recall also gets closer and closer to your lower bound of “p”. Remember “p” was the recall that we expect to get for Dandelion. This has a nice property which is that it's kind of smoothly smooth degradation as fewer and fewer nodes actually adopt your protocol. Even if one node adopts it, they get some privacy benefit and as more nodes adopt it, you get more benefits, like a herd effect.

## End story

The end story seems to be that complexity and robustness for the trade-off between complexity and robustness seems to be a barrier. So unclear if it would get adopted. We would like to try to see if we can make something work. I would like to try to see if something can be made workable.

One thing that I've been thinking about in the last couple of months is Dandelion-lite. This is really just like a one hop version of Dandelion. So instead of having this random number of hops in your stem you just send it over one hop and then diffuse it to the second guy as a transaction. Send it over one hop and diffuse it. It turns out that this very simple scheme has somewhat similar privacy guarantees to regular Dandelion if you assume that the adversary knows the graph. If you assume that the adversary does not know the graph then old Dandelion still has stronger privacy guarantees. You're giving up something in terms of privacy but it's a much simpler scheme. One thing that is still missing from this is simulations we’d like to run, so if anyone’s interested in talking to me about that.

Here with this one hop you don't know if you're receiving a diffusion message or a stem message. You basically include no flag, nothing. That's the difference. You might still think of it as a dedicated connection but you won't set a flag or anything. If I connect to you, you wouldn't know that you're my Dandelion connection.

Here's how it would work: I draw some random delay, I send it to you, and then as soon as my delay timer ticks then I start diffusing. If you decide to drop it I'm still broadcasting it. If you don't decide to drop it I get some small (inaudible). Here's one naive thing that you could do: you could say I'm only going to connect two nodes that are running Dandelion. Now what's the adversary gonna do? I'm gonna say I'm running Dandelion connect to me! So this blue curve is what happens if you do this announcement or if you try to only connect to Dandelion notes and the adversary is basically lying and they're saying that we're running Dandelion and nobody else is. Then you're going to get deanonymized 100% of the time we're close to it.

This pink region is what happens if you just make your connections independently. You don't care if they support Dandelion. If they do support the Dandelion then they'll relay it. If they don't support it and they'll just diffuse it (inaudible). This clearly seems to be the better operating protocol. In all of our analysis we assume that the adversary knows which nodes are running Dandelion. We already abstracted away that inference.

I wanted to close off with this interesting thought which came out of Princeton in 2017 by Narayanan and Moser. This is showing you a bunch of privacy technologies that have emerged in the blockchain space. Here on the horizontal axis we have the date of invention and on the vertical axis we have the strength of guarantees ranging from obfuscation to cryptographic. Obviously this is not a precise scale but they've ranked different protocols in terms of what the strength of their guarantees are. What's interesting about this is they've colored the different approaches based on whether they are used in Bitcoin, so that's orange, used in Altcoins is blue, these ones up top and gray is not used at all.

What’s kind of fascinating about this is that none of the cryptographic approaches are actually used in Bitcoin. Actually this might be a little bit out of date. Maybe some of these gray ones are used now. But the way I read this was that a lot of the cryptographic approaches are complex. They're a little bit too complex to actually get adopted; it takes too much overhead. I would love to hear perspective from the people actually developing this.

Our objective in this work was to try to work in the obfuscation territory but try to max out your privacy guarantees within those constraints. So far we've had interest from a few different venues. Dandelion’s currently implemented in Grin and Beam which are two privacy focused altcoins.

Bitmessage is a peer-to-peer messaging service that is supposed to protect your privacy. So Dandelion isn't really cryptocurrency specific, it's more like a one to all messaging service and so the way Bitmessage works is by broadcasting messages to everyone, so this was kind of aN oddly good fit.

## Take-home messages

That wraps up this presentation. Three take-home messages talk one is the bitcoin’s peer-to-peer network has kind of poor anonymity guarantees because of the randomization and the way that transactions propagate. So moving from trickle to diffusion didn't help so here there's a star here that actually IT did help because it was closing down this important bug. This is more from the perspective of like the theoretical analysis that we did. And third Dandelion may be a lightweight solution for certain classes of adversaries. I want to highlight here again that the adversarial models that we're considering are a really aggregate scale for parties that are trying to denormalize lots of parties. The tool is really not designed to protect against targeted attacks.

With that, thank you for your time and I'll take any more questions.

There were a lot of issues where, not just DOS, but like when we actually started trying to implement this, a lot of people from the Bitcoin Core team were bringing up ways that an adversary could potentially try to probe whether a node has a transaction in Dandelion mode. That led to a lot of additional complexity. At some point we were keeping like procurement pools, Dandelion mempools and which seems like it may not be feasible in the long term. There's a lot of DOS protections and making this compatible with all of them is I think tricky. That’s something that I don’t think we’ve fully figured out yet.

My understanding, which could be off, is that Erlay sends transactions along your outbound edges normally and with respect to the inbound edges does this second (inaudible). Is that correct? Notice that in Dandelion you're really only relaying on your outbound edges. That is completely compatible with Erlay because Erlay is only doing something different with respect to inbound edges. One is efficiency, one is privacy. I think what this would look like is you would do Dandelion for like some number of hops, whatever that ends up being until you enter the diffusion phase and then once you enter diffusion then you just basically do Erlay.

Questions? Okay, thanks guys!
