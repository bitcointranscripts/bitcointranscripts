---
title: "The State of Bitcoin Core Development"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://www.youtube.com/watch?v=zOZRRyboaYo
tags: ['bitcoin-core', 'career']
speakers: ['Aaron van Wirdum', 'Ava Chow', 'Ishaana Misra', 'Mark Erhardt']
date: 2024-08-31
summary: "Discover the latest developments in Bitcoin Core with our expert panel featuring key contributors to the project. This video delves into recent changes in security vulnerability disclosures, the challenges of funding open-source development, and the careful process of introducing new features to Bitcoin Core. Our panelists offer unique perspectives on the project's priorities and the distinction between Bitcoin Core and protocol development."
---
## Bitcoin Core Development Panel and Recent Policy Changes

Speaker 0: 00:00:02

Good morning.
My name is Aron Favirim.
I work for Bitcoin Magazine and this is the panel on Bitcoin Core development.
I'll let the panelists introduce themselves.
Let's start here with Eva.

Speaker 1: 00:00:16

Hi, I'm Eva.
I am one of the Bitcoin Core maintainers.

Speaker 2: 00:00:20

Hi I'm Merch, I work at Chaincode Labs on Bitcoin projects.

Speaker 3: 00:00:25

Hi I'm Ishana, I'm a Bitcoin Core dev and I'm currently interning at MIT's DCI.

Speaker 0: 00:00:31

Alright so let's start off with a recent topic.
So there was recently, there's a new policy within Bitcoin Core, there were security disclosures, right, Eva?
What's the story here?
What has changed about Bitcoin Core development?

Speaker 1: 00:00:45

Yeah, We've historically done a poor job of disclosing security vulnerabilities.
So recently, a couple of contributors have taken it upon themselves to rectify that.
So we've established a new disclosure policy where we're tracking bugs better, assigning them severities and now we're going to be disclosing things generally two weeks after the last vulnerable version becomes end of life.
In the lead up to deploying that, we've started disclosing a lot of historical bugs.
What is end-of-life?
Yeah.
In Bitcoin Core, we support three major versions.
So right now that's 27, 26, and 25.
So after the next major version comes out, then the oldest one becomes end of life.
So in a few months, we'll have 28, which means that 25 point whatever will become end of life and no longer supported.
And at that time, we would disclose any issues that were present in 25.

Speaker 0: 00:01:58

OK, so this is a new thing.
Merge, why is this new?
Why wasn't this happening before?

Speaker 2: 00:02:05

Before, probably most of the security closures just happened whenever the discoverer got around to writing up a blog post or whatever.
And so some things got disclosed, especially the bigger, for example the inflation bug a lot of people have heard about shortly, but now there was a backlog of some things that we knew about that hadn't been perhaps presented in any formal way yet.
So there's blog posts on BitcoinCore.org now that, well pretty short just disclosures on what vulnerabilities existed in older versions.
And I think one of the main things here is we're trying to tell, to make it clear that just because you hadn't heard about some vulnerabilities in Bitcoin Core before, it's not that it's bug-free software.
Stuff happens, it gets fixed, so we want to make a bigger, better job of, do a better job of disclosing and keeping track of that.

## Disclosures and Practical Benefits of Vulnerability Documentation

Speaker 2: 00:03:10

So everything up to 0.21 has been disclosed now.
I think end of this month, there will be some disclosures for 22.
So At the end of this month,
there will be some disclosures for 22?

Speaker 1: 00:03:19

So this month, at the end of this month, we'll have a couple more disclosures for things that were in 22.
Next month, it'll be 23, month after 24, and then 25 should be around when we release the 28 release.
So we will now be in sync with the policy that we established.

Speaker 0: 00:03:39

Maybe this is a stupid question, but real quick, what is the practical benefit of this?
Why do this at all?

Speaker 2: 00:03:47

In a way, so one problem is if there's undisclosed security vulnerabilities that people are aware of, attackers might have an edge.
So it's preferable that everybody knows.
Another one is that by documenting what has happened and how it was fixed, we retain the knowledge, we also teach maybe related projects what they should be looking at.
There is a ton of forked coins from Bitcoin, some of which have not very active development and well, they might want to know about these issues and fix them.

Speaker 0: 00:04:26

Ishana, you are a relatively new Bitcoin Core developer, right?
What's your experience starting out as a Bitcoin Core developer and what kind of advice would you have for other people who might be interested in doing that?

