---
title: Contracts in Bitcoin 
transcript_by: Caralie Chrisco
tag: ['smart contracts']
date: 2020-04-08
speakers: ['John Newbery']
---

Location: She256 Onboarding to Bitcoin Webinar

Video: <https://youtu.be/H-wH6mY9pZo?t=2549>

# Introduction

John: My name is John. I am a Bitcoin Protocol Engineer at Chaincode Labs in New York. I'm going to talk about contracts a little bit from a theoretical perspective, but I'm not a lawyer, and I'm not a legal scholar. For all of you legally minded people out there, I apologize in advance if I gobble this and say some nonsense.

Before I do that, I'm going to tell you a story and the story based on this picture. This is Odysseus and his sailors going past the island of the sirens on his way home from the war in Troy. And the sirens were beautiful women who sang very alluring songs to sailors who passed the island, and any sailors who heard that song would not be able to resist the temptation of the sirens. They would steer their ships towards the island, and the ship would be dashed on the shore, and they would be shipwrecked and devoured by the sirens.

Odysseus knew this was going to happen, and so he had his sailors cover their ears up with wax and wool and ordered them to tie him to the mast. Then he gave him a very strange order and said, "from now on until we get past the island, disobey any of my orders. If I tell you to steer towards the island, disobey me. If I tell you to untie me from the mast, bind me harder to the mast."

So they sailed past the island, Odysseus heard the song the sirens, but he couldn't do anything about it. They say he got passed, and eventually, Odysseus got home to Ithaca. Alright, enough of the storytime.

I am going to talk about contracts and what we call smart contracts. I'm going to talk about this language we have in Bitcoin called script and then more generally talk about contracts on a public blockchain. I'll talk a bit about the history of script in bitcoins who has changed over the last 11 years, and then I'll finish up with some possible future directions for scripts and contracts in Bitcoin.

# Contracts

What is a contract? Well, a contract is, in some ways, a meeting of the minds where two or more parties come together with shared intentions, and it's a situation where there's a common understanding in the formation of this contract. But a contract is also binding.

I might want to borrow money to buy a house, for example. And at some point in the future, I'll pay back that money, but I know that the future me would prefer not to pay back that money. All things being equal, I prefer to keep the money and the house. So I bind myself into a contract where there's a penalty for future me if I don't pay back the money. Because obviously, no one would lend me money if I could just run away with it.

So this is similar to Odysseus, binding himself to the mast. He knows that future Odysseus will want to go and visit the island of the sirens, but present Odysseus enters a contract with his sailors where he limits himself, and so he's bound to the mast just as we are bound to contracts.  

The concept here is limiting future me's freedom. The freedom to renege on my debt or to order his sailors to steer to the island expands present-me's freedom because I can borrow money. This concept of contracts has existed for centuries, for millennia. It is a fundamental building block of civilization and the market economy. We naturally think of contracts as written, but oral agreements count as contracts and have been around since prehistory. People were thinking about this for many years as the internet came online, and it would be impossible to rederive all of the wisdom contained in this tradition of contract law and norms very quickly. If we start from scratch using just kind of reason and first principles it would take us many centuries to redevelop sophisticated ideas like contract law. The digital revolution is coming and is challenging us to develop new institutions in a much shorter period of time than that.

# Smart Contracts

This man named Nick Szabo and he said, "New institutions new ways to formalize the relationships and make up these institutions are now made possible by the digital revolution. I call these new contracts "smart" because they are far more functional than their inanimate paper-based ancestors. A smart contract is a set of promises specified in digital form, including protocols within which the parties perform on these promises." Nick Szabo was writing this back in 1996. If you think of smart contracts as new or introduced by Ethereum or Bitcoin or blockchains, this predates Bitcoin by over a decade, and smart contracts are possibly older than you expected.

A little bit more about contracts before we get into Bitcoin. I'm going to outline some objectives when designing a contract, which I'm going to come back to throughout the talk. One objective is observability that the participants in a contract should be able to observe each other's performance in that contract. Another is verifiability. That is that participants can prove to an arbitrator or third party that the contract is being performed faithfully or prove that it's been breached.

Another important aspect is privacy. That knowledge and control over the contents of the contract should be distributed among parties only as much as it is necessary to observe and perform that contract. Then enforceability. That probably speaks for itself, but at the same time, I should add when we design a contract, we'd like to minimize the need for enforcement or minimize the need to go to a court, for example.

# Script

