---
title: "Lightning Specification Meeting - Agenda 1142"
transcript_by: Gurwinder Sahota via tstbtc v1.0.0
tags: ['lightning']
speakers: []
date: 2024-02-26
---
Agenda: <https://github.com/lightning/bolts/issues/1142>

Speaker 0: [redacted] said they won't be able to attend, but they’ve nicely created an agenda for us as usual. So I can take a look and run through the list. First up, so I think this has sort of went back and forth a few times. This is the very long-lived request to just have a zero value in reserve basically, like a first class type. [redacted] made this PR, so it's spec PR 1140. I think there's a back and forth thing. We realize that you also need to signal that you actually accept it — not just that you'll send it — just to make sure that things are just work without having some manual intervention. Pretty straightforward. We were wary of getting into a state inadvertently where a channel gets stuck because of some weird fee situation. So one thing we're doing now in 0.18 — something I think that was a very long and old portion — basically, I think that buffer thing. We didn't have the fee buffer. So basically, at times, we would have issues. Also, we do a thing now where we have some first compatibility with C-Lightning, where we would update the fee too quickly basically, we have to update [inaudible] as well. But that's the only thing I think of implementation-wise as far as zero reserve. I know people do it in the wild, but that doesn't mean they aren't hitting a fee-related XP.

Speaker 1: Yeah. I think the spec says you should be able to handle two times your current fee, and we actually wound back that. I don't know if we actually merged that PR for this release or next release, but if your fees are also historically really high, we figured the chance of it going to twice that is less. We have like a sliding scale, where we'll kind of have a fee buffer of down to 10%, but I can't remember exact numbers. [redacted] had some numbers. So, the idea that you should basically ensure that you can still get something through even if the fees were to jump by some factor or more — we've kind of dialed that back a little bit. But there's nothing objectionable on this feature that I can see, right? I mean, don't use it if you don't want it. And if you want it, now it'll be there.

Speaker 0: Yeah, same. Something that has been around for a while until an official patch, I guess like we should bring it in. It's just like it happened with zero conf for a period of time, so...

Speaker 1: Yep. Someone else has to implement it, and then do interop testing. I mean, you know, that should be pretty easy.

Speaker 0: Yeah. I think we also need to make a tracking issue for it as well, right? I'm sure I can just poke someone. I think Breeze has probably a few different versions of this patch sitting around. Maybe they can just contribute upstream assuming it applies cleanly, and it's not some of the most important fork. Cool. I'm guessing Eclair has one already because I think they've also had this deployed for some time just between their nodes and their mobile wallet as well. I guess we should catch up on the interop side with them. Cool. Check. Alright, trampoline. Seems like trampoline's back. I think LDK and Eclair did a bunch of work on it. I think just the packet format was the last thing I remember. I'm not sure if [redacted] is here or LDK.

Speaker 2: I'm here. Yeah, LDK. I was sick last week. I was making slower progress, but I have implemented unit tests and have full test vector parity with what [redacted] has produced, which I'm really excited about. We have the ability to be constructing trampoline packets. So now, I'm just building wrappers around that all the way until users are going to be able to just call methods. The next level that I'm currently working on is constructing a trampoline packet based on user specifications, like the structs that users are passing. And the next level of abstraction will be pathfinding that will incorporate trampoline-rod construction.

Speaker 0: Cool.

Speaker 1: You have to make some tiny modification to the spec so that you can name it the 2024 edition because it hasn't been updated in three years. It's currently on 2021 edition, which I know was a joke at the time but it's now, it's kind of old. So if you could come up with some trivial modification, that'd be great.

Speaker 0: [redacted], were there any changes to the format that happened or was it just sort of just coalescing towards what they already have? 

Speaker 2: No. I briefly suggested some changes that turns out would have made it more like rendezvous routing. The changes were about not nesting onions and just keeping everything at the same level —  unwrapping and rewrapping, and then unwrapping again. But it wasn't worth the additional complexities, so we're just keeping it as it was originally proposed.

Speaker 0: Got you.

Speaker 2: Now, I guess the only changes are really the TLV IDs, which [redacted] can expand on if they’re here.

Speaker 0: Cool. Then the thing about the PR, so I guess the one with 836 is like the version or — there's two PRs, right?

Speaker 2: I keep having to re-Google and reopen them.

Speaker 0: Yeah, so one is 836 and the other one is 829. 829 is the 2021 edition, that's what [redacted] was saying. Yeah. I didn't…

Speaker 2: There is one that most recently has been modified by [redacted] to incorporate updated test vectors. That is the definitive one.

Speaker 0: Yeah. It looks like this one has been updated most recently. 836.

Speaker 2: Then that's correct.

Speaker 0: Okay, cool. I was just curious. We've been just catching up a bit with that internally just after as we're working on blinded path stuff. I'm starting pathfinding, so it seems like they're related and can be composed. That's cool, but not the next release or anything like that — we're just trying to make sure we can get stuff into this one. The next release should be like March or at least, RC. There's RC in March, and then we'll go from there.

