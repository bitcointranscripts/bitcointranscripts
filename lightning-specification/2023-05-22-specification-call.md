---
title: Lightning Specification Meeting - Agenda 1082
transcript_by: Gurwinder Sahota via TBTBTC v1.0.0
tags: ['lightning']
date: 2023-05-22
---

Agenda: <https://github.com/lightning/bolts/issues/1082>

Speaker 1: So, the first PR we have on the list is a clarification on Bolt 8 by [Redacted]. It looks like, if I understand correctly, someone tried to reimplement Bolt 8 and got it wrong, and it's only clarifications. Is that correct?

Speaker 2: Yes. So LN message - a JavaScript library that speaks to nodes - had everything right except for the fact they shared a chaining key, which is correct to start with. They start at the same value, but there's actually a separate one. And the spec was not really clear. And so, of course, it worked for the first 500 or so messages, and then it failed. So, I thought given that we have an implementation that actually failed and when I looked back at the spec and went: OK, I think I see how they made that mistake. So, it just clarifies there are two separate keys: one for see, one for send.

Speaker 1: Did they have a look at your PR, and did they say that it was indeed clarifying the issues they had?

Speaker 2: No, I will ask them to look. I actually found a bug in the LN message with [Redacted]. So, they didn't have to go back to first principles.

Speaker 1: Alright. So, I think it's quite simple. Maybe someone from LND or LDK can have a look as well and hack it if it looks like it matches what they've implemented. That would be great. But probably not to do right now, but maybe when people have a bit of time. I realize that the next topic is the CLTV deltas for rad blinding. We discussed it last time, but I really didn't have time to do what I said I would do before this meeting. So, both [Redacted] and I have to write some clarification on what we mean, so I don't think we have anything.

Speaker 0: Yeah, I've been traveling a bunch, so I have not had a chance to do that.

Speaker 1: Yeah, me neither. I'll do it this week so that next time, we can actually really discuss that. So, let's keep it for today. Next up is Onion Messages, and I think we're ready to merge Onion Messages. Is there anything outstanding?

Speaker 2: No, I agree.

Speaker 1: Yeah, I think we can just squash the two fix up commits. Maybe if we have an act from one of our team, LND or LDK, to make sure that we didn't miss anything, then I think we should be ready to go. Which means that offers will finally be based on master, which means that offer is next. On the LND and LDK side, is there anything? I guess the implementations are complete on both implementations, so it's just a matter of verifying the test vectors. Can someone from one of the teams chime in? Oh, but there is, I think, a test vector.

Speaker 3: Oh, sorry, I mean we need to implement them on the LDK side.

Speaker 1: Okay. Is it something you plan on doing soon? Or would you have time to do it before the next meeting?

Speaker 3: Let me comment on the PR in the next day about that. But yes, love to. But we've done interop testing. So that's good. Pretty confident.

Speaker 1: Perfect. Alright. Anything else on Onion Messages or should we move on to others? Anything new on the other side?

Speaker 2: No, just minor clean-out, rebasing, things like that. There was a requirement to update the test vectors, but I'm trying to figure out if I've actually pushed that or not.

Speaker 4: I could check the current vectors versus what we have to see if anything has changed. If you want, we could review. I also noticed today the invoice error message has a couple of fields that aren't really well-defined as far as reading goes. It's basically the, I think, erroneous or suggested value in erroneous field. Maybe it's something like that. And there's some rationale about for these offerless invoice requests. Maybe we need this, but it seems we should just drop those fields entirely until we have something concrete to work with, and maybe just have an error message in that.

Speaker 2: Yeah, I mean, they're completely informational fields at this point. I mean, we did make this mistake with our general errors where we don't you get an error back, but it's just a text message. It doesn't say exactly what it's complaining about. So, this is basically the same thing left forward. They're optional for an implementation, and you can you can ignore them anyway. But they are kind of useful. Like say, this is the field that I didn't like, and optionally, here's a better; here's what I expected in this field; or here's like the minimum I expected or something like that. But they are, by definition, a little bit vague. And certainly, I'll just check that there are odd fields, but it's easy to...

Speaker 5: So, the idea is to add structured errors to onion message offers error replies, basically?

Speaker 2: Yeah, if they ask for an invoice or something and there's an error with it - as well as having a string saying: Hey, here's what I didn't like - you can actually specify because it's a TLV, right? Unless it's grossly malformed, like you have a field number. So, you can give some programmatic feedback, say this is the field I don't like, which is something we want to do in like normal error messages. But yeah.

Speaker 0: How is the sender expected to handle that, right? If you say like: Hey, your TLV field 42 is bad. Is the sender expected to have some kind of programmatic response to say like: Oh, I can decrease 42?

Speaker 2: Not necessarily. I mean, it's more a debugging aid. There is only case where it is useful; it's when you have basically a currency conversion issue. So, if your offer is in a currency that is not Sats, then you end up, there are cases where you will send an invoice and it will go: That's not enough. Right? Or you will send an offer to pay kind of thing. So, there was a corner case there where it's like: Okay, well, it's nice to have a programmatic way to say, here's the number I expected for this. But it's really a corner case that isn't particularly important at the moment. It's more debugging aid to say: Hey, this is, you know, this is what went wrong in some systemic way. But it does open the door to the idea that we could do something smarter in future. Probably working around bugs and implementations really. Oh, I don't know what this error message means and stuff like that. But it's optional.

Speaker 5: I like it. Yeah, this means LND won't send internal error. So, it can give you some more detail.

Speaker 2: So ideally you can complain about what's wrong. It seemed elementary, but yeah. Almost by definition, it's ill-defined because errors almost always shouldn't happen.

