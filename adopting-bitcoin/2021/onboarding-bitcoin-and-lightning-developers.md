---
title: "Onboarding Bitcoin and Lightning Developers"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://www.youtube.com/watch?v=-uJSdfo4z7c
tags: ['bitcoin-core', 'lightning']
speakers: ['Gloria Zhao', 'Will Clark', 'Adam Jonas', 'Jonas Nick']
categories: ['conference']
date: 2021-11-16
---
## Onboarding Bitcoin and Lightning Developers

Speaker 0: 00:00:15

Okay, so the next talk is going to be onboarding Bitcoin and Lightning developers with Will Clark, Gloria Zhao.
This is Josie, Bitcoin Core contributor.
Jonas, Nick.
Please come to the stage.

Speaker 1: 00:00:32

One mic short.
Hey, guys.
How are you doing?
Welcome.
So we are going to be talking about that onboarding Bitcoin and Lightning developers.
Do you guys want to introduce yourself?
I think all of you have been on stage already, but want to do a quick round?

Speaker 2: 00:00:51

So I'm Will Clark, I have been doing some work with Global Mesh Labs which is now finished, so I'm not actually doing as my badge says, and I'm working on sort of becoming a Bitcoin core contributor myself, so I'm in the middle of some of this stuff that we're going to be talking about today.

Speaker 3: 00:01:10

I'm Jonas, I work at Blockstream in the research group.
I work on various open source projects and also kind of try to bridge blockstreams to research to the academic side.

Speaker 4: 00:01:26

I'm Adam Jonas.
Definitely not to be confused with Jonas Nick, who's the real Jonas.
I'm also not Josie.
I'm a much shorter version of Josie, and I apologize for those that came out to see him.
I work at Chaincode.
We do education programming.
And yeah, happy to be here.

Speaker 0: 00:01:52

I'm Gloria.
I'm a fellow at Brink.
I work on Bitcoin Core.

Speaker 1: 00:01:58

Awesome thanks.
So we've have and I'm Pablo I am not a Bitcoin Core contributor, so I think this is interesting because you are kind of fairly new, right?
You've been around Core for a while, and you've maintained the SEC P256K1, right?
So that's like the cryptographic part of Bitcoin.
You do education and you've been a core, well, education with chain code, I mean.
And you've been, how long Have you been a core contributor?

Speaker 5: 00:02:35

A year and a half.

Speaker 1: 00:02:36

Yeah, okay.
So we have like a broad range of expertise.
Fantastic.
I thought that maybe we could start by discussing like different, have you guys observed different interests or reasons why people want to join as contributors like why different personas if you will of why people want to become a core or lightning developer?
Maybe, Adam?

Speaker 4: 00:03:05

Sure.
So I think, to sort of set the stage, I think there are three buckets that we think about when we're thinking about developers in general.
So there's the open source bucket.
And that can be anything from Bitcoin Core to Mempool Space or anything that's sort of open source that people don't need permission to contribute to.
Then there's the industry piece, which is getting a job and actually working in the industry.
And then there is the entrepreneurship piece.
So I think people are motivated by different things.
There are some people, I think we mostly see open source contributors coming from the Western world because they have the luxury of being able to take a break from their job or something like that.
And in terms of participation in industry, that's also pretty relegated to the Western world.
But I think we're hoping to change those things.
But the motivation is very, I think people want to be involved with contributing to the new monetary system.
So. Why did, I'm sorry, I'm not moderating, But why did you get involved, Gloria?

Speaker 0: 00:04:19

I think I share a personality trait with a lot of Bitcoiners, which is that I'm very ideologically oriented.
So it was very important to me when I was looking for a job that I actually cared about what I was working on.
But I think what really put the nail in the coffin for me in Bitcoin was it's fun on a day to day.
It's just very interesting.
It wasn't it didn't take very long after like cloning the Bitcoin core repo, where like every day I have two feelings.
One is, oh my god, this is so beautiful, like this is everything I was learning about in school.
And then the other feeling is, oh my god, this is disgusting, we need to fix this.
I think that combination is a perfect nerd snipe.
So, you know, when I wake up in the morning, I'm really excited to be working on it.
And then when I go to bed, I'm like, that was an amazing day.
So.

Speaker 1: 00:05:25

That's beautiful.
Yeah, absolutely.
And Do you guys see with these different persona, these different archetypes, is there a path to get there different?
Or is it the same and it doesn't matter where you're headed and you just have to go through the same path?

Speaker 4: 00:05:53

