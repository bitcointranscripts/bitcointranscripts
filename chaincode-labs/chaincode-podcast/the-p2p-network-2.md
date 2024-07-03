---
title: "The P2P network"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
source_file: https://anchor.fm/s/12fe0620/podcast/play/42369447/https%3A%2F%2Fd3ctxlq1ktw2nl.cloudfront.net%2Fstaging%2F2021-9-26%2Fe2b8de66-96bb-0262-100b-c307e04bbfc5.mp3
media: https://podcasters.spotify.com/pod/show/chaincode/episodes/Pieter-Wuille--Amiti-Uttarwar-and-the-P2P-network---Episode-16-e19bgv7
tags: ['erlay', 'p2p']
speakers: ['Pieter Wuille', 'Amiti Uttarwar']
categories: ['podcast']
summary: "P2P experts Pieter and Amiti chat about the P2P network."
episode: 16
date: 2021-10-26
additional_resources:
-   title: FIBRE Episode with Matt Corallo
    url: https://podcast.chaincode.com/2020/03/12/matt-corallo-6.html
-   title: 'PR #787'
    url: https://github.com/bitcoin/bitcoin/pull/787
-   title: Eclipse Attack paper
    url: https://eprint.iacr.org/2015/263.pdf
-   title: Sybil attack
    url: https://en.wikipedia.org/wiki/Sybil_attack
-   title: Addrman and eclipse attacks wiki page
    url: https://github.com/bitcoin-core/bitcoin-devwiki/wiki/Addrman-and-eclipse-attacks
-   title: 'Anchors connections - PR #17428'
    url: https://github.com/bitcoin/bitcoin/pull/17428
-   title: Connection exhaustion issue
    url: https://github.com/bitcoin-core/bitcoin-devwiki/wiki/Addrman-and-eclipse-attacks#open-questions-and-areas-for-research
-   title: paper
    url: https://arxiv.org/abs/1905.10518
-   title: BIP
    url: https://github.com/naumenkogs/bips/blob/bip_0330_updates/bip-0330.mediawiki
-   title: 'Limiting addr black holes - PR #21528'
    url: https://github.com/bitcoin/bitcoin/pull/21528
-   title: Rate limiting on address gossip in 22.0
    url: https://github.com/bitcoin/bitcoin/pull/22387
-   title: Leaky bucket rate limiter
    url: https://en.wikipedia.org/wiki/Leaky_bucket
-   title: Estimating the Node Degree of Public Peers and Detecting Sybil Peers Based
        on Address Messages in the Bitcoin P2P Network
    url: https://arxiv.org/abs/2108.00815
-   title: Coinscope paper
    url: https://www.cs.umd.edu/projects/coinscope/coinscope.pdf
-   title: TxProbe
    url: https://arxiv.org/abs/1812.00942
-   title: ASMAP
    url: https://blog.bitmex.com/call-to-action-testing-and-improving-asmap/
---
Speaker 0: 00:00:05

Hi everyone.
Welcome to the Chaincode Podcast.
This is Kira Leigh.
And it's been a while.
Hi Jonas.

Speaker 1: 00:00:10

Hey Kira Leigh.
Welcome back.

Speaker 0: 00:00:11

Thank you.
It's nice to be here.
Tell me more about this episode we've got.

Speaker 1: 00:00:16

This episode was designed for two P2P experts, Amiti and Peter, to sit down and talk about all things P2P.

Speaker 0: 00:00:24

That sounds very exciting.

Speaker 1: 00:00:25

It was very exciting.
I was supposed to be a fly on the wall, but then I asked a lot of questions and so.

Speaker 0: 00:00:30

Yeah, fly on the wall is not your strong suit.

Speaker 1: 00:00:32

It is not.
I enjoyed it quite a bit.
I was happy to be here, and I think you'll enjoy listening to it.

Speaker 0: 00:00:37

Well, great.
Looking forward to it.

Speaker 1: 00:00:44

So, Peter, This is your first episode as actually part of the Chaincode team.
So welcome to Chaincode.
It's been a while in the making.

Speaker 2: 00:00:52

Yeah, thanks.
It's great to finally actually be here.

