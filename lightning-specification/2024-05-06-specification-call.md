---
title: "Lightning Specification Meeting - Agenda 1161"
transcript_by: Gurwinder Sahota via tstbtc v1.0.0
tags: ['lightning']
speakers: []
date: 2024-05-06
---

Agenda: <https://github.com/lightning/bolts/issues/1161> 

Speaker 0: So the next one is go see 12-blocks delay channel closed follow-up. So, this is something we already merged something to a spec, saying that whenever you see a channel being spent on-chain, you should wait for 12 blocks to allow splicing to happen. It's just one line that was missing in the requirement, and then they found it in the older splicing PR. So, there's already three ACKs. So, is anyone opposed to just merging that?

Speaker 0: Perfect. So unless someone screams before tomorrow, I'll just merge that one tomorrow. Then, the next one is constant size failure on decryption. I understand that this was a topic that was covered in the last spec meeting, but it doesn't seem like it's merged or removed. 

Speaker 2: I think there was a little bit of agreement last spec meeting to suggest that this be rewritten as a more general — you should try to avoid being fingerprintable as to whether or not you were the sender based on externally visible timing and that kind of thing rather than trying to be super specific here. But it looks like that didn't happen.

Speaker 0: Okay. That sounds reasonable. So, we should not merge it as is right now. We should just wait for it to be updated and more general. Okay. Sounds good.

Speaker 2: I might be making that up, but I think that's what I remember from two weeks ago.

Speaker 3: That's what I remember as well. 

Speaker 0: Okay. I'll add a comment directly on the PR so that the author can update it. Alright. The next one is an update to a notation for math content. Oh, perfect, [redacted]. Right on time. We're talking about 1158, which is a follow up on the PR you mentioned about using math content notation. There are some things that are not rendering correctly, so someone came and started fixing them. So could you just have a look at it and ACK it if it looks good to you.

Speaker 4: Sure. What's the number?

Speaker 0: 1158. 

Speaker 4: Oh, cool. Okay.

Speaker 0: Alright. So just have a good look at it. Some of the things were not, at least for me, were not rendering correctly in the markdown. Now they are. There's only one remaining. But apart from that, it looks like it's okay.

Speaker 4: Yeah, I can have a look at this.

Speaker 0: Even though I find it quite a bit more painful to write, do you still write it? Because seeing this, reviewing the diff in plain text is horrible. So you have to just look at the render thing and it's kind of hard jumping between one and the other. Was it hard writing it down?

Speaker 4: The thing is, I think, for those that have written a lot of LaTeX, you basically compile it with your eyes. You know what I mean? But I think if you're not used to all of the random dollar signs and stuff like that, it is a little bit more difficult. But yeah, that is somewhat of a trade-off, I guess, in that once you're used to it, you can look at this and know if it's doing the right thing, but otherwise,  you need to just sort of rely on the rendered version. 

Speaker 0: Okay.

Speaker 3: I think it makes the spec itself easier to read and it makes the diffs way harder to read.

Speaker 0: Exactly. So that's probably a good trade-off. More people read the spec than review it.

Speaker 4: Yeah, and for this one, I think it's still stuff where you need to basically do dollar sign backtick basically. In some areas I did backtick dollar sign because backtick is like a reflex for doing any markdown code stuff anyway. 

Speaker 0: Okay. Alright. Sounds good. So just have a look at it. Once you ACK  it and the last comments are fixed, I guess we can merge it.

Speaker 4: Sounds easy.

Speaker 0: Yeah. So the next step is [redacted] making the channel update in onion errors optional. It's something we've been talking about a lot, but no one really bothered to open a spec PR because it's just a chore and it's annoying, but I think we should definitely do it and this is already happening on the network.

Speaker 4: What's the rationale here? I guess you're saying that fingerprint vulnerabilities, like when they shouldn't broadcast it. Was it a private channel or something?

Speaker 2: No. Previously, like six months ago and several spec calls in a row, [redacted] pointed out that if you receive an HTLC and then you send back a unique channel update to that peer, it will be in their gossip store. Then, you can query them for whether it's in their gossip store and then, you can identify who sent that specific HTLC. This updates the spec to say: You must ignore it if you see it and also, you should no longer require that it be there with the intention that nodes will eventually just start removing it.

Speaker 4: But if you ignore it, that sort of — I mean, it does have a purpose, right? The purpose is basically giving you the most up-to-date channel update whereas in the past — this basically lets you not have to sync all of gossip because you get the new stuff that you need when you try to, and you feel alright.

Speaker 2: No. You should never be relying on this. Frankly, the update in the onion error should never have been used to begin with because if you send a new fee rate, then you shouldn't be applying it for quite some time. I forget what the recommendation is, but it's a while. It's like tens of minutes or something, and by that point, everyone should have…

Speaker 4: Does anyone actually do that?

Speaker 2: Yeah, absolutely. 

Speaker 4: Okay. Well, I mean, so what we do is we shift that to happen basically. We'll do a thing where we'll give an individual another chance. Basically, send us a new update before saying: Okay, well, I think it's whack or not doing it. But I do think it has a role. The role is that you don't need to sync a lot of gossip. You can just basically get the stuff at runtime, but I realized this privacy issue here.

