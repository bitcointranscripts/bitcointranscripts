---
title: "Lightning Specification Meeting - 1152"
transcript_by: Gurwinder Sahota via tstbtc v1.0.0
tags: ['lightning']
speakers: []
date: 2024-04-08
---

Agenda: <https://github.com/lightning/bolts/issues/1152>

Speaker 1: Yeah, we did a point release to undo it as well. What I'd like to do is to write up the spec changes to basically say: Yeah, don't set the bit if you don't have anything interesting to say — rather than if you don't support it. Yes, my sweep through the network to go: Hey, there's only a few nodes that don't set this. Missed LDK nodes obviously. There are only a few of them that are public. I guess this is like a warning that just looking at the public gossip network and going: Hey, there's only like six nodes that don't support this, is not necessarily indicative of all the private nodes because they were only setting it in cases where there were an endpoint that wasn't doing gossip maintenance, so we weren't seeing those, of course, on the published network. Well, we found out.

Speaker 0: Okay, cool. That PR is still open, I think. 1092. 

Speaker 1: Yeah.

Speaker 0:  So, I guess, is that change in this PR now is making that one back to optional?

Speaker 1: Yeah, I haven't pushed the change, but I'm going to push it.

Speaker 0: Cool. For the mutual close, I think last time we talked about moving towards lock time. I haven't done that yet because I ended up not making our release. I was like: Okay, I'm going to focus on things that are making the release. That should be a pretty straightforward thing to do. I definitely anticipate a metric or two having interop with Eclair on that, and then see where we go from there. But otherwise, our PR is up, and at least works LND to LND. We just need to make that change and then actually get some other testing out. Cool. There's this other PR that I put up, which I guess I can plug now, which is just sort of updating some — I guess [redacted] isn't here, but updating some of the syntax for wrap lining stuff, which is this one, 1151. Just before, it was using this like parenthesis, which made it look like you were calling functions to me, and then I did underscores. GitHub now supports LaTeX rendering. So, I think there's some discussion like: Do we just do the underscores now and then do the LaTeX more broadly across everything? The upside is it looks great on GitHub because now you have everything type up properly. But if you're looking at the raw markdown, you see a bunch of random lines and stuff. So, that's the one visual trade-off there. But if not, we can just do the first one. But I mean, this could be like a typo rule type of thing, but I would just actually download and route find and be able to review all this code, and this is something that popped out at me.

Speaker 1: Yeah, wow. GitHub supports — I did not know this.

Speaker 0: Yeah. I mean, it's pretty cool. You can do diagrams, markdown, and stuff. It's nice. It'd be cool to incorporate some of the diagrams in the future as well — like the flow sequence diagrams, state machine, and things like that — just to revitalize certain order parts of the spec, where we have ASCII diagrams, which are cool. But yeah, this one gives you a little more.

Speaker 1: Oh, nice. Yeah, I'm all about this, yes. I mean, I'll just check the rendering, but other than that, this is cool.

Speaker 0: Yeah, I mean, yeah, so I guess we can discuss anything if we either just, because I think [redacted] wanted to do everything, so I can either just do a little bit in this one and then do everything in another one or otherwise, but I guess we can just keep testing that. 

Speaker 1: Yeah.

Speaker 0: Cool.

Speaker 1: Other than actually reading through to make sure we haven't introduced typos, I'm happy to put this under the spelling rule. 

Speaker 0: Cool. Yeah, the other thing I wanted to commit also was sequence and flow diagrams for the co-op close stuff as well since it's a little bit different now and you can copy paste it. It's nice too because it's just static markup, so it's like actually in Git and you can see if the diagram changes over time or whatever. It's easier than typing dash a bunch of times for ASCII. I don't know how people do it, but anyway, [redacted] is pretty good at the ASCII diagrams. We can ask them.

Speaker 1: Yeah, it's the 1970s calling, they want their ASCII art back.

Speaker 0: Cool. Last time, I think we talked about some liquidity ads, questions around renegotiation and stuff like that. I think it was initially advertising in the node announcement to break it up basically. Oh, there was thing about the inputs. I'm not sure, but I remember we talked about an init thing too, where you would have that no announcement and then inside, in init, you would say — it looks like that's there. Well, it looks like everything is in the PR now. I haven't checked everything out yet. Looks like [redacted] took a check of that. 

