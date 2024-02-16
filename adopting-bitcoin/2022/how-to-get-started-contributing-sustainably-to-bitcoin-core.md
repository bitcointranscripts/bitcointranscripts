---
title: "How to get started contributing sustainably to Bitcoin Core"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://www.youtube.com/watch?v=Bduon80-4CE
tags: ['bitcoin-core']
speakers: ['Jon Atack', 'Stephan Livera']
categories: ['conference']
date: 2022-11-16
---
Speaker 0: 00:00:00

Now we are going to have a panel conversation a kind of side fireside chat between Stephan Livera and John Atack and Name is how to get started contributing Sustainably to Bitcoin core so if you are a deaf and are looking to start to contribute to Bitcoin Core, this is your talk.

Speaker 1: 00:00:32

Okay, so thank you for having us and thank you for joining us.
Joining me today is John Atack.
He is a Bitcoin Core developer, contributor.
He started about two or three years ago, roughly?

Speaker 2: 00:00:47

March 2019.
Hello, everybody.
Good to see you.
Three and a half years now already, time goes fast.
Yeah, right.
We haven't seen each other since three years at the Lightning Conf in Berlin.
October 2019.
Yeah, we met and at that point I'd been working on Bitcoin Core since seven months.

Speaker 1: 00:01:06

So let's get into this today, we're gonna chat a little bit about your journey and offer some insights for people here or anyone on the stream if they are thinking about what it's like being a Bitcoin core contributor and if they want to get involved how they would do this.
So maybe just tell us a little bit about your motivation, like why did you want to go down this pathway?

Speaker 2: 00:01:27

That's a great question.
So I'd have been aware of Bitcoin since several years before I began and I had in the back of my mind the goal to that someday I would Stop taking freelance missions.
I was a freelance software developer working for large corporations saving their ass on missions that they were in trouble with and The whole time I was thinking okay.
I'm saving up money I'm stacking and I'm someday I'm gonna quit this and I'm going to work on Bitcoin.
It was an idea I had a long time years beforehand and You know you something something has to happen to kind of kick you in the rear and to kick-start you into doing it and That's something for me was totally unplanned.
It was end of February 2019 on Twitter I saw chain code labs saying last minute to apply for the summer residency at chain code labs this summer.
In 2019, chain code labs did a very large residency program.
It was very ambitious And at the last minute, I think 20 minutes before midnight when the applications closed, I submitted a proposal to join the seminar as a residence.
I was not accepted.
But this is where the story becomes interesting.
They did take me for a first round interview.
They said, okay, we don't know who you are.
You haven't done anything in the space yet, but we encourage you to try and to apply later, maybe to the next residency.
I thought, okay.
Two weeks went by and then finally I thought, nah, I'm just gonna start now.
And I started trying to contribute on my own, I would say half time.
And two weeks after that, I got a call from Chainflow Labs saying, Ah, you're active on Bitcoin Core and it's interesting.
Would you like a phone call with John Newberry to mentor you?" I said, sure.
And we did a phone call and I was like, whoa, this is ambitious.
He's setting the bar like up there.
So I just kept doing what I could and I was not in the residency, but one week before the program began, Chaincode Labs called again and said, okay, you've been doing this since March and now we're late May, why don't you, would you like to come to New York?
And so I did end up going to Chaincode Labs, even though they said no.

Speaker 1: 00:03:49

That's a great story.
And I think what has happened over time, because I know part of your story is that you were working unpaid, right?
You were doing this just because you believed in it.
And so then there was also a journey of trying to get sponsorship or grant money or funding to sustain yourself.
So could you explain a little bit about that process?
Because I think listeners will be interested.

Speaker 2: 00:04:17

Right, so basically when I began in 2019 it was brutal.
It was the bottom of the bear market, the previous bear market, and at that time none of the currently existing funding structures were in place.
Your only options were to be hired by Blockstream or Chaincode Labs.

Speaker 1: 00:04:40

MIT DCI maybe.

Speaker 2: 00:04:41

