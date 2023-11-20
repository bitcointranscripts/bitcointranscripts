---
title: Lightning Specification Meeting - Agenda 1076
transcript_by: Gurwinder Sahota via TBTBTC v1.0.0
tags: ['lightning']
date: 2023-05-08
---

Agenda: <https://github.com/lightning/bolts/issues/1076>

Speaker 0: First off of the list is dual funding. [Redacted] has merged the two small patches that we had discussed adding. There's only one small patch that is remaining, which is about making the TLV signed to allow for future splicing to make sure that splicing can also use the RBF messages for signed amounts. But apart from that, it looks like dual funding is almost complete. We plan on activating it on our node soon to be able to use it in Phoenix. Do you all see an issue with starting to advertise that feature a bit? Perfect. So, anything specific on dual-funding, or is it just waiting for implementation and the last few bits in other implementations?

Speaker 1: Very exciting. We're so close.

Speaker 0: Soon, you'll be able to test the Phoenix app that uses dual funding and splicing. Next on the list is a clarification on the truncated integers because it looks like we were not requiring them to be minimal, but actually, at least, our implementation was requiring it to be minimal. And apparently, C-Lightning was as well. The spec didn't say so, so I think it's a good idea to clarify the spec. I think the state of the PR is enough, and it doesn't need additional test vectors because there are already test vectors for that actually.

Speaker 2: I don't see why we need to worry about it. Test vectors are nice for failing, but who cares?

Speaker 0: Perfect. Then, I think we'll just merge that one. Then there's another very small PR to remove SHOULD requirements to disconnect on warning messages because they were confusing. Actually, it makes more sense to - whenever we a requirement somewhere, for example, in Bolt 7 when you receive a message that you should send a warning, if it makes sense to disconnect then we already say that we should disconnect at that time. So, there's really no good reason to have those in Bolt 1 with the warnings requirement because in general warnings, there's no good reason to disconnect by default. It's even harmful.

Speaker 3: Someone I was talking to was running Eclair, and their peer was running LND and Eclair was sending vaguely helpful warning messages and LND was disconnecting. So, this would be a behavior change for LND, but I think it is clearly merited.

Speaker 0: Yeah, in that specific case, the issue was that LND was asking for channel announcement for channels that were already closed. So when we receive those we do send a warning, but we do not disconnect but we send a warning about that. So, maybe that's worth fixing as well. It's wasteful to ask for channels that you know are already closed.

Speaker 3: Someone on LND could comment. But, at least, on this specific PR, someone should at least nag the LND folks to change their behavior.

Speaker 1: I think Core Lightning treats warnings as disconnects because I had to redo it. We added the TX abort message for dual funding stuff, and the big change with TX abort in Core Lightning is that we don't disconnect. So, I think Core Lightning will probably also have to change behavior for warnings, FYI.

Speaker 4: I'm happy with that. Having it occur rather than just randomly disconnecting. We have an issue at the moment that if the other side forgets their channel and we send a warning, we don't wait long enough for them to send the error that would make us fall on chain sometimes. So, you can get the state where you have to manually close if the other side has lost their database, so which is not the intention, right? You're supposed to receive that error from them and then drop the chain. In many cases, we won't do that, so I've been looking at this behavior anyway. I think removing this is fine. I think we went through the spec - that was a sweep - and we put wording everywhere to make it explicit. So, that's fine.

Speaker 2: Yes, I thought you did that?

Speaker 3: Well, we. Yes. I think it was done.

Speaker 0: Alright, perfect. I guess we can move onto the next one. The next one is a bit more tricky, and it's potentially harder to work on it only orally without writing stuff down - it's about CLTV handling in blinded paths. One of the things in the comments you made, [Redacted], that I don't understand is that - the way it works is really kind of the same kind of thing as non-blinded path. As a sender, when you have a blinded path, add more hops to reach the introduction node. When you start building your onion, you start from a block height at the recipient, then you add the CLTV delta for the route and your minimal final expiry delta. Then, you add the normal CLTV deltas to the other guys. So, we still send an absolute outgoing CLTV value to a recipient, which matches the value we started with. Does that make sense?

