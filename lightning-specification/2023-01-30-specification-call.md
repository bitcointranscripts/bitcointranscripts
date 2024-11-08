---
title: Lightning Specification Meeting - Agenda 1053
transcript_by: Generated
tags:
  - lightning
date: 2023-01-30
---
Name: Lightning specification call

Topic: Agenda below

Location: Jitsi

Video: No video posted online

Agenda: <https://github.com/lightning/bolts/issues/1053>

The conversation has been anonymized by default to protect the identities of the participants. Participants that wish to be attributed are welcome to propose changes to the transcript.

# Channel Pruning

Speaker 2: To be honest, I don't think anything has made a lot of progress since the last spec meeting, so I don't think we should do the topics in order. I didn't know what order to put them in. There's just one quick question I wanted to ask about implementations about the channel pruning behavior.

Speaker 0: Core Lightning has that integrated now.

Speaker 1: So we should have the same behavior.

Speaker 2: Okay, perfect. And what about LDK?

Speaker 6: Well there's the question whether we prune—

Speaker 2: Whether you do the right thing or, like most of us, you do the wrong thing. Do you prune if one of the channel updates is more than two years old? Two weeks old? Or do you wait for both of them to be more than two weeks old?

Speaker 6: We switched to doing it for either one in like two releases ago or maybe in the last release, so relatively recently. So you probably will find nodes that still do the wrong thing, but we do the right thing now.

Speaker 2: Yeah, I just wanted to check that it has been implemented by everyone and we can just drop it from the list. Okay, so perfect. Everyone has it now, so we can just remove that. All right. So let's move on to next. To be honest, I don't have any of those topics that I have seen apart from splicing on which [redacted] had a question. I don't know what topics we should cover. So if anyone wants to cover a specific topic, just raise your hand and cover it.

# Splicing

Speaker 3: Do you want to go over the splicing stuff?

Speaker 2: Yeah, sure.

Speaker 3: So, to explain the problem, there ends up being a race condition with the splice locked, where if there's pending activity on the channel- the HTLC settling commitments and stuff or even an announcement- there's a moment where one node doesn't think the splice is locked and sends a message in the old state before the other node receives it posts what they think is splice locked. You end up in this race condition where you either have to start making messages work pre and post splice locks, or you need some kind of going to STFU mode again to get an atomic moment where they both see the channel is locked. So I put together a short proposal that does the second one. It's a bunch of steps and it feels a little kludgy, but it might be the ideal solution. And I was hoping to get like people's thoughts on that: Is that the right way to do it? Is there a simpler way? That kind of thing.

Speaker 2: I'll take a look. Yeah, I think it's trivial because it means you just discovered that because you realized that there was a potential race condition with update messages, but until we exhaustively check or model check the protocol, we cannot be sure that your proposal would erase all of our issues. I know that someone wanted to play with TLA-plus or something like that at some point. Maybe it can be useful to test race because it's true that we are adding even even more complexity to our asynchronous commitment update things. So we could be created a lot of new bugs here.

Speaker 0: Can you explain the race condition again at a high level?

Speaker 3: Basically, the idea is that you have messages that are valid pre the six block splice confirmation and that are invalid after that. So, the most obvious one is when you do a commitment, you have the regular commitment and then a TLV of the spice commitments. You have dual commitments and that message becomes invalid after the splice is six blocks confirmed and the moment the nodes notice that six blocks confirmed and send their lock messages back and forth. The way it's structured now isn't atomic. So there's a second or two where there's messages in flight that can cross that barrier. So, we just do an atomic moment where both nodes are like: Yes, we both think that, it is confirmed six blocks; we're going to switch to the new commitment commitment thing.

Speaker 0: And then also funding locked in the current protocol though, or I mean, at least the current switch over.

Speaker 2: Yeah, but the difference is that you can have HTLCs whereas funding before funding locked, you don't have any HTLCs. You're not using the channel with splicing. The issue is that you have potentially two commitments that you are applying HTLCs to. But, at some point, one of the two nodes realize that this place is confirmed, so they can drop the previous commitment and some HTLCs that only make it into a new commitment can now be accepted. But if the other side has not seen the hazard, consider that it was locked, they will reject that message. But I think that it should work. If you only wait for the other guys place locked to sending to HTLCs that would only walk in the new ones, shouldn't it? I mean, if we separate the commitments, if we have one commitment message per commitment, instead of bundling everything into one message using TLVs, it's easy to just ignore the old commitment for commitment that you already dropped, isn't it?

Speaker 0: I mean, so I guess y'all take me into basically like there's new commitments. There's new TLV commitment segment that actually has multiple signatures for each of the pending splices. But then, then you also have that for all the HTLCs as well because one might get very large potentially, or run into potential like issues as far as the smallest message size or large message size rather.

