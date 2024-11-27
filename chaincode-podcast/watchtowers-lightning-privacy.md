---
title: Watchtowers, Lightning Privacy
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://podcasters.spotify.com/pod/show/chaincode/episodes/Sergi-Delgado-and-Watchtowers--Lightning-Privacy---Episode-28-e1uce42
tags:
  - lightning
  - privacy
  - watchtowers
speakers:
  - Sergi Delgado
date: 2023-02-02
aliases:
  - /chaincode-labs/chaincode-podcast/watchtowers-lightning-privacy/
---
Speaker 0: 00:00:00

I came into Bitcoin because I like peer-to-peer.
I discover more things that I love by doing so.
And again, these are not feelings, but they are feelings related to research.
Sorry, failing time.

Speaker 1: 00:00:12

We're going to make sure our editor takes out The love word.
We are back in the studio.
We are.

Speaker 2: 00:00:24

And today we're going to be joined by Sergi Delgado.

Speaker 1: 00:00:27

Yeah, we're going to talk about Watchtowers.
We're going to talk about some of his prior work.

Speaker 2: 00:00:31

Sergi is a former academic researcher.
He did his PhD and worked as a postdoc for a while, and now he's a Spiral grantee and works on the Eye of Satoshi.

Speaker 1: 00:00:42

Yeah, he's pretty privacy-focused, And it's really interesting to watch a researcher sort of move over and do implementation for now.
I don't know, it's been like three years he's been working on this.
So looking forward to hearing from him.
Hope you enjoy the episode.
So we're going to talk about things you worked on in the past a little bit.
First of all, welcome to the Chaincode office.

Speaker 0: 00:01:06

Thank you.
It's been amazing, but we don't talk about feelings here.

Speaker 1: 00:01:10

You're clearly a dedicated listener if you know that.
Yeah, we're going to talk about TXProbe because I think I saw you speak at Scaling in Tel Aviv.
And I was like, who is this guy?
He's talking about lightning stuff and some really interesting things.
And I looked it up and you had also done the transaction probing for network topology using orphan transactions, which I thought was pretty tricky.
And so,

Speaker 0: 00:01:35

Gaby, that was interesting.

Speaker 1: 00:01:36

Tell us about that project.

Speaker 0: 00:01:38

Gaby, So it started back in 2017, if I remember correctly.
That was the last year of my PhD.
I came to the States for the first time, those are not feelings, those are facts, to work with Andrew Miller, which is a quite renowned researcher for peer-to-peer in Bitcoin.

Speaker 1: 00:01:58

But now doing mostly other stuff.
We've lost him to other kinds of projects.

Speaker 0: 00:02:03

I don't think he has been doing research on peer-to-peer for a long time, but not because he's not interested in it.
It's all about what your PhD candidates are interested in, right?
He was doing all the stuff too, apart from only peer-to-peer.
And I guess in the end, you know, if none of the appliants are interested in peer-to-peer, then you stop doing that.
He's been interested in that.
Like, I just feel like either he doesn't have the time to do it himself, which I'm sure he doesn't, or he hasn't found any PhD applicant here to do it.
Which is kind of like the vibe going on for some years.
I think it was somewhere around 2017, I think, summer 2017, when they were working on the peer-to-peer at that time.

## Mapping Network Topology Research

Speaker 0: 00:02:49

They were known, pretty well known for the Coinscope paper, which was topology inferring using address messages and timing analysis and so on.
And I joined hoping we could do like some network research.
They were working on the TXPROPE paper, I think.
So the whole TXPROPE general idea was already mentioned in the Coinscope paper.
So they already had an idea of how to work on this.
I hear about it.
I loved it.
There was some experiment to do, there was some implementation to do.
So it was put there, theoretically, so it has to be tested.
And I spent, I think, the next four months battling with the testnet, getting results, like getting interference by other researchers that were also doing peer-to-peer stuff, which was like, at the time I didn't know what was going on.
Later on it was like super fun, and we actually had like nice conversations about it.
That's where I met the KIT people from Germany.
That merge came from there, kind of.

Speaker 2: 00:03:55

Yeah, they were a different group.

Speaker 0: 00:03:57

Not the same group, but the same unit, right?
Yeah.
Yeah, I think at the time the two better known groups for peer-to-peer in terms of research were Andrews and them.
Ethan Hillman too, but I think Ethan was not doing peer-to-peer anymore.
I mean he's like super well known for Glypse attacks, of course.
Well, and also Julia for dandelion and stuff.
But it was around that time, you know?
The interesting things were happening in the peer-to-peer.
Not like recently.
Research-wise.

## TxProbe paper  - Andrew Miller  - Coinscope  - Episode on Address Relay with Martin

Speaker 0: 00:04:28

Don't get me wrong.
Now we have aligning and that stuff, you know, and that have like overtaken all the interest of.

Speaker 2: 00:04:35

There was an attempt to map topology last year.

Speaker 0: 00:04:38

Did you see that?
No. I've also been like quite driven out of the whole peer-to-peer.

Speaker 2: 00:04:44

Yeah, We recorded a podcast with Martin a while back and looked into, there was an attack that used fake addresses of nodes to see how that information propagated and it probably could allow you to learn about the node degree.

Speaker 0: 00:05:02

Peter told me about that.
They were like flooding the network with thousands of IP addresses.
Interesting.

Speaker 1: 00:05:09

You did that project, and I thought it was pretty clever in terms of how you used Orvin transactions to fingerprint nodes.
And so you get to the other side of that, the results were pretty striking.
And what happens?
You deliver that.
Maybe talk a little bit about how you let the Bitcoin Core team know a little bit about what was happening, and then mitigation steps, and how the sausage was made there.

Speaker 0: 00:05:35

So, all right, four months passed, right?
We were writing this paper.
We knew we wanted to write a paper about this.
So I went back to Barcelona, which is where I live, And the person I knew about peer-to-peer at the time was Peter, right?
So I didn't know that much about disclosure and stuff like that.
You know, I was young.
So I actually probably disclosed this.
So I actually messaged Peter about it.
It was like, hey Peter, we've been working on this.
We are planning on publishing this at FC, which you know.
I sent a copy of the paper to Peter about like, hey, if there's anything you know that you don't want us to mention, here it is.
We have run this in testnet.
We haven't done anything in mainnet because we didn't want to mess around with the network more than we need.
Some people agree with that, some people didn't.
So yeah, we let them know.
Peter said that some of that was partially known, that they were aware of it, and that they will implement some countermeasures because of it.
Some of the ones that were literally specified in the paper, so For example, how orphan pool eviction was completely broken.
That was like patched straight away.
That and also in-blogging, which was one of the techniques we used.
Those two things were almost immediately patched by Peter before we got a chance of presenting that publicly, which happened like maybe four or five months later.
Years after, or months after, I don't, I'm like completely lost on the timing here.
I've learned some of that actually today, because I remember like seeing a PR later on about adding additional connections to Bitcoin Core, the ones that some of the audience may now know, the two additional ones, the ninth and the tenth outgoing connections.

