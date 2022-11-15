---
title: Carl Dong and Build Systems - Episode 9
transcript_by: Whisper AI & PyAnnote
categories: podcast
tag: ['GUIX talk at 2019 Breaking Bitcoin about reproducible builds', 'Gitian builds', 'Fake time', 'Timestamps and reproducibility of packages', 'reproducible-builds.org SOURCE_DATE_EPOCH', 'Toolchains', 'Windows Builds and reproducibility GCC libtool pointer confusion', 'NSIS', 'Using Debian as an example', 'User choice in their security model', 'Making the process accessible', 'Mac OS X Toolchain & SDK and cross-compiling']
---

Chaincode Labs podcast: Carl Dong and Build Systems - Episode 9

SPEAKER_01: and user choice in their security model as well as user choice in the extremes of security models right I feel like there should be a spectrum of how much you trust the developers so if you manage a lot of money you perhaps want to run this reproducible build

SPEAKER_03: Hi, everyone. Welcome to the Chaincode Podcast. My name is Kara Lee.

SPEAKER_02: and I am Jonas

SPEAKER_03: I'm Merch. And Merch is our brand new co-host of episode 8 fame.

SPEAKER_02: We've already just given him the title. We're not even making him work for it. He just shows up, does his own episode, and then shows it for the next one. And that works.

SPEAKER_03: You really, really made an impression, obviously. Well, for your debut episode as a co-host, who did you guys chat with?

SPEAKER_02: We talked with Carl, and we talked a little bit about his build and tool chain work, and then we talked about his consensus engine isolation and modularization that he's doing.

SPEAKER_03: So you kept it light.

SPEAKER_02: Yeah, always always like talking to Carl.

SPEAKER_00: Yeah, we didn't even cover any details.

SPEAKER_03: Well, great. Well, we hope you enjoy our conversation with Carl.

SPEAKER_02: So, welcome to the ChainCode Podcast, Karl. Hello. You know we've been doing this podcast for a while now, how come you haven't been on the show yet?

SPEAKER_00: Hello!

SPEAKER_01: Uh, I mean, we've been at home, and this is more of a...

SPEAKER_02: We had a few episodes before that though, I don't know, I don't know.

SPEAKER_00: Alright, it's fine. It's fine. We've got you know, we'll try not to take it

SPEAKER_02: personally. Love you guys. But today we are going to talk about all things Carl Dong. Maybe start off with a little bit about what you've been doing in the in the break. What have you been doing since we haven't been in the office?

SPEAKER_01: I've been doing a lot of stuff. I've been continuing my work on reproducible builds and the build system in general. And also, I've been getting into the code base, looking at some cleanup stuff that can be done and what features they may lead to.

SPEAKER_02: All right. Let's start from the top. Tell us about reproducible builds.

SPEAKER_01: All right. So after I gave that talk last year about geeks, I've been working a lot on that. And mainly this year, it's been a lot of getting things that were barely working into things that are nicely working. We can start with some context, I guess. Well, if you download a piece of software from the Bitcoin Core website or from GitHub or whatever, it's just like an opaque blob of thing that could contain any code that we want to. Technically, bitcoincore.com can serve up a binary that just steals all your Bitcoin. So how do people know that what they downloaded is what is intended or what is in the code base or something that they have reviewed? That's where you need reproducible builds so that multiple people can run the build and see that they got the same thing and that nobody inserted something malicious into the binary. So how do they make that comparison?

SPEAKER_02: Thanks for watching!

SPEAKER_01: So they make that comparison by looking at the inputs and looking at the outputs of this process, right? So the inputs will probably be Bitcoin code base and some kind of, you know.

SPEAKER_00: release tag, right?

SPEAKER_01: Yeah, exactly. The release tag and the tools that are being used to build it, the environment, that's something that people don't really think about, but that's actually part of the input. And then you look at the output, which is, okay, now you have built a Bitcoin binary, and what does that look like? And you can compare the inputs and the outputs across multiple different builds and see if they are the same or not.

SPEAKER_02: I think cool. So how is this done now? Like you didn't just come along

