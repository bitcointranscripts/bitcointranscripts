---
title: Pieter Wuille & Amiti Uttarwar and the P2P network - Episode 16
transcript_by: Whisper AI & PyAnnote
categories: podcast
tag: ['AddrRelay high-level goals and constraints', 'Very different than the goals of blocks and transactions', 'Marginal fee rate', 'Should we consider different transport layers?', 'FIBRE Episode with Matt Corallo', 'The introduction of Addrman in 2012, PR #787', 'What existed before AddrMan and the evolution of DoS resistance.', 'Eclipse Attack paperSybil attack Addrman and eclipse attacks wiki page Anchors connections PR #17428', 'Connection exhaustion issue', 'Erlay (paper, BIP)', 'AddrRelay', 'Limiting addr black holes PR #21528', 'Rate limiting on address gossip in 22.0', 'Leaky bucket rate limiter', 'Address Spam', 'Estimating the Node Degree of Public Peers and Detecting Sybil Peers Based on Address Messages in the Bitcoin P2P Network by Matthias GrundmannCoinscope paperTxProbe', 'Separate network stack', 'Fingerprint attacks', 'ASMAP']
---

Chaincode Labs podcast: Pieter Wuille & Amiti Uttarwar and the P2P network - Episode 16

SPEAKER_02: Hi, everyone. Welcome to the ChainCode podcast. This is Kira Lee. And it's been a while. Hi, Jonas. Hey, Kira Lee. Welcome back. Thank you. It's nice to be here. Tell me more about this episode we've got.

SPEAKER_01: This episode was designed for two p2p experts Amiti and Peter to sit down and talk about all things p2p That sounds very exciting. It was very exciting I was supposed to be a fly on the wall, but then I asked a lot of questions and so

SPEAKER_02: That sounds very exciting. It was. Yeah, fly on the wall is not your strong suit. It is not.

SPEAKER_01: it is not. I enjoyed it quite a bit. I was happy to be here and I think you'll enjoy listening to it.

SPEAKER_02: Well, great. Looking forward to it.

SPEAKER_01: So Peter, this is your first episode as actually part of the Chaincode team, so welcome to Chaincode, it's been a while in the making. Yeah!

SPEAKER_00: Yeah, thanks. It's great to finally actually be here.

SPEAKER_01: I agree. So luckily we still have Amini in the office. Maybe we can sort of start where we left off our episode with you, Amini. And for those that are just joining us and haven't listened to that episode, you should go listen to it. But let's start with Adderman and Adder Relay. Let's take it from there.

SPEAKER_03: Cool. I talked a little bit about add a relay as a concept and how IP addresses are important for nodes to learn about. Peter, do you have any initial thoughts of what are the high-level goals and constraints of address relay? Yeah, that's a good question.

SPEAKER_00: That's a hard and I guess good question. I think address relay is a really not well-defined problem because we're still figuring out what its exact goals should be. It's not like transactions or blocks where we have this fairly strict requirement that every node eventually learns about all of them. So, clearly there's some desire for IP addresses to propagate well on the network for some metric of well. But maybe that doesn't need to be everyone needs to hear about everything all the time because that's clearly an unscalable problem. If the number of nodes goes up and they all broadcast their existence on the network at a fixed frequency eventually all the bandwidth will be eaten up by such messages. So that's a difficulty but at the same time as I said it's maybe not a strict requirement that everyone hears about everything. So ultimately the reason why IP addresses are rumored is to have a network that's connected, that's resistant to partitioning. That is partitioning being the unintentional splitting of the network and I guess eclipse attacks being the term for when it's an attacker driven attempt to break someone's connectivity with the network. Like both of those but just in general it's both a hard problem and a not very well defined goal.

SPEAKER_01: BREAK SOME-

SPEAKER_02: I'm gonna I win.

SPEAKER_03: with. Yeah, definitely agree with that. I think even the premise of whether or not addresses should be able to propagate to all nodes on the network is something that, you know, established P2P contributors don't agree on.

SPEAKER_00: Yeah, and you have to see it in context, like maybe at the current size of network and activity of nodes that's a reasonable thing to do, but it wouldn't be if the network grows a hundred times in size. So maybe the goal can be up to a certain level of activity that's reached, but after that maybe not anymore.

SPEAKER_03: To play devil's advocate a little bit, don't we expect all transactions and blocks to be propagated to all nodes on the network regardless of how it scales?

