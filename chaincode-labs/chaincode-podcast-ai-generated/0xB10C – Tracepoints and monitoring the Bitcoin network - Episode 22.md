---
title: 0xB10C – Tracepoints and monitoring the Bitcoin network
transcript_by: Whisper AI & PyAnnote
categories: podcast
tag: ["What he's been up to since the residency", 'Monitoring the mempool', 'Mempool Observer', 'Monitoring Mining pools', 'MiningPool Observer', 'Mining pools not mining P2TR at Taproot activation', 'Why monitor the network?', 'Template discrepancies between pools and monitor', 'User-space Statically Defined Tracing (USDT)', 'Tracing Readme', 'Using tracepoints to simulate coin selection', 'Why are tracepoints in production code?', 'Using tracepoints for P2P monitoring', 'Using tracepoints to review PRs', 'Benchmarking Erlay with USDT', 'TransactionFee.info']
---

Chaincode Labs podcast: 0xB10C – Tracepoints and monitoring the Bitcoin network

SPEAKER_00: What up? We are back in the studio. Who are we talking to today? We're talking to OXB10C I know him as Timo. So we're gonna call him Timo. Okay, fine. That's it. Doesn't quite The student doesn't quite roll off the tongue. Is there anything in particular that you're interested in learning from Timo today?

SPEAKER_01: Thanks for watching! Yeah, I think we need to talk about Tether, what he's doing with Tether and Bitcoin.

SPEAKER_00: I'm not sure everybody's gonna get that joke. That's fine. That's it? I can't explain it.

SPEAKER_01: That's it, I can't explain it. All right, fine.

SPEAKER_00: Mm.

SPEAKER_01: Also rolls off the tongue. Totally. Also a short minor curve for tether. That's why. Got it. Thanks for joining.

SPEAKER_00: Well, we will talk to Timo about trace points.

SPEAKER_01: Anything else? Good evening member.

SPEAKER_00: Yeah, that's he knows he knows all that stuff. Yeah. All right. Well looking forward our conversation. Hope you enjoyed too

SPEAKER_01: Yeah.

SPEAKER_00: Timo, welcome back to the chain code office. You've been here before. Correct. Yes. Yes. Tell us last time.

SPEAKER_02: Correct, yes. Yeah, it has been has been three years now.

SPEAKER_00: nothing's happened since then. No, nothing at all. No, it's been the same. Timo was in the 2019 residency, the last in-person residency that we ran and in this very room was heckling our various presenters about Bitcoin and Lightning. And we did those, those two weeks of seminars. So since then, what have you been up to? What happened after that?

SPEAKER_02: No, nothing at all, no. After that, actually, I joined a startup in Zurich, the Shift Crypto guys, we worked on Plug and Play Bitcoin node, and I later moved on to Coinmetrics, did some mempool monitoring there, did some mining pool monitoring there, for example, which blocks mining pools mine on and so on, connecting to the stretching pools and seeing what they're giving out to the miners.

SPEAKER_00: And so was that closed source? Was that open source? Because you've clearly sort of gone into the

SPEAKER_02: Yeah gone into the that's industry work. That's closer. There are products using that behind the scenes

SPEAKER_00: There's Got it, okay. And so since then, you've been in the monitoring world. Right, yeah.

SPEAKER_02: Yeah, I'm really interested in what is happening on the Bitcoin network and what people are doing there and what they're not doing

SPEAKER_00: there. So tell us, what's the motivation to do that? Why did you gravitate towards those kinds of projects?

SPEAKER_02: So Bitcoin is an open system. You can do and you cannot do anything you like in the realms of, for example, policy or consensus. So it's really interesting to see how people behave in such an open system. And we often can gather insights and feed them back into development and improve things and then make things either align essentially better in some way or another.

SPEAKER_00: Cool. So the first project that I recall you were doing, the Mempool Observer. Correct. Yeah. So tell me about that project and then what did that morph into?

