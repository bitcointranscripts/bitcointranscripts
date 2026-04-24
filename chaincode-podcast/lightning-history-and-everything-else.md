---
title: 'Lightning History and everything else'
transcript_by: 'Hussman256 via review.btctranscripts.com'
media: 'https://podcasters.spotify.com/pod/show/chaincode/episodes/Tadge-Dryja-and-Lightning-History-and-everything-else---Episode-31-e20udtf'
date: '2023-03-20'
tags:
  - 'eltoo'
  - 'lightning'
  - 'segwit'
  - 'sighash-anyprevout'
  - 'trimmed-htlc'
speakers:
  - 'Tadge Dryja'
  - 'Jonas Nick'
categories:
  - 'podcast'
summary: 'Tadge Dryja chats with us about writing the Lightning Network paper and working in the Bitcoin space.'
episode: 31
additional_resources:
  - title: 'On the instability of Bitcoin without the block reward'
    url: 'https://www.cs.princeton.edu/~smattw/CKWN-CCS16.pdf'
  - title: 'Lightning Network White Paper'
    url: 'https://lightning.network/lightning-network-paper.pdf'
  - title: 'LN-Symmetry (Eltoo)'
    url: 'https://bitcoinops.org/en/topics/eltoo/'
  - title: 'SIGHASH_ANYPREVOUT'
    url: 'https://bitcoinops.org/en/topics/sighash_anyprevout/'
  - title: 'hardfork wishlist wiki'
    url: 'https://en.bitcoin.it/wiki/Hardfork_Wishlist#:~:text=The%20Hardfork%20Wishlist%20is%20to,them%20to%20be%20invalid%20blocks'
  - title: 'softfork wishilist wiki'
    url: 'https://en.bitcoin.it/wiki/Softfork_wishlist'
  - title: 'coinpools'
    url: 'https://coinpool.dev/v0.1.pdf'
  - title: 'MAS.S62: Cryptocurrency Engineering and Design'
    url: 'https://dci.mit.edu/research/2019/8/6/take-the-free-mit-open-course-taught-by-dcis-neha-narula-and-tadge-dryja-mass62-cryptocurrency-engineering-and-design'
aliases:
  - '/chaincode-labs/chaincode-podcast/lightning-history-and-everything-else/'
---
Tadge: 00:00:00
You know, it works, but it also worries me because it's like, oh, people are like, oh, I'm sending one sat.
And you're like, yeah, but it works very differently whether you're sending 100,000 Satoshis or one.

0xB10C: 00:00:18
Jonas.
We are back and we're going to have Tadge joining us in the studio today.
What should we chat about with him?

Jonas: 00:00:26
I think maybe lightning stuff.

0xB10C: 00:00:28
Yeah, lightning stuff.
It's lightning history.
I know he's spending a little bit more time working on lightning stuff at Lightspark now.

Jonas: 00:00:34
Oh, you know what?
Maybe we should ask him whether blocks should still be 130 megabytes.

0xB10C: 00:00:39
All right.
In the conclusion of the lightning paper, he talks about 130 megabyte blocks.
So that's where we'll start.

## Could blocks be bigger?

0xB10C: 00:00:55
So we didn't have the mic on, but you started diving in directly into ancient, it's not even that much ancient history.
It's just history at this point.
So bigger blocks, smaller blocks?
What do you think?

Tadge: 00:01:08
I think we shouldn't be dogmatic in that, like, if it's a sort of religious, like Bitcoin only has 21 million bitcoins and Bitcoin has one well really four megabyte blocks like this is dogmatic.
It's like, well, what are we trying to achieve?
Is this the best way to achieve it?
And I think programmable money, right?
You can program it.
And the thing I, the distinction I make that sort of got lost, you know, five, six, seven years ago when everyone was arguing, I think there's sort of an economic reason for the block size and also a technical reason.
And I feel that the technical one is much more variable in that, like, you never know.
What if computers get way better, right?
What if tomorrow AMD is like, hey, we just made some amazing new thing and computers are 10 times faster or 100 times faster or the Internet's 100 times like from physical laws, we know that that's totally possible.
And we are seeing, like I was impressed, last two or three years, like computer chips got better at a rate that they hadn't for a long time.
So you never know.
And that's work I've been doing, like on `Utreexo`.
So a big part of the goal was to try to get rid of these technical limitations, right?
To say like, okay, well, even if you did have 100 megabyte blocks, could you run it with `LevelDB`?
We never really tried that.
That's the problem, because it started with Bitcoin Cash and BSV and stuff.
And those aren't, I don't want to say, but they're not really serious.

0xB10C: 00:02:33
It's not just that, it's other variables have been played with over time with derivations, or even Ethereum, where faster blocks, bigger blocks, better blocks.

Jonas: 00:02:45
It's interesting to watch what BSV and BCash are doing, but the question is how indicative it is of whether we could do it.
Because if you actually then look at the content of the BSV blocks with multiple gigabytes, and it's just millions of times the same dog picture in the block, that's not going to be what sort of block we would see on a network that actually gets used like Bitcoin.

Tadge: 00:03:08
You would see a large `UTXO` set of billions of `UTXOs`, and that's to me a bigger bottleneck.
That's scary, yes.
But also, we're currently at one to four-ish blocks, but the `UTXO` set size really doesn't increase nearly as much as it could.
It could easily go up 50 gigabytes a year, and it's still five gigabytes after 14 years.
And so it's like, oh, okay, well that's not.

Jonas: 00:03:32
I would be very shocked and surprised if it wound up 50 gigabytes per year.

Tadge: 00:03:35
Worst case scenario, right?
If you're just, you know, an attack, like that's the worst case.

Jonas: 00:03:38
Yeah, if we just create outputs all year long, yes.

Tadge: 00:03:41
But you could reasonably see 20 extra gigs a year, right?
Like, that could happen.
It's hard to see, like, well, that sort of feels like an attack as you get towards that.
But it could happen.
And it's sort of like, yeah, we don't know how it works.
I haven't even really tested this kind of thing.
How does it happen?
But so anyway, that's a technical limitation.
We want people to be able to take their old laptop, whatever computer, run a node, verify everything, like have that, you know, security that Bitcoin and Bitcoin Core and whatever gives you, and that's awesome.
And we need that.
It's not worth anything to destroy that.
And then there's the economic aspect where like, well, OK, what if we have really good computers?
Everything works great.
We've got amazing software.
We can handle these things.
But the economic part is, okay, we do want scarcity because that's where the fees come from.

Jonas: 00:04:26
Right.
In the long term, our block subsidy will be leveling off.
We will need some other mechanism to...

0xB10C: 00:04:34
And quickly, I mean...
Exponential! That's how exponential works.
Yeah, pretty soon.

Jonas: 00:04:41
Yeah, and what is it?
We just went past the halfway point of this block subsidy era, and so...

Tadge: 00:04:50
No, wait, next year, 2024 is when it halves, I think.
So we're well into...

Jonas: 00:04:56
Yeah, end of 2022 was the point where we went over 105,000 blocks into the era.
So yeah, end of 2024, I think, is the next halving.

