---
title: Script Descriptors
transcript_by: Bryan Bishop
tags:
  - descriptors
speakers:
  - Pieter Wuille
date: 2018-10-08
aliases:
  - /bitcoin-core-dev-tech/2018-10-08-script-descriptors/
---
<https://github.com/bitcoin/bitcoin/blob/master/doc/descriptors.md>

I would like to talk about script descriptors. There's a number of projects we're working on and they are all kind of related. I'd like to clarify how things fit together.

Note: there is an earlier transcript that has not been published (needs review) about script descriptors.

## Agenda

* History of script descriptors and how we came to this.
* What's currently in Bitcoin Core v0.17
* Wallet integration
* DESCRIPT

## About script descriptors

The problem that I wanted to tackle was that currently in Bitcoin Core wallet we have a blob of public keys and private keys and HD chains and scripts and a bunch of other metadata and keypools. They all feed into each other and differently effect what you can sign and what we consider ours. The logic that currently exists about how we determine what outputs are ours is sort of a copy of the signing logic that says "can you sign for this". But with the caveat that for multisig, we require all the private keys to be there. At various levels, whenever through recursing the different scripts involved if there's something you consider something "watchonly" which is a separate set of scripts, then we also consider it ours. There's a distinction between what's solvable and what is watched. Solvable means, would we be able to sign this ignoring that we don't have the keys. Solvability means we can determine what the size of the spend is going ot be, useful for fee estimation, fundrawtransaction, coin selection and those kinds of things. It's very unclear what the reasoning is between the data that is in your wallet and how it effects solvability and spendability and we unintentionally made it worse in v0.17.

Script descriptors are a simple language for describing the conditions for spending. It's a language for computing scriptpubkeys, output scripts, together with all the information necessary for spending it. The simplest descriptor would be PKH(0302....), a hex pubkey with PKH around it means pay-to-pubkeyhash for that public key. This contains more information than just the address because it tells you the actual pubkey involved. At the very least, it tells you whether it's a compressed key or not, which matters to solvability.

You can also do things like SH(multi(2,02..., 04..., 05...)) this means p2sh of a multisig of 3 out of these 3. The language can do all kinds of multisig constructions at least the checkmultisig-based ones. All of this is in Bitcoin Core v0.17 but it's only exposed through a single RPC.

There's laso WPKH() which is the witness version of PKH(). There's also WSH() which is pay-to-witness-scripthash. You can also use these recursively like SH(WSH(PKH(...))) and this will work; don't do it, it's silly. But it works. It just shows the available composability. Also, you can use PK() for a plain pubkey. That works too.

Any place where you write a public key, you can also write an xpub with a derivation path and you can optionally end it with slash star which means all the direct cihldren of this keys. It doesn't refer to a single scriptpubkey but to a not-quite infinite series. The caller needs to be aware of a range or a gap limit. Conceptually, such a descriptor refers to all the children in a certain order.

The goal was to replace the ismine logic in the Bitcoin Core wallet. Instead of importing pubkeys, scripts and all these things, you would import one or two descriptors and say this is the one from which I draw my addresses and this is the one from which I draw my change. There could be some metadata along with a descriptor like where it comes from, do I need a hardware wallet, is this watchonly, what's the birthdate, and all these things become metadata for the descriptor rather than for individual keys. This is not yet done.

Q: What is done so far?

There's a module that implements the descriptors. It parses them, it can export them, there are tests around them. They are only exposed through scantxoutset RPC. You can give it a descriptor and it will go through the entire UTXO set and find outputs for everything that matches the descriptor.

A particular nasty thing that I hope this will solve is the confusion about "well I gave out a segwit address and someone turned it into a p2pkh address and I can't distinguish between-- I can't tell my wallet to only watch one version of it". Maybe I have a hardware wallet that can only sign one of them and I don't want to get confused into thinking I'm being paid by something that I can't spend. The descriptors are intended to be well-defined. We may add extensions to what constructions are supported, but the idea is that what is supported never changes what scriptpubkey it refers to. Given a descriptor string, it's well-defined which scriptpubkey it refers to, and it's intended to never change.

