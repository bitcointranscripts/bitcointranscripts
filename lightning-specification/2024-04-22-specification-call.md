---
title: "Lightning Specification Meeting - 1155"
transcript_by: Gurwinder Sahota via tstbtc v1.0.0
tags: ['lightning']
speakers: []
date: 2024-04-22
---

Agenda: <https://github.com/lightning/bolts/issues/1155>

Speaker 0: Cool. Okay. They have four or five things that I think are all in line with what we have already as well. First one is the spec-clean up. Last thing we did, I think we reverted one of the gossip changes, and that is going to be in LND 18. Basically, making the feature bits to be required over time. After that, is anything blocking this? I need to catch up with PR a little bit. Yeah, because I think we do all this. Yeah. Okay. Yeah, I think this is starting to land. Let me just come real quick.

Speaker 3: I assume all of this is in CLN since [Redacted], you wrote the PR.

Speaker 4: Yeah, and I found out that I broke LDK, but then we undid that, so it's all good.

Speaker 0: Yeah, I think with that, we should be good. Let me just check out this large deleted block. Oh, we deleted some of the old test vectors. Okay. Alright. Let's do this then. I probably need to do actual line by line, but I think we all do it as is anyway. So I got to automatically hit an approval on it.

Speaker 4: Yeah, there's some formatting changes [redacted] suggested that I should probably go through.

Speaker 0: Yeah, we don't even use the old anchors anymore. We don't expose that at all. Okay. Alright. I will put this on my list to actually take a look at today. Just to give the final stamp on it. Okay. Next is constant size failure onion decryption.

Speaker 5: So, this is just a clean up where I added some rationale why we do the 27 hop decryption even if we have less hops available. But the question is whether we want to still keep this requirement. We in LND do it, but network latency is so bad in general, so it’s — I think the decryption of those dummy hops will not have any effect on disguising the failure of the route.

Speaker 0: Yeah, it's definitely a best effort basis kind of thing, where it's like you should continue to do it, but you can stop short.

Speaker 3: t's just kind of a thing where it's like if you know something that could be used as an oracle, might as well try to eliminate it there. Good thing around the 20 to 27 because I think we have like a max hop value and we iterate over that, and then we continue decrypting afterwards.

Speaker 6: Exactly.

Speaker 3: I just wonder whether this requirement is even remotely useful. Like, this definitely feels like it was a mathematician talking about digital attacks and not actually controlling the deployment.

Speaker 0: Well, yeah. Has anyone measured? Not really. But I guess the thing is, if you can do it, I don't think it adds significantly more to like the latency. At least, on our end. I guess that would be an argument again for removing it, basically. For some reason, it took like a second more to…

Speaker 3: The argument to remove it is just to simplify the spec. That would be my…

Speaker 6: I would think that this definitely has an effect. It is often easy to tell whether a payment came from a given node, but it is not completely trivial to tell whether a payment came from a given node. Whereas with a timing oracle, it absolutely is. While I'm sure many nodes have other issues where they behave differently based on whether they sent an HTLC, nodes should fix those, and this would be one of them. 

Speaker 0: I mean, the other thing is that everyone does it today. Does anyone not do it? Installation-wise?

Speaker 6: We don’t do it directly, but we…

Speaker 0: I just check we do it.

Speaker 6: In many cases, we will be decoding the error HTLC asynchronously later, so not like blocking the message pipeline. It shouldn't necessarily be directly measurable anyway.

Speaker 0: Yeah. We loop over the 27 basically and keep going. On one hand, I think this also updates the spec because the spec said 20 times and now, it is 27 in terms of the max thing. So that's one part of it. We can even do that independently of the rationale or something like that. But yeah. So, I think that part about it is at least an update to the spec that I guess we just forgot about when things became a little smaller after we went to TLV onion.

Speaker 6: I mean, we could also make the normative section of the speucs simply say: You must prevent timing side channels that reveal whether you are the sender in a HTLC.

Speaker 0: Yeah, that way just make it more generic.

Speaker 3: So, consider though — I feel like if you do the decryption even three times when you're the sender, you've already hidden that. I mean there's no reason not to, I guess, to do the full amount, but I think the situations in which you can determine the sender exactly is extremely, extremely limited.

Speaker 6: I don't think that's true. If you are a lightning node and your peers are in the same data center, you can almost certainly get lower noise. So if you're both on AWS, you can probably get lower noise. 

Speaker 3: But does decryption actually help that? If they're in the same data center and you do the extra decryption, then you know that just from having the network latency — so you bounce the packet, it goes back to the source, the source does the extra decryption. But you're like: Okay, if the noise is gone anyway because the network latency is near zero, then you know that thing didn't back propagate many, many different network hops.

Speaker 6: No. I mean the peers should behave the same whether they're back propagating or not. They just continue with the commitment update.

Speaker 3: I mean, is anyone — well, I have to be misunderstanding that.

Speaker 6: I'm just not understanding what [redacted]’s point is.

