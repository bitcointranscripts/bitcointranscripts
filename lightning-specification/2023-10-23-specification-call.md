---
title: Lightning Specification Meeting - Agenda 1115
transcript_by: Gurwinder Sahota via TBTBTC v1.0.0
tags: ['lightning']
date: 2023-10-23
---

Agenda: <https://github.com/lightning/bolts/issues/1115>

Speaker 0: Alright. So, I guess the first item is something that has already been ACKed and is only one clarification. But I had one question on the PR. I was wondering, [redacted], for which feature you actually use that code because neither LND or Eclair handles — we just disconnect on anything mandatory that we haven't set. Where are you actually using that or how are you planning on using it?

Speaker 1: It's possible for pure backup, and it's possible for —  if you're writing simple tools to connect to the network, they may not set the correct bits, but it's up to them to disconnect. It's okay at the moment, I think, because all our requirements are symmetrical, but it's possible in future that we would have requirements that are not. But certainly if your peer sets a bit that you don't understand, you're supposed to disconnect. But if you set a bit and they don't understand it, that's their problem; not yours. I mean, you know, it's kind of like, they can continue talking to you at their own risk, right? So you don't need to disconnect. It's possible in the future that — I'm trying to think of a case where there are some bits that are symmetrical. So you probably shouldn't enforce it. Obviously, if they say something you don't understand, you hang up. If you say something they don't understand, it's kind of on them to do it. But there's no…

Speaker 2: You’re talking about 1109, right? The one defining what off-word negotiating means?

Speaker 1: Yeah, I think so. But basically, the point is that if you say you have to support a feature, you can just assume it, right? You don't have to really check their features anymore. It's just a simplification, really. You can just write code that assumes. If you say you must support this, then you can just write all your code assuming it does. And if they don't, they get to keep both pieces when it breaks. I think that's kind of the...

Speaker 2: So, are we saying that people should change their behavior? Because ours is that: upon connection, we'll disconnect. Is that still okay or…?

Speaker 1: Yeah, the behavior is okay. It's just that you don't have to check there's like at all. So, if you set a compulsory bit, you don't need to check what they set, right? That's like — you can literally just write straight line code, right?  Say, static remote key or something, you can set it as compulsory, and then you can just completely ignore the behavior, right? ‘Cause that's up to them to disconnect if they didn't understand it. So, you don't need to check their behavior in that case. That's kind of the only corner. It's basically, you can, right? But you don't have to, is what it's saying.

Speaker 0: We're just making it a bit more lenient on the sender.

Speaker 1: Yeah, making it clear whose responsibility it is. No, it's nice if you do disconnect, but who cares? Right. You can write code that's very, very simple that way.

Speaker 3: I think this works as long as the sender doesn't have anything at risk or continuing to assume the receiver understands.

Speaker 1: You never do. By definition, you can't. They could be buggy. I mean, you can't rely on anything. So, you can just go: Yeah, no, everyone's got to understand this and just assume they understand it. And if they don't, that's them, not you. I think that was the only change. But also, the words were not defined. That was where it started. We talked about the communication that offered.

Speaker 2: Can we land the PR then?

Speaker 0: Yeah, I think so.

Speaker 1: I think so.

Speaker 2: Alright, I'm going to hit the button.

Speaker 2: Done.

Speaker 0: Okay. The next one was about just actually specifying the 2016 default log time. I know that [redacted], you wanted it to be a one-liner. Not one left it a four-liner or something like that. To be able to have a reference to an extra section in the spec. Do you really mind or should we just ack it and not do that?

Speaker 1: That’s fine.

Speaker 2: Alright. Another merge?

Speaker 0: Sounds good.

Speaker 2: Alright, I'll put it on here as well.

Speaker 0: The simplified mutual close. Does someone else have an implementation or are we the only one?

Speaker 1: You're the only one. I did want to add something ‘cause I wanted to add the ability to say end sequence. I think that was the only thing we're missing.

Speaker 0: Yeah, anti-fee sniping would be useful. I think it's a good opportunity to do all of those.

Speaker 2: Yes. One comment here. More of like a meta. I guess like a contextual one. Something, I think, related to some stuff that we brought up during New York basically. Can we remove the old one here? Because it looks like I've caught up 20 minutes ago. Do we think it's okay to remove the old one? Because I guess everyone's committing imminently to just doing this one. But then, even with that, given that it has a feature bit flag here. Do we want to leave the old one around? Should we just move it to the end or something? Just thinking about what the evolution looks like there.

Speaker 0: We kind of have to remove the old one if we just want everything to be taproot at some point, right? Because this is the only…

Speaker 2: At some point, yeah.

Speaker 0: People that work for taproot, so.

Speaker 2: Yeah, I guess I just mean that it still takes time for this new one to take uptake me because we need to signal a feature bit still. And then we need to implement it.

