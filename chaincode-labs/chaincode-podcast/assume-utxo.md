---
title: "Assume UTXO"
transcript_by: Numba1ne via review.btctranscripts.com
media: https://www.youtube.com/watch?v=knBHvzKsIOY
tags: ["Utxo","Validation","Security","IBD","Forks","Bitcoin Core"]
speakers: ["James O'Beirne","Adam Jonas","John Newbery"]
categories: ["podcast"]
date: 2020-02-12
---

## Intro

James O'Beirne: 00:00:00

Bitcoin is a very complex piece of software and it's very difficult to review for correctness. Even people who are really experienced with the code base still have a really hard time determining, in some cases, whether a change is safe or not.

John: 00:00:25

Hi Jonas. Hey John. Hi Carly.

Carly: 00:00:27

Hi guys.

John: 00:00:29

We have Carly in the studio. Carly is our producer and she's been helping us with the episodes.

Carly: 00:00:34

Yeah, it's been a lot of fun. It's been really great working with you guys and getting to meet all of the wonderful guests that you guys have had on.

John: 00:00:41

Great to have you here.

Carly: 00:00:42

Thank you.

Carly: 00:00:42

And who do you guys have up next?

John: 00:00:46

Well, this week we talked to James O'Beirne who until very recently was a co-worker here at Chaincode Labs. I first met James a couple of years ago back in 2017, 2018 at a conference in Stanford and then a meetup in San Francisco. And it was obvious from when I met him that he was very passionate about Bitcoin and enthusiastic. And he was so enthusiastic he applied I think the very first day that we opened applications for the residency in 2018. So, he came to the residency in 2018 and then went on to join Chaincode and he's been a friend and a co-worker for the last two years.

Carly: 00:01:21

I love that. What did you guys talk about?

Jonas: 00:01:24

We talked a little bit about how he decides the projects that he works on and his most recent project which is Assume UTXO. And then we talked a little bit about how he sort of advocates and affects changes in Bitcoin Core.

John: 00:01:36

We really love talking to James and we hope you enjoy the episode. We'll be back at the end.

John: 00:01:44

Hi James.

Jonas: 00:01:45

Hey James.

James O'Beirne: 00:01:46

Hi.

John: 00:01:47

Welcome to the podcast.

Jonas: 00:01:48

Welcome.

James O'Beirne: 00:01:50

Thanks, it's great to be here in our conference room.

Jonas: 00:01:55

Well thanks for making the trip. We're going to talk about a few different things today. We're going to talk about what you're currently working on. We're going to talk about the vision quest that brought you here today. And so maybe why don't you go back to not the beginning, but the start of the new beginning. Sure thing. To Chaincode.


## 2018 residency


James O'Beirne: 00:02:15

Sure thing. Yeah. Well, let's see. I came to Chaincode in the winter of 2018. I think it was February 1st. And I had been talking to John previously because we had collaborated to some extent on a few things in the repo and I had met him in California at a conference out there and had told him that I'd like to apply to the residency. And So he encouraged me to do so. I did that and somehow got in. And so I showed up in New York during the winter of 2018 and started the residency, which was a lot of fun. Through that, got acquainted with Chaincode and that led to a full-time position. That was also the crypto winter of 2018, I believe. Correct.

John: 00:03:13

Oh yeah, we were coming off that hot 2017 bull run.

James O'Beirne: 00:03:19

Yeah, yeah, Mixed emotions. But it was a really great time. The residents were all awesome. The sessions that we had were really interesting because they were very, it was a smallish group. It was maybe 15 total, I think. Maybe a bit more than that.

John: 00:03:41

It was two sessions of two weeks and six or seven in each, I think. Oh, is it that small in terms of people there? Okay. Pretty small. Yeah. Select, exclusive.

James O'Beirne: 00:03:54

