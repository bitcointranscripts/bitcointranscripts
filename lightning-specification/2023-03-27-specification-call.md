---
title: Lightning specification call
transcript_by: Generated
categories: ['meeting']
tags: ['lightning']
date: 2023-03-27
---

Name: Lightning specification call

Topic: Agenda below

Location: Jitsi

Video: No video posted online

Agenda: <https://github.com/lightning/bolts/issues/1060>

Speaker 0: First off on the list is dual funding. I thought that we were done with dual funding, but there are actually two changes that are pending. There's one that LDK suggested which is to change the encoding of the script witness. I think that's fair. It's simpler with a change in the encoding and (Redacted) was okay with changing that. (Redacted) would be really painful for you in the code to use the Bitcoin encoding for script witnesses.

Speaker 1: No, it should be easy.

Speaker 0: Then I think we should do that. Can someone from the LDK team prepare the patch to update the spec to do that and give a few examples?

Speaker 2: Do you prefer to write out the whole Bitcoin encoding in the spec document or should we just say as encoded in a Bitcoin transaction?

Speaker 0: I think it's better to at least specify a bit? I'm not sure how it's encoded. I know it's a big endian instead of little endian. We use one in Lightning and the other one is used in Bitcoin. That's something that we need to make sure we don't mess up and that would create incompatibilities otherwise.

Speaker 2: Okay. I don't see (Redacted) here. I'll ask them if they wants to do it, otherwise I'll do it or find somebody to do it.

Speaker 0: The other change, which is both for dual funding and for splicing, is a change that fixes the reconnection cases. There's an issue in the interactive TX protocol. First you exchange commit signatures, then you exchange signatures for the funding transaction. The moment where you really need to store state about the channel is when you have sent your signature because then the channel can potentially be confirmed. A commit transaction can potentially be broadcast and you may have funds in that channel. If we only store the channel state at that point, there are cases where if we disconnect while we are exchanging signatures, one of the two sides remembers the channel because they have sent signatures but the other side has not received them. So the other side does not remember the channel. When you reconnect one side thinks there's a channel and the other side thinks there's no channel. For dual funding, it wasn't so much of an issue because you could just wait for the channel to be double spent or spend it yourself. For splicing it's going to be a real issue because if you reconnect and you disagree on what the set of commitments to which you have to add all the new updates is, then it's going to lead to a force close. When we realized that we thought it was best to fix it the same way for both dual funding and splicing. Our proposal is to start storing state whenever you send commit signature. So, one step before sending transaction signed. I have a big comment where I show that if you do that and you make a small change to the channel re-establishment logic, you are always able to reconcile state and either forget the channel safely (because you have not sent the signatures for the funding transaction) or finalize the signing steps and exchange the signatures that you're missing so that the channel is actually created. I don't know if someone has been able to look at it deeply enough and verify that it works. We've implemented it in Eclair for both splicing and dual funding and we think it works. We have tested all the scenarios, but another pair of eyes on it would be great. So I'll share a link to the huge comment. Whenever people working on dual funding have time to look at it would be really useful. I created a much bigger gist. We propose changes to the protocol, which I'm sharing right now. It would take time to read because it's a lot of protocol message flows. I think detailing the flow of messages is really useful to figure out how the protocol works and where there could be an issue if you actually read all the messages. I find it much easier to read and analyze than just the spec format.

Speaker 4: To give a high level overview really quickly, the problem with the current spec is: right now in the dual funding and splicing protocol (the interactive transaction protocol) as soon as you send a commitment signed message to the peer that gives them the ability to send you a transaction signed message. So from that point on they would have sent you all the information that you would need in theory to sign and broadcast the transaction. That's a problem because in the current way, at least in core lightning that we do it, we don't save that transaction to disk until we've received a commitment signature. So what can happen is: I could send a commitment sig and then the peer could get it and send both their commitment sig and their transaction sig at the same time because there's no ordering requirement on them. As soon as they've gotten our commitment signatures, they can go ahead and send us their transaction signature. The problem is that they can go ahead and fire off the transaction signed. If they're disconnected such that we have never received their commitment sig, our node would be in a position where it's totally forgotten the channel. When things come back and we reconnect, we would have completely forgotten that that channel existed. They think we must remember this forever because we sent you the transaction signed for it. The proposal that (Redacted) has come up with is that as soon as we've entered the state before you send a commitment sig, you would save it to disk and remember it as opposed to waiting until after you have received a commitment sig from the peer. This solves this entirely of this class of problems.