Speaker 1: Yeah, I'm tempted to give it a bit of a gap. Like, have both in there for a bit, even though it's awkward. And then…

Speaker 2: I'm happy to move it to the end. I don't know.

Speaker 1: Like, mark it deprecated.

Speaker 3: Yeah, I think marking it deprecated is the right answer. Because that's what form is. It's like this is around for legacy interop, but we don't need it going forward. Do not implement this if you're playing to ship stuff soon.

Speaker 1: Yeah. The way I wrote it is that the last commit basically removes it. But that was kind of so that we could discuss it. I'll toss the last commit and change it to something that marks it deprecated and put a few references. Whatever does the minimal damage. So what I'll do is I'll actually still create the commit that removes it to make sure it's pretty clean. But then…

Speaker 2: I'm gonna push that command. Yeah, and then we can just even stash that later to cherry pick. Cool. Alright. So this is on my radar to actually take a proper look at again, given that we've got a bunch of feedback.

Speaker 0: Yeah, because what do you do with LND? Because since in LND you started deploying taproot channels, how do you close them right now?

Speaker 2: So we close them with — basically everything is the same, other than the co-op closed transaction has RBF signaled. And we do a thing where we do a fast close basically, where the responder just says: Initiator, we're doing what you're doing basically. I think the idea was that we would then start to observe the new feature bit of this basically. Then if there's a set switch to that thing,  just start to ignore the old one basically. I think we have at least a pipeline basically to get in towards this one. It'll just be that new client, new client, they signal the feature, and they'll use this new one itself. Then, in theory, if someone has a co-op close present, I mean, we can code up the upgrade path, I don't know if you will, but then if it's unconfirmed, they can upgrade to this one and then do another bump. In terms of just because it'll be RBF at that point. So, but that's like a great path. I don't know if we're going to implement that.

Speaker 1: So, the other thing is if we allow them to set n sequence, we have to check that it's RBFable. So that's the only twist on letting them specify what n sequence is going to be.

Speaker 2: Oh, by RBF, what you mean is like actual signals RBF?

Speaker 1: Yeah, because I want to change it. We have a fixed, I think it's FFFFE as our n sequence. We want to be able — because there's that bit saying basically: You should try to blend in and here's how you should. Really complicated, anyway. All it means for this is that you should, when you close, here's the end sequence I want, right? And we should make sure that is not all ones, right? Not FFFF.

Speaker 2: Yep. So, we actually use that exact same value as well in our thing today. The FFFD basically.

Speaker 1: So yeah, that was the one that the spec currently says anyway, but we might as well give them the ability to set it because there seems to be a thing. So, yeah. I mean, if we're going to all this trouble, let's blend in, and then, implementations can tweak it arbitrarily.

Speaker 2: Okay, cool.

Speaker 0: I don't know. Maybe it's just spec stuff, but from the spec point of view, in the taproot spec, there has to be some dependency on something to specify how you mutual close. I don't know if in the taproot PR you have another definition for how to adapt the current mutual close. Because, at some point, we merge the Taproot PR, it has to have a defined way of doing the mutual close. Should we just say that to depend on that feature bit or something like that, or just depend on that feature?

Speaker 2: Yep. I think that makes sense because what we have deployed right now is the staging bit anyway, right? We can say the final bit assumes this thing. I think that was the idea, but we at least wanted to be able to like, at least just do the RBF today ‘cause we knew we wanted that, and then figure out the rest later. But I think that makes sense.

Speaker 0: Okay. Alright, so I guess next steps for that one is to have more implementation and add BIP 326. Is that it? And just resolve the comments. There are a few comments about typos or closing SIG instead of closing complete in a few places. But apart from that, it's looking good to me. We'll see when we do the post-compat test.

Speaker 2: I guess with this one, fee range doesn't matter much anymore, right? Because I'm just signing an offer, you're signing an offer, right? Or maybe it's useful for bounds. I'm not sure.

Speaker 0: It's not even included in the TLV stream of new messages.

Speaker 2: Okay. Alright. What's next? The spec cleanup thing. So, we have an issue for this one. I think we're trying to get this — basically, do the initial required flip in .18, which is our next major release. Which is probably realistically like January or something like that. We always try to ship during the holidays, and it never happens. So, it'll end up being early next year. But other than that, we have this track change code wise is pretty minimal. It's just a matter of seeing where stuff breaks around.

Speaker 0: Yeah, it's on our master branch as well. I think it will go on our node this week or next week. Something like that.

Speaker 2: Okay. Cool. I guess we'll merge this one once we are all actually start to signal it. Just then release that one and stamp them in the repo.

Speaker 0: Yep. Sounds good.

Speaker 2: Cool. Next one. Offers.

Speaker 1: Nope, nothing here. I've been slack, preparing for our release.

