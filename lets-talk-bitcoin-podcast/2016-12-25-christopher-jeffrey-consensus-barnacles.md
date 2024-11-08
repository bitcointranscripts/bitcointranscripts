---
title: Consensus Barnacles
transcript_by: Michael Folkson
tags:
  - consensus-enforcement
date: 2016-12-25
speakers:
  - Christopher Jeffrey
episode: 319
media: https://letstalkbitcoin.com/blog/post/lets-talk-bitcoin-319-barnacles-of-consensus
---
SF Bitcoin Devs presentation on Bcoin: https://diyhpl.us/wiki/transcripts/sf-bitcoin-meetup/2016-09-28-christopher-jeffrey-bcoin/

Breaking Bitcoin presentation on consensus pitfalls: https://diyhpl.us/wiki/transcripts/breaking-bitcoin/2017/2017-09-10-christopher-jeffrey-consensus-pitfalls/

## History of Bcoin

Adam Levine (AL): JJ thanks for being here today.

Christopher Jeffrey (JJ): Thanks man. Glad to be here.

AL: We are going to jump right into it with the elephant in the room on all this stuff. Bcoin is effectively an alternative implementation of the Nakamoto client including consensus code. That is kind of a controversial thing. In theory there could be many popular implementations of the Bitcoin consensus. We have seen some attempts in the past that didn’t make so much of an impact on the ecosystem outside of being proof of concept. In practice the majority of users, whether they know it or not, are using that Core Nakamoto implementation for all the hard consensus stuff and then individual wallets or applications layer the more nuanced feature stuff on top of that. This is not what you have done with Bcoin. Purse.io seems like an unlikely company to take on the Core consensus code. I think a good place to start with this is if you could share the backstory on how Bcoin came about and what the project’s ambitions are, how Purse came to create this thing.

JJ: Bcoin actually started out as this tiny little SPV wallet that was made by my friend Fedor Indutny. A lot of people if you are into NodeJS might know him from there. He is one of the JS devs. He wrote it in I think 2014.

Stephanie Murphy (SM): To clarify, SPV is simplified payment verification.

JJ: Right this was specifically BIP 37 SPV. SPV is rather than validate the entire blockchain you only pay attention to transactions that are relevant to you. He wrote this thing and that point in history I was sort of into cryptocurrency but I didn’t really understand it. I didn’t understand what a block header was or what those headers meant or anything. I didn’t know how transaction verification worked. When Fedor made this thing, he hosted it on GitHub, I took a look at it. It was the first time I really understood Bitcoin. I could actually look at how a transaction verification worked and it was the aha moment, it finally clicked for me. I started contributing to it immediately. I always had aspirations to make it something more than just SPV but never really got around to it. Then I got hired by purse.io last year. We initially had ideas of doing some kind of 2-of-3 escrow, some kind of semi smart contracts, things like that and we wanted a platform to do that. We actually do hold your coins in escrow when you buy something on Purse. If we could do that on the blockchain that would be much better. Right now we just hold it internally, in our system, it is custodial control. We wanted to put it on the blockchain and make it a 2-of-3 where the third party would be the mediator, us, who would come in if there was a dispute. That is what I was hired to do at Purse. I was looking around for what tools I wanted to use for it and I was like “Maybe there is some way I can use this Bcoin library that I worked on before.” I didn’t think it would end up being such a large project. It ended up being a lot more work than I thought it would be. I ended up turning it into a full node over the course of the past year or so. That is where we are at right now.

AL: That seems like a big jump from the system that you guys were talking about creating. One of the projects that I’m working on with my company is actually very similar to that. It would use 2-of-2, an escrow system so you don’t have to have the custodial risk. We have done it with Bitcore. How did you guys wind up going from one of the existing alternatives to using this? Was it easier to build it all out fresh or were the particular reasons that made you turn to this type of approach?

JJ: Our focus shifted as I was working on this. I will give you an example. There are many moving parts in our stack. Webhook notifications from BlockCypher, we were switching back and forth between Gem and Bitcoin Core for the wallet. We had blockchain notifications, transaction notifications, we basically needed an API for all of Bitcoin. At this point I was still working with Bcoin and it wasn’t really production ready. Everyone is looking at me and we were having trouble with all these services. He said “Can we just hack this into Bcoin? Can we get something working?” I was like “Maybe”. I went for it and it eventually snowballed from there.