Yeah, everybody there was great. And so we had some really great sessions. Very interactive, very Socratic. Yeah, it was a lot, It was intense. And I'm kind of first and foremost, I think of myself as like a carpenter, but instead of wood, it's like software. So at a certain point, I kind of tuned out and was just ready to start coding. But it was awesome. One of the things that I think about a lot when working on Bitcoin is that it's really easy to get hung up on how many smart people are here and you can get in your own head about like what can I actually contribute? It's a really easy rabbit hole to kind of spiral down because there are incredibly talented people working on Bitcoin. But what you've got to realize is that there are different kinds of smart. Everybody has different skill sets. I kind of like putting one foot in front of the other and having consistent engineering hygiene and trying lots of things and iterating quickly. And that makes me really good at some things, it makes me really not good at other things. And I think what's cool about development of Bitcoin is that there is actually space for a lot of different approaches.

Jonas: 00:05:21

As a carpenter starts to think about what he's going to build, how do you decide what to work on and what kind of angle you're going to take on a project like this?

James O'Beirne: 00:05:33

## Choosing what to work on

I think before you know anything, you just have to jump in and start doing things.  And I don't mean necessarily opening PRs and things of that nature. But I think cloning the source code and then playing around with it, making modifications to it, is really important just to get to know the code base, watching the way that reviews work. But fundamentally, it's all about, where the bottlenecks are, whether that's in terms of a feature set or the performance or resource usage or vulnerabilities. Everything is kind of like looking at what the lowest hanging fruit is and then kind of going from there. So I came in not necessarily knowing what I was going to work on. I came in having made a change to the level DB wrapper that we use and having worked on the test suite a little bit, but I think there were a whole lot of dimensions of Bitcoin that I, or Bitcoin Core that I just wasn't familiar with. I think the first thing I started to work on was like the fork detection framework.

## Fork detection framework

The idea there is that we want to have some kind of logging or alert system if Bitcoin sees a heavy work fork that's been going on and hasn't been resolved because that means that your node might have been partitioned somehow. And nominally we have ways of doing this but they're kind of broken so and they're still kind of broken And that has to do with balancing considerations around DOS and kind of the way that we do the bookkeeping around header validity. So anyway, I had started to work on that but that was kind of stalling and it didn't look like it was going anywhere. And frankly, It's a cool project and it was a good way of getting introduced to Bitcoin Core in a formal way, but I think the marginal utility of that is kind of low. So I started thinking about what really mattered to me in terms of where did I think the important work was in core.

## Initial block download (IBD)

That naturally led to the duration of the initial block download because I think That's kind of a sticking point for a lot of people who want to participate in consensus and want to run a node that they transact with because that's really the only way that you kind of reify the rules that you're using Bitcoin under. So it's an important thing to.

Jonas: 00:08:31

I'd like to challenge that a little bit.

James O'Beirne: 00:08:32

Sure.

Jonas: 00:08:35

Don't you think if someone has set up the hardware or just gotten their ducks in a row to actually participate, that they're just going to wait for whatever it takes to do the initial block download? The speed of which, I mean I hear the phone instance and I hear just usage or outdated hardware, or the case may be we want to enfranchise as many people as possible. But if you've set it up and you've started the process, can't you just wait a little bit longer? Like, is that really an area of optimization that we need?

James O'Beirne: 00:09:11

Yeah, you certainly can. And that's the right question to be asking. In my experience, there are a lot of people who are on the margin there. For example, I have a friend who is a very diligent user of Bitcoin and he's very privacy conscious But every time he's gone to download the chain and use Bitcoin QT, he gets kind of hamstrung and he's stuck waiting days and he's turning his laptop on and off. And so subsequently, that kind of user is pushed towards using something like say Electrum, which has a different security model than Bitcoin QT. So yeah, I think there are a lot of hobbyist users out there who are going to buy, say, a Raspberry Pi and set it up and wait the four or five days or whatever that it takes to sync. But I think appealing to those users who are maybe casual users of Bitcoin or maybe more than that, but they're kind of deciding between getting the whole blockchain or using Bitcoin under a different security model. And that's kind of on the margin. So I think those are important people to go after. And the other thing to keep in mind is that the blockchain is just going to keep growing. So there's linear growth there. And I think there has to come a point where we say, okay, we have to stem this somehow, because this thing is going to, if we want this to keep going on forever, IBD time can't scale with forever. So we needed to truncate somehow.

