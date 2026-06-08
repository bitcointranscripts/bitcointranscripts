---
title: 'Inside the "Kernel Project" & the Bitcoin Core Development Process w/ Core Dev Stéphan'
speakers:
  - Stéphan
  - Shinobi
tags:
  - libbitcoinkernel
  - multiprocess
  - stratum-v2
  - fuzz-testing
  - build-system
categories:
  - Developer Tools
  - Mining
date: '2026-02-03'
source_file: https://youtu.be/lEK_cej4AjE?si=VN72CMseVf64wzr5
media: https://youtu.be/lEK_cej4AjE?si=VN72CMseVf64wzr5
transcript_by: 0tuedon via tstbtc v1.0.0 --needs-review
summary: Stéphan (Core Developer at Brink) and Shinobi discuss two long-running Bitcoin Core architecture projects. The kernel project (libbitcoinkernel) extracts Bitcoin's consensus validation logic into a standalone library so external projects can use it without risking consensus divergence — moving this code is risky because any subtle behaviour change could cause a fork. The multiprocess project separates Bitcoin Core into distinct processes (node, wallet, GUI) with well-defined public interfaces, enabling safer development, better tooling and CI, and cleaner integrations like Stratum V2 mining interfaces. The conversation also covers fuzzing and testing infrastructure, cross-module complexity, and the case for long-term maintenance work over new features.
---

## Introduction to Bitcoin Core & Kernel Project

Speaker 0: 00:00:06

Hello, everybody.
I'm Shinobi, the technical editor at Bitcoin Magazine, joined here by Stefan, also known as Stikiz, a Bitcoin Core contributor.
So we're going to talk a little bit about some of the work he's been doing helping Settadid with the kernel project and then kind of go into some of his review work before that.
So I guess kind of start like what was the state of like the kernel project when you joined?

Speaker 1: 00:00:34

So the kernel project largely had two different phases.
In the first phase, it was all about identifying which code actually belonged to validation, and then moving all of that into separate directories or at least a separate library.
And then the second phase was about building a public interface around all that validation logic.
And so when I started looking at Kernel in more detail, it was somewhere halfway in that first stage of the code organization.
So the most work that I helped with since has been just moving everything into a more logical place, which also involved a bunch of cleanups because when you move code around, it's also a good time to clean things up a bit and remove some foot guns or some bugs or just make things a bit nicer, more modernized as well.

Speaker 0: 00:01:29

And So, what's your kind of take on the progression of the project?
I guess kind of from where it started before Saturday took over and kind of the general work that was involved in getting from the conceptualization to like where things are now?

Speaker 1: 00:01:52

I think the pace for these projects kind of goes up and down a bit based on where you are in the project and who's contributing.
I think in the first stage, again, from the part where I joined, progress was kind of moderate.

## Why Moving Consensus Code Is So Risky

Speaker 1: 00:02:07

It kept going at a steady but not super fast pace.
Also because these changes were very critical.
Like, if you move consensus code around, even if it's just moving it around, that can still introduce bugs potentially.
So you very much don't want to rush that process.
So yeah, not an excitingly fast pace, but I think quite appropriate given the circumstances.
And we had a group of a few contributors who would regularly come back to those PRs and keep making progress.
So it felt like it was...
It didn't feel like it was stalling for the most part.
And then I feel when things really picked up is about six months ago, when we already started working on the public interface of the Big Concurrent Library.
So thinking about how we expect and want people to use the validation logic.
That's when things really picked up pace, I think, for multiple reasons, but the main one probably, it becomes more tangible.
Like if you just move code around, except for people working on the project, it's not that exciting, because it doesn't add any functionality, it doesn't enable anything new.
It's important because it helps, it makes the code more robust, it helps us find bugs, it helps us prevent introducing new bugs when we make changes to what should be non-validation logic.
But yeah, it's just not that exciting, it's an important first step.
But then once we started building this public interface, we also asked people to like try it out and use it for small use cases, like we had some people use it for data science projects and then you know reports on findings on on Delving, or it was used in early prototype of SwiftSync.
And people could see that this was something that was working, even if in a limited fashion and still very experimental.
But it became tangible.

## Public Interfaces and Real-World Use Cases

Speaker 1: 00:04:00

And I think that gave us both the user feedback that was very helpful, but also attracted more developer interest.
So we've had a couple of new contributors joining who weren't contributing to the core before that are now spending really useful time on building new features, reviewing and bringing your own ideas into Kernel.
And that's really been speeding things up.
At the moment, we have a weekly call talking to my kernel, and usually it's around eight people on that call, which is a lot more than I think what you would have imagined a year ago.
So that's been really fun to see.