Speaker 2: Right, but each recipient in the blinded path gets a delta offset from that - right? - by looking at the blinded path? Am I understanding that correctly? So, what we actually send to each node in the blinded path, not ignoring the last hop, just each node in the blinded path is like: Here's the block height I started with. And then, look at the encrypted blob to figure out the offset from that.

Speaker 0: Okay, so what the intermediate nodes receive in the onion is not an absolute CLTV. The thing they receive is only in the HTLC, and in the non-onion part, the CLTV. In the onion part, they have an encrypted delta and they just should apply that delta to the absolute CLTV that they received in the HTLC outgoing CLTV. They just pass that all the way to the recipient. The recipient behaves differently, and receives directly in the onion, the absolute outgoing CLTV. Does it make sense?

Speaker 2: Right. There's two issues. Before we get into these details, let's ask the question: Who should add the random privacy fudge factor? Should it be the person creating the blinded path - i.e. the final recipient - or should it be the sender? Because we could go either way. We could say the sender adds - or both, although now we're just adding a lot of CLTV.

Speaker 0: But the thing is, if it's not both, you cannot trust that the other guy has done it, and adding a CLTV here protects both the privacy of the sender and the recipient. So, both of them may want to add random delays, and they cannot trust the other to add them. I think that both of them need to add some random delay, right?

Speaker 2: Okay, yeah. Makes sense. So then, maybe we need to specify as well that the recipient - if they have added one, they need to encrypt it back to themselves in the blinded payload that they'd bluffed for themselves. We don't have to specify how, but we should probably specify that they have to do that.

Speaker 0: Yeah, it's true that these things have not been specified much right now because only the blinded path mechanism has been introduced, but the way you create blinded paths was only done for the first time in Bolt 12. But I agree that this is really confusing and there are a lot of ways to interpret that. I agree we should do a better job at explaining those, and maybe going through a lot of examples will also be very helpful to see where to make it more explicit. I can spend some time doing that. Create a document where it's easier to see how it behaves - at least in Eclair - how I think it should behave. Then, people can comment on it.

Speaker 2: Right. I had understood that the behavior of all of this would be the same for - okay, so I was trying to document what had been communicated to me via a game of telephone of how Eclair operated, not actually looking at the code. That's just wrong. I had just written down that it's offset from zero, right? So, it's no longer an absolute CLTV, but in fact, just the delta from that the final node would be able to subtract this delta, and they should get the current block plus their expected difference, which would work as well, I think. But if you currently do the absolute value final as a block height difference, then we should document that instead. So, I will update this PR. Maybe not today. I will change the way it's worded.

Speaker 0: Perfect. I'll add more details in a document that makes it easier to explain how it works, and we will see how it goes then. I think it's going to be easier with diagrams and concrete examples.

Speaker 3: Do we need to have both ends add CLTV? I would say it's the responsibility of the person making the blinded path to add any CLTV padding. They certainly need to be able to do it because if they're actually secretly forwarding it to someone else - the classic: I'm wrapping someone else's invoice case - they do. But does the sender need to bump CLTV or can they just...?

Speaker 0: Actually, the sender protects themselves that way - actually, no. Maybe not. Actually, it's just that this way ensures that the next to last hop cannot guess who the last hop is. If the last hop didn't add any random values, the next to last hop can infer who the last hop is, and maybe the sender doesn't want that, so the sender adds a random delay. They cannot trust that the recipient has added a random delay.

Speaker 3: It's the shadow route thing again, where they pin to that.

Speaker 0: Yeah, with blinded paths, the sender can only add a delay and start with an absolute value at the recipient that is not just the current block height plus a few blocks for potential blocks found during payment propagation, but a bigger random delay to make sure that the next to last hop cannot guess who the recipient is.

Speaker 3: Okay, that's fair.

Speaker 0: Alright then. Should we move on to the next one? The next one is onion messages. There are a lot of small comments on the PR - I think just to finalize everything; nothing major, but the small things - but apart from that, we should be somewhat ready.

Speaker 3: Similarly offers. I should go through these. and make sure they're all addressed and merged. I agree, I don't think there's anything huge.

