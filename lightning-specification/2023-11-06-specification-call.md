---
title: Lightning Specification Meeting - Agenda 1116
transcript_by: Gurwinder Sahota via TBTBTC v1.0.0
tags: ['lightning']
date: 2023-11-06
---

Agenda: <https://github.com/lightning/bolts/issues/1116>

Speaker 0: I moved the first item on the to-do list today, dual funding, because we finally have interop between C-Lightning and Eclair. We were only missing the reestablished part, and everything was mostly okay from the beginning. It looks like the spec seems to be clear enough because we both understood it the same way. So now, we really have full interop on master, and I guess this should go in a release with experimental flags for CLN. Is that correct? 

Speaker 1: Yeah.

Speaker 1: Okay. I think [redacted] rebased the PR and squashed some commits to clean up the commit history a bit. I guess this is the last call for dual funding before we merge that. Hey, [redacted]. I don't know if there is anything pending from teams who are in the middle of implementing that. Is there some feedback here?

Speaker 2: We have very light progress. I would not say we have anything that's going to give you material feedback yet.

Speaker 1: Okay.

Speaker 3: Yeah. We're taking the long way around with this in terms of like down code and stuff, which goes into dual funding and splicing eventually.

Speaker 1: Okay. So does [redacted], or anyone who is reviewing that on the LND side as well, want to have a last look at the PR and make sure that we are not missing important things before we merge it?

Speaker 2: I can tag [redacted] and see if they have any more feedback. They’ve been in and out. I think they’re off this week, but I can ask [redacted] if they have some time.

Speaker 0: Okay, I think helping on the PR as well for the previous reviewer, saying that he might merge that soon. So if people want to have a last look at it, now would be the time. I guess that's it for dual funding. Simplifying mutual close. Is there anything new since the last two weeks?

Speaker 1: No, sorry.

Speaker 3: Yeah, I think this is in the ‘need implementation’ phase basically, right?

Speaker 1: Yeah.  I can't even remember if I added the N sequence set.

Speaker 3: It doesn't change what the sequence is on the call question direction or …?

Speaker 1: Oh, yeah. Basically, you'll nominate what you want the N sequence to be as long as it's RBFable.

Speaker 3: Oh, sure.

Speaker 1: There's a bit saying what values you can use for things and you know best practices, etc.

Speaker 3: Cool. Someone wants to check out again as well. 

Speaker 1: On the LND side, what's your plan to integrate that with Taproot?

Speaker 3: The plan is to use our current staging feature bit as what we have currently. Then, once we actually have the actual feature bit, to basically kind of assume the existence of this because I'm assuming this is going to get in well before that. We'll maybe even have a dependency in our codebase at least as far as like once you have the final type root bit, you basically also should have this one because that would be the co-op closed forward. It should be a pretty clean transition. I think it's also a good idea that we started to do the same thing in the first place. It simplifies the whole: Oh, I was on taproot 0.95; we merged 1.0; and blah-blah. So, I think we have that path clear at least.

Speaker 0: Sounds good. I guess next up is peer storage. [redacted], you put that one on the list. For what it's worth, I think that mine and this one, even if they diverge, this should rather be a blip, I think, than a bolt. I think this is really an add-on that doesn't need to be in the bolt. But...

Speaker 1: I don't mind. I mean, I would like to see it implemented everywhere. It's only interesting because it has asymmetric feature bits. It's one of the few. It's the first asymmetric feature bit we have. Like somebody has it: I offer this feature, and someone else is like: I need this feature. They're separate bits. Although, in our implementation, we'll be offering both. I mean it's trivial. It really is trivial. Basically, if they send you a new message, you just stash it somewhere, and when they reconnect you throw it back at them. Yeah we're hoping to get more sophisticated because people don't do backups. Hell, I don't do backups. We should all do backups, people. So just spraying it at your peers gives you an increased chance that if you just managed to say if you're secret, your master secret, in some form, at least this will let you get stuff back. We're basically just using it for static backups at the moment, but we would hope to get a bit more sophisticated and that would be kind of cool. It's kind of resting on the whole idea that we've discovered that generally your peers are kind of trustworthy. Best effort works shockingly well. So, you really can't get much simpler than this, right? You just throw an odd message in there and send it back. So we've implemented it. We do this at the moment, and it would be cool to see other people do it. Our plan is if you restore, you grab all the gossip and see if you've got any public channels, but it doesn't cover if you've got, and then you can connect to one of your unknown peers, right? From that, and then hopefully, they'll throw you back your peer storage and you can kind of bootstrap off that if you've got private channels. If you only have private channels, it's harder. You can try to connect to everyone on the network and see if anyone gives you a backup. The other option, of course, is that there could be people who will like — you throw them some sats, and they will back up for you anyway, right? It's assumed at the moment. If the idea is that you will best effort store a blob if you have a channel with someone, but not necessarily if you don't. But you could totally go: Cool, I'll store your crap for a year for. I get 64K, right? It really is in the noise. So that's the only possible extension to this really. So yeah, it's trivial. We have an implementation of it. I don't know. So [redacted] has got a grant, and they’re working on this. I think [redacted]’s talking about doing it, like trying to hack on LDK to add it there, but the only thing about that is that technical users have two independent implementations. And I'm like: If [redacted] implements both, are they still independent implementations? Left hand versus right hand? I don't know. But it is pretty straightforward.

