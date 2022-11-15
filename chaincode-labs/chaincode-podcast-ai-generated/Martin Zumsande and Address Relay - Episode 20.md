---
title: Martin Zumsande and Address Relay - Episode 20
transcript_by: Whisper AI & PyAnnote
categories: podcast
tag: ['His background', 'Getting interested in Bitcoin', 'How to approach P2P', 'The network is changing', "What's the purpose of the Address Manager (AddrMan)?Peering differences to LN nodes", "Ethan Heilman's talk on Network Partitioning Attacks", 'Addrman and eclipse attacks', 'AddrRelay and the role of node addressesGetting connected to the network', 'Self-announcements', 'Address spam in summer 2021 and peer distribution', 'Correction: The peer would not get addresses-divided-by-peers addresses, but 2×addresses-divided-by-peers addresses as the addresses get forwarded to two peers each.', 'Estimating the Node Degree of Public Peers and Detecting Sybil Peers Based on Address Messages in the Bitcoin P2P Network by Matthias Grundmann', 'Simulating the network', 'Requesting addresses from peers', 'Walking through first connection of a nodeCoinscope paper', 'Being a Bitcoin Core contributor']
---

Chaincode Labs podcast: Martin Zumsande and Address Relay - Episode 20

SPEAKER_02: you also have this distinction between the new and the tried tables. So the new tables are for unverified addresses that someone just sent you and you don't know whether they are good, whether there's really a bitcoin node behind them. And the tried table is addresses that you've been connected to in the past. So at some point, at least in the past, you know they were your peers at some point.

SPEAKER_00: Right and you also need to make sure that you get some fresh blood in there so you don't get sequestered into some part of the network and then I don't know you go on vacation and your node was offline for a week and you come back and nobody's online anymore. You need to constantly keep hearing about new nodes.

SPEAKER_01: Hi Jonas. Hey Merch, glad to get you back in the studio before you rush off to London and we're gonna be talking to Martin today, huh?

SPEAKER_00: Yeah, yeah, we heard a talk by him yesterday already. So we're kind of prepped. That's better than usual, isn't it? Yeah, yeah, we have a good idea what we'll be talking about already. We did a few peer to peer topics already earlier with Amity and Peter. But I think we're going to look at different aspects of peer to peer this time. Very good.

SPEAKER_01: Good idea, buddy. Well Martin's been with us for a couple weeks. We finally dragged him in the studio and hope you enjoy the episode Welcome to the chain code podcast Martin. Hi. Thank you for having me. Absolutely It's great to have you in the office these last couple weeks So today we want to hear a little bit more about your background sort of how you got to working on Bitcoin core And then some of the things you're working on so tell us where did where do you come from?

SPEAKER_02: Yeah, I'm originally from Germany and I'm a physicist. I did my diploma and PhD in physics and

SPEAKER_01: What specifically in physics? Physics is pretty...

SPEAKER_02: Yeah, I was doing statistical mechanics for Earth for my diploma thesis, like doing mostly simulations already, so a lot of computational work. And then for my PhD, I worked in the field of like systems biology, which is like a mix of physics, math, and biology. So somehow I tried to apply some physical techniques on problems from biology such as bone remodeling or some signal pathways in the cell, so that's what I did. But that's been a long time ago. I left science to work in the industry and I worked as consultant for banks until I found out about Bitcoin and yeah.

SPEAKER_00: Go.

SPEAKER_01: That's what I did. Well, having a physicist who's now spent some time at banks, I can see the progression to something like Bitcoin. How did you follow upon Bitcoin Core and how did you start working on it?

SPEAKER_02: Well, I got interested in the space at first, not so much technical, but trying to understand how Bitcoin works. There was an essay I read that I liked very much. It made me feel like I understood Bitcoin better, which was by also physicist, I think, Michael Nielsen. He had a blog post there and that was the first time I thought I really understood Bitcoin on a certain level, of course, and went deeper into it. I wanted to really understand how it works, like at a lower level, like at the lowest level, the level of code, and I got interested in Bitcoin Core and started contributing like the small thing first. Also, I still had a job at the same time, so I couldn't do this full time, so I picked some smaller projects, reviewed some PR, participated in the RevuClub, which was great, which also started at the same time when I got interested in Bitcoin, and yeah, here I am.