Yeah, but they didn't have these grants that are very prevalent now and the situation is much better now, much easier.
Really, you need to show proof of work.
You need to show up and humbly, you gotta stay humble.
You're gonna learn a lot, you're gonna fall down a lot, and you need to try to add value while respecting other people's time and being humble about it, you're gonna make lots of mistakes.
There's so much accumulated context and experience that the long-term contributors have that a newcomer will not, but that doesn't mean you can't provide value if you're careful about it and thoughtful and take the time.
So yeah, it took me literally back then one year to be funded.
Thank you to Jack Dorsey who created Square Crypto, now since renamed Spiral.
I didn't actually do anything to get a grant.
I was just, you're just showing proof of work and you, after a while people will push grantees to, I mean I suppose nowadays you can apply for grants with a project But I never had a project My only project was to review and to contribute and to fix things that I saw my project I never had a project dropped into my lap like hey I'm going to implement this I'm going to do fed admin, or I'm going to do you know pay join or or Join market or whatever or bit 324 implementation or bit 155 implementation.
I never had anything like that.
All I did was review and basically do the things that no one else perhaps wanted to do, but that needed to be done, like reviewing and testing and fixing things.
And after a while, that worked.
It took me a long time.
It was pretty hard.

Speaker 1: 00:06:24

So for the layman audience who don't understand perhaps the nuances of software development and Bitcoin Core, Can you explain the difference between writing a pull request, making some new code for Bitcoin Core and doing that other role that you was mentioning, the review, the testing?

Speaker 2: 00:06:41

Right, I think that gets back to what does a Bitcoin Core developer do and I think it doesn't correspond to the image that most people have of what we're actually doing.
I would say most of the time what we're doing is reading code, reading other people's ideas and thinking and maybe testing and reviewing.
In my case, There's very little coding.
I was a full-time software engineer from Quite a long time before Or you basically you just churn out the code and check off the boxes as fast as you can during your current sprint before the next sprint starts Bitcoin core is is different.
It's more you have to be more patient you have to There's more thinking going on and nuance and things don't always go quickly.
It depends on what it is.
So I would say the most important role in Bitcoin Core and what is most lacking is review and testing.
It's not coding and also spending time thinking through what other people are saying, testing, verifying.
Okay, maybe they're right.
Maybe they're wrong.
You need to come to these conclusions and pretty much you do it on your own.
Well I've always worked alone.
Some people work in large organizations, you know, some people work at Spiral, some people work at Chaincode, some people work at Blockstream.
But even Blockstream, they only support one Bitcoin core developer, Andrew Chow, and I believe he works mostly alone unless you travel into an office.
So a lot of it is just alone time with a code, reading things, reading the mailing list, coming to your conclusions.

Speaker 1: 00:08:17

So going on from that, I think it's also the, okay, so could you maybe outline as an example like somebody, like where some of the discussion takes place and then where the interaction back and forth like with other developers happens?

Speaker 2: 00:08:41

Well the interaction happens either on the Bitcoin Core Dev IRC channel or on the pull request on GitHub, generally, and occasionally on the mailing list.
Those are the three areas where there's, yeah.
Another thing that core developers do is educate.
They don't only work on Bitcoin Core, they might review and help write for, say, Bitcoin Optics Weekly Newsletter.
I did that for two years.
I see Murch is in the room.
He's currently on the Bitcoin Optics team.
They also perhaps help run the Bitcoin Core PR Review Club, which I also did for two years.
These are Annex activities that many core developers do in addition to working only on Bitcoin Core.

Speaker 1: 00:09:24

One other area that I think is interesting, and I know you mentioned this to me offline.
So with Bitcoin Core, as I understand, most of the code is in C++ and a lot of the testing is in Python.
But you mentioned that you actually had to learn this as part of your process.

Speaker 2: 00:09:42

