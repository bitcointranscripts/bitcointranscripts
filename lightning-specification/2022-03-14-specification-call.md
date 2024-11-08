---
title: Lightning Specification Meeting - Agenda 0969
transcript_by: Michael Folkson
tags:
  - lightning
date: 2022-03-14
---
Name: Lightning specification call

Topic: Agenda below

Location: Jitsi

Video: No video posted online

Agenda: <https://github.com/lightning/bolts/issues/969>

# BOLT 4: Remove legacy format, make var_onion_optin compulsory

<https://github.com/lightning/bolts/pull/962>

I think eclair and c-lightning have both removed support for legacy payments.

I’ll probably make a PR to add the feature bit or at least flip it to required. The only wallet I can think of that is somewhat more fringe now is Simple Bitcoin Wallet. I am assuming they are doing the new stuff because they have some other hosted channel thing that adds custom fields.

# BOLT 2: coop-closing clarification

<https://github.com/lightning/bolts/issues/964>

Next one is some questions around co-op close clarification. Do you allow people to send the co-op `closing_signed` message when HTLCs are there? What do we define as a clean slate when a co-op close transaction was able to move forward?

This is about shutdown not `closing_signed`.

You should only send the shutdown message once there are no uncommitted changes including fee updates. If you receive one early then you should just wait until the coast is clear to enter the second stage of co-op close negotiation.

I have two more questions. One of my questions was if you get a shutdown or you send shutdown and then you reconnect should the state be cleared?

Good question. This is something that we do right now. We need to fix it, we consider it a bug. If someone starts co-op close and the connection dies we won’t allow any force close or co-op close to resume after that. Co-op close is weird in that if you send a signature to someone and then resume the channel they can broadcast at any point. That is something on the side that maybe we should add to the spec as well.

It shouldn’t really matter. Once somebody sends shutdown if you care about the shutdown and you reconnect you should also resend the shutdown and then you are in the shutdown again.

What if you don’t send shutdown? That is one of my questions. Is that fine?

If nobody sends shutdown and then somebody sends `closing_signed`?

No if you send shutdown, reconnect and then don’t send shutdown again and horde an HTLC.

That would be up to your counterparty. If your counterparty thinks you are in shutdown they will reject the HTLC. If your counterparty doesn’t think they are in shutdown they will accept it. You are supposed to resend shutdown on reconnect? I don’t actually know if we do.

I don’t think so. I think he is bringing up a point that a channel could get stuck. If one side sends it and the other side remembers it. I think what we do is we remember the shutdown and then if things didn’t happen we won’t let a co-op close happen. It is kind of like a bug.

The solution to this is we should resend shutdown right?

You’d need to remember.

If you require that `shutdown` gets resent then on reconnect if one party remembered it they will resend and then you will be in shutdown. If neither party remembered it then no one will resend it and you won’t be in shutdown. As long as you resend it would be fine.

If they don’t resend and you don’t remember you won’t be in shutdown which is fine. If they do remember to send it and you don’t you’ll still send `shutdown`.

Yeah as long as the party that is remembering resends.

I don’t think it needs to be specified I guess.

I’m not 100 percent sure that resend `shutdown` is currently required but it clearly should be.

Looking at our code, right now after we send a `shutdown` message we will commit that and stop the channel from being used altogether.

We do the same thing as you. We commit it async and we have it implemented in `channel_reestablish`. When we receive a `channel_reestablish` if we’ve committed that and remembered that we have `shutdown` then we will resend that `shutdown` message and then we’ll be in shutdown. It is not a concern as long as you have resend implemented. We may have a bug in it but according to the code it looks like we resend it.

Right now we won’t allow it to resume. If we lack this behavior then I guess we should mandate retransmission on `shutdown`. At this point we will just resend it. If we come up and the thing is in co-op broadcast and we don’t have the commitment transaction to broadcast we can just resend `shutdown`. That would fix the whole resume issue that we have right now.