Speaker 0: Since we don't want to frighten people by merging two big PRs at the same time, we should merge onion messages soon, so that we have a bit more time before we also merge Bolt 12. Apart from that, I don't know if there's anything new on the onion messages PR and offers. On offers, the only topic that I've seen is the one linked to that CLTV delta. The fact that the blended paths do expire - they have an expiry in absolute block time - but the invoices do not include that expiry, but have an expiry in seconds, which makes more sense for users and to a UX. You go to a merchant website, you don't want an expiry in block height, you want to see an expiry in absolute timestamps. But that means that the creators of the invoices have to juggle between absolute timestamp and the route expiry to make sure that actually those two match.

Speaker 3: Yeah, the expiry on blinded routes was later than the original expiry from Vault 12, which is based on the expiry on Vault 11. I think having an expiry on your invoices that is not in seconds is weird. So, my assumption was that: Yeah, you would set your blinded path to be something larger. I mean, that's just a sort of safety check rather than a critical thing whereas your invoice might actually be: No, no, you need to pay by this date.

Speaker 0: Yeah, I agree, but that's just something that is not explained in the Vault 12 specification, and that can be confusing. So I think it's worth just putting it somewhere.

Speaker 2: Should we just remove the expiry from blinded paths? I mean, if you're staring at the expiry on an invoice, then...

Speaker 3: But you can still send - the expiry on the blinded path stops you, the path at all. It's designed to be a mechanism to avoid undue exposure, right? You don't want some vast time in the future you because you can you can find out who people are by uptime at some point, right? And if you give someone an eternal blinded path...

Speaker 3: Oh, the fire in the blinded path is in the per hop. Okay, nevermind. I will shut up.

Speaker 3: It has a different use, yeah. But obviously, there's a blinded path that doesn't last as long as their invoices a little bit defeating. So yeah, there should be a note there.

Speaker 0: Is there some other progress on offers or onion messages that someone had been working on or something to report? Anything to report?

Speaker 3: Yeah, Bolt 12 test vectors. I think we might need to regenerate those. Yes, I'll put that on my to-do.

Speaker 0: Then, for next topic, I don't think there's anything new on the dust exposure threshold PR. It's just missing some reviews. So, whenever people have time, just have a look at it so that we can merge that. And then, there's taproot. I don't know if there are people here who've been working on taproot recently. At least, people from the LDK team.

Speaker 4: Yeah, just started working on it again after finishing Swift stuff. I should have a PR up for LDK that will introduce the taproot feature - introduce taproot signer struct, and updates to the channel, and channel manager structs that implement the differences in the signing behavior. Next, I'll try to actually connect all of those different things.

Speaker 2: So, we're a ways away from anything too exciting there. At least, it looks for cross implementation thing.

Speaker 0: But on the specification, you do have agreement between LDK and LND on how it should be done, right?

Speaker 4: For the most part, yeah

Speaker 0: Okay, good to know. So then, maybe taproot-gossip. Has there been any did anyone have time to have a look at taproot gossip?

Speaker 3: Is that going to be the battle royale of New York?

Speaker 2: Probably. But [Redacted] keeps promising an introductory post on the mailing list to start the discussion there as well, and I guess that has never happened. Although, I guess, the other folks working on it could also do that. But for now, it keeps promising stuff.

Speaker 4: I mean, don't we all?

Speaker 2: Indeed. Indeed, we do.

Speaker 0: Alright, so next up then is splicing. And we've made a lot of progress on splicing recently. We've been starting to experiment with a version of Phoenix on testnet that uses splicing to only keep one channel per user, and it's really fun. It's really nice. So, we'll be able to share our testnet builds if people are interested and have Android. I think on iOS, it's going to be a bit painful to share to easily share a testnet build. But if some people want to try out an Android version and see what seems weird in the choices we made, just send me a ping and we'll send you a build this week or the week after that. And apart from that, on the specification, [Redacted], are there things that you wanted to discuss? I think we've been just making progress and implementing stuff.

Speaker 5: Yeah, I think we have everything kind of settled. There's definitely a lot of spec cleanup to do, which maybe would make more sense to do as we get into interop. But I did have one thought - which is just kind of a future thinking thing - is that: Do you think we'll ever want to use SIGHASH single in the interactive transaction protocol? So, if we ever want to use it, we probably should include support for it now before everyone else starts building it out. You know what I mean?

