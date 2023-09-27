---
title: Lightning Specification Meeting - Agenda 1101
transcript_by: Gurwinder Sahota via TBTBTC v1.0.0
tags: ['lightning']
date: 2023-08-14
---

Agenda: <https://github.com/lightning/bolts/issues/1101>

Speaker 0: Alright, should we start? I want to talk a quick update on dual funding because I've been working with [redacted] on cross-compatibility tests between Core Lightning and Eclair, and so far, everything looks good. The only part that has not yet been fully implemented in CLN is the reconnection part — when you disconnect in the middle of the signature exchange. This kind of reconnection is supposed to complete that signature exchange with one new TLV added to channel re-establish. So, I'm just waiting for [redacted] to finalize that, then I'll be able to do cross-combat test on those two. Once both are compatible, I guess we're gonna probably rework the commits and rebase the PR on top of master, but then it should be ready to go. That will also free up some cleanup on the quiescence and splicing spec PRs, so that we can have the same basis to work on those.

Speaker 1: Cool.

Speaker 2: Cool. We're trying to look at some of the questions and splicing stuff and it was kind of a stack on top of each other. So, decoupling it would definitely make it easier to work through and understand.

Speaker 1: Yeah, [redacted] isn’t here. So, I actually don't know. Is it further up? There's splicing further up. No?  Anyway, we've shipped an experimental splicing, so people are busy breaking it all over the place right now. So there's this. It's experimental, so they get to keep both pieces when they break it. It turns out one way to test is to do testing in CI. The other way is to just throw it at users, apparently.

Speaker 2: Oh yeah. They'll do all the random shit that you need, basically.

Speaker 1. I know. A little bit more testing would be nice, but they really wanted to make it into this release, so it's labeled experimental, and people can turn it on and keep both pieces. It works in the happy case. It's just all the unhappy cases, where people are discovering force closes and things. Hopefully that will resolve in the next three days before I do the final release.

Speaker 2: Cool. Is there any stuff that should start to come back to this book? I know [redacted] had that gist of other edge case-y stuff, and I'm guessing now the idea to sort of compile that down into a new text eventually in terms of what actually works a lot or what needs to be changed or whatever.

Speaker 0: Oh yeah. I haven't worked on that at all, but at some point, we were discussing how to represent message exchanges so that we could have test vectors that would be exactly the messages exchanged. It could also be an input for the test at some point, but it's also useful to have something visual, where people can see exactly what messages are exchanged and why this scenario is not working, so that people implementing the feature understand some of the edge cases and details that can happen when some of these messages are out of order or something like that. But I haven't worked on it more. I think I won't have time to work on that in the very short term, but that's definitely something I'll come back to.

Speaker 2: Cool. Yeah, and then the other related things — we started to take a look at the dynamic commitment stuff again. Kind of what we talked about in IC around aligning it, at least, with the message prefix and making sure the message flow meshes as much as possible. That's something we're doing in the background. I haven't started any code or anything. Just refreshing our mental model of the actual PRs, given some nuances if you looked at it last. But I think we'll have anything that comes through either on the questions or the slicing things. I think we also want the STFU for this as well, because otherwise, it's hard to do upgrades. I mean, it's simpler if there's no HTLCs. Obviously, you can upgrade HTLCs, but it's a lot simpler not to.

Speaker 1: Yeah.

Speaker 0: Yeah, great. So, I think in the end, it's just gonna end up being adding more TLVs to these splice messages to just explain what we want to negotiate on top of just creating a new transaction. I think it should be simple enough, but it's going to be to talk about it and to retell it once we have a standard basis for the PR after dual funding is merged.

Speaker 2: Cool, and the TLVs are mainly for re-establishers, right? So basically, you remember what happened on reconnection type of a thing? For splicing, I guess?

Speaker 0: I mean also in splicing it, but for dynamic commitment upgrades, I guess.

Speaker 2: Ah, yes.

Speaker 0: Like saying: Oh, by the way, I want to do that and that and update those fields and those fields. Something like that.

Speaker 2: Yeah, exactly. And it does look similar, or there's a bunch of stuff in channel established now to basically let you pick up.  But that's the thing — we need to sort of merge, if possible.

Speaker 0: Oh yeah, I see what you mean. You mean it could be either directly when you reconnect, but if you don't, you don't actually have to reconnect — you could do it while staying connected, so the same TLVs that will be added to channel re-establish will also be added to splicing it, I guess.

Speaker 2: Oh, that's right. There's a splicing message. Yeah, I'm still a little behind on that stuff, but I did a pretty good core type work step, so now I can start to catch up with the rest of the world.

Speaker 5: Alright. So, I guess that's it for dual funding, pricing, and all those related stuff. So there's that PR by [redacted] about clarifying optional and mandatory feature bits. I think it's now small enough and good enough.I can merge. You can have a look at it. It's only four lines, I guess, now.

Speaker 3: Yeah, I didn't change something that we all already did, right? So we should, It's just a clarification in the spec.

Speaker 2: Yeah. I know you had a question around the wording, [redacted]. Did that ever get resolved in line, if you're on?

Speaker 4: Yeah, I believe I went over it out of band. Sorry, I did not put it back on the review.

Speaker 2: No problem. Okay, cool. Should we land that here, if people like it?

Speaker 3: I think maybe we are here. We can discuss the wording. The suggestion was to change from must, not set all the film mandatory, optional and mandatory to shoot. But I don't see the point.

Speaker 2: Is the rationale that it doesn't say what you should do if they said it or…? Because must, I think they're saying that must should be. Must is: You're gonna bail out. While should is: They shouldn't do it, but also you shouldn't care. Or I think that was like describing…

