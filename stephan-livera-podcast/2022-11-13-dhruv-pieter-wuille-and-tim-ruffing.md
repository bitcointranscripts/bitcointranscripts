---
title: v2 P2P Transport Protocol for Bitcoin (BIP324)
transcript_by: Stephan Livera
speakers:
  - Dhruv
  - Pieter Wuille
  - Tim Ruffing
date: 2022-11-13
media: https://stephanlivera.com/download-episode/5607/433.mp3
---
podcast: https://stephanlivera.com/episode/433/

Stephan Livera – 00:03:20:

Gentlemen, welcome to the show.

Dhruv – 00:03:22:

Hello.

Tim Ruffing – 00:03:23:

Hi.

Stephan Livera – 00:03:24:

Yeah, so thanks, guys, for joining me and interested to chat about what you’re working on and especially what’s going on with P2P transport, a v2 P2P transport protocol for bitcoin core.

Dhruv – 00:03:36:

Bitcoin?

Stephan Livera – 00:03:37:

Yeah, for a course for bitcoin. So I think, Pieter and Tim, I think listeners probably know you, Dhruv, if you want to just give a quick intro for yourself, just for listeners to know who you are.

Dhruv – 00:03:48:

Oh, yeah, sure. So I’m Dhruv, I started working on I started studying bitcoin around late 2019, primarily because there was just one day I just realized that I was skeptical because I had been previously skeptical, which was kind of bad. So I started studying it, and in 2020, there was this day my wife was like, oh, you know, it feels like you could study this thing for a decade, but how about, like, how about you do something? You seem very engaged. I was talking about it a lot, and she wanted me to put my energy into doing something, which is very helpful. I reached out to Amedi, I found her blog post, and she mentored me in the early phases, which I’m very grateful for. And yeah, over time, I just kind of got interested in the P2P side. I was lucky to kind of get interested in BIP324. And in 2021, you initially said I should try to just move the entire project forward. That’s when I started to reach out for advice and met Pieter and Tim. I met Pieter before that, I think, but yeah, we started collaborating after that on this project.

Stephan Livera – 00:04:52:

Yeah. Okay, great. And so do you mind could one of you spell out some of the background for this project, as I understand? Well, you mentioned Jonas Schnelli. I know he was working on this in years gone by. Could you give us a bit of the background of this project and where it came from?

Dhruv – 00:05:08:

Yeah, I just have it open here, so I’ll just take a quick crack at it. But I wasn’t around in these cases. I’m sure Pieter and Tim can add more context. So on March 2016 is when I found the first kind of mentions of something called BIP151, which was initially proposed, and that was for peer to peer encryption. And in March 2019, that BIP was superseded with a new design called BIP324. And he presented it at Breaking Bitcoin, I think, in 2019. And the project had some momentum around 2020. We lost a little bit of steam on the project. There were some design changes that were made that he executed on, but as you know, he kind of moved on from core development about last year. So I was really interested in the project. I found it really fun to study. And so I wrote up all these notes. I wanted to chat with him, I wanted to help. And then August 2021, I remember I had a call with him and he said, you should just take it over and take it to the finish line. So in August 2021 is when he transferred ownership. And we just released the new BIP in October 2022. So it’s been a long road, but it’s also something that’s very, very kind of low level and fundamental, and we want to get it right. It’s hard to change these things multiple times. So that’s kind of the long history, right?

Pieter Wuille – 00:06:28:

Yeah, I think maybe a bit of background. The BIP150 and BIP151 proposal from 2016, 17, 18, which was when there was some activity around, that was a very straightforward design. We want to just add encryption and authentication to the protocol, like add a way first encrypt and then add a way for nodes to verify who is who. And I think as we started iterating on that and got some eyes from people more experienced with cryptography, we started to realize that there are actually lots of tiny improvements that could be made. Like, for example, we started caring much more about hiding the fact that there is even a Bitcoin connection in the first place. Or we started caring about the ability to hide what is going through the line, even in terms of traffic patterns, which isn’t actually included in BIP324, but it does include affordances for doing that later on. And on the authentication side, the idea for authentication, which started with a very simple digital signature scheme, BIP150 we realized there are far more private ways of authenticating, and we really care about that because the Bitcoin network doesn’t. Have a notion of identities, and we don’t really want to introduce a notion of identities, but at the same time, sometimes people connect to a node. They know who it is, it is your own, in which case we want something better than just trust that the IP address is yours, or force people to run over Tor or a VPN or something of that nature. So that proposal started living its life on its own, and we’re now working on actually a protocol for that. But we tried to get a paper written about that, get it actually published, and we’re not pushing for any of that at this point in time, while the encryption side is moving forward. And that is BIP324 now. So it’s an evolution of that original BIP151 idea, but I think it’s a lot better.

Stephan Livera – 00:08:50:

Yeah, sure, Tim?

Tim Ruffing – 00:08:51:

Yeah. And just let me add to what Dhruv said here. So I think this proposal or the entire idea of encrypting peer to peer traffic has been around for a very long time. But I think there were period of a few years where there was no progress on this project. And I think Dhruv really helped because he pulled up all the momentum and kept us busy with questions and all this stuff. So I was always interested in working on this, but it felt like I had a lot of other projects and I think it was the same for a lot of other people. And back then I think Jonas was pretty alone and he has some background in crypto, but he’s not like a trained cryptographer, so he needed help from other people. And back then I think no one really wanted to commit to work on this. But this has changed when Dhruv picked up and finally built up all this momentum and now we could work on it.

