---
title: "Lightning Specification Meeting - Agenda 1146"
transcript_by: Gurwinder Sahota via tstbtc
tags: ['lightning']
speakers: []
date: 2024-03-11
---

Agenda: <https://github.com/lightning/bolts/issues/1146>

Speaker 0: So first item, I just wanted to highlight that I opened the PR for zero reserve, if you want to look at it. I don't know if people are actually trying to implement that. It matches the implementation that we have currently in Eclair and Phoenix, but with a different feature bit. So if someone else is implementing that, they can just have a look at the PR, and we can work on the interop whenever someone is ready. I don't know if you guys want to discuss it further. It's just out there, and people can just read the PR when they are interested in implementing that.

Speaker 1: Yeah. I mean I've read that one. I also wrote the other one that I closed. I know that it's sort of my stance that given that a lot of the limitations today seem to implement things in a more relaxed way — at least, according to [redacted] as well — I don't know what the opposition is to relaxing it in the actual BOLT language is to reflect what the network does, but it's not a hill I'm trying to die on. That's why I closed the PR. But I do want to have a better understanding collectively about why it is that we can't relax the requirements in the BOLT.

Speaker 0: But it's rather that relaxing in the BOLT allows the other guy to set zero reserve to you, but basically, there's no way to say: I would like you to set zero reserve to me. If you want to signal that you want to open a channel, but you want the other guy to set zero reserve on your side, then it should be explicit with that. We don't use a channel type in the PR we created. So, you just realize on the behavior that people will just do that. Otherwise, you just reject the accept channel that doesn't contain zero for the reserve.

Speaker 1: So, am I to understand that the option zero reserve, when you advertise that feature bit, it functions as a request to not put up a reserve yourself?

Speaker 0: Yeah, it's still a bit fuzzy on what people would like to do. That's what we think is best. That's what we are currently doing. But maybe we want more hooks here to signal: I want you to set zero reserve on my side, but I'm okay if you don't. Or I really require you to set zero reserve on my side, otherwise I will just allow you to send accept channel without that. Depends on what people really think is useful. So, I don't know if people have played with those alternatives or not yet.

Speaker 1: I mean, maybe I'm missing something, but we already have provisions in the BOLTs where you can reject a channel if its reserve requirement is ‘too high.’ So, between saying that there's a zero reserve being offered, and then if they just don't set it on like and you can just reject it for the same reason that you might ordinarily.

Speaker 0: Yeah. But then, you will just never reach agreement. You're just gonna reject it and then, you don't make progress. Nothing happens. If it's supposed to be manually saying that the other side accepts with zero reserve, how would that work? Because if the other side doesn't send you with zero reserve, how do you make that change to actually get a channel that you would agree with?

Speaker 1: I mean, you can converge. It's like you either fundamentally can't reach agreement because of your requirements —  there's like a null set intersection — or you should be able to be like: Okay, I might cut my reserve requirement in half and try again.

Speaker 0: Yeah, but how do you tell me?

Speaker 1: Only down to what my own limit is.

Speaker 0: Yeah, but there's no way to tell the other node right now: Please set zero reserve for my side. I send you open channel. I want you to respond with accept channel with zero. There's no way to say to do that right now with the BOLTs. There's no way to express that. You can only set the reserve for the other guy, but you cannot ask the other guy to set the reserve for 0 on your side.

Speaker 2: Alright. They seem like orthogonal issues. Like, we could do both, right? These have to not.

Speaker 1: Yeah.

Speaker 2: If we want a way to do full-blown negotiation of zero reserve, we have to do something like [redacted] wrote out, but we can also describe the current behavior with [redacted]’s PR. 

Speaker 0: Yeah. I thought that I understood that everyone wanted that behavior, so we can do both in the same PR. But if people only want to make the current behavior clearer, then we reopen your PR as a first step. I really don't mind. I'll keep my PR open anyway because I think that's a behavior that can be useful. But I don't mind either way.

Speaker 2: I have no opinion. Do whatever. 

Speaker 0: Yeah. It really depends on what people actually want to ship. Because right now, we're just talking about it, but nobody has a plan to ship anything. We know that we want to ship the thing. We shipped the thing that is actually using a feature bit like that. If someone else really is ready to ship something, then when implementing it, they will realize what they want — what they currently have is enough — and then we can decide, I guess.

