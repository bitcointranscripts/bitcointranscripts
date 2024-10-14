---
title: 'Code Review and BIP324'
transcript_by: 'markon1-a via review.btctranscripts.com'
media: 'https://podcasters.spotify.com/pod/show/bitcoinbrink/episodes/Sebastian-Falbesoner-on-Code-Review-and-BIP324-e2909ue'
date: '2023-09-06'
tags:
  - 'libsecp256k1'
  - 'generic-signmessage'
  - 'v2-p2p-transport'
  - 'bitcoin-core'
speakers:
  - 'Sebastian Falbesoner'
  - 'Mike Schmidt'
summary: 'Sebastian Falbesoner (theStack) and Mike Schmidt talk about Bitcoin Core code review, BIP324, and Sebastian''s plans for the next year.'
additional_resources:
  - title: Sebastian's plans for the next year
    url: https://brink.dev/blog/2023/06/20/bip324/
  - title: https://brink.dev/
    url: https://brink.dev/
---
## Sebastian's journey to Bitcoin development

Mike Schmidt: 00:00:00

I'm sitting down with the stack Sebastian Falbesoner.
Did I pronounce that right?

Sebastian Falbesoner: 00:00:06

Yes, perfect.

Mike Schmidt: 00:00:08

All right.
We're going talk a little bit about his grant renewal what he's been working on in the past and what he plans to work on in the future.
So we've awarded Sebastian a year-long grant renewal through Brink.
Brink is a not-for-profit whose purpose is to support Bitcoin developers and that includes also funding them through our grants program of which Sebastian has been a grantee of Brink for the last two years and this will be his third year now.
We fund remote grantees and we also have an office in London where we fund folks and we acquire visas for them to be able to work together in our London office.
Sebastian is one of our remote grantees and he's also a little bit different in that he is a part-time grantee.
We can get into that potentially in one of our future questions.
But well, first of all, congratulations, Sebastian.
I think by everyone's account, your work is stellar.
The grant committee agreed.
Some of the developers that we talked to on the project, really value your feedback and your review.
So we're honored that you want to continue to be a Brinkie.

Sebastian Falbesoner: 00:01:23

Yeah, thanks.
Very happy to be a Brinkie for another year.
It's been an exciting journey so far.

Mike Schmidt: 00:01:30

Well, let's talk a little bit about that journey.
You've been a grantee for two years, this will be your third as we discussed.
What's your development journey been like so far?

Sebastian Falbesoner: 00:01:41

I will start before Brink because everyone has to make some contributions first, right, to get into some grants.
So I think my very first time that I actually wanted to do something on the Bitcoin source code and contributing was in summer 2019.
I visited one year before the Baltic Honeybadger, that is a conference in, I think it's Latvia, and there was very inspiring talks.
There was one by Justin Moon about a Biddle bootcamp, where he like motivated people to contribute to Bitcoin Core.
And with that I thought, okay, let's do that.
And yeah, then was summer 2019.
I started with my first pull requests.
The very first thing I did was just grepping for to-do in capital letters, just to see what is there.
At first, of course, getting familiar with the build environment, running the tests and everything.
Then the first PR got approved, you dig more and more into the code and it became more fun over the time.
And at that time, you probably remember there was this pandemic shortly after.
So I had a lot of time beginning of 2020.
We'll also talk about that, but I mostly got into the test framework where I contributed the most.
And at that time, I also applied for the Chaincode residency.
I had a talk with Jonas and John Newbery, which I first saw there.
I think he was the one being responsible for checking my submission.
There was some task you had to fulfill.
But that residency was cancelled, of course, because of COVID.
So that was a bit sad, but I just continued to contribute.
And then fast forward, spring 2021, John Newbery had a call with me.
He just wanted to check up on me and he asked me if I would be interested to become funded by Brink basically.
And there we are.

Mike Schmidt: 00:03:54

It's that initial discussion that do a part-time grant and I think at the time we were doing a half year, and now we're up to doing full year grants with you.

## Thoughts on contributing to Bitcoin Core in a remote, part time capacity

Mike Schmidt: 00:04:05

But it still is part time for you.
And so I'm curious about how you think about that.
There may be other folks who are poking around the code base, maybe contributing here and there, and maybe would entertain being a full-time developer, but maybe would also be curious about how one could be a part-time developer.
So maybe for a time situation, how do you find that that works?