Maybe Adam, I'm guessing that you are the most I don't want to do the most talking though yes, they're very different paths And I think we are trying to figure out what a more clear path would be.
So I think we don't do a lot of teaching of code.
Like in the very beginning, You sort of have to arrive in this ecosystem understanding what code is, because this is very complicated stuff.
And so I have seen some educational initiatives try to teach coding through Bitcoin.
I think you sort of muddle the message.
And so for coming into open source, like you start with very scalable things like books.
And then you start moving down the chain on moving into things that are more personalized, including like Blockstream internships and things like that.
For the industry, the bar is a little bit lower.
You just need to sort of prove or at least talk during your interview, prove that you can do the job.
And then people hire you because they need you to build virtual stuff.
So, yeah, I think there's two different paths.

Speaker 1: 00:07:13

Sounds like a fake it till you make it for the industry.
That's the official advice.
Okay, sounds good.
Yeah, go ahead.

Speaker 3: 00:07:26

I would like to add one persona, which is, I hinted at it earlier, because I think it's also important and these are PhD students or postdocs who are doing research at universities, they're developing proof of concepts or also doing research on the things that we want to eventually develop.
And there the path often is that as PhD students they have relatively short term incentives, writing papers and publishing papers and then heading over to the next project.
And I think that's why they don't see the value of doing research on Bitcoin at first.
They rather would like to explore separate systems.
And what I've experienced is that over time, sometimes naturally, because they see, okay, there have been so many things, most of them haven't worked out Bitcoin is still there It might make a lot of sense if I focus my career more on Bitcoin.
I think this is another path that is also relatively frequent in the academic world.

Speaker 4: 00:08:42

Do you think that when it comes to academia, Bitcoin has the stage that it should as in aren't other projects getting more attention and mindshare?

Speaker 3: 00:09:00

So the thing is that academics don't immediately see the problems that we are interested in as the research problems that they should spend their time on.
Like, I remember being at a conference one time and a professor asked Peter Weller, why are you interested in these Schnorr signatures and not like fixing Bitcoin from the ground up as they perceived it by moving to proof of stake?
Right.
So that's just the thing that isn't really, I mean, back then it was three years ago, but I don't think it has changed much.
I think it is changing, but still there's this general idea that Bitcoin is kind of...
That's it.
It's finalized.
There are some people who do a lot of good research on layer 2s, but I think there's also a lot of potential in this space.

Speaker 1: 00:09:57

Is this the path you took?
No. Out of curiosity.
What are some general resources, like the main resources I'm looking at?

Speaker 4: 00:10:13

I want to pass that to Will, because Will is working on some of those resources.

Speaker 2: 00:10:19

Yeah, well, as Josie alluded to in his talk yesterday, Chaincode have a whole series of fantastic residency and remote learning seminars, which people can, aspiring developers can use to boost their knowledge.
But currently there's still a little bit of a gap perhaps between completing one of these seminars and actually getting into the Bitcoin or some of these lightning implementation code bases and understanding how they all work because they're big.
Some parts of them are pretty monolithic still and some things have been broken out.
And it's just about teaching these new developers how all of these pieces fit together and then from there on you know where do you where do you start what should your first pull request be how do you get involved with the community and yeah we're trying to work on some resources now specifically to fill that gap between, you know, I know about Bitcoin the protocol, I've got some level of understanding and now I want to contribute, how do I go?
So hopefully there'll be some more resources on that soon.

## PR Review Club

Speaker 4: 00:11:34

I guess another piece would be the PR review club, which John runs.
It's a weekly review club.
It's on IRC.
Everybody reviews the code, and then they show up in IRC and talk about it.
And he's been doing it now for two years, two and a half years.
He's taken, I think, two weeks off.
So yeah, it's a very reliable thing to get involved.
It's specifically Bitcoin Core.
I don't see that popping up with other projects.
I'm still waiting for the SecP256K1 PR Review Club.
Good luck.
Working on it, sounds like.

Speaker 0: 00:12:15

I recently found out that there's also a Bitcoin Core Dev Wiki, which is, I guess, not very well known.
I would also show the Bitcoin OpTec newsletter, bitcoinops.org.
And there's some excellent podcasts out there for learning technical materials, such as the Chain Code podcast.
Brink has a Bitcoin development podcast that was just released.
So, I'm just going to put that out there.

Speaker 1: 00:12:47

With regards to the PR review club, you said, how approachable is it?
How far within the code, within how Bitcoin works, how far should you be to be able to go there and learn something?

Speaker 0: 00:13:08

Well, it's designed to be accessible for anyone, so beginners.
Typically, we write the notes such that you can have very little background and there'll be links for resources that you can use and the questions that we go through we usually go from like surface level or conceptual like deeper and deeper.
I think the biggest, like, the best part about the PR Review Club is it's supposed to be a safe space for anyone to ask questions.
And there's always very experienced developers in the meeting to answer those questions.
But nobody judges anyone for not knowing things.
So to answer your question, you don't need any background.
But doing your homework ahead of time helps.

Speaker 2: 00:14:03

I would say there's new people in there almost every single week.
So, you know, that's, you're not going to be the only new person in there if you want to just jump right in.
And people are super friendly.
I highly, highly recommend it as well.

