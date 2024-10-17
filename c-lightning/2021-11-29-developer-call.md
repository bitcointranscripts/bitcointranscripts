---
title: c-lightning developer call
transcript_by: Michael Folkson
tags:
  - lightning
  - c-lightning
date: 2021-11-29
---
Topic: Various topics

Location: Jitsi online

Date: November 29th 2021

Video: No video posted online

The conversation has been anonymized by default to protect the identities of the participants. Those who have expressed a preference for their comments to be attributed are attributed. If you were a participant and would like your comments to be attributed please get in touch.

# CI problems

I will note we have been having CI problems. We obviously slowly grew to the point where our CI uses too much memory. We’ve been getting OOM killed, the out of memory killer picks one of our processes and kills it. That makes it really hard to complete CI tests. I went through and did a little bit of surgery to reduce the amount of memory that we use by looking at how much memory all of our tests use and taking some of the biggest offenders. Hopefully that now means if you have a PR that has been failing with random stuff and you rebase on master you should be good. I would recommend that. You’ll just get your normal flakes and not these random things dying flakes. That’s been happening for a while but it has been getting worse. Restarting has been less and less effective, eventually it had to be fixed. Hopefully that is gone now. It turns out there is not really good tooling on how to diagnose that stuff now.

# Individual updates

I checked my [PR](https://github.com/ElementsProject/lightning/pull/4900) and it is still failing. It is not really failing, I know it is ok, I was testing it locally, but the CI. I rebased to the current master.

We have at least one other flake that I’m aware of. I will happily babysit that one through.

What number?

4900

It has ACKs, that’s not minor. Something is broken. That is not a flake, that is something real but I will see what it is. One failure could be a flake but multiple failures is an insertion error.

vincenzopalazzo: I think there is a port error inside the gossip test. We also gossip the port number.

I think that’s almost certainly what it is.

One I fixed some time ago and since then I could pass the tests.

There are other gossip changes that happened in the meantime. I think that is what happened. It could be the DNS test that is failing. The DNS test got [merged](https://github.com/ElementsProject/lightning/pull/4829) and I think that has messed up yours.

I am happy it got merged before me because it was being done for a longer time.

What DNS test got merged?

Has that not been merged?

You touched this code but it hasn’t been merged yet.

Almost but not yet.

Strange because the gossip test is clearly wrong. You need to change the test gossip addresses, that is going to fail. It is testing for the old port number, because we are running on regtest it will need to be the new port number. That should be an easy fix. That’s what most of your failures are about. There’s the hsmd code flake that happens every so often but that is not you. You definitely need to fix one of the tests.

We were discussing with Michael (Folkson) that patch and I was explaining to him what the fix means in that tests. I felt that the test is fixed but maybe there is something I did not to do.

If you find out that you need to fix 100 tests then maybe we need to think about changing the Pytest utils. I’m not sure.

This one is just one test. I wrote about it 24 days ago, I was able to pass all the tests.

Maybe something broke in the rebase.

I have not been doing a lot c-lightning. I finalized the DNS stuff, it should be good. There is one thing I noted, not really related to my change, when you run out of known addresses for a node, the try next address loop recursion thing, the CLI command to connect to a ID, it gives you code `41` with an empty error message which is somehow not really helpful. That is implemented in my tests as well, I could change it but didn’t. I think it would raise the same empty error message without DNS as well.

We should fix that. It would be nice to raise an issue and mark it to the milestone. I’ll make sure it gets fixed. It is nice to have that if we tried 3 addresses and it didn’t work.

One other implementation needs to pick up on it so it can be tested and merged. The other thing with the return the remote address is picked up already. I think I will focus on this PR first to get that ready. When I’m done with it, maybe implement something on another implementation.

That would be cool. It would be nice if we could skip experimental altogether and go straight in. It is tempting to skip experimental, every time we do that we get into problems. We should do it by the book. It is an annoying two step, you implement it and then you hack it out and hack it back in again. A second implementation, technically you can’t implement it, it has to be an independent implementation so you do have to get someone else to do it.

I thought eclair had implemented this? Wasn’t it briefly discussed at the [protocol meeting](https://btctranscripts.com/lightning-specification/2021-11-22-specification-call/#dynamic-dns-support-in-gossip-messages) last week?

Which one?

The DNS support in gossip messages.

Who implemented it?

Eclair.

I will check the corresponding pull request.

You should definitely check. Usually if you check the spec PR they will have referred to it in their PR. You can easily backtrace there. Then you can run interoperability testing.

That’s going to be merged in the spec?

You just have to get the people to ACK on the thing that you have interop tested, it is pretty uncontroversial so it should go straight through.

I think t-bast said he is waiting for some fixes from you.

On the remote IP address, yeah I know.

The other one I have not finished yet. He tested it, it works but it is not good yet.

I’ve been working on accounting stuff, basically rewriting how we do accounting events and onchain. I have got it mostly done. Almost every test in [test_closing.py](https://github.com/ElementsProject/lightning/blob/master/tests/test_closing.py) has an assertion about what the onchain events look like which is pretty exciting. You can make assertions about what onchain transaction trees, output trees should look like which is fun. I have got a huge pile of changes that I need to checkin commits. There are a few more things to do on the event side inside of c-lightning. Then we get to start exciting things on top of it which is the accounting plugin.

I look forward to the accounting plugin, I want pretty graphs, pie charts and things like that so I can find out where I lost all my money.

I don’t think we are going to have graphs at first but soon. I am actually a little worried that shipping accounting, we are going to lose like half of people running c-lightning nodes because they are going to realize where all their money is going. I think shipping accounting stuff is a little bit of a double edged sword. On the other side accounting is really a data collection problem so we are going to have some really good data about money and accounting on your Lightning node. The other thing about it is that once you start collecting data all of a sudden you have metrics so you can figure out better ways to not spend as much money. Hopefully this will lead to more improvements in how we handle onchain funds etc.

It will probably drive anchor outputs, the unilateral close at the moment where we are overpaying on fees….

I don’t know, anchor outputs cost money too.

They do but you can be more aggressive on fee rate.

We’ll see.

Maybe we’ll have the evidence that it is not worth implementing, I don’t know. At the moment we are in calm seas. With low fees everything is easy. It is only when fees spike where it will probably help. The original anchor outputs was really clean and cool but then it got less clean. You’re right, the two extra outputs cost you. We will see.

It is really expensive to be an opener I think we’re going to find out. Maybe this will make dual funding way more attractive because then everyone is going to want to be on the other side of the open.

Maybe. Anyway I look forward to that, that will be very cool.

I visited El Salvador in the past 2 weeks so I’ve been stress testing Raspiblitz onsite, setting up a couple and also my c-lightning node back home was successfully paying Bitcoin Beach wallet, Chivo wallet and other random BTCPays and things like that. I was very happy with that because I only had 8 channels or so. I have a lnd node which was working as well. That was a very good experience. Zeus connected through c-lightning REST was working quite reliably with a VPN. That’s practical experience. Development wise, it was a bit hindered. We are working on a GUI for the Raspiblitz which involves a bit of a Lightning wallet interface with payments, history and invoices to be shown. The c-lightning part is still to be worked out. I was working on infrastructure things, I will go harder on setting up virtual machines and making the Raspiblitz system available to be spun up in a virtual machine environment or just on pure Linux which will be good for dropping more c-lightning nodes as well. Otherwise been on a panel about Lightning privacy with t-bast and was listening to a very good presentation about the same topic from t-bast. I was chatting with him which was really good. I learned a lot. I was also told they are implementing onion messages which is almost ready and moving onto BOLT 12, we’d love to see that.

t-bast’s and generally ACINQ’s focus on privacy has been really good. They are very aware of issues. I listened to that panel as well, it was really good. Did you learn anything surprising in El Salvador? Other than getting to use Lightning? I am very envious.

It was a very nice place to stay, to learn. I was curious to see how people perceive it and whether they take Bitcoin or dollars. People seemed quite happy about what is happening, the ones who know a little about Bitcoin. I didn’t meet anyone who was against or technophobic. Some wanted to buy fuel in dollars because that’s the only thing available in the petrol stations, you need to use dollars. I am still processing. Seeing people using this thing day to day, “I need some dollars for my fuel but if you want to tip me this is my wallet”. They are also happy to try other things out. I think the Bitcoin Beach wallet is the most appropriate thing to use because it works the smoothest, regarding the custody at least you can speak to the people who are looking after your money, it is better than a bank. Also the backup things, for mobile it is even more important. What happens when you lose you phone? With the Bitcoin Beach wallet you register your phone number and then you can get it back. Through the phone number you can get your balance back. Whereas other things you need to upload some file here and there or write down 24 words etc. For day to day usage for groceries that is the way to go. What I was most excited about is speaking about this federated e-cash stuff. Also witnessed some Lightning invoices converted to an audio and going into CB radio. The other side of the building was recording the audio and getting the invoice paid. That was a fun thing, proving you don’t really need internet to do these things.

I definitely feel a trip to El Salvador coming up in my future.

vincenzopalazzo: This week I focused on the [RC1](https://github.com/LNOpenMetrics/go-lnmetrics.reporter/releases/tag/v0.0.4-rc3) of the [LN Open Metrics plugin](https://vincenzopalazzo.medium.com/introduction-to-ln-open-metrics-96a7c859f4e2). I finally achieved an executable and this week I will publish an [email](https://lists.ozlabs.org/pipermail/c-lightning/2021-November/000213.html) to the mailing list to describe how it works. Also on c-lightning I am working on reporting the error code for the c-lightning command when we interact with the CLI. I am refactoring the method to return an error code and pass the error message as an event. Now I need to ACK the Ccan library because there is only one error code and I would like to have a method that returns an exit code or something like that. But I am not very comfortable with the macros inside the Ccan library.

Sorry that’s my code. It is pretty hardcoded to return exits with `1` if something goes wrong. But at the very least we can have a function that overrides that and returns a different exit code instead. Or if you want something more sophisticated so different things return different error codes, we could do that too if we wanted to. Let’s discuss that offline and see if we can come up with something that you like. Excellent, I look forward to reviewing that PR.

Since last time I did have two days downtime, also called giving lectures. I didn’t have quite as much time to work on c-lightning, there is also quite a lot of stuff to do for Greenlight. What I did for c-lightning is to look into backporting Greenlight’s RPC mechanism which is currently gRPC based and MTLS based back into c-lightning. That is part of taking parts of Greenlight and making them open source and reusable through c-lightning. The networked RPC has been an issue that has been asked for a long time. Since we already have that part of the code it felt like a good place to start backporting stuff into the open source project. A major blocker there is we need to be able to generate TLS certificates that are somewhat valid. We can’t just randomly assemble stuff together, they have to verify. I am looking into Rust primitives to actually do that without relying on external tools which is what we do in Greenlight currently. It is about generating private keys, generating certificate signature requests, we might be able to skip those and generating signatures and then packaging them into PKCS8 files. Most likely we will be storing the certificate authority and the key for the gRPC plugin itself in the datastore. And write out the client TLS certificate into the `lightning` directory so you can pick that up and move it wherever you want. That’s how you authenticate the plugin to the client and vice versa. Through this mutual TLS authentication. Using that same infrastructure we will be able to extend the RPC interfaces to also include REST should that be desired. Most of the existing tooling is using REST, that seems like a worthwhile investment. Then we might be able to also reuse parts of the client libraries for Greenlight directly with c-lightning so that despite browsers not supporting mTLS, you’d have to add the client certificate to your browser, we might be able to use an alternative authentication method to have the browser sign off on requests it does. Therefore we can verify the authenticity of those requests. The other bigger chunk is that I’m looking into merging the adhoc channel filtering that we are doing currently. Merging the channel hints that we are currently using to decide whether a HTLC can pass a channel or not. Merge that down into the gossmap infrastructure which already has a facility that Rusty built to create overlays on top of your network. The idea there is to remember inside of the map itself what the channel capacities are that we’ve learned while doing a payment. Initially we will just use that to run Dijkstra in a more efficient way without blacklisting the channels that are obviously not going to work because they are too small. Later on we can then store that information as well and keep that information across payment processes. That can enable more efficient payments if you are doing many payments in succession. You will not start with a wiped memory, you will already have some pre-existing knowledge about what the capacities out there look like. The second improvement is we can do calculations on the graph itself. Stuff like actually implementing min cost flow on top of the graph will suddenly become possible. Currently we would have to run min cost flow on the graph itself and always look at the side whether the channel that we’re thinking has sufficient capacity actually has enough capacity. This opens up a whole new world of existing graph algorithms that we can suddenly throw on the network and pull out a path that has certain correct heuristics without having to have two sets of data that are involved. Those are my big chunks. I have also been looking into automating some of our workflow, specifically I have been looking into a system called Mergify which operates a bot on GitHub that can do stuff like automatically rebasing pull requests. You can add a pull request to a merge queue and they will queue them up for inclusion and rebase pull requests as you go. Stuff like “I just kicked CI and I will have to come back and merge it later”, that can all be automated. It also has a couple of additional rules like requiring acknowledgements from users but I am still undecided, I shouldn’t be the only one deciding whether to use it or not because we’d have to give that bot write access to the repository which is a bit dangerous? It doesn’t exactly feel safe.

What could possibly go wrong? It would be convenient sometimes. I find that before bed I’m like “I’m going to check that PR again. If it is passed I can merge it because I kicked it a hour ago before dinner or something”. That might be nice. Less CI flakes would also help.

It could be complemented by de-flaking the CI. At least give us the time that we used to spend on rebasing manually and having to checkin what happens, spend it on de-flaking the CI which I think is more important than all of the purely procedural things that we need to do like rebasing after we merge a pull request, stuff like that.

One thing I did was I coded a little plugin which was `forwardstats` that takes the list of forwards and counts the number of successful or failed tries on any of your channels. By doing so I figured that from my 40 channels I had like 5 channels that had terrible forwarding performance, like 0 point something percent. I thought “Ok now I could try to call the guy and find out what’s the deal”. I didn’t, I closed the channel. My payment routing got significantly better. If someone is experiencing stuff like this… Closing channels is not the way to go but it can help if it is a terrible peer.

If it is bad enough that’s exactly the right behavior.

Is it in the plugins repository?

Not merged, I can give a link.

Perfect, I’ll test it then.

# Automatic rebasing

The rebasing, surely that needs human judgement. When you’re saying automatic rebasing what does that mean? Whenever you rebase you have to decide which conflict to bring in and surely that is human judgement?

If there are conflicts certainly you definitely need human intervention. Most cases of rebases though don’t have a conflict at all. With the project of a certain size you have enough files that you don’t tread on each other’s toes. The bigger we get the fewer conflicts we have and therefore automatically rebasing is possible. Since the CI tests are being run after the rebase as well we should get about the same security or certainty about it working than we did before. If the CI fails we know that there is something wrong. It used to be the case that c-lightning was so tiny that every single commit I would start clobbering Rusty’s changes. Whereas now we are at a size where conflicts are not that often.

We have tried to reduce single points of failure. There is dumb stuff like putting includes in alphabetical order reduces conflicts. If everyone adds their includes at the end of the list then you always conflict. Dumb stuff like that. Not checking in generated files helps. We still have some generated files that we get conflicts on. The man pages in particular, we generate the schemas from them. Generating the schema part, that sometimes causes conflicts. Generally we have gotten better with that. If you just do a `git rebase` and it works you don’t check it by hand anyway. Having a bot do it is really no different. I don’t look through the rebase and see if it worked. There’s textual conflicts that are generally pretty easy to deal with, they are in your face at least. There are subtler conflicts where someone adds a test, you rebase on top of it and you needed to modify that test but it didn’t exist in your original tree. CI will hand you both pieces and you’ll have to figure out what goes on. You can’t everything. If everything is good, the PR has been ACKed and everything else, but policy we always rebase. One of the things that can happen is you get the break after rebase, we had at least one of those recently. Both patches were fine but one got put on top of the other and the combination was not good. You only find that out after it goes into master. Then someone hits it. “Why is my stuff breaking? It is nothing to do with what I touched.”  Sure enough master is broken. It has happened, at least a couple of times. It would be nice to have something do the grunt work and stop it.

Generally speaking GitHub by default doesn’t rebase pull requests so it can happen that you have two pull requests, you apply one and then the other one doesn’t apply anymore. Or worse you actually have semantic differences between what you based your work on and what your work is going to be based on later. That’s really dangerous. We should catch that with CI but at that point everything already went through code review and we should have noticed that. Those semantic changes are what can cause master to break. But from a purely mechanical point of view if there is a syntactical conflict, when you change the same lines, we will abort the rebase anyway. And CI like I said is our safety net. Currently what we do if you are release captain is that you can go through the pull request list and just merge all of them. This can result in a broken master whereas by automating the “We apply one then we rebase the next one in the queue and test it fully and only then apply it.” Then we rebase the next one. We also minimize the number of CI runs, CI for us is a contended resource.

Especially around release time. As release captain you are pushing a lot of stuff in at the same time. We give the release captain broad authority to ignore CI or abort it early, stuff like that. It would certainly assist. There are only so many hours in the day, you really want to get the release out. “These three are good so I am going to do trivial rebases and just push them in without CI passing”. That has been known to fail. The other thing we do is we aggressively rebase rather than merges. I always prefer this because if you have these kind of conflicts and you get a merge you can tell exactly what happened. You can tell it is no one’s fault, both before merge were ok and the merge was bad. That doesn’t help you very much semantically. If you rebase the set of changes then you can test and bisect and go “This was good, this was good, this was good, this was the point that you broke”. You don’t get the ability to blame at this point, you can’t go “You should have spotted that” because it turns out that maybe you’d built it on something else and you couldn’t tell. More importantly you do get the ability to nail quite easily down to the commit which actually broke something even if it is not obvious why that got as far as it did at this point. My preference is always to rebase rather than do merges. If you bisect and you get down to “It is broken in a merge commit” you are in deep s\*\*\*. You’ve got 100 changes here, 100 changes here, they are all fine but the merge is broken. You can’t bisect that further.

That’s even the simplest case where you are not doing an octopus merge right? Where you might have 10 branches all going into the same merge commit and then you have to disentangle 10 PRs to find which one is broken because of the combination that just didn’t work out.

I have always preferred rebases. Some of it is a holdover from kernel days pre-Git where you used patches. Effectively that is always a rebase so you are always applying on top.

# Individual updates (cont.)

I should mention that Aditya, the Summer of Bitcoin student is coming back as an intern. At least that’s the plan. I said to him that we really liked his work and we should totally take him on as an intern when he gets a break. He has just finished exams so ideally next week he’ll be doing an internship with Blockstream for a couple of months. I have put him on the idea of trying to get [Spark](https://github.com/shesek/spark-wallet) to use Commando. Spark at the moment requires HTTPS, it needs a TLS certificate and everything else. I was like “Wouldn’t it be cool if Spark, the wallet front end, could speak the native Lightning protocol and use Commando which is basically a way of sending commands across the Lightning protocol authenticated using runes?” Then you could skip this whole authentication step. You could just authorize your front end and at this point Spark would look a lot like any other node on the network. You just say “This node can send me commands” or “This is the list of commands it could send me”. That would be kind of cool. He has got a lot of the prerequisites for it because he wrote a lot of the Javascript work for BOLT 12 and he wrote the stuff to speak web socket and he wrote the stuff to actually speak the Lightning protocol in a primitive sense. He has kind of got the pieces. Spark is written in Javascript so I am going to see how far he gets with that. It will be interesting to see what his experiences are trying to get that working as a serious authentication method. I don’t think anyone has used Commando in anger before. And it will finally give you the ability to do a Spark read only where you’ve got a front end that can’t actually spend funds but can view things and stuff like that. That is what I am thinking for his internship project.

I am working on, other than de-flaking and trying to reduce memory in tests… My node had been up for almost a month, I was slacking on updating it across the release, it started to run out of memory. It runs in development mode and it turns out we had a small memory leak with a FIXME, 12 bytes at a time. It is fine except with all the development stuff we allocate a lot of extra metadata every time we do an allocation so we can find memory leaks. It turns out I had a gigabyte of extra metadata hanging around. Particularly because we have a log prefix and we would generate that on every JSON command. We didn’t ref count, I said we should ref count this but let’s just leak it for now. It is 12 bytes, what could possibly go wrong? You can do a lot of 12 byte leaking before anyone notices. It was the 256 byte backtrace that was attached to each one that started to get pretty heavy. Because I’m running CLBOSS. CLBOSS does an awful lot of JSON RPC commands all the time. You run it for a month or so under development mode, you get a gigabyte or so. That’s fixed. We deliberately suppressed our memory leak detection for that code because it was a known thing. We’ve got pretty good memory leak detection. I have a fix for that, I did it properly, that should be much nicer. But it is not a case that most people will run into because most people who run developer things and CLBOSS, you either have a big machine and you don’t really notice or you restart more often because you want to keep up with master. It was a fun one to find.

# Rearchitecting c-lightning daemons

Most of my time for the last week has been rearchitecting all of c-lightning so that every connection goes through what we call connectd. connectd is responsible for making connections and receiving incoming connections but usually what happens is once it has done the initial handshake and done the init message exchange, checked the features are ok, it hands the file descriptor off to openingd. It is openingd until it sends a message like reestablish or open or whatever. That file descriptor gets handed around so every subdaemon, channeld, closingd, openingd, dualopend, all speak across this directly to the peer. We have wanted to rearchitect it so that connectd always is the only one that talks out to the peer, it buffers internally and handles an internal file descriptor. That means moving all the crypto into connectd which it already had but then ripping it out of the other daemons which makes them a little bit simpler. But it also means it can intercept all the gossip messages. There is some weird stuff that we do. It goes into channeld for example, it goes “This is a gossip message” and it feeds it back to gossipd at that point. We also for complicated reasons handle onion messages that way. Every daemon doesn’t handle it, it just hands it off to gossipd. In the new method connectd is intercepting and only sends to each daemon the stuff that is specifically about the channel. Generic messages like pings, onion messages, gossip messages, it diverts immediately. Each daemon in fact becomes a reasonable amount simpler. There is a little bit more work on that to make them even simpler again. They are just concerned with talking to the peer and they talk in the clear, all the crypto happens in connectd. That is working pretty well. A lot of re-engineering and figuring out how to do this in a clean way as a nice series of incremental improvements rather than just one huge fireball of spaghetti which it almost turned into a couple of times. I am hoping that the end result of that will be a much nicer architecture for some of the other improvements that we wanted to do for this release. It has been a long road to try to get that all working. There were some interesting things along the way. We already have connectd talk to gossipd for not great reasons. When you say to connect to something it is actually connectd that asks gossipd “Do we know any addresses for this?” which is kind of dumb. I have changed it so that lightningd asks gossipd and then it sends to connectd “Here are all the addresses that we know”. The other thing we do which we are working on now is channeld itself. When we send an error message back for a HTLC that didn’t work, sometimes we are supposed to attach the latest channel update to tell them about the channel in case the problem is that their information is out of date. gossipd has that information. Rather than do that query inside our state machine inside lightningd we actually hand the unappended error message down back to channeld and then channeld asks gossipd “By the way can you give me the stuff I need for this?” It was always a bit naff really because you hold up for a little bit while you ask gossipd this thing. I decided I didn’t like that. lightningd will now have the latest channel update in memory. gossipd just tells it “There’s a new channel update, here it is”. Then it can just trivially assemble the error message without blocking or without having to go to sleep or do callbacks. It can just trivially take the latest, append it and send it down. That will be significantly simpler which is kind of nice. I was always a bit nervous… The reason I didn’t like this asynchronous thing is because halfway through erroring because the HTLC went wrong, you call out to gossipd and you do other stuff while you’re waiting for that reply to come back, you worry about race conditions. You’ve got this half failed HTLC that isn’t quite failed yet, it has got this partial error message you stash somewhere. What if another one comes through and you get conflicts? That made me way too nervous so I am doing it this way which is much simpler. There are some cleanups along the way because that was one of the only two reasons that channeld had to talk to gossipd. I would really like to get rid of that, it is another file descriptor. Then the idea is at the end channeld will only talk to two things, it will talk to lightningd directly and it will have this thing out to connectd to go to the peer. It will have two file descriptors and that turns out to be a lot easier to deal with. In a number of cases you can just ignore one and just use a single one. In UNIX reading and writing from a single file descriptor is about 10 times easier than reading and writing from two at once. You can just read and write rather than having to do a select or poll and then handle everything else. The end result should be that our daemons get simpler. This is nice because if we ever want to reimplement them in another language it gets simpler. It also reduces the number of file descriptor parsings that we do, not down to zero but it does reduce them. We could reduce them further by having connectd actually spawn the child daemons. That is not going to happen yet but it could happen at some point. This has been a lot of rearchitecting and figuring out how things go, revisiting parts that were always a little bit on the nose and trying to clean them up. It has been slow progress. It has been like a week of pulling stuff apart. I am 20 commits in at this point and I am probably about halfway. I will try to figure out a good point to cut.

# Individual updates (cont.)

The other thing that has been cooking is the onion message stuff. openoms mentioned that eclair have a PR for onion messages. They have tweaked the spec slightly. We go through this negotiation where we go “We like it this way rather than that way”. We are breaking onion messages again. With the current release we send out the obsolete onion messages and the new onion messages that we expect but the spec has since changed. I have removed the obsolete ones. Now we have the obsolete 2 ones and we have the new, new ones, the final hotness which will be the spec hotness. For the moment we will still send out both because we are dealing with n-1 peers. I have that code, we send out both and we hopefully receive one. But there is a thing heavily implied in the spec where we can also use this route blinding to send HTLCs. We have had that support for a long time. Updating that to the new spec is a larger task. I may just disable that functionality for the moment and hope to get back. Mainly we are using route blinding at the moment for onion messages but you can also use route blinding for real payments. We haven’t used that in a while so it would have to be re-redone. Even eclair doesn’t support that yet either. That will probably get pushed back just because I don’t want to have to rewrite all that right now. BOLT 12 offers have this ability to say “Here is how you pay me”, you give them a blinded route and you should be able to pay that. But I don’t think it is going to make this cut for this release. So lots of stuff going on. I am really excited to get onion messages finally finalized once we’ve got interop tests confirmed with eclair, that makes it a candidate for merging through the spec which is really good. Then I’m hoping some brave soul will implement it in lnd. Which you can almost do as a plugin. You can’t quite because you are supposed to advertise a feature bit saying that you support onion messages. Apparently lnd plugins can’t manipulate feature bits. But you can still in the latest lnd I believe have a plugin that handles arbitrary messages so you can do onion messages entirely in a lnd plugin which will be kind of cool. Even without that we should have some network effect and be able to experiment a lot more with what has happened with onion messages. The next step will be BOLT 12 on top of that. They have already gone through the spec once but as they implement it I expect there to be more feedback. There will probably be another BOLT 12 break. That’s just the path we chose. I have done a frustrating amount of re-engineering of stuff. Normally we would have an experimental only implementation that no one is actually using and we could change it arbitrarily. Then we’d go through the spec process and we’d just break it. Unfortunately because we had to prove that offers were something useful by actually getting them out there first, the downside of that is that we have support those users. I can’t just break them every single release. Every time we make a change in the spec I have to try to support both. At least for one iteration of c-lightning. That has meant a lot of forwards and backwards work just trying to make that work. It is frustrating but sometimes that is the cost of engineering in the real world, having users means you need to support them a little bit. I anticipate there will be a little bit more of that. I am hoping if the onion message layer at least is stable and spec’ed and finalized and done then it is a lot easier to build on top.

One more thing, I noticed we see a lot of ping pong messages now in debug which was expected. But it is also happening on non-Tor connections from my own node.

Originally we talked about doing it for Tor and then I realized it is just easier to do it for everyone, nobody cares. It is a 30 second timer plus or minus 15 seconds.

So if that is intentional then maybe we should make the debug message I/O or something.

Yeah you’re right. It is a lot.

A fun question. Do you think it improves the situation on the Tor connections or not?

This is a very good question that I will have to actually start reviewing my logs of Tor nodes to see how that is working.

It would be good to know because I’m not too sure about this.

You have this great plugin that we should use to assess our forwards. That’s the proof in the pudding, whether we actually get more HTLCs through our Tor connections or not. To actually do retrospective I’d have to go through the logs and see what our stats are.

Maybe we want to make a configuration parameter about the ping pong stuff because some people may be using this on mobile connections and that maybe painful. It forces you to not sleep at all ever.

That is a really interesting question. The other thing is we don’t log gossip for similar reasons so I’m not sure how much traffic it is making it worse than existing gossip which is every 60 seconds. I would have to look through on I/O debugging to see how much gossip we are getting every 60 seconds. I suspect you already in hell if you are trying to do this because you are going to get gossip from every peer every 60 seconds.

It can’t be tuned? Maybe that would be a nice side project to optimize it a bit for mobile connections.

The problem is your peers will be doing it as well. You’ll need to tell them to back off somehow, go into quiet mode. The answer is actually don’t connect to peers unless you have something to say. This would be the other way of operating your node, you only connect on demand and you disconnect when you are not interested. But that is terrible if they are trying to forward to you. Unless you have a full IP address and they can do the same thing, connect to you when they want to talk.

Mobile users have a lot of problems with public IP addresses.

They can only connect out so I don’t know how that helps. You can suppress gossip. Maybe it is worth having a similar thing… It would be interesting to see. We do currently choose 3 peers to gossip to us at any time. But if you were to run a node where you tune that down to zero for long periods of time and then burst your gossip in. If you want to play with gossip there is the Minisketch stuff as well that I have in a branch that I never pushed anywhere. The idea is you have a summary, you send this Minisketch summary of all your gossip every so often. If there is something useful to say then you transmit the gossip that the other side is missing. That would also be useful both for reducing bandwidth but also it potentially means you can go for a lot longer before you try to sync your gossip up. You might want to sync your gossip as you are doing a payment for example. Maybe you start the payment and then you also try to sync your gossip at the same time, I don’t know. I just suspect that if you are on mobile and you are really bandwidth constrained our implementation is not going to…

Bandwidth is not the main problem on mobile nowadays. I think it is battery.

I think running a routing node generally on a phone when you’re relying on battery is a difficult problem. Maybe not an impossible one if you put fees high enough so that you don’t woken all the time, maybe it is something that you could do. A research project for you, I look forward to the results.

On the phone I think the problem is the synchronization with the Bitcoin blockchain, this is the bottleneck.

Not necessarily phone. For example stuff like routers where you put in a SIM card, people may use them in the trailer or whatever.

But in that case are they running off battery?

Not really.

Lots of exciting stuff happening, I am really looking forward to this next release. By the way I have nominally made the date January 20th because we are going to lose the holiday break generally. Everything stops for a while. January 10th seemed a little ambitious.

Hi, good morning. My semester just finished so I will set up the Spark wallet today.

Once you’ve gone through the pain of trying to get it to do the Let’s Encrypt for the certificate so you can connect you’ll understand why we want to try something else.

# Rearchitecting c-lightning daemons (cont.)

Can I attempt a quick TL;DR of that first task you are running on? I think I understood. You are trying to simplify how the subprocesses are communicating to each other. At the moment it is a bit more complicated than it should be, there are more calls than there needs to be. You are trying to simplify how the subprocesses interact or how commonly they interact?

We are centralizing everything through the connection daemon. The connection daemon will maintain a connection at all times. It will be the only thing that talks to peers. It will de-mux a lot of stuff. The individual daemons that work with channels will get a much more simplified view. They are not talking directly to the peer anymore. They are not doing the crypto for peers, which is pretty trivial to be honest. They are not handling gossip messages, pings and onion messages and other things unrelated to channel management. They will only see things that are about their channel. Everything else will be intercepted by connectd which will farm off to the right place and do the right thing. We have a daemon for every channel. channeld is the classic one but there is an openingd when you are opening a daemon and there is a closingd when you are closing it. But it is a very simple daemon, it only handles one channel, only knows that. We already do some de-muxing. We have this simple daemon, all it knows is about one peer and one channel. It has no idea about the wider world. We are going even further. Now it won’t even see any messages that are not about its channel. These metadata messages like gossip and stuff, it won’t even see that at all. It is a simplification in that way. We already had this one daemon, connectd that had to handle finding peers and reaching out to them and doing the initial handshakes and setting up crypto and all that stuff anyway. Instead of handing the whole thing on after that point it just keeps that and then shuttles back and forth to the internal daemon. It is somewhat conceptually simpler but it is more centralized. The downside to that, whenever you have something doing work on behalf of something else you worry about starvation and denial of service and stuff like that. Previously if you had one peer that for some reason was using up a lot of CPU doing crypto whatever, that is fine because it is a single process. That is a much easier thing to contain. Whereas now connectd was doing some of the work itself, connectd just starts chewing up CPU and you’re like “Why?”. It is not that obvious. It is because it is doing work on behalf of this one channel that is maybe sending a lot of data through or something. In practice the encryption is fairly lightweight and I don’t see this as a huge issue. But in general the reason we did it the way we did it the first time is if you can constrain things so that everything about one peer is handled within one daemon, from a UNIX perspective that process is a very easy thing to manage. You can limit its memory, you can limits its CPU. You can rate limit. You don’t have to implement that yourself, they are all standard UNIX utilities. When you split that it becomes more difficult. If we want to do rate limiting for how much gossip a peer… At the moment the peer could keep asking us for a whole dump of gossip every second. We will spend our entire bandwidth just streaming gossip out to it. If we want to do intelligent limiting around that we would have to have some more sophisticated logic inside connectd rather than saying “Every process only gets 1MB a second”. There are some downsides to doing it this way but conceptually I think it is simpler.

I’d like to hear more about Greenlight one day as well. Not today, another time. Whatever you can share that is not client confidential like what lessons there have been from getting these people onboarded to Lightning who otherwise wouldn’t have onboarded. It sounds like an interesting topic for another day.

Don’t get me started. You won’t get me stopped. It is my new favorite topic. I put aside a hour during lectures to talk about Greenlight.

You should be filming the lectures.

They’re not mine. You can probably ask Lukas, the president of the Swiss Bitcoin Association, he is organizing the 21 Lectures stuff. I think he has a recording of it. Anytime I’m more than happy to talk about Greenlight. Maybe we can set up a special slot so I don’t take away too much time from everybody else. Because like I said once I get started I will not stop. There is not that much that is confidential, most of the stuff like I mentioned will be open source eventually. And we are already starting backporting some of the parts into c-lightning. The networked RPC being one example. That has always been the goal. We want to run c-lightning nodes to learn for the open source project. Cross help, cross finance our resources this way. And it allows us to gain a lot of experience running c-lightning in production as well. There is definitely a lot we can talk about.

I’ll message you and try to get something organized.

From today there is a [new Signet faucet](https://signet.bublina.eu.org/) run by me. I have 1000 Signet coins. I am using Signet a lot to teach new people Bitcoin. It is very helpful. I was experiencing some problems with the Signet faucet so I did my own and talked to kallewoof. It is now on the wiki and I want to see more people trying to ask for Signet coins. At the moment the balance is growing.

I have a lot of thoroughly mixed Signet coins in my Joinmarket instance. It is all communicated through the second version of the onion messages currently. But you won’t be finding where it is coming from.

That reminds me, I need to get my Signet node up.

I am happy to help anyone. Currently I have experience on Alpine Linux, multiple nodes. Very small, can run on Raspberry Pi, whatever.

