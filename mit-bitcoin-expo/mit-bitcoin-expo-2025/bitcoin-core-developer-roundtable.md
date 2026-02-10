---
title: Bitcoin Core Developer Roundtable
speakers: null
tags: null
source_file: https://youtu.be/TEVJUjOGmOI?si=bRZxlnBp2toFykWc
media: https://youtu.be/TEVJUjOGmOI?si=bRZxlnBp2toFykWc
categories: null
date: '2025-04-07'
transcript_by: 0tuedon via tstbtc v1.0.0 --needs-review
---

Speaker 0: 00:00:00

Maybe just to start things off, let's do a quick round of introductions and maybe add on why you work on Bitcoin Core.
You want to start with Gloria?

Speaker 1: 00:00:10

Sure.
Hello, I'm Gloria.
I went to college, not this one, but I went to college.
So like a lot of college students, I really wanted to save the world.
I was interested in technological solutions to social problems.
I met Alex Gladstein of the Human Rights Foundation and learned about all the activism and just billions of people who don't get access to the US dollar like we do in the US, and found this problem extremely compelling and found Bitcoin to be a really good solution to it, or at least the furthest I can think of.
And so as a computer science student who wanted to be a software engineer, this was kind of the perfect marriage of two really good reasons to work on Bitcoin.
And so I applied to the Chaincode residency when I was a college student, ended up starting to contribute to Bitcoin Core and then when I graduated I was lucky enough to get a grant from the HRF and it was called Square Crypto or Spiral at the time to do it full time.
And so since graduation I have worked on Bitcoin core full time for the past four or five years.

Speaker 2: 00:01:35

So I'm Corey, I have a background in open source, C++ software development, and I got tired of putting my credit card number in to buy things online.
That just seems stupid to me.
So I read about Bitcoin and the idea that you can push a payment as opposed to pull and that made more sense that that just seemed like the way that that things should be.
So I hopped in and there's this idea that the code is the money.
And it took a long time for that to click for me.
Like it's as simple as that.
The code, the software is the money.
And it just became a fascinating thing to think about to me.
And the number of just technology challenges, it's just that there are just hard problems in Bitcoin and they're a lot of fun.
So I got hacking on the code.
I started, I was asked to join the Bitcoin Foundation.
I had health insurance for one week at the Bitcoin Foundation before it crumbled.
And thankfully, Gavin and Patrick and some other people that were at the foundation kind of shopped us around and found us a home here at MIT.
So I've been working at the DCI here at MIT, the Digital Currency Initiative, for the last 10 years.
And my job is just to work on Bitcoin and Bitcoin Core and keep it going.

Speaker 3: 00:03:02

My name is Antoine Poinceur.
I work at Chaincode Labs.
I think I got started working on Bitcoin for similar reasons to Gloria and the reason I work on Bitcoin core in particular is probably impact.
Probably the most frustrating project you could work at, but also the most impactful one in the space.

Speaker 0: 00:03:29

Cool.
So we're going to do a nice, easy warm-up here.
What should we do about all these soft core proponents?

Speaker 3: 00:03:39

Stupid.
All of them at once, unsubscribe.

Speaker 0: 00:03:47

Anybody else want to jump in?

Speaker 1: 00:03:50

Yeah, I think you alluded to this in your presentation.
A lot of people, I guess, as Bitcoin devs, like, I mean, my job description is not completely clear, right?
There's maintaining the Bitcoin core code base, which I would say is kind of the primary hat that I would wear.
And then there's protocol research and Bitcoin solution creation.
So I think a good example of this is people are like, we need to make self-custody better.
And I think there are a lot of different ways to do this.
People want to build vaults, so they want some kind of covenant to build vaults.
But of course there are people who are building certain apps or companies where there's an app and a hardware wallet and they're trying to create a solution for custody.
Or if you're interested in scalability, like there are many different layers of the stack of not just technology but products that you can be working on.
And so I guess my thing is like, yes there are a lot of different things in Bitcoin and I think just talking about consensus is, I think people conflate consensus with protocol development or they conflate soft work proposal championing with Bitcoin core maintenance.
They're like very, very different things.
And actually, Corey, you had a really good point earlier when we were chatting about like how there's almost, they're almost incompatible sometimes.

Speaker 3: 00:05:29

So if you want to talk about that.

Speaker 2: 00:05:31

