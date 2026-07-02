---
title: 'Upgrading Bitcoin''s Consensus Engine: Bitcoin Kernel Explained w/ Core Dev'
transcript_by: 'bartoli via review.btctranscripts.com'
media: 'https://youtu.be/HDJqsL-f9DA?si=18ZW4fdnojMHEj5Y'
date: '2026-02-04'
tags:
  - 'bitcoin-core'
  - 'libbitcoinkernel'
  - 'multiprocess'
  - 'security'
  - 'refactoring'
speakers:
  - 'Sedited'
  - 'Shinobi'
categories:
  - 'podcast'
source_file: 'https://youtu.be/HDJqsL-f9DA?si=18ZW4fdnojMHEj5Y'
summary: 'Shinobi (Bitcoin Magazine) interviews Sedited, a Bitcoin Core developer, about libbitcoinkernel — successor to the abandoned libconsensus library — which extracts Bitcoin''s stateful consensus validation logic (block headers, UTXO database, script verification) into a modular library enabling alternative node implementations to build on Core''s proven consensus code directly. Sedited explains why libconsensus failed (limited to script verification, unable to surface the stateful UTXO and disk logic without excessive workarounds), how kernel cleanly demarcates validation from wallet and GUI code to improve review safety, argues that kernel reduces rather than centralizes Core''s influence by lowering the barrier for competing implementations (citing Floresta, an ARK test framework, and several full-node projects already integrating it), and closes with the hope that kernel''s granular per-function validation interfaces could eventually serve as the foundation for a formal Bitcoin protocol specification.'
---

## Why Bitcoin Consensus Isolation Matters

Speaker 0: 00:00:07

Hello everybody, I am Shinobi, technical editor at Bitcoin Magazine, joined by Sedited, a Bitcoin core developer contributing to the Kernel Project.
So Sedited, There's a little bit of a long tangled history to the kernel project.
Years ago, there was the lib consensus project.
So, attempting to actually take all of the consensus rules and move them to a totally external library that could just be called, used independently on its own, like any other software library.
And that project kind of got sunsetted in favor of the kernel project, which as opposed to trying to become a full library, is looking at just isolating kind of the consensus logic in the Bitcoin daemon so that you can call it independently or like granularly bit by bit from that program running rather than having to go through the whole validation flow as it's implemented in core.
You kind of want to talk a little bit about why all the effort switched from the lib consensus project to kernel and kind of the logic and the reasoning for that?

Speaker 1: 00:01:26

Yeah, sure.
So when it started out, the initial goal was to just isolate a very small subset of the entire consensus logic.
Specifically, it was only the script interpreter that was surfaced through the original consensus library.
And some projects did integrate this, but the traction it got was pretty limited.
And this had a multitude of reasons, but I think the main one was that it just didn't give enough leverage to the programmers using the library and its feature set was also pretty limited.
The main problem with expanding the scope of the original library was that the code within Bitcoin Core just wasn't suitable for that at the time.
So because everything was so very tightly coupled with completely unrelated functionality like the GUI or the wallet, was basically impossible to surface more validation logic that just did one thing at a time.
And yeah, it just took a lot of time since that original libbitcoin consensus release to get the internal code into a state where we can now finally add a bit more, let's say, flexibility for the developers using the library and features beyond just verifying scripts.
And you were specifically asking before where the cut between Libbitcon consensus and the new Libbitcon kernel happens.
And The main difference there is that the libbitcoin kernel functions are stateful, so they maintain system resources that are allocated on the hardware itself.
It has all the database functionality that a typical Bitcoin node would have.
And surfacing all of that through the original Bitcoin consensus architecture was basically impossible.
And yeah, that's why the step had to be taken to deprecate it.

Speaker 0: 00:04:24

So it's just, you know, because consensus entangles so many things outside of script, it's just like unpredictability in terms of how trying to apply that library interacting with alternate implementations of consensus critical things like the UTXO set or a block database, like that kind of issue.
You can isolate the script rules, but you can't actually guarantee that the rest of everything that needs to be touched in the consensus process will behave properly.

## Why "libconsensus" Failed

Speaker 1: 00:04:58