Speaker 3: Yeah. This seems super simple. I think we're going to take a look at doing this as well, because we have our SCB flow and I think we have a similar flow, which is a matter of doing the storage stuff and completion shouldn't be trivial. We have AED stuff on our end already, but I'll write this down to see what we can put this on future milestones.

Speaker 1: Yeah. It just seems like a no brainer. Something that [redacted] should probably start doing. The question someone asked: What happens if you've got more channels and fits in 64k? It's like: Get a serious fucking backup solution. Like, don't giant node or rely on having — I don't care. So, it fits pretty well.

Speaker 3: Make sense. Cool.

Speaker 1: Yeah, and we could just come up with a crappy bech32 styling coding CL emerge for the static backup file format. Just so people can cut and paste it, and feed it to our RPCs and stuff like that if they have one lying around. It's basically a tag in front of this encrypted SCB blob. Cool. Okay. No, that's it. I just wanted to raise everyone's attention that it's being worked on.

Speaker 3: Cool. Then y’all already have an implementation of the ship basically, right? It's virtual, something like that?

Speaker 1: Yeah. Cool. Yeah. You connect to it, you'll get your stuff back. The spec doesn't say you have to commit. I mean, in theory, you don't even need to put in a database. You just write to do somewhere, and best effort. It's kind of hard to specify that you definitely have. You're relying on the goodness of strangers, right? So, don't ask for too much.

Speaker 1: Cool.

Speaker 3: Spec cleanup. I think we're going to do the required feature bit thing for 18, which is our next major release. At least then, that's kind of on our radar still to get that in. I think we have an issue for it as well. I'm not sure if anyone has started. I think CLN can start to do some of these though.

Speaker 1: We've done it for this release, which is in RC1. So far, so good.

Speaker 3: Does Eclair already do this, [redacted]?

Speaker 0: Yeah, it’s on our network branch, and it should be on our node in the next few days.

Speaker 3: Yeah, it should be on master, I think at least. Okay. Just spec cleanup? Offers? I think the last time...

Speaker 0: I think the last time, we were just asking people whether they made progress on the SCID or pubkey encoding. I think one that has it implemented right now. We have a PR that is ready to review, but I think we need other people to have it, and also to include it in the test vectors, I guess.

Speaker 3: But like that's optional to my knowledge, right? That's just like a more compact version basically. Or is that meant to be like the standard where you're going forward?

Speaker 2: Meant to be the standard.

Speaker 4: Well, I think it's optional in the way it can be used, right? You can be either or. 

Speaker 2: I guess it's optional for the recipient, but the sender needs to support it if recipients are going to generally use it.

Speaker 4: Yeah, that's true. I guess on our side, we did have Munity wallets integrate offers in this experimental way. Not in a release or anything, but they were able to pay an offer generated by, I guess, with C-Lightning for their LSP. That was with a direct connection, which is what we support currently. And then, they were also able to parameterize our implementation so they could do a munity to munity through an LSP, along with the channels public. So, we're kind of there, but there's still more robustness that needs to be supported on our end for our next release. 

Speaker 1: Are there interesting things that you learned during that experiment? 

Speaker 4: Yeah, the one thing is they couldn't use — so by default, their channels are private with their LSPs, and we couldn't route to those. Just the way our routing algorithm is set up. I think they could kind of hack it with parameterizing their own router, but we didn't really go too far down that route. Otherwise, nothing surprising yet. But, like I said, we require a direct connection for onion messages. Although it was nice seeing that working correctly.