Speaker 0: Why can't we just assume that right now it's SIGHASH all, and if we want to use something else than SIGHASH all, it will be a new TLV that you have to understand that's mandatory or...

Speaker 5: Well, I mean, like if one side wants to use SIGHASH single and the other side doesn't care, right? There could be a scenario where it'd be helpful to be permissive of that - like, allow the other side to add SIGHASH singles and be like: I don't care; put them in. And maybe also broadcast them for them.

Speaker 3: Hold on. So I mean, it doesn't - oh, so you're sending straight signatures? You're not seeing SIGHASH flags at the moment?

Speaker 5: Everything is assumed SIGHASH all, yeah.

Speaker 3: Yeah, you're gonna need to fix that. Because one of the theories was that you might want to - because we have SIGHASH singles, right? You could be an existing HTLC transaction that you're trying to sew through your giant transaction that you're building. So, which is one of the reasons you can negotiate your input and output numbers so that you can try to make them match. So yeah, you probably want to think SIGHASH flags at that point.

Speaker 0: For which inputs do you mean? For the shared input or for normal inputs? Because for normal inputs, we just send the whole witness, so it has everything you need and it's not a shared signature. It's only for the previous channel output that you really need a shared signature ,but you don't have a choice here. The output was created to - Yeah.

Speaker 3: Yeah, I agree with you. Using single there is weird. As long as you can do it to your own inputs, it doesn't matter.

Speaker 5: Right. I think, in theory you can, but there's this question of the ordering of stuff, and currently...

Speaker 3: You've got a new random number now.

Speaker 5: Exactly, yeah. And then, if everybody tries to pick serial ID number one to get in front. Like how theoretically could happen without a spec change. But if that's going to happen, it feels like maybe we should do it a more correct way than random serial numbers. I don't know, it's a thought.

Speaker 3: No, random works shockingly well in practice. I mean, even if you both have an ordering, as long as you're both not naive about your ordering. You're both not trying to get numbers because you don't care which position as long as they match, right? So, statistically, you can always get what you want. You can always remove it again if you decide that you didn't like it.

Speaker 5: Oh, it's a good point.

Speaker 3: Right. So, it's theoretically possible that you will fail to get matching slots, and then you can remove it and try again. Or you've hit zero and you can't go any higher. Or you've got one, they've got zero, and you're like: Okay, well, I can either switch these or not. But in theory, yes, they've got the maximum number and the minimum number. Actually, you can't have both because one of you is constrained to odd, one of you is constrained to even. So, you can always get one in, right? But yes, in theory, you could fail to construct it the way you want. But, if you're just using random numbers in a 64 bit space, you're going to be able to put them wherever you want. So, I don't think it's actually a problem. I mean, I haven't implemented it, and it would be a little bit tricky to do, but it's certainly possible.

Speaker 5: Cool, yeah, that's the last like remaining question in my mind about the splicing spec, and I think everything else is pretty much there.

Speaker 3: So, we do have channel types in there now for the splice?

Speaker 5: That is a great question. I don't know.

Speaker 0: I don't think the specification right now adds it, but it's just a TLV that's already in open channel and accept channel, and that we need to add to splice and splice arc.

Speaker 5: So I don't think we have it now. Is the idea to upgrade channel types or something from an old V1 to V2 or something in a splice?

Speaker 3: You can just abort if they ask you for something that you don't support. You just go: No, I'm not going to splice into that channel type. That's fine. But, it's an obvious mechanism for us to upgrade later on when we get fancier channels.

Speaker 5: Right, yes. That is something that needs to be done.

Speaker 0: Yeah, and on our side, we haven't worked that much. We just started working on the quiescence part because we've started for Phoenix with just a poor man's quiescence, where we only initiate a splice when there's just nothing on the channel - no pending HTLCs, nothing. So, we're going to add quiescence on top, and maybe we'll have comments when we do that. But looking at the spec PR and at how it would be implemented in Eclair, there doesn't seem to be any issues there. So, we just have to do a compact test to verify that we understood it correctly. But I don't think there's anything weird that's going to come out of that implementation.

