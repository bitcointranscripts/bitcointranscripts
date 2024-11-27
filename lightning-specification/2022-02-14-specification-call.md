---
title: Lightning Specification Meeting - Agenda 0957
transcript_by: Michael Folkson
tags:
  - lightning
date: 2022-02-14
---
Name: Lightning specification call

Topic: Agenda below

Location: Jitsi

Video: No video posted online

Agenda: <https://github.com/lightning/bolts/issues/957>

# Organizing a Lightning Core Dev meetup

I was talking about organizing a face to face Lightning Core Dev meetup. If I understand correctly there has only been one formal one and that was in 2019 in Australia. There has been two?

Milan, the kickoff. There has only ever been two.

That was probably before my time in Bitcoin.

We get to Bora Bora? Did that come up on the list?

I think it is high time that we meet in person. I know there was one last fall but Rusty couldn’t travel and a bunch of folks couldn’t. Let’s try to get one organized that has as good a participation as possible from the Lightning spec developers. If anyone has questions we can discus right now. I just wanted to give a heads up. I plan to send a survey out just to get some sense for locations and dates that work for folks. It will probably be impossible to accommodate everyone but I’ll do my best to take that information and find a way to get something scheduled in the next few months. I suspect it will be April, May timeframe. I am going to try to make it work, at least by May. Something that works for everyone. Are there any quick questions or things I should be thinking about when trying to organize this? I’ve organized a couple of Core Dev meetups in the past, we’ll take lessons and learnings from that. As they develop we’ll reveal plans and get feedback from everyone to make sure it is as valuable as possible.

There are a few things popping up randomly that maybe people will be at. I know some people are going to be in London, some people may be in Miami. If we can piggy back maybe that can work but London is in like 3 weeks.

I’m probably the only Lighting one but I’m not going to the UK. I know a number of Core devs aren’t going to the UK either.

Some of our people are going but they are already in Europe, it is a skip. Not a long distance.

I’m happy to go to Europe. Because of the lawsuit currently entering into the UK… At least until we finish the jurisdiction challenge.

I forgot that was happening in the background.

As these Bitcoin conferences occur, some subset of us there, let’s meet up and make progress. Work towards to this one where the majority of us can hopefully attend.

# Use warning message in quick close

<https://github.com/lightning/bolts/pull/904>

This is a one liner to use a warning. This should be easy to integrate. Another thing that we could discuss about that PR is the point Laolu raised. We could add a feature bit for that. I don’t think we need to and I think Matt doesn’t think we need to either.

If this thing can save you a bunch of chain fees maybe you want to find people that promise to always do it. That was the rationale there. Otherwise you have the fallback thing. Maybe you end up paying more because they are doing weird stuff. I started implementing this, I need to go back to my PR.

We can separately discuss having a feature bit for the quick close thing itself. But this in general is just adding an extra warning message on the wire. I don’t know why we would add a feature bit for just that.

People send warnings today. I get some issues in lnd, an unknown thing. Maybe we should add more logic in there basically. I think c-lightning sends one if you already have a channel that is closing and you try to do a new one. I think Carla has an older PR for that, we just need to revive it so we can see when things are going wrong.

I think we send them too now. It is just a new message type that you are supposed to log.

We had an older PR that was waiting for stuff to settle down but it is merged now so we could move forward with that. I’m trying to find it now.

I agree it is completely orthogonal to a feature bit so maybe have a quick look at that PR.

# Offers

<https://github.com/lightning/bolts/pull/798>

We’ve been working a lot on offers on eclair recently. It is making steady progress. I put one comment on the PR about blinded paths in the `payinfo` but apart from that I don’t think there’s much to discuss on our side.

I did the classic pre-meeting “I should do something”. I went through and applied a few changes, a few typos and things. There was a compat break that I have implemented with compat mode. We seem to be pretty close. I look forward to seeing how interop goes once you’ve got that working. There was a request from Matt. We’ve got blinded paths but we don’t have simple route hints. The problem is you can’t pay via a blinded path until we’ve got the pay via blinded path stuff. He was wanting this shim that I’m reluctant to do but it is practical. I can give you a single unblinded hop. We hold our nose and implement for now. Then eventually it will be in the wonderful unicorn, flying car days and we’ll have full blinded payments and we can get rid of it.