Speaker 3: 00:04:39

Yeah, so I started Bitcoin Core development almost like a few years ago And I think that the main advice I'd have is, well of course you need a strong understanding of fundamentals.
And I think that Chaincode Labs has a really good Bitcoin protocol development seminar that gave me good fundamentals.
But I think that people should...

Speaker 0: 00:05:01

Did you do that seminar?
Did you do that seminar?
Yeah.

Speaker 3: 00:05:04

And so it's great to talk to people about these concepts, but also I wouldn't be too hesitant with trying to contribute.
There's a ton of good first issues and small PRs that you can open.
And people are generally very helpful and will review and super supportive of new contributors.

Speaker 0: 00:05:24

Right.
If you get started, so you would recommend this Chaincode course, But at that point, is that open for anyone or how do you even get in there?

Speaker 3: 00:05:35

Yes, so the resources are on the website and anybody can use them.
And then they also do seminars, which are like where you read the resources and then you meet with people and discuss them.

Speaker 2: 00:05:46

Right.
Yeah, so we have a course that you can do self-paced.
It's a bunch of resources.
It's a lot of talks and reading material and articles.
So if you want to go for it in your own pace, all of that is linked on learning.chaincode.com We did these Bitcoin developer seminars and lightning developer seminars that were five-week programs and we had earlier this year the big fast program with I think over 600 participants.

## Becoming a Bitcoin Core Developer and Funding

Speaker 0: 00:06:20

Okay, this maybe ties in a little bit but like, well I want to ask kind of why would someone want to become a Bitcoin Core Developer?
That's a good question in itself.
And tying in, what's the status of funding Bitcoin Core Developers?
Because many Bitcoin Core Developers do get paid in some way or another, so what's the status of that?
Maybe, Do you want to start?

Speaker 2: 00:06:46

I'll start quickly.
I was just thinking of that Shackleton ad, fearless men, there's danger of death and whatever.
And no, so it can be pretty rough.
Like there's been a bunch of legal harassment over the years.
Funding was uncertain at times.
Sometimes if you're working on stuff that's not super interesting to a lot of people, it can take a while to get review.
It is, I mean, inherently any group of at least two people has social dynamics.
So if you find a few people that you get along with and collaborate with them, you might have a great experience if you're working on something that only interests you or you don't find your folk, then it might be a little more isolated.
So a good thing is maybe to pick something that you're really excited about, that you have drive for, because if you scratch your own itch, you tend to not lose your motivation as easily, and if you're more excited about something you tend to infect others with that.

Speaker 0: 00:07:50

And when it comes to funding specifically, who's funding Bitcoin Core Development and what's the status of that?
How do you get funded as a Bitcoin Core Developer?

Speaker 1: 00:08:00

So mainly the funding situation right now is grants.
So there's nonprofits like Brink, OpenSats, and there are companies like Spiral, who provide grants to developers to continue to work on features and projects and open source stuff.
That's mainly how newer contributors get funding.
Sometimes, if you're really lucky, a company will hire you to continue working on open source.
So that's what I do at Blockstream.
But yeah, generally, the funding situation is a little difficult.
But the grants are the main way that people get money.

Speaker 2: 00:08:47

There's also a little bit of an entry hurdle.
Because even if you're an established developer in other fields, if you're not known in the community, it can be difficult to get a grant immediately.
So often, people start out by working on stuff in their free time or by taking off a month and interning somewhere and working on a specific project to get a notch in their belt.

## Investing in Bitcoin for Grants

Speaker 2: 00:09:13

I think that's sort of what we tried to do with the FOSS program at Chaincode earlier this year was to create a space where people could focus on doing a bunch of different little Bitcoin things for a few months and we actually got a few full-time contributors out of that now, But yeah, you really have to sort of invest a little upfront before you become eligible for grants.

Speaker 0: 00:09:41

Ishana, is this all your experience?
Do you have anything to add?

Speaker 3: 00:09:45

Yeah, so I've not like received any grants yet, but what I think makes Bitcoin very unique is that in other places you can just get hired or get grants before you do this work, but sort of like what Mertj was saying, I think proof of work is a really big thing in Bitcoin and so you do need to show that you're capable of doing the work in advance.

Speaker 0: 00:10:07

Yeah, and Mert you briefly mentioned the legal issues there, specifically Greg Wright's lawsuits I guess.
In general how big of a, well that lawsuit is over fortunately, but in general how big of a problem is this for Bitcoin Core development?
Like, it must be at least some deterrence.
Do you think it has affected Bitcoin Core development?