Speaker 0: 00:04:39

And so, you know, before you started contributing to the kernel yourself, you did like a lot of general review of kind of the project in general.
I think that gives you a good view into core as an overall project rather than just the subsections or sub-projects.
I guess to start getting into this, you think you at least take a college try at kind of breaking down like what are the major like different areas of core as a project in the code base?
Like what's their functionality?
Like how do they touch other parts of the code base?
And just like how that kind of organization works in terms of the different areas people work on?

Speaker 1: 00:05:25

Well, yeah, sure.
Trying to give it some structure.
So I think a helpful way to organize it is kind of at the foundation of it all.
We have the tooling and the build system, the CI that basically allows us to do the work that we're doing.
So over the last year or two, for example, We've had a big project that moved the build system from AutoTools to CMake, which was necessary for some technical reasons, but also just made for a smoother development experience.
CI, we've expanded lots, like automated testing.

## Tooling, CI, and Developer Experience

Speaker 1: 00:06:00

Whenever we push and merge code into the code base, that's been expanded a lot, it's been made faster, more robust, so everything that makes that developer experience better and helps us catch bugs faster before they even can be merged into the master branch.
Then we've had a lot of work happening on everything, like net processing, basically all the peer-to-peer stuff is another big area of the code.
Maybe not as much in recent years, But that's a big part of it as well.
We've had a lot of policy work happening and mempool related work.
Cluster mempool obviously has been the latest one that has got merged and is getting close to being in a final-ish state.
But then also, of course, the mempool policy-related work that's been a bit more in the news recently.
The IPC interface is a big one that's been making a lot of progress this year, especially.
Multiprocess has been around for, I think, almost 10 years now.
It's the longest running project that's still open in Bitcoin Core.

Speaker 0: 00:07:09

Real quick, do you kind of want to explain for your listeners what the MultiProcess project is, why that's been such a long ongoing project?

Speaker 1: 00:07:18

Yeah, sure.

## Multiprocess Architecture Explained

Speaker 1: 00:07:19

So the goal of multiprocess initially was to allow us to run different parts of what is currently Bitcoin Core into separate processes.
So Bitcoin Core is an application that does a lot of things at the same time.
So I think the initial outline of that project was to have a separate process to run the wallet, to run the node, and to run the GUI.
Those were the three main components, where for example, you could run your node on your remote server and run GUI locally.
You could spin it up and down how you wanted to.
So it enables certain new kinds of functionality and it also offers security and safety benefits that process isolation offer.
It was a very ambitious project.
And so it took a while to be developed and especially to be reviewed.
And so it kind of became inactive.
Well, this is before my time, but quite a few years ago.
Until we had a new use case pop up about a year ago or so, because there was, there's a lot of work happening on Stratum V2, the upgrade of the mining pool protocol to help mining pools communicate with hashers.
And an initial approach on making Bitcoin Core compatible with Stratum V2 was to basically incorporate a lot of Stratum V2 logic into Bitcoin Core.
But this of course then adds to the total service of the Bitcoin Core code base.
And so there was another approach suggested to try and keep it out of core and basically have separate applications talk to each other over IPC, over this inter-process communication protocol.
And so that was like an actual real use case to help move the multiprocess project forward.

## Mining Interfaces and Stratum V2

Speaker 1: 00:09:01

And that's also why we released the mining interface, I think, in version 29.
It could be off of the number.
As the first version to help Stratov2 clients connect to Bitcoin Core without putting the Stratov2 logic in Bitcoin Core to help maintain that modularity.

Speaker 0: 00:09:19

Hey everyone, it's Shinobi, and I'm here in front of the Chicago Fed to talk to you about the core issue of Bitcoin Magazine.
The last few years have been a bit of a communication breakdown between developers and people using Bitcoin.
Bitcoin exists to be an alternative to this institution, but to do that it needs people to actively maintain it.
If you actually want to hear from developers themselves how they approach their work and what they choose to work on, go to BitcoinMagazine.com and get yourself a copy of the core issue.
I mean, this is all kind of, I guess, a giant project untangling the mess, I guess you could say Satoshi left.
Like, If you actually, you know, even if you don't program or really understand software engineering, I think if you look at the code base today or other typical code bases versus what Satoshi released.
It was just a giant blob of code with everything all tangled together versus traditionally software is made modular to begin with.

## Why Bitcoin Core Must Evolve

Speaker 0: 00:10:58

You have this process over here, that process over here, cleanly talking to each other through a defined protocol or API.

Speaker 1: 00:11:06

