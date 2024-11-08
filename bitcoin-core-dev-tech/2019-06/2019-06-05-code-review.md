---
title: Code Review
transcript_by: Bryan Bishop
date: 2019-06-05
aliases:
  - /bitcoin-core-dev-tech/2019-06-05-code-review/
---
# Code review survey and complaints

<https://twitter.com/kanzure/status/1136261311359324162>

# Introduction

I wanted to talk about the code review process for Bitcoin Core. I have done no code reviews, but following along the project for the past year I've heard that this is a pain point for the project and I think most developers would love to see it improved. I'd like to help out in some way to help infuse some energy to help with code reviews. I sent out a survey. 11 people responded. I'll summarize the results from that, then I'd like to spend our time talking about ideas for how to improve some of the areas of the process. I have some concrete experiments that might make sense but I want to get feedback from folks and will need some volunteers.

# Survey results

11 people responded, and all of them were open to experimentation. All but 2 of the responses are developers who want to do more code reviews than they do today. I think there's an interest in doing more. There might be a guilt component. Should we work on increasing guilt? We should definitely leverage it.

One of the questions was, how do you go about selecting a PR to review and then how do you go about reviewing it? There seemed to be no clear consensus process for doing that. That might be an area of improvement. People were generally satisfied with code review quality but not very satisfied. I think most people had a desire to improve coordination around reviewing PRs.

How do we decide what to review? What would encourage more reviews? Three things that got a lot of responses in the survey was- for encouraging PR reviews, one was identifying PRs for reviews, and PR authors stating a better motivation for the PR, and more tests along with PRs. Those all got 5-7 responses out of the 11.

Developers generally don't know how many hours they spend on review. One hour reviews are very different from a 5 minute review. Maybe we should ask people to track this. Would it be valuable to track and monitor metrics on code reviews? There maybe three people that said yes, but most people thought no, it wasn't a high enough ROI.

We could keep a list of people who found a bug in someone else's PRs. Git has support for review-by and ACK-by. It's a convention not a feature. The linux kernel project does that, for example. It's freeform text that tools recognize.

It would be worthwhile to credit people in releases for review work, even if they didn't write code themselves. This can be pulled from the github API.

We have the high priority for review list. I don't have the impression that this system works very well.

# Experiments

I have 5-6 experiments I could walk through.

There's like 5-6 PRs in the high priority list. I could volunteer to help coordinate reviews for those by working with the author of the PR to identify who are candidate reviewers for the PR and then go out and see if those people will review the PR and nudge them and try to work out schedules. Like do we think we can get this done within a one week timeframe or some kind of timeframe? I would have to get from you guys, what's reasonable in terms of duration?

I think in general it would be good if there was a social convention where it is alright to prod someone like "hey I want you to review that" or someone coordinating that. We can't quite have authors choosing the only reviewers, but they can nudge them. Some people don't feel comfortable asking for review, so having a coordinator can help that out. It's not just a review bag, it's using knowledge to coordinate review requests. If there's one person coordinating then they will be able to push back on reviews for certain things if someone is overloaded, since the coordinator has a better view of what people are looking at.

When will appropriate reviewers actually have time for review? That will help set expectations about timeline. This helps everyone plan.

If having a coordinator works, then I would like to codify it so that it could scale better. Maybe it's a project manager activity. Phase one, I would be doing it to learn.

One of the things you would learn is figuring what parts of the code have to go to whom. Github has support for MAINTAINERS file. Unfortunately our directory structure isn't directly compatible with that.

