---
title: Lightning Specification Meeting - Agenda 1055
transcript_by: Generated, Human-Verified by Carla Kirk-Cohen
tags:
  - lightning
date: 2023-02-13
---
Name: Lightning specification call

Topic: Agenda below

Location: Jitsi

Video: No video posted online

Agenda: <https://github.com/lightning/bolts/issues/1055>

Speaker 0: A few people won't be able to attend. I guess we can proceed. Okay. I'm going to go down the list that you prepared for this. The first thing being dual funding. I don't know if we have any one involved here at this point.

Speaker 1: All right.

Speaker 0: Last time, both of them were moving closer towards interop. I think this is where we are right on the end of interop between CLightning and Eclair. LNDs has some PRs. I'm trying to find it, but we'll be catching up there pretty soon. Do you want to give any updates on the Route Blinding progress? I saw there was a new PR on the LND side. I haven't had time to check them all out yet though. I think now we're doing forwarding now?

Speaker 2: It's not much news. I've got sending and forwarding done in LND, and I'm working on interop with CL today. Just figuring out how to do it without the full offers flow, which is a bit challenging, but we're on track.

Speaker 0: Can you repeat that last part?

Speaker 2: I'm testing interop with CL today for LND to make a payment to a blinded route forwarding through other LND nodes to CL. There's just some funny time-lock stuff going on, but that's on the go.

Speaker 0: Good news. Nice milestone. Related to that, any questions? I think the last thing here is updating to match latest spec stuff. I think this has been interop for the most part. We're waiting on some other related stuff in the Blinding spec.

Speaker 2: I guess this is a good time to remind folks that we do have a Discord, where we've been chatting about Bolt 12 stuff. If anyone needs an invite, just let me know. I'll post the invite link in this chat. That's the place where we're discussing interop.

Speaker 0: All right. Into Taproot stuff.

Speaker 3: We were in Nashville last week, and unfortunately, didn't get much done. But I'm going to make sure to get interop testing working this week.

Speaker 0: I brought up the thing around the scripts. I haven't changed it yet, but I was going in that direction. I was, at least, proceeding with everything without those script changes. They're pretty minor. One was OP_1 versus OP_0 and the other one related to the nums point. I'll try to commit those this week, so we can prep for interop stuff on that point. I'm doing breach resolution stuff. I have all the other stuff working with the control block. I had to redesign some things. Now, I always make the control block upfront. I was going to do it at runtime, but then some things didn't really work well. That's one minor thing on the side there. I guess I'll reach out to you on chat as far as giving you a node, so we can start to push on that. That'd be really exciting. So, Fat errors. I think last on this was get the TLV stuff in there, which happened, and then circle back?

Speaker 5: I'd rather to make something more descriptive. Maybe for Wumbo, it was fun; but maybe shouldn't do it every time. I documented a rationale why we would want TLV. All the time, I had the feeling that TLV is probably better. Then, the sender doesn't need to reveal some characteristics about what they can interpret. Nodes can just return what they want. Maybe an order of priority based on how much space is available. So, it seems unlikely that we ever get there, but if we get there, at least the sender can keep a bit more privacy, I guess. And then, there's a routing node and a whole bunch of data that it wants to communicate back. So, they can spend six bytes on the whole time, but then also they spend, say 12 bytes, to communicate the actual channel balances or whatever is going to happen in the future. I am not saying that it is a good idea. And maybe, at some point, they see that we can't return everything that we have to say to the sender because there's only 32 bytes. So, the routing node decides that the most important thing is full time because that's what I mean with an ordering there. So, in case there is not much space available, routing nodes try to make a decision about what's most important to return. That way, the sender doesn't need to exactly specify which TLV records it expects. But it's all very weak - maybe we also never need it. But on the other hand, the attributable error is already quite large. So, it doesn't seem to be a big difference to add a few more bytes for the TLV overhead and just to keep the flexibility for the future. Also, open to other opinions. If people think like we should do a fixed format that only takes the whole time because that's the only thing we need right now. If they have new ideas later on, we just do something with a signal from the sender to signal that a different payload format needs to be returned.

Speaker 1: That's also fine with me.

Speaker 0: I'm in the TLV camp myself. If you want to check out the comments, [Redacted] posted this slide deck that shows the flow versus the prior one. It's got some recent review from them and [Redacted] as well.

