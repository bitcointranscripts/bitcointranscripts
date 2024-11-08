---
title: Roundgroup Roundup 1
transcript_by: Bryan Bishop
speakers:
  - Bram Cohen
---
Roundtable roundup review 1

# Future of SPV Technology

So hopefully I summarized this reasonably. There were a number of things that came up in our discussion. It would help SPV a lot if there were UTXO commitments in blocks. This can be done with a soft-fork. It has implementation cost difficulties. There are some ugly things you could do about how the trees are formed, so that you don't have to repopulate the whole thing every single block. There might be some happy place where the complexity of code and the difficulty of doing this and the complexity of doing the lookups are only modestly ugly. More work should be done there.

There should be a SPV implementation in Bitcoin Core which leads to not a clear leading reference that has good behavior. SPV clients should in general should talk to 1000s of nodes or even more. They should talk to hundreds of them because there's no actual big cost in doing so, the main one is whoever claims to have the largest chain and you can easily verify that from them.

SPV clients should maybe not do fee estimation, perhaps payment channels will interact with SPV in the future.

Bloom filter requests in SPV are broken and busted and have denial of service attack problems. It would be nice to have a private information retrieval protocol that would be more expensive but give you the privacy that it claims unlike the bloom filters which don't.

# Network propagation

Rusty Russell

Please propagate forward.

There was a lot of discussion about physical topology of networks, routing, overlay networks, but it was made very cloear that block propagation is the key focus for miners. There was a lot of speculation about how that would look, adding physical routing to the network. There was some discussion around that, but perhaps not many major conclusions, except that if bitcoind doesn't do it really really well, then miners will do it themselves. We also discussed IBLT. There were some interesting interest in doing weak blocks or near blocks. Because they tend to be very similar to final blocks, and final blocks are usually similar to weak blocks. This should be fairly easy to implement, unlike IBLT. Also general cleanups in networking code, which will lift our gain a bit there, and open some potential to doing smarter things like small nodes.

Most fascinatingly, 1 BTC is about equivalent to 7000 tons of water if you are operating a hydrodam.

# Involving academia

We talked a lot about publishing and how academics are judged by perhaps mysterious criteria if you haven't been a phd student. There's a standard top tier of journals. There's starting to be a small number of bitcoin papers per year. There's a lot of pressure to send my best ideas to there and impress clever computer about how clever that bitcoin stuff is, even if there's not many bitcoin people there. Then there's a hierarchy of second tier conferences. Then there's the bitcoin workshop, or Financial Crypto, or the Ledger journal as a special thing. Unfortunately that's not viewed as the same way, and academics don't get nearly as much career credit. That's a much better way to get your ideas out to the bitcoin community, but doesn't give you career brownie points. Perhaps we should take research from top tier research journals, and extract them and try to get information going down that way. And also some way to get cool research from bitcoiners from non-academics, who don't have incentives to write up long references and long papers, and perhaps get some of those ideas exposed to the crypto crowd to get them more interested in bitcoin. There's been some progress here in computer security. We've had more survey papers about what the interesting problems are, we could try to write more about what the open problems are and pose them in a good way to make sure that academics are solving the right problem. Surveys could help say that the community identified a problem. Would be great if more game theory and economics people were looking at bitcoin more. We need a repository where educators could put notes. Here's how IBLTs work, here's a pset on this, actual resources but people implementing it and trying to learn more. More outreach to undergraduates. Funding would be nice. The best way to convince academics to work on your problems is by convincing grant bodies about it, because then academics will get grants and then pay grad students to work on it. NSF is already funding some bitcoin stuff, but other academic funding bodies would be nice.

# Trustless UX and human crypto interaction

Paige Peterson

In terms of talking to users, in terms like vulnerability and dependency, to make things more clear. We also questioned a lot about whether users care about trustlessness and security, and how to change that mindset. A lot of the situations where people or basic users are going to appreciate the security that bitcoin brings, is centralized systems failing and seeing the examples of trusted systems just not working. It comes down to a mindset perspective shift. Security should be the default option, but it goes back to if given the option to have a quicker transaction or something like that, are users going to sacrifice their security? And how much to tell the user about cryptography and the security? How much should be relayed to the user, and how much do they even care about that? Does there need to be a more concrete relationship between designers and developers? Create positive feedback loops for funding this software. There is an incentive to centralize your application if you're going to be able to get more funding because users are more dependent on you. There should be more incentives for funding in a distributed manner.