SPEAKER_01: Before me doing the Geeks build and everything, we were doing this with Githian builds. And Githian builds were very nice. The way that they worked was basically you spun up a Ubuntu VM which is sort of the fixed environment. Though it's not really fixed because every time you download a package, you could be downloading different packages. But basically you ran the build in a very fixed Ubuntu VM with all the right hacks such that everything is the same. For example, we use things like fake time which is a tool that allows you to run any tool and it will report back the time as this time that you set. So that means all the timestamps that any program will ever see is the same. So these are like a few hacks that we sort of put in there in order to make all these things work and end up with a reproducible binary. And I think Bitcoin was one of the first projects to adopt this reproducible builds approach. And when I saw that and that was pretty inspiring. And in recent years, there have been more of a push towards a generalized reproducible build ecosystem. A lot of Linux distros are adopting this approach now. Debian, I think in the latest LTS release, has said that they're going to require new packages to be reproducible before they are accepted into their list of packages that they send to users. And also Arch Linux is making a lot of progress in this regard. And obviously, functional distros like Nex and Geeks are at the forefront of all this. They organize the conferences, and people go and...

SPEAKER_03: Yeah.

SPEAKER_02: We'd like to thank our sponsors for this episode. This episode is brought to you by Capital Controls, because your money belongs to you, except when it doesn't.

SPEAKER_00: So you mentioned that the timestamps were a big issue in the reproducibility of packages. Right, right. How do they do it? Do they have all their build processes also run on...

SPEAKER_01: Right. So this is one good thing about having upstream support. It would be very difficult if Bitcoin was the only project that cared about reproducible builds. But now that more people are caring about it, there's reproduciblebills.org, which is this organization of everybody who cares about this. People have rallied around the standard called source state epoch, if I remember correctly. So that's an environment variable that programs can implement in their own source code and abide by, right? So programs can, in their own source code, say, OK, now I have to insert a timestamp into the output. I'm going to check this environment variable and make sure that I'm going to check this environment variable and see if anything is set there. If anything is set there, I'm going to put that timestamp instead of what I intended to do as the timestamp. So that eliminates the hacky way of doing fake time, right? Because if you do fake time, then all timestamps are reported as that time, which is probably not what you want, especially if you do some kind of profiling or instrumenting or other things that you might need to do with time. But of course, not all software support this new standard yet. So it's sort of going along. But a lot of build tools are starting to honor this new environment variable, which is very cool to see.

SPEAKER_00: So there was a stack exchange question actually on how to do a Gitgen reproducible build today. Yeah, looked into it. And one of the first comments that I read was like, well, great, so now I build this VM package to build reproducibly, but I'm trusting the person that packaged that VM. Oh, for sure.

SPEAKER_01: you For sure, for sure. And that's a great question because that sort of gets to the root of why I want to do the work that I'm doing is because he's absolutely right. If you are downloading this VM package, you are trusting whoever packaged up this VM because again, it is an opaque binary that you're downloading. And not only that, the first thing you're running inside your Githian build is probably app get update and app get upgrade. You're upgrading all these packages and they are opaque binaries that somebody built. And so this is like a huge, how would you call this, trusted seed binary, that binary seed that you're trusting. And my goal with the new kind of reproducible build system based on Geeks is to reduce that to as small of a trusted seed as possible. So Geeks is, you can think of it as Githian but with a much smaller trusted seed. In fact, what we foresee to be able to be done is to have a trusted seed of about 500 bytes of assembly and it's just an assembly implementation of a hex decoder that we can use to then bootstrap the rest of everything. So it will go from that to a higher level language that's a subset of C to a larger subset of C to C itself and into TCC and then into GCC and then we can compile the rest of the world is how it is. So instead of being opaque binaries, these will be sources that could be read and understood by humans, which is much better than going through the binary and try to figure out what's going on.

SPEAKER_00: But strictly speaking, you'd still have to look at every package along the way, right? Right.

SPEAKER_01: How do you update them? You would not be able to. So the way that Geeks works is that it's by default source-based. So basically, if you run a bootstrap build, it will download that 500-byte binary from a seed from somewhere. And then it will actually build every single step along the way up until it gets to GCC. So that is the final goal, at least, is to build every step along the way up till GCC. So you don't have to audit all the outputs of those, all the opaque binaries of those. But you do have to audit the source code. And I don't think there's any way around auditing the source code until we can have some proof on ELF binaries or something like that. I don't think that's a possibility. Yeah.

