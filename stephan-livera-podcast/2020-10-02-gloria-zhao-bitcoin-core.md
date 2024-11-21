---
title: Learning Bitcoin Core Contribution & Hosting PR Review Club
transcript_by: Stephan Livera
speakers:
  - Gloria Zhao
tags:
  - bitcoin-core
date: 2020-10-02
media: https://stephanlivera.com/download-episode/2526/216.mp3
---
podcast: https://stephanlivera.com/episode/216/

Stephan Livera:

Gloria. Welcome to the show.

Gloria Zhao:

Thank you so much for having me.

Stephan Livera:

So Gloria I’ve heard a few things about you and I was looking up what you’ve been doing. You’ve been doing some really interesting things. Can we hear a little bit about you and how you got into Bitcoin?

Gloria Zhao:

Yeah, well, I didn’t get into Bitcoin by choice. Actually it was by accident. I’m a college student at Berkeley right now, and I got into Bitcoin basically by joining blockchain at Berkeley. But to start out at the beginning by sheer dumb luck, I was born in Silicon Valley and I think if I were born anywhere else, I don’t know if we’d be having this conversation. So if I were born in China, for example, but I wasn’t born in China, but my parents were born in China and they went through hell to get themselves out there and have me born here. And so the logical reasoning there is okay they covered the bottom layers of the Maslow’s hierarchy of needs a K getting themselves out of a communist country. And so now that I’m starting from a very privileged, privileged place, I get to think about self actualization.

Gloria Zhao:

And for me it’s been Bitcoin, but for the most like the majority of my life, it was a totally different path because being born in Silicon Valley means there’s actually a very clear template for what self-actualization means actually. So before I got to college, I was in high school. I was a college application. So I had to be valedictorian. I took all the standardized tests, got perfect scores. I had an honors recital. I had a portfolio of paintings. I had all these business trophies and I was supposed to like essentially fit as many achievements as I possibly could into a college application to like get started on this track towards like success and happiness, self actualization, whatever it is. And I mean, it was, it was hard. Like I pulled plenty of all nighters. I had a lot of caffeine pills and antidepressants, and it was the idea that, okay, you’re on this track, you need to go as fast as possible.

Gloria Zhao:

You make sacrifices today, just like my parents did right? For the things on my college application. And then one day I’ll get to be happy. So I went to college and study computer science because I was on this track, not so that, you know, I could lead up to Bitcoin, although, you know, looking back, it all makes sense. But yeah, like I did computer science because it was a hard thing to take and I could use it to prove that I’m smart on my resume and I could use it to get into clubs of other smart people like blockchain at Berkeley. And then these smart people can get me referrals to companies. And if I intern at this company, then I can do two interviews instead of seven interviews to get the full time offer. And then I could work there for five years as senior suite.

Gloria Zhao:

And then I’m going to switch between startups every three years. So that by the time I’m 50, I can have joined 10 startups and one out of every 10 startups succeeds, we learned this in fifth grade in Silicon Valley. Then I will have found a unicorn by the time I’m 50. And if I have some extra time, then I can become a VC. But anyway, like we had this very clear track of what self actualization was supposed to look like. And honestly, I ended up in Blockchain at Berkeley by sheer coincidence. And I learned about Bitcoin because it was what we were doing on weekends as kids it’s college.

Stephan Livera:

It’s very interesting. You’re telling me a little bit about the whole Silicon Valley culture and the mindset there. One thing that stuck out to me there is it’s like, there’s this implicit understanding that all things are gonna keep going. Like they have gone for the last whatever 30 years. What if that’s not even the case? Like what if it doesn’t actually play out exactly in that way? I mean, I guess these are is that considered as part of the culture or is it just kind of, everyone’s kind of one track mind in their kind of startup and VC world?

Gloria Zhao:

Yeah, well, I don’t, well, it’s very technology agnostic. Like, you know, it’s this idea of innovation, right? So Silicon Valley is really obsessed with this idea of innovation and, you know, to put this in a nice way, it’s generous towards new ideas. And if you are a young, bright person with an innovative idea, then all the VCs and all the developers flock to you, and you’re put in a position where you get to extract billions of dollars from, you know, whatever it is, be it Facebook, Google, like Uber, all of these things. Right. But so, you know, to put this in a less nice way, all that matters in Silicon Valley is appearing innovative. So like us college students, what we’re looking to do is play this game where you’re just signaling, Oh, I’m young, I’m smart. I’m innovative. Hire me. Like, cause you can’t say like, Oh, I’m an expert in this for however many years.

Gloria Zhao:

Cause you know, we’re just college students. So what we try to do is just follow wherever Silicon Valley’s trend is, right. It’s still innovation equals win and we’re just trying to play the game. Right. And that’s why I was this college application for 17 years of my life. And then I was resume for the next four. And then after I graduated, it’ll be, you know what, my LinkedIn profile says that I am and every, you know, few months or a year, like you have to update your LinkedIn profile and like kind of reword it to use the right buzz words so that it keeps up with what Silicon Valley wants.

Stephan Livera:

That’s really interesting. I think it’s like a really exaggerated startups culture, I guess. So for you, why was it computer science and not say the typical “be a doctor or a lawyer” or something like that?

Gloria Zhao:

Yeah, I think it was like I did want to be a doctor. It was like very Asian to be a doctor, like when I was 12. So, you know, I took all of like the AP biology and all those tests and things. I have an M cat book, which I bought when I was like 16. But you know, like, yeah, I talked to my dad and he’s like, no, I think you should do computer science. That’s where Silicon Valley is at. So that was it just, I chose computer science cause I was supposed to.

Stephan Livera:

Okay. So let’s, let’s fast forward then to starting university and you’re doing computer science and I guess at that time, was it just that blockchain was the hotness at that time?

Gloria Zhao:

Yeah. Yeah. So it was around 2017. I think I got in right before it got super, super hype and popular. But yeah, I just, I joined blockchain at Berkeley. It was kind of a no brainer you’re supposed to join a club. And one of the biggest things was we study blockchain and Bitcoin from a very like academic theoretical perspective at colleges. So we talk about like, Oh, you know, it’s essentially a distributed state machine and they have a consensus protocol and you know, we have, you know, we studied cryptographic hash functions and then we talk about, okay, what’s a hash pointer, what’s a blockchain, what’s mining. You know, like we talked about Bitcoin script even, but we didn’t really like send Bitcoin transactions or like most people did not have any Bitcoin. We were kind of studying it from a very theoretical perspective. So I guess that’s probably, that’s probably different from what most, how most people get into Bitcoin. But again it’s kind of like, okay, I want to have these, I guess kind of hard things on my resume. So it’s like, yes, I’ve studied distributed systems and cryptography. Which of course is underlying and very interesting. But I think our motivations for studying blockchain might be a little bit different from someone who, you know, finds it further along in their career.

Stephan Livera:

Yes as you mentioned, some people get into it from a more ideological perspective, whether they are a libertarian or whether they are a cypherpunk who believes in the idea of Ecash, digital money. So for you, I suppose you started from a more academic theoretical sort of scientific viewpoint, and then later you had to, well did you then go and find some of those other, let’s say cypherpunk aspects of Bitcoin and figure out those parts of it as well? Or what was that like for you?

Gloria Zhao:

Yeah, definitely. I think I would call myself a cypherpunk today, but I did take a few detours along the way. So one of the first things that I after joining blockchain at Berkeley was sign up to teach blockchain fundamentals, which is our course on campus that we teach through the computer science department. So again, very academic. And the first lecture that I tried to do, I can’t even remember what it was about, but we did a dry run and I was so awkward. Like, I like was just stumbling through like, Oh this is like this thing. And Max Fang, who was president at the time and like guiding me through this, he was like, Gloria, you just don’t believe at that point? And do you like you don’t, you’re just trying to spew facts during your lecture.

Gloria Zhao:

And I’m like, well, yeah, like, no that’s who I am. And he’s like, you know what? You need to go read digital gold by Nathaniel Popper. You need to go read the cypherpunk manifesto. You need to go read like Julian Assange’s bio on Wikipedia. Like whatever it takes for you to like, actually believe in what you’re saying, you know, like I could tell you to go rehearse like 50 times, but I think your missing piece is you don’t know why you’re doing this. And that’s true. That’s kind of like a theme in my life. I don’t know, like I’m doing it for the piece of paper essentially. Right. But after reading like more cypherpunk literature essentially, I was like, Oh, like, this makes sense. It was the first time that why piece had ever been answered for me. And you know, I say this today, Bitcoin is the only real thing that I’ve ever done in my life.

Gloria Zhao:

It’s the only thing I’ve done where I know why I’m doing it. But yeah, like we were kind of steered in the very Silicon Valley direction. Right. So a lot of what we learned was basically like, you know, a company comes to us and they’re like, Oh, we’re creating this new blockchain platform. We have this boiler plate code. We would like to see you guys, you know, you college students, like, let’s see what you can do in a hackathon over 24 hours. And then whoever wins, we’ll give all of you guys like iPads and Nintendo switches and you know, like, this is what drives college students. Oh, you get red bull like and snacks throughout the hackathon. So, you know, whatever we did, it was kind of guided by like what seems like it was going to help us get a job after we graduated. And here’s an interesting question, actually. So I want you to guess something. So I was president of Blockchain at Berkeley for about two years and we’ve done a lot of analytics to try to see what kinds of, you know, marketing tends to draw more applications to our club. Can you guess what the number one predictor is for how many applications we get?

Stephan Livera:

I really wouldn’t be able to say, I mean, in the general blockchain or Bitcoin world, and it would be the price is the main driver really. But for a student, I guess, maybe something to do with like how many job opportunities it looks like that, you know if it looks like there’s going to be a lot of jobs in this pathway, then maybe you’d get more people interested. Or maybe if it looks like it’ll be more fun.

Gloria Zhao:

Yeah. You actually said it. It’s the price of Bitcoin almost linear correlation. Like when the price of Bitcoin 10x’ed we had a 2000 word essay on our application and we got like 500 people who wrote 2000 word essays. And they had stories to write. Like, I mean, when I talk about self actualization, I mean a lot of us, you know, when we get to go to college, we have kind of room to follow our dreams. So they all had these stories about, Oh, you know, like the world needs to be decentralized. We need to care about our privacy. I’m a computer science student and I can’t stand by and see like the world’s freedom, like restricted by all of these giant companies. They had so many stories and in Berkeley the Berkeley students are very socially passionate to say the least.

Gloria Zhao:

So you’ve probably heard this, I think we have that reputation. And yeah, like we all had these like social, like desires and motivations. So yeah, we had all these students who were dropping out and making startups. We had hundreds of people coming to our meetups, we went to conferences, it was like amazing. And then crypto, winter hit and everyone bailed, like, you know and I totally understand it because again, like I said, like Silicon Valley cares about innovation and students, like we’re all computer scientists. We’re looking to get jobs in Silicon Valley, hopefully after we graduate. And that’s really, like, I wouldn’t say that they were lying when they said that they had these social motivations, of course. But you know, there are priorities, like that goes out the window when they’re like, Oh my God, my midterm is coming up in two weeks.

Gloria Zhao:

Or what if I don’t get a job after I graduate? Right. Priority number one is graduate priority. Number two is graduate with a job and priority number three is like, don’t disappoint. My parents like, look cool on Instagram, stuff like that. Right. So yeah, crypto winter was like chaos. We lost like 99% of like everyone who said that they were so passionate about blockchain and I don’t blame them. I don’t. But you know, chaos is a ladder and I climbed it. That’s when I became president when nobody wanted to be. But yeah, I did a lot of rebranding essentially because you know, this is the fact is like people like college students, this is what they want. So, you know, we did a lot of rebranding. We became very blockchain, corporate, blockchain focused, very Ethereum focused. So you know, all our new members, they would come, they’d learn software engineering.