Speaker 2: 00:10:28

I think it had a huge chilling effect for a while.
I know that of some people that specifically stepped out of Bitcoin contributions due to this legal precedent or not precedent but like situation.
I think what really helped was that a few people stepped up and just started taking care of it.
Started donating a ton of money and their time and organizing the Bitcoin Defense Legal Fund.
But yeah, it's not necessarily for the faint of heart.

Speaker 0: 00:11:12

Yeah, so what is, I mean, how do you move forward from here?
You mentioned rich people just sort of take care of it.
Is that the solution here, Eva?

Speaker 1: 00:11:22

I mean like traditionally as much as we hate it is that...

Speaker 0: 00:11:26

And by the way you were one of the people that was being sued, right?

Speaker 1: 00:11:31

No, I was not.
Oh. I don't want to get into it.

Speaker 0: 00:11:34

Okay, okay.

Speaker 1: 00:11:36

But I know a bit more about the lawsuit.
But I mean, traditionally in Bitcoin, it is just the rich people are taking care of us.
You see how much money that Jack donates.
And I believe Jack was one of the main people who helped out in the defense fund.
So that is unfortunately how it is currently.
But ideally, people and companies that use Bitcoin, rely on Bitcoin, would contribute monetarily if not, like, I guess for legal stuff definitely contribute monetarily and helping us with lawyers.
It's just unfortunate that that's how it has to be or that's how it is.

Speaker 0: 00:12:23

Okay, last question on the funding.
One of the concerns that some people have is that funding could also influence Bitcoin Core development.

## Funding and Influence in Bitcoin Core Development

Speaker 0: 00:12:32

For example, funding from ETFs could push Bitcoin Core developments in a certain direction.
Is this, in your view, a valid concern?
Shana, do you want to take it?

Speaker 3: 00:12:43

Yeah, so I think that people are generally conscious of not having, like, not employing too many Bitcoin Core developers or one organization giving grants to too many developers or maintainers.
But the thing is that, like, if for example an ETF does fund one Bitcoin Core developer, that doesn't, like, that's, They can't convince them to directly impact anything very big protocol-wise, because then that developer would have to go convince other people as well.
So yeah, I think that it does make sense to be thinking about what could influence a developer.
I think that sometimes the concern is kind of blown up a bit.

Speaker 2: 00:13:27

I would hope that if they make a contract like that, that they very clearly specify in the contract what sort of influence they intend to have on the developer's choice of work items.
Generally, I think if that situation is not very clear and people feel that the developer would be influenced heavily, they might have a harder stance convincing others that their ideas or projects are good or unbiased.
But for the most part, I would say that anyone in the ecosystem that has big impact, pushes around a lot of money, I would be happy if they have some sort of representation to take part in the conversation.
Because it's a two-way street.
If they have some developers that are involved in the development community, they'll learn about the developer concerns and it will flow back to the ETF or exchange or whatever as well.
And if the exchange or ETF has some concerns, those will be heard.
And right now, sometimes it feels that certain areas of the ecosystem are heavily dependent on how everything works, but sort of isolated from the communication.
So I'd actually be for it.

Speaker 0: 00:14:48

Yvan, anything to add?

Speaker 1: 00:14:49

Yeah, I think having a diversity in funding sources is actually really important.
As I mentioned earlier, a lot of funding was kind of coming from Jack in general.
So having more diverse funding so that if Jack gets bored or he gets hit by a bus or whatever, that we aren't suddenly all out of work or, I guess, out of money.
So I think it's fine that for ETFs, mining companies, exchanges, whatever, to have a couple Bitcoin Core developers on their payroll, As long as it's not one, and this applies also to the nonprofits, as long as it's not one organization that has everyone, I think that's fine.

Speaker 0: 00:15:41

So this ties in a little bit.
How hard or easy is it to get new futures in Bitcoin Core currently?

## Bitcoin Core Development vs Protocol Development

Speaker 0: 00:15:52

Some people would argue the bar is too high, Bitcoin doesn't sort of progress, or Bitcoin Core doesn't really progress, it's too hard to get anything new in Bitcoin Core.
Shall we start?
Yeah, Ava, we'll start with you.

Speaker 1: 00:16:03