Speaker 4: I guess the idea is that we're gonna make this very general. Still like it is now and not have very specific types of errors in the future. That's the idea.

Speaker 2: That's right. Yeah, I expect that we'll tighten this as we go, right? If there's some really useful feel for it, we'll start tightening the requirements. But for now, it's like just: Yeah, optionally fill this in; it gives us a clue.

Speaker 1: Also, I'm curious what you guys are currently doing when you get an offer. Are you directly connecting to the introduction point of the blended path or to the offer node or are you doing pathfinding to reach that first node?

Speaker 2: We pathfind, but we currently only don't support MPP when we have the - in that case, which is really dumb. Like it's a minimal possible implementation. We're working on this new pay plugin that does all the [Redacted] stuff, and that will solve that problem a lot more nicely.

Speaker 1: Okay, because we started doing that. We wanted to just reuse our pathfinding code, and we realized that there are a few edge cases because if you do a simple Dijkstra, the issue is that some channels are potentially disabled in one direction if the channel is empty whereas there's still a connection between those two. So, you still want to have that edge in your graph and be able to use it for Onion Messages because you don't think that the channel is actually empty. So, we were not sure how much we should change Dijkstra pathfinding to fit Onion Messages better or if you should implement something quite different. So, that's why I was curious to know what other people did.

Speaker 0: Yeah, we haven't landed it yet to do pathfinding, but we're just doing an entirely new Dijkstra implementation because this one can be so much more naive, right? Our existing router has so much logic around like: Oh, we hit HTLC min or max or blah blah blah. So, we're just doing a: Here's a straight line Dijkstra copied out of a textbook.

Speaker 2: So, we just plug in a really dumb evaluation function and it just works, right?

Speaker 5: I think the edit disabled thing could be a hint at least, because that could be a hint for the PR just being presently offline, which maybe you want to avoid because then that is another round trip for you to retry or something like that. But yeah, there probably isn't as much overlap, but some things can be helpful, I think, on the routing policy layer at least.

Speaker 1: I think that as well. For example, people who have been around for a while - channels that have that have existed for a long time - indicate that the peers are mostly online, and maybe you want to take that edge on onion messages as well. So, those are the things that make it potentially useful to reuse some of the pathfinding code and heuristics.

Speaker 5: It already has the history, so you can use that too: Okay, they forwarded five minutes ago at least.

Speaker 2: The other thing is using the fact that you're probably gonna make a payment after this, right? If you're requesting an invoice, right? So, it's a free probe. You might as well use something similar to what you're going to use for the payment. I mean, you don't know necessarily quite what the payment size is, but at least you can come up with some vague idea. And then, you can get an idea of if any of it's down, you find out early. But we're not that smart. We just do: I need to try that. If that fails, if we can't find a route, we then redirect connect. What we could do is connect to a neighbor that forwards onion messages, but we don't do that yet.

Speaker 1: Alright. Okay. Anything else on the files?

Speaker 4: The test vector. The first one in format string test, [Redacted], I believe is not valid. Looks like it needs to be updated.

Speaker 2: Okay, yes, I had an update. I'm not sure I pushed it. I will put that on my to-do today.

Speaker 4: Okay, thanks.

Speaker 1: Alright, so next step is to do the dust exposure threshold PR. So, it's on everyone's to-do list. So, maybe someday we'll have time to review it.

Speaker 5: Yeah, this is on the to-do list, but I was thinking about some stuff earlier this week because we had some reports around things, like force closes. I think there were some, but I think they also also sting harder because fees will be higher. So, something you didn't know before now maybe costs you some money. But I was thinking, I remember in the past, I think we were discussing basically adding another value to track the dust slots. So, a dust is into 483. The only thing I was looking at doing, because remember in the past, we tried to do this thing where we basically we would only go to chain if it made sense as far as you're getting enough fees out of it. Basically, factoring the chain cost or economic chain close. Then, we ended up abandoning that because we were like: Okay, well, we would hold onto the incoming HTLC. Which doesn't make sense, right? But then, I wanted to do another version that basically said: Okay, the idea is that, let's say I have a 100 HTLC, and it's about to expire, right? I would basically, potentially, go to chain for that. Instead, a prototype would be basically we just cancel it back in the incoming and hold onto the outgoing, right? So effectively, we're potentially holding onto the bag for that cost, but we've at least freed up the HTLC on the incoming link. In the future, maybe the outgoing one comes online, actually cancels it back, but that's fine because we're saying: Okay, losing 100 HLC is better than losing 5k SATs on chain. I remember there's some questions around: Is this a spectrum pad or whatever else? But basically, the idea is that you don't necessarily go to on-chain for dust, but you're potentially committing to losing that value in the future. Obviously, the trade-off here is that this does take up one of your 483 slots, but if there was another slot for dust, it wouldn't necessarily do that. But this is just something we're looking at because it doesn't really make sense to go to chain for that thing. Particularly because as soon as you go to chain, you can cancel it back, but still: Is it worth the opportunity cost basically of paying 10k sats to get a one sat fee? I know this is something that I think [Redacted] wanted to talk about in the spec meeting around that. But it seems like a strategy that you can do today - that you need some parameters on your risk model, basically around like how many you want to keep alive, what point do you go to chamber or else - but this can at least save some pain in the short term potentially.

Speaker 0: That's something we haven't had many discussions about it, but we intend to have discussions about too. I mean, I think everyone at this point has that kind of max dust exposure tracking, right? So you only accept up to some amount of dust. The other thing you can do is just say: Alright, I've hit my max dust exposure. I should have force closed, but this doesn't make sense, and so I'm just gonna sit here and not accept any more dust HTLCs, but the channel is otherwise useful.