Speaker 1: …dumb shit is pretty obvious. I don't know. I mean, I'm happy with a must like don't do this, and what are you doing? Like, seriously? It's weird. We never specified it. Like, it was said to do this or do this. We never said you could do that. If people do it, I'm not sure how people respond, but I know I find it hard to care about these cases. It's like: Well, if someone says both options, then they're just confused. If you go to weird stuff — I know it's not a bad thing to specify — don't set both. Just don't. We haven't defined that. You don't know what people will do. Don't do it. I mean, most implementations will go test: Do I have mandatory? Is this required? Yes, and they'll behave appropriately. I think our code, we don't explicitly reject you if you set both, but we will treat it as mandatory. We basically go: We understand it, we go, is either one set, we don't care. I think everyone will actually behave how this behaves.

Speaker 3: Yeah, I think we'll do that. I just would tell him that that's his thing. He takes the mandatory one. I guess LDK: Reject if we specify the optional one. No, LDK, do the same thing, I guess.

Speaker 2: The only time we reject is if you have a requirement that we don't know about at all, so there's no constant or whatever, right? And that's just kind: I don't know what you're gonna do; I don't know what you want. I'm gonna bail out, which makes sense. There's one related thing that I ran into — basically, last mile taproot stuff, in terms of on-chain stuff — I think this came up a few times around the implicit versus explicit negotiations. So, it's the implicit being when we say a BLAS negotiated for a channel type. For example, if we have anchor bit open, we'll open that by default right now. The explicit meaning actually specifying the channel type feature bit in open channel. But what I realized, which is something that isn't new in the process, is that post taproot — I don't really think you can always use the implicit negotiation. For example, right now, we have a test case, where both sides have the taproot feature bit set, but we actually want to open an anchor type. So, I guess it's more so about how people handle that default behavior because, at least right now, in the LND code, you can't open it for a publish channel. Let's say you both have the feature bit set and you need to open channel CLI with no arguments. It'll try to open a taproot channel, but then fail because it has to be a private channel only. But then, at that point, the only way you can override that behavior, which would be for people just to start saying: I want an anchor feature bit. So, I added the implicit negotiation for an I-test. I think I'm going to remove it generally, meaning then anchors will be the default. But just stating that once we have multiple channel types, it's no longer really clear what the default is or what the implicit is. So, at a certain point, it may make sense for us to flip the channel type bit to required and say everything must be implicit from now on. Because otherwise the negotiated is somewhat ambiguous at times, particularly what you want versus what they intend.

Speaker 1: Yeah, no, absolutely. The whole implicit was kind of a backwards compatibility hack for older nodes, and at this point, we shouldn't be adding to that. We should just be going: No, no, no. These days, say what you want, right? Because it's so much nicer to go: Yeah, here's the channel type I want, and it's really explicit. So, I would suggest, yeah, you're right, we don't expand the implicit logic, but that kind of gets abandoned slowly, and maxes out at anchor. From now on, everyone should just be saying exactly what channel type and eventually. you're right we make it mandatory and that logic goes away. Everyone's happy and unicorns are dancing.

Speaker 5: LDK is already making it half mandatory if we calculate the implicit based on the feature bits. But then, if the implicit that we calculate is anything aside from only static remote key, we just failed to open the channel. We say: What are you doing? You should have negotiated a…

Speaker 2: An actual explicit one? Yeah, we have something similar. We had a bug we fixed there too. But we have a thing too, where we try to assert if it should have been explicit. Maybe it's about avoiding the whole downgrade type of a thing — basically, going to static key. But I guess we can maybe remove whatever we call it, non-static key. Remove that one, non-to-explicit. There's a bunch of names for it.

Speaker 1: Yeah, so that PR that says we should assume these things and make these other ones compulsory and whatever else, I think we decided last meeting we'll do a mid-step, where we basically just turn all these things on as compulsory, and I think static remote key was definitely one of them right, so I don't think anchors was yet. We're about to have a release, but then next release I'm planning on turning those on and see what happens.

Speaker 2: So, cool. Yeah, we can do that for 18. We're also on the cusp of getting to release as well.

Speaker 1: That'd be cool.

Speaker 2: Not yet in the RC phase, but hopefully this week, finger crossed. Cool. Okay. Next thing.

Speaker 0: Mutual close.

Speaker 2: Oh, so should we merge 1095?

Speaker 0: Yep, go for it.

Speaker 2: Okay. Alright, I just merged it. Okay, close.

Speaker 5: Yes, I think the main discussion that maybe got out of hand a bit is what to do with a case that just never happens where we both don't have an output. So, do we just say: You always have an output for the one who has the most, the biggest amount in the channel? And if both have exactly the same amount, it has to be sorted by pubkey or something like that?

Speaker 1: Pubkey. Sure. Whatever is easiest to implement.

Speaker 2: So, the idea here is that, we're just saying that the possibility of both of us not having output just can't exist anymore, right? So now, how is this different from what we have today? It's more like if we have the desk trimming, then it seems like it's the same.

Speaker 1: Yeah. Basically, I think the closer today has to have an output. The other side can abandon their output. I think that's how it works today, except there's a dust rule as well. Yeah, you can't both drop your outputs at the moment anyway.

Speaker 0: But since there's no way to place out yet and everyone has a limit on the minimum size of a channel. We just, in practice, cannot be in that scenario. We should make sure that it is covered and we avoid getting into that state by having the specification say: Okay, it doesn't always gonna be at least one output.

Speaker 1: Yeah.

Speaker 0:  Apart from that, the only functional change is that if you send multiple shutdown, you can update the script you are shutting down to, except if you're using a front shutdown script, which is something that people will have to implement. That's probably not implemented today. But apart from that, at least on my side, everything looks good until we start implementing it.

