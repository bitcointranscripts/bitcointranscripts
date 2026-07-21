---
title: "Crashing Bitcoin Core with Niklas Gögge's Fuzzamoto"
speakers:
  - Niklas Gögge
  - niftynei
date: '2026-02-10'
tags:
  - fuzz-testing
  - bitcoin-core
  - security
  - testing
  - btcplusplus
categories:
  - podcast
source_file: https://youtu.be/_TsK_3bYpu8
media: https://youtu.be/_TsK_3bYpu8
summary: In this Bitcoin++ Insider Edition interview, niftynei sits down with Niklas Gögge (developer at Brink) to discuss Fuzzamoto, a coverage-guided fuzzing framework built to test Bitcoin full node implementations — currently Bitcoin Core, BTCD, and Libitcoin — by running the actual production daemon and exercising it through its external P2P and RPC interfaces rather than individual functions. The interview covers fuzzing fundamentals (coverage maps, corpus mutation, dictionary hints) and includes a live demo where Fuzzamoto, running across 32 parallel VMs, rediscovers a historic divide-by-zero bug in Bitcoin Core's Bloom filter code triggered by a specific filterload/filteradd message sequence, showcasing how automated fuzzing removes human bias and surfaces multi-step edge cases that unit tests typically miss.
transcript_by: 0tuedon via tstbtc v1.0.0 --needs-review
---

Speaker 0: 00:00:00

I mean, I can just like start blabbing about the tool and like...

Speaker 1: 00:00:04

I mean, I think the first one is like, so I mean, it's like, Hey, I'm Nifty.
You're Niklas.
You work at Brink.
What are you working on these days at Brink, Niklas?

Speaker 0: 00:00:18

Yeah.
So I currently mostly work on Fuzzer Moto, which is a fuzzing framework and also a fuzzing engine that I've built to specifically fuzz Bitcoin full nodes.
So currently mainly Bitcoin Core, but I have and do plan on supporting other implementations as well.
Like I have done some BTCD fuzzing and Libitcoin as well.
And the main point of supporting all of the different ones is eventually to have differential testing between all of these implementations, because the more implementations you sort of add to the mix, the better your Oracle power in like finding bugs gets.

Speaker 1: 00:01:04

That's cool.
Okay, I'd like to hear more about that maybe in a minute because I don't know what Oracle power means, but maybe just for like, so I'm talking, I mean, I know what fuzzing is.
Like I remember when Matt Corallo started doing fuzzy and lightning in like 2019, 2020, right?
So like, but I think there's a lot of people even like Bitcoiners or technical Bitcoiners that don't really know what it means to do fuzzing.
Do you have like a, I don't know what's to explain like a 5 version of making of what, like When someone says they're doing fuzzing, what does that even mean?

Speaker 0: 00:01:35

I can try.
So fuzzing is basically an automated and randomized testing technique for software.
And the most common form that most people that have used it before will probably be familiar with is that you test individual functions in your code or maybe classes and you test the APIs of the classes.
So the most well-known fuzzing engine is libFuzzer, which ships with the Clang compiler.
And there's also AFL++ or HongFuzz.
And all of these three engines are like general purpose fuzzing engines.
And that basically means that, actually I think I kind of skipped ahead a little bit too far in explaining the tools.
Okay, maybe the dumbed down idea for fuzzing is that you have a piece of code that you want to test.
And then all it basically is that you have a loop that calls this piece of code that you want to test over and over again, and it'll pass randomized inputs to, let's say, the function that you want to test.
And then there's a whole bunch of optimizations to make that fuzzing loop smarter.
So for example, to make smarter mutations, to have better inputs to your function.
There's also, which is now basically the default for all fuzzing efforts, but initially it wasn't.
There is coverage-guided fuzzing, which essentially means that you will pass an input into the function you want to test, and you observe which parts of the function you reached with that input.
And if you've reached something new, you'll keep the input in a set, which is typically called the corpus.
And then later on, you'll pick an input from your corpus again, mutate it, pass it to the function again.
If it hits something new, you add it to the corpus.
If it doesn't hit something new, you just discard it and pick the next input.
Or if you find something interesting, like a bug, for example, a crash, then you also report it as, hey, there's something wrong.