Speaker 1: You can you can go for the order N squared, right? Because you have N HTLCs and you have an M splices in progress. Although, did we restricted to one? There was talk at one point of kind of restricting it some same value. I mean, it's not actually that bad in practice, but you do need somebody to figure out a limit, so you don't hit no packet limits and silly things like that.

Speaker 2: Why don't we discuss just using separate commitment messages for each of the commitment? If you have any commitments pending at some point, you just send N commitment messages and you just reference which commitment this is signing for.

Speaker 1: Then you'd switch it. So put in the TLV: You'd say which splice with some unique splice identifier, hand wave something to say that's what this applies to, and then you can ignore all the ones that you don't care about, which is kind of simple. I mean, the thing is, the splice lock message is supposed to say- is where your peer acknowledges that. So you basically don't. You should keep sending things until you've both sent and received splice locked, right? So they send splice for a lot. You send splice lock, and then after that point, you stop with the old signatures, right? If you consider splice lock, but you haven't got it from them yet, you can't. Oh, okay. Yes, you're right. There is a race in there because you don't know that they've sent it yet and they have. You're right; there is a race. I think the answer is yes. If you have some creative, some constructive way of ignoring the ones you don't care about, then you can send until you've sent and received, and that's okay. There will be a window there where they will receive signatures they don't give a crap about. Now, that can work with I think either scheme, but you do have to allow it. I do kind of like the multiple messages. It's a twist to the way that we do things now, but it is pretty clean and you end up, you don't have the same kind of what happens if these messages get huge. So, how do you like the idea of- other than the fact that your code already exists and that is annoying to change?

Speaker 3: I didn't follow all of that. Is the idea that we're going to support both? We're just going to ignore the messages that are stale and not fail?

Speaker 1: So, step one is you ignore the things because they will keep sending it until they have received your thing. So, there's a window there where they don't know that you've just sent it. In transit is that I've got the splice, right? So you'll get big signatures. But the other change is: Rather than packing every signature in the TLV, which is how we do it now, you'll actually send multiple messages and the TLV will just say which splice this commitment sig refers to, which is kind of neater, right? You know this is the base or this is the splice. That comes up in the question of how we identify splices, which I can't remember. It's been a long time since I looked at the spec.

Speaker 3: That will keep our messages smaller. I wonder if there's some weird state we have to keep track of there because we need to wait for all of the splices to get their sigs.

Speaker 2: You can just do it. You can just queue them. If you know that you have N commitments, you can just queue commit sigs until you have N of them. You just handle that atomically and just ignore them while they're in the queue if you don't have all N of them.

Speaker 1: And it fits pretty well with the whole ignoring thing because you go, well, not N because you don't know which if you're not going to require ordering, which makes sense. You've got multiple; you make sure you've got the complete set basically, right? And then you ignore any ones that apply to one that you've forgotten. Assuming there's some unique hash or identifier with each one, you make sure you've got all the ones you care about and then you just ignore anything else, and that would work.

Speaker 0: Can someone explain why funding confirmation affects this at all? What's being invalidated? I think that's what I'm missing.

Speaker 1: The point is you stop sending signatures after the splice is deep enough. You go, cool, we no longer need to send signatures on the old one or the new one, right? We're just going to send new ones. The question is: When do we agree that that point has been reached? And the answer is you send us splice finished or splice locked thing, right? But I've received your splice locked. I've sent my splice locked, but the spec says you will switch when you both sent and received it. So I've sent it. I've received yours. I'm expecting we're done, but my send is still in transit. So you send another message, and you're like, well, I haven't seen yours yet. So I'm going to assume that you still want the old signatures for both. So there is a window there where a naive implementation would go, but I've sent and received it. So what the hell are you sending these extra signatures whereas you haven't received mine yet? So, there's that latency there. That would be the race that [redacted]'s running into. And the answer is you just ignore that. You can send extra signatures if you want. That's fine.

Speaker 2: Yeah, there's no risk for you, but you're dropping them because you've seen those splice confirmed. So, those signatures are for commitment. That would be a double spend of confirmed transactions, so you cannot just cannot be broadcast.

Speaker 3: So the question is: Does that mean we want to keep track of the prior funding transactions so that we can make sure that these involved messages aren't spam? Or do we just want to say any scale thing we just say is fine?

Speaker 1: Quality of implementation issue. Yeah, it would be nice if we actually said, hey, you're sending complete bullshit rather than, hey, I get what you're saying here. This is old, but whatever is easier is to code. I mean, it's nice to have those extra checks in there just for our own sanity. For our testing to go, hey, you do eventually forget about the old splices like you're supposed to. That's nice. There are other ways of doing that. You could just make sure they're understanding. One after a while, hand wave. But basically anything that you don't understand, you can throw away.

Speaker 3: The other thing that also comes up is the announcements because the block height for the old announcement is different than the new one, and that's what is over too. So, we need the same kind of fuzzy forgiveness for a channel announcement for the old block height.

