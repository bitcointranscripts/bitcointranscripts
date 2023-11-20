---
title: Lightning Specification Meeting - Agenda 1088
transcript_by: Gurwinder Sahota via TBTBTC v1.0.0
tags: ['lightning']
date: 2023-06-19
---

Agenda: <https://github.com/lightning/bolts/issues/1088>

Speaker 0: Thanks [Redacted]. So, there isn't much that has changed on any of the PRs that are on the pending to-do list, except for attributable errors. So, maybe since [Redacted] is here, we can start with attributable errors, and [Redacted], you can tell us what has changed about the HMAC truncation, for example.

Speaker 1: Yeah, so not that much changed. Just the realization that we could truncate the HMAC basically, because the failure message was so large already. If you truncate them, you can get to - let's say, 1200 bytes - roughly for the failure message. So, fitting within one, is it called an MTU unit? What is it actually called? MTU? [Redacted], you know all about that.

Speaker 2: Yeah.

Speaker 1: And I guess the downside is, of course, if four bytes, an attacker could correctly guess the HMAC, but then we realized that this is not super critical. If there's a failure message and you interpret it wrongly, it's not the end of the world. And also, it's a very difficult game for an attacker to play because if they make up an HMAC and it's incorrect, they will get penalized, and their next chance to try this again will take time. So, yeah, I didn't think about this before. And then [Redacted] said: Yeah, maybe we can do something with a graphic accumulator, but sounds like perhaps over-engineering with the whole idea of reducing the number of bits that we reserve for the HMACs. Yeah, maybe it makes sense. So, that's what I'm interested to hear from you what you think about that.

Speaker 3: Are we that concerned about the size of these things? I mean, does it really matter if it's two packets on the wire or whatever? I mean, it doesn't need to be 32 bytes. I don't know what it previously was defined as. It could be 16 because we're not worried about the original - the person writing it - having colliding with themselves. That's not a threat model. So 16 wouldn't - like, we would still have 'cryptographic security,' right? But are we that space constrained? Is there that much objection to the size of these things?

Speaker 1: I don't know really. It's difficult to say. I always identified it as a problem looking at how much we optimized our other messages in the past, like you know this X or of the channel point. I'm not sure if you remember that. Like really trying to save one byte. So...

Speaker 3: How big are they right now? Sorry.

Speaker 1: Well, right now as in the legacy format or in the attributable error, like the previous version?

Speaker 3: In the previous version of the attributable error.

Speaker 1: I think the map was about 12 kilobytes. Something like that.

Speaker 2: Yeah. There's a happy point somewhere between one packet and 12k, right? And as [Redacted] says, yeah. But getting - I'm impressed that you got it down to 1200 bytes, that's...

Speaker 0: But that's because you use only 32 bits of HMAC. So, can you explain how that - what exactly could an attacker do? How exactly would they try to replace someone else's HMAC? And I'm not sure I understand why they are risking something and how they can be not successful at that because it's not that much to grind, right?

Speaker 1: It's not that much to - sorry, what did you say?

Speaker 0: To grind. To make sure that you have only 2 to 32.

Speaker 1: I think they cannot grind, can they? Because they have no way to know whether the HMAC that they create is correct. Only the sender is able to verify. So, it would not be grinding, but this would be more like guessing.

Speaker 0: Okay, okay, I see. So, if they have absolutely no way of doing more than a pure guess. Yeah, 32-bit is probably more than enough. But yeah, probably needs to dive into it a bit more.

Speaker 1: Yeah. But if you'll say, it doesn't really matter. We want 32 bytes or 16 bytes of security on the HMAC is also fine. But, if we can reason that it doesn't actually make it more secure because there's this game theory about nodes getting penalized and it's not a super critical data, maybe it is nice to keep it a little bit smaller. Perhaps if it's like mobile phone nodes on slow connections; something like that.

Speaker 2: There's definitely a latency win to one or two packets definitely has a marked latency win. But I don't know. That's something I need to check carefully, right? Because you're really blurring the lines when you start going: Oh, we'll throw out some cryptographic assumptions. But if we're right, and it is a pure guess, it does sound appealing.

Speaker 3: I agree. It'd be nice to do - what was the number of hops that you defaulted to previously? Because the other thing we can do, right, is we can say: Well, there's two options for the number of hops. And the first one is max seven or whatever, which basically everything is anyway. And then, anything more than that, you fall back to this huge size.