Speaker 2: Which one is this?

Speaker 0: This is 1145.

Speaker 2: Okay.

Speaker 0: I just put that on need review. Yeah, because I think 1135 is split out a bit. This is just advertisement. People didn't, I guess, decouple like advertising and negotiation from whatever enforcement may look like, which may differ from place and location. Cool. What else? Where did you do the SCID thing for no nums or onion? Okay, no, that was closed. Sorry not to go down that path. There's async payments drafts, which I remember came up last time. I haven't had a chance to check this out yet myself. I know there was the lightning thing in Italy. The other extreme people talk about this a little more IRL, but that's also part of life. Some people aren't here themselves.

Speaker 0: I don't think there's anything new on Trampoline. Last I remember, packet update, which didn't happen, and then I think they're doing some interop. LDK was getting ready to be able to do some basic parsing or otherwise, interop. And we were thinking about, internally, just other discovery stuff — if you are really starting from nothing or if you have a graph or not, and so forth. Yeah, I see a PR merged. From LDK doing serialization.

Speaker 3: What was this for again?

Speaker 0: Trampoline. Any new…?

Speaker 4: Yeah, we have very early stuff right now.

Speaker 0: Done. Quiessence. So I think Eclair and LND were doing some interop testing on this. I know if you have anything to fill in there, [redacted]I think you're on like a few…

Speaker 2: In regard to STFU?

Speaker 0: Yeah, because I think last time, there is to have an in protocol resume instead of reconnection, and I think then they went down that line.

Speaker 2: Well, so we haven't done that. So just a couple of things. Number one is yes we're doing some interop testing between Eclair and LND right now. That's revealed a bug in the LND implementation, which I'm currently fixing. I'm also going to be putting together — probably tomorrow — a draft of the resume message. Just to do point separation and whatnot and just detailing all of the actual sort of semantics around recommendations about what happens if these messages come out of time. Because that was the main concern. How do we wrangle the complexity of: Okay, if someone says resume, and then they do another splice message, or if they do premature resume while you're in the middle of another protocol. Like, all of the sort of edge cases that that entails. I think that once I write all of those out, I think people will find that the actual complexity above and beyond what you would have had to handle anyway for random disconnects is actually just fine.

Speaker 0: Cool.

Speaker 2: But I'm fixing this LND bug first.

Speaker 0: Cool. How do we move that along? Related to that: Splicing. I saw [redacted] and [redacted] have a live stream code review thing. Anything kept coming out of that, or anything that went to the spec, or other stuff that we should be aware of?

Speaker 4: It's mostly all around my new flight script specification. It's kind of like a language shorthand for doing multiple complex splices kind of stuff. Making progress on that.

Speaker 0: Cool. So, is the current PR live for — I guess I'm trying to find which link I'm even looking for. Because we still have 863. I guess it seems like 863 is sort of in an indeterminate state, where it's had a bunch of review. There's a bunch of code for it. Is the plan to have [redacted] officially adopt that and move that out of the draft? Or were we in implementation land because there were a bunch of stuff that popped up? Just curious in terms of where we are with the spec part of it.

Speaker 4: Yeah, the current plan is a big to-do list of things. I'm working back and forth with [redacted] on. The list keeps growing, but it's eight or twelve things right now. Something like that. If you do those and then interop with Eclair on splicing. There’s probably just more things on the splice spec I’d imagine than those.

Speaker 0: Yeah, ‘cause I'm imagining there will eventually be the interplay with STFU and splice. Because I think Eclair is saying right now, because of their deployment environment, most of the time the code is clear if it's on a mobile wall, so it's not that big of a deal. But in running nodes, then the STFU matters more because of traffic and stuff like that. So, I think those streams will hook up. 

Speaker 4: I think the plan is to merge STFU and the splice spec, currently.

Speaker 2: I'm sorry. You're saying literally take the two documents and make them a single one?

Speaker 4: No, the PRs. Right now, we have PRs dependent on other PRs. We're going to fix that.

Speaker 0: I think it means a shared branch kind of. 

Speaker 4: Yeah. 

Speaker 0: Because right now I don't think there's no awareness — I don't even know if the STFU or the splicing spec references STFU at all. I'm assuming there needs to be to use STFU as a black box…