SPEAKER_00: Yes. This is definitely true for blocks. If a node cannot hear about a block, it is dysfunctional. Fortunately for blocks, it is easy. Blocks are incredibly expensive to create, so there is no spam problem for blocks. For transactions, we have something similar. It's a bit more complicated and fuzzy, but at least in Bitcoin Core, the mempool policy has this notion of marginal fee rate, which is the minimum fee rate we expect transactions to pay. And the reasoning is really that whenever we relay a transaction on the network, its cost is accounted for somewhere. So either we assume it will eventually confirm and pay for itself, or it is maybe evicting some other transaction and it is paying for that evicted transaction in addition to its own. So with that kind of reasoning, you essentially set a cost in terms of Bitcoin value on the propagation for a transaction across the network. But something like this is not possible for IP addresses. At the same time, there is no way of... What is a valid IP address? I can rumor anything. Is validity... Is it valid when you can connect to it? Is it valid when it is an honest node? Is it... Right.

SPEAKER_03: I'll see you next time.

SPEAKER_02: I know you can not

SPEAKER_01: here.

SPEAKER_02: Thanks for watching!

SPEAKER_03: Right. There's no such. Even if you can connect to it once, doesn't mean it will stay online, that's.

SPEAKER_01: Should there be different transport layers for these different messages that are being sent around? Obviously, going back to immediate design goals, like the reliability, the timeliness, the privacy, like these are different levers that could be pulled for these different messages that could be passed around.

SPEAKER_00: Maybe, this is I think an easier question if you're talking about blocks and transactions because for example, like initial block download has completely, it's like purely bandwidth constraint. You don't even care about partition resistance. Like, okay, a node can't get up, fine. It'll find some other solution in the worst case. While like block relay at the tip, there the problem occurs because now you want it fast. You want it reliable. You want it resistant to partition attacks and so forth. But transactions, like the timeliness isn't there to the same extent anymore. But say, due to the design of compact blocks where, so this is a BIP 152, is a mechanism where when a block is announced, it is sent to supporting nodes only with short hashes for the transactions. And since it can be assumed that the receiver node will have most of those already, this is at least a giant bandwidth gain. But in many cases, very significant latency gain too, because most blocks propagate on the network with like no round trips at all. Like the receiver has all of them. But that critically relies on the receiver having those transactions in the first place. So that puts some moderate timeliness constraints on transactions.

SPEAKER_01: too. To harken back to some of Matt's thoughts on this, I mean obviously Fiber was this experiment of even changing to UDP and being able to take advantage of not having bandwidth constraints. So separating those things out seems to make some...

SPEAKER_00: Yeah. Yeah. I don't know if it really needs to be completely set for that, but we are somewhat going into that direction by having block-only connections now and maybe more variety on those things will appear where some connections don't fulfill all of them because they're in conflict, right? If you have like a high bandwidth transaction stream, it's not really a problem these days, but maybe for super low connectivity things like the bandwidth of the transaction is in conflict with the timeliness of blocks and maybe this is easier to solve with separate connections. I think it's just good to think about these things as having very different goals and to get back to address-related. Their timeliness is not a concern at all and like even reliability is probably fine if an IP address just gets to 99% of notes rather than 100.

SPEAKER_03: Yeah, that makes sense.

SPEAKER_01: Let's go back to 2012 Adderman v1 was when you introduced it in PR 787 if you're keeping track at home and so maybe before we start getting into like the design of Adderman and what that was like I actually don't really understand what there was Before Adderman like there was this Adder dat file. Yeah, like can you explain what it actually was doing?

SPEAKER_00: So it was just a set of addresses and it basically stored all IP addresses that we received from other nodes. There were some tests on it, but it had lots of problems, like it was unbounded. As far as I can tell, I'd need to check to make sure, but it was effectively trivial to just spam a node with IP addresses and both its memory usage and its disk usage would blow up.

SPEAKER_01: Yeah. And do you recall that being just a known problem that you were going at?

SPEAKER_00: It was at the time, like, DOS resistance was not a thing, like, you can find multiple quotes by Satoshi where he says the software is not very DOS resistant. It is a hard problem, right? I really don't remember all the thinking and reasoning that led to Adderman. Unfortunately, if you go look at what is available in terms of logs, times were different. Like, you know, PR was open, someone said I tested it, it works, and it was merged.

