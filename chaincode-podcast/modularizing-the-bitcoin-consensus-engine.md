---
title: Modularizing the Bitcoin Consensus Engine
transcript_by: Michael Folkson
speakers:
  - Carl Dong
tags:
  - build-system
date: 2020-12-15
media: https://podcasters.spotify.com/pod/show/chaincode/episodes/Carl-Dong-and-Modularizing-the-Bitcoin-Consensus-Engine---Episode-10-enra84
episode: 10
aliases:
  - /chaincode-labs/chaincode-podcast/modularizing-the-bitcoin-consensus-engine/
---
AJ: Do you want to talk about isolating the consensus engine?

CD: Sure. More recently I have dove into the codebase a little bit more. That started with looking at Matt’s async ProcessNewBlock [work](https://github.com/bitcoin/bitcoin/pull/16175) and playing around with that. Learning from that how do you make a change to the core engine of Bitcoin Core.

## Matt Corallo’s PR on async ProcessNewBlock

https://github.com/bitcoin/bitcoin/pull/16175

AJ: Can you talk about that PR a little bit and what it would do?

CD: Basically right now when we process new blocks from a peer we block everything. That is bad in software that is supposed to be performant and also it is bad for embedded systems or systems with less processing power. The basic gist of it is that asynchronous ProcessNewBlock allows us to be able to process new blocks somewhat asynchronously. I looked into that a little bit. One of the things that I had talked about with Matt and Cory a few years ago was very interesting, which was modularizing our consensus engine. Capturing what our consensus engine is right now, as ugly as it is with warts and all, and seeing if we can perhaps physically separate it from the rest of the codebase. Obviously those are much future steps.

## Carl’s De-globalize ChainstateManager PR

PR: https://github.com/bitcoin/bitcoin/pull/20158

PR review club on this PR: https://bitcoincore.reviews/20158

CD: Right now one of the major problems with the consensus engine is that we have so much global mutable state. Having global mutable state is really bad because when you are looking at a function you consider its inputs to just be its parameters and what class it is a member of but you don’t consider that global mutable state can influence the execution of functions and macros greatly. For something as important as our consensus code we should probably modularize it so that it relies on less and less global mutable state and be able to work nicely. After we have modularized it perhaps we can separate it out. Perhaps into a library like people said about libconsensus a few years ago. Perhaps do something else. That is the first step. This is why recently I’ve been working on this PR to de-globalize a class called ChainstateManager. ChainstateManager was introduced as this manager class that manages multiple chain states. Basically chain states encapsulate our view of a chain and the UTXO set and blocks.

M: For example if there are stale blocks or two competing chain tips, they would have multiple chain states.

CD: That would be one chain state, one chain but two block trees. I think that is what it is. I will explain why there might be multiple chain states. We have multiple chain states in the case of [assumeutxo](https://github.com/jamesob/assumeutxo-docs/tree/2019-04-proposal/proposal). ChainstateManager was introduced for assumeutxo where we will have multiple chain states that are progressing. The active one may switch between one or the other. That’s why we have a chain state. If you look at what our consensus engine encompasses, it encompasses ChainstateManager and all of the objects that it owns and references. That is what I am trying to encapsulate and trying to de-globalize. Because before we had this one `gchainman` that was referenced from everywhere in the codebase. That was getting to be a mess. Also one of the things that is interesting for people who are into the nitty gritty of C++ is that global variables cannot be instantiated with things that are determined after main starts. That is why we have had some very weird ways to initialize these global variables where we initialize an empty one globally and then in main we want to make sure as soon as possible to initialize it with actual contents. There is like a three, four phase initialization. We also initialize it differently between bitcoind and bitcoin-qt and our test code. The combination of having a three, four phase initialization and those means you can have discrepancies between the test code and the main code when you are initializing stuff. It leads to a lot of bugs that are very hard to reason about.

M: Because it is so hard to reproduce.

CD: Yes exactly.

AJ: Nice callback. This is a lot of code that you are changing. The PR that we are talking about is PR 20158. It is 82 commits and 800 lines of sensitive code. How do you test this? How do you structure this for code review? How do you make sure that we’re not breaking Bitcoin?

CD: The mantra stands of getting it to work in a hacky way is very easy but getting it to work in a nice way… Especially if you are needing review from others, it is much harder. I had this working a long time ago but because of how much of the code I was touching I needed to structure it in a way so that every commit made a lot of sense. The review experience that I wanted for this was for reviewers to be able to look at every commit and be like “This is trivial. This is trivial. This is trivial.” By the end they’re like “I just reviewed a bunch of trivial commits.” In aggregate they do something big. This is why I have this piece of paper at home, I think I threw it in the trash, I should have kept it, where I mapped out all the calls within our codebase that relates to ChainstateManager. It looked like a tree and I started pruning the tree from the bottom up. From the bottom these are direct references to `gchainman`. I just said “If you are referencing gchainman then you should probably take in a parameter that is chainman and use that instead.” I basically pruned the tree all the way up and each commit prunes one node all the way up to the top where I remove `gchainman` and all of its things. In the middle I saw that one of the things that could lead to problems is the notion of the active chain state. Most of these functions, what they reach for is the chainman’s active chain state. Now you are passing in a parameter that is chain state but you have no idea which chain state this is. This could be the active one, this could be the inactive one. To make sure I put in a lot of review only assertions. I put in all these assertions that were like “Let’s assert that this chain state that is being passed in is the active chain state.” I put all of these in so that reviewers can run the code themselves and see that there was no assertion error and nothing failed. In the end I have one quick [scripted diff](https://github.com/bitcoin/bitcoin/blob/dca80ffb45fcc8e6eedb6dc481d500dedab4248b/doc/developer-notes.md#scripted-diffs) to get all of them out. Scripted diffs were really helpful during this, especially with large refactors like this where you’re like “I’m inserting a parameter. Oh no it is being called from 30 different places.” Being able to do a scripted diff is not only easier for me to rebase, it is also easier for reviewers because they can just look at the sed script and be like “Ok that makes sense.”

## Consensus engine

AJ: Can I ask some more meta questions? This path is littered with dead bodies of people who have tried to encapsulate our consensus engine. First of all consensus engine seems very deliberate. That phrase is not something that I’ve heard before. Where does that come from?

CD: It comes from the need to not say “consensus critical code.” Because people have a very specific understanding of consensus critical code and people have very differing understandings of consensus critical code. Is LevelDB part of consensus critical code? They might have different answers.

AJ: It was in [0.8](https://github.com/bitcoin/bips/blob/master/bip-0050.mediawiki)

CD: Exactly. That’s for sure.

AJ: The reason that is funny?

CD: In 0.8 there was an upgrade from BDB to LevelDB which caused a bug because of how many locks were available in each one, the limitation on locking. It is very deliberate. I get this phrase from Matt who texted it to me. I was like “I’m going to steal that.” Our consensus code as it is right now, everything it depends on and all the auxiliary things that are needed for it to work, whether it be caching or storage or whatever. That is very deliberate phrasing that I’m using to make sure that I’m being correct with how I say things.

## Past efforts such as Jorge Timon’s libconsensus project

https://github.com/bitcoin/bitcoin/projects/6

AJ: So you are slowly teasing this out and unbundling it. Can you tell us about others who have made past efforts? It sounds like Matt started doing this.

CD: Going chronologically backwards, the last effort was Matt’s effort. Matt is the one who introduced `CChainstate`. Before `CChainstate` there was a primordial soup of global mutable state in validation. He brought a lot of that together into `CChainstate`. That was supposed to be exported as a libbitcoinconsensus but that never happened. That is one of the first steps and I stand on the shoulders of giants. These are advancements that make my job much easier right now. I think before that Jorge had a big project to complete our libbitcoinconsensus into something that is more whole and encapsulates the consensus engine. Perhaps a good piece of context to give right now is that we do have a libbitcoinconsensus right now. It only does script verification, it doesn’t do anything else. It doesn’t connect blocks, it doesn’t do anything else. It is not a full consensus engine. Again to me these are lofty goals that are pretty far away. I want to look at what are some concrete steps where we can move towards a world where it is possible to do something like that to complete a library. What are some concrete steps that would benefit our codebase right now that move towards that. I think it is foolish to try to think about what would a perfect libbitcoinconsensus look like? Or what would perfect organization look like? I think it is good to take concrete steps that benefit us and then take a look from there. Once we get there we might have very different understandings of how the codebase should work. Maybe we discover new things and we take it a step at a time and learn and talk and discuss.

AJ: Wouldn’t multiple implementations come in handy for this? We have to copy the bugs as they are part of consensus. Wouldn’t that be handy right now to have other people who are thinking about this and trying to isolate what consensus is?

CD: One of the understandings of an [ABI](https://en.wikipedia.org/wiki/Application_binary_interface) is the bug interface. Bitcoin is unique in that it is a consensus system. You almost want to replicate the bugs. It sounds very weird to say. That’s basically what it is.

AJ: Not want to, you have to.

CD: Exactly. You have to replicate the bugs. This is very far off but if someday, maybe in the next ten years, we get to a place where we have a library that other applications can pull in and get a consensus engine that matches exactly with Bitcoin Core’s, then they can implement alternative implementations of Bitcoin without fear of being out of sync with the main chain. They can implement alternative implementations with different policies, mempool policies, different priorities.

M: One of the things that were introduced by previous alternative implementations was that you could serve unconfirmed transactions or serve parts of the UTXO set. Or think about block explorers. Bitcoin Core does not have a full transaction index by default. You can start it with `txindex` but then you still don’t have address balances for example.

CD: Exactly. This touches on one of the things that I felt was very compelling to me when I thought more about why I want to do this. It is a technical solution to a somewhat social problem. It can’t be that people try to cram all of the features that they want into Bitcoin Core. That is unmaintainable and not what we want. We don’t want a hundred different indexes to serve every single need. But if people have drastically different ways that they want to implement their node, having a library is so much more useful than telling them to fork the codebase. Forking the codebase means a major rebase every few years, that is not a practical thing to do.

M: And you inherit all the design decisions. You have to move away from that. Bitcoin Core’s codebase is rather quirky.

CD: For sure.

AJ: Another lesson of why not to put a proof of concept into production.

M: It kind of works.

AJ: It does. Any parting shots? Any other things to talk about in terms of the modularizing?

CD: I would encourage anyone listening to this to review the code. I have made it so that every commit is somewhat trivial to review. The more involved ones have very long commit messages to describe why it is the way it is.

M: Does a full node need to have a wallet?

CD: Maybe not.

AJ: It certainly doesn’t need a GUI. Thank you for joining us. We have been trying for months to get you on. Appreciate the conversation.
