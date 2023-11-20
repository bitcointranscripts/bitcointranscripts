---
title: Lightning Specification Meeting - Agenda 1067
transcript_by: Gurwinder Sahota via TBTBTC v1.0.0
tags: ['lightning']
date: 2023-04-24
---

Agenda: <https://github.com/lightning/bolts/issues/1067>

Speaker 0: Alright, so first thing I've got on deck is 1066, which says: Correct final CLTV handling and blinded paths.

Speaker 1: Yeah, I haven't dug as deep into the blinded path stuff, so this may be an incorrect reading that I was confused to. Basically, for a blinded path, we don't have a final CLTV for the recipient because we just have a full CLTV delta for the full blinded path. So, the spec is very clear that you have to include the final CLTV delta for the recipient, but that's kind of nonsense because we don't, in fact, have one. [Redacted] claimed that this - or [Redacted]'s read of the Eclair code - seemed to be that it does what I described here. Just always says zero plus if it added any extra value, it'll include that. As you know, if you're doing randomization, you have to tell the recipient that you randomized and how much you randomized by, so that it checks that. But I think aside from that, there's nothing else to include. So, I guess [Redacted] and [Redacted] aren't here, and really the two of them need to comment on this, but that basically summarizes it.

Speaker 0: Yeah, because I guess you're saying that - in this case, the receiver makes the last hop anyway, so they know what that value is.

Speaker 1: They know what the delta should be from the current block height, yeah.

Speaker 2: But another thing to note is that in the route blending spec, currently prior to [Redacted]'s PR, there's a max CLTV expiry field that's intended to be in the Bolt 12 invoice, but it's not. So, I think that would have solved that, but it seems like, from what I read in Eclair's code, that they just put the shadow offset.

Speaker 0: You're saying that there's a new field in the Bolt 12 invoice that was meant to be, but got left out or something?

Speaker 2: That's what it looked like when I looked at the route blinding spec. It mentioned a max CLTV expiry that was intended to be in the invoice, but it's definitely not in the Bolt 12 spec. I think what Eclair's doing makes sense. It's just the spec is not up to date to it, if that makes sense.

Speaker 1: So, should that be a separate PR to remove that field that doesn't actually exist?

Speaker 2: Yeah, I thought it was in your PR, but if it's not then...

Speaker 1: Oh, I forgot to do it. I know you'd mentioned it, I forgot to do it, I'm sorry. I don't know if you want to do that.

Speaker 2: Yeah, I'm happy to.

Speaker 0: Gotcha. I need to catch up a bunch of blinded path stuff in general, so I don't have too many thoughts other than like something-something test vectors. But I guess we have to see exactly what the desired behavior is and what this stuff prescribes right now.

Speaker 1: Test vectors? Just test it in prod. What are you doing?

Speaker 0: Oh, I've got some ideas how we can test in prod. Cool. Okay. Alright. We're done some basic notes there, I guess. Onwards 'cause I guess we need people that have implemented stuff. I don't know, [Redacted], does this make sense to you? I don't know if you got the bar.

Speaker 3: It seems to me what I've done was so low level that the API just requires that you give it a final CLTB because we just did a pathfinding in LND. But if you were to couple it all together, you'd need it.

Speaker 0: Cool. Alright, I just marked that to people to look at. I guess I'll tag you to ask me on it too. Cool. Next thing on here is - the list we've had for a while - onion messages? I think last time - something-something test vector regenerate. Looks like we have some new comments from [Redacted], I think. Looks like it's about test vector stuff.

Speaker 1: Yeah. Looks like they referenced an update in their code, and then unclear.

Speaker 0: Yeah, and I think it was also rebasing this after the bypass was actually merged into. So, that's done, and now it's test vector, so. Okay, cool. I think offloading has a similar test vector state. Okay, this has also been rebased. On top of the rebased onion messages one. But I guess I don't see any other comments other than rebase stuff. Thank you for supporting the implementation.

Speaker 1: Yeah, no further comments there from our end. I mean, I can let [Redacted] comment. We're still a little bit away from interop testing. We've got all the data structures done. We just have to basically wire it up to onion messages, and that's it - to do interrupt testing at least. But, we also have to be able to generate blinded paths. We're still a little bit away from that, but we got most of the stuff done.

Speaker 4: Yeah, my PR with the integration of onion messages. There's probably a few changes I need to get in.

Speaker 0: Cool. There's this desk thing, which, I think, last time was just a call for you to look at, which is 919. I think [Redacted] looked at it, and asked if you would take a look at it. I don't think that's happened since then. That was like in February even.

Speaker 1: I haven't had a chance.

Speaker 0: Yeah, I need a reload context to be honest too. I think it's a summarization of what we do today.

Speaker 1: Summarization, after you got fixed by everyone. Sadly, I think everyone is currently drowning in new features to add, and so, no one is actually working on it. Backlog on this bug.

Speaker 0: I'll make an issue on that one - the tracker for it too. Next, temporary channels. I was going to have this rebase, but I didn't get to my homework. But something I need to do. I think the only lingering thing here was some stuff around the anchor output. Anchor output, basically trade-offs re-allowing third parties to sweep. The main thing is that basically the internal key they need to make a control block may not always be revealed the way it is right now.

Speaker 1: Is that a trivial change to make it revealed?

Speaker 0: It depends on what key we use, right? In the past, we used the multi-sig key in the actual script, but now that's a mu-sig, so that's not always revealed. And the other thing as well, if we were to reuse that key there, that wouldn't allow the other - basically the broadcasting part - to even allow to sweep that themselves. So, some people came up with an idea of basically modifying the two local output to have the replication path in the script path, which would help for, I think, only public channels, depending on what you put for the internal key. But the main thing is that we can potentially allow it to always be swept at a cost of increasing the on-chain footprint for the average normal delay sweep. But if we do as is right now, there's a risk that some outputs are left on-chain, and the thing is people seem to be sweeping these pretty regularly. We actually have seen some issues resulting in not properly recognizing sweeps and things like that. So, it shows that they are being swept, and I don't know how many outputs are actually just sitting there on-chain. We could probably look at the actual value of all of them as well. But that's one thing. It's not a big change. It's just a matter of the anchor output stuff, as far as wanting to be swept. I think it is the case that for public channels if we put additional information or reuse information that's going to be in the channel announcement that can give a third party the ability to sweep it. But that doesn't help for unadvertised channels.