I would like to see more emphasis on Concept ACKs. Concept ACKs can help figure out review prioritization. Sometimes it's the opposite problem. Often we have lack of an initial Concept NACK, and then it takes a few things for someone to come up and show they disagree about it. High priority list should generally be concept ACKed. Nothing should get on the list if it's not concept ACKed. ((Some disagreement here.)) Previously the policy was "everyone gets one thing on the list" and it being on the list is not a judgement or anything, but it would be a good use of meeting time to turn that into a ... each person gets to nominate something (not necessarily your own PR). At the very least there should be some judgement, and if it's not really high priority then it should at least be a concept ACK, it is ridiculous to have something on there that we don't want merged. But sometimes giving a concept ACK is non-trivial to give, and it requires discussion sometime. If you find a PR that has no comments and you think it's interesting, then say "I think this might be interesting" at least.

I would focus on stale PRs, and either get them NACKed or get them some review. Getting concept ACKs is a way to get a PR author to feel more encouraged.

Sometimes I learn about PRs weeks later. Use github assignment and assign them to a PR? You can assign non-maintainers.

In our workflow, it's kind of unusual that we generally require multiple reviews from multiple people. It's not like you can assign review to a single person, because a single person is not enough. But assign to a person who is- when you get assigned, it is your job to maintain the review process or something. It's the authors job to merge-- especially for high-priority list. For new contributors it's different.

In the linux kernel, there are subsystem maintainers and specialists that understand different parts and a lot more interested in those subsystems. There are ways for other developers to sign up to pay attention to that type of problem. I wonder if it would help if people can volunteer.  There's already tags on the github issues added by fanquake within minutes.

The original purpose of high priority for review, it was originally about things that are blocking people. This was a big motivator. You have to motivate the PR for high-priority for review list inclusion. The high-priority page should have some text or description, like who proposed it and why. You should do this ideally during the meeting, but having descriptions could help on a page somewhere.

The high-priority list for review is sometimes really hard for reviewers, they are difficult PRs. That's normal. I've heard that issue from others. There is a natural tendency to review the smaller PRs because you can knock them out quick. The more impactful ones get either delayed more than they should or never get reviewed. So how would we improve that situation? One idea is that nobody can have more than 5 PRs open at a time. That would cut open PRs to 100 or 150 PRs. It would ratelimit work. This might encourage people to make bigger PRs. But you should split it up and focus on one thing at a time. But in practice they submit multiple PRs. When a bot auto-closes my PR and says sorry you have too many open PRs, my response isn't going to be "meh" instead I'm going to abandon it. But part of the problem is that you're forcing everyone to do priority management. As a reviewer, if I see someone with a sequence of multiple PRs, I will like say, oh this one includes this one, I'll just look at the first one.

The big important PRs don't get reviews because they are too complicated to understand. The 5 PR limit doesn't address that in any way. What would address it? Smaller PRs, maybe. You should be able to comment partially on a PR and come back to it later. At Facebook, when they make a PR, they review it commit by commit, and every commit that gets reviewed gets immediately merged in. But this might not work for us, like refactoring commits if the end result isn't going to go anywhere. If you do it commit-by-commit, the PRs get smaller, and you get things merged in.

On the 5 PR limit, right now I have open PRs and right now I don't have a reason to push people. But if I have a limit then I have to start pushing people. Concept ACK vs nit stuff, I haven't thought about it, I am going ot think about it, but I am not going to go in and write a bunch of nits.

Do we want to make the in-meeting decide high priority for reviews be automatic concept ACKs? Like you have a right during the meeting to argue that something should be on the list? Some people can't be present in the meeting, so you can't make it so that you must defend it during the meeting. The author should make a clear case in the PR. In the meeting, they can reference the PR and then you click on it and see the motivation. The person who puts it on the high priority list should either verify it's been concept ACKs, or say it needs concept ACKs. Deciding what goes on the high priority list, if it's "everyone gets to nominate one" then we don't need a meeting for that. It feels like a useful use of meeting time to use that meeting to concept ACK things. But there's the issue of not everyone can be present all the time. There shouldn't be final decisions in the meeting, but discussing things is fine. Bugfixes before a release, those should be automatically concept ACKed. Maybe in github, have subprojects for high priority.

