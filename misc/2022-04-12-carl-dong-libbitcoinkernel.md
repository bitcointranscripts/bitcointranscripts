---
title: libbitcoinkernel
transcript_by: Michael Folkson
tags: ['build-system']
speakers: ['Carl Dong']
date: 2022-04-12
media: https://www.youtube.com/watch?v=MdxIkH6GCBs
aliases: ['/chaincode-labs/2022-04-12-carl-dong-libbitcoinkernel/']
---
Tracking issue in Bitcoin Core: <https://github.com/bitcoin/bitcoin/issues/24303>

Pieter Wuille on Chaincode podcast discussing consensus rules: <https://btctranscripts.com/chaincode-labs/chaincode-podcast/2020-01-28-pieter-wuille/#part-2>

## Intro

Hi everyone. I’m Carl Dong from Chaincode Labs and I’m here to talk about libbitcoinkernel, a project I’ve been working on that aims to extract Bitcoin Core’s consensus engine. When we download and run Bitcoin Core it is nicely packaged into a single bundle, a single application. However those of us who have studied the blade know that Bitcoin Core just like most applications is in fact a collection of subsystems. Those of you who have attended meetups like BitDevs before or used the Bitcoin Core suite of applications and toggled the options or just know a little bit about Bitcoin Core architecture will perhaps recognize some of these names (wallet, GUI, RPC/REST/ZMQ, consensus engine, P2P, mempool). At the heart of it all though we have what I call the consensus engine, otherwise referred to as simply validation. Why did I refer to the consensus engine as the heart of it all? Why is it so gosh darn important?

## Consensus engine

It is because the consensus engine is the subsystem which keeps track of all the blocks and the UTXO set. In fact if you look in the right folders on your machine you can find these files. Not only does it keep track of the blocks and the UTXOs it is also the arbiter of truth when it comes to what constitutes a valid transaction or a valid block. Essentially it is the piece of code that defines what the Bitcoin blockchain is. That is why it is so gosh darn important. Since the consensus engine defines what is valid it is crucially important in a distributed system such as Bitcoin to make sure that the consensus engines of all the participants all agree. When a new block is mined and the consensus engines disagree between nodes that’s when unintentional hard forks happen. That’s the nightmare scenario that keeps Bitcoin developers up at night. Now I’ve hammered home how important the consensus engine is I’d like to return to our map of the Bitcoin subsystems.

## Bitcoin subsystems

When I lay it out like this on the slide everything looks so nice and tidy. It almost seems like we’ve got a well organized codebase. However the reality is in fact much more like this (spaghetti). The main problem here is the tight coupling and entanglement between the consensus engine and the rest of the codebase. It means that there is an ambiguous and ill defined boundary between what is part of the consensus engine and what’s not. That leads to problems. I hope you guys aren’t getting sick of me saying the phrase “consensus engine” but I am going to say it a few more times. For example it can sometimes be unclear when we make a change to the Bitcoin Core codebase whether or not it affects how our consensus engine behaves. Remember what I said before about how disagreements between the consensus engines of various participants and nodes across the network can lead to catastrophic forks. You can see why this can be a big headache. Resolving this problem, this entanglement problem is one of the key goals of the libbitcoinkernel project. We want to modularize or in other words extract out the consensus engine such that we have a more precise view of what our consensus engine depends on, what is consensus critical and how the rest of Bitcoin Core interacts with it. With regards to Bitcoin Core development itself this also means that contributors and reviewers when they are looking at a change or if they are making a change can have a clearer sense of how security critical that change is. Another big problem that arises out of the need for distributed consensus on the Bitcoin network is that developers with an experimental streak may want to rearchitect parts of Bitcoin Core. They may very well want to replace the peer-to-peer system, perhaps get rid of the mempool completely and send transactions straight to miners. Or wholesale replace all of our RPC mechanisms with the greatest and most efficient RPC system in the world, gRPC. There are a lot of things that you can imagine people will want to do with our system.

## Rust evangelism strike force

Additionally other developers may want to wholesale reimplement parts of Bitcoin Core in another language. If you have a badge carrying member of the Rust evangelism strike force on your team you know exactly what I’m talking about. They are going to want to turn these subsystems into artisanal crafted crates and brag about how they never ever, not even once clone memory. The challenge that these developers of alternative implementations face is they are faced with three options. In my mind they are three bad options.

## PR review

