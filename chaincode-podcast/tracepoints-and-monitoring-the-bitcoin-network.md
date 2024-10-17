---
title: Tracepoints and monitoring the Bitcoin network
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://podcasters.spotify.com/pod/show/chaincode/episodes/0xB10C--Tracepoints-and-monitoring-the-Bitcoin-network-e1jipel
tags: []
speakers:
  - '0xB10C'
date: 2022-06-06
aliases:
  - /chaincode-labs/chaincode-podcast/tracepoints-and-monitoring-the-bitcoin-network/
---
Speaker 0: 00:00:00

Hey, Merch.
What up?
We are back in the studio.

Speaker 1: 00:00:02

Who are we talking to today?
We're talking to OXB10C.

Speaker 0: 00:00:06

I know him as Timo.
So we're going to call him Timo.

Speaker 1: 00:00:09

OK, fine.

Speaker 0: 00:00:12

It doesn't quite roll off the tongue.
Is there anything in particular that you're interested in learning from Timo today?

Speaker 1: 00:00:17

Yeah, I think we need to talk about Tether.
What he's doing with Tether and Bitcoin.

Speaker 0: 00:00:22

I'm not sure everybody's going to get that joke.

Speaker 1: 00:00:24

That's fine.

Speaker 0: 00:00:25

That's it?
You got to explain that?

Speaker 1: 00:00:29

All right, fine.
USDT is user space statically defined tracing.
Also rolls off the tongue.
Totally.
Also a short moniker for tether.
That's why.

Speaker 2: 00:00:42

Got it.

Speaker 0: 00:00:42

That's the term.
Well, we will talk to Timo about trace points.

Speaker 1: 00:00:45

Anything else?
Temperate activation and mining pool observation.

Speaker 0: 00:00:49

Yeah.
That's what I think.
He knows all that stuff.
Yeah.
All right.
Well looking forward to our conversation.
Hope you enjoy it, too.

## What he's been up to since the residency

Speaker 0: 00:01:05

Timo, welcome back to the Chaincode office.
You've been here before.
Correct, yes.
Yes.

Speaker 2: 00:01:13

Tell us last time.
Yeah, it has been three years now.

Speaker 0: 00:01:15

Nothing's happened since then.

Speaker 2: 00:01:16

No, nothing at all.

Speaker 0: 00:01:17

No, it's been the same.
Timo was in the 2019 residency, the last in-person residency that we ran.
And in this very room was heckling our various presenters about Bitcoin and Lightning.
And we did those two weeks of seminars.
So since then, what have you been up to?
What happened after that?

Speaker 2: 00:01:37

After that, actually, I joined a startup in Zurich, the Shift Crypto guys.
We worked on Plug and Play Bitcoin node.
And I later moved on to Coinmetrics, did some mempool monitoring there, did some mining pool monitoring there, for example, which blocks mining pools mine on and so on, connecting to these certain pools and seeing what they're giving out to the miners.

Speaker 0: 00:02:00

And so was that closed source?
Was that open source?
Cause you clearly sort of gone into the...

Speaker 2: 00:02:05

That's industry work.
That's closed source.
There are products using that behind the scenes.

Speaker 0: 00:02:09

Got it.
Okay.
And so since then you've been in the monitoring world.
Great.

Speaker 2: 00:02:14

Yeah.
I'm really interested in what is happening on the Bitcoin network and what people are doing there and what they are not doing.

Speaker 0: 00:02:22

So tell us, what's the motivation to do that?
Why did you gravitate towards those kinds of projects?

Speaker 2: 00:02:28

So Bitcoin is an open system.
You can do and you cannot do anything you like in the realms of, for example, policy or consensus.
So it's really interesting to see how people behave in such an open system.
And we often can gather insights and feed them back into development and improve things and make things easier or align incentives better in some way or another.

## Monitoring the mempool

Speaker 0: 00:02:53

Cool.
So the first project that I recall you were doing, the Mempool Observer.

Speaker 2: 00:02:57

Correct.
Yeah.

Speaker 0: 00:02:58

So tell me about that project and then what did that morph into?

Speaker 2: 00:03:01