Speaker 3: Cool. Have people started to do more end-to-end routed stuff? I'm curious what people are presenting as far as the fallback. For example, a wallet: What timeout you're gonna use for actually fetching it? If it does timeout, did you just retry more? Are you trying parallel routes? Just thinking about the end wallet experience versus to get that as good or better to what we have today, basically.

Speaker 4: Our current version doesn't do any retries, but we will take every path that's in the offer, up to, I think, eight or ten, if you're rich. Just send invoice requests to all of them, and we'll make sure to pay one of them. If we are the person that receives those requests, we would issue more than one invoice, I believe.

Speaker 3: Oh, I see what you're saying. I guess you ignore the rest of them once the main one has been settled, or something like that.

Speaker 4: I mean, they would hopefully only pay one of them. If they wanna pay more…

Speaker 3: Sure. 

Speaker 4: They technically issued more than one request, but our code is set that we would only pay one of them. We basically put a payment ID in the metadata. It's encrypted, and then, we'll have some state tracking whether we've sent the payment yet or not.

Speaker 0: We fail after about three minutes if we haven't gotten an invoice in response to our invoice requests.

Speaker 4: Yeah, that might be down to one minute. I forget what we settled on, but for refunds, it's a little different. Refunds, I mean, like an inverse request that is without an offer. It's just how we’re phrasing them in our code, and there, it's based on the expiration of the refund.

Speaker 0: We will also be starting to prototype this inside Phoenix to see what the rise is when you actually start using it in a mobile wallet. This is on our roadmap for the next few months. We don't really have a timeline, but this is something we'll be working on soon.

Speaker 3: Yeah, I'm definitely interested in the wallet flows. For example, we did like APIs as well ‘cause right now, we just have the simple: add invoice, get invoice. But then, the whole offer thing, things like that. I guess for the wallets, at least on our end, people on top of it. But now that we're finding the inside of the paths, this is the stuff that we can start to be thinking about API wise.

Speaker 4: Yeah. For the API, like I mentioned earlier, we'll just basically use the same payment ID in each of the invoice requests that we sent out. And the developer UX, they're sort of agnostic to the fact that there's more than one message flying around.

Speaker 3: Gotcha. Yeah, because we're in the middle of a database rework basically because it was just hacks on hacks, as some of you know from the early days. Ideally we can revamp this stuff to have better support for attracting this on the database level, which would just make stuff easier. Because right now, our notification API, you can't get the first invoice because it's off by one error. So you have to get the first one and then get it. Things like that. So we're going to fix all that. Cool. Okay. Splicing?

Speaker 0: I guess on quiescence and splicing, now that dual funding has cross-compat interop between Eclair and CLN, I guess we should be able to do some splicing interop tests as well between Eclair and CLN. It's going to be easier, and since we will have a Dual Funding PR merge soon-ish, it will make it much easier to rebase the splice PR on top of the quiescence one. So I think it's going to be much easier for reviewers to figure out what is happening and what we are depending on. It's going to help us clean up that PR and make sure it becomes easier to read and review.

Speaker 1: Yeah. One issue with splicing is we decided to go the easy way with gossip and have this thing where we basically don't consider the channel actually closed until after 12 blocks so that you get the chance to go: Oh, it was a splice, right? So you get continuity. The problem is that channel updates happened during that time. That first six blocks. New one hasn't been announced yet. The old one is closed, but it's still in that pending state. I know Eclair got upset with us sending stuff about dead channels, but we're kind of in a rock and a hard place here, right? You've just done a splice. Should we have some flag to say: Hey, there's a splice in progress, or something? I don't quite know how we want to square that circle. Because the problem is a brand new peer starting up who has never heard of the old one is going to get upset with you spamming them about — we've already suppressed it so we won't re-announce that old one. The dead-looking channel, just because we won't piss peers off about that, which is kind of a corner case there. So we won't tell you the channel exists, but we will send you channel updates about it. And you'll go: That's weird because that's not any channel I heard about, and it doesn't seem to be in the UTXO set. So, just something we probably need to think about.

Speaker 3: So the issue is that splice unconfirmed, six blocks haven't passed yet, and you can't send channel update to the network or your direct peer?

