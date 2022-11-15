---
title: Pieter Wuille (part 1 of 2) - Episode 1
transcript_by: Whisper AI & PyAnnote
categories: podcast
tag: ['We talked to Pieter about his thoughts on some of those influential PRs, including headers-first syncing and ultraprune, and hear about the motivation for those changes and how he thinks about them now. This is a two-parter and in the next episode, we’ll hear about libsecp and Pieter’s thoughts about Bitcoin in 2020.']
---

Chaincode Labs podcast: Pieter Wuille (part 1 of 2) - Episode 1

SPEAKER_05: Peter, you've had over 500 PRs merged into Bitcoin Core and I think over 11,000 review comments in the repo, so...

SPEAKER_01: That- that is... possible?

SPEAKER_05: That's quite a lot, over 11 years. No, not quite.

SPEAKER_04: Sorry, we'll cut that bit so no one knows.

SPEAKER_02: this? I do not like the implication here.

SPEAKER_03: Hey, folks, you're listening to the ChainCode Podcast. I'm your co-host, Jonas, and I run special projects at ChainCode Labs here in New York City.

SPEAKER_05: Hi, John. Hi, Jonas. Hi, everyone. I'm John, and I'm a Bitcoin Protocol Engineer at Chaincode Labs. I work on Bitcoin Core, but I also spend a lot of my time trying to help bring new people into the Bitcoin technical community.

SPEAKER_03: So if you aren't familiar with ChainCode, we exist to support Bitcoin and we contribute to Bitcoin Core and other open source projects. But another important part of what we do is our educational work. We've run several residencies in the past to help onboard new contributors to Bitcoin protocol development. And if you have an interest in learning more about what we've done, you can find videos and curricula at ChainCode.com.

SPEAKER_05: This podcast is an extension of that work. We're lucky enough to have some of the smartest and most influential Bitcoin developers visit our office, and we want to share some of their stories more widely.

SPEAKER_03: So something a little bit different about this podcast is going to be deliberately technical. We are going to be talking to some of the best minds in Bitcoin and hear from them about their insights and reflections on the Bitcoin development process.

SPEAKER_05: And what better way to start than by talking to Peter Weller. Peter has been contributing to Bitcoin for nine years and is responsible for some of the most important developments in that time, including Segwit, Best 32, LibSecP, Schnortab Roots and many others.

SPEAKER_03: So we talked to Peter a little bit about some of those influential PRs, including headers for sinking and ultra prune. And we hear about the motivation for those changes and how he thinks about them. Now, this is going to be a two parter. And then the next episode, we're going to talk about Libsac P and Peter's thoughts about Bitcoin in 2020.

SPEAKER_05: We really enjoyed chatting to Peter and we hope you enjoy listening. Now here's a conversation. We'll catch up again at the end of the show.

SPEAKER_03: Welcome to the podcast.

SPEAKER_05: cast. .

SPEAKER_00: Hi, Peter. Hello, John and Jonas.

SPEAKER_05: Thank you for being the first guest on that podcast.

SPEAKER_03: So far, the most important guest we've had.

SPEAKER_00: That's an amazing honor. Thank you so much for having me.

SPEAKER_05: Well, we're here to talk about Bitcoin and Bitcoin Core development, and we have Peter Waller as our guest, who is a Bitcoin Core contributor of many years standing. Peter, you've had over 500 PRs merged into Bitcoin Core, and I think over 11,000 review comments in the repo, so...

SPEAKER_01: that that is possible.

SPEAKER_05: That's quite a lot, over 11 years. No, not quite.

SPEAKER_04: Sorry. We'll cut that bit so no one knows. Let's say nine years.

SPEAKER_02: I do not like the implication here.

SPEAKER_05: We have a few questions for you and the first question is of all of those PIs that you've done we've picked out a few that we think are interesting and we'd like to hear from you kind of your inspiration for those and interesting thoughts about those and the first one we picked was Headers First Sinking. So can you first of all tell us what that is?

