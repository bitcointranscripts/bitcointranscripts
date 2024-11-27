---
title: c-lightning developer call
transcript_by: Michael Folkson
tags:
  - lightning
  - c-lightning
date: 2022-03-07
---
Name: c-lightning developer call

Topic: Various topics

Location: Jitsi online

Video: No video posted online

The conversation has been anonymized by default to protect the identities of the participants. Those who have expressed a preference for their comments to be attributed are attributed. If you were a participant and would like your comments to be attributed please get in touch.


# Minisketch and gossip spam

I’ve been working on the multi channel connect stuff, trying to not get distracted by Tether talk and other stuff like that.

It was an awesome [write up](https://twitter.com/rusty_twit/status/1500606585403768832?s=20&t=eXvYFs__TkNA81w7D-Al3Q). I enjoyed it.

I wrote it up and then I thought do I really want to post this? I don’t really want to interact with people over this. I just wanted to drop it and run. My thinking was possibly worth exposing it, I don’t know if anyone cares. Nobody should care. Rene kept bugging me and poking the bear.

I’m still working on Minisketch stuff, I think I have the encoding figured out. I have a draft BOLT 7 update documenting what I’m doing there. Rusty shared an issue on GitHub, I was digging into the logs a little bit, I started logging some of the gossip I was receiving. I think the issue stemmed from node announcements not propagating. I was also looking into in general how often do we filter spam gossip. I was surprised, I parsed the logs and it looks like over a 24 hour period that number is something like 2,100. I’ve gathered a bit more data since I started doing that, I haven’t seen how variable it is. It looks like there is about 2,100 unique channels that we maybe out of date on gossip at any point in time simply because they’ve exceeded their allocated number of updates recently. I guess that doesn’t necessarily mean a lot to the traditional gossip mechanism but in terms of integrating Minisketch, definitely going to have to tighten up the rules around rejection of too frequent updates.

Are those 2,100 updates or 2,100 separate channels?

2,100 separate channels. It was 6,400 separate updates. I filtered those for redundancy and it was down to 4,000. It was 2,100 unique channels over a 1 day period. We are allocating tokens right now, you get one new update per day. I’m not sure that we’d have to synchronize with the other implementations in terms of updates in general. If we are trying to coordinate a Minisketch that will be something we’ll have to discuss, tighten up the spec.

I just merged a [PR](https://github.com/ElementsProject/lightning/pull/5068) that increases that number to 2 a day. Apparently there are LND nodes that are going down for 20 minutes to compact the databases every day causing 2 updates. We now allow 2 updates, that was the simplest fix.

I was a little surprised. We actually propagate the gossip regardless of the frequency. It is just for internal usage, updating our own gossip store. It looks like a valid gossip, we’ll still rebroadcast.

No the gossip store is the mechanism by which you rebroadcast. If it doesn’t go in the gossip store it doesn’t get rebroadcast at all.

That was what I thought but I’ll take another look. It wasn’t clear to me.

If it doesn’t go in the gossip store it won’t get rebroadcast, that’s traditionally true. There are a couple of holes in that but generally that’s the case. There’s no other mechanism to send gossip other than direct queries. If we drop it it won’t get transmitted. We know LND has much looser tolerances if any for stopping gossip spam so the level creeps up on the network in general. Allowing twice as much gossip spam is a thing. It is funny to have people complain about the potential bandwidth waste of onion messages when they are not filtering gossip spam which is wasting everyone’s bandwidth today. Somebody, their ISP changed their IP address and they lost a whole heap of channels because their node announcement didn’t propagate. The latest release is a bandaid, it is more aggressive with node announcements. We rebroadcast them at every startup and we refresh them every 24 hours. New timestamp, even if it is the same information. Part of the reason is that it is really hard to tell, if you are missing node announcements you can’t tell because they are optional. You can see the whole graph but you can’t see the node announcements. We have some heuristics to try to figure out if we are missing some and then go back and ask for more. But obviously across the whole network that’s not working all that well. For the moment we are going to be more aggressive with gossiping node announcements. In the long term things like the Minisketch gossip reconciliation should fix this. You will get a complete set of your matching peers. That’s a longer term thing hence the bandaid for the next release.

# Personal updates

I spent the last week in London. Before that I mentioned to implement the RPC methods, hooks and subscription interfaces for cln-plugin. That took a bit longer because I wanted to make them async/await which in Rust are really complicated types. That took quite a while to dig into but I am really happy now that we can also call the RPC which is async/await from inside one of these methods and hooks and notification handlers. That completes the scaffolding for cln-plugin and we can finally get it rolling. An additional issue that I had was that some of Rust’s internals triggers Valgrind. I had to figure out how to add suppressions for Valgrind inside of Rust which took me down a weird path. I wanted to make them minimal instead of just copy, pasting whatever Valgrind spat out at the end of the run. That took a bit longer. In London there was Core Dev and then we had Advancing Bitcoin, both excellent venues. We looked a bit into stuff like the RBF pinning attacks. We made some progress there though we will have to discuss this stuff with the wider community because there are no decisions being taken at Core Dev when there are people that might not join. There was general support for the [idea](https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-March/020095.html) of separating the denial of service part out of the RBF rules. This is the only reason why [Rule 3](https://github.com/bitcoin/bips/blob/master/bip-0125.mediawiki#implementation-details) is in there. That is hopefully something that we can address eventually. Funnily enough one of the proposals was the staggered broadcast again which we introduced for denial of service in Lightning all of these years ago and we seem to be quite happy with it. Even though we add these tokens for replacements. Other than that I’ve mostly been working on Greenlight stuff, backporting a couple of things namely for the gRPC interface. We now have automatically generated mTLS certificates. If you use gRPC you can use mutual authentication between server and client. That was a nice piece of code, it works quite nicely. If you don’t have the certificates it will generate them, very similar to what LND does at first start. It generates a couple of certificates that you can copy, paste to wherever you want to use them and end up with a secure connection.

I have a drive by bug report. Every so often I get changes to the Rust generated protofiles. Randomly it adds stuff and I’m like “Nothing changed”. I’m not quite sure whether there is a Heisen-bug in the generator or something. Next time it happens I’ll take a look. I `git clean` and then I `make` again and it is all happy.

I saw one enum being generated which was new. I’ll look into it.

As I jump back and forth on my patch series sometimes I do a `make` and I get Rust stuff.

I was very happy to see that enum pop up. I was like “Somebody changed the JSON schema files and my code worked”. But apparently it is a Heisen-enum.

There may be. I am not changing those files and it seemed to jump out every so often. Be aware that there may be a bug coming down when I’ve got some details.

On the RBF stuff you said you take the DoS RBF rule out. Does that just mean rather than having whatever the five rules were we are splitting them up now so there’s denial of service rules, maximization of transaction fee rules. Is that what you mean when you say split up? We are thinking about them in completely separate spheres now rather than having a bunch of RBF rules that are there for different purposes.

None of this is final, this is going to be discussed in public and probably somebody will come along and say this is a stupid idea. But the general idea is that currently RBF rules attempt to cover multiple facets. One being denial of service attacks, one being optimization for block composition for miners. That creates this multidimensional problem where we have one hammer but two different instruments we’d like to hit with it. Either we hit one completely or we do something in the middle or we hit the other completely. By realizing that these are completely different contexts we can now go back and say “Do we have something else that might be usable for the anti DoS mechanism. There were quite a few proposals, some of them involving our position in the mempool which kind of isn’t optimal because that’s not feasible for light clients. Some of them were saying “Let’s rate limit how much traffic we can generate by an attacker”. Effectively what we want to prevent in an attacker attempting to DoS the network is not the individual connection but we want to prevent an attacker from being able to inject a packet and have that spread in the wider network giving us this quadratic blowup from a single packet being sent to n squared packets being sent around the network. One solution would be to rate limit what an attacker can inject into the network. We’d still be kind of quadratic but we’d have a very low constant factor in front of it. The other one would be to give it a time delay as to what an attacker can forward. What interests me out of all of this is to destroy the confidence of an attacker that he successfully pinned a transaction. By adding delays, by rate limiting and by delaying how quickly he can infect the entire network with his pinned transaction we might get some of the benign transactions. One silly proposal that I made was what happens if all the nodes drop 50 percent of their transactions every minute or so. That means you drop away all of these transactions, the sum of them might have been pinned so these slots are now free again for the replacement transaction itself. It is a silly proposal but it would achieve the effect of removing the certainty for an attacker, whether they pinned or not a transaction. There are more efficient ways to do that obviously.

Light clients and RBF doesn’t make sense anyway, they don’t have a mempool, they can’t validate things so you have to ignore them.

# Mobile client for c-lightning

As some of you may have heard I have been working on the first [mobile client](https://jb55.com/lnlink/) for c-lightning. I wish I could say that I’ve had more issues but it has been pretty reliable. I’ll give one example. I’ve got [BOLT 12 support](https://twitter.com/jb55/status/1499270260595167232?s=20&t=P0oZSqLPywawthPrZ-wwZg) working so you can tip and it will do a payment. This is just calling `pay` and it works. The only issue I had was Commando, it seems to block. If I’m doing a long payment it will prevent any other request from happening so the app kind of bugs out. I’ve had to set the retry limit to 30 seconds instead of 60 seconds. Maybe even lower, 15 seconds. Usability wise, I don’t know if you’d want to wait a minute on your phone to do a transaction and then block the connection for 60 seconds. Other than that it has been super stable. Pretty impressed with how well it is working.

I am pretty sure I can fix that, I just have to make the command async.

I noticed there was an async PR for plugins from like 2019. You just need to add an async to the command hook. Another thing that came up with runes is this idea, we are restricted on if it starts with `list` or `get`, the read only runes. This is specific to crazy people who want to give me read only access to their node. If we ever introduce a `list` or `get` method that is sensitive in future we don’t have a way of revoking runes right now. I have been working on a way to change the master secret on runes, just revoke them all.

We do have a way to revoke them, they have a unique ID so you can go through and revoke them without having to change the whole master secret as well. It is not implemented but you can blacklist them individually. We made a mistake because there are a couple of `list` commands that are sensitive and now are read only.

Like datastore.

Yeah, `list datastore`, that’s got all the secrets in it, that would be dumb. We may end up doing something like a whitelist rather than a blacklist.

I was thinking maybe we should encourage people, if you are going to make a read only rune just do it for specific methods. Not a blanket read only.

This is true. Or have some explicit differentiation. We could have a plugin that wraps commands. There are ways. It is good to see runes and commando being used in the wild. It is what it is intended for.

I’m pretty happy with it other than that blocking issue.

Have you filed a bug?

I have an [issue](https://github.com/lightningd/plugins/issues/347) open on the plugin repo right now. If you want to try it out on the Testflight go to <https://jb55.com/lnlink/>. I need more testers.

# Personal updates (cont.)

As you mentioned earlier I did the [second part](https://github.com/ElementsProject/lightning/pull/5052) of the remote IP address discovery which implements the most basic algorithm I could come up with. It just tries to get the confirmation from two nodes we have a channel with, two different channels. If they both report the same IPv4 or IPv6 address we assume it is a default port and we send node announcements, that works. Rusty did some review, there are some issues with the code. The question I had was do we want a config switch? Or don’t we?

I don’t think so. It is best effort as you pointed out in your PR. Worst case we advertise something that is bogus.

If we had a config switch obviously we wouldn’t create node announcements that wouldn’t be usable because not all of the people will be able to open their router board. Then we just have an additional announced address that is not usable which changes over time. That’t the trade-off there. If we suppress it, we don’t have it, it makes it slightly easier for people to figure out. Maybe it depends on the documentation we’ll add later when we move the experimental.

If it was going to be an option it would have to be a negative option. One thing worth checking is if somebody is trying to run a Tor only node they must not advertise this and stuff like that.

That’s a good point.

You might want to suppress it by default if they are advertising anything explicitly. And have it only if there is no other advertisement. That would be fairly safe, it doesn’t make things worse. Assuming they are not forcing through a proxy. If they turn proxy for everything on, that’s the setting for Tor, you should not tell them your IP address. How’s the spec going? It can’t be moved out of experimental until the spec is finalized.

It is already [merged](https://github.com/lightning/bolts/pull/917).

Then take it off experimental, put it in.

I can do that. We didn’t have a release with it.

Experimental for stuff that would violate spec or that we can’t do because of spec concerns. That may change. Once it is in the spec it should not be experimental unless we are really terrified it is going to do something horrible to people. That’s fine.

The DNS is still [not merged](https://github.com/lightning/bolts/pull/911) in the spec. There was another implementation that was working on it so maybe we can get this in the spec soonish.

We had a great meeting in Istanbul before London. We had two LND developers, Carla and Oliver, spoke about BOLT 12 in a PR review club fashion which was great. Spoke about the onion messages, spam protection. Paid for a lot of Lightning beers with my c-lightning node. It is a node behind Tor, it was connected through a VPN to my phone with the new Zeus wallet. It was a release candidate then, now the 0.6 release is out, I can recommend. The Raspiblitz 1.7.2 has been so far a good update, we were focusing on stability improvements. We have a connection menu that exposes some endpoints for connecting Spark wallet, Sparko and the Zeus wallet through different interfaces: the c-lightning REST interface, the Spark wallet interface. We would be interested in a facilitated connection towards this iPhone wallet. I would be very happy to assist. If you give us a spec then we just put it into the menu.

# Bookkeeper plugin

I have been working on a [plugin](https://github.com/ElementsProject/lightning/pull/5071) that I’m now calling the bookkeeper plugin which will help you with your Lightning bookkeeping. I pushed up a PR late night Friday, thanks Rusty for getting some of the prerequisites in. I am currently working through the little things that CI wants me to do. Hoping to get that done by end of day today. The bookkeeping stuff, there are a couple of commands in it that I’m pretty excited about but I’m hoping people will take some time to look at them and run on their node, give me some feedback about what other information they want to have. The novel thing with the bookkeeper is the level of data collection that it is doing. There is probably a little more data we could add. For example when you pay an invoice there’s the possibility for us to write down how much of that invoice goes to fees versus to the actual invoice that you are paying and collect data on that. It is not something we are doing currently. The idea is this will give you a really easy way to print out all the events on your node that made you money, lost you money, where you spent your money, where you earned money at a millisat level of resolution. It is a big PR, a lot of the PR is just printing out different ways of viewing the data, there is a lot of data there now. Hopefully other people will run it and say “Wouldn’t it be great if we also had this view?” It is definitely going to make the on disk data usage a little bit higher than it has been. We are now saving a copy of stuff. I don’t really have a good answer of how to fix that. There is definitely a way you can rollup events that have passed a long time in the past, you checkmark things. Events that are 3 years old you probably don’t need the exact data on, that’s future work. It also keeps track of when a channel closes and has been resolved onchain. It is possible to go and rollup all the channels that you’ve already closed and have been resolved onchain, you already have the data for, after however many blocks e.g. 1000 blocks. There are opportunities for making the data less compact as time goes on.

This week I am going to work on some outstanding bugs and cleanups I need to do in the funder plugin, the way it handles PSBTs needs to be fixed up a little bit. I think I was going to look at making our RBF bump for v2 channels easier to use. Z-man has submitted a big request for that. That’s probably going to be what I’m working on this week unless anything else pops up.

With the bookkeeper plugin I wonder if we mark the APIs unstable for one release.

Right now it automatically turns on and starts running. Maybe there’s a set of plugins I could add it to that’s optional to opt into. You probably want the data but maybe we should make it opt into the data.

My general philosophy with these things is more switches is just confusing. As a general rule the only button should be install and it should just work. It is the same with data collection. I generally prefer to over collect data and then have tools to reduce it or heuristics to reduce it later than not have the data and wonder what the hell happened. The data problem tends to be proportional, as long as it is not ridiculous, people running really big nodes who have data problems either have serious storage or have ways of managing it and prepared to go to that effort. People running small nodes don’t have a data problem. My general emphasis is to store all the data, storage is cheap. At some point if you are running a serious node you’ll need serious hardware or we need to do some maintenance. I think your instinct that you can throw away data later is probably the correct one. I am excited about having it but I wonder if we want to go through a bit of a caveat on the APIs to start with and not guarantee backward compatibility. We generally do and that may be painful to add later if you decide to redo it. Ideally you won’t but it is nice to have the asterisk there.

At least for one release.

This is the first release. Give us feedback and try to keep a little bit of wriggle room.

What’s the best way to indicate on the APIs? Add experimental, exp before the actual thing and then delete it later?

That is almost worse. You’ve done quite a lot of API work so I would say it is unlikely you’re going to do a major change. Ideally of course you won’t or it will be backwards compatible, a new annotation or something. That’s the plan but it is not the promise. There’s a difference between those two. Maybe I’m backing out of this commitment. It is hard to indicate this in a way that isn’t going to hurt people. In the release notes I’ll make sure it is clear this is a new thing, please play around with it but it will be in anger next release. We are still in the data gathering phase maybe. I look forward to reviewing that PR. It is big so I’ve been waiting for you to rebase it  before I review it multiple times. It is a lot of code.

vincenzopalazzo: Last week I was also in London. The last two weeks I spent some time on lnprototest, I’m adding a new test for cooperative closing. In the last spec meeting we discussed the spec being underspecified in some way. It is good to have some spec tests from this side. This resulted in me finding a bug in lnprototest. When a test fails we don’t stop Bitcoin Core. After a different failure my machine blew up off the Bitcoin Core daemon. I fixed that, please take a look in case I’ve made a mistake. This week I will merge it and continue my work on the integration testing. I am also [working on](https://github.com/ElementsProject/lightning/pull/5022) splitting the `listpeers` command. I found a mistake in my understanding. The `listpeers` command uses the intersection between the gossip map and the peer that we are connected with. I am assuming that `listpeers` shows all the network and this is wrong. I need to refactor the logic that I proposed in the pull request.

# Reckless plugin manager

I talked in London with Antoine about the [Reckless](https://github.com/darosior/reckless) plugin manager. I propose to migrate this Reckless plugin to Rust because now we have Rust inside c-lightning. I will write a mail on the mailing list on the idea. The idea is splitting the Reckless plugin into three different binaries. One is the core library that makes the update of the plugin. Also I want Reckless to be a plugin of c-lightning but also a separate binary like Lightning tools. You can instantiate a new plugin, if you want to write a plugin in Python you can call it the language and the name of the plugin. It is a big project but I have some ideas.

I have some ideas on Reckless. It has been on my to do list as well since 2019. I believe that yes, it needs to be a separate binary. I would tend towards Python because it is going to have to deal with filesystem stuff. You can do that in C, you can do it in Rust but you could also just do it in Python. It also needs to do web stuff to obtain plugins and stuff like that. It is a pretty Python-y kind of problem and you have already got to have Python in tree. But I have no problem with a Rust dependency, that works just as well.

vincenzopalazzo: With Rust there is this cargo environment that gives you the possibility to avoid the circular dependency that we have in Python. We have pyln, proto and the BOLTs that are dependent on each other like lnprototest. With Rust we get Cargo and the workspace which takes care all of the stuff. With Python the end user needs to install all the dependencies and with Reckless I think we know the dependencies are different and we can have some resolution error. From my point of view Rust is the safe way to go. Maybe there is a little bit more work from our side but we can avoid the user having trouble with Python dependencies.

Whatever it does it does need to be standalone, it does need to be minimal dependency wise. Ideally you want it shipped with c-lightning, it is installed like anything else. The plugin ecosystem is very rich, I feel like it is badly served because it is so hard to install plugins. It should have a Reckless install whatever. And also manage them, activate them, deactivate them, upgrade them in particular is important, stuff like that. It is basically a shell tool, I would have written it in shell 5 years ago. It basically just manipulates the filesystem and runs a few commands to restart things. It doesn’t need to be particularly sophisticated, it does need to do some web stuff and some discovery stuff but that is about it. It is not c-lightning specific really. There are a couple of things it needs to do with c-lightning but it is a separate tool that pokes c-lightning regularly. It doesn’t really matter. The important thing is is that it is self contained, it just works. I would like to ship it by default. It becomes standard for people to say “Just reckless install blah”. It does it, it starts the plugin, does everything.

vincenzopalazzo: I think the most important thing is to introduce inside the plugin ecosystem a manifest of the plugin like a `npm install`. We can have different languages working in different ways. For instance in Java you need to create a bash script. In some other language you need to create other stuff. With a manifest we can have this second layer that you can work with. This is the first thing I will do, start to think about how to make a good manifest. The second thing, how to build a GitHub page with this manifest, query the GitHub page and get the list of plugins, a fake API. All with GitHub and maybe we can make a fake repository system without a server.

That’s not a problem. Thinking about different types of plugins, we already have two types in the plugin repository and we do test them in isolation. We have some code that already does create virtual environments that are populated by Poetry or by pip.  Adding more languages is all down to detecting which environments are present. It pretty much boils down to how well we structure the manifest, maybe we can merge them through a CI job and push them onto the web where they can be grabbed from the clients.

I’m happy with languages like Python, Rust, Python, Go. Make it a standard, if you are going to write a plugin it will be done like this. It will be configure, make etc. You can hard code things as much as you want. The other thing that I think is important, versioning is obviously important so you can upgrade. Upgrade maintenance is important. And dependencies between them. We are seeing more stuff needing Commando for example. If you have that, install this. They are the key issues. Just removing the maintenance burden of having to do this stuff manually. Discovery is nice but I don’t think it is critical. Being able to search for plugins, it is much easier for us to produce a web page that highlights plugins and plugin of the week rather than putting in the tooling.

# Q&A

I wanted to mention one thing about [Commando](https://github.com/lightningd/plugins/tree/master/commando). I noticed there was an experimental web socket. I know Aditya was working on web socket stuff. I was going to try compiling my lnsocket library with Emscripten. It compiles raw socket code to web sockets. How well tested is that? Is there any test code for people using web sockets?

It really works. It is weird but it does work. You can tunnel the whole thing over web sockets. Your problem is going to be in the browser, you may or may not be able to connect to an unencrypted web socket. You may need a proxy or you need a certificate which is the whole point to avoid.

You need a HTTPS connection?

Yeah. This is really annoying. I am probably going to run on bootstrap.bolt12.org, at some point there will be a proxy. You connect to that proxy because that’s got the certificate and then you tell it where you want to go. It means I can snoop your traffic but it is encrypted.

You can’t reverse proxy a Lightning connection because there is no SNI or anything to key off of.

Lightning is a parallel infrastructure so there isn’t any real overlap. Providing proxies is a fairly straightforward thing to do. You can use Lightning to pay for them. There’s a possibility there eventually.

The HTTPS thing is really unfortunate. I am just running my node off my home connection. I don’t have a web server and I was thinking of writing a plugin that lists all the payments to an offer. It would have been cool to do that with just lnsocket and Javascript code. But maybe I’ll just bite the bullet and run a proxy or something.

Once we have a public proxy you can do it. That’s the aim.

What was the point about not having SNI?

This is something Warren Togami was talking about, in terms of hiding your IP. Imagine if you had a privacy proxy where you could have an IP that is in front of your actual node. I was trying to think of a way to do that. I think the only way would be if you had a SNI type system where you could reverse proxy the Lightning connection. I don’t think it is possible.

From a browser you should be able to.

This is separate from web browser.

We are actually trying to build a SNI based gRPC proxy in front of Greenlight.

It would work for TLS but I was trying directly to the Lightning Network.

Maybe ngrok works? You can do pure TCP connections over ngrok, that might be an option.

If you have one IP that could potentially reverse proxy to multiple Lightning nodes, you would identify SNI based on the pubkey or something. That is what I was thinking, I didn’t think there was a way to do it in the protocol.