Speaker 2: It does.

Speaker 0: Oh, it does, okay.

Speaker 2: But it's a reference, it's not, I think, a PR dependency, like you said.

Speaker 4: Right. Let me just pull it up instead of just trying to do it from memory.

Speaker 0: Sure.

Speaker 4: We got a whole thing with this. But since dual merge now, we can fix some of the PR dependencies.

Speaker 0: Cool.Then the to-dos you mentioned, are those in a gist or an issue somewhere or is that in someone's fork of the spec or something?

Speaker 4: It's all on the Lightning GitHub PR for the splice draft.  It's in the comments there. There's a lot of chatter, so you can just scroll up a bit.

Speaker 0: Okay. I see it now.

Speaker 4: As opposed to the bunch of checkboxes and stuff.

Speaker 0: Yeah, I can link that in. I got that on my notes. Cool. Okay, moving along. Taproot stuff. I think there’s no new stuff. Haven't had any issues in a while or anything like that. I have one or two things that we fixed. I think Eclair is working on interop now, or rather working on the implementation for us to eventually get to interop, which would be cool. Remember last time I linked the secp-pr? I think it is getting more review now as well. It has comments five hours ago. Seems like it's moving along. Also, [redacted] is integrating it in bitcoind as well, so that'd be good feedback for them from another angle as well.

Speaker 4: I looked at the PR. I was fixing up PRs. The STFU one isn't merging. There's one about changing the TX signature messages in interactive TX. That's the one that's merging into the splice. Totally unrelated to the STFU.

Speaker 0: Gotcha. Similarly, gossip. I think we're just sort of like a holding pattern there in terms of when people have cycles to give some feedback. We have web draft PRs, and I think we just moved to getting things through for .18 on that. I think last time, [redacted] was somewhat interested in taking another look at it, but I'm not sure where they left. I think it'd be cool to stamp this somewhat because I remember, last year, [redacted] did a lot of research on PTLC stuff in general. How the modern state machine is itself, advocating for simplified commitment, and things like that. I think that's another sort of chunk there. If we're having all this additional interaction, should we just go with a simplified version? What's the action gonna look like protocol wise? I think that's where it sort of leads into there with other equipment changes, which, ideally, by then maybe — I guess that's another thing: Will the TX V3 stuff coincide with things that we're doing around this area, or are their other work streams that we combined? But I think we're holding pattern to fill out some of the changes in the future. Cool. PR backup, I think we're making more progress on implementation. That's something one of our interns is working on. I think some PRs were split off. It's not going to make .18, which is one that we're trying to get to RC on desperately, but it will be in some other next one basically. It'll be a feature bit thing. People can use it, interop, once we figure out some code stuff. I don't think — yeah, it should be straightforward to use.

Speaker 2: Yeah, that one's nearing completion. 

Speaker 0: Cool. That’d be cool to have. It's not on here, but blinded path stuff. So, I think this is one of the things that we wanted to make sure to get into our upcoming release, I think we're pretty far along. I think [redacted] did a bunch of interop testing — has some interop with everyone that has been doing it. We just have one or two more PRs. At least one that's up right now, of error handling, which I think is pretty far along. Trying to catch up with the latest. I don't know if you have any other updates you want to give there, [redacted]?

Speaker 5: Ah, no. It's just one more with error handling and flipping the feature bit on. I'm waiting for itests, and I'm going to request review.

Speaker 0: Cool. Exciting.

Speaker 5: Oh. Actually, I do have something here. When I was testing against CLN, [redacted], I mentioned a while ago that the max CLTV height I was getting from CLN was wrong. I did manage to reproduce that on a recent release, and I opened up an issue. I think it's a common issue rather than a state one.

Speaker 1: Great. I will put that on my queue. Thank you.

Speaker 0: Okay, cool. Channel jamming stuff, I don't know if there's anything explicit here. The one thing is that, I think I mentioned a bit ago is that I was starting to hook up certain things around making the update ad TLV blob more accessible. Or rather, you being able to set that either for payments or also forwarding as well. I think everything was mostly just there. There's a place I had to modify the DB slightly, but I say that it should be more accessible now for other high-level stuff there. Oh, there's another thing too — one thing that we're doing as well is, right now we have the HTLC interceptor which only lets you basically intercept the HTLC. We're adding one as well that lets you transform it on the other side, or have better capabilities, which I imagine would be useful for something that's using the adjustment bit. So, I got the bit set on the incoming. Maybe I wanna actually unset on the outgoing. I think that's just some API that we need for other stuff that will also contribute to progressive deployments here. We have someone that started that I think will be working more in this area, but they have a starter project that's a little bit slightly unrelated that I think will be digging more into channel jamming, blinded pass, and all that good stuff.