Speaker 2: Yeah. I think with LDK, the question really is: How much functionality do we want to incorporate? Because if it's just trampoline serialization, we already have it. If it is trampoline package construction, PR is open. We should be able to have it too, but…

Speaker 0: Have people thought about invoice stuff and how that combined with Bolt 11, Bolt 12 offers like that? I guess it's smaller than blinded paths or I guess — well, it's fixed size, right?

Speaker 2: No.

Speaker 3: I don't think for trampoline you're ever gonna include it in an invoice. It's more a thing to send to a known node.

Speaker 1: Yeah, The client goes: Oh, I have no idea how to route this, so I'm going to bounce it through the trampoline — kind of deal. So I guess you don't need a...

Speaker 0: Sure. That makes sense. Okay. This is like just packing construction because they don't have the — yeah. Sure. 

Speaker 2: Well, one thing you do need…

Speaker 1: There's a complimentary technology. There is a server-side idea, which is kind of similar, where you pay some node, handwave, to route stuff for you, and then you just redirect all your stuff to that node, and it figures out how to get it to you. But that's kind of separate. That's the other half, the incoming side equivalent of this, which doesn't exist yet.

Speaker 0: Were you saying something, [redacted]?

Speaker 2: Yeah.I was just thinking about whether it might make sense to incorporate in the invoice whether or not a recipient supports trampoline. I don't really think it necessarily makes sense because it is not the trampoline node that receives the money. The trampoline node is just the penultimate hop. However, would there ever be a scenario that we would want support where we are sending money directly to a trampoline node? I don't...

Speaker 3: Wasn't there a case? Eclair had something where they were — I think zero amounts were… The trampoline could steal some of the because the —  I mean it didn't commit to the amount. No, that's not right. There was some…

Speaker 0: Was that prepayment secret?

Speaker 3: No, it was post-payment secret. They had something where trampoline still wasn't safe, but I don't remember what it is now. So maybe just ignore it. Maybe it was fixed. We'll pretend it was fixed and ask faster in two weeks.

Speaker 0: Okay. Yeah, I don't really remember that. Okay, cool. Alright.

Speaker 1: Yeah, [redacted], hide that in the minutes somewhere. See if anyone reads them. There you go.

Speaker 0: Yeah. Question mark. Like, is there active vulnerability? No. Okay, cool. Next thing. Okay. I think it's like an offers thing around like another way to specify a node ID. Just so it's like less bytes. This is 1138.

Speaker 1: Yeah. Waiting on me for interop, I think. It’s pretty straightforward. 

Speaker 0: Oh, it's like a multi-format.

Speaker 1: Yeah, it's like we've got 02, 03 — why don't we just use 01 or something for, you know?

Speaker 0: I see.

Speaker 1: There's possibly a few places we could use it, but the most obvious place was in offers where people basically want to have a route and they want to say: Go via this. Because that's the ones that tend to be in the QR code. That's in people's faces, and it's length really matters. It's not particularly useful if it's a long live QR code that you wanted to tattoo on your ass, but it's because you're counting on that short channel IDs being around forever. But for many things, it would be perfectly acceptable, so it kind of makes sense. I think it's the least objectionable of all the different ways to encode it. So everyone hates it, but it is smaller, right? So waiting on interop, I think.

Speaker 0: Okay. Cool.

Speaker 4: I've got a somewhat related blinded paths question for everyone while we're here. 

Speaker 0: Sure. 

Speaker 4: I just wanted to ask: What is everyone currently doing for max CLTV expiry for a blinded path? Because I was testing my LND stuff the other day and I ran into a zero value. I think it was on an old version of CLM that I could get to build on my computer. So I just wanted to check — the zero value doesn't really make sense there because it's the highest height, which is except the payment. Does anyone know offhand if they are setting that to zero?

Speaker 1: Not deliberately.

Speaker 4: Okay, so I shouldn't — yeah, ‘cause right now, I was like checking if this is a zero value, just pretend it's not there because it's in like a composite field. But that sounds like the wrong thing to do.

Speaker 1: That does sound like a bug. Yeah.

Speaker 4: Okay. I'll see if I can reproduce that and then check it out.

Speaker 1: Yeah. Ping me about it because that's wrong.

Speaker 4: Okay. Great.

Speaker 0: Cool. Alright. Check that one. Channel jamming. So I guess there's this state thing. But I guess any general updates or anything here?

Speaker 4: No. No updates for me. I've been kind of trying to get the route blinding stuff done in LND.

Speaker 0: Gotcha.

Speaker 4: I think this week.

Speaker 0: Cool. Yeah. We have someone new starting, I guess, tomorrow. I think one of the other things we'll be starting to take a look at the blip and stuff like that, just in terms of integrating more deeply into LND or just having someone that is up to date on all the ways and goodness there.

Speaker 4: Nice. You did mention [redacted] last, last spec meeting, you mentioned there was something else that you might want to be passing along with update ad. Do you remember what that is?