Speaker 1: That seems like a base requirement. At the point you send you are potentially committed to it, so you need to remember.

Speaker 4: From an implementation standpoint it's nice not to have to save them until you've received a commitment sig, because that means there's never a point in your database at which you don't have a commitment sig for any potential channel. You can enforce constraints around always having to have a commitment sig for a channel when you write it to disk, which is kind of just nice from an invariant standpoint. This will be a break from that which is not a problem. We can figure out a different place to save it. It's cool that Acinq found it, I think this is a pretty good solution. Looking forward to getting that updated and implemented.

Speaker 0: I think I will try to write a patch for the spec to update to those requirements so that when you implement it in core lightning, we can make sure that we all understood it the same way and then we're able to do cross compatibility tests.

Speaker 1: I like next funding txid because it's explicit. If there's a mismatch there, you've got the wrong txid - it'll be very obvious.

Speaker 0: The thing we're adding to channel reestablish is that when you've been disconnected in the middle of a signing session, you're going to include the txid of the funding transaction that you are signing. If you did not complete the whole process your peer knows that they have to resend commit sig and tx signatures for that txid. That lets us reconcile. At first I was afraid of how this would interact with the other channel reestablished fields, but actually the cases where you disconnect while you were in the interactive tx protocol means you were in quiescence - so your commitments were in sync. Interestingly, you cannot have complex edge cases where the normal things you have to retransmit from other updates get mixed in with the things you have to retransmit for the splicing interactive tx stuff. I think it's actually simple and easy to implement.

Speaker 1: I agree. That was one of the reasons for the STFU protocol because I did not want to have to think about those cases originally.

Speaker 0: Then that's what I wanted to cover for splicing as well. We have this new proposal that we think fixes the reconnection logic. We also have a proposal where we exchange fewer messages. The main difference is that whenever you finalize a splice, instead of resigning all your active commitments, you only send commit sig for that new splice at the same commitment number. You don't revoke the other thing because there's actually no good reason to revoke them. Conceptually you're just adding a new commitment to the existing commitment number. We think that makes sense. I'm curious to see when you try implementing that alternative if it makes sense in other implementations.

Speaker 1: We split it to multiple messages now anyway, so that's a very consistent approach. Whereas before you needed that jumbo message. I just wanted to check: in the splice do we negotiate the channel type? The no-splice to upgrade the channel is something that we want. The splice proposal predates the channel type proposal. When you propose a splice you should also be able to propose a channel type. This is the classic splice to upgrade case. In fact you could implement splice in a mode which would just to use it for channel upgrades - not actually splice anything in or out. I just wanted to check if that had been added in there somewhere.

Speaker 0: I don't think it's been added to the current PR. There would be a few changes. In that case you don't even want to start the interactive tx protocol. Do you really need that to be spliced?

Speaker 1: If you've got to change the on-chain transaction? You'd still do interactive but you could just have a null interaction. At the moment it doesn't make sense to do a null splice. It's allowed by the protocol, but it would be a weird thing to do, right? If you want to change channel type, then you would actually have a new commitment transaction with some new commitment transaction form. You want to change to taproot channels, for example. You could certainly do both. Just putting the channel type the same way we do with modern open both sides would allow that upgrade transparently.

Speaker 0: So that would work for the channel types like moving to anchors. That would not work for migrating to taproot, for example. That would require a real splice that creates a new funding transaction. That could also be done, but it's not exactly the same mechanism.

Speaker 1: It is the same mechanism.

Speaker 0: So you mean that when you are updating, for example, from a static remote key channel to an anchor output channel, you would create a new funding transaction? You could also just create a new commit transaction?

Speaker 1: You don't need that, but you do need splice for something like going to taproot, right?

Speaker 0: Yeah.

Speaker 1: Yes, so we have a separate upgrade where you only need to upgrade your state, you don't need to do an on-chain update. If you need to do an on-chain transaction, it makes sense to do it as part of the splice logic, right? While we're splicing, let's upgrade to taproot.