Speaker 4: 00:14:15

But don't expect to understand everything that's happening your first meeting.
Because it's just an unrealistic bar.
If you've I remember my first technical meetup, my first Bitnevs in New York City, and I just didn't understand nearly anything that they were saying.
And it just takes time.
It's like learning a new language.
And so that fog of understanding will lift over time but you're gonna have to keep showing up you have to do the work so can you Can you guys talk a little bit about your experience, what you've seen, what are the...

Speaker 1: 00:14:51

You talked today about the hero's journey, right?
It's a tough process, so you start with an idea and you find that it's really hard and intimidating.
What are some of the characteristics of the people that get through to the end of that journey?
Is there an end to that journey?

Speaker 4: 00:15:11

I mean, they're sitting on the stage.
They're stubborn.
They don't give up.
Like, you just keep showing up.
This is really hard.
I mean, to imagine that you're just gonna learn this the first on first pass, like it's not realistic.
So You just have to keep showing up and eventually the fog will lift.
The hero's journey is that you get beaten down every time you learn something new.
Then you get back up and you go back and take another shot.

Speaker 3: 00:15:46

Perhaps also important to note that the Bitcoin network is a huge thing with many, many different components.
And perhaps it's not the greatest strategy to try to understand everything at the same time very deeply, but rather focus on very specific aspects and then go deeper and deeper on that side and then broaden your things.
But Bitcoin, even Bitcoin Core, that's such a big thing, it's so specialized already that very few people, I would say, understand most of it.

Speaker 4: 00:16:28

So let curiosity be your guide, like find what's something that's interesting that you can dig into and that will motivate you to come back tomorrow.
And so yeah, you just, I think that's really good advice.
Or, you know, in talking with Will and Gloria going through this process, like, you know, Gloria was coming out of school and had been working with C++, but you sort of have to relearn C++ or at least learn Bitcoin Core C++ in order to be, you know, a valuable contributor.
And so you just have to chip away at it from a lot of different angles.
She was reading, let me show Gloria for a second.
So, you asked about a characteristic of someone who ends up getting through their hero's journey.
And I met Gloria about two years, almost three years ago now.
And when she decided that she was going to be a Bitcoin Core contributor, it was just before the summer had started.
And she had gotten an internship at Google.
So she's working on an open source project at Google.
That's the pinnacle of a college senior Like that's that's what everybody's going for but she really wanted to work on Bitcoin core So she would wake up at 5 o'clock in the morning put in her, you know hours her her four hours or whatever it might be, and then do her regular day job, and then put in more time on Bitcoin Core, and then go to sleep, wake up, and do the same thing.
And she'd do it on the weekends and she just wouldn't stop and you see someone with that kind of engine and you just know eventually, they're just gonna figure it out and She did and we're glad to have her we're lucky to have her and but that's what it takes It takes someone with an engine.

Speaker 1: 00:18:20

That's beautiful.
What could you guys say is the success rate, I guess?
Like people that start and show some proof of work, like they not just show up once on IRC, but they start for real and they actually complete.
Like, whatever, how are you define complete?
Whoever wants to jump on it.
So that's a zero, okay.

Speaker 4: 00:18:57

All right, next question.
I don't know how you measure that.
I don't know what starting and completing looks like.
You know, I think that this is a journey that never stops.
I've been working with John now for three years and he's still at it.
You're a Bitcoin Core contributor.
You're a SECP256K contributor.
The learning never stops.
And that's the awesome part about all of this.
Like you just, I mean I work with Peter Wella, like he never stops.
It's, it's, it doesn't end And the people who are the most valuable continue to be curious about this space and continue to find problems to solve.
And watching someone like Peter, he needs an entire team to just do the stuff that's in his head.
And you know, I think it, that's what's so great about this, as in you will not get bored ever.
But there's no end.
And the start is you just decide that you're going to do it.
And sometimes life gets in the way.
Sometimes you're going to have your job's going to get busy, or your friend is going to need you to work on a startup and people take a break.
But the people that end up coming out on the other side always come back.

Speaker 3: 00:20:29

The failure rate in terms of people who start in Bitcoin and then move to shitcoins at least is relatively low.
Most of the time it's the other way around.
I think that's a positive note.

Speaker 1: 00:20:41

Is that so?
Is that developers that were on shitcoins coming into Bitcoin?

Speaker 3: 00:20:47

It happens, I guess, at least in my experience more often than from Bitcoin to shit coins.
They're more flexible.

Speaker 1: 00:20:57

Is there any ritual for like repent or something like that?

Speaker 3: 00:21:03

I don't know.
You don't look in the history of people, right?

Speaker 1: 00:21:06