SPEAKER_00: sure so historically how in the bitcoin protocol and bitcoin core implementation blocks were learned about and fetched from peers was using the get blocks message which you would send to a peer telling them hey i know about this block hash tell me what's more and they would send you a block a list of block hashes back and you'd start fetching them and at the end when you've done all of them you'd ask again now what more blocks should i ask about and this works fine as long as you're fetching blocks from one peer the problem is this this mechanism really does not parallelize well to multiple connections because there's no way to like interleave or i guess you could come up with some complicated mechanism where you're like oh i know this peer has these blocks and this peer has these blocks i'm gonna like ask one one from each but it's really a mess because you you don't know where you're going it's you start off at the beginning you just ask hey what's next and there's huge attack potential there because a peer could just be like yeah trust me i i have a very good chain for you in the end it's it's gonna have high difficulty but it just keeps giving you low difficulty blocks for for starters um so this was also a problem in practice um around the time maybe 0.6 0.7 this started to become an issue um because downloading blocks started taking longer than 10 minutes uh that may have been a problem before that time even um the the problem was

SPEAKER_05: Because you you even downloading the entire blockchain to yes.

SPEAKER_00: Yes. You'd start off downloading blocks from one peer. You'd ask one peer. Intentionally you would only ask one because we knew that this mechanism didn't parallelize. And then another peer would announce to you, hey, I have a new block. And you'd ask them, hey, give me that block. And you'd be like, well, I have no idea what its parent is. Can you tell me something about its parents? And the result was that you'd basically start off a completely parallel second block downloading process with that other peer.

SPEAKER_05: And that new block is called an orphan block.

SPEAKER_00: Right, that's even another issue that the pre-headers first mechanism had. You'd learn about blocks and have no way of knowing what its parents were until you had actually fully synced those parents. So there used to be a pool where these downloaded blocks without parents were kept called orphan blocks, which is unrelated to stale blocks, which are just blocks in the chain that were abandoned because the majority hash rate forked away. So around the time of 07, 0.8, 0.9, I think we kept adding hacks on top of the block downloading mechanism, trying to put heuristics to prevent it from having eight connections and basically downloading all blocks from all of them simultaneously. At some point, syncing got so slow that you'd end up with so many orphans that you could go out of memory while downloading. You're still trying to catch up and you're learning of all these new blocks that were just mined during the time you were syncing and they would all be kept in memory. And so then we introduced a limit on how many of those were kept and the oldest ones would be deleted and that led to even more problems where those orphans were actually downloaded over and over again. So overall, this was a mess and it was clear this wasn't going to keep working.

SPEAKER_05: And and for context this is 2013 14 ish

SPEAKER_00: possibly. This was fixed in 0.10, so you can... Header's first synchronization was introduced in 0.10. And what it did was split the synchronization process in two steps, so to speak, but they were performed in parallel. One is where the normal synchronization process that's just from beginning to end, give me whatever, was replaced with just synchronizing the headers. So you'd build the best header chain by asking peers, give me headers. Oh, you have more headers, give me more headers. And the same mechanism as previously was used for blocks would now just be used for headers, which takes in the order of minutes, because it's...

SPEAKER_05: Thanks for watching!

SPEAKER_00: At the time a couple dozen megabytes, maybe a bit more now.

SPEAKER_05: And the reason for that is the vast majority of time when doing an initial block download and initial sync is checking the signatures in the transactions.

SPEAKER_00: Right, plus also actually downloading the data because headers are 80 bytes per block rather than...

SPEAKER_05: one megabyte at a time.

SPEAKER_00: Yeah, well at the time they weren't quite fully yet, but and then there would be a second phase Which would just be a background process where during the main loop of Bitcoin course network processing it would Try to figure out which headers have I heard about from which peers and see oh This one has a chain that is actually better than my current fully Validated block tip and it would ask for a couple blocks there And by limiting how many blocks were asked of each peer this this parallelizes quite well because I think there's a limit of Maybe eight or sixteen Blocks per peer that are ever queued up. Okay, so you'd ask no you you have this this header chain I'll ask the next 16 blocks of you. Oh someone else has them, too I'll ask for the 16 ones after that one from someone else together with a Heuristic at a time that was very simple, but I think has worked fairly well, which is We'd never download a block that is more than a thousand and twenty four blocks ahead of our current tip So because we're starting to download blocks in parallel now from multiple peers and just validating as they come in and We don't have the problem of orphan blocks anymore because we already have their headers by the time we ask for them So we know they're actually part of the best chain Assuming that chain is valid, but there's still some dos denial of service concerns concerns there But they're they're much less severe in headers first model