To be clear I am not going to agitate strongly for this. I think it would let us deploy a little quicker. Obviously we would deprecate it within a year. Then we would remove it another year. But if the answer is no I am definitely not going to advocate very strongly for this and push back. I leave it up to you.

I need to dive a bit more into that. I do not realize yet how much work I will have to do. I would be able to know more in a few weeks and then make a recommendation. Right now I suggest to keep it in until we realize that it is too much and we want to ship without it. Then we may want to remove it. I added a comment today which is potentially another breaking thing so you may want to take a look at it. It is about using a single blinded hint for the whole blinded path instead of one per hop. That is something that would change the wire requirements. We need to decide whether we want to do it or not. While I was reviewing Thomas’ PR on eclair to add offers I realized that there this thing which is a routing hint saying how much fees and CLTV delta to use for the parts of the blinded path. Thomas understood it as there must be one for every hop in every blinded path that is in the offer or the invoice. The way I understood it was we only need one per path and we should apply the same fee and CLTV for all hops in the path to hide them more. You don’t want to show there are different fees here. That is an unblinding vector and it takes up less space.

You still have to indicate the number of hops though.

Yeah. You still have to have an unencrypted blob for each of the hops. But for the fees and CLTV you just provide one value that should work for all the hops in that route. It is more lightweight in the offer and in the invoice. Especially if you add dummy hops at the end of the blinded route you don’t have to repeat new fees and CLTV expiry that takes up more space for no reason. It also forces you to have something that is uniform and works for the whole path which makes it hopefully harder to unblind.

Does that mean you have to go through all the nodes across all the different payment paths, find the one which is charging the highest fees and apply that ubiquitously to every single node?

In a way that is already what you do. When you include the path you have all the data for all these hops so you just select the highest fee instead of selecting the right fee for each of the hops.

If you are doing something smart you obfuscate those numbers. It doesn’t help a huge amount because they can still probe. We have a plan for that, that’s later. You put something inside the onion to say “Don’t accept below this fee because they are trying to use it to probe you.” It is not a break for me because I don’t write this field at the moment. We can certainly change it. It is a simplification, it makes sense. You could imagine a case where I am feeding you a blinded path where one is higher. You could argue if it is such an obvious vector then don’t put that in the blinded path, start with the blinded path after that.

Or just use the higher value for everyone. One other thing I was arguing in the route blinding PR is that it may be frightening for the sender to see that there is a high fee to pay for the blinded part of the route. But actually you could reverse that and make it be paid by the merchant. The merchant would discount the value of the real item and would actually pay for the fee of the blinded path himself because it makes sense. The merchant is trying to hide themselves so they should pay the fee for the blinded part of the route.

I buy the argument. If you are paying for liquidity you will end up with this one hop that is potentially significantly higher. But at the moment the Lightning Network is still low. I ACK that, I will write some verbiage around it. Change it to a single that applies across the route, I like it.

# Zero conf channels

Previous discussion: <https://btctranscripts.com/lightning-specification/2021-11-22-specification-call/#simple-turbo-channels-enablement>

We have a pretty comprehensive implementation of it but there was that one thing that we left, the channel type or not. Maybe here I can explain our use case or flow versus the reject on accept. For me it is a fail early versus fail after they send you a non-zero value on min depth. In our case, people like Breez are already doing zero conf channels today. If Breez is starting to use Pool to acquire a zero conf channel for onboarding, in our case we have a channel acceptor that looks at the order in Pool and says “This is not the channel type, we reject.” With this we need a channel acceptor acceptor. Whenever someone sends you an accept message you need to have that hook there. We already have a pre-accept hook versus a post-accept one. Adding the channel type here would let us know if they are actually going to do the thing. Some people commented that they could do whatever anyway but at least we have that first protection. You can say “They can do that in any case but the protocol is what we expect. The extraneous stuff can be handled on the side.” We have a full implementation. We should probably test some stuff on the side. That’s the one thing. We want a channel type so we can at least say “I want to open a zero conf channel to you”. Whereas right now this is saying “I will allow you to do zero conf after it is extended”. That is a slightly different flow.

