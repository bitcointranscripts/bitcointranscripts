---
title: Onboarding Bitcoin and Lightning Developers
transcript_by: varmur via review.btctranscripts.com
media: https://www.youtube.com/watch?v=-uJSdfo4z7c
tags:
  - bitcoin-core
  - lightning
speakers:
  - Gloria Zhao
  - Will Clark
  - Adam Jonas
  - Jonas Nick
date: 2021-11-16
---
## Introductions

Introducer: 00:00:15

The next talk is going to be Onboarding Bitcoin and Lightning Developers with Will Clark, Gloria Zhao, Josie - Bitcoin Core contributor, Jonas Nick, please come to the stage.

Pablo Fernandez: 00:00:32

Hey, guys, how are you doing?
Welcome.
So we are going to be talking about onboarding Bitcoin and Lightning developers.
Do you guys want to introduce yourselves?
I think all of you have been on stage already, but want to do a quick round?

Will Clark: 00:00:51

I'm Will Clark, I have been doing some work with Global Mesh Labs which is now finished, so I'm not actually doing as my badge says, and I'm working on becoming a Bitcoin Core contributor myself, so I'm in the middle of some of this stuff that we're going to be talking about today.

Jonas Nick: 00:01:10

I'm Jonas, I work at Blockstream in the research group.
I work on various open source projects and also try to bridge Blockstream's research to the academic side.

Adam Jonas: 00:01:26

I'm Adam Jonas, definitely not to be confused with Jonas Nick, who's the real Jonas.
I'm also not Josie, I'm a much shorter version of Josie, and I apologize for those that came out to see him.
I work at Chaincode.
We do education programming, yeah, happy to be here.

Gloria Zhao: 00:01:52

I'm Gloria, I'm a fellow at Brink.
I work on Bitcoin Core.

Pablo Fernandez: 00:01:58

Awesome thanks.
I'm Pablo, I am not a Bitcoin Core contributor, so I think this is interesting because you (Will Clark) are kind of fairly new, right?
You've (Jonas Nick) been around Core for a while, and you've maintained the `libsecp256k1`, right?
That's the cryptographic part of Bitcoin.
You (Adam Jonas) do education with Chaincode.
And you've (Gloria Zhao) been a core (contributor).
How long have you been a core contributor?

Gloria Zhao: 00:02:35

A year and a half.

## What are the motivations and personas of Bitcoin Core or Lightning developers?

Pablo Fernandez: 00:02:36

Yeah, okay, so we have a broad range of expertise.
Fantastic.
I thought that maybe we could start by discussing different (reasons), have you guys observed different interests or reasons why people want to join as contributors?
Different personas if you will, of why people want to become a Core or Lightning developer?
Maybe, Adam?

Adam Jonas: 00:03:05

Sure.
So to sort of set the stage, I think there are three buckets that we think about when we're thinking about developers in general.
There's the open source bucket, and that can be anything from Bitcoin Core to [Mempool Space](https://mempool.space), or anything that's open source that people don't need permission to contribute to.
Then there's the industry piece, which is getting a job and actually working in the industry, and then there is the entrepreneurship piece.
I think people are motivated by different things.
I think we mostly see open source contributors coming from the Western world because they have the luxury of being able to take a break from their job, or something like that.
In terms of participation in industry, that's also pretty relegated to the Western world, but I think we're hoping to change those things.
But the motivation is, I think people want to be involved with contributing to the new monetary system.
I'm sorry I'm not moderating, but why did you get involved, Gloria?

Gloria Zhao: 00:04:19

I think I share a personality trait with a lot of Bitcoiners, which is that I'm very ideologically oriented.
It was very important to me when I was looking for a job that I actually cared about what I was working on.
I think what really put the nail in the coffin for me in Bitcoin was it's fun on a day to day, it's just very interesting.
It didn't take very long after cloning the Bitcoin Core repo, where every day I have two feelings.
One is, oh my god, this is so beautiful, this is everything I was learning about in school.
Then the other feeling is, oh my god, this is disgusting, we need to fix this.
I think that combination is a perfect nerd snipe.
So when I wake up in the morning, I'm really excited to be working on it, and then when I go to bed, I'm like, that was an amazing day.

Pablo Fernandez: 00:05:25

That's beautiful.
(applause)
Yeah, absolutely.
Do you guys see with these different personas, these different archetypes, is the path to get there different?
Or is it the same and it doesn't matter where you're headed, and you just have to go through the same path?
Maybe Adam, Im guessing that you are the most exposed to this.

Adam Jonas: 00:05:53