How about, instead of a 5 PR limit, how about the author can tag a priority level? But this didn't work in the past. How do they decide what is high priority? As a PR author, one of the things asked in the survey- if various things in the PR would encourage you to review it more. Stating a better motivation. Providing tests. These are two things that got good responses in the survey. Two others I listed but didn't get votes- is including a desing doc, and including a guide on how to review this PR. We can discuss the merits of each of these. This would make some PRs more reviewable. As a PR author, if one of them you feel is the most important or higher priority, put in the work to do these extra things and that's the indication that it is high priority, because you've made it easier to review. As a project, we could either have that as a criteria to be on the high priority list, or we could have another list which is a vetted quality PR list, basically ones that it has been vetted that it has a good motivation, it has tests, it has a design doc, etc. This could also improve the visibility of PRs if they are looking for PRs to review and they know in that list the author is taking care to make them as reviewable as possible.

Do we want to think about concept ACKs and code review ACKs as separate stages? This is something that annoys me personally, when like, a highly experimental vague idea PR and it gets buried under code nits. You don't even want to go in there and talk about the concept any more. I don't know if more structure is the solution for this. You don't do actual code nit style review until.... not sure this is avoidable. The rust integration into Bitcoin Core PR was like a very experimental thing, and the first comment was NACK. But even if we come up with this tag system, I fear it might not work. Concept discussion in issues? Suhas has been trying that. Maybe a needs-concept-ACK tag. Maybe the author can request that this needs concept ACK, and one of the maintainers would add this tag. This means the discussion should be limited to the high-level ideas. Is it possible to add issues to the high priority for review list, that might be a good way to have a concept discussion. We could ask the github CEO to make it impossible to make line comments impossible, because it makes the thread unreadable, because the rest of the reviewers were looking at code nits. The clutter might be a good comment for the github CEO. You get an email every time someone comments, and you might not see the concept discussion anymore. Maybe a checkbox for "this is a nit" and then don't trigger email notification for that. You could then configure, don't get notifications for nits, or filter them out on the visibility. Sometimes you don't want to comment because it will blow up someone's inbox. So it's both notification clutter, and also the web interface gets cluttered.

As an author, you should add someone to the review, if they fix something meaningful. The author should take the responsibility to-- either add someone as a commit, or add a "thanks to so-and-so". Github supports coauthors now. You don't want to give them the ability to push, but maybe we should talk about them recognizing code authors. However you pick someone to shout out to, it's a judgement call, don't spam. In the past, we have remembered to go back and credit someone for reporting a bug. We could be more thoughtful about doing that during the review process, and not just out-of-band bug reports.

A lot of the review is more nit-picky rather than deep thinking about what this is trying to achieve or more holistic. How could we encourage higher quality reviews? The author could offer a guide for review. But this doesn't achieve the thing you want. This is like a checklist for what you have reviewed; but ideally the reviewer comes up with their own plan for review to figure out what the issues are. When you write a tACK or something, you should write your own review for the steps you did, or the steps you recommend. When someone ACKs, what did they actually do? Did they spend 5 minutes on it, or 5 hours on it? Maybe replace ACKs with explanation, like "I checked these hashes" or "ACK, I verified gpg keys". Maybe we should get rid of just plain ACK and try to get some explanation. Also, you should include the commit ID with the ACK message. Maybe a button on the interface to ACK a specific commit. But this might lead to more spurious ACKs.

How many of you are reviewing on github versus locally?

# Video streaming

Someone was using twitch to livestream their Bitcoin Core coding. This was inspired by Lisa Neigut who does it on c-lightning. I think it's an interesting way to help educate people and socialize the development process. I did it as an experiment just once so far. It could be a useful practice. I would benefit from watching some of you guys do your work. We could do a webshow like that. You could make livestreams mandatory so you could check what people did during the review. What if we had the 3 best code reviewers doing that, would the rest of you not be interested in observing that for a few hours? If you have a PR, it could be helpful for the author of the PR to go through the code and use a video stream just as a way of presenting the PR and talking about it. We shouldn't encourage them to migrate away from text, but some users probably work better with video and voice. Also there are some code review podcasts. Some people might like video more than just text reviewing. I did some live coding of a lightning client in Munich, and some people found it interesting to hear you walk through your process while writing software.