Can you elaborate a bit?
Correct.
So Satoshi Nakamoto wrote in C++ And the functional test suite is in Python.
Now, before I'd arrived, I had not coded in either one.
I'd had C back in my college days.
But My personal work experience was we're in completely different languages.
Assembly and web development in Ruby and Ruby on Rails, for example.
So, yeah, but if I can do it, I think anyone can.
I arrived and I taught myself C++ while doing it.
Python came quickly because it's similar to Ruby.
But yeah, it's not impossible for you to show up and to learn these two languages and become a core developer if that is your goal.
Note that there isn't just Bitcoin core and I think that's important to underline.
There are many other valuable projects in the space besides Bitcoin core There are wallets miners lightning implementations lightning development specification bolts dips There are many super valuable projects It doesn't have to be Bitcoin core and even it doesn't have to be open source You could work on closed source.
There's lots of jobs out there now for Bitcoin Developers and it doesn't just have to be a developer You could also find a place for yourself if you're a product manager a designer a writer We need people like that in the space.
Maybe not on Bitcoin Core, which is just developers, but in other areas.
Or you could become a startup founder.
There are more and more VCs who are willing to fund Bitcoin and now lightning startups.

Speaker 1: 00:11:18

So could you elaborate a little bit in terms of non-developer contributions?
So let's say somebody's out there, they're interested to get involved.
Maybe they're not quite a developer, but they are, let's say, tech savvy and interested to contribute.
What are some ways that they could do that?

Speaker 2: 00:11:34

Well, for example, I believe that Spiral, who was my first sponsor and still a sponsor of mine, I believe that they're quite interested in finding product managers because a good product manager can have a lot of impact by leveraging through their work through developers and designers.
And I think they're very happy with the one or two product managers they do currently support and might be interested in more.
I don't know if I answered your question.

Speaker 1: 00:12:04

Yeah, that's one example.
And I know even some other open source projects are looking for translators as an example.
So literally no coding, just literally someone who can translate and make that wallet or that software accessible in other languages.

Speaker 2: 00:12:19

There was a period of about two years when Spiral was also giving grants to a lot of designers.
I don't know if they're doing that so much currently because we are unfortunately in a bear market, but you can always apply.
If you research it, you'll find that there are many funding organizations now, especially compared to four years ago when I began.
But the first step isn't to apply for a grant unless you're already well established in the space.
The first step is to apply, I would say, to Chaincode Labs online seminar, either Bitcoin or Lightning, or Summer of Bitcoin, or a number of other excellent programs that are up and coming to educate people in space right and yesterday on the same stage we had some other organizations like Vintium, Library of Satoshi and Torogos as well.

Speaker 1: 00:13:07

So these are some other organizations that you can potentially...

Speaker 2: 00:13:12

I believe there's one that's being started by Marina Spindler, I can't remember the name, for El Salvador focused.

Speaker 1: 00:13:19

That's Torogos.

Speaker 2: 00:13:21

Right.
DeFarm in New York, DeFarm, Desfarm maybe for Americans, DeFarm for people like me who live in France.
In New York they're also doing mentorships.
I helped mentor some developers, tried to at least.

Speaker 1: 00:13:35

And so there's a range of possible places that you could be sponsored by or directly employed with.
So you know historical and long-standing examples like Blockstream as we've mentioned, but there are other so Blockstream, Chaincode, MIT, DCI, Spiral as you've mentioned, there's Brink, there's probably a few others that I'm missing.
Yeah, Super Lunar is a new one and various Bitcoin and crypto exchanges.

Speaker 2: 00:14:02

Human Rights Foundation, also miners.
Unfortunately, they aren't going through a good time right now, but I had a grant for one year from Compass Mining.
Thank you to them.
Unfortunately, they may have been falling on hard times, but in Human Rights Foundation, They receive donations like Brink does and they support people.
And Alex Gladstein just renewed my grant for another year.
So thanks to them.

Speaker 1: 00:14:24

So these are some examples, or in some cases, exchanges will directly sponsor a grant or grantee.
So these are some of the pathways for people out there if you're interested in applying for this kind of thing.
I think it'd be good to chat a little bit about mentorship as well.
So I understand for yourself, it seems like you were a little more individual in your own way, but I understand for other people mentorship was very key for them So could you just explain a little bit about that?

Speaker 2: 00:14:52