Speaker 2: I mean, getting in a runtime is also really shitty. People don't like payments that are really slow, and if you wait…

Speaker 1: Well I guess the difference is that if you don't apply this on runtime you're potentially permanently failing a route because you don't have the latest thing, right? So, it's actually going to help to improve payment UX, right? Because now you can get the new value and try versus just saying: I'm giving up until gossip happens — which can be hours, right?

Speaker 2: Well, gossip's not hours. What?

Speaker 4: I mean, just depending, right? I mean, I don't know if anyone's measured the propagation speed, but that's just to say that…

Speaker 2: People have,

Speaker 4: It is a UX optimization. ‘Cause otherwise, if you don't get this new value, I mean, I think it matters more for — but do you…

Speaker 2: What do you do with the value currently? Do you actually apply it to your gossip store so you're vulnerable to the fingerprinting?

Speaker 4: So today, well, no. So, we won't apply it to gossip store. We'll apply it to that session basically. In that we'll apply it in memory, that's to say. So, we'll get the new thing; we'll buy it in memory; we'll try it again. Then, we have something called second-hand logic, which I think we took out of now, but otherwise, we will wait for that thing to come back again. Right now, we'll apply it in memory, which is useful because then, we can just try again.

Speaker 2: To be clear, you apply it just for that payment session, right? So just for that payment, you'll recalculate the route. And if you happen to decide to use the same channel, you'll try that one.

Speaker 4: Yep. Many times, you do actually retry again successfully because this is the thing that you're missing. So I see why we should discourage it, but I think removing it altogether would hamper UX.

Speaker 2: So it's worth pointing out that becomes a privacy issue with PTLCs, right? Because you don't want to indicate to someone that you're actually retrying the same HTLC, potentially. Separately, I'm curious if you could go take a look at cases where this actually kicks in. I imagine it's basically just right on startup, right? Like, the only time you're ever actually out of sync with gossip enough that someone's sending a new gossip update causes payments to fail should just be on startup.

Speaker 4: Well, I think it's different, right? I think your model is that they're using RGS to always get the latest gossip when they come up as a mobile node. But our model is instead that they'll get the latest update when they actually need to do so because we don't really aggressively think of the gossip network, and we don't have a built-in RGS type thing being bundled into the…

Speaker 2: So you mean specifically on mobile nodes? Not…

Speaker 4: Yeah, exactly. I think on server, you're online enough that you should have the latest stuff like you're saying. But I think on mobile it's a bit different if you're not using a fast gossip download type of thing. Assuming that you have all the latest.

Speaker 2: So that affects what, just Zeus? Is that the only major…?

Speaker 4: I guess Zeus. Breeze. Blixt. Whatever the other ones. 

Speaker 2: Breeze is moving off.

Speaker 4: They've been saying that for a while, but they're still here, I guess.

Speaker 2: Yeah. They have been saying that for a while. 

Speaker 4: I remember when Blue Wallet moved out, but then they don't really exist anywhere, right?

Speaker 2: Right. What was I going to say? Maybe we should have a conversation with those wallets about doing something more intelligent with gossip because this can cause lots of additional payment latency for them, right?

Speaker 4: Well, I think the difference is that obviously, syncing the gossip every single time does add additional costs to the node or to the implementation basically. But I think we do have a lot of security UX trade-offs in the protocol generally. This is yet another one basically. I think we should think about: Do we really want to just disallow this altogether? — which I think was a useful thing for particular payment latency — Or advise implementations what to do about it?  And can we mitigate that fingerprinting thing somewhat?

Speaker 2: It seems like the only thing you can do is either. — so it seems like we agree that this is totally not useful for non-mobile nodes, and if we had no mobile nodes relying on peer-to-peer gossip, we would just drop this entirely. So given that, for mobile nodes, if you're particularly behind on gossip, it seems like you're just going to have a lot of payments that are going to hit this all the time. You're just going to have a ton of round trips, which doesn't seem super great either, but maybe you hit this once while you're waiting for gossip to sync. It's not clear to me what the — you're telling me that there's these mobile nodes out there that startup, don't really sync gossip, send the payment…

Speaker 4: Well, it's not that... 

Speaker 2: …One channel on their path.

Speaker 4: Well, the thing is they'll get the channel updates, but they're not trying to sink whatever 50,000 gossip changes that may have happened while they're offline, right? I think you should also compare it to they may already encounter a failure due to whatever other issues basically. Which one dominates? Is it going to be the failure due to them not having the latest update or just everything else that can go wrong along the way? So, it's one of the two things. My intuition is that the latte. The second one is what matters more. Basically, just random failures that happen versus this particular case. Because I'm assuming people are going through similar nodes anyway, right? If they have those set of 20 updates versus out of the 50,000, they have a pretty good experience.

Speaker 3: Yeah, I think it comes down to how fast you can sync the unsynced gossip.

Speaker 4: If you have one of these third party servers, it's very fast. If you don't, it takes more time because in the past, people would do the complete backlog, which wasn't great because you would just send all this data over the entire time and try to validate it all. Now, we do have the go back 24 hours or whatever, but that doesn't cover everything. If you want to cover everything, you either need to do that all the time, or do one of these rapid gossip things, or handwave mini-sketch something.