What I'd like to work on i nthe short and medium term is changing the ismine logic in the wallet itself so that you can import records (in combination with a descriptor and metadata). Maybe convert all the old stuff into this new model, becaues it's more compact and easier to reason about. But there's compatibility issues to consider.

Q: What are the compatibility issues?

Well, you can't downgrade after doing this if you convert an existing wallet.

Q: You could do it at loadtime too.

This is not a simple operation, to convert. You have to iterate through all scripts you might possibly watch and feed them through the existing logic. I've implemented this, but even for a simple wallet, it's less than a second but it's painful. There's many combinations to try. Yeah sure you could do it at loadtime, but it's not quite as interesting I think.

Q: What if we keep the old ismine logic for old wallets? That's painful. We have to maintain two parallel tracks.

Yeah, but I think you can encapsulate the new stuff nicely where you say here's the data, apply ismine to it. There's different considerations there. I don't know what the best solution is there.

## DESCRIPT

I want to talk about some of the work we've been working on, Andrew and I and a number of other people at Blockstream. We want to deal with well what if you want to do more complex things with script? We have internal stuff that uses more complex scripts, we have lightning-related scripts, what if I want to do something like a multisig that after some time degrades into a weaker multisig? Like a 2-of-3 but after a year I can spend it with just one of those keys and stuff like that. How can you construct composable policies in script? Script is stack-based execution language that is really hard to reason about. In practice, people just pattern match a certain thing and then oh I know how to sign multisig, or p2sh multisig, or I know how to sign witness embedded multisig... but generalizing this is kind of a pain.

One thing that we came up with is what we're calling DESCRIPT is a subset of the bitcoin scripting language. It's only somewhat related to script descriptors. Let me talk about this first then I'll connect them. It's a subset of script that can embody AND, OR and thresholds (here are a number of subexpressions and k out of them need to be satisfied). It's a generalization of multisig but not just multisig. For example, the situation where I do an escrow of 2-of-3 but one of the participants is using a hardware wallet so it's a 2-of-3 where one of the keys is really a 2-of-2 or something like that. AND, OR, thresholds, pubkey checks, hashlocks and timelocks. I think this embodies everything that people use script for, today. Everything is some combination of those things.

We found a subset of script that is composable where you just say AND translates to this sequence of instructions and in this place you just substitute another thing which can be anything and in here you can substitute anything and so on. We investigated various constructions for this. We have like 5 different ways of writing an OR construction in bitcoin script. Experiments showed that all of them are useful sometimes. Which one is the best one depends on the context, the probability, the complexity of the statements inside.

We have a DESCRIPT compiler that takes something we're calling a policy language (AND, OR, threshold, public key, hashlock, timelock) together with probabilities for each OR to tell whether it's 50/50 or whether one side of the OR is more likely than the right, and it will not find the optimal script unfrotunately but the optimal script in this subset of script that we have defined.

Q: Can you get your compiler to output the lightning scripts?

A: We have not tried that yet.

Q: Do you handle witness malleability?

The scripts that come out are non-malleable by current standardness rules. Making things completely non-malleable under consensus rules is painful. You can't do lightning because you need to check if your signatures are not empty if they fail. I think everything that is non-malleable today relies on standardness rules. Lightning is simple enough that there wont be any failing signatures. Lightning has one specific construction in a few places, like branching based on the size of the input as a way to have it either be a signature or a hash preimage, and that is a malleability fix. Well, we can extend DESCRIPT, we can extend it with more constructions if necessary. We've taken malleability into account.

Q: Is the idea here that this would be something that would future proof the wallet so that if someone uses a script in the future, your old wallet could be made to recognize the script?