Speaker 1: The issue is that currently you can spend it with a key path, and in order to make it script. You have to somehow expose the script path if you wanna...

Speaker 0: Well, so the idea is that the third party needs to get the internal key that's committing to the script path in order to be able to sweep it. Depending on what you select for that internal key, the information might not always be available. So, for example, right now, I think we basically do the internal key of the two local output, which needs to be revealed in order to sweep with the delay. Basically, it means that only if that is swept, can the anchor be swept itself. But if that isn't swept, then the anchor cannot be swept. In a scenario with that, maybe some disaster recovery thing or so on, like loser channels and stuff like that can just already be swept. So it can be on the chain longer than we want and potentially no one can sweep it unless they know this value. The value can be communicated elsewhere, but it's not a super big showstopper. I think it's just kind of like that right now; it doesn't achieve the exact same thing as the anchor did before, which after 16 blocks without any additional information, someone can sweep it. But now, it's basically after 16 blocks and the two local party has swept their output. But that's the main difference, so there's a risk of it.

Speaker 1: For a public channel, we can use something that's public. I mean, we could use the node ID or something. But for a private channel, we have to reveal something.

Speaker 0: That's a good point, because if you use a node ID, then the party knows that. I guess that's the first time that
we're using that for an on-chain output.

Speaker 1: No, I'm not necessarily suggesting we would, but you could freeze it, add a public key to your node announcement or something and just say: This is my anchor public key, try this.

Speaker 0: Alright. Yeah, that was one thing, and then the other thing that was a lingering thread from before - just refreshing people's context - was basically some implications around which key is used for, I think, it's two remote parties, internal key output. And the idea there is right now we have that CSV one thing, where they always need to wait for that one block because of something-something - you know, mempool stuff. Prior, initially I had a nums then I made it a multi-key because we don't necessarily need that. Then people realize that the nums is nice there because it basically allows for people scanning the chain for that output, given that it's a static key. I think there were some people like: Oh, we hadn't used that before. But I made something, and we can have people look at that something and reproduce it. Reproducing is pretty simple. You take a hash of a word - lightning tap or something like that - check that point, and then concat. If that's not an actual point, you basically concat, and injure, and increment that. But I think it's just a matter of getting people to look at that. If people think it's trustworthy, then that can be used. And I generated one before, but we can use that one or just do something with scratch.

Speaker 1: That seems fine. Is there some more standard num? - I guess that's kind of the standard approach to generating a nums point anyway, but I guess So, nums point that's used for other stuff, we can reuse that as well.

Speaker 0: Yep, I think that was the other thing. I'm not sure if other stuff - maybe Liquid has one for their Peterson commitment or something like that. It's either try to use another one or just run this thing. And there's a pretty set algorithms - try and increment basically just a matter of picking what to reuse or do new one.

Speaker 1: On the previous topic, I personally, it seems nice to - if we have to increase the on chain footprint, that's okay to reduce the UTXO set size. This is the inefficient outcome anyway. So, a few things: It's obvious it's a lightning channel, so we don't need to try to hide it by doing the key path spend. It's just more efficient. Wasting a little bit of space in far like witness or in a transaction size versus reducing the UTXO set seems like a worthy trade off in a case that's already stupendously inefficient.

Speaker 0: Yeah, and it's not that much additional data. I think it's just like 32 bytes for the sibling hash in the tree, so it's not crazy.

Speaker 1: Right, so, at least, my vote - insofar as I am even paying enough attention to this to have an informed opinion would be to take the hit - put some extra data there and make it claimable.

Speaker 0: I wonder if it's already smaller than the old one. Also, maybe not, but I'd have to look at it. Maybe it's slightly larger.

Speaker 1: I imagine it is, but I'm not sure.

Speaker 0: Yeah, and I guess that's just the one thing. Yeah, it makes revocations a bit more, but that doesn't really happen that often. It's maybe like 65 bytes or something like that. Not too crazy. Alright, but I'm actually going to have that rebase and stuff, and then I just need to rebase all my PRs on the LND side. 'Cause we're doing a different approach for branches because it's a lot of changes back on each other. Touches like literally everything. Cool, alright. Check. Gossip stuff. I went through and made some comments before this. I caught up with a little bit as well as far as going through some of the other stuff. I guess there's a few things. One thing I realized: Implications of block height based rate limiting, which is just the stuff around saving up the budget - is that okay? Other things related to channel update errors and things like that. I guess I didn't realize that it would have some of those implications. I guess also gossip query stuff too. Because I think, pretty sure, Eclair implements the timestamp based gossip stuff because they wanted to sync channel updates more frequently. So now, this potentially has some downstream stuff there. I need to reread the section around the burst save up and things like that, and if that should be climbed a little more. But I think it's pretty cool that we can get like a global kind of limiting from that whereas right now, even the password, there's a...

Speaker 1:  Yeah, the most common is just a sender side thing. Shouldn't be too hard to implement. You just always announce a few blocks back.

Speaker 0: Yeah, and I guess you can just save up. It's not too hard to know when your last one was in the current height as well

Speaker 1: Right, you'll have to store the previous one you used, but that's fine.

Speaker 0: Yeah, you're right. You should have that. I don't know if there's some other thing there.

Speaker 1: I think the other big conversation about all this stuff is how exactly the proof format works and what we want to prove versus what we don't want to prove and over commit versus multi-sig versus whatever.