Speaker 1: 00:00:57

I agree.
So luckily we still have Amini in the office.
Maybe we can start where we left off our episode with you, Amini.
And for those that are just joining us and haven't listened to that episode, you should go listen to it.
But let's start with Adderman and AdderRelay, take it from there.

Speaker 3: 00:01:13

Edith Harper-Potter Cool.

## AddrRelay high-level goals and constraints

Speaker 3: 00:01:14

I talked a little bit about AdderRelay as a concept and how IP addresses are important for nodes to learn about.
Peter, do you have any initial thoughts of what are the high-level goals and constraints of address relay?

Speaker 2: 00:01:32

Yeah, that's a hard and I guess good question.
I think address relay is a really not well-defined problem because we're still figuring out what its exact goals should be.
It's not like transactions or blocks where we have this fairly strict requirement that every node eventually learns about all of them.
So clearly there's some desire for IP addresses to propagate well on the network for some metric of well but maybe that doesn't need to be everyone needs to hear about everything all the time because that's clearly an unscalable problem if the number of nodes goes up and they all broadcast their existence on the network at a fixed frequency eventually all the bandwidth will be eaten up by such messages so that's a difficulty but but at the same time as I said it's maybe not a strict requirement that everyone hears about everything so ultimately the reason why IP addresses are rumored is to have a network that's connected that's resistant to partitioning that is partitioning being the unintentional splitting of the network and I guess eclipse attacks being the term for when it's an attacker driven attempt to break someone's connectivity with the network, like both of those, but just in general, it's both a hard problem and a not very well defined goal.

Speaker 3: 00:03:14

Yeah, definitely agree with that.
I think even the premise of whether or not addresses should be able to propagate to all nodes on the network is something that established P2P contributors don't agree on.

Speaker 2: 00:03:31

Yeah and you have to see it in context.
Maybe at the current size of network and activity of nodes, that's a reasonable thing to do, but it wouldn't be if the network grows a hundred times in size.
So maybe the goal can be up to a certain level of activity that's reached, but after that maybe not anymore.

Speaker 3: 00:03:53

To play devil's advocate a little bit, don't we expect all transactions and blocks to be propagated to all nodes on the network regardless of how it scales?

Speaker 2: 00:04:03

This is definitely true for blocks.
Like if a node cannot hear about a block, it is dysfunctional.
Fortunately for blocks, it is easy.
Blocks are incredibly expensive to create, so there is no spam problem for blocks and for transactions we have something similar it's a bit more complicated and fuzzy but at least in Bitcoin Core the mempool policy has this this notion of called marginal fee rate which is like the minimum fee rate we expect transactions to pay and the reasoning is really that whenever we relay a transaction on the network its cost is accounted for somewhere.

## Marginal fee rate

Speaker 2: 00:04:49

So either we assume it will eventually confirm and pay for itself, or it is maybe evicting some other transaction and it is paying for that evicted transaction in addition to its own.
So with that kind of reasoning you essentially set a cost in terms of Bitcoin value on the propagation for a transaction across the network.
But something like this is not possible for IP addresses.
At the same time, there's no way of what is a valid IP address.
I can rumor anything.
And is validity, is it valid when you can connect to it?
Is it valid when it is an honest node?
There's no such...

Speaker 3: 00:05:38

Even if you can connect to it once, doesn't mean it will stay online.

## Should we consider different transport layers?

Speaker 1: 00:05:42

Should there be different transport layers for these different messages that are being sent around.
Obviously, going back to Hamidi's design goals, the reliability, the timeliness, the privacy, these are different levers that could be pulled for these different messages that could be passed around.

Speaker 2: 00:05:58

Cephas Storm This is, I think, an easier question if you're talking about blocks and transactions because for example like initial block download has completely, it's like purely bandwidth constraint, you don't even care about partition resistance like okay a node can't get up, fine it'll find some other solution in the worst case while like block relay at the tip, there the problem occurs, because now you want it fast, you want it reliable, you want it resistant to partition attacks and so forth.
But transactions, like the timeliness, isn't there to the same extent anymore.
But, say, due to the design of compact blocks, where, so this is a BIP 152, is a mechanism where when a block is announced, it is sent to supporting nodes only with short hashes for the transactions, and since it can be assumed that the receiver node will have most of those already, this is at least a giant bandwidth gain, but in many cases very significant latency gain too, because most blocks propagate on the network with no round trips at all.
The receiver has all of them.
But that critically relies on the receiver having those transactions in the first place.
So that puts some moderate timeliness constraints on transactions, too.