Tadge: 00:05:08
To me, those are very different concerns, right?
Where it's like, OK, we need small blocks so that we incentivize, you know, have fees and keep the security of the system.
And then we need the small blocks because of, oh, I'm currently running an Intel i5 whatever chip.
And that seems very ephemeral.
Computer chips, we're talking about a system we want to run for 100 years.

0xB10C: 00:05:29
Yes and no.
We are talking about people running Bitcoin on Raspberry Pis and whatever else.

Jonas: 00:05:36
We're also talking about people running Bitcoin in areas where bandwidth is more expensive and trying to just keep up with all the blocks is an expense that they have to calculate with.
I mean, clearly there's other ways to deliver the blockchain there, like get a satellite dish pointed at some specific point in the sky and it streams you the whole blockchain in a month.

Tadge: 00:06:0
But so it also is ephemeral in both directions.
Like maybe, you know, because a lot of people on the Internet are like, hey, Bitcoin's great for like when the apocalypse comes or, you know, when the system falls apart or something.
Maybe it gets worse, right?
Maybe we're scavenging through the dump to find 386 chips or I don't know, it's kind of a silly scenario.
I think it's much more likely that computers continue to get better, but it could go the other way.
But I think the technical side is very variable and we don't really know what will happen.
And it's quite possible that you could have an extremely cheap, small, power efficient device that can be used anywhere in the world that can verify Bitcoin like instantly.

Jonas: 00:06:39
Sure.

Tadge: 00:06:39
That could happen.

Jonas: 00:06:40
But then look also at recent events where people came up with new uses on how to use the blockchain as a publication medium.
Now you go to 20 megabyte blocks and suddenly the minimum fee rate matters a lot because that's the point at which people enter the data that they want to publish into the blockchain.
And sure, we already have a pull request in Bitcoin Core that might skip over witness data until assume valid point if you're pruning and assume valid.
But anyone that runs a full archive node wants to have all that data.
Anybody that wants to calculate the witness `TxIDs` themselves, they need the data in order to calculate the witness `TxID`.
So at that point, yeah, it's an economic design parameter, but also just like a question on how quick we can do `IBD` and how much bandwidth it'll take and how much disk space it'll take, to the cost of node operation parameters, basically.

Tadge: 00:07:46
But the cost of node operation you can think of as, okay, numerator and denominator.
The numerator is, okay, how big is it?
How many signatures?
How much data?
And then the denominator is, okay, how good are computers?
And that can change.
It can get worse, but it probably gets better.
But that's where the variables go.

0xB10C: 00:08:01
It's changed a lot since this debate certainly began, but also ended.

Tadge: 00:08:08
I don't want to reignite it.

Jonas: 00:08:10
One terabyte SSD is now $80.

Tadge: 00:08:14
I've seen them for $50 on Amazon.
It's great.
Because it sort of died, right?
Like, from 2010 to like 2020 ish.
It was sort of dead, like Intel chips didn't get much better, AMD, like nothing really progressed.
And everyone was sort of thinking, okay, well, Moore's law is sort of over.

Jonas: 00:08:31
And then I mean, that's kind of nice.
GPUs are cheap again since Ethereum stopped using all of them.

Tadge: 00:08:36
Yeah, well, I'd hope to be cheaper.
But yeah, so it is kind of cool.
During 2020, 2021, I was like, oh, there's significant progress in this whole microchips and technology and like that's great.
I benefit from that and yeah.

0xB10C: 00:08:51
And so what do you do with that?
So the denominator has changed, yeah.

Tadge: 00:08:54
What does that mean?
So I think it doesn't touch the economics of Bitcoin if it's, hey, we want fees and stuff.
It has nothing to do with that.
But it does mean that if you have the same computer, it's easier to verify the current blocks.
Or you could verify blocks that were 50% larger or something with the same spend of equipment.

0xB10C: 00:09:12
Yeah, that's not my question.
My question is, the denominator has clearly changed in the last five years and the last 10 years.
What do you do with that?
What's the next step?

Tadge: 00:09:23
Yeah.
It gives you flexibility to change things without compromising the ability of people to verify.

0xB10C: 00:09:30
I understand, but this is a consensus system.

Tadge: 00:09:32
Oh, I don't know.
I'm not saying...

Jonas: 00:09:34
Oh, you're not advocating for a block size increase?

Tadge: 00:09:36
No, I'm not going to.
But I do think it's like people should talk about, like AJ talks, you know, like talks about, okay, mining rewards and like how this should incentivize, you know.

## Paper: On the instability of Bitcoin without the block reward

Tadge: 00:09:48
And then there's a paper, "Bitcoin is unstable without the block reward."
It's an interesting paper, interesting attacks.
It kind of doesn't get to the heart of it because they assume unlimited block size and like the beginning of the paper they're like, okay assuming there's no limit, here's all these problems.
It's like, well, we have a limit so this isn't going to happen.
But you know, it is still something I think is really interesting, because as people are now using it more, there's like lightning stuff, and people are like, all right.
I will say it at the place I'm working now.
People are saying, OK, we're going to have billions of customers.
And I slowly raised my hand, like, hundreds of millions?
I think we can get hundreds of millions and that'll be okay.
But I don't think we can quite get billions, which is really interesting because it's so close.
It's like, wait, there's 8 billion people.

Jonas: 00:10:32
But even hundreds of millions would be an interesting challenge.

0xB10C: 00:10:36
Let's go specifically.
Why not the B number?

## Serving billions with Lightning

Tadge: 00:10:39
Why are we in the millions?
If you just look at the current limits, you've got about 50 gigabytes of new output space a year.
And ish, 15 is something, on the order of, maybe.

Jonas: 00:10:52
Okay, until recently, the blockchain was roughly growing by some 54 gigabytes per year.

Tadge: 00:11:00
Yeah, but I'm talking about `UTXO` space, right?
So if you don't do any signatures and you just want the non-discounted space, right, is around 50, like a little less.

Jonas: 00:11:09
But yeah.

Tadge: 00:11:09
Yes, yeah.
So if you want lots.

Jonas: 00:11:11
But I mean, you can't create outputs without it.

Tadge: 00:11:14
Sure, sure, so 40, you know, like you can, but if everyone wants to have their own `UTXO`, that's the space you're talking about.
And so you could, in theory, expand that by something, let's, okay, 40, you know, something on the order of 50.

Jonas: 00:11:31
Let's say we can create, so a gigabyte is a billion, we could create roughly one billion outputs per year.

Tadge: 00:11:37
Yeah, that's roughly, right, on the order of, and in practice it's probably more like half that because you gotta have inputs, you know, all these other things, but you know, in that range.
And so it's like, could we have everyone in the world use this?
It's like, not quite, but you're pretty close.
You're not a factor of a million off.
You're not a factor of even 100 off, but it's maybe more like a factor of 20 or something.
I don't know.
It depends.

Jonas: 00:12:04
I mean, yes, if you assume that every output is one new user that you add to the system.
But that's just also glossing over the fact that the people that are in the system already will want to use the system, that people that already run businesses have a higher per capita demand of blocks.

Tadge: 00:12:25
Yeah, I mean I have a bunch of `UTXOs` and I don't want to give them up.