Speaker 1: I think we already have similar kind of logic and problems for announcements at the moment, which we handle by, you know, because if you reconnect during it, you have to send another set of signatures and stuff. So yeah, there may be similar issues there, but I think that's OK.

Speaker 3: Same idea, we're just going to be like: Okay, this block height is stale. It's okay; we're going to ignore it though kind-of-thing.

Speaker 1: I think so.

Speaker 3: Yeah. Well, and the other thing is: Are there other things we're not thinking of that might be affected by this, if we're going to go this path?

Speaker 1: You'll find out when you implement it. I mean, if you're halfway through typing, you go, oh, then yeah, we'll have to go around again. Okay, so logically, this is consistent with the way we handle other things, you know, where you're expecting redundant packets in corner cases. And that's okay.

Speaker 3: So to summarize: We're not going to do the splice like the ACK or any of that. We're just going to throw out the stale messages, which we have two categories. We're thinking of the commitments and the announcement sigs.

Speaker 1: Yeah, but we'll switch the messages to the standard commitment signed message with the TLV to say, OK, this is for the splice. You'll just send multiple of, which actually is kind of neat. Yeah, it's a bit hard because you've got to accumulate them on the receive side. You accumulate them until you've got all the ones you care about, and then, mechanically, you can treat it like one message, right?

Speaker 3: You can just wait for the others. Do we want to require that they're that they're sent in that they're all sent? Like I start to make an event that send all five of the RBF splices and I finish or other messages spliced in. Do we care about it?

Speaker 1: Yeah. No, no. It's fair to insist that they. There's no friggin add HTLC season. The middle right. It should literally be a blast mechanically. The separate messages and there may be gossip messages intertwined and stuff. But from the point of view of non gossip, non error messages, non ping message, right. You know, channel messages. They will they will always be in order like they'll always be back to back. So you can literally sit there and accumulate them and do nothing else. You don't have to worry about. Oh, but what if they add an agent? Because that doesn't make sense, right? Their code should literally be generate them all and blast them out. There should be no adding HTLC season in the middle of that. I think that's fair.

Speaker 2: Right. I think that's just the same way that whenever right now we send committee. We're just waiting for your river can act before we send anything else anyway. So, there shouldn't be anything that would sleep in between those messages.

Speaker 1: Yeah. Definitely easier to implement.

Speaker 2: Cool. Cool. All right. So should we do another topic? Is there something that one of you has been working on that made progress and that it tends to report?

# Taproot

Speaker 0: I can talk about some Taproot stuff. Made a bunch of progress on Taproot stuff. Have everything working other than breaches and things like that. We've also went to review from some people as well that were on the spec, or at least looking at the code level. There's two things that came up in review. One thing is: In certain situations, we don't want a key spend path to exist, right? We only want to script a script path. For example, one situation is, okay, the remote output, we basically want them to force to have one CSV delay, right? And initially, like I have like a nums point in there, right? So basically something you can use to generate the okay, well, no, no, no, no, no, no, no, no, no, no, no, no, there's code. You can check things like that, people will. Okay, well, it's simpler. Maybe if we just instead use like the funding key and you say, okay, well, you're never gonna sign for that anyway, right? But then, you know, in review, people run off that. Like today, it's possible to sort of like actually scan on chain for your own to remote output, basically, by like looking at your own, you know, basically like your HD key chain, that's offline, you can actually go through all your keys, and then find it on chain, right? If we did the funding key method, that wouldn't, wouldn't be possible, unless you had some SCB type information, basically, right? So, that's kind of like an argument: Do we go back to the number point that would allow this easy recovery tool? Basically because this is a global parameter for the system, or something that's bound that particular point. That was one thing that came up. At the code level, it's just like whatever key you put in there, so it's really not that big of a change. It's just a matter of, are you hard-coding the key being this numbs point or are you doing some other thing? As far as the numbs stuff, I have some code that we've used to do the same thing for LNC, which requires this. You just use this PAKE handshake, basically. People want to write other code to verify this, to verify it themselves, to replicate this after their opinions. I think there was just some uneasiness around using this newer thing, essentially. If we can address that, just because it feels like the argument of that recovery tool is pretty nice and stuff still happens, and so it'd be nice if we can retain this, basically. The code impact is minor. It's just a matter of this constant or using the multi-sig key.

Speaker 1: Yeah. This sounds like speed running the discovery of static remote key, right?

Speaker 0: Yeah, basically. Exactly.

Speaker 1: Let's not do that again. Yeah, definitely having the ability to find your own outputs and stuff makes me sleep better at night. Validating a numbs point is pretty trivial, so I would definitely think you're on the right track there.

Speaker 0: Yeah. What I have here, the code I link is basically like the hash and increment. You start with the seed point. You can cat an integer to that, and then hash that, and then seed is a point. Then you basically increment that over and over again. I think this one stopped after four duration or something like that. If you have Go installed, you can just replicate it. That's just one thing that came up at least. This isn't something that needs to be right now, because I was mentioning it's something you can just have as a parameter. You can just hard code the function parameter itself. It's just a matter of people being comfortable with this, getting whoever to look at it as well, the relevant people or whatever, just to get that thumbs up on that.