What is the UX problem? It is different for different people in different situations. People having internet access. Is it problematic that you need to use cash for buying coffee? Where are the actual pain points that we should be focusing on? And then expand on user friendliness for less important things later on.

# Threat models and boogeymen

Andrew Poelstra

We talked about various threat models against bitcoin. We talked about threats to bitcoin from other systems. And threats to other systems from bitcoin. Consensus, fungibility, and selective rule enforcement. There were threats towards bitcoin from miners. Miners are the only part of bitcoin that involve a human element of trust. So we worried about if miners could collude or become centralized, what are the risks? One of them is that miners can cause consensus failure, and they might be coerced into doing this for example if there was political or other pressure on them to reverse transactions, you might have a situation where miners would be forced to rewrite the blockchain. There is then risk of consensus failure, or miners might have to use different rules just by legal agreement. Second we talked about fungibility, which is that if miners are looking at the transactions they are mining, then there is a risk that they might concern some coins worth more than others. Miners might be tracking coins for AML reasons. Some coins might be worth more than others. Technically, all coins should be worth the same amount. We shouldn't need a patchwork of legal infrastructure to keep track of coin worth.

There needs to be a way to incentivize a more distributed use to avoid monopolies at every single level. Miner monopolies, our final concern was selective rule enforcement. Miners in certain geography may not be allowed to mine certain transactions. Perhaps more insidiuous is internal selective rule enforcement and this would be something where miners might start imposing rules that benefit them, like if they start demanding ridiculous fees. We didn't go into specific examples, we were keeping it really high level, the one interesting thing at the end of the discussion was that if the threat can end bitcoin, was that a threat or a complete failure. Where do you draw the line that it's a threat to bitcoin's future, or is that just a bitcoin failure?

Do we want to model threats that are so large that you can't possibly handle it anyway?

# Data collection

Distributed systems often get designed by gut feel, like how many neighbors to use? In many contexts, these numbers don't really matter. In bitcoin, these decisions have real monetary consequences. The real driving point for our us was that we should reason quantiatively, and we need better tools for that. What sorts of data to collect from the network?

Node configuration, how do people configure their nodes? Peer lists, the topology of the network is an important detail. Just like the internet is an emergent living organism, the bitcoin relay network is an important emergent organism and we should understand it. The orphan rate is something critical. That orphan rate reported on blockchain.info is misrepresentative, it's not correct.

Mempool size. Blockchain state, divergences and consensus forks. Transaction arrival, timestamped data, a lot of this data is not timestamped at the moment. There's a lot of exciting data at the blockchain going, shapes of transaction graphs.

The next question is that collecting data has privacy implications. There's a real worry that attackers might use this data to launch attacks, and maybe adapt on the fly and so on. Raw transaction logs could be used to triangulate the source of transactions and find users in the network.

It's possible to overcome some of these concerns. One can share one own's node configuration, perhaps not with their name attached, as long as that configuration data is not attached to an IP address, I would hope also that some other people would share this data in anonymized form.

Another idea was to snapshot the network, but snapshot it and reveal it 6 months later. That would be incredibly useful to researchers everywhere. Every node could do this at the same time.

Have a public repository for users to contribute data that they have collected. Miners and pools should generate and share their own data, with incentives perhaps. How do you make sure that people wont game it, and that the data is correct?

How many locations do the beacons need to be at? The next discussion was what do you do with these studies. How does the bitcoin price impact the network behavior? Can you tell what the bitcoin price is based on the network behavior? Probably not for long.

Where are orphan rates going? Anomaly and attack detection. It's also useful for online attack detection. Where are the denial of service attacks coming from? Being able to quantify normal behavior versus bad behavior would be very useful for miners, which are sensitive to network health. At the moment they are using informal channels for this between different mining cartels.

What happens when there are 1 billion bitcoin users? Feasibility of different protocol changes, economic simulation, etc. We talked about the impact of collecting data, can people misuse this information. Do you restrict it to a closed set? The similarities to internet measurement also showed up. On the early internet, they had to use weird hacks to collect information from DNS servers. It would be nice if there was something that supported this. Network operators were willingly pooling their data. The ideal here is to build in some measurements into the protocol implementation itself.

There are some innovative ways to collect information, a geographically distributed relay network, use an opt-in tracer transaction technique, or using a bitcoin measurement body like IETF RG. Finally we tried to identify patterns of transaction, and get off-chain activity as well. It could move on the chain, or stuff on the chain could move off as well. And it would be good to get a handle on this.

We would like to urge the core developers to keep measurement off. The natural evolution of most systems is to restrict information over time. The ability to crawl the network might disappear in the future. This is a space where the protocols are under-researched and the next level of changes to be applied to the protocol need to be well-informed, which is impossible without data.

