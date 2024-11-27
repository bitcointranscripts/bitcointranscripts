---
title: Splicing, Lightning's Multiparty Future
transcript_by: ladyanarki via review.btctranscripts.com
media: https://www.youtube.com/watch?v=SOKNRHyGRvQ
tags:
  - splicing
speakers:
  - Dusty Dettmer
date: 2023-03-14
---
## Introduction

Thanks for coming.
It's exciting to be in Mexico City, talking about Lightning, splicing, and privacy.
I'm Dusty.
This is a photo of me when I was much younger—a little bit younger, but that number is growing every year, it turns out.
So, a little bit about me: I've been doing Bitcoin development stuff for probably five years, and about a year or change ago, I decided to focus on doing lightning stuff, and my first big project has been splicing.
Okay, so who here is technical?
Raise your hand—technical experience.
Okay, who runs a lightning node?
Okay, like half.
Cool, who runs a lightning node with more than one channel on it?
Okay, same.

So I'm gonna go over some of the basics of lightning, which, if you might already know this or you watched my talk, I covered this before, but we're gonna go over it briefly just for people that don't know, and then we're gonna get into some of the more detailed stuff relating to privacy.

## Basics of Lightning

If you imagine here, we have a mock Lightning network.
Each of these little, well-drawn boxes are the Lightning nodes, and they have channels between them.
When you want to make a payment through Lightning, you have to route it across these channels to get it to where you want to go.
As you can see, this little Bitcoin is moving to where it's trying to go.
So when we talk about working on Lightning, all of the development work is on an individual channel.
That's what we focus on, but the end result creates this mesh.
We're gonna dive into just what a channel is for a second.
An important thing you might not know about a channel is that it has an actual size.
So you open a channel, and it's set to a certain size.
That size could be big or it could be small.
And whether that size matters is if you're trying to route a larger payment that's bigger than the size of the channel; it won't be able to go through.
So if you want to make a larger payment, you're gonna need a bigger channel.
The problem there is that lighting channels can't be pre-sized, so the size of the set's done forever, so you can't push things through until now with splicing.
Much to the happiness of many node operators.

## Splicing

Okay, so what does splicing give us?
The main thing, and the most obvious one, is increasing channel sizes.
Here's a great image of that.
Here it's bigger; another payment can go through.
But what's become more apparent over time is that splicing gives us all these ancillary benefits that weren't exactly obvious at first.
One of them feels like a left turn, perhaps, but it's actually building a universal wallet.
Today, if you're using a Bitcoin wallet that's self-custody on your phone, you typically have two balances.
You're gonna have your Lightning balance, and then you're gonna have your on-chain balance.
And this is a UX challenge for on-boarding new users to manage what those words mean.
If you're new to Bitcoin, you get a phone app, and you have to learn what those things are.
That's a challenge.
With splicing, it enables us to build wallets where all of the balance is on Lightning, and we can use what's called a splice-out to make on-chain payments.
This should clean up a lot of user experience of users.
More on that.
The idea of using a splice to make an on-chain payment is you're going to splice-out and decrease the size of that Lightning channel by whatever the payment amount you want to do.
You can see here I have my on-chain or bust arrow, and if we move the Bitcoin out, we'll see the Lightning channel gets smaller by the amount of the size of payment.
In this way, you can now make on-chain payments from your Lightning balance, which I think is pretty awesome.
The other great use case for it is channel cross-sizing.
So if you're running a lightning routing node, you're often in the scenario where you have one very valuable channel that gets lots of routing going through it, and then a bunch of partially dead channels that aren't getting much traffic at all.
With splicing, you can move funds from one of the dead channels over to the better channel, making it bigger.
That takes your debt liquidity and makes it useful somewhere.
You can do this all without ever taking any of the channels down, so they're out for the entire time.
No channel downtime—that's a key point—no channel downtime.
The other point, which we're gonna cover a lot more later, is you can do these in a way that's a lot like a coinjoin.
So, these splices get mixed with other details and merge into a single transaction.
In this instance, we have three different splices you're trying to do between different channels.
You can merge them into a single Bitcoin transaction, which has a lot of benefits, like both transaction size and potentially some privacy benefits as well.
Some other examples of things you can do are: if you have one big Lightning channel, you could take the funds out of there, move them into three different Lightning channels, all with one transaction using splicing.
You could also take a fourth thing and move some funds on-chain at the same time.
So you could do all of these things in a single transaction, which is sort of the main guide for these cases of splicing.
Now, just going through some examples, you can take your on-chain balance and splice it into three channels at the same time.
You can do that and also make an on-chain payment at the same time.
You can go from two lighting channels to three and throw in an on-chain destination.
The point is, you can do a lot of things.
There's almost endless ways you can combine these things together into a lot of awesomeness.