Too much.
If you dig too deep, you will always find dirt.
Actually, this is a good jumping board.
It's one of the last questions that I had, but I think this is a good segue.
How do you guys feel and what would you recommend for taking in context what has happened with some guy that claims to be Satoshi and some lawsuits.
What would you recommend with regards to protecting yourself as an individual?
What are your thoughts with that?

Speaker 2: 00:21:46

I mean we're talking about being a pseudonymous developer right.
I mean there's definitely some issues with that.
I think for me personally it seems like a no-brainer that you probably should try to protect your identity.
I mean those lawsuits you're talking about are particularly nasty.
But Bitcoin and Lightning, I guess, development, as I see it, should be a meritocracy anyway.
Who you are and what you've done before shouldn't necessarily impact whether your changes are going to likely to be merged.
And I think that lends itself quite well to being sued anonymous or fully anonymous.
Obviously there is a few problems with that too.
Possibly it's more difficult to get funding or, you know, are you going to be able to get a job at another company without them knowing your details?
That's tough.
But some people have started to get some funding and things like that.
So I think it is possible.
And if more people did it, then I think that would be a good thing for me as well.

Speaker 4: 00:22:56

Yeah, I think it's a one-way door, right?
So you can always start as a pseudonymous name.
And you don't have to be you know some cat picture you could be what would be a normal name and so yeah just you can sign up for a get up account under John Smith and that works just fine So trying to think you know you can always go back like you can always go through that door if you choose to reveal who you are and I think when it comes to funding it is getting better but to work for a company like a US company they're gonna need to know who you are like that's how it goes We're not quite at a point where, you know, you just sort of ship a salary to a Bitcoin address.
So I think it's worth trying if you're establishing yourself, because you can just walk through that door later if you choose to.

Speaker 6: 00:23:55

Awesome.

Speaker 1: 00:23:58

You've mentioned that Bitcoin core is really big.
There are a bunch of different aspects and you don't have to know all the nuances of the mempool and everything that happens.
So what areas of Bitcoin and of Lightning Do you guys think that companies that are hiring in this space are most interested in?

Speaker 2: 00:24:25

I'm not sure about that, but I did have some other thoughts that it's one of the things I would like to see is more Bitcoin first companies, you know, getting some of their developers to use part or full time improving the parts that they're interested in.
So I don't know what they are, but you know, I think that's something that could be could be worked on.

Speaker 3: 00:24:49

At Blockstream I think we're interested in all the various parts that you could think of.
Of course the first step would be someone who's really familiar with just using a wallet.
Then there is this kind of ritual that many Bitcoin devs go through.
You build your own wallet.
Many people do that in various kinds.
Some people do a wallet on some kind of obscure architecture, others build a VR wallet.
So many people go through that.
I think what else would perhaps other essential skills perhaps is that you just know how to at Blockstream, I would say is like the fundamentals of how does proof of work work, how could I create a transaction.
Perhaps not so important like knowing it in detail how it works, but just look, know how to look it up.
Also know how to look it up in the code where to search for Bitcoin core is often the reference for many things.
Yeah, I think those are the most important things.

Speaker 4: 00:25:59

I think What mostly people are hiring for is people who work on wallets, people who work on trade engines and now there's like a growing economy of lightning app developers.
But it's not a big pool of people that really understand lightning and understand how to build on top of it.
So I think we need to sort of address what the, try to fill that funnel with more people.
But overall, there's a lot to build.
And people, companies are impatient, and they need to fill roles.
And so the bar is, I think, a little lower than it should be, which is our job to attract more people, give them the training they need, and then deliver them at the doorsteps of the companies to make them easy hires.

Speaker 0: 00:26:44

I'm Not a company.
It would be nice if more people come to work on Mempool.

Speaker 1: 00:26:53

Maybe you should do an enticing talk about it.
Do you guys think that, because Lightning has some very distinctive properties, right?
So we had a bunch of talks about liquidity management.
Do you guys think that that's going to be a field that companies are going to be particularly interested in and how should developers think about it?

Speaker 3: 00:27:20

I think companies are interested in it.
I think there will be a lot of specialization in this area as well because it's not that easy to do.
It should be easy for normal people to do, liquidity management as well.
So I think this is certainly also a very interesting and growing area and we're just at the start of this whole thing I think.
That as far as lightning network, liquidity, routing, these things go, we're just at the start, right?

Speaker 1: 00:27:56

Going back to what we were talking before, what would you guys say is the most common stumbling block?
Like, where do people get stuck?

Speaker 4: 00:28:09