SPEAKER_05: And one of the reasons that those dos concerns are less is that the head is very cheap to verify, but expensive to create.

SPEAKER_00: Exactly, that's a general principle. You try to validate things with the highest cost for an attacker divided by cost of validation. You do those tests first, and if you can bail out early, this can massively reduce attack potential. So in order to attack now, you still have to first create an actual best header chain, or of course, Sybil attack the node during its synchronization. And there's some techniques to avoid that as well, but ignoring those, we already have a headers chain so we can just ask for blocks from everyone in parallel, see when they come in, and as soon as we have all blocks up to a certain point, we can actually run the full script and transaction validation and continue. So this heuristic we have is one for, well, the question is of course, how do you pick good peers? During IBD, you don't care so much about partition resistance or anything, you're still catching up with the network and you're not fully functional until you've caught up. So your primary concern is, well, how do I pick fast peers to synchronize from? And the mechanism we picked is just never download a block that's more than 1,024 blocks ahead of your current tip. And if you're, so you have kind of a window of blocks that starts at your current tip and 1,024 blocks ahead, and in that window, you try to fetch blocks as possible from all your peers. If that window can't move because of one peer, which means you have either, you have downloaded all the blocks in that window, except blocks that are still outstanding requests with one peer, you would disconnect that peer. So conceptually, this means if you have one peer that's so much slower that it is preventing you from making progress that the other peers are allowing you to make, so it's a factor 10 slower than the rest or something. You would kick that peer and find another one. And this mechanism works reasonably well and it will find decent peers. It can get stuck with moderate peers. If they're all equally slow, this doesn't do anything. Right, and there's nothing to do. Well, you could still find fast, you don't know that there might be because your own connection is limited or it may be just because you've all picked rather bad, but not terrible peers. In any case, that mechanism is still being used today, I believe.

SPEAKER_05: And so for that PR, was that the first time we were tracking per-peer state or per-peer performance in order to do that kind of...

SPEAKER_00: I think so. There was per-peer state before that, in particular to prevent the same transaction from being downloaded from multiple peers. So there was already an ask for caching where you'd at most ask for the same transaction once every two minutes or something. So that already existed, that was there since forever. But as an actual performance optimization, I think this was the first, and maybe still the only, real heuristic for...

SPEAKER_05: .

SPEAKER_00: finding good peers as opposed to heuristics for safe, secure peers.

SPEAKER_05: Right, and there was...

SPEAKER_00: And there's so there's there's a bunch of those nowadays where we when trying to create outgoing connections or no, I think when When a new incoming connection comes, but all our incoming slots are already full. There are some heuristics that are used to determine is this peer better than any of the one Like should we maybe consider kicking one of our inbound peers in favor of this new one. And their rules are like don't kick the last peer that has given you a block or prefer peers that are from a variety of network sources or so on. But I think that this this 1024 window. Move prevention kicking heuristic is the only actual performance. Optimizing thing.

SPEAKER_05: And then I think in 0.17, there were a few checks added for peers that were obviously on a different chain or trying to follow different census rules from you.

SPEAKER_00: Right. Yes. Yeah, there were a bunch of other rules added where we were concerned about islands of nodes connected to each other that would share the same consensus rules, but they would all be surrounded by nodes with different consensus rules and they did not actually figure out that there were no blocks coming in. Right. And that was

SPEAKER_05: That was around the time of the Segwit 2X and Bcache hard forks, which is, I think, where that concern came from.

SPEAKER_03: For such a major change though, this was actually pretty quick. You open the PR in July 2014, it was merged in October 2014. So compared to today's review process, that's a pretty quick turnaround for some major changes.

SPEAKER_00: I think I started working on it significantly earlier than opening the PR, though I'm not sure. I remember it back then as a slow thing, but it's all relative.