Right?
You're right.
I'm pretty much a free-roaming Free roaming sort of independent person and I like to self-learn I've never found it very useful for me to learn in a classroom situation.
I'm a self-learner alone, just pounding my head into the material.
And again, I wouldn't be here if it wasn't for Chain Code Labs seminars.
They're excellent.
It's a good first step.
If you have any doubt as to whether you would like to join the space, apply.
Because not only will you learn as much, you will get as much back out of it as you give into it.
I promise you that.
But it's also, I would say, a talent scouting program disguised as an educational seminar.
In other words, you'll become known in the space just by participating in it.
The people who matter will see who you are and this person maybe needs support And that's how it happens.
I didn't actually apply for any grants ever you kind of got headhunted Well, that's how it happens.
Yeah And once you begin As long as you're doing the work, and this is all really about showing proof of work It's just like Bitcoin and once if you continue showing proof of work, people are valuable and needed in this space, and especially experienced people, context is important.
That's one of the things that people may not realize is the longer you stay in the space, the more accumulative context and history you have in your brain.
And that is terribly, that's a terrible loss for the space when someone stops contributing and has all that context and they leave.
So it's important to keep long-term people so that when someone new comes up with a flashy new idea, hey, I just thought of this, what do you all think?
You're able to say that's not bad.
Now, someone proposed that in 2015 and here's what happened and why it didn't get adopted and then in 2018 someone else brought it up in a different format and that almost made it but I think they got discouraged and dropped their effort.
So that's valuable.
You can apply history and context.
And so usually, once you get in, it's not too hard to stay in.

Speaker 1: 00:17:02

Yeah and I think that's a underrated point around context.
So from every Bitcoin Core developer I've spoken to, it seems that it matters having that longer-term knowledge of what happened before and so that's obviously a very useful thing when there are experienced contributors such as yourself and others out there who are longtime contributors who can then share the context about what happened and perhaps be on the lookout for certain bugs that maybe they have a heightened awareness of.

Speaker 2: 00:17:37

It was Adam Jonas at Chaincode who mentioned to me the value of long-term context in history and why it's important to keep long-term contributors.
And...

Speaker 1: 00:17:55

Well, a common thing is various Ideas get shared and actually that idea was on Bitcoin talk in 2011.
You know this kind of it's like a common thing but then Where that idea went and what whether it was the right time for that idea?
Maybe that's also a question right so people might have been speaking about payment channel ideas on BitcoinTalk, but nowadays we have the Lightning Network which is a network of payment channels and now it was the right time.

Speaker 2: 00:18:23

There is one paradox that will surprise maybe some of you who are considering entering the space and it might be finding it forbidding or Intimidating and that paradox is I'm going to use analogy that I pulled out of my head yesterday at a talk I gave it's a bit like the old music industry where The artists are saying man.
I can't find a record company to sign me.
But then at the same time, you would talk to the record companies, and they would be like, there's no good artists, we were looking for them, we can't find them.
The point being that, if you show up to a seminar like Chain Code or some of the other ones we've mentioned.
And you engage with the material, and you do the work, and you really show thoughtful work on it, you will stand out just because you're doing proof of work that is hard to find.
They have trouble finding people willing to engage deeply with the material, the space, the tech, the concepts, and to struggle and engage with them and work on it.
This is rare.
If you're willing to do that, then give it a shot because you're more rare than you realize and they're looking for you.
That's the paradox.

Speaker 1: 00:19:35

Do you have any comments on how Bitcoin Core development has shifted over time, if it has?

Speaker 2: 00:19:46

One thing that is striking is how fast things change.
For a long time you feel like you're the new person who's struggling and nobody cares what you have to say and everything you say feels dumb and you regret half of the things you write.
And then in a flick of a second, and all of a sudden people are talking to you differently and you're seen as established.
It's very odd, and it's a bit surprising.
Your grants renewed, and suddenly you're sort of an og or one of the most Experienced remaining contributors on the project because people drop out and leave I would say Well the event that affected me personally the most on Bitcoin core was the lead maintainer Vladimir Vanderland.
10 years he was lead maintainer.
I haven't said this here but he was the reason I was inspired originally to work on Bitcoin core because I really appreciated his maintainership style.
In addition to being interested in Bitcoin, Vladimir followed me on Twitter maybe three or four years before I began working on Bitcoin Core.
And I listened to him and read his tweets and following how he treated people on Bitcoin Core, which he was lead maintainer of for so long, he was kind, he was humble, service-oriented, he was lifting people up, and I thought that he was just the kind of leader I wanted to work with.
And I'm honestly very, very sad.
It was time for him to step down he needed to for himself he'd been around so long you know and everyone saw that coming since years but I think it's a great loss for the project.

