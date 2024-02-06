---
title: Lightning Specification Meeting - Agenda 1127
transcript_by: Gurwinder Sahota via TBTBTC v1.0.0
tags: ['lightning']
date: 2024-01-15
---

Agenda: <https://github.com/lightning/bolts/issues/1127>

Speaker 0: First of all, it looks like we still have a mailing list. I don't know how much we can rely on that. But, in the meanwhile, nobody has sent any email on the mailing list. I guess we should be migrating to Delving Bitcoin for now. Has someone experimented with running a discourse instance somewhere else? I think it was [redacted] who was supposed to do that. Yeah, so I guess nobody. So, let's switch to the V3 transaction topic. Maybe [redacted] or someone else — if you want to give us an intro and tell us what you're expecting; what kind of ack you'd like to reach; and what exactly we should be working on to make sure that we are able to reach an ack — say exactly what we need and what would be helpful to us.

Speaker 2: Yeah, sure. Great. So, I'm going to share a doc that [redacted] and I put together for this. I'll go first and talk about the roadmap for what we're trying to achieve here. There's some really nice stuff that we get short-term and then some really nice stuff that we get long-term that kind of addresses a lot of issues that I'm sure y'all are aware of. The short term stuff is V3. One parent-one child package relay and ephemeral anchors. So, the idea there is that you could switch to zero fee commitment transactions with one anchor that either party can bump and your commitment transaction plus fee bumping child can replace each other in mempool and then, we can get rid of CPFP carve out. They should propagate with one parent-one child package relay. Hopefully, it's much more efficient with ephemeral anchors. Long-term, there is a very nice cluster mempool proposal — which I'm sure [redacted] can talk more about — and that kind of addresses a lot of the more fundamental mempool problems that just make things really difficult. Then, we can have a more general package relay built on top of that, for general ancestor sets and use cases wise. Hopefully after that, you could have things like batch debumping and whatnot. So, what we wanted to do is make V3 and ephemeral anchors as useful as possible for the Lightning use case. We wanted to talk about CPFP carve out going away. Does that sound about right, [redacted]?

Speaker 1: Sounds right. So, the CPFP carve out — how many people know what that even is? Oh, there's a few people. I've got [redacted], [redacted], a few other people for sure.
But basically, it's a kind of descendant limit and ancestral limit based carve out for child replaces parent, where you use two anchors today, and it lets you spend your anchor without having to RBF their package essentially. But in a cluster mempool world, that might be a little difficult. [redacted], do you want to give that spiel since you're more practiced? Go on.

Speaker 3: I don't know how much context people have on mempool design and work that's going on. But I guess the very short summary is that in order to solve a lot of the problems we have today with the mempool. Currently, our mempool code does not keep a totally sorted mempool. We don't have a total ordering on transactions in the mempool. That makes it hard for us to evaluate the mining score of a transaction, which in turn makes it hard for us to design protocols that would like to know what the relative mining scores of transactions are. So, we think we can solve this by putting a bound on the size of connected components of the transaction graph within the mempool. By doing that, we think we can keep the mempool, kind of, fully sorted by sorting each connected component separately. This kind of allows us to have really nice algorithms for block creation, for managing mempool eviction, and for managing RBF, and ultimately, for things like package validation and package review, we think. That's further afield. The thing is that having a bound on the size of a connected component of the mempool is a different concept than having a limit on the number of descendants that a single transaction can have. So, I don't believe it's possible to come up with a similar carve-out kind of idea like we have for managing the descendant limit today. My quick intuition on this is —imagine you have 90 transactions that all have their two anchor outputs that you'd like either party to be able to spend. But one person is one of the parties on all of those and constructs a single transaction that spends all of their outputs. Now, you've got a cluster of size, say 91, and in order to allow every other output of every other transaction to be spent, your cluster could get as big as, say 180 or 181. So, I'd like to keep a cluster limit that is sort of bounded and doing that in a way that is both achievable and doesn't have a lot of waste where you artificially restrict limits to be very low to account for some weird carve out behavior that could may blow things off seems tricky.

Speaker 4: Before we get too far into this, I think it may be worth pointing out that I believe the only software that actually uses the carve out today is Eclair. The rest of Lightning does not.

Speaker 1: Is that so? Core Lightning, for example, does blind.

Speaker 5: Everyone uses it.

Speaker 1: Yeah, if you do a blind spend of the counterparty's latest commitment transaction off the anchor, that could use it.

Speaker 4: Right. I didn't think anyone but Eclair did that.

Speaker 1: Core Lightning does it. In my research for this topic, when I implemented the alternative spec, I said: Oh, it actually does that. Well, I'm surprised to hear that.

Speaker 5: I mean, you don't need to explicitly use it. You sort of get it as a side effect of the rule existing. Are you talking about targeting some specific spend or …?

Speaker 4: The only reason that Lightning cares about it is if you assume your counterparty has broadcasted a state and you try to RBF that state.

Speaker 1: The latest state.

Speaker 4: Not necessarily the latest, you could assume.

Speaker 2: You mean CPFP rather than RBF.

Speaker 1: I don't think anyone does older versions.

Speaker 5: Well, we do a thing that we're changing now, where at any point, we're not necessarily sure which one they broadcast. Like, we'll actually try to potentially CPFP three different versions, right? Which is our version, their version, and their sort of un-revoked version, which may exist. That's what we do. 

Speaker 4: So you do as well now — you didn't use to, correct?