Speaker 0: This is on my list. I think we're trying to get this next LND release out, and then I can catch up on everything else. [Redacted], I think this is in a similar boat, codifying stuff that we did before? Actually, there's an update 16 hours ago. They're saying that some VLS thing had a similar issue that they didn't account for dust. They're asking whether we just close this if we feel like we don't need any more clarification. I think nice to have. Maybe it's just a matter of people just haven't been able to reprioritize it. I'll, at least, write down that it's updated again. Back on the line, splicing. I remember last week, there was a thing around this race condition of knowing when to use a new version and being able to resolve that. You're talking about actually splitting up the commitment just using individual messages versus backing to everything just one message. And it looks like that's the direction that's going to see the commits pushed up after that as well, but now it's multiple commit signs. That seems easier because they're independent channels.

Speaker 1: Yeah, we had a meeting with Eclair and reworked in that direction. There's an issue which I don't completely understand where you have a partial msat balance and you splice- I think you can end up with this leftover partial msat. I think the consensus was: If you end up in that situation, you hand it to miners; and I think that's the right answer. It's the rounding problem. I think the answer is always that it ends up going to fees, and I think that's okay. Nobody cares, and when somebody cares, we can argue about it. So, it actually works out pretty nicely. We thought about using the channel ID, but you don't need the full channel ID. You just need the transaction ID of the splice transaction.

Speaker 0: You're talking about which in the root case?

Speaker 1: It's the original funding transaction, right? You just put that to be in all the commitments signed, so it's nice and orthogonal. The other question is: Do you ever change the channel ID? The answer is no because it's too tricky, right? Channel ID is funny example, but you know that that's a relic after you splice a few times. That's a relic, but it just complicates the protocol to change it. That's a universal identifier. Anyway, so that that doesn't change, and it all seems to flow through pretty well - modulo actually implementing it and working on it. There were a couple of other things pulling it apart and putting it back together. I think we came across a good consensus that'll make it easier to implement. So yes, it's moving forward.

Speaker 0: One question on that is: What about invoices then? Because you mentioned that channel ID is going to stay the same, but invoices will track the new splice assuming you're doing SCID? The channel ID changes?

Speaker 1: The channel ID that the 32 bytes that we put at the beginning of every measure - saying this is the channel I'm talking about - that stays the same because figuring out at what point you change that during a splice is difficult. You could change the channel ID, but you're de-muxing stuff based on this channel ID, and that would be weird. If it changed halfway through, you'd have this weird control flow point at which you go: This is the new channel ID, and that's a source of pain. So, that channel ID just becomes a universal identifier for the channel between the peers, right? That's only ever exposed in the messages.

Speaker 0: It seems like using a steady LHS makes that easier. At least on the import side because then you never have to worry about switching. You say: This is what we have because otherwise that could cause headaches of splicing then the payments in-flight gets canceled back. That just make it easier.

Speaker 1: You have a grace period anyway because you've got six blocks before you can announce the new one. So, you've got to handle the transition, and you've already handled that with with aliases. It's just another alias.

Speaker 0: We might revisit this. We're thinking about dynamic commitment stuff, so as far as pricing in the risk of having some taproot thing, that changes. Being able to update whatever small script change where there's overlap. We had a thing that we looked at, but I think we're just trying to reintegrate into what's going on here. We can see if this can follow the same path. It can be distinct, but it seems like there's some general pattern here of updating something. In this case, you're getting the anchor versus just parameters.

Speaker 1: Yeah.

Speaker 0: Okay, what's next? The test vectors. I made an issue for this now, and I rebumped it. This is just some vectors that were added for anchored zero fee. I'm pretty sure LND is all good, but I think we're in reproduction limbo. Maybe when I make test vectors for the taproot stuff, I'll make sure these apply. This is a channel reestablishment one from [Redacted]. I need to take a look at this myself for the main one. Okay, that brings us to other stuff. Anyone have anything they want to talk about in terms of everything else in the LN universe?

Speaker 1: We have intern [Redacted] who's done this peer backup protocol, which is similar to the ones in the spec, only completely different. You can send a message saying: Here's a blob of data for you to store. When you reconnect, it returns your data. It's two messages. One is data for you to store and one is: Here's your data you gave me before. Very simple peer backup. We're just using it for static channel backup style backups at the moment. It's an experimental option in our upcoming release. It's a really simple protocol. We have to write the spec, but it's pretty easy. We're hoping that it becomes a thing that people do because backing up for your peer is great. Once we get it all working, you can delete your node and restore from seed.