Speaker 0: Yeah, it's for the tap stuff. It's just like an asset ID value for the channel thing we're working on, and it matches that; Hey, where do you need to depth plumbing? — just so that we make sure that's available. I haven't started to dig into it yet, just other stuff. But hopefully this week I'll be able to take another deep look at it.

Speaker 4: Okay, sweet. I just get an idea of the APIs that that would need. But I'll ping you on Andy's Slack.

Speaker 0: Yeah, that's not a good thing. It's something that I'm figuring out. So It's either just going to be directly on the API itself. Maybe there'll be some other config thing. It may also just be a top-level config thing, so not necessarily at the RPC level, but something that you can do if you're making an LND node in a cool process basically. But so kind of finish finally — that's when designs that we should have to think about that.

Speaker 4: Okay. Right.

Speaker 0: Cool. Alright. We got the newest, the newest thing on the block. DNS-based offers. I guess we talked about it a little bit the other week. 

Speaker 3: Yeah. I don't think there's very much to talk about here. I need to follow up on the offer set of things. I think the way forward that makes the most sense is to rip up the current design and replace it with just including the user and domain parts in the invoice request. That's nice and easy. But the next step there, I think if I recall correctly, was to define some kind of blip type range for the offers, invoice request, and invoice so that we can define those in blips.

Speaker 1: Yes, that's been sitting in the back of my head for quite a while, is that we don't have — so it defines well which parts you're supposed to mirror. You have an offer. You're supposed to copy the things in the invoice request and the invoice request copies things into the invoice. You end up with everything in the invoice, but we define those in very strict ranges, and we really should probably add an experimental range and define what happens if you don't understand something. Do you copy it or not? Do you rely on features to say which bits you understand and you just blindly copy all the fields, even if you didn't understand them, or is understanding them like an acquiescence that you accept the terms of whatever it is that you just copied? Someone needs to think kind of hard about that. Somebody else. if it's even, then you won't do anything with — because if you see an unknown even field, you're like: I don't know what this is, you're out. So that already has a semantic, right? So you will be an odd field.

Speaker 3: That's magic you want. Like, the person who creates the thing can decide whether they want it to be either you understand this and you agree with it, or you fail, or you ignore this if you don't understand it.

Speaker 1: Right. Yeah, but it's the latter one. You're like: So are they not gonna copy it because they didn't understand what it was?

Speaker 3: Oh.

Speaker 5: They need to copy everything. Otherwise, the data we put in the metadata might not make sense.

Speaker 1: You're hashing scheme breaks — yes. So I think you want us to copy everything, in which case, you go: How am I going to tell whether or not you got it? If I'm supposed to say I'm trying to handle both, right? I've got some optional field, and if you understand it, great. But if you don't, I can fall back or whatever. Then, you kind of need to know. Now maybe we need some features in there and if you understand feature 3015, then you understand that field. You will set the feature bit and then you'll do it. The point is it's gotta be defined.

Speaker 3: I don't see any hard metal ways of copying. Like if you don't understand it, oh well. But you should always copy because the hashing scheme for us, — sure, yes — but also there's just no reason not to. You might as well. There are certainly schemes where you want it, and then there are schemes where you don't — I don't know.

Speaker 1: Oh. Well, we do require some mechanism to indicate whether or not you actually understood it. Sure. That can be separate from inclusion.

Speaker 3: That can be separate. Right, yes.

Speaker 1: Yeah. Cool. So somebody needs to sync, think through all this, and this is an opportunity to do that.

Speaker 0: One question. This is so a single node can respond to offers for many different users — user registered users basically, right? And that's the mapping here.

Speaker 3: Yeah. Basically, the intent would be that you'd have one offer that just goes to you — you know, big custodial service or whatever — and then, the invoice request says: Hey, I actually want to pay this user specifically. And then, you could say: No. Or you could say: Great. Then, you can hide it in the blinded path so that when you actually receive the payment, hidden in your little encrypted blob, it says: This is for user XYZ. Then, you can credit it; and it's all nice and stateless, and seamless, and yada yada. 

Speaker 0: Cool. Gotte catch up on the trio of docs. Next, support mutual close. I was close last week. I'm even closer this week. Just doing some final unit test basically. Just some of these edge cases. I should be able to just get the PR out of draft this week, and then start to hit up [redacted] or whoever's around on Async side for some interop testing. The only things that I need to do is just make sure I'm aware of edge case-wise — some of the signature combinations because I think I've implemented two-thirds, the ones that made sense, but I should just do the other ones and when it's like something complains by sending it. Otherwise, it wasn't too bad. It was an opportunity for me just to do things in a very new way in LND, which is why it took long. I made some stuff on the side, refactors, et cetera. But otherwise, I'm excited just to get people co-op close, and see if it actually works.

Speaker 1: Cool. Yeah, I haven't gone back and revisited the spec because I have not even implemented it. So I look forward to you having ironed out all the stupid ideas from it, and then I can just follow and implement it. 

Speaker 0: Cool. Alright. Okay. Quiescence. I think on this, [redacted] and [redacted] are looking to do some interop testing between LND and Eclair. There's a scenario y'all are discussing, I think, [redacted]?