Speaker 3: So, the other comment that I have is that I wonder if we should implement an optional reconnect message. So, the moment we had this idea of when we reconnect, we reset everything. We could have a message that says: For this channel, pretend I've just reconnected. So basically, I know a channel reset kind of thing that would simulate the same flow. So this would...

Speaker 5: Be TX abort?

Speaker 3: Kind of takes TX abort on a slightly more general - like for a case where we send a warning because the other side's messed up. And we hang up so that we'll reconnect, and we'll be forced to go through re-establish again. But that's disruptive to other channels that they have, especially if they're in a loop. Whereas if you could just send a hang up this channel - like a channel specific message saying hang up - then you act as if you've reconnected for the purposes of that channel. So, we're gonna have to reestablish. It'll be very similar to TX abort, only more general.

Speaker 5: Do you think we might be able to drop TX abort and just have that?

Speaker 0: What does it add on top of TX abort? Because it seems to me that's exactly what TX abort does, right?

Speaker 3: I don't think you can send TX abort if you're not splicing. We had a case where they've re-established a channel, but that number is messed up. So we send them a warning, and we end up hanging up on them because we can't do anything with the channel. But if they've got another channel that is okay, we just disrupt that because we're messed up. It's an unusual case, but it would be nice for us to say: Okay, just reset this channel, and we can go through the reconnect dance again. But I'm not gonna close connection.

Speaker 2: It seems like a lot of work. I mean, just disconnecting and reconnecting doesn't interrupt for very long.

Speaker 3: It does appear in a loop. Yeah, there are some cases where I can't talk to you anymore about this channel because you were way out of sync. So, at the moment, you have really no choice but to do a massive connect to reconnect, and that can be disruptive to multiple channels. It's kind of because the spec kind of - we retroed in multiple channels at the last minute and multiplexed it - and so, we have this awkward space here where we use reconnect as a huge hammer for things. But I mean, in theory, it could be an odd message, so it wouldn't be harmful. And maybe if they didn't understand it, you would then just hang up; if they talk about the channel again. If they send something unexpected, you'd just go: Well, you're wrong. Anyway, it's just a thought - I've thought it would be nice in some ways from a protocol point of view to have such a message. So, I would throw it in there in case you want one.

Speaker 0: Yeah, to be honest, I'm not entirely convinced yet. We haven't felt the need for that yet, but why not? Well, let's try it. Why not? I don't think it needs to hold up the splice PR, but we'll see. We're still far before we can finalize any of these. Alright, and I guess the next two items - there hasn't been any progress on those: fat errors and clarifying the channel established requirements. I guess no one had time to look at those or do any implementation work here.

Speaker 6: For fat errors, I played around with Rust Lighting a little bit and hacked them into it and see them interop with LND. So, that is implementation progress. On the concept itself, I think we're still where we were last time.

Speaker 2: Indeed, and that forced me to actually look at it though. So, I spent one evening, where I was already falling asleep and clearly didn't come up with anything interesting. But I stared at it for a while longer, and am little more convinced that we can't actually do better than this stupid N-squared thing. So I'll probably get back to that again sometime in the next week or so. I'm much happier with the design, which means I will actually have to go review the spec and give more useful feedback on the spec rather than just saying: I don't know, I'll get to it.

Speaker 6: Alright, looking forward to that.

Speaker 0: We're still interested as well on the Eclair side. It's just that we are deep down in the splicing and Bolt 12 rabbit holes. So, whenever we get out of those rabbit holes, we'll have time to look at it. But I don't know when that will be.

Speaker 6: Don't you feel that something like this is more of a fix on a base layer? That's something that you should have done a long time ago already, where we're splicing and Bolt 12 is more additions to what we already have.

Speaker 0: Yeah, definitely, but now that we are deep in that rabbit hole, we want to get out of it before we can put our brain onto something else. Otherwise the context switching is going to be too hard.

Speaker 2: Yeah, and as much as this is a nasty issue - which should be fixed - users don't feel it as much because nodes happen to mostly be honest. So, for the most part users feel the pain of of non-reusable invoices and expensive new channels and closes, especially with fees going up. So, it does lead to a little bit of an inversion of what priorities could be.