Speaker 5: That's one thing as well. You can have virtual queuing or buckets basically.

Speaker 0: Well, everyone already does, right? This doesn't require a change aside from just not force closing. You already won't accept any more dust HTLCs because you already have a dust exposure limit built out. So, that's kind of the easy way to fix this. Just say: Screw it. If the peer is being dumb, we'll print errors all the time and just no longer accept dust HTLCs on this channel and max out.

Speaker 2: Yeah. I was thinking more that we might go for a probabilistic model, where your chance of closing is, you haven't got a zero chance of closing. So you can't always be cheated. But your probability of closing over some thing depends on the ratio between how much it's going to cost you and how much you're gonna you're risk losing, right? So, if it's dust and fees are high, your chance of closing is really low, even though it's bogus. And as it approaches one as you start to risk more than you're risking in fees. That's a bit less of a: Here's your free amount here. If you can easily calculate how much you can cheat, I worried that people are gonna start doing that. But the theory is that...

Speaker 5: Cheat how?

Speaker 2: Well, as you say, you're holding the bag if you close out the HTLC...

Speaker 5: Yeah, hold the bag. Ahh, yeah.

Speaker 2: Yeah, obviously, you gotta control that. So if you just do a probabilistic model, you're kind of going: Well, at some point, I'm likely to close on you. I mean, the theory was that if your peers that unresponsive, it hasn't closed because if it's stuck downstream, it should have forced closed, so that it could close on you and not get forced closed by you. So, if your peers this out to lunch, you're like: How much else is getting through? I wonder. People complained about: Oh, you know, you went to change, it's like, hundred sats, but did you really? Or was it just your peers gone to lunch anyway?

Speaker 0: The other ssue that we've seen a bunch of - I think probably the most common forced close reason right now - is just one node forwarded a payment, their peers are out to lunch, and they had to force close legitimately, but they don't fail back the inbound edge of that payment until that commitment transaction and HTLC timeout hits the chain. Those HTLC timeouts were getting delayed long enough that the inbound edge channel was getting force closed. So, there's another thing to think about that we intend to have again - haven't managed to have a discussion about it yet - but do you just fail it back? Like you're waiting for something to confirm and your two options are: You fail it back now and just give it up, or your peer is going to force close and presumably their HTLC timeout is going to make it. But now, there is that race condition of your HTLC timeout took too long, your peer could technically claim it as a HTLC success, but you're kind of running out of time to fail it back, you need to claim it back. So, you have that like really narrow window, but I'm not sure that it's worth the force closed to keep that window open as long as you can.

Speaker 2: That's a really good point. At what point do you go: Well, it's floating around somewhere; it will get confirmed eventually. We don't have a risk model at the moment for that, and we probably should.

Speaker 0: Yeah, and I'm not sure that we're even going to bother with a risk model. My personal view is you just fail it back because you have that narrow window, you're already screwed. Your HTLC timeout did not make it by the time you really needed it to make it. We're so screwed. At least fail it back or something. You're going to lose it anyway. I've been trying to spend a bunch of time with like the plugnet people and whatever, debugging a bunch of these force closes, and I think that is by far the most common force close case today with the like LND bug that's going to get fixed soon. Hopefully, not too far behind it.

Speaker 5: So, we had that bug fix. I thought we were doing it, but what we're seeing sometimes is that either the TCP connection is stale or the state machine is stalled. We have a thing where we basically say: Okay, well, if we send a state, we don't revert back, revoke in a certain amount of time, we would basically 'tear down the link,' which just meant state machine is gone but the connection is still there. Now, we're going to disconnect. Some people also report that if they just do disconnect-reconnect, they shall see it disappear. Maybe there's some other lingering thing, but at least, we can do this to automatically try to trigger the basically that reconnect, which seems to resolve some things. But for us, it's a super old bug. The bug is three plus years old and was meant to fix something else. But that seems to be something that people are hitting right now, as far as those force closures. Mempool is chiller now, at least. So maybe it's not as dire. But I think what [Redacted] was saying they're on kind of like the race condition. Being hit more frequently would explain it because fees are higher now, and your outgoing doesn't confirm, the incoming doesn't confirm, and then you have a mini cascade basically. But the other thing is, I don't know if anyone's read this paper, something I need to actually take a look at, but it hypothesizes something I think we've talked about in the past: Using circular payments to sort of cancel back an HTLC earlier, which seems related to what we're talking about now with this dash HTLC. Can we use some hand wave reroute this dash HTLC to somebody else and they'll hold onto it or something like that? I don't really know, but maybe there's something worthwhile there as far as rerouting stuff, which seems to be useful in Azure Web Contacts, but just dropping that. It was an FC earlier this year, but I haven't really caught up with all the papers yet.

Speaker 0: So, does anyone else have thoughts on whether to give up on an HTLC if it's not? I would be very interested to hear thoughts on that, especially the giving up on an HTLC that is going to result in a backwards force close.

Speaker 1: That's always what we've been doing in Eclair. When an outgoing HTLC has reached the timeout and we're publishing our HTLC timeout, we are instantly failing back on the incoming link. We've always been doing that.

Speaker 5:  So, you fail back before confirmation. You're going on-chain outgoing and you fail back as soon as you make that decision basically.

Speaker 1:  Yeah, we take the risk to avoid that chain of not being forced leave as well.

Speaker 2: Yeah, we wait for three confirms, which is probably way too conservative, right?