SPEAKER_05: And on that, how has Bitcoin core development culture changed over those eight or nine years that you've been?

SPEAKER_00: It's certainly become harder, like, we started off with, like, Bitcoin Core had no tests at the time when I first started contributing. Testing meant, you know, manual testing, like, hey, I tried to synchronize and it still works. There were no unit tests, no functional tests. There was, I don't know when the unit test framework was introduced. This was fairly early, but it is limited in how much you can do with just these unit tests, the big interactions between nodes. The first attempt there was, or first major piece of infrastructure that tested larger scale behavior was Matt Corrello's pull tester, I think it was just a bot that would test pull requests. But one of the things it did was have a test implemented in BitcoinJ that simulated things like reorgs and so on and see that Bitcoin Core would follow the right path under all sorts of scenarios. And it was much later that that eventually got rewritten in Python.

SPEAKER_05: And that test still exists, I think, it's featureblock.py.

SPEAKER_00: correct yep that is now one of the the many functional tests that there are there's been dozens added over

SPEAKER_05: Think about 130, 140 right now.

SPEAKER_00: Yeah, that's, that's, how do you call that a dozen dozen score score.

SPEAKER_01: Score is 20, I think.

SPEAKER_03: Scores 20, I think. Oh, Abraham Lincoln. Gross, gross. Scores 20. Gross.

SPEAKER_05: Oh, I'm like, oh, gross. Yeah, I apologize. Well, cut that bit. I have one one final question on headers first sink, which is, so did you see an immediate uptick in performance? And what would if you hadn't done that, or if that hadn't been done, what would Bitcoin look like right now?

SPEAKER_00: So, not too long ago, I think BitMEX published a report of trying to synchronize various historical versions. And I was surprised to actually not see headers first make a big difference there. As far as I remember, there was no big difference between 0.9 and 0.10. And at the time, I believe it was an enormous difference. Like, wow, it would only download every block once. So, I don't know why they didn't observe that.

SPEAKER_05: It's possible the methodology was that everything was in their local network or they had a peer.

SPEAKER_00: I think they actually synchronize from random that appears on the network, but I'm not sure. I remember it as a very big difference, in particular for IBD, for outside of IBD it wasn't.

SPEAKER_05: All right.

SPEAKER_00: Thanks for watching!

SPEAKER_05: Well, if you're at the tip, it doesn't make a huge difference. Right.

SPEAKER_03: Yeah. Aldroprone, yes.

SPEAKER_00: I can talk about what ultra prune is. Yeah, go ahead. So this was in 0.8. Okay. And ultra prune is the name of the patch set I made that effectively introduced the concept of an explicit UTXO set to bitcoins validation logic. Before that time, there was a database that kept for every transaction output ever created, whether or not it was already spent and even where it was spent in tree using 12 bytes of data in the database per output ever created.

SPEAKER_05: That is a TXO set, not a UTXO set.

SPEAKER_00: Right, and it was mutable. It would like, and entries would, it was a database from TX ID to list of its outputs and whether or not they were spent and where they were spent. And by the time I started working on this, this database had grown to several gigabytes. And this was a problem. It was fairly slow, but also the database was indirect in that when you wanted to do validation, you had to go first check this database to see if those outputs were not already spent. And if they weren't, you still had to go find the transaction in the block files to find those UTXOs, because you wouldn't be able to validate a script before you could fetch the UTXO. So there was, effectively your working set was this whole database plus the whole blockchain. This couldn't work with pruning or anything. You actually had to have all blocks available because you were using the blockchain data as the UTXO data. And the motivation was someone had started working, I think on a patch that would go through this database and just delete all TX IDs whose outputs were already fully spent, because clearly these weren't needed anymore. And ultra prune started as a proof of concept of, well, if we take this to the extreme, how small can we make that database? So instead of storing something for every output, why don't we actually switch to something where you just store the unspent ones, because those are the only ones you still need afterwards. And then there was this performance consideration where like, well, everything is indirect. We need always this indirection to the blockchain data, but the UTXOs are actually small. They're just an amount and a small script usually. Why don't we copy that to the database as well? So everything you need for validation is right there. And it depends on what kind of IO speed you had, but just this at a time reduced the amount of data you had to access from several gigabytes to maybe in the tens of megabytes at a time.