Speaker 0: There's another thing around TLV everywhere or not. I thought funding V2 and splicing used TLV everywhere, but I checked - maybe I checked the wrong place - but I guess it didn't. I thought it did.

Speaker 1: They don't, at least the implementation PR with Rust does not.

Speaker 0: Maybe it'd be good to have a stance generally on this, going forward for new messages as well, or what parts should be hard-coded. I think [Redacted] talked about channel ID, because that's always going to be everywhere, at least in certain messages. I think [Redacted] brought some points around signaling for compulsory fields or not - stuff like that. One nice thing I just looked at is, for example, node announcement - I think we talked about removing color and some other stuff in the past. People use alias, not necessarily color. If it was a TLV, that means it's optional, which is nice. People can set it. I don't know what the actual use is, but that's one thing.

Speaker 1: Yeah, I don't know. Personally, I don't care too much. Flip a coin for all I care. If we intend to maybe remove, it should be a TLV. Stuff we have no intent to ever remove, and clearly, shouldn't remove, it probably shouldn't be a TLV. But I really don't care too much.

Speaker 0: Yeah, and one thing about the TLV thing is - for example, I feel like there's two points at which we're talking about for this output thing. I, you know, I said I was gonna make a post last time, I haven't done that yet, but I'm working on it. Two things - one is: How much the output script should be bound?; and the other one relates to that: How much the value should be bound? By bound, I mean it's a channel, and it's one BTC or whatever else, right? But as far as the output scripting, if we make revealing more information optional, that can naturally be a TLV. But I guess the question there is that: Who's going to do it versus not? Is everyone going to require it? You just sort of mess up certain goals as far as the end of the reset because in that case, it would basically be showing the two Bitcoin keys. Then, you can say if there's a nil tweak that means you're doing the 36, but then if not, then that means you know you're doing something else where it's fancy or something like that. So, that's at least one place where a TLV could be useful.

Speaker 1: I mean, it seems like something where like either most nodes are going to verify it, in which case you absolutely have to include it, or the vast, vast majority of nodes are not, in which case you will just never include it. It might as well be a new message at that point. I mean, it doesn't have to be a new message, but anyway.

Speaker 0: Yeah, I was just trying to, at least, write up some summary thoughts on trade-offs of the looser writing versus what we have today and pathfinding and things like that.

Speaker 1: But you intended to put that on the mailing list, right? That seems like...

Speaker 0: Yeah, I just haven't done that, but I'm gonna do it.

Speaker 1: I haven't even checked the mailing list, so had you done it, I wouldn't have noticed.

Speaker 0: Okay, cool. But yeah, just trying to at least move some things out of comments because they can get lost, and it's like everyone hops on the PR or something.

Speaker 1: The comments are getting long there. I mean, I'm sure the mailing list is going to be equally unreadable.

Speaker 0: Yeah, that's what my rule is: If I'm not part of the thread - there's more than six messages - I'm never reading. But if I'm part of it, then I feel like I have to, or if I started it, then I have an obligation, obviously. But even that maybe though. Cool. I don't know if anyone else has anything else as far as the Taproot Gossip stuff. I think we're gonna start, at least, looking at code on the internal - things that you need to do, new output type, things like that itself. At least, the fields should be the same, even if it's TLV versus not encoding wise, just to get some more familiarity with that. And then, we have a towers thing.

Speaker 1: If we do material over commitment, [Redacted] was moderately to strongly of the opinion that the proof should be in the channel the node announced...

Speaker 0: Here we go back to 2.0. The backslide.

Speaker 1: ...no down first versus no over commitment. I mean, my point was you could do overcommit without doing that, but [Redacted]'s view is that it should just move and do it cleanly. But yeah, I mean, that discussion is gonna impact the code structure point a bit.

Speaker 0: That'll also further impact just the protocol flow as well, like no down first and then that.

Speaker 1: So, that's going to impact the code structure. I mean, it's not going to materially complexify the code. It's just going to change the structure of it a good bit.

Speaker 0: Yeah, this one at least follows the current flow. That would be something very different. But right, okay, I'm always trying to touch.

Speaker 1: It won't materially change the total - like it'll change the diff a bit, and it'll add a little bit more complexity, but not a material amount. But it will mean the diff compared to the current state of the PR to that state of the PR would be drastically different. So, I think we're probably not gonna bother trying to touch code until that conversation is, at least, marginally resolved.

Speaker 0: Okay, and then at least I can make that post, and just put it out there sooner than later as well. At least, start a forum for it. Cool. I mean, we have more stuff to post in my comments, but I can talk through the rest of it and everything. Dual funding. I know there's some stuff around splicing and the messages. There's a mailing list throughout on that, but I didn't really get to. Oh, the last thing was the witness stack thing, and that went one way. Looks like some messages emerged or PR versions of [Redacted]'s fork.

Speaker 1: I think it ended up using the Bitcoin witness utilization format. I also didn't follow it too closely. I don't know if [Redacted] is here, but [Redacted] left a comment saying it did. And then, there's this ongoing discussion around more protocols.

Speaker 0: Should you send multiple messages?

Speaker 1: Yeah, I'm just signing those. Anyway.

Speaker 0: Yeah, and I know there's some slicing stuff on the mailing list around education's ordering or something like that, but I'm not sure if it's even that. It looks like there's been some comments in the past month or so on the PR. Cool. I don't think [Redacted] is here, but next one is trivial errors, 1044.  One thing I was thinking about this is: Does this have implications with blinded paths? Right? Because it changes the error message. I think there's more HMAC to stuff on it. Can it still be verified if part of the path is in the tunnel?

Speaker 1: I mean, a blinded introduction point will basically say: I got back an error that was in the tunnel. Leave me alone. So, I assume, at least, you can always verify it, or I assume you could build it, and it should be built such that you can verify that it came from the blinded introduction point. But then, to your point, the question then is: Well, what did you gain you've now learned that it's in the tunnel. I guess you know that you have a different tunnel.

