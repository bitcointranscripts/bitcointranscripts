---
title: Demystifying and Understanding Bitcoin Core Development
transcript_by: realdezzy via review.btctranscripts.com
media: https://www.youtube.com/watch?v=uOhkN4nefpI
tags:
  - bitcoin-core
  - developer-tools
  - soft-fork-activation
speakers:
  - Sjors Provoost
  - Mike Schmidt
  - James O'Beirne
  - Rodolfo Novak
date: 2023-02-22
---
## Intro

NVK: 00:00:40

Today, we're going to be talking about Bitcoin Core development and trying to demystify it, maybe sort of like shed some light.
So, some of the FUD goes away and new FUD comes in maybe, who knows?

## Guest introductions

NVK: 00:00:51

I have this awesome panel with me.
I have a James O'Beirne.
Hi James.

James O'Beirne: 00:00:56

Hi, good to be here.

NVK: 00:00:58

Thanks for coming.
Sjors.

Sjors Provoost: 00:01:00

Hello.

NVK: 00:01:02

Thanks for coming back.
And Mike.

Mike Schmidt: 00:01:05

Good to see you again.

NVK: 00:01:07

Do you guys want to tell the audience what you guys do related to Core?

James O'Beirne: 00:01:12

So yeah, my name is James And I've done work on Bitcoin Core since 2015, when I made a patch that's actually kind of coming back into relevance.
It obfuscated the chain state contents, anything that's loaded into memory because we were having this problem where Norton Antivirus software on Windows platforms would actually wipe out the chain data because someone had embedded viral signatures in the operations which is pretty funny.
Now, we're talking about doing that for blocks, of course with the rise of inscriptions.
Since 2018 I've worked full-time on Bitcoin Core and related projects.

NVK: 00:01:57

Cool.
Sjors.

Sjors Provoost: 00:01:59

I've been working on Bitcoin Core since 2017.
I mostly review stuff hanging around in the wallet, but I also like to test completely random stuff and review it.
So I've looked at some of James' work and other people's.

NVK: 00:02:13

Cool, and Mike?

Mike Schmidt: 00:02:15

I've never contributed to Bitcoin Core.
I'm the outsider on this panel, but I do have some I think interesting insights into the funding world around Bitcoin Core, as well as some of the supporting efforts that aren't necessarily the zeros and ones that James and Sjors are doing, but support some of those efforts in terms of funding, education, and news.
So I actually got my sort of break into the Bitcoin world by working at Blockstream and then actually met James through Bitcoin Optech, one of the initiatives that he helped start.
And so I helped contribute at Optech and also executive director at Brink where we actually fund Bitcoin open source developers.
So that's sort of my background and perspective.

NVK: 00:03:07

You're being very short there on Optech, which is an absolutely fantastic resource that I believe started to try to educate the industry on what's going on with Bitcoin Core development, right?
Because, realistically speaking, industry has very few sort of devs that often can understand or contribute to Bitcoin Core.
People are busy building stuff to ship to customers.
And there was always this huge gap between what's going on in Bitcoin, which can seem a little messy and very opaque.
How can we sort of like let people know that these are the things that people are working on.

Mike Schmidt: 00:03:47

Yeah, I think James could probably provide a bit more of the history, but I think it was a suggestion by Adam Back that the communication lines should be opened between developers and Bitcoin businesses.
And I think Optech has done a pretty good job of digesting developments in the technical Bitcoin dev space and surfacing those to a less technical or less involved audience, including Bitcoin businesses.
I think we've done a good job of that and maybe less of a good job, and maybe there's more potential for getting more feedback from Bitcoin businesses or Bitcoin users about how folks are using the software and feedback on that.

NVK: 00:04:35

I think it's an interesting thread and the reason why I started pulling on from there is because traditionally Bitcoin Core development was sort of opaque because it's like anarchic.
People work on what they want to work.
They may not even be on GitHub per-say.
Nobody decides what gets worked on.
There's a lot of initiatives going on at the same time and they may not have people's priorities in mind.
It's whatever people want to work on.
It's very hard to keep track of that stuff.
It's very hard to understand half the time what people are working on because of the technical complexity.
And correct me if I'm wrong, but I imagine the motivation behind Optech was around the Block Wars where there was a lot of opacity, not due to anybody's intent, but it's just that there's this completely galaxy brain shit that people are working on.
And then there's the industry trying to say, "Hey, the fees are high".
This sort of like, grub brain, "fees high - I need solution".
Then there is this like millions of things going on in Bitcoin Core development that may or may not affect that.
And I got a vibe that the intent of Optech was sort of like, "Okay, look, there's this massive gap.
Can we start bridging this and involving (the) industry and sort of educating (the) industry and sort of keep tab of what people are working on".

Sjors Provoost: 00:06:03

The newsletter helps developers keep tab on what's going on.

NVK: 00:06:08

It's true.

James O'Beirne: 00:06:10

That's true.
It's really the best resource week to week for what's kind of going on.
But yeah, you're right.
Optech was founded in 2018 on the heels of the 2017 bull run fee market.
Initially, there was a lot of emphases when we would go out and talk to various members of the industry about how to kind of manage the fee market and how to use things like RBF so that exchanges were making the most efficient use of block space that they could.
What I think we found in practice many times was that exchanges were aware that they were inefficient, but they just had kind of bigger fish to fry from the standpoint of being a corporate entity with shareholders and profits to make.
The conclusion that I kind of came to was, well, If a business wants to ignore best practices and basically penalize themselves with fees, you know, it's fine with me to subsidize miners and create a robust fee market.
So I kind of exited that conversation a little bit just because I found it was very hard to get uptake and it wasn't my position to try and sort of like push people.

NVK: 00:07:19

Yeah, It's a tough position to be in just generally speaking.
Bitcoin has a set of incentives, it's money for your enemies, and everybody is using it differently and they have both overt and covert incentives or sort of intentions.
And we can't read people's minds.
We can just work with the network thinkin the worst case scenario and the best case scenario and aim somewhere where it makes sense for each feature.


Let's go back in time.
How does this whole thing started?
How did Bitcoin development start?
I mean, you have Satoshi, releases the paper.
He releases the source code, I think was on SourceForge at the time.
And conversations were had on email and on Bitcoin Talk, if I remember right.
My memory is also failing of that time.
So that's sort of like how it starts.
Satoshi has very unilateral decisions that he pushes into Bitcoin.
Like, "oh, I don't want Bitcoin block to be 32 megabytes.
It's going to be one".
So like, boom, made a change.
Push.
Nobody says anything.

## The beginning of Bitcoin development

Sjors Provoost: 00:08:28

I read some of the discussion on the Bitcoin Talk forum for when Satoshi made those changes.
I think the change to one megabyte, the discussion wasn't even about that change.
There was another change in a pull request.
I'm saying between scarecrows because he just pushed change.
There were people commenting on that, even though two lines above, there was the block size decrease.
That then makes you wonder whether there was some private communication about that change, or whether there was just no communication about the change and people didn't even know about it until much later.

NVK: 00:09:00

I like to assume there is always private communication.
I think it's a better mental model for these things.
You have to assume that people are colluding, good or bad, to try to get their preference ahead.
It's just a normal human thing to do.
It's the natural market thing to do.

Sjors Provoost: 00:09:17

And we know that Satoshi communicated directly with some people because some of the documents were released.

NVK: 00:09:23

So we start that way.
There's 50 people using Bitcoin at a time.
Then a hundred and two hundred, it kind of grew a little fast, to a few thousand people within that sort of timeline.
And the software is sort of like, nobody, it's very low stakes too.
Who in their right mind would assume that this crazy idea would work.
You'd have to be either a liar or crazy.
Especially if you're around those days you'd understand this.
It's absolutely batshit crazy.
So things are progressing, it's lower stakes so people are less intense about things and people have a lot less of their bags depending on Bitcoin.
Then we started having other people coming in and you have personalities like Gavin who tried to bring a little bit of the Linux, let's call it the benevolent dictator, which I don't think he lasted more than just a few months.
I think everybody was very sort of affirmative on the fact that he should sidestep that kind of intention.

James O'Beirne: 00:10:31

Maybe Sjors you can help me here with the history because I'm a little bit fuzzy, but I think one of the things that he kind of pushed through pretty controversially was pay to script hash.
Is that right?

Sjors Provoost: 00:10:43

My understanding (is) that that is true, but I've only read one long-form article about it.
I have not actually done any digging myself in that history.

NVK: 00:10:51

Yeah, there's also `OP_EVAL` that had like a recursive bug or something like that.
And it had to be rewinded.

Sjors Provoost: 00:10:58

Well, the word "eval" just scares the hell out of me because like in JavaScript, that's one of the ways you can get any kind of payload to execute in a browser.
So if it was doing anything like that, like just evaluating stuff-

NVK: 00:11:11

There was a lot of stuff that could be seen as either incompetence or sketchy.
This is around the time when Mike Hearn was also around and known, I don't know if it's true or not, as the guy who put the backdoor on Gmail.
I'm not going to get into it because the point of this pod is not to create drama, to put any of the guests in any position where they don't want to be.
This history is very complex, long, and unclear as well.
We're not here to discuss that on specifics.
It's not the point.
It's just to give a picture to people that don't know, that the story on this is not like your traditional open-source project where there is a core amount of people and some people actually have the literal power to decide what goes in the next release.
It's a much more complex and fluid system.

Sjors Provoost: 00:11:59

In the beginning, I'm guessing it was more like a normal open-source project and it started evolving to the point where developers realized they can't  just unilaterally change things.

## Modern Bitcoin development

NVK: 00:12:09

So let's then evolve to the point where, you know, like post Gavin era where, you know, he was still trying to split Bitcoin Core from the wallet and all that stuff.
And so like a little bit more modern history of Bitcoin, let's put it this way, where it's like, okay, so we have this sort of like more functional thing.
There's a lot of money in the system And it's like sort of like last sketchy quote-unquote kind of thing.
It's kind of like moving on to GitHub where we have a lot of people working on it.
You have issues, you have the mailing list now.
Bitcoin talks were used a lot last.
It just became sort of like more industry than a cottage industry.
Right.
So, now we have GitHub, right?
Like, and we have over what, almost 350 BIPs now.


So let's say I wanted to make a change to Bitcoin, right?
Like a non-contentious change, right?
Like I just want to tweak a button on the UI or I want to change some help docs, right?
Like how would I go about doing that?

## The process for making basic changes to Bitcoin

Sjors Provoost: 00:13:09

Well, I mean, so that's important to distinguish.
I think we've done that in, you've at least done that in other episodes.
Bitcoin Core is a giant blob of software that includes the supercritical consensus stuff that you really want to be careful with and also includes lots of other stuff that is just software it would be nice if it was separated but that has been a decade-long project that sometimes gets some renewed attention.
But really if it was if it were separated then a lot of the things would be probably perceived as a lot less spectacular.
Because oh you're just a guy working on a Bitcoin wallet rather than oh you're working on the Bitcoin Core wallet.
It's like well you're working on the wallet that's sort of attached to Bitcoin Core like a Siamese twin and we can't take it out.
But to answer your question, how do you then contribute?
Let's say you find a typo in the README, you go to github.com, you make what is called a fork.
I think there's just one button in GitHub that says fork the repo.
Then on your own computer, you get some code editor or for read me just notepad, I guess.
You fix the typo, then you have to figure out how Git works, but you can download something like the GitHub Desktop Client, which is pretty user-friendly.
You make a commit, then on your own branch, you push the branch.
That's the jargon, but you basically submit a pull request, which then other people can see as, hey, some person and they'll see your picture or whatever pseudonym you picked, wants to make a change to Bitcoin, and other reviewers can then see what that change is.
So they'll see only one line changed, it's just a readme file, then they'll say, okay, that looks good to me.
In the case of like a simple typo fix, they'll say that, or you know, the discussion will be a bit longer.
And then if enough people have said that it's okay, which in the case of a typo would probably be just one person saying it's okay, one of the maintainers, we can I guess talk about it later, will hit the merge button?
And that merge button basically puts your change into the master branch.
And then it's just part of the Bitcoin software.
And then at some point, it gets released.

James O'Beirne: 00:15:12

But I think let me, yeah, let me pick up on that part of the story, because I think this is where Bitcoin gets very, very interesting and diverges from a lot of other, say application development.
Like, if you're using some app on your phone, that is updated typically on kind of a push model.
So like the developer pushes out a new update and then, you know, iOS or Android or whatever, we'll sort of like download that application involuntarily and give you a new version of it.
When, when Bitcoin is released roughly every six months, users of Bitcoin have to voluntarily go and update the software.
There's no automatic update process.

NVK: 00:15:53

But why is that?

James O'Beirne: 00:15:54

Yeah, I mean, it's very, very important because the idea is, aside from, you know, any kind of like deployment complexity that some kind of auto push thing would introduce.
The idea is that users should be fully aware of what changes they're opting into.
And they should sort of say, OK, yeah, I'm going to run this new version of Bitcoin that has that has these differences from the old version.

NVK: 00:16:17

Well, let's just give an example.
Say for example, like in the block wars.
Somebody goes, say like this didn't happen, but because the core devs sort of were trying to be neutral and also like, I'd imagine they'd probably be okay with me saying this, that the majority of them were for not making the blocks that huge.
So say the industry had enough weight.
Or even say they paid GitHub to block everybody out.
And that's even a better idea.
They paid GitHub to block everybody out.
They change the block size to 32 megabytes again or something.
And they make a release, right?
If their release was automated, everybody would receive that.
And now we would start making blocks with that size that were valid.
And it would be very hard to unwind that change.
You'd probably have to just ignore those and keep those big blocks going forward so you don't unwind it.
Right?
It's like, is that kind of scare?
Like, I mean, there's a lot of things that could happen.
You could have a change, you could have a hacker taking over Github.
See, there is a trend there on GitHub being centralized.
It doesn't quite work just like that.


Sjors Provoost: 00:17:26

But to go on that, into that rabbit hole, I think there was a way on Ubuntu to install a Bitcoin Core through the apt repository.
And that means if you do sudo apt install Bitcoin, that does get auto-updated.
And it gets auto-updated by whoever controls the Ubuntu repository.
So it's not even necessarily the Bitcoin Core developers.
So that's a bit scary.
But generally, you have to go and download it yourself if you want a new version.
And so you can wait until see if there's a panic on Twitter.
And if so, maybe wait a little bit.

NVK: 00:17:57

And also like and then there are the keys, right?
Like there are a bunch of people who have keys.
We're going to get into that, but there's a bunch of people who have keys and they all sign that release saying, hey, this release is good for me.
This release is good for me.
This release is good for me.
How many people are now like five or ten?
And then anybody else outside of those people who are known to have those keys also can do that, right, with Gideon.
Like anybody can go and sign it and say, this one is good for me.
So essentially you have a web of trust and you're vouching for that software because most people can't read the software.

Sjors Provoost: 00:18:27