I don't want to do the most talking though.
Yes, they're very different paths, and we are trying to figure out what a more clear path would be.
We don't do a lot of teaching of code.
In the very beginning, you have to arrive in this ecosystem understanding what code is, because this is very complicated stuff.
I have seen some educational initiatives try to teach coding through Bitcoin, I think you sort of muddle the message.
So for coming into open source, you start with very scalable things, like books, and then you start moving down the chain, moving into things that are more personalized, including Blockstream internships and things like that.
For the industry, the bar is a little bit lower.
You just need to, during your interview, prove that you can do the job.
Then people hire you because they need you to build virtual stuff.
So, yeah, I think there's two different paths.

Pablo Fernandez: 00:07:13

Sounds like a "fake it till you make it" for the industry.
That's the official advice.
Okay, sounds good.

Jonas Nick: 00:07:26

I would like to add one persona, I hinted at it earlier because I think it's also important, and these are PhD students or postdocs who are doing research at universities.
They're developing proof of concepts, or also doing research on the things that we want to eventually develop.
There the path often is that as PhD students they have relatively short term incentives, writing papers and publishing papers and then heading over to the next project.
I think that's why they don't see the value of doing research on Bitcoin at first, they rather would like to explore separate systems.
What I've experienced is that over time, sometimes naturally, because they see, okay, there have been so many things, most of them haven't worked out, Bitcoin is still there, it might make a lot of sense if I focus my career more on Bitcoin.
I think this is another path that is also relatively frequent in the academic world at least.

Adam Jonas: 00:08:42

Do you think that when it comes to academia, Bitcoin has the stage that it should?
As in aren't other projects getting more attention and mind share?

Jonas Nick: 00:09:00

So the thing is that academics don't immediately see the problems that we are interested in as the research problems that they should spend their time on.
I remember being at a conference one time, and a professor asked Peter Wuille - "Why are you interested in these Schnorr signatures and not (in) fixing Bitcoin from the ground up?" - as they perceived it, by moving to Proof-of-Stake.
It was three years ago, but I don't think it has changed much.
I think it is changing, but still there's this general idea that Bitcoin is kind of...
That's it.
It's finalized.
There are some people who do a lot of good research on layer 2s, but I think there's also a lot of potential in this space.

Pablo Fernandez: 00:09:57

Is this the path you took?

Jonas Nick: 00:10:02

No.

## What are the main resources for getting involved?

Pablo Fernandez: 00:10:03

Out of curiosity.
What are some general resources, like the main resources, I'm looking at you (Adam Jonas).

Adam Jonas: 00:10:13

I want to bounce that to Will, because Will is working on some of those resources.

Will Clark: 00:10:19

As Josie alluded to in his talk yesterday, Chaincode have a whole series of fantastic residency and remote learning seminars, which aspiring developers can use to boost their knowledge.
But currently there's still a little bit of a gap, perhaps, between completing one of these seminars and actually getting into the Bitcoin or Lightning implementation code bases, and understanding how they all work, because they're big.
Some parts of them are pretty monolithic still and some things have been broken out.
It's just about teaching these new developers how all of these pieces fit together, and then from there on, where do you start? What should your first pull request be, how do you get involved with the community?
We're trying to work on some resources now specifically to fill that gap between - I know about Bitcoin the protocol, I've got some level of understanding, and now I want to contribute, how do I go?
So hopefully there'll be some more resources on that soon.

Adam Jonas: 00:11:34

I guess another piece would be the PR review club, which John runs.
It's a weekly review club.
It's on IRC.
Everybody reviews the code, and then they show up in IRC and talk about it.
He's been doing it now for two years, two and a half years.
He's taken, I think, two weeks off.
So yeah, it's a very reliable thing to get involved.
It's specifically Bitcoin Core, I don't see that popping up with other projects.
I'm still waiting for the `libsecp256k1` PR Review Club.

Pablo Fernandez: 00:12:08

Good luck.

Adam Jonas: 00:12:09

Working on it, sounds like.

Gloria Zhao: 00:12:15