Sebastian Falbesoner: 00:04:32

For me personally, it works quite well.
Of course, it depends on your personal circumstances, how much energy and effort the other job takes.
In my case, I can easily fulfill both and they're different enough that they're both fun.
So as a small background, the other job, I'm working as an embedded systems engineer.
So I'm basically responsible for crafting together embedded Linux distribution.
And that involves also tinkering with hardware and I also like that.
I still have to go to shift long term full time into Bitcoin core development.
I think what stops me is that I'm not the type of personality who would enjoy 100% remote work.
So either I move to London to join the other Brinkies to the office or what would be my wish that there would be other contributors in Vienna where I live that do have some spaces there.
It would be nice to have one or two people to hang out at an office to discuss ideas.
So that is for me the main reason basically that I still want to go into some office have real talk.
I mean there is ideas that you're going to shared offices, but yeah, I would love to work with people together physically on the same project.
Yeah.

Mike Schmidt: 00:05:55

Yeah, that was something we heard from other grantees previously, which is why we have a London office and try to get people there if they want to participate in person.
Obviously, there's more and more Bitcoin developers every day, but in terms of folks who are really experts, there's not many of them and they're scattered amongst the globe.
And so to be able to have an in-person way to collaborate with people.
I know when I've been in the London office and visited, there's a lot of just kind of kismet or things that somebody is working on that even if they're on a different part of the code base they can have a question for somebody and there's some good collaboration that goes on there and so we're happy to facilitate that if you can drum up the local community otherwise maybe you're remote for an hour we can convince you to come and stuff.
You mentioned you sort of got into building the Bitcoin core code base and grepping for to-dos that could be something to work on.
And as part of that, getting familiar with the Bitcoin software, you mentioned running the test suite.
And I know you over the last year or so have been increasing test coverage and improving the test framework.
So I guess maybe first we can, for the audience, maybe just provide an overview.

## What is the Bitcoin Core test framework?

Mike Schmidt: 00:07:27

What is the test framework?
And second, what was wrong with it that you had to spend time improving it?

Sebastian Falbesoner: 00:07:34

Yeah, as a side note, also in addition to grepping for to-dos, there was a thing like labels "good first issue" back then and many of them were also test related.
There are not that many now, maybe that would also be a nice thing if contributors, maintainers could think more about what kind of issues would bear to attract new talent.
To the question of test frameworks.
So what we have is basically a framework where we spin up several Bitcoin core nodes that can communicate to each other for the sake of running tests.
So this is written in Python like an interpreter language which is kind of a nice choice for that.
And basically we have our own small client implementation, the test node, and those are running on  regtest, that means they're not on the real Bitcoin network, of course.
What we mostly do there is basically we do the things that a user would do, running RPC calls, checking that the results are what is expected.
As a developer, I think of the functional test as a documentation even.
Whenever I look for something that I'm not familiar with, I first look at the functional tests because those tests are run basically daily, several times on the continuous integration.
So it is kind of a truth what happens there.
And to your question, what was wrong with the test framework?
I wouldn't say there was anything substantially wrong, but there is always things to improve in terms of abstraction.
For example, when I started many of the tests, they needed to create output scripts, like for target addresses where you send the coins to.
And in order to do that, they would just manually push together the bare opcode of pay-to-public-key hash scripts and so on.
So one of my PRs was to just create some helpers that you just say p2 bkh script and you pass the public key and the test reader then doesn't have to bother with these bare op scripts, which is maybe interesting but not in the context of a test that does something completely unrelated.
It's more like making the life of the test writer and also the reader, not having to care about all those unnecessary churn easier.
Another example is the mini wallet.
So we have our own small wallet implementation in the test framework and there was a huge issue for letting the functional tests use that in order to not depend on Bitcoin Core's wallet anymore, because the long-term goal is to split those apart, so the wallet should be a separate process.
Right now, everything is entangled in one huge binary.
I think Russ Yanofsky has a PR open for the separation of that.
Most of the work I did was mostly to get the tests on point that they don't include stuff that are not supposed to test.

Mike Schmidt: 00:10:59