Yeah, exactly.
So I guess it would have theoretically worked if you would have been very, very careful to patch out all the unrelated functionality with stub functions that you manually copy in.
But once you're doing that, yeah, it's too much of a hassle to release, right?
You could just take the current code wholesale, if that's what you're doing anyway.
So yeah.

Speaker 0: 00:05:32

At that point, you're not achieving the goal of having a known, consistent, reproducible consensus rule set or implementation.
Exactly.

Speaker 1: 00:05:43

The entire point is that you don't have to artisanally interfere with the code every time you want to just verify a block, right?
We just want to give this one function that does the logic correctly and everybody can just call it in exactly the same way and get a reproducible result.

Speaker 0: 00:06:04

So what was kind of the original impetus for LibConsensus and now the Kernel project?
I mean, Bitcoin Core is unquestionably the dominant client on the network.
Like any serious miner is either running core or running something very tightly related to core in terms of custom behavior or code-based changes.
All the major businesses, exchanges are running Core.
Like why put so much time and effort into trying to strip out and isolate the consensus rules so they can be used somewhere else, as opposed to just continuing to focus on core as an implementation?

Speaker 1: 00:06:48

Yeah, so I think initially the impetus was purely on a philosophical level where we don't just want Bitcoin core to dictate everything to the entire ecosystem and kind of prohibit other node implementations from ever receiving the same trust level just because they kind of gatekeep the validation logic.
But even beyond that, the kernel has significant benefits to the project because it really clearly demarcates what actually is validation code and what isn't.
And yeah, making things nice to use from the outside will automatically also make it nicer to use for our own codes and allow us to also experiment more freely with it, write our own tools and utilities with it.
Yeah, so it gives us a whole lot more flexibility and also confidence with reading the codes and doing reviews of sometimes pretty complex validation changes.

## Kernel vs Multi-Process Bitcoin Core

Speaker 0: 00:08:03

So how has implemented kernel impacted or affected the work towards multi-process separation?
Like, that's something for a similarly long time, Core as a project has kind of been trying to clean up the codebase so that things are nicely isolated, could potentially in future actually be separated into completely separate programs that talk to each other as opposed to one singular codebase.
But it's been a long road, I think a lot longer than LibConsensus and the Kernel project, going from the giant file that Satoshi left everybody to like the much more modular, clean code base that we have today.

Speaker 1: 00:08:54

Yeah, definitely.
I would say the time spent on either, Probably more time was spent on the multiprocess project cumulatively so far.
Initially, the efforts that went into separating the code for multiprocess were also really useful for the kernel.
But by and large, that split is kind of done now.
There are a few areas where we definitely still need to separate a bit more cleanly.
For example, for the indexing code.
But that doesn't really directly affect the kernel anymore.
So the kernel is already like one subcomponent of the innermost multiprocess binary, or like the Bitcoin nodes multiprocess binary.
And most of the organization that takes place now in the kernel project is within that Bitcoin nodes multiprocess program already.
So There's not really much of a symbiosis between the two.
They're just on separate tracks and don't really interfere with each other.

Speaker 0: 00:10:09

Just kind of a little work overlap, I guess, in the early phases of Kernel.
I think the original goal of libconsensus, of Kernel Project, was to enable other implementations to just take core's consensus logic and then build out all the rest of an implementation themselves, knowing that the core thing that matters is going to be interoperable with the rest of the network.
Practically speaking, how far from that stage is development for the project.
Do you think that would be a safe thing to do now, or is there still some more groundwork to be laid before we're really at that point?

## Can Developers Build Full Nodes With the Kernel Today?

Speaker 1: 00:10:56

I think it's a fairly safe thing to do now.
We are at the point where there's, I think, two or three projects which are now trying to build out a complete full node around the kernel library.
My main hesitation still with that is the split and the interfaces for that are still pretty immature.
Like we probably want to wait a few more release cycles before we say, okay, we now officially release this.
It has been used successfully by, I don't know, maybe 10, 20 other projects.
No major bugs have been reported in like half a year.
Because obviously we really can't mess this up once it hits production.
So yeah, we definitely have to be very careful with that.
So most recently, I think two weeks ago, Floresta, one of the Utreexo implementations, integrated the kernel or this upset of the kernel library.

Speaker 0: 00:12:00

Yeah, that's the Project Vinteum's funding in Brazil, right?

Speaker 1: 00:12:05

