---
title: Lightning Specification Meeting - Agenda 1114
transcript_by: Gurwinder Sahota via TBTBTC v1.0.0
tags: ['lightning']
date: 2023-09-25
---

Agenda: <https://github.com/lightning/bolts/issues/1114>

Speaker 0: So, [redacted] pointed out that we did not do this, and we have to do this. I've been working on the code so that you have to push their commitment transaction. Now, there are several problems with this. One is that in many states, there are two possible commitment transactions they could have. In theory, you know what they are. In practice, it turned out to be a bit of a nightmare to unwind the state. So, I actually just ended up just saving the commitment transactions as we sign off on them, and then you just keep the last two. Of course, with splicing, you can have multiple in flight making it even more fun. But potentially, you could be in two states if they haven't revoked the previous. So, there's a pile of fun to be had dealing with that. Even once you've done that, you've got the problem that you can only tell about your mempool; you can't affect other people's mempool. So really, this is screaming for package relay or…

Speaker 1: Honestly, just sign everything you can and then just send it straight to the miners and then.

Speaker 2: You shouldn't ever need to do this if you assume package relay. And even if you don't assume package relay, you still don't need to do this because you're not going to get into the mempool anyway, if the thing doesn't have a high fee.

Speaker 0: No, so their commitment transactions are in the mempool, and they're not interested in pushing it. You need it. So you need to push on their anchor, right? That's why they're two.

Speaker 2: You can replace — oh, yeah. I mean, again, you need package relay.

Speaker 0: Yeah. So without package relay, you should at least — which we didn't do — we pushed our own anchor, which is our commitment transaction. We put a commitment transaction. It's not going in. Let's spend the anchor and push; and child pays for parent it. But what we didn't do is the case, of course, where the reason we can't even get in our mempool because their commitment transactions are in the mempool and we need to push their one. And because we don't look in the mempool, it's a little bit fun. No, it's not a PR that's discussed now. It was a bug in core lightning — well, a hole in core lightning — that we did not cover. So, I've gone through it. Having the fun of implementing that.

Speaker 2: Half the time your commitment transaction doesn't make it into the mempool just because it doesn't have enough fee anyway.

Speaker 0: Well, there's that too, right?

Speaker 2: Yeah. You need package relay. There's just no game around it. Until then everything's fucked. Why are you trying fix all of it?

Speaker 1: Yeah, this? Yeah, we're pampering over a little bit. Well, I mean, statistically, there's a decent chance that it's their commitment transaction in the mempool, not yours. But yeah, it still isn't solved in general.

Speaker 2: I had some channel I couldn't close this weekend that was anchored, but maybe a week or two ago that had zero — or just didn't have enough fee — two or three separate bytes or something. No, maybe I had five because it eventually confirmed after the fee rate limits came down. But in the meantime, LDK kept trying to bump the fee and kept trying to bump the fee and kept trying to bump the fee. Had I not caught it, it would have spent a lot of money on fees.

Speaker 0: Yeah, we fortunately do have a limit that we will not spend more than we could ever get. Basically, some of the HTLCs are timed out and certain things we go: We're gonna push that. But yeah, it'd still be a lot of stats you throw.

Speaker 2: Yeah, we talked about that. I wasn't a huge fan of using that limit. I mean, that is the only limit because indeed you can still blow a lot of money.

Speaker 0: Yeah, absolutely. We had a fun one a while ago where we would, if we were offline and came back, which is not unusual, and so we force close the channel, we would then freak out and go, wow, it's been like, you know, 30 blocks, nothing's happening. And we would just ramp up the fee, or fee bump. Ridiculously. So yeah, because we had originally no limit on the theory that we could be in a bidding war. And we should spend all the sats. Yeah. Yeah. Oh, man. So it turns out building on Bitcoin is hard.

Speaker 2: Yeah, we need package relay. That's all our problems. So we're done. Not all.

Speaker 0: Not all our problems.

Speaker 2: A large number of them.

Speaker 0: Yeah, a decent number just vanish. This, I think, was my original justification for not doing this thing where you spend their anchor, but meanwhile — I'll put it in a big banner saying: Package relay, package relay, package relay. So I know where to delete.

Speaker 3: And it's not for this. You might have two very convenient transactions, and you might have one version in your mempool and the other version in the rest in fragmented mempools.

Speaker 0: Yeah, exactly. It's not enough. You know, you could pay for it with onion messages where you send me an onion message, and I will broadcast that transaction for you, which is not probably not the worst idea anyway. But, at some point, you're building…

Speaker 3: Package relay.

Speaker 0: Should we start working our way through? 11.08, modern feature bit assignment. So, this is basically a practice that we came up with for splicing that we thought was, generally, probably a good recommendation. That while features are in flux, you just add 100 to the feature bit and use that as a stand in. If nothing changes with the final implementation, it's easy for you to have an implementation that accepts both, but it avoids the problem that you change the spec and then you end up with these broken, older nodes out there, and confusion, and bad things. So it seems pretty well acked. The only question: [redacted] asked whether we should also do this for TLVs. Maybe. I think it's almost a step too far. I mean, how much code do you really wanna change?

