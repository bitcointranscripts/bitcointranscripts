title: Lightning specification call 
transcript_by: Generated, Human-Verified by Carla Kirk-Cohen
categories: ['meeting']
tags: ['lightning']
date: 2023-03-13
---

Name: Lightning specification call

Topic: Agenda below

Location: Jitsi

Video: No video posted online

Agenda: <https://github.com/lightning/bolts/issues/1058>

Speaker 0: Well, then let's mix these up a bit. Is there anything anyone really wants to discuss? That has the quorum of people here who should discuss it?
 
Speaker 1: There was a brief mention on the Bolt 12 discord about whether we should build a Bolt 11 compatibility wrapper where the thinking basically is: The way LNURL works today is that it actually requests it and does the LNURL handshake. So, it gets a Bolt 11 invoice and then it can open with any Bitcoin wallet. It doesn't actually matter, any lightning wallet. It doesn't actually matter whether the lightning wallet supports LNURL or not. It just works. The question was: Should something similar to this be built for Bolt 12 so that, for example, a front end LNURL client can make that Bolt 12 invoice request, get a Bolt 11 invoice, and you can open it with any Bitcoin wallet? 

Speaker 0: When the LNURL request says I do or do not understand Bolt 12, then it gets either a Bolt 12 or a Bolt 11 invoice. So for LNURL, you can do it on the back end (I think).

Speaker 1: You could, but then we're still in the boat where, sorry, Iranians can't pay. Which is not a fun place to be.

Speaker 0: There was my proposal for extension to LNURL where you can put the offer in the LNURL. You do "O" equals and you recognize that match. You can go: "O" equals a valid Bolt 12 - I do not need to actually fetch it. I can pull it straight out of the URL. That doesn't help in this case because you cannot have a static one that has a Bolt 11 in it. The thing that the Bolt 11 bridge requires a very simple invoice, right? The offer has can't have anything exotic in it? To turn it into a Bolt 11, you need the Bolt 11 signature, which is tied to the encoding. You need the payment hash too, so you need to actually supply a payment hash at that point. 

Speaker 1: I think you would add a TLV to the invoice request and say: I would prefer a Bolt 11 invoice if you have it. You'd probably add that feature flag in the Bolt 11, or the Bolt 12 offer and then you just do that handshake. 

Speaker 0: In that case you could just return to Bolt 11. You take the Bolt 12 and then you add an offer. If you actually want to convert the invoice, that's a lot easier. You could do it for a simple offer, you can turn that into Bolt 12 directly. 

Speaker 1: Right, I don't think it's hard to do. The big complexity is it means you can't do blinded paths. This only actually works if the invoice where you don't have any blinded pads for it, which kind of sucks. 

Speaker 0: It's pretty trivial to spec out if somebody wants to do it. The other point was that there was talk of having this jumbo combo QR code that has on-chain, Bolt 11 and Bolt 12 in it all at once. If you have that, you can steal some of the Bolt 11 fields into the Bolt 12. In particular, the description might be worthwhile, right? 

Speaker 1: I think that's going to be super common. Definitely a thing to consider. I'm not sure whether the description is usually long enough to care too much about that exactly. 

Speaker 0: It's probably only a few numbers. 

Speaker 1: We could already do that with the Bolt 11 too, right? There's a description in the URI itself, and you can say: okay, don't bother providing a description in the Bolt 11 or Bolt 12, because there's one in the URI. 

Speaker 0: We could make that a thing. Someone would have to figure out if that is worthwhile. It's the only field that's obviously useful that overlaps all of them.  

Speaker 1: On that combo QR code you mentioned would there be a point of blinded paths in that?

Speaker 3: Since if you have a Bolt 11 in there, it's revealing the receiver. 

Speaker 0: Even if you've got an SCRD alias, you've told everything but the last hop. Perfect sanity of the good, right? I was just thinking about carving out the commit message during a splice to not require revoke an ACK. 

Speaker 2: It seems kind of risky to me to change the protocol so we don't revoke and ACK commits. Is there a reason that we shouldn't do that or that we should? If we don't revoke an ACK it and it becomes live, what happens? 

Speaker 0: You mean in the transition to a new commitment transaction? Technically we're abandoning the old commitment transaction to a new one. 


Speaker 2: It's not abandoned. We're going to have both commitments transactions. I wish {Redacted} were here because it doesn't make any sense to me why you would not revoke an ACK. We have two commit transactions that are both valid. There's no confirmations yet. This is all pre-signing, pre-everything. 

Speaker 1: So he was just saying you send a commitment signature for the new transaction, but we're not actually changing anything in the old transaction so we don't have to revoke? Aren't we still incrementing the numbers? 

Speaker 2: I feel like we still need to revoke an ACK. If you're incrementing the numbers I would.

Speaker 1: It's not like we're doing this all the time. So do we care about the extra efficiency of not doing that one extra thing? Of not doing that one extra fsync in this case? 

