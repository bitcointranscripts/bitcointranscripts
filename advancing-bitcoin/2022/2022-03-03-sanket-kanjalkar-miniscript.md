---
title: 'Miniscript: Composable, Analyzable and Smarter Bitcoin Script'
transcript_by: Michael Folkson
tags:
  - miniscript
speakers:
  - Sanket Kanjalkar
date: 2022-03-03
media: https://www.youtube.com/watch?v=Bn1CWsqt3VQ
---
Andrew Poelstra on Miniscript: <https://btctranscripts.com/london-bitcoin-devs/2020-02-04-andrew-poelstra-miniscript/>

## Intro (Jeff Gallas)

The next speaker is Sanket. He is working at Blockstream and is mostly working on Simplicity and Miniscript and that is also what he is going to talk about, Miniscript. Please welcome Sanket.

## Intro (Sanket Kanjalkar)

Good morning everyone. Today I will be discussing Miniscript which is a work of Pieter Wuille, Andrew Poelstra and me with input from many Bitcoiners. It has been changing constantly since summer of 2019 but now it is in a fairly stable state to share and get more deployment. The title is “Miniscript: Composable, Analyzable and Smarter Bitcoin Script”. A brief background, if you are interested in any of these things feel free to reach out to me after my talk and we can chat more about these things.

## Problems with Bitcoin Script today

Just to motivate Miniscript I want to discuss what are the problems with Bitcoin Script today. At a super high level, when Satoshi designed Bitcoin it was a really big step to think about “No I am not going to pay a person but pay to a script based program that you can satisfy”.

## Learning Bitcoin Script today