Enough theory. Enough armchair law. Let's talk about script in Bitcoin. Bitcoin was introduced by Satoshi Nakamoto in 2008, and we know that we can script on Bitcoin. So here's the white paper. Let's have a look for script. Oh, look at that; there's no mention of the word script in the white paper. Or maybe contracts? No mention of contracts either. Let's just scroll down a bit and look at what the white paper has to say about transactions. "We define an electronic coin as a chain of digital signatures. Each owner transfers the coins for the next by digitally signing a hash of the previous transaction and the public key of the next owner."

Okay, so the idea here is that ownership of coins is defined by public keys, and then transfer of coins is executed by creating a signature with a private key that matches a public key. No mention of scripts, no mention of contracts here.

But if we look at the first version of Bitcoin 0.1 that was released by Satoshi in 2009 we do see this function `EvalScript`. The comment here is Script is a stack machine like Forth that evaluates a predicate returning a bool indicating valid or not. There are no loops. Perhaps Satoshi thought that talking about script was getting in the weeds too much for a white paper that was just an overview of Bitcoin. But I think a more likely explanation is that this scripting system, this function was bolted on at quite a late date in the development of Bitcoin. The reason I think that is if we look at where that `EvalScript` function is called, you can see right down at the bottom here is a function called `VerifySignature`, which makes me think that Satoshi's original design for Bitcoin was this chain of signatures and public keys.

But then later, Satoshi added on this scripting language. Why did Satoshi do that? We don't know. We can't ask him. He's not around, but there's this mailing list post from 2010 where Satoshi says, "Once version 0.1 was released, the core design was set in stone for the rest of its lifetime. Because of that, I wanted to design it to support every possible transaction type I could think of. The solution was script. The nodes only need to understand the transaction to the extent of evaluating whether the sender's conditions are met. The script is actually a predicate; it's just an equation that evaluates to true or false. Predicate is a long and unfamiliar word so I call it script."

So Satoshi early on wants to add all kinds of fancy contracts like escrow transactions, bonded contracts for third-party arbitration, multi-party signatures, and so on. And as he was developing Bitcoin, the problem was, each of those special cases required special support codes and data fields, booleans to say whether the function was used or not. It was just this explosion of special cases. So script is the answer. It lends a flexibility to use Bitcoin and supports a tremendous variety of possible transaction types with a very limited set of primitives. Satoshi's reasoning was that if Bitcoin catches on in a big way, that later on, people could explore these different use cases because script was there for people to use. So that's where scripts in Bitcoin comes from and the idea of contracts.
Zooming out a bit and talking about contracts in general on public blockchains and whether they're a good fit for these smart contracts that Nick Szabo was talking about in the 90s. So how do they fit? Well, the good news is observability is good. Participants can all see all the possible parts in a contract, and they can see how the other parties had acted. So that's great. And verifiability is good because the contract is on a public blockchain. Everyone can see it, and participants can prove to third parties that they executed the contract faithfully. And enforceability seems pretty good. The contract is executed, and rules are enforced by all nodes. So you might think at first glance that a public blockchain is a pretty good place for smart contracts.

I put enforceability in yellow there because it's not all good news. In Bitcoin, we have blocks, and they arrive every ten minutes. So if you want a transaction to be confirmed, you need to wait for an average of ten minutes for the first block. You might not get confirmed in that block, and even if you are, there might be a reorg, and that transaction gets undone and doesn't spend. So we never really have a solid idea of finality in Bitcoin. Finality is kind of fuzzy. So enforceability seems somewhat good, but somewhat not good, and there are worse things.

Privacy is terrible. If we want to execute a contract, sometimes we want that contract to be private. That contract might include financial information. It might include trade secrets or proprietary business information. It might include medical information. It could include all kinds of data, and we don't necessarily want the whole world to see all of that. And if we execute a contract on a blockchain the whole world sees everything, not just now, but for all time because it's stuck in the blockchain forever.

Here's another thing: expressiveness. In Bitcoin, we have this limited set of primitives in our contracting language, which, when combined, can achieve quite complex things. But if we ever want to add new primitives, if we want to add, for example, time locks or sequence locks, which we did in 2015 and 2016, we need a consensus change in Bitcoin. Those things are slow and difficult to do and can sometimes get political. So adding expressiveness to the contracting language is very difficult.

Fungibility is a very important aspect of Bitcoin, and if everyone can see all of the details of a contract, the outputs of their contract are no longer fungible. A miner might be located in a jurisdiction where certain kinds of contracts are illegal, and they might find themselves forced or coerced or threatened to not include those transactions in the block, which would be bad for the blockchain and bad for Bitcoin.