SPEAKER_02: What other projects are taking security this seriously, this bootstrap?

SPEAKER_01: I mean, as I mentioned, the distros really care about reproducibility. That's the things that they really want. Obviously, geeks, aside from my use as a way to reproducibly build Bitcoin, is an operating system in and of itself. So that's one of the reasons why they care about bootstrapability really seriously is that they want to be able to support all kinds of architectures and also prove that nothing malicious was done along the way. I think one of the important projects that take this seriously is Tor. So Tor actually, after Bitcoin got Githian builds working, took that work and made it their own. I think afterwards, they rebuilt their own tool and abandoned Githian after a while. But I saw a post on the Tor mailing list or the Tor bug tracker that was like, hey, Bitcoin is doing this geeks thing now. Maybe we should do it as well. Yeah, maybe if I have time, I'll help them with that when they are interested.

SPEAKER_00: So you said that Bitcoin was the first project to use Githin. Is Githin a Bitcoin project?

SPEAKER_02: I think so.

SPEAKER_00: Yes. and he's a Yeah, so Gideon was actually created, but it wasn't something that was there before Bitcoin wanted to use it.

SPEAKER_01: So how old is it? Oh man, I'm like Z on the history

SPEAKER_02: All right. Okay. So we have this aspiration to get to both reproducible and bootstrappable builds. Yes. Tell us a little bit about the adventures along the way. What have you run into as you've been working on this? I think the first time you sort of went public with this was summer of 2019 at breaking. Yeah. Yes. And so that's now, it seems like forever ago, but only a little less than 18 months. So tell us about your progress. One pandemic earlier.

SPEAKER_00: Yeah.

SPEAKER_01: Thank you. Oh, man. So I'll start with some overarching things that I have learned out of this, and then we can go into the details. One thing is that in build systems, you can get something hacky working really quick if you really wanted to hack around things, but to get it working nicely, as in getting it to work in a way that will continue to work as packages and get updated and everything is... Reproducible, one might say. Yeah, exactly.

SPEAKER_00: Thanks for watching! reducibly across all sorts of operating systems and architectures, right?

SPEAKER_01: Exactly, and reproducibly, portably, nicely, is another thing. And this arises out of the fact that build systems, a large part of what, another word I guess for a build system is a tool chain, and it's literally what it is. It's a chain of tools that are supposed to work together nicely. Unfortunately, they always over-promise and under-deliver. As in, tools say we support this and that and this and that, and then they support, they actually support this set of features on the code path that is tested most, and on all the other code paths, nothing works properly. It's a mess. And so I had to go into a lot of this, so I mean, I remember clearly when I was doing Windows builds, the hardest thing was to get the builds to be reproducible. We had the builds working, but we had these massive diffs between the outputs of the Bitcoin Ds that were built, and we had no idea where they were coming from. We took a look inside the binaries, but they were just a mess. So the approach that I took was look at where it is in the binary, and sometimes you can figure it out. Sometimes you can't, and what you have to do is compare the intermediate byproducts of the build system. So for example, if it's an archive file, archive files are made by,.a files are made by archiving all of the object files. So if the archive files are different across two builds, let's look at the object files. Are they different? And so all of these things play into if it's reproducible or not. And the end result of doing Windows builds was that we found that GCC8 had a reproducibility bug in how it built Libstud C++. So Libstud C++ is the standard C++ library with things like vectors and all of that. And it is shipped inside GCC, and when you build GCC, it will build a Libstud C++, because GCC, we configured GCC to enable C++ as a language. So Libstud C++.a, as in the archive file, was non-reproducible, but all the object files that make up this archive file were reproducible. So it was actually the ordering of these object files inside this archive file that was non-reproducible. If you think about an archive file as just multiple object files. And so we found, so this comes to, when you put objects in an archive file, sometimes some build scripts will use find, so they'll just do find all.o files and then put them in an archive file or whatever, and that is actually wrong. That is non-reproducible, because when you do find, the order of objects that find returns is dependent on basically just whatever the file system wants. They can return in whatever the file system wants to return, and so you have to sort the output of that.