## FIBRE Episode with Matt Corallo

Speaker 1: 00:07:37

To harken back to some of Matt's thoughts on this, I mean, obviously Fiber was this experiment of even changing to UDP and being able to take advantage of not having bandwidth constraints.
So separating those things out seems to make some sense.

Speaker 2: 00:07:54

I don't know if it really needs to be completely separate out, but we are somewhat going into that direction by having block-only connections now, and maybe more variety on those things will appear where some connections don't fulfill all of them because they're in conflict, right?
If you have like a high bandwidth transaction stream, it's not really a problem these days, but maybe for super low connectivity things like the bandwidth of the transaction is in conflict with the timeliness of blocks and maybe this is easier to solve with separate connections.
I think it's just good to think about these things as having very different goals.
And to get back to address relay, their timeliness is not a concern at all.
And even reliability is probably fine if an IP address just gets to 99% of nodes rather than 100.
Edith Wosseth, PhD.

Speaker 3: 00:08:53

Yeah, that makes sense.

## The introduction of Addrman in 2012, PR #787

Speaker 1: 00:08:55

Let's go back to 2012.
Adderman v1 was when you introduced it in PR 787, if you're keeping track at home.
And so maybe before we start getting into the design of Adderman and what that was like, I actually don't really understand what there was before Adderman.
There was this adder.dat file, but like, can you explain what it actually was doing?

Speaker 2: 00:09:20

So it was just a set of addresses and it basically stored all IP addresses that we received from other nodes.
There were some tests on it, but it had lots of problems.
Like, it was unbounded as far as I can tell.
I'd need to check to make sure, but it was effectively trivial to just spam a node with IP addresses and both its memory usage and its disk usage would blow up.

Speaker 1: 00:09:49

And do you recall that being just a known problem that you were going after?

Speaker 2: 00:09:55

It was at the time, like DOS resistance was not a thing.
Like you can find multiple quotes by Satoshi where, where he says the software is not very DOS resistant.
It is a hard problem, right?
I really don't remember all the thinking and reasoning that led to Adderman.
Unfortunately, if you go look at what is available in terms of logs, times were different.
PR was open, someone said, I tested it, it works, and it was merged.

Speaker 1: 00:10:31

Seemed to be an upgrade though, and it held up pretty well.

Speaker 2: 00:10:35

Pretty well.
It was very ad hoc.
There was not much research that went into it.
There was no, it isn't that we went over, these are the design goals or whatever, it's just something like, yeah, there's a few that you can just derive by looking at the pull request at a time, like it's finite in size.
That is a big constraint and it's an obvious one because we just don't want things to grow unboundedly.
And from that, well, if it's finite in size, you need limits and you need like a replacement strategy.
So what Adderman did was make a distinction between IP addresses that we know work and addresses we have just heard about because they're pretty fundamentally different in terms of our confidence in them.
And You also want both in that there's this notion of like trust on first use, which is like your SSH client tells you or you're connecting to a server with this fingerprints, I haven't seen it before, and you say yep that's a good thing and it doesn't tell you again.
So you don't want to always make completely random connections because under the assumption that not every IP address is an attacker, if you constantly hop, your probability of eventually hitting an attacker is virtually 100% and not doing that gives you...
You may still be connecting to an attacker but in that case you have a problem anyway So you want some connections to be drawn from the set of peers And I really don't like to say trust because the level of trust we place in these is extremely low But that there has to be some assumption of not every node in the network is an attacker.
If it were, you know, we have a problem.
So we can just reasonably assume that that's not the case, and if that's not the case, well, you probably want to use the connections you've used before.

Speaker 1: 00:12:47

Right, some combination of having some memory and then also adding diversity.

Speaker 2: 00:12:53