Speaker 2: 00:07:31

The blocks only connections.

## Block-only connections PR by Suhas

Speaker 0: 00:07:32

Blocks only connections, yeah.
And that was proposed by Suhas, which I knew that someone proposed that, I didn't know it was Suhas.
And that was part of a countermeasure against topology inferring using transaction propagation data.
Because now, you know, some of the information that you may be propagating through the connections on block, sorry, transactions on block connections, like the normal connections, may beat you back in the ass using the block-only relay connections.
So you may not be able to use similar techniques to infer the topology.

Speaker 1: 00:08:05

Yeah, I mean, the genius of that too, of course, is given the combination, you're also saving bandwidth.
Like it's not that much of a, not that much overhead to add blocks only.
So pretty cool.
From there you went on to work on payment probing on Lightning, which is, first of all, it's a layer up, but also, you know, it's sort of the adversarial kind of research that you've been doing.
Like it's a whole new domain.
Like how did you get into that kind of world?

Speaker 0: 00:08:33

I think it was kind of the same approach I used for Bitcoin.
So I came into Bitcoin because I liked peer-to-peer.
I discovered a whole more things that I love by doing so.
And again, these are not feelings, but related to research.
Sorry, filling time.

Speaker 1: 00:08:54

We'll make sure our editor takes out the love word.

Speaker 0: 00:08:58

But I use that as a way of learning how things work.
So for me, being able to work on TXPROBE was kind of like a result of learning how a lot of the things on Bitcoin work, from transaction building to propagation to networking to the in-message, the get-out-of-message, everything that goes in between, right?

## An Empirical Analysis of Privacy in the Lightning Network

Speaker 0: 00:09:18

At some point, when I finished the PhD, I got the opportunity to go to work at UCL, that's where that paper started, with Sarah McGill-John, and they were doing, they were quite focused on privacy, right?
They are pretty well known for some of the chain analysis stuff.
So like some chain analysis actually was built based on one of the papers from Sarah back in 2014, 2015, or I don't even remember anymore.
But they are like quite privacy focused, right?

## Lightning white paper, 2016

Speaker 0: 00:09:45

So for me it was kind of a way of focusing more on privacy, but also about learning how the Lightning Network worked.
I knew generally how it worked.
You know, I've read the paper, I've tried to read the Lightning Network paper, which was kind of a challenge.
I mean, I think that's like well-known, you know, that like the paper was...
Yeah.
So I dig into the balls, I try to like get an understanding of like how everything worked, try to see, okay, is there anything that can be exploited, is there not, like what are the privacy aspects and so on and so forth.
And I think I reach, like give or take the same conclusion that many researchers reach at the time because there were like two or three papers talking give or take about the same stuff in that year.
One from Sergey actually with Rene Auers.
There was one from Jordi, my ex-advisor at Inversona talking about similar stuff.
Mainly like we shouldn't be using Lightning as a privacy layer because it's not.
It's adding some nice privacy features but it's not supposed to provide privacy, right?
It provides some level of privacy, but it shouldn't be seen as a privacy feature.
Lightning at the end of the day is routing.
I mean, it's routing payment, so it's as much as a peer-to-peer network as anything else could be, right?
So, yeah, I think that that was the way, like trying to understand how it works, trying to see if anything doesn't work as supposedly or what are the gaps in between, I guess.

Speaker 1: 00:11:16

And was it the same sort of process?
Like, how did you, did you feel like you needed to disclose this before it was published?
Did you get in touch with the early implementations to have a discussion about it?
Well, how is it the same or different than working with Bitcoin?

Speaker 0: 00:11:30

This was different, right?
Not because it was Lightning or Bitcoin, but because I was the postdoc at that time and there were like PhD students also working on this, right?
So I was more of the guy saying, hey, there's this, I think there's issues here, here and here.
I think we can do that and that and that.
And there was a lot of heavy lifting.
Most of the heavy lifting, don't get me wrong, done by the PhD students.
They got in touch with some of the implementations.
They disclosed some of this information.
They actually gather a lot of data from merchants or big nodes because there's plenty of stuff being done in that paper.
It's not just like routing.
It's not just using routing information to try to disclose stuff or probing, which My main part was probing, right?
But there was also analysis on invoice data or on chain data to see if, like, you could use the chain addresses, or you could build, like, a Peel chain of public channels and private channels to link a private channel to a public channel, or to know something that looks like a channel, maybe an actual channel.
So again, it was called empirical analysis on privacy in the Lightning Network.
It was not just about probing.
But They did most of the disclosure instead of me.

Speaker 1: 00:12:47

And just for our listeners, so that they have a better understanding, there's sort of the balanced discovery piece, which is, if you're interested in that, you should listen to Sergei's episode because we talk about it in a fair bit of detail.
There's payment discovery and there's path discovery.
So of those three, have you kept up with what's fixed, what's not fixed, like what's the state of things?
What's your general attitude towards where lightning is compared to when you looked at it more deeply?

Speaker 0: 00:13:15

I think it hasn't changed much, but because we were building on the fundamentals of how Lightning is built, right?
The whole balance, the whole trying to infer the balances on channels is built on top of channel probing, which it's something that you can do by default in Lightning because you don't pay for sending payments, right?

## Security and Privacy of Lightning Network Payments with Uncertain Channel Balances

Speaker 0: 00:13:38

So like failed payments doesn't pay anything.
And there's been some research done on that, like Clara and Sergey has done some research into how to mitigate that.

## Channel Jamming paper

Speaker 0: 00:13:50

That also relates to channel jamming.
I mean, it's like, feels like every single problem related to how to abuse the resources in the Lightning Network relate to the same thing, which is, I can route a payment from A to B without having to pay anything from routing the payment from A to B, as long as B doesn't get paid.
So it's also exploited for sending ephemeral data from A to B.
You can use this for multiple things.

