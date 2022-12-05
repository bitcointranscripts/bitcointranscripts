---
title: CTV BIP Review Workshop
transcript_by: Bryan Bishop
speakers: ['Jeremy Rubin']
media: https://www.pscp.tv/w/1PlJQmRZWnZJE
---

OP\_CHECKTEMPLATEVERIFY workshop notes

# Reference materials

transcript tweet <https://twitter.com/kanzure/status/1223708325960798208>

tweet <https://twitter.com/JeremyRubin/status/1223664128381734912> or <https://twitter.com/JeremyRubin/status/1223672458516938752> and <https://twitter.com/JeremyRubin/status/1223729378946715648>

IRC logs: <http://gnusha.org/ctv-bip-review/>

bip119 proposal: <https://github.com/bitcoin/bips/tree/master/bip-0119.mediawiki>

proposal site: <https://utxos.org/>

branch comparison: <https://github.com/bitcoin/bitcoin/compare/master...JeremyRubin:checktemplateverify>

workshop scripts: <https://github.com/JeremyRubin/ctv-workshop>

slides: <https://docs.google.com/presentation/d/1XDiZOz52XyJc4LDSbiD9_JAaJobyF5QDGtR3O9qD7yg/edit?usp=sharing>

# Introduction

Howdy livestreamers. Can someone just tweet that the livestream has actually started? <https://twitter.com/JeremyRubin/status/1223672458516938752> Okay thanks.

Welcome to the OP\_CHECKTEMPLATEVERIFY workshop. In the email I mentioned that we do have a code of conduct. It boils down to "don't be a jerk". Knowing most of you, that should be relatively easy to do, but if not then perhaps refer to the email. If you break the code of conduct, I will evict you and tell you to leave.

I'd like to start out by making a big thank you to everyone who got us here. This has been a long project and there's a lot of support from the community that has come out from Binance, Digital Contract Design, Cypher technologies, John Pfiffer, Jim Calvin, Scaling Bitcoin, Tales from the Crypt, and DG Lab have all been big supporters of this work. I am very grateful. Also SF Bitcoin Devs has also helped with arrangements.

# Schedule

The schedule will include opening remarks, walking through the BIP, an implementation walk-through and talk about the code. We'll discuss BIP alternatives. Then we'll look at some demos and look at applications, then we'll talk about ecosystem and their support. Then we will break for lunch. Then we will discuss more ecosystem support looking at the mempool and how this new stuff will work at that layer. Then there will be an open-ended workshop session like BIP review and BIP Q&A that bleed in together. Then we will do an implementation review session to look at the code and make comments. Then I'll present my thoughts on deployment and have a discussion on what that should look like. In the evening, we have a dinner planned.

There's an IRC channel which I will try to be roughly monitoring if anybody wants to submit questions. It's also a good way for remote participants to ask questions. It's a little better than twitter for questions. For WiFi, there's slips of paper floating around. For tweeting maybe use #bip119 as the hashtag.

This is a worksho, so ask any questions that you have. It's designed to be a little more engaging and I don't want to just lecture the whole time.

# Why are we here?

The main goals today are to review bip119, we're going to learn about applications of OP\_CHECKTEMPLATEVERIFY, we're going to discuss deployment and the roadmap. We're all here because we want to improve what bitcoin is doing. That's a nice principle that we all share. I want people to leave and be excited about new projects.

I thikn OP\_CHECKTEMPLATEVERIFY is one of the most exciting things in the ecosystem right now. It's a departure from what we were able to do before, and what we're able to do after it. There's a large set of things that people haven't been able to do due to complexity, which OP\_CHECKTEMPLATEVERIFY helps solve. There's some other proposals dealing with privacy and efficiency, but you can always make bigger transactions. The transactions might be too large. In limited cases, there's no new fundamentally new capability. OP\_CHECKTEMPLATEVERIFY lets you do new things.

How are we going to prepare the ecosystem for this? What is each project going to do with OP\_CHECKTEMPLATEVERIFY?

# What kind of "better"?

What does better mean? Is it more scalable, is it more secure, are we giving more users freedoms? Are we eabling easier to design protocols? These are all ways that we can talk about better and I think everyone is going to have their own definition of better. I think we can all agree that we're generally here to make bitcoin better.

# Quick demos

I want to show a few quick demos. Let me start up some scripts and stuff. The purpose of this is not to go super indepth. You can hold your major questions. It's just to get everyone excited and thinking about what is the goal here.

I have a UX that I cobbled together. It's neat, but not yet open source. All the mechanical parts are open-source right now. There's no private codebase other than the user experience. You have these scripts in the ctv-workshop repository.

The scripts I made available-- there's one that creates a batch payment, one that generates addresses, one that generates blocks, one that sets up the chain, and one that sets up your node. You can use any of those.

This is essentially a generic transaction viewer that I built. It allows you to load in a list of transaction hex along with some metadata for coloring. It lays out all the transactions and then gives you a UX which shows you where the bits and pieces are moving.

For those of you on the livestream, I apologize that this is not publicly visible right now. Let me repoint the livestream. Now the livestreamers can join in the wonder.

These marching ants around the transaction mean it's not in a block yet. It's still pending. That's what the animation is. The thick lines show that this is part of the transactions. UTXOs are round, and transactions are square. The thin lines are ways of spending a UTXO. The thin lines are possibilities. What I'm going to do is generate a slightly simpler program to look at.

It's going to be creating a new vault. What we have is a program that allows you to say "I have a litle bit of BTC in coin storage and I want to move those coins into my hot wallet". However, I don't necessarily want to move it all at once and I don't want to have to go and access my cold wallet all the time because my cold wallet takes a week to access. So what you setup is a ratelimited control flow program that gives you a little bit of coins every once in a while.

I'm going to mine a few blocks and play a few transactions. Let me broadcast this first transaction. It takes a few seconds to get processed and picked up. So we paid into a contract, we played the first step in that contract, which created two UTXOs: one which is a withdrawal contract, and another is a continuation of the vault program. So with the withdrawal, we can send to cold storage or we can send to hot storage. Okay, let's send it to cold storage.  Once that is confirmed, the other transaction gets removed. This is an undo-send functionality. We tried to send it, we pull it back to cold storage. This is a recursive program. It can have many steps.

These contracts tend to be composable. If you have a standard CTV contract, you can take and plug it into another contract. Maybe cold storage is another CTV and you plug it into the module. These steps have to be pre-planned. We will get into the composition techniques a little bit later. I just wanted to show so that people have some context.

The next demo I want to show is a batch payment. I'm going to go into my scripts directory and now I'm going to hit "generate addresses", which outputs some test data which is a bunch of addresses which are unique and random. If you leave it running, it's like 100 of them. I'm going to paste this into the batch payment API. You can do this using the same script in the repo essentially. Then I am going to click submit. What this does is create a batch payment. I'm going to start this in the background. This is the one that I have talked about a lot.

This is in the context of congestion control. Say we have 20 addresses we're trying to pay, so if you want to broadcast a transaction that was to everyone.... if you wanted to pay everyone, you would have to do 20 work, but for each leaf node it's 3 work plus 4 work, it's like a total of 11 amount of work.

Q: What is 12 work?

A: It's the amount of chainspace required for any individual to claim their own output. The total amount of work is maybe 30% more because you have interior nodes. As an individual I want to get my own UTXO and ignore everyone else.

So say we have two transactions, one is a commitment and one is a fan-out. For any person to claim, they have to do 100 work units in terms of space to get their UTXO. This allows existing exchanges to do it.

With a radix of 1, there's a chain where one person gets paid out first. Then there's a strict ordering for who gets paid when. This simulates an annunity contract with a payout per step. You can also have an nSequence lock. This is also similar to a vault. This is a vault, and if you change what each step is a little bit, you can maybe think about having some abstract representation for some of these.

# Why isn't bitcoin as-is sufficient?

Taproot is going to make complex scripts easier, but transactions largely are not programmable. It's pretty limited in scope of what you're able to do. OP\_CHECKTEMPLATEVERIFY helps you expand that. Pre-signed transactions let you emulate this and we'll probably hear from some others here about that. But pre-signed transactions are hard to statically analyze as a third-party because you need to be a member of the n-of-n multisig to delete the key with the trusted setup.

The pre-signed transactions require interactive setups. You're going to have denial of service attacks. With OP\_CHECKTEMPLATEVERIFY, I also have to hand you a tree of transactions and the redemption conditions. You have to have extra information in your wallet about this. This is no different from secure key deletion. It's impossible to prove that a key was deleted, whereas it is possible to prove that I have given you all the OP\_CHECKTEMPLATEVERIFY information and you can check there's no alternative spending path.

It's both auditing as a party not party to the contract, and also being able to do non-interactive setup. Non-interactive setup and audit are somewhat the same thing. When you create a protocol, before you make the payment and actually broadcast it, send it to the participant and ask them to sign that you have received and then save to disk. That's an interaction at a legal liability perspective, versus interaction at a pure protocol layer. There's an important difference between the two in my opinion.

The other issue is that if you want to use CHECKSEQUENCEVERIFY locks, you can't sequence events that are serial with that. There's some complexity around that and making timings well known.

# Revisitng why we're here

I think we spent too much time to go too in depth. I want to reiterate why we're here. Maybe everyone can say why they are here and what they are excited about. If anyone wants to introduce themselves...

Secure key deletion vs opcode covenants. Prototype hardware device. Stepan Snigiriev has been teaching a class lately on this. We don't really care what the actual covenant mechanism is. The complexities around key management are substantial and independent of mechanisms.

Here's why we're not here. You can disagree about this, but here we go. We're really not here to solve all bitcoin programmability problems. I think you can make the case that it would be really cool if you can run an abstract program over your transaction state. If that's what you want, then maybe look at ethereum. That's what they want to do, and they have spent a lot of time trying to make it work. We can discuss all those issues and things we might want to do, but discussion is different from solving. We don't want to say oh there's this one use case that is kind of interesting that we could do, and we want to make a leap forward in what we're able to do with bitcoin and get that out there, and try to do some follow-up features. OP\_CHECKTEMPLATEVERIFY is composable with new things that come along, it doesn't preclude you from using new things. If you were to add OP\_CAT then you can do a lot more. If you have something that checks if another script exists as another output you can get a lot of other interesting flexibilities. OP\_CHECKTEMPLATEVERIFY can do some of this, but not everything. Really we're here to prove that OP\_CHECKTEMPLATEVERIFY is safe if it is safe, and then figure out how we're going to deployment. We're more here to see if we can move the community forward.

# BIP walkthrough

I wanted to walk through the BIP. When I say walkthrough, I'm not going to do the line-by-line.

The metaphor for bitcoin UTXOs is that UTXOs are little treasure chests that hold gold coins. Gold coins are nice because they are relatively small and uniformly shaped, such that if you have a bigger treasure chest you can fit more of these gold coins in it. What you do with a treasure chest generally is you open it up and you take the coins out, you get them all out and put some back into a new treasure chest. But if you have a covenant, essentially what you're saying is that these coins aren't just gold coins but these are actually special like a rare treasure that there's only a few of. If this is a special Jimmy Hendrix guitar, you don't want to keep it like the coins, you want to say the treasure chest should be a special treasure chest like a guitar case. This is why you want a covenant. What you're expressing is don't just treat this as random coins, have some other functionality about how to handle the coins. This is a little bit like a monad where you have some safe set of transitions and you put something inside, and then people-- you put something inside, you unwrap it like a burrito, but you want to wrap it in a safe way. If you leave it unwrapped, maybe you access it in a thread unsafe mechanism. Covenants are a good way of thinking about what are the safe way to move the assets around. The idealized covenant is a program that is attached to a transaction that observes all state in the world, everything in the world, and then says is this transaction based on looking at all the state in the world. That's really broad and arbitrary though. So we pair it down: what about covenants that just look at all the blockchain history we're able to access? So within this system, is the property still true? Well, what about only the states we define to be part of the system? Eventually you can pair down to something implementable. You can think about ethereum contracts being fundamentally like what is a turing complete covenant for moving coins around? You express all the conditions around coin movement, but they don't move directly just inside of wrappers that have programmatic constraints on what gets paid. In OP\_CHECKTEMPLATEVERIFY, we're asking what's a simple way to do this for bitcoin and says this is a guitar let's put it in a guitar case and propagate constraints like that. Saying thinsg like funds should split according to a pre-defined schedule. These can be somewhat recursive covenants too. So we're not trying to solve all the programming constraints, we don't want to build an omniscient oracle and try to get all the state in the world, but rather we're just working on something more practical and feasible. People have different expectations. You want to build something that doesn't rule out an oracle at a later step, but you want to allow the oracle to exist later. Rather than selecting from any possible transaction, maybe select from a set of 1 of 5 transactions.

With that, let's actually get into the BIP. OP\_CHECKTEMPLATEVERIFY uses OP\_NOP4 (0xb3) as a soft-fork upgrade. It's sort of like a straightforward VERIFY NOP fork. If you have a new opcode you want to add, if you change the execution semantics of the VM, like you say we're going to put this new thing on the stack and then remove it, it's fundamentally incompatible with the previous version. But if you just verify a property with an assert, then it is compatible with previous versions. So then you can make the assertion mandatory and it makes it groovy and okay. So let's make it restrictive. Every time there's nothing on the stack, it fails. If there is something on the stack, then it should be exactly 32 bytes (the size of a sha256 hash). Say there's a well-defined hash function, StandardTemplateHash, matches on the stack, and if not, it fails. We can also as a policy rule reject non-32 byte hashes.

Q: Why are you using NOP for those non-32 byte data?

A: The reason not to fail is that at some point we might want to upgrade. Right now we have no version byte, but maybe someone can add a version byte later and maybe there's a new rule for hashing the transaction. You can think about it as hash flags, like the standard template hash.

Q: Would this require a different script version?

A: Every time we want a new template, we can have a new opcode, but we have limited number of opcodes, so this lets you version the data bytes and you can use the same opcode. That's more or less like a conservative implementation detail. Segwit and taproot have done similar things where they have a default version byte, and if the version byte is not the one in the standard, then we completely define it as "nothing" for now, which gives you more flexibility down the road. Wallets that don't want to lose their coins should just conform to the standard until we define the undefined behavior.

The OP\_CHECKTEMPLATEVERIFY implementation is straightforward. It's an opcode. We check if there's enough things on the stack. We look at the size of the last element, and if it's 32 bytes, we check the standardtemplatehash using CheckStandardTemplateHash. Future upgrades can add more semantics with version bytes. But for now we exclude it from the mempool.

The specification for the template hash is a little more nuanced. There are two different use cases that we have hashes for. The first case is where all the inputs to a transaction are segwit. If they are all segwit inputs, then what you do is you don't include the script. You know that they are all zero anyway, because in segwit the scriptSig is all 0, but the witness is a separate thing that doesn't get into the hash. This saves us from efficiency later on. This makes it more clear what the expectation is. It's a reasonable optimization to make. We'll revisit the details of the hash. The key thing is how we detect if there are scriptSigs.

As a standard rule, not a consensus rule but a mempool policy rule-- if something is just a 32 byte hash with an opcode... that's standard. There's P2WSH and so on. So we add a new one, saying that a 0x20 byte hash and an opcode should be standard.

# StandardTemplateHash rationale

So we go ahead and hash the nVersion, nLockTime and maybe as I mentioned we hash the scriptSig hash. We hash the number of inputs, we hash the hash of all the sequences, we hash the number of outputs, we hash the hash of all the outputs, and we hash the input index- the index of the input that is currently executing. We could do this in any order and it would be functionally equivalent. But there's a nice optimization if we think about what is the general likelihood of what order these fields are going to be modified in. If you have a streaming hash function and you're only changing the last little bit, then you do less work. This makes it easier to write scripts and do validation. I don't know exactly how people are going to use this. I generally expect that the version is not going to change that frequently. I don't think that people are going to be using absolute locktime that much, and when they do, it will probably change infrequently. They won't be scripting absolute locktimes. Relative locktimes, on the other hand, are a different story. The number of inputs- you generally know the number of inputs, but you might want a flexible protocol where you change that, so it comes later. The sequences come next, because they might need to change based on the branch of a program being taken. The outputs hash changes a lot. The input index might change a lot, because in validation if someone expresses that it will come at a different index, we can hash everything and just change that last little bit.

Why are we doing this partial merkelization where we hash the hash of the outputs? If you want a variable length encoding of a hash, you might have ambiguities. There's two specific lengths of hashes that can be used in OP\_CHECKTEMPLATEVERIFY. It also helps with future scripting capabilities where you want to add just one more output or something, it gives you compactness property.

# Malleability