The goal here is that we can extend the DESCRIPT language to respond to these scripts as well. You could import them into your wallets as watchonly or more general. Even without a descriptor part, you can have signing logic that works on any of these scripts and doesn't need to understand it. In particular, when we're talking about partially-signed bitcoin transaction operations (PSBT), you can have an updater-- you don't even need the updater actually, the updater can just recognize this is the script we're trying to spend and I know how to spend it, without being told additional information about this is the semantics of the script or whatever. I can go into how it compiles the things but I don't know to what extent there is interest in that.

Q: What about an example of a simple multisig between two wallets?

A: It's just PSBT. Nothing has changed.

Q: What are the 5 OR types?

The simplest OR you can imagine are where you have a subscript A and a subscript B and you use a BOOLOR. But B needs to be wrapped because A is taking its arguments from the stack. The problem is that A is expected to be an expression that puts 0 or 1 on the stack based on success. B should skip 0 or 1 that A produces. So we have a different calling conventions for different subexpressions, we have 6 subexpression conventions. The calling convention E is "take your elements from the stack and put 0 or 1 on the stack". W is the wrapped version and it starts with 00x and it puts on the stack x and then 0 or 1. You compile A in E mode and B in W mode. So now the two things on your stack are the success outcome and you use a BOOLOR and this overall is an E expression.

Another mode is what we're calling a CASCADE OR, which is execute A and only when it fails will you run B. A DUP NOTIF B ENDIF. Here, B can be compiled as an "F" (forced). You could either satisfy A, it puts 1 on the stack, it removes 1 on the stack and you end up with 1 on the stack. You have a 0 going into B so that's wrong... OK, it has to be an IFDUP, which only duplicates if it's 1.  It's a switch-left though. ....... Okay, we have to look this up. IFDUP NOTIF B ENDIF. IFDUP duplicates if it's true. If it's true, then notif will fail. If it's zero, it remains zero, you remove it, and you run B. The problem wit hthis construction is that if you want to make the whole thing fail, so you're going to satisfy A and B, then this is malleable-- no it's not malleable-- this is a bad example. Okay, what we're demonstrating here is why a compiler is necessary. This is a different style of writing an OR which has the advantage that if A is satisfied then B is not even executed, which makes sense if both B is likely to fail and expensive to fail.

You can go even further and have a direct E switch where you have IF A ELSE B ENDIF. This takes an additional input and tells you which of the two branches are going to succeed, and the problem with this is that it's malleable. When the whole thing is going to fail, and if IF select A going to fail, then you can modify it for the IF to take the B branch and fail B. We assume constructing a dissatisfaction is easy. The way we solve this is by introducing another compilation mode similar to an E but it has to succeed and that's the "F" mode for forced. If it fails, it will kill the script. It's only way of failure is abort, and it always succeeds by putting a true value on the stack.

Then there's other things you can do like at the top level we don't really require a script to put the zero on the stack for failure. It can abort. We have a version that is succeed by putting true on the stack, or fail by either putting 0 on the stack or aborting. Then there's a version that-- that's "T", top level. It has to put TRUE on the stack but not 1 on the stack. F does have to put 1 on the stack. Don't we have new names for these that aren't letters? Abort or 1. Then T is either fail or 0, or true (non-zero). This is why you compile top-level constructions as... you have more freedom if you are allowed to fail by aborting. A top-level AND is just concatenate two things, if you make the first one... I need to give you "V" as well, which is either nothing or fail.

An AND in a top-level is a V plus a T where you run the first one, if it succeeds it does nothing then runs the second one. If the first one fails then you abort immediately. This allows you to use the verify version of certain opcodes.

The sixth one is the "K" calling convetion that it's either something that fails, or it puts a pubkey on the stack.  The reason for this is that otherwise you end up with IFTHEN ELSE constructions where both of the branches end with a checksig which is silly, you want the checksig out of the IF. For doing so, you can compile both branches as the K version which guarantees to put a pubkey on the stack, then you convert it to a T by adding a checksigverify after that.