Stephan Livera – 00:09:53:

So if I could ask just to bring this back to a level for listeners, what exactly is being publicly shared by our Bitcoin nodes today? Just to help people understand what’s the current state today in terms of what are we sharing publicly? Like just every transaction, everything. But how do we think about that?

Pieter Wuille – 00:10:15:

Yeah, so yes, everything. And the PeerToPeer protocol primarily shares three things. You can think of it as a gossip network that relays individual transactions. So Mempool transactions and unconfirmed transactions. Blocks obviously try to propagate blocks across the network as fast as possible. And third, IP addresses of other nodes to connect to. And all of these things have sort of privacy implications to them. But it is not like the argument for encrypting. This isn’t trivial because essentially all of it is public data. Like everyone will see every transaction, everyone will see every block. IP addresses, not so much, but even there it’s very hard to hide. So why do we care about encryption? Is really metadata like a transaction itself? Well, sure, the transaction is public, but where it originates, which node broadcasted it first, that is perhaps private information. And sure, there are ways around that you can broadcast through Tor or whatever, try to hide by submitting it to a Block Explorer site. But really we just want to raise the bar of the whole network, make it more expensive for attackers to find this out. And for blocks, similar story is like if someone can figure out where a block originates first, they can locate where miners are located, which isn’t. Well, we like to have the possibility that miners run anonymously on the network. Like the barrier to entry should be low and that shouldn’t expose them to eclipse attacks or other attacks on their nodes. So that’s something we care about and I think it’s important to have that. BIP324 doesn’t fix any of this. All it does is raise costs because by its nature, with the Bitcoin network consisting of effectively as interchangeable nodes that all do the same thing, there’s no notion of am I connecting to the right node? Every node is equal. So an attacker can, they can man in the middle connection because you don’t know who you’re talking to. Or they could just spin up their own nodes and get you to connect to them. The point is just that all of this is significantly more expensive than just looking at transactions that go over the wire. If you’re a sufficiently powerful attacker with control over ISPs, or even bigger, well, you can today just see the transaction go over the wire, do that with enough connections and you see where it’s coming from.

Stephan Livera – 00:13:07:

I see as an example today, we see some of the chain surveillance companies come out with a report saying, oh look, we saw all these use of the Bitcoin blockchain or users of Bitcoin in this and that country. And because it’s all just being publicly broadcast, the transactions, the blocks, and as you mentioned, the IP, and currently, as you said, there are users trying to use the onion router Tor as an example. And I know bitcoin has support for that. And I know also there’s support for I2P also. So maybe we’ll have a bit of a conversation around what that is. So just to summarize then, the current say to play is basically transactions, blocks and IP are basically if you’re not doing anything to hide, that’s all just being publicly put out there. So somebody else could know who broadcast that transaction. So for example, they could say this transaction came from Pieters node. Or as an example, if you are a miner, I guess they would know where the mining pool is based out of, right? Like they would see where the mining pool is based out of. And so obviously that makes it a bit more hard to mine privately.

Dhruv – 00:14:10:

I want to add like a couple of things there which are related. So I think when people think about privacy, just to summarize that in a slightly different way, when people think about privacy, they think about confidentiality of the contents of something. However, in a public permissionless system, it’s the metadata that is critical. That’s all you can keep private, really, because by definition, everything else is public. And so the reason privacy of the metadata is important is, one, it is all the stuff you talked about where did the transaction originate, where did the block originate, but it’s also that it’s not really possible to have censorship resistance without privacy. So when we raise the bar on privacy, that lets us raise the bar on censorship resistance as well. So privacy kind of has to be the prerequisite goal of something that’s trying to raise the bar on censorship resistance. Because when you raise the bar on censorship resistance, you’re trying to avoid that censor being able to infer something which lets them censor. And by increasing privacy, you can make that harder to infer. And this is where what Pieter was saying is very important, is that it’s a public permissionless system. So you can’t really avoid a man in the middle attack because the kind of security is in the proof of work piece, but you can raise the cost to infer something about you. Anyway, that’s just kind of what I want to say.

Stephan Livera – 00:15:37:

Yeah.

Tim Ruffing – 00:15:38:

And as a follow up to what Dhruv said about censorship resistance, I think the game in censorship resistance is always raising the collateral cost or the collateral damage for the attacker. So for example, say your Internet service provider wants to censor a certain Bitcoin transactions. What the ISP can always just pull the block and disconnect you from the network entirely, right? But this is probably something that an ISP doesn’t want to do, right? Because then you won’t pay them anymore, they lose customers and whatever. Another thing the censor could do is just censor every bitcoin connection. This is a little bit less collateral damage, but still it’s a pretty heavy form of censorship. But now in the current situation where the ISP can see every transaction on the wire, could just look at the transaction and sensor only specific transactions. So once for the sensor, all transactions on the wire look the same, the censor can’t make that choice anymore. So there’s only the choice of either disrupting or censoring bitcoin connections entirely for a particular user or allowing bitcoin connections. But because as soon as we had privacy, we remove the ability that the sensor can specifically look at the transaction and censor it, or specifically look at the block and censor it. So this is really why privacy helps also with censorship, persistence, but they can.