Speaker 3: Okay. So you're saying that in the situation when you have the two nodes in the same data center, right? And that the noise is near zero, the latency is near zero, right? So, if an erroring node bounces the packet back and the other node is the original payment sender. Yes, you can do the extra decryption, it takes an extra time. However, if they retry it immediately, even with the extra decryption, the time that it takes to do the extra decryption is still going to be smaller, most likely, within a standard, inter data center network latency.    

Speaker 6: Are you saying if the payment gets retried?

Speaker 3: You're cutting out. I'm saying it's a what?

Speaker 6: Are you saying if the payment gets retried, then the retry will happen right away?

Speaker 3: Even with the extra decryption, the fact that there's no latency inside the same data center is going to leak the fact that it didn't leave the data center.

Speaker 6: Oh. That only applies if the node is the same hop and they retry through the same first hop. If they have other channels, they might try through a different peer. Similarly, you shouldn't be retrying right away. I mean, LDK doesn't, I don't know if other ones do, but you should wait a hundred milliseconds before you retry a payment.

Speaker 3: Okay, but then what's the value of the extra dummy decryption?

Speaker 0: Yeah, I mean, [redacted], as people have done scientific measurements here, not necessarily. I guess the thing is, I feel like there's two paths here. One is, like [redacted] was saying, make it more generic. Basically, that should take care to avoid timing side channel. The other one is basically saying: Well, it's a bug fix to go from 20 to 27 because 27 is the real up limit now; and if we weren't doing that, we should do that change there.

Speaker 4: Yeah, I'm prepared to bet good in the money no one can measure the side channel. As far as I can tell, the only thing you can tell us with the reattempt, right? There's no other signal I can think of. Unless they're actually making the payment as well, in which case I'm assuming that they know they're making the payment, right? But the latency on the error return. So, you're basically talking about the latency about retransmission, like the second transmit. Like, network is all over that. There's no way in hell anyone is gonna measure the latency of the packet decryption. At least, I'm hoping this is true because I looked through our code and I cannot find it. We do definitely do not put the spec here and I'm pretty sure we don't actually, we seem to stop decryption as soon as we hit a valid HMAC rather than looping. I'm tempted to remove it from the spec. Seriously, if you put any noise in your reattempt at all, then you're gonna — especially in the order of milliseconds — completely blow away any effect that you're having here. I would much rather put a zero to five millisecond sleep in payment reattempt and then just forget that this ever existed in the spec.

Speaker 6: So, there's a lot of studies on more general decryption timing oracles that are of similar, a few US, a few microseconds kind of timing oracles, or like 10 microseconds, where if you can get it repeated enough times, you can absolutely measure it. If you're doing it once, you probably can't. But if we're repeating it a handful of times and you know whether you — I don't know if anyone decrypts when you receive the update fail rather than waiting for the commitment or just if there's a stream of regular HTLCs. I would bet good money if you have a hundred thousand HTLCs, you could tell.

Speaker 4: The decryption time is not what it's about. It's about the latency. Like, if you're not delaying the outgoing payment, that's a much bigger problem. That's not mentioned anywhere in the spec, right? I think we should get serious and we should do that, right?

Speaker 3: That's exactly my point. Yeah.

Speaker 6: Yeah, I mean, you should be doing that too. But both are a problem because you can listen to the ping.

Speaker 0: Okay. So, it seems like we're going in the direction of make this generic and just say: Hey, you should watch out for eliminating timing side channels and remove our prescriptive directive here, as far as the shard encryption.

Speaker 4: I would much rather have something on reattempts saying that you should use something to obfuscate the timing. That's much clearer.

Speaker 6: To be clear, that's also not sufficient if you block the network pipeline waiting to decrypt. Because someone can send the message, send the ping, and then measure your response time directly. So, you do need to do both in some way.

Speaker 0: Both being shard encryption and — wait, I think I want to clear things. One is like randomized attempts basically, and the other one is the encryption thing, right?

Speaker 6: Right. You have to hide the decryption time somehow. So you can either do the decryption async in some other thread or go routine or whatever. Or you can do it in line and always decrypt 27 or whatever.

Speaker 4: You don't need to hide the decryption time. You need to hide your response time. You're overly focusing on the decryption time. The main thing about the response time is not decryption, it's the network latency. We should tell people to hide their response time.

Speaker 6: I misunderstood. When you said response time, I thought you were referring to, for example, retrying the payment.

Speaker 4: Yeah, that in this case is…

Speaker 3: Yes.

Speaker 6: Yeah. So that is just that, right? You need to hide the network. You need to hide both the response time in terms of how long it takes for you to move on to the next message in your message queue, and also how long it takes for you to go retry the payment.

Speaker 4: Well, that's implementation dependent. In our case, where separate processes would be processing a ping or something from the one that's actually handling this error. 

Speaker 6: Right. 

