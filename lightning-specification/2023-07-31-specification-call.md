---
title: Lightning Specification Meeting - Agenda 1098
transcript_by: Gurwinder Sahota via TBTBTC v1.0.0
tags: ['lightning']
date: 2023-07-31
---

Agenda: <https://github.com/lightning/bolts/issues/1098>

Speaker 0: Great. I guess, does anyone have any urgent stuff that we want to make sure we get to in the meeting today? If not, I'm just going to go ahead and start working down the recently updated proposal seeking review list. Great. Okay. First up on the list is option simple close. This is from the summit we had a few weeks ago in July. Looks like [Redacted] and [Redacted] have commented on this and [Redacted] stuff. Does anyone have an update on this?

Speaker 1: Which one is this?

Speaker 0: This is 1296, option simple close.

Speaker 1: Yeah. I took a look at it before this. I think I just had comments in the prior one around making feature bits required versus removing stuff. Because the last commit here ends up like removing the old one entirely. It feels like we can basically do feature bit gating, and then eventually, make this required. I think the other question for this one is: What about operations wise? Do people plan implementing this before taproot channels or after? Or is it something that we'll examine and then check out and then commit to there? Because depending on that, we could modify the fields, for example. Right now, there's a signature field that's directly coded in and that could be a TLV because for taproot channels, one's a partial sig in theory, the other one is just a regular sig — partially being bigger than a regular sig because it has the non-sign attached.

Speaker 2: I think that part of the motivation for this was to provide a better close for taproot. So, I think we should assume that everyone's going to have this for taproot.

Speaker 1: Yeah, I guess I was referring more before or after. Because if we think before, then it can make sense to make this a bit more flexible. For example, make the SIG fields a TLV, and that way, you can just have the remote one optional or not, and then also you have the partial SIG there. Well, if it's after, then it's the order of operations there. Maybe it doesn't really matter as much, but it feels like if we're not coupling it as tightly, we could make certain fields TLV, mainly the signature fields, to allow — for example, right now, I think there's a bool that says: Is my SIG attached? But that could just be a different TLV field, and then you just check if that's not there or not. Or I think it's called close SIG or something like that.

Speaker 2: Personally, I don't care about TLV versus whatever, but we will probably be implementing this before taproot, or at least, it'll be a separate PR that gets merged first. Same release or not, it doesn't really matter. But I would imagine most folks aside from maybe LND will implement this pre-taproot.

Speaker 1: Gotcha. Cool. Yeah, and I think the other thing is that we're just potentially gating certain sections a bit more. But I guess the main thing is that I don't see everyone switching over to this overnight. So, it feels like it makes sense to have a feature bit, and then make that required over time versus assume people are switching over overnight and then deal with like: I guess it's removed. I was thinking about the transition basically. Right now, it defines the feature bit, but it doesn't gate any of the behavior on that feature bit, which makes it seem as though once this is ‘merged,’ this is the thing versus the negotiation to then assume that you're using this new version of it. I love the comments on there, at least. It looks like [Redacted]’s not here.

Speaker 3: Yeah, also there is also a debate about what happens if we send multiple shutdown messages with different scripts, and we discussed on the PR that — [Redacted]’s here. We discussed on the PR…

Speaker 1: We're talking about the simple close. Sorry [Redacted].

Speaker 3: Yeah, no, no. We discussed on the PR that if I send a second shutdown, I invalidate the previous one. And when we return the message from the receiver, we need to confirm the script public key where we send the closing transaction. Does it make sense also to avoid concurrency?

Speaker 4: Well, the idea is you would always send one, right? So, you send it and the answer is: It does two things. One is when you send shutdown, you need to clean up your HTLCs, blah, blah, blah, right? But assuming that that's already done, when you send it, the response is the closing message, right? So, there's always a one to one. So, we had that something in there saying you should never retransmit, but that conflicted with the requirement above that you retransmit on reconnect. So, that was a separate cleanup. You could never meet that requirement, because we said elsewhere: Hey, you're supposed to retransmit this when you reconnect. It's like: Well, you can't have both. So, the idea now is that if you reconnect again, you send shutdown again, which you're always allowed to do anyway. But it'd be nice if you could basically — because we're looking at nonces, right? You will always start doing that sequence. You will always send shutdown and start the shutdown sequence again from there, rather than just connecting and sending closing signed or something. So, if we're doing that anyway, it makes sense for you to, at that point, be able to change where your output goes to if you really want to. Basically, use the last one, the one that you're responding to, that's the one that you're going to use. Of course, modulo the checks when you receive that you check that it's if they've done an upfront shutdown key, then you fail and stuff. Sorry, the reason I was late is I was actually pushing a couple — I didn't do the TLV thing. I think it's a good idea, [Redacted]. But I was like: Let's do the minimal stuff that's obviously wrong, and then argue on the call about what do we want to do about the stupid case that will never happen, but everyone wants to bike shit over. Of like zero, like neither of us wants anything from this channel.

Speaker 1: Yeah, I didn't get that, so I didn't comment on it.

Speaker 4: Well, it's theoretically possible, right? I mean, I say: I don't care about my output and you say: I don't care about my output — then what do we do? We could say: Well, don't mutual close, you're fucked. But it's nice to clean up the UTXO set. But one option is to say: You can't omit your own if you're higher. So, one of you has to have an output and just say: You can't opt out of your output if yours is the greater output — like, you've got two output amounts. The other thing that we're thinking about is we could put more information in this so that you could do a mutual close even if you've lost your channel state.

Speaker 1: Is that like [Redacted]’s Sigash None idea thing or different?

Speaker 4: No, this is different. I mean, the thing is that we think about this recovery case, where you like you rather do a unilateral close, you might want to go to your peer and go: Hey, let's mutual close. But you don't if you've really lost your channel state — you don't know what the balances are — we could put the balances in this message, so your peer will tell you at this point: Hey, let's shut down. It sends a thing going: Yeah, let's shut down. Here's the balances. You're like: Oh, sure. Right. Okay. Fine. I'll sign off on that.

Speaker 1: And if they accept that, should they just breach anyway?

Speaker 4: Yeah, it opens a whole other can of worms. I don’t know if we want to go there, but I thought it was probably worth mentioning as a thought, right?

Speaker 1: And so, [Redacted], the other question I have on this one is that: Why doesn't this have dust rules to proceed any of this amid my output or not?  Because aren't we relying on the dust field check anywhere? Are we saying that this lets us update that after the fact, whereas right now, like it's basically hard coded — the dust values?

Speaker 4: Yeah, so the thing is that at this point, you have a lot more information, because you know exactly how much it's going to cost you to spend the output and all that stuff, because the dust field is used. One, it's static, and two, it's used fo HTLCs and all these other things. At this point, you're like: I know exactly how much it's gonna cost me to spend this output. I can exactly tell you whether or not I care about this output now. So, it kind of makes sense to just have a flag and say: Yes, I want it or not. The downside is, of course, that you can't hand your — so, because you're supposed to sign each other's — I had to add this. You can't tell them: Yes, I want my output if it's dust, because then you're handing them an output as something that won't propagate, right? So, you do have to, unfortunately, have a dust rule in here as well, which I added in a commit three minutes ago. So, it is kind of ugly, but there's a whole branch of questions. I kind of picked one in most cases, and if people have really strong opinions on what to do in these cases, I'm happy to change it. I do want to change the signatures to TLV, so we can figure out what we're going to do. I mean, we could just go: If we both don't want our outputs, I'm not going to sign it. And the UTXO just goes, stays around forever. If it's that uneconomic for both of you, no one's going to unilaterally close anyway, I guess.

