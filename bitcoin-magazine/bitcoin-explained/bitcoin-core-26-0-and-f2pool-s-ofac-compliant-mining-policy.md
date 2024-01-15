---
title: "Bitcoin Core 26.0 (And F2Pool’s OFAC Compliant Mining Policy)"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://bitcoinexplainedpodcast.com/@nado/episodes/episode-85-bitcoin-core-26-0-and-f2pool-s-ofac-compliant-mining-policy-ainlt
tags: []
speakers: ['Sjors Provoost', 'Aaron van Wirdum']
categories: ['podcast']
date: 2023-11-23
---
Speaker 0: 00:00:20

Live from Utrecht, this is Bitcoin Explained.
Hello Sjoerd.

Speaker 1: 00:00:25

What's up?
Welcome back.
Thank you.

Speaker 0: 00:00:28

You've been back for, do you even live in this country still?

Speaker 1: 00:00:31

I certainly do.
Yes.

Speaker 0: 00:00:32

You were gone for like two months?

Speaker 1: 00:00:33

No, one month.

Speaker 0: 00:00:36

One month, a couple of conferences.
Where did you go?

Speaker 1: 00:00:40

Too many conferences.
In fact, Bitcoin Indonesia, Nastrasia in Tokyo.

Speaker 0: 00:00:45

Well, but the thing is before that you were in the States for a while and you were in Portugal.

Speaker 1: 00:00:49

I was, but I was home for a few weeks in between.

Speaker 0: 00:00:51

All right.
Well, you were gone for so long that there's a new Bitcoin Core release.

Speaker 1: 00:00:55

That's right.

Speaker 0: 00:00:56

Bitcoin Core 26.
But before we get into it, so that's what this episode is going to be about.
George, we're going to discuss Bitcoin Core 26.
Cool.
But there's been some recent developments that you suggest that we briefly touch on before we get there.

Speaker 1: 00:01:10

Yeah, I think so.
So remember, dear listeners, if you listen to episode 37, back in 2021, we talked about MaraPool, which at the time was making blocks that they said were OFAC compliant.
As far as we know they did not actually do any filtering but this triggered a developer which we will call 0xb10c to write a tool that monitors the blockchain for said censorship just in case that would ever happen.

Speaker 0: 00:01:46

Yeah, So just to reiterate what this all means, there is an OFAC list and this, and this means there are entities on there that you're not allowed to act with.
And that's the US government sanctioned list.
Is that the right way to think about it?

Speaker 1: 00:02:02

Yes, correct.

Speaker 0: 00:02:03

So these would include people that the US government does not like, essentially.

Speaker 1: 00:02:08

Yes, these are only people that the US government does not like.

Speaker 0: 00:02:11

Right, and there are Bitcoin addresses on this list?

Speaker 1: 00:02:14

Yeah, so I think the general idea is that they say, Hey, this guy and this guy, you should not do business with them.
And this is how you recognize them.
And they'll spell out their name in like five different ways.
And give maybe some known addresses.
And they might also give some known Bitcoin addresses that are associated with this person.

Speaker 0: 00:02:31

Right.
So there are Bitcoin address on this list.
And if you want to send Bitcoin to or from these addresses, then so what MarathonPool was doing was they would essentially filter these transactions and not include these transactions into a block.
That's how they would comply with this list, right?

Speaker 1: 00:02:49

Yeah, but they didn't actually do that.
I think they were thinking about doing that.
And they put some operatory message in the block.
But we explained that back in that episode.
Because as far as I know, they didn't actually do any filtering.
But it cost quite a lot of consternations and they backed out of that idea.
I think they even replaced their CEO, though that may have been completely unrelated.
But anyway, it was enough motivation for him to write this tool.
And what this tool does is it basically runs a Bitcoin Core Fullnode and a Bitcoin Core Fullnode will propose a block.
Basically, it just every 10 seconds creates what it thinks would be a correct block.
It doesn't do the proof of work, it just constructs the block.
And then when a real block appears, it compares it.
It looks at which transactions are missing that were expected to be in the block and which transactions are not missing.
And then for the transactions that are missing it would run it against a bunch of heuristics of why it might be missing.
Usually it's completely innocent.
So for example a transaction might be very new, maybe your node has heard about it one second ago, then it's very likely that other nodes have not heard about it yet, so it's not surprising that it's not in a block.
Something else that tends to happen especially these days is that miners will have an accelerator service where they will prioritize transactions that if you look at their Bitcoin fees they should not be in the block but they are in the block because they've paid through credit card or some other way to be included in the block.
And so basically some of the tools automatically filter some of these things and other times you basically wrote a blog post about it doing it manually just checking out what's going on here.

Speaker 0: 00:04:32

Okay, so what is going on here?
Why are we discussing this?

Speaker 1: 00:04:35