Speaker 4: Our next release, which should be today — I think maybe tomorrow — should have a basic version of offers. Just need a direct connection, but they'll lose me to wrap up for that.

Speaker 0: And does anyone have the SCID or pubkey thing implemented?

Speaker 4: We do not.

Speaker 0: Okay because we have a PR on Eclair that we want to get on our master branch soon, but it would be nice if we could test it against something else.

Speaker 2: Is that the ability to use SCID or pubkey to make the thing smaller?

Speaker 0: Yeah.

Speaker 2: Cool. Next, splicing. I think there's a lot of background movement on this. Just in terms of coalescing what everyone else's implementer thought of.

Speaker 0: I guess one first question would be are you managing that PR [redacted] or is [redacted] managing it? I think last time I checked, the PR already looked good and seems to be what we had both implemented, but just in case there are changes to make.

Speaker 1: Yeah I'm leaving it to [redacted]. We're leaving it experimental this time. I've got, I saw CI get a bad signature recently, so I'm like: Okay, there's still some fun in corner cases with splicing, where we definitely can break things. So it's still gonna be experimental this coming release. So, we're supposed to be code freezing. Well, we're supposed to do a November release, so the clock's kind of ticking now. The code's not quite where I'd want it to be for if we make it official. But yeah, I've been letting [redacted] run with the PR. So I have not looked at it recently.

Speaker 5: Yeah, and I've been just busy trying to get all the restart related nuances going. And once I get that done, then I plan on getting to the spec right after that.

Speaker 0: Yeah, that's probably why you get a few invalid committing errors. When you start implementing all the restart stuff, there are a lot of cases that you need to properly implement. Once you figure out the state machine, everything makes sense, but that's where we found a few bugs where people just disconnect at the wrong time. Or even restart from the wrong backup and it's not properly handled or something like that. It's interesting to implement.

Speaker 2: Cool. This is defined in the TLVs and the reestablish message, right? Which is sort of how you're supposed to, in theory, synchronize.

Speaker 0: Yeah. You just add one TxID in the TLV. When you were in the middle of the signing section, when you disconnected, you just add the TxID of the funding transaction, the splicing transaction you are creating, so that the other side knows that they have to retransmit commit SIG, and potentially Tx signature if they were the first signer.

Speaker 2: Cool.

Speaker 0: By the way, we'd really love it if C-Lightning had the support for the dual funded part of that so we could lend dual funding.

Speaker 2: Is that related to splicing or …?

Speaker 0: It's only the restart part of the channel reestablish. Was that what you were working on, [redacted], for dual funding as well?

Speaker 5: I haven’t done the dual funding part of reestablish. Just the splicing stuff. Is there something for dual funding you're hoping to get done?

Speaker 0: Yeah. This is really — oh, [redacted] is here. This is the missing bit for dual funding cross-compat, and it shares code with splicing. So, I guess this is code that is put potentially in both your branches.

Speaker 2: Is this a case of restarting a dual funded splice or a restarted splice with dual funded channel or …?

Speaker 0: Restarting anything that uses interactive Tx. Whether it is doing funding or splicing transactions. Restarting something where you disconnected in the middle of the signature process, like one side sent commit SIG or maybe commit SIG and Tx SIGs, but didn't receive everything. And when you reconnect, you want to make sure that you finish the signing session.

Speaker 1: [redacted] did promise yesterday they were back in Texas and was going to be working out on some dual funding stuff. So, [redacted] is right now promising that: Yes, it is almost finished and it is working perfectly, and it will happen.

Speaker 6: I think there's like one left to do with the dual funding stuff on reconnect, and I'm working on it this week. So, I don't know where the current release process is, but there is a slim chance we get it in the next release. I'm not gonna make promises though.

Speaker 1: Yeah, you've got six days. Actually, you've got slightly more than that because it's experimental. I mean, I'm not release captain, so you'll have to ask the captain, but nominally, if you have a PR up in the next week, you probably should be good.

Speaker 7: I heard RC1 by Monday, hopefully.

Speaker 1: Yeah, that may be optimistic, but it's good to have goals.

Speaker 0: And if you want cross-compat tests, just ping me when you have a branch, and I can test that branch against Eclair and let you know if everything seems to be working good.

Speaker 2: Cool. Okay. Taproot stuff, if we're moving from dual funding. So last thing on this one — okay, it looks like there's two, or maybe there's a few things I didn't catch up on. Last thing I remember at least was [redacted] talking about the extra nonces for the purpose of splicing basically. And if you are splicing a taproot channel, you need some additional changes there.

Speaker 0: Yeah, that one is actually a question where we'd need feedback from [redacted] on the splicing path because the first proposal I have doesn't need any change to the current TLVs that you're using. We just use the implicit ordering of the splice transactions and order the nonces with that implicit ordering. So TLV just handles that without changing anything. But if we do not want to rely on an implicit ordering of a splice RBF candidates, then we'd need to change to do a breaking change on the TLVs. So that's something I think we should decide soon. But, in my opinion, we should keep relying on the implicit ordering that a splice transaction has to be created after another one just because there's this splice protocol state machine. So you just order the nonces in that exact same order.

