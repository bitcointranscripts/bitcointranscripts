---
title: Lightning Specification Meeting - Agenda 1094
transcript_by: Gurwinder Sahota via TBTBTC v1.0.0
tags: ['lightning']
date: 2023-07-17
---

Agenda: <https://github.com/lightning/bolts/issues/1094>

Speaker 0: Alright. Does anyone want to volunteer to take us through the list? Nope? Okay. I will read the issue that [Redacted] very kindly left for us then. The first item on the list is Bolt 8’s chaining keys clarification. Is there anything we need to talk about here?

Speaker 1: Yeah. Yes, it's almost under the spelling rule, but I think it's been ACKed by everyone. So, unless people have objections to the specific wording. To be clear, it's not a change. It's just a clarification based on LN Socket's misimplementation of rotation.

Speaker 0: Cool. Well, I guess someone can hit merge. It's got enough ACKs.

Speaker 1: I'll do that.

Speaker 0: Sweet. Hit the button. Spec cleanup. I took a first look at this today, and [Redacted] had a look, but I guess it'll need a few more people to volunteer to take a look at the cleanup that we discussed in New York.

Speaker 1: Yep.

Speaker 0: There was some discussion on this about —  What was it? I think [Redacted] commented about this. Anyway, I think [Redacted] can comment on that next time. Anyone feel free to chime in at any point.

Speaker 1: No, I think I'm finally reading through the comments. Sorry. There's a question on…

Speaker 0: Here it is: Option static remote key being dependent on anchor outputs.

Speaker 1: Yeah. Or the other way around, anchor outputs dependent on options static remote key. So, [Redacted] doesn't want to assume it, but I think, I'm not quite sure why, but [Redacted] does comment that the whole section we should remove.

Speaker 2: [Redacted]'s saying they want to use it as a flag to say: I don't support non-anchor channels. Basically, if you unset that, it is an indication that you only support anchor channels — is what he's saying.

Speaker 1: Right. Okay, but you can set anchors to compulsory, I guess. Although then, you've got the problem that old clients can't connect to at all if they've got an existing channel with you.

Speaker 2: Well, then we have the issue too, where you can't do taproot because you require anchors, But I guess taproot also uses anchors. I don't know if there's some new anchor v2 something-something, then you couldn't set it to compulsory.

Speaker 1: That's true. I mean, if you put it in a neat message —  if someone has an existing channel, and you want to support that, but not support new opens — then, there's no great way of doing that other than rejecting the channel open, but they can't tell just by looking at you whether you are making things compulsory, because — yeah. So, we had this problem before. I'm not sure that static remote key is really the best way of doing it, but I think removing the explicit dependency is correct. So, I think I should remove that requirement, and also the whole initial sync section, and there's some typo fixes. This does seem like it needs a little bit more revision, but I think it's clear that people are broadly supportive. It's just a question of turning around a few times. I think basically you could ship this today. You could assume everything today, and no one will care. You won't get any bug reports because in practice, everyone says these bits, and I think that we have consensus on that. So that's good. Cool. Okay. I will commit to going around again, tweaking this a little bit, and having the debate with [Redacted].

Speaker 0: Cool. Sounds good. Next on the list, we've got the two blinded paths PRs. [Redacted]’s one — 1066 — and Redacted]l's one — 1069. At the summit, we said we'd update one of these to have the absolute block height, and then the other one, I don't know if we need any changes there. Are there updates here?

Speaker 2: No, there's no update. As soon as we get this next release out, and probably the one after that, then I'll have time to work on the spec.

Speaker 3: Yeah, I just need to clarify something-something about the delta calculation from the invoice expiry, but we'll get to that.

Speaker 2: If someone is annoyed, they can happily take over my PR. I know I've been holding that up for a while, and we'll do it eventually if no one does it. But if someone else does it in the next month, you will probably beat me to it, and you're welcome to take it over.

Speaker 0: Okay, I might grab this one from you because I'm busy working on this on LND, but don't hold me to that. Yeah, I guess these ones are just sitting and waiting. Next up is 1086, harmonized max CLTV expiry across implementations. Has anyone taken a look at this one? I haven't had a chance yet.