Speaker 1: 00:03:58

It's kind of like, You know, there's this like,
I don't know what they call it, like a thing, like if you take a million monkeys and you give them typewriters and you give them like, you know, you put them in a room, how long would it take for them to like recreate Shakespeare?
Is it fair to say that fuzzing is kind of like having a bunch of monkeys in a room poking at the typewriter, but the typewriter is your program?

Speaker 0: 00:04:21

Yes, yes, I think that is a, I mean the analogy breaks down at some point, of course, but yeah, that is a way of putting it.
I think you could say maybe that the monkeys, or, yeah, no, I think that's a good way of putting it.
That's an optimization that would basically translate to making the monkeys a bunch smarter, like maybe knowing pieces of the Shakespeare poem or whatever.

Speaker 1: 00:04:50

Maybe they use a dictionary so they're showing where you can set it.

Speaker 0: 00:04:53

Exactly.
Like there is literally a concept of a dictionary where fuzzers like have certain interesting pieces of bytes that we know are interesting so the fuzzer can insert.
Otherwise, if you have to guess, let's say you have to guess a sequence of eight bytes, and if the fuzzer has no knowledge of those special sequences, it'll take a long, long time to actually guess the right thing.

Speaker 1: 00:05:20

Got it.
That makes sense.
Right, so you kind of help it out with pre-picks.
These are some juicy byte sequences.

Speaker 0: 00:05:27

Yeah, exactly.
In the Bitcoin protocol, For example, we have for the networking messages, the type of the message is a string.
And then one of those useful things you could put in your dictionary is the strings for each of the message types.

Speaker 1: 00:05:43

Okay, yeah, that makes a lot of sense.
Why is it called fuzzing?
Do you know where the name, but why do they call it fuzzing?

Speaker 0: 00:05:53

I don't know the exact origin.
In my mind, it's just that you take something that exists and then you make it fuzzy, like you change it a little bit.
I don't know.
There's probably a better explanation for where the name comes from.
I don't know the exact origin.

Speaker 1: 00:06:12

Yeah, but so you've been working on fuzzing for how long now?
Like you joined Brint and started immediately like where like fuzzing is the coolest thing ever or like how did you end up getting into a point where you're building tools like Fuzzamoto?

Speaker 0: 00:06:26

Yeah I got really like I hadn't really used it before I started working on Bitcoin.
I think there was like one instance while I was working on Firefox where, I don't know, I think I wrote some code and then one of the first tests crashed and someone came back to me, hey, can you like look at this?
But yeah, I got really into it after joining Brink because I was refactoring some code and the whole point of that refactor was to add more tests.
And one of the things I found in BigConcord was that there were a lot of these fuzz tests.
I didn't really know a lot about it, but I wanted to learn more.
So I refactored the code as planned and then also wrote a fuzz test for the code that I had refactored, sort of proving the point that you can now write better tests once you've done the refactor.
And that turned out to actually find a pretty serious bug in the end.
And from there on I was kind of hooked because I was like, oh, this is great.
And then I went down the whole rabbit hole and now this is pretty much all I do.

Speaker 1: 00:07:32

Funny.
So let's talk about Fuzzamoto, which is the project that you spend most of your time on.
You said that you use it to test full node implementation, so this means you have to build the project and then you run Fuzzamoto against the binary of Bitcoin core?

Speaker 0: 00:07:50

Yeah, so this tool is, it's like the approach is a bit different from like the typical fuzzing you will see because it's not targeting like a specific function or some like API of a class or something in the code, it's actually fuzzing the whole full node daemon.
The idea is to actually use the daemon as close as possible to the production binary that we ship.
But there are a few tweaks we have to make to actually enable us to efficiently fuzz it.
But yeah, basically the idea is that you build Bitcoin Core as close as possible to the production setup.
And then you give it to the father and it'll like, use the external interfaces of the node, like the P2P port, which is sort of the most interesting surface security wise that we care about, or the RPCs, or whatever interface the node has available we can sort of use to test it.
And Yeah, I guess, I don't know.
What should we talk about next year?

