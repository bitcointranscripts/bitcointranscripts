---
title: History of the Lightning Network
transcript_by: Caralie Chrisco
tags:
  - lightning
speakers:
  - Christian Decker
date: 2018-10-22
media: https://youtu.be/HauP9F16mUM
aliases:
  - /chaincode-labs/chaincode-residency/2018-10-22-christian-decker-history-of-lightning/
---
Location: Chaincode Labs Lightning Residency 2018

## Introduction

Hi I'm Chris, as I said like three times before, and I'll be talking about the history of Lightning and history of off-chain protocols or layer two, or you name it, whatever name you want. I like to call them off chain because it doesn't imply a hierarchy of layers but I'll use all three terms interchangeably anyway.

I like to have an interactive presentation so if you have any questions please don't hesitate, just ask. I don't care if we can't make it through the entire slide set I have. For me it's important to actually give you a better understanding of what happens and if we don't get to the later slides that's totally fine as well.

## What are off-chain protocols?

Before we can talk about the history of Lightning and off-chain protocols, we probably need to first see what all the deal is about in the first place. What are off-chain protocols?

Off-chain protocols are usually systems in which you have a couple of users using data on a blockchain and managing it without touching the blockchain itself until the very last minute. So what we do is we have this sort of example of data that is on a blockchain. We have Alice, Bob, and Carol each have five bitcoins on their account and now Alice and Bob want to open an off-chain contract, a payment channel. And what they do is basically they lock some of the state of the blockchain, so that they cannot modify that state unilaterally anymore. Then they go into separate rooms basically and start discussing how they split or how to settle this state in the end. So the initial state which we represent with this scroll here, it's basically the same as we had on chain right? Alice has five bitcoins and Bob has five bitcoins. Now we can start interacting. We can, for example transfer one bitcoin from Alice to Bob, changing the balances and we have this transaction which basically represents the final state of this transfer. Then we can go ahead and transfer some more from Alice to Bob and we can even transfer some back and eventually we're happy with what happened. One of us wants to leave one of us has disappeared, but we want to reflect these changes that we discussed off-chain back onto the blockchain.

What we do is basically we send the state back to the blockchain. The blockchain sees the desired state, removes the old state, and applies the new state to it. What's important here is that these intermediate states are always aggregates of multiple individual states. So as we've seen before when transferring one bitcoin from Alice to Bob, the final state was four and six and then we transferred three more, and the final state was one and nine. This association between the individual transfers gets lost when reapplying it to the blockchain. It's also important to see that in order for this contract to be on the right, to be all to be able to be reflected on the Bitcoin blockchain, we need to have this in the form of a transaction because that's the only operation the Bitcoin blockchain will understand and will let you let you execute.

So this is a very simple concept and what we actually need for it to work is we need some way of updating this state. Basically making sure that we agree on what the current state is and what it would look like if we were to go on chain. The one really important issue with this is that, if I'm Alice I like the state because I have six bitcoins whereas initially I had like five, right? If I’m Bob I like this state much more. In this state, I have nine and Alice has one. We need some way of making sure that the older states are not applicable to the blockchain anymore and that's what I usually call an update mechanism. And that's the core issue that we've tried to solve in all of these off-chain protocols. How do we renegotiate something off the blockchain and make sure that only the latest agreed-upon state is actually enforceable on the blockchain and you can't cheat and go back? There's a little bit more supporting infrastructure for off-chain protocols, but this is really the core issue.

## Update Mechanisms

I'll be mostly talking about update mechanisms and see how they evolve over time. So update mechanisms, does anybody have a guess what the first update mechanism is going to be that I'm presenting? What could be the first one?

Audience Member speaks

Christian: You actually got it right. So the first ever replacement or update mechanism that was in Bitcoin was already in the source code released by Satoshi himself, the Sequence numbers. This is actually not Satoshi’s code. This is as far back on github as I could go. This is from series M, a commit in August 2009, but it's I think it's the same. I couldn't go back any further.

The idea with the sequence numbers is basically we create a transaction, we send it out there and then we create a new transaction that replaces this transaction. We hope that miners will replace it, but the issue of course, is miners do not have any incentive and if I'm cheating I could even go to the miners and say, “hey if you confirm this transaction I'll give you a cut of 25% or so.” You can actually incentivize miners to behave against this protocol and even worse is that you can't even prove that a miner misbehaved because he could just say, “no I didn't see any updates before I mined my block.” Because if you could, you could actually hold the miners hostage.

