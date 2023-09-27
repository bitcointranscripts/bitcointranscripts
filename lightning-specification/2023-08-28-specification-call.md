---
title: Lightning Specification Meeting - Agenda 1103
transcript_by: Gurwinder Sahota via TBTBTC v1.0.0
tags: ['lightning']
date: 2023-08-28
---

Agenda: <https://github.com/lightning/bolts/issues/1103>

Speaker 0: I don't think I've seen any discussion happening on any of the PRs. So, I don't think we should go and have them in order, except maybe the first one that we may want to just finalize and get something into the spec to say that it should be 2016 everywhere. But, as [redacted] was saying, can probably make it a one-liner and it would be easier.

Speaker 1: Please.

Speaker 0: Okay, so let's just make that feedback, and wait for [redacted] to transform this into a one-liner. One other thing that I've seen a lot of discussions on is related to simplified commitment. We had a bug; there was an issue. I'm going to link that issue right now for a force close that happened between an Eclair node and an LND node, but then also happened between two LND nodes. This is a case where actually without simplified commitment, we don't have a choice because people on both sides can asynchronously be adding HTLCs, we can end up just getting into the remote reserve and having to force close because the reserve is not met. There's just no way to avoid that situation with current protocols. So maybe that's a good argument for working on simplified commitments at some point.

Speaker 1: Yes, it's definitely on my to-do list for this next release, which is three months away. We've just done a release, so now I can't use that as an excuse anymore, and ption simplified commitments is on my list to do and then scratch out an implementation. We have one that [redacted] did because they did it for L2, but we have to. It's slightly more complicated for the current LN penalty. So, I plan on revisiting that in the next three months.

Speaker 0: Okay. Yeah, I think it's really worth it because we're starting to see all those issues with people experimenting with sending a lot of HTLC that frequent weights, right? We are hitting those edge cases and we want to provide commitment. There's just no way to avoid it, and having false closes that we cannot avoid is really annoying. So, shall we just quickly go down the list in order and see if we have anything to say on it, or otherwise we just move to something else. So, do we have anything new on the simple close? On my side, I haven't had time to prototype anything yet. So I think it's more waiting for implementation.

Speaker 1: Yeah. I have to rewrite it because we did say that whoever's got the most funds will have to provide an output was the simplified version. So I'll switch to that, and we just accept that if your channel is really tiny and you can't afford to close, you can't afford to close, right?

Speaker 0: Yeah, okay. So just needs a small change on the spec, and then people starting to actually work on it. Maybe is there someone from LND who started working on that in the context of Taproot? Since the first Taproot PR was merged to master on LND. Is there some followup work that is being worked on on the closing side? Or is there someone from LND?

Speaker 2: No progress right now on that front list.

Speaker 1: Okay. Yeah, I know [redacted] was pretty keen to get this, so I expect it'll happen pretty soon.

Speaker 0: Alright. So, then on the spec cleanup — add to my to-do list to actually, at least, make those features mandatory in Eclair. I think we should all do the same, but apart from that, nothing new on my side.

Speaker 1: So, there is an issue that came up with splicing and gossip, which I was just reminded by the fact [redacted] made a comment in the offer PR, which was a little meta on short channel ID usage. So, we have this issue where if you splice your channel, we have this 12 block bridge, where if you know about a channel and it closes, you give it 12 blocks and consider it still to be live. Now, that has some weird cases. It means that during that time, you probably don't propagate any updates for that channel. You will annoy other implementations if they're completely new on the network. You'll be talking about a closed UTXO and they will be like: I don't know what the hell you're talking about. We stopped gossiping about that because I know [redacted] complained to [redacted], said that we were gossiping about dead channels all the time. But it also means if that's your only channel and you've just spliced it, you can't propagate your node announcement now for like six blocks. So while it kind of works almost, it's not a great solution. We had proposed previously that you have this magical update that says: Hey, I'm splicing, there's a thing happening. And somehow that lets you change the rules. Like you explicitly mark something. But it still doesn't help the case with new nodes coming on the network. How do you provide a splice in progress? If they've got a simple lookup and they say, well, this UTXO doesn't exist, it's not clear to me how we solve that problem.

