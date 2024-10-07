---
title: Lightning Specification Meeting - Agenda 0936
transcript_by: Michael Folkson
tags:
  - lightning
date: 2021-11-22
---
Name: Lightning specification call

Topic: Agenda below

Location: Google Meet

Video: No video posted online

Agenda: <https://github.com/lightning/bolts/issues/936>

The conversation has been anonymized by default to protect the identities of the participants. Those who have given permission for their comments to be attributed are attributed. If you were a participant and would like your comments to be attributed please get in touch.

# BOLT 7 onion message support

<https://github.com/lightning/bolts/pull/759>

So PR 759 is built on PR 765 because we used the route blinding to decrypt where the end is going to go. After feedback from Matt I think we have a pretty good, close to final on onion message support. The original onion message was basically exactly the same as we do for HTLCs. The only difference is that it could be variable size. You unwrap the onion, figure where it is going next and send it onwards. The endpoint would have some extra fields to contain the data. That’s still the case but now it is always a blinded onion. When you unwrap it you get this second layer of encryption and then you decrypt that. The reason for that is that we were using that for onion replies. I send you an onion message and I include this route blinding path that you can drop into the onion to get the reply back to me. But that made it asymmetric and you could tell the difference between someone sending you the onion message and sending the onion reply. We went “No that’s it. It is always blinded even when that is gratuitous.” There is no particular reason to blind a message if you know exactly where it is going. But it does make them uniform. Basically route blinding is now compulsory in an onion message. But it is pretty straightforward. It is exactly the same onion format we use in HTLCs, you pull it apart. I have test vectors, Thomas H of ACINQ has been working his way through them. He found some bugs in my test vectors that basically work but I’ve had some cut and paste errors that I have to get back to. He has got interoperability between c-lightning and eclair on a slightly previous revision of onion messages. We tweaked the spec in a couple of small ways for the final version. The message number is now 513, it was previously in the gossip range and everyone objected to that, it was obviously not a gossip message. Now it is 513 which is undefined range. You can ignore it because it is odd. There were a couple of fields that were unified when t-bast did the route blinding stuff that will be the same as the ones we want to use in route blinded HTLCs. There were some minor field renumberings that don’t affect anyone except c-lightning, c-lightning now has to do both. I’ve implemented that and I think we are very close to finalizing on the two implementations there. I’m hoping that will happen this week. I would really like Matt to get back and reproduce that so we’ve got a three way compatibility test for at least that part. That is all looking really good. Hopefully that won’t change again. Obviously that leads us into offers which is the next bikeshedding thing on top of onion messages. I am hoping once we’ve formal interoperability of the slightly tweaked spec we can have our two implementation bake off test and all the test vectors complete. Definitely by next meeting we should have both implementations 100 percent I hope.