Speaker 2: Yeah, so that was on my list — to take a look at a sort of independent kind of POC implementation of it, just to see how things line up. The one thing I need to get back into the type of PR still is that now it does flag everything as RBF. So, the idea is that: Okay, well, you already flagged — everything's already RBF. Then, in the future, if that feature is there, you can just use that new protocol, and then eventually, we can make that mandatory. So, I think it should line up pretty well there. Yeah, I need to do another pass generally, and then start to sign up an actual implementation.

Speaker 1: Cool. There's, I think, one thing that needs to be tweaked and that is that we do need the dust limit, unfortunately, in there. If your thing is definitively dust, according to relay rules, you cannot propose that output, because otherwise, you will end up saying it can't relay on the other side. So, I think that's the only — we do have to have the dust rules in there. We could either. We could simplify them, and say: It always has to be 524, whatever. Or we could do the proper ones, which is 330 for witness and 524 for whatever else. But yeah, that was one addition I realized because otherwise, you will end up with something you can't relay. So, we do have to code that in. I don't care about the case…

Speaker 2: Do we make the dust limit explicit or just…?

Speaker 1: Yeah, you can include your output if it's below dust limit. Otherwise, I can end up with a transaction that doesn't relay, and that's not supposed to happen.

Speaker 0: Also, regarding the dust limit more generally — now that we have anchors with zero fee HTLC transaction, which means that we don't have the trimming threshold that adds to — I mean, without the European core — it's the dust limit plus the fee you're paying for the HTLC transaction that decides whether or not you include the output in the commitment transaction. With Uncar output 0 fees, that's not the case. It's only the static dust limit, which means your commitment transaction becomes bigger much quicker than before Uncar output 0 fees. So, I was thinking of raising potentially the dust limit on nodes once we all support encode with zero fee. For example, set it to 2000 sats because anything below 2000 sats, you probably don't want to have an unchained output for it. What do you guys think about that?

Speaker 2: You can't adjust it after the fact though, right? You're talking about like the open channel limit, but dynamic limits would let...

Speaker 0: Yeah, I mean, in a world where we can dynamically update those things: Do you conceptually agree that it potentially would make sense to update that limit to something higher to avoid having a commitment transaction that's full of outputs that are 1000 sats, for example?

Speaker 2: I think so, right? In terms of looking at the chain fee level and updating it accordingly. There's that whole thread that we discussed a few weeks back around not always going to chain or going to chain and giving up. Generally, there should be another toolkit there. I definitely want to be able to update the summit stuff because I mean, that was what we're going to do right

Speaker 0: Okay. I think that means we really need to keep sections about checking thresholds with a dust limit in many cases, such as, for example, this mutual close because if at some point we start having a just limit threshold of 5000 sats on both sides of the channel, we still need to make sure that outputs are not below that in the mutual close as well.

Speaker 1: If you really want to do it dynamically —  I mean, sending multiple signatures is like doing it on a per HTLC basis is possible, but then you really need the ability to reject HTLCs and go: No, no, I don't like that. I don't consider that to be dust. If you want that, we're going to have to put that on-chain and things like that. Or vice versa, right? But that's a whole other can of worms. So yeah, increasing a static dust limit is probably easier.

Speaker 0: Right. Or maybe once we have something like simplified commitments, every time you yield your turn or something like that, you announce your dust commit for the next turn. We can think of potentially many things once we start having simplified commitments or something different than what we have today.

Speaker 1: Yeah, well simplified commitments opens the door to failing things and so you can propose the HTLC and say: I want this to be dust; and I'll go: No, no, that's not, I'm going to reject it because that has to be on chain. And you can go: Okay, well, I'm not prepared to do that. And we can just go our separate ways, right?

Speaker 0: Yeah, even though it's still better if we negotiate it up front so that we avoid going back and forth and failing things that we actually want to relay.

Speaker 1: Yeah.

Speaker 0: I see what you mean.

Speaker 1: Yeah, you end up with a combinatorial explosion if you allow both possibilities of each one, though. We have to think about that, but it would be kind of cool. I just — fuck, I hate fees.

Speaker 2: No, yeah, fees are an annoying part about Bitcoin, right? Like, we could be doing fancy stuff. Cool. Next one is a clean-up thing. I think we talked about that this is going required first. I'm not sure it's updated yet.

Speaker 0: Yeah, there are still a lot of needs on the PR, but apart from that and starting by just keeping implementations where everything is required — it's looking good to me.

Speaker 2: Do we need to try to coordinate on that? I guess it's okay, right? Because it's not like we're adding a new thing that'll be required. We already have pretty good feature build overlap today, and then that's what would just be required. I guess this is also the set of things that we know. Everyone has already done it, so it shouldn't be an issue.

Speaker 0: I think on the contrary, if we want to see things break, we definitely should not coordinate and should release on their own and see if things break. If you don't, hopefully.

Speaker 2: I'll see you on testnet. No, I'm not going to.

Speaker 0: No, those features are features that we have all shipped for such a long time ago that only the people with whom it will break are people who are already potentially kind of out of the network.

Speaker 2: Yeah, it's actually several years old. Cool. I just added required for seeing that. One of the path stuff, but like, oh yeah, I guess it's saying go from 32 to SCID. I guess, is this tangible? I'm guessing this makes the stuff easier to scan. I don't know if there are any benefit of the key versus the SCID. I guess the key decouples from SCID alias. You don't have to care about that. Maybe that's one thing, but I'm not sure if that bothers in terms of hoppins or something like that.

