---
title: Cross Chain Deals And Adversarial Commerce
transcript_by: Bryan Bishop
speakers:
  - Maurice Herlihy
---
-- Disclaimer --
1.  These are unpaid transcriptions, performed in real-time and in-person during the actual source presentation. Due to personal time constraints they are usually not reviewed against the source material once published. Errors are possible. If the original author/speaker or anyone else finds errors of substance, please email me at kanzure@gmail.com for corrections.

2.  I sometimes add annotations to the transcription text. These will always be denoted by a standard editor's note in parenthesis brackets ((like this)), or in a numbered footnote. I welcome feedback and discussion of these as well.
--/Disclaimer --

Cross-chain deals and adversarial commerce

Maurice Herlihy

This is joint work with Barbara Liskov and Liuba Shrira. It's going to appear next year.

# Introduction

As we have seen, the history of distributed computing can be caputred by people's ideas of what's a realistic or interesting adversary. They tend to have certain powers or limitations. Your job is to describe an algorithm that works no matter what an adversary does within his power. In classical distributed computing, we thought we had a formidable adversary but in retrospect it just looks cute. It can do things like varied timing, like messages can be late or out of order, or nodes can crash. Or messages can be lost entirely. You can mix and match each of these things and you can define an algorithm that does something useful, and this was kind of the limits of what we thought was interesting in old school distributed computing.

At the limit, we had byzantine failures where some small number of parties could misbehave in arbitrary ways. Mathematically, that makes sense. But really what we were thinking about was not so much that there were evil parties on the other side, but that the failure modes were too complex to bother with. So we just say, okay, three of the sensors on the airplane wing can come back with arbitrarily broken readings and let's just assume they are malicious to simplify things. But we weren't worried about actually malicious behavior.

But things have changed in this post-blockchain world. Now we have adversaries that are much more formidable than we need to be. These are usually adversaries that evil and dedicated. If anyone here is Russian, I am not implying that all hackers are Russian, I just like to use cryllic fonts. The kinds of attacks we see are much more subtle, like sidechannel attacks including Meltdown and Spectre. In blockchain world, there are subtle attacks on smart contracts. These are all kinds of things that nobody really worried about in classical distributed computing and they were too messy and complex, but they have real consequences today.

The problems we're trying to solve are actually much harder. Instead of worrying about how to solve abstract problems like consensus, we're trying to build a distributed economy. What I am going to talk about here is what it means for distributed computations to be correct in a post-blockchain world. That is, classical distributed computing had a clear idea for what it meant for distributed computation to be correct, but I am going to argue that these definitions don't make sense anymore. They are a good launching point, but they don't extend to today's world.

# Adversarial conference

Let me give you an example of adversarial commerce. Bob owns a theater and produces tickets. Carol is out there and willing to pay for tickets. They can't find each other. So Alice is the ticket broker and she decides that she is going to make a deal among these parties. The thing to remember is that three of them don't really know each other. They found each other on Craigslist. If something goes wrong, there is little or no legal recourse and they can't sue each other. The deal we want to setup is that Carol sends 101 coins of some kind to Alice the broker and says I would like some tickets please. Alice then breaks these coins up and forwards 100 of them to Bob. Bob then sends the tickets back to Alice and then Alice sends the tickets to Carol.

This is what we want done; but that's not how you will do it because in the naieve way it's clear that anyone can grab the tickets or the money and run away. We're clear what we don't want to have happen at the end of this. I want to stop nad mention for those of you who are blockchain afficiandos, this is not the same as a cross-chain swap. There's a lot of work on atomic cross-chain swaps. We had to struggle to convince the referees that this is not a cross-chain swap. This is a different kind of transaction.

Alice is using Carol's money to pay Bob. This happens a lot in commerce. You sell things before you actually own them. Doing commerce with other people's money is a part of capitalism. You can't reduce this to a swap. Carol might pay and not get her tickets. Alice, if something breaks, might end up holding coins or tickets that she doesn't want. As a public broker, she's worried about her reputation so she has to figure out how to do refunds and these are all things that we would prefer to never happen.

# Cross-chain deal