Speaker 4: Yeah, my knee-jerk reaction is probably not.

Speaker 0: Yeah, I mean, you might choose that for some particular thing, but in general…

Speaker 2: I mean, the same considerations apply.

Speaker 0: They kind of do, except that at this point, if you really want to, you can do the: Oh, you're using the old feature bit. We will interpret it this way. It is a bit messier.

Speaker 2: You could, but in a lot of cases, we just deal with the message. If the TLV is set, we don't bother looking at the feature bit because why would we look at the feature bit?

Speaker 0: That's right.

Speaker 2: And so, you kind of do have the same issue there.

Speaker 0: Yeah, for us in our code base, it'd be a lot messier to do the TLV versions than the feature bit. The feature bits is really easy for us. I mean, the theory is that by the time you get to deploying it, you're kind of close to what it'll finally look like, you'd hope. So, I'm not as convinced.

Speaker 2: We could also just suggest if you need to change the feature be changed to feature, the TLV type, you change the TLV type, and then we've quote unquote wasted a TLV type in a message. But we just recycle it eventually, because hopefully, it won't turn into experimental garbage forever.

Speaker 4: I mean, TLV types are also message specific. So, we can shred through those pretty aggressively.

Speaker 0: That's true. But I think everyone's happy with it, at least, as it stands. So, should we merge? Cool. Looks like everyone's acked it, so I'm going to hit the merge button. Okay, 1109, another clarification. So, we use these terms. We didn't define them. We talked about features being offered and features being negotiated. But the only subtlety is that if you said it was compulsory, then you can basically assume that it's negotiated because it's up to the other peer to hang up if they did not understand it — i.e., you're allowed to just avoid it. Just set it to compulsory and just forget it and never check it. But I guess that's the only subtlety in that. But yeah, we use these terms in the spec. We just never actually said what offered means and what negotiated means, even though I think they're pretty clear. But, [redacted] again had a comment.

Speaker 4: Just the less brain cells we have to use to infer what the term means, the better, I think.

Speaker 0: That's what I figured. So, [redacted] made a comment. I'm not sure I understand it. Okay. I think I'm going to have to go around on this again because I do not understand [redacted]’s comment. So, it used to be that LND would check that the peer accepted the feature bit, but that's not in the spec. You're supposed to check what they offer you, and they're supposed to hang up if you offer them something they can't accept. Now, for most features currently, it's symmetrical anyway, so it doesn't matter. But in theory, I can offer you a feature that you don't offer me, and that's okay. So, you're supposed to basically just hang up on the other one. Particular things, like for pure backups for example, there's separate bits. There's one bit to say: Hey, I want you to back me up. There's another bit that says: I offer backup services. And they're not necessarily symmetric. You can say: You must back me up, but I don't have to offer that bit, for example. So the spec is written. I mean, you're allowed to hang up on anyone for any reason. But the spec is written as in you read their feature bits. You look through if there are any unknown ones that you don't like, you hang up. But yeah, so I will push that back.

Speaker 4: [redacted], is there a convention then about — is it always a service that you're offering that a feature bit is? Or is it a request for you to offer when you take your own feature bit?

Speaker 0: That's a very good question. It's a little bit meta. Generally, feature bits at the moment are the symmetrical requirement for us to both offer some feature, but they're not technically. Ah, see that's the difference between offer and supports. Supports is not actionable. Offers is like you set the bet. That's very clear. Supports is a much more vague statement about: Do you support something? Do you understand it? Offers is very clear. Offers is you set it in the bit. Whether you support it or not, it feels more meta to me. That's why I like the word offer. Offer means you set it in the bit, and set it in the init message, or in some contexts in the node announcement. Whereas supports is, I mean, you can support something that you do not offer for example, right? That's very different.

Speaker 4: Yeah, offering implies support, but not the other way around.

Speaker 0: Yeah, that's right. I mean, we can support a feature that we don't offer to anyone else. But if they offer it, we will handle it, perhaps. So, okay. Max HTLC value in flight, 1113. I have not looked at this, so I'm glancing at it now.

Speaker 4: It's just a wording clarification on the semantics of max HTLC value in flight. I just was kind of digging through the spec for some implementation reasons and found that it wasn't quite specific about whether or not it was the sum total of both sides of the channel or like both halves of the the HTLC buckets or if it was just one, and so I just try to clarify it.

Speaker 0: I don't think you can restrict the total. I think you can only restrict what they send you.

Speaker 5: Yeah, it's one of those things that's sort of like asymmetric, where it's like I set a value and you set a value. The value that I set is restricting you and the other way around. Wait, let me check the text a little bit.

Speaker 0: Yeah, I think that's right. Because you can both offer at the same time, you could accidentally step over any limit that was supposed to do the combined thing. So, it is literally: Yeah, you tell me: Don't send me more than this.

Speaker 5: Yeah, okay. I guess, do you think the critical change here is on the bottom, [redacted]? Like the sum total versus total value?