AVA GILBERT-LUKASIAKOVSKYI Well, it depends on the feature, right?
Like, there are things that don't affect users, that don't affect the rest of the network.
Like, There's a bunch of major-ish back-end changes, for example, the Bitcoin Core Wallet that we've been making.
And these can have a lower and other less impactful changes.
Can still be very important, but have a lower threshold for review.
On the other hand, we have things like consensus.
Consensus changes have a very high threshold, And it's not just the developers who decide consensus changes.
It's the entire community.
And a big part about evaluating consensus changes is seeing whether everyone else in the community, whether there's consensus for it.
What's the name?

Speaker 2: 00:17:01

I think that a lot of people in this context conflate Bitcoin Core development and protocol development.
I think they overlap heavily and traditionally a lot of the changes in protocol development have been proposed by people that were also Bitcoin Core contributors.
But even while there's big overlap, simply because some of the people that have been working on Bitcoin the longest are still contributing to Bitcoin Core, there are separate topics.
And one, like, concerns of what exactly should be in Bitcoin Core are much more driven by the individual contributors whereas of course protocol development is a community conversation.
I am very happy that the BIPS repository is moving a little faster again.
I think that is sort of one of these focal points where we can move stuff and exchange ideas in a comprehensive and comprehensible manner.
The mailing list is live.
Some people lost track of it when it moved.
The mailing list is getting more traffic again.
And so, like these traditional points where that conversation happened are alive and well and maybe should be considered again as points where people keep at least part of that conversation.
Obviously, everybody can talk wherever they want on Twitter, on meetups, at conferences, or whatever.
But please be sure to keep the bigger summaries and the write-ups in a place where we can find them again, where we can index them, where the community will notice that the conversation is happening.

Speaker 0: 00:18:46

Real quick then, you say Bitcoin Core development and protocol development aren't exactly the same thing.
Do you think it's plausible at all that we could see a protocol upgrade happen outside of Bitcoin Core?

## Feasibility of Implementing Futures in Bitcoin Core

Speaker 1: 00:19:00

So,

Speaker 2: 00:19:05

I think it's not impossible.
The ecosystem has grown a ton since we've had a lot of protocol upgrades.
As I said originally, a lot of that overlapped even more because there was just no other game in town at all.
But now there is more different Bitcoin implementations.
There's people that have some concerns that are maybe not championed by Bitcoin Core contributors very well.
So if they were to, say, create an activation client, and it turns out that a huge amount of the community is excited about this and running it, then I don't see why it couldn't happen that someone else is the driver of it.
I would still ask, though, that just so we actually can get a sense of whether there is rough consensus, people actually approach the whole community and some of the places that everybody tends to look at and see is like the mailing list and the BIPs repository.

Speaker 1: 00:20:08

I also want to add like if something if there appears to be community consensus for something there's also a good chance that people who work on Bitcoin Core will also think it's a good idea and want to then implement it in Bitcoin Core.
They may not be the champions of it but that doesn't mean that Bitcoin Core won't have that feature in the future.

Speaker 0: 00:20:31

Ishana, anything to add on getting futures into Bitcoin Core?

Speaker 3: 00:20:36

Yeah, so, well, we just talked a bit about Bitcoin Protocol, but I think in terms of Bitcoin Core especially, it is important and sometimes like newer contributors have to learn to advocate for their own work, to get review.
And in terms of just like reviewing PRs, because that is how features get merged, it's important to be reviewing other people's PRs if you want people to review your own.

Speaker 0: 00:20:58

So it's, yeah, it definitely, I think advocating for your own contributions So there are also people that say Bitcoin should actually ossify as soon as possible Bitcoin core development is maybe even sort of considered a risk in a sense Now this might be a bit of a biased panel in that regard, but I still want to hear your opinion.
So what are your thoughts on ossification?
Is that good, bad, possible, impossible?
Let's go the other way.
Do you want to take it first?
Yeah, Ishana, let's start with you this time.

Speaker 3: 00:21:32

I think it definitely depends on the kind of ossification that you're talking about, because some people are talking about the Bitcoin protocol and some people are talking about Bitcoin Core, and I think that it's important to distinguish the two, because with the Bitcoin protocol, I think, you know, that could be possible.
I haven't looked into exactly what that would mean.
I think that there are unsolved problems, so we might not want to do that just yet.

## Maintaining and Updating Bitcoin Core

Speaker 3: 00:21:56

In terms of Bitcoin Core, it's important to keep maintaining it and I don't know for sure if we'll ever be able to ossify it because we do have to keep making sure we're up to date with dependencies and fixing vulnerabilities and things like that.