Anyway, nSequence numbers are cute. They don't work and it's the reason why we’ve repurposed this field a number of times in the meantime for other purposes, which actually makes the semantics of the nSequence field really hard to grasp.

## Simple Micropayment Channel

So the first actually working payment channel implementation or off-chain protocol is what's called a simple micropayment channel by Spilman et al. 2013.

I'm not sure about that date this idea has been floating around Bitcoin Talk forever before and I think Spilman was the first one to actually put it in words that made sense. That's always the issue with the Bitcoin space in the lighting space somebody has always proposed it before you. You're never going to be the first one and then you publish a paper and everybody says “yeah, that's this old idea from 2011.”

So the simple micropayment channel is, uh, simple. It basically starts off with a green user and the blue user. The green user puts up five bitcoins and transfers them into a shared output owned by both the green user and the blue user. The color of the dot actually represents who has control over it. So in this case we need signatures from both the green user and the blue user to actually spend this funds. What this does, is basically it prevents me, if I'm the green user from pulling out the funds below the contract without giving the other side the control. It's basically just me putting up ten bucks on the counter and as long as these ten bucks are on the counter, both me and the barman, we have control over it and I can't pull them away and try to sneak them away.

Now we need some form of state representation and that's, as I said, is going to be a transaction. We have a set up transaction which creates this channel and we have a settlement transaction that represents the cumulative state of all our intermediate transfers. In this case I just get my five bitcoins back and the other party gets nothing.  At this point, I sign it. Well, I'll drop those dots in the future because this is the only part where the signatures are important. So the green party signs it and gives this half signed transaction over to the blue party. The blue party now has two options. This transaction is incomplete. They could add their own signature, completing this transaction and publishing it into the Bitcoin network or they can put it into their back pocket and say, “yeah I don't know. He set up a channel so maybe he wants to pay me.” Blue user just keeps it in his back pocket and now we actually go and confirm this first transaction. I'll always use the lock to represent stuff that is on chain and the box without lock in there to represent floating transactions, or a transaction that we haven't confirmed just yet.

Now we've set up the channel. We can actually go ahead and transfer some. In this case, the green user transferred one Bitcoin to the blue user, creating a new settlement transaction, again signing it. I can't do anything with it because the blue signature is missing, but I'm handing it over to the blue user. The blue user again has the option, “Okay, do I sign it or maybe there's more coming?” In most cases they will actually hold onto it and say, “Yeah, maybe something else is coming up.”

Indeed, we do this a few more times and eventually we have this final state. The blue user now sees, “Okay I need this money. I have to get it now or the green user disappeared and yeah I don't want to wait for him to come back.” So what the blue user does is it takes the transaction that gave him the most funds, adds the signature to it and broadcasts it in the Bitcoin network.
Eventually this is going to be confirmed.

This is a very simple payment channel that has been implemented a number of times. We have actually built some prototypes of access points being paid using these, coke machines that would dispense using these micropayment channels and so on and so forth.

Yep?

Audience Member Speaks

Christian: So you mean the blue party disappearing or the green party disappearing?

Audience Member Speaks

Christian: Yes. That's a very good point. What happens if people disappear? The easy case is when green disappears, blue can just take one of these transactions, sign it and send it off. If in the initial state or any state in between the blue party disappears then we have a problem, right? Because the green party does not have any way of recovering those funds. For this case we create an additional transaction that is time locked, that would refund basically the entire deal of the funds to the green user, basically forcing the blue party to either close or stay active.

Audience Member Speaks

Christian: Yes. The reason I left it out is because it adds more complexity and it's really ugly. It also gives your channels a fixed lifetime, which is, as soon as you denominate some limit of how long this can stay active, it sort of gets ugly. But we had this refund transaction that would actually work.

Audience Member speaks

Christian: Yes, so the refund transaction had this reliance on a malleability fix because it would need to be created before this one could be confirmed. So you have a transaction that was unconfirmed and you had a refund transaction that was also unconfirmed and the refund transaction was referencing the unconfirmed transaction here. This one could be malleated and thus detaching this refund’s transaction. That's an ugly thing indeed, yes. You could work around it with OP_CSV (OP_CHECKSEQUENCEVERIFY) and stuff, but...