SPEAKER_01: Seemed to be an upgrade, though, and it held up pretty well. Pretty well.

SPEAKER_00: It was very ad hoc, like there was not much research that went into it, there was no like, it isn't that we went over like these are the design goals or whatever, it's just something like there's a few that you can just derive by looking at the pull request at the time, like it's finite in size. That is a big constraint and it's an obvious one because we just don't want things to grow unboundedly. And from that, well, if it's finite in size, you need limits and you need like a replacement strategy. So what Adrman did was make a distinction between IP addresses that we know work and addresses we have just heard about because they're pretty fundamentally different in terms of our confidence in them. And you also want both in that there's this notion of like trust on first use, which is like your SSH client tells you or you're connecting to a server with this fingerprint, I haven't seen it before. And you say, yep, that's a good thing and it doesn't tell you again. So you don't want to always make completely random connections because under the assumption that not every IP address is an attacker, if you constantly hop, your probability of eventually hitting an attacker is virtually a hundred percent. And not doing that gives you, you may still be connecting to an attacker, but in that case you have a problem anyway. So you want some connections to be drawn from the set of peers. And I really don't like to say trust because the level of trust we place in these is extremely low, but there has to be some assumption of not every node in the network is an attacker. If it were, we have a problem. So we can just reasonably assume that that's not the case. And if that's not the case, well, you probably want to use the connections you've used before.

SPEAKER_01: or some combination of having some memory and then also adding diversity. Right.

SPEAKER_03: Totally.

SPEAKER_00: Right, because you want a network to learn. You want, if a new node joins, it over time should get connections so that the network should learn. And I think this is where this balance from like completely separating tried and new entries and dealing with them separately comes from. And then within each has this idea of bucketing them based on where the information comes from. And the idea is there that a single source where a source would be defined as like even not just a single IP address, but a range of IP addresses that are presumably geographically or administratively close to each other only have access to a certain parts of the database. Like every source IP range is mapped to a subset of the table. And the things it rumors can only enter those places in the table. The idea of there will, we need this replacement strategy and how do you prevent a spammer like a malicious spammer who is trying to poison your database? How do you prevent or to the extent possible minimize its impact? That's where that came from. And all the rest I think is just made up some numbers. What's the reasonable memory usage? How many table entries should there be? There's this magical constant of never revealing more than 23% of the table. I have no idea where it comes from. I don't know, I don't know, I don't know.

SPEAKER_03: So just some context for listeners, this is by and large still the fundamental tools that we currently use to store addresses in Bitcoin Core right now. And so far, it seems to be holding up really well.

SPEAKER_00: Well, it's evolved a bit over time, right? So in 2015, there was a paper published by Ethan Heilman and others on eclipse attacks, which I think was the first sort of academic look at this kind of problem. Because I think before that, we had talked about it as a civil attack, this problem of having lots of bad peers. But I think it was recognized that a civil attack is really something different. Because I think the history there is that civil is a name of a character in a book.

SPEAKER_03: Definitely.

SPEAKER_01: it.

SPEAKER_00: Oh, interesting. It's like multiple personality disorder story, and a civil attack is something that appears where you have a number of trusted peers and you trust them to be all distinct parties, but if there is someone who is really controlling multiple of these, they can do a confidence attack on you where you think, oh, most of my peers think this, but it's really just one party. And that is not really the problem.

SPEAKER_01: Oh, yeah.

SPEAKER_00: problem in a Bitcoin setting because fundamentally our hope is to be have at least one connection to the honest network and it doesn't really matter how many bad ones we have as long as there is one honest one so really the problem is eclipsing not so much sibling which is so eclipsing is an attacker managing to make sure all your peers are malicious

SPEAKER_01: I mean, that's such a remarkable trait, though. It really is. That everything could go wrong, except for one, and you're still okay.

SPEAKER_00: Yeah, it's of course, this is only true for the blocks and transaction parts, because presumably, if an attacker manages to be most of your connections, in terms of address, that, you know, this increases their ability to poison you, which over time leads to eclipse attacks. And so all these sorts of problems were analyzed in this paper, and it gave, I think, like seven or eight mitigation strategies for how the situation could be improved. And, like over time, all of them have been implemented, I think, or maybe they're, yeah, there's, there's still a few outstanding, yeah.