Speaker 0: Okay.

Speaker 1: That's the dream, right? That even if the dumbest user does absolutely frigging nothing and opens a couple of channels and then loses everything, there are 12 words they can restart a node with. Then, it figures out: Hey, I've already got existing channels - that's weird. It goes out and tries to restore them and gets everything back and it all works. That's the dream that even someone who doesn't do backups can come back with their 12 words and it will just get there. They'll reconnect to peers and get their blob of backup data. They can bootstrap from that.  Ideally, even continue channels that that are do not have a HTLCs in flight. That's where we'd like to get to eventually, and this is the first step having this peer backup. It's the dumbest possible implementation. With some polish, which it does not have at the moment, you just save the blob, restore the blobs that they send you, and it will be like magic.

Speaker 0: Is there a restriction for the blob size itself? If you only have the seed, how do you find the other nodes? Is there a static thing as the pubkeys and then you can go to find that? How do you find the nodes that are storing the blob?

Speaker 1: It's a single message, so 64k limited. If you've got a serious node, get a serious backup. Eventually, the plan would be that you go connect to the gossip network. Somehow, you bootstrap the gossip network and see: Huh, that's where I've got public channels. For private channels, it's going to be harder. If you've only got private channels, then you're going to have a little bit more fun, particularly if you've changed IP addresses. How do you get that first one? I figure eventually there may be places that will back you up for sats. Throw me some sats, I'll store 64k for you. That may be common, and you connect to all of those and see if they throw something back at you when you connect to them. Perhaps, there are a few different strategies. Some kind of big bootstrap thing would be pretty cool. The start is just this exchange of messages. We have it as an experimental option. It's not on by default because it's not probably specified yet. I think it's messages seven and nine, so if you see those on the network, that's someone throwing backups at you.

Speaker 0: In the past, Eclair did something similar? I'm not sure if they still have it deployed. It seems pretty simple. It's a blob, right? What are the other details?

Speaker 1: They put a TLV inside existing messages. And I kind of like having separation.

Speaker 0: I think it's in general reestablishment for them.

Speaker 1: Exactly. We'll just have a separate thing, and we send it before we establish. So, before you get confused that we're reestablishing something you don't have, we send you this restoration blob. There's a couple of refinements to go in the spec. I would like to echo the blob when they send it. If you connect to me as a rando, how do you know that whether or not I'm accepting your backups? Some nodes may accept backups from anyone; some may not. If you get them to restore and they immediately echo, it then you've got an ACK that you're taking backups for me. For example, my node will back data up for any public node because you've got some kind of proof that you exist.

Speaker 0: For restore, is there no requirement that the first message for a channel must be reestablished?

Speaker 1: This is not a per channel message. It's just a blob not related to a specific channel. It fits the existing flow pretty well because you can always ignore it. What if I have 3000 node IDs? Get a backup solution. At some point, you've got other problems. Get serious hardware and backup your database. I'm concerned more about that really important tail of casual users.

Speaker 0: Raspberry Pi.

Speaker 1: You could fragment it across your 3000 peers and back up a little bit so that you can do an N of M restore.

Speaker 0: Code on top of that?

Speaker 1: Yeah, exactly - you go for that; there's nothing stopping you. It's an encrypted blob. Whatever works, whatever floats your boat. I'm not worried about backup solutions for the high end. I'm much more worried about it for the casual user. In our case, it's the existence of the channel, a static backup. At the moment, we want to add a little bit more.

Speaker 0: So, you can pack a few thousand channels in there?

Speaker 1: Yeah, you can go to town on these things, and that's before you even get fancy. If you've got enough peers, you can totally shard stuff across.

Speaker 0: In theory, you could put pointers to other peers in the first one? It's like a meta thing. You get one blob, and then you have the piece of the puzzle map that says: Go to these other peers. The client can do it themselves.

Speaker 1: Exactly because it's a client side - it's an encrypted blob. You can't even enforce anything about it. That's the dream, and [Redacted] is going full steam ahead on that. Full disclosure, [Redacted]'s applied for a grant, which would be kind of cool. We have an experimental model for that.

Speaker 0: That's a PR or is that 881? No, that's the old Eclair one.

Speaker 1: Yeah.

Speaker 1: We've stolen the same feature bit, which is annoying. It's important that there's two. There's one saying I offer it; one saying I will store it for you. It's the same deal. Just different formats and we'll spec it up, but it's pretty trivial.