Speaker 5:  Yeah, so we wait for at least a single confirmation. But I think as soon as we broadcast, we cancel back dust at least, because things that were dust on the outgoing, because they don't really matter anymore. But we don't do everything, like Eclair seems to do.

Speaker 2: Actually, we're the same because when we see the transaction, we know which HTLCs are actually in it. Because there's that state where you've got the two transactions, and you're not sure until you see it on chain. Once you see that mined, we go: Okay, cool. These HTLCs can close because they're not there, and so, dust goes under that, too. The ones that are there, then we try to spend it. We wait until it's three deep before we fail back. But even if three or one, probably both sucks, right? There probably is a point where we should just fail it back. I'd love to see someone's write-up analysis of like when to do this, so I could type it in and not have to figure it out.

Speaker 5:  That's interesting, [Redacted]. Has Eclair always done that or did something happen and y'all decided to start to do that?

Speaker 1: No, we've always done that. But there's one caveat though. We still wait for the commitment transaction to be confirmed. We don't do that if the HTLC is timed out, but we still haven't confirmed the commitment transaction. We are not failing back those HTLCs yet because there are potentially two remote commitments and we don't know yet which one is confirmed. But as soon as the one commitment transaction is confirmed, we fail the HTLC timeouts as soon as they timeout on the downstream link.

Speaker 0:  We haven't been a high fear rate environment for a while. Do you have any sense of what the difference is in failure rates across those two models? Because I would assume somewhat naively that there's probably not a huge difference in force closure rates between waiting for the commitment and waiting for the HTLC timeouts.

Speaker 1: Yeah, I have no idea.

Speaker 0: From what I can gather, that is by far the most common force closure today. So I think we're going to reconsider it, and I would encourage others to.

Speaker 5: One thing that we didn't get into 16 is basically deadline awareness. So, we have a thing right now where we say three comps, it'll always retarget three comps at least, but it doesn't say: Oh, there's two blocks now. Let me ramp it up. So, we had code for that and we try to get it in to fix other Mempool stuff, but I think that'll help a lot. But the main thing is: How much are you willing to pay? Obviously too, right? Which is where maybe this desk thing factors in somewhat so.

Speaker 1: Yeah, that has cost us a bit because we have a deadline aware code that as soon as we get we're getting closer to the deadline, we actually RBF more aggressively, but we didn't really cap that by the value of the thing we're trying to get back. So, during the recent high fee environment, it cost us much more than what we were actually getting back in the HTLC, so we just changed that.

Speaker 2: Yeah. As of the release that just came out this month, we finally are deadline aware. Better late than never, and we do cap it. If we've capped it, because it's not worth it, we basically, at that point, ignore it. We don't care; we're not going to wait for it anymore on the theory that its best effort at that point, because we haven't paid what we think is a fair fee, which really screws up our accounting if that happens and it never gets confirmed and we forget the channel and we still have this thing outstanding.

Speaker 5: Do you mean once the fee is above that value, you forget that output or something else? So you say we're not even gonna try.

Speaker 2: Normally our state machine will wait for every output to be finished and everything else before proceeding. But we won't forget the channel until everything's 100 deep, it's all done. But if we had to lowball something, because it just didn't make sense, as we approach deadline, we'll ramp up, but we'll never pay more than approximately the value that we're gonna get back minus some dust. If we've capped it, we mark a flag and say: Actually, don't wait for this one; it's not gonna. We don't hold things up anymore for that. So it can end up, but that may never get spent.

Speaker 5: Gotcha. Cool. I just wanted to get y'alls thoughts around that and just give them all here, and this is like something that's happening right now. So, I have a draft PR in the LND repo for the whole hold the bag on dust HTLC thing, where we'll just prototype it more. We're not committing to it yet, but clearly someone could run the patch themselves if they're really afraid of this conservator or something like that.

Speaker 0: Somewhat related: A bunch of the plugnet people now are recommending and starting to use the interceptor feature in LND because it does result in the inbound edge being failed back, even if the outbound edge isn't confirmed on chain. So, people are manually forcing that behavior, basically via this hack in LND. I think we have the same. You can do the same thing in LDK, or if you intercept an HTLC, we'll force it back maybe. I'm not sure for, anyway.

Speaker 5: Gotcha, okay, I can see if I got some details or just make sure they're using the right call or something. Cool. Next thing?

Speaker 1: Taproot and Taproot Gossip. So, the floor is yours, I guess.

Speaker 5: Yeah, sure. I need to re-re-reload and refresh everything in. We've been doing much review on our side. There's nine actual PRs. So, I have like a bunch of side branches just to make the rebase hell a little bit easier. I think one thing popped up in the review of LND. The way we're trying to like do this non-stuff - basically, just to make sure it's safer using and side changing. And then [Redacted] brought up something around co-op close that I need to like revisit. The idea was: Okay, well, because co-op close, you only ever signing one message, so you only need one non-spare basically. Then, I added a thing where also it would fast accept, right? So, as long as what the initiator says is cool, we'll just cut everything short. But I think there was something around them not setting the same free rate and enforcing non-trees. That's one thing I need to take a look at. If that's the case, then before we send another set of nonces after every single reply, we can go back and do it in that, if this turns out to be actually a thing. So, I just need to check that out. But I'm just focusing on this just to get everything up and running. Get all the tests running there. And then, for the gossip stuff, there's just the other things that we need to discuss around how much to go into the 2.0 gradient.

Speaker 6: It's all review on our side right now. Got past the hurdle that I was talking about last meeting. Figured that out, and just trying to get that in. Maybe we'll get it in tomorrow, I hope. The channel co-op closing, we haven't really looked at that yet. So, that is really the big issue that since the very beginning of our taproot approach. We kind of have been leading open because I've always had the impression that it was gonna be subject to the most change.