Speaker 3: Is it worth solving?

Speaker 1: That's a good question.

Speaker 0: Couldn't we just emit a new channel update? We're still using the first SCID that has been spent, but we had a TLV with the current SCID that is unspent. Just say: Okay, you can look at the UTXO is actually unspent, and it is actually a child of the main one in the channel update.

Speaker 3: Or new nodes can just miss a single channel until they restart.

Speaker 1: That's possible. I mean, the question is: Do we allow the node announcement in the case, where the only channel you've got seems to be closed, and we're like: We're gonna let you do this for a little bit?

Speaker 3: Yeah. I mean, I would vote yes.

Speaker 1: Similarly, channel updates, right? So, can you change your fees while you're splicing? And I would think the answer is probably yes. You want that. It does mean some noise though, of course, for new nodes who will be confused if I'm talking about this thing that doesn't exist from there.

Speaker 3: Yeah, but they'll just drop it. I mean, they might send a warning message, but maybe they should read one of those warnings or something, I don't know, whatever.

Speaker 1: Well, you probably shouldn't send a warning message because the other node could be a block behind anyway. I mean, you always get that case where they think it's still live and you've seen a new block they haven't. So six blocks is a little bit pushing it, but still. Okay. I just wanted to bring it up because it's something that we should make explicit. Do you still propagate gossip for those? I think the answer should be yes. Maybe later we will. I mean, explorers are going to have to figure this shit out at some point because I think, at the moment, they’re marking channels close as soon as they close. So the channels vanish, and then they reappear again. Might be nice to have a hint that this is a splice in progress, but frankly, them delaying 12 blocks is probably fine too. Cool. I just wanted to bring it up, but if everyone's happy to continue down the same path for the moment, then I will just try to make sure that we do propagate on those.

Speaker 3: We can add a hint, but I would vote not having to add any logic around the hint. If we want to add a hint for block explorers or people to log or whatever, fine. But I would vote not having to write any code that deals with the hint aside from the occasional log.

Speaker 1: Okay, cool. Well, we'll leave it now and we can do something later, but yeah, I will restore our propagation. I'm reworking all this code at the moment, so it's a good time for me to look at whether we propagate these or not. But yeah, it's particularly annoying for the case of a single channel, where your node vanishes while you're splicing. It seems a bit unfortunate.

Speaker 0: Yeah, we haven't worked on the gossip part of splicing. We've just focused on doing it for private channels for now, which was simpler, but we should start working on the public part and how it links to Gossip. So, we should probably have feedback and ideas once we start working on that.

Speaker 1: Yeah, cool.

Speaker 4: I hope there's not a weird case with a splice that never confirms here.

Speaker 0: No because it never confirms the previous channel.

Speaker 1: Yeah. If you haven't confirmed yet, you can't even tell, right? So your individual channel is still fine. Everyone's happy with your gossip. So, it's actually pretty neat from that point of view.

Speaker 0: Any feedback on the spec cleanup or should we just start by just —in your latest PR, in your latest release in C-Lightning, did you make all those four features mandatory by default?

Speaker 1: No, it was too late, but that's one of the first batches that's gonna go into the new release and see what happens.

Speaker 0: Okay, we'll do the same.

Speaker 1: And even better: I'm gonna rip out the code that tests for it. it's gonna be fantastic, so nice.

Speaker 0: Alright, so the next step is the SCIDs in Blinded Path. I haven't thought about it more since last time. Is there a prototype implementation?

Speaker 1: No, I haven't implemented this yet either.

Speaker 0: And [redacted] or [redacted] on the LDK side?

Speaker 5: No, we've not implemented it.

Speaker 0: Okay. Yeah, I guess we should just wait then for people to implement it and see if it just works out okay, or if we discover some things that are annoying.

Speaker 3: Well, I mean it might end up being annoying for us, but that's okay.

Speaker 0: Why?

Speaker 3: Well, the Onion Messenger is wholly unrelated to the channel logic. It doesn't currently have any references to it. Now, it needs some pseudo references to it indirectly for paying multiple invoices. So, we can maybe reuse that interface, but currently there's no relation.

