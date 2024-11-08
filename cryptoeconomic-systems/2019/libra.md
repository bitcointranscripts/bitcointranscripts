---
title: Libra
transcript_by: Bryan Bishop
speakers:
  - Dahlia Malkhi
---
-- Disclaimer --
1.  These are unpaid transcriptions, performed in real-time and in-person during the actual source presentation. Due to personal time constraints they are usually not reviewed against the source material once published. Errors are possible. If the original author/speaker or anyone else finds errors of substance, please email me at kanzure@gmail.com for corrections.

2.  I sometimes add annotations to the transcription text. These will always be denoted by a standard editor's note in parenthesis brackets ((like this)), or in a numbered footnote. I welcome feedback and discussion of these as well.
--/Disclaimer --

BFT meets flexibility

Dahlia Malkhi

# Introduction

The technology we're all interested in here, does matter in very significant ways, whether it will be Libra or something else, or whether it will be both or all of them together, we're changing the fabric of society, money and financial services and the whole world. It will happen. It might take longer, there might be some hurdles, but it will happen.

The other reason I'm super excited to talk about it is that at the heart of tech disruption is the idea of decentralized algorithms and consensus. In the news last week, forming an agreemnet for consensus can be a little more difficult than we think. It's a tough technical problem and a very exciting and fascinating one to work on.

This is David Markus head of Libra testifying in front of Congress. Out of curiosity, how many in this audience watched any part of this testimony on youtube? How many of you noticed a Congressman ask him, so a Libra Association will make decisions by a quorum of 2/3rds? Did you jump and say 2/3rds plus one? I think this is pretty cool when a Congress person talks about quorums, consensus and 2/3rds and all of this. This is amazing. This is an amazing time. These algorithms and these technologies we're working on are really the focus of interest and fascination and a lot of curiosity and openness in the world to understand them and to bring understanding to how this will change financial services.

# History

This started 4 decades ago with Leslie Lamport and the book "Concurrency: The works of Leslie Lamport". These were the foundations for thinking about these problems, the pillars, the concepts, the terminology, and possibilities and the early solutions for addressing this fundamental problem of executing distributed software correctly and consistently. This slide is a shameless brag of a book about to come out, going live on the ACM Digital Library next week. I'm allowing myself to put this up; I was really only the editor. The content was written by wonderful contributors. A lot of the early concepts and terms and fundamental pillars of this field of concurrency, things like byzantine failures, paxos, some of the other solutions are discussed in the retrospect of history.

Now these founders invented, and coined, all of this field, to solve very different problems than the ones we are talking about today. They looked at a system of four computers in a mission critical setting like the cockpit of a space shuttle and they needed a resilient control system.

Bitcoin was the one that showed a more scalable and global use case for byzantine fault tolerance. As we know, the solution they gave does not solve byzantine fault tolerance. So this caused a renewed interest in the classic way of solving byzantine fault tolerance. This unlocked originality, innovation and some fascinating results in technology.

Here's an example of-- on some of the ways that innovation has been accelerated. In 1982, there was PLS and Byzantine Generals problem. Then in 1988 there was DLS, then in 1999 there was PBFT, then in 2007 Zyzzyva, and 2016 was Tendermint and Caspser, and then 2017 was "Revisitng fast....", and then 2017 was SBFT, and then 2018 was HotStuff. There was a quest for achieving linear solutions, linearity means that you don't pay fundamentally more than you would have to pay to spread the decision itself. Getting agreements and the solutions, just about that, was the quest for about two decades, the first of which is one that I will call the decade of confusion where the community as a whole went down the wrong track for a decade which we then showed was flawed. In the past few years, there was accelerated innovation and they fixed those problems and came up with the final result which a lot of blockchains are now basing on including our own technology at Libra which is finally providing the linearty solution.

This is an example of a use case for scalability and strong tech has driven a lot of research and innovation and some fascinating technology in this area.

# Libra

We're building Libra. It's a technology that I want to provide global currency for everyone to use and for everyone to access. Libra is going to be a very different type of digital technology. It is built on an engine that decentralizes trust. It's also different in some other ways in the way that the market is designed and the stability of the currency is going to be managed by Facebook Association. I want to talk about the tech underlying Libra; it's a database of programmable resources replicated using the power of decentralized algorithms with byzantine fault tolerance.

We announced that at launch date, this technology will be deployed among a set of permissioned participants. The founding members of the Libra Association. Down the line, we will open it for participation using state and other methods.