Speaker 5: We've done that the whole time. We're sort of reexamining this behavior now as far as doing it less. I mean, the current state of things is a bit fickle, but we had some complaints basically about we were being a little too aggressive when we were shooting these anchors. So now, we have a different thing, where we only try to sweep one when there's actually a fee deadline at hand. Another thing that we're doing now is — maybe this related — it's sort of like this interaction with fee filter, which I think maybe [redacted] pointed out maybe a month ago or so, where it seems like because the fee filters existence, we can only rely on just our own local mempool as far as inclusion basically when we're in broadcast.
Now, we're trying to look at our peers' fee filter as well because we realize that's the relay path. The relay path is what really matters. Because otherwise, our mempool maybe is too constrained because we have the default values. We're not actually evicting the fee level that they were evicting basically. This seems to be a wider spread issue that we're trying to investigate a little bit more as far as propagation and things like that. Because otherwise, you think something can propagate, but it's really not going past any of your peers. Maybe not some of them. This is a behavior as well where even though we have the default policy. Our mempool is like 200 megabytes — something like that itself —  and that causes us to have a much lower eviction rate. We think we can get a 10-sided byte into mempool, looking at our min mempool from Bitcoin. It's really much harder now, but that's an aside. I think that's something we're trying to fix right now because it's causing a lot of issues because many of the force closes we've been seeing over the past month or so are just due to cascades basically. So in LND, we have a parameter called mempool max anchor, which basically sets the max anchor rate that we'll set the anchor to basically, and that was like 10th out of byte because hey, we're in the zero fee interest rate environment before this. We're trying to make that automatic now. We're trying to make that automatic base off of the fee filter of all peers and also the mempool that we see locally as well. Because otherwise, it's something that people need to set, they're not setting it, and we didn't know what to set it to, but I think now we feel like we have a valid that we can use to automatically set it. That should just help out a lot of issues going on right now because people aren't studying this value and they can't get something into the mempool.

Speaker 1: Alright. Can I interject real quick?

Speaker 5: Yes.

Speaker 1: That's all reasonable. I guess the point was, people are actually using it. The only people that seem to be using it are Lightning Network folks, and we want to make sure that we're not rug pulling you guys on taking out something useful without giving something useful in return, right? So, that's kind of…

Speaker 5: But how can it go away, right? Because it's like policy and policy is like a gradient. Like, there'll be 27 or something like that, but like we'll still be relying on it.

Speaker 1: Let's say Bitcoin Core 27 got rid of it. It's not, but let's just say for instance, right? It's all the update lag would be there, right? The old nodes will still be around so things wouldn't still propagate using the old carve out, but over time as the network updates, then that would be going away, right? Specifically speaking, if people start upgrading to cluster mempool based implementation sometime in the future, over time the carve out would basically dissipate in effectiveness, right? So, that said...

Speaker 4: Specifically package relay, right? Package relay completely obviates the need for it without breaking any existing code as long as package relay is seamless, and magically exists, and we don't have to change anything.

Speaker 5: Yeah, the relay path exists. It's there. 

Speaker 1: On this document, I have some possible futures we could do — and we, I mean, you guys in the LN Spec universe — that I think are reasonable. Some are just using package RBF, some are using shared anchors that are keyed. You can do that too. So it's like min size output that both of you could spend or a single keyless anchor using ephemeral anchors. So, there's some choices there and we just want to make sure that with zero fee commitment transactions and all those nice things you get with it, that you guys would be incentivized to update to that and then wouldn't be relying on CPFP carve out anymore.

Speaker 4: That's essentially the story. Why does there — there doesn't need to be a change to the Lightning commitment transaction format at all to remove zero fee anchors as long as we get package relay.

Speaker 1: You mean like a package RBF, correct?

Speaker 4: Yeah.

Speaker 1: So that's another wrinkle here, right? Let's see. For package RBF, prior to cluster mempool, we're pretty limited. So, the design we're going through right now is basically you have one parent, one child conflicting with any number or up to 100 cold transactions that are all within cluster size of two. So, in this case, where if you're limited again, conflicting against a topology of size two, then we can compute much better the incentive compatibility of the RBF and accept it or not — if it makes the mempool better. It's actually, yeah. So, there is concern with short-term with being able to restrict the topology of our comparisons, I guess is my point. So, you guys don't even need...

Speaker 4: Are you saying that...

Speaker 5:  Sorry. To back up a little bit, you'd be happy with just package RBF, nothing else?
So, you'd be like a single anchor key.

Speaker 4: Yeah, we would just ignore the other anchor basically. Or code that doesn't ignore the other anchor would become dead largely.

Speaker 5: So [redacted] says: I don't think package RBF is enough to replace CPFP carve out. I think it was in the context of when you do package RBF, you have to — oh yeah. So, okay. There's the other issue where for package RBF, the children of your counterparty's anchor can be too large for pinning perspective? 125 rule three, correct?

Speaker 4: My comment hand waves a lot of that away.

Speaker 3: I think there's two different issues there. There's a pinning issue with — I guess if I understand you, what you guys are getting at, [redacted] — correct me if I'm wrong —you're suggesting that with package RBF, you would spend your anchor output with a high enough fee that it can replace whatever it needs to. Is that right?

Speaker 4: Correct.

Speaker 3: But so we don't currently have a good algorithm for sibling eviction. I mean, maybe we come up with one in this particular case, but then, you're still back to all the pending problems that I thought plagued this kind of solution.

Speaker 4: So, okay. There's a few problems here. The hack, even in a world where you're assuming that your counterparty — oh never mind. Yeah, I mean I'm basically hand waving away the pinning issue, assuming there is some alternative better outcome, right? So, maybe something like top of mempool, allowing eviction in some of these cases or something like that, where at some point, we're offering some very substantial amount of money for miners if they're willing to evict that other package. The fact that we're offering something that is substantial more than it means like something needs to change and somehow the policy needs to let us do that basically is what I'm saying.

Speaker 3: I don't think we have a proposal that is anywhere near the finish line on achieving that kind of a goal.

Speaker 4: Right, and I don't think it's realistic for — so, I mean, then you're talking about like a different commitment transaction format. First of all, Lightning doesn't currently have a protocol and people are working on one to change commitment TX format for an existing channel, right? 

Speaker 3: Got it. 

Speaker 4: So, we're years away from being able to deploy a new commitment TX format and saying: Yep, okay. We're like: Anyone who cares about it has upgraded, we can just stop the old one.

Speaker 3: Can I clarify one point on that? You specifically talking about going from two anchor outputs to say one ephemeral anchor output. Is that what you're referring to?

