---
title: Rene Pickhardt - Splicing
Transcript_by: Caralie Chrisco
categories: [‘residency’]
tags: [‘lightning’, ‘splicing’]
---

Name: Rene Pickhardt

Topic: Splicing

Location: Chaincode Labs Lightning Residency 2019

Video: https://youtu.be/ZzSveBMtUGI

Transcript by: Caralie Chrisco

## Introduction

So splicing basically means you have a payment channel, you have a certain capacity of a payment channel and you want to change the capacity on the payment channel. But you don't want to change your balance right? For balance change [here if you fill it about right because it can't] separate swapping since a month we'll get some money on it. But splicing really means you want to change the capacity. 

I mean the obvious way of doing this is close the channel, make a new channel with the design capacity and you could. The question is can we do this in a way that the channel keeps on operating by doing a splicing operation? Because regularly if you open a channel you need six confirmations on the blockchain. It takes some time, so not so great. So we want to think about how we could do this in a non-blocking way. The reason why I'm doing this format in this way currently is when I joined the lightning community back really trying to June last yeah it was a mighty big day and people from lightning necks were there they were telling me about all those concepts that I never ever heard of before like atomic multipath routing, splicing, watchtowers, like I didn't know that stuff. 

I thought well splicing is really cool because if you have splicing, you have an amazing user experience, because you don't need to bother any more about your on chain, off chain funds. You just show your funds in the wallet and whatever you can't pay off chain you could just splice something in. It's like an onchain transaction that just changes everything. 

So, I thought this was really cool and the guys from Lightning Labs were like, 'Yeah we're working on this.' And I thought this would be so difficult, because concept wise I mean what could happen right? You have a funding transaction and the funding transaction has something like some commitment transaction here that is like the animation of Christian’s here where you basically have several versions of this right? So what you're going to do, you just like use for example when you want to splice in, outputs are always circles, right?

Audience Member speaks. 

Rene: Okay so let's just say you have a new output and you basically somehow merge these and you get your new funding transaction F2, right? So you make a split like this, where you have two. Something like that. [inaudible] So I mean how difficult would this be right? I was sitting down and I mean I was still pretty new to Bitcoin and Lightning and everything. I was writing down some of the scripts and transactions and I thought, 'hey I can solve this.' So I volunteered on the Lightning Network mailing list, and I was like, hey I can spec this out. People were like not responding to me.  I was starting to look deeper into this, and then I realized so actually it's really difficult.

Audience Member: So the name and it should have given it away. I can tell you later about why I called it splicing. But splicing is really nice from any practical point of view, but it's really difficult once you get into the details.  The hidden difficulties were already named. 

Rene: What I'm trying to do with you right now is to figure out why it's actually difficult. So I want to make this a short session. I don't want to find all the difficulties but I want to be interactive with you, of like why is even this thing if we make it in this way, difficult? Like this would even be [like a blocking way right? Because now we have to somehow attach the new commitment ] transactions through this and we have to like wait and at this time we can't operate this channel. But even this way right why would it be difficult? And it would be really great if it's not always the same people, yeah Fabian.

Audience Member: What you were saying now, that the channel keeps operating is really taking <inaudible> like the financial section and beacons had it sent to another funny connection and we can update our commitment to infections like in a horrific way in through a protocol that I think you can work trust us. Then at the same time keeping the challenge like updating like that's when the complexity explodes basically. 

Rene: Okay so here, I agree with you. So here's my suggestion and I think there's something similar to something that I came up with this time when I crafted this mailing list post,  which is somewhat ridiculous. 

A funding transaction lives on a 2-2 multi-sig, right? So why can't I just send some funds to that address right? So let's say this is like some Bitcoin address 3XK5 whatever. So I take some Bitcoin and I just sendmore Bitcoin to this Bitcoin address.

Audience Member Speaks  mmm if two channels right well well I keep on I keep one 

Rene: I keep on operating on this one and as soon as this one is confirmed and I do this with the same method of like, this is my funding transaction too. Changing this picture a little bit now if this funding transaction - and this one already has commitment transactions right? Which is actually C prime and as soon as this one has enough confirmations, what I do is I say from now on I only use commitment transaction C prime. Prime that are spending these two funding transactions. I could flip that couldn’t I?

I mean I’m just suggesting when I'm just doing two new funding transactions with the same wallet I mean I can operate this all the time right? I already have commitment transactions pending this so it's safe for me.

Audience Member asks a question

Audience Member: From a privacy point of view, since it’s interactive anyway, get a new set of keys, get a different address, you know that they’re the same but not everyone is asking, right?

Rene: Fair enough, but let’s understand the difficulties first. 

Audience Member: So C prime is for just there to refund you?

Rene: C prime is just there to refund you. It's just there that I know when I Spy something it's no big deal for me. I keep on operating this one and as soon as this transaction is really confirmed I make a new commitment transaction that now is spending these two funding transactions and this is my new spliced channel. Why is that not working or why is that difficult,  why's that tricky?

Audience Member: That looks way easier than what I had in mind. 

Rene: That is what I had in mind at that time. I was like why are you all so, why is splicing so difficult for you? Literally. 

Audience Member: So the revocation would have to revoke on both sides?

Rene: Well you have to revocation keys for these commitment transactions already right? And at some point in time you have to 

Audience Member speaks

Rene: What do you mean atomically?

Audience Member speaks

Rene: Yeah, why not? You have messages on the peer protocol, just reveal the revocation key at the same time.

Audience member: And you can have him have the same revocation key. 

Audience member: Yeah, you can share 