Well what seems to be going on here is that there are four transactions by F2Pool which...
Transactions by F2Pool?
Well transactions not by F2Pool.

Speaker 0: 00:04:45

Transactions not included in a block by F2Pool.

Speaker 1: 00:04:48

Exactly.

Speaker 0: 00:04:48

Right.

Speaker 1: 00:04:49

Four of them.
And if you look at each four of them, I believe two or three of those, there's not a good explanation of why they're not in a block.
Could still be innocuous, but they're not recent transactions.
They're not pushed out because other transactions were prioritized, etc.
And then the explanation that would remain is that they were filtered because they were on that list.

Speaker 0: 00:05:13

So they are on that list.

Speaker 1: 00:05:14

They definitely are on that list.
That's not the problem.

Speaker 0: 00:05:17

Okay, got it.
So censorship is upon us.

Speaker 1: 00:05:20

Well, yes, but we didn't know for sure, I guess.
We could just do the analysis, but then there was a tweet by, I guess, the person in control of F2Pool.

Speaker 0: 00:05:36

Wangchun?

Speaker 1: 00:05:37

Yes, who says, will disable the TX filtering patch for now until the community reaches a more comprehensive consensus on this topic.
So basically… So that is

Speaker 0: 00:05:47

a confirmation that he was in fact filtering out OFAC transactions in breach of the OFAC list.

Speaker 1: 00:05:54

Yes, or at least some of them because it's not clear if he was filtering all of them.

Speaker 0: 00:06:01

But where does this patch even come from?
Like is this a patch?

Speaker 1: 00:06:04

Presumably just self-written.
Can I download this patch?

Speaker 0: 00:06:06

Okay.

Speaker 1: 00:06:06

No, you'd have to write it yourself.
You'd have to do something like if this transaction arrives...

Speaker 0: 00:06:12

Bitcoin Core does not offer this patch.

Speaker 1: 00:06:14

No, But I guess you can write a patch that keeps things from going into your mempool.
I don't know if we have a way to get things out of your mempool once it's in there.

Speaker 0: 00:06:24

Anyways so Wangchun F2Pool was using a patch, maybe self-written, maybe not, to filter these transactions out of blocks to comply with the OFAC list.
And now he's… Well,

Speaker 1: 00:06:39

we don't know if it was to comply with the OFAC list.
Josh, why

Speaker 0: 00:06:41

are you hedging everything so much?
It's pretty obvious at this point, right?
You did the analysis.

Speaker 1: 00:06:46

No, because there are some unconfirmed tweets that suggest that...
And he

Speaker 0: 00:06:49

confirms it on Twitter.

Speaker 1: 00:06:50

Yeah, but there are some other unconfirmed screenshots of tweets that suggest that Motiv may have been slightly different.
But in any case, we know that these transactions were deliberately filtered.

Speaker 0: 00:06:58

But what's the alternative motivation?
Well, it

Speaker 1: 00:07:00

might be that he just doesn't like those particular people.

Speaker 0: 00:07:03

He just doesn't like the same people that the US government doesn't like.

Speaker 1: 00:07:06

Yeah exactly.

Speaker 0: 00:07:07

Okay but then still he's filtering transactions.

Speaker 1: 00:07:09

Yes.
Like there's still

Speaker 0: 00:07:10

some form of censorship happening right?

Speaker 1: 00:07:12

Exactly but there could be two different reasons for censorship right?
One is you're afraid of some government like the US government making your life difficult and the other could be well you think the US government is actually right.

Speaker 0: 00:07:22

Okay.
But we

Speaker 1: 00:07:22

have no idea which of those two is the true motivation.
I'm just saying either is possible.

Speaker 0: 00:07:26

Sure, sure.

Speaker 1: 00:07:27

Either is problematic.

Speaker 0: 00:07:28

Are we talking about this because we should be worried about this?
Is your opinion that we should be worried about this?

Speaker 1: 00:07:32

I think we talked about that in the earlier episode, that I am worried about this in the long run.
Now in the short run it's absolutely not a problem, because these transactions were just mined by another miner, the next block.
Ironically by a US miner.

Speaker 0: 00:07:46

Yeah, maybe it's a bit much to go over this whole thing again.
Again, we discussed this in episode 37, you said?
Yes.
Yeah, so that's what we discussed, I guess, in depth.
How worried we are about it anyways.
Short term, So now it's turned off.
I guess the other thing maybe worth mentioning is, so this is something that…

Speaker 1: 00:08:07

So the fact that we were able to detect this at all is because of all this tooling, it's not that obvious normally because transactions, sometimes they appear in a block, sometimes they don't.
So that's pretty cool that we have the tech to detect it.

Speaker 0: 00:08:22

Yeah, well another relevant episode perhaps to listen to in this context is the episode we did on Stratum v2, because Stratum V2 is kind of a solution for this problem if we consider it a problem, right?

Speaker 1: 00:08:36

