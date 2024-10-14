---
title: "Lightning Specification Meeting - Agenda 1150"
transcript_by: Gurwinder Sahota via tstbtc v1.0.0
tags: ['lightning']
speakers: []
date: 2024-03-25
---

NOTE: There were some issues with the recording of this call, resulting in a partial transcript.

Speaker 0: If you're only connected to a single peer, it makes sense not to tell them that you speak gossip, right? Because you won't have anything interesting to say, and you don't want to — with our current state of gossip queries, they might think they're probing randomly and happen to hit nodes that don't know anything, and fall into a bad state. So, I'm not quite sure how we should go forward with that, whether we should revert that and say: If you don't have anything interesting to say, don't advertise gossip queries. [redacted], did you want to…?

Speaker 1: I don't have a lot to add. I mean, obviously, I think we'll probably revert it for our next release anyway because people have core lightning LSPs that they want to use. Obviously, this case is really kind of only for the mobile node folks, where you're connected to an LSP. So, it doesn't really matter that much what we do because it's really just a case of this very edge node and talking to a very, hopefully, well-connected node. So. I'm okay with anything. It's just kind of we should pick something.

Speaker 2: Yeah. We actually had the same issue because when we started implementing that and deploying it to our node, we had the same issue with older Eclair mobile and Phoenix nodes who did not advertise gossip queries and we made it compulsory. So, we had exactly the same issue and had to override it on our node. We thought it was okay because it was exactly what [redacted] says — that it's really specific to us and having mobile clients. But maybe I think it would still be cleaner to keep gossip queries so that you can actually say: I don't advertise it because I don't support any of it. It means we have to keep it on the ground, but I think it's cleaner.

Speaker 0: Yeah. No, I think it is. Like, we just repurposed the bit rather than to say: I don't understand it. As in, I just say: I don't have anything interesting to say — which I had not considered. So yes, I will modify the first issue to perhaps change that or add a patch that reintroduces it in a different explanation.

Speaker 2: Okay. Sounds good. Is there something else on that PR that we want to discuss? Doesn't look like it to me.

Speaker 1: I think the others are okay. Really quick on the same topic. Just to be clear, if you're going to do that soon, [redacted] — I mean, we're planning on doing a release in a week or two; well, probably three or four — would you backport that? Is that something we should bother announcing gossip query? Should we do it in one release and then revert it to next?  What are you thinking on timing on your end?

Speaker 0: That's a good question. We don't have anything scheduled for a point release. We did a point release already that we were pretty happy with. I don't know of anything that's cooking for another point, but this might make it. Yeah, interops are important. So, I would be tempted to say I would do a point release just for this and encourage everyone to upgrade.

Speaker 1: Okay, well, we can discuss it offline. I mean, it would really only be a specific release for the three or four LSP nodes running Core Lightning that have LDK clients. There's only a few nodes anyway.

Speaker 0: Yeah. I mean, it's trivial for me to do the minimum thing, which is basically just shut up and accept it again. 

Speaker 2: Alright. Perfect. Then, the next topic is the simple close option. [redacted], we had some discussion with [redacted], who implemented it during the last meeting. The main discussion was that right now, in closing sign, you set the end sequence, but not the unlock time. We actually want to do the opposite. We want to allow setting the unlock time, which should be set whatever the node wants, but actually, the end sequence, [redacted] made a good argument that it should always be said to be RBFable. Did you have a use case in mind for allowing nodes to set it to something different, or should we just revert it?.

Speaker 0: No. We should say that it should be RBFable, but — well, actually, does it matter? I don't know. Is it better anymore?

Speaker 3: Yeah. I sort of arrived at this in a roundabout way. I implemented everything, I went to do the co-op close and then, I thought it was a force close. I was like: Oh, what's going on? Then, I realized that in our code, we actually use the sequence at times in order to decide if there is a force close, a co-op close, or a breach — right? In all the other situations, you could uniquely identify. For now, if the sequence can basically be anything. If someone were to be mentioned incorrectly, it could look like a past state or a future state. I think in our case, it was the future state because I had some other sequence basically that was still RBFable, but below the max. At least for now, I've implemented where it's always the max, but I can do otherwise. I think definitely we should be able to handle the other case, but something I think just came with implementation that could be a potential pitfall for other individuals. I think the argument that I had for having to be the same value is: Well, everyone just has the same sequence value and it looks more uniform, assuming people are sending that right below the max value versus something that's arbitrary. In any case, would you really want to have a sequence lock delay on your close interaction? If we want to make it uniform, we can have one less knob basically, but otherwise, we would need to make sure that they can handle the various cases. In our case, we still detected it as a close, but we just thought it was a future state and then, we're like: Oh, we lost data at SED. And then, it was like: Okay; well, everything really closed already. So it still worked. It was basically like a bookkeeping thing there, in a sense.

Speaker 0: Yeah. So there was that BIP, I think, that suggested that you should be able to adjust both, but I don't know that's widely deployed. I mean, you could just use the standard. Go back to using the standard value, I think, for now would be fine. I wasn't sure what the greater ecosystem usage is because we should kind of try to match that pattern, but...