Yeah, though you have to sort of distinguish what exactly a Git signature means, so, or Gideon in the old days.
I personally think the only thing it means is that the source code matches the binary.
It is not necessarily like a seal of approval of the actual source code.
So you may have some disagreements on that.
Like I've git signed Knots, Knots, Luke Dash's version of Bitcoin Core.
And I have not looked at that code myself.
So I'm only I'm saying is like, if it's malware, it's because the source code was malware.

NVK: 00:18:59

You know, It's kind of like a retweet, you know, like just because you retweet something doesn't mean you agree with it.

Sjors Provoost: 00:19:04

Well, but it's somewhat implies it.
So it's a bit of a gray area,

NVK: 00:19:08

but it is.
But it's still a public service.
You're at least vouching that that virus came from that source code.
You can look back and say, hey, you know, it's just from like altering this or like doing some fact-finding there.
Some audit, you could go and say, hey, you know, this release was that source code.

James O'Beirne: 00:19:26

But so that's, you know, this Wall Street Journal article that just came out last week called something like, oh, the six shadowy coders that control Bitcoin or whatever.

Sjors Provoost: 00:19:35

The title was terrible.
The contents weren't too bad, but they do miss the point.

James O'Beirne: 00:19:40

Yeah, I just, yeah, I think it's gonna be probably interpreted by the laymen in the wrong way because what would happen, like, let's say hypothetically, tomorrow, one of the maintainers doubled the block subsidy, right?
And then merged that change, maybe even without a pull request.
In actuality, what would happen is that the code wouldn't be released for another few months.
And then even if it were released, you know, I think probably nobody would run that binary because there would be enough people who noticed that change.
Because, you know, we do comparisons between the last release version and kind of what all the sum change set of the new version would be.
You know, they'd see that and word would get out and nobody would run the software.

NVK: 00:20:27

But there is one more thing here, right?
I mean, Bitcoin is also the consensus of the network.
So like realistically speaking, this consensus is so complex that, if people make some little changes here and there, they're likely to fork and be out of consensus.
So there's a lot of risk in that too.

Sjors Provoost: 00:20:45

Well, but let's say they did it carefully and they just did a block size doubling.
The other thing is that the software is not updated simultaneously because it's not automatic.
So you might have exchanges that are running five-year-old versions of Bitcoin Core.
That's not, that does actually happen.
So that means that as soon as there is a split, because of some conspiracy, and it would have to be between the maintainers and a bunch of miners, you'd probably get a chain split and some of the old nodes would not follow it.
Some of the updated nodes would follow it.
So there'd be all sorts of signals out there that there's something definitely bad going on.

NVK: 00:21:19

I mean, you know, a great source of security for Bitcoin is for people to run old nodes and run many versions of Bitcoin.
That backwards compatibility that we have in Bitcoin is something very special in my view.

Sjors Provoost: 00:21:31

Schmidt pointed to forkmonitor.info, which does that.

Mike Schmidt: 00:21:35

I think the BitMEX folks run a bunch of those including older Bitcoin Core, as well as some of the other implementations like the Libbitcoin or BTCD.

Sjors Provoost: 00:21:46

Yeah, I built that.
So basically, it's for BitMEX Research App.
So it runs a bunch of older nodes.
It also runs different implementations.
It used to run Bitcoin, but it became quite hard to run it.
Hopefully, they'll do a new release that's quick again.
I think it runs BTCD.

James O'Beirne: 00:22:05

While we're plugging monitoring platforms, I have BMON which runs old versions as well.
One of the interesting metrics that I was looking at actually today on BMON is the difference in mempool size between contemporary node versions and old versions.
Old versions don't permit taproot spends to propagate and so their mempools are much smaller at this point than contemporary versions.

NVK: 00:22:28

Well, I mean, now people are going to want to probably increase their mempool size so that the dickbutts fit.
The mempool is much bigger.
But you know, I find it fascinating because technically, you know, I like to think of the JPEGs now as essentially like a placeholder for interesting taproot transactions.
It's just giving us a taste of what the future is going to look like with actual mempool and block space used for things that are not extremely dense transactions.
So we could see some crazy lightning channels with like a gazillion sort of intricacies that take, you know, 300, 500 kilobytes.
And they may not be as dense with fees, for that amount of bytes.
So they might be sort of floating to the top and you might not want to lose those.
So you might want to increase that mempool space as well.
It's a nice sort of like a dry run for all that stuff with a sprinkle of drama.

James O'Beirne: 00:23:30

Totally.

## Who decides what gets worked on?

NVK: 00:23:31

Okay.
So like taking this in a slightly different direction.
Who decides what gets worked on?
So like who's the boss of Bitcoin that says, Hey, you know, I am a business and I need this done, or I am a state actor?
I want this done.
Like who decides what gets worked on?

Sjors Provoost: 00:23:51

Well, a state actor is more than welcome to make a pull request, but then it'll be the state actor that has to hire, I guess, people who work for state actors to write code.
And if that code is proper and doesn't have any sneaky backdoors in it, it might get a little bit more scrutiny because people would suspect backdoors in it.
But if it's very clear that they're not, then that code would get a bunch of people saying, this code looks good, it's doing something that's good, let's merge it.

NVK: 00:24:18

But realistically speaking, right?

Sjors Provoost: 00:24:19

So anybody who wants to change will have to do it themselves or hire somebody to do it for them.
And then even though they've written all the code, they're still screwed because now they need to convince people that it's worth reviewing and worth merging.
But even if people think it's conceptually a good idea, the review part is still gonna keep you in limbo for a very long time.

NVK: 00:24:39

You get used to rebase.

Mike Schmidt: 00:24:40

Well, this is like changing the code.

James O'Beirne: 00:24:42

Oh yeah, yeah, that's a good one.

Mike Schmidt: 00:24:44

Change the code initiative, right?
Still waiting for that PR.

Sjors Provoost: 00:24:48

Yeah, That's an example of how you're not supposed to do it.
You're spending millions of dollars screaming, please change the code.
Even though they could have spent, you know, a tenth of that to have at least a bunch of students write some actual code, which would then have problems.

NVK: 00:25:02

But that's their intent, right?
Their intent is just to cause confusion and, you know, orchestra style.

Sjors Provoost: 00:25:07

Well, it depends on what you mean by them, right?
So if you mean the Ripple founder behind it, maybe his mission is to just disrupt Bitcoin.
I don't know if that's Greenpeace mission.
I mean, maybe their mission is simply to take the money and make a bunch of noise in a very like business way, or maybe they really believe that this change is possible and that the way to get the change is to make a bunch of noise rather than to actually change the code.

NVK: 00:25:31

But you know, we saw sort of like interesting kind of like, I want to call it like time wasting, dramatic, completely irrelevant changes, like when they changed the term blacklist, right?
Because it's a symbol of oppression or whatever.
So like, you know, and GitHub actually changed from master branches to main branches, which you have to go back in and change the defaults or all your script breaks.
So anyway, so like, but let's say this, these are friendly, sort of friendly actors, right?
Like, they actually want to work on some cool stuff or they want to hire people to work on some cool stuff and things that everybody wants.
How do people go about that?
How do people just go and sort of like, Hey, I want this done?
I may not be cool there.
I want this amazing thing done and I'm willing to fund it.
How would people go about that?

James O'Beirne: 00:26:19

Yeah, I mean, this is another one of the ways that Bitcoin is really unique and unlike any other open source project or even software project in that there's really no, there's no roadmap.
There's no centralized roadmap.
There's no indication of priorities, other than occasionally individuals might write a blog post saying, hey, this is what I care about.
This is what I think should be worked on.
So if you're a new contributor looking to get involved, it's really pretty tough, because you are responsible yourself for ascertaining what's valuable to work on, and what would people be receptive to.
And then if you're, say, a company who wants something done, that's more clear than being an individual contributor and wanting to get involved, because I think your move there is to go to the GitHub issue queue, write up what you want, kind of justify it with rationale.
And that actually, might be very welcome, because there are a number of people out there who are like, yeah, I want to get involved.
I want to help this thing out.
I want to write some code.
But I just have no idea where to start.
And I mean, that's, you know, personally, that's one of the really frustrating parts of the project.
And the people who, a lot of people who have quit, I think quit out of frustration because they're just in this position where they've done some valuable work, but it just kind of sits there and languishes and they have to rebase it.
And it's just this real, like in Bitcoin, you do like, you know, 10% of the work that you do is like writing the initial prototype code draft, putting it out there.
And then the remaining 95 to 90% is like addressing feedback, rebasing, just really mundane, awful.

NVK: 00:27:57

I mean, you gotta rebase, right?
Because you wanna keep that up to date because when people do have the time to come review your PR, right?
You want that to be like tip top and ready to go because.

James O'Beirne: 00:28:09

In a mergeable state, yeah.

NVK: 00:28:11

Exactly, right?
Because that might be your chance of the year, right?

Sjors Provoost: 00:28:17

I was going to say, but then you do rebase.
And then once in a while, somebody comes by and says, Hey, don't rebase this stuff.
I want to be able to run it on top of an older branch of Bitcoin.
That's happened to me a few times, not very often, and usually by one person.

Mike Schmidt: 00:28:30

There are a few different things that are in play there.
Of course, we talked about anybody, you know, Sjor's walked through how you could open up a PR and update the readme and potentially you find an issue that you'd like to work on and you can work on that.
There's a little bit of odds in what you may wanna work on and what is valuable to the reviewers and to the maintainers.
And while there is no Bitcoin Core roadmap, I do think that there's value in seasoned contributors telling the world what they're working on and plan to work on.
Because I think that can solve two issues.
One is reviewers or maintainers taking a look at new PRs that people who are just eager to help are putting together and it's potentially low-value PRs or distracting.
At least some folks can interpret it in that way.
And then secondly, some established contributors are also looking for people to help with their particular project or piece of code that they're working on.
And so by coming up with something like a personal roadmap or writing up a project that you're working on and where new contributors can potentially help you, you solve both of those issues because now you're not getting maybe a superfluous PR to the repository.
So you don't have to worry about review time on that.
But now not only that, but you're also now getting a pull request that is interesting for you if you're an established contributor.
So that's something I'm interested in.
Just as a point of clarification, Brink as an organization that funds open source development work, including on Bitcoin Core, explicitly, I do not want to be on the board and the grant committee does not want to be directing what our grantees are working on and some very sensitive to that.
But I do think it's interesting if they on their own volition would come up with something like, here's what I'm working on, here's what's important to me.
If you open up a PR with this, I'm more likely to review it and help you and potentially mentor you.

NVK: 00:30:48

You know, I personally have no issues if you guys wanted to sort of like dictate what you want to see exist.
If anything, I love the market honesty on something like that, not to say that it's dishonest what you do at all.
Like I understand where you guys are coming from and trying to sort of remain out of the politics while supporting the project.
But I love it when like industry comes and says, Hey, I'm willing to pay for somebody to do this thing because one, I don't think I'm breaking the system, right?
Like it's an earnest sort of intentional thing, right?
Like, say Stratum V2 or something, right?
Like I'm a miner, I really want to see like better, better way of doing coordination of new blocks and I'm willing to pay for it.
And you know, some people may not like it, you know, it's still fair, but like, I really want to fund this, can everybody who wants to work on it, lift their hands, you know, and I'm going to help you guys economically and whatever.
Like, I think it's important for people to know that there is space for that as well.
We don't have to all be like Brink which tries to remain outside of this, which is used to be the traditional model.
Like most entities that do fund Bitcoin Core development, try to stay out so that, you know, it doesn't murky the waters and stuff.
But I think when there's like a clear business goal and it's like a source of truth, right?
Like it's obvious, like these people are not being, Even if I don't agree, they're not being insidious or anything.
This is like, you know, this is what they're trying to accomplish, right?
This is how they make money.

Mike Schmidt: 00:32:22

Yeah, I think there's there's an implicit or explicit direction.
Obviously, I'm saying that Brink is not trying to direct our grantees explicitly, but you could always say, and this is true, the fact that we've chosen those grantees and the projects that they've chosen to work on is an implicit endorsement of that.
And I think that that's okay.
Obviously, we're comfortable with that because you do need to make a decision on what you think is the most impactful work that could be done on the project given the grantees that are applying in our case.
There are projects, and sections of code that would make up something called a project that I think the industry could fund and not get much backlash.
So, like, for example, BIP322 generic signed message is something that I've heard that there's some identity folks interested in funding, for example.
And I don't know, there's been some talk about that now with this Ordinals project that that signed message may be valuable.
And so something like that may be innocuous, whereas something more consensus related, like if you're funding, trying to get a new opcode or in or something like that may be more controversial.
Maybe James has some thoughts on that.
I don't know.

NVK: 00:33:41

You know, I think it's important for people not to be shy about airing their business intentions.
You know, sometimes it's beneficial to them to just shut up and not because, you know, they want to get that thing in, but they don't want their competitor to maybe push it against it.
But generally speaking, I think it's a nice thing to do because, you know, Bitcoin enemies, right?
Like we're state actors or things like that.
They're not going to be nice, kind and like, you know, go and say, Hey, I'd love to fund people and sort of like be quiet about it.
Right.
So they're going to be completely, completely covert.
And they're going to like, you know, like do all this with all this sort of like literally evil intent towards the project.
So it's anyways, I just, I like to air out the laundry of Bitcoin, I think is important and it's good for it without sort of like delaying people from their work.

Sjors Provoost: 00:34:31

I suspect that there are not a lot of companies that have a very specific thing that they want to change in Bitcoin Core that would warrant finding, and recruiting a full-time developer.
I guess there may be occasionally, you know, if they're using Bitcoin Core in their environment there might be occasionally a bug or whatever but I think at that point it's easier for them to just get one of their own staff to figure out how to fix it but the idea that a business would depend on like a new opcode or anything like that that's such a long-term game anyway

NVK: 00:35:00

I'll give you some examples.
For example think about like you know Lightning Labs and all the Lightning Network people, they needed Maleability to be fixed and some of the features of SegWit in order to exist.
Lightning would not have existed in any form that's actually usable, right?
Under the original set of primitives and constructs that Bitcoin had.
Right.
So they actually made a push and funded and helped sort of like push changes that like would benefit and make them exist as a business.
Let's see, for example, Stratum V2, right?
Miners, like a lot of miners, especially non-public traded miners, want that to happen because it does protect them in many different ways, with more privacy, with, you know, give them more speed.
And so like, I wouldn't say, a business is unlikely to need a specific feature.
Maybe `OP_VAULT` would be great.
Like I can see how a business would need that.
Like specifically, I need this so that I can do like large custody, you know, for like institutional clients.
That's the only way I can do it right, I can totally see that happening.

Sjors Provoost: 00:36:04

But Stratum V2 you can see the other approach which is just build your own software project because Stratum V2 in principle is its own software project now

Sjors Provoost: 00:36:13

At some point, there may be some things that they'll need a tweak to Bitcoin Core for in order to make it work.