Speaker 0: The kernel ID is a long-term identifier, whereas short-channel IDs are potentially things that come and go as you close channels. At this point — the introduction point — because for intermediate nodes, we are already using those short-channel IDs inside the payment union to relay so we would have the same issue and it's just used to identify your peer. But for the introduction node maybe it's a bit more painful but yeah.

Speaker 1: Yeah it basically depends on the expiry of the offer, right?

Speaker 5: Right? It's equally painful. But if you're talking about offers, the vast majority of payments in general tend to be these shorter term things that people post that might be a side effect of both love and sucking and requiring that, but that will still be enough material number of payments, and for those this may be particularly useful because you can have a much smaller QR code. But, I mean it is the case that if you want to build a very long term offer, you probably wouldn't use this. Still, this is just an option, right? You can go still.

Speaker 2: So, okay. So, it's not mandatory. It's just like adding a TLV to let you do the other works.

Speaker 0: Yeah. Basically, the implementation could decide when you generate an offer. With a long expiration, we would just wait for you and we've another ID; and if you have a short expiration, we would use a SCID.

Speaker 5: Potentially, yeah.

Speaker 6: For the encrypted data hops, they already have a short channel ID TLV in there. So, there wasn't nothing really added. It was just a change that you could actually set it. And then for the instruction node, you would write a type essentially that allows either.

Speaker 1: So, the hack where we do both is — I don't know. It has some appeal. So, 02, 03 is a pubkey. O0, 01 is a short channel ID. It always bugged me that we had that extra byte. So, we could abuse it that way as proposed. Now it would actually apply in a few different places. I mean, I only proposed that 24 hours ago, so I don't know if people have really absorbed that.

Speaker 6: The changes in the PR, so if you want to look at it — sorry, I like it.

Speaker 1: Okay, cool. It's weird because it's a new fundamental type because you've got to parse it. It's non-trivial to pull it out, but sure.

Speaker 0: It's interesting because it's extensible. That means it's going to be another idea that the binary is either 0 or 1 plus short channel ID, or 2 or 3 plus a 32 byte pubkey, or 4 or 5 plus something else in the future. So, it's interesting.

Speaker 1: Yeah. Adding another extension point feels like a hack, but I don't know. There are a number of places where it's like short channel ID or pubkey.

Speaker 5: Does anyone use open SSL to read pubkeys? Those are already defined.

Speaker 1: Oh God, I hope not.

Speaker 5: They are. No, no, there's a definition for like, one, two, three, four, and five or something.

Speaker 2: Oh, yeah, there are prefixes. Yeah, and there's a hybrid also.

Speaker 5: Yeah, they're really bad. Don't use them. But they exist. They're defined. Yep.

Speaker 2: Is that a PR, [redacted]?

Speaker 7: No, I'm working on a blinded payment path construction for LDK. Basically how our API works is, it takes a list of the unblinded payloads that are going to go in the blinded path, and so those payloads can contain stuff like payment relay, fee parameters, and payment constraints. Then from those payloads, I construct the blinded pay info that's going to go in the offer. But the only field that I can't really construct from that is the HTLC maximum msat because that's not included in the blinded payment TLVs for the blinded path. So, I'm just wondering if we plan to add that or if I should— how are people setting this? I don't know, [redacted], does that make sense?

Speaker 0: On top of my head, no. I really, that's something where I really need to dive deep into the code actually to make sure. Can you just put that in writing somewhere, so that we can look at it calmly tomorrow?

Speaker 2: Yeah, I wrote down in the summary. But what I'm picking up is that the HTLC max value isn't in the blinded path TLV payload, but it's something that you need to know to construct a route to know if you can send a payment or do shorting basically, right?

Speaker 7: Yeah, to construct the offer. Because it's a field in the offer, but it's not a field in the original blended path payloads. Okay, cool. I will leave a comment somewhere or maybe propose something in PR.

Speaker 0: Yeah, we need to look at the code again to make sure it makes sense.

Speaker 2: Cool. Okay. Quiescence. I think this just bumped because we were looking at how this relates to splicing and stuff like that. So, just trying to refresh it in our minds.

Speaker 0: Yeah, I don't think there's anything new. I think we finished implementing a quiescence and master stuff — like one that we haven't tested cross compatibility with CLN yet. We're finalizing the last bits of splicing before we do those compatibility tests. I don't think there's anything new in the PR at least.

Speaker 1: The only interesting thing is that the feature bit changed. So. we kind of decided, [redacted] pinged me after we released RC1 with a really good idea that we shouldn't use the final feature bit until it's spec final. So, we've added a 100. So, instead of 63, we're using 163 just as a rough convention to go. That way, if nothing changes and we spec final it and it gets a real feature bit, you can just advertise both in transition. But if something changes, you don't end up with someone shipping the final one, and they're getting these weird interop errors, because: Oh, no, we're running our experimental version, whatever. So, it's kind of a cute convention just to add 100 for things that are in progress, especially if you're deploying them. To add 100, so that we've got this, you're not going to break people who implement the final one: I wonder why the fuck nothing works. So, we've just temporarily flipped to bit 163. If people turn that on for a current release, and I think there's probably a good convention for anything like this, where the spec is not completely final, that just add 100. Because we had this problem with dual funding where we broke it multiple times. Then, if someone implemented final dual funding, they would get really confused because it would try to negotiate with old nodes.

Speaker 2: Yeah. That makes sense. Like staging.

Speaker 0: We have a lot of bugs on our node. When we started activating the opening feature bit and having a lot of old CLN node connecting and saying that another feature bit was required, whereas it was not, and we would break the connection with a lot of old CLN nodes.

Speaker 1: Yeah. Yes, so this should..