Speaker 2: Right, but if you go back a ways, you should hit everything basically. I'm confused why you have this problem to begin with.

Speaker 4: So, the thing is we stopped doing the backlog altogether. In the beginning, everyone did the backlog the entire time. You just sync the entire graph whenever you reconnect. But now, the thing is, if you're reconnecting every single time, you're getting that particular backlog. We just eliminated it because it was just flappy, and it would just cause a bunch of CPU, and it was just unnecessary. What we do is: We basically have three or eight peers or whatever; we only enable active gossip on those three peers. But we will periodically do the full channel range thing to basically spot check: Do we miss any new channels? But otherwise, when we reconnect, we're not asking for any sort of backlog at all.

Speaker 2: When you reconnect or when you startup?

Speaker 4: Both. They're basically the same for us in this context.

Speaker 2: That's why gossip's unreliable — okay.

Speaker 4: Well, I mean, the thing is for the routing nodes, they're gonna be getting those messages anyway  because you also are retransmitting your own messages. But also there is rate limiting that everyone does as well, right? I guess a question for you all: If you're not using RGS, what's the backlog that you ask for?  And I guess for Phoenix as well.

Speaker 2: On startup, the first three peers we talk to, we do a full graph sync, and then we just listen to the live updates from everybody.

Speaker 4: Isn't that the same way I just described? So, full graph sync is using the channel height range and not doing a backlog for...

Speaker 2: No, including backlog. Like, we download everything.

Speaker 4: Oh, so you redownload the entire channel on startup, basically. 

Speaker 2: The first three peers we talk to. Because you have to if you actually care if a node generates a gossip update that has a timestamp that's a little old, that's the only way to make sure you get it. Because the gossip sync stuff uses the timestamp and the message rather than the timestamp you received it.

Speaker 4: Yeah, I think that's where our model differs. On startup, you download the entire graph. We say we don't need to download it because if we're using that particular edge, we'll get this new update, apply it, and can just focus on the channel that we use versus the 90% that we'll never touch.

Speaker 2: But if there's some channel that you happen to not get an update for, that means every time you start off — like every time you try to send a payment — you're going to hit the first payment attempt is going to fail, and you're going to have to retry it.

Speaker 4: Well, that's either if we hear about it or not. 

Speaker 2: What?

Speaker 4: I mean, the question is: Do we hear about it later on or not basically, right?

Speaker 2: Sure, but you were telling me you were mostly worried about this for mobile nodes, and they're not going to hear about it later. They're not online long enough to hear about anything.

Speaker 4: Well, I guess what I'm trying to say is that this is a class of failure that can happen. By including the channel update, you basically allow individuals to recover from this type of failure, whereas otherwise they wouldn't be able to recover at all. There are other types of failures that can happen. Nodes being offline, channels being down, disabled...

Speaker 2: Only kind of, right? I thought we agreed that this is not the kind of failure we expect for any node that's online all the time, like any regular merging or whatever.

Speaker 4: Yeah, it's for nodes that aren't aggressively syncing channel updates, basically.

Speaker 2: Well, I thought we agreed that this is mostly like mobile node setups, right?

Speaker 4: Yeah, and to me, a mobile node is a node that doesn't necessarily care about syncing aggressively syncing channel updates, basically. 

Speaker 2: Right. Fair enough. 

Speaker 4: Because they're only going through a small portion of the network anyway, right? So why sync everything? That's my view at least.

Speaker 2: No, I mean, fine. My understanding of your model is they're not going to sync anything, right? They're going to sync stuff as it comes in.

Speaker 4: We sync new channels, yeah. We sync new channels and then, get the rest as it comes in. And then, on demand if there's something that we never heard of that is still new, we'll hear about it through the error.

Speaker 2: If somebody tries to pay somebody regularly, they're just going to hit this every single time they try to pay them, right?

Speaker 4: Not necessarily. If they hear…

Speaker 3: Why would that be the case? Would a new edge be applied? Wouldn't a new edge be applied when it actually hears about it?

Speaker 2: Well, it's a mobile node, right? It's online for a minute at a time once a day, so it never is going to really see stuff for the most part.

Speaker 3: And we don't currently commit the edge to the actual graph because of this attack, right?

Speaker 4: I checked last time, and it's just in the session. I can check again.

Speaker 3: I think that's right, is that we would hit it every single time.

Speaker 2: I'm going to do some loud, clacky stuff now. But I guess, [redacted], how's Eclair into this? I'm guessing you guys do some RGS type of thing, basically? Or I guess because it's Trampoline, they don't need to worry about that anyway?

Speaker 0: Exactly. For Phoenix, since we use Trampoline, we don't worry about gossip at all. We don't do any gossip.

Speaker 2: I didn't feel — I thought Zeus shipped some other gossip scheme that was not peer-to-peer because they had some issues with the peer-to-peer stuff being so slow.

Speaker 4: Correct. I think what they do, I think Blixt does it as well, where basically they'll do a fast channel graph import to bootstrap, but I don't think they spot check. So, I think they let people basically skip downloading from P2P because they download a snapshot that goes directly into the DB, but I don't think they do a on startup spot check. Let me see what the new channel graph thingy is.

Speaker 2: Right. So they're basically doing RGS, but via different format.