Speaker 6: We're going through how we want to go about testing because some of the stuff is like we're in a lot — do we want to mess around with the internals or do we want to just see from a point of view of outside users? I am currently working on an explanation for why we shouldn't actually try to put a whole bunch of internals instrumentation to do this interop testing.

Speaker 0: And by that do you mean something like some debug RPC to just send STFU or something or…?

Speaker 6: Well, or sort of measuring internal state about whether or not, like which one thinks it's the initiator. I don't think it's necessarily worth it, but…

Speaker 0: Interesting.

Speaker 6: I'm gonna be writing all this up and putting it in.

Speaker 0: Okay. But I guess TL/DR is that you feel like it's just better to test it in concert with something like splicing that actually uses it for an end goal versus saying am I flushed or something?

Speaker 6: Yeah. I'm trying to say we should be testing for things that are externally observable rather than trying to query internal state because I wouldn't recommend creating instrumentation in the internals of these implementations just to do interop testing. That's the domain of unit tests, in my opinion.

Speaker 1: Yeah. It's really hard to — because by itself, it doesn't do anything. Almost by definition. It just stops doing things. Our tests are horrible. We have this dev thing that can say: Hey send this; and it will start doing. Then, we look in the logs to check that both sides have done it and that there's no activity has occurred otherwise — right? — which is pretty pretty hacky. Yeah, you really can't test it until you have something on top.

Speaker 6: What I would love to be able to do is to get a framework that does protocol traces, where we can then start to do invariance checking over each side of the — basically, get a message stream one way, a message stream the other way, and then, just do a whole bunch of checks about what message orderings are allowed and stuff like that.

Speaker 0: We kind of have maybe two or three versions of that in various levels of maintenance.

Speaker 1: LN prototest was supposed to be that, but we've kind of abandoned it. We really need a good couple of rewrites and generalizations — all those things. But yeah, I mean, the important thing is that STFU goes away when you reconnect. That's kind of important. And you reset so you don't get stuck and that you actually do shut up after you've exchanged STFUs. There are a couple of corner cases if stuff is in-flight, but that's about it.

Speaker 0: Well, because I remember this came up — one question with that and splice. Let's say you have an actual channel; you do STFU; then you do a splice. Is the intent that you reconnect once confirmed or reconnect after the thing or is there something in the splicing that says: Okay, we're no longer in the STFU state? Because all…

Speaker 1: The STFU terminates, yeah.

Speaker 0: Okay.

Speaker 6: Yeah, That's something I'm not a huge fan of. I wish I would have understood that earlier. I thought that the point was that we were gonna reconnect after whatever thing took advantage of the stop traffic. If we wanna resume, then we should probably include that in the STFU proposal and not pepper it around all of the dependent proposals.

Speaker 1: [redacted]?

Speaker 7: What currently is: When you receive the signature for the splice, then the STFU is presumed to be ended.

Speaker 6: Right, but it does deeply entangle the two proposals in a way that just isn't necessary.

Speaker 1: Yeah, and if we're going to do other changes, then you're like: Well, should we have a STFU done?

Speaker 6: Yeah, and because dynamic commitments is going to try to make use of the STFU as well. It's like: Well, in that case: Can we do a resume in the STFU proposal rather than having to now say: Okay, in dynamic commitments, this is when we're no longer STFU. And then this, it's like…

Speaker 1: What if you wanted to do both?

Speaker 6: Maybe we save a message, but do we really need to save a message?

Speaker 1: Yeah. So, the reason it didn't exist is because the original STFU was for channel upgrade, where you reconnect to do it. But forcing reconnection in other cases is just weird and disruptive, right? Because you've got other channels, right? Why are you reconnecting for this one kind of thing? So yeah. I definitely don't want to do reconnect as the canonical way of resetting STFU, although it should reset. So yeah, I'd be happy with an STFU finished kind of, you know, come up with a cool acronym that's the opposite of STFU. Yeah, that's right, yeah.

Speaker 0: You could just call it OK or something. STFU, OK.

Speaker 1: Whatever, dude.

Speaker 0: Yeah, whatever. No, yeah, that makes sense. It seems like it would be, I guess, not a very elaborate cut out either and just like a way to decouple it — like [redacted] was saying as well — so you're not necessarily reliant on implicit sort of behavior in another protocol.

Speaker 6: I mean, this proposal is much easier to follow. 

Speaker 0: Yeah, Then there's a clear termination state or going back to normal basically.

Speaker 7: I think there's some weirdness, right? There are certain cases where the splice can't be abandoned. Like, if I've sent you a signature I haven't gotten from you, right? And then if you end the STFU in that point, that's going to be obviously the default, the force close, right? But it's not sure how clean it is to have just say this STFU ends, couldn't always work. We'll still be dependent on that…

Speaker 6: All protocols need a way to handle their state being essentially truncated, right? So it's like if you abandoned your interactive TX halfway through and you started going with your splice — what happened? The downstream messaging.