Speaker 5: Okay, nice. Yeah, that sounds great. The only channel jamming thing I have is that I just will have that blip open to start going on the experimental feature bit. [redacted] took a look at it. Thank you for that. I guess it is ready for a look if anyone is interested. It's just setting the experimental bit for a period of time and relaying it. The only real question here is: It's one byte of information — [redacted[ pointed out — is this a scale or a bit field? For my purposes, I just need a one or a zero, but I'm just waiting on promise to know whether or not a sync actually still want to go ahead and use the full eight bits. But other than that, I think the PR is pretty straightforward. So if that can get review, I would be very grateful.

Speaker 0: Cool. I'm going to drop that in our chat too. Done. Offer stuff. I think last time there's the thing: Any message, should they add that SCID thing? Seems like people didn't go in that direction. I think people are just in interop mode still here mostly. Yeah, I just saw the PR. Okay. LDK supports it as well. Cool. I don't know if you have anything you gotta add there [redacted] for offers stuff.

Speaker 3: So, a SCID directed key — it's not the one. That's 1138. 

Speaker 0: Oh.

Speaker 3: So, it's in the offers PR. We only do that for instruction node essentially and not in your house. So yeah, I have a PR. We're hoping to merge it soon. It does parse and handle them, but it doesn't create them. So, I'll add that with shell d self.

Speaker 1: Yes, we're in a similar position. We have a PR, but I've got to write the creation code just so I can test if the PR actually works.

Speaker 0: Other thing was [redacted]’s DNS offers thing. I don't know if people here have had a chance to check out yet. It's still on my list in terms of understanding off and off the bottom. This is the DNS thing. Attributable errors. I think this one is still holding pattern. I mean, we had some interop, I think it just sort of fizzled a bit as well ‘cause I think it started to spend some time elsewhere. Speaking of this, we ended up merging in a basic version of the old amount fees thing. Basically, restrictions on it are like: No positive fees, has to be backwards compatible, negative only. Also, I think we support positive, but we reject people doing the positive, because otherwise, you will have payment failure. I think the things that we're looking for is number one, looking on Gossip Network — basically, see who actually sets the field in general, which will get us an idea on the uptake and run the Network. Also, I think we have logging in place that'll show if people are aware of it or not. If someone pays more than they need to, you can save or have a discount that basically shows that the sender isn't updated. So, I think we'll be able to sample both: The number of nodes up here that are setting the field and running the network and the number of senders that are aware of it as well. That is all something that we'll be getting into our upcoming release. Then, hitting the bottom of the thing, there's that old channel reestablishment thing, that's only checkout, and that's related to only force close after they send an error thing as well. We'll probably take a look at that once we start to look at using the peer backup for more stuff. Or actually, using it effectively in our backup protocol. Cool. That's about the end of the list.

Speaker 1: Wow. Nice.

Speaker 0: Turbo speed.

Speaker 1: That's what happens when you cut and paste from the last list and don't add anything.

Speaker 0: Yeah. But I mean, I think there's a lot of interop stuff going on generally right now. They're just fine tuning. I can put that name up here as well. Okay.  I just posted my stuff. Anything else from people while we're here?

Speaker 1: No. I pushed the rebase of that feature cleanup although there's still a discussion on static remote key, which I disagree with. So, I'm going to comment on that.

Speaker 0: Is the idea people want to keep it still or…?

Speaker 1: Well, people are worried that — so, there's a nasty thing that we have a dependency at the moment that you're not supposed to offer anchors without static remote key, but we kind used that to say: Well, of course you're going to have static remote key. You can't have one without the other. But if we remove static remote key and you want to basically say: No, you've got to have anchors, then one logical way to do that would have been to split dependency and then have — you don't advertise that at remote keys. People go: Well, if I don't speak anchors, I can't. If you make anchors compulsory, the problem is then next time we have a new channel type, if you want to support that, then you're like: Well, anchors isn't really compulsory anymore, is it? Let me have anchors v2 or ephemeral or whatever the new thing is. I mean, fundamentally, we don't have a Turing complete language for like 10 to 10. You've got to approximate somewhere. So, I have to think harder about exactly how that is going to work. I think it still works, but I don't want to paint us into a corner when we go to upgrade next time and go: Oh shit, I wish we had done that right. But I think the right answer is for the moment, everyone should just ignore static remote key. When that rolls out and everyone's just ignoring that bit entirely, we'll be doing the right thing — which means that you can set it or not. So, older nodes might go: Oh, you don't support that; I'm not gonna connect to you. But that's pretty weird. I think the rate we're going, everyone supports anchors at the moment. I mean, if you made that compulsory today, I don't think you'd lose much at all. The only problem we have is existing channels.

Speaker 0: I remember there was something in the past where we tried to flip this anchor key bit early, but then we realized: Well, if we flip the bit and we had a non-static channel with the other individual, we would fail the feature bit comparison and we would need to reconnect. So that was one little, I think, quirk we realized with the init-level feature bits and how you compare that versus the other ones. But that was one thing that I remember. There was a slightly unforeseen interaction there.

Speaker 1: Yeah. If you mark it as basically, then you can just ignore it and that should work. But the other thing I want to do is the simple upgrade for channels, where we can do an upgrade without having to actually change the on-chain transaction. We should probably push that forward. We had it for static remote keys as an experimental option. We should dig it out again.

Speaker 2: Yeah. I don't know if you want to look for this, but that is going to be part of the first implementation of the dynamic commitment stuff.

Speaker 1: Yeah. It might be worth it. Maybe I'll leave it on the shelf for now and then, we can talk about dynamic commitments.

Speaker 2: The thing is that the way the dynamic commitments spec is written right now, you can reject commitment negotiation for any reason. So, you can actually do a partial implementation of the spec. You can be like: We're just going to upgrade channel constraints and screw all the taproot upgrade stuff. If you ask for a taproot update, we'll just say no all the time. That way, later you can then say: Okay, let me go implement the taproot upgrade stuff. Then, we won't reject those anymore. So, that's an option for you if you want.

Speaker 1: Yeah, that's nice. I mean, that also would let us flip everyone onto anchors, right? It's a bit trickier under the covers. We did this dumb thing for static remote key, where we remembered the points at which we changed, but if we were smarter, we would have just had our on-chain ID. Just try both, and go: Huh, was this static? Was this not static? Just cover all the cases at recovery time, rather than putting new entries in the database to go: Hey, these are the exact levels where we actually flipped it on, which is what we changed. Originally, we just had a flag to say if we are static or not and then, we changed that to basically a pair of commitment heights. That's actually overkill. You can detect it. Same with anchors. When you, if you actually see an on-chain transaction, you can detect at that point whether you were speaking anchors or not. So, it's actually not too hard to flip it on for stuff like that. So yeah, I might go back around and see if we get that ‘cause then, we could just cleanly upgrade the whole network. Of course,  then we want to upgrade them to taproot and then we've got a whole another — that's an actual on-chain transaction. But it would be nice because it is the only way you can really ever get rid of that code without selling a brand to close all channels if you do some kind of decent upgrade. If people have got really old channels, it just feels nasty to ask them to close them. Those things are like rare sats.

Speaker 0: Hear, hear. That makes sense. Cool. Anything else from anyone? Alright. Just looking forward to getting out the blind paths forwarding support so we can move on to the other phases. That'd be cool. Just more broader utilization across the network as well. And we've been doing some thinking around sort of creating the paths in general, like how you do the invoice side, the pathfinding applications for the receiver, and stuff like that, so…

Speaker 1: Yeah, I have to revisit our code. It's really dumb at the moment. If you give multiple blinded paths, we pick the first one and use that. We should do something smarter and basically be able to MPP across multiple or all the stuff eventually.

Speaker 0: Cool, okay. If that's it, then see everybody on chat and stuff.

Speaker 1: Yep. Cool.

Speaker 0: Alright. Thanks everybody. Please post it in my notes. 

Speaker 4: Cheers.