Speaker 5: When you say that stuff is ready, does it mean you're all ready for doing interop now?

Speaker 6: No, we need like probably three PRs to merge for interop.

Speaker 5: Okay, gotcha. That makes sense. I'll post about that co-op close thing and just generally refresh all of those other comments. I rebased all the branches last week, and just need to kind of start to chip away at all that stuff. Just I test, test vectors, so forth, weight estimates. That's kind of some of the stuff that we're missing right now from the specs side of things.

Speaker 6: Cool. Do we have anything new regarding gossip v1.5 on our side?

Speaker 5: I think last time, there were just questions around the whole strictly binding or not binding, and then also value amounts.

Speaker 0: Did you ever start that thread on Lightning Dev? Last I remember, you had committed to like do - I mean, at this point, we might as well just talk about it in New York.

Speaker 5: Correct, I haven't started it, but I'm gonna do it this week. It's on my fucking to-do list. I chopped up a bunch of shit. I imagine we will talk about it in New York as well but at least we can precede some of the discussion and stuff there. The one thing we're doing in the background is also just refreshing our taro implementation, just to make sure there's no crazy edge cases for taproot stuff as well. That's something I was working on. I don't imagine there's anything there that we haven't thought of, but just to at least cover that base. Because it's a little bit different now. Because you need to send the control block along with it instead of just the signature, et cetera. Cool. What else? Okay. Check, check. It looks like, I don't know to pronounce the word, but quiescence is back on the thing.

Speaker 1: Yeah because it's actually a prerequisite for splicing. We've started with splicing for now. We finished our splicing implementation, and we've been testing it on mainnet to see how it behaves with those high fees and how fun it is to do CPFP and RBF on those. Everything is looking well on the splicing part, but that's also because we hadn't implemented quiescence. We had only done a four-month quiescence, where you only do splicing when you have no HTLCs in any commitment whatsoever. So, now we are looking at making it with quiescence and with potential HTLCs. So, I just think it's time to revive that PR and make sure that it is up to date. But it looks like it has most everything that we need. We just need to spend more time finalizing our implementation.

Speaker 2: Yeah, it's kind of a weird PR because it doesn't do anything by itself. It kinda needs some other PR to make it useful. Like, why would you quiesce unless you've got some other feature? But it does make sense. I think it's a separate feature bit. I think that's the right thing. Yeah, it's pretty easy to implement. You just stop talking when you get the STFU message, and you will go quiescent at some point. The other thing that I wanted to discuss in New York is this idea of the simplified protocol, where we basically just start taking turns. Because it is a subset of the existing protocol, it's pretty easy to implement. Given that we still seem to have lingering state machine bugs, I kind of put it on the back burner because who wants to revisit that? But increasingly, I might know maybe we do. I know that [Redacted]'s L2 implementation actually uses the simplified, rather than being this full duplex thing where they can both have things in flight, this turn-taking thing. And the caveat is that I do not have an implementation of it for LN penalty. In particular, making sure it's still simple when you reconnect is the main issue.

Speaker 0: Yeah. The good news is, at least my worry that we had that kind of bug with LND, was misplaced. It was not, in fact, simply a state machine bug, but just a hang bug entirely. I'd seen it, I was confused initially because I saw it with two peers, and both of them were in one of these multi things and flight going both directions states. But that didn't turn out to be the issue, luckily.

Speaker 5: We're looking into one of those with Eclair related to reserve, potentially, where there's a kind of a thing where LND said that they sent something that went below the reserve, but then TVAS had some very detailed logs, annotations, and it turns out maybe not. So we're looking into that as well. Not sure exactly what it is;  if it's like a rounding thing or if it's something where we do a thing where we basically do a dry run of the full commitment transaction, and then make sure that works. But maybe there's a gap there or something like that.

Speaker 1: But it really doesn't have anything to do with the reserve. That is the bug I reported because if you look at the state, it just does nothing that makes sense as a reserve issue. Nothing adds up to make it look like it's a reserve issue because the HTLC that's an issue here is an HTLC sent by LND. So, LND decides to send this, and it doesn't make it fall into below its reserve. So, I really think it's unrelated. People think that it's linked to reserve, but I don't think this is really the issue.

Speaker 2: There's a theoretical bug we've always had caused when we decided to go full async. If you have a fee change in flight, it's not completely determined whether or not an HTLC is valid. Depends on what state that's in, which is really fucking annoying. One of the things that the flight update commitment says is that you can only change fees by itself, right? Because you're turn taking now. When it's your turn, you can change fees or you can add HTLCs. You can't do both, which means you both know exactly the state you're in, and it's very deterministic what happens, right? Either you can afford the fees or you can't, and what you do if you can't. Whereas at the moment you can end up with a case of: Oh, but I've added these HTLCs, but now on the new fee rate, I can't afford them, but we're kind of fucked. that's a problem we've always had. That's kind of annoyed me. We're all hoping that update fee goes away entirely, but until then it's possible that you could hit something like that if fee rates...

Speaker 1: Yeah, but you just hope we get rid of update fee before we hit those bugs. At least, in the case that I was investigating, I had the user put the whole Eclair channel state, so I could see exactly what changes were proposed and signed and act, and there was no update fee in flight in either direction. So because that was my intuition as well. That it had to do with something like that. But actually, the state was much simpler. So, I really don't see what went wrong and what caused the LND to send internal error.