People get stuck everywhere, because life gets in the way, and it's hard, and you feel dumb.
Like, honestly, that's the biggest.
If I had to make one place where people get hung up, it's that they feel dumb in front of a group and they're not willing to go through that pain.
And so, Yeah, I think we need to do I think the PR review club is a good example.
Like creating places where people can feel dumb together.
And that's okay.
And you sit up and you share a stage with, you know, a guy who's been doing this for a while and, like, understands cryptography, actually.
And you feel dumb.
I just sat through the federated Jami and E-cash, and I was like, I need to really learn what this is.
So it takes some humility to be able to get through that process.
And again, you just got to keep showing up and have faith that eventually you'll get it.
Again, I feel like it's very similar to just learning a foreign language.
I learned a foreign language as an adult in a different country, a different culture, and you feel dumb.
And over time, you start understanding the vocabulary, and then you start understanding some of the context when people say idioms, and then you can actually, like, you wake up one day and someone tells a joke in that language and you get it.
And you know, then you realize that it's just a matter of time.

Speaker 3: 00:29:42

You will, however, always feel dumb most of the time compared to other people and you will always have imposter syndrome.
I mean, it's not me or anything, but many people report that who have been in the space for a long time and are actually very good developers.
I think you just have to live with it and accept the fact that this exists.

Speaker 1: 00:30:03

Okay, so if you say that there is no hope for the rest of us, right?

Speaker 3: 00:30:08

No hope.
That's not what I'm saying.
I'm not saying, I'm just saying that it's not that you wake up the next day and suddenly you think, oh, I'm the best or anything and I'm the best developer and I understand everything about this particular protocol and I'm the only one and the only expert.
This will never happen.
There will always be people where you think that they know more about this than you do.

Speaker 4: 00:30:33

Yeah, I think you and you want people that have that humility working on this project because otherwise people get cocky and they make mistakes and you know you look around at the rest of you know you look around at other projects I'll say and people get cocky and stuff's gonna break and if you aren't sort of checking your own mistakes and having humility to think that you don't know everything, then you're not doing the best work.

Speaker 2: 00:31:02

I mean, I think one of the other areas is where do you start?
What do you do as your first move?
How do you get over the starting line?
And definitely one, not the only way, but one good way to do this, which also happens to be one of the main bottlenecks in a lot of these projects, is get involved with reviewing pull requests.

## Reviewing Pull Requests

Speaker 2: 00:31:21

Developers, I think, often have this desire to create new code, you want to write new features and get your satisfaction from implementing something, but you can learn a lot from doing reviews.
You often gain a little bit of context into that specific area.
Why are these changes being made?
Why was it originally like this and why are we changing it?
That burden of review is often cited as a sort of blocker for those experienced people to get on with doing what they want to do.
And I just think it's a really good way to learn.

Speaker 1: 00:32:00

So basically, I just heard of Bitcoin, I'm here to fix it.
Getting over there, right?
Okay.
So we've been talking a lot about how hard it is, how painful it is, how humbling it is.
What can developers that are thinking about starting or have started they are in the midst of it what can they keep in their mind as their guiding star what what should they keep in mind you got it sorry You got it, Zorja.

Speaker 0: 00:32:42

I think you should answer this question.

Speaker 3: 00:32:48

I don't have a good answer to this question because I don't have anything in particular in mind when doing this.
Perhaps one thing I have in mind is the long-term look that I mentioned, the long-term outlook on this thing.
This is going to be around for a long time so it makes sense to invest your time in it and it changes people's lives.
Perhaps not directly, it's a very indirect way of course to influence things but I think the chances are good that it works.

Speaker 2: 00:33:24

Yeah.
Yeah, and I think coming back to what Jonah said earlier, you know, most Bitcoiners I talk to are just super interested in Bitcoin.
Personally, they want to think about it all the time.
You're weaving it into conversation.
You want to work on it.
I don't know, perhaps if you've got a desire to keep learning about it continuously then I think it'll be good.
Like Jonah says, keep putting the work in, and you'll get there.

Speaker 0: 00:33:54

OK.
I think it's about imagining the type of world that you want to live in and recognizing that it's not going to happen unless you make it happen.
I want to live in a world where anyone can pay anyone.
Where big banks and companies and governments cannot just arbitrarily censor people.
Want to live in a world where when you like something that someone creates, you pay them directly with money instead of waiting for an intermediary to come in and seek rent from both of you.
Like, I don't know, I'm not, we don't want to wait for someone to build that for us.

Speaker 3: 00:34:42

Perhaps another guiding principle now that I'm just thinking about it.
At some point you will take responsibility and especially in or for example in the open source world that and also in the job of course it means doing a lot of things in your spare time for example that you probably don't want to do.
So that's, I think, one of the key things that many developers are also really, really driven by is just the sense of duty, right?
Because that's their part of the code, they want to improve it, they see other people's pull requests, they need to review it.
There are a lot of things that when you start working in this space and you have this kind of idealistic outlook, perhaps, that you really want to make this work and you get this sense of duty?

Speaker 4: 00:35:40