SPEAKER_02: Correct. So really early on, when I got started working on open source projects for Bitcoin, this was one of my first projects just mimicking Jochen Hoenigke's MempoolQ site, just because I wanted to try it out myself and I'm seeing where I got there. And then did another version of that in 2019. Actually, during the residency here, added a more like a live transaction monitor to that. So we actually plot the transactions by time they are entered by Mempool and the fee rate they paid. And from that, we actually can see some patterns. We can see people following fee rates or the estimates of the fee rates. We can actually see people doing consolidations, doing batch payments, doing RBF, and so on. That's really interesting to observe and learn from and see the patterns emerging there.

SPEAKER_01: One pattern that I really enjoyed looking at was multisig, you could split out the specific types of multisig and fee rate estimations as an overlay, and it was fairly easy to discover some of the market participants that way.

SPEAKER_02: Correct, yeah. Actually, I did a whole series of blog posts on that based on the data I observed there, for example, observing the blockchain.com wallet can closely follow their fee rate estimates and actually see the people using these wallets. So back at the time, they claimed to have one third of the market share in transactions. And I think that's true based on the data I observed.

SPEAKER_00: So as you do these monitoring projects and you did, you started with the mempool, but that morphed into mining pool as well. Right. Why mining pool? Why is that an interesting, well, difference?

SPEAKER_02: Right. Well... One key property of Bitcoin is decentralized resistance and well, we were fine as long if one mining pool says, okay, I don't mine one transaction, I don't allow this transaction to be included in my block, we're fine. But once we see multiple pools doing that, or all pools doing that, blocking or filtering certain transactions, then this property of Bitcoin doesn't hold anymore. And I think that's really important for us to know if that happens and maybe to react to that if we can, if we even can.

SPEAKER_00: I'm sure there are shenanigans happening. So like, how do you raise the flag or how do you call that to the community's attention? Or is that our job?

SPEAKER_02: Well yeah, I built the tool and if I observe something I would raise a flag, I don't know, I would tweet about it, I would blog about it, I mean that

SPEAKER_01: works, right? Looking at the taproot activation, your mining pool observer picked up that some mining pools were not mining paid to taproot transactions, even though it was active at that point. Yeah, and yeah, that definitely got seen.

SPEAKER_00: Yeah.

SPEAKER_02: Right. Yeah.

SPEAKER_00: And that was some of it by accident, right? Correct. Yeah. That's awesome.

SPEAKER_02: Great. Yeah. Tell us that story. Yeah. So actually I was running like a live stream up on Taproot activation. Activation is always interesting. There might be stuff happening that we didn't foresee, but we should have. We hope that everything goes smooth, but sometimes stuff happens in the very night of Taproot activation, actually already warning for me, Taproot activated. And we saw a lot of people broadcasting their first Taproot spans into the mempool, including operator messages saying, I'm the first one to spend Taproot for example. And then the first block arrived, didn't include any Taproot spans. These Hi-fi mempool transactions not included. So we thought, okay, is there anything wrong with our code? Is there anything we didn't test? Then your second block arrived.

SPEAKER_00: Because you had done a... was it with the F2 pool? Who had you actually done like a trial with before it was active?

SPEAKER_02: Oh, yeah, right. Okay. So yeah, even before activation, actually, we did with F2 pool, we spent a few taproot outputs that were like low value that I did them to bring just to show and learn how that's done and show that the software activates actually, anyone can spend or are not yet unspendable.

SPEAKER_00: And so how do you like arrange something like that? You reach out to the various pools or just them and just say I want to try this?

SPEAKER_02: I reached out to two pools. One of them was F2 pool and they said, hey, let's go. Yeah. Okay, cool. Yeah. And going back to the earlier story in this very night of Teplur activation, actually, they like the second block arrived from F2 pool this time and didn't include any Teplur spends. Third block arrived, didn't include any Teplur spends. So by the time the fourth block arrived, all these Teplur spends were confirmed. And it later turned out that these pools, it upgraded in time, weren't fault signaling, but the issue was that their peers were old and they had some weird manual peer configuration, which then caused problems for them. Their peers couldn't really do this pay to Teplur spends because they are non-standard for them.