Speaker 0: I don't know. 

Speaker 2: That makes sense to me. Keep the same safeguards that we have normally. The other thing is you can change fee rates and other stuff during commitment sigs. So do we need to have a special case checking that you don't change those in this particular commitment? A revoke and ACK just feels important to me. 

Speaker 0: He's concerned about the case where we disconnect and we haven't received all the signatures. One side's got it, the other side doesn't. Classic issue. I'm going to have to read through this in detail.

Speaker 2: I found the old link in the conversation about this exact issue. I think {Redacted} and I deep-dove into it and then wrote out this summary.
 
Speaker 0: So with retransmit, it's the nastiest part of the spec, always. I generally prefer things where you over-retransmit. So idempotent protocols where you resend and I go: cool, I've already got that and I can ignore it. That's generally a lot easier to implement and less painful. You do need to think about it really carefully. On reconnect what do I need to retransmit and when do I not need to retransmit? If you can make it simple, always retransmit on connect and then ignore. That is usually the simplest protocol to implement and the easiest one to debug as well. 

Speaker 2: With splicing we can just consider the splice aborted, right? That just feels so much simpler. 

Speaker 0: The problem is there's no aborted case that works because you always can have one side thinks it's ready and one side thinks it's not. You always have to handle that case where I'd already sent and received my sigs and you're haven't receive your sigs yet. 

Speaker 2: Isn't that only during the signature case, right? Everything up until a signature could have been sent? In my mind it makes sense to consider that aborted. Then once a signature could have been sent, then we get locked into reconnect and retry. It felt a lot simpler. 

Speaker 0: You end up with one in each case. I aborted it because we hadn't finished. You always have that step case where there will be out of sync. That's the one you have to think about hard and go: okay, so what happens in that case? 

Speaker 2: If you look at the thing I linked to, that's part of why I was saying that the commit sigs should be in a specific order. So we can know who is responsible for sending signatures first. That allows us to know specifically that we're now like locked into this splice continuing. 

Speaker 0: I will read through that. I think that's the kind of thing that I need to think about really hard and offline. Probably not while we're sitting here on the call.
 
Speaker 0: I do want to kick off the channel upgrade proposal again. Simply because we're going to be using it for abandoning channels that have the old pre-zero-fee-HTLC anchors. There's a few of those in the wild. 

Speaker 3: Gossip 1.5?

Speaker 0: Do you want to give us a potted summary of Gossip 1.5? 

Speaker 3: I haven't had the chance to read the proposal yet. 

Speaker 1: Are we doing overcommitment or are we not? 

Speaker 0: No. This is very vanilla. I'm trying to figure out whether it subsumes legacy channels. It seems like it's in addition. So there will still be the legacy ones floating around for legacy channels and this one will be Taproot only. 

Speaker 1: I still fail to understand why we're not just doing overcommitment. 

Speaker 0: Finite resources. How much did we really want to do? Let's roll a six-sided dice and choose how much to overcommit. 

Speaker 1: The only thing that I really want to change in this message is that I want the timestamp switch to block heights, it's just easier.

Speaker 0: So we just had more gossip pain implementing zombies. It's just nasty, right? You receive a channel announcement, we haven't seen the channel update yet. We kind of put in this holding state for a while because it's not useful by itself. Also until you receive a channel update if somebody requests your gossip by timestamp range, you don't know because the channel update doesn't have one. So the channel announcement doesn't have a timestamp, the channel update does. Should I tell you about this channel or not when you ask for something in this certain range? With block heights, that's just obvious. We may need some bridging for gossip queries if we want to do that. What does a timestamp mean if you're asking for block heights? We'll have a separate query mechanism. I don't really care. We could use medium time to map it onto numbers if we need to. That would be my only concrete thing that I would like to change. It would be nice if this eventually subsumed legacy gossip. Rather than having two forever. Obviously, that's a longer term thing. 

Speaker 3: I wonder how feasible it would be to include channel update data as part of those updated channel announcement messages. That way we would never need to put something in a zombie state. On the other hand, it would require that both parties coordinate what they want to send out before they would have a feasible, broadcastable channel announcement message. 

Speaker 0: That's particularly problematic if your partner is offline. You're trying to say: don't use this channel. That's one of the reasons we do it this way. Also just for space. You tend to do updates a lot more often.

Speaker 3: Not saying that channel updates should always come with the channel announcement, but vice versa. When you're announcing a channel your counterparty obviously is online because you just opened the channel. The first channel update would be sent with the announcement, or have some hybrid message. Just food for thought. 

Speaker 0: There's some temptation to go: first time, it's a big combo message which has everything and then you just do updates. 

Speaker 3: It would make a lot of stuff for us simpler too, including with rapid gossip sync. 

Speaker 0: That sounds really nice, I'm just trying to think through the ramifications. I like it on the surface for sure. The question of overcommitment. This is the golden opportunity to introduce it, before breaking things anyway. 