NVK: 00:36:19

That's often how it is, right?
Like the business will have this thing, but then they need a few little tweaks to Bitcoin so that like their thing actually works in a sort of performant way, right?

James O'Beirne: 00:36:30

And I mean, you could imagine that in many cases, a business might make those tweaks and they might just run a patched version of Bitcoind.
Like in the case of mining, I know there are people out there who want to solo mine, who don't want to use stratum because there's a tremendous amount of overhead in terms of doing the paper share accounting and all that.
And what they really would like is to get frequent block template pushes, right?
And that's something that you can kind of just patch onto Bitcoin and run in a pretty low-risk way.
I mean, obviously, there's a little bit of annoyance having to have a deploy pipeline that patches a version of Bitcoin that builds it, but it's not that a huge deal.
So I really, I mean, my take is like, I don't see anybody pushing for changes in Bitcoin in any kind of a, like setting aside malignance, but like in a sort of thoughtless way, I think, you know, a lot of the say stuff that like Blockstream is experimenting with, you know, the opcodes that they have for transaction introspection, like that obviously has applications for their liquid stuff, but you can make the argument that that stuff is very generally useful, and it's research that's really worth doing.
So I think at this stage of the game, I really don't see anything, even if you're talking about consensus proposals that are anywhere near the sort of nature of like, say, the block size increase proposals, which even then, I mean, maybe a lot of people who wanted the block size increase, maybe their motivations were probably genuine in the sense that they just want to see Bitcoin scale.
Yeah, they want to lower the fees.
They want to see Bitcoin adoption continue and so on and so forth.
But yeah, at this stage in the game, like maybe there will come a time when we see proposals that are kind of at the expense of some particular user group.
But I think right now, luckily, everybody just wants to see Bitcoin prosper, as far as I can tell.

Sjors Provoost: 00:38:24

The Segwit2x thing was interesting to watch that because there were attempts to increase the block size, like smaller pull requests, by experienced developers like Gavin.
But they never really got through.
But then once a bunch of companies decided that they wanted to Segwit2x alternative client, they forked the repo and hired, I think they, I don't know if they paid him, but I'm assuming they paid Garzik to do it.
So that's an example of you can hire an existing developer to do something specific for you.
And this didn't work out because it was just too hard for one person to do.

## Who chooses what gets merged?

NVK: 00:39:00

Yeah, so that sort of like leads me to sort of like the next thing, which is like who chooses what gets merged and how does something gets actually merged because You know if one thing I think a lot of people already understand is that like changes are excruciatingly reviewed, right?
Even minute changes.
And that's likely why we don't see malicious change attempts.
Because you become very clear, very fast.
So who are the people who, you know, get to merge it?

James O'Beirne: 00:39:31

It's a really subtle and difficult thing to explain because, on the one hand, the line that we all like to recite is that maintainers are just janitors and really They act as a kind of conduit to express the broader desires of the technical community.
And like at face value, that's absolutely true.
The more complicated nuanced reality is that oftentimes maintainers are seen as technical leaders.
They are in that position for a reason because people broadly trust their judgment.
And so people, whether they subconsciously or not, they pay a lot of attention to what those maintainers are doing and what they like.

NVK: 00:40:12

The proverbial gray beards.

James O'Beirne: 00:40:15

Yeah, the gray beards, exactly.
So, you know, I do think there's definitely a Bitcoin ivory tower and Bitcoin is very, very difficult because to understand it from first principles is not something almost anybody can do.
And so what happens is, in the community, you have varying degrees of technical capability, varying degrees of actually evaluating proposals.
And what happens is people sort of rely on the heuristic of, like, who do I trust?
Who's going to give me kind of a notion of what this change actually is and whether it's a good thing?
And so you're in this situation where there's like a very small number of people who are kind of upstream of the technical consensus around something and everybody else to varying degrees just kind of like sort of follows along.

Sjors Provoost: 00:41:01

But to get to the question of what should happen in kind of in theory, I guess, and I think it happens mostly in practice too, is there is a bunch of people who review code and then there is a group of about five or six whitelisted people essentially that we call maintainers who can hit the merge button on GitHub.
Now, in fact, we don't.
This is kind of weird because GitHub itself, we don't know.
It's a centralized company.
We don't know what it's doing.
You can't see it from the outside world.

NVK: 00:41:28

It could have been somebody else.

Sjors Provoost: 00:41:30

Maybe I can hit the merge button, I don't know.

NVK: 00:41:32

I mean, provided it was not signed, right?
Technically they could download, they could merge it locally, sign it, and then push it back.

Sjors Provoost: 00:41:39

So there's a group of people that are listed in a text file by their PGP key.
The idea there is that when they merge something into Bitcoin Core, not only do they hit the button on GitHub, but they don't hit the button on GitHub because they have to run a bunch of scripts, they have to PGP sign the fact that they merged it.
And then there's a script called verify commits, which does have problems, but it's there, that will actually go through recent commits and make sure that it was only those maintainers doing it.
Basically, you can just look at the GitHub history and see that these merges are done by that fairly small number of people.
Then you have to check, I guess, spot check or trust or whatever you want, that they are following a process that when they merge something, you can go back and see what they merged, and you can look at that board and see the discussion.
If the discussion is full of developers saying, no, this is horrible, don't merge this.
And yet they merge it, then, you know, that's probably a situation.
But usually what you'll see is other developers with experience in that area saying, okay, this looks good.

NVK: 00:42:42

So like that goes sort of like back to this.
Like that article, for example, that it's in the hands of six shadowy super coders, right?
Yes, practically, but no, technically.
So like, you know, these are people who are trusted to do some of this work, but you know, like there are a lot of people who understand Bitcoin enough to understand that change that just happened.
They may not have been as technical to sort of invent that change.
Which is often the case.
Like some crazy amazing cryptography was invented to do something or some new way of doing blocks like segregated witness or something like that, right?
But people who there is a next level of people there is a much larger group who can review that and say, you know, like, can you please clarify it here?
So even if they hit the button, because we don't have automated software pushes and updates sort of like a software update, the alarm would be sound.

Sjors Provoost: 00:43:42

Well, and also you're running, lots of people will run not the releases, but the master branch, so the in-progress version.
And those people include pretty much all of the developers who are working on trying new features.
And they'll often find bugs that were accidentally merged.
There are lots of pull requests in Bitcoin Core that are just fixing little things that were broken by pull requests because they were missed in the review.
It does get a lot of eyes on it.
Even if you didn't review the pull request yourself, I sometimes find a pull request because I'm working on another pull request, and whatever just got merged just broke my work.
I have to go in and look like, what the hell were they changing?
Why?
And then, you know, I'll say, okay, whatever, it's fine or not.
So there's a lot of eyes on it.

NVK: 00:44:24

Yeah.
So like, you know, we could almost divide, like this discussion kind of happens like when in the minutiae they happen on GitHub, right?
So like, you're going to have literally code-line comments.
You're going to have issue comments.
You're going to have PR-level comments.
And there's a lot of discussion that happens there.
PR comments, start getting a little bit more abstract, not necessarily to the specifics, but the nitpicks, and the nits are really done on a line level or code block level.
And then the PR discussions often sort of spill either from or to the mailing list and it all like, maybe people don't understand how the mailing list works.
Do you guys want to explain how the Bitcoin mailing list exists?

Sjors Provoost: 00:45:06

That's pretty rare, though.
I would say the amount of pull requests that overlap with what happens on the mailing list is probably 1%.

NVK: 00:45:14

But those are the ones that are the biggies.

Sjors Provoost: 00:45:15

Well, yeah, because they might influence some sort of either consensus or at least at the peer-to-peer level.

NVK: 00:45:21

Full-RBF, right?
That was one that spilled over from GitHub back to the mailing list.
And it's normal like it's fair.
I mean, people should find clarification, right?
You know, for the people that don't know, the Bitcoin dev mailing list is this sort of like a, like a traditional email mailing list where anyone can email there, there is moderation.
So if you just send an email saying, you know, like, f*ck you all or love you all.
It's definitely not going to make it.

Sjors Provoost: 00:45:48

It's not how you submit your inscription.

NVK: 00:45:50

That's right.
But you know, like even trolly sort of like valid questions or points are often let in because it's important to let a lot of that in.
Just don't expect people to respond if it's too out of scope, right?
IRC might be a better place to go ask that.
Often the idea of the mailing list is like things that could be a little bit more constructive, they need a little broader audience, including business to be sort of purview to, or to announce, right?
Like, hey, I have a new proposal.
I have a new idea.
You know, sometimes the back and forth will happen there.
Sometimes it'll happen right where you have your BIP being drafted.
So that brings us to BIPs.
Bitcoin improvement proposals.
What are BIPs?

## BIPs

James O'Beirne: 00:46:34

BIPs are, I guess, like a very technical specification of some idea that's relevant to Bitcoin.
It doesn't even have to be something that goes into Bitcoin Core or the protocol.
It could be some kind of a wallet format or, you know, strategy for using Bitcoin in some way.
But it's really, they're really just if you're familiar with like the way the internet was designed, it's almost like an RFC.

NVK: 00:46:59

So Like, you know, would you say like, maybe people like, I just saw this sort of like slight drama with the Ordinal's BIP being introduced.
And it all like the arguments are kind of fair on one side because, you know, it feels a little trolly, but I know Casey.
So like, I know it was not meant that way, you know, as a fair technical proposal too.
And I think people get confused if like what makes it a BIP number, a BIP draft doesn't mean it's going to make it to Bitcoin.
It's just like, Hey, we have this formal proposal.
It's a guideline to do something.
It's an idea, it's an idea that's very complete.
It's like technically sort of valid.
Which is always wishy-washy.
I know I'm being wishy-washy, but that's what we have to work with here.
And it's, And you know what like it is warranted to exist in the Bitcoin ripple.
Because you know, it's affecting people.
There's people using maybe this idea or there are people who really want to make this idea happen.
That's at least how I feel about BIPs. So, you know, you could actually quiet the discussion by just adding the damn thing.
And then like, you know, boom, let it have it there.
And now have the discussion under the BIP.

James O'Beirne: 00:48:07

I guess the counterpoint would be that you know, and I don't know how I feel about the ordinals, but it's probably fine to add.
But the counterpoint would be like, There's all kinds of stuff.
There's an infinite number of things you can do on top of Bitcoin.
And so the idea that like every time we come up with a new way to do something and somebody writes up a media wiki document, like the idea that we would like spam the BIPs repo with all these different things you could do with Bitcoin, at a certain point that just gets ridiculous, right?

NVK: 00:48:34

I know, I agree.
And that's why it's this sort of wishy-washy, depending on the people of the day, really, if it's gonna make it as a BIP or not.
I mean, listen, if it's gonna go on the protocol, right?
If it's going to actually have a meaningful change to the actual Bitcoin code and the actual Bitcoin consensus, it's almost like a hundred percent chance it's going to be a BIP.

Sjors Provoost: 00:48:56

But I wouldn't put too much value on whether something gets a BIP number.
You can write a Bitcoin improvement proposal and put it on your own website and have the same format as any other BIP but it won't get a number because of whatever politics.
Now the argument of having too many different proposals that are what you can do is a sort of a layer on top of Bitcoin, I guess.
Well, you can make a separate thing, like Lightning has its own repo with its own proposal.
Lightning doesn't make BIPs, they have BOLTs.
So you can say, okay, there is now a new repo for things that you're publishing on the blockchain that have no consensus meaning.
You know, you can describe counterparty there, give it number one and describe this guy, the inscriptions, and whatever, call it number two.
So that's just a matter of where you want to keep the information.
I don't think that matters.

NVK: 00:49:46

So I think the original sin of BIPS is not having a stricter sort of a set of requirements that you have to meet in order to make it as a BIP.
That's my opinion, my personal opinion.
This is not like the people who work on that opinion.
I don't know what their opinion is.
Might be the same, might not.
But the issue is like, we have a lot of BIPs, a lot of BIPs. They'll never make it to Bitcoin that like are interesting ideas, but you know, it's just not going to happen.
Or there's things, there are things that are just not implemented.
Then there are a lot of Bitcoin features that never made it into BIPs, even though they're referenced as BIPs, like BIP, is it 44 or 84?
I think it's 84.
There is no BIP that defines that derivation path, even though it gets referenced everywhere because the other derivation has a BIP that represents the number.
So listen, it's open source.
It's a, it's rough consensus, right?
So of course the things that we use as documentation, implementation, and building blocks are going to be messy too.
Right.
And I think people have trouble sort of accepting that it's not gonna be clean and pretty.
Then it's 44 that was missing.

Sjors Provoost: 00:50:58

Well, there's a lot missing, right?
So the numbering system of the BIP is more mysterious than ordinals.
They're not continuously numbered from zero to N.
They tend to come in groups of 10, where they might start numbering from like, you know, 21, 22, 23, and then there might be another series 40, 41, 42.
So there is some logic there that exists I believe in Luke's brain but it may have been documented too.

Mike Schmidt: 00:51:27

Tonal it's in tonal

Sjors Provoost: 00:51:29

That could be so the taproot bits you know or 340 341 342 but there are a lot of unused numbers there so

Mike Schmidt: 00:51:36

Rodolfo, are you saying that you think the BIP repo is too liberal on letting things in?
Is that your point?

NVK: 00:51:41

I think so.
I mean, you know, I'm the kind of person who prefers a little bit more of a general set of rules, right?
Just to avoid conflict.
The rules can be changed.
I'm cool with that.
Like, it's more like, hey, let's just have like, let's only add BIPs that like we should add all of them, every idiocy that people come up with as long as they have like some minimum, you know, technical merits to it.
Let's put it this way.

Sjors Provoost: 00:52:12

I think BIP2 actually put some constraints and it has to have some technical merit.

NVK: 00:52:17

But those should be drafts.
They should not be assigned numbers.
Maybe they can have the draft number, which is different than the final number.
But like it should be in a different folder in a different repo.
So it's like all the stuff that you want to come up with just so it gets like, it's really cool that things get documented, even stupid ideas, even like evil ideas or whatever, right?
Like, I mean, we should document all this stuff.
7,000 years from now, you go to this library, there's all this cool shit.

Sjors Provoost: 00:52:43

I think you're prematurely optimizing it.
There's one, There used to be only one maintainer up until like a year ago when a second was added, so I don't think they're being completely overwhelmed by the number of new BIP requests coming in.

NVK: 00:52:57

Right, but people are also scared.
I've met enough people who had very interesting ideas that I believe should be BIPs. They just don't do it because everybody is terrified of having to deal with it, right?

Sjors Provoost: 00:53:07

So they just write a proposal and don't give it a number and put it on the mailing list.

NVK: 00:53:11

Well, that's the other problem.
I then, the mailing list, I find that the mailing list audience is slightly different than the BIP actual.
It's like you get a different type of response.
And again, like it's a very like, it's a fault of the medium.

Sjors Provoost: 00:53:26