Yeah, so in my head I think of this as the soft fork paradox where basically the core developers are tasked with keeping Bitcoin as it is known alive and maintaining Bitcoin, the reference implementation, and that kind of is core.
And because there's no spec, because there are no written rules, the reference implementation is Bitcoin.
So if you're a core developer, if you're a maintainer, your job is to maintain Bitcoin as you found it, basically.
And so there's this kind of fundamental problem of who is tasked with, I mean, you can, it's a stretch, but you can define every soft fork as an attack, because it's an attack on the status quo.
And it may be an upgrade, it may be that 90% of people want this attack, but it's an attack because it changes the rules.
So it's kind of a, you know, there's kind of an oath that you take, kind of an implicit oath as a maintainer that thou shalt not change the consensus rules.
And so to merge in a soft fork, and especially the activation parameters for a soft fork, you're kind of violating that oath.
So to me it's this big open question of who is tasked with making these changes.
And I think it's easy to forget that there are people behind the merge button on GitHub or the merge script that the maintainers run.
There's a human being that is sitting behind that and clicking or hitting enter and saying, boom, I've broken my oath.
I've decided to fork Bitcoin.
That's a real thing that someone has to do.
And so who is that person?
Who can be tasked with that?
Gloria has that power.
Do you wanna do that?
Like that doesn't seem like a fun Thursday night.

Speaker 1: 00:07:23

Yeah, I think related to that, I think people seem to have this obsession with soft works that like, I'll often get asked like, oh, you work on Bitcoin, like what's the next soft work?
Which is like soft works, I think deservedly get a lot of coverage and sensationalism because like you said they consensus changes are changes to the rules that decide who can spend their money and who owns how much Bitcoins.
That's really, really invasive.
And I think that's so fundamental.
So of course it makes sense that it comes up in the news so much more often than what port you can open as a Bitcoin node for inbound connections.
But changing just from 83333 is really important for censorship resistance, for example.
We were really concerned about ISPs shutting down traffic to that port because that's so characteristically a Bitcoin node.
And so I think it was a really great change for us to work on that.
But there's no bit for that.
I didn't see any news coverage of like, oh, the porch has changed.
And so, yeah, I think it's almost like people watch too much Grey's Anatomy and they're like, all of medicine is brain surgeries.
Oh, you're a doctor?
How many brain surgeries have you done?
But like most of medicine is first of all not brain surgery.
It's certainly very impressive, very invasive, but most medicine is preventative and you can save lots and lots of lives and you know do health care without ever doing a brain surgery even if it is kind of this sensational, like dramatic thing.
So similarly, I think my point here, I'll finish up soon, is even within BIPCONCOR there's so much that is done that is not consensus.
If you look at the list of BIPs, probably half of them are actually peer to peer protocol things and there's a lot of very impactful things you can do there.
And a lot of things don't have BIPs because they are engineering challenges that Satoshi left as an exercise to the reader.
And we had to figure out.
And when there were tens of thousands of transactions coming down the network, like stalling nodes, we were like, okay, we need to fix this.
So the idea of Bitcoin being robust and censorship resistant and all these things are things that we work on every single day that you don't necessarily see.

Speaker 2: 00:10:03

So I'd quickly like to ask Jonas, because I've heard you give your spiel a couple times about how you're not one of us and you're the water boy and the helper and all that.
But that's bullshit.
So What would you do about all the software?

Speaker 0: 00:10:17

That's not bullshit.
I am an outside observer.
I really, I think for some of these, the truth of the matter is that we, as a non-big brain, need to have some trust for the keepers of the flame.
And if they, you know, it should be verified clearly.
But I think a lot of my opinion of course is informed by people that I respect the opinion of.
And I think I try to understand the trade-offs and understand the use cases and the risks involved.
But I'll never be the one that runs the script.
So it sort of absolves me from the ultimate load, and I think that makes me, again, a muggle and a waterboy like most of the ecosystem.

Speaker 3: 00:11:18

