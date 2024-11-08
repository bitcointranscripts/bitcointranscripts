---
title: Maintainers view of the Bitcoin Core project
transcript_by: Bryan Bishop
date: 2019-06-06
aliases:
  - /bitcoin-core-dev-tech/2019-06-06-maintainers/
speakers:
  - Michael Ford
  - Wladimir van der Laan
---
<https://twitter.com/kanzure/status/1136568307992158208>

How do the maintainers think or feel everything is going? Are there any frustrations? Could contributors help eliminate these frustrations? That's all I have.

It would be good to have better oversight or overview about who is working in what direction, to be more efficient. Sometimes I have seen people working on the same thing, and both make a similar pull request with a lot of overlap. This is more of a coordination issue. I think generally the maintenance process works pretty well. Having MarcoFalke has been really helpful, and fanquake with the tags, and meshcollider, we're in a good state.

Should fanquake be a maintainer? Is now a good time to nominate him? Sure. Yes. Yes. If he becomes a maintainer, is he going to stop tagging? It's actually a team of people on a farm in Australia. He currently doesn't have his key in the maintainer file. He could technically merge something, but then everything would fail. The branches are all protected too. Github verifies it as well, right? Indeed.

Way too many pull requests open. Please don't open any more pull requests, especially for small things. If you change consensus code, please have benchmarks and prove that it is better. Sometimes there's a lack of motivation for pull requests. That's my main complaint.

When can we poke it and get an initial block download benchmark on travis-ci? This effects users. Most of the benchmarks are microbenchmarks, but this one would really impact users. Right now you can say "yes it's faster" but not actually do anything. When are we going to have benchmark integration in the bots? We could have something that runs automatically based on the tags. There's only a few pull requests that are performance-sensitive. It's something that can be requested for a pull request, like needs-build and needs-benchmark. It could also do a once-a-day build for master and notify for regressions. We already have that, for benchmarking and performance regressions. It doesn't alert, but you can go and check. We should probably add an alert. It does IBD up to a certain height from a local peer, as well as running all the tests and benchmarks and all that stuff. Marco keeps a close eye on it. But yeah it's up there. There's 11 dedicated machines on there. They are generic 4 core HP servers or something. Half of them hard drives, some of them have SSDs. Or a system where you can click a pull request into a thing, and then get all those builds.

Wallet has been going well over the last few months. We have fortnightly meetings. Seems like we've been getting a lot of work done. The descriptors work is a common focus. So we have a group of people all looking at the same stuff. Looking historically, the time of significant progress in certain domains of code, it is often when there's a group of people all active with a common goal and probably have a maintainer on board. When there's sufficient momentum, having subprojects or task forces or special interest groups or whatever you want to call it, seems to help. And it's more fun. The interaction cycles are much smaller, right. You don't have to wait that much for review because there's other people you can bounce off ideas and look at things immediately. I don't know how to scale this to other things because the pre-requisite is that people have to be interested.

Are there other areas where momentum can be built, but it's just not happening organically? There are sections where I would like momentum to be built, like a lot of interesting p2p work. What about the thing for splitting into separate p2p networks? Like having a blocks network, and a transaction network, which basically operate independently of each other. They solve different problems that you care about. We should talk about this later. Should we have weekly p2p meetings? We would have to find a p2p maintainer. There's a real shortage of people who understand p2p. There should be a technical document of the p2p design philosophy for Bitcoin Core. People don't understand the current model, or why dandelion is important. ((Some confusion about how to pronounce dandelion; we seem to have settled on dan-dillion)). For building momentum around p2p... descriptors is adding momentum for the wallet and the wallet meetings, and having a wallet maintainer. But without a p2p maintainer, seems like aj, sdaftuar, carl are interested.

Other area for momentum is build system stuff. When are we overhauling the build system? When are we merging that? It seems like every 2 years someone shows up and wants to rewrite it from scratch. This isn't the "when do we switch to cmake" thing, but the "when do we drop gitian". I don't have an answer to that, but it's a work in progress.

One of the things that was helpful was when fanquake started triage, and currating the pull requests a little bit. Is there more stuff along those lines that could be done? Is it helpful to maintainers to have other people assisting in those tasks? It might be good to have a tag "waiting for author". That's a good idea. Yeah. Would this replace the needs-rebase tag? Because that's also "waiting for author". Maybe it could be combined. It's not common for us, but we could do the rebase at merge time ourselves. But we don't do that because we want to show what the author has submitted has been merged. For trivial things, I did it in the past sometimes. But REST got merged in a state where we couldn't use it, so we messed up with that in the past. Pull requests could be auto-closed after a few months of no author feedback. 3 weeks is too soon.

We added the "needs concept ACK" tag yesterday, right? Say we need to add a "needs author" or something, should we still ping fanquake? Ask one of the maintainers to edit, it doesn't matter who or where. Authors can't add or remove tags.  The maintainers maintain the tags. We could have user tags in comments, and a bot to parse the comment text, but we would want to filter those out from the maintainer currated tags. The bot can check if the person is in the travis restart group.

Users can edit issues and add tags, but not push to the repository. This is possible with protected branches on github but this is not supported on github really. If you forget a branch, it's a problem.

Someone in China is attacking mainnet and testnet with a DDoS right now. Well, at least someone is using testnet for once...