Right, because you want a network to learn, you want, if a new node joins, it over time should get connections so the network should learn and I think this is where it is balanced from like completely separating tried and new entries and dealing with them separately comes from and then within each has this idea of bucketing them based on where the information comes from and the idea is there that a single source, where a source would be defined as like even not just a single IP address but a range of IP addresses that are presumably geographically or administratively close to each other, only have access to a certain part of the database.
Every source IP range is mapped to a subset of the table and the things it rumors can only enter those places in the table.
The idea is there will be we need this replacement strategy and how do you prevent a spammer like a malicious spammer who is trying to poison your database?
How do you prevent, or to the extent possible, minimize its impact?
That's where that came from.
And all the rest I think is just made up some numbers.
What's a reasonable memory usage?
How many table entries should there be?
There's this magical constant of never revealing more than 23% of the table, I have no idea where it comes from.

Speaker 3: 00:14:30

So just some context for listeners, this is by and large still the fundamental tools that we currently use to store addresses in Bitcoin Core right now.
And so far it seems to be holding up really well.

Speaker 2: 00:14:46

It's evolved a bit over time, right?

## Eclipse Attack paper

Speaker 2: 00:14:49

So in 2015 there was a paper published by Ethan Heilman and others on eclipse attacks, which I think was the first sort of academic look at this kind of problem because I think before that we had talked about it as a Sybil attack, this problem of having lots of bad peers but I think it was recognized that a Sybil attack is really something different, because I think the history there is that Sybil is the name of a character in a book.

Speaker 0: 00:15:27

Oh, interesting.

Speaker 2: 00:15:28

It's like multiple personality disorder story, and a Sybil attack is something that appears where you have a number of trusted peers and you trust them to be all distinct parties, but if there's someone who is really controlling multiple of these, they can do a confidence attack on you, where you think, oh, most of my peers think this, but it's really just one party.
And that is not really the problem, a problem in a Bitcoin setting, because fundamentally our hope is to have at least one connection to the honest network and it doesn't really matter how many bad ones we have as long as there is one honest one.
So really the problem is eclipsing not so much sibling.
So eclipsing is an attacker managing to make sure all your peers are malicious.

Speaker 1: 00:16:27

I mean, that's such a remarkable trait though.

Speaker 3: 00:16:29

It really is.

Speaker 1: 00:16:30

That everything could go wrong except for one and you're still okay.

Speaker 2: 00:16:34

Yeah, it's of course, this is only true for the blocks and transaction parts because presumably if an attacker manages to be most of your connections in terms of address, you know, this increases their ability to poison you which over time leads to eclipse attacks.
And so all these sorts of problems were analyzed in this paper and it gave, I think, like seven or eight mitigation strategies for how the situation could be improved.
And over time, all of them have been implemented, I think.
Or maybe there's...

Speaker 1: 00:17:16

Yeah, there's still a few outstanding or in progress.
But yeah, there's a few that are undeployed or partially deployed.

Speaker 3: 00:17:25

Okay.
The vast majority have been implemented.
And I think one of the...

Speaker 1: 00:17:29

It was done very quickly, too.

Speaker 3: 00:17:30

Oh yeah.

Speaker 1: 00:17:31

It seemed like your collaboration with Ethan went quite well because things, you know, before the paper came out there was a push and then over time things got fixed also pretty quickly.

Speaker 2: 00:17:44

Yeah, so I think there were two big ones that were done pretty much immediately after the paper came out.
One was making a table bigger, just increasing the number of buckets and the sizes of the buckets.
A couple of years had passed.
I guess we were fine with using a bit more memory.
And the other one was giving addresses deterministic placement in the buckets.
This reduced the ability of like repeatedly inserting, trying to insert the same thing in a bucket.
If it only has one place, it goes there or it doesn't.
And then after that there were a few more.
Some of them took several years.
One was like feeler connections and retest before evicts policy.

Speaker 1: 00:18:34

By the way, Peter's doing all this from memory.
I'm sitting in front of the answers and Peter's just doing it in perfect order.
It's impressive.

Speaker 3: 00:18:41