Audience Member speaks

All of the malleability fixes are always pertaining to, “I have some transaction that is not confirmed. It can still change and I want to build onto bolt-on transactions onto that one. That's indeed the core problem we have with malleability when it comes to off-chain protocols.

Simple is good, but is it good enough? Anybody see a problem with this? Well, I know you already saw part of this …

Audience Member speaks

Yes. The issue really is that these are unilateral channels. If you're the green party, you can only ever send and the blue party can only ever receive. Why is that? Because the blue party will always be incentivized to use the latest state that gave them the most funds and so we can create a settlement transaction that transfers some funds back to green, but why would blue ever use that one, because it gives him less funds in the system? I used to call this replacement by incentive because blue is always incentivized to use the latest state. If he misbehaved he would basically give back more money than he should have, but I mean he's at fault so that's ok.

This is a simple mechanism. It worked for some things, but one major drawback is that all these funds can only ever be used once. It's basically like a debit card where I charge at the beginning of the month and then I can just spend it and once I've reached my limit, well then I can throw away the card. There's no reuse of funds multiple times.

## Duplex Micropayment Channel

What we came up with in 2015 is what's called a duplex micropayment channel and that's really a system which allows you to transfer back and forth multiple times.

Audience Member speaks

Christian: I think it was around Christmas that I had the core idea, 2014 and then we wrote the paper, which is always a long process and then we submitted it. It was under review for four months, meanwhile the Lightning Labs guys published their paper. I had a really exciting long weekend trying to understand what they do because the Lightning paper is really hard to grok and in the end it had so much overlap that I decided, yeah let's forget about duplex micropayment channels. We'll just jump on the big bandwagon. The reason I'm showing it here is basically that it's also rather simple, even if limited and it gets us closer to what Lightning actually is.

What we have here is, we have again the set up transaction being confirmed on the blockchain and then we have a representation of our state that spends this funding output and basically represents the aggregate of all interactions we had in between. If you're wondering what this T=100 means, that's a timelock, a simplified timelock. This basically means that this transaction will only be valid at day 100. We set up this transaction, let's say at day zero and then we have to wait 100 days for this transaction to be valid and then we can settle. So how do we do replacements? Well, we create a new settlement transaction that is valid slightly before that one. That means that in the time between day 99 and day 100 only this new transaction is valid. If we can make sure that during this one-day period we can actually have this transaction confirmed on chain, then the old state with T=100 is technically replaced. We can do that a number of times and as you can see it basically counts down towards today. This is sort of uglyish, but also ugly in the sense that now I have to wait like 96 days to get my funds back. That's really bad.

The solution here is to differentiate between a collaborative close and a unilateral close. In the unilateral close both parties have a copy of this transaction. The other guy goes away. So now I have to wait like 96 days for it to confirm, but I will get my funds back. In the collaborative close we actually have this system where you and I agree that we want to close this channel, that this is the final state, so let's just sign a copy without a time lock and be happy. If we do a collaborative close we can create this transaction, which is valid immediately and we can settle the channel without having to wait at all and everybody is happy.

One of the important parts here is that unlike in the simple micropayment channels, here the state is symmetric. Here I don't have, this guy signs first and this guy signs later. I hold a half complete transaction. You hold a full complete transaction. In this case we're always dealing with fully complete transactions, fully signed transactions and this will be important again with Lightning. We can have this collaborative close and just settle up.

## Lightning Penalty

Now for the one that everybody has been waiting for, the Lightning penalty mechanism as I like to call it. Lightning penalty is asymmetric again, which is why I emphasized that before. So we have some data that only the blue participant knows some data that only the green participant knows and the security of this protocol relies on the green participant not learning anything from the blue party and the blue party and the blue participant never learning anything of the green party. So if you ever try to do a backup on Lightning that's why. What we do is basically, instead of creating one settlement transaction we create two identical ones with one little difference in here, namely, that this output that goes to the blue participant and is known to the blue is encumbered with a bit of a poison and I'll show you how to use that in a second.

We have these initial states four and one, four and one... Now we want to create a new update: three and two, three and two and we've run into the usual problem
right? How can we ensure that this is the only version of the off-chain contract that will be enforced and this one can't?