SPEAKER_01: Yeah, there's still a few outstanding or in progress, but yeah, there's, let's say, there's a few that are undeployed or partially deployed. Okay.

SPEAKER_03: Come on! The vast majority have been implemented and I think one was done very quick

SPEAKER_01: It was done very quickly too like oh, yeah You can see it seemed it seemed like your collaboration with Ethan was went quite well because things You know before the paper came out. There was a push and then Over time things got fixed also pretty quickly

SPEAKER_03: Oh, yeah, some of them.

SPEAKER_00: Yeah, so I think there were two big ones that were done pretty much immediately after the paper came out. One was making a table bigger, just increasing the number of buckets and the sizes of the buckets. A couple years had passed. I guess we were fine with using a bit more memory. And the other one was giving addresses deterministic placement in the buckets. This reduced the ability of like repeatedly inserting, trying to insert the same thing in a bucket. If it's like only has one place, like it goes there or it doesn't. And then after that, there were a few more, some of them took several years. One was like a feeler connections and a re-test before evicts policy.

SPEAKER_01: Mm-hmm. See by the way Peter's doing all this from memory I'm sitting in front of the answers and Peter's just like doing it perfect harder. It's impressive.

SPEAKER_03: So I thought it was interesting, the idea of inbounds versus outbound peers and ensuring that just because you're connected to an inbound peer, if you mark them as, hey, this is a good Bitcoin connection, like I can use it again in the future, that allows attackers to abuse that, to write themselves into the tried table. That was one of that.

SPEAKER_00: write themselves. That was one that... Oh yeah, right, I had forgotten about that one, that we even did that. That seems so obvious in retrospect, and then Ang...

SPEAKER_01: It seems so. And then Anchors, which was maybe the most recent. Oh yeah, totally. Right, that too.

SPEAKER_03: Oh yeah, totally, because we used block relay only. So anchors are connecting to notes that you already know about when you start up versus selecting more randomly.

SPEAKER_01: So a few others that he suggested, more outgoing connections, which I think, you know, some of that, because of the two outbound block relay-only connections.

SPEAKER_00: Block-only connections have that, but at the same time, those don't relay addresses, so they're not really participating there. Maybe Erlay will help us move some of that traffic. The big issue with outbound connections is somewhere early on in Bitcoin's history, I don't remember exactly, there was a time when the network ran out of connectable inbound slots. Every node has a finite number of connections, on the inbound side it accepts like just sum all of those up, that is an upper bound on the number of connections that can be made. And at the time, like Bitcoin didn't have any like NAT PMP or mini UPMP to automatically open firewalls, probably a vast majority of nodes were running behind home routers. This explains the hesitancy that developers have had to increase the number of outbound connections. In an attack scenario, it's an easy way to increase your partition resistance is adding more connections, but it's been years and this hasn't been a problem for a long time, but it still I think drives decisions around number of connections. And so that's where Erlay really comes in, because Erlay is ultimately a mechanism without going into too much detail for increasing the number of connections without increasing bandwidth. With Erlay deployed, it would be more reasonable for people to increase the number of inbound connections a node can have or even changing the default about that and like that in its turn might make it more reasonable to increase the number of outbound connections.

SPEAKER_01: Yeah, yeah, exactly, like the... Given that that's obviously strong intuition, how do you go about testing that? How do you go out actually changing that default?

SPEAKER_00: very hard. Very carefully. Doing it gradually is a possibility and watching metrics, but it's hard because deploying software, especially something like Bitcoin Core takes a long time. It has very intentionally no auto-upgrade mechanism or something like that to avoid software maintainers from having too much power over pushing changes to the network. And from that, so you can't just say, you know.

SPEAKER_01: Yeah.

SPEAKER_03: I mean, very carefully.

SPEAKER_00: one release, increase it a bit and increase it a bit more, like it takes time. You know, given that we haven't seen a shortage in connections for a number of years and we can reason pretty easily about things like bandwidth usage and CPU usage that more connections bring, like those things you can just test in isolation. So it's not an entirely uninformed decision.

SPEAKER_01: It seems like, just generally, we can be more sophisticated than sort of the way you described your 2012 design, which, by the way, again, has held up very well, so it's not a slight in any way. It's just, I wonder whether simulated networks or just simulations in general would give us some more, some better intuition.

SPEAKER_00: Are you... Designed? Have Changed? Yeah, so for Erlay specifically, Gleb has been doing lots of simulation work to reason about bandwidth usage and so on.