This gives us a notion of a cross-chain deal. This is like a distributed atomic transaction but with important differences. Ecah party has some assets they want to trade. Multi-step transfers are OK. In the ticket brokering example where Alice takes money from one party and forwards it to another. Each asset lives on its own database or blockchain. I'll be describing this in the language of blockchain, but it's independent of hta ttehnology, we assume there's a tamper-proof and live underlying thing like a database or a blockchain. We're interested in high level notions of correctness; what do you want out of these mechanisms? This is independnet of any particular blockchain tech. Also, nobody trusts each other. But what do we mean when we say nobody trusts each other? I'll get to that in a minute.

This looks a lot like a distributed transaction, we'll see it is different from cross-chain atomic swaps.

# Correctness

I want to rethink correctness from classical distributed computing to the post-blockchain world. Traditionally, people talk about ACID: atomicity, consistency, isolation and durability. These notions don't hold up under rigorous scrutiny, but they are heavily embedded in the distributed systems world. There are some rough edges when we focus on these things, but they aren't my fault.

I'm going to explain what each of these terms mean as we go along, but the point I wanted to raise is that these properties don't really make sense in their classical terms in a post-blockchain world where we have autonomous parties that don't trust each other that want to cooperate for mutual benefit but since you don't trust anyone and know what their objective function is, you have to be very careful.

First, let me talk about the failure model. The literature is full of nuanced and subtle models. Dahlia gave us yet another one today. These models are great in their contexts, but these models don't really work in the context I'm going to talk about here. If you organize three or four people for a deal on Craigslist--- this is post-blockchain, nobody knows who you are. If you get some people from Craigslist, it's naieve to assume that some fraction or any of them are honest. Assuming there's a bound on who is honest and dishonest doesn't make sense in the context of distributed post-blockchain adversarial commerce. We have to assume that everyone is potentially dishonest, and we have to assume that they are all collaborating with one other. It's like one of those movies where everyone except one is colluding against the other, like the Roger Sten movies.

Conforming parties follow the protocol. Say I suggest a protocol and this is what we should do. If you're a conforming party, you are loyal to the protocol and you do what it says. If you're not, then you are a deviating party, and deviating parties might do anything. We don't care what the motivations are; they might be rational and trying to steal your money, or they might be irrational and maybe they are griefing everyone like maybe they are a foreign agent or acting in their own interest. Anyway, either you follow the protocol or you don't. That's the only model we need.

There's a lot of subtle nuanced models out there-- you can be faulty, altruistic, rational, you can be byzantine... we don't use that. All we say is that you either follow the protocol or you don't. If you don't follow the protocol, you can do anything. You can do things that give you an advantage, you can hurt yourself, you can hurt others. Conforming versus deviating is all that we care about.

# ACID: Atomicity

Let's revisit the ACID properties and let's talk about how each of them needs to be changed to adapt to this more demanding post-blockchain model. Classical atomicity says that you setup a transaction and either everything happens or nothing happens. If it doesn't happen, then we rollback and restore the world's previous state. But this doesn't work in a model where the participants are autonomous and you can't dictate to what to do, you can only ask them to do something. To take a simple example, suppose a deviating party makes an incompetent attempt to cheat and it gets caught and confiscated and the proceeds are given to the rest of the parties. Most systems will consider that a perfectly acceptable correct outcome when that happens, but that doesn't correspond to classical atomicity because it's neither "all" nor is it "nothing" and yet it's okay. So these very simplistic ideas that maybe everything happens or it doesn't, then that doesn't make sense in a world where we can't control or dictate what participants do.

Instead, we want to split into a liveness property and a safety property. Liveness is that if everyone conforms, the deal goes through. Safety says that in the presence of deviating parties, no conforming party ends up worse off. Defining what worse off means is going to require some careful phrasing and some undergraduate level game theory, but your intuition is probably perfectly okay for realizing this. You can't cheat a conforming party. You might have to rollback everything and you might waste some time and pay some fees, but they aren't going to confiscate your retirement account if this happens.

# ACID: Consistency