Gloria Zhao:

Did he get to work with clients and consulting projects. We’d ghost write papers. We speak at conferences. And then, you know, like there was money in consulting. So we got to buy everyone, Patagonia jackets and fly them to Hawaii and Barcelona and stuff. So like, they get the resume piece of like, Oh, look, I did all these projects and they also get the Instagram piece of, Hey, look, I’m on a boat. You know, everyone, you know, I get to flex or whatever. Cause that’s what you want in college. Right? Like people don’t have time to think about like Cypherpunk and whatnot. I mean, like we do, we will say we do, but again, there’s like a hierarchy of what we prioritize. So, but you know, obviously you can’t unread quotes by Julian Assange and like, you can’t forget like what it’s like and you know, like I’m scrolling through Instagram.

Gloria Zhao:

I can tell Instagram knows that I’m a girl. Cause I get all these makeup ads. And then, you know, I look over at my friend’s Instagram and I realize, Oh, we both get like ads for girly stuff. But like they’re targeted towards our specific bra sizes. Like my Instagram knows my bra size. Like that just, it makes it so uncomfortable. Right. And so like, you can’t just forget like privacy is an issue. You can’t just like decide like, Oh yes, my freedom is being like infringed upon, but that’s totally fine. You know, I’m gonna go work at, you know, Facebook or whatever. Right. so I was, I was becoming a little bit worried about, you know, I was, I had leaned really far into this like Silicon Valley narrative of like, Oh, you just, just follow the money. Actually the final straw for me, this really pissed me off final straw for me was one of my clients emailed me.

Gloria Zhao:

He sent me this article. He’s like, Gloria, you need to read this article. It says that because blockchain is not scalable. We’re actually moving away from that. And towards distributed ledger technology. Do you know anything about that? Yeah. That’s I was like, Oh my God, it took me like 30 minutes to write like a two sentence. Hey man, that’s a different buzzword for the same fricking thing to fool you guys in Silicon Valley because you need like a dopamine hit of innovation, like every three months. Yeah, I was pissed, man. So like at this point, like I’ve thought that I’m, you know, fighting for freedom or whatever, but I realized I was just playing a game, you know, like and my cards, weren’t looking too hot. You know, my friends were like, why are you still in blockchain?

Gloria Zhao:

Like nobody cares about blockchain anymore. It’s all about self driving cars now. And I’m like, what? Like I thought we cared about privacy like that. That was I thought it was about privacy, but you know, I was like, it’s over, I’m not gonna do this anymore. So I actually, like, I lined up the Google, Facebook, you know, the nice Silicon Valley, like a tech company offers and I was going to do back-to-back internships and completely remove any mention of blockchain on my resume. So this is what I was thinking about. Right. It wasn’t like, Oh, I want to care more about something else. It was, I need to change what is on my piece of paper that supposedly represents myself. Yeah. I just, I left blockchain for a while.

Stephan Livera:

Refreshingly honest. So what was it that made you stay and actually eventually get into doing Bitcoin core contributions?

Gloria Zhao:

Yeah. I’m getting to that part. Yeah, so I decided to leave blockchain kind of at the end of 2019 last year and I was totally done. And then in the beginning of this year, 2020, January, 2020, I got this email from Adam Jonas at Chaincode and he’s like, Hey, Gloria, you applied to the Chaincode residency last year. And we were hoping that you would apply again because you were pretty close last year. I was like, nah,nah, I’m good. I’m done. And he’s like, okay. How would you like to meet some Chaincode Bitcoiners? If you’re going to be at the Stanford blockchain conference could set up a coffee chat for you. And I was like, Oh, hell yes. Like, cause in my head I’m like, Oh, this is gonna be good. Cause I’m imagining these like carnivores, nutty Bitcoin maximalists. I’m like, this is going to be an entertaining conversation at the very least.

Gloria Zhao:

Imagine my disappointment. I met immediate with Amiti Uttarwar and John Newbery on a very fateful day and they’re not what I imagined. And you know, John, he says in his very soft, British voice, he goes, Oh, I work on Bitcoin Core, the most interesting project in the world. And I’m like expecting him to explain that because this is Silicon Valley. You can’t just go around saying good things about Bitcoin. And I’m like, well, I imagine you have to defend that statement all the time. And then I’m like, you know, in my head I’m getting the popcorn ready, you know? And he’s like, no, I don’t have to defend that very often. And I’m like, Oh shit. Like this is the first time I’m at a blockchain conference where I’m talking to someone who technically knows what they’re talking about and believes in Bitcoin. Like those two things have never coincided for me actually.

Gloria Zhao:

So this is like, this is my chance. And I basically sit there for three hours and they very kindly let me pick their brains. And I asked them like, okay, all the questions I’ve ever wanted to ask, deflationary monetary policy, environmental impacts of proof of work, decentralized governance, like toxic maximalism, like all this things. And at some point Amiti just goes like, you know, Gloria, you’re a computer science student. Why don’t you just clone the repo and like look at the code. And I’m like, nah, no, I know it’s not that easy. Like there’s no way there’s no way. Right. Cause I have worked for a few blockchain companies where, you know, they run testnets or main nets and you know, not to say that it was a terrible project, but you know, running a node is usually not that easy. You know, it takes like learning Docker and it’s like a several day kind of project to get all of the pieces together.

Gloria Zhao:

So I’m like, okay, yeah, I’ll try, I’ll try. And then that weekend I’m like, okay, I’m going to allocate eight hours to get this done. If it doesn’t work, then I’ll forget any of this happened. I’ll go back to, I’ll go to, I’m going to go to Google. I’m going to say, and then, you know, blockchain’s over for me. I already decided I’m out. But you know, the Bitcoin just makes it too easy to like run a node, you know, like you can run one on a Raspberry Pi, like you can get one running in a couple hours. So, you know, I refer to that day as the day that, you know, they unplugged me from the matrix essentially because like once I got started looking at Bitcoin, it was insane. Like it was just completely different. And I’m going to say this again, like Bitcoin is the only real thing that I’ve ever seen, encountered in my life because suddenly it’s like for the past three years that I’ve been like getting this computer science degree, all that stuff I learned about like file systems and synchronization, primitives, even like Fermat’s little theorem like this extremely obscure, like math, well, not obscure in Bitcoin, but like I never thought I would be using like math theorems to review code.

Gloria Zhao:

Right. And I took a cryptography class. They’re like, no never implement your own cryptography. I’m like, well, the sipa guys is doing it. But yeah, it’s like, I was like, Holy shit. Like this is technically extremely rich with, you know, it’s like, I’m like, Oh my God. Like my whole life has led me to this moment. Bitcoin is, this is all I want to do with my life. And but I still had this like Google internship and everything. Right. So I was like, okay, if I wake up at 8:00 AM, then I can review a PR before I get to work. I was like, okay, hold on. If I get up at 6:00 AM, then I can rebase my PR and address comments and review, okay. And, and then suddenly I’m like waking up at 5:00 AM every single day so that I can get like five hours of Bitcoin work in before I do my like, you know, my job or whatever.

Stephan Livera:

It’s very impressive. I mean, for years you were actually doing blockchain things and teaching as well, like doing lectures and things. And I watched, I’ve watched some of your YouTube lectures. It sounds to me like you were doing all this stuff and then it was only when you actually met John Newbery and Amiti that you actually got orange pilled?

Gloria Zhao:

Yeah, essentially. Yeah. Yeah. I mean like, you know, Bitcoin is open source. All things are open, but you know, the barrier isn’t do I want to do it? It was more like, can I do it right? I didn’t know that you could just, I don’t know. It seems like magic, you know, like Bitcoin is like this or Bitcoin core is like this, you know, magic thing. I didn’t know it was possible. I mean, not to say that it’s easy of course, but you know, it’s code and I was learning a lot of about computer science that applied to this code. Yeah it’s real.

Stephan Livera:

Yeah. So in terms of Bitcoin core contribution, why did you want to do it? I mean, was it basically because you had met you know, because you had had that exposure there and then you wanted to try and get more into it?

Gloria Zhao:

Yeah, well essentially it was like a drug or like, it was like falling in love, you know, like, it’s so cheesy, but like, you know, I had my first PR and then, you know, I had a second and I’m like, Oh wait, you know, this is really interesting too. And you know, I also reviewed a couple of PRs and like, Oh, like, this is really cool because like reviewing a PR, first of all, it’s like a really, really great way to contribute to Bitcoin core. It just, you know, you don’t show up as like the commit author, but a PR that someone else makes is essentially like an opinionated guided tour through a specific functionality in Bitcoin core, as well as the surrounding code base. And I also would go to PR review clubs and like, it’s so interesting. Like it’s beautiful really. And so like once I got started it, like I said, it was the only thing that I wanted to do every day when I woke up in the morning.

Stephan Livera:

In terms of making contributions, whether that is reviewing somebody else’s pull requests or doing your own pull requests, how do you get the idea or how do you decide what you want to work on or review?

Gloria Zhao:

Yeah. Yeah. That’s a good question. There there’s a lot of, on-ramps actually not just PR review club in which there’ll be like followups, like, Oh, you know, this isn’t a blocker to merge this particular PR, but it’d be nice to have this in general. And then, you know, that’s like a comment that someone makes and you’re like, Oh yeah, I could go do that. But in the core repo, there’s good first issues that are tacked various maintainers Marco makes a lot of good first issues, and they’re essentially just really well scoped and non-controversial issues. So that, like, if it’s your first PR all you have to do is figure out the code, write the code and then get it to a mergeable state. There’s no like politics or discussion, or like, you know, nasty, like debate that can go on.

Gloria Zhao:

So yeah, some of, I think one or two of my first PRs were just good first issues. And then, you know, while I was, so one of them was like writing tests for bloom filters. And then while I was writing the test, one of my tests failed and I realized like, Oh, it’s not that my test is wrong. It’s that this behavior is very peculiar. And then I like dove into that and it was like a whole journey. And then it resulted in like some P2P changes that I made. So like it, you know, it’s the gift that keeps on giving these good first issues. You know, it always sparks more conversation. There’s always things to be done and Bitcoin core. And yeah, it’s there’s all kinds of ways to start contributing.

Stephan Livera:

That’s really cool. So can you tell us a little bit about the, I guess the cultural aspects of it? I mean, were you getting support from other Bitcoin core contributors and you know, the maintainers and, and all the other people participating?

Gloria Zhao:

Yeah. Yeah. Well, I think, well, I don’t want to speak on behalf of all Core devs, but I definitely noticed that they’re really, really welcoming. Okay. There’s stereotypes of course but there’s like Twitter world. And then there’s like real world, like github world essentially. And, you know, like every time someone makes like a first contribution, there’s always like a bunch of comments. They’re like, ACK, welcome to the project. You know, thank you so much for contributing. So, you know, they’re all, they’re very excited about new contributors. But I also am really, really lucky to be in touch with Amiti and John, who I met on my matrix unplugging day, that, and they really care about putting a lot of effort into helping your contributors become longer-term contributors. So not just like the first PR, but, you know, becoming a real member of the community.

Gloria Zhao:

And I really, really like it means so much to me. So they offer a lot of mentorship of course, technically, but also like, what should I do when someone, you know, like, has something kind of mean to say, or like, how do I address this like negative feedback? How do I get myself into an emotional state where I can accept criticism better? And those, I think those are kind of like maybe unique challenges that I’ve never encountered in a software engineering project, but they’re really good in helping me grow of course. But yeah, like mentorship has been a really huge part of my journey. And like, I don’t know if I would still like be here if you know, these people hadn’t been so nice to me, but yeah, like I’ve experienced the environment is really, really welcoming.