I can echo your sentiment about the test framework being a good, approachable way to start interacting with the Bitcoin Core code base in that, for myself personally, we put together the Bitcoin Optech workshop that was doing Taproot before Taproot was activated.
So there's a modified Bitcoin core instance.
We built the workshop that we did for Taproot using the test framework.
And I think, yes, it's much more approachable to start interacting and doing things when you can spin up some nodes and start mining and sending bitcoins around.

Sebastian Falbesoner: 00:11:44

And that gives you a good understanding what's actually happens, right?
You start from zero and then you have to think about, okay, what do I have to do to get some coins?
Obviously I have to mine some first and yeah, it is.
Everyone that is really new to the code base, I would recommend to look at the functional tests.
There is also many low-hanging fruits, I think, still in the code base of code that is not tested yet.
So there are always pull requests welcome of increasing test coverage, which I also did quite a lot.

## From testing to PR authorship (and Bitcoin Core #25957)

Mike Schmidt: 00:12:15

If we were flipping from testing and some of the review side of things to actually offering new code, there was one PR that you authored, which recently made its way into version Bitcoin Core 25.0, which is PR 25957.
And it has the title of fast rescan with BIP157 block filters for descriptor wallets.
Maybe you can talk a little bit about, maybe also how you even came into that realm of code from the test framework and why you decided that that PR was important and why it was needed.

Sebastian Falbesoner: 00:12:58

Yeah, sure.
So that was also an interesting task for me because, I was actually surprised that this wasn't done before because it's an obvious idea and I think there was a PR before from Marco Falker like three years earlier but the time back then was different, the descriptor wallets were not as widespread yet, it was a little more difficult to figure out what `scriptPubKey`s a wallet has.
I actually did some wallet work before, more like small refactorings, and in the course of test writing I also learned a bit how an actual wallet would work.
And the idea of the PR is quite simple, so basically now when you restore a backup, for example from your seed words, not in Bitcoin Core.
Bitcoin Core doesn't support seed words, but let's say you just restore a backup, then the first thing the wallet has to do is look up all the funds from the past, like everything that you received in the past or you sent because you want to see your full balance, right?
So even if something happened deeply in the past and you want to have the transaction history again.
And in order to do that, what the wallet has to do, it really has to inspect every single transaction of every block and from each of those transactions, every input, every output, and it goes through that list and basically checks always, is this spent output or is this received output relevant for me?
Yes, no.
And this is of course quite time consuming and there is this nice thing called block filters which basically let you easily answer the question, is this block relevant for me in terms of a given set of output scripts.
So you create your filter sets, like that is the collection of all the scripts that you're interested in.
And then there is a matching function with that block filter and it can tell you easily if there is at least one of the relevant scripts in that block.
And what we do in, what I did in the PR is we take use of those block filters if they're available because we don't create them by default.
You have to pass an extra option to that.
Block filter index equals one.
And if they're available and if we use the descriptor wallets, then those are used to significantly speed up the scanning process.
It's around an order of magnitude faster to my experiments that I did.
Of course it depends heavily how many output scripts you have and so on, but it should usually give you easily a 10x speed increase which is quite nice I think.

Mike Schmidt: 00:15:50

Yeah that's great.
I think folks may be familiar with BIP157 in terms of like light client usage for for querying for relevant transactions but it sounds like you've also used the similar block filter functionality just internally, you're not querying another node, right?
You're querying your own node.

Sebastian Falbesoner: 00:16:12

Yeah, exactly.
So we just use them if they're created locally.
If that option is turned on, they're just really created on the go, whenever a new block comes in or on the initial block download, so that the index is created.
And another thing which uses that is the `scanblocks` RPC by James O'Beirne.
I'm always not sure how to pronounce his last name.
I think that one came in one release earlier, if I'm not mistaken, 24.
That is an RPC call though, and also, you can pass a set of output scripts that you're interested in and it would just return you all the blocks that are matching.
So it's kind of nice that we can use that to make the the life of users easier, hopefully.

## The scarcity and importance of code review

Mike Schmidt: 00:17:05

One thing that I got feedback on about your work is from a prominent Bitcoin Core dev who said, quote, "theStack's review matters."
theStack's review is valuable, something along those lines.
And so I think you've done quite a bit of review and maybe you can comment on that in the context of how do you think about how much time you spend authoring new code and PRs versus review?
And why do you think that this person said that your review counts?