Speaker 1: In the previous proposal, I went for 27, like the presumed maximum. But now I try to - actually [Redacted] did all this preparatory work - but I've been playing with that myself also a little bit. I settled for 20 hops and four byte HMACs because that ends up with a 1200 byte failure message. Obviously, you can also make it fewer hops than that. What I currently do is - in pathfinding, I don't look at this feature at all. I just look for the best path. And once the best path is found, I'm going to check all the node features, if all the nodes support attribute-divider errors, and the route length is below the maximum supported by the structure of the failure message, then it's going to be used. But if you put it to seven, and we would find the route as nine hops, then the LND implementation, at least as I'm proposing now...

Speaker 3: Sure, but the network diameter is like seven, right? Or something like that today? It's not very wide. So, even if we don't have to do - seven is obviously aggressive - but you could do 15, 12, you know. There are other mediums that we could pick if we don't want to go down to 4 bytes and would instead do 16.

Speaker 1: Yeah, I think one thing that's also important is when I was still at 12 kilobytes, it felt big and it seems that we needed to add some parameters to tailor to whatever the sender prefers because of its bandwidth. But then, people already raised the objection: Okay, this is introducing a fingerprinting factor because you can look at what is requested, so you know something about the sender. And if you can just make the whole thing overall smaller, then maybe there's no need for parameterization. So, in the current implementation, I just removed all the parameters. The sender is only signaling to every hop that it wants attributable errors, and then the parameters are just fixed in the spec to whatever we want them to do.

Speaker 3: No, totally huge fan of non-parameterization. To be clear, I wouldn't worry about the actual bandwidth here. If you're a mobile node, you're only sending or failing one or two of these at a time, so what do you care if it's 12 KB? It's true, you have high - if you send 10 packets, you might actually lose one, and then you have a bunch more latency. So, there's a consideration there, but the bandwidth itself is not the consideration. That's more the latency.

Speaker 1: Yeah, but I think if this story about the game theory and guessing, if that is indeed correct, maybe there's no reason at all to go bigger then.

Speaker 3: Yeah. It's worth talking about in New York. I agree. I think. Yeah.

Speaker 1: The other thing is I also tried to simplify - I started simple and I make it complicated; and now, try to simplify it again - is the format of the payload of the intermediate nodes. So, they can all attach data to the return packet. Initially. I just had four bytes to hold a hold time in milliseconds. And then, I switched to a TLV format to make it extensible, but also not really extensible because the length is fixed. So, the sender would communicate the maximum number of bytes, and then all the routing nodes would put a TLV stream in there. But, you need communication about: Okay, what should the node put in there? It just felt like: Do we really want this now? So, I reverted back to just four bytes for a whole time. Also, because there seems to be not much inspiration for whatever else we can put in that field other than the whole time. Currently, we're signaling this attributable error thing with an empty TLV record in the forward pass. If in two years time, we change our minds and we decide that: No, no, we need more space. Maybe we can just add a byte in there, or use a different QV record to signal: Okay, now this new format, and go from there.

Speaker 3: I was a fan of the extensible format there. It is fixed size, and we have to pick a size and we have to pay for that size. But again, we pay a privacy penalty every time we add a bit here, and I'm not a huge fan of paying another one. If we end up needing one extra bit, like why not? The TLV overhead sucks because for TLV, we have another two bytes per field for the TLV. But I don't know, I mean, kind of why not? I don't see a huge reason to rip it out. It's not like we have to, it's not like we would commit to, you know, 64 bytes or something for each hop. We'd do something smaller for constraint, but hey, at least we have flexibility.

Speaker 1: Yeah. I'm also open to that. I just try to simplify the whole thing. I don't know if any one of you have seen my little project in Layer 1 about the annex and the annex format. There's also several ideas how to shape the annex if you even want that. They also invented another TLV format, which is also quite interesting, like where the records ID is a Delta. So, if you have increasing records, you only have every small Deltas and then there's a new compressed in format. So, if we really want to save bytes, perhaps it's also interesting. But if in Lightning, we have our own standard, which is not as compact, but it is a standard.

Speaker 3: We need four more ways to encode everything in Lightning. We don't have enough.

Speaker 1: Yeah, maybe another thing taken from L1.

