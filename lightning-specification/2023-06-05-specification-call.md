---
title: Lightning Specification Meeting - Agenda 1085
transcript_by: Gurwinder Sahota via TBTBTC v1.0.0
tags: ['lightning']
date: 2023-06-05
---

Agenda: <https://github.com/lightning/bolts/issues/1085>

Speaker 0: Alright, so let's start. So, the first PR on the list is one we've already discussed last week. It just needs someone from another team, either Lightning Labs or LDK to hack. It's just a clarification on Bolt 8. So, I don't think it should be reviewed right now because just takes time to work through it and verify that it matches your implementation. But if someone on either of those teams can add it to their to-do list, hack it, and then we can merge it. Then, the next one for which we have a lot of discussions happening, is allowing an HTLC receiver to dip into the channel reserve 1083. So, this is kind of reviving the issue we had with stuck channels a while ago because when the initiator had a balance that was getting dangerously close to its reserve, it was not able to actually add new HTLCs to the commitment transaction because it put deep into the reserve and channels were blocked with all of the liquidity on the non-initiator side. This was an issue. We added a buffer to make sure that this doesn't happen realistically. In practice, it works quite well, but splicing make us go back into that situation because with splicing, the initiator can end up being below the new reserve since the reserve is a dynamic - is 1% of the total channel size. So, when the non-initiator splices some funds in, then you can end up with the initiator being below their reserve. And you still want the non-initiator to be able to send HTLCs, so that the initiator goes back towards meeting its reserve eventually. So, how should we do that? My proposal was to, on the sender side, when you're not the initiator, to just below sending that HTLC, because you are actually letting the initiator dip into its channel reserve, but it's actually already dipped into its channel reserve because of a splice. If you only send one outgoing HTLC and wait for it to resolve, you control how much extra risk you're taking, but it is still an extra risk. It depends on the way you look at it. In the specification, this is the sentence I'm changing is more general than that, and there was a lot of good feedback from [Redacted] saying that instead of doing that - if it's only for spacing that it's really happening, and it's true that in practice, it's only for spacing that this is really gonna happen - we can just keep tracking the old reserve until the new one is met, which is a bit more tracking work, but I'm fine with that as well. If people really don't want to add something to the spec that gets the sender deep into the channel reserve. So I don't know if [Redacted], you had time to look at my latest comment.

Speaker 1: I didn't, but I'm still a little confused by this because what you're going to set it - as far as I understand what you're in essence doing is just increasing that buffer by one HTLC or whatever. You're not actually solving the problem because there's still cases where someone can run a bunch of HTLCs at once. Like, if both sides push 400 at once, you still have the same problem. Either that or you just let them go all the way down.

Speaker 0: No, that cannot happen because the initiator is still not allowed to dip into that reserve. So, the initiator cannot add new HTLCs once they reach the reserve, but you're only allowing the non-initiator.

Speaker 1: But, the whole problem with this was that things happen at the same time, right? So, both nodes send 400 HTLCs at the same time. The initiator sends some number of HTLCs to put the non-initiator right at their channel reserve. And then, the non-initiator, at the same time, sends the same number of HTLCs to dip into the channel reserve by that number of HTLCs. And I just don't think we can - you haven't actually solved the problem unless you want to let them put 400 HTLCs worth of fees out of the channel reserve, which I don't think we should do.

Speaker 0: Okay. Yes, so the issue, what you say in a sense, is that when the non-initiator cannot know that they're in the situation where they should add only one HTLC because they are taking extra risk because the initiator is concurrently adding other HTLCs, which increases the size of the transaction. Okay, that makes sense.

Speaker 1: The whole issue is concurrency. If we want to solve the - so I didn't - I had missed the context. This was also for splicing, and I agree with [Redacted] that we should solve the splicing case by just tracking it. If we're worried about the race condition still - which I don't have any numbers on how often it actually happens and we should get numbers - we're worried about it, but I think we should just do the old RESTU proposal and just do updates one direction at a time.