The spec mandates that you remember `shutdown`. “Upon reconnection: if it has sent a previous `shutdown` MUST retransmit `shutdown`”. Technically it doesn’t mandate that you remember if your counterparty sends it. Your counterparty could send it and you could have not sent it yourself. But in practice it mandates retransmission which mandates remembering that you were shutting down.

The usual fix is to commit locally before sending a message. Then you resend it upon reconnect. You can’t force the other side to do it because a close message might have been lost. If we all just agree to resend a close on reconnect that should solve it.

We already store that we sent if so we can retransmit it. There’s no other information you need really to retransmit after you’ve sent one. I think that will resolve our quirk there?

Yeah.

I just commented on issue.

My next question was should `closing_signed` only be sent if there are no pending commitments?

That is already required. There has to be no pending anything for `closing_signed` to be sent. Can you specify your question a little more?

I think he means a dangling commitment. If I send one and you don’t revoke yet can I send `closing_signed`? You have two commitments and you haven’t revoked one of them. Is that the scenario?

Yeah it can be that the dangling commitment and your own local commitment are actually clear of any HTLCs.

You mean from the `update_fee`?

Yeah because the dangling commitment is an `update_fee`. Are we saying the `update_fee` hasn’t been fully committed yet or something?

Yeah, not locked in on both sides.

It shouldn’t matter too much.

How does this interact with `shutdown`? You wouldn’t enter shutdown until you had nothing pending?

It is saying if you are changing the fee, I don’t know if you are allowed to do at that point.

You wouldn’t have sent a `shutdown` if you had a pending fee update outstanding?

No but you could generate a fee update after you’ve sent `shutdown`.

I think you are saying that that shouldn’t be allowed. You should assume that you don’t send anything new after you send `shutdown`.

It is awkward to not allow that though because you may have a HTLC that times out in 2 days. If you aren’t allowed to do a fee update for 2 days while you are waiting on a HTLC to timeout that is kind of bad.

I thought the idea of sending a `shutdown` signals we are not updating this anymore.

The idea of `shutdown` is I’m not going to add any more new HTLCs. Now we are just waiting for the HTLCs that are here to timeout before we do a `closing_signed`.

eclair opened an issue on our repo. Rather than postpone the shutdown we’ll just say “We can’t shutdown”. Otherwise you get into an ambiguous state. Do you wait 2 days to send the `shutdown` with no feedback to the other party?

No you send the `shutdown` and then you wait for a `closing_signed`. That is what the spec says.

And then just waiting there potentially.

Yeah. `shutdown` says “Stop sending new stuff”. Once the existing stuff gets resolved you do a `closing_signed`.

What’s your HTLC case with `update_fee`? The reason that you’d want to send it?

Once you send `shutdown` you are not adding new stuff but you could have a HTLC that doesn’t timeout for quite some time. Yes you are about to do the `closing_signed` dance, you are about to do a co-op close, whatever, but you don’t want to be in a state where you are not allowed to do an `update_fee` for 2 days while you are waiting for some HTLC to be resolved.

Something, something anchors so you don’t care.

Anchors with package relay.

I think the answer is no. At that point you are waiting for the remote party to revoke. They have two different balances potentially. I think the answer is no, you should wait.

Ok. Everything clean?

But allow `update_fee` I guess.

That’s the thing, you have no idea if everything is clean. Your counterparty might have sent a `commitment_signed` that you haven’t received yet. Then you send a `closing_signed` and then you have to respond to the commitment transaction but you’ve already sent a `closing_signed`.

For us we will remove the channel from the active set of forwarding stuff. If you sent a `commitment_signed` after we’d sent `shutdown` it would get lost.

Certainly you have to be able to handle an update fulfil HTLC after shutdown.

We’ll just disable the channel and make sure nothing routes to it.

You are not allowed to route anything new to it but you’d handle an update fulfil.

You mean do we process a settle when are in the shutdown phase?

No.

That’s not the intent of `shutdown`. The intent of `shutdown` is to declare an intent to stop adding new stuff. It sounds like you guys have implemented `shutdown` the way the spec intended `closing_signed` to be implemented.