Consistency is a weird property in ACID world. It's an applications-specific constraints have to be respected. If you start in a consistent state, you end up in a consistent state. What we want is we want to extend this to the----- we want a strong nash equilibrium where everyone by default follows some strategy.  But suppose someone is going to secretly collude and cheat, it must not improve the payoff. So there's no motivation for any coalition of parties to deviate from the protocol in game theoretic terms; it doesn't mean they won't, because we don't necessarily assume everyone is rational, but if they were rational then they would follow the protocol. The analog for consistency, and this is a stretch, says, that if you propose a protocol then conforming to it should be a nash equilibrium then you should restrict your attention to protocols where conforming is a strong Nash equilibrium strategy. As an example, here's a generalized swap digraph. Everyone has a resource they want to trade with someone else, and we want all the transactions to go through. There's a theorem we can prove that says this structure is a strong Nash equilibrium if and only if it's a strongly connected graph, where every node is connected to ever yother node, and if not, then there's some subgraph that absorbs everything and the parties on the boundary has an incentive to ignore the free rider subgraph. So you only trade with people with which you are strongly connected, and you ignore everything else.

# ACID: Isolation

Isolation is a classic property that says that no transaction sees another's intermediate states. This gives us serializability, snapshot consistency, this whole set of classical correctness conditions: you don't have to care about interleavings, you can treat the world as if it is serial. From an engineering point fo view, we give you conforamcne but as far as semantics go, you can't see it.

Serializability doesn't make sense in post-blockchain world because if you look at atomic swaps and other protocols for doing cross-chain deals, they are all multi-step protocols where one party will post a smart contract, the other party will inspect it and propose their own smart contract, then someone releases a secret that's sent to a hashc ode, and there's many cautious steps that everyone takes because you're worried you will be cheated so you move the chess pieces around to setup the deal. Serializability doesn't make sense here.

Instead, we want another kind of isolation. To make a deal with someone, you want to put the assets into an escrow controlled by a smart contract before you believe I am going to cough up the goods. This is the analog of locks in a distributed system. This is the only kind of synchronization that matters. We are both going to put our assets in a contract escrow, we exchange data, the contracts trigger, and then we exchange the goods.

Safety says that I can't promise you something and then take it away. But if I put something in escrow, it's really locked and I can't control it. Liveness says, I can't lock things up forever, especially in the face of arbitrarily malicious behavior of my counterparties. There's no way for you trick me into locking things up forever. Unfortunately in some protocols you can trick them into locking up assets for a very long time, though.

# ACID: Durability

The other property is durability, and this is the easiest one to talk about. It says that in the classical world, we write things to disk before we commit. That's a world where everything but disk was non-volatile. Committed transactions survive crashes. Before you fire a missile or do anything that can't be rolled back, you make sure you record everything on stable non-volatile storage. But in the post-blockchain world, that's true, but our notion of things that threaten permenance are much more involved and sophisticated. We're not worried about our core memory losing power, we're worried about governance censorship or censorship by evil corporations or evil hackers or all kinds of bad actors. This is where replication and hashes come in, in the blockchain world.

# Rethinking trust

You might have a distributed implementation, but still the notion of trust isn't articulated in a clear way. It usually came in through the notion of fault tolerance. We trust that when a server crashes, it only crashes, it doesn't go rogue. We trust that a majority of servers stay up, and we trust that no more than 1/3rd of our servers go rogue. In order to talk about high level correctness conditions for the post-blockchain economic world, we need to talk about trust explicitly and we need to have much cruder models than the ones we have been focusing on. I think the one about conforming to the protocol or you deviant arbitrairly, and no limit to the number of participants of deviations.... we need to re-think trust and how we do data management and storage.

# Conclusion

In particular, I took the "ACID" properties which are the gold standard for distributed transactions, even systems that don't support transactions, they always talk about how they deviate from the ACID properties when they try to explain what they do..... this fundamental pillar of distributed computing has to be re-thought if we want to deal with the post-blockchain economic world. Here, I suggested a few things.

There's a lot of things missing; I haven't talked about how to map this on to synchronous and asynchronous and semi-synchronous. But I want to leave you with the idea that we need to think carefully about what we want our systems to do, in addition to how we want them to do that.