So really early on, when I got started working on open source projects for Bitcoin, this was one of my first projects just mimicking Jochen Hoeneke's Mempool queue site, just because I wanted to try it out myself.
And I'm seeing where I got there.
Then did another version of that in 2019, actually during the residency here, added a more like a live transaction monitor to that.
So we actually plot the transactions by time they entered by mempool and their fee rate they paid.
And from that we actually can see some patterns.
We can see people following fee rates or the estimates of the fee rates.
We can actually see people doing consolidations, doing best payments, doing RBF and so on.
That's really interesting to observe and learn from and see the patterns emerging there.

Speaker 1: 00:03:51

One pattern that I really enjoyed looking at was multi-sig.
You could split out the specific types of multi-sig and fee rate estimations as an overlay.
And it was fairly easy to discover some of the market participants that way.
Correct.

Speaker 2: 00:04:05

Yeah.
Actually, I did a whole series of blog posts on that.
Based on the data I observed there, for example, observing the blockchain.com wallet, you can closely follow their fee rate estimates and actually see the people using these wallets.
So back at the time, they claimed to have one third of the market share in transactions.
And I think that's true based on the data I've observed.

## Monitoring Mining pools

Speaker 0: 00:04:27

So as you do these monitoring projects, and you did, you started with mempool, but that morphed into mining pool as well.
So why mining pool?
Why is that an interesting difference?

Speaker 2: 00:04:37

One key property of Bitcoin is this interstitial resistance.
And we were fine as long as one mining pool says, okay, I don't mine one transaction.
I don't allow this transaction to be included in my block.
We're fine.
But once we see multiple pools doing that, or all pools doing that, blocking or filtering certain transactions, then this property of Bitcoin doesn't hold anymore.
And I think that's really important for us to know if that happens and maybe to react to that if we can, if we even can.

Speaker 0: 00:05:06

I'm sure there are shenanigans happening.
So like, how do you raise the flag or how do you call that to the community's attention?
Or is that our job?

Speaker 2: 00:05:15

Well, yeah, I like I built the tool and if I observe something I would raise a flag.
I don't know, I would tweet about it, I would blog about it.

## Mining pools not mining P2TR at Taproot activation

Speaker 1: 00:05:23

I mean that works, right?
Looking at the taproot activation, your mining pool observer picked up that some mining pools were not mining paid to Taproot transactions, even though it was active at that point.
Yeah.
And yeah, that definitely got seen.

Speaker 0: 00:05:38

And that was some of it by accident, right?

Speaker 2: 00:05:40

Correct.
Yeah.

Speaker 0: 00:05:42

Tell us that story.

Speaker 2: 00:05:43

Yeah.
So actually I was running like a live stream up on Taproot activation.
Activation is always interesting.
There might be stuff happening that we didn't foresee, but we should have.
We hope that everything goes smooth, but sometimes stuff happens.
In the very night of Taproot activation, actually early morning for me, Taproot activated and we saw a lot of people broadcasting their first Taproot spends into the mempool, including up-to-time messengers saying I'm the first one to spend Taproot, for example.
Then the first block arrived, didn't include any Taproot spend.
These high-fee mempool transactions not included.
So we started, okay, is there anything wrong with our code?
Is there anything we didn't test?
Then the second block arrived.

Speaker 0: 00:06:24

Because you had done a, was it with the F2 pool?
Who had you actually done like a trial with before it was activated?

Speaker 2: 00:06:30

Oh yeah, right, Okay, so yeah, even before activation actually, we did with F2Pool, we spent a few taproot outputs that were like low value, related them to bring just to show and learn how that's done and show that the software activates actually anyone can spend or are not yet unspendable.

Speaker 0: 00:06:48

And so how do you like arrange something like that?
You reach out to the various pools or just them and just say, I want to try this.

Speaker 2: 00:06:54

I reached out to two pools.
One of them was F2 pool and they said, hey, let's go.
Yeah.

Speaker 0: 00:06:58

Okay, cool.

Speaker 2: 00:06:58

Yeah.
And going back to the earlier story In this very night of taproot activation actually, the second block arrived from f2 pool this time and didn't include any taproot spans.
Third block arrived, didn't include any taproot spans.
So by the time the fourth block arrived, all these taproot spans were confirmed.
And it later turned out that these pools had upgraded in time, burned for signaling, but the issue was that their peers were old and they had some weird manual peer configuration, which then caused problems for them.
Their peers couldn't relay these pay-to-type-root spans because they are non-standard for them.