Speaker 4: This doesn't actually change the semantics as [redacted] noted. It was just a point of confusion as I was reading the spec, and I tried to reword it in a way that was like less — if I had encountered the wording that I put down, I would have not had confusion. Maybe people disagree with me, maybe they agree. I tried to get…

Speaker 2: I think the point is the first topic doesn't say anything about offered. It just says total exposure to HTLCs.

Speaker 0: Yeah, which is true. It does allow you to limit your exposure, but it isn't sufficient to limit your exposure. Right?, it's assuming that you also limit your own amount you sent. But how many more words do we want to add to point that out? Yeah. Cool. I mean, that really, for me, goes under the spelling rule. So, we can just kind of ack it.

Speaker 5: Yeah, it does have — [redacted] and [redacted] did the thumbs up on it.

Speaker 0: Yep. Okay. I'm going to say yes and apply.

Speaker 5: Cool.

Speaker 0: Cool. Okay. Harmonize. CLTV Expiry. Where did we get with that? What was the magic number today?

Speaker 3: 2016.

Speaker 5: Yeah, I think before it said 3000 or something like that, and then we said that we all did 2016. It looks to be in line with that now.

Speaker 0: Cool.

Speaker 5: Yeah, looks good to me.

Speaker 0: Yeah. I'm not sure. Yeah, we argued over the deserves own section or whether you should just literally put 2016 in that point.

Speaker 3: Yeah. I know it's cleaner. It's simpler to have a one-line change, but add on the other end, to clear up from something, you can reuse it.

Speaker 0: Yeah, I know. It's kind of bulky for — I know it's annoying to take everything and reduce it down to a one line change. But the problem is the indirection, you're reading the spec and then you're like: Oh, this max value; where's this max value? You look over there and you go: Oh, you mean 2016. Okay, that would have been good to know. I's a lot of words to say. It's not defined by default. It says defined by default. No, no, it's not defined by default. It's defined as, right? It's like literally there's no default. This is the value.

Speaker 3: Okay, fine, alright. I can change it.

Speaker 0: You can't change it. It was literally 2016. I mean, you could give it a name. You could say like max CLTV brackets 2016. Right, so you can point at it. But yeah, just tell us 2016 and we'll all do it. But I mean, we'll all do nothing because I think…

Speaker 5: It also looks like it just tries to modify the expiry too soon portion as well, which doesn't look correct to me at the glance. Before it was like, it's too close, but now you're trying to factor max HTLC into it being too close. I'm looking at line 123 in the diff on the left-hand side.

Speaker 0: Is it supposed to be the next bit, where it talks about being too far in the future?

Speaker 5: I think that would not be a thing in terms of moving. I think we should be modifying the line below.

Speaker 3: I think [redacted] is correct. I mean, It should be the next one.

Speaker 5: Yeah, just bump it down one. OK, cool. I got onto that just so you have a place over there.

Speaker 4: Yeah, I think we all just sort of pick something for that one too. I don't know what ours is off head. Maybe it's 20 blocks something. I don't remember exactly. In terms of when we reject for being too close. So, that's another round.

Speaker 3: Well, I will modify this proposal. At least, on the right.

Speaker 0: Okay, cool. But I think that was good. Okay. 1096. So, there's just been some light progress on this. This is the simplified close. [redacted] had a whole heap of feedback showing that I can't type or spell. There was one fix, where the case where I don't give you your signature because yours would be dust. But [redacted] said he is trying to implement that now. So I'm gonna let him do that and give us feedback and tell us which bits broke. I tried to really spell it out. Like do this. Do this in this case. Which in some ways makes it less clear to think about, but much easier to implement because it's really broken down to this multiple cases.

Speaker 5: Gotcha. Yeah, this is still on my list to start to work through an implementation on. We're almost done with our current LND.17 release, and I can have some more bandwidth to take a look at this more deeply.

Speaker 0: Yeah. Hopefully, we'll get some motion on that. I mean, I don't feel hugely wedded to this. I kind of made it up as we go. So, if it turns out to be impossible to implement, then we'll fix it. Yeah, I mean it enshrines the dust rule, which was mentioned previously, and basically adds OP_RETURN. Cool. Spec cleanup, 1092. Now, we've decided to kind of shelve this for the moment. Basically, make them compulsory and then later on, see if we can start ignoring them. We have in our next release in November, we will be making all these features compulsory. So, that'll be a nice test balloon. Some of them already are — of our onions — already compulsory for us anyway. And we will be weaning off the old anchors. We no longer offer it, but if someone else offers it, we will still accept it and we still support channels that are that. We're going to do the beta upgrade thing, because you can only ever do that if you enable experimental features. And if you like experimental features, you'll love experimental upgrade. So our idea is that we would upgrade to zero fee anchors because that turns out to always be possible to upgrade. Because you're just basically reducing the fees you're paying. So, there's no state you can be in where you can't just upgrade from the old non-zero fee anchors to the zero fee. So, it's actually like the most trivial case. So, we will be implementing that, and then we can rip out support for non-zero-fee anchors. Then, we can change the spec just to call those anchors and pretend the other ones don't exist.

Speaker 5: Don't you need some additional synchronization there? Because like the SIG hash flags are different now, right? And so now, you need to be able to verify.