Speaker 4: So you're not really gonna get that. I see what you're saying. Yeah, if you're doing it all inline, then you would worry about ping times potentially. But yeah, I think perhaps we need something broader that say — gosh. That's a big task, but it would be nice to go through and mention all the cases where you should probably insert some random delays.

Speaker 6: Yeah.

Speaker 0: Well, yeah, I mean, because like you're saying, the trial and error was sort of like a hand wave: Hhey, you should do something; here's something you should do. We can make it more generic and then, if someone really wants to go by and do all the passes, that is a path as well.

Speaker 3: I think in general, like any of the spec recommendations, should at least be very clear about what the recommendation is intending to solve, which is, I think, ultimately what this PR does. But I think it reveals that this is probably not the thing that we actually care about.

Speaker 4: Yeah.

Speaker 0: Okay. So, is the action item here on the PR to make this more generic? That you should add randomization for retries, basically? So, it shrinks somewhat? And then, we'll keep doing the 27 hop thing because we already do it. We're not going to — I don't think we're going to remove that. Maybe we'll benchmark to see exactly how much extra latency it adds on our end. But yeah, we already have some crazy scheduler that's doing stuff.

Speaker 4: Yeah, I feel like somebody poked this and now, we've just given them a whole pile of shit to do, which is perfect. 

Speaker 3: Go for it, [redacted].

Speaker 4: Yeah. You touched it.

Speaker 0: Okay. Alright. So, for now, I put down to just the direction of making this more generic, basically. You can remove the text. We already do it as is already and the rationale there that you should be watching out for this stuff at least.

Speaker 4: Yeah, I think [redacted] identified at least two latency on pings. We should probably fuzz those a little bit because that has some idea of how busy you are. But the other one is latency on retries. If anyone can think of others, that would be a fantastic thing. I would like to see that spelled out, especially everywhere that you should be adding false latency, put that in. I think that would be a much more concrete thing.

Speaker 0: Cool, okay. The ping thing, and also the randomizer retries as well. Okay. This is the one from the other week. If we want to go full on, I've got two ACKs. Alright. Shall I merge it? I think people  were saying should we do it everywhere. We can only start here, I guess. At least, this is the code and being annoyed that — so, I'm just going to merge it.

Speaker 4: It's pretty. I say yes.

Speaker 0: Yeah, it looks nice. Okay. I just merged that. Next thing is liquidity ads. This is something that [redacted] stated: ‘I posted a new design for liquidity ads. This one's more open to extension. I believe it would unify the LSP specs with both flips chasing a concept ACK on this.’ This is 1153. Or I think it's a new PR that I think tries to, I guess, will replace the other ones. I think we talked about decoupling the negotiation from whatever the mechanism was. If you were going to do the CSV versus not. I haven't checked it out as is, but I think they’re looking for a contact from people that are following this work stream.

Speaker 3: I'm not caught up on it.

Speaker 0: Okay. I'm not myself either, but I think you should look for a concept ACK. It looks like some of the people started to look at themselves. I guess there's a relation to the LSP spec stuff, which I'm not following too closely myself either, and it has test vectors. Cool. Okay. Next, basic payments. I think this one's still in a draft phase, built on top of other stuff as well. I know there's a talk about this at MIT. I haven't watched all the videos yet. Any immediate thing that needs to be done here? I think we were working on an implementation and stuff like that.

Speaker 8: Yeah, I'm still working on the LDK implementation. I have some updates locally to the feature bits and stuff, but I haven't pushed them yet.

Speaker 7: Cool.  Okay. Next, STFUs and quiescence. So, I think there's a little bit of this. I think we were doing interop with Eclair, and I think now that I think is actually integrating the explicit resume part of it. Am I right about that, [redacted]?

Speaker 2: Yeah, so I submitted a PR to [redacted]’s branch that includes an attempt at a spec for an explicit resume message. [redacted] replied back to that this morning. I still need to respond to their comments, but they said that he was gonna experiment with it in Eclair and see what happens.

Speaker 0: Okay, and I can link the…

Speaker 4: Scroll down to page 200 of the comments.

Speaker 3: Sorry.

Speaker 0: Okay, and then I might have to link the — so this is the version of that they just opened against [redacted]’s branch. STFU and then, go on. Carry on. Cool, and I think we have code for this also, [redacted], or is this pre-interop?

Speaker 3: We don't have code for the explicit resume message yet. I mean, I think we're still kind of TBD on whether — I haven't decided whether I want to do it or not at the moment because I think it's a good idea in principle. I put the spec together. I think I have slowly worked on [redacted] to like change their mind, and I think that there's been some loose buy-in now. But until someone else is like: Yeah, let's definitely do this, I wasn't gonna prioritize doing it. I might do it anyway, but it's just whenever.

Speaker 4: That's worth including this just for the backronym. I love that.

Speaker 0: I can't raise my hand right now. No, that's cool. Cool. Okay. So, it looks like [redacted] is responding to it. I like it in principle basically, so then that way it's sort of its own isolated thing. People can use it for anything else in the future. Just we have got that there already.