Speaker 1: The other question I had, which I posed a bit for [Redacted] — alright, so right now it adds a feature bit, right? It doesn't really seem to use that feature bit. It just says: This is the way it's going to be. But like, So the question I posed to people, I think it was: Are they going to do this before or after temporary channels in turn to like actually know when this is going to be updated because otherwise, we'd basically gated everything on the feature bit existence. But if you do the feature bit, you basically do this new thing. Otherwise, you do the old thing. ‘Cause I think the old thing is going to stick around for a bit, potentially. I mean, we haven't even done theory yet, and we have a PR for it.

Speaker 4: Yeah. I mean, that's why I did it as separate commits, right? I added it, and then, in a separate commit, I removed it — depending on whether people wanted to go for modern, clean, idealized spec, or whether they wanted ugly, dirty spec that we clean up later. I don't have a huge opinion. But the transition is not going to be — I mean, I think you probably do it around the same time. It's normally kind of independent. Like it works either way.. So, it's really up to you guys, because you guys are leading on taproot. If you guys go call now, this is gonna be the only way to close on taproot, then you go: Cool, this is dependent feature. And if you've got taproot, you've got to have this; that's the only close we're going to implement, and life's a lot nicer. That implies that you're going to put a TLV in the shutdown to say: Here's your nonce or nonces, whatever we choose.

Speaker 1: That makes sense. Right now in my brain, I've just updated the close text to be RBF. I need to do that on the spec as well. I guess then we'd say: Okay, well, if you're doing taproot, we'd make this a required bit potentially. That'd be one way to enforce it there. I still probably see that. It seems pretty simple. I think I'll probably just start with a completely independent implementation and normal co-op closed down. See what that looks like. Because it's just kind of like a one-shot thing. And then it just keeps going.

Speaker 4: Yeah, I want to play with it as well. I mean, I missed the whole too small issue and stuff like that. So, you know, there's a lot more bike shit. This was supposed to be simple.

Speaker 1: What's this thing around this game theory? I haven't read the comment, but it looks like a long comment.

Speaker 4: It's like, you know, so, oh, because you're paying your own fees. You're like: Well, I really want you to close and I want you to close kind of shit. Now, the thing is that in the unilateral case, the opener is paying all the fees. So, they have an incentive to do this anyway. Now, if I really, really don't want to pay for the close, but I want a mutual close, it's simple. I just propose a fee that is below one set per byte. If I really don't want to pay fees, I propose a zero fee close, and you sign off on it. Great. Good. Right? Now, the opener is not going to propose a zero fee because that would be dumb, right? But you could totally — there's nothing in the spec that stops you doing that. If you really, really want to close, but you don't want to pay anything, propose a zero fee. Whatever. I don't care. The opener will propose a fee that's maybe de minimis, but they'll want to propagate. So, it still works. People are really upset about the game theory, but it doesn't add any new things we don't already have, where you already try to convince the peer to force close and stuff like that. I think there's no game theory-free version of closing, and so make it simple.

Speaker 1:Yeah, I need to follow up or just understand the whole op return thing a bit better as well. That's the only thing that was new to me. Or  would you just give it to miners or effectively?

Speaker 4: Yeah, I mean, it's the only way of doing it because if you both say you don't want the output, you got to have something.

Speaker 1: Oh, this is for the give up channel case.

Speaker 4: Yeah. This is where I go:I don't want my output. You go: I don't want my output either. And it's like: Okay, well, then what do we do?

Speaker 1: But I guess doesn't the practical min channel size that people seemingly have — I think ours is 20k. Maybe it's even higher.

Speaker 4: This should never happen. No one should care, everyone is stuck on it. So, there are two options. Well, there are a number of options. Looking really long-term, you're gonna want to not close this way. You're gonna want to have an option to close via splice, right? Where you splice to nothing. So, you can construct your dream transaction that does whatever crazy wild thing, right? This is not that. Right. So, people said: Oh, we should do C cache single, whatever. No, no. If you really want to construct some fancy transaction, then tack that proposal on the end of the splice stuff, and do it that way. This is simple, right? But we've got to figure out something. Now, one way is to say that whoever has the higher balance cannot omit their output, so there always has to be an output. That's simple. I don't care. No one should care. It's not gonna happen, except in test scenarios where you've opened like a 500 sat channel or something stupid.

Speaker 5: Isn't the network minimum 20K?

Speaker 2: No, there's no network minimum.

Speaker 1: Yeah, so LND has a 20k value, [Redacted].

Speaker 5: Got it. Oops.

Speaker 1: Yeah, but I was thinking in practice, because we have a 20k minimum, it probably doesn't matter. But I was just like, cover all the bases or whatever.

Speaker 4: I think we can do it on testnet.

Speaker 2: I think we have a bunch of checks, so we probably end up with an accidental minimum that's some function of fee rates, and there's probably something like that, but in practice...

Speaker 1: Or just 20k hard-coded.

Speaker 2: But even 20k. Like, fees go up a bunch. It wouldn't be hard to hit a useless channel in 20k.

Speaker 4: Yeah, but you would just lib all your fees, right? You'd be like: Well, I may want this eventually. I'll do one set per byte, right? The thing is that there's no cost, there's no — okay, other than propagation, hand wave, right? If it was min fee. But in theory, right? You close now, and your child pays for parent when you actually want to use the damn thing. It doesn't cost you anymore. It's almost always the right thing to do. I think you'll end up closing on minimum fee almost all the time; and if you want that output, that point you start paying for fees. Otherwise, you wait. Maybe there's some UX issues. People like to see things confirmed. But as far as I can tell, you want to close on a low fee enough to propagate, and if you don't want the output this week, then leave it.

Speaker 1: Yeah, I guess what's the line between like just doing a low fee or giving up explicitly, but then, will that even confirm your maybe low prioritizing? I don't know.

Speaker 4: It makes me feel good to know we're not leaving a UTXO out there that's never gonna get spent. That's why it's there. But yeah, if you're hitting this case, you're doing something wrong.

Speaker 1: Cool, okay, I'll check out the new set of stuff as well, and then think about the dependency of making the bit required, et cetera. Or, at least, assuming that for the separate stuff or not, and then probably good just to see what the nonce flow looks like as well. But it should be more or less the same. I mean, just kind of like a single shot thing, which is what we have today, where we basically just have the responder always agreeing with the initiator, and that just makes the roles explicit, you can say.

Speaker 4: Yeah, I reckon you throw two nonces in the shutdown and you use that pair. Or, we're gonna TLV this, and we may end up with not always having two things, in which case you don't use one of the nonces. That's easy, right?

Speaker 1: Yeah, they can be fully random.

Speaker 4: Yeah, let's thrash it out on issue because there's a whole heap of kind of — wow. Yeah, I think there's a lot of stuff that people want to discuss, most of which I don't think is important, but you know.

Speaker 1: Cool. Okay, I'll check that off. We've got some notes here.

Speaker 0: Ready for the next one? I mean, not that we need to introduce it, but next one up is specified behavior when a node specifies both optional and required features. [Redacted], do you want to lead this discussion?

Speaker 3: Yeah, I think it's very much CPR. Basically, with LNPrototest, I noted that we don't have any requirement if we send a feature bit as required and as an optional feature bit in the same feature set. I was thinking that we should have something because bugs can happen, right?

Speaker 1: Yeah, I don't think we ever actually rejected. It's only like the unknown required case.

Speaker 2: Correct me, I accept them. But I don't know what is the behavior with — I think, we take the required one, but I don't know. I run a couple of tests with a number of tests and with Core Lightning, both succeed. So, I mean...