## Should we pay for failed payments?

Speaker 0: 00:14:18

It gets back to the point where all the debate about should we be paying for data relay inside the Lightning Network even if a payment hasn't succeeded or not.
What do you think?
I think we should.
I really think we should, because otherwise, if we don't, then anyone can exploit it.
It's all about waiting until someone coming around and saying, oh, I've built this data transmitting protocol built on top of Lightning that it's using failed HCLCs to send data from H2B in a peer-to-peer way, peer-to-peer encrypted way.
No one is using it?
Well, some of them are using it,

Speaker 2: 00:14:57

because Sphinx works in that way, right?

Speaker 0: 00:15:00

So there are already applications that work in that way.
It just feels like no one has bloated the network with it.
But you can, you definitely can.
It's there to be used.

Speaker 1: 00:15:08

We just need a Satoshi's dice to make it useful.

Speaker 0: 00:15:13

Well, you just need something that incentivizes people to make money out of it and then you're screwed.

Speaker 2: 00:15:17

Paul Friedman Or, I don't know, if someone put Nostr on the Lightning Network or something, another relay, like some application that gets a ton of adoption very quickly, Then very quickly I think we would see...

Speaker 0: 00:15:31

There are other things that also apply to this.
And again, they are fundamental from Lightning that can be exploited and doesn't look like there has been much fixed on it.
And correct me if I'm wrong, if I am and someone listens to it, and I'm being me and say, hey, you're super wrong about it.

## HTLC withholding vs. HTLC hodling

Speaker 0: 00:15:48

But HCLC withholding, it's another thing that can make a huge disruption.

Speaker 2: 00:15:53

We're exploiting something that is a basic function of the Lightning Network and maybe considered a strength in other regards for, well, dosing or spamming.
And therefore it's hard to mitigate because you have to distinguish between the two ways of how it's getting used.

Speaker 0: 00:16:10

And normally you cannot because there's the privacy bidding where it's built in the way that you shouldn't be able to do it.
And I mean, There are applications which use HCC hodling for that.
And it's like, there's applications being built with that, but that's a problem.
That's taking some of your opportunity cost for that to be used for routing or for whatever you're supposed to.

## Is Lightning flawed when it comes to privacy?

Speaker 1: 00:16:31

And so is just, is Lightning just fundamentally flawed and we should give up?
Like what's the?

Speaker 0: 00:16:35

No, I don't think so.
I don't think so.
I just think that it's built on these assumptions and it's been, I don't know if we should say it's built on these limitations, but that's how it's built because it's not focusing for this, It's focusing for kind of, I mean, it's giving some privacy.
And the fact that you're giving privacy means that there's a lot of these things that you cannot, let's actually put it into proper words.
So if I know that you're trying to attack me and I know exactly who you are, I just ban you and we don't interact anymore, right?
But if I don't know who you are and then you're trying to like exhaust my resources, I cannot just like say, hey, I'm not going to connect to you anymore.
I may not connect to your node anymore, but you create another like ephemeral ID and then you connect to me again.
If I know you by IP, you create another IP and then I don't know you anymore.
When things try to provide privacy, they're normally way harder to work with because you're adding some benefits to the user that can also be exploited by attackers.
And the fact that there's privacy there means that you don't know if I'm an attacker or I'm an honest user.
So as long as I'm exploiting the normal behavior of the network, there's not much you can do in that sense.

## Watchtowers

Speaker 0: 00:17:43

If you do, then it means that you have to like start front-charging or making the user do something.

Speaker 1: 00:17:51

Reputation-based stuff, too.

Speaker 0: 00:17:53

For example.
That's something that already exists in Lightning, for fail payments in some implementation, at least.

Speaker 1: 00:18:00

Let's transition a little bit.
We've been talking about your research and your prior work and haven't delved too much into what you're doing these days.
But I find Watchtowers, which is your current project and has been really your focus for the last three or so years.
It's one of those projects where Bitcoin talk forums you can dig up early comments about this It's been around forever kind of thing and yet no one's done it So you have essentially locked yourself in a room for three years to actually do it.
You're saying and and so Yeah, what is it?
I guess, you know, you have prior experience doing this collab, sort of collaborative research kind of thing.
And then you went off and embarked in this particular project.
Like why stick with this so long?
Like why?
I guess we can talk about usage soon, but is it the time even right for watchtowers in terms of the maturity of lightning and its needs?

Speaker 0: 00:18:58

So my train of thought at the time, when we're going back to 2019, was that I would rather be soon than late with this, because it's something that it's fundamental for Lightning.
It's like literally described in the Lightning paper, and it was discussed in 2016.
I mean, by touch at the beginning, and then some more people pick it up.
There's been multiple implementations of it, so it's not like I'm the first one with it.
I've never tried to claim, hey, this is something I've done.

Speaker 1: 00:19:28

Who else has done it before you?

Speaker 0: 00:19:29

Lightning was doing it, Lightning Labs was doing it at the time I started doing research on this.
So I think their release came like a couple of months or maybe three months after we started working on this.
And I picked a lot up from their work.
The first one I know of was Bitcoin Lightning Wallet, which was an Android-only Bitcoin Lightning Wallet, which was using a custom implementation of Watchtowers for their users, only for them, and using like, Xiaomi tokens or Bury tokens to do the whole registration, like how do you pay for the tower and so on and so forth.
So that's the same debt for simple Bitcoin wallet and the same for the Obi-Wan thingy and the same.
It's That guy, I don't know his name, but he was working also with the ZBD guys.
I think he's either Russian or Ukrainian.
He was also like kind of like hit by the war thing, so kind of like that and stuff.
I haven't heard from him in quite a long time.
But he was the first, at least the first I know.
And Lightning was the second.
Electrum was also working on that.
When I started working on this, I didn't try to be, okay, I'm going to just make another implementation.
My goal with this was, let's not make 15 implementations of this, let's try to get together, agree on something that, agree on how watch hours should be, you know?
We have like the explanation from Tadge about how they could work.
We are building the exact same thing, like replicated three or four times.
Why don't we get together, write a bolt or what could have been a bleep later or whatever kind of like standardization of this and make it work for any implementation, you know?
It's like if Lightning Labs builds it and CLion can use it, that's great.
If you want to use it with this beacon lining wallet or Electrum wants to use it, or Eclair wants to use it, whatever.
That's how it's supposed to be.
It's part of the infrastructure of lining.
It shouldn't be implementation specific.
So that was my main goal.
Actually, my main goal was going beyond lining.
This works for any layer two solution.
So vaults also work, channel backups also work, ephemeral data backup, like any kind of two-step protocol works for WhatsApp.
So, it was a cool research project and a cool way of like getting also involved with with lightning, I guess.