Speaker 1: No, I don't mind harmonizing. I don't think it's critical.

Speaker 2: Yeah, I'm not sure why. I think this basically came from a miscommunication. I was complaining about something else — about not knowing the maximum, I think, CLTV delta that nodes are willing to route through. Basically, how high can we set it before there's an issue and then, we won't go any higher? Then, we had a brief discussion about that in New York, and nothing really came of it. But then, [Redacted] ran ahead and also added this for the far away section, which is also related, but not super-related. But in general, it would be nice to have some of these be a little more — whether they're actually harmonized or, at least, just there's somewhere we can look that says the values everyone uses,  so that we can look that up and make decisions based on that would be very nice. ‘Cause right now it's kind of hard to make a decision for various parameter defaults because you don't know what other people will or will not accept.

Speaker 1: Yeah. I mean, my assumption always was that everyone's implementation and practice will be so far away that unless you're doing something really stupid, you're not gonna hit them. You shouldn't put it. I don't know. If you're playing on this edge, you're probably doing something wrong. If you try to create a four-way gate…

Speaker 2: Yeah, this one is much less than all of the other ones, mostly those that are default delta.

Speaker 1: I mean, I guess I always love it when somebody comes up with a number and everyone just uses it because it just saves the implementers the whole pile of mental churn trying to figure out what their magic number would be, particularly when there are considerations. So, I'm not even sure what it is that we use. I suspect we use two weeks TM. So four, why not? Sure, I guess more comments on the issue from people who know what their particular values are, and if people want to defend it, that's fine.

Speaker 0: Yeah, LND's 2016. So, also two weeks at the moment.

Speaker 1: Yeah, I think we're the same.

Speaker 0: I think Eclair used to be a thousand, and now they've bumped it, but I could be wrong there.

Speaker 4: Should we drop a comment in the issue to call for what those parameters are?

Speaker 1: Yep.

Speaker 4: Yeah, I'll do that right now.

Speaker 0: Cool. So, actions for this one: Drop in what you're currently using and when folks have time, give a PR a look. It hasn't got any reviews so far. Cool. [Redacted] pointed out that I missed 1093 on the list because reading is hard. So, allow empty onion hash for blinded errors. [Redacted] says it's implemented in LDK. Anything else that we need to discuss here?

Speaker 1: Yes, [Redacted] had the same comment, I think, that they wanted unset onion hash. We were talking about whether it should be a bogus — oh, yes, this is [Redacted]’s anyway. Cool. It's all zero. Sure. It turns out nobody uses this. So, the idea was that you put the hash of: Here's the thing I received that I'm complaining about in case there is some weird debate between: Did you send me crap or did I somehow corrupt it? But in practice, nobody ever used this field, as far as I can tell, even for debugging. So, setting it to zero doesn't break any existing implementation. Nobody does anything smart with this value, and zero is very clear. If someone's hand debugging, zero is very clear. I do not think this is the hash of the thing that I received. So, I think I can just ACK this. Done.

Speaker 0: Cool. 1044, attributable errors. Is [Redacted] here? Or does anyone have anything to add on this one?

Speaker 1: Yeah. So, attributable errors are now much more attractive than they were previously because they were really quite chunky before, and the question was: How big? But [Redacted] has a trick that we think is acceptable that is a little bit hinky, but does reduce the size down to 1300 odd bytes, which makes it fitted much, much more nicely. So, it's simply now a question of everyone actually getting around and implementing it because I believe this is another kind of network-wide upgrade thing, where the sooner we start, the better. It was marginal before and it's moved into my happy, good category now, so I like it. Does anyone have any actual plans to implement this?

Speaker 2: Maybe. I used to open the old version of it as a PR in LDK quite a while back, not an actual version, but a demo aware level code. So, I guess I owe him feedback on it now and we would like to do it too, but priority isn't all that stuff.

Speaker 1: Yeah. I think it's not literally on fire, but it's a nice-to-have.

Speaker 2: Yeah, it is nice to have. I think that it is pretty actively under review in LND last I checked and slated for a release sometime. So, it is happening.

Speaker 1: That'll give everyone else FOMO. So, that'll probably do it.