Speaker 4: Sure. Or whatever they're in. Zero fee. Whatever.

Speaker 3: Well, ‘cause I think there's another option which could be to simply make a — like the V3 proposal is to allow for transactions to opt into a topology restriction, which is that you can have at most one child. Now, we can tweak what that topology restriction is. For example, if you wanted to have a commitment transaction with two anchor outputs and that was it, and each anchor output could be a single spend with no other in-mempool parent, so you have a cluster of at most size three. I think that would be consistent with the cluster mempool design and still allow us to get rid of CPFP carve out without introducing any pinning issues. Unless [redacted], correct me if I got that wrong.

Speaker 1: Can you say the last part real quick? I didn’t hear it.

Speaker 3: If you had some variant of the V3 proposal, instead of opting into a one parent, one child regime, you opted into a one parent, two children regime. That would still kind of resolve — it would eliminate the need for CPFP carve out, I think.

Speaker 1: Yeah.

Speaker 4: So, to be clear, my comment about the time required to get a new commitment transaction format includes like: Well, all we have to do is change the version to 4.
That's still…

Speaker 5: What would the format change be? Is that just getting rid of anchors or is it something entirely more in-depth?

Speaker 1: I have a Strawman spec on number 6. You can see the Delta. It's mostly to get rid of update fee, change n version number to 3. That's mostly it. You can just take a look.

Speaker 5: Why do you — oh, you get a fee because construction is always zero fee now?

Speaker 1: Yes. So, you're left with — yeah, there's no fee negotiation during channel operation. You're relying completely on the anchors spends, right? This implementation uses not ephemeral anchors, but in principle, it doesn't super matter. You can reintroduce a minimal size dust anchor that's spent by one party pretty easily. That's not the complex part. It took me about two days to get some tests working on Core Lightning. Implement it myself. There's the one caveat being I didn't get the RPC calls handled correctly, but it was creating the right kind of transactions, generating them, trying to publish them. So, it's more of a restriction in format size or format than expansion. It's not any more complex per se.

Speaker 4: Yeah, I mean, in principle, these changes are doable.

Speaker 1: Yeah. 

Speaker 5: Yeah. But it seems to me like the bottleneck would be Bitcoind 27 or whatever that is.

Speaker 1: We're talking about a timeline. So, cluster mempool is kind of blocked on making sure that people are okay with CPFP carve-out going away. We don't want to rug pull people on that timeline. That's still a-ways out. You can ask [redacted] specifically.

Speaker 4: We’re assuming we were allowed a new commitment transaction format. Say Bitcoin Core rolls out some kind of limited package RBF. Then, we wait six months for the network to upgrade. Then, we start rolling out some new lightning commitment transaction format. We wait a year or a year and a half for people to have actually upgraded and the channels migrated, and then we rug pull the old format basically.

Speaker 1: [redacted], you can speak to timelines there. But yes, there is some sort of staggered timeline here, where people have to have time to upgrade rollout. Actually update their running software. All those things. If you just wanted minimal — if you just said: Oh, I don't care too much. We just need a limited package RBF that's sometimes pinnable, right? If that's the minimum bar you want, then we can do that faster. There is the one caveat that — again, I was talking about giving pre-cluster mempool, giving a package RBF that isn't like bananas when it comes to incentives. So that's where that restriction — I can link it offline, but there's current work. There's work for cluster size to package RBF.

Speaker 4: So, can we do something completely batshit and like have policy match lightning commitment TX formats? Like: Oh, if this transaction has two outputs that happen to be, whatever it is, 400 SATs, then it opts into TX version 4 and it gets all of these specific things, so we get package RBF.

Speaker 3: You mean we basically opt into new policy rules implicitly…

Speaker 4: Yeah.

Speaker 5: Yeah. You're saying pattern match on the current transaction format and get rid of the carve out…

Speaker 4: …the Lightning commitment transaction format.

Speaker 3: Look. I'll take anything that gets rid of carve out.

Speaker 4: I mean, we could do that today. That's not, that wouldn't require any lightning changes. Bitcoin Core can move at its own pace.

Speaker 3: Well, that breaks things for you guys though, right? Because, I mean, one of the things we would do is we'd restrict the spends of such a transaction, so you can no longer spend it out arbitrarily.

Speaker 5: So, if [redacted] is saying he doesn't care about pinning then all we need to do is give something that it gives package RBF. I think that's his point.

Speaker 4: No.

Speaker 5: No?

Speaker 4: Not quite because part of the answer to pinning today is using the carve out. Yes. It doesn't solve all pinning vectors, but it solves some of them. I don't know how everyone's wallet works, but you could imagine a world where we say: Alright. We restrict the types of anchor claims. For a Lightning node today that is using the carve out to work, the carve-out CPFP transactions must be only confirmed inputs. If we were to match for TX version 4 — that is based on just looking at the type of transaction and assuming it's Lightning — then, we would similarly restrict ourselves to also on your own anchor spends only confirmed inputs. But Lightning nodes should already have logic for only confirmed inputs because they need it if they're going to try to claim a counterparty anchor. I don't know if that would impact our users. It probably would, but we could look into that. So, I don't know what other people think about: What if we just restricted anchor spends to only confirmed inputs?

Speaker 5: Yeah, I'm pretty sure we do only confirmed inputs. Certain mobile wallets like to do a bunch of zero-conf stuff, and we discourage them from doing it. But, at least, like default, if you use a bump fee or anything like that, it's our automatic sweeping stuff, we always do only confirmed inputs.

Speaker 1: So, what about the case where you want to use the thing like the carve out? So, you're the kind of party that has made a large child, and then you're unable to package RBF because you don't like that the miner has a competing transaction, but you don't.
So, you're trying to package RBF, but you can't actually transmit it.

Speaker 4: We don't care as long as it's like as long as it gets confirmed and if it's not sufficient value to get confirmed, hopefully the rules that restrict it allow us to bump it, bump ours into getting confirmed.