Speaker 0: It looks the same rather than just like the message type. It's just a blob anyway. Check that off. Any other things people want to talk about in the greater the greater scheme of stuff? I saw there's new mailing list posts I haven't caught up yet around peer signaling that they want to be punished?

Speaker 4: That's right. You can now opt into severe penalization just to prove that you're serious. That seems to be quite contentious, given the two replies that I received so far. I thought it was actually a nice solution to a problem that we have.

Speaker 0: I don't think we can act like all peers are created equal. Some peers are more seriously managed than others. I guess we have the enable disable already, but you need to be observing that to see the pattern.

Speaker 4: Yeah.

Speaker 0: It's unavoidable that like some peers are better than others, right? If your algorithm biases towards those because they're just doing better, I don't think that's a bad thing.

Speaker 4: The advantage of penalizing is that you don't need to experiment as much. You don't have to explore as much because if you choose one of those nodes, you can just penalize the whole node. Not just the channel. The whole node because they don't reliably report availability. So, it's actually better for establishing a view of the network locally. Anyone has a chance to advertise this. If you want to be a routing node, you have to play the game at a certain level.

Speaker 0: So, it's kind of creating an overlay of self-professed serious nodes? If you say you're a serious node and you're not a serious node, then maybe you go on the permanent blacklist or something like that. It's a concept, and assuming people have APIs to set CLV values, it can be done at-will.

Speaker 3: We already have that differentiation between unannounced and announced nodes. If you're not serious about routing, why are you announcing that you are available for routing? And secondly, these self-declarations usually don't make much sense because they get abused, or everybody sets them, or nobody sets them. It gets us started down the road where we start accepting external signals instead of observing our own, which are more reliable.

Speaker 0: I think you're right that there's that class that exists. I think this is saying there's another class, which I think undeniably exists. Not every node in the network is online. That can be observed within the network itself. I think there definitely are classes. Just because you advertise, doesn't that mean you're doing something. My node is advertised, but it sits there for development. Some people spend hours a day and make money, and make some sats. I have rock bottom fees.

Speaker 1: There is the free signaling problem. Maybe we need some kind of proof of work before you can turn it on.

Speaker 0: Or you put down some funds or something?

Speaker 4: The way I see it is that the signalling is directional. So, if you have a channel and you make sure that you always have outbound, you can safely signal high availability. Traffic coming in the other direction is going to look at what your peers are signaling for this channel. So, it's not that if you have channels that get depleted to your to the remote side that you can't signal it anymore because it's directional. I've been reading the replies saying: This is a property of a channel that is highly available - yes or no? Whereas the way I see it is that it's a certain direction that is highly available. So, maybe it makes it a little bit better?

Speaker 3: No because you mentioned before that you are actually planning on banning the entire node for misbehaving for not keeping up that reliability? And I think that's probably the wrong direction.

Speaker 4: Yes, but not banning a node if you don't have inbound. You can't really control the inbound that you have. Your peer is supposed to do that.

Speaker 3: Yes, but this is a channel attribute that you're using to penalize the entirety of the node, independently of the availability of those other channels. So, you're inferring information that is wrong in this case. You say channel attribute, but it's an attribute of a certain direction of the channel. Maybe we call it an edge, or I don't know what the name is for the implementation.

Speaker 1: Sure.

Speaker 3: But I mean, the domain of that flag is wrong. It should be on the node if you're penalizing the entire node. And secondly, why are you penalizing the entire node if one channel goes unavailable?

Speaker 4: The node promises to be highly available and then it isn't. So, it's not reliable.

Speaker 0: The node said it was a super node, but turns out it's not a super node.

Speaker 4: I think you want to do it on the channel level because this allows nodes to gradually ease into this. So, if they have a few channels that they know that they can keep this service level up, then they just advertise the flag only on those channels. And the other ones, they don't do that. So, if there's a failure on those other channels, they won't penalize as strongly.

Speaker 1: I think you have to change the way you advertise every random interval: I'm also keeping up with the specs, so I'm a good citizen kind of bit. So it forces people to keep updating their software as well. That shows some dedication, right? So, you should flip a coin every day; if it comes up heads, then the spec changes.

Speaker 4: I see what you mean. Well, we keep changing the specs, so that is happening.

Speaker 0: Earlier, I meant being able to just like set arbitrary TLV values. I know it can be like: Hey, I'm serious today. Observance is another thing, but I know some people are doing more custom pathfinding stuff, so it could still be like a way to get into that.