Speaker 0: I don't think it's a rule in the Bolt to always add 100, but just a general implementation rule that when you start activating something experimentally in the network, don't use the final feature bit. You don't need to add anything to the bolt to mention that.

Speaker 1: There's a contributing document that we should probably — It says how to write the bolts rather than the bolts themselves, and that probably should go in there. 100 is a good number. 100 plus is our free range of experimentals, and it's pretty easy to go look at 163 and know what that means. It's a cute trick, so we should probably do that. It also means don't grab experimental features that happen to be a hundred plus an existing experimental feature. Cool.

Speaker 2: Splicing. I think we kind of talked about it earlier as far as breaking stuff. Getting better. You're breaking stuff better.

Speaker 0: Slowly moving along. Nothing major to report. We want one thing — we discussed today with [redacted] — it's not clear in the spec, but if you have a pending splice that's not confirmed: Do you allow another splice to be added as a child or do you force the other peer to RBF the pending splice if they want to make more contributions? I think it would make sense to always force RBFing when splices are unconfirmed because it's more efficient, but the spec doesn't say anything about it, and I don't know if the implementation does anything about that.

Speaker 1: Yeah, no, because when one of the splices is confirmed, you assume it cancels all the others. So, it's kind of implied they're at the same level. So, they're all competing against each other. Otherwise, you have to start introducing dependency trees and stuff and that's just messy.

Speaker 2: Yeah, it's more challenging.

Speaker 0: If you have a binning splice that's not confirmed and they send you splicing it, what are you gonna respond? Tx abort?

Speaker 1: I would have to check the code, but you can have multiple inputs. You can propose multiple, I believe.

Speaker 0: But it should use TX init RBF then, right? Because it's an RBF of the first one, it's more explicit to say TX init RBF instead of placing it again, right? Because for example, for zero-conf, then you don't really have a choice. And for zero-conf, you potentially must, yeah, you actually must chain those either instead of RBFing them. So, that's why there's a distinction between a new splice init on top of an unconfirmed splice or TX init RBF for the splice. But for non-zero conf, I think we should always RBF.

Speaker 1: Yes, I think so. But I may not have to check with [redacted] as to what their interpretation is.

Speaker 2: Cool. Taproot. So, I said I was going to have the spec thing draft by the next time. That happened, fortunately. But I have gained a lot more wisdom on on-chain stuff, generally. So, I think a big thing I want to do is expand the on-chain section, which is HTLCs, breaches, et cetera. The main thing that I was fixing in the past was just the additional data that needs to be stored or just regenerated. So, for everything, you have the control box, but then for all the replication paths, you also need to store the top tweaks of the second and first level for HTLCs. That's because they can breed, and then you have to basically use the top two to do the keyspend or they can go to the second level as well. And that was one thing that I hadn't stored, but then some itests basically showed just certain bugs there. So I've been on the on-chain stuff, I guess, for the past month or so. I think I finally concluded it last night as far as getting all the itests working. This is the only thing that, I think, I had to do for, but I didn't follow up on just as far as storing that extra information. I think, technically, for the second level of HTLCs, because it uses the same key — this is just the sweep after delay — I think you can just either regenerate it or only store one of them. But right now, I store one for every single HTLC. Now, all the HTLCs have these two levels alongside of it — or sorry, these values, rather. But other than that, I think our implementation is more or less complete now in terms of all the on-chain stuff, all the breach stuff, some things with co-op close, re-establish, all that stuff. So now, I'm going to start to work to get that wisdom back into the spec, and then ideally also add some basic test vectors around transaction construction, things like that as well.

Speaker 8: Awesome. So, one other thing that we were talking about last week, of course, was the fact that without the nonsense, FROST would be significantly simpler. I wanted to follow up on that. One of the things that some of the cryptographers are saying is that the big issue with FROST nested inside MuSIG2 is that there still isn't a security proof. However, that isn't really the biggest blocker because significantly higher difficulty is going to be having some sort of threshold agreement for channel revocation because the revocation disclosure and the private disclosure that's significantly more complicated.

Speaker 5: I'm confused by that. We already solved that. So, we just have 10 revocation routes and we XOR them together. That's already solved. I'm not sure why we can't solve.

Speaker 2: For some definition of solved.

Speaker 5 Well, I mean, that's the obvious solution. No one has anything better, and that certainly works very well. Obviously works.

Speaker 8: Were the 10 round trips, [redacted]? Sorry, is that what they said to you?

Speaker 5: No, there's no 10 round trips. You just have 10 of the revocation hash tree things.

Speaker 2: I think [redacted] means in the wild if you actually had 10 signers, but I guess you would have some decomposition amongst the signers who has what value or something like that?

Speaker 5: Ohh, you wouldn't need 10 individual round trips. You would need 10 round trips, but they all run in parallel. Or however many signers you have, of course.

Speaker 1: Yeah, someone should actually write down the calculations showing the different simple combinations of how you break up the 10 into your 2 or 3 case, your whatever else. I mean, there's a number of ways of doing it. Some of them are obvious, some of them are not. I would like to see that.

Speaker 8: I thought it was your proposal at the summit, unless I'm confusing it with the APA.

Speaker 1: No, no, it was mine. I hated it, but [redacted] improved it, and now I'm liking it more. It's dumb, and sometimes dumb things nobody can fuck this up. Well, okay, so sorry. Of course, they can.

Speaker 8: Okay, cool.

Speaker 1: But the question was the number, and I think [redacted] had some evidence that like to do three of five I think we need ten or something.

Speaker 5: Three of five and four of five — I think both need ten. And then, if you want five of six or six of seven or anything like that, you need like 30 or so, you need like way more, and suddenly it's kind of, yeah.

Speaker 1: Yeah, fuck those people. Okay.