Speaker 5: Yeah, and this is to me. I think the current spec does require them to be ordered in fee rate, which is essentially the same as the order in the creation order of the RBFs. So I think being structured is a good idea. The order.

Speaker 2: Cool. And then just curious: What would the explicit ordering look like? That would be numbered nonce basically, or fully enumerate them on the wire kind of thing?

Speaker 0: I think if you want it to be explicit, you would have to do a map funding TxID and nonces. Or splice TxID if you prefer, and nonces.

Speaker 2: I'm just curious what that looks like.

Speaker 0: But I think just relying on keeping the order in which you created the transactions is the easiest.

Speaker 5: Yeah, I like that too.

Speaker 0: Yeah, perfect. Then in that case you don't need to change anything in your current TLV format. It would just work because the length is already encoded.

Speaker 5: Love it. Let's go.

Speaker 2: Cool, okay. I think the other thing, which I think we got some more comments on, was basically the thing around miniscript. Just to double check that the scripts are miniscript itself. I think I asked a question on descriptors. Looking at that. And then, it looks like there are a few areas maybe where one byte was saved. It looks like some of them, I think, are instances where we opted not to use the CSV trick. I probably need to look at it a bit more. I think one byte is not considered compatible.

Speaker 0: Yeah, the rationale about making it miniscript compatible is not really to save one byte, but just to be able to import those policies directly into bitcoind instead of having to explicitly spend the output. This way we avoid the third stage transaction and instead of broadcasting it, we just tell bitcoind: This is the descriptor. Please include it in whatever next coin selection you do and we save one on-chain transaction. And anyone who would like...

Speaker 2: I guess I'm not too familiar with this, but how does bitcoind do the satisfaction basically, right? Like, because you're giving it a bunch of other stuff, right? And it just knows. I guess, that's the magic of miniscript or just curious about that at least.

Speaker 0: I think they compile it internally. At least, they run the compiler code internally. But I'm not sure.

Speaker 2: I guess I meant more like it in obtaining the input. Maybe that's a manual step anyway. Like, it can at least observe it, and then it asks you for the pre-image and you give it to it or something like that.

Speaker 0: Yeah, I don't know if anyone knows this part of it.

Speaker 8: Oh, you mean for spending it when you do the import descriptor with — because there are a bunch of parameters there, right?

Speaker 2: Yeah, yeah, that's what I mean. Just curious what the API looks like.

Speaker 8: Yeah, good question. Has anybody actually used bitcoind RPC API to spend?

Speaker 2: I think now they recently added tapscript support as well, which is I think newer on the bitcoind side. Maybe it was already specified, but that's another thing that I think happened recently.

Speaker 8: Okay, I'm actually really curious too. That is a fascinating question.

Speaker 2: Cool. I guess it was like he ignored the revoke script because there's sort of like a thing there to make the anchor still sweepable. But probably one thing I think would be useful is just to look at exactly what the diff is because it says: One byte here saved. I'm not sure exactly where that one byte is. I don't know if it's like an op drop. It looks like it most likely maybe the op drop gets moved or eliminated.

Speaker 8: Yeah, I think it is because when you don't op drop it, it actually still ends up being true. Then, the true is equal to the one, and then you can do that.

Speaker 2: Yeah, exactly. The funny thing is, I think someone pointed this out very early on, but we were like: Oh, that's kind of hard to understand, right?

Speaker 8: Yeah, we were talking about that, and so that is why we're initially leaning towards keeping that in just for clarity. But because miniscript is too optimized, I guess if we value the importability, we're going to abandon the clarity. But yeah, it's like that thing with not using nonce for unilateral closes. I feel like there are both drawbacks and benefits to both positions.

Speaker 2: Yeah. I mean, I think it feels like the miniscript art is strong enough, particularly people are aligning their tooling with that.

Speaker 8: Well, it depends. I think it depends on whether people are actually going to be able to easily provide the necessary arguments to spend from bitcoind. And if that is — I guess other wallets also use miniscripts to import the scripters. So maybe not necessarily. However, I do think that it requires the spender to know a certain amount of state that might be rather inordinate for the usual Bitcoin transaction output. Because all of a sudden, your on-chain wallet needs to be aware of how your Lightning wallet worked and what the pre-image was, et cetera.

Speaker 2: So, I've been following this, but here's a PR, I guess it was merged two weeks ago, that adds tapscript to miniscript. And because as far as I can tell — well, I guess the thing is, I think in most cases, our branches are pretty simple, but I think this one would let you do the top level of taproot one, which maybe does something. But I guess this is the same OP, so I'm assuming they've done that properly.