Speaker 1: 00:07:34

So basically they were up to date and ready to go and actually correctly signaling, but just didn't see the Taproot transactions because their peers filtered them out and dropped them as nonstandard.
Correct.

Speaker 2: 00:07:45

Yeah.

Speaker 0: 00:07:46

So what was remediation for that?
You chat with them, you figure it out.
They change their peers and then off and running?

Speaker 2: 00:07:53

Yeah, they had some custom code and I think they dropped that.
I think they now keep more closely to the Bitcoin core releases than before.
And then after a few weeks, the AMP pool took a bit longer.
We don't know exactly because the communication was a bit more difficult, but we know, they know my page attack would span just as all other pools are.

Speaker 0: 00:08:13

Cool.
And so, I mean, this is the service that you provide to the community.
Correct.
It's open source and you're being supported by Brink currently.

## Why monitor the network?

Speaker 0: 00:08:20

Yes.
And so how do you think about these kinds of projects?
The monitoring piece or we're going to talk about trace points next, but how do you think about the observability of the network and different things that are still missing.

Speaker 2: 00:08:33

I think talking to people helps a lot.
Hearing about what they're interested in, what their motivations are, what their goals are, what they're looking for, and what they're building, and then supporting them in a way that you provide them with data for either their proposals or for PRs to get merged and so on.
In general, just going back and saying, okay, Bitcoin is still an experiment.
We want to see if it succeeds or not, and we just somehow need to measure the levels of success.
So, for example, Bitcoin might not succeed if there's censorship on the network.
And you might want to know if there's censorship and say, okay, this isn't working.

Speaker 0: 00:09:09

Other, other things that you've observed running the mining pool observer as to how pools operate, whether that's how they figure out what tracks transactions go into blocks or things like learning about the custom code in terms of their peer set, things like that.
Are there other things that have come to light?

## Template discrepancies between pools and monitor

Speaker 2: 00:09:25

Yeah, of course, like the mining pool observer, it works by comparing a block that was recently mined to a block template that was recently created from my node.
So obviously there are some differences between the my nodes mempool and the mining pools mempool and we can't exactly time when the mining pool actually created his block template but we can still compare the template, my template and the pools block and figure out, for example, which transactions are shared.
We hope that's a big part, but we can actually see transactions that are missing from the block that we think should be in the block.
We can also see transactions that are extra to the block.
So one transaction that's always extra is the coinbase.
We don't have that in our block template.
Some other times we for example see the payouts and consideration transactions from pools which they sometimes include via a zero fee payment.
So they don't specify any fees, they are not related on the network and we can detect them being included there.
And of course transaction accelerators for example ERPTC runs a transaction accelerator, you pay an out-of-band fee and they include your low fee transaction really early on in their block and we can see that for example.

Speaker 1: 00:10:32

So you would say that generally you see all the mining pools you're observing as using the same block building as Bitcoin Core?
Yes.
But they sometimes prioritize transactions because of out of band or their own usage.

Speaker 2: 00:10:45

Yeah, I think they use the ERPC prioritized transaction.

Speaker 1: 00:10:49

So it's consistent with Bitcoin Core being run by all of them?

Speaker 2: 00:10:53

Yeah, I think so.
And we don't see too much deviation from the block template actually.
Right.

Speaker 0: 00:10:59

Well, that's Maybe more fodder for why, Mark, you should be continuing to work on that project.
Yeah, I know.

## User-space Statically Defined Tracing (USDT)

Speaker 0: 00:11:06

Cool.
One of the other projects you've been working on is adding trace points to Bitcoin Core.
Tell me about that.

Speaker 2: 00:11:13

In the Linux world, there are trace points, for example, in the kernel, and you can detect when a certain part of the code's reached and you can extract some internal information from that and do debugging, for example, and so on.
And I thought this would be really nice to have in BitConcord as well.
In December 2020, I sell PR to BitConcord, adding very primitive support for that.
And I picked that up, that work, and added the first trace points that 2BitConcord that are reached in the networking layer.
So for example, each time we receive a message from a peer or we send a message to a peer.
This trace point is reached.
And we can hook into this trace point and extract, for example, which peer we sent this message to, what this message contains, and similar data, and process this in some other way, some other process, like a tracing script, do analysis there, can do debugging, can do education, for example.
We can actually see the message being sent back and forth and infer the protocol there.
Just like to teach people about the protocol.