In terms of malleability, we committed to all of the data in that hash that can effect the txid, except for the outputs. It's a restricive rule. The input index cannot effect the txid. In some cases, it kind of could. Why do we want this strict rule about malleability? When you fit into a use case as a basic standard CTV template, it means you can perfectly predict what all the txids are going to be in that tree. We want to keep the txids locked down. We want no malleability. We want to know exactly what the txids are going to be. We want to just have a filter over a list of expected transactions. If you want to monitor the chain for a arbitrary covenant system, how would you know if it was something you cared about? That's kind of complex. But with a simple OP\_CHECKTEMPLATEVERIFY scheme- and you could get more complex- you can just look for txids and run some basic logic at that point, rather than looking at every transaction and carefully analyzing it. Being computationally ennumerable... in order to numerate all the conditions for a OP\_CHECKTEMPLATEVERIFY contract, it's fundamentally O(n) because there's a known number and it's countable. There's some list that someone had at some point. You can reconstruct from that list of n states and get the exact tree. With an arbitrary covenant system, that's not true, and if you had many steps then tracking that outputs, it's not clear what the txids would be on the whole path, and you would need to track recursively and regenerate all the covenant states at each depth. It's messy. It's a lot of complexity to put on wallet implementers. Instead, having a list of txids that are known ahead of time is a lot simpler. You could, if you wanted to do more complicated scanning. It's also a bloom filter issue. With a list, you can put it into a bloom filter. But with an arbitrary set of transitions, there's no bloom filter that you would be able to construct to cheaply check if a block has something you're interested in, you would have to get the full block- which isn't necessarily bad because people should have more full nodes, but it makes processing more heavy for wallets.

# scriptSigs hash

This is a weird rule. It makes an odd constraint that you fundamentally can't put a OP\_CHECKTEMPLATEVERIFY script inside of a P2SH. The reason is that.. in OP\_CHECKTEMPLATEVERIFY, you have to commit to all the scriptSigs, and the scriptSigs point to the hash of the script. It's a hash cycle. The txid of the parent transaction in the input would point to the StandardTemplateHash in the parent outut. These create some hash cycle issues. Alternatively, we can say all scriptSigs must always be zero, but that seems unfair to say that OP\_CHECKTEMPLATEVERIFY is incompatible with the whole class of outputs. So instead, it's compatible but there's more hashing if you use it in those situations. There might be some use cases where you want to use a scriptSig.