Speaker 0: Yeah, and to be honest, we don't actually need miniscript compatibility on all scripts. The only ones where we really need it are the two local and two remote, just to avoid the third stage transaction. So, those ones are easy to make compatible and maybe they are already. No, one of them is not.

Speaker 2: Yeah, I think one of them, one byte.

Speaker 8: Yeah, wait, but [redacted], what do you mean with with the top level spend? I thought that is now a nums point.

Speaker 2: That is, well basically I think they’re saying that they were ignoring one of the scripts because one of the scripts just pushes data onto the stack, so someone can use that data to sweep an anchor if they need to. So, I think they’re saying that they ignored that because according to miniscript, that's useless. But for us, we have an application level use for it.

Speaker 8: Okay, I see what you mean.

Speaker 2: Yeah, because otherwise, Miniscript would optimize that out because it realizes it's not used for the script at all. But cool, yeah. So it looks like everything is just basically, in a nutshell, getting rid of the op drop. I don't think any of the witnesses changed as a result. Maybe there's a pubkey ordering thing that does. But okay. I'll look at the actual side-by-side diff. Maybe I'll post that too, so it's a little bit easier to see exactly what that looks like. But yeah, otherwise, it makes sense.

Speaker 8: The witnesses should not change because the value is coming from the script not from the input, not from the redeem script.

Speaker 2: Yeah. But for whatever reason, it swapped a pubkey ordering, I don't know why it would. Maybe it would, but yeah, I think you're right. The witnesses shouldn't change. I guess a good thing I haven't done the weight estimation test vectors yet as well, because now, minus one and everything, but okay.

Speaker 8: Well, after 118, which is now this pretty quick release that we're doing due to a deadlock, we should be able to merge Taproot stuff for ending in 119, I'm looking forward to.

Speaker 2: Exciting.

Speaker 8: Oh, has there been anything new regarding gossip? Is [redacted] on the call yet?

Speaker 2: So [redacted] is not here, but asked to pick up gossip stuff again. One thing that we're doing for .18 — I think I mentioned last week — we're actually implementing the timestamp for everything now because we realized that without that, we have a hole in our graph. Because sometimes we don't hear about a zombie transaction or our channel doesn't get much records, so we're doing that. But I probably need to check my notes on the gossip stuff. I think last we were looking at like some of the stuff to add compatibility and what that upgrade path would look like. For example, like when people upgrade, are they gonna start to send all of their old channels with the new style thing? Will they only do it going in the future? I think we were just discussing what that pipeline looked like. Based off of that, do we still need the backwards compat announcement stuff there? Or I guess also, would we be announcing backwards compat stuff with Schnorr signatures as well? I think there's some things that we're chatting about with [redacted] and it came up, but…

Speaker 8: What about when you announce backwards compatibility, backwards compatible, or do you mean compatible announcements or announcements regarding compatibility?

Speaker 2: So basically, announce a SegWit v0 channel using the new scheme. Exactly like you know…

Speaker 8: Oh, I see what you mean. Yeah.

Speaker 1: Yeah, we did come up with a scheme for that. We thought about trying to retro in using the old signatures and stuff. It's just too fucking ugly. Basically, it is nicer if we've got this. I mean, we're gonna have to this transition stage where you're gonna have old style gossip and new style gossip anyway. It's not too bad to have to shoehorn a couple of these, right? You shoehorn the old, so you can announce the old style SegWit v0s on the new gossip thing. So, we can actually transition without ever having to close their channels. It's not too bad. Ideally that gives us a nice transition, right? And we can eventually stop with old gossip.

Speaker 8: How can you announce old gossip using, I mean, old channels using the new one, if you now have 50% of pubkeys that are not going to be representable?

Speaker 1: Oh, you have a tier.

Speaker 2: I'll use my pubkeys still.

Speaker 1: Yeah.

Speaker 8: But like if you're using…

Speaker 1: You can still invert. It still works.

Speaker 2: Okay. Alright. So, I'm looking at some of these notes here that I had from last time I chatted. I think one question we were asking is that, to my knowledge, I think it's not that you'll reannounce the old channels with a new scheme. It's that you can send a new channel update. You can send channel update 2, right? Is that your understanding, [redacted]? Or are you saying that you would reannounce the entire thing? Or just send channel update 2?

Speaker 1: I think you probably want the whole thing. I mean, it's the — I'll have to go back and check my notes too. I mean, I do want to turn off the old gossip at some point, and not wait for everyone to have reopened all their channels to do it. But I’ve spoken to someone who hasn't actually implemented it yet. I reserve the right to change my mind if I run screen when I actually meant this, right? But we're currently — it's one thing didn't get in this release, but it was to rewrite our whole gossip handling because it kind of evolves over time. And now, I'm like no no before I put this new stuff on top, I want to basically rip.

Speaker 2: Yeah, I was looking at doing something like that to ourselves.