Speaker 0:  Yeah.

Speaker 4: Or no, I guess we're the same and we just move the fees to zero. Just thinking about edge case, like retransmission or something like that.

Speaker 0: Yeah, so we still need to use the STFU, kind of the quiescence thing, where what happens — for the upgrade proposal thing, when you reconnect, you say: Hey, I want to be this state. And if you're actually got nothing in flight, the other side goes: Yes, now we're the state, and you're in the new channel type. We did it previously for static remote key. We could upgrade static remote key as an experimental thing, and that case, we kept in our database at what points we changed, which is actually kind of dumb. The only reason you care is if you ever see one on chain, you're like: Oh wait, hold on; this is old style. But we didn't need to do that. You really don't need to do it for anchors. You look at what's the — ‘cause you grind the fee anyway. We just grind the fee. If you go: Oh, it's zero. Okay, I know what you're doing. This was a zero fee anchor. So, I don't even think we need to add anything to the database to remember when we changed. We can just change and our on-chain code should just be able to intuit it from what it sees. That's my theory.

Speaker 5: Yeah. Have you added anything to the STFU message? Or is it just sort of like you know to send that, and it just knows because the version it's on and things like that? Or are you threading through any additional CLTV context, or anything like that?

Speaker 0: Technically, STFU is optional. So, the way the protocol works is when you reconnect, you say: I want to upgrade the channel. And if there's no retransmissions, then the other side acks that, and you go: Yes, we're good. We've upgraded the channel.

Speaker 5: I just have one question: What message are you sending to say: I want to upgrade? Is that STFU or is that something else?

Speaker 0: No, that's in the re-establish. The TLV in the re-establish says: Hey, I want to be this kind of channel. And the other side goes: Cool, I'm happy with that.

Speaker 5: TLV reestablish. Alright. Gotcha.

Speaker 0: But it can only work if there's no retransmissions going on. If there are retransmissions going on, then the upgrade fails and you will reconnect at some point. You can use the STFU to force this case, but statistically, you're fine. Your chances that every time you reconnect — so imagine, perhaps for one or two versions, we'll support this case, where we still handle the old code and we'll do an upgrade opportunistically. And given that they had to be experimental in the first place and turn the shit on, I'm just going to go with they're not going to get unlucky and always have an HTLC in flight that they need to retransmit at the time they reconnect. And probably, we'll have closed. If they fall all the way through that version, then the next version will probably force close those channels or something, and no one will notice it. That's my theory.

Speaker 5: That makes sense. Actually, because [redacted] started to look more into the whole channel upgrade thing as well. So, I was wondering if there is a very simple case. I think you have a very simple case of there's just zero fees. So, there's no new pubkeys to exchange or anything like that. So interesting. I was trying to look at this holistically.

Speaker 0: Yeah, cause we did it for static remote key and that was similar that you can just pretty much upgrade. So, anything where you don't have to — yeah, the no param upgrades are the easy case. We accidentally made another one.

Speaker 5: Cool.

Speaker 0: Offers. I don't have any progress. On my to-do list is to upgrade to the latest spec. The addition is that you can now have an introduction point to the blinded path that is a short channel ID and a direction bit. Using the pubkey hack, where 01, 00, and 01 become a magic direction value. It's spec'd. It's in the spec, but we haven't actually implemented it, but we will. We'll implement it. We won't ever create such a thing, except in dev mode, but we will accept them so that if others do. Cool. Ah, there. We're in the quiescence protocol. This is the STFU thing. I don't think there's anything. I don’t think there is anything.

Speaker 5: I don't think there's anything. I think he was just looking at it to better understand the uses and when you officially want to start to enforce it. I know it has some splicing overlap as well, but I don't think it's used there, but something that, I think, the final version would incorporate some.

Speaker 0: Yeah, so splicing does use STFU, and there's a comment here saying — I think it leads into what you were gonna say.

Speaker 4: Yeah, I would love to be able to use this as part of the dynamic commitments work. Just to simplify the number of different — like you said, in the rationale for having this at all, it can be nice to have just a primitive in the protocol to get everything to stop so that we can do whatever else we wanna do. The only thing that I saw in this that I was scratching my head about a little bit was that because the requirements for this double synchronization of commitment transactions. I think it is possible, but probably statistically unlikely that you can get into a flow of messages and heavy channel traffic, where you can't actually get the channel to STFU. I'm not 100% sure because I'm still kind of getting up to speed on how pending updates apply, but I've listed out a sequence of things that if you loop through them, that it would just never allow the thing to STFU. And maybe that's okay. But it could be beneficial to have a two-phase sort of thing where it's like: Okay, block the adding of updates and then actually commit to the STFU.

Speaker 0: Yeah, because the requirement is that you don't send it if there's anything pending for either peer, which means, I think, if you've got a flood of traffic, you will never — I mean, I think you should…

Speaker 5: Wouldn’t it have shut down semantics, where after you send it, you're supposed to stop sending stuff?

Speaker 0: That's the thing, but there's also a gate on sending it in the first place, which may be overzealous.