Speaker 2: Yeah. Middle-endian. We need some different endians in there just to really fuck things up.

Speaker 3: Yeah. Just like in stratum.

Speaker 2: Yeah. So, the per hop is completely a linear function, isn't it? So, you know, if we were to go from four to eight, it would basically be adding another four by 20 bytes.

Speaker 1: So much of change now that. I think whatever we decide here, I think everything is just going to work. And even if we make the wrong choice, then we can sort of correct it later on, but at the expense of flagging another bit indeed. But I am a little bit worried about having all these options, and we need to talk about that for a long time before we finally get to make it. So I'm a bit - well, we see New York how it goes. Maybe we can just settle on something and just go for that. I think especially with the smaller sizes, it does feel - even though maybe rationally you would say like bandwidth is not so important - it does feel a lot better to me if it's just one kilobyte, 1.5 kilobytes, it's almost the same as forward onion. And it feels better, but maybe it's just emotional. I'm not sure.

Speaker 3: No, I mean, if you're sending 400 HTLCs at a time, it starts to add up pretty quick.

Speaker 1: Oh, you mean failures?

Speaker 3: I think I'm ready to say we should finalize this in New York. It seems ready. Seems like it's time.

Speaker 1: OK, let's do it now.

Speaker 2: Yeah, and we'll debate all the details. We'll come up with some happy numbers. I'm going to have to validate that there's no hole in your theory about four byte HMAC 'cause it feels it's a slippery slope, right? Why not three bytes? Why not three bytes? Definitely not two bytes, you know, like...

Speaker 1: Okay, how about 20? Two bytes is probably fine, honestly.

Speaker 2: Two bytes, no. Two bytes starts to get - I don't know. The point is that I think if you get it, if you manage to nail it, you can penalize a different node, right? So I think that's the success.

Speaker 1: Yeah, I know, but then 65,000 times, you're not going to nail it, and then you're penalized all these times. So, and then it's a little bit lossy anyway. Like this whole reputation thing. So yeah. Maybe one byte is enough.

Speaker 3: No, we just gonna do three bits.

Speaker 1: Yeah, Three bits. Okay.

Speaker 2: Three bits - yeah. Let's discuss in New York, but it sounds it's, I don't know. You're right. There's an emotional difference between 'Oh, this is like 12k' versus 'This is like 1200 bytes' - starts to sound like a no-brainer. But I think we should pick something as few parameters as possible while squeezing in as much extensibility as possible and just just commit to that. Because I think I agree with you. You can kind of go over design, and then you've got more complexity or go right back. And if we can find the point where everyone's happy, that would be great in New York.

Speaker 1: Maybe for the TLV. Maybe we can think about if somebody can come up with at least one other application that would need storing something in that return payload because otherwise, it remains so theoretical. It's just extensibility without having any idea what we could put in there.

Speaker 2: I can think of only one. So, there was this idea of paying for anti-spam and you would logically - so you could actually pay SATs, but you could also pay in, like, I could issue Fedi tokens or some kind of e-cash token, and you will give me some SATs. I will give you back some e-cash tokens that you can use in future to pay for forwards or whatever, right? But that's probably pretty big - right? - to return in the error. That's a non-starter.

Speaker 1: Yeah. Well, that's also one thing we need to talk about in New York because this is only about the failure message. And the timing information is something like an additional benefit of the new design. But we might want to also do this for the success path, just because then it's a full circle.

Speaker 2: Yeah. Yeah. Well, but [Redacted], your actual available liquidity only. I can squeeze that in a bits of the timestamp frankly, because you need about two bits to say how far off you were. So yeah, you could steal the bits of the timestamp and go: Well, obviously the top two bits mean that or something. Let's discuss it in New York. And yeah, I do actually want actual available liquidity. As in something more than just: Meh, it's something didn't work. I want an explicit: No, lack of liquidity message. Ideally with a hint, because you're going to slam me with the binary search anyway. Why don't I just tell you whether it's worth trying or not?

Speaker 1: Yeah, but this is part of the errors note payload, right? This is just the regular thing. This is not for intermediate notes.

Speaker 2: Oh, that's true. Yeah, intermediate notes don't need to tell you how much.

Speaker 1: If you just want to spread that information around regardless.

Speaker 2: No, yeah, maybe not. Okay. Well, if anyone can think of something, then that may justify extensibility. Something that takes more than one or two bits.

