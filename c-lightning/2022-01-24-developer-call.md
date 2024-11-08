---
title: c-lightning developer call
transcript_by: Michael Folkson
tags:
  - lightning
  - c-lightning
date: 2022-01-24
---
Name: c-lightning developer call

Topic: Various topics

Location: Jitsi online

Video: No video posted online

The conversation has been anonymized by default to protect the identities of the participants. Those who have expressed a preference for their comments to be attributed are attributed. If you were a participant and would like your comments to be attributed please get in touch.

# Individual updates

Still working on the cln stuff. cln is basically the Rust libraries that I am building to interact with c-lightning and which will become the basis for the gRPC interface. Last week I got the mTLS certificates generated. So whenever you start up your node the plugin will start up with it. It will start up the gRPC plugin and it will then look if there are TLS certificates, if there aren’t it will generate them. Then you can use those TLS certificates in an authenticated and encrypted way with a gRPC plugin which will then relay everything back to the JSON-RPC. A long story of saying we are getting a networked RPC interface which should allow us to have a way better mechanism of interacting with c-lightning in the future. That is something a lot of people have asked for for a long time. We are finally going to deliver. It is also going to be the first Rust part in the repository. I had to take a bit of extra care in how we integrate that. Rust for now is totally optional. It will autoconfigure depending on whether you have the tooling available or not. Don’t worry, it isn’t going to break. But I will be cutting the releases with the plugin. If you download a binary release it will have the plugin ready and already setup. You will profit from this even if you don’t have the Rust compiler. I finished the mapping there, I finished the TLS stuff, I am currently working out some of the smaller parts of the plugin interface namely adding options and adding custom RPC methods. Those are mostly to configure the gRPC interface, where should it listen and what other options should we use. Besides that I also got into a fight with the OP_CTV author with respect to the ANYPREVOUT stuff. If you want to ask me about ANYPREVOUT feel free but I will not go into too much detail because it gets kind of niche pretty quickly. Jeremy Rubin has started making direct comparisons whereas I think that they mostly serve different goals and they are optimized for different things. They are definitely not competing and they can co-exist quite nicely.

We are grinding towards the multi channel stuff. It doesn’t help that my build machine is out. I’ve had to bounce off CI a lot and getting stupid errors. There are some nice cleanups in there. Addressing flakes as per normal. I haven’t done the actual part where I make it multi channel yet. Originally I wrote this whole series and I spent way too long debugging. I jumped straight to the end. I have learned to be more cautious now. I do have everything going through connectd now in the second series. connectd does all the work. The third part is to have connectd hold clients… At the moment when someone connects we throw them a fresh openingd, the openingd sits there and chats to them until they try to do something interesting. The idea is that connectd will do that work and connectd will chat until you really do have something interesting to say or wants to open a channel with you. Then we’ll fire off openingd. This is a little bit of a scalability win, it also changes a lot of our internal logic and should make it simpler in some ways. It should be fairly simple once I’ve got that piece to have multiple channel support. Each daemon will only see messages that are particularly relevant to its channel and will never see anything else. It has been a longer arc to get there than I had hoped. Other than that babysitting PRs. It looks like we are probably still a month from release. We are probably looking February something at this point unfortunately.

# Using Minisketch for gossip reconciliation

I’m doing a lot of learning still, I’m working on set reconciliation. I played around with testing out this library cross platform using the Raspberry Pi 4 to compare the performance between architectures with x86 versus ARM. It looks a lot better than I thought and I think that’s probably due to the 64 bit OS. This is only recently available. Still running some numbers there. I chatted with Rusty about how we could potentially use this to reduce bandwidth on the gossip protocol. It is looking promising but a lot left to do. Hopefully I will have more data to present in future meetings.

The idea was to use Minisketch for gossip reconciliation, send the sets back and forth and know what differences we need to send. That’s the high level idea. There is a lot of devil in the details. I have a draft thing from over two years ago that I had abandoned. I gave him all the pieces to reassemble. I don’t know if that was helpful or not.