Antoine, do you have opinions?
Three things.
I wrote a blog post about my opinion and all the staff folks' proposals.
For the longer version, you can refer to that.
I'd like, first of all, to highlight what Corey said about consensus.
I think people severely underestimate consensus.
We have this global network and the set of rules that everyone agrees upon.
If we got together and tried to decide the consensus rules today, with everybody with divergent incentives and opinion, it would just never happen.
And without consensus, there is no Bitcoin.
I've heard the other day on Twitter, somebody referring as, oh, the proof of work can just decide what the consensus is.
The proof of work is part of the consensus.
The consensus comes before anything else.
Bitcoin is valuable today.
Censorship-resistant money, even if it does not come at a huge scale, solves real problems today.
So we must be very careful in risking it.
Thank you, I wanted to give more practical response to your initial questions.
I think a lot of the soft fork proposals that we see today, not all of them, but a lot, because there are so many of them,
kind of solutions to such a problem or it's not exactly clear what problem they're solving.
And it's even amplified by the fact that Bitcoin has become so big that we cannot be specialists in every single area.
And there is this area, especially with the covenant discussion, there is researchers specialized in this area.
So it would be very useful if, because in addition to solutions in search of a problem, there is also not all of them agree on which solution without even defining clearly the problem in the first place.
So I think what would be useful from a Bitcoin Core perspective would be some sort of a research report from this loosely defined researcher community of we set to solve this problem and we find that this solution is appropriate and it has this and this tradeoff and we bring it to the community.
I know that there is a few people I see in the room that said to do exactly this work, in comparing different alternatives.
And I think that's very useful.

Speaker 0: 00:14:09

Can I ask, because I think this is a point of frustration for a lot of said people?
What's the right forum to do this?
It seems like it leaks into a lot of different places.
So, you know, there's back and forth on Delving, there's the mailing list.
I think the lowest common denominator seems to be Twitter.
But like, where's the right place to engage in these conversations?

Speaker 3: 00:14:35

Not Twitter.
Okay.
If you want to be taken seriously, I mean.

Speaker 0: 00:14:41

Okay, can we do more better than not Twitter?

Speaker 1: 00:14:46

Yeah, I think, I like delving.
I guess I'll take the bait.
Like I think so people often ask like oh like the maintainers are not merging.
Some coming in.
And you know Fiat Quokka and I will look at each other and be like, is there a PR open for that?
There isn't on Bitcoin Core.

Speaker 0: 00:15:14

But there is now.

Speaker 1: 00:15:15

Yeah, there is.
Well, I didn't name a specific one.
But like I think Bitcoin Core, the GitHub repo, is a place for code review.
And of course, we have lots of code, like, concept discussion on core at various times.
I'm not trying to like police, you know, where like you don't come on core.
But like a lot of the wider community discussions slash flame wars can be very disruptive in a GitHub repository.
It's like this is where we work.

Speaker 0: 00:15:50

We still don't have an answer.
What's the rules of engagement?
Because as I tried to point out, we have this conflation of protocol research and Bitcoin Core.
They do have to dance together eventually.
So what is the lead up, what is the back and forth and the social nuance of that lead up to said dance?

Speaker 2: 00:16:14

I think There's a frustrating truth here that that venue changes over time and has changed over time and there is no like Bitcoin, especially Bitcoin Core struggles with process because it's particularly hard to install process for something that's supposed to be essentially process free.
You know, the Core devs as you know, kind of, sort of kind of gatekeepers as we're pretty often called, like we shouldn't exist in that way.
And so there shouldn't be a technical forum or a specific venue for this type of a discussion because it almost certainly invites discrimination as far as who's allowed to show up, who's allowed to argue.
So over time, it used to be Bitcoin talk is where these discussions would happen, and then it was Reddit, and then it was the mailing list, and now it's delving and Google groups and they were scaling Bitcoin and there are conferences and there are papers and I think there just is an unfortunate truth that should be recognized that is these discussions are going to be fluid and the venues are going to be fluid and in order to participate, there's almost a mini consensus mechanism involved here as well that you have to know where the conversation is taking place.
There's a, clumping is just natural in these scenarios.
So these fork discussions may happen on Delving and that may be where the interesting thing happens, but that's not to say it's where it's going to happen next time.

Speaker 0: 00:17:43

We've covered one topic, so You get last word.

Speaker 3: 00:17:49

Just a third point I wanted to make earlier.
Just a clarification for people that are maybe newer in the room to Bitcoin.
Corey and Gloria talked about the merging scripts and we talked about soft forks.
Merging a soft fork in Bitcoin Core is not how it gets activated in Bitcoin.
It's what users choose to run, what software users choose to run.
I would tend to agree that Bitcoin Core is probably the only reasonable software to run as a full node.
But still, merging it is not enough to activate the soft fork.

Speaker 0: 00:18:28

So let's not talk about soft works.
But let's talk about how other things get done in Bitcoin Core, the software project.
So you all have done big things and are in the process of doing more big things.
And so, like, What does that dance look like?
How do you, how are you effective as a contributor to getting big things done at Bitcoin Core?

Speaker 1: 00:18:56

I heard CMake was 300 pull requests.

Speaker 0: 00:19:00