Yeah, what Stratum V2 does that's relevant here is that it delegates the responsibility of putting things into a block, not to the mining pool, which tends to be quite large.
You know, there's two pools that are 51% roughly of all the hash power, but it delegates it to individual miners.
So, and that's far more of them.

Speaker 0: 00:08:56

Yeah.
So we discussed that in episode 80.
Okay.
That's a, this was a long intro.
I guess the reason this is worth bringing up is because, I mean, it seems.
This is kind of the thing that Bitcoin, Bitcoin developers and journalists, maybe as well, sometimes have been like talking about and warning about for many years, and this is sort of the first time it's actually happening.
So there's actually a reason now for… If

Speaker 1: 00:09:22

you go through, you know, this, if you just assume a slippery slope, which is always a problematic type of argument, but if you do, then The ultimate outcome of this is you're back to PayPal because all transactions have to be KYC'd in permission before they go into a block.
Now we're nowhere near that, but does this make sense to worry about this?

Speaker 0: 00:09:39

Right, it is sort of a first step in that direction and it's interesting to see how things will play out, I guess.
So the first step we now saw is that Wankyun disabled his patch.
But yeah, it's an event in that sense.
Like it's a beginning of something that could go in a very wrong direction, even though it's only a very small step right now.
Right?
Is this, are we done with this?
This was the intro to our Bitcoin Core 27, wait, where are we?
26th episode.
Okay, let's talk about Bitcoin Core 26 then.
Yes.
First of all, I think everyone knows this by now.
Actually, I'm not even going to ask you about this anymore.
I'll just preface this.
So the way it works, Bitcoin Core releases a new version of the software every six months.
And that means that every new future that was done within the six months is in Bitcoin Core.
And that's, that means that's a new release.
There is not a new release because there is a new future.
There's just a new release and whatever is new is new.

Speaker 1: 00:10:42

That's right.
Yes, exactly.
So yeah, so there are no like things that must be finished before the deadline.
Whatever is ready is ready.

Speaker 0: 00:10:49

Right.
So the last release was about half a year ago, apparently, right?
At this point, where are we in the release process?

Speaker 1: 00:10:58

There have been two release candidates.

Speaker 0: 00:11:00

As far

Speaker 1: 00:11:00

as I know, the second candidate does not have many problems, so maybe it's the last one, maybe there'll be another one.

Speaker 0: 00:11:07

Right, so potentially the new Bitcoin Core release could be announced, released any day now.

Speaker 1: 00:11:13

Exactly.
Okay.
Or maybe a few weeks.
What's interesting perhaps is that there is a testing guide.
Now every release there is always a testing guide but this one apparently has had some extra love and attention.
If you've ever wanted to test a release you should look for the, I think if you Google Bitcoin Core 26 release testing guide, you'll find it and hopefully it'll be in our show notes.

Speaker 0: 00:11:35

Who is this for?
This is for developers, I would assume.

Speaker 1: 00:11:38

I would say a little bit lower barrier to entry than being a developer.
Anybody who can download a piece of software and carefully follow instructions.

Speaker 0: 00:11:46

What are you testing?

Speaker 1: 00:11:48

You're testing things that have changed.
So there's all the features that we're talking about, but there's also lots of smaller changes and the testing guide will basically take you through some of the changes and how you might go about testing them.
Of course, you should also test things in a way that's not in the guide.

Speaker 0: 00:12:02

How would you go about testing them?
Like what, can you give an example of what we're talking about here?

Speaker 1: 00:12:08

Yeah, well, I guess we can do that when we cover the actual changes.

Speaker 0: 00:12:12

Okay, sure.
Do you want to get into the actual changes?
Sure.
Okay, so the actual change.
So what we did, well, mostly short to be honest, is you picked out a couple of features in this new release that are noteworthy.
Even more, like you picked out the most noteworthy of the most noteworthy changes.
Right?

Speaker 1: 00:12:36

I just picked the ones that I thought were cool.

Speaker 0: 00:12:38

Okay.
So the first one, oh yeah.
And we mentioned some of them in our previous episode, actually, because in the previous episode, which I guess by now is two months ago, We did mention some new inclusions in Bitcoin Core, or you did already.
So we'll sort of repeat these for whoever missed that episode or just to give a complete picture.
So the first one is peer-to-peer transport encryption.

Speaker 1: 00:13:01

That's right.

Speaker 0: 00:13:02

What's the BIP number for that again?
Do you remember?
Do you know?
No. It's not BIP 151, right?
That one was replaced?

Speaker 1: 00:13:09