John: 00:11:01

Okay, so let's talk about IBD, initial block download. What is a node doing when you switch it on for the first time?

James O'Beirne: 00:11:10

Well, I think the first thing it does is check to see if it's got any data. And If it doesn't, then it tries to find peers. If it doesn't know any peers right off the bat,

## DNS seeds

it'll consult these DNS seeds that are run by various people, and it'll get a random set of peers. It'll connect to those peers and it'll basically ask them, I think, what the best block that they know about is. Is that right? And so in doing that, your node then gets the headers chain, which is basically like an abbreviated version of the blockchain. That's kind of the vital information, the vital metadata about blocks without the transaction data itself. And once it has all that, it figures out what the most work valid headers chain is, and then starts the initial block download process, which is where it's actually obtaining the data in the blocks, the full blocks themselves. Reassembling the blockchain, which basically amounts to building a few indexes,

## UTXO set

the most important of which is the UTXO set, which is kind of its own data structure. And so at the end of all that, you end up with this set of unspent coins, which you can then use to decide whether an incoming block is valid or invalid. And that whole process takes, at the moment, anywhere from four hours, if you've got a really good internet connection and really good hardware, to kind of an unbounded amount of time, depending on your hardware and bandwidth.

John: 00:13:01

Okay, so you start by getting this headers chain, which is the block headers, and that contains the proof of work, so you can, just from that small amount of data, 80 bytes per block, you can figure out which chain has the most work. At this point you're not validating transactions, so you don't know whether it's a valid chain, but you know that it's got the most work. And then you go back and download the blocks. And as you're downloading blocks, you're validating them and building this UTXO set, which is a set of coins, a set of unspent transactions. So that takes a long time. It takes a long time to download that data. There's IO there because you're writing to disk, and there's computation there because you're validating the signatures, and the blockchain is getting bigger all the time. So if you do this in a year's time, it will take longer. So what are some of the strategies that we've had so far before us? We're going to talk about assume UTXO, but before we get there, what are some of the strategies that we've had to make this take less time?

James O'Beirne: 00:14:11

Yep. So the first I'm aware of, and correct me if there's something we did before this, but That signature verification that we have to do for each block,

## Parallelized signature validation

you can to some extent parallelize that. And so one of the things that we do is we have kind of a thread pool of signature verification processes, so that gets parallelized.

## Assume valid

Another thing that we do is called Assume Valid. And I actually didn't know about this until I came to the Chain Code Residency. I was taken aback when I learned about it as I think most people are and should be because it's a very unintuitive idea and it should kind of raise the hair on your back if you're a dyed in the wool Bitcoiner And you're like, hey, wait a second, how does this thing actually work? So what assume valid does is there is a block hash hard-coded in source code. And if your Bitcoin client sees a headers chain that contains that block hash, it will assume that all of the signatures in all of the blocks underneath the block designated by that hash are valid. And so it'll skip signature verification. And traditionally signature verification is the most costly part of initial block downloads. So that saves you quite a bit of time. So the natural question is, how does this not somehow dilute the security model of Bitcoin. You know, you're trusting the developers, I think would be the catchphrase. The reality is that This works because Bitcoin source code is the trust model, right? That's what you're trusting when you run Bitcoin, is the source code that your binary is built from. And Basically, when you're evaluating a change to Bitcoin, that's obviously going to affect consensus in one way or another. That change could potentially be doing anything. It could be short-circuiting some kind of validation that might permit the spend of a certain coin that doesn't exist. It could be doing any number of things. And all Assume Valid does is it basically makes part of the review process a sort of commonly agreed upon attestation that the software has previously validated this particular chain. It doesn't really dictate what the right chain is because Let's say there's a massive reorg where somebody secretly forked, started working on a fork at some point before that assume valid mark, that alternate fictional chain could still potentially overtake the chain that's been deemed assume valid. It's just basically Bitcoin users coming together and saying, hey, look, yeah, this is the chain that we've all previously validated. We know it's valid. And it gets reviewed like any other piece of the code.

