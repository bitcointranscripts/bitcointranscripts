---
title: Package Relay
transcript_by: varmur via review.btctranscripts.com
media: https://podcasters.spotify.com/pod/show/chaincode/episodes/Gloria-Zhao-and-Package-Relay---Episode-21-e1j0ii3
tags:
  - package-relay
  - security
speakers:
  - Gloria Zhao
summary: Gloria Zhao sits down with us to discuss her package relay proposal and what it is like as a relative newcomer to propose a big change.
date: 2022-05-24
episode: 21
additional_resources:
  - title: 'Mailing List: Package Relay Proposal'
    url: https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-May/020493.html
  - title: 'Mailing List: Package Mempool Accept and Package RBF'
    url: https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-September/019464.html
  - title: 'Brink Podcast: Ep1 Mempool Policy'
    url: https://brink.dev/podcast/1-mempool-policy/
  - title: 'Censorship and DoS Attacks: An intro to Mempool Policy'
    url: https://vimeo.com/704956163
  - title: Transaction Relay Policy for L2 Developers
    url: https://www.youtube.com/watch?v=fbWSQvJjKFs
  - title: Mempool Garden
    url: https://github.com/glozow/bitcoin-notes/tree/master/mempool_garden
aliases:
  - /chaincode-labs/chaincode-podcast/package-relay/
---
## Introduction

Mark Erhardt: 00:00:00

Hey Jonas.

Adam Jonas: 00:00:00

Hey Murch.

Mark Erhardt: 00:00:01

We're going to try again to record with Gloria.
This time we want to get it really focused, short.

Adam Jonas: 00:00:07

We got a lot of tape in that last one, but I don't know if all of it was usable.
Yeah, we're going to talk to Gloria today about her newly released proposal for package relay.
Looking forward to getting something that we can release.
Enjoy.

Adam Jonas: 00:00:35

Hey, Gloria.

Gloria Zhao: 00:00:36

Hello.

Adam Jonas: 00:00:37

Welcome back to Chaincode.
This is our second time recording, but this one's going to be comprehensible, I think (Gloria's laughter).
I think we're going to make it work.

Mark Erhardt: 00:00:44

Yeah, I promise not to break all the discussions.

Adam Jonas: 00:00:48

It'll be fine, we don't have to... let's not get too in over our head.

Gloria Zhao: 00:00:51

It's a deep topic.

Adam Jonas: 00:00:52

It's a deep topic.
What I like about this conversation is you have something very specific to talk about.

Gloria Zhao: 00:00:58

Right.

Adam Jonas: 00:00:58

So you wrote to the mailing list.

Gloria Zhao: 00:01:00

Yes.

## What's package relay?

Adam Jonas: 00:01:01

And you [proposed package relay](https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-May/020493.html).
What's package relay?

Gloria Zhao: 00:01:05

I proposed some implementation of package relay, which is a concept that's been talked about for at least seven, maybe nine years.
It's the concept of requesting, announcing, and downloading groups of transactions together, namely related transactions.
A package is a widely used term for some set of transactions that have a dependency relationship.
So they must form a DAG, where a directed edge exists between one transaction that is spending the output of another transaction - so a child and a parent, a parent with lots of children, or a grandparent, a parent and a child, et cetera.

Adam Jonas: 00:01:53

What's important about that?
Why do we want that?

Gloria Zhao: 00:01:56

Right, so there's two use cases that people talk about the most.

One is fee bumping a parent or some transaction that does not meet a minimum fee rate on its own, but it has a child or some descendant that allows it to be incentive compatible for a miner to include in a block, because it means that they also get to mine that other descendant.
So that's the primary use case.

The other use case that people talk about is orphan fetching.
An orphan is a transaction from the perspective of a specific node, where it spends inputs that this node isn't aware of.
Sometimes that's just a non-existent input, but more often, in the happy use case it's - maybe you just came out of IBD, you have an empty mempool, and this transaction is spending an output from another unconfirmed transaction that was broadcast a few hours ago, for example.
You just weren't around to hear it, and so that would be an orphan.
Right now the way that we handle orphans is we request their parents based on the `txid`'s of those inputs that we're missing, but requesting by `txid` is inconvenient to dangerous.

## Why do people care about package relay?