Yeah.
So they're running it now which is pretty cool and they've also committed to working with us a bit and giving good feedback And we also try to upstream changes that we're planning to roll out to Bitcoin Core soon to them.
So yeah, that's been a good symbiosis.

## Real-World Kernel Adoption Outside Bitcoin Core

Speaker 0: 00:12:26

Hey, everyone, it's Shinobi.
And I'm here in front of the Chicago Fed to talk to you about the core issue of Bitcoin Magazine.
The last few years have been a bit of a communication breakdown between developers and people using Bitcoin.
Bitcoin exists to be an alternative to this institution, but to do that, it needs people to actively maintain it.
If you actually want to hear from developers themselves, how they approach their work and what they choose to work on.
Go to BitcoinMagazine.com and get yourself a copy of the core issue.
All right.
Alright, now I guess we should probably try to keep this higher level.
But I guess for some of the curious viewers out there, you think you can walk through the different validation steps that were in the code base and isolated in the kernel now.
And maybe kind of talk a little bit about which of those was maybe the toughest to kind of isolate or was sprawled the most across different sections of the codebase.

Speaker 1: 00:14:01

Yeah, I can try to do that.

## How Bitcoin Kernel Validates Blocks

Speaker 1: 00:14:03

So on a high level, you get a block from the network and then you pass that to various functions in the kernel library.
And Those functions then validate the block header.
So check the proof of work, check the timestamp, the previous block, that the Merkle root is actually calculated correctly with all the transactions in the block.
And yeah, once that is done, it commits it to disk or writes it to disk router.
And once that is done, it validates all the transactions and all the scripts from the transaction.
So it checks the signatures of every single spent output in the transaction.
So yeah, that's basically like the high level overview of what the logic actually does.
In terms of what was most challenging was probably the step between writing a block to disk and doing the actual validation.
There were like a couple of callback hooks back into the GUI and some extra functions that called out to the wallet unnecessarily.
It's not really too complicated stuff that I had to deal with personally, but also I have to say at that point that when I took the project over three years ago now, it already was in a fairly mature state and that preceded all the multi-process work before it that cleaned that up.
Some of the work that Cory Fields did on the old LibBitcoin consensus originally, some of the work that Coldong did.
Yeah, so it's really been this long process over probably more than a decade to get to this point.

Speaker 0: 00:15:48

Yeah, you know, it's kind of hard for me to reconcile looking at like how much work has gone into things like this in core, you know, like libconsensus, the kernel after that, multiprocess, Like all of these things that are decade long projects at this point with the explicit goal of opening the project, of making it easier for more people to do different things with it or to integrate it into something in different ways or even, you know, with Kernel itself to explicitly build something from scratch entirely around that core consensus logic that is really what matters.

## Does the Kernel Centralize Power?

Speaker 0: 00:16:32

You know, with this attitude nowadays that core developers are like some ivory tower group from above just trying to force their will on the network or retain like some position of power or influence, when the work I see is things like this, trying to do the exact opposite, like actually trying to give away some of that power and influence that they have and make it as easy as possible for other people to pick that up and actually do something with it.
What's it like working on something like this in that environment?

Speaker 1: 00:17:14

I mean, Honestly, I don't really get that criticism.
So one of the things I've heard repeatedly is that it's might actually centralize power further around call because now we're extending our control into other projects.
But I think that's even further from the truth, because the only thing that we're really establishing here is an interface and everybody can tinker with the actual validation codes as much as they want to.
And the cool thing to see over the past year of development on it was that a few people actually showed up and did exactly that.
So they only wanted this interface that they can rely on and reuse for their own projects and they ended up implementing some of the new opcodes, some weird tap script stuff.
So yeah, this is, I mean, it gives me a very good feeling and it makes me very hopeful for Bitcoin as a whole.
If we can get this project out there and just allow people to do whatever they want with it, with the confidence that they have this interface.
Yeah, they can tinker with it and probably have a bit of risk doing that, but all in all, they can build on this one and a half decades strong foundation.
So yeah, that's pretty cool.

Speaker 0: 00:18:50