It is. There is a lot going on. It was more than just early draft. When there are several peers there is a lot of duplicity and passing around every single gossip packet. The general idea is that you can get on a somewhat regular schedule with your peers. You can compile this sketch of a set of recent gossip updates. It compresses down to virtually just the size of anything you are missing. You can’t tell whether Sketch A or Sketch B, which node has the missing data but the difference is the total size of the sketch once it is transmitted. Once you are gossiping with many peers you can reduce much of that duplicated data. Essentially each gossip packet we are creating a signature for. All we really know is this is the exact piece of gossip I’m missing. Once you send your sketch to the peer and they can see the signatures of the gossip you are missing it is up to them to find those latest gossip updates and send you each one in return with all of the associated data. It is an amazing library. It is a lot of fun digging into. It blows my mind a little bit.

At the moment what we do is we have this rough heuristic where we pick three or four peers, some random number I chose, and we chat to those. We have a thing called a Seeker that picks some peers at random and goes “I will use you for gossip and suppress everyone else just so we don’t gossip with everyone”. But this would vastly simplify that logic. We would just send these sketches once every 60 seconds or so. Our Minisketches can be one network packet or less. They are really cheap and we only have to maintain one sketch. It has some really nice properties.

Based on the initial measurements that I have taken, one packet’s worth of data if we expand the sketch to the maximum size of that packet, it should the vast majority of the time cover a full 60 seconds worth of data. It does vary a bit. I am sure there will be sometimes when traffic picks up and maybe we fall back to other modes. For bandwidth constrained nodes it would be a major win.

# Individual updates (cont.)

I did the fixes of the review from the remote address branch. It is on master, mergeable. That’s it, I didn’t do much more.

Cool, I should review it.

I think it has been merged into the RFC last meeting already. It is just logging this information and I think I will do a follow up PR for using that information.

# Accounting plugin

I’ve been working on accounting stuff, I pushed up a couple of PRs late Friday, prerequisite work for the accounting plugin. One of them was little nits I found on the way to getting the plugin done. The other one was pulling the entire database code out into a separate directory. Right now all the database code is embedded inside of this wallet structure. I have put up a PR that pulls a lot of it out. There is one more commit that I want to add to that. There are some code files that I duplicated but I think we can add them to the generators as a generated file. That’s up, it is a huge thing, I should have probably broken it into more pieces but I didn’t. On the accounting side I’ve got it adjusting all the data now which is exciting. I started working on doing some reports and I realized that there is a couple of places that were missing information from c-lightning that would be really useful to have. One example, when you do a withdrawal we don’t actually report that you are withdrawing money to an external account. We show that you spend that output… Using UTXOs for accounting stuff is very difficult. To make it complete I need to add an extra event “Hey, this output went to an external account”. I am working on adding a new coin movement. We already have some coin movements for channel stuff that helps you tell when your outputs go to an external, your peer in the channel case. For these cases we should probably make a note that you made a withdrawal here. It also helps with the way that we calculate onchain fees in the accounting plugin. We use UTXOs as our base accounting thing. Every time a new UTXO comes in for a transaction I will recalculate what the onchain fees were as we get information. Not having this event that notates that money was sent to an outbound account, it ends up as onchain fees. I’m working on re-piping all that. I think I am going to flag it on the PSBT that you send to `sendpsbt`. Part of the difficulty with it is that we use plugins to do withdrawals. A plugin can’t send a notification, we’d have to pipe a notification into c-lightning and then c-lightning would have to retransmit it. The easier way is when we do a `sendpsbt` we’ll just mark which outputs are coming from that plugin and going somewhere else. When we get that we’ll notify on it. All the other UTXOs that we account for we wait until we see them in the chain before we announce on. This is going to be the only UTXO creation that happens when it enters the mempool. Once it has successfully entered the mempool we are emitting it. This unfortunately means we don’t have finality on those, I can add some stuff not to count those as final until we get the txid that sees the UTXOs that we were spending. Unfortunately it makes the accounting plugin a little more complicated but it is fine. The point of the accounting plugin is to be complicated and smooth over these edges so the data you get out looks nice and neat.