Speaker 1: 00:21:33

In terms of I guess like dealing with you know conflict or contentious things that come up in Bitcoin, what do you have any anything you could elaborate or share on that, on how you deal with that?
Like if, let's say, there are competing interests, if one party or people want something and the other people don't want that?

Speaker 2: 00:21:55

Yes, that's a good question.
Some people have different levels of tolerance or appetite for drama.
Some devs like to stoke drama on the social networks and others like me aren't too keen on the drama.
I've found it helpful to adopt sort of a stoic or Taoist philosophy, at least I try to.
It's helpful to not be the first person to get angry.
It's helpful to read, say, meditations by Marcus Aurelius.
And I also prefer people who say their position once without flooding over and over again and coming back and attacking anyone who disagrees with them.
There are characters like that in space.
That's not my cup of tea, and that's how I prefer to deal with it.
Like, for example, the mempool full RBF recent discussions.
There was one person who was just pretty much flooding all the threads everywhere on all the social networks and on the PR.
My personal opinion is that's, well, maybe they got what they wanted.
But I don't think that's the right way to have the debate.
I think people should think carefully, respond when needed.
But It's not always necessary to respond, especially to some sort of low kind of attack or criticism.
If what you've thought and said is your position, that's enough.
That's my position.

Speaker 1: 00:23:28

So perhaps, I mean, abstracting away from particular arguments and debates and things.
What is the right way to reason and debate about these things?
As I understand, there's a preference then for speaking about objective data or reasoned arguments.
Is that the right way that people should debate things or what is the right way?

Speaker 2: 00:23:51

Well in theory this is about rough content consensus right a rough consensus isn't voting There's an article on it written back in the 90s by the internet standards committee back in the day, where rough consensus is humming or something like that, where basically everyone needs to feel heard.
And I thought it was important on a process like the taproot activation one, which drew out for months and months.
But some people got very upset about that and I wasn't upset at all because in my opinion it was necessary for all the people who had something to say to be able to say it and to feel heard.
It's important for people to feel that validation, okay I was able to get out what I wanted to say.
And I think that's fine.
I mean, if people want to say something, they can.
At the same time, there's a delicate balance.
For example, in the recent Mempool full RBF, there's a whole bunch of people who have, say, an 80% understanding of the topic.
Some people have a 90%, some people maybe a 95%.
And there's maybe two or three people who I would say have a 99.9% understanding of the topic.
The deepest, most experienced, long-term, active researchers and contributors in the space, in my opinion, is that they were shouted down, perhaps.
People weren't listening to the most thoughtful and nuanced discussion, necessarily.
Maybe they were.
That's just my impression.
My opinion is we shouldn't break things if we don't need to.
We should be careful.
But I'm not one of the young fiery contributors.
I believe we should be prudent and reasonable.

Speaker 1: 00:25:30

I think that's a fair approach to take.
Can we chat a little bit about some of the various ways that people skill up.
So probably one good example would be Bitcoin Review Club.
So can you tell us a little bit about that and why that's useful for people?

Speaker 2: 00:25:47

Right, Bitcoin Core PR Review Club is an excellent initiative, again by John Newberry, who's done a number of excellent initiatives.
He also was the founder of Brink.
I highly recommend, if you want to get involved, participating in the Review Club sessions online on IRC every Wednesday, preparing the sessions.
The more you prepare, the more you give, the more you'll get and learn.
And eventually, hosting some sessions.
Because nothing is more scary than the preparation to feel you're capable and competent enough to host a session about something.
Highly recommended.

Speaker 1: 00:26:26