Speaker 1: Mostly just because it's so easy. You just have to say: pick a number, make it 2x, 5x. I don't care. Just put it in the spec and that's it. Implementation wise it's not that hard. You just have to check the node. 

Speaker 3: Is it not that hard? It seems to me that it actually would be pretty difficult. 

Speaker 1: I think the other side of it is. The actual verification is trivial. The announcement and deciding whether you should announce is not trivial at all. At least the verification side is easy. We can figure the announcement out later. 

Speaker 0: There's still a whole heap of questions. What's your minimum size? We've got a multiplier, you can advertise 1 BTC of channels. Are you allowed to advertise 100 million channels? Probably not. You do need another number in there. The other thing is who does it. You and I both have node announcements, who gets charged when we announce a channel? Does it come from my credit? Your credit? Can we change that? It's not an entirely trivial space to map out. The announcement is hard. 

Speaker 1: The verification is trivial. 

Speaker 0: The verification is basically what we do now. 

Speaker 3: Well verification might be pretty straightforward, but after that handling the channel and routing is difficult.

Speaker 1: I don't see what's complicated there. You have to make sure to remove it if the original one got removed, but that's not too hard. 

Speaker 3: Okay let's stipulate that the implementation of it on the verification side is trivial. It will definitely introduce a lot of additional discussion and back and forth, which Taproot is going to depend on. In order to enable Taproot channels I think we should enable Taproot Gossip first. We're going to need to figure out how we want this overcommitment to look.  

Speaker 1: We have this opportunity to have a little bit of privacy for public nodes. To go from complete trash privacy to a little bit maybe we can implement this for in the future privacy. Without rolling out the entire upgrade to the entire network to verify the side of it. Let's not throw that away. Just because we have to implement a little more code. We have to figure out the other side of it later. 

Speaker 3: Figuring it out is going to take some time though. Perfect is the enemy of the good. 

Speaker 1: I mean figuring out the announcement side of it. 

Speaker 0: Maybe we should discuss it offline to flesh out the design. If you connect to me maybe I don't really want using my credits because I'm a tiny node and you're a giant node. You can just use all of my the credits to announce this one channel. There's interplay there. The other thing is if you can use any UTXO as proof of a channel, proof you own a UTXO, that also potentially gives you some privacy. It doesn't require it to be a specific thing, a two of two or whatever. Taproot gives us an opportunity to prove we have some control over it.

Speaker 1: That comes for free if we have a single signature, right? 

Speaker 0: Which we should just do. Do we have a single signature here? We still talk about Bitcoin key 1 and Bitcoin key 2. There's still one sig. It's a musing sig of the two keys.

Speaker 4: The four keys are still there. So it's still a single sig of the four keys. The two Bitcoin keys and the two node keys. Then it's also updating the signatures on the update messages, and the node announcement to schnorr. 

Speaker 4: It's definitely useful if you want to have your node secret be backed by multiple entities.
 
Speaker 0: It seems like a no-brainer, but they do require you to disclose the internal keys. Do we have to? We have an output. We prove control of it. Who gives a crap if it's a real channel or not? Could be our cold storage. But then how do we prove that the update came from the node without the internal keys? 

Speaker 4: Without disclosing it you publish the two node keys. You don't have to publish the two on-chain Bitcoin keys. 

Speaker 1: You just publish the one on-chain Bitcoin key. Yeah, in theory it weakens it a bit but in practice I think it doesn't make a difference. 

Speaker 0: You've proven you've got some Bitcoin. That's good enough. You're saying you're not going to disclose the internal keys? 

Speaker 4: You're not going to disclose the internal keys. You're saying you publish the aggregate funding key? 

Speaker 4: Yes.

Speaker 1: Then isn't that recursive musig? 

Speaker 4: No. 

Speaker 1: The two parties are still building out of the four. You're still doing a normal musig for the four keys when you generate the signature. It's just when you publish it, you partially aggregate it. 

Speaker 4: So are you just doing simple point addition there? Or you're doing the actual musig aggregation? 

Speaker 1: Presumably. I haven't thought this all the way through. 

Speaker 0: I think you published the taproot internal key. 

Speaker 1: You should just republish whatever is on chain. Or not even publish it because it's on chain, maybe you don't have to publish it at all. 

Speaker 4: That only gets revealed when you spend?

Speaker 1: The pubkey itself? No, the root pubkey is in the UTXO. I think you do need to tell them it. 

Speaker 0: You need it pre-tweak. 

Speaker 1: Point being: Let's take this opportunity to do as much simple privacy we can on the verification side. We can spec out the announcement part of it, getting privacy later. 

Speaker 0: I think that is where we could perhaps change it, to publish a single key - the musig key. Flipping that to overcommitment could be done in a hacky way. Where you announce one and you get another one for free, as a future extension. I know {redacted} was reluctant to break the linkage, but I think breaking the linkage is the whole point. So that's fine with me.  