At least we are saying you need to retransmit `shutdown` which seems to clear up some of these issues here and fixes a bug that we’ve had for a long time to let people resume.

Yeah there is still definitely the question of how to handle fee updates post `shutdown` pre `closing_signed`. Do you mind taking an action item to try to draft an update to the section on `shutdown`?

Yeah. For `update_fee`?

The main thing here is should you allow `update_fee` after `shutdown` has been sent on both sides?

I guess the spec is clear already. It says “The only case where you are not allowed to send a new update is if there are no HTLCs”. Once the HTLCs are gone you are not allowed to send an `update_fee`”. I think that is clear. I don’t see any immediate edge cases there.

I think that limitation to piggy back on top of `update_add_htlc` or remove HTLC should clarify that.

I don’t think we implement this but you are allowed to send an `update_fee` as long as it is also with an update remove in the same `commitment_signed`.

You can’t send it in isolation but you can send it when removing a HTLC.

Yes.

You definitely should allow removing generally because that can help you get a channel to a clean state.

You have to allow removing. I think the spec is clear. I don’t have any questions here.

About fee, yeah ok but not about the pending commitment thing.

That needs a clarification. Do you mind trying to tackle that one?

I can do that.

I just [commented](https://github.com/lightning/bolts/issues/964#issuecomment-1067201164) on the issue. Number one, should you allow `update_fee` after shutdown has been sent but you still have HTLCs? Yes as long as there are HTLCs present. And it is packaged…

I don’t think it has to be packaged. It doesn’t have to be packaged, there just has to be HTLCs.

You can send it if there are HTLCs?

Yes. There have to be HTLCs or it has to be packaged.

# BOLT 1: introduce port convention for different networks

<https://github.com/lightning/bolts/pull/968>

I thought this was a non-standard port thing. Then I realized we already allow that. It is ports for different networks, mainnet, testnet etc.

You can do this today given we let you specify a port. It is kind of like adding a convention of using a different port for testnet. Funny how Litecoin is added there. Do people still support Litecoin? We kind of support it but not really.

Let’s just drop the Litecoin part, I don’t think we need it in BOLTs.

It is pretty broken in LND today. We broke it accidentally while we were doing some wallet stuff. I think someone has a fork somewhere. This sounds fine to me. It links to a bitcoind [PR](https://github.com/bitcoin/bitcoin/pull/23306) but I don’t think that PR is related (Make AddrMan support multiple ports per IP). We already kind of have that.

I don’t see how that is related.

I thought it was about letting people send out non 8333 port.

This is just convention, it seems fine. I left a comment on Litecoin and then I’ll be fine with it.

# BOLT 7: Onion message support

<https://github.com/lightning/bolts/pull/759>

Any updates here?

I don’t Rusty is online.

I need to reply to his reply to my mailing list post.

# Blinded fees

<https://github.com/lightning/bolts/pull/967>

Blinded fees, blinding more stuff. 967 is blinding more stuff in the blinded route itself. I guess including fees and CLTV, adding more data in the TLV I guess.

How does this work because you can’t just add up the…

How do you make the route?

You can make the route but it only works if there is a single hop. If you have two hops then you can’t just add up the proportional and absolute fees and use them separately. You have to list the proportional and absolute fees. I haven’t read the PR, does it require that you list them out?

For the CLTV you can at least increase your final hop delta whatever.

For the fees you can’t just add them. You at least have to reveal how many hops there are.

Not even that works. With different fee schedules you can’t compute that and it opens yourself up to being probed again by a strange fiddling of the fees.

I’ll post on here does this work and let you compute fees properly?

Can you respond on the issue?

Sure.

# Route blinding

<https://github.com/lightning/bolts/pull/765>

I guess this is related to the prior one? At least there is a new update to this one. Updating some notation.

# Dual funding

<https://github.com/lightning/bolts/pull/851>

I don’t have any immediate updates. There are still a few pending things that t-bast requested, making the reserve optional, that I need to get in. We are wrapping some stuff up for the next release. We’ve also got someone who has started working on splicing in c-lightning. That is using the [draft](https://github.com/lightning/bolts/pull/863) that Rusty wrote up a while ago. It reuses a bunch of the stuff that we have in the dual funding, the interactive transaction protocol part to do the splicing. Hopefully we will have some more progress on that soon which is exciting.

# Offers

<https://github.com/lightning/bolts/pull/798>

Offers, I saw there were some comments from Thomas from ACINQ. I’m guessing still working on interop and stuff like that.

# Add a max_dust_htlc_exposure_msat

<https://github.com/lightning/bolts/pull/919>

I’m not sure this has legs still.

I updated the wording a while back based on Rusty’s feedback.

The original feedback was that it was overly specific. Did you end up rewriting it to be less prescriptive and more just describing the issue?

Yeah I think so based on their feedback.

Re-request people to review.

# Websocket address type: allow transport over RFC6455

Interop section, this web socket thing. I think Chrome enforces it, maybe Firefox and some other ones don’t. That fragmentation probably makes it difficult to assume it is not there.

I think the solution to this is we need to drop the current design and replace it with a hostname. Have a flag to say “I support SSL or TLS”.

That’s related to [PR 911](https://github.com/lightning/bolts/pull/911) that adds the hostname in the first place.

Yeah. I feel like we need to have a separate hostname but Rusty is not here so I’m not going to try to declare how we should move forward, I’ll let Rusty do it. We just need to have a hostname and you have to say “Yes I support SSL” because it is going to be required.

That makes sense. The whole point of this is to do encryption in the plaintext web sockets but I guess that’s not really a thing.

If you are going to proxy you might as well just proxy.

Yeah, sure.

# BOLT 7: add gossip address descriptor type DNS hostname

<https://github.com/lightning/bolts/pull/911>

This is also in waiting for interop section.

Hasn’t it had interop? We haven’t added it yet but I thought eclair had it though. t-bast isn’t here.

I think they do. I know c-lightning has it. We have a similar feature that hacked around this but this is pretty straightforward.

We had a Summer of Bitcoin person open a PR but it needs a little love so we’ll get it eventually.

# Echo channel_type in accept_channel

<https://github.com/lightning/bolts/pull/960>

This came up in the zero conf discussion stuff, around making sure different modes could work. We got an ACK from Lisa. I think we already do this, it is just a thing to confirm on our end.

Was this the thing we were going back and forth on?

It is a thing we broke out.

I was confused. We always ack it back in the accept and I thought the existing language basically says that already. If you have the feature type set wouldn’t you be sending it in `open_channel` in the first place anyway?

It is your counterparty not you right?

We checked it and it wasn’t super clear so this is to make it more explicit.

If you negotiated the feature you have to send it in `open_channel` but somehow you could have ignored it in `accept_channel` and not have sent back anything. This would have been compliant with the spec but is obviously nonsensical.

My understanding of the spec and looking at the way it is implemented in c-lightning, if it is sent in `open_channel` we always send it back in `accept_channel`. That is because of the existing language in the spec, it should cover all those cases.

The existing language in the spec says that if you send it back you have to set it to the same thing. It doesn’t say when you have to send it back.

If it is set you have to send it back?

No the spec doesn’t say anything like that. It should.

If you don’t echo it back you can just stop funding basically.

I thought the change was just to add an extra thing about the feature bit. It seems the thing you are actually trying to say is if it is in `open_channel` you should always echo it back.

The feature bit thing is trying to say “If it is in `open_channel` and you understood it and you support it then you should echo it back”.

But you should always echo it back then?

If you understand it and you support it.

We had a few things where if they didn’t send it we assumed that they liked what we had. At least if you send it it is more explicit.

Then it is a question of what’s the behavior if they don’t send it back. But that’s not the part of the spec we’re patching?

This PR is saying if they don’t send it back you can just bail out.

Remember the history, the history was we did not have the feature bit at all in v1. In v1 of `channel_type` what happened was the initiator included it in `open_channel` and then either the `accept_channel` included the `channel_type` in which case they declared that they accept the channel type or they did not include the `channel_type` in which case you fallback to the classic behavior based on feature bits that exists. Then we added the `channel_type` feature and we said “If the `channel_type` feature has been negotiated you have to include it in `open_channel`” but we didn’t say anything about whether you had to accept it and include it in `accept_channel`. This is just saying “The feature bit is there. You definitely have to use the `channel_type` stuff and you can’t ever fallback to the classic pseudo undefined logic of deciding the `channel_type` based on the features that exist.

I don’t think we need to change the language on the top thing. If it is a `channel_type` you must set it to the `channel_type` for `open_channel` and that is a must.

The point is we want to declare that you have to use `channel_type` negotiation if you declare that you intend to use `channel_type` negotiation.

That is not what this PR does. This PR changes it from anytime the `channel_type` is set in `open_channel` you have to echo it back to only if the feature type was negotiated you have to echo it back. That seems like a downgrade from the current language.

To my understanding most of us already do this. It is just a matter of updating the spec to reflect our behavior. If you don’t send it we’ll reject.

I don’t think we have to change it.

When the spec was written if both nodes set the `option_channel_type` feature node A sends a `channel_type` in `open_channel` and node B responds with an `accept_channel` without setting `channel_type` that is both completely well defined and is not an inference of acceptance of the `channel_type` that was declared. Instead it falls back to the init message, feature based `channel_type`.

We are trying to prevent that.

Yeah because that is dumb behavior but that is the way it is currently written.

Sure, that’s my understanding as well. Right now if you send an `open_channel` with the `channel_type` and the other person sends `accept_channel` without the `channel_type` you are going back to the implicit feature bit.

You are not allowed to not send an `accept_channel` message without a `channel_type`.

It says “If it sets `channel_type`”. It doesn’t say that you must set `channel_type`.

The “it” here is the `open_channel` message. Maybe that is what is unclear. If the `open_channel` message sets a `channel_type` then you must set the `channel_type` from `open_channel`.

No “it” is the sender. The sender…. sets `channel_type`.

I think that is weird wording. If it sets `channel_type` and “it” you are saying is the `open_channel` message so this is making it less ambiguous wording wise.  Now it is saying “If the `channel_type` is negotiated then you must set the `channel_type` from `open_channel.” To me this is making it more explicit.

I see your understanding but I do not see how it refers to `open_channel`. The way that the specs are written is you have the top thing as the sender and then you have some bullet points. “It” refers to the sender.

That’s weird though right?

You just need this one bullet that says “If the `open_channel` sets the `channel_type` you must echo it back”.

That is confusing given old nodes don’t even know what these things are.

But the old node wouldn’t send it back and then you would fail it because it was supposed to set it.

It wouldn’t fail it. You’d just fallback to the old style of negotiation.

There is no “if the channel is not set”.

If it is not set in `accept_channel` the intent is that you fallback to the old style pre `channel_type` negotiation, which is based on the feature flags in the init message.

We are trying to make it explicit that we don’t want the fallback that you can reject if they try to do the fallback. That would less us delete a line or two from LND.

This update doesn’t do that.

My reading is that it does. At the very bottom it says “If the `channel_type` was negotiated but the message doesn’t include a `channel_type` you may reject the channel.” I think it is referring to the receiver receiving the `accept_channel`. Now we are saying you can bail out so you don’t have to do the weird implicit thing.

The original thing meant to have text of “It is a forward compatible change.” That’s part of why I read it that way. The initial wording was “It is forward compatible so if you don’t set the `channel_type` it is implicitly falling back to the old style.

I re-approved it. I guess t-bast can potentially merge when he gets back.

# Long term updates

I finished [MuSig2 stuff](https://github.com/btcsuite/btcd/pull/1820). Now it is fixing up the API, making it hard to re-use nonces, stuff like that.