Speaker 5: Yeah, it sounds like an inconsistency. 'Cause we have like two or three levels of checks. One is the dry run. The other is reporting what's available. Maybe it's something where it's like a user sent out a payment that skipped the normal forwarding path at the same time that we did the forwarding or something like that. But, I think you gave extremely detailed analysis. I think we can just look into that and plug it in. Maybe try to reproduce it, and see what's happening there and make sure we can prior that.

Speaker 2: We already have code to avoid sending two update fees back to back. We will wait till one's completely settled before sending another one just because it seemed to trigger people's state machines when that happened.

Speaker 5: Ah, yes. So, we're fixing a bug for that. We have a PR, and it's that we seem to get it. Basically, if the channel starts and you send funding locked and then immediately send an update fee, we'll lose the update fee because we haven't finished processing the channel yet. That one is known, and we have a fix for that as well. One of those race conditioning things, where it's like a message is propagating. But, at the same time, we don't have a thing spun up yet, so we'll just not even learn that you sent that. Then anything that we send after that will be invalid because we didn't process that. I think along the way, we're also gonna fix that really old issue around update fee and funding lock. There's some ordering thing where we send them on order because they say - but that's going to be fixed as well alongside that too. So. Cool.

Speaker 1: Nice. Regarding the option simplified commitment, apart from the fact that we're taking turns, everything else just stays the same. We exchange the same messages, commit, seek, revoke, and act, but just different P.

Speaker 2: We add two messages. One is a yield, so you can basically go: Oh, your turn. And the other is a no-op add, so you can provoke a yield. If you want to have a really naive implementation, rather than replaying - if you want a turn, you just send the no up, and that just invokes a yield. Otherwise, you just start sending updates. And either you get back an update, in which case if it's your turn, I can either just send an update and you just ignore it and send your own updates, in which case you're taking your return because that could happen simultaneously, right? Otherwise, you send a yield to say: Yes, no, no, it's your turn; after you, sir. And then you go. So, it's basically just two messages, and the no-op message is trivial. But it does allow for really naive implementation. Obviously, if you're employing both at the moment, you don't get the advantage of it. But, at some point in the future, when everyone supports it, you could have a very, very naive, very simple state machine. That's way simpler than what we do now. In theory, you don't lose any latency on a partially low utilization channel because you're taking turns anyway. You do, in theory, lose some latency on a high use channel, but in practice, it just means that you're batching a little bit more, which is probably closer to optimal anyway. So, it actually doesn't have many disadvantages.

Speaker 1: Cool. I don't have anything else on quiescence and splicing apart from the next PR I opened. Just a one-line PR about the HTLC receiver and channel reserve. It's something that I ran into because of splicing, because splicing make it makes this thing obvious. But, I think you all remember that almost three years ago, we discovered that channels could get stuck when all the funds were on the non-initiator side. And because when you add an HTLC, it increases the fee of a commitment transaction. So, you must make sure that the initiator who is receiving that HTLC will not dip into its channel reserve, and will not dip below zero basically. But actually, the spec says that as a sender, you must make sure that the receiver of the HTLC, when he's the initiator, is able to pay the increased fee, but also needs to maintain its channel reserve. Otherwise, you don't send an HTLC. I don't think there's any good reason to make them maintain the channel reserve because they just need to be able to pay that fee and they are actually receiving an HTLC. So, if it fails back and it took them below their channel reserve. If HTLC fails, they will go back to above the channel reserves, and if the HTLC fulfills, they get even more funds. So, it makes the channel balance more balanced. Because the issue with splicing is that when you're in a state where the non-initiator with the fund, the initiator is slightly above their reserve, but the non-initiator swaps in some funds. The reserve is here because it's 1% of now a bigger channel. So now, you are stuck. Now you are in this situation when you, the non-initiator, has all the funds of the channel but they're not about any HTLCs, so you're really screwed. But this can actually happen also without splicing, so I was looking at fixing this and I was wondering what implementations you do on the receiver side. If you are the receiver and receive an HTLC, you did use the increase fee but do you also verify that you maintain your channel balance? And if so, do you just let the HTLC go or do you force close? Maybe I can share the one line in a clear...

Speaker 5: Basically what you're saying is that adding funds can cause a reserve requirement to go up. And if that goes up, maybe you can cause something to become stuck even outside of like that slight edge case, right?

Speaker 1: What's interesting is that the spec says that the sender should not send such HTLCs, but there's no requirement on the receiver. So, if no one implemented the receiver side requirement, we can just drop the sender side requirements and get rid of this issue. Otherwise, we have to think about it some more if we want to make it backwards compatible. So I'm curious what implementations do on the receiver side. If you are the initiator, you receive an HTLC, you compute the increased commit fee. You verify that it's lower than your balance, but do you also verify that you still meet your channel reserve after that increase in the commit TX fee?

Speaker 5: For LND, I think yes, and it'll result in us sending an error or a warning and just kind of stopping. I need to check with biscuit, but the full scenario is: What do you do as a receiver if you're the initiator, and you're about to propose a HTLC, or you receive a HTLC that causes you to dip below the reserve or you receive an update fee that causes that?

Speaker 1: Yeah because actually, I don't see why we need to maintain the reserve in that case. We only need the initiator to still be able to pay the fee for the commitment transaction, but we don't really care if it makes them fall below the reserve.

Speaker 5: And this is what the receiver who is the initiator does, right? So as the initiator, you receive an HTLC, you display the reserve, what do you do?