Don’t you already have some kind of hooks on the accept channel message? There’s tonnes of fields in the accept channel message that users will presumably want to filter on?

The way we handle it, depending on how you do it, you either have a function closure that tells you what to post to the other party… Up until now there has never been a need to do anything on accept channel. Whenever someone sends you an `open_channel` message that’s when you’d say “I only want private channels. I don’t support this feature bit. They have a green alias, I don’t like that.” That is what people use pretty widely today.

You said on receiving `open_channel`? These are two different directions. You mean before you send `open_channel`?

Us and other implementations have something like a channel acceptor when you receive `open_channel`. You are saying “Do I want to accept this channel since the default things are currently one way?”

Let’s separate the conversation between outbound and inbound channels.

I’m concerned with accepting. Let’s say Breez acquired a channel for their user, a node on the network is now opening a channel to your mobile.

So it is an outbound channel?

Yes it is an outbound channel. The way it is setup, the maker is always the one that is going to be opening the channel, in this case the person who is opening the zero conf channel. Right now in our flow the user would see the `open_channel`, assuming there is a channel type and whatever else, see it is not zero conf and then reject it. Otherwise it would need to accept it and then later on have an exception down the line that they send a `min_depth` of a different value. That’s the flow.

You flipped it on us again. You are talking about the side that is accepting the channel, not the channel opener. And you want to filter on the `open_channel` message itself.

Yes. We do a similar thing. If someone wants anchor only because we have a feature bit or a channel type there, they can say “That’s not an anchor channel. I’m rejecting it” and everything moves forward like that. I don’t see a reason not to add a channel type here if it can make peering and general protocols built on top of it more explicit. We can fail quicker rather than failing later. The failing later, we would receive the `min_depth`…

You said this is for the case where a user has received an `open_channel` and then is going to make some decision based on that `open_channel` and then send a response or an `accept_channel`. But once you’ve received that `open_channel` you now have all the information. The `min_depth` is only in the `accept_channel`. Presumably the node that is opening the channel, if you tell it it is zero conf it is just going to accept that because why wouldn’t it? In my understanding of the way we’ve done it and c-lightning has spoken about implementing it just seeing the `open_channel` and knowing what you are going to write in the `accept_channel` is sufficient to know whether the channel will be zero conf.

That’s the difference. Y’all are saying zero conf all day everyday. We are saying zero conf under these very precise scenarios. It wouldn’t be a default thing for the world. I don’t see any downside and I feel like it makes certain protocols more precise because you can fail earlier. We have a lot of feature bits, we already have a channel type here too. Maybe certain channels can’t support zero conf in the future.

And multi funder is a whole other discussion.

We have the ability at the protocol level to allow that filtering to exist in the future by having the zero conf bit here.

In the case of you’ve received an `open_channel` message, you say “I’m going to do zero conf with this channel”. Presumably at that point you’ve done further out of band negotiation. Obviously you are not going to accept zero conf from anyone, you are going to say “This node, we’ve already negotiated this and that”. Why can that negotiation not be the thing that decides this instead of having it be a negotiation? First you negotiate, you know you are going to do zero conf with this node, you get a channel from that node and then you do an additional negotiation step and say “It must be zero conf”.

This is when things are extended. At that point maybe they are eligible. But in this case whenever you send it I know it is there at runtime. We always try to verify the lowest layer. Let’s say we are doing this thing and it is not in the feature bit. Then the user sends `min_depth` zero, for whatever reason other party says “No”. At that point you have a weird silent failure. Now the receiver is saying “Zero conf” rather than the proposer. If the proposer initially gets the `accept_channel` and then does nothing, UX wise it is hard to have a consistent flow there.

I don’t understand why. You’ve already negotiated it. The initiator and the acceptor has negotiated it. The acceptor says “Yes zero conf” and now the initiator is like “Actually no, not zero conf”. Then you’re saying “The UX is going to be confused.” Of course the UX is confused, the initiator is buggy.