Jonas: 00:12:32
You hog you.

Tadge: 00:12:33
Yeah, so it is, but it is, you know, just this is very like sort of theoretical, you know, how could it work?
And so it is an interesting, like, you can have a lot, and you know, writing the Lightning Network paper, this was sort of what we, you know.
And if you look at the end of the Lightning Network paper, we're like, oh yeah, 130 megabyte blocks and we're good.
And that's what we sort of said.
Because at the time, it was like someone saying, no, we should go down to 300k.
Someone saying, no, we need to go to gigabytes.
And it was like, what's going on?
It's like, OK, well, we at least have a bound.
It seems that we definitely don't need more than this.

Jonas: 00:13:04
So how come the big blockers hated the Lightning Network?

Tadge: 00:13:09
So that's actually really funny because they did, and then I worked on `Utreexo`, like I'm still working on it, like `Utreexo` for a couple of years, and I'm like, well, this seems like perfect for big blockers.
You know, like this is great.
Now you throw away the `UTXO` set, you can have these efficient proofs.
But no interest.
I don't know.
But it does seem like, yeah, I should fit in with the big block crowd, because all the things I'm working on help this.

## The state of the debate when writing the Lightning Network White Paper

0xB10C: 00:13:34
Bring us back to the genesis of the lightning paper and how you had been thinking about the problem.
And there was somewhat parallel discoveries.
I think Christian Decker was a few months behind you, but generally how were you thinking about it and take us back to that time?

Tadge: 00:13:49
So this was, I worked with Joseph, Joseph Poon in San Francisco, we met up at like SF Bitcoin Devs and that's where everyone met everyone.
And we talked, it was a lot of the `HTLC` part, channels was his idea and we sort of talked about it and came up with all this stuff.
I think right around that time was when, I think Gavin first was saying, okay, I'm going to increase the block size.
It's not that people hadn't talked about that before.
They certainly did.
I talked about it at my first post on Bitcoin Talk in I think 2012.
I was like, wait, because the Bitcoin wiki I think was written by Mike Hearn and it said like, oh, we're just going to increase the block size and all this stuff.
And I was looking at it like, okay, cool.
And then looking at the code, I'm like, where?
And then I said on Bitcoin Talk, I think the first post I ever posted, I was like, hey guys, we should really fix this soon.
Because like, you know, like IPv4 and IPv6, these things get big and they get real hard to change.
So if we're going to do it like it says on the wiki, we should, I would say just, you know, next version, just do it.
And then like, Greg Maxwell is the first to respond.
He's like, no, no, no, the wiki is written by this guy, totally different.
I'm like, oh, I'm now learning about decentralization.
You can ask about Bitcoin, you go to Bitcoin.it and totally different.
But Greg said like, no, I don't think this is going to happen.
And so, but it was still very much open.
Like nobody really knows.
And then I remember going to lunch with Gavin Andresen and he said, I'm going to increase the block size to 20 megabytes.
And we're sort of like looking at each other like, no, I don't think he is.
Like, wait, you know.
Can you give us a better idea of the date?
Classic, before Bitcoin Classic.
Oh, this is 2014 I believe.
So this is a while ago.
And I think Gavin was in a position that's pretty different than now.
It was a bit more centralized in that he was the lead maintainer, and he sort of said stuff.
He said on video, oh, I'll throw around my weight and make it happen.
Yeah, that's not something that Vladimir has ever said or fanquake has ever said, right?
Like that's not how the current people who maintain Bitcoin Core think about it.
But I think Gavin, you know, he said hey, I was Satoshi, made it, I've been maintaining it, like he wanted to, you know, could do what he wanted.
And I don't think he realized the mess that it was going to become.
Because I remember him saying this as sort of, this is what we're going to do.
And he's like, I think this is the best way to do it.
And he probably did, but we were, you know, I just remember talking to Joseph after and he's like, oh man, like, this is going to be, like, no, he's not in control of Bitcoin, right?
Like, and even to this day, I mean, just a few weeks ago, there was like a Wall Street Journal article about Gloria and fanquake and all the people we're friends with.
But the headline said they're like mysterious or whatever.

Jonas: 00:16:36
And in control of them.

Tadge: 00:16:38
Yeah, I'm like, come on, they're not mysterious.
They've hung out at my house a bunch of times.
You know, like everyone's friends.
They're not that weird.
Maybe they just didn't want to talk to the reporter because, you know.
But I think it was different then.
It was a bit more hierarchical.
And so that sort of set off this whole mess that ended, I guess, with BCH forking off and SegWit and stuff.
But during that time, it was still a big question.
And so we were sort of open-minded.
It's like, okay, well, we do want to be able to run it on small machines.
Like, okay, if we want it, Lightning seems like a decent multiplier.
And I think my talk at Scaling Bitcoin in Hong Kong was, well, what if we don't have SegWit?
Can you still do Lightning?

## Would Lightning be possible without SegWit?

Tadge: 00:17:18
It's like, well, you need set time duration channels.
What if we don't have `OP_CSV`, things like that.

Jonas: 00:17:25
But also the transaction malleability was an issue, right?

Tadge: 00:17:28
Yeah, yeah, so if you didn't fix malleability, you could still do some lightning things.

Jonas: 00:17:33
You'd have to have like a, you'd basically have to have multiple possible return transactions that the counterparty signs.
So if your transaction gets malleated...

Tadge: 00:17:45
You could put like a `OP_CSV` + `CLTV` script, right?
So it's two of two `multisig`, or after a week, it all goes back to the person who funded it.
So now your channel can only last a week.
And that was similar to, I think, with, it's not the same.
The Christian Decker stuff had these decrementing time locks, which is not the same thing, but similar, had like, you could only change a certain amount of times and stuff like that.
That was sort of like during the process and coming up with Lightning.
But it was also, like Joseph didn't necessarily want to publish this.
I remember part of it was thinking that, okay, other people are going to come up with this or they're going to do it the wrong way, so hey, let's publish this or let's put it out.
So it was for SF Bitcoin Devs, we gave a talk, and that was I think the day or two before, it was like, okay, we need a name, like try to come up with a cool name.
And I thought Lightning Network, OK, because it's got little bifurcations.
I don't know.
So the name stuck, so that's cool.
But yeah, and there was interest, but it wasn't like, and it still is like, okay, who works on it?
How does that whole ecosystem?

0xB10C: 00:18:50
Lots of people work on it.

Tadge: 00:18:51
Yeah, yeah.

## Looking in from outside on a project you started

Tadge: 00:18:52
But it wasn't like, well, actually most people, a lot of times think I have nothing to do with it.
And sometimes I've had to like tell people like, no, no, I wrote the paper.
And like, they're like, no.
And I'm like, okay, look, here's my driver's license.
See, that's my name.
Because a lot of people think I don't have anything to do with it.
It's like, well, I didn't.
Because I didn't really work on it at all for a couple of years.
Now I'm sort of working on it a bit more.
But it is very decentralized, and I think that's a good thing.
And it's also sometimes frustrating because no one will listen to me.

