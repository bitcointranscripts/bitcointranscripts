---
title: Splicing
transcript_by: Caralie Chrisco
tags:
  - lightning
  - splicing
speakers:
  - Rene Pickhardt
date: 2019-06-26
media: https://youtu.be/ZzSveBMtUGI
aliases:
  - /chaincode-labs/chaincode-residency/2019-06-26-rene-pickhardt-splicing/
---
Location: Chaincode Labs Lightning Residency 2019

Transcript by: Caralie Chrisco

## Introduction

So splicing basically means you have a payment channel, you have a certain capacity of a payment channel and you want to change the capacity on the payment channel. But you don't want to change your balance right? For balance change,(inaudible) we'll get some money on it. But splicing really means you want to change the capacity.

I mean the obvious way of doing this is close the channel, make a new channel with the design capacity and you could. The question is can we do this in a way that the channel keeps on operating by doing a splicing operation? Because regularly if you open a channel you need six confirmations on the blockchain. It takes some time, so not so great. So we want to think about how we could do this in a non-blocking way.

The reason why I'm doing this format in this way currently is when I joined the lightning community back in, I really joined in June last year. It was a Lightning Hack Day and people from lightning hacks were there. They were telling me about all those concepts that I never ever heard of before like atomic multipath routing, splicing, watchtowers, like I didn't know that stuff.

I thought well splicing is really cool because if you have splicing, you have an amazing user experience, because you don't need to bother any more about your on chain, off chain funds. You just show your funds in the wallet and whatever you can't pay off chain you could just splice something in. It's like an onchain transaction that just changes everything.

So, I thought this was really cool and the guys from Lightning Labs were like, "Yeah we're working on this." And I thought this would be so difficult. Because concept wise I mean what could happen right? You have a funding transaction and the funding transaction has some commitment transaction here that is like the animation of Christian’s here where you basically have several versions of this right? So what you're going to do, you just use for example when you want to splice in, outputs are always circles, right?

Audience Member speaks.

Rene: Okay so let's just say you have a new output and you basically somehow merge these and you get your new funding transaction F2, right? So you make a split like this, where you have two. Something like that.

[inaudible]

So I mean how difficult would this be right? I was sitting down and I mean I was still pretty new to Bitcoin and Lightning and everything. I was writing down some of the scripts and transactions and I thought, "hey I can solve this." So I volunteered on the Lightning dev mailing list, and I was like, hey I can spec this out. People were like not responding to me.  I was starting to look deeper into this, and then I realized it's actually really difficult.

Audience Member: So the name and it should have given it away. I can tell you later about why I called it splicing. But splicing is really nice from a practical point of view, but it's really difficult once you get into the details.  The hidden difficulties were already named.

Rene: What I'm trying to do with you right now is to figure out why it's actually difficult. So I want to make this a short session. I don't want to find all the difficulties but I want to be interactive with you, like why is even this thing if we make it in this way, difficult? Like this would even be like a blocking way right? Because now we have to somehow attach the new commitment transactions through this and we have to wait and at this time we can't operate this channel. But even this way right, why would it be difficult? And it would be really great if it's not always the same people, yeah Fabian?

Audience Member: What you were saying now, that the channel keeps operating is really making the headaches. We can take the current state of the transaction by the funding transaction and we can have it sent to another funding transaction and we can update our commitment transactions in a collaborative way through a protocol that I think can work trustless. Then at the same time keeping the channel here like updating like that's when the complexity explodes basically.

Rene: I agree with you. So here's my suggestion and I think there's something similar to something that I came up with in this time when I crafted this mailing list post, which is somewhat ridiculous.

A funding transaction lives on a 2-2 multi-sig wallet, right? So why can't I just send some funds to that address? So let's say this is like some Bitcoin address 3XK5 whatever. So I take some bitcoin and I just send more bitcoin to this bitcoin address.

You have two channels, right? I keep on operating on this one and as soon as this one confirmed and I do this with the same method of like, this is my funding transaction two. Changing this picture a little bit now. If this funding transaction two - and this one already has commitment transactions right? Which is actually C prime and as soon as this one has enough confirmations, what I do is I say from now on I only use commitment transaction C’’ that are spending these two funding transactions. I could flip that couldn’t I?

I mean I’m just suggesting when I'm just doing two new funding transactions with the same wallet I mean I can operate this all the time right? I already have commitment transactions pending this so it's safe for me.

Audience Member: From a privacy point of view, since it’s interactive anyway, get a new set of keys, get a different address, you know that they’re the same but not everyone is asking, right?

Rene: Fair enough, but let’s understand the difficulties first.

Audience Member: So C prime is just there to refund you?