This gave rise to a notion of Script where you have some instructions to execute, a program to run, which is run by all the different network participants to see whether a certain transaction is valid or not. But the design in principle has a few issues. Firstly it is hard to reason about. I know a lot of us Bitcoiners correctly advertize the fact that it is limited in expressive power, even if it is limited in expressive power we just don’t know how to analyze script. If I give you some sample random bytes you can’t semantically analyze it. Until we have something like Miniscript deployed Bitcoin is just something where you pay to a person whereas this is a more generally composable framework. It is difficult to use and almost all tooling, a Xapo wallet or even multisig, it is a shame that when we say multisig we have to associate a complex word with it. Conceptually speaking it is not that complicated. Still you have all custom tools for Miniscript, you have a 3-of-5, you want to change that to something else, then you need Bitcoin experts to analyze different things. This is an example from [BOLT 3](https://github.com/lightning/bolts/blob/master/03-transactions.md), one of the Lightning HTLCs.

```
OP_IF
        ## Penalty transaction
        <revocationpubkey>
    OP_ELSE
        `to_self_delay`
        OP_CHECKSEQUENCEVERIFY
        OP_DROP
        <local_delayedpubkey>
    OP_ENDIF
    OP_CHECKSIG
```

We’ll go through this example later, this is copied as it is, looking at this it is not really easy to see what this is trying to do. You have experts who can look at this and figure out what this is doing but it is not that easy to figure out what the script is doing.

## Using Bitcoin Script today

The other issue with Bitcoin script is that if you want to argue correctness of the script, let’s first focus on the perspective of a user. You are not a wallet developer, you are a Bitcoin user and you want to custody your coins into a complex script for better security. There are a few things that you want to have good semantic answers for. The first of them is “If I have access to certain keys, let’s say my cold key and some other keys, can I always spend this complicated Bitcoin script?”. If I give you some script blob today it is not that easy to figure out whether that is correct or not. You want to be sure that as long as I have these keys no one can steal my coins, even though you are engaged in a complex multiparty setup. You just can’t analyze these things today. Secondly you may also be interested in “These keys should not ever spend my coins unilaterally”. If I am in a multiparty contract with another participant and they have these keys, given a script you want to be able to reason about things where the person alone cannot spend these coins unilaterally. Other things which you might be interested in, malleability vectors. For example with the Segregated Witness upgrade we solved the most common third party malleability but it is still possible to write complex Bitcoin script which are inherently malleable if you don’t program things correctly. You want to know statically whether all possible satisfactions, all possible spending paths, for this script can be spent in a single way so they can’t be malleated by anyone. It would be a big problem for example if you are spending a transaction and you set some fee for it, assuming that the satisfaction is 100 vbytes witness, someone malleates it and it is suddenly 10,000 vbytes, your transaction is not confirmed. If you are relying on some Layer 2 protocol then suddenly it becomes a security issue if your transaction is not confirmed in time. You can’t analyze these things. If I had to highlight one thing which Miniscript provides it is composition. Currently you cannot compose script policies. If you have say one Bitcoin Core wallet, one Green wallet, name your favorite wallet, maybe a hardware wallet, and you want to have a cold policy where you want to have 2 of these 3 keys. Let’s say Green wallet has internally its own timelock. You don’t have any way to compose these scripts correctly in a high level tooling way. You need Bitcoin experts to understand things and write them for you. Then again it just becomes a one time tool that only works for that particular script template. In most interesting use cases you have this generic composability, your wallet should only care about the part that they are interested in. You have all the other stuff that they don’t really need to understand. They just need to semantically know that this policy is acceptable to them. The hardware wallet needs to know that without its keys the policy, the script, cannot be spent. It just needs to provide a signature. You might also want to check other things like change outputs and so on. You have a structured way to reason about Bitcoin script whereas previously it was just some opcodes that you wanted to execute.

## Rethinking Bitcoin script

With this let’s try to rethink Bitcoin script so that we don’t have these problems. We cannot get rid of Bitcoin script, it is there, it is consensus code so unfortunately we are stuck with it. But can we do something smarter with the things that we already have?

## Spending policies

For this let’s look at what people use Bitcoin script for. The three things that people most use in Bitcoin script are public keys, where you do signature verifications, you have hashlocks which are the basis for the Lightning Network, HTLCs or any other swap protocols, and you have timelocks where you have an absolute timelock or a relative timelock that specifies after some time you want to spend or at some time you want to spend some funds. And you want to compose these things. You want to say this Public Key 1 AND this hashlock or this timelock AND this public key or maybe you have a threshold which is kind of in between, you need 3 out of 5 things to satisfy this fragment.

## Some simple policies

To get familiar with things let’s look at some simple policies. The first thing just indicates that Alice should be able to spend the output which is just `pk(Alice)`. If you have some 2-of-3 wallet you would have a threshold with 3 keys `thresh(2,P1,P2,P3)`. Or if you have something complicated with a co-signer like Green Wallet you can encode these things that are not Bitcoin script but are the way in which you think about Bitcoin script. If the user `U` or the Green co-signer `G` signs then you can spend the output OR after 90 days the user `U` can spend the policy.

`and(U,or(G,after(90 days)))`

Some other complicated things like the Liquid sidechain control of funds, you have functionaries in a 11-of-15 multisig and if they don’t respond then you have a 4 week timelock after which some emergency keys can be used.

`or(999@thresh(11,functionary_keys),1@and(after(4 weeks),thresh(2,emergency_keys)))`

Policies are the most basic way to think about things.

## Miniscript and Script

Let’s see what Miniscript is with respect to Script. Miniscript is Bitcoin script. We just want to think about in a different way. Technically speaking it is a subset but we have some structure. With stack based languages and random opcodes thrown in there you don’t really have a structure to it. But if you have a program, programming relies on trying to compose things, trying to understand things locally. You want to build a bigger complicated program with smaller components. You want generic signing where you have some complicated policy, for example this is a 2-of-3 multi where either A, B or C can spend it or after some time, 10 blocks CSV, some emergency key E can spend it.

`or_d (multi(2,A,B,C),and_v(vc:pkh(E),older(10)))`

This is the same Bitcoin script that you would write using Bitcoin opcodes but instead of thinking about it in a Bitcoin script raw byte format you encode it in a more structured way. Because you have structure things are easy to semantically analyze. Just looking at this you can easily see this is an OR and if I have A and B I can spend it. Because it is structured you can write software which operates on the structures and can answer things like “If I just have the emergency key and no blocks have passed can I spend it?” This can output things for you. There are some weird things `d`, `v`, `vc`, those are some technical details about how you want to use Miniscript, rules for composition but users can just ignore these things. Those are for people who want to write Miniscript but if you want to semantically analyze what your Miniscript wallet is trying to do you can just ignore those details. The `pkh` you can just assume those to be individual components. You can just forget that those things exist when you are trying to analyze Bitcoin script. Technically speaking Miniscript is Bitcoin script. The idea that you can write a high level language is not something new. People have thought about these things previously. There have been compilers which have been written. There are a couple of unique things about Miniscript. Firstly it is Script. It is not getting compiled into another language. If you are given a script you have a one-to-one mapping between Bitcoin script and Miniscript. If you get a corresponding Miniscript you have Bitcoin script. But even though the underlying thing is the same and the interpreter is executing it the same way it represents a different way to think about things. A good vision for the Miniscript project would be that the developers should just forget that there is a stack. There are some instructions you want to execute, there is a OP_CHECKSIGADD which takes in 3 parameters and does so and so things and adds `1`. You should just think there is a `multi` and I just need conditions to satisfy. Instead of some instructions to execute to the script machine we want to think in terms of what conditions do I need to satisfy to execute these things. All of the underlying work for converting Bitcoin script to Miniscript and Miniscript to Bitcoin script is done by the Miniscript stack itself. Developers should just think about what they care about. You as a developer know what threat model you are aiming for so you should focus on that and let Miniscript handle things like how you want to describe or how you want to encode things into Script. Instead of a stack like approach Miniscript has a functional, compositional approach which really helps us do these things in a structured way.

## Miniscript <-> Script Translation

check(key)
```
pk(key)
 <key>
pk_h(key)
OP_DUP OP_HASH160 <HASH160(key)> OP_EQUALVERIFY
```
X or Z
```
or_b(X,Z)
[X] [Z] OP_BOOLOR
or_d(X,Z)
[X] OP_IFDUP OP_NOTIF [Z] OP_ENDIF
or_c(X,Z)
[X] OP_NOTIF [Z] OP_ENDIF
or_i(X,Z)
OP_IF [X] OP_ELSE [Z] OP_ENDIF
```

These are some basic examples of how Miniscript translates to Bitcoin script. The fragments are constructed in such a way so that you can always go back and forth between those two things, there is no ambiguity. For example `pk` just translates to `<key>`. The `pk_h` is the popularly known PKH fragment where you do `OP_DUP OP_HASH160`, you don’t do the CHECKSIG, it is just pushing the key onto the stack. Then you have different ways of doing ORs. But the key idea is to semantically understand script you just ignore `_d` `_v` rules. The Miniscript encoder will help you figure out how you need to compose these things to create a correct script. But when you want to semantically analyze these things it is much easier to analyze these fragments.

## Miniscript: A bird’s eye view

At a very high level each Miniscript expression has some base type (`B`, `K`, `V`, `W`) for interaction with the stack. It has some type attributes (`z`, `o`, `n`, `d`, `u`…) to argue about correctness and non-malleability. It has some wrappers (`a`, `v`, `c`…) to convert between types and modify attributes. And some combinators to combine these types (combine Miniscript with `and`, `or` and `thresh`). Think of it like a programming language, a very rough analogy. You have different types and there are rules of how you want to compose these functions together. These rules are determined by the Miniscript type system. In order to convert between these types you have wrappers. Engineers can look at these things, it is not terribly hard to figure out how you need to compose these things. You can write Miniscript by constructing a Policy and then get a Miniscript that represents a Bitcoin script such that the Policy is mapped one-to-one. You figure out how you need to compose things. Or you can write compiler tools that operate on Policy and output Miniscript.

## Composability and generic signing

To give one concrete example to see the full power of Miniscript, when you want to have some generic signing or a composable script. We talk a lot about multisig, people say that is a complicated script and that’s the reason we have all custom tooling around it. Today if you want to participate in a threshold 3-of-4 setup, let’s say you are a big company and you are doing custody, I am one of the participants and I have my own custom setup. For the same reasons you have a multisig I don’t want my own single key to be just one thing that I write down on a paper wallet. I also want that to be some multisig or another complicated protocol. To do that today all of these things need to understand what exactly this script template is. If you look at wallet code, some wallets look at this byte at this index and figure out this is the public key and so on. These things don’t directly compose nicely. But if I want to have some policy where I’m allowed to do something like “This is my own threshold and I have my own setup with me. A and all these other guys should not force my policy onto me. I might have my own policy where I can use `C1` and `C2` if I have those. This is a degrading timelock example. After `100` time I can use just `C1` or `C2`. This is what we want to aim for, composability. If I want to sign for any of these keys then I would create signatures with PSBT support, participant A can give a signature if it wants to participate in this policy. Because of Miniscript’s structure it can understand this and it knows that either I alone can spend this or A, B and C can. If it wants to check another thing semantically it can but otherwise it can just provide a signature on this script. The Miniscript finalizer, the PSBT component that assembles the witness can figure out how to create the final witness for this script. You can have signatures of `A`, `B`, `C1` and `C2` and then it will figure out if they are in some Tapleaf or if they are in some other location. If in another subpolicy you have all the required signatures you don’t need any custom tooling, the finalizer will look at the PSBTs, check the signatures and assemble the correct witness. Wallet developers can forget about the stack, use PSBTs and Miniscript, forget about how the script executes, give it sufficient witnesses and the Miniscript finalizer will do the rest for you.

## Semantic analysis

`or_d(multi(2,A,B,C),and_v(v:pkh(E),older(10)))`

This is how a Miniscript will look like in a textual format. These would be descriptors, this is a Miniscript and if you just want to look at semantics you ignore these underlying words here. Software can look at this and easily reason about things. Is it possible that after some time I can spend with my emergency key? Yes. If I have A and B I can spend. Answering these questions is much easier if you have this structure.

## BOLT 3: HTLC received example revisited

`t:or_c(pk(rev),and_v(v:pk(remote),or_c(ln:older(9),and_v(v:hash160(H),v:pk(local)))))`

Here is the HTLC received example. I looked at the script and I handled it, it is not even which exists in tooling, there are tools which help you do this, construct a Miniscript from a Policy. This is much more understandable to software and to humans to reason about things. One of the advantages here is not only it has structure but you can write tools that take some spending policy and output Miniscript or a descriptor in case of Taproot where you split it into multiple scripts. The good thing is that computers are good at optimizing things. Experts trying to optimize Lightning with minimum script weights, but a compiler piece of code produces optimal scripts for HTLCs which are better than hand written scripts. Similar for the Liquid sidechain, there were scripts that were written by experts but computers are good at brute forcing and figuring out optimal things. The average case satisfaction cost for this Policy is much better than what you would have in the Policy specified. But the key point here is because it does Miniscript it works with everything else. You have a 3-of-5 multisig, one of them is a Lightning wallet controlled by the BOLT 3 policy, inside of that it is composed of some other key. If the finalizer and the updater in the PSBT understand Miniscript everything just works. You don’t have to worry about opcodes, you don’t have to think about script. And if you want to analyze things semantically you can write software where you can say “Can I always revoke with my revocation key if someone broadcasts a previous state?”. You can do it and this is easy to understand. Not only that but it gives you this nice composability which will help all future wallets, you can interoperate. If you have some custom setup and you want to move to another wallet you import keys and they won’t work. Or you have a 2-of-3 and you want to import it somewhere else. If you have Miniscript descriptors supported then you just import the descriptor and they will figure out how to spend them and how to sign them.

I’ll talk a a bit about the Policy compiler. With the Policy compiler that can do more complicated things. For example in Jimmy’s (Song) [slide](https://btctranscripts.com/advancing-bitcoin/2022/2022-03-03-jimmy-song-taproot-multisig/) we had different ways in which you wanted to spend your policies and have 2-of-2, 2-of-3. You just give it the Policy, that will output a descriptor, that tells you how to satisfy it. You don’t need to worry about how that works. Miniscript has done that for you. You just need to know “This is my Policy. This is my compiled descriptor.” If you don’t trust the compiler you can look at it semantically and see whether that satisfies the conditions you are interested in. That’s not implemented currently, MuSig support, but even without that it will do complicated things like figuring out which things you want to place on the upper level of leaves, where you want to place things so your average case satisfaction cost is minimized. If you add MuSig support to it then you can figure out these keys are MuSig compatible, I can place this as the internal key or this should be at level 1, this should be at level 3. Because we have this structure, Miniscript is Bitcoin script, this really opens the door for writing different compilers. There is one compiler in rust-miniscript, there is a compiler in C++, you are welcome to write your own thing. The point here is after you’ve produced Miniscript you can do sanity checks, you can figure out whether this is the Policy you are interested in.

## Miniscript in practice

To summarize, Miniscript is an easier way to write or reason about script. Forget opcodes, forget how they work internally, think about satisfying conditions. It is composable and you can have generic signing. If after darosior’s work on Bitcoin Core, that will be one of the wallets which will support generic signing for SegWit v0. You have BDK and some other wallets that are using Miniscript. You can create complicated policies between those things and that will just work. Only the finalizers and the updaters need to understand what Miniscript is. For example if you have a dummy hardware wallet signer, I know some hardware wallets are interested in figuring out whether the change is spent to them, or if you have some custom signer somewhere it just needs to sign the PSBT. It needs to figure out what it is and put the signatures in there. The Miniscript finalizer is smart enough to assemble a witness from all the signatures, all the hash preimages. Finally Script has some weird conditions, there are weird limitations on the stack limit. You can have timelock mixing. Even if you have some Policy which you want to compile into Bitcoin script because of the weird interactions in Script it might not represent what actually ends up getting executed. For example one of the parts can have more than 201 opcodes. You look at it, you semantically analyze it, you say “Ok it is good” but when you try to spend it you suddenly can’t. The network rejects your transaction. It statically helps you determine whether your script has such things. We have a bunch of things in the Tapscript update, one of the reasons for having CHECKSIGADD is because `multi` was annoying to deal with statically. We now have better opcodes that represent different things. As I highlighted we can have Policy compilers that output Taproot descriptors so all the examples which Jimmy mentioned Miniscript will do it for you.

## Q&A

Q - Does Simplicity make Miniscript obsolete? Or are we anticipating that a lot of people will continue to use Bitcoin Script?

A - The advantage of Bitcoin Script is we have Bitcoin Script today. If you want Simplicity in Bitcoin that would be another soft fork. Simplicity is not ready yet. People have different opinions. It will render it obsolete if it ever gets in. It is not at that stage. Simplicity can do everything which Bitcoin Script can do but it is not there today. Whether we want that or not it is a different question.

## More resources

Finally, there is a Bitcoin Core PR by darosior. You can look at the [reference](https://bitcoin.sipa.be/miniscript/) and ask more questions. People have built nice front end tools which help you think about script so you don’t have to worry about these things. You can look at these various implementations to use in your own project. For example rust-miniscript is used in the BDK wallet project and Sapio. And if you are a wallet developer you should use Miniscript because it will help you interact with the rest of the wallets in a seamless way. If you are designing a new wallet, unless you are doing something very funky the scripts you write are already Miniscript, if you can support Miniscript fully you have this generic signing capability. In the future when I have a Lightning wallet or Trezor or Ledger or Jade I can just work with them.

Reference: <https://bitcoin.sipa.be/miniscript/>

C++ implementation: <https://github.com/sipa/miniscript/>

darosior PR to Bitcoin Core: <https://github.com/bitcoin/bitcoin/pull/24148>

Rust implementation: <https://github.com/rust-bitcoin/rust-miniscript>

min.sc: <https://min.sc/>

BDK compiler playground: <https://bitcoindevkit.org/bdk-cli/playground/>

miniscript.fun: <https://miniscript.fun>