0xB10C: 00:19:19
Give us a little bit more background as to when you've been participating.
Again, it's a little bit like the genesis of the system is with you and Joseph.
Neither of you are seen as, I would say, lightning leaders at the moment.
And so you take it from sort of this was the idea, it's off and running, companies are spun up, implementations are made, and you went off and did Lit for a little bit, and then put that aside for `Utreexo`.
But I'm sure you still have opinions.
How does that all fit together?

Tadge: 00:19:58
A lot of it is, we can be all rational and Spock, Vulkan, whatever.
But a lot of it is just like emotions, right?
Like people work on what they want to work on.
And like there's a ton of stuff that happens at Chaincode that I mean if you want to look objectively, you're like, does this really matter?
But it's cool, so like people work on it.
And similar with me too, like you can't, there's things that bug me about the BOLT specs and you just have to like, okay, whatever, I'm going to like not think about that.
But you know, there's things like, so I think millisats, that was Joseph's idea.
And I don't think anyone who really works on it now really likes it.
It's kind of annoying.
It's not actually that useful.
But part of, I remember at the Australia meetup I think 2018.
I was like, guys, guys.
We really need to get rid of millisats.
Let's just use Satoshis.
This is going to start being a big deal.
It's going to be hard to change.
So let's just change it now.
And you know, Rusty and everyone's like, nah, it's too late.
We already have code.
We're using millisats.
I'm like, oh, man.
And it's not the end of the world.
It's like a little thing.
But even where I work now, there have been so many bugs where they're like, wait, oh, it's 1,000 different, you know, factor of 1,000 different and all these weird, you know, annoying things.

Jonas: 00:21:07
And then you can't even pay them out properly.

Tadge: 00:21:10
Yeah, they don't really exist, right?
Like, so that, and then I think the bigger one that I also was like, don't do this, is trimmed `HTLCs`, which I worry about because it feels a lot like Bitcoin circa 2013, 14, where there's all these people saying, it can do all these amazing things, Bitcoin, free transactions for everyone, and then once there's fees, people get mad and think that you changed it on them.
With trimmed `HTLCs`, what if the dust...

Jonas: 00:21:38
Yeah.
Could you just repeat what trimmed `HTLCs` are?

Tadge: 00:21:40
So when you're sending Lightning payments through multiple hops on the network, you make what's called an `HTLC`, and it's a way to ensure that, you know, Alice will pay Bob if and only if Bob pays Carol.
And that `HTLC` is another output in the transaction.
And there's a limit on how small they can be.

## Trimmed HTLCs: Sending 1 sat vs 100,000 sats

Tadge: 00:22:02
Because the whole idea of Lightning is like, yes, it's layer two, it's all happening sort of off-chain.
But at any moment, all of this could fall back onto chain and it is all valid Bitcoin transactions.
And so the `HTLC`, if it's too small, it's not a real output, right?
You can't...
I don't actually remember the rules.
Is it standardness where if you try to make a dust output it will deny the transaction or is it just if you try to spend it?

Jonas: 00:22:26
We will not relay transactions with dust outputs.
Also, the other problem is if the amount is too small, the additional cost of creating the output is bigger in fees than the amount that it's worth.
So it would strictly make the recipient have less money.

Tadge: 00:22:41
Yeah, yeah.
So there's several reasons why you can't do this.
And so the solution in the current BOLT specs that you know LND, LDK, all these people use is, and I'm working on two now, is you sort of pretend it's there, right.
You send the hashes, you get the pre-images, but you don't actually touch the commitment transaction, you don't add this `HTLC` output because you can't.
And you know it works, but it also worries me because it's like, oh, people are like, oh, I'm sending one sat.
And you're like, yeah, but it works very differently whether you're sending 100,000 Satoshis or one.
And there's like a completely qualitative difference in what's happening under the hood that people are not aware of.
And I worry about that because I don't have an actual thought out fear.
Okay, what if the dust limit becomes much larger and then people are, you know, normal payments?

Jonas: 00:23:31
What if the people that do inscriptions are getting really really popular and fee rates go to 20 cents per byte in general and suddenly the dust size is effectively 20 times larger.

Tadge: 00:23:44
Yeah, and you know, and then there could be problems.
I don't worry about it too much, but it is sort of like on a purity kind of thing.
It's like, wait, if you're gonna change it, you should at least show it in the UI or something.
Like, hey, this is below a certain threshold.
It's going to work differently.
Or there's a different flag, some way to know.

Jonas: 00:24:02
Although that's the source of all evil in UX.

Tadge: 00:24:06
Yeah.

Jonas: 00:24:06
Showing complexity that we can get.

0xB10C: 00:24:07
Yeah.

Tadge: 00:24:07
I know.

Jonas: 00:24:09
So you're saying the channel shouldn't facilitate any payments below a certain amount?

Tadge: 00:24:15
I don't, I think that's an okay solution.
That's the quote I wrote.
It just wouldn't let you.
It would just say, yeah, that's not supported.
And they're right now very small, right?
It's like cents.
So it's just like, oh, I have to send at least 10 cents.
I can't send five.
Probably okay.
I don't know.

Jonas: 00:24:31
It depends on where you try to use it.

0xB10C: 00:24:33
Yeah, and I also think the lightning for micropayments use case, it starts rubbing up against, why are we doing this at all?
So if you're talking about a narrow range of, we support this, we don't support that.
And then for larger payments, you should go on chain.
It starts to get a little murky in terms of how you handle it.

Tadge: 00:24:52
I mean, yeah, but it's murky.
Maybe the reason I'm not a lightning leader or whatever, laser eyes, I don't sell it.
I'm like, here's what it can do.
And even when we were starting Lightning Labs, and we were talking to VCs, I would just talk about all the limitations.
Like, here's what we don't have working.
Here's what we don't know how to do.
But we know within these parameters it can work and stuff.
And it's sort of like, no, don't say that to the VCs.

0xB10C: 00:25:21
We've got to sell the dream.

Tadge: 00:25:22
But to me it's like, well, the reason we're asking them for money is to fix these things.
If we already had it all working, we don't need them.

## Limitations of the Lightning Network

0xB10C: 00:25:27
And so you've talked about some very concrete limitations that are, I don't know, certainly the latter one that we just talked about seems like a real limitation.
But there's also things that sort of seem fundamental in terms of griefing attacks, pinning attacks, and sort of like the assumptions that are made of the base chain.
And I'd be interested in your take as to, without reworking the base layer, do these assumptions hold?

Tadge: 00:25:58
So, okay, so there's those types of attacks.
There's also the general limitations of like, channels are a pain, right?
Like, you would much rather have a system where anyone can pay anyone without these sort of restrictions on routing and stuff like that.
But yeah, so the attacks, on the one hand, you can sort of hand wave and say there's reputation.
And what that really means is it's probably going to be fairly centralized.
And there's so many pressures in the system to centralize these things.
And my hope, I don't think you can eliminate them.
I don't think you can solve it.
But I think you can make it such that, well, yes, there may be some centralization, but hey, it's a layer two.
You can always drop out.
You can always say, OK, if I've got routing through this one large node and it doesn't want to cooperate, I can close the channel on chain and move somewhere else.
So it's sort of the competition can help that.
But yeah, attacks on nodes like that, it may make it so that certain nodes require identity or something.
I don't, no one's doing that yet, I think, hopefully.
But worst case that kind of thing happens or you get something like Tor where like it kind of works, but you know, there's this sort of constant din of like attacks on it that hurts it.