Speaker 0: Yeah, it feels like the the answer is maybe there's no implications, but at least something that - I think we wanted to look into before we had some of the PRs and stuff like that.

Speaker 1: That makes sense.

Speaker 3: I've looked at both of these, working on blind and I've looked at [Redacted]'s thing. Given that route blinding pretty much just drops whatever it got up until the introduction point, and then the introduction point returns, and there shouldn't be a problem. There may just be some sender-side thing, where you need to make sure you don't overly blame the introduction point because in a normal case, if something dropped all the HMACs, you blame them for being malicious. But in the blinded case, this is what this person is supposed to do. But that's a general blinded paths thing anyway. You need to penalize the whole blinded route, not just the introduction node. Otherwise, you'll hammer them.

Speaker 0: Yeah. Interesting. Yeah, I'd say put it with my head to actually think about it. But yeah, maybe not. Channel reestablish requirements. This is homework that I, [Redacted], - still for a long time now. Just basically tighten up the spec around reestablish, which is one of the more involved parts of it. Cool. Peer source backup. This is 881. Oh yeah, because Eclair had something a while ago, and I think Core Lightning rolled something, and maybe this is about reconciling them? I'm not really sure because I think the Eclair thing is live. I think they do it for all their wallets, things like that.

Speaker 1: I think correlating is live too. I'm not sure whether they're the same or not, but yeah.

Speaker 5: Yeah. So, we had a Summer of Bitcoin intern work on an experimental feature. It's live now, but you've gotta manually enable it.

Speaker 0: Gotcha, okay.

Speaker 5: So, they were looking for funding to do kind of a follow-on, integrating that into the spec and kind of merging those two. I'm not sure what the status of that is though.

Speaker 1: Okay. Yeah, I mean, anyway, we'll probably do whatever is spec an option here. I don't know if we'll use it, at least, in the short term. We'll probably use it some, but certainly we'll implement it because storing 64K for your peer just sounds like a nice thing to do.

Speaker 0: Alright, that's everything. Going back down to stale. So, one thing we're looking at again was the inbound fee stuff. I guess [Redacted] was saying that people commented that they wanted to look at other stuff or something. But I didn't fully understand that context because I don't think I was at that spec meeting.

Speaker 1: No, I thought you were. We had a previous meeting. I mean, this was months ago, and I think there was a lack of agreement. Basically, we spent a bunch of time on it, and then concluded: Eh, we'll talk about this again because we're not close to actually merging it. And so, I just was highlighting that if people are getting close to actually moving forward there, we should have that conversation again. Sadly, we're missing a ton of people here, so it's a little hard to have this week.

Speaker 0: Okay. I mean, I still stand by my old kind of perception that - I think the other one, you can't really rely on someone to broadcast an update for you, and in the future, if there's more at a global level, that's not as compatible basically. They have different trials as far as deployment, and also implications as far as their own fee schedule and everything like that. The other one indirectly has the similar effect, but one's directly sender-receiver, the other one's direct peers, which needs to update as well.

Speaker 1: Right. I think if you hold the position that the only negative fees are going to be adopted - which I don't necessarily agree with; I think it's, in fact, very limiting to what people want to use this protocol for - then, you can still do negative fees on both, right? You have the same kind of update policies around it. If your peer tells you: Hey, I'm going to assign a negative fee to our channel, you have a very strong incentive to go ahead and announce that because it means your channel is going to get used more and your peers' the one paying for it. So what do you care? So, I don't think that's true from a general point of view. It's only true if you're - it's like an Apple Store; just comparison basically, because the version that is just two peers also supports positive fees, which is an additional further feature that I also think is really important for people actually adopting this. Because just supporting negative fees is very restrictive.

Speaker 0: I don't see why the other one can't do positive fees. I think right now it's a sign integer, but you can emulate it.

Speaker 1: No, every node will just ignore it. If you announce: Hey, I'm trading positive fees, nodes will just ignore it.

Speaker 0: But it's a sender level thing.

Speaker 1: Yeah, and some nodes will ignore it because you have an option to pay more in fees or not pay more in fees, and you will simply not pay more in fees.

Speaker 0: Well, you can increase your other fees, so then they can pay that or not pay that. And not paying that means not routing, right? Or not getting racial see-through.

Speaker 1: No, no, because it's not broadly adopted, right? You could wait. If we were talking about every node supporting it and not talking about some something that is just built for LND, then you could actually enforce it over time, say in three years or something. But you couldn't enforce it immediately because most nodes - I mean, certainly today, no nodes support it, right? So you have to wait awhile until senders actually support it before you could enforce it.

Speaker 0: Yeah, I guess what I meant is like a combination of normal fees and then also this as well. I need to actually walk through it, but I'm pretty sure you can use it to simulate positive inbound fees as well, just by doing your updates and then, advertising this as well.

Speaker 1: So, the problem - if you if you sign a further positive fee on all of your channels and then the negative fee to offset it on all of your channels, and then take away that negative fee on one channel. That's true, but again, you have the sender upgrade problem, right? Like you're gonna cause senders to never send through you because you're assigning a huge positive fee for senders that don't interpret this new field. So again, the previous proposal was phrased as: This is a thing for people to try out, and we're gonna see how it goes and see where it goes. My point is, it is absolutely incongruous with people just testing this out because senders have to upgrade to support it, and that's gonna take quite a while and senders aren't gonna actually upgrade. So, you can't get good data using this feature for how inbound fees actually impact your routing performance because you're gonna hurt your inbound. You're gonna hurt your routing performance materially by trying to do positive inbound fees and not doing positive inbound fees, which strikes the proposal so substantially that it just doesn't really - its not a good test bed.

Speaker 0: Well, I think to be seen if it's a good one or not, and we can see that is by trying it out and seeing if people use it or not. We can very easily track people that are advertising it because it's a new field, and then there can be just reports on the sender side as well.