Speaker 4: Yeah, if you've got the mandatory, we take that. It's undefined what happens if you set both. We kind of left that open in case we came up with some really clever thing to do with both. Like, because it's really a trinary — not there, optional or required. The fourth case is undefined. I'm happy to say: Don't do that. I think it's pretty clear that if it's mandatory, you treat it as — well, yeah, it's undefined. If we want to say, yeah, sure. Obviously, if the compulsory bit is there, you shouldn't ignore it, right? So, if you don't understand it…

Speaker 5: Yeah, I mean, you can think about optional as ‘can do’ versus the mandatory bit as ‘must do,’ and ‘must do’ will subsume ‘can do’ in every case.

Speaker 4: Yeah, exactly, which is why setting both is weird. But yeah, it's just an undefined corner.

Speaker 2: Yeah, in the PR, I define this and maybe in the — I don't know. To me, it makes sense to have this set of rules. I don't know. Maybe also it's good to catch some bugs if we set both. We can always remove it. If we think about something that can be useful to set both. Because if it's required, that can be optional for some nodes, right? So, if I know they say: Hey, I require these, you cannot say: Okay, this is optional for me. You need to specify it always.

Speaker 1: Yeah, maybe both is assumed, which I guess we'll talk about in a second here. One question not fully related to this, but like have people fully ripped out legacy onion parsing from their node? If I try to send you an onion with legacy onion parsing, do you just choke on it? Do you send back a fail? Just curious. ‘Cause I think that's really the…

Speaker 2: Choke.

Speaker 4: We bad onion it, I think.

Speaker 1: Bad onion?

Speaker 4: We get upset. We're like: What the hell is this?

Speaker 2: Same.

Speaker 1: Okay. Yeah, because we're like that.

Speaker 2: I doubt it's bad — oh, probably bad onion? I don’t know.

Speaker 1: It's either bad onion or malformed onion, whatever the name is.

Speaker 4: Yeah, it's one of those ones. Yeah.

Speaker 1: Yeah. I was curious. I think we're looking to actually remove it. I guess we can set the bit to required first, which maybe is related to the thing around the assumption stuff, which is the next thing. Okay, but so for this one, we're saying it's okay for now. We'll think about something, or do we want to have it be airtight?

Speaker 4: I'm relatively happy for it to be undefined. I'm trying to look at where we say set the feature. Generally, we say we test the feature bit, and so if they're both set, then it just kind of works, but it's kind of nice to be explicit.

Speaker 1: Yeah, whenever we do exist, we do like both versions of the bit.

Speaker 4: Yeah, we have the same kind of test, right?

Speaker 1: Yeah, but I don't think we fail if both are set. We just carry out. One of them is set. And then elsewhere, we do the unknown feature bit check.

Speaker 5: I think following the principle of being permissive with what you accept, we probably shouldn't fail if both are set as long as the rest of the semantics are congruent with the mandatory bit.

Speaker 4: Yeah. I mean, don't send it, but if someone does…

Speaker 3: The PR is not saying that we should fail. But if both are set, we take the required one. It's a pretty trivial one. So, you should do it either way, right? If I know this is required for me. Also, if I specify that this is also optional for me, it's required, right? I don't think the PR said that you should fail, but maybe wrong.

Speaker 1: Well, basically you're saying: You shouldn't set it, but you shouldn't reject it. Right now, this PR is set.

Speaker 3: If you set the receiver, need to take this like: Hey, you want this as the quad. I don't care if it's also optional. So, just in your, the optional one.

Speaker 4: Okay. So, looking through the spec briefly, we talk about rejecting evens and everything else. We never define what negotiated means, but we assume everyone knows what negotiated means. We should probably define that somewhere. When we say a feature is negotiated, which is the language we use, it means that basically, you either both set it to optional or you both set it to compulsory. You both set it — optional or compulsory, right? You don't care. But yeah, it basically implies you both set it, and therefore it's negotiated. Since that isn't defined, I think everyone is basically doing that test, but it might be good to spell it out. So, a feature is offered if whoever we're talking about has set it, either optional or compulsory; and if we both offered it, then it's negotiated. Right? So, that's the language that the spec kind of is heading towards, and maybe we should just nail that right down.

Speaker 5: Just as a quick clarification: Are all the currently deployed features strictly independent? Or do some of them imply other ones?

Speaker 4: Yeah, there's Bolt 9 actually specified.

Speaker 5: So, then presumably any mandatory feature bit can also imply mandatory all the way down the dependency stack?

Speaker 4: It could, but you don't have to. Although, presumably, everyone accepts it, right? The only difference between mandatory and optional is that if they don't understand it, they should behave differently. There's no other signaling on that. So, presumably, if you've specified a higher level one, they understand that one. Otherwise, it would have hung up on you. And so, the lesser one, who cares?

Speaker 5: Right, yeah, I guess it depends on how sort of nitpicky we want the protocol to be. But are these dependencies listed explicitly in Bolt 9?

Speaker 4: Yes.

Speaker 1: Yeah. So, every bit has something that lists dependencies, basically. We have logic for that in LND as well. It's like deps.go, I think, is where that is.

Speaker 4: It's a lot easier than trying to deal with all the test metrics of: Oh, but what if you offer this and not that and stuff like that. So, in some cases, it's just like: Be modern; offer the modern set.

Speaker 5: Yeah, I don't think it would be tremendously terrible to require a consistency in the feature bit set that you offer. Like, if you're mandatory in the downstream dependency, then you should probably be mandatory in the upstream one.

Speaker 1: I see what you're saying. You're saying require, yeah. I think you need to accept both right now.

Speaker 4: I mean, feature bits are like a really crude hammer, right? It's like literally if you don't understand this, I don't even want to talk to you, which in practice is the last stage — right — and we hit this recently because usually you're like: Well maybe I don't want to open new channels to you, but if you've got an existing channel with me, I still want to talk to you. So, really you've got to have everyone upgraded before you can really start top mandatory. The exception is if you were writing a new implementation or something and you're like: Well, I don't care about old nodes and I'm gonna be ahead of the curve, sure. But yeah, we've discovered it's a pretty crude, crude hammer.

Speaker 1:Cool.

Speaker 5: These are like node, right? Not per channel.

Speaker 1: There's different levels. There's node, init, channel update. Yeah, there's like a little column in nine that tells you where it should go basically. I-N-C or nine or something like that. I don't know exactly.

Speaker 4: Yeah.

Speaker 1: There's an invoice, their announcement and then something-something. Okay. The next one?

Speaker 0: Next one is site cleanup, removing unused features. Oh wait, did we just finish that one? You guys are like...

Speaker 1: This is related but different.

Speaker 0: Yeah, okay. So, this is removing unused features and assuming four more ones on 1092.

Speaker 1: Yeah, something we talked about just in terms of cleaning stuff up. My main thing for this is that it feels like there should be the intermediate phase of required. ‘Cause it feels like we never really did require. Looking at our bits right now, the only thing we have required is like the payment secret, or people call it in the invoice, and nothing else. For example, now we can theoretically set TLV and then payload to require in our next release, and just start there or something like that. There's probably some other ones that we can make required, like static key required, whatever else.

Speaker 4: Yeah. I wonder if we want to flip them onto required. I'll leave this on the back burner for a bit, flip them on to required. See what happens. Then, once everyone's like: No, it's required, then we go: Cool, let's just start assuming it.

Speaker 1: Yeah, exactly.

Speaker 4: That's effectively the same.

Speaker 1: Yeah, because remember one time, I think we had a bug with Eclair, where we flipped them to required basically, right? But then we had an existing channel that was legacy, so we couldn't even have a TCP connection at all with them, right? So, this could reveal other kind of edge cases there. I mean, I'm in favor of a two-phase thing. Get the required set of stuff, which should be like a pretty small change for everybody. Flip that on, and then, we can look at burying it or whatever.