# Mathematical modeling

Bram Cohen

There's doing simulations and emulations, differential equations with pencil-and-paper. Mobile process calculus which you can find out by searching for pycalculus and it's useful for concurrent process analysis. There's some stuff for mining incentives, there's an unfortunate lack of modeling of peer selection algorithms resulting in network segregation or not, they seem not to but who knows. High-level models are easier when you make simplifying assumptions, which you can sometimes do. Bitcoin is hard to analyze because it's a large monolithic protocol, even if you modularize it internally, it's really a big monolithic interconnected thing.  Proof-of-stake are even harder to analyze, and they have the retroactive go back to where you have 50% problem.

# Miner-developer relations

Matt Corallo

How can we improve conversations between miners and developers? We focused largely on dealing with immediate alerts about something is broken and something needs to be fixed immediately and make sure the messages come from the right people. Who's allowed to send messages directly to mining operators? How do we filter that list? We had a much longer discussion about what kind of mechanisms and how should these messages look. We talked about the existing alert system and how it's going away. We talked about how existing miners have networks designed and which points we can inject messages that will get to them very quickly.

And then we moved on to maintaining good working relationships between miners and developers. How do we have regular basis meetings? How do we have non-emergency communication? How can we get people to use the mining mailing list? How can we talk with them in general, about Bitcoin Core announcements? Or things that miners should be aware of?

Why are we at Montreal at all? What are the block size issues? Why are we having these discussions? It's important to have these discussions between miners and developers because these discussions have not already taken place. We had a brief discussion about exactly why the block size is still a contentious issue and why we're in Montreal and what everyone should be trying to take out from Montreal.

# Scalability and hosted infrastructure

We very well represented by bitcoin infrastructure companies. I wont give the names. We had a good number of hosted wallet providers, as well as API providers. The major takeaways were that people, of this group, universally agreed with increasing the block size which is interesting to me, because it's a hard-fork to bitcoin. It's weird that they agreed to hard-fork bitcoin. There was an interesting point about it's not just about changing the block size, it's about proving to the world that somehow bitcoin can govern itself so that people don't have to be afraid that when critical issues arise we can resolve this somehow.

We talked about things like the difficulty that the stress test has caused wallets right now. The wallets are unsure how to calculate fees, so some people talked about making looking at the code in Bitcoin Core for how to calculate fees correctly, whatever that means. But still lots of wallets have had difficulty with this. Another interesting thing to me was that a number of infrastructure companies don't run Bitcoin Core. They run completely different implementations of bitcoin. I thought that was very interesting.

There was concern about cost and concern about this spamming attack- this "stress test"- there was higher cost to the infrastructure companies. There was major cost impacts. And then customers get grumpy, and then the API companies have to devote engineers to this.

# Pathways to adopting better cryptography

Andrew Poelstra

We talked mostly about new cryptography that could be used in bitcoin for better scaling. Most of the stuff we can soft-fork in an unexciting way. Where can we improve scaling? The first thing we talked about was looking at digital signature validation. That's a huge part of validating blocks and the initial block download. We can work on that concretely and we have been doing that in Bitcoin Core. We talked about some boring algebraic improvements, and suppose you could replace the ECDSA signature algorithm with EC Schnorr signatures. It's functionally identical to ECDSA, but the algorithm does not involve division. A critical thing this enables is n-of-n multisignature, where all parties are required to sign. To create such a tihng, there's a large script required. You need a 10x script size to get a 10-of-10 bitcoin script at the moment. A standard single signer signature looks the same as the 10-of-10 signature for Schnorr signatures. We can extend this from n-of-n to m-of-n where there are different values. We do this in a cheap way where we reduce it to n-of-n, like if I was going to do a 5-of-10 multisignature, then I publish a public key eequivalent to what 5 pick 10, we can get some space savings by putting all the possibilities into a merkle tree, then reveal only the path that actually gets used. There are very expressive multisiganture that is only logarithmic in size with the number of possibilities, which is much better than today's OP\_CHECKMULTISIG today.

Schnorr signatures also allow batch validation. We have some ideas where if it was possible to change bitcoin script so that checksigs were not allowed to fail, so we can only have checksigverify, then we can run through all the script validations for a block, and make sure all the transactions succeed, so we first make sure the signatures are okay, then we take all of the signatures in the block and make sure everything works. In schnorr signatures we can combine them all algebraically, then do a single validation, and this is a 50% speedup versus individually verifying all the signatures. That's just from fairly simple algebraic tricks.