Speaker 0: Yeah, see that feature bit popping up, FOMO. Okay, next up: 759, Onion Messages. [Redacted], anything here?

Speaker 2: Can we merge those? What's it waiting on? Any final feedback or …?

Speaker 1: No, we have interop.

Speaker 1: We've got a whole pile of fixups on it. After an ACK…

Speaker 0: Oh, I remember what this was. It was waiting on just [Redacted] checking the test vectors in LDK, and I told [Redacted] I'd do that, and then I forgot about it. So, I'll chat to [Redacted] and maybe try and either manually or properly do the test vectors, and then we can merge. Or you can just go ahead because you have interop. I forgot about that completely.

Speaker 1: Cool. Well, I'd like the test vectors. It's always good to have test vectors checked. So, I'll write a comment saying we agreed to merge pending active test vectors. Just ping me when it's done, so I can hit the button, because I'd like to hit the button on this one. Actually, I really don't care.

Speaker 4: But I had a quick question on it, because I'm kind of new to this part of the spec. But I do remember a few years ago, people were concerned about DOS vectors. I just wanted to know if that resolution had been documented anywhere. I'm sure people have talked it to death at this point. So, I'm not trying to re-raise it as much as just understand where the state of that discussion is.

Speaker 1: Yeah. So, this is a good one. I mean, it's simple. It does suggest, I believe, that you should do some rate-limiting, but it sort of lays it at hand-wave as to what you're going to do. To be fair, there's a fix-me in our code, we do not do rate-limiting. But then, it's an experimental option. So, we're like: Get to keep both pieces. I mean, you can just do naive rate-limiting and just go: Well, if you have a channel with me, you can get ten messages a second, and if you don't, you can have two messages a second or something.

Speaker 4: Got it. So, at the spec level though, it's really just like: This is a problem, solve it somehow?

Speaker 1: Yeah. So, the idea of doing a more sophisticated one does require spec changes, where we'd actually do some kind of pushback and say: Hey, this failed. Or: I rate-limited this, and you can basically rate-limit backwards that way. You can also increase reliability using a very similar mechanism, where you kind of go: The last Onion Message you sent me failed, and it turns out that statistically if things are not too busy, you will end up getting the failure all the way back to the source, which adds some reliability because at the moment they're unreliable — right?  You send it if somebody isn't you finds out because it times out, or you've got to send multiple and things like that. But that is basically a level above this, but basically getting the initial mechanism in is more than sufficient. Once we have champagne problems, like there's too many Onion Messages flying around, then we will look at more sophisticated things. So, there's a hand-wave sketch of what that would look like, but it hasn't got even a spectra after yet.

Speaker 2: It's also probably worth mentioning, naive implementation should, at least, do the thing they do for gossip, which certainly we do, right? If you have time in your socket, you will happily fill it up with Onion Messages, but if you have any more important things to do, you will, of course, do those first. I think the fact that the available bandwidth is probably two, maybe three, orders of magnitude more than what we need for gossip messaging makes the denial of service attacks actually pretty hard to pull off in any meaningful way if you just repeat your messages a few times. So, I think there's an open question about: How high of a priority is it if you just do some kind of naive rate-limiting using the existing code you have for gossip messages?

Speaker 1: Yeah, the spec says you should do rate-limiting, and that's where it leaves it. So, I kind of agree with [Redacted]. We'll go with that, and we'll see. If we actually start hitting real issues with rate-limiting, as in we are rate-limiting too aggressively — real traffic, not people trying to stream video — then, we definitely have some things that we can do.

Speaker 4: Cool. Thanks for educating me on that.

Speaker 1: Cool.

Speaker 0: Alright. So, test vectors and then, a big green button — very exciting. Likewise, I guess, Offers 798, no updates here. Just waiting on interop.

Speaker 1: And [Redacted] to do test vectors. Full test vectors for all the fields and stuff. I'm just gonna — matter of typing, right?

Speaker 0: 1000 monkeys, GPT. That sort-of thing.

Speaker 1: Yeah, that should be easy. Because if you've got a decode routine, you can just feed them all in and check. So, that's basically right.