But you get the best responses once you've actually implemented something like working code, either in Bitcoin Core or somewhere else, depending on what the thing is that you're working on, then you'll get feedback from the relevant people.
If you're just writing a sort of a high-level proposal, yeah, then you're not gonna get

NVK: 00:53:42

No, it doesn't belong in a BIP.
High-level stuff, you need to have like pseudo code, you have to have like, like a true representation of what is it that you want to implement as a BIP, right?
At least that's my view.

Sjors Provoost: 00:53:53

But if you're putting something on the mailing list that's not very fleshed out, then the people who are going to respond to that are the people who are into things that are not very fleshed out.

Sjors Provoost: 00:54:01

Might as well either ignore you because they'll be tired of even pointing out that your proposal is not fleshed out enough.

NVK: 00:54:08

So my idea is, you know, like have a slightly better-improved set of rules and then just dump them in a separate repo, right?
We call that the library of BIPs, right?
And then you can categorize them as like the forgotten, the forbidden, the, you know, like whatever you want.

Sjors Provoost: 00:54:26

I don't want to see it as long winding discussion about meta, what has to go in a BIP or not.
And you just don't want this.

James O'Beirne: 00:54:34

Yeah, when I was doing an AssumeUTXO, I didn't do a BIP for that.
Partly at the time because I think I was intimidated, but partly because it seemed like an implementation detail for Bitcoin Core.
And so I was like, OK, well, this needs to be.

Sjors Provoost: 00:54:46

I would say it's too much.
So it definitely deserves a BIP if somebody else because it's not something that should only work in Bitcoin Core.
And, you know, you might want to build tooling around it, too.

NVK: 00:54:57

Just selfishly speaking, I don't want to go read the discussion first.

I want to go read the paper first.
So like having that BIP.
Even if it's an assigned number is just by name.
In some separate repo.
So we're not polluting the same Git file.
It's very useful.
Very useful.
So you go read it like, okay, this is interesting.
Then you go check out the discussion, which it could be, you know, like one dude having no objection to like, you know, the whole sort of internet hating on it.

Sjors Provoost: 00:55:27

With James's proposal for the vaults, now you have a PDF, that describes the initial idea.
Then there is a BIP and there's an implementation.
And that's on the mailing list.
That is good.
The only problem is, the only problem is if you go to the PDF, that's from like early January.
And so the actual implementation has changed based on discussion on the mailing list.
So it's actually kind of a pain for you, I guess, to keep all that up to date.
I mean, ideally, I would want a PDF that also updates with the latest proposals so that I can get a very high level.

NVK: 00:55:58

Personally, I don't like PDFs. Yeah, no, screw PDFs, Markdown.

Sjors Provoost: 00:56:01

It's all written, I assume it's written in Markdown and then you generate the PDF.
So you can read the original Markdown.

James O'Beirne: 00:56:07

No, I wrote it in LaTeX.

Sjors Provoost: 00:56:09

No. Oh, but you can write with Pandoc.
You can write Markdown, which is converted to LaTeX, and then write

James O'Beirne: 00:56:15

Yeah, but the formatting isn't as nice.
You don't get as much control.
I wanted to make a nice-looking paper.

Sjors Provoost: 00:56:21

Pandoc is extremely powerful.
I would not underestimate it.

NVK: 00:56:24

Do the PDF once it goes in.

Sjors Provoost: 00:56:26

I spent a ridiculous amount of time fiddling with the layout of my book, like figuring out how to get Pandoc to do certain things.
That's true.
But anyway, it's nice to have like a high-level document, like a pretty PDF and then a BIP, and then you know, you can see the middle of this discussion.
But yeah, anyway.

Mike Schmidt: 00:56:43

And there's actually versioning a new venue that you want your idea or your code to get in.
And this is something that James is working on, which is this Bitcoin inquisition.
James, as part of the process or what you're going through, do you see that you wanna have `OP_VAULT` activated there now?
Is that like the playground where ideas that are truly valuable get activated in Bitcoin Inquisition?

James O'Beirne: 00:57:16

Yeah, I think so because it used to be if you wanted to play with a pending soft fork, you had to wait until that soft fork got enough consensus to go to testnet, and then you could do testnet transactions.
But a soft fork being on testnet kind of signifies that it's slated for mainnet.
So Inquisitions is nice because we can just kind of do whatever we want there and play with ideas and actually have persistence in terms of test data.
So yeah, I think it's a great institution.
I mean, obviously, Vaults hasn't hit Inquisition yet, but I'm really hopeful for it.

Sjors Provoost: 00:57:50

But does Inquisition run on the regular signet?
Because in principle, you can have a custom signet for every single softfork proposal.
I guess it's nice to have a lot of sample transactions in a real blockchain and faucets and infrastructure like that ready to go.

James O'Beirne: 00:58:04

Yeah, and I think the idea is to sort of measure how any given proposal interacts with totally unrelated stuff, you know, so you would want some unrelated traffic.

Sjors Provoost: 00:58:14

So Inquisition combines all the code then?
It's like, takes all these pull requests and adds them together.
That's pretty cool.

James O'Beirne: 00:58:21

Yeah, and it's kind of a pain because now I have two things to rebase whenever anything changes.
And you do have to make some material changes to what you're proposing because the existence of other soft forks changes the code in non-trivial ways.
So it's a little bit of a pain, but I think it's probably worth it.

Mike Schmidt: 00:58:40

So you can actually have `OP_CTV`.

James O'Beirne: 00:58:42

Yeah, right.
Right now he's merged `SIGHASH_ANYPREVOUT`, `OP_CTV`, and hopefully pretty soon `OP_VAULT`.

NVK: 00:58:48

Very cool.
I mean, it's, Bitcoin is very complex and it's very hard for us to find out if there is any problems, right?
And even at the implementations, they use the new features too.
So, you know, like having ways of testing this of like a good amount of transaction data is kind of a big deal.

Sjors Provoost: 00:59:06

This is, it is a bit strange though, because the idea of testnet was to just test things, but typically when you wanna do something on testnet, it should be probably be merged into Bitcoin Core, even if it's only active on test net.
And here, I mean, signet should be no different in principle because signet is just the same as test net in that sense.
But now what you're doing is you're taking a different repository and you're merging these experimental softworks in there, and then the consensus is enforced by the people who run that particular signet, which in this case is two people.
I guess it works.
It's a different model to just try things out on an experimental blockchain without merging it into Bitcoin Core because I guess that act of merging is seen as a bit too much endorsement.
And also it makes it very hard to change anything else, because you are touching consensus code.
Even if you're saying, skip this line, if you're on test net, that could still be a very, very bad bug on mainnet.

## Is Github centralisation a risk?

NVK: 01:00:03

Yeah.
So as a side note here, like this is a constant sort of thing that gets brought up.
Like is GitHub centralization a risk?

Sjors Provoost: 01:00:11

It's a risk, yes.

NVK: 01:00:13

It's a realistic risk.

Sjors Provoost: 01:00:15

Well, it depends on the risk for what, but it's, it's such a useful tool that if we get rid of it, yeah, it'll be a bit safer, but we'll move about 10 times slower.

NVK: 01:00:23

We see people tend to think that, you know, we are at risk.
It's always like, you know, the airplanes are going to fall out the sky kind of risk.
You know, I think it could be a nonsense and annoying and not like, we wouldn't be as productive, but like we are all saying, Git is decentralized and everybody has a copy of everything and everybody has signatures and, you know, we can move to Git labs and we might even lose the issues which would really suck.
But I have a feeling that somebody out there is keeping a copy.

Sjors Provoost: 01:00:55

Let's say GitHub could just change the code from under us, but that's why we have all these signatures, so that's pretty easy to detect and make a bunch of noise about.
They can mess with the release tags, I guess, but the releases are on a different website anyway than GitHub, the actual downloads that we give to people.

Mike Schmidt: 01:01:13

There's also, like, the TornadoCash example, where they just decided to take down the repository completely.
And I know that got the heckles up of at least some of the Bitcoin developers that were worried that, well, maybe the sky isn't falling today, but they've definitely shown that things can fall from the sky if you rub people the wrong way.
And so I know there's at least some experimentation going on right now with trying to mirror the repository to maybe GitLab, GitLab hosted, maybe a GitLab self-hosted and seeing what that mapping looks like, because yes, Git is decentralized, but a lot of the goodies and niceties and even things like, emoji reactions, up down vote, you know, those sorts of things maybe don't have a mapping.
So it's a matter of figuring out what gets mapped over and could get mapped over so that you don't lose all that productivity if GitHub were to go down.
I think it would be quite chaotic for a period, although it wouldn't be obviously an existential threat to Bitcoin in any way.

NVK: 01:02:27

It's the metadata and the logic that GitHub have that's quite good.
By the way, there is a 12 BTC bounty for somebody to create a GitHub alternative on Nostr.
So like, and I think it would probably get upped if somebody showed that they were producing something interesting.

Sjors Provoost: 01:02:44

Yeah, I think this general sentiment is that GitHub is good as long as it's there, but we should always assume that it may disappear from one moment to the other.
The thing to be worried about is making sure that we have backups of everything that happens there, and then there will be some period of interruption.
It'd be nice if we have a backup plan ready that really works.
But meantime, GitHub provides some really good tools.
It's really in the small things.
I can look at a couple of lines of code somewhere, then I can click on the blame button and see who was the last person changed it, and I can dig back right to the pull request and see all the discussion around that line of code.
So it's a very good way to just get information about how things work and where they came from.
And it's a very low barrier to entry.
Somebody who has experience working on any other GitHub project will understand how to do this.
Whereas every time I have to make a contribution to a GitLab project, I get confused.
It's not a very nice interface.
So it's there, it's like a bunker, but I hope we don't need it.

NVK: 01:03:42

You know, I always joked about, what's the name of that Adobe competition on Linux?
I keep on saying to them, don't try to invent something, you just copy Photoshop, please.

James O'Beirne: 01:03:52

Oh, Gimp.

NVK: 01:03:53

Yeah, so like, please just keep all the buttons exactly the same.

Sjors Provoost: 01:03:57

But a lot of the other scenarios that people would be worried about by thinking GitHub is centralized, like yeah, GitHub itself could start messing with the code.
Those kinds of scenarios I think would also exist if the thing was more decentralizedly hosted because then you have to trust whoever is behind that.

NVK: 01:04:11

Well, even more, right?
Because Microsoft has a reputation here too, right?
I mean, they don't wanna be known for the people who like rug pull software out of people.
It's kind of a biggie.

Sjors Provoost: 01:04:21

Yeah, and if it's just like one core dev who happens to run a little server, then he gets compromised.
Even unknowingly, the server gets taken over by the NSA, and then the sneaky backdoor will be put in there closer to the release in a way that's a little bit more subtle by also using a compromised PGP key of that same maintainer.
Something like that.

NVK: 01:04:41

I think the biggest risk with Git, like the realistic practical risk, is, for example, say China tells GitHub, don't show the Bitcoin repo to Chinese people.
Cause GitHub's still there, right?
Like all the devs are there, but they just can't work on that repo, right?
You're gonna probably see a lot of that going on as we go forward, as things get a little bit more weird, but it's not gonna be like a full-on.

Sjors Provoost: 01:05:02

Yeah, that could be an argument for having a good mirror somewhere so that people can keep contributing on some other website.
But I guess with China, it's such a whack-a-mole game that even having a mirror just doesn't crush the mirror.
If they want to not have the Bitcoin repo accessible to developers in China, there's no point in going to some other site because there'll be one guy in charge of making sure that happens.
And if that guy sees the mirror, then I'll add that to the list.

## Activation methods

NVK: 01:05:27

So guys like, you know, to go into a more difficult topic here.
First is like, who chooses, the activation method, what are the activation method options, and how does whole massive shit work?
I mean, you know like it's always dramatic.
It has not been sort of flushed out.
And I don't believe it ever will, just the nature of the project.
But like we talked about the changes, a lot of changes require a soft fork or a hard fork.
So, you know, we have to have ways of doing that safely and we have to have ways of signaling and creating consensus and displaying consensus.
You know, I'm a big fan of Flag Day, Game of Chicken.
I really don't like the speedy trial stuff, you know, a `LOT=true`, you know, so like, as default, so those are my sort of things, but like, how do you feel about this?

James O'Beirne: 01:06:27

Yeah, Rodolfo, can you, can you describe what you don't like about speedy trial, because from what I know, all speedy trial is saying is basically like, hey, we're gonna do a short period where if all the miners absolutely want this thing, then the signal.
So otherwise we're just gonna fall back to something else later on that's gonna be more lengthy.
Like what is your objection to that?

NVK: 01:06:48

So I don't wanna give miners an upper hand in the dynamic, right?
It is a very slight and very subtle upper hand that we give a speedy trial to them.
We essentially let them show to each other, right?
Did the miners themselves have consensus?
So they could be trying things that would be beneficial to them and not beneficial to economic nodes, right?
And sort of like using this mechanism covertly, right?
To sort of try to signal to each other, okay, you know what?
Hey, oh, look, we have consensus.
You know what I mean?

Sjors Provoost: 01:07:21

But then you don't like the whole idea of using miners to activate softforks.
I mean, there is an actual dependence on miners when you want to activate a softfork in a way that's safe.
That's just, that dependence is there because you want the majority of miners to enforce it so that people who upgrade more slowly don't get fooled by all sorts of chain splits.

NVK: 01:07:40

I don't also have like a good answer either.
I mean, aside from the fact that I'm perfectly fine with the game of chicken.
I think that's how it should be.

Sjors Provoost: 01:07:48

I am not fine with the game of chicken at all.
So I'll just shamelessly plug that I wrote a whole chapter on soft fork activation in my book.

NVK: 01:07:57

Which everyone should read by the way.

Sjors Provoost: 01:07:58

The book is called Bitcoin a work in progress by Sjors.
So basically I kind of went through like, you know, Satoshi was just activating soft works sneakily really, and then things got better with things like BIP9 and then there was a lot of drama around SegWit and in my opinion, we just had a bit of post-traumatic stress syndrome from SegWit so that we made more of a flow of taproot than was necessary.
My guess is that would have been fine with BIP9 especially given what happened during speedy trial and the drama just delayed activating the whole thing because as soon as this drama a lot of Bitcoin developers will be like, okay, I'm just gonna sit in a little corner away from the drama, and I will come back when the drama is over.
And then the lack of action will cause more drama.

NVK: 01:08:46

Let me add one thing.
I'm okay with speedy trial if we did `LOT=true`.
I think what I want is consequences for people making decisions.

Sjors Provoost: 01:08:54

I think `LOT=true` is a terrible idea.
So the whole point of using miners to activate software is to make it safe.
To make it so that if you don't upgrade your node, if you're running an old node, whatever, you're not going to get confused because the miners are making sure that any deviation gets re-orged.

NVK: 01:09:09

But then let's make `LOT=true`.


Sjors Provoost: 01:09:12