As I mentioned before, the outputs that are known by the blue participant and go to the blue participant or the green participant and go to the green participant are encumbered a little bit. And the way we use that is when the blue participant wants to convince a green participant that, “No, I'm not going to use this transaction.” What they do is basically they hand a transaction that steals their funds. They hand that transaction to the green participant, basically saying, “Hey if I ever publish this transaction feel free to steal my funds.” The same goes for the other side, in this case, the green participant could use this transaction to get four bitcoins here. So it creates a punishment transaction that takes these funds and rewires them to go to the blue participant and then he sends this transaction over to the green participant basically saying, “Hey if I ever misbehave, if I ever try to confirm this transaction, which I promised you that I wouldn't, feel free to punish me.” We can do that several times. In this case we've just updated to four and one and again we poison the old transactions in such a way that if they ever leak on chain then we're going to die.

The nice part about this is, this can go on indefinitely. That's a huge advantage compared to duplex micropayment channels. Duplex micropayment channels have a limited time life. The reason for this is because we were counting down time locks towards today and when we've reached today, there is nothing we can do. We've had a bit of a workaround there with the invalidation tree and because that's the go-to place for computer scientists who find their solution. If doesn't work, let just use a tree. Yeah it wasn't that nice. Okay, but this is basically Lightning penalty. This is the most complex update mechanism I have to present here today, so are there any questions? Is everyone a Lightning expert and I'm wasting my breath?

Audience Member asks a question

Christian: Yes that one.

Audience Member asks a question

Christian: Okay, so one step back. In this case, we are actually punishing the misbehaving party, right? If for example the blue participant publishes this transaction, it's not it's not enforcing the latest state we agreed upon, but it enforces that yes green gets his money back (and some more) and blue gets nothing. This is why I call it LN penalty and why everybody is like, “Yay, cheaters are going to be hit on the head!”

I don't quite like the penalty model because I had some really awkward situations where people were backing up stuff and then restoring nodes. And it's really easy. If you forget any of this happened and you restored this state, then it's not your fault, but you're going to cheat. Even if you re-establish contact with the other party and say, “Hey, by the way I have this state.” The other party can say, “Whoa, that's really old. Yeah, yeah you go publish that. You go ahead and do that.”

So there's this sort of deadlock where I can't do anything and if I do something then I'm going to be punished. That actually happened to me while at coredev in New York I was sitting in the middle of the room and I was like, “Yeah I'll just restore this node quickly. I'm sure I've stopped it before taking the update.” And suddenly in the middle of the room you hear me crying out because I was like, what the fuck happened here? It turns out the node was not shut down and I reconnected and the other side actually said, “Yeah, yeah, you go ahead. Publish that one. You'll be fine.” I wasn't.

Audience Member Speaks

Christian: Yes. Exactly. So the advantage here with eltoo is that it actually can outsource all of this. It's not me, well I'll get to that later when I'm actually talking about this.

What I don't like about the penalty mechanism is that it makes stuff really hard. If you backup stuff, we've had loads of people that were using the Google backup from eclair and we're like, “I can replicate this node multiple times and run it on my phone and my laptop and my tablet” and then they were like, “what just happened?” Because they were using it concurrently and they were backing it up to Google Drive and then restoring it and then...it's just really bad.

Audience Member Speaks

Christian: You have had seven breach closes in your favor?

Audience Member Speaks

Christian: It also makes the whole state machine really complex when you're implementing this. We have this one issue where the other side misbehaved and we stole their funds, but forgot about our own funds. So that's a really fun corner case to try to debug and it took forever to actually find it. The more complex the state machine is, the more bugs you will have basically.

Audience Member Speaks

Christian: Having multiple devices you would probably prefer to open multiple channels that are not shared among devices or you need to remote or having one device be a slave to the other and the other one is actually running the nodes. Yeah, sharing states among multiple nodes is really bad and it makes this really painful.

Audience Member Speaks

Christian: So what you can do, is there's two things and that I'll talk about later. Eltoo actually allows you to have multi-party channels because this asymmetry which you have here is no longer there and there are two proposals one is Perun, which is some Nordic god of lightning and I always pronounce it with a Spanish accent which makes it super weird. That allows you to have virtual channels that map to real channels or you can have channel factories, which are basically bigger groups that then bootstrap channels off of this large group.

Audience Member Speaks