If we have a flow here where we know the initiator is doing a weird thing from the beginning we are able to make things a lot more consistent. The way it works, we ignore them, we do matching again and we can proceed. While with this one it is a weird indeterminate thing.

The channel now has to wait for a few confirmations. So what?

But now the user’s expectation is trashed. “I thought I was getting a zero conf channel. I can’t use it at all. Is the wallet broken?”

It is the user’s fault.

It is not the user’s fault. It is the protocol not being able to surface and allow things to be explicit like this. Can you explain the cost of adding a channel type feature bit here? In the future maybe certain channel types aren’t zero conf friendly at all. We are able to add a provision for that from the get go versus in the future realizing that the `min_depth` dance isn’t sufficient for whatever new super Taproot covenant channel type people come up with.

I am just trying to understand exactly the differences here in terms of the flow.

The UX is inconsistent because after everything is under way things can break down. Versus just saying “We’ve checked at the beginning. You have the `open_channel` rejected there.” Then we can at least say “We weren’t able to find a match for you” versus “We’ve found a match but then it turned out to be a counterfeit good basically”. It is like buying a car, they told you it was manual and it is automatic. You are like “What is this? I can’t drive this thing.” That’s a framing. It is making sure the user is buying or selling the good as much as we can validate it upfront.

The problem with this PR is it conflicts two things. One is if you do zero conf you need some alias mechanism, you need a name for it before it is confirmed. That’s almost useful. We’ve decided we like that. Whether you are doing zero conf or not it is nice to have this alias facility, private channels and stuff like that. That’s almost a PR by itself. The problem with zero conf is if you say “Yes I want a zero conf channel” are you committing to trusting them with the channel? I can open a zero conf channel and let you open it and pretend and then never forward anything until it is confirmed. But presumably when you’ve said “I want a zero conf channel” you are all in and ready to trust with this. Or you are on the side that doesn’t require trust. That is what you are trying to signal.

One other slight thing here with the way Pool works, we like this because it increases the set of signers required to double spend. For example if I have a batch of 5 people opening a channel it requires all 5 of them to double spend rather than just the person that was opening. It also requires us to double spend as well too. It increases the total set of collusion that is necessary in order to double spend the output. The reason they can’t double spend is they are in a UTXO that is a 2-of-2 with us. They would need us and every other person as well to double spend the entire batch. That’s the one difference security model wise with how this works in this setting. It is like a coinjoin where everyone has a timelocked input basically. The input will only be signed if things look good. The trust stuff is explicit. That’s another reason to add a channel type there. “Do I want to accept this zero conf thing?” You are right that there is a double opt-in. We are just trying to make it more explicit. It is more sensible if we know zero conf stuff can’t work for every channel type.

Originally the channel types were just to get around this hack. There were some features we had to remember. If you negotiated that at the beginning that made sense for the whole channel lifetime independent of what’s in the future. But generalizing it to “This is not persistent state but this is stuff about this channel”. It is not objectionable.

If we want explicit signaling I would strongly suggest we switch to a TLV in `open_channel` rather than making it a channel type.

That’s exactly what we have. We have a TLV that is a channel type in `open_channel`.

Internally from the architecture, when we switched across I just went through and changed everything to channel types internally. It was so much nicer. Instead of all these adhoc things going “Is this an anchor channel? Is this a static remote key channel?” suddenly became this bit test of the channel type, this field that went all the way through.

For us it allows us to move our implementation closer to the protocol. We already had the channel type before but now it is one-to-one. It is a different enum or whatever but same thing.

In retrospect we should have done this originally. There are two things. One is do you get an alias? I think the answer is everyone wants an alias. You need an alias if you are doing the zero conf thing obviously. But the way the spec was written is that you’ll get one. I think this is nice. I am actually not all that happy with a channel type the more I think about it. But I do want to go and implement it and see what that does.

It does feel weird because channel type is all stuff that is only persistent.

It is today but maybe that is inflexible thinking. My only caveat on this, it is not necessarily a huge issue, you open a channel and you go “I expected that to be zero conf”. You can specify that afterwards. We were going to have an API where you could go “Trust this node ID”. Obviously if you open a new channel it would be zero conf but you could also zero conf an existing channel by going “I’m going to start ACKing it”. Assuming that it had support for the alias so you were ready to do that. You would end up with a zero conf but you would never have signaled a zero conf. I guess you are free to do that.