And so that seems to be one good tool or way to skill up on things.
I understand other people use things like Socratic seminars.
That's another way that people try to learn by asking Socratic questioning of each other.
And there's mailing list discussion as well and of course GitHub, the comments on the pull requests.
So could you just elaborate a little bit on some of those methods of the discussion and learning that can take place?

Speaker 2: 00:26:54

First of all, you reminded me I highly recommend subscribing by email to the Bitcoin Optech newsletters.
They're written by Dave Harding every week with a competent team of reviewers, of which I did that for two years, and wrote articles as well.
It's a great way to keep up with developments in the space.
Subscribe to the mailing list.
And I've already forgotten your question.

Speaker 1: 00:27:17

Well.
Yeah, if you could just elaborate a bit on that discussion.
I think you already were and I know there's an IRC chat as well, and I think that's shifted now Definitely follow the IRC discussions in whatever project that you're working on.

Speaker 2: 00:27:32

There are IRC channels for L&D, Sea Lightning, Lightning Protocol Development, Bitcoin Core Dev.
All the projects, Join Market, they all have IRC channels.

Speaker 1: 00:27:45

Now I know also, it can vary, but some bitcoin core Contributors have an area that they are a specialist in whether that's the wallet or whether it's You know different aspects of that Do you have an area that you you would consider yourself a specialist or do you consider yourself more like a generalist?

Speaker 2: 00:28:04

I'm definitely more of a generalist.
There's not a part of the codebase that I'm not willing to try to review and to learn about.
And it's kind of cool that moment when you open up a file that you've never looked at before, which in Bitcoin Core is easily possible for a very long time.
Yeah, it depends on you.
I like to roam.
At the same time, there are certain parts of the codebase I spend much more time on than others.
So it's just up to you.

Speaker 1: 00:28:29

So let's talk a little bit about that process, maybe for people who aren't as familiar.
What does it look like then, that process of a person, let's say, contributing some kind of change, review for that, and maintainer?
If you could just talk through that process.

Speaker 2: 00:28:47

Yeah, it's hard for me to know how familiar people are with that process, but if someone opens a pull request and then people review the change on a conceptual level or on a code review level, it suggests changes and the process moves forward.
When there is enough approval by the reviewers, then it might be merged.
Some different kind of review and different amount of review is necessary depending on the change and how critical it is if it touches consensus or not Some changes are really low risk other ones are high risk so in theory Were I a maintainer I would probably want to see much more review on a critical piece of code than on a non-critical one.

Speaker 1: 00:29:34

Is there anything in terms of the broader Bitcoin ecosystem that you're excited about or that you would like to see, like whether it's, I don't know, whether it's lightning or some other thing, are there any aspects of that that you are particularly interested to see?

Speaker 2: 00:29:50

My main goal is for Bitcoin Core to be robust because failing it being robust it's hard to build on it and it's decentralization.
So most of my concerns are if there's some failure that we can see or some area that isn't as robust as it could be, it's the base layer, so it needs to be really solid.
And the second key point is decentralization.
So I'm speaking in general terms, but that's what it is I think Bitcoin might be the last one standing apart from any captured coins Thanks to its decentralization, but it's not as decentralized as it could be and I would hope for it to become more decentralized in the future and on all levels including the core development level.

Speaker 1: 00:30:41

And it's right to say that there's been a focus on that even amongst developers.
I think one other area, maybe this is like an observation, that sometimes when you're talking to people who are known for let's say evangelizing Bitcoin, they will speak in this kind of, oh it's inevitable sort of sense.
But then when you talk to somebody who's a core developer, contributor, and they're closer to the code.
They're a lot less inevitable, let's say.
So could you just elaborate a bit on that?

Speaker 2: 00:31:09

Yeah, well we see how the sausage is made, warts and all, and I mean, there's a lot of things that could be improved that no one on the outside will necessarily notice that it has been changed.
And yet, these are, in my opinion, the most important things.
I'm not talking about refactoring or making the code cleaner or prettier, I'm just talking about making the code base as robust as it possibly can be, and finding and fixing bugs.
Sometimes they're not talked about.
Sometimes they're fixed sort of in a way that people don't see.