## Different than checkpoints

John: 00:17:31

And so this is different from checkpoints. A hard-coded checkpoint in the source code because if there's a competing chain with more work, you can reorg to that chain and you'll get into consensus with that longer, more work chain. Whereas with a checkpoint, it precludes that. A checkpoint would hard-code the exact chain that you would have to follow.

James O'Beirne: 00:17:57

Right, right. So that really is the developers of software dictating what the only allowable chain is. Whereas this just says, this is sort of a public attestation that, hey, we've all previously validated this chain, we know it's valid. And so This kind of change is interesting because when you think about it, it's from a threat model standpoint, it's kind of a nice thing to have because Bitcoin is a very complex piece of software and it's very difficult to review for correctness. Even people who are really experienced with the code base still have a really hard time determining, in some cases, whether a change is safe or not. And so when you kind of crystallize your security assumptions in a place where almost everybody can review it. So for example, the way that we update the assumed valid value, because we do that typically with every release,

## Updating assume valid value in the code

is somebody will post a modification of that value, and then a number of people will chime in on the pull request and say, yeah, so I've, you know, I use the node that I previously provisioned with the initial block download process, and I ran this RPC command, and it told me that this hash that you mentioned in the source code is actually in my chain. So I agree to this. And that's something that you don't have to be an expert in C++ to be able to do. You don't even necessarily need to be a software engineer to do that. So the use of this technique allows you to get way more widespread review over a pretty security critical change.

Jonas: 00:19:59

Do you find non-software engineers actually contributing though? That assumption seems to work if actually other people are doing it.

James O'Beirne: 00:20:03

Yeah, I think not enough people are at the moment. But you definitely do see people in the Bitcoin community who are not involved in this sort of day-to-day development of Bitcoin Core. They pay attention to those pull requests. And they'll chime in and they'll say, yeah, I ran this RPC command and this matches up. So it really brings more people into the fold than otherwise would be on something where many, many people should be paying attention. Because I could post a pull request tomorrow that claims to be some kind of optimization to the UTXO set, and it could contain some vulnerability. And the number of people who are currently able to find that vulnerability is very, very limited relative to the number of people who can run an RPC command and say, no, no, no, this doesn't match up with what I have.

John: 00:20:55

Yeah, and it should also be noted for the mountain men who, sorry, and mountain women, we don't know, preclude any people who live on mountains. But you can switch off this feature and validate every signature from Genesis to the tip.

James O'Beirne: 00:21:12

Yeah, exactly, very important.

John: 00:21:16
So does that mean we're going to transition to assume UTXO and how you arrived at that solution?

## Assume UTXO ()

James O'Beirne: 00:21:17

Yeah, we can do that. So I was very concerned with this IBD thing. And I thought, how cool would it be if we could cut that time down substantially? And even maybe cut it down enough so that you could at some point run it on these really underpowered devices and devices with not great internet connectivity. So I spent a little bit of time tinkering with doing small things like trying to make logging asynchronous and just these little optimizations. I thought even if I eke out 10% to 15% reduction of this time, it's not going to make a big dent. So what are some of the bigger ideas that might help me get this time down? And I think I first heard Alex Morcos mention this. But the idea of using some kind of a UTXO snapshot to bootstrap a node came up at some point. And I thought, oh, that's kind of an interesting idea. I don't think it'll necessarily work or sort of be acceptable from a security standpoint, but it sounds like it'll be fun to implement. I was looking for an excuse to get to know the code base better anyway. So I said, okay, well, I'll come up a little prototype and just see how it works. And so I did that. And throughout the course of doing that, I became increasingly convinced that this was basically just the spiritual continuation of AssumeValid. And so the idea of this is basically that, like AssumeValid, you could hard code the hash of the UTXO set at a certain point in time, at a certain block height. And if you hard code that expected value there, you can then have the user upload a serialized version of the UTXO set that hashes to that value. And you can then initialize all the data structures in Bitcoin that are necessary for operation based upon that snapshot. And then in the background, you can do the regular old initial block download. But meanwhile, you're able to transact kind of as a, you know, as sort of a fully validating node. You know, you can see incoming blocks and you can judge their validity and send transactions. And yeah, so I implemented this and found that, in terms of security model, it didn't really differ from AssumeValid and shopped it around to a few people. And to my surprise, the conclusion was, yeah, this looks pretty good. On top of that, in just the preliminary testing I did, the results were great in terms of trimming down the IBD time. I think the latest numbers are something like an hour and a half from start to finish to get up and running on my computer. So pretty good results so far.