## Collaborative Transactions

Okay, who here has heard of collaborative transactions or interactive transactions?
Cool, okay.
These are very exciting.
This is a way—it's a protocol—for nodes to build transactions together.
So if we take an example, here we have two nodes, and let's say one of them wants to do a splice.
It tells its peer that it wants to do a splice.
The other peer could say, "Hey, I want to open a channel." And with the collaborative transaction protocol, they can decide to do it together.
So when they do that, they then take their payloads, the splice payload, and the open channel payload, merge them into a single transaction, and then when that gets confirmed, they both get what they wanted through the same transaction.
So this gives us a lot of flexibility with how we build transactions and allows us to make them into one.

How's everyone feeling?
Is this all making sense so far?
Raise your hand if it's not making sense.
Great, okay, either you're all shy or you're all following; I love it.

Okay, so just to really drill this home, it doesn't stop there.
Say there's a third node that wants to make an on-chain payment; they can all three do it together.
And in that case, it still again gets put into one single transaction: combine the open channel payload, the splice payload, the payment, and they all get it done.
Collaborative transactions, otherwise called interactive transactions, is this idea of building transactions among multiple peers, and they're designed to be extensible.
Right now, this is used with dual opening, or dual funding, as it's sometimes called, and it's also used with splicing.
But it could be used with more things in the future.
One notable thing that comes to mind is dual closing will use it.
And potentially, coinjoin services could join into it as well.
It could be used for anything.
It's a totally open, uncontrolled protocol.

## Peer Connections

Okay, so how do you find peers to do this with?
You do it with the Lightning Network.
So it turns out, the Lightning Network works perfectly for this.
We already have peer connections set up.
If you use your existing Lightning peers to find peers to build a collaborative transaction with, it's like a natural fit.
Here's an example.
We're gonna go through the last one we did, which is one guy wanted to do a splice, one guy wanted to open a channel, one guy wanted to do an on-chain payment.
How does that work in practice?

We have one channel that says they'd like to splice; they tell their peer.
That peer is there, waiting with the thing it wants to do.
It wanted to open a channel with this other node.
It tells that node.
And then that node has an opportunity to say, "Hey, I have this pending payment I want to do.
I want to do that, too."
And then that gets relayed back to the initial one.
You have the channel open, and payment payloads are passed up to the first one.

[Audience 1]: "So those are four communications that happen in a row."

Yes, so we have one, two, three, four.
There's actually gonna be a fifth one that's gonna be next, which is the middle node, which will also relay the splice request from the first one over.
So in this way, every node in this particular collaborative transaction ends up getting all of the payload details, and they're passed from peer to peer.

[Audience Max]: "And does ordering matter here?
Like when, which message gets sent when?"

The ordering—well,  the ordering mostly doesn't matter, but you do have somebody who starts it.
In this case, the top node here started the whole process, and the second middle node is responding to that request.
So the second middle node will have some pending stuff that it wants to do, and it's gonna try to save fees, but instead of doing it right away, it's gonna wait till it gets an incoming request and then add in what it wants to add to it.