Speaker 1: Well, we do send channel updates out, but it looks weird to people because you're sending channel updates about a channel that's not in the UTXO set anymore. right? Now, if they saw it die, right? They can mark it somehow going: Oh, yeah, cool. I understand. This is kind of a zombie channel, I guess, because you're sending channel updates. I assume you must be splicing or something. But if they never saw the original, then they're fresh on the network. It's kind of weird for you to send them these things about a channel that they can't find. So, we did restrict what we were doing there because I know Eclair is getting upset with us spamming them about dead stuff. At the moment, there's no way of knowing the difference either. If you've just closed the channel and you haven't spliced, you can still send channel updates. We will go: Okay, we'll just keep updating it. I mean, you should be nice and send one out saying: Disabled. In fact, that's what we will do. If we've actually shut it down, we'll send a disabled update. so that should be all you see. But yeah, it's just sort of a bit vague in the spec, and I wonder if it's going to be a problem in reality.

Speaker 3: But I mean, did y’all say that you also send a disable update during the splice, [redacted], or is that just saying for a co-op close?

Speaker 1: No, for a co-op close or a unilateral close or anything else, we will send out an update saying the channel is disabled. ‘Cause that'll hit you faster than — as soon as we enter that state, we send it out. So even before it gets mined, you'll see that. In our case, you can tell, but we haven't kind of spelled it out anywhere that you should do that. As this spreads on the network, I think we will hit more of these issues. People have seen weird gossip stuff because of it.

Speaker 0: Yeah, on the other side, we haven't worked really on the gossip part at all yet, but we have relaxed a bit — when we were screaming at you for sending channel updated that we couldn't see, we had a very low threshold for that, so we relaxed that one and made it, I think, configurable as well. So we should not scream at you that much, but that's definitely something that we need to do, and we just haven't spent time on the gossip part yet.

Speaker 1: Cool. 

Speaker 3: Yeah, I mean, also people wanna entertain it. They're still the idea of basically like having this nice splicing transaction, which maybe already is, be somewhat identifiable. So then, once you hit the chain, you know that it's probably a splice and you can reuse the anchor, or something like that. So, we have that in our back pocket. If for whatever reason blocks and p2p stuff, networking stuff — it's just not not tightly synchronized enough.

Speaker 1: Yeah, that's right. I mean, we don't have anything at the moment. One way is to have an option in the channel update to say: Hey, this is actually a splice. And you just keep setting that until — I mean, that's cheap, right? We just use a bit. But yeah, we haven't done it and we should see.

Speaker 3: Yeah, and if the same multi-sig key is used again, then that's also like a — or maybe not, okay. I think

Speaker 0: That's not the case. At least on our side, that's not the case. We do rotate the funding key for every splice.

Speaker 3: Gotcha. I see. Yeah. I guess the splices have RBF, but if you did add the anchor outputs on that, that would make it somewhat inviolable basically. But then you have extra baggage. Is it worth it just for this one hour period of time or something? Yeah, open question.

Speaker 1: Yeah.

Speaker 3: Cool. Then, as far as quiescence, we started implementation on our end. At least for kind of the mechanics, which also takes a very long-standing bug with the way we just reject co-op close if things aren't ready. So, we're kind of figuring out what that looks like code path wise on the LND side, which eventually go over to splicing and the dynamic commitment stuff. [redacted]’s recently been looking at the version of dynamic commitments we're working on again. I don't know if you have any updates on that either, [redacted]. I saw you open a PR.

Speaker 6: Yeah, I just put in a draft PR into the main bolts repo that replaces the original dynamic commitments one. It is probably gonna tweak a little bit as we finish implementation in LND, but it's close to — it's reviewable at the moment. There are specific line items in the bolt too as notes for reviewers because there are still certain things that might require discussion, but it's a very readable proposal as is. I make no claims it's perfect, but as far as I know there's nothing wrong with it. 

Speaker 3: Do you have a quick primer on how exactly it works and what it builds on?

Speaker 6: Yeah. So, this is something that I wanted to talk about maybe with the quiescence stuff a little bit, which is that we have an extra requirement right now in dynamic commitments that requires not only HTLCs to be doubly synchronized on both sides of the channel, so that both sides have fully revoked and committed all of the updates — that's the requirement for quiescence as is — but we have an additional requirement that we actually need there to be no HTLCs on the channel. So, we actually do this thing where we negotiate what the dynamic commitment target is, and then flush all the HTLCs before actually applying that. When I built this originally, I tried to make it build off of quiescence directly. But quiescence only is like: Okay, things are committed. Freeze things as is. The trouble with that is that some of the goals of dynamic commitments are to change the channel parameters, which might yield invalid states, or it might result in the fact that the commitment transaction that is current is invalid according to the newly negotiated channel parameters. While you could work around that by saying like: Okay, all future updates must converge towards the allowable space, it's gonna dramatically blow up implementation complexity. I don't think anyone here wants to deal with that. So I don't know. It is kind of on my list of things to do to see if we can make small tweaks to quiescence or add a provision that could kind of unify them. But at the moment, it does not actually use the quiescence protocol as it's because of that extra requirement of zero HTLCs, which is overly stringent, but it's overly stringent to protect the implementation complexity.

