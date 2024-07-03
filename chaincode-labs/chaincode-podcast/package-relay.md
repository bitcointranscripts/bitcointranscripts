---
title: "Package Relay"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
source_file: https://anchor.fm/s/12fe0620/podcast/play/52496387/https%3A%2F%2Fd3ctxlq1ktw2nl.cloudfront.net%2Fstaging%2F2022-4-24%2F7dc718ef-caa2-0ba5-69c2-f2d0a7f117e2.mp3
media: https://podcasters.spotify.com/pod/show/chaincode/episodes/Gloria-Zhao-and-Package-Relay---Episode-21-e1j0ii3
tags: ['package-relay', 'security']
speakers: ['Gloria Zhao']
categories: ['podcast']
summary: "Gloria Zhao sits down with us to discuss her package relay proposal and what it is like as a relative newcomer to propose a big change."
episode: 21
date: 2022-05-24
additional_resources:
-   title: 'Mailing List: Package Relay Proposal'
    url: https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-May/020493.html
-   title: 'Mailing List: Package Mempool Accept and Package RBF'
    url: https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-September/019464.html
-   title: 'Brink Podcast: Ep1 Mempool Policy'
    url: https://brink.dev/podcast/1-mempool-policy/
-   title: 'Censorship and DoS Attacks: An intro to Mempool Policy'
    url: https://vimeo.com/704956163
-   title: Transaction Relay Policy for L2 Developers
    url: https://www.youtube.com/watch?v=fbWSQvJjKFs
-   title: Mempool Garden
    url: https://github.com/glozow/bitcoin-notes/tree/master/mempool_garden
---
Speaker 0: 00:00:00

Hey Jonas.

Speaker 1: 00:00:00

Hey Merch.

Speaker 0: 00:00:01

We're going to try again to record with Gloria.
This time we want to get a really focused, short.

Speaker 1: 00:00:07

We got a lot of tape in that last one, but I don't know if all of it was usable.
Yeah, we're going to talk to Gloria today about her newly released proposal for Package Relay.
And yeah, looking forward to getting something that we can release.
Enjoy.

Speaker 0: 00:00:22

Let's go.

Speaker 2: 00:00:23

Let's go.
Enjoy.
Let's go.
Let's go.
Let's go.
Let's go.
Let's go.
Let's go.
Let's go.
Let's go.
Let's go.
Let's go.
Let's go.
Let's go.
Let's go.

Speaker 1: 00:00:35

Let's go.
Hey, Gloria.

Speaker 3: 00:00:36

Hello.

Speaker 1: 00:00:37

Welcome back to Chaincode.
This is our second time recording, but this one's going to be comprehensible, I think.
I think we're going to make it work.

Speaker 0: 00:00:44

Yeah, I promise not to break all the discussions.

Speaker 1: 00:00:48

It'll be fine.
We don't have to, let's not get too on our head.

Speaker 3: 00:00:51

It's a deep topic.

Speaker 1: 00:00:52

It's a deep topic.
What I like about this conversation is you have something very specific to talk about.
Right.
So you wrote to the mailing list.

Speaker 3: 00:01:00

Yes.

Speaker 1: 00:01:01

And you proposed package relay.

## What's package relay?

Speaker 1: 00:01:04

What's package relay?

Speaker 3: 00:01:05

Okay, so I proposed some implementation of package relay, essentially, which is a concept that's been talked about for at least seven, maybe nine years.
And it's the concept of requesting, announcing, and downloading groups of transactions together, namely related transactions.
So a package is a widely used term for some set of transactions that have a dependency relationship.
So they must form a DAG, where a directed edge exists between one transaction that is spending the output of another transaction.
So a child and a parent, a parent with lots of children, or a grandparent, a parent and a child, et cetera.

Speaker 1: 00:01:53

And so what's important about that?
Why do we want that?

Speaker 3: 00:01:56