Speaker 4: Yeah, that’s what I was pointing out. You could do a two phase version of this where it's like: Yes, there are pending updates, but like stop. And then there's the one that's like: Okay, there are no more pending updates. Now we're like really stopped.

Speaker 5: So, like double active kind of, yeah.

Speaker 1: Yeah, so like shutdown, where you only reply when it is all clear.

Speaker 5: Yeah, closing sign implies that.

Speaker 1: Yeah, I think that would work. Yes, the receiver is not supposed to send any more updates, but the sender is restricted on when they can send it and that's the issue. It's been a long time since I've looked at this. I think there's probably a reason why it works this way. I will put that on my to-do list today to figure out if it's simple or major to fix it up. You're right. I think statistically it works, but we should make it more robust. Cool. Is there anything new on splicing dynamic commitments: upgrade and reestablish? Otherwise, we go to Taproot because I'm sure there's exciting stuff there.

Speaker 5: I think for splicing, I saw [redacted] commented some laundry list. I think there was some minor chatter on IRC, but I think people just know like the final things to start to fill in, so I got that.

Speaker 0: I noticed that the spec is mainly lies. What they implemented is not. Like, I basically went to re-import. I went: Oh, let's re-import the CSVs from the spec. And I went: Hold on, these don't match what you've actually got here, [redacted].

Speaker 6: Yeah, some things changed, and they didn't get written down. So, they're on the list now. Hopefully, everything is in that list that I made. If there isn't, please tell me to add it.
Speaker 5: Cool.

Speaker 0: That's cool.

Speaker 1: On Taproot. LDK. We're prioritizing 1.17 before we merge Taproot stuff. So, nothing really exciting to report from our end.

Speaker 5: What's 1.17? Is that like a LDK PR number?

Speaker 1: Our next release.

Speaker 5: Oh, right. Next release. Gotcha. Oh, yeah. It's a high number, I guess. I was thinking a PR number.

Speaker 0: Oh, wow. Up in the hundreds.

Speaker 5: I see.  Okay, cool. Nothing too big changed. We've had some more testing and things like that. People were testing recovery, SEB, stuff like that. We found some small things with certain API calls not being fully updated on our side. I still haven't added the test vectors yet as well. It's still kind of in that state that I had it on prior and I think we have a better way.  We have another project to have the test vectors along with some unit tests to make it a little bit easier. But that's sort of where we are with that. I think probably the next week or so, we can start to pick up the gossip changes more now. But now that I will be shipped over to other stuff, I think we'll have to start to look at that and work through some of the feedback in the PR, and then just see how things line up on the code side of stuff.

Speaker 0: Cool. Yeah, I noticed on the gossip PR, there's like a: I'm gonna get to this real soon marker, which I'm happy with because that means I don't have to do anything again.

Speaker 5: Yeah, he's working on some other stuff. Cool. Alright, So you're saying working on getting the next release out and then y’all back to pick up the patch and wrap, right?

Speaker 1: Yeah.

Speaker 5: Okay, cool.

Speaker 1: By the way, with regard to the Taproot gossip — I'm not sure, I don't think I'm seeing [redacted] here — but how final is the spec?

Speaker 5: So, we haven't started code at all. I think the spec represents a state after our conversations in New York around combining the messages, being able to advertise both, the whole handing out this MuSig2 thing and so forth. So, I wouldn't say it's super final by that regard, and there's no code at all committed to it. I think everyone needs to take another look at it after to make sure it matches what we thought we had in our minds leaving New York.

Speaker 1: Yeah, okay. Cool, thanks.

Speaker 5: Yeah, I mean, if you wanna dive in and leave a bunch of comments, no one's gonna get mad because they feel like it's almost done.

Speaker 9: Oh yeah. That's well — I have to dive into my code first. After interop I'll be happy to leave gossip comments.

Speaker 5: Cool. The main thing we're looking at is just the messages and just having that line up with expectations and requirements and stuff like that. That's sort of working right now, to my recollection.

Speaker 0: Yeah, the gossip stuff for us is critical because that's the first thing we're going to implement. So, we make sure that we can see other people's taproot channels, which is like a minimum viable, right? So as people start publishing them, at least we can use them.

Speaker 5: Yeah, and I think the other thing about that is trying to always — we're supporting advertising the old with the new formats. That also helps bridge the network sooner versus like a hard switch over and there's no one, or don't we talk to, whatever — so that's good.

Speaker 1: I don't want to couch our horn too much, but one funny side effect of RGS is that with all of the data that was being stripped out and principally could advertise taproot channels or include taproot channels, and then put it snapshots there without nodes being any the wiser that those are taproot channels. Because they don't need to know. They're just routing through them.

Speaker 5: Yeah, Good point. I guess it depends on how much validation you do. Without it, if you have validated knowledge, just insert. Sure. Because otherwise, maybe they don't know how to parse, or pay the taproot, or something like that. But I mean, you're totally right. If you have some side server gossip thing, you can do whatever. Assuming the client is okay with that.

Speaker 1: I'm nodding.

Speaker 5: Cool, cool.

Speaker 0: Attributable errors. Has anything happened?