Speaker 0: Nice. Alright. 919, dust exposure threshold. This one has been sitting for a very long while at the bottom of everyone's to-do list because I believe we already do this, but it just isn't written into law. So, another to-do list bump, I guess, unless anyone else has anything to add here. Cool. The infinite to-do list grows ever longer. 995, simple taproot channels. [Redacted]’s not here. Anything from anyone else?

Speaker 2: There's a very large discussion to happen around the nonces, but [Redacted] should probably be here for that.

Speaker 1: Oh yeah, [Redacted]'s idea of basically going: Let's not do this at all — is something that we should discuss too. Like, not using taproot for our commitment transactions.

Speaker 2: Oh, sorry. That's what I meant, yeah.

Speaker 1: Yeah, it's a whole can of worms around that. I see the temptation. I can also see [Redacted]’s frustration with: But I did all this work. So, you're right. That needs a broader discussion.

Speaker 0: Okay.

Speaker 5: I wish it had come like two or three days early. Well, but in the interim, what are folks doing? Because I know that I'm continuing to operate under the assumption that we are gonna end up using non-sys. However, I guess I'm able to throw that code out.

Speaker 1: Yeah. Look, I'm always tempted by the simplicity of just going: Let's not do, or let's push it back, right? You know, we could have a future feature bit, where we've optimized our commitment transactions to have a single SIG, and that's cute. I'm really tempted to go: Hey, this is a good place to cut the research project, right? I don't know, you're the closest to implementing it. Like, what do you think?

Speaker 5: Well, basically what I'm saying is it's not that much of an additional onus to implement, but the simplicity of getting rid of the nonces is very appealing, especially in terms of the introspectability of the individual — the signature composition, you know?

Speaker 1: Yeah.

Speaker 5: It'll be easier to debug.

Speaker 6: And you're storing less sensitive secret stuff, right?

Speaker 5: Yeah. But here's the thing: It is very rare that I am a true neutral, but right now, I see the appeals of both paths with pretty much equal value. So, I would honestly generally be fine with either decision we may end up making.

Speaker 1: It sounds like you're the perfect person to make the decision, to be honest.

Speaker 5: Yeah, I'll sync with [Redacted]. I was hoping they would be in here and with [Redacted]. But for the time being, now definitely not seeing a problem with continuing to just implement those nonces. It's not hard. The nonces themselves. The refactor is a pain in the ass, as everybody already knows.

Speaker 1: Yeah. And I mean, the issue of playing a bit fast and loose with storing nonces and things is always, I think, the nervousness-making from a theoretical point of view. Getting rid of that is kind of appealing.

Speaker 5: Yeah, it is. In that regard, I have a PR that I actually just opened an hour or so ago against simple taproot to slightly increase the just-in-timeness of the local nonces for channel opening. It's very marginal. It also gets rid of the images that are there and converts them to memory JS embeds, so we can more easily see diagrams and update them. But this is all operating on the assumption that's — it's disregarding [Redacted]'s proposal for the time being.

Speaker 1: Okay, cool. Well, yeah, I guess, yeah, go away and have a deep think about it and decide which way you advocate for us to go because I'm too far enough away to really have an informed opinion, but I can see your dilemma. Good luck.

Speaker 5: Either is great, honestly

Speaker 0: Cool, okay. Alright. 1059, taproot gossip. [Redacted] is here here. Posted a comment right before.

Speaker 7: Yeah, I just posted a comment on the PR just giving a summary of all the updates that I took away from the meeting. So, just to get an ACK from everyone before I go ahead and actually update the whole doc. Yeah, so would appreciate it if people gave it a read before the next call.

Speaker 2: One thing that I was talking to someone about at the meeting, and I don't remember who, is we should take this also as an opportunity to really clearly define a lot of the stuff that's not as clearly defined. Like, there was some conversation about the disabled bit, and whether that means ‘My peer is gone, I can't write a payment,’ or whether that means ‘I have no available liquidity on my side of the channel.’ It seems some nodes use it for one thing, some nodes use it for the other, and that's really bad. That should have one definition. So, it might be worth taking this also as an opportunity to be able to much more clearly define some of these things that already exist — that will presumably continue to exist — but that we should all standardize on in one way or another.