Speaker 1: No. I mean, I was making the point that there's plenty of situations, where if you don't see your common party’s commitment transaction, you only see your own and they're pinning you using their anchor outputs, but it's kind of hard to put a whiteboard here.

Speaker 4: My understanding of this proposal was basically we would restrict something that looks like a lightning commitment transaction to not make it ‘pinnable’, where not pinnable means one transaction that can spend it up to a certain size with only confirmed inputs.

Speaker 1: Okay. So, you're saying V3-like, but inputting it onto a template?

Speaker 4: Yes.

Speaker 1: And then doing sibling eviction-like thing in this narrow band, basically you're opting into this. So, the counterparty could make a child of size blah, but this blah is limited and your spend of your anchor can implicitly RBF that. Is this what you're talking about?

Speaker 4: Yeah, basically.

Speaker 5: I mean, it depends. Like I was saying earlier, we do have quite a lot of stuff generally in the pipeline protocol wise. I mean, that's another thing just to be able to say: Hey, what are you working on today? What are their goals for the year? But it depends. If everyone makes it the number one priority, I think we can get it done. But there's just a lot of other stuff lingering.. 

Speaker 4: It can’t start until Bitcoin Core has shipped something, and then, also the network has upgraded, and then, also lighting.

Speaker 5: Yeah, I think [redacted]’s right in that us doing the format won't naturally be the bottleneck in the deployment pipeline for that sort of something like that.

Speaker 2: So, what if we had V3 in 0.27 or something?

Speaker 5: But doesn't that require that all of your effective relay peers also upgrade as well in order to effectively propagate?

Speaker 4: And from you to the miner.

Speaker 2: Yeah, and that takes time.

Speaker 1: So, from our perspective, it's like — if we think that we're rug pulling from you guys, then we won't deploy something until we know. There's also a lot of other people who have their own varied opinions that have weighed in. So we need to know: Are the people who are here actually gonna use it, use it? And what is that? So, that's kind of where we're at.

Speaker 3: I mean, I think also there's like a little bit of a chicken and egg here. I think we wanna make sure that if we're gonna deploy something like V3 so that Lightning has an alternate solution to what carve out provides today, we should make sure we design it so that Lightning community will actually use it. So, I think that's why we just need to know whether this is worth doing.

Speaker 0: For what it's worth, the changes on the Lightning side are really simple. I've had a branch for a long while that just changes the commitment transaction to zero fee and not a single income, but that would be easy as well. It's really minimal, and then it lets you clean up a lot of stuff in your implementation. It's only the upgrade path that may require some more work, but making the new commitment transaction format is really trivial. So, I'm all in favor of doing that.

Speaker 4: Yeah. I mean, the only reason I pointed this out is basically it's not that we wouldn't then switch to using V3 and Bitcoin Core could eventually remove this stupid matching garbage — it's that we could both move forward in parallel and Bitcoin Core doesn't need to wait for lightning to do anything or lightning node operators to do anything.

Speaker 1: So, you'd still have this — let's call it protocol update — you'd still have update fee, all the protocol would be the same, we'd still have issues with mempool min fee, but you'd get around the need for a CPFP carveout. Is this the idea?

Speaker 4: Basically, you do V3, but then, you also apply the V3 rules to this other template matching. And then separately, Lightning starts fixing all of this stuff because now: Hey, we have V3; we can fix this stuff. But it doesn't block cluster mempool. Cluster mempool can move forward at a pace where as long as Lightning nodes have a path from themselves to miners using V3 or V3 template mashed, then it doesn't matter. Bitcoin Core can ship cluster mempool. So, in the meantime, of course, Lightning wouldn't be able to be free.

Speaker 3: I like the idea of Bitcoin Core development not being blocked on Lightning Spec changes. Do you think that the template matching idea you're proposing is viable in the sense that you can come up with something that would just match what Lightning's doing today and it has extraordinarily low probability of matching anything else?

Speaker 4: I think so because you have these like two outputs that are both exactly — what is it, 400 and something SATs?

Speaker 5: Yeah, it's like 483 or something like that. 

Speaker 4: That by itself almost feels like it should be fine.

Speaker 5: Also, you could also set both the sequence and the lock time at all times. Like, there's like other smaller things that look weird.

Speaker 1: Yeah, ideally it'd be a very easy check, But I think you could. There's the theoretical possibility that somebody's doing something that looks like a unilateral close on Lightning, but is not. I've never heard of that, but that'd be the one theoretical risk.

Speaker 4: Well, and specifically, they would still propagate. They just wouldn't be able to build a large chain of transaction spending for that.

Speaker 1: Yeah, so I'll let this conversation finish. ‘Cause number four is like a follow-on to regardless of how we want to deploy this, what would it look like?

Speaker 4: I mean, I think to be clear, we need sign off from everyone that their anchor spends do not spend unconfirmed inputs. That's something that we need to basically sign off of all of the lightning implementations today. Now, it may be the case that it's already there because they need that logic to use CPFP carve out. So, using CPFP carve out, they already need this. But we just need to make sure everyone's on the same page there before we do something like this.

Speaker 5: Yeah, so with the case of LND, I have to double check, but we shouldn't be using unconfirmed for bumping. But maybe there's something like where do I think of someone doing a zero conf funding off or something that we're sweeping, which happens today unfortunately.

Speaker 1: Yeah, the real problem comes if you try to do a child pays for parent chain multiple times, right? So a chain of size three, say, or two attempts at child pays for parent — it's fine if first child per parent is high enough to succeed because it'll just confirm and you just keep going.

Speaker 4: Yeah, basically, we push people into RBF of the CPFP. I think that's okay.

Speaker 5: Okay. Any other high-level questions, [redacted]?

Speaker 3: I guess it sounds to me like there's a pre-consensus forming around V3 and its rules being a good idea and useful for lightning in the long run, but not necessarily ephemeral anchors. Is that what I'm hearing or is that not? Is that too strong a statement?

Speaker 1: It's changing anchors at all for now.

Speaker 2: Yeah, I'll profess to not be caught up on ephemeral anchors enough to actually have an educated opinion.