Speaker 1: It's equivalent to a disconnect, yeah. If you receive it at a time you can't handle it, you hang up on them and let them try again. 

Speaker 7: Right. 

Speaker 1: And you're like: I'm gonna pretend I didn't see that.

Speaker 7: This is implications for channel reestablish. ‘Cause there's certain cases where I've given you certain signatures and I haven't gotten them back. They get really complex to handle with re-establish. I can't think through live right now what they would mean if someone's doesn't at end STFU command at one of those moments. Like, what is the correct thing to do?

Speaker 6: What if you hang up at the same time? I think…

Speaker 7: Well, those are well defined, right?

Speaker 1: I think you treat them the same.

Speaker 6: That's sort of my point. If you already have a mechanism to resolve this halfway state commitment, and just use it for any sort of situation where you receive a message out of time. And if you don't have one, then you have bigger problems, right?

Speaker 7: Yeah, we can do that. It's just that the re-established stuff gets really complex really fast, and I'm not saying it does make it more complex, but it's something that I would think about.

Speaker 0: So, [redacted], without something like this, what do you do in that case? Let's say you're saying we're doing the splice. You only get one signature. The channel is still also just stuck, right? You can't do anything basically with that, right?

Speaker 4: In certain cases, yes. In certain cases, no. What you do is you reestablish and ask for the signature and stuff that you're missing. You demand that to restart the channel. Without that, then you have to force close everything.

Speaker 1: So yeah, if you receive an unexpected packet, you would hang up. You'd warning out, and you'd hang up. Or maybe you'd force close. But probably you'd just hang up and hope they fix it next time. Similarly, if they try to splice halfway through a splice and they send you other rubbish.

Speaker 6: Or send an update ad, right?

Speaker 1: Yeah, that's right.

Speaker 6: That's the thing, we can send you any one of a thousand different things that are going to fuck your whole world and it's like — I don't think there's a way to sidestep it.

Speaker 7: 99% of the splicing, we just drop the splice. There's just these key moments when the signatures are ones that has and ones that doesn't where it starts to get you. You have to be very careful with it.

Speaker 1: Yeah. So I think you would treat it as if they've disconnected except you would disconnect. You'd send a warning ideally saying: I don't know what the hell this is; you can't do that yet. You would disconnect, hope it doesn't happen again, and file a bug report. So I don't think it would be too bad. The only problem is that the breaking of existing implementations if you don't expect the STFU to be terminated — if the other side expects you to explicitly terminate the STFU and our implementation doesn't, what happens here? Because STFU termination would probably be an even message. So in theory, this would be a feed that change. Transient problems. We'll sort out some way of detecting that.

Speaker 7: Yeah, I think it could work thinking about it more. But one of the weird things is when you go through the reestablished mode, there isn't currently an explicitly defined STFU entering, and yet the code will assume that you leave the STFU when the splice finishes reestablishing, which is something I've been thinking about maybe to document more, but I don't know. It's complicated. 

Speaker 0: Well, yeah because it seems like you could send it again. It seems it's better to just have this explicitly be defined as well in either case because it seems like the state space, like you're saying. 

Speaker 1: In particular, the case where if in future we have a whole heap of things using STFU for, in theory, you might want to do more than one at once, and you can't do that at the moment. They would have to be segmented, right? You're like: If we're going to change dust limits using STFU or something, we wouldn't be able to do that at the same time as a splice because each one would terminate the STFU?

Speaker 0: Ah, yes. 

Speaker 6: That's sort of the point. I think that you want the proposals to be modular. The way I even see the splicing proposals, you have two different protocols. You have the main splice one, and then you kind of go into a new protocol stack frame, if you will, when you go into interactive TX. It's like that, but once you've agreed on the TX, then you're discharging that protocol and then returning back to your main splice. The way I see it is splicing and dynamic commitments sit on top of another protocol stack frame, which is your STFU. I'd like to keep those stack frames properly…

Speaker 1: Yeah, but on the other hand, you'd be like, from our point of view, you get a request to do a splice, or you get a request to do something from like the main daemon sends to you and you go: Cool, I need to be in STFU. If you're already in STFU, I think we would optimize — we're unlikely to force it in and out of STFU at that point. We would actually just go: We're already in STFU; we will do this while we're here. But yes, you need a separate loop that is your limited protocol for transaction construction. I don't think allowing random shit in there is useful at all. So, I'm saying you can slightly blur them and you can buy an STFU. I don't think you want to overlap them and have: Oh, while we're in the middle of a splice interactive TX, I am also going to send you a request to change dust limit or something. That is insanity. So yeah, I share your frame.

Speaker 6: Just because we can do something doesn't also necessarily mean that we should. That's the other thing. If you guys want to experiment with trying to sort of bash them together and stuff like that, that would be fine. But my point is that if we have a protocol that explicitly says: Okay, this STFU stack frame is getting dropped, AKA now you may speak, or whatever sort of resumption there is — at least there's a clear view on both sides of the channel what the protocol state is. Regardless of how you want to handle the actual software that orchestrates it, it's very cleanly separated, and you can look at the traces and see like okay this is the state that we're in.