So I thought it was interesting, the idea of inbounds versus outbound peers and ensuring that just because you're connected to an inbound peer, if you mark them as, hey, this is a good Bitcoin connection, like I can use it again in the future, that allows attackers to abuse that to write themselves into the tried table.
That was one.

Speaker 2: 00:19:04

Oh yeah, right I had forgotten about that one that we even did that.
It seems so obvious in retrospect.
And then anchors,

Speaker 1: 00:19:11

which was the most maybe the most recent.

Speaker 3: 00:19:13

Oh yeah totally, because we used block relay only.
So anchors are connecting to nodes that you already know about when you start up versus selecting more randomly.

Speaker 1: 00:19:27

So a few others that he suggested, more outgoing connections, which I think, some of that because of the two outbound block relay only connections.

Speaker 2: 00:19:37

Block only connections have that, but at the same time those don't relay addresses, so they're not really participating there.

Speaker 1: 00:19:45

Maybe Erlay will help us move this.

Speaker 2: 00:19:46

Yeah, exactly.

## Connection exhaustion issue

Speaker 2: 00:19:48

The big issue with outbound connections is like somewhere early on in Bitcoin's history, I don't remember exactly, there was a time when the network ran out of connectable inbound slots.
Like every node has a finite number of connections on the inbound side it accepts, like just sum all of those up.
That is an upper bound on the number of connections that can be made.
And at the time, like Bitcoin didn't have any like NAT PMP or or mini-UPMP to automatically open firewalls.
Probably a vast majority of nodes were running behind home routers.
This explains the hesitancy that developers have had to increase the number of outbound connections.
In an attack scenario, it's an easy way to increase your partition resistance, is adding more connections.
But it's been years, and this hasn't been a problem for a long time, but it still I think drives decisions around number of connections.

## Erlay (paper, BIP)

Speaker 2: 00:20:55

And so that's where Erlay really comes in, because Erlay is ultimately a mechanism, without going into too much detail, for increasing the number of connections without increasing bandwidth.
With Erlay deployed, it would be more reasonable for people to increase the number of inbound connections a node can have, or even changing the default about that.
That in its turn might make it more reasonable to increase the number of outbound connections.

Speaker 1: 00:21:31

Given that that's obviously a strong intuition, how do you go about testing that?
Like how do you go about actually changing that default?

Speaker 2: 00:21:39

That's very hard.

Speaker 3: 00:21:40

Very carefully.

Speaker 2: 00:21:43

Like, doing it gradually is a possibility and like watching metrics, but it's hard because, you know, deploying software, especially something like Bitcoin Core, like takes a long time.
It has very intentionally no auto upgrade mechanism or something like that to, you know, avoid software maintainers from having too much power over pushing changes to the network.
And from that, so you can't just say, you know, one release increase it a bit and increase it a bit more.
Like it takes time, you know, given that we haven't seen a shortage in connections for a number of years, and we can reason pretty easily about things like bandwidth usage and CPU usage that more connections bring.
Those things you can just test in isolation.
So it's not an entirely uninformed decision.

Speaker 1: 00:22:43

It seems like just generally we can be more sophisticated than the way you described your 2012 design.
Which, by the way, again, has held up very well.
It's not a slight in any way.
It's just, I wonder whether simulated networks or just simulations in general would give us some more information?

Speaker 2: 00:23:05

So for Erlay specifically, Gleb has been doing lots of simulation work to reason about bandwidth usage and so on.

## AddrRelay

Speaker 3: 00:23:13

Cool, so can I pop us back to address relay and some more of that?
I think in version 22 there were two big changes to address relay.
One was one I introduced about reducing black holes.
Let's not talk about that, let's talk about the other one.
Okay,

Speaker 2: 00:23:33

happy to talk about that one too.

Speaker 3: 00:23:36

About rate limiting address gossip.
Can you tell us about what the mechanism is?

Speaker 2: 00:23:41