Speaker 7:  Right, cool. Yeah, that makes sense. Awesome. Sorry, one thing just while we're on this, just one point that I just want to definitely make sure everybody kind of agrees on — and I think this might depend on the nonce decision as well, so this might be void — but the whole we don't care about the script thing means we can have like a three of three MuSig, right? And then the verifiers just need to check the output key, plus node one plus node two. Awesome. So, that's all good, and we can prepare the verify for that from the get-go. But, we also want to tell the signers in the spec how they should be creating this, and that would use nested MUSIG, which currently there's like — spoke to [Redacted] about this as well. And there's no current — yes, sorry, I see. Yeah?

Speaker 1: I spoke to [Redacted] too, and they're like: There be dragons. So, it seems like we need half aggregation — is the best we can do, which is also un-spec-ed. Thank you. But they're eager to do it, and there's some example code and things. There's a PR. A bad PR. I reviewed it. Has some fix-me's, like fix the endian here. So, there's a very rough PR for ZKP that does this, but it's mathematically quite a simple operation to do the half aggregation. So, we could half aggregate the two signatures, and that may well be the way we have to go because recursive MuSig is not something that's going to happen anytime soon, it seems. Was that your conclusion too?

Speaker 7: So, my initial conclusion was just: We can kind of leave it a little bit open, but give a suggestion. In the meantime, we can say there's an optional Bitcoin key one, Bitcoin key two plus tweak, and then, they can reconstruct and it can be a four, four — like a flat four, four. But that's optional, right? And the verifier only verifies that it's a four, four, if those things are there. Otherwise, they assume it's a three of three. Then, the creators of the message can deviate from the spec when they're creating it. So, they can play with half aggregation or nested using or whatever if they really want to.

Speaker 2: I was not convinced. Did someone talk to — oh, you spoke with [Redacted], you mean [Redacted]?

Speaker 1: Yeah.

Speaker 2:  And why do we feel like we need to have this need for recursive MuSig and not be aggregatable? If we say: I'm okay with my counterparty deliberately picking a node ID that is the inverse of my node ID, so that they can forge a signature with only the on-chain parts. Like, we don't care. If we're okay with that is not in our security model, I'm wondering why we can't actually just do this.

Speaker 1: Above my pay grade.

Speaker 7: But wouldn't the whole let the verifier kind of just verify three of three — kind of let that be a possibility. It's just not the suggestion we give to the channel peers creating the message.

Speaker 1: You can certainly do two separate signatures: one with the taproot key and one with the MuSig between the two nodes, right? That would definitely work, right? That's very simple. There's no aggregation. There's two signatures. You could definitely have a variant that has one signature and you say: If it's one signature, just assume it's signed by all three because it's easy to verify. It's just that no one may be able to create that without a lot of more math-math.

Speaker 2: Let's have a conversation with [Redacted] again. Because if we just agree on a nonce, I think we can just add the keys because we don't actually care about the linearization here or the delinearization. It will have implications on the verifier, I think, because you don't add the hashes and something- something. But I think we should get on the same page there before we jump ahead. To your more direct question, I don't want to implement it. Let's just try to get on the same page. Hopefully it won't take more than a week or whatever.

Speaker 7: Cool.

Speaker 1: Okay. So, I mean, at the end of the day, what we win out of this is one less signature. So, we save 64 bytes. So, I'm not panicking over it.

Speaker 2: Yeah, that's true, especially if we don't even have to worry about the details, we just add them together. That'll be nice and easy. So, let's follow up. I guess I will take that as an action item. I'll follow up with [Redacted].

Speaker 1: Cool. Okay. So [Reacted], choose which dragons we slay. Excellent.

Speaker 0: [Redacted], do you want to talk about SCIDs now?

Speaker 8: Sure. This is something that [Redacted] came to me about in New York, and I guess there was some conversation that I wasn't part of the process of. [Redacted]. [Redacted], you could correct me if I'm wrong. It could be for offers in particular.

Speaker 2: Yeah, we had a conversation.

Speaker 1: I think I nodded. I think it was like: Yes, we should do that.

