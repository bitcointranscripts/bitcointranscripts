---
title: Reproducible Builds
transcript_by: Michael Folkson
speakers:
  - Carl Dong
tags:
  - reproducible-builds
date: 2020-11-30
media: https://www.youtube.com/watch?v=Y5Gfli3x6rI
episode: 9
aliases:
  - /chaincode-labs/chaincode-podcast/2020-11-30-carl-dong-reproducible-builds/
---
Carl Dong’s presentation at Breaking Bitcoin 2019 on “Bitcoin Build System Security”: https://diyhpl.us/wiki/transcripts/breaking-bitcoin/2019/bitcoin-build-system/

## Intro

Adam Jonas (AJ): Welcome to the Chaincode podcast Carl.

Carl Dong (CD): Hello.

AJ: You know we’ve been doing this podcast for a while now. How come you haven’t been on the show yet?

CD: We’ve been at home.

AJ: We did a few episodes before that though.

Murch (M): It is fine. We’ve got you now.

AJ: We’ll try not to take it too personally. Today we are going to talk about all things Carl Dong. Maybe start off with a little bit about what you’ve been doing in the break, what have you been doing since we haven’t been in the office?

CD: I’ve been doing a lot of stuff. I’ve been continuing my work on reproducible builds and the build system in general. And also I’ve been getting into the codebase, looking at some cleanup stuff that can be done and what features they may lead to.

## Reproducible builds

Bitcoin Build System Security presentation: https://diyhpl.us/wiki/transcripts/breaking-bitcoin/2019/bitcoin-build-system/

Guix: https://guix.gnu.org/

AJ: Start from the top. Tell us about reproducible builds.

CD: After I gave that talk last year about Guix I’ve been working a lot on that. Mainly this year it has been a lot of getting things that were barely working into things that are nicely working. We can start with context I guess. If you download a piece of software from the Bitcoin Core website or from GitHub or whatever it is an opaque blob that could contain any code. Technically bitcoincore.com (not the trusted site for Bitcoin Core, that is bitcoincore.org) could serve up a binary that steals all your Bitcoin. How do people know that what they downloaded is what is intended or what is in the codebase or something that they have reviewed? That is why you need reproducible builds so that multiple people can run the build and see that they got the same thing. Nobody inserted something malicious into the binary.

AJ: How do they make that comparison?

CD: They make that comparison by looking at the inputs and looking at the outputs of this process. The inputs will probably be the Bitcoin codebase…

M: The release tag?

CD: Exactly, the release tag and the tools that are being used to build it, the environment. That is something that people don’t really think about but that is part of the input. Then you look at the output which is “Now you have built a Bitcoin binary. What does that look like?” You can compare the inputs and the outputs across multiple different builds and see if they are the same or not.

AJ: How is this done now? You didn’t just come along.