Speaker 4: They're doing RGS, but only for initial bootstrap. They don't do a spot check.

Speaker 2: Do they not redownload? Like, they installed the wallet six months ago, they've opened it once a week for a minute. Never really done any peer-to-peer graph sync. Do they like re-download it at some point, or do they just let it get progressively more and more stale?

Speaker 4: I don't think they re-download it, but I'd have to check. I'm pretty sure Blixt doesn't re-download it. For Zeus, maybe they do, but I know they were collaborating on a fast channel graph loading that was somewhat LND specific.

Speaker 2: Alright. So how about I chat with [redacted] at some point then, and we come back to this next meeting. Because it seems like if Zeus and Blixt are doing something else, then we don't really need to care about this and we can drop this. If they're not doing something else, then we can revisit whether this makes sense.

Speaker 0: Anyway, if we take a step back, it at least makes sense to update the spec to say that the channel update is not mandatory anymore but optional because it's already the case that some nodes just do not include it because of plugins on different implementations. I think it was…

Speaker 2: Or Lightning has had a bug for a while that they don't include it. I don't remember why. I don't think I ever got debugged.

Speaker 4: But I think that makes sense [redacted], right? I think we do it in two steps. We can say it's optional now and then remove it later. When we talk to the other one, it's like: Well, it's already optional as is.

Speaker 0: Yeah. We should really say that it's optional because it's what actually happens on the network right now, so people need to allow reading such an amount that doesn't contain a channel update.

Speaker 2: Well, there's nothing in this PR right now at all that says anything about suggesting not including it. It just says that you have to ignore it if it's there. LND can choose to do something else for its payment sessions, but...

Speaker 4: No. The thing is it does remove the section on should you use the new channel update or not, right? If you look at the line 1402...

Speaker 2: Right, because the section on using the new channel update says you should broadcast it and you should apply it generically, which you definitely should not do. I don't think anyone does anymore.

Speaker 0: Yeah, we changed that.

Speaker 4: I mean, I guess we should see what CLN does here as well, but it seems like we can at least do the language to stamp it that's optional and then look at this later. Because I think clearly it's like a private security trade-off, but we should just make sure we’re making conscious decisions here and not degrading UX in this way. We've done this for a long time now and we haven't had any complaints about it either.

Speaker 2: I'll share with [redacted] and see what they have to say about what Zeus currently does and whether this impacts what they do. If they say it doesn't impact them at all and they don't think it impacts Blixt, it sounds like we would all probably be on the same page that we should just go ahead and drop it.

Speaker 0: Alright. Should we move on to BOLT 12? Okay. So in BOLT 12, there were some latest changes to the specification, mostly allowing some fields to become optional that were previously mandatory. I think there's still an ongoing discussion about the case where you specify both an offhand ID and blinded paths. I'm quite not sure what everyone's opinion is because it looks like people mostly agree with each other, but it's unclear. I'm linking the comment right now.

Speaker 5: I don't think [redacted] agreed with us on it, actually.

Speaker 0: You don't think that what?

Speaker 5: [redacted] agreed. I think they wanted to have — so we wanted to support sending, but not necessarily receiving. But if we do not have the node ID when there's a path, we would have to support receiving as well. 

Speaker 0: Okay.

Speaker 5: I think most of that discussion occurred on the spec meeting notes from last time, and [redacted] may have not seen all of that. At least, it was implied that we would support sending, not receiving.

Speaker 0: Okay. So we should just ping [redacted] and wait for them to continue the discussion directly in the comment.

Speaker 2: Yeah. Sadly we're going to ship this as a release tomorrow. So without [redacted] here, it's a little tricky. But we're probably just going to ship it as is and it should at least work with Phoenix because it at least matches what [redacted]’s understanding or [redacted]’s goal was. Well, Core Lightning will figure it out or we'll fix that later.

Speaker 0: Okay. On our side, we can still iterate a lot. We haven't skipped anything and we can update anything based on how the cross-compat test go.

Speaker 6: Sorry if I jump in. What is the problem, from the CLN point of view, that I missed the last two spec meeting? There is someone that can do a summary.

Speaker 2: I don't think this has a problem from the CLN point of view. Given this was a change we only made two weeks ago, I kind of doubt [redacted] has gotten to implementing any of this in Core Lightning. It's more of a disagreement on what we should do.

Speaker 6: Okay. Yeah because I was also trying to grab the BOLT 12 specification to see what are the missing points from the Core Lightning side to try to rebase our current implementation on the spec meeting on the current spec. So because I see that we missed something, but I still need to figure out what.

Speaker 0: Yeah, I think there's a lot that changed since the latest implementation was done in CLN. [redacted said that they wanted to allocate some time in May to work on it and make sure that CLN was up to date with the spec. So I guess that once they’re back from Austin and they’re done with covenants, I think they’re going to be working on that. So that should help move the needle a little bit.

Speaker 6: Okay. Makes sense. Thanks.

Speaker 2: There's also this issue where LDK and Core Lightning disagree on how you should build a reply path for an invoice request message. [redacted] indicated they were going to acquiesce or at least support what LDK did, but yeah.

Speaker 0: Can you detail? I missed that issue.