Speaker 1: 00:09:09

Do you want to do a demo maybe?
Maybe that's the easiest way to get it running.
So you get your terminal up, what do you have running here?

Speaker 0: 00:09:18

Yeah.
So the way it currently works, if you want to use this, there's a bunch of Docker files in the Fuzzer Moto repository, and they essentially set up the whole environment that you need to use the tool.
What you see here right now is that I am in one of these containers that I've pre-built, so we don't have to wait for the build to finish here.
In this container, we have a Bitcoin D, which is a custom branch that I made to reintroduce some bugs that we previously had.
And then we We also have the FuzzerModo project itself, which comes with this FuzzerModo libafl tool, which is the fuzzer.
And there are a couple of steps that are not that interesting to walk through here.
That you have to like, there's a couple of commands you have to run to like, create the setup, for example, to like create this directory here.
And maybe we can link to the documentation where all of those steps are described, but it's really just very manual, like execute this and then that, and then you have it.
And yeah, so basically once we execute this command, it will start running the tool and we'll start sort of testing the node in various random ways.
And hopefully eventually find some of the bugs that I reintroduced for this demo.
So if we just start this, it takes a little bit at the start because it sets up and it creates a virtual machine and it sets up the Bitcoin D-nodes and then eventually it starts running here.
And yeah, This is basically just some basic output.
We can see how many total test executions we've done, how much coverage we've achieved so far, how fast we're going.
So currently, we're doing 900, 800 executions per second, which is basically like 900, 800 test cases that we do per second.
And then maybe the most interesting is the one at the end, the number of bugs we found.
And so far we have not found anything.
I am not sure how long, it might take like a couple minutes for it to find the first bug.
But while that is running, we can go and look at some of the test cases that it's generating.
I don't know, like sometimes it's, some of the test cases are not gonna be like super involved or interesting, but which directory did I use?
Yeah.
So. Here's a Silly question.

Speaker 1: 00:12:22

How many Bitcoin core nodes do you have up and running at a gantt?
Does it spawn maybe 30 of them or something?

Speaker 0: 00:12:32

The way it works that there's one VM for each, well, you can specify on the fuzzer like how many VMs it should have in parallel.
And then currently in this setup that we have here, there's one Bitcoin Core node in each VM.
So we have like 32 because the machine has 32.
Or is.
32 cores, exactly, we have 32 VMs. And in each of them, we're sort of testing one Bitcoin Core node.
Yeah, and this folder here, the output folder has like for each instance that we're running, we have, so instance zero, for example, we have a queue, oops, a queue folder, which is the corpus.
Actually, let me do this.
So there's just a bunch of files in here that sort of describe an individual test case that we generated.
And then we can run this input locally in this Docker container without, I just picked a random one.
I don't know if that's going to be interesting, but we'll see.
We can turn on some extra logs as well.
Then we can run this input with the actual Bitcoin D binary.
Then once we run this, we will see output from the test and also the Bitcoin D logs while it's executing this test case.
It's just, that's a bunch of stuff.
Yeah, this test case isn't like, we see there's like the Bitcoin core node survived.
There's nothing wrong as far as we know.
At least it didn't crash.
And then if we go up, we can see here there's a bunch of logs of like, orphans being added and removed.
Essentially just the test case seems to be submitting a bunch of transactions to the node.
A bunch of ping pongs.
Yeah, this is like where the test case essentially starts running.
And we could do this for like all the test cases that we have in this queue folder, and each of them will be slightly different, exploring some slightly different scenario.
Yeah, still no bugs.
If we don't end up finding them soon, then I have also prepared, I ran this earlier and I have some of the inputs that actually trigger the bug so we can see what happens there too.
It should find them within five minutes.