Speaker 3: Yeah, we could look on like mempool.space since like people do RBF stuff more generally, or more regularly these days anyway. Because at least at that point, assuming you also did do the thing with deferring transaction — which maybe you shouldn't — it would look slightly more uniform. But that's where I was about to do interop stuff, and then I ran into that, and I was like: Okay, let me just at least post this off. But so, I think this week, we have to spin up another node on testnet to do actual closes back and forth, but we have it all working in itest and things like that. 

Speaker 0: Yeah. There was that enthusiasm for setting up some signet nodes that could be kind of played with and, you know, remote control. Did anything happen with that?

Speaker 3: I've never used signet myself. I don't know if y'all have. I'm a testnet reg test guy like. Yeah.

Speaker 0: Yeah. I'm a reg test main net guy. 

Speaker 3: Yeah, sure. Okay, so are we saying then clamp the value and remove the field for now, or keep the field but force it to be a specific value to leave the door open of changing it later, or just leave it? Those are the three options, seemingly. Leave it like it is right now, remove the field, or keep the field and then restrict the value.

Speaker 2: 0I think that keeping the field but restricting it to be a static value doesn't make sense. It's more burdensome than just adding another field later in the TLV because if you ever want to change it, you will need to have a feature bit anyway, so we should just add it in a TLV flag later. I think it would look like my last comment on the PR. The method should be just channel ID, fees, and lock time and then, we can add the CSV, the end sequence later, if we ever need it in a TLV field, potentially with a new feature bit.

Speaker 0: Yep. I will ack that.

Speaker 3: Okay. So you're saying add lock time or remove this?

Speaker 2: I would say remove right now the message is channel ID fees and sequence. The message should be changed to be channel ID, fees, and lock time. Basically, it takes the same number of bytes, but the last item is just the end of time instead of the end sequence. It is in my last comment on the PR.

Speaker 3: Okay, that seems simple enough.

Speaker 2: And then once we both modify that, we should be able to do some cross-compat test between LND and Eclair.

Speaker 3: Sure. Yeah. I'm here to update my PR definitely this week.

Speaker 2: Okay, cool. I can do the same.

Speaker 3: Okay, alright. Sounds good to me. We were trying to get this into the next release, but without interop, it doesn't feel good to do that. I think we're just going to hold it off and keep it in master. Maybe we'll do some release on the side or something like that.

Speaker 2: Because if you have it in master, we can do reg test against it very easily and very quickly, so we should be able to tell you that we have compatibility quite easily. I think that would give more assurance that you don't have to do some backwards compatibility things later.

Speaker 3: Cool, yeah. So it's not merged right now, but there is like a branch I think you can fetch, but maybe we can coordinate on the side with chat.

Speaker 2: Okay. Yeah. Let me know when you're ready. Alright, So next up is liquidity ads. During the last meeting, there was an agreement that having a first version that only advertises the liquidity ads without any enforcement of the lease — basically using a lease time of zero — made sense. So I opened a PR for that. But I have one question related to the funding weight that I wanted to pick your brains on. I'm not sure that's something we should do, but in your liquidity advertisement, one of the fields you tell people — the base fee you're going to ask from them, the proportional fee, and also a funding weight that they will refund to pay for the inputs and outputs that you will be adding to a transaction and you will be paying on-chain fees for. They will basically pay back some of those on-chain fees to you. How to set that funding weight depends on the number of inputs and outputs you expect to put in the transaction and that really depends on the amount because if someone asks for a very large amount, you're probably going to need more inputs than if they ask for a small amount. So right now, if you set only one funding weight for all of your liquidity ads, that means that when somebody is going to ask for a bigger amount, you will pay from your pocket more of the on-chain fees. Maybe that's okay because there's a proportional fee anyway, and you can say that this is what's paying for the additional thing. Or you say that you have to make sure that your UTXO set matches the amounts that you are offering so that you always need only a few inputs to be able to fund and then have one funding weight that works for all of the inputs. But another alternative would be to include a range. Have one ad per range of amount where you set a different price, basically. If you want to buy between that amount and that amount, this is going to be my price. If you want to buy between that other amount and that other amount, this is going to be my price. If you want to buy between that other amount and that other amount, this is going to be my price. Or even maybe do fixed amount liquidity ads. Say, I'm going to sell exactly this amount at that price or exactly that amount at that price. So I'm not sure what we should do, to be honest.

Speaker 1: If you're doing this based on your current available UTXO set and you do any material volume, you're going to end up updating your liquidity ad a lot. You're just going to be like: Oh, I spent this UTXO. Wait, now I have to go update my liquidity ads — every time someone claims one.