Pieter Wuille – 00:17:07:

Still spin up their own node and look at everything and then still selectively sensor. And I think it’s important to point this out that this is a limitation, but it does raise the cost for the censor. They can just passively observe most of your connection and just here and there intervene. They really need to intercept the whole connection from the beginning to the end and raising costs.

Stephan Livera – 00:17:32:

Yes. So also from reading the page and also just I’ve heard of this concept online of deep packet inspection. So is that related to this at all? If you could explain that for us, I think yes.

Tim Ruffing – 00:17:44:

So deep packet inspection in general is a term that means that a firewall or some network device doesn’t only look at headers or let’s say protocol metadata like IP addresses, TCP, UDP port numbers and other things to decide whether connections should be allowed. This is what firewalls often do, right? They for example, they don’t allow incoming SMTP connections. SMTP is the email protocol for normal desktop computers because they don’t need this and this prevents attacks and so on. But deep packet inspection really goes a layer deeper and means that the firewall will look at the contents or really the data that is transmitted to decide whether a connection is allowed or not, or in this case maybe whether as I previously said, like a transaction is allowed or not.

Dhruv – 00:18:34:

Tim, is it right that just normal inspection is doing stuff based on metadata that the router has to act on anyway? Like if you look at the IP address of the board, you have to forward it anyway. And so you’d be acting on information that you have to process to do your primary job as the firewall or the router. And then deep packet inspection is looking at the content which is doing additional work to then do something else. That’s not your primary function. Is that kind of right?

Tim Ruffing – 00:19:04:

I think this is one right way to look at it. I guess the terms are not defined 100% right. Where is really the distinction between normal processing and deep packet inspection? I think there is no formal definition, but I think what you say is essentially the right thing in particular for routers to anyone need to look at IP addresses, as you say.

Pieter Wuille – 00:19:27:

I think you can think of deep packet inspection as layer violating. I think that’s exactly what you’re saying. Sure. It has to route packet so it has to look at where the packet is going. But a router isn’t supposed to look at the contents of packets and so when it does, we call that going a step deeper.

Stephan Livera – 00:19:46:

Yeah, okay. And so just to explain, this is another term I’ve seen, if you could help explain this for us, what is a PeerToPeer bytestream? Could you explain that?

Dhruv – 00:19:57:

Yeah, I can crack it on when we say that in the BIP, what we are referring to is just if you take all the contents of the TCP/IP packets and put them together, that’s the bytestream, it doesn’t have timing information, what time the packet arrived, it doesn’t have all the other metadata about it. It’s just when we refer to the bystream we’re referring to the concatenation of all the contents of the TCP IV packets on the wire.

Stephan Livera – 00:20:25:

I see. Okay. So yeah. Could you just walk us through a little bit about this proposal and what is proposed to change just so that node runners and listeners out there can understand what’s going on?

Pieter Wuille – 00:20:36:

Yeah. So the goal is opportunistically encrypting every connection. So the goal is whenever two nodes talk to each other and they both support this proposal, they can negotiate an encrypted connection between them. And all that is encrypted is the transport between these two nodes. So it’s not an end to end encryption or anything like that, it’s just the connection between the two nodes.

Stephan Livera – 00:21:07:

I see. So if I understand it right, then it’s like we might do a version communication and say I’m a v2 node and you’re a v2 node. Okay, now we’re going to talk in this.

Pieter Wuille – 00:21:17:

It’s not that simple. That’s arguably what BIP151 proposal did. It would start as a v1 connection and then sort of negotiate to upgrade to an encrypted one. But there’s an obvious leak there because you’ve done the negotiation to the higher version in an unencrypted process. And I think that is the primary change that BIP324 does. Encrypted connections start out encrypted from the very first bytes that is being sent effectively. And the way this works is the Node making the connection really has to have a reasonable guess that the Node they’re trying to connect to support v2, and they will just start the v2 handshake, which is encrypted from the beginning. And if it fails, it can retry with the v1.

Tim Ruffing – 00:22:08:

That is kind of a negotiation. But it’s not an explicit negotiation. You just try to speak v2 to someone. Well, if the other node just disconnects you, then probably the other Node doesn’t like v2.

Dhruv – 00:22:21:

Yeah. So in Bitcoin P2P, we talked about, we talked about three kinds of gossip traffic before, right? Transaction blocks and adders, which is addresses of potential peers you could connect to. We have a mechanism called service bits in that adder gossip. So let’s say your node and my node are connected, and your node will occasionally query my node, or sometimes my node will just advertise to you. A bunch of potential people you could connect to sometime in the future, should you like when those addresses are gossiped, certain services supported by those nodes are also gossip. For example, SegWit was one of these, right? Does that peer support SegWit. So that way when you make your traffic with them, you can do what is appropriate for that service. We have added a service bit flag for BIP 324 support in the proposal, which means that, let’s say Tim is running a BIP324 supportive node. When my node tells your node, hey, Tim’s node is a potential node you could connect to in the future when you’re looking for a new peer. I can also tell you, oh, by the way, Tim supports BIP324. So you can start out with a completely, what we call in a proposal pseudo random bytestream, which means you don’t have to do this thing where you start out in clear text and then upgrade. What you can do is you can start out encrypted and you can downgrade to clear. And if it turns out that I was falsely advertising to you, let’s say that Tim’s Node is supportive of BIP324. What that accomplishes is otherwise. What I could do is if Tim doesn’t support BIP324 and I tell you that it supports it, you would try encrypted connection, and then his node wouldn’t understand it, and then you wouldn’t be able to connect to him. So I could attack his node in that way. But because you are going to downgrade that attack is not possible. But yeah, that’s the whole story on the signaling, I think, side of it.