Sebastian Falbesoner: 00:17:47

To your first question, I think the review time I spend is more than authoring time.
I would even love to spend more time reviewing, because I think it's the resource that is most missing in Bitcoin Core actually.
Like it would be great if we have more review power.
And yeah, according to what person's reviews counts, I think it's also kind of a proof of work system in Bitcoin Core.
Not specifically regarding me, but in general, if you over the time give review comments that are helpful or are considered helpful by others, then of course you're getting taken more seriously.
I think my review style has been also inspired by other people from the top of my head.
I could name Russ Yanofsky who give very great detailed review comments and that's inspired someone, right?
To be detailed and whenever testing some PR like really thinking what could go wrong.
How could I trigger some code path that is not intended or something like that.
The nice thing about reviewing is that you can do it offline.
Like for example, recently for a BIP324 PR, that one was about the test framework.
I basically printed out the code and read it being in the pool.

Mike Schmidt: 00:19:22

Wow.

Sebastian Falbesoner: 00:19:23

Not in the pool, but outside.
And I think it's sometimes good to be focused, to not even have the computer on and just, that obviously works more better with conceptual review, like for BIPs or just fresh code, if you have a PR that changes like 10 different files, then that is not a way to go, but very often, I also do more and more offline review with pen and paper, which may sound odd or old school, but for me it works.

Mike Schmidt: 00:19:57

You mentioned you personally are inspired by seeing valuable in-depth detailed feedback.
But I suppose in order for you to give that sort of feedback, you do need to have done that proof of work, which is being able to understand what is being changed or added, and also the context in which it's being changed or added.
And so when you see something or a project or even just a single PR that maybe you're somewhat familiar with but not in depth, like how do you approach that trying to figure out where you can add value in terms of review?
Like how do you think about that?
And I'm just thinking in the context of somebody else who's doing review now and maybe they think they're doing good review and maybe there's room for improvement in some manner, trying to get an insight into what you're doing.

Sebastian Falbesoner: 00:21:01

Do you mean like how to prioritize what to review, how to best use the resources or how to dive into a topic that you're not as familiar in order to?

Mike Schmidt: 00:21:13

Yeah, I guess maybe a combination thereof.
A topic that you're maybe familiar with you want to provide insightful feedback but in order to do that you need to acquire the knowledge to even know what is valuable feedback.
Is it really just a matter of spending the time and doing the work and jumping into the intricacies of the proposed changes and its potential effects?
Do you spend a lot of time doing that before you even write a word of review or do you sort of take a different approach to it?

Sebastian Falbesoner: 00:21:47

Yeah, it always depends on what kind of review it is.
There are these small things called nits where you just propose to change code styles and stuff which are often frowned upon because those are not like affecting like the deep logic of PR.
But what I definitely do is first check out the PR locally, play around with it, maybe try to break it.
I think when you work a little bit for PR, then you for some time, then it's easier to give valuable feedback compared to if you just look at it online on GitHub maybe.
Actually using it, try to do something useful with it, or even sometimes try to do something that is not intended with it, just to see what could go wrong in the worst case.
And yeah, but I guess everyone has a very individual review style.

## Benefits of BIP324, Version 2 P2P Encrypted Transport Protocol

Mike Schmidt: 00:22:47

Maybe we can use this as an opportunity, this sort of, I've given you kind of a general hypothetical of how you approach review, but one thing that you're looking forward to doing now and looking forward to doing more in the coming years, reviewing BIP324 and the associated code changes with that.
And maybe just maybe just to set the stage before we jump into it.
So currently, all data relayed on the Bitcoin peer-to-peer network is public and peers talk to each other over unencrypted connections and BIP324, its purpose is to solve that potential issue with the ability to have encrypted connections to your peers.
I think everybody would prefer encrypted communication over unencrypted, but maybe you can get into why in the Bitcoin network, what sorts of vulnerabilities or attacks are available as a result of not speaking to each other in unencrypted connection.

Sebastian Falbesoner: 00:23:56