Speaker 0: Yeah, it's probably going to be annoying for us as well.

Speaker 1: Yeah, we already have that crossover in routing, right? Where you nominally have no real connection to your short channel IDs that you're gossiping, but now you have to. I don't hugely mind it.

Speaker 3: Yeah, I mean our routing system is obviously also separate from our — oh, you mean routing for on-EMS use, yeah.

Speaker 1: Yeah, exactly, the same issue, right? In theory, there's no real reason to have the short channel ID except that...

Speaker 0: Yeah, it just basically adds one lookup, so it's a bit more expensive to relay messages.

Speaker 1: The problem is do we need to — the argument for this PR was that it is worth it to reproduce sizes. If it is, then let's do it.

Speaker 3: Yeah, I think it's definitely clearly worth it on the forwarding parts — that introduction part is more annoying. But actually, the introduction part might be easier in the code. We'll figure it out when we get there.

Speaker 5: Yeah, for routing, though. I mean, not that it's restricted now, but it's really only important when you're forming invoice requests. Ideally, invoices wouldn't have these short challenges; they wouldn't need them at all. You know, wire. The point of having this is for QR codes, but we're not enforcing that in this method.

Speaker 1: Yeah. I mean, they are transient identifiers, and that means you get to keep both pieces. Of course, you could lose these things at any time, but there are cases where it might make sense. So, the latest version is using the encode alternative hack where we use O1 and O1. I have a love hate relationship with that idea. I know I came up with it, but I'm still — I don't know. If nobody thinks of anything better, then sure. Let's do that. Cool.

Speaker 5: Yeah, it makes the spec change pretty much trivial, which I kinda like. Otherwise you're adding new types for path, like an effort —TLV record for a different type of thing.

Speaker 1: Exactly. Now, if we were to introduce such a thing — oh, we've already got separate fields in onion messages — we could go back later if you wanted to and unify those fields and use the pubkey, but then put the SCID in there if you wanted to. I don't know if it's worth it. So fine. Okay.

Speaker 5: I was about to say it's also annoying when you have to, if you get — I don't know whether whether we would want to support both types of paths and offer for instance, or it was just one. It just adds more logic.

Speaker 0: Yeah.

Speaker 1: Cool. Okay. Other than the fact that I hate the fact that you renumbered things gratuitously to try to keep the deal.

Speaker 5: That’s no longer a problem ‘cause we got rid of that.

Speaker 1: Yeah, cool. So, I might fold this into my PR, so it's all in one place. The offers PR.

Speaker 5: That sounds good.

Speaker 1: Yeah. Okay, cool. Everyone seems in agreement. Easy.

Speaker 0: Yeah. On the other side, I'm preparing for the TabConf net next week. I'm going to do a workshop about writing plugins for Eclair, and we're going to write a Bolt 12 plugin so that people can accept tips using Bolt 12.  I've just finished testing it, and it's really, really easy to write. So, I hope people will start playing around with it, and we get to merge that soon.

Speaker 1: I am going to create another PR — because people love these things — that reintroduces this recurring payment thing, so that we can discuss that thing that we pointed out. But it will keep it as a separate PR, as an extension, because I think it's an interesting idea. There are complexities in there. I mean, it's definitely something that we want. It's a very clear use case that everyone loves. But I have very opinionated ways on the way you have to do it because people have proposed really dumb ways, where you'll call the server and ask: Do I owe you a payment? Or they'll call you and ask for another payment and stupid things. So, it's worth having a discussion once we get to that point. I will reintroduce that, which it was an old diff that I have to now rebase. Ooh, [redacted] has some news.

Speaker 6: Yeah, just chugging along. Merged several last week, but still some to go. So, we're pretty focused on it. So yay!

Speaker 3: We're making good progress. There was a bunch of conversation in the Bolt 12 discord around the spec for how you build the fees and the HTLC minimums, which I found to be very confusing. And then, there was more conversation and something-something. I think that's our next thing that we need to figure out. So, I would appreciate some help there, but I know people are busy.