SPEAKER_00: You basically went into GCC 8 and added a.src to the building of C++ standard.

SPEAKER_01: Yeah, so this is why I feel like Bill's system work is so weird, and that when you start this detective work, you have no idea what anything is, and then you have five different theories, and then you try five different patches. None of this is going to be documented. Thank you.

SPEAKER_02: at it, obviously.

SPEAKER_01: Well, I, hey, I am, I commit messages. I try to document as much of the rabbit hole as possible for, yeah, and that's sort of like one of the things that I want to do is because I feel like a lot of build system tools and build system tools, they're done with the philosophy of, hey, I had to go through this, so future people have to go through this. This is the hard way to learn and whatever. And I don't think that should be the case. So wherever I touch, I try to, first of all, do it nicely so that it's sort of self-documenting. And also in the commit messages, I talk about where you could go wrong, where you could find the sort of misleading evidence that will take you a week to get yourself out.

SPEAKER_02: That's one thing if you're doing this for the Bitcoin project and those commit messages will live in Bitcoin core But there's no documentation on GCC. So

SPEAKER_01: et cetera. So there actually is this specific bug. I opened a pull request to reproduciblebills.org because I found this to be such a just a mind-bending bug. I opened a pull request and they put it in their the wiki. So people in the future who are building with GCC version less than nine, they will know how to make their things reproducible. Awesome. Anything else you run into? Oh yeah, I mean there are there are there are so many things I could talk about. So with the Windows Geeks builds itself...

SPEAKER_02: I

SPEAKER_01: All of these things, most of these things I do, I try to upstream. So for example, NSIS, which is a tool that we use to build Windows installers for our Bitcoin releases, I had to bump it up to 3.05 upstream in Geeks so that it would be maintained and everything. The reason why I wanted to do so is because, coincidentally, the Electrum devs put a patch in there that fixed one of their reproducibility issues. So while I was going through that, I was like, okay, if that might be something that we need in the future, I'll just do that. Which is really cool, as in sort of the Bitcoin open source software community cares that much about reproducibility and everything like that.

SPEAKER_00: So it sounds like there's a bigger, broader movement now of more projects caring about that, and by upstreaming stuff and collecting it on, you said, reproduciblebuilds.org, collects this information. And then perhaps also, I mean, you said it only affects up to GCC 8, so after GCC 8, other versions were reproducible?

SPEAKER_01: Sure. Right, so that bug from before, it's even trickier than I described before. So after GCC 8 and GCC 9, they fixed this in GCC 9's own version of LibTool. And the thing is, when I was doing this at first, I didn't realize that they had already fixed it because this was fixed upstream in LibTool in version 2.7.7b. And in GCC, when they pulled it into their code base, they pulled 2.7.7a and then fixed it locally without pulling the change from upstream. And so it was just a mess, people vendoring different stuff and getting it fixed. So that is all described on the reproducible builds wiki entry that I put in there just in case it helps somebody in the future. But yeah, that was a big thing. One of the things that I learned that might be helpful for anybody else who tries to do reproducible build stuff or just build systems in general is look at what Debian does. Honestly, look at what Debian does. So many times I've been stumped by this reproducibility thing or this build error for days. And then I think, okay, let's go to the Debian repos. So the Debian folks have all of the patches that they apply, all the build scripts that they do, they're all in Git. And I go there and I look at their patches and they have a lot of patches that fix reproducibility issues and that's why it was so helpful for me that we started out with Githian, right? Because Githian uses Ubuntu, which is based on Debian. So I sort of had a source of truth to look to. And so a few examples is, for example, when we were making Windows builds reproducible. So a tool chain consists of, I'm just going up a level, when a tool chain sort of consists of two main things, sorry, three main things, a lot of main things. But the main part is a compiler driver like GCC along with all of its binaries and sort of binutils, which are the utilities that you use to manipulate binaries. And binutils is, again, this is one of those things where it's supposed to work together, but sometimes it doesn't. Binutils is supposed to be kind of compiler driver agnostic, but it really isn't. But for example, in binutils in recent releases, they have added a configure flag, which enables determinism in their tools, which is, again, great. This is a community-wide effort to get things to be deterministic and reproducible. However, when you turn that flag on in configure, it makes all of the tools deterministic, but in the LD linker specifically for Windows builds, it doesn't turn on the determinism flag, which is one of the things. Again, this is the overarching context, right? Things are supposed to work well together, but they don't. So this is one of the things that I found in Debian's repository that was extremely helpful. And that flag makes sure that when we link together, it sets the deterministic mostly means the user ID is zero, the group ID is zero. That's sort of the really easy things to leak into non-determinism, and the timestamp is like one or something reasonable and deterministic ordering. One of the things, sorry, that just came to my mind, one of the things about sorting find output or sorting directory listings or sorting symbols or anything like that is it's actually not enough to use sort, because sort is locale dependent, so you actually need to set your locale to a deterministic locale before you sort, which is, again, one of those things where it's just like, why doesn't it work the way I want it to? But yeah, that was really cool. We found another tool, DLL tool, which is Windows specific, that the files it outputs has prefixes tied to that tool's processes ID. So it's PID is the prefix of all the files that it outputs, which it just makes no sense at all to me, but that's just the way it works. That's a source of non-determinism. ID or PID could be any number, basically. And obviously things like GenDef, which includes a date in its output, which is a big source of non-determinism. But yeah, it was just like whacking things, making them work.