Yeah, intuitively when I talk about this with like friends or people, they say, okay, but it's a permissionless network anyway.
Why do we even want to encrypt this if the transaction end up in a publicly available block anyways right and but it's here it's more about the metadata like even if you transact something then maybe just by watching the traffic, it could be inferred that you're the originator of a transaction, for example.
So it's more about even hiding metadata rather than the public data itself.
And right now, for example, it's trivial for ISPs to just detect also that you run a Bitcoin node, because all the packets, they start with the same network magic.
And therefore, it's just easy to passively detect that you run that.
And the packages can also be tampered with.
So what ISPs could also do, they could selectively just censor single transactions if they wanted to.
And with the BIP324 we can even hide the fact that we run a Bitcoin node from the beginning, which is very nice, I think.

Mike Schmidt: 00:25:15

So right now I think the default is 8333, the port, but I do think there is the ability to change what port you're communicating on and then also...

Sebastian Falbesoner: 00:25:25

Yes, exactly.
Because if that wouldn't change, then we don't gain something in that respect, right?
If everyone runs v2-p2p encryption but would still be on port 8333, then it would still be trivial to figure that out.
But I think that there's also been some changes recently on the network layer that there is no strong preference to connect to 8333 port peers anymore.
And yeah, what I really found fascinating is this approach of we want to have everything random from the very beginning because there was an earlier proposal by Jonas Schnelli, BIP-151, and with that one you would start out as a v1-p2p encryption and then upgrade so you could negotiate for an encrypted connection.
But BIP324 really goes one step further and everything looks random on the wire from the start.

Mike Schmidt: 00:26:26

So even the initial reaching out to a new peer.
There's nothing that says, hey, I want to talk Bitcoin with you that is visible to an eavesdropper.

Sebastian Falbesoner: 00:26:42

No, it's not.
So the very first things that are sent are really, in fact, the public keys to each other for the Diffie-Hellman key exchange.
So they could both agree on a encryption key or rather set on encryption keys.
And for that, a new scheme of encoding public keys used.
This is this Alligator Swift, where Peter Wille, Tim Ruffing, I think did a great work, they basically took the idea from a paper from other researchers and put it in a way in the `libsecp` library to make it available for us.
And that PR just got merged a few days ago.
So we see some nice progress there.

Mike Schmidt: 00:27:32

You can't even see that initial public key exchange, that initial key exchange is obfuscated in a way that...
So what ways are there then, if you're an eavesdropper on this connection to...
Is there the frequency of the transmission of information or is there anything that they can key off of?

Sebastian Falbesoner: 00:27:56

Yeah, what they can always do is still connect to you And because it's still an open permissionless network, so we cannot stop anyone from connecting to us really.
But it just raises the costs to do attacks.
And they could still do man-in-the-middle attacks, of course.
But even for that, something nice is included in the BIP324, where you have like a session ID that each one of the participants can see locally and they could compare it off-band to find out if they have been man-in-the-middle attacked.

Mike Schmidt: 00:28:33

Interesting, so you can share that session key outside of the Bitcoin peer-to-peer network communication to ensure that there's not somebody in between.
Essentially repackaging everything.

Sebastian Falbesoner: 00:28:46

Yeah, there is some RPC call, or I think it's an existing RPC call get peer info and for all the v2-p2p connections they would just use, they would just show another field called session ID and this ID you can compare to your other node if you wanted to and if those match then you're sure that there is no one.
Then you haven't been man-in-the-middle attacked.

## Sebastian's approach to contributing to BIP324 and libsecp256k1

Mike Schmidt: 00:29:12

So I want to take a quick diversion and hearken back to what I was giving you in a generic example of earlier, which is how do you approach a project or a change to the code and figure out how you can add value both as a reviewer and a contributor.
Maybe we can apply that to this particular project that you have an interest in and are contributing to.
And so you see BIP324 and maybe you follow along at a high level as a Bitcoin developer for a BIP, but then you decide you want to jump in and contribute.
So this is a somewhat complicated project, I'd assume.
So how do you even think about getting started to understand what is going on and figure out how you can provide value there from a reviewer or a contributor side of things?

Sebastian Falbesoner: 00:29:59