SPEAKER_03: Cool. So can I pop us back to address relay and some more of that? I think in version 22 there were two big changes to address relay. One was one I introduced about reducing black holes. Let's not talk about that. Let's talk about the other one. Happy to talk about that one too. About rate limiting address gossip. Can you tell us about what the mechanism is?

SPEAKER_02: you

SPEAKER_00: Happy to talk about that one too! There was just an observation we had that the total amount of IP addresses rumored on the network today, like if you start a node and run it for a couple weeks and just see how many addresses you see from various nodes, it is a really low number, it's like one every couple seconds. I don't remember the exact number. And then if you compare that with how much we would permit there to be relayed, so this is the old mechanism I'm describing from earlier releases that had been used since time immemorial, was I think there was a buffer of the set of addresses we want to relay to every peer. And it was capped at a thousand, and if more things would enter this buffer, it would randomly start overwriting things out of those thousand. And there was a certain rate at which this buffer is flushed, like just every so often, I don't know, two minutes or something, was it 10 minutes, is it an hour? There is a Poisson timer, or is it every 10 seconds? I really don't know. There's going to be some.

SPEAKER_01: There's going to be some constant in there.

SPEAKER_00: Like, beep, this is where we insert, we look it up and we will insert it. So every so often we check, hey, for every peer, what's in this set of addresses? We want a rumor and just send it out and then clear it. So this puts a natural rate limit on the outbound side of IP relay. It is at most a thousand addresses every this many seconds on average. And if you compare that number to the amount that was actually being used on the network, it was some enormous factor, like a hundred more or a factor a hundred more or something.

SPEAKER_01: This is where we insert, we look it up. Thanks for watching! Thanks for watching!

SPEAKER_03: Oh, gotcha. Yeah, I think it was between like 100 and 1000 X of what was actually being utilized.

SPEAKER_00: And that's concerning because in a way this means that the presumably mostly honest activity on the network today is using far less than what the network would permit relaying and that is exploitable. One can, it's not completely non-trivial, but if someone finds a way to get this buffer full enough, they could have their set of addresses propagate at way, way better than others in the network. And given the fact there effectively is already this funnel effect at the outbound side, it seemed like a fairly easy solution was to apply that at the inbound side as well and just limit at what rate we process incoming connections. So made some statistics, like looking at a bunch of nodes, what kind of activity level do we see and pick a number based on that. So this is a known technique in networking called the leaky buckets rate limiter. And the idea is that you have a bucket with tokens and like say every X seconds a token is added to this bucket, but the bucket can overflow. It can never go about over a thousand say. And whenever an address is processed, it takes a bucket from, a token from the bucket unless there is none. What this gives you is a mix between a relatively low sustained rate, but at the same time also permitting occasional spikes, they go way beyond it without really changing the long term average because ultimately everything is limited by the rate at which these tokens are added to the buckets. And this was necessary because the existing behavior on the network is very spiky due to the way these things are buffered and send out every so often. Obviously the big question with a design like is this exploitable, like can someone overload you and the answer is yes, I think that this does indeed mean that someone spamming you is going to be able to indirectly reduce the propagation. Because this is on the inbound side, this is one step removed, but if I'm going to spam you, Jonas, then honest IP address is being relayed by MIDI to you, like you'll try to send out both to someone else, but together it's too much. So my spam is effectively reducing her honest traffic. The noise drives out the signal. Yes. But A, you do it on the inbound side, which is better than doing it at the outbound side because then it would be you directly already having it. And at the same time, this problem already exists because there is already this rate limiting that is unintentional and not really designed as a rate limit, but the set of a thousand with random replacement strategy effectively allows the same thing already just at a much higher threshold.

SPEAKER_01: Thanks for watching!

SPEAKER_03: On the topic of address spam, I think we saw some really interesting address spam when this PR was up.

SPEAKER_00: I don't know what happened there, but there was this report all of a sudden of lots of apparently random IP addresses being relayed on the network just a couple days after this pull request came up. So I guess it was in time. As far as I know, it was not related in any way. We don't know because I don't think anyone figured out who exactly was doing it. All right, no one's...