Speaker 2: I'm posting a link to an old mail posted a while ago about helping backups by deriving keys based on something-something. I had nothing to do with it because if I remember correctly, it was something we potentially could do with Taproot, but maybe it works even before. I haven't reread it, so I don't even know if it works, but I think it was worth. I noted down to investigate it again when we potentially reworked channel funding. So if you want to have a look at that and see if it's meaningful for the group change.

Speaker 0: There was an issue. Yeah, I remember this. I don't remember the details, but something I didn't remember.

Speaker 1: Yeah, I went to start implementing this back to pre Taproot. The problem, as I recall, was that because you now had to derive every key from your node ID, you could no longer have this idea of, I've just got the keys for this channel and not the root secret for my node, and I can run the channel on it. For our security model: Basically, you can have a mode where you do have one-way derivation, like hard derivation, and you basically use that key to basically run the channel and do all the signatures for transactions. With this model, it's got to be a non-hardened derivation, basically. So, that thing that's dealing with a single channel has to have access to your master key. Just in a practical sense, that was a security downgrade that made me uncomfortable. Now, we actually implement that today because we basically have an HSM. We ask all the questions. But in theory, you can have this isolated thing that only has the keys to that channel, it can only screw up that, right? And it doesn't have access to your node's master key. So, that was the reason that I disliked it. I liked it in theory that, yes, you could go back and you could derive the stuff and you could find out who you had. You could basically ask, calculate everything on the network, do I have a channel with them, right? And look on chain to find it. That was cute. But I didn't think the theoretical gains were worth the fact that you have to have access to the master key to do this, and we couldn't figure- I mean, obviously we've got the whole, the standard problem of that without pairing curves and exotic stuff, you can't do that trick, right? You can't have some derivation that everyone can do and yet you can't do backwards, right?

Speaker 4: Yeah, I agree. I think non-hardened derivation is a rather frustrating security issue. I think it's possible to have something that would not have this vulnerability, but especially once PTLC has become a thing, and you wanna, then the payments of pre-image becomes actually just a discrete log. You really don't wanna mess around with unhardened anything. Yeah.

Speaker 1: Yeah. That was, for me, it was the killer. I mean, it's a cute idea, but I didn't think the benefits for that were worth the- it's kind of like the, you lose a little bit of day-to-day security for this corner case, where you can find your own channels. And in practice, if you can find your own outputs when they close the channels, you're almost as good anyway. So, yeah.

Speaker 0: So, the question is looking at the script: What happens if the sig is invalid? Does the script succeed or does it fail? And I mean, if people know the context of this, I can say that, or that can be another hint in terms of where this is used, doesn't it check if I fail when the value is zero? So, [redacted] said it checks: CSV fails when the value is zero. [Redacted]'s asserting that there's a special check for zero, I think is [redacted]'s answer here. I'll say that's correct.

Speaker 4: Quite a question more so than a question, but yeah.

Speaker 0: Yeah, that's a good question. Yeah, accepted because the verified doesn't pop. Okay, so [redacted]'s saying that if you pass a zero in there, it's still accepted.

Speaker 1: I think the answer is no one should ever write direct script.

Speaker 0: And also, this is one of those optimizations, right? Where initially I had like the explicit thing of putting the one there, right? So verify, and then one CSV, this is basically the carve out thing for the treatment output. You know it turns out. This relies on the trick where at the end, this is gonna try to verify that zero is greater than zero. Zero being the zero on the stack and zero being what's gonna be in the sequence, which is always gonna be false, right? So, you know, if the signature is invalid here, it will be false. But there's just kind of a question where people saw this, they try to check the bit, the bit wasn't clear. People thought there was a special case for the zero. That's not actually there. It's one of those things because CSV is actually implemented with the sequence. So, there's a few layers in the direction. So, the question here is: Is this okay? Because you know, I wrote tests and verified that like things are valid. Or do people want the more explicit thing, which is the cost of the one V byte or whatever, for just adding the one there and making that a verify?

Speaker 2: So is it, yeah, right.

Speaker 0: So, do we want to just have the one in there? Because then you can glance at it and know this works. So, it does work. It's just the one thing where I had to go back and verify myself. Like I wrote some work, I was like, okay, no, no, no, it works, like, you know, this is good. But it's just one of those things where even developers were just kind of like: What's going on here?

Speaker 4: Yeah, I remember we actually were working on this thing a little more like a month or two ago. Also, manually verifying it. Given that less than half a year has passed, and I- at least- have already forgotten the special case, I'm very much in favor of explicit legibility and documentation.

Speaker 0: The thing is, it is one byte, but you already have the control block and stuff, right? Which is 33 bytes in this case, and then the script and things like that. So, it doesn't mean it's significant in terms of the savings there, and people are already stuffing more data in the chain of servers these days.