Speaker 0: Definitely, that makes sense. I don't think it's been added to the spec proposal yet. Do we have anything blocking on route blinding? Because I think it's ready to go.

Speaker 1: I think route blinding is something we should merge.

Speaker 0: What do other implementations say? Should we merge?

Speaker 1: We have interop, so...

Speaker 2: Yeah, we're still working on it. (Redacted) is working on it. No theoretical objections, unless they have some. Ok, they say not.

Speaker 1: The question is interop testing. We have core lightning and eclair, but it's always nice to have a third.

Speaker 0: That will really test it. LND and LDK, I think, for route blinding, not the blinding payments, but at least the blinding path for onion messages have interop?

Speaker 2: I'd say it's up to y'all. (Readacted) is working on it so it shouldn't be too far behind.

Speaker 0: (Redacted) do you have any idea on how much time you would need to be able to have a basic interop test with any of the other implementations?

Speaker 2: I think it would be at least two weeks hopefully within a month, I would say.

Speaker 0: Should we wait for a month, then? Before merging that?

Speaker 2: I'm okay if you guys want to go for it.

Speaker 0: Okay, we can merge it and we can do some patches, because we will ship something that people will start using in the wild in the next few months. We can merge it as is and then do some small patches if there are small things that we need to fix. Excellent.

Speaker 3: For what it's worth, I've got clightning able to make a blinded payment through LND nodes. So that piece is also working.

Speaker 1: Oh, great. That means you've got route blinding.

Speaker 0: So next up, we have this old PR about dust exposure. I think it's ready to be merged, but definitely need someone else to look at it. If someone has time, one of the other implementations should review this PR so that we do something about it. It's something we've all fixed in our implementations, so we should make it official by putting it in the spec. I guess that's not something we should do now because it takes a bit of time, it would take half an hour to review. If someone can find the time, put your to-do list that. Onion messages. I don't think there's anything new, but does someone have something about onion messages?

Speaker 2: I mean, once we land blinded routes, we should probably just hit merge on that one too? That one has way more interop testing.

Speaker 0: I agree.

Speaker 1: There are only two things that I would like to add to this, but they're separate things. Just to roadmap this for people. One thing that might be nice is this response where you can make it semi-reliable. We talked about using this rate limiting thing where you remember the last thing you sent and you push an error message backwards in an opportunistic fashion. That doesn't require you to keep much state. We can use that both for you got dropped because of congestion pushback and for rough failed for some other reason error. Like peer was unavailable and it could not route. You would also get some feedback if your path failed statistically. If things were noisy, perhaps you won't, but it would make it semi-reliable. You would probably commonly get an error back in that case from an onion message, which would be kind of cool. We could use the same mechanism for both, but it's an obvious extension afterwards. The other thing is that you could have a bit that nodes advertise to say that they will opportunistically connect. Essentially, they will spam for you. You can connect to it and it has this feature bit to say: if you connect to me and try to send an onion message to someone else, I will try to connect to them and send it for you, which would help bootstrap connectivity. Obviously an implementation would need to decide to turn that on and you would need to rate limit it in some way so you're not connecting to every node all the time. If we had that as an advertiser feature bit, it's something that nodes could start using to make onion messages more reliable.

Speaker 2: The second one makes sense. As for the first one things have to be very quiet for that to work, right? If you're relying on the last message routed to a given peer being the one that you're talking about having failed then it has to be the last message that routed on a given path. Presumably if you take three or four hops it adds up. Things would have to be very quiet for that to work.

Speaker 1: I would want to model it. It would definitely get the near cases pretty well. And it's cheap because if we're doing it for congestion control anyway we could just have a bit that says: actually, this wasn't congestion problems it's a can't reach peer problem. It would just be nice. The two dovetail pretty nicely, because if you connect to my node, they send to this node, I can then give you an error.

Speaker 2: The problem is if it fails 70% of the time, suddenly you're retrying. Somebody is going to end up getting that error message, and they're going to retry something.