Speaker 2: LDK sends an invoice request with a reply path that is just like any other blinded onion message path that it would make. But when Core Lightning sends an invoice request, it builds a reply path directly back along the path it sent the invoice request. So for example, if they have to do a direct connection to an introduction point to make an invoice request, they'll just send you a reply path that is that introduction point straight back to them because they currently have a live connection to them, even if they don't have a channel with them. So Core Lightning doesn't have any logic to do direct connections for invoice request replies. Only for invoice request sends. [redacted] indicated they were just going to add support for that for replies.

Speaker 0: Okay.

Speaker 4: Can you repeat that last part? I don't know if I understood. You're saying that they don't do direct connect for invoice replies. I thought the reply is going over the connect that the sender made?

Speaker 2: So, if we send an invoice request message to Core Lightning, we will include a reply path that is just like we would do for any other reply path. So I might connect via the async node to connect to the introduction point for requesting an invoice from [redacted], but the reply path I include with that is just gonna be whatever LDK's router decides, and that might be you must reply via, I don't know, Blitz node or whatever. Then, there on the receiving end, Core Lightning will say: Well, I'm not connected to them; I can't reply. They were going to add connection logic for that, at least. 

Speaker 4: Okay. That makes sense.

Speaker 0: But either connection logic or just routing logic because they could also just find a path to a Blitz node from themselves to send a reply, right?

Speaker 2: Right. Routed or connection. I mean either way, they were going to add support for making sure that message gets there because currently it never does.

Speaker 0: Okay.

Speaker 2: So generally, when people have been trying to test BOLT 12, they've hit this issue. This seems to be the low hanging fruit that everyone's been hitting.

Speaker 0: Okay. Sounds good. So, it means cross-compat tests are making progress and people are starting to experiment with the end-to-end flow, which is really nice.

Speaker 2: Yeah. People seem to be having a lot of success with the end-to-end flow, at least for LNDK and LDK or Core Lightning to Core Lightning. I don't know that there's been a lot — I think there's been some developer testing with Eclair, but not kind of general hackathon testing.

Speaker 7: [redacted] got Eclair LNDK the other day, and then also ran into the same bug with C-Lightning, so that's also working.

Speaker 2: Oh. Right. Right. Anyways, it's making good progress. I haven't been able to get in touch with [redacted]. They’re off this week, so I haven't made the progress that I wanted to make for our official cross-compat test so we can merge the spec. But hopefully, next week or whenever, [redacted] will get back and we'll be able to work on that.

Speaker 0: Okay. I think we'll need to wait for [redacted] to update CLN as well and to make sure that there’s nothing that they want to change on the latest changes we've proposed. But I'm hoping that May will be the month where we can finalize that. Alright. So kind of related to offers, [redacted] had a comment for the blinded paths and Trampoline, but I think I addressed it in by directly answering the comment. [redacted], does that make sense?

Speaker 8: Yes, that does make sense. Thank you for clarifying that last part. One thing I'm wondering about — we don't have to get into it now — but for async payments, it looks like the sender will be setting the final CLTV. With async payments, you want to set a quite long CLTV. So, we were hoping the first trampoline hop could set the CLTV to a more reasonable one. I have to think about it more, but that was something that came up.

Speaker 0: Okay. We'll have to think about this because in that case, you're right that maybe we'd need another mechanism than letting the sender directly send it in the trampoline onion, so we need to think about that.

Speaker 8: Yeah. Yep.

Speaker 0: Okay. Let's keep discussing it directly on the PRs. Alright. Next up, quiescence. There has been some progress on quiescence. We investigated with [redacted] adding the go-on message at the end. Unfortunately, what we realized is that really whenever you do a fundamental protocol, there's going to be two stages. One stage where you are still doing things that you can just roll back and ignore, and one stage where you just cannot abort anymore because, for example, you gave a signature for the current funding transaction, but the protocol is not complete yet because usually you need to wait for the other guy to also send signatures. At that point, you cannot roll back anymore, and you have to handle any kind of failure in the protocol, disconnections, and everything. That creates, inherently, a layering violation that can only easily be resolved by integrating with a channel reestablished mechanism and adding the go-on message on top adds too much additional complexity. So we figured out that it's really easier to just stick with what we have now without this explicit termination of quiescence and tying the termination of the inner protocol or the disconnection to the termination of the quiescent states. So, I think we should be able to resume our cross compatibility tests with the existing code base. Is that correct, [redacted]?

Speaker 3: Yeah. As it stands right now, LND is ready to do cross-compat testing with the existing spec with Eclair and I guess whoever else has implemented it as is. There, in my opinion, still need to be spec updates, but these are more like clarifying positions of the current design, not like any changes to the fundamental approach that we're going.

Speaker 4: I have a question for that. Like, if there's not an explicit termination, then how can, in theory, other high-level stuff all using STFU coordinate? I guess it's sort of assume it's an internal implementation thing.