Speaker 1: But it doesn't actually because senders have to support it and you're gonna blow up your routing.

Speaker 0: Yeah, the senders that do, and I think you'd leave it to the routing nodes, right? Because a lot of nodes are a lot more sophisticated now as far as tracking their costs. So, we can give them a knob and see if it helps or not. They can turn it off. It's completely optional.

Speaker 1: Right. But my point is that it's not - if you're coming into this, you're saying: I want to see 'Is inbound fees are a good thing that allows routing nodes to achieve some end goal?' This is not the way to test it, right? Because this doesn't actually allow you to test it kind of 'completely.' It only allows you to test it for a subset of senders, which is going to be a very, very small subset of testers for a while, and then grow to a somewhat larger subset of testers, but certainly will never grow to like the vast majority of senders - at least not for for some number of years. So, it doesn't really allow you to answer the question: Do inbound fees allow you to accomplish X or Y goal? It only allows you to answer the question: Do inbound fees accomplish X or Y goal, given a very small percentage of the network is sufficient - is upgraded to LND version X or Y or running LND version X or Y? I don't think it allows you to ask that question.

Speaker 0: Well, I don't agree. I think it's less about percentage of the network and more about, like, you can say the aggregated volume of certain senders, right? For example, if you just know that there's some company or something that actually sends through you reliably and this can help you solve.

Speaker 1: Percentage of which have upgraded, that's true.

Speaker 0: Yeah, sure. I mean, it's a sender-side thing. So you're right. It is bottlenecked on that, but that maybe happens more quickly than you know, which is why we can see if it does or not.

Speaker 1: My point is that it's not really about 'Does 50% of senders or whatever?' - more 'Does it reach a vast majority?' Because you don't really get a'representative sample' to answer the question: Does inbound fees allow you to accomplish goal x? - unless you have the vast majority of volume by sender upgraded to interpret...

Speaker 0: For your node?

Speaker 1: Sure. Yes, for your node.

Speaker 0: Yeah, for your node and some nodes are more specialized than others. Some nodes exist for a singular purpose in the network today. If node exists for a singular purpose, that's highly specialized.

Speaker 1: If a node exists for that purpose, it should just use something that's not in the global broadcast network and tell its peers about it. That doesn't really make sense.

Speaker 0: Alright, I guess we'll see if this works or not.

Speaker 1: I think you're pushing something that has an impact on every node implementation. I think we should have a conversation about that rather than just saying: YOLO.

Speaker 0: But it's optional, right? You're saying that centers can do it if they do it or not.

Speaker 1: It's really not optional. You're saying you're going to emulate positive inbound fees by assigning a different fee to the outbound edge - that's really not optional.

Speaker 0: I'm saying that's one way to do it. That's the same as increasing your fees.

Speaker 1: But you're also changing fees in a way that has an impact on everyone's routing algorithm. Like in order for a node to materially implement Lightning.

Speaker 0: If they want to do it.

Speaker 1: No, in order for a node to materially implement Lightning - i.e. give their users competitive fee rates...

Speaker 0: I think you're assuming we're jumping to the point where everyone's updated. But you already said that's going to take a long time - right?

Speaker 1: I'm saying that you are pushing something that - irrespective of users updating - node software implementations really are largely forced to update because they want to give their users a competitive user experience or a good user experience, where they're paying a competitive amount on fees.

Speaker 0: You're saying you're saying forcing I'm saying it's an incentive, right? They can take it or leave it or not. No one's forcing. This is no voluntary network.

Speaker 1: Okay. That's a very similar outcome.

Speaker 0: Yeah, I mean, I think if you analyze through that lens, I'm sure there's a lot of things we could look back at. You know, that you could say that have a similar effect.

Speaker 1: Yeah, that's probably true. That doesn't mean my point isn't valid.

Speaker 0: Well, yeah. I think we're just approaching from different angles. You're assuming that everyone needs to do this.

Speaker 1: I want to better understand your angle because I'm not really sure I understand your angle here.

Speaker 0: I guess my main thing with the other one is that I don't think you can reliably rely on the other node to always broadcast your updates. I think you had some examples that said: Well, they're gonna get a certain discount or a fee. But you, as a routing node, you don't necessarily know if the sender ever even got that update at all, right? So, I think the issue there is that it's indirect. You're telling another person to give a discount in your direction and saying they should do that. This other one is a direct thing. If someone routes through me, I can cancel the HTLC and give them an update directly; and no one needs to know about it. So, the other one requires all of your direct peers to update in order to actually push this thing forward and make sure all of your peers are able to do this. This only requires you in the sender. So, if only two people in the entire network were updated, someone could get some value out of this thing versus having all of your routing operators update. And then, not to mention potential negative cycle or effects of causing individual to basically always trigger updates. If I tell you that you need to do my new update, do you take into that account to basically do your fee schedule and then tell your neighbor and that, eventually, has a cycle as well? So, I think there are different approaches to the problem, and I don't see why you can't put them on in series or concurrently, rather.

Speaker 1: So, let me address your first point. Your first point was that you can't fail on HTLC because you can't rely on your peer to actually send the update. So, my point...

Speaker 0: Oh, I meant that you don't know if the sender has the update because you don't know if the peer is actually going to take that into account - because they also have their own fee schedule algorithm and they need to take into account this if it's the case for all the other direct peers as well.

Speaker 1: Right. That was a good feedback. Originally, I did update my proposal to take that into consideration. So, first of all, obviously your peer can always just decline to forward payments to you. So them explicitly misbehaving and doing something incorrect is not really a material concern because they can always just do that.

Speaker 0: Yeah, they may do it inadvertently because they need to factor in their fees and your fees. If that makes sense.

Speaker 1: Yeah, of course.

Speaker 0: It's lossy is what I mean. It's lossy.