CD: Before me doing the Guix build we were doing this with [Gitian builds](https://gitian.org/). Gitian builds were very nice. The way they worked was basically you spun up an Ubuntu VM which is the fixed environment, though it is not really fixed because every time you download a package you could be downloading different packages. You ran the build in a very fixed Ubuntu VM with all the right hacks such that everything is the same. For example we use things like [faketime](http://manpages.ubuntu.com/manpages/trusty/man1/faketime.1.html) which is a tool that allows you to run any tool. It will report back the time as this time that you set. That means all the timestamps that you any program will ever see is the same. These are a few hacks that we put in there in order to make all these things work and end up with a reproducible binary. I think Bitcoin was one of the first projects to adopt this reproducible builds approach. When I saw that, that was pretty inspiring. In recent years there has been more of a push towards a generalized reproducible build ecosystem. A lot of Linux distros are adopting this approach now. Debian, I think in the latest LTS release has said that they are going to require new packages to be reproducible before they are accepted into their list of packages that they send to users. Also Arch Linux is making a lot of progress in this regard. Obviously functional distros like [Nix](https://diyhpl.us/wiki/transcripts/stephan-livera-podcast/2020-07-26-nix-bitcoin/) and Guix, they are at the forefront of all this. They organize conferences and people go.

M: You mentioned that the timestamps were a big issue in the reproducibility of packages. Do they have all their build processes also run on…?

CD: This is one good thing about having upstream support. It would be difficult if Bitcoin was the only project that cared about reproducible builds. Now that more people are caring about it there is [reproducible-builds.org](https://reproducible-builds.org/) which is this organization of everybody who cares about this. People have rallied around this standard called [SOURCE_DATE_EPOCH](https://reproducible-builds.org/docs/source-date-epoch/). That’s an environment variable that programs can implement in their own source code and abide by. Programs can in their own source code say “Now I have to insert a timestamp into the output. I am going to check this environment variable and see if anything is set there. If anything is set there I am going to put that timestamp instead of what I intended to do as the timestamp.” That eliminates the hacky way of doing fake time. Because if you do fake time then all timestamps are reported as that time which is probably not what you want. Especially if you do some kind of profiling or instrumenting or other things that you might need to do with time. But of course not all software supports this new standard yet. It is going along but a lot of build tools are starting to honor this new environment variable which is very cool to see.

M: There was a StackExchange [question](https://bitcoin.stackexchange.com/questions/99967/reproducible-gitian-builds-but-not-the-same-hash-as-bitcoincore-org) on how to do a Gitian reproducible build today. I looked into it. One of the first comments I read was like “Great. So now I build this VM package to build reproducibly but I’m trusting the person that packaged that VM.”

CD: For sure. That’s a great question. That gets to the root of why I want to do the work that I’m doing. He’s absolutely right. If you are downloading this VM package you are trusting whoever packaged up this VM. Because again it is an opaque binary that you are downloading. Not only that, the first thing you are running inside your Gitian build is probably `apt-get update` and `apt-get upgrade`. You are upgrading all these packages and they are opaque binaries that somebody built. This is a huge trusted binary seed that you are trusting. My goal with the new kind of reproducible build system based on Guix is to reduce that to as small a trusted seed as possible. You can think of Guix as Gitian with a much smaller trusted seed. In fact what we foresee to be done is to have a trusted seed of about 500 bytes of assembly. It is an assembly implementation of a hex decoder that we can use to then bootstrap the rest of everything. It will go from that to a higher level language that is a subset of C to a larger subset of C to C itself and to TCC and to GCC. Then we can compile the rest of the world. Instead of it being opaque binaries these will be sources that could be read and understood by humans which is much better than going through a binary and trying to figure out what is going on.

M: Strictly speaking you would still have to look at every package along the way right? How do you update them?

CD: The way Guix works is that it is by default source based. If you run a bootstrap build it will download that 500 byte binary seed from somewhere and then it will actually build every single step along the way up until it gets to GCC. That is the final goal at least. To build every step along the way up until GCC so you don’t have to audit all the outputs of those, all the opaque binaries of those, but you do have to audit the source code. I don’t think there is any way around auditing the source code until we can have some proof on the binaries or something like that. I don’t think that is possible.

AJ: What other projects are taking security this seriously, this bootstrapability?

CD: As I mentioned the distros really care about reproducibility. That is one of the things they really want. Obviously Guix, aside from my use as a way to reproducibly build Bitcoin, is an operating system in of itself. That’s one of the reasons why they care about bootstrapability really seriously. They want to be able to support all kinds of architectures and also prove that nothing malicious was done along the way. I think one of the important projects that takes this seriously is Tor. Tor, after Bitcoin got Gitian builds working, took that work and made it their own. I think afterwards they rebuilt their own tool and abandoned Gitian after a while. I saw a post on the Tor mailing list, on the Tor bug tracker, that was like “Hey. Bitcoin is doing this Guix thing now. Maybe we should do it as well.” Maybe if I have time I will help them with that when they are interested.

M: You said that Bitcoin was the first project to use Gitian. Is Gitian a Bitcoin project?

CD: I think so.

AJ: The author, I see devrandom. He’s a Bitcoin contributor.

M: So Gitian wasn’t something that was there before Bitcoin wanted to use it.

CD: No I don’t think so.

AJ: And how old is it?

CD: I’m fuzzy on the history.

AJ: We have this aspiration to get to both reproducible and bootstrappable builds. Tell us about the adventures along the way. What have you run into as you’ve been working on this? I think the first time you went public with this was Summer 2019 at Breaking Bitcoin. That seems like forever ago but only a little less than 18 months. Tell us about your progress.

CD: I’ll start with some overarching things that I’ve learned out of this then we can go into the details. One thing is that in build systems you can get something hacky working really quick if you want to hack around things. But to get it working nicely, as in getting it to work in a way that will continue to work as packages get updated…

AJ: Reproducibly as one might say.

M: Upgrading systems and architectures

## Reproducibility bug in GCC

CD: Reproducibly, portably, nicely is another thing. This arises out of the fact that build systems, another word I guess for a build system is a toolchain. It is literally what it is. It is a chain of tools that are supposed to work together nicely. Unfortunately they always overpromise and underdeliver. Tools say “We support this and that” and then they actually support this set of features on the code path that is tested most. On all the other code paths nothing works properly. It is a mess. I had to go into a lot of this. I remember clearly when I was doing Windows builds the hardest thing was to get the builds to be reproducible. We had the builds working but we had these massive diffs between the outputs of the bitcoind’s that were built and we had no idea where they were coming from. We took a look inside of the binaries but they were just a mess. The approach that I took was look at where it is in the binary and sometimes you can figure it out. Sometimes you can’t. What you have to do is compare to intermediate byproducts of the build system. For example if it is an archive file, archive files are made by archiving all of the object files. If the archived files are different across two builds let’s look at the object files. Are they different? All of these things play into whether it is reproducible or not. The end result of doing Windows builds was that we found that GCC8 had a reproducibility bug in how it built [libstdc++](https://gcc.gnu.org/onlinedocs/libstdc++/faq.html). libstdc++ is the standard C++ library with things like vectors and all of that. It is shipped inside GCC. When you build GCC it will build libstdc++ because we configure GCC to enable C++ as a language. `libstdc++.a` as in the archive file was non-reproducible but all the object files that make up this archive file were reproducible. It was actually the ordering of these object files inside this archive file that was non-reproducible. If you think about an archive file as multiple object files. When you put objects in an archive file sometimes some build scripts will use `find`. They will do find all `.o` files and put them in an archive file. That is actually wrong. That is non-reproducible because when you do `find` the order of objects that find returns is dependent on whatever the filesystem wants. They can return whatever the filesystem wants to return and so you have to sort the output of that.

M: You went into GCC8 and added a sort to the building of C++ libstd?

CD: I feel like build system work is so weird. When you start this detective work you have no idea what anything is and you have five different theories.

AJ: None of this is going to be documented obviously.

CD: In my commit messages I try to document as much of the rabbit hole as possible. That’s one of the things I want to do. I feel like a lot of build system tools, they are done with the philosophy of “I had to go through this so future people have to go through this. This is the hard way to learn.” I don’t think this should be the case. Wherever I touch I try to do it nicely so that is sort of self documenting. Also in the commit messages I talk about where you could go wrong, where you could find the misleading evidence that will take you a week to get yourself out of.

AJ: That is one thing if you are doing this for the Bitcoin project. Those commit messages will live in Bitcoin Core. But there is no documentation on GCC etc.

CD: There actually is. This specific bug, I opened a pull request to reproduciblebuilds.org. Because I found this to be such a mind bending bug I opened a pull request and they put it in their wiki. People in the future who are building with GCC version less than 9, they will know how to make their things reproducible.

AJ: Awesome. Anything else you have run into?

CD: There are so many things I could talk about. With the Windows GUIX builds most of these things I do I try to upstream. For example [NSIS](https://sourceforge.net/projects/nsis/) which is a tool that we use to build Windows installers for our Bitcoin releases, I had to bump it up to 3.05 upstream in Guix so that it would be maintained. The reason I wanted to do so is because coincidentally the Electrum devs put a patch in there that fixed one of their reproducibility issues. While I was going through that I was like “If that might be something that we need in the future I will just do that.” This is really cool that the Bitcoin open source software community cares that much about reproducibility.

M: It sounds like there is a broader movement of more projects caring about that. By upstreaming stuff and collecting it on reproduciblebuilds.org, collects this information. You said it only affects up to GCC8 so after GCC8 other versions were reproducible?

CD: That bug from before, it is even trickier than I described. After GCC8, in GCC9 they fixed this in GCC9’s own version of libtool. When I was doing this at first I didn’t realize that they had already fixed it because this was fixed upstream in libtool in version 2.7.7b. In GCC when they pulled it into their codebase they pulled 2.7.7a and then fixed it locally without pulling the change from upstream. It was just a mess. People vendoring different stuff and getting it fixed. That is all described on the reproducible builds wiki entry that I put in there just in case it helps somebody in the future. That was a big thing.

## Look at what Debian does

CD: One of the things that I learned that might be helpful for anybody else who tries to do reproducible build stuff or just build systems in general, is look at what Debian does. So many times I’ve been stumped by this reproducibility thing or this build error for days and then I think “Let’s go to the Debian repos.” The Debian folks have all the patches that they apply, the build scripts that they do, they are all in Git. I go there and I look at their patches and I have a lot of patches that fix reproducibility issues. That’s why it was so helpful for me that we started out with Gitian. Gitian uses Ubuntu which is based on Debian. I had a source of truth to look to. For example when we were making Windows builds reproducible. A toolchain consists of a lot of main things. The main part is a compiler driver like GCC along with all of its binaries and Binutils which are the utilities that you use to manipulate binaries. It is one of those things where it is supposed to work together but sometimes it doesn’t. Binutils is supposed to be compiler driver agnostic but it really isn’t. In Binutils, in recent releases, they haven’t added a configure flag which enables determinism in their tools. This is again great. This is a community wide effort to get things to be deterministic and reproducible. However, when you turn that flag on in configure it makes all the tools deterministic but in the LD linker specifically for Windows builds it doesn’t turn on the determinism flag. This is the overarching context, things are supposed to work well together but they don’t. This is one of the things that I’ve found in Debian’s repository that was extremely helpful. That flag makes sure when we link together it sets… Deterministic mostly means the user ID is zero, the group ID is zero. Those are the easy things to leak into non-determinism. The timestamp is one or something reasonable. And deterministic ordering. One of the things about sorting find output or sorting directory listings or sorting symbols or anything like that is it is actually not enough to use sort. Because sort is locale dependent so you actually need to set your locale to a deterministic locale before you sort. This is again one of those things where it is like “Why doesn’t it work the way I want it to?” We found another DLL tool which is Windows specific. The files it outputs have prefixes tied to that tool’s process ID. Its PID is the prefix of all the files that it outputs. It makes no sense at all to me but that’s the way it works. That’s the source of non-determinism. Your PID could be any number basically. Obviously things like gendef which includes a date in its output which is a big source of non-determinism. It is like whacking things, making them work.

## User choice in their security model

M: Turtles all the way down. We talked about how multiple people might reproduce a build in order to provide the binary on say bitcoincore.org or bitcoin.org and other sources from which you might retrieve Bitcoin. They start out with the same inputs with the release tag, built from source, using Gitian or Guix, set up to have a shared toolchain that is reproducible as well. Then they arrive at the same package. Should everybody do that at home? Is that something that every single Bitcoin user should do?

CD: I believe, this is a personal opinion, in user choice in their security model as well as user choice in the extremes of security models. There should be a spectrum of how much you trust the developers. If you manage a lot of money perhaps you want to run this reproducible build just to see that everything is being built the way that it should. This is one of the reasons we have source based distros like Gentoo. Gentoo is just build the world from source because you don’t trust anybody. I would say that that is meaningless without a way to actually bootstrap everything like Guix does. But you should build from source if you trust no one. One of the great things about reproducible builds is it allows for people to attest to results. I don’t know too much about web of trust, I feel this is a big word. You can almost look at your web of trust, who do you trust to build this correctly? Who do you trust to be adversarial enough such that they are not going to lie together or things like that. Look at their Gitian signatures and look at what they have attested to. See that this build is probably reproducible, this build is probably ok.

AJ: Right now that is mostly the maintainers?

CD: Exactly, that’s mostly the maintainers. But it could be run by anybody.

M: There are a few people that aren’t even code contributors that have figured out how to run the Gitian builds and they add their signatures to it. That is great actually because they are not part of the developer cabal. You can still make the attestation that you took a specific release tag of code and ran it on a separate machine and you got the hash I guess is what you end up comparing. While you might not have compared the code itself you compare the process and you show that you could reproduce the building step of it. Then there are other people who might review the code and attest that the code is fine in a release. People sign off on a release before it is tagged.

## Making the process accessible

CD: This also ties back to another thing that I wanted to talk about which was we want to make this process accessible to as many people as possible. For example, when I first started to try to run Gitian builds it was extremely hard because I think there were two tested paths that were on Ubuntu and Fedora and I was running Arch Linux at the time. Things would break. I was on LXC version 3 and the instructions were for LXC version 2. The only thing that worked was Docker on Ubuntu. That was the only easy path that worked. Being able to get it on Guix where everything runs on a Docker container, where we have pinned everything. For example we use the nicely named Guix time machine command to roll the system to a specific commit of the Guix distro. It is really nice for being able to reproduce bugs, being able to look at that. I think the requirements for Guix are a sane Linux kernel with namespaces enabled which has been enabled since a few LTS versions ago. I think that will be very nice. I hope that with that we can encourage who run different distros, not only Debian based distros, to be able to run this build for themselves. They don’t need to attest publicly in Gitian but they can if they want to. They can prove to themselves.

AJ: Those hashes. How are they produced? Is this just a hash over the binary?

CD: Yes. They are just a very simple SHA256sum over the binary.

## Mac OS X Toolchain & SDK and cross-compiling

AJ: Do you want to talk about your Mac toolchain?

CD: Yes for sure. Our Mac OS build system is mostly two things: a toolchain and a SDK. Let me back up and give you some context here. It is definitely not supported to cross compile for Mac OS from Linux or from any other operating system.

AJ: That’s how Steve Jobs wanted it.

CD: Exactly. The way we got this to work, this was before I was around, one of Cory (Fields) first contributions, making Mac OS cross compiles work for Bitcoin. The way that he got that to work was to lock everything down. As in what we use for our toolchain is a version of Clang that is downloaded from llvm.org, a trusted binary, that targets the Ubuntu distro. That means you can’t run cross builds from things like Arch Linux or any other thing to Mac OS. He pinned it at this specific binary because when Apple releases a SDK it couples this SDK with this specific Clang and toolchain. When he was doing this they released the SDK and the SDK was pinned to Clang 3.x. Throughout the years when we bump our Apple SDK we also bump the toolchain to match that. That’s how normally our thing is constructed. Let’s talk about how we do this. I don’t think cross building for Mac is something that most developers have done just because it is such a big hassle. One of the things I wanted to do when making Guix build for Mac OS’ system is make it less of a hassle. It really doesn’t need to be that way. The SDK, one of the things about making the SDK is that you need an Apple developer account. There is no URL to wget the SDK. You need to go in and you need to have the authentication cookie set so that you can download this SDK. We download this SDK and it is in a proprietary format that ends with `.xip`. It is a zip file but not with a `z`. The way to extract that is we need to compile a program called xar and a program called pbzx. Then pipe this `xip` file through xar and then pbzx and then cpio. Finally we get an Xcode.app that is like multiple gigabytes which is not the best. From that Xcode.app we have documentation on what I would call our incantations. I feel like these are not invocations, these are incantations because we are compiling with Clang with fixed rpaths. These are incantations to extract the SDK from this Xcode.app. Then we can use this SDK with our toolchain. There are so many ways to fail in every step in this incantation. It is incredible. One of the things I did with this was to Python all the things. What I found is that the Python standard library, this is one of the great things about programming languages that are universally available with a big standard library, is that Python has this great standard library that is more flexible than command line tools. I tried to write this in bash first because I love bash but I found it to be much easier in Python. I wrote a Python script that was able to extract SDKs in the right way and then Cory contributed a part of this. He was able to extract the `.xip` file without needing to compile xar or pbzx. He did some nice bit fiddling. Now it is just two Python scripts that you run on one file and there is no compiling this application with Clang and having to do all of this stuff which was really great. That has simplified a lot of stuff. Hopefully it will lead to many more people being able to do this process in the future.

## Core contributors to the build system

AJ: There are not a lot of you doing this process of review and looking at your PRs. It is you, fanquake, Cory, Sjors is doing a decent amount of testing. How do we move forward when there are four people who we are all relying on.

CD: I don’t think there is only four people. I think there are more people because with things like the Mac OS toolchain changes that I’m talking about, we do this and then a lot of forks of Bitcoin, if you go back to that PR you’ll see at the bottom a lot of forks of Bitcoin, they do their own review and then they pull this into their codebase. I’m very happy about. They might submit bug fixes and stuff in the future for the random scripts that I write which is fantastic.

M: I can just trust a binary up there. It has been signed by the release key of the Bitcoin maintainer. There are a bunch of people that in the process of creating that binary who did reproducible builds already. You said that people can choose different trust levels, if my trust level is I already trust the developers for the code, the same developers, a bunch of them, produce this reproducible build in order to come to consensus that this is the release that they wanted to produce. It is signed by the appropriate key. I trust Wladimir’s key and I trust the developers to produce the right thing. Do I open myself up to attacks by installing the toolchain to do reproducible builds? Is it in some scenarios safer to go with the signed binary?

CD: If you already trust the maintainers and trust people who are signing the binary to not do anything malicious the benefit to you of reproducible builds is that you can think of it as a way for these maintainers that you trust to check themselves. Before releases the maintainers run reproducible builds to check among themselves that everything is alright.

M: I think I get the point that the reproducible build helps maintainers to come to consensus that they agree on what they had for source and what the output of that was and as a group authenticate something.

CD: Exactly. The fact that this is reproducible in the other sense, as in reproducible outside of this group, means that if your level of trust shifts a little bit towards “I’m not entirely sure that this group of maintainers is not collaborating” you can go check them yourself.

M: Even if you don’t program or don’t want to go through the codebase yourself you could pay someone to review what exactly is in the release tag and to do the reproducible build. Basically do an audit.

CD: Exactly, that's exactly what it is.