Speaker 1: 00:31:46

This to me is more important than adding new features, but that's personal other people have a project This person is supposed to implement this pip this person is supposed to bring this into the project, and that's fine And generally I see my role is reviewing those things And I think it's fair to point out that there are debates even amongst the community about how much change Bitcoin should have right and it's almost it's I don't want to get too political, but it's almost like a similarity of like progressives and conservatives and you have like people who just say no just focus on the reliability and then maybe there are Other people who have let's say this big new feature that they that they want and so I suppose there are even even on Bitcoin call there are people with a different focus, right I Think I turn my mind.

Speaker 2: 00:32:31

Oh, it's good.
I thought I turned my mic off.
I'm not against new features at all.
They're not necessarily my priority, but I'm happy to review them.
Sometimes we break things without realizing it.
It's easy to think something's safe and it breaks something, and it's noticed only later.
So, what we need more than anything is review and testing.
And even if you're not a C++ expert, you can still test.
You can test the release.
You can test the areas that you're interested in that you use in Bitcoin in the new release or Even in not a new release But the release you're using and report anything you find in a way that makes it possible for us to reproduce what you found So let's leave it here with a few tips and then we can maybe open up for questions.

Speaker 1: 00:33:24

So, if you had any closing thoughts and tips for people out there, whether they want to become a Bitcoin Core contributor themselves or whether they just want to have an awareness of the process, what are some things that you think people should know?

Speaker 2: 00:33:38

Well the number one thing if you want to become a developer or something else in the space, in my opinion, is to show proof of.
It's as simple as that.
You got to dig down and do it.
And depending on who you know, maybe it will go faster or go slower, but proof of work is something that in the end, I think, rises to the top and is visible.
So that's basically if you want to be a core developer or work on Bitcoin or Lightning, I highly recommend the Chaincode Lab seminars or any of the other initiatives.
That's the best possible way to begin that I can think of.

Speaker 1: 00:34:18

Great, well everyone give John a round of applause.
Thanks, Stephan.
Thank you.
So we've got a few minutes for questions, so we can probably take two or three questions.
So can we just get a runner, down the back I think was first.

Speaker 2: 00:34:40

So yeah, we got Bitcoin core in your humble opinion should anyone even bother with BTC D or other implementations Should anyone run BTC D No, should anyone you know start contribute, you know As far as contributing to Bitcoin Core, is it worth looking at the other implementations as well?
That's up to you.
I don't want to tell people what to do.
Do what you like.

Speaker 1: 00:35:12

Next question, anyone?
We've got one at the second row here.

Speaker 3: 00:35:20

Thanks very much for your talk, it was enlightening.
You mentioned about being funded to work on Bitcoin Core through a grant.
I just wondered if you could say a little bit more about those grants and maybe even like what kind of level are they at?
How does that compare to say like salaries in big tech for senior professionals?

Speaker 2: 00:35:51

If I understand correctly, you're asking how high are the grants?
In terms of financial terms.
Generally, it depends on the grant structure.
Some offer you the ability to be paid all in Bitcoin, some all in dollars or even a choice of half and half.
I've often had the choice of all three, USD or Bitcoin or half and half.
I would say that it's less than a big Silicon Valley salary.
But nothing's stopping you from applying to several sponsors to accumulate them if you so desire.
I didn't do that at first.
And after I did begin talking to a few others, that turned out to be a good thing to do, in my case, because at one point I had three instead of one, and now I currently have two.
I don't worry about it as much as maybe I should because I like to stay focused on the work and not on the money Because I find that thinking about the money doesn't isn't conducive to being productive on the on the focus on the work itself But that's just me I would say that if you're young, it's very interesting financially once you begin.
If you are a bit older with say mortgages and a family to support, it's a bit more difficult, but it's not impossible.
It depends on what you're used to and where you live.
For example, I don't believe that they're geo-adjusting the grants.
For example, Spiral offers the same grant amount to everyone and then it's up to you to geo-arbitrage if you need to.

Speaker 3: 00:37:30