Adam Jonas: 00:03:13

So, we just dove right in.
We got into package relay and the importance of it.
But I want to zoom out a little bit more.
So this has been out there for eight years.
Why people care?
What are we worried about?

Gloria Zhao: 00:03:24

Yeah, so the fee bumping use case is a bit of a security issue for a lot of layer two contracting protocols.
By that I mean, when you have this layer two contracting protocol, you're trying to build some functionality on top of this L1, right?
The idea is you and some untrusted counterparty are going to create transactions that you're not going to broadcast, hopefully.
But if something goes wrong, then you can go and settle on-chain.
The way that they usually do this, is they'll create these transactions that lock you into these spending paths.
And there's `N` spending paths, for example.

One is the happy case, you move on together because you agreed on something new, and another is, okay, counterparty tries to cheat.
The honest party is able to then revoke or redeem the funds that are rightfully theirs before a certain time lock.
That's the part where it gets really dangerous, because the time that you're signing the transaction, and the time that you go to broadcast that transaction sometime in the future - can be very far apart.

It requires you, when you're signing the transaction, to either have some clairvoyance as to what fee rate am I going to need in order to get this transaction confirmed on time?
Or it requires you to be able to fee bump, in the future, if you were not clairvoyant and you accidentally put too low of a fee, and either the mempool traffic has increased, or whatever it is.
So then in these contracting protocols fee bumping becomes a security issue.

## What are these "contracting protocols" package relay matters for?

Adam Jonas: 00:05:05

Why do we keep calling it contracting protocols?
We're talking about Lightning, right?

Gloria Zhao: 00:05:08

Lightning is the biggest use case because they use this pattern of pre-signed time sensitive transactions and I would also count DLCs.
I would also count vaults.

One implementation of a vault - Revault - has this revocation transaction - a cancel.
So if one of your vault parties tries to un-vault and spend money, you within a certain period of time can then cancel that un-vault.
Same thing with DLCs, they have a refund transaction where if the Oracle didn't respond or whatever, you can always go back on chain and be like, hey, it didn't happen.
The same thing with Eltoo, which is a proposed improvement to Lightning, but right now they're very hamstrung by (not having) the fee bumping options that make this secure.

Mark Erhardt: 00:05:59

I think we can generally summarize this as: we are in a situation where we have a pre-signed transaction that we cannot change, and its fee rate is locked in, but we also rely on being able to get a confirmation within a certain time frame.

Gloria Zhao: 00:06:14

Yes, exactly, and that combination of conditions is quite dangerous, because that means you have to have a fee bumping option that works.

Mark Erhardt: 00:06:22

Because we do not have any propagation or confirmation guarantees for unconfirmed transactions.

## Pinning attacks

Adam Jonas: 00:06:28

And there's a name for that kind of attack.

Gloria Zhao: 00:06:30

Yes.
So I would like to credit, I think, either BlueMatt, Antoine Riard, or t-bast with coining the term "pinning attack," which is a type of censorship attack on unconfirmed transactions, where you use the fact that there's no propagation guarantees and specific limitations in mempool policy across nodes in the network to prevent a transaction from getting into the mempool or getting mined.

## Why do you work on package relay?

Adam Jonas: 00:06:57

Cool.
What attracted you to this project?
Why this?
You've made a ton of progress for someone in their first year of Bitcoin Core development.

Gloria Zhao: 00:07:05

Thank you.

Adam Jonas: 00:07:06

I think there's a lot of lessons to be learned in terms of how you've done that, because a change of this size is not easy to get people excited about, or to navigate the social pieces of getting code merged.
But yeah, why this?

Gloria Zhao: 00:07:22

Yeah, good question.
I think it started from me spending a little bit of time in the mempool code and realizing how freaking cool it is, because there's so many interesting trade-offs and security concerns you have to be mindful of.
Then I very quickly figured out that package relay relies on primarily getting a safe mempool validation logic in there first, and then you can talk about packages on P2P.

Then I also figured out that package relay is super non-controversial.
I've never heard anyone say, we don't need package relay.

Adam Jonas: 00:08:00

How'd you figure that out?

Gloria Zhao: 00:08:01