[Audience Max]: "So this middle node waits for the answer until it coordinates with the right node, like, 'Hey, let's open a channel.'"

Yes.

[Audience Max]: "Then the right node is also waiting until it communicates, 'Hey, I want to make a launch event.'"

Yes.

[Audience Max]: "And then those two bottom nodes are happy, so the middle node will talk to the top node."

Exactly.

[Audience Max]: "Okay, that's cool."

Yep, that's the idea.
I love it.
Any more questions?
Please feel free to holler at any time.
So, at the end of this, each node gets a copy of all...

[Audience 2]: "So does this also apply to channel-closing transactions?"
You mentioned moving dead liquidity to a better channel.
Could you just close that whole channel and just move it all the way over?"

Yes, asterisks.
That's coming.
That's probably what I'm gonna be working on after I finish splicing.
You give a name for it, what do you think?
Splice to close, collaborative close, build close?

[Audience 2]: "I'll think about it."

Okay, awesome.
Yeah, that's definitely coming, but that's still totally at the idea stage.

[Audience Max]: "Sorry, another question to the previous slide."
Here, that right node.
If he wants to make a payment, but the middle node does not talk to him to open it, to open a new channel, that new node could not be part of this whole construction."

Correct.

[Audience Max]: "It's a response, so someone has to invite you so to say."

Yes, yeah.
And you know, maybe at some point there will be some kind of service that they'll invite people just to invite them.
There's nothing stopping that from happening, but as of today, there's no reason to be invited without a prompt.

[Audience Max]: "So one guy starts it and then there's a chain of invitations until that's done?"

Yep, exactly.

[Audience Max]: "That's cool."

So then each node gets a copy of all the payloads, they combine them into a single transaction again, and then once that gets confirmed on-chain, we get the splice.
One guy gets his splice, the other guy gets his channel opened, and then the other guy gets his payment made, and it's all done in a single transaction.
But in practice, this extends much further than just these three node examples; this is to kind of keep it simple.
In practice, this can chain on for many, many, many, many peers, so here's an example.
What is this?
Six peers.
And we have the same guy charge starting a splice, and then they're inviting other peers along their channels to do other things too.
So this one is purposely a complicated example.
We have a splice coming in, two splices, and a whole bunch of people trying to do payments.
And they're all trying to get them done in this single collaborative transaction.

[Audience Max]: "Why do the later guys who want to make the payments get invited?
Because nobody's opening up those new channels."

That might actually be a great point.
Right, the current spec doesn't actually support this.
That's an excellent point.
Anyway, glossing over that.
Okay, so then all of those get combined again into a single Bitcoin transaction.
And in this, we have them all confirmed again; the splices, the payments, all get confirmed in a single transaction.

## Privacy

All right, what about privacy?
How does this work from a privacy perspective?
Who knows what's happening in this whole setup?
Let's dive into the first peer.
What, actually, is this peer made aware of in this entire process?

Okay, let's zoom into it.
That's the peer we're talking about.
He started everything.
He started out saying, "I'd like to make a splice." He was aware of his own action.
Talked to that node, and then what he got back was a request: "I'd like to do a splice and 18 transactions." And that's all he sees; that's all that that node knows.
And there's no way for it to know about the other five nodes that are further down the path.

[Audience Max]: "And each of these 18 transaction outputs are registered separately.
So there's not just one batch request with 'hey, I want to do these 18.'"

[Audience 1]: "Yeah, that's what Lisa said earlier, but I'm not sure I understood the point, because whether it's batch or one by one you still can't infer that it's all from one person or all from separate people.
I was confused about that."

Yeah, that sounds correct.
I mean, the actual protocol moves these outputs over one by one, but my understanding is in practice, there wouldn't be a way to tell anything from that.
Yeah?