Speaker 4: Yeah, it was more about which ones do we want, right?

Speaker 1: Yeah, I think this is the set that everyone does. The other thing I checked on here — I remember we talked about, [Redacted] — sort of codifying the whole thing around gossip timestamp in terms of behavior, and in terms of send me everything or don't send me anything. I don't know if there was a third one.

Speaker 4: Yes. We've implemented that, but I'm a mere suspect. Basically, zero is: Give us everything, and FFF is: Give us nothing. Then, any other number is: I'm just gonna start streaming from now on. We actually go back a little in time. We give you the last hour or something, like very rough heuristic. We go back a little bit because that's what everyone does. They either send the current time to say: Yeah, yeah, from now on I want to know, or they would want everything or they want nothing. So, or the other, the other exception is, of course, we always send you anything about our channel. So, our channel updates, we send immediately. As of this release, we're going to send you our node announcement, which we forgot to send, and that propagation sucked. But we're also going to send our peers channel update, which we didn't do. So, we'll send you all the messages we generated, but we'll also send our peers' side of the channel because that's important too. But yeah, we span that to everyone when they first connect and then, we obey whatever they ask for.

Speaker 1: Yeah, we basically use it to control where we get updated from. So, we'll like rotate and stuff like that. So, I guess, [Redacted], you're saying that, you know, collating doesn't do any backlog at all or it's just kind of like you pick the backlog size?

Speaker 4: Yeah, we do. I'll have to check. It's a couple of hours. We basically keep a trailing pointer from a while ago and we update that slowly. So no guarantees, but you'll get a little bit in the path. The idea is if you rebooted your node or something, you're really not going to miss anything.

Speaker 1: Sure, sure.

Speaker 4: This was also about banning the idea that you can ask for everything.

Speaker 1: Yeah, I realized that wasn't just deleting stuff and not necessarily the updated interpretation of what — I guess, we're, at least, restricting that somewhat.

Speaker 4: I mean, I've always thought that's reasonable, right? First time you send it, you can send zero to say: Sure, give me everything, but you can't do that again. Like whatever; you're not getting it. I'm not gonna go back and do that again. I mean, maybe. I don't know. Should we have just some general — it's just generally pretty antisocial. Like, you want them to be able to basically say: Give me all the gossip. That's probably fair, although you might wanna rate limit them.

Speaker 1: Yeah, if they're asking for it too much, then that's not good.

Speaker 4: But there's a whole heap of things they can ask for too much, right? I think we should probably need to be more general and just kind of whack this one.

Speaker 2: So, we currently do. I think we request for the first three peers we connect to, because we don't really have any idea when we last synced. I mean, we can take a guess based on the timestamps of nodes we have. But I think we shouldn't overthink this, and we shouldn't actually build a real gossip protocol, so that we can do a proper thing.

Speaker 4: Yeah. 1.5, it's coming.

Speaker 0: Should we move on to the next one? Cool. Is there any actions or items we should take from this spec cleanup stuff or is it more discussion in the paper?

Speaker 4: I think the answer is we should make all those bits compulsory and see what happens.

Speaker 1: I think it's required. Let's see what happens. And then we can say: Okay, now it's actually required. Now, we have the bid set and the network didn't explode for whatever reason.

Speaker 0: Yeah. Cool. Okay, then make a comment on that. Sounds good. So, next one is correcting the final TV for blinded paths. Basically, two PRs which both seem to build on the same prior PR, which is 1066. Are [Redacted] or [Redacted] available to talk about these?

Speaker 6: Yeah, so 1097 is mine, and it actually replaces 1066. Pretty much exactly what [Redacted]’s PR had with the update that we spoke about at the summit. So, I think if maybe [Redacted] or [Redacted] could take a look at that, it's ready to go. It's just clarifying the outgoing CLTV value for the final hop in a blinded path.

Speaker 2: So this seemed fine to me, but I'll delegate to [Redacted].

Speaker 7: I ACKed it.

Speaker 1: So, are 1097 and 1069 the same thing or different?

Speaker 6: 1069 is [Redacted]’s, and that follows up with something different.

Speaker 1: Gotcha.

Speaker 0: Does this peer require changes in what anyone has already merged for blinded path stuff? Or is this just a clarification?

Speaker 6: I believe it's just a clarification. It's definitely what Acinq is currently doing. I'm not sure about CLN, and it's what [Redacted] and [Redacted] are doing in RPRs. (around 36:10 mark)

Speaker 0: Cool.

Speaker 4: Then it's correct.

Speaker 0: Then, are we okay to apply it then? [Redacted] has approved it, it looks like [Redacted]l's approved it.

Speaker 1: Do it.

Speaker 0: Okay, cool, so I think we're good with that one then, unless there's objection? Nope? Okay, that one's ready to merge. I'm going to go ahead and merge it then. That's cool. Okay.

Speaker 1: Do it.

Speaker 0: Great. That one's in. Sick. Next up would be the clarify final CLTV computation. This is [Redacted]'s.

Speaker 7: Yeah, I still need to add a few clarifications to this one, but I should be getting to that soon.

Speaker 0: Is there anything that we wanna discuss around this one for the meeting today?

Speaker 7: I don't think so. We had some discussions at the spec meeting, but basically the PR is just regarding there's like a field in route blinding that you end up computing with Bolt 12 using the invoice expiration. So, you're kind of translating the invoice expiration into block heights, assuming 10 minute blocks. So, it's basically just clarifying that, and I just need to respond to a little bit of feedback. Sorry for the delay.

Speaker 0: No, that's cool. Okay, so the to-do on this one is a little more discussion on the PR and we should probably revisit it next meeting.

Speaker 7: Yeah, sounds good.

Speaker 0: Cool. Okay, moving onwards. Harmonize, so more CLTV stuff, but this time not for blinded paths. It's harmonizing the max CLTV expiry too far across implementations, 1086. This is from [Redacted]. [Redacted], want to lead the discussion on this one?

Speaker 1: I don't think they are here.

Speaker 0: Not on the call. Is there anyone else then that wants to lead the discussion on this?

Speaker 1: I think it's in the comments.

Speaker 2: I think it was discussed last meeting.

Speaker 1: Yeah, or look at the comments.

Speaker 0: Everyone has the same value. Yeah, that does look like what the comment says. Okay. This is proposing to change it to 4032. Everyone currently is in 2016, but this is proposing to change it to 4032.

Speaker 3: I don't think it was intended to change it. I think it was intending to standardize it, and it's just wrong.

Speaker 1: There's something that [Redacted] says was suggested to be 4032. But…

Speaker 5: Yeah, we discussed this at the last spec meeting.I think where we had landed with that we just wanted to get everybody on the same page first, and then we can talk about changing the value to a different one like a sort of subsequent discussion.

Speaker 4: Why is your magic number better than our magic number? I don't know. How do we pick?

Speaker 1: Well I mean everyone already does 2016.

Speaker 2: The discussion I recall at the last meeting was: Let's stick with what we have because everyone has the same number and not less changes. I don't think there's much left to discuss aside from the PR needs to be updated to suggest 2016.

Speaker 0: Okay, cool. Let's see, attributable errors. I don't have this one open yet. Sorry. This is from [Redacted]. Is [Redacted] on the call?

Speaker 1: I don't think so, but talking with them, and a bit more tech — I think the last thing on this was looking at changing up the HMAC or something like that. I think that was like the last thing that came out, and I think I discussed it a little bit in New York.

Speaker 2: There's some level of agreement on that, right? So, basically this is waiting for Interop.