Speaker 0: Yeah. The risk is how this step happens. You never get to a state where you have zero HLC or it takes such a long time that you just lose too much on feed revenue, right?

Speaker 3: Well, isn't this the case with shutdown already, right? That stuff could just...

Speaker 0: With shutdown, you are shutting it down. It's not exactly the same. Here you are trying to create a channel, but you still want to use it, and you want to use it as soon as possible.

Speaker 3: Yeah. That's it. You're right.

Speaker 1: Well, I think it makes sense to have both. I mean, I'll take a look and see if we can do a flag and try to figure out what the semantics are. I mean, if you need to, I agree. There are some changes you do not want to make to live HTLCs. If you want to really be able to mess with some of the channel parameters. I didn't even want to try to get my head around the case of: Oh, well, that's not allowed because of this. The things that we've done so far with quiescence have not affected HTLCs. So, we've been good, and we haven't tried to change parameters dramatically. The only thing is splicing, which is much more sophisticated anyway, has that newer old rule for HTLCs, but that's okay. If you're doing something like…

Speaker 6: Yeah, the things that actually affected, like raising the dust limit would prune a whole bunch of HTLCs off of the commitment transaction. Changing the reserve requirement might yield an invalid state. Now, we already kind of have provisions for that where, obviously, if you're at a channel open or the receiver of that channel open is under their reserve limit for the initial states, but that's okay. So, there are things that we can change that essentially yield invalid commitment states, and we can't necessarily predict them. So...

Speaker 7: Is there a way that you could pre-negotiate? If that makes sense? Like, so figure out — I don't know. Maybe that's more complicated. Okay, maybe not.

Speaker 6: Well, the thing is, the way the proposal is structured right now is that all negotiation happens before the actual channel becomes unusable. So, if you can't come to an agreement, your channel can continue to operate as normal all through this. As soon as both sides have essentially acked the thing, it now kind of enters this flushing state similar to shutdown, where you can only take HTLCs off the commitment via fails or fulfills until it hits zero and then all the new constraint updates are applied. If there's a re-anchoring step, then the re-anchoring step is applied at that point too.

Speaker 0: But couldn't you just, once you reach quiescence, revoke the current state so that you don't have to deal with that invalid state. And when you sign the new one, you also sign it at the new commitment index, so that you revoke the current quiescence one so you don't have to deal with that state becoming invalid. Because you still have to deal with revoked states that will be invalid after the change anyway. so if you just revoke that one instantly…

Speaker 6: It's not about the revocation. It's that — let's say that you raise the reserve requirement and now, your channel peer is no longer above it. Now, in theory, you would just reject this at the beginning if it started that way. But if following all of the HTLC stuff, it changed. Actually, this is still a problem, even in the current proposal, I think.

Speaker 3: But yeah, I think the main thing here is it seems like we need...

Speaker 6: I'll have to think about that.

Speaker 3: Yeah, it seems like we need a bit of some sort in the STFU message that says: This is turbo STFU. Like everything is fully clear. The main thing is we could try to enumerate and make sure every single transition actually was able to map the HTLCs. It was easier just to not do that in the beginning, and I guess figure out the cases where the channel is just too high volume. Maybe you can reconnect or something like that. I'm not sure.

Speaker 0: But would this become much simpler if we did option simplified commitments? Because if you use an option simplified commitments and STFU, then instantly at the beginning, you know what is already committed and that user just need to sign back and forth. So, at the beginning, you can say: Oh we're going to have an invalid state, so I'm aborting right now.

Speaker 1: Yes, that's always true though. Yes. Self-simplified commitments make things simpler. But that's also a bigger change, right?  

Speaker 6: What I'm hearing is that there are, possibly, ways to do this without flushing HTLCs to zero. [redacted], I think that's what you're suggesting, is that there may be opportunities for that. I will go ahead and take a second look, and make sure that either that is impossible and come back with an argument for why it's impossible or do the thing.

Speaker 1: Yeah, let's see how ugly it gets.

Speaker 3: Yeah, I mean, to my knowledge, splicing is the same today. Like, you don't splice the HTLCs yet, right? Or you do?

Speaker 1: Yes, we do. We do have HTLCs in flight.