Speaker 1: Yeah, we don't currently have scheduled work, but I think we are amenable to implementing this feature.

Speaker 0: Okay. Then it can just lie there for a while until you are ready to really ship something and then, we can pick up the discussion. There's no rush in getting that one merged or getting progress on that one. We can just stay with the current behavior until you want to make progress on that. Perfect. So next up. I just had a small question on the Trampoline PR. I opened a comment on the spec PR because in these test vectors, I'm using a notation for short channel ID — the coordinates notation that we defined in the spec — but [redacted] found it unclear. That's something I use a lot, but maybe I'm the only one. So just tell me if it's unclear and if I should switch.

Speaker 3: Oh, sorry. It was only because it was using the zero block and zero transaction, I think.

Speaker 0: Ohhh. Yeah, okay.

Speaker 3: Yeah, in that specific use case, it looked like a double hex prefix encoding. I think in any other use case, it would have been perfectly fine. So, that's on me. Sorry, brain fart.

Speaker 0: Okay. Then I can just update it to look like a real short channel ID using a block height of 800,000-something so that it looks more like a short channel ID. That will be clearer. Okay. Apart from that, any more feedback on the implementation on the LDK side, or are we still on hold?

Speaker 3: Well, I opened another follow-up PR on the LDK side that actually constructs the trampoline onion and then, the outer onion and makes them dependent on one another. I talked to a couple people regarding the hashing idea, and so far, haven't really met any resistance. But now, part of me is still worried about that. It seems like it should be safe, but I don't know. We should probably think of some more folks to talk about that and make sure it's all safe and sound.

Speaker 0: Okay. Sounds good. Alright, then. Trampoline is making progress. Next up, on mutual close, there was a question by [redacted]. So LND finished its implementation, and right now, the spec allows you to decide on the sequence field that we apply to your transaction. I was asking to add the lock time because I think the lock time is even more usable, and being able to define the lock time I use is more usable for anti-fee sniping. [redacted] was pointing out that maybe we actually don't want to let the sequence field be set, and maybe we always want it to be set to RBF basically. I think that kind of makes sense. It's too bad that [redacted] is not here because I think that at some point, they opened it up to be able to be more future-proof to be able to do more things within sequence. But [redacted] points out that if we ever do more things within sequence, that will also come with a new transaction version probably. So, maybe it's a bad idea to auto any sequence number right now, and maybe we should just restrict it to FFFFD. Do people have an opinion on that? It's too bad that [redacted] and [redacted] are not here, but...

Speaker 2: That makes sense to me. I mean, we should certainly do anti-fee sniping, but that's just lock time. Sequence-wise — I mean, I think the thing with setting a different sequence number is we have to do a whole upgrade cycle anyway. No nodes today are going to set a different sequence number. In the future, if we set a different sequence number, we're going to want to do a whole — there'll be some new software update and some negotiation of it. We're going to have to have a negotiation to decide whether you support setting something else because most nodes today would usually reject it. So it seems like we should, like we'll need a new, not necessarily feature bit, but certainly TLV anyway, so we might as well just have a new TLV. I don’t know. 

Speaker 0: Okay. So for now, we just replace that field to be the lock time that we know we really want to be able to set. If we ever want to allow setting the sequence to something else than signaling RBF, it will be done with a new TLV and potentially a future base. Okay, that should make [redacted] happy and we'll just see if [redacted] is okay with that, but...

Speaker 1: Yeah. [redacted] was just concerned about making it predictable.

Speaker 0: Yeah. I think there's a point that right now, everyone writes it to just be the same value that signals RBF. We don't have any use case to set it to anything else. So maybe it makes more sense just hard-code it to that right now. We'll see. Yeah, I think that makes sense. I'll put that back on the PR comments and we'll see if [redacted] updates the PR accordingly. I don't know if anyone on the CLN team has been working on implementing simplified mutual close. Nope. Okay, Then let's just wait for feedback from [redacted]. The next PR is about the compact representation for node ID. [redacted] opened that to be able to use a SCIDDR or pubkey — basically, an SCID or a node ID in the onion messages instead of the next node ID. The goal for that is to allow people who get an offer that is referring to a node by its short channel ID and the direction instead of another ID and who doesn't have access to the graph to just directly use that in the onion message. We don't really have to do it in the spec because that can be just added reading. Allowing reading that is still spec compliant, and if we only write it with specific nodes — in our case, in Phoenix — it's okay. It looked like [redacted] was against it. [redacted] was for it. I hate SCID or pubkey anyway in all cases. So we're not really making progress on that. I don't know how to decide and I don't really care that much, to be honest. So I don't know if people have opinions. But we were mainly waiting for [redacted] to chime in here. But yeah, [redacted], do you have more opinions on that one? Or someone else?