SPEAKER_00: And that's... That was the first one.

SPEAKER_01: Very good. I think waxwing is a physicist, isn't he?

SPEAKER_00: He's a mathematician, I think. I think he used to be a math teacher. Cool.

SPEAKER_01: Oh, okay. Well... We'll let the part out. I was wrong about that. So you seem to spend more of your time in Bitcoin core lately in the P2P area. So tell us why that area and sort of what's interesting you there.

SPEAKER_00: area.

SPEAKER_02: I think I've been interested mostly in peer-to-peer from the start. It's just that I have more time now to work on these problems. And it is the field that interests me most and mostly because I think it's not only about the code and understanding the code, but about the network, like how all these different agents who run their own code, some different versions of Bitcoin Core, some other implementations, whatever, they all work together and on a systems level, some behavior comes into play that is larger than just the parts. So it all works together and it is, it needs to be secured. There are like several ways one could attack Bitcoin Core or the Bitcoin network and making sure that this works well when everyone plays nice together. And it's also resistance against attacks. That is something that I find really interesting.

SPEAKER_00: Ma- Yeah, I think one of the interesting things is that the credo is never to trust another node for what they tell you, because they might be lying. So on the one hand, you have to make it work locally and you have to have an emergent behavior across the whole set of participants that is not wasteful, but still gets everybody all the information they need. So, yeah, I can see the appeal.

SPEAKER_01: you And how do you sort of approach the different tradeoffs? Because when we talk to, we've had Peter on the podcast talking about P2P, we've had a media on the podcast talking about P2P, it seemed very nuanced. And so how do you think about those tradeoffs and understanding when you pull this lever, something else pops up over there and also the history and the context of P2P because some of it in some cases came out of Peter's head, some of it is like deliberate, there still seems to be some, you know, DOS vectors in there. So how do you think about all

SPEAKER_02: Well, I think the one thing is to try to really read the code and not read it once, but read it many times and try to find new nuances. Why is that that way? If you find something that interests you and one of the things that you should do, if there is something that you find you don't really understand, but then often you have the urge to say like maybe, oh, I'm sure someone has thought about it and maybe think of it another time and let's concentrate on something else for now. And I think these exactly are the points where most people do the same and where it's interesting to look deeper and really answer the questions you have yourself and until you know or assure you have a solution. And sometimes, yeah, you found something that some people haven't thought of before and then you maybe create a PR to fix this and yeah.

SPEAKER_00: Yeah. So you're saying Bitcoin developers are like peer-to-peer nodes. They don't trust what other peoples have done?

SPEAKER_02: Yeah, I mean, you should never really trust the code that it works. I mean, it's not necessarily that someone has written bad code on purpose, but maybe something that used to work once stopped working because of something that was done in another part of the code base. And there are many ways that things could go wrong. And so I think it's always best to check for yourself how the code works. And that way you also find ideas of things to change. I think it's sometimes it's good just to read code and try to make sure you really understand it well, and that's where you find ideas for ways to improve the code by yourself. Sometimes better than going into a code section, like with the purpose. I'm going to change this now also, because this might lead to changes that are not so great.

SPEAKER_00: Yeah, this actually reminds me of one of the topics that came up at BitDev's this week, where we talked about Jameson Lopp's observation that the network appears to get slower because more and more of the nodes are on home connections and core connections. So there's fewer slots on IPv4 available for other participants. So these magic values that were picked, how many peers people or nodes have, might not scale to everybody being on a broadband connection at home. So it's not only that the code and all the Bitcoin core node around it changes, but also the reality of the network changes. So it's sort of multivariable emergent behavior.

SPEAKER_01: Yeah, it will continue to emerge because we continue to try to encourage people running their nodes on Raspberry Pis in remote locations. And what may be good for decentralization may not be so great for bootstrapping and initial block download and things like that. So.

