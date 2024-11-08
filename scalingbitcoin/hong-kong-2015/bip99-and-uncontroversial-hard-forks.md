---
title: Bip99 And Uncontroversial Hard Forks
transcript_by: Bryan Bishop
tags:
  - soft-fork-activation
speakers:
  - Jorge Timón
media: https://youtube.com/watch?v=aQ1--w4uEMM&t=1121
---
slides: <https://scalingbitcoin.org/hongkong2015/presentations/DAY1/1_overview_1_timon.pdf>

bip99 <https://github.com/bitcoin/bips/blob/master/bip-0099.mediawiki>

We are going to focus on consensus rules. I am going to give an introduction and then focus on controversial versus non-controversial hard-forks.

Why do we want to classify consensus changes in the first place? Well, for one, you often have long discussions many times in Bitcoin, we don't always share the same terminology and the same definitions, and this could lead to disagreement. Another advantage of classifying consensus forks is to recommend strategies for them. One of the objectives of bip99 is to make a suggestion for non-controversial hard-fork deployment.

The first classification that is more commonly used for consensus forks is soft-forks versus hard-forks. Soft-forks limit the rules for things that are invalid are still invalid, but some things that were previously valid now become invalid. This is what we have been doing so far for many consensus changes. They have the advantage that they are backwards-compatible, you don't have to adapt your code. You can still be part of the network.

Soft-forks have some limitations as well, which is why I want to deploy hard-forks as well.

Another category of consensus forks is unintentional hard-forks. Accidents happen. There are mistakes in implementations, not everyone always implements the exact consensus rules. Accidents like this have happened in the past. Does it matter if they are soft-forks or hard-forks? I don't think so, we just don't want to do this. The deployment combination is trying to not deploy this. It's simple. But what are this specification of consensus rules that people are not able to follow?

There's some documentation that claims to be consensus rules, but it's usually outdated and doesn't go into enough detail. One project that several people are working on is decoupling the consensus rules from Bitcoin Core, from the rest of Bitcoin Core. The project is big, and the consensus rules are really only a tiny part of that. So far we have exposed verifyscript, which is kind of low-level, but it's pretty good, because you have most of the crypto and the difficult stuff. I would like to expose VerifyTransaction and VerifyBlock and hopefully move this into its own repository apart from Bitcoin Core.

When we have that, we will have a formal specification and the implementation. Other implementations separate from Bitcoin Core will evolve form that. We don't have libconsensus yet.

Non-controversial soft-forks are what we have been doing so far. It's been very successful. It's backwards-compatible because if you don't upgrade to the new rules, it's fine. As long as miners have upgraded, of course. Blocks that would be valid with the new rules will validate just fine.

Here are a list of deployments that we have done, like bip65 in progress. I think it's very advanced, I don't know the percentage of miners that are upgraded, but it's high I think. The way we deploy this at first, we used the time threshold. And then we started to use this block supermajority which allowed miners to use the block version to coordinate the deployment. People sometimes cause this "miner voting", but I don't like calling it "miner voting" because it's not something that is being voted, these changes were supposed to be completely non-controversial and we expect all miners to use, so they're not really voting on anything.

bip9... Super-majority has problem with parallel deployment. bip9 tries to change this. Instead of using the version field as an integer, we just use the bits individually. Only 29 bits, because 3 of them have been lost. One due to the fact that the- signed versus unsigned number, and two more because we used version 4 last month. But I think 29 is good. I don't think we'll ever deploy 29 different consensus forks at the same time.

Uncontroversial hard-fork is something we have never done. I would like us to do this sometime. There are many things we could do, but these are some of the least controversial ideas for an uncontroversial hard-fork, and they are easy to implement and are good candidates.

In the scripting language, there are operators that don't do anything but return true. We could use them to deploy soft-forks and there's limited space, and we could have made bigger from the beginning but we didn't, we could fix that with a non-controversial hard-fork.

If people want hard-forks to be deployed slowly for all of the implementations to have time to adapt their software, we want to have a hard-fork as soon as possible. 5-years is probably too much time.

For the temporal threshold, we could use the time in the header, but I don't like that much, because you don't know for a given block if the next block is going to be using the new rules or not. With a blockheight you could know that, and that's the option I like more. But people don't like that because you're unable to plan very accurately, you can say 1 year from now, but it's not going to be 1 year, it's going to be 1 year in terms of chain time (block height). So people prefer to use the median time instead, and I think it's fine.

So that's what bip99 is going to recommend, evne though I prefer the height.

A controversial soft-fork is where miners decide to collude between themselves, perhaps not doing any coordination- well, coordination yes but perhaps not through the chain. They could censor types of transactions, maybe they just don't like the soft-fork, and the censor all votes or something. The deployment recommendation is for miners to please not do this.

There are controversial hard-fork proposals. We will see some examples if I have time. The point here is that we don't care about miners here because if we have something controversial, some miners might be opposed, then we don't want use any miner upgrade confirmation mechanism because we can just use a time threshold and that's it.

A schism hard-fork is like going to war, and we don't want to kill civilians or anything, we don't want to hurt bystanders that don't know what's going on. A way to do that is to start the controversial hard-fork is by.....

(inaudible / stream problems)

... are not going to agree with fixing it. That's another example. Another example would be ... like there's some altcoins that their initial distribution starts, all altcoins could have been launched like this, for example freicoin could have been launched at... and not much would have changed. We don't have many users, that's true, most bitcoiners ignore us, that's fine, but I think that if had been a controverisal hard-fork instead, then the result would have been practically the same, we would have been able to change some things, but bitcoin users could use the new features in freicoin.

...

And yeah people can disagree for unbounded amounts of time, and some people deny that, but that's fine because that's an example of something that would be open disagreement. People don't have to follow the majority, whatever you mean by majority, if it's miners, we can fork miners out. You can measure economic majority whatever it means, but I would use the freicoin as an example again. Frei-fork chain would be used if it was a controversial hard-fork, and bitcoiners would not have moved to freicoin, some users like me would be using both chains, there's no reason why there always has to be a unification there.

Specially if it's not very clear if there is a difference in fundamental values, even if this wasn't true then it's not very important. If you have questions, we'll take questions.

Q: ...

A: ... You cannot predict demand for the two chains, but one way they could be unified is by one of the sides going to zero in the market or exchange rate.

Q: Do you think it's worth differnetiating between hard-forks that are undetectable to SPV clients versus others?

A: With controversial hard-forks, we recommend in bip99 to make this visible to SPV clients.