Speaker 4: Yeah, but I don't think the API does not exist yet.

Speaker 0: I think you're correct. I think we just allow node announcement, or in 0.16. We don't do the other ones yet, but we do it in a way where it would be in the reserved range that we protected.

Speaker 4: Yeah.

Speaker 1: Do what? Set TLVs in channel update?

Speaker 0: Yeah. I'm talking about hypothetically exposing that. Right now, I think we only do node announcement, but if someone wanted to be the first serious node, they could start to advertise this. Anything else people want to talk about?

Speaker 2: It's a bit far out, but I'd like to talk about some channel jamming stuff if there's nothing else more pressing.

Speaker 0: Sure.

Speaker 2: We have been running meetings every other week with the spec meetings. We have another one this time next week about channel jamming. I've been looking at taking [Redacted] and [Redacted]'s paper, who are some researchers at [Redacted], which proposes upfront fees and reputation and turning them into the spec. In the early discussions, we've had around upfront fees, it seems like the very simple, very easy case unconditionally pushing very small upfront fees along a route is not going to work. While it would be very nice to keep it simple, as you accumulate fees along the route, if some nodes have high fees and some nodes have low fees, it's just not going to work out because people's incentive is to steal those funds. So, drop the payment and claim the upfront fee rather than forwarding it because the upfront fee is higher than their own success case fee. Last week, we started looking into the concept of doing a proof of forward for claiming your upfront fees. You don't just get an HTLC and you get the money. You get an HTLC, and if you can reveal a secret in the next node's onion, you can then go and claim your upfront fees from your peer. There were two things we ran into while we were figuring out how this would look. The first one is that if you happen to choose a route as a sender that has two attackers next to each other that are collaborating, they can still cheat the system because one of them can just give the secret to the previous one and claim the fees anyway. The other thing that this type of scheme would reveal would be that the forwarding node now knows that the next node was a source of failure. If you fail back an HTLC without that proof of forward, clearly you never managed to get that value from your peer. I know it's difficult to grasp these concepts as I described them in a call, so I'll follow up with a mailing list post. But I was just wondering, what the gut feeling is around how bad this is? We didn't think that being two attackers in a row in a route is too bad because that's pretty unlikely for you to be able to engineer that. You can still punish with routing algorithms that punish failures. The issue of if Alice forwards to Bob and Bob fails back without that proof of forward secret, Alice will know that Carol failed it. I wanted to get a read from folks on that.

Speaker 0: It seems like we're falling back into the old saga. This one seemed to be newer, maybe less trade-offs, and a little bit simpler. But if you're abandoning the unconditional push, then I feel like there's a lot of stuff we looked at in the past - the dual fees in both direction, the hold fees, things like that - which gets into the proof of forward stuff, which gets into the unwrapped onion stuff. So, it seems like maybe some of the other stuff should be reexamined now. I don't think you can say that's unlikely, or improbable, to have two attackers in the same route just because there's a lot of nodes now. A lot of people are running a lot of nodes themselves as well. If the simplicity of the prior approach isn't really there, then this seems to get back into like that massive well of these sort of ideas around applying forwarding fees. Then, the other question I have is: Are we are looking at this first versus the reputation mechanism of the endorsement? The endorsement thing seemed easy to deploy in a way that didn't really affect other individuals? It didn't require a global setting to be created. Just one comment there, and then another question around the endorsement thing: If you were looking at this before that? If this is going back into that massive design space spiral, the endorsement thing be prevention deployed instead?

Speaker 2: Yeah, totally. So, a few things. First one on reputation. I'm looking at the upfront fees and [Redacted] is busy working on reputation thing. Our next call, which is next week Monday, is going to be specifically about reputation. We thought that the unconditional push would be easier, which is why we started with it. It hasn't turned out that way. So, we're definitely still working on reputation. We're thinking about possibly even doing it with an experimental feature because that could be interesting to get some insight. Allowing people to run these things in read-only mode is also another compelling thing, so we're definitely still pursuing that. In terms of falling into the old well, absolutely. I missed some of the beginning of these discussions, but I have been reading backup and mailing lists and trying to catch up on all the things that all the people have thought about this. I'm trying to find something that is a more simple version of what's been discussed in the past. But yes, this generally seems to be the pattern of channel jamming mitigation that we move in large circles. Maybe this time, we break out of the circle?