SPEAKER_00: OK, cool.

SPEAKER_01: So basically they were up to date and ready to go and actually correctly signaling, but just didn't see the type of transactions because their peers filtered them out and dropped them as non-standard. Correct.

SPEAKER_02: Yeah.

SPEAKER_00: Yeah. So what was remediation for that? You chat with them, you figure it out. Okay, yeah. Change their peers and then off and running.

SPEAKER_02: Yeah, they had some custom code and I think they dropped that. I think they now keep more closely to the Bitcoin core releases than before. Yeah. And then after a few weeks, our pool took a bit longer. We don't know exactly because the communication was a bit more difficult, but we know that they know my page attempt was spent just as all other pools are.

SPEAKER_00: Yeah Cool. And so, I mean, this is the service you provide to the community. And it's open source and you're being supported by Brink currently. And so how do you think about these kinds of projects? The monitoring piece, or we're going to talk about trace points next, but, you know, how do you think about the observability of the network and different things that are still missing?

SPEAKER_02: Correct. but... I think talking to people helps a lot, hearing about what they're interested in, what their motivations are, what their goals are, what they're looking for, what they're building, and then supporting them in a way that you provide them with data for either their proposals or for PRs to get merged and so on. In general, just going back and saying, okay, Bitcoin is still an experiment, we want to see if it succeeds or not, and we just somehow need to measure the levels of success. So, for example, Bitcoin might not succeed if there's censorship on the network, and we might want to know if there's censorship and say, okay, this isn't working.

SPEAKER_00: Are there other things that you've observed running the mining pool observer as to how pools operate, whether that's how they figure out what tracks transactions go into blocks or things like learning about the custom code in terms of their peer set and things like that, are there other things that have come to light?

SPEAKER_02: Yeah, of course, like the mining pool observer, it works by comparing a block that was recently mined to a block template that was recently queried from mynode. So obviously there are some differences between the mynode's mempool and the mining pool's mempool and we can exactly time when the mining pool actually queried his block template, but we can still compare the template, my template and the pool's block and figure out, for example, which transactions are shared. We hope that's the big part, but we can actually see transactions that are missing from the block that we think should be in the block, we can also see transactions that are extra to the block. So one transaction that's always extra is the coinbase. We don't have that in our block template. Some other times, we, for example, see the payouts and consolidation transactions from pools, which they sometimes include via a COFee payment. So they don't specify any PAs, they are not related on the network and we can detect them being included there. And of course, transaction accelerators, for example, via BTC runs a transaction accelerator, you pay an out of band fee and they include your low fee transaction really early on in their block. So you can see that, for example.

SPEAKER_01: So you would say that generally you see all the mining pools you're observing as using the same block building as Bitcoin core, but they sometimes prioritize transactions because of out of band or their own usage.

SPEAKER_02: Yes. Great. Yes. Yeah, I think they use the RPC, prioritized transaction.

SPEAKER_01: Yeah. So it's consistent with Bitcoin core being run by all of them.

SPEAKER_02: Yeah, I think so. And we don't see too much deviation from the proc template actually.

SPEAKER_00: Right. Well, that's maybe more fodder for why, Mark, you should be continuing to work on that project. Yeah, I know. Cool. So one of the other projects you've been working on is adding trace points to Bitcoin Core. Yeah. Tell me about it in the comments below, and I'll see you in the next video.

SPEAKER_01: I mean, that was interesting. Yeah.