SPEAKER_03: Yeah. No one's stepped forward and so it's it was me. Yeah. Yeah So the behavior that was observed was there would be nodes that would spin up and connect to public peers and send packets of 500 adder messages with 10 addresses each and this 10 number is magical in Bitcoin core because Above that and you won't forward those addresses. So that kind of gives the merging effect from different peers that you were mentioning before but then the nodes would just disconnect and there were a few Properties of the addresses that were observed one was that the time associated with the message was Perfectly placed I think nine minutes in the future. So because if it's too far in the future, we won't Propagate addresses anymore and similarly if it's too far in the past so by putting it as far in the future as possible that ensures that You have the largest window of time that nodes will continue trying to propagate these addresses

SPEAKER_00: Yeah, at least. Yeah, and there was a paper written about this researcher called Matthias Klintman wrote a paper on this behavior and formulated a theory about what it was doing, like pointing out this nine-minute-in-the-future aspect, too, and hypothesizing that this is to ensure the longest possible time these addresses propagate on the network. And there was an attempt to map the network to see... Yeah, this is inferring typology, isn't it? Yes, exactly. That was... I mean, we don't know, but that's the theory. I don't know if that's expected.

SPEAKER_01: Yeah, this is inferring typology, isn't it? Yes, exactly. I'm sorry, I'm sorry, I'm sorry, I'm sorry, I'm sorry.

SPEAKER_03: Thanks for watching! the suspected biggest reasons that you would do it and essentially be able to say, how many peers is this public node connected to? Right.

SPEAKER_00: It's trying to count connectivity of nodes.

SPEAKER_01: How is that different than the COINSCOPE paper? COINSCOPE is the long-lived connections and using timestamps, inferring topology through how those are propagated because they're unique. You can connect to a peer from another angle and be able to reconcile that data to see whether they were propagated. Frage the answer in comments.

SPEAKER_00: Yeah, there have been other techniques like TxProbe where you send conflicting transactions and see how those propagate to infer who is connected to who.

SPEAKER_01: Yeah. and see you.

SPEAKER_03: Honestly, I think the amount of information you can get is kind of it's getting harder So in this I think the main thing you could extract was how many peers each of these public nodes are connected to Not who yeah, the previous ones were identifying techniques for who? nodes are connected to

SPEAKER_00: It's not not who yeah nodes are connected to. Yeah. Hmm. Interesting. In TxProbe, you literally connect to two nodes and you want to know, are these connected to each other? That makes sense, yeah. So it's different aspects of, like, different projections of topology data you get out. And I think we have to live with the fact that you can't make it completely impossible to prevent that information from being revealed. And there are people whose opinion is that this information should just be public so it can be used for...

SPEAKER_01: Right.

SPEAKER_03: The information of node topology? Yeah. Oh, interesting.

SPEAKER_00: Yeah. Oh, interesting. I think there have been papers that argued for, you know, making no topology public because that makes it, you know, available for research. Oh, okay, but-

SPEAKER_03: Oh, okay. But wouldn't that also make the network easier to attach? Yes.

SPEAKER_01: Yes. You have to raise new defenses.

SPEAKER_00: To be clear, what's a concern here is if topology is known that helps a potential partitioning attacker figure out where to focus their efforts, right? If you assume it is possible for this information, like if we think that all these techniques for inferring topology are...

SPEAKER_03: sufficiently able to retrieve that.

SPEAKER_00: Then maybe that is indeed the right decision to just make it not hard, but I don't think that's the case. I think that there's always going to be some signal there, but there are lots of possibilities for improving.

SPEAKER_01: Yeah, can't there be some like combination of sort of like how lightning does it in terms of the public your public connectivity and then your private connectivity and the private connectivity at least gives you a little bit of Again, all you need is one honest one. You just have one honest connection

SPEAKER_03: Yeah.

SPEAKER_00: Again, all you need is one honest, one... I think you can't really compare.

SPEAKER_01: Lightning nose because I don't want to compare. I'm saying a concept of having a public versus a private and the idea of there's different kinds of trust when you're talking about public versus private but you introduce a little bit of reputation when you're talking about public and Private and maybe those are longer lasting connections and it's it's up to you as to who you're trusting

SPEAKER_00: I'm sorry. The problem with any kind of reputation is that there has to be something at stake that you lose when you behave badly. And in Lightning nodes, nodes have an identity and have connections with money that is at stake. And in Bitcoin nodes don't have an identity intentionally because we want to hide the topology. But also, there can't be an identity that...

SPEAKER_01: Thank you.