No, it's a new one.
It's peer-to-peer encryption.
So we did a whole episode on this, episode 77.
That really explains why you want to do this.
But the short version is that nodes will encrypt their traffic between each other so that the especially internet providers cannot simply just listen to what you're doing.
This is actually very easy to test.
It's also something that's not on by default but as part of testing you might want to turn that on.
So roughly the way you would test this is you download Bitcoin Core, the new version, you turn this feature on by changing the configuration setting And then your friend also downloads Bitcoin Core, also turns this feature on, and now you try to connect to them.
So in Bitcoin Core normally it automatically finds peers, but you can manually say, hey, please connect to this IP address.
And then you can actually get something called a session ID.
It should be in the instructions, but basically you'll be able to see a number just like with Signal, a long number, and if you compare that long number with what your friend sees as a long number, then you know that you are directly connected to them.
There's not a man in the middle.
So that's the kind of thing you can test.
And it'd be very worrying if the number was different, that would indicate a bug.
Or somebody spying on you, but probably a bug.

Speaker 0: 00:14:27

Okay, well, let's linger here a little bit, because now you spoke about testing and we did discuss it in previous episodes, but still.
So right now Bitcoin Core nodes, they, you know, they're part of the peer to peer network, so they communicate with each other, which specifically means they send transactions and blocks to each other.
And right now they do that over an unencrypted channel.
They just, it's just plain text.
It's just plain information.
Right.
So that means that, that internet service providers can see exactly which transactions and blocks you're sending.
And I guess the main problem is that this would allow ISPs to sort of see where transactions originate.
Is that the main problem?
Yeah, I'd say that's

Speaker 1: 00:15:09

one problem.
And the other is it makes censorship easier because if it's very easy to detect that it's a Bitcoin node, it's also very easy to block it.
Now that's still easy with this encryption in place for other reasons, but having encryption, it makes it one step easier to get around censorship.

Speaker 0: 00:15:25

Okay.
That, yeah, that's, that's basically it, right?
That covers this.
Okay.
So this is now in Bitcoin Core, but it's optional?

Speaker 1: 00:15:34

Yes.

Speaker 0: 00:15:35

So you can switch it on.
And is there preferential, or did you just explain it?
Is the preferential seeking of other nodes that do the same thing?

Speaker 1: 00:15:44

Yes.
No, it's not preferential.
But if it happens to connect to another node and it knows that it has this feature, it will use it.
But it's not preferential.

Speaker 0: 00:15:53

Okay, so it still connects to other nodes randomly, but they will first sort of try, hey, are you using encryption?
No, they will only

Speaker 1: 00:16:01

try if they think the other side can use it.

Speaker 0: 00:16:03

Oh, so how do that?

Speaker 1: 00:16:05

So how

Speaker 0: 00:16:05

would my notes think that your note is using encryption?

Speaker 1: 00:16:08

So we talked about, I think in episode two or three, we talked about, how nodes bootstrap and, and learn about other notes.
So they learn about nodes by having a list of IP addresses to connect to, but in addition to those IP addresses there's also some metadata of which features these nodes support.
So in your long address book of potential nodes to connect to is information like is this a prune node or a full node, does it have specific bloom filters or whatever filters you want.
And as of now, it also tracks whether the node supports v2 transport.
So if your address book says that this other node supports that new feature, which could be a lie, but at least that information would be there, then he'll try that first and if it fails, just tries the v1 connection.
Now I guess in the future we might turn that around and just always try the v2 and then fall back to v1 if it doesn't work.

Speaker 0: 00:16:59

Yeah, why wouldn't you just always try it?
Just because it has extra data to communicate?
Like this extra try, like why wouldn't you just by default first try encrypted?
Encrypted?

Speaker 1: 00:17:10

Because if you first try encrypted and it, and the other side does not support it, the other side will hang up on you.
So you have to connect again.
Which is not the end of the world but right now the majority of the network doesn't support it so that means all of your connections would fail and you'd retry.
But I don't know if that's a big enough deal in the long run so it might be turned around just try it.

Speaker 0: 00:17:31

Yeah I would assume eventually the goal is that everyone would use this right?
Are there any downsides to using this?

Speaker 1: 00:17:38

Well there is now because it's too new so if something goes wrong your note might simply fail to connect or get hung up on by all of its peers and you don't get the latest blocks, right?
So right now it's not safe yet, but in the long run I don't think there's any downside.
It was designed to not have downsides, in the sense that it's actually even a little bit faster than the original protocol.
You'd think it'd be slower because it's encrypted, but the original protocol uses checksums to make sure that the messages are correct, and those checksums use SHA-256, which is very slow, and the new algorithm uses a quicker checksum.
So it's better in, hopefully in every way, if it's not broken.

Speaker 0: 00:18:17

Right.
So how, if I download Bitcoin Core 26, how do I switch this on?

Speaker 1: 00:18:22

You go into your Bitcoin.conf settings file and then you turn on, I think you enter v2 transport equals one, but it'll be in there, either the release notes or the testing guide.

Speaker 0: 00:18:33

Right.
Alright, moving on to the next point.
Assume UTXO was implemented for Cignas testnet?
Not mainnet, right?