I am pretty sure we will have by the next meeting complete interoperability between eclair and c-lightning. If people have time to review the PRs and find things that look odd. Maybe on the route blinding one, by specifying the route blinding for payments, it was mostly useful for onion messages as well. Right now there is the real spec part that updates the BOLT and only adds the things that are necessary to the onion message and the low level utilities for route blinding. I also have a separate [document](https://github.com/lightning/bolts/pull/765) that is a proposal format with more details and documents and more brainstorming kind of things around payments. I am not sure that should be merged initially so let me know if there are parts to remove in the first version that we will add when we actually use route blinding for payments. That may make sense.

c-lightning has support in experimental mode for an earlier version of the route blinding for payments too. It is pretty trivial. It needs to be updated for the modern spec. It is really easy. The only thing that we do not support in onion messages is route blinding direction by short channel ID because I simply haven’t implemented it yet, there is a FIXME. You can either specify the next hop by short channel ID or by full node ID. I do not yet support short channel ID but I will fix that before the next release. I originally ripped it out but t-bast put it back because it makes more sense for payments anyway. It is nicer, it is more compact, you use less space in the onion. For payments where the onion is a fixed size that is perhaps more critical.

It sounds like both route blinding and onion messages, we might have some level of interoperability between c-lightning and eclair by the next meeting?

Yeah we had it then we tweaked it. We both broke it in the same way.

It is Thanksgiving week here in the US so you’re probably not going to get a lot of work out of the rest of us.

One more question about the onion messages. We’ve had a discussion on Twitter and so on and I am still surprised that none of you seem to be very concerned about abuse of these onion messages. You can route them in 27 hops all across the network, it seems like we are stepping over that as easy as we did with the HTLCs and replicate the same problem in onion messages. I know they are lightweight etc but isn’t there the endgame here that no one wants to forward onion messages and you can only connect directly. You have no privacy gain because of that. You might as well have not done onion messages.

I am concerned as well.

There are a few things we can do with onion messages that we can’t do necessarily with HTLCs. Maybe we can approximate the failure modes of HTLCs. One obvious thing that I think Rusty has mentioned before is the ability to tell a peer “You are sending me too many onion messages. Shut up or slow down.” That peer doesn’t just blindly drop onion messages based on a flow rate to that next peer who told them to slow down but actually can do it based on the previous hop. That peer who gets told “Slow down”, they can look at their inbound onion message flows and say “The source of all these onion messages is that peer. I am going to rate limit him and I am going to tell him to slow down.” You can do a backwards flowing rate limiting or flow control there. A little bit naive flow control but does let you rate limit someone and then tell them to do it based on source. If you are rate limiting based on source and it flows backwards…

The trick is you do it without state. What happens if you are being flooded then next time you go into the thing that you have to rate limit, you tell the source to rate limit it. You are going to hit the path that is flooding you most. If someone is flooding down one path that will get it. If someone floods the entire network, sure.

The answer to flooding the whole network is you stop accepting onion messages for forwarding except from someone you have a channel with. Now you can’t necessarily flood everything.

Would that really address things though? It seems like rate limiting is a requirement and the existence of that destroys quality of service. You don’t really have any guarantees. It is even more unreliable as a messaging thing. Maybe that is ok for certain things.

Yes, the internet works by doing retransmissions.

The Tor network.

Tor has centralized rate limiting. We can do that too but then we’re biting off a pretty big challenge there.

Tor does not have centralized rate limiting.

What do you mean? The directory authorities.

Tor has centralized selection of pseudo honest nodes but anyone can connect and start flooding the Tor network. They don’t have centralized rate limiting.

<https://blog.torproject.org/research-problem-adaptive-throttling-tor-clients-entry-guards/>

It is closed membership in a sense.

Not on the client side though.

Sure. All I’m getting at is that it seems like we are trying to replicate the Tor network, or a subset, it just seems that’s a lot to bite off basically. Maybe we’ll get there when we get there. We’d just end up with VPNs over Lightning. That sounds cool, I thought that was cool a few years ago, I did talks and stuff but now I’m more wary of it.

The point is that yes you have to rate limit, if someone tries to spam you with 100MB a second of onion messages you will rate limit them and tell them to shut up. But if you could flow that flow control back to the source then you’re not as strictly impacting the quality of service for others. You can actually push the flow control back through honest nodes to the border where you have some node…

There is no sybil resistance here because the attacker could just create another ID. If we are not rate limiting people who don’t have a channel, creating new node IDs and just sending anonymous messages is really easy. That goes back to accepting onion messages from people who have channels. Another thing that I wanted to mention is we need to think about what is the degraded. In most cases that we want to use onion messages for the degradation of service when you just drop the onion messages would just mean that you may be losing privacy by having to connect directly, one hop through your ISP instead of a longer route, but that is probably acceptable in most cases right?

The streaming movies thing is kind of interesting. It depends how our rate limiting is. If our rate limiting is relatively aggressive…. You basically want one message back and forth generally, You are very low actual requirements. Your rate limiting can be fairly aggressive. It will be interesting to see if we see massive amounts of abuse. We’ve seen some HTLC abuse.

It seems like botnets are going to love this thing.

Botnets can use HTLCs though, they can use failed HTLCs for confs and we haven’t seen that yet.

Botnets do use Tor, they use all kinds of other stuff.

I understand that. It just seems like to me we are just adopting this other network type due to necessity. I am just afraid what happens in future.

If you require a channel no botnet is going to use this because no botnet is going to open a channel at each endpoint of the botnet.

I like your monetization strategy, that’s awesome.

I’m just caught on the arbitrary data thing. The implications of that, whether it is things that we like or we don’t like, what people can use it for in the future, the tension that can draw. I understand it is super useful for other stuff but I’m just worried about the tail end of it. Maybe it is not going to happen.

I think we’ve built that already unfortunately. HTLCs built that already.

Onion messages are no more or less s\*\*\*\*y. The only difference with an onion message assuming proper rate limiting like we described is you have to pay maybe a 100 msat fee or 1 sat fee. That is the only difference. And you get much smarter rate limiting for onion messages because you can push the rate limiting back towards the sender.

I’m not very optimistic, I guess we’ll see where it goes. I guess people will handle it when we get Wireguard over Lightning. That sounds cool.

I do anticipate at some point that we will see people paying for HORNET. There are definitely going to be LSPs, people who run Lightning nodes and are quite happy to sell you bandwidth. I expect that this rate limiting will become too aggressive for that kind of usage. It will be interesting to see where people set the rate limits.

Have people implemented the rate limiting today or just hypothesizing how it could be done in the future?

No we are handwaving, I haven’t rate limited. There is a FIXME in the code, you should rate limit here.

I assume before shipping people will have naive rate limiting. The previous discussion of being able to tell the peer to shut up and slow down is something that would need to be spec’ed in the future.

Payment flow control and data flow control, I don’t know. It seems like a lot but that’s just me maybe.

At least data flow control is easy.

But it is something else entirely.

Who do you rate limit if you get your limit on two paths? You send to both, you go “I’m rate limiting you by the way.” When it goes in the outgoing you’d go “That’s rate limited. I am going to push back and say by the way you’re rate limited.” And that flows back indefinitely. In effect yes you’d end up degrading the entire network down to your rate limit but that’s a feature if you are flooding the entire network.” The question of can I jam an uninvolved party at very small cost, you can jam in the sense that you can send them lots of traffic and they can start rate limiting traffic. That’s way, way better than them jamming your HTLCs where they jam your ability to make payments. This is the OP_RETURN argument. It is far worse for them to spam you with HTLCs so you provide them with this low overhead method of sending stuff so they don’t do the worst thing.

I guess we’ll see how it develops.

I don’t think we’re making any progress here so we should move on.

# Add payment metadata to payment request

<https://github.com/lightning/bolts/pull/912>

PR 912, the current state, it looks like there are a few updates. Christian posted an update 42 minutes ago, Christian is doing the normal thing of contributing to the spec on meeting day, thanks Christian.

It is just a minor formatting…

There is some formatting discussions on the thing, I think I had a similar formatting discussion comment. It looks like there is one implementation from the eclair folks, t-bast had something.

LND also has send and receive in a PR.

It looks like it is just pending resolution of some spec update comments that can happen on GitHub and then cross implementation tests. Are there any comments that need higher bandwidth discussion that should come up now? Or can we resolve everything on GitHub?

It is interesting that LDK is doing this already, just with the payment secret but there is an immediate use for this, that is quite nice.

Yeah it turns out on the LDK end we don’t need a whole lot of data so we are just going to do this today with the payment secret. We don’t need more data.

If you want to do just in time insertion of invoices and just replicate the invoice as if you already had it in the database then inside that payment metadata you need to put all the fields that were used to create the invoice, the invoice you didn’t store, so you can recreate it when the payment actually comes in. How is this going to work out? Is every implementation going to…

On the LDK end we are not talking about doing that. LDK splits the responsibilities there. We handle authenticating the payment which is the standard payment secret concept and then we let the user deal with storing actual concrete metadata. Description and all that kind of stuff. We anticipate with our change that users will still actually store data about the payment in their own local database but that is outside of the scope of LDK. LDK will generate payment secrets such that we can authenticate the payment by amount and authenticate it with the sender. We don’t actually do anything else, that is not our job.

If you want to take that one step further and you also don’t want to have this user database, that is possible as well with this. Everything in the metadata, you can just insert it on the fly. It is very stateless, it is also very cheap. You can generate as many invoices as you want. If they don’t pay they don’t take up any space. There is no expiration. Will something be standardized or will a loose standard emerge on how to do this? Maybe if we copy over…

Something, something bLIP or SPARK, whatever people want to call it.

I think it depends on what the emergent use cases will be. Maybe it is going to take an initial iteration but it is non-binding which is cool.

Maybe in hindsight we should have made the payment secret of variable length. Now at least we are forcing to be some kind of random number so maybe it is safer.

It should be variable size. That is something I regret.

We did discuss it at some point but then we said it is too dangerous, people will use one byte and then it is not secret anymore, something like that.

# Advertize compression algorithms in init

<https://github.com/lightning/bolts/pull/825>

t-bast and I were communicated a little bit about doing some cross implementation tests. I have a testnet node with this up, I think t-bast has too but I was too lazy to setup my testnet to support Tor. It does need a rebase and it looks like Vincenzo has some comments on GitHub which should be resolved on GitHub. Is there anything that needs high bandwidth discussion and should be discussed here? Ok, follow up on GitHub, we will introduce some cross implementation tests on that soon as well.

# Dynamic DNS support in gossip messages

<https://github.com/lightning/bolts/pull/911>

<https://github.com/lightning/bolts/pull/917>

Next we’ve got these two PRs for gossip addresses, DNS hostname and to tell your peer what IPs you have when you connect. Are there implementations of this? Or is it still just theoretical?

The IP one, there is a c-lightning and eclair implementation but last I tested I don’t remember, I think I sent some comments to m-schmoock because there were issues that I found in the c-lightning implementation. I don’t know if that has been fixed since then.

It is still a pull request, we haven’t merged it yet. Unfortunately Michael is not on the call. It is still a work in progress as I understand it but the spec seems pretty straightforward.

Sounds like c-lightning and ACINQ are working on cross implementation testing and nothing worth discussing here.

# BOLT 2 and BOLT 9: introduce feature bit to gate new channel_type feature

<https://github.com/lightning/bolts/pull/906>

We shipped something that messed up, PR 906 basically, this is the feature bit one. I think we all interpret the presence of the feature bit and sending the value slightly differently. In a way that works sometimes and doesn’t work other times. I am getting some reports, I think y’all always require the channel type to set if the feature bits are there right? You respond with one even if we didn’t send one? I just want to make sure that is the fix.

We always spawn with one because it is an odd TLV even if you didn’t set the bit or didn’t send anything, we are going to respond with something.

But what are you going to respond with if I didn’t send anything?

What we are going to use, what will automatically picked up by the normal feature bit negotiation.

I see. You are sending the implicit one even if I didn’t send one?

Yeah exactly.

I think we don’t like that because we didn’t choose anything and we exit out there.

We figured it is just making it explicit something that was implicit. The other side can just ignore so I thought it was a win. It was less code because we just send it all the time.

If you didn’t advertise this feature bit you should be ignoring.

c-lightning does that as well too right? Ok we can fix that.

There is also a comment on the PR 906. Right now you don’t ignore obviously if you receive a channel type even though the feature bit is not set, the feature bit doesn’t exist yet because the PR is not merged. The PR currently says that you should ignore the channel type if the feature bit was not set. I commented and t-bast seems to agree that you should continue to optionally interpret the TLV whether the feature bit is set or not. In part because nodes do this today.

Don’t feature bits gate inclusion of a TLV? If you are setting the TLV and I have the feature bit I wouldn’t read it right?

You can read it if you want. It is there. It is used today, that is what the spec says today. I know LDK does that, I don’t know what other people do. We send the TLV and we interpret the TLV whether there is a feature bit or not.

Interesting. We’ll parse it but we’ll ignore it. That seems like a different requirement. We’ll only look at it if the feature bit is set.

If you want to not send a channel type in response then that would be fine too. My proposed change here is we’ll send it, we’ll parse it if we receive it, we don’t care about the feature bit. And we’ll also eventually now set the feature bit. But if you want to ignore the field because we didn’t set the feature bit, you are talking to a current version of LDK, not a future version, then that’s fine as long as you don’t respond with a channel type in the accept channel message. We’ll just say “Clearly they didn’t understand it and that’s fine”.

I’ll need to go back and read the original PR.

I see what you are saying. But if it is present in both messages and we only send it if it was present…

The problem is what you are suggesting is a change from the current spec. The current spec says you should just send it and if you receive it you should parse it. If you understand it and you parse it you should respond with something in the accept channel message.

Currently it is gated on both sides.

It is making it slightly tighter yeah.

If we had done it the right way, if we’d put a feature bit in the first place then it is pretty easy. Set the feature bit and send it. If you don’t set the feature bit don’t send it. And then it is very easy. But we didn’t do that. Now it is kind of implied, if you sent it that means you wanted me to use it. If we both send it then we’re using it. If we didn’t both send it then we’re not using it at all.

I think it is compatible with the behavior in that if I’m sending the bit I’m going to send it. I can remove that to make that looser but I think it is compatible with our behavior of we only send it if we send a bit.

The proposed change makes existing implementations do something that they must not do.

They won’t set the bit but they will send it.

They won’t set the bit and they will send it. The proposed change makes that something you are not supposed to do.

I can fix that super easily. I think I found the source of that other bug. I think there is another one with eclair but I’ll message you about that t-bast. Then we can hopefully do the part release.

I need to reread the full text but my intuition is that it would still be the case whether the feature bit is set or not, if one node sends the TLV and the other node sends back the TLV in the accept channel then you’re using the TLV whether the feature bit is set or not. If a node wants to gate responding with the TLV on the feature bit they can do that, that’s totally fine. But if both TLVs are there you are using them whether the feature bit is set or not.

I see what you are saying. We arrived at that conclusion to set the bit differently but you’re right. If both people set the type we’re using it.

I just wanted to make sure, that would be the current behavior.

After this gets merged and everyone has updated then everyone will set the feature and everyone will send the thing. It is a future point if you didn’t set the feature you wouldn’t send the thing.

I think that’s the other error that we are seeing here. Interoperability testing will figure it out.

# Simple turbo channels enablement

<https://github.com/lightning/bolts/pull/910>

Turbo channels, PR 910, are there implementations of this? We’re working on it, we’re getting there.

I think Eugene has one now that he has tested. I think there are just questions on chantype stuff. We are talking about zero conf.

My only concern was there is no chantype for zero conf explicitly. I left a comment.

Zero conf isn’t a different channel construction, it is not really something you have to remember. Originally channel types were stuff you had to remember. “This is a static remote key” or stuff that was obviously persisting across the channel. There is one thing however you have to remember. If this is a private channel and you don’t want them to route by the short channel ID… Let me pull up the PR, I should mention turbo in the title then I could find more easily. I think the last commit may have added this, there is a pile of 8 fixes. Now there is a channel type but that channel type means don’t you dare route by short channel ID. That’s cool and the reason that is cool is because when we have channel type upgrade, which is another PR, you can take the existing private channel and then go “From now on no longer route via short channel ID. We are going to use the alias thing now.” For a normal channel you can route by both. I can give you an alias and you can use either. But obviously for an unannounced channel in the ideal world you would never route by short channel ID to avoid probing. You can’t do that today because it breaks back compatibility. You don’t know when the other side is ready. They have got to be handing out aliases in their invoices and stuff like that. By adding a short channel ID just for the private case that gives you that feature that you want.

I saw the recent change. I was mostly referring to if I start a channel flow and I have the feature bit and they have the feature bit, they want zero conf. When the acceptor sends accept channel it is kind of like “I hope you open a zero conf channel to me. I hope you send `funding_locked`.” In the spec currently if a `funding_created` is sent back then the initiator agrees to open a zero conf channel, a promise almost. The current wording is very open ended I think.

We should make it clear that if you offer this ability and you are funding the channel then you should do zero conf. You’ve got nothing to lose, I trust myself so I will zero conf for you. Whether you accept it or not is obviously beyond my control. You might decide to delay for some confs. But the opener should always send, I’ll check the wording. The idea is to prefer this model of opening in future. If you advertise this you will aggressively send `funding_locked` before it is really locked. I will check the wording to make sure that is explicit enough.

His point is he preferred to be more explicit. Y’all are saying they don’t have to send it. We’d like to make that explicit.

There are two things here. One is do I trust you? There is a whole trust question. Am I prepared to let you open a zero conf channel and route stuff and accept payments and everything else? I am not quite clear how you would do that, that decision may come later.

That decision is entirely out of band basically. It almost doesn’t need to be in the protocol because do I trust you is a question that is going to be decided entirely out of band via some mechanism of either talking to someone if it is a regular node or some LSP, whatever that system is. It being in the protocol doesn’t seem to add very much because they already know who they are talking to, they already have some special protocol.

You’ll start bouncing HTLCs off.

Does that mean you can’t signal it within the protocol? Otherwise every party opening a channel with me if I have the feature bit set is somehow assuming that I may send it. Versus if I am opening a channel outbound and I don’t set the bit they know we are not doing zero conf. To me it is about the explicit versus implicit type of thing. Do we implicitly know because I don’t know who Matt actually is in real life that we are not doing zero conf? Or can I set in my message “Hey we are doing a zero conf”.

It seems like you are trying to interpret the bit in a way that the bit doesn’t mean. The bit does not mean zero conf. That’s not what the bit means.

I think the difference is that y’all are interpreting it as behavior while we’re thinking of it as a channel type. If we can add logic to validate that channel type and let users explicitly open that channel type. Y’all are saying “I have the bit set. I might send it, I might not”.

I think the UX will be other way round. Matt opens a channel with me and then he pings me and goes “You don’t trust my node yet, I can’t route through you” and I go “Cool, I am going to flip that on”. There is no way to change the channel type after we’ve negotiated it. It depends how your controls are going to work. If beforehand you are going to have a vetted list of nodes that you trust then when we’re talking obviously in the protocol I could say “By the way I am perfectly happy to open this zero conf with you”. When you open a channel with me I go “Yeah I trust you” and you know. But I don’t know how that would extend to the case where after you’ve opened the channel with me I decide that I trust you and I’m going to do the thing.

We’re talking about two different feature bits here. Y’all have the option SID but we’re thinking of another funding level bit basically.

Yes. You are proposing adding another feature bit.

I was talking about a channel type.

Which is a bit in this case with the way that it is set up.

It would technically be the same.

Was your suggestion that if `funding_created` is sent back in response to `min_depth=0` that the initiator promises to open a zero conf?

You shouldn’t be promising to open a zero conf in the spec.

If you set `min_depth` as zero then you’re saying you’re good. At the moment the opener says “I want to open this channel” and the acceptor says “Here’s my min depth” and usually that is 3 or whatever. If I trust you I would set that to zero and it says that in the spec. Set that to zero implying that I’m ready to go whenever, as fast as the message can get through I will trust your channel. We do have a flag explicitly in the protocol, a way of saying “I trust you”. On the other side we are saying you should always open zero conf. If you are the one doing the opening you should `funding_locked` aggressively immediately because you are signaling that you are all good. It is the receiver side, the acceptor side, in that case we do have a method of you saying “Yes I want this to be a zero conf channel”. Now we could also put it in a channel type somewhere but what I am saying is I think in a lot of use cases it is going to posthoc. After you’ve opened the channel you will suddenly decide that you want it to be zero conf. There’s no really good way of doing that. The way to do that is you actually send the `funding_locked` early. You might have set `min_depth` as 3 but that is a hint.

Two things, we have something in mind basically where we’ll know ahead of time, not the after the fact thing. It seems like the flow is different, you are thinking about it differently. Right now the acceptor sends `min_depth` meaning the initiator can’t say “Let’s open a zero conf”. The acceptor says “I’m going to make it zero conf”. I think that is the control flow we want to flip basically. To allow the initiator to say “I’m going with zero conf” which also lets the acceptor assert that this is going to be zero conf and they’ve opted into it as well.

In the future the sender will always open zero conf, always. Every channel will be zero conf, everyone will be zero conf. There is no non zero conf anymore. “Here’s the feature, I support zero conf”.

Moving to full RBF in v24, full RBF and zero conf everywhere don’t really go together super great.

For channel v2 stuff?

Bitcoin Core is planning to ship in v24 full RBF, so every transaction is RBFable. Rusty’s point is that the initiator knows that they are not going to RBF and that’s totally on the initiator’s side. The receiver is the one who has to decide do I trust you to not RBF or do I set it at some `min_conf`.

It just feels like the control flow should be flipped. Let’s say I’m opening a zero conf with Rusty and he doesn’t like me. I send `open` with chantype zero conf or the bit, whatever else, and he sends me the `reject` and now we know. There is no ambiguity of “I opened it. I want a zero conf. Is he going to go first?” I think we’re trying to eliminate the ambiguity. The initiator says “We’re doing it” and then they deny immediately. Otherwise you are in some limbo. Are they going to send it or are they not? “I guess they didn’t send it, too bad”. We think with the protocol we have in mind not having this explicit thing in there makes it hard to reason about what is going to happen. I feel like we have different use cases in mind. You are thinking “After the fact we decide to make it zero conf” while we’re thinking “We are setup to do a zero conf channel”.

You are not going to accept zero conf from anyone.

Yes, which is why you’ll send the `reject` message.

The point is no one is going to say “I accept this from everyone” and so there is always going to be some out of band negotiation.

You are assuming a lot about how that negotiation will take place. Rusty is assuming that the negotiation will take place after we already opened the channel…

No I wanted to allow that.

I am just assuming there will be a negotiation. There doesn’t need to be anything in the protocol at that point. There is implicitly.

If people are doing it like that today, we are trying to add something in the protocol.

You can’t get away from that. You can add as much as you want to the protocol, there will still be some kind of out of band negotiation to say “Hey can you mark my node as trusted so I can open a zero conf channel with you”. At that point I don’t need it in the protocol.

Sure, but right now what doesn’t exist direct feedback or explicit acknowledgement of that relationship within the protocol.

There is, if they reply with `min_depth=0` that means they have accepted that they are ready to go with a zero conf channel. But it is not in the channel type.

It is basically a delayed three way handshake. I send it, you send something… versus me just sending it.

No you send that at the same time you send the channel type, it is literally in the same package I think.

But the responder sends `min_depth`.

They would also send the channel type.

The difference is me the initiator, I can’t initiate a zero conf and then have you accept or deny it. You denying it is basically you sending the error message or the warning.

But it is the same message flow.

It is not the same message flow.

The difference is that instead of the acceptor failing it you would then fail it. The opener would then reject and go “No you didn’t put a zero min_depth so I’m not going to open this with you”. Is there a case where you would want to not fallback to a non-zero?

Yes. We have a specific use case. If it is not zero conf we’re not doing it because we wanted zero conf as the initiator.

But you don’t need a feature bit for that either. What you are saying is you want a feature bit so that instead of an `accept_channel` message the receiver immediately sends an error message. You don’t necessarily need to do that immediately, they can send that `accept_channel` and then the initiator can send back an error instead of moving forward.

You want them to send an accept and an error?

No, not the receiver. The receiver sends the accept and the initiator says “Whoa, that funding_locked is not zero, I don’t want to do this”, sends an error, closes the channel and moves on. You don’t need a new feature bit to do that. You can accomplish that by just sending an error message.

It is a different way of doing it. Philosophically maybe I’m the odd one, I like things to be explicit on the protocol level.

The only thing I dislike about the channel type is that the channel type is persistent across the channel. In the long term it doesn’t matter whether it was zero conf. It is a weird thing to put in the channel type. Using the message depth to indicate whether you are accepting zero conf or not…

You could delete the bit, you could keep it in memory, I don’t know.

What do you think about the fact also that even if I tell you it is zero I can switch all my `funding_locked` and make it non-zero afterwards. You’re not going to close that channel on me because we just went through the trouble of opening it.

You can always accept the open and then refuse to route or accept any HTLCs too.

I feel like you can do a bunch of things. We are just trying to make things explicit for the computers and they know what we’re doing. We have to handle all the extraneous cases where you do some random thing because you are buggy still. We are literally talking about a bit. You already store the bit.

It has to be another one because I stole this feature bit to mean something else. I stole the feature bit to mean don’t route into the channel type already.

There are two different things. We are just talking about making the negotiation explicit basically. We can write down this flow as well to make it more clear.

We are all on the same page, I just don’t buy that that is more explicit. I totally understand what you are saying. I don’t buy that that is materially more explicit. Users don’t see “Channel closed with reason channel failed to open because you didn’t accept zero conf”. At the end of the day the user experience is still you see the same error message and the same failure reason.

You are assuming a lot about how negotiation will work in general, how out of bounds stuff will work in general.

The spec explicitly says if you trust them you should set the depth to zero. If they don’t do that you go “You don’t trust me so I’m going to close the channel. I’m not going to continue opening.” We already have a flag, it is just that it is not in the channel type. If you put it in the channel type the failure is faster.

It fails faster by one packet.

Yes. That’s lovely. Why do we have TCP Fast Open? It is one more round trip.

On the downside this would be worse for us because we will open everything zero conf and we want to fallback. We will have to reopen, “That’s right, you didn’t accept the zero conf channel type.” Every time we would have to try again with the non-zero conf variant of the channel type. It is a lot more work for everyone else.

You seem to be living in a universe where everything is zero conf everywhere. We’re like “It is going to be zero conf if both sides cross the t or sign here basically”. I think we are looking at it differently in that regard as well.

We will be offering zero conf to everyone.

And we wouldn’t. We’d only do it under very specific situations.

Why?

Or one side setting it explicitly.

The receiver can always immediately send a `funding_locked`. Now you’re sitting on your `funding_locked` for no reason.

We wouldn’t do anything because we didn’t set the bit. This is just constraining the paths of the software and what we expect. It seems like people at least acknowledge that there’s a condition where maybe you want the initiator to be able to specify this upfront. And it fails faster. At least we have those two acknowledgements. We won’t be setting zero conf for everything once this is in as well too.

We will. So we definitely do not want your dance where you have to reconnect and offer a different channel type. That is why. It is a lot more logic for us to change this.

It is still implementation phase.

More code in exchange for half a RTT, faster failure does not seem like it is…

You’re trivializing the implicit versus explicit thing. More code is super relative.

It is still explicit. There is still an error message, it is still incredibly explicit. If you interpret the bytes on the wire in the way described in the spec it is equally explicit in both cases.

Comment: Making the “we always open zero conf” much harder in exchange for a tiny speed improvement for those that don’t should make the `channel_type` undesirable. 1/2 RTT in exchange for 4 RTT for a reconnect.

Are you really going to do everything zero conf after this?

Why not?

You can’t really do that with 2 player channels. Anything that uses an interactive protocol, you start getting into trouble.

That is unspec-ed so far. We need to figure that out. Once the other party is putting funds in you cannot default to zero conf without a trust relationship. But in this case of simple open this is very simple. One side has nothing to lose by offering zero conf. In the case of simple open that is the funder.

If I said on Reddit every channel is now zero conf people will be like what?

On the initiator side I agree that the initiator has an incentive to always say zero conf. If he’s the only one putting funds in the channel on the receiver side I agree that we would choose depending on other conditions. But on the initiator side I don’t see why we would not do zero conf all the time.

The initiator might not just auto do zero conf because the market may price that default risk? If you have no marginal cost then you would but if there is a market premium for that service from an acceptor…

Again that negotiation happens out of band. If you have an out of band price for accepting a zero conf then presumably that will be you have to set at least a `push_msat` of x in order for me to accept your zero conf. But if I just request a zero conf and set a `push_msat` below that you simply won’t accept it and that’s fine. You still do it at the protocol level because why not?

I guess we just have different ways of looking at this risk, the feature itself and negotiation.

What risk?

I just want to make it explicit. I want to make sure that both sides are double opting in to this zero conf type thing. I send the feature bit, you decline. It is fast close. It does get in the way of this every zero conf thing. I don’t know if that is a good idea. Maybe that is just simpler, to do zero conf all day, every day.

Way simpler.

Even from our perspective after implementing this code, is it just gating this new behavior?

Even if we don’t go there zero conf for everything having the ability to open a zero conf without having to first check with the node whether they would accept it is something that we need to have. If we end up aborting a fund channel because our counterparty did not accept the zero conf then we have to reconnect, that’s way more code than the optimization we gain from closing half a roundtrip earlier.

Yeah we won’t be doing that, that is dumb.

We won’t be doing zero conf all day everyday.

Why would you possibly not offer this?

Because we want to make it explicit to the users.

In the current spec you can choose to not opt in.

The difference is y’all won’t be able to open it up and then find out after the fact if they accept it. From the receiver standpoint.

You do it by error, we do it by examining a field. It is the same thing.

I want to be able to open up a channel without knowing if the relationship exists already. I find out once they get the open.

We want to try to open a zero conf channel. Our counterparty says “No go away”. We have to reconnect, remember across these connections that they didn’t accept it and retry without zero conf. That is way harder than just saying “Can we try opening a zero conf?” and the other side then says “I don’t want to” and we are still good. We can’t do better than falling back into a non-zero conf channel after trying a zero conf channel.

If we really wanted to do zero conf when they return with `min_depth` not equal zero we go “No sorry you are not zero conf enough for us. We only like zero conf things. We want people to trust us or whatever.” We send an error at that point. I cannot imagine that it is priced except in a negative sense. c-lightning always offers zero conf and I can use it if I want and lnd doesn’t.

Do you all agree that the acceptor is the person taking on risk?

Yes.

So they decide.

So why not let them be explicit with that?

We are by setting `min_depth`.

They say “Here’s my min_depth, it is not zero”. That is how they are telling you explicitly whether they are going to zero conf or not.

Y’all are saying this lets me open up a channel and not know if they support it yet and they tell me later. Versus me just saying “I want to open the channel” and they say “No”. That’s the difference.

Right because this is way simpler. You can offer it to everyone and they can accept or not on their own terms. You don’t have to do this dance where you go “I insist on a zero conf channel even though I don’t care either way because it doesn’t make a difference to me, I’m opening it and I trust myself. I explicitly want to open a zero conf channel.” They go “No I don’t trust you”. Then I go back and say “Now let’s open a normal channel”. It is the dumbest protocol ever.

Do we realize that this is the type of negotiation that we put into place with the explicit channel type? Remember we had a different type before. There was this double opt in thing. We said “No you’ll just send the error and then try again”. That’s what this is. We’ll have to do that anyway for any channel type because that’s the way we decided to do negotiation.

They are different. The reason I think it makes sense for channel type to try some specific channel type, “I want this anchor thing” and you say “No”. I’m like “Ok maybe something else”. But here the reason it is different is that I really think when you actually use it if a guy says “No to zero conf” you still want to have a channel with them.

But we described a case where that’s not the case. We only want zero conf.

Then you send them an error going “No you didn’t accept my zero conf”.

You only want zero conf, it is for UX. Because otherwise the user opens it, they’re waiting and maybe the wallet promised that they can send now but they can’t because of this thing.

I don’t think the gain of gaining half a RTT is worth it in that case. You just reject and not complete the flow. They say `min_depth` is not zero.

The opener would close in that case instead of the acceptor closing.

Yeah that’s the difference.

The opener would go “No you are not zero conf enough for me. I only want channels with people who trust me” and they error out at that point. I am really looking forward to zero conf everywhere. If you trust my node then sure we’ll do zero conf and if you don’t that’s fine we’ll be normal. But you still get the other features that we want here.

The other thing, this negotiation isn’t what we all signed up for. The whole try it, reject and then try again.

No remember the original proposal was mine, it didn’t have that and everyone was like “We can do that if this ever occurs”. I went “Ok let’s make sure one of them never occurs”.

Do you remember the rationale? We were talking about how do you handle these weird feature bit combinations. I want anchors and something else that doesn’t exist. How do we handle that? Just reject instead of both sides sending their overlap and then do it again.

Do we want to try another PR? I think this gets back to the longstanding disagreement about what feature bits are for and required for.

It comes up a lot, we really view the way negotiations work differently. It seems like every time we are like “Let’s add a feature bit” there’s this massive campaign of “No feature bits are bad and we don’t want to do them. It is going to make the code more complex.” When I thought the whole point was to negotiate features.

I have a suggestion. Let’s write down on paper arguments for and against. You do that, we do that and then we do a meeting only on that so we can just have the arguments laid down beforehand and prepare a bit more.

We’ll write down that situation where it is like zero confs or bust. We are like zero confs or bust, you are like zero conf all day everyday. I think that’s the difference how we’re approaching the protocol design here. Sounds good.

On [PR 906](https://github.com/lightning/bolts/pull/906) the feature bit one, we are going to do a release super soon once we know this is there because we broke stuff unfortunately, my fault.

Ok I can test it and review it when it is ready.