Speaker 1: 00:15:29

Cool, I have one quick question about it.
So you've got the coverage number, which is up to 9% now.
So we're tracking upwards.
I'm assuming as coverage increases, our chance of finding the bug goes up.
What's the stability number over there on the far right?
It says like 96%.

Speaker 0: 00:15:45

Yeah, the stability metric essentially describes how deterministic the test is.
So one thing that we want with fuzzing is that if you give the test the same input, we want it to behave the same.
Like we want it to hit the same coverage.
But software is like usually, or often software will not be deterministic.
And this metric sort of tells you, is it deterministic or not?
And if it's not 100%, then it's not deterministic.
So the way the metric is calculated for so the way that coverage works is that the compiler instruments each control flow edge in your program.
And then for each edge, you essentially have a bit in your coverage map.
Then the stability metric is for all edges that you've seen in total, sorry, it's the fraction of the edges that are stable over the number of edges that you've seen in total.
So I guess 95 percent of our edges are currently stable, and the other edges we've seen to be like randomly be hit.
But yeah, it's, for me, yeah, it's not a super useful method really.
I think if it goes like down significantly, then you should probably work on like making your first test more deterministic because yeah, non-determinism can prevent you from finding bugs.
So you do want like all these tools are essentially designed with the assumption that your test is going to be deterministic.
So if they're not, you degrade the efficiency of your testing effort.

Speaker 1: 00:18:01

Wait, so hang on.
Just so I understood the last bit, you design them so that they are the same every time?

Speaker 0: 00:18:07

Yeah, exactly.
Like the, oh, sorry, now we found one crash, apparently.

Speaker 1: 00:18:14

Two, two now, maybe.

Speaker 0: 00:18:16

It's usually, it'll find the same one over and over again.
So the it doesn't be duplicate Again the one of the assumptions that fuzzing tools are Built around is that the thing that you're fuzzing is the germanistic Right got it.

Speaker 1: 00:18:35

Okay, because you don't want to have to run if you run the thing multiple times You don't want it to be like slightly different or whatever.

Speaker 0: 00:18:41

Okay, if you do coverage guided fuzzing then if you find something interesting you save it to your corpus and then if you pick that again and you mutate it, you're kind of making the assumption that you mutate it slightly to find something new.
But then if you execute it again and all of a sudden something random happens and it doesn't even hit the code that you previously hit to save it into the corpus, now it's like something completely different.
So it adds noise to your corpus if it's not deterministic and you end up doing more work on stuff that maybe isn't interesting.

Speaker 1: 00:19:12

That makes sense.
Cool.
Do we want to go ahead and look at what these bugs are just as a, I don't know.

Speaker 0: 00:19:20

Yeah, that should be quick.
So go over to the other one.
We can just see which instance.
So we can see CPU 17 found all of the three.
Then we can use the command I had here earlier.
17, I'll pick one of them.
Oops.
Crash, crash, crash.
And now we should see at the end, crash totter not alive.
Okay, so this crash looks like It is not deterministic because it didn't.
Okay.
I actually have not seen this.
We might have to cut this because I don't know what this is.
I'm guessing it is one of the bugs I introduced, but it's actually not the one that I was looking for.

Speaker 1: 00:20:38

That is.
Yeah, it's okay.

Speaker 0: 00:20:41

I don't know.
It's probably not an actual issue, but Yeah, this is not the one I was looking for, so we'll just pick another one.
This is the same one.
OK, they're all the same.
Crash.
Yeah, it's not a crash because I think this is like the node detecting some error that we can't recover from and then it shuts down.
The actual one I was looking for is like an assert failure.

Speaker 1: 00:21:17

Oh, got it, okay.

Speaker 0: 00:21:18

I'm still guessing that this is caused by the patch I reintroduced.
So let's see if there's, oh yeah, I stopped the fuzzer.
So I can use, damn it.
I do have the ones prepared that I was looking for.

Speaker 1: 00:21:39

Okay, yeah, so this would be like an example of what the crash would look like if, what do you call it?