Speaker 2: So here's my 1 byte.

Speaker 0: I'm leaning towards the one thing. 'Cause like [redacted], I had to go back and convince myself to respond to the reviewers, like, okay, no, it's legit. But it's cool to know that this is a trick that exists now. I think it was [redacted], one of the people that was looking at it.

Speaker 2: But that's only for scripts in first clause anyway. So that's something that should happen often. So yeah, we can definitely eat the one more V byte, right?

Speaker 0: Yeah. The other thing as well is this reoccurs in a few other places as well. For example, here's like a HTLC success. Right, so yeah, yeah, force close, yeah, exactly. So this is only the force close case. This is another case where the same thing is here, where they're assuming that check sig pop zero gives you a zero that's going to be sequence verified. So, I would go through and then make all of these just one CSV, so you can look at it and know: Hey, this does what we do 'cause you know, today we have that same explicit nature in the script.

Speaker 1: Oh, no, I think it's cool. I've read the bit. Yes, it has to be; the item has to be greater than. That was my question: Is it greater than? Yeah, it was the greater than. That's the subtle thing, right?

Speaker 0: 'Cause if you have zero there, zero greater than zero false.

Speaker 1: Look, this is not the scariest thing in Bitcoin. Hey, we validated it; it works. I'm like, okay, if we save one byte think of the starving children or think of the NFTs you could create in that. Yeah, the starving blocks. Yeah. I guess it's part of me that goes: Shouldn't we just be generating all these things from mini script these days and doing that? And what does it generate? So, everything here has just been hand-rolled. I don't think there's been mini script. Maybe that, maybe mini script popped this out.

Speaker 0: I'm not sure. Initially, I had this little version, and then the contributor, I think it was [redacted], came through and then gave us the stuff which is a little bit smaller. And then I think it's just like, I don't know.

Speaker 1: In retrospect, at least this is the time we would have written everything in mini script and just used it as output, right? I don't know if it does this trick. It should, it should, everyone should. This should be one of those things, right? But, I guess the question is: What does mini script produce?

Speaker 4: Is the mini script generator even finalized as its gonna produce everything? Well, it will be eventually deterministic, but are there gonna be changes to it that might change the script? Because it is my understanding that to be able to verify the tap tree, you actually need to know exactly what script your counterpart is gonna generate.

Speaker 0: Correct, this would be a hard coded thing basically.

Speaker 1: Yeah, but even so, mini script is pretty finalized. People are actually suddenly interested in implementing it. So, I don't think there are any changes pending for it.

Speaker 4: Okay, cool. I think in principle, it would be possible to like check for five, six different combinations of scripts that I guess could be produced, but I just don't think it's worth it. I think it's a complication that we should avoid. A double cost.

Speaker 1: Yeah.

Speaker 0: I can always run it through, and see what it pops out with. Maybe it's the same thing because this isn't too crazy. It's just time out success, things we've been doing for a while now. I think those are my two major type of things.

# Blinded Paths Interoperability

Speaker 2: Perfect, so what else do you guys wanna discuss? What have you been all working on for the past two weeks?

Speaker 2: I also saw that [redacted] had a lot of issues with the test, so I'm not sure. I saw that you merged the PR with the latest changes for the Blinded Paths path to CLN. Is that gonna be in your next release?

Speaker 1: Yes, that puts it in the next release. So, you staggered into the case where CLN is too smart: it will go, hold on, you're a dead end node; and I'm not gonna create a route hint. And now like a Blinded Path to that node, because you're a dead end, so you've gotta have a public node behind it, and it goes, oh, okay, so there's real, you're a real, you're not a dead end, and then it will actually create the path through.

Speaker 2: It's not really smart, is it? It's potentially an issue for real users, right? Even if their N is really small or something like that?

Speaker 1: In the route hint case, it makes sense because it's like: Why give you a route hint to somewhere you can't reach anyway as a general rule? We could carve it out and go: Well, if there's only one option, we should use it, even if it looks like a dead end, because it does actually complicate some of our tests, because in a test case, we get this all the time, right? Where you go: Hold on, I'm not gonna do that. But in general, the point is that if you've got a whole heap of peers, and you've got one peer that doesn't have any other peers, you don't wanna use that as your route hint. You can use it for your Blinded Path. It's a bit weird because you're bouncing it out perhaps, but you don't have to be as strict with the filtering. But that's because I stole the same code this way.

Speaker 2: It's not really weird because the sender could be privately connected to the node that you think is a dead end. In that case, it would make sense for them to even see a route hint for that.

Speaker 1: It could, but we select them randomly, and so we just eliminate the ones that look like dead ends. We could then go, oh, but if it's, again, we could fall back to. But if there's only one case, use it even though it's a dead end, which would cover this case, right? This is that; we're kind of in, doesn't happen in real networks case. This is optimized for mainnet, where you do have to have if you're a big node; you'll have a whole heap of dead ends, and there's no point.