Stephan Livera:

That’s great to hear. And from what I have read and seen as well, that there is a focus on, I guess, trying to get people to a point where they can more meaningfully contribute as well. And because it’s understood that sometimes the bottleneck is getting review time or even perhaps maintainer time. And so, you know, there might be a lot of people who want to put in a pull request, but not as many people who want to review and then also time on the part of the, maintainer to sort of keep to kind of keep the gears ticking. And so I suppose there’s kind of different motivations that go into that. And then you end up with different kinds of contributors, right? Because as an example, you might have somebody who just comes by and they just do their drive by one contribution, that’s it? And then there are others who are more like a long term sustained contributor, right?

Gloria Zhao:

Yeah, yeah, yeah. Actually, if you look at, I think the contributors there’s been like 800 people who have made at least one commit to the Bitcoin core repo, but I think less than 50 that actually do it on a daily basis.

Stephan Livera:

And I guess just like with many things, it’s like that Pareto power law sort of thing, right? Like the 80:20, there’s like a few people who are doing most of the work then, as opposed to what, I guess, if you just naively think, Oh, 800 contributors, are they all just doing like an equal amount, but it’s really not like that. And the actual amount of people with, I guess in depth technical knowledge about some certain area of the code it’s much smaller because it just takes a lot of time to get to that level of knowledge.

Gloria Zhao:

Yeah. Yeah. It does take a long time. Most of what I do is just figure out what this person meant in this one sentence in this comment. There’s so much it’s it’s so it’s like a tourist attraction. I don’t know, like how to talk about Bitcoin. It’s just like everything is so beautiful and everything, I want to spend like five hours looking into, so yeah. But yeah, like I said it’s very rewarding to learn about Bitcoin core, but yeah, it is pretty tough to get to the point where it’s like, yeah, I can go, but you know, review attention, anyone can go and review code as well. So yeah, it exists, but there’s all kinds of efforts to relieve that bottleneck including the PR review club, which I really enjoy.

Stephan Livera:

So let’s talk about that. So firstly, now listeners you might’ve heard from my earlier episode with AJ or with Jon Atack, we’ve spoken a little bit about that. But maybe it’d be a good time to just tell listeners what is the PR Review Club and tell us a little bit about how it works?

Gloria Zhao:

Yeah, yeah, sure. So PR Review Club was started by John Newbery and run by a couple of others about like a year and a half ago, I think. And like I said, John really cares about putting energy into helping newer contributors succeed. And it’s great for tackling the review bottleneck in core. So the way it works is every week there is PR that is selected or a specific commit from a PR. And the host will come up with a bunch of questions to kind of guide someone through reviewing that PR. And I think that part is extremely valuable because, you know, like bringing PR it’s like, of course there’s questions like, Oh, is this the best data structure to be using? Or is this syntax correct? Or, you know, but there’s automatic CI tests that are run on the pull request.

Gloria Zhao:

So, you know that part is covered, but in Bitcoin Core we care a lot about like security and whether this is introducing like a DOS vector, you know, how do we assess the performance of the new code? Like how do we assess the complexity that’s introduced by this new code versus let’s say the performance win or the simplicity win or whatever it is that we get from making this change. Because if you break Bitcoin, that’s pretty bad. But these are very like abstract notions. I think of like, Oh, the security is important and the host will distill that into more explicit questions. Like, Oh, if we call at ATMP this way what are the performance like drawbacks here? Like how much of this is cached and how much do we have to recalculate all over again? And it helps build that mental model for someone who’s trying to be a more long term contributor, be a better reviewer.

Gloria Zhao:

So yeah, and another really awesome thing is John Newbery and John Atack, and a lot of more longer term contributors like sipa will show up a lot of times and they’ll give context as to like, well, obviously you can like figure out through gift inaudible, why code is a certain way, but they’ll be like, Oh yeah, we originally introduced this piece of code because, you know, we saw that, you know, it would help in this situation or, you know, this is Satoshi’s old code and we were trying to improve upon it or whatever it is, and having access to people who are extremely knowledgeable in a very safe space. That’s like beginner friendly is super, super valuable.

Stephan Livera:

And I know you hosted one, I think maybe a month or so ago. Tell us a bit about your experience hosting the PR review club.

Gloria Zhao:

Yeah. Yeah. Before I hosted, I think I had been to at least like a dozen PR review clubs. Like the first one I went to, I like studied for like two days, and then I like couldn’t figure out how to join the IRC channel. Like I’ve never used IRC before. But yeah. And then now I’m like hosting one and I got to like, look back and see like, Oh, like I kind of know how to review PRs now. And so, you know, like I had been looking, it was on one of my own PRs and I hadn’t been looking at that code for like three, four months at that point. And so to me, it was also a way of being like, I kind of understand how this code works and what is really obvious to me. I now need to like figure out how to guide someone through the process of how I got to this particular solution.

Gloria Zhao:

And of course, like I noticed that the mental model that I was talking about about around security and performance and DOS vectors, like I had kind of built into a more concrete thing and explicitly turning them into questions on my own PR was also a really good exercise for me. And that was really fun. And then, you know, like hosting the IRC meeting itself I was like, I was so like in the zone, it was like the most, one of the most like nerve-racking things I’d ever done. I think I like tweeted the hour before I was like, Oh my God, I’m so nervous I put on makeup for an IRC meeting. That was really funny. Yeah. I was like sweating bullets. Like I’m like, I’m so glad there’s no video, but like, you know, if you looked at what I was doing, I was just like typing on my computer. Like yes, that’s right. Yeah, it’s really, it makes people really, I think it makes me very self conscious for people to look at my code. You know, it’s like a very personal thing.

Stephan Livera:

I didn’t know that people could see that!

Gloria Zhao:

Yeah. yeah, they were like looking at like, you know, my style and Oh yeah. It’s scary, but it’s really rewarding for sure.

Stephan Livera:

So the cool thing with some of these, well, because a lot of Bitcoin core stuff, it’s just all transparent and out in the open, so anyone can go and see the core review club transcript. And so it’s there and you can sort of see the questions that some of the other Bitcoin developers are asking. And so you were also asking some interesting questions in terms of guiding the discussion to be about certain concepts right saying, okay, you know what’s ATMP for example. So tell us a little bit about some of the kinds of questions that people were asking about that pull request.

Gloria Zhao:

Yeah. So I can answer what ATMP is first. Yeah, so what I was touching was ATMP or accept to memory pool, and that is the main interface through which we handle unconfirmed transactions. So something that was broadcast to us from our peers or something submitted to through one of our clients, like RPC or our wallet. And so, because it is an interface exposed through which people can send you unconfirmed and even invalid transactions, the main concern there is DOS protection denial of service attacks, right? Because if someone can very cheaply literally in an invalid transaction and take up a lot of your resources, that can be really dangerous. And this is different from say, if you were to receive like a block where the first thing you do is validate the header and the proof of work, like it’s very expensive for someone to DOS you that way.

Gloria Zhao:

But you know, ATMP is like a very kind of touchy piece of code. So even though like the total number of lines changed on my PR is very small. I think a lot of people are really concerned. Were really concerned about the performance, which is really, really heavily tied to denial of service. But in my case, just as a disclaimer because we’re only talking about client okay, so sorry, let me backtrack. Cool. Okay. So in my PR we’re touching ATMP, but there’s a completely different adversarial model when we’re talking about things coming in from our peers versus coming in through our clients, because our clients through like RPC or something, that’s privileged, like it’s usually like the node operator themselves, like they’re just connecting their own wallet versus a peer could be anyone on the, on the internet. Right. So, because I was touching ATMP, but only in a client like perspective for me, I was saying like, okay, this, like, you know, DOSing is not really a concern here, but of course, you know we talked about that at length during the PR Review club.

Stephan Livera:

Gotcha. And there was also some discussion around checking the fee you know, at what point should Bitcoin core check the fee and when does it need to, you know, is it before the broadcast or where should it be done? Could you just spell out a little bit of the thinking around that?

Gloria Zhao:

Yeah. Yeah. So at the end of the day, Bitcoin core is software and there’s a lot of like software engineering best practices that, you know, apply here as well. So checking a fee for a client. Okay. So for context, my PR is talking about absurd fees. So we want to protect our users from absurd fees, say there’s a bug in their wallet. And they accidentally made a transaction that has like, I don’t know, like many, like several Bitcoins, like per byte or something ridiculous like that. That’s almost certainly a mistake. So the node Bitcoin core, wants to bake in some logic there around like, okay, if someone does this, then we want to reject the transaction. But do we do that in the Bitcoin core client or we, or do we do that during validation? And you know, the answer is a software engineering best practices question of like, we want a clean interface for ATMP, which handles validation and mempool logic. It shouldn’t be responsible for handling like client specific logic. It’s like, we still want to protect users from absurd fees, but it’s like a question of like where we do it and do we want to be consistent? Or like if we did it in ATMP, then it might not be consistent across all of the transactions.

Stephan Livera:

Great. And so, as I understand from the process, then there might be some feedback that comes through and then you basically address that feedback and then put up a new version and say, okay, can you guys re review it? And then from that point, you know, assuming it’s all good, then that’s where it can get merged in and potentially packaged in as part of the next release. Correct?

Gloria Zhao:

Yeah. Yeah.

Stephan Livera:

All right. So I also wanted to chat a little bit about your map of the Bitcoin network blog post, which you did back in July. So can you tell us, first of all, why did you write this one?

Gloria Zhao:

Yeah, I, well, okay. So I wanted a map because I think throughout my journey, I’ve been in Bitcoin. Well, I’ve been talking about Bitcoin and reading about Bitcoin for like at least three years now. And it gets really confusing when people compare nodes. So first of all, people have a different definition of node often, and then they’re like, Oh, you know, and then there’s like these users and there’s miners and there’s developers, but, you know, developers are also users and users can be miners. And then, Oh, we have like light clients and light clients, are clients to nodes, but then those can also be clients and servers. And, you know, like it was very unclear and ambiguous when people use terms like node, like client, full node and like a wallet, for example, like you can, you can literally have a wallet can be a node.

Gloria Zhao:

Technically, you know, there were so many, there’s like a grey area and like all of these terms, and I wanted to at least give what my definitions that I’ve kind of landed on so that if someone’s like, okay, you just said, node as a server or node as a client, like what do you mean by that? They can kind of refer to this as like a, okay, these are all relative terms, right? A node can be a server, a node can be a client in any given situation. Different types of nodes, do these things. Given an individual node, it can have all these different configurations of, you know, it might be downloading from another peer. And in that case, it’s a client, but it might be servicing a SPV node, or it might have clients through like RPC. And in that case, it’s a server. And then, you know, how does it make connections to other nodes? And then, so that I can kind of say like, okay, I can’t draw you an exact map of what Bitcoin looks like at any given point in time, but given these terms that are used, how can you orient yourself around the terminology that’s being used and, you know, whatever code or like article that you’re reading.

Stephan Livera:

Yeah. So, I mean, we’ve got these different types of nodes. So for example, full node, archive node, mining node, light clients, can you just spell out what are some of the differences there between those types of nodes?

Gloria Zhao:

Yeah. Yeah. So I think the main thing that I was always confused about was is a node, a server or a client? Right. And it depends on the type of node. So for example, let’s say you’ve just started your node. It’s in initial block download in that case, it can’t really service anyone. It’s more of a client, right? Because it’s getting serviced from other nodes that it’s downloading blocks from, but then a node often has clients. I mean, why would you run a node for no reason, right. Well, other than to, you know, but like, so it usually has clients such as, you know, your wallet or maybe you’re running a Block Explorer that’s like querying the node through RPC interface. And in that case, your node is a server, right. And so basically what your node is defined as.