Speaker 3: Okay, alright. Nevermind. I'm wrong. Because I was curious for high volume routing nodes. Like if that is delayed a lot, but if that's not the case, then okay. That's fine.

Speaker 6: Yeah, it's just tricky with things like if you wanted to change the max HTLC value in flight constraint. You're just basically fucked if it's up above that. Now, maybe you just say: Alright. Well, the negotiation will fail if the result of the negotiation produces an invalid state?

Speaker 1: I don't think you have to. I think you just clarify it so that those constraints apply on add. So then it works, right? Yeah, sure you've got one that was weird, but that's okay, right? You handled it before. You can't get upset about it now, right? So, I think if it's really clear where the constraints apply — and at the moment, they're all defined to happen in add — so if you said: Add something, and I'm like: No, fuck off, that's fine. But I don't check again, right? I'm not gonna go back and go: Oh, but now that's weird, because it's above our max. Like no, no, no. That check happens at add time. So that one, for example, is actually pretty clean. There may be other states — I mean, the reserve state, as you say, we already hit the case where you can be below the reserve. That's kind of okay. If I agreed to increase it, then great. That's a future commitment. It's not necessarily a commitment today. We already deal with it. I don't think that's a problem. We still have the ratchet problem that I still have to let you do something that puts you below the reserve as long as it's in the right direction. But we already have that kind of logic. We will have to go through it. Obviously not in the meeting, and step through all the cases. But I suspect that we end up with — it seems like a hairball, but I think when we actually break it down, I don't think it'll actually be that bad. It would be great if we don't have to drain HTLCs because it simplifies everything and it does keep everything flowing, right?

Speaker 6: Alright. So how about for the next meeting then, I'll put an appendix in the proposal that steps through some of these cases and then y'all can look at it. I hate this. Then, we can talk about the flushing route. If you guys are like: Ah, this seems all right, then we can proceed that way.

Speaker 1: Yeah.

Speaker 3: Yeah. One other thing that we tried to pull in — I think there was an old idea, I think it was for like the early open channel like negotiation basically— so we try to have a vector to say which things are rejected and why. Or at least, we're kind of looking at either doing a full TLV or something more compact by that. Something that we're looking at on the side that maybe can be repurposed elsewhere. Cool. Alright. Next, we covered all that stuff. Taproot Channels. This is my week to do everything. I have some test vectors that I need to finalize basically to get that up, and I was finding the thing around the application messages. Now, it just ended up being part of the final feature bit basically. We'll just have a switch statement in certain places. Don't imagine it being too invasive. I haven't implemented it yet, but it's literally just removing an OP_Drop in certain places and reordering it slightly. It doesn't really change things significantly. It does change the weight estimation slightly because obviously, you have that one less op code, and some places, two. That's about it. As far as bugs, we fixed a bug in 17.1, which is something related to ignoring. Basically, the whole channel re-establish versus funding lock thing as far as when the announcements were sent. So, I think I'll probably try to clarify that a little more in the spec, just to make sure other people don't run into that, because that's the first thing that we fix. But other than that, it's been pretty smooth so far. People are using it. Private channels only, so it's not super widespread yet. But I have some, and it's nice. Co-op close works. Then on the gossip stuff, so [redacted] was out the past week or so, but is back now. I think they’ll be diving back into this. I think last time we talked about re-announcing the old channels or not, I think we were just gonna stick with just doing the new flow and then looking at what the old one looked like to see — oh, that's right. The other thing was mapping between timestamp to block height. Basically, if you wanna do that or not. I think that was the main interaction that we uncovered there as far as which one do you do, but block height's better, but time is a little bit fuzzy. But at least, I think our plan is just do the new stuff first, and then make sure the retrofit can work. Or look at what needs to be changed slightly because at least we can announce the new one.

Speaker 8: Nice. I got out of rebase hell, and I think this week is also going to be a little easier. I would just ask that I not be put back into it because I might get feisty. Hopefully going to be able to make a ton of progress, but nothing really interesting besides that because it was a lot of fighting.

Speaker 3: Okay, cool. Yeah, so we'll be ready. I guess we should think about which version we want to target [redacted] because the scripts I guess will change slightly but not heavily. I'm assuming — do you guys have the current scripts? Basically, the thing that's in the PR and not in the comments. Like the non-miniscript version?

Speaker 8: Yeah, but it's pretty easy to change, though.

Speaker 3: Yeah.

Speaker 8: I don't really care. Just you can tell me if you want me to use the newer version. That's what I'll do.

Speaker 3: Okay, yeah. I’ll probably try to at least have some branch up that we can use to do the neural processing based off of. 