Speaker 1: Yes, I think the PR needs updating.

Speaker 2: Yeah, PR may need to be updated. There may or may not be constant changes, but I think the next step concretely here is interop. Yeah.

Speaker 1: Yeah, and I think the only PR isn't up to date either yet. But I think [Redacted] just got the scope of clarification that you're looking for generally.

Speaker 0: Okay, so the summary is: It's awaiting interop and some proposed PR changes. Does that sound correct?

Speaker 4: Yeah, it needs an update and it needs interop. Sorry, can we jump back to 1086 for a sec? The expiry too far — the magic number. I like the idea of nailing the magic number, it is fine. I just think it's a one line change. It's not a whole new paragraph that describes a new variable that everyone needs to set with a discussion. I really think it's just where we say send this error, you say: If it's greater than 2016, send this error. Don't overcomplicate it. Just textually, I think it's a terrible change to the spec. If you read the actual PR, rather than discussion on the number, we have a section on what errors to return. Just have a thing saying: If it's greater than 2016 return this error. Done. Like, we've already got the checks laid out in requirements. This adds a whole new section with a new variable name in order to give it one number. So, anyway, I will respond on that. So, I like the idea of nailing it. I hate the idea of adding 20 new lines to do it. So, I will respond on that.

Speaker 2: Yeah, that seems reasonable.

Speaker 0: Yeah. Okay, great. Thanks, [Redacted]. That is a good general note for spec writing. Less words is better, I guess. Okay, so we talked about attributable errors. The next one on the list of what to talk about is onion messages, Bolt 7. So, adding onion message support. [Redacted], your name's at the top of it. Is there, do you want to lead this discussion?

Speaker 4: I think we have interop. Last  I knew, I think there was talk about test vectors being reproduced. Somebody want to talk?

Speaker 2: [Redacted].

Speaker 7: I wrote the test vectors for LDK. I think they could use a review glance first, which I'm still waiting on, but they're written. The values that I'm asserting on right now are just the onion messages themselves and the onion routing packet. So, not really asserting on intermediate values, but I think that's okay. But yeah, I mean.

Speaker 4: Yeah, I think it's hard to get the intermediate values wrong. The final one's correct.

Speaker 1: That's my problem with onion stuff.

Speaker4: Yeah. When it works, it works. When it doesn't, oh my god.

Speaker 7: It doesn't bad HMAC, and that's all you get.

Speaker 6: Bad HMAC. Go away.

Speaker 7: So yeah, I don't mind. I mean, I don't know what the normal protocol is if we want to wait for a review or just say that looks good.

Speaker 2: If it passes, that means our test code may need cleaning up, but at least the thing passed. So, from the spec level, it's right.

Speaker 4: Yeah, let's get together and do an interop test. Actual real interop, just to make sure that we haven't missed something stupid, [redacted]. So, we'll do that offline, and we can join some nodes together and send messages and see what happens.

Speaker 7: Awesome.

Speaker 6: Well, in the most strange interop way possible, I've used LDK to send onion messages to CLN and it works through LND, but maybe we should do a less Frankenstein-y interop.

Speaker 0: I mean, it's a good question: What counts as interop?

Speaker 5: Isn't Frankenstein-y good for interop?

Speaker 4: Yeah, weirder is better, right, surely.

Speaker 0: Okay, so what are we trying to decide on this one? Is it that we want to do more interop tests?

Speaker 4: I think we're ready.

Speaker 0: We're good? That means it can be merged, I guess. Yes? Yep. Someone who wants to work on it — want to hit the merge button?

Speaker 4: I would love to hit the merge button.

Speaker 0: This has been a very exciting meeting. Cool. Okay, so onion messages are in. Unless there's any further comments on that particular item, I'm going to mark it off and move on to the next topic, which is offers.

Speaker 4: Still waiting on me to write some test vectors. Sorry, which I will do. We have rough interop, but we should still do test vectors.

Speaker 0: Okay, so this is pending.

Speaker 8: I opened up PR too for reduced software sizes just before the meeting, so it's in the comments on the note. The meeting agenda rather.

Speaker 0: I'm sorry, I didn't catch that. Did anyone else catch the comment?

Speaker 8: Sorry. 1099.I opened just before the meeting. It's in the comments of our meeting agenda. It's to reduce the number of flights we use in blinded paths and offers. So, that's just one update.

Speaker 0: Okay So, this is an update on top of, or modification, of offers. So, taking the offer protocol and making it — sorry. Do you want to give a quick summary of what this is?

Speaker 8: Yeah, we discussed it last meeting. So I don't have much to really discuss now, but I just wanna let you all know that it's available for review.

Speaker 0: Okay, great.

Speaker 2: [Redacted] got muted in the middle of talking. I'm not sure if we muted them or why they got muted.

Speaker 8: Okay. Well, let me try it again. So, we replaced pubkeys with short channel IDs.

Speaker 0: That's a nice update, okay. That seems pretty cool. Cool, so this is open for review, and hopefully we'll have it on the docket for our next meeting.

Speaker 4:  Yeah, and I've put it on my to-do to actually implement and roll into the test vectors.

Speaker 0: Cool. Okay, so this is an update to the offers PR. I'm sorry, could someone remind me what the resolution is for 798? That's the offers PR for next one. It says I have a pending.

Speaker 4: Test vectors and this are both pending, so we won't merge it.

Speaker 0: Okay. Just reading comments all over the place. Alright.

Speaker 4: Yeah, we want 1099.

Speaker 0: Okay, I'm gonna edit. Great. Awesome, y'all. What is up next? It would be adding a dust exposure threshold. This is 919. This is also from [Redacted].

Speaker 3: [Redacted] said something about reviewing it, but all of us are reviewing.

Speaker 0: This is very old.

Speaker 1: Yeah, it's mega old. [Redacted] has looked at it. That's it. I think it's one of the things where everyone does this already, and this is about catching stuff up. It's just a matter of revisiting, but yeah, I guess it's just in this review state.

Speaker 0: Okay, looks like there's still some unaddressed comments I left two years ago about changing things where things are. Okay, there's nothing to do on that one, I guess.

Speaker 4: Do we time this one out?

Speaker 0: What does timeout mean?

Speaker 1: Well, it was worth the OP did, and then I said, should we reopen it? But we can let them timeout again.

Speaker 2: I mean, we should — even if we don't, what's the current text of it? Because the very original text of this PR was like super specific and nothing anyone wanted. If we don't land this, whoever presses the close button should, at least, add a note. There is an attack here that if you let the max dust exposure go up, you can be hurt. So, see this and do something about it. There's a lot of text here, and we could just not have all this text, and just have a much smaller thing.

Speaker 4: I think that was my thing. There was a lot of text and very little action. I like the spec to tell me what to do. Just give me a thing. Tell me where I have to check stuff and where I have to stop stuff.

Speaker 2: I would say this text does roughly that. It has five sentences and then like: Here's how you calculate your dust exposure. I guess you could leave out. Then it says: You know, if you receive a HTLC and it's high, then you have to fail the HTLC if you — I mean, I would say it is pretty prescriptive in that sense. But the question is: Do you want something super prescriptive, or do you just want to say there's an attack here, do something about it? I think that's a question for [Redacted].

Speaker 4: You always want something prescriptive, right? Hey, there's an attack over here you should also think about while you're juggling all these other things that you have to think about.

Speaker 2: Then I think we have to merge this as is basically. I don't think it's going to cut down that much.

Speaker 4: Okay, let me look at the final text. Okay, so I promise I will review this today.

Speaker 0: Okay, cool. That seems like a solid point. Should I note it on the PR?

Speaker 4: Yep.