Speaker 2: I owe another comment. I had managed to confuse myself in my previous comments. So, I'm a little confused by [redacted]’s comment that this is about onion message forwarding, which requires a network graph if you're not already connected to the next node. No node should be dynamically constructing connections to do onion message forwarding. Certainly to send your own onion messages, sure. And probably for an LSP, in your case, maybe. But a normal node shouldn't be doing that.

Speaker 0: Yeah. It's basically for wallets who wouldn't have access to the graph.

Speaker 2: Right.

Speaker 0: Because that's the only use case I see.

Speaker 2: Yeah, I'm not super motivated to support this on our end. I think Phoenix is the only wallet that exists that doesn't have access to the graph.

Speaker 0: Yeah, but maybe that will change. We'll see.

Speaker 2: I mean, it might eventually, and then we can reconsider this.

Speaker 0: Yeah, but if we reconsider it later, the issue is that we would have to add a feature bit for that. If you don't have access to the graph, how do you know if those peers support that thing? Whereas if we do it right now, we know that it's in the first version and it's supported anyway. But maybe it's a gamble because we don't use it and we just added more code for something that nobody uses.

Speaker 2: I mean, honestly, I'm not really a huge fan of doing a graph lookup to forward an onion message anyway. Most nodes, or at least some nodes, don't have the graph in memory, which means you're hitting disk to do an onion message forward, which was kind of the whole point of onion messages is we don't want to hit disk for it. So that was most of my concern here, was like: I want to hit disk for this.

Speaker 0: Yeah, but then if we…

Speaker 2: LDK currently holds the graph in memory, so we don't actually hit disk, but other people do, and we might eventually stop that.

Speaker 0: But then, because if that's the reason against it, then shouldn't we remove SCIDDR on pubkey entirely?

Speaker 2: No because that's only when sending. I'm perfectly fine hitting disk when I'm intending to send a payment. I'm going to hit disk anyway for like you know sending payment.

Speaker 0: Yeah that makes sense. Okay. Then we'll see if [redacted] answers on the PR, but we may just close it and just keep it only in our implementation because it can be done in the backwards compatible way — at least with the worst thing spec compliance, so that's okay. Alright. All good for that one. Then, I just wanted to highlight that I opened a liquidity ads PR that is basically a subset of [redacted]’s PR that since we discussed last time, or I guess a few few spec meetings ago. We decided that it was really hard to figure out whether we wanted to modify the commitment transactions to add log times in there for the liquidity ads and the fact that it created a lot of complexity. Maybe it made sense to start with a PR that just lets you advertise liquidity ads rates without imposing anything on the seller. As a buyer, you just take a gamble. The seller could just take your money and then close the channel and see how the network behaves and see if we need after that, in the second step, to do a more strict version of liquidity ads that does add script restrictions. So that's what I did in that PR, but with some small changes to the liquidity ads types to express the list duration, which allows us to use a list duration of zero right now, which will be feature compatible if we add these durations that are higher than zero and add a log time to the transactions. So, whenever people want to have a look at that and if people think that it's a good first step, we could merge in the shorter term than the full-blown version that uses scripts. Just have a look at it whenever you want. Yeah, I don't know if [redacted], you had time to have a look at it, or you have opinions on that, or you're okay with it.

Speaker 4: I haven't really closely looked at the PR review. I just kind of skimmed it and it looks very similar to prior versions of the liquidity ads. I just left kind of a longer comment on the pull request. I think I'm generally in favor of moving forward with this. I think it's probably a good idea to kind of get it shipped and out there. I think maybe a lot of the feedback and sort of design decisions that we were making around the commitments, et cetera, were definitely more hypothetical and getting this out there, I think will help us maybe make some better decisions about what the market actually needs or wants. It is like an economic protocol, which, although I think there are economic downsides to buyers participating in a market like this, even our bus protocol designs that we had doesn't fully remove that risk. Since it is economic so to speak, I think that does give buyers and sellers an opportunity to kind of help price that risk in. So yeah, I think I'm in favor. I think this is a great way to move forward.