Speaker 1: Yeah, just check out the document. Drop a comment if you like. It's there. Everyone should be able to comment. It's just a way of talking about the future solutions. One other bike shedding thing is that the way we're limiting pinning — this is number four on that doc — the way we're limiting pinning is by picking an arbitrary number that's much, much less than the normal package limits and virtual bytes size and saying, if you want to CPFP, it must be only this big, and this big right here is one kilo-virtual byte. It's an arbitrary number. So, this is like a potential bikeshedding vector that, for good or bad, right? Basically, if you guys wanted to opt into this regime — even implicitly saying, right? — how big are your CPFPs? How many virtual bytes do you expect those to be, right? ‘Cause this is kind of — if you need 100 kilo-virtual-bytes, then we're back to where we started, right? But if you only need one kilo-virtual-byte tops to make an effective RBF of your CPFP, then that's the limit. There's other limits too you could pick. Does that make sense? That's number four on this doc.

Speaker 2: Yeah, so the question is kind of the smaller we make it, the more pinning protection you get. So I guess but I mean, the smaller we make it, the fewer UTXOs you can use for your fee bumps.

Speaker 1: Right.

Speaker 3: So, I guess the question is: What’s the smallest we can make it where you'd still feel comfortable that your wallet's going to always be able to fund your fee bumps?

Speaker 4: I was just going to say that the other issue is anchor HTLC outputs, right? Because you can spend up to 400 HTLC outputs that were in the commitment transaction in one follow-on transaction, and that has to be something that can't be pinned. It's not the same because it's not like an anchor. It's not like these two transactions, but it also has issues here. I don't know how that fits into V3.

Speaker 1: Let's talk about parent and child transactions. There's the commitment transaction, which would be the parent, and then, there's the child who spends at least the anchor output, right? I think you can spend the counterparty's commitment transaction with your to_remote output.

Speaker 4: No, this is not even anchors, right? 

Speaker 1: Sure.

Speaker 1: Oh, you're talking about HTLC pre-signed transactions?

Speaker 5: Yeah, he's talking about scraping HTLCs either due to a breach or just due to success or timeout, basically. That I tack those on as well.

Speaker 4: Yeah, there's like a lot of competition on those outputs too.

Speaker 0: But those don't need CPFP. You're only doing RBF since we do SigHashSingle/ SigHashAnyoneCanPay, right?

Speaker 4: That's true, but they still have competition around the pin. You could still potentially pin it, right? 

Speaker 1: So, yes…

Speaker 2: They can be CPFPed if you force closed, right? Because I'm not second level.

Speaker 1: So, last year in New York, I gave kind of the total design  where I, at every step — I think this is pin resistant, but it adds extra for the HTLC side of things. It was adding some extra bytes in the like the benign case. So, it was kind of out of hand rejected, I guess, and that was put as future work. So yes, that's out of scope for now. I do have hope that in the future we can fix that, but for now, put that as future work.

Speaker 5: Can I ask people about if they're concerned about that fee filter thing that I mentioned, basically? I guess I have two questions. Number one: What do you set your current max anchor fee rate to, if at all? Like, is there a configured value, basically? Then also: Do you factor in your min-menpool or the fee filter of your peers whenever you're doing fee estimation in order to make sure they can actually propagate fully? Because we're seeing instances where people aren't sending this value, which we need to change obviously because they should be automatic. But then, also other instances where due to them never seeing a certain class, which turns out can lead to the fee filter of their peers being higher than their own value — their notion of what can probably get skewed. And this seems to be causing a lot of force closes now generally as far as people either not spending that value or the value is set, but they’re not factoring in the actual greater fee filter. Right now, we've been purging above like 20 sat-per-byte and like that for the past few months.

Speaker 4: Right. If you just run a Bitcoin Core node, you'll often not limit your mempool because your peers are limiting your mempool for you.

Speaker 5: Exactly. Right. So, that's the interaction I stumbled upon just looking at some of our nodes, like: Oh, what's actually going on? For example, I wasn't getting purged at all. But then all my peers were purging from 25 or even above, basically.

Speaker 4: Yeah, so we don't use — I think we tried to, but then immediately stopped using the mempool min fee for the channel fee — because you just can't use the mempool min fee at all. 

Speaker 5: Yes. What we're looking to do is basically use our mempool min fee and then, some aggregation of our peers’ fee filter as well.

Speaker 4: Why not just look at the longest out fee estimate?

Speaker 5: That'd be far too low in order to actually even get to the mempool, and then, you can't fee bump because it falls out. Right now, people are just fucked right now. They were at like 11-sat-per-byte and things are just falling out. So, we're basically trying to prevent that now by factoring in the propagation fee rate itself.

Speaker 4: Yeah, I think there's no solution to that. The other solution to that is: Sometimes, it just works anyway because a lot of times, you'll have a path between you and a miner that has unlimited size mempools. And so, I've seen many transactions confirm like that. It's not reliable and I don't know what to do about it. But to answer in terms of the concrete, like: How to set fees? — you can't. There's no solution. Yeah.

Speaker 5: Yeah, so what do people do today for their max for the anchor fee rate, right? Are they still doing update fee as before? Because we stopped more, but now we're trying to do something slightly more automated. Like not get into the next block, but instead just get into the mempool, or rather, get into a dominant relay path that is.

Speaker 4: Yeah, we just use update fee as before with a relatively long estimate time horizon.

Speaker 5: But do you see the issue? Like, that can result in people's transactions just falling out of the mempool like right now?

Speaker 4: It can. It totally can. I don't know what the solution to that is though. There's no solution, right?

Speaker 5:  Yeah. I guess we've at least identified the problem.

Speaker 4: Mempool min fee and peer fee filter, maybe you can do that max with the long time horizon. But even the long time horizon estimate, in my experience, is usually better than mempool min fee. It's usually always higher, but I guess, there are certainly cases where that's not the case if mempool skyrockets.