Scalability is also not very good if we put everything on the blockchain. It means every single
node on the blockchain needs to execute every step of every contract. We, therefore, have a trade-off. Either we exclude small underpowered nodes from taking part in consensus, or we limit their total throughput of the system. So those are pretty bad things about trying to use a blockchain as a platform for smart contracts.

This is Andrew Poelstra. He's got a really great talk from 2017 called "using chains for what they're good for." And Andrew says, "contracts executed by explicitly published code are really only using the blockchain for one thing - to get an immutable ordering of what order the transactions happen in. All that they really care about is that their transaction is not reversed and not double spent. All of the extra details of the contract execution can be done by things that are not on the blockchain."

# Post's Theorem

I'm going to have one very technical slide, and it's got some symbols in it. This is Post's Theorem. I'm going to talk a bit about logic from the 1930s. So Turing-complete languages -- Alan Turing defines these in the 50s and 60s, as computably enumerable predicates. So like we said earlier, predicate is just a function that returns a boolean true or false.

In the 1930s, Emil Post defined an Arithmetic Hierarchy. So there are Δ0 predicates, and they have no unbound quantifier. So an unbound quantifier is one of these "∀x's or Ǝy", where there's no bound on what it could be. So, for example, for ∀x and the natural numbers, there's an infinite range where it could fall.

Δ0 predicates, all of the quantifiers are bound. For example here:

∀x < z . Ǝy < z s.t.x+y = z.

Then Σ1 predicates are those which contain an unbound ∃ (exist) sign. So for:

∃X in the natural numbers s.t. ∀y>z and x<y.

So the difference there is that these unbound quantifiers have an infinite search space. Σ1 predicates have an infinite search space. Turing complete languages define these Σ1 predicates, which have infinite search space, and that is why Turing-complete languages can contain or can express non-halting programs.

Post's theorem states that computability enumerable predicates, so that's Turing-complete, predicates that can be defined in a Turing-complete language are identical to Σ1. And that validating a Σ1 predicate can always be reduced to validating a Δ0 predicate with a witness. So if I provide you this thing called a witness, this clue, or this data that narrows down the search space, we can convert a Σ1predicate to a Δ0 predicate. And a Δ0 predicate always terminates.

That's a lot of theory. Let's try and re-frame that a bit.

This is Russell O'Connor. He's saying, "In Σ1, I'm going to write a program, and everyone on the blockchain is going to execute this program, and everyone will do the same thing because they're running in the same environment." That would be something like the Ethereum Virtual Machine, where you write a program and everyone runs it. "With Δ0 thinking, I'm going to run the program myself on my computer and generate some witness data, and I'm going to have everyone only validate that witness data instead of running the entire program. It's a change of attitudes that can be a lot more efficient, a lot more private, and save a lot of time."

So by using a Turing-complete language, you're effectively saying, "here's my proposed state transition. Please, everyone, do this unbounded search. It could take forever." That's why Ethereum has a gas limit. Whereas in Bitcoin, you don't have a Turing complete language, we use Δ0 thinking, and those programs are always bound. So we provide a witness.

That's really the difference between computation, where we provide a program for it to run on the one hand, and verification, on the other hand, where we provide a witness. We just have people verify that witness. It's not a binary thing we can move along that scale.

How does this tie into our contract design? Well, if we get everyone to compute everything, that's not private -- it's less private. And if we just give people a witness, it's more private. And in the limit, that would be something like a zero-knowledge proof where we reveal nothing about the data inputs. For our scalability, if we get everyone to compute everything, that's less scalable. It means everyone's doing the same work. Whereas if we do it ourselves and provide witness, that's more scalable. Fungibility is less fungible if you get everyone to compute and more fungible if we just use verification. In terms of observability and verifiability, we still get that with verification, but it's just privately observable. Only the parties in the contract can observe the contracts being run. And same for verifiable -- only parties in the contracts can but only post in the contract can reveal to third parties that the contract has been faithfully executed. I'm going to claim that enforceability and expressiveness are available anywhere on that spectrum.

One final quote, this is from Greg Maxwell. "Is this mental model similar to conventional programming? No. But smart contracts aren't conventional programming, and blockchain isn't a conventional computing environment (how often does history change out from under most of your programs?). These design elements make for a clean, simple system with predictable interactions. To the extent that they make some things "harder," they do so mostly by exposing their latent complexity that might otherwise be ignored."

# How Script Has Changed

That's the theory. I'm going now talk a little bit about how script has changed over the last 11 years, and then we'll look forward to how script and contracts in Bitcoin might change over the coming years.