Speaker 3: In general, I want to remove the number of situations where people have to have deep knowledge of many different proposals in order to understand how a certain thing goes together. Because without something like this, you would have to define it in both dynamic commitments and in splicing when the quiescence is considered risen, which just seems to me like a layer violation.

Speaker 0: Okay, cool. Alright. So, I’ll check that out in the background. Next is the trifecta of splicing and dynamic commitments. I think last time — [redacted] isn’t here —  but I think we were just discussing sort of overlap dynamic commitments and splicing and things like that. I mean, ‘cause I remember like we discussed, I think it was New York last year, where if we were starting in a bubble from idea land, it would have all started at the same. But obviously. slicing has progressed pretty significantly and we didn't feel like it made sense to sort of try to co-author or direct it all towards the thing that we were working on. I think maybe [redacted] and I had sort of disagreed about the importance of giving people a path to upgrade Taproot channels that didn't require always broadcasting that transaction, where the thing that we're working on right now, you can defer that part of it. But it's also the case where what we have right now does split the negotiation from the execution, and one part of execution pass for the Taproot channel thing does require that whole kickoff thing, but if you just wanted to use this to upgrade a dust limit, you wouldn't necessarily need to use that at all. And that's, I think, where some of the back and forth was. Probably doesn't need to be on the splicing PR itself, but that's sort of like where it ended up.

Speaker 3: Well, the reason that that discussion kind of got opened up there is because [redacted] was like it'd be nice if during this like splicing transaction, we also could change the output type; and I was like: By all means, go for it. But this does not change the reasons that we want to do it in dynamic commitments because we want to be able to withhold that output conversion transaction off-chain indefinitely, which you can't do if you are splicing in. You can actually do it if you're splicing out. If you're splicing out, then you can't invalidate the transaction by double spending one of the inputs. But unless we can make it such that you can irrevocably commit an input to a splice, then you can't withhold the splice transaction. You have to actually broadcast it in order for the post-splice to be usable safely.

Speaker 0: Yeah. I think we had different views on how important it is to make sure people don't have to go on-chain to upgrade basically? For me, it's fairly because I think it'd be a disaster if the entire network had some bug and we all force close basically — or rather a bug for the closing. They're still open you can say, but it would look like that, right? That could be a weird event. Also, hey, fees are high right now. Maybe they won't be high forever basically. But I think that also impacts it that this would let you hold it off-chain and then decide to do that, but then still have the benefits. To me, it's related to what in my mind is like a path to get to PTLCs, in that if we do the taproot gossip stuff, the new channels can use that itself. You can then maintain the existing channels and update a feature bit if you have that, kickoff to the new tempered output off-chain basically, and then PTLCs can flow through. Then, people will go on-chain as they need just because of normal stuff happening — co-op closes or HTLCs or whatever else versus indirectly creating this trigger point where a lot of things end up going on-chain. 

Speaker 4: So I assume you want actual mutual close to do cut-through and basically close the old one, not push the Taproot one on-chain, right?

Speaker 3: So that's an open question.

Speaker 0: Good question, yeah.

Speaker 3: I think for Taproot assets reasons, we don't, but that is an option if you don't have assets in-channel.

Speaker 0: Yeah. So you could do the cut-through on co-op close, or you could just say, we'll do that thing and then do it. I mean, the cut through is better because of one transaction on-chain, but I guess we haven't got to that part, go to us, so. But it is something that you should do ideally if you're able to.

Speaker 4: Yeah. See, if you don't do that, then you're doing a fair bit of work just to defer the on-chain. You're not ever getting rid of it. You're just deferring it.

Speaker 3: There's still value there though. So, you might ask yourself the question: What is this actually buying you? You still have to pay the fees anyway. You still have to budget for them in advance. But the difference here is that with splicing, you have to actually wait for the on-chain transaction to confirm before you have full service quality from that channel because you have to take the most restrictive subset. Whereas now, once the negotiation and these signatures are exchanged, you have full usability of the post-upgraded channel as soon as that negotiation's done. I think there's value there. You can decide how much engineering you want to do in order to be able to support that. But at least for us, I think we see it's enough for us to be prioritizing it, so…

Speaker 0: Yeah, there was maybe a slight misconception as far as I think they thought that you always had to spend the funding output in order to do a change, but that's not the case. Certain changes may want you to spend the funding output, but certain changes are just like:  ‘Oh, this is a new dust limit,’ and that's what we're gonna implement first. We're gonna do the parameter stuff first because it's a lot more contained versus needing to worry about the new change transactions and pick all that stuff up.

Speaker 5: Yeah. Definitely the non- on-chain changes are pretty straightforward. That's what STFU was originally designed for, right? ‘Cause that makes it easy. I'm gonna have to think harder. I mean, the splice case, we liked it because you generically don't care. But if you wanna do a lazy splice and leave that one sitting around, you really have to care about their outputs. You have to make sure they're standard.

Speaker 3: Well, it’s the inputs. 