Speaker 1: Oh, no. In the error message, you encode something from the onion, right? You hash something in the onion so you can tell them: this is not for me, this is crap. Then you're out with three modes: I didn't get any answer back, I got an answer back, I know that it failed here. Even if that last case is only 20% of the time you get it, it's still nice. I just thought that if we're looking at congestion control, we should probably have a bit that says: this isn't for congestion control, this is a failure.

Speaker 2: When we get to the point where we need congestion.

Speaker 1: Hand wave. The other bit I think, makes sense to opportunistically connect.

Speaker 2: Yeah, I like that.

Speaker 0: Next up is offers. That also builds on top of all that. We just merged the last bit. Not exactly the last bit we needed, just for an MVP in Eclair. We have the receiving part, an offer manager component that lets you actually manage offers, respond to invoice requests and accept payments and defer some decisions to plugins. We've been able to test it with CLN and everything seemed to work OK. So the only part we're missing is to actually do some pathfinding for the invoice request message. Apart from that, we already have everything.

Speaker 1: Ours is really dumb.

Speaker 0: We're getting there.

Speaker 1: Yeah, we are getting there. Speaking of which, I think the route blinding PR needed a squash. Or is that already done?

Speaker 0: It is question to do you want to have a single commit because I split it into three logical commits: one with just the crypto, one with I don't remember what and one with the payment part.

Speaker 1: Logical is even better. That's fine, I'm glad you did it.

Speaker 0: So now it's three nice commits.

Speaker 1: I will rebase the onion messages one as well. Then I'll rebase offers on top of that.

Speaker 2: We're still dealing with all of the: how in what way do we derive all of the secrets to deterministically respond to an offer and sign an offer and generate a random key to sign the offer and generate a random key to as the payer key and all that.

Speaker 1: There's a whole heap of fun with persistent key pairs and things like that, if people want to start down that path of and fake IDs.

Speaker 2: I think we are gonna have a two options: a persistent payer and one that will always be randomly generated. They won't be attached to your node ID or anything. We were discussing that this morning, but we'll have an option to provide the nonce used to derive the payer key and use it repeatedly for all of these payments or just generated a random key.
Speaker 1: We're always doing a hardened derivation. In the future when we you want to do a refund the information is in the invoice that you write, which is one of the fields that you include.

Speaker 2: We're doing something similar, but we're not doing a hardened derivation because if we're using a random key, we might as well use the key derivation for that key to also be the checksum so that we don't have to include a bunch of data in the metadata. We put an ID in the metadata which is smaller, but then we actually use the key itself. 

Speaker 0: I'd be interested in having more details about what what you come up with because currently we don't do anything fancy, we just reuse the same one. It's on our to do list for later. It's also something that came up when doing those stateless invoices because when when you respond to an invoice request, you definitely do not want to store the invoice on your in your DB because otherwise you easily get dos-ed. We just encoded everything in the blinded path. Right now the way we do it is very naive and not efficient at all. We can probably do better. I think it would be interesting to share ideas on how how people want to do stateless invoices for Bolt 12.

Speaker 2: We save the invoice.

Speaker 1: We save the invoice, but we we have a really short expiry, so we can time them out pretty fast.

Speaker 0: You can kill your DB access because I'm going to send you invoice request all the time.

Speaker 2: There is a discussion in the Bolt 12 discord where I went to the code for using for that. If you're interested take a look there. We're basically doing what I described. We're just hashing all the data in the in the invoice, taking that doing an HMAC with it, using that to derive the key and then using that as your signing key or payer key. Then if we hash it again and the key checks out and we know that it was ours.

Speaker 2: Unless of course the user is giving us a defined key, then we shove it in the metadata.

Speaker 1: I have a dumb question to ask actually not about this, but if we are between topics. What are people's rules for setting fees on commitment transactions when they're doing zero fee anchors? I'm at that point of implementation and I'm wondering what the future min fee going to be, what's the answer?

Speaker 0: You only want it to be above the min relay fee.

Speaker 1: We've got a different future problem than the previous future problem, but it's still a problem until we have package relay. I wondered what people did as a heuristic. I'm tempted to say 10. No one ever needs more than 10 sats per fee byte.

Speaker 2: Just use the longest fee range fee range fee estimate they have.