I recently found out that there's also a Bitcoin Core Dev Wiki, which is not very well known.
I would also shill the Bitcoin Optech newsletter, [bitcoinops.org](https://bitcoinops.org).
And there's some excellent podcasts out there for learning technical materials, such as the Chaincode podcast.
Brink has a Bitcoin development podcast that was just released.
So, I'm just going to put that out there.

Pablo Fernandez: 00:12:47

With regards to the PR review club, how approachable is it?
How far within the code, within how Bitcoin works, how far should you be to be able to go there and learn something?

Gloria Zhao: 00:13:08

Well, it's designed to be accessible for anyone, so beginners.
Typically, we write the notes such that you can have very little background, and there'll be links for resources that you can use.
The questions that we go through, we usually go from surface level or conceptual (to) deeper and deeper.
The best part about the PR Review Club is it's supposed to be a safe space for anyone to ask questions, and there's always very experienced developers in the meeting to answer those questions, but nobody judges anyone for not knowing things.
So to answer your question, you don't need any background, but doing your homework ahead of time helps.

Will Clark: 00:14:03

I would say there's new people in there almost every single week.
So you're not going to be the only new person in there if you want to just jump right in, and people are super friendly.
I highly, highly recommend it as well.

Adam Jonas: 00:14:15

But don't expect to understand everything that's happening your first meeting, because it's just an unrealistic bar.
I remember my first technical meetup, my first BitDevs in New York City, and I just didn't understand nearly anything that they were saying.
It just takes time.
It's like learning a new language.
That fog of understanding will lift over time, but you're gonna have to keep showing, up you have to do the work.

## What are the characteristics of the people that get through to the end of the hero's journey?

Pablo Fernandez: 00:14:44

Can you guys talk a little bit about your experience, what you've seen?
You talked today about the hero's journey, right?
It's a tough process, you start with an idea and you find that it's really hard and intimidating.
What are some of the characteristics of the people that get through to the end of that journey?
Is there an end to that journey?

Adam Jonas: 00:15:11

I mean, they're sitting on the stage.
They're stubborn.
They don't give up.
Like, you just keep showing up.
This is really hard.
To imagine that you're just gonna learn this on first pass, it's not realistic.
So you just have to keep showing up and eventually the fog will lift.
The hero's journey is that you get beaten down every time you learn something new, and then you get back up and you go back and take another shot.

Jonas Nick: 00:15:46

Perhaps (it's) also important to note that the Bitcoin network is a huge thing with many, many different components.
Perhaps it's not the greatest strategy to try to understand everything at the same time very deeply, but rather focus on very specific aspects and then go deeper and deeper on that side and then broaden.
Even Bitcoin Core, that's such a big thing, it's so specialized already that very few people, I would say, understand most of it.

Adam Jonas: 00:16:28

Let curiosity be your guide, find what's something that's interesting that you can dig into and that will motivate you to come back tomorrow.
I think that's really good advice (points to Jonas Nick).
In talking with Will and Gloria going through this process, Gloria was coming out of school and had been working with C++, but you sort of have to relearn C++, or at least learn Bitcoin Core C++ in order to be a valuable contributor.
So you just have to chip away at it from a lot of different angles.
Let me show Gloria for a second.
So, you asked about a characteristic of someone who ends up getting through their hero's journey.
I met Gloria about two years, almost three years ago now.
When she decided that she was going to be a Bitcoin Core contributor, it was just before the summer had started, and she had gotten an internship at Google.
So she's working on an open source project at Google, that's the pinnacle of a college senior, that's what everybody's going for, but she really wanted to work on Bitcoin Core.
So she would wake up at 5 o'clock in the morning, put in her four hours or whatever it might be, and then do her regular day job, and then put in more time on Bitcoin Core, and then go to sleep, wake up, and do the same thing.
She'd do it on the weekends and she just wouldn't stop.
You see someone with that kind of engine and you just know eventually, they're just gonna figure it out, and she did.
We're glad to have her, we're lucky to have her, but that's what it takes. It takes someone with an engine.
(applause)

Pablo Fernandez: 00:18:20

That's beautiful.
What could you guys say is the success rate, I guess?
Like people that start and show some proof of work, they (do) not just show up once on IRC, but they start for real and they actually complete, however you define complete?
Whoever wants to jump on it.

Adam Jonas: 00:18:57

I don't know how you measure that.
I don't know what starting and completing looks like.
I think that this is a journey that never stops.
I've been working with John now for three years and he's still at it.
You're (Jonas Nick) a Bitcoin Core contributor, you're a `libsecp256k` contributor.
The learning never stops, and that's the awesome part about all of this.
I work with Peter Wuille, he never stops.
It doesn't end.
The people who are the most valuable continue to be curious about this space and continue to find problems to solve.
Watching someone like Peter, he needs an entire team to just do the stuff that's in his head.
I think that's what's so great about this, as in you will not get bored.
Ever.
There's no end.
The start is - you just decide that you're going to do it.
Sometimes life gets in the way, sometimes your job's going to get busy, or your friend is going to need you to work on a startup, and people take a break, but the people that end up coming out on the other side always come back.

Jonas Nick: 00:20:29

The failure rate in terms of people who start in Bitcoin and then move to shitcoins at least is relatively low, most of the time it's the other way around.
I think that's a positive note.

Pablo Fernandez: 00:20:41

Is that so?
Developers that were on shitcoins coming into Bitcoin?

Jonas Nick: 00:20:47

It happens, at least in my experience, more often than from Bitcoin to shitcoins.
They're more flexible.

Pablo Fernandez: 00:20:57

Is there any ritual for repentance or something like that?

Jonas Nick: 00:21:03

I don't know.
You don't look in the history of people too much, right?
If you dig too deep, you will always find dirt.

## Malevolent lawsuits and anonymity considerations

Pablo Fernandez: 00:21:06

This is one of the last questions that I had, but I think this is a good segue.
Taking in context what has happened with some guy that claims to be Satoshi and some lawsuits, what would you recommend with regards to protecting yourself as an individual?
What are your thoughts with that?

Will Clark: 00:21:46

We're talking about being a pseudonymous developer, right?
There's definitely some issues with that.
For me personally it seems like a no-brainer that you probably should try to protect your identity.
Those lawsuits you're talking about are particularly nasty.
But Bitcoin and Lightning, I guess, development, as I see it, should be a meritocracy anyway.
Who you are and what you've done before shouldn't necessarily impact whether your changes are likely to be merged, and I think that lends itself quite well to being pseudonymous or fully anonymous.
Obviously there is a few problems with that too.
Possibly it's more difficult to get funding, are you going to be able to get a job at another company without them knowing your details?
That's tough.
But some people have started to get some funding and things like that, so I think it is possible.
If more people did it, then I think that would be a good thing for me as well.

Adam Jonas: 00:22:56

Yeah, it's a one-way door, right?
So you can always start as a pseudonymous name, and you don't have to be some cat picture, you could be what would be a normal name, and so you can sign up for a Github account under John Smith, and that works just fine.
You can always go through that door if you choose to reveal who you are, and I think when it comes to funding it is getting better, but to work for a company, like a US company, they're gonna need to know who you are.
That's how it goes.
We're not quite at a point where you just ship a salary to a Bitcoin address.
I think it's worth trying if you're establishing yourself, because you can just walk through that door later if you choose to.

## What are companies interested in for hires?

Pablo Fernandez: 00:23:55

Awesome.
You've mentioned that Bitcoin Core is really big.
There are a bunch of different aspects, and you don't have to know all the nuances of the mempool and everything that happens.
So what areas of Bitcoin and of Lightning do you guys think that companies that are hiring in this space are most interested in?

Will Clark: 00:24:25

I'm not sure about that, but I did have some other thoughts.
One of the things I would like to see is more Bitcoin first companies, getting some of their developers to use part or full time improving the parts that they're interested in.
I don't know what they are, but I think that's something that could be could be worked on.

Jonas Nick: 00:24:49

At Blockstream I think we're interested in all the various parts that you could think of.
Of course the first step would be someone who's really familiar with just using a wallet.
Then there is this kind of ritual that many Bitcoin devs go through.
You build your own wallet.
Many people do that in various kinds, some people do a wallet on some kind of obscure architecture, others build a VR wallet.
So many people go through that.
Other essential skills at Blockstream - I would say is you know the fundamentals of "how does proof of work work, how could I create a transaction?"
Perhaps not so important knowing it in detail how it works, but just know how to look it up.
Also know how to look it up in the code, where to search for, Bitcoin core is often the reference for many things.
Yeah, I think those are the most important things.

Adam Jonas: 00:25:59

I think what mostly people are hiring for is - people who work on wallets, people who work on trade engines, and now there's a growing economy of Lightning app developers.
It's not a big pool of people that really understand Lightning and understand how to build on top of it, so I think we need to try to fill that funnel with more people.
Overall, there's a lot to build.
Companies are impatient, and they need to fill roles.
So the bar is, I think, a little lower than it should be, which is our job to attract more people, give them the training they need, and then deliver them at the doorsteps of the companies to make them easy hires.

Gloria Zhao: 00:26:44

I'm not a company.
It would be nice if more people come to work on mempool.

Pablo Fernandez: 00:26:53

Maybe you should do an enticing talk about it.
Lightning has some very distinctive properties, right?
We had a bunch of talks about liquidity management.
Do you guys think that that's going to be a field that companies are going to be particularly interested in and how should developers think about it?

Jonas Nick: 00:27:20

I think companies are interested in it.
I think there will be a lot of specialization in this area as well because it's not that easy to do.
It should be easy for normal people to do liquidity management as well.
I think this is certainly also a very interesting and growing area and we're just at the start of this whole thing.
As far as Lightning network, liquidity, routing, these things go, we're just at the start, right?

## What is the most common stumbling block?

Pablo Fernandez: 00:27:56

Going back to what we were talking before, what would you guys say is the most common stumbling block?
Where do people get stuck?

Adam Jonas: 00:28:09

People get stuck everywhere, because life gets in the way, and it's hard, and you feel dumb.
Honestly, if I had to make one place where people get hung up, it's that they feel dumb in front of a group and they're not willing to go through that pain.
I think the PR review club is a good example, creating places where people can feel dumb together.
And that's okay.
You sit up and you share a stage with a guy who's been doing this for a while and understands cryptography, actually, and you feel dumb.
I just sat through the federated Chaumian e-cash, and I was like, I need to really learn what this is.
It takes some humility to be able to get through that process.
Again, you just got to keep showing up and have faith that eventually you'll get it.
Again, I feel like it's very similar to learning a foreign language - I learned a foreign language as an adult in a different country, a different culture, and you feel dumb.
Over time, you start understanding the vocabulary, and then you start understanding some of the context when people say idioms, and then you wake up one day and someone tells a joke in that language and you get it.
Then you realize that it's just a matter of time.

Jonas Nick: 00:29:42

You will, however, always feel dumb most of the time compared to other people, and you will always have imposter syndrome.
It's not me or anything, but many people report that, who have been in the space for a long time and are actually very good developers.
I think you just have to live with it and accept the fact that this exists.

Pablo Fernandez: 00:30:03

Okay, so if you say that, there is no hope for the rest of us, right?

Jonas Nick: 00:30:08

That's not what I'm saying.
I'm just saying that it's not that you wake up the next day and suddenly you think, oh, I'm the best developer and I understand everything about this particular protocol and I'm the only one and the only expert.
This will never happen.
There will always be people where you think that they know more about this than you do.

Adam Jonas: 00:30:33

Yeah, you want people that have that humility working on this project, because otherwise people get cocky and they make mistakes.
You look around at other projects and people get cocky and stuff's gonna break, and if you aren't sort of checking your own mistakes and having humility to think that you don't know everything, then you're not doing the best work.

Will Clark: 00:31:02

I think one of the other areas is where do you start?
What do you do as your first move?
How do you get over the starting line?
Definitely one, not the only way, but one good way to do this, which also happens to be one of the main bottlenecks in a lot of these projects, is get involved with reviewing pull requests.
Developers often have this desire to create new code, you want to write new features and get your satisfaction from implementing something, but you can learn a lot from doing reviews.
You often gain a little bit of context into that specific area.
Why are these changes being made?
Why was it originally like this and why are we changing it?
That burden of review is often cited as a sort of blocker for those experienced people to get on with doing what they want to do.
I just think it's a really good way to learn.

## What can developers keep in mind as their guiding star?

Pablo Fernandez: 00:32:00

So basically, "I just heard of Bitcoin, I'm here to fix it".
Getting over that, right?
So we've been talking a lot about how hard it is, how painful it is, how humbling it is.
Developers that are thinking about starting, or have started, they are in the midst of it, what can they keep in their mind as their guiding star?
What should they keep in mind?
You've got this, Gloria?

Gloria Zhao: 00:32:42

I think you (Jonas Nick) should answer this question.

Jonas Nick: 00:32:48

I don't have a good answer to this question, because I don't have anything in particular in mind when doing this.
Perhaps one thing I have in mind is the long-term outlook on this thing.
This is going to be around for a long time so it makes sense to invest your time in it, and it changes people's lives.
Perhaps not directly, it's a very indirect way of course, to influence things, but I think the chances are good that it works.

Will Clark: 00:33:24

Yeah, and I think coming back to what Jonah said earlier, most Bitcoiners I talk to are just super interested in Bitcoin personally, they want to think about it all the time.
You're weaving it into conversation.
You want to work on it.
I don't know, perhaps if you've got a desire to keep learning about it continuously then I think it'll be good.
Like Jonah says, keep putting the work in, and you'll get there.

Gloria Zhao: 00:33:54

OK.
I think it's about imagining the type of world that you want to live in, and recognizing that it's not going to happen unless you make it happen.
I want to live in a world where anyone can pay anyone, where big banks and companies and governments cannot just arbitrarily censor people.
I want to live in a world where when you like something that someone creates, you pay them directly with money, instead of waiting for an intermediary to come in and seek rent from both of you.
We don't want to wait for someone to build that for us.

Jonas Nick: 00:34:42

Another guiding principle now that I'm just thinking about it.
At some point you will take responsibility.
For example in the open source world, and also in the job of course, it means doing a lot of things in your spare time that you probably don't want to do.
So I think, one of the key things that many developers are also really, really driven by is just the sense of duty, right?
That's their part of the code, they want to improve it, they see other people's pull requests, they need to review it.
There are a lot of things that when you start working in this space, and you have this kind of idealistic outlook, perhaps, that you really want to make this work, and you get this sense of duty.

Adam Jonas: 00:35:40

Why did we all fly down here?
Like, this isn't convenient to be here.
Yet, we're all here because it's meaningful, and it's impactful, and we want to make big change.
So, the ability to contribute to that as a builder, is there anything better than that on the planet?
The way that Gloria described, where she wakes up every day excited to go to work, and goes to sleep every day feeling like she had a meaningful day?
What else could you ask for?
(applause)

## How should companies approach developers?

Pablo Fernandez: 00:36:26

I'm guessing most of you, like myself, get a bunch of spam from recruiters with horrible pitches.
How do you guys think that companies in this space, or (companies) that want to launch a project in this space, should approach developers in a way that is meaningful for them?

Jonas Nick: 00:36:55

The Blockstream approach to this, which is apparently working, is to build this kind of image of being a cypherpunk company whose future is completely aligned with Bitcoin's future, and also who's investing a lot in open source projects.
And that on the other hand attracts a lot of people who start contributing in their spare time, or who see Blockstream as something that they would want to work at.
I think this is something that really helps Blockstream right now to get applicants for the job postings.

Adam Jonas: 00:37:54

So I do quite a bit of recruiting, but it's mostly for open source developers, not to necessarily work at Chaincode, but just to work on the project, Bitcoin Core related technology protocol stuff.
The way I reach out is mostly because someone has already shown interest, as in someone has already made the first move, and you just offer help.
Like, how can we be helpful?
Now, Chaincode is a little bit different, and I think a little bit unique, but something I've started to do when recruiters send me emails is I take the call, and then one of the first questions I ask is "what are you doing for the ecosystem?"
I've had some meaningful conversations with recruiters trying to help them understand that their approach is a waste of their time, if they're actually looking for the kind of people that they want to hire, and if they went about it in a way where they actually were helping the ecosystem as opposed to trying to extract from the ecosystem, that they'd be more successful.
So if you're a company and you have a budget for recruiting, you probably have a budget to work on open source or something like that.
So take your marketing budget and put it towards something that will actually make things better, please.

## What to expect going into open source development?

Pablo Fernandez: 00:39:26

I've done a lot of open source development myself, and I've worked for companies.
The way open source development works, it's very different than how working in a company feels like, and how the approach to everything is like.
Can you guys talk a little bit about how someone that has worked within (and) for companies their whole life, what to expect going into open source development?

Adam Jonas: 00:40:17

It's different in that oftentimes no one's telling you what to do.
That's the big change.
When you work for a company, there's a hierarchy and a structure.
You get orders from on high, business makes decisions, and then that gets filtered down through layers, and eventually it reaches the front line developer, who is told it's broken up into smaller features, and they go and implement it.
People who work in open source scratch their own itch.
Oftentimes, there's not that kind of coordination.
So you go after the things that are important to you, you go after the things that are meaningful to you, and that can feel very scary when no one's telling you what to do, because you don't know what to do.
So we actually have examples of people working in open source and deciding that they wanted to go work in a company because they didn't feel comfortable in that murkiness of feeling like they were (un)productive.
The shipper's high that you get from shipping a feature and the CTO celebrating that with you, you don't really feel that in the same sort of way.
So open source may not be right for you.
That's OK.
You can still contribute to the space in meaningful ways.
But you may not like taking orders, too, and so maybe open source is a better fit for you.
I think it comes down to your personality and comes down to your mindset.

## Audience Questions

Pablo Fernandez: 00:42:03

I thought about leaving some time for questions from the audience.
So if you guys want to talk about something before we open for questions, something we didn't touch on?
Yeah, good.

Audience 1: 00:42:29

Hello, awesome panel.
Two questions.
One is for the whole group.
What are some good milestones that people can aim for when they're onboarding, both early ones and later milestones?

Gloria Zhao: 00:42:52

For me it was the day when I was wondering how something worked in Bitcoin, and instead of going on Stack Exchange or Googling, I just look for it in the code.
After hitting that, it's just full speed ahead, because you never need anyone to learn.

Audience 2: 00:43:21

So you talk about the hero's journey and you folks, you've taken the hero's journey.
I mean, I see it and I know it.
What about for normal people?
I'm glad you're doing it, I'm glad you're cultivating those heroes, I'm so glad you are.
But there's a whole lot of other folks who are not going to be able to take that journey because of where they are in life, because of whatever, but we need them.
I don't know whether it's, like maybe we're just not the product, the ecosystem is not mature enough yet to be able to take advantage of the normal folks?
Or is it that we need to pivot the ecosystem to make it be more accessible, so we can use us normal folks.
Does that make sense?

Adam Jonas: 00:44:25

That's a great question.
Will, go ahead.

Will Clark: 00:44:27

Yeah, certainly for Bitcoin Core and some of the other projects, I think it's a misconception that it's all super technical, and you need to be incredibly specialized and incredibly good at something to contribute, but it's not the case.
There's a ton of work that needs to be done that doesn't require you to be a cryptography expert or a mempool expert.
So I think there's stuff for everyone to jump into, really, and it's just about getting a journey started and getting involved.

Adam Jonas: 00:45:06

Everyone's a hero.
I can't code for beans.
I am not good at developing.
So I've chosen a different path because that's how I can contribute.
So you have to find what you're good at, and what you're excited about, and how you can position yourself to make meaningful contributions.
There is no hero here.
I mean, these people (rest of the panel) are heroes.
But I promise you, I'm no hero.
How do you take advantage of that?
You find a way that you're excited about to contribute.
That's it.
I'm happy to talk to you about who you are and how do you contribute.

Audience 2: 00:46:02

I'm not just thinking about myself, but I'm using myself as an example.
There are folks out there that we need that are never going to get passionate, right?

Adam Jonas: 00:46:13

Oh, yeah.
I don't want those people.

Audience 2: 00:46:16

But we need them.

Adam Jonas: 00:46:17

No, no, no, I don't think we do.
I really disagree with you.
I think what's exciting about this space is that we just flew thousands of miles to come to a country because they made a Bitcoin law.
That's what we need.
One of those people can do 10 times the work of someone who's just clocking in.
You don't need to be a hero, you just need to be excited and you really do the work.

Audience 2: 00:46:50

Are you saying that because that's where we are right now in the ecosystem, in the environment?

Adam Jonas: 00:46:59

No I think if you compromise on that, then you dilute what you're doing.
You dilute why you're doing it.
And it's okay.
You can dilute it to a certain extent.
If you're building a big company, and that's your goal, to build a big company, that's different than building a company to push Bitcoin and Lightning forward.
So if you're doing that, then you need to find people who care about what you're doing.

Audience 2: 00:47:27

I'm again thinking like traditional banking system, right?
I mean, way back when, at some point in time, somebody was really passionate about fractional reserve banking, and they went crazy, and now it's normal, and thousands of people go to JPMorgan Chase every day and work on whatever they work on.
I mean, don't we want Bitcoin to be like that, where it's just normal?
It's normal and that keeps it going?

Adam Jonas: 00:47:55

I don't.
It's OK.
I think it's OK to want that, but I don't want that, because I don't want to work with people who aren't excited.
I don't want to work with people who clock in.
By the time Bitcoin gets there, hopefully nobody has to work on the planet at all.
We've figured out how to have a society where you have so much surplus, you don't need to work.
But that's not meaningful.
That doesn't bring meaning to your life if you don't care about what you do.

Audience 2: 00:48:25

No, no.
You can have other things that you find meaningful in life and a job is a means to get income for you to do the meaningful thing in your life.
There's nothing wrong with that.
That's not me, but there's nothing wrong with those people.
We need those people to do the drudge work, whatever, to integrate it in with the cash registers, whatever.
We need those people.

Adam Jonas: 00:48:53

I just disagree.
It's OK.

Audience 1: 00:48:58

Can I ask my second question now?
(The) second question is, how can someone who didn't do a PhD get involved with the research side?

Jonas Nick: 00:49:12

I don't have a PhD and I'm on the research side.
How does it work?
How did it work was basically working with the right people, right?
You need to be in the right group and you need to learn from people, you need to find someone who is willing to teach you, who is willing to spend time with you.
You need to be willing to learn and then it just takes time.
I learned all the things from other people, who really took the time to do that, who knew more in this specific area than I did.
Especially in the field of cryptography, I didn't have the formal training that other people do, for example, to do stuff like music, but somehow I was able to pick it up just from other people who were willing to teach me.
(applause)

Audience 3: 00:50:09

So you've been talking about onboarding, you obviously all care about getting more developers into the Bitcoin and Lightning ecosystem.
I'd be curious, for the four of you, what does success look like in two or three years time?
What does the Bitcoin and Lightning developer ecosystem look like?

Adam Jonas: 00:50:45

I don't have a snappy answer.
We are at a point where we are just so desperately looking for people that are willing to do the work, that it consumes me.
In two to three years time, I hope that, and it is happening, I think you find people who are attracted to this kind of work and they start doing it themselves.
But success looks like that the community has taken this over, and there's a flywheel effect, where people who go through and someone helps them, they then help the next group, and that group gets larger and larger.
So success in two to three years looks like - there's just a big base of teachers and mentors and a whole decentralized onboarding path for your local community.
Wherever you are, we have filled enough gaps, where we are providing clear paths for people to onboard into this ecosystem.

Jonas Nick: 00:52:15

To add to that, I think we don't only want people who are super motivated, great developers, etc.
We also want people who are philosophically aligned.
I think for success it is also very important that we are able to teach the values of Bitcoin, permissionless, decentralized, money for everyone, to the next generation of developers as well.

Adam Jonas: 00:52:49

That's a better answer.

Audience 4: 00:52:52

I have a question.
A suggestion first, and then a question.
I'm coming from another open source project, I'm into web development.
I've been in the Drupal content management ecosystem.
I've been there through the years and seen the transformation that's done in that project.
One of the most important things I saw happen was one year they decided to work on what they called developer experience.
It's how to get people to work on Drupal core, and get more people from off the street, so to speak, working on it.
One thing that they did, for the PRs and the patches to core, what they did, they assigned them with difficulty.
So it allowed newbies to come in and say, "Okay I'm seeing a bunch of PRs here. Which ones are within the range of my abilities?"
That helped a whole lot because it allowed people to come in and say "Okay, I can perhaps start on these smaller ones first".
It kind of adds to his point where it creates stair steps for people who are not necessarily passionate.
I think passion can begin in two ways.
There are people who come in passionate, you grew up around computers or something, and you just have passion for things technical.
Then the other people who learn passion, you do something and you realize it works, and then you do something else and you realize it works, you step up the stairs until you're really passionate about something.
So I think improving the developer experience by creating those stair steps for new developers to come in.
I was really interested in Bitcoin I'm the type of guy who comes in with high passion, right?
But even coming in with high passion, I was trying to figure out - so how do I get started?
I asked people on Twitter, what projects are there to get worked on, and people were like, "Well I don't know, just kind of get started, right?"
It was kind of difficult for me, because I wanted to know what projects needed help, as a newbie, where could I go and get started?
It was kind of difficult.
So working on a kind of stair-stepped method to get into developer experiences is perhaps something that you can work on for the future, to make it easier for people to onboard as developers.
Secondly, again from the Drupal ecosystem, the companies that are running Drupal in their businesses, they also contribute to the community.
So there are a lot of bounties and things that allow people to have motivation to work on these projects.
I'm in the Caribbean, and most of the guys around me, they're not going to work on open source projects because a lot of them just want to get food.
They don't have the free time to go and work on stuff, right, and you just want something so you can pay your bills or whatever.
After you start making good money as a developer or whatever, then you have the spare time to start working on open source projects and so on.
But if there are bounties, bounties could be a thousand sats, it is a kind of motivation to allow people to get started.
There might be bigger problems, with larger bounties.
So companies who are working and benefiting, Blockstream or whoever, could perhaps set bounties on different issues, and tell the developer community about these issues and have them work on it as well.
So, just two suggestions I have.

Audience 5: 00:56:49

So, I wanted to pick up one of my neighbors and what they're saying about the heroes and stuff.
I read Onboarding Bitcoin and Lightning developers, not Bitcoin Core developers.
I think it's pretty dangerous to idolize Bitcoin Core and Lightning and all the super hard things, because there's so many super small projects where one or two people are working on, and I think the people that work in those projects would be way more passionate to teach new people to work with them on their very small projects.
They're usually way lower barrier to entry, and I think it would be really great if there's more resources for people to find those smaller projects and not want to work on Core, or want to work on Lightning.
Because those projects are freaking hard, and most developers will never work on them or don't have to work on them because it's hard.
So maybe a mailing list, or a newsletter, where smaller projects can announce new things that they built - or something like that where then you can look at (these).
Yeah, smaller projects, web projects, point of sale projects, hardware projects, like smaller things.
Lower barrier of entry.

Gloria Zhao: 00:58:06

Some of us have a personality trait where when we see something that's not quite right, there's a typo or something, we're like, I wish I could open a PR to fix that.
Like a broken lamp or something.
If you have this personality trait, pretty much everything in Bitcoin is open, or there's a lot of open source Bitcoin projects, and a lot of them are, like Stephen said, not Bitcoin Core.
(It's) not going to cause (the) Bitcoin network to die if you make a mistake, so if you have this personality trait, I think you'll be surprised by how many places are welcoming contributions.

Pablo Fernandez: 00:58:56

Okay, I think that's time.
So if we don't have any more questions, we'll wrap it up.
All right, thanks guys.