John: 00:24:43

OK, So let's just dig in a bit into how it's different from AssumeValid and why you get that significant performance improvement or lower time to sync to the tip. With AssumeValid, you get the headers chain, you download all the blocks, and then you're building this UTXO set, but you're not validating signatures as you build up to the AssumeValid block. And that building of the UTXO set itself is quite expensive. Maybe you can talk a little bit about why that is and the coins cache and flushing to disk and that kind of thing. Whereas with AssumeUTXO, you don't need to build that UTXO, so you get a snapshot. And so you just fast forward through the first 500, 000, 600, 000 blocks, whatever it is, the height of the assumed UTXO block. So maybe just a bit about where you're saving time when you do this.

James O'Beirne: 00:25:44

The UTXO set is probably, other than maybe bandwidth, probably, and signature validation, probably the biggest bottleneck in doing initial block download. I guess maybe we never defined what the set itself is, but it's basically a mapping of outpoint, which is the transaction ID and index, and then valued by the unspent coin itself, which you can find at that outpoint location. And we reference this thing when we're validating incoming blocks because we want to obviously verify that the coins being spent in the block are valid spends. And then we want to actually update the set with the new unspent coins that are made available by that block. This gets tricky because the UTXO set is about three and a half gigs right now. And on some platforms that can fit into memory. And so access to that sets very fast. On other platforms, we're limited by memory, and so we have to basically write out part of that cached disk and kind of selectively page in and out the parts that we're using at the moment into working memory.

## Platform and memory considerations

So Depending on your platform, it can get really expensive to do operations on this set when it gets big. And that's indeed where a lot of the time is spent when you're doing initial block download on, say, a machine that has 2 gig of memory and maybe an old spinning disk. You spend a lot of time flushing the in-memory coins down to disk and then maybe reading coins that you haven't found in your in-memory part of the cache from disk. So with Assume-UTXO, when you're given this serialized snapshot, and you can just load it in from a certain point in the height, a certain point in the chain, You've foregone maybe doing a lot of disc writes and reads.

## Criticisms

John: 00:27:56

What criticisms have you received thus far?

James O'Beirne: 00:28:01

I think a lot of people read it and they are initially very skeptical, which I completely understand because I was skeptical and you should be skeptical. It sort of seems like a too good to be true kind of thing. The tricky part is that conceptually, it's much easier to sneak in, say, an illegitimate unspent coin than with assume valid. So For example, if you could convince someone to accept an AssumeUTXO hash that they had constructed specifically, it's very easy for an attacker to then serialize a modified version of the UTXO set that matches that hash, and then basically convince someone to accept an illegitimate spend. Oh, and I guess it's worth noting an important part of the proposal is that unlike in AssumeValid, you cannot specify the AssumeUTXO hashes through the command line. And this is a pretty intentional... I think that would just be a huge foot gun because then you could have someone, you could pre-format the Bitcoin D command and trick somebody that way. Okay, short of the malicious command line that you might give somebody, what you would have to do is modify the source code somehow to say, accept that malicious, assume UTXO value. The thing to keep in mind is that if you can modify somebody's binary, then you're cooked in the first place. Because if you can modify their binary, it's much easier to just add some little conditional into the coins cash code that accepts their spend or does any variety of things. And so in actuality, this doesn't open the potential for any attacks because we're still relying on the threat model of not being able to have your binary modified?

John: 00:29:58