Presumably the way y’all would implement that is that even if your counterparty says “6 confs” you will always send the `funding_locked` immediately after you broadcast the funding transaction if you are the initiator. Is that what you are thinking?

Yeah. If you are the initiator and there is no `push_msat`. And in our case with dual open, if you’ve got no funds on the line we will just go “Sure whatever”, we will zero conf stuff.

Why does `push_msat` matter?

If I have all the funds in the channel then I can use the channel immediately. If you screw me you’ve just lost money. But if I’ve `push_msat` to you you can push stuff through the channel.

You are still presumably not going to double spend yourself. It just prevents you from double spending the funding transaction? The idea is that you’d like to be able to continue double spending the funding transaction? The initiator pushes msat to the other counterparty, it is all your funds but you’ve given it to the initiate key?

Specifying `push_msat` puts you at some risk of them getting the money. If it is single conf even if your double spend fails you still have everything.

Presumably you were ok with them getting the money because you’ve pushed msat to them?

If you wanted to scam them maybe you wouldn’t do that.

The guy who accepts the `push_msat`, if it is a payment for something that has been semi trusted and done before, “I will push you msat because I opened this channel because you opened a channel to me. I opened a channel back in response. I will push you money through that.” But if you accept it as zero conf and they double spend it you lost that msat, maybe you opened a channel in response. It is more the guy who accepts the `push_msat` that has a risk of accepting zero conf.

You can generalize this for the dual funding case.

This is an interesting question then. Basically the channel type or TLV or whatever would say “Either send me an accept with zero `min_depth` or I’m going to immediately close the channel.”

Or send a warning message or error and whatever else.

The initiator will still always send a `funding _locked` immediately and the receiver can still send a `funding_locked` immediately if they want to. The feature bit is only an indicator of either you do this or I am going to close the channel.

It should also indicate that you have some degree of trust, that you will route. I could send whatever I want across the wire and not consider the channel open until… I think it should imply that you are going to let them do zero conf.

They can just deny any channel that has this set. Maybe that helps, maybe that doesn’t. They at least have that ability.

The thing is it should flag that they are trusting the zero conf, not just that they are walking through the protocol.

It should say that they must, not just that they can. If you see this bit and you are going to send an `accept_channel` that does not have a zero conf `min_depth` you must fail the channel.

Negotiation has failed at that point.

It is not optional.

On the alias being decoupled, do we like that in the same combo still? The alias thing has a feature bit already right?

Yes.

You must only route through this bit, not there is an alias offered. The feature bit is not just for the alias itself.

The feature bit is weird. It is like “Only use this one. I really understand what I’m doing and I only want you to use this. Discard the real short channel ID.” This is kind of what you want. But whether we should use a different feature bit for that, I am going to have to look back. We do want a way to say “I am all in on this whole alias idea.”

It should be all or nothing.

But for backwards compat or “I don’t care. It is going to be a public channel but it is zero conf for now” I can use an alias and then throw it away. This is where the alias becomes a bit schizophrenic. We’ve got these two roles. The feature bit would say “We’re all alias and we are only alias”. It is kind of overloaded. Maybe we should go back and change the bit number. If I switch it to a channel type I’ll see what happens.

I thought you did switch it to a channel type.

That is a channel type. Because that is something you have got to remember forever. The same bit would be used for the other channel type so now I have to find another one.

I think it is an example of the advantage of the feature bit. You can have these as individual things. Zero conf and the alias only or you can have all of them. That’s nice in terms of the bit vector comparison thing.

This is where I’m coming around to they are separate things.

A different feature bit.

Yes. Part of the roadblock that we got is because we put them both in together. It became this logjam.

Zero conf requires aliasing though yes?

In order to receive before confirmed yes but maybe we don’t care about that eventually.

Yes. If you don’t have an alias then all that can happen is they can push sats through you but you can’t use the channel.

It is kind of useless without that. Does that mean that you intend to split this PR into two? Or are we going to continue? It sounds like LND already has an implementation, LDK has one.