Right.
So there's two use cases that people talk about the most.
One is fee bumping a parent or some transaction that does not meet a minimum fee rate on its own, but it has a child or some descendant that allows it to be incentive compatible for a miner to include in a block because it means that they also get to mine that other descendant.
So that's the primary use case.
The other use case that people talk about is orphan fetching.
So an orphan is a transaction from the perspective of a specific node where it spends inputs that this node isn't aware of.
So sometimes that's just a non-existent input, but more often in the happy use case it's just, oh maybe you just came out of IBD, you have an empty mempool, and this transaction is spending an output from another unconfirmed transaction that was broadcast like a few hours ago, for example.
You just weren't around to hear it and so that would be an orphan.
And right now the way that we handle orphans is we request their parents based on the TX IDs of those inputs that we're missing but requesting by TX ID is inconvenient to dangerous.

## Why do people care about package relay?

Speaker 1: 00:03:13

So we just dove right in we got into package relay and the importance of it.
But I want to zoom out a little bit more.
So this has been out there for eight years.
Why people care?
What are we worried about?

Speaker 3: 00:03:24

Yeah, so the fee bumping use case is a bit of a security issue for a lot of layer two contracting protocols.
And by that I mean, when you have this layer two contracting protocol, you're trying to build some functionality on top of this L1, right?
And the idea is you and some untrusted counterparty are going to create transactions that you're not going to broadcast, hopefully.
But if something goes wrong, then you can go and settle on-chain.
And the way that they usually do this is they'll create these transactions that lock you into these spending paths.
And there's end spending paths, for example.
One is the happy case, you know, you move on together because you agreed on something new.
And another is, okay, counterparty tries to cheat.
And the honest party is able to then revoke or redeem the funds that are rightfully theirs before a certain time lock.
And that's the part where it gets really dangerous, because the time that you're signing the transaction and the time that you go to broadcast that transaction sometime in the future can be very far apart.
It requires you, when you're signing the transaction, to either have some clairvoyance as to like, okay, what fee rate am I going to need in order to get this transaction confirmed on time?
Or requires you to be able to fee bump in the future if you were not clairvoyant and you accidentally put too low of a fee and either the mempool traffic has increased or whatever it is.
So then in these contracting protocols, fee bumping becomes a security issue.

## What are these "contracting protocols" package relay matters for?

Speaker 1: 00:05:05

Why do we keep calling it contracting protocols?
We're talking about Lightning, right?

Speaker 3: 00:05:08

So Lightning is the biggest use case because they use this pattern of pre-signed time-sensitive transactions and I would also count DLCs. I would also count vaults.
So one implementation of a vault re-vault has this revocation transaction a cancel.
So if one of your vault parties tries to un-vault and spend money, you within a certain period of time can then cancel that un-vault.
Same thing with DLCs, they have a refund transaction where it's like, okay, if Oracle didn't respond or whatever, you can always go back on chain and be like, hey, it didn't happen.
And same thing with L2, which is a proposed improvement to Lightning, but right now they're very hamstrung by this, like, oh, we don't have the fee bumping options that make this secure.

Speaker 0: 00:05:59

I think we can generally summarize this as, we are in a situation where we have a pre-signed transaction that we cannot change and its fee rate is locked in but we also rely on being able to get a confirmation within a certain time frame.

Speaker 3: 00:06:14

Yes, Exactly.
And that combination of conditions is quite dangerous, because that means you have to have a fee bumping option that works.

Speaker 0: 00:06:22

Because we do not have any propagation or confirmation guarantees for unconfirmed transactions.

## Pinning attacks

Speaker 1: 00:06:28

And there's a name for that kind of attack.

Speaker 3: 00:06:30

Yes.
So I would like to credit, I think, either BlueMatt, Anton Riart, or T-Bast with coining the term pinning attack, which is a type of censorship attack on unconfirmed transactions where you use the fact that there's no propagation guarantees, and specific limitations in mempool policy across nodes in the network to prevent a transaction from getting into the mempool or getting mined.

## Why do you work on package relay?

Speaker 1: 00:06:57

Cool.
What attracted you to this project?
Why this?
You've made a ton of progress for someone in their first year of Bitcoin Core development.

Speaker 3: 00:07:05

Thank you.

Speaker 1: 00:07:06

And I think there's a lot of lessons to be learned in terms of how you've done that, because a change of this size is not easy to get people excited about or to sort of navigate the social pieces of getting code merged.
But yeah, why this?

Speaker 3: 00:07:22