Speaker 2: We had — well, no, and then you suggested another variant. So, there was a conversation around switching to relaying based on SCIDs for the Onion Messages. So being able to select the next hop in a blinded path for an Onion Message by SCID, and I think there was agreement to do that. Then, there was a question of: Well, what about specifying the introduction point by an SCID and one bit? So then, it was a question of: That's complicated, but is it worth it for the size? And I asked [Redacted] to come up with the sizes, and apparently they have an answer for us. Take it away, [Redacted].

Speaker 8: Alright. I need to pull up what I sent to you, which I think is my Discord chat. Sorry, give me a minute. So, roughly for anything that has blinded paths — and I think I had to find those paths to have, I want to say, two hops — there would be a 33% reduction in QR code size, or at least, in the factory-to-encoding size. So, that's essentially the numbers I got.

Speaker 2: So size with — this is switching from just the introduction node, right?

Speaker 8: No, these were all of them — sorry I wasn't clear. So, I use the one bit plus or eight bytes for the interaction and eight bytes for the other ones.

Speaker 2: Okay, do you happen to know offhand what the difference was if we just do half of that?

Speaker 8: Offhand, I don't.

Speaker 2: Okay.

Speaker 8: But there's a difference in size, like the byte size is less than a third.

Speaker 2: Yeah. Yeah, that's a pretty big deal.

Speaker 1: Yeah. Doing the inside stuff is trivial. The fields are already there. It's just a matter of going: Yes, you can set this, and you should use it. Doing it for the introductory point, of course, is a bigger spec change. It's more than one line. It's all doable, right? Someone's got to figure out what that looks like. Where do we put that extra bit? Do we try to stash it in the — do we put it in bit 63? I don't know.

Speaker 2: I mean, we can just use a byte for that. I mean, it is removing a full pubkey, and that's a pretty big difference in a lot of cases, especially in QR code. Yeah, 24 bytes. I mean, some of these changes, and I guess [Redacted] can share this table that they have, but I mean, some of the changes are one blinded path or whatever, where we removed two pubkeys, and then the third pubkey is a third of that 30% difference. So, that means like 10% reduction basically, I think would be the estimate. Yeah. I hate it, but my vote would be: It's worth it. It's more work for [Redacted] though, so…

Speaker 1: Yeah, no, I agree. Okay, [Redacted], sounds like you're on this. Do you want us to do the spec change, put up a PR that makes both changes?

Speaker 8: Yeah, I'd have to look into the details, but it shouldn't be too bad, I imagine.

Speaker 1: Yeah, I think there's a bit saying: Don't use the SCID. To be honest, you can use the SCID, and then obviously, the receiver side needs to look at it. If there's no — I don't think it's security. I don't think it matters what happens if there's both. Pick one.

Speaker 8: Are you saying that every user still supports the old way to do these?

Speaker 1:  Yeah. So for long-lived paths, I think you generally want pubkeys over SCIDs. If you're trying to do it like a blinded path, it's gonna last for a long time. SCIDs are more transitory. So, there's definitely an argument to have pubkeys.

Speaker 8: Yeah, I mean, I guess the ones that are less transparent are the offer ones. That's really what matters, right?

Speaker 1: Well, it depends on how you're using offers, right? I guess you maybe you're not using blinded paths if you really, really care. But, at least, in theory,  the offer that you're gonna spray paint on a wall, it's going to be there for years; you may not want to use SCIDs.

Speaker 8: I wasn't there for the entire conversation, but yeah.

Speaker 0: Cool. Alright. 869, quiescence.

Speaker 6: Is everyone being silent about the subject? Was there something specific we were talking about? Or just that we like it and it's great?

Speaker 0: [Redacted] put on the list, but I can't really see any comments updates. Maybe we just wait till next week when [Redacted]’s back.

Speaker 6: Oh yeah. I think that's one of the things he's going to get working right for interop with us. It's more complicated than it looks. Maybe we'll talk to him next time I see him.

Speaker 0: Oh, nice. I guess [Redacted] will catch up with [Redacted] there. 863. Oh, splicing versus dynamic commitments. 863 versus 1090. Can we merge these two proposals?

Speaker 1: I know there was some discussion and whiteboarding, but I wasn't at the whiteboard. So to those who were there…