As soon as you start adding a game of chicken dynamics that can potentially lead to giant reorgs, you have removed the whole safety.
So if you don't care about safety, then why are you trying to do it safely?

NVK: 01:09:26

No, it's not black and white.
Hang on.
It's not black and white.
There are different shades of safety here.
I think you could make a case with `LOT=true` and Speedy Trial.
And a long activation period, you could make it safe.

Sjors Provoost: 01:09:41

Well, the idea of Speedy Trial was to try it before anything else.
So something like Lotru could have been done after the Speedy trial.
There is no point in doing a Speedy trial with `LOT=true` because `LOT=true` is basically saying we're going to activate this software at some point in the future.
If you're going to do that, then I don't think you need to Speedy trial.
You can just use a `LOT=true` activation and then allow miners to signal from it right away.
So there's no benefit in the speedy trial.

NVK: 01:10:08

I want people to like shit or get off the pot, right?
I don't want to give people the benefit of just sort of testing out little things because this is a way in which people find It's a way to test things.
They may not be beneficial to everybody without consequence

Sjors Provoost: 01:10:25

Well, that's why I don't like this speedy trial either because I think it would have been fine to just do the regular BIP9 activation

NVK: 01:10:31

Yeah, that's fine by me

Sjors Provoost: 01:10:33

And maybe we could have modified it to the BIP8 without the `LOT=false` stuff because it uses heights.
It's a little bit less, and has a few less edge cases than BIP9 does because it uses timestamps and you can do some annoying things with timestamps.

Sjors Provoost: 01:10:47

So I think we shouldn't have made a fuzz about it and it's very easy to deploy multiple soft forks at the same time using BIP9.
If you start adding `LOT=true`, I really don't want to even think about what that will look like if you had multiple active at the same time

NVK: 01:11:00

I don't think you can have multiple things going at the same time.

Sjors Provoost: 01:11:04

You have some, you have a controversial soft fork number one and another one number two, and then one of them caused a time bomb, but the other one activated, but then due to a giant reorg, the other one didn't activate.
I don't want to think about it.

NVK: 01:11:16

So here's an interesting thing.
I still have an unsettled like my own personal preference.
I don't know if I rather have many little things get activated unceremoniously often and by often I mean you know say every six months and we even have a set date, you know, that the little thing is going to work.
And I mean little, I mean little, right?
That is something that does require activation and not bundle things into this Omni build sort of style.
Cause this is, I think a lot of people got a bad taste too during the block wars because like SegWit was kind of an ominous bill, right?
So like you have all this crap in.
It's very hard for people who don't understand these things deeply to understand what's going on.
And then people feel bitter about it afterward.

Sjors Provoost: 01:12:02

But I don't know if it could have been done that much smaller.
I mean, there were some, maybe some things you could have removed from it.
Just if it's Taproot, you definitely could have removed some things from it, but it was a nice package.

NVK: 01:12:11

Yep. No, I get it.

Sjors Provoost: 01:12:12

I mean, you could have done Schnorr separately and other things separately.

NVK: 01:12:16

I don't know.
Is there conversations about like, you know, should we do the little things?
Should we make big bundles?
Is there a lot of conversation going on about like how to activate things like proactive thinking?

James O'Beirne: 01:12:29

All I can say is, you know when I started doing AssumeUTXO and obviously, implementation changes are different from consensus, but I had this very optimistic idea that I would carve this thing up into a bunch of tiny changes and do it bit by bit so that everybody could follow along and be assured that every step of it was safe.
And in hindsight, I really regret that in some ways, because I think it winds up dragging things out to an incredible degree.
It makes everybody fatigued.
You have to test and retest and retest and retest.
And like with a consensus change, I think to your point, you don't wanna make the community kind of lazy and you don't wanna just acclimate them to these constant changes rolling out because then they won't scrutinize them as much.
And so, you know, it's this tension between having these big, you know, I mean, Segwit and Taproot, as I've said before, they're like these massive, almost reinventions of Bitcoin scripting and they're great changes, but they are, you know, pretty hefty.
So there's a tension between that and then having like a bunch of small changes to get rolled out and people just get used to kind of upgrading consensus.
And that's maybe a less-than-ideal state.

NVK: 01:13:41

You know, it's funny.
I thought Schnorr, adding Schnorr, just Schnorr, not even talking about everything else like it was going to be the thing.
Like I thought that people were going to literally go to war over that.
That's a fundamental change to Bitcoin.
I mean, we now have a secondary crypto primitive in there.
Like it's hard to convey.
Like, I mean, you could almost say this is not Bitcoin anymore.

Sjors Provoost: 01:14:05

I mean, to nodes, it's anyone can spend.
So, you know, it's fine.

NVK: 01:14:09

But it's like, it's fascinating.
The things you just never know what is the thing that's going to tick the community and the thing that won't, right?
Like it's so hard to measure.

Mike Schmidt: 01:14:20

Activation.

James O'Beirne: 01:14:22

I thought it was hilarious.
I thought that people got bent out of shape in terms of the activation of her taproot was the most ridiculous thing I'd ever seen because it's the least, to me, it's the least substantive part of the proposal.
It's like, and so it almost, it felt to me like contrived.

NVK: 01:14:39

No, I mean, I was angry about the activation.
I am, I'm being very open here.
The activation was annoying me.
I did not like the way it was kind of like it felt shoved through.
The package I had no issues with.
I mean, I always found it important for Bitcoin to have a second cryptographic primitive in case the other one breaks.
So like, ready to go kind of thing.

Sjors Provoost: 01:14:59

Not that independent though.
I would say that if ECDSA breaks, then Schnorr breaks.
I mean, Schnorr is like ECDSA with a few lines of code removed essentially.

NVK: 01:15:08

I understand, but like, you know, we have proof for it.
It's just nice to have, you know, maybe the issue with ECDSA is found that Like, you know, it's in a minute part of it.
It's a subsection of it.
Like, you know, it's just, it only affects certain kinds of keys that were generated, whatever, right?
The point is it's nice to have a backup that's already part of the chain.
But anyway, going back to this, The package was fine by me.
Like, you know, I want these features.
I think they're great.
The issue was activation.
It did feel shoved through.
I think it was sort of like part of it was because of the PTSD.
A lot of people were not in the mood of talking and it's only gonna get weirder.

Sjors Provoost: 01:15:45

Well, the show-through part is you could say the speedy trial kind of gives that feeling perhaps, but I think if there had been no drama, the BIP9 deployment would have been earlier than that we had speedy trial.
So in a sense, I think it got delayed by all the drama by about three to six months.
And then the speedy trial was kind of a way to cop out of the drama, the saying like, okay, let's just put this drama on pause, see if the speedy trial just works, and then we can continue the drama if it doesn't work.

Mike Schmidt: 01:16:14

Well, it's a bit interesting that, you know, we had the, so some folks from Optech and AJ Towns put together taproot review and there was little groups that met each week or every two weeks and sort of went through different prompts and tried to review this, the code base, the package, as you say, Rodolfo.
And I think there was some good that came out of that.
But in terms of the energy put into that versus the energy that went into discussing about discussing about discussing the activation method.
It's a little disheartening that so much energy and passion went into that where it felt like people were kind of going through the motions than actually reviewing the thing.
So there's a bit of contrast there that I wanted to point out.

Sjors Provoost: 01:17:07

I'm glad that people did do all that intensive review of the package, which I went to one of those workshops in London.

NVK: 01:17:14

It was really great.
I mean, like it was it was incredible.

Sjors Provoost: 01:17:17

That was really good.
And I think part of the reasons why the activation will have more debate is because more people feel that they are competent in that.
So because it's in a way it's simpler, so it's easier to have an opinion.

James O'Beirne: 01:17:30

It's a bug shed.

Mike Schmidt: 01:17:31

Yeah, exactly.

NVK: 01:17:32

I think you guys are sort of looking at this more from the core perspective.
I think there are a few things here.
One is, yes, I mean, Taproot, Schnorr, and all the package, it's a little bit more complicated than your average industry person can sort of comprehend.
The actual technology there is not simple.
But there were two years of people seriously having work groups and discussing and providing as much.
Listen, we're really trying to not create contention for when this thing comes about.
That was the sentiment.
But I think the issue with activation is even people who don't want something get that thing.
And there is a certain feeling of getting a new consensus on Bitcoin being shoved onto your node, which is literally what happens.
And I think it's a feature that these things are so horrible.
They create a lot more scrutiny on the people, on the package, on the method, on the medium.
And that, like, even though it will definitely make people retire early, it will definitely make sure that you know, some people need a long break.
As horrible as it is, it's necessary.
It's something that in my view needs to be that way so that we discourage any kind of like a bad actor from trying to participate in that unless they're fully vested.

Sjors Provoost: 01:19:04

But there's a difference between making it difficult to activate something and making it a drama to activate something.

NVK: 01:19:11

Oh, yeah, the drama is retarded.


Sjors Provoost: 01:19:13

If the drama is about the content of the thing, that's the kind of scrutiny you want.
But if the drama is only about the activation method, then well, that actually is all just review time that doesn't go to the package.
So you couldn't have a malicious fork and then deliberately create a lot of drama around it, around the activation of it so that people don't pay attention to what you're actually doing.

NVK: 01:19:32

But you know, you could say that the activation method is still unsettled, right?
So like, there's gonna be drama around that.
I don't know, maybe we should start working groups on figuring out new activation groups for the next activation.

Sjors Provoost: 01:19:43

I mean, my heartache on the activation is just BIP8 minus the `LOT=true` stuff, and it's fine.

James O'Beirne: 01:19:50

I think that's the thing, is like if there was some fundamental objection to Taproot people had, they could have articulated it through Speedy Trial.
Like Speedy Trial could have failed.
And I just don't know that, I mean, personally, I'm not interested in the activation method.
I hope to God, if `OP_VAULT` stuff goes well, somebody else has some strong, well-informed opinion about how activation happens because I surely don't.
Probably somebody like, you know, with the Inelective Sjors, should be thinking about that stuff.
I don't have the mind for it, but yeah.

Sjors Provoost: 01:20:23

I don't want to do it either.
That's why I just do BIP8 without `LOT=true` stuff.
Because I've already reviewed that code so that's fine.

NVK: 01:20:30

And, you know, like, guys, I don't think like there's no amount of discussing it at least at this stage of Bitcoin that I think will make it easier.
Again, like, you know, we came from an extremely contentious like Game of Chicken, which was Segwit.
And then it was fairly recent right after that we did another activation of something that was kind of like big and hard for people to understand, even though all the information was available there for them to understand or cope or whatever.
But again, I think the fact that people are not interested in entertaining the discussion about activation, cause everybody was just so PTSD from it sort of like made people think that there is some more contentious sort of like this thing just feeds on itself.
But, you know, maybe the next one, because this one was fairly like, you know, for all the drama that was, was fairly insignificant.
I mean, compared to the previous.
So I think the next one, depending on the Bitcoin price at the same time, because that matters, will sort of dictate maybe a slightly different dynamic.
Maybe some galaxy brain comes up with something more clever that sort of appeases most people or better compromise.

Mike Schmidt: 01:21:43

Do we need something easy?
Do we need to do the great consensus cleanup?

NVK: 01:21:49

I think that if we found a way to have miners have a backseat on it and yet they still have to participate because they still have to activate, right?
But if there was a way where the dynamic essentially deferred to the economic nodes in a way where even if it's like soft, I think it would go a long way because I think a lot of people, a lot of people are PTSD with miners trying to take control of the network.
So I think having that dynamic somehow shows that the economic nodes are kind of calling the what's gonna happen really it's kind of a big deal even if it's a pageant show and not the actual thing.

Sjors Provoost: 01:22:34

But I don't know what you would demonstrate then that's always the problem there.

NVK: 01:22:38

No, I know, that's what I'm saying, I don't have an answer.

Sjors Provoost: 01:22:41

So if you want to have a fun one, I guess the great consensus cleanup could be an interesting one to get some complicated game theory because one of the things it does is it diffuses the time warp bomb or the time warp thing.
So then you could have miners that could vote to activate the cleanup, which would remove their ability to ever do a difficulty bomb, or sorry, not a difficulty bomb, a time warp attack.
But if they don't like it, then they could start, you know, immediately perform said time warp attack to frustrate the activation of this thing.
And then I don't know what the game theory would look like, but definitely.

NVK: 01:23:16

I'm just saying, like, if anything, it would just be fun to watch.
I'm going to buy a lot of popcorn, you know, like that, that would be an absolutely fantastic event to happen in my lifetime.

Sjors Provoost: 01:23:27

Yeah, But I think that the question you want to, I think one question that's important to ask is, you know, is there some sort of future where you're worried about some specific change to Bitcoin that is very bad for the users, but somehow not bad for the miners and where you would have the miners push it through?

NVK: 01:23:45

Yep.

Sjors Provoost: 01:23:46

Is that the thing you're worried about?
Or is there ever a scenario where you're worried about the miners stopping the change from going through?

NVK: 01:23:52

No, I'm not concerned about the miner stopping changes.

Sjors Provoost: 01:23:58

Then you don't need `LOT=true`, right?
If the miners don't stop it, you don't need anything like that.

NVK: 01:24:02

Yeah.
Not technically, but in practice you kind of do.
The main issue, I guess, is I am afraid of miners activating things that users don't want.
I'm not as concerned about them blocking because, you know, the only thing they would want to block is like you know say algo change right but then you're already ignoring them anyways right like anything that they would truly want to block or things that like you just be moving on from them anyways So I don't think that that's a concern.

Sjors Provoost: 01:24:33

I don't think we have a mechanism to stop miners from activating a soft fork that we don't have.

NVK: 01:24:37

Oh yeah, no, I agree.

Sjors Provoost: 01:24:38

And we've been waiting for a very long time for some other group of miners to re-org them.
So the most obvious bad soft fork that miners could deploy is a KYC soft fork, where basically blocks are empty unless miners have proved that you have done your KYC through whatever mechanism they want.

NVK: 01:24:55

Yeah, but then you add more fees and some other miners gonna mine it, right?
Like that's why those kinds of miners picks the transactions kind of like attacks, right?
So like they do either empty blocks or whatever, not very concerned.

Sjors Provoost: 01:25:09

Well, that is a case where just having miners enforce softfork doesn't really make it a softfork because the economic nodes will completely ignore that rule set.
Nobody will run a node that enforces that rule set.
So as soon as the majority of miners no longer enforce it, no longer re-org out blocks that don't comply with it, then you just get it.
Everything will just go in anyway.
There'll be a giant mempool, maybe a few hundred-gigabyte mempool, but eventually, it will go through.

NVK: 01:25:37

Now another fun thing too on that game theory is that like, you know, as Bitcoin halves, right, the rewards per block, like, you know, the miners further depend on the users, right?
For their income.
So like it becomes, it's going to become economically stupid for them not to mind the transactions, right?
Like, even if they don't agree with the transactions, even their state is saying, Hey, don't do this because then they're going to just move their gear somewhere else.

