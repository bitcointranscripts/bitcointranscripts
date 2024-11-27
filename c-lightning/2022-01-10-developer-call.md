---
title: c-lightning developer call
transcript_by: Michael Folkson
tags:
  - lightning
  - c-lightning
date: 2022-01-10
---
Topic: Various topics

Location: Jitsi online

Date: January 10th 2022

Video: No video posted online

The conversation has been anonymized by default to protect the identities of the participants. Those who have expressed a preference for their comments to be attributed are attributed. If you were a participant and would like your comments to be attributed please get in touch.


# Accounting plugin

I have been working on the accounting plugin for the last few months. We are getting close to a `listbalances` command which is very exciting. I am hoping to wrap up the command stuff this week, get a PR out hopefully later this week. The biggest part with the accounting stuff was I decided to reuse all the database stuff that we already had. The accounting plugin is going to have its own database where it will keep all this data in separately from your node. This will make it such that you will have moving forward historic, we can’t capture old data, but anything that you replay etc will be in this separate database. The nice thing about that is you can cleanup your other database stuff and all your payment data will still be saved elsewhere. That meant I had to take all of our existing database infrastructure and pull it all out into its own little database thing and rewrite some stuff. Christian wrote this incredible re-compilation of translation of SQL statements into Postgres and/or SQLite making it such that our translators can use separate sets of stuff. It is still a little messy, there’s probably some duplication that I could cleanup, I have some ideas about how to do that. It is like rough working copy. I got all the database stuff in around Christmas and then the last week I’ve been working on building out the new crud and database schema for the accounting stuff. Once that is in, the tests are all passing, it seems to be fine. Right now I’m working on the exciting part, we’ve got account balances and then once you have all these events, print out all the events and then we can do more exciting stuff on top of that. My goal tomorrow is to have it printing out a list of all your coin movements in such a way that you could export that and upload it to something like CoinTracker. Have a better understanding of where you’ve earned and lost money operating a node. Lost being things such as onchain fees or fees that you paid for sending a payment. I think we are capturing that data now. You send a payment, a portion of the payment pays the invoice and another portion of that pays the routes along the way. Hopefully the idea is we will be able to start keeping track of that data. You can go through and be like “I paid out this amount of money but this portion of my payments went to paying transaction fees”. This is interesting from an accounting perspective, being able to have a better idea of how much they are saving by using Lightning. That work is continuing. Hopefully to be done soon.

That database shift must have been major work. It grew organically for a long time. Ripping it out and putting it into plugins, that is awesome. That is definitely something that I wanted to do for a while and never got the courage to do.

It is a very big copy, paste job.

This is something you wanted to do anyway. Ignoring the accounting plugin, you wanted to get the database into plugins and you’ve used this opportunity to do that?

I wanted it, Lisa wanted it too.

Everyone wants to talk to databases.

From a basic perspective you could just shove a bunch more fields into the existing database.

And we already do that. There is the datastore API which is there to allow plugins to store additional information inside of the database itself from the main Lightning daemon. This allows you for example if you have a Postgres deployment where you don’t have direct file access, or in SQLite you cannot access the same file, we needed some way of allowing plugins to store the data alongside the Lightning proper data. That’s where the datastore came from. But of course having a database sitting right inside of the plugin is much more performant.

# Working on the cln-rpc and cln-grpc to enable Rust plugins

<https://github.com/ElementsProject/lightning/pull/4980>