We have one of everything. The only divergence is the upfront feature bit check. I am cool with keeping it as is and we maybe throw out the bits. Once we have that squared up we can look at cross compat testing.

Add a TLV rather than defining a new bit.

We have a TLV.

Add a TLV that says the required bit.

I’ll edit this PR for now. If I was smarter I’d have split it into two. I don’t think it is worth splitting now.

It is pretty small, not a multi file mega thing.

Action Rusty to do another pass, make a channel type and see what happens, how bad it gets.

# Zero reserve

I’m going to jot that down on the PR. One other thing related to this is zero reserve. Eugene is implementing this and asking questions about zero reserve. Right now I let you cheat me for free but maybe it is not useful unless we have it both ways. I think he was wondering do you always do zero reserve? I think right now technically if you send zero it is in violation of the spec. I think we have must be greater than zero thing.

We accept it, we do not allow you to send it currently. We may at some point allow you to send it. We accept it, maybe in violation of the spec.

Must set greater than or equal to `dust_limit_satoshis`.

If you set that to zero there is that weird interaction. I looked at a really old Breez PR, I found that it allowed zero reserve but it didn’t because it would reject it if it was less than the dust limit. We also had some dust limit revelations a few months ago as far as interactions with other fields.

At least in our codebase I don’t think there’s a weird interaction. If the output value is less than the dust limit you still have to remove it.

Otherwise you’d have a weird situation where I make the reserve on your commitment transaction below dust which means it can’t propagate. Maybe I can do that by rebalancing or something like that.

There is still a `dust_limit_satoshis`.

The issue is you can end up with a zero output transaction.

As long as your dust limit is non-zero. You still remove the output.

No you remove all the outputs, that’s the problem. That’s not a valid transaction.

A zero output transaction, I see your point.

By forcing a reserve you are saying that someone has an output at all times. I think that was the corner case that we ended up slamming into. Maybe it doesn’t matter. What are you doing with your life if you’ve managed to turn everything into dust? I don’t if that is real but I remember that corner case.

I know Breez is running a LND fork and they already doing this in the wild.

If the other guy lets you have zero reserve on your side it is all a win for you. It is only for the other guy that it is a risk.

Exactly. If you say I can have zero I’m fine with that. That doesn’t necessarily give you what you want. You want to be able to do “send all”, close the app and walk away. But right now people have that weird change value lingering. I’m not sure how the mobile apps handle it in practice.

That’s why we did zero reserve on Phoenix, to be able to do “send all” and to have users send all of their balance out, there is nothing remaining.

Because otherwise it is weird. You have this value you can’t move and people will get frustrated about that.

We had users who were like “No I need this or I can’t ship”. I think we have separate dust enforcement around our outputs. That’s a good point, there may be a corner case where you could hit a zero output transaction.

That was the killer. It is unspendable. In one way you don’t care, on the other hand it is UTXO damage.

It is application level brain damage at that point.

So this is one of those more investigation required things?

Write in the spec what you do if you end up in this case. Or figure out a way to avoid it. Say that “The minimum channel size must be such that you can’t be all dust”. Though that isn’t actually possible because your HTLC dust limit depends on your fee rate and stuff like that.

If it is only when anchor outputs, zero fee is used then you have no risk. There is no trim to dust, it is only the dust limit on HTLCs. If your channel is not really small you will always have outputs in there.

What do you mean there is no dust? What if we just move the reserve to the anchor output? Maybe that would solve it.

He’s two steps ahead. I was suggesting that you make your channel size such that you can never have it all dust. But that is not possible in a classic channel because your HTLC size that gets trimmed depends on your fee rate. But as he’s saying, that is not true with zero fee HTLC anchors. Modern anchors, that is not true anymore. You could just figure out what the number is and don’t have a channel smaller than this and you can have zero reserve. Maybe that’s the answer.

Can you explain the making sure you never have dust? You mean you have a minimum channel size that is just above dust?

