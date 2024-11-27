---
title: c-lightning developer call
transcript_by: Michael Folkson
tags:
  - lightning
  - c-lightning
date: 2021-12-13
---
Topic: Various topics

Location: Jitsi online

Video: No video posted online

The conversation has been anonymized by default to protect the identities of the participants. Those who have expressed a preference for their comments to be attributed are attributed. If you were a participant and would like your comments to be attributed please get in touch.

# Enabling multi channel support

<https://github.com/ElementsProject/lightning/pull/4984>

<https://github.com/ElementsProject/lightning/pull/4985>

I have actually been pulling Humpty Dumpty apart. I have a series of like 40 patches which rearchitect the entire way we do c-lightning. We have this architecture where we hand this file descriptor around. The peer connects in or we connect to the peer, we take the file descriptor and hand it around to all the subdaemons. They talk to to the peer depending on what is happening. We have a openingd, we have a dualopend if that is what you are doing, we have a channeld that runs the normal state, we have a closingd that shuts things down. I am changing it so that connectd is always in the loop and intermediates between all of them. The file descriptor, when that gets handed around, connectd does the decryption and encryption. The peer daemons are just now talking like normal. They don’t do any crypto themselves. It is neater in a way because every daemon had to talk to gossipd. If you got a gossip message or wanted to send a gossip message it would have to shuffle it back to the gossip daemon. Now connectd does all that. At the end of this the daemons only see things that are directly relevant to them which simplifies them a fair bit. The connect daemon is doing all the multiplexing and intermediating and stuff like that. There are some good side effects. The connection daemon gets to handle onion messages and ping packets and all those things that are completely independent of what’s going on in the channels themselves. The goal of this is that eventually we can have [multi channel support](https://bitcoin.stackexchange.com/questions/110497/why-doesnt-c-lightning-allow-you-to-open-multiple-channels-with-the-same-peer). We can have multiple channels happening at the same time. But it has taken 3 weeks of disentangling everything. There are a whole heap of dev hacks that were relying on the old architecture. That’s the main things, the developer mode things. We have a whole set of things so you can tell a daemon to disconnect at a certain message to test things. That completely broke when we switched to this new disintermediated form. A whole heap of miscellaneous cleanups and things like that that occurred. It has been a real grind to pull all this apart. The reason that we are doing this is not because it makes the Lightning Network better but because with lnd dropping the ball on standard stuff we feel like c-lightning has to become competitive. One of the big pain points of people is that we can’t do multiple channels with the same peer and people like having that. We always said it is better to have multiple peers and splicing will be coming really soon now. But people have been very clear that this is something that we have to have. I feel like I’ve been doing a lot of engineering and tricky rewriting of stuff that was perfectly fine beforehand because of this. I am a little bit resentful spending all that time because the spec stuff has to be pushed back. We also have some weird CI flakes that I would really like to get to because they are being annoying. In particular it seems like we don’t shut down cleanly sometimes. We get stuck shutting down. That shut down code got rewritten recently so I am very suspicious that that is the cause. It is causing CI to hang. Right at the end of the test everything goes fine, we are shutting down, we put all these messages out saying that we are shutting down and we don’t actually exit and we time out. Obviously we need to find that but it is a very intermittent thing that does not happen for me locally. It does happen on the CI. I really need to get in there with a debugger and figure out what happens which means I really want to reproduce it. I’ll have to do some stress tests at some point and see if I can figure out exactly how we manage to get stuck right at the end. Or go back to first principles and try to figure out how that could happen based on the fairly complicated patch set that went in. Those are the main things. It does mean we’ve got more of a backlog in the PR queue than I would like. Both because I’ve been distracted trying to get this patch series out and also because of this CI glitching due to this issue. Other than that it has been pretty good. I apologize if I haven’t reviewed your PRs, I am really trying to get this muxing and demuxing stuff out. As you can imagine it has been a number of rewrites. I’ve wrote it, figured out a wrong way, gone back. I’ve written at least 3 times as much code as ended up in the final version. This is the kind of deep surgery that unfortunately is never as straightforward as you’d hope. I think I can see the light at the end of the tunnel now. connectd is almost at the point where it can tell what is going on. Every channel has this temporary channel ID and at some point the temporary channel ID becomes a real channel ID. It needs to understand enough of that so that it can direct them to the right place. I think I am really close to being able to do that. At that point I can go through and change all our internal code that makes the assumption that we only have a single channel. The daemons themselves won’t care because they only ever deal with a single channel anyway. It is the logic in the middle that has this concept of an active channel that I need to go through and rip out. The database itself I believe will also not care because it is similarly agnostic to what channels are going on. It is only this logic in lightningd. I am hoping that it will be like that trick where you pull the tablecloth and nothing moves. That’s the theory but there is an awful lot of prep work to get to that point where I do this magic thing at the end. It will be a bit anticlimactic I hope when I finally enable multiple channels at once. But yes we are slowly closing on that. It is leading me into all kinds of dark corners of the code that haven’t been touched, particularly dev hacks. Dev hacks are not engineered the same way the rest of our code is. Touching those has been a little bit nasty. That is the status of where my stuff is. Every time this meeting comes around I realize it is exactly halfway between the spec meetings. If there is anything I haven’t done in that week I’ve got one week left to get stuff done so I can show my face at the spec meeting having done the stuff I promised. Because I have been doing all this I have not done any of that. I’ll have to start leaving post-it-notes for myself to do the spec stuff that I promised. That is my brain dump of all the stuff I’ve been on and my excuses for this week.

# Individual updates

vincenzopalazzo: I’ve finished the work on error reporting in the c-lightning command line. In the lnprototest we have a failure on GitHub Actions where sometimes we are putting the same transaction in the blockchain. We have a failure that I need to work on this week. I am also reviewing some pull requests.

Thank you, your reviews have been helpful too. I look forward to figuring out what that flake is in lnprototest at some point. Every so often it trips so thank you for looking at that. It takes stuff off my plate. Aditya is officially on as an intern after his successful Summer of Bitcoin, we have him on as an intern for a couple of months.

Congratulations.

Most of my time went into figuring out the codebase of the front end. I have added the web socket button at the footer of the wallet and it redirects to a new page, then we enter the IP and runes and then it connects to the node. This is what I’ve done in recent days because the codebase is pretty huge.

This is Spark. This is extending some of the work you did beforehand. When you set up the Spark wallet you have to get a certificate and it uses the certificate to connect. In order to get the certificate you have to have a public domain name, you have to redirect port 80 or run it as root so that you can bind to port 80 to get the Let’s Encrypt certificate handshake, to connect Spark to your wallet. With Aditya’s earlier work that speaks the Lightning protocol in Javascript, instead of doing all this we had this idea that you could just connect to your Lightning node like anything else would and use the Lightning protocol to speak to it. We have this plugin called Commando that lets you run arbitrary commands like that. Our idea was to integrate that into Spark so that instead of doing all this you could just get the rune that Commando uses, basically a cookie, and give it the IP address and the node ID. Eventually it is in QR code form and then you could drive your node that way which is much more convenient than doing this whole setup and Let’s Encrypt certificate. Because our protocol is already encrypted and authenticated that provides you with the same security guarantees you’d have before. Nicely it allows you to have a read only version of Spark because you could hand out a rune that only gives read only access. There are a few twists along the way. One is that the codebase is really big and Aditya has had to wade through and figure all that out. But the other thing is Spark doesn’t actually work the way you’d write it in a modern way. It is a front end to c-lightning. You talk to this Spark server that implements some superset of commands. We want to speak to c-lightning so those commands that need to exist will have to be in a plugin so that you can refer to them like normal commands. There’ll be some work at the backend as well to make all these pieces work. Getting the bit where it actually connects through is huge so great to get that far. I am looking forward to that because I think it will make Spark a lot more usable. I had to give him access to my node to test this out because it has all the Spark backend pieces already set up. I checked and my money is still there which is good. It is my old tip jar, it became my c-lightning node. That powers that for the moment. What’s the next step now you’ve got it connecting?

Now I test out the handshake, then we send the command to run. I’ll do that in the coming weeks.

Excellent. Eventually it will be nice to come up with some QR code format for that so that instead of having to put it in manually they can do a scan. That’s a nice to have on top. You don’t need that for testing. Just in case you get bored.

# Working towards an accounting plugin

I have been working on the accounting story for c-lightning. I got a big [PR](https://github.com/ElementsProject/lightning/pull/4966) up last week that has all the changes that are required in the core, completely revamps what events we are sending out etc. This week I am transitioning to work on the plugin that will consume all the events that c-lightning produces. That will be able to tell you what your balances are, where all your money went, what happened over the last week, what your profit/loss was etc. That is currently work in progress. It feels like I’m making good progress but we’ll see. Hoping to have something out soon and hopefully that will go out in our next release which means that everyone who has been excitedly using CLBOSS to manage their funds will now have a good idea of how much that is costing them or maybe they are making lots of money, we’ll find out.

This might be horrifying for people to figure out how much funds they are burning on random things. This may be true but more information is surely good. I look forward to finding out. For example, with my node I run CLBOSS and it does stuff sometimes that I don’t know. Having some insight into that will be pretty cool. In theory I should be filing tax returns for this stuff as well but I think it is probably a wash. It would be nice to be able to validate that. I think I am spending at least as much on onchain funds as I am gaining on forwarding. I think I’m probably just failing to declare a loss somewhere. That’s a lesser crime I think.

# Backporting Greenlight work

I have mostly been working on pulling the Greenlight plugin apart, working on backporting some of the things that we built for Greenlight namely the plugin interface protocol, JSON-RPC over stdin and stdout. The same goes for the RPC connection, there are a couple of crates out there that talk to c-lightning but they are a bit outdated and it feels weird to have a crate that is inside of the c-lightning repository depending on something that is external to the c-lightning repository which references the c-lightning repository again. I’ll be internalizing all of that stuff and have it in sync with c-lightning itself. Adding Rust to c-lightning means a bit of work integrating into the build system. Many of the pieces of the build system expect stuff to be actual C and therefore that they have a `.o` file matching their `.c` filename. It means disentangling some parts or sidestepping some other parts, making sure that we recompile when our Rust code changes and stuff like that. Minor stuff but it is taking a bit of time. And of course I couldn’t avoid the trap of revisiting the entirety of the code I wrote for Greenlight and making it better. Or at least I think I am doing that. One thing that we definitely have to do is generalize the plugin infrastructure that we write in Rust whereas in Greenlight we only have one plugin that we need to maintain, a framework that is going to be extended by all the plugin authors. It is worthwhile investing a bit of time to actually make sure that it is future proof and extensible. That is what is going on there. The goal of course of all of this is to have the RPC interface that is currently local only exposed over the filesystem through UNIX domain sockets. It should eventually be exposed over gRPC initially simply because that is what we already have for Greenlight with alternative protocols also on the roadmap. I am especially hoping for a REST version so that we can ship with a ready made interface without having Spark have to redo the REST interface and RTL have to redo the REST interface. Basically consolidate around a single authoritative interface. Not so sure yet whether we want to generate the RPC out of the schema files. This might be a neat idea. However the goal for me is to have somewhat stronger typed RPC than we currently have in the schema. For example the public key is of type hex which doesn’t help us much there. Having a stronger typed interface there might be nice. I am undecided whether we want to have the JSON schema to Rust converter and have some overwrite rules that say “Hey if the field is called something pubkey then make it a pubkey” and stuff like that.

We can add types to the schema. We’ve already extended the schema for a few types, we should do it for more. That is just good for everyone. The more authoritative and precise the schema the better the stuff is that we can generate out of it. The schema itself of course is a bit of a rabbit hole. Not sure if I want to take a plunge but then again last week I complained about these rodents running around and me stepping into all the rabbit holes. It might be my job at this point. That is what I have been working on mostly on c-lightning. Since we are all talking about RPC and getting stuff to work with each other I have also built a small tool called RPC tunnel that pretends to be a local c-lightning and in the background talks to Greenlight. I can run Spark over it. That was my small hobbyist project to give myself a frontend to the service that I have been building for the last couple of months. We got a [paper](http://eprints.cs.univie.ac.at/7191/1/fc22_39.pdf) accepted into Financial Crypto 2022 too.

What is the paper on?

It is a re-publication of an analysis of the Lightning Network census that we did a couple of months ago. It looks into the gossip and tries to deduct what implementation it is running and tries to infer some network heuristics like centrality, strongly connected components and stuff like that. You can probably find the previous version online, I’ll look it up later and post it into the chat. It is been accepted as a short paper and I’ve never gotten a paper into Financial Crypto. I should mention I didn’t write it, I’m just the co-author and supervisor of the student that did. Not as much credit to me.

This means you are more senior now, you don’t do the dirty work.

If I was a professor I would claim full responsibility.

# Working towards an accounting plugin (continued)

On the accounting work can you explain the highlights of the coin movements changes you’ve made in the PR? The UTXO view of onchain events has changed?

Nothing has changed that you would see if you were a user of c-lightning. The biggest change has to do with structure of events that we are emitting them, when we emit them and the data that is contained inside of them. We have this notification that we have been emitting, it used to contain this data and be emitted on these certain times. Now it is getting emitted at slightly different times with slightly different data. That is the biggest thing that you as a user of a c-lightning would see with that PR applied. All of the UTXO view stuff has to do with test infrastructure etc.

You’ve got to step back. We’ve had for a few years this infrastructure to trace all the coin movements but we really didn’t have a consumer of it. It was there, Lisa did it ages ago, we never finished it. When Lisa went to finish it she went “I don’t like the data it is producing. It doesn’t quite hit the spot”. So she went back, tore it up and did it the second time better. Hopefully this time we’ll get the part of the iceberg that pokes above the water done. The new version has some nicer properties that we discovered the first time round. It is that classic you have to write the first one so you can throw it away to write the second one kind of thing I think. From a user point of view this will finally happen I think, we will have this much more coherent view of what is going on.

The part that I am working now will be way more exciting and interesting and will actually use all of the updated information. But that isn’t PR’ed quite yet.

One of the open problems with the first one was the whole if you’ve already been running your node you can’t go back in time but you want to get a snapshot of where you are before you start recording from now, getting all the coin movements from now on. That was an open problem previously, we should do something clever, hand wave. This new version is much more amenable to making that work which is where everyone will be starting from now. In future of course you will be running this from Day 1, you’ll have the start from zero every event. But doing it posthoc is kind of nice. And it is good if for some reason it is down for a while, if you don’t have accounting for some period, you can still catch up and see the delta.

Is the commit message description outdated then? It says “Pivoting from a transaction ID based world to an outpoint based world”. Another one is “UTXO view of onchain events rather than fee amounts”.

That’s correct. It is referring to the data that is emitted in the event.

# lnmetrics project

<https://lists.ozlabs.org/pipermail/c-lightning/2021-November/000213.html>

The lnmetrics project, you put a [blog post](https://vincenzopalazzo.medium.com/introduction-to-ln-open-metrics-96a7c859f4e2) up. You want people to connect to your node so there is more data populated on the LN Metrics site? What do you want people to do to help test this?

vincenzopalazzo: lnmetrics is divided between the plugin of c-lightning and the server. To help people need to run the plugin inside the c-lightning node and add in the conf file the link of the server. If you want to know what is the data you are sharing with the node there is the spec but there is not much information, only gossip stuff and payment forwarded information about failures and successes.

It is mostly collecting performance metrics about the use of the node and tries to get a wider picture of what is happening in the network. At the moment we are very much myopic in that we see up to our peers but not beyond that. Vincenzo’s project is to get a better visibility into the behavior of not just individuals in the network but also get a more global view of what the network looks like and what the performance characteristics are. To inform what the future steps of the specification and the individual clients should be.

vincenzopalazzo: lnmetrics also gives the opportunity to specify additional metrics, benchmarking your node in a realtime environment. A couple of months ago we talked about benchmarking the node, if you create new metrics you can benchmark the payment of the node in the real environment by timing the start and the end of the payment. What I want to do with lnmetrics is create a unique system to collect these metrics. We have thousands of data collected but we have different forms. You can acquire all your data from one endpoint. You are trusting me and I am trusting you because you are sharing some data about the forwarding payment success and failures. I really don’t know if it is true or not because you can put additional data in at random but for the moment I trust you and you trust me that I make the right calculation to bootstrap the project.

Speaking of trust we should probably also mention that your plugin is read only right? It doesn’t initiate payments, whenever possible it tries to obfuscate private information as much as possible and not be granular enough to be able to trace payments. But give us developers a view of what is happening in the network and if there is something that could be improved.

vincenzopalazzo: We also verify that the information came from the node by the signature of the payload. We hope to add some privacy features in the future.

But it will just be c-lightning nodes running the plugin that have connected to your node? It is just collecting data on that subset of the network?

vincenzopalazzo: Yes but not because I only want to support c-lightning. At the moment there is not a unique wrapper for all the nodes. If I want to call the `listchannels` or `listforwards` I need to add a wrapper, It is too much work for now to create the wrapper in Go etc. The commands are very stupid, `listchannels`, `listforwards`, not much that we cannot do for other implementations.

That’s future work but they will always have to connect to you or have a channel to your node to populate the site with the data from the nodes?

vincenzopalazzo: No you only need to run the plugin inside c-lightning and add the link of my server. It is only a HTTP request to my server to add your data. This is giving me your view of the network, your list of channels etc. You don’t need a connection with my node and in reality I am not running a real node under the hood, under the server. I am verifying by hand the signature of the node.

I am installing right now, thank you for the reminder.

I hope there isn’t a crash.

My node goes down, you know why.

Software never goes down, it is impossible (joke).

Our software never fails, that’s right (joke).

By the way if somebody is wondering why I kept chiming in with Vincenzo’s project, it is because I volunteered to supervise his project for him. It is not just me being nosy.

In my Master’s thesis we need to draw a graph of how we make this connection, my university, Christian etc.

These projects are never straightforward, don’t worry. We are used to the arrangements we have to do with academia.

# Individual updates (continued)

I am working on networking issues mostly these past couple of days. lnd has been churning up a lot of dust with this tor skip proxy for clearnet targets = true setting which is an interesting thing that c-lightning already has. It makes Tor only nodes an option to connect out to the clearnet peers circumventing Tor through clearnet. When you are a Tor only node by default you are going through the proxy with every connection. A clearnet node would have an incoming connection through Tor through 4,5 hops which adds 1.5 to 7 seconds of delay. It is very easy to ping a IP address API that spits back a IP address to see how it works. Without a VPN I was having 0.3, 0.4 seconds to get to a server and back. This is not even Lightning, this is my node or computer doing it with my home internet connection. A VPN adds about 0.2, 0.3 seconds which is acceptable but Tor is making this 5 times more at least if we are lucky with the circuit. Running a routing node, this is an issue. Going into the c-lightning settings there is this always use proxy = true which we use for the Tor only nodes. If that would be put to false then the same thing happens, it would not use the proxy towards the clearnet nodes. This is an issue when someone is running a node at home because it would expose the IP address. But quite easily you can just download an open VPN configuration and with any of the VPN providers you can mask your home IP and get away with just that one hop. A subscription is needed but multiple nodes can be used on multiple devices. A firewall needs to be set up which can be done with IP tables. What we’d like is to put this into Raspiblitz so that people who are exposing their clearnet IP anyway, they can set this on and be reachable through Tor and clearnet. Or for someone who is more privacy focused they still could set up a public VPN subscription and still have this on and still have 3 times less lag on their payments or routing. It is a complicated issue because there are so many moving parts here.

# CLBOSS

<https://github.com/ZmnSCPxj/clboss>

Another thing is that people are coming to use c-lightning and the biggest attraction is CLBOSS because they realize it is too much to manage channels. People want to participate in the Lightning Network and they want to have a routing node, pay from their own node traveling to El Salvador or whatever, it is easily possible but to manage the node’s liquidity and receive payments it is work that some would never do. For people who are technical enough to do the management of the node but don’t want to focus on it it is a very good option and it seems to work very well. There is a lot of discussion, I have been in contact with Will Clark a lot about his suggestions and PRs for the CLBOSS repo on which nodes to open to. That is the biggest question. The channel sizes should be increased from what is in the last release, it shouldn’t open channels which are below 1 million or 2 million satoshis if there is enough liquidity onchain available. It seems to me that CLBOSS is easily performing as a beginner routing node manager, someone who would just sit down and open 5 channels and leave it as that. A channel would close, they would unbalance and their routing node wouldn’t work anymore. Instead of that it just manages it, a very good experience. It might even be related to the data we can collect with Vincenzo’s plugin. If there is some pattern towards which nodes we would like to open channels to for example, which could be incorporated into the logic of the peer selection of CLBOSS, that could be very useful and something that is a practical outcome of it.

vincenzopalazzo: I am also talking with Z-man to see if this API can help on what data is usable. I was reading an issue, when rebalancing the channel put the money in the smallest channel because we don’t want to create centrality in the network. If you put a lot of money in a channel that doesn’t have enough capacity you have a problem. It is useful to know this information.

There were very good discussions in the issues from fee rate estimation to this kind of peer selection. I understand you don’t want to just open the most simplistic to the biggest node but also you don’t want to end  up having dead ends with poorly connected peers.

vincenzopalazzo: Another problem with CLBOSS is if me and you share the payment CLBOSS starts to understand that me and you are friends and opens a channel with your peer. But this means that we are sure that your friends are good enough for me and this is true or false.

I have seen that happen. Whoever was using CLBOSS, we had some back and forth traffic just paying each other, it was opening back even if they closed the channel.

This is interesting, where are these discussions? They are on the CLBOSS [repository](https://github.com/ZmnSCPxj/clboss)?

Yes in the issues.

vincenzopalazzo: You need a weekend to read all the discussions, they are very long.

Z-man is very verbose, it is a good read.

Is there any plan to add liquidity advertisements or channel leasing know how to CLBOSS?

There is an open [issue](https://github.com/ZmnSCPxj/clboss/issues/78) for dual funded channels which is not implemented yet. It should be because obviously that is a huge saving. No discussion yet so if you make some suggestions there it would certainly be useful. It is something we should push for and it would be good to see.

That is very good that people are pooling resources and the knowledge that they gather. That is how PhDs are made.

That is how the AI is getting born.

Z-man AI is coding up the next AI?

Exactly.

I have heard Z-man refer to themselves as I so they are already sentient.

I met him at the Lightning Conference, the smaller stage upstairs. Not recorded or anything.

CLBOSS interestingly once sent a whole pile of money out in Spark. It was doing a rebalance and Spark doesn’t show onchain movements. If you looked at the logs you could see the money came back to me as an onchain payment. It was a little bit nerve racking. I gave him access to my box to run CLBOSS. As you say it is pretty much like having a novice user do some fairly simple things. It saves me a whole pile of time and so far my funds are still there.

For monitoring RTL it does need to have the c-lightning REST repo installed and RTL but it does show the onchain movements, a richer interface than the Spark one.

Spark is basically just about showing your own payments and what you’ve received rather than monitoring your node so that does make sense.

Accounting fixes this.

Yes. I look forward to my pretty accounting view of all this stuff. That is interesting though. Accounting will give us a view into what CLBOSS is doing which will be interesting. You can armchair quarterback a little bit more easily and say “Hold on. You opened this and I saw you spend this much in fees and we got this much out in Lightning fees. Was that really worth doing?” It is a problem with any kind of active management. You always wonder if you are spending more doing your active management than you are getting back. If you just did the dumb thing maybe you would be better. CLBOSS doesn’t seem to do a huge amount of work. It does spam my logs, it does a lot of monitoring but it doesn’t spend all my sats.

What is best is it is aware of chain fees. It is waiting for 1 sat/vbyte, there was a discussion about it not opening a channel when the fee was 1.65 but it waited until it was 1.0. In the past two weeks it was often 1.0. It is dynamically aware of the mempool state so that is something that saves you time. Sometimes it is better to do this Sunday night.

Has anyone actually looked at the CLBOSS code by the way?

It is C++, I try.

vincenzopalazzo: I am trying to read some code. The only thing difficult for me is the multithreading and the asynchronous stuff. I don’t know the codebase very well.

I am glad two people have cast an eye over it. I know it is C++ but I haven’t even opened any of the files. I have no idea what is going on inside at all.

The issues are mostly about him explaining the logic on why these things happen. You should be able to point to the code but it is not that straightforward.

I would have written it in Python myself. I think AI is probably a better fit for Python.

For rebalancing there are two Python based scripts. One is done by [C-Otto](https://github.com/C-Otto/rebalance-lnd) who is running a big lnd node. That rebalances lnd. There is also [lndmanage](https://github.com/bitromortac/lndmanage) by bitromortac who is a physicist in Germany. Very nice software as well, it is very well laid out in the command line. Both are planning to do this kind of automated node management feature. That would be some competition from that side as well. The thing is that with dual funded channels c-lightning has better tools.

When we do multi-channels as well especially with fees low it does give you another thing for Z-man to play with. Of course if the peer supports dual funded channels that’s easier. And when we get splicing that will also allow him to do that. With everything else on my plate it is definitely not going to be this release. I keep promising the next release but maybe the next, next release. That would be cool.

CLBOSS’s last release was December 15th 2020. One year and two days.

Let me check what version I am running. I think he runs weird versions on mine. 0.11b, whatever that is.

0.10 is the release and considered to be stable. That is what people run on the Raspiblitz at least.

It is not even a Git repo. He is running a tagged release, he is not running straight from Git. It is good to see people contributing to that. As you say it does catch the low fee times when I am not going to be awake or doing other things. One of the things is I wanted to pull out some funds out of my node to start a new node and do an onchain transfer. It really wants to use all your UTXOs to build channels. I had to mug it, turn it off, restart c-lightning, close the channel manually and then move the funds out before it would steal them for opening new channels. It would be nice to say “CLBOSS make this payment but there is no hurry. I want to make this payment within a week, pay to this address” and have it figure out what to close and where to get the funds from. It would be cool to have a little bit more direction to it. At the moment it is get out the way and I’ll do all the stuff for you. I do wonder if it will eventually evolve into this much more high level direction where you give it some vague stuff. “I would like to take some funds out to cold storage” and it just figures out how to do it. Maybe eventually.

At the moment it doesn’t close channels. It does in master but the release has no channel closing activated.

I really want a higher level, maybe I’ve got too much in my node and I want to move to cold storage because the price has gone up or whatever but I’m not in a hurry. I want it done in a week or a month or something. Because it already knows onchain fees and can figure out which channels to close it makes more sense than what I did which is pick two channels that look about the right size and close them and move the funds. That was really dumb, I probably chose the wrong ones. You are right, he needs to do another Christmas release. Bother him for that.