Didn’t we just recently add custom notifications to plugins as well?

Yes. I could have used a custom notification but I decided it would be more generic if I added it as a flag to the PSBT that you send to `sendpsbt`. If any other plugin started to do it instead of having to notify a custom plugin they just set a flag on the PSBT outputs.

That makes total sense. I introduced plugin notifications for the pay plugin which had a very similar issue. I like your reverse engineering. The problem is the pay plugin doesn’t use PSBTs so I don’t have a place where I can stash that information.

I did think about using custom notifications. The PSBTs have a known field so you can add custom fields to inputs and outputs, extra tags and stuff. We just use that. We were using that already for dual funding. I already have some code to add a little unknown thing.

They are supposed to be preserved. Even if you use an external signer they should stay through the loop so you can have those annotations on your outputs. The other way to do it would be to annotate the other way and say “This is going to a channel”. But I think it is better to annotate and say “This is going externally”.

The channel ones you don’t have to annotate because the channel ones you see get deposited. The channel deposits we see are a channel open. I can track all of that. When we make outputs that are from our funds then I need to see all of those.

That makes sense. The subtractive case is it is somebody else’s outputs that are mixed through or something, these would be unannotated I guess so ignore those.

That would happen on dual funding opens or if we do splices. Those would pass through silently.

Which is why you are seeing them as giant fees.

For splicing it should be ok as long as we account for every output that we created and every input that we did our fee calculations will be perfect in terms of only accounting for the fee that we paid for.

I suspect there may be some corner cases. People actually start to use accounting, looking at it and going “This is weird”. Whether we annotate things further or file some edges off will be interesting.

# Plugins interacting with other plugins

This notifications problem seems like it would be a common one across plugins. If plugins are requiring other plugins or interacting with other plugins is this going to be a common thing? Does the custom notifications thing solve this or is that just one approach?