Stephan Livera – 00:24:20:

And I guess one other question for listeners, they might be thinking, does this mean even from the very start of a new Bitcoin node, like straight from initial block download? Or is this more like once you’re up and going? Or is it more like you would need to first know a v2 peer to connect to if you want it to be private from the get go.

Pieter Wuille – 00:24:37:

I mean, this goes to the question of how do you discover IP addresses to connect to? To answer your question, yes, it is from the very beginning encrypted. As long as you know that the node you’re connecting to supports it. Today Bitcoin core uses a number of mechanisms for gathering IP addresses. There are the DNS feeds, there are fallback IP addresses hard coded in the binary that get updated every release. And there’s obviously the IP addresses that just get rumored on the network, plus whatever the user manually adds on command line or config file. And not all of these mechanisms support giving the service flags along with them. DNS seats, kind of, but really through a hack because we just say that we have different DNS names that resolve to different subset of nodes based on what flag you’re for. But really the only thing that supports telling another node directly these are the service flags supported is the peer to peer protocol. So IP addresses gossip before you get to that stage. I guess very first connections, at least for some time, we’ll probably not get the encryption. Does that match people’s understanding?

Dhruv – 00:26:04:

Yeah, I think I think it’s a little nuanced. I just want to repeat it. Basically, going back to our example, right? Your node and my node are connected. If my node tells you about potential peers, that protocol has service, I’m going to give you the service bits. But on the other hand, let’s say Pieter, and Pieter is running a DNS feed node, right? So let’s say your node just comes online and you don’t know of any peers. You are going to query him for potential peers. Now, his seed is aware of the signaling for BIP324 support, but you would have to query for it. And in the beginning, when there are very few BIP324 supported peers, we don’t think it is reasonable to change the default to query for BIP324 supportive peers. So you only get encrypted peers. People can still choose to do that. Perhaps it makes sense to add a command line flag or something, but it does not make sense as a default once the majority of the network is supportive of BIP324, that is the change we could make. And so then even your initial connections for IBD and such could be encrypted. But it’s a little bit about that adoption curve and getting to a point where that default makes more sense.

Stephan Livera – 00:27:18:

Back to the show in a moment. At a time like this, when there’s a lot of transactions, flying Mempool.Space is the place to view this. It’s a transaction and blockchain visualizer. Bitcoin is a multilayer ecosystem, and Mempool.space helps you by covering this entire ecosystem. You can see the Mempool and the projected blocks. You can see the blockchain. You can even see secondly in networks such as the Lightning Network, it has a Lightning Explorer, which allows you to see the different Lightning node and see what kind of fees they’re charging who has channels open with who. And it’s just a really cool tool that you can even use yourself. It’s free and open source. You can install it on your own software or on your own node rather, and use it to view the Bitcoin blockchain. Now, if you’re with an enterprise, Mempool.Space offers customized mempool instances with your company’s branding. So if you’re interested to learn more, go to mempool.space/enterprise. At times like these, with exchanges blowing up, there’s never been a more important time to learn to self custody your coins, especially your larger cold stack. With unchained capital, you can easily create a multi signature vault. Now, you can do this for free on the website. Just go to Unchained.com. You can set up with them. You can create the vault yourself if you’re savvy enough. Now, you can bring two hardware devices, or alternatively, if you need some help with the set up process, they have a concierge on boarding, so you can pay them. They’ll send you some devices if you need them, they’ll do a call with you and walk you through the process, even if you’ve never held your own keys before. And remember, by doing this, you are helping remove single points of failure. So this allows us to even make one or two mistakes in certain circumstances without losing all of our coins. So unchained.com/concierge is the website here and use code livera for a discount on your package. And now back to the show. So for the show today, Bitcoin Core contributors and developers are joining me. They are Dhruv, Pieter Waller and Tim Ruffing. So now on to the show with Dhruv, Pieter and Tim.

Stephan Livera – 00:29:16:

I see. Yeah. So basically it’s early days, but the idea is that eventually, like, if enough of the Bitcoin network updates to speak v2 P2P, so to speak, then it might actually make sense for that from that point of view. Okay, so you mentioned this idea of Opportunistic transport encryption. So I presume that’s what we’re talking about here is this idea of if both of the node can speak v2. That’s what we’re talking about here with Opportunistic. And you’ve also mentioned this idea of encryption without authentication. Could you explain a little bit about what does that mean?

Tim Ruffing – 00:29:53:

Right, so let me first add some other comments. We always. Say sometimes v2 sometime BIP324 it’s just the same thing here, just for the listener who may be confused about this, it’s just that Bitcoin improvement proposal proposes the version two of the peer to peer protocol. When we use these terms, they actually mean the same. Yes. So we asked about authentication, sorry, about encryption without authentication. And this is usually a little bit of a strange thing because usually we can’t really have this because let’s say I want to talk to Pieter in a secure way or in a confidential way. When I say confidential, that already kind of includes the identity of the person that I want to talk to, right? Like, because I need to say, okay, I want to have this conversation such that only Pieter can read what I say or can read what I write and not someone else. And this kind of means that we can’t really have encryption in a strict sense without some form of authentication. Now, but what we can do in an open network such as Bitcoin, where there are no real identities, as Pieter mentioned earlier, it’s just we can still just enable encryption and hope we talk to a node that’s not spying on us, in a sense. And now what could happen is that we actually talk to an attacker. Maybe that’s just because this is a node which is malicious, or this is an attacker that inserts itself into the connection maybe between me and the honest node and then place this kind of man in the middle attack. And at that moment, again, our encryption is not really helping us because now I can’t tell that I’m talking to this malicious peer instead of honesty, because, again, there’s no real difference between a malicious peer or an honest peer. Of course peers can be malicious or honest. They can spy on you. They can’t spy on you. But it’s not that I can’t tell the difference. I just connect to a random node and a random peer. And whether this peer is acting malicious or reading my data or like, I don’t know, reporting my data to some agency or whatever, this is something I can’t know at that point. So the idea is that, again, as Pieter said, we’re just raising the cost for raising the bar for the attacker. Because now the attacker either has to spin up their own nodes and hope that they connect to them, or they can connect to us, or they really have to actively interfere with connections and not just be passively listening on the connections.

Pieter Wuille – 00:33:00:

So I think this is a good point to go into the difference between active and passive attacks. The definition for that is just a passive attacker is someone who can observe what is going through the wire but cannot change it. And an active attacker is a non passive attacker. But even within active attackers, I think we can distinguish multiple degrees of activity. The simplest active attack that is possible today on the network is go back to that example of an ISP willing to censor one specific transaction, but they can just see that transaction on the wire and not relay it. That’s sort of the they don’t need much state. They can just look at what goes to the wire, delay it by a bit, look at the byte, see, oh, here’s a transaction, I’m not going to pass it through. A slightly higher level is what would be actually significantly higher level is what an attacker would need to do to interfere with BIP324. That is, they basically need to run their own BIP324 implementation on both sides of the connection. So really the honest node is talking to the attacker. The attacker forwards all the data to another connection, which forwards it using BIP324 to another node. And this is in principle detectable because nodes compute a session ID. And if these nodes have a means of communicating out of band, they’re both my nodes and I can look at the session ID, I will notice that they’re different because now there are two separate encrypted connections from the different nodes to the attacker. This is a more expensive and more detectable active attack than just one that drops certain transactions because they basically need to intercept the entire connection, every byte. They can’t selectively do this anymore. And I’d say an even higher cost is just the attacker running their own nodes and get you to connect to them, which is not as detectable, perhaps, but it’s also not as powerful because sometimes people make deliberate connections to a certain IP address.

Stephan Livera – 00:35:16:

I see. Yeah. As an example, just so I’m understanding this right now, I’ve heard of attacks or ideas where people can try to look across the network and see where did that transaction originate or where did I first see that transaction. But in a BIP324 world like hypothetically, in order for that kind of attack to happen, the attacker might need to be running a lot of nodes all around the network and hope that one of his nodes was the first to be connected to and sent that transaction. Right.

Pieter Wuille – 00:35:43:

That’s one possibility. Another is that the man in the middle connection. So if the attacker has the ability to actively intercept and actively attack connections being made by honest nodes between each other, they don’t actually need to run their own node. It’s more like inserting node in between. You don’t know who you’re talking to.

Stephan Livera – 00:36:04:

I see. But that’s also not an easy task to achieve, especially if the Bitcoin nodes are connecting to eight connections or ten connections and things. Right, right.

Tim Ruffing – 00:36:12:

And also because if you look at, for example, your ISP, who would be able to perform like a passive attack very easy. Like just get all the data on the wire, they control the routers. Right. So they can just dump all the data that goes through to the network. But it’s much harder to perform an active attack because they need to run up their machines in the sense that the network infrastructure is the core of the network, is typically not like real computers, there are routers and cables and all that kind of stuff. So of course you could in theory perform those active man in the middle attacks. But that basically means that either the router has to do this and this puts a lot of lot on the router, or the router has to forward like your connection in the malicious way to some machine in some data center run by the ISP again. And then this machine needs to do the heavy processing and basically emulate the full v2 connection. So this is just from the amount of cost that is required, much, much higher. Because really routers are built to basically move data from one wire to the other wire really, really fast. And they are not supposed to just by design, not supposed to look at the contents because this will be very slow. And if you would try to run like one of these attacks on the router or do this on a large scale, that’s not easy with the current hardware. So this is why this really raises the bar for attackers like your ISP, for example.

Dhruv – 00:37:49:

Yeah, on that I want to add a little thing, which is two things. One is a lot of the themes of the project remind me of this phrase, bitcoin is money for enemies. You don’t know your peers usually and so bitcoin lets you there are incentives which make it so you can trust the data coming in. There’s proof of work, there are incentives. And so you’ll see a lot of that theme in here. That’s one thing I wanted to say, every time I think about these things, as I’m hearing them, once again I’m thinking of that phrase. And the other thing I want to say is, before BIP324, an ISP could say, or, you know, a government could go to an ISP and say, I want you to drop all bitcoin traffic. They could literally look at the word bitcoin version, verac and these packages drop it and they already have the tech to do that, especially places like China. You see this, right? They can do DPI pretty easily. But now instead of blacklisting bitcoin, they would have to whitelist protocols. They would have to say drop everything that you don’t understand because the bytestream is pseudo random. So they would have to drop everything that they cannot understand. That might include proprietary protocols between large corporations that would result in a hit to economic activity. It just kind of raises the bar of it’s just like not as easy to isolate this traffic and just be like shut this down, this one thing. And that goes back to the point of collateral damage Tim was making earlier. That is what raises the collateral damage if they were to try to censor on a large scale. Yeah.

Stephan Livera – 00:39:27:

So put in other words, it’s like saying it’s not easy for, or making it so that it’s not easy for an ISP or a government to stop specifically bitcoin connections. They would have to stop a lot more than that, and in so doing, they would cause all this additional damage. Like, let’s say some corporate server wants to connect to some other guy with Zoom encrypted, then they might have to stop that too. And so then it makes it harder for people to, I guess you’re saying, to single out the bitcoin connection and stop that only that’s what we’re talking about, right?

Dhruv – 00:39:57:

Still not impossible, but harder. That would be the thing, right?

Tim Ruffing – 00:40:02:

Or at least that’s the vision. I mean, currently, even if every node now would run v2, it would still be very easy to single out bitcoin connections just by looking at the TCP port number. So the way this works on the internet is that every machine has an address. You have some kind of IP address, but now, of course, you want to have more than one connection. So to be able to distinguish multiple connections, you have something like port numbers. So I can connect to you on port 80, maybe if your web server, I can connect to you also on some other ports to get some other kind of service. And also bitcoin uses very specific ports. And this is still something that is very easy to see even for routers nowadays or for firewalls. But by adding encryption to the protocol, we basically lay the groundwork for getting rid of this too. So of course we could just also now move to different port numbers. For example, I could run even an unencrypted bitcoin node today on a port that’s usually used for web traffic, for http traffic. But of course it would kind of not be that super helpful because now the firewall could still look at the traffic and see, okay, there’s still this literally the true set of word bitcoin in there in the first few bytes. So it’s very easy to distinguish if we encrypt the connection, we get rid of that easy way to spot the bitcoin protocol, and then just makes it much easier now to move to other port numbers and make this look like.

Dhruv – 00:41:48:

Some arbitrary other protocols that’s project Pieter is doing. Right in parallel.

Pieter Wuille – 00:41:52:

Yeah. So there is some work ongoing in Bitcoin core. In a relatively recent release, maybe 22 or 23, a change was made that removes the strong preference for connecting to nodes on the standard board. So historically, the bitcoin core code base and the satoshi code base it originated from have had this very strong preference to pretty much only connect to non port 8333 nodes if there are no 8333 available. It was an incredibly strong preference that for some reasons existed. But due to how the database of IP addresses works today, the reason for that no longer hasn’t held for ten years, basically. So we removed that preference. Now you can run a node on an alternative port and it will get connections from these newer Bitcoin Core nodes. However, the default is still 8333. And if we actually want to get rid of that, that’s a much longer term project. But that is an obvious necessity if we care about hiding the existence of nodes in the first place. Because running on port 8333 is a big flag saying hello Bitcoin, node here. So all the encryption won’t do much then.

Dhruv – 00:43:20:

Yeah, I see.

Stephan Livera – 00:43:21:

But as you’re saying, it’s one step on the way. So you also mentioned, I think this idea of upgradability. So maybe that’s a good point, if you could mention a little bit about upgradability of BIP324.

Pieter Wuille – 00:43:32:

Yeah. So because we take this step of making the bytestream pseudo random like from the very first, and let me repeat that because significant design effort went into making sure that this is the case. So there are really no markers whatsoever, there’s no magic bytes that get sent, no negotiation that’s open in clear text like from the very first byte, every byte is random or from the perspective of an attacker. Due to that, it obviously means there is no version negotiation beforehand. So we couldn’t create a v3 that is detectable by looking at the bytes on the wire unless it removes that pseudo randomness. Again, pseudo randomness means it can be anything, so it must cover everything with the exception of, well, if the first twelve bytes look like a v1 connection, then we’re going to interpret it as a v1 connection, but everything else we’re going to interpret as v2. This obviously means that if we wanted to introduce a v3, where do you put that? The answer is of course, well, you start as a v2, which is already encrypted. So from a perspective of an attacker they’re already equivalent. So you start as a v2 and then upgrade to v3. And we felt that because of the pseudorandomness we really needed an in protocol upgrade mechanism and negotiation mechanism for future versions. And so what those future upgrades could include is we could think about a post quantum cryptography negotiation for example. This is something that would be come at an extremely high cost to introduce to Bitcoin at the consensus level because post quantum schemes, signature schemes have very large keys or very large signatures, but for just key negotiation, post quantum schemes are very reasonable these days and there’s active efforts on standardizing them. So we could imagine that we start off with the v2 as we propose it. Now in a couple of years an extension gets proposed that start with v2, do everything you did, but then additionally run. Let’s now negotiate a key using this other mechanism, and the result is secure if either the traditional elliptic curve based cryptography holds or the new one holds. Another one that we’ve already touched upon is this possibility of an optional authentication scheme later that would only really take place between nodes who do care where they’re running, but obviously many other things, adding compression to messages or yeah, sure.