Speaker 1: Yeah, but we can do it anyway if we feel that it might be useful. And also, if we don't do it, I think it's still possible to go around that because there's also another byte reserved currently to signal whether a payload is an intermediate payload or a final payload. The only uses value zero and one currently. So, you could also introduce a two and a three there. So, I think there's a lot of ways to improve if you want to.

Speaker 0: Right. I think, for the other PRs, I don't think there's much to cover because we've already covered everything last time, and there hasn't been any new development apart from [Redacted]. People said that on the authors PR, test vectors are apparently lacking or incorrect. So, maybe even on the onion messages PR, I think we should be ready to merge that one, but maybe it needs a rebase. I'm not sure. No, it doesn't look like it. Oh yeah, okay. My last comment was that [Redacted] or someone from LDK was supposed to verify the test vectors on onion messages, and then we would be able to merge that one. So I don't know if [Redacted] or someone else has worked on that on the LDK side, and is here. Otherwise, we can do it in New York.

Speaker 3: Looks like [Redacted] will send me a question first, sorry.

Speaker 0: Yeah, then we will just validate that in New York and merge onion messages, so that we can then rebase our files on top of master, which is a great, great achievement. And then see if there are test cases to test vectors to fix. But apart from that, I don't think there were any feedback on offers or anything else.

Speaker 3: Yeah, the complaint about test vectors is that there's no actual message content. Like there's a string format test, but there is not a test vector for an exhaustive test vectors for the actual offers and all the things that could go in them, which would be nice to have. So yes, it's not that they're wrong. It's just there's not enough of them.

Speaker 0: Alight, perfect. So, do we want to discuss one of the other PRs? Is there anything someone wants to discuss about the PRs or should we start preparing the summit and deciding on which topics are worth discussing in whole groups versus smaller groups?

Speaker 1: I have one question, not related to PRs and also not related to New York. So in my little project about the annex, I got to know this thing a little bit better. And I wondered: Are there any implications for taproot channels in Lightning? So, just assume that annex is standard without restrictions. Let's say that's just like an alternative node that allows all the annexes as long as it is consensus valid. Like, what does this mean? I think typically, the problems occur when somebody is stuffing that annex. So, let's say you've got a dual funded channel, and then the final signer - it's stuffed that annex - and then it brings the fee rate right down. And then the other party sees their coins locked, for example. But I'm not sure what else there is. It seems mostly focused around that, because if there's just a single sign or you're only increasing the size of the transaction, but it's your own transaction. And we're just wondering if there's like any like crossover there with what's happening in Lightning currently.

Speaker 0: On the fee rate staking issue, I think that even without that, the last signer can already increase the size of his witnesses or he has other ways to make sure that the transaction is bigger than expected. So, that's an issue anyway. I don't think the annex will make it worse. So I think it's an issue anyway.

Speaker 1: So, before CoinJoin, they were talking about the mitigation, where a participant needs to reveal their complete taptree, so that you can verify that the source of the coins does not allow any spend path that includes 1MB JPEG.

Speaker 0: Yeah, but even with that, if you decide to accept inputs that are UTXO that are unconfirmed, you potentially cannot verify their ancestors without looking at your mempool, and maybe they are not in your mempool because it's just not in your mempool yet. And do you want to reject all those channels? If you do, then, potentially, it's an issue because maybe it was a valid one and you're just going to receive the parents right afterwards, and they were paying already a high fee rate. But if you accept them, you don't know the fee rate of the parent, so maybe the fee rate is going to be bad afterwards.

Speaker 1: Yeah, but you can get around this by only using confirmed inputs then. And if you...

Speaker 0: Yeah, that's an option we put in Eclair, but another operator can decide to only accept confirmed inputs, but it means that you are going to actively reject a lot of things. And especially in a high fee environment, it's quite useful to use those unconfirmed inputs in other transactions to actually bump the parents in the same operation, so it's not really nice to disallow that, but yeah.

Speaker 1: Okay, so it sounds like this is not your biggest problem.

Speaker 4: For LND, for legacy channels and anchor channels, we enforced the length of the witness. And so, one thing for Taproot channels that we do is to not check the length of the witness. And I think LDK also asserted on the length of the witness when extracting like a pre-image or something. So now, they're variable. And so, you don't want to panic on going out of bounds on a slice check or something.