Speaker 4: What is, this is separate from the issue where you were saying that say a two of three consensus is not really achievable, but a three of four is, or was that for..?

Speaker 5: That is separate and that is still true.

Speaker 2: But were you gonna get into something around the FROST MuSIG2 thing or something, or around the proof?

Speaker 8: Yeah, I was going to say that — up until two minutes ago, my thinking was that with the bigger complication still being their vocation, which I guess isn't the case. At least, I want to see a write-up, which I'll do tomorrow with [redacted]. I was thinking that it doesn't really make sense to not do nonces because we have this more difficult barrier anyway. So, I was going to advocate that we proceed on course.

Speaker 5: So, I just pasted it on IRC. I guess I'll copy it on matrix and put it separate. But that's if you have 10 non-shares, and you have five things, and you split up the non-shares as indicated, then that gets you three of five.

Speaker 8: Wait, that's nonces. I'm talking about revocation.

Speaker 5: Sorry, revocation, that's what I meant.

Speaker 8: Okay.

Speaker 5: If you have 10 revocation shares and you split them up as follows, and then you XOR the result together, you get three of five out of that.

Speaker 2: Cool. I think one interesting thing around... Oh, go ahead.

Speaker 5: I was going to say that we did neg this. So, last week, we'd kind of gotten not very far in the discussion, and then somebody said: Hey, what about — have we asked the VLS folks? We did go ask the VLS folks. Sadly, I don't know if [redacted]’s here, but [redacted] said this morning that they were having some technical issues and travel issues, so wasn't gonna be able to make it this week, but they did paste — well, I can leave it to you, [redacted]. But they did post on the spec meeting thing, saying basically, the explicit script pack thing would be much simpler.

Speaker 1: Right. What he said.

Speaker 8: He also said it would probably be computationally cheaper on some low-powered devices. I think it's still comparatively negligible because at the end of the day…

Speaker 2: You still have number one, the difference in on-chain costs, which is more than double a witness size. And the other thing, this is simpler, but have they done the FROST stuff in the VLS setting as well? That's the main motivating factor we've been going in that direction. Should someone get that far before we double the force close cost for everybody to make potentially small use case in terms of no reviews are actually possible?

Speaker 9: I think we should defer to [redacted] for the details there, but I don't think we're adamant about it. It's just that it seems simpler is what they’re saying.

Speaker 2: Yeah, probably so. I spent most of my time on the on-chain stuff, and maybe this is my recency bias of this is the last thing I worked on compared to this is the earlier thing. But, at least, our code base, which is updating assumptions of: Okay, you need a control block. You need a tab tweak. This thing is slightly different. Are you doing a key spend or a key — that was kind of dominating a lot of our review cycle, but granted that I did do the non-stuff a lot earlier on the process. This was kind of like: Okay, like get into that stuff. But that's just like at least one data point at least where I happen to spend a significant time, but you know, somewhat skewed.

Speaker 8: Yeah, we haven't really had any issues with the fronts, but with the nonces after we got over the initial hurdle of figuring out their nomenclature. If I dare say so, because it sounds like maybe we still haven't really gotten over it.

Speaker 2: Yeah, I think everyone has names that work for them.

Speaker 8: I still advocate for ‘You can delete.’

Speaker 2: You can delete.

Speaker 5: Yeah, I mean, I remain not sure where to go with this. The FROST stuff seems doable enough. There is an implementation somewhere, right? It's not just a theory thing, not in the Lightning context, but there is outside of Lightning.

Speaker 2: I think there are a few, I know like [redacted] has been working on stuff. They have some hard hardware wallet thingy. I think they're out there. I'm not sure if they're used ‘seriously’ yet, beyond like a demo or something like that.

Speaker 5: So that doesn't seem that far away, and it seems worth considering that. I mean we do have to take a kind of holistic decision here: Do we want Taproot to look like multisig for all counterparties? Or do we want Taproot to look different for a multisig counterparty versus not? I mean, at least, as the crypto exists right now, I would guess that means it has to be two of two multi-sig and it has to be this — let's call it 10 revocation secrets XORed together. So, I mean we have to decide. I think that's the decision. I think the decision is: Always looks like multisig or doesn't always look like multisig and has a separate feature bit for multi-sig.

Speaker 8: [redacted], can you explain what your hesitation is? You said the crypto right now looks that you know there should be an explicit do of two multi-sig. That's not really the message that I've gotten from [redacted], but maybe I'm mixing it up.

Speaker 5: I mean, there's no proof. From what I've heard, there's not a lot of confidence in how to prove. It's not like there's no like approach for how to prove nested MuSIG or FROSTed MuSIG yet. So, I don't think we can make any kind of assumptions based on that yet.

Speaker 2: Yeah, I think the interesting thing with that — or I kind of like our proof or not — is that it is possible technically, right? So, I think there's another question of…

Speaker 5: If it's actually implemented and it works.

Speaker 2: Yeah, but if it's possible — meaning that you can't even verify someone's doing it or not — there turned out to be an issue with the proof down the line, doesn't that mess up the whole scheme, if you know what I mean? Or wouldn't issue in the nested instance mean that in the non-nested instance, given that you can't distinguish the two, if you don't have anything from the other party would that modify the security? It seems like a weird sort of circular thing where it's like: You can do it, but we don't have a proof. But if let's say they can't write a proof or the proof show something, there's an issue there. Doesn't that invalidate part of the actual greater scheme? Just a way to think about it, and I think that's where I'm wrangling with. Generally, it's okay, you can do it. You can't stop me from doing it, but the fact that they can do it modify your security and all if the answer is no, that…