This gives us some kind of weird capabilities. If you imagine you know someone's exact scriptSig for spending an output in the transaction, then you know their signature. The signature commits to the output of that transaction. So you can kind of implement something that looks like OP\_CHECKINPUTVERIFY where you want to check that the other input is something you care about. There's some interesting things like that, but it's rather inflexible.  If people want that.  A P2SH can be committed to, like "if (spend coin with Alice's key) ELSE (spend coin with Bob's key) ENDIF CTV".

We don't have OP\_CAT right now, but it would make things more powerful. A lot of the flexibility could come with this easy script change that people are already thinking about.

# half-spend problem

OP\_CHECKTEMPLATEVERIFY is generally immune to the half-spend problem. You have to opt-in to the half-spend problem. Imagine you did not commit to the input index, and you had a OP\_CHECKTEMPLATEVERIFY script that said I am going to spend from Alice to Bob and this transaction will have 2 inputs because you want someone else to add inputs to that transaction. Maybe you wanted that. If someone else shows up with the same OP\_CHECKTEMPLATEVERIFY, then those two outputs can be combined into the same transaction because of the lack of commitment to which index the inputs appear at. This can create a problem where the OP\_CHECKTEMPLATEVERIFY is used in a way that steals coins. We should say commit to which input index these things are meant to be at.

Q: What about accounting for the obligations that each covenant requires, instead of letting one output satisfy multiple identical conditions from multiple inputs?

A: Interesting.

# Branching

You can select a branch and execute one. You have a list of StandardTemplateHashes and we have the OP\_ROLL. For non-segwit, you need OP\_FROMALTSTACK. If you're not in the segwit world, then you can get rid of the OP\_DROPs. Segwit enforces a cleanstack rule. This is not enforced in bare non-segwit script where you can leave a dirty stack. In the segwit version... the reason for the OP\_FROMALTSTACK is a little simpler than typing OP\_ROLL twice. The alternative is that you have to have an additional byte which tells you how many templates there are, and then you OP\_ROLL.  If you had more than 256 things, you would need more than one byte. Actually, more than 16. So you only have one byte literals up to 16. So it saves you a byte in a number of cases. It's conceptually simpler to explain with OP\_FROMALTSTACK. It would probably be better to imagine we had taproot, where we could have as many scripts as we want.

You can do bounded recursion too. This might be obvious. You can put one of these inside of another one. So you could have (H(pay to H(x) CTV) CTV). Each one can have timelocks; you can opt-in for singatures from different people at different times. Makes interactive protocols easier to define.

# Literal checking

A previous version of the BIP had literal checking where you would check that the element was on the stack was immediately from a push, the last push we did. This was setup in a way so that the rule could later be soft-forked out. It's kind of a little clever that we could easily remove this later if we wanted to, but enforce it at first. I got rid of this in bip119. It doesn't protect against a known issue, but it allows you to separately introduce OP\_CAT without enabling constructing things on the stack. This would make things safer. Once we get OP\_CAT, you can now construct things on the stack. Say we want OP\_CAT but not constructing templates on the hash, then maybe we want to include that literal checking rule. But a lot of developers have said it's arcane and makes writing script interpreters a pain and please don't do it. I originally included it to be more conservative. I'm generally in the camp of let's do more interesting things in bitcoin, so it's there, it's gone.

# Unspecified CTV

You can do "unspecified CTV". The scriptPubKey is CTV and the witness is H(anything). Why would you want to do this? You wouldn't want to do this in a future world where you can have a delegated witness type. Imagine a future of bitcoin where there's a script, and also another one which is delegate to another script. You could say delegate to another script, let them pick a script and execute a script. We can sign off with a key from a different template to execute. This is not "why would you do this", I'm giving you a list of things that are wacky that are things to review in the BIP not that you would necessarily want to do this. This is effectively anyonecanspend. You can already write OP\_TRUE, so this is just redundant, but it's just a weird thing I wanted to mention.

# Bare script oddity

Say you are using scriptSigs and they are committed. We can commit to inputs indirectly. It's possible to try to implement a little bit of an OP\_CHECKINPUT case, but only if the ohter inputs are non-witness or if they are witness then you can commit to the other programs but not your own input because it's already committed to itself. I would expect someone to come up with something fun to do with this. I don't think this imposes any safety issue. These are fundamentally non-recursive because you're picking an additional input you want to be with, but that input can't impose some condition on the outputs because that condition on the outputs is already enumerated inside of the template. Doesn't create crazy unbounded amounts of flexibility.

# Underfunded CTV

Why not have a list of things you are trying to audit, like Bryan said? Say you have an underfunded CTV. Maybe you have an output with 10 BTC in 10 outputs, and you only have 1 sat in the input. That transaction would not be able to broadcast. But if you have another input, you could say someone else should fund this. There could be a control path without funds, and someone else pays for it. You could imagine someone pays for lunch. I have an HTLC that lets me revoke after a week, and I put half of the BTC in one part, and someone else can showup and sign at different input indexes and combine into one clear condition. So the underfunded case is kind of interesting. You can commit to the number of people too. For accounting for each obligation in the way Bryan asked about, you would have to specify the number of obligations. You would have to introduce a lot of other functionality. The best way of doing that would in my opinion be to add some kind of explicit fee opcodes. There's other cases where you want to do a spend and "allow this much fee" or something. Unclear. This would let you write something where-- I have done SIGHASH\_SINGLE and someone else can claim the rest of this output, but not to fee. They can put it into something else, but not fee. I don't know why you would want that.

Q: How is underfunded CTV different from anyonecanpay?

A: It is anyonecanpay. I'm saying anyone can pay for half of my lunch. You both say "me" and then there's a race condition. Anyone can fulfill the other type of the contract. You can also use OP\_CHECKINPUT if you want to say this specific person. You as the second person for the underfunded case, you might want to say "me" but I don't want to express that everyone can join and pay for lunch, but I do want to say I will specifically pay for that lunch. You can have flexibility on the claim, but it is "anyone can claim" at that point.

Q: So it could be, hey, my company will you pay for my lunch, rather than will anyone pay for my lunch?

A: Yes. If you want to express that you can be spent to any output, then you should specify there should be 2 inputs can be this, and I am okay with being at input 0 or 1. If you want the unbounded case where you are spent at any index, then you need OP\_CAT to add whatever sequences are appropriate, add whatever number of inputs and outputs you want, then you just express that I want this company to have some limited set of coins. So that would be a more complex scripting primitive. While there's use cases for that, let's solve that. You can already do a lot, these are just weird edge cases you can't do as well.

Q: Is this source-specified CTV, rather than underfunded?

A: You're not  necessarily specifying the source, you could do it if you want to. You can specify the source if it weren't a taproot output. You can specify the source but not the outpoint. Specifying a specific source is a weird thing; why are you enforcing coin selection or key selection on that other wallet? It's useful for protocols, but there's no obvious use case for this. In most cases, you want anyone to add whatever output they want to the transaction in the inputs. You don't care who pays you, you just care that you got paid. It doesn't really matter what person does this.

Q: In Mike Hearn's lighthouse protocol, you could have people put money into the crowdfund and also take it back.

A: It would be complicated to do something with that many state transitions. But you could build a UTXO accumulator script where at each step adds half a bitcoin into it. If it doesn't get to the terminal state, then some other action happens, or the money is only released once you get to this big point, but then the clawback mechanism is kind of hard. There's a lot of things you can do. I think we mentioned this on bitcointalk: the wrong way to engineer OP\_CHECKTEMPLATEVERIFY is to pick a well-defined application and then figure out how to do it in OP\_CHECKTEMPLATEVERIFY. It's better to pick a use case, and find out the OP\_CHECKTEMPLATEVERIFY way of doing it, because it might look differently. You can't map on this arbitrarily signing multisig thing to this; but you could say we're using OP\_CHECKTEMPLATEVERIFY with multisig on top of this, and this is the tied-hand oracle model where oracle can only do a few things like deciding how refunds get processed but they don't get to decide who gets the money. With the chain thing, you can preclude the case where someone decides to take hteir money back. Maybe clawbacks only happen once a month or at a specific time. There's a lot of nice things you can do, but you want to figure out the UX from a OP\_CHECKTEMPLATEVERIFY native perspective.

Let's keep moving just so we can get through this session.

# Upgrading OP\_CHECKTEMPLATEVERIFY

We have left this 32-byte thing as the only defined one. If you have 33 or 34 bytes, you could define new types of OP\_CHECKTEMPLATEVERIFY as a soft-fork. The general mechanism for this is there. If you want to not commit to inputs, and propose that as a new one, that might be reasonable, but it would require a new soft-fork and there's a well-defined place for that soft-fork to go. We can add on a version byte for new semantics.

# Implementation walkthrough

I want to walk through the code. Let's do a 10,000 foot flyover. There's only a few commits.

<https://github.com/JeremyRubin/bitcoin/commits/checktemplateverify>

<https://github.com/JeremyRubin/bitcoin/pull/9/files>

You can scroll through this in the next session or on your laptop as I go.

# Add single sha256 call to CHashWriter

It normally computes the hash of the hash. One hash is enough, though.

# MOVEONLY: Move GetSequence/Output/PrevoutHash to primitives/transaction.h

This functionality belongs in the transaction primitives where this is a defined hash for the transaction. This is where we want the templatehash stuff. As a wallet implementer it makes sense to pull these things into this area.

# Refactor those utility functions

These all get the double hash. We don't need a double hash though; so let's refactor those to just define the single hash we defined earlier. Then update the pre-computed transaction data to re-hash those again. These are all just setup commits. I think taproot has something similar to this.

# Add StandardTemplateHash definition

This is an important commit. Now we're adding a StandardTemplateHash. We need a new utility function called GetScriptSigsSHA256. Then we define the way of computing StandardTemplateHash. Maybe look at the skip scriptSigs check line. The skip\_scriptSigs thing. We also want to check, are the arguments passed in the correct order? We don't have type-safe hashes for bitcoin. Maybe a type-safe hash definition where you don't put the wrong hash into the wrong place, that would be a good pull request against Bitcoin Core.

# Add SignatureChecker method for checking StandardTemplateHash

In bitcoin, we have a notion of a signature checker which handles the abstract state of the world we might need to verify when validating the transaction like what's the current chain height. We have an abstract class so that we don't need a native version of that in script. This is a natural place for this code to go. We add a method that checks this. Are things being cached? Caching can come later. Caching is not part of validation. It comes later.

# Add OP\_CHECKTEMPLATEVERIFY opcode as OP\_NOP4

We define the semantics of OP\_CHECKTEMPLATEVERIFY in this commit. The code should be the same as in the BIP. There might be differences. I use a switch instead of an if statement. It makes it easier to add upgrades in the future. Other than that, there's not a lot to check here other than the meat of the BIP.

# Precompute the StandardTemplateHash

This is like it. That's the core of the BIP. These other things are like what are we doing with the BIP and how do we make the implementation better? So now we have some hash caching. We precomputed some of these values- can we pull those in? Can we just store the hash again and not re-hash during block validation? In block validation, there's some pre-computed data structures. You pre-compute things when you receive a block you can pre-compute these batchable things of the block and run other checks. You can run through and compute these hashes. So we're adding StandardTemplateHash to this existing pre-computed issue. So it hashes all the transactions. When you're doing this, it makes sense to do this. Script validity is a different data structure. A block comes in, you look at all the transactions- and from somewhere-  you get all these precomputed things filled out in a vector, then you check validity, and then you have this other stuff. To check it, we need the hash of the transactions. All of those hashes end up making their way into here. I'm all doing is adding a new one. Let's just look at it. The Precomputed data structure is here.... you have the hashPrevouts, the hashSequence, hashOutputs, then I have the hashes that I am adding that weren't there previously. I'm just adding a few things. The only one I'm adding is the StandardTemplateHash. I'm not adding that much space compared to what else is already in there. This has the witness hash hashes. The things you need to efficiently compute the sighashes in segwit. In the case where you have standard sighash flags. If you have different sighash flags, you need something else. This is a lot of caching stuff.

# Make bare OP\_CHECKTEMPLATEVERIFY basic transactions are standard

We add a standard type for this. Adds standard type TX\_STANDARDTEMPLATE. Adding a standardness rule is there just for efficiency. As soon as you need more than one input, the overhead in the segwit world is smaller, maybe you want to add it but add it later. Are there other types- like one where we have a few different options as a standardness type? In taproot, you will already have this. You can't have vaults in barescript though if you don't add it. For vaults, just doing it in segwit anyway. This is a carveout only for bare script, in the case where you care about efficiency like a congestion control tree.

Q: can you elaborate more on why someone would want to use a bare op\_ctv basic transaction?

A: Great question. If you're doing a congestion control tree, and you're trying to pay out 1000 people and you have a tree of outputs... You're trying to decongest the network. You want the maximally efficient way for one person to claim an output. You want a minimum overhead on-chain. If you use the smallest possible script to express the OP\_CHECKTEMPLATEVERIFY constraint, then you are most efficient. Doing it inside of segwit does it with another hash and then the witness. But if it's just a single input and there's a number of outputs, and it's just this basic OP\_CHECKTEMPLATEVERIFY, then that works for this congestion control tree case with no other conditions or sign-offs you want. So I think that's important for network plumbing to have that type defined. Does that answer your question?

# OP\_CHECKTEMPLATEVERIFY deployment parameters

This is a joke for now... Can we completely define the deployment parameters and get the logic correctly? The soft-fork starts March 1st. We're not going to start March 1st. I picked this months ago. I was thinking six months ago that March 1st is reasonable but it's not going to happen. We can change those dates and then it would be defined correctly. The controversial question is do we want to use bip9 version bits? It makes sense to use a non-controversial deployment strategy.

# OP\_CHECKTEMPLATEVERIFY functional tests

This one is interesting. These are tests that make sure it's working correctly. Writing tests that don't rely on other parts of wallet functionality is some kind of painful. You're manually constructing transactions to have a bare-minimum test framework for the pull request. In a later branch, I have tests where I just call an RPC and broadcast the transactions in some order. That's much easier to deal with and look at. For the sake of testing bare functionality, here's some tests. The questions to ask are, are these tests convincing to you? Are there other edge cases that are prime to be tested, and would you like to write those tests?

# Modify script\_tests.json to enable OP\_NOP4

There's a thing saying don't use OP\_NOP4, so we modify this. This is annoying. It's pretty simple. These files are compiled into the binary to get these actually through. I don't remember what it is. Someone more familiar with that should look into that.

# Alternatives

At some point we'll have a presentation from some folks. We'll have Jacob come up and talk about his alternative. I talked a little bit about pre-signed transactions. What I want to underscore is that OP\_CHECKTEMPLATEVERIFY is not the only way to get this, but I think it's pretty good. So what are the alternatives?

## OP\_CHECKOUTPUTVERIFY

There's a far dated bitcointalk thread about covenants. I'm sure this exists in Nick Szabo's literature about smart contracts and things like that. But in terms of bitcoin, this thread was pretty much the first. There was OP\_CHECKOUTPUTVERIFY by Moser, Sirer and Eyal in 2016. It presents an extension to bitcoin scripting language that says let's add regular expressions to bitcoin script and make sure that an output matches a regular expression. It allows some self-reference, make sure I myself was included inside of myself. This is cool, and people started to think about the use cases in this limited but powerful model (MES16). They wrote code for it, but it never had traction. There's a lot of complexity in the implementation.

There's a few drawbacks with OP\_CHECKOUTPUTVERIFY. If you're trying to use this for congestion control, the script is less useful because of the size. It doesn't have a way of ensuring txid stability. You can't say, I want this exact txid because you can malleate locktimes. This was pre-segwit and pre-CHECKSEQUENCEVERIFY. To pick up MES16's OP\_CHECKOUTPUTVERIFY today, there would need to be a lot of design work. The patterns are not computationally numerable. At some point, it's O(n) because someone computed everything. For OP\_CHECKOUTPUTVERIFY, you can't do that. The wallet has to be more complex, you can't just write a bloom filter for txids.

## OP\_PUSHTXDATA

jl2012 wrote a proposal for OP\_PUSHTXDATA. This is about pulling out the relevant pieces of transactions.  There's a lot of conditions you would need to check for the obvious case of committing to everything. I think you can do anything with OP\_PUSHTXDATA maybe with one or two more fields, but it would be easy to add fields to OP\_PUSHTXDATA. If you want to make OP\_PUSHTXDATA a soft-fork and don't want to have an OP\_SUCCESSx because it's not taproot yet, there's no way to add UTXOs to the stack. So these all need verify semantics. It would be verify, and then you have another copy of the data and the script would get worse and worse.

I think this would be a reasonable way to do it, if you had a way to loop. You can kind of do looping with rolling it out in script. But it's pretty gnarly and it grows quickly. I think OP\_CHECKTEMPLATEVERIFY is superior for shipping.

# OP\_CAT + OP\_CHECKSIGFROMSTACKVERIFY

If you had both OP\_CAT + OP\_CHECKSIGFROMSTACKVERIFY you can kind of do the same things. But this is kind of complex. The scripts are really complex. I think it's unlikely that this will get deployed. I think it's disqualified because these scripts have lots of signatures and they are expensive to evaluate. You also get arbitrarily complicated scripts from this. This is probably not good for scripting. Therefore I don't think these are the best option even if strictly speaking possible.

Q: You're talking about the scaryness of the scripts that would be generated using these, but isn't there a lot of promise to having simpler script generation language that is well-verified that creates verified scripts?

A: I think that could be good. I think there's something nice about not having that being too complex. You need a formally verified script generator. The formal verification work I have seen has not been promising because you only get the properties you have proven and if you forget a property then your entire thing is completely screwed, like if you rely on OP\_CAT but you don't have the rule that checks the last input doesn't make it go above 520 bytes, and someone can pass something too large and cause it to fail... It's another thing to write covenants and pass inputs that don't trigger weird rules about how bitcoin validates state. I think simpler is better. In bitcoin the status quo is that during this audit we have everyone look over what the script is.

Q: gmaxwell said a long time ago that, with every output you're proving that you can control those funds. You're not doing computation. Ethereum went the other direction and said we should be doing on-chain computation. Instead, we should be providing proofs and not on-chain execution. I think a lot of people are allergic to doing computation on-chain.

A: I think that's a reasonable way to say it. I think OP\_CAT plus OP\_CHECKTEMPLATEVERIFY enable most of the same things that OP\_CAT + OP\_CHECKSIGFROMSTACKVERIFY would enable. OP\_CHECKTEMPLATEVERIFY enables some stuff, and CHECKSIGFROMSTACK enables a broader set of things which might be good but the chances that CHECKSIGFROMSTACKVERIFY getting through is regrettably for some people in the audience, low. But we will see, maybe in a few years we will have a nicer way. The real reason for CHECKSIGFROMSTACKVERIFY is to delegate scripts and say yes this person has signed off on this, and we can do that without adding CHECKSIGFROMSTACKVERIFY.

Q: Easier to implement OP\_PUSHTXDATA? Neither OP\_CAT or OP\_CHECKSIGFROMSTACK pushes things on the stack.

A: The argument that I am making in that point (3 on the slide), if we're comparing the scripts you're writing.... let me restate your question. You're saying CHECKSIGFROMSTACKVERIFY is still a verification OP\_NOP upgrade, and PUSHTXDATA is not soft-fork compatible in this way. CHECKSIGFROMSTACK could be added as a soft-fork but...

Q: The 3rd point seems to be saying I can do arbitrary computation on the stack with OP\_CAT and OP\_CHECKSIGFROMSTACKVERIFY ?

A: No. You have three alternatives: OP\_CHECKTEMPLATEVERIFY, OP\_PUSHTXDATA, and OP\_CHECKSIGFROMSTACKVERIFY. I've already made the argument that OP\_CHECKTEMPLATEVERIFY is better than OP\_PUSHTXDATA. The PUSHTXDATA scripts are better than the CHECKSIGFROMSTACK scripts. I'd say just using PUSHTXDATA would be better. An example of CHECKSIGFROMSTACKVERIFY would be the [Blockstream blog post](https://blockstream.com/2016/11/02/en-covenants-in-elements-alpha/). You have to serialize the transaction itself into the stack in its entirety. I don't know. You have an aneurysm when looking at it. You have to put the transaction into the stack. You serialize all of this into the script itself. The difference between CHECKSIGFROMSTACK and CHECKTEMPLATEVERIFY and TXPUSHDATA is that in CHECKSIGFROMSTACK and TXPUSHDATA you have to duplicate everything. But OP\_CHECKTEMPLATEVERIFY says don't duplicate just hash. With TXPUSHDATA, you put it on the stack not as a literal but you're saying put this on the stack from the data itself, but to enforce the covenant you have to hash it and enforce anyway. So if you're going to be adding OP\_CHECKTEMPLATEVERIFY anyway, you might as well just use OP\_CHECKTEMPLATEVERIFY. If you add TXPUSHDATA, you get the same thing in the end. The CHECKSIGFROMSTACK way of doing things is a mess by comparison. Maybe in 20 years the tooling will be better. If you look at miniscript with these other things... miniscript only works on things that are CNF like, or monotonic boolean expressions might be the exact category. As soon as you want to move transaction data into the stack and verify signatures, you have to go back and do that.

Q: Aren't you pushing a ton of the verification to the ...

A: Exactly, it's just a single hash you push on. What's nice is that those validations are cacheable outside of script validation whereas you need script validation caching for these other proposals and it's not clear these are scripts that you can cache the validity of. In validation, the scripts you write for TXPUSHDATA it's not immediately clear to me that those scripts are eligible for the script validation cache. If your transaction is not eligible for the signature validation cache, then it might be eligible for the script validation cache. PUSHTXDATA it's not clear that without a lot of work those would be eligible for either of those caches and it's not clear we would ever have a general rule to get those in there. I'm not sure what the rules are to make something eligible for those caches, but OP\_CHECKTEMPLATEVERIFY is very easily cacheable. It's an optimization in script size and also amount of work done in validation. It makes it a better and cheaper primitive to use. I could imagine you want to commit to one thing that is less than 32 byte, but that's a strawman really- when have we ever really had less than 32 bytes of conditions? What exactly are you checking- one input had a value more than something? I don't know. You're still going to have a signature in that case, anyway. Maybe a way to prove this is that any time you have a cryptographic need of authorization, you're going to need at least 32 bytes. Maybe 20 bytes for P2SH... if you wanted real efficiency.. but yeah.

# OP\_CHECKTXOUTSCRIPTHASHVERIFY

OP\_CHECKTXOUTSCRIPTHASHVERIFY is broken. It's a much weaker version of OP\_CHECKTEMPLATEVERIFY. It's a similar thing. If you like this one, you should just use OP\_CHECKTEMPLATEVERIFY.

# ANYPREVOUT (NOINPUT)

OP\_CHECKTEMPLATEVERIFY is redundant with ANYPREVOUT/ANYSCRIPT/NOINPUT. If you just had one... for all time, you could only have one or the other? Then maybe take ANYPREVOUT because you can use OP\_CHECKTEMPLATEVERIFY with it and get something similar. However, the scripts for it are worse- they are bigger and require signature validation which is going to be more expensive. They require elliptic curve operations. It's sort of similar to OP\_CHECKTEMPLATEVERIFY in other ways. There's some edge case conditions though, because you're doing a signature over something. In a segwit transaction, the first method of doing ANYPREVOUT is not eligible because you're always committing to the scriptpubkey in the signature so you need the version that is ANYPREVOUT, ANYSCRIPT, and any key, which I don't think is currently proposed. It's already not exactly ANYPREVOUT because you need an additional exemption for the signature verification algorithm, just to enable something less efficient than a purpose-built solution like OP\_CHECKTEMPLATEVERIFY.

Q: If we get any form of ANYPREVOUT or SIGHASH\_NOINPUT, you can emulate OP\_CHECKTEMPLATEVERIFY by putting a bare CHECKSIG in the redeemScript.

A: ... say there's a known public key, you have ANYPREVOUT+ANYSCRIPT, then this one should be able to validate. This one also you need the ANYPREVOUT ANYSCRIPT ANYKEY variant because otherwise you always commit to the key in Schnorr which creates a hash cycle which prevents this method from working. So you need this new NOKEY version which I don't think we want for any reason other than enabling OP\_CHECKTEMPLATEVERIFY... and just to do the same job of committing to the hash correctly... Yeah, it's off the table because of signature aggregation reasons in the Schnorr proposal...

Q: You say you need the NOPUBKEY variant. But why not just a regular CHECKSIG that doesn't use segwit? Schnorr commits to the public key in additional ways.

A: ANYPREVOUT is not proposed for non-segwit scripts. Right now it is only intended to be added to segwit. I've ignored the proposal and don't know the exact answer. Unless we add it specifically to bare script, then we wouldn't be able to use it anyway. If you did it inside of bare script, it would be incompatible with the signature aggregation use case. It might be key aggregation actually. Maybe an actual cryptographer should go look at this and come up with a proposal to do this and that's fine.. but the point is that, essentially what we're doing it is going through a lot of hoops to add a signature in our validation, but why not just add that feature anyway?

Q: I'm worried about any footguns you might try to evade with OP\_CHECKTEMPLATEVERIFY might be doable with this other covenant mechanism.

My final point about ANYPREVOUT is that at best you get something like OP\_CHECKTEMPLATEVERIFY with no ability to construct things on the stack, so no future extendibility. But you might have the half-spend issue, but maybe you commit the input indexes -that's still open for debate- but you would also not be able to upgrade without a new sighash flag and sighash type. In OP\_CHECKTEMPLATEVERIFY there's an explicit way for upgrading this stuff which is to add a new template type. There just wouldn't be an upgrade path... I'd think if you go, like, there's no such thing as the signaturehash flag... the signature hash flag maintainers you would have to convince them to add a flexible scheme for signature hashes that allows you to construct any possible amount of data to sign in the transaction, then that's going to be a really long-term project and not something that could be done in the near-term. That sort of flexibility imposes a lot of DoS considerations and then you need either special cases that those functionalities are only turned on for ANYPREVOUT ANYKEY etc... But we could just directly introduce a feature. The signature doesn't save you from any footguns because you already have the footguns already.

Q: Where does the hash cycle come from?

A: The hash cycle comes from the fact that -- for doing pubkey recovery.. Well, then you can't do this. You can use this without pubkey recovery, yes that's right because it's ANYPREVOUT ANYSCRIPT and you have a signature. In this case, if you're using a nonce point for the public key, just some well-known random number.. I don't know if you can actually use G, that might have a problem. Then you're signing with "1" as your privkey.. I don't know if that's broken? Again, that's a topic for a cryptographer.

Q: That mechanism is a covenant mechanism that achieves a lot of the same things as OP\_CHECKTEMPLATEVERIFY. If there are things prevented by OP\_CHECKTEMPLATEVERIFY, but are possible with a noncepoint public key like in ANYPREVOUT covenants, then...

A: The thing that is generally possible and is that you, you can combine ANYPREVOUT with other sighash flags which can enable you to select different parts of the transaction. I don't know if that... it's not clear to me what exactly that gives you over being able to specify one of n OP\_CHECKTEMPLATEVERIFYs. So if you're using taproot, you can specify the conditions you're interested in. One is happening at the sighash layer, and one is a literal instruction. I guess it goes back to your earlier point: with OP\_CHECKTEMPLATEVERIFY, we're saying that the transaction inherently has to satisfy this property. With adding new sighash flags, we're saying run some masking instructions on the transaction and then see if this thing fits on that pattern. Let's validate not compute, and for that philosophy then OP\_CHECKTEMPLATEVERIFY makes more sense because it's only O(log(n)) cost for that use case.

Q: OP\_CHECKTEMPLATEVERIFY is a sighash. You're taking what's normally done as a sighash and puting it over here. Why not use a sighash?

A: There's a reason for this. The way that sighash flags are defined right now, there's only 8 bytes. I think that adding more extensibility there is going to be a larger engineering project. I did consider it. It's possible to define OP\_CHECKTEMPLATEVERIFY as a new sighash flag. But then there's a question like, well you've added 128 invalid sighash flag types where we only wanted to enable this one and not these other sighash flags... you end up not being able to cache as efficiently, because you can't precompute what the OP\_CHECKTEMPLATEVERIFY hashes would be, you have to actually run the scripts in order to validate. OP\_CHECKTEMPLATEVERIFY is done in order to give you the best context-free way of evaluating whether a transaction is valid. When working with signatures, you inherently have to do something interpretative to check those signatures. With OP\_CHECKTEMPLATEVERIFY, it's just a single hash check and it can be precomputed. The strongest case to be made that ANYPREVOUT is striclty redundant, is that OP\_CHECKTEMPLATEVERIFY looks more efficient. For the use case of helping the network, caring about efficiency is a goal. We want to be able to cheaply make this. With ANYPREVOUT, unless we're using a well-defined nonce point, you don't get the compression benefits with OP\_CHECKTEMPLATEVERIFY which are known to be computed deterministically from their leaf nodes. In terms of wallets-- because the signatures...  the signatures in this case end up being, if you're using a well-known nonce point that everyone has a key for, you can recompute them. But recomputing them for validation requires more signature operations. Signing is generally slower than validating. This is just why it's a worse idea.

Q: If you have SIGHASH\_NOINPUT, you can't prevent that. So saying that OP\_CHECKTEMPLATEVERIFY is made better by this...

A: Any script that you write, it's always possible to precede it with a layer of like 10 OP\_DUPs and end it with 10 OP\_DROPs... you're free to write a less-efficient version of whatever script you want. There are many scripts that have other forms that are less efficient. If you do it the most efficient way, people will probably prefer that. Other than standardness rules, go ahead. You can write multisig as OP\_IFs, but we have CHECKMULTISIG too. This is the ability to express the same higher-order preconditions which is a mathematical object, no ordering, into two different programs. You can write two different programs in two different ways that are functionally equivalent.

Q: I am more concerned about functional inequivalence. What are the things enabled by this difference?

A: The only thing enabled as far as I understand is that you can do a covenant to any existing set of sighash flags, as long as they are compatible with NOINPUT ANYSCRIPT. Anything that is compatible with NOINPUT ANYSCRIPT, any transaction, you could then commit to. That's the difference. The problem would be, these are not well defined BIPs. I don't think there's a single definition of what are the sighash flags compatible with NOINPUT ANYSCRIPT. What are the weird edge cases you have to worry about if you're using those things? I can't directly answer that right now. You have to go read what NOINPUT ANYSCRIPT is safe with. That's one of the issues that people have with ANYPREVOUT. It's a lot of complexity and validation. People are cognizant of this; are we going to add something that is not going to preserve some key variant and now we're stuck with it because we added it at one point? I'm not going to come out and say NOINPUT ANYSCRIPT can never go in... but I would say that the set of proofs and arguments for the safety of it aren't sufficient where I have invested time enough to say this is a reasonable path... CTV could be an optimization of this.

Q: If OP\_CHECKTEMPLATEVERIFY comes without NOINPUT, then it stands on its own. But if we do NOINPUT, then we have to consider interaction with OP\_CHECKTEMPLATEVERIFY. If we get NOINPUT first, then we can do a number of things that CTV does without using CTV.

A: If you want to make the argument about getting one but not the other... The thing I would say is that if you actually want ANYPREVOUT... because ANYPREVOUT ANYSCRIPT is equivalent, and you want to decrease the amount of review burden for ANYPREVOUT ANYSCRIPT (and maybe we get just ANYPREVOUT and not ANYSCRIPT)..... the amount of difference being introduced by this new proposal is actually less, and then the security considerations are less. It makes more sense to do OP\_CHECKTEMPLATEVERIFY and then this decreases the review burden of ANYPREVOUT ANYSCRIPT and reduce the likelihood of it not getting adopted. Just pushing on one is just, it's equivalent to the sort of Schnorr/Taproot/Tapscript spiral we had where we really want Schnorr well we can also do taproot well we can also do... and as you do this, the complexity goes up. The amount of time to get Schnorr over the line is now years, whereas it could have been 2 years. If we just said Schnorr only, maybe we would have to introduce something after Schnorr, but right now it's separate enough to think about ideas where we say we're not enabling any additional features on top of ANYPREVOUT. So that's more conservative.

# Pre-signed transactions using multiparty ECDSA

I tried to get people interested in multiparty ECDSA like <https://github.com/jeremyrubin/lazuli> and it works today but there's a lot of setup assumptions. I also wasn't able to get any review for that methodology and that's where OP\_CHECKTEMPLATEVERIFY came from where I introduced something that I wanted directly.

Q: If you have Schnorr and a tree of pre-signed transactions, ... is this a tree of...?

A: The threat model is you're okay leaking your private key data, as long as you detect you leaked your private key data. In this model, you can pre-sign a bunch of transactions that you have not yet committed to. You generate everything, and then you spend to it. What's nice about this is that, not caring about whether your keys get leaked.

Q: How do you detect key leakage?

A: You detect if a signature got produced. I believe if you see a valid signature at the end state of your protocol, for my protocol, then that means your key did not get leaked. If the person worked to create the signature in this protocol, then it would not be possible to both produce a signature and a ....  You delete the key. You can safely reuse them if you have the signature. You're doing 2-p ECDSA like for lightning in theory. Bitconner has a library for that stuff.

# Pre-signed transactions with secure key deletion

This is work that I am doing with Spencer, Bryan and Bob. I am presently based in London. This is two projects from my PhD work. Like Jeremy said, it is possible to do covenants in bitcoin today. I think if we're going to propose a new mechanism to do covenants, then it's worth digging into the details about what is possible today, what are the security properties, and what do we really gain from introducing a new opcode or some other proposal? Hopefully this will help push forward any proposal that can make covenants work.

## Basic idea

The basic idea of a pre-signed transaction covenant is that you start by constructing a covenant transaction. You encode in that the conditions of your covenant. You can specify specific addresses, or maybe you want to specify something simple just like the version number of the transaction. You then sign this transaction with an ephemeral key. You commit to those conditions. Then you delete the key so that no new transactions can be signed for the address you specify during the deposit or commitment transaction. At some point before you create the covenant, you have to specify the deposit transaction and you need this to be a segwit transaction so that it has a static txid so that you can point to the output for the deposit. Once you sign the covenant transaction and delete the key, then you can broadcast the deposit or commitment transaction.

## Security analysis

I have a definition here of what I think a covenant is: it's an unbreakable commitment to a specific set of conditions that apply to the transfer of control of coins. The security of this setup relies on the secure key deletion technique. I would argue that there's a range of different security models you can get for your secure key deletion. I'll discuss that in a moment. It also depends on protecting your private keys before you have deleted them. Using a secure random number generator is also important. That security concern is equivalent to any other mechanism you would use for a covenant, though. Finally, instead of securing your private key, you then have to securely store the covenant transaction itself. This has a more limited attack surface, but you still have to do it.

## Secure key deletion

The main point to discuss is secure key deletion. An opcode covenant basically relies on the consensus security of bitcoin. But in this case, we're relying on the process of whoever is setting up the covenant and doing the key deletion. If you just had a single key used to sign the covenant transaction, then the security of the key deletion is only as good as that one process of deleting the key. But if you had for example, a multisignature output in your deposit transaction, then you can distribute the risk of failing to delete one key. If you use an n-of-n multisignature output in your deposit transaction, then only one of those key deletions really needs to happen. Then that way, you have a customizable security model for your key deletion. You can also get different guarantees of key deletions by using different signing devices like a disposable key and signing device that you incinerate later, or you can try to implement provable key deletion in your hardware device.

## Class of possible covenants

The class of possible covenants with pre-signed transactions is limited to the things you can specify by transaction templates. If you use this type of mechanism to make a covenant, then you have to think carefully about what sighash flags you use. You could make a uselessly-constrained covenant commitment by using ANYONECANPAY | NONE or ANYONECANPAY | SINGLE. But you have to be aware that those inputs and outputs can be repackaged into different transactions, and it's not that useful if you're building a tree of covenant transactions because you don't know the txids ahead of time.

Alternatively, you can make a maximally-constrained covenant where you just sign with SIGHASH\_ALL where you commit to all the inputs and all the outputs. Most of the power comes from the script in the outputs of your covenant transactions.

You can make a chain of covenant transactions that you have to pre-specify before you commit to it by broadcasting the deposit or commitment transaction. You can also do disjoint covenant commitments like OR branches. You can combine those arbitrarily, too. It's possible also to do multiple deposits but there's safety issues that you have to think about there, especially if you're in a multi-party situation.

Before I talk about comparisons to opcode covenants, I just want to say it's possible to do a certain set of covenants today. It might be worthwhile in some applications, and it might not in some other applications. If we can elaborate on what situations it is useful to use the mechanism of secure key deletion, then we will know exactly what we're getting when we introduce something like OP\_CHECKTEMPLATEVERIFY. Among a set of trusted parties, secure key deletion is useful. But if you have multiple distrusting parties, then I would argue that OP\_CHECKTEMPLATEVERIFY is probably more useful there. It's not the key deletion that is the problem... everyone can locally make their secure key deletion as secure as they want. The problem is more about the communication complexity and interactivity. It's an availability argument. You have to be online to construct and then delete. If you're creating an address for your covenant transaction, you want to do that to as close to the activation of the covenant as possible, as close to the time that you're deleting the key so that your ephemeral keys are as short-lived as possible. With OP\_CHECKTEMPLATEVERIFY, you can have long-lived addresses. It is availability. One of the major differences between secure key deletion and opcodes, is that you have to construct the transaction, compute the txid, sign it, and then delete it. In a multi-party scenario, this becomes a pretty serious restriction because all n devices have to be offline. I have to go offline to retrieve a public key, I have to do this twice for every signing twice. We have prototyped with one device deleting a key. It's also for every transaction in the program graph. One advantage of this though is that you can construct multiple offline pre-signed transactions and nobody has to know they exist. This is an off-chain protocol. Whereas with an opcode you have to put those paths on the stack. But doesn't this make more toxic data to have these pre-signed transactions? Yes, it increases your attack surface only in so far as people know there are alternatives. In a post-taproot world, which has some benefits for pre-signing too, you're only paying log(n) data on the stack. If you huffman encode the probability of which branches are going to execute, then you're back to O(1) expected chain space for as many conditions as you want, within a probability distribution of the likelihood of your branches.

There are differences not only from which you derive your security from (key deletion or bitcoin consensus), and then there's also privacy differences. If you're sure that you can't accidentally lose your ephemeral key when you use n-of-n, then it's safe to use n-of-n. But if some weird thing happens to your signing device, then you might want some tolerance for that. It's not about protecting from theft, it's protecting from device failure. You can always restart the protocol if the device fails. In a multiparty case, what happens if one of the parties walks away? You can do threshold delete-the-key where it's k-of-n instead of n-of-n.

Q: In OP\_CHECKTEMPLATEVERIFY you have to expose the whole tree?

A: No not actually.

Q: Have you looked at BitML at all? We can talk about that later.

... Bryan asked how to choose between standard templates... you use OP\_ROLL, and htat exposes the alternatives. But with taproot, you have a tree and put one in each branch. With taproot you learn nothing about the structure of the tree. With huffman encoding, you can imagine a left and right, and left is the most likely one, and the right one is the branch of the second-most likely script. So you can have a linked list style thing... and then the property you have is that if you sum up the expected values of the probabilities for the branch, then you would have something efficient in terms of space. Huffman encoding is just the easy one to explain. The downside is that people learn that this is the one that you thought is most likely, but generally you don't learn the length of the chain, except for the taproot value which is like 180 deep or something? You don't have to reveal the total structure. I think the other point is that, you asked, doe sthis require that you have that whole contract program on-chain. Not really, you can communicate it out-of-band, but it might be a well-known template and people could plug in inputs they know about and re-generate them.  If you wanted to blind them, you could add salts to them like an OP\_RETURN output or something. That transaction would then be blinded. You could also put it into the scriptsig.

Let's say I wanted to construct a protocol that required a preimage to be revealed in order for this to be valid, one thing that I could do is say I'm in a case where it's a single input, and then I add a salt to my scriptSig that is just a PUSHDATA of 32 bytes of garbage and then I reveal to you the transaction template but I don't reveal to you the scriptSig nor the scriptSig hash. Then you know that, you reveal the scriptSig hash but not the preimage or something... So this solves this, giving you the ability to optionally blind the template, but by default anyone can recompute the template just by knowing the parameters.

With pre-signed transactions, no information is revealed, but with OP\_CHECKTEMPLATEVERIFY there are some arguments revealed. Pre-signed transactions are great, then I would say OP\_CHECKTEMPLATEVERIFY is also great. Using taproot, generate your non-interactive protocol and then lazily use deleted-key with n-of-n Schnorr signature to make the version that is blinded in terms of alternatives so you don't reveal anything else in the tree. That gains more privacy. OP\_CHECKTEMPLATEVERIFY lets you optimistically spend, and collect signatures. From a resource allocation standpoint, you're forcing everyone else's node to bare your security premium... say you want something where you're confident that a sufficient set of keys has been deleted, and I'm forcing everyone else to eat this multisig that there isn't much network verification burden for OP\_CHECKTEMPLATEVERIFY. It's an upfront thing with OP\_CHECKTEMPLATEVERIFY due to the hashing, versus secure key deletion where it exists and you do it today and there's an ongoing cost. With Schnorr, we can use musig for n-of-n with one signature, but this benefits both.

The main barrier to opcodes are that it's difficult to reach consensus for a soft-fork. Also, it is hard to analyze systemic risks. We can analyze specific risks, but how does that translate to the system as a whole? I am not sure how to do that. Also, what applications should be designed for? Is it broad use, narrow use? These don't preclude opcode covenants in any way, but it's something to think about.

The main benefits of opcode covenants that I see is that you don't have the procedural overhead of dealing with the secure key deletion procedure. The security of the opcode doesn't depend on that process of key deletion. Wallet development might be easier. We already know how to handle private keys, but nothing really manages pre-signed transactions. In OP\_CHECKTEMPLATEVERIFY the watchtowers still have to know the pre-made transactions. It might be harder to design wallets in both cases. Proof-of-reserves is pretty easy with the opcode covenant because you still have the key, and you can prove your ownership of the key. This is harder to do if you have deleted the key. A covenant address can be a lot longer lived with an opcode, which is nice.

# Vault custody protocol

This wraps up our first project, which is describing secure key deletion covenants in general and what are the security properties of various covenants. The second project we're working on is a vault custody protocol. In theory, you can swap out the covenant mechanism to the one that you want. We have two types of vaults: a Moser-Eyal-Sirer vault, and then a simple push-to-cold-storage vault. We have a computer interface mediating communication between many different hardware wallets. We have a multisig hot wallet (active wallet). There's a recovery wallet which has strict rules about how many times you want to access those hardware wallets. Then there's a set of devices for the vault wallet, where you do the ephemeral key generation, signing and deletion. They will have to be right now custom hardware that we define for secure key deletion functions. Also you need a watchtower to monitor for any release of your vaulted funds.

## Benefits of vault custody protocol

It enforces gated access to your set of funds. The idea is to distribute those funds across many vault outputs and ratelimit the amount of unvaulting funds. In that situation, you limit how much risk you expose yourself to every time you want to access your funds. You retain the ability to adjust the security of your remaining funds because you can always sweep the remaining UTXOs into your recovery wallet.

## Drawbacks of vault custody protocol

It's a complex setup. There's high procedural overhead for users. They might require advanced domain knowledge to use this, or a team of engineers to build a custom wallet. Commercial hardware and software for the management of these covenants is not available yet, and the security analysis is pretty complex. We have two drafts of two manuscripts and if anyone is interested in this work then send me an email.

Q: What are your main critiques of OP\_CHECKTEMPLATEVERIFY ?

A: It's difficult to get a consensus for a soft-fork. It's hard to know what systemic risks you're introducing. Wallet implementation. Just specfying the design for the set of applications you want. Any change to bitcoin is inherently very risky. The application of covenants seems to be the most interesting in terms of what I've seen.

I mentioned earlier about the ability to use standard checksigs... Deleted key is another type of covenant mechanism. We can use one or two of these at the same time. Any guarantees put into OP\_CHECKTEMPLATEVERIFY could be evaded by other mechanisms. That's one of my big concerns: why do we need three covenant mechanisms? Shouldn't one covenant mechanism be enough? I can't emphasize enough how complex the wallet actually is. It's stupidly complex. If you have a trezor, life might be good. But the active wallet has to be multisig, so that's at least two devices. You need a backup, so double that. You need a recovery wallet in case a theft attempt is detected, then you have the watchtowers, then the device that deletes the keys. You're talking a minimum of just like 6-8 devices, and finally you need the watchtower which you might operate yourself if you're sophisticated but less sophisticated users will probably want to outsource that. Do the sweep transactions get triggered automatically by watchtowers? Does it notify you? Does it have personally identifying information on the watchtower? Do I have to be available for the recovery attempt? All of that is independent of whether we use OP\_CHECKTEMPLATEVERIFY or deleted keys. All of those elements, like the active wallet vs the vaulted wallet.... All the trusted hardware stuff, you can throw that away, you have eliminated like one device out of 8. All the wallet handling stuff is simpler. All the logic for implementing a OP\_CHECKTEMPLATEVERIFY wallet, you inherently have the metadata. But for presigned... No, it's the same. I have the pre-signed transaction, or I have the metadata from OP\_CHECKTEMPLATEVERIFY. It's identical.  A wallet has to be able to inspect the outputs... If you're auditing for a third party, then you need OP\_CHECKTEMPLATEVERIFY.  A wallet is operated by one entity, they have everything. If I want to commnicate it to a third-party, then yes I need OP\_CHECKTEMPLATEVERIFY. If I have all the metadata as an operator... there's less metadata for OP\_CHECKTEMPLATEVERIFY ?  There's a difference between batch and vault. One of the prime use cases for vaults is making inheritance schemes. If you want to assign assets to your descendants and give them 1 bitcoin/month stipend, in that case, I'm going to give you these assets, you receive them, so you're getting them from a third party. It's not the vault you made, it's the vault someone else made for you. How do you vet that they didn't have the key? You would have had to be a part of that. In multiparty scenarios, you're right unless you come up with a good multiparty key deletion scheme... OP\_CHECKTEMPLATEVERIFY is going to be better, for multiparty. But a wallet is a single party. I'm going to book-end this. We have 15min before lunch.

# Demos and applications

## Compressed batch payments

Right now in bitcoin you can batch payments together into a single coinjoin transaction or a non-coinjoin transaction with a fan-out with a bunch of UTXOs. You might have a small privacy hit. The number of signatures you need is drastically reduced, which decreases your fees. The key idea in OP\_CHECKTEMPLATEVERIFY is a two-phase commit.  The first phase is assign the inputs that you're going to spend, and then phase 2 is create the outputs. This is a little bit less efficient than the original batch payment transaction, but it's only O(1) extra work.

What you gain from this is huge. If you had an incentive to not batch outputs because you think it's less likely to go in, then you're probably not going to ues batching and make space efficiency worse for everyone. But, you could say, I could guarantee that for a nominal fee rate, I can just get it confirmed, that's a pretty big win. Now I can pay top of the mempool fee rate for one input one output transaction. Later, we can pay non-peak fee.

So the question is, who wants one of these things? Most people want a UTXO immediately. Here's an interesting case. How many people move coins from Binance to Coinbase? That's a pretty common use case. So for exchange-to-exchange, they can see that they can redeem an output and not need it right away. Exchanges could then manage cash flows. You get a time benefit, for arbing between Binance and Coinbase, it's batched up, and now there's privacy on whale-alerts.

Q: Doesn't this peg your fee rate?

A: Yes.

Q: What if the two exchanges don't trust each other and one of them commits to only spending coins as that transaction, and then decides not to broadcast it?

A: Fundamentally this presumes exchanges operate a node with an infinite mempool and any transaction they see that involves their address, they store that transaction. So the idea is that going between Binance and Coinbase, they will say here is the second transaction.

The exchanges don't need to have pre-existing relationships... but you do, because you can send the transactions into the mempool. No, they just check it out of the mempool. Every user already has the withdrawal transactions. You already need this because you don't know the txid. The exchange emails it to the user and they can store that, submit it or whatever, or you can broadcast all the data to the mempool. The de-congestion goal isn't that you can't do this with the mempool.

The primary benefit is that it's a non-interactive protocol between exchanges. Today in bitcoin, there's two things-- you pay someone, and you give them the option to pay someone else. Now there's two buckets: you pay somebody, and you can say, I can pay you and give you the option to pay someone else immediately which is how it works today, or you can say I'm going to pay you and here's a proof that you can eventually push data to the chain and get that payment option. But if you want to, for whatever reason like fee minimization, you can hang on to that and delay. It increases the economic utility of the chain.

Q: Isn't this just equivalent to...

A: We can pick this up later.

Q: This is your biggest pitch for OP\_CHECKTEMPLATEVERIFY so it seems prudent to cover why this is impossible without OP\_CHECKTEMPLATEVERIFY.

## Tree payments

You just need a branch, you don't need the other stuff. The longer you wait, the less fee you will have to pay. Different people get paid out at different areas of the tree. Each user would pay for transactions in the path from the tree, and have multiple intermediate transactions that they broadcast. You have an arbitrary merkle root that you are verifying. A lot of this logic is shared.

## Why do we care about this?

Batching is the worst case if your layer 2 uncooperative closes. You're going to be contending with batches in the apocalypse scenario... it makes the argument that we have probabilities that we will do better by having some cooperative protocol up the stack, makes those claims stronger for lightning or layer 2. Yes, lightning could be better, but fundamentally they all decay into this in the worst case, so let's make sure they are good. This focuses a lot on making sure this is okay.

## Simulation

This walks through a simulation and shows what the mempool looks like with batching and without batching and how much better congestion is under different scenarios. The fundamental question is, what is this notion of scaling that we're trying to achieve? The thing that we want to focus on is how much is a user aware that there's a blockchain under this all. To the extent that the wallets can become nice UXs and we can load in proofs that we need, we can get transactions from a rational mempool etc, then does the user know that they are on a blockchain that has only one megabyte of transactions per block? Every protocol here makes different tradeoffs. Being able to postpone work lets you be fee-abstracted, and you can have an agent that tries to minimize fees by delaying the expansion later, and the less aware of fees you are the better in this case. What do we mean when we say scaling? Are you aware that there's a horrible database underneath this? OP\_CHECKTEMPLATEVERIFY promotes a cooperative case where they are able to better express which of their bandwidth is better and which is not.

Q: For batching, why not just submit the batch tree? One way to think about batching is that it's an ability to transfer fee payment from the sender to the receiver. Child-pays-for-parent could do this anyway.

A: Yes, that's one way of using it. It gives you the flexibility to decide different policies.

Q: I could do that anyway with child-pays-for-parent.

With OP\_CHECKTEMPLATEVERIFY, you can expand the payment bandwidth of the chain in a capacity in a way you can't do with CPFP. You can signal to miners a higher priority for transaction inclusion. But with OP\_CHECKTEMPLATEVERIFY, you can pay a vastly higher amount of people than you can today on-chain. If you're using CPFP for that purpose saying users can pay if they want, they can have unconfirmed outputs which is awful. If I'm trying to shove through a payment and I'm an exchange operator, I'll just replace-by-fee and RBF the whole thing. You don't need OP\_CHECKTEMPLATEVERIFY for that. With RBF, you're not increasing just total fee, it's also total fee rate. You have to pay O(n) more fee to get that bumped. It's a big amount that you're paying. It's a lot more fee than CPFP...

Q: If your fee rate is monotonically increasing, then OP\_CHECKTEMPLATEVERIFY doesn't help.

Q: Did you record your certified check presentation?

A: I don't think there's video. I also need to go pick up lunch.

<https://bitcoin.stackexchange.com/questions/92746/how-is-op-checktemplateverify-a-scaling-solution/92755#92755>

# Other comments

Marty from Tales from the Crypt sponsored lunch for us, and transiently Square who is sponsoring them.

Say you are doing arb between Coinbase and Binance and they engage in a two-party deleted key. If either party deletes the key, then that's fine. You can also do a regular multisig, without deleted key. So you can already do that. For batched exchange-to-exchange payments, you can do that in a single UTXO already with netting, doesn't necessarily require OP\_CHECKTEMPLATEVERIFY.

Pile of unconfirmed transactions, use CPFP.

You can't trust a sender to trustlessly send you money. You need a confirmed UTXO.

With OP\_CHECKTEMPLATEVERIFY congestion control batch withdrawal tree, you still have an unconfirmed UTXO: the one that you can spend eventually with your real value is deep in the tree and the fee environment might be the case that it is too expensive to get to that point. So from the perspective of the user, it's still unspendable in the same way as an unconfirmed UTXO that the user can help get into the blockchain with CPFP. But it requires the exchange to have a bunch of UTXOs, and for the use case to allow the user to trust the exchange (or payer) to not double spend out from under you.

Show me that the congestion control (non-interactive exchange-exchange arbitrage) is not possible without OP\_CHECKTEMPLATEVERIFY -- not convinced yet. The idea of using the mempool to communicate between two distrusting parties can be done in other ways too, such as in transactions that you never intended to get confirmed to send OP\_RETURN information or whatever, to establish an off-p2p-network other communication method. I am willing to say lightning payment channels isn't viable due to apocalyptic fee congestion channel closure fee issues for large numbers of payments between exchanges, but they can be aggregated together.

Well, it is also batched payments for non-exchange use cases where you don't want to trust that someone won't double spend a UTXO out from under you.

It's stupid wallets. Say I have received payment. My wallet says I have received payment. Now I have a UX problem: I have to worry about whether th e tree is in the block... I can arrange for funds with CPFP, all before I can spend it. I have 17 extra steps in my wallet before I can spend the funds that I presumably already have.

With 2-of-2 multisig with secure key deletion, you can do the batch congestion thing without OP\_CHECKTEMPLATEVERIFY at all. The only problem is that it introduces an interactivity requirement to use a pre-signed transaction covenant here. So you can have a tree of transactions and do the batched congestion control thing anyway, with pre-signed transactions, with the added problem of an interactivity requirement.

You can use the mempool to interactively establish channels with new peers. Especially if you can use the ECDH trick. One exchange can give the user a codeword that they type into another exchange's interface, to recover a communication channel created through the mempool. Well, you could also just paste a URI into another exchange's system and avoid the mempool. Then one exchange can query another one.

Could we get a better description of the scenario for apocalyptic channel closure fee issue with lightning?

# Back to the schedule

We will go back to BIP review and implementation review later.

# Lightning and channels

What are the impacts of OP\_CHECKTEMPLATEVERIFY on lightning and channel technologies?

## Ball lightning and channel factories

I call this ball lightning. But it's a channel factory. Ball lightning is a real phenomena though. The core idea is you make a big tree of lightning channels. This is really cool because right now if you want to make a lightning channel, you need a transaction. But say the network is lopsided and you want to create as many routes as you want in an O(1) transaction, and then to redeem later you can pull them out. This spot fixes and adds liquidity into the lightning network. Here it makes it cheaper to do that because you're not competing for blockspace. Privacy, it helps too because nobody can see that you're opening those channels. .... At the end of the day, if you're making n^2 channels then you will need n^2 chainwork eventually but in the mean time the work is log(n) which is cool.

## Non-interactive channels

It's the idea that OP\_CHECKTEMPLATEVERIFY lets you come up with a program and let someone audit it, they see it's correct, and they see you produced something of value. You can do non-interactive channel setup. After some amount of timeout in steps, I can take my money back. Along those steps, you have an opportunity to give the other party a pre-signed transaction. This is where pre-signed transaction works with lightning network. You can say, here's a new state, here's a new state, here's a new state. Those states can be arbitrary whatever lightning protocol you want. If it's time to close and the issuer is dead, then the person receiving the money can go ahead and get their money. If the person receiving the money is dead, then you can wait and claim all the money which is even better for you, or all the money or some original state.

The other thing that is important is, can you do this today in lightning? Yes. In a specific case, if I'm making a payment to you, and the payment is-- I think where, where I by default owe none of the money.. I can open a channel to you where I have none of the money, and you own it all, and how am I going to make an incremental payment? You have to do it in a non-polarized way.

## Max HTLCs in a channel

... this helps you wumbo more than you have wumboed in the past. Wumbo is roasbeef's fault, yeah. In the existing case, you have lightning and you open up all the HTLCs every time. But in the new case, you open up the tree of HTLCs and they keep expanding to as many HTLCs as you need.

There's a max HTLCs limit in lightning in the protocol. I think it's 65,000. It's the maximum message sized and also for the block in bitcoin... If you want to get around that, there's a soft limit that nodes implement which might be 12 but it may have increased. I think you can do about 500 in the current clients. If you want to go to 1000, it wouldn't be a big deal with this technique I'm describing. The more HTLCs you have in flight, the more liquid the lightning network is which is good for everyone. HTLCs are like subchannels of channels. This amorizes the expansion for you which you would have had to do eventually otherwise. The more nested state you have... and then you need more.. to make sure you... One thing that is nice is that in the hashing construct of this, the verification-compilation can be amortized. Some of the hashes don't change because you're updating only one state, so you can cache those branches. This is for you guys to solve: how can you efficiently use this? This also points to a difference to pre-signed transactions, that the amortization where you don't have to re-transmit everything which would happen if you had to sign.

## Payment pool

The idea behind a payment pool is a multi-party channel that serves three people and sign three HTLCs that can kick people out at any time. But say you want a fully signed state, there's some sort of n factorial. With pre-signed, you could say maybe we don't have a pre-signed for.. maybe we only do up to three-deep for three series of people and then we re-sign on a rolling basis and otherwise go to some other protocol. That gets complex. I don't think payment pools work with pre-signed transactions. Matt Corallo and I talked about what payment pool opcodes you would want, you need OP\_MERKLEBRANCHVERIFY OP\_CAT and something to set bits in a bitvector.. and that might sound like a lot. I don't think it's incompatible with a bit vector and a merkle branch to not propagate a state to the next run... But with mutating state, you lose txid and non-malleability.

This is where you pull out one UTXO and create another UTXO that re-vaults the rest back into the pool.

## Implementing payment pools in OP\_CHECKTEMPLATEVERIFY

There's a tree of channels, and no special logic really, and you do all the transactions in the lower layer. This is a privacy benefit and an efficiency benefit. Going up the tree, the leafs in the node, you include a taproot aggregate key for all the participants in the subtree. So what you do is you can say, we're completely polarized here, we want to make a payment that rebalances things, so what do you do- you ask the neighbors hey can we rebalance, and recursively go up the tree and optimistically you'll get to the top and cooperate with whatever optimal subset of them are online... This goes back to the batching argument I made earlier: in the case where you can assign probabilities for cooperation as you go up the tree, you can say it's better because you get txid non-malleability which lets you build nested protocols a little more efficiently. So I think this is a more reasonable design, but maybe someone will come up with a really good payment pool system that doesn't need this.

n factorial expansion of txids for a simple payment pool.

Some people really like payment pool idea, but I think it's better to do something that is a combination of more known primitives rather than a whole new primitive.

## Vaults

This is the program I showed you earlier in the interactive GUI. But I also made it as a slide as well. You have some arbitrary UTXO and you have this control program in orange that says every once in a while create a UTXO and then that UTXO then either sends everything to cold, or it continues. To continue, you emit a withdrawal UTXO. It's like an undo send where you say oh I messed up, send it back to cold storage. Say you move 1 BTC per month to your phone. If your phone was hacked and someone else got control, then that 1 BTC has a 1 week maturity period where you can send it back to cold storage still. A rational attacker would wait until something has matured that they can steal.

## WIP metascript compiler

This is a research project I am interested in pursuing. We have a few scripting languages. We have Dan here who wrote Ivy. There's also Balzac and Solidity. It's poorly named, but it actually has some really interesting ideas that aren't in other scripting languages for bitcoin. There's some notion of participants with private state they are storing, and has some notion of interactivity. I also threw up there BlueSpec which is like a VHDL competitor that is pretty neat. If you think about it, there's a software layer for controlling vaults but there's also a hardware layer- so how can we describe transactional hardware? You wind up with similar controls as a BlueSpec-like language where you are creating plumbing and a description of how things are moving rather than something that has imperative state.

As an example, one of the properties with OP\_CHECKTEMPLATEVERIFY that is cool is the narrow window of a standard OP\_CHECKTEMPLATEVERIFY script is that you have this composability property where for a given model that goes to arbitrary address outputs, you can just throw another one inside it. As the outputs of that annuinity, you can put undo send as the outputs of that annunity, and you can tag on more and more programs into that if you want. On this slide is a templately description of a language, which helps if someone else given the same program description can verify that the hash is the same for the given inputs. Instead of sending you a million branches, you can generate them yourselves.

Q: Miniscript?

A: Miniscript is not suitable for this because it would be fundamentally what you're expressing like the keys, but miniscript only lets you take monotonic boolean expressions and compile them into an optimal form, rather than understanding the funds through transactions. Miniscript has no notion of what the next transaction is.

Q: BitML?

A: Balzac seems to be based on BitML. You need a templated system that allows for recursion.

BitML currently compiles to Balzac which is more of a transaction description language. They don't have recursion. It might be an easy hack on to it to say it's a copy-paste templater, you put the template in front of it and you get something that works, but what's complex there is that BitML and Balzac has some notion of state and participants and I'm not sure how that would work out. Also, they are incomplete: they don't use sighash modes other than SIGHASH\_ALL so they can't express everything that bitcoin can express. You can express more if you were able to use SIGHASH\_SINGLE and ANYONECANPAY. This is more of a research question. There's interesting things around like, can someone pass me a precompiled ABI.

The other thing that is cool is that I like the idea of being able to put responses inside. Say there's some event that is confirmed, and one that is in the mempool. You can also trigger valid spends if you saw something in the mempool. You can also gate logic around seeing a signature or a txid to unlock another branch that is partially-signed but encrypted by another party. Some of these interactive things, you don't have the budget to write your own off-chain protocol except at the top layer where you novate everyone; you can aggregate signatures from enough paricipants, and otherwise rollback. This elides the requirement for another interactive system. It becomes a question of how much time you have to develop your own custom backend and things like that. I would expect that if you produce a real scripting system like this, you would see an explosion of innovation in bitcoin. Right now it takes me a week or more to write an RPC for just one of these contracts and there's a lot of edge cases. But being able to write at a high level, and having an output that we can inspect in a transaction tree viewer like the one I showed you... that would enable many more people to build on bitcoin which I think would be good. It increases user liberty like if I want a specific contract for myself, right now bitcoin doesn't let you do that unless you're a sophisticated developer. Making this more approachable- well there's a tradeoff between keeping users safe, and letting users meet their needs with other scripts.

Q: With arbitrary computation-- with chains of arbitrary transactions, I can compute absolutely anything, and why do that? In eltoo, they proposed that you can have a chain of state updates that has that computation off-chain. Putting these all on-chain is like going the route of ethereum.

A: You're correct. The reason for doing it this way is that if you want non-interactive protocols, you fundamentally have to roll it out on-chain. At the top level, it doesn't mean you're going to be signing ANYPREVOUTs... but if you want to be able to start doing these things, it's chicken-egg where coordination is so hard that we're probably not going to do it. Off-chain coordination is a little bit easier. Being able to express some of these logics on-chain, that would open the door for people being able to do it on-chain.

Once you have OP\_CHECKTEMPLATEVERIFY the thing you add is a zero knowledge proof generator opcode and prove that you could have had other transactions but you prefer not to. Locktime might be difficult. If you opt into doing this with your script, you can just say hey this thing is equivalent and I obeyed all the rules. But you still need the kernel saying, we couldn't produce this. Eltoo says you can elide all the intermediate states. I'm confident that this will help you write eltoo things. But otherwise you would, essentially you wind up making eltoos that are agreeing to new contracts.

You could say you have a branch that does play-by-play, like wait one block get one coin, and wait one block wait one coin. Or maybe one says wait 6 blocks and get 6 coins, or maybe you want to elide a few of those steps because you did in fact wait n steps. A rational mempool wouldn't have replace-by-fee, it would be "consider this other transaction as well" and then you would be able to pick which set of transactions is back. Say you had a batch that uses CTV and one that doesn't, then you as a miner might choose one that is higher fee rate but less overall fee. Depending on what the mempool backlog looks like, miners would either pick one that elides the state or doesn't elide the state. OP\_CHECKTEMPLATEVERIFY is a scheduler for picking your priority on the blockchain computer. Ew, I said blockchain computer.

Q: Is there code for your metascript thing?

A: No. It's just an idea I've been toying with. I got relatively close to metascript just writing in C++ just writing with C++ templates. Then I got ready to kill myself doing that because writing templates.

Q: Do you need a language?

A: I think starting with function calls would be smart, and then dress it up with a language. But the nice thing with languages is that there's a human readability aspect.

# BIP review

Q: Are we doing the right thing? We would have to figure that out before the BIP review in detail.

A: That's part of the BIP review: should we be doing something else?

Q: The mempool ecosystem support stuff. What's the urgency for that in this workshop, versus non-emergency because it will inevitably get enough attention?

A: The urgency on the mempool stuff is that the mempool is not rational. It's a good attempt at being rational, but it's not. Most of the stuff that you might care about doing immediately you might not be able to do if the mempool is not sufficient. Overpaying is a simple solution. Since overpayment is so easy for fees, it's more like an academic concern well we want some robust way of writing smart contracts... so that's one reason why you might prefer to hear about mempools rather than fees. On the other hand, fees are fundamental to whether this approach can workout in the long run.

There are three options. We can either skip ecosystem stuff and get into the BIP, or we can do wallets and fees, or we can do mempool. Or fourth option, we can do them all but do them fast.

If you want to create taproot and you had a soft-fork for it, you wouldn't be able to use it until the mempool supports it because no miners would have it. You want code in the mempool that can accept transactions which is critical for accepting transactions. So the mempool has some inefficiencies, that make any sort of programming on the bitcoin blockchain almost impossible. So you have specific carveouts and things that handle specific cases. It's general, not jus to OP\_CHECKTEMPLATEVERIFY, but there's a lot of things in there. The software development of mempool and making it more rational to understand OP\_CHECKTEMPLATEVERIFY and other smart contracts. You would need these for pre-signed transactions. You can't submit a transaction and its child, unless the parent transaction was accepted. So that needs to get fixed in nodes. There's also some transaction pinning issues. There's not much public familiarity with these issues. This requires a lot of background reading to understand what's going on with mempool acceptance. It sounds non-controversial, so getting people to understand the controversial parts is more important.

# Ecosystem support: Wallets and fees

## Sending OP\_CHECKTEMPLATEVERIFY payments

We'll talk about wallets on the OP\_CHECKTEMPLATEVERIFY sending side, and then on the receiving side, and then fees. One of the RPCs I created is called create\_ctv\_vault that builds that diagram I showed you. What we do is we build a OP\_CHECKTEMPLATEVERIFY script where we first pick our base cases. We pick our end states that we want our program to be in, and then we build backwards to get to the root of the tree. We start with the last little withdrawal, we build up all the way, and then we now have a hash that tells us this is the program that we want to run. Then what we do is, we say submit this to the wallet, for how to pay for this transaction. We figure that out, we construct that transaction, we sign for it, and then we have now a well-known transaction with the txid. Then we attach. It's like a linker. The first step is compiling, then we emit objects, then we link. Linking is where we get the txid for the root transaction and we propagate the txids down the chain. Now I have a txid for your parent, now put it into the input, and then put it into the bottom, then we send that back to the client so that the client has that blob of hex. Then you load that into your wallet software. That linking step can be a separate concern; you can just do the compilation step only, or you can create just the transaction that does it, or just do the linking. They are all separate concepts, but in an RPC you might want to do them all at once.  This is the inspiration for metascript where maybe we shouldn't write custom linkers every time we write a new program.

We create the use cases we want... we create a use case for going from hot-to-cold, and one case for hot-to-hot which is undoable spend, and then one continuation of the vault where we go vault-to-vault, and one case where we go from vault-to-vault that's our recursive step. What's complex is that we go and find the hashes and compile into OP\_IF OP\_ELSE scripts and then we set our script witnesses appropriately to have that script.

Q: So this is creating the templates and transactions in our wallet.

A: Yes. We're just making the tree. We start at the bottom, and then work our way up and add each one piece by piece. The catch is that in our code, we have a base case- the conditional where, if we have no vault that we're trying to attach to, then do one thing a little differently. You can look at the details of what this is in the code to get more nuance. The linking step takes an optional integer because inside of our program we know what the COutPoints will be- because we can say 0 is the one for the vault-to-vault and 1 is for the undoable spend... but to the outside world, they could have put it for any index, so we allow it to be specified there which is messy but it's fine. Then we add the prevout. We know what the hash is, so we add it.

Then broadcasting: so we've gone through the process; we found this program, we built it, it turned into an object, and then we linked the executable against a pointer. Now we want to broadcast it to a mempool. Fees have to be sufficient, it must fit within mempool limits, and the sequences/nLockTime must be "mineable". You can start broadcasting state transitions, essentially. If these things aren't true; if it can't go in the mempool yet or the fees aren't sufficient, then your local wallet can still track it, and it will wait for rebroadcasting logic which will rebroadcast once a day to try to broadcast again. Amiti is working on making that better. Rebroadcasting logic will eventually help in the case of the batch payment.

Any more questions about sending?

Q: Are you waiting to re-broadcast because you expect fees to go down, or are you re-broadcasting because it's not acceptable for the mempool yet?

A: If there's a sequence lock, you can't put it into the mempool, and there's no mempool that will handle things that will soon be able to go into a block. You could imagine writing mempool code to do that, which is reasonable. You might want some miner with 1% of the hashrate to have some logic about optimizing for what things they are mining, and rescheduling and when they mine it or something.

Wallets should already be doing these rebroadcast things. It's more important in the OP\_CHECKTEMPLATEVERIFY world that your wallet does this. It's more important in the OP\_CHECKTEMPLATEVERIFY world because the transaction can't be amended or replace-by-fee doesn't work.

I think you can make the case that this should be a daemon as a separate process next to bitcoind. The idea of putting things in Bitcoin Core is that these are things that are important to get right for the ecosystem. Fee estimation is actually critical to bitcoin, so we do have fee estimation in Bitcoin Core. Predicting future fees and based on historical data, it's reasonable to put this into Bitcoin Core.

Mempool relay fee could change dynamically in theory. Mempool is, I'll consider accepting this after it relayed. If it's sitting in my mempool, I'll continue to send it. Your mempool has special-case stuff for things that are your transactions. I don't know exactly what that interface is. But in general I think the wallet does not put things into the mempool it's treated as a separate unit. If you're a miner, you would obviously prioritize your own transactions. A payer's wallet software if they want to give a guarantee of payment, their job is not done after they broadcast it.

## Receiving OP\_CHECKTEMPLATEVERIFY payments

If you assume the "long chain" is sufficient fee to be in the mempool for relaying... the wallet will just show an unconfirmed parent, but they won't know the extra metadata that the wallet should trust this as basically confirmed. If the wallet properly understands CPFP, then they would understand that, and they would try to do a spend from their unconfirmeds. In Bitcoin Core wallet, you will do unconfirmed spends from your own transactions because they are considered change to your own wallet.

If it's insufficient for the mempool, it depends. Some services have a less restrictive mempool policy. Maybe they can have a terabyte of mempool and they just keep everything they have ever seen and they write everything to disk. Some people have complained about blockchain.info doing that because it can interfere with replace-by-fee. If it's insufficient for the mempool, the user will need to submit the transaction to their wallet manually.

How does the payee determine whether or not they have been paid? It doesn't seem onerous to say, you have communication with your.... Yes, I agree with you it's reasonable, I'm just presenting what it is. If you don't learn about it through regular broadcast and mempool, then someone needs to give it to you.  When you put something into the mempool not sure if you check if it's something that is yours, and prioritize it that way. I don't know.

Once it's in the wallet, I think it should work kind of okay. You can manually do opportunistic CPFP where you do consolidation when fee is low. The unconfirmed parents I believe do get stored in your wallet. In a lightning context, you need to backup your node and use watchtowers, so it's not a new burden over what we already say you should be doing. If you lose your wallet metadata you can already lose funds today because of HD keys and non-HD keys and things like that. The point earlier is that if you don't have robust backup then the employer still has the obligation to provide it. In the case where you're batched with a bunch of people, like one of those 100 people would have to have that data.

So the idea is to have a non-interactive out-of-bound... to provide proof that you have paid a wallet that has not upgraded yet. You already have this in bitcoin it's called blockspace. Email is a bulletin board. If you can't learn any data, then you can't use bitcoin. This is data you can learn outside of blockspace, you can learn it out-of-band.

Bitcoin should not be viewed as robust storage. It's robust ability to validate storage. You could run a pruned node and throw away transaction data anyway. We also have proposals for txout proofs. OP\_CHECKTEMPLATEVERIFY is an on-chain txout proof. The txout proofs say we're not going to store this at all, and this pushes the obligation on to the clients to store their UTXOs and information but they get pushed to do more of the work. See also utreexo.

Users should already be storing the unconfirmed transactions relevant to them, but wallets aren't necessarily used to having this responsibility and perhaps assume the transaction stays in various mempools on the network.

## Fees

So do you overpay, or wait for fees? This is really simple and works today. It's either expensive or slow and it's not flexible. This is the first order obvious answer: either wait, or overpay your fees. Most protocols can handle this.

Child-pays-for-parent is the next obvious way of paying for fees. This uses a child transaction to subsidize their parent transaction. You get to bid the fee rate when you make that transaction. It turns out that the mempool is bad at this though, and there's pinning and relay issues.  And maybe needs carveouts for specific applications. Another drawback is that it requires that you spend the output you had. If you didn't want to spend that output, maybe it was for something else, and maybe you have to spend from your allowance to get your allowance is a little weird. It would be nice to treat it as two separate layers. Lastly, for CPFP, it's child-pays-for-parent not children-pay-for-parent so you don't get the optimal fee sharing. You have a slightly less optimal fee sharing structure because you're only looking at the best possible child, rather than the sum. So you basically have to overpay.

Gas outputs fix one of the CPFP issues which is that your child was for something else. With a gas output, you just have an OP\_TRUE output. You have to include a dust amount on these outputs or something like that. If someone else comes along and says howdy ho I want to spend this as well, then your transaction gets removed, invalidating your bit because someone else is spending on the same path and now you get to bid on this again. There's a nice behavior around the atomicity of paying these fees.

Gas inputs: this is the inverse idea. Rather than paying up the tree, you pay fee up the tree. So say you have some initial thing, and you add a new input to it that is fulfilling the same role. You specify all the inputs that can go in, and you can still get co-opted in the same way as before, like someone could be like instead of your fee I'll add one instead. If you had one part that got stuck, you can replace it with another thing. But this creates more gas outputs in the side transaction. You're pouring fee into the top, so the child pays for parent first ancestor acceptance problem goes away because you're able to get the parent confirmed. This is parent-pays-for-child basically. The issue with this is txid malleability. In this case, one thing that you might want to do is if you wanted to make use of this capability to check who's paying, you could say "it must be one of these people with this key".

Here, gas just means fees. I'm calling it gas because I think there's more literature to this with computational input. Ethereum didn't come up with the word "gas". It's used in formal verification logic and like people trying to prove things and then you can only prove things in the coq theorem prover in a finite case except you know these common infinite things, so people use a gas or fuel argument that gets consumed and then you can objectively prove over it. The other reason I like "gas" is that it feels like you're pouring gas on the problem.

The synthesis of gas inputs and gas outputs is gas I/O where we don't always want to create extra outputs, and we don't always want to have to get the worst of both worlds. You could combine them together-- so someone could add a gas output but it could be ripped out and someone can add a gas input. So it lets someone modify what's going to happen. If in the optimistic case you don't need any extra fee, that's fine, but in the pessimistic case where someone has to go and bump, then you only create the number of now unspent outputs corresponding to the number of interventions you had to make. It permits a lot of flexibility for how people are cooperating and paying fees. You can already make these long chains, and it's not fundamentally worse than what you're doing today.

Q: Does this work with OP\_CHECKTEMPLATEVERIFY today because of the malleability?

A: You can't express it today, without... You can express it today, and you can express it without third-party malleability which is what malleability typically means in the literature. But you can only get as good as n-of-n non-malleability which is that for those gas inputs you made a commitment to the segwit script. The members of the n-of-n set pick gas outputs from a set of UTXOs set aside at the beginning. So then within the n-of-n group they can pick that. They would be segwit CTVs for the gas output UTXO pool. It's minutia, but it does kind of work.

Conditionalizing: you could imagine that you have the gas IO setup. But you could imagine it is conditionalized. Say you specify a different branch with different gas outputs and more fees, and this could be hidden from miners. This can be masked in taproot or without taproot. If it's not going through, you can do it with higher fees. With pre-signed transactions, you can sign a rainbow tree of transactions for different fees and then pick the one you want later. But this causes a huge blow-up and you should prefer CPFP etc.

Time locked flexibility: It's another OP\_CHECKTEMPLATEVERIFY but with two inputs... in the first week, it has a certain plan but after a week you add the ability to add another input. You can slowly peel off signature by signature, if nobody else is around then maybe they don't care about malleability or something and maybe they pay the fee.

New fee opcode: This is all garbage, right. It's a lot of complexity so why are we doing the fee stuff? Why not just have a fee opcode? What I presented to you is interesting for programmability separate from fees. But for just fees, then the long-term approach is that we probably want a fee opcode. This is not specific to OP\_CHECKTEMPLATEVERIFY. We might say, count my fee against this other transaction. This is much better for the ecosystem I think. You might want to say the outputs are only OP\_RETURNs and they have 100 block timeouts so no validity in a reorg... you might want to guarantee that your gas payment transaction is atomic with the rest. There's a few ways you might want to think about doing it; this is good for OP\_CHECKTEMPLATEVERIFY, good for lightning, good for a myriad of things where re-signing for a fee issue is a huge pain in the ass. So I think a new fee opcode is the way to go. What I like about this is that there's no reason we couldn't do this, and you can overpay on fees until we get there.

What about a new general opcode? OP\_CAT could add more flexibility that would make it much easier to dynamically add a fee input or fee output.

Q: Making a tree of transactions, using OP\_CHECKTEMPLATEVERIFY or otherwise.... the fee requirement has to be varying, not just going up monotonically.

A: I think we want transactions to be confirmed faster, and OP\_CHECKTEMPLATEVERIFY helps you get that. You can confirm the root and get the other ones later. The fundamental question is, is interactivity a reasonable assumption? I think interactivity is not a reasonable assumption. If I am an exchange and I want to pay 10,000 customers. Being interactive makes this really hard or impossible, and therefore OP\_CHECKTEMPLATEVERIFY offers this and pre-signed transactions don't.

Q: Fees are going up and down. I am trying to schedule when I want my payment. So I want to do something to pay less fees.

A: It's not just that. It's faster confirmation. Say that fees are 100 sats/byte. Say I want to confirm 10,000 payments. When I go to issue those 10,000 payments, they are bidding against themselves in the mempool. You're driving a big surge in a feedback loop of fees for the mempool. With OP\_CHECKTEMPLATEVERIFY, you have 10,000 people and we do the two-phase commit. Rather than pay 100 sat/byte, I'm going to pay 200 sat/byte and get something small into the mempool and sometime later we can roll out the other transactions without paying more.

The mempool is an orderbook for the fee rate, and yours is a dark pool orderbook for the fees.

Fundamentally, this is an economics question. There are three issues. Fundamental economics issues aren't won by making arguments. You need empirical data or a strong model to suggest one way or another being better. We could argue back and forth on this all day like what are fees going to look like if people act this way or that way, honestly we won't know until we try. That's dangerous. Economics is self-referential system and to say that we can't know what happens until we try it is not enough to get this BIP deployed. We need to do better than saying we're changing the fee market in a good way. I have simulations suggesting that this is radically better. I have not come across a single argument that it is worse... well, except one argument. The argument that it is better, and maybe I havne't allocated time for this in this presentation, but here's some simulations based on a framework I published. If we look through this, I can show you what the mempool looks like over time for different scenarios.

There's a market for confirmation, and a market for resolution chainspace for redemption. In a free market hypothesis, if you believe in free markets, allowing people to choose what they pay for a good and not aggregating goods inherently has to improve it. But what does this do for the network security? We have a huge problem: there's the "mine the gap" paper which shows that if we clean out the mempool, people will stop mining because people want to wait for the mempool to get filled back up. OP\_CHECKTEMPLATEVERIFY helps you have a band of things that need confirmation, and then OP\_CHECKTEMPLATEVERIFY lets you have a pool of things that can get confirmed and rolled out layer. This ensures there's sufficient mining rewards over a much longer timespan. It enables fee sharing over a longer period of time.

BC: Instead of observing and having a requirement about a particular transaction being mined in the same block, what about having a particular txid being spent?

A: The reason why I decided against that is because-- then someone waiting to be RBFed, you just subsidized these other transactions I actually wanted to do. I don't know.

BC: This is a vague thing, but it feels like that in bitcoin it's very conservative and there's this idea that a transaction shouldn't be able to influence things that aren't any of its goddamn business.

A: I think it's an exciting thing, maybe we should open a mailing list discussion about what that could look like. Instead of child-pays, it's more like "someone cared". This is really good for an abstraction between transactions being understood as intents and wills, and fees saying this should be sponsored by someone, and these responsibilities should be separated. The bigger issue with child-pays is graph traversal, which is why child-pays doesn't work so well. In order to look at the mempool, it makes mining and transaction selection an n^2 algorithm.

For each thing you're considering including, if including it requires a lot of other things in the blockchain, then you add up the sum total and look at the fee per byte. The issue for this is that you need to traverse all the way up. With a new fee opcode, you would structure it as expressing the dependents directly and it doesn't propagate upwards. This is the difference between an idealized perfectly rational mempool, and this opcode runs in mempool code is really bad. I have some optimizations for mempools that makes this faster, and applies to the fee bumping opcode.

BC: I think a lot of the same issues apply to fee-bumping as for child-pays.

Fees are complicated. One thing that is true across anyone who is working across crypto spaces is that fees are complex. In every project, people are struggling to figure out how to pay fees. The first order solution is to overpay or wait. That's the status quo across the industry. However, I do feel good that there are some mechanisms that we can introduce over time that we can ameliorate this with over time.

Is this economic change good for bitcoin? Is more people using bitcoin good for bitcoin? That's what this is doing: we're finding a way for people to use bitcoin. No, you're decreasing the total transactions going through... No, today you can never go back in time and use latent blocksace. Unfortunately there are blocks in the past that aren't full and you can never recapture that value. But if you can create a solid fat queue where a miner can always put in, creative a stack of transactions that are always getting put into blocks, you can increase the utility of that blockspace.

The one criticism is the overhead: this is the equivalent of saying, operating systems are bad and you should run on bare metal because there's overhead from a scheduler. If you want ultimate performance, you would have no scheduler. That's a fundamental tradeoff. In the worst pessimistic case, OP\_CHECKTEMPLATEVERIFY decreases overall throughput because of the tree structure, but in the optimistic case it increases the usability of layer 2 protocols and it also lets you cut-through on transactions moving from one company to another. You can tell Coinbase to non-interactively open a channel for you with OP\_CHECKTEMPLATEVERIFY.  If you use radix=4 for the tree case, that's 1/(1-1/4n).. it's like 30% more... If there's a 50% more or savings with being able to use non-interactive setups for layer 2 protocols, then that makes sense. This will drastically improve chain utilization and it's a pretty good tradeoff. This is a question for people who work on layer 2 stuff: will this increase adoption of layer 2? If the answer is yes, then that should blow out the 30% we talked about earlier.

Q: That sounds like a strong presentation of your argument... but it's a shift of the withdrawal from an exchange batching.. I'm suggesting that, as someone has identified a shift in your strongest argument.

A: It's not necessarily a shift so much as I've been trying to build this from first principle up. We need to present batching because this is what everything devolves into. So I presented lightning and non-interactive lightning. You're building up a future where it's easy to do non-interactive initialization of layer 2 protocols. You can go to Coinbase and give them an address that opens a channel and they don't even have to realize that. So maybe they are payment pools and they spend into a payment pool or something. Prove the fundamental is good and not deleterious. But if you apply these probabilities up the stack about do we have optimistic cases, then it's really good.

Q: I think that's the wrong approach. You've tried to find different use cases, which you have done great. I think that's detrimental to your effort. You really need a good use case for which OP\_CHECKTEMPLATEVERIFY is a really good answer. What I see instead is maybe we can do this and that. There's a lot of ways to do a lot of things. This isn't going to convince everyone, and it's terribly confusing. What would get it through is having a really good problem with a really good answer for which OP\_CHECKTEMPLATEVERIFY.

A: There's running code. You can immediately do vaults and batch payments, you can do this already today.

Q: You've done a good job, but we need to find out if any of these are killer apps.

This is just software and it's open-source, and anyone can get it while cloning.

If you want to do a soft-fork, you need to defeat the other ways to do this which don't require a soft-fork, you need an overwhelmingly strong use case that cannot be done.

So is interactivity okay or not okay? Jeremy said no. We were talking about this-- what would other ways you could do this with pre-signed transactions? We were talking about that at lunch while you were getting food. Say batch payments and child-pays-for-parent are easy to do with presigned transaction and you need interaction for secure key deletion for the n-of-n setup. So it's that interactivity is the big difference and when that's clear, and it comes really clear in the second layer stuff.... I felt that your strongest argument had centered around those cases, and you explained that batching to get us up to thinking at that level.

Batching is an abstract and strange place. How do you build a better wallet? Does deleting a key result in a better wallet? If you do CTV, is it any different? Is it a better wallet? This comes down to, can I make a security analysis around this that convinces someone that this is more secure? Or that some application is more better solved through OP\_CHECKTEMPLATEVERIFY?

In lightning, you already need durable memory, in the same way you would need for OP\_CHECKTEMPLATEVERIFY.

There's another big advantage to OP\_CHECKTEMPLATEVERIFY over pre-signing everything which is that if you want a vault that is somewhat dynamic that can pull stuff out at varying rates, you couldn't ever possibly sign...

With OP\_CHECKTEMPLATEVERIFY you can have malleability and you can have different fees if you allow for malleability. How much slower is a signature than a hash? It's like 10-1000x slower. Maybe this is getting into the weeds into things that should be supported or hackery tricks of how to apply this stuff, but it should be possible to use these hashchain-style covenants by being careful about what you're pre-signing to, so that you can have a vault that was dynamic in terms of the actual amounts where you still have to pre-sign out this one linear thing through the whole thing where the amount can vary.

One of the things I think is cool is that there's sort of... an optimizing compiler that optimizes how it compiles. If you have a program that has branches that exist more than once place in the program, you only have to compile them once. So say you want to emit a payment that is 10, 20, or 30, that is going to be the same branch each time. But yes, the txids do change in those, so you do need to link against those objects that's true. You don't need to link ahead of time, actually, if you had better separation between this is the output and this is the program.

The hashchaining needs to be done through scriptpubkeys not the txids.... If you have dynamic logic at each step to figure out the txid, but the thing you preset ahead is what the scriptpubkey is of your output. So you could have a number of options in your scriptpubkey... No, it's all the same scriptpubkey and you know what these are going to be every step of the way, but you don't know what the exact amounts are going to be.

... you could have the ability to write a limited set of pre-conditions and post-conditions and then you have a fixed list of pre-conditions and post-conditions. Pre-conditions can be things like, enforcing "this other transaction was mined". You express all the possible end states, and whatever end states you have that's what you have.

You can do this with OP\_CHECKTEMPLATEVERIFY as you have envisioned it, where part of the solution is here how the other output scriptpubkey gets filled in, and then you OP\_CHECKTEMPLATEVERIFY the whole thing and it only enforces the one thing that it really wanted to enforce. That sounds correct. This makes it so that it is much more powerful than simply pre-signing transaction.

Q: Why did we need to... why do we need to know the txid for our tree why? So why is that in your BIP?

A: The underlying reason for that is that, in the use cases that OP\_CHECKTEMPLATEVERIFY is designed to really excel at, you want to be able to build layer 2 protocols on top of it. You also want to simplify wallet support. If you want to have both of those properties, not malleating the txid is actually quite useful because you can just tell someone here's the txids to monitor ,rather than here's some abstract representation of my program. For a lot of this with txids you can have bloom filters applied across the entire block.

Q: But what lite clients look for today is scriptpubkeys, and maybe you want to work within that regime.

A: Yeah, that's a fair counterargument. The issue is that, in a more general flexible thing, you can imagine malleating the scriptpubkey. Not if it's a segwit hash or something like that, but if you're doing stealth addresses or things like that. You can't just rely on SPKs in some case. Conner would know better about filters.

A: It's all scriptpubkey.

So fundamentally keeping the txids the same is not incompatible with scriptpubkeys, since they are fixed, but it's a simpler way of knowing what state you're at and what your options are. If you dynamicaly adjust fields, then you need to introduce logic to figure out what the change bit is. If someone is changing the amount of money or moving into the transaction, or I want to know the money going in... I don't want someone to be able to change that. If you want to change someone to be able to support that, it's OP\_CAT... But for prime order use cases, it's not like, it's not that useful and I think most of the time, you would be trying to squeeze it into something that isn't malleating txids.

Q: It seems that transactions themselves malleate strictly more than scriptpubkeys.

A: Yes, that's reasonable. That's fundamentally true because a transaction is composed of scriptpubkeys, so therefore it has to be more malleable. But this is in the weeds.

Q: So what I expected was that, the safety criteria would be harder to evaluate. But the only thing I heard you say is that it would be easier to write clients to understand OP\_CHECKTEMPLATEVERIFY the way it is specified now.

A: The security arguments are inherent. I will make a mea culpa that, I've been up here for a long time, but yes, those too. One of the major reasons for something simple and restricted is security. Introducing all these flexibilities into a script that you can introduce in validation, it opens the door for consensus failures and things that we don't fully understand how they might work. With OP\_CHECKTEMPLATEVERIFY we really understand the security perimeter around, and it doesn't violate many core assumptions about how transactions work. If you had an arbitrary covenant system, you could have all kinds of weird malleations that miners could apply because if it's being passed into the witness then anyone can manipulate a transaction in unknown ways. If you have a predefined set of end states, it's easier to verify that those end states are what you want. But if it's made through computation, it's much harder to prove that the end states you don't want aren't there, which means you're not trying to prove what's there but rather what's not there which is fundamentally harder. Something like OP\_CHECKTEMPLATEVERIFY makes more sense for a foundational layer, which is why the standard type that is defined is very limited. We don't really have super robust use cases for the other ones; we have good ideas, but we know some stuff we can do for the very restricted case like for layer 2 and vaults. We can do that today, let's keep it flexible enough to make new stuff. I think OP\_CHECKTEMPLATEVERIFY is a simple enough proposal, it's worth its weight in gold per line of code. It's not too complex, and it doesn't violate rules, and maybe it's worth advocating for this change. I think all of these factors point to OP\_CHECKTEMPLATEVERIFY being a reasonable change for bitcoin.

Q: Do you have any stats on how much fee that batched payments would have saved during the fee market top back in 2017?

A: The problem with empirical analysis on bitcoin is that it is a chicken-egg issue. Fees are really low right now, so a lot of this is like why should we care since blocks aren't full... But I thikn those arguments are weak because I want to live in a world where everyone is using bitcoin all the time. I think what makes it secure is having more people using bitcoin. You don't even want batching; batching adds security risks.

Q: No specifically in 2017 when we went through fee events, and when exchanges made the switch to batching.

A: The problem with batching is that it's easy to get wrong. There's some subtle security issues. If you do batching wrong, you can screw over the exchange. As you do incremental RBFs, you need to hold a property of common UTXOs... or a batch not having a common UTXO, and they can both be valid transactions. So batching with RBFs can be hard. It's not hard to do, you could say- analyzed all possible reorgs up to 12 blocks, and we set our confirmations for 12 blocks or more... But you could run into an issue where you confirmed one, but if that transaction was undone then this would enable a new batch or something, so you need to look for that for batches too. You always want an output that you chain the last one based on, which guarantees linearization and serializability.  So you should chain previous batches.  You also want to chain on recent deposits, as well, in your giant batches. In ethereum, you can't do that, but in bitcoin you can express the dependency order in which the transactions can get confirmed.

We need some technologies that will let users who- you might not think that users know this implicitly, they couldn't tell you this- but in aggregate, markets know that bitcoin isn't efficient, so we need some new tech to be able to postpone confirmation and make the fee market more efficient precisely so that users will show up, in the infinite wisdom of markets that currently realize that bitcoin isn't efficient and therefore they don't want to use it.

Q: The business model of all the people in the ecosystem has been to add more shitcoins, rather than making bitcoin better.

A: That's out-of-band, we can't solve that.

Q: If the idea is to get exchanges to implement it, that won't work. They don't care.

A: Yes, but there are incumbents, and a newcomer might be able to offer lower fees and outcompete the established exchanges.

Q: For vaults... In the wallet ecosystem, Trezor and Ledger spent a lot of time implementing shitcoins. All the devices are part of a multisig protocol and there needs to be mutual device authorization. If I have two trezors in a vault, they need to... most of the complexity is around knowing that the devices are doing the right thing.

A: That's a fair point. With OP\_CHECKTEMPLATEVERIFY, say you have a high-order compiler, and then some third-party can say hey look here's a vault we programmed, we have a script, we have a server that compiled it, and maybe here's a zero-knowledge proof that it was compiled correctly, here's the thing. That's the minimum possible, but also you could compile it yourself. But you could say, look, I'm concerned that one lapto is hacked, so now I have multisig and now I'm running the compiler on all my devices to check that the script is correctly compiled. You can check a setup with OP\_CHECKTEMPLATEVERIFY and also audit after the fact.

Q: That logic has to be in the hardware device or in the Trezor.

A: I might be an extremist here, but I think there's no such thing as secure hardware. There's secure devices, though. What makes a device secure is that you know the provenance of it and so on.

Q: Yes, but the question is "should you sign it". This is supposed to be part of the vault, and you want to ensure the funds are only going to the hot wallet or only back to the cold wallet. At the time that I am signing, you have to have the computer.

There's protocol layer, and then there's audit/compliance layer. Those are two separate concerns. The protocol layer, I have these addresses from these people and they sent me a request for withdrawal, and then I make that. For them to have that money, doesn't require any further communication, it's already theirs. They have to learn the transactions maybe, but they have to learn those anyway. But getting authorization and approval for, would be for constructive receipt which is a legal doctrine that says if I hand you a dollar, that's a receipt, but if I send you a check via fedex then that's not constructive receipt. If I send by USPS, then it is constructive receipt. If it's a check, and I wrote a date on it, then that's also constructive receipt for that date being correct. I was trying to figure out how OP\_CHECKTEMPLATEVERIFY works into a constructive receipt case. So we email these things to your preferred email address, and we will retain a record for this so that if you inquire about this in the future we can provide it. That's already have exchanges operate; they legally have to provide these logs to you. You might have to go court otherwise, and so businesses provide this to you on demand. If the exchange goes out of business, and you didn't save the transaction and you didn't upload it to the Internet Archive, then you have a problem but that's the same as losing your private keys. You could setup watchtowers and send this data to those too. Nobody can interfere; you can even bake in a reward.

Q: I'm trying to get to the point where we have a really good use case, and then this is a really good answer.  Maybe fees is the answer. Exchanges have the wrong financial  incentive for the fee use case. For vaults, the only people who do it are the hardware wallet manufacturers who sign it, and they also don't have incentive to build this hardware right now- they build shitcoins not bitcoin improvements.

You separate the audit layer and signing layer. Then you can have an audit machine, and also signing devices and also a bitcoind. The vault wallet case is an attempt to get higher guarantees.

If you can have one piece of hardware, or minimum quorum of that you personally set, to audit to know what you're signing, that this is sufficient to make this functional for some set of people. The goal is to ensure a higher degree of reliability. With a Trezor, you sign one thing. With two Trezors, you do multisig.

With OP\_CHECKTEMPLATEVERIFY, I can hire an external third party auditor who has no involvement and can sign a certificate assuring that the protocol is complete and does the thing.

I can build a wallet that is more insurable through better auditing... there's a few ways to do that. Another way is to define what's more secure. The way I try to define that is multiple points of compromise, compromising multiple devices. With multisig you'd think it's n-of-n. But when you do this, it's not so simple to figure out how many things need to be compromised to violate the properties of the vault.

Q: I think there is going to be an evolution of hardware. They will get really good at partially signed bitcoin transactions, which they're not good at right now. At some point, your hardware instead of displaying the address you're sending to, will display the hash of the partially-signed transaction it's signing, and you could compare that with your audit statement from your external auditor or your multi-device auditing system's output.

It has to know more about the tree. Where am I in the state system? It's not an auditing question. It's operational.

Q: Is the question how to reduce the human cost so that a computational auditor can provide this?

A: No the question is how to make the best case for OP\_CHECKTEMPLATEVERIFY. It's a different discussion than CTV.

Q: If the reason you're pushing OP\_CHECKTEMPLATEVERIFY is for vaults, then you must talk about hardware.

Well, it's more than about vaults. I'm going to want hardware that wants to show the hash of the pre-signed transaction. I'll be happy to show you the wrong hash and sign something else. I'm not going to sign the wrong hash because I have the other computers that I trust. So now you have cross-device mutual authentication, so device 1 knows what device 2 is doing. What? Not necessarily.

Suppose that with OP\_CHECKTEMPLATEVERIFY you want a small hardware module and it can load a small amount of metadata about what your intent is, and then it can load a couple signatures to check. It can't compile anything or run anything. With CTV, eventually, with support, it would be possible to construct a zero-knowledge certificate that the compilation was correct. You can use compcert- certificate generating compilers. So you say here is the source code, here's a screen that shows the contract you're agreeing to, and here's a proof that this hash. So it's a simple device that checks ZKP. There's evil maid replace firming, and the certificate doesn't me any good. Evil maid attack.

Hardware is difficult, so I am going to table the discussion. If you're going to say we want a vault, then we need to argue that OP\_CHECKTEMPLATEVERIFY makes this better. OP\_CHECKTEMPLATEVERIFY enables composable non-interactive programs which is a big deal. Now you don't need to move funds from Coinbase to cold storage, you can move them from cold storage to a vault. So one of the advantages is that when you do a pre-signed transaction, the device generates a pubkey and gives it to you. But when you use OP\_CHECKTEMPLATEVERIFY, there's a round of interactivity that is removed, because you already know the pubkeys in your vault because they haven't been replaced by an evil maid attack or other adversary.

Non-interactivity is the thing. Being able to provide something and not have to get coordination, is a big enabler for all of this stuff. The hardware stuff is valuable in that we need to push to have more reliable hardware, but it seems like another angle in which we make bitcoin better. If we do get to better hardware, it doesn't invalidate OP\_CHECKTEMPLATEVERIFY and make pre-signeds look really viable.

It's about implementing a wallet and knowing how it works. We can do the vault with 10 copies with bitcoind, and then we have to look at this and say is this actually better. We're talking about an enabling technology, and this is the barest layer. It's going to be five years before people build up around this. It's going to take a long time to have a robust technology stack that makes bitcoin usable. We have to get primitives right.

What I heard out of this discussion was that the abstract argument about non-interactivity is really critical and it's a little difficult to get across. It's also a good argument. It's a little abstract as an argument. But this is the case for taproot; there's a lot of excitement by authority or something, but deep down it's just privacy and multisig, so it really that exciting? We need to have a primitive enabling it.

Taproot is like OP\_CHECKTEMPLATEVERIFY in the sense that you're delineating things that can happen in the future. You can emulate taproot in OP\_CHECKTEMPLATEVERIFY, like if you say this transaction has to be confirmed with this child, and then you expand out the tree. There's a similarity, but taproot is more in script space. But being in the transaction space allows you to sequence and split funds, whereas keys don't let you do that.

# Deployment discussion

We have about 30 minutes left. I think it would be useful to shift into deployment and share some thoughts on what I think deployment could look like.

Q: I know you have all these slides, but why not just go UASF user-activated soft-fork?

A: We didn't get segwit because of a Core release, but rather for UASF. But we don't really know. All we know is that it could happen. Buried deployment, in our actual code base, once we know that something was deployed at a certain date, then we can set that date. One of the things is that we can set that date to be the earliest date at which we saw no conflicts, so we can push the buried deployment as early as possible. The truth is that we don't know what event caused segwit to get activated. We could argue that any of the activation mechanisms caused segwit to get activated, but honestly it's probably all of them. The number of people doing UASF influences how likely it is that a versionbit soft-fork is likely to activate. What's the threshold of people boosting the... so who activated it? I have no idea, can't tell you.

Q: The goal is for this to be non-contentious, and then UASF doesn't matter. bip9 is easy and a good idea.

Other soft-forks have used various mechanisms. We don't have a great track record on bip9. We have used other mechanisms in the past. BlueMatt sent a message recently. Luke-Jr says bip9 is a proven failure. So we should do bip9 and if it doesn't happen in a year, then after 6 months after that, we do bip8 with a 2-month horizon. I think this is naval gazing with rational arrogance: if only everyone was rational then they would all agree with me. I think people typically feel that way. The issue with bip9 is more about the proposed changes rather than the mechanism itself. Any mechanism would activate a change that everyone agrees to. So any mechanism that everyone agrees with for that everyone likes, will activate that change. This is fundamental for most reasonable mechanisms. In order to make a soft-fork, if it's during contentious times, it's probably going to be harder. We've learned some of these social dynamics and people have left the community- it's just not the same.

Q: Why was segwit controversial?

A: asicboost was a part of it, but no. I understand that narrative. The asicboost argument is like a 12x increase in computation, is that enough to block a feature that is helping to increase and improve bitcoin? Maybe. The broader context is that one group had one proposal, another group had another proposal, and both sides were passionately in favor of their own proposal. And then it blew up somehow.

Q: If the change doesn't impact the miners, then they won't signal.

A: The change has to impact the miner; they have to believe it improves the economics of bitcoin, improving the viability of mining. So anything has to effect the miners.

Rehashing segwit2x is probably not the best use of our time here so let's move on.

So my proposal is, let's just use bip9. It's there. OP\_CHECKTEMPLATEVERIFY looks pretty good. The implementation of it can be independent of taproot. I'm proposing to use bit 5, and taproot can use another one. In terms of start time, I don't have a proposal there. Is 95% a good threshold? I don't know. I don't advocate for lowering the threshold. I think 95% is a good way to do consensus. But what about 10% of the miners being checked out and not following along?

I gave a presentation called [Spork](https://diyhpl.us/wiki/transcripts/stanford-blockchain-conference/2019/spork-probabilistic-bitcoin-soft-forks/). The sooner that you make the activation and there's reasons to... the sooner you make it, the less they care because it will activate anyway. If miners think this is going to activate sooner than later, then there's less of a game for delaying it themselves personally. So if we take Matt's proposal... if the miners aren't impacted, then they will make it the very end of the period. Miners are already heavily discounted for hardware cycles, so if we think that something is going to make mining a better investment for a future set of miners... but if it's a small set of miners saying it's bad for us, but bad for mining overall as an ecosystem... the question is what draws in the most investment capital into mining that makes us the biggest network? A lower threshold might be the answer then.

If it's 95% threshold, then you actually only need like I don't know 89-85% of mining to signal to get it to activate it in a year, because in a year you have 26 rolls of the dice for a period to have enough signaling. What's the chance that one of those goes above 95% because you have 85% of the mining, it's pretty good. This is not specific to Spork, this is just bip9 versionbits. If you have 90% of miners approving in bip9 versionbits, then it will get deployed. It's not an obvious property, but if you do the math, the estimation at the bottom of this slide shows that.

The point of spork was to say it is costly to signal, and you have to really consider it and not make it trivial.

Here's four different timelines of what it could look like: now, soon, "soon", and later. I'll call "soon" maybe mid-term. Who wants this "now" in 4 months? This is the start and end of the activation window and then have enough signaling for it. You have from the point of time that you merge release parameters to the time that you make an actual release, that gives you extra time. So when do you open a mainline pull request saying this should go in? I was thinking maybe after this workshop we open the pull request in March.

You don't want releases to have soft-forks. Historically we have had new soft-forks happen in minor releases backported to all the previous supported versions.

There's a hangover from segwit activation and all this deployment discussion is a hangover from the segwit activation issues. I don't think we should wait for taproot. I think it makes more sense to parallelize and see what gets more review sooner. Taproot has more review, but the need for review in taproot is significantly greater than the need for OP\_CHECKTEMPLATEVERIFY. But the number of use cases for OP\_CHECKTEMPLATEVERIFY might necessitate more review. OP\_CHECKTEMPLATEVERIFY has no new cryptographic assumptions which makes it easier to review than taproot which fundamentally has new cryptography assumptions. There's one person in this entire audience I would look to for reviewing that cryptography. Getting that level of detailed review is really tough, and OP\_CHECKTEMPLATEVERIFY doesn't have that problem. The standard of review- if you're saying it's best to make one go through and see what the other is-- then OP\_CHECKTEMPLATEVERIFY would be better for that.

Q: Say I am a lazy miner and I have hacked my cgminer code 3 years ago... and I want to know the absolute minimum lines of code that I can implement to just ignore all these transactions and not create invalid blocks. Do I have to implement all the lines of code that you have in my pull request?

A: You only need to implement the opcode. You don't need any of the standardness anyway. All the standardness rules aren't required for miners, although a rational miner would want that, but a miner that doesn't have development capacity...

Q: In your head, rough estimate, say we have n lines of code in the set of pull requests, how many are you selling to me the lazy miner?

A: Can I play code golf? I can get it down. If I wanted to be aggressive, it could be probably done in 100 lines of code.

Q: Okay, so that's what you're selling to me.

A: I'd be happy to produce that; I'd rather have one implementation across the board.

Q: Are there any smaller soft-fork proposals on the table?

A: Maybe policy becoming consensus? But those are scary, like hey you have broken my old p2sh wallet or stuff. Matt proposes getting rid of OP\_CODESEPARATOR, who knows if they are used anywhere in p2sh scripts, right?

Q: Say I am a lazy wallet author, and I want to ignore OP\_CHECKTEMPLATEVERIFY and let users deal with not seeing their transactions until they confirm in the blockchain.

A: Fundamentally I think that exchanges early days using batching.. it's not too complicated, if they take the burden of making the second one get confirmed for lazy fee bidding or something, sure. Users call up exchange support desks and then they lose revenue basically. If there's ecosystem support and people get ready for it, that could be day 0, because there's no wallet changes required you just see things that look like normal transactions.

Q: With the arguments that ... this will reduce miner fee revenue if this goes through.

A: That's like saying toll revenue goes down because people carpool.

Q: You don't have fee bidding wars because they are hidden.

A: My fee rate on the small OP\_CHECKTEMPLATEVERIFY transaction can actually be a lot higher.

The miners don't know that a given output is a tree is a tree... The service provider isn't going to pay 1000x more. Why would you pay more than the going rate? Paying saves you fees, to guarantee placement in the next block you can't do it, but there are fee rates that make it very likely. So pay that, but I am not going to pay 1000x that amount. At equilibrium, everyone would be paying the same amount they would have paid before. This is the topic of economic bundling. When you bundle economic goods, you can always provide more value by bundling.

The other thing to remember here is that we have a lot of simulation of lightning which is another transaction compression mechanism. The simulations show that at scale the fees from lightning will be higher than if lightning did not exist. It's like the paradox where as something is more efficient then more people use it. So you get more users, more mining revenue, more fees. If it was the case that OP\_CHECKTEMPLATEVERIFY decreased miner revenue, then bitcoin would be better off having one transaction per block. A more fundamental point is that decreasing user fees with basically an unbound cap on user growth should inherently increase fees total because there's a difference between what I'm paying and what the whole network is paying and I can not shoulder that whole burden. Lightning does this: yes individually per payment and you can consider individual payments as users, yes the fees are pretty bad. But if you're based on the number of real users, your comparative goes up.

Q: So what is the argument that total fees are going to go up if you make a bip9 proposal for activation. Make a solid argument that fees are going to go up.

A: Well if you just say fees are going up, users might say they don't want that. But the nuance here is that users individually aren't paying much more. Communicating to users that your personal fees are going down is more urgent. Miners are more rational and can draw the connection. If there's a savvy miner, what you should argue is that your revenue will go up. Not necessarily that fees will go up. If you argue to the miner that this increases the ... that bitcoin as a currency, then that will increase their revenue. Just focus very specifically on the difference between inputs and outputs is too reductive. You want to convince them that the total utility of the network and the coins goes up.

How are people feeling about OP\_CHECKTEMPLATEVERIFY ? I know we didn't go in depth for the actual implementation. But if there is nothing up my sleeve on what I presented, how is everyone feeling about deployment? Are we assuming all the mempool pull requests are part of this, or already in? I think the general way, even in taproot, there's no wallet support for taproot. Nobody has even started to look at wallet implementation of taproots. I don't know what the mempool would need for taproot in particular; I don't think there's any changes. Let's assume that the mempool stuff will be in progress for a while. I'm working hard to get it going before a soft-fork would be available. It's the tree case that is a little harder to work with, which entails general problems with mempool that other people are already working on. Assume develoment of mempool and everything continues in the pace it continues previously. Given that we don't outside this room; we should feel what we're comfortable with without gauging other people. Once code is final, how much time should we have? What do people feel about that? They all have the bip9 12 month standard activation period. Do people want to see a start date in this quarter, or one that is a half-year away? Are we thinking we want to wait another year? This informs me as to what makes sense to spend time on.

Some people were upset about getting a BIP number... So opening a pull request about it on Bitcoin Core might be bad if it's too early because you don't want developers to dogpile and knee-jerk reaction, because then a year later the developers would say it's not ready yet, so the idea is to open the pull request when it is likely to be generally accepted by developers. A draft BIP doesn't mean anything; people get draft BIPs all the time. If you want a BIP number, it's just a low bar of review. I think people... it's gratifying when you get the thumbs up on github, but when there's a draft there, people should understand it's a living document that will be amended probably. I think opening a draft BIP is more like RFC style to put things up and invite feedback from the community and get more eyes.

I think the only way to get around this whole process argument.. is to wait until another soft-fork deployment has happened. If everyone waited for that, then we would have no deployments. If I do it tomorrow, then people will viciously attack my character. If I open the pull request for this tomorrow, will tweet anything? No. Well, then it doesn't help me... The kneejerk reaction is going to say... If people come together and give a concept ACK, and these are people who have reviewed it and want it to go through, then that's fine. I'd want to make sure that developers would be willing to advocate for it.

I've been thinking about vaults for a long time. I wrote a blog post in 2016 about it. I still haven't figured out the criteria for myself to figure out if any given vault mechanism is the right one. I think building a wallet would finalize it. When we have a functional wallet that does what we think it does, then that helps finalize this. There's a lot of organization, orchestration, watchtowers, stuff that has to be done. Once I understand those things and I think this approach is good-- and again there's many benefits for using OP\_CHECKTEMPLATEVERIFY over pre-signed transactions-- but as we got into writing a wallet, we discovered a number of things we were surprised by. It might seem simple, but there's a lot of complex details like building devices, wallets, watchtowers to control this, know it works, know your state, know the state of all the UTXOs, these trees are terrifying because how do you map that to a state machine... and the state space is large.

The lesson to learn from is MERKLEBRANCHVERIFY. It was an opcode proposed by maaku proposed as an alternative opcode and there were two variants, one with MERKLEBRANCHVERIFY as a script opcode and one that was a segwit type, and it got subsumed into taproot. It never got deployed, it got subsumed into taproot. Short of code maintenance liabilities, taproot was really searching for a silver bullet that would solve all the problems for the things people would want. But that's bad because Mark said we should have MBV to make scripting more powerful and enable people to build new things, back in 2016, and had a well-thought out and well-reviewed proposal that could have gone through.... and then the segwit concussion was much stronger so people were even more afraid of these things. As a general principle, I would want to just do something that enables more competition and innovation. I think a lot of these questions about do we have exactly the right primitive. We're probably close enough that there's enough room for experimentation.

Ultimately soft-forks are at the whims of a few set of people who have large followings. Ideally you want bitcoiners to be thinking for themselves, but these peoples comments can be hurtful for deployments. So creating a perception of a coordinated effort might be bad and not actually help. The only people who care to say something are people who are against the idea, which is detrimental to getting it through. I think bitcoin is for everyone and bitcoin review is also for everyone. If this is interesting to you and it solves a problem you care about, then you can individually make a difference by looking at it and saying something publicly.

Sounds like you need an assurance contract for BIP approval, where either everyone pays or nobody pays, or the set of people say this is worthwhile or nobody posts their approval.

Taproot became a search for silver bullet. People have quit bitcoin because of not being able to get a reasonable timeline on the things they wanted to build.  Some people had something clean enough that they thought was ready to go, but some other people said we don't want to support it because we're going to come up with something better. This argument becomes worse over time, and there's always one more thing you want to cram in. The other side of that too is that from a user perspective and bitcoin freedom perspective and shoving things on people, it's kind of unfortunate that we have to adopt Schnorr and Taproot at the same time. There are people really into schnorr and not so much taproot and now you have an inability to express a preference. I am personally okay with taproot and I think it's well-designed and should get in. To keep bitcoin pure, we should find small things that compose well and then allow people to express dissent without sinking the whole ship.

Q: Could we get this thing on litecoin next week?

A: Sure, call up Charlie and let's see. I think I have DM'ed him on instagram, but he didn't respond.

Okay, strawpoll. So it sounds like everyone who is okay with "now" should be okay with a little bit later. No? Oh. So maybe the right thing to do is set like 6 months and that would, and plus one month from today because it's 7 months, which is closer to the 8 months one. If over the next month, we could take enough review and get some confidence for a pull request with that, and maybe we could open the pull request on valentine's day as an act of love for bitcoin.

We have dinner reservations at a random restaurant.

# Follow-up questions and issues

* Are there any particular use cases that OP\_CHECKTEMPLATEVERIFY is overwhelmingly good for, that cannot be solved with current existing primitives? For example, is non-interactive vaults a better way to do vaults? Or do you still need some steps in your protocol to verify your keys with your hardware wallet devices anyway? How many rounds of communication are you really eliminating with OP\_CHECKTEMPLATEVERIFY?
* Is congestion control possible with pre-signed transactions?
* Besides exchanges, what are the other use cases for batched congestion control transactions?

* market for computing the n^2 child-pays solutions? for miners. pre-compute and send this data around? miners pay for pre-computation optimization of transaction orderbook ordering?
* a covenant with output script template with masking? Instead of committing to the whole script, allowing certain variables.
* reduce interactivity requirements for pre-signed transactions (n-of-n secure key deletion trusted setup) for batched payments (withdrawals from an exchange?)