Sjors Provoost: 01:26:02

Yeah.
But my doom scenario there is that they will get subsidized.

NVK: 01:26:07

So sure.
But then, you know, we're going to have an empty block every four.
Who cares?
Like, I mean, it's not the end of the world.
It's going to suck.

Sjors Provoost: 01:26:13

No, they'll get subsidized to reorg, basically.
So basically, the minor revenue is not coming from Bitcoin transactions is coming from governments that pay them to censor.

Mike Schmidt: 01:26:22

This is the Eric Voskuil discussion.

NVK: 01:26:25

Yes, very much.
So yeah, but I still don't think it would be as economically interesting as mining those because see, what users would do is just further increase the fees, right?
Like, and then you're gonna have miners outside of that network to do it.
And then they're gonna start getting into Whack-a-mole, where you're gonna start like, you know, blacklisting miners, you're gonna try to fork the actual stratum network.
And it all like, it just gets weird nonsense.
I'm sure they'll be very successful at bothering us for like a few months.
But like, it's very hard to sustain this kind of stuff forever.

Sjors Provoost: 01:27:00

Yeah, it'll be an interesting question about security budget, who has the bigger budget here?
Is the economic use of Bitcoin, you know, are people really willing to pay enough fees to overcome an opponent that is willing to pay a lot of money to not have them make transactions?

NVK: 01:27:14

You know, a heuristic that I like on that, It's not like a perfect analogous to it, but it's like Bitcoin is the largest computational capacity on earth by like many, many, many, many, many orders of magnitude.
And it's still like this kiddie pool, a tiny economic system, right?
Like, I mean, like Bitcoin is hilariously small, even at the peak.
Like we barely hit a trillion and it's still like, man, what Apple probably has more cash than Bitcoin has its own value, right?

Sjors Provoost: 01:27:44

Like, is it really though?
I mean, I know we have a lot of hash power, but I think, I don't know how it compares to other data centers.

James O'Beirne: 01:27:52

It's not like general-purpose compute, right?

NVK: 01:27:54

It's not general-purpose, but it is.

Sjors Provoost: 01:27:57

No, no, I get that.
We're the biggest SHA-256 thing in the world, but we're not necessarily the biggest compute thing in the world.

NVK: 01:28:03

I think it is.
Like somebody did some calculation on that, right?
And it was a crazy amount.
I mean, ours is specific.

Sjors Provoost: 01:28:12

I have no idea how many gigawatts worth of data centers are out there that are just doing general compute and AI.
Maybe Bitcoin is bigger than that, but maybe not.

NVK: 01:28:21

That came up, I think on the last, sorry, on the previous bull run.
But anyway, somebody can give us some notes later.

So guys, like there's like, I guess like two things now, like one, one main thing I want to address and then like some questions from the audience, unless you guys sort of like have things that you want to bring up, which is totally cool with me.
So one thing is like really like the optimist view here, like What can we do to improve two things, the visibility on how the sausage is made so that the FUD can exist as easily.
So we don't have like Wall Street Journal writing retarded articles or at least retarded headlines.
And the other thing is like how do we improve development in terms of like, I wouldn't say like certainly like attracting more people, but like getting the people that are interested in working on that, like working on that.
Who wants to tackle each question here?

## Improving Bitcoin development and visibility/perception of development

Sjors Provoost: 01:29:13

Well, to the first one, so the problem I guess is we have lots of good views into what's going on if you read Optech, but the average Wall Street Journal reader is not gonna read Optech.
So I guess then the countermeasure would have to be some popular science writer actually writing about random Bitcoin Core requests as if they're like super interesting.
And that just takes a great science communicator or a great technology communicator who somehow can do it without coming across as a complete shill.

NVK: 01:29:43

Well, I mean, the cool thing about pop science is that it can just invent whatever the fuck you want.
And it goes into the thing as if it was true.
Right.
I mean, you know if you read any pop science magazine or whatever, we have to stuff there is like, like completely either a lie or wrong.

Sjors Provoost: 01:29:59

So the risk comes in.
So whoever is that writer may then decide to start promoting Ripple all of a sudden, or at least promote some sort of hard fork that they want.
So maybe it's good that Bitcoin is a bit boring.

James O'Beirne: 01:30:12

Yeah, I think, you know, the Wall Street Journal has political motivations.
So you're never gonna, you're never gonna fix that.
I think there's a vested interest in misinterpreting the technological stuff.

Mike Schmidt: 01:30:24

I actually spoke with the author of that article before the article, and it wasn't clear what he was going to be writing about.
And the title is obviously very unfortunate and it's also unfortunate that at least the discussions that I had with him, it didn't get through.
And so I don't think it's a matter of making ourselves necessarily available to those people to educate them.
I think that's OK.
It obviously didn't work or it didn't work to the degree that I had hoped with respect to this article.
So maybe similar to how there's a developer, you know, legal defense fund, maybe there's another organization out there already or one that could be doing advocacy or PR in some of this regard, at least if we're talking about like the mainstream level.
I think if you're talking about a little bit lower level, I think you guys had mentioned the ad that Optech can help educate, at least from that very grassroots up.
But I don't know.
I kind of lose I get dizzy when you get up at that mainstream level about what should be done.

NVK: 01:31:33

You know, one little tip on media relations is when a reporter reaches out to you without being very clear on the article that he's writing, like, oh, I'm writing this.
Can you please help me understand so I can, you know, like I need a quote or whatever, right?
If they're being wishy-washy about what they're writing, it's 100% a hit piece, either on you or on the topic you like.
They're just using you as a means to get better technical bullshit so that they can sort of feel the sound better.

Sjors Provoost: 01:32:03

Well, the problem is it's hard to distinguish from actual good journalism because an actual good journalist writing an honest piece, which may or may not be critical, would also not tell you what they're going to write because that's their job.
So now let's forward in the future.
Let's say journalists do understand how the Bitcoin Core development process works and we're 10 years ahead and there's actually two or three malicious maintainers that are doing very sneaky things.
I would like to have a mainstream journalist discover that and blow the whistle on it.

James O'Beirne: 01:32:30

But they're not gonna be breaking that news.
It's, you know, someone in the technical community is going to figure that out well before they would ever, you know.

NVK: 01:32:36

You know, I found like 99% of the time when they reach out with like, you know, they, they will be very specific when they're in good faith.
Like here is what I'm writing about or, Oh, I read this awesome blog piece about like this feature that's coming.
Can you please help me clarify it?
Like they're very forthcoming about what they're writing when they're not being insidious.
And when they're doing a hit piece or something negative, they always hide what they're trying to write.

Sjors Provoost: 01:33:06

Yeah, there's a bit of observation bias in there because all the pieces that are mainstream pieces about Bitcoin have been negative hit pieces.
So like It's very hard that you would have been approached by an honest piece.

NVK: 01:33:18

No, there has been.
I've had a piece, especially in the past, quite some time ago, where it was like mainstream just learning about Bitcoin and stuff.
The article didn't make it out, but they were earnestly trying to write a decent piece about it to the extent that they could sort of comprehend, especially back in the day.

Sjors Provoost: 01:33:35

Well, the first person we need to, you know, as a group of people need to convince how the process actually works is, you know, a certain judge in England.
So that'll probably give us a lot of ways to phrase things that they understand.

James O'Beirne: 01:33:52

You know, again, see political motivation.
I think we need to be ready to reckon with the reality that these institutions are structurally motivated to fight against Bitcoin in ways that are potentially unfair to the technical realities.

Sjors Provoost: 01:34:08

Yeah, I'm not saying we should use those institutions to communicate these things.
We should first figure out how to communicate them because that's quite hard.
And that's why I said maybe the court case will give us some actual ways to articulate it that make sense that is not just written by shills basically but have stood the test of scrutiny by somebody who's very adversarial on it and then you need a medium to broadcast that stuff in that could be, you know, somebody else going off.

NVK: 01:34:35

But here's the thing.
Mainstream functions in certificates and in appeal to authority and all that stuff.
And they have their own approved authorities.
I think that the reality that bitcoins have to sort of accept is that you know, at least for the next decade, at least I believe, you know, we're just going to have an in-hospital sort of like space, in-hospitable space for Bitcoin in the mainstream.
That'd be mainstream politics.
That'd be mainstream anything really, because we're building the thing that sort of kind of like defunds them.
So you know, they're not going to like it.

NVK: 01:35:08

There's going to be some de-factors from them, but like the majority of the damages, listen, we're coming for your, for your bread.


Sjors Provoost: 01:35:14

If you're trying to reach large audiences, you don't need to go through traditional media, but I would call Joe Rogan mainstream media at this point.
Like he's reaching a bigger audience.
He doesn't get Bitcoin.
No, but you can go on his show and basically talk.

NVK: 01:35:29

People have tried.

James O'Beirne: 01:35:30

Yeah, you guys are 100% right.
I mean, we should be doing both, right?
We should be trying to communicate as best we can the realities and what makes Bitcoin special and the fact that it really isn't controlled by any single group of people.
But we also need to keep in mind that we have potentially a rough road ahead and we're going to encounter a lot of headwinds in terms of institutions being adversarial.

Mike Schmidt: 01:35:56

There's some room for improvement even within our own house.
I've noticed this.
I'd be curious about your guys' comments on this, but I've seen on Twitter lately, a lot of, there shouldn't be developers in Bitcoin as a career.

James O'Beirne: 01:36:13

Oh yeah, that moron Steve.

Mike Schmidt: 01:36:14

Yeah, well, there's that, but there's him and then there's others too.
As he may have, I don't know what his point is, if I'm being, if I'm steel manning his argument.

NVK: 01:36:24

So Steve is a good friend and I understand where he's coming from.
And I don't like it.
I don't like Bitcoin lewdism.
It feels like lewdism, right?
It's like we were having this conversation, I think like an episode ago that I had the two of you there.
I think it might have been the `OP_VAULT` episode where we're talking about gardening versus like, you know, software does not exist without updates.
And I differ in this mindset where it's like, I believe that all the devs should be hired by actual industry.
So it's very clear on their motives as opposed to charities and things like the Brink is doing, like, which is great, but it's harder to see what the intent is, right?

James O'Beirne: 01:37:08

So his concern is that if you employ people full time to work on Bitcoin, their constituency to develop their own interests, they can be, you know, subtly manipulated by the people who are paying them to work on Bitcoin and, therefore we shouldn't have anybody paid to work on Bitcoin.
So there should be no Bitcoin developers, which is just fucking nuts.
It's just insane.

NVK: 01:37:28

But I think that's what happens when people who are not software people, look at Bitcoin.
And in all honesty, I think most of the fault here is when you have a system that is very complex, opaque, and anarchic.
Like by nature, it is f*cking hard to understand Bitcoin.
I mean, you know, I was just joking before we started, like half the people complaining about Bitcoin on Twitter, they don't understand how Bitcoin works.

I mean, like, and these are people who go on spaces and talk about like Bitcoin as if they were some expert.

James O'Beirne: 01:37:57

I was just going to say real quick and, you know, I'm sure Sjors And Mike, maybe this resonates with you to some extent.
But I just wanted to make clear the one thing I wanted to get across in this episode is like, AssumeUTXO, `OP_VAULT`, like I wouldn't have done these things if someone wasn't paying me full time for the last four years to sit in a chair and like look at the Bitcoin source code, they would have been completely unreasonable to do like in a part-time capacity.
And so I think that the funding is really important.

NVK: 01:38:24

And it's self-flagellation to create Bitcoin proposals and like get them out.

James O'Beirne: 01:38:28

It's not fun.

NVK: 01:38:29

No, no.
I mean, it's very like, it's not like the goodness of your heart that you do that.
Like, it's like, it's really is like, well, I mean, it is kind of the goodness of your heart too, but like, it takes a lot.
It takes a lot out of you too.

James O'Beirne: 01:38:44

Yeah.

NVK: 01:38:46

You know, and people want to get paid to work.

James O'Beirne: 01:38:50

It takes four years of full-time context, at least for me.
I'm not the smartest guy in the world, but like, like it's, it's a ton.
It's a ton of time.
And you just, you're not going to make positive changes.
You're not even going to be able to be capable of routine maintenance.
If you don't have it.

NVK: 01:39:05

I think those comments are out of ignorance and frustration.
So yeah, ignorance to like how the software works, how it's maintained.
And then there is frustration with things like how things get activated.
And, and, and the consequences of where things are not truly thought through.
I mean like, you know, nobody would have thought that people are going to use the discounted, unlimited witness of taproot to put in Dick-butts.
So the answer is, listen, stop f**king with my money.
Please stop making changes.
So like I understand that that's the sentiment that a lot of people get.
And it's fair.
I mean, yeah, they're not necessarily wrong to say, You know what, stop it.
I don't want more changes.
I don't want more features.
It's good enough for me.

James O'Beirne: 01:39:48

Emotionally, that's a completely fair stance.

NVK: 01:39:51

But the market might not agree with them.

Mike Schmidt: 01:39:54

You need a 25.0 release of Bitcoin at some point.
Otherwise, you're trying to run Bitcoin on a floppy disk, you know, from 1992.
It's just you need certain things to be done that are maybe not the interesting proposal like `OP_VAULT` that James is working on, which I think is also valuable.
But I think these ossification folks don't realize that the ossification that maybe they're seeking, then maybe we could debate, ignore that debate, but that they're seeking is at the protocol level.
They're not seeking ossification at the software level per se, although the two are somewhat related.
And I think there's a confusion.
This is what I said earlier about we need to clean up and educate within our own Bitcoin Twitter house before we try it.
You know we got people who are side hard money Bitcoiners in the profile who say there's Why is there anybody working on Bitcoin?
Right.
So I think we got education to do.

NVK: 01:40:49

No, but for example, you know, it would be very easy to sell stuff like, for example, encrypted communication between nodes with a white listing.
So they're like you have like pub keys that you share with each other.
And now you're actually preventing spam.
So there's like a bunch of stuff you can do there.
There are things that you can do because those things don't feel like you're messing with people's money.
Even though you are creating slightly different dynamics in a way.
So like, you know, there is a narrative, a narrative issue.

Sjors Provoost: 01:41:16

I think that's not for those people.
On stage, you just try to run Bitcoin Core version 0.1. I've never been able to.
I think I've never been able to run anything before 0.5.

James O'Beirne: 01:41:28

Well you need a Windows computer, right?

Sjors Provoost: 01:41:30

Yeah, for one thing, you need a Windows computer, but try to run old Windows software I think it will refuse to run it because it I think it used to let you run in 32-bit mode and it might not do that anymore.
So operating systems get annoying.
The other thing is compiling gets annoying So If you are a business and you're running Bitcoin Core, probably you are compiling it yourself on your whatever infrastructure.
Wait two years, well maybe on Linux it's a bit longer.
I know on Mac OS, every one or two years, Mac OS will do something to make compiling impossible because they've moved half the system libraries around.
Linux is a little bit less annoying than that, but still, within five years or so, it's going to not compile.
You need to figure out why it's not compiling.
If you wait 10 years, it's just not going to work.
And then you have zero days sitting probably in all sorts of places.
So you can't run it without it getting attacked and shut down.
And then maybe one day it'll be a consensus bug that we didn't realize and nobody knows how to fix it.