Speaker 1: Yeah, I also saw that fixed, that someone of your team made to pool. There was also fixed annex length of three.

Speaker 4: Yeah, pool wasn't vulnerable. That was just something I pointed out to them, just to check in case.

Speaker 1: Of course, we're still protected by standardness, but maybe it's also not a very real protection. So, good for me. Enough about it.

Speaker 0: Alright, so should we plan the topics for the summit? I think that what we can do is just grab them in order of the votes, and for each of them, just flag them as we want to discuss that as the whole group or we can just put it separately in smaller groups. That's okay? Alright. The first one on the list is Gossip v1.5 versus v2. I think it's interesting to discuss that one as a whole group. What do you think? Can someone take notes or do? Perfect, thanks, [Redacted]. This comment contains the other list in the screenshot. Oh, and [Redacted], you're muted.

Speaker 2: I think the gossip debate on exactly what that's going to look like. And the minutia of that and the simple taproot channels are obviously, clearly from this poll, really important, and I think that deserves everyone's input because it would be really good to nail those at the summit, right?

Speaker 0: Yeah, because we need to decide on what people actually implement afterwards. I agree. I'm not sure that PTLCs really need a whole group discussion, to be honest. I don't think everyone is interested in. There aren't many new developments on PTLCs. It's just that we need to finish simple type of channels.

Speaker 4: I think [Redacted] is going to come up with something, like just a draft or something.

Speaker 0: Okay, but does it need to be whole group or can it be in a smaller group?

Speaker 4: I don't know.

Speaker 3: That sounds like it can be discussed async too. There's not a proposal yet. Who wants to present one? Can do that like via the mailing list. Like, that seems like a way though.

Speaker 2: Yeah, I've always treated PTLCs as something that somebody just needs to spec. I don't think there's any controversy, right? It's just: Tell us what the fields look like, so we can code it up.

Speaker 5: Maybe to just give a bit of context about the space we've got. So, we have one big room where everyone will be sitting, but then we do have access to six or seven little breakout rooms that can have four to six people. So, maybe something like PTLCs, we could use the main space for that and people that aren't interested can just go and work somewhere else. There's also like a full set of desks and monitors where the Wolf people sit, where you can go and do a bit of work. So, that is kind of the layout that we're working with.

Speaker 0: Okay, sounds good. I think it will be useful for the smaller sessions. I think it will be useful to just do what Bitcoin can't even do, where we just find a creator schedule for each room and people put post-its saying I want to discuss that in that room and we try to make sure that there are not too many overlapping subjects that too many people want to attend at the same time. But this way, we can divide efficiently across all rooms and make sure that we discuss the things that interest us the most. But maybe let's just figure out for now the topics we want to discuss all together. I think, for example, channel jamming is interesting to discuss all together because there are a lot of high level decisions on what do we actually do next, what do we research next, what do we prototype next, and it would benefit from everyone's input. I don't think that package relay needs a whole group session.

Speaker 2: Well, I feel package relay is something that everyone kind of needs to know about, but it's more [Redacted] saying: Here's what we're planning. And then, have a breakout afterwards. I reckon I'm speaking for [Redacted] here, but I'm assuming that it would be good for [Redacted] to do like a five minute 'Here's our plan for package relay,' so everyone knows. And then have a breakout room for people who wanna discuss the minutiae of exactly what's happening, right? Because there's package relay, there's v3 transactions, but it'd be good to get a high-level summary. so we all kind of know where we're going and then we can discuss the details if people want to break out.

Speaker 0: Yeah, agreed. It's true that there are open questions on the design of v3 FML anchors and until we have a good answer to those questions, nothing will make progress on the layer one side. So, we really need to give some input and say: Oh, we want that part and we want those restrictions and that size. So yeah, that's probably worth spending a bit of time. It should be quick enough.

Speaker 2: Yeah. We want zero fees, not one set per VByte, which was one of the proposals to make the coding for them simpler. I was like: No, we want zero.