Speaker 8: Okay. 

Speaker 3: Okay, sounds good.

Speaker 0: Thanks.

Speaker 3: Did that. Two errors. Just like [redacted] is back on the scene. I don't think they’re here, but we've been looking at this thing. I think [redacted] commented some updates here because I think [redacted], from Async, responded to some things around requirements. [redacted] responded, reopened it, and has a force push. 

Speaker 7: I think I have two comments on this. Not to use attributable errors yet, but at least to ignore them. So we can be in a route that uses attributable errors, even if we won't require attributable errors. So I had two comments. There is this problem of what do we do if when we forward the error, the error is actually not forwardable because it's too small. For instance, it's a legacy error. So, I think maybe we should add a new error message in the spec for this case. You said that in their implementation, they use a different method, which is to just pretend that they received just zeros. That's another possibility. The other problem is the way we signal that we support attributable errors. Sorry, not that we support it, but that we want to use it. So what [redacted] proposes is that we put inside the payload the bits that says: Please use attributable errors. But the problem is if the onion is not readable for some reason, should we use the legacy errors? Should we fall back to the legacy errors or use attributable errors by default? So a solution to that would be to put these bits to use the attributable errors, not inside the payload that's encrypted, but in the message when you add the HTLC.

Speaker 3: Interesting.

Speaker 0: If we want to relay it and re-add that flag for the next HTLC, the sender should check that everyone in the path supports it and the intermediate nodes should just relay that flag in the updated HTLC message. Is that correct? 

Speaker 8: Exactly. Yes. 

Speaker 1: But they have to understand it anyway, don't they, in order to relay it backwards correctly?

Speaker 8: Yes. Actually, they may not even have to all understand. Even if we can have like the first nodes that understand the attributable errors, then the suffix of a path that doesn't support it and that could work.

Speaker 1: But it makes sense to put it outside the — because you may not know. You set it, you send it to the first one, it won't forward it. If it doesn't understand it, it will just go: Ignore the TLV. It'll do it for you, right?

Speaker 8: You need to make sure that they support it. 

Speaker 1: Why? Oh, you're gonna send them? No. Can't you just set it, and if it does, they don't support it, then you'll get back a legacy error?

Speaker 8: Yeah. Okay. I guess that…

Speaker 1: Literally, the thing about putting it not in the onion, but putting it alongside it — like in the add HTLC message — you just set it all the time and it doesn't hurt.

Speaker 3: Yeah, because that's what a blinded path does, right? It kind of has something outside to interpret.

Speaker 8: Yeah, but I mean, you only need to put it if you received an HTLC that has it. If you forwarded an HTLC and you didn't receive it...

Speaker 1: Exactly. You wouldn't set it on one that didn't have it, but you will clear it if you don't understand it. That's natural behavior. So I think that's actually kind of nice from an implementation point of view. You'll just set it on everything. To start with, no one will support it, and it'll just be clear all the time.

Speaker 8: Yeah. So, that's it. Apart from that, I think the proposal is quite good as it currently stands. The implementation is almost ready on our side. We just need to clarify these small points, and review it.

Speaker 3: Okay, cool. Yeah, and I can make [redacted] to get some interop testing going as well. I think we're looking at getting some basic versions in 0.18, which would be like our next major. We just did one a few weeks ago. So, yeah.

Speaker 0: Okay, so you'll have some support in master or in a branch that we can test against?

Speaker 3: Yes, it's in a branch. It probably needs a rebase, but it's there, and it works, at least, LND to LND. But I can try to find exactly where that is.

Speaker 0: Okay, cool.

Speaker 3: Yeah, there's a branch. Okay, and I can link it in the notes too. Cool. That's it. I guess now this is everything else.

Speaker 0: Yeah, I think [redacted] had a question about liquidity ads and maybe making it a blip or updating it.

Speaker 7: Yeah, I can weigh in. So now that dual funding is almost over the line, which is very exciting, I've kind of turned my focus back to getting the dual liquidity ad spec updated and kind of rebased on top of the existing funding implementation. Like spec stuff. One of the big changes we're gonna make to the current spec is — this is my kind of a minor thing — going from CSVs to CLTVs, which I think works really well. It means kind of a little less work in terms of the protocol messages that are required for that. The other question that I had — I think [redacted] and I were kind of talking about this offline a little bit — is whether the ads is part of the bulk specification, or if we should submit it as a blip. I think both of us are a little agnostic in terms of where it should go. But in terms of it's currently written as a bolt update, et cetera. Ideally, it is a standard that everyone supports on top of full funding such that everyone is able to participate in liquidity market. But I don't know. [redacted] thought it was a good idea to turn it over to the wider spec committee just to see if there were strong opinions either way. Is that correct, [redacted]? Did I characterize that correctly?