I want to spend one slide to talk about the technology that Libra is delivering, and then switch back to technical areas. Calibra is the company that Facebook has established to build a product which is a custodial wallet that allows payments and transactions with the Libra Coin. Libra is a blockchain, an open technology governed by the Libra Association with multiple members. We announced it with 28, and at launch date we want 100 members. An analogy is that Libra is the highway, and Calibra is one of the many cars driving on this highway. Libra is open for other applications and services to be built on top of our platform.

# Beyond classical approaches to consensus protocols

When you build such a serious technology with the potential of changing society, and the potential of reaching global reach, what do we worry about and what keeps us up at night? What do we want to work on technically? I am going to talk about some of the questions we raised for going beyond current byzantine fault tolerance. I want the community to think about some of the difficult problems we had there.

The classical approach to BFT, using experts such as myself and many of the other experts in this room... you start with some of the theoretical underpinnings of the field. Is the network going to be synchronous or asynchronous? Are we going to rely on a synchrony assumption? If yes, then we can tolerate up to 1/2 of the participants going rogue. In partial synchrony, then we can only tolerate at most 1/3rd. This is denoted as delta in the manuscripts. Once we have this, we can go to the literature and survey the myriad number of solutions out there. We can then go find the best consensus protocols, so we might choose PBFT tolerating 1/3rd byzantine faults in a partially-synchronous setting. Then everyone needs to agree with the administrator's assumptions. This is the standard approach that we all follow, and how systems should be designed.

# Some questions

But why do we need something new? There's several opportunities I would like you to consider. Yes, there are rigorous and well understood bounds like 1/2 or 1/3rd byzantine falts. But the question is, is the model the right one? Is byzantine fault tolerance, is this really giving us the right analysis for the problem we're solving? If you think about it, again going back to the setting where we're launching the Libra blockchain, we're going to have a set of strong and credible industry leaders participating in the infrastructure and in the backend of these systems. Is it really reasonable to assume byzantine failures for these sets of members? These are members who run services 24/7 credibly, reliably, with 100% uptime for years. Is it really reasonable to assume that Facebook doesn't have 100% uptime?

The second question is, are we really going to design this system statically once with an administrator's design and assume it will stick forever? In particular, while running the systems, we might learn during runtime or its operation that various things are happening in the system. We can actually observe failures or network conditions that can change the way we model the system. So the question is, can we support multiple assumptions under the same deployed implementation and adapt it to varying conditions?

The third question, which keeps me up at night, what happens in the end when some assumption is violated? The current theory says throw your hands up in the air and give up. Liveness, safety, it all goes away. But can we do something if our assumptions get violated? And finally, what hapens if we lose the quorum and there's some disaster? Do we lose transactions and lose money? We're working on something very serious; this is not just academic.

I'm putting out these questions because I have some insights. We have some ideas.

# Beyond classical BFT

There have been academic work that has addressed some of these hard questions already. The first thing that people have done, sort of the obvious approach, they said well let's assume there are fewer byzantine failures, like not 1/3rd. The premise is that byzantine failures are the worst that can happen. But maybe we have one attacker in the system, but maybe we will have some faults that are just benign crashes or delayed or omitted packets.  So some works in this "hybrid fault" model--... I don't want to mention who was the first, because I don't want to accidentally miss someone. But these fault models assume that byzantine greater than everything; it's the worst type of failure that can happen.

But what I want to talk about briefly today are some advances that we worked on recently called flexible byzantine fault tolerance where we don't assume byzantine is the worst kind of failure. The last thing is, if you lose the quorum, can you still salvage the committed transactions that were in the network partition?

# Flexible BFT

This is joint work with Kartik Nayak and Ling Ren. This is also work that will appear in the coming ACM CCS 2019 conference in London. In a nut shell, flexible byzantine fault tolerance offers stronger resilience. With this new model, we can tolerate a higher number of corruption or malicious activity than any of the known lower bounds, both for synchronous and asynchronous system without breaking any impossibilities or violating known results. The second component is diversity: it allows at different times to conclude different things about the system using different points of views of learning about what has committed to the system. Depending on the assumptions and the observations, you can see different things.

The way this works is a new model where we introduce a new type of fault, called live but corrupt. Alive-but-corrupt faults assume that for the most part the participants in the infrastructure of a blockchain supporting a financial system, have interest in maintaining the system live and in collecting fees from it and in committing and following through with transactions. What they do, potentially have interest in, if they want to cheat, is in breaking the consistency. They might want to double spend the same coin, they might want to fork the system, but not to prevent the system from being live. So rather than saying byzantine is the biggest problem or worse than a crash fault, but I'm saying the other way aronud: there's no reason for the participants to stop being reliable, but there is an incentive if they are corrupt if they try to cheat. So alive-but-corrupt says the attacker wants to attack safety but not liveness. This is the opposite assumption of previous models. The total number of corruptions is the total number of byzantine, so it could be benign, faulty or corrupt. In this model, we can break away from all the known resilience bounds.