[Audience 2]: "Yeah, so this sounds a lot like a v2 channel opening protocol.
Is it the same exact protocol, or is it the v2 channel opening protocol a particular implementation of this collaborative thing?"

Yes.
It's the same protocol.
And there's a lot of benefits to being the same protocol is that it works with it.
So if you wanted to put a dual open v2 and a splice in the same transaction because they're using the same protocol, that becomes possible.

[Audience 2]: "Okay, so basically, it's correct to say you can use the v2 channel opening protocol to do channel splicing."

You could do them at the same time.

[Audience Lisa]: "So we gave that particular - the reusable part of the protocol - we gave the name interactive transaction construction.
That part is used both in the v2 opens and in the slicing protocol."

[Audience 2]: "Gotcha, OK, so v2 opens are like a specific kind of use case for the channel."

[Audience Lisa]: "The setup is different.
The information that you exchange and setup is slightly different, but the actual part of sharing the parts of the transaction is identical to the splicing."

[Audience 2]: "Awesome."

Yeah, does that make sense?

[Audience 2]: "Yeah, when you first said, who knows what the interactive channel transaction construction protocol is, I was like, I might know what that is.
I'm not sure."

So just for the recording, the question was, could you use dual open to do splicing?
And the answer's kind of mostly no, with a little bit of yes.
There's a piece of v2 channel opens that uses the interactive protocol, transact protocol, that splicing also uses.
So they're independent actions, the splicing and the open, but they can work together to create a single transaction.

[Audience 3]: "So you can't do both at the same time, even though they're using the same protocol?"

Oh, you can definitely do it at the same time.
I guess it's kind of how you define are they the same?
So the question is, can you do it at the same time?
If you're running a node and you want to do a splice and a channel open, you would do both of them and then merge the data together.

[Audience 3]: "Okay, but I mean, in terms of diagrams, could we have a channel open as one of these?"

[Audience 4]: "Yeah, like the first node says, I wanna do a splice, and then the second and third node say, we wanna do a dual open."

[Audience 3]: "Oh, yeah, you already said it.
Yeah, you said it last there.
I'm sorry, I forgot, but you had it, the channel."

No, but it's definitely worth revisiting; let's see.
He wants to do a splice, and I'd like to open a channel.
In this example, these are separate nodes, but to answer your question, you're asking, can one node do both?
And there's no reason they couldn't.
There are a lot of ways to spin this sort of stuff.
All right, where were we?
Okay, so we're diving into this node's experience.
It sees that it gets back to do the splice in 18 transactions.

[Audience Max]: "What about the timing of these 18 transaction requests?
Like, might there be some timing effects?"

[Audience Lisa]: "Yes."

Yes.
Lisa says yes, definitely.
I mean, I imagine an implementation could do things to mitigate those, but they're not; there's nothing in the spec that would prevent time inference of information.

[Audience Lisa]: "Yeah, I mean, there's other things you can do.
So there's spectrum supports like adding and subtracting things, so you could add fake stuff and then remove it later.
Yeah, that'd be interesting.

[Audience Lisa]: "So there is a possibility to kind of mess with it.
I mean, I guess if you know what to remove, whatever."

For the mic, what Lisa's saying is that you can do this, you can add in something to the splice transaction and then remove it again later, maybe add it again, and there's been some griefing potentials from there.

[Audience Max]: "So you add an output, and then you remove an output."

[Audience Lisa]: "You could remove an output, yeah.
There is a way to add and remove stuff, yeah."

[Audience 5]: "Or you could also just say I pass, and then on the next round you could be like, Oh, actually, I have more."

[Audience Lisa]: "Yes, yeah.
The risk of that is that your peer ends it before you do, but yeah."

Yeah, that might work, might not; it depends.
If you say you're done and they say they're done, then you lose it obviously.
But you have a chance; they might, and it's probably worth exploring how...

[Audience 6]: "Sorry to interrupt you.
Max, what's the timing exactly?
So one of these other guys who's making the extra payments, you're seeing it happening?
Who's seeing what?"