Speaker 0:  Yep, perfect.

Speaker 7: Cool. Great, okay, Sounds like everyone is about the same where we are with that one. So, we'll just continue with how it is and see where we go with that. Cool.

Speaker 1: Yes. I want to see what it looks like with CLTV. I mean, CSV thing was a cute hack, but for minimal change, but maybe it'll be nice. 

Speaker 3: We do a CLTV thing too. We have a channel type that just basically has the extra delay and we ended up doing the CLTV. It wasn't too bad. We haven't updated it for taproot channel and stuff yet because it was just different. The only thing is you have a drift before it confirms. So, if it takes three days to confirm, that eats into it, and that's the main trade-off there.

Speaker 7: Yeah, so I thought through this. For the liquidity-ad particular case, I think that's totally fine because the person who pays for the fees is the one who is getting liquidity. So, you would think that they're incentivized to pay appropriately. If the one who's opening the channel is the one who's going to be receiving the service, if that makes sense, of the additional liquidity, so it's in their favor for that transaction to get confirmed. So, if they decide to make it lower, then basically they're eating at their own CLTV, right? Because that block wasn't a benefit for them. So if we don't pay enough to get it confirmed in a timely manner, then they're basically losing out on the CLTV time anyway. I think in this particular use case, it's totally fine. If you guys have a draft of the CLTV that you guys added to the commitment transaction somewhere, it might be useful to use that and converge, if that makes sense. So we do the same thing. If you have some drafts somewhere written up, I would love to incorporate it. 

Speaker 3: Cool. Yeah, I think we have a write up somewhere. On the side, I feel like the final thing that's sort of semi on top tier is the whole fees thing. Because I think Magma does a thing where they'll say you're bad if you change the fees. I think the only way you could actually do it is to have fee updates to be signed by both parties. Then, you could have the other party reject. But other than that…

Speaker 6:  So, I was actually talking about this with [redacted], [redacted], and a couple other people here last night. I think the way that the spec is written currently, we're basically doing what amounts to a fraud proof. You get a signed signature from the selling party, the person selling you liquidity, at the time of creating the transaction. It has their signature on it, and it says that they're committing to keeping their fee rate within a certain band. Then, at any point, if they sign a channel update from their node during that period that the lease is for, you have two pieces that are signed by them that conflict with each other. So, we don't have a process right now for adjudicating fraud proofs, but the spec includes them, and it's part of the currently implemented spec that Correlating has, which is pretty cool. Anyways, so like..

Speaker 6: It's not hard to set up a service provider to ingest those things and publish them out.

Speaker 7: Yeah, exactly. I think the cool thing is we're currently basically building fraud proofs already, so we wouldn't need to change anything about gossip or how channel updates happen because you would get both pieces that you would need to prove to anyone, any third party, that they violated a contract they had signed, which I think is cool. The only thing I would really want to like double-check, or confirm, is that the block times are in those, so you can verify that the signatures or the timestamps so that if you have the two pieces, you can check that like the gossip update occurred in a time period or the email update occurred in a time period when they said they wouldn't. The only thing I think we'd want to double-check is this fact. But otherwise, I think it's pretty cool to have properties built into the spec.

Speaker 3: Yeah.

Speaker 1: In that case, for proof, it's the same thing as another topic we discussed on the mailing list — that if this is a private channel and you're using SCID alias, the only channel updates that you will get are for your alias. So you don't have a mapping from that to the actual on-chain output. You need the liquidity provider to also sign the channel update that uses the real SCID and not only the SCID alias. Otherwise, you cannot prove the link between that channel update and the actual channel.

Speaker 7: Okay, that's good to know, and maybe work for. I think one of the cool things about this fraud proof is maybe we could talk to Magma to ingest it. If you have a problem, you can send them the fraud proof and then, we'll incorporate it in there or whatever. I mean, that's a thought. But, yeah. That's all I had on that. I'm excited about it. I think it's a really cool spec, and I'm excited to update it. so it's a little less of a burden. The current implementation, I think, takes a little more work than is necessary, and the big CLTV people really fix that, which is cool.

Speaker 3: Cool. Anything else? I just posted my notes. Okay, if that's it, I'll hit stop record.