Speaker 5: Yeah, okay, that makes sense. I guess we'll just try to explore this area because otherwise, people ask me what to do and I'm like: I'm sorry; we can't do much right now. We'd have to — it needs to stop raining. That's literally the response.

Speaker 4: I mean, if you submit your transactions directly to mempool space…

Speaker 5: Well, that's the other thing... 

Speaker 4: It usually does work.

Speaker 5: Yeah, I've been trying to get them to basically do their fee accelerator thing, but keysend based basically.

Speaker 4: Without any accelerator or anything. If you just send those transactions, it does usually work. Because there are enough miners with unlimited mempools that within a day, you'll get mined.

Speaker 5: Sure, sure. At least, the key sending was a way because people could write some side script to automate that, right? Like, if there is a quote-unquote mempool node or mempool dot space node or whatever, they could key send with a TXID to get a fee bumped versus like logging and doing whatever credit card thing they do today. So it's a tool at least. Maybe I can continue to bother them in DMs and I'll write a prototype or something like that for them to do, but alright. Curious if anyone had any good solutions. Seems like there's none really. We'll look into whatever fee filter aggregation thing and see if we can alleviate some of the pain until the weather improves.

Speaker 1: So the last recap is: So, we're asking from you, I guess, would be explicit ACK on the V3 side of things when it comes to topology restriction and whatnot, right? As a general one parent, one child strategy, is that good enough for everyone to move forward and what kind of sizes do they think are realistic?

Speaker 4: To be clear, if we're doing this on the templated format, it needs to be one parent, two children.

Speaker 1: Yeah. Well, what we do is we would have the child. Each child size would be restricted in some way to reduce the pinning, and you RBF it directly. So technically, it would still be one. It would just allow the sibling eviction functionality. I think we tried to explain. Does that make sense? We'd magically RBF the other child to keep the topology simple.

Speaker 3: Yeah, I think that should be beautiful.

Speaker 4: You'd evict the other child if a new child comes in that's better than the other child. 

Speaker 1: Yes. If it's incentive compatible, yeah.

Speaker 4: Ah-ha. It is fundamentally incentive incompatible, but yes that's okay for Lightning.

Speaker 1: What do you mean? 25 chain limits on the…

Speaker 4: You're fundamentally reducing the value of the mempool.

Speaker 1: Alright, you could turn it off if you want, but...

Speaker 4: Okay, I mean, whatever. It is fine. I was just...

Speaker 1: We can make better judgments about RBFs in this situation.

Speaker 4: Yeah. I mean, one parent, two children with only confirmed spends seems like it should be practical but maybe it's just not worth it right now, which is fine too.

Speaker 3: Yeah, I think we can discuss the one-parent two-child, I think. I think that's not inconceivable yet.

Speaker 5: Yeah, I think that means if you package RBF, you're paying for both of them though. It's kind of annoying, but we'll talk offline about it.

Speaker 4: Yeah. It's also reasonable to just say it's not worth it and we'll figure it out with cluster mempool, like we're just doing a short-term thing for now.

Speaker 1: Yeah I mean I think we can definitely do stuff that's more incentive compatible going forward. Top block checks are trivial. That sort of thing.

Speaker 3: Yeah, [redacted], I mean, you say it's not incentive compatible, but if you think about descendant limits to begin with, we have the same problem, right? Like turning down a transaction because your descendant size is it, is kind of silly. But then, if you're gonna allow it and then you evict some unrelated transaction that's also valid, you say: Well, that's not incentive compatible. But we have to do something, right?

Speaker 4: Of course. Doing it as a threshold of two transactions just feels weird.

Speaker 3: Fair enough.

Speaker 1: Too used to 25, [redacted].

Speaker 4: Yes, I've been spoiled.

Speaker 2: Thanks for your attention. I really appreciate it.

Speaker 5: Thanks. Yeah, I'll do my homework this time. Next time in this discussion, I'll be able to have some important opinions.

Speaker 4: Yeah, I've got homework to do. I mean, it sounds like in any case, there's going to be some, at least minor, changes on lightning nodes, even if we do this abbreviated version that I suggested.

Speaker 5: Yeah, I think eventually we'll need some change to support whatever finally is propagated there.

Speaker 1: I think the big one is just you're going to have to try packages together.

Speaker 5: What do you mean try packages together? You mean like what you're bumping? Like different combinations of what you saw.

Speaker 1: We dig it offline. I'll have to draw diagrams for this.

Speaker 5: But okay, I'll look at the Delving posts. Cool, I guess in the last 10 minutes, should we just talk about what people are working on right now?

Speaker 4: I know [redacted] had a discussion he wanted to open around Trampoline.

Speaker 5: Oh, okay. Cool.

Speaker 6: Yeah. Thanks, [redacted]. So, customers have been asking for trampoline and the async payments. At the very least, for outbound trampoline. I was looking at the trampoline spec, and the current status of it is that you essentially have a nested onion that is half the size of the standard onion. So, you have a standard onion that is 1300 bytes, and the trampoline node and its hop payload receives a nested onion that is 650 bytes. From there on out, it figures out how to construct the remainder of the path. Because the hop payload has to contain at least 650 bytes of data, that means that the trampoline node needs to be within the first half of the 1,300-byte package, such that the 650 bytes can be included in full. I was wondering if there might be a way to do away with that limitation. I had this idea of, rather than having a fully nested onion included in the trampoline node's hop payload, rather having the trampoline node receive a marker saying: Hey, you are the trampoline hop. You need to figure out the path to the next hop; and then having the trampoline node rewrap an onion. Basically adding layers back on top of what it has peeled and just imposing a limitation on how many bytes of additional data it may add, assuming, of course, that that amount of data is standardized for privacy purposes. That's really it. That is all there is. The one consequence of that is that because it now has to rewrap it and has to start not from the zero byte HMAC, but from the custom HMAC, it will create an interruption in the ephemeral session key chain. And so, it will have to tell the node that is the last node that has been inserted as an additional onion layer what the resumption is going to be of the original ephemeral session pubkey. Now, I think [redacted] has a bunch of thoughts and probably a bunch of security considerations that I haven't thought of and dangers that this imposes. So I'm expecting that this is not gonna work, but I would love to hear from you, [redacted].