Speaker 4: No. If you don't have any inputs, if you're like: Okay, we can't do any new inputs, we can't splice in, but we can splice out. But now, you really have to care that their splice out is valid. You've got to make sure that their outputs are standard and stuff like that. Whereas with generic splicing, we didn't have to care. You put whatever you want, and if it goes in, great. If it doesn't, well, we're stuck. We still got the old channel. But if you want to assume that, then you need to be tighter. That just introduces that whole: Okay, well now we've got a new version, a new SegWit version or something; we've got to go through this whole standardness check thing. Although I think they might be standard, I don't know. But yeah, you have to check your outputs for standardness in the case that you're talking about, right? Where you want to be able to assume that it exists. 

Speaker 0: Yeah, in this case, It's already constrained, so... 

Speaker 4: Well, you did it splicing. But we generally didn’t constrain it, right? Because we didn’t have to. 

Speaker 6: You definitely can do that for inputs.

Speaker 4: Yeah, for inputs, that's right. For inputs, we couldn't do anything anyway, so we didn't care. But you're talking about a subset where you can

Speaker 3: You might be able to employ some fancy cryptography tricks that cause people to irrevocably commit inputs, but I don't think we want to do the engineering for that either. 

Speaker 0: Well, yeah. I think like you're saying is — I think this started from [redacted]’s points — if we're doing this, we should always show RBF in the funding output. I mean, I think you can do that, but I feel like my recommendation would be just to get splicing as is finalized versus adding yet another thing on top of it basically. It's nice to be able to do that, but there's a lot of other considerations just because of inputs and outputs and standardness and all the other stuff. So. I'd just be like: Keep it as it is; you can add it later and then, at a certain point, maybe we can combine stuff. That was at least the lofty hand wave from New York last year. I think we can still see where that is going to go. 

Speaker Alright. Next thing. So one thing that [redacted] and I are doing is we get to make progress on Taproot Gossip. We always think we'll ship it whenever possible. That's one thing I was playing on sort of like re-engaging with internally for us as well. Right now, like we have the spec up there. It went through a few iterations. We had some feedback from [redacted] and co. in New York last year. [redacted] has some PRs up that implement the current thing that we have right now, but we sort of decided to pause just because we don't want to go super far ahead and then stuff is super different. 

Speaker 4: Yeah, I gave some feedback last week too. We've woken up. We've given some feedback last week. In particular, we're trying to retro in the — so you can use the Taproot Gossip or the Taproot. The V2 gossip for V1 channels. So bridging that too because we want to eventually have like: Here, you can just gossip it. You can gossip everything. We went back and forth on how to do that, but it's pretty simple. There's just a couple of light language changes in the spec to kind of decouple them a little bit to say: If you support Taproot Gossip bit, then you use the Taproot Gossip, even if it's not a Taproot thing. But in which case you have to do both, right? You have to do the old school and the new one. It's when you send the signatures, right? So you end up sending the announcement signatures message to say: Hey, let's exchange signatures. You end up doing announcement signatures and announcement signatures 2.

Speaker 0: Ah, have to send both.

Speaker 4: But you'd already split the — the option Taproot is separate from Option Taproot Gossip, so we already have a separate feature bit for it. So in theory, you can support. The way we plan on implementing it first is we plan on implementing the option Taproot Gossip first. So, we will do all the gossip things, including for old channels. It just requires some spec cleanup. It means that that some of those message numbers are odd now, because then you can just spread out and not care and stuff like that. But yeah, so just minor feedback.

Speaker 0: Okay, cool. Yeah, I think we implemented the broadcasts, — sorry, I think we implemented the duplicate with the other one, yes.

Speaker 4: Yeah, it's still in both. It's gonna be kind of — I mean, temporarily it'll double our gossip load, but we're okay with that.

Speaker 0: Cool, okay. Alright. It looks like we're moving things along. Okay, feature bit, time. 

Speaker 1: I had a question. I was jumping back a little bit, but with the dynamic commitments: If I have a dynamic commitment that's already pending — right? — and then I do another one, are you chaining multiple transactions together? How do you have it?

Speaker 3: For simplicity reasons, we're gonna chain the kickoffs, but there are actually subs in the spec where I put like notes for review, where if you wanted to apply. So if you don't, we have to be able to revoke the kickoffs, which means that we need to do asymmetric kickoffs, and that will kind of explode some of the complexity. I just figured, why? Like, why not just do the conversion as a chain? If people are doing this so often and they're like: Oh my God, it's so expensive, we can do it later and justify the engineering by actual user pain. But for now, we're just gonna chain them if you do multiple. You might just block it to start. We might just say: Don't do multiple.

Speaker 0: Yeah, and if you're updating your dust twice, it's going to be like: you update fee and then, update fee again. There's no, at least by now, other channel type that we were considering to be implemented. So, it's either a revoke thing or chain it, but I don't think we're doing a soft fork tomorrow. So yeah. I'm just a little like that person.