SPEAKER_02: Yeah, and some things just happen because people choose different ways to participate in the Bitcoin network. For example, I just recently was really surprised to see that there are like so many nodes using Tor right now. So I think there are even if you look at some statistics website, there are a bit nodes, there are even more peers in the network that are using Tor than that are using IPv4. So reachable nodes, reachable nodes, reachable nodes. And that is something like a very new development. I don't think it was like this three or four years ago.

SPEAKER_00: Reachable notes, yeah. Reachable notes.

SPEAKER_01: I feel like that's the umbral effect.

SPEAKER_00: Yeah, Raspi Blitz and Umbrol and a few other of those home node packages are configured to automatically only connect to Tor. I think it's part of it is that it is not trivial to puncture NAT and local area network and open up the ports. And if you have a Tor connection, you basically do that automatically. You are configured to receive from outside. So I think that might have something to do with it. And also that people that run Lightning nodes especially don't want to reveal their IP address because it sort of is a hard quality. So Adderman, what's the goal of the address manager?

SPEAKER_02: Yes. Thanks for watching! The goal of the address manager, I would say, is to have a good variety of peers to find to connect to. So you don't want to have all your peers be from the same IP range, or you want to have like a good variety there. But you also only have like a limited amount of addresses you can save. You don't want to have a system where it can overwhelm you, like write up your disk, so you also need to have like a limited amount, so you have like restricted number of addresses that fit there and, and you, and in other men, you also have this distinction between the new and the tried tables. So the new tables are for unverified addresses that someone just sent you and you don't know whether they are good, whether there's really a Bitcoin node behind them and the tried table is addresses that you've been connected to in the past. So at some point, at least in the past, you know, they were rather peers and they were your peers at some point.

SPEAKER_00: Thanks for watching! Bye! and they- Right. And you also need to make sure that you get some fresh blood in there so you don't get sequestered into some part of the network. And then I don't know, you go on vacation and your node was offline for a week and you come back and nobody's online anymore or things like that. So you, you need to constantly keep hearing about new nodes. Yes.

SPEAKER_02: Yes, and that means that old notes will be overwritten at some point. If you haven't heard from them for a long time, they will be like new notes that have a higher probability of actually being there on the network still. They will get a preference, and the old one might be replaced by them.

SPEAKER_01: I think there's a big difference between something like this and the Lightning Network is that these ephemeral connections between Bitcoin nodes, I was surprised when I first booted up a node to watch those connections turn over and find them in your logs, as opposed to Lightning, which is much more like you want to establish yourself as a good member of the community and consistent and like, unless you're going on chain, there's a pretty permanent connection.

SPEAKER_00: Right. Especially since you want to talk about a channel you have with them, you would be permanently peering with those. But with Bitcoin peers, it's very exchangeable. You just need somebody that talks to you, right? So on the one hand, you do want some persistence because you don't want to give an opportunity to an attacker to completely replace all your peers and eclipse you. But on the other hand, you do want some mixed fruit, so you keep being well connected to the whole Bitcoin.

SPEAKER_02: So. And there is one important thing that is different from the Lightning Network in Bitcoin. You don't want to be the network public, so you don't want your peers or anyone else to know which nodes you are currently connected to. That is something that is, I think in Lightning Network it's being published, but at least for the public nodes and in Bitcoin Core this is something that nobody should be able to get this information out of you.

SPEAKER_01: Yeah, I think one of the clearest explanations of the trade-offs here was Ethan Heilman give a talk at the residency and there's a video, we can put that in the show notes, where he talks about just sort of like, I mean, it's really in the context of eclipse attacks, but he really dives into the new and tried table and the different considerations there. And then there's a wiki page on the dev wiki that goes into how that's evolved over the last seven years since that paper came out, seven years. So anyway, if you're interested in more reading, there's stuff there. Yeah, it's a great article. So we did a couple of episodes with Amidi, 15 and 16, that was in October. And then Peter joined for that for episode 16. We covered a little bit of Atterman and Atter Relay, but those are some areas that you're also spending some time into. So why those areas of the code? What is interesting there? And yeah, and why spend so much time.