Rene: C prime is just there to refund you. It's just there that I know when I spy something it's no big deal for me. I keep on operating this one and as soon as this transaction is really confirmed I make a new commitment transaction that now is spending these two funding transactions and this is my newest spliced channel. Why is that not working or why is that difficult? Why's that tricky?

Audience Member: That looks way easier than what I had in mind.

Rene: That is what I had in mind at that time. I was like why are you all so, why is splicing so difficult for you? Literally.

Audience Member: So the revocation would have to revoke on both sides?

Rene: Well you have to have revocation keys for these commitment transactions already right? At some point in time when you make this new commitment transaction you’ll get a revocation key for this one, you get a revocation key for that one you might not necessarily need.

Audience Member speaks

Rene: What do you mean atomically?

Audience Member speaks

Rene: Yeah, why not? You have messages on the peer protocol, just reveal the revocation key at the same time.

Audience member: And you can have him have the same revocation key.

Audience member: Yeah, they can share revocation keys.

Rene: Well not really because you operate this channel and this one but here you could make the same as here, as the current state. But, yeah that’s even more.

Audience Member: It does allow for larger HTLCS, but it's also you've got two inputs so now you're gonna have two signatures. Like it's halfway between having two channels and one channel in a way. Probably the code is all going to change after this.

Rene: Why is that difficult?

Audience Member: So you have another signature?

Audience Member: Well now you got these channels that are a channel and a half kind of thing. It’s just a code change, but I'd imagine in C Lightning it’s a fairly big code change.

Audience Member: What do you announce though?

Rene: Ah! Thank you. That is what I was waiting for.

Audience Member: So you’re worried about code complexity in all of these implementations…

Rene: Sure. But Felix, again, what was your question?

Felix: What do I announce to the network?

Rene: What do I announce to the network? You know, I need a funding transaction, but I have two funding transactions and that’s kind of messy for the gossip protocol.

Audience Member: Why having two funding transactions, you should have the splice ….inaudible

Audience Member: Then is it really more efficient than closing channels?

Rene: Wait. I like his input, I’m very happy for you to do it again but can we first visualize what you’re saying first so everyone can join? Because I mean you say this and I think Fabrice understands you and I think I can follow, but I'm not sure if everybody else was able to grasp this quickly. So you have a different idea for a splicing protocol, right?

Audience Member: First of all, are we doing the splicing in or splicing out?

Rene: Let’s do splicing in at this time.

Audience Member: Splicing in. So you may have a splicing transaction.

Rene: We're making our own Antoine suggestion. This was splicing by Rene and this by Antoine.

Audience Member: You have funding outputs,

Rene: Funding transactions and my commitment transactions

Audience Member: You have a commitment transaction And now you have a splicing transaction

Rene: Where?

Audience Member: Spending is the funding outputs and your other inputs

Rene: So this one is spending the funding and some other, let’s call it F1 -

Audience Member: Before you broadcast it, you have the commitment transaction on top of the splicing transaction.

Rene: So now I have commitment transaction C prime

Audience Member: According to the last state of the -

Rene: Which is the same as this one basically. Not exactly the same because you have more funds to go

Audience Member: Sure, but the outputs are the same.

Audience Member: But you can’t use your existing channel while that’s confirming?

Audience Member: That’s the same thing as closing and reopening the channel basically.

Audience Member: Because now you’ve committed to the C- and it has the current balance and you can’t update that current balance.

Audience Member: Oh can’t I?

Audience Member: Can you?

Audience Member inaudible cross-talk

Rene: That’s the point. Now I do C3 and C1, and C prime...

Audience Member: That’s already possible. How is this any different from what we can do now? You mutually close a channel but instead of using the regular transaction you just add another input and change the output to be in your channel - that’s the same.

Audience Member: So the idea behind splicing is basically these funds never touch a single sig so you can be absolutely sure that s will eventually confirm so you can start building on top of s. That's the main difference between closing and reopening.

Audience Member: How can you be sure it will be confirmed?

Audience Member: Because all of the funds are basically already on multi sigs.

Rene: You learn how to move them. You need your channel partner and your channel partner’s following the protocol and if the channel partner is not following the protocol, either you -

Audience cross talk, inaudible

Rene: This one doesn’t have to be multisig ahead of time?

Audience Member: Yes it has.

Rene: Ah yes, because otherwise I could double spend.

Audience Member: So that’s expensive?

Audience Member: No, no, no,no. (inaudible) you don't add this to the channel until a splicing transaction is confirmed.

Audience Member: So then you need to wait for the confirmation?

Audience Member: Yeah, you need to wait for the confirmation before you use it.