Speaker 5: Not much. I think we're starting to take another look at the PRs, now that we're down to level 17 — our upcoming major release. Last I remember, [redacted] or [redacted] was looking at it, and there was something around reducing the size of the HMAC, something-something. But I think now it'll be picked back up as far as review and stuff. But I don't think anything super actionable yet.

Speaker 0: Cool. Channel reestablish requirements. There are two of these PRs.

Speaker 5: Yes, this is something very old in my to-do. I think we realized that this part of the — I can't remember why there's two of them. I think one of them, 1051, I think is a bigger overhaul to some of the wording.

Speaker 0: Yeah.

Speaker 5: And I think the other one was meant to just be like clarification around failing the channel versus sending the error first. That whole thing.

Speaker 0: Yeah, okay.

Speaker 5: For now, it's the user review.

Speaker 0: Yeah, homework everyone should check out these, including me. There's a big banner at the top that says, [redacted] has requested your review, so I'm guessing that I should review it. Cool.

Speaker 5: Yeah, I'd check that too.

Speaker 1: Right. I think that marks everything that we had in seeking review.

Speaker 5: Yeah, there's one thing that I mentioned on chat. Remember a while back, we had these like gossip extensions. I think Eclair wanted the timestamp one and the checksum one. I thought it wasn't super necessary basically, so we never implemented it. But now I realized that we have an issue where if a node is either off for a long period of time, or has poor connectivity, they'll never sort of resurrect zombie channels, right? So, what's it like — certain LND nodes are missing portions of the graph, either because the new update won't propagate to them or other unknown reasons, right? And the reason why that matters is, for example, if we mark something as a zombie, we wait until we see a fresh update to actually resurrect it basically. If that never comes, or due to the ordering, if we're down for a while, we've proven before other stuff, then we have these gaps. So, I think we're looking into implementing the timestamp extension basically for the gossip queries, so that we can basically see: Oh, there's a newer timestamp than what we have right now. Maybe this thing actually isn't a zombie. And maybe there's a few thousand channels that are in this state. We tested as far as wiping this, sort of like zombie cats that we have and we're seeking and things like that. So that's one thing we're looking into because it can affect pathfinding. Obviously, you don't have portions of the graph. There can never be a path sometimes, but I was wondering if people implemented that, The timestamp thing already, in terms of like us finding peers and stuff.

Speaker 0: We have.

Speaker 2: Yeah. Basically because of this issue, we never bothered to implement, or we implemented gossip queries and then we immediately ripped it out and never actually used it because of this issue. We just always download the full graph every time we start up because LND didn't implement the timestamp thing.

Speaker 5: Gotcha. Okay. That's good to know.

Speaker 0: I'm looking forward to Gossip v 1.5 for this. Taproot Gossip makes it easier for us to sync stuff, but yeah.

Speaker 2: Yeah, I think we'll probably just won't bother. We'll just go straight to minisketch, and we'll just keep downloading the full graph on startup. It doesn't take very long. It doesn't cost anything really.

Speaker 5: Gotcha. Yeah, because I remember the thing and the reason why we added this. Initially, there was, a while back, where testnet had this thing where it would just churn zombies over and over again, and testnet was boring other than this. That's why we started to add some of these protections there. But you're right. It's not super large, particularly if you're already using the RGS thing, then you get a pretty streamlined dump of it. But there's something that we realized that can affect particular mobile phones, because no neutrino nodes don't always download all the blocks, things like that. They also may not always see channel closes the way like a full node will as well. So, we had some stuff to work around there. But okay, cool. So at least we can get it from clear nodes and then to lighting nodes, and then we'll start to serve that data as well. That's a second background thing that I realized. People were just complaining: Why do I have 20K channels less? I was like: Oh, they're not really needed. But those are actually the free channels.

Speaker 0: Yeah, I'd be tempted to put a heuristic in to go: We expect this many channels, and if we were way short of that, we should start just scraping stuff. We try to do stuff where if we see an update for a channel we don't know about, we start to get suspicious and we do probes and stuff, but we don't have an absolute threshold. Other than for a fresh node, we have nothing in gossip, then we will reach out and grab stuff. It's all heuristics and bullshit. It really is not pretty.

Speaker 2: Just sync the full graph on startup when you make your first three peers you connect to. Sync the full graph. It works great. Don't have to think about it.

Speaker 5: Well, I think it's like — so we actually do sync the full graph. So what we do is, every 20 minutes or so, we'll basically do a diff on our channel IDs and y'all's channel IDs. The issue is that we see channel ID 5, and we're like: That's a zombie. We're not going to fetch that thing. To avoid downloading it and then pruning it right after. So that's why we don't always just get everything. We treat the zombie edges slightly differently, but now the gap in our logic was: Well, you may already have the edge and it may be a zombie, but there could be a newer update. That's where we're trying to be able to fill the gap on there.

Speaker 2: Right, because yeah, you have to actually have the timestamp to know. But you might as well just download it. It's not very much data.