To avoid this problem where you end up with zero outputs because everything is dust, if you blow away the reserve requirement, you could fill it with enough HTLCs that are all dust. Suddenly you have got zero outputs. You want to avoid that. Figure out what the numbers are. It depends on the max number of HTLCs and your dust limit. But it no longer depends on the fee rate which was the impossible one. If you put that as a requirement, you’ve got to have modern anchor and you’ve got to have larger than this number, formula whatever, then you can have zero reserve. I think that covers the corner case.

You could probably also get away with that Antoine PR that is overly specific. Presumably at this point every implementation has their own separate dust limiting functionality and you could also lean on that depending on how you implemented that. Maybe that is too weird.

It seems like anchors makes it possible for you to compute what this minimum channel size should be to make sure nothing is ever fully dust. You always have enough funds left over after paying for the fees of HTLCs, the first level output that is.

Independent of fee rate which is nice.

There is still one edge case. If the fee rate goes really, really high and you are not capping it because of anchor. If you don’t have any HTLCs and the fee rate goes to the roof… there is only one guy paying the fee…

As long as that guy paying the fee is the one with all the balance and the other one has rounds to dust.

It is possible in theory, yeah.

You may have to put a clause in the fee rate saying you don’t do that. “Don’t set a fee rate such that you would end up with zero outputs”. Figure out exactly what to test rather than just saying that. Assuming we can work out why are we suggesting this is a new channel type? A zero reserve channel type?

I don’t see why it would be.

The argument is “This is the kind of channel I want”.

It would be the exact same reasoning of the previous discussion. They can always send it and presumably you negotiated it in advance.

Similar thing. This would give them the level of guarantee they have today. But more broadly in the network. By them I mean people like Muun and Breez that already do it.

It is one of those things that are pre-negotiated.

That does touch on what Lisa is doing on dual funding. On dual funding she says that the reserve is not negotiated, it is only a percentage. There is a boolean saying “Include it or not include it”. You decide it at what step exactly? In which message? I don’t remember.

I don’t think I have added the boolean thing yet. We’ve talked about adding it.

At the moment it is 1 percent. The 1 percent is known at negotiation time, you choose the protocol you are using. I haven’t added the boolean thing yet.

 Even if we had the boolean it would be after discussing the channel types. So maybe it would be the same thing as for zero conf. If we want to know it upfront then we do need a channel type.

I think it makes sense as a channel type. It also is a feature bit. You know what you are getting. The reason I like 1 percent reserve is the same kind of reason. I could tell you exactly what channel size you will have after putting in this many sats. If we make it a channel type it falls automatically into dual funding anyway.

Does anybody know if you can get zero outputs with just one side sending zero channel reserve? Because there’s an asymmetry here?

Both sides have to have zero reserve right?

What he’s saying is ignoring this I can send it and you don’t send it. Presumably we have asymmetric dust limits, is there some weird edge case there?

Only pre any HTLCs right? You could start with a zero balance on one side before any HTLCs have flown?

<https://github.com/lightning/bolts/issues/959>

There was another PR on ours that we were looking at but I guess this clarifies things. If it is a bit we would modify the bit vector to make sure it is only the new anchors or whatever anchors and go from there. Now we can test some stuff out in the wild again, I can take a look at Eugene’s monster PR.

# RBF

One topic that has been discussed a lot recently is RBF. I don’t know if you’ve followed all the discussions on the mailing list about RBF. I am really eager to see people in meatspace and discuss it more.

Why isn’t it as simple as just deleting that other code? If it was me I would just have a pure delete PR.

It is a denial of service attack against Bitcoin Core nodes. The problem is all of this stuff very quickly turns into either a) it is not actually optimal for miners or b) it is a denial of service attack against Bitcoin Core nodes such that you can’t possibly implement it without breaking everything.

Wouldn’t you keep the whole min step thing? Each replacement still needs to replace a certain amount?

One issue is that if the transaction package is going to confirm in the next block, it is actually not optimal for miners to accept a replacement that is smaller but has a higher fee rate. You decrease the value of the next block which is exactly the thing you don’t want to do.

Why would a miner have a bigger mempool and keep the conflicts? You could check only the ancestor package and accept things that have a bigger ancestor package than the things they are replacing, not care about descendants. The miners would keep more and would keep conflicts, for them it would make sense.