## Python PoC

Speaker 0: 00:21:49

I mean, I came from research, right?
So my timing or my way of assessing how long something would take was not the best in terms of implementation.
So what was supposed to be a six-month project ended up being a six-month POC.
And then I tried to pursue it.
So I got in touch with the Spiral guys, Square, Crypto at the time, now Spiral.
I got a grant to work on watch hours from research to implementation and we ended up building the client for C-Lining around 2020.
All that was Python so at that time it was like okay we are reinventing a lot of the stuff.
The support for Bitcoin in Python could be better.
I mean, the only mature and good project, let's say, or robust project I know that builds on Python in Bitcoin is Electrum.
There's no good tooling.

Speaker 1: 00:22:48

Not that they don't have their own problems though.

Speaker 0: 00:22:51

It makes sense.
After spending more than one year building on that, I can definitely know why.
It's good for some things, it's not good for others.
Especially if you don't have a good community around the language you're using, which is the case, then it means that you're going to have to build and maintain a lot of the stuff yourself.
And that's not ideal.
It's far from ideal.

Speaker 1: 00:23:12

And why?
It's not that you don't have a good community.
I mean, everybody writes Python.

Speaker 0: 00:23:16

Yeah, but not good Python.
I mean, don't get me wrong, it's like, you build something for one specific reason, you just don't maintain it, you don't update it.
It may not even be generally enough for someone else to use it.
It's a toy project.
And for me, when I started thinking about adding lightning functionality to the watchtower, then I realized that it was an existence.
Like the best thing you could get was the testing and kind of developing libraries from C-Lightning, which had some functionality, but not all the functionality, right?
So it came to the thing of either doing it myself, so like implementing part of the bolts myself, which I started doing.
I saw that that was going to take years, so it was definitely worth it, not just because of the time, but also because of the maintaining, right?
Just like if I'm building something that is getting updated frequently, then at some point I'm going to have to like update all the dependencies I'm supporting, and it's not going to work.
Like This is going to grow way too much, and I'm not going to have time for everything, right?

## Building on LDK

Speaker 0: 00:24:19

So my second thought was, okay, there's LDK, and they are working on bindings.
It was like the beginning of them working on bindings.
So I think the Java bindings may have been there already.
The C bindings were definitely there.
So I spent some time building bindings for Rust to Python.
I think that was like a three, four month period.
One of the worst periods of my life.
I'm not kidding.
I knew nothing about Rust at the time.

## Transition to rust

Speaker 0: 00:24:44

So I thought, you know what, let's stick to Python but let's use something that it has a good chunk of devs behind it and they can like update it and so on and so forth.
Issue, there's no automatic proper automatic way of building bindings for Python to rust.
So it means that if you're developing faster than me, I have the exact same problem.
Plus, I'm building in a language I don't know anything about.
So after that, it came to whether I wanted to again do everything myself or switch to something more robust with more community support and so on.
So I decided to reimplement the whole thing in Rust, and that took some time, mainly because I didn't know any Rust.
But the investment seemed worth it.
It was like, If I can learn Rust and do it, then, I mean, it may take me the same time to learn Rust well enough to reimplement it, that to implement everything that I need in Python and then maintain it.
So I went for the Rust route, and that's why the code base was reimplemented in Rust, was actually improved.
A lot of the design was simplified because I didn't have to do everything myself.
So LDK was already doing a lot of the heavy lifting.
So real logic was already covered.
Part of the components were completely gone.
There's components I don't even remember.
Now there's three or four components in the code.
There's components I don't even remember.
There was a time where I was building something called the Librarian for Python, which was supposed to be an actor on the tower.
I mean, I started like calling everything in the tower funny names, you know, like the gatekeeper, the librarian, the watcher, the blah blah, you know, because it was kind of like a court and they had to do stuff.
I had to have fun too, you know, like building this stuff.
So...

Speaker 2: 00:26:30

Too much feelings, sorry.

Speaker 0: 00:26:32

No, they didn't actually get along, but anyway.
So the librarian was supposed to deal with history, you know, blocks and reorgs and stuff like that.
And I built that myself and then he was like, there's no need for this anymore.
Like, let's get rid of this thing.
Like, it's way too complex.
And like BitcoinD and LDK already do that for you.
So like, why would you be doing that too?
I realized that there was a lot of, what's the word for this?
Like, bad inheritance, I'd say.
Or things that came from like the Python mindset that then were way simplified.
For example, one of the things we recently introduced to the IOS Satoshi after talking to many people about it, like including Antoine, Dribbble Antoine, and Simon Ruth, was transaction indexing within the tower.
We used to build the IOS Satoshi on top of Bitcoin D with transaction indexing, meaning that we needed around 450 gigabytes of data to deploy a fresh tower.
Now we need 5.5, because we only care about the last 100 blocks.
That was something that initially, that's how things change.
We assume that there's order and storage in the tower because we don't have L2.
So it was like, if you have order and storage, have an archival node, that's not going to be an issue.
And it's not, in the end you're going to probably have more than that, but you don't have to start with that.
I've been running a tower for months now, and I didn't even have a gig of like tower data with multiple users connected.
So, I guess you learn things.

Speaker 1: 00:28:08

Yeah, tell me more about your current status in terms of having users actually use the software and Have you actually caught any breaches?
Is it doing its job?

Speaker 0: 00:28:18

Well, I mean, mine is.
It hasn't caught any breaches.
That doesn't mean it's not doing its job.
So MyTower specifically hasn't caught any.
I think it right now has something around 20 users, 20 clients.
I think the pivoting point from people running it or not running it was actually doing the no transaction indexing thing.
Because that meant that people could run this on a Raspberry Pi that they already had without having to have any additional disk requirements, storage requirements.
The code is not that CPU intensive, especially after switching to Rust.
So you can run that at home and offer that to your peers or whatever.
And that was always the idea, but it felt like people were not doing it.
Well, first, mainly because installing like Python stuff, like running all these things in Python was like way more complicated.
So like switching to Rust definitely helped.
And then minimizing the or reducing the entry barrier for what you need really helped.
So right now that I know of, there's at least eight or nine people running this because we have like a list of altruistic towers in the repo that people can connect to.
There were some users before, so I knew at least about two tower operators.
I don't know what they were doing.
There's the guys at Embassy these days, which is a Node in a Box project, that are integrating the EOS Satoshi.
I got in touch with them during BTC++ in Mexico last year, like in December last year.
They were at the presentation for the iOS Satoshi.
They were like, we love this, we're going to integrate it.
And actually they pinged me a couple of days ago because of this.
There's also the guys at Voltage, which pinged me about it, I think it was like mid last year or something like that, about offering this as a service for their users.
They haven't yet, I know that they've been swamped with work, but they really want to do it, so I'm guessing they will at some point this year.