SPEAKER_02: I'm done. Ha ha ha ha! Yeah. There are trace points, for example, in the kernel and you can detect when a certain part of the code is reached and you can extract some internal information from that and do debugging, for example, and so on. And I thought this would be really nice to have in Bitcoin Core as well. In December 2020, I sell PR to Bitcoin Core, adding every primitive support for that. And I picked that up at work and added the first trace points to Bitcoin Core that are reached in the networking layer. So, for example, each time we receive a message from a peer or we send the message to a peer, this trace point is reached. And we can hook into this trace point and extract, for example, which peer we send this message to, what this message contains and similar data and process this like in some other way. Some other process like a tracing script, do analysis there, can do debugging, can do education, for example, we can actually see the message being sent back and forth and infer the protocol there just to teach people about the protocol.

SPEAKER_00: Why are we adding trace points to certain parts? Why don't we just add it everywhere? And what are the trade-offs of having it in certain places versus having them just every line of code?

SPEAKER_02: versus having just every line of code. So the more trace points you have, the less readable your code gets, I say. And obviously when you actually don't use the trace points, you have like very minimal overhead. But if you hook into the trace point, then you have small overhead. Whilst you're running more code, you have more overhead there.

SPEAKER_01: So if you compile it with the trace points disabled, it's actually not a noticeable difference. Correct, yeah.

SPEAKER_02: Oh yeah. Correct. Yeah, there's a macro in there and it actually evaluates to to nothing. So if you don't enable during compile time, enable the trace points, you don't see anything there.

SPEAKER_01: But for us developers that want to know what's going on internally and get detailed information at various points We can turn on the trace points. It's a compiler flag and then just suddenly results to these Kernel events being yeah, actually and this time

SPEAKER_02: Yeah, actually. And this time in this time, it's not really the current event, we hook in over the kernel and put the Linux kernel into that. Yeah, but yeah. Okay. And one thing to note is that we currently in the latest release, the GUIX builds actually include the dependency and the release builds with trace points enabled. So somebody running a Bitcoin Core in production, for example, an exchange or another service, for example, or user even can actually use the trace points and debug their system if they need to.

SPEAKER_00: Yeah. So... And have people been doing that? Have you seen projects that have been used really taking advantage of these treatments?

SPEAKER_02: So one project I've heard about from someone is that they're using it for debugging or actually simulating the coin selection in Bitcoin Core's wallet. Maybe Mercy can talk about that.

SPEAKER_01: Hmm that. Andrew Chow and I have been using it very extensively in the past weeks. So Andy added face points in the coin selection to learn which algorithm was used to produce an input set out of the ones that were proposed, which one was preferred, whether we managed to avoid partial spending of a key and things like that. And we have a project with which we have been simulating different fee rate scenarios and basically benchmarking improvements that we're trying to make to the Bitcoin core wallet. And it's a means for us to convince ourselves and hopefully also our peers that the improvements we're making to the wallet are actually going to benefit the overall health of the network and make it cheaper for the users to use and more private.

SPEAKER_00: Yeah, I mean, I definitely see the value when you're developing something or you're checking something. I guess I'm questioning why it would end up in production at all. As in PDB is not supposed to make its way into like a production app. And so when you're making a call to provide a trace point and ship it for a release, what's the delineation between that being a good idea versus us just adding a trace point when we're doing a PR and then providing that data on the PR, why production versus when you're sort of using it in the debugging world.

SPEAKER_01: Yeah, I think we don't want to plaster the whole code base with them because they had a maintenance burden. And if you add them in points that aren't known to be useful, it would be a wasted effort. It makes review harder. There's more code there. Since they're compiled in, it might actually have a performance impact. I think adding them in at specific points where we already know that people are going to use it. For example, in coin selection, I can see also enterprise users wanting to have detailed information at that point. And I personally know three developers that are running with the coin selection hooks already and doing simulations and actively learning about how good of an idea their ideas for the Bitcoin core wallet are. There it's a clearer cut that it's an improvement that's worth the effort.

SPEAKER_02: Yeah. Good.

SPEAKER_00: you