I think, I mean, why did we all fly down here?
Like, this isn't convenient to be here.
And yet, we're all here because it's meaningful and it's impactful and we want to make big change.
And so, the ability to contribute to that as a builder, like, is there anything better than that on the planet?
Like is there anything to wake you to just the way that Gloria described where she wakes up every day excited to go to work and goes to sleep every day feeling like she had a meaningful day?
Like what else could you ask for?

Speaker 1: 00:36:26

How do you guys think, I'm guessing most of you like myself, get like a bunch of spam from recruiters with horrible pitches.
How do you guys think that companies in this space should, or that want to launch a project in this space, should approach developers in a way that is meaningful for them.

Speaker 3: 00:36:55

The Blockstream approach to this apparently is, which is apparently working, which is apparently working, which is to build this kind of image of being a cypherpunk company that is really, whose future is completely aligned with Bitcoin's future.
And also who's investing a lot in open source projects.
And that on the other hand attracts a lot of people who start contributing in their spare time or who see Blockstream as something that they would want to work at.
I think this is something that really helps Blockstream right now to get applicants for the job postings?

Speaker 4: 00:37:54

So I actually do quite a bit of recruiting, but it's mostly for open source developers.
Not to necessarily work at Chaincode, but just to work on the project or I think the project Bitcoin core related technology protocol stuff and so the way I reach out is mostly because someone has already shown interest As in someone has already made the first move, and you just offer help.
Like, how can we be helpful?
Now, chain code is a little bit different, and I think a little bit unique.
But something I've started to do when recruiters send me emails is I take the call and then one of the first questions I ask is like what are you doing for the ecosystem?
And I've had some actually some meaningful conversations with recruiters trying to help them understand that their approach is a waste of their time if they're actually looking for the kind of people that they want to hire and if they went about it in a way where they actually were helping the ecosystem as opposed to trying to extract from the ecosystem that they'd be more successful.
So if you're a company and you have a budget for recruiting, you probably have a budget to work on open source or something like that.
So take your marketing budget and put it towards something that will actually make things better, please.

Speaker 1: 00:39:26

One of the things that I think are very, very different is I've done a lot of open source development myself and I've worked for companies and the the way open source development works it's very different than how working in a company feels like and how the approach to everything is like.
Can you guys talk a little bit about how someone that has worked within four companies their whole life, what to expect going into open source development?

## What To Expect Going into Open Source Development

Speaker 4: 00:40:17

It's different in that oftentimes no one's telling you what to do.
So that's the big change is when you work for a company, there's a hierarchy and a structure.
You get orders from on high, business makes decisions, and then that gets filtered down through layers, and eventually it reaches the front line developer who's told it's broken up into smaller features, and they go and implement it.
People who work in open source scratch their own itch.
And oftentimes, there's not that kind of coordination.
And so you go after the things that are important to you.
You go after the things that are meaningful to you, and that can feel very scary when no one's telling you what to do because you don't know what to do.
And so I think we actually have examples of people working in open source and deciding that they wanted to go work in a company because they didn't feel comfortable in that murkiness of feeling like they were productive.
You know, there's no...
The shipper's high that you get from shipping a feature and, you know, the CTO celebrating that with you, you don't really feel that in the same sort of way.
And so it may not, Open source may not be right for you.
That's OK.
You can still contribute to the space in meaningful ways.
But you may not like taking orders, too.
And so maybe open source is a better fit for you.
I think it comes down to your personality and comes down to your mindset.

Speaker 1: 00:42:03

I thought about leaving some time for questions from the audience.
So if you guys want to talk about something before we open for questions, something we didn't touch on.
Yeah, good.
We don't have any more mics, right?

Speaker 3: 00:42:22

No.

Speaker 7: 00:42:29

Hello.
Awesome panel.
Okay.
Two questions.
One is for the whole group.
What are some good milestones that people can aim for when they're onboarding both early ones and later milestones?

Speaker 0: 00:42:52

For me it was the day when I was wondering how something worked in Bitcoin, and instead of going on Stack Exchange or Googling, I just look for it in the code.
And after hitting that, it's just like full speed ahead, because you never need anyone to learn.

Speaker 8: 00:43:21

So you talk about the hero's journey and you folks are all, you've taken the hero's journey.
I mean, I see it and I know it.
What about for normal people?
You know, like, you focused on, and I'm glad you're doing it, I'm glad you're cultivating those heroes, I'm so glad you are.
But there's a whole lot of other folks who are not going to be able to take that journey because of where they are in life, because of whatever, but we need them.
And I don't know whether it's, I don't know whether it's like maybe we're just not the product, the ecosystem is not mature enough yet to be able to take advantage of the normal folks or is it that we need to pivot the ecosystem to make it be more accessible and so we can use us normal folks.
Does that make sense?

Speaker 4: 00:44:25

That's a great question.
Noel, go ahead.

Speaker 2: 00:44:27