Speaker 0: Okay, I think we'll eventually do that, but I think we will get splicing before that. So, I want a solution that happens before we actually rework the commitment update scheme. So yes, I guess I'll go then with closing that PR, and just adding to the splice spec PR one note that you should keep tracking the old reserve requirement until the new one is met; and that I think that should solve it. Alright then. That sounds good to me and it sounds like it's what [Redacted] asked as well. So I'll just take it to the splice spec PR. So, next step is CLTV handling in blinding paths.

Speaker 1: Yeah, that's on me. I still haven't done anything. I was traveling a bunch the last week. I promise I will do it this week. Okay. I don't think we're in any rush for it right?

Speaker 0: Yeah, no. If we want to actually change things, maybe - before it starts getting used. But in my last comment last week, I created a gist with explanation and details and examples. So I'll let you go through it. Basically, I think that what the spec is currently saying is correct. It works, at least, it looks like it works as I expected. It lets the sender add a random number of nodes if they want to. So, I think what the spec currently does is okay, but we need to make sure of that.

Speaker 1: To be clear, I have no desire to change anything. I'm happy to describe what people already do. It might or might not be the cleanest possible outcome, but it doesn't really matter. I just want to have to describe what people do.

Speaker 0: Okay then. Anyone should just have a look at the gist I put in the comment, and see if it seems to make sense or if I missed something. And I think other pairs of eyes would be really helpful. Now, I'll put the link here, but it takes some time. You should grab some coffee and spend, at least, half an hour on that to make sure that it makes sense. So yeah, we'll keep tracking that directly on the PR. Nothing more to do on that one. So, the next step, [Redacted] added a PR to harmonize the max HTLC expiry across implementations, if I understood correctly?

Speaker 1: Yeah, that basically we're out of - like you wanted to increase the amount that we were defaulting to four days or something. And my response was basically: There's no way other nodes are actually going to keep routing through us if we do that. So, I don't know that we need to actually write it.

Speaker 0: You mean selecting you in pathfinding or allowing to relay HTLCs at intermediate nodes?

Speaker 1: The one that we announce - i.e. the one that we put in their channel update and tell people you have to add at least this delta. I don't know that there's a reason to put it in the bolts necessarily, but there should be some way for everyone to be on the same page in terms of what their route finding limits are. Basically, it really is a question of like how high can we set it before people start not running through us.

Speaker 0: Yeah, I agree. I think this is an issue because we mainly started way too low. Initially, years ago, people tended to put low CLTVX by read-down-time because HTLC tended to get stuck because of bugs, and it was really annoying if they were stuck for too long. It's not happening that much. It can still happen in the malicious case. So, that's why we don't want to infinite numbers there either. But, what's the right balance? Yeah, I don't know. But here, the value that [Redacted] wants to set is when we are an intermediate node, the difference between the nlock time of HTLC and the current block height, right?

Speaker 1: Oh, I don't see why that needs to be. I mean, I guess that could be specified too. But I mean, that's probably just, at least, the delta. So, it doesn't really matter, right?

Speaker 0: Yeah, because I think it makes sense, because for example, we're changing Internet Eclair to this value to be 2016 blocks like others because we're starting to see that everyone is raising their CL to be expired delta. But we were, before that, at 1008, which means that if someone selected a route that exceeded 1008, we just would not accept to relay that, and people have no way of knowing that, which is bad. So, we need a high enough number here, but this is also...

Speaker 1: It is different, right? So, delta from the current block height to future block height to the CLTB for an intermediate node is different from the CLTB delta, right?

Speaker 0: Yeah, but they actually matter because if you select my node in a route that has further down the path an LDK node that uses a HTLC with 400 blocks, then the delta between the current block and the end of time in my HTLC is going to be big, and I'm still going to reject that HTLC instead of relaying it.

Speaker 1: Oh, right. Yes, I wonder if we should just specify then. That nodes have to have a delta from the current height that's equal to or greater than the delta announced in the channel update?

Speaker 0: Yeah, it will be. But the thing is, it has to take into account other channels further down the road that you don't know about. Oh, you mean in our channel?

Speaker 1: Oh, you mean the too far away thing, not the - oh, yeah. Sorry, I had the direction confused. Yeah, I don't see a reason why not to just - I mean, I guess we should set that, but I'm less concerned about that. More concerned about the total CLTV delta to begin with.

