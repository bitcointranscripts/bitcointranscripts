---
title: Reproducible Builds
transcript_by: Bryan Bishop
tags:
  - build systems
speakers:
  - Carl Dong
---
Reproducible builds, binaries and trust

Carl Dong (Chaincode Labs)

# Introduction

I am Carl and I work at Chaincode Labs and I will be talking about software, binaries and trust. I am happy that Ethan talked about his subject because it ties into my talk. For the purposes of this talk, assume that everything is perfect and there's no bugs and no CVEs and all the things that Ethan talked about don't exist. Basically, imagination. I am here to talk about that even if this is the case, clean source code is not enough.

Even with clean source code, we can invoke the worst case bug he talked about across architectures if we do just one thing. Because we have all of these things that are in the stack and we have no visibility into what we're talking about-- hardware is cutoff here for a reason because it's just too worrying for me. My name is Carl and I am here to haunt your dreams.

# Runtime dependencies

Cory mentioned earlier that there was an openssl bug in 2008. I'd like to go into that a little bit more. Basically it started with this debian maintainer posting on the openssl mailing list asking about hey these two lines look like a use after free in valgrind and can we just remove it? After some back and forth, they decided to remove it. This caused a CVE in 2008 where the openssl package was generating predictable random numbers which aren't random. The effected keys were openssh keys and so on, all the things that we depend on for our security--- again, they didn't do anything wrong, but everything went wrong because of the runtime dependency on openssl.

The only way to mitigate this is to minimize and audit our runtime dependencies. All you can do is minimize the number of dependencies that you have. Minimize the out-of-tree dependencies that you have. In Bitcoin Core, the way we do this is that after we run release builds, we run a checksymbols script that only allows some specific libraries in the ALLOWED\_LIBRARIES variable.

# Buildtime dependencies

Clean source code is not enough. We talked about auditing dependencies and whatever, but auditing dependencies is not enough. Let's go to the second circle of hell, buildtime dependencies. There was an incident in 2015 called XcodeGhost. This might be a little obscure. But basically what happened in 2015 was there was this hacker called coderfun that uploaded versions of xcode to pan.baidu.com which is China's version of dropbox. Because the app store is super flakey in china, they just download the first thing htey find on Google. They were able to do some SEO optimizations to get his link to be the first link. People downloaded it and compiled their applications. He was able to infect some of the biggest apps in China. These were the apps like Didi, Wechat and Netease which were the equivalents of Uber, WhatsApp and Spotify. So how do we counter against this in bitcoin?

# Building releases in bitcoin

So how do we do this in bitcoin? Well, we prevent against those buildtime attacks by using gitian reproducible builds which was invented by the bitcoin project and eventually adopted by the tor project. Gitian normalizes the build environment. It normalizes the environments such that it doesn't matter who builds it, the source code will correspond to the same output. So we will have bit-for-bit output and we will always get the same disk image each time.

We upload summaries of these build outputs to a repository on github and we sign those summaries. This is the gitian sigs repository. We call these gitian dot assert files. It might look intimidating at first, but it really isn't. Here's the input-- it's just bitcoin at some git tag like v0.18 and here's the output which is the disk image with the following hash. When we have these uploaded on to the repository, we compare them against each other after validating the signatures are good. We want to make sure all the hashes are the same and all the signatures are valid.

# Reproducible build

With this reproducible build system, then we are able to detect either malicious builders or something going wrong with their build system. This has become a bit of a movement in the open source software community. Tor was using gitian for reproducible builds for a while. I think the new version of debian requires that all new packages be reproducible, which is a great thing to see in this field.

# Toolchain and trusting trust

Okay, so we have reproducibility. Is reproducibility enough? No, it's still not enough.  This is clear if you go look at the dot assert files and you scroll down a little bit, you will see there's a long list of dependencies that we still depend on. Those are what constitutes our toolchain and our build environment. These are basically .deb files that we download from Ubuntu servers that we're just trusting as an opaque blob of things. We have no idea if these are the tools that we expect them to be, or something that is going to steal your keys.

The third circle of hell is trusting trust. Where does our build environment come from? Where does the toolchain come from? A toolchain is built in a similar way you make yogurt. The way you make yogurt is you add some milk to some yogurt and you make more yogurt. That's the same thing with source code and you feed it into a toolchain. This property of a toolchain lends it to a very novel attack. Ken Thompson described this in his 1984 Turing award lecture about trusting trust. It's the trusting trust attack. He described how because toolchains are built by older versions of themselves, you can poison an entire line of toolchains by poisoning just one generation of tools. So what this means is that you can be reproducible with gitian, but if the toolchain that we originally download from Ubuntu or Redhat or Apple is malicious then what we have is a reproducible system that is reproducibly malicious. So we're reproducible, but we're reproducibly malicious.

# Bootstrappability

What can we do about the fact that our toolchain consists of countless trusted binaries that can be reproducibly malicious and there's the possibility of a trusting trust attack propagating down the chain and us having no visibility into it? Well, we need to be more than reproducible, we need to be bootstrappable.

Being bootstrappable means that we can't have that many opaque binary tools that we trust to be downloaded from a third party server that can be changed at any time. We need to know how these tools are built and we need to be able to reproduce these tools from a preferably minimal trusted set of binaries. We need to maintain a minimal trusted bootstrap path from trusted binaries to everything else. This minimizes trust, and maximizes verification.

# guix

We need to use functional package managers like guix, which is a lot like nix if you guys know about that. It's a package manager if you know about that. Reproducibility and bootstrappability are fundamental tenants here. Every binary output that guix produces is a pure function of the source code and the toolchain used to produce it. Every package that guix builds can be traced back to a minimal set of trusted binaries. Let me show you what that means.

There's this heavy command called "guix graph packagename" and it will show all the dependencies, and with a few more flags it will show more dependencies, and if you give it all the flags then it will show you all the dependencies. This is a complete graph of all the dependencies required to build this package. In guix, every package has a dependency tree and they all have a root that has bootstrap binaries that it depends on.

For comparison, in debian, they have been having this problem of dependency hell where in their dependency tree they have a strongly connected component of 2000+ packages that has been around since 2013. It's really just only growing since then. Those are sort of the advantages of guix. For our toolchain with guix, if we use guix to build our toolchain then we can audit our how toolchain was built, we can easily bootstrap it from a minimal set of trusted binaries.

# Next steps

The software heritage foundation decided to use guix for their long-term project. Rust was one of the first languages to use guix, so shout out to them. And also scientific institutions are trying to use guix for reproducible scientific workflows. So the work going forward is to make the minimal set of trusted binaries even smaller; right now it's 232 MB which might sound like a lot but it's already a fraction of what debian is using. There's a mes bootstrap method which brings things down to 131 megabytes. At the end of the day, what we will hopefully do is incorporate a project called stage0 or hex0 which will bring it down to 357 bytes or so depending on architecture and all we'd have to do is look at these 357 bytes and easily audit it and fully commented x86 or whatever assembly code that is, and we would be able to bootstrap the whole world.

# See also

<https://diyhpl.us/wiki/transcripts/breaking-bitcoin/2019/bitcoin-build-system/>