Speaker 1: Yeah and I prefer more restrictive protocols like in interactive TX. I don't want to have to handle anything other than interactive TX, right? You should have like four messages or something that are possible. Anything else is crap. You should neither set nor receive. That's way, way simpler than trying to handle the intersection, particularly intersection of messages that don't exist yet that we add to the protocol, and then nobody thinks: Oh, but how is this going to interact with? Yeah, we don't want to go there. I agree.

Speaker 0: Cool. Okay. So, it seems like we're looking in the direction of creating STFU terminate to just decouple it from other stuff. Okay, cool. Which leads us into our next topic, splicing. I saw you made some tool, [redacted], sort of like a DSL to communicate or like the sequencing of the splice stuff. That looked pretty cool.

Speaker 7: Yeah, it's kind of scripting language, sort of. I was like mocking up what complex splices would be. And I was like: Why don't we just parse this? Like, a simpler form of doing it. So, the core idea is just be able to take a splice of tons of channels and tons of deposit withdrawals and stuff and just merge it into one liner script kind of thing. I got really excited about it and went really ham with it. and I think it's awesome. But yeah, working on that. I don't know if that should be a spec thing, but something I'm excited about.

Speaker 0: Well, yeah, I see something useful to get a feel for API-wise. I think an interesting thing as far as you're saying. Sort of like a way you can declare it if you communicate batch splices across several different channels, which seems relevant for the big nodes out there. But I'm assuming maybe you'll get more experience with it, and we'll go from there because otherwise, API-wise, I haven't thought — I guess I've only thought in the single splice, like single channel, single splice, obviously you can batch it on-chain, and there should be a way to communicate that to some API level. There been any changes spec-wise?

Speaker 7: Yeah, I wish [redacted] was here. I've been going back and forth on a bunch of things, but I guess they couldn't make it. There were a couple of little things I thought I could ask while I was here. The original splice command has the chain hash in it, and [redacted] was saying we don't need that because we have the channel ID. I'm guessing there was something to do with that. Maybe [redacted], do you know?

Speaker 1: Yeah. Well, originally, the open you needed to because you didn't have an existing context, right? You were like: I want to open one of these; and in theory, it could be a different chain or something. So yes, that is redundant in the context in any channel message, right? I think: Yes; no, I'm not going there and like a channel that has multiple; no, let's just…

Speaker 0: Yeah, I don't know about y'all, but we actually ripped out Litecoin in the past release. Like it was just there and had some hacks around it. So maybe we were the last ones. I don't know.

Speaker 1: We may have ripped it out. I don't know. No one's said it. 

Speaker 0: I think for us, it was working for several years. No one complained. So, we're like: We can wrap this thing out now. 

Speaker 1: Oh, yeah.