SPEAKER_02: Mm-hmm.

SPEAKER_00: Turtles all the way down. Yeah, exactly. Turtles all the way down. So we talked a little bit about how multiple people might reproduce a build in order to provide the binary on, say, bitcoincore.org or bitcoin.org and other sources where you might retrieve bitcoin. They start out with the same inputs with the release tag, build it from source, use this Githyn or Geeks set up to have a shared tool chain that is reproducible as well. And then they arrive at the same package. Should everybody do that at home now? Is that something that every single bitcoin user should do?

SPEAKER_02: Mm-hmm.

SPEAKER_01: So, I believe in, and this is just a personal opinion, but my personal opinion is I believe in user choice in their security model, as well as user choice in the extremes of security models, right? I feel like there should be a spectrum of how much you trust the developers. So if, perhaps, if you manage a lot of money and you, you know, you perhaps want to run this reproducible build just to see that everything is being built the way that you should. And this is, you know, one of the reasons why we have source-based distros like Gentoo, right? Like Gentoo is you just build the world from source, right? Because you don't trust anybody. I would say that that is sort of meaningless without a way to actually bootstrap everything like Geeks does, but, you know, you should build from source if you trust no one. But one of the great things about reproducible builds is that it allows for people to attest to results, right? So you can almost, I mean, I don't know too much about Web of Trust, I feel like this is a big word, but like you can almost look at your Web of Trust, like who do you trust to build this correctly? Who do you trust to be adversarial enough such that they're not going to lie together or things like that and look at their Gideon signatures and look at what they've attested to and see that, okay, this build is probably reproducible, this build is probably okay.

SPEAKER_02: And that's right now mostly the maintainers, right?

SPEAKER_01: Yes, right, exactly. That's mostly the maintainers, though this could be run by anybody.

SPEAKER_00: There's a few people that aren't even code contributors that have figured out how to run the Githian bills and they add their signatures to it, and that's great, actually, because they're not part of the developer cabal. And you can still make the attestation that you took a specific release tag of code and ran it on a separate machine and you got this tag, sorry, the hash, I guess, is what you, in the end, compare. And while you might not have compared the code itself, you compare the process and you show that you could reproduce the building step of it. And then there's other people that might review the code and attest that the code is fine and got released. People sign off on a release before it's tagged, right?

SPEAKER_02: You can We'd like to again thank our sponsors. This episode is brought to you by Capital Controls, because nothing says you can trust the value of our currency by just banning you from cashin' out.