Speaker 0: Yeah, I should spend some time on that document again to try to clarify that, but maybe after the TabConf. Okay then. Quiescence and splicing. I'm not sure there's anything new, but we were discovering more and more edge cases, where handling the reserve after a splice is really annoying when two people splice, and you have to compute the previous reserve. But apart from that, it should eventually be working great.

Speaker 1: Yeah, there was always the problem that with the 1% fixed reserve, if I splice in some massive amount into your channel, you can't spend, we can't — basically the channel's useless until — normally if I put like a hundred times the existing amount in a channel with a 1% reserve, what happens? Like, we can't use the channel now?

Speaker 0: We had a discussion on that in a PR that I created and then closed with [redacted] and [redacted] and the other [redacted]. The main takeaway is that whenever you splice, if a new reserve is not met, it's as if it was a new channel, actually. So, you should just enforce the previous reserve and start enforcing the new reserve only once it gets met.

Speaker 1: Fair.

Speaker 3: Presumably not allow any channels that make it worse, Or any HTLCs which make it worse, right?

Speaker 0: Make it worse in what way? As long as it's still...

Speaker 3: You have to make progress towards the new reserve if you have an HTLC going the wrong direction, which is still within the old reserve, but doesn't make progress towards the new reserve. Shouldn't you reject it?

Speaker 0: But that could be an issue when the other side adds a hundred times the price of a channel. You may still have an untrivial amount of money in that channel that you want to send out, but the other side is kind of forcing on you that the channel gets much bigger. So, are you then stuck until they push some funds on your side? Or should you reject that splice?

Speaker 3: You should reject that splice if you don't want — I mean, or you don't change the channel reserve, right?

Speaker 0: Yeah, in a way, They are adding a lot of incoming liquidity to you which is nice, but that means you need to then wait for them to use that liquidity before you can start using the channel again in your direction.

Speaker 1: Once the splice is locked in you will fall into the code where you have to head towards meeting your reserve if you haven't already. The question is: Do you do that once you've agreed to the splice or not? We should get rid of reserve.

Speaker 0: Is that what you do even for normal open? Well, I mean, if I open a channel to you with a push msat, so that you are initially under the reserve requirement: Are you allowed to send that push msat out or do you block that until…? I think because in Eclair we allow you to as long as you haven't met the reserve once. We kind of let you do whatever you want.

Speaker 1: Oh, I'm pretty sure we make you, you can only go towards the reserve. If you're under it, you can't get further away from the reserve. I don't think. I'd have to check the code though, but it only happens with push msat, and it doesn't really happen. Yeah.

Speaker 3: Yeah. No one uses that. But what about if you send one HTLC and then can they send it back? I don't know.

Speaker 0: Yeah. Reserve is annoying. Really annoying.

Speaker 3: Yeah.

Speaker 0: Anything else on splicing? Any new progress on either that or quiescence?

Speaker 4: I was just curious how quiescence is going for you over there.

Speaker 0: Oh, quiescence. We finished implementing quiescence, and it's even on master on Eclair. [redacted] wanted to try it against the Lightning to see if the quiescence part works. We know that the splicing part is not gonna work because we don't use exactly the same TLVs in commit-sig. But all the quiescence part, I guess, should be working. [redacted] will try that, and we'll try to do cross-compat tests on that next week, this week or next week. So we should have feedback on that one soon.

Speaker 4: Sweet. Yeah, I think it's one of those things that seems really simple, and the corner cases kind of creep up on you.

Speaker 0: Yeah, exactly. So we'll see what we find. I think initially we think that cross-compat is going to be easy. Everything is just going to work out great. Then the real world happens, and we find a lot of issues. We'll see.