Speaker 2: I was more thinking the other way around. You decide that you're going to offer liquidity ads for those specific amounts, and then it's going to be your task to make sure that your UTXO set matches that, and if it doesn't, it's your fault and you're not going to earn as much. You're going to have to use more inputs and you won't get refunded for all of it. But the way we're approaching this is that, at least in Phoenix, we are only selling fixed amounts and then, we are working on coin selection to try to make sure that we always have inputs in those buckets so that most of the time we're able to do one input zero output for those transactions, but we wouldn't change on the fly. Depending on our UTXO set, it would be the opposite. We will try to make sure that our UTXO set looks as much as possible like what we are selling. So that we keep fixed liquidity ads, but make sure that we try to shape our UTXO set accordingly.

Speaker 0: Yeah, because it's in the Gossip Network. We tried to keep the ad fairly short, so it has this approximation in there for the UTXO set. If you want to put multiple ads in there for different values, maybe that's a completely different format.

Speaker 2: But maybe you only include a handful of them in your non-announcement, but then in your init, you can include more of them. It's not an issue if in your init message, you have many more liquidity ads, right? Because it's...

Speaker 0: Yeah, but the market making is done in the gossip stage, right? So you look around and you can go: Hey, there's this liquidity ads, I can — if you then have to connect to each node to find out what they actually are offering, that really cuts down on the marketplace. 

Speaker 2: Yeah, that's true.

Speaker 3: Well, I mean, I think it's a mistake to do it without any enforcement at all because then, what's the user buying, right? I remember before, people were concerned about the initial briefing attack of I pay and then, I close. Then, I guess there's another one and then decided there's just no protection at all. So I think this shows sort of problems created by the fact that it's sort of like a classified ads thing, but not like a true venue with any price discovery or anything, right?

Speaker 2: But that's completely orthogonal. Those are two orthogonal things, enforcing them or...

Speaker 3: Well, but I guess what I'm saying is part of the medium, like you were saying, is ideally you want to say: Oh, I'm going to do up to blah BTC for blah particular price. But then, my point is if you do that on Gossip, you're chaining it the entire time. Whereas right now, maybe there should be something that's more interactive that actually does more interactive negotiation when you have an individual, which just sort of forces you to connect to every single node. It just feels like maybe we're trying to stretch this to do a lot, but maybe the bare minimum is just advertising here, particularly given that you don't know what amount an individual is willing to actually fund with you. You sort of have to do a trial, right? You try it and they reject. But yeah, I don't know. I'm not sure if this is the thing that will — it feels like there's a lot of divergences in mental models or how things should work generally and pricing and such, but I guess that's what we have.

Speaker 0: Yeah, so I mean, a deep liquid market's important, right? One way to do that is to constrain what can be advertised and say, you can only advertise there are five different channel sizes. You have five marketplaces, and you pick one of those. If we knew what those five numbers were, I'm sure that would work great. You really do want to be — I mean, it's already bad that you have to assess the seller based on what’s their node connectivity and all of these other things. And now, of course, we've added the fact that you have to kind of judge whether you can trust them or not, right? Which definitely undermines the whole open marketplace liquidity idea. But as a stepping stone, it's perhaps not too terrible. Also adding the constraint that they may only offer fixed sizes makes it awkward. I mean, I'm trying to think from the point of view of a user. I guess you've got some estimate on how much liquidity you think you need, right? So, you're in the market for a certain amount of liquidity. It would be nice if you could scan the network and tell where you could get that from. I mean, there's always been to some extent, yeah. You might pick someone and they're actually a minnow and they don't have any liquidity. But assuming that you're rating them by their connectivity, the assumption is that they're a fairly big node and they have some liquidity, otherwise they wouldn't be advertising, right? But that said, I don't know if there is a good option here or whether — because if you have fixed sizes and fixed buckets, then you can give a single price for each one. You don't need to do this proportion thing, right?

Speaker 3: To answer it quickly, isn't this [redacted]’s point that if you don't know the amount, or even if you know the amount, because you don't know your current distribution, you may end up paying more in fees depending on what that looks like, which seems unavoidable, I guess. If I understand that, I guess you're saying if you don't know the amount or your current distribution, basically, you don't know how much you need in fees to pay for the things, therefore you don't know how much to set aside to actually satisfy a request.

Speaker 2: Yes. Usually you will make the buyer overpay by taking the worst case number of inputs or something that is at least some percentile of your worst case potential inputs. But I don't think the liquidity should have a fixed amount, but at least, maybe ranges. For example, right now, lease rate takes only 16 bytes. If we add the minimum amount, maximum amount to it, it would be like 24 bytes. So, if we allow you to have 10 of them, it's only 250 bytes and you're able to build 10 ranges that potentially cover from 0 to 2 BTC, and maybe that's enough so that you can have different funding ways that match those ranges without polluting the gossip network too much because it's only 250 bytes. So, if you restricted to an arbitrary number of things, you can have at most 10 of those in a node announcement. Maybe that's okay?

Speaker 0: Okay. I think I would want to see a concrete proposal at this point as to what works for you because you're pushing the boundaries of what this looks like at scale. So, what you want is a pretty good guide to what a decent design is, I think.