Speaker 0: Well, I have one question. So, I thought like Blinded Paths are sort of like some super route hints, right? So that you would just put everything, everything's encrypted now. Is that the case, or is this like a hybrid case that y'all are talking about?

Speaker 1: Of route hints and what is not? Yeah, we use the same logic to select where do we do our, so we do it in the minimal case. If we have only private channels, we go, crap, we're gonna need a route hint to something, and then we look at all our peers, but we eliminate all the peers or dead ends, and of course, [redacted] is creating this simple case where, you know, Carol's here, and Core Lightning's here, and going, oh, well, why don't you create, surely, you have to create the route hint from the Eclair node, because it's only one choice, but Core Lightning's too smart and goes, hold on, you're a dead end, I'm not creating a route hint or a Blinded Path for you, because you're a bad choice. And that heuristic is probably, it is overzealous in this case. If it's only got one choice, it should do it anyway. So I could probably just fix that in the code, and it will simplify a whole pile of tests.

Speaker 2: Yeah, I put it only to appear where I am raising that, but there was also another issue in my comment that C Lightning doesn't seem to be able to send multi-parts to, if C Lightning has two separate Blended Paths, and each of them doesn't have the whole capacity, you don't do MPP yet?

Speaker 1: No, it does the dumbest possible thing. It creates the first one and takes, does it? So okay, we found an intern, someone who's done some work with [redacted]'s stuff before, and we're like: Oh, we want a boutique implementation. So we found someone who could intern for us to do that because I've lost [redacted]. So I'm hoping that they will basically produce a new pay plugin that does all the things, and part of it will be to do MPP properly across Blinded Paths and everything else. At the moment, I've totally hacked it in to the pay plugin. So I just tell the pay plugin: Oh no, you're actually going to the end of the Blinded Path, and then fix it up at the end after it calculates the route, then slap the Blended stuff in- which has got a whole heap of problems with it- but it was enough for testing, right? But one day, it'll be a real boy, and it will have all the things, and it'll do it properly. So yeah, that's definitely to fix.

Speaker 2: Okay, so I can just ignore those use cases right now for the end-to-end test. So it looks like apart from that, everything else was now working correctly for the interop between Eclair and CLN. So if others want to chime in on the spec PR, I guess. Otherwise, I'll maybe clean up a bit the commits, and they should be ready to be integrated then.

Speaker 1: Cool, excellent. Yeah, so when you've cleaned it up, ping me, and I'll just do another scan for anything else. Cool, perfect.

Speaker 0: Cool, yeah, and then hopefully I'll see you can join in on that in the next few weeks, maybe a month or so.

Speaker 1: Yeah, cool.

Speaker 2: You will be able to see three nice commits and not a mess of big stuff.

Speaker 0: Yeah, the current Taproot thing is like that too. There's even merge commits in there. So once I do, I'll do these changes, and I'll run through the mini script, and then I'll kind of have a new, like a clean slate to check out.

Speaker 2: Okay, perfect. And on the offer side as well, we have a PR that implements all of offers, sending, receiving, and [redacted] is going to do end-to-end tests with CLN as well. So with CLN, if [redacted] takes the master branch, he should have everything he needs.

Speaker 1: Okay, perfect. Yeah, look forward to that too. So that will be good because you'll be the first interop on that.

Speaker 2: All right, so what else? Dual funding. Since [redacted] isn't there, we're just waiting for CLN to finalize the code to be able to do the end-to-end tests. Route blinding, done. And then messages. I don't think there's anything new of us as well. So is there one of the topics from the bottom of the list or something else that people want to discuss?

# Oakland Protocol

Speaker 1: Yeah, so the Oakland Protocol, which is like on the back burner, getting further off the back burner. We talked about doing a non-enforcing one that sees how much it would break things. Has anyone actually done that yet?

Speaker 2: It is on my to-do list, but I decided that I would finalize dual funding, liquidity ads, and splicing before that. So we're getting back to the end of it. Yeah, maybe this summer. I don't know. It'll take a while.

Speaker 0: Not yet. I'm pretty sure someone made like a gist of the actual thing. I think I have like something easy you can do to make probing a little more difficult; and that was like my takeaway from it.

Speaker 1: Yep. So, one of the steps which y'all do, and we don't yet, is by default restrict the maximum HTLC in flight to lessen the channel by default. That opens the window to doing the Oakland Protocol, which everyone should start doing. Next release for sure, I'll put it on it. I'll open the issue to make sure I don't forget it.

Speaker 6: We do limit by default the channel in flight amount to less than the thing. It's configurable, but by default, we do it. If someone announces an HTLC max in their channel update, which is less than the channel amount that we saw on chain, we prefer to take that path. So if you start doing it, we will definitely give you more routing fees. And by definitely, I mean we absolutely will not because the preference is very, very small and it probably will never matter.