Speaker 6: Yeah, we should get that LND hacker guy to surf and roak invoices. That make nodes upset because they start to penalize all their channels. So, at least, for LND.

Speaker 2: If we're done with this, unrelated topic, which I forgot to put on the issue - Core Lightning is serving update type onion failures without a channel update in it, which the spec isn't clear in the actual body of it but elsewhere - and I didn't look at the git history whether this is new or not - it says that you have to, and we were expecting it, and we get mad at Core Lightning nodes for not doing this. We actually blame the inbound channel rather than the outbound channel, because we were like: Oh, this node gave us garbage. We don't like this. And maybe we should fix that, but I think the question is: Will Core Lightning fix it, or should we start treating this as actually okay? Well, I mean, it's also a question of if you're sending a temporary channel failure and you're sending it because there's not enough liquidity, it's not crazy to not want to send a channel update message. I mean, it's a speck of violation of how it's worded today, but it's not crazy to just not include that.

Speaker 3: Yeah, [Redacted] has reported this as well, and it's on my to-look list, but I got flooded for last release. So, I'm not quite sure where we did. I knew there was a weird corner case where we did it, but obviously it's hitting. So, we must be missing it somewhere else, which is odd. So, I do need to actually go and reproduce it. It shouldn't be too hard, because it seems to happen. Well, other than the fact that we should have a message that says: It is your payment. I think we should have a separate capacity issue payment-like message because, at least, for many implementations, this could also mean the node is down or there's no connection at the moment. So, a hint that trying a different amount might help would probably be useful. In practice, that's what people do, and it would just speed their efficiency. And how many bits of hint - like, how much hint you give them - is an open question. I've suggested we have an order of magnitude approximation where you go - I think for most implementations, if you would have to reduce it by a factor of 100, it's not interesting. It is a failure. If you reduce it by a factor of 2, then maybe it's still interesting for you. So, having a number of bits that suggest the order of magnitude would be nice. Now, whether we retrolate into the existing one or have a new error, I don't know. I know that LND may still send unknown peer if the peer is disconnected, which is obviously incorrect, but everyone has to handle now. But yes, I will definitely look at this. There is a PR, so I will fix it.

Speaker 0: Okay. So, the next two. There's a here's two old competing PRs to clarify the channel reestablish requirements because last time we looked at it, we all said that it was a mess but just whenever someone has time to review them. Then there's the peer storage backup because C-Lightning had started working on it with one of the summer Bitcoin interns. Is that correct?

Speaker 3: Oh, yes. [Redacted] has an implementation, and it's very, very simple. So, we need to write up a spec. [Redacted] was trying to seek a grant at the moment to continue that work, particularly the spec work. So, it's sort of in a holding pattern.

Speaker 0: Okay. We can definitely talk then about mailing list moderation. So, is it just you, [Redacted], moderating the emails right now?

Speaker 3: It seems to be. So, the three moderators are [Redacted], myself and [Redacted], but I went away for a week and it seems like nobody did the moderation. So, I'd like to throw in a couple more moderators. The only problem is that there's a single password, so it's basically complete. It's very open kimono. If you give someone access to moderate the mail list, they have complete control on the mail list because this is mailman. So, I would like to have a couple more people, particularly in different time zones who've got access. [Redacted], sounds like you're volunteering.

Speaker 2: Oh dear God. I mean, I'm happy to do it. But you know me, I create drama. So I mean, if you want me fine, but that sounds like a bad idea.

Speaker 3: Yeah, I didn't say I would continue doing it. But you're welcome to do it. And [Redacted]. I mean, if people who post regularly are good people as moderators, because they'll at least check it when they post and push their own post through. As you know, there was some personal drama that was in danger of spilling onto the list, which is why we turned on emergency moderation. That seems to have died down and it is possible we could switch emergency moderation off, and it would not be an issue. I have not had to moderate a huge amount, surprisingly, under that. All I've been doing is putting delays into the mailing list. So, did I send an email when moderation turned on last week? Yes, I did send a mail, and then I forgot to push it through. So, it was in the moderation queue for a while, but there was a mail-to-mail list about emergency moderation.