Speaker 2: If [Redacted]’s happy with this, I'm happy to see it merged without anyone else looking at it. Do we time out the requirements for two ACKs? Can we time that out?

Speaker 0: No. Cool. Alright. So, let's keep moving then, if everyone else is okay with that. The next thing up is taproot. Extension bolt simple taproot channels, 995.

Speaker 9: I still have one PR up. I mean, it's a minor PR converting the image from Remy JS Bin. I think we should continue with just using non-sys. I think it's the easiest path forward, and we already have that.

Speaker 1: That's on my fork, right? Yeah. Okay, cool. I'll check that out. So, I'm going to have this be updated in terms of out of draft and stuff like that this week. So, I need to get this thing in there. I think there's some things around like the co-op close thing, just at least making it an RBF to start with. I just need to go through and just respond to comments generally, and implementation-wise, we're doing the last PR, which is on-chain handling — which is where a lot of stuff is different

Speaker 9: Yeah, I have a LDK PR that's kind of having some issues with lifetimes, and we have several different solutions for that. That's fun. Oh my god, it's been so fun. I'll defer to [Redacted] about telling you about all the fun because I think I've had all too much fun with that one.

Speaker 1: Cool, but I'll ping people. I guess PR, IRC, whatever else, once nothing is done. At this point, I can just get some test vectors up as well, just for the various transactions, and maybe do a new JSON vector. ‘Cause I don't think we have JSON anywhere else, right? They're just like the...

Speaker 9: No, I don't think I have seen JSON anywhere. Yeah, that’ll be good. That sounds fun.

Speaker 1: Well, no, [Redacted] added JSON for zero anchor. So, that's already there, or at least, I think that's in line. But I was looking to do that for the TX transaction stuff there too. But yeah, so generally, I'm focusing on catching up the spec this week, and just in terms of the minor changes and other things like that — say, MuSIG 1.0, etc. — and then, ideally to be out of draft this week too, which, I think, was like my thing to have test vectors on there.

Speaker 9: Okay, exciting.

Speaker 0: I have a quick question. I don't know if it's related to this, but has there been any — I know [Redacted] had an interesting proposal not to use the MuSig 2 for the commitment transactions.

Speaker 9: Yeah, that's what I was referring to. I think we should just keep using the nonces because it introduces the on-chain footprint. We do have to have some non-scanling code anyway, so it's fairly easy to reuse it for the commitments.

Speaker 2: No, isn’t it that other nonces can’t really that we have to have completely set only for shutdown, right? So, it would be very different part of the code. Certainly in LDK, it's a completely separate part of the code base.

Speaker 4: And it's transient. You never have to persist the nonce. That was the huge attraction.

Speaker 9: That is true. We never would have to persist them.

Speaker 1: This one feels late in the game. I don't know. We've been talking about MuSIG for a year.

Speaker 4: I know. [Redacted], where's your...

Speaker 1: This is making more sense with the force close. Taproot compared to regular as well because you have the extra up key, and then also the control block as well. I think people can do it.

Speaker 2: You could just force close. Isn’t that part of the reason why we're fixing the shutdown stuff to not be as force close happy?

Speaker 1: Well, I think it's just independent of it. It just feels like we felt like we were going to go all the way and stopping halfway because people had trouble implementing or don't want to. I don't really understand what the rationale was. Just not have to do the non-stuff you have to do it anyway? To me, this feels very late in the game, given when we talked about this last year, to say co-op code is different now, and then co-op code is also different. Then you have more bytes on-chain, as well as more expensive. I think once people sit down and look at the nonce stuff, it sounds scary, but I think we've slimmed it down a bunch to what it was before. Credit to [Redacted] and [Redacted] for doing the Jitnons thing and stuff like that as well. But I don't think it's as scary as people think it is.

Speaker 9: I kind of agree with [Redacted]. I think it's nice to have a smaller fucking green lateral close. I don't think the non-stop is too complicated. However, as before, I'm perfectly fine with dropping it entirely, even though it's late in the game. I think we should keep it down.

Speaker 4: That's hard because everyone else needs to look at this and go: How hard is this gonna be? Painful is this gonna be for us to implement? I like the cleanliness of doing it all, right? Taproot all the things.

Speaker 9: Well, I don't know if you can necessarily call it clean, because you could argue that not having to deal with this shit brings even more cleanliness.

Speaker 5: Well, I mean, you're going to want to reduce the chain footprint eventually, especially since a lot of the taproot rationale is to try to compress things down to these like single signatures.

Speaker 9: Right. The argument of course is that unilateral closes happen much more rarely than cooperative closes. On the other hand, if you do have a unilateral close, then you probably want to make sure that you can spend as much money as possible on fixing a fee situation. So, if the close itself takes up less weight, it's probably a big benefit. Yeah, debate.

Speaker 10: But co-op closes are also smaller, right?

Speaker 9: I'm sorry, what's smaller?

Speaker 4: Oh, yeah. Everyone wants it for co-op close. That's undeniable. We definitely want taproot for co-op close, right?

Speaker 9: Yeah, but that's not up for debate.

Speaker 4: But that's also the easy part, right? That's pretty trivial. We know how to do that.

Speaker 0: Not having to remember to actually state the nonce stuff, [Redacted] and I worked through this at the Spec Summit a few weeks ago. Removing the state requirement of adding taproot nonce negotiation for the commitment transaction — it is non-trivial, right?

Speaker 1: Well, so the thing is this isn't codified in the spec yet, but we're doing a thing where we don't have to remember anything because it's another shot chain. It's another shot chain. You can use that to drive the nonce. You have a counter already for the state. They're distinct messages. They never see your signature because it's constructed. \

Speaker 2: You have to store your counterparty's nonce, right?

Speaker 1: Well, you already need to do that — oh no, you don't need to. I'm sorry, you're right. Correct, yeah. There is that per state field now, which is just that 33 by nonce. But you're already storing. To me, it's no different than the next revocation, which we store today.

Speaker 2: We just store it once. Or we only store it for the latest state, right? Because you only need to sign the latest state.

Speaker 1: Yeah, I mean, latest state. But I guess I was drawing similarities between basically the next revocation key that we send anyway, that you also need to store. I don't know. I know people are doing remote or VFS things like that. I'm not sure what the implications are there, but to me, I don't know why we should make forced closing more expensive for the new thing, and then also have two different paths for signing updates versus closing. And it just feels late to do this.

Speaker 2: Not the other key, it's marked into the signature, right? Because you already have to store the signature for that — the counterparty signature for that state — you're just making the signature a little larger.

Speaker 1: Yeah, so for us, we basically serialize the SIG and their nonce alongside of it, right? So, this is like the partial sig with nonce thing. So we store that, and it is a bit more there, but you can say less on-chain generally. If people like this direction because they wanna do an explicit threshold thing, that's something else, I guess. If the whole FROST thing was too complex, something like that, that's something else, and that feels like it can be done. But to me, it feels late to try to add co-op close and make that distinct here. And it's just more bytes on-chain. And now you have two different paths as well.

Speaker 2: That's an interesting point. It makes the FROST stuff way simpler.

Speaker 0: Is this something that you could add…

Speaker 1: It feels like people were discouraged about FROST, but they haven't fully given up there. So, I don't know if they’re still investigating that. There is just like the check SIG add thing as well. I think one of the things because Gossip 1.75 — or we're calling it like now, just say it's a pubkey — means you can do whatever you want to, right? Where before it maybe would sort of prescribe MuSIG 2. Now, you can have a script path that has 20 signers if you want to, right? And that's not enforced on the gossip layer anymore, but then you would need to define all of that for that channel type, which you can do because it's a length level thing. And hey, there's gonna be more channel types in the future anyway, so yeah.