Yeah, good question.
I think it started from me spending a little bit of time in the mempool code and realizing how freaking cool it is because there's so many interesting trade-offs and security concerns you have to be mindful of.
And then I very quickly figured out that package relay relies primarily getting a safe mempool validation logic in there first.
And then you can talk about packages on P2P.
And then I also figured out that package relay is like super non-controversial.
I've never heard anyone say, we don't need package relay.
How'd you figure that out?
Because I would just talk to people and they would be like, oh, it would be so nice if we had package relay.
Cause then we could have XYZ and it's like, oh, we can't do this yet because there's no package relay.
So this is insecure.

Speaker 1: 00:08:13

So then there's just not that much low hanging fruit around the project.
Why hasn't this been done before?

Speaker 3: 00:08:18

Not to toot my horn too much, I guess.
Cause it's like difficult.
Toot away.

Speaker 1: 00:08:24

That's what we're all here for.

Speaker 3: 00:08:28

I think just the process of figuring out the design space, like figuring out what really is the commonality between all of these constraints that people have.
And abstractly us being able to come here and say, yeah, in summary, it's pre-signed and it's untrusted and they need fee bumping.
Like that's something that was figured out recently, right?
And then you need a good idea of what the L2 projects out there are.
You need a way to talk to the developers and ask what their desired interface is.
You need a good idea of mempool validation and how to get something in there that's safe.
And then you have to look at the hairy spaghetti TX relay code and net processing and figure out, okay, how does this interact with Erlay?
How does it interact with all these other P2P messages?
The big hairy mess that is transaction relay.
How do we then make it even more complicated and add package relay?
So it requires a lot of exploring.

Speaker 1: 00:09:30

And as you're thinking about the complexity, have you been able to clean up things as you're complicating things?

Speaker 3: 00:09:36

Yeah, I think that that's my approach is like not to make it more spaghetti And also like I think refactoring helps clarify the interface for everyone So for example, like part of package RBF was modularizing and documenting our current replace by fee policy and pushing that into its own module.
And then now it's just like five helper functions and like package RBF, as I've implemented it now is just calling those same functions with a few different arguments.
So that's nice.
And now we hopefully understand RBF better.
But that kind of also opened a can of worms, and now people want all of the RBF pinning attacks to be solved.
But yeah, I think it's also a nice opportunity to clean things up.

## What's special about the mempool?

Speaker 1: 00:10:19

And this fascination with mempool, like what makes mempool unique and special of all the things you could have gone after?
It's sort of putting a fork in the socket.
It's scary, but you learn a lot.

Speaker 3: 00:10:29

Yeah, definitely.
I like to say that mempool is where the ideologies that we Bitcoiners have really translate into technical problems.
So for example, this idea of permissionless, right?
Like censorship resistance.
Anyone anywhere should be able to send a payment, regardless of what country they live in or politics, like attempted financial censorship by people.
Like they should be able to just run a Raspberry Pi Bitcoin node and broadcast their transaction on this P2P network where you're able to hide a little bit because all the peers look the same.
There's no permission you need to join the network, yada, yada.
But then also the flip side to that is since anybody can join and you don't really know who people are, there's probably gonna be bad guys.
And so I really enjoy the highest level of security model possible.
You can never take for granted like, oh, we're just gonna throw in this assertion there.
And as long as the peers don't send something crazy, it's not gonna be hit.
We can't do that because if somebody does send it and they might, then all the network nodes will crash.
And likewise, it's like, okay, yeah, you know, we'll keep processing these orphans until we're done.
Well, if you don't limit the resources you allocate for them, then someone could send out a transaction or set of transactions that causes all of the network nodes to stall.
And even if that stalling is only for 10 seconds, that's a reasonable head start if you're a miner and looking to get a head start on the next block.
There's so much danger, it's very exciting.

## How do you approach the security considerations?

Speaker 1: 00:12:08

And so as you start to unravel those denial-of-service attacks, you don't have a security background.
Like how are you growing your own experience with thinking about this critical part of the code and also reaching out to people who have been working in and around mempool for a while.
How is that all coming together in your head?

Speaker 3: 00:12:26

Well I have a big whiteboard.
I've gotten a lot of help from people who have worked on Mempool, like Sue Haas and Blue Matt and John.
So having those people there to be like, hey, Glory, you actually can't do that.
That's going to be really dangerous.
It's like, oh, I didn't realize.