Speaker 0: 00:12:13

Why are we adding trace points to certain parts?
Why don't we just add it everywhere?
And what are the trade-offs of having it in certain places versus having them just every line of code?

Speaker 2: 00:12:21

So the more trace points you have, the less readable your code gets, I say.
And obviously, when you actually don't use the trace points, you have like very minimal overhead.
But if you hook into the trace point then you have a small overhead because you're running more code you have more overhead there.

Speaker 1: 00:12:37

So if you compile it with the trace points disabled oh yeah it's actually not a noticeable difference.

Speaker 2: 00:12:43

Correct yeah there's a macro in there and it actually evaluates to nothing.
So if you don't enable, during compile time, enable the trace points, you don't see anything there.

Speaker 1: 00:12:53

But for us developers that want to know what's going on internally and get detailed information at various points, We can turn on the trace points, it's a compiler flag, and then this suddenly results to these kernel events being...

Speaker 2: 00:13:09

Yeah, actually, in this time it's not really the kernel events.
We hook in over the kernel and put the Linux kernel into that.
And one thing to note is that currently in the latest release, the GUIX builds actually include the dependency and the release builds with TracePoints enabled.
Somebody running Bitcoin Core in production, for example, an exchange or another service, for example, or a user even can actually use the trace points and debug their system if they need to.

## Using tracepoints to simulate coin selection

Speaker 0: 00:13:37

And have people been doing that?
Have you seen projects that have been used really taking advantage of these trace points?

Speaker 2: 00:13:42

So one project I've heard about from someone is that they are using it for debugging or actually simulating the coin selection in Bitcoin Cross Wallet.
Maybe Merchant can talk about that.

Speaker 1: 00:13:54

Andrew Chow and I have been using it very extensively in the past week.
So Andy added face points in the coin selection to learn which algorithm was used to produce an input set out of the ones that were proposed, which one was preferred, whether we managed to avoid partial spending of a key and things like that.
And we have a project with which we have been simulating different fee rate scenarios and basically benchmarking improvements that we're trying to make to the Bitcoin Core wallet.
And it's a means for us to convince ourselves and hopefully also our peers that the improvements we're making to the wallet are actually going to benefit the overall health of the network and make it cheaper for the users to use and more private.

## Why are tracepoints in production code?

Speaker 0: 00:14:39

Yeah, I mean, I definitely see the value when you're developing something or you're checking something.
I guess I'm questioning why it would end up in production at all.
As in, PDB is not supposed to make its way into a production app.
And so when you're making a call to provide a trace point and ship it for a release, what's the delineation between that being a good idea versus us just adding a trace point when we're doing a PR and then providing that data on the PR.
Why production versus when you're sort of using it in the debugging world?

Speaker 1: 00:15:11

Yeah I think we don't want to plaster the whole code base with them because they add a maintenance burden.
And if you add them in points that aren't known to be useful, it would be a wasted effort.
It makes review harder.
There's more code there.
Since they're compiled in, it might actually have a performance impact.
I think adding them in at specific points where we already know that people are going to use it.
For example, in coin selection I can see also enterprise users wanting to have detailed information at that point.
And I personally know three developers that are running with the coin selection hooks already and doing simulations and actively learning about how good of an idea their ideas for the Bitcoin Core wallet are.
There it's clear cut that it's an improvement, it's worth the effort.

Speaker 2: 00:16:01

Also one downside of the trace points is there's only trace points on Linux.
We don't have them on Windows.
We don't have them on Mac OS, for example, and OpenBSD, for example, as well.
They just don't exist because they don't run the Linux kernel and we can't use them for debugging or anything out there.
So if there's some enterprise users running Bitcoin Core on Windows for whatever reason.

Speaker 0: 00:16:22

Yeah, for whatever reason.

Speaker 2: 00:16:23

