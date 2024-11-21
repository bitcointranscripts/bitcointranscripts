---
title: Multiparty Channels (Lightning Network)
transcript_by: Lucas de C. Ferreira, Ben Knáb
tags:
  - lightning
  - multiparty channel
  - channel-factories
speakers:
  - Christian Decker
date: 2019-06-28
media: https://youtu.be/PUDWGH_MvmQ
aliases:
  - /chaincode-labs/chaincode-residency/2019-06-28-christian-decker-multiparty-channels/
---
Location: Chaincode Labs Lightning Residency 2019

Slides: <https://residency.chaincode.com/presentations/lightning/Multiparty_Channels.pdf>

# Symmetric Update Protocols

## eltoo Update Mechanism

Two days ago, we’ve seen the symmetric update mechanism called eltoo, and having a symmetric update mechanism has some really nice properties that enable some really cool stuff. Just to remind everybody, this is what eltoo looks like. That’s the one you've already seen. It’s not the only symmetric update mechanism, though.

## Duplex Micropayment Channels

It was predated by this stuff. Has anybody seen this before? This was basically my first attempt at creating a duplex micropayment channel or a micropayment channel that couldn't go both ways... Basically, what we did was have timelocks and have them decrease over time. So this all is timelock 100, and the first update has timelock 99, 100, 100, and so on. And every time you do a replacement, you basically count down on one of these levels and then basically just make sure that this is confirmable slightly before the other stuff is confirmable.

Back then, I didn't realize this but what we did was basically have this invalidation tree which is used to sort of count down time, but what you have here is basically simple micropayment channels. These are unidirectional payment channels and what you do is you have the structure of an update mechanism and then something built on top of it, right? Because if you have an update mechanism, the only thing that you’re basically doing is having some way of creating a transaction. Eventually, that might create some outputs. That's all we basically try to do; in Lightning, it happens to be the balances of the two parties and HTLCs, but really there is not much of a difference to have any construction of transactions on top of these outputs that you're guaranteed will eventually be created or will not be created in the case you remove them later on.  So we can actually have these kinds of settlement transactions take off other stuff.

# Ok, but why?

## Multiparty channels

But why do we care about this? For starters, you can do stuff like multiparty channels. Multiparty channels are basically a bunch of people gather, put some money on the table, and then decide how to split it again. The initial setup is basically everybody puts in five bitcoins, and we are guaranteed that we will get 5 bitcoins out at the end, but since we now have this construction here, we can actually iteratively send back and forth money and basically replace this state with any other state we want. And the advantage here is that we didn't have to create multi-hop payments to make channel adjustments inside of our group, so we actually have a setup as if we had a complete graph between us, in terms of Lightning channels, each with the full capacity. So you increase liquidity, you increase flexibility of the funds that you're using and have a lot of freedom, and you could then also start building channels on top of this stuff.

## Channel Factories

That's basically the idea of channel factories. It's basically you have the setup transaction, and you have the settlement transaction, that in turn then splits funds into smaller groups and you can then have channels built on top of this bigger group, you can split them and really have just the yellow and the pink one talk to each other while we still have commit control over the entirety of your funds.

We have this thing here where we can freely send back and forth money between any two endpoints. Why would we then start to do stuff like this where we create channels where we split out funds and create subcontracts, basically, in our bigger contract? Anybody?

Audience: You don't need to get everybody to sign the same transaction.

Christian: Exactly. So the issue here is that in order to move these funds or to update this contract here, you basically need everybody to sign off. Everybody needs to be aware of what happens in those, and if you want to have a private session with somebody else, then you might say:

Okay, we now talk only about these four bitcoins, and then we go off and do our discussions between ourselves, and then when we come back, we only settle the aggregate of what we do.

It also means that if the yellow participant goes away, then this channel still remains active because, on this one, we don't need signatures from the yellow participant. So we can basically drop this contract onto the blockchain. This state here, this one will eventually be resolved, this one will eventually be resolved, but we can continue negotiating on this sub-contract.

Audience: If I’m the yellow participant and my parents just dry up and have no more funds into it, I think I have an incentive to not resign the new revocation.

Christian: Sure. So that's definitely something that might not be too nice. You have sort of silent bystanders that do not have a stake in your contract, and they might be malicious and not contribute anymore. At this point, you might actually just create an update that ratchets this forward and drops the yellow participant. Then you can confirm that on the blockchain but at the same time still be operational and still do stuff in there.

Audience: (inaudible)

Christian: Yeah, exactly, but sometimes silent bystanders are exactly what we want. We want people that do not have a stake themselves but are aware of what happens in the contract.

So think, for example, of an audit: If you have an auditor in your contract that can see what happens and can sign off on changes, he doesn't have to have a stake himself to be able to track what happens inside of this contract. So sometimes, having somebody without stake is sort of the desired state.

So we've just discussed how to drop a person from an existing contract. Is there a way to onboard people into one of these? So if I were, for example, a green participant, could I join this contract?

Audience: Even if you use something like eltoo, you (inaudible) write a new revocation.

Christian: Dropping people is sort of doable, but you have this additional intermediate hop where you drop this and make this a 2-of-2 instead of a 2-of-3, but onboarding is really hard if the onboardee does not trust the group that is already in there or if he doesn't trust at least one of the people that are in the group and I could basically make a copy of this and onboard Antoine, and I could have another copy where he isn't and the third copy where Jonas is in and then we suddenly are double-spending stuff right because I could send to Antoine and I could send to Jonas it gets really weird. If that's something that you're interested in there is there are proposals for what's called state chains, but they tend to be a bit more reliant on a third party to actually give these assurances where you have somebody basically vouching that this has only been signed once and this is the state that you will actually have right now.

Audience: Something like (inaudible) some code and magic.

Christian: Well, that’s all on-chain, right? As long as we’re off-chain…

Audience: Yeah, but if we can predict the new state, if you can force all the parties to include the same next state, I mean they don’t have an incentive to broadcast this on-chain if you’re sure that’s...

Christian: I mean, this is just three of us, and then we can do whatever we want as indirection so that you can’t...

Audience: No, I’m the green participant, and you give me a new revocation, and maybe you can trick the first revocation to do a covenant on the second one to force it to (inaudible)

Christian: That would already mean that I was aware that you might join, so why did we include you initially?

Audience: (inaudible) some blank key, and you can replace (inaudible)

Christian: Yeah, it gets really hard. Either you have a provision in there to eventually onboard somebody that you already know might join, or it's really weird of a situation so that in our case, we revert back to having this trust.

Audience: Then you have the double-spend problem.

Christian: Right, it's the off-chain version of the double-spending problem exactly. So this kind of dynamic membership would be really nice because we could basically have somebody enter the room, and they would be able to interact with us, and we wouldn't have capacity issues, we wouldn't have multi-hop health issues, we wouldn't have CLTVs. It would all get so much easier, but we just don't know how to do that yet. So maybe one of you guys will come up with something, hopefully.

Audience: This doesn’t work with LN-Penalty, right?

Christian: It's really hard for LN-penalty because to revoke this stuff, you exchange loads of revocation secrets, and you always have the situation where the last person that is giving out the revocation secret might basically do some really nasty stuff. LN-penalty, in this case, makes it hard because you always need to know who to punish in case something ends up on the blockchain.

Audience: You end up with multiple (inaudible) with three parties. You end up with three different variations of the same transaction. Actually, multiple of that, because (inaudible) You need to have copies (inaudible)

Christian: Basically, it gets to state explosion and that's exactly because of this symmetry because we have this symmetric state. Symmetric state makes it so much easier because you just have this; okay, this is the last transaction, I don't care about anything else.