0xB10C: 00:27:10
I guess the main, let me be more explicit, the main issue that I'm thinking about is reliance on the `mempool` when the `mempool` isn't a place where you can rely on it.
If you are trying to come up with justice transactions when someone has wronged you and you're relying on getting something actually confirmed or in a block, that's a guarantee that doesn't exist.
And so how do you sort of reconcile the idea of this reliance on the robo-judge on the base layer when that justice doesn't actually, that's not real unless it's a best case scenario.

Tadge: 00:27:52
Yeah, I mean it's a best case scenario that so far has worked but we can't necessarily assume.

Jonas: 00:27:58
Yeah, do high fees break lightning, right?

Tadge: 00:28:00
So I would say that high doesn't, but highly variable many, right?
And so this is something after we wrote the Lightning Network paper.

## Do high fees break lightning?

Tadge: 00:28:08
I think Joseph was like super into this like, okay, how do we make, maybe there can be some other soft fork where there's like block signaling and certain, you know, once the blocks are a certain amount full these transactions can get priority and these others can't or something.
But it's not even that, it's just the foresight that you would need to know what to pay in the future for fees.
Well, that seems like an `RBF` for the justice transactions because those are immediately spendable.
You have the immediate unencumbered key for, and you in theory, you know, depending on your reserves in this channel, you may have quite a bit to spend on fees before it actually eats into the money that like should be yours.
Right, so if it's, you know, you're supposed to have five five and they close at six four and they shouldn't, and you know you're supposed to get five coins, but they made it so that you get four coins, and you're taking the whole six output.
You really only need one of those coins to be made like whole.
And so you can spend like a bunch on fees, and you do have the ability to `RBF` it.
So it's, you know, it's stacked in your favor in that sense, in that you can `RBF` and you can pay a lot of fees.
But so it's still a concern, and you know, what if you flood the entire `mempool`?
You know, as a single attack it's probably not as much, but if it's like a coordinated large-scale attack.

Jonas: 00:29:20
And then if channels are very small in general, you have less budget in order to close them.
And if they cheat while they had very little left.

Tadge: 00:29:29
Yeah, so the reserves and that's, and so you know having started at a company recently who's using Lightning and not familiar with Bitcoin or Lightning, a lot of what I do on a day-to-day is people are on Slack, and they're like, why does it do this?
I'm like, oh yeah, that's because of this.
How come I can't send all the money?
It's like, oh, there's like how many reserves?
There's so many reserves now.
Like in LND, there's the on-chain `UTXO` reserve for the anchor outputs.
There's the in-band, like in the channel, channel reserves.
You know, there's a couple different things.
And so, you know, one of the things we started with too is like in Bitcoin Core, it's like, okay, here's your balance.
In Lightning, it's like a lot more complicated.
How much money do I have?
It's like, well, depends.
And that's like not good UI, right?
Like, you want it to be very clear like I have this many bitcoins.
And you sort of can come up with different answers like, oh yeah, this much on your regular `UTXO` wallet, this much in channels if you closed immediately, uncooperatively you'd have this much, but then you'd get this much back later.
You know so it's kind of annoying.
But those are all to mitigate these attacks.
And then of course it's the frustrating thing where if you have really good attack mitigation, the attacks never happen.
And so everyone just says, well why do we need these reserves?
No one's ever doing this.
Why do we need all these different things?
Because reorgs never happen.
Why do we need all this code for reorgs, all these things?

Jonas: 00:30:54
Until they do.

Tadge: 00:30:56
But if you did, and so...

0xB10C: 00:30:58
Well, the deterrent is why they're not happening.
Exactly.

Tadge: 00:31:00
So why do you have all this proof of work mining if reorgs never happen?
It's like, well, Bitcoin is secure because of all this and no one bothers to attack because of that.

0xB10C: 00:31:09
I'd be interested in your take, given your explanation and the importance of the punishment.
I'd be interested in your take on Eltoo.

Tadge: 00:31:17
Okay, so.

Jonas: 00:31:18
LN-Symmetry.

Tadge: 00:31:20
So, to me the interesting part of something like LN-Symmetry, the different ideas in LN-Symmetry, is for more than two parties in a channel.
To me the downside, like I came up with the punishment mechanism.
I think it's cool.
I think it's an effective, you know, game theory-ish, what a thing.
But I think to me the biggest limitation in it is that it kind of restricts you to two parties.
Right?
You've got Alice and Bob.
If Bob does something bad, Alice gets all the money.
If Alice does something bad, Bob gets all the money.

## LN-Symmetry (Eltoo)

Tadge: 00:31:49
Once Carol shows up, it's like, OK, what do we do here?

Jonas: 00:31:54
I literally just wrote this answer on StackExchange three weeks ago.

Tadge: 00:31:57
OK, so yeah.
So LN-Symmetry, I think, constructions like that, if LN-Symmetry is still, you've got Alice and Bob in an LN-Symmetry channel, and the only advantage is, hey, now we can not have this punishment transaction and sort of update.
To me, that's like, that's not that interesting.
Like, that's not the powerful part of something like this.
To me, the powerful part is, now you can maybe get multiple parties in a channel.
And then maybe you can have more people using it, and they're all sharing a `UTXO`.
So if we're limiting the `UTXO` set, and block size, and all that, well, at least people can have, there's 10 people sharing a `UTXO` and sort of making payments.
That I think is a good way to go.

Jonas: 00:32:38
And you're basically short-circuiting payments between these people.
Let's say this is a group of friends that often need to settle for drinks and dinners and whatever, what they use Venmo for in the olden times.
And now they are all in a shared channel with five participants and they have virtual channels between each of each other.
And suddenly you get, yeah, what do you need?
Usually to have a completely interconnected set of five people with channels, that's five times four, times three, times two, times one.

Tadge: 00:33:15
Bunch of channels.
Yeah.
So having those kind of speed up.

## SIGHASH_ANYPREVOUT

Tadge: 00:33:19
So LN-Symmetry basically needs `SIGHASH_ANYPREVOUT`, which came from `SIGHASH_NOINPUT`, which I think I introduced like a million years ago on IRC.
And actually, that was my idea for instead of SegWit as a malleability fix.
Like, hey, if you're not signing the input `txid`, you don't care if it's modified.
You know, the signature still works.
And I gave a talk about that a couple months before the Lightning Network talk.
Because that was sort of my idea.
And I think we started programming like, hey, assume we have a `SIGHASH` that doesn't cover the input.
Let's start building Lightning that way.
And SegWit's better because there's a lot of foot guns with `ANYPREVOUT` or `NOINPUT`.
But I still think it's a useful thing to have.
I think it'd be really cool.
There are risks that people screw stuff up and blah, but like.

Jonas: 00:34:05
Just don't use it for the things that you're not supposed to.

Tadge: 00:34:08
Right, I don't worry about it.

Jonas: 00:34:10
Who would ever do that?
Use something for a different purpose.

## Why are soft forks so hard?