Speaker 1: I'm just trying to think ahead. In a situation where I have two dynamic commits chained together and then, I have splice and the RBF of splice. Like, how many versions of the funding am I keeping track of? It sounds like it might get a little complicated.

Speaker 4: The question is then: Did you cut through or not, right? I mean, at some point, you go: Well, it's been five years. You've upgraded this channel like twice or something and you've got a chain of them and now, you want to splice. At that point, we think about: Do you go back and you say — the same way with mutual close, right? Do you go back and you actually splice the original one so you can cut through? I think the answer is probably yes, but if there's three people in the world do it, it's cheaper to pay the fees than it is to just for engineering. I don't know. 

Speaker 1: And probably we don't want to do a dynamic payment on top of a pending splice, like a low fee splice that never goes through. On top of that, it sounds terrible

Speaker 4: It's dynamic on top of a pending splice. It's like you're not saving a transaction anymore. So I don't think that's. 

Speaker 1: Right. Just RBF the splice. That makes sense, yeah. 

Speaker 4: Replace the splice, yeah.

Speaker 0: Cool, okay, Alright. Nice to get some updates on gossip stuff. I think on channels, I think Eclair in the background is still working on some interop stuff. Peer storage backup. I think we have a PR that in-progress. I think there's some activity on the PR itself as well, but the PR is not going to be in our upcoming release anyway, so let's push that a little bit. Okay, it looks like there's still something I can do. I wasn't sure if the OP had moved on to other — it looks like they responded two weeks ago. Okay. Channel jamming stuff. I know there was a thing this past week. Are there any new ways or new insights that people got from that?

Speaker 7: Yeah, we tried to break it. We didn't manage to totally break it, which is good, but we got some cool new attacks to think about. I'm going to write a Delving post about it once we've sort of post-parsed the data a bit more. But spec stuff, I owe a clarification on that blip about interpreting as a scalar. Otherwise, there's nothing here.

Speaker 0: Cool. Check. Offers.

Speaker 9:  Yeah, so actually on offers, I sent a small comment on the PR recently. It's something that we already proposed a long time ago, but it's to make the node ID increase it — in case we have a banning path, that makes the QR code a bit smaller, and I don't see any downside.

Speaker 4: I think the problem is you can't create multiple paths with the same node ID terminating it. That's the problem. So it has to be a transient throwaway because of the way you create the paths. I think that was the issue.

Speaker 9: So, if you want to keep a node ID that people can recognize, you can still put the node ID, but it would be optional. The idea is if you want to optimize for QR code size, you don't need to put it. For instance, for updates, we don't need to put it.

Speaker 6: The only question for me on this is not whether we should do it — it seems like a perfectly fine idea. It's whether we should do it before we merge BOLT 12. 

Speaker 9: I think we should. 

Speaker 6: Because we're at a point where we're tipping topper and encouraging people to integrate in BOLT 12, and we got to draw a line. We got to draw a line real soon.

Speaker 9: So actually, on the Phoenix side, we've already implemented most of it. Before we will release it, we want to have a default offer for Phoenix, and this default will stay like that for years. So, we really want this default offer to be as small as possible, and that means no node ID.

Speaker 6: Yeah. So I mean, we're gearing up to ship a release soon that we have a bunch of BOLT 12 fixes for. We anticipate, potentially, some large LDK users going live with BOLT 12 with it, and I think it's too late to add that now. So I mean, that doesn't mean we can't just wait to merge BOLT 12, add it in three months, and then wait another two months before people adopt it, but...

Speaker 9: Because the idea is that for Phoenix, we would generate the offer completely deterministically. So, if we need to change things later, then we'll have two versions.

Speaker 6: Well, I think maybe more generally — I mean, probably people are only going to support send for a while, right? So, we can ship send while we work on this. We can ship send. Do cross-compat. Maybe even merge BOLT 12. Then, add support for this, and have it in place in all the senders by the time anyone has received support.

Speaker 9: It's also a quite simple change.

Speaker 6: It is. I agree. It's just missed our release deadline. It was purely a deadline question.

Speaker 4: I'll look immediately after the meeting. But I think, I mean, it is trivial to at least read it, so I'll take a look.

Speaker 6: Yeah, I don't know if we'll implement receiving to it because it's a little weird, but we might eventually.

Speaker 9: But if you can just implement sending to it, that's good enough for our use case.

Speaker 6: Yeah, of course. We'll implement that into it, no problem. It just missed this release thing.

Speaker 0: Cool. Okay, I'm going to write that down. 

Speaker 6: Merge soon. Like real soon. 

Speaker 0: Alright. Any updates on DNS based offers? 

Speaker 6: No, that's still on [redacted]’s plate. I blame [redacted].

Speaker 0: Cool. Attributable errors didn't make it into our equipment release. I think I know a bit [redacted], [redacted], and [redacted] did some iterations as far as HMAC size and things like that. I'm not super caught up on it myself, but also the PR hasn't received updates in a bit. I think [redacted[ been doing some stuff from the edges now, so maybe we can re-engage them on this to see. Let's pick it back up again. Okay. Then, there is this channel action thing, which has been there for a while. But I guess with that, any other stuff outside of the core?