## Altruistic towers vs professional services

Speaker 2: 00:30:20

So, so far, this is all altruistic towers.
So people running it without any expectation of profit.
You said that your tower implementation currently needs like 5.5 gigabytes, And then of course, for each new commitment transaction in the channel, you need to have a new appointment, a new backup package that you keep and that just keeps growing,

Speaker 0: 00:30:46

right?
So. That's around 720 bytes per payment, if I remember correctly.
And I'm saying I'm saying this from the top of my mind, it may be a little bit less.
Let's say around.

Speaker 2: 00:30:58

Yeah.
Okay.
So a little less than a kilobyte per channel update, I should say, so either an HTLC or a fee update in the channel.

Speaker 0: 00:31:08

Carlos Bustamante So if you think about payments, by the way, and that's something that is quite misunderstood generally, there's two appointments per payment.
Because normally you add an HCLC and you fulfill that HCLC, meaning that for every single payment you do, you're going to have to update the tower twice.
So yeah, it's for every single channel update.

Speaker 2: 00:31:26

Rimas So even all these people that you just talked about, embassy, voltage, and so forth, they're looking into the altruistic tower or are they trying to make a product from this?

Speaker 0: 00:31:37

I really don't know.
That's the cool thing about open source, you know?
The code is there, you can do it in the way you want.
The design allows for paying for the service.
So every single user registers with the tower and is given a time period, a subscription period, and some slots within that period.
And that's given for free in the current implementation.
But the only thing you have to do in order to make people pay for that is building a paywall between that endpoint.
You know, it's like, in order to like register to a tower, you have to like pay this HLC or this invoice or this whatever, right?
So the design is completely compatible with making you pay for what you're using.
Whether people are gonna pay for it, if there's people offering also for free.
At this stage, I don't know.
I think there's a lot to be talked about, the incentives and the revenue expectation and how you price all this stuff, which is something I haven't done, to be honest.
I'm building it so you can pick how you want to do it, and I think there's people who are way more into the economical aspect than me that can do a way better job than I could do.
But it's compatible.

Speaker 2: 00:32:44

Also, probably just a question of the volume as more and more people look to have their channels back up to watchtowers or employ a watchtower to watch their channels for them eventually the freemium model will go away because there will be just too much data to keep in store that people will not want to provide that for free, right?

Speaker 0: 00:33:05

Yeah, it would make sense.

Speaker 2: 00:33:07

So basically all the paths are laid already for people to transition just to professional services.

Speaker 0: 00:33:15

And the DOS protection things are also in place because there's a lot of things that can go wrong, especially when you are offering this for free.
I mean, if you're offering it for free, you know that you have DOS at vector open.
And that's something that the user should know.
I mean, if you don't, you know now.

Speaker 1: 00:33:31

Jeff Deist Yeah, it's just a file.
You can also just make it like a file sharing service.
You just have you store all my stuff.

Speaker 0: 00:33:38

Carlos Gonzalez-Ramon You could actually, it's built in a way where you can do that because not all the watch hour implementations allow for this, but you can retrieve the data that you have sent to the AOS Satoshi.
So I can send you encrypted backups of something and then I can retrieve them later on.
As long as I have the encryption key, I have a free backup system.
So the AOS Satoshi allows this by design because it's not meant only to be used for lining.
It was kind of like a general-purpose watchtower that ended up being implemented first for lining because it was like the best fit.

## More privacy considerations in Lightning

Speaker 1: 00:34:11

And what kind of privacy considerations did you think about as you were building this out and sort of thinking about the trade-offs?

Speaker 0: 00:34:17

Ruiz So the design has user privacy in mind, to the highest extent I think it could.
As I was mentioning, there's some registration and some subscription model built in, but that's being built using a few more keys for the user.
So the user mainly creates a key pair for Sec6AP256K1, so like the Bitcoin curb, and uses the private key of that, sorry, the public key of that as an identifier with the tower, and the private key to sign messages with the tower.
So it's like I identify, so I send you like signed messages so you can like identify me and I use the public part to say it's me to register for you to be able to like verify my signatures, right?
But that doesn't have to do anything with the node ID, the channel ID, whoever is sending you data.
It's just something you create in the same way you may create a Bitcoin address and use that as an identifier.
Right now the tower is being offered using two different endpoints.
One is a HTTP slash HTTPS interface, so that's kind of like if you want to use GlueNet, but we also offer a Tor interface.
So By using Tor and not linking your ID to anything related to you, you could decouple your node and your channels from your Tower client identifier.
That's on one place.
On the other place, the Tower doesn't know anything about node IDs. Again, first because the user is identified using a different identifier.
It doesn't know anything about channel IDs. So all the information being shared between clients and towers is done under this subscription umbrella with ephemeral IDs and there's no distinction between different channels so like all the data goes in the same direction.
If you're reusing the exact same key for different nodes you can just like you dump that and you import it in another node.
The tower doesn't have any way of telling.
Well, it may if you're using ClearNet, because it may be able to see that you're sending that using two different IPs, but if you're using Tor, then there's no way.
There's also a PR in there for using lining as a communication channel.
Lining peer-to-peer, not lining as in what we were referring to before.
I'm using Lightning for this, but like connecting at the Lightning Peer-to-Peer level using ephemeral IDs and then sending that kind of information.
That's what LND does, for example.
We went for HTTP first because it felt like an easier way for people to integrate instead of having to implement the noise protocol and so on.
But there's a PR building on top of LDK too.
That's one of the reasons why we switched to trust.

Speaker 2: 00:37:02

Paul Audio So you're saying that the watchtowers are going to be bona fide members of the Lightning Network communication?
And they could.
Going to speak to Lightning Protocol?

Speaker 0: 00:37:12