Because I would just talk to people and they would be like, "Oh, it would be so nice if we had package relay, cause then we could have XYZ," and it's like, "Oh, we can't do this yet because there's no package relay, so this is insecure."

Adam Jonas: 00:08:13

So then there's just not that much low hanging fruit around the project.
Why hasn't this been done before?

Gloria Zhao: 00:08:18

Not to toot my horn too much, I guess because it's difficult.

Adam Jonas: 00:08:24

Toot away.
That's what we're all here for (laughter).

Gloria Zhao: 00:08:28

I think just the process of figuring out the design space, figuring out what really is the commonality between all of these constraints that people have, and abstractly us being able to come here and say, "Yeah, in summary, it's pre-signed, and it's untrusted, and they need fee bumping."
That's something that was figured out recently, right?

Then you need a good idea of what the L2 projects out there are.
You need a way to talk to the developers and ask what their desired interface is.
You need a good idea of mempool validation and how to get something in there that's safe.
Then you have to look at the hairy spaghetti TX relay code and net processing and figure out, okay, how does this interact with [Erlay](https://bitcoinops.org/en/topics/erlay/)?
How does it interact with all these other P2P messages?
The big hairy mess that is transaction relay.
How do we then make it even more complicated and add package relay?
So it requires a lot of exploring.

Adam Jonas: 00:09:30

As you're thinking about the complexity, have you been able to clean up things as you're complicating things?

Gloria Zhao: 00:09:36

Yeah, I think that that's my approach.
Not to make it more spaghetti, and also I think refactoring helps clarify the interface for everyone.
So for example, part of [Package RBF](https://gnusha.org/url/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-September/019464.html) was modularizing and documenting our current Replace-by-Fee policy and pushing that into its own module.
Now it's just five helper functions and Package RBF, as I've implemented it now, is just calling those same functions with a few different arguments.
So that's nice, and now we hopefully understand RBF better.
But that kind of also opened a can of worms, and now people want all of the RBF pinning attacks to be solved.
But yeah, I think it's also a nice opportunity to clean things up.

## What's special about the mempool?

Adam Jonas: 00:10:19

This fascination with mempool, what makes mempool unique and special - of all the things you could have gone after?
It's sort of putting a fork in the socket.
It's scary, but you learn a lot.

Gloria Zhao: 00:10:29

Yeah, definitely.
I like to say that mempool is where the ideologies that we Bitcoiners have really translate into technical problems.
For example, this idea of permissionless, right?
Censorship resistance.
Anyone anywhere should be able to send a payment, regardless of what country they live in or politics, like attempted financial censorship by people.
They should be able to just run a Raspberry Pi Bitcoin node and broadcast their transaction on this P2P network where you're able to hide a little bit because all the peers look the same.
There's no permission you need to join the network, yada, yada.

But then also, the flip side to that is since anybody can join and you don't really know who people are, there's probably gonna be bad guys.
So I really enjoy the highest level of security model possible.
You can never take for granted like - oh, we're just gonna throw in this assertion there, and as long as the peers don't send something crazy, it's not gonna be hit.
We can't do that because if somebody does send it, and they might - then all the network nodes will crash.

And likewise, it's like - okay, we'll keep processing these orphans until we're done.
Well, if you don't limit the resources you allocate for them, then someone could send out a transaction, or set of transactions that causes all of the network nodes to stall.
Even if that stalling is only for 10 seconds, that's a reasonable head start if you're a miner and looking to get a head start on the next block.
There's so much danger, it's very exciting (laughter).

## How do you approach the security considerations?

Adam Jonas: 00:12:08

As you start to unravel those denial-of-service attacks, you don't have a security background.
How are you growing your own experience with thinking about this critical part of the code and also reaching out to people who have been working in and around mempool for a while.
How is that all coming together in your head?

Gloria Zhao: 00:12:26

Well, I have a big whiteboard (laughter).

Mark Erhardt: 00:12:32

I can attest to that.

Gloria Zhao: 00:12:33

I've gotten a lot of help from people who have worked on mempool, like Suhas and Blue Matt and John.
So having those people there to be like, "Hey, Gloria, you actually can't do that.
That's going to be really dangerous".
It's like, "Woah, I didn't realize".

Adam Jonas: 00:12:47

When you're asking those questions or they're reviewing your proposals, are there second order... like, well, what if we look deeper into this?
Are you proving the beginner mindset is allowing you to ask questions about how we think about the mempool, and questioning the assumptions that we have about how it's constructed?

Gloria Zhao: 00:13:06

Yeah, I do think as a beginner, we maybe have a bit less of the instinct people often have when reviewing code, where they see what they want to see instead of what's actually there.
I think we don't take as many things for granted.
I think Martin talked about this on his podcast of just like, "Is that really true? Let's go and verify it".
For me, it's literally like, I don't even know how this works, so I have to go and maybe spend a day white-boarding it.
Yeah.

Adam Jonas: 00:13:32

How do you capture that?
That's really valuable.
We don't want Gloria Junior to have to do the same thing, we want to somehow capture and memorialize that kind of information.
So, what do you do?

Gloria Zhao: 00:13:44

I sometimes publish notes (laughter).

Adam Jonas: 00:13:46

No, that's not an accusation.
I'm just saying - this information organization problem is definitely something that I think a lot about, as in if you have something that's so mission-critical and so scary and you have someone who has the bravery to just dive in and be like - I'm going to own this thing.
I'm going to master this thing.
I'm going to really get it.
Now there's value in the torture of that process in the first place, but can't we just make it a little bit easier, or even an order of magnitude easier for the next person who's diving in after you?

Mark Erhardt: 00:14:17

Well, maybe let me take this one.
I've read some of the notes that Gloria has written, and it's made it much easier for me to understand what sort of problems we get from basically giving everybody permission to send data to us.
I've also seen reactions to her mailing list contributions where people who only see part of the problem maybe say, "Oh, isn't that much easier though?".
But it really isn't, when you start reading and looking into it more and more, you have this huge conflict between the huge attack surface that you have, but also wanting it because you need it to allow everybody to use Bitcoin in a censorship-free way.
So yeah, there are these notes, there are these mailing list posts that are probably going to be seminal pieces that we point people at - read this, then come back and talk.

Gloria Zhao: 00:15:02

Yeah, especially when they'll talk about like, "Oh, we have this in block relay, why don't you do this in transaction relay?"
Block relay is easy.
When you send a header that's 80 bytes, they had to put a Proof-of-Work on it to make it valid.
That's easy to deal with (laughs).
We make notes, we make review clubs, we put stuff out there for people to read, but I don't think there's a way for someone to just read five sentences and get time to be like, for example...

## Synthesizing information for the ones coming after you

Adam Jonas: 00:15:28

Yeah, I'm not saying that you need an ELI5 kind of thing.
When someone goes through that pain, the idea is to save at least a portion of that pain for the next person, and incrementally, it improves over time.
If we can, again, memorialize that process, then you get other people who get excited about mempool and either could lend you a hand because they actually grok it, or they come and do another improvement behind you.
So this is the classic GMax (Gregory Maxwell) kind of thing.
GMax has thought about all of the problems and wrote it down.
Often it has been recorded somewhere, it's just everywhere - combing through IRC logs, and random Stack Exchange answers, and some video he did...

Mark Erhardt: 00:16:11

Some personal write-up on his website.

Adam Jonas: 00:16:12

Yeah, the website that's now been taken down.
How do you bring that all together to something that someone can actually comprehend?
I don't know how much of a painful process that was for someone like him, but you have gone through some pain and the question is - how do you then translate that pain into artifacts that can be useful for the future?

Gloria Zhao: 00:16:34

Well, I have two notes repositories where I...

Adam Jonas: 00:16:39

It's somewhat of a rhetorical question because I think you've done a good job in doing that.
I'm not accusing you of not doing it.

Mark Erhardt: 00:16:43

Why are you talking about pain so much?
(laughter)

Adam Jonas: 00:16:46

Because I've witnessed some of the pain, and I think it's valuable for contributors who don't understand what it's like to take on a really hard project to understand what you're taking on.
There is some level of mental torture that goes through in trying something really hard, taking a really big swing, and doing it just so early in your Bitcoin Core career.
I think that's what I'm talking about.

Gloria Zhao: 00:17:08

Yeah, I don't know if the issue is there not being enough educational material.
One thing I wish we could cultivate more is the act of reading through someone's mailing list post before responding to it, for example (laughter).

Adam Jonas: 00:17:23

Burn.

Gloria Zhao: 00:17:24

I think we should place more value...
I don't think we as a community encourage/reward synthesizing information and presenting feedback in a constructive way.
If we want more of that, then we should encourage stuff that's already done for it.

Mark Erhardt: 00:17:43

One moment of silence for the sick burn.

## What's next for package relay?

Adam Jonas: 00:17:46

Tell us about the current status and what happens next in terms of making this change happen.

Gloria Zhao: 00:17:51

Yeah, so like you said, it's pretty big.
I posted it with the mindset of - people are going to have opinions and it might change.
When I posted the package mempool policy post, I was pretty sure this was the best way to do it, and I think most people agreed.
Right now I'm getting a bit more feedback on like - okay, how do we make these P2P messages more efficient?
Why don't we add some of these conventions that are sometimes used that I wasn't aware of, for example.
We hopefully iterate a little bit until we get to a final set of protocol changes.
Then I make those tweaks to my implementation and flesh it out more, and we merge it, and we test it hopefully for at least a release.
We air it with L2 devs, see if this interface is working for all of their use cases and then...

Adam Jonas: 00:18:41

So how do you plan on testing it?
You'll have it behind a flag or like what's the...

Gloria Zhao: 00:18:45

Yeah it'll be behind a flag, for sure, at first.
Then you can have testnet nodes relaying packages to each other.
You can see what happens when there's interactions between package relay nodes and non-package relay nodes.
I was thinking about one potential problem for un-upgraded nodes, that maybe we should merge something right now to fix, so that two releases from now when package relay is new, then anyone who upgraded within the last two releases should do it.

Adam Jonas: 00:19:13

What about simulation?
Is that something that can be simulated?
Is that something that you're thinking about?

Gloria Zhao: 00:19:17

Yeah, so simulations make a lot of sense for something like Erlay when you're trying to motivate it based on bandwidth usage, for example, in a wide network of nodes.
For the use cases that I'm looking at, it's more - does this package propagate?
Of course, simulate in different topologies, but I think what really matters is what the transactions are, rather than what the network looks like.

Adam Jonas: 00:19:44

And can't you use historical data to figure out the transaction constellations?

Gloria Zhao: 00:19:47

Yes, yes, but it's also like we're trying to enable transactions that couldn't be relayed before.

Adam Jonas: 00:19:53

I see.

Gloria Zhao: 00:19:53

So what I would ask for, maybe I'd go to ACINQ and LDK and LND and be like - hey, can you send me some raw transaction data?
And by the way, there's this RPC that I recommend you test on.
Then as they're perhaps developing wallet logic for fee bumping using package relay, then they use that interface.
But yeah, there's all kinds of ways to test.

Mark Erhardt: 00:20:17

So being a little behind on my mailing list reading, does this, for example, now enable zero fee transactions and a child that bring your own fees?

Gloria Zhao: 00:20:26

Yes.

Mark Erhardt: 00:20:27

Cool.

Gloria Zhao: 00:20:28

So this brings me to - say we deploy package relay, and now Lightning, because they can, puts zero fees on their commitment transactions, and they all have anchor outputs and you're going to attach a high fee child to the anchor output when you broadcast.
I think it would be fine as long as you have a good amount of nodes on the network, and there's always a path to get from your node to a miner so that they can mine your transaction.

## Bridging protocol development with L2

Adam Jonas: 00:20:51

So you've waded into the space between L2 and the base layer, and that's a pretty amorphous space.
There's not a lot of people that are really being that bridge.
What has that been like?
How do you feel about the L2 technology that's being created?
You started with Bitcoin Core, but now you're expanding out to other projects.
What's your impression?

Gloria Zhao: 00:21:11

Well, I haven't really worked on those other projects.
I've just interacted with their devs and they've all been really nice.
I think because I'm always like - hey, I'm trying to help, like - what do you want from the Bitcoin Core interface?

In the beginning, I think there were a few interactions where even on L2, the security models is a little bit laxer.
So in the beginning, there were a few bad interactions I had where people had unrealistic expectations of what we can do, because they'll be like - why don't you just do this?
And it's like - well, that's a trivial DOS attack.
It's hard to look at both Bitcoin and Lightning, or Bitcoin and whatever that application is.
So for me, I've learned a lot about diplomacy (laughs).

Adam Jonas: 00:22:00

That's a very diplomatic way of saying that.

Gloria Zhao: 00:22:03

Yeah, so I don't pretend to know how Lightning works.
The BOLT I visit the most is BOLT3, which is the transaction's structure, but other than that, I don't know really anything.
I don't know anything about networking and in lightning.
I just ask like - hey we have to define a clear interface between our code and your code, our network and your network, because we rely on each other, right?
Bitcoin cannot do thousands of transactions per second and Lightning transactions are Bitcoin transactions.

Adam Jonas: 00:22:34

Well, maybe not Bitcoin Core, but there's other Bitcoin implementations (laughter).
So, thanks for joining us, and we are going to link your [Brink podcast about mempool policy.](https://brink.dev/podcast/1-mempool-policy/)
We are going to link to your [talk at Advancing Bitcoin](https://vimeo.com/704956163), which is the intro to mempool policy.
We are going to link to your [talk about mempool policy](https://www.youtube.com/watch?v=fbWSQvJjKFs) for L2 devs.
We are going to link to your [diagrams](https://github.com/glozow/bitcoin-notes/tree/master/mempool_garden).
I mean, you're pretty good at code, but your diagrams seem to be your real talent (laughter).
You might want to be thinking about a professional diagrammer.

Gloria Zhao: 00:23:12

This is what I mean, the bar is so low when it comes to Bitcoin devs being able to express themselves.
Thank you for the compliment.
I think more people should add diagrams to explain things that are complex because...

Adam Jonas: 00:23:27

They've got like colors and stuff though?
I don't know.

Mark Erhardt: 00:23:30

They're really good to understand the things you're talking about.

Gloria Zhao: 00:23:33

Thank you.

Mark Erhardt: 00:23:34

A lot of stuff is just wall of text, and that's not always the best way of explaining stuff.

Gloria Zhao: 00:23:38

Well, and poorly written wall of text is very common too.

Adam Jonas: 00:23:42

Yeah.
Well, this isn't a show about critiquing other people's walls of text (laughter).

Gloria Zhao: 00:23:47

Well, I think in general, if there's Bitcoin devs listening to this, let's just raise the bar in terms of how we communicate with each other.

Adam Jonas: 00:23:56

You heard here, called out by Gloria for not doing (laughs) what she wants to be doing.
Thank you, Gloria.

Gloria Zhao: 00:24:02

Thank you for having me.

## Wrap-Up

Adam Jonas: 00:24:07

Well, we've been trying to avoid the wrap-up question of, what do you think of that?
I don't know how else to ask it.
So that was interesting.

Mark Erhardt: 00:24:15

I think we got a very digestible, solid talk.
I think people listening to this will get a decent sense of what package relay is about.

Adam Jonas: 00:24:26

I wanted to talk about the cultural stuff maybe more than you two did, but I think it's really interesting as a case study to see someone who's pretty new to take a big swing like this, and for the most part, at least from my perspective, it's been incredibly successful.
I think there's a lot of lessons there for both experienced and inexperienced devs in terms of getting their stuff in.

Mark Erhardt: 00:24:46

I find it also really fascinating to watch where the actual trouble then ends up being finding reviewers that have a deep enough understanding of the topic to actually comment on it.

Adam Jonas: 00:24:57

But you found a way to motivate them too.

Mark Erhardt: 00:24:59

Yeah, yeah, but a lot of projects just stall out because they make good progress and then there's nobody there that can interact with it, and give good feedback, and help getting it polished to actually being put in.
Here, this is a good example of it working, but this is rough for a lot of big projects.

Adam Jonas: 00:25:16

There's definitely some reviewer fatigue that sets in after many months of back and forth, and I can see a lot of momentum from projects that people were really excited about, they just lose steam, then the author gets discouraged.
I wouldn't call it a death spiral, but it's a sad spiral of some sort.

Mark Erhardt: 00:25:35

Yeah, it takes a lot of stamina to get through a big project like this, and we have a few that we're watching up close here.

Adam Jonas: 00:25:43

All right, enjoyed the conversation.
Hope you did too, and we'll talk to you next time.