Yeah.
Then they can't debug it.
But we might also want to make sure our Windows builds are okay, even if that's not the enterprise user.

Speaker 1: 00:16:33

Maybe one comment for our power users listening, these trace points only evaluate locally, there's no telemetry in Bitcoin Core.
It's just you, yourself on your own machine can hook into it.
I guess maybe that would be another concern though, if you had other software running on your computer and there was abundant trace points everywhere, BiWare could perhaps listen to what your Bitcoin core is doing locally.

Speaker 0: 00:16:56

Oh, but I even think that'd be, I mean, I think it'd be better is to have a partner piece of software that gathers these trace points, organizes them, keeps a historical record over time, etc.

## Using tracepoints for P2P monitoring

Speaker 0: 00:17:04

Etc.
That could be quite valuable.

Speaker 2: 00:17:06

Yeah, I'm actually working on my P2P network monitoring using trace points where we collect the data and we analyze the data for potential anomalies.
And maybe someone to do a bug somewhere in master and we want to test it before we have a release candidate, for example.
So we can test multiple versions against the other, for example.
Or there's a developer attack on the network, which we can actually detect and learn from.

Speaker 0: 00:17:31

And so you'd imagine that multiple nodes in geographically distributed places would be running this software and then it'd be collected in a centralized place or.

Speaker 2: 00:17:40

Yeah.
Like my idea of the project, what I'm working on is just providing an interface that hooks into the trace point and provides that without users to listen to the data feed coming from BitConcord without the hassle of working actually with the trace points.
So making that really easy and providing interface for people where, for example, why did a quick Python script and just run that Python script that filters out the relevant stuff for them.
That's the goal, yeah.

Speaker 1: 00:18:02

Oh, I could see enterprises being super interested in having a closer look at what their nodes are doing, how they're connected and that sort of thing.
And it enables people to donate their logs more easily, maybe.
Probably, yeah.
If we see fun stuff, like what we talked to Martin about.
Yeah.

Speaker 0: 00:18:19

Do you want to explain what that means?

Speaker 1: 00:18:21

Yeah.
I think that episode's not out yet.
Right.
So we had Martin Zum Sande visit us and we talked to him a little bit about how changing the peer to peer behavior could change the emergent behavior of the network in the whole.
And there were some interesting events in the peer to peer sphere a year ago or so, where somebody started broadcasting vast amounts of made up addresses.

Speaker 2: 00:18:45

Oh, yeah.

Speaker 1: 00:18:45

And we dissected that story a little bit with Martin and looked a little bit at the peculiarities of the address relay, how sending small chunks would carry further than sending big buckets of them and things like that.

Speaker 2: 00:19:00

Yeah, right.
Actually, the address flooding that happened last summer actually was one of the motivations for that project.
So one goal is actually to take some of the address flooding or similar flooding or anything in that direction and have an alert because I think, at least from my perspective, I was not directly involved in that.
But from my perspective, this was just a coincidence that we actually saw that happening on the network and might be valuable for us to know something like that.

Speaker 0: 00:19:28

Yeah, it was, I think It was raised to GMAX's attention on a BitcoinTalk forum, which then got relayed to more active folks.
But without someone combing BitcoinTalk forum, it wouldn't necessarily...

Speaker 2: 00:19:43

In the end, there was a paper about it, and so it definitely got attention.
But I think it could have happened that nobody reported it or the core development process, people involved in that never heard about it.

Speaker 1: 00:19:55

Yeah.
Making peer-to-peer traffic more readable and more accessible to regular users would maybe enable more of that to come to attention.

Speaker 2: 00:20:04

Yeah, and there are different attacks on the PTP networks.
We do early on, one idea was maybe we can even detect somebody trying to eclipse us and they keep opening connections and so on.
Obviously, I think that's a really hard challenge and you probably have better defense by just having another out of bounds source of your block headers.
But this might be, might be an interesting way of detecting attacks that we don't know about or learning about attacks that are actually performed on Inverk.
We don't know even about yet.

Speaker 0: 00:20:35

Yeah, I think sharing information from nodes that aren't necessarily connected is probably pretty important for the health of the network generally and this is something that Ethan Heilman brought up when he spoke at the residency of just doing better health monitoring.
And it seems like that is still pretty infantile in terms of the kinds of things that we still need.