Yeah, I mean, I think certainly for Bitcoin Core and some of the other projects, there is a bit of a, I think it's a misconception that it's all super technical and you need to be incredibly specialized and incredibly good at something to contribute, but it's not the case.
You know, there's a ton of, there's a ton of work that needs to be done that doesn't require you to be a cryptography expert or a mempool expert.
So I think there's stuff for everyone to jump into, really, and it's just about getting a journey started and getting involved.

Speaker 4: 00:45:06

Everyone's a hero.
I don't, like, I can't, I mean, I can't code for beans.
Like, I am not good at developing.
And so I've chosen a different path because that's how I can contribute.
And so you have to find what you're good at and what you're excited about and how you can position yourself to make meaningful contributions.
And there is no hero here.
I mean, these people are heroes.
But I promise you, I'm no hero.
And so How do you take advantage of that?
You find a way that you're excited about to contribute.
That's it.
I'm happy to talk to you about who you are and how do you contribute.

Speaker 8: 00:46:02

I'm not just thinking about myself, but I'm using myself as an example.
I mean, there are folks out there that we need that are never going to get passionate, right?

Speaker 4: 00:46:13

I mean, we've got...
Oh, yeah.
I don't want those people.

Speaker 8: 00:46:16

But we need them.

Speaker 4: 00:46:17

No, no, no.
No, I don't think we do.
I really disagree with you.
I think what's exciting about my wife is calling me a lot right now.
I'm sorry.
I think what's exciting about this space is that we just flew thousands of miles to come to a country because they made a Bitcoin law.
Like, that's what we need.
Because one of those people can do 10 times the work of someone who's just clocking in.
And so, yeah, you don't need to be a hero, you just need to be excited and you really do the work.

Speaker 8: 00:46:50

Are you saying that because that's where we are right now in the ecosystem, in the environment?
Because I mean, I'm just thinking...

Speaker 4: 00:46:59

No I think if you take someone who, if you compromise on that, then you dilute what you're doing.
You dilute why you're doing it.
And it's okay.
You can dilute it to a certain extent.
If you're building a big company, and that's your goal is to build a big company, That's different than building a company to push Bitcoin and Lightning forward.
And so if you're doing that, then you need to find people who care about what you're doing.

Speaker 8: 00:47:27

But I mean, like, I'm again thinking like traditional banking system, right?
I mean, way back when, at some point in time, somebody was really passionate about fractional reserve banking, and they went crazy, and now it's normal, and thousands of people go to JPMorgan Chase every day and work on whatever they work on.
I mean, don't we want Bitcoin to be like that where it's just normal?
It's normal and that keeps it going?

Speaker 4: 00:47:55

I don't.
It's OK.
I think it's OK to want that, but I don't want that, because I don't want to work with people who aren't excited.
I don't want to work with people who clock in.
That's not, by the time Bitcoin gets there, hopefully nobody has to work on the planet at all.
We've figured out how to have a society where you have so much surplus, you don't need to work.
But like, that's not meaningful.
That doesn't bring meaning to your life if you don't care about what you do.

Speaker 8: 00:48:25

No, I mean, no.
You can have other things that you find meaningful in life and a job is a way, is a means to get income for you to do the meaningful thing in your life.
And there's nothing wrong with that.
I mean, that's not me.
But there's nothing wrong with those people.
We need those people to do the dredge work, whatever, to integrate it in with the cash registers, whatever.
We need those people.
I mean, that's.

Speaker 4: 00:48:53

I just disagree.
It's OK.

Speaker 7: 00:48:58

Can I ask my second question now?
Second question is, how can someone who didn't do a PhD get involved with the research side?

Speaker 3: 00:49:12

I don't have a PhD and I'm on the research side.
How does it work?
How did it work was basically working with the right people, right?
You need to be in the right group and you need to learn from people.
You need to find someone who is willing to teach you, who is willing to spend time with you.
You need to be willing to learn and then it just takes time.
But really, I learned all the things from other people, right, who really took in the time to do that, who knew more in this specific area than than I did.
And especially in the field of cryptography, I didn't have the formal training that other people do, for example, to do stuff like music.
But somehow, I was able to pick it up just from other people who were willing to teach me.

Speaker 9: 00:50:09

So you've been talking about onboarding.
You obviously all care about getting more more developers into the Bitcoin and Lightning ecosystem.
So I'd be curious for the four of you, what does success look like in two or three years time?
What does the Bitcoin and Lightning developer ecosystem look like?

Speaker 1: 00:50:28

It's okay.

Speaker 5: 00:50:31

It's okay.

Speaker 4: 00:50:45