Speaker 1: Speaking of splicing though, we should mention that [redacted] and I had this communication about feature bits. So because we've rolled out RC1 and had experimental splicing as an option, and splicing is like bits 62 and 63, [redacted] pointed out that until the spec is finalized and everyone's happy with interop, we probably shouldn't use the real feature bits. We're advertising if people turn experimental splicing on in core lightning, they get 163. So, we decided to add 100 to the bits, and I will document that convention, I think, and we should carry it forward. In the PR, you put: Hey, we're going to reserve this bit. That's fine. But until it's actually finalized, and you've done interop testing, you should probably add 100 and advertise like a shadow feature bit. And then, of course, in transition, if it's ratified with no changes, then you can just accept both features for some transition, and it will work fine. But it does mean we don't have this annoying case that we had with dual funding, where the spec changed, but our implementation still advertised the real one, and if you're perfectly spec compliant, you don't actually interop with everyone else who's also advertising the bit. Then, you have all these debugging pain. We always hold on: That's an old core lightning node. That's why it's not working. So, just going forward, we should probably adopt that rough convention that we actually advertise like on the experimental, like a plus 100 for a while.

Speaker 0: By the way, what do you do for dual funding in your latest release? Because I think that now most of the messages do follow the spec and we have internal testing on that between AKL and CLN, but there's still the channel reestablished part that hasn't been fully implemented in CLN and is not yet tested. So I'm not sure how that would be in practice.

Speaker 7: Sorry, the question is about backwards compatibility or just the progress on…?

Speaker 0: In the latest release of CLN, what is going to happen for the potential incompatibilities that channel reestablish…? We will just build that channel?

Speaker 8: That's a good question. I'm not sure, I'd have to check. I'm in progress of implementing it, so that would make it easier to test, because I'll have one. I will look into this this week. This is a good question.

Speaker 1:So, we have a point release coming up because MacOS. Anyway, so I'm holding that back, although we don't generally do changes like this in a point release because it's experimental. Whatever. If [redacted] gets a compact change, and we completely break or completely fix — whatever the euphemism is — dual funding, that's allowed to go in a point release. So, we could release a point for this. Certainly, if you reach an interop milestone with Eclair, that would be a good reason to put it in, even if it breaks existing core lightning. I'll just redirect all the bug reports to you.

Speaker 8: Great. That sounds good. The status on that is that the change has been implemented. I just need to update. It changes some of the tests. So I just need to fix the test stuff. So there's a good chance that we would have that ready to go this week. Question mark.  So, I'll try and move that up on my to-do list.

Speaker 0: Perfect. Nice. Cross-compact test during Tabconf, and we can release dual funding in TabConf.

Speaker 4: Hey, there we go.

Speaker 0: Nice. To be honest, we'll only have an impact. It's really the only thing that it fixes is people disconnecting after exchanging commit SIG, but not TX SIG on the dual funding channels. In practice, it shouldn't happen much. So, even if we break that or think that, it should be okay to release in my opinion.

Speaker 1: Yeah. The one thing I like about dual funding is — however bad it is, if you get through the funding stage, you're pretty much done, right? You've got a normal channel at the end, so that's nice. There is one case. So, I recently revisited our logic. If your channel gets reorg'd out after it's supposed to be all confirmed and you're locked in: What do you do? I changed the behavior to force close the channel, unless we were the funder, in which case we don't care. But if in the dual funding case, you do care. If they provided any inputs and you didn't trust them to do zero conf anyway, then at that point you should probably freak out if it gets re-org'd. And we don't actually track whether it was originally a dual funding. We track whether we put all the funds in, but that's technically not sufficient, because they could have put funds through the transaction. Not contributed anything to the channel, and you still can't trust it. So. there is a really mild corner case here, where you suddenly care whether it was dual funding, but that's only if it reorgs after your max confirms, in which case you're so screwed, it probably doesn't matter. So yeah.

Speaker 0: Alright Next up is Taproot. Is there anything new on Taproot? I've seen that a big PR was merged on LND. Oh, there's a question back there. Oh, there's a question about reorg.

Speaker 1: This is a good question. It depends. If your peer is trying to screw you at this point, you're in trouble. If it's just a normal reorg and it just bounces out and bounces back in again, then you're probably okay. Either way, our answer is usually just force close if we're in trouble. Force close may push the transaction back in because your closed transaction may — child pays for parent. There's no good answers at this point. In our case, if we trusted them to do zero-conf in the first place, we do not get upset and close the channel if it gets reordered out. But yeah, there's really no good solution. and it's such a corner case that you don't spend too much time thinking about. So, the answer was we tried to force close it. But, at least, that will stop us from making things worse by using the channel at this point. That was my theory: Alright, at least we'll shut the channel down and we won't send any more HTLCs. Yeah, note that our current implementation does not do this and we'll just continue to — it'll only get upset when the channel gets re-logged back in. So if it gets out, it will just not log anything and keep using the channel.