Speaker 0: I mean, would it make sense to make this like just a different channel type then? Like, there's an option to do commitment transactions without the nonces. I guess then you get the: Who's supporting it? It's probably better to have a single.

Speaker 5: That’s going to make it more complicated.

Speaker 9:  Yeah, you get an N squared problem.

Speaker 1: Well, yeah, I mean, if whoever wants to take it all the way and actually implement it, then it's there. But then the question is: Do people really want to have the two versions too? Where there's some new stuff, and, at least, it seems like the libraries upstream, like ZP and things like that, are giving you that stuff, and you can use ZKP otherwise. But generally, what we're spending time in the PR review now is basically all the on-chain stuff. The funding and the statement itself was relatively contained because it just piggybacked onto everything, and you basically encapsulated the MuSIG 2 stuff on the side. But I guess the thing is, until we get farther, you can't really internalize what it's like versus this or not, right?

Speaker 9: Yeah, I do want to say, though, that if people want to use a non-sluss scheme in order to be able to use FROST more easily, that's a disadvantage because then that leaks that you are probably interested in that because they have some different signer setup. So...

Speaker 2: Right, in order to...

Speaker 1: Yeah, it's not clear that you can not leak. Unless you warn everybody.

Speaker 2: Right, but I think that's...

Speaker 9: Yeah, so everybody has to be the same for a maximal anonymity set.

Speaker 2: Right, so that would be a very strong reason to do the non-spaced version.

Speaker 9: Yeah, assuming we can figure out FROST 4, but that doesn't sound in MuSIG 2.

Speaker 2: Right. I think that'd be a really strong argument for doing that for everyone.

Speaker 1: Yeah. Doing what for everyone?

Speaker 9: Nonce analysis.

Speaker 1: But, I mean, are we over-indexing the FROST case, right? Are people actually ready for that on a large scale and Robono is going to be doing it? Or, how many writers are actually going to be doing it? Should we really burden everything?

Speaker 2: I don't think it's going to be common, but I think it will. I think, as we figured out more and more pieces to it, I think people are becoming much more ready for it.

Speaker 1: Yeah, its not that you can't do it. It's just that the existing model maybe didn't fit a hundred percent, but it's still possible if you're willing to expand your model of the single signers or whatever.

Speaker 2: What do you mean? No, you need, with the current taproot thing, you need FROST in MuSIG 2, right?

Speaker 1: Well, I was talking about like the whole like three, four thing that it's not that it's not possible — it's that the parameters have changed basically, or there's some additional parameters you need to consider that maybe people hadn't really thought of in the past, which was the threshold number on the FROST level and the fault tolerance level.

Speaker 2: Yeah, but now that there's been some additional thinking there, I think it's the clarity in terms of whether this is possible is much better. I think by far the largest question is: Can you do a FROST in MuSIG? Or: At what point would FROST in MuSIG be something that you could reliably do and consider secure?

Speaker 1: Ah, and you're talking about nested MuSIG with one of them being FROST basically.

Speaker 2: Right, because that's what you would need to do if you did not do the nonce. If you did the non-nonce version, you just need FROST, and I think that's much clearer.

Speaker 1: And non-nonce being basically checksick checksick, right?

Speaker 9:  Yeah. The thing is, we have been looking into the whole nested FROST thing, and every time we're looking into it, there is something else that we notice; and then something that we realized we had overlooked; and then something where we think: Oh, actually, it's not as bad as we thought it was. So, it would be nice to have some sort of concreteness from the academic side of the Bitcoin developer community to know what is and isn't possible. Like, are we shooting ourselves in the foot if we decide not to do the no-nonce thing?

Speaker 1: Well, the thing is, I feel like at the end of the day, FROST is MPC, and MPC implies sheer bit systems, and sheer systems are hard. So, try to get away from the complexity of the scheme itself.

Speaker 2: FROST itself is relatively better understood in terms of design.

Speaker 1: Yeah, I mean, there’s FROST: the crypto protocol, and then FROST: the stuff that implements it basically, right? Like the wrap around, where you have to talk to a network.

Speaker 2: I think the implementing part, at least, I think there's some level of confidence that that's doable. The nested part is the — we don't even know if this is possible without adding multiple rounds and additional massive leakage. Right, so I think that's that's the…

Speaker 0: We are overtime by 10 minutes. If people want to keep talking, I'm definitely down to keep chatting. But if that.

Speaker 2: [Redacted] has been sitting here, smacking their head for the last 10 minutes.

Speaker 4: No, no. Look, I'm loving this conversation. I did want to note that we looked at nested MuSIG for the gossip stuff, where you go: Oh, actually, because we're signed with a taproot key, and we want to sign with two node keys, and can we do this? I'm leaning towards a hybrid at the moment, where if you've got one SIG, that means: Okay, I have signed the whole thing with three keys — the taproot internal key and the two node keys — and I've managed to do that. If you've got two, it means: Well, one of them's just, this is signed by the taproot key, and this is signed by the node keys. So, you don't have to do nested FROST if you can't do that. But if you manage to do that in future, then — because the verification side is trivial, right? Validation signature, well, it's signed by all three. That's great. How do you produce that? So, we're probably going to have to do some awkward hybrid thing. They talked about half-aggregation, which is much easier, but I'm still holding out hope that we will end up with nested FROST SIG Mu-Sig — that this Franken creature will come to life, and we will get down to a single signature. So, even though it's gossip and we care about bytes, I'm tempted to not go for half aggregation and go for either two SIGs or one SIG.

Speaker 2: On this. I did go back and forth a little bit after the last meeting with [Redacted], I think. [Redacted] pointed out you don't really gain anything if we get that hybrid creature actually, because the verification time is basically the same. It's all just adding the pubkey anyway. Might save a single operation.

Speaker 4: It's size.

Speaker 1: Yeah, it's more about the signer being able to do it in the future, right? Verifier is more or less the same. It's like when the standard figures are out.

Speaker 2: The performance of the verifier is not substantially different is the point. You just save the extra bytes of the extra signature.

Speaker 4: Yep, yeah. Cutting from two signatures to one is better. Yeah, but it's gossip, right? The tighter we can make gossip, the better, always, right?

Speaker 1: Yeah, and I don't think [Redacted]’s updated the PR yet, but my thing is what they’re talking about here, as far as letting FROST exist or nested in the future basically, but then, have the verifier be able to understand whatever. That just gives us time to figure it out. If we do, whatever.

Speaker 4: I think that's where we ended up. But yeah, go beat up an academic and get them to implement nested FROST MuSIG today.

Speaker 1: Yeah, I partially implemented nested MuSIG, but this is before 1.0 — and there's like another like parity factor or whatever that kind of messed it up. I probably just need to revisit it. But I mean, I maybe have to do it, but I guess the question: Do they think we should do it? Alright, so that's the ‘is it possible versus is it secure’? That's how I see different questions.

Speaker 2: So, that was not really a conclusion at all to the taproot thing. The problem is we really should decide this cause to [Redacted]’s point, it's getting late in the game. So it would be nice to have a concrete conclusion.

Speaker 1: If people want to add the bit and then define it, I think they can. And you know that obviously requires other people to do it too.

Speaker 2: I assume, at this point, that LND will ship with nonces because you guys have already written the code. That is a very separate question from: Will others ship with the same? I mean, similar to what we ended up with anchors because people shipped quick, there ended up being two different variants of anchors, and we're only just now getting that fixed. Right?

Speaker 4: So that's one question. I need to write up. Do you want me to write up the nonce thing? Because I think I talked about the recognition. We said: Okay, well we won't prescribe it basically, but we can say: People, you should have a new nonce, right? Should I write up the nonce thing and more details in the end.