Speaker 1: 00:18:42

That's right.

Speaker 0: 00:18:43

Okay, so what is Assume UTXO again?

Speaker 1: 00:18:46

We covered that in episode 14, so that's quite a while ago.
It's basically the short version of it is that instead of starting at the genesis block when you start your node and going all the way to the most recent block, which takes a long time, you start at a snapshot and you assume that it's valid and then you go from this snapshot which might be a few months ago to the present to the tip and then once you've done that you you start from the genesis block and in the background you check all the blocks and you make sure that you indeed arrive at this snapshot that you assumed initially.

Speaker 0: 00:19:20

So the benefit here would be that you can start using the Bitcoin Core node before fully syncing?

Speaker 1: 00:19:27

Yes, you would basically sync only the last 10% of the blockchain and you would be immediately able to use a wallet, receive coins, send coins, but there's still some chance that your starting point was wrong.
And what could go wrong then is let's say there's some malicious developers and they just create fake coins.
Well, now you think you've received coins, but these coins don't actually exist.
Now that's a really, really expensive attack, right?
Because somebody still has to make a block with enough proof of work that is wrong according to all the other nodes, but only correct according to you or the list of victims that they have.
So I don't think that attack is super realistic, but we still want to...

Speaker 0: 00:20:09

Plus you need to, plus the developers need to be corrupt, obviously.

Speaker 1: 00:20:12

Yeah, so this depends on the distribution mechanism.
Right now the idea is that the correct block is hard-coded into the source code, so you would indeed have to compromise the developers.
You could, we could still change that approach.
I don't know if it'll be changed, but the approach could be that, no, you can just use any block and the developers do not bless any of the blocks.
Because it's the downside of the developers blessing the blocks is that, well, now if you compromise the developers, you're screwed.

Speaker 0: 00:20:41

The upside is that...
How would you use any block?

Speaker 1: 00:20:44

You basically, Bitcoin Core wouldn't care.
You would just give it a block, say assume this one is correct.
You just download that from somebody on the internet that you trust.

Speaker 0: 00:20:53

And

Speaker 1: 00:20:53

then you'll find out if it was right or not, but it'll take a while.

Speaker 0: 00:20:56

Right, I see.
And obviously, so- So that

Speaker 1: 00:21:00

means there's no centralized group of people to pressure or to corrupt.
But the downside is you will get scammed left and right because everybody can just make their own fake one.

Speaker 0: 00:21:10

Yeah.
Okay.
Interesting.
So wait, so which version is implemented in Bitcoin core right now?

Speaker 1: 00:21:15

The blessed one.

Speaker 0: 00:21:17

Okay, the developers have blessed it.
Yeah.
Okay.
So yeah, you mentioned...

Speaker 1: 00:21:22

And for testnet and Cygnet, obviously, that's fine.

Speaker 0: 00:21:25

Right.

Speaker 1: 00:21:25

But it's also not, there's also no theft risk there.

Speaker 0: 00:21:28

Right.
It's only on testnet now, and Cygnet, which is a version of testnet.
So yeah, so you mentioned, even if it would be on mainnet, the attack would be expensive because you need to create a fake block and you need to, at least in the current version, corrupt the developers.
Plus it would only work temporarily because it's kind of a stopgap until you've actually synced from

Speaker 1: 00:21:50

yeah basically once you've synced from the genesis block the note would crash

Speaker 0: 00:21:54

it's kind of a yeah right it's sort of a solution until in the meantime yeah and therefore it's obviously also optional you can just opt to actually wait until it's fully synced before you receive any transaction.

Speaker 1: 00:22:05

Although in that case you should just not use the feature.

Speaker 0: 00:22:08

Yes well that's what I'm saying the future is basically optional.

Speaker 1: 00:22:12

That's true in general yes.
So if you wanted to test this, again you download BitConcord, then you obtain the SIGNET or the TestNet snapshot.
There's some links to Torrents I believe.
And then you just run one command and you'll see it in action.

Speaker 0: 00:22:28

Okay, so that's also new in BitConcord 26.
On to the third point.
The third handpicked selection by Shortz is network diversity.
There's a new upgrade in updated network diversity tools.
What's going on Shortz?

Speaker 1: 00:22:47

Yeah, so I believe if I understand this feature correctly, and I did not read it up in detail, it's been a while, but here's the thing.
Bitcoin Core will connect to about eight nodes, will make connections outbound to about eight nodes.

Speaker 0: 00:23:01

That's the default?
Eight is the default?

Speaker 1: 00:23:02

Yes, it might be 9 now but and then other nodes might connect to you but if you're behind a router etc then that won't happen.
Now those 8 nodes by default would just be on plain internet, IPv4, IPv6, but if you want to you can also connect to Tor nodes if you turn Tor on.
Now if you don't do anything you may or may not have a connection to a Tor node and if you have one and you lose that connection because they hang up on you or something goes wrong, then you're just going to connect to a new node and maybe it's a Tor node, maybe not.