Tadge: 00:34:13
But I think I have a pretty different take on like, you know, even `OP_CTV`, check template verify.
I thought that was really cool.
I was like, yeah, I'll support that.
Like, I'll run that.
Like, I think this is a cool improvement.
And so, after Taproot merged in, I was like, ooh, maybe we can have like a bunch of changes to Bitcoin in the next couple of years because, you know, before SegWit like `OP_CLTV` and `OP_CSV`, it was just like no big deal.
You know, it was like people sort of write it like, okay, cool, merge it in like a couple of weeks later.
Yeah, it's running, you can use it.
And like, things like that weren't a big deal.
And then after SegWit, you know, no one wanted to touch anything.
But now we have, you know, with Taproot getting in, it's like, hey, maybe, maybe all the people who are arguing about SegWit being counter to Satoshi's vision or whatever they're saying, maybe they've all left and we have a bunch of people who are sort of okay with changing things or okay with making improvements.

Jonas: 00:35:08
There does seem to still be a large group of people that think that developers are an attack on Bitcoin and we should ossify yesterday.
I see a little difference with how `OP_VAULT` is received now versus how `CTV` was received last year.
Just sort of more focused on the exact use case and how do I make that work instead of look what I can build.
Although, Daryl, exactly, he made, James mentioned randomly, yeah, maybe we could use...

Tadge: 00:35:40
What fault is a covenant?

Jonas: 00:35:42
No, no, we could activate it with a, what is it, a speedy trial?
And that exploded immediately because speedy trial is terrible apparently.

Tadge: 00:35:52
It did work.

Jonas: 00:35:55
It did work, yes.

Tadge: 00:35:56 
With Taproot, yes.
I've been talking to people, even just this morning was talking to people who are not familiar with Bitcoin.
And I told them, I was like, look, I think long term it's probably going to ossify and we really can't make any changes.
But to me it's like, well, while we can, we want to make improvements.
But of course it's really risky.
What if you screw it up?

0xB10C: 00:36:17
What is your wish list?

## What's your wish list (hard fork wishlist wiki, soft fork wishlist wiki) for protocol changes?

0xB10C: 00:36:18
If you could wave.
There's a hard fork wish list and a soft fork wish list wiki page.
But what's yours?

Tadge: 00:36:25
I know, okay, Gleb has the like, not opcode, it's like pools, the coin pools.
I think that was Gleb.

Jonas: 00:36:33
Yep, I found it on Gleb, yeah.

Tadge: 00:36:35
And something like that, but I need to post to the mailing list.
I have a slight tweak to that that I think, it doesn't really make it much better, but it's like, oh, you could do it this way.
So something like that where, because I think if we're not going to have an increase in like, you know, block size, `UTXO` set size, whatever, what do they call them?
The little blocks inside the big, like extension blocks or something, I don't know.
If there's not something like that and you are sort of fixed at like, okay, we got a megabyte of output size and 4 megs, then if you really want lots of people to use it, okay, you need to start sharing `UTXOs` in a secure, usable way.
And so I think that `SIGHASH_ANYPREVOUT` can help with something like that, but also something like coin pools or something, you know, `TLUV`, `tapleaf update verify`, things like that where you're saying, okay, the outputs are sort of trees.
We started to have that with Taproot, where now you have like this sort of tree, but something like that is definitely something, you know, I'm looking at and interested in.
It's like, okay, we might only have a couple more years where we can feasibly get something in and so try to get something that will let people sort of share.
Yeah, I think I can improve outputs as well.
But I'm thinking a channel that can serve anyone would be.
And the other, the main other, like not even fork wish list, I just want it to be more usable because so many people, you know, quote unquote have Bitcoin and it's just on an exchange.

## Bitcoin needs to become more usable

Tadge: 00:38:00
And, you know, or if they're using Electrum, great.
Electrum's a huge improvement over being on an exchange.
And so many people, like so FTX fell apart a couple months ago, and a bunch of people I knew were like, hey, I should get my coins off an exchange.
I'm like, yes, you should.
Like I've said that a bunch, you should just run Bitcoin Core.
And then I worked, you know, like my parents, you know, people I know who are not, who are, you know, no computers, they're smart.
They download Bitcoin Core from bitcoin.org because I'm like, yes, that's all the people I know.
I'm friends with them.
I know where this is.
And then they download it.
You get, I think, eight executables.
You've got to run Bitcoin Qt.
There's a readme, but it just says how to compile it.
And it doesn't really say how to run it at all.
And so when I'm helping people run it, they're just like, how am I supposed to know this?
And I can run Bitcoin Core, everyone here can.
But I do think there is a bit of a lack of feedback loop where it's sort of built for the developers.

Jonas: 00:39:03
Bitcoin Core as a wallet, I think is generally a scratching your own itches.
Maybe showcasing some of the new things you can do, showcasing some of the privacy ideas we have, but I think there are a lot of wallets that have much better UX.
And especially, I'm pretty excited about a lot of wallets coming in doing output descriptor-based `multisig` solutions out of the box.
With `PSBTs` and output descriptors, it's gotten much easier.

Tadge: 00:39:34
So that part, but then, you know, if people are running an `SPV` wallet or it connects to an Electrum server, it's like, I don't want to recommend it because I know the limitations there.
Most people don't mind at all, right?
Because it's like, oh, you're losing some privacy or you're not verifying everything.

Jonas: 00:39:50
It's hard to quantify privacy.

Tadge: 00:39:51
Yeah, and so far everything works fine, right?
There's no, we don't know any attacks on `SPV` where you, we've never seen like someone mine a bunch of invalid blocks with valid proof of work so they can fool an `SPV` node or something.
Like, but you could.

Jonas: 00:40:07
Also, compact client-side block filters are much better in that regard.

Tadge: 00:40:11
Yeah, yeah.
But so, I want, I want my friends, I want the people I know who have Bitcoin to run Bitcoin Core, because that's the whole package, right?
It's verifying everything, it's got the whole, you know, either pruned or has the whole history, you know, does everything, it's like the real thing.
But it's hard because it's not as usable.
And it feels like low-hanging fruit to me in that like, yeah, we could make this easier to run without too much work.

Jonas: 00:40:39
Where's your pull request?

Tadge: 00:40:41
So I have, I've did issues to like, and might because you know, I've talked to Andrew Chow a bunch about different things, but yeah, so I want to work on it.
But also the other direction of it is, you know, working at a company that's not near, like, you know, they're not Bitcoiners and sort of saying, hey, you really need to have everyone have their own keys.
Like, that's sort of the part.
And also verification on client side, like all these things need to happen just to sort of nudge the rest of the ecosystem towards that hopefully.

Jonas: 00:41:08
I'm very excited.
I've talked to a big company that's working on a wallet solution and they're really trying hard to build it right with like, you own your own keys, it's still good UX, you can, there's a recovery mechanism.
So I do hope they come out with that soon.
I hope that they do stick to Taproot only because it would be so much better as a product.