Speaker 0: 00:21:48

Exactly, like this would be, when the fuzzer finds a bug, I normally reproduce the bug it found in this way to see all the output and potentially already see what the actual problem is, but sometimes you have to do more debugging afterwards to obviously figure out exactly what the problem was.
So this bug, oops.
This is an old bug.
I think this was fixed in like 2013.
And it was a divide by zero in the Bloom filter code.

Speaker 1: 00:22:28

Okay.

Speaker 0: 00:22:28

So this is The FBE signal is, yeah, I think a signal you get if there's like a problem with the arithmetic.
So like a divide by zero, for example, we'll throw the FBE signal.
And then because I compiled with the address sanitizer, we get this nice stack trace here, which at the top we can see there's the bloom filter hash and there's some like divide by zero in there that I reintroduced.

Speaker 1: 00:22:58

And it found this because it sent into like it randomly like the fuzzers, some of the inputs tests that it was doing triggered it such that it tried to divide by zero.
And so rather than have to come up with all the manual test cases as to what to ask, you just use the fuzzer to like hit basically the corner case where the zero is.
So.

Speaker 0: 00:23:19

Yeah.
I think in like this specific bug requires like a sequence of one filter load message and then a filter ad, which adds nothing, which just adds like an empty byte array to the filter.
And that's like the size of that empty array is what's causing the problem and the divide by zero.

Speaker 1: 00:23:39

Got it.

Speaker 0: 00:23:42

So this is not like a complicated bug.

Speaker 1: 00:23:43

It was multi, It required multiple steps to trigger, right?
And like if you, so like the difference between like using a fuzzer versus like, you would have to manually realize that you need to call these two commands in this way to cause it to crash, right?
But the fuzzer can just try a bunch of stuff and find things without you having to figure out what to test, right?
Maybe you could...

Speaker 0: 00:24:05

Yeah.
Yeah.
Normally in unit tests or integration tests, you'll sort of codify what you expect your program to do correctly, but you obviously are not going to cover all the edge cases.
And a fuzzer has a good way of removing your own bias for coming up with the test cases.
So it'll try completely ridiculous stuff that you would probably assume to be fine or haven't thought about or whatever.
And then it'll find edge cases like this.
I don't know if this vibe was found with fuzzing back in the day, but it can be easily found with fuzzing nowadays.

Speaker 1: 00:24:49

That's cool.
Yeah, makes sense.
Cool.
Well, I think that was, for me, this is like a great example of how Fuzzimoto works, that kind of thing.
You're gonna be in Brazil in two weeks to talk about Fuzzimoto at Bitcoin++.
Is there anywhere else people can look to find your work?
Like Fuzzimoto is up on GitHub.
Is that a good place to look it out, try out the project, that kind of thing?
People want to learn more?

Speaker 0: 00:25:16

So there's the GitHub repo.
It has a bunch of documentation, also a little bit on the inner workings on how it works, but obviously the code would be the best source to figure out how it works.
There's also a introductionary blog post on the Brink blog, which also covers some of the design and architecture.

Speaker 1: 00:25:39

Perfect.
Oh yeah, I saw that.
That was an amazing...
You put that out just last month in January, right?

Speaker 0: 00:25:46

And it'll be like a whole series.
I'm not there's no fixed schedule for like the posts to come out But yeah, there will be more posts first of chapter one.

Speaker 1: 00:25:55

Okay, cool Well, thank you for your time Nicholas.
I really appreciate it and I'm looking forward to seeing what you've got for us in Brazil in a few weeks.
Yeah, I don't know if there's anything else you want to leave a note or promote or whatever at the end for people to hear more about.

Speaker 0: 00:26:13

Yeah, not really.
Come to Brazil and you'll learn more about fuzzing from me and a bunch of other people as well.

Speaker 1: 00:26:21

Yeah, it's going to be great.
Cool.
All right.
Thanks Niklas.

Speaker 0: 00:26:24

All right.
Thank you.
Bye bye.