Speaker 1: Yeah, exactly. Do you even check it? Because the spec doesn't say that as a receiver, you have to check it. We do check it in Eclair, and I'm removing that, but I wanted to know if other implementations are checking that as well. Because in Eclair, that would result in a false close, which is bad. But if no one else does that, we can still phase it out pretty quickly. But if other people do that, because we'll have to fix that for splicing anyway because with splicing, since the reserve is set to 1% and 1% of something that grows becomes bigger, we will hit that issue a lot more. So, we have to figure out a way to fix it. But maybe we can just say that for channels that have the splice feature, then we do it differently and we skip that check and we allow dipping into the channel reserve in that case. But it would be easier if we don't have to add an if to the specification and we just do that in all cases.

Speaker 5: I think LND were error out.

Speaker 2: I think we did too.

Speaker 5: So, we'll take that, and then basically run a simulation to see what it would look like, and then I think we error out. I think at that point the channel was kind of stuck if you sent a sit, because you retransmit that on restart basically. But looking at it right now - I haven't looked at this code a while - so I think we're error out basically.

Speaker 1: Do you agree that conceptually we should not? There's no reason? So, the other guy is making you dip into your channel reserve, but that's because they're adding an HTLC to you. So. that will just improve the situation, and you have no incentive to actually reject that channel. You're dipping into your channel reserve, but yeah, that's okay.

Speaker 5: Yeah because we might gain funds if that thing sells. But can this be allowed to happen multiple times? Because eventually won't we go to zero? But I guess you're saying that: Well, you're letting us go to zero.

Speaker 1: Yeah, you're still checking that you cannot go below zero because then you cannot create the commitment transaction and pay the right fee. So, that would fail if you go below zero. But I think you can go all the way to zero.

Speaker 5: Yeah, I think we actually hit this. Some people were reporting that like they were doing winter rebalancing stuff. They inadvertently got their channel into the state because they were just you know doing winter rebalancing in a loop.

Speaker 2: So, what you're saying is in theory there's no reason for me to check you're not pushing me under my reserve because that's your problem, not mine. Okay.

Speaker 1:What's nice is that if we had implemented that, we could remove the sender requirement as well because the sender wants to push the funds. Because otherwise, the channel is stuck, and they have a lot of money on their side. They want to be able to make payments. They don't really care if you go below your reserve because it's only temporary. It will either: If the HTLC fails, we get back to the situation we had before. If it succeeds, there's more funds on the other side. So, it means they meet their channel reserve. So, it's a win-win situation to remove that. But, we will probably have a backwards compatibility issue.

Speaker 5: Yeah, I think the logic there follows. And this is just, I think just us trying to be super defensive after we had weird stuff happen in the past in this area. We need to look at that last thing also.

Speaker 1: But there's maybe something we can do is just cheap on the implementation side. Removing the check on the receiver, and the senders will still not send those HTLCs, but the receivers will not check it anymore. And so that when we can see that everyone, at least enough people, have updated, then we can remove the sender requirements as well.

Speaker 5: I guess you can just assume that is there for splicing. Unless you just want to mention that explicitly, I guess. Because yeah, I can see how this can happen more. Yeah, more in terms of...

Speaker 1:Alright. I think I'll detail that more directly on that PR. We've planned to only remove the - since the specification doesn't really match what the implementations do, and the implementations are currently more defensive than the specification, I'll just make it a hint for implementers to drop a receiver side requirement, ship something, and then six months later, we will drop from the spec both, all the requirements and from the implementations as well. Hopefully, that will match the timeline for splicing as well. Perfect. Next we have, is there anything new on attributable errors? I don't think [Redacted] is here. No, [Redacted]'s not here.

Speaker 5: Nothing new.

Speaker 1: And the channel reestablished requirements are not a priority either. Your storage backup, anything new? Nope? Alright, so has there been progress on issue 934 that was opened a while ago? Where you should not directly publish your commitment when you receive an outdated channel reestablished, but instead wait for an error. Did everyone ship that in the implementation? I didn't check.

Speaker 5: Good question. I think we haven't shipped this yet. I think us and CL had like a little thing that was patched over basically, just because I think they wait a bit of time now. But we do have this opportunity. We do have this thing coming up to fix the whole: Let's disconnect if they get an error. So we can potentially slip it in there. My thing then was just making sure that it aligned with expectations of older LND nodes kind of a thing.

Speaker 2: Yeah, that shim is still to do. Actually, we released without it. But yeah, the problem is that we would get upset with them. We would send a warning on error, which means you don't close the channel. But then, we would hang up on them, and we would usually not receive their error in time. It means you get in this state where often they had to manually force close the channel rather than happening automatically in the case where their peer has just lost their shit. So, the workaround is to wait a little bit. The bigger thing is to change it so that we don't automatically drop the connection when there's a warning set. But I worry about the side effects of that too. So, that's a little bit more invasive change.

Speaker 5: Okay. Yeah. I mean, hey, at least for us, we know people are on some newer versions as a result of stuff that happened. So there's that. The word is just to make sure we're not breaking what's old stuff. One other thing - remember we did the whole thing where we basically made max-HTLC required, right? And as we were reporting that they were doing syncs, and then they were rejecting old updates just because they didn't have the field set. And I think we did it and I think there's a bunch of new ones that aren't being sent, but maybe there's some older node that has these legacy ones. But I told people: Hey, just don't sweat that. But I didn't realize that, initial graph analytics, people get that stuff. But it's something that's interesting.

Speaker 2: Yeah, it's not real. So, those ones we've looked at. We looked at this, we went: What the hell; we were sending it out. Like a warning at that point. Hanging up because they're sending us this bad gossip. We dropped that; we started just ignoring them. But it was really interesting. So we looked at the ones they are, and they're like five years old. They're sending us really ancient channel updates for like, why? That was the problem. We didn't find any recent channel updates like in the last six months or something that would actually be valid that they should ever be sending us that have this issue. So, the answer is just to ignore them.