NVK: 01:42:27

But that's because people are not running FreeBSD because if they were running FreeBSD like us, they would have servers, they have like six years up-time, you know, running an old core on it and everything is just fine.
Don't touch it.
That's what's working.

Sjors Provoost: 01:42:40

That's what's working.
People were using the same computers that they put in in 1970 because they couldn't replace the actual computer.
If that's how you want to run Bitcoin and sure, that sounds good.

NVK: 01:42:49

I'm just kidding.
But like, I think there is room, for both.
I think it's important that people run old versions.
I think, I think, we need to communicate the importance of gardening, right?
Because, you know, I was one of those people screaming ossify.
But my ossification sort of idea, I feel like it was confusing people.
So I stopped saying it because that included the gardening, right?
Like what I mean, ossification is like, okay, let's be more conservative about new features.
Because, you know, like maybe I want to, like, I want the inertia to start setting in.
I don't know how much more should be done.
Not that I have any control over anything, but like just in my own mind.
Like what is acceptable to me versus potential consequences.

Sjors Provoost: 01:43:34

But I also think protocol is not done yet in the sense that it's not going to be able to handle.
I think James talked about that on the Marty Benta podcast, which was a nice little therapy session, kind of.
It was very good.
In the second half, some people didn't like the `OP_VAULT` stuff because it was too technical, but just stuck through that.
I mean, that's not interesting, but if you stick through it, it gets really existential.
And one of the things is, yeah, we need, if we want Bitcoin to work for the world population, and let's assume that it doesn't actually grow too much.
It sticks to the order of 10 billion.
Yeah, we have some work to do.

NVK: 01:44:08

You know, recently after the whole drama with ordinals, right, I think I was talking to Rindell And I sort of kind of came to this realization just talking that like, okay, so it's 5,000 years have passed.
Like there is not a single person that has been able to verify from Genesis anymore.

Sjors Provoost: 01:44:30

Yeah, I think that will happen eventually.

NVK: 01:44:32

And no, but it gets extra interesting, right?
You could have had some fork a thousand years in, they got swept under the rug and the people a thousand years after that sort of like forgot that history and sort of like moved on, you know, maybe there was a great fire in the cathedral, right?
Like, and all the documents were burned.
And this has happened throughout history, like a multitude of times, right?
In the cultures, they were the best at maintaining documentation in rocks.

Sjors Provoost: 01:44:58

And there will be coins that people will allege are unfairly created.
So there will be very rich families or ethnicities that will be accused even just falsely accused of owning false coins because some of the history is gone.
And then the conspiracy will say well in that piece of history that we lost, that's where these people created these fake coins and then there'll be horrible wars over it.

NVK: 01:45:21

yeah.
You know, like having a form of conservatism, right?
That is not Lewdism.
And having that as like this gardening mentality is the little bonsai, you try not to kill it, you just want to keep it going in a certain direction.
Like, and conveying that, educating people on that, and like literally explaining, if we don't change this, you cannot run Core in the new processor.
Like, if we don't do this, you can't do that in this other way of routing on the internet.
Like things like that.
I think it will help people understand that some changes in software need to exist.
Or you're screwed.
Or you might have the best version of Bitcoin, a floppy drive, and you cannot find a floppy drive, right?
Like that's what happens to software.
God, I have some zip disks around.

Sjors Provoost: 01:46:11

Well, people have an ideal picture of what Bitcoin should be.
But it is important to realize that what Bitcoin should be is not what it actually is.
Usually, you know, the reality is a little bit more complicated.

NVK: 01:46:24

Maybe just separating more of the consensus stuff from operational business logic stuff might help a lot.
Like, And I'm not talking about the core, like the node versus the wallet part on Bitcoin Core, which is like God-awful work and God bless if you're trying to do that.
And I'm talking about like, and that's where it kind of goes back to the BIP stuff, you know, like for example, Craig wanted a BIP to do labels, right?
So wallets had like a standard for labels.
Like, you know, and I'm not saying I have an answer either, but like having sort of like this other section of Bitcoin Core, it's kind of like formal, it's kind of like Bitcoin Core-ish style, but it's like for things that are unrelated to consensus, unrelated to deep code.

James O'Beirne: 01:47:07

I get what you mean.
Just having a centralized index where you can kind of browse like, okay, well here are some standards that maybe aren't, you know.

NVK: 01:47:13

Yeah.
And maybe they get assigned a number too in a different thing.
Like you have a separate spec there that's for like, you know, like IO stuff or whatever.
Like maybe it's overcomplicating.
I don't know.
But like industry wants something set in stone to develop on top.
Like ideally.
So it's like, you're not like, for example, we, we did the PSBT thing was forgotten.
Nobody was using it.
But then as soon as we started doing PSBT because nobody was going to do it.
Oh no, we want to kind of change it and fix it a little bit.
So it's like, ah, you know, of course, this was going to happen.
Like everybody forgot about it.
Nobody wants it, but then somebody starts using it.
Well, let's change it.
So it's just this idea of having a better place for standards that are more business logic standards to exist that may be separate the drama of that from the consensus drama, which is very different.

Sjors Provoost: 01:48:04

But so far it's just one giant blob of code and it is being organized better, but I think no matter how you do it, you also want to clean up the code in that giant blob or even in the consensus part of, however, you want to define that, Even if we have a separate kernel, you know, that's being worked on, that kernel itself will have C++ code that we'll want to make maybe safer so it doesn't crash or so that it still compiles or so that it validates signatures three times faster.
Things like libsecp, sorry, `libsecp256k1`.
That's a library and it's being maintained and it is extremely important.

NVK: 01:48:38

Can you imagine if that was done inside Core?
I think it was brilliant that they did it outside.

Sjors Provoost: 01:48:42

It's done outside Core, but it is being updated to Core.
And that's a library that I don't know how to review it.
It's super scary.

NVK: 01:48:51

I don't think there are more than 10 people in the world that can.

Sjors Provoost: 01:48:55

I feel good when I see the test suite didn't change.
Then If the right test factors are there, it's probably not malicious.
But good luck reviewing that.

NVK: 01:49:06

No, but like that's the thing, right?
It goes back to this heuristic of having grey beards you trust.
I mean, like you're not going to get out of that.
That's true for airplanes.

Sjors Provoost: 01:49:13

Not just the grey beards.
I mean, you can also, you will use the new version.
You will sync the Bitcoin Core blockchain from scratch with the `AssumeValid` off and a bunch of things like that.
So you know, at least whatever shenanigans they did, they didn't like, you know, if I run that thing in a new blockchain appears now, like, yeah, this is odd, but that that usually doesn't happen.

## Audience questions

NVK: 01:49:35

Hey guys, we're hitting two hours here.
I want to be respectful of your time.
Do you guys want to go through some questions here from, from the audience or, or, or you guys sort of like, okay, like I think we've addressed most of it and sort of cap it at that.

James O'Beirne: 01:49:49

Yeah.
Let's do questions if you think there are good ones.

NVK: 01:49:51

There might be, I haven't read them yet.
So a heads up there.

James O'Beirne: 01:49:55

Oh, Nostr only.

NVK: 01:49:56

So, okay.
So can a more public-facing website be built to show active developments and what stage they are in, navigating GitHub can be imposing for the average person from Andrew.

Sjors Provoost: 01:50:15

It's problematic for Bitcoin developers too.
You can be working in your own little corner and you have no idea what's happening in others.

NVK: 01:50:19

I think it's two things.
I mean, the average person is not gonna understand what's going on anyway.
So I think that the proverbial average person is completely hopeless and is gonna have to trust companies and people.

James O'Beirne: 01:50:30

Well, Optech, like you said, does a really good job of surveying everything.

Sjors Provoost: 01:50:35

And also reads the mailing list for you.
That's very nice.

James O'Beirne: 01:50:39

It's just a lot of work.
It's a ton of work to aggregate that stuff.
You would really have to go out and like basically interview all the frequent contributors.

NVK: 01:50:47

And you don't know what's going to stick or get abandoned for a while either.
It's like you don't want to invest too much effort into stuff that could just sort of sit there forever.

James O'Beirne: 01:50:55

Yeah, I mean, Pierre's Bitcoin Axe thing was pretty cool.

NVK: 01:50:58

Yeah.
What was, and you could put bounties, right, on PRs too.

James O'Beirne: 01:51:02

It didn't really work though.
Like the bounties never really worked.
I think you could kind of.

Mike Schmidt: 01:51:07

There are a couple of different layers.
Obviously, if you know enough, you can look at the code or issues.
Then at a level higher, some of the PRs are tied into projects on GitHub, which may help summarize some of that, but I think a lot of that gets out of date and maybe that's still too technical.
Then you have Optech, which does this weekly, but it's still pretty granular.
I've tossed around the idea, maybe even James, back when you were at Optech of Optech being like the what, what happened, what got changed, what got discussed, what's on the mailing list.
And there is the ability to maybe have a so what on top of that, that digest that.
We did one of those with Optech and had the executive briefing and sort of summarized that for executives.
Maybe there's a way, for example, to take the Optech end-of-year digest mammoth write-up and doing a so what on top of that.
And maybe that would make it more accessible for people.
I don't know if that's what that question is asking but maybe that's a potential solution.

NVK: 01:52:15

I normally don't have time to go through the whole Optech.
It's like because it's just there's too much stuff going on in Bitcoin.

Mike Schmidt: 01:52:21

How dare you.

NVK: 01:52:23

And you guys are really curate.
No, and you guys are curating all that stuff into even last.
You condense that and you give a lot of TLDRs, which is fantastic.
But it's just too much.
So one thing that I really love is the spaces that you guys do, which I wish was longer.
I really wish it was longer.

Mike Schmidt: 01:52:39

You want it longer?

NVK: 01:52:40

Yes.
I mean, there's no topic in Bitcoin that it can do in less than two hours.
This was something that one of the reasons why I started the spot is because you cannot have any Bitcoin conversation in less than two hours.
Like if it's less than two hours is because it's just interviewing a person who's like sort of like explaining exactly what the narrative they had in their mind.
Like, which we all do, but like, it's, it's impossible.
Like this topics just have too many tangents.
You're complicated, you know?
So yeah, longer, or, or like more of them in topic specifics.
One good thing is like, for example, in the interview style, like delivering episodes on pretty much everything that happens, right?
You'll find the person who either created the problem, resolved the problem, or proposed something and have the person talk for an hour there, right?
That's very helpful too.

Sjors Provoost: 01:53:30

I know another podcast.

NVK: 01:53:32

Sorry?

Sjors Provoost: 01:53:33

I know another podcast.

James O'Beirne: 01:53:34

Yeah.
The Sjorsnado.

NVK: 01:53:36

Yes.

Mike Schmidt: 01:53:37

Yeah.

NVK: 01:53:37

But you know like, but your pod is like, is very good for like average people to try to understand Bitcoin, but it's not like addressing like specific like issues that are timely or is it like.

Sjors Provoost: 01:53:48

Yeah, it's mostly actually we try to be evergreen.
So there are lots of episodes and some people will even approach me saying oh I just listened to your entire backlog which is like that's impressive.

NVK: 01:53:57

That's what people do by the way.

Sjors Provoost: 01:53:58

Yeah, and the thing is most of these episodes are still correct.
Some of the proposals may have changed a bit.
But it is not a current events episode.
It's just that we often run out of topics and then we'll do like, oh, what's new in Bitcoin Core Vision 24?
And that's our version of clickbait.
But we'll still explain what's in there.

NVK: 01:54:18

But I am a listener.

Sjors Provoost: 01:54:20

Thank you.

NVK: 01:54:21

All right.
So let's move on to the next question here.
Current FUD from MSM about the small number of devs that we've already addressed that one that was from 1F52b.

Sjors Provoost: 01:54:32

Well, we didn't address the part that they confused developers and maintainers.
They really just suggested there were like six developers, even though there are more than a hundred.

NVK: 01:54:42

No, but I don't think we can address that.
That's just stupid.
Like, you know what I mean?
Like it's easy, either like malicious stupid or just like, you know, like, peacefully ignorant or whatever.
It's just, you know, that's just read more.

Sjors Provoost: 01:54:54

I've heard a little thread on Mastodon basically pointing out some of the errors in the article, including I think that one.
Anyway.
Yeah.
We've addressed it.

NVK: 01:55:02

Yeah, Okay, Ben Gunn.
Please debunk the thought about the centralization of contributors, same one.
Like, so this is what's doing the rounds.
Yeah, I mean, it's gonna be centralized because there's only so many brains in the world.
So the easier the problem, the more people are there to help address it.
And you know, you're going to have to trust people to a certain extent, but we have great webs of trust so that you can check the signatures and check the code and check the releases.

Sjors Provoost: 01:55:31

We also have this thing called the whistleblowing effect.
So even if the person you trust to keep an eye on things might be asleep, as long as you have some access to what happens in the rest of the world by being on some social network or talking to some people occasionally, you'll find out that there's something really bad going on.
That's also a mechanism that you're trusting, I think.

NVK: 01:55:54

Yep, Christopher Liss.
I still don't entirely get the derivation path and why it can't be the same.
Okay.
This is out of scope for this episode.
I highly, recommend going check out <walletsrecovery.org>.
I put all that information there.
Bitburn.
I would cover some aspects of the blockchain wars and the history of development.
I think we've sort of gone around it.

Sjors Provoost: 01:56:22

And there's a book about the blockchain wars, right?
Called The Blockchain Wars.
The Block Size Wars, Jonathan Beer.

NVK: 01:56:27

Yeah, BTC Totoro.
I'd love to hear a bit about what a day or a week in the trenches working on Bitcoin Core is like day in and day out.
Does the job feel isolating and alone or is it the opposite where it's lots of people willing to help and find issues?
Well, the two of you there called on it so go for it.

Sjors Provoost: 01:56:54

It's basically like any job where you're working from home except you don't have direct colleagues in the same way you don't have a boss who's screaming at you, and so you have no idea what you should be working on.
No, it's not, I don't know, it's not always easy.

James O'Beirne: 01:57:10

No, I find it exceptionally difficult at points, especially if you're kind of in the middle of working on something that's not, you know, getting a lot of reviews or you're unsure about how to proceed on something or, you know, you're kind of you spend a lot of time trying to figure out what's worth working on.
And the other thing is you spend a lot of time doing code review because code review is one of the most valuable things in Bitcoin.
Sjors is really, really good at doing reviews and testing.
But that's, you know, it's kind of I mean, personally, I find a lot of joy in being in an office environment and seeing people and talking to people and seeing people face to face.
And you get zero of that because you get it a few times a year when the core devs, some of them meet.
But for me, it's very isolating and very difficult.