Carlos Ancelo They are.
They have been for years because LND has been doing it in that way.
I'm just saying that you choose your communication channel.
You can use whatever you want at the end of the day.

Speaker 1: 00:37:23

Maybe we cut this bit, but if you're constantly getting fed data and you're also a member of the communication channels and you can do things like balance discovery, path discovery, payment discovery, combining that with your like sitting on a wealth of data.
I mean, are there serious concerns about these watchtowers becoming all seeing?
Like It's in your logo, so.

Speaker 0: 00:37:51

Non-negligible, let's say.
Yeah.
I think they are a part of the network.
They could be different actors in the network.
So you could be offering this and also be a node.
And that may give you a stronger position than other nodes.
I'm just going to highlight something that I think is quite viable, but people may not know.
So I could have a channel open with my node and I could be offering a watch hour service, like those are the couples, you don't know about them.
And I may know that you're actually the one sending me the information because you're using the identifiers that relate to the commitment transactions that are being revoked in the same channel that I am.
So I may know that you are actually backing up the information with me.
I don't know if you're using any other watchtower.
So, like, if I assume that, you know, you're using my tower as your protection service, and you are connected to me, and I know that you may be offline because, you know, I'm not being able to...

Speaker 1: 00:38:45

Hey, I might roll the dice.
But beyond that, I'm also identifying myself with how related transactions, aren't I?

Speaker 0: 00:38:52

Well, but if I'm already connected to you, I already, oh, you mean from other channels, not for the ones, yeah.
Yeah, well, you may be telling the tower how often you're receiving payments.
I can roll out the frequency of my own channel.
I may know other channels you have open because I know your node ID.
I may know about your private channels.

Speaker 2: 00:39:12

So I would still not be able to tie the commitment transaction IDs to the other channels.

Speaker 0: 00:39:17

You may not be able to know where they come from.
You may be able to know the frequency that nodes are receiving payments, not from where.

Speaker 2: 00:39:23

You wouldn't even be able to know whether it's the same node or another node, right?
It could be a second node that your channel partner's running.

Speaker 0: 00:39:30

We could be sharing the same subscription.
I mean, theoretically, a lot of those things can happen.
So like Merge and Me can just like pay for one subscription and use the same key to sign and send that information to the tower.

Speaker 1: 00:39:40

Yeah, I understand there's probably some, you know, there's maybe not certainty in a lot of these things, but there's probably some useful heuristics you'd be picking up.
And for the Umbrella user running on a Raspberry Pi in their home, you can make some pretty solid assumptions.

Speaker 0: 00:39:57

I do agree.
I think, I'm not going to be wrong, this is an under-researched area.
Not many people have put the time to invest the years into researching what's ours.
It's complicated, and it's complicated I think for the good reasons.
You're trying to build something that is super privacy aware for the user, meaning that you open yourself to a ton of DOS attack vectors, and then you're providing a service for the user to not be online.
You're like, okay, you're here, you have all the information, I may help you, but you're giving me some data, right?
That data is encrypted, and I may not be able to know anything about the data, but I can know everything about the metadata of the data you're sending me, like frequency, where it comes from.
I can use that with other lining or on-chain data to try to triangulate stuff.
I think the minute you start sharing something with someone else, you open yourself to metadata analysis for sure.

Speaker 2: 00:40:56

Paul Audio So you're saying you're not going to be surprised if the IOP Satoshi is going to get run by blockchain analytics companies and offered as a service.
Probably that's where the free watchtowers will come from.

Speaker 0: 00:41:09

Carlos Bustamante No, no, I thought about that, of course.
In the same way that routing nodes could be run by chain analytic companies and like offer low fee channels so you end up running through them and they may end up like learning or potentially learning something about you.

Speaker 1: 00:41:25

Well if Async and LN Big you know spin up theirs then It gives them a pretty nice competitive advantage.

Speaker 2: 00:41:32

That's assuming that LN Big is not chain analysis.

Speaker 0: 00:41:37

Or it's not selling your data.
Just kidding.
I'm not saying they are.
I'm just saying that the moment you are a big actor in a network, it gives you the potential of doing nasty stuff.
And that's one of the reasons why you should design.

Speaker 1: 00:41:50

It becomes very interesting in this hub-and-spoke topology that's continuing to cement itself.

Speaker 0: 00:41:56

That's why I think the protocol itself has to maximize for privacy.
That's what we've tried to do with towers.
If I cannot do it, it's not like I'm not going to do it.
It's like I should not be able to do it.
And as long as I'm not able to do it, then I minimize the attack surface of what I can do.
That's why all the information is encrypted, that's why we don't keep like much information about users, or we use like ephemeral IDs. That's where all that came from.

Speaker 1: 00:42:23

You mentioned earlier that you don't know if you'd be using other towers.
So there's a couple ways that professional towers might be compensated.
One is through the subscription models and you pay a SAT through every state update or the other one is through a bounty or maybe there's the combination of the two of them.
But it becomes very interesting as someone who doesn't run a tower.
Like as a user, it becomes very interesting if you are sending data to multiple bounty hunters and then something happens and they have to fight over who claims the bounty, you would imagine there would be some pretty weird network behavior of those towers trying to one-up each other to claim that.

Speaker 0: 00:43:06

Raul-
Yeah, you start getting to CPFBs fights.

Speaker 2: 00:43:10

Paul-
So does this get better with RBF?

Speaker 0: 00:43:12

Raul- You cannot do RBF.
I mean, the tower cannot do RBF.

Speaker 2: 00:43:16

Paul-
With full RBF.
So in order to have multiple watchtowers that watch for you that each could collect a bounty they must have different penalty transactions which I think penalty transactions should always be marked with RBF enabled but...

Speaker 0: 00:43:34

Yes, but the tower can spend from it, it cannot...

Speaker 2: 00:43:38

It cannot update the penalty transaction itself but a child inherits the RBF quality from its parent and I think that a second package would be able to replace the first.
Okay, maybe not.

Speaker 0: 00:43:54

I don't know that much about that.

Speaker 2: 00:43:58

Anyway, so unaffected basically, nevermind.

## Monitoring and reacting paradigm

Speaker 0: 00:44:01