Christian: So I'm aware of a few projects that go into that direction. One of course is Raiden which is the one-to-one clone of Lightning basically. I had fun giving a lecture at Stanford. I had really a lot of fun half an hour before the lecture started recreating the smart contract for Raiden and it's 20 lines. So that's like three and a half million dollars of funding per line. Really good value. There is of course what we call state channels, but...

Audience Member Speaks

Christian: No sprites is a mechanism to ensure the timely settlement of payments. State channels are the ones in ethereum where they basically have arbitrary contracts running over off-chain protocols and then reflecting that state back onto the blockchain itself. And it's really fun because Perun was created for the state channels and they were like, “Yeah no way this is going to work on Bitcoin.” And yes it's working. So treat ethereum like a testnet and back port whatever is useful.

## Eltoo

Let's go onto eltoo. Eltoo is a proposal that we created or published earlier this year and I'd like to think it's easier than Lightning, but we'll see about that. So we have the usual setup thingy and then we have a settlement transaction. This time, I drew it below here and if you can see the small clock basically means that this transaction is time locked.

What we do is basically we create the setup transaction and we immediately create this settlement zero. The settlement zero just gives back the money to the green participant and we encumbered this transaction using a time lock. Basically this settlement will become valid after, let's say after a day. Okay if nothing else happens, green gets his money back and we're done.

Now if you want to do an update, we basically just create what's called an update transaction. Update, one that takes this output and creates a new output that has exactly the same structure and we attach the new settlement one to it, which reflects the new state. So we just transfer one bitcoin from green to blue. We've invalidated this by double spending it. So this is no longer valid because the update basically just spent this one.

That's how updates work in eltoo. We can do that a number of times again so update two activate settlement two, settlement one is discarded and so on and so forth.

Audience Member Speaks

Christian: Yes, so I didn't mention this but you can actually replay the entirety of this protocol on chain which makes it really easy to visualize. We can actually do this interactively on-chain. In here, we have 24 hours to create an update and then the update gives us another 24 hours if we update in time and we get another 24 hours and so on.

Audience Member Speaks

Christian: Yes so we could just refresh the timer by having a dummy update. Anybody see an issue with this? It's a shitload of transactions.

For every state update we actually have one transaction. We could just have done this on chain as well. What we do is now we lift this off the blockchain and say, “Okay, instead of replaying this entire thing on the blockchain we just keep the chain of updates in memory and always only the latest settlement.” Because that basically is the path that we need to take to get to the latest settlement.

Let's say the green user wants to enable this state here right? What he does is he publishes update one. Then he has to wait 24 hours to settle it. The blue participant says, “Wait, you’re trying to cheat me.” So what he does is publish update one, two, and three and then has 24 hours to wait before you can send settlement. What we actually do is we allow you to try to initiate a settlement using an old state but we'll just tag on, right? We'll just continue.

Audience Member Speaks

Christian: The time locks are always there so that the update gets priority over the settlement.

Audience Member Speaks

Christian: The short answer is we'll just use a month or so for this time so. We still have a limited time lifetime for the channel. The more advanced one is that we have a trigger transaction that is placed in between so that we have the funding transaction that creates the shared output, we have a trigger transaction that initiates the time locks and only then we attach settlements. So think of it like the settlement 0 does not exist and update one actually initiates the countdown. We have ways to make this open indefinitely.

Audience Member Speaks

The issue here was that we basically have this problem of if we have N updates we were playing N transactions on chain. What if we could do something like instead of having the update three connect only to update two we could actually go ahead and say, “I connected it to the settlement transaction.” We just skip all of these intermediate updates. We skip to the one that we are interested in and can do our settlement. That's actually what SIGHASH_NO_INPUT allows us to do which is a proposal that we're currently trying to propose, but so far I've not heard too many negative voices about it. There's two complaints, one is it allows for replay attacks, but then again we have SIGHASH_NONE and the other one is it doesn't go far enough we should parameterize everything. To that I just say first we need use cases before we open up more flexibility.