Sjors Provoost: 01:57:57

Well, one thing that's peculiar about, I guess, Bitcoin Core as a team or to the degree that it's a team, there's no office.
There's no central office.
There's not even a central spot.
It's not like, oh, if only you move to City X, then you can be somewhat more in people's company.
Like, you know, there are some cities where you have more than two.

NVK: 01:58:14

It's also very academic too.

James O'Beirne: 01:58:16

It's very academic.

NVK: 01:58:18

It's, You know, like you have to have a, like a threshold of, of like pain that's very high, at least in my view, I don't exist in academic environments.
Like you have to be prepared for that sort of like, you know, slow pace and sort of like a very sort of like review like and, you know, it's the opposite of business really.

James O'Beirne: 01:58:39

I tell people it's like doing a PhD except you don't have an advisor.
Like you're just on your own, you know, hoping you're doing something useful.

Sjors Provoost: 01:58:47

Well, worse than that, I think, because there's no scope.
So it's not ever finished, you're not producing a single document.
Although some people like yourself are working on very specific fairly large projects that at least give you some focus.
One of my things is that I review very random stuff.
So there's almost no scope there.
That can be tricky.
The other thing that is just generally more fun, I guess, or not like a serious problem, but the way GitHub works is it uses notifications.
I have been advocating for killing that blue dot because it just draws my attention.
What it does is it makes you focus on pull requests that get activity on them.
What it means is that you'll focus on things that are very active and it's very easy to start forgetting about stuff that is not active.
So it actually amplifies a pull request that becomes stale become even more stale because nobody's getting notifications for them and nobody looks at them.

NVK: 01:59:46

But there's perverse incentives there.
Yeah, and then you get to a point where it's like apps, right?
Like people creating new releases just so people look at it, right?
People are gonna keep on updating the code even though there's nothing that should be updated.
Did they update just the docs or something?
So it goes up.

Sjors Provoost: 02:00:01

I'm doing that so that I get on your podcast.
But there are some countermeasures.
Like I have my own to-do list system that will actually show me what things I want to review.
But sometimes I don't get to that.
And I review recent stuff more often.

James O'Beirne: 02:00:15

I have like five of those to-do list systems and I keep making them and abandoning them.
Like I have, you know like five different lists with PR numbers on them to review.

NVK: 02:00:23

You know, I do not do to-do lists.
F*ck to-do lists.
F*ck calendars.

James O'Beirne: 02:00:32

No calendars.
Wow, That's barbaric.
I don't know.

NVK: 02:00:35

You know, like I have some bare calendars, like for example, Johnny would put the episodes to do, or, you know, I have a call with a lawyer, but I don't schedule a single anything unless it's like, you know, trying to get a group of people to do a very specific for anything more than two days.
I don't schedule anything more ahead than two days.
I want my calendars clear, completely clear so that if I want to do something, I can do the thing.

Sjors Provoost: 02:01:01

Yeah, same here.
I think, I mean, I use calendars only for things that physically have to happen at a certain time in a certain place.
I do not use them to say, oh I'm going to work on X, I'm going to work on Y.
It's very GTD and I'm not saying GTD is perfect.
GTD has some huge drawbacks but I've been using that since 2005, I think.
And as a general system, I like it.
And the tool I use for it is OmniFocus, which is a simple Mac app.

NVK: 02:01:27

I remember that one.

Sjors Provoost: 02:01:28

And it really does the job.
The thing is, GTD, you can have a to-do open for months and you won't forget it.
So the nice thing about GTD is you will never forget to do something.
However, you may still never do it because you're just not doing it.

NVK: 02:01:44

Yeah, no, I can't deal with that.
It's like, you know, if I have things that need to be done, they're gonna get done.
If they don't need to get done, they're getting off the list.
There's no middle ground.

Sjors Provoost: 02:01:55

I'll toss everything in the system that needs to be done, but sometimes, but usually when I'm doing things, I'm just doing them based on notifications or what I feel like.
But then I know that I have this trusted fallback system that I can go through every item and make sure that, you know, the things I did impulsively, I can just check off and the things that I didn't do then, oh yeah, I need to do those.
So it's a nice system, but yeah.

NVK: 02:02:17

You know, unimportant items, just it's like, it's like noise pollution in things to do.
They just like deviate you from the things that are actually important shit gets done.
Yeah.

Sjors Provoost: 02:02:26

But not when you're reviewing,

NVK: 02:02:27

you know, like it just because it needs to happen like taxes or like, you know, shipping, whatever.
Like if you're like pushing from, from like pushing say new firmware or something, like it's probably because those features are not that important.

Sjors Provoost: 02:02:44

No, but if you look at like, you know, in GTD you have things, something called a project, which is anything that's more than one action.
A lot of my reviewing things are basically saying, wait for this thing to get rebased or updated.
That's just a waiting-for thing that's there.
So occasionally that'll pop up and I'll look, okay, has this actually somebody touched this?
And then the next instruction would be for me to test it or, for my own pull request, usually, the project just consists of waiting for feedback or it being merged, but that's a one-action project.
So it's still nice to have a list of things that I care about.

Mike Schmidt: 02:03:19

The Eisenhower Matrix.
The urgent and important.
And you don't necessarily want to be spending your time in the urgent important quadrant of that.
You probably want to be spending your time in the not urgent but important category so that you don't have to worry about that.

Sjors Provoost: 02:03:37

Just get shit out of the way.
Well GTD makes no such quadrant.
It's just things that can be done given the context, given that you are behind your computer, what could be the next action?

NVK: 02:03:49

Maybe we should do an episode on just that time management.

James O'Beirne: 02:03:53

I'd like that.

Sjors Provoost: 02:03:54

It just works better.
I mean, if you ever want to read the book, you should read the original one.
So the one from the 1990s, which uses very analog technologies to get the job done.
He wrote a new one, but it's too abstract and too long.
So stick to the old one.
And the thing it doesn't really account for is this world of instant notifications that we're getting now, which GitHub is one of the problems, but emails and others.
I mean, part of that is just you want to kill all those notifications.
And you should not get you should not be getting push messages from Twitter.
That's like if that's what you're doing, that's not good.

NVK: 02:04:29

Yeah, I think people just struggle with actually triaging what is actually important.
And then like, and then sort of like the complacency kind of sets in because you know, it's just we're all human, right?
Like it's really, it's just, that's the true challenge is like what's really important.
And then like people don't leave room to just like fucking do nothing to and like just reflect.

James O'Beirne: 02:04:50

And that's very important.

NVK: 02:04:52

Be stupid.
And that's where the best ideas come from.
It's like you know people are like oh you know like I can only do coffee for 15 minutes.
What kind of life do you live?
Like I could sit here with you for the afternoon and I have a company to run.
Like you must be really, really, really important.

Sjors Provoost: 02:05:09

Yeah, you don't have to be busy all the time, all the day basically.


NVK: 02:05:13

That's horrible.
Anyways, all right.
So a couple more questions here and we're setting this one off to bed.
Aside from C++, are there any prerequisite skills, or knowledge a dev should have before attempting to contribute?
Gary Kraus.

Sjors Provoost: 02:05:29

Python is nice.
That's great.
Some people have actually, that was their entry point.
They knew Python and they would be helping write better tests.
C is nice if you want to work on `libsecp`.
C is not nice, but it's useful for that.

NVK: 02:05:44

No, but C is like, if you can do C, the world is your oyster.
It's like, it's a different thing, right?
You understand computers now.

Mike Schmidt: 02:05:52

I think the philosophy is important too.
I think there are a couple of different documents that would help even if you do know sort of the technicals.
If you're talking about doing Bitcoin Core work, there's a Bitcoin development philosophy doc that's on GitHub that you may be interested in from a philosophical perspective.
And then Will Clark is working on an onboarding to Bitcoin Core document as well that I think if you combine that with the technical knowledge would be very valuable for a budding C++ Bitcoin developer wannabe.

Sjors Provoost: 02:06:28

Yeah, and if you wanna do testing, you don't actually have to understand either of these languages, at least not in detail.
What is much more useful for testing is understanding how Bitcoin Core should behave.
A lot of what I do with video is just like, I'll see somebody change something and I know how it should behave and I'm going to try and guess what they forgot and then see if I can break it very quickly and then just say okay you broke this part and then move on to the next pull request.
So just knowing how a piece of software should behave, is a kind of QA work that is useful too.
Though it does require that you've probably used this offer a lot before you know, because otherwise you're going to file bugs about bad behavior in Bitcoin Core and I can guarantee you those bugs have been filed hundreds of times and nobody wants to fix them.
So it is important to know what the things are that are bad that we care about.

NVK: 02:07:17

This reinforces this idea that like, you know, and why you need to have full-time people on it is because it takes like, you know, like nearly a decade for somebody to have full visibility on the code base.
Like, like a good sort of broad view on what's going on.

Sjors Provoost: 02:07:33

You will never have full visibility of the code.
Yeah, but full visibility on like 10% of the code base.

NVK: 02:07:39

Sure.
But the point is that like, you know, it takes years for you to sort of like get what's going on.
Right.
Like in a system that's that complex.
And that's why you want to have people that make their money, like doing that all day.
Right.
Like if you're just like a tourist to Bitcoin Core, you're not going to understand why something was done in a stupid way or why it was inherited that way and is not going to change.

Sjors Provoost: 02:08:04

I don't think you need to do it full-time, by the way, but I'm very Dutch in that sense.
I think you can do things part-time, but it's nice to have long-term continuity though.

NVK: 02:08:13

Yep.
There was, Okay, so here's another question that's along those lines too.
An open source optimist guy.
How are decisions made about code-based structure and best practices?
So like, I'm just interpreting his question here, but like code structure and sort of like best practices and sort of like how the core sort of like prefers things to be done.

Sjors Provoost: 02:08:37

And there's a developer notes markdown file in the GitHub repository that has a bunch of these standard things like, you know, do the indentation this way, do the indentation that way.
There are a few linters that check things and other than that I think the convention is to do whatever similar code was already doing, like kind of just follow the existing pattern.
Don't go and refactor all the commas in the code, you're not going to make people happy.

James O'Beirne: 02:09:04

The document that Mike referenced earlier, the onboarding to Bitcoin Core, I think spends a lot of time talking about architecture and the considerations that would involve and how the evolution of how things has gone.
So That's really, I mean, you could do a two-hour podcast on just how core should be architected, how it is architected.
So that document's definitely worth reading if you're curious about that.

Sjors Provoost: 02:09:25

Yeah, but usually if you're making a small change, you're not changing the structure that much.
So if you're new to the project, you probably don't need to know all that because you're just gonna make a small change.
Though, if you wanna, you know, if you're making any more complicated change, you'll have to understand at least how the code works.

NVK: 02:09:42

Okay, so BourbonicPlague.
Would love to hear a discussion around contributing anonymously to risk personal attack and all that stuff.
So the other day I made a post about how like I think maybe people should share IDs, do ID mixing, and all like ID shuffling.
And you know I highly like to recommend people doing, creating NIMS for their submissions.
The code is gonna get reviewed anyway.
It's not because you have a bigger name that your code is not gonna, like it's gonna go faster or whatever.

Sjors Provoost: 02:10:17

But do you remember the thing that we just talked about, but like the work being quite hard and you very occasionally meeting other people?
Now you're removing that part too because you're not.

NVK: 02:10:27

Yeah, but you know, safety, right?
Nothing is without trade-offs.
Maybe you have some great ideas or you want to fix some work and you don't want to expose yourself to any dynamic that may come from working on Bitcoin, positive or negative.
You know, come in as a NIM, do something, and leave.
Xiaolongfan.

Mike Schmidt: 02:10:43

Yeah, Z-Man's doing it, right?
He's got funding.
He's got funding as far as I know on and that's anonymous.
He communicates with voice and he's been on the Optech recap that we've done.
So he's still connected and maybe maybe he wouldn't do an in-person meeting.


NVK: 02:11:02

But you know, like guys, it's also not that like I think like the fear is blown a little bit out of proportion because, you know, a few devs had issues with Craig Wright and stuff.
I mean, realistically speaking, like, you know, there's a lot of people working in, And like the great majority never had any issues that I know of.
So, you know, like don't just fall for the fear to like, you know, have some balls and go get some shit done.

Sjors Provoost: 02:11:25

Kind of depends on where you live, too, right?
If you live in a sort of, you know, free speechish place, it's going to be a little bit different than if you live in a country where being even remotely involved with Bitcoin is like death penalty stuff.

NVK: 02:11:40

I think I think we can leave it on that note.
Listen, guys, this was a huge pleasure.
I really appreciate you guys putting in all this time.
I hope we managed to have people sort of like have another inch of understanding of how Bitcoin works and the dynamics in that.
I think many people who listen to this, to the show, probably know how to contact the guests and sign up for Mike's mailing list.
You know, subscribe to Sjor's podcast, you know, follow James in multiple places.
So any final thoughts, James?

James O'Beirne: 02:12:21

Thanks for throwing a great podcast.
I always love coming on and talking to you.

NVK: 02:12:26

Hey, man, I really appreciate it.
You guys are awesome.
Sjors.

Sjors Provoost: 02:12:34

Thanks for having me.
And yeah, please check out Bitcoin Explained.

NVK: 02:12:39

And buy his book.
Mike.

Mike Schmidt: 02:12:44

Yeah, I think it's easy to listen to two and a half hours of people talk about how strange everything is and BIPs here and that and activation and fighting and mailing lists and to be discouraged by that.
But I think that the alternative is much worse, which is organization and control centralized in a single place.
And Bitcoin represents the opposite of that.
So I think we should embrace the decentralization and some of the chaos and craziness that we've talked about on this call as a positive thing.
So just maybe try to end on a high note.

James O'Beirne: 02:13:25

It's a really good point.

NVK: 02:13:26

Oh, for sure.
I mean, it's working.
Bitcoin is working.
People are working on it.
Businesses are being built on it.
And you know, like it's hard, but it's clearly going somewhere.
And with that, I, you know, closing up.
Thank you so much, guys.
Thanks for listening.
If you're new to the pod, make sure to listen to some very cool other episodes.
Episode 15 about Lightning.
Episode 11 about podcasting 2.0 and value for value.
And we also had a hardware wallet security panel on episode five.
Don't forget to follow at @BitcoinReviewHQ or get in touch on Telegram [Bitcoin Review Pod](https://t.me/BitcoinReviewPod), or Bitcoin Review at CoinKite.com.
We don't have a crystal ball, so let us know about your projects.
Leave your Boostogram on this episode and we'll try to read it on the next episode.
We've added more people to the splits.
Now, if you send us streaming sats, some of that go to [opensats.org](opensats.org) and also to Citadel Dispatch with my guest Odell.
If you don't know much about Value for Value or Bitcoin Podcast 2.0, Go to [bitcoin.review/v4v](bitcoin.review/v4v)