Speaker 3: You have to reacquire a quiescence. To explain in more detail what's the problem is that for all of these fundamental updates, there comes a point where you get to what we call half-committed, which means that you can't abort the protocol anymore. But only one side has exchanged some sort of secret data that can no longer be revoked, and the other side has not. Right now, you can always end up in half-committed states during any disconnect process, but we handle disconnect processes cleanly during this channel reestablish process. If we were to add this go-on message, and we essentially sort of nuke the inner protocol state, then we can end up in a half-committed state, but without having disconnected from the peer. So you have to ask them the question: How do we resolve this half-committed state? Do we put some sort of channel reestablishment flow mid-protocol? What do we do? It turns out it's okay. We could try to put some sort of state synchronization protocol downstream of one of these events, but why go through the extra effort? We should just instead centralize all of this synchronization through the channel reestablishment process and then, essentially force a disconnect if any of this happens. The problem is that the go-on message would explicitly bless a message sequence that can result in this half-committed state, and we don't want to do that. So I've changed my mind about this. I don't like that there's this layering violation happening, but the implementation complexity to resolve this half-committed state issue is a far more serious issue than the I don't like the layering violation.

Speaker 4: Interesting. Okay. Cool. Yeah, I think I got this. At least, I wrote it down. 

Speaker 3: There’s a whole discussion transcript. 

Speaker 4: Okay, yeah. I also wrote down, sort of, the bulletins you gave me there, and I will check out the transcript as well, but yeah. Interesting.

Speaker 3: I think the commentary back and forth on the issue is more than complete in terms of explaining why we made the choices.

Speaker 4: Gotcha, I mean, okay. So it's the job of a protocol waiting to know when things are done because we reconnect basically?

Speaker 3: Yeah. So this is the spec change I still need to author. I looked at the draft to the quiescence PR. But what it essentially means is that only one downstream protocol — like, quiescence essentially creates this session token, and that session token is given in an ownership sense to the downstream protocol. So we can't actually batch these multiple fundamental upgrades into a single quiescent session as a consequence because of this implicit termination. So, what we do is we bind any sort of terminal state of the downstream protocol state machine to the terminal state of quiescence, so they both terminate at the same time. But as a result, it means that you have to reacquire quiescence. So, if you wanted to do quiescence and splicing, then that terminates the whole session. You need to do quiescence and then dynamic commitments if you wanted to do both. You couldn't do quiescence, then splicing dynamic commitments, and then unquiesce. Like, that's not a valid protocol flow anymore.

Speaker 0: I think it's actually a good thing that you have to reapply because usually, while you're quiescent, you will have comments that are being queued up to fail or fulfill HTLCs and you need to wait for the questions to end. So, it's really a good thing that even if you end it and the other side has nothing to apply and sends the STFU immediately, you can still get all your updates done before you also send STFU and then get another session. So, that gives you an opportunity to make sure that everything that is waiting for settlement can be settled before the next fundamental thing.

Speaker 4: Gotcha. Okay. I guess just moving from implicit to explicit. Or sorry, explicit to implicit.

Speaker 3: If you think about the UX issues as well, it's like if you're on RPC being like: Hey, I want to do a splice, right? By the time the splice operation is done and the user gets the feedback, you don't still need to be in quiescence. That thing can resolve. It's like resume. It's like internal function and clear out various cues. Then you might be like: Oh, even if I, as a user, want to do these things back to back, there's going to be plenty of CPU time in between them to keep things in sync.

Speaker 4: Cool. 

Speaker 3: I can't imagine a time where I'm going to want to batch the operations together, especially since I don't think that there's really any benefit to batching those multiple fundamental things.

Speaker 4: Alright. Cool.I'll check out the thing. I guess if you have anything that needs to be changed from that.

Speaker 0: Okay, and I'll reach out to you, [redacted], to resume the cross-compat test that you had been starting a few weeks or months ago. Alright. So related is the splicing PR. I finally opened the concurrent splicing PR because the existing splicing PR was really old. It was really hard to read because there were a lot of things that were still there from the very early draft of splicing and didn't look like, anymore, how splicing works today, which was really confusing to read and really hard to fix. So instead, I just restarted from scratch and rewrote it to also match what we currently have and that we've seen working. So, I would recommend reading that PR instead of the initial one. Also because I added a lot of test vectors, where detailed protocol flows. I think it makes it really easier to see the edge cases, the handling edge cases that can happen with splicing, and making sure that your implementation does correctly implement nasty disconnection or nasty concurrencies with splice message. So, whoever wants to review splicing right now should take a look at this read. CLN is looking at it right now to make sure that they potentially update their code base to match. 

Speaker 4: Cool. Yeah, I mean, I think we definitely have been waiting for a fresh one because the other one was comments of to-dos on to-dos, basically.

Speaker 0: Yeah. There was a comment by [redacted] to make it an extension bolt. I don't have a very strong opinion on that. Most of it is already in its own subsection, so it could be moved to an extension bolt as well. The only thing that I think is important is to keep the TLV definition next to the messages where they're defined. For example, we define TLVs for commit SIG, TX add input, and TX signatures. I think that has to be defined right next to the definition of these messages. Otherwise, you don't want to be jumping from one place to be able to see all the TLVs defined for a particular message. But apart from that, moving the core part of splicing to an extension bolt could work as well.

Speaker 4: Yeah. Also, interactive TX is already merged in, right? 

Speaker 0: Yeah.

Speaker 4: Okay. Cool. Just making sure about that. 