That's kind of just confusing logic to me that something like kernel would give more power to core because like the underlying dynamic here is like to do something completely from scratch, like unrelated to core is the risk of consensus and compatibility.
That's only a risk because of how big Core is.
And they're the dominant implementation on the network.
Almost everybody economically relevant is running that.
And when you open the door like this to build entirely new things, knowing they're compatible with core, you're opening the door for anything to come in and compete and gain network share without that risk of a consensus split.

## Competition, Forking, and Consensus Safety

Speaker 0: 00:19:41

And at that point, if it comes down to it, if something else using the kernel were to actually, you know, gain adoption, become a majority of the network, like at that point, it's just another repository.
Like those other projects can simply fork it and do whatever they want with it.
Like, Core has no power just because they originally implemented that codebase.
Like, just click fork.
And if everybody's running some other thing built around it instead of Core itself, like, Core literally voluntarily obsoleted itself in that scenario.
I don't get the argument that that's entrenching Core more.

Speaker 1: 00:20:25

Yeah, I don't buy it either for the same reason.
One thing that I can see playing out maybe is that people will just stick with us because we have all this tradition that we're building on top of.
But I mean, as long as that is well earned and it can be switched away from easily, which it definitely can if we deploy this common interface that everybody just uses anyway.
Then yeah, this is just a pure win in my eyes.

Speaker 0: 00:21:00

Yeah, I mean it's definitely an important project.
I think to kind of go back to the lineage of libconsensus and then kernel and kind of project out to the future, you know, the next ideal step would be a formal specification.

## Could Bitcoin Ever Have a Formal Specification?

Speaker 0: 00:21:24

Like an actual like bit for bit, this is how the protocol should operate, This is how it should evaluate data.
This is the result that should be output in whatever conditions to provide the same degree of guarantee that the kernel is aiming to without any actual code dependency.
Like, that is a really sticky topic in this space in terms of the practicality of that, you know, whether that's worth the effort, whether that's something that's even potentially possible.
Like, What are your thoughts on just the issue of a formal specification for consensus rules?

Speaker 1: 00:22:07

You're definitely right that it is a sticky topic.
I think it was one of the first topics that were discussed in Bitcoin's history from the very beginning.
So we have been going a bit in circles around is it better to have a specification or is it better to just have the code be the reference?
And yeah you have to re-implement it bug for bug if you want to, and that's going to be very hard because the code is difficult to read and it's pretty complicated.
Looking out into the future, I think I would like to see a specification of Bitcoin eventually.
And I'm kind of hoping that the kernel can be a tool to make that easier so that we can break all the validation logic into separate calls to the kernel library itself and have these calls be super, super granular, where you just do a single check per validation function.
And then you just let the interface for each of that validation function.
And what it exactly does, be the specification for Bitcoin.
I think that is probably the cleanest way to achieve any kind of formal description of Bitcoin.
Just because you have this guarantee that you don't introduce a bug when you translate from the reference client to...


Speaker 0: 00:23:51

Yeah, it's really...
It would have been hard enough as just a distributed system, But with the mess that the code base was beginning, it's even worse problem to go backwards rather than having started with a spec and like move towards an implementation, which is the norm, You know, when you really look at things.

Speaker 1: 00:24:17

Yeah, but that's not what we have, right?
Yeah.

Speaker 0: 00:24:20

We have what Satoshi gave us.

Speaker 1: 00:24:22

Yes.

Speaker 0: 00:24:23

All right, well, I guess, any last thoughts on the project or your work over the last few years, you want to voice?

## The Future of Bitcoin Kernel Development

Speaker 1: 00:24:32

Yeah, I'm pretty hopeful on what it will enable for the ecosystem at large.
I was hesitant, I think a year ago or so, about the feeling that it didn't really get traction.
But now we have like three, four bigger projects, completely external to Bitcoin Core, actually using it, actually integrating it into their stacks.
Second, one of the ARK implementations now uses it in their test framework.
I can see a future where the Lightning implementations will use it to either check their scripts for their transactions or do some pre-validation that their transactions that they create actually pass the policy rules.
Yeah, there's just so much that can be built with this.
And I think just putting it out there, ensuring that it is as easy to use for developers as possible.
That's going to take a lot of work still, but I think it'll be very worthwhile.

Speaker 0: 00:25:41

I couldn't agree more.
Thanks for sitting down and talking, Sedited, and I hope you all enjoyed.

Speaker 1: 00:25:49

Thank you.