Speaker 1: At some point the problem is a month in the future when you decide to close and min relay fees higher than 10. I was thinking, the estimate fee or whichever is higher? I wondered if people had already spent nights wrestling over the formula and I can just steal theirs.

Speaker 2: The problem is you're still stuck with: my counterparty requested something that I think is too little and I'm gonna have to force close again problem.

Speaker 1: Yeah, we're gonna be pretty tolerant.

Speaker 0: The best answer I got is just wait for package relay and make the commit transaction zero fee which is much better.

Speaker 1: The math is so much easier.

Speaker 0: The next step is taproot and taproot gossip.

Speaker 3: We had some discussion about that last week specifically. If one of the sides had a threshold signing frost setup it might be a siloed, so we had the idea to have the local nonce. At the very least until you know it's time for channel closing negotiations, for it to be constant. Even with the local nonce you're always producing a partial signature. You're only ever using the remote nonce and that would certainly simplify a bunch of things as long as there really is no configuration where you might be producing a signature in any circumstances such as using a watchtower for instance. I don't think it really necessarily involves any changes to the protocol unless somebody were to be overzealous and enforce distinct local nonces for their counterparty, which is a long shot.

Speaker 2: We still have to do something for the revocation secrets.

Speaker 3: Yeah, of course.

Speaker 2: You can't use the hash trick anymore. You just have to store all of the revocation secrets which sucks.

Speaker 3: We had some thoughts some alternatives to that also might circumvent the need for a verifiable encryption where instead of revealing a secret you would actually pre-sign with sighash none on your side for the spend for the other parties local output as well as for the HTLC outputs. I think you would mess up the cost and that would definitely complicate a lot of things. Maybe let's get to that bridge later. I think that at first glance it definitely sounds like it might be really dangerous. What are people thinking about the potential to not change the local nonce initially?

Speaker 1: Prove it's safe and simple is good.

Speaker 3: All right. Other than that, I think as far as dependencies on our side towards moving towards interop, most of them should be out of the way. So hopefully soon, but we've been saying that for a while now and something has always been persistently coming up, so I don't even believe myself at this point and neither should you.

Speaker 1: Speaking of gossip, is there an issue actually created for the V1.5 gossip? I believe there is.

Speaker 2: There was some back and forth on the PR.

Speaker 2: We're still in the stages of just wanting to get some discussion going on certain topics.

Speaker 1: I think the main ones are at what level should we still be binding to the Lightning context? That's probably the main thing people are upset about. Then there's other small ones like: Should we go full TLV or not? Should we have TLV defaults or not? The other big change is the timestamp to block height change, but I think everybody's pretty on board with that.

Speaker 2: Flip a coin on full TLV. Obviously, I feel strongly on the privacy and bindings and that kind of stuff.

Speaker 1: The problem with going TLV for things that are actually compulsory is then you now need to check that. Which is just a bit of a pain. On the other hand, if you chose to put something in there then you want to move later. You've pinned yourself into a corner, so I can see both sides. I think there's going to be a gossip v2 proper later. I realized a few weeks ago you responded to all my comments, so now I will go offline and respond to all yours.

Speaker 2: I would put good money on if we fix some of the privacy issues, gossip v2 will be such a low priority that it doesn't happen for years. Hence why I'm pushing the privacy stuff now because I feel like it's going to be such a low priority at that point.

Speaker 1: Well, it is a really simple change in effect. It's slightly weakened it so you just prove that it is an output rather than proving that it is of the form that you expect currently for lightning. We can have that debate.

Speaker 0: (Redacted) your proposal to fix it without complex cryptography to just let you just omit the onchain point? So there's two?

Speaker 2: There's two pieces here. There's step one which requires that you show that the on chain output is a two of two. So don't require that. Just remove the second pub key, don't reveal that. Then the second one is: optionally, up to some overcommit ratio don't include the real SCID, use some fake SCID that's some big number. You include a bit that says: does this come out of node one's balance or node two's balance? Every node is allowed to have two X more, or whatever, in channels than they have proven on chain. Whatever number we pick for the ratio, we've actually doubled it because each of the two nodes can then overcommit. If we say two X more, that means we're effectively saying in total we can have four X more channels than there are UTXO groups.