Speaker 0: Cool. Perfect. Then, whenever other people want to have a look at it and review it and start potentially implementing that. That version is really simple to do because you don't have to modify the commit transactions in any way. So it's really easy and quick to implement. If people want to start playing around with that, that could be helpful for to harmonize LSP implementations and to depend on that in LSP specifications. Alright. The next step in the quiescence PR, there was a discussion opened by [redacted] about adding an explicit message to end the quiescence part, which basically makes it much cleaner from a protocol point of view because it decouples the quiescent state machine from the inner protocols that run during quiescence, which makes a lot of sense. At first, I was really against that because of the potential additional complexity of nodes misbehaving and not sending that message correctly. But now, I'm quite partial to it. I think it's not that bad, and it actually makes sense to be cleaner from a protocol's point of view. I haven't implemented it though, so it would need implementation to see how much more complex it is, but I wanted to have other people's opinions on that, if people had looked at it or [redacted], if you want to talk about it more?

Speaker 1: No, I mean, I've already shed enough ink on this. I just think insofar as we have goals for being able to do layered protocols in terms of composing them, being like: Hey, I want to be able to make a new set of assumptions in some protocol; and then, those assumptions are provided by a layer beneath if we want to do this sort of layered design. I think I see it emerging — not just here with quiescence plus splicing and dynamic commitments, but we already also have it with interactive TX on top of the splice machine and on top of the like dual funding stuff. So insofar as we want to do that, having clean delineation is my preferred option. I also am sympathetic to the argument that it can create complexity and so, I think I made a concession in that thread that if we don't want to do this, I'd be fine with it, but it does mean that we need to make some other finer points of how those protocols interact a little bit more clear. Because at the moment, there's this sort of implicit requirement that isn't stated outright that I think is really important that people understand.

Speaker 0: [redacted], do you have an opinion on that? Based on the CLN implementation, do you see, would it be hard? Okay? Good?

Speaker 5: My thoughts are kind of just like yours — that it might be fine, or maybe reestablish ends up in this more complicated situation than it already is. Maybe it explodes or maybe it doesn't. I don't know.

Speaker 0: Yeah. Then I guess, [redacted], could you add a commit to the quiescence PR, open a PR on top of that one that has this unquiesce — or I don't know how you wanted to call it — message, and just specify whether we want it to be ack or not. Basically, both sides have to send it to end it.

Speaker 3: It's a both sides thing. It would have to be.

Speaker 0: Okay. Then once we have that, we can just work on our implementations and add that step, see how hard it is, and see if we're okay with it.

Speaker 5: Is there anything, like if I send it and don't get it back, can I just ignore all the messages that come through or I have to keep acking…?

Speaker 0: I guess you would disconnect if you receive something else. I guess in all cases whenever something fishy is going on and you are really expecting nothing else than a response to your unquiesce message, if something else comes in, you just disconnect and it resets the whole story. I might

Speaker 5: I might have a valid message queued up though, right? It's on the wire already by the time I send it out, so I don't really know when they got it and replied. So, I have to kind of just accept any message until I get the exact...

Speaker 1: Well, no, I mean, we assume in-order message processing, right? So if we already have something queued up on the wire and you queue up on the wire behind it. Like the resume message.

Speaker 5: That's a good point.

Speaker 0: You mean like [redacted], you send unquiesce and you expect only an unquiesce back, while [redacted] was sending you update add and commit sig. So that if you disconnect, then [redacted] is just going to resend update add and commit sig because they have sent a sig. Then, you are in a state where you can only force close. Is that all in a reconnection loop? That's what you say. But in that case, you would be buggy because you are still quiescent, so you are not allowed to send a date add and commit sig?

Speaker 1: Yeah. I mean, the channel has to be considered still quiesced until both it's sent and received. I mean, I think I need to detail the actual spec requirements here, so I can take that work on. But I think there is well-defined behavior that we can arrive at that I think makes the complexity no worse than it already is and gives us this facility to do the disconnect without disconnecting because that's functionally what it is. Like, at all times, if you want to just go to an unquiesced channel, you just nuke the connection, right? This is already an option that any implementation has, and you have to cope with the results of having a protocol that hasn't been executed to some committable state. As long as that's true, this just sort of gives you the facility without dropping the connection, which might be helpful in cases where you have parallel channels on the same peer connection and you don't want to drop the connection for all of them just to be able to reset the one.