SPEAKER_00: You know, you don't want something like a proof of stake before you can run a node. So that makes it very hard to say what is an honest node, right?

SPEAKER_01: I mean, I guess another way that is different and that is the ephemeral nature of these connections and if you watch a node and sort of see The disconnection and connection and when I was a new user and sort of seeing that that was happening often was a little surprising It's like wait I don't I don't maintain these relationships any longer than is actually occurring that it felt counterintuitive

SPEAKER_03: Yeah. And in fact, we have mechanisms to very carefully have potential for rotation, such as every so often, I think five or 10 minutes, we connect to an additional block relay only. And if that node provides us a block that we didn't know about, then we will prioritize it. And make it replace an old...

SPEAKER_01: Yep.

SPEAKER_00: and make it replace an old connection and yeah.

SPEAKER_03: yeah yeah so in the logs that shows a bunch of disconnecting connecting right even if that might not actually change your long lasting peers or similarly we have one for when we haven't gotten a block in a long time that might be normal or you might be eclipsed so as this last ditch effort you make a full relay connection to an additional node and say a fabled ninth one

SPEAKER_01: Okay.

SPEAKER_00: One, two.

SPEAKER_01: which is also short-lived. Any closing thoughts before we...

SPEAKER_03: I'm very glad we got to cover all of P2P. All of it. We know-

SPEAKER_01: all of it. We now understand everything. Every little detail. It's complex, but we have our best people working on it. It'll be fine.

SPEAKER_00: There's lots of work still to be done there.

SPEAKER_01: If you had more time Peter, what would you like to work on? What's something that you would like to address?

SPEAKER_00: For example, what we were talking about just before, like typology, one possibility is, for example, run a completely separate adderman or even going further, like a completely separate network stack for every public IP you have. Like say you run on Tor simultaneously with IPv4 and IPv6, like just give them their own completely independent network stack. That is not a complete solution because like you're still not going to give them each their own mempool for resource reasons probably. So that's probably still some leakage between them, but things like that would I think help a lot. It's just one thought. There are so many things.

SPEAKER_03: Yeah. So that was actually what popped up in my mind, is top of wishlist as well. And I think we have so many different fingerprint attacks of identifying this node through different networks, which is actually also that paper on the address spam was hypothesizing that that was an additional piece of information you could get, because each one of those addresses had kind of unique attributes to it. So if you send it over an IPv4 address and then you see it on an IPv6, or what would be worse is on these privacy networks that you're trying to keep private for some reason. So I think the fingerprint attacks are a whole class that are pretty hard to attack individually. But if we're able to separate the components and just have different network managers for different networks, then it would really diminish the surface area of that potential.

SPEAKER_00: I think another thing that would be nice to see more work on is S-MAP. So since a couple of releases, Bitcoin Core has had functionality of loading a database of basically telling it which IP ranges are controlled by the same network operators like ISPs and similar level things. But this needs infrastructure, like where do you get that database, what's the supply chain for providing users with that, which is as much a technical problem as it is like logistical and trust question one. So that's something I'd like to work on.

SPEAKER_01: Thanks for watching! And you would couldn't imagine that being hard-coded or distributed from like the weight the same way that the bootstrapping is done Yeah and the so the IP address

SPEAKER_00: Yeah, a problem with that is that it is transient, this information changes constantly, but it is available. You can find these databases from various sources that gather them. But the problem is it is constantly changing. So it's not like you can have a verification procedure about it where, you know, you do it as part of your deterministic build and people repeat it and get the same thing out. So that probably implies we need tools to say, diff two databases and see that there's some value judgment there of like, hey, there's suddenly this change here, is this expected or not? And so I think a lot about it is just giving transparency in what is it and the ability to change it. But I would hope that a mechanism can be found with sufficient eyes that it can indeed be just shipped as part of the Bitcoin Core distribution and at least you have a default.

SPEAKER_01: Well, thank you both for making such a glorious return to the studio.

SPEAKER_00: Thank you. You

SPEAKER_02: Well, that was great.

SPEAKER_01: You're never going to leave disappointed with Peter around, so that was fun.

SPEAKER_02: Yeah, and a treat to have Amini here as well. What more could you really ask for when it comes to talking about P2P?

SPEAKER_01: You can't. You can't ask for anything more, Carolee.

SPEAKER_02: Well, glad we got that straightened out. Thanks everyone for listening.