Rene: Well not really because you operate this channel and this one but here you could you could make the same as here, as the current state. But, yeah that’s even more.
Audience Member: It does allow for larger HTLCS, but it's also you've got two inputs so now you're gonna have two signatures. Like it's halfway between hundred two channels at one table away yeah and so that might be and probably cope with change well

Audience Member: Why is that difficult? 

Audience Member: 

Rene: A it's done teasing comb like so my signature yeah well then you guys now you've got these channels that are like you know just a coaching but it's a fairly I'm gonna imagine like thank you these implementations they're really 

Rene: Sure but Felix again what do I know some network do you know I need a funding transaction we have to funding transactions it's going to be messy for the gossip protocol. 

Audience Member: why too funny cross section you should have the spice into elections paintings of funny outputs and on top of the spice introduction commitment transaction the splicing touch being confirmed  feel like you're nothin I'm I'm a very it was again but can we first visualize what you're saying then everybody else can join because I mean you say this and I think Fabrice understands you and I think I can follow but I'm not sure if everybody else was able to grasp this quickly. So you have a different idea for my supporters why are we doing a splicing 

Audience Member: spice and 

Rene: let's discuss it at this point in time splicing 

Audience Member: splicing yeah okay so you may have a splicing cross-section alright so we're making our own suggestion right so so this was passing by our name I'll become oh yeah okay funding I'll put my funding treads at you ugh where's our microtransactions right yeah right I know you are the spice introduction okay and that's the point no no I do 

Audience Member: how is that different than what you can do now you mutually closed the channel but instead of use the regulations actually just add another input and then add and change the output to be a new channel 

Audience Member: so the idea there behind splicing is basically east ones never touch a single thing so you can be absolutely sure that s will eventually confirm so you can start building on top of this that's the main difference between closing and reopening.

Audience Member: How can you be sure because all the puns are smooches funny on non vult e-cigs and 

Rene: you know channel partners following the protocol and if the channel is not following the code so yes you got you I mean you shouldn't compute No ah 

Audience Member: yes because otherwise I know that you may have input one can do even without PTC if you have an output on see if you have 

Audience Member: not put on c3 prime just giving back this one to the other guy and you don't add this from the channel until is a splicing transaction International versions of the of the state 

Audience Member: If f1 is a multi so you can basically switch over to just continuing yeah right no it's not 

Rene: Well as soon as this is confirmed you can switch over.

Audience Member: Yeah if he's confirm you know and if that is not what you see at some point yes I'm paces confirmed right yeah yeah yeah so and then if can't be CC shows you know you can't use them until it's it's spicing is not perfect continuous page I'm not saying we're trying to understand why it's actually so tough right and 

Rene: I hope that we want to talk a little bit more okay I stop because well 

Rene: I mean what you can do is I think in November last year rusty was making a proposal for splicing protocol and when you read it it's actually really hard to figure out if he was using a mechanism like this or like this because only talking about was the general protocol. Like what kind of revocation keys are we sending back and forth? How do we trigger splicing? How do we move the funding transaction right because in in this scenario what you have to do and gossip you have with gossip to tell them hey by the way this is my new funding transaction at some point in time like once the splicing is locked in gossip has to know that this is actually Noldor right 

Audience Member: So there's this position period where we see F being good being being spent and therefore the channel is closing but not because we are transitioning to s so there is a grace period where you don't close it 

Rene: Remember what I told you about gossip right gossip doesn't have this close channel message a channel is closed and gossip if you see the funding transaction is spent on chain. So the channel disappears right? it's its operation but it disappears 

Audience Member Speaks

Rene: well well you see as a member would write which kind of sequence that F is spent but you don't have to look at it because you don't know where it's being mined so you can't announce this on gossip because it was attributed work right 

Audience Member: Also we don't we don't allow channel announcements if the funding transaction isn't that doesn't have at least six confirmations so so the rest of the world the channel would put a little active or 

Audience Member: six should maybe in a weekends I mean I'm spending and funding approach which has been previously and yeah so so you don't have to wait six confirmation.


Audience Member: so we would have to pre-announce my Flickr 


Audience Member: Why not change the gossip channel announcement 

Audience Member: is looks like sort of a transaction that has an input and the output is the channel ID? 

how does fly south I just want to say one point he make the basis to like so so that's basically my answer we can do a lot of stuff right but depending on what we do it has severe consequences along and that was for me a thing that I needed to learn over a four year three quality like for a long time because I was just drawing these pictures of me like hey yourself splicing why was it so difficult for lighting gifts to this 

Audience Member: so try mixing in the backwards compatibility with notes that might or might not have upgraded yet and 

Rene: So yes we couldn't talk a little bit more about splicing out how this might look like but my feeling is that the main point that I want to transport you it was successfully transported and the funny thing however is this that my feeling is in this group there's many people know who understand the difficulties of protocol development, who can actually walk through the proposals, actually really like make suggestions like really see on which parts of the protocol are being impacted and why are they being impacted and what should we keep in mind right because overall you if you know yes yes you can't in this country yes yeah but I'll 

Rene: Just think about gossip and all these things right at the entire channel protocol. I mean before you only like you know you have different states that know what cure I mean it's just like these kinds of questions that arise so yeah but in edifice spirits you can do a lot of stuff no 

I think that's really the spirit that people should have been looking at these problems. So anyway I would pass over to the next person, hope that this was enlightening. 

Audience Member: Yeah part here is there are no dumb ideas just because we went down one rabbit hole doesn't mean that they're simpler version stuff you guys might come up with so tell us if we're being stupid about these things. 