Oh, 300 pull requests.
That's a lot for those that don't know what that is.
But that's a lot.

Speaker 2: 00:19:05

So I think maybe Gloria's point there was there's a lot of boring stuff that goes on in the day-to-day development of- That's not what I meant.

Speaker 0: 00:19:16

This is poor framing, Corey.
Why don't you try again?

Speaker 1: 00:19:21

OK.

Speaker 2: 00:19:21

I think what Gloria meant there was Bitcoin Core is a software project like any other.
And yes, it may be money, and it may be a consensus mechanism like no one has ever seen before, but it's also a massive C++ pile of code.
And just like any other project, there are refactors.
So the build system is one that I participate in a pretty good bit.
There's the build process, the release process.
We can't even just hit merge on, we can't hit the green button on GitHub because we're too paranoid that Microsoft might start sliding in soft forks on us.
So we have, you know, there's a script that attests to certain keys.
You know, you as a user have all kinds of power to monitor us.
I don't know if that's known or obvious, but if Gloria is trying to do something sneaky, then it would be very quickly noticed.
So there's just all kinds of work that goes into not only just doing the day-to-day maintenance, the modernization moving from C++ 98 to 11 to 17 to 20 and managing dependencies and refactoring code.
And there's just a lot that goes on.
And it's just not all sexy soft fork stuff.
So to me, my day-to-day code, or my day-to-day work, the thing that motivates me is just doing plumbing work, is just making sure that the code looks prettier now than it did yesterday or last week.
And so to me, this is something I talk a lot about, like the modularity of things, the architecture of the software, keeping the code alive and maintainable for the next 10, 20, 50 years.
You know, it's kind of insane to think, but right now there's only one reference implementation of Bitcoin.
And unless that changes somehow, then 50 years from now, if we still want Bitcoin to be running, then this piece of software will still need to be running.
So there's just a lot that goes on in day-to-day work that's not this soft fork stuff.

Speaker 1: 00:21:29

I think build system is one of the most underappreciated parts of core.
And there are, I think, unique challenges that are battles that we picked in Bitcoin for a really good reason, like you mentioned, being really conservative about dependencies.
Obviously, we do that for security purposes, but also the fact that we have a build system that supports so many different platforms So many different ways of running Bitcoin and not just you know x86 Linux is So that it can be very accessible for anybody to run a node on their Windows laptop, on their Raspberry Pi, in the background on their MacBook, or their Linux box.
Having reproducible builds for each and every one of those targets is ultra hard, right?
And these are, I think, uniquely challenging.
And we spend a lot more effort on things like this than maybe proportional to other things in the project compared to other cryptocurrencies or whatever, because we care really strongly about the security and the accessibility of running a node.
So I think but, like, you never hear about the build system.
Like raise your hand if you've ever seen a single, like, Bitcoin, like, article about CMake.
Like, never.
Right?
But that was, like, a 300 pull request over the past couple years, and it was executed really, really well, and it took a village to do.
Yeah, I just, sorry, I just wanted to shill build people.

Speaker 3: 00:23:03

Yeah, Antoine?
Can just do things.

Speaker 0: 00:23:10

You can.
We just talked about how that's hard.
You just had like 20 full minutes of you can't just do things.

Speaker 3: 00:23:19

Well, actually you can.
There is a lot of things that we just don't do yet that was just kind of Astonishing given the size of the network two years ago.
We had a CVE Because there was too many transaction on the network We had never stress tested the transaction relay to this extent and it just cloaked the CPU So that's one thing you don't need to change Bitcoin Core to just help with testing in this area.
There is many people, so One recent news is that Eugene Segal joined Brank to work on Bitcoin Core full-time.
Little guy was working on LND full-time and he found a critical, not critical, high severity vulnerability in Bitcoin Core.
He didn't need to change Bitcoin Core to do this and It's big things because it's high impact Another one which needed small changes to Bitcoin Core is DRX block that Jonas mentioned earlier about peer-to-peer monitoring.
This one guy that does it for this massive network that is Bitcoin.
He introduced TracePoint into Bitcoin Core which was a small way to get metrics out of the software.
And then he built his own infrastructure entirely out of the software.
And that's how he monitored the whole network.
And he's crying for help.
So if anybody is interested in doing high impact stuff for Bitcoin, you could help with network monitoring.
You can just do stuff.

Speaker 0: 00:25:11