Speaker 1: 00:12:47

When you're asking those questions or they're reviewing your proposals, are there second order?
Like, well, what if we look deeper into this?
Are you proving the sort of the beginner mindset is allowing you to ask questions about how we think about mempool and yeah, just sort of like questioning the assumptions that we have about how it's constructed.

Speaker 3: 00:13:06

Yeah, I do think as a beginner, we maybe have a bit less of the instinct people often have when reviewing code, where they see what they want to see instead of what's actually there.
I think we don't take as many things for granted.
I think Martin talked about this on his podcast of just like, is that really true?
Let's go and verify it.
For me, it's literally like, I don't even know how this works, so I have to go and maybe spend a day whiteboarding it.
Yeah.

Speaker 1: 00:13:32

And then how do you capture that?
That's really valuable.
And we don't want Gloria Junior to have to do the same thing.
We want to somehow capture and memorialize that kind of information.
So like, what do you do?

Speaker 3: 00:13:44

I sometimes publish notes.

Speaker 1: 00:13:46

No, that's not an accusation.
I'm just saying like, this information organization problem is definitely something that I think a lot about as in if you have something that's so mission-critical and so scary and you have someone who has the bravery to just dive in and be like, I'm going to own this thing.
I'm going to master this thing.
I'm going to really get it.
Now there's value in the torture of that process in the first place, but can't we just like make it a little bit easier or even an order of magnitude easier for the next person who's diving in after you?

Speaker 0: 00:14:17

Well, maybe let me take this one.
I've read some of the notes that Gloria has written, and it's made it much easier for me to understand what sort of problems we get from basically giving everybody permission to send data to us.
And I've also seen reactions to her mailing list contributions where people only see part of the problem maybe say, Oh, isn't that much easier though?
But it really isn't when you when you start reading and looking into it more and more, you have this huge conflict between the huge attack surface that you have, but also wanting it because you need it to allow everybody to use Bitcoin in a censorship-free way.
So yeah, basically there are these notes, there are these mailing list posts that are probably going to be seminal pieces that we point people at.
Read this, then come back and talk.

Speaker 3: 00:15:02

Yeah, especially when they'll talk about like, oh, we have this in block relay.
Like, why don't you do this in transaction relay?
Block relay is easy.
Like when you send a header that's 80 bytes and they had to put a proof of work on it to make it valid.
That's easy to deal with.
We make notes, we make review clubs, you know, we put stuff out there for people to read, but I don't think there's a way for someone to just read five sentences and get time to be like, for example.

## Synthesizing information for the ones coming after you

Speaker 1: 00:15:28

Yeah, I'm not saying that, you know, you need an Eli Five kind of thing.
When someone goes through that pain, the idea is to save at least a portion of that pain for the next person.
And incrementally, it improves over time.
And if we can, again, memorialize that process, then You get other people who get excited about mempool and either could lend you a hand because they actually grok it or they come and do another improvement behind you.
And so this is, you know, the classic Gmax kind of thing.
Like Gmax has thought about all of the problems and wrote it down.
Often it has been recorded somewhere.
It's just everywhere.
And like, combing through IRC logs and random stack exchange answers and some video he did.

Speaker 0: 00:16:11

Some personal write-up on his website.

Speaker 1: 00:16:12

Or like, yeah, the website that's now been taken down.
It's just like, how do you bring that all together to something that someone can actually comprehend?
And I don't know how much of a painful process that was for someone like him But you have gone through some pain and the question is like how do you then translate that pain into?
Artifacts that can be useful for you know the future.

Speaker 3: 00:16:34

Well, I have two notes repositories where I- It's somewhat of a rhetorical question because I think you've done a good job in doing that.

Speaker 1: 00:16:41

I'm not, I'm not, I'm not accusing you of not doing it.

Speaker 0: 00:16:43

Why are you talking about pain so much?

Speaker 1: 00:16:46

Because I've, I've witnessed some of the pain and I think it's valuable for contributors who don't understand what it's like to take on a really hard project to understand what you're taking on.
There is some level of mental torture that goes through in trying something really hard, taking a really big swing and doing it just so early in your Bitcoin Core career.
And I think that's what I'm talking about.
Yeah.

Speaker 3: 00:17:08