I think there's a maybe more philosophical, subtle argument against, which is kind of a slippery slope argument that we want validation to be quick and IBD to be quick. And taking a shortcut like this is kind of kicking the can. And if people come to rely on this as the only way to validate the full chain, we might get ourselves into a position where it actually is impossible to fully validate the full chain. Ethereum might be there at this point already. And fastest way to do the IBD is to just not validate at all. Super-fast. There you go.

James O'Beirne: 00:30:42

Totally true. Yeah, no, and That's a good line of thinking. I think the thing is that when we introduced pruning, we kind of went through this. Obviously, if you run a prune node, that means that you only keep around a certain number of the most recent blocks. And so, well, obviously, if we don't want to use disk space, then everybody should run a pruning node. And at that point, nobody's serving blocks. I guess this is a little bit different in the sense that, yeah, if everybody's starting in XUMU TXO mode and not back validating the chain, which is a sort of mandatory part of the current proposal. Yeah, it's worth pointing out that if you are using Assume UTXO in its current incarnation, you're doing a background validation from scratch. And so I think that kind of alleviates that concern. But there are people who argue that if you're willing to buy into the Assume UTXO security model before you have done the back validation, then why even do the back validation? And, you know, there are a lot of people who have thought a lot about this and still sort of hold that opinion. But I think the nice thing is that if we all agree that that's the case, then it's a pretty simple matter to make the background validation optional or disabled at some point. But for now, we can be conservative and still do that.

## Championing a big change in Bitcoin Core

John: 00:31:12

So we were covering the arc of your JNCOD journey, and I guess I'd be wondering, what is it like to champion something that's such a big change and just so different? And what can you do yourself? And what do you need others to do to get something like this into Bitcoin Core?

James O'Beirne: 00:32:35

Initially, I didn't really think about this as a big change, but in hindsight, I guess it is. I think The best thing you can do is just to try and be very communicative, try and kind of at every opportunity provide motivation for why this is a good thing, why it makes sense. I have taken the approach of trying to break this change up into a number of small constituent PRs and just get those steadily merged so that the notion of progress doesn't become this binary thing about whether the giant PR is merged or not, you can kind of have some incremental progress. I think everybody feels a little bit better about that. But yeah, I think in Bitcoin development, one of the really hard parts of it is socializing your work and It's definitely difficult given the slow pace of development, which is of course merited. I think effective communication and just being very clear about your motivations and demonstrating why it's worthwhile change.

Jonas: 00:33:49

Just to be clear to the listeners, how did you go about socializing this? You did a work in progress or a draft implementation and you started carving off pieces, or You did a draft up front. How did you get it out?

James O'Beirne: 00:34:04

Yeah, so I did the draft implementation, and that was the first artifact I had. And I spent a little bit of time polishing that up and making the commits work semantically. And I posted that along with a pretty lengthy description. After that, maybe a few weeks after that, I let it hang out for a little bit. I then made a mailing list post and solicited feedback from the Bitcoin dev mailing list. I used that feedback to then build what, in hindsight, probably should have just been a BIP, but it was a frequently asked questions document that I posted on GitHub. And I asked a few people to review that. And some of that feedback I actually posted in the same repo as the frequently asked questions document. So after that, I started just proposing parts of that big draft PR. And while that was going on, I guess I did some more informal stumping. I went on a few podcasts and you blackmailed me into doing a few talks, which I should thank you for. All done, yeah. So, yeah, it's a multifaceted thing and kind of any way you can shill your change, it's probably good. Thanks James. Thanks James. Thank you guys.

John: 00:35:43

Okay, I really enjoyed that talk. What did you think Jonas?

Jonas: 00:35:46

Yeah, I really liked the conversation about IBD and the assumed valid conversation. Those were my two highlights.

John: 00:35:52

And we're certainly going to miss James here in the office.

Carly: 00:35:54

Yeah, it was great that you guys got to sit down with him before he took off for his next adventure.

John: 00:35:59

Good luck, James. We'll see you here.

Carly: 00:36:01

Good luck, James.

John: 00:36:08

Bye.

Good luck, James.

John: 00:36:08

Bye.