Yeah, it's an iterative process.
The very first thing I would always read is the BIP of course.
In this case it's very nicely written in a generic way first but then later it gets very detailed with all the cryptography stuff which is kind of scary.
But the good thing is when I started there were already some PRs available.
For example, there was a Python implementation of BIP324 basically from Stratospher, which is another Bitcoin Core contributor interested in reviewing BIP324.
So it's a little reading BIP, a little reading available PRs already and figuring out what they do.
Then there is also podcast material.
I remember I listened to the Stefan Livera podcast.
He had an episode where he invited the Dhruv, Peter Wille and Tim Ruffing, where they explained the thing.
And then you get more and more, you hear more about that topic.
And also of course Bitcoin Core meetings.
It was my first Bitcoin Core meeting last year in Atlanta, where these people's also presented.
And yeah, and at some point you would just pick some PRs and try to understand them deeper.

Mike Schmidt: 00:31:26

So maybe let's jump into that.
So what did you pick up first?
You familiarize yourself with the topic by reading the BIP and maybe looking at some sample Python code and then where did you decide you wanted to sink your teeth into and actually start contributing to the project?

Sebastian Falbesoner: 00:31:46

What I first did back then still Dhruv was maintaining the PRs.
So I just first built the main PR that includes all the sub-PRs and ran a node just to also have something available already and playing a bit around what the end product would look like and then iteratively I would look at those sub-PRs and no, I didn't look at the `libsecp` parts until recently.
It always was appeared very scary for me all those cryptography and math stuff but I also ended up doing a little review there.
I was lucky enough to join a hangout at the last CoreDev meeting in Ireland where Peter gave an introduction to the `libsecp` library and he specifically presented the PR1129, which is the ElligatorSwift part.
So I got a little deeper into that through that.

Mike Schmidt: 00:32:48

And you've been now dabbling in `libsecp`?
Maybe just a quick overview of what is `libsecp` other than a little bit intimidating and then...

Sebastian Falbesoner: 00:32:59

Yeah.
So, what every transactions basically consists of to show proof that the one spending a transaction owns the private key of the address where the funds have been sent to, it includes a digital signature.
And for that digital signature, we have our own library called `libsecp256K1`.
It is named after the curve that has been chosen back then by Satoshi to represent those digital signatures.
Earlier it was initially OpenSSL has been used but that has been replaced because that had some problems with the malleability like the same signature could be represented by different encodings and also it wasn't very performant, so at some point I think it was Peter Wuille, he came up with the idea to write their own library, `libsecp256K1`.
And yeah, that's what we use nowadays.

Mike Schmidt: 00:34:12

It also eliminates the dependency as well.

Sebastian Falbesoner: 00:34:15

Excuse me?

Mike Schmidt: 00:34:17

It also eliminates the dependency on an external library.

Sebastian Falbesoner: 00:34:22

Yeah, sure, yeah.
Which is also something that Bitcoin Core always is happy if we can keep the dependencies low, yes.

Mike Schmidt: 00:34:31

So how are you contributing to `libsecp` now?
You got a little bit more familiarity with it.
You gave us an overview of what it is.

Sebastian Falbesoner: 00:34:38

Yeah, so it is a project completely written in C, in the C language.
I think even still sticking to the C89 standard, which is probably widely supported on a huge range of platforms, including small microcontrollers.
And what it basically includes are functions to just create and verify digital signatures.
A large part of the most recent softfork, the Taproot and the Schnorr signatures, that last part, the Schnorr signatures that has also been implemented in `libsecp`, of course.
And yeah, it's a different world than Bitcoin Core.
It's so much more low-level.
Like every math operation is basically a single function called.
And yeah, what I contributed was mostly I opened a couple of PRs for improving documentation for the API, some refactoring, and lately also some tiny performance optimization.
There were some calls where some function calls were called that were not needed to be called, so they could be removed.
So I was a bit overexcited at first.
I ran a benchmark, and it showed a 3% increase.
But it turned out it was just unstable on my PC.
So the increase is not that noticeable, but that's still fine.
It saves a few instructions.
It got 1x so far, I think, so maybe it gets merged soon.
And I think it's good to also have more review power in `libsecp`.
So my plan would be to also stay there.
I'm still going in baby steps.
And another thing is I realized I looked at the silent payments, which is another nice idea, and that takes also quite intense use of cryptography.
So I thought, okay, if I want to really give good review, it may make sense to get a little deeper in the `libsecp` to at least conceptually understand what's going on behind the scenes.

Mike Schmidt: 00:36:52

It's interesting to kind of walk through and talk through this journey from your initial to do grepping into now these big projects and these big important pieces and trying to contribute to those and review those as well.
I feel like we got a great overview of your journey.