Gloria Zhao:

It depends on its connection to whatever it’s talking to, as well as what services it is able to provide. So for example, you asked about pruning nodes and archival nodes. Full nodes are just nodes that can validate blocks and transactions, right. But whether or not you store the entire history of the blockchain is actually not very relevant to whether or not you’re able to validate, right. Because the state that you’re actually using is the UTXO set. And that tells you like what coins can be spent and you know, what signatures would be valid to redeem these coins. Right. you don’t actually look into your blocks database. Like every single time you want to validate a transaction not anymore, at least. So you can be a full node, whether or not you store the entire blockchain. So if you store the entire blockchain, you are an archival node and people want to connect to you during initial block download because you’re able to serve them the old blocks.

Gloria Zhao:

Whereas a pruned node is, you know, that like only keeps the last two or at least the last two days worth of blocks so that you’re able to reorganize is if there’s a fork. But you know, it doesn’t need to be able to arbitrarily serve, you know, whatever block or transaction to someone that asks for it. So yeah, like nodes, when they connect with each other, they’ll do a version handshake where they negotiate like, Hey, this is what I’m able to provide. I can serve you arbitrary blocks from any point in time in the past, or I am only able to, you know, but I’m like, I’m just a node network or like, I’m just a full node without, you know, everything in the past. Or let’s say I serve bloom filters or I serve compact block filters. You know, there’s a whole list of things that nodes are willing to provide and they’ll negotiate that relationship when they connect to each other.

Stephan Livera:

Excellent. And an interesting point there is maybe this is a common confusion, but a pruned node is technically still a full node.

Gloria Zhao:

Yes.

Stephan Livera:

It’s just not an archive node. And I think that’s an important point as well, that you spell out, even in your with, you’ve got the Venn diagrams, they’re kind of showing, okay, this is what’s inside there and what’s not. And I think another really interesting part about this article is you talk a little bit about the different types of peer to peer connections in Bitcoin. So can you tell us a little bit about those?

Gloria Zhao:

Yeah. Okay. We’re getting pretty technical here. Yeah. so when two nodes connect, like I said, they’ll do a version handshake. But that connection is always initiated by one of those peers. Like someone says, Hey, can I connect to you? And you know, and then they start deciding whether or not they want to. So when you’re the one that initiates, you are creating an outbound connection and when someone initiates a connection to you, that’s an inbound connection. And of course there’s also manual connection. So that’s a different model because usually it’s like, Oh, that’s my friend. I’m going to connect our nodes. Or like, that’s my wallet. And I want to connect them or, you know, whatever it is. So with these inbound outbound connections, it’s always asymmetric. And a lot of what we care about in these situations is two things.

Gloria Zhao:

We want accessibility, because we want anyone to be able to initiate connections and become a part of a network without, you know, having however many years of history or, you know, this is the whole point of Bitcoin. And then also preserving privacy about the details of how this node is configured. So the example that I used in the article was block relay only connections and blocks only nodes. So if you’re a blocks only node basically you don’t keep a mempool. You don’t care about unconfirmed transactions, but of course, you’re, you still keep a UTXO. So set so that you can validate the transactions within blocks that are relayed to you. However, if someone were to know that you are a blocks only connection blocks only node, sorry. If someone were to know that you’re a blocks only node, then they would know that any transaction that is sent from you is your own transaction.

Gloria Zhao:

Like it comes from your wallet or, you know, one of your clients, because you wouldn’t be accepting someone’s transaction and then relaying it. That would mean that, you know, you validated this unconfirmed transaction, right?

Stephan Livera:

Clever!

Gloria Zhao:

Yeah. So this is a privacy concern. If someone is to be able to tell that you’re a, blocks only note, however, in, in the types of connections that we renegotiate, you’re allowed to say, I only want to send blocks. I don’t care about transactions. And there are connection types that are blocks only, or it’s called block relay only. So no transaction relay. And so if someone connects to someone and they say, I only want blocks, there is some ambiguity and okay, maybe this person only wants blocks from me. And it doesn’t necessarily mean that they’re a blocks only node. Right? So then there’s nothing that you’re able to infer from a block really only inbound connection where you’re, you’re only communicating blocks because it could just mean that they want blocks only from you, but they’re, doing full really everywhere else. And so that is a privacy win to be, to have these different types of connections negotiate it.

Stephan Livera:

That’s really cool. Yeah. I really liked this post. It’s got a lot of good simplifications and explanations. So I recommend listeners you go and check that out. So I also wanted to chat a little bit about funding in the space and how developers can get funded. So I know for instance, some developers have the github sponsors thing. Some of them take Bitcoin donations and others are properly funded with a grant from a, you know, from one of the larger I guess organizations in the space or sometimes an exchange. So are there any that you are currently exploring or you’re using right now?

Gloria Zhao:

I haven’t really thought about funding. I guess I have like a github sponsors page, but you know, it’s just for fun. I’m still working on my degree, so I’m not graduating until December. And like, hopefully I can continue to work on Bitcoin after that. Well, I will, like, no matter what it takes, I will still work on Bitcoin. But you know I guess I’ll cross that bridge when I get to it. I’m just like really happy. Like I just, all I want to do is work on Bitcoin and that’s all I care about right now, essentially, I guess this is the first time in my life where I’ve been like, I’m just going to do what I want to do instead of, you know, what’s going to get me a job or, you know, what’s gonna look good on my resume. So yeah, I’m just happy to be here. Of course. You know, if someone wants to give me money, I’m not going to say no, but I haven’t really thought about funding.

Stephan Livera:

Oh, that’s great. Yeah. I mean, for listeners interested, you can see a Gloria’s GitHub profile. Do you have any particular priorities in terms of things that you want to work on in terms of Bitcoin development?