Speaker 7: The other thing we were messing with now that we're getting close to finalizing it — we just dodged the post-splice reserve requirements problem, and we kind of have to answer that now. There's a couple competing ideas of ways of doing it. Let me find my notes here. One second. Right. So, one idea is treat it as a fresh channel, so all the reserve requirements is to reset as if it were a fresh channel. The second one is to follow the old channel reserve requirements until the new ones post splice are met and then swap over to them. The third one is just drop the reserve requirements entirely. Apparently [redacted[ messed a lot with the second one and found that to be extremely complicated, according to them.

Speaker 0: I can see that.

Speaker 7: That's kind of an up-in-the-air question, really.

Speaker 0: I guess dropping it entirely just means implicit zero reserve, basically?

Speaker 1: No, because this should fall out of the zero reserve channel type, right? If you splice and you say: This is the channel type I want the result to be, and that type is zero reserve; then you've got your answer. But your restrictions are always like the minimum subset. How does this work? The most strict of all the splices that are possibly happening at the moment, including the one you're on right now. So that falls out pretty naturally with reserve, like who's got the highest reserve? That's our reserve. It does allow you to do stupid things. If you're assuming 1% reserve and you splice in a 100x channel, now you're kind of fucked because you're in reserve until that, but don't do that. Yeah, people can always do things that are stupid. Yeah, you'll have to wait until…

Speaker 6: Don’t splice at 100x. Just open a new channel.

Speaker 1: That's right, exactly. But I do think it dovetails pretty nicely with the zero reserve feature. You would say: Hey, I want channel type zero reserve. That's fine. And then, you would still have the reserve until that splice is confirmed, and you're on that for sure. But the nominal, like the worst case requirement of all the splices and use that, applies to reserve as well. I think that's pretty simple.

Speaker 7: Are we allowing that kind of channel change on reserve requirements during a splice or is that happening somewhere else?

Speaker 1: You should have a channel type in there somewhere because it's the obvious thing to do. For example, just because your existing channel doesn't have anchors doesn't mean that your splice won't have anchors, right? You should be able to control that.

Speaker 6: Yeah, so this definitely has implications. Like, if that's the route that we're going, where splicing includes channel type conversion and stuff like that, then it does very much intersect with a lot of the dynamic commitment stuff. I know that we have talked about that before?

Speaker 1: So what's an opportunity if we don't do it, I think, right? I mean, it's…

Speaker 6: Well, I agree. I'm not actually saying that you shouldn't do that. What I do want to say about it though is that the way that we're currently planning to handle that with dynamic commitments is that the new, like the re-anchoring step — and this is where it kind of differs from splicing because like not all of your channel liquidity is available until the actual splice confirms and with dynamic commitments, the whole idea is like we're not trying not to go to chain with the re-anchoring step immediately. It's supposed to be kept off-chain. And so at the moment, we only enforce the new channel requirements. We enforce the new channel-like constraints or whatever long before the actual UTXO turnover happens. Does that make sense?

Speaker 1: Isn't that the same? So the splice rule is that you do the worst, the minimum subset kind of requirement, which in your case falls back to the same thing, I think. If the new splice requires you to have more something, then you have to have more something immediately as soon as you propose it. I think that's true.

Speaker 6: But I think the difference is that the dynamic commitment rule is not most restrictive. Because it's not contingent on a bunch of different competing. Because this requirement comes from the fact that you can have multiple in-flight splices.

Speaker 0: Can you reject a splice as is today? Is that in the protocol today?

Speaker 6: Yeah.

Speaker 0: Because otherwise, you might want to reject the channel type upgrade. It could be a dog breed or something. If that is alongside of it.

Speaker 7: Yeah, we use the tx abort command, which is already there from interactive tx, and it's kind of a general reject.

Speaker 1: So, if you're not insisting — oh, I see. Yes because you're — huh.

Speaker 6: These proposals are very related, but also they have very key differences.

Speaker 1: Subtle differences.

Speaker 0: Yeah, I feel like we've been trying to mash them up for some time now. But I mean, I think just based on all the momentum splicing already has, I feel like it should just progress. But if there is that magical cutout that comes to someone with a moment of insight, we definitely entertain that.

Speaker 6: The key difference here, and this only even applies to a subset of splicing use cases, but if you're splicing out, you can actually just invalidate your final commitment on the previous UTXO and then just wait for the splice to confirm. But the problem is if you splice in, then you're pulling in new inputs, then you can invalidate the transaction because the splice depends on the… 

Speaker 1: You can do that, we can't.

Speaker 6: Yeah, exactly.

Speaker 1: Exactly. So, if you're not changing anything, then you get more power. You make a lot more assumptions. You can go: Cool, this is definitely going to happen in a way that we can't because we're taking in random bullshit from the other side. So yeah, that does give you a window that we don't have, which is kind of interesting. You don't have to wait for anything to happen because you can go, well, it's the only way this thing is going to exit, which is kind of nice. Yeah. Okay. So is your plan to like, other than not waiting, presumably you will actually output it, and it will be broadcast, and will eventually happen, right? But you don't care?

Speaker 6: Yeah. We had a thought that maybe if we wanted to co-op close the post dynamic  committed channel at some point that we might close it off the original UTXO, but I don't think that's going to be good for anyone. So, I think the goal is that in all cases there is an eventual confirmation of that re-anchoring step.

Speaker 1: Well that's where that's where splicing already has that because our closes will apply across all of them. So in theory, you get that for free because we have to. We have to close all of the in-flight splices just in case one of them goes through, right? Our mutual close code already covers that. So you might get that one, which would be nice.

Speaker 0: One of the distinctions I think worth mentioning here, I think there's two classes of what we're looking at in the requirements. One is where you have a kickoff that you never want to broadcast, right? And this is the whole: I went from basically SegWit V0 to basically V1 now in the new type of channel. That's one that has a little more special handling. The other variants where it looks like we're going to the new anchor code and format that would necessarily require the special handling. That one can be combined a little bit more. It's just the case of having the kickoff that you're not necessarily going to broadcast and certain occasions of that. For example, we're discussing if you have that kickoff and if you do a few different instances of it, you need to revoke the old one: Is it okay that you can just rely on someone broadcasting the second level so we have the second level HTLC? I think that's where things start to diverge a bit. I guess also some of the negotiation up front. If, for example, you're doing parameters like dust, you can't just say: Here's a new dust. Maybe I want to have my own dust as well. But it feels like we'll end up with 60 percent shared module here somewhere and maybe there's just like two different interfaces. I'm not really sure how it's going to turn out in the end. There's a lot more concrete code for slicing, so there's only that.

Speaker 7: We're talking about just changing everything up. What about adding some TX to the closed transaction? Make that a split.

Speaker 0: Yeah, that's a long-term feature. I think I got bumped a week ago as well. Yeah, that would make a lot of sense, but I guess one thing at a time maybe.

Speaker 1: Yeah, that one, as long as we use this parallel construction trick, where you both get to construct whatever you want, then it's really nice. But again, it's got a 30% overlap with — it's not quite the same interactive construction, right? Because I will let you add anything, whatever the hell you want to yours, and you will let me add whatever the hell I want to mine, because you don't care, which is kind of cute. But it's different from interactive TX, where you're mutually trying to build a transaction. You're actually trying to build two separate ones. In the construction for closed case, it's slightly different. It uses the simplified closed ideas,, just in interactive format. So it's similar, but it's actually not the same.

Speaker 0: Cool. Okay. Going down the list here. Taproot. So I think Eclair is working on a version of this, so they asked some questions. Just waiting for interop chance. On our end, nothing crazy has happened on mainnet still. Some people are using it, some people aren't. There was like a bug or two, but nothing shortstopper wise yet. I think last time we talked about there's like a spec PR up now for MuSIG2 stuff. Maybe that gets merged and you know, monthly trees and things like that. I have to check that one at a later time. Okay, here it is. Yeah, it was opened on January 6th.

Speaker 2: How is user demand in general? Are you seeing a lot of people asking for it? It seems that the fee rates have calmed down a little bit since, I think, what we saw at like 600 or something stats per vbyte this one time. Because I'm thinking while fee rates are calm, people are probably not gonna be demanding it, but with 600 sats per vbyte, even taproot is probably not gonna see the sort of savings that people will be looking for. At that point, we probably would need something like cross-input signature aggregation. Do folks have any thoughts?

Speaker 0: I think that's one factor of it. I think another factor you can say is that people just wanting to run lazy. I think Zeus is now looking to make a default, or at least if it's available for the user. But I think the bigger thing to me is just the progression of the top channels to gossip to PTLC. PTLC gives us a bunch of stuff as far as privacy improvements, and also things like the form-hole attack, which I think we were looking at some other variants of it. So, it's a means to the end to get there. I think we have the path of doing the different PTLC that was ECSA and Schnorr, but we didn't do that. We committed to the Schnorr roadmap. I think, to me, that's the end goal there. But I think it's primarily used by mobile wallet stage because obviously you don't need to run it on purpose otherwise. We do have the gossip stuff as well. We haven't given a code for it, but we pause because we just want to make sure we have good feedback because we would literally make LND net if we just released our own gossipers. We definitely don't want to do that. So to me, the end goal is getting to the PTLC land, and everything else is a stepping stone in between that.

Speaker 2: Fair enough.

Speaker 1: I like that it's got cool points, right? That's giving it a bit of a tailwind. Like, people are like: Oh, I want taproot, why? I want taproot. It's like: Okay, dude; cool. Yeah, I agree with you. Like, the payoff is further down and it's less instant gratification for users, but it's nice that they go: Oh cool, taproot. That's nice.

Speaker 0: Yeah, and I saw that Eclair has stuff recently where they're doing a Taproot variant swap. It's like they also figured out miniscript stuff with that as well, where they have a way where someone can import a backup type of thing. I think there's a tooling thing there as well. Not to say that it can't work, or maybe it can work either way, but I haven't dug into it as much there. But yeah, fees are down now, but hey, who knows next month? Things are all top. 

Speaker 1: Usually, yeah. Like a fucking goldfish. It's like: Oh no; fees aren't there anymore. But wait, hold on — you were freaking out like five seconds ago. 

Speaker 0: Yeah, exactly. 

Speaker 1: They'll be screaming again soon. Don't worry.

Speaker 0: Yeah, exactly. We were working on in Diatina just general to just improve feed bumping. Basically, so it's like number one, delay base and number two, also getting ready for it's also getting ready for [audio glitch] some of the new code format changes as far as not sweeping anchors together; things like that. So, we are working on that stuff. I'm for it because you're working towards a winter, you know, maybe comes and goes.

Speaker 1: Did everyone else just get some [redacted] rap in there?

Speaker 6: Yeah. ‘Getting ready for.’ 

Speaker 0: Wait, what happened?

Speaker 7: It's a glitch in the matrix.

Speaker 0: Oh, a remix? Okay, alright. I saw you on the active. Did I say something funny?

Speaker 1: ‘Also getting ready’ — five times. It just kept going, man.

Speaker 0: That's funny. Cool. But yeah, gossip stuff. We have some code. We're just basically waiting on some additional feedback from other people because we have to do all the same thing for this one to have a single network. So we're just chilling on that. I think since then, [redacted] started working on supply path stuff. Attributable errors. I know this progressed a bit. I know [redacted] and [redacted] are going back and forth. I don't know what the latest is here though. But maybe I'll write down to have updates ready for next time. Peer stories back up. We have someone working on this now. There's an issue with PR just for the wire messages. I think there were some comments in the actual PR around messaging and stuff like that.

Speaker 6: I am going to be taking a look at that later today.

Speaker 0: Cool. Nothing right there. Offers. Actually, we covered it a little bit earlier with the multi-format for node identifier.

Speaker 1: As far as I know, [redacted]’s doing the human readable enhancements, which has opened a can of worms for how we handle unauthorized ranges; and there's the SCID or pubkey stuff. That's really the only thing that I know of.

Speaker 0: Okay. Channel reestablish. I think this one is just waiting on — review limbo. Just codifying some edge cases and how things work today. Cool. I guess for the last few minutes, anything else people want to chat about?