Yeah.

Speaker 0: 00:11:07

And yeah, I really think like viewers should appreciate like how important something like this is, Just from the point of view of this is software, developers have to continue maintaining this.
Like Bitcoin, even if the consensus rules never change again, like it is not a piece of software that can just never change, never have code updated to respond to changing realities of the world.
And that really is a necessary thing if we want people like yourself to continue spending your time actually keeping this working for us.

Speaker 1: 00:11:46

Yeah, no, absolutely.
I think it's the reality that like software just needs to be maintained because you know, operating systems change, compilers change, and just keeping up to date with that reality is already a reasonable part of the law.
But we also see the way that Bitcoin is used changes.
I think the min relay fee changes that were done a few months ago I think are a good example of that.
That is not something that was initiated or pushed by Core, but it was something that Core had to react to because suddenly users decided to use Bitcoin in a different way.
And so you have to react to that.
And then, yeah, there is the reality that, like you're given a certain code base to work with, which was not perfect in all ways, But yeah, that's what you have to deal with.
And so I think a lot of the work that we're doing now is to help turn that into a foundation that we can build on for not just next year, but for decades to come.
And a big part of that is just spending the time to, for example, modularize code more as we do with the kernel project, and to, for example, with the multiprocessor project, to just increase that robustness.

## Validation, Testing, and Fuzzing

Speaker 1: 00:12:56

And that is also one of my personal goals for the future, is to make sure that even with reduced developer resources, we can still maintain and make sure that BitConcord is as reliable, robust, and useful as it is now, even if in the future it will have more features and more functionality than it has now.

Speaker 0: 00:13:19

Are there other big areas of the code base or projects you think are worth mentioning?

Speaker 1: 00:13:25

Oh, yeah.
So I think I already mentioned the build system in CI is like one component.
You have all the P2P logic that deals with, you know, you have all these different Bitcoin nodes that need to talk to each other.
How do you do that in a safe way?
Because you're dealing with an authenticated protocol.
So you have to build in certain defenses that people can't bring down your nodes.
And that's a bit of a different paradigm than most other software that is authenticated.
Then of course you have a whole lot of validation logic that deals with validating transactions and blocks, everything consensus related.
We also have a lot of effort focusing on testing these years.
We have our unit tests and our functional tests, but then also a rather recent focus has been the first testing, which has been getting a lot of attention in recent years to basically, in a smart way, hammer the system with all kinds of possible inputs and see what kind of output it creates and see if that can crash the application, which helps you catch a whole range of issues that are just very difficult to do with manual testing because we're humans and we don't see all the options all the time.
The wallet is another big component of BigConcord.
We also have a visual user interface, the GUI, that helps people that don't want to run BigConCore in their command line to give them a bit of an easier access into the software.
And we have some other more utility like software, for example, some indexes that you can build with BigConCore for common stats, for addresses, And I think I'm probably forgetting something, but I think top of mind is roughly the main areas of work.

## Cross-Module Complexity in Core

Speaker 0: 00:15:13

And so, you know, when you go through reviewing PRs in different sections of the codebase, like given the state of things now in like the past couple years, like how often does somebody who say just wants to make a change to the wallets or something in the peer-to-peer logic have to kind of cross the boundaries and deal with other parts of the code base.
Is that as common as it used to be?

Speaker 1: 00:15:41

I think that's improved a lot.
So A lot of the work that has already been done for the multi-process project was to basically build those interfaces between different parts of the code, for example, between the node, between the wallets, between P2P, to really separate those concerns.
So If you make changes in the wallet, you really should not have to be concerned about most of the other code.
But there are exceptions.
Like, you know, the isolation is not perfect.
And so when you do make those changes, you do need someone with a bit more in-depth knowledge to verify that what looks like a safe change is indeed a safe change, because those side effects are sometimes hard to anticipate.
So I'd say mostly it's in a pretty good shape isolation-wise, but not perfect, which makes it...

Speaker 0: 00:16:29

How much does it slow down the progress in a PR when somebody does have to deal with that overlap and like consider what's going on in some other system based on what they've changed and what they're working on?

Speaker 1: 00:16:42

I think it's maybe one of the biggest factors in which PRs make progress and which don't.
Obviously, people review PRs as a function of how important they think that change is.
That's probably the biggest factor, but then also how likely is it to make progress and is it gonna get merged eventually?
Because if you know, like, no one else is going to review it or it's just too complex to be merged, then it's kind of hard to convince yourself to spend time on something because it doesn't really serve an actual purpose.
And so assuming that the change is meaningful enough to satisfy that first criteria.
If the code that's being touched is more complex, as in it touches different systems, then people just find it much more difficult to be confident that the change is safe.
And then it becomes much more, again, much more difficult to justify spending your time on that, because you have to spend much more time reviewing the code and thinking about edge cases and maybe adding tests.