Speaker 0: Okay. I don't think we actually have a rest friction here. We just slightly penalize - at least, in Eclair - we just slightly penalize longer deltas, but that's customizable. And I think our default is to actually not penalize that much. And now...

Speaker 1: I think that someone dug in the LND and concluded that they do the same. I, kind of, be concerned about that though. Like, it's too low. I assume you also have a separate check for it can't go over some threshold. I think we're gonna move - or well, I intend to and probably won't ever get around to writing the code to just saying that there's a limit per hop. It's not really - users might care about the total, but it's kind of awkward in Dijkstra to have a total limit that you randomly hit at some point, even if you penalize in your scoring, so you might just have a hard limit per hop anyway.

Speaker 0: Yeah, okay I see. So yeah, probably let [Redacted] chime in on that PR, and we'll follow up later on that one. Alright. So then, if [Redacted] is not here, I don't know if we have anything to add on onion messages or authors. Anyone has something to add or should we just move on to the PRs?

Speaker 2: About the test vectors, they essentially are bech 32 encoding and different line continuations. But, there really isn't anything about: Are these TLVs semantically correct? I'm not sure if that is intended or we want to expand on those.

Speaker 0: No, I think it's just that [Redacted] needs to update them and expand them, but just didn't have the time to do so. So, I think your point from last meeting still stands that the test vectors need some love.

Speaker 2: Well yeah, my point was more about they had old fields, like recurrences. But I didn't really push on the fact that they weren't really expansive. But yeah, maybe I should. I'll add a comment to the PR.

Speaker 0: Okay, and I think we'll just follow that there. I think the next step is first to merge the onion messages, so that the files is going to be based directly on master. It's going to be a bit easier to handle all the comments and rebases. Alright, so next up, dust exposure threshold. It still needs some love if someone can spend some time to review the latest state of the PR and either hack it or make comments on it to see what we need to change to actually merge that because that's something we already implemented. So, it really makes sense to have it in the spec, in my opinion. But yeah, so people, add it to your to-do list. Then, do we have something new about taproot and taproot gossip?

Speaker 1: Sounds like we're just gonna boot that to New York since [Redacted] never - Wait, is [Redacted] here? No. Since [Redacted] never got around to starting a mailing list thread, and the mailing list is now filled with spam. Before we move on - I know there was some conversation about the taproot spec itself, not the gossip. I know [Redacted] and [Redacted] and [Redacted] were going back and forth on that. I don't know what the state of that is, and [Redacted] not even here, so I'm not sure it's worth taking too much into.

Speaker 3: Yeah, it's not worth it. You can just table it for next time.

Speaker 0: Okay, and does anyone have some news about when we can expect to have a musig2 in lib-secp and not the lib-secp-ZKP? No news on that.

Speaker 3: In ZKP or in the upstream, like the official Bitcoin Core one?

Speaker 0: Yeah, I thought in the long run they agreed that they would once it would be stabilized that they would add it to lib-secp, but I don't know the state of that. We were kind of waiting on that one to get started on taproot.

Speaker 4: I was chatting with [Redacted] recently. I may be mistaken, but I think there is some opposition to adding musig, at least, in the near term, because of wanting to do constant time operations on some stuff that's not currently supported.

Speaker 1: We can get it in ZKP sooner, right? So, it's not really a huge deal.

Speaker 4: Well, it's in ZKP already.

Speaker 1: Okay. Some people should just use ZKP.

Speaker 0: Yeah, okay. So, we consider using ZKP then. Okay, and about taproot gossip, is there something to add or open questions that could be resolved?

Speaker 1: Looks like neither [Redacted] nor [Redacted] are here, so probably not.

Speaker 0: Yep, alright. Can I put in a sentence for splicing? I think, also only for Blockstreamers. So, I'm not sure we are going to be able to do much tonight. Internal reestablish, but else? BTS, dual funding. I don't know if there's some feedback on dual funding, if there's been progress on the LDK side or LND side.