Tim Ruffing – 00:46:22:

Can I add one thing to post quantum stuff? Because it’s interesting to think about it. You may think, okay, why would it even be useful to add post quantum encryption on the P2P layer if it’s so much harder to update the core network? In a sense that, okay, it’s great that the attacker now can’t break my privacy, or not even true. We’re just raising the bar to for breaking privacy. But now the attacker can steal all my money if he gets a quantum computer. So what’s the point of this? And the answer here is really different timelines. So what you could do now as an attacker against privacy, you could just capture all the data that’s currently transmitted, right, and store it for, I don’t know, 30 years, 50 years in the hope that you can decrypt it. Maybe after 50 years, and I don’t know if Bitcoin still exists in 50 years, if my money is still there, or whether we move to a post-quantum scheme or not in the core of the protocol for storing the funds or not. Maybe we did, but this is something we only need to do when there is a quantum computer. So because at that point, you can steal the money. And this is kind of different to this attack where you capture all the data on the peer to peer network now and try to decrypt it in 50 years.

Pieter Wuille – 00:47:49:

I think a simple way of putting this is in the case of encryption you want to protect from the future. You’re trying to create privacy for something happening now, ideally for some time in the future that people can’t figure out what you did for signatures. You sort of want to protect the past. I don’t have this argument.

Tim Ruffing – 00:48:15:

Yeah, let me give it another try. Let’s say I have some Bitcoin stored now under an elliptic curve public key, right? And I have the private key for this. And let’s say now there is a risk that, I don’t know, there is a quantum computer in a few years or something like this. Now, at least in theory. Of course, this raises a ton of other questions. But what we could do is we could introduce a post quantum secure signature scheme in Bitcoin. And that would mean that at that point in time, I can send my Bitcoin stored under the elliptic curve key to a public key of the post quantum scheme. And at that point, the private key of my old elliptic curve public key is useless. Right. The attacker could get it, I could actually publish it and it wouldn’t have the attacker because no money is stored under this key anymore. And this is why we can basically make that upgrade. Again, like there are a lot of caveats on open questions here, but in theory we can make that update when there’s really concern about a post quantum or a quantum attacker. Whereas for privacy, again, if you store the data now and you have a quantum computer in 30 years, you could decrypt it then. So this is really what makes a difference here.

Stephan Livera – 00:49:29:

I see. So it could help you make that shift theoretically in that post quantum world, let’s say. Also, I guess another question people might be thinking is, does BIP324 or v2 impose a lot of additional costs to running a bitcoin node, either computationally or from a bandwidth perspective?

Dhruv – 00:49:50:

I think sometimes we get very lucky that Satoshi did some things early on that were later. At that time I’m not really sure why they were done, but later it turns out that they were more expensive than they needed to be and we basically end up using that and simplifying the scheme so that overall this does not cost more, or at least not by very much. Right. I think one benchmark is 97% as fast as the previous protocol, and in terms of bandwidth is actually cheaper by three bytes on every message. So we’ve tried to hold the bar of non inferiority. That doesn’t mean that there aren’t sometimes situations where it’s okay to pay a little bit more in compute or bandwidth to gain something. It’s a trade off we have to make. But as of now, as the proposal stands, the users will not see increased computational or bandwidth cost based on our benchmark bandwidth, definitely. Competition is a benchmark.

Pieter Wuille – 00:51:01:

Yeah, I think our goal wasn’t improving bandwidth or improving computation, but we wanted to make it designed in such a way that it having worse bandwidth or computation. Wouldn’t be an argument against it. That’s just noninferiority thing with the caveat that the primary cost in processing things in the transport protocol today is that every message has this four byte checksum, which is double SHA256 over the whole message. And that’s actually the majority of the costs. Now, SHA256 is relatively slow except on hardware that has specific acceleration for it. Very modern intel and AMD CPUs and some ARM CPUs do have hardware acceleration for SHA256 directly. So on those platforms you will see a degradation, but we’re talking in the order of nanoseconds per byte or less.

Stephan Livera – 00:52:08:

Yeah.

Tim Ruffing – 00:52:09:

Let me stress this point. Maybe even if we couldn’t make or couldn’t combine our encryption proposal with those optimizations, encryption is really, really cheap, the kind of encryption that we are deploying here. I think a similar debate was happening, I don’t know, a decade ago when people were trying to enable HTTPS compared to HTTP and some system administrators were concerned that it would increase a lot on their servers. And yes, it increases a lot, but maybe by 1% or something like this. So encryption usually is not a big concern for terms of computation.

Stephan Livera – 00:52:48:

Now, some listeners might also be thinking about whether BIP324 and the v2 protocol here has any impact for users who want to use, let’s say, Tor or I2P. As I understand, there’s no impact on those users, but could you just explain or elaborate?

Dhruv – 00:53:04:

Yeah, so Tor or I2P, these are transports that are available similar to clear, Net, TCP, IP. And so what BIP324 is doing is it’s encrypting before sending on any transport and decrypting after receiving on any transport. So, sure, you can take a completely pseudo random bytestream and do the encryption and onion routing that Tor does, and it would work just fine. Think of it like the deepest layer of the onion, right? It’s the innermost thing, and you don’t have to worry about it. So you can use any transport, we’re just changing the bytestream and you can send it on the transport of your choice.