Speaker 5: It sounds like it's probably worth putting in the spec that you can only send it on your turn. You can't just send it whenever you want.

Speaker 0: But it does not turn on that.

Speaker 1: Well, that assumes that there's a turn-based protocol. Turns as an idea begins in the interactive TX.

Speaker 0: Yeah. But it makes me think that right now, without the unquiesce message, it means that quiescence implicitly ends when the inner protocol ends. But if we add an unquiesce message, we also need to specify that when you are unquiescing, then you need to abort the inner protocol as well. Because, for example, interactive TX has a TX abort message that you can send at any time when you don't like what the other guy sent you. If you instead receive unquiesce, then you should also abort the inner interactive TX session or any inner protocol basically that is in the middle of a protocol that has to cleanly abort or if it can't somehow disconnect and resume or...

Speaker 5: I feel like once you're inside of TX, you either should finish it or TX abort. This NSTFU is only for the valid finishing of the connection without any kind of problem.

Speaker 2: What happens if we start a quiescence and then someone starts an interactive TX and then also starts an interactive TX v2 or some other quiescence-based protocol — they’re probably gonna stomp on each other. So should quiescence have a stated ‘here's the protocol we're going to do’ field?

Speaker 0: I think it's rather that once you're quiescent, any protocol that you're going to do is kind of a lock on the channel basically. So if you start splicing, until you're done with that splice, you can’t start something else in parallel on that channel, I guess.

Speaker 1: Yeah. I think intuitively, the fact that the STFU sort of means something fundamental is underway, we might be able to get away with doing multiple fundamental things at once, but that seems — I feel very hesitant to do that.

Speaker 5: Yeah. 

Speaker 1: I think this exclusive lock idea is good because if you're trying to literally re-pour the foundation of this channel, you're not gonna wanna do that with two different things trying to compete for space. You want total ordering of those operations.

Speaker 5: We might want the end STFU message to say: And start again for a new session. In case I want to chain up some things.

Speaker 0: But do you really need that? Because basically, it's fundamentally kind of the same thing as — oh yeah, no. Okay. Yeah, it's atomic if you send…

Speaker 5: If I don't want the channel to mutate. If I got two things I want to do — splice and something else — and I don't want the channel to mutate between them, I want to keep the STFU going through both sessions.

Speaker 0: I'd rather keep it simple. You unquiesce; you send STFU again; and the worst that can happen is that you do two round trips to exchange six before you do that second thing, and it just wastes a bit of bandwidth. But it's not really wasted. You just made some progress before doing your other thing. I think that's simpler, that you don't know, you don't have complexities that blows up and potential test cases that blow up this way.

Speaker 5: Yeah, that’s fine. Sure. 

Speaker 1: Yeah, I'm in agreement.

Speaker 5: Yeah. Important to note that I think we're kind of glossing over it without saying it explicitly — TX abort is the message that should be used to end it early and abnormally, and this STFU completed message would, as I understand it, just be in the success case. So right now, we imply it when you send the signature for the splice and we'd add a new message there, and only there, that is an STFU.

Speaker 0: But also when you abort, if you abort the interactive TX session, you would send TX abort and then, unquiesce.

Speaker 5: Oh. Wouldn't that just be implied?

Speaker 0: No. That's the goal. To stop the quiescence part, so that — yeah, you stop something that was at another layer, the interactive TX one. Then, you stop the quiescence part that is in the quiescence layer, I guess.

Speaker 1: I don’t know how…

Speaker 5: …with the reestablish process. I mean, it feels a little separate from STFU. I guess if you would — it's like the soft disconnect.