There was just an observation we had that The total amount of IP addresses rumored on the network today, like if you start a node and run it for a couple of weeks and just see how many addresses you see from various nodes, it is a really low number.
It's like one every couple of seconds.
I don't remember the exact number.
And then if you compare that with how much we would permit there to be relayed.
So this is the old mechanism I'm describing from earlier releases that had been used since time immemorial, was, I think there was a buffer of the set of addresses we want to relay to every peer.
And it was capped at a thousand.
And if more things would enter this buffer, it would randomly start overwriting things out of those thousands.
And there was a certain rate at which this buffer is flushed, like just every so often, I don't know, two minutes or something?
Was it 10 minutes?
Is it an hour?
There is a Poisson timer, or is it every 10 seconds?
I really don't know.

Speaker 1: 00:24:59

There's going to be some constant in there.

Speaker 2: 00:25:02

Like beep, this is where we insert, we look it up and we will insert it.
So every so often we check, hey, for every peer, what's in this set of addresses, we want a rumor and just send it out.
So this puts a natural rate limit on the outbound side of IP relay.
It is at most a thousand addresses every this many seconds on average.
And if you compare that number to the amount that was actually being used on the network, it was some enormous factor, like 100 more, or a factor 100 more or something.

Speaker 3: 00:25:46

Yeah, I think it was between like a hundred and thousand X.
Yeah, something like that.

Speaker 2: 00:25:52

And that's concerning because in a way this means that the presumably mostly honest activity on the network today is using far less than what the network would permit relaying and that is exploitable.
Someone can, it's not completely non-trivial, but if someone finds a way to get this buffer full enough, they could have their set of addresses propagated way, way better than others in the network.
And given the fact there effectively is already this funnel effect at the outbound side.
It seemed like a fairly easy solution was to apply that at the inbound side as well and just limit like at what rate we process incoming connections.
So made some statistics like looking at a bunch of nodes what kind of activity level do we see and pick a number based on that.

## Leaky bucket rate limiter

Speaker 2: 00:26:56

So this is a known technique in networking called the leaky buckets rate limiter and the idea is that you have a bucket with tokens and like say every X seconds a token is added to this bucket but the bucket can overflow it can never go about a thousand over a thousand say And whenever an address is processed it takes a bucket from a token from the bucket unless there is none.
What this gives you is is a mix between you know a relatively low sustained rate but at the same time also permitting occasional spikes that go way beyond it without really changing the long-term average because ultimately everything is limited by the rate at which these tokens are added to the buckets And this was necessary because the existing behavior on the network is very spiky due to the way these things are buffered and sent out every so often.
And obviously the big question with a design like this is exploitable.
Like can someone overload you?
And the answer is yes, I think.
This does indeed mean that someone spamming you is going to be able to indirectly reduce the propagation.
Because this is on the inbound side, this is one step removed, but if I'm going to spam you, Jonas, then honest IP address is being relayed by MIDI to you, like you'll try to send out both to someone else But together it's too much So my spam is effectively reducing her honest traffic The noise drowns out the signal.
Yes, but A, you do it on the inbound side, which is better than doing it at the outbound side because then it would be you directly already having it.
And at the same time, this problem already exists because there is already this rate limiting that is unintentional and not really designed as a rate limit, but the set of a thousand with random replacement strategy effectively allows the same thing already, just at a much higher threshold.

## Address Spam

Speaker 3: 00:29:18

On the topic of address spam, I think we saw some really interesting address spam when this PR was up.

Speaker 2: 00:29:25

Yeah, I don't know what happened there, but there was this report all of a sudden of lots of apparently random IP addresses being relayed on the network just a couple of days after this pull request came up.
So I guess it was in time.
As far as I know, it was not related in any way, or I mean, we don't know because I don't think anyone Figured out who exactly was doing it.

Speaker 3: 00:29:53

No one's stepped forward and so it's it was me.
Yeah So the behavior that was observed was there would be nodes that would spin up and connect to public peers and send packets of 500 adder messages with 10 addresses each and This 10 number is magical in Bitcoin Core because above that and you won't forward those addresses so that kind of gives the merging effect from different peers that you were mentioning before but then the nodes would just disconnect.
And there were a few properties of the addresses that were observed.
One was that the time associated with the message was perfectly placed, I think, nine minutes in the future.
So, because if it's too far in the future, we won't propagate addresses anymore.
And similarly, if it's too far in the past, so by putting it as far in the future as possible, that ensures that you have the largest window of time that nodes will continue trying to propagate these addresses.