I have been working on making our remote procedure call interface actually remote and no longer a huge misnomer. To do that I set myself a task of writing a plugin in Rust that on the one side talks JSON-RPC with a Lightning daemon. For those who don’t know that is going through a UNIX domain socket and can therefore only be accessed locally. We should probably call it LPC, Local Procedure Call. On the other side of the plugin we are going to talk gRPC with mTLS authentication initially with the goal to have eventually more fine-grained access control using Rusty’s [runes](https://github.com/rustyrussell/runes) project. This itself is a reimagining of macaroons. I already did this kind of plugin for Greenlight. It is not something that I could just lift and shift. The methods that we implement on the JSON-RPC side and we expose on the gRPC side need to be mapped. For Greenlight I did that manually because we currently only expose a subset of that. For the full c-lightning API that was way more work than I was willing to do. We now have a generator that takes the JSON schemas, they represent the structure and are used to verify that our responses from the JSON-RPC are well structured and match our expectations. We generate the reading side of these RPCs from those. We have a JSON stream on one side, we get structs out on the other side. We have a translation layer which takes the JSON formatted data and writes them into gRPC formatted data. The conversion is a bit more complex because on the JSON side we cannot have binary strings. Everything is hex encoded. On the gRPC side we can actually use binary strings which is much more performant. Then we also use the JSON-RPC schema to generate the gRPC scheme. This looks a bit weird. Which is why I have a tiny little [drawing](https://hackmd.io/5rtG-VJ6Rh-3mtKq1JZJtQ) here that I’d like to share. There are a couple of conversions. One of the important things that I did over the last couple of days was write a generator that will take the JSON-RPC files and extract and generate all of the surrounding code. It can get a bit weird. This image helped me order my thoughts. Ultimately we should have a RPC that is modern, can be granularly instrumented and authorizations can be given out in a very granular fashion. It should become the de facto standard for our networked RPC. Once we have these generators there is really nothing that prevents us from also generating a REST RPC for example or a GraphQL RPC. This is the first step and I’m hoping that we can use these derived things over time and extend the RPC that way. Otherwise I have mostly been doing small stuff, assisting Rusty in shepherding issues and pull requests through CI. Hopefully we can get to a publishable state pretty soon.

This brings me to Rusty’s update. Rusty has been pretty much in the refactoring hell. He is reworking the way that we communicate with our peer. What we have had so far is when we have an incoming connection we take this connection, we hand it around to different daemons depending on what life stage we are in for the channel. It starts off at openingd, then it goes to channeld, then it goes to closingd and then it goes to onchaind. There never is a fixed daemon where you can talk to a peer. It might be in different stages. That is what has prevented us from having multiple channels per connection or per peer in the past. You could have two channels that are in opening and the other one is already in closing. To which one are you talking? To which one do you give the file descriptor? What Rusty is doing is he extracted all of this into connectd, connectd being the daemon that takes care of talking to the peer. Everybody else just tells connectd what to say to it. That has surfaced a couple of regressions that we didn’t expect. We did expect some regressions but we didn’t expect these specific regressions. We have mostly been working towards fixing those regressions. Currently it is looking very nice and we should get to a publishable state soon. I’m not complaining because that gives me more time to work on my nice RPC of course.

rust-lightning (LDK) has done a lot of work in terms of language bindings for Rust. How does it compare building bindings for other languages from C to what they are doing on rust-lightning?

There we are talking about different bindings. These are the bindings that we use for our RPC interface. I think when rust-lightning is talking about bindings they are talking much more about having a C API that they can compile into their own apps. Whereas this is inter daemon communication or daemon with plugin or daemon with front end. The C API that rust-lightning is building is most likely to be consumed by a binary directly. For example if you are building a Java application or an Android application you will most likely be using GNI to talk to rust-lightning instead of some other Java code. I think they are referring to that. Whereas this is mostly inter daemon and inter process communication. We have a connection or a file descriptor where we write stuff out.

So a bit more internal, a bit more closer to the core?

rust-lightning, yes. What you have on rust-lightning is C function calls that you can call from any client code. But they are residing in the same process. Whereas these protocols that I’m writing are more for inter process communication. I have done some Rust bindings myself for Greenlight, for the client side, and it is a very nice thing to do. So much more comfortable than writing C files yourself. That’s the way to go.

# Individual updates

I’ve been mostly working on the Spark wallet. I’ve [added](https://github.com/shesek/spark-wallet/pull/194) the web socket option in the Electron build. For the web build I will have to set up a proxy because browsers hate unsecured connections. The immediate next step is to add the QR code option in the Electron build so that the user can just scan the QR code and connect to the node, get read only access to the node. I had a brief meeting with Rusty this morning, we will be using the runes library, I don’t know much about that. I will have to read through it. I’ll be writing a plugin similar to the Sparko plugin so I can get information of the node through web socket to the wallet. Present all the information on the wallet through web socket.

So runes are nothing to be scared of. They are just bearer tokens. They are just a string of text that never changes. You send it over as http headers usually when you are talking http. Definitely something that you’ll be able to do.

I think Michael (Schmoock) has got a PR still open on the Spark wallet from December 2020.

I messaged shesek on Twitter.

I am working on finalizing the remote address lookup support which is looking good. There are some remarks from Rusty of course. Fixing those is not that easy. It will be done. The proposal itself I think is also almost clear. There was one point that came up after Rusty’s review of my code. Rusty asked why don’t you check the port that is reported back to the listening port that is obviously not the listening port. Maybe Rusty didn’t think about that. The remote can only report the source port, not the listening port. For me and I think for Sebastian that was clear. I think that this should have been clear to Rusty as well. Another node needs to do, in order to use the remote address feature, is to make certain assumptions or best guesses about what my own listening port will likely be on the public side. This necessarily must not be the same as the listening port on the local side. Why do we transmit the listening port on the protocol level at all? Maybe out of laziness. The address descriptor format which we are referencing in this proposal is from BOLT 7, it has address and port. We say it is the same structure as in this BOLT. We don’t have to redeclare all of this. Sebastian is fine with it. I am also fine with it. I am not sure if anybody else has other opinions on this including a pointless field in the protocol.

Why don’t we need a port when we do domain lookups?

The NAT public IP discovery thing. What we now do is the peer that is getting an inbound connection is reporting back the connection to the remote. “I heard you on this public address with this source port”. The source port obviously isn’t very useful to either one. It could have been removed from the proposal but then we have to redeclare the data structure because currently it is the same data structure as in the node announcement. We just reuse it. Sebastian said it is ok to have it in there, no problem. In theory if we are very pedantic we don’t need this. We would redeclare and transmit without the port. In practice, maybe in the future someone will have some use for this. I don’t know, not sure. You could comment in the RFC if you want it or not.

I wonder if it can be used to detect NAT devices in between, if the source port changed there is a NAT device.

Yes, absolutely. In my opinion we go with the source port and everybody knows it is the source and not the listening port. Maybe some smart guy in the future has a better idea how to use this field. Apart from this it is almost done. Our first PR in our code will have the experimental flag and the first version will likely just log the information. I will open up another PR which will then use this information in several ways. To get this decoupled from the RFC and the cross compatibility testing I want the network layer feature without utilizing this field. That can be in another PR.

The source port doesn’t really hurt there. It is not like it is gossip. It doesn’t have to be stored by everybody. It is just a P2P message. Spending too much time on efficiency there is probably not a good use of your time.

It is just 2 bytes.

Times each connection and both directions. When we switch to 128 bit ports…

Is that planned?

Once we go to IPv64 yes, I guess (Joke). You can’t really expect the author of IP tables to realize the source port isn’t useful in this protocol.

You have to have a port to initialize the connection. Let’s start from there is no Lightning node. When the first two appear how do they communicate? They have to know something, how to reach each other.

That is why we have the DNS seeds. It is a couple of nodes run by me, BlueMatt and roasbeef that feed into a DNS server. All the IP addresses, ports and node IDs they see. You can ping the DNS server to find a node you are looking for or get a random sample.

It is our centralized bootstrapping solution.

This bootstrapping problem is something that we’ve known in literature for the last 60 years now. We’ve not found a good solution for it.

Let’s use Twitter (Joke).

You need to have some way of fixing it. There are viruses that solve the bootstrapping problem by doing an exhaustive search of the entire IPv4 space. This also works but it is kind of expensive.

vincenzopalazzo: Before Christmas I opened a PR to introduce compiling and testing on Alpine. I did this on lnprototest with a Docker container, we can reproduce locally without running the CI each time. Also we can maybe solve the problem that Rusty has to reproduce the failure of the CI locally. Maybe we can introduce the Docker image to try to compile for testing. I was reading the PR that Christian made with Rust because I was working with the same idea, take the JSON and create a different model for a different language. I have a problem to abstract because in JSON we miss the comment and you cannot add metadata. I discovered JSON5 that is a version of JSON that admits the comments. I was starting from JSON schema 5, convert with the metadata, convert the model to an intermediate language and after convert to a different type of language, Java, Rust and Go. It is tricky. Maybe Christian will find a solution and I can find a way to add this metadata. In addition I have two questions. One error I found in `listchannels`, I am not able to catch when `listchannels` is not able to find a channel by short channel ID. `listchannels` sees inside the gossip map and the gossip map contains all the channels of the network. If the channel is not there then it means the peer is offline?

The `listchannels` lists all the channels that have had an update in the last 2 weeks. That is our liveness condition. Only the directions for which the update was. We have two channel entries in `listchannels` for each channel, one going in this direction and one going in this direction. We only keep the ones where we’ve had some activity in the last 2 weeks. And of course we only know about the channels that we have seen something from, in this case being the update.

vincenzopalazzo: If I see some activity like payment forwarding in the last 10 days or 24 hours and I don’t find this channel inside the gossip map I have a bug in my code or I am missing something?

This is a local channel of yours? Is it announced?

vincenzopalazzo: Yes. I have this error by the RPC that there isn’t this channel with this short channel ID. But there is activity in this channel in the last 24 hours. I don’t know why this error happened. If it is not a bug inside my code we can look inside c-lightning.

Make sure to store the gossip store so we can reproduce it. That way we can load up a c-lightning node with the gossip store and see where it goes wrong.

vincenzopalazzo: I need to take a snapshot of what? The gossip store each time I got a failure?

One snapshot and a short channel ID that should be in there, that is sufficient. Then we can load it up and verify why it is not finding it.

vincenzopalazzo: The second question is related to `listchannels`. If I open a channel with a node directly, in `listchannels` there is one inbound and one outbound. Why do we have this channel in 2 directions? If I open a channel from A to B why do I see two types of channels, one from A to B and one from B to A?

It just makes things easier. When computing a route we need to consider that directions can individually be disabled. Therefore this is a directed graph. Once we learn about the capacities while performing a payment we might find that one direction of a channel is too small but the other one might still work. We definitely don’t want to exclude both directions if we find a channel that is too small. Therefore what we do is we use the directed graph where each channel is represented by two edges and we can individually disable them. Why we show that on the `listchannels`, that is for ease for ourselves. It means we don’t have to group the channel halves together. It is just a choice.

vincenzopalazzo: In the dual funded channels what is the difference in `listchannels`?

Nothing.

vincenzopalazzo: We see the same stuff? Only the capacity can change.

No the capacity does not change because we always consider the funding output. That is symmetric for both channels. We don’t share who gave how much into a channel just like we don’t share who got how much from a channel.

Going back to generating metadata, I am tempted to go one step back and have the message gen format be the root document. There is a bit of information that is missing from the JSON-RPC schemas. For example, they are all just JSON files. There is no relationship between request and response. We don’t even have requests for the most part. We don’t have a super structure. For example gRPC calls a service that bundles multiple RPC calls, request object and response objects. I am tempted to do that and have the JSON-RPC schemas be generated. They are incredibly repetitive and horrible to maintain. If you’ve ever looked at it it is just a list of fields. You have if, else statements encoded as JSON objects that tell you which keys are mandatory and which ones are optional. We can come up with something better. What’s the standards joke? There are 10 different standards, now there are 11. That’s my goal for this release.

vincenzopalazzo: JSON5 can be helpful if you want to build an intermediate representation. For example for Golang you want to specify the name of the internal variable if you want to respect some convention.

I’m probably going for YAML simply because it is more widely used. It does have all the features like multi line strings and stuff like that, it does have comments and it is easily convertible to JSON. That for me is probably the way I’ll be going.

vincenzopalazzo: From the YAML you generate the schema, from the schema you generate all the stuff?

No I would probably go from YAML to everything else. The indirection through the JSON schema is lossy.

Have you considered API Blueprint?

No.

That is a markdown text format.

That is Apiary?

Yes. It got bought by Oracle. API Blueprint should be the open source thing.

An [announcement](https://ln.anyone.eu.org/). It has been running for 129 days. It is a computer dedicated for a Bitcoin node and Lightning. It is all the networks, mainnet, testnet and signet and c-lightning on all of these networks. Make some use of it if you like, if you want to test, you have a node over there, you can open channels to it. Not on real Bitcoin, I suggest Signet. Whatever is current and experimental I will be happy to test it. I am generally running always the latest c-lightning source compiled on Alpine Linux.

It is an old MacBook as I see it?

I never needed something like DNS but I am happy to try it. It changes IP addresses, when I reconnect on DSL, a home network.

You restart the daemon?

Yes I restart the daemon and supply it with the current IP address. At the moment there are Chaincode Lightning Network seminars. Since the Bitcoin seminars in the summer we are holding a kitchen, everyone can join any day, it is free kitchen. You can come to kitchen and say hello. If you want to discuss or work on something. There have already been some c-lightning nodes on Signet spawned in the kitchen.

I personally have never run c-lightning on signet. There is something new you can teach me there definitely.

I’ve been working on some infrastructure projects since the last meeting. There have been a lot of people testing CLBOSS in the Raspiblitz context, it has been generating a lot of activity. The backup plugin was growing so much, the biggest backup file I’ve seen was 19GB and that is within 2 months. In the next Raspiblitz release there will be an automatic compact backup feature. It takes the backup file down to the size of the actual database which has been shrinking with the release of v0.10.2. I have lnd nodes that have between 5 and 10GB each even after compacting but it seems like c-lightning is more efficient with space. We’ve had a couple of people recovering nodes and channels, the tools are coming together at least in my mind. We are trying to put it into a menu and guide, some presentable things. I am aware that Lisa has been doing a lot of that as well. Regarding infrastructure I’m running on ARM 64 bit Raspberry Pis and Odroids which are 32 bit. I started a project which is Linux on ZFS, I know your recommendation is Btfrs but ZFS seems to be more battle tested to me. For ZFS if you are using an encryption key file that uses a 32 bit secret exactly the same as the `hsm_secret`. I was able to use the HSM tool to regenerate this, make it from the BIP 39 compliant 24 words. That file is encrypting my disk. I could have the same file as the `hsm_secret`. I have a node now that is much more performant than previous ones in virtual machines and Raspberry Pis. I do run various testnet and signet instances but they are not very stable, they are more experimental and blow up from time to time. There is this [Plebnet playground](https://github.com/PLEBNET-PLAYGROUND) which is on GitHub. It is a signet instance, you have to adapt your Bitcoin Core to be on that network, it is not the default signet network of Bitcoin Core. People are very active there, there is a huge amount of routing and scripts running, around 20-40 nodes. They have no c-lightning instances so that would be an interesting thing to join into.

I didn’t know they used a special signet.

They have all the coins to themselves and they can run their own faucet. There is a [Plebnet wiki](https://plebnet.wiki/wiki/Main_Page).

There is a [video series](https://bitcointv.com/c/bitcoinkindergarten/videos) by Jestopher who has joined us previously, he is working on AMBOSS. He is part of the bitcoinkindergarten community.

You talked about the size of the backup. There is an upcoming feature in 0.10.3. This will be less data consumptive as the backup plugin.

That probably depends. If you have a second sqlite instance running that will consume read and write cycles on your SD cards more quickly than if you had an append only log but it will be smaller yes. I have been looking into writing a sqlite based backup backend as well that should replay all of the operations in the secondary database which could also be remote. Trailing one operation so we can rollback that one which we might be off sync with.

This backup compact command is really good. The Lightning daemon doesn’t need to be stopped for that to run, it just works on the fly. It is just a question of a cron job. You can’t really go smaller than the size of the database I guess?

It shouldn’t because the first step is take a copy of the original database.

I’ve been experimenting with this hybrid connectivity. lnd introduced it and I realized c-lightning had it all along. If you are not forcing the Tor connections then the clearnet peers would be connected through clearnet even if the node is running on Tor. That is a new thing for lnd. We just need to change one option in the config file for c-lightning. I have been running that paired with a hosted VPN, I’ve had mixed results. I had this discussion. The question is on privacy, you are hiding your IP address because you don’t want to expose your home IP but you are doing these clearnet connections where obviously your IP address is leaking. The question was in this discussion, does it make any sense to advertise a Tor and a clearnet IP address at the same time? There is no point because if you have a fixed clearnet IP then it would make sense just to advertise that even if Tor is enabled as well. The connections coming to your clearnet IP would go through less hops. The peers over clearnet or Tor connecting through your Tor endpoint would go through an additional 3-5 hops.

Maybe implementations can only do one, either Tor or clearnet when you have the capability to announce both.

You need at least some nodes that have both otherwise we have two separate networks completely.

You could connect to a Tor endpoint even if you are only advertising your clearnet endpoint. You can advertise multiple endpoints already. The question was does it make sense to advertise a Tor endpoint when there is Tor connectivity? For the lag and the reliability of connection there is no point to advertising a Tor endpoint if there is a clearnet endpoint as well.

That’s why most implementations I guess prefer clearnet when you have both.

It depends on the settings. The Tor nodes of lnd, to a clearnet endpoint they would connect through Tor. Now they have this setting bypassing the proxy which connects to the clearnet endpoints through clearnet bypassing Tor even if the node is advertising a Tor address only. It is a bit of a mess.

I have just made the change in my config because I understand what you are saying and it makes sense. I’m not advertising onion anymore because I know that onion things can connect through Tor to my IPv4 address. There is no point for me to advertise onion.

If you don’t need the privacy which not all users need.

I am advertising IPv4 anyway.

If you have a clearnet endpoint you don’t have anything to hide.

The only thing is at least with our implementation you have to restart the daemon to get the new IP address, maybe we should fix that. I am working on those issues. That is one reason to maybe broadcast Tor, when your software is unable to update its public IP address then maybe Tor is a fallback option. We are using Tor for two reasons. To get around your router and to get around your router.

If only there was a new version of IP that could cover every grain of dust with its own address so we wouldn’t need NAT anymore. I should stop dreaming now.

So Tor is the most fixed endpoint you can have. If you have a dynamic IP or a changing one then you should have that on as well. Yeah ok.

I thought ZFS was from Oracle. You mentioned it is a BSD and I am pretty sure it was from Solaris. Unless I am mistaken and Solaris is actually a BSD.

FreeBSD has their own implementation of ZFS as far as I know which is unrelated to Solaris’ implementation. It is just the design.

My nostalgia bubbled up there because I used to love Solaris and Sun Microsystems.

OpenZFS has appeared on Linux 2 or 3 years ago.

I am brand new, just joined the c-lightning team today actually. Rusty has got me a nice project to start off with. I am going to taking a look at Pieter Wuille’s Minisketch and seeing if we can use it to do more efficient set reconciliation with the gossip network. Try to reduce the bandwidth required for channel updates, things of that nature. I am still going through the BOLT specifications and excited to learn some more. Hopefully in future meetings I’ll be able to present some progress.

There is a lot to play with in the future. Some of the gossip will be restructured as we move towards Schnorr signatures and integrating with Taproot. All that is set in stone right now will become available for re-discussion and improvements in the near future.

I’ve been curious on what the plans are there. That is going to blow things wide open I imagine.

It is definitely good to have you look into Minisketch and bring that perspective into that process as well. We can make the best gossip protocol there is.

My background is probably a little different. I am a mechanical engineer by background. Got into electrical, had to spin up some servers and relay information over it so I got into protocols. That’s my background. I am trying to catch up on a lot of the more IT focused aspects. Excited to learn.

# Zero base fee

I can give a brief overview and we can start thinking about this in the future. I have been talking to Rene (Pickhardt) today. He has been doing his research on finding optimal routes in the Lightning Network. One of the complications that we face is that fee function that we are currently using is kind of working against us for having the optimal algorithm for finding this min cost flow. The reason for that is during the reformulations for the calculation of the min cost flow these fall out as remainders and accumulate, basically just mess everything up. You might have heard in the past that especially on Twitter there has been a push for setting the base fee to zero. Let me take one step back and explain what the base fee is and we can see how that would impact it. When we set the fees for our channels to be used we have one part which is fixed, to say “If I forward any amount there is some fixed overhead for whoever I’m forwarding this for so I want to be compensated for that”. And there is a variable part that is proportional to the amount that is being transferred. Taking the aspect that I have made some of my money available for you to forward your payment and so I should be rewarded proportionally to that. Currently we have both the base fee and the proportional fee, they sum up. According to Rene’s research it would be much nicer to have just the proportional size. That brings us to a cost function when we compute flows and paths where everything is proportional to the size of the payment that massively simplifies the computations. For the mathematically inclined the problem when you have the base fee is NP complete. If you don’t have the base fee it is polynomial. The complexity is polynomial which is way more manageable. There are two ways to get to this more malleable, more tractable problem. Those are we all set the base fee to zero, making it drop away in all the computations, or we approximate. We pretend it is zero, it is not going to be a dominant part of the fee that we are going to pay anyway. Let’s set it to zero for the computation and when we have the route we can do the correct computation with the slightly higher fees. The problem is we don’t have any idea of how good this approximation is. Rene is currently working on finding out how good that approximation is. In the meantime he asked us whether it would be possible to set the base fee to zero by default in c-lightning. The idea being that this already would bring the majority of the c-lightning nodes to have this more tractable problem for pathfinding which we could then start using. That’s basically the setup. I don’t have a good answer of what is preferable or what isn’t. It is definitely something that we as a community should decide together.

Why don’t we set the proportional fee to zero instead?

I’m not sure that would make it polynomial again.

Maybe you have to discuss this with Rene. I thought that it was just the fact that we have two variables instead of one.

No it is that we have a non-linear factor in there.

I am not a fan of this proposal. There is a reason for the base fee and there is a reason for the proportional fee. The reason is not that somebody wants to earn money, it is more the reason that we have to find out how to cover the risks. Maybe in the future we can talk about how to earn money by this. In theory it has to cover risks and by setting this to zero it disables the ability to cover risk which is problematic. The easiest example one could give is that by having a zero base fee someone can do a flooding attack on your node and just route around with the tiniest minimal amount you can get and pay almost nothing.

We do have tools like min HTLC size. You could take the min HTLC size, have your base fee and the proportional fee and hide that base fee in that. You will always get more than base fee plus proportional fee. You’d actually be getting more for larger HTLCs. I am not arguing that we should do that, it is just that as I remember it this nonchalant “We have to do some work that is fixed so we want to get paid for that”, that is something we decided in half a hour back in 2016. There definitely isn’t a big plan behind it.

What is good about zero base fee is since nobody came up with a proper answer to the question how big a base fee should be we have a magic number problem. The easiest answer to a magic number problem is just remove that number. There is no good argument for either number but in the end it should be up to the user or the software to decide a proper number.

I’m saying setting the default to zero.

If you educate the network in a way that zero is the proper value and if you don’t use zero no one will use you for routing then you can’t reintroduce this value anymore. If you set it there will be no forwarding through your node.

Our default is 1 and 1.

In lnd.

In c-lightning it is even smaller isn’t it?

It is 1 msat instead of 1 sat. We don’t have to remove the base fee from the set, it will remain in the capabilities and all we do is set the default hoping in fact that most people will not modify it. But if they choose to they can modify it. Setting a base fee different to zero doesn’t mean you won’t get used. You will be preferred for larger HTLCs where the base fee that you set isn’t the dominating part. You might have a proportional part of 1 and your neighbor might have a proportional part of 2 per satoshi. If I have a base fee of 50 anything above an amount of 50 I will be favored because my overall fee is going to be 100 whereas my counterparty is going to be 100 but they are growing faster. You can mix and match however you want but it is definitely wrong to say outright that setting a base fee in a zero base fee environment makes you ineligible for routing. You may target a different market, your risk may be different but it doesn’t skew things that much.

I always had the idea that a plugin developer would come up with an answer and set the base fee dynamically per channel which hasn’t really happened yet. When too many implementations go for zero then too many routing algorithms will assume zero or filter out the rest and this value will be gone in future. That’s likely what will happen. It will still be there for backward compatibility but effectively nobody would like to choose to change it.

If algorithms choose to ignore the base fee and compute a route without it and then recompute it back in you are actually getting more money than if they were computing correctly. We are actually paying you for sticking to the old protocol. My main thing for a zero base fee right now is that it is almost impossible for us to assign a value to the work that we do for a single forwarding. I have not seen anybody really play with it that much. Most of the algorithms today already make most of their decisions based on the proportional fee.

What’s BlueMatt’s opinion?

He is against it. I think his fear is very much like yours that we lose flexibility and we are taking away options from users.

One thing about this is almost nobody is earning money on Lightning yet. My node is operating at a loss and I don’t care because I do other stuff. The stuff we decide now will have an effect in the future. If we lose this value and it would be good in future to have this value then we would have a problem.

Then we’d reintroduce it.

You are more on the side to drop the base fee?

I am undecided, I would like to move the discussion forward. I do feel that Rene is not being heard despite having an amazing result. A lot of people talk this amazing result down and I have seen what it can do. It got lost in the noise.

This is just implementation level? It is just an implementation choice. Surely it is a c-lightning developer, contributor choice and that’s the entirety of it?

We should still make sure it makes sense at a network wide level and that we aren’t going against the desires of our users by dropping the Easter egg into their laps. It is part of a longer discussion if we want to switch over to a min cost flow based routing computation rather than our current iterated Dijkstra.

Do you see a non-proportional amount of risk to a forwarding? A risk to lose money or HTLC fails, you have to close a channel, certain fees apply. Is there a non-proportional part or is it mostly non-proportional?

It depends on the threat model you have. If it is a purposeful attack and you have an attacker that is motivated to try to ruin you they can just use hodl invoices to not pay any fee and still give you the bad effects. That is very much non-proportional but also pretty meaningless to consider because no matter what parameters we have there we won’t counter that kind of attack.

Along the route the attacker and the victim is someone else but it causes you to fail the channel.

That is definitely a possibility and that is a non-proportional risk. Every HTLC no matter how big, if it is above the dust threshold, can end up killing your channel.

So we have a non-proportional risk. Do we have a proportional risk?

Yes every forwarded payment, if you are not timely, you may end up forwarding but not receiving the incoming payment. That is proportional.

So we have two kinds of risk, one proportional and one not proportional. That’s the reason why this is in but no one has an answer how to use it because most of the users are operating at a loss.

I wouldn’t say that is the reason it is in. I was there, it was the simplest formula we could throw on a whiteboard, linear. It has an explanation that is sensible in the aftermath.

The way I understand the base fee is to cover the non-proportional part of the risk, somebody has to decide how big this or a plugin decides in certain circumstances.

There are good points on both sides, I just wanted to bring it up once more.

I won’t block it.

If I understand this right, the risk goes up with the number of inflight HTLCs that you have open at any time. Would an optimal solution have a dynamic minimum base fee? Gossip protocol aside, would that the ideal solution. You can dynamically set it depending on how close your channel is.

It is slow because we purposefully slow gossip down because we want to prevent flooding but also prevent people from successfully leaking all of their channel balances. They can but now it is deferred some time and it is randomized.

But the cost to the first HTLC having a zero base fee is much less than as you approach maxing out…

No we can’t make it that dynamic because that would leak… We have to have a fixed proportional fee and a fixed base fee, otherwise we would have to communicate to the outside “You paid too little or too much because you weren’t the first HTLC”. That’s leaking that there is another payment going through this node. At least for the risk of closure it should be independent. Probably the base fee should be the same for all HTLCs anyway. Also because they have overlapping lifetimes but they don’t match exactly. This might be the first one, suddenly you only have this one but it came second so you gave it the lower base fee.

Losing the channel or closing the channel is the risk of making a possibly large or costly onchain transaction but there is the opportunity cost of having a large channel open and that liquidity moving. That is entirely covered by the proportional fee, the base fee has no role in that. The base fee is almost just like an anti-spam measure which doesn’t make sense if your min HTLC is set properly.

When a channel gets closed because there is a HTLC attached to it you have the onchain fees which are fixed no matter the size of the HTLCs attached. A zero base fee in my mind was always there to pay for the onchain fees in case of an emergency with a cumulative part through the proportional fees. But it is hard to gauge the risk of forwarding a HTLC and therefore coming up with a good base fee.