SPEAKER_01: So this also ties back to another thing that I wanted to talk about, which was we want to make this process accessible to as many people as possible, right? So for example, when I first started to try to run GTM builds and whatever, it was extremely hard because the, basically the, I think there were two tested paths that were on Ubuntu and Fedora, and I was running Arch Linux at the time, and somehow things would break, like I was on LXC version three and the instructions were for LXC version two, and basically the only thing that worked was like Docker on Ubuntu, that was the only easy path that worked. And so being able to get it on Geeks, where everything runs in a Docker container where we have pinned everything, for example, we use the nicely named Geeks time machine command to roll the system to a specific commit of the Geeks distro, is really nice for being able to reproduce bugs, being able to look at that, and I think the requirements for Geeks are just like a sane Linux kernel with namespaces enabled, which has been enabled since a few LTS versions ago. And so I think that'll be very nice, and I hope that with that we can encourage people who run different distros, not only Debian-based distros, to be able to run this build for themselves, and they don't need to attest publicly in gettn.segs, but they can if they want to, and they can just prove to themselves.

SPEAKER_02: Can I ask a basic question? Those hashes, how are they produced? Is this just a hash over the binary?

SPEAKER_01: Yeah, yeah. I mean, they're just a very simple SHA-256 sum over the binary, which is, yeah, it's pretty nice, yeah.

SPEAKER_02: Cool. Awesome. Do you want to talk about your Mac toolchain? Oh yeah.

SPEAKER_01: Oh yeah. Yeah, for sure. Yeah, I'd love to talk about that. So going into the Mac OS toolchain. So our Mac OS build system is mostly two things, a toolchain and an SDK. And let me back up and give you some context here. You're basically not really supposed to, not supposed to, but it is definitely unsupported to cross-compile for Mac OS from, okay, it is definitely not supported to cross-compile for Mac OS from Linux or from any other operating system. That's how Steve Jobs wanted it. Exactly. That's how Steve Jobs wanted it. And so I think the way that we got this to work was like, I mean, this was before I was around, but this was, I think Corey's doing, Corey's, one of Corey's first contributions was making Mac OS cross-compiles work for Bitcoin. And the way that he got that to work was to lock everything down. As in what we use for our toolchain is a version of Clang that is downloaded from llvm.org. Yes, that's a trusted binary. Downloaded from llvm.org that targets, I guess it could be the API, but basically it targets the Ubuntu distro, right? But that means that again, you can't run cross-builds from things like Arch Linux or any other thing to Mac OS. So he pinned it at this specific binary just because when Apple releases an SDK, it releases an SDK and it says, and it couples this SDK with a specific Clang and with a specific toolchain, right? So when he was doing this, they released the SDK and the SDK was pinned to Clang three points something or something like that. And throughout the years, when we bump our Apple SDK, we also bump the toolchain to sort of match that. And so that's how normally our thing is constructed, right? And so let's talk about how we do this because I don't think cross-building for Mac is something that most developers have done just because it's such a big hassle. And one of the things I wanted to do when making Geeks build for Mac OS is just to make this less of a hassle because it really doesn't need to be that way. So the SDK, one of the things about making the SDK is that you need an Apple developer account. There's no URL to W get the SDK. You need to go in and you need to have the authentication cookie set so that you can download this SDK. And so we download this SDK and it's in a proprietary format that ends with.XIP. It's a zip file but not with a XIP file. And basically the way to extract that is we need to compile a program called XAR and a program called PBZX and then pipe this XIP file through XAR and then PBZX and then CPIO and then finally we get an Xcode.app that is like multiple gigabytes which is not the best. And so from that Xcode.app we have documentation on what I would only call our incantations. I feel like these are not invocations. These are incantations because we're compiling with Clang with fixed R paths and everything. These are incantations to extract the SDK from this Xcode.app and then we can use this SDK with our toolchain. And all this is like you can there are so many ways to fail in every step of this incantation that it is incredible. So one of the things I did with this was to Python all the things basically. What I found is that Python's standard library, this is one of the great things about program languages that are basically universally available with a big standard library, is that Python has this great standard library that's actually more flexible than command line tools. I tried to write this in bash first because I love bash but just found it to be much easier in Python. I wrote a Python script that was able to extract SDKs in the right way and then Corey contributed a part of this which was he was able to extract the.xip file without needing to compile XAR or PBZX. He did some nice bit fiddling and now it's just two Python scripts that you run on one file and there's no compiling this application with Clang and then having to do all this stuff which was really great and that simplified a lot of stuff and hopefully it will lead to much more people being able to do this process in the future.