But what I've learned to, what I've grown to learn with this is that even though we've all ended up designing the same approach for towers, which is non-custodial, third party, not trusted, watch hour, right?
So like try to minimize all of that stuff and try to react in our switch or in no no no no instead of the user in either to work for that I don't remember well when I when I act on your own behalf of the user on behalf of the user sorry it didn't come up I've learned to realize that that may not be the best solution in terms of storage, in terms of mempool, in terms of...
Reliability is fine, but you don't want people to fight over this kind of stuff.
So some time ago, I thought about designing this in a different way.
So I had weighing up my plate with the current approach to just start something different.
But I like to describe this in a way that A watchtower is doing two things, and that's why the bounty plus the subscription approach makes sense.
A tower can fail in doing two things.
One is the tower cannot be watching for whatever it's supposed to be watching, and then if it's not watching for what it's supposed to be watching, then there's nothing further, right?
Or a tower could be watching for channel breaches and something like that, but do nothing with them, right?
So there's normally two actions or two jobs that a tower does.
One is the watching part and the other one is the reaction part.
And the whole heavy lifting, the whole issue, everything that makes towers complicated is on the reacting part and not on the watching part.
The watching part is pretty easy.
The watching part doesn't require, it does require order and storage potentially, but it's at a way lower, so it's still linear, but smaller in the linear size.
You can just be storing identified instead of identifies plus penalty transactions if you're not going to react.
So if you split this into two, like the watching and the reaction part.
You can actually design simpler towers that are not as powerful in this sense, so like may require the user to do stuff, but you're not like super replicating the data that the user already has.
So like the best place for the replication data to be at is at the node's control, right?
And what the tower is doing is trying to have that data and reacting when the node is not there.
But we have solutions in place for the node being able to be out for some time, right?
It's not like if you're not there for like an hour, your channel is going to be closed and then you're going to be screwed.
Normally there's like in the order of days, if not weeks, for you to react.
And that's a range and we can talk about it and we can see like how this could be like maybe optimized.
But we know that we are never going to go below a threshold because if we do then like statically we are putting the node in danger, right?

Speaker 2: 00:46:55

So you're saying just watch and send an email?

Speaker 0: 00:46:58

For example, I mean that could be a solution but yeah that's mainly what I'm saying.
You could watch and notify either the tower, the node admin or the application or whatever about, hey, you know, your channel is in danger.
And If you just come back online, you're going to be able to do whatever you're supposed to do.

Speaker 1: 00:47:19

Maybe send a letter because there are probably already offline, right?
Like,

Speaker 0: 00:47:23

well, it's not like that, honestly, because the placing where WhatsApp makes more sense is for mobile wallets, Because those are the ones that are normally not online all the time.
But they are not online all the time, not because the phone is not online all the time, which it is, but because the app is offline.
Like, if your node is always online, if you have like a beefy setup, if you have like the most robust fail-safe setup, A tower is not useful for you, not much useful for you.
It's useful when you're actually on the other side of the spectrum, you know, you're using something that is not connected all the time, or because of like OS limitations, your app is not on all the time, or cannot like be checking this kind of stuff all the time.
So for mobile wallets, it makes the most sense.
And they are all, not always, but potentially always online.
You know, they are on your pocket.
You can open it up and react about that easily.
But they don't allow chain monitoring or blockchain monitoring because you cannot have a background.

Speaker 2: 00:48:19

They don't run in the background.

Speaker 0: 00:48:21

What I wanted to go into by the way with this approach is that normally what makes towers different from different protocols is the reacting part, not the notification part.
So if you split that, you can use this.
I mean, you can use this for multiple projects already, but even in a simpler way.
Again, the whole heavy lifting comes from the reacting part.
And that logic is better built in nodes because they can resign, they can re-agree on stuff, they have all the keys, they can do all the stuff.
Even with this kind of approach you can build something like I share some of the keys with the tower because I'm only running that tower for myself And then now the tower doesn't have to notify me.
Now the tower actually has sign potential.
So I'm splitting like the watching with this part.
And for me, the tower has like propagation key material so it can like sign some of the stuff.
It could be an email, it could be a telegram message, it could be an Oster message, it could be whatever.
So, again, it's not as powerful, but towers are crippled anyway.
It's like the true power is in the node side, and we are assuming that the node is not going to be there but if we find like a proper compromise with the to self delay to make it long enough so you can like come back but not too long as it is right now so if you get a non cooperative node then you have to wait for two weeks to recover your funds.
I know that's something that has been around my mind for more than a year.
I've never worked on it, but I think that that could be a better solution or a more useful or used solution than what we have right now.

Speaker 1: 00:50:01

Another thing you've mentioned a couple times is storage.
And one of the things on the horizon, of course, is L2.

## Storage and Eltoo

Speaker 1: 00:50:06

So how does that, is that something you're really hoping for in terms of helping with adoption?
I mean, I've seen that cited as one of the more useful gains from doing L2 is the storage component.
So what do you take?

Speaker 2: 00:50:23

Not just for watchtowers, but...

Speaker 1: 00:50:25

Of course, for the nodes themselves.
But I mean, obviously with the amount of data that you're going to have to be plugging somewhere.
This helps.

Speaker 0: 00:50:33

Jorge Carrasco For towers, it's tricky, actually.
Because people tend to think that the storage will be 01, because the only thing you have to store is the last update.
And that's not true.
So it could be true, but then you have privacy leaks.
And that's something I used to think too, because that's what it's normally known, let's say, across the community.
But ZMN actually taught me better.
He's like the privacy guy for this kind of stuff.
He has also been thinking about watchtowers, apart from privacy.
I think he actually has a few mails in the mailing list dating back from 2016, maybe 2017, talking about watchtowers, talking about how to...
I'm going to refer to the presentation I was doing before, but how the whole like identifier overriding attack works, all those things that like I ended up like learning by doing this stuff, Then I learned that he had done that way before me.
So at some point, we started a really nice conversation about Towers on how he thinks things should be done with privacy really in mind, because he's always a privacy-aware guy.
Well, anyway, L2 specifics.
So it turns out that if you send the WhatsApp hour only the last update and you keep updating the last update, that's all one of course, but you're telling the WhatsApp hour what your node ID is and not your channel ID is.
Because if you don't, then it cannot update the last update.
So it's like, if you need an endpoint, if your trigger is consuming this transaction ID, and what I have to use for consuming that transaction ID is this last update.
I have to identify the transaction ID, the funding transaction ID.
If I don't want it to be like that, I want it to be in the same way that it is right now with locators and stuff like that, it means that the tower shouldn't be able to link one commitment to another commitment.
So it's going to be ordered in storage anyway.
Again, it's not going to grow as fast.