Gloria Zhao:

Yeah. Yeah. I’m really interested in the general idea of looking at packages of transactions rather than individual transactions, because we’re not able to do that in many ways. Or like, let me explain. So we have a RPC method called test mempool accept where you’re able to dry run the acceptance of a transaction to see if it would be valid and accepted to the mempool, but it only accepts one transaction at a time because essentially if you wanted to do a chain of transactions, like I don’t know, let’s say you have like a lightning thing and you’re like, okay, I want to make sure that these child transactions are going to work if I were to broadcast them, but I don’t want to actually submit them to the mempool just yet. We’re not able to do that for more than one transaction because essentially, like you would need to make like a scratch space copy of the mempool in order to like, look at multiple applications of like state changes, right?

Gloria Zhao:

Like you can only do, you can only look at one transaction right now, essentially. And then same thing for like packages or transactions. We’d like to think about fees for an entire package of transactions. But each like right now, if you were to use child pays for parent, for example, each individual transaction needs to pass mempool policy in order to be considered together. And I think that we could make some changes to the mempool to make it a more well, I haven’t actually done this yet just as a disclaimer, but I’m very interested in seeing how we can play around with the mempool data structures to see how we can reason about multiple transactions essentially. And this can kind of pave the road for like package relay and a bunch of other things that I think are really exciting as well.

Stephan Livera:

So Gloria, what’s package relay?

Gloria Zhao:

Yeah. So very good question. I think a lot of people have been talking about package relay on in the Bitcoin core community, but maybe less so outside, but it’s this idea of right now we relay transactions one at a time. So if I’m trying to tell my peer about this transaction, or, you know, even if I have a chain of transactions that, you know, rely on each other, I send them one at a time and my peers will apply them using ATMP one at a time. And even if together they’re all valid and the fee is perfectly acceptable as a package, nodes will not consider them at all, unless they individually all meet the fee requirements of the policy requirements of their node. And you know, this is less than ideal. A lot of times say you’re like a lightning watchtower.

Gloria Zhao:

You don’t always have control over the fee of a transaction and you’d want to like bump it with, you know, a child pays for parent or something. But, you know, just in general, we’d like to be able to tell peers like, Hey man, like, I’m going to send you a package of transactions. Okay. Like, please look at them all together instead of individually. Cause you know, together, they make sense, but not individually, but of course like a lot of things that are touching ATMP and especially things coming from peers, especially validation in large groups of transactions that may potentially be invalid. Like I said, this is like a potential denial of service attack vector. So there’s a lot of open questions around how are we going to design this? And that’s why I’m not saying like, Oh, my project is package relay because it’s a very non trivial thing to do. But a precursor to that is how do we reason about transactions as a package.

Stephan Livera:

I see, and just turning to Bitcoin more broadly. Are there any other particular areas that you are interested in? I mean, like for example, are you into lightning or are you more like, are there any other aspects that you like or are you kind of more really focused into Bitcoin core and the protocol?

Gloria Zhao:

Yeah, well it’s, well, it definitely isn’t that I don’t find other things interesting it’s that I have very limited time. Of course, like everyone and I can like barely keep up with the PRs that are open on Bitcoin core right now. So it’s what I’m focused on right now, but I don’t hesitate to say lightning is super cool. I wish I knew more about it. I want to run a lightning node. Like all of those things. I’m very interested in all things Bitcoin only of course. But yeah, I’m mostly focused on the Bitcoin core right now.

Stephan Livera:

So other than the work you’re doing more directly, what else are you kind of excited to see coming into Bitcoin core?

Gloria Zhao:

Taproot? Obviously. Yeah. Like I guess Taproot is what most people are focused on right now. And I also really actually, I’m not sure how to answer this question, to be honest.

Stephan Livera:

It’s okay. I mean, you don’t have to, it takes a lot of work to kind of get involved into those other aspects that are coming.

Gloria Zhao:

Yeah. Well it’s like, I like Taproot. There’s a couple other peers that I think are really interesting, but it might not be as sexy to hear about on a podcast. It’s like some of the tests framework additions, but that’s probably not very relevant to users.

Stephan Livera:

Yeah, no, that’s totally cool. The test suite is not exactly as easy to speak about, is it? Yeah.

Gloria Zhao:

So one thing that I really appreciated about Bitcoin is, or Bitcoin core, sorry, one thing I really appreciate about Bitcoin core is how thoroughly everything is tested and not to say that it’s perfect. Of course. But you know, the test framework is literally like, ah, let’s just spin up a couple of regtest nodes and like we’ll do that in like two seconds. And that’s, I think like I haven’t seen that very much in other projects. But of course there’s a lot of things that we’re not able to mock in the test framework. Like for example, right now, Amiti’s working on mocking different types of peer to peer connections and that’s really, really exciting. But also for example, a lot of the ways that we create transactions in the test framework is through the wallet, the core wallet.

Gloria Zhao:

And, you know, we’d like to be able to have, you know, like just a light little like framework, like utility function so that we could just create raw transactions from our test framework code, because, you know, we don’t want to have to compile the wallet every single time in order to test like some P2P function, for example. So, you know, there’s a couple of things that are missing and there’s ways to improve the test code. But yeah, I only talk about this because I started mostly in the test framework. It’s written in Python, which means it’s a lot more accessible than the C++ portion of Bitcoin core. And I just I’ve spent so much time in it that I get really excited whenever, you know, there are new additions to it.

Stephan Livera:

Well, look, I’ve really enjoyed chatting with you, Gloria. Have you got anywhere listeners can find you online?

Gloria Zhao:

Yeah. I’m on Twitter. I just changed my handle to @glozow so that’s probably the best way to find me.

Stephan Livera:

Awesome. Well, thank you so much for joining me today. Thank you.

Gloria Zhao:

Thank you so much for having me, Stephan, I really, really enjoyed this.