Speaker 1: Yeah, exactly.

Speaker 8: We did fix that nasty RGS bug last Friday. So now, we no longer need Gossip. Everybody can just bring that server.

Speaker 2: Oh yeah. We can just use [redacted]’s server. We can run our own too. Okay, so other thing I wrote down was — okay, no announcement too. Everyone can just start to advertise that itself. I think the only thing that we were discussing was sort of just vector bookkeeping. Not significant. Basically, send both versions. I think something around comparing timestamps versus block height, right? Because for the old channel, it'll have a update one with timestamp, and then on update two with a block height. I don’t remember exactly what we were trying to drill into there, but I drew that down for that channel. You have both versions. I don't know if it really matters much.

Speaker 8: I thought the announcement only had block height and then updates had both timestamps and — yeah, I thought it was based on the semantics, where announcements had the block height.

Speaker 2: Correct, yeah. Announcement has an SCID, but channel update has a timestamp. Channel update one has a timestamp, but channel update two, we're looking to just move to block height every row for the most part.

Speaker 1: Block height, yeah. Which is much nicer.

Speaker 8: Yeah, I agree.

Speaker 1: Yeah, the question is: What happens when people do a query? Which one do you return? I think you blast both of them because you still want to propagate. So the thing is, even if people understand the new one, you still want to propagate the old one, right? Because most people are gonna have to be bilingual for a long time. That makes queries a bit weird. I think maybe we have to think about that. Like, if someone says: Hey, I want everything from this block height onwards. Do you just go: Well, I'm giving you the latest v2 one. So I'm gonna give you the v1 one as well, because why not? Someone has to think through all that.

Speaker 2: Yeah, and I guess they can just ignore it if they don't understand it. So you reset the message typewriter or whatever.

Speaker 1: Yeah, exactly. I'm thinking we…

Speaker 8: Do you envision new queries being able to query by both block range and the Frankstum range?

Speaker 1: I don't know. So I'm hoping that we go to mini-sketch, and we basically just sync the new stuff, but that won't help for the old ones.

Speaker 2: Yes.

Speaker 1: But in my head, I've got it so that you basically just deal with the new ones all the time. If I'm ever going to send you a new one, and there's an old one tagging around, I'll send you the old one as well, and you can just ignore it or whatever you want.

Speaker 2: Also, in theory, you can convert between a timestamp and a block height, given some arithmetic, right? So, it depends. If you want to put it all in the same bucket, you can do it, right?

Speaker 8: What kind of arithmetic?

Speaker 2:  Well, if you just assume about 10 minutes per block.

Speaker 1: Use the median time.

Speaker 2: Or just use the timestamp of the block height itself.

Speaker 1: Offset by an hour and use the median time.

Speaker 7: I went down this rabbit hole, and I think it's uglier in practice than in theory. It sounds like it's feasible, but until you implemented it, I don't know. I'd hold off judgment there.

Speaker 1: Yeah, the other thing is that you end up with a thing that can't happen, which is that you can have two timestamps that land you in the same block height. Then you're like: Well, are these the same update or are they different?

Speaker 7: Right. I mean, what happens if you get a one block reorg, then you got to look at all the most recent stuff.

Speaker 8: Yeah, a timestamp could also feasibly refer to multiple blocks, considering that with the median block height and the up to 2R drift. It could be really anything. So, any timestamp could probably map to a range of maybe like 12, 15 blocks?

Speaker 1: No, the median time has to move forward, so you can use median time and have some offset and you'll get a specific block, but it doesn't really help you that much because you could still end up with multiple. Yeah, I mean, that conversion is theoretically possible, but it's ugly and seems kind of unnecessary. It's possible that we'll end up with some — anyway, we really have to step through and see what this is going to look like, right? Especially with all queries. Like, do we want a new set of queries? And what is it going to look like? But I would definitely like to do mini-sketch across this. One of the things about block height is it does make mini-sketch a lot easier. But yeah, for a long time, we're going to have to deal with the old stuff.

Speaker 7: Yeah, that was basically the last roadblock to mini-sketch, so for set reconciliation.

Speaker 2: Okay, cool. Alright, I'll funnel some of that back over to [redacted]. I think it's just like some of the points that we had when I was looking at it to take a look at. I think [redacted] has some code now, lie the messages. I think the start of some of the new stuff, but I don't think [redacted]’s looked at what the backwards compat stuff looks like as clearly as far as advertising deal with the new. But, at least, we can do the new and then make sure the old isn't super weird. Cool. It looks like we have some initial code towards that. I think by next time, maybe we'll look at some of the backwards compatibility stuff a bit more. But yeah, we just have legacy stuff, where we can store the node announcement too by having some random prefix in the database or we can just make it all better  before we start to do all these hacks on top of it, but we'll probably just work through some of that, so. And we're just generally trying to overhaul a lot of storage stuff in LND right now too. Alright, that was two birds. That was typewriter and typewriter gossip. Next, we had attributable errors. I don't think [redacted] is here, though, but we were looking at this and also the inbound fee stuff on the LND side. I think once we get through further on that — I think Eclair actually had an implementation, or a comment rather, but I think you just have to look at the PR in a bit — but we could in theory start to do interop there? Because [redacted]’s PR is just sort of like sitting there, so.