SPEAKER_02: Yeah, that's a great thought. Yeah, I mean, I'm very interested in add a relay. It's different than the other types of relay, like blocks where you need proof of work, transactions where you spend some Bitcoin, whereas for an address to relay, you don't really have to do any kind of work to relay it, but we still need those. Nodes need addresses to find other nodes to connect to. So it's on the one hand, it's easy to spend the network with addresses. On the other hand, it's important that address relies still works as good as possible so that nodes have a good variety of peers to connect to, that they can find peers quickly and to get all of these different goals and make them work together. And that is something I find really challenging and interesting.

SPEAKER_00: So maybe we can briefly give an overview of how nodes get addresses in the first place. If you want to start with a fresh node, how do you get connected to the network and how do you hear more about other peers in the network after?

SPEAKER_02: Yeah, there are different ways of getting addresses, like for a new node in the network, they would query the DNS seeds. Those are like centralized seeds that are run by Bitcoiners, and they will give you a small number of addresses that will help you bootstrap. They are not meant to be a source of addresses forever, but ideally just once when you are new to the network, they will give you something to start with, and then you build up your own address database and use that in the future. But for that to be possible, you need more ways of relaying addresses to the network, and there are two ways, I would say. One of them is the address gossip relay. So basically once a day, a node will self-advertise its address to the network, send it to its peers, and those peers will take it, pick it up, and add it to their address database, but also will relay it a bit further to some of their peers, usually two, sometimes between one or two. This helps an address propagate over the network, but there is like a certain system for this, some algorithm in place that makes it sure that it doesn't go on forever. We don't want to spend the network with a given address, so this will only work for like 10 minutes or so, and after that it will stop, and maybe on the next day we try again. But yeah, that is the gossip relay, and that is how nodes self-advertisement relate to the network.

SPEAKER_00: Bye!

SPEAKER_01: So we've seen, even within the last year, people try to mess with that. I know that Peter and Amiti briefly went over this in their episode, but what did you observe and how are we addressing that going forward?

SPEAKER_02: Yeah, actually, that was in last summer. There was suddenly a huge spike in the traffic of address being relayed. And it was really interesting to see this unravel in real time. It was some kind of TACA to use a botnet to spam the network with addresses that were not its own. They were just randomly generated IPv4 addresses. They had a number of nodes that did that. They connected to random peers, send them like 5,000 addresses and disconnected and did that again to some other peers. And there were like maybe 30, 40 peers doomed at this time time. And this was going on for quite a long time, like for two months or so.

SPEAKER_01: It was really interesting.

SPEAKER_00: you

SPEAKER_01: And what's your theory? Research, harming the network, like what's the motivation?

SPEAKER_02: Yeah, I can only speculate because it's, I think, not, it is not known. You don't have to speculate, it could have been you.

SPEAKER_01: Could have been you, you don't have to speculate. It could have been you. You seem to know a lot about it.

SPEAKER_02: Yeah, there are different theories. I mean, the attacker, they might have had the intention to attack the network, they might have had the intention to do harm to the network, make it impossible for new nodes to find peers. But that's just one theory. And it's also possible that these were like researchers that were people who want to analyze the topology of the network because they did this in a very special way. They didn't send huge chunks of addresses that would only reach the victim that would receive them and the victim wouldn't propagate them any further. What they did was they split these up into very small packages with up to 10 addresses and they send a lot of these small packages. So what this did was this made use of the address propagation algorithm in Bitcoin Core because Bitcoin Core, when it would receive up to 10 addresses in a package, they would distribute them to the peers and send them further along. So the attackers, they might have had the intention to use this in order to find out how many peers their victim was connected to. So you can do this. I mean, you need one attacker node that sends the addresses and you need one detection node that would also connect to the victim and just see how many addresses get related to this node. And you can do the math there and then you can figure out this node, our victim node has a hundred connections or something. Yeah, yeah.

SPEAKER_00: So you talked about this yesterday to us already, so I understand, I think, how it works now. Every time a node receives an announcement of addresses with up to 10 addresses, for each address separately, they'll randomly pick two peers to forward it to. So if you send, say, 500 packages of 10 addresses and a node has 100 peers, they'll randomly decide for each of those 5,000 addresses which two peers to relay that to. So now if there's another peer connected to the attacked node, this receiver or observer node would probably get some 50 addresses. If there were only 10 peers connected to the attacked node, they'll receive 500. So the observer will basically get n divided by a number of peers of these randomly generated addresses forwarded, and that way, well, an attacker could measure the peer degree of the node, right?