Speaker 2: 00:31:02

Yeah.
And there was a paper written about this researcher called Matthias Quintmann wrote a paper on this behavior and formulated a theory about what it was doing, like pointing out this nine minute in the future aspect too and hypothesizing that this is to ensure the longest possible time these addresses propagate on the network and there was an attempt to map the network.

Speaker 1: 00:31:31

This is inferring topologies.
Yes exactly.

## Estimating the Node Degree of Public Peers and Detecting Sybil Peers Based on Address Messages in the Bitcoin P2P Network by Matthias Grundmann

Speaker 3: 00:31:34

I mean we don't know but that's One of the suspected biggest reasons that you would do it and essentially be able to say, how many peers is this public node connected to?

## Coinscope paper

Speaker 1: 00:31:46

Trying to count connectivity of nodes.
How is that different than the Coinscope paper?
Coinscope is the long-lived connections and using timestamps, inferring topology through how those are propagated because they're unique.

## TxProbe

Speaker 1: 00:32:00

You can connect to a peer from another angle and be able to reconcile that data to see whether they were propagated.

Speaker 2: 00:32:07

Yeah, there have been other techniques like TX probe where you send conflicting transactions and see how those propagate to infer who is connected to who?

Speaker 3: 00:32:17

Honestly, I think the amount of information you can get is kind of, it's getting harder.
So in this, I think the main thing you could extract was how many peers each of these public nodes are connected to.

Speaker 2: 00:32:29

It's not who.

Speaker 3: 00:32:30

Yeah, the previous ones were identifying techniques for who nodes are connected to.

Speaker 2: 00:32:36

Yeah.
In TX probe, you literally connect to two nodes and you want to know, are these connected to each other?

Speaker 1: 00:32:44

That makes sense.
Yeah.

Speaker 2: 00:32:45

So it's different aspects of like different projections of topology data you get out.
And I think we have to live with the fact that you can't make it completely impossible to prevent that information from being revealed.
And there are people whose opinion is that this information should just be public so it can be used...

Speaker 3: 00:33:10

The information of node topology?
Yeah.
Oh, interesting.

Speaker 2: 00:33:13

I think there have been papers that argued for, you know, making node topology public because that makes it, you know, available for research.

Speaker 3: 00:33:23

Oh, okay.
But wouldn't that also make the network easier to attack?
Yes.

Speaker 1: 00:33:28

You have to raise new defenses.

Speaker 2: 00:33:30

To be clear, what's a concern here is if topology is known, that helps a potential partitioning attacker figure out where to focus their efforts, right?
If you assume it is possible for this information, like if we think that all these techniques for inferring topology are sufficiently able to retrieve that, then maybe that is indeed the right decision to just make it not hard, but I don't think that's the case.
I think that there's always going to be some signal there, but there are lots of possibilities for improving.

Speaker 1: 00:34:11

Yeah, can't there be some like combination of sort of like how Lightning does it in terms of the public, your public connectivity and then your private connectivity.
The private connectivity at least gives you a little bit of, again, all you need is one honest, you just have one honest connection.
I can't really compare Lightning nodes because...
I don't want to compare it.
I'm saying the concept of having a public versus a private and the idea of there's different kinds of trust when you're talking about public versus private.
But you introduce a little bit of reputation when you're talking about public and private and maybe those are longer lasting connections And it's up to you as to who you're trusting.

Speaker 2: 00:34:50

The problem with any kind of reputation is that there has to be something at stake that you lose when you behave badly.
And in Lightning Nodes, nodes have an identity and have connections with money that is at stake.
And in Bitcoin nodes don't have an identity intentionally because we want to hide the topology.
But also there can't be an identity that, you know, you don't want something like a proof of stake before you can run a node.
So that makes it very hard to say what is an honest node.

Speaker 1: 00:35:30

I mean, I guess another way that is different and that is the ephemeral nature of these connections, and if you watch a node and see the disconnection and connection, and when I was a new user and seeing that that was happening often was a little surprising.
It's like, wait, I don't maintain these relationships any longer than is actually occurring, it felt counterintuitive.

Speaker 3: 00:35:53