Speaker 8: It doesn't really seem to be the case because you know you're describing it from a third-party observer, but you know the participants know more. One of the critical assumptions that you also don't think private key material to the participants, and so if there's something where nonce nesting would reveal something to your other participants that not nesting it wouldn't, I think that that might potentially expose you to vulnerabilities, where you, at the very least, would lose the threshold signature property even though externally it still looks perfectly sound.

Speaker 5: Yeah, it seems to me like that would just imply that you can steal your counterparty's money, but not the other way around. Otherwise, presumably, MuSIG2 itself would be not sound in some very material way.

Speaker 2: I think that's where I'm getting at, right? That like — I send you a key, but that could be a nested instance.

Speaker 5: Right. I guess my point is we have to assume that no one serious will implement FROST nested inside of the MuSIG2, or even MuSIG nested in MuSIG, until there's at least some level of confidence that this is something that's secure. And so given that that is of unknown and potentially infinite timeline — again, if we want to have multi-sig, we're going to have two of two in the script path, plus this 10 revocation secrets thing. Given that, do we just want to do that, or do we want to have a separate feature bit for that?

Speaker 2: I'm in the separate feature bit camp just because it feels like it's a theoretically important use case, but one that people just really don't seem to be ready to deploy anytime soon. On top of that, the burden of having to support that on the normal scheme and the burden there being double the witness size and the 10 nonce thing. However, you may size that up. It's just the sort of thing you're carrying around as baggage to support a case that, maybe, won't necessarily be super widespread. I think there still is some value of uniformity there in terms of handling yourself, but then also just other cases, at least in the early days when it's only on advertised channels.

Speaker 8: Then, you're leaking though that you're likely trying to do a multi-sig setup.

Speaker 2: Yeah, I don't know. In theory, I can deduce that, maybe just from your latency or something. I don't know. Right? But the thing is, the whole point of this initially was not leaking it, right? Okay, well I could be five nodes and you don't really know, right?

Speaker 8: Yeah, and of course with the unilateral close, you're still leaking the fact that it was one.

Speaker 5: I think the other question on the VLS side: Is there any ignoring the multi-sig case? And I guess it would be nice if they ran away here, ignoring the multi-sig case, is there any strong desire to avoid the nonce stuff just because of the storage requirement? Or I guess it's you already have all the storage requirements and lightning, so it doesn't matter.

Speaker 2: And the other thing as well — as I mentioned earlier, you have more storage requirements. You basically need to store the control blocks, unless you recreate them and also the tap tweaks, which is the root hash you know the replication path. So, even without the nonce, which you know we're saying maybe you can avoid that with a deterministic approach. You still do have extra requirements in order to spend unless you recompute everything from scratch, and then, either way, you need that additional stuff. Maybe there already are. I don't know.

Speaker 9: I don't think it changes our storage requirements massively. So significantly. Massively, so significantly.

Speaker 5: Any opinions from [redacted] or [redacted]?

Speaker 1: No, I'm staying out for brighter people to decide what we should do, and then I'm going to follow.

Speaker 8: Same.

Speaker 1: Alright. [redacted] likes nonsense. I like nonsense.

Speaker 8: No nonsense nonsense.

Speaker 5: Alright, I mean, this seems fine to me. I think it does mean that we're going to end up with a taproot-multisig-feature flag that will have different on-chain format and different everything, and presumably that means everyone needs to support both because people are going to want to run it.

Speaker 8: I think we have a bit of incomplete information right now, [redacted]. And based on the majority of — I mean, I really agree with [redacted] reasoning here. The majority of the use case with the lack of Frost implementations seems like the best thing for the ecosystem at the moment is probably just to go with the process.

Speaker 5: People will eventually support FROST obviously. Like FROST is a straightforward-ish thing to build, and people will use that for lightning nodes. I think that's clear.

Speaker 8: People eventually will also support L2.

Speaker 5: Well, I mean, that has a much more indeterminate timeline in terms of softworks. But the point being you're like: Everyone will have to support both. Because some people will want to run very large multi-sig nodes. There'll be some big nodes on the network that are multi-sig, and everyone's going to need to implement both the nonce version and the non-nonce version in order to have broad compatibility.

Speaker 1: No, what we do is we use LND as a forcing function. If you want to talk to LND, you've got to write a nested MuSIG proof.

Speaker 2: If you do that, you'll get a job from one of us. Oh yeah, we'd be happy to pay for that. One question related to something [redacted] brought up around the plus 100 as a convention for like pending stuff, right? So, for example, ideally by this week, we'll have merged something in, and that something will be available with a build tag or a flag or whatever else. It feels like it makes sense that we should advertise the plus 100 feature bit for this. I don't know exactly what bit we have in the spec, but that just seems to be the thing to do going forward now, and we can do that pretty easily on our end.

Speaker 5: Yep.

Speaker 2: Cool. Okay, we'll do that. Because we have something but you know, will it be the final thing? We need to interrupt to know exactly. Cool. I'll write that up.

Speaker 5: Okay, Just to be clear, all of y'all will implement the non-nonce version eventually when people have demand for it?

Speaker 2: Yeah. Whenever it's written out, whatever.

Speaker 5: Which might be three years. I don't know.

Speaker 2: Yeah, right. And then, that'll just be the other channel type or whatever. Then, at least with that, the latter half stays the same, assuming everything else.

Speaker 5: Cool.

Speaker 8: What's next — CLTVX Fiery?

Speaker 2: Yeah, I don't think there's any updates on Gossip yet. I need to sync up with [redacted] on that and she's not here yet either. So check that.