Speaker 1: 00:22:12

Ava, anything to add?
Again what Ashana said, with Bitcoin Core itself, it is impossible to not keep making changes to Bitcoin Core because people keep finding bugs.
People keep finding vulnerabilities.
Software, operating systems change, and that necessitates updating Bitcoin core so that it can even like compile and run in the first place.
In terms of protocol, yeah, that could ossify.
There are like time bombs in the protocol though.
Like there are there are things that will stop working in a couple hundred years and those will need to be changed if we want Bitcoin to still work.
So even then the protocol can't really ossify currently.

Speaker 2: 00:23:01

Yeah I feel that often the cry for ossification is a little motivated by concerns about features people don't like or don't understand.
And I don't think that it really, usually it's not the most productive conversation.
I think that in general we are doing pretty well for, let me take that from a different angle.
If you look at how other internet applications have evolved over the last 20 years, we will find other ways in which we want to scale.
If we want to scale to have Bitcoin be usable by the entire population of the planet, we certainly have to make some amendments and changes.
I think we are reasonably conservative and that it is necessary for people to really convince the rest of the community that something is a good idea, but we definitely will need to make more improvements if we want this to actually fulfill the vision that there's digital cash for everyone on the planet.

Speaker 0: 00:24:12

Okay, well this will be the last question.
What are the priorities of Bitcoin, or the priority, or how are these determined?
How does Bitcoin Core maybe differentiate itself from other implementations?
Like what is the focus and the priority of Bitcoin Core?
Let's, Shana, do you want to start?

Speaker 3: 00:24:32

Yeah, so do you mean like of the developers or the project in general?

Speaker 0: 00:24:36

What's the difference?

Speaker 3: 00:24:39

Yeah, well, in terms of just developers, I think that because there's so many, and there's no sort of like, I mean, the whole point is that it's decentralized and anyone can contribute.
So I think that everybody has different priorities.
I think that a lot of people are just trying to, you know, improve things, fix bugs.

## Priorities in Bitcoin Core

Speaker 3: 00:24:58

There are also people who just like show up to the repository and try to get their own stuff merged really quickly and then leave.
But yeah, I think that everybody has different priorities.
So it depends on what your interest is and what sort of changes you want to make.

Speaker 2: 00:25:15

Marc?
Yeah, I think that Bitcoin Core really is different from many other projects in the regard that there is not a founder that has a lot of sway, or sure, there's some members that have been around for, or contributors that have been around for a very long time.
But for the most part, things just organically happen.
Someone has an interesting project, others are also excited about it.
There's maybe a working group, four or five people, and then things start moving.
So if there's important issues, that tends to motivate.
If there's cool new stuff that provides us benefits, that tends to motivate.
We recently introduced priority projects into the Bitcoin Core.
Actually, you should talk about that.

Speaker 1: 00:26:05

Yeah, okay.
I do want to first start out with, it's important to remember that Bitcoin core is not a monolith.
The maintainers are not a monolith.
It's not like everyone thinks the same thing.
There are many differing opinions.
So the priorities are whatever the contributors, every individual contributor, like, wants to happen.
And then they can spend the time, spend time convincing other contributors that their priorities should also match because it's a good idea.
So that is, as Merch just mentioned, this priority project things.
But even then, it's not like things that the entire project prioritizes.
It's things that most people in the project think are good ideas and want to spend time focusing on.
And so this, for the past couple of months, that's been package relay, cluster mempool, and removing the legacy wallet.
But even then, even though these are priorities, not everyone is working on those.
People still do their own things.
They do whatever the hell they want.
And there's just maybe a little bit more focus on that from people, especially people when they find that they have downtime and don't know what else to look at next.

Speaker 0: 00:27:23

Did you have a last word, Murch?

Speaker 2: 00:27:26

I just wanted to clarify.
So the way the project comes up with priority projects is someone proposes that something should be a priority, and then there's a number of other people that are saying, I'll contribute review to that.
And that's why we talk about it in our weekly meeting.
It's not like we've voted and said, oh, we should work on this, or someone decided.
It's just enough people are working on it that it becomes a permanent item on our weekly meeting.

Speaker 0: 00:27:55

Got it.
All right, that's our time.
So everyone, thanks for being here.
Give a hand to our panelists.
And enjoy the rest of the conference.
Thanks for having us.

Speaker 2: 00:28:04

Thank you.

Speaker 3: 00:28:30

You you