Andreas Antonopoulos (AA): It sounds like a case of monumental scope creep with a happy ending. I really love how you can have either the audacity or the complete lack of foresight as to how humongous a project like this can become. To not be discouraged by people around you and just embark on this crazy voyage. I think that’s how some of the best innovation happens. It is a great project.

JJ: It is always hard to explain how we got to this point exactly because it veered off. It snowballed and ended up being something completely different from what we initially set out to create.

## Bcoin in comparison to Core

AA: Let’s talk about where it ended up because I find this fascinating. Right now if you run any kind of Bitcoin service, any application, if you are building any kind of base infrastructure, up until now Bitcoin Core is it. Bitcoin Core is obviously the reference consensus code but it is not particularly suitable for large scale industrial resilient deployments within the kind of business applications you might need for APIs and things like that. I am not bashing Core, it is a phenomenal piece of software but it is not multithreaded, it is not very easy to access with various APIs. It has only recently had an event queue for notifications and more importantly it is a monolithic piece of code where if you want to run something you run everything in a single instance. That is very different from what Bcoin is. Bcoin is very modular, loosely coupled, event driven architecture which you can scale each component independently. Can you tell us a bit about how it ended up? I think as a piece of industrial level code for running in infrastrucuture projects that’s probably one of its most interesting features.

JJ: Bcoin had the benefit of rather than being passed from developer to developer and having all this legacy code it was just basically me and Fedor originally. We had the benefit of being able to think this through and decide maybe it isn’t a good idea to have global state all over the process and global variables everywhere. Maybe it is actually a good idea to instance these things, make the blockchain separate from the mempool. They can communicate indirectly but they maybe don’t directly know about each other that much. Being able to abstract all these components like the chain, the mempool, the HTTP server, the websocket server for notifications, the wallet and have them all loosely coupled is I think a much better design and a lot easier to work with. There is talk in the future that the Core wallet might eventually be moved out as a separate service. I don’t think that will ever happen. If you look at the code it is accessing chain headers from the wallet. That is everywhere in Core. I don’t think that is ever going to happen. Core is stuck in this weird spot where they are accessing all these shared locks all over the process and all these global variables. I wanted to diverge from that model greatly in Bcoin. That’s basically how it ended up.

AL: Just to make sure that I’m onboard and still understanding this. Really what we are talking about with all the talk of modularity and all the talk of multithreading is right now we have a lot of bottlenecks that are all hooked together. There are a lot of things that can go wrong and if anything goes wrong in any of the bottlenecks the whole system suffers from that because it is all one thing. That is really the advantage of making this modular. It means that part of it can fail without taking everything down. If something has a lot more load on it like the mempool is enormous or something like that then you can specifically just beef up that component without having to touch everything else in the chain.

JJ: That is the basic idea.

AA: You can build this as a scale out infrastructure and you can choose which components to run where and have them communicating through message queue. How has that changed Purse’s business? What benefits have you had from running this as your primary consensus mechanism for Bitcoin?

JJ: I would say the biggest feature of Bcoin and the thing we mostly use it for is just how hackable it is. It is easy to go into the code and change something around. Like what I was talking about earlier we were having trouble with BlockCypher webhook notifications. At this point we hadn’t used Bcoin in production at all yet. Steven looked at me and he said “Could you just do this in Bcoin? Could we set up a Bcoin node and do this right now?” I was kind of nervous because we hadn’t even used it yet. I was like “Yeah alright, screw it, I think we could.” Within the next hour I had something up and running that mimicked BlockCypher webhook notifications and it worked perfectly. We could monitor all the addresses we needed to watch. Eventually we wanted to get away from that model completely and we ended up just using the Bcoin wallet. All of these notifications and everything that we needed has made our lives a lot easier in that respect. Just being able to go into the code and add any notifications or any extra features that you need, that has been the greatest benefit to us.

## Bcoin features

AA: One of the other places that I think demonstrates the ability to move quickly and incorporate features is the sheer number of features you have packed into this consensus implementation. For example BIP 150 and 151 which is a relatively new proposal by Jonas Schnelli to incorporate end-to-end encryption between the Bitcoin nodes. That’s now implemented in Bcoin as far as I understand it. And a whole bunch of other things that are either BIPs that are not yet properly implemented or that are in progress or in testing on various testnets in Core but have not yet moved into production. Can you talk about some of the features you have been able to cram in?