Speaker 0: It's classic: People talk about it, then people forget about what they talked about, they have something new that seems to be very shiny and simple. Then, all the trade-offs are checked off, and then turns out: Okay, well, those are just like these other things, and then back to step one.

Speaker 2: Yeah, we can make some forward progress.

Speaker 1: I think if there's a network of attackers who all communicate with each other, then randomly getting two attackers in a row probably comes with like a non zero probability.

Speaker 2: Yeah, totally. You're able to minimize it because you'd still have to pick a path. It's just like objectively better than an unconditional fee, which anyone can steal at any time. So, with an unconditional fee scheme, you're probably likely to have some sketchy behavior. But I'm hoping that with something like attributable errors and this proof of forward, then you can really minimize the amount that can be stolen. And we're talking about pretty trivial amounts to begin with. I agree with you that it's not impossible.

Speaker 1: Yeah. So, it's strictly an improvement over the "If I receive it, I can take the fee" - is that I have to forward it to take the fee. In the first case, only a single node has to be bad to take the fee, so you've definitely improved it. The next execution case, where you can now tell that it's N plus one implies that you've got a simple scheme where everyone takes one, but that may not necessarily be true; you could tip. In theory, at least, it could be that the next node was entitled to a larger amount than you expected. So, you can tell when it being N for you. You kind of need to do that. Otherwise, you can tell from the amount that was taken how far the success case was, right? So you go: Oh, it failed, and this much was taken out. So, I can intuit that it went three hops before failing. That's just the pattern in general, so you're going to require some variation. The original scheme was that you get one set every time you you hash the preimage. So they go: Huh, they've hashed that 28 times; therefore, they're entitled to 28 sets, or 28 msats, whatever it is. I don't think that my problem with the N plus one schemes. It was always trying to do it without adding another round trip in the protocol, and it wasn't entirely clear to me that that worked. That was a bit of a killer. If you can do it without having a round trip, so that you can do it without adding another round trip, or maybe only adding around trip in the failure case, then that's acceptable. I never got far enough down the weeds to decide whether or not that was worth doing. The problem with the pay forward is always that tracing problem. If it fails, you now have a hint as to how far it fails, which you didn't really before. At least, in theory, modular timing. You can supersede attributable errors to some extent because you now know how far it gets, but you don't get any other data, like how long it took or anything else in that proof. You do have a strong implication on where it actually failed, which is kind of key.

Speaker 2: This is what we're looking at - is a slight simplification of the idea of okay. One preimage gives you one set. It telescopes the fees from the sender. If you forward it, you can just claim the accumulated fees, which does mean that the fees will be bigger. You will always be claiming the same amount on failure. So, you don't have that like 1,2,3 decreasing issue. But you do know that this has failed one or two hops down the line if someone didn't give back your proof of forward.

Speaker 1: That's not quite true, right? Can I put two proofs of forward inside a thing and overpay? I don't know what your proof of forward is here, but if it's a hash, then can I just give you two of them so you can take twice as much?

Speaker 2: There's a secret that the sender produces in the next node's onion. The upfront fee amount is specified: I'm pushing 10 sats of upfront fees to the next node; if you give me the secret that the following person's onion, you get all 10. There's no 16 preimages where you can claim different amounts based on different numbers.

Speaker 1: How do you give that to me and prove that you're entitled to it? How do I as a random node in the middle? Get that back for you? Oh, yes, you are entitled to 10 sats.

Speaker 2: You locked in an update, add that, you commit to that. I was trying to like keep it slightly higher level because I'll send out a mailing list post and make some pictures with these. I'll also reread those old mailing list posts because I don't want to reinvent the reinvented wheel again.

Speaker 1: I'm not sure how much of it is in concentrated in a useful mailing list post I have.

Speaker 0: It's usually mailing list posts with like 30 replies, at which point I stopped reading at 15.

Speaker 2: Yeah, I've only made it 15 deep, but I'll only ever to make it to the end just to be sure.

Speaker 0: It was in the 27th post, but no one actually read that one.

Speaker 2: Anyway, that's what I've got. I'd also just like to shill the meeting. Next week, we're going to be chatting about reputation. We'll send out a reminder email on the mailing list, and there's a GitHub issue where people can drop any agenda items they'd like to add them.

Speaker 1: And if I'm correct, it's exactly seven days after the beginning of this meeting was.

Speaker 2: Yes, it is. We will send a reminder with the date and the link and everything.