What about instead of just having different branches for merkle trees, what about extending this to the whole script? Where you have an IF statement in the script, what about if you take all the pathways for the execution of the script and put those in the merkle script, and rather than publishing the whole thing, you only publish the scriptpiubkey as just the merkleroot of your script, and it only reveals the pathway that is actually taken. You no longer have to reveal the entire script. The standard execution is very narrow and efficient in some cases, and then there's like someone dropping out and then an expiring locktime, well if these bad events don't happen then you only reveal the nice case which is very simple. You could have complicated recovery scripts where the blockchain does not have to bare the complexity of this.

We talked briefly about quantum-resistant cryptography using lamport signatures rather than ECDSA which would be a huge size hit, of like, 100x or more size increase in the size of our signatures but potentially faster verification assuming we had SNARKs which is compact verifiable computing, which we talked about earlier in earlier talks, we could eliminate all of the blockchain data and just provide proof that it was all correct. Lamport signatures and using hash-based signatures would be faster in that case, instead of using ECDSA. There is weird situations where usually Lamport signatures are very bad ideas for scalability, but if we had other magic crypto then suddenly they are a good idea again.

We talked also about UTXO commitments in blocks and various tradeoffs in that.

# Privacy and scalability

zooko

Privacy is related to censorship resistance and fungibility. Censoring someone because it's usually cheaper to do that, rather than punishing them for having said it. Privacy is the weak-link. Fungibility means that all money is created equal and trades at face value. There were a whole bunch of people at this roundtable, which I thought was cool, because bitcoin is terrible at privacy. But at the social layer, almost everyone agrees that privacy is extremely important. We talked about three specific technologies, one is lightning network with onion routing attached, another one was coinjoin + confidential transactions, and the third was zerocash with SNARKs like Andrew Poelstra just mentioned. They have lots of tradeoffs.

We talked about how one measures or evaluates privacy. Most of the methods were rejected as not really useful. The one that we thought was potentially interesting was the qualitative practice of creating user stories, and whether their use in certain stereotyped patterns would betray them or not.

We agreed that privacy is more of a group property rather than individuals; it should be ubiqituous and the default setting if it's going to do any good. Someone mentioned that in their bitcoin company that when they are talking about potential privacy features, someone mentioned that the US banks were the most excited about that because they need privacy from their competitors. We often see privacy in terms of social terms, but lots of people need more business-oriented privacy.

Privacy is a really difficult problem, but this community is full of really smart people that care very strongly about privacy and so we're not going to give up.

# Potential for SHA-3-like competition processes for bitcoin

Our group discussed potential competitions and contests. SHA-3 contest was held by the US government for selecting a new hash standard. They had three stages. First they had a bunch of workshops, and then they looked at what their requirements are for the new hash function, and what it should be strong against. Once they did that, they published a set of requirements and then opened up the field to various people proposed hash functions, once they got the initial proposals in. Everyone evaluated them, different teams attacked the other teams' hash functions, and you found other people's problems in hash functions. It was epsecially productive in the cryptography community. Because it happened over a long period of time, people were able to set long-term research agendas, for example it started in 2004 and continued into 2011 when they selected Keccak as their SHA-3 standard. This could offer value bitcoin in the sense that this could produce legitimacy, having this nice discussion and having reasons and very formal well-thought-out logical manner could help these discussions and help everyone understand stuff, but it could also help the technology.

One of the questions was well with SHA-3 there was a committee for selecting which hash function should win, and this might be contentious in bitcoin. So there was some question for whether this was useful for solving contentious issues, and there was a bit of discussion around this and I don't think it was resolved. One thing that we generally seem to agree on is that it would be useful for non-contentious issue, and just because something isn't contentious doesn't mean it couldn't harm bitcoin. So what issues could help bitcoin and could prevent lots of problems? One of those we thought of was the p2p network, because you can run different p2p networks and relay networks without causing forks, it's independent of the blockchain consensus decisions. That might be less contentious.

Also we should approach non-contentious issues first, might be a good way to move to more contentious issues later. And then potentially having it on a longer time-scale like a few years to 10 years allows people to develop technologies that wouldn't have immediate applications but might have larger applications long-term. A lot of academics take a while to steer the ship, having a longer-term time frame might build confidence and get deeper longer-term research projects involved.

We also discussed that SHA-3 was a government project, so it had a lot of government resources. The cryptography community in Ceasar engaged in a similar competition in a shorter time-scale outside of government. Who would fund this?