Speaker 9: So, after the simplified commitments discussion, folks from LND came up and they started discussing dynamic commitments with [Redacted]. As they were breaking it down, they basically came to the conclusion that the proposals are very similar. I think the action item there was on the LND folks to see if they could just remove the on-chain part from splicing and arrive at the same proposal. So, I think we're just waiting on them to see if that works.

Speaker 1: Yeah, I think that was my suggestion — that a splice without any actual adding inputs and outputs should map pretty well onto this dynamic commitment.

Speaker 9: Yeah, because they don't want to implement any of the interactive transaction stuff.

Speaker 1: Yep. They do, just not yet. They just don't know it yet.

Speaker 6: Yeah, I feel like that works. There's some weird things, like splice lock doesn't make sense anymore. A few little subtle things.

Speaker 9: Why do you say that? What does splice lock do?

Speaker 6: It's when it's locked on-chain six confirmations, obviously, if you're not doing anything on chain.

Speaker 9: Oh, I see. Yeah.

Speaker 1: Well, they are doing something on-chain though, right? I mean, this is the case where you wanna migrate to taproot. They just don't wanna change anything else, right? If you don't need to change on-chain, it's a different — then, there's the simple update protocol, which is even simpler, where you just, on reconnect, you just say: I want to be this kind of channel, and the other side says: I wanna be this kind of channel too; and you're done. But that's not the interesting case.

Speaker 6: Oh, is the other one that they move the funding output over to the taproot spot?

Speaker 1: That's the one they really want, right? Which makes sense. That's basically a splice without any in or out.

Speaker 6: A hundred percent, yeah.

Speaker 1: If you just wanna do something like flip to anchor outputs, you don't need any of this. It's way, way simpler.

Speaker 9: Okay. It seemed like they also wanted the dynamic amendment stuff to achieve that as well. But if you can already do it…

Speaker 1: Yeah, you don't need that. There's a proposal to do this, which is really, really simple. It is, and I've implemented it. It's really good. It just works. We haven't pushed it because we haven't had a significant reason to upgrade, but that's worth doing now, I think. Because it'd be good to flip around over to anchors.

Speaker 9: Okay. And that just uses the same STFU, yeah?

Speaker 1: Actually, STFU is optional for it because what happens is it just fails if you reconnect and you've got stuff in flight, you just don't upgrade; and you both know that. So, it falls out naturally. If you wanna force it to happen, then you want to STFU and then reconnect. But statistically, that's not a problem, right? What happens is, in practice, you upgrade your node and then it tries to reconnect. So, the reconnect is the logical point to do this. If both nodes have upgraded to the new hotness where they both want to change the anchors or whatever it is, then at that point, they will reconnect. Nobody's doing stuff on the fly. So, the reconnection point is the logical point to do an upgrade. The upgrade fails gracefully, and doesn't happen if there is stuff happening, right? So, if there are not HTLCs in flight, that's okay, but literally more HTLCs being proposed. So, if you've sent add HTLC or something, and then you failed in the middle of that and you reconnect, you won't do an upgrade. ‘Cause that's messy. So, it's actually independent of the STFU proposal because you can work it without it.

Speaker 9: Okay, cool. Yeah, I guess we'll see what they say once they're around for the next one.

Speaker 0: Alright. And last item on the list — this one's also been a little stale recently. 1049, clarify channel reestablish versus 1051, rework channel reestablish. Is anyone on the call keeping up with this? Alright. It doesn't seem so.

Speaker 1: GitHub says it's asking for my review. So I should do that, right? I will do that.

Speaker 0: On the to-do list. Great. Yeah. I guess, a reminder to anyone who feels like they can take a look at those two. They've been hanging around for a while. That's it for the sort of formal agenda, what I've got on the issue. I'd just like to make a request to folks who are at the spec meeting: If you'd like to take a look at the notes, and maybe amend them if there's anything you're unhappy with. I'm going to send those out to the mailing list on Wednesday morning. It's as good as we could do. The audio recordings didn't really come through, but I made notes and [Redacted] from Labs made notes, so we have some kind of record. Any other topics before we close out for today? No. Okay.