Speaker 1: That way you move proofs into the node announcement, which is significant. One of the whole points is that you don't want to expose UTXOs, so you proved you got some skin in the game for anti-spam. What an implementation does by default, or throughout trading proofs and crap like that, will be they use the real UTXOs from their channels. So at least they'll only have to expose the first two channels and maybe the other two can be hidden. If you can insist on one to one, then effectively every implementation, unless they're doing something clever, will end up exposing all the channels again, because they need to prove capacity. Capacity is important because everyone's using Pickhard payment style routing where capacity becomes an issue and bigger is better. So in practice, you won't gain any privacy because everyone will have to tell you all their UTXOs. You won't necessarily know which ones are with which channel, but it'll be pretty obvious for most nodes. So having a magnifying factor allows them to obscure some of them.

Speaker 0: How do you prevent people from giving your capacity? I guess you're going to fizz it a bit compared to the real on-chain out point and you're not going to announce it right after you publish the transaction? What's the distribution of amounts in Bitcoin blocks nowadays? How long should you wait and how much should you fuzz the capacity to make sure that people cannot just trivially know that this has to be one of these five on-chain outputs, for example? So is it really going to gain us privacy?

Speaker 1: There's a reasonable number of transactions, particularly as you move forward to the future, where people are doing things like using each other's UTXOs and making trades. You can really obfuscate the graph, which is pretty nice. The early ones probably won't have a huge impact because implementations will be done and they will just go: here's my new node announcement, and here's my new channel, completely unrelated, right? It'll be obvious. The first channel will be obvious, but beyond that, maybe not as much.

Speaker 2: I think that until people have a chance to really dig in and spend a lot of time on implementation, it's going to provide very little privacy. Eventually, I would hope that it can provide more. That's part of the reason also why you don't want to require it via multi-sig. Let's say you have a joint market node and you're a Lightning node, you should be able to just say: hey, I'm going to use my joint market UTXOs to prove liquidity for my Lightning node. Then I won't actually announce anything. That's my Lightning node because my Lightning node wallets are super commingled funds and whatever, and my joint market nodes are super private funds.

Speaker 1: To be fair, we can kind of do that already by basically just proving a UTXO. Although it does have to then we have a one-to-one match, right? So you have to have a UTXO that's approximately the same size as your channel. Otherwise, you're wasting everyone's time. Is it one UTXO is one channel? That's the current proposal. So you can't go: here's a million sats and here's a million channels? You do want to have some spam restrictions. So there will be a cap on how many as well as the amounts? You can't say there's a million one-sat channels because that's just spam.

Speaker 0: Also you still need to monitor those. If I give you UTXOs and I use them to prove channels, then I just spend the UTXOs? There's some reassignment you need to keep track of, which is not necessarily trivial if you're not using real channel outputs as your proof.

Speaker 1: In my original one you ordered them and you lost the bottom ones. You gave them a priority order, saying these ones are my important ones. If for some reason one of them vanished you would lose the lower ones you could no longer justify by whatever magnification factor.

Speaker 2: The approach in PR that was just that you sorted by SCID.

Speaker 1: SCID is good. That's made up numbers anyway. You have to agree on which ones you would trim. Particularly in the case where you lease from someone. At least it has to be a trust thing, where you go: cool, I'm going to lease a UTXO signature from you, and then they sign for you. Obviously they could spend at some point and you'd have this leakage. You do get 12 blocks to respond, but because there is the delayed closed stuff, but still you know that at some point you're going to need to go find something else. You would probably want to control which things worst case would get lost. That's gossip v2. There was a line between gossip v2 and gossip 1.5, where 1.5 was: what's the minimum we can do for taproot and 2 is do we shift this whole basis? I feel like we're sliding back in that direction.

Speaker 2: We don't have to define the actual negotiation protocol yet. Which is a big chunk of the complexity.

Speaker 2: The other question is: do you actually move the UTXOs into the node announcement? Or do you just leave it in the channel announcement and you say sometimes you don't have to provide one.

Speaker 1: No, you put them in the node announcement. I mean, you're effectively doing the same thing. You're referring to the node announcement and then moving them back to other channels. It's just that you're just doing it in the messiest way possible. If we're going to change the protocol anyway, we would move it to the node announcement, right? A naive implementation would just send out a new node announcement when it has a new channel. If you were doing the dumbest possible thing, which is not too bad. I thought we had decided not to do that?