Speaker 3: Well, [redacted], can you explain the init message thing. I guess the init message is basically you would send more information about what your current offering is right now, right? So, the ad is basically sort of my range and then I connect to you and you tell me I can do like one BTC? Or is that something else?

Speaker 2: So in my node announcement, I would have, for example, three liquidity ads. One that says that if you buy from zero to 500,000 sats, you're going to have to pay that much. If you buy from 500,000 sats to one million sats, it's going to be that much. Between one million sats and one BTC, it's going to be that much. When you connect to me, you ask for a specific amount, and then I'm going to answer back with the liquidity ad for that amount that actually came from my node announcement. If that doesn't match what you saw in my node announcement, you just reject it automatically. But it should match what was in my node announcement and you should agree with the rate. Then, we just apply those rates during the transaction.

Speaker 3: Yes. So basically, you use the connection to do final negotiation. I guess there's going to be new messages beyond the init message as well, unless I set it in my init.

Speaker 2: No. It's directly in the open channel message that you add a TLV saying you request some funding from me, either in open channel 2 or splice init.

Speaker 0: Yeah. They reply with what you're actually going to get.

Speaker 3: Ahh. In the accept messages.

Speaker 2: Yeah. Basically, you tell these in the open and accept messages and splice and splice out messages. So yeah, I'll put a concrete proposal. Maybe a separate PR from this one that looks a lot like this one. Or maybe a PR on top of that one that changes the format with those min and max amount. See what makes sense and see if people like it better than the current one. 

Speaker 0: Yeah. 