JJ: BIP 150 and 151 are probably the most bleeding edge stuff that Bcoin has. It was actually the first implementation of BIP 150 and 151. If I see a BIP or some kind of proposal or some idea that I think will benefit Bitcoin a lot like BIP 150 and 151, I think those in particular will be very important for SPV in the future. Purse.io doesn’t need that but I think it is a good thing to have in there. I very strongly believe in it, maybe that is a good way to put it. If I see some kind of proposal like that that I think is a good idea I’ll work on it at home or whatever and try to get it into Bcoin and just see how it works. MAST is another one. When I read Johnson Lau’s proposal for MAST I was like “Oh my god that’s brilliant. Pay to Merkle root, not pay to script hash. That makes so much more sense.” I was like “Yeah I’ll implement this and play around with it.” That is exactly what I ended up doing. Now there is MAST support but MAST is still in the works, the specification is changing a lot.

## MAST

AL: I am actually not familiar with the pay to Merkle root vs pay to script hash. You’ve got me interested from your interest in it, what that does, what that means and why that makes sense. Can you explain that real briefly?

JJ: This is MAST. It was Johnson Lau’s BIP, his proposal.

AA: One great example of that is if you think about this at extreme scale. Right now you can do multisig up to 15 keys. What if you wanted to do a massive multisig? Let’s say 1 of 15,000. That’s impossible to do but it is quite possible to do with Merklized Abstract Syntax Trees. Instead of doing 1 of 15,000 multisig which you can’t do you create a contract that is if 1-of-15 or 1-of-15 or one of the other 15. You list all 15,000 keys 15 at a time. That is almost impossible to write as a script but 15,000 clauses in a Merkle tree is only what 13 levels deep. If you wanted to redeem one of the leaves in the tree you could simply put the 1-of-15 multisig and then 13 hashes that lead you to the root and boom you are done. You could fit all of that probably within the current limitations of the script operands limit.

AL: Where do you hold the logic? What I hear you saying is you just track the fingerprint, that is analogous to a leaf here, then you can track that back into this data that is stored in a different structure than on the blockchain itself that has advantages. Is that correct?

JJ: The logic is stored in these individual scripts that you have at the leaves of the Merkle tree. What people noticed is usually when you have IF statements in scripts like that, when you’re redeeming it you provide some kind of input and based on the input a certain branch of code is activated. But when you are redeeming something you already know what branch of code you want to activate. All these IF statements, it was useless, it made the other parts of the script totally unnecessary because you only wanted to execute one branch of code. Wouldn’t it be nice if you could just execute that one branch of code and only include that branch of code in a redemption of an output?

AA: What is perhaps missing here is that you construct the trees offline, you store the logic behind them, you have to remember all the leaves in the tree and all of the components of the tree and store those in some other database offline somewhere. If you want to redeem them, you have to store them, you have to be able to recreate them. You can construct them once and then store them somehow. Or you can construct them in a deterministic way. For example if you had 15,000 keys you just sequence them and you can always reconstruct the tree from scratch. They can be from a HD wallet or something like that. But none of that is in the blockchain. All that goes on the blockchain is the Merkle root and when you redeem, the 5 hashes that lead you to the root. The tree has to be constructed, held and remembered or reconstructed for redemption. I love that we are both so enthusiastic about MAST. It blew my mind the first time I read about it. It is an amazing technology and it is so close to being implemented.

JJ: I know. I’m like “This is such a good idea. Why didn’t we do this earlier?” Like you said, it can get around a lot of the limits for scripts that currently exist, a lot of consensus limits. The other thing you were mentioning, an address with multisig, I was thinking about a way to do that with the current scripting system pre-SegWit pre-MAST. I was coming up with an idea for this last year for Purse because we were thinking of maybe potentially having a certain situation where instead of just having a 2-of-3 escrow we would have 3-of-5 or 2-of-3, something like that. I started trying to design a way to easily create these scripts from a simple notation. It would compile it down. You’d give it keys and say “2-of-3 or 3-of-5” and then figure out how to easily sign them. Having all these inputs and all these branches of code, you need to know what branch you want to execute, the redeem script was huge. It just wasn’t an efficient way of doing it. I forgot about it for a while and I see this MAST thing and I’m like “That is what I was looking for. That is what I needed.”

AA: You also had support for Lightning Network as well as SegWit as I understand it very, very quickly.

JJ: SegWit was another one. I think I was more certain that SegWit was the future of Bitcoin. That seemed more of a sure thing to me than BIP 150 or BIP 151. Maybe that is a strange way to look at it, the SegWit thing has become so political.

## Benevolent dictatorship

AL: How many people are working on Bcoin?

JJ: Right now it is pretty much just me. I wanted to get more contributors.