Speaker 1: It's not. So, I did update the doc to describe - obviously you already, today, have to wait some amount of time before you enforce a fee update because it has to propagate. So, I did update the doc to take that into consideration. You do obviously see when your peer sends an update message; you don't know necessarily that they received your message. But you do know that if you keep track of when you sent the message, and when you got the last other message from your peer. It's not super hard. We do that all the time in Lightning, and I did implement that. It's super trivial. Then obviously, you see the next channel update they send after you're sure they heard your message. At that point, you can be confident that they're actually doing the correct thing at that point, and then you can enforce it based on whatever timeline you already had for HTLC updates. So, I don't think that's now a legitimate concern. I don't know if you read the latest...

Speaker 0: Yeah, I'm not having the greatest one.

Speaker 1: I would recommend you read the latest one because that's no longer an issue, as far as I know. If you find an issue with it, I would love to hear about it. But that's not an issue anymore. So, that just leaves the question of - to your later point - was just saying: What is the upgrade procedure like for routing nodes versus their peers versus senders? I think that just fundamentally gets back to the question - if the goal here, which is, at least, the stated goal, is to try out inbound fees and see kind of what the net effect is. See whether it achieves certain goals that routing node operators think it will achieve. Then the question is: Which set of nodes having to upgrade better achieves that goal? Is it just peers of the routing node operators that want to test this feature or is it representative set of the senders routing through that node? I am fairly confident that it would be just peers because to your point, you probably only have a handful of channels that you want to apply a certain fee rate policy on, certain inbound fees, because you don't want that capacity to get used towards you. So, you really just need to get those specific node operators to update, and presumably, that's a much easier task than a representative sample of senders. You're right that there are definitely some nodes that are operating in an environment where they only really care about one sender or small group of senders. So, in that case, it might be easier. But even there, I think those nodes that are only caring about one or a small group of senders are also only caring about one channel - right? Like if you're a node that's sitting right next to loop and you want to charge something based on that. Or you're sitting right next to another node that charge something based on - if you're talking about one sender, you're also only talking about one channel that they're using or one set of channels that they're using. And again, I think it's much easier to talk about that one node being your peer updating because you already also have a relationship with them. Hopefully you can ask them to update. Well,

Speaker 0: Yeah, I think that makes a lot of sense about the test bed and the node environment, and how quickly your nodes will update and so forth. But I still assert that one can be tested with two people updating and the other requires hundreds or even the entire network itself. Now, I think it's a pretty big difference, right?

Speaker 1: Can example where that's true? Where you only care about one sender, but you also care about many channels.

Speaker 0: One sender is the reductive case basically, right? That like if you know that there's a wallet app out there, and for whatever reason, this wallet app ends up sourcing a lot of your traffic because you have some peer relationship or other things. This lets you do that. The other one requires all the peers to update. We do know that there's a lot of things people are working on right now network-wise, right? Will all of them update in time? And you also can't rely on this thing to be enforced reliably unless all of your peers are updating. That seems very fundamental to me.

Speaker 1: No, that's not my point. I think you missed my point. My point is that if you only care about one sender, then you probably also only care about one channel, right? That if you care about one sender upgrading, then that one sender is probably using your one channel from that sender or through one specific path from one of your peers. Right. So again, you only have one channel you care about. Like if you have one sender you care about, you also only have one channel you care about. And so the upgrade requirements there are the same.

Speaker 0: I don't know about that. I don't think that's the case because those peers can use any of your channels. You're saying that if you care about one sender, they're only going to use one channel? But does that mean that you're bound? Does that mean you're bound with that one channel for that one particular peer? I think it's a pretty fundamental difference. Basically, you're saying restricted to that one peer and one channel and one implementation.

Speaker 1: No, what? No. You were arguing that it's easier to update or it's easier to get useful information with the announcement because we only need to care about the one particular sender.

Speaker 0: What is reductive? It's just whoever gets the announcement.

Speaker 1: Okay, what has updated? We're talking about a number of things that need to update in order for someone to get useful data from this experiment, right?

Speaker 0: Yeah, but I'm saying those two endpoints, that being the one node and potentially, the set of senders.

Speaker 1: I'm saying that it's actually equivalent. So, if I'm a node on the network and I hear about one or five...

Speaker 0: I think that's where we fundamentally disagree.

Speaker 1: Can we talk it through then? Because I don't understand your point there.

Speaker 0: Well, you're saying the number of nodes to update to have meaningful data for an experiment is the same, right? And I say that's not the case. Imagine one node that has 100 channel peers, right? 100 channels that are reliably used for various purposes, right? All 100 of those need to be updated to allow a sender to take any given path to that node, right? But you're saying if they only take a single path, then only one node needs to update. Yeah, sure, but what if they didn't want to take any of those hundred paths to that node?

Speaker 1: So, first of all, we're talking about just the inbound path. While it's true that a node might take one or two or three different paths to reach a node, it's fairly uncommon - at least, when I look at like routing graph or when I like try different routes to a node. It's fairly uncommon that there's more than just one, two, or three that me and individual sender are gonna take to a given node, and that's doubly true if that nodes close to me if that nodes close to me in the graph.

Speaker 0: Are you even assuming MPP? I think if you assume MPP like that already breaks down, right? You're probably gonna take multiple paths, and even for real primitives, you can take multiple paths.

Speaker 2: So, we're talking about a node that's close to you, right? Because we're talking about specific cases where there's only a small subset of nodes of senders that need to update in order to take advantage of this feature. And I think mostly we're talking about routing nodes, not sending to. So that's for MPP is a little less important there because generally when you're MPPing you're not gonna send five MPP parts through the same node via different channels. Normally, at least in my experience.