Speaker 0: Yeah, but you end up churning zombies. We had zombie protection code that we ripped out because it wasn't working correctly, and we never put it back. So, we still have the issue that we will un-zombie things as updates come in from one side. So I'm looking at reworking that for this release.

Speaker 2: Yeah, I think we will un-zombie it, but we won't actually use it when routing, so it doesn't really matter. Delete it again later.

Speaker 0: They tend not to be critical stuff. But if your node's been down for a long time, then that may mess with things as well.

Speaker 5: Yeah, and usually it's like: Oh, my node was down for a week, and I didn't notice, and I came back up and then I have 10k less channels, or something like that.

Speaker 0: Yeah, we run a prune timer that runs every day. So you come up; you've got like a day to sync. We won't prune immediately, at least. So, you got some window, but this could still get messy.

Speaker 5: Yeah, we should. Because I think part of the issue is recruiting is the first thing we do, but we should, like you're saying, have some time or to give them time to propagate and shit.

Speaker 0: Yeah, because we found that we were throwing away all our gossip the first time we came back.

Speaker 5: It's like: Oh, you've been down for a month? Everything's a zombie.

Speaker 0: That's right. Yeah, it's all gone. Why can't I pay anything? Oh, yeah. Cool. Right. Is there anything else that we should talk about? There were some weird people who were complaining about force closes on mainnet, bolts in particular. I don't know about others.

Speaker 2: Yeah, I had an issue…

Speaker 5: We fixed an issue of this on-chain thing. So it was a case where if we were using a hodl invoice — which I'm pretty sure there were — and hand wave concurrency nasty stuff, it could deadlock. But we fixed that one in particular. There was this other like peer-based one, basically, another kind of an academic thing. One thing I'm realizing as well is that — for example, we had some random ones for our nodes as well. We realized many times, it was just due to the worst case of a cascading force close, where no one could actually get into the chain. It's a combination of no anchors, or even if you have anchors, not bumping aggressively enough, or not being aware of the deadlines coming up. So it's one of those things, where because the mempool was flooded with people doing this dollar auction type stuff basically, people just couldn't get in time. So we're looking at reprioritizing because we'll, at least, target a deadline, but we won't do the bump on a curve type of a thing. The other thing that relates to that is the things that we talked about around dust HTLCs, where right now, we'll unfortunately go to chain for a dust HTLC, and we won't cancel back until the outgoing is fully resolved. But if it's a dust, you can maybe just not go to chain at all, but then also cancel back a lot earlier, right?. So things around dust HTLCs leading to timeouts, leading to congestion, leading to that whole spiral is what I think is going to happen. At least, for the cascade. It would pass a few weeks.

Speaker 0: Yeah, we put some logic. So I know Eclair has logic, where it basically will immediately close as soon as it goes to chain. They take the chance. We give it more, and we kind of go: Hold on. We're in danger of our peer force closing on us. Huh, the outgoing one is on chain. Hasn't been resolved yet. Fuck it; we're just gonna take the chance that is not now gonna be resolved rather than lose the channel behind us. So, we try to cut through the cascade if that happens for any reason — it could be because it's a dust HTLC; it could be because of congestion; it could be because of bugs; whatever it is. We now try to break that. Because it's weird because it's the only case where you care about your peers' timeout. Normally that's their responsibility. Like, if they have a HTLC that's gonna timeout, that's on them. But this is the one case where you go: Huh. Well, hold on. I suspect they're going to hang up on me soon, so I'm gonna have to close it. So we've taken that chance because I think people would prefer that to a force close.

Speaker 5: Yeah. Anything but force close.

Speaker 2: Yeah, we will probably do it, but we have not yet done it.

Speaker 0: The other thing is the tolerance thing…

Speaker 5: Is that if you have a whole thing early or not going on chain back?

Speaker 2: Both. You go on chain and then you fail back early.

Speaker 5: Gotcha.

Speaker 0: Yeah. The question of tolerance, right? Is there some level of HTLC, which you know — obviously, if it's a dust HTLC going on chain, doesn't win you much, except for vengeance, or kind of getting upset with channels that are not working well. But the idea of having some statistical tolerance is something I've kind of toyed with. I mean, rather than have some absolute cutoff, have some kind of statistical thing where you go: Let's flip a coin or do a curve and go, No, I'm not going to close the channel just for this one. Particularly when you combine it with the cascading logic, where you close out the HTLC even though the upstream's still stuck. Maybe somewhere we have to go eventually because people really hate forced closes. Maybe they'll hate losing money more. I don't know.

Speaker 5: Yeah. I mean, I think that's the interesting thing about choosing to not go on chain is that best case, something happens, it gets canceled back. Worst case, you're just eating this thing basically, and you need to keep track of your debt to pay it down because it starts to choke into your channel capacity. But I think the one related thing I think we talked about in the past that could help with that — I think something [redacted] started a while back — is having a different dust limit. So, there's a different limit for max dust HTLC that doesn't necessarily hamper your throughput, right? So you can keep that on. It's basically two different buckets, and they're very different classes.

Speaker 0: Yeah. Someone should spec that because it'd be interesting to see what it looks like.