Speaker 1: The way I'm envisioning this is that quiescence is like its own stack frame in the protocol. Maybe this is a wrong way to think about it, but it's the way I'm currently thinking about it. If we were to take splicing and that entire stack, for instance, you start with the quiescence. You find a way to come to agreement on quiescence, which now allows you to make new assumptions. The new assumption being no HTLC traffic. Then splicing initial negotiation happens — right? — and then on top of that, you actually have the interactive TX protocol to actually come to agreement on the precise transaction. So in my mind, TX abort really should just drop that top stack frame and you're still in splice land. Now that said, I'm not totally sure because technically speaking, I'm not really working on the splicing proposal. But if I were making suggestions for it, that TX abort would only drop that top layer and leave the rest of it. Because you might want to try to retry again with the actual interactive TX. Like, if you were to import the splice all the way down.

Speaker 5: I think the way we use TX abort now is basically just reset everything in the channel without disconnecting. So, we go through as if the connection had dropped and reset. You basically do that, but keep the connection open because you might have multiple channels on that connection. That's how I think of TX abort.

Speaker 0: But I think in that case, it should be TX abort and unquiesce right after that. It feels cleaner that you stop the inner protocol and then, you stop the outer protocol because otherwise, there's no reason to add this unquiesce at all. Let's discuss that when [redacted] opens the PR to add this commit; we start implementing it and see how it behaves in our implementations. Okay?

Speaker 1: Yeah, I'll try to get pretty specific too because I think there are some hidden requirements in there.

Speaker 0: Okay. Sounds good. 

Speaker 5: Sounds good. 

Speaker 0: Right. So next up — I had kept the DNS-based offers because I think [redacted] wanted to make the BIP final. Is there anything you want us to look at, [redacted]?

Speaker 2: No, not specifically. I think the BIP itself — so the Bitcoin, not necessarily Lightning parts, are basically final. There's some ongoing conversation about bike-shedding  how to include sale and payments and BOLT 12 things in Bitcoin URIs, but it's truly bike-shedding at this point. Of course, we have stuff to do on the Lightning side that [redacted] said they were going to work on and that I would then adapt to — or I think [redacted] said they were gonna work on. If they didn't, I'm setting them up because they’re not here to complain. But yeah, I don't think there's anything super interesting here aside from: If you haven't read the BIP, go read the BIP because I don't really want to change it anymore. If you have feedback that is not super critical, please don't tell me because I don't really want to change it anymore.

Speaker 0: Sounds good. I'm done with that. Alright. The next step is placing a dynamic commitment upgrade. Is there anything new on that front?

Speaker 5:  Dynamic commitment upgrade? Not anything new for me.

Speaker 1: No. My only update on it really is I'm mid-implementing it. I'm actually more focused on the quiescence part. I'm working with [redacted] to get interop tested.

Speaker 0: Perfect. Then I think it's safe because if we can get that first part integrated into a spec — the quiescence part — then it's easier to build the other things on top and have no dependency between PRs. So perfect.

Speaker 1: I also like that we're coming at it from two different angles. I think it helps in making the actual protocol design a little cleaner.

Speaker 0: Yeah, I agree. Alright. The next step is Taproot and Taproot gossip. I don't know what's the status of that since last time. Who's working on Taproot? 

Speaker 3: Is anybody currently actively working on it?

Speaker 1: Just on our side, we already have the main stuff. The gossip part, people are actively working on it, but I don't know what the status is.

Speaker 0: Okay. I think you are also waiting on the simplified mutual close to be able to actually close those Taproot channels. I guess that once that discussion is done, then it will be easier to move to the next steps — last steps potentially of the Taproot channels. The next step is peer storage backup. I've seen that there was a bit of discussion in there.

Speaker 1: Bike-shedding.

Speaker 0: Okay. But have you started implementing something like that in LND? Is it a plan to ship something like that in the short-term, or midterm, or…?

Speaker 3: Yeah, [redacted] is on the call. I don't know if they can hear us. We've made good progress on it. I've done the review, so it's coming along.

Speaker 0: Okay. Yeah, then no action in the short term. Then, channel jamming, I saw that [redacted] had updated the — was it the bLIP? Yeah, I think it was the bLIP that got updated today. [redacted], do you want to talk about that?

Speaker 6: Yeah, I just updated it to add a feature bit like we discussed last time this came up. So it's ready for a read-through. I've been chatting to [redacted] about getting it into the next LND release, so hopefully we can move on that. Well, the next next.

Speaker 0: Okay, sounds good. I think that it's been on hold on the Eclair side as well while we were waiting on BOLT 12 mainly, but I think we should not be too far from being able to set that TLV. So, we should be able to follow through once LND has something as well.