The replay attack basically means… so in this case the replay is wanted. We can have and have funds, so this transaction can spend this output and this output. If they weren't connected among themself then we could basically just replay that transaction and get it multiple times. If you use funds on an address and you want to send them to me and you sign them with SIGHASH_NO_INPUT, then I could take and you have more than those funds lying on that address then I could basically rebind the transaction that you sent to me and grab any of the other outputs. There needs to be some care taken about how much you expose yourself to that and we usually just new key pairs for every single one of these dots. Sighash is a little flag in the signature that tells us what information is part of the signature and what isn't. So SIGHASH_NO_INPUT basically means that we are signing in the transaction that we want to authorize, but we're leaving out some parts so that other people can come, or even I can come, and change that slightly without invalidating the signature. So that's basically this -- in this transaction, there is a small reference in the form of a hash to the previous output that I'm going to spend and instead of taking the small transaction just signing it will just carve out this little space and sign everything around it instead. That keeps some flexibility in there and allows us to rewrite it without invalidating, which has some nice effects.

Audience Member Speaks

Christian: The alternative would be to have this transaction sign it like N times. So that's one thing, but you can't get around having at least one signature for each output that existed at some point in the system. Even if you do a skip list you have to have a path from every single node up to the next level in the skip list and up to the next level and so on. You're not gaining that much. You can move signatures from having to be transferred to, “okay yeah we structure it as a skip list,” but you'll still have to remember N signatures in total.

Audience Member Speaks

Christian: No, I mean if you what you can do is basically have this update and sign it N times bound to every single one of them and I'll give you this bunch of signatures and then we don't have to have an unchanged footprint innocent that is any bigger than SIGHASH_NO_INPUT, but you have huge messages. Yes, the skip list is a trade off where you have smaller messages, but also have a bigger on-chain footprint.

Audience Member Speaks

Christian: If you cheat, we can make you pay the fee and not give it back to you, but it's always hard to sort of punish one party in the case of misbehavior because misbehavior is not observable on-chain. Misbehavior is only observable by other parties that know about the state of the channel. We can't really build a punishment into the state transaction without having interaction with the other party and I think I'm running short on time.

I had a few more slides, but as I mentioned great interactions. It's basically layers all the way down. We have discussed the update mechanism, but there are many many more facets in there. What we've just talked about are these two boxes her. The Lightning Network is a lot more than we have. We have a transfer layer that allows us to have multi-hop and the secure end-to-end payments basically either my payment arrives or doesn't. We have the Sphinx layer, which obfuscates which path we're taking through the network. We have a gossip layer that basically exchanges information, how can I go from point A to point B in the network. There's a whole lot of transport layer encryption and feature negotiation and so on and so forth. I have channel factories, cool topic. Perun we've talked about this before, it's one of the things that I'd like to backport from the ethereum folks because it's rather nice and that's it.

I'm out of time but I'm around the whole week so if you have any questions...

Audience Member Speaks

Christian: You can express time locks both as a timestamp or as a block height and in block height, obviously the granularity is like ten minutes or whatever your block interval is. And the timestamp based ones, I have absolutely no idea why they are in there. I guess it's median time passed the block size is what they're referencing? But I always use block based time locks because they're easier to reason about and they're actually absolute numbers that do not have this issue of is this is now 10:00 p.m. or is it one second to 10:00 p.m.?

I guess the upper bound of this is like five million blocks, so you have quite some time to settle your channels.

Audience Member Speaks

Christian: Yes. What I wanted to show in this slide is basically that the LN penalty and eltoo are basically drop-in replacements. The entire rest of the stock remains the same. All we do is basically we change the way we negotiate new states and HTLCs are just part of the state that is attached to a settlement transaction.

Audience Member Speaks

Christian: It's way less painful because you don't have penalty, backups are possible because even if you publish an old state well the other guy will just give it get your newer state. You won't lose everything. The state management is much easier because we now have symmetric state. There is no way if I leaked this information and you can try to kick me in the butt like that. And you keep far fewer states because there is no way for the replaced information to ever leak on-chain.

Whereas with LN penalty, you still have to keep all these secrets from removed HTLCs  because HTLCs might actually leak on chain. This is no longer possible with eltoo. It's much easier from a state management point of view.

Audience Member Speaks

Christian: Any disadvantage? I think depending on how we implemented we might have a footprint that is slightly bigger, so one more transaction. Instead of having like two transactions we have three. In the case of SIGHASH_NO_INPUT not making it. We will have a really hard time actually trying to implement it. So this is one of the cases where I sort of break my promise about layer two and off chain protocols being really nice because they allow you to experiment freely. Not really because we actually need to change the base layer as well. That's sad, I would have liked to go to get it working without, but I haven't figured out how to yet.

Thank you so much and I'll be around.