Speaker 0: Alright, then Taproot stuff now. There's a big PR has been merged on the LND side on master. I don't know if compact tests have been done with LDK. Does anyone have news on that?

Speaker 8: We've had, we've merged a PR, have a follow-up PR up in LDK, but we haven't looked at the LND PR.

Speaker 0: Okay. And do you have done any interop test between LND and LDK Or do you have any idea whether that works or doesn't?

Speaker 8: No, we haven't done interrupt testing with LND yet.

Speaker 0: Okay. And so for now, it looks like we're still using MuSIG2, even for the commitment transactions.

Speaker 8: Yes. We're using MuSIG2 for unilateral closes. Yes.

Speaker 1: Do we have anything, any progress on Gossip? Taproot Gossip?

Speaker 2: Nothing yet, [redacted]. We're hoping to make progress in the coming weeks.

Speaker 1: Oh, the longer it takes you, the further I can push it back on my own to-do list. So, I'm not pushing. I'm just asking.

Speaker 2: Sure.

Speaker 0: Alright, then it's attributable errors. I haven't followed up on the implementation PRs. I think we're at the stage where we're waiting for just interop testing and last reviews. And everything else is just still — people are still working on everything. So, any other topic people want to discuss? Or anything else people have seen or been working on that's interesting to share? It's August. Nobody's been working?

Speaker 4: I have a thing, which is not really a spec thing, but [redacted] and I were working through how you do cross-channel splices moving from one channel to another, and it ends up interacting with the signing order stuff a lot and just gets really complicated. Just something to think about.

Speaker 0: What do you mean? Many people trying to batch multiple splices across channels?

Speaker 4: Oh, like just a simple case. If I have two channels on my own node, I want to move from one to the other one. My signing order with those channel peers affects the signing order of passing PSPs around. It's not really a spec thing, but I just thought it was interesting, and it's actually more complicated than I realized. I don't think it'll mean any changes to TX signature ordering, but I don't know. It's interesting.

Speaker 0: Yeah, I think we had, at some point, a very long discussion about that. The ordering we chose, we verified that it guaranteed that there could be no deadlock. But it doesn't mean that the implementation is simple. It's a mess, but at least in theory, there's no deadlocks.

Speaker 4: Wait, are we doing it in the same way? We did end up on the same thing, right? Did we? I forget now.

Speaker 0: Yeah, I think so. I think it's the one who contributes the most to the transaction, not actually the funding amount, but just the amount of inputs. And if there's a tie, then it's the lowest pubkey that signed first.

Speaker 4: Yeah, lowest pubkey of the original channel, right?

Speaker 0: Yeah. No. Oh no, the current one, I'd say. Oh, good question.

Speaker 4: Hopefully, you wrote this down somewhere.

Speaker 0: No, I think we said node ID.

Speaker 1: Yeah, lowest node ID usually.

Speaker 4: Yeah, node ID. That sounds right.

Speaker 0: Yeah, we do node ID in Eclair.

Speaker 1: Well, it seems like [redacted] isn't coming back.

Speaker 0: Yeah, it's the usual reboot the whole PC to fix the issue.

Speaker 9: Cool. Was somebody else talking or can I pose my question?

Speaker 0: Go for it.

Speaker 9: I was wondering whether we are planning in the lightning spec to implement something that we can fail HTLC's or something like this. Not the current way, where we force the other person to accept an HTLC and we cannot fail it back. It's like UDP mostly, whether we plan to do something else.

Speaker 0: Yes, that's exactly something that we cannot do right now with the current protocol, but the simplified commitment change that I linked into the issue will enable us to do. I think, [redacted] called that an ‘add an HTLC,’ where the other guy says: Update add HTLC, and you instantly say: Oh no, I don't want that one. Don't even bother try signing it. Let's just remove it right now.