Speaker 7: No, it's definitely all right. It's just a rephrasing that I'd like to do. If you look at it, you essentially get an onion that departs from somewhere else and then reaches your destination. And what you're trying to do is prepend a number of steps to get to that next hop, right? 

Speaker 6: Exactly, yes. 

Speaker 7: So, what you're trying to do is rendezvous routing, and so we can reapply all of the research we've done for rendezvous routing, including a trick that is very similar to yours. And let's see if we can rephrase it, essentially. What you're saying is that if the Nth hop is the trampoline, the N-1th needs to tell the Nth that it is a trampoline and therefore needs to switch the ephemeral key, right?

Speaker 6: Right, exactly. 4N+1.

Speaker 7: Exactly. So what you could do, for example — and that was one of my rendezvous proposals a couple of years ago — was essentially to say: Hey, let the Nth node actually process twice. It essentially receives an onion, it unwraps it the usual way with the ephemeral key it got from the previous hop, just like normal. The previous hop did not know anything special. But in its payload, it sees just: Hey, a switch of an ephemeral key. So it knows: Oh, I need to re-decrypt using this ephemeral key; and then, I actually get the payload that is destined for me. So, it is from a number of bytes. It is identical to your proposal, but it doesn't require the N-1th to be aware of this thing. There is another trick that I don't know if it applies here — because there was a way to compress an onion by essentially filling the padding inside of the final destination with the fillers of the previous ones, such that essentially at the rendezvous point, you ended up with a whole bunch of zeros in the middle that you could cut out and therefore get a small onion that you could nest into the larger one. But I think the first proposal is probably the same as yours, and we also just fixed the idea of having to have essentially two subsequent nodes be aware of being a trampoline, essentially.

Speaker 5: Can someone state the difference that we see between the idealized rendezvous and trampoline as is today? Because I understand what happened was something in between, then what I passed happened. I guess I'm missing the distinction between pure rendezvous — whatever we all thought that was years ago — and trampoline as it is today.

Speaker 7: The pure rendezvous essentially was saying: Hey, you have a small onion. You have an onion that you somehow compressed and that you could fit it inside of the larger onion that you needed. That is very similar to the current trampoline construction, by the way. The proposal that [redacted] made is essentially to get an onion, process one hop, noticing where do I need to send it next pre-pending a bunch of hops. So all you have is the outer onion. You don't have any sort of nesting in between, but you sort of are playing this accordion of essentially unwrapping the overall instructions and then adding places to get to that next hop.

Speaker 6: One thing I would point out, though, is that if the node that is the trampoline node is node number N. So, node N-1 does not actually know that the next one is a trampoline node because it is only contained within the hop payload for N, for the trampoline node. And rather than being a full prepension, what actually happens is that the trampoline node inserts a bunch of layers between N and N+1. So, if it has K shifts, then node N+1 will become N+K+1, but node N will remain node N. So because it has to find a route from itself to N+1 using those K additional hops. The other — yeah, but obviously, I wanted to apologize to you, [redacted], that when I was thinking about how to improve trampoline, it didn't occur to me to read up on the prior art on rendezvous routing.

Speaker 7: Honestly, I don't think I ever wrote them down as such.

Speaker 5: [redacted], do you want to go as far as this package-size thing?

Speaker 0: Yeah, so I'd like to zoom out a bit because fundamentally I think that was either there's a misunderstanding or we're actually just redoing the same thing but just bundling it slightly differently because the current proposal for trampoline —  which doesn't match the Eclair implementation, so that's why you need to match to look at the spec PR and not the implementation — since we put the TLV field that contains the trampoline onion, this can be variable size. This can be any size at all, and it's the sender that decides on the size of that. So, you can use any number of trampoline nodes in between, and [redacted]’s proposal, it only shifts that kind of one layer up — from being inside a TLV to just being directly in the route — but it actually has exactly the same constraints that this cannot be greater than the size of the route that are between trampoline nodes. So this constraint is going to be there regardless of how we do it. Regardless of whether we do it directly on the onion route or inside the nested onion. So, I don't really see what your proposal, [redacted], fixes here. I like the separation of constraint that the trampoline onion is actually in a TLV because it's like it actually shows the nesting that and it actually better matches what pathfinding algorithms are run. It's actually a simpler implementation and design. I implemented your version today and it seems to me that the nested onion version is actually just simpler and does the same thing. So, I'm planning to understand the reasoning behind your proposed change.

Speaker 6: Yeah, so I do think that the nested onion is definitely simpler than having to wrap it. There is one constraint though that it removes because whatever the size of the nested onion is, it has to be at least — so if you have that certain size, it means that the amount of space that you have is, it cannot be closer to the end of the 1300 total bytes that you can have across the entire Sphinx payload than that size of the nested onion. Whereas if you have the onion getting rewrapped, regardless of how much additional padding you allow or prohibit, the trampoline node can be as late along the path as you like it to be without any additional privacy implications or constraints. So it removes a small constraint. I think if the standard for trampoline onions is 650 bytes, then that constraint is gonna have a stronger or bigger consequence than if say, we set it to like a hundred or 150 bytes, but...

Speaker 0: Why do you want to set any constant? Why don't you want to let it be completely variable size and decide by the sender on a case-by-case basis?

Speaker 6: Oh well, you do want it to be standardized for privacy purposes. That I think is quite important.

Speaker 0: Not really. I don't think so. I don't see why, to be honest, because it's rather the sender that decides on: If I want to make it look like I could have that many trampoline nodes, I'm just going to choose that size. And if everyone does a variable size thing and adds some randomization...

Speaker 4: That fingerprints the sender though. That fingerprints the sender because all the senders are going to have some default. They're going to fix the value to 1, 2, 3, whatever, and then if we start revealing that, it's going to fingerprint the sender.

Speaker 0: What would you do instead of just randomizing it?