Yeah, I don't know if the issue is there not being enough educational material.
One thing I wish we could cultivate more is the act of reading through someone's mailing list post before responding to it,

Speaker 2: 00:17:19

for example.

Speaker 3: 00:17:24

You know, like I think we should place more value.
I don't think we as a community encourage slash reward synthesizing information and presenting feedback in a constructive way.
And if we want more of that, then we should encourage stuff that's already done for it.

Speaker 0: 00:17:43

One moment of silence for the sick bird.

Speaker 1: 00:17:46

Tell us about the current status and sort of what happens next in terms of making this change happen.

## What's next for package relay?

Speaker 3: 00:17:51

Yeah, so like you said, it's pretty big.
And I posted it with the mindset of people are going to have opinions and it might change.
Like when I posted the package mempool policy post, I was like pretty sure this was the best way to do it.
And I think most people agreed.
Right now I'm getting a bit more feedback on like, okay, how do we make these P2P messages more efficient?
Why don't we add some of these conventions that are sometimes used that I wasn't aware of, for example.
I think we hopefully iterate a little bit until we get to a final set of protocol changes.
And then, you know, I make those tweaks to my implementation and flesh it out more.
And you know, we merge it and we test it hopefully for at least a release.
We air it with L2 devs, see if this interface is working for all of their use cases and then...

Speaker 1: 00:18:41

So how do you plan on testing it?
You'll have it behind a flag or like what's the...

Speaker 3: 00:18:45

Yeah it'll be behind a flag for sure at first.
And then, you know, you can have testnet nodes relaying packages to each other.
You can see what happens when there's interactions between package relay nodes and non-package relay nodes.
I was thinking about one potential problem for un-upgraded nodes that maybe we should merge something right now to fix so that two releases from now when package relay is new, then anyone who upgraded within the last two releases should do it.

Speaker 1: 00:19:13

What about simulation?
Is that something that can be simulated?
Is that something that you're thinking about?

Speaker 3: 00:19:17

Yeah, so simulations make a lot of sense for something like Erlay when you're trying to motivate it based on bandwidth usage, for example, in a wide network of nodes.
I think for the use cases that I'm looking at, it's more does this package propagate?
And then, so what we want to probably do is, of course, simulate in different topologies, but I think what really matters is what the transactions are rather than what the network looks like.

Speaker 1: 00:19:44

And can't you use historical data to figure out the transaction constellations?

Speaker 3: 00:19:47

Yes, yes.
But it's also like we're trying to enable transactions that couldn't be relayed before.

Speaker 1: 00:19:53

I see.

Speaker 3: 00:19:53

So I think what I would ask for, maybe I'd go to Asanc and LDK and LND and be like, hey, can you send me some raw transaction data?
And by the way, there's this RPC that I recommend you test on.
And then as they're perhaps developing wallet logic for fee bumping using package relay, then they use that interface.
But yeah, there's all kinds of ways to test.

Speaker 0: 00:20:17

So being a little behind on my mailing list reading, does this, for example, now enable zero fee transactions and a child that bring your own fees?

Speaker 3: 00:20:26

Yes.
Cool.
So this brings me to say we deploy package Relay and now Lightning, because they can, puts zero fees on their commitment transactions and they all have anchor outputs and you're going to attach a high fee child to the anchor output when you broadcast.
So I think it would be fine as long as you have a good amount of nodes on the network and there's always a path to get from your node to a miner so that they can mine your transaction.

Speaker 1: 00:20:51

So you've waded into the space between L2 and the base layer.

## Bridging protocol development with L2

Speaker 1: 00:20:56

Yeah.
And that's like a pretty amorphous space.
There's not a lot of people that are really being that bridge.
Yeah.
What has that been like?
How do you feel about the L2 technology that's being created?
And yeah, you sort of started with Bitcoin Core, but now you're expanding out to other projects.
What's your impression?

Speaker 3: 00:21:11

Well, I haven't really worked on those other projects.
I've just interacted with their devs and they've all been really nice.
I think because I'm always like, hey, I'm trying to help.

Speaker 2: 00:21:22

Like, what do you want from the Bitcoin Core interface?

Speaker 3: 00:21:27