Speaker 5: Just some people would just freak out about logs. So maybe we can make like a warning or something instead of like error or whatever.

Speaker 2: Or check the timestamp. If the timestamp is too far in the past, then just drop it. But if it's recent and they don't have that field, then yeah, something's weird. But I don't think you'll...

Speaker 5: It's probably one of the cases where we would have accepted it, but then pruned it because it was a zombie, like the next block or something.

Speaker 2: Yeah, exactly. Definitely older than two weeks.

Speaker 5: We know no LNDs are sending that stuff out. Also, someone do them custom.

Speaker 1: I see that [Redacted] wanted to talk about subject. Regarding LSP stuff.

Speaker 3: Yeah, I realized no one's probably read this yet, but basically we have some LSPs that want to be able to take an extra fee on the first payment that an end user receives to cover the inbound channel opening fee. So, basically all it does is it just forwards less than the onion says. And there's an extra TLV in the update add HTLC that says how much fee they took. We also have a configuration option, obviously. So, you just have to opt into it on a per channel basis, although that's not part of the spec. So yeah, it's pretty early, but we're hoping to get this in pretty soon. So, if there's any initial thoughts on that, that'd be great.

Speaker 1: Does that mean that whenever you receive an HTLC that you should forward to a client and doesn't have enough capacity, you're going to immediately open a channel and forward that HTLC with those additional TLVs?

Speaker 3: I was mostly just thinking about the first channel that they receive because I think they're gonna potentially include some buffer, so that they won't just open at just enough to cover the initial payment only.

Speaker 1: I really think that cannot work well because of MPP. Because as VLSP potentially, you receive a first HTLC to forward, but then there are the two others that are coming. So, what we're doing in Phoenix is that we have this small protocol where when we receive an HTLC and there's not enough balance, we send a new message that's called a pay to open request. We just include the onion, and we let the client receive it as if it were an HTLC. They could be on the onion, see that there's potentially more coming because there's a total amount. So, we let the client aggregate everything. We also have those pending on the LSP side. So, when the client has everything, they can send a message to say: Oh, then please open a channel; I need to receive all of those. And then we negotiate the fee.

Speaker 3: How does the fee negotiation happen on that?

Speaker 1: Oh, it's really - the VLSP says: I want to take that much fee. The client has to say: OK or not OK. So, the way we do that is that we are changing the way it's going to be done in Phoenix, where the user will be able to control how much they are willing to pay with both max percentage and max flat amount. So the user just sets this once, and it will automatically accept or reject depending on what VLSP says.

Speaker 3: Got it. Okay. Is that incompatible with this? Because wouldn't they just do all that calculation, and then just set the fee to whatever was previously agreed upon or negotiated?

Speaker 1: Oh yeah, that's not incompatible at all. But it's just that your proposal alone seems that it's only part of the thing. And if you only do that naively, you're going to be opening too many channels and wasting a lot of on-chain fees.

Speaker 5: Can you repeat the thing around the MPP incompatibility there, [Redacted]? That it works, but if you have many HTLCs, then...

Speaker 1: As VLSP, if someone is sending an MPP payment that's split into, let's say, three HTLCs, for example. You receive the first one as VLSP. You have a channel to that mobile wallet, there's enough liquidity, you forward a normal HTLC. Then there's another HTLC coming with that same payment hash, but now there's not enough balance to forward it on the channel. So, you send another message with the onion. If you instantly open a channel and forward that HTLC, then when the third HTLC comes in seconds after that, you're gonna open yet another channel and forward it on that one, which is really sad. You forward the onions to let the client tell you: Okay, I received everything. That's the amount. Open the channel for just that amount, and then forward the HTLCs through that.

Speaker 5: Makes sense. Basically, y'all have MPP awareness at the LSP node to make sure you can give it back a single unit to avoid the slow trickle. Okay, that makes a lot of sense.

Speaker 1: And on the mobile wallet side. Because the important part is that it's the mobile wallet that still receives the onions and that does the aggregation, and only at the end of the aggregation says: Okay, I'm ready to receive everything. Please open a channel for that amount.

Speaker 2: Right, but it's got to be something other than add HTLC, right? Because you can't add those HTLCs to the channel yet, right?

Speaker 1:Yeah, that's why we have a new lighting message that contains the onion and some information about, I think, the fees amount. Something that really looks like add HTLC, but is not tied to a channel.

Speaker 3: Yeah, that makes sense. And I think [Redacted] was discussing that. This is just kind of what they requested, so we're kind of just rolling with it. But I think we should talk about that in more detail. But you're kind of saying that there should be some additional parts to this, basically.

Speaker 1: Yeah, I think it's better to really look at the whole thing before doing small parts because otherwise it's going to be hard to have something that really works end-to-end. See, we haven't yet made that into a blip or even a bolt because we figured it - at least the TLVs added to existing messages - could be directly in the bolts because it will eventually benefit everyone to be able to run the same kind of LSP things. But we really think that splicing and liquidity adds are really important tools for an LSP. So, we think we have to do those first before we do any kind of LSP specification.

Speaker 3: Got it. That makes sense. OK, I'll bring that back and see what the LSPs that we're talking to think about that, but that makes perfect sense to me. So, cool.

Speaker 5: That's interesting. Cool. Guess that's about it. I think we have two more of these before the spec meeting. Maybe one, depending on time zones, do something again. I just posted that and then also [Redacted] had that. [Redacted] made an issue tracking kind of discussion topics like we've done in the past. I haven't done anything there yet, but you should have to check that out, so we can start to look at what the schedule looks like. [Redacted] posted it there.