Speaker 0: Yeah. So, high-end chain fees, I think it's more - even just corridor discussions, where we can say: Oh, there's those high-end chain fees. We have some ideas. Those are some of the small things that we made. Not sure it deserves a whole group discussion. Blinded paths doesn't deserve a whole group discussion either. It's just a breakout between people who actually spend time implementing it because otherwise, you're just going to be lost. And then, we can discuss the open PR that [Redacted] created and make sure that we rub that one up. Maybe dynamic commitments make sense as a whole group discussion because it also relates to splicing depending on what part of it is actually done in splicing and what really needs something different. I think it's interesting to make sure we converge on that one and we don't create two separate proposals that actually do the same thing.

Speaker 4: So, on our end, I think we were going to go ahead and do just dynamic commitments without splicing.

Speaker 0: But can't it just use the same protocol as splicing? But you just put it in place?

Speaker 4: Yeah, the issue here is that I guess we want to deploy it sooner rather than later. And so we would have to wait to converge on something there.

Speaker 2: So, can we have a definition of dynamic commitments?

Speaker 4: Upgrade the channel, upgrade the commitment type, and upgrade like static parameters. So, max HTLC in flight, something like that.

Speaker 2: Right. So, this overlaps with simplified as well. And there's already a channel upgrade proposal, which is independent of splicing, which is a couple years old, which we implemented, but we only implemented for static remote key. So, these things kind of pre-exist.

Speaker 3: Is there any - at this point, it sounded like that we were just gonna do it as a side effect of splicing and move on.

Speaker 2: No, because you don't always wanna spend the commitment transaction, right?

Speaker 3: Oh, you mean, yeah.

Speaker 2: You don't need an on-chain. To go for static remote key, for example, which is of course a bit obsolete now, but all you need is a quiescent channel. And so, you basically - if you look at the proposal, the upgrade proposal, and I could pull out the PR - you end up basically going, when you reconnect, you go: Huh, we are static. And you basically send a thing going: This is the channel type I want, this is the one we've got. And if you both agree that you want the new channel type, you basically do an upgrade, which is pretty simple. The only trick is that that you kind of want the ability to quiesce the channel so that you can guarantee you'll ever get into that state, but even without it, you'll just eventually reconnect and both agree on the new channel type. Pretty robust.

Speaker 3: Yeah, I'm gonna be a little annoyed if we end up with two ways to do this - right? - if we end up doing it as a side effect of splicing, and also having a wholly separate protocol to do it, when the case is where we don't want an on chain transaction. Is there some way we can like...

Speaker 2: It's really trivial protocol. It's not a problem. It's easy. I mean, I regard splicing as a subset of this. We go: I'm going to splice, and by the way, the new one should be this type. Is a logical subset. But, the dynamic commitments where you change other things, right? So where you go: Hey, I actually want to increase the max HTLC in flight or anything. That is a dumb suggestion because the right suggestion is to go for simplified commitments, and then have the ability to knack commitment transactions. So that, and I do not want to knack it without simplified commitments, because that would make our state machine an even bigger mess. But once you can knack, you no longer have to tell your peer about arbitrary restrictions that you have on the channel, right? Which I believe is one of the holes in current implementation interop. I'm pretty sure you can probably force them to break channels by disagreeing over what they're allowed to send. And that's always kind of bugged me a lot. But the reason that we have that enforcement is because there's no way to say: No, I do not accept your commitment sign, try again.

Speaker 3: Is there presumably in doing so, we would be able to say: This HTLC; drop this HTLC and try again?

Speaker 2: Yeah. There's a kind of three stage plan. You start with your simplified commitments, which basically means you're just doing turn taking. So, the state machine is significantly simplified. Once you've got that, it's pretty easy to then do a fast failure mode. So, the fast failure is basically a soft fail. You send me an update, I say: By the way, I'm going to fail that when you commit. And if you receive that in time, you can go: Okay, I unadd that one. And then commit without it. If you don't, you commit normally, and I will hard fail it the normal cycle, right? The step beyond that is that I send you the failure message, and then when you go, 'commitment signed,' I say 'commitment knack,' right? And we go through a cycle where it's as if you've not added anything, and then you can try again without that HTLC. So, that allows you to break all kinds of rules. Like, you could put an HTLC that's more money than you have, for example, and I'll just go: No, I'm gonna knack that, right? So, it does give a lot more flexibility, and it means there's no longer a max-in-flight or anything like that. I mean, I could give you a hint, but I don't need to because if you try to put an HTLC and I don't like I can do something about it, and I'm not going to be stuck holding it for this period of time. And thus having to tell you about all the restrictions that I might want to implement.