Speaker 0: Yeah, I think we could because we have a branch. We haven't merged it to our master branch yet, but I think it's ready and should be implementing the latest spec, unless there are feedback. There's some feedback on the spec. But I think everything is just waiting for cross-compat on our side.

Speaker 2: Pretty cool. Alright. I will tell [redacted] about that.

Speaker 0: Well, there was some comments from [redacted] on the safety arm that haven't been looked at by [redacted]. If you can have a look at them.

Speaker 2: Alright, I'll just link that to [redacted] directly as well. Oh yeah, feature goods. Check. My quarterly homework to [redacted] is still there. Maybe I'll try to get someone else to look at it. It's there. It's going to happen.

Speaker 0: I think it's more annoying to review than it was to write, so you're going to have a hard time.

Speaker 2: Alright. I'll make sure to get some nice coffee before I sit down with that. Going down. Inbound fee stuff, I think it's a similar position. We're doing some review testing and stuff like that. Also, we were focusing some more on blinded path stuff to get some of that into 18. I think [redacted]’s pathfinding has been merged in. We have a follow-up for that, and then, we're also working on forwarding on some other things around recognizing when an error comes from within the tunnel versus outside. Things like that. So moving forward on that. I think that's where all some of our attention was instead of some of the other inbound stuff and things like that. But yeah, so the goal is at least to get that base version into 18, which is like 10 weeks from early next year. And then we can move forward with everything else from there to complete the stack. I don't know if you have any direct updates on that. I think we've all been interoping for some time now as well. It's just a matter of getting through the remaining PRs. Or around, at least.

Speaker 9: On route blinding stuff?

Speaker 2: Yeah, route blinding stuff. I was trying to give an update for you.

Speaker 9: Yeah. So we're into upping paying CLN and LDK, and then I've just got to follow up to do the like handling the error in the right way. I'm still busy reworking the forwarding one, which is just infinitely growing in size. So yeah. Just breaking that up into two smaller PRs And that also works, and is interoping, but obviously needs review and everything.

Speaker 2: Cool. Okay. Yeah. So the HTLC's flow, you just got to finish up the actual code of it. Cool. Any other grab bag stuff people want to discuss?

Speaker 0: Yeah, there's one thing I wanted people's opinion on. It's the email about zero reserve that I sent to the mailing list. The link is here. Just wanted to get feedback from people to see if I missed something because we've been doing zero reserve for a while on Phoenix. But we were only doing zero reserve for the Phoenix side, where we were actually taking a risk, but it's a measured risk because the user has paid us fees to get into the system anyway So, even if they publish a revoke commit, it's okay. We can just — we know they're not going to be able to steal money. We're going to be able to penalize that. I think that it's easy to argue that the other side works as well. And that it's  mostly a good thing to allow the LSP to be zero reserve as well. But I'd like people to just check if they think the incentives are okay, and just tell me if you think there's a strong knack or if it's okay.

Speaker 2: Yeah, I guess my initial take is like, I view it's kind of like the zero conf channel type in the first place. Basically, you can opt into it, and it's sort of your risk type of thing. Or are you proposing something different in terms of like making it a blanket thing? Or, I guess, just permitting someone sending it to setting to zero in the actual initial funding flow?

Speaker 0: Yeah, but the interesting thing is that even if it's set to zero — yeah, the goal here is that whenever you do zero reserve, you do it on both sides. But even if it's set to zero, the channel initiator still has to be able to pay the fee for the commitment tx. So, it's not an additional reserve on top, but it's still something. That plus the reputation and the fact that they should be earning fees from you, I think is okay. And also the fact that just being able to publish a revoked commit and having an incentive to do that, instead of publishing the latest date, doesn't bring you much because in practice, you're never going to win. So you could do that, but it's exactly the same as L2, where you can always publish for latest date, and you are wasting on chain fees by doing that. But you're not going to win anything because people are watching the chain and are not going to let your revoked transactions go through.

Speaker 10: But I think that's the point of a mobile node, right? Or the mobile node is probably not watching the chain and you will win pretty large percentage of the time. It's only open, the mobile node, once a month.

Speaker 0: But if they only plan to open it once a month, they should put the self-delay to two months.

Speaker 10: Okay. Does Phoenix let you configure that?

Speaker 0: No, but we tell people they should connect regularly. We put notifications. The app runs in the background. If it's not able to connect to its Electrum server and check the chain, it's going to warn the user that they should come online.