Speaker 6: Okay. Awesome.

Speaker 0: Alright. Attributable errors. We haven't heard from [redacted] for a while, and I don't think anyone has been working actively on that — or has someone been working actively on that one? Yeah, I guess not. The next step is offers. Is there something happening? We are actively working on it from the wallet angle and discovering a few things. A lot of things to iron out basically, but nothing related to the spec — apart from that first PR that we opened. So apart from that, everything seems to be going smoothly on our side, so I don't know if people are looking for feedback on anything regarding offers.

Speaker 6: Oh. I opened up that really small clarification about Node ID and SCID. I opened that like five minutes ago, but it's pretty straightforward.

Speaker 0: Yeah, perfect Thanks for doing that. I think we all agree that it should be restricted the way you described it. I'll have a look at it this week. Okay then. Apart from that, nothing has been happening, I guess, on inbound fees as well. The spec cleanup PR that is waiting for interop, I guess, can be merged. I think that the LND release actually applied that, and we applied this in our Eclair release as well, and maybe CLN as well. I'm talking about this one by [redacted]. I'm going to paste the link here.

Speaker 1: Yeah, we flipped all those on.

Speaker 0: Okay. I think it needs a rebase and a bit of cleanup of comments. But apart from that, then it means we should be able to — I think the small rebates and some of the minor comments should be addressed, but I guess that when [redacted] gets back to it, we'll be able to merge that one. Alright. I guess we got to the end of the list, and we're early for once. So, if anyone has a topic they want to bring to the table, just feel free to do it right now.

Speaker 5: I feel like splicing is really close to being done. What is there to — is there stuff we should talk about instead of over the comments? I feel like we've mostly hashed it out.

Speaker 0: Yeah. I think all of the comments on the PR hash out most of those things. I think that once they are addressed on the PR and we converge on the TLVs and that kind of thing, then we should be able to do the interop. Once we agree also on the final state of quiescence — if we do that unquiesced message or not — then I think we should be quite close from being able to do cross-compat tests.

Speaker 5: Sweet. Yeah, I think the — how did you end up doing reserve requirements post-splice? Do you need to do a new channel?

Speaker 0: Yeah, that's the one I think what we do is that. Hmm. I need to double check. I don't remember what we eventually did here.

Speaker 5: Yeah, it'd be sweet to just drop reserve requirements post-splice, but I realize that's around the table. We're talking about adding reserve TLVs, I presume, to the open channel stuff. Do we want to mimic that for splicing? One thing we could do is just say: Hey, request zero channel reserve in the splice command. Maybe we just support that first, and then get around to the rest of the reserve requirements later. These are just ideas. What do you think, [redacted]?

Speaker 0: Yeah, that's actually what I did in the zero reserve PR I opened. The TLVs I'm adding to open channel, and accept channel too, I mentioned that the same TLV should be added to splice and splice add, and work basically the same way.

Speaker 1: Is this to change all the channel constraints broadly, or just the reserve?

Speaker 0: No, just the reserve. It's the TLVs from my zero reserve PR — the TLV that says just drop the reserve. Because in open channel and accept channel, the v1, the reserve is explicitly in the message. But since it's not in the open channel too, I had to add a TLV to say drop the reserve in that case.

Speaker 1: Because it's assumed to be 1%.

Speaker 0: Yeah, exactly. The main issue we had while testing it with users is that what happens a lot of time is that some users initialize their wallet by receiving a first small lightning payment because someone told them: Oh, install this wallet; it's cool. Look, I'm just sending you sats, and you get a very small channel. Then they do a swap-in, and that is much, much larger than what was initially there. So now, the reserve requirements get huge compared to the previous version of the channel. With our initial implementation, the channel would just get stuck with the usual feedback for issues where you cannot add HTLCs anymore because you would be below the channel reserve. But I don't really remember exactly what we did on the implementation side to work around that. So that is something that is not specified right now and should be properly specified. There were all discussions with [redacted] about that directly on the PR, so we just need to pick up the discussion again and decide what we want to do once we actually implement those things. Looks like nobody has anything else to add. First time we're going to end early. Alright then.

Speaker 6: Cool. Thanks everyone.

Speaker 0: Thank you everyone.

Speaker 5: Bye.