Speaker 0: Why not? But I don't know. It feels like you're making a lot of assumptions around how people run writing nodes, the way senders work, things like that. But I stand by the end to end assertion, right? That one is end to end. You need two people to update the other. You need several other individuals with direct channels to update. I don't know how you can get around that. That seems very fundamental. We've done this a lot in the past. That's very fundamental. For example, we were able to add the metadata field in the invoices, right? Because that was an end-to-end update. That only required the person giving you the invoice - the person sending - to update. This is a similar thing. Only the sender and the internal node that they're routing through.

Speaker 1: Does anyone enforce metadata? I don't think so, right? Because it's not universally supported, is it? I don't think anyone enforces it yet.

Speaker 0: Well, I think people people want to move it to for payment secret, but that that seems beside the point. But yeah, it seems like we have a very different view of network updates, and who needs to update versus not. I think I've written down my views for what constitutes an end-to-end update.

Speaker 1: It's not a fundamental question here. This is not some foundational question. This is a specific question for a specific experiment. Let's be clear. If the stated goal is: We want inbound fees in lightning, then we should be going about this in a different way. And maybe your design is actually probably better.

Speaker 0: But the thing is, [Redacted], taking that approach in the future does not preclude doing incremental things today, right? That's just how this works, right?

Speaker 1: Right, I know, so that's not what I'm arguing. I'm just saying that if our goal is to get to a point where we have inbound fees, we should be doing inbound fees because every sender has to update to do that. We should just do it, right? If our goal is to experiment, for like: Can we build something that demonstrates inbound keys are useful? Let's build something and actually try it. Then, we need to talk about how do we get the best data with the minimal amount of effort. And I'm still very confused about your take here that fewer nodes need to update in order to get the best data. Because I don't think that's really accurate here.

Speaker 0: Yeah, I think we're just looking at this very differently. You think everyone needs to update.

Speaker 1: I'm really trying to understand your view here. I'm not saying everyone needs to update. I'm saying, in order to get good data, you need basically the vast majority of senders who are sending through your routing node, and I thought you agreed with that.

Speaker 0: It doesn't necessarily need to be the majority. It can be weighted by volume they give out. And I think the other thing around the channel update is that we would have a very clear signal. We would have a clear signal of which nodes are even using this feature in the first place, right? If we do this, and none of the LND nodes actually do it at all, and there's only two of them, and they say it's cool - okay, well, they can implement that on a side by having a custom message or something like that. Or adding custom data to the TLV, and that could be an RPC on the side. But if we do it, and then we're finding the vast majority of them are actually setting it, then we can say: Okay, well, we can go talk to those individuals. We can say: How's it working for you? Is it actually resulting in better traffic? They can look at a lot of stuff down there

Speaker 1: You can announce the data in in both designs, right? I don't think the whether or not you announce the data in the channel update precludes whether or not you do it in this restricted negative case only or if you do it by negotiating with your peer and then you also set a TLV bit and just say: Hey, I'm using this feature, come talk to me. I think that's an unrelated question. You can do both.

Speaker 0: I think it's related because the mechanics of these are very different, right? I think we can, at least, agree on that. The mechanics are very different.

Speaker 1: Right, and I want to focus on the mechanics and the material difference with the mechanics, and whether which one is going to get us more useful data easier, quicker.

Speaker 0: Sure, we can look at the mechanics. I think one mechanic is indirect. The other one is very direct. In any case, this isn't a global level update basically, and people that have different vantage points of how to best collect the data, they can do so. We can then see at the end, which one worked or not. Maybe it doesn't do anything. Both routes are feasible because this is this is a fully optional thing. You would say it's not optional. I think that's what we diverge. I think it's what we diverge. Do you think it's optional? You think it's not optional? I think it is.

Speaker 1: Irrespective of if it's optional, let's ignore that for a moment - I'm just trying to understand which one is going to get us better data with less effort and less nodes that have to update. And I'm very, very unconvinced by your arguments there.

Speaker 0: Well, last thing I'll say on that. If you're saying less nodes to update, go back to that example of a node having 100 channels, which are each equally utilized as far as doing sourcing inbound or routing. In that case, it's 100 versus 1. So, that's just one counter example. If you reject that, you can.

Speaker 1: But it's not just 1. You're saying: Oh, it's just one sender has to update. But it's the sender weighted by total volume.

Speaker 0: I'm saying 1 minimally. Yeah, and maybe there's one predominant sender.

Speaker 1: Okay, and my argument is if there's one predominant sender routing through your node, probably they're kind of close to you. And almost certainly, you have one or two channels with peers that are very close, probably the direct neighbor of that node. So, you don't need to...

Speaker 0: The sender may be categorized as the same Wallace software, but not necessarily the same individual. Yeah, like last time, to paraphrase, I think [Redacted] was like: Hey, I don't know if this is right or not, try it out and see if it happens. I think [Redacted] expressed something similarly. Just try it out. So, I think we're just at: Let's just try it out phase. I think [Redacted]'s saying maybe another one will give you more pertinent experimental data. I think that depends on a number of caveats and [Redacted]'s envisioned scenario and who's not. It just doesn't feel like we need to be in a gridlock to let people launch experiments that can be rolled back very easily just not setting the field.

Speaker 1:  I'm not suggesting any kind of gridlock. I want to understand what the...

Speaker 0: Well, yeah, [Redacted], you posted on a PR and said: Don't do this. You posted on a PR and said: Don't do this.

Speaker 1: Yeah, well...

Speaker 0: If that's not gridlock, what is?

Speaker 1: ...because I think you are also pushing other people to - Don't do this and let's have a conversation about it and then you can do it is a very separate question. But, you are also...

Speaker 0: Well, but yeah, the thing is, it feels like we have a conversation, but we have a very different view of routing.

Speaker 1: No, I don't think we had a conversation because the conversation we had concluded with: Let's have this conversation again. So, that's why I'm trying to have the conversation again.