AL: That seems like a small team given what you’ve been able to accomplish. Is this just a fundamental difference in how it is built or are you just really, really amazing? It seems like a lot more people are working on Core and yet a lot of this stuff takes a lot longer to get in. Obviously you have the advantage of being the only guy there so you don’t have to argue with anybody. It can’t be more efficient to do this as a single person than to do it as a group of 15 really smart people or a hundred really smart people?

JJ: I guess in a way I’m the benevolent dictator of myself.

AL: I see you as a catalyst at this point. You become the benevolent dictator when there are people to boss around. At this point you are the lone guy out there who is working on this. I guess the question I am really trying to ask is are there trade-offs? Are you aware of trade-offs that come from this? Are there places that you know more work is needed before something like this should be deployed in a commercial environment? You are already using it so it seems like you have a high degree of confidence. I’m trying to figure out what the problem is here because it seems like this is a lot easier in a lot of ways.

JJ: As far as Purse goes we are already a very small team. The other developers we have are very busy with other things. I don’t really get help on that front. It is hard to hire for Bitcoin because it is such a specialized thing. As far as outside contributors to Bcoin, I would really love to get some people contributing to Bcoin. I would love there to be a whole Bitcoin ecosystem around it. I feel like as far as Bitcoin and consensus protocols go, Bcoin used to be this tiny little thing and now it is this huge thing with all this consensus critical code. I think that is intimidating to a lot of people and it is hard to understand because the codebase is big now. It is probably not an easy thing to get into. We are using it in production but I still haven’t done a public stable release of Bcoin yet. That is still in the works. I keep saying I’ll get it out within the next week. I’ll say it again and I hope it will be true this time. Right now we are using it in production. I think it is stable enough to use in production. The problem is I’m changing serialization formats for the database and optimizing certain things. For example the past week I just optimized the UTXO set compression which is a huge pain in the ass.

## Production readiness

AL: It is new, that is what I’m hearing from you. It works well enough that you are using it internally but ultimately it is new and you are still changing some fundamental things about it.

JJ: I am still changing things that require database migrations and stuff. I don’t want people to be using that in the wild, in production and then have me force them to do a huge migration on their entire database and have them be p\*ssed off at me. I want it to finally settle and be set in stone before I can consider it stable.

AL: Is that what you are talking about, a week from now? It seems like it is not. It seems like this timeframe is a 3-6 months thing.

JJ: I think the code is there is what I am saying. The things that I am worried about are the data serialization, because once you do a stable release it is hard to change that, and then the public facing APIs because once you do a stable release it is hard to change that because you can’t do it without breaking other code. For example, the format that the blockchain is stored in the database. It is stored in a certain way and if you change that other people’s blockchains will be incompatible. Nobody wants to do a migration on 80 gigabytes of data.

SM: I wanted to bring this back to the big picture. How close are you to the holy grail? What remains to be done before you achieve the thing you set out to do? To use the blockchain for escrow for Purse.io transactions and rely on the internal server system for that.

JJ: I think once I mark Bcoin as stable I can focus on things like that. Andreas mentioned my Lightning implementation. That is still very primitive and not ready. There is the basic state machine there for Lightning. One thing getting into Lightning opened my eyes about is how exactly to implement these Layer 2 solutions. Like doing a simple 2-of-3 escrow. I have had a lot of help from roasbeef.

SM: What is roasbeef?

JJ: His name is Laolu, everyone calls his roasbeef, that is his name. I’ve had a lot of help from him. I think now that Bcoin is getting into a stable state, once we do that we are going to look back into things like Lightning and other Layer 2 things like some system for doing 2-of-3 escrow. Now that the whole stack is there and it is nice and neat. I think we will do that soon but I can’t say when.

SM: But you are moving in that direction?

JJ: Yeah.

AL: When did you start working on this project?

JJ: When did I start working on it for Purse? When I first started it was back in 2014 when Fedor released it on GitHub, just as a small project. When I started to turn it into a full node and add all the things I thought we might need, I started doing that almost exactly a year ago, December last year. It has been about a year to get it into this state.

## Second implementation as a “menace to the network”

AA: Working on this project, have you read comments by Satoshi Nakamoto in 2010 when he said that a second implementation of the client would not only be difficult to achieve but would in effect be a “menace to the network”? Or were you blissfully unaware of those comments?