## Long-Term Maintenance vs New Features

Speaker 1: 00:17:41

And yeah, That's what I personally see, I think those PRs usually stall the most, because it's just hard to stay enthusiastic and motivated about working on that.

Speaker 0: 00:17:52

Yeah, so the multi-process project quite literally is something that could drastically improve development pace and development speed, like finishing the last, I guess, string of things that need to be finished there?

Speaker 1: 00:18:08

I think that's actually already done.
The isolation work, as far as I've seen, is pretty much complete.
The most outstanding work that needs to be done there is more the code that actually deals with the communication between those different parts.
Because you're certainly talking about, yeah, different processes that need to communicate to each other efficiently, reliably.
You need to be able to debug it and kind of monitor those processes quite efficiently.
And that introduces new dependencies, which then again need to be understood and reviewed because we don't add dependencies into the code base without knowing that they are secure and reliable and have a minimum surface to introduce potential risks for the code.
And I think that's the main holdup with multipass at the moment is that that code is just fairly complex.
And again, with some of these complaints, people are less confident that it's safe.
And if they're not confident that it's safe, then they're going to be much more reluctant to leave their axe.
And yeah, that's a difficult thing to get out of.
But having the actual demand, you know, We had the use case now with the mining interface for Stratum V2, and so the complexity is still there, but if demand increases, then you're more likely to make progress on these kind of projects that are important, but it's just, it takes more resources.

Speaker 0: 00:19:28

Mm-hmm.
Alright, and I guess, You know, looking at this kind of work and the fact that a lot of developers' time is kind of spent on this, I wouldn't call re-architecture completely, but re-architecting of things and kind of polishing and streamlining things, maintenance, optimization.
Like a lot of people in the community kind of look at those things being prioritized and see that as something to criticize.
Like there are better things that developers should be doing with their time or more important things to focus on.
What do you think when you hear that type of criticism from people?

## Building Bitcoin for the Next Decades

Speaker 1: 00:20:13

I think it's definitely, There's a lot of truth to it.
I think it's important that developers work on projects and on features that matter and that have impact and we shouldn't get lost in academic exercises on building stuff that is very nice on paper, but in practice doesn't serve real purpose.
And I think it's important to keep an eye out for that.
But I also think the people working on core do that because of, and in ways that they think are important, is because they get excited about certain projects.
And yeah, some or maybe even a lot of those projects at the moment are focused more on maintenance or improving the robustness of Core rather than adding new features like protocol upgrades or covenants, which is a big one.
And I don't think one should be done instead of the other.
It's more a function of what are the people working on the software care about the most based on their experience and their view?
And I think a lot of people, at least it's my own personal preference, my priority for working on Core is to make sure that we can We have this foundation that we can easily and reliably keep building on for the next decades to come.
And I think having software that is easy to maintain, easy to understand, easy to review, increases the pace of future developments.
Because if you have code that you can easily grok, that you can safely make changes to because you have good testing infrastructure in place that is more modern, so it can't introduce some of the bugs that you could have with like older C++ code, for example.
That's kind of investing into...
You invest time now and you expect to get return on the time in the future, because adding features on a code base that you don't understand, it's just incredibly dangerous to do.
And, you know, after all, we are building software for the future that should never introduce any significant bugs, especially stuff like consensus failures, that's absolutely critical to the system.

## Closing Thoughts on Bitcoin Core’s Future

Speaker 1: 00:22:28

And so, yeah, I think neglecting the importance of those kind of changes, having good testing, having good build systems, having good modularity, having modern and easy to understand code, is absolutely critical for being able to do the also important work such as protocol upgrades.
So yeah, I just invite anyone that thinks that a certain feature or change is important to come join and help us do the work.
Not instead of, just in addition to.
Both things I think can happen at the same time.

Speaker 0: 00:23:02

Yeah, I mean, it's kind of like your car breaks down.
Do you just stubbornly go deal with the complexity of public transit or taking a cab everywhere and the extra cost?
Or do you just take the time and fix your damn car so you can get where you need to go?
Yeah.
All right, well, I really appreciate you sitting down and talking to me about this, Stefan.
And I hope everybody who watched this has a little bit better of an idea as to how core is organized as a project and why developers prioritize certain things over the other.
So thank you again.

Speaker 1: 00:23:39

Thanks for the chat.