Speaker 6: What's the state of BOLT 12 and CLN? Some people have been rumoring that it's outdated compared to the spec, but I haven't heard anything like that from you. So, is this just a rumor? Is this true?

Speaker 4: It's probably true. I need to go back and revisit and update it. So we have the issue — I have some patches that basically catch up with the spec as is. In particular, there was a spec change. The short channel ID option. I have a PR for that that basically merges in the short channel ID stuff in the next release. So, I'm hoping to get it up to minimal spec standard for the coming release, which is nominally 1st of May. It will not be 1st of May. We're going to be in Austin. So it's going to be like late May-ish. But our May release should have it. Sorry, I've been a bit distracted. So people have been hitting by denial of service, and I've started to freak out about how to handle denial of service stuff, which we should talk about at some point too. But yeah, it does need some love and it will get it for the next release.

Speaker 6: Okay. If you have PRs for that at some point. I'm sure someone on the LDK team would love to do cross-compat testing and get us over the line with that. But if not, and it waits to the release and we just do it on mainnet, that's okay too.

Speaker 10: I was about to ask: What do you see as interop for offers given we're going across line to paths? Like, do we want to have some sort of combination of different implementations where one's a hop along the path? Or how do you see something that we could say: Hey, we're ready to merge because we've tested these various scenarios out with different implementations?

Speaker 4: Yeah. I mean, the obvious one is that the dummy hop where you basically have a mini-blinded path to yourself obviously needs to work. That's the absolute minimum bar. Obviously, it would be nice to test that you could go via someone else, and that would work. I have another PR pending that, Because we expect, for example, when you give a reply to a blinded path, that that terminates directly at us, and you create a path that leads directly to the reply. But LDK doesn't always do that. So, in that case, you need to do something a little bit fancier or to get entry point of the blinded path and we just give up. It would be nice to fix that. I'm not sure if that will go in the release though, but I do have a PR. Because in some cases, you've got to basically create a transient connection to wherever you want to go to bridge that. Because we always figure out how to get to the person first, and then we create the blinded path. So if we do a direct connection, we just create the blinded path, it only goes one hop. So there is that. But obviously, I mean, the ability to basically pay each other's offers is — that exercise is an awful lot. You've got to get an awful lot of it working before you can actually pay a BOLT 12 offer. So if we had that, blinded paths have got to work to some extent. Otherwise, you can't even do that. So once we've got to that point, I would be reasonably happy to, kind of, go ahead and find the rough edges as we go.

Speaker 7: [redacted], did you have a chance to take a look at that expiry height issue that I opened up.

Speaker 4: I did. I made a comment on it. I'm not quite sure how you actually created such a thing. But it is on my to-do list to fix for this release.

Speaker 7: Okay. Cool. It's just using a fetch invoice. I have to break it up because LND doesn't have the whole flow. 

Speaker 4: Right. 

Speaker 7: So maybe that's making it a bit funny. I create the offer, manually fetch it, break it up, and pay it.

Speaker 4: Okay. Cool. I'll check that.

Speaker 0: Cool. I guess, on release stuff, I think we're on track to get line and path forwarding or handling stuff in for .18, which is like our next big release. Fingers crossed. RC this week. I think [redacted]’s been doing much interop stuff in the background, so it looks like we're good on that front too.

Speaker 7:  Yeah. We've got with LND and LNDK, we've got interop with Eclair on offers.

Speaker 0: Nice.

Speaker 7: Making the payment.

Speaker 6: So, we can just press the button then.

Speaker 7: I don't know, I'm not gonna put LNDK up as an implementation. Thank you very much.

Speaker 0: Cool. Anything else on the edges? I just posted my notes for now. I think one thing we were starting to look at for our next release — I remember maybe like a month ago, we talked about some stuff implementations can do to make decisions about going on-chain or not. I think we identified three of them or so. One of them was not going on-chain for your own outbound payments, potentially doing the whole dust fee budgeting basis. So, never going on-chain that's very close to dust fee levels. Just things that we can do sort of, decision-wise, reduce force closures that aren't all trade-off free, but something that I think we may start to look at in our next round. At least for the current one, we have a bunch of stuff to basically do like proper deadline aware feed bumping, and not sweep anchors together, and start preparing for some of the TX V3 stuff. So at least you know we're a little bit late, I guess, if fees stay where they are right now, but things should be better as far as people getting confirmations to place and just the thing of not broadcasting garbage because we use Haskell and pull accept. Stuff like that.

Speaker 6: I think the biggest one by far is just failing an HTLC. Like, if you relay an HTLC from A to B, and B just held on to the HTLC too long, and so you force close your channel with B, failing the HTLC back to A while you're waiting for the channel with B to hit chain. Because…

Speaker 0: That's dangerous though, right?