SPEAKER_05: And if you extrapolate that to today, it changes from 300 gigabytes or whatever the blockchain is to 3 gigabytes or whatever.

SPEAKER_00: something like that yeah exactly so yeah and and this this not only was a performance improvement it's fairly fundamental as a scaling thing because your UTXO set hopefully does not grow as fast as your blockchain there have been times in the past where it's shrunk not as much as I would like but UTXO set is much more correlated with actual usage while the blockchain is clearly append only and cumulative and ever-growing based on activity so there's of course ultra prune was combined with a switch from BDB to level DB right those were developed independently and then actually turned in I think into into one PR before being merged and this had the well-known effect of having caused a fork in the chain in March 2013 I believe so the problem here was 0.8 was

SPEAKER_01: you

SPEAKER_00: so much faster that miners switched over to it almost immediately, but much of the network had not switched from 0.7 to 0.8. The BDB database that was used for the TX index with all this spentness information in 0.7 had an issue and had always had an issue that BDB requires you to configure how many lock objects you need and the number of lock objects is correlated with the number of pages in the database that are simultaneously affected by a single atomic transaction.

SPEAKER_05: Where a transaction here is a database.

SPEAKER_00: Correct. It has nothing to do with Bitcoin transactions. This is a database transaction and the whole update of applying a block to the database was done as one atomic update so that either the block would validate and you would be able to continue or there would be a failure and the whole thing would never be applied. So a problem was this number was – let me rant a bit about the BDB documentation which tells you in guiding how to pick this number is run your database with a reasonable load and use this function to determine how many locks are used. There was no way you can predict ahead of time how many locks your actual absolute maximum is. This was combined with a bug in our code on the Bitcoin Core side that a failure to grab a lock would be treated as that block being invalid and things would have been somewhat but not all that different if we wouldn't have had that bug.

SPEAKER_05: So the crucial difference there is that the block failed, but instead of attributing that to a local failure in your own system, you attribute it to a consensus failure.

SPEAKER_00: correct and it would just permanently mark the block as invalid when it somehow needed too many locks. This was non-deterministic across platforms and as we later found out even exploitable because during a reorg the whole reorg would be done as one atomic update which means that the number of locks you need is actually even proportional to the size of your reorg and this means that by feeding different forks to different nodes you could probably have always before 0.8 selectively forked nodes off by triggering this behavior. So what happened was 0.8 which switched to a completely different database model as well as leveldb which is a local database with no locking whatsoever bdb is a cross process database system so what happened of course was someone produced a block that for a wide range of nodes on the network exceeded the number of locks that were needed. The network rejected the block but the miner that created it as well as a majority of other miners were all happily continuing because they were on 0.8 that had no concern about these locks so what had happened was we had unintentionally removed a consensus rule which was already inconsistent but still it shouldn't have been removed without being aware of it and thereby actually introduced a hard fork.

SPEAKER_03: Hmm

SPEAKER_00: It's debatable whether it is a hard fork, given that the old code was actually inconsistent with itself all the time. In any case, it caused an actual consensus failure on the network. Miners quickly agreed to temporarily revert back to 0.7, which allowed overriding a chain with one that everybody would accept. 0.8.1 was released that in 0.8 added something simulating the locks limits that BDB had in the hope that people could use 0.8.1 that had the same restrictions or at least similar restrictions.

SPEAKER_05: so they wouldn't be creating blocks that old nodes would.

SPEAKER_00: But I don't know how, and then this was temporary, I believe, two or three months later, this rule expired. And I believe it took until August 2013, until another block was produced that might have triggered the 0.7 issue, but by then the network had largely updated to 0.8 and later versions.

SPEAKER_05: Wow, okay. There's really a lot to dig into in in all of that My first reaction would be I'm a little bit hesitant to call that a hard fork. Yeah, I wish I think you said yeah That's very simply because well, I don't think the word hard fork has much meaning in this context really

SPEAKER_00: Yeah, I agree Let's keep it at an unintentional consensus failure