Tadge: 00:41:35
Yeah, yeah.
So I think part of it is gonna be people learning about this stuff as well.
So I don't think it's just, oh, we need to make it like a super easy slick UI.
Like, yes, to some extent, but there are some complexities I don't think you can abstract away.
So talking about what is a `UTXO` versus an account, almost every block explorer shows addresses as inputs.
And everyone I've talked to at these new companies starting to work on Bitcoin, they're saying, I'm spending from this address.
And I'm like, I think that's it.
And this is on Slack.
How come this isn't working?
I'm spending from this address, but it doesn't do this.
And I'm like, just that first line, you're not spending from an address, you're spending a `UTXO`.
And they're like, well no, like here, and they send the link to mempool.space and it shows the input address.
And I'm like, yeah, no, that's not how it works.
It's really confusing because every website, so many things show it working a certain way and that's not how it works.

Jonas: 00:42:32
That is one of the things that I really hold blockstream.info in high regard for.
They actually show that you're spending a `UTXO` and only at the bottom, previous address, only in the detailed version.
I talk to the mempool.space people often, I should really bring that up.

Tadge: 00:42:49
I mean I can understand the convenience where you say, oh it's from this address, but it's like, well...

Jonas: 00:42:54
There's no from addresses in Bitcoin.

Tadge: 00:42:57
And I think part of Bitcoin taking over the world as it's doing that is people are going to learn how these things, you know, it's not much harder.

Jonas: 00:43:06
At least it's in the first place.
It's called, it should be called an invoice.
It's only used once, right?
So, yeah, so the whole term is just so misleading.

Tadge: 00:43:16
Yeah, so I think, but I think that's part of, you know, part of it is writing code, getting these things working, and then part of it is also educating and getting people to understand it and use it.
And it is a sort of weird, you know, use it quote-unquote the right way, because there's a definite like, developers of Bitcoin Core and Bitcoin things are sort of like, hey guys, everyone do it this way.
And then you see users in general, like, not necessarily agreeing 100%, right?
Like, if you try to make all this privacy and only use an address once.
And then some of the first things they do is like Vanitygen.
They're like, no, I want my name on it.
And general Bitcoin Core developers certainly were not pushing for ordinals.
But they're very popular.
There's 300,000 of them already, something like that.
And so to some extent, you've got to sort of say, look, people are going to do what they want.
We want to build the tools.
We want to build the software.
And hopefully, everyone uses it and has fun.

## Tadge's thoughts on Education

0xB10C: 00:44:17
You mentioned education.
And your open course, your MIT open course that you taught.

Tadge: 00:44:23
Yeah, open courseware.

0xB10C: 00:44:25
Was it 2018 is when that came out?

Tadge: 00:44:27
Yeah.

0xB10C: 00:44:28
So that's five years ago now?

Tadge: 00:44:29
Wow.
Yeah, it started almost five years ago.
Well, the videos...

0xB10C: 00:44:34
People still talk about it though.

Tadge: 00:44:35
The videos didn't come out till, I think, end of 2019.
So, yeah, early 2020 or something was when the videos were posted.

0xB10C: 00:44:42
Okay, so be that as it may, it's still.

Tadge: 00:44:45
It's old, yeah.

0xB10C: 00:44:46
People talk about it and it is now out of date.
But like, how do you think about education?
I mean, you were at an educational institution, you were speaking with students often, you've moved away from that, but like, what is the, what do we need still?

Tadge: 00:45:01
I still kind of want to do that kind of thing.
It was a class for students at MIT that, but if you look at it now, it's like, well, way more people, it was a class at MIT, but if you look at it, way more people not at MIT viewed this than the students at MIT.
And so it's like, yeah, maybe it should be.
Like, redo it as a primarily online course or something.
That would be a fun thing to update.
Because it's good to get new, it's really encouraging to see new people.
Because a lot of times, there's this sort of idea, like, oh, Bitcoin's boring, or I want to work on whatever, some other crazy coin.
But there's a lot of cool new things happening in Bitcoin.
Like you can definitely get involved.

Jonas: 00:45:38
I must admit that was one of the things that I thought was charming about the whole Ordinal hype, inscription hype.
Suddenly a lot of people that had outright dismissed Bitcoin as being old tech, uninteresting and so forth, started banding together on Discord to run full nodes and look at it.
And so far I haven't seen a ton of new ideas or output out of that, but these people will have a different view on how everything works.
We'll maybe have input on UX issues or we occasionally need an influx of new opinions.

Tadge: 00:46:11
That and also just the forces of Web3 or altcoin world.
So I was at MIT and there's the MIT Bitcoin Club.
And it's still called that, but every year it's a fight.
There's so many new students who come and are like, why don't we call it the Blockchain Club?
And it's like, no, no, no, Bitcoin.
But yeah, and certainly, and a good example is like some of the students I worked with at MIT came into the space through altcoins.
I don't even remember the name of the coin, but they had a hackathon at some university in Boston and, you know, there's free pizza.
And so people go and work and it's like, yeah, there's free pizza and like learn these stuff.
And then when I was interviewing him, he's like, you know, I worked on, I don't remember the coin.
It's like, okay, well, we're working on lightning or Bitcoin.
And then after a few weeks of working together, he's like, oh, this one makes a lot more sense.

0xB10C: 00:47:00
You often see the marketing the other way of, you know, come work on the better Bitcoin and, you know, people are picked off.
But there's not a ton of it.

Tadge: 00:47:11
I don't know many people who have really worked on Bitcoin and then said, OK, I'm going to go work on altcoins.

## Dynamics of working on Bitcoin

Tadge: 00:47:17
That's not like, there's not a ton of that, right?
Like, there's definitely people who drop out of Bitcoin and say, like, OK.
And I totally understand that.
Like, it's sometimes very stressful and annoying.
You know, it's like, OK, well, I worked on Bitcoin.
And now I'm going to go do something else and work on a normal company or, you know, the regular world.
That's not as crazy.
But there's not a ton of like, okay, how many Chaincode alumni are now working on, you know, just Carl?
But yeah, like, it is sort of interesting that like there is a, but like these other coins and whatever, they have a budget, right?
There's no, well, there was a Bitcoin Foundation, I think, some don't really exist, and they're not like there's not a university outreach from Bitcoin Core or anything.
I mean, Chaincode is probably the best example where they have the residency and, you know, newer developers who aren't as familiar can come and learn it.

Jonas: 00:48:17
Summer of Bitcoin I think is sort of the only example that comes to mind that does something like that.

Tadge: 00:48:23
But yeah, it's not as...
Summer of Bitcoin is more around the world, kind of.
But Chaincode had, I don't know if they...
I assume it died in COVID, where you don't have like people all show up in the summer, but you're...

Jonas: 00:48:35
For residents.

Tadge: 00:48:36
Yeah.

0xB10C: 00:48:36
Yeah, we do an online seminar.
Yeah.

Tadge: 00:48:39
So those kind of things, I think are great to get people in.
And also just being in person, like at MIT, having students involved, it's great.
And I don't know the best way to do it.
Like, I think we're in a much better situation than we were a bunch of years ago.
But even little things like IRC, like try getting a current university student to use it.

Jonas: 00:49:00
Use internet relay chat?

Tadge: 00:49:01
Yeah.
They're like, what's IRC?
And I'm like, it's sort of like Slack, but it's from the 80s.