There's a number of pieces here. We're writing up a description of this subset of script called DESCRIPT with its semantics and how to sign for it. This is orthogonal to all the wallet stuff, really. We can write up a description of DESCRIPT, then we can write signing logic for any of these scripts because there's a simple conversion from the descriptor-like notation to the script but also the other way back, using a simple LR parser to look at the script and figure out the structure. It's like a one-token lookahead. It's even simpler than one-symbol lookahead, it's one-token lookahead, you always know and it's not exponential in complexity. LR parsers are linear though. Look into it. You can do it in a linear way; the recursive decent version is exponential though. You don't need a recursive decent, you can use a lookahead parser. You can do even simpler-- you don't need to read any papers about parsing, the obvious thing to do will be linear.

DESCRIPT is a subset of script which you can do a few things with. You can convert it back to a tree form, and given the tree form you can sign it and you know how to sign for it. Then we can add extensions to the descriptor language for this subset of script. So there could be different types of AND, OR with it. Then there's importing into the wallet. The last piece is a compiler from a higher-level policy language down to the descriptor form.

Someone give me a policy. 2-of-2 multisig, or after 1 month it's either of the signatures. So this would be AOR(MULT(2,A,B)) and this is an asymmetric OR where the left branch is far more likely than the right branch, and then you need the other side, so AOR(MULT(2,A,B),AND(CSV(1 month), MULTI(1,A,B)). You could write A as a private key, if you wanted to talk about wallet integration. In the wallet, it's the compiled form. Compilation is kind of slow. The compiler goes from the policy to the compiled script version. The conversion between the policy and the compiled version is a bijection, never changing.

It compiles down to a CASCADE OR, and then there's a MULTI branch, and then there's an.... the CASCADE OR is a T execution style... the multi branch is an E, ... then there's an AND branch.  You're compiling into a descriptor. The policy language is something we haven't specified yet. It does stuff like probabilities. So how to go from a descriptor to a script, that's a bijection. That's an efficient thing in both directions.

The compiler from the policy language to the descriptor is non-trivial. We wrote two versions with different methods, and then compared the two compilers and figured out which one produced the best versions and optimized it by that way. We used the couple first few million scripts and compiled to the same thing. When you're developing your application, you run the compiler once. The AOR stuff is the policy layer. There are three steps, yes. What is the name of the translation from DESCRIPT to raw script is just an encoding. It's just an encoding.

One of the thing is common subexpression; if you write a public key multiple times, that key ends up in the script multiple times. This could be improved.

Ivy is an attempt to do this. It is both a higher and lower level language. It's more general. It uses explicit variables. It says write a script that takes three inputs, the first the second and the third and the first input is the one that goes into this public key. This doesn't do that though, this treats the inputs as an abstract thing and you just write a policy. Here you would say, timelock and multisig and there's nowhere in this langugae no signatures appear. There's only public keys. In Ivy, you deal with the signatures as explicit variables that get passed around.

The BIP will say, this thing you sign this way, this other thing you sign this other way.

You never deal with raw scripts in the wallet; that's what we want to get rid of. You import a descriptor into your wallet, and that's all. And now it has all the information to recognize it and spend it. You generate the script on the fly, but you only store the descriptor. You derive the address when you need to.

DESCRIPT is revenge on the eltoo people for name reasons. I would call existing script FOOTGUN. Maybe this is DOUBLEBARREL.

The descriptor gets put into your wallet. The policy language can be compiled into a descriptor, and descriptors correspond to the subset of script called DESCRIPT. The policy is the asymmetric OR stuff. The descriptor is the abstract syntax tree stuff... the descriptor can be turned into a script, and specifically a subset called DESCRIPT. If the wallet has the descriptor, does it know what the policy is? You cannot go back from a descriptor to a policy, because it loses probability information. So you might want to keep that metadata.