Pieter Wuille – 00:53:48:

I think maybe a more interesting question is why don’t we use Tor or, say, WireGuard or existing protocols to accomplish what we’re trying to do with VIP 324? And in the case of Tor, I think there’s a very easy answer. Like Tor comes with significant latency increases, some bandwidth increases, significant computational costs, reliability questions, the fact that Tor is essentially a centralized network with centrally run directory servers. There are many good reasons why you wouldn’t want to use Tor for everything. There are very good reasons why you do want to use it, but they don’t apply all the time. And we really want to make something that works for every connection. The wider question is, why not use mechanisms like TLS or noise that are sort of general purpose transport layer encryption? I think that the best argument for that is they incur a very significant complexity because they are centered around trying to connect to someone you know you’re trying to connect to. So a lot of the complexity in these protocols is around authentication. And they go through sometimes extensive steps to get this authentication done as fast as possible, because if you’re loading a website, you care that there are not going ten messages going back and forth before your image starts loading. And so they have a lot of complexity for dealing with this authentication question. And we’re really trying to build a protocol that doesn’t care about this at all. And so we want to avoid the complexity and all the infrastructure that goes along with it, because we can’t have it, we need to stub it out or use fixed public keys or something. And so we can design a much simpler protocol. Plus we can aim for this pseudo randomness from the very beginning, which is not something that protocols today have except as optional extensions or for use in some fairly obscure things.

Tim Ruffing – 00:56:10:

And also we want zero configuration. It should just be enabled by default. You spin up your node and you get a optimistic encryption without any need to configure certificates, public keys.

Stephan Livera – 00:56:23:

Yeah, so as I understand that, it’s about what’s suitable for the network as a whole or the everyday user, as opposed to the more highly privacy conscious user who may be using other things on top or more comfortable to do manual configuration.

Dhruv – 00:56:38:

As I understand it’s also this point that privacy has like some transitive properties. Like it becomes harder for me to be private if you are not taking your privacy seriously. And so that’s why the default setting. But yes, people who want to be private, they are going through all these measures, but even they might have more leaks because everybody else is not doing that. And so when you can do something by default, so you make it opt out instead of opt in, then the transitive benefits of privacy really can ripple through the network, essentially.

Stephan Livera – 00:57:15:

Okay, right. So in terms of this BIP324 and I guess kind of timeline, it would be for people that this might potentially appear in bitcoin core. What kind of timeline are you looking.

Dhruv – 00:57:29:

At in bitcoin core? That’s a hard question to answer. The BIP is out there for public review. We have received a couple of comments so far. Nothing huge so far. There are also a couple of conversations we are still having about improvements that have come up within the working group. The code is all out there. So this is something I want to stress is but there are people, I think there are like about eight or ten people now running v2 nodes. And because this is opportunistic encryption, you can run it on mainnet. We don’t have to go through some very complex testing phased thing. So people are running it. James Obern, Route 13. Max. There are a couple of threads on Twitter. There are adders available. I’m happy to help people get set up with nodes, but it’s there. People are testing it. There is significant enthusiasm in the community about it. But the bottleneck, as with most bitcoin projects, is going to end up being reviewed and it’s hard to at least for me, it’s hard to place the timeline.

Stephan Livera – 00:58:30:

Yeah, sure.

Pieter Wuille – 00:58:32:

There’s good momentum and interest in it. Like cautiously optimistic, I’d say.

Stephan Livera – 00:58:37:

Sure. So for people who want to get involved, what’s the best way for people who are interested or if they want to find out more, what kind of resources would you point them to and what kinds of things are you hoping people do?

Dhruv – 00:58:49:

Yeah, so the primary resource I want to point people to is BIP324.com. That’s one place they can go read the history. They can go get links to the BIP. They can go get links to the PRs. There’s a nice chart of the dependencies between the PRs. So if you want to start reviewing code, where to start and where to go, it’s all laid out there. That’s BIP324.com. And I think for people that are already embedded in the ecosystem and reviewing PRs code, review is the most helpful thing to do. And for people that want to help in other ways, testing is the most helpful thing to do. So take that branch. The instructions for running the node and what to do are on the PRs 24545. The peers, potential BIP324 supportive peers are listed there. Run it on mainnet, tell us on Twitter or GitHub or wherever you want if it’s working well and especially if it’s not working well.

Pieter Wuille – 00:59:48:

Also, I would encourage people to just read the BIP. We put a lot of effort into clearly explaining the rationale for lots of design decisions. And a substantial portion of the BIP isn’t all that technical in details, it’s just text explaining why these choices are made. I think that is interesting as well, even if you don’t care about the nitty gritty details of how the encryption works.

Stephan Livera – 01:00:14:

Fantastic well, I think that’s probably a good spot to finish up. So yeah, we’ll leave that there. I’ll put all the links in the show nodes. So BIP324.com. And thank you Dhruv, Pieter and Tim for joining me today.

Pieter Wuille – 01:00:26:

Great, thanks for having me.

Dhruv – 01:00:27:

For having us.

Tim Ruffing – 01:00:28:

Thanks.

Stephan Livera – 01:00:29:

Get the show notes at stephanlivera.com/433 thanks for listening and I’ll see you in the Citadels.