Speaker 2: Frankly, personally, I was totally fine with the nonce thing until you brought up the multi-SIG question, and I'm like: Oh shit actually maybe this makes more sense.

Speaker 0: Well, just have multiple phones, right?

Speaker 3: Four different lighting channels, it's fine. Yeah, I mean, I'm okay with taking that down the road. I assume people — at least, you and probably maybe even us — will ship with nonces because you've already written it and [Redacted] already written some stuff. But that's different from what other people implement in V1 and what goes in the Bolts, right? Because, at least, the conversion between the two of them will be really kind of trivial. Having a feature that is supporting both is not really hard.

Speaker 1: But okay, I guess is there any direct soul searching that needs to happen on this front?

Speaker 0: I mean, I feel like it's like Core Lightning hasn't implemented anything for taproot yet, right? So like, as like a new implementer, it's like: Okay, we want to do what we think is going to be like the best thing for the spec, right? So ignore — we clearly don't have the history or any of the code that we would have to change. It's all greenfield to some extent, right? So for us, it's like: Okay, what is going to be, what do we think is, what shuffles have already been put in the ground, what is the best implementation, when not with compatibility, right? So, I'm not really sure what the answer is. Maybe we should have another discussion about this next meeting around it after — definitely over time here…

Speaker 2: I just feel bad kicking it to the next one because then it's just going to be: Well, we've already shipped the code, instead of: Well, we're about to ship the code.

Speaker 0: That makes sense. I mean, I definitely worked on spec stuff that had to get changed after it got shipped. I think all of us probably have. So, I don't really feel that one. I mean, from a design perspective though, what are our design goals?

Speaker 1: My initial goal was MuSIG minimally everywhere, which is what led to state machine and code close being MuSIG. That also coincided with reducing on-chain fees whenever possible. There are some cases in the new one, where things end up being a script path because anchors, other things like that. But, at least, my initial goal was like MuSIG everywhere, minimal chain footprint test stuff for BTLC stuff, and sort of like de-risk MuSIG stuff in general, in terms of knowing how it works and other edge cases and stuff at least. But if we're changing that to support more multi-SIG thresholds or something like that, then it's separate. I guess the other thing is wouldn't the whole thing around allowing arbitrary multi-SIG threshold also lead into the whole mini-SHA chain thing, which doesn't seem to have been figured out fully yet?

Speaker 2: I think that has been figured out fully. I'm sorry. I don’t know if I posted it on IRC, but we did get a general solution.

Speaker 4: Did you get all the numbers? Like, how many do we need? Is eight the right number? Okay.

Speaker 2: I think 10 is the right number because if you want to do five of seven, it blows up to huge, but 10 gets you three of five.

Speaker 4: Okay.

Speaker 1: So, that's everyone always send and process 10 SHA chain things.

Speaker 2: Basically.

Speaker 4: Sure.

Speaker 1: I guess one part of me  feels like we're really impacting the protocol for what seems to be a rare case that people like, but it's unclear how widespread it will be. I mean, because are you really going to have five different nodes? Or where are they? Like latency stuff?

Speaker 8: Well, if it's not going to be supported, it's obviously not going to be widespread at all.

Speaker 1: Well, but I just mean the burden of everyone having to always do the 10, right? If you want to have an empty set hand wave.

Speaker 4: It's pretty easy. I mean, Modulo haven't actually implemented it yet, but I mean, it's pretty easy to implement. It's going to be trivial. We'll probably just, by default, tweak the SHA chain thing to get nine more secrets out of it, and then just…

Speaker 0:  I just posted a quick question in the chat about — How much does ease of VLS support way, and do they like the design of the protocol? I don't know how easy to SHA chain stuff really easy to implement or add to the VLS stuff, but maybe something

Speaker 4:  I think it will be trivial for them. I mean, it's pretty efficient and they will do, at least, if they're doing single signer and they're not trying to do this advanced — we've actually got multiple signers, doing multi-SHA chain is really trivial.

Speaker 1: Yeah, ‘cause also I'm not sure if VLS has any MuSIG 2 partial SIG API stuff at all, which they would need, right? So, I think that's like a whole ‘nother thing they need to figure out in their model on top of — either way, potentially, even if the co-op close versus not. I'm looking at — they have like a state struct that I guess would have this too. But yeah, I guess we can ask them how they thought about that MuSIG 2  in general.

Speaker 4: Yeah, I don't think it's going to make a big difference for them, to be honest. Oh, maybe they care about nonces.

Speaker 1: Yeah, it's a question of whether they want to do the new nonce thing or not. They do have that extra bit of state they need to store, which is alongside the signature really. And they're doing that verification, but I guess we can ask them about it. I guess, at least the social thing stuff here is: See what VLS thinks and then, Core Lightning, size up the impact or something.

Speaker 4: I will hand that to [Redacted].

Speaker 2: Oh gosh. So I'll do that...

Speaker 4: I'll do multi-SHA chain. How's that?

Speaker 2: I can ask the VLS folks to join next week, and think about this beforehand if that's helpful.

Speaker 4: Maybe get them to join in two weeks, that way we'll be here.

Speaker 2: Yeah. I won't be. I'm off next Monday, too. So, I also won't be here.

Speaker 1: Cool, okay, alright, so we at least have cell search and action items, and then them being there as well. I'll write the thingy up, just at the end and add it to the spec. Maybe it's clearer when it's just there, and it should be there anyway. We can just say: Hey, this is an optional thing if you want to do this. Otherwise, the nonce should be random. Figure that out.

Speaker 4: Yep.

Speaker 1: Cool. Okay. I mean, and it can be pretty short as well, because at least, we're doing this. I mean, I guess when people want me to prescribe the SHA chain thing we're doing right now, or just say: You can do a counter thing.

Speaker 4: Yeah, no, might as well describe it. Here's a scheme because that's always saves me thinking, right?

Speaker 0: The SHA chain thing is more on the…

Speaker 1: There's two SHA chain things. One is the 10 SHA chain. The other is another SHA chain that generates your nonce.


Speaker 0: The SHA chain side is on the generation stuff, not the storage side, right? So, it's more like — I mean, I feel like whenever we're looking at those, and it's been a few weeks, the bigger thing wasn't on picking your nonce. Picking a nonce to send is on the SHA chain side, right? It's more the needing to remember and store and keep these extra stuff around. You either have to store the nonce from your partner now or the... .

Speaker 4: Well, [Redacted] was saying, I think, that the requirements for nonce storage are the same as requirements for signature storage. So, if you treat it as like it’s a partial signature – which is kind of what you do now — you keep their signature. You keep their signature in the nonce, so that you can make your signature.

Speaker 1: Correct, right? And so…

Speaker 4: It doesn't seem like a stretch.

Speaker 1: Yeah. Otherwise, if you don't do counter-based, you would need to remember the non-state you sent so you can force close, right? So now, your minimal force close state is their signature and that as well. You can serialize it, and that's fine. But okay, but I think it just tells me I can just add some more section in the spec around just the requirements. If that's not clear, then also specify the scheme and just make it clear — what you need to store and what you can get away from not storing and so forth. But yeah, in the minimal sense, it's no different than today. You just have their nonce and a signature alongside of it, which you need to do the combined thing anyway.

Speaker 0: Yeah, okay. That sounds good.

Speaker 1: Okay. Cool. Alright. I got to hop off. But a productive meeting. See you all on my interesting stuff. Bye.

Speaker 9: Yeah. See you.

Speaker 1: Thanks so much.

Speaker 9: That was really helpful.

Speaker 2: Cheers. Thanks, everyone. Bye.