SPEAKER_01: node.

SPEAKER_02: Yes. The thing that is called in network science, I think it's called degree distribution, which says like how many peers have how many other peers that they are connected to and to make a distribution out of that. And that is an important measurement to show about the topology of a network. And there are different ways that peer distributions can be. And they could be a power law, they could be like very random, like very evenly distributed. And maybe the attacker just wanted to know how it is for the Bitcoin at degree distributions.

SPEAKER_01: Yeah, that's interesting. I mean, I'm trying to think of the value of that. One, we mostly see them in Lightning. Like you see the Lightning network visualized and like sort of cool and you can understand what the interconnectivity and you can see how it grows. There's also the idea of, there's gotta be heuristics associated with nodes that are configuring their peers and not using the defaults. And so a node that has a thousand connections is some sort of flag as to what it might be. It might be a spy, it might be a miner, it might be just, there's a reason that it would have more connections. So I don't know, I'm just sort of thinking about why someone would do this. It could be a fingerprint. We haven't seen a paper come out yet associated with it as far as I can tell.

SPEAKER_00: Yeah, it could be. We haven't seen a paper.

SPEAKER_02: I mean, actually, there is a paper not by the attacker, but by a team in Karlsruhe. They are a team of researchers there, and they actually have a note that monitors the whole network and probably put the link there in the show notes. They also published a paper on archive about this, and they were actually in a position because they are connected to most notes to calculate the degree distributions. And this is something I find really interesting because this is something really positive that can come out of this because the degree distribution, it doesn't really reveal privacy because it doesn't say who is connected to who, but it does give a good estimate how the network looks like. And this is something that Bitcoin developers or researchers can use in simulations of the network because if we understand how the networks behave, it's much more easier to simulate the dynamics on it in some agent-based model, for example. And so I think this is something I don't know if the attacker wanted to know this, but it's definitely something that the Bitcoin research community can make use of.

SPEAKER_00: DOOP

SPEAKER_01: I want to hear a little bit more about simulations and you've done some simulations for Atter Relay, but you also have a prior history of science and simulations and I'd love to hear sort of how you think about creating simulations and using that past experience. Is there any crossover to creating simulations for Atter Relay? Yeah, how do you go about it?

SPEAKER_02: Yeah, I think there's definitely, I've done a lot of simulations in the past, but it's something I would want to pursue much deeper in the future, because I think for a lot of decision, if we want to change some things, for example, an address relay, change a little thing there, we can say that makes sense locally, we can understand why it should be good, but we are not really sure what this will do for the network.

SPEAKER_01: I mean, there's lots of things, there's early, there's transaction rebroadcast, the list goes on and on. It goes back to my original question of how you think about when you pull a lever and something pops up over there, if you're changing how the network interacts, those variables can cause unintended consequences. So having simulations to go along with the code review obviously gives you more confidence.

SPEAKER_02: Exactly. And I think it would be great if there was some agreed upon or like widely used simulation framework so that each time I want to simulate something that interests me, like that I know about it, I wouldn't need to worry about creating a realistic degree distribution. So it would be good to have that out of the box. Just take one of the realistic scenarios and see how this affects the simulation. Yeah, I know.

SPEAKER_01: Yeah, I know that Suhas has his simulator, Gleb has his simulator, the Carnegie Mellon team, obviously there could be some shared notes there. So there's a third way that nodes on the network learn about addresses, and what's that third way?

SPEAKER_02: Yeah. That way is the get adder message. So when a node makes an outgoing connection, not, not for inbound, just for outgoing ones, we asked them, we sent this get adder message to them once. And then they will answer this with a huge chunk of addresses, up to thousand addresses. And those addresses, they randomly picked from the adder man. And yeah, so that gives, they, they are not filtered for recency or something. So they might, might be a bit older. They might be, they're also being cached right now. So with the get adder message, we would only send out one set of thousand addresses to our peers within 24 hours. So they are something, yeah, a little bit more, uh, long-