SPEAKER_02: Also, one downside of the trace point is there's only trace points on Linux. We don't have them on windows. We don't have them on Mac OS, for example, and open BSD, for example, as well. And they just don't expect it because they don't run the Linux kernel and we can't use them for debugging or anything out there. So if there's some enterprise users running a Bitcoin core on windows for whatever reason. Yeah. For whatever reason, then they, then they can't debug it. But we might also want to make sure our windows builds are okay. Even if that's not the enterprise user.

SPEAKER_00: Then they then they kind of

SPEAKER_01: Maybe one comment for our power users listening and these trace points only evaluate locally. There's no telemetry in Core it's just you yourself on your own machine can hook into it I guess maybe that would be another concern though if you had other software running on your computer and There was abundant trace points everywhere by where could perhaps listen to what your Bitcoin core is doing. Oh, but I even think that

SPEAKER_00: Oh, but I even think that, I mean, I think it'd be better is to have a partner piece of software that gathers these trace points, organizes them, keeps a historical record over time, et cetera, et cetera. That could be quite valuable.

SPEAKER_02: Yeah, I'm actually working on my P2P network monitoring using TracePoints where we collect the data and we analyze the data for potential anomalies that may be someone to do a bug somewhere in master and we want to test it in before we have a release candidate, for example. So we can test multiple versions against each other, for example, or there's a development attack on the network which we can actually detect and learn from.

SPEAKER_00: And so you would imagine that multiple nodes in geographically distributed places would be running this software and then it'd be collected in a centralized place, or...

SPEAKER_02: Yeah. Yeah, my idea of the project, what I'm working on is just providing an interface that hooks into the trace point and provides that without users to listen to the data feed coming from Bitcoin Core without the hassle of working actually with the trace points. So making that really easy and providing interface for people where, for example, write a quick Python script and just run that Python script that filters out the bit of stuff for them. That's the goal. Good to see you.

SPEAKER_01: I could see enterprises being super interested in having a closer look at what their nodes are doing, how they're connected, and that sort of thing. And it enables people to donate their logs more easily, maybe. If we see fun stuff, like what we talked to Martin about, do you want to do it?

SPEAKER_00: Probably, yeah. Do you want to explain what that means?

SPEAKER_01: Yeah, I think that episode's not out yet, right? So we had Martin Zum Sande visit us and we talked to him a little bit about how changing the peer-to-peer behavior could change the emergent behavior of the network in the whole. And there were some interesting events in the peer-to-peer sphere a year ago or so where somebody started broadcasting vast amounts of made-up addresses and we dissected that story a little bit with Martin and looked a little bit at the peculiarities of the address relay, how sending small chunks would carry further than sending big buckets of them and things like that.

SPEAKER_02: Oh yeah.

SPEAKER_00: and I'll see you next time.

SPEAKER_02: Yeah, right. Actually, the address flooding that happened last summer actually was one of the motivations for that project. So one goal is actually to detect some of the address flooding or similar flooding or anything in that direction and have an alert. Because I think, at least from my perspective, I was not directly involved in that. But from my perspective, this was just a coincidence that we actually saw that happening on the network and might be valuable for us to know something like that happened.

SPEAKER_00: So... Yeah, it was, I think it was raised to G max's attention on that Bitcoin talk forum. Yeah. Which then got relayed to more active folks, but, um, without someone combing Bitcoin talk for it, it wouldn't necessarily. Yeah. And in the end, even the.

SPEAKER_02: Yeah. Yeah. Yeah. And in the end, even there was a paper about it. And so it definitely got attention, but I think it could have happened that nobody even reported it or the core development process, people involved in that never heard about it.

SPEAKER_01: Yeah, making peer-to-peer traffic more readable and more accessible to regular users would maybe enable more of that to come to attention.

SPEAKER_02: Yeah, and the different attacks on the PTP networks we do early on, one idea was maybe we can even detect somebody trying to eclipse us, and they keep opening connections and so on. Obviously, I think that's really hard challenge, and you probably have better defense by just having another out of bounds sort of your block headers. But this might be might be an interesting way of detecting attacks that we don't know about, or learning about attacks that are actually performed on the network we don't know even about yet.