Jonas: 00:49:10
Totally selling that, Tadge.

Tadge: 00:49:13
So yeah, it's cool to see all the new people working on this stuff, because we have to.
People come, people leave.
You want to get a lot of new people.

0xB10C: 00:49:24
Yeah, I was going to ask a question about people coming and leaving.
So we mentioned a lot of names here.
There's Joseph Poon, we talked about client-side block filters.
That was Jim Poe.
Gmax came up, Gavin of course.
You've hung in there, but you moved around a little bit.
I think when you go back to the beginning and think about how much context we've lost by people moving on, and some of the names, I just want to be clear, not all of the names that I mentioned are equal.
But I do think that by people churning out, we do lose context no matter who they are.
And do you have a take on why?
Do you have a take on how we can better hold on to that context or how we can learn from some of those things?

Tadge: 00:50:10
Yeah.
I mean, I can totally understand people sort of burning out and being like, I don't want to work.
Like in some examples, it's like you're getting sued by some crazy guy in London and, right.
Or, I don't really know what Greg Maxwell, like he's been sort of off, I mean, he's sort of still around, he's like on Reddit and stuff, you know, but he's sort of, okay, I'm not working on this technically.
But yeah, a lot of it, I think, a lot of it is stories, a lot of it is like knowing people.
And if it's going to be like this thing that takes over the world and you know, everyone's using his money, we probably want to get away from that because it is sort of this like somewhat insular, like, you know, we know people and talk.
We do, you know, have to sort of, but it's hard because like that's the default, right?
It's so much easier to like hang out with the people you know and talk to the people you know.
And if Peter Wuille is putting a PR, you look at it and you read his post because like, oh, like I'm going to click on his post and read it because he's got so many good ideas.
But I think we do have a pretty good system where like if something's anonymous, we're still okay, we still read it.
You know, like a good example from a few years ago was like MimbleWimble, it's anonymous, still we look at it, you know, use it.
People still post anonymously to mailing lists and stuff.
ZmnSCPxj, kind of anonymous, even though people have met him.
You know, like there are anonymous developers and stuff.
And that's, hopefully we don't need to go further in that direction.
But we might, you know, what if legal restrictions on development and stuff happen?
But then the question of like how to get people to not leave, it's hard because it's not like, you know, just look on Twitter.
There's so many reasons where you're just like.
And and I know I've argued with people too about like, okay, do we want, you know, mercenaries or only people who have like this sort of, I really want to work on Bitcoin.
I have this like, you know, desire and motivation to work on Bitcoin specifically, versus people are like, oh, it's just a job.
I'm in it for, you know, I'm getting paid, I'm getting a good salary.
I want to work on this.
I think you do sort of need a mix right now.
It's mostly people who are still sort of people who are into it.
It's not seen as something you get into just out of sort of like, oh, this is a good career to get into.
But that is still changing, I think.

0xB10C: 00:52:22
Well, it's a principle-driven project.
So it's by having people that don't identify with those principles.

Tadge: 00:52:30
Well, so that's where I'm working now to some extent, right?
And I think that's what I'm interested in and curious.
Like, OK, here's a company that, you know, most of the people don't have Bitcoin experience, but they're like, yeah, let's use this.
This is a good technology to use.
It's OK.
And they're all sort of getting on board.
And that's cool.
They're not tied to Bitcoin, but they're using it anyway.

Jonas: 00:52:49
Yeah, I think that the principle-driven, or also the ideological-driven people that work on Bitcoin space, I think they tend to go towards protocol development.
In the Bitcoin companies, there is quite a few people that aren't there for that.
There's a software job.
This is kind of interesting.
I learned something new.
But they are not there because they've been following Bitcoin for 10 years.
I had a similar experience at BitGo.
Where people, sure there was, especially on my team, on the Bitcoin team, we had a bunch of people that were really into Bitcoin.
But over time as we grew from 20 to 120, more and more people were just software developers for front end or for back end or for DevOps.
And it was a day job.

Tadge: 00:53:37
And I think, you know, if so that's this fun thing where like there's these Bitcoin or you know laser-eye people like Bitcoin is going to take over the world.
If it takes over the world, most people will not be laser-eyed, you know, they'll just be regular people who are like, oh, I use it because it's useful, it's convenient, whatever, I use this.
They're not going to be like, oh, this is the most amazing thing ever.
And so you're necessarily going to sort of lose that, like, hardcore, like, oh, Bitcoin kind of focus if it's going to billions of people.
And I think that's okay.
And I mean, like the idea of a lot of people using it, just, yeah, I use Bitcoin.
Cool.
Like that's a useful thing.

Jonas: 00:54:12
In the end, presumably it will be forgotten.
It's just the rails on which the new monetary system, transactions payments, global payment systems maybe, could work on.
And just like nobody knows how a credit card works, people won't know that Bitcoin is powering this underneath.

0xB10C: 00:54:29
Yeah.
We've come full circle.
We started with the idea of the big blocks and we went through lightning and then we got to where have all the people gone and now we're, doesn't matter.

Tadge: 00:54:42
No, I mean you still, you need people to work on this.
But the thing is, it's better than it's ever been.
We have Chaincode, we have Brink, we have DCI.
We have a bunch of places for development and you know it's still not that big, but it's also a good way you can say that Bitcoin's very efficient.
If you look at all the money from all the ICOs, the billions and billions of dollars, and then you look at like how much does Bitcoin Core, like protocol development, you know, like how much does Chaincode pay people a year, and how much does Brink pay people, you know, like add it all up.
It's not that much for the total, you know, development of Bitcoin over the entire life of it, it's much less than a single EOS or Tron or something, right?
Like way smaller.
And so it's like, hey, this is a very cost efficient system we've been working on.

Jonas: 00:55:31
It is so baffling when you look at Bitcoin week by week, nothing ever happens.
And then you look at what happened in the last two years and you're like, oh, that's pretty cool.
And oh, yeah, we did make quite a few steps forward here and there.

Tadge: 00:55:45
But yeah, it's easy to lose perspective if you're that close to it.
Oh, yeah, I mean, you definitely, it's great to talk to people who aren't familiar with it and see, you know, what they're seeing about it, and I try to do that a lot.
So yeah.

0xB10C: 00:56:00
Thanks for joining us, Tadge.

Tadge: 00:56:01
Great, thanks.

0xB10C: 00:56:02
Great conversation.
All right, Merch, another one in the books.
Any reflections?

Jonas: 00:56:17
I liked how many directions this conversation went.
Lots of things to touch on, lots of little anecdotes and context.

0xB10C: 00:56:26
Taj has done a lot of things.
So he's a, he's a Renaissance man in the Bitcoin community.

Jonas: 00:56:32
It's kind of funny that people don't think he has anything to say about Lightning.

0xB10C: 00:56:36
It happens and he, you know, I guess it'd be like Satoshi.
What if Satoshi was like, hey, I did this all.
Like no one would believe him.

Jonas: 00:56:47
No, in a way it's a sign of the success of the project, right?
There's so many new people working on this that the names of the original idea giver is no longer that important.

0xB10C: 00:56:58
Cool.
Well, I hope you enjoyed listening and we'll see you.