Speaker 0: 00:23:36

Wait, if I'm using Bitcoin Core, which I am, but I haven't explicitly made any sort of change to connect through Tor, can I still connect to other Tor nodes?
No, right?

Speaker 1: 00:23:46

No, you have to turn something on to do that.

Speaker 0: 00:23:48

Okay, got it.
Okay, go on.

Speaker 1: 00:23:49

But once you have turned it on and you, but you let the VidCon core node automatically handle what it connects to, you may or may not have a connection to another Tor node.
And if you have a connection to another Tor node and you hang up on that one, or they hang up on you, maybe you won't have it again.

Speaker 0: 00:24:03

Right, so what you're saying is I'm connected to eight nodes, one of them is a Tor node because I switched the thing on that allows me to connect to Tor nodes.
Now this guy's internet, Wi-Fi fails, whatever, I'm disconnected with him, So now I'm going to reconnect randomly to another node, which may or may not be a Tor node.
So it's possible that I'm connecting to not a Tor node, and now I'm not connecting to any Tor node.

Speaker 1: 00:24:25

Yeah.
So basically the Tor feature so far just does not guarantee that you actually connect to a Tor node.
You may or may not.
And so this new change makes sure that you do.

Speaker 0: 00:24:35

It

Speaker 1: 00:24:35

makes sure that at least, I don't know what the percentage is, but let's say at least one connection will go to Tor if you have Tor on.
And it will basically, if that connection disappears it will make another one.

Speaker 0: 00:24:45

And so the way I would do this again is I go into the config file and I say...

Speaker 1: 00:24:49

No, this just works.
This just works.
Out of

Speaker 0: 00:24:52

the box.

Speaker 1: 00:24:52

If you have Tor on, yes, this just works.
Tor does not work out of the box.

Speaker 0: 00:24:57

Sure.
Okay, so what's the...
So This will basically guarantee that I'm going to connect to a TOR node if I want that.

Speaker 1: 00:25:04

Well, assuming there is one that you can connect to at all, but it will try.
And now, what's the benefit?
This solves a problem known as eclipse attacks.
And we have done previous episodes, too, about eclipse attacks.

Speaker 0: 00:25:15

Also probably very early on, I think.

Speaker 1: 00:25:17

Yes, I forgot to write down the numbers, but you'll find them.
Basically in Eclipse Attack the idea is that some evil person makes sure that your node only connects to them.
So you think you're connected to 8 different peers, but you're not, you're connected to the same person because they have eight different IP addresses and tricked you into connecting to them.
I'll explain all that.
Now if you also connect through Tor, this attack becomes more difficult because they might be able to trick you into connecting to them through normal IP addresses but they may not be able to trick you into connecting to them through Tor.
Or if they're making the connections to you, they might not know your Onion address that they're connecting to.
They only know your normal IP address.
Yeah.
So that's why this helps.

Speaker 0: 00:25:59

It's kind of a safeguard.
Like Eclipse attacks themselves are kind of unlikely to happen.
There are more tools against that, right, in Bitcoin Core?

Speaker 1: 00:26:08

Yeah, I would also say Eclipse attacks, you know, again, in order of Eclipse attacks are getting more and more difficult.
And if you want to do them, You probably want to have a motive, like you want to be able to scam somebody into accepting your payment and then double spending them and working with miners and all that stuff.
They're not easy attacks, but we like to make them impossible or harder.

Speaker 0: 00:26:27

So Tor is kind of a lifeline to still get the latest blocks in case they're being censored in some sort of eclipse attack scheme.
Yeah, exactly.
Okay, so this is also new in Bitcoin Core.
You'll… so network diversity is embedded more and more thoroughly.
Then I'm seeing you selected, there's a Taproot Miniscript upgrade.

Speaker 1: 00:26:52

Yes, so we covered Miniscript in episode 4.
A very long

Speaker 0: 00:26:56

time ago.
Really?
Yep.

Speaker 1: 00:26:58

One of the first things we did.
So what's the TLDR of Miniscript?
It is a subset of script, you could say.
So not all of Bitcoin script, but a part of Bitcoin script that has been handpicked by super wizards like Andrew Polstra and SIPA to make sure that you don't shoot yourself in the foot.
And that you can combine pieces of script.
Like two pieces of script and you put and in between it etc.
So these allow you to do complicated fancy wallets with like okay I want two signatures but after one year I only want one signature etc.
And this worked, This has been added to Bitcoin Core a year ago or so in various steps, which we've covered in earlier episodes.
And the latest step is that you can now also use Miniscript with Taproot.

Speaker 0: 00:27:45

Right.
And what is the benefit?

Speaker 1: 00:27:48

So the benefit of Taproot in general…

Speaker 0: 00:27:50