They can try to get the code through the review process into Bitcoin Core. But the Bitcoin Core project wants to avoid too many features and toggles because they bloat the codebase. You end up with the choice of either imposing a maintenance burden on reviewers and maintainers or having features that are not well maintained which is also a problem.

## Fork

These developers may also want to maintain their own fork as an alternative. This is a codebase fork not a network fork. This is a burden on these developers as it is a huge hassle to rebase on Bitcoin Core’s codebase every release or every few releases as the Elements project devs can attest to.

## Reimplement

Or as most do projects and people implement their own consensus engine. That means risking any language specific quirks or nuanced differences in implementation leading to incompatibilities and into unwanted forks which we talked about before.

So extracting out the consensus engine into a reusable library, the thing we’ve been talking about this whole time, means there can be a relatively stable API, or at least relatively stable compared to the internal structures of Bitcoin Core anyway, that these developers can code against and be sure that they are consensus compatible with the rest of the network. Enabling safe and easy experimentation.

On a more personal note, I think that it speaks to the strength of the Bitcoin community that we have experimenters who want to push Bitcoin forward. In other words I think they are an asset and I want to lower the cost of safe experimentation.

## How do we get there?

So how do we get there? How do we get to this promised land where our consensus engine is decoupled from the rest of the codebase and made into a library?

## Prior Art: libbitcoinconsensus.so

Let’s first look at some previous attempts at this problem. Those of you who have followed Bitcoin Core development for a while may know that there was a libbitcoinconsensus, there is a libbitcoinconsensus that was shipped starting with Bitcoin Core version 0.10. In fact it has been shipped with every version of Bitcoin Core since then. However libbitcoinconsensus is an incomplete library. It only supports script verification and doesn’t even manage the UTXO set, the block tree or do any block validation.

## Prior Art: 2016 effort

Following that in 2016 there was a brave effort to complete libbitcoinconsensus which I would characterize as having perhaps crumbled under the weight of its own ambition. It started with building a minimal Bitcoin consensus interface with decoupled storage and caching, with a C interface and perhaps was a little too much all at once.

## libbitcoinkernel - an incremental approach

Given how these previous attempts turned out we need to devise a new plan that takes into account and respects the sheer size of work that is extracting the consensus engine. In my mind this is work that will involve multiple contributors, it is certainly not a one man job, and perhaps will span across multiple releases. I think we need to take an incremental approach to extracting the consensus engine instead of trying to build a perfect library from the ground up out of nothing. What does taking an incremental approach mean?

## What it is?

On an abstract or logical level it means that we first capture a rough outline of what our consensus engine is today. Once that is done we can whittle it down to what we would like our consensus engine API to look like or what it should be. Make it available to other languages via bindings. This whittling it down approach has the benefit of avoiding prematurely optimizing for the perfect boundary and API since that can be highly subjective, non-obvious and probably a hot bag of unproductive bikeshedding.

## Reuse classes -> refine API

On the code level it means that we will also be able to reuse our existing C++ classes, as ugly as they are, and gradually simplify them as we are making bindings available to other languages. This means that we will always have one user, we’ll be continuously integrated with Bitcoin Core. It also means that every step along the way we can benefit from Bitcoin Core’s extensive test suite. Perhaps we can have something like a CI job that enables an experimental configure flag that will link Bitcoin Core against libbitcoinkernel. That will be possible.

## Logistics

Let’s talk logistics.

## Current phase - Extraction

Right now I am in the middle of completing a candidate branch of the extraction phase that will yield a libbitcoinkernel that has a API that’s very Bitcoin Core specific but is usable by an external C++ project. This phase will also include a dummy binary which uses this library and exercises our consensus engine a bit just to prove out that it works.

## Prevent Re-entanglement

What I’ve realized after experimenting with this branch over the last couple of months is that the biggest value add of this first phase, this extraction phase, is that after it is merged any re-entanglement of consensus with new modules will result in linker errors. In essence there is a big value add just to be gained from the first part alone in that we will avoid any entanglement regressions.

## Future - Continual API refinement

My hope for the next phase is that there will be strong collaboration between contributors to continually refine our consensus engine’s interface. At this stage should users of libbitcoinkernel other than Bitcoin Core emerge it would also be incredibly helpful to get their perspective on how the API could be made more robust and how it could be made more ergonomic.

In closing, it is my sincere belief that libbitcoinkernel can be a project that improves the Bitcoin network safety, increases Bitcoin’s longevity and one that enables more consensus compatible experimentation. Thank you all for listening.