Speaker 2: Well (Redacted) primarily had an objection on the overcommit generally. As well as, it must show a multi-sig in order to. That is a conversation to be had around, do we want to trade off privacy here?

Speaker 1: Yeah.

Speaker 2: We can discuss it again in two weeks, hopefully (Redacted) is here.

Speaker 1: I think it's an easy halfway point to at least do the whole just proof that you have some control of the UTXO and don't define it. I also want this to a future be able to be used for existing gossip. So it would be nice if we could get rid of V1 gossip at some point, right? Legacy channels would still work, and that would just fit under the same kind of model. Although there might be special proof, but the same idea. You just prove that you have control of a channel and you're done.

Speaker 2: Eventually, we'll replace it with ZKPs.

Speaker 1: There'll be ZKPs, there'll be mini-sketch, there'll be all the things.

Speaker 0: Eventually. Maybe (Redacted) is already ready to use starks replace everything. We'll see what they comes up with. The next topic is fat errors, but I don't think that anyone has actually made progress on that? Nope. I have those two small competing PRs to rework the channel re-establish requirements to actually match better what we do, and verify that this is what other people do. There are conflicting requirements nowadays in the channel re-establish field, and it's a bit messy. It's really painful to review, honestly. So, whenever you have time and you feel courageous enough, take a look at it. Definitely not something to do now. I re-included the old peer storage backup proposal, because I think that Core Lightning has started working on it? Were you basing your work off on that PR or something else entirely?

Speaker 1: No, our implementation was the dumbest possible. There's two messages and there's two feature bits. The feature bits are the same, but the messages are basically: here, take my encrypted data. The other one is like: here is your old encrypted data. So, they're separate messages. It's the simplest possible scheme that we could come up with, and it's trivial to implement. The complicated thing is dealing with restoration of data. Obviously, the restoration case is a lot more complicated. The actual mechanism and protocol is really simple. (Redacted) who's working on it, is currently seeking a grant to continue that. Part of that will be actually writing up the spec and going through that process. We have an experimental feature at the moment that does it. The spec is going to be pretty trivial. Just mainly advice on what to put in there. At the moment, we're essentially doing the static channel backup. You could fit quite a lot because you've got 64K. You could actually keep a lot more state. My ambition is that we would keep enough state that we could restore all the channels that didn't have HTLCs in flight, even if we lost everything except for the seed. You would not be able to penalize old HTLCs in that case because you wouldn't have kept that old state if they tried to cheat you after that. Obviously, that would only be until you did a splice, because after that point, you would lose all the old transactions so, you'd be safe again. The idea is that you could stumble along quite well just on this pure backup solution, which I think is really good for people who don't read instructions and don't back up their node. It is actually pretty nice. There's a pain point in that you really want to send it before the reestablished message. The way we do it is that there's a client and a server because you cannot be both storing each other's backup. Otherwise, it just doesn't work. The one who is the client is never sending channel reestablished first, always waiting for the other guy to start. The backup is included in the channel reestablished so that you can first check it before sending yours or restore. It works better as a separate message because then you just always send it first if you have it.

Speaker 2: Why does it need to be a client and a server? Why can't both sides just store each other's data?

Speaker 0: If both sides store each other's data and if only one of them loses data, the other one thinks the one that lost data is cheating because he's not giving him his up-to-date backup, so he's not giving him back to backup either. If either side loses data, you're actually not benefiting from the backup because one side thinks the other one has cheated and the other one has just lost data or is maybe cheating.

Speaker 1: We don't penalize you for cheating though, we don't have any penalty mechanism for cheating. So, if you don't give me my data too bad, the idea is that we have enough peers that somebody will give us the honest data? We don't do the enforcement thing that we do with reestablish.

Speaker 0: I think for wallets you should do it because you only have a good guarantee if you're checking it every time you reconnect to your LSP. That's what keeps them honest because if your LSP cheats, then they're taking a risk because you have checked at every reconnection that they were not cheating.