JJ: I think at that point in 2014 I had not read that comment. When I did see it I was like “He has a point.” It is difficult to reimplement consensus code especially Bitcoin because there are so many little gotchas in the scripting system, counting sigops etc. There are so many little things you need to do. I totally understand why Satoshi said that and it is not an unreasonable opinion I don’t think. The opinion that reimplementing Bitcoin is a bad idea, that opinion has merit. I think it is a good point to make that this is really hard and if you screw something up there is potentially money on the line and you might lose it. At the same time I did it, other people have done it, we do have actual money on the line and it seems to be working from what I can tell.

## Barnacles as bugs

AA: One of the descriptions that I and others have used for Bitcoin consensus code is that almost like an ocean liner, as it collects barnacles on the hull, these barnacles are bugs. In Bitcoin it becomes consensus code. Once the side effects become part of the blockchain the bug itself becomes consensus code because in order to create that blockchain you have to create the side effect of the bug exactly as it occurred every single time. You talked about this very eloquently in your introduction to Bcoin specifically at the SF Bitcoin Developers meetup which is a great group. Can you talk about this process of discovering bugs and then having to faithfully simulate them in your code in order to maintain consensus?

## Process of verifying the alternative implementation

JJ: That was actually one of my favorite parts in a way of implementing a full node. You would implement transaction verification as best you could, you implement the scripting system as best you could and then you basically try to sync the blockchain and verify transactions. You might get a failure at height 30K. Now you look at this transaction, you look at the previous output scripts. What is this doing exactly? What is the expected output here? Then you dig into the Core code, you dig into old mailing list posts. Why the hell is this happening? You say “Oh ok it was this bug” or “It was this odd behavior that I wasn’t really aware of.” Then you fix it and you keep moving. You might get to height 80K until it crashes again. One of the best ways to do it is to try to verify historical data that you know is valid. You keep getting a higher height each time in your blockchain sync. That was essentially how I did it. A lot of trial and error and a lot of digging into the Core code and seeing what the hell is this doing? If I really didn’t understand something like the SIGHASH_SINGLE thing that I mentioned in my talk at the SF Bitcoin Dev meetup, I thought I was hallucinating when I saw that. Like I said I was syncing the blockchain, transaction verification failed and so I am looking at this transaction and I see a signature in the previous output script which is logically impossible. I was like “What the hell?” I showed my colleague Kent and I’m like “Do you see this? Am I seeing this right? Is that a signature?” I had to Google it, I Googled that transaction ID and I ended up with a mailing list post from Peter Todd where he explains it. I was like “Oh ok that is really weird. It is a sort of unfinished feature that Satoshi had in Bitcoin which is only enabled by a bug that also exists.” There are lots of things like that. It was a lot of trial and error, a lot of tearing your hair out and getting frustrated. And a lot of fun at the same time.

## How Bitcoin compares to Ethereum

AA: And now you have faithfully simulated all of these bugs so you can reproduce the exact same which means you have rebuilt all the barnacles that stuck to the hull of Bitcoin as it travelled through time. One of the fascinating things for me is the difference in attitudes between Ethereum and Bitcoin for example. In Bitcoin there is no formal specification of what the consensus rules are. Or rather there is and it is Bitcoin Core, it is whatever the hell Bitcoin Core does is the formal specification. In Ethereum they have a formal specification. Until recently the formal specification was written in a yellow paper. The clients had to conform to the formal specification, not the other way round. Until the implementation of the Ethereum hard fork, the last one, when both clients implemented the specification incorrectly. They went back and rewrote the specification to match the buggy behavior. One of the interesting things here is can you ever really write a specification or do you just have to remain faithful to running code?

JJ: Ethereum’s consensus protocol, it was formally specified before it was implemented? Is that how it happened?

AA: There is a yellow paper as it is called. Now there are many colored papers including the latest one which is called Polkadot because they gave up on colors. There are many colored papers, the white paper, the yellow paper and the mauve paper. The yellow paper is a formal specification written I believe by Gavin Wood and Vitalik Buterin. The yellow paper specifies how the consensus algorithm works using math. It is a formal specification. The clients, of which there are at least two that are broadly active in large percentages, implement that formal specification to the dot and coordinate it. Kind of like the Milan agreement on Lightning. They converged on a common specification rather than the Bitcoin model which is whatever Core code is the specification.