Speaker 2: Eclair does that now by default. We use 45% of the total capacity, and it's configurable by the other operator.

Speaker 1: 45? Doesn't LND use 10? Does somebody use 10? I know I had 10 in my head.

Speaker 6: We do 10, I think. We do 10 by default.

Speaker 2: Okay.

Speaker 6: 45 is very high because you're likely to still be pretty probable because your channel's rarely that. 10 is probably too low.

Speaker 1: I don't know. You need some floor, obviously. Like if the channel is small enough, you're like, well.

Speaker 6: Yeah, someone recently opened an issue because we actually can't open smallish channels with core lightning because it gets mad that we don't have a floor, and core lightning has a floor. I think if you try to open less than like 100 msats or something channels, we fail because c-lightning gets mad. It was unclear whether we should fix it, or you're all should fix it, but they changed their settings network.

Speaker 1: Okay. Maybe we should just go don't open stupid tiny channels anymore.

Speaker 6: Yeah, I wasn't in a rush to fix it because stop opening 100 msats channels. I don't know.

Speaker 1: Cool. I'm hearing 20% is like the golden number between the two of your numbers. So that's good. I'll open an issue.

# Max HTLC Requrement

Speaker 0: There's one thing that we need to catch up to: Basically, the change that we did for the HTLC max being required. We now realize there's some like subtleties around that, but I think we have a way to do it properly without partitioning the network in a sense, but that was like one thing that we thought was a little bit easier. So, we're fixing that with next release definitely. And then same thing with the SCB delay thing as well. We realized there's another thing with some old LND nodes, but I think we have a way to resolve that too. But do you think that we're a little bit behind on that? I think we should have to catch up in, but you've seen make sure that we do proper testing. I think we've reproduced both the HTLC max disconnecting with c-lighting, and then also, the first goes to lighting as well.

Speaker 1: Yeah, so our next release is going to just ignore those messages rather than starting sending warning and hang up because there are some nodes out there that are sending, and these ones are all ancient. Like they're two years old.

Speaker 0: Yeah, there's old nodes. I think that's the thing where sometimes we move quickly in the spec, which is great because we're like: Hey, do the thing, but then it's kind of like the random lagger node. That matters too.

Speaker 1: Yeah. So, we've currently suppressed the warning, and we basically just go, you sent a bogus one. We're just going to ignore it for the moment, and eventually, we can switch that back on.

Speaker 0: And then we'll still send that error then, so that'll work out. Then, we'll even give people some CLI to just send an error or something like that.

Speaker 2: Cool. What is the subtlety with the HTLC max?

Speaker 0: Well, just the subtlety was just that LND was still relaying HTLC max stuff. So, if you relay that, it can cause disconnection with another peer, right? Which is like a second order thing. It's not us sending it; it's someone else that relays and then sends- they get sent over to basically. So, 'cause we've made an issue where that's weird. We knew that, but then, it was kind of one of those things as far as coordinating that roll out.

# Async Payments

Speaker 2: Oh yeah, that is mentioning that [redacted] posted a scheme for the long-term async payment. I haven't had time to look at it yet.

Speaker 0: Same.

Speaker 2: It doesn't make any noise.

Speaker 1: I think it's basically just tweaking the PTLC point with a receipt message and announce from the receiver. But I still need to study it in a lot more detail as well.

Speaker 2: This is mostly for offers and the reusable invoices, right?

Speaker 1: This is offline. So you can actually get a pre-image out of the node that's offline, but you want to. So you basically want to send and get the point if it's PTLC.

Speaker 2: Yeah, but if I have given out a one-time invoice, that payment it will just be deferred until I am back online, right?

Speaker 1: Yeah, but the problem at the moment is they go: Cool, I want an invoice. Even to generate the invoice, you have to wake the node to get it to calculate the pre-image and give you that, right? So the idea is that somehow you mix in something that they sent, so you'll get a unique value.

Speaker 2: Yeah, so you send and build 12 offers, right?

Speaker 1: Yeah, pretty much. Although technically, it would apply to any scheme like this, whether LNURL or anything like that. But yeah, anything where you basically have to request a new invoice without waking up the node. Yeah, so I think the HTLCs base one will use keysend and not have proof of payment, but then the scheme that [redacted] posts is how we can get proof of payment back with PTLCs.

Speaker 2: Sounds very similar to our stuckless payment design we had a couple of years ago.

Speaker 0: Yeah. I think we were thinking about that because [redacted] was asking us how we felt about stuckless payments, and should it be in PTLC version one.  What's that really looking like? Does it add extra round trips? Latency? Which version? 'Cause there's like three of them. I think now, some of them were actually impossible. Some of them: Well, it's possible, but if they pull over, they get punished or something like that. But I mean, we know there's a massive design space for this stuff. So, after we at least did the simple thing, and even just this, CSV thing shows other stuff there. But that definitely, I think, will be a big thing later as far as like getting over the PTLC hump and seeing what that looks like in reality. I remember last time we talked about secp, or secp ZKP adding support from musig 1.0- and I think that PR is still open- but at least once that's in, then people can use that and get familiar and start doing interop, etcetera.