## BIP322 generic signmessage

Mike Schmidt: 00:37:15

Another thing I wanted to bring up is another project that you were looking at which is BIP322.
Oh Generic sign message which allows wallet to sign or partially sign a message for any script which they can conceivably spend.
And so that means a signed message can produce a signed message for any script or address that a wallet can potentially be able to spend.
And I think right now only P2PKH addresses are supported in Bitcoin Core for message signing.
And so maybe you can talk a little bit about this BIP and this project and what's the latest progress or not progress with that?

Sebastian Falbesoner: 00:37:58

Yes, yeah as you said we currently only support signing messages for legacy output scripts, like legacy addresses starting with a one.
And so that it's not that useful anymore, like in the year 2023, where at least most people right now use at least SegWit addresses.
So it would be very nice to have some generic format for signing messages.
I found the idea nice, very nice also how the BIP is specified, like the signature would basically have the structure of a transaction basically for easier interoperability.
And I would find it very useful.
I reviewed it also last year, and I think the code is not that complicated in the end.
But unfortunately, it didn't get much traction.
I think there wasn't much activity for the last few months at least, so it would be nice to revive that.
And I had the idea to maybe give a review club session for that to attract more people to take a look at it.

Mike Schmidt: 00:39:20

That would be code is in I mean is it in it just needs to be reviewed and after doesn't need significant amount of...

Sebastian Falbesoner: 00:39:38

The code is basically fine I didn't see any huge problems or blockers.
I was basically already giving an edge and there was only some nits left, which are also fine if they're not addressed.
So, but of course it would be definitely good to have more eyes on it.

Mike Schmidt: 00:39:51

People may be familiar with `signmessage`.
I think there's been some Twitter chatter about old addresses signing messages saying that certain people are not Satoshi or they don't own these coins because this other person is signing a message proving that they have access to that private key and they control those coins.
But what are some of the other use cases for `signmessage`?

Sebastian Falbesoner: 00:40:20

I don't know what private people use it for, but what it is, it's sometimes used by exchanges, I think, that they want to have a proof before you send funds to somewhere to actually prove to them that you actually own the private key corresponding to an address which depends on how you look at it it could be seen as the customers are protected.
On the other thing, I think there was a bit of backlash because with this travel rule thing, I think there was even some discussion to completely remove it in order to avoid that.
There was an issue opened recently on the Bitcoin Core repo to completely remove it.
And I think that was motivated out of, I'm not familiar with the concrete thing, but I think there was some opinions like this could be used to implement the travel rule or something like that.
It felt a bit rushed to me to just remove a call that usually seems useful just out of fear that this could be used in the wrong way?

Mike Schmidt: 00:41:38

I know some exchanges have looked at this type of functionality in order to facilitate proof of reserve type systems.
Yes,

Sebastian Falbesoner: 00:41:48

Yeah, awesome.

Mike Schmidt: 00:41:50

Also, some folks are looking into this who are identity people, and so somehow using the address as an identifier and the signed message as some sort of a way to authenticate that identity.
I don't know all the details there, but I know there's some folks looking into each of those types of use cases as well.

Sebastian Falbesoner: 00:42:14

Yeah.

Mike Schmidt: 00:42:16

All right, Sebastian, we got sort of a whirlwind of your progress and what you're looking to work on this coming year.
Is there anything else that you think listeners could find interesting about what you're working on or anything about being a Bitcoin developer?

Sebastian Falbesoner: 00:42:34

I would encourage everyone who is interested in that to just start digging into the codes, don't be shy, ask contributors.
I think everyone is more than willing to help and yeah if the time comes and you contributed enough, don't also be shy to apply for a grant, for example, at Brink.
Meeting people is also important, going to events and I enjoyed also the Coredev meetings and yeah, thanks also to Brink for the support of course and more excited than ever for the journey what the future brings.

Mike Schmidt: 00:43:24

Well I know that we're excited to renew you for another year.
Congratulations on all your progress.
We're looking forward to the next year of even more progress and some of these important projects that you talked about, getting them across the finish line.
I think it's great to be able to support somebody like you who's contributing in this way.
Thank you, Sebastian.

Sebastian Falbesoner: 00:43:47

Thanks as well.