Speaker 0: Yeah. That's also why I wanted to start fresh with the latest state of master because it's easier to reference everything. The only thing that is still a dependency and is not merged is quiescence, but we actually only need one link to it. So that is just a dead link right now in my PR, but once quiescence is on master, this won't be a dead link anymore. Alright/ So, whenever people have time, they can just have a look at this spec PR. It's the same for liquidity ads. I also created a new one that is more flexible and allows people — it's mostly bLIPS for example — or extensions to define new ways of paying for liquidity. The goal: I'm trying to set up a bLIP specification for under-flight funding, like LSP under-flight funding stuff, that would use this new format for liquidity ads as a proof of concept that this works. So, I think I should be done with that in a few weeks. Maybe that will help review that liquidity ads proposal.

Speaker 4: Sorry. You said that you're working on a POC of what?

Speaker 0: On the under-flight funding. Basically the LSP stuff, where what happens if you want to relay an HTLC to one of your mobile clients and they don't have enough balance. How exactly do you do negotiate on the fly liquidity? I want that to rely on liquidity ads and splicing as much as possible because it really makes it much better in terms of trust in most cases. Now that we have splicing almost finalized and liquidity ads potentially making progress, I think it's a good idea to try to specify that.

Speaker 1: How's the liquidity ads come into play though? I mean, assuming the node that we're hiring is going to be one that opens, right? Or are you trying to disintermediate that? But then, wouldn't that require like preimage transport across those nodes basically? So, like an interceptor type of thing?

Speaker 0: No. What I mean is just a way to give your rates to your mobile client so that on the fly, the mobile client is able to pay for additional liquidity and use zero-conf to add liquidity on the fly and receive HTLCs that they would, otherwise, not be able to receive.

Speaker 4: Gotcha. But I guess, isn't that dependent on the HTLC because it's sort of an extra routing fee, right? And that, if they're getting one BTC HTLC, they get like 0.9, right?

Speaker 0: No. No. The goal of the latest liquidity ads proposal I'm making is that there's flexibility in how you pay it. So, for example, if you already have a channel and you would need to splice new liquidity to add the new HTLC. Maybe the mobile wallet has some balance in that channel, so they could pay the fee from the balance in that channel and no one else — the sender — doesn't need to know about it. And even if they don't, then it could be shaved off the value of the HTLC when it is relayed so that the sender of the HTLC doesn't have to know anything. My goal really is that the sender doesn't have to know anything and it only happens between the LSP and the mobile wallet, and no one else has to know about the fact that the funding is happening.

Speaker 4: Gotcha. Well, it just seemed like this was different from liquidity ads. I feel like this is like negotiation of a JIT channel, right? Which, I guess, can't use that for advertising, but you need to get messages somewhere.

Speaker 0: It’s what liquidity ads does. It is actually just you can actually do it with just reusing liquidity ads. So that's why I want to avoid adding something else if we can just reuse tools that we use everywhere, and liquidity ads is a great tool here to just advertise how much it would cost to add liquidity on the fly and just reuse the exact same flow. Right now, we just use the plain liquidity ads and splicing spec in Phoenix, and that worked great.

Speaker 4: But one last question, I guess you're assuming that the user is always going to accept, right? Because I mean, otherwise they need something to reject. I guess, how would they reject in theory? Is this a time-based thing?

Speaker 0: Okay. So, the way we do it in Phoenix right now is that users set a fee budget. They set a static thing saying my fee budget is that much. If it fits the fee budget, then it's automatically accepted by the wallet. If it doesn't, it's rejected. But otherwise, you could also imagine sending a notification to a user and waiting a small delay.

Speaker 1: Well, I guess that's what I meant. Like, if you were trying to do it all in protocol, you would need some reject thingy. But I guess you're saying you're already contacting them — the notification or something like that.

Speaker 0: Yeah, and it is possible to reject it. It's just a matter of how you decide to implement your wallet. You can always reject it, both on the LSP side and then the wallet side.

Speaker 4: Gotcha. But I mean, but then wouldn't you still need something else to ensure that the user’s wallet basically accepts the smaller value invoice payment? Or you're saying that this is implicit? You don't necessarily need anything for that, and they know because I accepted the liquidity ad. Like, I'm going to accept the 0.9 BTC HTLC?

Speaker 0: Exactly. That's going to be part of the liquidity ads format to say: I'm going to fund that much on that transaction and in exchange, I will take that much in fees from the HTLCs that I will relay next. So, that's part of the thing that we were defining a way to communicate that.

Speaker 4: Okay. Yeah. I think I actually need to check out the latest PR to understand. I think it’s different now.

Speaker 0: I think the easiest way would be to wait for the bLIP that I will be writing about that. That should contain all the information and link to the liquidity ads and splicing parts that make sense for this. I think this should make it clearer.

Speaker 4: Cool. So 1153 is the v1, because I see there's two liquidity ads. Right? So I see 1145 and 1153. One just says advertise; the other one is extensible.

Speaker 0: Yeah. So basically, 1145 was just mostly 878 without the enforcement of scripts, but with only one format of liquidity ads. It is actually limiting and cannot easily be used for more LSP stuff. So, that's why I then created 1153 and I explained in the description that this is a more extensible format that allows more ways of paying the fees to be added and all used in extension.

Speaker 4: Gotcha.