Speaker 7: So, I think you should always use the biggest possible inner onion you can to get to your destination. But I would argue that this constraint is actually a security parameter for us, because every time that we go from trampoline to trampoline, that could be a full 20 hops of more locked up funds. So, the number of slots inside of the inner onion times the number of slots on the outer onion is the length of the maximum HTLC, not considering CLTV and fee constraints, but you could end up locking up a lot of liquidity using that. That being said, even if we choose to have an inner onion that is half the size of the outer onion, we still have about 10 hops to get to our next trampoline, and then that trampoline has 10 hops to get to the next trampoline. I don't think we have a network that has a diameter that is larger than 10. So, I wouldn't try to push the maximum out of the length of the route we can get here because it could even be hurting us, and I think we do have quite a bit of flexibility already.

Speaker 0: Yeah, but basically, I'm not sure why we should try to change it because the onion nested in an onion is conceptually simpler and from the implementation side is simpler as well. So, I think we should really explain why it's bad in terms of privacy or an alternative would be better before considering changing it to something that requires more code and more complexity.

Speaker 6: I do think it makes it easier to have multiple trampoline hops, but I just truly want to emphasize that. Well, I don't think trampoline is really being used a lot, so I'm personally fine with just going with whatever the simplest implementation is.

Speaker 0: Yeah, I agree. I think that should be the reasoning, the simplest, and think that is cleanest from an implementation and conceptual point of view. To be honest, I think having implemented both versions, I think the onion inside an onion is really the simplest one. But maybe, but you, you have to do it as well and other people's opinions are going to be interesting here. Oh, I hadn't seen all the messages from [redacted]. Can you state that?

Speaker 5: I think the most important one, I guess, is working backwards from some of the new goals that they have as far as revisiting it. To my understanding, it's basically like ASIC retrend for mobile users. Basically, they can start a send and then go offline, and therefore, Trampoline Hub is basically doing the thing, which improves UXing. To my understanding, that's the main thing that they're working backwards here to achieve UX-wise. I think we talked about this in New York, [redacted]. I think you convinced me then, but maybe I've forgotten my prior insight around compatibility with PTLCs. Because at first, I thought there was some other thing, or I think it was related with the other routing thing, like the two-phase payment thing basically, where that's slightly different. But I think that's the goal here. At least with async send retry thing.

Speaker 4: That's the main goal, yeah.

Speaker 5: Okay. Yeah, and then my other questions were just around — I need to catch up here — I guess understanding how they can prepend and  can they derive a shared secret the entire thing's authenticated and so forth. Because my current mental model is similar to what [redacted]  talked about as far as just putting it in the nested TLV. But I missed the thing around how the pre-pend works. I'm not sure if that's written down anywhere in any of the spec PRs or if that was just something that was unveiled just now.

Speaker 6: Yeah, I can…

Speaker 1: Yeah, it isn't yet, but it's actually very similar to the switch ephemeral key idea that [redacted] described a long time ago.I think it's probably even still in the wiki part of the Github and was discussed, maybe even in Adelaide or something like that, where there was this proposal that we discussed that [redacted] detailed how you would do that switch ephemeral-key. I'll try to find it, but it's very similar to what [redacted] is doing right now.

Speaker 7: I should really just write these trickeries up because sometimes they can be useful. Onion messages, for example, would be really nice to have rendezvous for.

Speaker 5: Okay. Or you mean rendezvous onion messages? Or use it to make rendezvous better?

Speaker 7: You could add rendezvous to onion messages to essentially talk to some hidden service.

Speaker 5: Ah, sure. Hey, here we go.

Speaker 7: That's where that research comes from.

Speaker 5: I guess we can just have our websites in lightning pretty soon. Quick thing on the side. I remember last time, I think, [redacted] said you're going to start to look at taproot gossip stuff. I'm assuming now you're full on trampoline.

Speaker 6: Trampoline, it really depends. If we just go with the current status quo that is already implemented, I have a functional PR, so that completely matches.

Speaker 5: A PR for Trampoline?

Speaker 6: Yes, implementation for trampoline. So, once that is done, I would hope I can switch back to taproot stuff quickly.

Speaker 5: Cool. Then, as far as this, if y'all like searching about stuff as far — I don't know if this was like implemented in the past because there's only a few of them — but Trampoline node discovery. For example, if a new node is bootstrapping basically, and the only one in 16 Trampoline nodes, is there some new query gossip type extension thingy, where we sort of tell them we only care about this feature bit in the node that we get, we got to think about something like that or something else entirely. This is basically: Okay, a new node joining; they're not going to get the entire graph anymore and assuming template nodes have a feature bit, do they have some queries essentially to basically only fetch those nodes in order to do bootstrap and do pathfinding. Basically: What does bootstrapping look like for a new node?

Speaker 4: I mean, currently nodes can just download the whole network graph. So probably, we'll just keep doing that.

Speaker 5: Okay.

Speaker 4: To add feature bits so you can, but I mean it depends on the nodes. Depends on the LSP, you know. Some people will do the async approach of just using one LSP and sending everything to them. Some people will have a few more hops in the trampoline for privacy.

Speaker 5: And this is Trampoline for Async Sense, not necessarily a restricted channel graph. 

Speaker 4: Right. 

Speaker 5: Because you feel the channel graph is so small, you don't need to worry about it.

Speaker 4: Currently, the channel graph is sufficiently small, no one really seems to have a problem with downloading the whole thing.

Speaker 0: Actually, I want to highlight that there are two separate steps in the trampoline design. What we are working on right now with [redacted] is finalizing mostly the Onion construction. It's quite independent of how we then decide to potentially advertise trampoline nodes and then decide how to advertise the rates and errors. So, I think those two can be phased separately because only having the onion construction is useful for wallets because in wallets, you don't have any issue. You can just include those in the invoice and you can just either directly connect to LSPs that you know of trampoline stuff or find a small route to them. And then, we can face the potential advertisement and advertisement of fees in another future afterwards.

[Error in video, transcript cut off].