The second contribution has to do with this diverse point of view on the system. So in one protocol, one family of protocols, we're able to support learners with different assumptions. The same protocol, the same deployed system can support different points of views. In particular, learners can come and make their own decisions. The most surprising thing here is that the same system can support synchronous learners or asynchronous learners. There could be learners that want to be very safe against some htreshold like a third or more of corruptions, and against asynchrony, and other learners who have more patience and want to wait the maximum assumed network bounds until they get a higher level of assurance assuming these synchronous bounds.

The third contribution of this approach is that we can support recovery. If a resilience bound has been broken, then we can go back to the system and change our assumptions and pick the one that was correct under a stronger assumption.

Technically, flexible BFT has two components. There's a synchronous BFT protocol that despite using synchrony to guarantee safety, it advances without any explicit steps that delay the synchronous bound. This is an async protocol, and only when the learner looks to learn when a transaction was committed, applies assumptions about the synchronous bounds  and decides when to commit. Only when an external client of the system observes, only that one applies the synchrony assumptions on the system. The system doesn't wait 10 minutes or 10 seconds at all. This is a new protocol. If you think about your standard diagram of distributed protocols, synchronous protocols--- the stander one has synchronous periods and epochs that wait the maximum delay and then they advance from one synchronous round to another. Our new protocol will not have any of these synchronization epochs. The protocol will look completely asynchronous. It also happens to be the most simple protocol I can think about; it's very natural to get rid of the delay steps.

The second technical contribution is this notion of flexible byzantine quorum systems that uses the new "ABC" fault model described above. The fundamental threshold lower bounds that we have in this field, stem from the fact that we're using quorum systems that assume the same bound for liveness and for safety. So this notion of Q-- the size of the quorum that we need to drive a decision, and Q has to be small enough to guarantee that we can get messages from Q, so at most 1-Q fraction can be crash faulty. At the same time, the intersections between quorums is the one that guarantees safety. In our technique, Q can be much larger. Because we assume ABC faults aren't going to effect liveness. So we can wait for a much larger Q and liveness will be retained. The intersection we get has much higher resilience. This tension between safety and liveness is broken, and this allows us to bypass not to break, the resilience bounds.

What can we do with flexible BFT? A lot. Wonders. You can start running a system. If you observe P active participants, that you know could be corrupt but definitely haven't crashed, then what you can do is take away the p you see participating out of the resilience bound you assume for byzantine. If you assume a third--- so you assume 1/3rd minus p, could be byzantine, because I already have evidence from p that are active. They might be corrupt they might be trying to double spend, but they are definitely active and I can see messages from them. So you split the third threshold between corrupt and potentially crashed. The magic here is that you can now --- (1/3 - P) of this byzantine you don't know about, and you get the extra resilience of the P that you observed for free. So you can still have 1/3rd corruption plus the Ps you have observed. It's 1/3rd plus P corruption resilience.

What else can you do with flexible BFT? You can already use what you observe in the system to increase your assumption on failure thresholds at runtime. You can also if you observe participation that is corrupt, you can switch between synchronous and asynchronous. If you see evidence of corrupt participation, then you can then decide to step back and start operating in synchronous mode where your resilience can go as high as 1/2. Whereas before, you can operate in async mode and move more quickly. But vice versa; if you have operation in synchronous to have high resilience, but you notice the network has transient instability and message delay, you can switch to asynchronous mode. You can also recover from forking once you see that your assumption was broken, and you can use the transcript of the existing protocol.

You can also perform periodic safety checkpoints on the system. You can wait every 1000 transactions for more messages in the system to arrive, maybe in retrospect, and you get safe checkpoints. You can differentiate between--- transactions that are payments for coffee at Starbucks which don't require high assurance, as opposed to transactions where you're selling a house for a million dollars and you want to wait for high assurance on those transactions.

So you get a flexible space of guarantees. What this chart shows is the fraction of byzantine faults on the x axis, as opposed to the fraction of total corruptions..... the area under the curve is impossible because you can't have total number of faults less than byzantine, but you have the boundary of the grey area... where... you are getting the green area for synchronous assumptions, and this orange area is for asynchronous assumptions. All of these combinations of corruption and byzantine fault tolerance are possible.

# Calibra Research

I am here to talk to you, I'm coming out of Calibra Research. We have a strong interest in advancing the technology of cryptoeconomic and blockchain systems. We're doing a lot of research. We're hiring. If you have interns, students, or postdocs interested in a career advancing this technology, then please contact us. Thank you.