Speaker 0: [redacted[ is supposed to be reviewing it, but they gave me a concept ACK on the latest one — that more extensibility is probably a good idea because the initial format that they were using was really very tailored for the specific case where they wanted to add an addition to the script to make sure that it was a CLTV locked. But if we're not going to do that in some cases, then it makes sense to have more flexibility and define more ways of selling liquidity.

Speaker 4: Cool. Okay. Alright. One last question here — maybe this is going to be in the bLIP — whenever you're sending an open channel request, is it going to include the payment hash of the HTLC you got? I assume yes. 

Speaker 0: It could or — actually, it's really the other way around. The way I'm planning on doing it is that whenever you, as VLSP, you cannot relay on HTLC, you're going to send a new message that will add HTLC that contains, basically, all of the HTLC but isn't tied to a channel so that the mobile wallet receives all the earnings and verify that by decrypting the onions, they receive a whole payment. It's a payment they would accept if they had a channel. Then, the mobile client is initiating the open because they know that they are expecting this HTLC to then be relayed on the new channel.

Speaker 4: Gotcha. Okay.  I guess while we're here: Do people think it's useful to have the HTLC from the start? Well, I guess it depends how you pay for it because otherwise, you have the thing where the server basically opens the channel, but you don't do anything, right? Versus they can reject the HTLC just having it there.

Speaker 2: Yeah, you always have that. So the reason why you have the ‘will add HTLC’ message is less to fix that issue and more just to handle MPP because you need to handle MPP somehow. You need to know: Hey, I have three HTLCs, is this a full payment or are you still waiting for more? The way you address the…

Speaker 0: Probing as well. 

Speaker 2: And probing. Right. The way you address LSP trust client versus client trust LSP is just a question of when you broadcast the transaction for a zero-conf channel. So, in either design, you open the channel, you do your normal channel open flow, and the LSP sends the client the update at HTLC messages. You do the whole dance. The only difference is either the client immediately responds with the payment preimage, whether the LSP has broadcasted the funding transaction or not, or the LSP waits to broadcast the funding transaction until after they see the preimage. So either way, you have the exact same message flow. It's just a question of when that transaction gets broadcast and whether the client checks the mempool or something.

Speaker 4: Yeah, but I guess my question is: Do people think it's useful, if we're doing the channel thing in a separate format, to add a push amount HTLC? Or you're not worried about that gap? Because this would basically have the first date have the HTLC is where I am getting at. 

Speaker 2: Right.

Speaker 4: But that's something I think we discussed before.

Speaker 2: My point is that that gap is not a gap. My point is that that gap is not a gap if the LSP waits to broadcast the funding transaction until after they see the preimage. You're just adding more messages and more additional flow that's not actually required because the real thing is the LSP is just going to wait to broadcast the funding transaction.

Speaker 4: But isn't it risky for the user to send before because then the LSP can just not broadcast, right? And just take the HTLC.

Speaker 2: Yeah. So you can't fix this problem. There is no way to fix a zero-conf JIT channel, or any kind of JIT channel. Always, either the user can ignore the HTLC, not provide the pre-image, and grief the LSP and waste their liquidity, or the LSP can steal the money because the user sends the preimage before the funding transaction is actually out there. There's no way to fix that. You just have to pick one. So I think the intention — and I don't want to speak for [redacted] — but I think the intention is that the spec will support both. But the spec will support both purely just by saying the LSP can broadcast the funding transaction immediately, or they can wait. That's up to them.

Speaker 4: Okay. Yeah, I guess it's like zero-conf spend, basically. And they can double spend it anyway. Because even if you added it, they can still double spend basically is what you're saying.

Speaker 2: Right. You would have to wait for one confirmation. So yeah, the client would have to wait for one confirmation or the LSP has to wait to see the preimage to broadcast. But you got to do one or the other.

Speaker 4: Makes sense. 

Speaker 0: But one of the things that I will detail in the bLIP is that this really happens when you create the channel initially, but when you're splicing, most of the time, the liquidity fee can be directly paid from the user's channel balance. So then, you don't have this issue because you make them pay the fee for the liquidity they're buying and then you relay the HTLCs. Even if they fail it instead of fulfilling them, they have already paid a fee for the liquidity. So it's okay, and they cannot cheat as much as for a new channel. So, it makes it better and shifts the issue to the initial channel creation and cases where the user doesn't have any balance in the channel, but it's not in every under-flight funding attempt. But I will detail in the bLIP because it's hard to grasp, and it makes a lot more sense when we detail every scenario. 

Speaker 4: Cool. Looking forward to that. That was something I think is needed just to fill the gap there, and we'll use all the same thing there.

Speaker 0: Yep. Alright, So we are already at one hour. Is there another topic that someone really wanted to discuss today?

Speaker 4: Yes, I know [redacted] isn't here, but I don't know if people are up on gossip V2 stuff. I need to get up to speed, but [redacted] wasn’t able to be here. They asked me to pose two questions primarily around the motivation of re-announcing old and new channels using the protocol basically. Because it feels like if we can cut that out, then you don't have to worry about questions like: How do you acquiesce to the timestamp versus the block height? And then also: Do you continue to retransmit both messages? 


[Error in video. Transcript cut off.]