Speaker 7: Okay, I missed that. Thanks.

Speaker 3: So yes, I will signal [Redacted] and [Redacted] the access credentials, and I'll update the thing to say that you're also moderators, and that's it. Then, we will decide whether we switch emerging moderation off again because it is a pain.

Speaker 2: Damn, you're gonna make me go post to the mailing list more regularly, weren't you?

Speaker 0: I agree with what [Redacted] said in one of the mailing list posts: We haven't posted a lot on the Lightning Dev mailing list. A lot of things have been happening directly on spec PRs, and people who are not following spec PRs that already have thousands of comments are missing some interesting bits. For example, the part about the liquidity griefing attack on dual funding. So, that's why I also decided to start posting that kind of thing to the mailing list. I think we should try to post some of the important stuff we discover in the spec PRs for the important features, such as taproots, splicing, dual funding - those complex stuff. It makes sense to have them in the mailing list, where it's easier to search for than in GitHub comments in big PRs. So, if other people have time to share things that they discover on the mailing list, I think that would be helpful.

Speaker 2: Yeah, there's also stuff like - I know LND did a bunch of routing work in their last release, and that was cool to me because I was also doing some similar stuff and wanted to crib off their notes, but sadly they never got a chance to write it up. And that's the kind of thing that I think could also be on the mailing list. And I'm now realizing that I'm accidentally setting myself up to write about what I've been working on, which was a mistake, but oh well.

Speaker 0: Alright, so is there any other topic that people wanted to discuss? Is there anything that comes to mind? There's been There's also been a new PR opened by [Redacted] about the HTLC endorsement - the reputation part of Jamming. But it's really a draft PR for now, and I haven't had time to look at it yet. I don't know if other people had time to look at it. It's 10.71.

Speaker 2: It was pretty short, right? It didn't actually specify suggested strategies for doing the endorsing, but it had a link to something else that didn't specify a bunch of drafts for that. So, I felt like I had to go read that, and then I kind of fell off and ran out of time.

Speaker 8: Yeah, it's just a draft PR at the moment. Sorry, I don't know what draft draft implies on the spec, but we just wanted to have it up to have something to refer to when we talk about the endorsement structure. But we'll fill it out with the actual reputation thing and then take it out of draft. It's just easier making a draft than opening on your own fork and then comments get spread between all of that.

Speaker 0: Perfect. That makes sense. Then it's easy for us. We don't have to look at it yet. Perfect.

Speaker 8: Yeah, I'll take it out of draft when it's ready for a look, and I'll bother everyone massively. So, you'll know.

Speaker 0: Perfect. So, anything else anyone will need to discuss?

Speaker 2: Wait, there was one other thing. I was just looking at the PR list. Oh, WebSocket. PR 10.68. [Redacted] with attempt to revive WebSocket push, and announce basically the host name that would receive a WebSocket TLS wrapped thingamajig.

Speaker 3: Yeah, so I was going to close the other one. I don't know if this PR got merged. No, I think it's going in next time. But I mean, having WebSockets is kind of cool, but advertising it is a whole another can of worms. So, I decided to split the two. I like the fact that we have WebSocket support, and you can offer it, but mainly people are using it for commando and things to control their own nodes, rather than as a generic mechanism for nodes to actually talk to each other. So, at least for us, that part is less interesting. So, I was going to withdraw the WebSocket announce PR.

Speaker 2: Yeah, I kind of agree, but I do wonder whether anything changes when we're talking about onion messages, because then you can have a website that connects to a node and asks for an invoice or something. I don't know if this is actually a good idea. Maybe this is, in fact, a bad idea, but it's a thing to consider when we discuss it.

Speaker 3: Well, I think actually having public web socket proxies for Lightning starts to make sense. So you can connect to the proxy and it will connect to the lightning node for you, and you can speak lightning from JavaScript. Its kind of nice. But for for individual pleb nodes, not quite as interesting, I think.

Speaker 2: Well, it'd be nice to skip the proxy. Like, there's no reason to want a proxy.

Speaker 3: Yeah, because not every node will support WebSocket. So, you have a proxy and you connect to it, and it connects out.

Speaker 2: But you could do onion message routing starting with nodes that do support the...

