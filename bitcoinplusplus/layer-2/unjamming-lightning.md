---
title: "Unjamming Lightning"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://www.youtube.com/watch?v=S7ZH4hr2FlA
tags: ['research', 'channel-jamming-attacks']
speakers: ['Clara Shikhelman']
categories: ['conference']
date: 2023-07-01
---
Okay, so let's talk some Lightning.
So I'm Klara, I'm from ChainCode Labs, and I want to talk to you about an ongoing project that tries to solve the jamming problem in the Lightning Network.
So we'll start from what it is and then we're trying to get it.
So a very quick reminder to all of you about Lightning Network routing.
Let's say Alice wants to route by Bob to Charlie and Grab HTC's for atomic swaps the way it goes pretty much Alice talks let's say a hundred satoshis between herself and Bob telling him if you'll get some secret it will be all yours and then the instructions to Bob that the next hop is Charlie.
Bob locks again funds between himself and Charlie saying okay give me the secret you'll get the funds.
Charlie gives the secret, takes the funds, Bob with the secret goes to Alice Claiming the funds everything is fantastic Bob also can charge a fee when this succeeds.
It's not in the animation, but trust me it happens Okay, so Everything is fun and great But what happens when Charlie doesn't give the secret?
Okay, we have this funds locked and they're just hanging there Until the tea part which is time kicks in and after a while, let's say two weeks, Alice gets her money back and Bob gets his money back, but then for quite a while we have this unusable funds in the channels, which is not fantastic.
Even worse than that is that if we have a malicious actor, for example, so we have the original channels between Alice, Bob, and Charlie, and then somebody, our beloved jammer, is trying to stop this chance from working, they can open channels to Alice and Charlie and then start routing a payment from themselves to Alice, to Bob, to Charlie and back to themselves.
So locking funds here, here, here and here and now everybody is waiting for a jammer to release the cigarette, but he has no intention of doing it and as you can see the direction from Bob to Charlie is completely stuck.
No fans can move this way unless something happens from the other direction.
Of course, if we have a sophisticated jammer that wants to ruin this whole channel, we can repeat the trick in the other direction, rendering this channel useless.
And the fun part for the jammer of this whole thing is that once the payment fails, there is no fee charged either.
So you do have to pay for opening the channels, but from that point, it's all fun and games.
So when we're talking about jamming, there are two types of scarce resources the jammer can try and take over.
The first one is the liquidity, as we've seen in the previous picture.
It's at most the channel capacity.
It depends on the direction, things like that.
And when the attacker aims at the liquidity, they will take all of the available Satoshis and just lock them in these HTLCs. Another scarce resource is slots.
So, in general, we have about 483 slots per channel.
You can push this number a bit higher, but at the end, it's a limited number.
Each HTLC needs its own slot.
So if I go and send 483 payments, HTLCs over a standard channel and don't release them, nothing else can go through it.
So generally, a jammer trying to ruin a channel will take up either all of the liquidity or all of the slots.
And this difference is going to be important a bit later on because this is quite different from the behavior of an honest payer trying to send payments.
So I'll go get some water and we'll see if we're all on the same page.
So the motivation of the jammer could be various things.
If we're talking about a personal level, a business competitor, there's a routing node.
I want their traffic.
I want their fees.
I just jam their channels.
They can't do any business.
All the business goes to me.
There's a service provider, somebody selling t-shirts.
They can't sell t-shirts if they can't get payments, so everybody has to come over and pay for me.
A different route is There are also people that sort of want to see the world burn.
So for example, maybe I want just to disconnect a bunch of nodes just to make them suffer, for lulls or whatnot.
Or I want to break the lightning network into two parts.
These are all options with the scanning attacks.
Another thing, sometimes I want to push flows towards myself, not from a business point of view, but if I'm trying to accomplish attacks in the spirit of flood and loot or things like that, there's a family of attacks that depends on other people routing through me a lot of expensive HTLC.
That is locking a lot of Satoshis and this depending on me, or me having a lot of past, in the past, having some, me publishing some stale conditions, then trying to get justice on chain and not being able to do that.
So for me to initiate this kind of an attack, I need to have a lot of flows going through my channels and jamming any other option is the first step to get all of this and then I can go ahead and do this flood and load style of attacks.
So in general jamming is not great.
So when we're thinking about jamming we will think about two kind of flavors or ways that people can go about them.
We will call them slow jamming and quick jamming.
And the main difference would be the time to resolve.
So in the slow jamming, somebody locks up all this HTLCs, not releasing the secret, and then this, they hold HTLC for hours or days or something like that.
In the most subtle quick jam, the HTLCs are released with a fail message within seconds.
But then you can just send something, hold it for 10 seconds, release, and immediately send a new one.
So the end result is the same.
For hours or days, channels are absolutely useless.
But the way it's performed is slightly different, and it has some importance.
And this is important because the slow jams are very predictable.
Okay, you have HTLCs hanging for a few hours or days, somebody is doing something wrong.
Maybe they're malicious, maybe they have no idea what they're doing, maybe something in the route went wrong, whatever it is, somebody is not great.
With a quick one, it's harder to pinpoint.
Because maybe there's just a flood of not great transactions over the network.
Maybe there's a reason for all these failures or something like that, it's harder to say, okay, now somebody is doing something wrong.
Now this HTLC is a bad one because it's just one of this endless flow that takes up a lot of things.
For these reasons, the solution is a two-part.
And when we're thinking about slow solution, we will use something that we call reputation or local reputation.
It's a very, very soft version of what we think about when it comes to reputation.
But in the quick part, because it's not easy to blame, we're just going to use fees or more specifically, unconditional fees.
We're going to ask people to pay just a little bit for failures.
So this is the general scheme and I will jump into the details.
Cool.
So just as an overview, when we're talking about reputation, we're talking about local peer reputation.
So it's the smallest kind of scope of reputation we can think about.
It is aimed to stop the slow gems.
And here, each node assigns reputation only to other nodes that they have a channel with.
Okay, so just the neighbors.
The neighbors I have a direct interaction with, I'm receiving HTLCs from them, I can observe what's going on there, and these are the nodes that I'm going to care about the reputation.
Now, the reputation is not a big deal.
If you have an excellent reputation with a neighbor, The only thing that it gives you, it gives you more access to more slots and more liquidity.
Even if your reputation is not great, it's okay.
You're a new guy in the neighborhood, nobody knows you.
You have access to some liquidity and to some slots.
It's usually okay for any use, any everyday use or something like that.
But to have the ability to use all of the slots or all of the liquidity in a channel, you do need to gain some reputation with this neighbor of yours.
So this is the idea behind local computation.
And when we're thinking about unconditional fees, again, this is aimed to stop this quick jamming.
These things that we can't exactly pinpoint that this is an attack.
This is paid even if the payment fails.
So unconditional, doesn't matter if failing or succeeding.
And it's soft again to compromise the jam node.
So if we're thinking about a routing node, there's like a usual traffic of business and then usually 20 of the slots are taken up by actual users, and there are some fees that we get.
Now, when a jammer comes in, they cannot take only 20 slots.
They have to take almost 500 slots immediately.
So they will have to give me more money than in unconditional fees.
Even if they fail, this will start adding up, and at least to some extent, compensating me for the business I lost.
But even more than that, this would be actual money that I have to pay, where a single user is just taking up one slot.
This is going to be just a few Satoshis.
And from simulations, we're talking about 2% from the success case fee.
Something that you won't really notice if you're not trying to run any shenanigans, and you're not just sending 100 failed transactions because you don't know what you're doing.
So this is the general scheme.
Okay, so let's jump a bit deeper into reputation.
I will say this is a project under discussion right now.
So there are still a few arguments.
And there's like a suggested PR in the spec.
There's a discussion.
I'll talk about this a bit more towards the end and how can you join the fun.
But this seems to be the part where most people are on the same page.
Reputation, as I said, would use it to determine the allocation of resources.
In the beginning you have some resources, rate of reputation, you can extend this.
So the way it would work for example is as before Alice offers this HTLC to Bob.
Now earlier, asking him to forward it to Charlie, earlier Bob would just go ahead and do that if the liquidity and slots are available.
Now Bob will first of all think, what do I know Alice?
What's her reputation?
If he looks at her and goes, Alice is fantastic.
We had this job for years, paying very good fees, transactions resolved, everything's great.
Sure, forwarding this to Charlie, and hopefully everything resolves.
In a different case, let's say a different Alice offers him this HTLC.
Now you'll notice that first of all, if Bob accepts it, this is the last of the liquidity that he has in this direction.
And now he looks at Alice and he doesn't know anything about her.
Maybe she's great, maybe not, but because she's asking the very last part of his liquidity, he will fail payment and return this.
So this is the general idea of reputation.
Again, reputation is local.
Bob has only an opinion about Alice and Charlie.
Charlie, for example, doesn't have any ideas about Alice, doesn't assign any reputation or anything like that.
Yeah, so we only keep track of our direct neighbors, because this is the interactions that we're having, and also we don't have to agree.
So Charlie has some idea about Bob, gives him some reputation, so does Alice.
This could be two very different reputations depending on the very different experiences with Bob.
So our reputation is very, very local and helps us manage things.
Cool.
So this is, so up until now, I think this is, everybody's on the same page.
Here, I am presenting the direction that I like.
There are a few more ideas floating in the space, But in general, I think that having a very binary kind of local reputation is more than enough and this is the regularity that will get us where we want to be going.
And the idea here is, again, we give reputation to a neighbor, and then a neighbor can endorse payments that they forward to us.
Okay, so a neighbor, first of all, has a reputation, zero, one, and when they're offering us a payment, they can say, did it come from a trusted source or did it come from an unknown source?
I can't say what to do with this.
So Alice, for example, so Bob and Charlie are trusted neighbors while David is the new guy.
She knows nothing of him.
So Alice would forward, use all her liquidity and endorse a payment, if and only if it comes from a neighbor she trusts.
So Bob offers her an HTLC, she trusts Bob, Bob endorse this HTLC saying, this came from somebody I trust.
Alice goes, fantastic, forwarding this to Zoe.
Well, when David offers her an HTLC telling her, listen, this is a fantastic HTLC.
She's like, I don't know you, David.
I will forward it, but without endorsing.
OK, so she will forward it, but telling Zoe unknown source.
So do what you wish.
Also, David could offer this, and if Alice doesn't have enough liquidity or slots, she might fail it.
Similarly, if Bob gives her something unendorsed, maybe she will forward it unendorsed or maybe she'll just fail it.
And yeah, it's important to note that the allocation of resources is per channel, so everything was examined in light of her channel whatsoever.
Okay?
Yeah.
So, as we said, we're talking about the binary case.
So the reputation is either high or low.
Reputation is gain if you forward payments that first of all, they succeed quickly.
They behave as good behaviors should be behaving and they pay enough fees Okay, so opening a channel and then sending this one payment that succeeds once a year is not enough okay, so if you want to have a lot of business resources, you should show yourself as a reputable and worthwhile business partner to that extent.
Okay, so this is what we're looking at.
Of course, if you're sending things that you endorsed and then they failed or, God forbid, got stuck for two weeks, you would lose your reputation.
So reputation is lost when they're clearly gems or you used to behave very well, and now you're just disappearing or not doing a lot of business.
But the rule of thumb is that reputation is difficult to gain and easy to lose.
And again, remember that having the beginner's reputation, you're appearing, You're still good to go and buy your coffee, pay what like me.
You can do most of the things you want to do, just not to do the heavy trafficking of either small payments or a lot of liquidity.
But the downside of reputation is that there are always edge cases.
Okay, we can draw the lines, we can be as sophisticated as we want.
There's always, always, always something.
I know in this audience, they're like, I don't know, some of my best friends, they make their lives living from looking at edge cases and breaking things.
It's a fun hobby, yeah, for fun and profit, but edge cases must exist, there's no way around it.
Now, for example, we say like, okay, so your transaction must resolve within 10 seconds, otherwise it's a big no-no.
Sure, I'll resolve it within 9 seconds and send another one, and another one, and another one.
Or, for example, 50% of the transaction need to succeed.
Okay, so I will open a bunch of channels to your neighbors and then route through them and all the failures will happen on the channel that I'm trying to attack, which is not a direct neighbor of mine.
So I will use the fact that there's a privacy with WAPT to ruin any rule of this spirit.
And so this such cases is what we nicknamed quick jamming.
And to stop it, it's very difficult to detect.
That's the main punchline.
And to use them and to stop them, we want to use the unconditional fees.
But we're always remembering that this is something that rarely can happen to an honest user.
Sometimes it will send an HTLC.
It would get stuck.
It's not on you.
So we can't have any severe punishment for this, but we do want this behavior to be punished if there's something systematic that you're trying to do.
So for this, we have the unconditional fees.
So as I said, currently fees are charged only for successful payments.
So this allows, for example, one thing, jamming, but in general, having the ability to DOS or to send things around the network without any precautions allows a bunch of other things.
For example, it allows spamming, just like throw messages, do things around things that the network, people that joined the network did not agree for the network to be used and they are, for now, they have to facilitate.
And other things that happen is probing.
So probing is a softer thing because personally I don't think it's like a great evil If you probe a bit or just send channels, you want to do better channel routing.
But then for example, if I'm probing the whole network to try and see where are payments going, who's doing what, there should be a line where you're saying, okay, you can probe, we can stop that, we can tell the difference in many cases, but it can't be free.
You're asking to use resources from people, you're asking something from people, it makes zero sense for this to be like, yeah, sure, whatever, have as much as you want.
So for the reason that we're allowing free failures, we can do this three things and probably a bunch of other variations that creative people will come up with.
So what we're suggesting is a standard, the standard structure for fees.
Also in a conditional case, there would be a base fee, and there's going to be a proportional fee.
So this is, first of all, to stop jamming.
And as we remember, jamming uses one of the scarce resources.
So if I decided to use liquidity to jam you, I will have to pay something from the proportional fee.
I will have to pay a hefty sum because I'm taking all of your liquidity.
And that's, even if I'm taking 2% from the success case fee or something like that, this things add up.
And remember, I have to redo it every, I don't know, nine seconds, 20 seconds, one minute.
But again, if I want to cause the node that I'm attacking some pain, this will have to start adding up to more and more and more.
And also, as a bonus, if we're charging a proportional fee, this means that also probing me will cost you something.
You do this once, it's not the end of the world, but if you make a habit out of it and try to do it on a large scale, this will start to add to some kind of a bill.
Similarly, so you don't want to pay whatever you get, you have to pay to try to take up all of my liquidity, you go ahead and you try to take up all of the slots, sending the smallest payment you can get through the network.
And then the proportional fee will be nothing, but that will be the base fee.
And because you have to take up this almost 500 slots, when you multiply this, it will grow up into something.
And again, as a bonus, This is if you're just running things around, spamming around, you still have to pay the space fee because you're taking up a resource of mine.
Cool.
Okay.
Everybody hates paying for failures, right?
And this is the worst.
Nobody likes consequences.
Nobody likes anything.
Okay?
This sounds horrible.
Why would we do that?
So we have to do that for all the reasons we talked about earlier, but the truth is that it's not that bad.
And here's a graph, because a graph is fun.
The thing about this is that if you're trying to send a payment, the number of retries you have to do is not that large.
So for example, let's assume the probability of route failure is 10%.
And you want to send, you're asking yourself, how many times will I need to retry to guarantee a success rate of 99%?
Okay, just do it twice.
Okay, so for the first one, you might have to pay this unconditional very small fee, but by the time you do the second try, this one will go through with very good probability.
If you want to get to 99.99, okay, with that 10% route failure, you just try it three times, okay?
And also, If our failure rate is 50%, so first of all, what's up?
But this happens sometimes.
Unconditional fee would be, I don't know, not the first thing I would worry about in this case.
But still, I want to get to a 99% probability, I need to retry it seven times.
Because that additional fee is something small, it's like 1%, 2%, at the end, Instead of you pay 10%, 20% more, but it's not changing orders of magnitude.
It's not even twice than what you were planning to pay in fees when routing.
Now, there are two cases.
Either you are a savvy Lightning user, you know, going to BTC++, having fun, doing your things, you understand jamming, you know the problems, and then you're like, okay, yeah, I'll pay.
If you want Satoshi's, it's not the end of the world.
If you are a wallet user that has no idea not how Lightning works, not what are fees, nor how keys are paid, this is something on the wallet to sort of hide from you.
So for example, the wallet presents that the fee is going to be maximum something.
Playing it super safe, one success case fee and 10 failures.
And then in the worst case, you end up paying less for routing.
And then nobody's ever angry for, oh, it ended up being cheaper.
It's not the end of the world.
So there is some UX work to do in the way we present this, in the way we talk about this, but the truth is if we're not trying to jump the network, the amount of this payment for failure on conditional fee is just pretty small.
And we need to have a correct presentation of it when we're talking to users.
Cool.
So the main challenges that we see for the future is, first of all, all of this, we're doing simulations in times of peace.
Nobody is attacking the network.
We have not experienced this spirit of attacks, at least not on a large scale.
So we're sort of guessing what the attacker will do, what users will do, and things like that.
And we have to accept the fact that these simulations are with a grain of salt.
Another thing is that we have to keep in mind in this work is that any mitigation strategy could create a new attack vector.
So we don't want somebody to create some honeypot and then bring a lot of people in, taking this unconditional fees from them.
I don't know.
There's lots of things that we should be very, very careful about.
A lot of thought is going into this.
And we also want to think about influence on the honest user.
We talked about this in UX when we're talking about unconditional fees.
It also has to do with the way we build the reputation and things like that.
So these are the things that we're facing right now and we're trying to work around them as carefully as possible.
So in general, fees and reputation, hopefully, will stop jamming.
So, there's a blog post linking to the original paper and a small POC for reputation.
Over here, There's some spec PR suggestions linked over here.
This is an ongoing process, but these are the things.
Any questions, any feedback, it's one of my favorite conversation topics, So please don't be shy.
And we have a call every two weeks.
The next one is this Monday.
It's usually announced on the mailing list.
So please join us.
Tell us your thoughts.
Yeah.
This is happening.
Have you explored the backwards propagation research that they've been doing for like spamming Vault 12 on your messaging?
Like how much, it almost kind of works in the same binary scenario as before, but it's basically I'm telling you, slow down, the previous node, hey, you should probably tell them to slow down, and then it sort of resolves itself with the simulations.
Like is it similar or like how do you guys work with that?
There are many similarities in spirit.
There are some issues there because it's almost as a reputation that it's larger than the local.
And the thing is that it opens some possible attacks.
And we find that the local thing is just safer in many ways, especially with the endorsement part, where you get to say, listen, this is not me, I want to throw it out, it's okay, it's not mine.
So it is very, very similar in spirit.
Personally, at least I find this just being more careful and enough to stop the whole jamming thing.
But other people, for example, suggest not to use more than 50% of your liquidity for privacy reasons and things like that.
So there's a lot of similar ideas happening for different reasons, but I think it will add up to There will be some limitations to what you're about to do on the network.
I mean I could ask questions.
Do the, there we go.
Yeah, let's take it offline then.
Thank you.
Bye bye.
Bye bye.
Bye bye.