It is definitely one mechanism for us to have inter plugin communication. It is not the only one. But it is the one that is pushed based. You have a real time way of interacting with some other parts of the system. The other ones are basically the [datastore](https://github.com/lightningd/plugins/tree/master/datastore) where you can deposit some information and then retrieve from another location. Those are the two that are dedicated to communicating information between plugins.

The other way of doing it is you can have a command in this plugin. That’s only one-to-one generally because you can’t both implement a command. “This plugin should always call this command” is a way of doing it but it is pretty ugly.

You can also have RPC commands intercepting commands from other plugins which can be really strange. The canonical use case for that would be an authentication mechanism for a RPC that is entering the system through another plugin. You could have a web frontend plugin that receives incoming requests and then forwards these requests unauthenticated to the JSON-RPC. Since there is a second plugin using a RPC command intercepting everything it can reject or accept only authenticated messages. If for example you have a cookie inside of your JSON-RPC request that could be checked by a second plugin. You can keep RPC and authentication orthogonal to each other. Not that anybody has ever needed that flexibility but we have it.

I thought about doing it for [Commando](https://github.com/lightningd/plugins/tree/master/commando) but I decided no. As it comes in it validates it and sends it on. It doesn’t have a second plugin that does generic authentication. If we did we would need hook ordering. CLBOSS for example intercepts commands. You want to get to it before CLBOSS does. You are opening that can of worms about hook ordering.

That and the authentication plugin crashing but not taking the node down with it can be really weird.

I think authentication would have to be an important plugin. Presumably it is important, otherwise you wouldn’t have it. User configuration and “Let’s comment out this line in the config and not start it” or something like that. That is always a possibility that I don’t like.

Commando works quite well doing inline authentication but if you wanted a more generic rune authentication as has been discussed we might want to use that mechanism.

# Individual updates (cont.)

vincenzopalazzo: I have worked on a [compilation error](https://github.com/ElementsProject/lightning/pull/4987) on c-lightning about Alpine. The solution I came up with was if we are in the test environment we store in this process that we use in the CLI. If we are in the test environment this is the test read function, otherwise it is the read function that we have. This way we can compile on Alpine without any error. With another pull request I am integrating the compilation test with Docker Compose with Alpine. Last week I released the first version of my Dart wrapper around c-lightning. This can be very useful now we have the gRPC interface because with Dart it is possible to make a cross compiled UI using Flutter. Hopefully we can give the opportunity to use this library to interact in an isolated way with c-lightning. We have different ways to talk with c-lightning: the REST API, UNIX socket and now gRPC. I would like to implement a GraphQL API when Christian finishes the Rust plugin. One thing we discussed two weeks ago, taking a data model description and translate this data model to the source code, this can be useful to maintain all the wrappers that we have in c-lightning. Rust, Golang, Java and all the others.

I have never even seen Dart code. I will be interested to take a look when you’ve hooked that together.

vincenzopalazzo: Dart code is a little bit C++ plus Javascript plus some weird stuff.

I’ll try to read it, see what happens.

I had a chat with shesek, he told me he’ll review the PR as soon as he gets the time. This week I’ve had fever, my health dropped harder than Bitcoin this week. I’ve been mostly been going through the documentation of plugins and runes. I’ll try to implement it from tomorrow onwards.

Someone submitted a patch, the version on pip had fallen out of the version of the GitHub so someone submitted a patch to fix the runes code which makes it easier to install from GitHub directly. Other people are obviously looking at runes which is cool. I’ll be interested to see your feedback. It is an interesting experiment. I like them more than macaroons plus the name is shorter.

I have been quite busy extending and implementing a couple of automatic recovery options. That will be the biggest addition to the c-lightning bit as well as the lnd bit. Trying to get people to be able to recover from the seed we provide. This BIP 39 compatible seed they write down when they are generating a wallet in Raspiblitz. There is an automatic rescan which is picked up during running and then switched off for the next restart. There is this cl rescue file which is just a copy of a directory and can be imported from the graphical interface. It is built in a way such that when we get this web UI going we should be able to implement it there as well because all processes are running in the background. There is a Redis database which is caching the system status and taking care of these background processes. That has been a lot of work for rootzoll. More and more users are trying out c-lightning, they like it, they like the simplicity, the speed. Some of them have been going through the recovery things from which I have been trying to pick up what can be improved. For example the `guess_to_remote` function is something that is quite difficult to automate. When users are offline and the peers are force closing channels then that will be picked up automatically as I understand. I documented in detail in our Raspiblitz c-lighting frequently asked questions [page](https://github.com/rootzoll/raspiblitz/blob/v1.7/FAQ.cl.md). You need to look up the node ID and the peer and which address to look for which is not the timelocked one. It involves a lot of testing and restarting and recovering nodes so it is a time consuming process.

Plebnet was mentioned last time. I started a c-lightning node on Plebnet, the same one which is always running the latest master. I started running an explorer for Plebnet. I am trying to get some attention for c-lightning on Plebnet.

This is the playground on Signet?

Yes.

There’s GraphQL which may not make this release because the ambitious person who decided to write GraphQL has bitten off a lot. It was a very ambitious PR and I am having to meet them halfway. I am going to have to do more infrastructure work so that we can fit their things in. They had this vision that we would drop JSON-RPC and just replace it all with GraphQL. That is not going to happen. We are going to have both for a while. I am not going to commit to a GraphQL first approach until we’ve implemented it and seen if people use it. If it becomes a dominant use then we can talk about rewriting all our internal functions to match it. But I’m not going there first. We are going to try to leave as much as possible of the internal code the same. We produce the JSON and do some tricks in the backend to make GraphQL work. But I have to write that code unfortunately. It is great to have such an ambitious PR but for future reference I would never recommend your first PR be “I’m going to rewrite your whole JSON-RPC interface and all the functions”. That would not be my choice. Unfortunately I’ve been cycle bound with this other work so I haven’t had as much time to do that as I would wish.