Speaker 0: Yeah, I think we're here again. Yeah, I think I think we just have very, very different views on how the routing network works, what routers have been asking for over the past few years, the the level of pertinent usage we need to get for experimentation purposes. And to me, the only way to resolve that is just try it out. If we try it and nothing happens, no one uses it - we're not able to get pertinent data and you're able to launch another experiment that's a slightly different way that gives you very, very strong signals. We'll clearly look at you know, what actually happened empirically, right? Sometimes, just to do is to actually find out, right? With that said, I don't know if anyone has...

Speaker 1: Right, you have two options in front of you. Sounds like we're out of time.

Speaker 0: Yeah, I think we're out of time. I don't have any other final, final stuff. One thing that I think we're going to look at, not for this one, is the WebSockets thing. I think it sort of got nerfed because we realized we couldn't just do raw without TLS on the browser level, and then we added the DNS stuff. But I think maybe, you know, picking up on the side, but something super, super on the side.

Speaker 1: It's still on the to-do because it makes TLS easy because you just slap engines in front of it, instead of like having to have the full proxy. To be clear, I was the one who complained about it or kind of pointed this out, but I still think it should be done. It just it's less important.

Speaker 0: Yeah, we need to do the DNS advertisements first, and then we can do this. I also wonder, does Mutiny Wallet use this or do they do something else? Like the...

Speaker 1: I think they have their own custom proxy because they want to talk to all nodes, and so, they don't. Plus, they want to talk to other stuff. So, they have their own custom proxy currently, I think. I don't know if they support browser or if they just support Node.js, then obviously Node.js, you can do TCP directly. I'm not 100% sure. I guess I shouldn't speak for them.

Speaker 0: I've seen a demo, and I think it's browser, but something to check out.

Speaker 1: Yeah, I know they have a demo. I think the demo uses a proxy, but I'm not sure.

Speaker 0: Cool. Okay. Alright. I posted my notes.

Speaker 1: I have an unrelated question, if you have another 30 seconds, [Redacted]. You guys announced doing your routing changes. I couldn't find good sources on exactly how it does, but my main question.

Speaker 0: Like pathfinding?

Speaker 1: Yeah, your pathfinding scoring changes. My big question was: What the probability distribution function you're using for a priority channel?

Speaker 0: Good question. I'd have to check the code again, but I think it's just a uniform one, like the other stuff. The new one is the one that breaks away from a uniform distribution.

Speaker 1: Right, I was asking about the new one. Is it just an exponential?

Speaker 0: Yes, so the new one is like a custom bimodal exponential function. I can send you like a Wolfram Afro link, so if you want to see where it actually.

Speaker 1: Yeah, I was playing with some similar stuff and was curious what you did. I read through several of your posts and none of them actually explained in detail what the exact function was. It just said: We're using a thing that assumes it's at the edges, which makes sense. It's a good insight, but I didn't know what the actual function was.

Speaker 0: Yeah, there's something called Desmos, I think, where it basically lets you plot it, and then even mess around with it. If I hang on for a second, I can probably find a very direct link.

Speaker 1: Well, yeah, I mean, if you've got it, if you don't, that's okay too. And are you just chopping off the ends based on what you know about the liquidity? Or you're using historical weighting of that function based on historical failure attempts or success and failure attempts? Because I know you just used like historical success and failure and not like liquidity bounds.

Speaker 0: Yes, so now, the main change for this one is - generally, we didn't use liquidity bounds at all before. It was just a store for success and failure. But now, both of them use liquidity bounds, and then this other one it basically builds in a more kind of like pessimistic view.

Speaker 1: So, it takes the probability distribution function and chops it off at the liquidity bounds and then uses that basically? Is that what it does?

Speaker 0: Yeah.

Speaker 1: Okay, cool.

Speaker 0: I don't know if anyone in the chat knows what I'm looking for. I'm looking for, I think, it's called Desmos. It's a graphing thing.

Speaker 1: If you happen to know where it's linked from, I can go find it. You don't have to dig for it.

Speaker 0: Yeah, I thought it was linked in the actual PR. But maybe... Oh, here it is. I found it.

Speaker 1: I did not read the PR. I only read the announcement.

Speaker 0: Alright. I found two things. I don't know if one of them is what I'm looking for, but I think these have a little bit less information.

Speaker 1: Well, that's alright. I'll figure it out. Thank you so much.

Speaker 0: Yeah, and this one has like a slider too.

Speaker 1: Yeah, interesting. Okay, you guys have much more complicated - okay, cool. Thank you.

Speaker 0: No problem. Cool, alright.

Speaker 1: Oh, one last question. Was that like determined by doing probing or was that more experimentally determined?

Speaker 0: So, I think initially, it started with a sort of hunch, like looking at, for example: Is the uniform really the best contribution to apply to this? I think it was sort of verified just by looking at some initial experimental probing basically, and also you can say inferences based on the lack of actual liquidity management that many individuals do and also that most channels are single funded as well. So, it was kind of a combo of both an assumption and then some basic probing to verify. And then, we're looking at what we look at right now. I think also it's the case where there's a value that we can modify that controls how imbalanced things are - basically what the modes look like as well.

Speaker 1: Sure. Cool, thank you.

Speaker 0: Not a problem. But yeah, I think we'll do more writing on that as well because I think that was just initial blog. It was a section in a blog post of a bigger thing. But I think we want to kind of do something that zooms in a little bit more on what the process looked like, and once our experiments get further, what change that we actually saw.

Speaker 1: But that's that'd be that'd be interesting. I'd be interested to read that. It was a good insight. I think we'll probably do something similar based on it. We have a few more things that we do beyond the just the liquidity bounds. We're also working on on making more, more useful, but we'll probably do something like your modified probability distribution. I'm not sure if we'll use the same one or not.

Speaker 0: Cool, yeah. I mean, I do have that post coming down in a month or so. There's stuff in the comments obviously, but that's not the same. It's like actual bloggers. Cool. Okay, I posted my notes and yeah, I guess thanks everybody.

Speaker 1: Thank you. Cool.

Speaker 0: Peace.