I don't have a snappy answer.
I think we are at a point where we are just so desperately looking for people that are willing to do the work that it's, it consumes me.
In two to three years time, I hope that, and it is happening, I think you find people who are attracted to this kind of work and they start doing it themselves.
But success looks like that the community has taken this over and there's a flywheel effect where people who go through and someone helps them, they then help the next group and that group gets larger and larger.
And so in success in two to three years looks like there's just a big base of teachers and mentors and a whole like decentralized onboarding path for your local community or your, you know, wherever you are, that we have filled enough gaps where We are providing Clear paths for people to onboard into this ecosystem Just to add to that I think we don't only want people who are super motivated, great developers, etc.

Speaker 3: 00:52:27

We also want people who are philosophically aligned.
And I think for success this is also very important that we are able to teach the values of Bitcoin, permissionless, decentralized money for everyone, to the next generation of developers as well.

Speaker 4: 00:52:49

That's a better answer.

Speaker 5: 00:52:52

I have a question.
Well, a suggestion first, and then I guess a question.
I'm coming from another open source project.
I'm into web development.
I've been in the Drupal content management ecosystem.
I've been there through the years and seen the transformation that's done in that project.
One of The most important things I saw happen was one year they decided to work on what they called developer experience.
It's how to get people to work on Drupal core and get more people from off the street, so to speak, working on it.
One thing that they did for the PRs and the patches that we call them to core what they did they assigned them with difficulty right so so it allowed newbies to come in and say okay I'm seeing a bunch of PRs here which ones I guess are within the range of my my ability and and that helped a whole lot because it allowed people to come in and say okay I can perhaps start on these smaller ones first right so and I think it kind of adds to his point where it, it creates stair steps for, for people who are not necessarily passionate because I think passion can begin in two ways.
There are people who come in passionate.
You, you, you, you, you, you grew up around computers or something and you just have passion for things technical.
Then the other people who learn passion, you do something and you realize it works, and then you do something else and you realize it works, and You kind of step up the stairs until you're really passionate about something.
So I think improving the developer experience by creating those stair steps for new developers to come in.
Because I was really interested in Bitcoin.
I mean, I'm the type of guy who comes in with high passion, right?
But even coming in with high passion, I was trying to figure out so how do I get started.
I asked person like what what projects are there I need to get worked and I was asking on Twitter asking people and people were like well I don't know just just kind of get started right And it was kind of difficult for me, because I wanted to know what projects needed help, you know, as a newbie, where could I go and get started?
And it was kind of difficult.
So working on a kind of stair-stepped method to get into developer experiences is perhaps something that you can work on for the future to make it easier for people to onboard as developers.
Secondly, just again from the Drupal ecosystem, the companies that are, you know, running Drupal in their businesses, they also contribute to the community.
So there are a lot of bounties and things that allow people to have motivation to work on these projects.
I'm in the Caribbean, and most of the guys around me, they're not going to work on open source projects because a lot of them just want to get food.
The priority, they don't have the free time to go on to work and stuff right and and you just want something so you can pay your bills and whatever and after you start making good money as a developer or whatever Then you have the spare time to start working on open source projects and so on.
But if there are bounties, bounties could be a thousand sats.
It is just a kind of motivation to allow people to get started.
And then there might be bigger problems with the larger bounty.
So companies who are working and benefiting Blockstream or whoever, could perhaps set bounties on different issues.
And tell the developer community about these issues and how they're more accountable.
So, just two suggestions I have.

Speaker 6: 00:56:49

Can I maybe add to that real briefly?
So, I wanted to pick up one of my neighbors and what they're saying about the heroes and stuff.
And I read, onboarding Bitcoin and Lightning developers, not Bitcoin Core developers.
And I think it's pretty dangerous to idolize the Bitcoin core and lightning and all the super hard things because there's so many super small projects where one or two people are working on and I think there does the people that work in those projects would be way more passionate to teach new people to work with them on their very small projects.
And they're usually way lower barrier to entry.
And I think it would be really great if there's more resources for people to find those small, smaller projects and not want to work on core or want to work on lightning.
Because those projects are freaking hard.
And most developers will never work on them or don't have to work on them because it's hard.
So maybe like a mailing list or a newsletter where smaller projects can announce new things that they built or something like that where then you can look at, Yeah, smaller projects, web projects, point of sale projects, hardware projects, like smaller things.
Lower barrier of entry.

Speaker 0: 00:58:06

Some of us have a personality trait where when we see something that's not quite right, there's a typo or something, We're like, I wish I could open a PR to fix that.
Like a broken lamp or something.
If you have this personality trait, pretty much everything in Bitcoin is open or, you know, there's a lot of open source Bitcoin projects and a lot of them are like Stephen said not Bitcoin core like not going to cause Bitcoin network to die if you make a mistake so if you have this personality trait I think you'll be surprised by how many places are welcoming contributions.

Speaker 1: 00:58:56

Okay.
I think that's time.
So if we don't have any more questions, We'll wrap it up.
All right.
Thanks guys.

Speaker 0: 00:59:15

You