Speaker 1: I don't know if [Redacted]'s here, but [Redacted] started doing some amount of work implementing the dual funding flow. It's still a little early, and we have to do some internal refactors first, but there will likely be something to look at in New York. Probably not merged, but at least something that might be - maybe I shouldn't speak for [Redacted], but something that might be worth trying to do, testing on in the art.

Speaker 0: Okay, cool. Yeah, then I don't have anything else that I wanted to cover specifically. So, if anyone has anything that they want to cover, just now is the time.

Speaker 1: The mailing list went back on moderation. I don't know if it's worth talking about that in any form. Obviously, there's some garbage spam, but just figured I'd mention it.

Speaker 0: Yeah, and there hasn't been a lot of volume on the mailing list, and there's nothing that has been added since then. So, I think we can handle the moderation manually. We're enough moderators right now. So that sounds good. Yeah, anything else interesting that has happened in the last two weeks in either your implementation or something else?

Speaker 1: Not really. I mean, I did want to - I don't know if it's worth talking about, but we're going to have to make a decision soon on whether or not to do that early failure back of HTLCs. Like if you forwarded an HTLC and you had to force close the outbound edge channel and the force closer commitment transaction or the HTLC timeout have not yet confirmed - do you fail back the inbound edge? We haven't had an LDK discussion about it yet, but we probably will next Monday at our meeting. But if anyone else has opinions for whether or not they're going to do a similar thing. I would love to hear thoughts.

Speaker 0: Yeah, we've been doing it forever in Eclair, and I know that [Redacted] agreed to that. You agree.

Speaker 1: You say, didn't you say you only did it after the commitment transaction confirmed?

Speaker 0: Yeah. Right.

Speaker 1: Right. So, I'd also be interested in whether you would change that too.

Speaker 0: Yeah, I don't know. Because yeah, we're aggressively trying to get the commitment transaction to confirm.

Speaker 1: Yeah, it may just be kind of a more of a pre-anchor issue. I'm not sure. I know that this was, I think, the biggest issue. My estimates were that this was, by far, the biggest issue for force closures, or at least easily avoidable issue for force closures when the fees were rapidly going up. Again, this might have been more of a pre-anchor channel issues, but I think it was the biggest issue, so I don't know.

Speaker 0: Okay. Yeah. I need to think about it and to see if we add that for the case of a commitment transaction is that confirmed. I know that [Redacted] created an issue on the CRN and indicating that they wanted to do something like that, but they didn't specify whether they would do it also if a commitment transaction wasn't confirmed or need the case where the HTLC timeout wasn't confirmed. I'm not sure.

Speaker 1: Yeah. I'm trying to think of what other force closures there were. Is the LND bug, which they've now fixed and I don't know if they've done a release yet. So, make sure your peers are running LND 16.3 if you have LND peers.

Speaker 0: It's probably going to help and we turned on ignoring internal errors from LND. So, that's going to help as well.

Speaker 1: Oh really? I don't know that I've seen internal errors causing force closes on recent versions of LND.

Speaker 0: We've seen people reporting that they received such errors and Eclair was actually first closing when it received an error. So, we had a few people...

Speaker 1: Yeah, you're supposed to first close when you receive an error.

Speaker 0: Yeah, but we had too many reports of people being affected by that. Mostly, one guy who was playing a lot with rebalancing tools and making a lot of HTLCs, so I think he was hitting a lot of edge cases on his peers, so he was probably hitting most of the LND bugs when he was trying to push the limits. A lot of his channels eventually forced closed, and he lost a lot of money on that.

Speaker 1: So, that sounds like a him issue rather than something to work around.

Speaker 0: Yeah, I agree as well.

Speaker 1: I mean, they did have that bug a while back where they were treating warnings as errors. But I think they fixed that a while back. That might have been a year ago now.

Speaker 0: Yeah, I haven't seen that reported. So, apart from that maybe we'll discuss it more in...