SPEAKER_00: Yes. Yeah.

SPEAKER_01: long-living ones. But there's a grab bag there. You have maybe some junk in there, maybe some stuff that's in the tried table, and maybe some actual connections that the node would be paired with, right?

SPEAKER_02: Yeah, I mean, but there is not really a selection for this. We just get random addresses that we just would send away in a GET ADDRUM response. We would just send random addresses. Do you think it should be preselected? Yeah, I think it makes sense because, for example, in many nodes, they would have a lot more addresses in the new table than in the tried table. So that would mean that also like in a GET ADDRUM message, we would have a larger percentage of nodes on a new table. In the new tables, they are not really filter for quality. So I think it might make sense to think about like including a certain percentage of addresses from the tried table that we know that are quality and are good and actually appears on the Bitcoin Core network and include them in a GET ADDRUM response that would be.

SPEAKER_01: We don't care. Yeah, I think it makes sense because And what circumstances would you actually ask for these messages? So you have the bootstrapping mechanism through DNS seeds and you have the gossip. And so it's sort of like that in-between state of I know about a few and I'm going to do some connections and I'll go ask for some samples. Is that sort of the best? Is that the best use of? I mean, it's kind of.

SPEAKER_02: I mean it's being done just once. When you start a new connection to outbound peer, you just ask them once for this big chunk at the beginning of the connection, and then never again while the connection lasts.

SPEAKER_00: So, if you were to restart and reconnect to the same outbound pier again, you would ask again. Yes.

SPEAKER_02: Yes. Yeah. But if you do this within 24 hours, you would get the same response because this is, we don't want to be able to make use of this to scrape our other man database to be able to see that, to see all the nodes that are in there.

SPEAKER_00: nodes that are in there. So and obviously since we don't trust any of our peers we're very paranoid we add that only to our new table right so so we get a big chunk of a thousand new addresses from each outbound connection add that to our new table and if we ever need later some more outbound connections or with our feeler connection every two minutes we would try some of the new tables and potentially move them to trade exactly

SPEAKER_02: The distinction between new and tried, it makes a lot of sense because whenever we would make an outbound connection, we would toss a coin and with a probability of 50%, we would pick one address from the new table, just one, whatever it is, or we would pick one from the tried table. So if our new table was overwhelmed by spam or something, we would still have a 50% chance for each try to pick one from the tried table, which is probably not affected by this. So even if for some reason our new table was junk, we would still have a way to find peers in a reasonable amount of time if we have some addresses in the tried table. If we don't have done, we are out of luck.

SPEAKER_00: Well, if we have some addresses in the tritable, if we don't have them. So, so if you're a completely new node, you would connect to a DNS seed. How much do you get from a DNS seed? Is that like just a few connections or is that a thousand? It's just a few.

SPEAKER_02: I think it was reduced at some point in the past recently, but it's under 50, I think.

SPEAKER_00: OK, so I'm a new node. I connect to a DNS seed. I get under 50 addresses from a DNS seed. And they are basically tried addresses, right? And not new addresses.

SPEAKER_02: They are tried for the DNS seed, so the DNS seed is internally, they have a crawler which tries to connect to Bitcoin core nodes and will only give those that actually exist on the network.

SPEAKER_00: So we are a little less paranoid towards DNS seeds, but that kind of makes sense because we're completely new here and we don't know that we can't trust it. But we still store these in the new table, in our new table, so we don't...

SPEAKER_02: But we still store these in the new table, in our new table, so we don't just believe the DNS seed that they are good, we just put them to try.

SPEAKER_00: to say a good- And then, of course, the node would make eight outbound connections, two blocks only connections, and a feeler connection would start going through the remaining new. And then each outbound connection would give us a thousand new addresses again. So very quickly we would build up some stock of new addresses in our new table.

SPEAKER_02: Exactly. Yes. And all the, let's say, 10 notes that we connected to, when we disconnect them, we would also, like, promote them to the tri-taper, because now we have been able to connect to them.