Let's talk about the roles that people play in the software project, Because I think from an outsider, it does seem really hard to just sort of like, well, where do I start?
What do I do?
But there's also like these maintainers, and these maintainers are, you know, ordained somehow, and they have special powers, and they decide our future.
Isn't that all right?
Isn't that, isn't that, they're, they're in charge?
Is that how it goes?
What's the, what's the, let me put it to a, a better, more pointed question.
What's the overlap between maintainership and leadership in this project?

Speaker 1: 00:25:52

You can just do stuff.
Didn't you hear, Adeline?

Speaker 0: 00:25:57

This panel has gone off the rails.

Speaker 1: 00:26:03

I think they're orthogonal.
Like, what is a maintainer?
Apart from, like, having the keys to do the merge button, I think everyone here does some form of maintenance.
Like, Cory knows everything.
So you need to like there are so many parts of the code.
Like if you think about part of our job as Bitcoin core people to just remember how stuff works I would say like you remember the most stuff works.
And so the fact that you dedicate so much time to review and helping people with their projects and kind of figuring out all of the kinks of CMake, for example, I think is very maintainery.
And similarly with Antoine and Nicholas, the security advisory stuff, we went many years without a proper security disclosure policy.
And I think it's one of the most important things that happened last year.
The two of you kind of took ownership over, like, okay, let's go through past stuff.
Let's come up with a policy.
Let's make sure this thing is robust.
And we will open ourselves I think the security mailing list is one of the biggest human DOS vectors ever.
Because it's like an open port to the entire public where all of the emails that come in have to be read by trusted people.
And they contain extremely potentially extremely important information.
So, it needs to be opened immediately.
And so, I don't know, it's just like very, very docible.
And so to take ownership and be like, okay, I'm gonna be in charge of this, this is a very heavy responsibility, is maintenance of Bitcoin Core, right?
And then there's like, what do I do?
Which is like, run some scripts and make sure, try to get a release out the door, which, you know, I'm trying to do right now.
But it basically involves just being like, okay, who's going to do it?
I'll do it.
Right?
And these are the things that have to happen in order for the project to keep moving.
And similarly with, you know, there's like merging things and then there's like the administration of the GitHub repo.
Like we get so much spam, like that has to be closed or moderated or whatever.
There are all these stale issues.
There are 400 issues open and 250 pull requests open on the GitHub repo.
And it would be great if they are all responded to so that people don't think that Coin Core is this black hole, this abyss that you send your work into and never hear back from.
Of course you were talking about deletion and what I said about remembering how things work when reports do come to the security list or, like, you know, this has happened to me a few times where, like, I'm really going to get this thing done, I'm going to write this code, or I'm going to get this review done, and then I get an encrypted email.
It's like, oh, I found this thing that crashed.
Oh, crap.
I have to drop everything and go and do that.
The idea of taking responsibility for something.
When of course you can't, it's not written in anybody's job description as the volunteer fire department that if a fire happens, it's your job to put it out.
But you know that if you don't do it, who will?
So that's kind of what maintenance means to me.
And then the leadership thing.
There are no leaders.
You can just do stuff.

Speaker 2: 00:29:46

So I think Gloria was alluding to this in a couple of different ways.
But I think that historically we've conflated leadership and maintenance.
And specifically with the people who have the maintainer bit on GitHub.
The people who can actually hit the button or hit the merge script.
And the idea that we've tried to establish over the years is that a maintainer is essentially an automaton.
So no offense.
But someone who could, in a lot of ways, be replaced by chat-gbt, where your job is not necessarily to weigh in on the work that others are doing.
Your job is to kind of represent when it looks like most of the developers or the developers who matter for this particular pull request are on board and have signed off.
Once you have a good number of acts by the people who matter, you kind of just hit the button.
So maintainers aren't necessarily supposed to, or I hope it's understood by the other developers and by outsiders that the maintainers aren't necessarily weighing in when they merge something.
They're not necessarily endorsing any particular pull request.
They're simply acknowledging that this pull request seems to have the weight behind it, that the developers who have contributed to it have, you know, that it seems to basically fill the requirements.
And so it's unfortunate that, like for example, that Gloria is tasked with that responsibility and with looking at the security mailing list.
You know, those are two things that I think she's kind of stumbled into both of those roles because of this conflation of maintainership and leadership.
And one of the things that we talk about pretty often, or have started talking about more recently, is trying to split up these responsibilities so that maintainers aren't necessarily tasked with all of the leadership tasks as well.
Where the maintainership is kind of a role on, I mean, specifically on GitHub or in the Git repository.
And some of the decision-making and the leadership and the other roles that people take on, that people take on, you know, release management, For example, that's one that we were talking about at lunch.
You don't necessarily have to be a maintainer to do like 90% of what it takes to create a release.
There are some things at the very end, you know, you have to do the tagging and the binary pushing and that kind of thing.
But there are just a lot of things that go into producing a major Bitcoin core release that you don't necessarily need to be a maintainer for, you could volunteer that as a different role.