Here's a transaction in Bitcoin. It has some metadata at the start and the end. At the start, we have a version. At the end, we have a locktime. Then within a transaction, we have one or more txins, so we can see one here. We have one green txin, and then dot dot dot. There can be many of those. SS stands for script sig. Then we have one or more outputs. We can see one here. It's red. We can have many. SPK is the script pubkey. So that's one transaction. We have a second transaction, and the input from that second transaction spends the output from the first transaction.

In the first version of Bitcoin, you take the script sig from the input and the script pubkey from the output being spent and concatenate them and then execute them, and they're all written in the same script language. You can see that from the code that I showed you earlier, `EvalScript` on the scriptsig from the inputs plus this code separator thing, then plus the script pubkey from the output. Well, that was bugged. It was a pretty big bug where anyone could spend anyone's money. Satoshi fixed that in 2010. The fix was just to separate. So, execute a scriptsig first and then execute scriptpubkey. You might think, why is the scriptsig why is that signature a script? All it's doing is providing data. And you'd be right. The scriptsig really just pushes data onto the stack. We can see from this snippet of code that first `EvalScript` is running the scriptsig, and the job there is just to push data to the stack, and then the second `EvalScript` actually runs the script, the locking script, the script pubkey.  

# Pay to Script Hash (P2SH)

Then in 2012, we introduced pay to script hash. This made a change whereas previously, the script pubkey in the transaction output contained the entire script and contains the entire encoding of that contract. In pay-to-script-hash the output simply contains a hash commitment to that script, so a hash commitment to their spending conditions. Then the scriptsig contains the script itself that encodes the spending conditions and the satisfaction to that script.

So it's a two-step process to verify that. First of all, we check that the spending script that is provided by the spender matches a commitment. Then, we have the spending script and we check that the input data satisfies that script. Why do we do this? Well, there's a lot of advantages to this model. One is that the outputs are a fixed size. They're always a 20-byte hash for pay to script hash- 32 byte hash for pay to witness sighash. That allows us to have a fixed address length. It also means that the person sending the money does not need to know what their spending conditions are. So if I get you to send me money to a 2-of-3 multisig, you don't need to know that it's a 2-of-3 multisig. That's none of your business. You just send it to an address I give you. You can't tell because the only thing in your output is a hash, a hash output. So the evaluation for this gets a little bit more complex. You'll see it's similar to what we had before. That at this point, it's just doing the checking that the commitment is a valid commitment for the script that is being provided by the spender, and then this if statement, the bottom half of this, is doing the actual script evaluation with the data and making sure that that data satisfies the script.

Then in 2016, we had Segregated Witness. This is pretty similar to P2SH. We have a commitment in the outputs, but when we move the spending script and the satisfactions to this separate field called the witness, and it works almost identically to P2SH. The reason we do that is because witness is not part of the txid, and that fixes a problem called transaction malleation.

# How are Things Going to Change

Last section. How are things going to change in Bitcoin? We hope that we'll have a soft fork in the next couple of years to introduce a new kind of signature called Schnorr signatures. Schnorr signatures are really nice because they have this property that allows us to add up public keys and add up signatures. So with a Schnorr signature, we can have a spending condition with something like a 2-of-2. So two signers out of two have to sign, or three out of five. By the time they reach the blockchain, it just looks like a single public key and a single signature. So no one else knows that it's a multisig. That's really good for privacy because you're not revealing from the entire world what the spending conditions are. It's good for scalability because there's only one signature evaluation for all the full nodes to do. It's good for fungibility as well.

That same soft fork will hopefully include a technology called MAST or script trees. This is a new way of encoding scripts where you only reveal the branches of that contract that you execute when you spend from the script. Rather than in P2SH where you have a commitment to the entire script and then when you spend it, you reveal the entire script, in MAST you have a commitment to a tree of conditions, and then when you spend it using one of those conditions, you only reveal that part of the tree. That's more private. It's more scalable. It's more fungible.

We can combine those two things, Schorr signatures and MAST, to have a technology called taproot, wherein the very best case where all the parties in the contract agree, you don't reveal any of the tree at all. You just reveal a single signature, and you can just prune away that entire tree.  So again, great for privacy, greater scalability, and fungibility.

Then adapter signatures are something else that we can do with Schnorr signatures. This allows us to make really interesting contracts. For example, atomic swaps where a signature, within just the mathematics of the signature, we encode complex conditionals that we would usually do in script. So the entire script disappears, and all that appears on the blockchain is a single public key and a single signature.

So those are some things to look forward to. We hope we'll get those in the next year or two in Bitcoin. But it's a public network. No one controls it, so we can't say for sure. That's the end of my show!