Speaker 2: What if you sent a message and they shut down and lost the message and send you a stale state? Are you going to force close on a restart?

Speaker 1: No, we tried to avoid any reliability guarantees. So, I've sent it to you and I think you've got it, but you haven't actually got it because there's no ACK. I've just thrown it into the void and you may not have even saved in a persistent database. You may have just stored it in memory for a while. You all care, no responsibility. So if you don't send it to me, too bad, it is a weake incentive to cheat me. I can also start rating you over time and say: you never respond with my backup messages, I'm going to downgrade you as a peer statistically. I think there are ways of doing it in a more gentle way. You can both back each other up and not have a huge concern. That's why the proposal is now really, really simple, it is dumb.

Speaker 0: Once you have something written up, I'm curious to compare it with what we do and see if it would also work for the mobile wallet use case.

Speaker 2: How do you know when to send your channel re-established? Do they have to send a dummy pure data message in order to get you to send channel re-established? If for example, lost their backup data?

Speaker 1: In our case, as soon as we connect after the init message we send any data that we have. They've just connected so we also go: here's some data for you to hold. We were sending that to everyone. You have to have the feature bit, but there's no reason - it's an odd message. You can just spread it to everyone.

Speaker 2: I guess my question was: do you wait to see that data to check whether you're running with an old state before you send the channel re-established? Or do you just assume you're not running with an old state because you have some state, and you only care about that data when you are restoring.

Speaker 1: At the moment, we are really dumb. You do manual restore and you figure it all out. We'll then send our apparently invalid re-establish and fall through that case. We'll realize and we'll stop at that point. It's up to the user to restore. Eventually, what we hope is that when someone restores their node from seed, you'll reach out on the network. You'll see if you have any channels that exist, and go: huh, that's weird, I already have channels. Then start connecting to all of those nodes, and then try to get your data back. Then establish the one that's giving you the latest restoration, and start going from there. So, there's a whole unwritten side of that whole magic restore thing, which is important. That was the plan.

Speaker 2: Does it make sense, spec-wise, though, to just say: you can wait to send your channel re-establish, and if you set the peer backup feature bit, you must send at least a dummy one, even if you don't have any data for that peer. You must send a dummy one for your channel re-establish for nodes that are waiting.

Speaker 0: To unblock them. I think that would make sense.

Speaker 2: They always wait before sending their channel re-establish, even if they didn't have stayed before, which they may or may not know.

Speaker 1: Okay, so you're saying, I expect you to give me a restoration. That only covers the case where your database has gone backwards, not the case where you've completely lost your database. If you've completely lost your database, you don't have a re-establish, you didn't even know you had a channel. So, you kind of don't have this problem.

Speaker 2: My point is really that maybe you do care about when your state went backwards, so you want to wait until you see some of these messages before you actually re-initialize your channels and start going. What happens if you're waiting for this message and your peer lost its data for you and it's restored from one of these backups? Now, you're just, waiting forever.

Speaker 1: You would both deadlock, yeah - least of your problems, though. You've both managed to mess up your database. I guess the case is where you don't know, and so you're doing this as a precaution in any case. We don't intend to do that. I'm more concerned about the I've lost all my data case, where this is not a problem. If you wanted to put in a delay there, you could do something saying: I'm going to give you five seconds.

Speaker 2: The only thing the spec would require there is just saying: if you don't have data for this peer, you have to always send them a dummy backup data.

Speaker 1: That's worse. If you don't have data, don't send it.

Speaker 2: Well, then you have the deadlock issue.

Speaker 1: No, you wait. You wait for five seconds. You're addressing such a tiny corner case, I would not over-engineer it. It's your decision to implement it this way. We will not be implementing it this way.

Speaker 1: I don't think we will either. The only advantage is you then haven't told your peer that you were behind. You just seem really slow. Then you go away for a little bit and you come back and you pretend everything's good. That's is okay, it's going to be a little bit problematic. You would want to have that delay in that case. I think a reasonable delay is fair. I'd have to think through all the cases, but I would put a random delay in there for five to ten seconds. Is there anything that we should be talking about?

Speaker 0: We're going to be looking at quiescence and splicing because it's necessary for splicing. So we should be able to provide some feedback on the quiescence proposal as well soon.