You are saying that you look at just the part that is in the next block and then you look at whether or not that has a higher total fee?

No. The code that we would use for RBF on the relaying nodes would not be the exact same code as what the miners would do.

Russell O’Connor’s [proposal](https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2018-February/015717.html) from 2018 is still the best in my opinion.

If a Bitcoin Core node is making decisions that are different from what is being mined you are denial of service attacking yourself. Fundamentally by relaying and by validating and doing all the work you are spending time doing something. If that transaction is something that the creator of that transaction knows will never get mined then they know they can do this all day long.

You are not always doing the optimal thing because there may be descendants. I want to ignore descendants when evaluating whether a package is better than another package. Ignoring descendants, it is much easier because it doesn’t vary from one mempool to another if you only look at ancestors. You still force the ancestor package to increase.

The ancestor package but what about the descendants? You’ve kicked out the descendants and the descendants are a free relay issue. If I can add a bunch of descendants to the mempool and then do something that kicks them out without paying for the descendants then I can do this over and over again and blow up your CPU.

I believe the conflict is fundamental here. The miners don’t care how much spam you’ve got to get through to get to them, that is what their priority is. The network priority is minimize network traffic. These two are in conflict. They are absolutely in conflict. Currently Bitcoin Core biases towards protecting the network rather than optimizing for miners. Not long term incentive compatible.

What you are saying, you don’t care if you are throwing out children. The point is you could also have a world where you just simply don’t accept these children. If you are wasting traffic adding all these children, I guess this gets into the distinction between top block versus not. These descendants being in the top block versus not. Fundamentally if you really wanted to rearchitect the whole mempool from top to bottom what you would really do is say “I am going to aggressively relay things that fit in the next block. Beyond that I am going to aggressively rate limit it. I am going to have a fixed bandwidth buffer for stuff that is not in the next block. If it is in the next block I’ll relay it.

You have less spam problems at that point because anyone trying to spam with tiny replacements is at risk of getting mined at any point. It also gives them emergency override to go “I need to override this so I am going to slam it with a fee that is going to get in the next block and everyone will relay it.” It is also much more miner compatible. Fundamentally the concept of a mempool as being a linear array of transactions that is ready to go into blocks at any point is not optimal for miners. They should be keeping a whole pile of options open and doing this NP complete thing where they are rejuggling things, that is not going to happen.

What is practically optimal for miners is also what they can run in their CPU in a reasonable amount of time and can actually implement. There is an argument to be made that what is optimal for miners is always do whatever Bitcoin Core does because it is probably good enough and anything else takes a lot of effort which may screw you if you make an invalid block.

On your point about evicting descendants being costly. Is it really because it is bounded? You don’t have chains of descendants that can be longer than 25.

It is not bounded because you can do it over and over again.

Every time you are still increasing the package of the ancestors. That on its own will eventually confirm. You will have paid for something.

The question is how much of a blowup compared to current relay cost are you doing? Current relay is very strict. There should be no way to relay anything such that you pay less than 1 satoshi per vbyte of the thing you’re relaying. Full stop, you should always pay at least that. What you’re saying is “Yes you can relay more but you’ll pay something”. It is true, you’ll pay for something because you are increasing the fee rate. If you don’t require that you pay an absolute fee for the things you evicted you are potentially paying substantially lower than 1 satoshi per vbyte. The question is how much of a blowup is acceptable, how much of a blowup is it? To make this argument you’d need to go quantify exactly how much blowup can you do, what have you reduced the relay cost to from 1 satoshi per vbyte? I don’t think any of these proposals have done that.

That is something that should be easy to compute. I can try to have a look at it before London. I will discuss this with folks who will be in London.

I will start to review Eugene’s zero conf thing. People can ping on the issue once they have that ready for interop. Then maybe by a meeting or two from now I will have some Taproot PTLC stuff ready and make t-bast’s [gist](https://github.com/t-bast/lightning-docs/blob/master/taproot-updates.md) a little more concrete.

I don’t know if anyone replied to the [gossip thing](https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/lightning-dev/2022-February/003470.html) I threw out there. I did promise last meeting I’d put some meat on that proposal. It is still way off.