SPEAKER_00: Although we do not get any new addresses from blocks, only relay connections, right?

SPEAKER_02: Right, but I think the block-only connections themselves that we connect to, their address will still be promoted or tried.

SPEAKER_01: Yeah. I mean, as I listen to this and as I'm sort of catching up on my reading, it just seems so nuanced. Get Adder messages were taken advantage of by in the CoinScope paper where they use specific timestamps that were proliferated through the network to understand network topology. And then Gleb added the cache responses because otherwise you could scrape the Scrape Adder man if you just kept querying.

SPEAKER_00: Yeah. So it's like to remember that there was something that made sure that you never share more than 30% 20 23% 23% yes, 23%

SPEAKER_01: 23% And Peter doesn't claim full responsibility for that, but I'm sure we can look up the code.

SPEAKER_02: I think it was introduced by Peter, I remember. Maybe he found it from somewhere else. That's right.

SPEAKER_00: Illuminati. Hopefully that gets good.

SPEAKER_01: All right. I want to talk a little bit about just what it's like to be a Bitcoin Core contributor and sort of how you think about spending your time, what kind of code review you pick up, how you look for ways to contribute.

SPEAKER_02: Yeah, I think there are many different ways of being a Bitcoin Core contributor. And I think every person has to find a way that works best for them and for their interests. But what I personally like is I don't want to spend all of my time on projects like the multi-index Edelman. And I want to spend a lot of time on review, reviewing other things, because that's the way you learn, especially if you're a relatively new contributor. I think that is important to not get lost in some like esoteric area and spend all your time there, but also like get to know other parts of Bitcoin Core better. And something that I personally really like is like, just look at the list of issues, maybe there's some intermittent failure in some functional tests and just try to see what has happened, try to find a fix, make a small PR there. And yeah, this can take some time, but it's usually not a huge project. You can do this like one evening maybe, and yeah, you fix some small bug there. And that is something I really like. And you also like learned of something about some part of the code base that was not familiar to you before.

SPEAKER_01: Go- Thanks for watching! What's the difference between doing this on nights and weekends and having the opportunity to do this full time and making this your regular job? Like does it, how does it change your approach or how do you pace yourself? Or, I mean, you're a few months in, so what has that transition been like?

SPEAKER_02: Yeah, I think for me personally, before I didn't really have the energy to do large projects because I was just doing this on the side. So I just did a small review there and the small PR there, like changing small, smaller things. Now that I have more time, I'm concentrating on, on larger things like multi-index project is one of them. But I would also try to review larger PR and more complicated PRs of current. So recently I've been become interested in the indexes and there's a large PR by Russ and I'm currently trying to review that, which is, it takes a lot of time because it's a, it's a large change and yeah, I want to spend more time on more complicated changes to the code.

SPEAKER_01: We have an Ackruss t-shirt we have to get in your hands then. I don't know if we have your size but cool. Thank you for sitting down with us and telling us about your days on Bitcoin.

SPEAKER_02: I'll see you next time. Yeah, it was great. Thank you very much.

SPEAKER_01: So, any takeaways from our conversation?

SPEAKER_00: I thought that the Adderman spam was really interesting, the spam attack that was trying to either leverage the exact behavior of Bitcoin Core on what it will relay to learn the node peering distribution, but maybe also just didn't know exactly what was going to happen and then didn't get all their addresses relayed as wanted. Right. That was an interesting thing there. Must have been in government, huh?

SPEAKER_01: Right. Must have been a government op. Didn't read the code close enough. I don't know.

SPEAKER_00: Didn't read that, didn't read that. I don't know. And I just find it fascinating how much a little change at the local level changes the global emergent behavior.

SPEAKER_01: Yeah, which is why we have our best physicist on the case something happens over here and something else happens over there. So Phantom entanglement. That's right. Yeah, it was great to have Martin in the office these last couple weeks And yeah, I really enjoyed the conversation with him He's a really approachable guy and I mean he's been working sort of moonlighting on Bitcoin now for a couple years But really excited to see him working full-time with a grant through brink. So very good We'll try to get this out soon and get into the studio again Probably in the next couple weeks