[Audience Max]: "I'm guessing the longer this chain is, the longer it will take."

[Audience 6]: "It has to pass through the other guys."

[Audience Max]: "Exactly."

[Audience 6]: "I was thinking globally - an observation.
Within the path."

[Audience Lisa]: "Within the path, yeah."

[Audience Max]: "So the difference would be, one example is here you have a long chain versus the other things; it's still just the three nodes and the third node wants to make potential..."

[Audience 6]: "And if it was ..."
you wouldn't have that concern about it.

[Audience Max]: "Yeah."

Yeah, I don't know; maybe you got a random delay on purpose.
It's interesting questions.
Anyway, moving on.
So just to kind of really drive this point home, if you're before this node that's circled, did our peer below do all of these things?
Did it add 18 payments and do a splice?
We don't know.
It could be either.
It could have done it, it could not have done.
So you end up with a plausible deniability where even if you're going just one hop and they're doing stuff, they might have done other hops that you don't know about.
So if they're literally just doing their own stuff, you don't know that it's them.
If they're doing other people's stuff, you don't know that it's other people's; it could be theirs.
So it creates this problem.

## Questions & Answers

That's mainly the talk I wanted to cover.
If you want to go into more technical stuff, we can do that.
But I want to go over any questions.
Anybody, yes?

[Audience 1]: "I was wondering if you could speak on the trade-offs between doing just a normal re-balance and using splice to achieve the same thing."

Sure, the main difference is here you can change the capacity of the channels; re-balances you can't.
So if you're trying to, let's say you have a node that has one channel unbalanced on one side this way and the opposite on the other.
If you can do a re-balance to fix that, you're always gonna wanna do that first, assuming the price is right.
Sometimes the re-balance will just cost you a fortune; if it's not worth it, then it becomes cheaper to do something on-chain and splicing.
But in general, I think every node should try to do the re-balance first at some reasonable rate, and once that fails, you go to these fallback options.
I suspect there will always be positions in the lightning network where re-balancing will never be possible, and in practice, the circular re-balance is kind of a mythical creature that everyone talks about existing and like no one's actually seen it or used it, but they're like everyone else is using it, I think.

[Audience 2]: "I've been feeling very personally shitty for using re-balance instead of circular.
I was told exactly this, that 'Oh, you're missing out on so much, bro, like you could've made ten times more.' So it doesn't even exist."

Yeah, in theory it does and I'm sure people have found it, but I know one guy who literally has a computer set up where it just tries to re-balance every five minutes of every day forever.
Just like waiting for the brief moment of it popping open.
Which is long.

[Audience 3]: "Peerswap fixes this."

Peerswap?
There you go.

[Audience 2]: "There are people that have opened channels to my node that instantly, I call it insta-nuke, where I try and make my channels balanced, and then immediately after I balance it, it goes all the way back to entirely outbound on my end.
It's Pay With Moon does it, and a couple of other of these big lightning payment processors instantly.
I'll spend like 500 sats on two channels and then they'll just go back like that immediately, and I've suddenly only got half my liquidity"

Yeah, I wonder if we could get a mic on him.
I just want to repeat what he said for the TV.
He was saying that he gets a good lighting channel going, he balances it, and then appears like Muun instantly unbalances it for him every time.

[Audience 2]: "But it's Pay With Moon, not the Muun wallet."

Oh, Pay With Moon.

[Audience 2]: "Different company."

Right.
Are your fees high enough?
Maybe your fees are really low?

[Audience 2]: "Yeah, I raised them really high and then tried to do a couple more, and it came to like 24,000 sats.
They stopped doing it now.
I was wondering if that was like what you were referring to a minute ago, like someone monitoring and automatically doing it."

Most likely.
Yes.