Speaker 1: Oh, I was going to mention one other force closure case. I was trying to remember what it was. So, one question is: If you forwarded an HTLC and it's been tossed on both the inbound and outbound edge, does it make sense to have a feature bit to say: I'm not going to foreclose on that? And if your inbound edge has set that feature bit, then don't foreclose. It's tricky to get right because fee rates can change. So, maybe you only do it for anchors or for very, very small HTLCs that are going to remain dust. But, it's kind of weird that we'd like to not force close if we have an outbound dust HTLC that's expired - because why would we force close that - but the inbound edge is going to force close the node that sent the HTLC to us, so we have to. So, would people be open to some kind of feature bit saying: This HTLC is less than, I don't know, whatever, 100 sats, - like, just a feature bit saying: I will not force close on an HTLC less than 100 sats. And you might have to set that in the update at HTLC because it has to propagate all the way down the route. I don't know.

Speaker 0: Aren't we going through a lot of effort instead of fixing the root cause that there's just no reason that this HTLC is not failed back?

Speaker 1: Well, I mean, yeah, it might just be that your peers offline, right?

Speaker 0: Yeah, but should your peers stay offline for hours?

Speaker 1: Well, if you're restarting an LND node, yes.

Speaker 0: Yeah, but that's crazy. That's what should be fixed. Restarting an LND node will take ages. It will take minutes to restart.

Speaker 1: I agree. But anyway, it was just a thought because I thought we'll just stop force closing and then realized, of course, you can't do that because the inbound edge will also force close. So, you're right, it's probably way too much effort, but it's gross.

Speaker 0: Maybe not if it's a good short-term solution, so that...

Speaker 1: Yeah, I mean, I think it's one of those things where it's like, if we were redesigning everything today, we would set some floor and say: No one will ever force close under 100 sats or something. But is it worth the effort to add that now? Probably not so much.

Speaker 0: It's mostly that if you're, how much of those force causes would actually be avoided by that because if one of the peer is not failing these dust HTLCs, are there also non-dust HTLCs that are not failed and should be failed, which will make you force close anyway?

Speaker 1: Right. It's more a question of what is the proportion of HTLCs that are under this threshold, where you would just outright not fail because you wouldn't force close because all your HTLCs are under the threshold.

Speaker 0: Yeah, let's discuss that one in New York, and see if we really want to do something about it. By the way, I'm really ashamed because I'm looking at the picture I took from the last summit about our probing protection protocol - the Oakland protocol - and I'm reminded that I said I would implement it. It's been a year and it still has not been implemented on my side. I don't know if anyone else will look at it.

Speaker 1: If you implement it, you'll get a nice little bump in whether LDK prefers to route through you.

Speaker 0: But I actually implemented the part that we set the max HTLC in flight to 45% of the capacity, I think, by default. But they did not implement the other thing about artificially reducing the capacity of other channels, of parallel channels, to avoid people tracking HTLCs. And that's the interesting part, I think.

Speaker 1: What was the other part? No, I thought it was just that.

Speaker 0: No, what we had on the whiteboard is to first reduce your max HTLC in flight, then have a 50 milliseconds commit sign timer to actually batch some stuff, and then put a full ceiling on the actually max HTLC in flight. Whenever you send an HTLC through one channel, you choose two of our random outgoing channels, and you reduce dust ceiling for, we said, 200 to 1000 milliseconds to make sure that people probing and trying to send through various channels cannot actually track where the HTLCs are going. By looking at what HTLCs are succeeding. Yeah, I don't remember the exact details.

Speaker 1: You also create a fake secondary HTLC on another channel. Was that the...?

Speaker 0: Yeah.

Speaker 1: Oh, yeah. We never did that either.

Speaker 0: Yeah. And I've kept that directly under my nose in one of the screenshots. I put under my nose, so that I look at it almost every day, but then I still haven't implemented it.

Speaker 1: Well, first fix force closes, and then we'll...

Speaker 0: Yeah, it wasn't really a priority. We have too many other things. Alright. If there's nothing else, maybe we can end early tonight. Perfect. So, I'm not sure if we - are we going to do the meeting in two weeks or should we just wait for New York?

Speaker 1: Let's do the meeting in two weeks just in case there's something that we want to talk about before New York. Like, if we want to have any discussions about topic ideas or pre-discussions or whatever.

Speaker 0: Alright, that'll create the tracking issue. Alright then. Thanks guys, and see you next time.