Audience Member: If F1 isn’t a mult-sig already, you have to track on both versions of the state, if F1 is a multi-sig so you can basically switch over to just continuing on S1

Rene: Well as soon as S is confirmed you can switch over. If that is not multi-sig at some point in time S is confirmed and then F can’t be double spent.

Audience Member speaks in audibly

Audience Member: I’m not saying this is the best protocol. We’re trying to understand why it’s actually so tough. I hope that we can talk a little bit more.

Who here follows the lightning dev mailing list?

Audience Member: Okay I stop because there’s too many mails.

Rene: I mean what you can do is I think in November last year Rusty was making a proposal for splicing protocol and when you read it, it's actually really hard to figure out if he was using a mechanism like this or like this because all he was talking about was the channel protocol. Like what kind of revocation keys are we sending back and forth? Are we triggering splicing? How do we move the funding transaction? right because in this scenario what you have to do and gossip you have with gossip to tell them hey by the way this is my new funding transaction at some point in time. Once the splicing is locked in, gossip has to know that this is actually now the-

Audience Member: So there's this transition period where we see F being good being spent and therefore the channel is closing but not really because we are transitioning to s so there is a grace period where you don't close it….

Rene: Remember what I told you about gossip. Gossip doesn't have this close channel message: a channel is closed in gossip if you see the funding transaction is spent on chain. So the channel disappears right? It’s operational but it disappears.

Audience Member Speaks

Rene: You see as in the mempool, which kind of signals that F is spent but you don't have a block height yet, because you don’t know when it’s being mined. You can't announce this on gossip because on gossip you need a block height.

Audience Member: Also we don't allow channel announcements if the funding transaction doesn't have at least six confirmations. So for the rest of the world the channel would look inactive for six blocks at least.

Audience Member speaks

Audience Member: So we would have to pre-announce, hey by the way I support splicing protocol in advance

Rene: Preannounce over gossip to everyone.

Audience member: We might see this flicker on and off again.

Audience Member: Why not change the gossip channel announcement so it looks like sort of a transaction that has an input and the output is the channel ID? You know what I’m saying? You could easily make it where a channel has more than one funding transaction.

Rene: So here's the thing, you can easily make a lot of things.

Audience Member: I don’t want to say easily, but somehow this looks simpler to me, code wise.

Audience Member: The left one is really cool because you are actually not closing the channel.

Audience Member: All you need to do is change the gossip so that it will accept the channel with two funding transactions.

Audience Member cross talk

Rene: I’m leaving (laughs)

Audience Member: Oh right, the left one doesn’t allow splice out. That’s difficult.

Rene: We can only splice it this way.

Audience Member: Wait, how does splice out look?

Rene: Wait a second.

Audience Member: I just want to say everywhere where we rely on one output leads us to checking that we are correct on chain…

Rene: So that's basically my answer to we can do a lot of stuff. Depending on what we do it has severe consequences along a lot of other stuff on the protocol and that was for me a thing that I needed to learn over half a year, for a long time. because I was just drawing these pictures and being like, hey I solved splicing, why was it so difficult for the lightning devs to do it.

Audience Member: Try mixing in the backwards compatibility with nodes that might or might not have upgraded yet and it’s really weird.

Rene: So yes we couldn't talk a little bit more about splicing out. How this might look like but my feeling is that the main point that I want to transport you it was successfully transported and the fun thing however is this that my feeling is in this group there's many people know who understand the difficulties of protocol development, who can actually walk through the proposals, actually really like make suggestions, like really see on which parts of the protocol are being impacted and why are they being impacted and what should we keep in mind. The more eyes you have on something, the better it is, I say.

Audience Member: I have a question for the left side. If you force close and you have multiple funding transaction can you….inaudible

Rene: No the funding transaction is always on chain.

Audience Member: When you force close it, when you go to chain, you would spend from both outputs?

Audience Member: Yes. The commitment transaction is a single transaction that is confirmed or not and it’s going to spend both outputs.

Rene: But you have to say a little more stuff because let’s assume someone makes a (inaudible) and spends this one, now you can’t do penalty with some of theirs, so you really need to remember that. But that’s the point, stuff gets ugly.

I promise to make 15 minutes about splicing and maybe we can be on time.

Audience Cross Talk

Rene: Just think about gossip and all these things right at the entire channel protocol. I mean before you only like you know you have different states that know - I mean it's just like these kinds of questions that arise.

I think that's really the spirit that people should have been looking at these problems. So anyway I would pass over to the next person, hope that this was enlightening.

Audience Member: Yeah part here is there are no dumb ideas just because we went down one rabbit hole doesn't mean that they're simpler version stuff you guys might come up with so tell us if we're being stupid about these things.