Speaker 3: Yeah. I think the straight to the proxy, I kind of wanted to implement one somewhere. The problem is that because you need WSS, you need a web certificate and everything else, and I don't think most people are going to do that for their nodes.

Speaker 2: Yeah, I mean, it'll be a relatively rare thing, but I think the question is more: If you were to announce it, then basically you get this proxy thing for free. Basically, any lightning node that does do this, not only is a proxy, but then if you fetch a snapshot of the graph or something, then you know a list of proxies, rather than having to have that be a whole separate concept.

Speaker 3: Yeah, but I think it's not a priority. So, I was going to close my PR, and then somebody can implement it and then push it.

Speaker 2: It's certainly not a priority for me. I guess my question was more - well, I mean, it might be a priority for [Redacted], so [Redacted] might implement it in the LDK, but I think the question was more: Is this a 'Well, maybe we could do this?' or is this a 'No, we don't want a website connecting to my node' kind of thing? I guess you could always just not add the TLS wrapper under your node if you didn't want that. But more of a philosophical question: Is this a thing that we want to do? Obviously, I don't think this is happening soon.

Speaker 3: I don't know. That's why I think if someone wants a proxy and it becomes popular, then you start to go: Cool, everyone should have one, and we should probably push the PR. But if this proxy is used by three people, then maybe it's not worth pushing. I don't know.

Speaker 2: Yeah, I mean, the other thing is a bunch of people trying to build LDK-based nodes and WASM. And for some reason, these stupid web browser extension wallets are popular. I don't know why, but people keep trying to build them and they keep getting users and it's frustrating, but that also means no direct TCP for these things.

Speaker 3: Yeah, that's why I think the proxy idea kind of makes sense. And to bridge the web and lightning worlds is kind of cool. It's unfortunate that we have to go through this hacky web socket thing to do it. I mean, I've been pitching this idea to people that we should eventually end up with nodes that provide you with a service card of: Here's all the services I offer. And this could be one of them, right? I will proxy your stuff. I will provide a web socket and I will provide back up; all these things that you could potentially do.

Speaker 4: I think it's probably a good thing because due to the inherent limitations of browsers. We probably don't want browsers being able to run full nodes themselves because they can't do chain monitoring. They can't guarantee that your funds aren't going to be breached.

Speaker 2: You can as an extension. I mean, insofar as the computer's online, but the normal extension. That's why the browser extension things are popular, right?

Speaker 3: Also, importantly, I don't think we can stop them from doing it badly. But yes, I'm not going to write one. So don't oppose it, but I'm not particularly interested in it, I guess is the answer. But I am going to shut the old PR.

Speaker 2: Okay. Well, then I think don't be surprised if [Redacted] goes and implements it in LDK and then nags people about it. Just 'cause they are actually building a wallet that runs in WASM. I don't think in a browser, but it does run in WASM, which may imply that just using WebSockets is easier for them.

Speaker 0: Alright. Anything else or should we wrap it?

Speaker 8: I've got a meta thing about the summit if there's nothing else. I just want to ask how folks want to get together a topic list. I was thinking of sending out a survey to everyone to add topics, and then another one to vote. Is that alright? I can't remember how we did it last time.

Speaker 0: I think that last time we had an issue on the spec repo and everyone added topics in there. Those topics contain potential links to documents, and it was simple enough. I can try to find that old issue. I think it's lying around somewhere.

Speaker 8: Okay, perfect. I'll spin up an issue then, and then everyone can just drop in things they'd like to talk about. Seems like a good idea.

Speaker 2: We should put a public note that - now, at the spec meeting, is not a time to unveil a grand new proposal, because it's far more productive if people get to look at it beforehand, and then you could discuss it rather than getting thrown it this brand new idea face to face. I mean, sometimes it happens because you come up with ideas. But if you have some great thing you want to bring, surprise is not your friend here. Because it's just the time everyone to get up on it. It's not useful. It's nice if people have a bit of foretelling about what they're interested in is actually a really good idea.

Speaker 8: Okay, great. I'll add some advisory to please link documentation beforehand rather than just random topics. That's all for me.

Speaker 0: Alright, then I guess we're all good.