Speaker 6: No, I mean, you're going to either get your money or you're not going to get your money, but it doesn't — once it expires, of course.

Speaker 0: I mean, if you don't get your money, I mean...

Speaker 6: But once it expires with A, it's too late. A is going to chain, right? Sorry, I mean when it expires on the inbound chain. Not right away.

Speaker 0: Oh. You're saying that you're already on-chain with B and A is about to expire, so might as well just do it off-chain versus making it go on chain.

Speaker 6: Right. A is off-chain if you wait another block, so you should just fail it back now.

Speaker 0: Yeah, that makes sense.

Speaker 4: Did we do a spec patch for that? Because I remember implementing it. Because yeah, it used to be we don't care, it's their problem to close it. But in that case, you would chain force close.

Speaker 6: Right. I don't think we ever did it. Maybe we — I don't think we ever did it. But I think that would make the biggest change in network-wide force closures by far.

Speaker 4: Yeah. Because it's the one case where you have to care about incoming stuff, where it's your responsibility to...

Speaker 0: Yeah, that'll sort of prevent the cascade scenario, which is the worst thing, where people can't get in because of fees, and then it just goes all the way back.

Speaker 6: If your peer is not failing an HTLC and it's timed out, your peer is just buggy. You probably don't want to have a channel with them anyway. If your peer is failing the failback because they are hitting this cascade failure, then you're cascading and now, everything is going horribly wrong. If we fix the cascading, then, well, we've already closed with shitty peers. Okay? It sucks to be a shitty peer.

Speaker 0: True. And then for LMP on call, I think we can do that pretty easily. Because now the resolver has the circuit mapping solution, we can look at the incoming height, and then once we're on-chain outgoing, we can...

Speaker 4: Yeah, we do. We basically said if the outgoing is on-chain and we don't care why — like, just if we haven't resolved it already and we're going to get force close incoming — something's gone wrong. A fee. Something handwave. Or sometimes, the outgoing has decided it's not economically feasible for it to actually do the on-chain close for the HTLC. Either way, whatever's happening, it doesn't matter. We save the incoming channel by failing the incoming HTLC. So we put in a generic kind of band-aid there, and that helps. It also means if we're buggy for some reason, at least we won't cascade failure. We may lose funds, but we won't cascade failure. So, yeah.

Speaker 0: Minimize pain for everybody else and deal with your own issues.

Speaker 4: Yeah, that's right.

Speaker 0: Yeah. Like an updated version. Cool. If there's nothing else…

Speaker 4: Denial of service. I did want to mention there have been some denial of service attacks on the network. Of course, Eclair.

Speaker 0: Targeted nodes?

Speaker 4: Targeted nodes. It seems so. Everyone should start thinking about that. We've done some things for this coming release, but we're going to do more. There's we've got a Bitcoin Summer Code intern hopefully, who's going to do — there's a protocol where basically you share a private address with nominal peers, just like a local mesh, say: Hey, here's some other addresses you can connect to me. The idea is that you could do that with your bigger channels. You give an alternate address to connect, and then you filter that. Only those node IDs can connect through that other address. So the idea is that you could then limp along. Of course, you've got to choose your friends wisely, but if your main thing is getting hammered, you could at least have some alternate IP, alternate port, or ideally, alternate IP, where established channels could connect. Of course, that could leak and you could fail that way, but it's possibly better than nothing. Our default implementation will probably be: Once you've got a channel and you've put some funds in, we will hand you out a second address if we have one, right?

Speaker 0: And then I guess, you may or may not need to do this, but is it sort of like implementation level DOS stuff? Or like a network level DOS?

Speaker 4: Network level DOS, right? Where they're basically just hitting you with a heap of crap. There's more sophisticated attacks potentially where they start pretending to open channels and stuff that are a little bit harder to deal with. You can DOS yourself if you put too aggressive limits on channel creation, but you do have to have some limits there too.

Speaker 0: Interesting.

Speaker 4: Yeah, but it does turn out that, at least on Linux, you can get more file descriptors just by asking for them. I had not appreciated that the hard limit, like the default limit for file descriptors on my laptop is like 1024, but you can have a million, right? You just gotta...

Speaker 0: Yeah. LND was way past that. That was something we should have advised you earlier, but it can obviously indicate an issue.

Speaker 4: People are doing it manually, but it's like: Yeah, hold on. We should when we start up. There's the thing in the latest release. We've got a thing where you start up, we're gonna at least make sure we've got twice as many as we have channels, right? For now. So, if you restart every so often, you'll at least bump it. We don't go so far as to — we should probably just: Hey, how many can I have? Just give me all of them. But there's probably a reason that everyone shouldn't do that, but yeah. I hadn't realized it was such a huge difference between the number you can just ask for. We were supporting the decentralization of the network by not supporting more than 900 channels.

Speaker 0: Yeah.. We'll let you respond. Cool. Okay. Alright. Posted my stuff. See some of y'all in Austin next week. Thanks everyone for attending.