Speaker 2: Alright. Then next up, I still have SCIDDR on pubkey. Maybe because we wanted you [redacted to give your opinion on that one. 1138. Having SCIDDR on pubkey everywhere. I don't know if we should do it or not. I'm not a big fan of it anyway. Yeah, don't have a strong opinion on that one.

Speaker 0: Yeah. I started implementing it, and it goes through all my code to change this into a 0 and this pubkey could be a either or and stuff. It's not the worst thing, but then you've got to make sure you resolve it at various points, right? Because you don't want to end up — but there were two. One is used inside and the other is the one in the actual offer. I'm halfway through implementing it, so it's not too bad. But the problem is if people don't actually want to allow it they're kind of stuck, right? My main worry is if people are not actually going to have nodes which cannot do the lookup, then you're going to be producing offers that don't work.

Speaker 2: But that's a bit what [redacted]’s point was —that LSPs can do it, in the sense that if we have a SCIDDR pubkey for the introduction node of an offer, only the sender needs to resolve it. If the sender cannot resolve it, then they can put it in the next node ID for the LSP, and the LSP could decide to resolve it, even though it's not in the spec because the format of the node ID is actually potential, at least for readers. You can accept reading what is supposed to be a node ID into actually an SCIDDR pubkey and do that resolution on the fly without even advertising it. It would be cleaner to advertise that you are able to do that thing, but right now, RNode does that. If you put in the next node ID an SCIDDR pubkey, we're going to resolve it for you.

Speaker 0: Okay. That is kind of nice actually. The one thing I like about this proposal is that it does fold very neatly into a pubkey. [redacted]?

Speaker 1: I think I've managed to confuse myself again. If we just restrict this to LSPs — I thought this was just for the case of when you're forwarding out, not the case of a blinded path that someone else has built, but I think I was wrong. Right?

Speaker 0: Yes. 

Speaker 2: It depends on how the sender constructs it.

Speaker 1: So it's recipient, you mean? The blinded path creator, i.e. message recipient.

Speaker 2: Yeah, they will use an SCIDDR for the introduction node, but the issue is going to be when the sender cannot resolve it and actually has to put it as a next node ID in the message, and the node that is right before the introduction node has to resolve that thing.

Speaker 1: Right.

Speaker 2: In that case, yes.

Speaker 1: Right. Okay, so I wasn't entirely confused. The part of the confusion — I was complaining that I don't want to do graph lookups when forwarding onion messages, which was fine, but we have to do that anyway because if you are a node in the interior of a blinded path, then you have to be able to support it. Because the whole point of this was to do it for the interior of the blinded paths. So my original complaint made no damn sense. Basically, I only made because I hadn't actually seen the implementation of this prior. But now I have, and I don't have a complaint anymore. I'm fine doing this because we did it.

Speaker 3: [redacted], wasn't the lookup in interior just like a channel lookup essentially, not a graph lookup?

Speaker 2: Yeah.

Speaker 1: Ohhhh. 

Speaker 2: I think you're probably still in the trance, [redacted]. Because in the onion message case, potentially there's no channel, so it's not only a channel lookup. It's really a graph lookup whereas inside the blinded path, it's only a channel lookup. So, I think your initial comment made sense — that it adds something, a new lookup, that we didn't need to do before that PR. That's why I'm not a big fan of it anyway. Maybe it's only something that LSPs offer for their wallets, and that doesn't go into a spec. 

Speaker 0: Well, okay. So, we always create blended paths that lead nicely directly to the recipient, right? So it will be a local lookup for you if we were to use it. So we alway — we don't create it until we figured out the path that we're gonna send. At first. we look at the path we're gonna send, we connect directly or whatever, and then we can create the reply path. So the reply path always, and [redacted] hit this, we don't handle the case in fact — I've got a PR about it — but we don't generally handle the case where you give us a random path, and we have to get to there to start sending the blinded path reply. We assume there's a was fixed me in the code. Well, we just assume that you're gonna give us a nice path that leads straight to our door for the reply. If you do that, then the SCID is simply a local lookup and not a graph lookup. Because it will be one of your short channels.

Speaker 1: Right. I don't know if we want to require that as a matter of...

Speaker 0: Yeah. I mean, you could say that if you're going to use that, you should make it directly connected to the peer, right?

Speaker 1: Right.

Speaker 0: It only works for the reply, of course. That doesn't work for like: Here's an offer; it has a blinded path in it, so you can't tell where I am. If you wanna use a short channel ID in that case, you're going to have to do a graph lookup there.

Speaker 3: What I'm trying to understand is: Using SCIDs, why does it require knowledge of the graph? Because if you're forwarding, you already know the SCID of the channel that you have, you're forwarding over, right? So, why do you need to look anything up?

Speaker 0: This is the case where you're using it for the sender. The beginning of the blended path — the entry point for the blinded path — allowing that to be a short channel ID implies that there's just kind of some well-known thing on the graph and you're like: To reach me, send it through. Normally, it's a node ID, but you could make it compact by putting in the short channel ID and that implies they've actually got some knowledge of the graph so that they can send you messages.

Speaker 3: This is for the person constructing the path?

Speaker 0: Yeah, this is the entry point, not the internal. The internals are fine. It's the entry. If you use it for the entry point of the graph, now you have this issue.

Speaker 1: Yeah. So, it sounds like we're all on the same page that we leave things as we previously discussed and we don't do this for the PR.

Speaker 2: Okay, sounds good. That's just something we're probably going to do on our node for Phoenix, but it doesn't have to be in the spec. Okay, so we'll pull that PR. 

Speaker 0: Man, I wrote a crap load of code for this, too. I mean, it's a cute idea. We may find somewhere else where we want to have a short general ID or something, and it's a nice format. But that's the main takeaway.

Speaker 2: But we do keep it for the introduction node of a blinded path, right? What's currently in the offers PR?

Speaker 1: Yeah. Well, that's the question.

Speaker 0: We did add that to the offers spec already, yes. Separately from this.

Speaker 1: Yeah, I think we keep it for the offers for the interior of a blinded path and for the intro node, but just not for anything else.

Speaker 2: Okay, yeah. Sounds good.

Speaker 1: I guess we could make it general. We can just say you can always specify it an SCID or DIR as long as it's a local channel, but you can't specify anything that requires some kind of other routing, or connection, or anything.

Speaker 3: I dropped something in the chat — something I started reading when I was on vacation last week, but then didn't get through it — but it's a paper sort of analyzing onion messaging in terms of worst case propagation delay, other DOS, and things like that as well. One part of it, I think, ends up changing the packet format slightly to reduce the total amount of hops. I think it goes from 500 or something like that, which sounded much higher than I thought it was initially, to like 30-something or something like that. Then another one, I think tries to add a POW that I don't really understand to the packet. The final one is sort of like a rate limiting thing that uses, I think, the capacity of a channel that you're forwarding over as part of the rate limiting vector. So maybe some of it's useful. Maybe not all of it. I can do a write-up, but I haven't finished reading everything yet, but just something that maybe people are interested in.

Speaker 1: Yeah, it may make sense to look at trying to reduce the hop count, But they didn't actually do any analysis of the current system. They just said Well, you can do a min number of hops, and then this is bad. That was kind of it. They didn't do a lot of analysis. 

Speaker 3: The current things doesn't have any prescribed rate limiting or anything, though? Or do you need something different about current system?

Speaker 1: Well, I mean, of course, all nodes rate limit, but they don't do any analysis of: Well, if you're flooding this, and then how many drops do you get over here? And how much DOS does that actually cause over here? Anything like that.

Speaker 3: Ah, yeah. It's a shorter paper.

Speaker 1: Yeah. But they proposed interesting, like the reduction in hop count. That makes sense. I didn't actually look at how they proposed doing it. They just mentioned that you could get a long path and maybe we should not allow that, which is reasonable.

Speaker 3: Yeah, I think it tries to restrict the bytes that you can allocate to the next hop or something like that. There's a diagram that I need to stare at more. Alright. Next.

Speaker 2: Next up, [redacted] opened a PR about asking payments, 1149. They wanted conceptual feedback on it. The main thing in that PR is the usage of keysend for the case where you want to let your LSP respond to invoice requests on your behalf if you're offline and they cannot wake you up. So, I think that's the main problem that needs some conceptual feedback.

Speaker 5: Yep. Has anyone looked at it? Thanks, [redacted].

Speaker 2: As I said, I'm still not a big fan of having to do keysend. I think that…

Speaker 3: Is the idea that the keysending includes an invoice? What's in there? Is it just like a payment or does it have something else in it?

Speaker 5: Basically, you know how in BOLT 12 you request an invoice, you get an invoice in response? Well, the mobile recipient isn't online to provide that invoice in response. So instead, its LSP or some other node will provide a keysend invoice on its behalf, and that basically allows a third party to provide an invoice without the ability to steal money. Because if an LSP provides the same invoice twice, it knows the preimage. So it can steal any subsequent payment if there's a payment hash.

Speaker 3: What's a keysend invoice? Is that like the AMP static invoice?

Speaker 5: Basically, yeah. It's just a payment hashless invoice. I mean, it's in the PR, but it’s basically just an offers invoice without a payment hash.

Speaker 3: Okay, I mean, if people are interested in integrating that, they could do the AMP version, too, that gives you MPP. I don't know.

Speaker 1: I mean, you can already do MPP, right? It still works just the same.

Speaker 3: Well, yeah…

Speaker 1: It doesn't add any value.

Speaker 3: No, I mean, the difference is the payment hashes. Do you want them to be the same or do you want to do different?

Speaker 1: Right…

Speaker 3: Also, you also do get an identifier to let you identify all the payments for specific sub-invoice. I don't know if this keysend invoice thing has that or not, which I think is useful.

Speaker 1: We can always create an identifier. I think the other thing that's maybe worth pointing out and discussing here is one thing that is really awkward is just how this interacts with other BOLT 12-based protocols. For example, the human readable names we were talking about, including the name itself that you intend to pay to in the invoice request probably. But if you end up using async payments — which maybe you wouldn't need async payments if you're doing this human readable name stuff, but you know if you imagine you are, then suddenly you don't see that invoice request. The final recipient never sees the invoice request. Similarly, [redacted] has some work that they’d shared on the BOLT 12 Discord around kind of enabling you to notify a point of sale system when a payment completes. Where similarly you need, or at least in some variants of what [redacted] had proposed, you need that invoice request to make it to the recipient to work properly. It seems like the only way to hack around this problem is to include the invoice request in the HTLC onion, which is pretty gross, but kind of solves the problem. Yeah.

Speaker 3: Yeah. I guess what I mean, if you're obtaining, you could just do an AMP invoice in this case, right? Because there's no requirement of fetching anything. You have the thing that's fully enclosed, right? And that could help you fetch later over offers.

Speaker 1: No. You want to still do the request because you want a few things, right? You want to do the request because you want a handshake with the second to last hop to do holding HTLCs potentially, but you also want the ability to seamlessly upgrade, right? so if the recipient's actually online you want them to be able to just send you a full invoice, full BOLT 12 invoice, and not have to deal with all this stuff. So, you still want to do the request. You don't want to just skip it and do something more naive, or just do like BOLT 11 or something.

Speaker 2: Yeah, it's really just a fallback basically. I think that what LSP would do is try to wake up the mobile device for 10 or 15 seconds. If that fails, then fall back to that key send option. 

Speaker 1: Right.

Speaker 3: How can they reply? It's like a short circuit reply, basically. So, they have this invoice thingy — oh, they send it to that party. But how do they know who's the sender? Like, how do they, or am I missing something?

Speaker 2: It's a reply path. An onion reply path. A way to contact them back to send them back the invoice.

Speaker 3: Oh, I see. Interesting.

Speaker 1: So, yeah. I don't know if we've come up with a way to solve these issues in the alternative form.

Speaker 3: But that's not authenticated, right? They can just send you anything in theory, right?

Speaker 1: No, it's signed by the final recipient. The final recipient pre-signs it and the LSP just stores this one pre-signed, no-payment hash invoice.

Speaker 3: But if the recipient is offline, what can they do with this invoice? They can't actually make a payment, right?

Speaker 1: No, the sender will then receive this pre-signed payment hashless invoice and would know to send a keysend async payment.

Speaker 2: Yeah, I think you're missing the async payment part, [redacted]. Then, they see that it means the recipient is, most of the time, offline, so they use a long CLTV on the way back. There's this other mechanism where it can be held by the sender's LSP, who gets notified when the recipient comes back online to be able to then forward the HTLCs to make sure that we don't lock liquidity and wait for the recipient to be online to actually send the payment. That ties back to the earlier discussions and earlier PR. I don't think there's a whole PR for that in what [redacted[ sent. It does, at least, link to the emailing list post that described that mechanism.

Speaker 0: If we would use PTLCs, do we get rid of this eventually?

Speaker 1: Yes. 

Speaker 5: Yes. 

Speaker 1: At least, the keysend part. I mean, you still keep the kind of payment hash plus invoice. You would just say: Please PTLC me if you can.

Speaker 5: [redacted] sent out a proposal for how to get proof of payment back with PTLCs.

Speaker 0: See that's — yeah. So, as an intermediary, this is fine, I think. This was confusing me too, [redacted]. This is built on top of async payments, and you're kind of assuming that we have that. Then it makes more sense.

Speaker 5: Yeah, sorry.

Speaker 1: There's that really old PR for the async part of it, basically.

Speaker 3: Speaking of PTLCs, who's working on Taproot? Hey, [redacted]!

Speaker 0: You guys are doing everything. Great! Oh yeah, do we have a note in the agenda for Taproot gossip?

Speaker 2: Yeah, we can go directly to that if you want because for the other topics, I don't think — there's a company routing — there's nothing new. Same. We are waiting for another PR and splicing as well. So, I think we can go directly to Taproot if you want and then go back to those topics if you have time.

Speaker 3: Cool. Chans-wise, I think, same. I think Eclair is working on interop. We're already there. I got some emails. I think maybe there's some back and forth there. On Gossip, we're just sort of waiting for other feedback really. Like, we have PRs up, but it doesn't make sense for us to move forward without much of the feedback. I think in the past, [redacted] was looking at it, but then moved on to Trampoline stuff. But I think that's the main thing we're looking for. It's just sort of like more feedback on what we ended up with, with the compromise of the compromise. Or like, putting it together, which is I think the current PR. I think it's up to date, but I'd have to ask [redacted] to find out details, but I think they have everything.

Speaker 1: The one thing that I know was mentioned offhand once, but never actually written down: Did we end up splitting the disabled bit into at least three bits? I know we discussed that before.

Speaker 3: What were the three bits?

Speaker 1: Channel permanently gone because you know channels closed. Channel disabled because my peer is gone and channel can no payments — HTLCs cannot go either direction. Channel disabled unit directionally. Because currently, the disabled bit means all three. I guess theoretically, you could fit it in two bits if you really wanted to.

Speaker 3: But the disabled bit is directional because the channel updates are directional, right? In theory, I can disable in my direction, but someone else could route in the other direction. Or maybe people are in the other direction.

Speaker 0: Yeah. We've flipped back and forth on how we interpret it. If you say you disabled, does that mean they're disconnected? Should we just also eliminate the other direction or not? But then, sometimes that happens and you just gust out of date. So, having a explicit  like ‘No, no, this channel is dead, dead’ or ‘This channel is completely unusable both ways’ versus ‘You can't use it this way’ is actually potentially kinda nice. I'm not quite sure how we would set that in practice, but I think if you can set it, we could use it. 

Speaker 1: I think the problem is right now, some people disable channels if there's not enough liquidity on their end. They have some automated shitty software that does that, which they really shouldn't, but they do. So, at least giving them the ability to do what they want — which they shouldn't be doing — but giving them the ability to do what they want to do, that doesn't break everything else, would be really nice. Separately, it would be kind of nice to have a permanently disabled bit, I think. Like, ‘Channel is closed,’ basically. Not that it's a huge difference there, but I think that'd be nice.

Speaker 3: Cool, yeah. I'm not sure if this is in the current version, but I'll forward this to [redacted], and we can see. It doesn't seem too difficult at all because I think everything's TLV in that portion of it anyway now.

Speaker 1: I mean, I assume it's still a bit field. We can just define new bits. It's not really complicated. It's just a matter of doing it.

Speaker 3: Oh, that's right. There is a disabled bit, yeah.

Speaker 0: And make sure we describe what to do with bits you don't understand. That's the key. I mean, we talked previously about having a bit say ‘Splice incoming’ — right? — to say: Look, you'll see it to close on-chain, but ignore that for a bit. I mean, we currently do that for everything at the moment, but that gives some weird results sometimes.

Speaker 1: I mean, I think that's part of the reason why you wanna have a disabled bit, or like a channel closed bit, in an update. So, it really should be announcing an update when their channel is closed, but if one's offline, it's closed or whatever…

Speaker 3: Yeah, we do a disable on co-op close initiation, but I don't know if we force close. Do we do it on our disable?

Speaker 1: Yeah, I don't remember if we do either. But like, no, you should be doing that. And that would solve that problem too.

Speaker 0: You mean, in the sense that if you don't see it, then you would assume that it's going to be spliced? Yeah. I guess you have more faith in gospel reliability than I do, but yeah. Sure. 

Speaker 1: Maybe.

Speaker 0: I guess that's fair, right? If you don't see anything, you still have to assume that you just haven't seen it and that maybe there is one out there. So even if we used a positive bit to say:  Yes, I am going to splice — you would still have to fall back if you haven't seen anything. So I guess that's fair.

Speaker 1: That's true.

Speaker 3: Cool. One thing I just linked now, it looks like, you know, secp PR has been getting more review, and it looks like also [redacted] started to just pull it in to implement it or to integrate directly in bitcoind, which I think is good. We'll get more API feedback, please, for that C1. Cool. I guess, have you all run into anything surprising as far as the interop stuff with Taproot stuff or still a little bit early on?

Speaker 2: No, it's the only way. We started. I think that at some point, [redacted] had something where he was able to open a Taproot channel with LND, but then other things broke. We iterated on it in the Eclair side, so I think we're still far from having cross-compat in the Taproot part, but at least we were working on it and making progress on it. 

Speaker 3: Cool. Oh, that's the other thing. With the current co-op close one that we have there — like, in the PR, I sort of just said: Okay, hey,  the co-op closed; it should be RBF basically. But I haven't gone back and added the nonces to [redacted]’s PR yet. I can open another PR or update the Taproot PR to assume that one is there if that makes sense and then, define them as extra TLVs the way I do with the other ones. That maybe seems a little bit cleaner, and we'll just have the assumption that this thing is a lot more canned than the whole new channel type.

Speaker 2: I think updating the Taproot PR would be the best way because hopefully, since we've got two implementations of options in co-op close, we should be able to know the options in co-op close somewhat soon-ish. I think it makes more sense to assume that it's going to be done before the Taproot PR and the Taproot PR just adds the TLVs.

Speaker 3: Yeah, I think the flow should be pretty similar as well because in that one, I ended up just sending the non-system shutdown and you send shutdown anyway to restart. So you can just  wipe all your state and then sign the new version.

Speaker 2: Yeah, it should be easy.

Speaker 3: Cool. Let me write that down. I'll sync with [redacted] around this feature bit stuff. I need to catch up with the PRs generally, but they should be sort of parked there for some time now. I’m focused on near term stuff. Cool. What else in the last 10 minutes or so?

Speaker 2: Is there a specific topic someone wanted to discuss?

Speaker 3: So, we have a PR now for the peer backup thing. At least, that's just the initial — like, be able to send it and receive it. We don't do anything yet. We have some other plans to try to use it to recover your HTLCs, but we, at least, just have the base PR to allow us sending and receiving. I don't think it's gonna get into that .18, which is our current, or upcoming, release, but probably definitely in the next one. Then, obviously, we can do interop, but it feels it's really straightforward. You just return the bytes.

Speaker 2: We should get to it at some point as well to replace our existing mechanism with that one. Make sure that it works all the way for the use cases that we have.

Speaker 3: Are there concrete differences or is it sort of like a semantic thing? Is there like a...

Speaker 2: Yeah, I don't think it's a lot of differences, but until we implement it, I'm never sure. So we should do the work, implement it, and make sure that everything works end to end.

Speaker 3: Cool.

Speaker 2: I don't expect any weird surprises, but I still don't know. [redacted], have you been making progress on quiescence? I don't remember exactly the details of the unquiesce message you wanted to add on the quiescence PR.

Speaker 6: Yeah, I haven't been able to work on that last week. I was pretty sick, and I've been working on some of the review for the upcoming release of .18. So, I haven't actually gotten to it. But it's still in my backlog, along with helping with some of the interop testing.

Speaker 2: Okay. Perfect. Oh, apart from that, I don't know if people had a look at that one in a while. Not publishing your commitment when receiving an outdated channel re-establish. I don't remember the status of that. Did everyone implement that, maybe in even earlier releases? Can we start depending on that? Or is that still ongoing for some implementations?

Speaker 3: Good question. 

Speaker 1: I think we implemented it.

Speaker 3: Yeah, I think it's ongoing for us, but there's some stuff that we were fixing anyway. Like, we were handling errors with tearing on the connection and stuff like that. I'm pretty sure we have an issue. Let me find it.

Speaker 2: I can also just do a round of testing against everyone's latest release and see who behaves in what way right now. This way we will be able to know if this can be closed or if this is still happening?

Speaker 0: Yes. I'm pretty sure we addressed that earlier.

Speaker 2: Okay. So, CLN and LDK should have already addressed it, and LND maybe, but to be confirmed?

Speaker 3: Yeah. I'm trying to find the issue. I don't think we do it yet. We have an issue in maybe a draft PR.

Speaker 2: Okay.

Speaker 0: Yeah, I'm pretty sure we even have a test for it. Yeah, you have to send us an error before we'll go on-chain.

Speaker 2: If you don't have a test for it, it doesn't work.

Speaker 0: Yeah, definitely. Sometimes, even if you do have a test for it, it doesn't work. But yeah.

Speaker 2: Alright. Anything else someone wants to discuss?
 
Speaker 3: Any Trampoline stuff that's happening? I think people have a new format. Anything that we should ship deployments or?

Speaker 2: No, I think it's just been — [redacted] has been working on it on the LDK side, and PRs have been getting merged lately. So, I think it's just working towards cross-compat, and there hasn't been any big changes on it. It's just clarifications and making sure that everything is okay when testing the cross-compat, but I think everything is looking good so far. So, it's just a matter of keeping on implementing the latest things and testing cross-compat.

Speaker 7: Yeah, all the test vectors, including all the updates that you pushed have been working out of the box. We have a couple open PRs still. We have one PR that I think should be landing in a couple days, hopefully. We have a follow-up PR, and I'm working on testing interop just based on that follow-up PR. So, this notably is only for sending Trampoline payments from LDK. That seems to be getting along quite nicely.

Speaker 1: One question that came up in our discussions is: Because Trampoline currently requires recipients’ support Trampoline…

[Error in video. Transcript cut off].