Speaker 1: Yeah, but you can also fail, but they have to send both signatures. So, they have to send: Here's this commitment signature if you fail the HTLCs. And then the question is: Do you have to fail all of the add ones at once? I think the answer is yes, because otherwise, you have to send a combinatorial number of signatures. So, here's if you're going to fail things, and here's if you're going to accept things. So you do have to send both signatures across. There are a few twists in here. but it becomes much easier to think about with option simplified commitment.

Speaker 9: Okay, cool.

Speaker 1: Yeah, definitely something we want because it simplifies your protocol a great deal in that you no longer have to specify what the other side is not allowed to send you. Because you can it can send you anything. It could send me things that go outside the balance or whatever, and I can just reject them. At the moment, we can't obviously do that because I would have to hold that state for a while. Similarly, with fee changes and things, you would have a neat mechanism to reject them. So, it's an obvious hole in the protocol at the moment, but definitely something we want to fix.

Speaker 9: I had another question related to the fee negotiation for static remote key channels. CLN was already carving out some exceptions because there were some negotiation problems. The spec just states: Have a reasonable range of fee accepted. I was wondering whether CLN is going that route to accept these things or will it still be there in the future?

Speaker 1: Sorry, we do accept a reasonable range. The thing is that with anchor outputs, which is currently experimental in CLN, but will ideally be enabled, since we haven't found any problems, since it'll be enabled on the next release in three months' time. Then, generally, fees are lower. We just don't get fee disagreements anywhere as much as we do at the moment. So, without anchors, you have to be fairly strict about — anchors do not reduce it completely. Don't remove your requirement to agree on fees completely. We're hoping for TX relay magic, and things like that, that will allow us. But for the moment, it's a significant practical difference that there will be less fee agreements. We're already pretty damn wide in the range of fees that we accept. We don't accept things that won't relay. That's kind of — I refuse to do that without some explicit user interaction, right? What happens is, particularly with LND, if LND gets into its head that a fair fee rate is like the minimum fee rate, and it's not on our end, it will never change its mind. It will continue to retransmit that. Basically, it will not change fee rate. Every time it connects, it'll try the same fee rate, even if it now no longer considers it to be a valid fee rate. So, it will retransmit. That's why we added in this latest release, an option to ignore fee rate — like, allow any fees on a specific channel. So, you can basically let it get unstuck. But there's a danger. If you accept a fee rate change that will not relay from someone, you're screwed. And people have said: Oh, but you know, this fee they've offered is slightly below what you allow. And it's like: Well, that's always possible. It's always true. So, the real answer to this is anchor outputs. And the real, real answer to it is better transaction relay so that we can basically go zero fee, and everyone can agree on zero. We can remove that whole part of the spec and all that pain. So, lobby your Bitcoin Core representative.

Speaker 9: Okay, thanks, sounds reasonable.

Speaker 3: [redacted], your release notes said something about better pay plugin, something-something, smarter routing. Are you now tracking history of failures? And if so, what scoring algorithm are you using for selecting?

Speaker 1: Yeah, so [redacted] has been looking at the green light stuff. So, obviously we can see people's payments at this point. We were doing some dumb stuff. We were pre-splitting, but above a certain amount. We automatically pre-split before we even tried to send a payment. It turns out that that does not work very well. That was actually increasing our failure rates because at some point, you start hitting HTLC number limits. So we eliminated that. There were just some dumb bugs, especially where we had an alias channel. We wouldn't consider it if we had a zero-conf channel. We didn't properly consider it in routing and things like that. Mainly, it was bugs. Our real hope is that the Renepay plugin, which is way experimental at the moment. Tends to crash; get upset. I'm hoping that [redacted], who wrote the min cost flow — because it's in the main cost flow part; it hits an assertion. It's like: Hold on, these numbers don't work. Like: Well, how did we get here? So, there's some fun debugging to go, but our hope is that we'll end up doing the min-cost flow approach, and we'll end up with something that is much nicer than what we have now, which is Dijkstra bolted on something, handwave, added some heuristics. So, there are incremental improvements, but I'm really hoping that next release will have something that doesn't mean cost flow and we get a decent idea of what's happening on the network. We don't even remember between payments at the moment. Renepay actually does keep history of stuff. It's a very low bar at the moment. It's pretty easy to improve. But we're hoping to jump right up with a complete rewrite.