[Audience 4]: "Yeah, hi, I've got a question about the mechanics of splicing, because I've been looking at this recently and thinking about it.
Well, I won't describe it, but when you splice, you've got a new transaction, so you've got to wait for it to confirm, right?
So as I understood it, I think Christian Decker told me that you're sort of basically maintaining the state in both the old and the new channels simultaneously.
And I was just, I think maybe this answers yesterday, but I'm not really sure.
I'm worried that if, my particular use case, maybe both channels, well, anyway, because you've got to wait for the confirmation, it might take a while.
Is there something screwy that can happen?
If payments are being forwarded through it and capacity's different, I guess it's just, I think you said it was the minimum; these are the two."


That's right.

[Audience 4]: "Whichever one, if it doesn't work on one of them, then it doesn't work.
Is that basically how it works?"

Yeah.

[Audience 4]: "So this process can take quite a while, right?"

Yep.
The idea is that splicing is changing the channel balance.
There's an old balance and a new balance.
Whatever the lesser of the two is, then you're only allowed to route that amount until the splice confirms.
Yeah, and the way they're done in parallel is in a typical Lightning channel: you have your funding transaction, then a pre-signed commitment transaction, and a bunch of HTLCs in there.
Then, with splicing you just duplicate that.
You have your funding transaction, and you also have the splice transaction, which is a duplicate funding transaction, but it's still pending, and then you create a commitment transaction as a child of that one and recreate everything the funding channel has.
So essentially, it's all duplicate.

[Audience 4]: "Yeah, thanks; it's definitely, I get it now.
My particular use case is a bit weird.
I have a protocol I'm trying to imagine where actually the two parties will sort of sign off on the splice, but then there will be other stuff going on before they even broadcast it.
Does that sound like it will cause a problem?"

Other stuff as in payments?

[Audience 4]: "Well, no, they're pre-signing a bunch of other transactions, and then other transactions get broadcasted, and then this splice-in is actually gonna be delayed with it.
I'm not even sure if this is remotely feasible with a time lock.
Yeah.
Maybe I should explain it to him."

Yeah, it sounds vaguely like a grandfather-pinning attack.
What that is is if in the splice transaction you're adding in-funds from on-chain and those funds coming in aren't confirmed on-chain.
Yeah, I think we've updated the spec that's specifically not allowed for these issues.

[Audience Max]: "So only confirmed coins can be added?"

Yes.

[Audience 5]: "Zero-conf is not gonna happen.
Stop trying to make zero-conf happen."

So the question is, is zero-conf going to happen?
No comment?
How about negative one-conf channels?
Can we do that?
What's up?

[Audience Max]: "How about the ordering of the inputs and outputs of the final transaction?"

That's a great question.
The question is, what is the ordering of them?
They're ordered by serial IDs which are randomly assigned.
It ends up being deterministically in a random order.

[Audience Max]: "Can you elaborate?"

Yeah.
Every time you add an output you give it a serial ID, and then all the outputs have a serial ID, and then you sort by those, and those are just chosen randomly.
Is there a reason that you're thinking about that?

[Audience Max]: "Okay, so why...
Every peer needs to know the ordering."

Yes.

[Audience Max]: "And so how does, I still don't get how to reach consensus on the order."

When I send an output, I also send a serial ID.

[Audience Max]: "Ah, so the person who registers the output also chooses the serial ID?"

Yes.

[Audience Max]: "And that's just a nonce?"

Yeah, exactly.

[Audience Max]: "And the inputs the same?"

Yeah.

[Audience Max]: "Ah, okay."

Yeah, so it's not designed to be secure against anything.
It's just literally this is our deterministic way of determining the order of inputs and outputs of the final transaction.

[Audience 6]: "But that means that an individual user can just choose their serial number, so they can just choose the highest one and make sure that it's still dependent on the list.

Will get in first, yeah, but I mean, there is no benefit in being the first.