SPEAKER_00: Yeah, I think sharing information from nodes that aren't necessarily connected is probably pretty important for the health of the network generally. And this is something that Ethan Heilman brought up when he spoke at the residency of just doing better health monitoring and it seems like that is still pretty infantile in terms of the kinds of things that we we still need.

SPEAKER_02: Yeah.

SPEAKER_01: Should we popularize something like finding a buddy whose node you connect to in general? You have a friend and just always connect or add that node.

SPEAKER_02: Maybe, or even if you run multiple nodes, maybe connect them, maybe, I don't know.

SPEAKER_01: Yeah. So I know that there's eight outbound peers. There's two blocks only peers that we use as anchors. And there's the feeler connection. And the added nodes are an addition, right? So if we popularized telling people, hey, you should find a buddy and connect to their node as an added node, it would just be an additional peer. And semi-trusted in the sense that you would expect them not to be in on an eclipse attack against you. Yeah.

SPEAKER_02: Yeah. Yeah. On the other hand, we have done, I think, a lot of work on mitigating eclipse attacks. Maybe there are other attacks we haven't invested so much in or that could be more relevant to focus on.

SPEAKER_01: Right, but either way, such an added node might be an interesting way of making the network more resilient.

SPEAKER_02: way, such an added note might be an entry.

SPEAKER_00: Thanks for watching! Yeah, what are the things you excited about what what else is on your mind and things that you're excited to work on things that you know obviously Software activation is on the tip of everyone tongue

SPEAKER_02: I think that's not really other, but using the trace points to review PRs has helped me a lot. Actually, for example, looking at some P2P changes and actually seeing the protocol change here a bit or it worked the same as before and so on. And that actually for me, personally, has helped because I'm not the guy that sits in front of the C++ code and reads it all day. I'm more the guy that looks at it visually, for example, or in some way, filter it, looks at what's happening and not what should happen.

SPEAKER_00: Let's take something like Erlay, so talk to me about how trace points might help with Erlay.

SPEAKER_02: Yeah, right. Right. So the goal of early is to reduce the bandwidth usage for transaction propagation. And one thing I did with the trace point is I ran in an early patch node from, from the PRR and I ran master node and compared those two and the bandwidth that we're using, they're connecting to the same peers and we could actually measure the bandwidth usage of both. And we saw the early node using far less, I think only 85% or so, or even less bandwidth for transaction relay than the, the master node. So that's really, and I think that was really helpful for Gleb or at least he communicated that, that he needs people to actually evaluate his changes and backtest his simulations, for example, in the, in the real world.

SPEAKER_01: So that's really interesting where the other peers that you were testing against also running the early patch. Yeah. Yeah. Okay.

SPEAKER_02: Yeah. Yeah. Okay. Yeah. So glad Brian, I think 12 early peers, I ran one master and then one early peer. And yeah, so, so

SPEAKER_01: Yeah, so, so your non early appear or your node that wasn't running early and the one that was running early, we're all connecting to early appears and it reduced the bandwidth use by 15% or so.

SPEAKER_02: Correct. Yeah, on some occasions even more. Yeah.

SPEAKER_00: Cool. Is there anything else we should cover? Not at the moment. Maybe next time. Cool. Thanks, Timo. It's good to have you back. Thanks for telling us about what you've been up to since we were last here.

SPEAKER_02: Not at the moment, maybe next time. Thanks for having me.

SPEAKER_00: All right, so another conversation in the books any takeaways from our conversation with Timo That was fun, short and sweet. Yeah, he's up to a lot of good things for the health of the ecosystem.

SPEAKER_01: Oh, I help with the Yeah, I need to make another shout out. One of my favorite websites, transactionfee.info where I quote a lot of charts from is also run by Timo.