Speaker 2: 00:52:40

I mean, you could still send a delete request, just not exactly at the same time when you send a new storage request?

Speaker 0: 00:52:47

You could, but then the tower knows the frequency of your payments.

Speaker 2: 00:52:52

Of your channel updates.

Speaker 1: 00:52:53

And a delete request doesn't mean it's actually deleted, it just means you could maybe open up slots or something on your account.

## Professional tower revenue models - subscription vs. bounties

Speaker 2: 00:53:00

Yeah, talking about the subscription model, where I think we haven't actually mentioned this in the podcast yet, but you would purchase a number of slots and for some amount of time, By deleting some of your appointments, the backups of channel state, you would open up slots again.
Sure, whether or not Watchtower actually deletes the stuff is their business, but you would notice if they don't give you back your slots.
So you could still have five new updates and then delete three an hour later or something and basically have them on random delays, all of the things.

Speaker 0: 00:53:45

It will reduce significantly the amount of storage that the watchtower needs.
Again, like two dozens of bytes per update instead of like hundreds of bytes per update.
Because it's like last update number, let's say, with the ID.
Either that ID is reused or not.
So it could be O1, if with a little privacy leak, it could be ONN for small updates.

Speaker 2: 00:54:07

I mean they would still not know your channel until there is a breach.
They would just know that they belong to the same package.

Speaker 0: 00:54:15

They may know your payment frequency though.
Even if you're like delaying that, they may know like how many payments you have received because you're sending them unopted for everyone.

Speaker 2: 00:54:23

Or at least the number of times that you request an appointment.

Speaker 0: 00:54:27

Yeah.
That's also true because that's something that we haven't mentioned.
But you could always add junk here from the user side.
It's like, okay, I want to obfuscate this a little bit more.
Since the tower doesn't know anything about this, if you're not overwriting the data you're sending, you can just every now and then pop up some random junk that it's going to consume some of your slots, but it's going to make the tower potential analysis be screwed.

Speaker 2: 00:54:54

And also, so the new appointment should happen every time the commitment transaction in the channel is updated, which also happens when the fee rates are updated.
When you add an HTLC, when you remove an HTLC, you can batch that, you can add multiple HTLCs at the same time in parallel.
For example, if there's an EMP payment.

Speaker 0: 00:55:15

That's trade-off though, because if you queue kind of like your updates to the tower, which you can, it means that if your node breaks at some point before you send those to the tower, then you're not covered for that.

Speaker 2: 00:55:27

Sure, but with L2 especially,
grouping it would be much cleaner, because for the LM penalty, you would actually need every single state for the watchtower because your counterparty could use any old state.
But with L2 you only, like You could stagger it out, you could subscribe to three watchtowers and only give each one third and you'd always be covered but none of them would see your whole frequency.
That's also true.
So L2 would make privacy and storage much better.

Speaker 1: 00:55:57

Ooh, but that becomes very interesting when there's a breach and They all try to grab it.

Speaker 2: 00:56:02

Oh, that's fine.
They can overwrite each other.

Speaker 0: 00:56:04

They actually cannot overwrite.
Well, that's what I wanted to say.

Speaker 1: 00:56:07

They can't overwrite each other.

Speaker 2: 00:56:07

They can't.

Speaker 0: 00:56:08

Well, they will overwrite each other, but up to a point in where one wins, right?

Speaker 2: 00:56:12

If you do it roulette style, it's whoever.
Only one of them can overwrite the others.
Two of them can overwrite the third.

Speaker 1: 00:56:19

Some very angry towers out there.

Speaker 2: 00:56:22

Wait, they would still get the bounty, because their transaction gets into the blockchain, and then the output of the transaction is spent.
So you would pay three bounties.

Speaker 0: 00:56:32

Would you?

Speaker 2: 00:56:32

I think so.

Speaker 0: 00:56:34

It's it's replaced, isn't it?

Speaker 2: 00:56:35

I think it's not replaced, you can spend a previous.
So there's a trigger transaction.

Speaker 0: 00:56:41

But as long as it is a mempool, not in blockchain.

Speaker 2: 00:56:43

Oh, in the mempool, yes, in the mempool, it would get replaced.
But I guess a miner would not necessarily need to include the newest or the one with the highest.

Speaker 0: 00:56:52

That's true, of course.

Speaker 2: 00:56:53

They could even include all three of them in the correct order.

Speaker 0: 00:56:56

Does that work though?
Because I mean, my understanding of L2 is not that wide, but I thought only the later one would be included.
So like, they are spending from the same point.

Speaker 2: 00:57:09

No, so any PrevOut links to any UTXO that has the same script pubkey and the same amount.

Speaker 0: 00:57:17

Oh, you mean that they will be linking one to the previous?

Speaker 2: 00:57:20

So the miner could actually collect all three transactions, as long as they order them in the right order.

Speaker 1: 00:57:24

It's any of the PrevAs.

Speaker 0: 00:57:27

Yeah, yeah, yeah, of course, of course.
I've never thought about that.

Speaker 2: 00:57:30

So actually, using multiple towers in parallel would help your privacy, but suck for you because you pay three bounties.

Speaker 0: 00:57:39

Yeah, being honest, I haven't put that much thought into L2 mainly because, you know, if towers were early, imagine building on L2 towers, which have no release date.

Speaker 1: 00:57:53

Well, enjoyed the conversation about watchtowers and...
Enjoyed?
Enjoyed.

Speaker 0: 00:57:59

That sounds like like a feeling, you know?

Speaker 2: 00:58:01

It's over.

Speaker 1: 00:58:04

Feeling time is over.
Thanks for joining us.
It's great to have you in the office this week.

Speaker 0: 00:58:09

Thank you for inviting me.

Speaker 1: 00:58:20

OK, Merch, what did you think of that?

Speaker 2: 00:58:22

I think we covered all of it.
Eight years worth of Bitcoining.

Speaker 1: 00:58:26

That's a lot of going back to the original idea of watchtowers and the incentives of the network.
It's interesting to think about how watchtowers factor into how Lightning functions properly.

Speaker 2: 00:58:42

I think, especially in the context of mobile wallets getting more powerful, getting more capability with having work on HODL invoices.
And I think it sounds pretty much sure Watchtower implementation will make a mobile lightning wallet environment a lot more doable.

Speaker 1: 00:59:02

Anyway, enjoyed having him around in the office and hope you enjoyed the episode and we'll have another one out shortly.