Speaker 3: Okay. Yeah, I was just curious whether you were remembering or not yet as always I'd like to Keep up with what people are doing on routing because it tends to be the source of all of the failures that people say.

Speaker 1: The other thing is the explanatory power, right? When something does fail, trying to explain why is kind of interesting. It means that with Renepay, I designed it not quite the way you'd expect. We basically run it naively. Then we go: Well, there's a really good solution, but we can't use it because this peer is offline or something like that. It's not the most efficient, but it does give you more explanatory power. That you can say to them: Hey, this — because you've got like, Alice has a direct channel to Bob and tries to pay Bob. But it's not online at the moment, right? Or it doesn't have capacity or something like that. It's really nice to mention why the obvious thing didn't work because that's one of our main complaints. Why didn't this work? Its like: Well, you're not connected to the peer. So, it's trying to route around and things like that. So, it does somewhat affect the implementation because we do it more naively than you would expect, and then filter out the results, so we can give feedback to the user.

Speaker 3: Okay. Yeah, that's definitely a common complaint about all routers, I think. In other news, the node name on my public node has included a script alert tag for a long time. I finally got one. Someone was complaining that I was breaking their management software. So remind people to validate strings before they shove them into HTML. Also, someone really should try the SQL version because I'm sure we'll get somebody eventually.

Speaker 0: Does it work in mempool.space?

Speaker 3: No, it doesn't work on any of the public ones that I've seen.

Speaker 0: Too bad. Oh, and [redacted] mentioned getting feedback on LNPrototest on the mailing list. Well, maybe we can do that quickly.

Speaker 10: Oh, yeah, I'm pretty happy to do that. We are in the process to rewrite LNPrototest to make this a little bit more nice to read, basically. I was curious if some other implementation tried to implement LNPrototest runner and give up because it was too messy.

Speaker 0: Yeah, we regularly said we would, but then every time we said we would, either [redacted], [redacted], or someone else said: Oh, but let me write some more documentation to help you know what you actually have to do. And then, we've always just never came back to it. So, we never did anything, but we would really like to do something to get compatibility with the LNPrototest, but we've never actually done it. So, feel free to rewrite whatever you want. I don't know if LDK or LND has played with LNPrototest, but I think they haven't either.

Speaker 10: Yeah, no, with LDK, I arrived to a prototype, but LDK is easy because you need to build your node, right? So, at some point, it is pretty easy to support the LDK. I am also in the process to write some documentation on how to write a runner for it. Basically, what I think some implementation is missing — some way to pass custom key to the node to the lightning node. For instance, if a LNPrototest want specific channel key, private key, because we make some calculation on what we expect in the test. At least on the LDK side, I had some trouble to support the planar decay.

Speaker 0: Sounds good.

Speaker 1: Cool. I'm sorry, [redacted], I haven't reviewed your rework, but it's on my to-do list.

Speaker105: Yeah, now I am working on the way, how to chaining part of the spec, right? If you want write the connection integration test, and then you want to use the same code to do the funding channel, I am working on this way to chaining previous test.

Speaker 1: The main purpose for LNPrototest is testing cases that never happen. So, it's sending invalid packets, sending odd messages that aren't spec'd, stuff like that. That's been the main use for us. Not so much testing the normal happy cases, but testing things that never happen. Sending TLVs that you don't expect and things like that. That are harder to test in a black box testing way. So, I made it really hard to write this. Sorry.

Speaker 0: It would also be really useful for all the interactive TX testing, where there's a lot of messages that the other guy could send out of under, and it could create a whole heap of mess or being able to test that easily is really, really useful, I think.

Speaker 10: Yeah. Also now, on LND, we are implementing some big feature, right? Splicing all the stuff is really easy to say: Okay, this is the normal workflow and what we get. Something like that.

Speaker 0: Alright. If we have nothing else, we can just call it a day and get back to work.

Speaker 10: Sounds fantastic.

Speaker 1: Ciao.

Speaker 4: Cheers.