Speaker 5: I think there's a PR from the initial death saga we went through. It's just kind of sitting there perhaps. Or we talked about making it. But yeah, those are the two different causes of buckets.

Speaker 2: I have been seeing some evidence of peers just losing HTLC.  I had an LND peer force closed a little bit ago. Sadly, he lost his logs. But I did note that none of his — the HTLC was routed through his node, and none of his other channels. He had a number of other channels force closed, I think due to the same issue, but none of them had the HTLC that was forwarded through his node.

Speaker 5: And it wasn't dust?

Speaker 2: And it was not dust. It wasn't close to it. It was like a hundred case sats or something. It could have been dust on one of his other channels, but I think that's unlikely.

Speaker 5: Yeah, it seems unlikely.

Speaker 2: I, sadly, don't have logs, so I'm not gonna open an issue, but I've seen some weak ads.

Speaker 5: Yeah, because one thing…

Speaker 2: There may still be an HTLC hang somewhere.

Speaker 4: Yeah. One thing we did fix in 17 was the old thing, where if you sent a channel update super quickly after the reestablish, we would guarantee to not really handle that, but now that's handled as far as synchronization there. I think that's also fixed some other channel update things. At least, that's one thing that we know is an issue. But right now, the main thing that we know is an issue is this dust stuff. The thing we're looking to have some interim thing. Probably just do the cancel back early, and then examine the not going to chain with some of the other implications that that adds.

Speaker 0: Speaking of channel updates, so what do people do with channel updates that receive an error message? We put it in our gossip store, but that's potentially an information leak. So we'll start broadcasting out to everyone else, which is always a bit meh.

Speaker 5:  think yeah, so we take it; verify it; apply it. But I'm not sure we broadcast it to others.

Speaker 2: We don't broadcast it, but if somebody else does a full fetch from us, then it would be included in that.

Speaker 5: But you’re saying information leak — the rest of you are watching to see if you got my update kind of thing?

Speaker 0: Yeah.

Speaker 2: They're watching.

Speaker 5: Ah. Yeah.

Speaker 0: I mean, we could do some kind of dandelion thing. I mean, you can apply it locally just for this payment and then forget it. Which would work, right? So, you don't call even Carly and cross other payments. We can do some kind of dandelion thing, where you spread it to a peer and then eventually, it explodes and something like that. Although if you only got one peer, it's pretty obvious at that point. Maybe you don't do it in that case. I just wondered what others did ‘cause we will put it in our Gossip store, which will validate everything else. If all comes good, we basically just do it. Go back and start again and do a path find now that it's in there. But that's a little bit too social. We also have potentially a problem with Gossip v 1.5 that [redacted] pointed out where, because you use block heights and you can't have two updates with the same block height. If you go take the first one, it's easy to segment the network and do a similar kind of thing where you basically pollute the network with injecting gossip, and then you can tell by when someone makes a payment, which update they had for your channel. You must be in this region of the graph because I pushed that into there. So, the rules around how you overlap gossip if you get two gossip at the same timestamp are tricky. In particular, everyone goes minisketch and everything else, you may never see both of them because you may think that they're the same thing. So,there's actually an open issue…

Speaker 5: Yeah, I think for the height thing, there definitely needs to be some burst tolerance. Whatever that is. If that needs to be global or synchronized, I'm not sure, but yeah, you definitely need some burst tolerance to number and handle those retries, and then also the propagate stuff.

Speaker 2: It seems like we really kind of have to either ignore it completely, do a pathfinding that just avoids that channel, which sucks, or do a dandelion thing. Or you fetch a new route using that information, but you don't use it for future payments. You just use it for this payment. You don't edit the gossip store. You just wait. Then, all future payments will also fail or you have to segment it completely. I don't think anything that works at the peer to peer level is going to work short of like a dandelion thing.

Speaker 0: Yeah. No. I'm tempted to say you should just apply it locally for this payment, and then hope that it propagates in a genuine way. If they're working properly, it'll propagate in a genuine way, and you're just a bit behind. That's fine. If they're trying to do weird shit, where they advertise one thing, and then when everyone asks, they send something else. You're gonna get bouncing off them and that's their problem really. You're gonna read. You're gonna hit them every time if there's a little best route and maybe you bias against them at that point. I don't know. But I just feel our implementation is probably wrong and leaking information.

Speaker 5: Yeah, that's a really good point. I'll check what we do. I feel like maybe we queue it to get sent out eventually, but on a delayed basis. But this is a good point. I like some analogies of transaction broadcasting stuff like that.

Speaker 0: I don’t think it's the biggest information leak we have in the network, but I thought I'd ask.

Speaker 2: It sounds pretty nasty. I disagree with that, actually. It's one of the worst ones.

Speaker 5: I mean, it sounds very inadvertent.

Speaker 5: Okay. Alright. I'll check what we do and maybe modify it. Maybe don't. Maybe we do the right thing. Maybe there's nothing to check.

Speaker 2: Cool.

Speaker 0: Okay, I'll put it on my to-do as well. Cool, okay. Is there anything else we should — is burning on fire on the network?

Speaker 5: No, that's about it.

Speaker 0: Cool.