I think it would be helpful if Bitcoin Core developers made videos like that. I think there's a lot to learn from you guys. So consider doing it, either for reviews or writing code. Let's not make this an expectation though. But also, programming is generally slow not just typing it out fast. Googling "how to do a for loop in python" etc. Well, people watch cricket games, don't underestimate what people find interesting.

# Bitcoin Core review club

We have a weekly Bitcoin Core review club. We're trying to get more reviewers. Everyone here is welcome to join. It's on IRC. So far it works. It's in 3 hours actually. If you want to do one on video, then maybe.

# Back to reviews

When coordinating reviews, there are limtiations on tags- how often are people going to look for tags? There's a lot of value in getting to know the different developers, as a coordinator. Maybe begin to form different interest groups, not exactly subsystem maintainers but maybe people can volunteer for different clubs.

The github dashboard is useless. But maybe it could say "hey you recently worked on this code, and this other PR modifies it or something". Or blame automation. It's hard to automate relevance in terms of who is actually capable of reviewing it, or who is interested in that. The github tags list is not something that everyone is using all the time. An email notification isn't quite right. Maybe a webpage, but it has to be personalized to each user. So maybe a review request web application? Or the coordinator can do it manually, and then automate it eventually.

A coordinator can decide not to coordinate something; so in a way the coordinator becomes a decider.

For particular PRs, like consensus code or p2p-critical code, could some PRs benefit from synchronized group review whether over chat, video or face to face, like a meeting like this? Would that improve the quality of finding bugs, sharing best practices? This would be useful for concept ACKs. Does anyone at an office have a coordinated time for reviews? Like at Chaincode? No.  Could have a group chatroom that is open and running. There's a #bitcoin-builds channel, because some of this requires discussion. Have a separate channel for PRs and reviews.

Which PRs need concept ACKs and which don't? It would be better to communicate this. Probably not everyone is not capable of making that determination.

We could ask for nits to be sent privately to PR authors. This would de-clutter the github UI.

There is a regular "state of the repo" issue opened up regularly. Can you self concept-ACk your own PR?

We used to have a way to list out trivial pull requests, instead of the big consensus changes. Right now our policy is to reject any PR that updates copyright headers or some other things. We've been drowning up in- there's a lot of fchanges like linters and things going into that. Does anyone use those tools locally? Are they useful? A bunch of them are broken on Mac. The UX of these tools are not super intuitive. I want something like "check everything since master". Right now I have to give it a range or some incantation I don't know. I have a simple script that I use. It should be something like "script/make\_linting\_easy.sh" or something.

There's a massive header refactoring PR open right now. There was a problem with this one. There's a lot of time spent fixing and maintaining scripts to do things. The linters are useful because they do point at things we don't really look at usually. So there should be an easy button locally that fixes this up locally, and then submit a PR? I always keep a travis-ci tab open because I know it's going to blow up. But maybe a pre-commit git hook, and some tutorial on how to do that with two easy steps or something, that could help. It used to be that travis-ci was faster than my local computer but right now I think it's the other way around.

We could spin up development VMs for reviewing PRs, automatically. So it would make it easier to build and run tests. Users could login with their github login oauth or something. For wallet tests, maybe just run wallet tests only. That would be nice. Sometimes it doesn't do that. Are you compiling with --disable-wallet?

I am looking forward to seeing how these ideas pan out. John recently mentioned conflicts are an issue with respect to rebasing. So I started opening up my PRs in draft, then wait to see the conflicts, then decide whether I want to continue with that pull request.