Okay, thank you.

Speaker 1: 00:37:32

We've got time for one more.

Speaker 4: 00:37:33

We've got John over there I really appreciate your comment about people wanting to be heard in the process.
What do you think is the best way for not only users and merchants to actually be heard but also feel heard in the process while they are not actually part of core engineers or really familiar with the culture of how to interface With that community.
What do you think is the best way for these outsiders yet still bitcoiners to be heard and feel heard?

Speaker 2: 00:38:16

Okay, that's an excellent question So first of all, I think it's good to remind ourselves that Bitcoin Core isn't a closed team.
It's an open source project that anybody can provide feedback on.
And feedback is welcomed.
And for example, just yesterday I reported a large Bitcoin financial company has some minor issues with the upcoming release and I reported it.
And they were like, well, why didn't they comment directly on the PR?
Well, I understand that it can be intimidating to do so and Also, they're busy They may be not have the time to go in and review and say something that they're not afraid that they're unafraid to say On the pull request it's intimidating.
I get that But it's open to everyone I encourage businesses and merchants to get involved.
As we recently saw with the Moon Wallet and Dario and others on the mailing list and on pull requests, There is a productive and less productive way to be giving feedback, so I would suggest giving feedback, but doing so productively, in a positive way, but yes, please do give feedback.
People want to see that.
We shouldn't be in our own little ivory tower, breaking things downstream for people without even realizing it.
We need that feedback.
I think it's very important to keep the core devs' feet on the ground, and I say that to myself.
I want to keep my feet on the ground.
And it is an issue because there is a tendency to say, give high respect to people who are just really deep in the code, but who actually maybe, you know, it works in theory, but not necessarily in practice.
So please do provide feedback, and do so in a conducive and constructive way.
It's very helpful.
Thanks.
And you certainly can.
Anyone is welcome to.
Last 30 seconds.

Speaker 1: 00:40:17

One up the back there.
Got to keep it quick, though, or we might run over.

Speaker 2: 00:40:25

What would you say is the main reason that people leave?

Speaker 1: 00:40:29

What would you say is the main reason people leave?
I believe Bitcoin Core, is that what you're saying?

Speaker 2: 00:40:34

That's a great question, why do people leave?
Working on Bitcoin Core is particularly frustrating, I believe.
It can take you years to have changes merged or even never merged.
You can work a lot and hard on something that takes a lot of your time, only to at the last minute have it not worked out because someone finds a really good reason why it shouldn't take place.
The review can be brutal.
Also some aspects are not necessarily fun.
Like, you know, it's a little bit like high school.
In some ways it feels like there's popularity comes into question.
And all these things sort of combine to burn people out.
And there's also the high stakes.
For example, you know, the discussion on the social media really burns people out I've had feedback from people who've left recently that you know all the talk about Bitcoin fixes the world or Bitcoin boils the oceans or why didn't you stand up to CSW and assassinate him yourself like you're some kind of ninja and not just the developer.
You know people have these really crazy expectations of core devs like we're just humans We're just developers and we need to focus on our work.
And we're not necessarily here to argue with every single person and spar debate with them online about whether Bitcoin is boiling the oceans and whether it's fixes the wars and whether it does this and whether it does that.
We're just trying to do our work.
And so this gets to people.
It gets under their skin even if it shouldn't.
And of course the Craig Wright things really burn people out because you're a potential target.
We're all one lawsuit away from deep stress.
So, yeah.
These things sort of do eat you, at you for a while over time.
And as much as you try to push them aside and focus just on working on Bitcoin Core, they do get under your skin after.

Speaker 1: 00:42:33

Yeah.
Well, all right, everybody, put your hands together for John.
Thank you, John.
Woo, woo, woo, woo, woo,

Speaker 0: 00:42:40

woo.
Yes, yes, yes.

Speaker 2: 00:42:42

Thanks everybody.

Speaker 0: 00:42:45

All right.
So, let's keep it going and remember to share your pictures tweets memes or anything that you want to share in social media using the adopting BTC hashtag so people could join and see all the experience that we already have in here in adopting.