Speaker 1: 00:20:55

Should we popularize something like finding a buddy whose node you connect to?
In general, you have a friend and just always connect or add that node.

Speaker 2: 00:21:07

Maybe, or even if you run multiple nodes, maybe connect them, maybe, I don't know.

Speaker 1: 00:21:11

Yeah, so I know that there's eight outbound peers, there's two blocks only peers that we use as anchors, and there's the feeler connection.
And the added nodes are in addition, right?
Yeah.
So yeah, if we popularized telling people, hey, you should find a buddy and connect to their node as an added node, it would just be an additional peer and semi-trusted in the sense that, that you would expect them not to be in on an Eclipse attack against you.

Speaker 2: 00:21:42

Yeah.
On the other hand, we have done, I think a lot of work on mitigating Eclipse attacks.
Maybe there are other attacks we haven't invested so much in, or that could be more relevant to focus on.

Speaker 1: 00:21:53

Right.
Right.
But either way, it's such an added note, might be an interesting way of making the network more resilient.

Speaker 0: 00:21:59

Yeah.

## Using tracepoints to review PRs

Speaker 0: 00:21:59

What are the things you excited about?
What else is on your mind and things that you're excited to work on?
Things that, you know, obviously software activation is on the tip of everyone's tongue.

Speaker 2: 00:22:09

I think that's not really other, but using the trace points to review PRs has helped me a lot.
Actually, for example, looking at some P2P changes and actually seeing the protocol change here a bit, or it works the same as before and so on.
And that actually for me personally has helped because I'm not the guy that sits in front of the C++ code and reads it all day.
I'm more the guy that looks at it visually, for example, or in some way, filter it, looks at what's happening and not what should happen.

## Benchmarking Erlay with USDT

Speaker 0: 00:22:42

Let's take something like Erlay.

Speaker 2: 00:22:45

Yeah, right.

Speaker 0: 00:22:45

So talk to me about how TracePoints might help with Erlay.

Speaker 2: 00:22:49

Right, so the goal of Erlay is to reduce the bandwidth usage for transaction propagation.
And one thing I did with the TracePoints is I ran an Erlay patch node from the PR and I ran master node and compared those two and the bandwidths that we're using, they're connecting to the same peers and we could actually measure the bandwidth usage of both.
We saw the early node using far less, I think only 85% or so, or even less bandwidth for transaction relay than the master node.
So that's really, and I think that was really helpful for Gleb or at least he communicated that he needs people to actually evaluate his changes and backtest his simulations, for example, in the real world.

Speaker 1: 00:23:34

So that's really interesting.
Were the other peers that you were testing against also running the early patch?

Speaker 2: 00:23:40

Yeah.
Yeah.
Okay.
Yeah.
So Gleb ran, I think, 12 early peers.
I ran one master and then one early peer.

Speaker 1: 00:23:49

And yeah.
So your non-early peer or your node that wasn't running early and the one that was running early were all connecting to early peers.
Correct, yeah.
And it reduced the bandwidth use by 15% or so.

Speaker 2: 00:24:01

Yeah, and some occasions even more, yeah.

Speaker 0: 00:24:04

Cool.
Is there anything else we should cover?

Speaker 2: 00:24:06

Not at the moment.
OK.
Maybe next time.

Speaker 0: 00:24:08

Cool.
Thanks, Timo.
It's good to have you back.
Thanks for telling us about what you've been up to since you were last here.

Speaker 2: 00:24:13

Thanks for having me.

Speaker 0: 00:24:21

All right.
So another conversation in the books.
Any takeaways from our conversation with Timo?

Speaker 1: 00:24:27

That was fun, short and sweet.

Speaker 0: 00:24:30

He's up to a lot of good things for the health of the ecosystem.

Speaker 1: 00:24:33

Yeah, I need to make another shout out.
One of my favorite websites, transactionfee.info, where I quote a lot of charts from, is also run by Timo.

Speaker 0: 00:24:42

Well, you can pay him off with a lot of likes.
I already bought him breakfast.
Seems like a fair trade.
All right, well thank you for joining us and we will have hopefully another episode out shortly.
Thanks.

Speaker 2: 00:25:04

Have fun here.