Speaker 4: Well, it's a blocker for us because we needed for production readiness for Taproot. Until then, we are trying to open source and experimental, definitely non-production ready musig to implementation in rust That is solely for, again, solely for experimental purposes, meant as a bridge gap solution just to be able to get some of the arithmetic right. But there are a bunch of things that it not only doesn't support, but also can support because it relies on Bitcoin, secp256k1 Rust, whose error messages aren't really precise enough. Like, they won't let you know that some additional results in an infinity pointer, things like that. However, I think it would be nice to get some review of that regardless, such that pending the productionisation of musig to in the Rust, and the secp library, and then the Rust bindings, there's at least anything that people can work with.

Speaker 0: Okay, yeah. But so once I do this script stuff, I can get people like a pubkey or something to test again to be ready for that phase of stuff.

Speaker 4: Cool.

# Channel Jamming

Speaker 0: Anything else? I guess one thing is. I know [redacted] opened up some channel jamming stuff. I don't know if you've checked that out. I haven't checked out at all. I know some people made some comments.

Speaker 2: Yeah, [redacted] also posted to the mailing list. We had a meeting about jamming last Monday, and [redacted] posted a good summary on the mailing list, especially with some potential issues that we found with using upfront fees. When there's a big difference in channel fees between nodes hops in the route, upfront fees may not make sense and may have the wrong incentives. Some nodes may have an incentive to just collect them and not relay. So there are a lot of open questions in [redacted]'s email. So if everyone can have a look at it, maybe think about it, and join the next meeting, that would be great.

Speaker 5: Yeah, so the stuff that's open on the spec now, and there's a concept in LND, is very like the absolute most basic way we could do upfront fees. I think the big question for me is: If we want to go in the upfront fees direction, how far do we wanna go down the proof of forward rabbit hole? Because what we were looking at is actually the loop node that has just like some really high fee peers. If we have these super unconditional upfront fees, we just push them along the route. The node before the high fee peer is very incentivized to take the upfront fee and not forward at all because they have low success case fees and the high fee node has very high upfront fees. So I mean, there's transcript, there's main list post, there's PR, so that should provide extra context. But yeah, just really how deep do we want to go on a first version of upfront fees if we want to go with upfront fees at all?

Speaker 1: Yeah, I looked at the proof of forward stuff. I didn't think that I could reliably do it without adding a round trip in. On the whole, I will only get paid if I forward to you case, which is kind of really nice incentive compatible. On the other hand, the case where if you're routing through something that has really high upfront fees, you've made that choice and you're kind of running that risk. I don't actually think it's because upfront fees, almost by definition, cannot be fee dominant if they are. You've got massive incentive problems, even with forwarding and things. I don't think you can paper over it entirely. So, it's definitely a nice tick box to have, but if it makes it significantly more complicated, I don't think it's worth it. But I haven't read your mailing list post, so I should go through and do that.

Speaker 2: Yeah, I think there will be a very large difference in channel fees between very large established nodes, like loop, that have been there for a while that are real things and new nodes that are joining the network and have to use a very low fee to start attracting more channels. So, it wouldn't be unreasonable to see a factor of at least 10 or maybe 100 between those two fees. So, if upfront fees are 1% of that, then we have an issue.

Speaker 5: Yeah, something we didn't really get to as well is: How much can this be? We require the sender to make sure they don't send a super irrational route. And on the other side, will people actually steal it if failing the payment means they'll be skipped over in future? What's difficult about both of those is they're kind of fuzzy because maybe the payment has no other routes. And then on the other side, we can't really just rely on the soft wishy-washy penalty of you'll lose out on some traffic in future if you do this because there's lots of different people sending payments. So, that's where the fuzzy upfront fees then becomes even more fuzzy. Ideally, we'd have something incentive compatible, but if we have something incentive compatible for the whole route without the sender having to enforce it, the spec change is gonna just get so nasty so quickly. But yeah, please take a look at the post, take a look at the transcript, and we meet every other week with the spec meeting. So it's a bit of jamming mitigations, working group rather than just looking at our front fees. It's an hour earlier than this meeting, which I imagine would be terrible for [redacted], but we can chat about the timing if folks in different time zones wanna attend.

Speaker 2: Or we just pay you that meeting and we send you the summary and you can just jump to conclusions and raise new points.

Speaker 5: Yeah, I got absolutely nerd sniped by all the new AI stuff out this weekend. Now I'm very into it and gonna do transcripts and transcripts for everything. So, we'll hopefully have some quality transcripts, and we found something to do speaker attribution, which I think helps a lot with following them. Cool, all right.

Speaker 1: That's it. I guess we can end early.