Speaker 1: Yeah. Oh, so on the Gossip 2.0, like the extension that I promised [redacted], I have a trick for short channel IDs. So, the thing is that if you stop proving your UTXOs, you lose globally unique short channel IDs, but there's a trick where you can use the numbers beyond the block limit. If you've got say, rounded up 4k transactions in a block, then you can use a short channel ID. So you see you prove this UTXO, and then you use UTXO plus, as if it's transaction plus 4K, or 8K, or 16K, whatever, you end up with about 10 bits worth. Those are basically shadow SCIDs. So, if you ever see one of those, it doesn't come with a proof, but you know where to find the proof, right? You're basically saying it's linked to this other one, right? So you can figure out what the master short channel ID is; go find that channel and check that that's valid and everything; and then you can accept the kind of shadow short channel IDs. That gives you a pile of bits. And all you have to remember is how many transactions in each block, or actually how many bits worth of transactions in each block.

Speaker 5: Can you — I mean, the annoying part is many nodes don't have the full block data, so you don't know how many transactions were in the block. Can we just hard code that?

Speaker 1: You can guess. The thing is…

Speaker 0: It sounds like we're about to create ordinals. It sounds like [redacted] wants lightning ordinals.

Speaker 1: Short channel IDs are ordinals, right?

Speaker 2: Yeah, they are.

Speaker 1: I actually originally thought of doing an ordinals-like thing, but it's too much tracking and no one has time for that shit.

Speaker 2: Yeah, you need a big-ass index.

Speaker 1: Yeah. But you can intuit it. I mean, in theory, right? One day, handwave, you'd be getting Merkle proofs, and you can't Merkle prove these things because they're off the end of the Merkle. That's why you round up the order of the power of two. So you can't even try to Merkle prove it.

Speaker 5: Just save one bit, right? We currently allow for 16 million transactions in a block. Is this right? No, I must be wrong. Yeah, the TX index. We have three bytes for the TX index. Let's just shave a bit off of it and call it a day.

Speaker 1: Sure. We'll use the top bits first, right?

Speaker 5: Yeah.

Speaker 1: Cool. Two bits, because you may want, depending on what your factor is, right? But yeah, a handful of bits. Yeah, cool. So that was the only new trick.

Speaker 2: Cool. The CLTV thing, we're bumping up towards the end also. I think we know the values everyone has. Everyone seems to have the same value. I think this thing advocated doubling it. We said we don't need to double it, and I think it looks okay.

Speaker 5: It needs to be updated, the PR, to not double it?

Speaker 2: Yep, it's updated to not double it. It has a rebase conflict artifact in it. That's the only thing I see at a glance. Okay. Errors. [redacted] isn't here. I don't think there's much new here. Looks like we have ACINQ. ACINQ has an implementation too, which is cool. I think there's a feature bit conflict as well, which we should make sure is resolved. Yeah, this isn't in the next LND release, so we got time. Dust thing, I think this was finally updated. This is 919.

Speaker 0: Now, we have two acts, and it looks like it was separated from the rest of — It's looking good.

Speaker 2: Yep, okay. So is this ready to get in? I think on our team, [redacted] looked at it last. It’s very old also.

Speaker 0: Okay, I'm looking at it again to see if anything changed, but it looks like it's looking good. Yeah, here's what I remember. Yeah, I'm gonna actually do it.

Speaker 2: Alright, so I'll pass the merge baton to you, [redacted].

Speaker 0: Okay.

Speaker 2: I think we all do this in some form. I think it's good to, for posterity, catalog it somewhere, but...

Speaker 0: How old is that PR? October 4th, 2021.

Speaker 2: Yeah, that's pretty old.

Speaker 0: It's still young.

Speaker 2: Yeah, it needs to ripen.

Speaker 1: It needs to age a little bit, you know.

Speaker 2: Yeah, we can put it back in the barrel.

Speaker 2: Cool. Check. Can already establish this is my very long term homework for [redacted] that I haven't followed through on yet. I'm almost done with my taproot saga, so now I can go back up right here and check this out actually. Cool. I guess anything else in the final round here?

Speaker 1: We did skip over offers, but I did do test vectors for offers, which is always a pain to write because you got to write all the ones that are invalid, and they're really friggin hard to generate. But I did put those up. I also should really do invoice requests and invoices like the same thing. Here's all the valid ones. Here's all the fields. Here's all the invalid ones. So, there probably will be a couple more PRs, but there were no surprises in implementing it. It's just a fairness thing, right?

Speaker 2: Cool, okay. I just heard that, and I posted my stuff too. Cool. Anything else? I think people are going to be at TabConf also. Personally, I have major FOMO. I have a conflict thing unfortunately, so I'm already feeling FOMO. I mean, ‘cause it was dope last year. Okay, cool. Real quick. Someone made a thing around like something about matrix IRC library doesn't work. I thought that was just a thing, right? Like you can just proxy or something like that. I don't know how that works exactly. Oh, they disabled the bridge.

Speaker 5: They disabled the bridge because the matrix people don't have the resources to maintain anything that they've built.

Speaker 2: Is that something that one of us can run or…?

Speaker 5: Yeah, and I probably should set it up at one point when I get around to it. No, the bigger issue is spam and some other crap. As long as no one wants to spam us, we're okay; and we're okay, and it'll be easy. Let's just hope we don't have a spam problem.

Speaker 2: Okay.

Speaker 5: If we get hit with a spam problem, we'll have to figure it out.

Speaker 2: Okay, but no immediate action needed now, I guess. Okay, manual I think.

Speaker 0: I think you've said it enough. That's the right approach.

Speaker 2: Okay, cool. Alright. I guess I'll see y'all on chat and stuff.

Speaker 1: Cool.

Speaker 2: Thanks, y'all. Cheers.

Speaker 1: Thank you.