Speaker 3: 00:32:26

I'm going to do something very dangerous and disagree slightly with Kari.
I don't think we can replace maintainers with JetDBT because we need to keep accountability.

Speaker 2: 00:32:37

That was not a suggestion, by the way.
Okay.

Speaker 3: 00:32:40

Yeah, but I think that's something that is worth and...
Fuck, I cannot pronounce this word, so I'm going to skip it.
But just making importance of this is that we need accountability from maintainers.
But again, you can just do stuff.
And there is accountability that comes from non-maintainer contributors.
For instance, I can think of Marker, who keeps reviewing every single request that gets merged and finds bugs after it's merged.
And say, just before the release, he found a bug that was merged and we did not have CI, and he just read the code and since he has a compiler in his head or something.
He just realized that's not valid C++.
And he just said, well, you merged invalid C++.
And yeah, that's sort of a leadership, but just maybe leading by example more than trying to get people to do what he wants.

Speaker 0: 00:33:53

Cool.
We've done a lot of talking.
Do we want the audience to ask some very benign questions that we can be comfortable answering?

Speaker 3: 00:34:05

Or not.

Speaker 4: 00:34:06

Adam, I know you said you're less technical, so I'll ask you a less technical question.
What was it like growing up a Jonas brother, and what do you think the contributions of boy bands from the Beatles forward have been to the music scene in general?

Speaker 0: 00:34:20

Yeah, those are my cousins from New Jersey, and we're very proud of their success.

Speaker 4: 00:34:26

Thank you, appreciate it.
You're welcome.

Speaker 0: 00:34:29

Any other really important questions?
These are the kinds of questions that actually I like.

Speaker 5: 00:34:36

Thanks a lot for giving us the color on a lot of what the day-to-day work is that you do.
So thank you all.
One, just kind of a quick take, you know, some of the big things that are, you know, that thinking about OpCat and OpCTV, any kind of quick takes on are those going to happen and when?
I mean, just I don't want to derail the whole discussion, but just kind of your quick takes on that, given your perspective.
Thank you.

Speaker 3: 00:35:07

Maintain those decide self talks, right?

Speaker 2: 00:35:11

I mean, are you going to roll it at UASF?
Is that you?

Speaker 1: 00:35:18

One of those has a PR, but no acts, so there's nothing for me to do.

Speaker 5: 00:35:30

Do you think that it's going to happen if it's more than a city that you interact with?

Speaker 3: 00:35:38

My personal perspective is that there is still a lot of disagreement on each of those.
There is one that seems, because it's much simpler, well, not really, it seems safer, seems to be further in the road, but also there's clearly, clearly no consensus on anything.
And therefore there is no real role for Bitcoin Core at this point.
It seems that you would show up at Bitcoin Core for the final code review after reaching consensus among the wider Bitcoin research and developer community.

Speaker 2: 00:36:21

So in some ways I think to not weigh in is kind of a punt, but at the same time, so I personally don't see this as my job.
I can say that I have reviewed both technically.
I've looked at the code behind Upcat and CTV, and they're both simple.
And I've kind of given both the thumbs up.
But I don't consider myself big brain enough to understand what the implications of them are.
And so I think that, you know, like I called myself a code monkey earlier, I like to me, the C++, sure, ship it.
But the activation parameters, the, you know, actually having it as a feature in the currency that I have zero opinion on because I don't feel like I should.
So with all that being said about the soft forks, do you think we could get a Boston agreement hashed out tonight or should we wait until next year?
Let's go.
So who signs?

Speaker 3: 00:37:25

Who signs what?

Speaker 2: 00:37:27

If we get a Boston agreement drafted, who signs it?
Okay.

Speaker 3: 00:37:33

So. What's included?
Do you include the consensus cleanup or?
Cool.
The kitchen sink.
Let's keep going.
I'll let you ask the next question.
Mine's not super important.
You go.
I think we're next, right?
No, after you.
OK, thank you.

Speaker 1: 00:37:48

Awesome.
So in the interest of time, unfortunately, we have to wrap up the Q&A for this session.
But maybe we can catch the speakers afterwards.

Speaker 0: 00:37:59

All right.
Thank you so much.