Speaker 4: When you upgrade from static remote key to anchors, do you have like an intermediate transaction? To make a new funding output? Or what do you do?

Speaker 2: No, no, you don't. You don't have a new funding output. I've only done the upgrade from my implement this ages ago, the upgrade from non static remote key to static remote key. But you could use exactly the same thing to upgrade to anchors was my plan. And after, I kind of want to implement because we had an experimental release where you could have the old anchors, and now we've got new anchors. It'd be really neat to do the transition there, but basically I've got three people who care. But what happens is, basically you say: From now on, we're using the new style, not the old style. And for every style that we have that works because you can't be in a state that doesn't work with the new one, right? There's no way you can have a commitment transaction that doesn't work on the new style, right? Because in fact, fees are dropped.

Speaker 4: If you upgrade the taproot, you're upgrading...

Speaker 2: Taproot's a whole 'nother - that's basically, you're doing a splice. You might be doing a dumb splice, but you're basically having to put new on chain. So, that falls more into the splice category. This upgrade is for - I just want to change the commitment format, not the funding format.

Speaker 4: Okay. So, one thing for dynamic commitments when upgrading to a taproot channel is that CPFP carve out breaks. If you don't, you need the intermediate transaction to confirm first before you start using the channel or CPFP carve out breaks. But besides that, I think we can combine the proposals, but we'll have to see what [Redacted] says.

Speaker 0: Yeah, I think to summarize, it means that there are actually three topics that we should bundle in one whole group discussion. Its: dynamic commitments, simplified commitments, and splicing. And we should discuss all three of those in the same session to make sure that we end up with something that lets us do all of them without duplicating effort.

Speaker 2: Yeah, I agree. And I think that if you want to upgrade, you end up doing a splice in a mode where you say: You can't add anything; we're just going to splice like a no-op splice. Which is probably an easy to implement subset, but still uses the same protocol, right? You'd say: I want to do a splice but we're not allowed to add anything. That should give you the ability to upgrade the output without having three protocols.

Speaker 0: Alright, then I think it's good. It's three topics that are going to be discussed in the whole group discussion. I think async payments don't need to be whole group. I think it's a small group discussion. Does anyone really want to have it in a whole group discussion?

Speaker 2: I'm kind of assuming that if people in the small groups come up with something that they feel they're ready to move forward with. They'll, at least, give a two minute summary to the room, so we know where everyone is.

Speaker 0: Yeah, definitely a good idea. Whenever we finish one of the smaller group session, we can just all come back. Or at the end of the day, every small group just gives an update on their results. I think it's the same for trampoline payments; definitely not worth a whole group discussion, we can do it in a smaller group. But I think it could be interesting to group the two meta state of future of LLM and meta specification process and have a small whole group discussion about that for all the meta things on how we work together. Anything that comes up, I think, is worth having in a whole group. I'm not sure that L2 and APO really need a whole group discussion. I think it's whoever is interested attends the smaller group one. Same for onion messages, dust mitigation. Same for UTXO management for splicing - is really a quick thing that I mentioned during the whole group splicing stuff. Attributable errors - we already said that we want to discuss it, but I don't know if it really needs to be a whole group. It's rather the people who have spent the time studying the crypto and understanding the proposal that will be really useful. And then, disabling update fee is just a byproduct of package relay, so I don't think there's much to discuss at all. Maybe inbound fees, if we want to discuss it again, but there was not much interest, and standard interfaces for LN as well. I think it's going to be smaller group discussion or things we discuss on the side, depending on who's interested. So yeah, I think that's a good summary. It's already split half and half. Only half of the topics are really useful for whole group discussions, which would be easier to fit them all if we want to do something like what [Redacted] was proposing, where we do in the morning, whole group sessions, and in the afternoon, smaller groups? What do you think, [Redacted]?

Speaker 5: Yeah, that sounds good. So, just so I've got the list right: gossip, simple taproot, jamming, dynamic commitments, and then a meta discussion are all whole group things. And then afternoon, un-conference style, we've already got some sticky notes and all of that. And then maybe at the end of each day, like 30 minutes optional wrap-up, where everyone can report back.

Speaker 0: Yeah, that sounds really good. This is going to be fun. So, what else? Is there something that people want to discuss?