Yeah, and in fact, we have mechanisms to very carefully have potential for rotation, Such as every so often, I think five or 10 minutes, we connect to an additional block relay only.
And if that node provides us a block that we didn't know about, then we will prioritize it and make it replace an old connection.

Speaker 2: 00:36:15

And yeah.

Speaker 3: 00:36:16

Yeah.
So in the logs that shows a bunch of disconnecting connecting right even if that might not actually change your long lasting peers or similarly we have one for when we haven't gotten a block in a long time that might be normal or you might be eclipsed so as this last ditch effort you make a full relay connection to an additional node and say a fabled ninth one which is also short-lived any closing thoughts before we I'm very glad we got to cover all of P2P.

Speaker 1: 00:36:52

All of it.
We now understand everything.

Speaker 3: 00:36:55

Every little detail.

Speaker 1: 00:36:58

It's complex, but you know, we have our best people working on it.
It'll be fine.

Speaker 2: 00:37:06

There's lots of work still to be done there.

Speaker 1: 00:37:09

If you had more time, Peter, what would you like to work on?
What's something that you would like to address?

## Separate network stack

Speaker 2: 00:37:14

For example, what we were talking about just before, like typology, one possibility is, for example, run a completely separate Adderman or even going further, like a completely separate network stack for every public IP you have, like say, you know, run on Tor simultaneously with IPv4 and IPv6, like just give them their own completely independent network stack.
That is not a complete solution because Like you're still not going to give them each their own mempool for resource reasons, probably.
So that's probably still some leakage between them, but things like that would, I think, help a lot.
It's just a one thought.
There are so many things.

Speaker 3: 00:38:01

That was actually what popped up in my mind, is top of wish list as well.
And I think we have so many different fingerprint attacks of identifying this node through different networks, which is actually also that paper on the address spam was hypothesizing that that was an additional piece of information you could get because each one of those addresses had kind of unique attributes to it.
So if you send it over an IPv4 address and then you see it on a IPv6 or you know what would be worse is on these privacy networks that you're trying to keep private for some reason.
So I think the fingerprint attacks are a whole class that are pretty hard to attack individually but if we're able to separate the components and just have different network managers for different networks, then it would really diminish the surface area of that potential.

## ASMAP

Speaker 2: 00:38:58

I think Another thing that would be nice to see more work on is S-MAP.
So since a couple of releases, Bitcoin Core has had functionality of loading a database of basically telling it which IP ranges are controlled by the same network operators, like ISPs and similar level things.
But this needs infrastructure, like where do you get that database?
What's, you know, the supply chain for providing users with that, which is as much a technical problem as it is logistical and trust question one.
So that's something I'd like to work on.

Speaker 1: 00:39:43

And you couldn't imagine that being hard-coded or distributed from the same way that the bootstrapping is done and the IP addresses?

Speaker 2: 00:39:52

Yeah, the problem with that is that it is transient.
This information changes constantly, but it is available.
You can find these databases from various sources, they gather them.
But the problem is it is constantly changing, so it's not like you can have a verification procedure about it where you do it as part of your deterministic build and people will repeat it and get the same thing out.
So that probably implies we need tools to say diff two databases and see that there's some value judgment there like hey there's suddenly this change here is this is this expected or not and So I think a lot about it is just giving transparency in what is it and the ability to change it.
But I would hope that a mechanism can be found with sufficient eyes that it can indeed be just shipped as part of the big concord distribution and at least you have a default.

Speaker 1: 00:40:53

Well, thank you both for Making such a glorious return to the to the studio.

Speaker 2: 00:40:58

Thank you.
Thanks for having us Well, that was great you're never gonna leave disappointed with a Peter around so that was fun Yeah, and a treat to have Amiti here as well.

Speaker 0: 00:41:09

What more could you really ask for when it comes to talking about P2P?

Speaker 1: 00:41:12

You can't.
You can't ask for anything more, Carly.

Speaker 0: 00:41:14

Well, glad we got that straightened out.
Thanks everyone for listening.

Speaker 1: 00:41:18

And hopefully we will be seeing you soon.

Speaker 0: 00:41:22

♪♪