And in the beginning, I think there were a few interactions where even on L2, the security models is a little bit laxer.
And so in the beginning, there were a few bad interactions I had where people had kind of unrealistic expectations of what we can do, because they'll be like, why don't you just do this?
And it's like, well, that's a trivial DOS attack.
You know, it's hard to look at both Bitcoin and Lightning or Bitcoin and, you know, whatever that application is.
So for me, I've learned a lot about diplomacy.

Speaker 1: 00:22:00

That's a very diplomatic way of saying that.

Speaker 3: 00:22:03

Yeah, so like I don't pretend to like know how Lightning works.
The bolt I visit the most is bolt three, which is the transactions like structure.
But other than that, like I don't know really anything.
I don't know anything about networking and in lightning.
I just ask like hey we have to define a clear interface between our code and your code our Network and your network because we rely on each other right like Bitcoin cannot do thousands of transactions per second and lightning transactions are Bitcoin transactions.

Speaker 1: 00:22:34

Well, maybe not Bitcoin Core, but there's other Bitcoin implementations.

Speaker 0: 00:22:37

Yeah! Oh, Drew.
Drew.
No.

Speaker 1: 00:22:43

Okay, cool.
So, thanks for joining us And we are going to link your Brink podcast about mempool policy.
We are going to link to your talk at Advancing Bitcoin, which is the intro to mempool policy.
We are going to link to your talk about mempool policy for L2 devs.
We are going to link to your diagrams.
I mean, you're pretty good at code, but your diagrams seem to be your real talent.

Speaker 3: 00:23:09

You might want to be thinking about a professional diagrammer.
This is what I mean when like the bar is so low when it comes to like Bitcoin devs being able to express themselves.
Thank you for the compliment.
I think more people should add diagrams to explain things that are complex because...

Speaker 1: 00:23:27

They got like colors and stuff though?
I don't know.

Speaker 0: 00:23:30

They're really good to understand the things you're talking about.

Speaker 1: 00:23:33

Thank you.

Speaker 0: 00:23:34

And a lot of stuff is just wall of text and that's not always the best way of explaining stuff.

Speaker 3: 00:23:38

Well, and like poorly written wall of text is very common too.

Speaker 1: 00:23:42

Yeah.
Well, this isn't a show about critiquing other people's walls of text.
Yeah.

Speaker 3: 00:23:47

Well, I think in general, if there's Bitcoin devs listening to this, let's just raise the bar in terms of how we communicate with each other.

Speaker 1: 00:23:56

You heard here, called out by Gloria for not doing what she wants to be doing.
Thank you, Gloria.

Speaker 3: 00:24:02

Thank you for having me.

Speaker 1: 00:24:07

Well, we've been trying to avoid the wrap-up question of, what do you think of that?
I don't know how else to ask it.
So that was interesting.

Speaker 0: 00:24:15

I think we got a very digestible, solid talk.
And I think people listening to this will get a decent sense of what Package really is about.

Speaker 1: 00:24:26

I wanted to talk about the cultural stuff maybe more than you two did, but I think it's really interesting as a case study to see someone who's pretty new to take a big swing like this.
And for the most part, at least from my perspective, it's been incredibly successful.
And I think there's a lot of lessons there for both experienced and inexperienced devs in terms of getting their stuff in.

Speaker 0: 00:24:46

I find it also really fascinating to watch where the actual Troubledon ends up finding reviewers that have a deep enough understanding of the topic to actually comment on it.

Speaker 1: 00:24:57

But you found a way to motivate them too.

Speaker 0: 00:24:59

Yeah, yeah.
But a lot of projects just stall out because they make good progress and then there's nobody there that can interact with it and give good feedback and help getting it polished to actually being put in.
And here, this is a good example of it working, but this is rough for a lot of big projects.

Speaker 1: 00:25:16

There's definitely some reviewer fatigue that sets in after many months of back and forth.
And I can see a lot of momentum from projects that people were really excited about.
They just lose steam.
And then the author gets discouraged.
And again, it's sort of this, I wouldn't call it a death spiral, but it's a sad spiral of some sort.

Speaker 0: 00:25:35

Yeah, it takes a lot of stamina to get through a big project like this.
And we have a few that we're watching up close here.

Speaker 1: 00:25:43

All right, enjoyed the conversation.
Hope you did too.
And we'll talk to you next time.