Speaker 4: Oh yeah. So for Taproot, I think we wanted to go with a co-op close where the initiator says: Here's my fee and the responder has to agree. How do people feel about that?

Speaker 3: I mean, they have no ability to say no, I don't think so.

Speaker 4: Okay, yeah, I think that's what we're gonna do then.

Speaker 3: Yeah, we can't do that. I mean...

Speaker 2: You can always say: No, you just disconnect. Right?

Speaker 3: Yeah, I mean, you're just removing the explicitness of it - right? - where currently, it's the case that you can say: No, but here's my range of what I would find acceptable.

Speaker 4: Yeah, the main reason is it's kind of annoying to send nonces just to do the whole state machine thing. So, that's why.

Speaker 3: Yeah, I mean, I think you just increase the probability of a forced close, right? That nodes no longer can signal: Hey, here's the range. But you can do it without sending the nonce, right? You can just not sign in the first closing sign, send a range, and then the non-initiator can respond either with 'yes, here's the value out of your range that I'm okay with' or they can respond with 'goodbye, I'm force closing now.'

Speaker 4: Okay, so send the fee without the SIG, I guess. That also works.

Speaker 3: I mean, that's basically no different than today. It just means one more hop for the SIG. That's not a big deal.

Speaker 4: Yeah, okay. We'll go with that.

Speaker 2: I think you can ack with the value and the SIG, right? Because you need both SIGs, right? I think that works.

Speaker 3: Probably.

Speaker 2: Maybe it's premature optimization.

Speaker 0: Didn't you also have an idea on how to use interactive TX to build actually two transactions, one for each side, for the mutual close, where each side can pay the fee that they are willing to pay. So that if I want to use that fee, I'm going to build one where that fee is paid, but it's taken from my output. And if you want that fee, we're going to build one where it's taken from your output. So that in the end, we're sure that we have something that everyone is happy with.

Speaker 2: Yes, there are some subtleties But I think we did have a variant proposal where we basically end up with two closing transactions.

Speaker 0: Yeah, I don't know how painful it is to actually manage the state for something like that.

Speaker 2: I think I convinced myself it was okay. But we need to think about it again. Thanks for remembering that.

Speaker 4: Is this for Taproot? Or just in general?

Speaker 2: It was in general.

Speaker 4: We don't have interactive TX yet. So, I think the plan was to just go ahead.

Speaker 0: But even when we've added that interactive TX, something that you could do is that each side, you build two transactions where in one transaction, side A takes the fee from the output, and in transaction B, side B checks the fee from their output. But it opens up a game where you are always incentivized to let the other guy pay the fee, but if you are actually the one initiating the mutual close, maybe it's okay. You still want to pay the fee because you actually want to get your funds back instead of playing those games for only a few sats. So, I don't know how impactful that would be. If I know that if you're not happy with my fee, you are going to pay it out of your pocket. Maybe I'm just incentivized to let you do that.

Speaker 4: I don't know. I would have to think about that.

Speaker 2: Yeah, me too. But it has the no disagreement property, right? You don't care. You'll accept any fee I'm prepared to pay because why not? On the high end anyway, but then you have the game theory, I think, on the low end. It would reduce force closes, I think, is the answer. But someone really needs to think through this hard.

Speaker 4: Yeah, it seems like someone would only force close if the force close fee was higher than the co-op close fee. Is that true?

Speaker 0: Lower, you mean?

Speaker 2: No, because the force close fee is paid by one side at the moment. So, the original panel...

Speaker 4: Right. If you're the fundee, you would want the force close fee, right? And I guess, if you would always want the higher fee, maybe. If you're the fundee.

Speaker 0: The funds would be locked for a longer time. I think the main advantage of mutual close is that your funds are instantly there and the transaction is smaller.

Speaker 4: I see, yeah.

Speaker 2: Yeah, I think a blend is certainly possible, where you split some min fee and then you pay additional or something rather than be absolute one side or the other, if that improves the game theory.

Speaker 0: And also a very important advantage of mutual close is that the output that you're getting out of a mutual close - oh no. Actually, no. That's not right. Forget it.

Speaker 2: Cool, okay. Well, let's think about that because it does have nice properties. At least, to figure out to see if it's wrong. Cool. Homework for you now in New York.

Speaker 0: Yeah. Alright then. See you guys in New York. Have fun until then. Travel safe.

Speaker 2: Ciao.