[Audience 6]: "The point you're trying to make is that you want a random ordering, and that doesn't really assure a deterministic random order.
Because I could choose a higher serial number and make sure mine is in a particular position.
I know it has no effect economically, but I think privacy - it might screw up privacy - is what you're looking at."

Interesting thought.
I mean, yeah, other than that, I suppose you could deterministically generate the nonces from the outputs themselves.

[Audience Max]: "and/or address"

Yeah, it's an interesting thought.

[Audience Max]: "And how are blame attribution for failure to sign?"

[Audience 7]: "Can you explain that?"

That's a great question.

[Audience Max]: "So we have a coinjoin transaction with many inputs, and the transaction is only valid if every single input signs it.
So if one single input fails to sign the coinjoin, we have a denial of service.
The transaction does not succeed.
You need to attribute that a certain person failed to sign and then ban him from entering in the future because otherwise you just keep on registering the same coin and you keep on not signing and for an indefinite amount of time you denial the service."

Yeah, I think that's a great point, and I think there's a couple of things there.
In other words, signing order, but I believe the best way to do this is to blacklist actual UTXOs. 

[Audience Max]: "But how do you find consensus on which you choose to blacklist among all the peers?"

Well, you just do it individually for your own node, but that's definitely an area where I don't believe there are any actual specs about that.
This is like more of an implementation specific sort of detail, but there is a related thing, which is the signing order, like who is supposed to sign first, which is kind of related.
What we've come to is the best idea, as we understand it, is having the person who put in the least amount of Bitcoin into the transaction, they have to sign first, and then you go up from there to the ones who put in the most and sign last.

[Audience Max]: "Why is signing order important?"

Because there's a potential grief where you could purposely not sign to lock up people's, just to screw with them and make it so they have to double spend their UTXOs in order to get out of the risk of this thing confirming later sort of thing.
[Audience 6]: "But see, that's in answer to your point about blame because if we know the determining signing order, then we know that that's the guy who should sign next, and therefore we blame him, can we?
Did I miss something?"

[Audience 8]: "But if they have an honest reason not to sign, for example, because somebody else added a new legal output or something, you cannot distinguish between them being honest and them being adversarial.
But this could be done with anonymous credentials.
I think that's Max's point."

[Audience Max]: "But who issues the anonymous credentials?"

Satoshi.

[Audience 8]: "All the peers could do it with coconut credentials.
You could have a threshold issuance scheme that still uses monomorphic founding commitments in exactly the same way as verification ones."

[Audience 9]: "I was going to ask, so why would something like a commitment transaction work the way that channel opens and closes work, where everyone has to sign, has to provide a valid signature where everyone can get their money out before the transaction even goes live?"

[Audience Lisa]: "No, you do that for splices and for...
So that happens before the transaction seems to go anywhere.
So you do get ballots; you would get ballot signatures from your counterparty for the commitment transaction."

I just want to relay for the recording that he was asking what if people pre-sign the commitment transaction before doing this, and Lisa was saying yes, they definitely do that already.
So you do a transaction, and before you sign anything with the splice, you make sure all the commitments are signed correctly before you do anything with the splicing.

[Audience 8]: "The threat with these coinjoin type constructs is not that, which this is; we're talking about coinjoin here effectively because everyone's contributing to this, is not economic.
There's no risk of people getting their money lost here, like there is when you put money into a multi-sig.
The threat here is that somebody just chooses not to sign and the whole project fails.
And then you're losing either time—technically,  time value much, but you're losing time anyway, and you have to deal with that.
So denial of service."

[Audience 10]: "I guess as the number of participants goes up, the risk of such attacks increases."

[Audience 9]: "Or just failures, as well as attacks."

Yeah, there's like, if you're a big Lightning service provider and you only have so many UTXOs, this could be a concern for you kind of thing.
But you're not losing money; you're just losing, you're just more cluttered, but it keeps you happy.
Cool, yeah, okay.
So if you have no more questions, I think I'm over time already, so thank you so much.