JJ: Right, absolutely. That is something I have thought about. Ethereum and Lightning have the benefit of being built from the ground up and being able to formally specify these things ahead of time. Bitcoin, Satoshi just threw it out there. I try to think of what would happen if you had formally specified Bitcoin before that SIGHASH_SINGLE bug with the find and delete thing that I mentioned before. Before that had even been discovered. I have a feeling there is probably things about Bitcoin, things that Core is doing right now that are still undiscovered in the consensus protocol. You end up with some odd situation where what is the law here? Is it the formal specification or is it Bitcoin Core? Say we discover another thing like the SIGHASH_SINGLE bug in Bitcoin Core after it is formally specified and set in stone, this is the consensus protocol. What do you do then? Do you update the formal specification to match Core? In that case Core is still pretty much the specification for the consensus protocol.

## Alternative processes for verifying the alternative implementation

AL: Your process for going through this was to essentially just run it. Run it, see where it breaks, fix the part where it breaks, run it some more until it breaks again and then eventually you run out of places where it breaks. That means you are in complete consensus with the existing blockchain. It seems like it is not so much the client as it is the blockchain. The blockchain has its own logic to it and if you can’t sync to it… Am I wrong about this, I feel like I’m going off the rails here and that’s incorrect but I feel like there’s something important here?

JJ: That’s just the way I did it.

AL: Given all the things we know, given all the unknowns here, it seems like that is the way you’d have to do it. Because otherwise you’d go through and try to figure it all out on paper, get it into practice and still run into these problems?

JJ: Absolutely. You could do it by analyzing the Core code and reimplementing it to a T. Just doing a bunch of static analysis and running some tests but eventually you are going to sync the blockchain and you are going to have bugs and run into issues. Ultimately you do need to verify a lot of historical data. If it all verifies as far as you know you are consensus conforming. You could be wrong. Bcoin could have some consensus issues, some code that needs to be executed that hasn’t ever been triggered on the blockchain or on any historical data.

AL: That I think is the important part. You are covered for anything that has ever happened up to this point by nature of the fact that it syncs to this point. If you uncover problems in the future then you are right but they will be problems that literally weren’t present at this point in a way where you could detect them.

JJ: That’s right.

## Consensus and minority forks

AA: Ironically there is no being wrong in the consensus game, there is only being on the minority fork. If you have the majority of the hashing power and you fork off of consensus then you are right and the other party is wrong because you have the majority. Right now if Core has a bug and you fork off the blockchain you are wrong even though Core has the bug. But if the hashing power was inverted then you would be right. We have actually seen this play out again, it is a very useful example, in Ethereum where denial of service attacks took down Geth and they started running Parity on the miners. It had the majority of the hashing power afterwards even though it had different bugs. One of the really interesting things about this is that if you are able to continue to develop this and it has more broad application, perhaps one day with miners too, not as a client that is competing to implement a different vision of Bitcoin like a Bitcoin Unlimited, Classic etc which are trying to implement a different policy. One which is faithfully trying to follow at least the current model. You could have the possibility of having two clients which would be a great protection against bugs.

AL: It seems like it is a true alternative implementation rather than a competing implementation which I think you could more accurately describe something that has an ideological or political difference. Do you have any ideological or political differences implicit in this project that we should talk about or be aware of?

JJ: I don’t think so. I just wanted to do cool things with Bitcoin. It is not a political project, I am not trying to change anything that Core regards as consensus.

## Javascript and a teaching tool

AA: Just the fact that this is all written in Javascript is radical enough.

JJ: I get asked that question all the time. Why is it in Javascript? People don’t realize that Javascript is actually getting pretty good. It is a lot faster than people think it is. People still seem to think that it is this tiny interpreted language. It is not interpreted. It is legit, it is compiled to machine code, it is fast, trust me.

AA: When you first saw Fedor’s code for Bitcoin it allowed you for the first time to understand validation of transactions and some deep secrets of Bitcoin. I see some tremendous value for Bcoin, not just as a production tool but also as a teaching tool for many of the developers out there who are much more comfortable with Javascript than they are with C++. Do you think the codebase of Bcoin could give them an insight into how Bitcoin works without a lot of the historical legacy complexity of Core and help new developers?

JJ: I really hope so. That is what it did for me. That is what really brought me down the rabbit hole of Bitcoin, was seeing that code for the first time. It is such a strange moment when you finally get it and you dive deeper and deeper. I think absolutely it could because it is very hard to understand the Core code. It is really, really messy. I like to think that my code is a bit cleaner and it is a bit easier to understand because it is not accessing all these locks just to get UTXOs everywhere. It is a little bit cleaner I think. I hope that is one of the end results, that a lot of people see it and get interested in it and finally understand how it works, and also fall down that same rabbit hole.