Speaker 10: Yeah, but people just ignore notifications. Like that's not a thing.

Speaker 1: The argument is stronger for L2 because watchtowers are so trivial, right? So, it's not — I think the argument is possible to make, but I think it is definitely stronger for L2, where anyone could be a watchtower. One of us could run a watchtower for the whole network, quite trivially, with L2.

Speaker 2: So two questions. You're saying it's not actually zero because the initiator still needs — so, it's zero for those final, but the initiator still needs the fees to pay for everything, basically, right?

Speaker 0: Yeah.

Speaker 2: Gotcha. I mean, one of the things that we're gonna officially implement, the whole fee buffer thing, We have a PR for that now. This is like to me we're into a while back. You basically need a buffer. I think we're just matching the behavior of Eclair to Lightning, CLN,I think now with as far as the amount. That reminded me of just edge cases with reserves and fees. But I guess I can check out the thing more. I think mine is just like: Yeah, I guess if both people said it, they both opted into it, right? So I don't know. And people do zero conf in a similar way already.

Speaker 0: It's basically that…

Speaker 1: The zero conf is transient trust, right? So this is slightly different. Zero conf is like you're kind of out on the ledge for a little bit, but confirms happen, and then, you're happy again. This is a longer term trust issues. It's not quite the same. But I tend to be like: I somewhat agree, right? There's definitely a UX win to having zero reserve, right? You don't have…

Speaker 2: Yeah, and a lot of mobile nodes, because I know, for example, I know Breeze with their LND version does this. A bunch of people have been doing this for some time already. It's an old little corner.

Speaker 10: Yeah, we always allow our counterparty to give us zero reserve, but we never set it. So I think that's like what Phoenix does. We always like: If our counterparty wants to do something, we let it.

Speaker 2: That makes sense.

Speaker 0: It's not a UX thing. The main issue is that, especially when we start moving to dual funding and splicing, channel reserve is 1% of the total capacity, which means that as an LSP, you have to put in reserve 1% of all of your users' funds. So, that just doesn't scale. As the LSP, you just cannot really scale because if you have to keep a new liquidity that is 1% of all your user base — all of their money, not yours — it's just a lot of wasted capital.

Speaker 10: I mean, you shouldn't set it to 1%, right?

Speaker 0: Yeah, but that's what happens by default. So, then we started thinking: Oh, but maybe then, we should override that to a hard code to another value. But then we said: Oh but does it really make sense to have it at all and that's where we got that's why we got here

Speaker 1: Yeah I think the original dual funding just nailed it to 1%. That's what everyone's using. But I somewhat agree. Like, 1 and 0 are the compelling values, right?

Speaker 0: Yeah, because it's annoying. We have users that have 10 BTC channels. So that means we have to have 0.1 BTC just in reserve for them. It's really a lot. It's really wasted capital, and those people are usually not using lighting much.

Speaker 2: I guess I need to check if we allow it or not. I think maybe we disallowed explicitly. At least, if we were looking to move something like LDK's approach, where we let people just set it. Or we let people set it for us, but then accepting it is different. Or setting ourselves different rather, because we need a flag for that. And a good point about the whole, I guess, over time many channel thing, around that 1% of the queue of 1% as well. I hadn't thought about that before. I guess I'll check out the email. Yeah. I guess the behavioral change here would just be everyone lets people set it, or without the feature bit, or I guess what do you think this will look like deployment wise to us?

Speaker 0: Yeah it's that we use a feature bit and that feature bit means that both sides get zero reserve.

Speaker 2: Sure. I've got to hop off here in a bit, but I guess while we're here, anyone have questions around this whole RBF thing? We're assuming we know the skinny.

Speaker 9: I have a miscellaneous thing, which is unrelated. If anyone would like to, on Friday, Chaincode's running a research day, which the goal is to nerd snipe some researchers into working on Bitcoin and Lightning. So we've sent a few people emails, but just if you have anything on your wishlist that you'd like to try and get some academics interested in. If you want to send me a one page write up of what that is. We're going to have them on display, so that folks can sort of get interested and reach out to people working in the development space. Just a little show there if you want to try and nerd snipe some academics. We're doing our best.

Speaker 2: I just posted the link in chat here as well. It's brd23.com. Nice domain. Yeah, I need to figure out my travel plans and stuff. Okay, cool. Thanks for the plug there. That's this weekend, right?

Speaker 9: That's Friday this week, yeah.

Speaker 2: This Friday. Okay, cool.

Speaker 0: Cool.

Speaker 10: So if you want to submit stuff, it has to happen like today or tomorrow or whenever?

Speaker 9: Yeah. I mean, ideally Thursday. It's just sort of a one page that we print, but yeah.

Speaker 2: Cool. Okay, cool. With that, I posted my notes on the thing and thanks everybody. Cool. See ya.