SPEAKER_02: So there's not a lot of you doing this process of review and looking at your PRs like, it's you, Fanquake, Corey, Shores is doing a decent amount of testing. So like, how do we move forward when there's, you know, there's four people that we're all relying on?

SPEAKER_01: I don't know. I don't think there's only four people, I think. I think there are more people because with things like the macOS toolchain changes that I'm talking about, we do this and then a lot of forks of Bitcoin, if you go back to that PR, you'll see at the bottom a lot of forks of Bitcoin, they do their own review and then they pull this into their code base, which I'm very happy about, which means they might submit bug fixes and stuff in the future for the random scripts that I write, which is fantastic.

SPEAKER_00: I mean, I can just trust the binary up there, right? It's been signed by the release key of the Bitcoin maintainer. And there's a bunch of people that, in the process of creating that binary, did the reproducible builds already. So you said that people can choose different trust levels. If my trust level is, I already trust the developers for their code. The same developers, a bunch of them, produced this reproducible builds in order to come to consensus that this is the release that they wanted to produce. And it's signed by the appropriate key. So I trust Vladimir's key. And I trust the developers to produce the right thing. What do I gain? Don't I open myself up to other sorts of attacks by installing maybe the tool chain to do reproducible builds or something? Is it maybe not even, in some scenario, safer to just go with the fact that it's the right thing?

SPEAKER_01: I'll see you next time.

SPEAKER_03: Thanks for watching!

SPEAKER_01: Mm-hmm.

SPEAKER_02: Thanks for watching! I don't know.

SPEAKER_01: I mean, if you already trust, so going back to what you said, if you already trust the maintainers and trust people who are signing the binary to not do anything malicious, the benefit to you of reproducible builds is that you can think of it as a way for these maintainers that you trust to check themselves, you understand what I'm saying? Because before releases, people run, the maintainers run reproducible builds to check amongst themselves that everything is alright.

SPEAKER_00: So I think I get the point that the reproducible build helps maintainers to come to a consensus that they agree on what they had for a source and what the output of that was. Yes. So to, as a group, authorize something, right? Exactly.

SPEAKER_01: Thanks for watching! Right? And the fact that this is reproducible in the other sense, as in reproducible outside of this group, it means that if your level of trust shifts a little bit towards I'm not entirely sure that this group of maintainers is not collaborating, you can go check them yourself. Right.

SPEAKER_00: Right, and even if you don't program or don't want to go through the code base yourself, you could pay someone to review what exactly is in the release tag and to do the reproducible build and then come basically do an audit.

SPEAKER_01: Yeah, exactly. That's exactly right.

SPEAKER_02: what it is. That was part one of our interview with Carl. Stay tuned for the second half released in a couple of weeks.

SPEAKER_03: Well, what a great sit down with Carl. It was a nice sit down. You guys covered a lot.

SPEAKER_02: It was a nice sit down.

SPEAKER_00: Oh yes. I especially have a new appreciation of how much detective work and debugging work it is to get something reproducible. I mean, if you're writing code, you're at least staring at your own stuff and you have an idea of where you're looking, but you're diving into this whole tool chain here and you have no idea at what level of the stack something is going awry. I think that just has to be really appreciated.

SPEAKER_02: Yeah, I think something that stood out to me was hearing about Gideon and how it grew up around Bitcoin. I guess it's undetermined whether it was a Bitcoin project or Bitcoin was the first to really use it. But these other projects that have adopted Gideon and now Geeks, Bitcoin is sort of leading the way and being paranoid about what's happening upstream and guarding against it.

SPEAKER_00: Mm-hmm. Yeah, it's kind of interesting. Sometimes we're a little close to the whole project. But also, for example, on GitHub, it's just been breaking a few of the previous assumptions about project interactions, how much work there is going to be in one code base, and things like that. So it's sometimes nice to see how it impacts other areas of software engineering.

SPEAKER_02: Thanks for watching!

SPEAKER_03: Great. Well, we hope you enjoyed. Thank you for listening. If you'd like to learn more about ChainCode, or Carl for that matter, you can go to ChainCode.com. And where else? Where else can they find you?

SPEAKER_00: Definitely go to Twitter. You can find us on Twitter at ChainCodeLabs.