Maybe should I first, for those that didn't follow that, so yeah, Bitcoin transactions use scripts, so it's basically a programming language for Bitcoin, allows you to lock Bitcoins up in all sorts of creative ways, time locks, multi-stick, whatever.
A mini script is a way to sort of simplify that.
And it's really for developers, right?
Like I'm not going to use it.
It's for people like you and.

Speaker 1: 00:28:13

It's for developers or for wallets that have been written by very small developers and that do it for you in the background.

Speaker 0: 00:28:19

Right.
But with regular script, it's kind of easy to make mistakes and lose coins.
And with mini scripts, kind of the most common ways to make these mistakes are just ejected.
Like you can't use this.
Only the simple stuff is left.
And because of that, you can actually make fairly complex things relatively simply and safely.
Yeah.
Okay.
So this was already available in Bitcoin Core.
So what this means specifically is I think you can connect wallets that use this to Bitcoin Core.
I don't think I'm saying that right.

Speaker 1: 00:28:55

Can you

Speaker 0: 00:28:56

say that right?

Speaker 1: 00:28:56

That's true, yeah.
So, well, the Bitcoin Core wallet supports Miniscript.

Speaker 0: 00:29:00

Right.

Speaker 1: 00:29:00

But there's no like graphical way or anything in the interface where you can do that.
You'd have to manually type these pieces of mini script.
But there are wallets out there that will connect to Bitcoin Core using the RBC, for example.
And they might use the Bitcoin Core wallet for the key storage, et cetera.
But they would have some graphical user interface and they would construct a mini script.

Speaker 0: 00:29:21

So where, I think I'm skipping ahead.

Speaker 1: 00:29:25

So where Taproot comes in.
I don't

Speaker 0: 00:29:28

want to go there yet.
Where is this?
I don't know how else to ask it.
Is this in the Bitcoin Core wallet or is this in the Bitcoin Core like node software?
So where do I find whatever we're talking about?

Speaker 1: 00:29:40

Well, the mini script lives in the Bitcoin Core wallet.

Speaker 0: 00:29:43

Yes.
So this, Okay, so we're talking about a Taproot upgrade.
Let's go there then.
Yeah.
So now this has been made available in Taproot.
So is this an upgrade in the Bitcoin Core wallet?
Yes.
Okay, got it.
So what's the upgrade?

Speaker 1: 00:29:58

So the upgrade is that you can now use this mini script, so these safe pieces of script, not just in SegWit, in regular SegWit, which used to be the only thing, but you can now also use it in Taproot scripts.
And remember what's nice about Taproot scripts is you can have all these multiple ways that you can spend a coin, you can now hide all the ways that you're not using by putting them in different leaves.
So your wallet would basically know that, okay, there are five different subscripts, essentially, that are possible, and the user will tell me which one of these five to use when I want to spend this coin and will hide the other ones.
And there were some like, there's some subtle changes between the scripts in Taproot and the scripts in SecWit before some limits were dropped, but that's not that important.

Speaker 0: 00:30:42

Right.
It's just, It's basically just the benefits of Taproot are now available in combination with Miniscript in a Bitcoin Core wallet.

Speaker 1: 00:30:50

Yes, but either you will have to write your little Taproot Miniscript yourself and put it in the wallet.
Once you've put it in the wallet, by the way, it just works, right?
You just click on receive new, make new address, it'll show an address, looks like any other address, and you'll be able to spend from it and it'll just work.
But you generally do not want to type mini script yourself, even though it's safer than regular script, you probably want to use some other tool that does that for you.

Speaker 0: 00:31:13

Right.
So this is available in Bitcoin Core now, Bitcoin Core 26.
Well, I say now, at the time of recording, we're still in.

Speaker 1: 00:31:21

Yeah, I don't know if this is in the testing guide.
Maybe it is, that would be pretty cool.

Speaker 0: 00:31:26

Who's gonna benefit from this?
Are there any Wallets that use this right now or that want to use this?

Speaker 1: 00:31:32

I think Liana Wallet wants to because they're trying all sorts of fancy multisig, yeah, multistage multisig things, right?
What's it called?
Multisig.

Speaker 0: 00:31:42

No, the wallet.

Speaker 1: 00:31:44

Liana.

Speaker 0: 00:31:44

Liana.
Have I heard of this?
I don't think so.

Speaker 1: 00:31:46

Wizard Sardine is the company.

Speaker 0: 00:31:48

Oh yeah, yeah, yeah.
Okay, Kevin.

Speaker 1: 00:31:51

Yeah, and they do a lot of work on Miniscript in general to contribute back.

Speaker 0: 00:31:55

Yep, that's true.

Speaker 1: 00:31:57

But hopefully, and I know for example that there's other wallets that support Miniscript already, But the hard part is the setup part, I would say.
So many wallets might be able to sign Miniscript, even hardware wallets, but they will not...
Like, once you've put it in there, it's not that easy to make these wallets in the first place.

Speaker 0: 00:32:21

Right.

Speaker 1: 00:32:23

Okay,

Speaker 0: 00:32:24

last point I think.
We're going to the last point, the last mentionable upgrade in Bitcoin Core 26.
Submit package RPC, you wrote down.

Speaker 1: 00:32:35

Yeah, I believe in previous episodes, we have talked about the idea of package relay for transactions.
So then the simplest example is, I have a Lightning channel, I want to force close that Lightning Channel.
My partner of the Lightning Channel, or no longer partner of the Lightning Channel, is offline.
So all I have is the last time we co-signed a transaction, and this was before ordinals were invented, and fees were super low.
And so I try to broadcast that transaction, but it simply does not even go into the mempool of my peers.

Speaker 0: 00:33:06

We have a solution for that though.
You can use child pays for parent shorts.
That's right.
The only problem is that the child...
Hang on, let me explain the solution.
So the solution is I'm going to spend the money from this transaction to myself with a higher fee.
So now the miner will see that if he wants to confirm the high fee transaction, he'll also have to confirm the low fee transaction and I'll get the money and the problem is solved.
Correct.

Speaker 1: 00:33:32

Yes.
And the miners already do this as far as I know.
The problem is getting it to the miner.
Because this is where the bureaucrats come in.
You basically go to your peers in the network and you say, here's the transaction, but hold on one second, I've got another transaction.
But no, no, no.
Your peers say, no, this transaction is too low of a fee.
But wait, I have this other transaction.
Here's the other transaction.
Well, that has a really high fee, thank you.
But it's spending a transaction that I've never heard about.

Speaker 0: 00:34:01

Yeah, hang on, you got to emphasize.
So when they say this has not enough fee, the fee is too low.
What they even mean is the fee is too low for the mempool.

Speaker 1: 00:34:11

They're

Speaker 0: 00:34:11

not even going to include it in the mempool.
Yes.
So yes, it would not fit in the block.
Now that's fine because it usually goes into the mempool and then you can use the child pays for bear tricks that I explained.
But in this case the transaction because of all these ordinals isn't even gonna fit into the mempool and therefore it's not gonna be seen by anyone and therefore the higher fee transaction is not going to be seen by anyone either because it's not spending funds from a transaction that anyone is seeing.

Speaker 1: 00:34:39

Yeah, because mempools only process transactions one by one and if the first one doesn't pay enough fee, it's not going in there.

Speaker 0: 00:34:45

Right.

Speaker 1: 00:34:46

So, what is the solution?
It is You need a way to send two transactions at the same time to your peers.

Speaker 0: 00:34:53

So peers and miners will consider them in tandem right from the get-go, before it even goes in the main pool essentially.

Speaker 1: 00:34:58

Yeah, and this thing is called Package Relay and work is in progress to do that.
It's not easy and we've discussed some baby steps in that direction.
One of the first baby steps was the RPC called Submit Package and the idea was to send transactions to your own mempool, so not to your peers just your own mempool.
And I think half a year ago or so we covered how that worked.
You would give this RPC two transactions and it would just basically reject it because it would use the same logic as always, it would process them one by one.
So why was that added?
Well, because the next step makes it more useful.
Now with the 26.0 release, it will actually consider both of them and therefore include it in its own mempool.
Right.
But not really yet.

Speaker 0: 00:35:47

So this upgrade only applies to...
So if I make two transactions, one of them is a Lofi, one of them is a Hyvi, I can now send this transaction over RPC to my own node?
But that's it, right?

Speaker 1: 00:36:03

Yeah, and you could imagine maybe there would be a website of a miner where you can send it directly to the miner this way and they would use their own RPC.
That's not the future obviously, but you could see some use even of this primitive feature.

Speaker 0: 00:36:17

Right.
So there's now something in Bitcoin Core, it's a baby step, it's a step towards packet relay, right?
That's just a way to think about it.
Yeah.
It's not, it's actually kind of useless in itself.
Or is there, you just speculated about a potential maybe use

Speaker 1: 00:36:33

case of a miner?
Yeah, and the other is like at least it would be in your mempool and so maybe once the fees go down, you know, it's a bit easier to...

Speaker 0: 00:36:38

Rebroadcast it

Speaker 1: 00:36:39

or something.
But rebroadcasting is also not automatic.
So yeah, no, it's not there yet.

Speaker 0: 00:36:44

It's basically useless, but it is a step towards package relay which itself is a useful and important upgrade one day hopefully

Speaker 1: 00:36:53

right yes

Speaker 0: 00:36:55

okay great so these are we've now discussed six five of the most important upgrades in Bitcoin Core.
That's the episode actually, right?

Speaker 1: 00:37:06

That's right.
That's a wrap.
Okay.
Thank you for listening to Bitcoin Explained.
